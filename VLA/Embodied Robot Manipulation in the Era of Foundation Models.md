---
title: "Embodied Robot Manipulation in the Era of Foundation Models: Planning and Learning Perspectives"
date: "2025-12-28"
authors: "Shuanghao Bai; Wenxuan Song; Jiayi Chen; Yuheng Ji; Zhide Zhong; Jin Yang"
venue: "T-RO"
url: https://arxiv.org/abs/2512.22983
pdf: https://arxiv.org/pdf/2512.22983
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.22983)** / [論文ページ](https://arxiv.org/abs/2512.22983)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Embodied Robot Manipulation in the Era of Foundation Models: Planning and Learning Perspectives 

Shuanghao Bai<sup>1</sup><sup>_∗_</sup> Wenxuan Song<sup>2</sup><sup>_∗_</sup> Jiayi Chen<sup>2</sup> Yuheng Ji<sup>3</sup> Zhide Zhong<sup>2</sup> Jin Yang<sup>1</sup> Han Zhao<sup>4</sup><sup>_,_5</sup> Wanqi Zhou<sup>1</sup> Zhe Li<sup>6</sup> Pengxiang Ding<sup>4</sup><sup>_,_5</sup> Cheng Chi<sup>7</sup> Chang Xu<sup>6</sup> Xiaolong Zheng<sup>3</sup> Donglin Wang<sup>4</sup> Haoang Li<sup>2</sup><sup>_†_</sup> Shanghang Zhang<sup>8</sup><sup>_†_</sup> Badong Chen<sup>1</sup><sup>_†_</sup> 1 Xi’an Jiaotong University, 2 Hong Kong University of Science and Technology (Guangzhou), 3 Chinese Academy of Sciences, 4 Westlake University, 5 Zhejiang University, 6 University of Sydney, 7 BAAI, 8 Peking University _∗_ **Equal Contributors** _†_ **Corresponding Authors** GitHub: Awesome-Robotics-Manipulation 

**_Abstract_ —Recent advances in vision, language, and multimodal learning have significantly accelerated progress in robotic foundation models, with robotic manipulation remaining one of the most challenging embodied tasks. Its difficulty lies in integrating perception, semantic understanding, task reasoning, physically grounded action generation, and reliable execution. This survey examines robotic manipulation from an algorithmic perspective and organizes recent learning-based approaches through a unified abstraction of high-level planning and low-level action modeling. At the high level, we extend the classical notion of task planning to include reasoning over language, code, affordances, geometric constraints, and 3D representations. At the low level, we present a learning-paradigm-oriented taxonomy of learningbased action models, covering input modeling, latent learning, and policy learning. Within this abstraction, foundation models contribute either by generating structured planning artifacts that are instantiated as constraints or latent inputs for downstream action generation, or by directly modeling executable actions and trajectories. Finally, we summarize open challenges and future directions related to scalability, generalization, data efficiency, multimodal physical interaction, and safety. Together, this survey provides a structured view of the design space and emerging trends in foundation models for robotic manipulation.** 

**_Index Terms_ —Robot manipulation, robotic foundation model, high-level planner, imitation learning, reinforcement learning, vision-language-action models, latent learning, policy learning** 

## I. INTRODUCTION 

In recent years, embodied intelligence has emerged as a major frontier in artificial intelligence, driven by advances in computer vision, natural language processing, and large-scale foundation models [1], [2]. Among embodied tasks, robotic manipulation is particularly challenging because it requires closing the loop from perception and semantic understanding to task reasoning, physically grounded action generation, and reliable execution. This difficulty is further compounded by the diversity of manipulation settings, which vary across operation mode, object property, and robot embodiment. Representative examples include basic manipulation with single-arm or dualarm robots for object-centric tasks, dexterous manipulation with multi-fingered hands for fine-grained control, deformable object manipulation over non-rigid objects, and embodied settings such as mobile, quadrupedal, and humanoid manipulation [3], as illustrated in Figure 1. Unlike navigation or 


Fig. 1. Representative robotic manipulation scenarios spanning diverse manipulation settings, including basic manipulation [4], dexterous manipulation [5], deformable object manipulation [6], and embodied manipulation such as mobile [7], quadrupedal [8], and humanoid manipulation [9]. 

locomotion, which primarily regulate the robot’s own motion, manipulation involves contact-rich interactions that intentionally alter object states, making it inherently a multi-level problem spanning reasoning, action generation, and control. 

Recent progress in robotic manipulation has been largely driven by data-driven approaches, including deep visuomotor policies [10]–[12], imitation learning [13], reinforcement learning [14], and, more recently, robotic foundation models [15]–[17]. These foundation models enhance perceptual and semantic representations and enable flexible task conditioning through multimodal inputs such as language and vision. Importantly, their roles in manipulation systems naturally align with the multi-level structure of the problem: they can operate either as high-level modules that generate structured guidance (e.g., task plans [18], [19], code [20], affordances [21], or geometric constraints [22]) or as low-level models that directly parameterize actions or trajectories [23]. 

To systematically capture this multi-level structure, we adopt the taxonomy illustrated in Figure 2, which decomposes robotic manipulation into three layers: High-Level Planning, Low-Level Action Modeling, and Actuation-Level Control. High-level modules produce structured artifacts that guide 


Fig. 2. Overview of the proposed taxonomy for foundation-model-based robotic manipulation. The pipeline is decomposed into three layers: HighLevel Planning, Low-Level Action Modeling, and Actuation-Level Control. High-level modules produce structured planning artifacts, either as explicit inputs or as constraints for downstream action generation. Low-level action modeling includes both classical non-learning methods and learning-based approaches, and operates either on such artifacts or directly on raw multimodal observations. Solid arrows denote the primary scope of this survey, namely High-Level Planning and Learning-Based Low-Level Action Modeling. 

downstream behavior, while low-level modules generate executable actions or trajectories that are ultimately realized through the actuation layer on the robot. Within this hierarchy, our primary focus is on High-Level Planning (Section II) and Learning-Based Low-Level Action Modeling (Section III), where foundation models most directly reshape robotic manipulation. In this context, we define a robotic foundation model as a model pretrained on diverse robotic and/or multimodal data that enables transferable manipulation across tasks, objects, or environments through reusable representations or policies. Rather than imposing rigid thresholds on model size or dataset scale, we characterize such models by three practical properties: diverse pretraining, broad capability scope, and reusability for downstream adaptation. 

Building on this taxonomy, we develop a structured understanding of learning-based robotic manipulation through the dual lens of High-Level Planning and Learning-based Low-Level Action Modeling, providing a unified view of how modern systems couple high-level reasoning with lowlevel action generation. Unlike prior surveys that organize the literature mainly by model families, such as vision-languageaction models [24]–[26], diffusion policies [27], or generative 

approaches [28], our perspective emphasizes the functional roles of different components and their interactions across levels. Under this view, we introduce a systematic taxonomy that categorizes high-level methods into task planning, programmatic planning, geometric constraint generation, affordance modeling, and 3D representations, while organizing low-level action models by input modeling, latent learning, and policy learning. This unified framework enables more coherent comparisons across approaches and reveals common design patterns that are less visible when methods are grouped only by model family. Based on this structured perspective, we also synthesize emerging trends and identify four future directions: more general-purpose robotic foundation models, improved data scaling and sim-to-real transfer, richer multimodal physical interaction, and safer real-world deployment. 

## II. HIGH-LEVEL PLANNING 

High-level planning plays a central role in robotic manipulation by providing structured guidance for downstream execution. It determines action intent, temporal organization, and attentional focus over the environment, thereby shaping how perception and control are coordinated. Large language models and multimodal large language models have become increasingly influential at this level, supporting task decomposition, skill sequencing, and adaptive reasoning grounded in language and perception. Complementarily, affordance learning highlights action-relevant regions and object relations, while 3D scene representations provide spatial structure and geometric constraints for planning. Together, these approaches show that high-level planning can guide manipulation through different forms of structured intermediate representations. Formally, this layer can be written as 


where _o_ denotes observations and _l_ denotes language instructions. Depending on the method, the planning artifact _A_ plan may take the form of task plans, programs, geometric constraints, affordance priors, or 3D representations. These artifacts are not executable actions themselves; instead, they provide structured guidance for downstream action generation, for example by being transformed into target poses or spatial constraints for conventional motion planning and control, or by being encoded as conditions for learning-based action models. 

This view provides a natural basis for organizing the literature in this section. We summarize this taxonomy in Figure 3 and provide an illustrative overview in Figure 4. 

## _A. LLM-based Task Planning_ 

Early high-level planning methods followed a symbolic grounding paradigm, where neural networks mapped demonstrations and observations into symbolic states and goals [62]. With the emergence of large language models, this paradigm shifted toward language-centric planning. SayCan [18] was an early milestone, using an LLM as a global planner to select executable skills based on language-level relevance and affordance-based feasibility. Grounded Decoding [29] further relaxed the reliance on fixed skill libraries by enabling joint 

2 


Fig. 3. Taxonomy of high-level planning approaches for robotic manipulation, organized into six categories: LLM-based task planning, MLLM-based task planning, programmatic planning, geometric constraint-based planning, affordance-based planning, and 3D representation-based planning. 

decoding between language and grounding models for openvocabulary planning. A key limitation of early LLM-based planners is the lack of execution-time feedback. Inner Monologue [63] addresses this through a closed-loop framework that incorporates real-time feedback, scene descriptions, and human input for dynamic plan revision. Subsequent work further improves robustness and scope through feedbackdriven planning [30], explicit modeling of constraints and failures for long-horizon reasoning [31], [32], multi-agent collaboration [33], more open-ended interactive settings [34], [64], and multi-robot coordination [65]. 

Overall, LLM-based task planning provides strong semantic reasoning and task decomposition, but purely language-based plans often lack numerically consistent physical understanding and may fail to satisfy geometric, kinematic, or contact constraints required for reliable execution. As a result, semantically plausible plans may still be physically infeasible, making downstream grounding, affordance estimation, and execution feedback essential for robust robotic manipulation. 

Existing work mainly follows three directions. A first line adapts general-purpose MLLMs for embodied decision making. PaLM-E [19] co-trains a vision–language model on robot embodiment data alongside standard VLM objectives, enabling end-to-end task reasoning at the cost of substantial data and computation. VILA [35] instead shows that offthe-shelf GPT-4V can support manipulation planning without robot-specific fine-tuning, while PG-InstructBLIP [36] improves manipulation-relevant reasoning by injecting physical priors through lightweight object-centric fine-tuning. A second line strengthens MLLM-based planning through additional reasoning structure, such as chain-of-thought reasoning [37], [67], scene-graph-based spatial structure [68], multi-agent coordination [69], and failure-aware planning [70]. More recently, a third line has begun to develop robotics-specific MLLMs trained on large-scale robot-centric data, including RoboBrain [17], Gemini Robotics-ER [38], and RynnEC [71], suggesting a promising step toward foundation models tailored for robotic manipulation. 

## _B. MLLM-based Task Planning_ 

Early large language models are inherently unimodal, operating only on text, with perception handled by separate vision modules whose outputs are serialized into language. Recent multimodal large language models (MLLMs) [2], [66] relax this separation by jointly reasoning over vision and language, and have increasingly been adopted in robotic manipulation to improve high-level planning while simplifying system design. 

A practical consideration of MLLM-based task planning is computational cost and latency. Unlike reactive visuomotor policies or VLA-style action models, whose inference is directly coupled to action generation, MLLM-based planners typically operate at the task level by producing intermediate plans or subgoals. Their cost therefore mainly affects highlevel decision or replanning latency, rather than the inner control loop during trajectory execution. 

3 


Fig. 4. Overview of the taxonomy of high-level planners, highlighting six core components: LLM- and MLLM-based, programmatic, geometric constraintbased, affordance-based, and 3D representation-based planning. Figure are adapted from [20], [22], [30], [37], [46], [58]. 

## _C. Programmatic Planning_ 

While LLMs and MLLMs have shown strong capabilities in task decomposition and high-level reasoning, purely language-based plans often lack the precision and executability required for reliable manipulation in diverse environments. Programmatic planning addresses this limitation by using code generation as an intermediate abstraction between highlevel reasoning and low-level control. By expressing plans as executable programs, these methods provide explicit structure, conditional logic, and compositionality, enabling finer-grained and more adaptive control. 

Early efforts explored translating natural language instructions into programmatic representations without modern foundation models [72]. With the advent of LLMs, Code as Policies [20] established this paradigm by exposing perception and control APIs as prompts, allowing an LLM to generate executable code for robot behavior. Related work such as 

ProgPrompt [39] further demonstrated the generality of codedriven control for manipulation. Subsequent studies expanded the scope and robustness of this paradigm: Instruct2Act [73] improves zero-shot generalization by combining code generation with visual foundation models, Demo2Code [40] summarizes long-horizon demonstrations into compact programs, and SHOWTELL [41] directly translates visual demonstrations into policy code. To improve execution robustness, Statler [42] maintains an explicit world state during program execution, while HyCodePolicy [74] integrates symbolic execution traces with perceptual feedback for more reliable closed-loop control. Overall, programmatic planning provides a structured and interpretable interface that more tightly couples high-level reasoning with low-level execution. However, the explicit executability of generated programs also raises challenges for safety and formal verification, since LLM-generated code may contain invalid operations, unsafe action sequences, or logic that fails to respect physical constraints. These issues make 

4 

program correctness, constraint satisfaction, and runtime monitoring especially important in safety-critical robotic settings. 

## _D. Geometric Constraint-based Planning_ 

Geometric objective and constraint generation serves as an intermediate abstraction between symbolic task reasoning and low-level motion execution. Rather than directly synthesizing trajectories, these approaches translate language and perception into structured spatial objectives or relational constraints that are subsequently optimized by classical motion planners. VoxPoser [22] constructs composable 3D value maps conditioned on language instructions, enabling motion generation through optimization over spatial cost fields. ReKep [44] formulates manipulation as relational keypoint constraint satisfaction, producing geometry-aware constraints over objectcentric keypoints. CoPa [43] infers part-level spatial relations and converts them into target end-effector poses for downstream planning, explicitly incorporating contact geometry and functional part relations. Similarly, GeoManip [45] treats geometric constraints as a general-purpose interface between semantic reasoning and optimization-based motion generation. Collectively, these methods use foundation models to infer structured geometric planning artifacts, while delegating final trajectory generation to downstream planners or optimization modules. This decomposition improves modularity, interpretability, and physical grounding, and positions geometric objective generation as a mid-level planning interface within robotic manipulation. 

## _E. Affordance-based Planning_ 

Affordance learning shifts the focus of robotic manipulation from recognizing what objects are to inferring what actions they enable. Originating from Gibson’s theory of affordances [75], this concept links perception to action by characterizing the interaction possibilities that objects or environments provide relative to an agent’s capabilities. In robotics, affordances serve as a useful abstraction for grounding manipulation decisions in physical structure and functional intent. Early work emphasized geometric and model-based reasoning, while recent advances increasingly learn affordances directly from sensory data, often with self-supervision or foundation-model priors. In this section, we review affordance learning from four perspectives: geometric, visual, semantic, and multimodal. 

**Geometric Affordance.** Geometric affordance relates interaction possibilities to an object’s 3D geometry, part structure, and kinematic properties. This line of work focuses on inferring part-level geometry and articulation constraints directly from 3D observations [46], [47]. Representative methods such as Ditto [46] and GAPartNet [47] ground affordances in object dynamics and reusable part taxonomies, while compositional approaches such as CPM [48] model manipulation as structured combinations of geometric constraints. 

**Visual Affordance.** Visual affordance learning infers action possibilities directly from 2D observations, typically through dense pixel-wise affordance prediction [49], [50]. Transporter 

Networks [49] established this paradigm by predicting pickand-place heatmaps in pixel space without explicit object models, while later work such as VAPO [50] improved scalability through self-supervised learning from unstructured play data. **Semantic Affordance.** Semantic affordance leverages semantic priors, such as object categories or part names, to guide manipulation. Early work such as affordance-based imitation learning [51] associated semantic parts (e.g., handles or lids) with manipulation trajectories, illustrating how abstract symbolic cues can support generalization across objects with similar functional structure. 

**Multimodal Affordance.** Recent work increasingly combines visual, linguistic, geometric, and spatial cues to support more holistic affordance reasoning. Representative examples include CLIPort [21], which decouples semantic grounding from spatial localization, extensions to part-level affordances [76], [77], and approaches that incorporate explicit 3D spatial reasoning for precise grounding [52], [78]. More recent efforts aim to learn unified and transferable affordance representations across objects and tasks [79], [80]. 

Affordance-based planning offers an action-centric bridge from perception to manipulation, but predictions can be ambiguous, perception-sensitive, and unreliable in cluttered, novel, or long-horizon settings. Since affordances do not ensure geometric feasibility or executability, they typically require downstream planning and control. 

## _F. 3D Representation-based Planning_ 

Although 3D representations such as Gaussian Splatting and neural descriptor fields do not directly output control commands, they serve as mid-level planning interfaces by transforming perception into structured action-relevant representations, such as grasp candidates, spatial correspondences, or optimization objectives. In this sense, they bridge perception and action and naturally fall under high-level planning. 

One line of work uses Gaussian Splatting as an editable and semantically enriched scene representation for manipulation. Splat-MOVER [81] distills open-vocabulary semantics into a 3DGS scene to propose grasp candidates for downstream planning, while object-aware and physically embodied variants extend Gaussian Splatting with object-centric reconstruction and physics coupling for dynamic interaction [82], [83]. Building on this editability, RoboSplat [56] synthesizes diverse demonstrations by directly manipulating reconstructed scenes, improving one-shot generalization of visuomotor policies. A complementary line represents scenes as implicit or descriptor fields in continuous 3D space. Neural Descriptor Fields learn SE(3)-equivariant representations for pose transfer and relational rearrangement [57], [84], while F3RM and _D_<sup>3</sup> Fields distill foundation-model features into 3D fields for language-conditioned grasping, placing, and zero-shot rearrangement [58], [59]. More structured world models, such as Imagination Policy [60] and RoboEXP [61], further use 3D fields and scene structure for downstream planning. 

Overall, 3D representation-based planning enables rich spatial reasoning and language grounding, but depends heavily on accurate scene reconstruction and can degrade in dynamic, 

5 


Fig. 5. Overview of the taxonomy of learning-based Low-Level Action Modeling. It is organized into three components: Input Modeling, which specifies how multimodal inputs are represented and utilized; Latent Learning, which learns intermediate representations; and Policy Learning, which maps them to executable actions. Representative learning paradigms include reinforcement learning, imitation learning, and learning with auxiliary tasks. 

cluttered, or partially observed environments. Moreover, these representations provide structured guidance rather than executable actions, and therefore still require downstream planning or control modules. 

## III. LOW-LEVEL ACTION MODELING 

Low-Level Action Modeling concerns how observations and task specifications are transformed into executable actions, thereby grounding high-level reasoning in physical execution. Unlike High-Level Planning, which produces structured guidance, this layer outputs motion commands or action sequences that can be executed by downstream controllers. For representative vision-language-action models, this process can be written as 


where _o_ denotes observations, _l_ denotes task specifications, and _A_ plan is optional. More broadly, this formulation also applies to a wider family of learning-based action models beyond VLA systems. Following the learning pipeline of this layer, as shown in Figure 5, we organize the literature into three components: input modeling, latent learning, and policy learning. Together, these components provide a unified perspective on how learning-based action models couple perception, intermediate representation, and action generation. 

## _A. Learning Strategies_ 

Learning Strategies describe how supervision, feedback, and optimization signals are used to acquire manipulation policies. Rather than specifying what is perceived or how actions are parameterized, they determine how experience is converted into executable behavior, thereby affecting data efficiency, generalization, and robustness. Existing methods mainly differ in the extent to which they rely on environmental interaction, expert demonstrations, or auxiliary training objectives. As shown in Figure 6, we group them into three categories: reinforcement learning (RL), imitation learning (IL), and learning with auxiliary tasks. 


Fig. 6. Comparison of learning paradigms for low-level robotic manipulation. RL optimizes policies through trial-and-error interaction using reward signals, IL learns direct policy mappings from expert demonstrations, and auxiliarytask learning shapes representations via self-supervised objectives such as world modeling and goal abstraction. 

_1) Reinforcement Learning:_ In robotic manipulation, RL is an important paradigm for acquiring complex control policies through trial-and-error interaction with the environment. This section briefly reviews RL-based methods for robotic manipulation and groups them into two broad classes: model-free and model-based approaches, depending on whether an explicit or learned dynamics model is used during learning. 

_a) Model-free Methods:_ Model-free reinforcement learning (RL) learns manipulation policies directly from interaction without relying on explicit environment models. Although broadly applicable to high-dimensional control, such methods are often limited by poor sample efficiency. Recent work therefore increasingly combines model-free RL with largescale pretraining and efficient post-training, using offline robotic data, pretrained policies, or reinforcement-learningbased adaptation to improve generalization and online refinement [85]–[87]. Overall, the role of model-free RL in robotic manipulation has gradually shifted from training task-specific policies from scratch toward scalable adaptation of pretrained generalist models. 

_b) Model-based Methods:_ Model-based reinforcement learning improves data efficiency by leveraging explicit or learned models of environment dynamics for imagination, planning, or gradient-based optimization. Representative directions include latent world models for imagined rollouts, planning-oriented methods that integrate learned dynamics into model-predictive control, and differentiable simulation frameworks that enable gradient-based policy refinement [88]–[91]. While these methods offer advantages in sample efficiency and interpretability, their effectiveness ultimately depends on model accuracy, which remains challenging in contact-rich and high-dimensional manipulation settings. 

_2) Imitation Learning:_ IL acquires manipulation behaviors from expert demonstrations, avoiding explicit reward design and reducing extensive trial-and-error interaction [92]. From early control-theoretic formulations to modern deep visuomotor policies, it has become a widely used paradigm for robotic manipulation. Recent approaches further benefit from large- 

6 

scale pretraining and foundation-model priors, improving multimodal perception, generalization, and transfer across tasks and embodiments [93]. 

_a) Imitation from Action:_ When expert state-action pairs are available, behavior cloning (BC) remains the most direct and widely used approach, learning policies that map observations to low-level actions [94], [95]. To improve long-horizon performance and robustness, recent methods often incorporate hierarchical structure, skill decomposition, pose-level action abstractions, or planner-guided supervision [96]–[98]. Beyond direct action cloning, some approaches instead infer the objectives underlying expert behavior through inverse or adversarial formulations, enabling policies to imitate demonstrations at the level of rewards, constraints, or state distributions [99], [100]. 

_b) Imitation from Observation (IfO):_ IfO removes action supervision and learns from state or visual trajectories alone, requiring the agent to infer executable behavior from observed transitions. Existing methods typically recover reward-like signals or objectives from observations, align demonstrations and agent behavior in learned representation spaces, or extract intermediate goals from videos for downstream control [101]– [103]. These approaches are particularly attractive when action labels are unavailable or difficult to transfer across embodiments, although the lack of direct action supervision often makes learning more ambiguous and challenging. 

_3) Learning with Auxiliary Tasks:_ Auxiliary-task learning enhances manipulation policies with additional self-supervised or weakly supervised objectives, providing structured learning signals beyond sparse task rewards or demonstrations. One major direction is _world modeling_ , where agents learn predictive representations of environment dynamics to support planning, control, or latent rollout-based optimization [104]– [106]. Another direction focuses on _goal extraction and representation shaping_ , transforming raw observations into compact and actionable abstractions such as masks, keypoints, waypoints, motion-centric representations, or language-grounded subgoals [107]–[110]. In addition, auxiliary objectives such as multimodal alignment and reconstruction-based pretraining help improve spatial and temporal consistency in learned representations [111]–[113]. Overall, these methods improve data efficiency and representation quality by converting weak or indirect supervision into more informative training signals. 

## _B. Input Modeling_ 

Input modeling defines how a robot perceives the world by specifying which sensory modalities are used and how they are encoded before policy learning. It includes the selection, alignment, and fusion of multimodal observations, such as vision, language, touch, and force, and transforms raw inputs into structured representations for control and decision making. Effective input modeling preserves essential spatial, temporal, and semantic information, providing a reliable perceptual foundation for robust manipulation across diverse tasks. 

_1) Vision–Action Models:_ Vision–Action models tightly couple visual perception with action generation, learning direct mappings from visual observations to motor commands. Rather than relying on explicit symbolic planning, these 

methods typically encode task-relevant information implicitly within end-to-end visuomotor policies. Recent advances have expanded this paradigm from early convolutional designs to transformer- and diffusion-based frameworks with improved temporal modeling and policy expressiveness. 

_a) 2D Vision as Input:_ Most Vision–Action models operate on 2D visual observations, typically RGB images from single or multi-view cameras [114]–[116]. Representative methods include diffusion-based policies such as Diffusion Policy [114], hierarchical extensions such as HDP [117], and transformer-based models such as HPT [115]. These methods have demonstrated strong scalability and empirical effectiveness, but they generally lack explicit geometric grounding. As a result, they may struggle with precise spatial reasoning, contact geometry, and robust occlusion handling in complex physical environments. 

_b) 3D Vision as Input:_ To address these limitations, a growing line of work incorporates explicit 3D visual information into Vision–Action models [118]–[120]. By lifting 2D observations into 3D scene representations, these methods align action generation more directly with scene geometry. Representative examples include RVT [118], which infers 3D action targets through multi-view transformations, GenDP [119], which conditions diffusion policies on reconstructed 3D semantic fields, and DP3 [120], which integrates point clouds into the policy input. Although these methods substantially improve spatial reasoning and execution accuracy, most remain primarily perception-driven and still lack strong semantic grounding, leaving generalization across openended goals and instructions an open challenge. 

_2) Vision-Language-Action Models:_ Recent advances in VLA models have established a unified paradigm for mapping multimodal perception to executable robotic behaviors. Unlike earlier vision-only or language-conditioned controllers, VLAs integrate semantic grounding, spatial reasoning, and sequential action generation within a single framework. As summarized in Figure 7, we organize existing methods by input modality (2D vs. 3D) and methodological orientation (model-oriented vs. model-agnostic), which together reveal the main design trends of modern VLA systems. 

_a) 2D Vision as Input:_ Most existing VLA models primarily rely on 2D RGB observations, sometimes combined with multi-view images, as their main perceptual input. Under this setting, methods can be broadly divided into modeloriented approaches and model-agnostic strategies. We first review the model-oriented approaches: 

**Non-LLM-based VLA.** Early VLA systems directly mapped visual observations and textual commands to actions through language-conditioned sequence models. RT-1 [121] introduced a transformer-based discretized action policy that scaled to thousands of demonstrations, enabling diverse manipulation skills. Subsequent work such as VIMA [123] and HULC [124] extended this paradigm to compositional instructions and multimodal imitation. While effective in relatively closed settings, these approaches remained limited in generalization. **LLM/VLM-based VLA.** The emergence of LLMs and VLMs has introduced substantially stronger semantic priors into VLA systems. RT-2 [15] co-trains web-scale vision-language data 

7 


Fig. 7. A taxonomy of VLA models organized along two dimensions, input modality (2D vs. 3D) and methodological orientation (model-oriented vs. modelagnostic), highlighting representative directions in architectural design, training, and inference. 

with robot trajectories, enabling improved semantic generalization and the transfer of web-scale knowledge to robotic control. RoboFlamingo [132] demonstrates the effectiveness of leveraging pretrained VLMs through lightweight action interfaces, whereas OpenVLA [16] scales end-to-end VLA training over diverse robot demonstrations. Building on these advances, _π_ 0 [23] and _π_ 0 _._ 5 [134] further improve robustness and generalization through stronger continuous action modeling and large-scale multimodal training. Despite this progress, a persistent gap remains between high-level semantic reasoning and precise continuous motor execution. 

**Latent Learning for VLA.** A parallel line of work introduces latent action spaces that compress task-relevant motion into compact intermediate representations. UniVLA [135] learns language-conditioned latent actions in visual feature space and decodes them into embodiment-specific controls. villaX [140] jointly learns vision-based latent actions and proprioceptive forward dynamics within a diffusion framework, while AgiBot-GO1 [139] inserts a latent-action planner between a vision-language backbone and low-level controllers. Collectively, these methods use latent actions to improve efficiency and transferability. 

**Action Quantization for VLA.** Another direction discretizes continuous trajectories into action tokens, reducing actionspace complexity and stabilizing training. VQ-VLA [142] and MiniVLA [143] learn quantized motor codebooks, while FAST [144] maps control signals into frequency-domain tokens. Such quantized interfaces help bridge high-level intent and continuous execution, although maintaining semantic consistency and avoiding codebook collapse remain challenging. 

**Dual- and Multi-System VLA.** Inspired by dual-process cognitive theories, recent work proposes VLA architectures that separate fast reactive control from slower deliberative reasoning. Typically, a lightweight policy handles low-latency execution, while a larger vision-language model performs higher-level planning, reasoning, or memory management. Representative examples include LCB [145], HiRT [148], RationalVLA [149], HiRobot [153], and OpenHelix [152], as well as multi-system extensions such as TriVLA [150] and G0 [151]. These architectures improve robustness and flexibility, but also introduce new challenges in arbitration, credit assignment, and cross-system consistency. 

Second, we consider _model-agnostic strategies_ , which improve training or inference without modifying the underlying policy architecture. 

**Inference-Time Optimization.** Methods such as RoboMonkey [154] and CronusVLA [155] refine action selection at inference through voting, sampling, or calibration strategies. These approaches are particularly attractive because they can improve robustness without retraining and can be readily applied across diverse VLA backbones. 

**Reinforcement Learning and Post-training.** Recent work explores interactive post-training of pretrained VLAs by introducing RL signals tailored to multimodal, long-horizon policies. SimpleVLA-RL [191] combines verifiable outcomebased rewards with group-level policy optimization, enabling stable refinement from sparse task feedback. VLA-RL [159] emphasizes large-scale rollout-based RL to better align pretrained action decoders with execution-level requirements in generalist manipulation. RIPT-VLA [160] formulates post- 

8 


Fig. 8. A structured overview of tactile-based action models. 

training as lightweight interaction, using rollout feedback to improve performance without relying on a critic. ConRFT [161] bridges offline imitation and online reinforcement learning through a consistency-based objective, reducing distribution shift during refinement. 

**Learning with Auxiliary Tasks.** Auxiliary-task designs introduce structured supervision beyond action prediction to enrich intermediate reasoning and decision making. Representative directions include chain-of-thought-style intermediate reasoning [165], [166], explicit subgoal extraction [167], [168], and reconstruction-based consistency objectives [4]. By making intermediate structures more explicit, these approaches can improve reasoning horizon and execution transparency. 

**Efficiency, Robustness, and Long-Horizon Generalization.** 

Another practical line of work focuses on making VLAs more deployable in real-world settings. Methods such as TinyVLA [175], VLA-Cache [177], and CEED-VLA [158] improve efficiency through lightweight design, adaptive computation, or parallel decoding, while other approaches improve robustness through safety alignment, failure awareness, or perturbation defense [178]–[180]. Long-VLA [181] further targets long-horizon and compositional manipulation by improving temporal consistency and memory. Together, these efforts reflect a shift from single-step policy prediction toward stable and reliable long-horizon deployment. 

_b) 3D Vision as Input:_ Compared with 2D observations, 3D representations provide richer spatial grounding for contact-rich manipulation and long-horizon planning. Since most vision-language backbones are pretrained on large-scale 2D image-text corpora and lack intrinsic 3D understanding, increasing effort has gone into equipping VLA systems with explicit 3D perception. Existing methods can be broadly grouped into _model-oriented_ approaches, which directly incorporate 3D information into the policy architecture, and _model-agnostic_ strategies, which improve 3D VLAs without modifying the backbone. 

**3D Embedding and Fusion.** A primary model-oriented direction augments VLAs with explicit 3D embeddings, such as point clouds, depth maps, or voxel grids, and fuses them with 2D vision-language features. SpatialVLA [182] and GeoVLA [183] improve spatial precision through 3D positional or point-based geometric embeddings, while FP3 [184] and RoboMM [185] explore large-scale 3D training and multimodal pretraining with explicit 3D inputs. Overall, these methods improve spatial awareness and robustness, though often at higher data and computation cost. 

**Spatial Alignment.** Another line of work addresses occlusion and viewpoint ambiguity through explicit spatial alignment 

and multi-view reasoning. BridgeVLA [186] improves geometric consistency under partial visibility by aligning point clouds across viewpoints via cross-view heatmap prediction. **3D Reasoning and Prediction.** A third direction incorporates explicit 3D reasoning and predictive modeling to improve spatial understanding and long-horizon manipulation. 3DVLA [210] employs language-guided point-cloud diffusion to predict future scene states, while Evo-0 [187], ChainedDiffuser [188], and SGR [189] introduce complementary mechanisms for implicit spatial reasoning, joint keypose and trajectory prediction, and semantic-geometric representation learning, respectively. Together, these approaches enrich VLA policies with structured 3D priors that support more spatially grounded action generation and planning. 

**Model-Agnostic Strategies.** Compared with the growing model-oriented literature, model-agnostic enhancements for 3D VLAs remain relatively limited. Existing efforts mainly focus on inference-time view selection or feasibility filtering, as exemplified by TVVE [190], while more systematic advances in calibration, consensus decoding, caching, and post-training for 3D settings are still scarce. This makes efficient inference and adaptation for 3D VLAs an important open direction. 

Across both 2D and 3D modalities, recent VLA research is moving toward richer representations and more structured action generation. In 2D settings, this mainly appears through stronger LLM/VLM priors, latent abstractions, and multisystem reasoning, while 3D approaches emphasize spatial embeddings, alignment mechanisms, and explicit world models. Nevertheless, current VLA systems still face important challenges in robustness, efficiency, and generalization, especially under long-horizon tasks and real-world deployment. Promising directions include more standardized 3D representations, hybrid architectures that combine reactive control with deliberative planning, and joint training across 2D and 3D modalities. 

_3) Tactile-based Action Models:_ Tactile sensing provides fine-grained feedback on contact, geometry, and material properties, making it particularly important for precise and contactrich manipulation. Unlike vision, tactile signals directly reflect physical interaction and remain informative under occlusion, slippage, and uncertainty. Recent advances in tactile sensing and representation learning have therefore motivated a growing body of work that incorporates tactile feedback into action models to improve robustness, accuracy, and adaptability. We summarize this line of work in Figure 8. 

**Tactile Latent Learning.** A first line of work focuses on learning transferable tactile representations. CLTP [192] aligns tactile geometry with language through contrastive pretraining, 

9 

while Sparsh [193] learns generalizable tactile embeddings from large-scale self-supervised visuotactile data. 

**Tactile-Action Models.** Another direction directly incorporates tactile feedback into action generation. Representative examples include Feel the Force [194], which transfers contactforce patterns from human tactile-glove demonstrations to robot policies, Seq2Seq Imitation [195], which models tactile signals as temporal sequences, and RoboPack [196], which integrates tactile sensing into learned dynamics for MPC. **Tactile-Vision-Action Models.** A growing body of work studies visuotactile fusion for robotic manipulation. Representative methods such as T-DEX [198], RotateIt [199], and Multimodal-SeeThrough [200] combine vision and touch to improve dexterous manipulation and imitation learning, while VTTB [201] and VITaL [202] show the value of joint visuotactile pretraining. Reactive Diffusion Policy [203] further demonstrates responsive contact-rich control with a slow–fast visuotactile diffusion architecture. 

**Tactile-Language-Action Models.** Several recent works align tactile perception with natural language. TLA [204] learns tactile-language-action mappings from sequential tactile signals, while Octopi [205] uses tactile-language modeling to reason about object properties beyond visual appearance. **Tactile-Vision-Language-Action Models.** More recently, tactile sensing has been incorporated into full VLA pipelines. Tactile-VLA [206] extends VLA models with tactile inputs to improve physical interaction, VTLA [207] combines vision and touch with language-conditioned preference learning for robust insertion, and Touch Begins [208] adopts a two-stage strategy that uses vision-language models for localization and tactile feedback for execution. 

_4) Extra Modalities as Input:_ Beyond vision and language, force and audio provide complementary physical cues that are valuable for contact-rich and partially observable manipulation. Research on force sensing has progressed from early imitation-learning approaches that jointly modeled motion and force [211] and bilateral teleoperation for position–force coordination [212] to more recent force-aware visuomotor policies and VLA extensions for physically grounded control [213], [214]. Audio provides a complementary sensing modality that captures contact events and state transitions often inaccessible to vision, supporting manipulation under occlusion [215], feedback for hidden interactions [216], audiovisual imitation from in-the-wild demonstrations [217], and audio-enhanced VLA models [218]. Together, these modalities enrich action models with physically informative signals and improve robustness in real-world manipulation. 

## _C. Latent Learning_ 

Latent learning examines how robotic models can acquire robust and generalizable representations from input data, and how these representations can be effectively leveraged by the policy head to decode actions. We categorize existing work into two directions: pretrained latent learning, which focuses on learning high-quality representations for downstream tasks, and latent action learning, which addresses not only representation learning but also how to optimize the decoding of these representations into actions. We summarize these in Figure 9. 

_1) Pretrained Latent Learning:_ Learning transferable visual representations, often referred to as robotic representations, is an important foundation for robust real-world visuomotor control. Inspired by the success of large-scale pre-training in computer vision [219] and natural language processing [220], recent robotics research increasingly relies on pre-training visual encoders on diverse, domain-relevant data. Depending on the data source, these representations can be broadly grouped into three categories: models trained on general-purpose image datasets ( _e.g._ , ImageNet [221]), human–object interaction datasets that provide rich manipulation priors ( _e.g._ , Ego4D [222]), and robot-centric datasets collected from embodied interaction ( _e.g._ , BridgeData V2 [223]). **Training on General Datasets.** General-purpose visual pretraining offers a scalable alternative to robot-specific data collection. Parisi _et al._ [224] show that multi-layer feature fusion from vision models pre-trained on large image datasets can provide strong control-oriented representations, in some cases rivaling state-based inputs. Theia [225] further distills multiple vision foundation models into a compact and transferable representation for downstream robot learning. 

**Training on Human Egocentric Datasets.** Human egocentric video provides rich priors on object interaction, hand motion, and task structure, making it a valuable source for transferable robotic representations. VC-1 [226] and R3M [111] show that large-scale egocentric pre-training can yield general visual backbones and support few-shot real-robot learning, while Voltron [227] and HRP [228] further incorporate language grounding and affordance priors to improve higher-level semantics and cross-embodiment generalization. Together, these works highlight the value of egocentric pre-training for bridging human demonstrations and robot manipulation. 

**Training on Robotic Datasets.** The growing availability of large-scale robot-collected datasets has enabled representation learning directly grounded in embodied interaction. MVP [229] uses masked visual pre-training on diverse inthe-wild videos to learn transferable visual representations. Premier-TACO [230] further improves multitask representations through temporally contrastive objectives for better few-shot policy learning. More recently, manipulation-centric analysis [231] explicitly aligns visual representations with downstream manipulation performance through large-scale robotic pre-training. 

_2) Latent Action Learning:_ Recent advances in latent action learning connect video representation and world modeling, enabling robots to acquire action abstractions beyond explicit supervision. Dual-system and latent-learning approaches for VLAs, as discussed in Section III-B2, also fall into this category. Broadly, latent actions can be grouped into two forms: discrete representations, typically learned through quantization, and continuous vector representations. We review these two classes below. 

_a) Discretization and Vector Quantization:_ These methods convert continuous actions or representations into discrete tokens, yielding compact and reusable action primitives that simplify policy learning and improve stability. Early work such as ILPO [232] and LAPO [233] inferred latent action structure from observation-only demonstrations via inverse 

10 


Fig. 9. Overview of latent learning. **Top left** : Robotic encoders are pretrained on general datasets, human egocentric datasets, and robotic datasets to produce latent representations for downstream policies. **Bottom left** : In a dual-system architecture, System 2 outputs latent features to guide System 1 in action generation. **Right** : Latent action learning can be implemented using either discretized latents through Vector Quantization (VQ, yellow) or continuous latents (pink). Representative modules include Inverse Dynamics Models (IDM), Forward Dynamics Models (FDM), and Diffusion Transformers (DiT). 

dynamics. Later methods discretized continuous control into latent tokens for efficient generative control and scalable multitask learning [234]–[236]. More recent approaches combine discretized latent actions with vision–language models: LAPA [237] learns latent actions from visual transitions, while DreamGen [238] scales this paradigm using video world models and inverse dynamics to synthesize large robotic datasets. Overall, this line trades fine-grained continuity for compositionality, robustness, and scalability. 

_b) Continuous Latent Action Representations:_ Continuous latent action representations encode actions as vectors in a continuous space, providing a compact interface between perception and control. By abstracting low-level motor commands into smooth latent trajectories, these methods support interpolation, generalization, and transfer across behaviors, embodiments, and task contexts. 

**Latent Dynamics Representations.** A first line of work represents task-relevant dynamics as latent variables that condition action generation. MimicPlay [239] predicts latent actions from goal images derived from human play for long-horizon imitation, CLAM [240] learns continuous latent actions from unlabeled demonstrations with robust motor alignment, and CoMo [241] scales latent motion embeddings from internet videos to improve cross-domain generalization. 

**Implicit World Modeling.** Another class exploits latent predictions from learned world models to guide control. VPP [242] adapts a video foundation model for manipulation and aggregates predicted visual latents to condition a diffusion policy. FLARE [243] aligns future latent predictions with implicit world models to improve generalization from human demonstrations, while Genie Envisioner [244] enforces consistency between video-diffusion latents and action-diffusion policies, strengthening prediction–control coupling. **Latent Diffusion Policies.** Several approaches integrate con- 

tinuous latent spaces into diffusion-based control. LAD [245] trains diffusion policies in a shared latent action space for cross-embodiment transfer, while LaDi-WM [246] learns a latent diffusion world model whose predicted semantics and geometry condition downstream action generation. 

**Koopman-based Latent Dynamics.** Koopman-based methods learn linear latent dynamics that approximate nonlinear manipulation processes. KoDex [247] studies Koopman representations for dexterous manipulation, KOROL [248] learns interpretable object-centric latents through Koopman rollouts for stable and explainable control, and KOAP [249] combines Koopman-based control with diffusion planning for longhorizon execution. 

**Goal- and Instruction-conditioned Latents.** Some methods jointly encode observations and instructions into task-centric latent actions. Procedure Cloning [250] introduces latent procedural abstractions inspired by chain-of-thought reasoning for long-horizon tasks, while UniVLA [135] learns task-centric latent actions from cross-embodiment data in an unsupervised manner, enabling VLA prediction without action labels. 

## _D. Policy Learning_ 

Policy learning specifies how learned representations are decoded into executable robot actions, defining the functional interface between perception, internal representations, and motor execution. 

_1) MLP-based Policy:_ Early learning-based manipulation policies adopt multilayer perceptrons (MLPs) to directly map encoded observations to actions, serving as simple and efficient visuomotor controllers when paired with strong representations [111], [229]. 

_2) Transformer-based Policy:_ Transformer-based policies use self- and cross-attention to model temporal dependencies and multimodal context, enabling sequence-to-sequence 

11 

action generation from variable-length histories. Within this paradigm, ACT [251] introduced action chunking to reduce error accumulation and stabilize bimanual manipulation, with later extensions scaling skills and incorporating richer supervision [129], [252]. In parallel, autoregressive policies treat manipulation as next-token prediction over action sequences, supporting in-context imitation and long-horizon reasoning, as exemplified by ICRT [253] and CARP [254]. 

_3) Diffusion Policy (DP):_ DP formulates action generation as an iterative denoising process, enabling multimodal trajectory synthesis and strong generalization in robotic manipulation [114]. Recent extensions improve this paradigm along several directions: 3D-aware variants enhance spatial grounding for contact-rich and long-horizon manipulation [120]; mixture-of-experts and equivariant architectures improve multitask generalization by encoding task structure and symmetry priors [255], [256]; and integration with video prediction and world modeling supports planning-oriented and data-efficient learning [257]. These advances make diffusion policy a flexible and extensible paradigm for modern robot manipulation. 

_4) Flow Matching (FM) Policy:_ FM policies replace stochastic denoising with deterministic transport dynamics, yielding faster inference and smoother action trajectories. Early work demonstrated FM as a stable and efficient alternative to diffusion for imitation learning [258]. Building on this foundation, RTC [259] enables real-time execution by overlapping action generation with ongoing control, further improving efficiency and temporal consistency. 

_5) Other Policy Paradigms:_ Beyond the above families, alternative designs explore different inductive biases. Statespace-model-based policies leverage long-sequence modeling for efficient control [260], while frequency-domain policies encode actions spectrally to improve long-horizon stability [261]. These approaches highlight complementary directions for structuring action generation. 

Across these paradigms, policy learning has evolved from direct regression toward structured sequence generation that models uncertainty, temporal dependencies, and long-horizon coherence. MLP- and Transformer-based policies emphasize representation decoding and context aggregation, while diffusion and flow-based methods treat action generation as a generative process over trajectories, improving robustness and multimodality. Together, these advances point toward policies that more tightly integrate perception, memory, and planning for scalable robotic manipulation. 

## IV. PROSPECTIVE FUTURE RESEARCH DIRECTIONS 

As discussed in Sections II and III, and summarized in Table I, foundation-model-based manipulation systems have advanced in semantic reasoning, task decomposition, and action generation. However, most approaches remain constrained by narrow task and embodiment coverage, limited sensory and action interfaces, and insufficient real-world robustness. Future research should therefore address four tightly coupled challenges: building a general robot brain that generalizes across tasks and embodiments, collecting diverse large-scale data, enabling richer multimodal interaction beyond vision- 

dominant perception, and ensuring safety and collaboration in open-world environments. 

## _A. Core Challenge 1: Building a True Robot Brain_ 

A central long-term goal of robotic foundation models is to move beyond task-specific fitting toward a true “robot brain” that can generalize across tasks, objects, environments, and embodiments. While recent large-scale VLA systems and policy learning approaches have shown promising progress, most existing results are still obtained under relatively controlled variations, such as adapting to new object instances within familiar task families, recombining known task primitives, or handling moderate environmental changes [138], [272]. These settings are closer to interpolation than true extrapolation. 

A true robot brain, however, should support stronger forms of generalization, including robust transfer to unseen task structures, object categories, and substantially different environments, as well as more compositional and adaptive behavior under novelty. Achieving this capability requires more than scaling current policies within narrow benchmarks. It instead calls for general-purpose architectures that support flexible modality and embodiment interfaces and scale effectively with data and compute [17], [134]; stronger generalization and adaptation through continual and lifelong learning, memory, replay, and efficient representation updates [273]; and more reliable long-horizon execution through tighter coupling between high-level planning and low-level closed-loop control [181]. Together, these directions point toward robotic systems that acquire reusable structure for flexible open-world manipulation, rather than merely performing well within fixed distributions. 

## _B. Core Challenge 2: Data and Evaluation Bottlenecks_ 

Despite recent progress, current robotic foundation models still rely heavily on data-driven fitting. As summarized in Table II, existing benchmarks evaluate different aspects of robot manipulation. CALVIN emphasizes long-horizon languageconditioned execution but has limited environment diversity and a fixed embodiment; LIBERO focuses on multi-task and lifelong learning but uses a fixed embodiment and limited out-of-distribution settings; SimplerEnv evaluates real-to-sim consistency rather than real-world performance. Other benchmarks mainly target low-level control, offline imitation learning, large-scale task diversity, or language-guided reasoning, each with corresponding limitations in scene, embodiment, horizon, or interaction complexity. Benchmark scores should therefore be interpreted with respect to the capabilities and constraints of the specific evaluation setting, rather than as universal measures of robotic intelligence. In addition, the lack of standardized evaluation protocols hinders fair comparison across works. This challenge is compounded by the scarcity and cost of real-world manipulation data and the limited fidelity of current simulators for contact-rich, articulated, and deformable interactions. Future progress therefore requires more reproducible evaluation frameworks [274], scalable “data flywheels” for autonomous experience collection and high-value data extraction [275], and higher-fidelity differentiable simulators for policy optimization and sim-to-real transfer [276]. 

12 

TABLE I 

SUMMARY OF MAJOR FOUNDATION-MODEL-BASED ROBOTIC MANIPULATION METHODS ACROSS HIGH-LEVEL PLANNING AND LOW-LEVEL ACTION MODELING. FOR EACH CATEGORY, WE SUMMARIZE A REPRESENTATIVE METHOD, ITS CORE IDEA, MODALITIES, DATA REGIME, ADVANTAGES AND USE CASES, AND LIMITATIONS, HIGHLIGHTING THE CAPABILITY BOUNDARIES AND CHARACTERISTIC FAILURE MODES OF DIFFERENT APPROACHES. 

|**Type**<br>**Category**|**Representative**<br>**Method**|**Core Idea**|**Modalities**|**Training Data Regime**|**Advantages & Use**<br>**Cases**|**Limitations**|
|---|---|---|---|---|---|---|
|LLM-based<br>Task Planning<br>(Section II-A)|SayCan<br>[18]|LLM-planned global reasoning<br>with affordance-grounded<br>feasibility|RGB images,<br>language|(I) 68K robot demos; (II) 12K<br>successful autonomous robot<br>trajectories|Strong semantic<br>reasoning and task<br>decomposition|High cost; may<br>violate physical<br>constraints|
|r<br>MLLM-based<br>Task Planning<br>(Section II-B)|PaLM-E<br>[19]|Embodied multimodal LLM for<br>end-to-end task reasoning|RGB image, state<br>estimation,<br>language|(I) Large-scale language data; (II)<br>Internet-scale vision-language data;<br>(III) Real robot demos|Unified perception and<br>reasoning; positive<br>transfer across tasks|High cost; may lose<br>language capabilities|
|vel Planne<br>Code Generation<br>(Section II-C)|Code as<br>Policies<br>[20]|LLM generates executable code;<br>calls perception and control APIs|language,<br>perception API,<br>control primitives|No training data|Unsafe or invalid code<br>may be generated||
|High-le<br>Geometric<br>Constraint-based<br>Planning<br>(Section II-D)|VoxPoser<br>[22]|Builds 3D value maps from<br>language-vision for smooth motion|RGB images,<br>language, 3D voxel<br>maps|No training data|Strong physical<br>grounding|Relies on predefined<br>geometry; limited<br>semantics|
|Affordance<br>Learning<br>(Section II-E)|CLIPort<br>[21]|Decouples semantics and<br>localization: CLIP grounding,<br>Transporter pick-and-place|RGB images,<br>language|Simulated robot demos|Action-centric<br>interaction|Affordance ambiguity<br>in cluttered or novel<br>scenes|
|3D<br>Representations<br>as Planner<br>(Section II-F)|F3RM<br>[58]|Distills CLIP into 3D fields for<br>language-based pick-and-place|RGB images,<br>language, 3D<br>geometry|10 robot demos across 5 tasks|Rich spatial reasoning|Sensitive to<br>reconstruction errors<br>and dynamics|
|2D<br>Non-LLM-based<br>VLA<br>(Section III-B2a)|RT-1<br>[121]|Transformer maps vision and<br>language to actions; discretization<br>enables low-level control|RGB images,<br>language|130K robot demos across 744 tasks<br>from 13 robots|Demonstration<br>scalability and diverse<br>manipulation skills|Weak semantic<br>priors; limited<br>generalization and<br>cross-domain transfer|
|2D<br>LLM/VLM-based<br>VLA<br>(Section III-B2a)|OpenVLA<br>[16]|Fine-tunes Prismatic VLM on robot<br>data; fuses SigLIP and DINOv2<br>with discrete action tokens|RGB images,<br>language|970K real robot demos curated from<br>the Open X-Embodiment dataset|Strong language<br>grounding and<br>scalability|Action discretization<br>limits precision|
|Latent Learning<br>for VLA<br>(Section III-B2a)|LAPA<br>[237]|Learns discrete latent actions via<br>VQ-VAE; VLM predicts latent<br>actions|RGB images,<br>language|(I) 220K action-free human<br>manipulation videos; (II) robot demos<br>from BridgeData, Open<br>X-Embodiment; (III) 100 robot<br>trajectories in SIMPLER|Efficient and<br>transferable latent<br>action abstractions|Inference latency|
|n Modeling<br>Action<br>Quantization<br>for VLA<br>(Section III-B2a)|MiniVLA<br>[143]|Learns quantized motor codebooks;<br>trajectory discretization for stable<br>training|RGB images,<br>language|(I) Real robot demos from Open<br>X-Embodiment; (II) robot demos from<br>LIBERO-90 and BridgeData|Reduced complexity<br>and stabilized training|Difficulty in semantic<br>consistency and<br>collapse avoidance|
|w-level Actio<br>Dual-/Multi-<br>system VLA<br>(Section III-B2a)|OpenHelix<br>[152]|Dual-system VLA: frozen MLLM<br>and pre-trained policy; separates<br>fast reactive control and slow<br>deliberative reasoning|language, 3D scene<br>representation,<br>RGB,<br>proprioception|Robot demos from CALVIN|Efficient real-time<br>control|Limited high-level<br>reasoning|
|Lo<br>Learning with<br>Auxiliary Tasks<br>(Section III-B2a)|_π_0_._5<br>[134]|Hierarchical inference with subtask<br>prediction; flow matching action<br>generation|RGB images,<br>language,<br>proprioception|(I) Real mobile manipulator demos in<br>homes; (II) multi-environment robot<br>trajectories; (III) vision-language data|Continuous action<br>modeling with smooth<br>trajectories|Higher computational<br>cost|
|Reinforcement<br>Learning<br>(Section III-B2a)|VLA-RL<br>[159]|Large-scale rollout RL refinement,<br>multi-turn conversation<br>formulation; PPO with robotic<br>reward densification|RGB images,<br>language,<br>proprioception|(I) Robot demos for 40 LIBERO tasks;<br>(II) online simulation trajectories<br>collected with RL; (III) segmented<br>trajectories with automatically<br>generated process rewards|Scalable refinement<br>from sparse feedback<br>and execution-aligned<br>action decoder|Extensive online<br>interaction and critic<br>dependence|
|Efficient VLA<br>(Section III-B2a)|VLA-Adapter<br>[174]|Parameter-efficient adapters;<br>all-layer latents and bridge<br>attention for efficient action<br>generation|RGB images,<br>language,<br>proprioception|Robot demos from LIBERO and<br>CALVIN|Parameter-efficient<br>adaptation|Strongly depends on<br>backbone quality|
|Robustness<br>(Section III-B2a)|BadVLA<br>[179]|Objective-decoupled backdoor<br>attacks; reveals VLA security<br>vulnerabilities|RGB images,<br>language|(I) Robot demos from LIBERO and<br>SimplerEnv; (II) poisoned robot<br>trajectories with visual or multimodal<br>triggers|Systematic backdoor<br>vulnerability analysis|Limited to<br>training-time<br>injection|
|3D VLA<br>(Section III-B2b)|SpatialVLA<br>[182]|Introduces 3D positional encodings<br>and adaptive action grids to capture<br>transferable spatial priors|3D point clouds or<br>depth, RGB,<br>language|1.1M real robot demos from multiple<br>datasets|Improved 3D spatial<br>reasoning|Depends on accurate<br>scene reconstruction|


## _C. Core Challenge 3: Multimodal Physical Interaction_ 

Vision-centric manipulation alone is insufficient for realworld physical intelligence. As summarized in Section III-B, existing action models can incorporate additional modalities such as language, tactile signals, and audio [206]. However, unlike humans, who adaptively integrate multiple sensory cues during task execution, most current models support only one extra modality beyond vision and language, making unified multimodal perception and action difficult to achieve. Future robotic foundation models should therefore fuse richer sensory streams, such as touch, audio, and thermal signals, into uni- 

fied, adaptive, and temporally coherent representations despite heterogeneous sampling rates and noise characteristics. 

Beyond multimodal input modeling, robotic manipulation also requires stronger physical interaction capabilities. A major frontier is the manipulation of complex materials, such as cloth, cables, fluids, and granular media [277], where state spaces are effectively high-dimensional and contact dynamics dominate. Progress in this direction will likely require new object representations, such as graph- or field-based models [113], [278], together with stronger physics-informed inference and learning algorithms that remain stable under partial observability and uncertain contact. 

13 

TABLE II 

SUMMARY OF REPRESENTATIVE ROBOT MANIPULATION SIMULATORS AND BENCHMARKS. HERE, DEMOS DENOTE THE NUMBER OF DEMONSTRATIONS. 

|**Name**|**Simulator**|**Objects**|**Tasks**|**Data Scale**|**Robot**|**Evaluation Scope**|**Main Limitation**|
|---|---|---|---|---|---|---|---|
|MetaWorld [262]|MuJoCo|80|50|2.5K demos|Sawyer|Multi-task reinforcement learning and<br>policy generalization|State-based single-arm manipulation<br>only|
|RLBench [263]|CoppeliaSim|28|100|2.7K demos|Franka Panda|Vision-based multi-task manipulation|Waypoint-based demonstrations simplify<br>execution|
|CALVIN [264]|PyBullet|28|34|40M frames|Franka Panda|Long-horizon language-conditioned<br>manipulation|Limited environment diversity|
|Robomimic [265]|MuJoCo|15|8|6K demos|Franka Panda|Offline imitation learning|Limited task diversity and data scale|
|LIBERO [266]|MuJoCo|67|130|6.5K demos|Franka Panda|Lifelong and multi-task learning|Limited embodiment and<br>out-of-distribution coverage|
|RoboCasa [267]|MuJoCo|2509|100|100K+<br>demos|Franka Panda, Fourier<br>GR1, Tiago, etc.|Large-scale household manipulation|Limited scene diversity|
|SimplerEnv [268]|SAPIEN|16|10|140K+<br>demos|Google Robot, WidowX|Real-to-sim evaluation of VLA policies|Limited scene and task diversity|
|RoboTwin [269]|SAPIEN|731|50|25K demos|ALOHA, UR5, Franka,<br>ARX-X5|Cross-embodiment manipulation|Limited long-horizon evaluation|
|ManiSkill3 [270]|SAPIEN|10K+|12|1M frames|Franka Panda, Unitree<br>H1, AnyMAL-C etc.|Large-scale general manipulation|Limited language-conditioned evaluation|
|VLABench [271]|MuJoCo|2K+|100|5K demos|Franka Panda|Language-guided reasoning and<br>manipulation|Limited contact-rich manipulation|


## _D. Core Challenge 4: Safety and Collaboration_ 

As robots enter human environments, safety must be treated as a first-class design constraint rather than a secondary feature. As discussed in Section III-B2a, existing research has begun to address safety-related issues such as failure prediction, backdoor attacks, and language-instruction interference [178]–[180]. However, future robotic foundation models will require stronger guarantees at multiple levels. At the single-robot level, they should provide intrinsic safety through self-constrained control that respects kinematic and dynamic limits while regulating smoothness, force, and energy in real time [149]. At the multi-robot level, they should support safe collaboration through predictive coordination and shared protocols. For real-world deployment, safety must also be paired with autonomy in fault detection and recovery, including continuous monitoring and reliable fallback policies [279]. More broadly, practical systems will likely rely on hybrid paradigms that combine the adaptability of learning-based models with the stability of classical methods, such as rulebased logic or MPC [280], especially in safety-critical settings. 

## V. CONCLUSION 

This survey has reviewed recent progress in robot manipulation through a unified perspective on high-level planning, learning-based low-level action modeling, and future research directions. By organizing existing methods along planning and learning dimensions, we aim to clarify the algorithmic structure of modern robotic manipulation systems. Despite substantial progress, the field remains far from achieving robust and general-purpose capability. Key challenges include building unified architectures that couple perception, reasoning, and control, overcoming data, evaluation, and perception bottlenecks that limit scalability and generalization, and ensuring safety and reliability in open-world human environments. Addressing these challenges will be critical for moving beyond specialized manipulation pipelines toward more adaptive and trustworthy robotic foundation models. We hope this abstraction-driven survey provides a useful reference for understanding current methods and framing future research in robot manipulation. 

## REFERENCES 

- [1] H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux, T. Lacroix, B. Rozi`ere, N. Goyal, E. Hambro, F. Azhar _et al._ , “Llama: Open and efficient foundation language models,” _arXiv preprint arXiv:2302.13971_ , 2023. 

- [2] H. Liu, C. Li, Q. Wu, and Y. J. Lee, “Visual instruction tuning,” _Advances in neural information processing systems_ , vol. 36, pp. 34 892– 34 916, 2023. 

- [3] S. Bai, W. Song, J. Chen, Y. Ji, Z. Zhong, J. Yang, H. Zhao, W. Zhou, W. Zhao, Z. Li _et al._ , “Towards a unified understanding of robot manipulation: A comprehensive survey,” _arXiv preprint arXiv:2510.10903_ , 2025. 

- [4] W. Song, Z. Zhou, H. Zhao, J. Chen, P. Ding, H. Yan, Y. Huang, F. Tang, D. Wang, and H. Li, “Reconvla: Reconstructive visionlanguage-action model as effective robot perceiver,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 22, 2026, pp. 18 549–18 557. 

- [5] A. Nagabandi, K. Konolige, S. Levine, and V. Kumar, “Deep dynamics models for learning dexterous manipulation,” in _Conference on robot learning_ . PMLR, 2020, pp. 1101–1112. 

- [6] F. Luan, S. Meng, Z. Wang, Y. Dong, Y. Zhou, B. He _et al._ , “Learning efficient robotic garment manipulation with standardization,” in _Fortysecond International Conference on Machine Learning_ , 2025. 

- [7] J. Wu, W. Chong, R. Holmberg, A. Prasad, Y. Gao, O. Khatib, S. Song, S. Rusinkiewicz, and J. Bohg, “Tidybot++: An open-source holonomic mobile manipulator for robot learning,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 3729–3741. 

- [8] D. Hou, C. Zhu, Z. Zhang, Z. Li, C. Guo, and Y. Liu, “Efficient learning of a unified policy for whole-body manipulation and locomotion skills,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 5455–5461. 

- [9] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 2828–2844. 

- [10] S. Levine, C. Finn, T. Darrell, and P. Abbeel, “End-to-end training of deep visuomotor policies,” _Journal of Machine Learning Research_ , vol. 17, no. 39, pp. 1–40, 2016. 

- [11] L. Pinto and A. Gupta, “Supersizing self-supervision: Learning to grasp from 50k tries and 700 robot hours,” in _2016 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2016, pp. 3406–3413. 

- [12] Y. Yang, H. Yu, X. Lou, Y. Liu, and C. Choi, “Attribute-based robotic grasping with data-efficient adaptation,” _IEEE Transactions on Robotics_ , vol. 40, pp. 1566–1579, 2024. 

- [13] Y. Duan, M. Andrychowicz, B. Stadie, O. Jonathan Ho, J. Schneider, I. Sutskever, P. Abbeel, and W. Zaremba, “One-shot imitation learning,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [14] A. Rajeswaran, V. Kumar, A. Gupta, G. Vezzani, J. Schulman, E. Todorov, and S. Levine, “Learning complex dexterous manipulation with deep reinforcement learning and demonstrations,” in _Robotics: Science and Systems_ , 2018. 

- [15] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models 

14 

- transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [16] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong _et al._ , “Openvla: An open-source vision-language-action model,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 2679–2713. 

- [17] Y. Ji, H. Tan, J. Shi, X. Hao, Y. Zhang, H. Zhang, P. Wang, M. Zhao, Y. Mu, P. An _et al._ , “Robobrain: A unified brain model for robotic manipulation from abstract to concrete,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 1724–1734. 

- [18] A. Brohan, Y. Chebotar, C. Finn, K. Hausman, A. Herzog, D. Ho, J. Ibarz, A. Irpan, E. Jang, R. Julian _et al._ , “Do as i can, not as i say: Grounding language in robotic affordances,” in _Conference on robot learning_ . PMLR, 2023, pp. 287–318. 

- [19] D. Driess, F. Xia, M. S. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu _et al._ , “Palm-e: An embodied multimodal language model,” in _International Conference on Machine Learning_ . PMLR, 2023, pp. 8469–8488. 

- [20] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence, and A. Zeng, “Code as policies: Language model programs for embodied control,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 9493–9500. 

- [21] M. Shridhar, L. Manuelli, and D. Fox, “Cliport: What and where pathways for robotic manipulation,” in _Conference on robot learning_ . PMLR, 2022, pp. 894–906. 

- [22] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “Voxposer: Composable 3d value maps for robotic manipulation with language models,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 540– 562. 

- [23] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_<sup>0</sup> : A vision-languageaction flow model for general robot control,” in _Robotics: Science and Systems_ , 2025. 

- [24] Y. Ma, Z. Song, Y. Zhuang, J. Hao, and I. King, “A survey on vision-language-action models for embodied ai,” _arXiv preprint arXiv:2405.14093_ , 2024. 

- [25] Y. Zhong, F. Bai, S. Cai, X. Huang, Z. Chen, X. Zhang, Y. Wang, S. Guo, T. Guan, K. N. Lui _et al._ , “A survey on vision-languageaction models: An action tokenization perspective,” _arXiv preprint arXiv:2507.01925_ , 2025. 

- [26] T.-Y. Xiang, A.-Q. Jin, X.-H. Zhou, M.-J. Gui, X.-L. Xie, S.-Q. Liu, S.-Y. Wang, S.-B. Duan, F.-C. Xie, W.-K. Wang _et al._ , “Parallels between vla model post-training and human motor learning: Progress, challenges, and trends,” _arXiv preprint arXiv:2506.20966_ , 2025. 

- [27] R. P. Wolf, Y. Shi, S. Liu, and R. Rayyes, “Diffusion models for robotic manipulation: A survey,” _Frontiers in Robotics and AI_ , vol. 12, p. 1606247, 2025. 

- [28] K. Zhang, P. Yun, J. Cen, J. Cai, D. Zhu, H. Yuan, C. Zhao, T. Feng, M. Y. Wang, Q. Chen _et al._ , “Generative artificial intelligence in robotic manipulation: A survey,” _arXiv preprint arXiv:2503.03464_ , 2025. 

- [29] W. Huang, F. Xia, D. Shah, D. Driess, A. Zeng, Y. Lu, P. Florence, I. Mordatch, S. Levine, K. Hausman _et al._ , “Grounded decoding: Guiding text generation with grounded models for embodied agents,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 59 636–59 661, 2023. 

- [30] C. H. Song, J. Wu, C. Washington, B. M. Sadler, W.-L. Chao, and Y. Su, “Llm-planner: Few-shot grounded planning for embodied agents with large language models,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2023, pp. 2998–3009. 

- [31] B. Liu, Y. Jiang, X. Zhang, Q. Liu, S. Zhang, J. Biswas, and P. Stone, “Llm+ p: Empowering large language models with optimal planning proficiency,” _arXiv preprint arXiv:2304.11477_ , 2023. 

- [32] Z. Liu, A. Bahety, and S. Song, “Reflect: Summarizing robot experiences for failure explanation and correction,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 3468–3484. 

- [33] H. Singh, R. J. Das, M. Han, P. Nakov, and I. Laptev, “Malmm: Multiagent large language models for zero-shot robotics manipulation,” _arXiv preprint arXiv:2411.17636_ , 2024. 

- [34] T. Wang, H. Lin, J. Yu, and Y. Fu, “Polaris: Open-ended interactive robotic manipulation via syn2real visual grounding and large language models,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 9676–9683. 

- [35] Y. Hu, F. Lin, T. Zhang, L. Yi, and Y. Gao, “Look before you leap: Unveiling the power of gpt-4v in robotic vision-language planning,” in _First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024_ , 2024. 

- [36] J. Gao, B. Sarkar, F. Xia, T. Xiao, J. Wu, B. Ichter, A. Majumdar, and D. Sadigh, “Physically grounded vision-language models for robotic manipulation,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 12 462–12 469. 

- [37] Y. Mu, Q. Zhang, M. Hu, W. Wang, M. Ding, J. Jin, B. Wang, J. Dai, Y. Qiao, and P. Luo, “Embodiedgpt: Vision-language pre-training via embodied chain of thought,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 25 081–25 094, 2023. 

- [38] G. R. Team, S. Abeyruwan, J. Ainslie, J.-B. Alayrac, M. G. Arenas, T. Armstrong, A. Balakrishna, R. Baruch, M. Bauza, M. Blokzijl _et al._ , “Gemini robotics: Bringing ai into the physical world,” _arXiv preprint arXiv:2503.20020_ , 2025. 

- [39] I. Singh, V. Blukis, A. Mousavian, A. Goyal, D. Xu, J. Tremblay, D. Fox, J. Thomason, and A. Garg, “Progprompt: Generating situated robot task plans using large language models,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 11 523–11 530. 

- [40] Y. Wang, G. Gonzalez-Pumariega, Y. Sharma, and S. Choudhury, “Demo2code: From summarizing demonstrations to synthesizing code via extended chain-of-thought,” in _Advances in Neural Information Processing Systems_ , vol. 36, 2023, pp. 14 848–14 956. 

- [41] M. Murray, A. Gupta, and M. Cakmak, “Teaching robots with show and tell: Using foundation models to synthesize robot policies from language and visual demonstration,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [42] T. Yoneda, J. Fang, P. Li, H. Zhang, T. Jiang, S. Lin, B. Picker, D. Yunis, H. Mei, and M. R. Walter, “Statler: State-maintaining language models for embodied reasoning,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 15 083–15 091. 

- [43] H. Huang, F. Lin, Y. Hu, S. Wang, and Y. Gao, “Copa: General robotic manipulation through spatial constraints of parts with foundation models,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 9488–9495. 

- [44] W. Huang, C. Wang, Y. Li, R. Zhang, and L. Fei-Fei, “Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 4573–4602. 

- [45] W. Tang, J.-H. Pan, Y.-H. Liu, M. Tomizuka, L. E. Li, C.-W. Fu, and M. Ding, “Geomanip: Geometric constraints as general interfaces for robot manipulation,” _arXiv preprint arXiv:2501.09783_ , 2025. 

- [46] Z. Jiang, C.-C. Hsu, and Y. Zhu, “Ditto: Building digital twins of articulated objects from interaction,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2022, pp. 5616–5626. 

- [47] H. Geng, H. Xu, C. Zhao, C. Xu, L. Yi, S. Huang, and H. Wang, “Gapartnet: Cross-category domain-generalizable object perception and manipulation via generalizable and actionable parts,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 7081–7091. 

- [48] W. Liu, J. Mao, J. Hsu, T. Hermans, A. Garg, and J. Wu, “Composable part-based manipulation,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 1300–1315. 

- [49] A. Zeng, P. Florence, J. Tompson, S. Welker, J. Chien, M. Attarian, T. Armstrong, I. Krasin, D. Duong, V. Sindhwani _et al._ , “Transporter networks: Rearranging the visual world for robotic manipulation,” in _Conference on Robot Learning_ . PMLR, 2021, pp. 726–747. 

- [50] J. Borja-Diaz, O. Mees, G. Kalweit, L. Hermann, J. Boedecker, and W. Burgard, “Affordance learning from play for sample-efficient policy learning,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022, pp. 6372–6378. 

- [51] M. Lopes, F. S. Melo, and L. Montesano, “Affordance-based imitation learning in robots,” in _2007 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, 2007, pp. 1015–1021. 

- [52] W. Yuan, J. Duan, V. Blukis, W. Pumacay, R. Krishna, A. Murali, A. Mousavian, and D. Fox, “Robopoint: A vision-language model for spatial affordance prediction in robotics,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 4005–4020. 

- [53] F. Liu, K. Fang, P. Abbeel, and S. Levine, “Moka: Open-world robotic manipulation through mark-based visual prompting,” in _Robotics: Science and Systems_ , 2024. 

- [54] X. Li, M. Zhang, Y. Geng, H. Geng, Y. Long, Y. Shen, R. Zhang, J. Liu, and H. Dong, “Manipllm: Embodied multimodal large language model for object-centric robotic manipulation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 18 061–18 070. 

15 

- [55] Y. Sheng, R. Lin, L. Wang, Q. Qiu, Y. Zhang, Y. Zhang, B. Hua, and J. Ji, “Msgfield: A unified scene representation integrating motion, semantics, and geometry for robotic manipulation,” _arXiv preprint arXiv:2410.15730_ , 2024. 

- [56] S. Yang, W. Yu, J. Zeng, J. Lv, K. Ren, C. Lu, D. Lin, and J. Pang, “Novel demonstration generation with gaussian splatting enables robust one-shot manipulation,” in _Robotics: Science and Systems_ , 2025. 

- [57] A. Simeonov, Y. Du, A. Tagliasacchi, J. B. Tenenbaum, A. Rodriguez, P. Agrawal, and V. Sitzmann, “Neural descriptor fields: Se (3)equivariant object representations for manipulation,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022, pp. 6394–6400. 

- [58] W. Shen, G. Yang, A. Yu, J. Wong, L. P. Kaelbling, and P. Isola, “Distilled feature fields enable few-shot language-guided manipulation,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 405–424. 

- [59] Y. Wang, M. Zhang, Z. Li, T. Kelestemur, K. R. Driggs-Campbell, J. Wu, L. Fei-Fei, and Y. Li, “D<sup>3</sup> fields: Dynamic 3d descriptor fields for zero-shot generalizable rearrangement,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 272–298. 

- [60] H. Huang, K. Schmeckpeper, D. Wang, O. Biza, Y. Qian, H. Liu, M. Jia, R. Platt, and R. Walters, “Imagination policy: Using generative point cloud models for learning manipulation policies,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 5150–5165. 

- [61] H. Jiang, B. Huang, R. Wu, Z. Li, S. Garg, H. Nayyeri, S. Wang, and Y. Li, “Roboexp: Action-conditioned scene graph via interactive exploration for robotic manipulation,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 3027–3052. 

- [62] D.-A. Huang, D. Xu, Y. Zhu, A. Garg, S. Savarese, L. Fei-Fei, and J. C. Niebles, “Continuous relaxation of symbolic planner for oneshot imitation learning,” in _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2019, pp. 2635– 2642. 

- [63] W. Huang, F. Xia, T. Xiao, H. Chan, J. Liang, P. Florence, A. Zeng, J. Tompson, I. Mordatch, Y. Chebotar _et al._ , “Inner monologue: Embodied reasoning through planning with language models,” _arXiv preprint arXiv:2207.05608_ , 2022. 

- [64] X. Zhao, M. Li, C. Weber, M. B. Hafez, and S. Wermter, “Chat with the environment: Interactive multimodal perception using large language models,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2023, pp. 3590–3596. 

- [65] Z. Mandi, S. Jain, and S. Song, “Roco: Dialectic multi-robot collaboration with large language models,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 286–299. 

- [66] J. Li, D. Li, S. Savarese, and S. Hoi, “Blip-2: Bootstrapping languageimage pre-training with frozen image encoders and large language models,” in _International conference on machine learning_ . PMLR, 2023, pp. 19 730–19 742. 

- [67] K. Zhang, Z.-H. Yin, W. Ye, and Y. Gao, “Learning manipulation skills through robot chain-of-thought with sparse failure guidance,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 8012–8018. 

- [68] Z. Qi, W. Zhang, Y. Ding, R. Dong, X. Yu, J. Li, L. Xu, B. Li, X. He, G. Fan _et al._ , “Sofar: Language-grounded orientation bridges spatial reasoning and object manipulation,” _Advances in neural information processing systems_ , vol. 38, pp. 76 367–76 412, 2025. 

- [69] A. Zeng, M. Attarian, K. M. Choromanski, A. Wong, S. Welker, F. Tombari, A. Purohit, M. S. Ryoo, V. Sindhwani, J. Lee _et al._ , “Socratic models: Composing zero-shot multimodal reasoning with language,” in _The Eleventh International Conference on Learning Representations_ , 2023. 

- [70] J. Duan, W. Pumacay, N. Kumar, Y. R. Wang, S. Tian, W. Yuan, R. Krishna, D. Fox, A. Mandlekar, and Y. Guo, “Aha: A visionlanguage-model for detecting and reasoning over failures in robotic manipulation,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [71] R. Dang, Y. Yuan, Y. Mao, K. Li, J. Liu, Z. Wang, X. Li, F. Wang, and D. Zhao, “Rynnec: Bringing mllms into embodied world,” _arXiv preprint arXiv:2508.14160_ , 2025. 

- [72] S. G. Venkatesh, R. Upadrashta, and B. Amrutur, “Translating natural language instructions to computer programs for robot manipulation,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2021, pp. 1919–1926. 

- [73] S. Huang, Z. Jiang, H. Dong, Y. Qiao, P. Gao, and H. Li, “Instruct2act: Mapping multi-modality instructions to robotic actions with large language model,” _arXiv preprint arXiv:2305.11176_ , 2023. 

- [74] Y. Liu, Z. Liang, Z. Chen, T. Chen, M. Hu, W. Dong, C. Xu, Z. Han, Y. Qin, and Y. Mu, “Hycodepolicy: Hybrid language controllers for multimodal monitoring and decision in embodied agents,” _arXiv preprint arXiv:2508.02629_ , 2025. 

- [75] J. J. Gibson, “The theory of affordances:(1979),” in _The people, place, and space reader_ . Routledge, 2014, pp. 56–60. 

- [76] Y. Yin, Z. Han, S. Aarya, J. Wang, S. Xu, J. Peng, A. Wang, A. Yuille, and T. Shu, “Partinstruct: Part-level instruction following for finegrained robot manipulation,” in _Robotics: Science and Systems_ , 2025. 

- [77] H. Geng, S. Wei, C. Deng, B. Shen, H. Wang, and L. Guibas, “Sage: Bridging semantic and actionable parts for generalizable manipulation of articulated objects,” in _Robotics: Science and Systems_ , 2024. 

- [78] B. Chen, Z. Xu, S. Kirmani, B. Ichter, D. Sadigh, L. Guibas, and F. Xia, “Spatialvlm: Endowing vision-language models with spatial reasoning capabilities,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 14 455–14 465. 

- [79] Y. Tang, W. Huang, Y. Wang, C. Li, R. Yuan, R. Zhang, J. Wu, and L. Fei-Fei, “Uad: Unsupervised affordance distillation for generalization in robotic manipulation,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [80] Y. Kuang, J. Ye, H. Geng, J. Mao, C. Deng, L. Guibas, H. Wang, and Y. Wang, “Ram: Retrieval-based affordance transfer for generalizable zero-shot robotic manipulation,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 547–565. 

- [81] O. Shorinwa, J. Tucker, A. Smith, A. Swann, T. Chen, R. Firoozi, M. D. Kennedy, and M. Schwager, “Splat-mover: Multi-stage, openvocabulary robotic manipulation via editable gaussian splatting,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 4748–4770. 

- [82] Y. Li and D. Pathak, “Object-aware gaussian splatting for robotic manipulation,” in _ICRA 2024 Workshop on 3D Visual Representations for Robot Manipulation_ , 2024. 

- [83] J. Abou-Chakra, K. Rana, F. Dayoub, and N. Suenderhauf, “Physically embodied gaussian splatting: A visually learnt and physically grounded 3d representation for robotics,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 513–530. 

- [84] A. Simeonov, Y. Du, Y.-C. Lin, A. R. Garcia, L. P. Kaelbling, T. Lozano-P´erez, and P. Agrawal, “Se (3)-equivariant relational rearrangement with neural descriptor fields,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 835–846. 

- [85] D. Kalashnikov, A. Irpan, P. Pastor, J. Ibarz, A. Herzog, E. Jang, D. Quillen, E. Holly, M. Kalakrishnan, V. Vanhoucke _et al._ , “Scalable deep reinforcement learning for vision-based robotic manipulation,” in _Conference on robot learning_ . PMLR, 2018, pp. 651–673. 

- [86] A. Kumar, A. Singh, F. Ebert, M. Nakamoto, Y. Yang, C. Finn, and S. Levine, “Pre-training for robots: Offline rl enables learning new tasks from a handful of trials,” _arXiv preprint arXiv:2210.05178_ , 2022. 

- [87] Y. Guo, J. Zhang, X. Chen, X. Ji, Y.-J. Wang, Y. Hu, and J. Chen, “Improving vision-language-action model with online reinforcement learning,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 15 665–15 672. 

- [88] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” in _International Conference on Learning Representations_ , 2020. 

- [89] P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg, “Daydreamer: World models for physical robot learning,” in _Conference on robot learning_ . PMLR, 2023, pp. 2226–2240. 

- [90] N. A. Hansen, H. Su, and X. Wang, “Temporal difference learning for model predictive control,” in _International Conference on Machine Learning_ . PMLR, 2022, pp. 8387–8406. 

- [91] E. Xing, V. Luk, and J. Oh, “Stabilizing reinforcement learning in differentiable multiphysics simulation,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [92] S. Schaal, “Is imitation learning the route to humanoid robots?” _Trends in cognitive sciences_ , vol. 3, no. 6, pp. 233–242, 1999. 

- [93] M. Dalal, A. Mandlekar, C. R. Garrett, A. Handa, R. Salakhutdinov, and D. Fox, “Imitating task and motion planning with visuomotor transformers,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2565–2593. 

- [94] Y. Huang, L. Rozo, J. Silv´erio, and D. G. Caldwell, “Non-parametric imitation learning of robot motor skills,” in _2019 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2019, pp. 5266– 5272. 

- [95] S. Bai, W. Zhou, P. Ding, W. Zhao, D. Wang, and B. Chen, “Rethinking latent redundancy in behavior cloning: An information bottleneck approach for robot manipulation,” in _Forty-second International Conference on Machine Learning_ , 2025. 

16 

- [96] G. Katz, D.-W. Huang, R. Gentili, and J. Reggia, “Imitation learning as cause-effect reasoning,” in _International Conference on Artificial General Intelligence_ . Springer, 2016, pp. 64–73. 

- [97] H. Sun, Y. Wang, Z. Zhou, S. Wang, H. Yang, J. Sun, and Q. Cao, “Exploring pose-guided imitation learning for robotic precise insertion,” _arXiv preprint arXiv:2505.09424_ , 2025. 

- [98] M. J. McDonald and D. Hadfield-Menell, “Guided imitation of task and motion planning,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 630–640. 

- [99] P. Englert, N. A. Vien, and M. Toussaint, “Inverse kkt: Learning cost functions of manipulation tasks from demonstrations,” _The International Journal of Robotics Research_ , vol. 36, no. 13-14, pp. 1474–1488, 2017. 

- [100] J. Ho and S. Ermon, “Generative adversarial imitation learning,” _Advances in neural information processing systems_ , vol. 29, 2016. 

- [101] M. Alakuijala, G. Dulac-Arnold, J. Mairal, J. Ponce, and C. Schmid, “Learning reward functions for robotic manipulation by observing humans,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 5006–5012. 

- [102] Y. J. Ma, S. Sodhani, D. Jayaraman, O. Bastani, V. Kumar, and A. Zhang, “Vip: Towards universal visual reward and representation via value-implicit pre-training,” in _The Eleventh International Conference on Learning Representations_ , 2023. 

- [103] S. Haldar and L. Pinto, “Point policy: Unifying observations and actions with key points for robot manipulation,” in _Conference on Robot Learning_ , 2025. 

- [104] W. Zhao, J. Chen, Z. Meng, D. Mao, R. Song, and W. Zhang, “Vlmpc: Vision-language model predictive control for robotic manipulation,” in _Robotics: Science and Systems_ , 2024. 

- [105] G. Lu, S. Zhang, Z. Wang, C. Liu, J. Lu, and Y. Tang, “Manigaussian: Dynamic gaussian splatting for multi-task robotic manipulation,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 349– 366. 

- [106] Y. Du, S. Yang, P. Florence, F. Xia, A. Wahid, P. Sermanet, T. Yu, P. Abbeel, J. B. Tenenbaum, L. P. Kaelbling _et al._ , “Video language planning,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [107] J. Gao, Z. Tao, N. Jaquier, and T. Asfour, “K-vil: Keypoints-based visual imitation learning,” _IEEE Transactions on Robotics_ , vol. 39, no. 5, pp. 3888–3908, 2023. 

- [108] L. X. Shi, A. Sharma, T. Z. Zhao, and C. Finn, “Waypoint-based imitation learning for robotic manipulation,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2195–2209. 

- [109] H. Bharadhwaj, R. Mottaghi, A. Gupta, and S. Tulsiani, “Track2act: Predicting point tracks from internet videos enables generalizable robot manipulation,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 306–324. 

- [110] Z. Jia, V. Thumuluri, F. Liu, L. Chen, Z. Huang, and H. Su, “Chainof-thought predictive control,” in _International Conference on Machine Learning_ . PMLR, 2024, pp. 21 768–21 790. 

- [111] S. Nair, A. Rajeswaran, V. Kumar, C. Finn, and A. Gupta, “R3m: A universal visual representation for robot manipulation,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 892–909. 

- [112] T. Xiao, I. Radosavovic, T. Darrell, and J. Malik, “Masked visual pretraining for motor control,” _arXiv:2203.06173_ , 2022. 

- [113] Y. Ze, G. Yan, Y.-H. Wu, A. Macaluso, Y. Ge, J. Ye, N. Hansen, L. E. Li, and X. Wang, “Gnfactor: Multi-task real robot learning with generalizable neural feature fields,” in _Conference on robot learning_ . PMLR, 2023, pp. 284–301. 

- [114] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Robotics: Science and Systems XIX_ , 2023. 

- [115] L. Wang, X. Chen, J. Zhao, and K. He, “Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers,” in _Advances in neural information processing systems_ , vol. 37, 2024, pp. 124 420– 124 450. 

- [116] A. Prasad, K. Lin, J. Wu, L. Zhou, and J. Bohg, “Consistency policy: Accelerated visuomotor policies via consistency distillation,” in _Robotics: Science and Systems_ , 2024. 

- [117] D. Wang, C. Liu, F. Chang, and Y. Xu, “Hierarchical diffusion policy: manipulation trajectory generation via contact guidance,” _IEEE Transactions on Robotics_ , 2025. 

- [118] A. Goyal, J. Xu, Y. Guo, V. Blukis, Y.-W. Chao, and D. Fox, “Rvt: Robotic view transformer for 3d object manipulation,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 694–710. 

- [119] Y. Wang, G. Yin, B. Huang, T. Kelestemur, J. Wang, and Y. Li, “Gendp: 3d semantic fields for category-level generalizable diffusion policy,” in _8th Annual Conference on Robot Learning_ , vol. 2, 2024. 

- [120] Y. Ze, G. Zhang, K. Zhang, C. Hu, M. Wang, and H. Xu, “3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations,” in _Robotics: Science and Systems_ , 2024. 

- [121] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” in _Robotics: Science and Systems_ , 2023. 

- [122] D. Ghosh, H. R. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, J. Luo _et al._ , “Octo: An open-source generalist robot policy,” in _Robotics: Science and Systems_ , 2024. 

- [123] Y. Jiang, A. Gupta, Z. Zhang, G. Wang, Y. Dou, Y. Chen, L. FeiFei, A. Anandkumar, Y. Zhu, and L. Fan, “Vima: General robot manipulation with multimodal prompts,” in _International Conference on Machine Learning_ , 2023. 

- [124] O. Mees, L. Hermann, and W. Burgard, “What matters in language conditioned robotic imitation learning over unstructured data,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 4, pp. 11 205–11 212, 2022. 

- [125] S. Wang, S. Liu, W. Wang, J. Shan, and B. Fang, “Robobert: An end-to-end multimodal robotic manipulation model,” _arXiv preprint arXiv:2502.07837_ , 2025. 

- [126] Z. Hou, T. Zhang, Y. Xiong, H. Duan, H. Pu, R. Tong, C. Zhao, X. Zhu, Y. Qiao, J. Dai _et al._ , “Dita: Scaling diffusion transformer for generalist vision-language-action policy,” in _International Conference on Computer Vision (ICCV)_ , 2025. 

- [127] H. Huang, F. Liu, L. Fu, T. Wu, M. Mukadam, J. Malik, K. Goldberg, and P. Abbeel, “Otter: A vision-language-action model with text-aware visual feature extraction,” in _International Conference on Machine Learning_ , 2025. 

- [128] H. Huang, X. Chen, Y. Chen, H. Li, X. Han, Z. Wang, T. Wang, J. Pang, and Z. Zhao, “Roboground: Robotic manipulation with grounded vision-language priors,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 22 540–22 550. 

- [129] S. Haldar, Z. Peng, and L. Pinto, “Baku: An efficient transformer for multi-task policy learning,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 141 208–141 239, 2024. 

- [130] M. Reuss, O.<sup>¨</sup> E. Ya˘gmurlu, F. Wenzel, and R. Lioutikov, “Multimodal diffusion transformer: Learning versatile behavior from multimodal goals,” in _Robotics: Science and Systems_ , 2024. 

- [131] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong, “Unleashing large-scale video generative pre-training for visual robot manipulation,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [132] X. Li, M. Liu, H. Zhang, C. Yu, J. Xu, H. Wu, C. Cheang, Y. Jing, W. Zhang, H. Liu _et al._ , “Vision-language foundation models as effective robot imitators,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [133] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-language-action models: Optimizing speed and success,” in _Robotics: Science and Systems_ , 2025. 

- [134] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai _et al._ , “ _π_ 0 _._ 5: a visionlanguage-action model with open-world generalization,” in _Conference on Robot Learning_ , 2025. 

- [135] Q. Bu, Y. Yang, J. Cai, S. Gao, G. Ren, M. Yao, P. Luo, and H. Li, “Univla: Learning to act anywhere with task-centric latent actions,” in _Robotics: Science and Systems_ , 2025. 

- [136] J. Wen, Y. Zhu, J. Li, Z. Tang, C. Shen, and F. Feng, “Dexvla: Visionlanguage model with plug-in diffusion expert for general robot control,” in _Conference on Robot Learning_ , 2025. 

- [137] Q. Li, Y. Liang, Z. Wang, L. Luo, X. Chen, M. Liao, F. Wei, Y. Deng, S. Xu, Y. Zhang _et al._ , “Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation,” _arXiv preprint arXiv:2411.19650_ , 2024. 

- [138] J. Wen, M. Zhu, Y. Zhu, Z. Tang, J. Li, Z. Zhou, C. Li, X. Liu, Y. Peng, C. Shen _et al._ , “Diffusion-vla: Generalizable and interpretable robot foundation model via self-generated reasoning,” in _International Conference on Machine Learning_ , 2025. 

- [139] Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Hu, X. Huang _et al._ , “Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025. 

17 

- [140] X. Chen, H. Wei, P. Zhang, C. Zhang, K. Wang, Y. Guo, R. Yang, Y. Wang, X. Xiao, L. Zhao _et al._ , “Villa-x: enhancing latent action modeling in vision-language-action models,” in _International Conference on Learning Representations_ , vol. 2026, 2026, pp. 70 673–70 703. 

- [141] S. Bai, J. Lyu, W. Zhou, Z. Li, D. Wang, L. Xing, X. Zhao, P. Wang, Z. Wang, C. Chi, B. Chen, and S. Zhang, “Latent reasoning vla: Latent thinking and prediction for vision-language-action models,” in _Fortythird International Conference on Machine Learning_ , 2026. 

- [142] Y. Wang, H. Zhu, M. Liu, J. Yang, H.-S. Fang, and T. He, “Vq-vla: Improving vision-language-action models via scaling vector-quantized action tokenizers,” in _2025 IEEE/CVF International Conference on Computer Vision (ICCV)_ . IEEE, 2025, pp. 11 089–11 099. 

- [143] S. Belkhale and D. Sadigh, “Minivla: A better vla with a smaller footprint,” 2024. 

- [144] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “Fast: Efficient action tokenization for vision-language-action models,” _arXiv preprint arXiv:2501.09747_ , 2025. 

- [145] Y. Shentu, P. Wu, A. Rajeswaran, and P. Abbeel, “From llms to actions: Latent codes as bridges in hierarchical robot control,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 8539–8546. 

- [146] K. Zhang, P. Ren, B. Lin, J. Lin, S. Ma, H. Xu, and X. Liang, “Pivot-r: Primitive-driven waypoint-aware world model for robotic manipulation,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 54 105–54 136, 2024. 

- [147] Q. Bu, H. Li, L. Chen, J. Cai, J. Zeng, H. Cui, M. Yao, and Y. Qiao, “Towards synergistic, generalized, and efficient dual-system for robotic manipulation,” _arXiv preprint arXiv:2410.08001_ , 2024. 

- [148] J. Zhang, Y. Guo, X. Chen, Y.-J. Wang, Y. Hu, C. Shi, and J. Chen, “Hirt: Enhancing robotic control with hierarchical robot transformers,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 933–946. 

- [149] W. Song, J. Chen, W. Li, X. He, X. Zheng, Z. Liu, H. Wang, and H. Li, “A dual-system vision-language-action model for rational manipulation,” _IEEE/ASME Transactions on Mechatronics_ , 2026. 

- [150] Z. Liu, Y. Gu, S. Zheng, X. Xue, and Y. Fu, “Trivla: A unified triplesystem-based unified vision-language-action model for general robot control,” _arXiv preprint arXiv:2507.01424_ , 2025. 

- [151] T. Jiang, T. Yuan, Y. Liu, C. Lu, J. Cui, X. Liu, S. Cheng, J. Gao, H. Xu, and H. Zhao, “Galaxea open-world dataset and g0 dual-system vla model,” _arXiv preprint arXiv:2509.00576_ , 2025. 

- [152] C. Cui, P. Ding, W. Song, S. Bai, X. Tong, Z. Ge, R. Suo, W. Zhou, Y. Liu, B. Jia _et al._ , “Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation,” _arXiv preprint arXiv:2505.03912_ , 2025. 

- [153] L. X. Shi, B. Ichter, M. Equi, L. Ke, K. Pertsch, Q. Vuong, J. Tanner, A. Walling, H. Wang, N. Fusai _et al._ , “Hi robot: Open-ended instruction following with hierarchical vision-language-action models,” in _International Conference on Machine Learning_ , 2025. 

- [154] J. Kwok, C. Agia, R. Sinha, M. Foutter, S. Li, I. Stoica, A. Mirhoseini, and M. Pavone, “Robomonkey: Scaling test-time sampling and verification for vision-language-action models,” in _Conference on Robot Learning_ , 2025. 

- [155] H. Li, S. Yang, Y. Chen, Y. Tian, X. Yang, X. Chen, H. Wang, T. Wang, F. Zhao, D. Lin _et al._ , “Cronusvla: Transferring latent motion across time for multi-frame prediction in manipulation,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2026. 

- [156] T. Zhang, H. Duan, H. Hao, Y. Qiao, J. Dai, and Z. Hou, “Grounding actions in camera space: Observation-centric vision-language-action policy,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 22, 2026, pp. 18 782–18 790. 

- [157] W. Song, J. Chen, P. Ding, H. Zhao, W. Zhao, Z. Zhong, Z. Ge, Z. Li, D. Wang, L. Wang _et al._ , “Pd-vla: Accelerating vision-language-action model integrated with action chunking via parallel decoding,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 13 162–13 169. 

- [158] W. Song, J. Chen, P. Ding, Y. Huang, H. Zhao, D. Wang, and H. Li, “Ceed-vla: Consistency vision-language-action model with early-exit decoding,” in _European Conference on Computer Vision_ , 2026. 

- [159] G. Lu, W. Guo, C. Zhang, Y. Zhou, H. Jiang, Z. Gao, Y. Tang, and Z. Wang, “Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning,” _arXiv preprint arXiv:2505.18719_ , 2025. 

- [160] S. Tan, K. Dou, Y. Zhao, and P. Kraehenbuehl, “Interactive post-training for vision-language-action models,” in _Workshop on Foundation Models Meet Embodied Agents at CVPR 2025_ , 2025. 

- [161] Y. Chen, S. Tian, S. Liu, Y. Zhou, H. Li, and D. Zhao, “Conrft: A reinforced fine-tuning method for vla models via consistency policy,” in _Robotics: Science and Systems_ , 2025. 

- [162] C.-P. Huang, Y.-H. Wu, M.-H. Chen, Y.-C. F. Wang, and F.-E. Yang, “Thinkact: Vision-language-action reasoning via reinforced visual latent planning,” in _Advances in Neural Information Processing Systems_ , 2025. 

- [163] M. Nakamoto, O. Mees, A. Kumar, and S. Levine, “Steering your generalists: Improving robotic foundation models via value guidance,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 4996–5013. 

- [164] Y. Chen and X. Li, “Rlrc: Reinforcement learning-based recovery for compressed vision-language-action models,” _arXiv preprint arXiv:2506.17639_ , 2025. 

- [165] M. Zawalski, W. Chen, K. Pertsch, O. Mees, C. Finn, and S. Levine, “Robotic control via embodied chain-of-thought reasoning,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 3157–3181. 

- [166] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn _et al._ , “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 1702–1713. 

- [167] R. Zheng, Y. Liang, S. Huang, J. Gao, H. Daum´e III, A. Kolobov, F. Huang, and J. Yang, “Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [168] Y. Tian, S. Yang, J. Zeng, P. Wang, D. Lin, H. Dong, and J. Pang, “Predictive inverse dynamics models are scalable learners for robotic manipulation,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [169] Z. Zhong, H. Yan, J. Li, X. Liu, X. Gong, W. Song, J. Chen, and H. Li, “Flowvla: Thinking in motion with a visual chain of thought,” _arXiv preprint arXiv:2508.18269_ , 2025. 

- [170] S. Deng, M. Yan, S. Wei, H. Ma, Y. Yang, J. Chen, Z. Zhang, T. Yang, X. Zhang, W. Zhang _et al._ , “Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data,” in _Conference on Robot Learning_ , 2025. 

- [171] J. Zhang, Y. Guo, Y. Hu, X. Chen, X. Zhu, and J. Chen, “Up-vla: A unified understanding and prediction model for embodied agent,” in _International Conference on Machine Learning_ , 2025. 

- [172] S. Belkhale, T. Ding, T. Xiao, P. Sermanet, Q. Vuong, J. Tompson, Y. Chebotar, D. Dwibedi, and D. Sadigh, “Rt-h: Action hierarchies using language,” _Robotics: Science and Systems_ , 2024. 

- [173] D. Niu, Y. Sharma, G. Biamby, J. Quenum, Y. Bai, B. Shi, T. Darrell, and R. Herzig, “Llarva: Vision-action instruction tuning enhances robot learning,” in _Conference on Robot Learning_ , 2024. 

- [174] Y. Wang, P. Ding, L. Li, C. Cui, Z. Ge, X. Tong, W. Song, H. Zhao, W. Zhao, P. Hou _et al._ , “Vla-adapter: An effective paradigm for tiny-scale vision-language-action model,” in _Proceedings of the AAAI conference on artificial intelligence_ , vol. 40, no. 22, 2026, pp. 18 638– 18 646. 

- [175] J. Wen, Y. Zhu, J. Li, M. Zhu, Z. Tang, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen _et al._ , “Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [176] Y. Yang, Y. Wang, Z. Wen, L. Zhongwei, C. Zou, Z. Zhang, C. Wen, and L. Zhang, “Efficientvla: Training-free acceleration and compression for vision-language-action models,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 40 891–40 914, 2025. 

- [177] S. Xu, Y. Wang, C. Xia, D. Zhu, T. Huang, and C. Xu, “Vlacache: Efficient vision-language-action manipulation via adaptive token caching,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 164 448–164 473, 2025. 

- [178] Q. Gu, Y. Ju, S. Sun, I. Gilitschenski, H. Nishimura, M. Itkina, and F. Shkurti, “Safe: Multitask failure detection for vision-language-action models,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 40 041–40 076, 2025. 

- [179] X. Zhou, G. Tie, G. Zhang, H. Wang, P. Zhou, and L. Sun, “Badvla: Towards backdoor attacks on vision-language-action models via objective-decoupled optimization,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 127 496–127 523, 2025. 

- [180] C. Xu, T. K. Nguyen, E. Dixon, C. Rodriguez, P. Miller, R. Lee, P. Shah, R. Ambrus, H. Nishimura, and M. Itkina, “Can we detect failures without failure data? uncertainty-aware runtime failure detection for imitation learning policies,” in _Robotics: Science and Systems_ , 2025. 

- [181] Y. Fan, P. Ding, S. Bai, X. Tong, Y. Zhu, H. Lu, F. Dai, W. Zhao, Y. Liu, S. Huang _et al._ , “Long-vla: Unleashing long-horizon capability 

18 

- of vision language action model for robot manipulation,” in _Conference on Robot Learning_ , 2025. 

- [182] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, Y. Ding, Z. Wang, J. Gu, B. Zhao, D. Wang _et al._ , “Spatialvla: Exploring spatial representations for visual-language-action model,” in _Robotics: Science and Systems_ , 2025. 

- [183] L. Sun, B. Xie, Y. Liu, H. Shi, T. Wang, and J. Cao, “Geovla: Empowering 3d representations in vision-language-action models,” _arXiv preprint arXiv:2508.09071_ , 2025. 

- [184] R. Yang, G. Chen, C. Wen, and Y. Gao, “Fp3: A 3d foundation policy for robotic manipulation,” _arXiv preprint arXiv:2503.08950_ , 2025. 

- [185] F. Yan, F. Liu, L. Zheng, Y. Zhong, Y. Huang, Z. Guan, C. Feng, and L. Ma, “Robomm: All-in-one multimodal large model for robotic manipulation,” in _International Conference on Computer Vision (ICCV)_ , 2025. 

- [186] P. Li, Y. Chen, H. Wu, X. Ma, X. Wu, Y. Huang, L. Wang, T. Kong, and T. Tan, “Bridgevla: Input-output alignment for efficient 3d manipulation learning with vision-language models,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 63 635–63 673, 2025. 

- [187] T. Lin, G. Li, Y. Zhong, Y. Zou, and B. Zhao, “Evo-0: Vision-languageaction model with implicit spatial understanding,” _arXiv preprint arXiv:2507.00416_ , 2025. 

- [188] Z. Xian and N. Gkanatsios, “Chaineddiffuser: Unifying trajectory diffusion and keypose prediction for robotic manipulation,” in _Conference on Robot Learning_ , 2023. 

- [189] T. Zhang, Y. Hu, H. Cui, H. Zhao, and Y. Gao, “A universal semanticgeometric representation for robotic manipulation,” in _Proceedings of the 7th Conference on Robot Learning (CoRL)_ , 2023, pp. 3342–3363. 

- [190] Y. Bai, Z. Wang, Y. Liu, W. Chen, Z. Chen, M. Dai, Y. Zheng, L. Liu, G. Li, and L. Lin, “Learning to see and act: Task-aware view planning for robotic manipulation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2026. 

- [191] H. Li, Y. Zuo, J. Yu, Y. Zhang, Z. Yang, K. Zhang, X. Zhu, Y. Zhang _et al._ , “Simplevla-rl: Scaling vla training via reinforcement learning,” in _Advances in Neural Information Processing Systems_ , 2025. 

- [192] W. Ma, X. Cao, Y. Zhang, C. Zhang, S. Yang, P. Hao, B. Fang, Y. Cai, S. Cui, and S. Wang, “Cltp: Contrastive language-tactile pre-training for 3d contact geometry understanding,” _Biomimetic Intelligence and Robotics_ , p. 100324, 2026. 

- [193] C. Higuera, A. Sharma, C. K. Bodduluri, T. Fan, P. Lancaster, M. Kalakrishnan, M. Kaess, B. Boots, M. Lambeta, T. Wu _et al._ , “Sparsh: Self-supervised touch representations for vision-based tactile sensing,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 885– 915. 

- [194] A. Adeniji, Z. Chen, V. Liu, V. Pattabiraman, R. Bhirangi, S. Haldar, P. Abbeel, and L. Pinto, “Feel the force: Contact-driven learning from humans,” _arXiv preprint arXiv:2506.01944_ , 2025. 

- [195] W. Yang, A. Angleraud, R. S. Pieters, J. Pajarinen, and J.-K. K¨am¨ar¨ainen, “Seq2seq imitation learning for tactile feedback-based manipulation,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 5829–5836. 

- [196] B. Ai, S. Tian, H. Shi, Y. Wang, C. Tan, Y. Li, and J. Wu, “Robopack: Learning tactile-informed dynamics models for dense packing,” _Proceedings of Robotics: Science and Systems_ , 2024. 

- [197] K. Yu, Y. Han, Q. Wang, V. Saxena, D. Xu, and Y. Zhao, “Mimictouch: Leveraging multi-modal human tactile demonstrations for contact-rich manipulation,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 4844–4865. 

- [198] I. Guzey, B. Evans, S. Chintala, and L. Pinto, “Dexterity from touch: Self-supervised pre-training of tactile representations with robotic play,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 3142– 3166. 

- [199] H. Qi, B. Yi, S. Suresh, M. Lambeta, Y. Ma, R. Calandra, and J. Malik, “General in-hand object rotation with vision and touch,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2549–2564. 

- [200] T. Ablett, O. Limoyo, A. Sigal, A. Jilani, J. Kelly, K. Siddiqi, F. Hogan, and G. Dudek, “Multimodal and force-matched imitation learning with a see-through visuotactile sensor,” _IEEE Transactions on Robotics_ , 2024. 

- [201] Y. Gu and Y. Demiris, “Vttb: A visuo-tactile learning approach for robot-assisted bed bathing,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 6, pp. 5751–5758, 2024. 

- [202] A. George, S. Gano, P. Katragadda, and A. B. Farimani, “Vital pretraining: Visuo-tactile pretraining for tactile and non-tactile manipulation policies,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 258–264. 

- [203] H. Xue, J. Ren, W. Chen, G. Zhang, Y. Fang, G. Gu, H. Xu, and C. Lu, “Reactive diffusion policy: Slow-fast visual-tactile policy learning for contact-rich manipulation,” in _Robotics: Science and Systems_ , 2025. 

- [204] P. Hao, C. Zhang, D. Li, X. Cao, X. Hao, S. Cui, and S. Wang, “Tla: Tactile-language-action model for contact-rich manipulation,” _arXiv preprint arXiv:2503.08548_ , 2025. 

- [205] S. Yu, K. Lin, A. Xiao, J. Duan, and H. Soh, “Octopi: Object property reasoning with large tactile-language models,” in _Robotics: Science and Systems_ , 2024. 

- [206] J. Huang, S. Wang, F. Lin, Y. Hu, C. Wen, and Y. Gao, “Tactilevla: Unlocking vision-language-action model’s physical knowledge for tactile generalization,” _arXiv preprint arXiv:2507.09160_ , 2025. 

- [207] C. Zhang, P. Hao, X. Cao, X. Hao, S. Cui, and S. Wang, “Vtla: Visiontactile-language-action model with preference learning for insertion manipulation,” _arXiv preprint arXiv:2505.09577_ , 2025. 

- [208] Z. Zhao, S. Haldar, J. Cui, and L. Pinto, “Touch begins where vision ends: Generalizable policies for contact-rich manipulation,” in _Second Workshop on Out-of-Distribution Generalization in Robotics at RSS 2025_ , 2025. 

- [209] J. Bi, K. Y. Ma, C. Hao, M. S. Zheng, and H. Soh, “Vla-touch: Enhancing vision-language-action model with dual-level tactile feedback,” _IEEE Robotics and Automation Letters_ , 2026. 

- [210] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3d-vla: a 3d vision-language-action generative world model,” in _Proceedings of the 41st International Conference on Machine Learning_ , 2024, pp. 61 229–61 245. 

- [211] P. Kormushev, S. Calinon, and D. G. Caldwell, “Imitation learning of positional and force skills demonstrated via kinesthetic teaching and haptic input,” _Advanced Robotics_ , vol. 25, no. 5, pp. 581–603, 2011. 

- [212] T. Adachi, K. Fujimoto, S. Sakaino, and T. Tsuji, “Imitation learning for object manipulation based on position/force information using bilateral control,” in _2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2018, pp. 3648–3653. 

- [213] Z. He, H. Fang, J. Chen, H.-S. Fang, and C. Lu, “Foar: Force-aware reactive policy for contact-rich robotic manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [214] J. Yu, H. Liu, Q. Yu, J. Ren, C. Hao, H. Ding, G. Huang, G. Huang, Y. Song, P. Cai _et al._ , “Forcevla: Enhancing vla models with a forceaware moe for contact-rich manipulation,” in _Conference on Robot Learning_ , 2026. 

- [215] M. Du, O. Y. Lee, S. Nair, and C. Finn, “Play it by ear: Learning skills amidst occlusion through audio-visual imitation learning,” in _Robotics: Science and Systems_ , 2022. 

- [216] H. Li, Y. Zhang, J. Zhu, S. Wang, M. A. Lee, H. Xu, E. Adelson, L. Fei-Fei, R. Gao, and J. Wu, “See, hear, and feel: Smart sensory fusion for robotic manipulation,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 1368–1378. 

- [217] Z. Liu, C. Chi, E. Cousineau, N. Kuppuswamy, B. Burchfiel, and S. Song, “Maniwav: Learning robot manipulation from in-the-wild audio-visual data,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 947–962. 

- [218] W. Zhao, P. Ding, M. Zhang, Z. Gong, S. Bai, H. Zhao, and D. Wang, “Vlas: Vision-language-action model with speech instructions for customized robot manipulation,” _International Conference on Learning Representations (ICLR)_ , 2025. 

- [219] K. He, X. Chen, S. Xie, Y. Li, P. Doll´ar, and R. Girshick, “Masked autoencoders are scalable vision learners,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2022, pp. 16 000–16 009. 

- [220] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pre-training of deep bidirectional transformers for language understanding,” in _Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers)_ , 2019, pp. 4171–4186. 

- [221] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, “Imagenet: A large-scale hierarchical image database,” in _2009 IEEE conference on computer vision and pattern recognition_ . IEEE, 2009, pp. 248–255. 

- [222] K. Grauman, A. Westbury, E. Byrne, Z. Chavis, A. Furnari, R. Girdhar, J. Hamburger, H. Jiang, M. Liu, X. Liu _et al._ , “Ego4d: Around the world in 3,000 hours of egocentric video,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2022, pp. 18 995–19 012. 

- [223] H. R. Walke, K. Black, T. Z. Zhao, Q. Vuong, C. Zheng, P. HansenEstruch, A. W. He, V. Myers, M. J. Kim, M. Du _et al._ , “Bridgedata v2: A dataset for robot learning at scale,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 1723–1736. 

19 

- [224] S. Parisi, A. Rajeswaran, S. Purushwalkam, and A. Gupta, “The unsurprising effectiveness of pre-trained vision models for control,” in _international conference on machine learning_ . PMLR, 2022, pp. 17 359–17 371. 

- [225] J. Shang, K. Schmeckpeper, B. B. May, M. V. Minniti, T. Kelestemur, D. Watkins, and L. Herlant, “Theia: Distilling diverse vision foundation models for robot learning,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 724–748. 

- [226] A. Majumdar, K. Yadav, S. Arnaud, J. Ma, C. Chen, S. Silwal, A. Jain, V.-P. Berges, T. Wu, J. Vakil _et al._ , “Where are we in the search for an artificial visual cortex for embodied intelligence?” in _Advances in Neural Information Processing Systems_ , vol. 36, 2023, pp. 655–677. 

- [227] S. Karamcheti, S. Nair, A. S. Chen, T. Kollar, C. Finn, D. Sadigh, and P. Liang, “Language-driven representation learning for robotics,” in _Robotics: Science and Systems_ , 2023. 

- [228] M. K. Srirama, S. Dasari, S. Bahl, and A. Gupta, “Hrp: Human affordances for robotic pre-training,” in _Robotics: Science and Systems_ , 2024. 

- [229] I. Radosavovic, T. Xiao, S. James, P. Abbeel, J. Malik, and T. Darrell, “Real-world robot learning with masked visual pre-training,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 416–426. 

- [230] R. Zheng, Y. Liang, X. Wang, S. Ma, H. Daum´e III, H. Xu, J. Langford, P. Palanisamy, K. S. Basu, and F. Huang, “Premier-taco: Pretraining multitask representation via temporal action-driven contrastive loss,” in _International Conference on Machine Learning_ , 2024. 

- [231] G. Jiang, Y. Sun, T. Huang, H. Li, Y. Liang, and H. Xu, “Robots pretrain robots: Manipulation-centric robotic representation from largescale robot datasets,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [232] A. Edwards, H. Sahni, Y. Schroecker, and C. Isbell, “Imitating latent policies from observation,” in _International conference on machine learning_ . PMLR, 2019, pp. 1755–1763. 

- [233] D. Schmidt and M. Jiang, “Learning to act without actions,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [234] S. Lee, Y. Wang, H. Etukuru, H. J. Kim, N. M. M. Shafiullah, and L. Pinto, “Behavior generation with latent actions,” in _Proceedings of the 41st International Conference on Machine Learning_ , 2024, pp. 26 991–27 008. 

- [235] K. Wu, Y. Zhu, J. Li, J. Wen, N. Liu, Z. Xu, and J. Tang, “Discrete policy: Learning disentangled action space for multi-task robotic manipulation,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 8811–8818. 

- [236] H. Li, Q. Lv, R. Shao, X. Deng, Y. Li, J. HAO, and L. Nie, “Star: Learning diverse robot skill abstractions through rotation-augmented vector quantization,” in _Forty-second International Conference on Machine Learning_ , 2025. 

- [237] S. Ye, J. Jang, B. Jeon, S. J. Joo, J. Yang, B. Peng, A. Mandlekar, R. Tan, Y.-W. Chao, B. Y. Lin _et al._ , “Latent action pretraining from videos,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [238] J. Jang, S. Ye, Z. Lin, J. Xiang, J. Bjorck, Y. Fang, F. Hu, S. Huang, K. Kundalia, Y.-C. Lin, L. Magne, A. Mandlekar, A. Narayan, Y. L. Tan, G. Wang, J. Wang, Q. Wang, Y. Xu, X. Zeng, K. Zheng, R. Zheng, M.-Y. Liu, L. Zettlemoyer, D. Fox, J. Kautz, S. Reed, Y. Zhu, and L. Fan, “Dreamgen: Unlocking generalization in robot learning through video world models,” in _Proceedings of the 9th Conference on Robot Learning (CoRL)_ , 2025, pp. 5170–5194. 

- [239] C. Wang, L. Fan, J. Sun, R. Zhang, L. Fei-Fei, D. Xu, Y. Zhu, and A. Anandkumar, “Mimicplay: Long-horizon imitation learning by watching human play,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 201–221. 

- [240] A. Liang, P. Czempin, M. Hong, Y. Zhou, E. Biyik, and S. Tu, “Clam: Continuous latent action models for robot learning from unlabeled demonstrations,” _arXiv preprint arXiv:2505.04999_ , 2025. 

- [241] J. Yang, Y. Shi, H. Zhu, M. Liu, K. Ma, Y. Wang, G. Wu, T. He, and L. Wang, “Como: Learning continuous latent motion from internet videos for scalable robot learning,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2026, pp. 42 352–42 363. 

- [242] Y. Hu, Y. Guo, P. Wang, X. Chen, Y.-J. Wang, J. Zhang, K. Sreenath, C. Lu, and J. Chen, “Video prediction policy: A generalist robot policy with predictive visual representations,” in _Forty-second International Conference on Machine Learning_ , 2025. 

- [243] R. Zheng, J. Wang, S. Reed, J. Bjorck, Y. Fang, F. Hu, J. Jang, K. Kundalia, Z. Lin, L. Magne _et al._ , “FLARE: Robot learning with implicit world modeling,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [244] Y. Liao, P. Zhou, S. Huang, D. Yang, S. Chen, Y. Jiang, Y. Hu, S. Liu, J. Luo, L. Chen _et al._ , “Genie envisioner: A unified world foundation platform for robotic manipulation,” in _International Conference on Learning Representations_ , vol. 2026, 2026, pp. 88 446–88 463. 

- [245] E. Bauer, E. Nava, and R. K. Katzschmann, “Latent action diffusion for cross-embodiment manipulation,” in _CoRL 2025 Workshop Dexterous Manipulation: Learning and Control with Diverse Modalities_ , 2025. 

- [246] Y. Huang, J. Zhang, S. Zou, X. Liu, R. Hu, and K. Xu, “Ladi-wm: A latent diffusion-based world model for predictive manipulation,” in _Proceedings of the 9th Conference on Robot Learning (CoRL)_ , 2025, pp. 1726–1743. 

- [247] Y. Han, M. Xie, Y. Zhao, and H. Ravichandar, “On the utility of koopman operator theory in learning dexterous manipulation skills,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 106–126. 

- [248] H. Chen, A. Abuduweili, A. Agrawal, Y. Han, H. Ravichandar, C. Liu, and J. Ichnowski, “Korol: Learning visualizable object feature with koopman operator rollout for manipulation,” in _CoRL_ , 2024. 

- [249] J. Bi, K. Lim, K. Chen, Y. Huang, and H. Soh, “Imitation learning with limited actions via diffusion planners and deep koopman controllers,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 4861–4868. 

- [250] M. S. Yang, D. Schuurmans, P. Abbeel, and O. Nachum, “Chain of thought imitation with procedure cloning,” in _Advances in Neural Information Processing Systems_ , vol. 35, 2022, pp. 36 366–36 381. 

- [251] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _Robotics: Science and Systems_ , 2023. 

- [252] H. Bharadhwaj, J. Vakil, M. Sharma, A. Gupta, S. Tulsiani, and V. Kumar, “Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 4788–4795. 

- [253] L. Fu, H. Huang, G. Datta, L. Y. Chen, W. C.-H. Panitch, F. Liu, H. Li, and K. Goldberg, “In-context imitation learning via next-token prediction,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [254] Z. Gong, P. Ding, S. Lyu, S. Huang, M. Sun, W. Zhao, Z. Fan, and D. Wang, “Carp: Visuomotor policy learning via coarse-to-fine autoregressive prediction,” _Proceedings of the IEEE international conference on computer vision_ , 2025. 

- [255] Y. Wang, Y. Zhang, M. Huo, T. Tian, X. Zhang, Y. Xie, C. Xu, P. Ji, W. Zhan, M. Ding _et al._ , “Sparse diffusion policy: A sparse, reusable, and flexible policy for robot learning,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 649–665. 

- [256] J. Yang, Z. Cao, C. Deng, R. Antonova, S. Song, and J. Bohg, “Equibot: Sim (3)-equivariant diffusion policy for generalizable and data efficient learning,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 1048– 1068. 

- [257] C. Zhu, R. Yu, S. Feng, B. Burchfiel, P. Shah, and A. Gupta, “Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets,” in _Robotics: Science and Systems_ , 2025. 

- [258] F. Zhang and M. Gienger, “Affordance-based robot manipulation with flow matching,” _arXiv preprint arXiv:2409.01083_ , 2024. 

- [259] K. Black, M. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 33 383–33 407, 2025. 

- [260] X. Jia, Q. Wang, A. Donat, B. Xing, G. Li, H. Zhou, O. Celik, D. Blessing, R. Lioutikov, and G. Neumann, “Mail: Improving imitation learning with selective state space models,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [261] Y. Zhong, Y. Liu, C. Xiao, Z. Yang, Y. Wang, Y. Zhu, Y. Shi, Y. Sun, X. Zhu, and Y. Ma, “Freqpolicy: Frequency autoregressive visuomotor policy with continuous tokens,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 56 493–56 526, 2025. 

- [262] T. Yu, D. Quillen, Z. He, R. Julian, K. Hausman, C. Finn, and S. Levine, “Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning,” in _Conference on robot learning_ . PMLR, 2020, pp. 1094–1100. 

- [263] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison, “Rlbench: The robot learning benchmark & learning environment,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 3019–3026, 2020. 

- [264] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard, “Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 3, pp. 7327–7334, 2022. 

- [265] A. Mandlekar, D. Xu, J. Wong, S. Nasiriany, C. Wang, R. Kulkarni, L. Fei-Fei, S. Savarese, Y. Zhu, and R. Mart´ın-Mart´ın, “What matters 

20 

- in learning from offline human demonstrations for robot manipulation,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 1678–1690. 

- [266] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” in _Advances in Neural Information Processing Systems_ , vol. 36, 2023, pp. 44 776–44 791. 

- [267] S. Nasiriany, A. Maddukuri, L. Zhang, A. Parikh, A. Lo, A. Joshi, A. Mandlekar, and Y. Zhu, “Robocasa: Large-scale simulation of everyday tasks for generalist robots,” in _RSS 2024 Workshop: Data Generation for Robotics_ , 2024. 

- [268] X. Li, K. Hsu, J. Gu, O. Mees, K. Pertsch, H. R. Walke, C. Fu, I. Lunawat, I. Sieh, S. Kirmani _et al._ , “Evaluating real-world robot manipulation policies in simulation,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 3705–3728. 

- [269] T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Q. Liang, Z. Li, X. Lin, Y. Ge, Z. Gu _et al._ , “Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation,” _arXiv preprint arXiv:2506.18088_ , 2025. 

- [270] S. Tao, F. Xiang, A. Shukla, Y. Qin, X. Hinrichsen, X. Yuan, C. Bao, X. Lin, Y. Liu, T.-k. Chan _et al._ , “Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai,” in _Robotics: Science and Systems_ , 2025. 

- [271] S. Zhang, Z. Xu, P. Liu, X. Yu, Y. Li, Q. Gao, Z. Fei, Z. Yin, Z. Wu, Y.-G. Jiang _et al._ , “Vlabench: A large-scale benchmark for languageconditioned robotics manipulation with long-horizon reasoning tasks,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2025, pp. 11 142–11 152. 

- [272] K. Dreczkowski, P. Vitiello, V. Vosylius, and E. Johns, “Learning a thousand tasks in a day,” _Science Robotics_ , vol. 10, no. 108, p. eadv7594, 2025. 

- [273] H. Liu, C. Kim, B. Liu, M. Liu, and Y. Zhu, “Pretrained visionlanguage-action models are surprisingly resistant to forgetting in continual learning,” in _Forty-third International Conference on Machine Learning_ , 2026. 

- [274] A. Yakefu, B. Xie, C. Xu, E. Zhang, E. Zhou, F. Jia, H. Yang, H. Fan, H. Zhang _et al._ , “Robochallenge: Large-scale real-robot evaluation of embodied policies,” _arXiv preprint arXiv:2510.17950_ , 2025. 

- [275] R. Li, Y. Zhou, Y. Zhu, K. Chen, J. Wang, S. Wang, K. Hu, M. Yu, B. Jiang, Z. Su _et al._ , “Roboclaw: An agentic framework for scalable long-horizon robotic tasks,” in _European conference on computer vision_ , 2026. 

- [276] X. Yang, C. Eppner, J. Tremblay, D. Fox, S. Birchfield, and F. Ramos, “Robot policy evaluation for sim-to-real transfer: A benchmarking perspective,” in _Robot Evaluation for the Real World_ , 2025. 

- [277] Z. Zhang, C. Yue, H. Xu, M. Liao, X. Qi, H.-a. Gao, Z. Wang, and H. Zhao, “Robochemist: Long-horizon and safety-compliant robotic chemical experimentation,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [278] S. Li, L. Gao, J. Wang, C. Che, X. Xiao, J. Cao, Y. Hu, and H. R. Karimi, “Information-theoretic graph fusion with vision-languageaction model for policy reasoning and dual robotic control,” _Information Fusion_ , p. 104193, 2026. 

- [279] E. Zhou, Q. Su, C. Chi, Z. Zhang, Z. Wang, T. Huang, L. Sheng, and H. Wang, “Code-as-monitor: Constraint-aware visual programming for reactive and proactive robotic failure detection,” in _2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 2025, pp. 6919–6929. 

- [280] N. Hansen, H. Su, and X. Wang, “Td-mpc2: Scalable, robust world models for continuous control,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

21 

