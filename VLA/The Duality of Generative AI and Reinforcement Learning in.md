---
title: "The Duality of Generative AI and Reinforcement Learning in Robotics: A Review"
date: "2024-10-21"
authors: "Angelo Moroncelli; Vishal Soni; Marco Forgione; Dario Piga; Blerina Spahiu; Loris Roveda"
url: https://arxiv.org/abs/2410.16411
pdf: https://arxiv.org/pdf/2410.16411
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2410.16411)** / [論文ページ](https://arxiv.org/abs/2410.16411)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# The Duality of Generative AI and Reinforcement Learning in Robotics: A Review 

Angelo Moroncelli<sup>a,</sup><sup>_∗_</sup> , Vishal Soni<sup>a,b</sup> , Marco Forgione<sup>a</sup> , Dario Piga<sup>a</sup> , Blerina Spahiu<sup>c</sup> , Loris Roveda<sup>a,d,</sup><sup>_∗_</sup> 

> _aDepartment of Innovative Technologies, IDSIA, University of Applied Science and Arts of Southern Switzerland, Lugano, 6900, Ticino, Switzerland_ 

> _bDepartment of Mechatronics and Automation Engineering, Indian Institute of Information Technology Bhagalpur, Bhagalpur, 813210, Bihar, India_ 

> _cDepartment of Informatics, Systems and Communication, Università di Milano Bicocca, Milano, 20126, Lombardy, Italy_ 

> _dMechanical Department, Politecnico di Milano, Milano, 20156, Lombardy, Italy_ 

## **Abstract** 

Recently, generative AI and reinforcement learning (RL) have been redefining what is possible for AI agents that take information flows as input and produce intelligent behavior. As a result, we are seeing similar advancements in embodied AI and robotics for control policy generation. Our review paper examines the integration of generative AI models with RL to advance robotics. Our primary focus is on the duality between generative AI and RL for robotics downstream tasks. Specifically, we investigate: (1) The role of prominent generative AI tools as modular priors for multi-modal input fusion in RL tasks. (2) How RL can train, fine-tune and distill generative models for policy generation, such as VLA models, similarly to RL applications in large language models. We then propose a new taxonomy based on a considerable amount of selected papers. 

Lastly, we identify open challenges accounting for model scalability, adaptation and grounding, giving recommendations and insights on future research directions. We reflect on which generative AI models best fit the RL tasks and why. On the other side, we reflect on important issues inherent to RL-enhanced generative policies, such as safety concerns and failure modes, 

> _∗_ Corresponding author(s) 

_Email addresses:_ `angelo.moroncelli@supsi.ch` (Angelo Moroncelli), `loris.roveda@supsi.ch` (Loris Roveda), `loris.roveda@polimi.it` (Loris Roveda) 

_Preprint submitted to Information Fusion_ 

_September 2, 2025_ 

and what are the limitations of current methods. A curated collection of relevant research papers is maintained on our GitHub repository, serving as a resource for ongoing research and development in this field. 

_Keywords:_ robotics, generative AI, foundation model, reinforcement learning, data fusion, review 

## **1. Introduction** 

Two main pursuits of embodied intelligence and robotics are achieving physical grounding [37, 83], the capability of robots to sense, comprehend, and interact efficiently with the physical environment, and human-level reasoning on abstract concepts [37, 24, 5, 72], which remain a central goal of artificial intelligence (AI) research in general. Recently, the convergence of two powerful paradigms, generative AI and Reinforcement Learning (RL), has shown significant promise in advancing this objective [163, 94, 151, 101, 103, 184, 71]. On the one hand, tools from generative AI, including Large Language Models (LLMs), multi-modal foundation models [14] such as VisionLanguage Models (VLMs), and world or video prediction models, have excelled in processing and generating diverse data types such as text, code, and images [10, 33, 128, 60]. Trained on vast multi-modal datasets, these models encapsulate rich, generalizable knowledge representations [28, 57, 123]. Moreover, diffusion models excel in generative capabilities and robust training processes for downstream tasks such as state representation and policy generation [61, 35]. RL, on the other hand, offers a framework for agents to learn optimal behaviors through interaction with their environment [139, 111]. 

The potential synergy between generative AI and RL is particularly compelling in the context of robotics. Generative models can serve as robust priors for information fusion in RL agents— _i.e._ , fusing information flows from different sources to produce a robot control policy—providing extensive world knowledge, grounding language understanding, and generating rich behaviors [51, 101, 151]. Conversely, RL can “embody” generative AI models used as generative policies for robotics, usually trained through pure Imitation Learning (IL) [119], allowing them to interact with and learn from dynamic physical environments and suboptimal data [140]. This integration could lead to robotic systems with enhanced adaptability, generalization, and overall intelligence through feature alignment with experience [141], similarly to RL from human feedback training for LLMs [186]. 

2 

Foundation models, in particular, have demonstrated exceptional proficiency in processing information for downstream robotics tasks [73, 134, 12]. Additionally, specialized foundation models for robotics exist [51]. Foundation models have also been adopted in the field of learning and control of dynamical systems, where robotics represents a key area of application. Transformer-based pre-trained models have been proposed [52, 46] for zeroshot prediction of outputs from a class of dynamical systems in response to any query input sequence, and for in-context state estimation [22]. These advancements highlight the potential of foundation models to introduce innovative approaches and paradigms to traditional dynamical control systems, facilitating a shift towards data-driven estimation and control synthesis for classes of dynamical systems, rather than for single, specific systems. 

However, despite significant progress in foundation models, their application with RL in robotics remains underexplored. Recent developments suggest this promising union to enhance robotic learning and generalization, yet challenges persist, especially for real-world robotic applications [99]. 


(b) The heatmap highlights the notable rise in the use of diffusion models as tools for RL in robotics from 2023 up to February 2025 (dark purple block). Notice the recent introduction of few seminal works in RL-based fine-tuning and distillation of generative policies. 

Figure 1: **Trends in generative AI and RL integration for robotics.** 

## _1.1. Scope and Contribution_ 

Despite rapid advancements in both generative AI and RL [47, 2, 111, 126], there is a noticeable lack of comprehensive studies systematically exploring their integration in robotics (see Table 1). Few research either focuses on these areas in isolation [69, 162, 51, 181], or examines narrow aspects of 

3 

their combination [23, 184]. Our review addresses this gap by providing an in-depth analysis of current research trends at the intersection of generative AI and RL in robotics. Specifically, it examines Transformer- and Diffusionbased generative AI models (LLMs, VLMs, diffusion models (DMs), world models (WMs) and video prediction models (VPMs)) currently used to enhance RL, considering the diverse data modalities, roles, and applications (see Sections 3, 4, and 5). Figure 1a illustrates the growing adoption of generative AI models for RL, particularly diffusion models as tools for RL in 2023–2024, as shown in Figure 1b. Additionally, particular attention is given to the unique relationship between generative policies, which are a specific and relatively narrow type of generative models for robotic action generation, and their integration with RL (see Sections 6, 7, and 8), with insights on their good fitting with learning-based control techniques for grounding into downstream robotic tasks (see Section 10). To the best of our knowledge, RL fine-tuning of generalist generative policies has also not been classified in previous surveys [69, 162, 51, 181]. 

|**Survey**|**RFM**||**Too**|**ls for R**|**L**|**RL **|**Policies**|
|---|---|---|---|---|---|---|---|
|||**LLM**|**VLM**|**DM**|**WM/VPM**|**Train**|**Fine-Tune**|
|Hu et al. [69]|✓|_⋆_|_⋆_|||✓||
|Xiao et al. [162]|✓|_⋆_||||_⋆_||
|Firoozi et al. [51]|✓|_⋆_|_⋆_|||✓||
|Zhou et al. [181]|✓|_⋆_||||_⋆_||
|Wang et al. [148]|✓|||||_⋆_||
|Cao et al. [23]|_⋆_|✓||||||
|Zhu et al. [184]|_⋆_|||✓||||
|**Ours**|_⋆_|✓|✓|✓|✓|✓|✓|


Table 1: Comparison of survey papers across robotics learning categories and methods: _Foundation Models for Robotics_ ( **RFM** ), _Generative Tools for RL_ ( **Tools for RL** ) and 

_RL for Generative Policies_ ( **RL Policies** ). _⋆_ means that the survey falls into that category but it does not broadly focus on the RL analysis, instead focusing on a specific subtopic. 

## The main **contributions** of our work are: 

1. A comprehensive review of the intersection between Transformer- and Diffusionbased generative models and RL for robotics. 

2. The first, to the best of our knowledge, dual analysis of how generative AI tools improve RL and RL improves generative policy models for robotics. 

3. The identification of best practices and challenges when using generative AI models as tools for RL. 

4 

4. A detailed classification of RL-based training, fine-tuning and distillation methods for generalist generative policies. 

5. The identification of three new research directions integrating generative AI and RL to enhance robotics. 

6. A unified new taxonomy and continuously updated repository<sup>1</sup> for tracking progress in this field. 

The remainder of our paper is structured as follows: **Section 2** presents our taxonomy based on the duality between generative AI transformer- and diffusion-based tools and RL. **Section 3** ( _Base Model_ ), **Section 4** ( _Modality_ ) and **Section 5** ( _Task_ ) investigate deeper the dimension of generative AI models used as modular tools for the RL training loop, analyzing _Generative Tools for RL_ . On the other hand, **Section 6** explores _RL-Based Training_ of generative policies with consequent _RL-Based Fine-Tuning_ for downstream tasks ( **Section 7** ) and _Model Distillation_ ( **Section 8** ), looking into _RL for Generative Policies_ . **Section 9** discusses challenges. We conclude with **Section 10** , suggesting our perspective on possible future research directions based on our findings. 

## _1.2. Methodology_ 

We conducted this comprehensive review on the integration of transformerand diffusion-based models with RL because these are two of the most rapidly emerging research areas in robotics learning. As noted in the previous section, we have observed a significant increase in the number of published papers on these topics in recent years, but especially, at their intersection. Given the exponential growth of research in generative AI for robotics, we chose to focus our review specifically on transformer- and diffusion-based models. To compile our dataset, we searched for relevant papers published between 2019, when we identified the first preliminary works integrating transformers with RL for robotics applications, and February 2025. We used keyword-based searches to filter papers aligned with the scope of our review, excluding those that did not meet our criteria, following the widely recognized PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) methodology<sup>2</sup> . In the identification phase, we selected 15 relevant keywords to identify papers relevant to our review. We used combinations of terms such as RL with foundation models, LLM, VLM, diffusion models, world models, and 

> 1 `https://github.com/clmoro/Robotics-RL-FMs-Integration` 

> 2PRISMA: Preferred Reporting Items for Systematic Reviews and Meta-Analyses 

5 

video prediction models for filtering works on _Generative Tools for RL_ . For _RL for Generative Policies_ , we combined RL with transformer, diffusion, flow matching, generative policy, pre-training, fine-tuning, and distillation. Our search spanned multiple platforms, including Scopus, DBLP, IEEE Xplore, Google Scholar, and ArXiv, as well as references found in other related surveys listed in Table 1. In the screening phase, two researchers manually reviewed the abstracts of the identified papers to ensure their relevance to the robotics domain. During the selection stage, 169 papers that strictly met the inclusion criteria were chosen for analysis. To structure our taxonomy, we identified relevant categories based on two major dimensions of our study. Papers included in our review were required to be directly related to robotics and RL, published in English, and ideally peer-reviewed. However, given the fast-paced nature of this field, many relevant works have been published on preprint servers such as ArXiv and have yet to undergo formal peer review for top-tier journals or conferences. 

## **2. Taxonomy** 

In our review, we analyze how prominent generative AI tools and RL converge to enhance control policies for robots, specifically, action reference signals in the robot’s Cartesian operational space. To achieve this, we propose a new taxonomy that categorizes the 169 papers we examined, tracing the evolution of generative AI and RL integration for multi-modal data fusion in robotics policy generation. Our taxonomy (see Figure 2 for an abstract representation) primarily explores the duality between _Generative AI tools for RL_ and _RL for Generative Policies_ . We chose to analyze only papers focusing on specific generative models—particularly modern architectures widely adopted in recent works for policy generation, primarily based on transformers or diffusion models. We further classify the approaches along six principal dimensions based on orthogonal features of the works. For _Generative Tools for RL_ , we categorize papers based on their underlying model architecture, which we refer to as the **Base Model** ; the input and output modalities, referred to as **Modality** ; and finally, the aim of the RL process, which we call the **Task** . For _RL for Generative Policies_ , we analyze research along: pretraining strategies for different policy architectures, which we refer to as **RL pre-training** ; methods for adapting policies through interaction, referred to as **RL fine-tuning** ; and the transfer or compression of policies, which we call **Policy Distillation** . We chose these categories to reflect two clear and 

6 

growing trends in recent literature, that we depict in Figure 3: the increasing use of generative models as tools within RL pipelines (blue outline), and the rise of RL techniques for training and refining generative policies (red outline), especially in robotic manipulation. Model architecture, modality, and task alignment are now central to foundation model choice [55], while RL techniques like fine-tuning and policy distillation are increasingly used to adapt generative policies [107]. Our taxonomy captures this duality by focusing on the most recurrent and emphasized dimensions in recent works. 


Figure 2: **Taxonomy.** A taxonomy of the generative AI tools and RL integration for robotics. 

## _2.1. Generative Tools for RL_ 

_Generative Tools for RL_ explores how selected generative AI architectures can be integrated into the RL training loop (see Figure 3a). We analyze prior work on leveraging generative and foundation models to enhance robotics, focusing on Transformer and Diffusion backbones. **“As tools”** highlights that pre-trained foundation models (like LLMs) are not being retrained endto-end with the RL agent, but are instead leveraged in a modular way—as plug-and-play components that provide capabilities (such as understanding or generating specific modalities) that the RL agent can use during training or decision making. Their in-context learning ability allows them to flexibly adapt to tasks without needing full retraining, making them useful tools for enhancing RL agents. Our analysis is structured along three key secondary dimensions: (i) _Base Model_ , (ii) _Modality_ , and (iii) _Task_ . 

## _Base Model_ 

_Base Model_ classifies the models based on their underlying architecture, which directly influences their capabilities. Different architectures process 

7 

and generate various types of data, shaping how they interact with RL. We analyze how deeply each base model can be incorporated into the RL framework based on its structural characteristics. Furthermore, for each model, approaches are analyzed along with (i) the framework names, (ii) code availability, (iii) the data used for training, and (iv) whether the pipeline is in simulation or the real world. Under this dimension, we consider the following models: _LLMs_ , _VLMs_ , _Diffusion Models_ , _World Models_ , and _Video Prediction Models_ . 

## _Modality_ 

Under the _Modality_ dimension, we analyze approaches based on their _Input_ and _Output_ modalities, such as text, images, trajectories, or low-level sensory signals. These modalities determine how generative AI integrates with RL by tackling input data interpretation and representation. Understanding these modalities helps assess the suitability of different generative AI tools for various RL applications. 

## _Task_ 

Generative AI models often serve as powerful priors within the RL training loop, as they are typically pre-trained modules that enhance specific aspects of learning. In this section, we delve deeper into how different works have employed generative models to address key _Tasks_ in the RL training loop such as: _Reward Signal_ generation, _State Representation_ and _Planning & Exploration_ . Figure 3a illustrates scenarios where various generative AI tools enhance RL tasks. As an example, LLMs support symbolic reasoning for rewards or plan generation based on task descriptions, while VLMs contribute to reward augmentation or plan generation through scene understanding. 

## _2.2. RL for Generative Policies_ 

The second primary dimension of our taxonomy examines RL methods used to train generative models, offering a complementary perspective to _Generative AI Tools for RL_ . Here, we analyze works that employ RL-based approaches to pre-train, fine-tune, or distill generative policies—where RL is used directly to optimize models for action generation. We organize our discussion along three secondary dimensions, which we refer to as: (i) _RLBased Pre-Training_ , (ii) _RL-Based Fine-Tuning_ , and (iii) _Policy Distillation_ (see Figure 3b). 

8 

## _RL-Based Pre-Training_ 

We survey various RL methods used to pre-train Transformer- and Diffusionbased policy backbones, enabling generalist generative policies that can process complex instructions; we divide them in _Transformer Policy_ and _Diffusion Policy_ respectively. Alternatively, RL can be used to train any set of simpler, task-specific policies for low-level control. These policies serve as a library of primitives ( _Primitive Generator_ ), which can then be orchestrated by a foundation model-based planner for more complex behaviors. 

## _RL-Based Fine-Tuning_ 

Fine-tuning pre-trained policies is a standard approach to adapting models to new tasks or datasets. We classify fine-tuning methods for generative policies based on their architecture and policy size—we call them _Policy Specific Methods_ . Additionally, we discuss emerging policy-agnostic fine-tuning techniques that aim to improve generalization across different generative architectures—called _Policy Agnostic Methods_ . 

## _Policy Distillation_ 

Beyond policy fine-tuning, RL includes the concept of _Policy Distillation_ , which refers to transferring knowledge and learned skills from a “teacher” policy to a “student” policy [131]. Recently, researchers have begun investigating how to distill knowledge from large pre-trained Vision-Language-Action (VLA) models into smaller and efficient RL-based expert policies ( _From Generalist to Expert_ ), as well as how to use RL pre-trained single-task policies to inject more knowledge into VLA models ( _From Experts to Generalist_ ). 

## **3. Base Model** 

Generative models as tools for RL can be primarily classified by their _Base Model_ — _i.e._ , the backbone architecture. In our review, we identify five main architectures that are typically used in RL: LLMs, VLMs, diffusion models, world models, and video prediction models. Figure 4a visually represents these models, along with reference papers [101, 3, 71, 169] for each category and their associated input/output modalities. 

The _Base Model_ section classifies the papers according to their architecture, briefly describes their features, and summarizes key aspects in tables. These aspects are important when selecting a tool for the RL tasks defined in Section 2. The table columns represent the following: 

9 


Figure 3: **Duality between RL and generative AI models in robotics.** 

- _Paper_ : Lists the corresponding research papers. 

- _Framework_ : Specifies the generative AI framework used. 

- _Base Model/ Architecture_ : Specifies the generative AI architecture used. 

- _Network_ : Indicates the actual neural network model ( _e.g._ , GPT-3.5, GPT-4 for LLMs). 

- _Code Available_ : Highlights whether the implementation is accessible. 

- _Training Data_ : Lists the environments or datasets employed. 

- _Task_ : Describes the key task or feature handled by the framework ( _e.g._ , reward function design, exploration). 

- _Simulation_ or _Real Exp_ : Distinguishes between simulated environments and realworld experiments. 

Table 2 offers details on LLM-based works; Table 3 covers VLMs; Tables 4 and 5 summarize diffusion models; and Table 7 presents information on world models and video prediction models. 

## _3.1. LLM_ 

LLMs are changing how agents learn through RL. These models enable agents to acquire skills more effectively and flexibly by generating high-level plans, interpreting instructions, and providing structured feedback [101, 103, 98, 12, 177, 138]. LLMs are incorporated into RL systems mostly because of their capacity to leverage vast amounts of existing information [171, 23]. Because of this integrated knowledge, agents are less penalized by learning everything from scratch, which facilitates exploration and convergence on efficient behaviors. For example, GPT-4 is utilized in the EUREKA frame- 

10 

work [101] to automatically generate code for RL tasks. Similarly, in openended textual settings with undefined learning objectives, LMA3 [39] uses GPT-3.5. Adaptability is another benefit. LLMs can take zero-shot decisions through prompts or updated instructions, in contrast to classic RL techniques that frequently demand for big datasets and retraining when situations change[5]. But flexibility is not without its drawbacks. Because pre-trained models’ reactions are limited by the data they were trained on, they may perform poorly in contexts that are novel or that change quickly. If not handled appropriately, this can result in biased behavior and false assumptions [51]. However, adding LLMs to RL also presents a number of difficulties. Interpretability is a major problem. It is challenging to comprehend or follow the logic behind the outputs of LLMs because they function mostly as “black boxes.” In safety-critical applications such as robotics, this lack of transparency becomes a significant concern [36, 44, 173]. Furthermore, there are real-world limitations due to the computing requirements of LLMs [47, 148, 183] and few works utilize open-source models. 

Recent work combining LLMs with RL is summarized in Table 2, which covers the main frameworks, models, code availability, training data, and use cases in the RL training loop. The BOSS framework [175], for instance, makes use of GPT-3.5 to provide skill chaining across long-horizon activities, assisting agents in learning complicated behaviors through the extension and reuse of acquired abilities. FoMo [96] increases agents’ sensitivity to task context by using LLMs to dynamically scale reward signals based on visual inputs. The functions that the LLMs perform, including reward design, plan creation, or skill discovery, are represented by the _Task_ in the table. These task modules are integrated into larger RL pipelines. More details are given in Sections 4 and 5. 

## _3.2. VLM_ 

The integration of multi-modal VLMs into RL is a significant step forward with respect to single modality LLMs, enabling more useful and informative text and visual input fusion [40, 146, 3, 102, 151, 136, 167, 42, 128, 10, 33, 104, 98]. This is particularly useful in complex robotic tasks where goal states are better represented through images rather than numbers or text. One of the key advantages of VLMs is their ability to generalize across tasks without requiring environment-specific fine-tuning, similar to LLMs [40]. Moreover, VLMs can work directly with real-world perception and don’t need to rely on accurate environment information translated into 

11 

|**Paper**|**Framework**|**Base Model/ Ar-**<br>**chitecture**|**Network**|**Code**|**Training Data**|**Task**|**Simulation**<br>**or**<br>**Real-World Exp.**|
|---|---|---|---|---|---|---|---|
|Chu et al. [36]|Lafite-RL|LLM, World Model|GPT 3.5 and GPT<br>4|N/A|Simulated<br>robotic<br>environment|Reward Signal|Simulation|
|Colas et al. [39]|Language Model<br>Augmented Au-<br>totelic<br>Agent<br>(LMA3)|LLM|ChatGPT (gpt-3.5-<br>turbo-0301)|N/A|Text-based<br>envi-<br>ronment (Cooking-<br>World)|Planning & Ex-<br>ploration|Simulation|
|Zhang et al. [175]|Bootstrapping<br>your Own Skills<br>(BOSS)|LLM|GPT 3.5|Yes|Alfred<br>Dataset,<br>Demonstration<br>data|Planning & Ex-<br>ploration|Simulation + Real-<br>World|
|Ahn et al. [5]|SayCan|LLM|GPT-3, FLAN and<br>LAMBDA|Yes|Various real-world<br>robotic tasks|Planning & Ex-<br>ploration|Real-World|
|Ma et al. [101]|EUREKA|LLM|GPT 4|Yes|Variety of robotic<br>tasks|Reward Signal|Simulation<br>(NVIDIA<br>Isaac<br>Gym)|
|Lubana et al. [96]|Foundation<br>Models<br>as<br>Re-<br>ward<br>Functions<br>(FoMo Rewards)|LLM|N/A|N/A|Visual observations<br>from<br>agent’s<br>tra-<br>jectory|Reward Signal|Simulation|
|Huang et al. [72]|Grounded<br>De-<br>coding (GD)|LLM|InstructGPT<br>and<br>PALM|N/A|Various<br>embodied<br>tasks|Planning & Ex-<br>ploration|Simulation|
|Carta et al. [24]|Grounded<br>Lan-<br>guage<br>Models<br>(GLAM)|LLM|N/A|Yes|Textual<br>environ-<br>ment<br>(BabyAI-<br>Text)|State Represen-<br>tation|Simulation|
|Du et al. [44]|Exploring<br>with<br>LLMs (ELLM)|LLM|GPT-3,<br>GPT-2<br>and InstructGPT|Yes|Various<br>environ-<br>ments<br>(Crafter,<br>Housekeep)|State Represen-<br>tation|Simulation|
|Colas et al. [38]|Intrinsic<br>Mo-<br>tivations<br>And<br>Goal<br>Invention<br>for<br>Exploration<br>(IMAGINE)|LLM|N/A|Yes|Procedurally-<br>generated scenes|Planning & Ex-<br>ploration|Simulation|
|Hu and Sadigh [64]|LLM Prior Pol-<br>icy with Regu-<br>larized RL (in-<br>structRL)|LLM|GPT 3.5, GPT J|Yes|Toy game and Han-<br>abi benchmark|State Represen-<br>tation|Simulation|
|Yu et al. [171]|LLM-based<br>Re-<br>ward Translator|LLM, VLM|GPT-4|Yes|Simulated<br>quadruped<br>robot,<br>dexterous manipu-<br>lator robot tasks|Reward Signal|Simulation|
|Dalal et al. [41]|Plan-Seq-Learn<br>(PSL)|LLM|GPT-4|Yes|Challenging<br>robotics<br>tasks<br>benchmarks|Planning & Ex-<br>ploration|Simulation|
|Song et al. [135]|Self-Refined<br>Large Language<br>Model|LLM|GPT-4|Available<br>Soon|Various continuous<br>robotic<br>control<br>tasks|Reward Signal|Simulation<br>(NVIDIA<br>Isaac<br>Gym)|
|Xie et al. [163]|Text2Reward<br>Framework|LLM|GPT-4|Yes|ManiSkill2,<br>Meta-<br>World, MuJoCo|Reward Signal|Simulation|
|Triantafyllidis<br>et<br>al.<br>[143]|Intrinsically<br>Guided<br>Ex-<br>ploration<br>from<br>Large Language<br>Models<br>(IGE-<br>LLMs)|LLM|GPT-4|N/A|Robotic manipula-<br>tion tasks|Planning & Ex-<br>ploration|Simulation|


Table 2: Summary of large language models as tools for RL. 

text, compared to LLM frameworks such as EUREKA [101]. The computational demand of VLMs remains significant, if not greater than that of LLMs. Few methods [146, 151] aim to mitigate this by solving RL tasks without excessive computational costs or calling the model inference at lower frequency. Moreover, fine-tuning VLMs to optimize their responses for RL specific tasks remains sometimes necessary [70]. The effectiveness of VLMs in RL also de- 

12 

pends on the choice of architecture— _e.g._ , several works use specialized modules such as CLIP (Contrastive Language-Image Pre-Training), a model that predicts the most relevant text sequence given an image [124, 134, 136], while others use general-purpose foundation models like GPT-4—and experimental setup, inheriting the issues of LLMs. Some studies focus on simulation environments with synthetic data [151], while others explore real-world robotic applications [98], leading to variations in prompting strategies, RL methodologies, and evaluation metrics. Notably, in Table 3 some models are used primarily for reward generation—similar to LLMs but based on visual input ( _e.g._ , _Reward Generation_ in Venuto et al. [146])—while others use VLMs to define the goal task or condition the learning to it (classified as _State Representation_ ), as seen in Cui et al. [40]. See Section 5 for more details on column _Task_ . 


Figure 4: **Generative AI tools for RL.** 

## _3.3. Diffusion Model_ 

Diffusion models, known for success in image generation [129, 50], are emerging in RL [95, 79, 137, 59, 82, 145, 65, 122, 75, 30]. Unlike models that use only textual or visual inputs, diffusion models can also operate directly in the trajectory space, generating continuous actions [185, 115]. These models learn to reverse a diffusion process that adds noise to states, rewards or policy parameters, generating new quantities from random noise. This approach 

13 

|**Paper**|**Framework**|**Base**<br>**Model/**<br>**Architecture**|**Network**|**Code**|**Training Data**|**Task**|**Simulation**<br>**or**<br>**Real-World Exp.**|
|---|---|---|---|---|---|---|---|
|Cui et al. [40]|Zero-Shot<br>Task<br>Specification<br>(ZeST)|VLM|ImageNet-<br>supervised<br>ResNet50,<br>ImageNet-trained<br>MoCo, CLIP|N/A|Simulated<br>robot<br>manipulation tasks<br>and<br>real-world<br>datasets|State Represen-<br>tation|Simulation|
|Venuto et al. [146]|VLM-CaR<br>(Code<br>as<br>Re-<br>ward)|VLM|GPT-4|N/A|Discrete<br>and<br>continuous<br>envi-<br>ronments|Reward Signal|Simulation|
|Adeniji et al. [3]|Language<br>Re-<br>ward Modulated<br>Pretraining<br>(LAMP)|VLM,<br>World<br>Model|CLIP|Yes|Ego4D,<br>video<br>Dataset, automat-<br>ically<br>Generated<br>language Dataset|Reward Signal|Simulation|
|Ma et al. [102]|Language-Image<br>Value<br>Learning<br>(LIV)|VLM|CLIP with ResNet<br>50 backbone|Yes|EpicKitchen,<br>sim-<br>ulated<br>and<br>real-<br>world robot envi-<br>ronments|Reward Signal|Simulation + Real-<br>World|
|Wang et al. [151]|RL-VLM-F|VLM|Gemini and GPT-4<br>Vision|Yes|Various<br>domains<br>including<br>classic<br>control and manip-<br>ulation tasks|Reward Signal|Simulation|
|Sontakke et al. [136]|RoboCLIP|VLM|S3D|Yes|Howto100M|Reward Signal|Simulation|
|Yang et al. [167]|ROBOFUME|VLM, LLM|MiniGPT4|Available<br>soon|Diverse<br>datasets,<br>real robot experi-<br>ments|Reward Signal|Simulation + Real-<br>World|
|Di Palo et al. [42]|Unified<br>Agent<br>with Foundation<br>Models|VLM, LLM|CLIP, FLAN-T5|N/A|Image<br>and<br>Text<br>datasets|State Represen-<br>tation|Simulation|
|Rocamonde<br>et<br>al.<br>[128]|Zero-Shot<br>Vision-Language<br>Models<br>(VLM-<br>RMs)|VLM|CLIP|Yes|Human<br>motion<br>task dataset|Reward Signal|Simulation|
|Baumli et al. [10]|Vision-Language<br>Models (VLMs)<br>like CLIP|VLM|CLIP|N/A|Playhouse|Reward Signal|Simulation|
|Chen et al. [33]|PR2L (Prompt-<br>able Representa-<br>tions for RL)|VLM, LLM|Vicuna-7B version<br>of<br>the<br>Instruct-<br>BLIP, a Llama2-7B<br>Prismatic VLM|Yes|Minecraft, Habitat<br>environments|State Represen-<br>tation|Simulation|
|Mahmoudieh<br>et<br>al.<br>[104]|Zero-Shot<br>Re-<br>ward<br>Model<br>(ZSRM)|VLM|ResNet-50|N/A|Large<br>dataset<br>of<br>captioned images|Reward Signal|Simulation|
|Ma et al. [98]|ExploRLLM|VLM, LLM|GPT-4|N/A|Image-based robot<br>manipulation tasks<br>dataset|Planning & Ex-<br>ploration|Simulation + Real-<br>World|


Table 3: Summary of vision-language models as tools for RL. 

has several advantages. First, it promotes behavior diversity, encouraging exploration and the discovery of novel solutions by generating a wide range of control policies. Second, it is well-suited for tasks with continuous action spaces, thereby avoiding the suboptimal performance that can arise from discretization. Finally, it improves sample efficiency by learning from limited demonstrations, reducing the need for extensive data collection [61, 184, 152]. The ability of diffusion models to be conditioned on language instructions or goal prompts enhances adaptability, making zero-shot policy generation possible. While still early in development, diffusion models offer new perspectives compared to more widely explored LLMs and VLMs [161, 91, 115]. 

14 

|**Paper**|**Framework**|**Base**<br>**Mod-**<br>**el/**<br>**Archi-**<br>**tecture**|**Code**|**Training Data**|**Task**|**Simulation**<br>**Real-Worl**|**or**<br>**d Exp.**|
|---|---|---|---|---|---|---|---|
|Lu et al. [95]|Contrastive En-<br>ergy<br>Prediction<br>(CEP)|Diffusion<br>model|Yes|D4RL benchmarks|State Represen-<br>tation|Simulation<br>benchmarks|(D4RL<br>)|
|Kang et al. [79]|EDP|Diffusion<br>model|Yes|D4RL benchmark datasets|State Represen-<br>tation|Simulation<br>benchmark)|(D4RL<br>|
|Suh et al. [137]|Score-Guided<br>Planning (SGP)|Diffusion<br>model|Yes|Cart-pole system, D4RL bench-<br>mark (MuJoCo tasks), pixel-<br>based single integrator environ-<br>ment|Planning & Ex-<br>ploration|Simulation <br>simulations|(Various<br>)|
|Hansen-Estruch<br>et<br>al.<br>[59]|Implicit<br>Diffu-<br>sion Q-Learning<br>(IDQL)|Diffusion<br>model|Yes|D4RL benchmark (halfcheetah,<br>hopper,<br>walker2d,<br>antmaze),<br>Maze2D|State Represen-<br>tation|Simulation<br>benchmark,<br>Maze2D)|(D4RL|
|Kim et al. [82]|DuSkill|Diffusion<br>Model|N/A|Rule-based<br>expert<br>policies,<br>multi-stage Meta-World tasks<br>(slide puck, close drawer)|State Represen-<br>tation|Simulation<br>stage Meta-|(Multi-<br>World)|
|Venkatraman et al. [145]|LDCQ|Diffusion<br>Model, World<br>Model|N/A|MuJoCo<br>benchmarks<br>(Hop-<br>per,<br>Walker,<br>Ant),<br>Maze2D,<br>AntMaze,<br>FrankaKitchen,<br>CARLA|State Represen-<br>tation|Simulation <br>environmen|(Various<br>ts)|
|Hu et al. [65]|Temporally-<br>Composable<br>Diffuser (TCD)|Diffusion<br>Model|N/A|Gym-MuJoCo<br>environments<br>(HalfCheetah,<br>Hopper,<br>Walker2D),<br>Maze2D,<br>Hand<br>Manipulation tasks|State Represen-<br>tation|Simulation<br>MuJoCo,<br>Hand Mani|(Gym-<br>Maze2D,<br>pulation)|
|Psenka et al. [122]|Q-Score Match-<br>ing (QSM)|Diffusion<br>Model|Yes|DeepMind<br>Control<br>Suite<br>(Cartpole<br>Balance,<br>Cartpole<br>Swingup, Cheetah Run, Hopper<br>Hop,<br>Walker<br>Walk,<br>Walker<br>Run,<br>Quadruped Walk,<br>Hu-<br>manoid Walk)|State Represen-<br>tation|Simulation<br>Mind Contr|(Deep-<br>ol Suite)|
|Jain<br>and<br>Ravanbakhsh<br>[75]|Merlin|Diffusion<br>Model|N/A|PointReach,<br>PointRooms,<br>Reacher, SawyerReach, Sawyer-<br>Door, FetchReach, FetchPush,<br>FetchPick,<br>FetchSlide,<br>Han-<br>dReach|State Represen-<br>tation|Simulation <br>simulated<br>ments)|(Various<br>environ-|
|Zhu et al. [185]|MADIFF|Diffusion<br>Model|Yes|Multi-agent<br>particle<br>environ-<br>ments,<br>MA<br>Mujoco,<br>Star-<br>Craft<br>Multi-Agent<br>Challenge<br>(SMAC), NBA dataset|State Represen-<br>tation|Simulation<br>agent envir|(Multi-<br>onments)|
|Ni et al. [115]|MetaDiffuser|Diffusion<br>Model|Yes|MuJoCo benchmarks (Hopper-<br>Param, Walker-Param), Point-<br>Robot 2D navigation|State Represen-<br>tation|Simulation<br>JoCo, Point|(Mu-<br>-Robot)|
|Chen et al. [30]|SfBC|Diffusion<br>Model|N/A|D4RL<br>benchmarks,<br>AntMaze<br>tasks, Maze2d, FrankaKitchen,<br>Bidirectional-Car tasks|State Represen-<br>tation|Simulation <br>benchmarks|(Various<br>)|


Table 4: Summary of diffusion models as tools for RL. 

Their iterative process allows for fine adjustments, making them ideal for complex tasks like grasping and balancing [85]. Additionally, their capacity to model complex dynamics and manage noise and uncertainty makes them robust in real-world robotic environments. However, their effectiveness in high-dimensional tasks is limited [61, 182, 92] and issues such as sensitivity to training data persist. We investigate further these aspects in Section 5 and we classify diffusion-based papers in Tables 4 and 5. 

15 

|**Paper**|**Framework**|**Base**<br>**Mod-**<br>**el/**<br>**Archi-**<br>**tecture**|**Code**|**Training Data**|**Task**|**Simulation**<br>**or**<br>**Real-World**<br>**Exp.**|
|---|---|---|---|---|---|---|
|Liang et al. [91]|AdaptDiffuser|Diffusion<br>Model|Yes|Synthetic expert data|Planning & Explo-<br>ration|Simulation<br>(Maze2D,<br>Mu-<br>JoCo)|
|He et al. [61]|Multi-Task<br>Dif-<br>fusion<br>Model<br>(MTDIFF)|Diffusion<br>model|N/A|Meta-World and Maze2D<br>environments|Planning & Explo-<br>ration|Simulation<br>(Meta-World,<br>Maze2D)|
|Brehmer et al. [17]|EDGI|Diffusion<br>Model, World<br>Model|N/A|Offline trajectory datasets<br>(3D<br>navigation,<br>Kuka<br>robotic arm)|Planning & Explo-<br>ration|Simulation|
|Li et al. [88]|Hierarchical Dif-<br>fusion (HDMI)|Diffusion<br>model, World<br>Model|N/A|Maze2D,<br>AntMaze,<br>D4RL<br>environments,<br>NeoRL benchmark|Planning & Explo-<br>ration|Simulation<br>(Various<br>envi-<br>ronments)|
|Xiao et al. [160]|SafeDiffuser|Diffusion<br>model|Yes|Maze2D<br>environments,<br>MuJoCo<br>environments<br>(Walker2D,<br>Hopper),<br>Pybullet environments|Planning & Explo-<br>ration|Simulation<br>(Multiple<br>envi-<br>ronments)|
|Chen et al. [29]|Hierarchical Dif-<br>fuser|Diffusion<br>Model, World<br>Model|N/A|Maze2D<br>(U-Maze,<br>Medium,<br>Large),<br>Multi2D,<br>AntMaze,<br>Gym-MuJoCo, FrankaK-<br>itchen|Planning & Explo-<br>ration|Simulation<br>(Various bench-<br>marks)|
|Kim et al. [81]|Sub-trajectory<br>Stitching<br>with<br>Diffusion (SSD)|Diffusion<br>Model|Yes|Maze2D<br>environments,<br>Fetch environments|Planning & Explo-<br>ration|Simulation<br>(Maze2D, Fetch)|
|Lee et al. [85]|Restoration<br>Gap<br>Guidance<br>(RGG)|Diffusion<br>model|Yes|Maze2D<br>environments,<br>Gym-MuJoCo<br>locomo-<br>tion tasks, block stacking<br>tasks<br>with<br>Kuka<br>iiwa<br>robotic arm|Planning & Explo-<br>ration|Simulation<br>(Multiple<br>envi-<br>ronments)|
|Zhang et al. [174]|Language<br>Con-<br>trol<br>Diffusion<br>(LCD)|Diffusion<br>Model|Yes|CALVIN<br>language<br>robotics<br>benchmark,<br>CLEVR-Robot<br>bench-<br>mark|Planning & Explo-<br>ration|Simulation<br>(CALVIN,<br>CLEVR-Robot)|
|Janner et al. [76]|Diffuser|Diffusion<br>Model|Yes|Maze2D<br>environments,<br>block<br>stacking<br>tasks,<br>D4RL locomotion suite|Planning & Explo-<br>ration|Simulation<br>(Multiple<br>envi-<br>ronments)|
|Nuti et al. [117]|Relative Reward<br>Function|Diffusion<br>model|Yes|Maze2D, D4RL locomo-<br>tion tasks, I2P dataset|Reward Signal|Simulation<br>(Maze2D,<br>D4RL)|
|Mazoure et al. [108]|Diffused<br>Value<br>Function (DVF)|Diffusion<br>Model, World<br>Model|N/A|Maze2D<br>environments,<br>PyBullet<br>environments,<br>D4RL offline suite|Reward Signal|Simulation<br>(Multiple<br>envi-<br>ronments)|


Table 5: Summary of diffusion models as tools for RL (continued). 

## _3.4. World Model and Video Prediction Model_ 

World models in RL introduce new methods for learning representations and dynamic models that serve as internal simulators for planning and prediction in RL [159, 109, 60, 172]. Typically, a world model consists of an encoder that incorporates environmental observations, a dynamics model that is learned during pre-training and allows for internal simulation, and an optional decoder that reconstructs information from the latent space. A reward model, which forecasts rewards based on the learned representation, might 

16 

also be included. Although they are not commonly employed as primary dynamic predictors, LLMs and VLMs have recently being integrated into world models. LLMs are mainly used for high-level reasoning and task specification [149, 116], while VLMs [109] support state representation by providing rich visual-linguistic embeddings. The core transition dynamics are typically modeled using architectures like RNNs, transformers, or diffusion models. 

Table 7 demonstrates that _State Representation_ is the primary use of world models, with almost all works concentrating on this function [57, 109, 158, 150]. Few studies focus on _Reward Signal_ generation [116, 27], or _Planning & Exploration_ [169, 170] as the main tasks. With little application to real-world data, the majority of the studied techniques are trained and assessed in simulated contexts. Though, few works [149, 133, 170, 27], include real-world experiments. 

Video prediction models, special models that learn the temporal dynamics of a visual environment, have also proved good results in visual RL, with frameworks like VIPER [49]. However, the main limitation is the reliance on specific environments for training [27, 7]. 

See Table 6 for a comparison between features of VPMs and WMs for RL, where _action-conditioned_ means that the model’s prediction can be influenced also by the action taken by the RL agent, and Sections 5 for more details. 

|**Feature**|**Video Prediction Models**|**World Models**|
|---|---|---|
|**Output**|Future frames (pixels)|Latent states, frames, rewards<br>|
|**Use Case**|Future frame generation|Future state/control generation|
|**Reward Modeling**|Rarely included|Often included|
|**Action-Conditioned**|No|Usually|


Table 6: **Comparison between video prediction models and world models for RL.** 

## **4. Modality** 

This section focuses on the classification of five types of generative AI models used in RL, as introduced in Section 3, with an emphasis on how their input/output modalities shape their role within RL frameworks. 

Bridging the gap between symbolic concepts and real-world experience is a concept referred to as _grounding_ , introduced in Section 1. Our classification highlights a fundamental trade-off between abstraction and grounding: while LLMs [47, 2] and VLMs [8, 176, 16, 183, 33] are adept at abstract reasoning 

17 

|**Paper**|**Framewo**|**rk**|**Model**<br>**Class**|**Code**|**Training Data**|**Task**||**Simulation**<br>**or**<br>**Real-World**<br>**Exp.**|
|---|---|---|---|---|---|---|---|---|
|Ha and Schmidhuber [57]|MDN-RN|N|World Model|Yes|CarRacing-v0,<br>DoomTakeCover-v0|State<br>tion|Representa-|Simulation|
|Wang et al. [149]|GENSIM <br>4,<br>G<br>Code Lla|(GPT-<br>PT-3.5,<br>ma)|World Model,<br>LLM|Yes|Generated 100 tasks from<br>a task library|State<br>tion|Representa-|Simulation<br>+<br>Real-World|
|Mazzaglia et al. [109]|MFWM<br>based,<br>Video2)|(GRU-<br>Intern-|World Model,<br>LLM, VLM|Yes|Walker,<br>Cheetah,<br>Quadruped,<br>Stickman,<br>Kitchen|State<br>tion|Representa-|Simulation|
|Wu et al. [158]|iVideoGP|T|World Model|Yes|OXE<br>Dataset,<br>SSv2,<br>RoboNet|State<br>tion|Representa-|Simulation|
|Mao et al. [106]|Segment<br>thing<br>(SAM),<br>(GPT-3.5|Any-<br>Model<br>LLMs<br>)|World Model,<br>LLM|N/A|Cart Pole, Lunar Lander|State<br>tion|Representa-|Simulation|
|Bruce et al. [20]|Genie<br>Transform|(ST-<br>er)|World Model|N/A|Platformers<br>dataset,<br>robotics dataset|State<br>tion|Representa-|Simulation|
|Yang et al. [169]|Observati<br>Prediction<br>Model<br>Diffusion|on<br><br>(Video<br>f Model)|World Model,<br>VLM,<br>Diffu-<br>sion Model|N/A|Simulated environments,<br>real robot data, human<br>activity videos, panorama<br>scans|Planni<br>ration|ng & Explo-|Simulation|
|Seo et al. [132]|Masked<br>Models (|World<br>MWM)|World Model|Yes|Meta-world, RLBench|State<br>tion|Representa-|Simulation|
|Seo et al. [133]|Multi-Vie<br>Masked<br>Models<br>MWM)|w<br>World<br>(MV-|World Model|Yes|RLBench|State<br>tion|Representa-|Simulation<br>+<br>Real-World|
|Ye et al. [170]|Foundatio<br>Actor-Cri<br>(FAC)|n<br>tic|World Model,<br>Diffusion<br>Model|N/A|Internet-scale<br>robotics<br>datasets, Meta-World|Planni<br>ration|ng & Explo-|Simulation<br>+<br>Real-World|
|Chen et al. [27]|Domain-<br>agnostic<br>Discrimin<br>(DVD)|Video<br>ator|World Model|N/A|Something-Something-<br>V2,<br>robot<br>videos<br>in<br>various environments|Rewar|d Signal|Simulation<br>+<br>Real-World|
|Nottingham et al. [116]|DECKAR|D|World Model,<br>LLM|Yes|Minecraft environment|Rewar|d Signal|Simulation|
|Zala et al. [172]|EnvGen||World Model,<br>LLM|Yes|Generated<br>and<br>original<br>environments|State<br>tion|Representa-|Simulation|
|Wang et al. [150]|RoboGen<br>ative Sim|Gener-<br>ulation|World Model,<br>LLM|Yes|Generated tasks, scenes|State<br>tion|Representa-|Simulation|


Table 7: Summary of world models as tools for RL. 

and symbolic processing, their input/output operations are less directly tied to physical control [24, 12, 37, 5, 101, 163]. On the other hand, diffusion models, by generating low-level, continuous control actions and operating directly in the action space, provide a more sample-efficient approach to policy learning [63, 129, 152, 35, 184, 76], though they may lack the higherlevel abstraction capabilities inherent to larger language models. Models that can effectively fuse abstraction and grounding for low-level action generation in robotics remain limited, although world models [159, 132, 169] and video prediction models [49, 45] represent promising approaches by integrating both 

18 

high-level abstraction and grounded sensory information. 

The diagram in Figure 4b shows that, based on our analysis, each generative AI tool used in RL contributes distinct input/output modalities. LLMs, working with text as both input and output excel at symbolic reasoning and can synthesize or interpret textual inputs such as task goals, environment documentation, or learned RL primitives, enabling them to produce reward signals or task refinements aligned with high-level objectives [101, 103]. VLMs, in contrast, can process visual inputs and generate reasoning over visual scenes. This makes them valuable for visual feedback mechanisms [151]. Their ability to bridge visual and textual modalities allows flexible integration into tasks where visual context is critical. Diffusion models can be highly specialized for policy learning and state generation, as they can model complex distributions over low-level states and actions. Operating directly in continuous action spaces, they can produce precise control signals that are easily integrated with RL algorithms [35, 71]. This modality specificity makes them ideal for applications in robotics and control where fine-grained action generation is required. Lastly, world and video prediction models, with their broad support for multi-modal input fusion and internal representation learning capacity, provide an even more flexible foundation. They can incorporate and generate rich multi-modal state representations (including visual, textual, proprioceptive, and other sensory data), making them well-suited for learning predictive models of environment dynamics and for supporting planning and model-based RL [159, 132, 169]. 

The level of abstraction and the size of the models (in terms of parameters) strongly influence how easily they can be integrated into the RL training loop. Larger, more powerful, and generalist models ( _e.g._ , current LLMs, which are text-based) can be quickly incorporated in a zero-shot fashion in several frameworks [101, 103]. However, they are often less tailored and less adaptable to the specific input/output requirements of RL tasks. Moreover, the choice of model—whether a diffusion model, an LLM, or a VLM—directly impacts the integration strategy within RL frameworks. Different models impose distinct computational demands and offer varying levels of flexibility in adapting to real-world dynamics [61, 180, 71]. The diagram in Figure 4b visually summarizes these trade-offs across models, mapping representative tools based on their degree of symbolic reasoning and grounding in physical control. This complements our analysis of modality diversity and integration strategies by illustrating how models such as **UniSim** , **EUREKA** , **RL-VLM-F** , **Reward Diffusion** , and **KCGG** occupy different positions 

19 

in this space. 

## **5. Task** 

RL tries to perform optimal decision-making considering the interaction of an agent ( _e.g._ , a robot) with its environment, with the goal of maximizing rewards [140, 11]. In the RL framework, several core components play essential roles in guiding the agent’s behavior. First, we have _states_ , which represent all possible situations the agent might encounter within its environment. At any given moment, the agent will find itself in a particular state, prompting it to consider the best _action_ ( _e.g._ , the action that maximizes the reward). These actions are the set of choices available to the agent, allowing it to interact with and influence the environment. The _policy_ represents the probability of taking action given a state ( _e.g._ , it’s the agent’s strategy). As the agent takes actions, it receives feedback from the environment through the _reward function_ , which assigns immediate rewards based on the outcome of each action. This reward signal helps the agent understand how to act optimally to achieve long-term goals. Two key functions support the agent in making more informed decisions over time. The _value function_ estimates the expected long-term return of being in a particular state, giving the agent an idea of how promising that state is under the current policy. The _Q-function_ , on the other hand, is slightly more detailed. It assesses the expected return not just for states, but also for specific actions taken within those states, enabling the agent to evaluate the quality of particular actions in given situations. One of the biggest challenges in RL is designing an effective reward function [139, 101]. A poorly designed reward system can mislead the agent, resulting in suboptimal or unintended behaviors. Crafting rewards that properly guide the agent toward good outcomes is crucial. Other two significant challenges are representing the state space and exploring it. If states are not represented accurately or comprehensively, the agent may struggle to learn the true dynamics of the environment, which can impede its ability to make optimal decisions [111]. 

This section reviews key works that exemplify how generative models have been employed to address critical aspects of the RL training loop in robotics, specifically focusing on: (i) _Reward Signal_ generation in the presence of sparse rewards and under goal specification constraints, (ii) _State Representation_ learning to improve sample efficiency, and (iii) _Planning & Exploration_ mechanisms that support generalization to new tasks. Based on 

20 

the modality and purpose of the generative models employed in relation to the RL _Task_ , the works are categorized and examined. A more thorough classification of the basic models under examination is provided in Table 8. 

|**Network**|**Reward Signal**|**State**<br>**Representa-**<br>**tion**|**Planning & Explo-**<br>**ration**|
|---|---|---|---|
|**LLM**|Textual<br>feedback|Textual state<br>encoding|High-level<br>guidance|
|**VLM**|Multi-modal|Multi-modal|Multi-modal|
||feedback|state encoding|evaluation|
|**DiffusionModel**|Reward|State|Action|
|**f **|generation|generation|sampling|
|**WMdVPM**|Reward|State|Model-based|
|**an **|prediction|prediction|planning|


Table 8: **Generative AI tools for RL integration.** Classification of generative AI models as tools based on integration into RL, as anticipated in Section 3 and Section 4. 

## _5.1. Reward Signal_ 

An increasing amount of research explores how generative AI models, particularly foundation models, can help automate or enhance reward design [94, 163, 135, 39, 44, 143, 24, 72, 101, 36, 13, 84, 3, 40, 86, 104, 128, 10, 27, 49]. These models offer new ways to interpret user input, perceive environments, and produce reward signals that guide effective policy learning. 

## _5.1.1. Reward design with LLMs_ 

Recently, LLMs such as GPT-4 [2] or Llama 3 [47], have been used to address the challenges of reward function design and direct reward specification. While LLMs struggle to directly control robots due to their ineffectiveness to produce control commands, they are highly valuable in evaluating the performance of RL agents, performing in-context reasoning on natural language problems. Traditionally, reward functions in RL are meticulously hand-crafted by researchers, often requiring significant domain expertise and limiting the agent’s ability to adapt to new situations. However, foundation models offer a compelling alternative by providing rich, generalist knowledge representations that can be leveraged to automatically generate or inform reward functions. Imagine a robot tasked with “cleaning the kitchen”. An LLM could identify sub-tasks like “wiping the table” and “putting dishes in the dishwasher” and assign rewards based on their successful completion. This structured approach breaks down complex tasks and provides clear goals for the RL agent. 

21 

Some approaches use LLMs for zero-shot reward generation [101, 163, 135] to convert natural language descriptions of desired behaviors into mathematical reward functions. TEXT2REWARD [163] and Self-Refined LLM [135] use LLMs to generate reward functions as executable code, while EUREKA [101] employs LLMs for evolutionary optimization of reward code. These methods leverage the LLM’s ability to understand task semantics and translate them into reward functions. Others leverage the in-context learning capabilities of LLMs to learn from demonstrations or feedback provided in natural language, shaping the reward function iteratively [39, 44, 143, 36, 171]. For example, Lafite-RL [36] uses LLM feedback to iteratively refine the reward function, employing few-shot learning to guide the LLM’s generation process; while Language to Rewards [171] uses LLM feedback to define reward parameters that are optimized for specific tasks. While TEXT2REWARD and Lafite-RL focus on generating dense reward functions that provide feedback at each timestep, other methods, like Language to Rewards, may generate sparse rewards that are only provided at the end of an episode. Some methods, such as EUREKA and Language to Rewards, incorporate interactive feedback from humans to refine the reward function. In FoMo Rewards [96], LLMs are employed to evaluate the likelihood of an instruction accurately describing a task given a trajectory of observations. This likelihood then serves as a reward signal. While the use of LLMs for reward function generation is still an emerging field, it shows significant promise for improving the development and deployment of intelligent agents. This approach can streamline the reward function design process, making it more general and task agnostic. Lastly, Nair et al. [113] showcase the use of LLMs to learn language-conditioned rewards from offline data and crowd-sourced annotations. This approach avoids the need for extensive human demonstrations, offering a scalable solution for learning complex behaviors. These different approaches highlight the versatility of LLMs in reward generation for RL in robotics, while the choice of approach depends on the specific requirements of the task and the available resources. However, one main drawback we found in existing work leveraging LLMs to craft rewards is that, since they work with text-only input, they are limited in acquiring perception from the real world [103]. This especially limits their capability to simulation environments where full state information is readily available. 

22 

## _5.1.2. Reward design with VLMs_ 

The integration of vision-language models [124, 125] in RL task evaluation represents a significant advancement over methods that rely solely on textual or numerical feedback [104, 128, 3, 10, 136, 151, 3, 40, 86, 167]. By leveraging the power of visual understanding, VLMs can be used for task evaluation [3, 40] based on prompts and image frames as input. 

Many robotic tasks involve interacting with a complex environment filled with diverse sensory information. Vision foundation models can leverage their ability to process different data modalities (text, images) to construct richer reward functions. Imagine a robot tasked with sorting laundry. A VLM could analyze an image of the clothing to identify the fabric type and color, and combine this information with text instructions to create a reward function that promotes sorting based on pre-defined categories, performing multi-modal reward learning. In Mahmoudieh et al. [104], Rocamonde et al. [128] and Adeniji et al. [3] VLMs are employed as zero-shot reward models. These approaches leverage the in-context learning ability of VLMs to evaluate if a visual scene coming from a camera sensor effectively match the language task description. This approach eliminates the need for manually designing reward functions or gathering extensive human feedback; moreover, it does not need environment state information. Differently, in RoboCLIP [136] rewards are generated by evaluating how closely the robot’s actions match the provided example. Interestingly, Code as Reward [146] utilizes VLMs to generate reward functions through code, thereby reducing the computational overhead of directly querying the VLM every time. Wang et al. [151] takes a slightly different route, querying VLMs to express preferences over pairs of image observations based on task descriptions, and subsequently learning a reward function from these preferences. 

## _5.1.3. Reward design with diffusion models_ 

Similar to other types of generative AI tools, diffusion models can be leveraged to infer rewards in RL. Huang et al. [71] and Nuti et al. [117] present methods for deriving reward functions by conditional diffusion models that are trained on expert visual demonstrations to generate rewards, similarly to the usage of diffusion models for conditional image generation [129]. On a different approach, Mazoure et al. [108] introduces the Diffused Value Function (DVF) algorithm, which leverages diffusion models to estimate value functions from states and actions, enhancing efficiency without explicitly learning rewards. They show improved long-term decisions. To conclude, diffusion 

23 

models are a relatively new approach to reward design, but they show strong promise; particularly due to adaptability, dense reward generation, and fast inference. We do not yet see immediate applications for text-conditioned reward generation. 

## _5.1.4. Reward design with video prediction_ 

The approaches for reward design presented so far in our taxonomy often lack accuracy in predicting changes in the robot’s visual state within the environment. Recent methods, such as those in Chen et al. [27] and Escontrela et al. [49], utilize the ability to predict future video frames based on current observations to shape rewards more effectively, leveraging environmental models ( _e.g._ , video prediction models) to enhance reward specification in RL systems. Specifically, Chen et al. [27] propose DVD, a discriminator that learns multi-task reward functions by classifying whether two videos perform the same task. This approach allows generalization to unseen environments and tasks by learning from a small amount of robot data and a large dataset of human videos. Escontrela et al. [49] introduce VIPER, which uses pre-trained VPMs to provide reward signals for RL based on frame observations rather than the actions the robot takes. VIPER achieves expert-level robot control across various tasks in simulations without predefined rewards, demonstrating the potential of VPMs for online reward specification during robotic task execution. At the same time, other researchers propose HOLD [7] and VIP [100]. This approaches generalize to unseen robot embodiments and environments, effectively accelerating RL training on various manipulation tasks zero-shot; the second one is trained on large-scale human videos. 

## _5.2. State Representation_ 

Foundation models can offer a promising avenue to address the challenge of more realistic state representations for data augmentation and training in RL [28, 116, 94, 116, 149, 169, 133, 150, 109, 158, 20]. However, the successful integration of foundation models as world representations for meaningfully training robots on augmented data and through model-based RL techniques hinges on addressing a fundamental issue mentioned many times in our discussion: _grounding_ . While these models excel at processing abstract representations, their ability to effectively model realistic scenarios depends on establishing a meaningful connection between these representations and the real-world objects or concepts they abstract [159]. This section surveys 

24 

research papers that utilize learned representations to predict and interact with environments in RL. 

## _5.2.1. Learning representations from videos_ 

Integrating VPMs with RL enhances the training of robots by allowing them to predict future frames from a sequence of previous images. VPMs forecast how a state will evolve, enabling the RL agent to plan actions and make decisions with more data-efficient learning and safer exploration, by anticipating future scenarios while reducing reliance on real-world trials [45, 170, 13, 105]. However, the success of this approach depends on the accuracy of the predictions, as well as managing the increased computational complexity, that often limits the possibility to use a single pre-trained model for a wide variety of robotics tasks. As a result, a common trend in research is to train or fine-tune different VPMs for specific applications, but future work could focus on scaling VPMs to improve their generalization. 

Du et al. [45] present UniPi, a unique approach that casts sequential decision-making as a text-conditioned video generation problem. UniPi leverages the knowledge embedded in language and videos to generalize to novel goals and tasks across diverse environments and to transfer effectively to downstream RL tasks. This approach enables multi-task learning and action planning, showcasing the potential of video generation for policy learning. Foundation RL [170] takes this objective a step further, they trained an RL model that leverages foundation priors from large-scale pre-training for embodied agents and they tested it on simulated robotic tasks. 

## _5.2.2. Foundation world models for model-based RL_ 

Many RL algorithms rely on accurate models of the environment’s dynamics to plan and make decisions [139]. World models [57], particularly those trained on data that includes physical interactions, can be used to learn these models of the world. The learned model can help the RL agent to predict the consequences of its actions ( _e.g._ , its future states) and make informed decisions based on predictions [159]. World models capture the action space of a robot. They can be constructed in a variety of ways, utilizing diverse data sources and employing different learning architectures. One recent approach to building a world model for abstract representation is through the use of large language models [116, 172, 149, 132, 133]. For example, Zala et al. [172] propose EnvGen, a framework where an LLM generates and adapts training environments for 

25 

small RL agents. By creating diverse environments tailored to specific skills, EnvGen enables agents to learn more efficiently in parallel. The LLM receives feedback on agent performance and iteratively refines the environments, focusing on weaker skills. On a similar approach Wang et al. [149] introduces GenSim, which uses GPT-4 [2] to automate the generation of diverse simulation tasks. Differently, Yang et al. [169] further advance the state-of-the-art in learning interactive real-world simulators for robotics as foundation models. They leverage diverse datasets, each rich in different aspects of real-world experience, to simulate the visual outcomes of both high-level instructions and low-level controls. The resulting simulator is used to train policies that can be deployed in real-world scenarios, showcasing the potential of bridging the sim-to-real gap in embodied learning. 

World models can also be trained at a very large scale from scratch, leading to the development of multi-modal foundation world models capable of generalizing greatly in vertical domains. Building on this for efficient robot training, Wang et al. [150] present RoboGen, a generative robotic agent that automatically learns diverse skills through environment simulation. Similarly, Mazzaglia et al. [109] introduce GenRL, a framework for model-based RL training of generalist agents, that learns a multi-modal foundation world model. Moreover, Wu et al. [158] presents iVideoGPT, a scalable autoregressive transformer framework for interactive world models. It is pre-trained on millions of human and robotic manipulation trajectories, demonstrating its versatility in various downstream tasks. While Mao et al. [106] focuses on zero-shot safety prediction for autonomous robots using foundation world models. They propose a world model that combines foundation models with interpretable embeddings, addressing the distribution shift issue in standard world models. Their approach demonstrates superior state prediction and excels in safety predictions, highlighting the potential of foundation models for safety-critical applications. Lastly, Bruce et al. [20] introduces Genie, the first generative interactive environment trained in an unsupervised manner from unlabeled Internet videos. 

While significant progress has been made in model-based RL and world models could unlock unlimited data availability for training, Wolczyk et al. [156] discuss the issue of catastrophic forgetting in post-training RL models, where pre-trained knowledge can be lost as new tasks are learned. This problem is particularly evident in compositional tasks, where different parts of the environment are introduced at different stages of training. 

26 

## _5.3. Planning & Exploration_ 

Policy learning refers to the process of determining a set of actions that can be executed to reach the desired target state for a given task [140, 54]. In this section, we briefly highlight interesting findings in the literature where generative AI models are used to learn effective policies for RL. In particular, two important concepts are exploration, which enables the agent to discover new states and maximize rewards, and planning, which involves combining skills to develop more comprehensive policies [94, 110, 122]. Various approaches leveraging LLMs, VLMs, and diffusion models have been explored to enhance both exploration and planning in RL settings [38, 65, 175, 33, 98, 40, 91, 182, 17]. 

## _5.3.1. LLMs for planning and exploration_ 

LLMs can be used for planning in RL, where the LLM acts as a strategic semantic planner, guiding the application of learned RL skills to new tasks based on task-specific prompts. Ahn et al. [5] and Huang et al. [72] introduce two methods that combines LLMs with pre-trained skills and affordance functions extracted from the RL training to ground language in robotic actions. The LLM is used to propose high-level actions, while the affordance functions, often learned through RL, determine the feasibility of these actions in the current context. This approach enables robots to execute complex tasks based on natural language instructions by ensuring that the proposed actions are both semantically relevant and physically feasible. Similarly, Plan-SeqLearn (PSL) [41], is a modular approach that uses motion planning to connect abstract language from LLMs with learned low-level control for solving long-horizon robotics tasks. PSL breaks down tasks into sub-sequences, uses vision and motion planning to translate these sub-sequences into actionable steps, and then employs RL to learn the necessary low-level control strategies. This approach enables robots to efficiently learn and execute complex tasks by leveraging the strengths of both LLMs and RL. 

Regarding exploration, Colas et al. [38] were the first to work on it by specifically incorporating language-driven imagination into RL. According to their IMAGINE architecture, “imagination” is the process of applying a learned goal recognizer to relabel prior experiences with other, languagebased objectives. By predicting which natural language descriptions could realistically correspond to an episode’s outcome, this methodology enables the agent to associate new hypothetical objectives with previous ones. The agent may efficiently learn from these relabeled goals by combining a modular 

27 

policy with a language-conditioned reward function. This improves generalization and exploration in a variety of language-specific tasks. The research underscores the critical role of language in enhancing creative, goal-driven exploration in RL. LLMs have shown promise in directly generating RL policies, instead of generating reward functions: GLAM [24], InstructRL [65], and BOSS [175], explore this, each with distinct approaches and contributions. GLAM focuses on grounding LLMs in interactive environments through online RL. It utilizes an LLM as the policy for an agent operating in a textual environment, refining the LLM’s understanding of the environment through continuous interaction and feedback. This approach aims to address the challenge of aligning the LLM’s knowledge with the actual environment dynamics, improving its ability to make decisions and achieve goals. The key innovation of GLAM lies in its online learning approach, where the LLM is not just pre-trained on existing data but actively learns and adapts as it interacts with the environment. This allows for a more dynamic and contextaware policy generation process. InstructRL, on the other hand, introduces a framework where humans provide high-level natural language instructions to guide the agent’s behavior. These instructions are used to generate a prior policy using LLMs, which then regularizes the RL objective. This approach aims to align the agent’s actions with human preferences and expectations, making it more suitable for collaborative tasks. InstructRL bridges the gap between human intentions and agent actions. The authors acknowledge that their work is limited by the challenges of abstracting certain actions, like continuous robot joint angles, into language, but they are optimistic about future advancements in multi-modal models expanding their applicability. Addressing the problem of generating realistic robotic policies and providing a more robust framework for translating abstract concepts into precise commands for robots, BOSS tackles the challenge of learning long-horizon tasks with minimal supervision. It starts with a set of primitive skills and progressively expands its skill repertoire through a bootstrapping phase. During this phase, the agent practices chaining skills together, guided by LLMs that suggest meaningful combinations. This approach enables the agent to learn complex behaviors autonomously, reducing the need for extensive human demonstrations or reward engineering. BOSS’s innovation lies in its ability to leverage the knowledge embedded in LLMs to guide the exploration and learning of new skills, making it a promising approach for developing generalist agents capable of performing a wide range of tasks. 

28 

## _5.3.2. VLMs for exploration_ 

Another major theme in the research is the use of FMs that work with images together with text to guide exploration in RL agents. VLMs offer deeper grounding in robotics applications compared to LLMs because they directly associate visual perception with the input task in text form and do not require a separate vision module for perception, hence enhancing efficient exploration based on goal evaluation [98, 102, 40]. By processing real-time sensory data from the robot ( _e.g._ , camera images), the model can identify unexpected situations or deviations from the expected plan. This information can be used to modify the reward function online, penalizing actions that lead to undesirable outcomes and encouraging exploration of alternative strategies. For example, if a robot attempting to pick up a cup encounters an obstacle, the foundation model could adjust the reward function to prioritize navigating around the obstacle before resuming the grasping attempt. As demonstrated by Cui et al. [40], VLMs can enable zero-shot task specification in robotic manipulation by supporting more general and user-friendly goal representations—such as internet images or hand-drawn sketches—which promote exploration more closely aligned with the intended task. Other studies, however, assert that general-purpose VLMs might struggle with exploration and result in agents that act too roughly, especially in online RL [33]. 

## _5.3.3. Diffusion models for planning and exploration_ 

Conventional RL planning techniques frequently use deterministic algorithms, which might perform poorly in complicated or unpredictable contexts [77, 48, 179]. Diffusion models, which were first created for generative tasks, have been modified to provide flexibility and stochasticity to the planning process in order to add robustness [91, 182, 17, 88, 61]. These models allow for flexible decision-making by iteratively converting noise into planned action sequences. One important strategy, Diffuser [76], combines RL with diffusion models to create reward-conditioned plans based on prior knowledge. It is excellent at long-term planning. To improve sample efficiency and generalization, extensions such as EDGI [17] treat planning as conditional sampling and add domain constraints. Other studies focus on safe planning, guaranteeing constraint satisfaction, and refining plans that are not feasible [160, 85]. Diffusion models also improve exploration by stochastically generating a wide range of possible states and objectives [153, 88, 174, 81, 29]. 

Lastly, diffusion models for planning and exploration works well in **offline** 

29 

**RL** , where we can train diffusion models to generate high-quality actions from large datasets or benchmarks [53, 95, 137, 79, 65, 59, 122, 75, 185, 82]. Some methods [137, 95], use gradient-based planning or energy functions to steer action generation and improve reward outcomes. Other works [79], focus on optimizing the sampling process to make diffusion models more practical and faster. Researchers also developed techniques like Implicit Diffusion Q-Learning [59] and Q-Score Matching [122], incorporating Q-learning ideas to better connect action choices with predicted rewards training offline [65, 63, 145, 129, 75]. 

## **6. RL Pre-Training** 

Until now, our survey has examined Generative AI as a tool within the RL pipeline ( _Generative Tools for RL_ ). We now turn the coin over and explore the converse perspective: using RL itself to _pre-train_ , _fine-tune_ , and _distill_ generative policy models. In _RL Pre-Training_ we survey methods that pre-train transformer- or diffusion-based policies with RL objectives. 

## _6.1. Transformer Policy_ 

Autoregressive transformer models were originally restricted to the domain of natural language, but they now form an integral part of RL, especially when the task can be framed as a sequential decision-making problem [68, 21, 87, 157, 126]. In particular, specialized adaptations of the Transformer architecture, such as Decision Transformers (DTs) [32], are becoming more popular. Like language models, DTs generate tokens ( _i.e._ , actions) one at a time, conditioned on the previous context, and use the Transformer to predict the next action in a sequence based on previous return, state, and action tuples. Recent transformer-based RL studies focus on scalability, adaptivity, and transferability [67, 84, 154, 165]. Results from Wen et al. [154] and Xu et al. [165] show how large models may generalize across various RL tasks. These methods show how transformer backbones can learn from little supervision and generalize well. HarmoDT [68], LATTE [21], and PACT [15] would be examples of such architectures that have trained transformers at scale for RL-based robotic control on real robots. Tackling a different problem, Q-Transformer [26] leverages offline data, human demonstrations, and trajectory rollouts to learn Q-functions with transformers so that robots can perform tasks appropriately. AnyMorph [142] pushes the 

30 

generalization frontier by adapting to different robot morphologies. We describe here the small number of DT variants applicable to robotics, but we envision that many RL problems may be addressed by foundation models utilizing DTs backbones [155]. Lastly, a major trend is merging language and reasoning into policies: Mezghani et al. [110] merge language generation with action prediction, allowing agents to reason in natural language while planning actions. This has not been validated directly in real-world robotics but gives an interesting approach for tasks which require long-term planning. Recently, GATO [126] emerged as a generalist agent due to its ability to execute tasks across modalities, spanning from gaming to real-world robotics, using a single transformer backbone that performs input fusion into a RL policy. 

|**Aspect**|**Transformer Autoregression**|**Diffusion Model**|
|---|---|---|
|**Generation Process**|Sequential, one step at a time.|Iterative, gradual refinement from<br>noise.|
|**Output Type**|Typically discrete (e.g., tokens, discrete<br>actions).|Typically continuous (e.g., trajecto-<br>ries, continuous actions).|
|**Training Objective**|Maximize likelihood of observed data.|Predict noise added during forward<br>diffusion.|
|**Inference Speed**|Faster (if same size).|Slower due to iterative refinement.|
|**Error Propagation**|Errors can compound over time.|Less prone to compounding errors.|
|**Expressiveness**|Highly expressive for sequential data.|Highly<br>expressive<br>for<br>continuous<br>data.|
|**Applications**|Discrete action RL policies.|Continuous action RL policies.|
|**RL Fine-tuning Ease**|Straightforward with standard RL algo-<br>rithms (e.g., PPO, Q-learning).|More complex, may require custom<br>integration with RL.|
|**Sample Efficiency**|Moderate; improves with pretraining.|High;<br>performs<br>well<br>in<br>low-data<br>regimes.|
|**Action Modeling**|Limited multi-modality; can struggle in<br>complex spaces.|Strong multi-modal capabilities; ex-<br>cels in complex control.|
|**Best For**|Long-horizon, complex reasoning tasks;<br>fast inference scenarios.|Smooth, continuous control; plan-<br>ning; multi-modal outputs.|


Table 9: **Comparison of generative policies.** Transformer autoregressive policies versus diffusion non-autoregressive policies in RL. 

## _6.2. Diffusion Policy_ 

Using iterative refinement instead of step-by-step prediction, diffusion models have recently acquired popularity as alternative to autoregressive techniques in robotic policy generation [35, 76] (see Table 9 for a comparison). They are ideal for dynamic robotic environments due to their ability to manage uncertainty and provide a variety of behaviors [74, 184, 152]. Diffusion models can model complicated or high-dimensional dynamics by refining probability distributions to construct action sequences, in contrast to classic RL methods that yield deterministic outputs [139, 61]. They can incorporate 

31 

constraints such as safety or energy efficiency and allow expressive, contextsensitive behaviors by directly modeling action distributions [115, 90]. Hegde et al. [62] present a method to condense a large archive of policies, trained using RL, into a single generative model. A diffusion model is then trained on these compressed representations to generate new policies conditioned on specific behaviors, either through quantitative measures or language descriptions. Other studies use diffusion models as policy in offline RL, improving performance and scalability [31, 43]. Moreover, Diffusion-QL [152] uses conditional diffusion to match IL with Q-learning while preserving demonstration data proximity and optimizing rewards. Lastly, frameworks such as Decision Diffuser [6] and DIPO [168], formulate the sequential decisionmaking problem as a conditional generative modeling problem using RL to train a diffuser. 

## **7. RL Fine-Tuning** 

Generative models, such as transformer-based and diffusion-based policies, are often trained with IL and they demand flexible RL fine-tuning strategies, if expert data for supervised fine-tuning (SFT) are limited. Recent works effectively integrate these expressive models into RL pipelines without instability or loss of efficiency [66, 107]. In this section, we explore two major classes of generative policies where we identified RL fine-tuning is particularly relevant, (i) large transformer policies (mostly VLA models), and (ii) diffusion policies (usually smaller in size). 

Recent advances in **Transformer-based policies** have transformed robotic control, with robotics foundation models excelling through large-scale pretraining. A major step toward generative policy architectures and datasets for robotics is the OpenX Embodiment project [119], which introduced the largest open-source real-robot dataset—the Open X-Embodiment Dataset. This dataset supports the development of pivotal VLA models like RT-X models [18, 19], Octo [118], and OpenVLA [80]. However, state-of-the-art generalist VLA policies are typically trained via IL and often require additional training to adapt to out-of-distribution scenarios [89, 99, 162, 69]. RL has become an alternative to improve policy performance, particularly when it comes to managing distribution shifts or leading generalist models toward specialization. This has motivated the development of new RL-based finetuning algorithms, particularly actor-critic methods [56, 93]. Actor-Critic approaches enable very reliable and effective policy updates by utilizing two 

32 

networks: the critic to assess actions and the actor to decide on them. This method aids in RL fine-tuning by continuously enhancing action selections in response to critic feedback [139]. Through the use of on-policy algorithms such as PPO, cautious learning rates, and distinct actor-critic networks, the FLaRe framework [66] demonstrates RL-based fine-tuning by matching pretrained transformer policies with new experience. FLaRe reduces the sim-toreal gap by using domain randomization and extensive simulations, increasing success rates by roughly +30 % on both real robots and in simulation. PPO is the recommended RL technique for VLA fine-tuning, according to Liu et al. [93]. Its advantages include shared actor-critic backbones, short training epochs, and great generalization on unseen objects and dynamic situations. However, the low-frequency action generation (reported in panel **a** in Figure 5a) of VLA models and the requirement of large amounts of interaction data even for minor adjustments, make online fine-tuning difficult and limited in rel world settings. Standard fine-tuning methods still need further exploration in case of VLA models, and current research focuses on large-scale RL fine-tuning for transformer policies [66]. 

An alternative area where RL fine-tuning shows potential is with **Diffusionbased policies** , which offer many possibilities with RL due to their ability to predict smooth trajectories non-autoregressively at each inference step [152, 34]. However, key problems in applying RL to diffusion policies are include the high-dimensional nature of the action space, the slow iterative denoising process involved in action generation, and training instability. Standard policy gradient methods have been viewed as inefficient for such models, due to the increased number of steps over which rewards must be predicted, introduced by iterative denoising [168]. Recent advances, such as Diffusion Policy Policy Optimization (DPPO), have demonstrated that RL can be effectively integrated with diffusion policies by formulating the denoising process as a Markov Decision Process [127]. This approach enables policy gradients to propagate through the diffusion steps, leveraging the structured noise removal process to facilitate more stable training. A major advantage of RL-fine-tuned diffusion policies is their ability to engage in on-manifold exploration, meaning that the policy remains close to the expert data distribution while still improving performance through RL. This structured exploration contrasts with traditional RL methods, which often struggle with off-manifold exploration, leading to unstable training and suboptimal policies [121]. Panel **b** of Figure 5a shows the working principle of diffusion policies, while panel **c** depicts the state-of-the-art methods for RL-based 

33 

## fine-tuning generative policies. 

In general, most research focuses on transformer-based or diffusion-based policy architectures separately, as they align with different goals and finetuning methods, although Actor-Critic RL is commonly used. While some researchers are exploring these pathways, others aim to develop a generalized RL-based fine-tuning framework for any generative policy, regardless of size and backbone model [107]. 


Figure 5: **Generative policies.** 

## **8. Policy Distillation** 

Policy distillation is a well-known concept in the RL literature [131]. Recently, with the emergence of large generalist generative policies, RL-based methods for policy distillation have been applied to VLA models. In particular, recent works have explored policy distillation in OpenVLA [80] and Octo [118]. The goal of policy distillation is to transfer pre-trained knowledge from a _teacher policy_ to a _student policy_ . The recent literature can be categorized into two opposing approaches: 

- **From Generalist to Expert:** Jülg et al. [78] developed a method to create task-specific RL agents distilled from a pre-trained VLA model. While VLA models are known for their strong generalization capabilities, they often struggle to achieve highly precise results compared to task-specific RL policies. The key 

34 

idea is that the internal knowledge of VLA models can be useful in guiding RL exploration for specific agents. However, this work primarily presents preliminary simulation results, emphasizing that sim-to-real transfer remains the main challenge when training RL policies in simulation. This is particularly relevant given that OpenVLA and Octo typically perform better in real-world conditions [119, 89]. 

- **From Experts to Generalist:** Xu et al. [164] propose a method to improve OpenVLA and Octo using demonstrations from expert RL policies. Their approach focuses on generating high-quality training data to fine-tune VLA models, as these models performance is highly dependent on the quality of their training data. Their experiments demonstrate that this method outperforms models trained solely on human demonstrations, achieving superior results in real-world precision manipulation tasks. 

## **9. Challenges, Recommendations and Future Research Directions** 

We organize challenges, recommendations and few important insights for the future into three macro-categories based on our taxonomy—Section 9.1 is related to challenges in _Generative Tools for RL_ , Section 9.2 presents challenges in _RL for Generative Policies_ and Section 9.3 is on _Future Research Directions_ . Each category addresses specific limitations and opportunities that must be tackled to enable scalable, safe, and adaptive robot learning that integrates generative AI and RL. 

## _9.1. Challenges in Generative Tools for RL_ 

Every generative model we discussed has unique advantages for RL; consequently, different generative AI models present distinct challenges, and we highlight those we identified as most urgent to be addressed. 

_LLMs for reward signals_ 

Despite their strength in symbolic reasoning, LLMs lack grounding in real-world tasks [37, 12]. Main challenges are: (i) **limited contextual understanding** [5, 72, 44, 39, 143, 41], (ii) **real-world reduced adaptability** [101, 103, 36, 96, 163] because most works are based on the assumption that the LLM has access to the environmental states from the simulation, and (iii) **symbolic-physical misalignment** [12, 37, 12, 24]. 

_Recommendation:_ Similarly to Ma et al. [103], we believe that LLMs can improve reward generation in real-world. Develop architectures that pair LLMs with RL controllers capable of translating high-level goals into more 

35 

controlled rewards. Employ LLM fine-tuning gradually increasing real-world sensor data exposure to avoid simulation environments dependency. 

_VLMs for reward signals and state representation_ 

VLMs excel at perception and language integration and they are more effective in real-world tasks than LLMs, but they struggle with translating visual-semantic representations into actionable RL policies. Challenges are: (i) **detailed scene understanding** [40, 146, 102, 151, 167, 33, 104, 98] and (ii) **inferring physical affordances or dynamics** [70, 3, 136, 42, 128, 10]. 

_Recommendation:_ Associate VLMs with with more meaningful information to improve precision: extracting pose of relevant objects, keypoints, or region of interest in the frames. Use positive and negative visual examples to generate semantic rewards, since it’s proved to be more effective than only positive ones by Huang et al. [70]. Use auxiliary tasks like affordance prediction to narrow the abstraction gap, and combine VLMs outputs with filtering mechanisms, as in Ahn et al. [5]. 

_Diffusion models for planning and exploration_ 

Diffusion models offer strong distribution modeling and short-term planning, but suffer from: (i) **in-context understanding** [184, 59, 122, 75, 30, 91, 182, 153, 17], (ii) **multi-modality extension** [137, 82, 145, 115, 61, 76], and (iii) **poor reasoning** [95, 79, 65, 185, 88, 160, 29]. 

_Recommendation:_ Embed hierarchical control into diffusion models to manage long-horizon planning; integrate LLMs for reasoning levels with lowlevel diffusion-based modules. Combine diffusion models with RL through receding-horizon approaches for stable planning, as shown in recent approaches [184]. Guide diffusion models generation by conditioning them on state information or meaningful variables [6]. 

## _World models and video prediction for environment modeling_ 

World models and video prediction models give agents the ability to “imagine” future without actually interacting with the environment, which is particularly helpful in situations with limited data. However, they have drawbacks: (i) **restricted generalization** [25, 57, 158, 106, 169], (ii) **compounding errors over extended rollouts** [144, 132, 133, 116, 172], and (iii) misalignment between actionable state representations and visual accuracy [149, 109, 20, 170, 150]. Similar to this, video prediction algorithms try to predict changes at the pixel level, but they frequently produce (i) 

36 

**misaligned forecasts** [27] and have (ii) **poor physically significant dynamics** [49] over time. 

_Recommendation:_ Use foundation world models [109] rather than video predictors for more robust representation learning. Employ stochasticity and uncertainty modeling to mitigate compounding errors in prediction. Augment world models with high-fidelity sensory data [20, 149]. Hybrid frameworks combining analytical simulators with learned models ( _e.g._ , [9]) can improve realism and transferability. Fine-tune video prediction models on task-specific environments and prefer them only for data augmentation or internal reward shaping. 

_Scalability and resource demand of foundation models in RL training_ 

Recent research draw attention to the difficulties of incorporating foundation models straight into the RL training loop, where RL training have (i) **memory limitations** [156, 157, 144] and foundation models have (ii) **high inference costs** [69, 162, 23] that reduce efficiency on complex tasks. 

_Recommendation:_ Give priority to modular architectures, such as Ma et al. [101]. Deploy distilled RL policies for low-latency real-world control and use foundation models mainly for offline learning and reasoning in the RL training loop. Create hybrid pipelines in which smaller controllers make decisions in real time, while LLMs or VLMs offer symbolic reasoning. 

## _9.2. Challenges in RL for Generative Policies_ 

_RL pre-training_ of generative policies is widely studied and shares challenges with classic RL training as described in prior work [111, 139, 112], we first focus on _RL fine-tuning_ , which presents new and specific open challenges unique to generative policies. While, unpredictability, safety verification, and robustness under uncertainty are inherent challenges that are common to both pre-training and fine-tuning. We highlight key open problems in these directions. 

## _Policy agnostic RL fine-tuning_ 

Fine-tuning of generative policies remains a critical challenge for deploying policies in real-world or dynamic environments. The main challenges are: (i) **obtaining new fine-tuning RL methods** and **fine-tuning methods independent from the backbone model** [157, 186, 34, 127], and (ii) **achieving good fine-tuning for any size of the policy** [66]. 

37 

_Recommendation:_ Investigate new specific methods for efficient RL finetuning of VLA models [66, 107], or smaller diffusion models [127]. Develop methods that are agnostic from the policy architecture, such as in Mark et al. [107]. 

_Online RL fine-tuning of VLA models_ 

Four major obstacles stand in the way of fine-tuning VLA models with RL: (i) **data gathering is expensive in real-world** , and VLA models are usually trained with real-world data through IL, limiting GPU parallelization in simulation [80, 119]. It is (ii) **computationally demanding to conduct online training** [66], and it is (iii) **difficult to assess VLA model performance** [89]. They also suffer from (iv) **catastrophic forgetting** [156, 157, 144]. 

_Recommendation:_ Leverage realistic simulations for massive training and few-shot real-world fine-tuning to close the gap between simulation and reality. Integrate offline RL pipelines to minimize the need for online training. Use distillation to condense huge VLA models into lightweight, task-specific policies that allow for effective RL deployment [78]. Test in simulations the VLA models using frameworks like [89]. Combine replay-based continual RL with regularization to mitigate forgetting [144, 25]. 

## _Safety and failure modes of generative policies_ 

Generative policies present serious safety and reliability issues in robotics, due to their black-box nature and absence of clear constraints. They may behave in an unpredictable manner. Challenges are: (i) **closed-loop verification** and (ii) **real-time monitoring** [68, 21, 87, 157, 126, 35, 76]. 

_Recommendation:_ Incorporate safety-aware control modules that monitor and oversee the outputs of generative policies, to enforce physical constraints, and direct policy correction in the face of uncertainty [4, 130, 54]. Create closed-loop systems that use environment feedback to continually test and improve policy behavior, and implement hybrid architectures where generative policies are constrained by explicit safety layers or fallbacks [120]. Apply verification techniques such as control barrier functions [114]. 

## _9.3. Future Research Directions_ 

We highlight three promising research directions based on our findings. 

38 

## _9.3.1. RL from human feedback_ 

Techniques such as RL from Human Feedback (RLHF) and related approaches (e.g., Preference Based RL [1]) have been used for aligning large language models and other generative systems to produce outputs that are both useful and aligned with human input[186, 97]. Future research should explore RLHF to fine-tune generalist generative policies—such as VLA models. However, evaluating robotic actions remains harder than assessing tasks like chatbot responses. 

## _9.3.2. Actor-critic foundation models_ 

A new research direction could be to develop specialized foundation models that act as critics in RL or generate in-context rewards zero-shot in realworld settings for policy training. Traditional RL depends on manually designed rewards, which can be limiting. Instead, specific foundation models can dynamically assess actions using multi-modal inputs, improving learning efficiency and adaptability with respect to generic LLMs [101]. 

## _9.3.3. Constraint-aware generative models with optimal control_ 

Based on recent advances in model-based training of IL policies [120, 161] and extending our discussion on safety in generative policies (Section 9), we propose that integrating constraint satisfaction methods from optimal control theory, such as control barrier functions, into RL presents a promising direction for safer and more grounded diffusion policies (as suggested in Figure 5b). Moreover, adaptive learning-based techniques that dynamically respond to changing environments can significantly enhance the deployment of diffusion policies across various control tasks, much like model predictive safety filters [147]. Our argument is further supported by recent works leveraging diffusion models within a receding horizon framework for control action execution [147, 178, 58, 166, 180, 123, 35], which integrate model predictive control frameworks obtaining stronger stability. 

## **10. Conclusion** 

The integration of generative AI models and RL marks a transformative advancement in robotics, enhancing reasoning and adaptability in complex tasks [36, 151, 101, 103, 163, 94, 71, 66]. This synergy combines the extensive knowledge and in-context learning of foundation models, the generative capabilities on multi-modal input fusion of generative AI and the high learning 

39 

capacity in decision-making of RL in robots. Our review critically examined this integration, with a focus on duality aspects between generative AI and RL for robot action generation; extracting policies from text, video and states information. We first studied how _Generative Tools for RL_ consist in a solid portion of research papers where LLMs and VLMs play a major role, and how the union of diffusion models and RL is a very exciting trend in this direction, that deserves further investigation. Moreover, the exploration of how RL can harness foundation world models to enhance model-based RL training further highlights the potential of this integration. Finally, we categorized preliminary work on the other side of our duality investigation— _RL for Generative Policies_ —and we focused on combining generative AI with RL in training, fine-tuning, and distilling generative policies. While the opportunities for such a research field are vast, we highlighted remaining challenges, notably in grounding abstract representations of foundation models to physical world concepts—an area needing significant exploration. We concluded that RL-based fine-tuning of robotic generative policies, along with the exploration of failure modes of black-box policies, remains underexplored. While, the scalability and computational demands of these systems pose substantial challenges, especially in resource-constrained environments, limiting the possibility of online training. Addressing these challenges is critical for building fully autonomous robots, controlled by generative AI models able to create policies from multi-modal inputs. Based on our findings, we shared promising research directions for the coming years. 

## **CRediT authorship contribution statement** 

**Angelo Moroncelli:** Writing – original draft, Writing – review and editing, Visualization, Methodology, Investigation, Software, Formal analysis, Conceptualization. **Vishal Soni:** Writing – original draft, Writing – review and editing, Visualization, Investigation, Software. **Marco Forgione:** Writing – review and editing. **Dario Piga:** Writing – review and editing. **Blerina Spahiu:** Writing – review and editing, Methodology, Conceptualization, Supervision. **Loris Roveda:** Writing – review and editing, Supervision, Project administration, Funding acquisition, Conceptualization. 

## **Declaration of competing interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work 

40 

reported in this paper. 

## **Acknowledgements** 

The authors would like to thank the Hasler Foundation for providing funding to carry out our research. Our work was partially supported by the GeneRAI (Generative Robotics AI) project, funded by Hasler Stiftung. 

## **Data availability** 

No data was used for the research described in the article. 

## **Declaration of generative AI and AI-assisted technologies in the writing process** 

During the preparation of this work, the author(s) used ChatGPT in order to check and improve the grammar and clarity of the text. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the published article. 

## **References** 

- [1] Abdelkareem, Y., et al., 2022. Advances in preference-based reinforcement learning: A review, in: 2022 IEEE SMC, pp. 2527–2532. 

- [2] Achiam, J., et al., 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774 . 

- [3] Adeniji, A., et al., 2023. Language reward modulation for pretraining reinforcement learning. arXiv preprint arXiv:2308.12270 . 

- [4] Agia, C., et al., 2025. Unpacking failure modes of generative policies: Runtime monitoring of consistency and progress, in: CoRL, PMLR. pp. 689–723. 

- [5] Ahn, M., et al., 2022. Do as i can, not as i say: Grounding language in robotic affordances. arXiv preprint arXiv:2204.01691 . 

- [6] Ajay, A., et al., 2022. Is conditional generative modeling all you need for decision-making? arXiv preprint arXiv:2211.15657 . 

41 

- [7] Alakuijala, M., et al., 2023. Learning reward functions for robotic manipulation by observing humans, in: 2023 IEEE ICRA, IEEE. pp. 5006–5012. 

- [8] Alayrac, J.B., et al., 2022. Flamingo: a visual language model for few-shot learning. NeurIPS 35, 23716–23736. 

- [9] Authors, G., 2024. Genesis: A universal and generative physics engine for robotics and beyond. 

- [10] Baumli, K., et al., 2023. Vision-language models as a source of rewards. arXiv preprint arXiv:2312.09187 . 

- [11] Beck, J., et al., 2023. A survey of meta-reinforcement learning. arXiv preprint arXiv:2301.08028 . 

- [12] Bhat, V., et al., 2024. Grounding llms for robot task planning using closed-loop state feedback. arXiv preprint arXiv:2402.08546 . 

- [13] Bhateja, C., et al., 2023. Robotic offline rl from internet videos via value-function pre-training. arXiv preprint arXiv:2309.13041 . 

- [14] Bommasani, R., et al., 2021. On the opportunities and risks of foundation models. arXiv preprint arXiv:2108.07258 . 

- [15] Bonatti, R., et al., 2023. Pact: Perception-action causal transformer for autoregressive robotics pre-training, in: 2023 IEEE/RSJ IROS, IEEE. pp. 3621–3627. 

- [16] Bordes, F., et al., 2024. An introduction to vision-language modeling. CoRR . 

- [17] Brehmer, J., et al., 2024. Edgi: Equivariant diffusion for planning with embodied agents. NeurIPS 36. 

- [18] Brohan, A., et al., 2022. Rt-1: Robotics transformer for real-world control at scale. arXiv preprint arXiv:2212.06817 . 

- [19] Brohan, A., et al., 2023. Rt-2: Vision-language-action models transfer web knowledge to robotic control. arXiv preprint arXiv:2307.15818 . 

42 

- [20] Bruce, J., et al., 2024. Genie: Generative interactive environments, in: ICML. 

- [21] Bucker, A., et al., 2023. Latte: Language trajectory transformer, in: 2023 IEEE ICRA, IEEE. pp. 7287–7294. 

- [22] Busetto, R., et al., 2024. In-context learning of state estimators. IFAC 58, 145–150. 

- [23] Cao, Y., et al., 2024. Survey on large language model-enhanced reinforcement learning: Concept, taxonomy, and methods. arXiv preprint arXiv:2404.00282 . 

- [24] Carta, T., et al., 2023. Grounding large language models in interactive environments with online reinforcement learning, in: ICML, PMLR. pp. 3676–3713. 

- [25] Chan, B., et al., 2024. Offline-to-online reinforcement learning for image-based grasping with scarce demonstrations, in: CoRL Workshop on Mastering Robot Manipulation in a World of Abundant Data. 

- [26] Chebotar, Y., et al., 2023. Q-transformer: Scalable offline reinforcement learning via autoregressive q-functions, in: CoRL, PMLR. pp. 3909–3928. 

- [27] Chen, A.S., et al., 2021a. Learning generalizable robotic reward functions from" in-the-wild" human videos. arXiv preprint arXiv:2103.16817 . 

- [28] Chen, B., et al., 2023a. Open-vocabulary queryable scene representations for real world planning, in: 2023 IEEE ICRA, pp. 11509–11522. 

- [29] Chen, C., et al., 2024a. Simple hierarchical planning with diffusion. arXiv preprint arXiv:2401.02644 . 

- [30] Chen, H., et al., 2022. Offline reinforcement learning via high-fidelity generative behavior modeling. arXiv preprint arXiv:2209.14548 . 

- [31] Chen, H., et al., 2023b. Score regularized policy optimization through diffusion behavior. arXiv preprint arXiv:2310.07297 . 

43 

- [32] Chen, L., et al., 2021b. Decision transformer: Reinforcement learning via sequence modeling. NeurIPS 34, 15084–15097. 

- [33] Chen, W., et al., 2024b. Vision-language models provide promptable representations for reinforcement learning. arXiv preprint arXiv:2402.02651 . 

- [34] Chen, Y., et al., 2025. Fdpp: Fine-tune diffusion policy with human preference. arXiv preprint arXiv:2501.08259 . 

- [35] Chi, C., et al., 2023. Diffusion policy: Visuomotor policy learning via action diffusion. arXiv preprint arXiv:2303.04137 . 

- [36] Chu, K., et al., 2023. Accelerating reinforcement learning of robotic manipulations via feedback from large language models. Arxiv preprint arXiv:2311.02379 . 

- [37] Cohen, V., et al., 2024. A survey of robotic language grounding. arXiv preprint arXiv:2405.13245 . 

- [38] Colas, C., et al., 2020. Language as a cognitive tool to imagine goals in curiosity driven exploration. NeurIPS 33, 3761–3774. 

- [39] Colas, C., et al., 2023. Augmenting autotelic agents with large language models, in: CLLA, PMLR. pp. 205–226. 

- [40] Cui, Y., et al., 2022. Can foundation models perform zero-shot task specification for robot manipulation?, in: LDCC, PMLR. pp. 893–905. 

- [41] Dalal, M., et al., 2024. Plan-seq-learn: Language model guided rl for solving long horizon robotics tasks. arXiv preprint arXiv:2405.01534 . 

- [42] Di Palo, N., et al., 2023. Towards a unified agent with foundation models. arXiv preprint arXiv:2307.09668 . 

- [43] Ding, Z., Jin, C., 2023. Consistency models as a rich and efficient policy class for reinforcement learning. arXiv preprint arXiv:2309.16984 . 

- [44] Du, Y., et al., 2023a. Guiding pretraining in reinforcement learning with large language models, in: ICML, PMLR. pp. 8657–8677. 

44 

- [45] Du, Y., et al., 2023b. Learning universal policies via text-guided video generation. arXiv e-prints , arXiv–2302. 

- [46] Du, Z., et al., 2023c. Can transformers learn optimal filtering for unknown systems? IEEE Control Systems Letters 7, 3525–3530. 

- [47] Dubey, A., et al., 2024. The llama 3 herd of models. arXiv preprint arXiv:2407.21783 . 

- [48] Duchoň, F., et al., 2014. Path planning with modified a star algorithm for a mobile robot. Procedia engineering 96, 59–69. 

- [49] Escontrela, A., et al., 2024. Video prediction models as rewards for reinforcement learning. NeurIPS 36. 

- [50] Esser, P., et al., 2024. Scaling rectified flow transformers for highresolution image synthesis, in: ICML. 

- [51] Firoozi, R., et al., 2023. Foundation models in robotics: Applications, challenges, and the future. arXiv preprint arXiv:2312.07843 . 

- [52] Forgione, M., et al., 2023. From system models to class models: An in-context learning paradigm. IEEE Control Systems Letters . 

- [53] Fu, J., et al., 2020. D4rl: Datasets for deep data-driven reinforcement learning. arXiv preprint arXiv:2004.07219 . 

- [54] Gu, S., et al., 2022. A review of safe reinforcement learning: Methods, theory and applications. arXiv preprint arXiv:2205.10330 . 

- [55] Gui, Y., et al., 2024. Conformal alignment: Knowing when to trust foundation models with guarantees. arXiv preprint arXiv:2405.10301 . 

- [56] Guo, Y., et al., 2025. Improving vision-language-action model with online reinforcement learning. arXiv preprint arXiv:2501.16664 . 

- [57] Ha, D., Schmidhuber, J., 2018. Recurrent world models facilitate policy evolution. NeurIPS 31. 

- [58] Hansen, N., et al., 2024. Td-mpc2: Scalable, robust world models for continuous control. 

45 

- [59] Hansen-Estruch, P., et al., 2023. Implicit q-learning as an actor-critic method with diffusion policies. arXiv preprint arXiv:2304.10573 . 

- [60] Hassan, M., et al., 2024. Gem: A generalizable ego-vision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control. arXiv preprint arXiv:2412.11198 . 

- [61] He, H., et al., 2024. Diffusion model is an effective planner and data synthesizer for multi-task reinforcement learning. NeurIPS 36. 

- [62] Hegde, S., et al., 2023. Generating behaviorally diverse policies with latent diffusion models. NeurIPS 36, 7541–7554. 

- [63] Ho, J., Salimans, T., 2021. Classifier-free diffusion guidance, in: NeurIPS Workshop on Deep Generative Models and Downstream Applications. 

- [64] Hu, H., Sadigh, D., 2023. Language instructed reinforcement learning for human-ai coordination, in: ICML, PMLR. pp. 13584–13598. 

- [65] Hu, J., et al., 2023a. Instructed diffuser with temporal condition guidance for offline rl. arXiv preprint arXiv:2306.04875 . 

- [66] Hu, J., et al., 2024a. Flare: Achieving masterful and adaptive robot policies with large-scale reinforcement learning fine-tuning. CoRR abs/2409.16578. 

- [67] Hu, S., et al., 2023b. Prompt-tuning decision transformer with preference ranking. arXiv preprint arXiv:2305.09648 . 

- [68] Hu, S., et al., 2024b. HarmoDT: Harmony multi-task decision transformer for offline reinforcement learning, in: ICML, pp. 19182–19197. 

- [69] Hu, Y., et al., 2023c. Toward general-purpose robots via foundation models: A survey & meta-analysis. arXiv preprint arXiv:2312.08782 . 

- [70] Huang, S., et al., 2024a. Understanding and mitigating noise in vlm rewards. arXiv preprint arXiv:2409.15922 . 

- [71] Huang, T., et al., 2024b. Diffusion reward: Learning rewards via conditional video diffusion. ECCV . 

46 

- [72] Huang, W., et al., 2023a. Grounded decoding: Guiding text generation with grounded models for embodied agents, in: NeurIPS. 

- [73] Huang, W., et al., 2023b. Voxposer: Composable 3d value maps for robotic manipulation with language models. arXiv preprint arXiv:2307.05973 . 

- [74] Huang, X., et al., 2024c. Diffuseloco: Real-time legged locomotion control with diffusion from offline datasets. arXiv preprint arXiv:2404.19264 . 

- [75] Jain, V., Ravanbakhsh, S., 2023. Learning to reach goals via diffusion. arXiv preprint arXiv:2310.02505 . 

- [76] Janner, M., et al., 2022. Planning with diffusion for flexible behavior synthesis, in: ICML. 

- [77] Janson, L., et al., 2018. Deterministic sampling-based motion planning: Optimality, complexity, and performance. IJRR 37, 46–61. 

- [78] Jülg, T., et al., 2025. Refined policy distillation: From vla generalists to rl experts. arXiv preprint arXiv:2503.05833 . 

- [79] Kang, B., et al., 2024. Efficient diffusion policies for offline reinforcement learning. NeurIPS 36. 

- [80] Kim, M.J., et al., 2024a. Openvla: An open-source vision-languageaction model. arXiv preprint arXiv:2406.09246 . 

- [81] Kim, S., et al., 2024b. Stitching sub-trajectories with conditional diffusion model for goal-conditioned offline rl. arXiv preprint arXiv:2402.07226 . 

- [82] Kim, W.K., et al., 2024c. Robust policy learning via offline skill diffusion. arXiv preprint arXiv:2403.00225 . 

- [83] Kollar, T., et al., 2017. Generalized grounding graphs: A probabilistic framework for understanding grounded commands. arXiv preprint arXiv:1712.01097 . 

- [84] Kumar, A., et al., 2022. Pre-training for robots: Offline rl enables learning new tasks in a handful of trials. RSS . 

47 

- [85] Lee, K., et al., 2024a. Refining diffusion planner for reliable behavior synthesis by automatic detection of infeasible plans. NeurIPS 36. 

- [86] Lee, O.Y., et al., 2024b. Affordance-guided reinforcement learning via visual prompting. arXiv preprint arXiv:2407.10341 . 

- [87] Li, P.h., et al., 2024a. Online foundation model selection in robotics. arXiv preprint arXiv:2402.08570 . 

- [88] Li, W., et al., 2023a. Hierarchical diffusion for offline decision making, in: ICML, PMLR. pp. 20035–20064. 

- [89] Li, X., et al., 2024b. Evaluating real-world robot manipulation policies in simulation. arXiv preprint arXiv:2405.05941 . 

- [90] Li, Z., et al., 2023b. Beyond conservatism: Diffusion policies in offline multi-agent reinforcement learning. arXiv preprint arXiv:2307.01472 . 

- [91] Liang, Z., et al., 2023. Adaptdiffuser: Diffusion models as adaptive self-evolving planners. arXiv preprint arXiv:2302.01877 . 

- [92] Liu, J., et al., 2023. Dipper: Diffusion-based 2d path planner applied on legged robots. arXiv preprint arXiv:2310.07842 . 

- [93] Liu, J., et al., 2025. What can rl bring to vla generalization? an empirical study. arXiv preprint arXiv:2505.19789 . 

- [94] Liu, S., et al., 2024. Rl-gpt: Integrating reinforcement learning and code-as-policy. arXiv preprint arXiv:2402.19299 . 

- [95] Lu, C., et al., 2023. Contrastive energy prediction for exact energyguided diffusion sampling in offline reinforcement learning, in: ICML, PMLR. pp. 22825–22855. 

- [96] Lubana, E.S., et al., 2023. Fomo rewards: Can we cast foundation models as reward functions? arXiv preprint arXiv:2312.03881 . 

- [97] Luo, J., et al., 2024. Precise and dexterous robotic manipulation via human-in-the-loop reinforcement learning. arXiv preprint arXiv:2410.21845 . 

48 

- [98] Ma, R., et al., 2024a. Guiding exploration in reinforcement learning with large language models. arXiv preprint arXiv:2403.09583 . 

- [99] Ma, Y., et al., 2024b. A survey on vision-language-action models for embodied ai. arXiv preprint arXiv:2405.14093 . 

- [100] Ma, Y.J., et al., 2022. Vip: Towards universal visual reward and representation via value-implicit pre-training. arXiv preprint arXiv:2210.00030 . 

- [101] Ma, Y.J., et al., 2023a. Eureka: Human-level reward design via coding large language models. arXiv preprint arXiv: Arxiv-2310.12931 . 

- [102] Ma, Y.J., et al., 2023b. Liv: Language-image representations and rewards for robotic control, in: ICML, PMLR. pp. 23301–23320. 

- [103] Ma, Y.J., et al., 2024c. Dreureka: Language model guided sim-to-real transfer. arXiv preprint arXiv:2406.01967 . 

- [104] Mahmoudieh, P., et al., 2022. Zero-shot reward specification via grounded natural language, in: ICML, PMLR. pp. 14743–14752. 

- [105] Majumdar, A., et al., 2024. Where are we in the search for an artificial visual cortex for embodied intelligence? NeurIPS 36. 

- [106] Mao, Z., et al., 2024. Zero-shot safety prediction for autonomous robots with foundation world models. arXiv preprint arXiv:2404.00462 . 

- [107] Mark, M.S., et al., 2024. Policy agnostic rl: Offline rl and online rl finetuning of any class and backbone. arXiv preprint arXiv:2412.06685 . 

- [108] Mazoure, B., et al., 2023. Value function estimation using conditional diffusion models for control. arXiv preprint arXiv:2306.07290 . 

- [109] Mazzaglia, P., et al., 2024. Multimodal foundation world models for generalist embodied agents. arXiv preprint arXiv:2406.18043 . 

- [110] Mezghani, L., et al., 2023. Think before you act: Unified policy for interleaving language reasoning with actions. arXiv preprint arXiv:2304.11063 . 

49 

- [111] Mnih, V., et al., 2013. Playing atari with deep reinforcement learning. arXiv preprint arXiv:1312.5602 . 

- [112] Mnih, V., et al., 2015. Human-level control through deep reinforcement learning. nature 518, 529–533. 

- [113] Nair, S., et al., 2022. Learning language-conditioned robot behavior from offline data and crowd-sourced annotation, in: CoRL, PMLR. pp. 1303–1315. 

- [114] Nakamura, K., et al., 2025. Generalizing safety beyond collisionavoidance via latent-space reachability analysis. arXiv preprint arXiv:2502.00935 . 

- [115] Ni, F., et al., 2023. Metadiffuser: Diffusion model as conditional planner for offline meta-rl, in: ICML, PMLR. pp. 26087–26105. 

- [116] Nottingham, K., et al., 2023. Do embodied agents dream of pixelated sheep: Embodied decision making using language guided world modelling, in: ICML, PMLR. pp. 26311–26325. 

- [117] Nuti, F., et al., 2024. Extracting reward functions from diffusion models. NeurIPS 36. 

- [118] Oier, M., et al., 2024. Octo: An open-source generalist robot policy, in: Proceedings of RSS, Delft, Netherlands. 

- [119] Padalkar, A., et al., 2023. Open X-Embodiment: Robotic learning datasets and RT-X models. 

- [120] Pérez-Dattari, R., et al., 2024. Puma: deep metric imitation learning for stable motion primitives. Advanced Intelligent Systems 6, 2400144. 

- [121] Permenter, F., Yuan, C., 2024. Interpreting and improving diffusion models from an optimization perspective, in: ICML, JMLR.org. 

- [122] Psenka, M., et al., 2023. Learning a diffusion model policy from rewards via q-score matching. arXiv preprint arXiv:2312.11752 . 

- [123] Qi, H., et al., 2025. Strengthening generative robot policies through predictive world modeling. arXiv preprint arXiv:2502.00622 . 

50 

- [124] Radford, A., et al., 2021. Learning transferable visual models from natural language supervision, in: ICML, Pmlr. pp. 8748–8763. 

- [125] Ramesh, A., et al., 2021. Zero-shot text-to-image generation, in: ICML, Pmlr. pp. 8821–8831. 

- [126] Reed, S., et al., 2022. A generalist agent. arXiv preprint arXiv:2205.06175 . 

- [127] Ren, A.Z., et al., 2024. Diffusion policy policy optimization, in: arXiv preprint arXiv:2409.00588. 

- [128] Rocamonde, J., et al., 2023. Vision-language models are zeroshot reward models for reinforcement learning. arXiv preprint arXiv:2310.12921 . 

- [129] Rombach, R., et al., 2022. High-resolution image synthesis with latent diffusion models, in: Proceedings of the IEEE/CVF, pp. 10684–10695. 

- [130] Ross, S., Bagnell, D., 2010. Efficient reductions for imitation learning, in: Teh, Y.W., Titterington, M. (Eds.), ICAIS, PMLR, Chia Laguna Resort, Sardinia, Italy. pp. 661–668. 

- [131] Rusu, A.A., et al., 2015. Policy distillation. arXiv preprint arXiv:1511.06295 . 

- [132] Seo, Y., et al., 2023a. Masked world models for visual control, in: CoRL, PMLR. pp. 1332–1344. 

- [133] Seo, Y., et al., 2023b. Multi-view masked world models for visual robotic manipulation, in: ICML, PMLR. pp. 30613–30632. 

- [134] Shridhar, M., et al., 2022. Cliport: What and where pathways for robotic manipulation, in: CoRL, PMLR. pp. 894–906. 

- [135] Song, J., et al., 2023. Self-refined large language model as automated reward function designer for deep reinforcement learning in robotics. arXiv preprint arXiv:2309.06687 . 

- [136] Sontakke, S., et al., 2024. Roboclip: One demonstration is enough to learn robot policies. NeurIPS 36. 

51 

- [137] Suh, H.T., et al., 2023. Fighting uncertainty with gradients: Offline reinforcement learning via diffusion score matching, in: CoRL, PMLR. pp. 2878–2904. 

- [138] Sun, J., et al., 2024. Prompt, plan, perform: Llm-based humanoid control via quantized imitation learning, in: 2024 IEEE ICRA, IEEE. pp. 16236–16242. 

- [139] Sutton, R., Barto, A., 1998. Reinforcement learning: An introduction. IEEE Transactions on Neural Networks 9, 1054–1054. 

- [140] Sutton, R.S., 1988. Learning to predict by the methods of temporal differences. Machine learning 3, 9–44. 

- [141] Tian, R., et al., 2024. Maximizing alignment with minimal feedback: Efficiently learning rewards for visuomotor robot policy alignment. arXiv preprint arXiv:2412.04835 . 

- [142] Trabucco, B., et al., 2022. Anymorph: Learning transferable polices by inferring agent morphology, in: ICML, PMLR. pp. 21677–21691. 

- [143] Triantafyllidis, E., et al., 2024. Intrinsic language-guided exploration for complex long-horizon robotic manipulation tasks, in: 2024 IEEE ICRA, IEEE. pp. 7493–7500. 

- [144] Van de Ven, G.M., et al., 2024. Continual learning and catastrophic forgetting. arXiv preprint arXiv:2403.05175 . 

- [145] Venkatraman, S., et al., 2023. Reasoning with latent diffusion in offline reinforcement learning. arXiv preprint arXiv:2309.06599 . 

- [146] Venuto, D., et al., 2024. Code as reward: Empowering reinforcement learning with vlms. arXiv preprint arXiv:2402.04764 . 

- [147] Wabersich, K.P., Zeilinger, M.N., 2021. A predictive safety filter for learning-based control of constrained nonlinear dynamical systems. Automatica 129, 109597. 

- [148] Wang, J., et al., 2024a. Large language models for robotics: Opportunities, challenges, perspectives. arXiv preprint arXiv:2401.04334 . 

52 

- [149] Wang, L., et al., 2023a. Gensim: Generating robotic simulation tasks via large language models. ArXiv abs/2310.01361. 

- [150] Wang, Y., et al., 2023b. Robogen: Towards unleashing infinite data for automated robot learning via generative simulation. arXiv preprint arXiv:2311.01455 . 

- [151] Wang, Y., et al., 2024b. Rl-vlm-f: Reinforcement learning from vision language foundation model feedback, in: ICML. 

- [152] Wang, Z., et al., 2022. Diffusion policies as an expressive policy class for offline reinforcement learning. arXiv preprint arXiv:2208.06193 . 

- [153] Wang, Z., et al., 2023c. Cold diffusion on the replay buffer: Learning to plan from known good states, in: CoRL, PMLR. pp. 3277–3291. 

- [154] Wen, M., et al., 2022. Multi-agent reinforcement learning is a sequence modeling problem. NeurIPS 35, 16509–16521. 

- [155] Wen, M., et al., 2023. Large sequence models for sequential decisionmaking: a survey. Frontiers of Computer Science 17, 176349. 

- [156] Wolczyk, M., et al., 2023. On the role of forgetting in fine-tuning reinforcement learning models, in: ICLR Workshop on Reincarnating Reinforcement Learning. 

- [157] Wołczyk, M., et al., 2024. Fine-tuning reinforcement learning models is secretly a forgetting mitigation problem. arXiv preprint arXiv:2402.02868 . 

- [158] Wu, J., et al., 2024. ivideogpt: Interactive videogpts are scalable world models. arXiv preprint arXiv:2405.15223 . 

- [159] Wu, P., et al., 2023. Daydreamer: World models for physical robot learning, in: CoRL, PMLR. pp. 2226–2240. 

- [160] Xiao, W., et al., 2023a. Safediffuser: Safe planning with diffusion probabilistic models. arXiv preprint arXiv:2306.00148 . 

- [161] Xiao, W., et al., 2025. Safediffuser: Safe planning with diffusion probabilistic models, in: ICLR. 

53 

- [162] Xiao, X., et al., 2023b. Robot learning in the era of foundation models: A survey. arXiv preprint arXiv:2311.14379 . 

- [163] Xie, T., et al., 2023. Text2reward: Reward shaping with language models for reinforcement learning, in: ICLR. 

- [164] Xu, C., et al., 2024. Rldg: Robotic generalist policy distillation via reinforcement learning. arXiv preprint arXiv:2412.09858 . 

- [165] Xu, M., et al., 2023. Hyper-decision transformer for efficient online policy adaptation. arXiv preprint arXiv:2304.08487 . 

- [166] Xue, H., et al., 2024. Full-order sampling-based mpc for torque-level locomotion control via diffusion-style annealing. `arXiv:2409.15610` . 

- [167] Yang, J., et al., 2024. Robot fine-tuning made easy: Pre-training rewards and policies for autonomous real-world reinforcement learning, in: 2024 IEEE ICRA, IEEE. pp. 4804–4811. 

- [168] Yang, L., et al., 2023a. Policy representation via diffusion probability model for reinforcement learning. arXiv preprint arXiv:2305.13122 . 

- [169] Yang, M., et al., 2023b. Learning interactive real-world simulators. arXiv preprint arXiv:2310.06114 . 

- [170] Ye, W., et al., 2023. Towards embodied generalist agents with foundation prior assistance. arXiv preprint arXiv:2310.02635 . 

- [171] Yu, W., et al., 2023. Language to rewards for robotic skill synthesis. Arxiv preprint arXiv:2306.08647 . 

- [172] Zala, A., et al., 2024. Envgen: Generating and adapting environments via llms for training embodied agents, in: COLM. 

- [173] Zeng, A., et al., 2022. Socratic models: Composing zero-shot multimodal reasoning with language. arXiv preprint arXiv:2204.00598 . 

- [174] Zhang, E., et al., 2024a. Language control diffusion: Efficiently scaling through space, time, and tasks, in: ICLR. 

- [175] Zhang, J., et al., 2023. Bootstrap your own skills: Learning to solve new tasks with large language model guidance. arXiv preprint arXiv:2310.10021 . 

54 

- [176] Zhang, J., et al., 2024b. Vision-language models for vision tasks: A survey. IEEE Transactions on PAMI . 

- [177] Zhang, Y., et al., 2024c. Motiongpt: Finetuned llms are generalpurpose motion generators, in: Proceedings of AAAI, pp. 7368–7376. 

- [178] Zhao, W., et al., 2024. Vlmpc: Vision-language model predictive control for robotic manipulation, in: RSS. 

- [179] Zhou, C., et al., 2022. A review of motion planning algorithms for intelligent robots. Journal of Intelligent Manufacturing 33, 387–424. 

- [180] Zhou, G., et al., 2024a. Diffusion model predictive control. arXiv preprint arXiv:2410.05364 . 

- [181] Zhou, H., et al., 2024b. Language-conditioned learning for robotic manipulation: A survey. arXiv preprint arXiv:2312.10807 . 

- [182] Zhou, S., et al., 2024c. Adaptive online replanning with diffusion models. NeurIPS 36. 

- [183] Zhu, D., et al., 2023a. Minigpt-4: Enhancing vision-language understanding with advanced large language models. arXiv preprint arXiv:2304.10592 . 

- [184] Zhu, Z., et al., 2023b. Diffusion models for reinforcement learning: A survey. arXiv preprint arXiv:2311.01223 . 

- [185] Zhu, Z., et al., 2023c. Madiff: Offline multi-agent learning with diffusion models. arXiv preprint arXiv:2305.17330 . 

- [186] Ziegler, D.M., et al., 2019. Fine-tuning language models from human preferences. arXiv preprint arXiv:1909.08593 . 

55 

