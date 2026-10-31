---
title: "From Manuals to Actions: A Unified VLA Model for Chain-of-Thought Manual Generation and Robotic Manipulation"
date: "2026"
venue: "CVPR 2026"
url: https://openaccess.thecvf.com/content/CVPR2026/html/Gu_From_Manuals_to_Actions_A_Unified_VLA_Model_for_Chain-of-Thought_CVPR_2026_paper.html
pdf: https://openaccess.thecvf.com/content/CVPR2026/papers/Gu_From_Manuals_to_Actions_A_Unified_VLA_Model_for_Chain-of-Thought_CVPR_2026_paper.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://openaccess.thecvf.com/content/CVPR2026/papers/Gu_From_Manuals_to_Actions_A_Unified_VLA_Model_for_Chain-of-Thought_CVPR_2026_paper.pdf)** / [論文ページ](https://openaccess.thecvf.com/content/CVPR2026/html/Gu_From_Manuals_to_Actions_A_Unified_VLA_Model_for_Chain-of-Thought_CVPR_2026_paper.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **From Manuals to Actions: A Unified VLA Model for Chain-of-Thought Manual Generation and Robotic Manipulation** 

**Chenyang Gu**<sup>* 1</sup> , **Jiaming Liu**<sup>_∗†_1</sup> , **Hao Chen**<sup>_∗†_2</sup> , **Runzhong Huang**<sup>_∗_1</sup> , **Qingpo Wuwu**<sup>1</sup> , **Xiaoqi Li**<sup>1</sup> , **Zhuoyang Liu**<sup>1</sup> , **Ying Li**<sup>1</sup> , **Renrui Zhang**<sup>2</sup> , **Peng Jia**<sup>3</sup> , **Pheng-Ann Heng**<sup>2</sup> , **Shanghang Zhang**<sup>�1</sup> 1State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University<sup>2</sup> The Chinese University of Hong Kong<sup>3</sup> Simplexity Robotics 

## **Abstract** 

_Vision–Language–Action (VLA) models have recently emerged, demonstrating strong generalization in robotic scene understanding and manipulation. However, when confronted with long-horizon tasks that require defined goal states, such as LEGO assembly or object rearrangement, existing VLA models still face challenges in coordinating high-level planning with precise manipulation. Therefore, we aim to endow a VLA model with the capability to infer the “how” process from the “what” outcomes, transforming goal states into executable procedures. In this paper, we introduce ManualVLA, a unified VLA framework built upon a Mixture-of-Transformers (MoT) architecture, enabling coherent collaboration between multimodal manual generation and action execution. Unlike prior VLA models that directly map sensory inputs to actions, we first equip ManualVLA with a planning expert that generates intermediate manuals consisting of images, position prompts, and textual instructions. Building upon these multimodal manuals, we design a Manual Chain-of-Thought (ManualCoT) reasoning process that feeds them into the action expert, where each manual step provides explicit control conditions, while its latent representation offers implicit guidance for accurate manipulation. To alleviate the burden of data collection, we develop a high-fidelity digital-twin toolkit based on 3D Gaussian Splatting, which automatically generates manual data for planning expert training. ManualVLA demonstrates strong real-world performance, achieving an average success rate 32% higher than the previous hierarchical SOTA baseline on LEGO assembly and object rearrangement tasks._ **_Project page:_** _https://sites.google.com/view/maunalvla._ 

## **1. Introduction** 

Recently, building on internet-scale pretrained visionlanguage models [1, 33], vision-language-action (VLA) models have emerged [9, 36] and are trained on robot 

> *Equal contribution<sup>_†_</sup> Project leader<sup>�</sup> Corresponding author. 


Figure 1. **Overview.** (a) Long-horizon tasks with predefined goal states, such as LEGO assembly or object rearrangement, pose a significant challenge for intelligent robots, as they require not only imagining procedural manuals but also executing precise manipulations based on them. (b) We address such tasks by introducing ManualVLA, a unified VLA model built upon a MoT architecture, which enables coherent collaboration between multimodal manual and action generation via a designed Manual Chain-of-Thought. 

demonstrations to predict control actions. These models exhibit impressive capabilities in robotic scene understanding [45, 47, 89] while demonstrating strong generalization and manipulation performance in out-of-lab scenarios [5, 27, 48]. Such advances have significantly accelerated progress toward developing generalist robotic agents. However, when confronted with long-horizon tasks that re- 

13540 

quire precisely defined goal states (Figure 1 (a)), such as LEGO assembly or object rearrangement, VLA models remain highly challenged. The difficulty arises from two aspects: (1) the VLA model must execute precise manipulation strictly aligned with the predefined final scene or object configuration, and (2) it must integrate long-horizon planning with fine-grained control, while maintaining generalization to diverse real-world environments. 

In contrast, for humans, upon accumulating sufficient manipulation experience, they can perform long-horizon, goal-specific tasks independently, without relying on further demonstrations. For example, humans can assemble LEGO structures by inferring the target configuration, or reorganize household objects according to a predefined spatial arrangement. This ability stems from humans’ intuitive inference of intermediate cues, reasoning over spatial and causal relations, and decomposition of tasks into coherent, subgoal-directed manipulation steps. Recently, some hierarchical methods have attempted to emulate this ability by relying on detailed manuals [50] or human demonstration videos [2, 28, 62, 80]. However, such approaches are often limited in generalization to unseen final goal states and increase the dependence on human involvement. This naturally leads to a question: _“Is it possible to endow a VLA model with the capability to infer the procedural “how” from the desired “what,” thereby transforming a predefined final goal into a sequence of coherent and precise execution steps?”_ 

To this end, we propose **ManualVLA** , a unified VLA model based on a Mixture-of-Transformers (MoT) [44] architecture, capable of generating multimodal manuals and actions directly from a final goal state. Since only the final state is provided and intermediate steps are unknown, previous VLA models that map sensory inputs directly to actions struggle with such long-horizon tasks. In contrast, as shown in Figure 1 (b), ManualVLA selectively activates planning and action experts within a unified framework for subgoal manual and action generation. Specifically, ManualVLA is equipped with a planning expert to generate intermediate manuals that integrate images, position prompts, and textual instructions. These manuals are then used in our proposed **Manual Chain-of-Thought (ManualCoT)** reasoning strategy, which guides the action expert by treating each subgoal step as an explicit condition for precise execution. Furthermore, a cross-task shared attention mechanism between the two experts enables long-context interactions between manual-generation features and action generation, providing implicit guidance for coherent manipulation. 

**To train ManualVLA** , we first leverage the generative capability of the VLM model (e.g., Janus-Pro [84]) and finetune it on self-collected and simulation-synthesized manual data to acquire the planning expert capability. Due to the substantial uncertainty in the final goal states, a large amount of data is required to train the model with sufficient world 

knowledge for effective task planning. To alleviate the burden of data collection, we develop a high-fidelity digital-twin toolkit based on 3D Gaussian Splatting [34], which automatically generates manual data for planning expert training. Meanwhile, we pretrain the action expert on large-scale open-source robotic datasets comprising over 400K trajectories [35, 61]. Benefiting from the rich manual conditions incorporated during action generation, ManualVLA requires only around 100 trajectories to achieve generalizable manipulation while finetuning on downstream tasks. Experimental results demonstrate that, when confronted with long-horizon and complex LEGO assembly and object rearrangement tasks, ManualVLA not only generates accurate manuals but also achieves an average manipulation success rate of 32% higher than the existing hierarchical SOTA baseline. Note that ManualVLA also achieves state-of-the-art (SOTA) performance on other general manipulation tasks. In summary, our contributions are as follows: 

- We address long-horizon tasks with precisely defined goal states by introducing ManualVLA, a unified VLA model built upon a MoT architecture that supports coherent multimodal manual generation and action execution. 

- We design a Manual Chain-of-Thought (ManualCoT) reasoning process that translates generated manuals into precise actions, where each manual step provides explicit control conditions and its latent representation offers implicit guidance for manipulation. 

- Equipped with the proposed training strategy, ManualVLA demonstrates strong real-world performance, achieving superior manipulation accuracy and generalization compared with previous SOTA baselines on downstream tasks. 

## **2. Related Work** 

**Vision-language models (VLMs)** [1, 33, 67] have achieved strong multimodal reasoning by learning from internet-scale image-text data. Building on this progress, VLA models [9, 36] have emerged as a promising approach for robot learning, enabling end-to-end mapping from multimodal observations to control signals. Subsequent works have further advanced VLA models by incorporating richer sensory understanding [39, 42, 49, 65], exploring more robust action generation [7, 27, 40, 48, 82], and developing optimized inference strategies [47, 63, 83] as well as dual-system paradigms [5, 12, 21, 93]. However, when faced with longhorizon tasks that require precise goal specifications, these models continue to struggle. To reconcile this issue, several works [26, 43, 90, 98] have incorporated visual world modeling into VLA architectures to enable reasoning about the future images. They typically decouple long-horizon progress into intermediate steps either by generating explicit pixel-level subgoals [60, 85] or by formulating compressed token representations [10, 22, 41, 95]. Nevertheless, these models struggle to capture the relationship between subgoals 

13541 

and fine-grained control. In contrast, we introduce a comprehensive Chain-of-Thought (CoT) reasoning process that combines both explicit and implicit cues to transform the generated manuals into precise actions. 

**Final goal conditioned manipulation** , where robots must reach specified target states from given initial configurations, such as LEGO assembly or object rearrangement, represents a challenge in embodied AI. A prominent research direction uses human hand videos [2, 28, 73] to present the desired intermediate procedure. Methods such as Vid2Robot [28] and DexCap [80] extract manipulation trajectories from egocentric videos, transferring human dexterity to robotic control. Meanwhile, several works [64, 81, 94] exploit operation manuals or goal-state descriptions as guidance. CheckManual [50] conditions robot policies on predefined instruction manuals, while [87, 91] utilize the final target scene configuration to inform execution goal. However, providing hand videos, human-crafted manuals, or additional reasoning models introduces extra human effort and computational cost, limiting the practicality of these approaches. In contrast, we make the first attempt to address long-horizon, goalconditioned manipulation through a unified VLA model that enables coherent collaboration between multimodal manual generation and action execution. 

## **3. ManualVLA** 

In this section, we first introduce the fundamentals of VisionLanguage-Action (VLA) models in Section 3.1. Then, Section 3.2 presents the architectural details of ManualVLA, followed by Section 3.3, which elaborates on its working principles. Sections 3.4 and 3.5 describe the training strategies of ManualVLA and the digital-twin toolkit, respectively. 

### **3.1. Preliminary** 

VLA models integrate visual, linguistic, and proprioceptive inputs to generate robot control signals, exhibiting strong generalization in diverse manipulation tasks [7, 36]. Despite their impressive abilities, existing VLA models often struggle with long-horizon tasks with defined goal states, reflecting their limited world knowledge for planning the intermediate progress required to achieve such goals. 

To address this limitation, we aim to endow the VLA model with a human-like capability to infer the procedural “how” from the desired “what”. Therefore, we propose ManualVLA _πθ_ , a unified VLA model equipped with world knowledge that first reasons about multimodal manuals describing the task procedure, and subsequently generates the corresponding actions for execution. As shown in Figure. 2, given the language instruction _l_ together with the images of the current state _It_<sup>current</sup> and the final goal state _I_<sup>goal</sup> , ManualVLA first generates a manual that consists of the textual description of the target objects<sup>ˆ</sup> _lt_ , their target 2D coordi- 

nates _pt_ , and the corresponding subgoal image _It_<sup>subgoal</sup> : 


Based on this manual, we construct a prompted image _It_<sup>prompt</sup> by overlaying the target object’s final position as a mask on the current scene image _It_<sup>current</sup> . Finally, the model takes the robot state _st_ and the prompted image _It_<sup>prompt</sup> , together with _Ft_<sup>subgoal</sup> , _Ft_<sup>_p_, and</sup><sup>_F_</sup> _t_<sup>ˆ</sup><sup>_l_(the key and value features</sup> stored during the generation of<sup>ˆ</sup> _lt_ , _pt_ , and _It_<sup>subgoal</sup> ), as conditional inputs for modeling the action chunk _at_ : _t_ + _h_ , enabling explicit subgoal-guided action generation. 


### **3.2. Model Architecture** 

ManualVLA adopts Janus-Pro [14] as its foundation model due to its strong capability in general multimodal understanding and generation. Unlike atomic or short-horizon manipulation tasks, our goal is to perform long-horizon, goal-specific tasks, where the model must not only generate detailed manuals but also predict precise actions and enable effective interaction between the two processes. To achieve this, we extend the basic VLM into a Mixture-of-Transformers (MoT) architecture, forming a unified VLA model that integrates collaborative planning and action experts. We next detail the key components of our ManualVLA. 

**Vision Tokenizer and Encoder.** As shown in Figure 2, given the distinct characteristics of discrete and continuous image-injection paradigms, as well as the differing demands of manual and action generation, ManualVLA employs two separate visual modules: a VQ-based vision tokenizer for manual generation and a continuous vision encoder for action generation. For the vision tokenizer, ManualVLA adopts an encoder-quantizer-decoder architecture following VQGAN [20]. The encoder and decoder are convolutional networks with a downsampling factor of 16, and the quantizer maintains a codebook **Z** _∈_ R<sup>16</sup><sup>_,_384</sup><sup>_×_8</sup> . For the vision encoder, ManualVLA uses SigLIP-Large [92] with an input resolution of 384 to extract high-dimensional semantic features from input images. 

**Mixture-of-Transformers LLM.** The base language model in ManualVLA is DeepSeek-LLM 1.5B [4]. To integrate the distinct capabilities of manual generation and action generation, we construct a MoT architecture atop this LLM. The proposed MoT extends the standard Transformer by introducing task-specific parameter sets for all non-embedding components, including feed-forward networks (FFN), attention projections, and layer normalizations, yielding the planning and action experts illustrated in Figure 2 (a). When faced with complex and long-horizon tasks, this design enables the VLA model to efficiently handle heterogeneous 

13542 


Figure 2. **Framework of ManualVLA.** (a) To accomplish long-horizon tasks with defined goal states, we propose ManualVLA, a unified VLA model built upon a MoT architecture. The framework consists of two experts: a planning expert responsible for generating multimodal manuals, and an action expert responsible for predicting precise actions. The planning expert processes human instructions, the current image, and the final goal image to generate intermediate manuals that combine next-step images, positions, and sub-task instructions. We introduce an explicit CoT reasoning process, where each positional indicator serves as a visual prompt embedded into the observation of the action expert. (b) Along with the cross-task shared attention mechanism and the designed attention mask, the generated manual tokens are also used as conditioning signals for action generation, enabling an implicit CoT reasoning process that effectively guides the action expert. (c) ManualVLA adopts a three-stage training strategy that aligns the planning and action experts for effective collaboration. 

tasks while preserving its ability to learn cross-task dependencies within a unified framework. 

To formally describe this mechanism, we take a single MoT layer as an example. Let _x_ = ( _x_ 1 _, . . . , xn_ ) denote the input token sequence, where each token _xi_ is assigned to exactly one task category _ti ∈T_ = _{_ manual _,_ action _}_ . For each task, we define task-dependent operator bundles Θ<sup>_t_</sup> = _{θ_ attn<sup>_t, θ_</sup> ffn<sup>_t}_and corresponding mappings Φ</sup> attn<sup>_t,_Φ</sup><sup>_t_</sup> ffn<sup>:</sup> R<sup>_d_</sup> _→_ R<sup>_d_</sup> , which are applied token-wise depending on the associated task. Then, a MoT layer acting on a mixed-task sequence can be compactly expressed as: 


where the notation _t_ ( _·_ ) indicates that each token at position _i_ uses its corresponding task parameters and _N_ attn<sup>_t_,</sup><sup>_N_</sup> ffn<sup>_t_denote</sup> task-specific layer-normalization operators. 

Finally, to define the global attention operator [18], let _X ∈_ R<sup>_n×d_</sup> denote the matrix form of the input sequence _x_ = ( _x_ 1 _, . . . , xn_ ), where each row corresponds to a token embedding. The operator is then given by 


where the projections _WQ_<sup>_t_(</sup><sup>_·_)</sup><sup>_, W_</sup> _K_<sup>_t_(</sup><sup>_·_)</sup><sup>_, W_</sup> _V_<sup>_t_(</sup><sup>_·_)</sup> _, WO_<sup>_t_(</sup><sup>_·_)</sup> are selected per token according to its task _ti_ , while the attention 

weight matrix _A_ is computed globally across all tokens. This formulation enables ManualVLA to adaptively allocate computation according to the distinct characteristics of manual and action generation, while maintaining a unified architecture for the collaborative execution of final goal conditioned manipulation tasks. 

**Action and Robot State Components.** ManualVLA employs a diffusion-based approach for action modeling, therefore, a noise encoder is introduced to inject the noised actions into the action expert, and a noise decoder predicts the noise from the latent representations. Both modules are implemented as two-layer MLPs. In addition, the robot state is incorporated into the action expert through another twolayer MLP (state encoder), enabling the model to condition action generation on the current proprioceptive state. 

### **3.3. Manual and Action Generation via CoT** 

Given the final goal state of a task, ManualVLA generates subgoal manuals at key steps. To better produce corresponding action sequences based on the current observation and the generated manuals, we introduce a Manual Chain-ofThought (ManualCoT) reasoning process, including both explicit and implicit CoT. Specifically, we introduce the details of manual generation in Section 3.3.1, followed by the method for generating executable actions through ManualCoT in Sections 3.3.2. Finally, in Sections 3.3.3, we describe how both processes are unified within a single token sequence for the end-to-end training. 

13543 

#### **3.3.1. Subgoal Manual Generation** 

To accomplish long-horizon manipulation tasks with predefined goal states, we design a multimodal manual that consists of (1) textual descriptions for subtask reasoning, (2) next-step images providing semantically rich conditioning, and (3) low-level position prompts for precise manipulation guidance. As shown in Figure 2 (a), upon receiving the language instruction along with the current and final state images, ManualVLA first generates a textual component that describes object attributes and actions. For target positions, we represent them using the pixel-level ( _U, V_ ) coordinates of each object’s centroid. Finally, subgoal image generation helps the model better model the physical world dynamics. 

We assume that accomplishing a long-horizon task does not require extremely dense temporal subgoals. Instead, providing guidance only at key frames where the task state changes is sufficient, such as when placing a pair of bricks onto the board. ManualVLA generates a new manual only after the completion of the previous subgoal, ensuring efficient planning without redundant intermediate guidance. To achieve this, we first generate the text description in the manual. If the generated description of the manipulated objects differs from the previous planning output, ManualVLA proceeds to produce an entirely new manual. For example, the text output changes from “yellow blocks” to “purple blocks”. Otherwise, it reuses the previously generated manual for 

#### subsequent action generation. 

#### **3.3.2. Manual-Conditioned Action Generation** 

Based on the generated subgoal manual, ManualVLA executes actions in a closed-loop manner, progressively generating the action sequence until the subgoal is achieved. As shown in Figure 2 (a), leveraging the effectiveness of visual prompts for manipulation, we use the predicted ( _U, V_ ) coordinates to overlay a mask on the current image, highlighting the affordance region that serves as input to the action expert. This construction of a prompt image to guide the action learning is defined as **explicit CoT reasoning** . Meanwhile, we introduce an implicit CoT reasoning process within the shared attention module. As shown in Figure 2 (b), in the latent space, the subgoal manual serves as a conditioning signal for action modeling through our constructed cross-task attention mask. This conditioning information first informs the model about “what” object to manipulate, then specifies “where” the object should be placed, and finally provides the anticipated visual outcome after the manipulation. This CoT reasoning process performed in the latent space is referred to as **implicit CoT reasoning** . By incorporating both explicit and implicit CoT reasoning processes, ManualVLA significantly improves its success rate in long-horizon tasks, as demonstrated in Section 4.3. 

#### **3.3.3. Token Sequence Design** 

After introducing the processes of manual and action generation, this section describes how ManualVLA jointly learns 

both tasks within a unified token sequence, while employing planning and action experts to specialize in different tasks. As shown in Figure 2, the language instruction, along with the current and goal scene images, is first inserted into the token sequence as the condition for subgoal manual generation. The subsequent tokens represent the generated manual, including object descriptions, target coordinates, and subgoal image, all of which are processed by the planning expert. Following this, the sequence incorporates the prompt image used in explicit CoT reasoning, as well as the robot state and noised action embeddings, which are handled by the action expert. As shown in Figure 2 (b), a cross-task shared attention mechanism is designed to allow the action expert to attend to the subgoal manual representations while masking out earlier inputs, thereby enabling effective information exchange between the two experts and fostering coherent reasoning across planning and action generation. 

### **3.4. Training Strategy** 

As shown in Figure 2 (c), we train ManualVLA in three stages. Before training, we initialize ManualVLA with the pretrained parameters of Janus-Pro [14], and duplicate its LLM to separately initialize the planning and action experts. 

**_Stage 1: Action expert pretraining._** During this pretraining stage, we curated an assembly dataset by carefully filtering large-scale cross-embodiment datasets [35, 61, 86] to update all parameters of the action expert. As detailed in Appendix A, the resulting dataset comprises over 400K trajectory samples. ManualVLA was trained on this dataset for five epochs, where the only conditioning inputs are the language instruction, a current scene image, and the robot state. Following diffusion policy [15], the training objective is the mean squared error (MSE) between the predicted noises _ϵ_ ˆ<sup>_i_</sup> at the _i_ -th denoising steps and the ground-truth noises _ϵ_ , defined as: _L_ action = E _ϵ∼N_ (0 _,_ 1) _,i_ �� _ϵ_ ˆ _i − ϵ_ ��22<sup>_._</sup> 

**_Stage 2: Manual expert pretraining._** At this stage, we train only the manual expert using data synthesized with our digital-twin toolkit, resulting in a dataset of over 10K frames for each task. Following Janus-Pro [14], the model is supervised with a cross-entropy loss _L_ manual applied to the subgoal manual, which includes the object description, target position, and subgoal image tokens. 

**_Stage 3: Joint manual-action fine-tuning._** Benefiting from the stable generation capabilities acquired during pretraining, we collect 100 demonstrations for each downstream task using 3DConnexion Spacemouse teleoperation. Objects are placed at diverse locations on the table to ensure sufficient variation. Each demonstration includes both action execution data and automatically extracted manual data. All components of ManualVLA are then jointly trained using the token sequences defined in Section 3.3.1. The final objective is defined as: _L_ final = _L_ manual + _L_ action _._ 

13544 


Figure 3. **Digital-twin example.** (a) We reconstruct 3D Gaussian Splatting representations, which are then decomposed into the LEGO board and individual bricks. (b) We iteratively place the bricks on the board or objects on the box. 

on a planar board. Given the final 2D assembled structure as the goal, the model must infer a sequence of intermediate manipulation actions and execute them through coordinated bimanual control. **(2) 3D LEGO Assembly:** The task extends the 2D LEGO Assembly task to a more challenging 3D setting, where the final configuration transitions from a planar layout to a 3D structure. This upgraded task imposes greater demands on the model’s spatial reasoning abilities. **(3) Object Rearrangement:** The task begins with several objects of diverse shapes, sizes, and semantics scattered around a box. Given a goal state in which all objects are placed at their designated positions inside the box, the model must progressively generate manipulation actions, alternating control of the left and right arms to prevent collisions. More detailed task settings can be found in Appendix A. 

#### **4.1.2. Baselines** 

### **3.5. Real-to-Render Data Generation** 

To construct downstream task data, we develop a highfidelity digital-twin toolkit based on 3D Gaussian Splatting [34] to automatically generate training data with intermediate target states. For example, in Figure 3 (a), we first reconstruct 3D assets of the LEGO board and individual bricks through multi-view capture, and then align them to a unified Cartesian coordinate system for consistent spatial referencing. Subsequently, we follow an iterative placement procedure as shown in Figure 3 (b), where given an initial state and a set of available bricks, we sequentially place each brick by randomly sampling a valid position on the board. At each intermediate state, we render the current configuration from a front-view camera perspective. This process produces photorealistic images for each assembly or rearrangement step, along with position and textual information. More details are provided in Appendix A. 

## **4. Experiments** 

We organize our experiments as follows. Section 4.1 defines the tasks and introduces the baseline methods. Section 4.2 compares ManualVLA with these baselines on manual generation and manipulation performance. In Section 4.3, we assess the effectiveness of our MoT architecture and CoT reasoning mechanism. Finally, Section 4.4 evaluates the generalization of ManualVLA to unseen object shapes, backgrounds, and lighting conditions. All experiments are performed on a dual-arm Franka robotic platform. 

### **4.1. Experimental Setup** 

#### **4.1.1. Task Definition** 

We design three long-horizon tasks with defined goal states, challenging the model’s procedural reasoning and manipulation capabilities. **(1) 2D LEGO Assembly:** The task begins with several LEGO bricks of different colors placed 

We compare ManualVLA against three categories of strong VLA baselines that represent the state of the art in robotic manipulation. **(1) First category:** _π_ 0 [7], _π_ 0 _._ 5 [27], and FAST [63], which adopt robust action-generation paradigms. We load the official pretrained weights provided by each method and strictly follow their fine-tuning protocols, except that we additionally embed the final goal image into the model as the target condition. **(2) Second category:** CoTVLA [96], which not only incorporates the final goal image as an additional condition, but also predicts key subgoal future images. For fair comparison, we align the supervision of subgoal image generation with that used in ManualVLA. **(3) Third category:** We introduce a hierarchical baseline that combines a VLM [14] with _π_ 0 _._ 5. The VLM is trained to generate visual and language prompts similar to our method, while _π_ 0 _._ 5 is trained to interpret these prompts and generate actions. This baseline can be regarded as a hierarchical variant of our manual-generation approach. 

### **4.2. Main Results** 

#### **4.2.1. Manual Generation** 

Table 1. Quantitative results of ManualVLA in generating subgoal images and ( _U, V_ ) coordinates across the three downstream tasks. 

|**Task**|**Subgoal**|**Image**|**_(U,V)_**|
|---|---|---|---|
||PSNR_↑_|FID_↓_|MAE_↓_|
|2D LEGO Assembly|29.01|36.39|3.23|
|3D LEGO Assembly|28.68|34.63|3.58|
|Object Rearrangement|28.11|24.46|6.21|


We first evaluate the capability of the planning expert in ManualVLA to generate high-fidelity manuals on 300 unseen test samples. As shown in Table 1, our model produces satisfactory intermediate images across all three tasks, achieving high PSNR scores, indicating strong structural and pixel-level consistency with the ground truth. Furthermore, 

13545 

Table 2. **Comparison of ManualVLA and baselines.** We report the manipulation success rate (S.R.) for the complete long-horizon tasks using 20 unseen test goal states, and additionally report the success rate of key intermediate steps. 

|Method||**2D LEGO A**|**ssembly**|||**3D LEGO A**|**ssembly**|||**Object Rearra**|**ngement**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||2 bricks|_→_2 bricks_→_|2 bricks_→_|**S.R.**<br>2|bricks_→_|2 bricks_→_|2 bricks_→_|**S.R.**<br>2|objects|_→_2 objects_→_|2 objects|_→_**S.R.**|
|_π_0 [7]|0.25|0.20|0.15|0.15|0.25|0.15|0.10|0.10|0.35|0.20|0.10|0.10|
|_π_0_._5 [27]|0.30|0.25|0.25|0.20|0.30|0.20|0.15|0.15|0.45|0.25|0.15|0.15|
|FAST [63]|0.20|0.15|0.10|0.10|0.15|0.15|0.05|0.05|0.20|0.15|0.05|0.05|
|CoT-VLA [96]|0.40|0.35|0.30|0.30|0.35|0.30|0.25|0.25|0.60|0.40|0.30|0.30|
|VLM +_π_0_._5|0.75|0.70|0.65|0.60|0.65|0.45|0.35|0.35|**0.90**|0.55|0.65|0.50|
|**ManualVLA**|**0.95**|**0.90**|**0.85**|**0.85**|**0.90**|**0.75**|**0.65**|**0.65**|**0.90**|**0.70**|**0.80**|**0.65**|


Figure 4. For each task, we visualize three components: (1) manual ground truth (GT), (2) manual predictions (Pred.) generated by ManualVLA, and (3) the final goal image. 


Figure 5. Visualization of real-world experiments on Franka Research 3 dual-arm robots, executed from left to right. 

the low FID scores, particularly in the Object Rearrangement task, demonstrate that the generated image distribution closely matches that of real images, confirming their realism and fidelity. The remarkably low MAE scores further highlight ManualVLA’s precision in predicting the position of target objects. For language descriptions, we evaluate accuracy by checking the predicted object nouns, all of which are correctly generated on unseen test samples. 

Figure 4 presents qualitative results of ManualVLA on 2D and 3D LEGO assembly as well as object rearrangement tasks. The model accurately predicts intermediate steps that align with the ground truth, effectively capturing both spatial arrangements and object identities. In LEGO assembly, ManualVLA sequentially reconstructs the correct brick placements and colors, demonstrating precise step-wise rea- 

soning. For object rearrangement, it gradually progresses toward the final goal configuration and accurately generates the spatial relationships between objects. Overall, these results highlight ManualVLA’s strong intermediate reasoning capabilities in long-horizon tasks, establishing a reliable foundation for the action expert to generate accurate actions. 

#### **4.2.2. Action Generation** 

Across all three real-world long-horizon tasks, ManualVLA achieves the highest success rates, markedly outperforming all baselines. As shown in Table 2, we report both step-wise subgoal accuracy and end-to-end task success. Compared with the strongest hierarchical baseline, ManualVLA improves the final task completion rate by 15%-30%. While baseline models often succeed in the early stages of a longhorizon pipeline, they typically fail to sustain this performance through the whole sequence. In contrast, ManualVLA mitigates this degradation by decomposing complex tasks into structured subgoal manuals and grounding them into precise actions through a combination of explicit and implicit reasoning, enabling consistent performance throughout the entire task. Note that, as reflected in the manual generation results, the generated manuals may contain minor inaccuracies. Nevertheless, with the ManualCoT strategy and the capacity of our MoT architecture, ManualVLA remains robust and can still produce reliable actions even under moderate manual errors. In Appendix B, we also validate the advantages of our method on general manipulation tasks. 

The qualitative rollouts in Figure 5 further corroborate these results. ManualVLA generates structured and interpretable intermediate states that reliably guide the dual-arm system through precise grasping and relocation motions. In both LEGO assembly tasks, the robot maintains accurate brick alignment across all stages, while in the objectrearrangement task, it robustly manipulates objects with varying shapes, textures, and occlusions. More visualizations, failure case analyses, and execution videos are provided in Appendix C, Appendix D, and the supplementary material. 

### **4.3. Ablation Study** 

We conduct detailed ablation studies on the 2D LEGO Assembly task, reporting the long-horizon task success rate. **(a) What information should a generated manual contain?** 

13546 


Figure 6. **Ablation study.** We investigate the impact of (a) the information contained in the generated manuals, (b) explicit and implicit CoT reasoning, (c) the MoT architecture design, and (d) the action generation paradigm on long-horizon manipulation success rates. 

We explore three variants: generating only the target positions ( _U, V_ ), generating both target positions and subgoal images, and generating the full set of multimodal manual. As shown in Figure 6 (a), increasing the amount of multimodal information in the manuals leads to improved manipulation performance. Note that in this experiment, we consistently use explicit CoT visual-prompt images as inputs to the action expert. The results demonstrate that high-level textual descriptions for subtask understanding, next-step images for semantically reasoning, and position prompts for accurate localization all serve as critical implicit conditions that enable precise manipulation. **(b) Importance of Explicit CoT and Implicit CoT.** We examine two variants of our ManualCoT reasoning: (1) No Explicit CoT, where the action expert receives only the latent features from the planning expert, together with the current image; and (2) No Implicit CoT, where the action expert receives only the visual-prompt image. As shown in Figure 6 (b), both variants lead to a noticeable performance degradation compared to ManualVLA, demonstrating that explicit and implicit CoT reasoning are jointly indispensable for solving long-horizon, goal-defined manipulation tasks. **(c) The MoT Architecture and Action Generation Design.** In Figure 6 (c), we compare our MoT architecture with a standard Mixture-of-Experts (MoE) architecture (duplicate only FFNs in LLM) [18]. The results show that using an MoE strategy fails to produce high-quality manuals and actions simultaneously, both of which are crucial for long-horizon tasks. Meanwhile, we find that for precise manipulation tasks, diffusion-based action generation yields superior performance. More ablations on how manual quality influences manipulation performance are provided in Appendix B. 

### **4.4. Generalization Analysis** 

First, in Section 4.2, all final goal states used for evaluation differ from those in the teleoperated manipulation training set. Therefore, our main results simultaneously validate the generalization capability of ManualVLA with respect to both final goal states and object positions. In addition, we evaluate the robustness of ManualVLA under variations 

Table 3. **Generalization.** We report the mean success rate and performance degradation ratio for each task over 20 rollouts under variations in background, object shape, and lighting. 

|**Backgroun**|**d**|**Shape**||**Lighting**|
|---|---|---|---|---|
|2D LEGO|Origin|Background|Shape|Lighting|
|VLM +_π_0_._5|0.60|0.45(-25%)|0.35(-46%)|0.50(-17%)|
|ManualVLA|0.85|0.65(-23%)|0.60(-29%)|0.70(-17%)|


in background, object shape, and lighting. As shown in Table 3, these unseen perturbations are introduced in the 2D LEGO Assembly task and differ from all configurations seen during training. ManualVLA exhibits only a modest performance drop, which can be attributed to the rich guidance provided by our proposed manual generation expert and the CoT reasoning strategy during action prediction. Moreover, our proposed digital-twin toolkit provides large-scale manual generation data, allowing the model to produce accurate manuals even in unseen scenarios. 

## **5. Conclusion** 

In this work, we address the challenge of enabling robots to autonomously perform long-horizon tasks with defined goal states, such as LEGO assembly and object rearrangement. To this end, we introduce ManualVLA, a unified VLA model built on a Mixture-of-Transformers architecture that couples multimodal manual generation with action execution. Central to the model is a Manual Chain-of-Thought (ManualCoT) process, which converts subgoal manuals into precise actions by using them as explicit control conditions and implicit manipulation cues. To support scalable training, we further develop a 3D Gaussian Splatting-based digitaltwin pipeline that automatically produces large amounts of manual data. Experimental results on long-horizon tasks show that ManualVLA achieves a 32% higher average success rate than existing VLA methods. 

13547 

## **6. Acknowledgement** 

This work was supported by the National Natural Science Foundation of China (625B2007). This work was also supported by the National Natural Science Foundation of China (62476011). This work was also supported in part by the InnoHK initiative of the Innovation and Technology Commission of the Hong Kong Special Administrative Region Government via the Hong Kong Centre for Logistics Robotics. 

## **References** 

- [1] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. _Advances in Neural Information Processing Systems_ , 35:23716–23736, 2022. 1, 2 

- [2] Shikhar Bahl, Abhinav Gupta, and Deepak Pathak. Human-to-robot imitation in the wild. _arXiv preprint arXiv:2207.09450_ , 2022. 2, 3 

- [3] Suneel Belkhale, Yuchen Cui, and Dorsa Sadigh. Hydra: Hybrid robot actions for imitation learning. _arxiv_ , 2023. 1 

- [4] Xiao Bi, Deli Chen, Guanting Chen, Shanhuang Chen, Damai Dai, Chengqi Deng, Honghui Ding, Kai Dong, Qiushi Du, Zhe Fu, et al. Deepseek llm: Scaling opensource language models with longtermism. _arXiv preprint arXiv:2401.02954_ , 2024. 3 

- [5] Johan Bjorck, Fernando Castaneda,˜ Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 1, 2 

- [6] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pretrained imageediting diffusion models. _arXiv preprint arXiv:2310.10639_ , 2023. 4 

- [7] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, et al. pi0: A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 2, 3, 6, 7, 4 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 1 

- [9] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _arXiv preprint arXiv:2307.15818_ , 2023. 1, 2 

- [10] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 2 

- [11] Federico Ceola, Lorenzo Natale, Niko Sunderhauf, and Kr-¨ ishan Rana. Lhmanip: A dataset for long-horizon languagegrounded manipulation tasks in cluttered tabletop environments. _arXiv preprint arXiv:2312.12036_ , 2023. 1 

- [12] Hao Chen, Jiaming Liu, Chenyang Gu, Zhuoyang Liu, Renrui Zhang, Xiaoqi Li, Xiao He, Yandong Guo, Chi-Wing Fu, Shanghang Zhang, et al. Fast-in-slow: A dual-system foundation model unifying fast manipulation within slow reasoning. _arXiv preprint arXiv:2506.01953_ , 2025. 2 

- [13] Lawrence Yunliang Chen, Simeon Adebola, and Ken Goldberg. Berkeley UR5 demonstration dataset. https:// sites.google.com/view/berkeley-ur5/home. 1 

- [14] Xiaokang Chen, Zhiyu Wu, Xingchao Liu, Zizheng Pan, Wen Liu, Zhenda Xie, Xingkai Yu, and Chong Ruan. Januspro: Unified multimodal understanding and generation with data and model scaling. _arXiv preprint arXiv:2501.17811_ , 2025. 3, 5, 6 

- [15] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668, 2023. 5, 1 

- [16] Zichen Jeff Cui, Yibin Wang, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. From play to policy: Conditional behavior generation from uncurated robot data. _arXiv preprint arXiv:2210.10047_ , 2022. 1 

- [17] Shivin Dass, Jullian Yapeter, Jesse Zhang, Jiahui Zhang, Karl Pertsch, Stefanos Nikolaidis, and Joseph J. Lim. CLVR jaco play dataset, 2023. 1 

- [18] Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou, Feng Li, Zeyu Wang, Shu Zhong, Weihao Yu, Xiaonan Nie, Ziang Song, et al. Emerging properties in unified multimodal pretraining. _arXiv preprint arXiv:2505.14683_ , 2025. 4, 8 

- [19] Frederik Ebert, Yanlai Yang, Karl Schmeckpeper, Bernadette Bucher, Georgios Georgakis, Kostas Daniilidis, Chelsea Finn, and Sergey Levine. Bridge data: Boosting generalization of robotic skills with cross-domain datasets. _arXiv preprint arXiv:2109.13396_ , 2021. 1 

- [20] Patrick Esser, Robin Rombach, and Bjorn Ommer. Taming transformers for high-resolution image synthesis. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 12873–12883, 2021. 3 

- [21] figureai. Helix: A vision-language-action model for generalist humanoid control. https://www.figure.ai/ news/helix. Accessed 2025.5.7. 2 

- [22] Shenyuan Gao, Siyuan Zhou, Yilun Du, Jun Zhang, and Chuang Gan. Adaworld: Learning adaptable world models with latent actions. _arXiv preprint arXiv:2503.18938_ , 2025. 2 

- [23] Ankit Goyal, Jie Xu, Yijie Guo, Valts Blukis, Yu-Wei Chao, and Dieter Fox. Rvt: Robotic view transformer for 3d object manipulation. In _Conference on Robot Learning_ , pages 694–710. PMLR, 2023. 4 

- [24] Jiayuan Gu, Fanbo Xiang, Xuanlin Li, Zhan Ling, Xiqiang Liu, Tongzhou Mu, Yihe Tang, Stone Tao, Xinyue Wei, Yunchao Yao, Xiaodi Yuan, Pengwei Xie, Zhiao Huang, Rui 

13548 

Chen, and Hao Su. Maniskill2: A unified benchmark for generalizable manipulation skills, 2023. 1 

- [25] Minho Heo, Youngwoon Lee, Doohyun Lee, and Joseph J. Lim. Furniturebench: Reproducible real-world benchmark for long-horizon complex manipulation. In _Robotics: Science and Systems_ , 2023. 1 

- [26] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 2 

- [27] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, et al. _π_ 0 _._ 5: a vision-languageaction model with open-world generalization, 2025. 1, 2, 6, 7, 4 

- [28] Vidhi Jain, Maria Attarian, Nikhil J Joshi, Ayzaan Wahid, Danny Driess, Quan Vuong, Pannag R Sanketi, Pierre Sermanet, Stefan Welker, Christine Chan, et al. Vid2robot: End-to-end video-conditioned policy learning with crossattention transformers. _arXiv preprint arXiv:2403.12943_ , 2024. 2, 3 

- [29] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019–3026, 2020. 2, 3 

- [30] Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pages 991–1002. PMLR, 2022. 1 

- [31] Yueru Jia, Jiaming Liu, Sixiang Chen, Chenyang Gu, Zhilve Wang, Longzan Luo, Xiaoqi Li, Pengwei Wang, Zhongyuan Wang, Renrui Zhang, et al. Lift3d policy: Lifting 2d foundation models for robust 3d robotic manipulation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 17347–17358, 2025. 4 

- [32] Dmitry Kalashnikov, Alex Irpan, Peter Pastor, Julian Ibarz, Alexander Herzog, Eric Jang, Deirdre Quillen, Ethan Holly, Mrinal Kalakrishnan, Vincent Vanhoucke, et al. QTOpt: Scalable deep reinforcement learning for vision-based robotic manipulation. _arXiv preprint arXiv:1806.10293_ , 2018. 1 

- [33] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ , 2024. 1, 2 

- [34] Bernhard Kerbl, Georgios Kopanas, Thomas Leimkuhler,¨ and George Drettakis. 3d gaussian splatting for real-time radiance field rendering, 2023. 2, 6 

- [35] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, Peter David Fagan, Joey Hejna, Masha Itkina, Marion Lepert, Yecheng Jason Ma, Patrick Tree Miller, Jimmy Wu, Suneel Belkhale, Shivin Dass, Huy Ha, 

   - Arhan Jain, Abraham Lee, Youngwoon Lee, Marius Memmel, Sungjae Park, Ilija Radosavovic, Kaiyuan Wang, Albert Zhan, Kevin Black, Cheng Chi, Kyle Beltran Hatch, Shan Lin, Jingpei Lu, Jean Mercat, Abdul Rehman, Pannag R Sanketi, Archit Sharma, Cody Simpson, Quan Vuong, Homer Rich Walke, Blake Wulfe, Ted Xiao, Jonathan Heewon Yang, Arefeh Yavary, Tony Z. Zhao, Christopher Agia, Rohan Baijal, Mateo Guaman Castro, Daphne Chen, Qiuyu Chen, Trinity Chung, Jaimyn Drake, Ethan Paul Foster, Jensen Gao, David Antonio Herrera, Minho Heo, Kyle Hsu, Jiaheng Hu, Donovon Jackson, Charlotte Le, Yunshuang Li, Kevin Lin, Roy Lin, Zehan Ma, Abhiram Maddukuri, Suvir Mirchandani, Daniel Morton, Tony Nguyen, Abigail O’Neill, Rosario Scalise, Derick Seale, Victor Son, Stephen Tian, Emi Tran, Andrew E. Wang, Yilin Wu, Annie Xie, Jingyun Yang, Patrick Yin, Yunchu Zhang, Osbert Bastani, Glen Berseth, Jeannette Bohg, Ken Goldberg, Abhinav Gupta, Abhishek Gupta, Dinesh Jayaraman, Joseph J Lim, Jitendra Malik, Roberto Mart´ın-Mart´ın, Subramanian Ramamoorthy, Dorsa Sadigh, Shuran Song, Jiajun Wu, Michael C. Yip, Yuke Zhu, Thomas Kollar, Sergey Levine, and Chelsea Finn. Droid: A large-scale in-the-wild robot manipulation dataset. 2024. 2, 5, 1 

- [36] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 3 

- [37] Vikash Kumar, Rutav Shah, Gaoyue Zhou, Vincent Moens, Vittorio Caggiano, Abhishek Gupta, and Aravind Rajeswaran. Robohive: A unified framework for robot learning. In _Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ , 2023. 1 

- [38] Michelle A. Lee, Yuke Zhu, Krishnan Srinivasan, Parth Shah, Silvio Savarese, Li Fei-Fei, Animesh Garg, and Jeannette Bohg. Making sense of vision and touch: Self-supervised learning of multimodal representations for contact-rich tasks, 2019. 1 

- [39] Chengmeng Li, Junjie Wen, Yan Peng, Yaxin Peng, Feifei Feng, and Yichen Zhu. Pointvla: Injecting the 3d world into vision-language-action models, 2025. 2 

- [40] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 2, 4 

- [41] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025. 2 

- [42] Xiaoqi Li, Liang Heng, Jiaming Liu, Yan Shen, Chenyang Gu, Zhuoyang Liu, Hao Chen, Nuowei Han, Renrui Zhang, Hao Tang, et al. 3ds-vla: A 3d spatial-aware vision language action model for robust multi-task manipulation. In _9th Annual Conference on Robot Learning_ , 2025. 2 

- [43] Junbang Liang, Ruoshi Liu, Ege Ozguroglu, Sruthi Sudhakar, Achal Dave, Pavel Tokmakov, Shuran Song, and Carl 

13549 

Vondrick. Dreamitate: Real-world visuomotor policy learning via video generation. _arXiv preprint arXiv:2406.16862_ , 2024. 2 

- [44] Weixin Liang, Lili Yu, Liang Luo, Srinivasan Iyer, Ning Dong, Chunting Zhou, Gargi Ghosh, Mike Lewis, Wen-tau Yih, Luke Zettlemoyer, et al. Mixture-of-transformers: A sparse and scalable architecture for multi-modal foundation models. _arXiv preprint arXiv:2411.04996_ , 2024. 2 

- [45] Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. Onetwovla: A unified visionlanguage-action model with adaptive reasoning. _arXiv preprint arXiv:2505.11917_ , 2025. 1 

- [46] Huihan Liu, Soroush Nasiriany, Lance Zhang, Zhiyao Bao, and Yuke Zhu. Robot learning on the job: Human-in-theloop autonomy and learning during deployment. In _Robotics: Science and Systems (RSS)_ , 2023. 1 

- [47] Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Pengju An, Xiaoqi Li, Kaichen Zhou, Senqiao Yang, Renrui Zhang, Yandong Guo, and Shanghang Zhang. Robomamba: Efficient vision-language-action model for robotic reasoning and manipulation. _Advances in Neural Information Processing Systems_ , 37:40085–40110, 2024. 1, 2 

- [48] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model. _arXiv preprint arXiv:2503.10631_ , 2025. 1, 2 

- [49] Zhuoyang Liu, Jiaming Liu, Jiadong Xu, Nuowei Han, Chenyang Gu, Hao Chen, Kaichen Zhou, Renrui Zhang, Kai Chin Hsieh, Kun Wu, et al. Mla: A multisensory language-action model for multimodal understanding and forecasting in robotic manipulation. _arXiv preprint arXiv:2509.26642_ , 2025. 2 

- [50] Yuxing Long, Jiyao Zhang, Mingjie Pan, Tianshu Wu, Taewhan Kim, and Hao Dong. Checkmanual: A new challenge and benchmark for manual-based appliance manipulation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22595–22604, 2025. 2, 3 

- [51] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_ , 2017. 4 

- [52] Ilya Loshchilov and Frank Hutter. Sgdr: Stochastic gradient descent with warm restarts, 2017. 4 

- [53] Jianlan Luo, Charles Xu, Xinyang Geng, Gilbert Feng, Kuan Fang, Liam Tan, Stefan Schaal, and Sergey Levine. Multistage cable routing through hierarchical imitation learning. _arXiv preprint arXiv:2307.08927_ , 2023. 1 

- [54] Jianlan Luo, Charles Xu, Fangchen Liu, Liam Tan, Zipeng Lin, Jeffrey Wu, Pieter Abbeel, and Sergey Levine. Fmb: a functional manipulation benchmark for generalizable robotic learning. _arXiv preprint arXiv:2401.08553_ , 2024. 1 

- [55] Corey Lynch, Ayzaan Wahid, Jonathan Tompson, Tianli Ding, James Betker, Robert Baruch, Travis Armstrong, and Pete Florence. Interactive language: Talking to robots in real time. _IEEE Robotics and Automation Letters_ , 2023. 1 

- [56] Ajay Mandlekar, Yuke Zhu, Animesh Garg, Jonathan Booher, Max Spero, Albert Tung, Julian Gao, John Emmons, Anchit Gupta, Emre Orbay, Silvio Savarese, and Li 

Fei-Fei. RoboTurk: A crowdsourcing platform for robotic skill learning through imitation. _CoRR_ , abs/1811.02790, 2018. 1 

- [57] Oier Mees, Jessica Borja-Diaz, and Wolfram Burgard. Grounding language with visual affordances over unstructured data. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , London, UK, 2023. 1 

- [58] Russell Mendonca, Shikhar Bahl, and Deepak Pathak. Structured world models from human videos. _CoRL_ , 2023. 1 

- [59] Soroush Nasiriany, Tian Gao, Ajay Mandlekar, and Yuke Zhu. Learning and retrieval from prior data for skillbased imitation learning. In _Conference on Robot Learning (CoRL)_ , 2022. 1 

- [60] Soroush Nasiriany, Fei Xia, Wenhao Yu, Ted Xiao, Jacky Liang, Ishita Dasgupta, Annie Xie, Danny Driess, Ayzaan Wahid, Zhuo Xu, Quan Vuong, Tingnan Zhang, TsangWei Edward Lee, Kuang-Huei Lee, Peng Xu, Sean Kirmani, Yuke Zhu, Andy Zeng, Karol Hausman, Nicolas Heess, Chelsea Finn, Sergey Levine, and Brian Ichter. Pivot: Iterative visual prompting elicits actionable knowledge for vlms. 2024. 2 

- [61] Open X-Embodiment Collaboration, Abhishek Padalkar, Acorn Pooley, et al. Open X-Embodiment: Robotic learning datasets and RT-X models. https://arxiv.org/ abs/2310.08864, 2023. 2, 5, 1 

- [62] Georgios Papagiannis, Norman Di Palo, Pietro Vitiello, and Edward Johns. R+ x: Retrieval and execution from everyday human videos. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8284–8290. IEEE, 2025. 2 

- [63] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, et al. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 2, 6, 7, 4 

- [64] Ava Pun, Kangle Deng, Ruixuan Liu, Deva Ramanan, Changliu Liu, and Jun-Yan Zhu. Generating physically stable and buildable brick structures from text. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 14798–14809, 2025. 3 

- [65] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 2 

- [66] Gabriel Quere, Annette Hagengruber, Maged Iskandar, Samuel Bustamante, Daniel Leidner, Freek Stulp, and Joern Vogel. Shared Control Templates for Assistive Robotics. In _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , page 7, Paris, France, 2020. 1 

- [67] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PMLR, 2021. 2 

- [68] Ilija Radosavovic, Tete Xiao, Stephen James, Pieter Abbeel, Jitendra Malik, and Trevor Darrell. Real-world robot learn- 

13550 

ing with masked visual pre-training. In _Conference on Robot Learning_ , pages 416–426. PMLR, 2023. 1 

- [69] Erick Rosete-Beas, Oier Mees, Gabriel Kalweit, Joschka Boedecker, and Wolfram Burgard. Latent plans for task agnostic offline reinforcement learning. In _Proceedings of the 6th Conference on Robot Learning (CoRL)_ , 2022. 1 

- [70] Saumya Saxena, Mohit Sharma, and Oliver Kroemer. Multiresolution sensing for real-time control with vision-language models. In _7th Annual Conference on Robot Learning_ , 2023. 1 

- [71] Nur Muhammad Mahi Shafiullah, Anant Rai, Haritheja Etukuru, Yiqian Liu, Ishan Misra, Soumith Chintala, and Lerrel Pinto. On bringing robots home, 2023. 1 

- [72] Rutav Shah, Roberto Mart´ın-Mart´ın, and Yuke Zhu. MUTEX: Learning unified policies from multimodal task specifications. In _7th Annual Conference on Robot Learning_ , 2023. 1 

- [73] Kenneth Shaw, Shikhar Bahl, and Deepak Pathak. Videodex: Learning dexterity from internet videos. _ArXiv_ , abs/2212.04498, 2022. 3 

- [74] Haochen Shi, Huazhe Xu, Samuel Clarke, Yunzhu Li, and Jiajun Wu. Robocook: Long-horizon elasto-plastic object manipulation with diverse tools, 2023. 1 

- [75] Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, Adrian Li-Bell, Danny Driess, Lachy Groom, Sergey Levine, and Chelsea Finn. Hi robot: Open-ended instruction following with hierarchical vision-language-action models, 2025. 6 

- [76] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiveractor: A multi-task transformer for robotic manipulation. In _Proceedings of the 6th Conference on Robot Learning (CoRL)_ , 2022. 2, 4 

- [77] Ioan A Sucan, Mark Moll, and Lydia E Kavraki. The open motion planning library. _IEEE Robotics & Automation Magazine_ , 19(4):72–82, 2012. 4 

- [78] Priya Sundaresan, Quan Vuong, Jiayuan Gu, Peng Xu, Ted Xiao, Sean Kirmani, Tianhe Yu, Michael Stark, Ajinkya Jain, Karol Hausman, Dorsa Sadigh, Jeannette Bohg, and Stefan Schaal. Rt-sketch: Goal-conditioned imitation learning from hand-drawn sketches, 2024. 6 

- [79] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe HansenEstruch, Quan Vuong, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale, 2023. 1 

- [80] Chen Wang, Haochen Shi, Weizhuo Wang, Ruohan Zhang, Li Fei-Fei, and C Karen Liu. Dexcap: Scalable and portable mocap data collection system for dexterous manipulation. _arXiv preprint arXiv:2403.07788_ , 2024. 2, 3 

- [81] Ruocheng Wang, Yunzhi Zhang, Jiayuan Mao, Chin-Yi Cheng, and Jiajun Wu. Translating a visual lego manual to a machine-executable plan. In _European Conference on Computer Vision_ , pages 677–694. Springer, 2022. 3 

- [82] Junjie Wen, Minjie Zhu, Yichen Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Chengmeng Li, Xiaoyu Liu, Yaxin Peng, 

Chaomin Shen, et al. Diffusion-vla: Scaling robot foundation models via unified diffusion and autoregression. _arXiv preprint arXiv:2412.03293_ , 2024. 2 

- [83] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 2 

- [84] Chengyue Wu, Xiaokang Chen, Zhiyu Wu, Yiyang Ma, Xingchao Liu, Zizheng Pan, Wen Liu, Zhenda Xie, Xingkai Yu, Chong Ruan, et al. Janus: Decoupling visual encoding for unified multimodal understanding and generation. _arXiv preprint arXiv:2410.13848_ , 2024. 2 

- [85] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In _International Conference on Learning Representations_ , 2024. 2 

- [86] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, et al. Robomind: Benchmark on multiembodiment intelligence normative data for robot manipulation. In _Robotics: Science and Systems (RSS) 2025_ . Robotics: Science and Systems Foundation, 2025. 5, 1 

- [87] Mingdong Wu, Fangwei Zhong, Yulong Xia, and Hao Dong. Targf: Learning target gradient field to rearrange objects without explicit goal specification. _Advances in Neural Information Processing Systems_ , 35:31986–31999, 2022. 3 

- [88] Ge Yan, Kris Wu, and Xiaolong Wang. ucsd kitchens Dataset. 2023. 1 

- [89] Shuai Yang, Hao Li, Yilun Chen, Bin Wang, Yang Tian, Tai Wang, Hanqing Wang, Feng Zhao, Yiyi Liao, and Jiangmiao Pang. Instructvla: Vision-language-action instruction tuning from understanding to manipulation. _arXiv preprint arXiv:2507.17520_ , 2025. 1 

- [90] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, et al. Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ , 2024. 2 

- [91] Yiming Zeng, Mingdong Wu, Long Yang, Jiyao Zhang, Hao Ding, Hui Cheng, and Hao Dong. Lvdiffusor: Distilling functional rearrangement priors from large models into diffusor. _IEEE Robotics and Automation Letters_ , 2024. 3 

- [92] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 11975–11986, 2023. 3 

- [93] Jianke Zhang, Yanjiang Guo, Xiaoyu Chen, Yen-Jen Wang, Yucheng Hu, Chengming Shi, and Jianyu Chen. Hirt: Enhancing robotic control with hierarchical robot transformers. _arXiv preprint arXiv:2410.05273_ , 2024. 2 

- [94] Jiahao Zhang, Anoop Cherian, Cristian Rodriguez, Weijian Deng, and Stephen Gould. Manual-pa: Learning 3d part assembly from instruction diagrams. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 6304–6314, 2025. 3 

- [95] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, He Wang, 

13551 

Zhizheng Zhang, et al. Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge. _arXiv preprint arXiv:2507.04447_ , 2025. 2 

- [96] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 6, 7, 4 

- [97] Gaoyue Zhou, Victoria Dean, Mohan Kumar Srirama, Aravind Rajeswaran, Jyothish Pari, Kyle Hatch, Aryan Jain, Tianhe Yu, Pieter Abbeel, Lerrel Pinto, Chelsea Finn, and Abhinav Gupta. Train offline, test online: A real robot learning benchmark, 2023. 1 

- [98] Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. Robodreamer: Learning compositional world models for robot imagination. _arXiv preprint arXiv:2404.12377_ , 2024. 2 

- [99] Xinghao Zhu, Ran Tian, Chenfeng Xu, Mingyu Ding, Wei Zhan, and Masayoshi Tomizuka. Fanuc manipulation: A dataset for learning-based manipulation with fanuc mate 200id robot. 2023. 1 

- [100] Yifeng Zhu, Peter Stone, and Yuke Zhu. Bottom-up skill discovery from unsegmented demonstrations for long-horizon robot manipulation. _IEEE Robotics and Automation Letters_ , 7(2):4126–4133, 2022. 1 

- [101] Yifeng Zhu, Abhishek Joshi, Peter Stone, and Yuke Zhu. Viola: Imitation learning for vision-based manipulation with object proposal priors, 2023. 1 

13552 

