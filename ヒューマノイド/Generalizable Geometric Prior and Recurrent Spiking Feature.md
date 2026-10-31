---
title: "Generalizable Geometric Prior and Recurrent Spiking Feature Learning for Humanoid Robot Manipulation"
date: "2026-01-13"
authors: "Xuetao Li; Wenke Huang; Mang Ye; Jifeng Xuan; Bo Du; Sheng Liu"
url: https://arxiv.org/abs/2601.09031
pdf: https://arxiv.org/pdf/2601.09031
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.09031)** / [論文ページ](https://arxiv.org/abs/2601.09031)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

1 

# Generalizable Geometric Prior and Recurrent Spiking Feature Learning for Humanoid Robot Manipulation 

Xuetao Li ˙ID , Wenke Huang ˙ID , Mang Ye ˙ID , _Senior Member, IEEE_ , Jifeng Xuan ˙ID , _Member, IEEE_ Bo Du ˙ID , _Senior Member, IEEE_ , Sheng Liu ˙ID , _Fellow, IEEE_ , and Miao Li ˙ID , _Senior Member, IEEE_ 

**Abstract** —Humanoid robot manipulation is a crucial research area for executing diverse human-level tasks, involving high-level semantic reasoning and low-level action generation. However, precise scene understanding and sample-efficient learning from human demonstrations remain critical challenges, severely hindering the applicability and generalizability of existing frameworks. This paper presents a novel RGMP-S, Recurrent Geometric-prior Multimodal Policy with Spiking features, facilitating both high-level skill reasoning and data-efficient motion synthesis. To ground high-level reasoning in physical reality, we leverage lightweight 2D geometric inductive biases to enable precise 3D scene understanding within the vision-language model. Specifically, we construct a Long-horizon Geometric Prior Skill Selector that effectively aligns the semantic instructions with spatial constraints, ultimately achieving robust generalization in unseen environments. For the data efficiency issue in robotic action generation, we introduce a Recursive Adaptive Spiking Network. We parameterize robot-object interactions via recursive spiking for spatiotemporal consistency, fully distilling long-horizon dynamic features while mitigating the overfitting issue in sparse demonstration scenarios. Extensive experiments are conducted across the Maniskill simulation benchmark and three heterogeneous real-world robotic systems, encompassing a custom-developed humanoid, a desktop manipulator, and a commercial robotic platform. Empirical results substantiate the superiority of our method over state-of-the-art baselines and validate the efficacy of the proposed modules in diverse generalization scenarios. To facilitate reproducibility, the source code and video demonstrations are publicly available at https://github.com/xtli12/RGMP-S.git. 

**Index Terms** —Humanoid Robot Manipulation, Geometric Prior, Recurrent Spiking Feature Learning. 

✦ 

## **1 INTRODUCTION** 

H bodiedUMANOIDintelligence,robots representcapablea pivotalof mergingfrontierhigh-levelin emcognition with dexterous physical interaction [2], [3], largely propelled by the emergence of foundation models trained on massive-scale datasets [4]. However, in real-world deployment, robotic agents face inherently unstructured environments governed by complex physical laws, which differ significantly from the static internet data distributions used in pre-training [5], [6]. Due to the infinite variability of 3D scenes and the exorbitant cost of collecting highfidelity interaction data, the prevailing ”brute-force” scaling paradigm, which relies on exhaustive statistical memorization, becomes prohibitive and sample-inefficient for mastering dynamic manipulation tasks [7]. Driven by such realworld challenges, augmenting architectures with explicit geometric reasoning and spatial awareness has been increasingly explored, as it equips agents with structural inductive biases to decipher physical constraints effectively [8]. 

Vision-Language Models (VLMs), exemplified by PaLME and InstructBLIP, excel at parsing spatial semantic information from multimodal inputs to generate logical robotic 


Fig. 1. **Overview of our framework.** By integrating geometric commonsense with spatiotemporal features, our RGMP-S encodes the robottarget spatial relationships for manipulation tasks. RGMP-S achieves a 19% performance improvement and exhibits 5 _×_ greater data efficiency compared to the Diffusion Policy (DP) baseline. 

- _The authors are with the School of Computer Science, School of Robotics, Institute of Technological Sciences, Wuhan University, Wuhan, China 430072. E-mail:{xtli312, wenkehuang, yemang, jxuan, dubo, shengliu, miao.li}@whu.edu.cn, (Xuetao Li and Wenke Huang contributed equally, Jifeng Xuan and Miao Li are corresponding authors)._ 

- _A preliminary version of this work has appeared in Proceedings of the AAAI Conference on Artificial Intelligence (AAAI 2026) [1]._ 

task plans [9]–[11]. However, a critical gap remains in the execution phase: current architectures struggle to translate abstract instructions into contextually appropriate robotic skills [12]. The fundamental bottleneck lies in the 3D geometric grounding process, where VLMs, despite their proficiency in object identification, often fail to infer the physical 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

2 

interaction affordances dictated by specific geometries [13]. Specifically, regarding skill selection in open-world environments, this disconnect leads to a breakdown in differentiating manipulation primitives. Standard VLMs often confuse geometrically sensitive actions, such as grasping versus pinching, when encountering diverse object shapes [14], [15]. For instance, a model trained to grasp standard Coke cans typically targets the cylindrical sidewall. When presented with a crushed Coke can, the VLM retains semantic recognition but fails to perceive the structural deformation. Consequently, the robot attempts to execute the original side-grasping primitive, which is no longer physically feasible for the flattened geometry, resulting in task failure, as illustrated in Fig. 1. In fact, the flattened profile necessitates a pinching motion rather than the conventional side grasp. Such failures stem from a lack of explicit **geometric reasoning** . Existing approaches usually combine spatial indicators such as bounding boxes or contact points with high-level task descriptions [16], [17]. However, these methods predominantly rely on coarse semantic embeddings. In dynamic settings, such dependence results in plans that maintain semantic validity yet remain physically inexecutable [18]. This deficiency emphasizes the critical necessity for systems capable of verifying skill feasibility through rigorous geometric analysis. This leads to a core research question: **_I)_** _How can robots effectively exploit geometric reasoning to reliably select feasible manipulation skills?_ 

Despite the remarkable progress in robotic manipulation driven by generative models, deploying these policies in dynamic environments remains a formidable challenge. A predominant paradigm, Diffusion Policies, has demonstrated exceptional capability in modeling action space by leveraging Gaussian noise to represent robotic behaviors [19]. By learning the gradient of the data distribution, these methods can generate high-fidelity trajectories that capture humanlike dexterity [20]. However, this expressiveness comes at a steep computational cost. The inherent mechanism of diffusion models relies on an iterative reverse denoising process. As highlighted in recent analyses [4], [21], this sequential computation introduces prohibitive inference latency, rendering standard diffusion approaches ill-suited for high-frequency, responsive manipulation tasks where realtime feedback loops are critical. To circumvent the latency bottleneck of iterative solvers, recent advances in VisionLanguage-Action (VLA) models and Transformer-based architectures advocate for direct, end-to-end action generation [4], [12], [22]. These methods typically tokenize visual observations and directly predict actions in a feed-forward manner, ensuring rapid inference. However, achieving robust generalization with these architectures has historically demanded a brute-force strategy: scaling model parameters to billions and training on massive, diverse datasets. While effective at scale, this approach is data-inefficient and computationally heavy. Crucially, these methods often treat visual inputs as flattened sequences of semantic tokens, ignoring the intrinsic spatiotemporal mechanisms of manipulation. They lack explicit inductive biases to capture the fine-grained **spatial relationships** between the robotic endeffector and the target object, and often fail to distinguish task-relevant features from the dense, noisy visual context [23], [24]. Consequently, without massive data covering 

every variation, these black-box mappings are prone to latching onto spurious background correlations, leading to poor performance under domain shifts or in cluttered scenes [25]. Thus, a critical research gap exists between the need for expressive, real-time control and the requirement for data-efficient generalization. The challenge lies in moving beyond simple parameter scaling or inefficient iterative denoising. Instead, we must explore how to construct an architecture that naturally embeds the spatiotemporal structure of manipulation tasks. This leads to the other core research question: **_II)_** _How can robots effectively learn robust dataefficient policies from limited demonstrations?_ 

To surmount the deficiency in spatial-geometric reasoning outlined in **_I)_** , inspired by the efficiency of human cognitive processes in synthesizing vision and logic, a preliminary version of this work published in AAAI 2026 [1] explores geometric priors via a lightweight commonsense tuning strategy. In particular, we aim to bridge the gap between 3D geometric perception and semantic task planning through implicit geometric information decoding from 2D inputs. Traditional explicit 3D reconstruction provides detailed spatial information, but it exhibits high computational latency and sensitivity to noise [26], and lacks of adaptability for real-time robotic interaction. This motivates us to bypass costly reconstruction in favor of capturing implicit geometric structures directly from RGB inputs. We propose the **Long-horizon Geometric-prior Skill Selector** (LGSS) to encode spatial affordances into the latent space of the policy, effectively aligning 3D spatial indicators with robotic action spaces and commonsense reasoning. Specifically, we integrate geometric inductive biases into a VLM with minimal fine-tuning, requiring only a concise set of rule-based constraints. This approach offers a practical solution to realize robust decision-making in unseen environments. Furthermore, we believe that LGSS is essential because it introduces a decision-making process analogous to human cognition [27], which mirrors the human ability to synthesize an action plan for the long-horizon manipulation task. To this end, we develop the LGSS framework to enable the manipulation of diverse objects via rigorous geometric consistency checks, proving its effectiveness and robustness in real-world humanoid deployment. 

To surmount the overfitting risks inherent to limited data ( **_II_** ), we deviate from data-hungry scaling and instead embed explicit spatiotemporal inductive biases via recursive spiking dynamics, enabling the efficient distillation of robust skills from sparse demonstrations. In our conference version [1], we employed recurrent computation to construct spatial relationships between the robotic end-effector and the target object, offering a foundational policy for action generation. However, standard recursive models are prone to vanishing gradients during global modeling [29] and often struggle to distinguish task-salient features from complex backgrounds [30]. We posit that effective spatial memory requires dynamic regulation to prevent the loss of key historical cues while suppressing noise. Purely spatial processing lacks the temporal reasoning necessary to filter redundant information from dense visual features [31]. This motivates us to introduce an adaptive mechanism that integrates spiking information to refine feature retention. In this journal version, we propose the **Recursive Adaptive Spik-** 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

3 


Fig. 2. **Pipeline of RGMP-S** . Upon receiving a speech command, the robot utilizes LGSS (see § 3.1 for details) to identify and localize the target object. By integrating object coordinates, shape cues (extracted via Yolov8n-seg [28] model _ϕ_ ), and geometric-prior knowledge, the robot selects an appropriate skill from the library, where each primitive is associated with a pretrained RASNet model (see § 3.2 for details). The selected RASNet model subsequently executes the task precisely through adaptive recursive feature extraction and GMM-based refinement. 

**ing Network** (RASNet), which incorporates Spiking Dense Feature Extraction (SDFE) to embed temporal reasoning into spatial feature understanding. We utilize Rotary Position Embeddings (RoPE) and recursive computation to form a global spatial memory, while simultaneously deploying an Adaptive Decay Mechanism and Adaptive Spike Neurons (ASN) to dynamically control memory retention and amplify task-critical features. Finally, we apply Gaussian Mixture Models (GMM) to approximate the joint motions. Compared with our conference version, SDFE not only effectively suppresses redundancy within dense information but also significantly enhances the generalization ability in unseen scenarios featuring complex backgrounds. 

Our primary contribution is to present RGMP-S, a unified framework that bridges the semantic-geometric gap to achieve robust, data-efficient, and generalizable robotic manipulation. To successfully facilitate high-level skill reasoning and low-level motion synthesis, we present the following technical contributions: 

- **Long-horizon Geometric-prior Skill Selector (LGSS).** We introduce a lightweight geometric tuning strategy that fuses vision-language models with low-rank geometric adapters. By injecting shape-level commonsense biases, LGSS aligns semantic instructions with latent geometric constraints, enabling the precise selection of parameterized skills from a pretrained library without requiring task-specific fine-tuning. 

- **Recursive Adaptive Spiking Network (RASNet).** We formulate a novel policy architecture to investigate intrinsic spatiotemporal mechanisms in robotic manipulation. By modulating latent representations through Adaptive Spike Neurons (ASN) and recursive computation, this network captures directional spatial dependencies within a spatiotemporally consistent latent space. This design effectively distills task-critical features from dense visual observations while mitigating optimization conflicts in sparse data regimes. 

- **Data-Efficient Generalization.** We conduct a rigorous validation of the RGMP-S framework across the ManiSkill benchmark and three diverse physical robotic platforms. Extensive real-world experiments demonstrate that our framework ensures robustness against dynamic disturbances, significantly outperforming the Diffusion Policy baseline with an 89% generalization success rate and 5 _×_ superior data efficiency. 

This manuscript represents a substantial extension of our preliminary version published in AAAI 2026 [1]. We augment the original work in the following aspects: 

- **Algorithmic Advancement in Reasoning.** We advance the preliminary skill selector to the LGSS via a hierarchical Chain-of-Thought (CoT) mechanism. This enhancement enables the structured decomposition of intricate goals into multi-stage sequences, significantly boosting performance on long-horizon manipulation 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

4 

- tasks (e.g., towel folding and water pouring). 

- **Architectural Evolution for Robustness.** We evolve the previous visuomotor module with Spiking Dense Feature Extraction (SDFE) and Adaptive Spike Neurons (ASN) to dynamically filter redundant visual noise in cluttered scenes (as shown in Fig. 2). This addresses the limitations of the original model regarding feature redundancy and lack of temporal logic, ensuring robust action synthesis in unstructured environments. 

- **Expanded Real-World Evaluation.** We broaden the experimental scope by incorporating a commercial Aloha robot [32] and introducing three additional challenging long-horizon manipulation tasks: towel folding, water pouring, and bin picking, as detailed in § 4.1. 

## **2 RELATED WORK** 

### **2.1 Vision-Language Models for Robotic Manipulation** 

**Semantic Planning and Grounding** . A pioneering line of work leverages the semantic reasoning capabilities of Large Language Models (LLMs) and Vision-Language Models (VLMs) to decompose high-level instructions into a sequence of robotic primitives [9], [10], [13]. While these foundation models excel at high-level task planning, they often treat the physical world as a semantic abstraction. Consequently, they suffer from a _semantic-geometric gap_ , where the generated plans are logically sound but physically inexecutable due to a lack of low-level spatial awareness. Subsequently, a large body of methods [33]–[36] began to incorporate explicit 3D representations, such as voxels or neural radiance fields, to ground semantic queries into physical space. For instance, recent research has explored establishing dense correspondence between visual observations and linguistic concepts to enhance manipulation precision [37]. These methods mainly focus on explicit 3D reconstruction or external trajectory solvers to bridge the gap. However, when robots operate in unstructured open-world environments, explicit reconstruction exhibits high computational latency and sensitivity to perception noise [26]. Meanwhile, relying on external motion planners separates semantic reasoning from control, which is a suboptimal setting for dynamic interaction. In this paper, we focus on learning implicit geometric priors directly from 2D RGB inputs. By fusing geometric adapters with VLMs, our LGSS avoids costly reconstruction while maintaining robust spatial reasoning. **Geometric Reasoning in Manipulation** . With the demand for precise object interaction, geometric-aware manipulation has been an active research field. One direction is introducing object-centric representations [38], [39] that predict keypoints or 6-DoF poses. However, these techniques struggle with category-agnostic objects or deformable materials where defining canonical poses is difficult. Recently, a specific line of research [14], [15], [40] leverages affordance maps or contact primitives to guide grasping. Therefore, these approaches heavily rely on the quality of pre-defined primitives and often fail to distinguish fine-grained manipulation modes (e.g., grasping versus pinching) under structural deformation. Recent works [16], [41], [42] have proven the feasibility of combining bounding boxes with language. However, these methods reach only coarse spatial alignment, which is not suitable for learning a generalizable 

policy for diverse geometries and thus lead to task failure in unseen scenarios. In this paper, based on the Geometric Prior Skill Selector, we inject shape-level commonsense biases to enforce rigorous geometric consistency checks, thereby effectively mitigating uncertainties and handling dynamic constraints to ensure robust reasoning in tasks. 

### **2.2 Generative Robotic Policy Learning** 

Imitation learning [43], [44] has been an essential paradigm in robotics, with the goal of acquiring robust policies from expert demonstrations [45]. Existing works can be broadly divided into two branches: Transformer-based methods [22], [46]–[48] and Diffusion-based methods [19], [49]. Transformer architectures, such as the Decision Transformer [50], treat control as a sequence modeling problem. Specifically, self-attention mechanisms in Transformers have been shown to effectively capture global dependencies [51]. However, achieving generalization with Transformers has historically demanded a brute-force scaling strategy involving billions of parameters and massive datasets [4]. In contrast, Diffusion Policies, they model the action distribution using iterative denoising processes. Despite their expressiveness in capturing multimodal distributions, the sequential denoising computation introduces prohibitive inference latency. Unlike standard diffusion approaches, we focus on a feedforward recursive architecture that ensures high-frequency real-time responsiveness without the heavy computational strain typically associated with iterative solvers. 

### **2.3 Spatiotemporal Representation** 

Learning effective spatiotemporal representations is critical for mastering dynamic tasks. Traditional approaches utilize Recurrent Neural Networks (RNNs) or LSTMs [52] to model temporal dependencies. However, standard recursive models are prone to vanishing gradients and often struggle to filter redundant information from dense visual streams. Recently, Spiking Neural Networks (SNNs) have emerged as a powerful method for processing temporal information with high energy efficiency and sparse computation [53]– [55]. Related methods have explored SNNs for event-based vision and motion estimation [54], [56]. The key difference between our RASNet and the aforementioned efforts is that ours is designed for dense visual feature extraction rather than purely neuromorphic processing. Inspired by the efficiency of spiking neurons, we construct the Adaptive Spike Neuron (ASN) to modulate feature retention. Furthermore, we investigate how to better maintain global spatial dependencies and develop the Recursive Adaptive Spiking Network, which captures intrinsic spatiotemporal mechanisms and ensures data efficiency under limited demonstrations. 

## **3 METHODOLOGY** 

**Overview of RGMP-S.** To achieve generalizable robotic manipulation, we introduce **R** ecurrent **G** eometric-prior **M** ultimodal **P** olicy with **S** piking Features (RGMP-S). This framework generates task plans and 6-DoF actions for humanoid robots using egocentric RGB inputs. RGMP-S comprises two key components: the **L** ong-horizon **G** eometricprior **S** kill **S** elector (LGSS) and the **R** ecursive **A** daptive 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

5 

TABLE 1 **Notations** table. 

||Description||Description|
|---|---|---|---|
|_P_|Generated action plan|_I_|Current user instruction|
|_O_|Current visual observation|_C_|Predefined contextual set|
|_Pi_|Action sequence (Eq. (1))|_W_|Adaptive decay factors (Eq. (3))|
|_F_0|Initial feature map (Eq. (2))|_Xk_|Spatial attention mask (Eq. (9))|
|_Bk_|Spatial attention feature (Eq. (9))|_Dk_|Feature for attention processing|
|_QA_|Spiking dense feature (Eq. (11))|_Fk_|Extracted dense feature map|
|_A_|Adaptive spike neuron function|_µk_|Mean of_k_-th GMM component|
|_Ff_|Fused feature map (Eq. (14))|_ain_|Initial action prediction (Eq. (16))|
|Σ_k_|Covariance of_k_-th GMM component|_lk_|Mahalanobis distance (Eq. (20))|
|_K_|Number of GMM components|_µ_<sup>_ω_</sup><br>_k_|<sup>Mean of</sup><sup>_k_-th GMM component</sup>|


**S** piking **Net** work (RASNet). The LGSS translates natural language commands and visual observations into executable skill sequences by incorporating geometric commonsense priors. Complementarily, the RASNet converts visual inputs into robotic manipulation actions through spatiotemporal memory modeling. 

Instead of employing computationally expensive explicit 3D reconstruction, the policy learns to extract implicit geometric information from RGB inputs by correlating spatial cues with action labels and commonsense reasoning. Additionally, we incorporate spiking neural networks to process dense features that capture fine-grained spatial perception. This approach enables the model to focus on task-relevant visual regions, emphasizing important details while suppressing redundant information, thus enhancing performance. This method is inspired by the natural and intuitive process of human object manipulation. In human grasping, the eyes first detect the target object, and the brain rapidly processes this sensory input to generate an appropriate motor command for the hand, allowing the arm to execute the grasping action and complete the task successfully. Similarly, our RGMP-S mimics this process by seamlessly integrating perception with action: the RGB image is analyzed to identify the object and its relevant geometric context, while the RASNet is employed to predict the joint angles required for the robotic arm to grasp the object. A summary of notations is provided in Tab. 1. 

### **3.1 Long-horizon Geometric-prior Skill Selector** 

**Motivation of Geometric Priors.** A fundamental challenge in robotics is the precise selection of skills (e.g., grasping versus pinching) for objects with diverse geometries or in previously unseen scenarios. While VLMs support object recognition and localization, they often struggle to translate semantic information into accurate actions, primarily due to their lack of explicit integration of **geometric priors** in the vision-action mapping process. This limitation motivates the development of our novel LGSS framework, which seamlessly combines geometric reasoning with semantic task planning through geometric commonsense alignment. 

The LGSS operates through two sequential phases to bridge semantic instruction and physical execution. Initially, a VLM [57] is employed to interpret human instructions, allowing the robot to detect and locate the target object within the provided image. This visual grounding step generates bounding boxes that anchor subsequent reasoning processes. Building on this visual localization, the system then analyzes spatial relationships and morphological characteristics of the identified objects. This geometric analysis 

incorporates commonsense knowledge about object properties and their functional implications for manipulation. The resulting object-centric representation, combining semantic and geometric features, guides the selection of appropriate manipulation strategies from a predefined skill library. This structured approach enables the robot to translate abstract commands into context-aware action sequences through a novel geometric-object decomposition mechanism that coordinates perception with action selection: 


where _P_ represents the generated action plan, _I_ is the current natural language user instruction, _O_ denotes the current visual observation, and _C_ constitutes a predefined contextual set containing _n_ examples _{_ ( _Ii, Oi, Pi_ ) _}i_<sup>_n_</sup> =1<sup>,which</sup> encapsulates instructions, prompts, and commonsense reasoning to facilitate in-context learning. 

The system processes an RGB image _O_ where a VisualLanguage Model first identifies the target object with a bounding box. This localization provides the foundation for generating executable manipulation skills. The model combines predefined context _C_ with geometric properties like spatial relationships and object shape to determine these skills. For example, when receiving the instruction _“I want Fanta”_ , the LGSS follows the contextual prompt _“Please box the target object in the instruction”_ . It locates the specific beverage can among other items, then uses YOLOv8n-seg to determine its shape. Finally, the visual-language model integrates contextual information _C_ with geometric reasoning to produce operational commands. 

The LGSS adopts a modular design with minimal computational overhead. Its architecture integrates three key components: a visual-language interpretation module for command processing, a semantic segmentation module for object analysis, and a prompt-based skill selector for action determination. These elements operate synergistically to transform user instructions and visual inputs into appropriate skill choices. The complete inference process requires 105 milliseconds when executed on an NVIDIA 4090 GPU. **Visual-Language Interpretation Module:** This component employs the Qwen-vl API for visual-language understanding, utilizing structured prompt engineering to incorporate prior knowledge. The preparation involves providing the API with carefully selected training instances, each containing: (1) an RGB image with an object bounding box, (2) corresponding semantic segmentation results, (3) manually annotated shape categories (such as “cylindrical” or “crushed”), and (4) the corresponding manipulation skill. For example, training data includes a Fanta can image with a bounding box and segmentation mask, labeled as “cylindrical shape” and paired with the “side grasp”; similarly, an encircled Fanta can is associated with the “lift up”. The model is primed with 20 representative examples spanning common object categories to establish a robust mapping between visual features, geometric attributes, and manipulation strategies. During operation, the API processes input prompts formatted as: _“Instruction: Identify target object in image and output bounding box [x1, y1, x2, y2]”_ . This configuration achieves 93.1% localization accuracy on our dataset with a mean latency of 45 ms per query. 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

6 


Fig. 3. **Structure of Spatial Mixing Block and Channel Mixing Block.** The Spatial Mixing Block uses ADM to generate Dynamic Decay _W_ recursively, and employs RoPE to introduce directional awareness relative to spatial positions. These mechanisms collectively enhance the ability of the block to integrate spatial information effectively. The Channel Mixing Block reallocates channel-wise feature responses by integrating correlations between channels. See § 3.2 for details. 

**Semantic Segmentation Module:** This component processes the bounding box coordinates provided by the Qwenvl API by extracting the corresponding image region and passing it to a YOLOv8-seg model. The model, which has been pre-trained on large-scale datasets and subsequently fine-tuned on our proprietary data, generates precise semantic segmentation masks to capture the object’s geometric structure. On our evaluation dataset, the module achieves a mean Intersection over Union (mIoU) of 97.6%, demonstrating the reliability of its shape extraction capabilities for subsequent geometric reasoning. 

**Geometry-Grounded CoT Skill Reasoner:** This module orchestrates the translation of perceptual inputs into executable actions by synthesizing bounding box coordinates with morphological features via the Qwen-vl reasoning engine. Instead of simple instruction following, we deploy a structured Chain-of-Thought (CoT) protocol to enforce physical grounding. The system is instantiated with a constraint-aware prompt: “ _You are a robot with five skills: Side Grasp, Lift Up, Top Pinch, Pour Water and Delivery. The image you are observing has a resolution of 640x480. Based on the observation, the coordinates of the bounding box and the shape information of the object, choose the skill without collision and generate an action plan based on these skills._ ” By embedding task-specific primitives (e.g., Side Grasp, Pour Water) within this reasoning framework, the model explicitly maps latent geometric affordances to appropriate manipulation strategies. Crucially, this mechanism resolves operational ambiguities by integrating safety-critical constraints, prioritizing kinematically feasible and collision-free interactions based on environmental context. The final decision is derived from a confidence-weighted assessment of candidate skills, ensuring robust planning under uncertainty. 

**Skill Library** The skill library encompasses a comprehensive set of predefined grasping configurations parameterized by finger joint angles, supporting three core manipulation primitives. Side grasping is employed when objects can be accessed laterally without obstruction. Lifting is utilized 

for vertical retrieval, often in contexts where obstacles limit horizontal approach. Pinching is reserved for handling thin or delicate items such as paper sheets and cables. These skills define hand posture without imposing object-specific constraints. The LGSS selects the appropriate skill by combining geometric priors with real-time RGB observations, determining feasible hand configurations for the current scenario. Each skill corresponds to distinct model parameters, and the RGMP-S subsequently generates corresponding action trajectories dynamically during real-time inference. 

### **3.2 Recursive Adaptive Spiking Network** 

**Motivation of RASNet.** Effective robotic operation necessitates a precise understanding of spatial relationships within visual scenes, particularly the correspondence between image regions and the robotic end-effector position. Existing methods often face challenges in inferring such relational structures in novel environments, primarily due to limitations in modeling spatial relationships and dense representation learning that hinder generalization. To address this issue, we introduce the RASNet framework. This framework adaptively learns spatial dependencies between the robot and target objects in previously unseen settings through recursive spiking feature processing, while enhancing robustness and mitigating overfitting by employing Gaussian action space modeling when training data is scarce. 

Our RASNet advances action generation through three interconnected technical innovations. An Adaptive Decay Mechanism (ADM) dynamically regulates the retention of historical context, enabling the model to capture long-range dependencies while maintaining spatial accuracy. Adaptive spiking neurons selectively amplify task-relevant visual features, such as object contours, and suppress non-essential background information within dense feature maps. These elements are unified by a hierarchical fusion framework, which seamlessly integrates multi-scale representations to preserve both high-level semantics and detailed spatial structure through learned attention weighting. 

Specifically, the RASNet comprises three principal components: (1) a Stem layer for preliminary feature extraction, (2) three hierarchical processing stages, each containing two RASNet blocks, and (3) a multi-scale feature fusion module integrated with a GMM, as illustrated in Fig. 2. Given an input RGB image _O ∈_ R<sup>_H×W ×_3</sup> , the Stem layer performs initial spatial downsampling and feature embedding, reducing the resolution to<sup>_<u>H</u>_</sup> 4<sup>_×_</sup><sup>_<u>W</u>_</sup> 4<sup>whilepreservingcriticallow-</sup> frequency information. This design significantly mitigates computational overhead for subsequent operations. The transformation can be formally expressed as: _F_ 0 = _P_ ( _SReLU_ ( _BN_ ( _C_ 3 _×_ 3( _O_ )))) _,_ (2) 

where _C_ 3 _×_ 3( _·_ ) denotes a 3 _×_ 3 convolutional layer, _BN_ ( _·_ ) refers to batch normalization, and _SReLU_ ( _·_ ) represents the Squared ReLU activation function. This activation improves gradient flow and increases the network’s nonlinear representational capacity. The operator _P_ ( _·_ ) corresponds to a max pooling layer. The resulting feature map _F_ 0 is then split into two parallel processing pipelines within the RASNet block at Stage 1: one for dynamic recursive computation and another for spiking-based dense feature extraction. 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

7 

**Dynamic Recursive Computation.** In this branch, _F_ 0 is first processed by the ADM to generate content-adaptive decay factors that modulate historical memory retention. This process extracts local spatial information through convolutional layers, applies channel-wise recalibration, and constrains the decay factor to the range [0 _,_ 1] via a sigmoid activation function, formulated as: 


where _C_ 1 _×_ 1( _·_ ) denotes a 1 _×_ 1 convolutional layer that performs channel-wise recalibration, and _σ_ ( _·_ ) represents the sigmoid activation function. We then apply Rotary Position Embeddings (RoPE) to encode positional information via geometric rotations in feature space. This method enhances the capacity of model to capture position-sensitive dependencies. Unlike standard additive or learnable position embeddings, RoPE incorporates relative position awareness by applying rotational transformations to queries and keys during attention computation. This design offers two main advantages: it removes learnable position parameters, thereby reducing overfitting risk while preserving efficiency; and it encodes positional offsets as angular shifts, ensuring attention scores inherently reflect relative token distances. Formally, we first generate the keys _Ks_ and values _Vs_ from _F_ 0 via a 1 _×_ 1 convolution. To incorporate positional awareness, we apply the rotation matrix **R** Θ to pairs of channels in _Ks_ . The rotation matrix is defined as: 


where _xh_ and _xw_ represent the discrete horizontal and vertical coordinates of a pixel, and the frequency parameter _θ_ controls the rotation speed across channel dimensions (indexed by _j ∈_ [0 _, C/_ 2)). Using a base constant of 10000, lowfrequency components emphasize global structure, while high-frequency components capture local positional details. By applying **R** Θ( _x_ ) to the query and key representations, we ensure that their inner product encodes relative positional information. After positional encoding, _Ks_ and _Vs_ are partitioned into 16 _×_ 16 image patches. Sequential dependencies among these patches are modeled using a recurrent _WKV_ mechanism: 


where _i ∈_ [0 _,_ ( _H × W_ ) _/_ (16 _×_ 16)) indexes the sequence of image patches, and exp( _·_ ) denotes the element-wise exponential function. _ki_ and _vi_ denote the corresponding patch representations extracted from _Ks_ and _Vs_ . To ensure consistent accumulation, the initial states (at step _i_ = 0) are set as _n_ 0 = _k_ 0 _⊙ v_ 0 and _d_ 0 = _k_ 0. The term _u ∈_ (0 _,_ 1) represents a learnable position bias, and _W ∈_ R<sup>_C_</sup> is the channel-wise time-decay vector. 

**Motivation of Spatial Memory.** The recurrent connections in our framework build a spatial memory of observed 

scenes for the robot. This memory supports locating endeffector positions that are most relevant to the current task. However, recurrent computation is prone to vanishing gradients, which complicates training and often requires large amounts of data to alleviate this issue. To overcome this issue, we introduce an Adaptive Decay Mechanism that dynamically adjusts the decay rate of historical memory, preserving essential spatial information while adaptively emphasizing task-critical image patches. Here _W_ denotes the content-adaptive decay factors that govern memory retention (Eq. (3)). Finally, a gating factor _Rs_ produces a dynamic weight to modulate how the output of the Spatial Mixing Block influences the current state: 


Then we apply the Channel Mixing Block to _FS_ 0 to reallocate channel-wise feature weights for feature extraction: _FC_ 0 = _σ_ ( _C_ 1 _×_ 1( _FS_ 0)) _⊙_ ( _SReLU_ ( _C_ 3 _×_ 3( _FS_ 0))) (8) 

**Spiking Dense Feature Extraction.** In the parallel branch, dense visual features are extracted using a Dense Block. These features capture contextual information and textural details of target objects. The input _F_ 0 _∈_ R _<u>H</u>_ 4<sup>_×_</sup><sup>_<u>W</u>_</sup> 4<sup>_×C_</sup> is processed by the Dense Block, yielding an enriched representation _Fk ∈_ R _<u>H</u>_ 4<sup>_×_</sup><sup>_<u>W</u>_</sup> 4<sup>_×_4</sup><sup>_C_</sup> . This output then passes through a Linear layer with _C/r_ output channels, producing two new feature maps _Bk_ and _Dk_ . The map _Bk_ is subsequently used to generate a spatial attention mask _Xk_ : 


where _I_<sup>¯</sup> = _n_ <u>1</u> � _I − n_ <u>1</u><sup>**1**</sup> � and _n_ = _h × w_ . _I_ and **1** are the _n × n_ identity matrix and matrix of all ones, respectively, and _Xk ∈_ R<sup>_n×n_</sup> . We define _x_ ( _i,j_ ) _∈ Xk_ (where 0 _≤ i < n_ ; 0 _≤ j < n_ ), which encodes the global dependencies between the _i_ -th pixel and the _j_ -th pixel from _Bk_ . _Xk_ is fed into a softmax function and then multiplied by _Dk_ : 


Then, _Uk_ is reshaped and transposed to R<sup>_n×C/r_</sup> . Subsequently, it is fed to a 1 _×_ 1 convolutional layer and added to the spiking feature _A_ ( _Fk_ ) by our adaptive spike neuron: 


**Motivation of Adaptive Spike Neuron.** Current robotic manipulation models typically generate actions based solely on spatial perception, overlooking temporal information. To incorporate temporal reasoning into spatial feature understanding, we employ a spiking neuron mechanism. Conventional spiking neurons combine spatial information from previous timesteps with a decay factor to modulate the current signal, enabling robots to integrate observations from past frames when processing current visual input. However, traditional spiking neurons rely on a fixed decay factor and a binary signaling mechanism, which introduce training difficulties in spiking neural networks due to nondifferentiable operations during gradient backpropagation. To address these issues, we introduce an adaptive spiking neuron. Our design replaces the static decay factor with a dynamically adjustable one at each timestep. Training focuses on learning this adaptive decay factor rather than 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

8 

directly optimizing the spiking neural network parameters. This approach mitigates the refractory period characteristic of spiking neurons and resolves gradient propagation challenges posed by non-differentiable components, resulting in a more stable and efficient learning process. The governing equations of our adaptive spike neuron are detailed as: 


where ∆ _t_ denotes the time interval (typically unit time), and _Vt_ represents the membrane potential obtained through integration of spatial input _Xt_ and temporal input _Ht−_ 1. Here _Xt_ is extracted from dense visual features, and _Ht−_ 1 corresponds to the membrane potential from the previous timestep after undergoing reset or spike emission. If the membrane potential exceeds the threshold _uth_ , the neuron fires a spike; otherwise, it remains silent. The function Θ( _·_ ) denotes the Heaviside step function, defined as Θ( _x_ ) = 1 for _x ≥_ 0 and Θ( _x_ ) = 0 otherwise, yielding a binary output _St ∈{_ 0 _,_ 1 _}_ . The term _Ht_ indicates the temporal output, where _τ_ represents the adaptive decay factor produced by our channel-wise attention mechanism. The reset potential _V_ reset is engaged after a spike is fired. In the absence of firing, _Vt_ decays exponentially according to the adaptive factor _τ_ . To create an adaptive decay factor _τ_ suited for particular tasks, the computation of _τ_ is seamlessly incorporated into the gradient backpropagation process of the policy: 


where E[ _·_ ] computes the average of mapped values across channels, and _R_ ( _·_ ) denotes a feature reshaping operation. This integration enables the decay factor to adjust dynamically based on the complexity of the current motion sequence. Finally, we apply a 1 _×_ 1 convolutional layer to _QA_ to obtain query vectors _Q_ with matching channel dimensions to the key and value vectors _K_ and _V_ . A guided selfattention mechanism then merges the dynamically recurrent features and the spiking-based dense features as follows: 


where _dk_ denotes the dimensionality of the queries and keys, and _B_ represents a relative position bias. The feature map _F_ 1 is produced by down-sampling the output from two successive RASNet blocks using a 3 _×_ 3 convolution. This procedure is repeated in Stage 2 and Stage 3. The resulting multi-scale features _F_ 1, _F_ 2, and _F_ 3 are subsequently fused through a set of learnable weights: 


where _Fi_ represents the feature map produced at Stage _i_ (with _i_ = 1 _,_ 2 _,_ 3), and _αi_ denotes learnable parameters that weight each level during feature fusion. The fused feature map _Ff_ is then used to generate an initial action prediction: 


To train the model, we minimize the mean-squared error between the predicted action and the ground-truth action from human demonstrations using the following loss: 


**Algorithm 1:** The RGMP-S Framework 

**Input:** Training epochs _E_ , conversation round _T_ , human instructions _I_ , human demonstrations _D_ with capacity _M_ , current observation _O_ , VLM model _W_ , Stage of RGMP-S _S_ , RGMP-S _Gm_ 

**Output:** Robotic actions _a_<sup>_∗_</sup> 

/* Human Demonstration Collecting: */ **for** _i_ = 1 _,_ 2 _, ..., M_ **do** _di ←_ ( _Oi, Ji_ ) through Eq. (21) ; // § 4.1 _D ←D ∪{di}_ Θ _←_ EM( _D_ ) via Eq. (18) return _D_ , Θ /* RGMP-S Training pipeline: */ **for** _e_ = 1 _,_ 2 _, ..., E_ **do** _F_ 0 _← Stem_ ( _Oi_ ) by Eq. (2) ; // § 3.2 _W, Ks, Vs ←A⌈_ ( _F_ 0), _R_ ( _F_ 0) by Eq. (3), Eq. (4) _F_ 1 _, F_ 2 _, F_ 3 _←S_ ( _Ks, Vs, W_ ) _×_ 3 _ain ←M_ ( _F_ 1 _, F_ 2 _, F_ 3) by Eq. (16) _L ←_ ( _ain, aground_ ) through Eq. (17) _Gm ←Gm − η∇L_ return _Gm_ /* Inference pipeline: */ **for** _t_ = 1 _,_ 2 _, ..., T_ **do** _Box_ ( _x_ 1 _, y_ 1 _, x_ 2 _, y_ 2) _←Q_ ( _I, O|C_ ) by Eq. (1) _Os ←_ ( _x_ 1 _, y_ 1 _, x_ 2 _, y_ 2) _, ϕa_ ( _O, Box_ ) _Sseq, P ←QCoT_ ( _I, Os|C_ ) Voice _←_ response in _P_ **if** _Sseq̸_ = _∅_ **then for** _sk_ in _Sseq_ **do** _a_<sup>_∗_</sup> _←Gm_ ( _O, sk,_ Θ) through Eq. (20) Execute _a_<sup>_∗_</sup> 

where _L_ is the loss and _a_ ground is the ground-truth action. **Motivation of Gaussian Mixture Model.** A single Gaussian distribution [19] often regresses to the mean, which can suppress distinct action modes and compromise control precision. To better represent the multi-modal nature of robotic actions, we adopt a Gaussian Mixture Model (GMM). Let **x** _∈_ R<sup>_n_</sup> denote the ground-truth joint configuration. The GMM with _K_ = 6 components is defined as: 


where _αk_ , _µk_ , and Σ _k_ denote the prior weight, mean, and covariance of the _k_ -th component. These parameters are estimated via the expectation-maximization algorithm to maximize the data likelihood. To refine the initial prediction _a_ in, we compute the Mahalanobis distance to each GMM component. As the intrinsic metric for Gaussian distributions, it utilizes covariance to normalize deviations, ensuring statistical consistency by penalizing errors in lowvariance dimensions: 


The final action _a_<sup>_∗_</sup> corresponds to the mean vector of the component with the smallest distance: 


The pseudocode of RGMP-S is presented in Algorithm 1. 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

9 


Fig. 4. **Hardware configuration of our humanoid robot.** The platform integrates several core subsystems: an NVIDIA Jetson AGX Orin module for onboard computation; a head-mounted RGB camera for egocentric vision; an omnidirectional microphone array for audio input; a 6-degree-offreedom robotic arm paired with a dexterous hand for manipulation; and a multi-axis joint module for torso mobility. These components collectively enable environmental perception, physical interaction, and autonomous movement. See § 4.1 for details. 

## **4 EXPERIMENTS** 

This section presents a systematic experimental evaluation of the proposed RGMP-S framework. Our experiments aim to validate the effectiveness and generalization capacity of the overall architecture and its two core modules: the LGSS and the RASNet. We analyze the distinct contribution of each module and compare the full framework against several state-of-the-art baselines on a range of manipulation tasks. The following sections detail the experimental setup, implementation specifics, evaluation metrics, and present a comprehensive discussion of the results. 

**Dataset and Evaluation Criteria** . To verify the efficacy of the proposed RGMP-S framework, we curated a comprehensive dataset comprising 500 expert trajectories within the skill library. Each trajectory constitutes an operational path paired with a visual observation captured immediately before the initiation of a robotic task. In particular, the visual input facilitates the mapping to a specific action, while the trajectory delineates the transition of the manipulator from the starting configuration to the target spatial coordinates and end-effector pose. This data collection process is formulated in the following manner. 


### **4.1 Experimental Setup** 

**Hardware Setup** . Our experiments are conducted on three distinct robotic platforms. The primary platform is an upper-body humanoid robot with four integrated subsystems: vision, audio, decision-making, and actuation. A head-mounted egocentric RGB camera provides primary visual input. An iFLYTEK S0Y22F omnidirectional microphone and speaker array, mounted on the torso, handles voice interaction. An onboard NVIDIA Orin compute module performs high-level behavioral planning. The actuation system consists of two 6-degree-of-freedom (6-DOF) robotic arms, each equipped with a 6-DOF dexterous hand. The entire system (as shown in Fig. 4) is self-powered and communicates via a local wireless network, enabling fully untethered operation. To assess cross-embodiment generalization, we also employ a desktop dual-arm manipulation robot. This secondary platform is equipped with an overhead RGB camera and two 6-DOF robotic arms dedicated to executing precise physical manipulation tasks. The third platform comprises the Aloha robot, which incorporates a centrally positioned RGB camera and dual robotic arms equipped with wrist-mounted RGB sensors. 

where _J_ signifies the joint space of the robotic system and _O_ represents the corresponding perceptual observation. During physical experiments, the system performance is quantified via two complementary metrics. The skill selection accuracy _Accs_ represents the capability of the model to identify the appropriate primitive for a given instruction. Furthermore, the execution success rate _Acct_ evaluates the precision with which the manipulator interacts with the target object. Consequently, the comprehensive success rate _Acc_ is defined as the product of these two components. 


**Real-world Task Configurations.** To verify the performance of the RGMP-S, we conduct a comprehensive comparative evaluation against several state-of-the-art baselines across 10 manipulation tasks. This evaluation suite comprises five simulation tasks from the ManiSkill2 benchmark and five physical experiments. The specific configurations of the realworld tasks are outlined in the following descriptions. 

**_Interactive Bar Service_ .** In this scenario, the humanoid robot engages in verbal dialogue with a human and provides assistance based on vocal instructions. These tasks 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

10 


Fig. 5. **Experimental validation within the interactive bar service scenario.** Evaluation of the RGMP-S framework regarding the delivery of beverages and tissues. The training phase involves 40 expert trajectories per object category. Quantitative results demonstrate that RGMP-S attains superior success rates and robustness relative to the Diffusion Policy (DP) baseline. See § 4.2 for details. 

include the delivery of beverages or tissues (as shown in Fig. 5). During evaluation, the skill selection accuracy _Accs_ is recorded as 0 if the robot selects an inappropriate skill. Typical failures primarily involve unstable side grasps on deformed objects and collisions with peripheral obstacles during cluttered manipulation. Conversely, successful skill identification is denoted as _Accs_ = 1. Furthermore, the execution success rate _Acct_ is recorded as 1 only upon the successful grasping of the target object. For each behavioral primitive, the model is trained using 40 expert trajectories and subsequently validated across 20 randomly positioned objects, yielding the mean success rate as the final accuracy. 

**_Zero-shot Grasping_ .** To assess the generalization capability of the RGMP-S framework within previously unseen environments (as shown in Fig. 6), we evaluate the performance of the action generation ability. The training phase utilizes a constrained dataset comprising 40 expert trajectories solely for grasping a Fanta can. During the inference stage, the zero-shot transfer capability is validated through grasping trials performed at randomized positions on novel objects with distinct geometries including a Coke can, a spray bottle, and a human hand. In addition to testing unseen categories, we examine spatial generalization by deploying the originally seen Fanta can in various randomized positions across the workspace. Each evaluation trial is quantified via a binary success metric, where a stable retrieval of the target is recorded as 1 and a failure as 0. For each object category, we conduct 100 independent trials at randomized locations to determine the final success rate. 

**_Towel Folding_** . The towel folding task involves the manipulation of deformable objects through a sequence of maneuvers intended to achieve a predefined configuration. This environment involves high degrees of freedom and stochastic physical properties including randomized initial poses and various fabric textures. Success is defined as aligning the fabric edges within a specified spatial tolerance ( _±_ 2 cm) and maintaining a stable folded geometry. The training corpus for this task comprises 100 expert trajectories that encompass diverse towel dimensions and colors. For evaluation, we employ a validation scheme involving randomized placements and novel towel instances to assess the generalization performance of the proposed framework. 

**_Pouring Water_** . The primary objective of this task is the coordination of a source container to facilitate the successful transfer of liquid into a target receptacle. The environment involves complex fluid dynamics and stochastic physical properties including randomized initial positions and various container geometries. Success is defined as the spillfree transfer of water into the target receptacle. The training corpus for this task comprises 100 expert trajectories that encompass different initial fill levels and container types. For evaluation, we employ a validation scheme involving novel receptacles and randomized spatial configurations to assess the robust generalization capability. 

**_Bin Picking_** . Within the bin picking scenario, the robot is tasked with retrieving objects from a storage bin and relocating them to a designated target zone under cluttered conditions. The environment involves complex occlusions 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

11 


Fig. 6. **Generalized manipulation capabilities of the RGMP-S.** We evaluate the RGMP-S regarding its ability to grasp various novel objects at randomized positions. The training phase relies on a dataset containing only 40 expert demonstrations focused on grasping a Fanta can. Experimental results indicate that RGMP-S achieves proficient success rates when grasping the Fanta can across diverse spatial configurations. Furthermore, the system demonstrates substantial zero-shot transfer to previously unencountered entities such as a Coke can, a spray bottle, and a human hand. This outcome highlights the inherent versatility and adaptability of the architecture across diverse manipulation scenarios. See § 4.2. 

and stochastic physical arrangements including randomized orientations and various object geometries within a confined space. Success is defined as the accurate retrieval of the target object and its stable placement within the goal area without unintended collisions. The training corpus for this task comprises 100 expert trajectories per object category to capture diverse grasping configurations. For evaluation, we employ a validation scheme involving novel object instances and randomized clutter patterns to assess the generalization robustness of the proposed framework (as shown in Fig. 7). **Simulation Benchmark Specifications.** To evaluate the proposed framework, we select five representative tasks from the publicly available and standardized ManiSkill2 simulation benchmark (as shown in Fig. 8). These tasks demand high-precision interaction and robust spatial reasoning. The detailed specifications for each task are described as follows. 

**_OpenCabinetDrawer / CabinetDoor_** : These articulated object manipulation tasks require a single-arm mobile manipulator to actuate target components on a cabinet. These environments involve stochastic physical properties, including randomized friction and damping parameters for the joints. Success is defined as opening the target component to at least 90% of the maximum range and maintaining a static state. The training corpus for these tasks comprises 300 expert trajectories per target, spanning 25 and 42 unique cabinets for drawers and doors, respectively. For evaluation, 

we employ a validation scheme involving ten unseen cabinets to assess the generalization capability of the model. 

**_PushChair_** & **_MoveBucket_** : These tasks evaluate the capacity for precise bimanual coordination. In _PushChair_ , a dual-arm robot must translate a swivel chair to a target location without causing the object to tip over. Success requires the chair to remain static within 15 cm of the destination. The _MoveBucket_ task involves a complex manipulation sequence where the robot must lift a bucket containing a ball onto a raised platform without losing the internal object. Both tasks leverage a dataset of 300 trajectories per object, featuring 26 chairs and 29 buckets for training. 

**_PlugCharger_** : This insertion task necessitates highprecision control of the end-effector. The manipulator must insert a charger into a wall receptacle. This task provides 1,000 successful trajectories for training. The validation scheme consists of two stages of 100 episodes, each featuring randomized initial joint configurations of the robot and varied initial poses of the charger relative to the wall. **Counterparts.** We compare the proposed RGMP-S framework against several representative baselines to evaluate performance across diverse manipulation tasks. 

- **ResNet** [CVPR’16] [58]: Robust visual feature extraction via deep residual learning for manipulation tasks. 

- **Transformer** [NeurIPS’17] [59]: Global dependency modeling in trajectory sequences through self-attention. 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

12 


Fig. 8. **Performance within the ManiSkill2 benchmark.** Quantitative evaluations on 5 representative manipulation tasks to compare the proposed framework with state-of-the-art baselines. Refer to § 4.2. 

Fig. 9. **Quantitative analysis of long-horizon tasks.** The proposed framework is compared against state of the art methods for towel folding, water pouring, and bin picking. See § 4.2 for details. 

- **Diffusion Policy** [RSS’23] [19]: Robotic action distribution representation via an iterative denoising process. 

of object orientations, which effectively mitigates unstable side grasps on deformed objects. 

- **ManiSkill2 1st** [RSS’23] [60]: A finetuning mechanism that achieved 1st place in the ManiSkill2 challenge. 

**Generalized Performance Analysis** . We conduct extensive comparative experiments in Table 3 with representative state-of-the-art models on the zero-shot grasping scenario, and our RGMP-S achieves consistently superior performance. As depicted in the comparison, standard data-driven methods such as Octo and OpenVLA struggle to effectively generalize to novel categories like spray bottles and human hands due to the lack of explicit geometric reasoning. RGMP-S consistently outperforms all other counterparts on different targets. Specifically, RGMP-S outperforms the best baseline Dex-VLA by 12% in terms of average success rate. Notably, in the challenging human hand handover task, our method attains a success rate of 0.93 compared to 0.84 for the second-best method, demonstrating the remarkably robust zero-shot transfer capability of the framework even when trained on a highly constrained dataset. Moreover, regarding computational efficiency, RGMP-S achieves a high inference frequency of 75.2 Hz, significantly surpassing the computationally intensive models (e.g., 3.6 Hz for OpenVLA and 1.01 Hz for Diffusion Policy), thereby ensuring the low latency required for real-time robot control. 

- **Octo** [RSS’24] [12]: An open-source generalist policy trained on massive datasets for robotic control. 

- **OpenVLA** [CoRL’24] [61]: Integration of VLMs with action tokens for open-world manipulation. 

- **RDT-1B** [arXiv’24] [62]: Performance scaling in multiple robotic tasks via a diffusion transformer architecture. 

- **Dex-VLA** [CoRL’25] [63]: Alignment of vision and language representations for dexterous manipulation. 

### **4.2 Performance Comparison with SOTA Methods** 

Comprehensive evaluations are conducted against state of the art baselines across ten manipulation tasks, encompassing five physical scenarios and five simulation benchmarks. **Human-robot Interaction Analysis** . Table 2 details the quantitative outcomes of the interactive bar service task. The tabulated data reveals that the absence of geometric guidance compromises the skill selection accuracy _Accs_ of the standard Qwen-vl baseline, particularly when paired with the ResNet50 backbone. This limitation highlights the necessity of geometric inductive biases for precise decisionmaking. In contrast, the integration of our LGSS framework consistently outperforms the Qwen-vl counterpart across all diverse backbones. For example, within the Diffusion Policy configuration, LGSS outperforms the baseline by 15% on the squashed Coke task, which is calculated through the enhancement of overall accuracy from 0.40 to 0.55. This improvement primarily stems from the accurate identification 

**Long-horizon Manipulation Analysis** . We summarize the comparative results of long-horizon manipulation tasks in Figure 9. The figure clearly depicts that under complex physical constraints, standard vision-language models like Octo and OpenVLA present significantly suboptimal performance in these three tasks. This demonstrates the difficulty of handling complex stochastic physical properties without explicit geometric guidance. Our RGMP-S framework 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

13 

TABLE 2 

**Ablation study regarding the LGSS framework and Qwen-vl.** Experimental validations are conducted within environments featuring Fanta cans, Sprite cans, tissue paper, squashed Coke cans, and human hands with randomized object configurations for each trial. The training phase for each skill category involves 40 expert trajectories, while quantitative results are derived from 20 randomized validation trials. Comparative experiments are performed against representative baselines, including ResNet [58], Transformer [59], ManiSkill2-1st [60], and Diffusion Policy [19]. The superior performance within each category is emphasized in **bold** and the second-best result is denoted with an underline. See § 4.3. 

|Methods||Fanta<br>|||Sprite<br>|||Tissue<br>||Squ<br>|ashed C<br>|oke<br>|Hu<br>|man Ha<br>|nd<br>|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||_Accs_|_Acct_|_Acc ↑_|_Accs_|_Acct_|_Acc ↑_|_Accs_|_Acct_|_Acc ↑_|_Accs_|_Acct_|_Acc ↑_|_Accs_|_Acct_|_Acc ↑_|
|with_ResNet50_||||||||||||||||
|Qwen-vl [57]|0.65|0.54|0.35|0.60|0.42|0.25|0.65|0.46|0.30|0.65|0.46|0.30|0.70|0.57|0.40|
|Our LGSS|0.85|0.53|0.45|0.75|0.46|0.35|0.85|0.47|0.40|0.85|0.47|0.40|0.85|0.56|0.48|
|with_Transform_|_er_|||||||||||||||
|Qwen-vl [57]|0.60|0.58|0.35|0.65|0.54|0.30|0.70|0.50|0.35|0.60|0.58|0.35|0.65|0.62|0.40|
|Our LGSS|0.80|0.56|0.45|0.75|0.53|0.40|0.85|0.53|0.45|0.85|0.53|0.45|0.85|0.64|0.54|
|with_ManiSkill2_|_-1st_|||||||||||||||
|Qwen-vl [57]|0.70|0.57|0.40|0.65|0.69|0.45|0.65|0.53|0.34|0.65|0.54|0.35|0.65|0.62|0.40|
|Our LGSS|0.85|0.53|0.45|0.80|0.68|0.54|0.85|0.53|0.45|0.80|0.56|0.45|0.85|0.70|0.60|
|with_Diffusion_|_Policy_|||||||||||||||
|Qwen-vl [57]|0.65|0.76|0.49|0.65|0.75|0.50|0.65|0.68|0.44|0.65|0.62|0.40|0.70|0.71|0.50|
|Our LGSS|**0.85**|**0.76**|**0.65**|**0.80**|**0.77**|**0.62**|**0.85**|**0.69**|**0.59**|**0.85**|**0.65**|**0.55**|**0.90**|**0.83**|**0.74**|


TABLE 3 

TABLE 5 

**Generalized performance and efficiency comparison.** Models are trained on 40 Fanta can trajectories. Evaluation across Fanta, Coke, spray, and hand targets demonstrates the robust zero-shot capability and real-time inference speed ( _f_ ) of RGMP-S. See details in § 4.2. 

**Component contribution analysis.** Quantitative evaluations across grasping generalization tasks validate the efficacy of RoPE, Spatial Mixing Block (SMB), Channel Mixing Block (CMB), and Guided Self-attention Module (GSM). Please see details in § 4.3. 

|Methods|Fanta_↑_|Coke _↑_|Spray _↑_|Hand _↑_|Avg _↑_|_f_(Hz) _↑_|
|---|---|---|---|---|---|---|
|ManiSkill2-1st [60]|0.70|0.60|0.63|0.62|0.64|15.2|
|Octo [12]|0.65|0.55|0.58|0.62|0.60|13.4|
|OpenVLA [61]|0.68|0.58|0.61|0.60|0.62|3.6|
|RDT-1b [62]|0.70|0.61|0.60|0.62|0.64|6.7|
|DP [19]|0.75|0.65|0.68|0.72|0.70|1.01|
|Dex-VLA[63]|0.87|0.66|0.71|0.84|0.77|55.3|
|Our RGMP [1]|**0.98**|0.78|0.81|0.90|0.87|**78.6**|
|Our RGMP-S|0.96|**0.83**|**0.85**|**0.93**|**0.89**|75.2|


|RoPE|SMB|CMB|GSM|Fanta _↑_|Coke _↑_|Spray _↑_|Hand _↑_|
|---|---|---|---|---|---|---|---|
|–|✓|✓|✓|0.88|0.67|0.73|0.79|
|✓|–|✓|✓|0.85|0.76|0.76|0.84|
|✓|✓|–|✓|0.92|0.63|0.66|0.75|
|✓|✓|✓|–|0.86|0.61|0.62|0.73|
|✓|✓|✓|✓|**0.96**|**0.83**|**0.85**|**0.93**|


|Our RG|MP-S<br>|0.96<br>|**0.83**<br>TABLE 4|**0.85**<br>|**0.93**|**0.89**|75.2|0.86<br>Our RG|~~0.92~~<br> <br>MP-S|0.83<br>W/o SDFE|0.86<br>0.8<br>1.0|5x data<br>~~efficiency~~|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Ablation stud**<br>tissue passing<br>effectivenes|**y of RA**<br>and sq<br>s of the|**SNet a**<br>uashed<br>propose|**nd GMM**<br>Coke m<br>d comp|**.**Quan<br>anipula<br>onents.|titative e<br>tion task<br>See det|valuatio<br>s valida<br>ails in §|ns on<br>te the<br>4.3.||||0.4<br>0.6||
|Methods|GMM|_Accs ↑_|Tissue<br><br>_Acct ↑_|_Acc ↑_|Squ<br>_Accs ↑_|ashed C<br>_Acct ↑_|oke<br>_Acc ↑_||||0.2|Ou~~r~~RGMP-~~S~~<br>D~~if~~fu~~s~~i~~on~~P~~ol~~ic~~y~~|
|DP [19]|–<br>✓|0.85<br>0.80|0.58<br>0.68|0.50<br>0.56|0.80<br>0.85|0.61<br>0.65|0.49<br>0.55|**Fold**<br>Fi10|**Pour**<br>**blti**|**Bin-pick**<br>**td**|**Avg**<br>**0**<br>0.0<br>**ddtfi**|**40**<br>**200**<br>**160**<br>**120**<br>**80**<br>**iili**Thlftl|
|Our RASNet|–<br>✓|0.80<br>**0.85**|0.69<br>**0.71**|0.55<br>**0.60**|0.85<br>**0.90**|0.71<br>**0.77**|0.60<br>**0.69**|g. . <br>validates <br>|**ao**<br> the Spi<br>|**suy a**<br>king Dens<br>|**n aa ei**<br>e Feature <br>|**icency anayss.** e e pane<br>Extraction (SDFE) module across<br>|


**Ablation study of RASNet and GMM.** Quantitative evaluations on tissue passing and squashed Coke manipulation tasks validate the effectiveness of the proposed components. See details in § 4.3. 

Fig. 10. **Ablation study and data efficiency analysis.** The left panel validates the Spiking Dense Feature Extraction (SDFE) module across long-horizon tasks. The right panel illustrates that RGMP-S achieves comparable performance to the Diffusion Policy baseline with 5 _×_ fewer training trajectories on grasping Fanta task. See details in § 4.3. 

consistently outperforms all other counterparts on different scenarios. For example, in the Pouring Water scenario, RGMP-S outperforms the best baseline Diffusion Policy by approximately 16%. This metric is calculated through the successful transfer of liquid into target receptacles with randomized spatial configurations and various container geometries. We further conduct experiments within the towel folding scenario involving highly deformable objects, and our method achieves a superior success rate of 0.86 compared to 0.68 for Dex-VLA. This validates the robust generalization capability of the proposed framework in aligning fabric edges and maintaining stable folded geometry within high-degree-of-freedom environments. Similarly, in the Bin Picking task characterized by complex occlusions, RGMPS attains the highest success rate of 0.83 and effectively avoids unintended collisions. Relative to the preliminary RGMP conference version [1], RGMP-S incorporates dense spiking features to enrich spatiotemporal representations. This mechanism significantly enhances the robustness of action execution across the temporal dimension for longhorizon tasks and consequently yields consistently superior 

### performance over the previous version RGMP. 

**Simulation Benchmark Analysis** . We present a comprehensive evaluation on the ManiSkill2 benchmark, summarized in Tab. 6 and visualized via the radar chart in Fig. 8 and learning curves in Fig. 11. As observed, Transformer-based and Diffusion Policy methods exhibit suboptimal performance when subjected to stochastic physical constraints. This degradation highlights the inherent challenge of adapting to randomized friction parameters without explicit geometric guidance. In contrast, our RGMP-S demonstrates superior robustness, consistently outperforming state-ofthe-art baselines across all evaluated scenarios. Specifically, in the _Open Cabinet Door_ task involving articulated objects, RGMP-S achieves a success rate of 26.48%, surpassing the ManiSkill2-1st baseline (24.68%) and Diffusion Policy (15.32%). This performance advantage is attributed to our method’s ability to handle stochastic dynamics while actuating target components to at least 90% of their maximum range. Furthermore, in the bimanual _PushChair_ task, RGMP- 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

14 

TABLE 6 

**Quantitative comparison on the ManiSkill2 benchmark.** Comparison of average success rates (in %, mean _±_ standard deviation) of our RGMP-S against state-of-the-art baselines across five diverse manipulation tasks. All results are averaged over multiple random seeds. See § 4.2. 

|Methods|Push Chair_↑_|Move Bucket _↑_|PlugCharger _↑_|Cabinet Door _↑_|Cabinet Drawer _↑_|Average Score _↑_|
|---|---|---|---|---|---|---|
|RDT-1b [62]|3.97_±_1.35|1.46_±_0.34|1.75_±_1.21|13.44_±_3.86|11.62_±_3.12|6.44_±_1.98|
|Dex-VLA [63]|2.36_±_1.33|3.47_±_1.36|1.62_±_1.35|18.36_±_2.93|8.49_±_2.48|6.86_±_1.89|
|ManiSkill2-1st [60]|8.63_±_2.36|4.23_±_1.39|3.41_±_1.42|24.68_±_3.22|12.48_±_3.28|10.69_±_2.33|
|Octo [12]|5.35_±_1.24|2.46_±_1.26|3.29_±_1.48|20.37_±_3.98|10.35_±_1.48|8.36_±_1.89|
|OpenVLA [61]|6.33_±_1.48|4.49_±_1.63|4.28_±_3.21|24.29_±_4.25|15.47_±_2.33|10.97_±_2.58|
|Diffusion Policy [19]|4.39_±_1.22|6.48_±_2.39|6.44_±_2.36|15.32_±_1.48|17.38_±_2.68|10.01_±_2.03|
|Our RGMP [1]|14.32_±_2.32|8.46_±_1.43|7.44_±_1.28|26.48_±_**4.35**|20.46_±_3.45|15.43_±_2.57|
|**Our RGMP-S**|**16.47** _±_ **2.34**|**9.64** _±_ **1.46**|**8.45** _±_ **2.23**|**26.48**_±_4.26|**20.16** _±_ **4.18**|**16.24** _±_ **2.89**|
|0.15<br>0.10<br>0.0<br>0.0<br>0.0<br>0.0<br>0.05|8<br>4<br>6<br>2|0.08<br>0.06<br>0.04<br>0.02||0.25<br>0.15<br>0.05|0.20<br>0.15<br>0.10<br>0.05||
|0<br>5k<br>10k<br>15k<br>20k<br>25k<br><br>**Push Chair**|0<br>5k<br>10k<br>15<br>**Move B**|k<br>20k<br>25k<br>0<br>**ucket**<br>RDT|5k<br>10k<br>15k<br>20k<br>**Plug Charger**<br>-1b<br>Dex-VLA<br>M|25k<br>0<br>5k<br>1<br>**Op**<br>aniskill2-1st<br>Octo|0k<br>15k<br>20k<br>25k<br>0<br>**en Cabinet Door**<br>OpenVLA<br>Diffusion Po|5k<br>10k<br>15k<br>20k<br>25k<br>**Open Cabinet Drawer**<br>licy<br>Our RGMP<br>Our RGMP-S|


Fig. 11. **Learning curves on ManiSkill2 benchmark.** The X-axis represents training steps, and the Y-axis denotes the success rate. Shaded areas correspond to the standard deviation. Our RGMP-S variants achieve stable convergence and superior performance across all tasks. Refer to § 4.2. 


Fig. 12. **Failure cases.** Our method and current state-of-the-art models struggle in scenarios requiring fine-grained manipulation. Refer to § 4.3. 

S achieves a score of 16.47%, nearly doubling the performance of the strongest external baseline (ManiSkill2-1st at 8.63%). This significant margin validates the efficacy of our approach in preventing object tipping and ensuring precise static positioning within 15 cm of the target destination. 

### **4.3 Diagnostic Experiments** 

**Ablation study** . To rigorously evaluate the individual contributions of the proposed components within our RGMPS framework, we conducted a series of ablation studies across diverse manipulation tasks. First, we investigated the efficacy of the Spiking Dense Feature Extraction (SDFE) module in long-horizon tasks. As illustrated in the left panel of Fig. 10, removing the SDFE module leads to a significant performance degradation across all tested tasks (Fold, Pour, Bin-pick). For instance, in the ”Pour” task, the success rate drops from 0.92 to approximately 0.65 without SDFE. This confirms that the SDFE module is crucial for capturing temporal dependencies and fine-grained spatial features necessary for complex, multi-stage manipulation. Second, we analyzed the impact of the RASNet module and the GMM component. Table 4 presents quantitative results on tissue passing and squashed Coke manipulation tasks. The baseline Diffusion Policy achieves a combined accuracy ( _Acc_ ) of 0.50 and 0.49 on the Tissue and Squashed Coke tasks, respectively. Incorporating GMM into the baseline improves these scores to 0.56 and 0.55. However, our proposed RASNet method, even without GMM, outperforms the baseline, achieving accuracies of 0.55 and 0.60. The combination of 

RASNet and GMM yields the highest performance, reaching an accuracy of 0.60 on Tissue and 0.69 on Squashed Coke. This demonstrates that RASNet effectively enhances feature representation, and its synergy with GMM further enhances the robustness of the policy against object deformability and state uncertainty. Third, we performed a component contribution analysis to validate the efficacy of Rotary Positional Embeddings (RoPE), the Spatial Mixing Block (SMB), the Channel Mixing Block (CMB), and the Guided Selfattention Module (GSM) in grasping generalization tasks. As detailed in Table 5, the full model achieves the highest success rates across all objects (Fanta: 0.96, Coke: 0.83, Spray: 0.85, Hand: 0.93). Removing any single component results in a noticeable performance drop. For example, omitting the GSM reduces the success rate on the ”Hand” object from 0.93 to 0.73, highlighting its importance in guiding attention to relevant geometric features. Similarly, the absence of SMB leads to a significant decrease in performance on the ”Fanta” object (0.96 to 0.85), underscoring the necessity of spatial mixing for robust grasping. 

**Data Efficiency Analysis.** We further evaluated the data efficiency of RGMP-S compared to the Diffusion Policy on the Fanta grasping task. The right panel of Fig. 10 illustrates the dependency of the success rate on the quantity of training trajectories. Our method demonstrates superior data efficiency, achieving a high success rate with significantly fewer demonstrations. Specifically, RGMP-S reaches a performance level comparable to the converged Diffusion Policy (trained on _∼_ 200 trajectories) using only _∼_ 40 trajectories. This 5 _×_ improvement in data efficiency is attributed to the inductive biases introduced by our RASNet, which allow for effective learning from sparse data. 

**Failure Case Analysis and Limitations.** To ensure a comprehensive and rigorous evaluation, we investigate the boundary conditions where the proposed RGMP-S and other stateof-the-art baselines encounter difficulties. As visualized in Fig. 12, performance degradation is observed across all evaluated methods in scenarios demanding extreme perceptual precision. Specifically, in the _Fold Towel_ task, when the deformable fabric lies completely flush against the table surface, the available vertical clearance for gripper inser- 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

15 

tion diminishes to the millimeter level. This insufficient manipulation margin allows for negligible error tolerance, frequently causing unintended collisions with the tabletop or failed grasping attempts due to precise z-axis control limits. Similarly, in the _Plug Charger_ task, the success rate drops significantly when the insertion alignment tolerance is stricter than 5 mm. Under such high-precision constraints, self-occlusion of the robotic gripper hinders the fine-grained visual feedback required for exact mating. It is worth noting that these failure modes reflect the intrinsic complexity of the physical interaction rather than specific algorithmic flaws. Empirical observations indicate that these scenarios are non-trivial even for human operators, where the oneshot success rate via teleoperation is also limited. These findings highlight the open challenges in handling highfidelity contact dynamics and suggest future directions for integrating tactile feedback or active vision. 

## **5 CONCLUSION** 

In this paper, we present RGMP-S, a novel and robust framework for generalizable robotic manipulation. RGMPS exploits both geometric-prior knowledge and spatiotemporal feature learning by constructing the Long-horizon Geometric-prior Skill Selector (LGSS) and the Recursive Adaptive Spiking Network (RASNet), effectively overcoming the semantic-geometric gap and acquiring generalizable dexterity in dynamic environments. Furthermore, for alleviating the data scarcity problem, we formulate an Adaptive Spike Neuron to modulate feature retention and integrate a Gaussian Mixture Model to refine action generation, enabling the policy to learn from limited demonstrations while preserving precision. Moreover, we maintain the supervision of geometric consistency to provide strong spatial constraints, boosting both long-horizon planning and fine-grained interaction performance. We experimentally demonstrate that RGMP-S performs favorably against many existing state-of-the-art methods across ten diverse manipulation tasks, including physical interactive scenarios and standard simulation benchmarks. We hope this work paves for future research on efficient and generalizable robotic learning as it is fully reproducible and includes: 

- RGMP-S, a strong baseline that outperforms existing approaches while maintaining **high data efficiency** and **robust generalization** across unseen scenarios. 

- A comprehensive benchmark comparison of the stateof-the-art on **multiple real-world** and simulation tasks. 

## **REFERENCES** 

- [1] L. Xuetao, H. Wenke, P. Nengyuan, Z. Kaiyan, Y. Songhua, W. Yiming, L. Mengde, Y. Mang, X. Jifeng, and M. Li, “Rgmp: Recurrent geometric-prior multimodal policy for generalizable humanoid robot manipulation,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2026. 1, 2, 3, 13, 14 

- [2] Y. Tong, H. Liu, and Z. Zhang, “Advancements in humanoid robots: A comprehensive review and future prospects,” _IEEE/CAA Journal of Automatica Sinica_ , vol. 11, no. 2, pp. 301–328, 2024. 1 

- [3] J. Li, Y. Zhu, Y. Xie, Z. Jiang, M. Seo, G. Pavlakos, and Y. Zhu, “Okami: Teaching humanoid robots manipulation skills through single video imitation,” _arXiv preprint arXiv:2410.11792_ , 2024. 1 

- [4] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 1, 2, 4 

- [5] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai _et al._ , “ _π_ 0 _._ 5: a vision-language-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 1 

- [6] W. Huang, J. Liang, Z. Shi, D. Zhu, G. Wan, H. Li, B. Du, D. Tao, and M. Ye, “Learn from downstream and be yourself in multimodal large language model fine-tuning,” in _International Conference on Machine Learning_ , 2025. 1 

- [7] A. T. Abu-Jassar, H. Attar, A. Amer, V. Lyashenko, V. Yevsieiev, and A. Solyman, “Development and investigation of vision system for a small-sized mobile humanoid robot in a smart environment,” _International Journal of Crowd Science_ , vol. 9, no. 1, pp. 29–43, 2025. 1 

- [8] I. Skubis and K. Wodarski, “Humanoid robots in managerial positions-decision-making process and human oversight.” _Scientific Papers of Silesian University of Technology. Organization & Management/Zeszyty Naukowe Politechniki Slaskiej. Seria Organizacji i Zarzadzanie_ , no. 189, 2023. 1 

- [9] D. Driess, F. Xia, M. S. M. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. H. Vuong, T. Yu, W. Huang, Y. Chebotar, P. Sermanet, D. Duckworth, S. Levine, V. Vanhoucke, K. Hausman, M. Toussaint, K. Greff, A. Zeng, I. Mordatch, and P. R. Florence, “Palm-e: An embodied multimodal language model,” in _International Conference on Machine Learning_ , 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID: 257364842 1, 4 

- [10] W. Dai, J. Li, D. Li, A. Tiong, J. Zhao, W. Wang, B. Li, P. N. Fung, and S. Hoi, “Instructblip: Towards general-purpose visionlanguage models with instruction tuning,” _Advances in neural information processing systems_ , vol. 36, pp. 49 250–49 267, 2023. 1, 4 

- [11] J. Liang, W. Huang, G. Wan, Q. Yang, and M. Ye, “Lorasculpt: Sculpting lora for harmonizing general and specialized knowledge in multimodal large language models,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2025. 1 

- [12] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu _et al._ , “Octo: An opensource generalist robot policy,” in _Proceedings of Robotics: Science and Systems_ , 2024. 1, 2, 12, 13, 14 

- [13] M. Ahn, A. Brohan, N. Brown, Y. Chebotar, O. Cortes, B. David, C. Finn, C. Fu, K. Gopalakrishnan, K. Hausman _et al._ , “Do as i can, not as i say: Grounding language in robotic affordances,” _arXiv preprint arXiv:2204.01691_ , 2022. 2, 4 

- [14] H. Shi, H. Xu, S. Clarke, Y. Li, and J. Wu, “Robocook: Longhorizon elasto-plastic object manipulation with diverse tools,” _arXiv preprint arXiv:2306.14447_ , 2023. 2, 4 

- [15] C. Tang, D. Huang, W. Ge, W. Liu, and H. Zhang, “Graspgpt: Leveraging semantic knowledge from a large language model for task-oriented grasping,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 11, pp. 7551–7558, 2023. 2, 4 

- [16] A. Mousavian, C. Eppner, and D. Fox, “6-dof graspnet: Variational grasp generation for object manipulation,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 2901–2910. 2, 4 

- [17] X. Chu, J. Deng, G. You, W. Liu, X. Li, J. Ji, and Y. Zhang, “Graspcot: Integrating physical property reasoning for 6-dof grasping under flexible language instructions,” _arXiv preprint arXiv:2503.16013_ , 2025. 2 

- [18] J. J. Rothert, S. Lang, M. Seidel, and M. Hanses, “Sim-to-real transfer for a robotics task: Challenges and lessons learned,” in _2024 IEEE 29th International Conference on Emerging Technologies and Factory Automation_ . IEEE, 2024, pp. 1–8. 2 

- [19] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Proceedings of Robotics: Science and Systems_ , 2023. 2, 4, 8, 12, 13, 14 

- [20] T. Pearce, T. Rashid, A. Kanervisto, D. Bignell, M. Sun, R. Georgescu, S. V. Macua, S. Z. Tan, I. Momennejad, K. Hofmann _et al._ , “Imitating human behaviour with diffusion models,” _arXiv preprint arXiv:2301.10677_ , 2023. 2 

- [21] Y. Song, P. Dhariwal, M. Chen, and I. Sutskever, “Consistency models,” in _International Conference on Machine Learning_ , no. 202. PMLR, 2023. 2 

- [22] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 2, 4 

GENERALIZABLE GEOMETRIC PRIOR AND RECURRENT SPIKING FEATURE LEARNING FOR HUMANOID ROBOT MANIPULATION 

16 

- [23] M. Shridhar, L. Manuelli, and D. Fox, “Cliport: What and where pathways for robotic manipulation,” in _Conference on robot learning_ . PMLR, 2022, pp. 894–906. 2 

- [24] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence, and A. Zeng, “Code as policies: Language model programs for embodied control,” in _2023 IEEE International Conference on Robotics and Automation_ . IEEE, 2023, pp. 9493–9500. 2 

- [25] W. Huang, J. Liang, G. Wan, D. Zhu, H. Li, J. Shao, M. Ye, B. Du, and D. Tao, “Be confident: Uncovering overfitting in mllm multitask tuning,” in _International Conference on Machine Learning_ , 2025. 2 

- [26] V. Sitzmann, J. Martel, A. Bergman, D. Lindell, and G. Wetzstein, “Implicit neural representations with periodic activation functions,” _Advances in neural information processing systems_ , vol. 33, pp. 7462–7473, 2020. 2, 4 

- [27] P. W. Battaglia, J. B. Hamrick, V. Bapst, A. Sanchez-Gonzalez, V. Zambaldi, M. Malinowski, A. Tacchetti, D. Raposo, A. Santoro, R. Faulkner _et al._ , “Relational inductive biases, deep learning, and graph networks,” _arXiv preprint arXiv:1806.01261_ , 2018. 2 

- [28] M. Yaseen, “What is yolov9: An in-depth exploration of the internal features of the next-generation object detector,” _arXiv preprint arXiv:2409.07813_ , 2024. 3 

- [29] R. Pascanu, T. Mikolov, and Y. Bengio, “On the difficulty of training recurrent neural networks,” in _International conference on machine learning_ . Pmlr, 2013, pp. 1310–1318. 2 

- [30] Y. Bengio, P. Simard, and P. Frasconi, “Learning long-term dependencies with gradient descent is difficult,” _IEEE transactions on neural networks_ , vol. 5, no. 2, pp. 157–166, 1994. 2 

- [31] K. Roy, A. Jaiswal, and P. Panda, “Towards spike-based machine intelligence with neuromorphic computing,” _Nature_ , vol. 575, no. 7784, pp. 607–617, 2019. 2 

- [32] Z. Fu, T. Z. Zhao, and C. Finn, “Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation,” _arXiv preprint arXiv:2401.02117_ , 2024. 4 

- [33] J. Zhang, J. Huang, S. Jin, and S. Lu, “Vision-language models for vision tasks: A survey,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 46, no. 8, pp. 5625–5644, 2024. 4 

- [34] J. Sun, Y. Wang, and D. Wang, “Towards real-world aerial vision guidance with categorical 6d pose tracker,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 47, no. 7, pp. 6055– 6072, 2025. 4 

- [35] J. Liu, W. Sun, H. Yang, P. Deng, C. Liu, N. Sebe, H. Rahmani, and A. Mian, “Diff9d: Diffusion-based domain-generalized categorylevel 9-dof object pose estimation,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 47, no. 7, pp. 5520–5537, 2025. 4 

- [36] K. Liu, Y.-J. Liu, and B. Chen, “General 3d vision-language model with fast rendering and pre-training vision-language alignment,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 47, no. 9, pp. 7352–7368, 2025. 4 

- [37] S. Qiu, S. Anwar, and N. Barnes, “Dense-resolution network for point cloud classification and segmentation,” in _Proceedings of the IEEE/CVF winter conference on applications of computer vision_ , 2021, pp. 3813–3822. 4 

- [38] A. Zeng, P. Florence, J. Tompson, S. Welker, J. Chien, M. Attarian, T. Armstrong, I. Krasin, D. Duong, V. Sindhwani _et al._ , “Transporter networks: Rearranging the visual world for robotic manipulation,” in _Conference on Robot Learning_ . PMLR, 2021, pp. 726–747. 4 

- [39] L. Manuelli, W. Gao, P. Florence, and R. Tedrake, “kpam: Keypoint affordances for category-level robotic manipulation,” in _The International Symposium of Robotics Research_ . Springer, 2019, pp. 132–157. 4 

- [40] H.-S. Fang, C. Wang, M. Gou, and C. Lu, “Graspnet-1billion: A large-scale benchmark for general object grasping,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 45, no. 9, pp. 11 427–11 443, 2023. 4 

- [41] S. Jin, J. Xu, Y. Lei, and L. Zhang, “Reasoning grasping via multimodal large language model,” _arXiv preprint arXiv:2402.06798_ , 2024. 4 

- [42] T. Zhao, P. Liu, and K. Lee, “Omdet: Large-scale vision-language multi-dataset pre-training with multimodal detection network,” _IET Computer Vision_ , vol. 18, no. 5, pp. 626–639, 2024. 4 

   - [44] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics_ , 2011, pp. 627–635. 4 

   - [45] H. Razali and Y. Demiris, “Keystate-driven long-term generation of bimanual object manipulation sequences,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 47, no. 9, pp. 7784– 7795, 2025. 4 

   - [46] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning finegrained bimanual manipulation with low-cost arms,” in _Proceedings of Robotics: Science and Systems_ , 2023. 4 

   - [47] L. Chen, K. Lu, A. Rajeswaran, K. Lee, A. Grover, M. Laskin, P. Abbeel, A. Srinivas, and I. Mordatch, “Decision transformer: Reinforcement learning via sequence modeling,” _Advances in neural information processing systems_ , vol. 34, pp. 15 084–15 097, 2021. 4 

   - [48] S. Hu, L. Shen, Y. Zhang, Y. Chen, and D. Tao, “On transforming reinforcement learning with transformers: The development trajectory,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 46, no. 12, pp. 8580–8599, 2024. 4 

   - [49] F. Keller, N. M. Shafiullah _et al._ , “Consistency policy: Accelerated visuomotor policies via consistency distillation,” _arXiv preprint arXiv:2405.07503_ , 2024. 4 

   - [50] L. Chen, K. Lu, A. Rajeswaran, K. Lee, A. Grover, M. Laskin, P. Abbeel, A. Srinivas, and I. Mordatch, “Decision transformer: Reinforcement learning via sequence modeling,” _Advances in neural information processing systems_ , vol. 34, pp. 15 084–15 097, 2021. 4 

   - [51] K. Han, Y. Wang, H. Chen, X. Chen, J. Guo _et al._ , “A survey on vision transformer,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 45, no. 1, pp. 87–110, 2023. 4 

   - [52] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” _Neural Computation_ , vol. 9, no. 8, pp. 1735–1780, 1997. 4 

   - [53] S. Ghosh and G. Gallego, “Event-based stereo depth estimation: A survey,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 47, no. 10, pp. 9130–9149, 2025. 4 

   - [54] Y. Wu, R. Zhao, J. Zhu, F. Chen, M. Xu, G. Li, S. Song, L. Deng, G. Wang, H. Zheng _et al._ , “Brain-inspired global-local learning incorporated with neuromorphic computing,” _Nature Communications_ , vol. 13, no. 1, p. 65, 2022. 4 

   - [55] M. Yao, X. Qiu, T. Hu, J. Hu, Y. Chou, K. Tian, J. Liao, L. Leng, B. Xu, and G. Li, “Scaling spike-driven transformer with efficient spike firing approximation training,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 4 

   - [56] G. Gallego, T. Delbruck, G. Orchard, C. Bartolozzi, B. Taba, A. Censi, S. Leutenegger, A. J. Davison, J. Conradt, K. Daniilidis, and D. Scaramuzza, “Event-based vision: A survey,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 44, no. 1, pp. 154–180, 2022. 4 

   - [57] J. Bai, S. Bai, S. Yang, S. Wang, S. Tan, P. Wang, J. Lin, C. Zhou, and J. Zhou, “Qwen-vl: A frontier large vision-language model with versatile abilities,” _arXiv preprint arXiv:2308.12966_ , 2023. 5, 13 

   - [58] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2016, pp. 770–778. 11, 13 

   - [59] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” _Advances in neural information processing systems_ , vol. 30, 2017. 11, 13 

   - [60] F. Gao, X. Li, J. Yu, and F. Shaung, “A two-stage fine-tuning strategy for generalizable manipulation skill of embodied ai,” in _Proceedings of Robotics: Science and Systems_ , 2023. 12, 13, 14 

   - [61] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An open-source vision-language-action model,” in _Conference on Robot Learning_ . PMLR, 2024, pp. 2679–2713. 12, 13, 14 

   - [62] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” _arXiv preprint arXiv:2410.07864_ , 2024. 12, 13, 14 

   - [63] J. Wen, Y. Zhu, J. Li, Z. Tang, C. Shen, and F. Feng, “Dexvla: Visionlanguage model with plug-in diffusion expert for general robot control,” in _Conference on Robot Learning_ , 2025. 12, 13, 14 

- [43] D. A. Pomerleau, “Alvinn: An autonomous land vehicle in a neural network,” _Advances in neural information processing systems_ , vol. 1, 1988. 4 

