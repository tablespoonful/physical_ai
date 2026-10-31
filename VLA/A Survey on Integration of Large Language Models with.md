---
title: "A Survey on Integration of Large Language Models with Intelligent Robots"
date: "2024-04-14"
authors: "Yeseung Kim; Dohyun Kim; Jieun Choi; Jisang Park; Nayoung Oh; Daehyung Park"
url: https://arxiv.org/abs/2404.09228
pdf: https://arxiv.org/pdf/2404.09228
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2404.09228)** / [論文ページ](https://arxiv.org/abs/2404.09228)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# A Survey on Integration of Large Language Models with Intelligent Robots 

Yeseung Kim, Dohyun Kim, Jieun Choi, Jisang Park, Nayoung Oh, *Daehyung Park 

Korea Advanced Institute of Science and Technology, Daejeon, Republic of Korea. 

*Corresponding author(s). E-mail(s): daehyung@kaist.ac.kr; Contributing authors: yeseung.kim.88@kaist.ac.kr; dohyun141@kaist.ac.kr; jichoi0101@kaist.ac.kr; jisang.park@kaist.ac.kr; lightsalt@kaist.ac.kr; 

#### **Abstract** 

In recent years, the integration of large language models (LLMs) has revolutionized the field of robotics, enabling robots to communicate, understand, and reason with human-like proficiency. This paper explores the multifaceted impact of LLMs on robotics, addressing key challenges and opportunities for leveraging these models across various domains. By categorizing and analyzing LLM applications within core robotics elements—communication, perception, planning, and control—we aim to provide actionable insights for researchers seeking to integrate LLMs into their robotic systems. Our investigation focuses on LLMs developed post-GPT-3.5, primarily in text-based modalities while also considering multimodal approaches for perception and control. We offer comprehensive guidelines and examples for prompt engineering, facilitating beginners’ access to LLM-based robotics solutions. Through tutorial-level examples and structured prompt construction, we illustrate how LLM-guided enhancements can be seamlessly integrated into robotics applications. This survey serves as a roadmap for researchers navigating the evolving landscape of LLM-driven robotics, offering a comprehensive overview and practical guidance for harnessing the power of language models in robotics development. 

**Keywords:** Large language models, Intelligent robotics, Prompt engineering, Multimodal perception 

## **1 Introduction** 

Over the last decade, we have witnessed remarkable progress in the field of robotics in applying language models (LMs). This progress includes not only human-like communication but also understanding and reasoning capabilities of robots, thereby significantly improving their effectiveness across various tasks, from household chores to industrial operations [52, 105]. In the early stage of work, the success stemmed from statistical models analyzing and predicting words in linguistic expressions. These models enable robots 

to interpret human commands [110, 121], understand contexts [3, 5], represent the world [50], and interact with humans [135], albeit with a limited depth of understanding. Then, the adoption of Transformer architecture with self-attention mechanisms [141], particularly pre-trained LMs such as BERT [26], has elevated the capability of capturing complex patterns while fine-tuning models for specific tasks. However, the performance of these models is often contingent upon limited datasets, 

1 

constraining their ability to grasp deeper contextual understanding and generalize across diverse scenarios. 

With the advancement of large language models (LLMs), language-based robotics introduce innovative changes across various domains such as information retrieval, reasoning tasks, adaptation to environments, continuous learning and improvements, etc. [61, 64]. These LLMs, characterized by their vast parameter sizes and training on internet-scale datasets, offer zero- and fewshot learning capabilities for downstream tasks without requiring additional parameter updates. These prominent advancements come from emergent abilities, defined as “the abilities that are not present in small models but arise in large models” in the literature [148]. The abilities have significantly enhanced robots’ performance in understanding, inferring, and responding to open-set instructions by leveraging extensive common-sense knowledge [8]. Furthermore, prompt engineering techniques have enabled LLMs to incorporate richer contextual information through free-form language descriptions or interactive dialogues, facilitating generalized reasoning [149]. The introduction of in-context learning abilities [8] leads LLMs to generate outputs in expected formats, such as JSON, YAML, or PDDL, or even code, based on provided instructions or demonstrations in prompts [42, 86]. Recent LLMs, such as GPT-4, have further expanded capabilities by integrating with external robotics tools such as planners or translators [89]. 

Despite the diverse capabilities of LLMs, their utilization faces several challenges [69]. Firstly, LLMs often generate inaccurate or unexpected responses. As the safety of robot execution is one of the most important deployment factors, LLMbased robotic applications require filtering and correction mechanisms to ensure safety. Second, the emergent abilities, such as in-context learning, are not predictable and consistent yet [19]. Even minor alterations to input text may lead to unpredictable changes in response. Third, a well-designed prompt enables robots to effectively leverage the abilities of LLMs but there is a lack of systematic guidelines supporting key components of robotic systems, hindering seamless integration [35, 54, 164]. Therefore, we need to investigate component-wise LLM engagements in robotics toward an understanding of limitations and safety. 

Currently, various surveys have started exploring the intersection of LLMs and robotics [142, 164], primarily focusing on application or interaction dimensions of LLM-based robotics. However, there remains a gap in providing holistic reviews and actionable insights for integrating LLMs across key elements of robotic systems, including communication, perception, planning, and control. Additionally, researchers explore the wide field of pre-trained large-capacity models, called foundation models, seeking the generalization capabilities across multimodal transformer-based models [35, 54]. However, this expansive field spans a wide spectrum of robotics and diverse methodologies, making emerging researchers miss in-depth reviews and guidelines. 

In this paper, as shown in Fig. 1, we aim to categorize and analyze how LLMs could enhance core elements of robotics systems and how we can guide emerging researchers in integrating LLMs within each domain, encompassing communication, perception, planning, and control, toward the development of intelligent robots. We structure this paper following three key questions: 

- Q1: How are LLMs being utilized in each robotics domain? 

- Q2: How can researchers overcome the integration limitation of LLMs? 

- Q3: What basic prompt structures are required to produce a minimum functionality in each domain? 

To address these questions, we focus on LLMs developed after the introduction of GPT-3.5 [106]. We primarily consider text-based modalities but also review multimodalities for perception and control areas. However, for an in-depth review, we limit our investigation to LLMs rather than foundation models. 

In addition, we provide comprehensive guidelines and examples for prompt engineering, aimed at enabling beginners to access LLM-based robotics solutions. Our tutorial-level examples illustrate how fundamental functionalities of robotic components can be augmented or replaced by introducing four types of exemplary prompts: conversational prompt for interactive grounding, directive prompt for scene-graph generation, planning prompt for few-shot planning, and code-generation prompt for reward generation. By providing rules and tips for prompt construction, we outline 

2 

the process of generating well-designed prompts to yield outputs in the desired format. These principles ensure effective LLM-guided enhancements in robotics applications, without parameter adjustments. 

The remainder of this paper is organized as follows. Section 2 outlines the historical background of LMs and LLMs in robotics. Section 3 reviews how LLMs empower robots to communicate via language understanding and generation. Section 4 investigate how LLMs perceive various sensor modalities and advance sensing behaviors. Section 5 and Section 6 organize LLM-based planning and control studies, respectively. In Section 7, we provide comprehensive guideline for prompt engineering as a starting point for LLM integration in robotics. Finally, Section 8 summarizes this survey. 

The studies in the pre-LLM era also show improved application performance unlike previous methods trained on small, task-specific datasets. Transformer-based models and self-supervised learning techniques, such as masked language modeling, have led to the development of internetscale pre-trained models, including BERT [26] and GPT-2 [115]. These models exhibit a broad understanding of language, enabling both (1) improved generalization abilities and (2) fine-tuning for specific robotic tasks [74, 75, 124]. In addition, researchers have also developed LMs that process multi-modal information [116] since robotic applications often require accessing diverse multimodalities, such as natural language and vision, for interaction with users and environment [76, 126]. 

### **2.2 Large Language Model in Robotics** 

## **2 Preliminary** 

We briefly review language models used in robotics, categorizing them in terms of pre- and post-LLM eras. Unlike previous literature [164], we define the pre-LLM era as the period for LMs up to the advent of GPT-2 [115], characterized by neural language models such as recurrent neural networks (RNNs) [33] and early Transformer architectures. We then provide a brief explanation of LLMs, introducing terminologies and techniques for subsequent reviews. 

### **2.1 Language Models in Robotics** 

In the pre-LLM era, early-stage studies have primarily focused on sequential data processing, using RNN-based models [23, 46]. The models are often to transform linguistic commands into a sequence of actions [6, 99] or formal languages [40], leveraging RNN’s sequence-to-sequence modeling capabilities. On the other hand, researchers have also used RNNs as language encoders converting textual input into linguistic features that could be mapped to visual features for referring object identification [121, 125]. However, the long-term dependency issue in RNNs restricts the scope of applications. Then, the Transformer architecture [141], which is a non-sequential model supporting long-range comprehension, has enabled new robotic tasks, such as vision-and-language navigation [14, 16]. 

Recent advancements in LLMs, such as GPT3 [8], GPT-4 [107], LLaMA [137], Llama 2 [138], and Gemini [2], demonstrate notable improvements in understanding, contextual awareness, generalization capabilities, and knowledge richness, surpassing earlier language models. These improvements are from their training on vast datasets with billion-scale parameters, enabling them to capture intricate data patterns. Further, advanced learning strategies, such as reinforcement learning from human feedback, have been developed to align the behaviors of LLMs with human values or preferences [108]. However, learning with large-scale parameters requires computationally expensive costs of updating the entire model. To address this issue, researchers have developed parameter-efficient fine-tuning methods (e.g., an adapter [49] and LoRA [51]) for robotic tasks. For example, `LLM-POP` [132] fine-tunes their model using adapters, which are small, trainable networks inserted into each layer of an LLM for interactive planning scenarios. 

Alternatively, prompt engineering with incontext learning (ICL) [8] marks a significant advancement in learning from prompts without additional training. Its effectiveness relies on the design and quality of prompts, which can be enhanced with detailed task descriptions, fewshot examples, or model-friendly formats (e.g., ‘###’ as a stop symbol [167]). Moreover, chainof-thought (CoT) prompting [149] is another 

3 


**Fig. 1** : Overview structure of intelligent robotics research integrated with LLMs in this survey. The rightmost cells show the representative names (e.g., method, model, or authors) of papers in each category. 

emerging approach that incorporates intermediate reasoning steps in prompts. The CoT method substantially enhances the reasoning and problemsolving capabilities of LLMs, making it a dominant technique in robotics applications [86, 128, 163]. 

agents effectively [97]. We categorize the communication capabilities into two primary areas: (1) language understanding and (2) language generation. We show the detailed categorization in Fig. 1 alongside relevant studies, referred in green cells. 

## **3 Communication** 

We investigate the utilization of LLMs to facilitate human-like communication in robotics, enabling robots to interact with humans and other robotic 

### **3.1 Language Understanding** 

We review language understanding capabilities, addressing how LLMs handle the variability and 

4 

ambiguity of linguistic inputs through _interpretation_ and _grounding_ processes. 

_Interpretation_ transforms natural-language inputs into semantic representations that are easier for robots to process. These representations include formal languages such as linear temporal logic (LTL) [93, 160] and planning domain definition language (PDDL) [18, 42, 89, 155], as well as programming languages such as Python [56, 76]. To aid in interpreting free-form sentences, researchers leverage LLMs’ ICL capabilities, providing guidelines and demonstrations within prompts [56, 76, 89, 122]. Despite the efforts, LLMs often fail to satisfy syntax or capture precise semantics when translating an input into formal languages. To address this issue, researchers suggest simplifying vocabulary or fine-tuning LLMs with domainagnostic data [93, 160]. For example, `Lang2LTL` [91] translates landmark-referring expressions in navigational commands into LTL symbols. Further improvements often involve in using human feedback and syntax checkers to correct generated formal language translations [18, 42]. For instance, Guan et al. present a human-in-the-loop translation framework, in which human domain experts repeatedly review PDDL descriptions and provide feedback in natural language [42]. 

_Grounding_ is another process that maps linguistic expressions to reference targets, such as behaviors or objects, recognizable to robots. Early studies identify mappings that maximize the cosine similarity between word embeddings of LLM outputs and real-world targets [58, 76, 93, 117]. Subsequent studies leverage LLMs’ commonsense knowledge to capture the context of object text labels for improved grounding [41, 118]. For instance, `ConceptGraphs` [41] demonstrate how LLMs can ground an expression, ‘something to use as a paperweight,’ to a ceramic vase based on size and weight assumptions. However, grounding accuracy depends on the detail and accuracy of the world model. To address this, researchers augment LLMs with multimodal capabilities to directly correlate linguistic inputs with sensory percepts [31, 47, 114, 159], or enable LLMs to interact with environments [158, 168] or humans [61, 109, 120] for better context gathering. For instance, `LLM-Grounder` [158], a 3D visual grounding method, actively gathers environmental 

information using vision tools such as LERF [72] and OpenScene [111]. 

### **3.2 Language Generation** 

Language generation refers to the production of human-like written or spoken language that reflects communicative intents [39]. We categorize language generation into _task-dependent_ and _-independent_ types based on their communication intents, diverging from conventional natural language generation (NLG) categories of _text-to-text_ and _data-to-text_ [30] due to our focus on the communicative purposes of studies. 

_Task-dependent_ language generation focuses on producing language with specific functional objectives, being declarative or imperative. To generate open-ended declarative statements, researchers often provide LLMs with contextual information [20, 62, 96]. However, LLMs often result in repetitive and factually inconsistent outputs, confined by the reliance on previous dialogues and commonsense knowledge [20, 83]. Consequently, researchers augment LLMs with auxiliary knowledge sources to broaden the scope of available information [4, 21, 157]. For instance, Axelsson and Skantze enhance a robot museum guide with knowledge graphs [4]. Furthermore, researchers instruct LLMs to clarify ambiguities by generating imperative instructions requesting human assistance [25, 61]. To improve inference steps, probabilistic models have been introduced to evaluate the uncertainty of situations [109, 120]. For instance, `KnowNo` [120] and `CLARA` [109] interaction systems assess confidence and semantic variance, respectively, triggering generation only when these metrics indicate significant uncertainty. 

_Task-independent_ language generation involves crafting expressions with social-emotional objectives [11], by embedding non-verbal cues (e.g., non-verbal sounds, hand gestures, and facial expressions) within prompts to enhance engagement and empathy [73, 80]. For example, Khoo et al. have developed a conversational robot that generates empathetic responses using transcribed audio and visual cues [73]. However, conversations with LLMs remain superficial due to the limited knowledge and dialogue history [65]. To overcome this, researchers integrate memory modules into LLMs, enabling them to distill and store 

5 

information from conversations in a structured format [22, 63, 65, 162]. For example, the companion robot designed by Irfan et al. continuously updates the robot’s memory based on interactions with users to generate personalized dialogues [65]. 

## **4 Perception** 

Perception plays a crucial role in enabling robots to make decisions, plan their actions, and navigate the real world [113]. In the field of LLM-based robotic perception, research primarily focuses on two aspects: sensing modalities and behaviors. In this section, we introduce how LLM-based robots have integrated language with sensor modalities and how agents acquire environmental information through passive and active perception behaviors. Fig. 1 presents the detailed categorization alongside relevant studies, referred in pink cells. 

### **4.1 Sensing Modalities** 

Researchers have significantly advanced robots’ comprehension and generalization capabilities through the integration of multimodal language models. We categorize primary sensing modalities into _visual_ , _auditory_ , and _haptic_ modalities, reviewing recent studies leveraging multimodal LLMs for perception tasks. 

_Visual_ perception tasks involve the interpretation of visual information such as image or point clouds. Pre-trained visual-language models (VLMs), such as CLIP [116] and InstructBLIP [82], allows LLM-based robots to directly utilize image sources. For instance, recent LLM-based manipulation systems, such as `TidyBot` [152] and `RoCo` [96], use image-inferred object labels or scene descriptions generated from CLIP and OWL-ViT [100], respectively. In addition, researchers extend reasoning capabilities by applying VLMs on downstream tasks such as image captioning [41] and visual question answering (VQA) [37, 78, 103]. The downstream tasks enable LLMs to subsequently request VLMs to infer object properties (e.g., material, fragility) [37] or ground object parts for grasping [103]. However, images are often challenging to acquire spatial-geometric information. 

Alternatively, Huang et al. associate visuallanguage features from a VLM (i.e., LSeg [81]) with three-dimensional (3D) point clouds for 3D map reconstruction [56]. Further, Jatavallabhula 

et al. improve this association mechanism with RGB-D images by introducing fine-grained and pixel-aligned features from VLMs [66]. However, association with 3D information tends to be memory intensive, limiting scalability for large scenes [56, 66, 158]. As an alternative solution, researchers often associate geometric and semantic features with 3D scene graphs [41]. 

_Auditory_ perception involves the interpretation of sound. LLM-based studies often leverage pretrained audio-language models (ALMs), such as AudioCLIP [43] and Wav2CLIP [151], integrating them with visual data to enhance environmental or contextual understanding [55, 94, 123, 163]. For example, `AVLMaps` [55], a 3D spatial map constructor with cross-modal information, integrates audio, visual, and language signals into 3D maps, enabling agents to navigate using multimodal objectives such as “move between the image of a refrigerator and the sound of breaking glass.” In addition, `REFLECT` [94], a framework for summarizing robot failures, transforms multisensory observations such as RGB-D images, audio clips, and robot states into textual descriptions to enhance LLM-based failure reasoning. 

_Haptic_ perception involves the interpretation of contact information. Researchers introduce multimodal perception modules that interactively incorporate _haptic_ features obtained from predefined high-level descriptions [168] or CLIP-based tactile-image features [48] about haptic interactions. For example, `MultiPLY` [48], a multisensory LLM, converts tactile sensory readings into a heatmap, encoded by CLIP. Then, by introducing a linear layer of tactile projector, the model maps the heatmap information to the feature space of LLMs. 

### **4.2 Sensing Behavior** 

Following the type of sensing behaviors, we decompose this section into _passive_ and _active_ perceptions. 

The _passive_ perception refers to the process of gathering sensory information without actively seeking it out. Despite its limited nature, _passive_ sensing has been extensively employed in LLMbased robotics studies for various tasks: object recognition [37, 53, 152], pose estimation [103, 156], scene reconstruction [41, 59, 122, 122], and object grounding [66, 144, 158]. For example, `TidyBot` 

6 

[152] detects the closest object from an overhead view and subsequently recognizes its object category using a closer view captured by the robot’s camera. However, the _passive_ nature of sensing limits the ability to perform tasks when information is unobserved or unavailable (e.g., unseen area, weight). 

On the other hand, _active_ perception refers to the conscious process of gathering sensory information by taking additional actions. _Active_ information gathering enhances environmental understanding by acquiring new information through sensory observations or requesting user feedback [78, 129]. For example, `LLM-Planner` [129] generates seeking actions such as ‘open the refrigerator’ to locate invisible objects. Recent studies also focus on collecting sensory data to better understand objects’ physical properties [48, 132, 168]. However, LLMs often generate inaccurate or fabricated information, known as hallucinations. To address this issue, Dai et al. introduce a personalized conversational agent designed to ask users for uncertain information [25]. 

## **5 Planning** 

Planning involves organizing actions to solve given problems, typically through generating a sequence of high-level symbolic operators (i.e., task planning) followed by executing them using low-level motor controllers [38, 84]. This section investigates how LLM-based planning research addresses limitations in the planning domain by categorizing them into three key research areas: (1) task planning, (2) motion planning, and (3) task and motion planning (TAMP). Fig. 1 presents the detailed categorization along with related planning studies, referred in purple cells. 

### **5.1 Task Planning** 

LLM-based task planners are capable of generating plans without strict symbol definitions [58], while traditional task planners are required to predefine operators with domain knowledge about available actions and constraints [34, 98]. In this field, most planners employ a _static_ planning strategy, which takes fixed descriptions that are not adaptable to the changes in environment [163]. However, an alternative approach, _adaptive_ planning, allows for the incorporation of environmental 

feedback into input prompts, enabling adjustments to actions based on observed conditions. This section reviews LLM-based planners in terms of these two strategies: _static_ and _adaptive_ planning. **Static planning** : _Static planning_ approaches are generally zero- or few-shot prediction methods, where zero-shot methods generate a plan based solely on an input command, while few-shot methods leverage learning from a limited set of similar examples [9, 27, 70, 163]. However, LLMs often exhibit poor performance in long-horizon task planning due to limited reasoning ability [89, 140]. To address this limitation, Huang et al. introduce a planner that iteratively selects the most probable action among executable ones generated by LLMs [58]. 

Alternatively, LLM-based code generators, such as `Code as Policies` [86] or `ProgPrompt` [128], produce codes that result in actions responsive to observations [56, 57]. Singh et al. demonstrate that code generation outperforms basic task planning from LLMs since the output plan closely aligns with execution environments [128]. Despite their advantages, these methods lack validation and replanning processes. 

To validate plans, researchers often augment LLMs with logical programs, either to (1) check if resulting plans violate logical constraints or (2) generate plans using an external logical planner. For instance, `SayPlan` [118], a GPT4-based planner, validates abstract-level actions through a scene-graph simulator 3DSG [1], while `LLM+P` [89] applies a PDDL problem translated from LLMs to a classical task planner, Fast Downward [45]. In addition, Silver et al. demonstrate that a searchbased planner with an initial plan from LLMs performs better by exploring fewer nodes [127]. These studies underscore the effectiveness of integrating LLMs with logical programs to increase the success rate or the performance of generating feasible plans. 

**Adaptive planning** : _Adaptive planning_ allows robots to modify their plans or actions in response to feedback, either by generating new plans based on environmental observations [20, 142, 152, 168, 169] or by detecting failures and adjusting accordingly [61]. Chen et al. and Huang et al. introduce adaptation strategies that generate new plans based on observed feedback, enabling robots to respond to a broader range of scenarios [12, 60]. 

7 

Another adaptation strategy is the detection of failures as feedback. For instance, `Inner Monologue` [61] retries the initial plan until it succeeds. Furthermore, other studies provide textual explanations about past failures to help avoid recurrent issues [87, 94, 117, 147]. `LLM-Planner` [129] and `COWP` [28] improve replanning capabilities by finding alternative plans that leverage context from observations and the commonsense knowledge of LLMs. These flexibilities in adapting to new information enhance robot autonomy in dynamic settings. 

### **5.2 Task and Motion Planning** 

We outline LLM-based low-level planning, classifying methodologies into motion planning and TAMP areas. 

_Motion planning_ refers to the process of generating a path by computing sequential waypoints within configuration or task spaces. Jiao et al. introduce an LLM-based motion planner that directly generates positional sequences for drone choreography [68]. While this work demonstrates LLMs’ spatial reasoning abilities, the scenario presented is relatively simple. Further, planning spaces are often continuous, which presents a challenge for language models that operate with discrete tokens. Alternatively, indirect sequencing approaches, such as `VoxPoser` [59], generate a potential field code with the help of a VLM and then conduct motion planning within the generated field, augmenting LLMs with a search-based planner. 

_TAMP_ refers to integrating high-level task planning with low-level motion planning. Recent studies often use LLMs as TAMP planners, leveraging LLMs’ logical and physical reasoning capabilities [79, 96, 153]. Researchers guide LLMs to generate high-level subgoals, which are then used for low-level trajectory generation [79, 96]. However, the coarse representations of LLMs restrict their applications to simple tasks such as pickand-place. To address this limitation, researchers use additional prompts or augment LLMs to improve reasoning abilities. For example, Xia et al. enable LLMs to consider kinematic knowledge through kinematic-aware prompting for more complex manipulation tasks, such as articulated object manipulation [153]. Ding et al. introduce a logicaugmented LLM planner that checks the logical feasibility of the task plans generated by LLMs [29]. 

Meanwhile, others use physics-augmented LLM planners to evaluate physical feasibility [18, 44, 88]. For example, `Text2Motion` [88] allows an LLM to generate physically feasible high-level actions and combine them with learned skills for low-level actions. 

## **6 Control** 

Early studies primarily focus on establishing mappings between simple linguistic commands and known motion primitives. With the advent of deep learning, researchers have explored two main approaches in control: direct modeling of control values based on linguistic instructions [7, 119] and indirect interpretation of complex instructions via LLMs to generate actions [154]. We categorize the work in this field into two groups: (1) direct approach which means the direct generation of control commands based on linguistic instructions and (2) indirect approach which stands for indirect specification of control commands through linguistic guidance. Fig. 1 presents a detailed categorization alongside related papers, referred in orange cells. 

### **6.1 Direct Approach** 

The direct approach involves using an LLM to interpret and produce executable commands, either by selecting motion primitives [134] or generating control signals [146, 170]. Early work generates action tokens to produce a control policy training Transformer architecture with taskspecific expert demonstrations such as `Gato` [119], `RT-1` [7], and `MOO` [131]. Researchers linearly map action tokens to discretized end-effector velocities [119] or displacements [7, 131] for continuous motion. While these approaches demonstrate a degree of generalization over unseen tasks, such as new objects or realistic instructions, they often require extensive data collection and training time. 

To reduce the collection effort, researchers often leverage existing web-scale vision and language datasets such as `RT-2` [170] and `RT-X` [143]. For example, Zitkovich et al. train VLMs (e.g., `PaLI-X` [17] and `PaLM-E` [31]) with visual-language datasets and robotic demonstrations [170]. This approach maintains general knowledge of visual-language tasks while training for control tasks. In addition, to reduce the training burden, Chen et al. use 

8 

a low-rank adaptation (LoRA) [51] method for fine-tuning an LLM for control tasks rather than fine-tuning the entire model [15]. 

LLMs often struggle to generate continuous action-level commands such as joint position and torque values, as LLMs typically generate atomic elements known as tokens [134]. Therefore, researchers instead generate task-level output using LLMs [10, 101, 134]. For example, `SayTap` , an LLM-based controller for walking, generates contact patterns between feet and the ground for walking motion with an LLM instead of directly producing joint positions [134]. Other studies solve the control problem as natural-language generation tasks, completing a sequence of end-effector poses [101] or generating Python codes [10]. Recent studies often restrict action space to enhance LLM control outputs. For instance, Wang et al. design a prompt that produces positive integer control values while maintaining a smoothness trend in outputs [146]. Alternatively, Li et al. demonstrate that incorporating robot kinematics information helps the LLM determine joint values for desired poses [85]. 

### **6.2 Indirect Approach** 

LLMs are also useful for generating indirect representations of control commands, such as subgoals or reward functions, based on natural language instructions. To guide the learning process, researchers leverage the goal description that explains desired behaviors in natural language [32, 67, 77]. For example, `ELLM` [32], an LLM-based reinforcement learning (RL) framework, uses an LLM to generate subgoal descriptions as prior knowledge of the RL policy and further uses the similarity between current observation and the subgoal description in text embedding space to calculate reward. Further, Kumar et al. generate a goal description based on the history of human instructions to reuse previously learned skills [77]. However, as the output of an LLM is a naturallanguage description, these approaches require an additional step of grounding or interpreting the description. 

Alternatively, researchers often generate codelevel reward functions. Yu et al. convert a naturallanguage goal into a high-level motion description and then generate a corresponding reward function 

[161]. However, this method requires pre-defined reward formats. Instead, recent work prompts an LLM to infer a new reward function from human-designed examples [71, 145]. Nonetheless, the generated reward functions may not always be accurate or optimal enough for direct use in training [130]. 

To improve accuracy, researchers add a refinement loop to validate both the syntax [112] and semantics [95, 130, 154, 165] of the generated reward functions. For example, Song et al. use an LLM to redesign a reward function based on the convergence of the training process and the resulting robot motion [130]. Chu et al. employ an LLM to directly generate rewards for evaluating robot motion [24]. Other approaches refine a motion by adjusting control parameters based on the error state [133] or by selecting a suitable motion target from human feedback [90]. 

## **7 Prompt Guideline** 

We provide prompt design guidelines for robotic tasks to researchers entering this field. A prompt is a message that directs LLMs to process and generate outputs according to our instructions [92, 150]. Well-designed prompts 

- include clear, concise, and specific statements without using technical jargon, 

- incorporate examples that allow anticipating the model’s process, 

- specify the format that we want the output to be presented, and 

- contain instructions to constrain actions. 

The prompts enable models to generate desired content following output formats and constraints without parameter updates. We provide guidelines over four robotics fields: (1) interactive grounding, (2) scene-graph generation, (3) few-shot planning, and (4) reward function generation. 

### **7.1 Conversation Prompt: Interactive Grounding** 

We detail a conversation prompt design, leveraging an LLM as a grounding agent, to clarify commands such as ‘Bring me something to eat’ and infer the ambiguous targets, expressed as ‘something,’ through logical inference. Fig. 2 shows the design detail, where the prompt consists of three key 

9 

|Task Description<br>i|
|---|
|You are a conversational agent that interactively grounds referenced objects within tasks to a specific world model. You should<br>engage with humans for clarifications and logically infer the target objects. Keep your response concise without explanation.<br>Task Procedure|
|You should:<br>1. Identify the target objects and their details from the task.<br>2. Iteratively ask for additional detail with a new criterion if multiple options within the world model meet the criteria.<br>3. Select the most appropriate object within the world model when only a single option meets the criteria.<br>Task Context|
|Task: "Bring me something to eat"<br>World Model: ['water bottle', 'plate', 'napkin', 'coke can', 'potato chips', 'candle', 'sandwiches', 'pepper shaker', 'salt shaker',<br>'fork', 'banana', 'cookie', 'apple', 'cereal box', 'juice box', 'cup']|
|Interaction|
|**LLM:** Do you prefer something savory or sweet to eat?<br>**User:** sweet<br>**LLM:** Do you prefer something crunchy or soft as a sweet snack?<br>**User:** crunchy<br>**LLM:** Based on your preference for something sweet and crunchy, I suggest bringing the "cookie."|


**Fig. 2** : A conversational prompt for interactive grounding. Through the ‘task’ in the prompt, we ask an LLM to ground the underspecified object, referred to as ‘something’ in the ‘task’ as a ‘cookie’ by interactively asking for a personal preference. The prompt consists of _task description_ , _task procedure_ , and _task context_ parts guiding the LLM’s behavior and contextual understanding. The words in bold indicate the subjects of interactions, while the LLM responses are highlighted in blue. 

components: _task description_ , _task procedure_ , and _task context_ . We further describe each component as follows. 

The _task description_ outlines the expected behavior and response format of the LLM. In this example, we particularly emphasize its role as a conversational agent, which fosters dynamic interactions with users, guided by directives such as ‘you should.’ Further, the imperative statements containing ‘keep’ provide task constraints or requirements. We also place behavioral constraints at the end to suppress the LLM’s verbosity. 

The _task procedure_ then defines a sequence of inference steps for the LLM to follow, aimed at achieving the task objective. This description employs numbered steps to instruct LLMs to execute the actions step by step. By using logical representations, we also enforce actions to be performed in a logical order; we use ‘iteratively’ to indicate a ‘while loop’ and ‘if’ or ‘when’ to represent conditions. 

The _task context_ describes the contextual inputs, such as ‘world model,’ that LLMs perform grounding upon. Consistency in terminology across _task description_ and _task procedure_ is crucial for LLM operations. For example, the common expressions, such as ‘task’ and ‘world model,’ allow the LLM to work within the same context provided. Further, by using clear names for objects in the world model, we enable the LLM to apply common knowledge to named entities. Note that although 

we use a list of objects as a world model, LLMs accept world models in various formats: textual descriptions, a list of objects, and scene graphs. 

With these structured components, the prompt invokes an interactive grounding dialogue for precise object identification, as shown in Fig. 2. We obtain the resulting interaction using ChatGPT 3.5 [106]. 

### **7.2 Directive Prompt: Scene-Graph Generation** 

We introduce directive prompt designs for constructing a scene graph from a scene image using a multimodal LLM, particularly with GPT-4 [107]. The scene graph consists of objects as nodes and their relationships as edges [36, 41]. Despite the advancement of multimodal LLMs, their capability has limitations in inferring 3D relationships from a 2D image [13]. To reduce the limitation, we decompose the task into two steps: _node creation_ with multimodal inputs and _edge creation_ with textual information. We describe each step with detailed examples provided in Fig. 3. 

The prompt for _node creation_ consists of two parts: (1) _task description_ and (2) _task context_ . The _task description_ includes the multimodal LLM’s expected behavior (i.e., role) and response format, similar to Section 7.1. For instance, the multimodal LLM’s role is to identify objects as nodes in the 

10 


**Fig. 3** : Directive Prompts for generating a scene graph. The table includes two prompts: _node creation_ and _edge creation_ . Given segmented images in a scene, a VLM identifies objects, and then an LLM infers relevant relationships using geometric information. The words in bold indicate the subjects of outputs, while the model responses are highlighted in blue. The visualizations are not part of any conversations. 

given images. We then specify the output format 

as ‘ObjectName(ID)’ for consistency and simplicity. Then, the _task context_ presents a sequence 

11 

|Task Description|
|---|
|Create a next plan for a robot to complete a household task using the allowed actions and visible objects. The robot is<br>able to pick up and hold only one object. The robot CANNOT open or close some objects when the robot holds an object<br>(after PickUp and before PutInto). Initially, the robot does not hold anything, and every openable object is closed. All plan<br>sequences start with 'Initial,' which means initial condition. When the task is completed, use the action 'Done' to finish it.<br>Do not do anything other than what the task requires. Answer only one step of the next plan without other things.|
|Examples|
|For example,<br>Task: Put paper in the drawer<br>Allowed actions: Initial, Open (object), Close (object), PickUp (object), PutInto (object), Done<br>Visible objects: paper, drawer, carrot<br>Executed plans: Initial, Open (drawer), PickUp (paper), PutInto (drawer)<br>Next plan: Close (drawer)|
|Task: Put only stationery in the drawer<br>Allowed actions: Initial, Open (object), Close (object), PickUp (object), PutInto (object), Done<br>Visible objects: paper, drawer, carrot<br>Executed plans: Initial, Open (drawer), PickUp (paper), PutInto (drawer), Close (drawer)<br>Next plan: Done|
|Task Context|
|Task: Put only food in the refrigerator<br>Allowed actions: Initial, Open (object), Close (object), PickUp (object), PutInto (object), Done<br>Visible objects: refrigerator, carrot, pencil<br>Executed plans: Initial<br>Next plan:|
|LLM Output|
|**LLM:** Open (refrigerator)|
|Interaction|
|**User:** Executed plans: Initial, Open (refrigerator)<br>Next plan: **LLM:** PickUp (carrot)<br>**User:** Executed plans: Initial, Open (refrigerator), PickUp (carrot)<br>Next plan: **LLM:** PutInto (refrigerator)<br>**User:** Executed plans: Initial, Open (refrigerator), PickUp (carrot), PutInto (refrigerator)<br>Next plan: **LLM:** Close (refrigerator)<br>**User:** Executed plans: Initial, Open (refrigerator), PickUp (carrot), PutInto (refrigerator), Close (refrigerator)<br>Next plan: **LLM:** Done|


**Fig. 4** : A planning prompt for few-shot planning. Leveraging input-output example pairs, the LLM improves performance in generating a plan to accomplish the task objective. The prompt consists of _task description_ , _examples_ , and _task context_ . The words in bold indicate the subjects of interactions, while the LLM responses are highlighted in blue. 

of unique object identifiers with corresponding object-centric images. In this scenario, we assume that object-centric images are obtained using an active perception method to identify objects with occlusion. 

The _edge creation_ consists of (1) _task description_ , (2) _examples_ , and (3) _task context_ . The _task description_ not only specifies the expected behavior and output format but also elucidates on how to identify the relationships between nodes leveraging examples. We particularly explain how the LLM uses 3D object coordinates and unit measurements to infer spatial relationships from a predefined set such as ‘left,’ ‘right,’ etc. Unlike the node creation, this allows for generating additional output explanations to accommodate the complexity of discerning spatial relationships. 

To enhance the understanding of the input format and corresponding output, we include _examples_ showcasing edge generation. We choose an example similar to the target scenario in terms of 

objects and their spatial interrelationships, thereby providing richer information for edge identification. Finally, the _task context_ provides source and target node information as inputs and leaves the output empty to obtain responses from the LLM. We also assume that the 3D bounding boxes are obtained through a neural network-based detector [104] or from the extent of point clouds using depth information [41]. 

### **7.3 Planning Prompt: Few-shot Planning** 

We present a planning prompt design aimed at predicting subsequent actions to fulfill an instructed objective, integrating contextual elements such as available actions and environmental settings. This design particularly focuses on few-shot planning, enhancing performance through examples. The design comprises four components: (1) _task_ 

12 

|Task Description<br>i|
|---|
|You need to control a two-jointed robot arm to touch the target with its fingertip in 2d xy plane. The action space is Box(-1.0,<br>1.0, (2,), float32) as a torque applied to joints. Please design a reward function for training RL agents in Python based on the<br>following information.|
|Available APIs|
|You can use the following functions to design a reward function.<br>- def get_joint_angles(env) -_>_ tuple[float, float] # get the current angles of the joints in radian<br>- def get_joint_angular_velocities(env) -_>_ tuple[float, float] # get the current angular velocities of the joints in rad/s<br>- def get_current_action(env) -_>_ tuple[float, float] # get the current action torque in Nm<br>- def get_current_position(env) -_>_ tuple[float, float] # get the current x, y position of the fingertip<br>- def get_target_position(env) -_>_ tuple[float, float] # get the target x, y position|
|Goals and Constraints|
|The trained RL agent should accomplish the following goals and constraints.<br>- The starting joint angles and angular velocities are all initialized to zero<br>- The target position is randomly initialized<br>- Finish the task with less joint torque consumption as possible<br>- Do not consider other goals or constraints except given ones|
|Generation Rules|
|You should follow the rules below.<br>- Write the Python function in the form of 'def compute_reward(env) -_>_ float' and return the 'reward: float' only<br>- Do not use redundant constant variables, class instances, or functions that are not given, but you can use popular Python<br>libraries like numpy if you import them<br>- Consider the scale of each reward component<br>- Return the generated Python function only|
|LLM Output|
|`import numpy as np`|
|`def compute_reward(env) -> float:`<br>`# Get current position and target position`<br>`current_pos = np.array(get_current_position(env))`<br>`target_pos = np.array(get_target_position(env))`<br>`# Calculate Euclidean distance between current and target position`<br>`distance_to_target = np.linalg.norm(current_pos - target_pos)`<br>`# Get current joint angles and angular velocities`<br>`joint_angles = np.array(get_joint_angles(env))`<br>`joint_velocities = np.array(get_joint_angular_velocities(env))`<br>`# Get current action`<br>`current_action = np.array(get_current_action(env))`<br>`# Calculate penalty based on joint torque`<br>`torque_penalty = -0.01 * np.linalg.norm(current_action)`<br>`# Calculate reward based on distance to target`<br>`distance_reward = -0.1 * distance_to_target`<br>`# Combine rewards`<br>`reward = distance_reward + torque_penalty`<br>`return reward`|


**Fig. 5** : Prompts example for reward function generation. The prompt consists of _task description_ , _available APIs_ , _goals and constraints_ , and _generation rules_ . The LLM generates a reward function in Python code for RL training. 

_description_ , (2) _examples_ , (3) _task context_ , (4) and _additional interactions_ , detailed in Fig. 4. 

The _task description_ include task objectives, expected behaviors, and response formats similar to conventional prompts. However, unlike previous ones, this prompt specifies the robot’s constraints, including initial states and action limitations. For example, the term ‘CANNOT’ in Fig. 4 emphasizes the robot’s limitation to manipulating only one object per action. Moreover, these constraints extend to the rules governing the ‘Done’ action, indicating task completion. 

The _examples_ demonstrate input-output pairs that guide the LLM in generating the desired action. The _examples_ adapt the generic ‘object’ 

argument in the allowed actions (e.g., ‘Close (object)’) to specific object names such as ‘drawer’ or ‘paper,’ reinforcing task constraints written in the _task description_ . For instance, the second example returns the ‘Done’ signal instead of further planning after achieving the task objective. 

The _task context_ provides information about the current scenario, including ‘task,’ ‘allowed actions,’ ‘visible objects,’ ‘executed plans,’ and ‘next plan,’ as shown in the examples. We allow the LLM to fill in the blank space after ‘next plan:’ suggesting the next action without adding unnecessary elements like line breaks, ensuring output precision. 

13 

Furthermore, when additional prompts update the executed plans, the LLM generates new plans based on this updated context without reiterating the full task context, enabling a dynamic and iterative planning process that adapts to changes and maintains efficiency. 

### **7.4 Code-Generation Prompt: Reward Design** 

We introduce a code-generation prompt design to generate a reward function for the MuJoCobased Reacher task [136] from Gymnasium [139]. The goal of the Reacher task is to move the endeffector of a robotic arm close to a designated target position from an arbitrary starting configuration. The prompt is to translate this task objective into a reward-specifying code. Fig. 5 shows the design detail, comprising four key elements: (1) _task description_ , (2) _available APIs_ , (3) _goals and constraints_ , and (4) _generation rules_ . 

_Task description_ define the expected robot behavior and task conditions for the LLM, including the robot’s control strategies and the action space of the two-joint robot arm. We particularly specify the action space as a continuous ‘Box’ space using an API from Gymnasium, assuming the LLM’s familiarity with well-known library functions. Then, this description leads the LLM to grasp the overarching RL objective of the defined actions. 

_Available APIs_ list the APIs necessary for designing the reward function, including the names and input-output specifications of each API. By providing Python function annotations, we enable the LLM to infer the types of inputs and outputs, given its presumed knowledge of float-like variable types and how the APIs work. 

_Goals and constraints_ provide the task objectives and limitations that guide the reward contents. We clearly define the initial setup, goal assignment, and goal conditions, aiming to exclude unnecessary reward components, such as penalizing high velocities for smooth motion. Note that we recommend the use of concise and consistent words, such as ‘torque,’ as used in the _task description_ , instead of ‘power.’ This ensures the generated reward function aligns with the specified task requirements without introducing ambiguities or unintended penalties. 

Lastly, _generation rules_ establish guidelines for generating directly executable code, addressing the tendency of LLMs to produce unnecessary or incorrect variables or functions. These rules restrict such declarations, as written in the second component of the _generation rules_ in Fig. 5, encouraging the use of well-known Python libraries to enhance programming quality. Furthermore, considering the linearly combined elements of the reward function, we introduce a rule for scaling reward components to maintain balance. 

## **8 Conclusion** 

In this survey, we have investigated the current robotics research works with large language models in terms of intelligent robot components encompassing communication, perception, planning, and control. This component-wise investigation reveals how researchers integrate LLMs to overcome challenges inherent in pre-LLM approaches across various tasks, thereby offering a comprehensive understanding of LLMs’ impact in this field. Within each component area, we examine the improvement of methodologies proposed to maximize the utilization of LLMs’ capabilities and enhance the integrity of their responses. Additionally, our survey offers guidelines for prompt engineering in each component area, supplemented with key examples of prompt components, to provide practical insights for researcher entering this field. The core contribution of this paper is to highlight the transformative impact of LLMs in robotics, enabling the development of versatile and intelligent robots. By synthesizing these insights, we aim to guide future research on integrating LLMs into robotic system. 

**Acknowledgements.** This research was supported by the DRB-KAIST SketchTheFuture Research Center and the KAIST Convergence Research Institute Operation Program. 

## **References** 

- [1] Agia C, Jatavallabhula KM, Khodeir M, et al (2022) Taskography: Evaluating robot task planning over large 3d scene graphs. In: Proceedings of the Conference on Robot Learning (CoRL), pp 46–58 

14 

- [2] Anil R, Borgeaud S, Wu Y, et al (2023) Gemini: A family of highly capable multimodal models. arXiv preprint arXiv:231211805 pp 1–62 

- [3] Arkin J, Park D, Roy S, et al (2020) Multimodal estimation and communication of latent semantic knowledge for robust execution of robot instructions. International Journal of Robotics Research (IJRR) 39:1279–1304 

- [4] Axelsson A, Skantze G (2023) Do you follow? a fully automated system for adaptive robot presenters. In: Proceedings of the ACM/IEEE International Conference on Human-Robot Interaction (HRI), pp 102–111 

- [5] Barber DJ, Howard TM, Walter MR (2016) A multimodal interface for real-time soldierrobot teaming. In: Unmanned Systems Technology XVIII, p 98370M 

- [6] Blukis V, Misra D, Knepper RA, et al (2018) Mapping navigation instructions to continuous control actions with position-visitation prediction. In: Proceedings of the Conference on Robot Learning (CoRL), pp 505–518 

- [7] Brohan A, Brown N, Carbajal J, et al (2023) Rt-1: Robotics transformer for real-world control at scale. In: Proceedings of Robotics: Science and Systems (RSS), pp 1–22 

- [8] Brown T, Mann B, Ryder N, et al (2020) Language models are few-shot learners. In: Conference on Neural Information Processing Systems (NeurIPS), pp 1877–1901 

- [9] Cao Y, Lee C (2023) Robot behavior-treebased task generation with large language models. In: Proceedings of the AAAI 2023 Spring Symposium on Challenges Requiring the Combination of Machine Learning and Knowledge Engineering (AAAI-MAKE), pp 1–15 

- [10] Cao Y, Lee CG (2023) Ground manipulator primitive tasks to executable actions using large language models. In: Proceedings of the AAAI Fall Symposium Series, pp 502–507 

- [11] Chattaraman V, Kwon WS, Gilbert JE, et al (2019) Should ai-based, conversational digital assistants employ social- or task-oriented interaction style? a task-competency and reciprocity perspective for older adults. Computers in Human Behavior 90:315–330 

- [12] Chen B, Xia F, Ichter B, et al (2023) Openvocabulary queryable scene representations for real world planning. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), pp 11509– 11522 

- [13] Chen B, Xu Z, Kirmani S, et al (2024) Spatialvlm: Endowing vision-language models with spatial reasoning capabilities. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR) 

- [14] Chen K, Chen JK, Chuang J, et al (2021) Topological planning with transformers for vision-and-language navigation. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp 11276–11286 

- [15] Chen L, Sinavski O, Hünermann J, et al (2024) Driving with llms: Fusing object-level vector modality for explainable autonomous driving. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA) 

- [16] Chen S, Guhur PL, Tapaswi M, et al (2022) Think global, act local: Dual-scale graph transformer for vision-and-language navigation. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp 16537–16547 

- [17] Chen X, Djolonga J, Padlewski P, et al (2023) Pali-x: On scaling up a multilingual vision and language model. arXiv preprint arXiv:230518565 pp 1–30 

- [18] Chen Y, Arkin J, Zhang Y, et al (2023) Autotamp: Autoregressive task and motion planning with llms as translators and checkers. In: Proceedings of the IEEE International Conference on Robotics and Automation 

15 

(ICRA) 

- [19] Chen Y, Zhao C, Yu Z, et al (2023) On the relation between sensitivity and accuracy in in-context learning. In: Findings of the Association for Computational Linguistics: EMNLP 2023, pp 155–167 

- [20] Chen Y, Arkin J, Zhang Y, et al (2024) Scalable multi-robot collaboration with large language models: Centralized or decentralized systems? In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA) 

- [21] Cherakara N, Varghese F, Shabana S, et al (2023) FurChat: An embodied conversational agent using LLMs, combining open and closed-domain dialogue with facial expressions. In: Proceedings of the Annual Meeting of the Special Interest Group on Discourse and Dialogue (SIGDIAL), pp 588–592 

- [22] Cho H, Nam TJ (2023) The story of beau: Exploring the potential of generative diaries in shaping social perceptions of robots. International Journal of Design 17:1–15 

- [23] Cho K, van Merriënboer B, Gulcehre C, et al (2014) Learning phrase representations using RNN encoder–decoder for statistical machine translation. In: Proceedings of the Conference on Empirical Methods in Natural Language Processing (EMNLP), pp 1724–1734 

- [24] Chu K, Zhao X, Weber C, et al (2024) Accelerating reinforcement learning of robotic manipulations via feedback from large language models. In: CoRL Workshop On Bridging the Gap between Cognitive Science and Robot Learning in the Real World: Progresses and New Directions, pp 1–10 

- [25] Dai Y, Peng R, Li S, et al (2024) Think, act, and ask: Open-world interactive personalized robot navigation. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA) 

- [26] Devlin J, Chang MW, Lee K, et al (2019) BERT: Pre-training of deep bidirectional 

transformers for language understanding. In: Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT), pp 4171–4186 

- [27] Di Palo N, Byravan A, Hasenclever L, et al (2023) Towards a unified agent with foundation models. In: ICLR Workshop on Reincarnating Reinforcement Learning, pp 1–14 

- [28] Ding Y, Zhang X, Amiri S, et al (2023) Integrating action knowledge and llms for task planning and situation handling in open worlds. Autonomous Robots 47:981–997 

- [29] Ding Y, Zhang X, Paxton C, et al (2023) Task and motion planning with large language models for object rearrangement. In: Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp 2086–2092 

- [30] Dong C, Li Y, Gong H, et al (2022) A survey of natural language generation. ACM Computing Surveys 55:1–38 

- [31] Driess D, Xia F, Sajjadi MSM, et al (2023) PaLM-e: An embodied multimodal language model. In: Proceedings of the International Conference on Machine Learning (ICML), pp 8469–8488 

- [32] Du Y, Watkins O, Wang Z, et al (2023) Guiding pretraining in reinforcement learning with large language models. In: Proceedings of the International Conference on Machine Learning (ICML), pp 8657–8677 

- [33] Elman JL (1990) Finding structure in time. Cognitive Science 14:179–211 

- [34] Fikes RE, Nilsson NJ (1971) Strips: A new approach to the application of theorem proving to problem solving. Artificial Intelligence 2:189–208 

- [35] Firoozi R, Tucker J, Tian S, et al (2023) Foundation models in robotics: Applications, challenges, and the future. arXiv preprint 

16 

arXiv:231207843 pp 1–33 

- [36] Fisher M, Savva M, Hanrahan P (2011) Characterizing structural relationships in scenes using graph kernels. In: ACM SIGGRAPH Papers, pp 1–12 

- [37] Gao J, Sarkar B, Xia F, et al (2024) Physically grounded vision-language models for robotic manipulation. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA) 

- [38] Garrett CR, Lozano-Pérez T, Kaelbling LP (2020) Pddlstream: Integrating symbolic planners and blackbox samplers via optimistic adaptive planning. In: Proceedings of the International Conference on Automated Planning and Scheduling (ICAPS), pp 440–448 

- [39] Gatt A, Krahmer E (2018) Survey of the state of the art in natural language generation: Core tasks, applications and evaluation. Journal of Artificial Intelligence Research (JAIR) 61:65–170 

- [40] Gopalan N, Arumugam D, Wong LL, et al (2018) Sequence-to-sequence language grounding of non-markovian task specifications. In: Proceedings of Robotics: Science and Systems (RSS), pp 1–10 

- [41] Gu Q, Kuwajerwala A, Jatavallabhula KM, et al (2024) Conceptgraphs: Openvocabulary 3d scene graphs for perception and planning. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA) 

- [42] Guan L, Valmeekam K, Sreedharan S, et al (2023) Leveraging pre-trained large language models to construct and utilize world models for model-based task planning. In: Conference on Neural Information Processing Systems (NeurIPS), pp 79081–79094 

- [43] Guzhov A, Raue F, Hees J, et al (2022) Audioclip: Extending clip to image, text and audio. In: IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp 976–980 

- [44] Ha H, Florence P, Song S (2023) Scaling up and distilling down: Language-guided robot skill acquisition. In: Proceedings of the Conference on Robot Learning (CoRL), pp 3766–3777 

- [45] Helmert M (2006) The fast downward planning system. Journal of Artificial Intelligence Research (JAIR) 26:191–246 

- [46] Hochreiter S, Schmidhuber J (1997) Long short-term memory. Neural Computation 9:1735–1780 

- [47] Hong Y, Zhen H, Chen P, et al (2023) 3d-llm: Injecting the 3d world into large language models. In: Conference on Neural Information Processing Systems (NeurIPS), pp 20482–20494 

- [48] Hong Y, Zheng Z, Chen P, et al (2024) Multiply: A multisensory object-centric embodied large language model in 3d world. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR) 

- [49] Houlsby N, Giurgiu A, Jastrzebski S, et al (2019) Parameter-efficient transfer learning for NLP. In: Proceedings of the International Conference on Machine Learning (ICML), pp 2790–2799 

- [50] Howard T, Stump E, Fink J, et al (2022) An intelligence architecture for grounded language communication with field robots. Field Robotics 2:468–512 

- [51] Hu EJ, Shen Y, Wallis P, et al (2022) LoRA: Low-rank adaptation of large language models. In: Proceedings of the International Conference on Learning Representation (ICLR), pp 1–13 

- [52] Hu H, Chen J, Liu H, et al (2022) Natural language-based automatic programming for industrial robots. Journal of Grid Computing 20:26 

- [53] Hu Y, Lin F, Zhang T, et al (2023) Look before you leap: Unveiling the power of gpt4v in robotic vision-language planning. arXiv 

17 

preprint arXiv:231117842 pp 1–20 

- [54] Hu Y, Xie Q, Jain V, et al (2023) Toward general-purpose robots via foundation models: A survey and meta-analysis. arXiv preprint arXiv:231208782 pp 1–48 

- [55] Huang C, Mees O, Zeng A, et al (2023) Audio visual language maps for robot navigation. In: Proceedings of the International Symposium on Experimental Robotics (ISER), pp 1–8 

- [56] Huang C, Mees O, Zeng A, et al (2023) Visual language maps for robot navigation. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), pp 10608–10615 

- [57] Huang S, Jiang Z, Dong H, et al (2023) Instruct2act: Mapping multi-modality instructions to robotic actions with large language model. arXiv preprint arXiv:230511176 pp 1–21 

- [58] Huang W, Abbeel P, Pathak D, et al (2022) Language models as zero-shot planners: Extracting actionable knowledge for embodied agents. In: Proceedings of the International Conference on Machine Learning (ICML), pp 9118–9147 

- [59] Huang W, Wang C, Zhang R, et al (2023) Voxposer: Composable 3d value maps for robotic manipulation with language models. In: Proceedings of the Conference on Robot Learning (CoRL), pp 540–562 

- [60] Huang W, Xia F, Shah D, et al (2023) Grounded decoding: Guiding text generation with grounded models for embodied agents. In: Conference on Neural Information Processing Systems (NeurIPS), pp 59636–59661 

- [61] Huang W, Xia F, Xiao T, et al (2023) Inner monologue: Embodied reasoning through planning with language models. In: Proceedings of the Conference on Robot Learning (CoRL), pp 1769–1782 

- [62] Hunt W, Godfrey T, Soorati MD (2024) Conversational language models for humanin-the-loop multi-robot coordination. In: International Conference on Autonomous Agents and Multi-Agent Systems (AAMAS) 

- [63] Ichikura A, Kawaharazuka K, Obinata Y, et al (2023) A method for selecting scenes and emotion-based descriptions for a robot’s diary. In: Proceedings of the IEEE International Conference on Robot and Human Interactive Communication (RO-MAN), pp 1683–1688 

- [64] Ichter B, Brohan A, Chebotar Y, et al (2023) Do as i can, not as i say: Grounding language in robotic affordances. In: Proceedings of the Conference on Robot Learning (CoRL), pp 287–318 

- [65] Irfan B, Kuoppamäki SM, Skantze G (2023) Between reality and delusion: Challenges of applying large language models to companion robots for open-domain dialogues with older adults. Research Square preprint pp 1–43 

- [66] Jatavallabhula KM, Kuwajerwala A, Gu Q, et al (2023) Conceptfusion: Open-set multimodal 3d mapping. In: Proceedings of Robotics: Science and Systems (RSS), pp 1–17 

- [67] Jia Z, Liu F, Thumuluri V, et al (2023) Chain-of-thought predictive control. In: ICLR Workshop on Reincarnating Reinforcement Learning, pp 1–16 

- [68] Jiao A, Patel TP, Khurana S, et al (2023) Swarm-gpt: Combining large language models with safe motion planning for robot choreography design. In: NeurIPS Robot Learning Workshop: Pretraining, Fine-Tuning, and Generalization with Large Scale Models, pp 1–10 

- [69] Kaddour J, Harris J, Mozes M, et al (2023) Challenges and applications of large language models. arXiv preprint arXiv:230710169 pp 1–72 

18 

- [70] Kannan SS, Venkatesh VL, Min BC (2024) Smart-llm: Smart multi-agent robot task planning using large language models. arXiv preprint arXiv:230910062 pp 1–8 

- [71] Katara P, Xian Z, Fragkiadaki K (2023) Gen2sim: Scaling up simulation with generative models for robotic skill learning. In: CoRL Workshop on Towards Generalist Robots: Learning Paradigms for Scalable Skill Acquisition, pp 1–13 

- [72] Kerr J, Kim CM, Goldberg K, et al (2023) Lerf: Language embedded radiance fields. In: Proceedings of the International Conference on Computer Vision (ICCV), pp 19729–19739 

- [73] Khoo W, Hsu LJ, Amon KJ, et al (2023) Spill the tea: When robot conversation agents support well-being for older adults. In: Companion of the ACM/IEEE International Conference on Human-Robot Interaction (HRI), pp 178–182 

- [74] Kim D, Kim J, Cho M, et al (2022) Natural language-guided semantic navigation using scene graph. In: Robot Intelligence Technology and Applications (RiTA), pp 148–156 

- [75] Kim D, Kim Y, Jang J, et al (2023) Sggnet2: Speech-scene graph grounding network for speech-guided navigation. In: Proceedings of the IEEE International Conference on Robot and Human Interactive Communication (ROMAN), pp 1648–1654 

- [76] Kim D, Oh N, Hwang D, et al (2024) Lingospace: Language-conditioned incremental grounding for space. In: Proceedings of the AAAI Conference on Artificial Intelligence (AAAI), pp 10314–10322 

- [77] Kumar KN, Essa I, Ha S (2023) Words into action: Learning diverse humanoid behaviors using language guided iterative motion refinement. In: CoRL Workshop on Language and Robot Learning: Language as Grounding, pp 1–11 

- [78] Kwon M, Hu H, Myers V, et al (2024) Toward grounded commonsense reasoning. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA) 

- [79] Kwon T, Di Palo N, Johns E (2023) Language models as zero-shot trajectory generators. In: CoRL Workshop on Language and Robot Learning: Language as Grounding, pp 1–23 

- [80] Lee YK, Jung Y, Kang G, et al (2023) Developing social robots with empathetic non-verbal cues using large language models. In: Proceedings of the IEEE International Conference on Robot and Human Interactive Communication (RO-MAN) 

- [81] Li B, Weinberger KQ, Belongie S, et al (2022) Language-driven semantic segmentation. In: Proceedings of the International Conference on Learning Representation (ICLR), pp 1–13 

- [82] Li J, Li D, Savarese S, et al (2023) BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In: Proceedings of the International Conference on Machine Learning (ICML), pp 19730–19742 

- [83] Li M, Roller S, Kulikov I, et al (2020) Don’t say that! making inconsistent dialogue unlikely with unlikelihood training. In: Proceedings of the Association for Computational Linguistics (ACL), pp 4715–4728 

- [84] Li S, Park D, Sung Y, et al (2021) Reactive task and motion planning under temporal logic specifications. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), pp 12618–12624 

- [85] Li Y, Li J, Fu W, et al (2023) Learning agile bipedal motions on a quadrupedal robot. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA) 

- [86] Liang J, Huang W, Xia F, et al (2023) Code as policies: Language model programs for embodied control. In: Proceedings of the 

19 

IEEE International Conference on Robotics and Automation (ICRA), pp 9493–9500 

- [87] Lin BY, Fu Y, Yang K, et al (2023) Swiftsage: A generative agent with fast and slow thinking for complex interactive tasks. In: Conference on Neural Information Processing Systems (NeurIPS), pp 23813–23825 

- [88] Lin K, Agia C, Migimatsu T, et al (2023) Text2motion: From natural language instructions to feasible plans. Autonomous Robots 47:1345–1365 

- [89] Liu B, Jiang Y, Zhang X, et al (2023) Llm+p: Empowering large language models with optimal planning proficiency. arXiv preprint arXiv:230411477 pp 1–8 

- [90] Liu H, Chen A, Zhu Y, et al (2023) Interactive robot learning from verbal correction. In: CoRL Workshop on Language and Robot Learning: Language as Grounding, pp 1–18 

- [91] Liu JX, Yang Z, Idrees I, et al (2023) Grounding complex natural language commands for temporal tasks in unseen environments. In: Proceedings of the Conference on Robot Learning (CoRL), pp 1084–1110 

- [92] Liu P, Yuan W, Fu J, et al (2023) Pre-train, prompt, and predict: A systematic survey of prompting methods in natural language processing. ACM Computing Surveys 55:1– 35 

- [93] Liu S, Zeng Z, Ren T, et al (2023) Grounding dino: Marrying dino with grounded pretraining for open-set object detection. arXiv preprint arXiv:230305499 pp 1–17 

- [94] Liu Z, Bahety A, Song S (2023) Reflect: Summarizing robot experiences for failure explanation and correction. In: Proceedings of the Conference on Robot Learning (CoRL), pp 3468–3484 

- [95] Ma YJ, Liang W, Wang G, et al (2023) Eureka: Human-level reward design via coding large language models. In: CoRL Workshop on Language and Robot Learning: Language as Grounding, pp 1–45 

- [96] Mandi Z, Jain S, Song S (2024) Roco: Dialectic multi-robot collaboration with large language models. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA) 

- [97] Mavridis N (2015) A review of verbal and non-verbal human–robot interactive communication. Robotics and Autonomous Systems 63:22–35 

- [98] McDermott D, Ghallab M, Howe AE, et al (1998) Pddl–the planning domain definition language. Tech. rep. 

- [99] Mei H, Bansal M, Walter M (2016) Listen, attend, and walk: Neural mapping of navigational instructions to action sequences. In: Proceedings of the AAAI Conference on Artificial Intelligence (AAAI), pp 2772–2778 

- [100] Minderer M, Gritsenko A, Stone A, et al (2022) Simple open-vocabulary object detection. In: Proceedings of the European Conference on Computer Vision (ECCV), pp 728–755 

- [101] Mirchandani S, Xia F, Florence P, et al (2023) Large language models as general pattern machines. In: Proceedings of the Conference on Robot Learning (CoRL), pp 2498–2518 

- [102] Mirjalili R, Krawez M, Burgard W (2023) Fm-loc: Using foundation models for improved vision-based localization. In: Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp 1381–1387 

- [103] Mirjalili R, Krawez M, Silenzi S, et al (2023) Lan-grasp: Using large language models for semantic object grasping. arXiv preprint arXiv:231005239 pp 1–7 

- [104] Mousavian A, Anguelov D, Flynn J, et al (2017) 3d bounding box estimation using deep learning and geometry. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp 7074– 7082 

20 

- [105] Nyga D, Roy S, Paul R, et al (2018) Grounding robot plans from natural language instructions with incomplete world knowledge. In: Proceedings of the Conference on Robot Learning (CoRL), pp 714–723 

- [106] OpenAI (2023) Chatgpt (jan 15 version). https://chat.openai.com/chat, large language model 

- [107] OpenAI, Achiam J, Adler S, et al (2024) Gpt-4 technical report. arXiv preprint arXiv:230308774 pp 1–100 

- [108] Ouyang L, Wu J, Jiang X, et al (2022) Training language models to follow instructions with human feedback. In: Conference on Neural Information Processing Systems (NeurIPS), pp 27730–27744 

- [109] Park J, Lim S, Lee J, et al (2024) Clara: Classifying and disambiguating user commands for reliable interactive robotic agents. IEEE Robotics and Automation Letters (RA-L) 9:1059–1066 

- [110] Patki S, Fahnestock E, Howard TM, et al (2020) Language-guided semantic mapping and mobile manipulation in partially observable environments. In: Proceedings of the Conference on Robot Learning (CoRL), pp 1201–1210 

- [111] Peng S, Genova K, Jiang C, et al (2023) Openscene: 3d scene understanding with open vocabularies. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp 815–824 

- [112] Perez J, Proux DM, Roux C, et al (2023) Larg, language-based automatic reward and goal generation. arXiv preprint arXiv:230610985 pp 1–32 

- [113] Premebida C, Ambrus R, Marton ZC (2018) Intelligent robotic perception systems. In: Applications of Mobile Robots. IntechOpen, chap 6, p 111–127 

- [114] Qian S, Chen W, Bai M, et al (2024) Affordancellm: Grounding affordance from vision language models. arXiv preprint 

arXiv:240106341 pp 1–12 

- [115] Radford A, Wu J, Child R, et al (2019) Language models are unsupervised multitask learners. OpenAI Blog pp 1–24 

- [116] Radford A, Kim JW, Hallacy C, et al (2021) Learning transferable visual models from natural language supervision. In: Proceedings of the International Conference on Machine Learning (ICML), pp 8748–8763 

- [117] Raman SS, Cohen V, Paulius D, et al (2023) CAPE: Corrective actions from precondition errors using large language models. In: CoRL Workshop on Language and Robot Learning: Language as Grounding, pp 1–9 

- [118] Rana K, Haviland J, Garg S, et al (2023) Sayplan: Grounding large language models using 3d scene graphs for scalable task planning. In: Proceedings of the Conference on Robot Learning (CoRL), pp 23–72 

- [119] Reed S, Zolna K, Parisotto E, et al (2022) A generalist agent. Transactions on Machine Learning Research (TMLR) pp 1–42 

- [120] Ren AZ, Dixit A, Bodrova A, et al (2023) Robots that ask for help: Uncertainty alignment for large language model planners. In: Proceedings of the Conference on Robot Learning (CoRL), pp 661–682 

- [121] Roy S, Noseworthy M, Paul R, et al (2019) Leveraging past references for robust language grounding. In: Proceedings of the Conference on Computational Natural Language Learning (CoNLL), pp 430–440 

- [122] Shah D, Osiński B, Ichter B, et al (2023) Lm-nav: Robotic navigation with large pretrained models of language, vision, and action. In: Proceedings of the Conference on Robot Learning (CoRL), pp 492–504 

- [123] Shah R, Martín-Martín R, Zhu Y (2023) Mutex: Learning unified policies from multimodal task specifications. In: Proceedings of the Conference on Robot Learning (CoRL), pp 2663–2682 

21 

- [124] Shao L, Migimatsu T, Zhang Q, et al (2021) Concept2robot: Learning manipulation concepts from instructions and human demonstrations. International Journal of Robotics Research (IJRR) 40:1419–1434 

- [125] Shridhar M, Mittal D, Hsu D (2020) Ingress: Interactive visual grounding of referring expressions. International Journal of Robotics Research (IJRR) 39:217–232 

- [126] Shridhar M, Manuelli L, Fox D (2022) Cliport: What and where pathways for robotic manipulation. In: Proceedings of the Conference on Robot Learning (CoRL), pp 894–906 

- [127] Silver T, Hariprasad V, Shuttleworth RS, et al (2022) PDDL planning with pretrained large language models. In: NeurIPS Workshop on Foundation Models for Decision Making, pp 1–13 

- [128] Singh I, Blukis V, Mousavian A, et al (2023) Progprompt: Generating situated robot task plans using large language models. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), pp 11523–11530 

- [129] Song CH, Wu J, Washington C, et al (2023) Llm-planner: Few-shot grounded planning for embodied agents with large language models. In: Proceedings of the International Conference on Computer Vision (ICCV), pp 2998–3009 

- [130] Song J, Zhou Z, Liu J, et al (2023) Selfrefined large language model as automated reward function designer for deep reinforcement learning in robotics. arXiv preprint arXiv:230906687 pp 1–62 

- [131] Stone A, Xiao T, Lu Y, et al (2023) Openworld object manipulation using pre-trained vision-language models. In: Proceedings of the Conference on Robot Learning (CoRL), pp 3397–3417 

- [132] Sun L, Jha DK, Hori C, et al (2024) Interactive planning using large language models for partially observable robotics tasks. In: 

Proceedings of the IEEE International Conference on Robotics and Automation (ICRA) 

- [133] Tagliabue A, Kondo K, Zhao T, et al (2023) Real: Resilience and adaptation using large language models on autonomous aerial robots. In: CoRL Workshop on Language and Robot Learning: Language as Grounding, pp 1–12 

- [134] Tang Y, Yu W, Tan J, et al (2023) Saytap: Language to quadrupedal locomotion. In: Proceedings of the Conference on Robot Learning (CoRL), pp 3556–3570 

- [135] Tellex S, Gopalan N, Kress-Gazit H, et al (2020) Robots that use language. Annual Review of Control, Robotics, and Autonomous Systems 3:25–55 

- [136] Todorov E, Erez T, Tassa Y (2012) Mujoco: A physics engine for model-based control. In: Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), IEEE, pp 5026–5033 

- [137] Touvron H, Lavril T, Izacard G, et al (2023) Llama: Open and efficient foundation language models. arXiv preprint arXiv:230213971 pp 1–27 

- [138] Touvron H, Martin L, Stone KR, et al (2023) Llama 2: Open foundation and fine-tuned chat models. arXiv preprint arXiv:230709288 pp 1–77 

- [139] Towers M, Terry JK, Kwiatkowski A, et al (2023) Gymnasium. URL https://zenodo. org/record/8127025 

- [140] Valmeekam K, Marquez M, Sreedharan S, et al (2023) On the planning abilities of large language models - a critical investigation. In: Conference on Neural Information Processing Systems (NeurIPS), pp 75993–76005 

- [141] Vaswani A, Shazeer N, Parmar N, et al (2017) Attention is all you need. In: Conference on Neural Information Processing Systems (NeurIPS), pp 1–11 

22 

- [142] Vemprala S, Bonatti R, Bucker A, et al (2023) Chatgpt for robotics: Design principles and model abilities. arXiv preprint arXiv:230617582 pp 1–25 

- [143] Vuong Q, Levine S, Walke HR, et al (2023) Open x-embodiment: Robotic learning datasets and RT-x models. In: CoRL Workshop on Language and Robot Learning: Language as Grounding, pp 1–16 

- [144] Wang T, Li Y, Lin H, et al (2023) Walle: Embodied robotic waiter load lifting with large language model. arXiv preprint arXiv:230815962 pp 1–13 

- [145] Wang Y, Xian Z, Chen F, et al (2023) Robogen: Towards unleashing infinite data for automated robot learning via generative simulation. arXiv preprint arXiv:231101455 pp 1–39 

- [146] Wang YJ, Zhang B, Chen J, et al (2023) Prompt a robot to walk with large language models. arXiv preprint arXiv:230909969 pp 1–8 

- [147] Wang Z, Cai S, Liu A, et al (2023) Describe, explain, plan and select: Interactive planning with llms enables open-world multi-task agents. In: Conference on Neural Information Processing Systems (NeurIPS), pp 34153–34189 

- [148] Wei J, Tay Y, Bommasani R, et al (2022) Emergent abilities of large language models. Transactions on Machine Learning Research (TMLR) pp 1–30 

- [149] Wei J, Wang X, Schuurmans D, et al (2022) Chain-of-thought prompting elicits reasoning in large language models. In: Conference on Neural Information Processing Systems (NeurIPS), pp 24824–24837 

- [150] White J, Fu Q, Hays S, et al (2023) A prompt pattern catalog to enhance prompt engineering with chatgpt. arXiv preprint arXiv:230211382 pp 1–19 

representations from clip. In: IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp 4563–4567 

   - [152] Wu J, Antonova R, Kan A, et al (2023) Tidybot: personalized robot assistance with large language models. Autonomous Robots 47:1087–1102 

   - [153] Xia W, Wang D, Pang X, et al (2024) Kinematic-aware prompting for generalizable articulated object manipulation with llms. In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA) 

   - [154] Xie T, Zhao S, Wu CH, et al (2024) Text2reward: Automated dense reward function generation for reinforcement learning. In: Proceedings of the International Conference on Learning Representation (ICLR) 

   - [155] Xie Y, Yu C, Zhu T, et al (2023) Translating natural language to planning goals with large-language models. arXiv preprint arXiv:230205128 pp 1–15 

   - [156] Xu J, Jin S, Lei Y, et al (2023) Reasoning tuning grasp: Adapting multi-modal large language models for robotic grasping. In: Proceedings of the Conference on Robot Learning (CoRL), pp 1–13 

   - [157] Yamazaki T, Yoshikawa K, Kawamoto T, et al (2023) Building a hospitable and reliable dialogue system for android robots: a scenario-based approach with large language models. Advanced Robotics 37:1364–1381 

   - [158] Yang J, Chen X, Qian S, et al (2023) LLM-grounder: Open-vocabulary 3d visual grounding with large language model as an agent. In: CoRL Workshop on Language and Robot Learning: Language as Grounding, pp 1–8 

   - [159] Yang S, Liu J, Zhang R, et al (2023) Lidarllm: Exploring the potential of large language models for 3d lidar understanding. arXiv preprint arXiv:231214074 pp 1–15 

- [151] Wu HH, Seetharaman P, Kumar K, et al (2022) Wav2clip: Learning robust audio 

23 

- [160] Yang Z, Raman SS, Shah A, et al (2023) Plug in the safety chip: Enforcing constraints for LLM-driven robot agents. In: CoRL Workshop on Language and Robot Learning: Language as Grounding, pp 1–15 

   - [170] Zitkovich B, Yu T, Xu S, et al (2023) Rt-2: Vision-language-action models transfer web knowledge to robotic control. In: Proceedings of the Conference on Robot Learning (CoRL), pp 2165–2183 

- [161] Yu W, Gileadi N, Fu C, et al (2023) Language to rewards for robotic skill synthesis. In: Proceedings of the Conference on Robot Learning (CoRL), pp 374–404 

- [162] Yu Y, Zhang Q, Li J, et al (2024) Affordable generative agents. arXiv preprint arXiv:240202053 pp 1–20 

- [163] Zeng A, Attarian M, Ichter B, et al (2022) Socratic models: Composing zero-shot multimodal reasoning with language. In: Proceedings of the International Conference on Learning Representation (ICLR), pp 1–35 

- [164] Zeng F, Gan W, Wang Y, et al (2023) Large language models for robotics: A survey. arXiv preprint arXiv:231107226 pp 1–19 

- [165] Zeng Y, Xu Y (2023) Learning reward for physical skills using large language model. In: CoRL Workshop on Language and Robot Learning: Language as Grounding, pp 1–22 

- [166] Zhang H, Du W, Shan J, et al (2024) Building cooperative embodied agents modularly with large language models. In: Proceedings of the International Conference on Learning Representation (ICLR) 

- [167] Zhao WX, Zhou K, Li J, et al (2023) A survey of large language models. arXiv preprint arXiv:230318223 pp 1–124 

- [168] Zhao X, Li M, Weber C, et al (2023) Chat with the environment: Interactive multimodal perception using large language models. In: Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp 3590–3596 

- [169] Zhao Z, Lee WS, Hsu D (2023) Large language models as commonsense knowledge for large-scale task planning. In: Conference on Neural Information Processing Systems (NeurIPS), pp 31967–31987 

24 

