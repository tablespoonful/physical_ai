---
title: "Pedagogical Alignment for Vision-Language-Action Models: A Comprehensive Framework for Data, Architecture, and Evaluation in Education"
date: "2026-01-20"
authors: "Unggi Lee; Jahyun Jeong; Sunyoung Shin; Haeun Park; Jeongsu Moon; Youngchang Song"
url: https://arxiv.org/abs/2601.13876
pdf: https://arxiv.org/pdf/2601.13876
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.13876)** / [論文ページ](https://arxiv.org/abs/2601.13876)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Pedagogical Alignment for Vision-Language-Action Models: A Comprehensive Framework for Data, Architecture, and Evaluation in Education** 

**Unggi Lee**<sup>1</sup><sup>_†_</sup> , **Jahyun Jeong**<sup>2</sup><sup>_†_</sup> , **Sunyoung Shin**<sup>2</sup><sup>_†_</sup> , **Haeun Park**<sup>3</sup><sup>_†_</sup> , **Jeongsu Moon**<sup>1</sup> **Youngchang Song**<sup>1</sup> , **Jaechang Shim**<sup>1</sup> , **JaeHwan Lee**<sup>1</sup> , **Yunju Noh**<sup>1</sup> , **Seungwon Choi**<sup>1</sup> **Ahhyun Kim**<sup>1</sup> , **TaeHyeon Kim**<sup>1</sup> , **Kyungtae Joo**<sup>1</sup> , **Taeyeong Kim**<sup>1</sup><sup>_†_</sup> and **Gyeonggeon Lee**<sup>4</sup><sup>_†_</sup> 

1Chosun University 2Seoul National University 

3Korea Institute for Curriculum and Evaluation 4Nanyang Technological University **Corresponding Authors (†, contact emails):** codingchild@korea.ac.kr, gyeonggeon.lee@nie.edu.sg 

## **Abstract** 

Science demonstrations are important for effective STEM education, yet teachers face challenges in conducting them safely and consistently across multiple occasions, where robotics can be helpful. However, current Vision-Language-Action (VLA) models require substantial computational resources and sacrifice language generation capabilities to maximize efficiency, making them unsuitable for resource-constrained educational settings that require interpretable, explanation-generating systems. We present _Pedagogical VLA Framework_ , a framework that applies pedagogical alignment to lightweight VLA models through four components: text healing to restore language generation capabilities, large language model (LLM) distillation to transfer pedagogical knowledge, safety training for educational environments, and pedagogical evaluation adjusted to science education contexts. We evaluate _Pedagogical VLA Framework_ across five science demonstrations spanning physics, chemistry, biology, and earth science, using an evaluation framework developed in collaboration with science education experts. Our evaluation assesses both task performance (success rate, protocol compliance, efficiency, safety) and pedagogical quality through teacher surveys and LLM-as-Judge assessment. We additionally provide qualitative analysis of generated texts. Experimental results demonstrate that _Pedagogical VLA Framework_ achieves comparable task performance to baseline models while producing contextually appropriate educational explanations. 

## **1 Introduction** 

Science demonstrations, where teachers perform experiments while students observe, play a crucial role in STEM education by enabling students to witness scientific phenomena closely and connect theoretical concepts to real-world applications [Hofstein and Lunetta, 2004]. However, conducting 


Figure 1: Robot science demonstrations with pedagogically-aligned explanations connecting actions to learning objectives ( _left_ , _center_ ), and safety-aware behavior enabling immediate halt upon detecting human presence in the workspace ( _right_ ). 

these demonstrations poses challenges for teachers, including preparation time, safety concerns when handling hazardous materials, and the difficulty of maintaining consistency across multiple class sessions [Singer _et al._ , 2006]. 

Robotics has been applied to education primarily through social robots serving as learning companions and rule-based systems for programming education [Belpaeme and others, 2018; Spolaˆor and others, 2025]. These approaches have demonstrated positive effects on student engagement, but they rely on pre-programmed behaviors and lack flexibility to perform complex physical tasks such as science demonstrations. 

Recent advances in Vision-Language-Action (VLA) models offer new possibilities for educational robotics [Brohan and others, 2023; Kim and others, 2024]. VLA models integrate visual perception, language understanding, and action generation, enabling robots to perform complex manipulation tasks starting from natural language instructions. However, VLA research have focused exclusively on general manipulation tasks [Huang and others, 2025], with almost no consideration of educational contexts. To address this gap, we apply VLA models to real robots in education, selecting science demonstrations as the target domain due to their need for precise manipulation, safety awareness, and pedagogical explanation. 

We identifed four critical gaps in applying VLA models to 


Figure 2: Overview of the Pedagogical VLA Framework. The framework integrates data collection via teleoperation with LLM-generated pedagogical text, extends SmolVLA with a text decoder trained for safety awareness and pedagogical alignment, and evaluates both task execution and text quality through human experts and LLM-as-Judge. 

education: (1) state-of-the-art VLA models require substantial computing resources impractical for typical classrooms, necessitating lightweight alternatives; (2) most VLA models sacrifice language generation for efficiency, but educational contexts require models that explain their actions for interpretability; and (3) existing VLA models lack safety mechanisms for settings where students may enter the workspace, and (4) evaluation frameworks neglect pedagogical quality. 

To address these gaps, we propose _Pedagogical VLA Framework_<sup>1</sup> , which applies pedagogical alignment to lightweight VLA models through four components: _text healing_ to restore language generation capabilities, _Large Language Model (LLM) distillation_ to transfer pedagogical knowledge from LLMs, _safety training_ to halt operation when students enter the workspace, and _pedagogical evaluation_ for multi-dimensional assessment of both task performance and educational quality. We implement this framework by extending SmolVLA [HuggingFace, 2024] with a text decoder module that generates pedagogically-aligned explanations during task execution. 

### **1.1 Contributions** 

- We propose _Pedagogical VLA Framework_ , which applies VLA models to educational contexts based on five design principles derived from educational robotics and 

> 1https://anonymous.4open.science/r/pedagogical ~~v~~ la submission-517D/README.md 

pedagogical alignment research. 

- We introduce text healing and pedagogical data distillation to achieve interpretability, transparency, and pedagogical alignment in lightweight VLA models. 

- We design a multi-layered evaluation framework that assesses both robot task performance and educational usability through quantitative metrics, teacher surveys, and LLM-as-Judge. 

## **2 Pedagogical VLA Framework** 

### **2.1 Overview** 

Drawing from educational robotics [Belpaeme and others, 2018; Spolaˆor and others, 2025] and pedagogical alignment research [Lee _et al._ , 2025], we identify five design principles for applying VLA models to education: lightweight-first, interpretability through language, safety-by-design, pedagogyaligned, and multi-dimensional evaluation (Table 1). 

Based on these principles, _Pedagogical VLA Framework_ can be examined from three dimensions: Data, Architecture, and Evaluation (See figure 2). The Data dimension addresses how to collect and annotate training data with pedagogical content through LLM distillation and safety intervention scenarios. The Architecture dimension describes how to restore language generation capabilities to lightweight VLA models through text healing. The Evaluation dimension defines how to assess both task performance and educational usabil- 

Table 1: Design principles for pedagogical VLA derived from educational robotics and pedagogical alignment research. 

|Principle|Description|
|---|---|
|Lightweight-First|Resource-constrained deployment|
|Interpretability|Natural language explanations|
|Safety-by-Design|Integrated safety mechanisms|
|Pedagogy-Alignment|Connection to learning objectives|
|Multi-dimensional|Task and pedagogical evaluation|


ity through quantitative metrics and teacher surveys. Moreover, we analyze generated text with exploratory data analsys (EDA) and ground theory [Strauss and Corbin, 1998] 

### **2.2 Data** 

#### **LLM Distillation for Pedagogical Text** 

Educational explanations require domain knowledge about science concepts, pedagogical strategies, and curriculum alignment that cannot be learned from action demonstrations alone. We address this through LLM distillation, transferring pedagogical knowledge from LLMs to our lightweight model. 

SmolVLA employs action chunking, predicting 50 actions per inference. We align text generation with this chunking by generating one pedagogical annotation per action chunk using GPT-4o. The annotations follow a structured format: 

[Stage] Current demonstration phase [Action] Robot’s current action description [Safety Status] Normal / Stop - Human detected **Learning Focus** : Key concept being demonstrated **Connection to learning goal** : How this step relates to learning objectives **Next** : Upcoming action or instruction 

We construct few-shot prompts with exemplars covering idle states, active manipulation, and safety intervention scenarios. This ensures the distilled model learns to generate appropriate responses across diverse situations. 

#### **Safety Intervention Data** 

Educational environments present unique safety challenges as students may unexpectedly reach into the robot’s workspace [Robinette _et al._ , 2020; Lasota _et al._ , 2021]. Unlike industrial settings with physical barriers, classroom deployments must handle such situations gracefully. 

We collect episodes where human hands enter the workspace during experiments. The robot outputs zerovelocity commands and generates safety-focused text annotations. This data teaches the model to detect human presence, halt immediately, explain the intervention, and wait for clearance before resuming. 

### **2.3 Architecture** 

#### **Input Representation** 

The model receives three types of inputs at each timestep _t_ . Visual observations _It_<sup>wrist</sup> _, It_<sup>top</sup> _∈_ R<sup>_H×W ×_3</sup> are RGB images from wrist-mounted and top-view cameras ( _H_ = 480, _W_ = 640). These provide complementary perspectives 

where the wrist camera captures fine manipulation details while the top-view camera provides global scene context. Proprioceptive state _st ∈_ [ _−_ 100 _,_ 100]<sup>6</sup> is a 6-dimensional vector representing normalized joint positions. Task instruction _ℓ_ = ( _w_ 1 _, w_ 2 _, . . . , wL_ ) is a token sequence describing the experimental task, e.g., _“Hold stick, tap powder, hold over blue 3s, return to cup. Stop if hand detected.”_ 

#### **Base Model** 

We build upon SmolVLA [HuggingFace, 2024], a 450M parameter lightweight VLA derived from the SmolVLM visionlanguage model. SmolVLA inherits SmolVLM’s vision encoder and text model layers but removes the language model head to prioritize action prediction efficiency. The architecture processes inputs as follows. 

The vision encoder _f_ vision (SigLIP, frozen) extracts visual features: 


The text model layers _f_ backbone (frozen) fuse visual features, proprioceptive state, and language instruction into a multimodal representation: 


The action expert _f_ action (trainable) predicts action chunks using flow matching: 


where _at ∈_ R<sup>_C×D_</sup> with chunk size _C_ = 50 and action dimension _D_ = 6, and _h_<sup>expert</sup> _t_ denotes the expert’s hidden states. 

#### **Text Healing** 

While SmolVLA’s removal of the language model head improves efficiency, it eliminates interpretability through language output. Text healing restores this capability by reconstructing the text generation pathway using three components. 

First, we extract context from the action expert’s hidden states through mean pooling: 


Second, a projection layer transforms the expert dimension to the language model dimension: 


where _W_ proj _∈_ R<sup>_d_hidden</sup><sup>_×d_expert</sup> is newly trained. 

Third, we restore text generation using components initialized from SmolVLM: a text decoder _f_ dec (12 transformer layers, trainable) and a language model head _W_ lm (pretrained weights, trainable): 


The generated sequence _y_ = ( _y_ 1 _, . . . , yT_ ) describes the demonstration stage, current action, safety status, learning focus, and upcoming steps. The text decoder is trained on pedagogical annotations from LLM distillation (Section 2.2.1) and safety intervention data (Section 2.2.2), enabling the model to produce both educationally meaningful explanations and appropriate safety responses 

#### **Training Objective** 

The model is trained with a combined loss function: 

## **3 Experiments** 

### **3.1 Experimental Settings** 

#### **Demonstration Tasks** 


where 


is the mean squared error between predicted and groundtruth actions, and 

Two science education experts within our research team selected five demonstration tasks most suitable for robotassisted demonstrations in K-12 science education. The selection criteria included curriculum relevance, procedural clarity, and safety considerations. Table 3 summarizes the selected tasks spanning major STEM disciplines. 

Table 3: Overview of demonstration tasks selected based on curriculum relevance, procedural clarity, and safety considerations. 


is the cross-entropy loss for text generation. The weight _λ ∈_ [0 _._ 01 _,_ 1 _._ 0] balances action accuracy and text quality; we set _λ_ = 0 _._ 1 based on preliminary experiments. 

### **2.4 Evaluation** 

|Domain|Demonstration|Description|
|---|---|---|
|Physics|Electromagnetic Induction|Magnet insertion/withdrawal through<br>coil|
|Chemistry|Flame Test|Wire coating, heating to observe emis-<br>sion colors|
|Biology|Yeast Fermentation|Dispensing, sealing flasks to observe<br>CO2|
|Earth Sci.|Rock Classification|Acid application to identify carbonate|
|Lab Support|Agar Plate Prep.|Pouring agar into petri dishes|


#### **Quantitative Metrics** 

We adopt evaluation metrics from recent laboratory automation benchmarks [AutoBio Team, 2024; Chemistry3D Team, 2025; LabBench Team, 2025]. Table 2 summarizes the metrics organized into three categories: task execution, text quality, and usability. For each task, we run 10 episodes and average the scores. Task execution metrics are rated by two human experts who evaluate independently and then resolve disagreements through discussion. Text quality is assessed using LLM-as-Judge with GPT-4o. Usability is evaluated by 2 science education experts using a 20-item Likert scale questionnaire (Appendix E). Detailed evaluation criteria are provided in Appendix A and the rubric in Appendix B. 

Table 2: Quantitative evaluation metrics adapted from laboratory automation benchmarks to assess both task performance and educational usability. 

|Group|Category|Metrics|Eval.|Scale|
|---|---|---|---|---|
|Task<br>Execution|Task<br>Success<br>Protocol<br>Efficiency<br>Safety|Grip, placement, task-specific<br>Step order, condition compli-<br>ance<br>Unnecessary action rate<br>Collision, drop, jerk, human<br>detection|Human<br>Human<br>Human<br>Human|Acc.<br>Acc.<br>Acc.<br>Acc.|
|Text<br>Quality|–|Relevance, pedagogical value,<br>safety comm., fluency|LLM|1-5|
|Usability|–|Effectiveness,<br>efficiency,<br>safety,<br>sustainability,<br>enjoy-<br>ment|Human|1-5|


#### **Qualitative Assessment** 

Two science education experts record narrative observations during the quantitative evaluation process. These observations capture contextual factors, failure modes, and pedagogical insights that numerical metrics cannot fully represent. We analyze these expert notes using thematic synthesis to identify patterns across demonstrations and models. 

#### **Data Collection** 

We used the SO-101 robot arm, a low-cost 6-DOF manipulator with Feetech STS3215 servo motors (Appendix H). We collected dual-camera video (wrist and top view) and action trajectories through teleoperation for each task. For each demonstration, we collected both normal execution episodes and safety intervention scenarios where a human hand enters the workspace. Text annotations were generated separately: simple action descriptions for Text-SmolVLA baseline, and pedagogical explanations via GPT-4o with task-specific fewshot prompts for Pedagogical VLA. Table 4 summarizes the dataset statistics. 

Table 4: Dataset statistics showing episode distribution across safety intervention and normal conditions. All data collected at 30 fps with dual-camera setup. 

|Demonstration|Safety Intervention|Normal|Total|
|---|---|---|---|
|EM Induction|20|60|80|
|Flame Test|20|60|80|
|Yeast Fermentation|22|100|122|
|Rock Classification|30|100|130|
|Agar Plate Prep.|30|130|160|


#### **Baseline Models** 

We compare _Pedagogical VLA Framework_ against three baselines. ACT [Zhao and others, 2023] is the Action Chunking Transformer, a state-of-the-art imitation learning method without language capabilities. SmolVLA [HuggingFace, 2024] is a lightweight VLA model that conditions on language instructions but does not generate text outputs. TextSmolVLA is SmolVLA augmented with our text decoder but trained to generate simple action descriptions (e.g., _“Picking up the beaker”_ ) rather than pedagogical explanations, serving as an ablation to isolate the effect of LLM distillation. 

#### **Training Details** 

All models are trained for 100,000 steps with batch size 32. The text generation model for distillation is GPT-4o. The text loss weight _λ_ is set to 0.1, maximum text length to 128 tokens, and text decoder depth to 12 layers. 

### **3.2 Experiment Results** 

#### **Quantitative Evaluation** 

Table 5 presents quantitative evaluation results across three categories. Task execution metrics (Task Success, Protocol, Efficiency, Safety) are rated by human experts as accuracy (%). Text quality is assessed by LLM-as-Judge on a 1-5 scale. Usability is evaluated by 2 science teachers (each with _>_ 5 years experience) using a 5-point Likert scale. 

For task execution, ACT achieves the highest scores across Task Success (78%), Protocol Order (80%), and Condition Compliance (64%), demonstrating the effectiveness of action-focused imitation learning without text generation overhead. SmolVLA shows moderate performance (49% task success), while Text-SmolVLA and Pedagogical VLA exhibit lower task success (38% and 29%) due to the additional text generation objective competing for model capacity. Notably, VLA models with text output achieve higher Human Detection Stop rates (60–78%) compared to ACT (20%), suggesting that language conditioning improves safety response learning. Pedagogical VLA achieves the highest Manipulation Safety score (90%), computed as 100% minus the average of collision, drop, and jerk event rates. 

For text quality evaluation, we used GPT-4o-mini as an LLM-as-Judge to assess 1,000 generated utterances (50 samples per condition) across four metrics. Pedagogical VLA significantly outperformed Text-SmolVLA in Relevance (3.7 vs 2.3), Pedagogical Value (3.5 vs 1.3), and Safety Communication (2.7 vs 1.0), with all differences statistically significant ( _p_ ¡ .001). Text-SmolVLA achieved higher Fluency scores (3.9 vs 2.6) because its simple action descriptions contain fewer grammatical errors than the longer pedagogical explanations. These results demonstrate that LLM distillation successfully transfers educational scaffolding capabilities to the lightweight model. Detailed results by experiment and condition are provided in Appendix C. 

#### **Qualitative Evaluation** 

Two experts within our research team provided narrative observations. A recurring theme was safety detection: evaluators noted “ACT lacks safety response,” while VLA models’ detection required close proximity, with one noting “if the robot only stops when hands are very close, it seems meaningless.” 

Evaluators identified a monitoring burden when success rates were low: “If the robot arm frequently fails, I would have to continuously monitor it. Then I cannot focus on students.” This was amplified for liquid-handling tasks, where “solution spillage frequency is very high.” 

Despite challenges, evaluators recognized unique value. For hazardous experiments, “significant time is spent on safety instructions; this time can be reduced” by robots. They appreciated fine motor capabilities: “The robot performed well at fine gap adjustments required for dropper use,” but 

cautioned that reliability must improve before classroom deployment. 

## **4 Generated Text Analysis** 

### **4.1 Codebook Development** 

We developed a codebook for analyzing pedagogical text outputs following grounded theory methodology [Strauss and Corbin, 1998]. Initial codes were drafted based on established science education frameworks: scaffolding theory [Van de Pol _et al._ , 2010], the BSCS 5E instructional model [Bybee _et al._ , 2006], inquiry-based science education [van Uum _et al._ , 2021; Petersen, 2022], and laboratory instruction research [Hofstein and Lunetta, 2004; Millar, 2004; Singer _et al._ , 2006]. Two researchers then independently reviewed model-generated text outputs for each episode, iteratively refining codes through discussion until reaching consensus. 

Table 6 presents the final codebook with six categories spanning conceptual, procedural, inquiry, affective, safety, and technical dimensions. 

Table 6: Codebook for pedagogical text analysis developed through grounded theory methodology based on established science education frameworks. 

|Category|Code|Definition|
|---|---|---|
|Conceptual|EXP-GOAL<br>OBS-CONCEPT|States learning objective or what will be ver-<br>ified<br>Connects observations to scientific concepts|
||PROC-GUIDE|Guidance on experimental procedures|
|Procedural|EQUIP-OP|Instructions for equipment operation|
||PRECAUTION|Emphasis on accuracy/reliability precautions|
||HYPOTHESIS|Predictions about experiment results|
|Inquiry|VAR-CTRL<br>RESULT-OBS|Explains variable control rationale<br>Guidance for observing results|
||RESULT-INT|Interprets results or guides conclusions|
|Affective|AFF-SUPPORT|Addresses learner anxiety or motivation|
|Safety|SAFETY-MGT|Emphasizes safety to prevent accidents|
|Technical|TECH-CAP|Highlights robotic system capabilities|


### **4.2 Quantitative Analysis** 

We classified all generated text using GPT-4o-mini, measuring character counts to account for length differences between models (Figure 3). Pedagogical VLA generated 90.8% of total characters, with 99.1% classified as educational scaffolding. Text-SmolVLA generated 9.2%, with 99.9% classified as Technical Execution, demonstrating effective pedagogical knowledge transfer through LLM distillation. 

The _left_ panel of Figure 4 shows how scaffolding subcategory patterns vary across experiments. EM Induction emphasizes Experiment Goal (52%) and Observation-Concept Connection (40%), reflecting the need to explain electromagnetic principles. Rock Classification shows 90% Procedure Guidance, emphasizing step-by-step instructions for acid application and observation. These results suggest that Pedagogical VLA adapts its scaffolding strategy to match the pedagogical requirements of each experiment. 

The _center_ panel of Figure 4 reveals safety awareness patterns across experiments and hand conditions. When a human hand entered the robot workspace, Safety Management 

Table 5: Quantitative evaluation results. Gray indicates non-text models; <mark>Blue</mark> indicates text-generating models. Task execution metrics are in % (higher is better), except Eff. _↓_ (lower is better). Det. is Human Detection Stop Rate; Manip. is Manipulation Safety (100% _−_ avg. of collision, drop, jerk rates). Text Quality and Usability are on 1-5 scale. Results averaged over 5 experiments and 10 episodes per task. 

|||T|ask Exec|ution (%|)||Te|xt Qua|lity (1-|5)||Us|ability (|1-5)||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Task|Prot|ocol||Sa|fety||||||||||
|Model|Succ.|Order|Cond.|Eff._↓_|Det.|Manip.|Rel.|Ped.|Safe|Flu.|Eff.|Effi.|Safe|Sust.|Enj.|
|_Non-text Models_||||||||||||||||
|ACT|**78**|**80**|**64**|**26**|20|80|–|–|–|–|**3.7**|**4.2**|**3.2**|**3.8**|**4.9**|
|SmolVLA|49|42|31|52|**78**|76|–|–|–|–|2.5|2.8|**3.2**|2.8|4.1|
|_Text-generating Models_||||||||||||||||
|Text-SmolVLA|**38**|**28**|20|**40**|**78**|85|2.3|1.3|1.0|**3.9**|**2.8**|**3.3**|**3.3**|**3.1**|3.5|
|Pedagogical VLA (Ours)|29|22|**24**|48|60|**90**|**3.7**|**3.5**|**2.7**|2.6|2.6|3.1|3.2|**3.1**|**3.8**|


Figure 3: Descriptive statistics of generated text. The _left_ panel shows average text length by model, where Pedagogical VLA generates 10.2 _×_ longer utterances (697 vs 68 characters). The _center_ panel compares text volume by experiment between Pedagogical VLA (blue) and Text-SmolVLA (orange). The _right_ panel shows Pedagogical VLA category distribution with Procedural Support (68.9%) and Conceptual Support (28.9%) as dominant categories. 

comprised 2.29% of generated text compared to 0.39% without hand presence (Odds Ratio = 5.49, _p_ ¡ .001). Most experiments show reactive safety behavior, generating safety utterances only when a hand enters the workspace. In contrast, Flame Test exhibits inherent safety awareness, producing safety content even without hand intervention (3.2% without hand, 5.3% with hand), suggesting the model acquired prior knowledge about experiment-specific hazards through distillation. 

The _right_ panel of Figure 4 shows keyword frequency patterns across experiments. EM Induction shows high frequency of learning-related keywords, reflecting its conceptual focus. Flame Test emphasizes safety-related terms. These patterns demonstrate that Pedagogical VLA generates contextually appropriate vocabulary aligned with each experiment’s pedagogical goals. 

### **4.3 Qualitative Analysis** 

Manual coding of representative outputs reveals distinct scaffolding patterns. Pedagogical VLA generates conceptual support linking observations to scientific principles [Van de Pol _et al._ , 2010]: e.g., _“Helps visualize how consistent motions affect the induced voltage, reinforcing electromagnetic induction.”_ It also provides safety scaffolding [Hofstein and Lunetta, 2004]: e.g., _“Maintain a safe distance from automated equipment.”_ In contrast, Text-SmolVLA produces 

only technical execution descriptions across all experiments: e.g., _“The robot is pouring blue liquid from a beaker into a flask”_ and _“The robot is dispensing a clear liquid from a pipette onto a rock.”_ 

This pattern aligns with scaffolding theory’s distinction between cognitive and procedural support [Van de Pol _et al._ , 2010]. Pedagogical VLA provides cognitive scaffolding through concept connections, while Text-SmolVLA’s outputs function as mere action narration without educational value. The structured format of Pedagogical VLA outputs, including Learning Focus and Connection to Learning Goal, enables systematic delivery of pedagogical content synchronized with robot actions. 

## **5 Ablation Study** 

### **5.1 Text Decoder Depth** 

We vary the number of transformer layers in the text decoder module (4, 8, 12 layers) while keeping other hyperparameters fixed. Results in Table 7 show that shallower decoders achieve substantially higher action success rates (80% for 4 layers vs. 30% for 12 layers), while text quality peaks at intermediate depth (8 layers). This suggests that excessive decoder capacity may interfere with action prediction while providing diminishing returns for text generation. The 4-layer configuration represents a Pareto-optimal choice when action 


Figure 4: Main analysis results. The _left_ panel shows experiment-specific subcategory patterns where EM Induction emphasizes Experiment Goal (52%) and Observation-Concept (40%), while Rock Classification emphasizes Procedure Guidance (90%). The _center_ panel presents Safety Management by experiment and hand condition, revealing inherent safety awareness in Flame Test (3.2% without hand) versus reactive safety in other experiments (0% without hand). The _right_ panel displays keyword frequency patterns by experiment showing distinct pedagogical emphases across tasks. 

#### reliability is prioritized. 

## **6 Related Work** 

Table 7: Effect of text decoder depth on the trade-off between action success and text quality. Shallow decoders favor action success; intermediate depth optimizes text quality. 

|Decoder|Text|Action|Time|Success|
|---|---|---|---|---|
|Layers|Quality (_↑_)|Success (_↑_)|(s) (_↓_)|Time (s) (_↓_)|
|4|2.41|**80**|35.5|37.9|
|8|**2.43**|40|32.5|**37.2**|
|12|2.32|30|**25.6**|37.7|


### **5.2 Text Loss Weight** 

We examine the effect of the text loss weight _λ_ on the balance between action accuracy and text quality. As shown in Table 8, lower _λ_ values strongly favor action success (60% at _λ_ =0.005 vs. 30% at _λ_ =0.05), while higher values improve text quality (2.63 vs. 2.47). This trade-off reflects the competing objectives in the joint loss function: emphasizing text generation diverts model capacity from action prediction. Notably, successful trials with higher _λ_ complete faster (38.7s vs. 44.2s), suggesting that better verbal guidance may improve execution efficiency when tasks succeed. The choice of _λ_ thus depends on deployment priorities along the Pareto frontier. 

Table 8: Effect of text loss weight _λ_ on balancing competing objectives in the joint loss function. Lower _λ_ favors action success; higher _λ_ improves text quality. 

|_λ_|Text|Action|Time|Success|
|---|---|---|---|---|
||Quality (_↑_)|Success (_↑_)|(s) (_↓_)|Time (s) (_↓_)|
|0.005|2.47|**60**|36.9|44.2|
|0.01|2.43|50|35.0|40.0|
|0.05|**2.63**|30|**27.9**|**38.7**|


Educational robotics research has focused on robots as learning companions or programming platforms [Papert, 1980; Belpaeme and others, 2018], while laboratory automation benchmarks [AutoBio Team, 2024; LabBench Team, 2025] address robotic tasks without educational contexts. However, these approaches have not yet leveraged VLA models, which represent a paradigm shift in robot learning by unifying perception, language understanding, and action generation within single architectures. RT-2 [Brohan and others, 2023] demonstrated that large vision-language models can be finetuned for robotic control with impressive generalization, OpenVLA [Kim and others, 2024] introduced an open-source alternative, and SmolVLA [HuggingFace, 2024] showed that competitive performance is achievable at smaller scales. 

Existing VLA models focus primarily on action generation, often sacrificing language output capabilities to improve efficiency. Our work addresses this limitation through text healing, restoring language generation to lightweight VLA models while adding pedagogical alignment through LLM distillation, bridging the gap between educational robotics and VLA research. 

## **7 Conclusion** 

We presented Pedagogical VLA Framework for science education robotics. The framework restores language generation to lightweight VLA models through text healing, transfers pedagogical knowledge through LLM distillation, and ensures classroom safety through intervention training. Experiments across five science domains demonstrate that Pedagogical VLA achieves comparable task performance while generating contextually appropriate educational explanations with explicit learning objectives and safety guidance. We release our model and dataset to support further research at the intersection of robotics and education. 

## **References** 

- [AutoBio Team, 2024] AutoBio Team. Autobio: A benchmark for robotic biology labs. _arXiv preprint arXiv:2406.08160_ , 2024. 

- [Belpaeme and others, 2018] Tony Belpaeme et al. Social robots for education: A review. _Science Robotics_ , 3(21), 2018. 

- [Brohan and others, 2023] Anthony Brohan et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- [Bybee _et al._ , 2006] Rodger W Bybee, Joseph A Taylor, April Gardner, Pamela Van Scotter, Janet Carlson Powell, Anne Westbrook, and Nancy Landes. The BSCS 5E instructional model: Origins and effectiveness. Technical report, BSCS, Colorado Springs, CO, 2006. 

- [Chemistry3D Team, 2025] Chemistry3D Team. Chemistry3d: Robotic interaction benchmark for chemistry experiments. _arXiv preprint arXiv:2505.14030_ , 2025. 

- [Hofstein and Lunetta, 2004] Avi Hofstein and Vincent N Lunetta. The laboratory in science education: Foundations for the twenty-first century. _Science Education_ , 88(1):28– 54, 2004. 

- [Huang and others, 2025] Yanjiang Huang et al. Vision language action models in robotic manipulation: A systematic review. _arXiv preprint arXiv:2507.10672_ , 2025. 

- [HuggingFace, 2024] HuggingFace. Smolvla: A small vision-language-action model. Technical report, HuggingFace, 2024. 

   - [Robinette _et al._ , 2020] Paul Robinette, Ayanna M Howard, and Alan R Wagner. Safety considerations for robots in education. _Paladyn, Journal of Behavioral Robotics_ , 11(1):331–340, 2020. 

   - [Singer _et al._ , 2006] Susan R Singer, Margaret L Hilton, and Heidi A Schweingruber. _America’s Lab Report: Investigations in High School Science_ . National Academies Press, 2006. 

   - [Spolaˆor and others, 2025] Newton Spolaˆor et al. Social robots in education: Current trends and future perspectives. _Information_ , 16(1):29, 2025. 

   - [Strauss and Corbin, 1998] Anselm Strauss and Juliet Corbin. _Basics of Qualitative Research: Techniques and Procedures for Developing Grounded Theory_ . Sage Publications, 1998. 

   - [Van de Pol _et al._ , 2010] Janneke Van de Pol, Monique Volman, and Jos Beishuizen. Scaffolding in teacher–student interaction: A decade of research. _Educational Psychology Review_ , 22(3):271–296, 2010. 

   - [van Uum _et al._ , 2021] Martina SJ van Uum, Marieke Peeters, and Roald P Verhoeff. Professionalising primary school teachers in guiding inquiry-based learning. _Research in Science Education_ , 51(Suppl 1):81–108, 2021. 

   - [Zhao and others, 2023] Tony Z Zhao et al. Learning finegrained bimanual manipulation with low-cost hardware. In _Robotics: Science and Systems (RSS)_ , 2023. 

- [Kim and others, 2024] Moo Jin Kim et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [LabBench Team, 2025] LabBench Team. Labbench: A hierarchical benchmark for scientific labs. _arXiv preprint arXiv:2505.22634_ , 2025. 

- [Lasota _et al._ , 2021] Przemyslaw A Lasota, Terrence Fong, and Julie A Shah. A survey of safety in human-robot interaction. _Foundations and Trends in Robotics_ , 8(4):1–94, 2021. 

- [Lee _et al._ , 2025] Unggi Lee, Jaeyong Lee, Jiyeong Bae, Yeil Jeong, Junbo Koh, Gyeonggeon’Boaz’ Lee, Gunho Lee, Taekyung Ahn, and Hyeoncheol Kim. Pedagogy-r1: Pedagogical large reasoning model and well-balanced educational benchmark. In _Proceedings of the 34th ACM International Conference on Information and Knowledge Management_ , pages 1497–1507, 2025. 

- [Millar, 2004] Robin Millar. The role of practical work in the teaching and learning of science. In _High School Science Laboratories: Role and Vision_ . National Academies Press, 2004. 

- [Papert, 1980] Seymour Papert. _Mindstorms: Children, Computers, and Powerful Ideas_ . Basic Books, 1980. 

- [Petersen, 2022] Marina R Petersen. Strategies to scaffold students’ inquiry learning in science. _Science Education International_ , 33(3):267–275, 2022. 

## **A Detailed Evaluation Criteria** 

This appendix provides the complete evaluation criteria for each demonstration task, developed in collaboration with science education experts and laboratory operators. 

The robot dispenses sugar and yeast into flasks, adds water, seals with balloon-capped lids, and students observe CO2 production through balloon inflation over time. 

Table 11: Evaluation criteria for yeast fermentation demonstration. 

### **A.1 Electromagnetic Induction (Physics)** 

This experiment demonstrates Faraday’s law through magnetcoil interaction. The robot picks up a bar magnet, inserts it into a solenoid coil connected to a galvanometer, and oscillates it at varying speeds to show how flux change rate affects induced current. 

Table 9: Evaluation criteria for electromagnetic induction demonstration. 

|Metric|Criterion|Benchmark|
|---|---|---|
|_Task 1: Magnet_<br>|_Pickup_<br>||
|Grip Success|Stable magnet grip|_≥_90%|
|Placement|Position in coil center|_±_1.5 cm|
|Stability|No drop during transfer|0%|
|_Task 2: Oscillati_|_on_||
|Alignment|Magnet centered in coil|_±_1.5 cm|
|Collision|Contact with coil walls|0 events|
|Cycle Success|Complete up-down cycle|_≥_85%|
|Induced Current|Galvanometer response|_≥_5%|
|_Task 3: Variable_|_Speed_||
|Cycle Time|Fast oscillation period|_≤_1.5 sec|
|Current Gain|Higher induced signal|_≥_30%|


|Metric|Criterion|Benchmark|
|---|---|---|
|_Task 1: Sugar_|_Dispensing_||
|Amount|Flask 1: 1, Flask 2: 2|_±_0.1 spoon|
|Placement|Flask opening center|_±_3 mm|
|Spillage|Material outside flask|0 g|
|_Task 2: Yeast_|_& Water Addition_||
|Yeast Amount|1 spoon per flask|_±_0.1 spoon|
|Water Volume|100 mL per flask|_±_5 mL|
|Mixing|No layer separation|_≤_10%|
|_Task 3: Cap S_|_ealing_||
|Alignment|Cap centered on opening|_≤_2 mm|
|Rotation|Turns to seal|1.5-2.5|
|Balloon|No damage or leakage|0 failures|


### **A.4 Rock Classification (Earth Science)** 

This experiment distinguishes carbonate rocks (limestone, marble) from non-carbonite rocks using acid tests. The robot picks up a dropper, aspirates dilute hydrochloric acid, applies drops to rock samples, and observes fizzing reactions indicating calcium carbonate presence. 

Table 12: Evaluation criteria for rock classification demonstration. 

### **A.2 Flame Test (Chemistry)** 

This experiment identifies metal ions through characteristic flame colors. The robot dips a nichrome wire loop into cleaning solution, collects salt samples, holds them in a Bunsen burner flame, and observes emission spectra colors (e.g., sodium: yellow, copper: green). 

Table 10: Evaluation criteria for flame test demonstration. 

|Metric|Criterion|Benchmark|
|---|---|---|
|_Task 1: Sample Co_|_llection_||
|Contact Accuracy|Wire tip to sample|_±_3 mm|
|Sample Adhesion|Single contact attach|_≥_90%|
|_Task 2: Flame He_|_ating_||
|Flame Alignment|Wire in flame center|_±_5 mm|
|Heating Duration|Maintained in flame|3_±_1 sec|
|Color Detection|Observable emission|_≥_30%|
|_Task 3: Wire Clea_|_ning_||
|Immersion Depth|Wire submerged|5-10 mm|
|Cleaning Duration|In cleaning solution|_≥_1.0 sec|
|Residue Removal|Remaining sample|_≤_10%|


|Metric|Criterion|Benchmark|
|---|---|---|
|_Task 1: Acid A_|_pplication_||
|Drop Accuracy|Acid on rock surface|_±_3 mm|
|Drop Volume|Single drop applied|0.05 mL|
|Spillage|Acid outside target|0 drops|
|_Task 2: Observ_|_ation_||
|Wait Duration|Observation period|5_±_1 sec|
|Position Hold|Stable viewing angle|_±_5 deg|
|_Task 3: Classifi_|_ication_||
|Fizz Detection|CO2 bubble observed|Yes/No|
|Sort Accuracy|Correct bin placement|100%|


### **A.5 Agar Plate Preparation (Lab Support)** 

This task supports biology experiments requiring sterile culture media. The robot removes petri dish lids, pours molten agar solution evenly across plates, and replaces lids while minimizing contamination risk, demonstrating precision liquid handling for laboratory automation. 

### **A.3 Yeast Fermentation (Biology)** 

This experiment demonstrates cellular respiration by comparing fermentation rates with different sugar concentrations. 

Table 13: Evaluation criteria for agar plate preparation. 

|Metric|Criterion|Benchmark|
|---|---|---|
|_Task 1: Lid Re_|_moval_||
|Grip Success|Stable lid grip|_≥_95%|
|Lid Placement|Set aside without flip|0 flips|
|_Task 2: Agar P_|_ouring_||
|Pour Volume|Agar amount per plate|15_±_2 mL|
|Coverage|Even surface coverage|_≥_90%|
|Bubble Count|Air bubbles in agar|_≤_3|
|Spillage|Agar outside plate|0 mL|
|_Task 3: Lid Re_|_placement_||
|Alignment|Lid centered on plate|_±_2 mm|
|Contamination|Lid interior contact|0 events|


## **B LLM-as-Judge Evaluation Rubric** 

We use GPT-4o as the judge model with the following rubric for evaluating generated text quality. The rubric assesses four dimensions: Relevance measures how accurately the text describes the current robot action; Pedagogical Value evaluates the educational scaffolding quality; Safety Communication assesses hazard awareness and guidance; and Fluency measures grammatical correctness and readability. Each dimension uses a 1–5 Likert scale where 1 indicates lowest quality and 5 indicates highest quality. 

Table 14: Rubric for text quality evaluation (1-5 scale). 

|Score|Relevance|
|---|---|
|1<br>2|Completely unrelated to current action<br>Partially related but inaccurate|
|3|Related but lacks specificity|
|4|Accurately describes current action|
|5|Accurate with rich contextual detail|
|Score|Pedagogical Value|
|1|No educational content|
|2|Simple action description only|
|3|Mentions basic science concepts|
|4|Connects to learning objectives|
|5|Includes inquiry prompts or extensions|
|Score|Safety Communication|
|1|No safety information|
|2|Inaccurate safety information|
|3|Basic safety reminders|
|4|Context-appropriate safety guidance|
|5|Proactive safety education included|
|Score|Fluency|
|1|Incoherent or ungrammatical|
|2|Multiple grammatical errors|
|3|<br>Minor errors, understandable|
|4|Clear and well-structured|
|5|Natural, professional quality|


## **C Detailed Text Quality Results** 

Table 15 presents the complete LLM-as-Judge evaluation results across all experimental conditions. We evaluated 50 randomly sampled utterances per condition using GPT-4o-mini, totaling 1,000 evaluations across 5 experiments _×_ 2 models _×_ 2 hand conditions. Each score represents the mean rating on a 1–5 scale, where higher values indicate better quality except where noted. 

Table 15: Text quality scores by experiment, model, and hand condition (mean on 1-5 scale). Rel.=Relevance, Ped.=Pedagogical Value, Safe.=Safety Communication, Flu.=Fluency. 

|Experiment|Model|Hand|Rel.|Ped.|Safe.|Flu.|
|---|---|---|---|---|---|---|
||Pedagogical|with|3.82|3.60|2.88|2.82|
|A Plt|Pedagogical|w/o|3.88|3.50|2.66|2.82|
|gar ae|Text|with|2.24|1.28|1.00|3.84|
||Text|w/o|2.22|1.22|1.00|3.92|
||Pedagogical|with|3.58|3.90|1.98|2.48|
|EM Idti|Pedagogical|w/o|3.56|3.86|1.86|2.40|
|nucon|Text|with|2.28|1.38|1.00|3.90|
||Text|w/o|2.66|1.60|1.14|4.02|
||Pedagogical|with|3.46|3.48|2.94|2.48|
|Fl Tt|Pedagogical|w/o|3.34|3.44|2.84|2.32|
|ame es|Text|with|1.76|1.00|1.00|3.70|
||Text|w/o|1.70|1.00|1.00|3.76|
||Pedagogical|with|3.66|3.26|2.90|2.46|
|Rk Cl|Pedagogical|w/o|3.64|3.22|2.90|2.42|
|oc ass.|Text|with|2.90|1.74|1.04|4.14|
||Text|w/o|2.80|1.56|1.00|4.02|
||Pedagogical|with|3.76|3.56|2.78|2.76|
|Y F|Pedagogical|w/o|3.84|3.52|2.92|2.80|
|east erm.|Text|with|1.96|1.02|1.02|3.92|
||Text|w/o|2.00|1.02|1.00|3.98|


Pedagogical VLA achieves Relevance scores of 3.34–3.88 across experiments, indicating outputs that accurately describe current actions with moderate specificity (score 3–4 range). Text-SmolVLA scores 1.70–2.90, reflecting outputs that are often only partially related to the ongoing manipulation. The gap is largest for Flame Test (1.76 difference), where Pedagogical VLA provides detailed descriptions of wire positioning and flame interaction while Text-SmolVLA produces generic statements. 

The most substantial difference appears in Pedagogical Value, where Pedagogical VLA scores 3.22–3.90 (connecting to learning objectives) versus 1.00–1.74 for Text-SmolVLA (no educational content to simple descriptions). EM Induction shows the highest Pedagogical Value (3.90) as the model generates explanations linking magnet motion to induced current, directly supporting Faraday’s law instruction. This demonstrates that the LLM distillation process successfully transfers educational scaffolding capabilities. 

Safety scores reveal context-dependent behavior. Pedagogical VLA achieves highest Safety scores in Flame Test (2.84– 2.94), reflecting inherent hazard awareness for fire-related tasks. Agar Plate (2.66–2.88) and Rock Classification (2.90) also show elevated safety content due to chemical handling. EM Induction shows lowest Safety scores (1.86–1.98) as this task involves minimal hazard. Text-SmolVLA scores near 1.0 

across all conditions, indicating complete absence of safety guidance. 

Text-SmolVLA achieves higher Fluency scores (3.70– 4.14) compared to Pedagogical VLA (2.32–2.82). This inverse relationship is expected: Text-SmolVLA generates short, simple action descriptions (e.g., “Robot is moving magnet”) with fewer opportunities for errors, while Pedagogical VLA produces longer, structured explanations with multiple components (Stage, Action, Learning Focus, Connection) that increase grammatical complexity. The moderate Fluency scores for Pedagogical VLA indicate room for improvement in text generation quality while maintaining pedagogical content. 

Table 16: Task execution results for electromagnetic induction (%). 

|Category|Metric|ACT|SmolVLA|Text|Ped.|
|---|---|---|---|---|---|
||Grip Success Rate|100|100|100|90|
||Grip Stability|90|100|90|90|
|Task Success|Target Placement|100|100|80|90|
||Oscillation Success|100|100|90|90|
||∆I Detection|100|90|80|90|
|Prtl|Step Order|90|100|89|90|
|ooco|Condition Compliance|90|85|70|90|
|Efficiency|Unnecessary Action_↓_|10|10|10|10|
||Collision Rate_↓_|10|30|40|0|
|Safet|Drop Rate_↓_|10|10|10|0|
|y|Jerk Event Rate_↓_|10|0|0|10|
||Human Detection Stop|20|100|100|90|


## **D Detailed Task Execution Results** 

This section provides detailed task execution evaluation results for each experiment across four model configurations: ACT (action chunking transformer baseline), SmolVLA (base VLA without text output), Text-SmolVLA (VLA with text healing but no pedagogical training), and Pedagogical VLA (our full model with LLM distillation). Metrics are organized into four categories: Task Success measures completion of manipulation sub-tasks; Protocol Compliance evaluates adherence to experimental procedures; Efficiency measures unnecessary actions (lower is better); and Safety includes collision rates, human detection, and hazard-specific metrics. For safety metrics marked with _↓_ , lower values indicate better performance. 

### **D.1 Electromagnetic Induction** 

This task involves picking up a bar magnet, inserting it into a solenoid coil, and oscillating it to induce current. The manipulation is relatively straightforward compared to other experiments, requiring only single-object handling without liquid or fine positioning constraints. The primary challenges are maintaining stable grip during oscillation and achieving consistent motion patterns that produce measurable induced current. 

All models achieved high grip success rates ( _≥_ 90%) for this task. ACT and SmolVLA demonstrated strong oscillation performance (100% cycle success), while text-generating models showed slightly lower scores (90%). The ∆I Detection metric measures whether the galvanometer registered measurable current during oscillation, with ACT achieving 100% and other models 80–90%. Notably, Pedagogical VLA achieved 0% collision rate and 0% drop rate while maintaining 90% human detection stop rate, suggesting that the pedagogical training objective does not compromise safety behaviors. 

ACT shows concerning safety behavior with only 20% human detection stop rate, meaning it failed to halt operations in 80% of cases when a hand entered the workspace. VLA-based models achieve 90–100% stop rates, demonstrating that language conditioning improves safety response learning even when the language output is not explicitly safety-focused. The electromagnetic induction task represents the best-case scenario for educational robotics deployment, where relatively simple manipulation requirements al- 

low all models to achieve acceptable performance while VLA models provide additional safety benefits. 

### **D.2 Flame Test** 

This task requires collecting salt samples with a nichrome wire loop, holding them in a Bunsen burner flame, and observing characteristic emission colors. The task proved challenging due to precise flame alignment requirements and safety constraints around open flame. ACT achieved the highest scores across most metrics, particularly in contact accuracy (100%) and flame alignment (80%). VLA models struggled with flame positioning, with SmolVLA achieving only 0% flame center alignment. All text-generating models showed zero reagent splash events, indicating that the additional processing does not increase spillage risk. 

Table 17: Task execution results for flame test (%). 

|Category|Metric|ACT|SmolVLA|Text|Ped.|
|---|---|---|---|---|---|
||Grip Success Rate|100|90|100|40|
||Grip Stability|90|90|90|30|
||Contact Accuracy|100|60|40|10|
|Task Success|Flame Center Alignment|80|0|30|20|
||Heating Duration|60|40|10|30|
||Cleaning Depth|80|40|60|30|
||Cleaning Duration|70|40|60|30|
|Ptl|Step Order|90|60|50|20|
|rooco|Condition Compliance|90|60|30|30|
|Efficiency|Unnecessary Action_↓_|20|10|30|0|
||Reagent Splash Rate_↓_|10|30|0|0|
|Safety|Jerk Event Rate_↓_|0|0|0|0|
||Human Detection Stop|0|80|60|10|


The low human detection stop rates across all models for Flame Test (0–80%) suggest that the presence of open flame and the need for precise positioning may interfere with safety response behaviors. Pedagogical VLA shows particularly low detection (10%), possibly because the model prioritizes completing the hazardous task quickly rather than pausing. This highlights an important area for future safety training improvements. 

The flame test results reveal a critical limitation: tasks requiring precise spatial alignment with external references (flame position) remain challenging for current VLA architectures. The cleaning metrics (Cleaning Depth, Cleaning 

Duration) show that ACT maintains better procedural consistency (70–80%) compared to VLA models (30–60%), suggesting that multi-step sequential tasks benefit from actionfocused training. For classroom deployment, flame test would require either improved model performance or human supervision during the heating phase. 

### **D.3 Yeast Fermentation** 

This multi-step task involves dispensing sugar and yeast into flasks, adding water, and sealing with balloon-capped lids. It was the most difficult task in our evaluation suite, with all models showing degraded performance. The task requires sequential manipulation of multiple objects (spoon, flask, cap) with liquid handling, presenting challenges for current VLA architectures. ACT achieved the highest task success rates but still struggled with cap alignment (40%) and rotation (30%). Text-generating models failed most sub-tasks, with Pedagogical VLA achieving 0% across grip success, grip stability, and all downstream metrics. This reflects the challenge of coordinating complex liquid handling with simultaneous text generation. 

Table 18: Task execution results for yeast fermentation (%). 

|Category|Metric|ACT|SmolVLA|Text|Ped.|
|---|---|---|---|---|---|
||Grip Success Rate|80|70|20|0|
||Grip Stability|80|70|0|0|
|Tk S|Insertion Position|20|0|0|0|
|as uccess|External Spillage|90|80|10|0|
||Cap Position Alignment|40|0|0|0|
||Rotation Count|30|0|0|0|
|Ptl|Step Order|70|30|0|0|
|rooco|Condition Compliance|30|0|0|0|
|Efficiency|Unnecessary Action_↓_|40|60|100|60|
||Collision Rate_↓_|40|40|80|80|
|Safety|Jerk Event Rate_↓_|0|20|0|0|
||Human Detection Stop|0|20|70|10|


The high unnecessary action rates (40–100%) across all models indicate that the multi-step nature of this task leads to significant inefficiency. The 80% collision rate for both TextSmolVLA and Pedagogical VLA is concerning and suggests that these models struggle to maintain spatial awareness during complex sequences. Future work should focus on improving action planning for multi-object manipulation scenarios. 

The yeast fermentation results represent the lower bound of current VLA capabilities for educational robotics. The complete failure of text-generating models on core manipulation metrics (0% grip success for Pedagogical VLA) indicates that the cognitive overhead of text generation may exceed model capacity for complex tasks. However, this experiment also has the longest task horizon (multiple pouring and sealing operations), suggesting that architectural improvements in longhorizon planning could yield significant benefits. For practical deployment, this experiment would require either task decomposition into simpler sub-tasks or hybrid approaches combining robot preparation with human completion of critical steps. 

### **D.4 Rock Classification** 

This task requires picking up a dropper, aspirating dilute hydrochloric acid, and applying drops to rock samples to observe fizzing reactions indicating carbonate content. Fine dropper manipulation proved challenging across all models due to the precision required for controlled liquid dispensing. ACT achieved reasonable grip success (100%) but struggled with precise dispensing (60% accuracy). VLA models with text output showed particularly low scores (0–20% for most metrics) due to the difficulty of coordinating fine motor control with language generation. The positive finding is that human detection stop rates were high across VLA models (90– 100%), and acid solution leakage rates were low (0–30%), indicating that safety mechanisms function well even when task performance is poor. 

Table 19: Task execution results for rock classification (%). 

|Category|Metric|ACT|SmolVLA|Text|Ped.|
|---|---|---|---|---|---|
||Grip Success Rate|100|80|40|30|
||Grip Stability|100|50|20|10|
||Dropper Uptake Volume|80|10|10|0|
|Task Success|Tip-Reaction Alignment|70|10|20|0|
||Dispensed Volume|60|10|10|0|
||Tip-Holder Alignment|30|10|0|0|
||Holder Placement Stability|20|10|0|0|
|Protocol|Step Order|80|20|0|0|
||Condition Compliance|30|10|0|0|
|Efficiency|Unnecessary Action_↓_|30|80|0|100|
||Acid Solution Leakage_↓_|30|0|0|0|
|Safet|Collision Rate_↓_|40|20|0|0|
|y|Jerk Event Rate_↓_|10|80|0|0|
||Human Detection Stop|60|100|90|100|


The contrast between task success (low) and safety metrics (high) for this experiment is notable. Text-SmolVLA and Pedagogical VLA achieve 0% collision rate, 0% acid leakage, and 90–100% human detection, despite failing most manipulation sub-tasks. This suggests that the models have learned conservative behaviors that prioritize safety over task completion when manipulation is uncertain. 

The rock classification results highlight the challenge of fine motor control in VLA models. Dropper manipulation requires precise grip positioning and controlled pressure application that current architectures struggle to achieve. ACT’s relatively better performance (60% dispensed volume accuracy vs. 0–10% for VLA models) suggests that actionfocused training better captures the subtle motor patterns required for precision tool use. However, ACT’s higher acid leakage rate (30% vs. 0%) and lower human detection (60% vs. 90–100%) indicate a safety-precision trade-off that favors VLA approaches in educational settings where student safety is paramount. 

### **D.5 Agar Plate Preparation** 

This three-stage task involves removing petri dish lids, pouring molten agar solution evenly, and replacing lids while minimizing contamination. The task showed strong performance variation across stages: all models performed well on Task 1 (lid removal) but performance degraded significantly in Tasks 2 and 3. ACT excelled at early stages (100% grip success for 

Task 1) but dropped to 70% by Task 3. VLA models struggled with the sequential nature of the task, with SmolVLA achieving 0% success for Tasks 2 and 3. Pedagogical VLA achieved 0% collision rate despite low task success, maintaining safe operation throughout. 

Table 20: Task execution results for agar plate preparation (%). 

|Category|Metric|ACT|SmolVLA|Text|Ped.|
|---|---|---|---|---|---|
||Grip Success (Task 1)|100|100|80|50|
||Grip Stability (Task 1)|100|100|70|50|
||Insertion Position (Task 1)|100|70|40|50|
||Grip Success (Task 2)|90|10|10|10|
|Task Success|Grip Stability (Task 2)|90|10|10|10|
||Device Alignment (Task 2)|70|10|10|10|
||Grip Success (Task 3)|70|0|10|10|
||Grip Stability (Task 3)|70|0|10|10|
||Dispensing Position (Task 3)|70|0|10|0|
|Pl|Step Order|70|0|0|0|
|rotoco|Condition Compliance|80|0|0|0|
|Efficiency|Unnecessary Action_↓_|30|100|60|70|
||Collision Rate_↓_|30|80|20|0|
|Sft|Media/Water Spillage_↓_|0|10|30|20|
|aey|Jerk Event Rate_↓_|80|0|0|0|
||Human Detection Stop|–|90|70|90|


The high jerk event rate for ACT (80%) compared to VLA models (0%) suggests that VLA architectures produce smoother motion trajectories, potentially due to the language conditioning regularizing action predictions. The “–” for ACT human detection indicates that this metric was not evaluated for ACT in this experiment due to protocol differences. 

The agar plate preparation results demonstrate the challenge of multi-stage tasks where errors compound across phases. The sharp performance drop from Task 1 (50–100% grip success) to Task 3 (0–70% grip success) across all models indicates that accumulated positioning errors and changed object states (removed lid, poured agar) create increasingly difficult manipulation conditions. Pedagogical VLA’s 0% collision rate despite low task success suggests that the model adopts conservative motion strategies when uncertain, which may be preferable in educational settings where safety matters more than task completion rate. 

ACT achieves the highest task success and protocol compliance scores across all experiments, demonstrating the effectiveness of action-focused imitation learning for manipulation tasks. However, ACT shows lower human detection stop rates (0–60%) compared to VLA models with text output (10–100%), suggesting that the language instruction conditioning in VLA models contributes to better safety response learning. Pedagogical VLA shows competitive manipulation safety scores despite lower task success, indicating that the text generation objective does not significantly compromise safety-critical behaviors. The results highlight a trade-off between task performance and safety awareness that merits further investigation in educational robotics contexts where student safety is paramount. 

## **E Teacher Evaluation Survey** 

We developed a comprehensive survey instrument to evaluate teacher perceptions of robot-assisted science demonstrations. 

The survey design draws on established usability frameworks from human-computer interaction research, adapted for educational robotics contexts. We consulted with science education researchers to ensure items captured pedagogically relevant dimensions beyond mere technical performance. 

Two science teachers with over 5 years of classroom experience evaluated robot demonstration videos. Both teachers had experience conducting hands-on science experiments in middle and high school settings, providing relevant domain expertise for assessing the practical viability of robotic assistance. Teachers viewed videos of each model (ACT, SmolVLA, Text-SmolVLA, Pedagogical VLA) performing each of the five experiments, completing the survey for all 20 conditions. 

The survey comprises 20 items organized into six dimensions. Accuracy and Reliability (3 items) assesses whether teachers perceive the robot as performing procedures correctly and consistently. Educational Value (3 items) evaluates whether the robot contributes meaningfully to instruction. Efficiency (3 items) measures perceived time and effort savings. Safety (4 items) addresses concerns about student protection during robot operation. Classroom Integration (3 items) examines practical deployment considerations. Interest and Adoption (4 items) gauges teacher enthusiasm and willingness to use such systems. Each item uses a 5-point Likert scale from 1 (Strongly Disagree) to 5 (Strongly Agree). 

##### **Teacher Evaluation Survey Instrument** 

**Instructions** : Please observe the robot performing the science experiment in the video. After watching, rate your agreement with each statement on a scale of 1 (Strongly Disagree) to 5 (Strongly Agree). 

##### **Accuracy and Reliability** 

1. The robot arm performed the experimental procedure largely accurately. 

2. The robot arm’s performance appeared stable. 

3. The robot arm’s operation is trustworthy. 

##### **Educational Value** 

4. The robot arm has value as a support tool for classroom instruction. 

5. The robot arm performed with minimal unnecessary movements. 

6. The robot arm’s execution speed seems appropriate. 

##### **Efficiency** 

7. Using the robot would reduce overall time spent on experimental lessons. 

8. Using the robot would reduce teachers’ mental and physical effort. 

9. Once set up, the robot appears reusable across multiple classes. 

##### **Safety** 

10. The risk of collision with students feels low. 

11. When handling hazardous materials, the robot would improve safety. 

12. The robot stopped appropriately when a hand approached. 

13. I could understand how teachers should respond to problems. 

##### **Classroom Integration** 

14. Using the robot would allow teachers to focus more on student guidance. 

15. Monitoring the robot does not appear to be a significant burden. 

16. Robot-assisted experiments appear feasible without disrupting classroom flow. 

##### **Interest and Adoption** 

17. I found watching the robot perform the experiment interesting. 

18. Robot-based experiments would increase student interest. 

19. The robot’s movements were natural and visually satisfying. 

20. I would like to introduce robot-assisted experiments in the future. 

## **F Detailed Usability Evaluation Results** 

Two science teachers (each with _>_ 5 years of classroom experience) evaluated robot demonstrations across five usability dimensions derived from the ISO 9241-11 usability framework adapted for educational contexts. The dimensions are: Effectiveness (task completion quality), Efficiency (time and resource usage), Safety (hazard prevention), Sustainability (reusability across classes), and Enjoyment (student engagement potential). Each dimension uses a 5-point Likert scale (1=Strongly Disagree, 5=Strongly Agree), with scores representing the mean across relevant survey items. 

Table 21: Usability scores by experiment and dimension (15 scale). Eff.=Effectiveness, Effi.=Efficiency, Safe=Safety, Sust.=Sustainability, Enj.=Enjoyment. Bold indicates best score per experiment and dimension. 

|Experiment|Model|Eff.|Effi.|Safe|Sust.|Enj.|
|---|---|---|---|---|---|---|
||ACT|4.00|3.75|2.63|3.88|5.00|
|EM Idti|SmolVLA|4.63|4.50|3.75|4.38|5.00|
|nucon|Text|4.50|4.88|4.38|4.88|5.00|
||Pedagogical|**5.00**|**5.00**|**4.25**|**5.00**|**5.00**|
||ACT|**4.38**|**4.88**|3.50|**4.63**|**5.00**|
|Fl T|SmolVLA|2.75|3.50|**4.13**|2.25|4.75|
|ame est|Text|3.25|4.25|4.00|3.38|4.88|
||Pedagogical|3.25|3.50|3.25|2.63|**5.00**|
||ACT|**3.63**|**3.75**|**2.50**|**2.88**|**4.38**|
||SmolVLA|2.13|2.88|2.13|2.38|4.25|
|Yeast Ferm.|Text|1.63|2.38|1.88|1.88|1.88|
||Pedagogical|1.63|2.63|1.75|2.00|3.13|
||ACT|**2.63**|**4.13**|**4.13**|**3.75**|**4.88**|
|Rk Cl|SmolVLA|1.25|1.50|2.88|2.00|2.88|
|oc ass.|Text|2.38|2.50|3.38|2.50|2.50|
||Pedagogical|1.38|1.50|3.25|2.88|2.75|
||ACT|**4.00**|**4.50**|3.38|**4.00**|**5.00**|
||SmolVLA|1.50|1.38|3.00|3.00|3.38|
|Agar Plate|Text|2.00|2.63|3.00|2.63|3.13|
||Pedagogical|1.88|2.63|**3.38**|2.88|3.25|


Usability scores strongly correlate with task difficulty. EM Induction, the simplest task, shows highest scores across all models (mean 4.37), while Yeast Fermentation shows lowest scores (mean 2.56). This pattern suggests that current VLA models are most suitable for simpler manipulation tasks in educational settings, with more complex tasks requiring further development. 

ACT achieves the highest usability scores across most experiments (15 of 25 dimension-experiment combinations), particularly in Effectiveness and Efficiency dimensions. This reflects teachers’ preference for reliable task completion over advanced features. The gap is largest for complex tasks: in Yeast Fermentation, ACT scores 3.63 for Effectiveness versus 1.63 for Pedagogical VLA. However, in Electromagnetic Induction, the simplest task with highest success rates, Pedagogical VLA achieves perfect scores (5.0) across all dimensions, suggesting that when task execution succeeds, teachers highly value the pedagogical explanations. For Safety, Pedagogical VLA achieves the highest or tied-highest score in 3 of 5 experiments (EM Induction, Rock Classification, Agar Plate), indicating that teachers perceive the safety-aware text generation as valuable. 

The Enjoyment dimension shows consistently high scores for ACT (4.38–5.00) and Pedagogical VLA in successful tasks (5.00 for EM Induction and Flame Test), indicating strong teacher interest in robot-assisted demonstrations. However, Enjoyment drops significantly for failed tasks (1.88 for Text-SmolVLA in Yeast Fermentation), suggesting that repeated failures negatively impact engagement perceptions. Overall, these results indicate that improving task success rates is critical for practical deployment, while pedagogical features provide additional value when basic manipulation succeeds. 

## **G Pedagogical Text Examples** 

This section presents representative sample outputs from Text-SmolVLA and Pedagogical VLA across different demonstration scenarios, illustrating the qualitative differences in generated text that distinguish these models. These examples were selected from actual model outputs during evaluation runs to demonstrate typical generation patterns. 

Text-SmolVLA was trained using text healing, which restores language generation capability to the base SmolVLA model by adding a text decoder trained on action narration data. This produces outputs that describe robot actions in simple declarative sentences without educational elaboration. The text serves primarily as a transparency mechanism, allowing observers to understand what the robot is doing, but provides no scaffolding for science learning. 

Pedagogical VLA extends text healing with LLM distillation, where GPT-4o generates pedagogically-aligned training data that the model learns to reproduce. The resulting outputs follow a structured format designed in consultation with science education researchers: Stage indicates the current phase of the experiment; Action describes the specific manipulation being performed; Safety Status alerts observers to any hazards; Learning Focus provides conceptual explanations connecting the action to scientific principles; Connection to 

Learning Goal explicitly links the current activity to broader educational objectives; and Next Step previews upcoming actions to support student anticipation and engagement. 

The contrast between these output styles reflects the difference between mere transparency (knowing what the robot does) and pedagogical alignment (understanding why the action matters for learning). The following examples span all five experimental domains and include both routine operation and safety intervention scenarios. 

### **G.1 Flame Test - Idle State** 

##### **Text-SmolVLA** 

_Robot arm is in standby position. Ready to begin flame test experiment._ 

##### **Pedagogical VLA** 

- [Stage] Flame heating / [Action] Positioning wire loop with sample in the hottest part of the flame / [Safety Status] Caution - Open flame in use 

**Learning Focus** : Observing characteristic flame colors. When metal ions are heated, their electrons absorb energy and jump to higher energy levels. As they return to ground state, they emit light at specific wavelengths. Sodium produces yellow, copper produces green, and lithium produces red. 

**Connection to learning goal** : This demonstrates how atomic emission spectra can be used to identify elements, a fundamental technique in analytical chemistry. 

**Next** : Observe the flame color carefully and record the result before cleaning the wire. 

##### **Pedagogical VLA** 

### **G.4 Yeast Fermentation - Sugar Dispensing** 

[Stage] Initial setup / [Action] Robot arm in standby position, preparing for flame test / [Safety Status] Normal 

**Learning Focus** : Understanding flame test preparation. Before heating, identify the materials: nichrome wire loop, salt samples in dish, burner, and cleaning solution. Each metal salt will produce a characteristic color when heated. 

**Connection to learning goal** : Proper preparation ensures accurate identification of metal ions through their emission spectra. 

**Next** : Pick up the wire loop and clean it in the solution. 

### **G.2 Electromagnetic Induction - Active Phase** 

##### **Text-SmolVLA** 

_Moving magnet into the coil. Pulling magnet out of coil._ 

##### **Pedagogical VLA** 

[Stage] Magnet insertion and withdrawal / [Action] Sliding the magnet into and out of the coil along its axis / [Safety Status] Normal 

**Learning Focus** : Linking changing magnetic flux to induced voltage/current. Moving the magnet changes the magnetic flux through the coil. This changing flux induces an electromotive force (voltage), and a current flows if the circuit is closed. Watch the meter. 

**Connection to learning goal** : Supports correct identification of induction by relating motion direction and speed to the sign and size of the induced signal. 

**Next** : Compare the meter response for insertion vs. withdrawal motion. 

### **G.3 Flame Test - Heating Phase** 

##### **Text-SmolVLA** 

_Holding wire in flame. Wire is in the burner flame._ 

##### **Text-SmolVLA** 

_Robot is adding sugar to the flask. Dispensing material into container._ 

##### **Pedagogical VLA** 

- [Stage] Sugar dispensing / [Action] Adding measured amount of sugar to Flask 1 / [Safety Status] Normal 

**Learning Focus** : Setting up a controlled experiment. We are adding different amounts of sugar to each flask to test how sugar concentration affects fermentation rate. Flask 1 receives 1 spoon, Flask 2 receives 2 spoons. This creates our independent variable. 

**Connection to learning goal** : Understanding variable control is essential for scientific experimentation. By changing only the sugar amount while keeping other factors constant, we can determine the relationship between sugar concentration and CO2 production. 

**Next** : Add yeast to both flasks, then add warm water to activate the fermentation process. 

### **G.5 Yeast Fermentation - Observation Phase** 

**Text-SmolVLA** 

_Flasks are sealed. Experiment setup complete._ 

##### **Pedagogical VLA** 

[Stage] Fermentation observation / [Action] Monitoring sealed flasks for balloon inflation / [Safety Status] Normal 

**Learning Focus** : Cellular respiration produces CO2. Yeast cells break down sugar through anaerobic respiration (fermentation), producing carbon dioxide and ethanol. The CO2 gas inflates the balloons, providing a visible indicator of metabolic activity. 

**Connection to learning goal** : Comparing balloon sizes be- 

tween flasks demonstrates how substrate concentration affects enzyme activity and metabolic rate in living organisms. **Next** : Record balloon sizes at regular intervals to track fermentation progress over time. 

### **G.6 Rock Classification - Acid Application** 

**Text-SmolVLA** 

_Robot is dispensing a clear liquid from a pipette onto a rock._ 

##### **Pedagogical VLA** 

[Stage] Acid test / [Action] Applying dilute hydrochloric acid drop to rock sample surface / [Safety Status] Caution - Handling dilute acid 

**Learning Focus** : Chemical identification of carbonate minerals. When acid contacts calcium carbonate (CaCO3), a chemical reaction occurs: CaCO3 + 2HCl _→_ CaCl2 + H2O + CO2. The bubbling (effervescence) indicates CO2 gas release. 

**Connection to learning goal** : This acid test distinguishes carbonate rocks (limestone, marble) from non-carbonate rocks (granite, basalt), demonstrating how chemical properties help classify geological samples. 

**Next** : Observe the rock surface for fizzing reaction and record whether bubbles appear. 

### **G.7 Rock Classification - Result Observation** 

##### **Text-SmolVLA** 

_Observing rock surface. Waiting for reaction._ 

##### **Pedagogical VLA** 

[Stage] Result observation / [Action] Holding position to observe acid-rock reaction / [Safety Status] Normal 

**Learning Focus** : Interpreting chemical test results. If bubbles form vigorously, the rock contains significant calcium carbonate and is likely limestone or marble. Weak or no reaction suggests the rock is granite, basalt, or another noncarbonate type. 

**Connection to learning goal** : Scientists use simple chemical tests like this to identify rock types in the field. This connects laboratory techniques to real-world geological investigation methods. 

**Next** : Classify the rock based on the reaction intensity and move to the next sample. 

### **G.8 Agar Plate - Lid Removal** 

##### **Text-SmolVLA** 

_Robot is removing the lid from the petri dish._ 

##### **Pedagogical VLA** 

- [Stage] Plate preparation / [Action] Carefully lifting petri dish lid and setting aside / [Safety Status] Caution - Maintaining sterile technique 

**Learning Focus** : Aseptic technique in microbiology. When preparing culture plates, minimizing lid-open time reduces contamination from airborne microorganisms. The lid should be held at an angle over the plate rather than placed on the bench surface. 

**Connection to learning goal** : Sterile technique is fundamental to microbiology experiments. Proper plate preparation ensures that only the intended organisms grow in subsequent experiments. 

**Next** : Pour the molten agar evenly across the plate surface. 

### **G.9 Agar Plate - Pouring Phase** 

##### **Text-SmolVLA** 

_Robot is pouring liquid into the dish. Adding agar to plate._ 

##### **Pedagogical VLA** 

- [Stage] Agar pouring / [Action] Dispensing molten agar solution evenly across petri dish / [Safety Status] Caution - Hot liquid handling 

**Learning Focus** : Preparing solid growth medium. Agar is a polysaccharide derived from seaweed that solidifies at room temperature. The molten agar (kept at approximately 50°C) must be poured smoothly to create an even surface without bubbles, which could interfere with colony counting. 

**Connection to learning goal** : Properly prepared agar plates provide a consistent growth surface for microorganisms, enabling reproducible experiments in microbiology and biotechnology. 

**Next** : Replace the lid promptly and allow the agar to solidify before use. 

### **G.10 Safety Intervention Scenario** 

##### **Text-SmolVLA** 

_Stopping. Hand detected near robot._ 

##### **Pedagogical VLA** 

- [Stage] Human intervention detected / [Action] Pausing operation - human hand in workspace / [Safety Status] Stop - Human detected in robot operating area 

**Learning Focus** : Laboratory safety protocols. When a human hand enters the robot’s workspace, operations must pause immediately. This prevents potential collisions and injuries. Never reach into the robot’s working area while it is moving. 

**Connection to learning goal** : Understanding human-robot safety boundaries is essential in automated laboratory environments. 

**Next** : Wait for clear workspace before resuming the experiment. 

## **H Hardware and Training Configuration** 

We used a low-cost robot arm setup designed for educational environments where budget constraints are common. The SO-101 is a next-generation open-source robot arm developed by The Robot Studio in collaboration with Hugging Face, designed for integration with the LeRobot framework. The arm provides 6 degrees of freedom (5 arm joints plus 1 gripper joint) suitable for tabletop manipulation tasks typical of science demonstrations. Compared to its predecessor SO100, the SO-101 features improved wiring, simplified assembly without gear removal requirements, and updated motor configurations. 

The follower arm uses six Feetech STS3215 servo motors with 1:345 gear ratio. Each motor features a 12-bit magnetic encoder providing 4096 steps per 360° rotation (0.088° resolution per step), enabling precise position control. The magnetoresistive encoder design eliminates friction-based wear compared to potentiometer-based alternatives. The motors provide 19.5 kg _·_ cm stall torque at 7.4V, sufficient for manipulating laboratory equipment and samples. Independent testing has confirmed measured stall torque slightly exceeds datasheet specifications, though mechanical backlash (approximately 2 encoder steps or 0.17°) and firmware-defined dead zones may reduce precision for fine motion tasks. 

The total hardware cost is approximately $300 USD including the arm, motors, gripper, and mounting hardware, making the system accessible for school settings with limited budgets. Dual cameras capture complementary views for robust visual perception: a wrist-mounted camera provides close-up manipulation views essential for precise object interaction, while a top-mounted camera captures the overall workspace context for spatial reasoning and safety monitoring. 

Table 22: Hardware configuration for data collection and deployment. 

|Component|Specification|
|---|---|
|Robot Arm|SO-101, 6-DOF (5 arm + 1 gripper)|
|Motors|Feetech STS3215 (7.4V, 19.5 kg_·_cm, 1:345 gear)|
|Encoder|12-bit magnetic (4096 steps/revolution)|
|Gripper|Parallel jaw gripper|
|Wrist Camera|RGB, 640_×_480, 30 fps|
|Top Camera|RGB, 640_×_480, 30 fps|
|Control Frequency|30 Hz|
|Action Space|Joint positions, normalized to[_−_100_,_100]|


Our implementation builds on SmolVLA, a compact 450M parameter Vision-Language-Action model designed for efficient robotics applications. SmolVLA uses SmolVLM2 as its VLM backbone, consisting of a SigLIP vision encoder for image processing and a SmolLM2 language decoder for multimodal reasoning. The action expert is a separate transformer module (approximately 100M parameters) trained with flow matching to output action chunks of 50 timesteps. Despite 

its compact size, SmolVLA achieves performance comparable to VLA models that are 10 _×_ larger, making it suitable for educational deployment where computational resources may be limited. 

Training hyperparameters were selected based on preliminary experiments balancing action accuracy and text generation quality. The text loss weight ( _λ_ = 0 _._ 1) was chosen to ensure that text generation does not dominate the training signal while still enabling meaningful pedagogical output. Higher values led to degraded manipulation performance, while lower values resulted in generic text outputs. The 12layer text decoder provides sufficient capacity for generating structured educational explanations while remaining computationally efficient for real-time inference on consumer hardware. 

Table 23: Hyperparameters for model training. 

|Parameter|Value|
|---|---|
|Base Model<br>|SmolVLA (450M parameters)<br>|
|Training Steps|100,000|
|Batch Size|32|
|Learning Rate|1e-4 (AdamW,_β_1=0.9,_β_2=0.95)|
|LR Schedule|Cosine decay (min 2.5e-6)|
|Text Loss Weight (_λ_)<br>|0.1<br>|
|Max Text Length|128 tokens|
|Text Decoder Layers|12|
|Text Decoder Hidden Dim|768|
|Image Resolution|512_×_512|
|Action Chunk Size|50 timesteps|
|Distillation Model|GPT-4o|
|Training Hardware|4_×_NVIDIA A100 (80GB)|
|Training Time|Approximately 48 hours|


Data collection was performed via teleoperation using a leader-follower setup, where a human operator controlled a leader arm while the follower arm replicated the movements. Each experiment was collected 50 times with variations in object positions, lighting conditions, and operator speed. For safety intervention data, we collected an additional 20 episodes per experiment where a human hand entered the workspace at random intervals, with the operator demonstrating appropriate stopping behavior. The total dataset comprises approximately 350 episodes across 5 experiments (250 standard + 100 with hand intervention), with each episode containing 500–2000 timesteps depending on task complexity. 

For LLM distillation, we prompted GPT-4o with video frames and task descriptions to generate pedagogical explanations for each timestep. The prompt included the current action, experiment type, and safety status, instructing the model to generate output following the structured format (Stage, Action, Learning Focus, Connection, Next Step). We filtered generated text for quality, removing outputs that did not follow the format or contained factually incorrect scientific content, retaining approximately 85% of generated explanations for training. 

