---
title: "Large language models for artificial general intelligence (AGI): A survey of foundational principles and approaches"
date: "2025-01-06"
authors: "Alhassan Mumuni; Fuseini Mumuni"
url: https://arxiv.org/abs/2501.03151
pdf: https://arxiv.org/pdf/2501.03151
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2501.03151)** / [論文ページ](https://arxiv.org/abs/2501.03151)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Large language models for artificial general intelligence (AGI): A survey of foundational principles and approaches 

Alhassan Mumuni<sup>1</sup><sup>_∗_</sup> and Fuseini Mumuni<sup>2</sup> 

**Abstract** —Generative artificial intelligence (AI) systems based on large-scale pretrained foundation models (PFMs) such as vision-language models, large language models (LLMs), diffusion models and vision-language-action (VLA) models have demonstrated the ability to solve complex and truly non-trivial AI problems in a wide variety of domains and contexts. Multimodal large language models (MLLMs), in particular, learn from vast and diverse data sources, allowing rich and nuanced representations of the world and, thereby, providing extensive capabilities, including the ability to reason, engage in meaningful dialog; collaborate with humans and other agents to jointly solve complex problems; and understand social and emotional aspects of humans. Despite this impressive feat, the cognitive abilities of state-of-the-art LLMs trained on large-scale datasets are still superficial and brittle. Consequently, generic LLMs are severely limited in their generalist capabilities. A number of foundational problems —embodiment, symbol grounding, causality and memory — are required to be addressed for LLMs to attain human-level general intelligence. These concepts are more aligned with human cognition and provide LLMs with inherent human-like cognitive properties that support the realization of physically-plausible, semantically meaningful, flexible and more generalizable knowledge and intelligence. In this work, we discuss the aforementioned foundational issues and survey state-of-the art approaches for implementing these concepts in LLMs. Specifically, we discuss how the principles of embodiment, symbol grounding, causality and memory can be leveraged toward the attainment of artificial general intelligence (AGI) in an organic manner. 

**Index Terms** —Large language model, embodiment, symbol grounding, causal reasoning, memory mechanism, artificial general intelligence. 

✦ 

## **1 INTRODUCTION** 

### **1.1 Background** 

Intelligence relates to the ability of a system, biological or otherwise, to achieve some level of success in accomplishing one or more desired goals in a given environment (or variety of environments). An intelligent system is capable of inferring its own state as well as the state of the environment, and is able to transform these inferences into appropriate responses leading to the achievement of desired goals. Intelligence is characteristically a unique feature of higher living organisms, and in the pursuit of developing their artificial counterparts, artificial intelligence, researchers have frequently borrowed concepts from biology. An important attribute of biological intelligence is its generality, i.e., its ability to handle many different problems across a wide variety of settings. Human intelligence, in particular, is remarkably sophisticated, rich and versatile, and can effortlessly handle many novel tasks. The general superiority of human intelligence over that of other higher animals stems (primarily) from the ability of humans to structure and transfer knowledge through social and cultural constructs such as art, norms, rituals, belief systems and customs [1]. Language plays a vital role in all these processes. 

> _•_ 1 _Alhassan Mumuni: Department of Electrical and Electronics Engineering, Cape Coast Technical University, Cape Coast, Ghana._ 

> _∗Corresponding author, E-mail: alhassan.mumuni@cctu.edu.gh_ 

While the idea of creating this kind of generalist intelligence is attractive, it is extremely challenging to achieve such level of sophistication and generalization power in machines. Until quite recently, AI techniques that achieved impressive results were narrowly focused, solving specific problems in one domain or in a restricted set of domains (e.g., face recognition, medical image segmentation, text translation, stock market forecasting, pedestrian tracking, etc.). Lately, generative AI techniques based on variational autoencoders (VAEs) [2] and generative adversarial networks (GANs) [3] have contributed greatly in revolutionizing the capabilities of AI, and enabling single models to simultaneously handle a wide variety of complex tasks [4]. More recently, the emergence of large-scale pretrained foundation models such as large language models (LLMs) [5], diffusion models (DMs) [6], vision-language models (VLMs) [7] and vision-language-action (VLA) models [8] has real prospect for replicating generalist property in artificial intelligence. Owing to their ability to handle a wide range of challenging open-domain problems [9], [10], [11], [12], largescale pretrained foundation models, especially multimodal large language models, have renewed interest in the quest for developing artificial general intelligence [10]. The main aim of this work is to present the fundamental principles of cognition that supports the realization of artificial general intelligence, and review state-of-the-art techniques for implementing these concepts in large language models. 

> _•_ 2 _Fuseini Mumuni: University of Mines and Technology, UMaT, Tarkwa, Ghana. E-mail: fmumuni@umat.edu.gh_ 

2 

### **1.2 Language as the foundation of general intelligence in biological systems** 

### _1.2.1 Language as a medium of knowledge acquisition, representation and organization_ 

It has been shown that communication using natural language is one of the most effective ways of learning general knowledge about the real world [13], and while, human’s sensory and motor capabilities are not generally superior to other higher animals, including primates (see [14], [15], [16], [17], [18], [19], [20], human cognitive capabilities are far more advanced than other animals. The superiority of man’s cognitive capacity compared to other members of the animal kingdom, including his closest relative, primates, has been largely attributed to humans’ use of language [21], [22], [23]. 

Language plays a central role in man’s ability to represent, interpret and reason with abstract concepts [24]. In human societies, one of the most important functions of language is to facilitates the acquisition and sharing of new knowledge. With the help of language – whether by literature, speech or art – humans can effortlessly learn from others and accumulate knowledge not only by observation or through their own interactions with the world, but also by acquiring knowledge accumulated by other humans. Besides, language provides a conceptual framework for representing and internalizing knowledge [22]. It has been demonstrated that the specific linguistic structures and vocabulary used by a group influence reasoning and interpretation of the world. Indeed, linguistic differences (e.g., in terms of vocabulary) has been shown to influence how individuals members of different linguistic groups remember and describe their experiences [25], [26], [27], [28]. In this regard, language can structure or restructure cognition [29], and therefore shapes how subjects understand and interact with the world [30], [31]. 

### _1.2.2 Language as a tool for cognitive information processing_ 

Besides creating abstractions to represent and organize the representation of perceptual information and knowledge, language plays a fundamental role in facilitating cognitive computational operations [24]. Lupyan [31] argues that basic linguistic elements like words provide cues for other cognitive components to construct meaning. Thus, language is not just a set of static symbols that reference real-world objects, phenomena and experiences, but it also serves as a tool for manipulating these symbols. Clark [24] specifically describes six different ways by which language facilitates cognitive information processing and reasoning in humans. Language been shown to facilitate not just crystalized intelligence (i.e., representation-related cognitive mechanisms) such as experience/stimuli categorization [26] and memory [25], [28] but also elements of fluid intelligence (i.e., analytical problem-solving skills) like perception [32], [33], [34] and reasoning [24], [31]. Moreover, exposure to multiple linguistic frameworks has been demonstrated to broaden the individual’s perspective and facilitates an understanding of concepts in a more nuanced manner. Because of its centrality in biological cognitive abilities, language has been characterized variously as “the interface to cognition” [21], 

“intelligence amplifier” [35], and human cognition itself has been described as language-augmented cognition [31]. 

### **1.3 The concept of artificial general intelligence** 

While there are different interpretations of artificial general intelligence (AGI) in the literature [9], [36], [37], [38], [39], [40], the concept is generally understood as AI systems that exhibit broad intellectual abilities and are able to perform high-level cognitive tasks such as perception – including context understanding and a degree of self-awareness [41], [42], reasoning, planning, and the application of learned knowledge in new contexts. AGI systems are universally powerful models that can successfully accomplish significantly complex and diverse cognitive tasks across multiple domains without the need for additional training. The term human-level intelligence [37], [43], [44] is often loosely used to refer to AI systems that demonstrate general intelligence. 

AGI should not be taken to mean super-omniscience and omnipotent machines. Such hypothetical level of capability is referred to as artificial super-intelligence [45], [46]. Practical AGI systems are systems possessing general – yet limited and, to a degree, uncertain – knowledge about the world but is sufficiently powerful and flexible to solve a wide range of problems requiring sensorimotor control, perception, context understanding, commonsense and analytical reasoning capabilities. This understanding of artificial general intelligence, in essence, reflects not only the fact of the practical difficulties in embedding or learning all relevant knowledge and skills at once, but also the performance limitations of such an approach. Moreover, conceptualizing artificial general intelligence as limited in scope but adaptive, flexible and extensible is consistent with the nature and properties of biological intelligence in higher living organisms like humans. Despite the wide variety of definitions in the literature, there almost a unanimous agreement on some of the defining features of AGI. Specifically, the most important features of a typical AGI system are that (see, for example, [9], [36], [43], [47], [48]): it can learn and flexibly apply the limited and uncertain knowledge to solve a wide range of problems in entirely different contexts; its learning and actions are autonomous and goal-driven; it retains and accumulates relevant information in memory and reuse the knowledge in future tasks; and it can understand context and perform high-level cognitive tasks such as abstract and commonsense reasoning. We summarized the important properties in Figure 1. 

It is important to point out that AGI is fundamentally different from Strong AI (see [49], [50], [51]). While AGI focuses on developing intelligent systems that have broad cognitive capabilities and can solve truly nontrivial problems, Strong AI aims to create very powerful intelligence that not only mimics human cognitive abilities at the functional level but one that is also characterized by real human cognitive properties such as intrinsic mental states and subjective experiences, including intentionality (desires, hopes, beliefs, inner motivation, etc.), morality, emotions, and self-awareness [52], [53] in the sense of being conscious and sentient. Readers interested in this topic may want to see [54], [55], [56], [57], [58] for more detailed discussions on Strong AI concepts, including sentience [54], [56], [57], 

3 


Figure 1. Some of the most important features of artificial general intelligence (AGI) systems. These features give AGI systems vast cognitive capabilities despite the models’ limited knowledge and the need to, for the sake of conserving energy and time, take shortcuts in cognitive information processing. 

consciousness [55], [57], [59] and morality [60], [61] of AI systems. 

a holistic cognitive model based on these interrelationships and interactions. Finally, we present a summary discussion of the concepts in Section 8 and conclude in Section 9. 

### **1.4 Scope and outline of work** 

In this work, we present an extensive discussion of the core principles we consider important to achieving general intelligence. We also discuss the various approaches for realizing each of these concepts in artificial intelligence and LLM systems. The concepts discussed here are not algorithmic solutions for achieving AGI but rather general principles and properties of biological intelligence that AI systems based on large language models must be imbued with if they are to attain the kind of generality, robustness and sophistication of human cognitive functions. In fact, the core concepts are by nature algorithm-agnostic, that is, their implementation is not specific to any particular techniques or set of methods. It is important, however, to note that specific cognitive functions – e.g., perception, reasoning, planning, action, etc. – can be enriched by these general concepts and principles. The remainder of the paper is organized as follows. In section 2, we present a brief overview of the key elements of large language models that make then so powerful and underlie their potential for solving complex problems requiring human-level general intelligence. The important foundational principles for achieving general intelligence in large language models are covered in sections 3 through 6. These include embodiment (Section 3), symbol grounding (Section 4), causality (Section 5) and memory (Section 6). In Section 7, we discuss the interrelationships and interactions of the cognitive principles and synthesize 

## **2 TOWARDS ARTIFICIAL GENERAL INTELLIGENCE WITH LARGE LANGUAGE MODELS** 

### **2.1 Large language models and artificial general intelligence** 

Much of human knowledge and skills have been acquired and transmitted through multiple media, most significantly through language and visual media (reading, listening, direct observation, etc.). In a similar way, multimodal language models, relying on multiple data modalities, hold a great promise for providing systems with general, multidimensional knowledge about the world. While unimodal language models such as GPT-3 [62] and BERT [63] could handle only text data, multimodal LLMs (e.g., Palm-E [64], Minigpt-4 [65], Flamingo [66], LLaVA [67]) naturally integrates many different data modalities, including visual, auditory, textual and spatial information seamlessly to generate richer and more comprehensive representations for cognitive tasks. This is similar to the way biological intelligence relies on complex, multisensory data streams. The generalist capabilities of state-of-the-art multimodal large language models have already been widely demonstrated [9], [40], and their ability to solve a wide range of complex cognitive problems that traditionally required human intelligence is in no doubt. The remarkable success of large language models has redefined the possibilities and scope 

4 

of artificial intelligence. The main factor that drives this success is the ability to build and train very large neural network models on diverse, multimodal data. These models are typically trained on generic data from the wild (e.g., online publications, books, news articles, social media and other sources of information from the web), and are able to capture intricate concepts and generalize more effectively to new tasks with little (few-shot learning [68], [69]) or no (zero-shot learning [70]) task-specific training. Consequently, complex cognition-intensive, open-domain tasks such as commonsense and analytical reasoning [71], [72]; mathematical problem-solving [73], [74]; itinerary planning [75], [76] or general task planning [77]; and open-vocabulary question answering [78], [79]. Significantly, state-of-the-art LLMs are able to perform creative and artistic works such as composing essays, short stories, or even entire novels [80], [81] according to any given criteria (e.g., author style, diction, mood, etc.). 

### **2.2 Features of large language models that support the attainment of human-level intelligence** 

In the context of achieving general intelligence, besides training on large and diverse datasets, large language models possess a number of interesting features that allow their knowledge and skills to be naturally extended as needed. This extensibility, together with their already vast generic knowledge, allows them to overwhelmingly outperform traditional deep learning models that are typically designed with narrow optimization objectives and trained on restricted datasets from curated environments. 

While the underlying processes and mechanisms that support extensibility of large language models are fundamentally different from those that support biological intelligence, the resulting properties somehow mirror the multilayered and multidimensional nature of human intelligence in many respects. For example, pretraining large language models endows them with general knowledge that is sufficiently powerful and flexible to tackle a wide range of common problems requiring perception, context understanding as well as commonsense and analytical reasoning capabilities. Where domain-specific knowledge is needed, finetuning can be applied to augment the general knowledge with specialized knowledge by training the pretrained LMM further on domain-specific datasets. This approach is similar to the way human experts – who already have general or commonsense knowledge– acquire specialized competencies in narrow areas of endeavor (e.g., as professionals in engineering, medicine, law, or web development). It is also usual to ground the internal representations in realworld concepts using prior knowledge. Again, this feature is similar to the way biological intelligence is built on prior knowledge encoded as genetic information. In addition to the internalized knowledge and cognitive capabilities, humans frequently rely external knowledge (e.g., through consultations with experts or books) and tools (e.g., software, machines, etc.) to extend their capabilities. Similarly, stateof-the-art language models can utilize tools (see [82], [83], [84]) and external knowledge –through retrieval augmented generation (RAG) [85], [86] – to extend their capabilities. We summarized these important features in Figure 2. 

### **2.3 Overview of foundational principles for AGI with LLMs** 

Despite the fact that state-of-the-art large language models are incredibly powerful, they still have a number of limitations that constrain their ability to achieve general intelligence [87], [88], [89], [90]. Generally, the models’ understanding of context is often superficial and their solutions, in many cases, only exhibit external resemblance to human knowledge [91], [92]. The problem stems from the fact that AI systems, including LLMs, are still just digital constructs that that attempt to mimic human knowledge and cognitive capabilities by learning general properties of the world from vast amounts of data. This knowledge is generally limited to observed patterns but does not capture the underlying principles responsible for the behavior. 

It has long been argued that for machines to achieve AGI they necessarily need to emulate some key aspects of human cognition which enables human intelligence to be so robust, efficient, flexible and general yet sophisticated in the way it handles complex problems. Among the key aspects of human cognitive process are embodied sentience or simply embodiment [93], [94], symbolic grounding [95], causal reasoning [96], [97], and memory [98], [99], [100]. Embodied sentience—the ability to have subjective experiences and feel sensations—is considered a fundamental aspect of higher intelligence. It is an essential capability to enable general intelligence because it provides a sort of pseudoconsciousness and autonomy [101], [102], [103] Specifically, it enables agents to be self-aware, and therefore align their decisions and actions to a more universal, intrinsic higherlevel goal [104], [105], [106]. Embodied sentience also allows agents to recognize the experiences of others. This allows them to be ethical and moral in decision-making and behavior. Another key principle of biological intelligence, symbolic grounding, performs a complementary function to embodiment by connecting abstract cognitive representations to meaningful entities and concepts in the real world. Grounding in LLMs ensures that the abstract representations learned correspond to specific real-world concepts, and are utilized or manipulated within the context of their semantic essence. Although the internal mechanisms underlying the grounding process in human cognition are still not well-understood, rudimentary techniques for realizing grounding in artificial intelligence systems have shown a lot of promise in their ability to align LLMs’ knowledge with the world’s [107]. Another important set of ingredients for artificial general intelligence, intuitive physics [108], [109] and intuitive psychology [110], [111], relate to the ability to infer cause-and-effect relations about events and interactions in the real world. Human’s natural understanding of intuitive physics is known to be the basis of robust perception and causal reasoning abilities. Meanwhile, intuitive psychology allows humans to form beliefs about intentions and probable actions of other living entities without the need to learn about specifically learn about them. Theory of mind (ToM) techniques [112], [113], [114] are typically employed in LLMs to facilitate their understanding of intuitive psychology. Finally, memory allows learned knowledge and past experiences to be preserved and accumulated over time. This extends and enriches knowledge in a way that 

5 

|**Aspect of intelligence**|**Human**|**LLM**|
|---|---|---|
|**Innate knowledge**|Gene�c informa�on that underlies important<br>biological processes, including behavior and<br>innate cogni�ve abili�es.|Prior informa�on about the world (e.g.,<br>physical laws, principles and causal<br>rela�onships) manually encoded in the LLM.|
|**General knowledge**|Generic, commonsense knowledge acquired<br>through experience.|Vast, task-agnos�c universal representa�ons<br>learned during pretraining of the base model.|
|**Specializa�on**|Acquisi�on of addi�onal, task-specific skills by<br>special training and learning, e.g., driving,<br>singing, engineering, repair, etc.|Finetuning enriches the base model with<br>relevant knowledge from a par�cular<br>domain or context for a given task while<br>ensuring that it maintains its vast general<br>knowledge.|
|**Expert consulta�on**|Consulta�on of experts and other resources<br>when exis�ng knowledge is not adequate to<br>handle the target task|Retrieval augmented genera�on (RAG) serves<br>as a means to obtain addi�onal knowledge<br>from external sources to solve specific<br>problems.|
|**Machine or tool use**|Use of machines and tools to ease the<br>performance of complex tasks.|LLM tool use to extend capabili�es of LLM<br>models and allow them to perform addi�onal<br>tasks that are not inherently enabled.|


Figure 2. LLM versus human intelligence: Important mechanisms that allow flexible extension of knowledge and cognitive abilities. 

|**Concept**|**Essence**|**Features of AGI supported**|
|---|---|---|
|**Embodiment**|Framework for learning & organizing knowledge<br>Mechanisms for sensing & actua�on|Interaction with and learning about the real world;<br>goal-directed behavior and autonomy.|
|**Grounding**|Connec�on of abstract representa�ons to real-world<br>en��es and concepts.|Context understanding (by providing meaningful and<br>rich contexts of the real world to the digital world)|
|**Causality**|Incorporation of physical constraints & rules for<br>manipulating symbols.|Robust generalization; logical, commonsense and<br>analytical reasoning.|
|**Memory**|Encoding, storage and reuse of past experiences|Adaptation of knowledge; continual learning.|


Figure 3. A summary of the essence and role of each of the foundational AGI concepts covered in this work. 

promotes general-purpose utility. Moreover, the ability to introspect [115], [116] and reflect [117] on past decisions and actions by virtue of memory mechanisms provides a way for LLMs to (accomplish) continual learning and adaptation. A summary of the role of each of these concepts is presented in Figure 3. 

## **3 EMBODIMENT** 

### **3.1 Basic concept of embodiment** 

Modern conceptualizations of biological cognition suggest that cognitive processes in the human nervous system are deeply rooted in the mind’s interactions with the body and the external environment. Per this view of intelligence, the brain, body, and environment are assumed to form a unified system where they jointly influence and shape intelligent behavior [118], [119], [120], [121]). The concept of neural plasticity, one of the most important cognitive phenomena that enhance adaptative behavior of intelligence, also assumes mind-body-environment interaction [122], [123], [124]. In [119], the three components are considered as essential cognitive resources that are required by the organism to solve specific tasks. In line with this understanding of mind-body-environment trinity, it has been argued that for AI systems to be truly intelligent, they, like biological 

systems, must necessarily be able to interact with the world in a physical way and receive feedback and learn about the results of those physical interactions (see [125], [126], [127], [128], [129], [130]). According to this hypothesis, artificial intelligence can only attain general intelligence comparable to human-level cognitive capabilities if such intelligence were created in, and intrinsically linked with a physical body that possesses the ability to perform physical actions on the environment [109], [129], [131]. Embodied AI systems are systems that – unlike traditional approaches that are solely digital in nature – have a tangible physical manifestation through which they can perceive and process sensory information, and interact with their environment. 

### **3.2 Embodiment as the foundation of general intelligence** 

Embodiment provides the foundation for intrinsic goaldirected behavior. An embodied artificial intelligence system necessarily has agency [132], [133], i.e., it undertakes intentional actions – actions it desires to perform (e.g., based on specific goals and needs) and over which it has complete control. This goal-directed behavior is a fundamental requirement for autonomy. Besides, AI systems endowed with rich sensorimotor resources with unlimited possibilities to 

6 

explore and interact with the environment will attain extensive intellectual capabilities. Such an intelligent system will necessarily possess accurate and robust perception of the world and of its own state. In addition, it must be able to act on and influence the world in a purposeful way. It must also be capable of seamlessly adapting to the complex dynamics of the real world. Thus, while conventional approaches to intelligence results in models that are inherently rigid and mechanistic, embodied intelligence is more flexible and nuanced, and can connect objective experiences with subjective concepts values, cultural norms and expectations [134]. By providing a more integrated way of interacting with the world, learning and decision-making, embodied agents are more robust and can handle complex and diverse problems, thereby supporting their generalist credentials. 

### **3.3 Key aspects of embodied intelligence** 

The most important aspect of artificial general intelligence is the requirement for full autonomy – the ability to independently make decisions and take appropriate actions even in the absence of explicit commands or control signals from the outside world. The implementation of embodied general intelligence involves four main considerations. 

**Goal-awareness:** In order to achieve full autonomy, like biological systems, the artificial intelligence system must have an overarching goal to which all other goals, including explicit instructions given by other actors, must be subordinated. This goal must be intrinsic and guide the successful accomplishment of external goals triggered by other agents (e.g., commands given by users, actions of other agents, etc.). 

**Self-awareness:** As the body is the executor of actions that influence the physical world, the intelligence process must be tied to the structure and capabilities of the body. That is, the appropriateness of intelligent actions depends not only on the goal the intelligent system seeks to achieve, but also on the optimality of the actions with respect to the available means to carry out the target goal. In order to be successful, the embodied intelligent agent must, therefore, be aware of its own capabilities and limitations. In humancentric contexts, this awareness includes the ability to understand oneself from the perspective the broader social setting, and to connect experiences with values, cultural norms and expectations. This facilitates the realization of social intelligence [134], [135], [136]. 

**Situational-awareness:** An entity’s intelligence is shaped by the specific context or situation it finds itself in. This underscores the fact that intelligent behavior is often a response to specific needs or challenges presented by the environment. Therefore, to achieve any goal, it is important to know the properties of the world and to predict beforehand the outcome of the target action with respect to the intended goal of the action. Moreover, since the external world behaves differently in response to actions by different entities, the intelligence of each intelligent system must be unique in some way. This means intelligent behavior of the AI system must take into account the expected responses elicited by other objects or the environment by virtue of its special characteristics. In humans, behavior is often shaped by social and cultural factors. Similarly, the 

actions of embodied AI agents must reflect social, cultural and demographic realities of their environment. AI agents must be able to achieve goals while respecting practical constraints, including safety [137] and alignment with ethics and cultural values [138]. 

**Deliberate action:** Actions are central to embodied intelligence since they are the primary means to influence the world and to achieve desired goals. Through actions an agent can perform active exploration of the world, thus further improving its perception and facilitating learning and adaptation in dynamic environments. Intelligent embodied agents must incorporate mechanisms to influence the world trough purposeful actions. 

In the following subsections, we discuss these four aspects of embodied intelligence and approaches for realization with modern AI systems based on pretrained foundation models, particularly large language models. A detailed summary of these discussions is presented in Figure 8 

### **3.4 Goal-awareness** 

### _3.4.1 Foundation of goal-awareness and role in general intelligence_ 

Human behavior is generally guided by goals that extend far beyond the objectives of immediate tasks [139], [140], [141]. These high-level goals are an important aspect of biological intelligence [142]. Similarly, in machines, intelligence is intrinsically linked with the ability to achieve defined goals. Therefore, to achieve truly general intelligence in AI, that kind of high-level goal-oriented behavior is required. Goal-awareness is considered a crucial capability for the realization of artificial general intelligence because it determines the ability of AI systems to operate autonomously [143], [144], [145]. Specifically, high-level goals provide intrinsic guidance that ensures meaningful and purposeful behavior in the absence of an external influence or instructions. 

Goal-driven embodied agents can align immediate decisions and actions towards useful, long-term outcomes. In this regard, goal-oriented behavior facilitates an open-ended approach to problem-solving, allowing intelligent agents to exploit many possible actions without being restricted to specific behavioral options. This flexibility is important in problem settings where the course of action is not immediately obvious or cannot be computed analytically or is ill-defined and require non-linear, creative reasoning to arrive at. In particular, it allows autonomous AI agents to perform useful acts in society, for example, responding to emergencies like motor accidents, while still maintaining their core functions. In Figure 4, for instance, two intelligent agents are shown taking part in evacuating and assisting victims during a traffic accident. These agents may not have been trained for such specific acts and may not have even anticipated such an incident but, being directed a higher goal that is aligned with broader societal values, they can make decisions independently to assist in such situations. Besides this cognitive flexibility, AI systems with goalawareness capability can better generalize learning, select or prioritize relevant knowledge, and pursue actions that are directed towards achieving specific outcomes. 

7 

Goal-driven behavior is particularly important in longhorizon tasks, situations involving delayed reward [146], [147], [148], where immediate actions do not have a direct correlation with current sensory state of the agent. In this case, the intelligent agent selects actions based on intrinsic goals rather than explicit instructions. Many intelligent tasks performed by animals involve such delayed rewards [146], [149]. The goals in biological cognition can be in different forms and from different sources [150], including implicit goals driven by biological needs (e.g., survival, reproduction, etc.), persistent, temporary objectives for a particular task (mission), instructions given by other humans. 


Figure 4. In this scene, two intelligent agents **A** and **B** assist during an emergency. When driven by high-level goals that are aligned with human interests and values, such agents can perform good acts spontaneously. Goal-awareness allows them to be proactive, autonomous and capable of attending to multiple tasks without deviating from their main essence. 

_3.4.2 Approaches to achieving goal-awareness in LLMs_ Generic LLMs have been shown to exhibit goal-oriented behavior [151], [152], [153]. Notwithstanding these recent capabilities, goal-awareness in LLMs out of the box is still limited. For instance, experimental evaluation of LLM goalawareness capabilities by Li Yu et al. [154]and Li Chuang et al. [155] show poor goal-awareness. To mitigate this shortcoming, some recent works (e.g., [156], [157], [158]) have sought to align LLM behavior with explicitly-specified goals. One of the simplest ways to introduce goal-awareness in LLMs is to incorporate high-level goals in the form of input prompts for the LLM to guide the underlying models [159], [160], [161]. Approaches to enabling goal-oriented behavior in a more intrinsic manner involve specifically formulating goals in the LLM framework [162], [163]. For instance, Li et al. [155] employ a dedicated goal planning agent together with a tool-augmented knowledge retrieval agent to handle goal-awareness in long-horizon tasks. Liu et al. [164] encoded goal information in a knowledge graph which is then leveraged to design a goal planning module 

that guides LMM-human conversations in a goal-directed manner. Similarly, Ni et al. [158] exploit the commonsense relationships that exist in knowledge graph entities as goals for conversational LLM agents. With the approach, goaldirected responses are generated by traversing through the graph. Another common approach is to finetune the LLM on specific datasets (e.g., [154], [165], [166], [167]) that have been curated with the intended goal in mind. Unfortunately, models trained this way are often short-term goal-oriented. Another way to enhance long-term goal-awareness can also be accomplished by fine-tuning LLMs with imitation learning (e.g., in [168]), using reinforcement Learning with Human Feedback [169] or with feedback from a submodule (e.g., [170]) or from a different LLM acting as external evaluator (e.g., [171]). Advanced LLMs can leverage intrinsic high-level goal-awareness to enable intelligent agents to independently formulate low-level goals and pursue task-specific objectives without explicit human supervision have already been proposed [151]. In EmbodiedGPT [172] and CoTDiffusion [173], for instance, Chain of Thought approach is used to generate subgoals for embodied actions. They can also refine decisions and modify actions according to changing circumstances and goals [151], [174]. 

### _3.4.3 Scope of application of goal-awareness in intelligent agents_ 

Goal-awareness can facilitate human-robot collaboration [156], [175], [176]. When LLM-based intelligent virtual agents or robots are aware of goals—both their own and those of the humans they work with—they can align their actions more closely with human intentions, leading to more seamless and effective collaboration. Agents can then be more forward-looking and take proactive actions [156] instead of merely responding to user requests. The awareness of human goals also helps LLM agents to clarify ambiguous situations and better interpret observations about humans. For instance, with knowledge of the broader goals, especially recommender-based conversational LLM agents, can provide better and more tailored responses [177]. Moreover, high-level goals can provide context for understanding instructions and other human inputs. 

### _3.4.4 Global and local goals_ 

While biological cognition can handle global, high-level goals, LLMs, till date, are generally limited to tasks that can be described by or decomposed into multiple subtasks that, each consisting of a sequence of steps, where some kind of fixed ordering of actions exists. This kind of goal-awareness can be more accurately described as mission-awareness. In complex, real-world scenarios, intelligent agents need to understand not just immediate goals, or missions, but also how multiple intermediate – often seemingly contradictory – goals and subgoals fit into broader contexts, including societal interests (e.g., avoiding physical harm, minimizing climate change or promoting inclusiveness). Ultimately, the ability to incorporate/understand high-level goals allow AGI to reason about trade-offs and determine the best courses of action to maximize overall success. By contrast mission-awareness involves goal-directed behavior on a specific task or related sets of tasks. 

8 

### **3.5 Situational-awareness** 

### _3.5.1 Main aspects of situational-awareness_ 

Embodied perception, that is, situational-awareness by embodied agents, involves two main aspects: the awareness of the environment and awareness of other strategic agents. 

**(a) Awareness of the environment and the general context** 

The most important task in embodied AI research is aimed at enhancing the situational-awareness of agents – their ability to make sense of the real world in a way that allows them to interact with it and carry out actions towards the achievement of specific goals. Perception in the context of embodied cognition entails not only an understanding of the current state of the world and the processes occurring in it, but also an understanding of how the environment will change in the near and distant future as a result of various factors, including, most importantly, the effects of the actions of the agent and/or other agents. For humans, situational-awareness is a result of knowledge acquired through learning and experience, instincts and innate knowledge transmitted through genes, as well as “on the fly” information provided by other humans and intelligent systems. Intelligent agents based on LLMs also possess similar attributes. For example, the core model itself is a knowledge base for commonsense generic knowledge about the world [178], [179], [180], [181]. In addition, specific information about the world can be acquired through various means (see discussions in subsection 2.2) 

### **(b) Awareness of users and other agents** 

Most real-world settings are complex multi-agent environments, where the behavior of agents is influenced not only by static and unintelligent inanimate objects and variables, but also by the intelligent and purposeful actions of other agents which can be cooperative or competitive at a given time. In such an environment, behavioral outcomes depend on the goals, intelligence and the overall competences of other agents. However, it is often not possible to directly observe the properties – i.e., access the goals and strategies – of other agents. These properties are inferred from the actions and reactions of the agents in the course of interaction. Prior knowledge about their behavior can also be incorporated in the LLM model. Specialized datasets and finetuning methods can also endow LLM models with knowledge about the behavior or other agents. Some works incorporate specialized cognitive modules to infer various attributes about other agents, including their believes, intentions, knowledge level and general state of mind [182], [183]. Hypothetical Minds (HM) [182] observes the action history of other agents and leverage the information to predict their strategies and output a high-level description in natural language which can then be utilized to refine the model’s (HM’s) own behavior. 

### _3.5.2 Approaches to realizing situational-awareness in embodied LLMs_ 

### **(a) Physical agents in real world environments** 

The most straightforward approach to realize embodiment in LLMs is to design and implement embodied agents in the form of robots with appropriate sensing modalities and then integrate the advanced language understanding 

capabilities with the robot’s physical and sensory mechanisms. Embodied generalist agents must perform multiple tasks at the same time: perception, planning, navigation, object manipulation, natural language communication, physical interaction with humans and other AI agents, as well as and low-level control tasks. In principle, generalist embodied agents can be trained on specially-curated embodied datasets such as EgoExoLearn [184], Holoassist [185], EgoTracks [186] and EgoChoir [187] in an end-toend manner. Special embodied multimodal models such as EmbodiedGPT [172] (see Figure 5), PaLM-E [64] and AlanaVLM [188] are trained on these types of multisensory embodied dataset. The data commonly consist of egocentric datasets containing videos of humans performing diverse actions in different settings. 

The actions are typically aligned with context-relevant language descriptions. In addition, they sometimes often audio and other sensory information. In order to ensure that the embodied datasets are as realistic and informative as possible, some works (e.g., [189], [190], [191]) leverage wearable sensors like accelerometers, inertial measurement units (IMUs), global navigation satellite systems (GNSS), head-mounted displays (HMDs) and gyroscopes to capture additional information (e.g., location, orientation, pose, etc.) about the environments, objects, humans and the activities. Thus, the task of training a multimodal model is to learn a common representation for these multiple sensory information types. While this approach has demonstrated impressive capabilities for robots and embodied autonomous agents, it is exorbitantly costly and time-consuming to collect such datasets. 

Since it is often difficult and costly to develop and train language models from scratch for general-purpose multisensory embodied robotic systems, most works typically fine-tune pretrained multimodal large language models with task-specific datasets. That is, the realization of physical systems for embodied AI involves adapting the model to handle specific tasks and interactions – e.g., navigation [192], [193], [194], manipulation [195], [196], humanmachine dialogue [197], [198] – that are relevant to the physical capabilities and sensory inputs of the target embodied AI system. For instance, Palm-E [64] is specifically designed for kitchen settings. Therefore, the most common tasks it performs are navigation in the kitchen environment, recognizing household objects, picking and placing cooking utensils and other objects, assisting with general chores relating to cooking, cleaning, and serving food. Thus, the approaches are usually domain-specific addressing a restricted set of situations. Owing to the difficulty in curating sufficiently large and diverse real data for embodied tasks, many works [199], [200], [201] train large multimodal language models using synthetic datasets or augment real datasets with synthetically-generated egocentric data. Dedicated frameworks for generating (e.g., LEAP [202], EgoGen [203]) or annotating (e.g., PARSE-Ego4D [204]) synthetic egocentric data have been proposed. Generally, the target tasks and specific interactions the embodied AI needs to handle (e.g., navigation, manipulation, human-machine dialogue) are predetermined and a suitable dataset is selected or generated. While this workaround effectively mitigates the data curation challenge for specific embodied tasks, it is 

9 


Figure 5. A simplified representation of EmbodiedGPT [172]. The framework utilizes a large-scale egocentric, EgoCOT—curated as part of the work, to teach agents a wide range of embodied skills, including video captioning, visual question answering, multi-turn dialog as well as navigation and object manipulation in the physical world. It consists of four integrated components: (a) a vision-transformer to encode visual information from observations; (b) a custom submodule, so named Embodied-Former, to map input text and images (i.e., embodied instructions and visual information), and to generate relevant features for embodied, high-level planning and low-level control tasks; (c) a large language model to perform language-related tasks (e.g., image captioning, planning and embodied question answering); (d) a so-called policy network that generates low-level actions from the features learned by the Embodied-Former submodule. These actions allow the agent to physically interact with the real world using its actuators. Chain of thought approach is used to generate task-relevant goals from prompts. 

still difficult to extend these models to general, open-ended, long-horizon tasks. This is largely because current synthetic datasets, like their real counterparts, capture short, independent video snippets containing only partial and local information about the underlying Physical environment and tasks. It is particularly challenging to handle multi-agent systems [205], [206], [207] in complex environments where multiple factors interact over long-horizons. To address this limitation, some recent approaches propose to combine multiple specialized embodied modules to perform specific tasks [208], [209]. 

However, in terms of achieving AGI, this approach is still extremely limited. Firstly, the datasets are often static, with less opportunities for learning rich representations and complex skills. As these datasets are not interactive, agents can only make passive observations and process these observations as sensory signals for acting on the world. Secondly, agents cannot “live” in these environments and have experiences from first-person perspective. Moreover, training with such static datasets is fundamentally different from learning in the real world, where agents’ observations are a result of their own, mostly deliberate, actions – i.e., the agent controls the data it receives through interactions with the environment. A promising workaround is to train the agent model in a virtual world, a more complete simulation environment, and then transfer to the real world. 

### **(b) Simulated agents and virtual environments for embodied AI systems** 

A promising approach to simplifying the difficulty of developing and training embodied agents in the real world, is to create and train virtual agents in simulated 3D digital environments. This provides a low-risk, quick and cheap 

means to learn about the world. In a simulated environment, agents can also learn from humans through humancomputer interaction (HCI) interfaces [130], [210], [211]. They can also learn from the experiences of other agents through observation or interaction with them [212], [213], [214]. This is consistent with the way human learn in the real world. This shared observations and knowledge exponentially enhances the capabilities of the intelligent agents. 

The trained model learned in the virtual environment can then be transferred and finetuned for agents in the real world. Using this approach, sophisticated embodied agents can be effectively trained for complex, dynamic and unknown environments without requiring carefully-curated datasets or prior knowledge about the structure, sensory modalities and functions of the agent itself. It should be noted that autonomous agents such as chatbots, avatars, virtual medical assistants and conversational recommender agents can fully function as virtual agents instead deploying in cyberphysical systems. Such agents operating in virtual mode can still be considered as embodied in the sense that in their context (i.e., in the virtual sense) they can be endowed with most of the attributes of embodied intelligence, including virtual bodies, internal model of behavior, sensing and actuation capabilities that allow them to interact with the physical environment and receive feedback about the interactions. 

To facilitate general intelligence, the virtual environment must meet the following vital requirements: 

- Large scale, with the possibility of extension 

- Computationally efficient 

- Rich and informative 

- Adequate diversity and variability 

10 

_•_ Realistic and physically-plausible 


Figure 6. A practical case where situatedness (situational-awareness coupled with self-awareness) is needed: the red mini bus has to swerve the pedestrians to avoid knocking them down. Situatedness helps AIbased systems such as autonomous vehicles to adhere to acceptable behavior in society and also enables them to avoid serious incidents while incurring minimal penalty (e.g.,injury to occupants, damage of vehicle). In this particular case, situational-awareness allows the AI agent to understand the scene and know where to move to so as to avoid running into another danger while swerving the pedestrians. On the other hand, self-awareness allows the AI-driven vehicle to consider its own physical constraints in order to perform safe maneuvers. 

### **Common types of simulated worlds for training embodied agents** 

Simulated agents and virtual environments for embodied AI can be created in different ways. Some of the common approaches are based on using 1) 3D game engines and 3D graphics tools— e.g., [216], [217]; 2) realistic physics simulators— e.g., [218], [219], [220]; 3) extended reality (XR) technologies—e.g., [221], [222]; and 4) generative AI techniques such as LLMs and VLMs—e.g., [223], [224]. We briefly describe each of these methods in the following paragraphs. 

### _(i) Game engines and 3D graphics_ 

One of the most popular methods for developing simulated embodied agents in virtual environments is by the use of game engines 3D graphics tools. These tools can simulate realistic environments with dynamic conditions (e.g., rainy, bright, dark and foggy weather). These environments support virtual sensors and interactive objects that allow the agents to learn useful skills, affordances and associated constraints that mimic their real-world versions. 

For a number of reasons, there is a big incentive to use tools such as such 3D game engines. Firstly, it easy to create large-scale, realistic environments with these tools. Secondly, already-made generic environments that can be used for training LLM agents are widely available. Popular 3D environmnts like AirSim [225], AI2-THOR [226] and 

Carla [227] have been created with the Unreal Engine. In turn, tools for training LLM agents can be derived from these 3D simulation models. For instance, LLM-based multiagent environment simulation frameworks such as EAISIM [228] and AeroVerse [229] are based on AirSim [225]. MultiPLY [215] learns by interacting with simulation environments that integrate sensory-coupled 3D virtual objects—that are in turn derived from the Objaverse [230] and ObjectFolder [231] datasets—into a large-scale virtual world built around Habitat-Matterport 3D [232]. In addition, nonplayable characters (NPCs) [233], [234] created for computer games that (by themselves) exhibit intelligence and interact with the target agents (e.g., see [235]) can be imported to existing environments as game assets. They support complex behaviors, long-horizon interactions and can engage in sophisticated storylines. 

One of the main limitations of this approach is the enormous computational requirements for developing worldscale environments. There is often the need to balance realism with game performance, thereby constraining the level of realism that can be achieved. Another major challenge relates to the inadequacy of game engines to effectively model complex, physically-plausible mechanical interactions as the tools are typically optimized for visuals, an important feature in gaming. 

_(ii). Realistic physics simulations_ To overcome some of the aforementioned shortcomings of game engines in creating realistic simulation environments for training embodied agents, recent works employ physics engines (e.g., PhysicsX, Bullet, Symbody and ODE) [236] to create realistic, physically plausible simulators such as PyBullet [218], Isaac Gym [237], DIFFTACTILE [238] and for generating virtual agents and environments. For instance, state-of-the-art models for LMM embodied agents such as ROS-LLM [239], LANCAR [240] and MHRC [219] are based on PyBullet [218]. Compared with 3D game engines, this approach provides more controlled, physics-informed environments where agents can interact with objects and phenomena in a way that aligns with real-world behavior. These tools are particularly suited for agent learning approaches based on reinforcement learning paradigm, since the embodied LLM agents can receive realistic rewards or penalties based on their actions in the environment. The realism provided by physics-based simulators helps agents develop more practical, transferable skills that could eventually be applied in real-world scenarios. Complex tasks such as object manipulation, embodied path planning, and interaction with dynamic environments can be learned more effectively with such accurate physics. 

While physics simulation supports more realistic behavior, the approach is inherently expensive. Moreover, it is often not possible to simulate very complex behaviors or phenomena whose underlying mechanisms are unknown. These problems constrain the range of scenarios that can be effectively modeled and the degree of sophistication that can be achieved in any given task. 

_(iii). Simulated virtual worlds in extended reality (XR)_ Immersive experiences offer more natural settings for AI agents to acquire useful skills as the virtual agents can interact seamlessly with humans and the real world. Agents trained in this type of environment can comprehend complex, multimodal input, including gestures and emotions, 

11 


Figure 7. MultiPLY [215], a state-of-the-art embodied LLM trained on simulated worlds, supports a vast array of sensory modalities, including textual, visual, thermal, audio and tactile. By jointly encoding context information from multiple sensory modalities and learning the relationships among these diverse representations, the framework achieves advanced capabilities on multiple open-domain tasks such as task planning, tool use, multimodal dialogue, video captioning, question answering, spatial reasoning and navigation. 

and generate contextually appropriate responses [241]. Extended reality (XR) tools, especially virtual reality (VR) and mixed reality (MR) techniques, can create immersive, highly interactive 3D environments that accurately simulate realworld behavior. In XR environments, embodied LLM agents can leverage simulated sensorimotor feedback to learn to perceive and act in the world. In mixed reality mode, virtual agents ‘live’ in the real world and can interact seamlessly with the real world as well as with other virtual objects [241].. Such mixed reality agents can directly perceive the real world through sensors and internet of things (IoT) devices [242]. VR worlds can also provide realistic environments with human-looking virtual agents in the form of avatars that interact with and learn from humans. Social XR [243], [244] platforms create settings that allow diverse humans to engage in practical human-centered activities (e.g., trading, shopping, etc.) with virtual objects [245], [246]. They can simulate human-agent and agent-agent interactions, making it an ideal setting for training agents in social or collaborative tasks. 

While immersive virtual environments have been created using computer graphics tools and game engines, more recently, the use of generative AI techniques have been employed to build entire XR world models [247], [248] or to create specific content for existing XR worlds wang2024systematic. The power of have LLMs have also be exploited to adapt computer graphics-generated worlds (e.g., in SituationAdapt [249] and GUI-WORLD [250]) to the underlying social setting and physical environmental attributes. 

_(iv) Virtual environments generated by AI (e.g, LLM and VLM)_ Because of the complexity of simulated virtual environments and the associated high labor cost in their creation, a large number of recent approaches (e.g., [223], [224], [251], [252], [253]) have proposed to circumvent this problem by utilizing pretrained foundation models as world simulators to accurately infer the properties of the world and, hence, produce embodied action plans and predict how differ- 

ent actions alter the world.. With this approach, the LLM frameworks are specially constructed to leverage their rich knowledge to generate embodied training environments that serve as media in which other embodied LLM [254] and VLM [254] agents will be trained. This line of work has been particularly successful in robotics for complex tasks like embodied planning, navigation and manipulation tasks. 

A common approach [251], [255], [256], [257], [258] is to produce intermediate code from high-level goals that are specified as natural language instructions which is then used to generate plausible 3D world models that embodied agents interact with. These methods typically utilize the rich prior world knowledge encoded in the LLM to guide code generation. The generated code can further manipulate the world model to produce diverse scenes and environment conditions based on the artificial agents’ desired goals and experiences. Hu et al. [255] propose a code generation approach that synthesizes 3D scenes by generating Blender code. To achieve this, they build a scene graph that encodes the geometric relationships and constraints of primitive 3D objects. A specialized VLM module based on GPT4-V, sonamed SceneCraft, is then able to leverage the scene graph to generate Python scripts that creates and populate a 3D scene in Blender with relevant objects. SceneMotifCoder [259]leverages LLM code generation for open-vocabulary 3D object generation and arrangement in a geometry-aware manner. Tang et al. [256] frame the embodiment problem as a model-based reinforcement learning task that leverages prior knowledge in the form of LMM to learn embodied planning and actions with only a few interactions with the environment. The world model in these cases are built from python code with the help of natural language instructions. While this approach seems promising, the practical difficulty of modeling large, complex and dynamic environments in this manner limits the method to relatively simple environments. For instance, for practical realization, Tang et al. [256] formulate the virtual scene as a deterministic environment where interactions are episodic. Owing to the 

12 

|**Aspect of**<br>**embodiment**|**Main contributions to AGI capability**|**Common approaches for realization in**<br>**LLMs**|**General remarks**|
|---|---|---|---|
|**Goal-awareness**|• Enhances autonomy<br>• Allows agents to be proactive instead of merely reacting to situations<br>• Ensures consistency of behavior<br>• Allows agents to multi-task<br>• Enhances flexible and adaptive behavior<br>• Facilitates collaborative task execution (since all agents can focus on goals)<br>• Allows ability to recover from anomalous situations|• By implicitly learning from data (e.g., [151, 152])<br>• Through specifying goals in input prompts (e.g., [159,<br>161, 169])<br>• By finetuning on goal-aware datasets (e.g.,[165, 167])<br>• By explicitly incorporating goals in the deep learning<br>model (e.g., [156, 157, 158])|Goal-awareness in LLMs is limited to<br>low-level goals about specific tasks.<br>Current<br>approaches<br>cannot<br>enable<br>high-level,<br>overarching<br>or<br>global<br>goals that can guide behavior in all<br>situations.|
|**Self-awareness**|• Allows agents to better make use of external resources since they know<br>their limitations and can enlist external sources as needed<br>• Enhances reliability and safety (by virtue of agents not attempting tasks<br>they cannot succeed in)<br>• Facilitates continual learning and self-improvement (by introspection and<br>reflection)<br>• By acknowledging its own limitations, the agent promotes trust|• Through in-context learning (e.g., [268] )<br>• By finetuning on self-aware datasets (e.g., [274] )<br>• By specifically querying agents (through prompts) on<br>their knowledge and capabilities (e.g., [279, 281])<br>• Using reinforcement learning with human feedback<br>(e.g., [278] )|Self-awareness<br>is<br>inherently<br>task-<br>dependent and an agent may be self-<br>aware in a limited set of settings.<br>Moreover, it is a continuous metric<br>and there are often varying degrees of<br>self-awareness<br>in<br>different<br>tasks.<br>There is currently way of assessing<br>the overall self-awareness of LLMs.|
|**Situatedness**<br>**(situational-**<br>**awareness)**|• Facilitates strategic behavior (decisions and actions accommodate the goals,<br>expectations and actions of others)<br>• Enhances high-level context understanding<br>• Promotes ethical and social intelligence<br>• Allows better interaction with the environment (including humans and other<br>agents)<br>• Enhances safety and reliability (by virtue of agents knowing and avoiding<br>situations or actions that present danger or risk)|• By deeply learning from real-world environments<br>using datasets (e.g., [183, 186, 189])<br>• Using synthetic egocentric datasets using 3D graphics<br>tools (e.g., [198, 199, 200])<br>• Interactive world models based on game engines (e.g.,<br>[215, 226, 227])<br>• Realistic physics simulations (e.g., [ [219, 239, 240])<br>• Immersive virtual worlds in XR (e.g., [241, 243])<br>• AI-generated virtual worlds (e.g., [255, 257, 258])|Egocentric datasets are static and not<br>interactive; they are expensive to<br>curate and scale. virtual world models<br>are highly interactive and scalable but<br>suffer from the so-called Sim-to-Real<br>gap.|
|**Deliberate**<br>**action**|• Fundamentally, enables agency<br>• Promotes log-horizon planning<br>• Serves as the primary mechanism for physical interaction<br>• Serves as a means for low-level sensorimotor control<br>• Provides a means to extend agent’s capabilities (by means of tool use)|• Employing special pretrained foundation models such<br>as VLAs (e.g., [303, 304] )<br>• The use of external tools (e.g., [84, 392])<br>• Learning<br>action<br>sequences<br>using<br>neuro-symbolic<br>approaches (e.g., [253, 293, 294] )|LLM<br>agents’<br>ability<br>to<br>perform<br>physical actions is limited to simple<br>actions that can be decomposed into<br>definite steps.|


Figure 8. A summary of the important contributions of the main aspects of embodiment to AGI capabilities and the general approaches to implementing each of these components of embodiment in large language models. 

difficulties in achieving realistic, physics-based interactions with LLM-generated worlds, further refinements are often employed to ensure physically-plausible behavior [222], [260], [261], [262]. For instance, Volum et al. propose a code generation method to synthesize interactive objects and characters for virtual worlds using LLM prompting. Their approach, _Craft an Iron Sword_ [260], additionally employs the LLM to infer interaction outcomes and generate plausible response (i.e., in the form of scene manipulation). 

### **3.6 Self-awareness** 

Self-awareness is the ability of the AI system to understand its very nature, including its properties, capabilities, limitations, context, and role in interactions with external entities. The body’s physical structure influences how biological systems or living organisms process information. Its shape, size, and capabilities constrain and afford certain capabilities and types of actions, which in turn affect the cognitive strategies required to achieve them. The nervous systems of living organisms naturally learn to control the body mechanisms such as muscles and limbs in a body-specific way. This explains, for instance, why humans require extensive training to be able to easily use prosthetic limbs [263], [264]. A self-aware embodied agent can also understand the implications of its actions on other agents (human and artificial) and the environment overall. An AI agent that is both self-and situational-aware is said to be situated. Figure 6 depicts a typical scenario where situatedness is critical for an AI system to take correct decisions. 

### _3.6.1 Self-awareness in generic LLMs_ 

Many researchers (e.g., [265], [266], [267]) have investigated self-awareness in LLMs, including the ability know the limit of their own knowledge [268], [269], [270], and to introspectively reflect on decisions and actions [116], [271], [272], and adjust behavior. Based on the preliminary evidence, multimodal LLMs are generally considered to possess selfawareness as an emergent ability, an ability that arises spontaneously as a result of the sheer volume of training data. Yin et al. [268], for example, show through extensive empirical studies that state-of-the-art LLMs naturally possess a degree of self-awareness about the limit of their own knowledge, i.e., knowing what they do not know. Several other studies confirm this ability [273], [274], [275], [276], [277]. 

### _3.6.2 Achieving self-awareness in LLMs_ 

While, out-of-the-box, current state-of-the-art LLMs like GPT-4 still lack true self-awareness in the sense of human cognition, a number of techniques can help to elicit selfawareness. For instance, it has been shown that in-context learning [268], reinforcement learning with human in the loop [278] and fine-tuning [274] can be used to attain some level of self-awareness in LLMs. A common way to achieve self-awareness is to evaluate a model’s outputs for inconsistencies or errors by comparing generated responses with known facts or previous dialogue. In this way, the model can be explicitly prompted about its limitations [85], [273]. Instead relying on humans to probe and prompt LLMs about their knowledge or capabilities, a recent approach is 

13 

to formulate the self-awareness task as an intuitive search question, whereby an embodied agent queries its base LLM on the existing world knowledge about the given situation [279], [280], [281]. In line with this line of work, multiple LLM agents can collaborate to assist one another, through probing or questioning, to reveal capabilities and inherent weaknesses [282]. More recent works (e.g., [283], [284], [285]) have proposed to infer the properties of the LLM models from the hidden representations of their internal states. SEAKR [283] computes a so-called self-aware uncertainty from latent representations of the internal states of the LLM’s feedforward network by comparing the consistency score across multiple responses. Self-Controller [285] incorporates a dedicated submodule, state reflector, that stores state information for assessment. Potentially, these approaches could be extended to address awareness of more pertinent attributes of embodied LLM agents, allowing them to, for example, become cognizant of their physical construction, the mechanisms of action and response, as well as the attendant outcomes of actions and their own physical limitations. A self-aware LLM can recognize when its internal knowledge is insufficient to address a problem, and turn to additional resources, e.g., retrieval-augmented generation [286], [287]. This approach is similar to the way human enlist additional resources to tackle problems they are not capable of handling by themselves. The useful attributes of awareness of both self and the environment in embodied AI systems is better illustrated by Figure 8. 

### **3.7 Deliberate action** 

Although LLMs are primarily language entities, when endowed with embodiment—e.g., as physical robots, virtual agents, or other interactive systems—they can take deliberate actions in the real world or through virtual or simulated interactions. This capability stems from their ability to comprehend task- or goal-oriented dialogue [172], [288], [289], [290], formulate step-by-step plans to accomplish tasks or to achieve target goals [253], [291], [292] and execute taskappropriate actions according to the predefined plans [293]. An embodied agent can discover new affordances and previously unknown properties of objects through deliberate interaction with the environment. This enables it to make decisions or take actions that are more beneficial, empathetic and morally informed. Most embodied LLM systems (e.g., [253], [294], [295]) incorporate dedicated planning and action submodules to handle action execution and interaction with external entities. These specialized modules typically employ representations of action primitives that are related to the agent’s design and capabilities. The action primitives are then encoded in the form of policies (i.e., rules for allowable behavior) [296], [297], [298] or into action templates [299], [300] that describe how to respond to various scenarios. Through the ability to use external tools [301], LLMs can extend their potential to perform various actions. 

Vision-language-action models (VLAs) [302], [303], [304], [305], [306] are a new family of multimodal foundation models specifically designed to execute actions. They jointly learn visual, language and action modalities through end-toend training. Consequently, they can perceive the environment, interpret instructions, carry out high-level planning 

and synthesize low-level actions to complete various tasks. VLAs are commonly used in robotic applications. They particularly excel in tasks such as open-world navigation, object manipulation, grasping and interpreting and responding to complex sensorimotor signals, including verbal and nonverbal cues. State-of-the-art Bi-VLA [302], VLAs such as RT-2 [307], Unified-IO 2 [305], QUAR-VLA [306] and 3D-VLA [303] can perform a wide range of complex activities in open-domain settings. 

## **4 SYMBOL GROUNDING** 

### **4.1 Basic idea of symbol grounding** 

Symbol grounding, or simply grounding, relates to the ability of AI systems to connect the abstract internal representations of concepts in computational models to their real-world equivalents. In its basic form, the grounding problem essentially involves specifying a set of primitive symbols, defining their semantic connotation and postulating rules for manipulating them. The rules that govern symbol manipulation are purely syntactic in nature, and are independent on the assigned meaning (i.e., the realworld, physical interpretation) of the symbols [95], [308]. The symbols themselves are abstract primitive entities that are treated as atomic tokens that can be combined into composite tokens to encode higher-level concepts [309]. The symbol system is supposed to be semantically interpretable at all levels of representation [95] (see illustrations and further explanation in Figures 9 and 10). Symbol systems are, thus, patterns of information that provide access to the external world. Newell and Simon [310] hypothesized that physical symbol systems are not only necessary but also sufficient for intelligence. 

Methods of grounding in artificial intelligence and large language models have been inspired by the way the human brain processes and associates sensorimotor information to the external world [311], [312], [313], [314]. Psychologists have long argued that the human mind itself relies on a symbolic system of representation and manipulation of information in mental processes (see [311], [314], [315], [316], [317]). Per this view, cognitive phenomena that influence human perception and behavior, including vision, language, emotions, thoughts, perspectives and beliefs, are governed by symbol processing [318], [319]. It is worth noting that a large class of symbols do not relate to physical properties of the world but rather to abstract concepts. For example, symbols such as “happy”, “innovation’, “clever” and fascination” are merely concepts that describe high-level phenomena. However, humans are still able to effortlessly connect these symbols with their appropriate semantic contexts. When presented with images of people or even animals, for instance, humans can correctly classify them by their emotional state. 

14 


Figure 9. Human cognition relies on associating abstract mental representations, or symbols (e.g., words), with entities, concepts and phenomena in the real world. The symbol grounding system allows the internal cognitive system to access the external world. In this manner, internal representations acquire meanings that are invariant in a given sense, and can therefore identify referents (i.e., the objects or categories referred to) in different contexts. In the same way, grounded artificial cognition aims to connect abstract computational representations to actual objects and concepts with respect to some concrete interpretation. 


Figure 10. The grounding mechanism allows intelligent systems to represent and manipulate cognitive information in a hierarchical manner by combining different symbols to form more complex, composite representations. In (a), for example, the symbols "metal", "wood", "chair", "structure" all provide context to describe the high-level concept "sit". The semantic content in (b) is the activity "to walk". (c) and (d) are more complex scenes consisting of several hierarchies of symbols but they still represent very simple semantic contents as the labels indicate. 

### **4.2 Grounding as a bridge between the digital world and reality** 

Language uses symbols (digits, words, lexical concepts, etc.) represent humans’ understanding of various ideas about objects and concepts in the world: their essence, properties, relations, and possible actions that can be performed on them by an agent. The goal is to provide more meaningful and rich contexts of the real world to facilitate a better understanding of and allow interaction with the external envi- 

ronment by establishing the correct relationship between the abstract symbols captured internally in AI models, and the physical world they seek to represent. In essence, grounding aims to bridge the inherent semantic gap that exists between artificial intelligence and the real world. This allows AI systems to “make sense of” inputs from the environment, thereby enhancing their situational awareness and taskappropriate behavior [320]. 

### **4.3 General approaches to symbol grounding in AI** 

Classical techniques for symbolic grounding utilize explicit representations, with fixed rules and ontologies to describe the relationships and properties of the abstract concepts and physical entities involved. For instance, mathematical operations based on variable binding techniques [321], [322] and logic rules [323], [324], [325]are often used for symbol manipulation. The key advantage of this class of methods is the (increased) transparency and interpretability of the resulting models. However, the approach is highly restrictive as it requires all situations to be anticipated in advance and handled appropriately. Furthermore, it is challenging to (move) from fixed, structured representation of symbols to high-level cognitive tasks like perception and reasoning in the open world. Another layer of difficulty lies in the ability to unambiguously and reliably ground fuzzy concepts related to human social relationships and interactions as these are often have strong in cultural contexts and lack consistent interpretations. In these scenarios symbolic manipulation techniques are generally incapable of adequately processing cognitive information as high-level rules often fail to capture contextual nuances and the symbols themselves tend to have differing interpretations, leading to unpredictable or inconsistent inference. Because of the serious limitations of the analytical techniques based on fixed symbols and logical rules [326], probabilistic graphical models [327], [328] and knowledge graphs [329], [330], [331] have become more viable alternatives as a result of their flexibility, better representation power and scalability. These recent methods, the so-called neuro-symbolic techniques [332], [333], [334], [335], employ primitive entities as representation priors but utilize artificial neural networks to learn the relationships and properties of the symbols. This approach has proven effective but also suffers from poor scalability. Another recent approach, neuro-symbolic grounding [336], [337], [338], [339], seeks to ground primitive symbols implicitly by learning the semantic connections of abstract symbols and the real world with the help of neural networks. Methods for learning symbol representations implicitly end-to-end from data without relying on explicit primitives have also been proposed [340], [341], [342], [343]. 

### **4.4 Approaches to grounding in LLMs** 

We discuss the main approaches for symbol grounding in large language models in the remaining subsections. A detailed summary of these approaches is presented in Table 1. 

### _4.4.1 Grounding LLMs with knowledge graphs_ 

In large language models, a common way to capture expressive relationships between various entities, in this case, 

15 

between abstract symbols and real-world entities, is by the use of knowledge graphs (KGs) [344], [345], [346]. Knowledge graphs represent words as nodes in a visual tree-like structure known as a graph or semantic network. These words represent individual objects, object categories, events and concepts. The relationships that exist among the various words are described by edges connecting the nodes. Through this mechanism KGs can store a large volume of explicit knowledge that is grounded in real world. For this reason, they have been proposed to mitigate common problems such as hallucination and provide a means to internalize physically-grounded knowledge in LLMs [347], [348], [349], [350]. This reduces the need for very large training data and, hence, saves time and reduces training cost. Besides, in contrast to pure neural architectures, the structured knowledge in KGs encodes explicit relationships and is therefore more semantically meaningful and suitable for emergent tasks such as reasoning and planning. 

While LLMs augmented with KGs can enhance the inferential capabilities of the LLMs, manually building the KGs is a nontrivial task [351]. Consequently, with their extensive world knowledge, LLMs have, in turn, also been proposed to build or enrich KGs (see [352], [353], [354], [355]). Thus, these two classes of methods, LLMs and KGs, can be integrated in a way that allows them to mutually enhance each another. This capability presents a promising prospect for symbol grounding as KGs are incorporated in the LLM framework to improve its performance, while at the same time the resulting LMM helps to extend and refine the KG with additional knowledge to even produce better outputs. This could in turn generate even better content for the graph, and so on. Some recent works [356], [357], [358] are already exploring this approach. 

### _4.4.2 Grounding LLMs by ontology-driven prompting_ 

Prompting techniques have been used to steer LLMs to generate more nuanced, contextually appropriate responses. The technique utilizes user-supplied instructions or specific examples (i.e., input-output pairs) at the inference stage. The process does not affect the learned model parameters and also avoids costly re-training or finetuning procedures. This form of adaptation, known as in-context learning, can effectively ground and align model inferences with real-world context according to user needs. More recently, instead of directly inputting human-readable instructions as prompts, a large number of works (e.g., [359], [360], [365], [366], [367]) have sought to leverage ontologies as symbolically grounded knowledgebases that provide context-relevant prompts in an automated way to guide the model on how to effectively deal with specific situations. The ontology engine is created by a formal specification of facts, rules as well as entities, categories, properties, and relations between them. As an alternative to building the symbolic system (i.e., ontology) manually, some works (e.g., [368], [369] have proposed to exploit LMMs to create or enhance ontologies. Different types of operations to generate new knowledge from established facts and rules in specific contexts. 

### _4.4.3 End-to-end grounding through embedding_ 

In LLMs, the symbol grounding problem can be solved by implicitly modeling the meanings of and the associations 

between learned concepts in the high dimensional vector space [370], [371], [372]. In the vector space, symbols such as words and visual concepts are encoded based on the contexts in which they frequently occur and how they relate to other symbols. Researchers have devised techniques that exploit this representation to associate learned embeddings to the actual objects, perceptual experiences, actions, or concepts in the real world [361], [362], [373], [374]. These embeddings can also establish the semantic relationships with other concepts. For example, the phrase “Toyota Landcruiser” can be connected to “Car”, “Vehicle”, “Transportation”, etc. Moreover, symbol manipulation procedures can also be learned in an end-to-end manner using the expressive power of the underlying neural networks. 

While this class of techniques is more scalable and relatively simple to implement compared with the other grounding methods covered here, it is important to note that the approaches may not yield precise mappings in some cases. It is also not often possible to determine which symbols are not correctly grounded. For these reasons, grounding methods that leverage vector embeddings typically suffer from issues of trustworthiness and lack of explainability. 


Figure 11. Grounding can be achieved by actively exploring the world and learning about the forms and meanings of entities the abstract digital symbols refer to. Reinforcement learning is an effective way to learn these symbols by interaction. Illustration courtesy [375]. 

### _4.4.4 Grounding by active exploration and interaction with the environment_ 

An important way to ground symbols is to actively explore the world to find the meanings of relevant entities [312], [376], [377]. Approaches for facilitating generalist capabilities of LLM agents by means of embodiment have been discussed in detail in Section 3. From the discussion, it is clear that the role of embodiment as a tool for knowledge acquisition is anchored in its ability to support deliberate actions or exploration and interactions with the world [128], [378], [379]. In addition to the cognitive skills that can be learned with the help of these interactions, the (embodiment) mechanism helps LLM agents to learn the meanings of abstract symbols through direct experiences with objects and phenomena in the world. Current approaches (e.g., [107], [363], [380], [381], [382]) typically employ reinforcement learning techniques to directly connect language constructs, physical 

16 

Table 1 

A summary of the main approaches for grounding large language models 

|**General approach**|**Description**|**Rep. works**|**Main strengths**|**Weaknesses**|
|---|---|---|---|---|
|Knowledge graphs|Represents the relationships between<br>symbols and the actual entities they<br>represent in a structured form.|[347], [349]|Can naturally handle hierarchical relationships;<br>easy to integrate into LLMs; highly transparent.|Laborious process; difficult to represent<br>ambiguous or fuzzy concepts.|
|Ontology-driven<br>prompting|Utilizes in-context learning (high-level<br>instructions as input prompts) to explic-<br>itly ground symbols.|[359], [360]|Can be used to refine already-grounded symbols;<br>can be used with any of the other methods; reliable<br>since grounding is explicit.|Cannot accomplish grounding exhaustively;<br>not scalable; requires knowledge about the<br>underlying concepts and relationships.|
|Vector space<br>embeddings|Deeply-learns and encodes relationships<br>in the feature space.|[361], [362]|Highly scalable; can learn relationships that aren’t<br>known by the human developers; very simple and<br>easy to implement.|Requires large and high-quality data; may learn<br>spurious relationships; opaque and difficult to<br>diagnose.|
|Active exploration|Methods whereby symbols are grounded<br>by embodiment mechanism through inter-<br>action with the world and experiencing the<br>behavior of objects and phenomena and the<br>effects of actions. Mostly relies on RL<br>approaches to learn useful representations.|[107], [363]|There is direct coupling of cognitive information<br>with the real world; learned representations are<br>physically-plausible.|Expensive and time-consuming to implement; may<br>produce incomplete connections when used alone;<br>cannot work on purely abstract concepts.|
|Generative AI|Leverages generative AI models ( LLM,<br>GAN, VAE, VLA ,VLM) are employed<br>to synthesize the patterns and relation-<br>ships of symbols and referents.|[353], [354]|Does not require prior knowledge about relationships;<br>extremely scalable; very easy to implement.|Not transparent; prone to fake connections (e.g.,<br>hallucinations); not easy to verify; representations<br>may be unreliable.|
|External knowledge|Utilizes readily-available knowledge<br>about relationships contained in external<br>knowledge bases (e.g., through RAG) to<br>ground symbols in LLMs.|[286], [364]|Leverages a wide variety of existing knowledge;<br>can augment other approaches; provides practically<br>unlimited scope of domains and tasks for grounding<br>symbols.|May introduce inconsistences as a result of different<br>representation schemes; external information may be<br>subject to malicious attacks.|


objects, abstract concepts and actions. To achieve this, the agent first learns to ground low-level symbols in tangible experiences. In turn, high-level concepts can be built on and grounded in these low-level symbols. Human-in-theloop reinforcement learning approaches [383], [384] have also been used to provide semantically richer grounding for high-level concepts. Since training agents with reinforcement learning requires a huge number of trials, virtual worlds are commonly used to simulate the behavior of the real world [299], [385], [386], [387]. Figure 11 show a generalized architecture of this approach. 

### _4.4.5 Leveraging external knowledge for LLM grounding_ 

Besides the explicit symbolic grounding methods discussed, LLMs can also leverage external knowledge from diverse sources to provide “weak” grounding. So-called encyclopedic knowledge graphs [350], for example, can represent a large volume of structured knowledge mined from diverse sources, including encyclopedia like Wikipedia [388] and relational databases [389], [390]. Even though these approaches may not strictly involve abstract, primitive entities with connected by syntactic or logic rules, they still provide a bridge between the pure implicit knowledge in classical LLMs trained on large-scale generic datasets. RetrievalAugmented Generation (RAG) [85], [286], [364] is another common technique for grounding LLMs on external knowledge. The basic idea is to leverage additional information from external sources to augment available knowledge for the grounding process. RAG is particularly useful when there is the need to augment the generic knowledge stored with domain-specific knowledge within a very narrow context [391], [392]. Another popular form of RAG, _domain tool augmentation_ , enables LLMs to access and use external tools and plugins through specially designed application programming interfaces (APIs) [393], [394], [395]. 

## **5 CAUSALITY** 

### **5.1 Causality in artificial and human intelligence** 

Causality characterizes how various factors, phenomena or events influence other events, objects or processes in the real world [396], [397]. Causal learning in its simplest form is aimed at determining the dynamic relationships between two variables, where one variable, the cause, directly influences another variable, the effect. While grounding primarily deals with connecting primitive symbols such as words to their meaningful representations (i.e., variables, phenomena, concepts, etc.) in the physical world, causality is concerned with explaining the underlying mechanisms and reasons responsible for changes in these parameters and how they affect various outcomes in the world. In machine learning and AI, known casual relationships can be explicitly encoded by their human developers. 

Causal reasoning – the process of leveraging the understanding of cause-and-effect relationships to explain events–enables AI systems to reason about (make accurate predictions about) complex real-world phenomena such as the resistance of structures to adverse weather elements, climate change, spread of diseases, accidents, population growth, economic performance, etc. This understanding is vital for everyday activities such as cooking, washing and driving (see Figure 13). Another vital role of causal reasoning is to improve robustness to interference and maintain correct inference when the underlying conditions and internal mechanisms or the environment changes. Thus, causal modeling allows AI systems to better generalize and transfer learned knowledge to new settings. Additionally, causality-aware models can account for inherent limitations and deficiencies of observations or data. For example, they can eliminate or mitigate the effects of adversarial examples [398], [399], [400]. and biases [401]. 

### _5.1.1 Basic principles of causality_ 

Causal understanding can be categorized into different degrees based on the level of causal reasoning power they per- 

17 

mit. These degrees range from basic associations to reasoning about hypothetical scenarios. One of the most popular classification frameworks was formalized by Pearl in [402]. It describes a three-level hierarchical scheme for classifying causal relations derived from observations, or more specifically, from data. The levels are designated as Association (Level 1), Intervention (Level 2), and Counterfactual (Level 3) —see Figure 12 for a summary of the typical questions addressed by each of these levels of causality. According to this scheme, solving reasoning problems at any level is possible only if information from that level or higher is available. The lowest level of causal reasoning, Association, relates to situations where answers to questions are obtained directly from observations in the form of statistical relations in the observed data. Intervention, the second level of causal reasoning, involves estimating the extent to which changing one variable (for example, treatment option) affects a target variable (i.e., a particular outcome, in this case recovery). Causal information at this level allows the effect of specific actions to be correctly predicted. For example, a force of 10 Newtons impacting a heavy truck would not cause any measurable motion. The third and highest level, Counterfactual, allows answering hypothetical questions or making inference about unobserved outcomes. This involves answering "what if this happened" type of questions- that is, what could have happened if certain events had not occurred or had happened differently. Counterfactual reasoning allows us to determine which variable to manipulate, and to what extent, in order to change a target variable to some desired state (obtain a desired treatment outcome). Solving intelligence problems at this level involves using both associative and interventive information. 

|**Level of**<br>**causality**|**Types of cognitive functions**<br>**supported**|**Types of problems or questions that can be**<br>**solved**|
|---|---|---|
|1. Association|Observation or recognition|What is X? How would the observation X affect<br>our believe about Y?|
|2. Intervention|Projection or interpolation|What … if?  What will Y be if X is 1.5?<br>How would Y change if X were to double?|
|3. Counterfactual|Imagination, analysis,<br>retrospection|Why? What if X had happened differently? What<br>would the inflation rate in 2024 have been if the<br>Covid-19 pandemic had extended beyond 2022.|


Figure 12. Levels of causality per Pearl [402] and the types of problems each can handle. 

### **5.2 Approaches for modeling causality in LLMs** 

Learning causality (or causal modeling) generally aims to solve two problems: (1) causal discovery – identifying the underlying mechanisms, their associated physical parameters and the interrelationships that govern the operation of the system; and (2) causal inference – the task of estimating the effects of causal variables on one another based on a pre-defined hypothesis about their causal relationships [403]. Causality modeling can be in the form of implicit learning of causal relationships [404] or explicit representation using prior knowledge about some domain-specific causal mechanisms and relationships [405], [406]. Implicit causal learning methods rely on end-to-end deep learning methods to identify cause-and-effect relationships directly from data or apply this knowledge for inference. We discuss the important methods for modeling causality in the next 

subsections. A comparison of these methods is summarized in Table 2. 


Figure 13. Interpreting events and observations or performing everyday activities such as cooking and driving requires an understanding of causal relationships. In cooking, for example (a), there is the need to understand concepts like volume, weight, boiling, as well as the behavior of entities such as fire, etc. Similarly, driving (b) requires an understanding of concepts such as speed, momentum, inertia, collision, and soo forth. 

### _5.2.1 Conventional deep learning methods_ 

Multimodal LLMs trained on large-scale generic data have shown a great capacity to model causal relationships [404], [407]. This is mainly achieved by learning hidden patterns from the vast amount of training data. For instance, an LMM may be able to infer important variables that impact economic growth or inflation, as well as identify specific causal links between these variables via purely learned patterns, even when this information is not explicitly specified in the training data. Knowledge acquired in this manner is constrained by the fact that not all observed connections have cause-and-effect relationships. Indeed, a large number of real-world phenomena exhibit correlative relationships [97], [408] –a relationship in which changes in the target variables, by coincidence or by unrelated influences, follow each other but are actually not related by any causal link. In reasoning tasks such false correlations can lead to inaccurate or wrong conclusions. 

In addition, owing to their ability to learn cause-effect relationships by discovering hidden patterns in training data, LLM’s are also trained on extensive text that describe cause-effect relationships, including mathematical relations, scientific principles and laws, etc. In the training process, for example, models can acquire knowledge about causal relations that allow them to handle high-level causal reasoning tasks– including interventions [409], [410], [411] and counterfactual reasoning [410], [412], [413], [414], [415], [416] – from explicit statements such as “lack of physical exercise leads to obesity”. Despite this seemingly powerful ability 

18 

to model causality, researchers have shown that state-ofthe-art LLMs are not able to acquire real causal reasoning capabilities [91], [417], [418], even with additional training aimed at enabling causality, including in-context learning and finetuning [419]. Specifically, LLMs trained purely on data, without internal causal modeling mechanisms, are, not inherently aware of physical laws or underlying mechanisms and principles that govern behavior in the real world, and their predictions are often merely based on learned correlations. This can lead to serious and dangerous mistakes. To address this limitation, researchers often have to rely on finetuning the models on specially-curated causal datasets (e.g., [420], [421]) to discover causal relationships. However, this approach is a laborious and difficult task that is often impractical to scale up in complex real-world settings. Moreover, the method often requires many simplifying assumptions that can sometimes lead to incorrect relationships (see [422], [423]). 

### _5.2.2 Neuro-symbolic methods_ 

In contrast to the DL approach which builds predictive model that mainly learn statistical dependencies, neurosymbolic methods explicitly incorporate prior knowledge about causal mechanisms into the LLM model. One way to achieve this is by leveraging knowledge graphs [331], [350] and other structured knowledge-based causal representation and inference techniques [424], [425], [426]. As these models naturally encode relationships between concepts, many works (e.g., [354], [427], [428], [429], [429], [430], [431]) utilize them to provide structured knowledge as causal mechanisms which the LMM then incorporates into its information generation process. One of the most effective neuro-symbolic approaches to extending the causal reasoning ability of LLMs is to integrate causal graphical models [432], [433], a special class of structured knowledge techniques, that, by their nature, are inherently causal. The basic approach is to represent causal assumptions formally using special diagrams or graphs. In the representation, nodes of a graph represent causal variables while edges indicate the existing causal relationships between the variables. By evaluating the effect of several variables, it becomes possible to determine whether or not the prior assumptions about causality are valid. And in the case where these assumptions hold, to derive mathematical expressions that describe the relationships. Conversely, the methods allow researchers to falsify causal assumptions. The idea is simple: to establish causation, isolate and induce a change of one of the possible factors. Where there is causation, it will manifest as a corresponding change in the target variable. The learned latent structural relationships are then integrated into the LLM’s neural network’s learning process. A large number of works (e.g., [434], [435], [436]) that employ causal graphical models [432], [433] have demonstrated the potential of this . For instance, Wang et al. [437] propose a so-called Causal Relationship Enhancement (CRE) submodule that utilize Structural Causal Model (SCM) to model casual mechanisms for subsequent integration into an LMM framework. On the other hand, Samarajeewa et al. [438] employ external causal knowledge to augment LLM to improve causal reasoning. The authors argue that LLMs, though have shown strong reasoning capacity, still need additional causal knowledge 

from structured sources to adequately infer causal relations. To this end, they employ RAG technique to recover Causal Graphs as external knowledge sources to extend LLM’s causal reasoning capabilities. 

Because of the tedious and time-consuming nature of the task of modeling causal mechanisms with the aforementioned graphical methods, some new approaches have been devised to leverage LLMs themselves to construct causal graphs models which, in turn, could be utilize to augment the LLMs. Since large language models themselves already possess extensive knowledge of real-world contexts, and patterns of behavior, including causal relationships between different variables [439], a large number of recent works (e.g., [407], [440], [441]) have proposed to leverage this knowledge to build causal graphs. In this line of work, the LLMs commonly serve as a source of prior knowledge about causality – i.e., to establish initial variables and dependencies [442]– or as a means to augment already known causal relationships by suggesting additional causal variables [443]. Typically, the LLM helps by describing the general structure of the graph in the form of variables (i.e., nodes) and their causal relationships (i.e., edges). With this method, there is also the possibility to interact with the LLM and exploit its reasoning abilities to refine the skeletal graph through prompting [404], [409]. 


Figure 14. Unlike AI systems, humans naturally have an intuitive understanding of cause-and-effect relationships, including a rough knowledge about how physical properties of materials and systems affect their behavior. The player can roughly estimate the amount and direction of force needed to get the ball to the right location. Similarly, the goalkeeper has a rough idea about the ball’s direction and speed based on the striker’s movement and pose before the kick. 

### _5.2.3 Physics-informed world models_ 

It has been hypothesized that humans’ ability to infer and reason about causal events relies on their world model (see, for example [444], [445], [446]). This world model, or metal model [447], encode causal abstractions of concepts, phenomena and objects in the world in a way that maintains a definite, albeit fuzzy, structure and rules governing behavior.. Based on these abstractions, humans have rough, implicit knowledge about the world in the form of intuitive physics [448]– i.e., basic properties of various entities and how these properties influence behavior. This allows humans to make unconscious but quick judgments about the physical interactions in the environment, for example, they can make fairly precise judgements about how objects move, fall, or collide (Figure 14). 

19 

Table 2 

A comparison of the strength of causality provided by the different classes of approaches. Note: In this table, w.r.t. means with respect to; Assoc. refers to the association level of causality; Interv. is the intervention level; and Count. is the counterfactual level. 

||**Capabili**<br>|**ty w.r.t. le**<br>|**vels of causality**<br>|**General comparison**<br>||
|---|---|---|---|---|---|
|**Class of approach**<br>Deep learning<br>(e.g., [420], [421])|**Assoc.**<br>Yes|**Interv.**<br>No|**Coun.**<br>No|**Strengths**<br>Does not require prior domain<br>knowledge; easy to scale; simple|**Weaknesses**<br>Can only establish correlations,<br>requires specific datasets for causality.<br>Prone to serious errors and catastrophic<br>failures.|
|Knowledge graphs<br>(e.g., [331], [350])|Yes|Partial|No|Can model complex relationships,<br>can readily be integrated into deep<br>learning frameworks|Not all data types are supported, modeling<br>casual relationships can be laborious and<br>time-consuming; difficult to scale.|
|SCM<br>(e.g., [432], [433])|Yes|Yes|Yes|Can model causal dependencies in<br>a comprehensive way; can be used<br>for interventions and counterfactual<br>reasoning|Difficult to implement, requires complete<br>knowledge about all factors, extremely<br>difficult to scale.|
|Physics models<br>(e.g.„ [449], [450])|Yes|Yes|Yes|Extremely scalable, models can<br>leverage existing world models,<br>can be used for interventions and<br>counterfactual reasoning|Require enormous computational resources,<br>requires knowledge of factors and their<br>relationships.|


In line with this idea, many recent works [109], [446], [451] leverage virtual worlds based on intuitive physics engines [449], [450], [452] to ground LLMs’ knowledge in causal properties and behavior of the real world. These models employ formal, mathematical models designed on the basis of prior knowledge to represent physical laws about the world. As a result, they simulate causal relationships and effects of real-world phenomena such as aerodynamics, gravity, force, and lighting, and heating. LLMbased AI agents that interact in such worlds in the process of training learn generalizable causal laws and behavior (e.g., flying, falling, burning, deformation, floating on water and breaking into pieces, etc.). Using knowledge from areas such as psychology and anthropology, it is also possible to model human behavior as well as social interactions [453], [454]. This allows “common sense” reasoning about observations and interactions. The inherent relations allow agents to easily handle questions about counterfactual. Agents themselves can be intrinsically designed as embodied virtual models capable of seamlessly interacting with the simulated causal world. Such agent models typically incorporate external frameworks or submodules that utilize accurate mathematical relations to model physical laws that describe the agents’ own properties and behavior. This way, embodied agents such as robots can predict the impact of their own actions as well as various physical influences on themselves. Causal modeling approaches that utilize virtual models have a number of strengths. They allow to simplify the complex process of obtaining large corpora of real data for training. Importantly, the underlying mathematical relations about physical interactions are invariably grounded in rigorous Newtonian physics, thermodynamics, or – depending on the level of realism required –particle physics and quantum mechanics. Therefore, the causal knowledge encoded in this class of models is precise and is often without any ambiguity, allowing exact results of interactions to be defined. Because of this representational power and precision, causal models based on physics engines can handle complex phenomena with consistency and accuracy far beyond human intuitive understanding. Despite these advantages, virtual models impose a number of limitations 

on the range and complexity of skills that can be learned. 

One of the main difficulties with this line of work is that highly detailed, large-scale simulations often require significant processing power. It is also enormously challenging to model such detailed, highly precise physical relations. However, the performance of the resulting AI systems is limited by the quality and completeness of the models used. Simulations may fail to accurately account for fuzzy concepts or factors unknown to the human developers. For example, simulations about human interactions may not accurately account for cultural, social and emotional factors. To overcome some of these challenges, approaches to incorporate deeply learned knowledge have been proposed. These include learning intuitive physics from data using special deep learning techniques [455], [456] or learning interaction policies using reinforcement learning with human feedback [457], [458], [459]. Another common limitation is that the interactions modeled by these techniques are rigid and operate strictly according to the physical parameters and rules encoded. To mitigate this drawback, some works [460], [461] have proposed to leverage data-driven optimization techniques to induce a degree of variability and randomness in physics-based models. 

## **6 MEMORY** 

### **6.1 Basic concept of memory in biological and AI systems** 

Memory mechanism differs fundamentally from the other cognitive processes covered in Sections 2 through 4– embodiment, grounding and causality –in the sense that it primarily serves as a means to preserve, consolidate, and subsequently make available the important knowledge acquired through these other processes. The memory mechanism does not lead to the generation of fundamentally new knowledge about the world, but mostly restructures the knowledge that has already been obtained. Thus, the main role of the memory mechanism in AGI is to reconstruct and organize the already acquired knowledge for high-level cognitive tasks and for storage for future reuse. When new knowledge emerges in the process, it is often as a result 

20 

of this reorganization process [462]. Memory facilitates continual [463], [464] or lifelong learning [465], an important feature of biological intelligence [466]. Memory can also serve as a means to incorporate prior knowledge into the AI system [467], [468]. Living organisms of the same species often jointly occupy a given ecological niche and constantly interact with one another, mostly in a cooperative way. For this reason, an important aspect of their intelligence depends on the ability to learn and maintain knowledge about shared behavioral characteristics that govern their interactions. Humans, in particular, commonly rely on shared structured knowledge in the form of norms, rules, belief systems and customs that allow them to interact seamlessly in social settings [1]. In addition to memorized information, humans and other higher living organisms have in-built prior knowledge or innate knowledge (see [469], [470]) that is encoded in genes and transmitted from parents to offsprings. To realize a similar function, AI approaches typically incorporate structured knowledge related to specific tasks in the form of knowledge graphs (e.g., in [471], [472]) or ontologies (e.g., [473], [474]) to augment learned knowledge stored in memory. They comprise not only facts and properties of specific concepts or objects about the world, but also relationships and general rules about the world. Together with the learned knowledge, allow effective and meaningful inferences about newly encountered situations. 

Besides storing and retrieving information, the memory mechanism serves as a means to bypass costly computations by reusing already computed cognitive variables and solutions [475], [476]. For instance, when humans first learn a new task such as driving, it takes constant attention and conscious effort to perform it. However, after ingraining the requisite skill in memory through constant practice, the learned tasks can be performed effortlessly without much attention. The phenomenon is well-grounded and supported by evidence from psychology. This saves scarce cognitive resources for new skills and conserves energy. Skills for mentally-engaging cognitive tasks in domains such as mathematics and complex games that require analytical reasoning particularly benefit from this phenomenon (for details about this see [475], [476]). Memory has also been shown to play a key role in metacognitive tasks, where existing knowledge about a domain facilitates learning new skills [477], [478], [479]. In addition, phenomena like imagination and mental imagery also illustrate the reuse of previous computations to facilitate efficiency [475]. 

### **6.2 General approaches to realizing memory in LLMs** 

The main techniques for implementing memory in LLMs are: 

- Parameters in deep neural networks 

knowledge by modifying these learned parameters instead of requiring information to be stored in independent, explicit memory. This often alters the model parameters and invariably leads to the loss of important information, a phenomenon commonly known as catastrophic forgetting [480]. A common workaround is to freeze some model parameters during the finetuning process to ensure that only knowledge that needs to be modified is affected [481], [482]. More recent techniques include elastic weight consolidation (EWC) [483], unsupervised replay [484] and adversarial neural pruning [485]. Using knowledge editing techniques [486], [487], [488], it is also possible to directly modified the learned knowledge instead retraining the model by the finetuning approach. 

### _6.2.2 Attention mechanism_ 

Another way to obtain memory in LLMs, or in neural networks in general, implementations is to utilize attention mechanism to temporarily hold and process information from past input sequence. While most modern LLMs are based on transformers, earlier language models employed various variants of recurrent architectures, including recurrent neural networks (RNNs) [489], [490], long shortterm memory (LSTM) [491], [492], gated recurrent units (GRUs) [493] that explicitly capture and retained fragments of previous inputs through hidden states using attention mechanism. In essence, the attention mechanism in this case provides short-term memory that allows the model to “remember” recent sequences or, more technically, to maintain context within the given sequence. However, the memory capacity in this case is very limited. Some works (e.g., [494]) employ the context window of the LLMs as memory, where information contained in prompts leveraged as state, task or goal description. This information is treated as working memory. The information in the context window can also be in the form of high-level concepts in natural language. These may be object or environment properties, task goals, desirable skills or attributes of the agent itself. Owing to the restricted memory capacity of the LLM context window, the volume of information that can be handled by this type of memory mechanism is very small. Moreover, recent work (e.g., [495], [496], [497]) has shown that models often exhibit bias for information at the beginning and end of the context window, prioritizing these portions while ignoring the middle. Consequently, very long contexts may result in a situation where a large portion of information (outside the two extremities are not memorized, culminating in the so-called Lost in the middle problem [497]. Because of these limitations, explicit memory has been proposed as a viable workaround that allows practically unlimited memory capacity for large-scale knowledge storage for generalist agents. 

- Attention mechanism 

- Explicit memory 

- Adequate diversity and variability 

- External memory (e.g., through RAG) 

### _6.2.1 Memory as model parameters_ 

Classical deep learning approaches store task-relevant knowledge as model parameters. Techniques such as finetuning and in-context learning seek to incorporate new 

### _6.2.3 Explicit memory_ 

To address the shortcomings of aforementioned memory techniques, approaches have been devised to allow selective storage of persistent, task-relevant information in computer memory for reuse [494], [498], [499], [500]. In particular, domain-specific knowledge can be stored explicitly in memory as prior knowledge to augment the extensive generic knowledge learned by the LLM. Learned knowledge in 

21 

the form of agent experiences (i.e., past decisions, actions or attempted actions and feedback from the environment) may also be stored explicitly in memory [501], [502], [503], [504]. The essence of this memory system is to sample and accumulate useful experiences over time in the process of interaction with the environment. Relational databases [494], [505], [506], [507] are one of the most popular type of storage for traditional information-intensive tasks. The stored information can then readily be retrieved using sequential query language (SQL) queries. This approach also allows information to be readily saved on external database servers and then retrieved as needed. Since the data format of traditional relational databases is often not designed to be readily usable by LLMs, a common workaround is to utilize structured databases [508], [509] for knowledge storage. Vector databases [510], [511], [512], [513], in particular, are very useful for this purpose. This type of memory system can store specific facts, concept definitions and entity relationships in the form of knowledge graphs, which the LLM can query to aid inference. Memory mechanism based on vector databases allows not only for quick retrieval, but also permits sophisticated and fine-grained manipulations to be carried out at the feature level (i.e., feature vector space). Moreover, this representation method makes it easy to use learned operations acquired in the training phase instead of relying on predefined analytical routines to manipulate the stored information. 

### _6.2.4 External memory through RAG_ 

With regard to generalist capabilities, one of the key advantages humans have over other animals is the ability to use external knowledge resources and tools to augment or extend their competences (e.,g., by reading manuals, books, or by browsing the internet for the necessary information for a given task). This alleviates the need for storing all needed knowledge internally. Motivated by this prospect, recent works have sought to enable LLMs to access and utilize external resources, thus, extending the range of tasks they can perform. This also helps to overcome inherent limitations associated with insufficient memory and processing power. For example, using retrieval-augmented generation methods [364], [514], [515], [516], models can also query external knowledgebases to retrieve additional information when the they do not find the required knowledge locally. This information from external sources can be processed and utilized straightaway or can be stored in local memory for later use. Large volumes of knowledge can be stored for long time spans since the volume of information that can be stored does not depend on the agent’s memory capacity. There is also the ability to exploit rich and diverse knowledge resources already available (e.g., web portals, wikis, etc.). Besides shortening development time and simplifying the development process, the ability to exploit readilyavailable external knowledge also offers an economically cheaper way to realize advanced capabilities. The main drawback of this approach is that the external information may not be guaranteed to work correctly as a result of unknown errors, including the presence of unknown errors, inconsistencies or incomplete information. There can also be a complete loss of access to the external information for various reasons, including a change in access privileges, loss 

of storage resource or the information itself. The external information may also be more exposed to other users and malicious actors, thereby endangering security. 

### **6.3 Memory types and their characteristics, role and implementation in LLMs** 

Three types of memory systems are commonly identified: sensory memory (SM); working memory (WM), also referred to as short-term memory (STM); and long-term memory (LTM). We discuss the general characteristics, main functions, role and methods of implementation of these various memory types in LLMs. A generalized memory structure of a typical cognitive system is shown in Figure 15. The main functions and approaches for implemention of each of these forms of memory are summariszed in Table 3. 

### _6.3.1 Sensory memory_ 

Sensory memory mechanism is the initial stage in the information processing pipeline and it is primarily associated with registering sensations. The role of sensory memory is to record perceptual inputs from various sensors and input systems (e.g., text, joystick and other control inputs) of the agent. Additionally, by focusing on more salient information while ignoring noisy signals, sensory memory serves as a filter for the vast amount of continuous sensory information from the environment. In terms of storage duration, this type of memory preserves information for the shortest amount of time. It retains information only briefly for sensory systems to access. That is, acting as a buffer, it makes sensations persistent enough to overcome the inherent inertia associated with sensory processing systems. In biological cognitive systems, sensory memory is automatic and not under voluntary control. Similarly, sensory memory systems in artificial intelligence systems can be implemented as a form of latching systems that buffers input signals [517], [518]. This function– i.e., holding sensory inputs for finite amount of time – allows the cognitive system to produce continuous perception of the environment. This “perceptual continuity” (creates a persistent experience of reality, which) is useful for understanding and interacting with the world in a coherent manner. Memory buffer can be realized natively by leveraging latches and buffered data mechanisms typically employed in microprocessor systems dedicated to real-time signal processing [518], [519]. Peripheral interfaces for such microprocessor systems may utilize a kind of read buffer mechanism in order to avoid read misses as a result of delayed access. This buffered peripherals usually employs a dedicated register or set of registers that holds the last data received from the external peripheral [520], [521]. This data is typically erased only when new data is written to the buffer or when an explicit deletion is requested by software. Write-back buffer can also be used at the destination to allow time for the processing elements to access sensory data. Such a buffer mechanism helps to ensure continuous access and availability of the sensory information during processing. 

Bio-inspired techniques that imitate the sensory memory mechanism of biological neural systems have also been proposed (e.g., in [522], [523]). These approaches are commonly based on advanced material technologies—technologies 

22 

that produce artificial systems that exhibit useful properties of biological sensory systems. 

Even though most state-of-the-art large language models do not explicitly incorporate sensory memory, the working principle as described in the preceding paragraph is naturally implemented in cyber-physical systems that utilize sensors for perception. Thus, with this loose definition of sensory memory mechanism, one can assert that almost all embodied LLM systems that read sensory signals implement sensory mechanism of some sort. 

### _6.3.2 Working memory_ 

Working memory [506], [524], [525], [526], also known as short-term memory, retains relatively small amounts of information in an active, readily accessible state for relatively short durations during/for processing for immediate cognitive tasks, including perception, decision-making, reasoning, instruction following and executive functions (i.e., sensorimotor control). The biological concept of short-term memory was first described by NC Waugh and DA Norman in [527]. Baddeley [528] later introduced the concept of working memory, a model that conceptualizes short-term memory as a block of memory in which information needed for the execution of current tasks circulates. Thus, the content of short-term memory is retained until the target task is completed, after which the information is either forgotten or is saved to long-term memory. 

High-level contextual information about interactions is also maintained in working memory to facilitate more complex tasks such as abstract reasoning. For example, in reinforcement learning-based agents, real-time information relating to agent trials and feedback are commonly maintained in working memory to facilitate reasoning [529]. By momentarily holding recent inputs for immediate processing, the context window in LLMs can be regarded as serving analogous function as working memory. The LLM typically holds the most recent tokens in the context window, remembering only what was presented a few sentences away from the present. The content, similar to working memory, easily decays or overwritten by new input. Thus, it functions as the “memory” from which the model can retrieve and process recently inputted tokens before they are discarded or replaced by new inputs. The size of the context window determines the capacity of this memory. Indeed, many works precisely utilize the LLM context window as short-term memory mechanism [494], [504], [530]. In this regard, the information in the context window is leveraged as intermediate task, state or goal description. LTM content can also be utilized/retrieved by prompts to extent/enrich the information represented in the context window. Conversely, information in the context window can also provide additional knowledge to enrich long-term memory [531], [532]. 

### _6.3.3 Long-term memory_ 

Long-term memory preserves information for long time spans. The content of long-term memory is information selected from working memory that is deemed useful for longterm storage [533], [534], [535]. This ensures that the most relevant and important knowledge is available for reuse. In 

biological cognitive systems, long-term memory can hold information for the entire lifetime of the organism [536], [537], though over time the information may be subject to decay, distortion, or loss [538], [539]. The problems of information loss can be avoided in synthetic memory systems by incorporating explicit schemes that maintain information permanently [540], [541]. With effectively unlimited capacity, long-term memory is the ultimate reservoir of knowledge, accumulated experiences and skills that can be recalled and utilized when needed. There are two main types of longterm memory systems commonly implemented in LLMs: declarative and procedural memories [542]. 

**(a) Declarative memory** Declarative memory is also known as explicit memory in biological cognition as the content can be consciously interrogated and recalled [548], [549]. In the context of artificial intelligence, declarative memory involves knowledge about specific facts that can be explicitly represented and retrieved [550]. Declarative memory is further subdivided into semantic and episodic memories [551]. 

_Semantic memory_ Semantic memory maintains general knowledge that does not depend on specific contexts or agent’s “personal” or unique experiences. The knowledge encoded in semantic memory consists of facts, formulas, general rules and laws, definitions as well as words and symbols and their meanings. The semantic memory focuses on high-level, conceptual knowledge about the world and how these are expressed in terms of symbols (e.g., words), graphics and speech (audio). In addition to facts about the world, semantic memory allows general rules and abstract principles to be retained for later use. These rules are leveraged to manipulate new information in cognitive information processing. In this regard, they serve as a reasoning framework for interpreting the world as well as for acquiring and evaluating new knowledge. 

In large language models, semantic knowledge is naturally captured during training. In the course of training, multimodal language models learn to associate words, phrases, images, symbols and concepts based on the statistical patterns in the training data. This process allows the LLM to build a rich internal representation of general knowledge, which is maintained in long-term memory and recalled in the future to support cognitive tasks. By virtue of this knowledge, generic LLMs are impressive in reasoning tasks [70], [552], [553] and answering questions that require factual information [554], [555]. For instance, questions like "What is the largest city in California?" or "How many feet make one kilometer?" are easily handled by these models. They are also adept at mining general rules from data and applying them in new tasks (see [556], [557], [558]). This property of LLMs is the foundation of their impressive commonsense and analytical reasoning capabilities [74], [559]. Semantic memory can also be implemented in the form of prior knowledge encoded in structured forms such as knowledge graphs and causal graphical models can serve as long-term memory in LLMs. These structured knowledge submodules within LLMs can store facts, rules, concepts and relationships in a persistent manner, thus, allowing LLMs to retrieve useful information as needed. Works such as AriGraph [468], HippoRAG [543] and KG-Agen [560] specifically employ structured knowledge forms as long- 

23 

Table 3 

A summary of the main memory types and the common approaches for their realization. The asterisk (*) symbol Indicates long-term memory. 

|**Type**|**Main functions**|**Methods fo realization in LLMs**|**Rep. works**|
|---|---|---|---|
|Sensory<br>memory|Stores sensory information momentarily for the<br>cognitive system to access.<br>Servers as a buffer mechanism to allow cognitive<br>processing components to work at different speed<br>without information lost.|Buffered I/O systems; latching mechanisms for<br>sensory inputs; bio-inspired sensory memory<br>techniques .|[517], [522], [523]|
|Working<br>memory|Filters information (e.g., through attention mech-<br>anism) for long-term storage.<br>Holds active information temporally for cognitive<br>processing|Attention layers in deep learning networks;<br>LMM context window.|[494], [504], [530]|
|Semantic<br>memory*|Maintains and accumulates information about<br>general rules, facts, principles, relationships of<br>various entities and general knowledge about the<br>world.<br>Allows prior knowledge about the world to be<br>reused in tacking cognitive problems tasks.|Structured knowledge in graphs; embeddings in<br>deep layers of neural networks; vector databases;<br>external knowledge accessed using methods such<br>as retrieval-augmented generation; in-context<br>learning of semantics.<br>.|[468], [543], [544]|
|Episodic<br>memory*|Integrates multimodal information (spatial, audio,<br>auditory, visual, olfactory, etc.) to form a unified,<br>contextually-grounded representation that captures<br>“personal” experiences.<br>Allows agents to introspect and reflect on the past<br>in the context of current reality, and, thus, provides<br>a means to self-improve.|Explicit storage of specific events and experiences<br>with the associated temporal, spatial, social, etc.<br>contexts; in-context learning of significant events<br>by active prompting;|[545], [546]|
|Procedural<br>memory*|Stores information about the detailed steps involved<br>in performing various specific (often, sensorimotor)<br>activities.<br>Allows agents to perform complex activities without<br>cognitive computations. This automates tasks, boots<br>speed and saves cognitive resources for other funct-<br>ions.|Explicit, long-term storage of real-time information<br>obtained from interactions with the environment;<br>explicit encoding of task plans using neurosymbolic<br>methods; external knowledge about task- specific<br>action sequences (e.g., using knowledge graphs);<br>retrieval-augmented generation.|[295], [547].|


term memory. These specialized representation frameworks can particularly simulate the complex structure and interrelationships of various entities that is intended to be capture by information in semantic memory [468]. In this representation, where high-level concepts, their properties and relationships are explicitly connected. 

_Episodic memory_ Episodic memory maintains information about important events, experiences and associated contextual information [561] – that is, information about the times, locations, surrounding background or situational context, and nature of the events (e.g., the visual imagery, specific characteristics, including taste, touch, sound and other sensory signals that accompanied the event). This information is represented as time-ordered sequence of experiences. The information is not additive, that is, different events recorded are separate and the experiences are not generalized nor accumulated. Episodic memory mechanism in large language models can be realized in several ways, including by utilizing the attention mechanism of the underlying transformer architecture to capture episodic knowledge; transferring relevant episodic information from the LLM’s context window to long-term storage; through fine-tuning generic, pre-trained LLM frameworks on specific datasets that explicitly contain episodic knowledge which can be saved to long-term memory and recalled in the future. 

**(b) Procedural memory** Procedural memory deals with the acquisition, storage, and recall of knowledge about the logical steps needed to carry out complex activities. This commonly involves motor skills such as autonomous driving, cooking and robot manipulation. In the realm of large language models, procedural memory facilitates cognitive 

functions such as activity planning, instruction following, reasoning and execution of physical actions. This set of highlevel cognitive capabilities are a core part of LLMs’ emergent abilities. 

In biological cognitive systems, a major aspect of procedural memory involves subconscious processes [562] – processes occurring outside the agent’s awareness, e.g., priming [563] and classical conditioning [564], [565]. The task is to learn and store natural associations between stimuli and corresponding responses, thereby allowing appropriate responses to be invoked automatically in the right situations. This bypasses the need to perform complex cognitive computations required for reasoning, and, consequently, speeds up reaction times. The subconscious phenomena and how they interact with explicit representations such as facts are still poorly-understood. Consequently, implementations of such techniques are lacking in the AI arena. Procedural knowledge in large language models is commonly learned implicitly and stored in long-term memory. This is achieved by virtue of LLMs’ ability to learn sequences of actions, structures, and relationships in the training data. After the pre-training phase, LLMs can further be fine-tuned on taskspecific, sensorimotor datasets (e.g., [566] which usually include detailed step-by-step instructions on how to accomplish the target tasks. The fine-tuning process is aimed at internalizing (i.e., learning from scratch) or refining (i.e., align slightly different tasks) the model’s ability to generate and follow explicit execution plans necessary for solving the given problem. Despite the impressive performance of state-of-the-art models on procedural tasks, it is often more effective to encode specific skills explicitly with the 

24 


Figure 15. A simplified representation of the memory system showing information flow as well as the interaction various components and the cognitive system. 

help of neuro-symbolic techniques [294], [547], [567]. These symbolic methods are sometimes used to provide structured reasoning frameworks that can be utilized by implicitly learned procedural knowledge for solving specific sets of problems. 

## **7 GENERALIST AI (AGI) FRAMEWORK BASED ON THE PRINCIPLES OF EMBODIMENT, GROUNDING, CAUSALITY AND MEMORY** 

In this section we develop a conceptual framework for AGI that unifies the concepts covered in this work. Such a framework implements the essential computational mechanisms that support the realization of sophisticated, robust and general intelligence based on the principles discussed in Sections 2-5 of this paper. These seemingly isolated concepts surveyed in this paper– embodiment, grounding, causality and memory – are inherently interrelated and complementary in their functions with regard to their role in facilitating artificial general intelligence. Embodiment provides the general structure and requisite mechanisms for interfacing with the world. This allows AI systems to experience the world (through sensing systems) and influencing its state by performing desired actions in response to sensory inputs and goals. These embodied experiences serve as useful signals for grounding symbols. That is, rather than relying solely on abstract, linguistic associations of 

input words in training data, embodiment allows the agent to obtain meaningful sensorimotor experiences – through actual perception of and interactions with the world – that is used to ground abstract representations in the agent’s actual perception of and interactions. This grounded embodied experiences, in turn, allows the agent to observe and learn causal relationships directly from the physical world through interaction with and feedback from it. Additionally, memory mechanisms provide a means for encoding, storing and accessing grounded symbols, embodied experiences and causal relationships learned in the process of training the AI agent (see Figure 16). Moreover, memory serves as a means to incorporate already-known causal relationships and grounded symbols as prior knowledge. As shown in Figure 16, the causal knowledge and symbolic associations learned from agent observations and embodied interactions with the environment can then be augmented with the prior known causal relationships and grounded symbols encoded in memory in the form of structured knowledge, providing a more comprehensive knowledge for robust perception, reasoning and other cognitive tasks. These mechanisms, working together, form a robust framework that enables LLM agents to generalize knowledge better. 

Functional block diagram of a generalized AGI system based on the principles covered in this article. The conceptual model consists of (1) a core framework, embodiment, that provides the physical essence and necessary mecha- 

25 


Figure 16. Functional block diagram of a generalized AGI system based on the principles covered in this article. The conceptual model consists of (1) a core framework, embodiment, that provides the physical essence and necessary mechanisms for interfacing and interacting with the world; (2) memory, made up of different memory subsystems – sensory, working and long-term memory, whose role, among others, is to allow both learned and prior knowledge to be preserved and accumulated over time; (3) symbol grounding subsystem, which provides a way to connect abstract representations in the underlying LLM model to actual entities in the world; and (4) causal learning mechanisms that learn the properties and physical laws associated with entities of the real world. Note that the symbol grounding and causal learning mechanisms combine both prior knowledge encoded in memory and learned knowledge resulting from cognitive information processing to achieve correct results. 

nisms for interfacing and interacting with the world; (2) memory, made up of different memory subsystems – sensory, working and long-term memory, whose role, among others, is to allow both learned and prior knowledge to be preserved and accumulated over time; (3) symbol grounding subsystem, which provides a way to connect abstract representations in the underlying LLM model to actual entities in the world; and (4) causal learning mechanisms that learn the properties and physical laws associated with entities of the real world. Note that the symbol grounding and causal learning mechanisms combine both prior knowledge encoded in memory and learned knowledge resulting from cognitive information processing to achieve correct results. 

## **8 DISCUSSIONS** 

Large language models have surpassed traditional deep learning approaches in many tasks. They have achieved impressive results in many nontrivial AI problems, including reasoning, planning, multimedia (i.e., text, image, video, speech, etc.) generation, open-world navigation, coding, natural language understanding, and open-domain question answering. Because of these capabilities, commercial 

firms, including tech giants such as Google, OpenAI, Meta, Nvidia, Amazon, Apple and Microsoft have invested huge sums of money and human capital in developing generic as well as domains-specific generalist AI systems. State-ofthe-art generalist AI systems are also increasingly being incorporated in commercial products such as search engines, chatbots, generic software, portable navigation equipment, smart phones, autonomous vehicles, and extended reality systems. The recent success of multimodal language models has drastically raised expectations about the possibility of machines achieving universal intelligence in the foreseeable future. In fact, some researchers are of the view that with state-of-the-art LLMs artificial general intelligence is already attainable [10], [40], [568]. While multimodal LLMs are showing enormous promise, these claims, at the moment, are premature and exaggerated. A possible route to attaining artificial general intelligence is to continue to scale up large, universal machine learning algorithms and training them with yet larger and larger quantities of data so as to handle complex problems in a wide range of domains. Given the impressive results already achieved by state-ofthe art neural network frameworks, especially multimodal large language models, such an approach seems possible, at 

26 

least in principle. The large model size and the enormous volume and diversity of training data allows these models to capture general yet intricate concepts and semantically rich patterns and associations that are valid across multiple problem domains and application settings. However, experience shows that such an approach has serious limitations: limited data in many specialized domains, neural networks tend to learn mere data correlations and fail to distinguish between superficial associations and causal relationships. Moreover, as demonstrated by state-of-the-art large language models (see, for example [91], [92], [569], [570]), such intelligent systems will be very superficial with regard to the sophistication of its knowledge and ability to apply learning in a flexible, context-dependent manner in unseen situations. Thus, simply scaling up LLMs and training on similarly larger datasets may not be enough to achieve human-level intelligence. 

Large language models are still unable to match the robustness, flexibility, efficiency and the overall generalist capabilities of the biological cognitive systems. In contrast to large language models and AI systems, human intelligence is extremely rich and multifaceted. Humans are able to make accurate judgments about the properties and behavior of objects without direct measurements. To mitigate this shortcoming, many works aim to achieve general intelligence by engineering specialized properties that make biological intelligence so powerful, robust, data-efficient, versatile and adaptive. In particular, the concepts discussed here – embodiment, grounding, causality and memory –would be extremely useful in achieving significant milestones. While the principles are promising, there is still significant room to improve the approaches used to implement each of these concepts. It is also important to emphasize that each of the concepts only solves specific cognitive problems related to the realization of general, human-level intelligence. To facilitate general intelligence, however, it will be much more beneficial to incorporate all these principles and approaches in a more integrated manner in a single cognitive framework. 

Thus, while the concepts of embodiment, symbol grounding, causality and memory have been long recognized as the foundation for artificial general intelligence, and have been widely employed to advance the state-of-theart in LMMs, continued progress toward AGI will require fundamentally new paradigms for designing LLMs that implement all these principles in a unified fashion. Such design philosophies will involve integrating deep learning models with neuro-symbolic techniques that leverage prior information to encode constrains and physical properties of the real world. This approach requires these core concepts to be treated as a unified set of interrelated and complementary primitives that jointly model intelligent agents and their environment. The cognitive process is then reduced to interfacing the various subcomponents and processing and exchanging information between them. The processed cognitive information is then leveraged to understand specific event of interest, interact with the world, explain observations and account for counterfactuals. In this context, it will be extremely important to handle situations that are absent or are sparsely represented in training datasets. 

Another major challenge with AGI research is that 

although the goal of achieving human-level, general intelligence seems well-defined, evaluating and ascertaining when this is achieved is a challenging problem. In particular, while comparisons of the intelligence of AI systems and humans are usually based on performance on specific sets of tasks, there exist fundamental differences in how human and machine intelligence are designed and function. These differences are reflected in their respective strengths and weaknesses. For instance, biological intelligence developed through evolution out of the necessity of survival of the agent itself (or its offspring) in dynamic and hostile environments. Human intelligence is fundamentally fuzzy and broad in scope, adaptable, and includes subjective aspects such as emotional, social, creative reasoning capabilities. In contrast, machine intelligence is typically designed and optimized to directly solve specific set of problems – no matter how general these problems may be. Owing to these important differences relating to their nature, design objectives and specific abilities, comparisons may yield misleading results. Consequently, even when an AI agent achieves general performance on complex tasks comparable to humans, it will still be difficult to characterize it as such. Moreover, Intelligence as an abstract concept is a continuous metric that encompasses multiple dimensions and measuring it in objective terms is not feasible. Consequently, it is not practical to even assess how close state-of-the art LLMs are to achieving AGI. 

Nevertheless, as the capabilities of intelligent agents continue to improve, at the point where one is no longer able to distinguish between the decisions and actions of AI agents and those of humans in a wide variety of complex (virtual or real-world) settings, one can safely conclude that we have attained human-level, general intelligence, even if in a limited sense. Currently, state-of-the-art LLM agents increasingly perform complex tasks in complex human-centric environments, and can assume leadership roles and provide expert guidance in specific open-world settings, where trust as well as professional, social, emotional relationships may develop between agents and humans as a result of their interactions. These agents are increasingly exhibiting fundamental human characteristics and capabilities, including the ability to understand the emotional state of humans; empathize; respond to unexpected, random events; help and request help; collaborate with humans and other agents to jointly solve problems; and engage in meaningful dialog with humans. At this stage, we are not very far from some form of what can be described as general intelligence. 

## **9 CONCLUSION** 

In this work we present what we consider the core enablers of robust and sophisticated cognitive capabilities that AI models based on large language models can leverage to achieve artificial general intelligence – embodiment, symbol grounding, causality and memory. While these concepts are by no means the only principles necessary for the realization of general intelligence, they form the fundamental building blocks which are essential for any AI system to achieve general intelligence in dealing with the real world. Integrating these techniques in LLMs an intrinsic way will lead to a fundamentally new set of important characteristics 

27 

that natively support AGI. The core building blocks and techniques for realizing these principles are already available, at least in rudimentary form. As our understanding of these principles and the techniques for implementing them continue to improve, the prospect of achieving human-level general intelligence in the foreseeable future is within reach. 

## **ACKNOWLEDGMENTS** 

The authors would like to thank... 

## **REFERENCES** 

- [1] S. S. Adams and S. Burbeck, “Beyond the octopus: From general intelligence toward a human-like mind,” in _Theoretical foundations of artificial general intelligence_ . Springer, 2012, pp. 49–65. 

- [2] D. P. Kingma and M. Welling, “Auto-encoding variational bayes,” _arXiv preprint arXiv:1312.6114_ , 2013. 

- [3] P. Isola, J.-Y. Zhu, T. Zhou, and A. A. Efros, “Image-to-image translation with conditional adversarial networks,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2017, pp. 1125–1134. 

- [4] S. Bond-Taylor, A. Leach, Y. Long, and C. G. Willcocks, “Deep generative modelling: A comparative review of vaes, gans, normalizing flows, energy-based and autoregressive models,” _IEEE transactions on pattern analysis and machine intelligence_ , vol. 44, no. 11, pp. 7327–7347, 2021. 

- [5] S. Minaee, T. Mikolov, N. Nikzad, M. Chenaghlu, R. Socher, X. Amatriain, and J. Gao, “Large language models: A survey,” _arXiv preprint arXiv:2402.06196_ , 2024. 

- [6] F.-A. Croitoru, V. Hondru, R. T. Ionescu, and M. Shah, “Diffusion models in vision: A survey,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 45, no. 9, pp. 10 850–10 869, 2023. 

- [7] Y. Du, Z. Liu, J. Li, and W. X. Zhao, “A survey of vision-language pre-trained models,” _arXiv preprint arXiv:2202.10936_ , 2022. 

- [8] Y. Ma, Z. Song, Y. Zhuang, J. Hao, and I. King, “A survey on vision-language-action models for embodied ai,” _arXiv preprint arXiv:2405.14093_ , 2024. 

- [9] S. Bubeck, V. Chandrasekaran, R. Eldan, J. Gehrke, E. Horvitz, E. Kamar, P. Lee, Y. T. Lee, Y. Li, S. Lundberg _et al._ , “Sparks of artificial general intelligence: Early experiments with gpt-4,” _arXiv preprint arXiv:2303.12712_ , 2023. 

- [10] B. A. y Arcas, “Artificial general intelligence is already here,” 2023. 

- [11] R. Firoozi, J. Tucker, S. Tian, A. Majumdar, J. Sun, W. Liu, Y. Zhu, S. Song, A. Kapoor, K. Hausman _et al._ , “Foundation models in robotics: Applications, challenges, and the future,” _The International Journal of Robotics Research_ , p. 02783649241281508, 2023. 

- [12] T. Yu, C. Jiang, C. Lou, S. Huang, X. Wang, W. Liu, J. Cai, Y. Li, Y. Li, K. Tu _et al._ , “Seqgpt: An out-of-the-box large language model for open domain sequence understanding,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 38, no. 17, 2024, pp. 19 458–19 467. 

- [13] S. Mohanty, N. Arabzadeh, J. Kiseleva, A. Zholus, M. Teruel, A. Awadallah, Y. Sun, K. Srinet, and A. Szlam, “Transforming human-centered ai collaboration: Redefining embodied agents capabilities through interactive grounded language instructions,” _arXiv preprint arXiv:2305.10783_ , 2023. 

- [14] E. S. Spelke, “What makes us smart? core knowledge and natural language,” 2003. 

- [15] A. Prestrude, “Sensory capacities of the chimpanzee: A review.” _Psychological bulletin_ , vol. 74, no. 1, p. 47, 1970. 

- [16] R. Doble, “Animal senses compared to the human sense of time,” 2014. 

- [17] G. Mendoza and H. Merchant, “Motor system evolution and the emergence of high cognitive functions,” _Progress in neurobiology_ , vol. 122, pp. 73–93, 2014. 

- [18] D. J. Felleman and D. C. Van Essen, “Distributed hierarchical processing in the primate cerebral cortex.” _Cerebral cortex (New York, NY: 1991)_ , vol. 1, no. 1, pp. 1–47, 1991. 

- [19] E. Thelen, “Learning to walk: Ecological demands and phylogenetic constraints.” _Advances in infancy research_ , 1984. 

- [20] H. Ackermann, S. R. Hage, and W. Ziegler, “Brain mechanisms of acoustic communication in humans and nonhuman primates: an evolutionary perspective,” _Behavioral and Brain Sciences_ , vol. 37, no. 6, pp. 529–546, 2014. 

- [21] M. A. Novack and S. Waxman, “Becoming human: human infants link language and cognition, but what about the other great apes?” _Philosophical Transactions of the Royal Society B_ , vol. 375, no. 1789, p. 20180408, 2020. 

- [22] N. J. Bourguignon, “The emergence of language in the human mind and brain- insights from the neurobiology of language, thought and action.” _Psychological Review_ , vol. 130, no. 6, p. 1544, 2023. 

- [23] E. L. Grigorenko, “The never-ending innovativeness of homo sapiens,” in _Creativity, Innovation, and Change Across Cultures_ . Springer, 2023, pp. 3–27. 

- [24] A. Clark, “Magic words: How language augments human computation,” in _Language and meaning in cognitive science_ . Routledge, 2012, pp. 21–39. 

- [25] B. H. Schmitt, Y. Pan, and N. T. Tavassoli, “Language and consumer memory: The impact of linguistic differences between chinese and english,” _Journal of consumer research_ , vol. 21, no. 3, pp. 419–431, 1994. 

- [26] Y. Tajima and N. Duffield, “Linguistic versus cultural relativity: On japanese-chinese differences in picture description and recall,” _Cognitive Linguistics_ , vol. 23, no. 4, pp. 675–709, 2012. 

- [27] J. C. Trueswell and A. Papafragou, “Perceiving and remembering events cross-linguistically: Evidence from dual-task paradigms,” _Journal of Memory and Language_ , vol. 63, no. 1, pp. 64–82, 2010. 

- [28] M. I. Feist and P. C. Férez, “Remembering how: Language, memory, and the salience of manner,” _Journal of Cognitive Science_ , vol. 14, no. 4, pp. 379–398, 2013. 

- [29] A. Majid, M. Bowerman, S. Kita, D. B. Haun, and S. C. Levinson, “Can language restructure cognition? the case for space,” _Trends in cognitive sciences_ , vol. 8, no. 3, pp. 108–114, 2004. 

- [30] A. Duranti, “Linguistic anthropology: Language as a non-neutral medium,” _The Cambridge handbook of sociolinguistics_ , pp. 28–46, 2011. 

- [31] G. Lupyan, “The centrality of language in human cognition,” _Language Learning_ , vol. 66, no. 3, pp. 516–553, 2016. 

- [32] G. Thierry, P. Athanasopoulos, A. Wiggett, B. Dering, and J.-R. Kuipers, “Unconscious effects of language-specific terminology on preattentive color perception,” _Proceedings of the National Academy of Sciences_ , vol. 106, no. 11, pp. 4567–4570, 2009. 

- [33] G. Lupyan and M. J. Spivey, “Perceptual processing is facilitated by ascribing meaning to novel stimuli,” _Current Biology_ , vol. 18, no. 10, pp. R410–R412, 2008. 

- [34] L. Meteyard, B. Bahrami, and G. Vigliocco, “Motion detection and motion verbs: Language affects low-level visual perception,” _Psychological Science_ , vol. 18, no. 11, pp. 1007–1013, 2007. 

- [35] G. Roth and U. Dicke, “Evolution of the brain and intelligence in primates,” _Progress in brain research_ , vol. 195, pp. 413–430, 2012. 

- [36] B. Goertzel, “Artificial general intelligence: concept, state of the art, and future prospects,” _Journal of Artificial General Intelligence_ , vol. 5, no. 1, p. 1, 2014. 

- [37] S. McLean, G. J. Read, J. Thompson, C. Baber, N. A. Stanton, and P. M. Salmon, “The risks associated with artificial general intelligence: A systematic review,” _Journal of Experimental & Theoretical Artificial Intelligence_ , vol. 35, no. 5, pp. 649–663, 2023. 

- [38] P. Wang and B. Goertzel, “Introduction: Aspects of artificial general intelligence,” in _Advances in Artificial General Intelligence: Concepts, Architectures and Algorithms_ . IOS Press, 2007, pp. 1–16. 

- [39] N. Fei, Z. Lu, Y. Gao, G. Yang, Y. Huo, J. Wen, H. Lu, R. Song, X. Gao, T. Xiang _et al._ , “Towards artificial general intelligence via a multimodal foundation model,” _Nature Communications_ , vol. 13, no. 1, p. 3094, 2022. 

- [40] D. Ili´c and G. E. Gignac, “Evidence of interrelated cognitivelike capabilities in large language models: Indications of artificial general intelligence or achievement?” _Intelligence_ , vol. 106, p. 101858, 2024. 

- [41] N.-M. Aliman and L. Kester, “Hybrid strategies towards safe selfaware superintelligent systems,” in _Artificial General Intelligence: 11th International Conference, AGI 2018, Prague, Czech Republic, August 22-25, 2018, Proceedings 11_ . Springer, 2018, pp. 1–11. 

- [42] G. Buttazzo, “Rise of artificial general intelligence: risks and opportunities,” _Frontiers in artificial intelligence_ , vol. 6, p. 1226990, 2023. 

28 

- [43] S. Adams, I. Arel, J. Bach, R. Coop, R. Furlan, B. Goertzel, J. S. Hall, A. Samsonovich, M. Scheutz, M. Schlesinger _et al._ , “Mapping the landscape of human-level artificial general intelligence,” _AI magazine_ , vol. 33, no. 1, pp. 25–42, 2012. 

- [44] T. R. Besold and U. Schmid, “Why generality is key to humanlevel artificial intelligence,” _Advances in Cognitive Systems_ , vol. 4, pp. 13–24, 2016. 

- [45] S. Pueyo, “Growth, degrowth, and the challenge of artificial superintelligence,” _Journal of Cleaner Production_ , vol. 197, pp. 1731–1736, 2018. 

- [46] N. Bostrom, “Ethical issues in advanced artificial intelligence,” _Machine Ethics and Robot Ethics_ , pp. 69–75, 2020. 

- [47] C. Pennachin and B. Goertzel, “Contemporary approaches to artificial general intelligence,” in _Artificial general intelligence_ . Springer, 2007, pp. 1–30. 

- [48] P. Voss, “Essentials of general intelligence: The direct path to artificial general intelligence,” _Artificial general intelligence_ , pp. 131–157, 2007. 

- [49] A. Braga and R. K. Logan, “The emperor of strong ai has no clothes: limits to artificial intelligence,” _Information_ , vol. 8, no. 4, p. 156, 2017. 

- [50] J. C. Flowers, “Strong and weak ai: Deweyan considerations.” in _AAAI spring symposium: Towards conscious AI systems_ , vol. 2287, no. 7, 2019. 

- [51] M. V. Butz, “Towards strong ai,” _KI-Künstliche Intelligenz_ , vol. 35, no. 1, pp. 91–101, 2021. 

- [52] D. C. Mograbi, S. Hall, B. Arantes, and J. Huntley, “The cognitive neuroscience of self-awareness: Current framework, clinical implications, and future research directions,” _Wiley Interdisciplinary Reviews: Cognitive Science_ , vol. 15, no. 2, p. e1670, 2024. 

- [53] J. Takeno, _Creation of a conscious robot: Mirror image cognition and self-awareness_ . CRC Press, 2012. 

- [54] C. Metz, “Ai is not sentient. why do people say it is?” _International New York Times_ , pp. NA–NA, 2022. 

- [55] A. Knight, “Refuting strong ai: Why consciousness cannot be algorithmic,” _arXiv preprint arXiv:1906.10177_ , 2019. 

- [56] M. Gibert and D. Martin, “In search of the moral status of ai: why sentience is a strong argument,” _AI & SOCIETY_ , vol. 37, no. 1, pp. 319–330, 2022. 

- [57] G. W. Ng and W. C. Leung, “Strong artificial intelligence and consciousness,” _Journal of Artificial Intelligence and Consciousness_ , vol. 7, no. 01, pp. 63–72, 2020. 

- [58] D. McDermott, “Artificial intelligence and consciousness,” _The Cambridge handbook of consciousness_ , pp. 117–150, 2007. 

- [59] D. Li, W. He, and Y. Guo, “Why ai still doesnt have consciousness?” _CAAI Transactions on Intelligence Technology_ , vol. 6, no. 2, pp. 175–179, 2021. 

- [60] R. Manna and R. Nath, “The problem of moral agency in artificial intelligence,” in _2021 IEEE Conference on Norbert Wiener in the 21st Century (21CW)_ . IEEE, 2021, pp. 1–4. 

- [61] A. D. Young and A. E. Monroe, “Autonomous morals: Inferences of mind predict acceptance of ai behavior in sacrificial moral dilemmas,” _Journal of Experimental Social Psychology_ , vol. 85, p. 103870, 2019. 

- [62] L. Floridi and M. Chiriatti, “Gpt-3: Its nature, scope, limits, and consequences,” _Minds and Machines_ , vol. 30, pp. 681–694, 2020. 

- [63] J. D. M.-W. C. Kenton and L. K. Toutanova, “Bert: Pre-training of deep bidirectional transformers for language understanding,” in _Proceedings of naacL-HLT_ , vol. 1. Minneapolis, Minnesota, 2019, p. 2. 

- [64] D. Driess, F. Xia, M. S. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu _et al._ , “Palm-e: An embodied multimodal language model,” _arXiv preprint arXiv:2303.03378_ , 2023. 

- [65] D. Zhu, J. Chen, X. Shen, X. Li, and M. Elhoseiny, “Minigpt-4: Enhancing vision-language understanding with advanced large language models,” _arXiv preprint arXiv:2304.10592_ , 2023. 

- [66] J.-B. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds _et al._ , “Flamingo: a visual language model for few-shot learning,” _Advances in neural information processing systems_ , vol. 35, pp. 23 716–23 736, 2022. 

- [67] H. Liu, C. Li, Q. Wu, and Y. J. Lee, “Visual instruction tuning,” _Advances in neural information processing systems_ , vol. 36, 2024. 

- [68] T. Gao, A. Fisch, and D. Chen, “Making pre-trained language models better few-shot learners,” _arXiv preprint arXiv:2012.15723_ , 2020. 

- [69] X. Liu, D. McDuff, G. Kovacs, I. Galatzer-Levy, J. Sunshine, J. Zhan, M.-Z. Poh, S. Liao, P. Di Achille, and S. Patel, “Large language models are few-shot health learners,” _arXiv preprint arXiv:2305.15525_ , 2023. 

- [70] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa, “Large language models are zero-shot reasoners,” _Advances in neural information processing systems_ , vol. 35, pp. 22 199–22 213, 2022. 

- [71] S. Yin, C. Fu, S. Zhao, K. Li, X. Sun, T. Xu, and E. Chen, “A survey on multimodal large language models,” _National Science Review_ , p. nwae403, 2024. 

- [72] S. Krause and F. Stolzenburg, “From data to commonsense reasoning: The use of large language models for explainable ai,” _arXiv preprint arXiv:2407.03778_ , 2024. 

- [73] J. Ahn, R. Verma, R. Lou, D. Liu, R. Zhang, and W. Yin, “Large language models for mathematical reasoning: Progresses and challenges,” _arXiv preprint arXiv:2402.00157_ , 2024. 

- [74] S. Imani, L. Du, and H. Shrivastava, “Mathprompter: Mathematical reasoning using large language models,” _arXiv preprint arXiv:2303.05398_ , 2023. 

- [75] Y. Tang, Z. Wang, A. Qu, Y. Yan, K. Hou, D. Zhuang, X. Guo, J. Zhao, Z. Zhao, and W. Ma, “Synergizing spatial optimization with large language models for open-domain urban itinerary planning,” _arXiv preprint arXiv:2402.07204_ , 2024. 

- [76] A. Kanhed, P. Bhagwat, K. Palande, N. Palav, S. Balpande, K. Deshpande, and U. Patil, “Destinai: Your personalized travel itinerary planner and chat catalyst using generative ai,” in _International Conference on Information and Communication Technology for Intelligent Systems_ . Springer, 2024, pp. 47–55. 

- [77] Y. Shen, K. Song, X. Tan, D. Li, W. Lu, and Y. Zhuang, “Hugginggpt: Solving ai tasks with chatgpt and its friends in hugging face,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [78] K. Cheng, Z. Li, X. Sun, B.-C. Min, A. S. Bedi, and A. Bera, “Efficienteqa: An efficient approach for open vocabulary embodied question answering,” _arXiv preprint arXiv:2410.20263_ , 2024. 

- [79] A. Majumdar, A. Ajay, X. Zhang, P. Putta, S. Yenamandra, M. Henaff, S. Silwal, P. Mcvay, O. Maksymets, S. Arnaud _et al._ , “Openeqa: Embodied question answering in the era of foundation models,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 16 488–16 498. 

- [80] A. Yuan, A. Coenen, E. Reif, and D. Ippolito, “Wordcraft: story writing with large language models,” in _Proceedings of the 27th International Conference on Intelligent User Interfaces_ , 2022, pp. 841– 852. 

- [81] G. Franceschelli and M. Musolesi, “On the creativity of large language models,” _AI & SOCIETY_ , pp. 1–11, 2024. 

- [82] Z. Shen, “Llm with tools: A survey,” _arXiv preprint arXiv:2409.18807_ , 2024. 

- [83] X. Li, “A review of prominent paradigms for llm-based agents: Tool use (including rag), planning, and feedback learning,” _arXiv preprint arXiv:2406.05804_ , 2024. 

- [84] C. Wang, W. Luo, Q. Chen, H. Mai, J. Guo, S. Dong, Z. Li, L. Ma, S. Gao _et al._ , “Tool-lmm: A large multi-modal model for tool agent learning,” _arXiv preprint arXiv:2401.10727_ , 2024. 

- [85] Y. Gao, Y. Xiong, X. Gao, K. Jia, J. Pan, Y. Bi, Y. Dai, J. Sun, and H. Wang, “Retrieval-augmented generation for large language models: A survey,” _arXiv preprint arXiv:2312.10997_ , 2023. 

- [86] D. Sanmartin, “Kg-rag: Bridging the gap between knowledge and creativity,” _arXiv preprint arXiv:2405.12035_ , 2024. 

- [87] H. Ye, T. Liu, A. Zhang, W. Hua, and W. Jia, “Cognitive mirage: A review of hallucinations in large language models,” _arXiv preprint arXiv:2309.06794_ , 2023. 

- [88] Y. Wolf, N. Wies, O. Avnery, Y. Levine, and A. Shashua, “Fundamental limitations of alignment in large language models,” _arXiv preprint arXiv:2304.11082_ , 2023. 

- [89] A. Tamkin, M. Brundage, J. Clark, and D. Ganguli, “Understanding the capabilities, limitations, and societal impact of large language models,” _arXiv preprint arXiv:2102.02503_ , 2021. 

- [90] M. U. Hadi, R. Qureshi, A. Shah, M. Irfan, A. Zafar, M. B. Shaikh, N. Akhtar, J. Wu, S. Mirjalili _et al._ , “A survey on large language models: Applications, challenges, limitations, and practical usage,” _Authorea Preprints_ , 2023. 

- [91] M. Zeˇcevi´c, M. Willig, D. S. Dhami, and K. Kersting, “Causal parrots: Large language models may talk causality but are not causal,” _arXiv preprint arXiv:2308.13067_ , 2023. 

- [92] E. M. Bender, T. Gebru, A. McMillan-Major, and S. Shmitchell, “On the dangers of stochastic parrots: Can language models be 

29 

- too big???” in _Proceedings of the 2021 ACM conference on fairness, accountability, and transparency_ , 2021, pp. 610–623. 

- [93] D. Howard, A. E. Eiben, D. F. Kennedy, J.-B. Mouret, P. Valencia, and D. Winkler, “Evolving embodied intelligence from materials to machines,” _Nature Machine Intelligence_ , vol. 1, no. 1, pp. 12–19, 2019. 

- [94] C. Durt, T. Froese, and T. Fuchs, “Against ai understanding and sentience: large language models, meaning, and the patterns of human language use,” 2023. 

- [95] S. Harnad, “The symbol grounding problem,” _Physica D: Nonlinear Phenomena_ , vol. 42, no. 1-3, pp. 335–346, 1990. 

- [96] M. K. Goddu and A. Gopnik, “The development of human causal learning and reasoning,” _Nature Reviews Psychology_ , pp. 1–21, 2024. 

- [97] T. Marwala, _Causality, correlation and artificial intelligence for rational decision making_ . World Scientific, 2015. 

- [98] K. Schweizer and H. Moosbrugger, “Attention and working memory as predictors of intelligence,” _Intelligence_ , vol. 32, no. 4, pp. 329–347, 2004. 

- [99] A. R. Conway, M. J. Kane, and R. W. Engle, “Working memory capacity and its relation to general intelligence,” _Trends in cognitive sciences_ , vol. 7, no. 12, pp. 547–552, 2003. 

- [100] J. Alexander and S. Smales, “Intelligence, learning and long-term memory,” _Personality and Individual Differences_ , vol. 23, no. 5, pp. 815–825, 1997. 

- [101] S. Torres-Martínez, “Embodied human language models vs. large language models, or why artificial intelligence cannot explain the modal be able to,” _Biosemiotics_ , pp. 1–25, 2024. 

- [102] M.-Y. Lin, O.-W. Lee, and C.-Y. Lu, “Embodied ai with large language models: A survey and new hri framework,” in _2024 International Conference on Advanced Robotics and Mechatronics (ICARM)_ . IEEE, 2024, pp. 978–983. 

- [103] D. J. Chalmers, “Could a large language model be conscious?” _arXiv preprint arXiv:2303.07103_ , 2023. 

- [104] G. Pezzulo, P. F. Verschure, C. Balkenius, and C. M. Pennartz, “The principles of goal-directed decision-making: from neural mechanisms to computation and robotics,” p. 20130470, 2014. 

- [105] E. Morsella, A. G. Velasquez, J. K. Yankulova, Y. Li, C. Y. Wong, and D. Lambert, “Motor cognition: The role of sentience in perception and action,” _Kinesiology Review_ , vol. 9, no. 3, pp. 261– 274, 2020. 

- [106] X. E. Barandiaran and L. S. Almendros, “Transforming agency. on the mode of existence of large language models,” _arXiv preprint arXiv:2407.10735_ , 2024. 

- [107] T. Carta, C. Romac, T. Wolf, S. Lamprier, O. Sigaud, and P.-Y. Oudeyer, “Grounding large language models in interactive environments with online reinforcement learning,” in _International Conference on Machine Learning_ . PMLR, 2023, pp. 3676–3713. 

- [108] M. Vicovaro, “Intuitive physics and cognitive algebra: A review,” _European Review of Applied Psychology_ , vol. 71, no. 5, p. 100610, 2021. 

- [109] J. Duan, S. Yu, H. L. Tan, H. Zhu, and C. Tan, “A survey of embodied ai: From simulators to research tasks,” _IEEE Transactions on Emerging Topics in Computational Intelligence_ , vol. 6, no. 2, pp. 230–244, 2022. 

- [110] S. Baron-Cohen, S. Wheelwright, A. Spong, V. Scahill, J. Lawson _et al._ , “Are intuitive physics and intuitive psychology independent? a test with children with asperger syndrome,” _Journal of developmental and learning disorders_ , vol. 5, no. 1, pp. 47–78, 2001. 

- [111] L. Ross, “The intuitive psychologist and his shortcomings: Distortions in the attribution process,” in _Advances in experimental social psychology_ . Academic Press, 1977, vol. 10, pp. 173–220. 

- [112] M. Verma, S. Bhambri, and S. Kambhampati, “Theory of mind abilities of large language models in human-robot interaction: An illusion?” in _Companion of the 2024 ACM/IEEE International Conference on Human-Robot Interaction_ , 2024, pp. 36–45. 

- [113] H. Li, Y. Q. Chong, S. Stepputtis, J. Campbell, D. Hughes, M. Lewis, and K. Sycara, “Theory of mind for multiagent collaboration via large language models,” _arXiv preprint arXiv:2310.10701_ , 2023. 

- [114] J. Richards and M. Wessel, “What you need is what you get: Theory of mind for an llm-based code understanding assistant,” _arXiv preprint arXiv:2408.04477_ , 2024. 

- [115] J. Toy, J. MacAdam, and P. Tabor, “Metacognition is all you need? using introspection in generative agents to improve goal-directed behavior,” _arXiv preprint arXiv:2401.10910_ , 2024. 

- [116] Y. Qu, T. Zhang, N. Garg, and A. Kumar, “Recursive introspection: Teaching llm agents how to self-improve,” in _ICML 2024 Workshop on Structured Probabilistic Inference {\&} Generative Modeling_ , 2024. 

- [117] W. Yao, S. Heinecke, J. C. Niebles, Z. Liu, Y. Feng, L. Xue, R. Murthy, Z. Chen, J. Zhang, D. Arpit _et al._ , “Retroformer: Retrospective large language agents with policy gradient optimization,” _arXiv preprint arXiv:2308.02151_ , 2023. 

- [118] D. Mougenot and H. Matheson, “Theoretical strategies for an embodied cognitive neuroscience: Mechanistic explanations of brain-body-environment systems,” _Cognitive neuroscience_ , vol. 15, no. 3-4, pp. 85–97, 2024. 

- [119] A. D. Wilson and S. Golonka, “Embodied cognition is not what you think it is,” _Frontiers in psychology_ , vol. 4, p. 58, 2013. 

- [120] P. E. Tibbetts, “Where does cognition occur: in ones head or in ones embodied/extended environment?” _The Quarterly Review of Biology_ , vol. 89, no. 4, pp. 359–368, 2014. 

- [121] L. Foglia and R. A. Wilson, “Embodied cognition,” _Wiley Interdisciplinary Reviews: Cognitive Science_ , vol. 4, no. 3, pp. 319–325, 2013. 

- [122] L. Hsu, “Entangled cognition: Exploring the links between mind, body, and environment in the era of aied,” _Psychology Research and Practice_ , vol. 3, no. 2, 2024. 

- [123] H. Thoenen, “Neurotrophins and neuronal plasticity,” _Science_ , vol. 270, no. 5236, pp. 593–598, 1995. 

- [124] P. R. Huttenlocher, _Neural plasticity: The effects of environment on the development of the cerebral cortex_ . Harvard University Press, 2009. 

- [125] R. Pfeifer and F. Iida, “Embodied artificial intelligence: Trends and challenges,” _Lecture notes in computer science_ , pp. 1–26, 2004. 

- [126] N. E. Sharkey and T. Ziemke, “Mechanistic versus phenomenal embodiment: Can robot embodiment lead to strong ai?” _Cognitive Systems Research_ , vol. 2, no. 4, pp. 251–262, 2001. 

- [127] M. Savva, A. Kadian, O. Maksymets, Y. Zhao, E. Wijmans, B. Jain, J. Straub, J. Liu, V. Koltun, J. Malik _et al._ , “Habitat: A platform for embodied ai research,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 9339–9347. 

- [128] M. G. Mecattaf, B. Slater, M. Teši´c, J. Prunty, K. Voudouris, and L. G. Cheke, “A little less conversation, a little more action, please: Investigating the physical common-sense of llms in a 3d embodied environment,” _arXiv preprint arXiv:2410.23242_ , 2024. 

- [129] Y. Liu, W. Chen, Y. Bai, X. Liang, G. Li, W. Gao, and L. Lin, “Aligning cyber space with physical world: A comprehensive survey on embodied ai,” _arXiv preprint arXiv:2407.06886_ , 2024. 

- [130] C. Zhang, J. Chen, J. Li, Y. Peng, and Z. Mao, “Large language models for human-robot interaction: A review,” _Biomimetic Intelligence and Robotics_ , p. 100131, 2023. 

- [131] K. M. Lee, Y. Jung, J. Kim, and S. R. Kim, “Are physically embodied social agents better than disembodied social agents?: The effects of physical embodiment, tactile interaction, and people’s loneliness in human–robot interaction,” _International journal of human-computer studies_ , vol. 64, no. 10, pp. 962–973, 2006. 

- [132] D. Swanepoel, “Does artificial intelligence have agency?” _The mind-technology problem: Investigating minds, selves and 21st century artefacts_ , pp. 83–104, 2021. 

- [133] P. J. Ågerfalk, “Artificial intelligence as digital agency,” _European Journal of Information Systems_ , vol. 29, no. 1, pp. 1–8, 2020. 

- [134] D. P. Williams, “Belief, values, bias, and agency: Development of and entanglement with artificial intelligence,” Ph.D. dissertation, Virginia Polytechnic Institute and State University, 2022. 

- [135] J. Lindblom, _Embodied social cognition_ . Springer, 2015, vol. 26. 

- [136] P. Voestermans and T. Verheggen, _Culture as embodiment: The social tuning of behavior_ . John Wiley & Sons, 2013. 

- [137] J. Gao, R. Pi, T. Han, H. Wu, L. Hong, L. Kong, X. Jiang, and Z. Li, “Coca: Regaining safety-awareness of multimodal large language models with constitutional calibration,” _arXiv preprint arXiv:2409.11365_ , 2024. 

- [138] U. Agarwal, K. Tanmay, A. Khandelwal, and M. Choudhury, “Ethical reasoning and moral value alignment of llms depend on the language we prompt them in,” _arXiv preprint arXiv:2404.18460_ , 2024. 

- [139] I. Ajzen and T. J. Madden, “Prediction of goal-directed behavior: Attitudes, intentions, and perceived behavioral control,” _Journal of experimental social psychology_ , vol. 22, no. 5, pp. 453–474, 1986. 

- [140] M. Frese and J. Sabini, “Goal directed behavior: The concept of action in psychology,” 2021. 

30 

- [141] H. Aarts and A. Dijksterhuis, “Habits as knowledge structures: automaticity in goal-directed behavior.” _Journal of personality and social psychology_ , vol. 78, no. 1, p. 53, 2000. 

- [142] J. Duncan, H. Emslie, P. Williams, R. Johnson, and C. Freer, “Intelligence and the frontal lobe: The organization of goaldirected behavior,” _Cognitive psychology_ , vol. 30, no. 3, pp. 257– 303, 1996. 

- [143] M. R. Morris, J. Sohl-Dickstein, N. Fiedel, T. Warkentin, A. Dafoe, A. Faust, C. Farabet, and S. Legg, “Position: Levels of agi for operationalizing progress on the path to agi,” in _Forty-first International Conference on Machine Learning_ . 

- [144] T. Hansmeier, “Xcs for self-awareness in autonomous computing systems.” Ph.D. dissertation, University of Paderborn, Germany, 2023. 

- [145] B. Goertzel, “Golem: towards an agi meta-architecture enabling both goal preservation and radical self-improvement,” _Journal of Experimental & Theoretical Artificial Intelligence_ , vol. 26, no. 3, pp. 391–403, 2014. 

- [146] M. E. Hasselmo, “A model of prefrontal cortical mechanisms for goal-directed behavior,” _Journal of cognitive neuroscience_ , vol. 17, no. 7, pp. 1115–1129, 2005. 

- [147] C. E. Köpetz, J. L. Briskin, R. Sultana, and S. C. Stanciu, “The motivational factors underlying delay discounting.” _Motivation Science_ , vol. 7, no. 3, p. 264, 2021. 

- [148] M. Al-Shedivat, L. Lee, R. Salakhutdinov, and E. Xing, “On the complexity of exploration in goal-driven navigation,” _arXiv preprint arXiv:1811.06889_ , 2018. 

- [149] C. Luo and R. W. Proctor, “A diffusion model for the congruency sequence effect,” _Psychonomic Bulletin & Review_ , vol. 29, no. 6, pp. 2034–2051, 2022. 

- [150] B. Hommel, “Goaliath: A theory of goal-directed behavior,” _Psychological Research_ , vol. 86, no. 4, pp. 1054–1077, 2022. 

- [151] R. Yang, J. Chen, Y. Zhang, S. Yuan, A. Chen, K. Richardson, Y. Xiao, and D. Yang, “Selfgoal: Your language agents already know how to achieve high-level goals,” _arXiv preprint arXiv:2406.04784_ , 2024. 

- [152] F. Bellos, Y. Li, W. Liu, and J. Corso, “Can large language models reason about goal-oriented tasks?” in _Proceedings of the First edition of the Workshop on the Scaling Behavior of Large Language Models (SCALE-LLM 2024)_ , 2024, pp. 24–34. 

- [153] L. Ruis, A. Findeis, H. Bradley, H. A. Rahmani, K. W. Choe, E. Grefenstette, and T. Rocktäschel, “Do llms selectively encode the goal of an agent’s reach?” in _First Workshop on Theory of Mind in Communicating Agents_ , 2023. 

- [154] Y. Li, Y. Huang, Y. Lin, S. Wu, Y. Wan, and L. Sun, “I think, therefore i am: Awareness in large language models,” _arXiv preprint arXiv:2401.17882_ , 2024. 

- [155] C. Li, Y. Deng, H. Hu, M.-Y. Kan, and H. Li, “Incorporating external knowledge and goal guidance for llm-based conversational recommender systems,” _arXiv preprint arXiv:2405.01868_ , 2024. 

- [156] Y. Deng, W. Lei, M. Huang, and T.-S. Chua, “Goal awareness for conversational ai: proactivity, non-collaborativity, and beyond,” in _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 6: Tutorial Abstracts)_ , 2023, pp. 1–10. 

- [157] ——, “Rethinking conversational agents in the era of llms: Proactivity, non-collaborativity, and beyond,” in _Proceedings of the Annual International ACM SIGIR Conference on Research and Development in Information Retrieval in the Asia Pacific Region_ , 2023, pp. 298–301. 

- [158] J. Ni, V. Pandelea, T. Young, H. Zhou, and E. Cambria, “Hitkg: Towards goal-oriented conversations via multi-hierarchy learning,” in _Proceedings of the AAAI conference on artificial intelligence_ , vol. 36, no. 10, 2022, pp. 11 112–11 120. 

- [159] H. Li, J. Leung, and Z. Shen, “Towards goal-oriented large language model prompting: A survey,” _arXiv preprint arXiv:2401.14043_ , 2024. 

- [160] K. Valmeekam, A. Olmo, S. Sreedharan, and S. Kambhampati, “Large language models still can’t plan (a benchmark for llms on planning and reasoning about change),” in _NeurIPS 2022 Foundation Models for Decision Making Workshop_ , 2022. 

- [161] J. Yao, X. Yi, X. Wang, Y. Gong, and X. Xie, “Value fulcra: Mapping large language models to the multidimensional spectrum of basic human values,” _arXiv preprint arXiv:2311.10766_ , 2023. 

- [162] P. Zhong, Y. Liu, H. Wang, and C. Miao, “Keyword-guided neural conversational model,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 35, no. 16, 2021, pp. 14 568–14 576. 

- [163] Y. Deng, W. Zhang, W. Xu, W. Lei, T.-S. Chua, and W. Lam, “A unified multi-task learning framework for multi-goal conversational recommender systems,” _ACM Transactions on Information Systems_ , vol. 41, no. 3, pp. 1–25, 2023. 

- [164] Z. Liu, D. Zhou, H. Liu, H. Wang, Z.-Y. Niu, H. Wu, W. Che, T. Liu, and H. Xiong, “Graph-grounded goal planning for conversational recommendation,” _IEEE Transactions on Knowledge and Data Engineering_ , vol. 35, no. 5, pp. 4923–4939, 2022. 

- [165] E. Perez, S. Ringer, K. Lukoši¯ut˙e, K. Nguyen, E. Chen, S. Heiner, C. Pettit, C. Olsson, S. Kundu, S. Kadavath _et al._ , “Discovering language model behaviors with model-written evaluations,” _arXiv preprint arXiv:2212.09251_ , 2022. 

- [166] L. Zhou, C. Xu, and J. Corso, “Towards automatic learning of procedures from web instructional videos,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 32, no. 1, 2018. 

- [167] A. Sarkar, S. Sastry, A. Pirinen, C. Zhang, N. Jacobs, and Y. Vorobeychik, “Gomaa-geo: Goal modality agnostic active geolocalization,” _arXiv preprint arXiv:2406.01917_ , 2024. 

- [168] C. Snell, M. Yang, J. Fu, Y. Su, and S. Levine, “Context-aware language modeling for goal-oriented dialogue systems,” _arXiv preprint arXiv:2204.10198_ , 2022. 

- [169] Z. Volovikova, A. Skrynnik, P. Kuderov, and A. I. Panov, “Instruction following with goal-conditioned reinforcement learning in virtual environments,” in _ECAI 2024_ . IOS Press, 2024, pp. 650– 657. 

- [170] Y. Qin, E. Zhou, Q. Liu, Z. Yin, L. Sheng, R. Zhang, Y. Qiao, and J. Shao, “Mp5: A multi-modal open-ended embodied system in minecraft via active perception,” in _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 2024, pp. 16 307–16 316. 

- [171] H. N. E. Barj and T. Sautory, “Reinforcement learning from llm feedback to counteract goal misgeneralization,” _arXiv preprint arXiv:2401.07181_ , 2024. 

- [172] Y. Mu, Q. Zhang, M. Hu, W. Wang, M. Ding, J. Jin, B. Wang, J. Dai, Y. Qiao, and P. Luo, “Embodiedgpt: Vision-language pre-training via embodied chain of thought,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [173] F. Ni, J. Hao, S. Wu, L. Kou, J. Liu, Y. Zheng, B. Wang, and Y. Zhuang, “Generate subgoal images before act: Unlocking the chain-of-thought reasoning in diffusion model for robot manipulation with multimodal prompts,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 13 991–14 000. 

- [174] H. Yuan, Z. Mu, F. Xie, and Z. Lu, “Pre-training goal-based models for sample-efficient reinforcement learning,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [175] L. Chen, D. J. Cook, B. Guo, and W. Leister, “Guest editorialspecial issue on situation, activity, and goal awareness in cyberphysical human–machine systems,” _IEEE Transactions on HumanMachine Systems_ , vol. 47, no. 3, pp. 305–309, 2017. 

- [176] L. Chen and P. Rashidi, “Situation, activity and goal awareness in ubiquitous computing,” _International Journal of Pervasive Computing and Communications_ , vol. 8, no. 3, pp. 216–224, 2012. 

- [177] L. Wang, S. Joty, W. Gao, X. Zeng, and K.-F. Wong, “Improving conversational recommender system via contextual and timeaware modeling with less domain-specific knowledge,” _IEEE Transactions on Knowledge and Data Engineering_ , 2024. 

- [178] K. Singhal, S. Azizi, T. Tu, S. S. Mahdavi, J. Wei, H. W. Chung, N. Scales, A. Tanwani, H. Cole-Lewis, S. Pfohl _et al._ , “Large language models encode clinical knowledge,” _Nature_ , vol. 620, no. 7972, pp. 172–180, 2023. 

- [179] X. Liu, Y. Zheng, Z. Du, M. Ding, Y. Qian, Z. Yang, and J. Tang, “Gpt understands, too,” _AI Open_ , vol. 5, pp. 208–215, 2024. 

- [180] Y. Chang, X. Wang, J. Wang, Y. Wu, L. Yang, K. Zhu, H. Chen, X. Yi, C. Wang, Y. Wang _et al._ , “A survey on evaluation of large language models,” _ACM Transactions on Intelligent Systems and Technology_ , vol. 15, no. 3, pp. 1–45, 2024. 

- [181] T. Tu, S. Azizi, D. Driess, M. Schaekermann, M. Amin, P.-C. Chang, A. Carroll, C. Lau, R. Tanno, I. Ktena _et al._ , “Towards generalist biomedical ai,” _NEJM AI_ , vol. 1, no. 3, p. AIoa2300138, 2024. 

- [182] L. Cross, V. Xiang, A. Bhatia, D. L. Yamins, and N. Haber, “Hypothetical minds: Scaffolding theory of mind for multi-agent tasks with large language models,” _arXiv preprint arXiv:2407.07086_ , 2024. 

- [183] A. Chernyavskiy, A. Skrynnik, and A. Panov, “Applying opponent and environment modelling in decentralised multi-agent 

31 

reinforcement learning,” _Cognitive Systems Research_ , p. 101306, 2024. 

- [184] Y. Huang, G. Chen, J. Xu, M. Zhang, L. Yang, B. Pei, H. Zhang, L. Dong, Y. Wang, L. Wang _et al._ , “Egoexolearn: A dataset for bridging asynchronous ego-and exo-centric view of procedural activities in real world,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 22 072– 22 086. 

- [185] X. Wang, T. Kwon, M. Rad, B. Pan, I. Chakraborty, S. Andrist, D. Bohus, A. Feniello, B. Tekin, F. V. Frujeri _et al._ , “Holoassist: an egocentric human interaction dataset for interactive ai assistants in the real world,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2023, pp. 20 270–20 281. 

- [186] H. Tang, K. J. Liang, K. Grauman, M. Feiszli, and W. Wang, “Egotracks: A long-term egocentric visual object tracking dataset,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [187] Y. Yang, W. Zhai, C. Wang, C. Yu, Y. Cao, and Z.-J. Zha, “Egochoir: Capturing 3d human-object interaction regions from egocentric views,” _arXiv preprint arXiv:2405.13659_ , 2024. 

- [188] A. Suglia, C. Greco, K. Baker, J. L. Part, I. Papaioannou, A. Eshghi, I. Konstas, and O. Lemon, “Alanavlm: A multimodal embodied ai foundation model for egocentric video understanding,” _arXiv preprint arXiv:2406.13807_ , 2024. 

- [189] L. Xu, Q. Wu, L. Pan, F. Meng, H. Li, C. He, H. Wang, S. Cheng, and Y. Dai, “Towards continual egocentric activity recognition: A multi-modal egocentric activity dataset for continual learning,” _IEEE Transactions on Multimedia_ , 2023. 

- [190] Z. Fan, P. Dai, Z. Su, X. Gao, Z. Lv, J. Zhang, T. Du, G. Wang, and Y. Zhang, “Emhi: A multimodal egocentric human motion dataset with hmd and body-worn imus,” _arXiv preprint arXiv:2408.17168_ , 2024. 

- [191] Y. Ashok and M. K. Rohil, “Egocentric+: A multipurpose data set for head-mounted wearable computing devices,” in _Proceedings of the 2024 International Conference on Advanced Visual Interfaces_ , 2024, pp. 1–5. 

- [192] H. Wang, W. Liang, L. V. Gool, and W. Wang, “Towards versatile embodied navigation,” _Advances in neural information processing systems_ , vol. 35, pp. 36 858–36 874, 2022. 

- [193] R. Bigazzi, F. Landi, M. Cornia, S. Cascianelli, L. Baraldi, and R. Cucchiara, “Out of the box: embodied navigation in the real world,” in _Computer Analysis of Images and Patterns: 19th International Conference, CAIP 2021, Virtual Event, September 28– 30, 2021, Proceedings, Part I 19_ . Springer, 2021, pp. 47–57. 

- [194] P. Gao, P. Wang, F. Gao, F. Wang, and R. Yuan, “Vision-language navigation with embodied intelligence: A survey,” _arXiv preprint arXiv:2402.14304_ , 2024. 

- [195] X. Li, M. Zhang, Y. Geng, H. Geng, Y. Long, Y. Shen, R. Zhang, J. Liu, and H. Dong, “Manipllm: Embodied multimodal large language model for object-centric robotic manipulation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 18 061–18 070. 

- [196] T. Zhang, D. Li, Y. Li, Z. Zeng, L. Zhao, L. Sun, Y. Chen, X. Wei, Y. Zhan, L. Li _et al._ , “Empowering embodied manipulation: A bimanual-mobile robot manipulation dataset for household tasks,” _arXiv preprint arXiv:2405.18860_ , 2024. 

- [197] A. Kalinowska, P. M. Pilarski, and T. D. Murphey, “Embodied communication: How robots and people communicate through physical interaction,” _Annual review of control, robotics, and autonomous systems_ , vol. 6, no. 1, pp. 205–232, 2023. 

- [198] K. Shidara, H. Tanaka, H. Adachi, D. Kanayama, T. Kudo, and S. Nakamura, “Adapting the number of questions based on detected psychological distress for cognitive behavioral therapy with an embodied conversational agent: Comparative study,” _JMIR Formative Research_ , vol. 8, p. e50056, 2024. 

- [199] O. Taran, D. M. Manzone, and J. Zariffa, “Benchmarking 2d egocentric hand pose datasets,” _arXiv preprint arXiv:2409.07337_ , 2024. 

- [200] R. Leonardi, F. Ragusa, A. Furnari, and G. M. Farinella, “Egocentric human-object interaction detection exploiting synthetic data,” in _International Conference on Image Analysis and Processing_ . Springer, 2022, pp. 237–248. 

- [201] M. Birlo, R. Caramalau, P. J. Edwards, B. Dromey, M. J. Clarkson, D. Stoyanov _et al._ , “Hup-3d: A 3d multi-view synthetic dataset for assisted-egocentric hand-ultrasound pose estimation,” _arXiv preprint arXiv:2407.09215_ , 2024. 

- [202] E. Dessalene, M. Maynord, C. Fermüller, and Y. Aloimonos, 

   - “Leap: Llm-generation of egocentric action programs,” _arXiv preprint arXiv:2312.00055_ , 2023. 

- [203] G. Li, K. Zhao, S. Zhang, X. Lyu, M. Dusmanu, Y. Zhang, M. Pollefeys, and S. Tang, “Egogen: An egocentric synthetic data generator,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 14 497–14 509. 

- [204] S. Abreu, T. D. Do, K. Ahuja, E. J. Gonzalez, L. Payne, D. McDuff, and M. Gonzalez-Franco, “Parse-ego4d: Personal action recommendation suggestions for egocentric videos,” _arXiv preprint arXiv:2407.09503_ , 2024. 

- [205] L. Wang, C. Ma, X. Feng, Z. Zhang, H. Yang, J. Zhang, Z. Chen, J. Tang, X. Chen, Y. Lin _et al._ , “A survey on large language model based autonomous agents,” _Frontiers of Computer Science_ , vol. 18, no. 6, p. 186345, 2024. 

- [206] C. Zhang, K. Yang, S. Hu, Z. Wang, G. Li, Y. Sun, C. Zhang, Z. Zhang, A. Liu, S.-C. Zhu _et al._ , “Proagent: building proactive cooperative agents with large language models,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 38, no. 16, 2024, pp. 17 591–17 599. 

- [207] T. Guo, X. Chen, Y. Wang, R. Chang, S. Pei, N. V. Chawla, O. Wiest, and X. Zhang, “Large language model based multiagents: A survey of progress and challenges,” _arXiv preprint arXiv:2402.01680_ , 2024. 

- [208] H. Zhang, W. Du, J. Shan, Q. Zhou, Y. Du, J. B. Tenenbaum, T. Shu, and C. Gan, “Building cooperative embodied agents modularly with large language models,” _arXiv preprint arXiv:2307.02485_ , 2023. 

- [209] A. B. Hassouna, H. Chaari, and I. Belhaj, “Llm-agent-umf: Llm-based agent unified modeling framework for seamless integration of multi active/passive core-agents,” _arXiv preprint arXiv:2409.11393_ , 2024. 

- [210] L. Pan, Y. Li, C. Yu, and Y. Shi, “A human-computer collaborative tool for training a single large language model agent into a network through few examples,” _arXiv preprint arXiv:2404.15974_ , 2024. 

- [211] A. Padmanabha, J. Yuan, J. Gupta, Z. Karachiwalla, C. Majidi, H. Admoni, and Z. Erickson, “Voicepilot: Harnessing llms as speech interfaces for physically assistive robots,” in _Proceedings of the 37th Annual ACM Symposium on User Interface Software and Technology_ , 2024, pp. 1–18. 

- [212] C. Sun, S. Huang, and D. Pompili, “Llm-based multi-agent reinforcement learning: Current and future directions,” _arXiv preprint arXiv:2405.11106_ , 2024. 

- [213] B. Hu, C. Zhao, P. Zhang, Z. Zhou, Y. Yang, Z. Xu, and B. Liu, “Enabling intelligent interactions between an agent and an llm: A reinforcement learning approach,” _arXiv preprint arXiv:2306.03604_ , 2023. 

- [214] Z. Liu, Y. Zhang, P. Li, Y. Liu, and D. Yang, “Dynamic llm-agent network: An llm-agent collaboration framework with agent team optimization,” _arXiv preprint arXiv:2310.02170_ , 2023. 

- [215] Y. Hong, Z. Zheng, P. Chen, Y. Wang, J. Li, and C. Gan, “Multiply: A multisensory object-centric embodied large language model in 3d world,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 26 406–26 416. 

- [216] Z. Zhao, W. Chai, X. Wang, B. Li, S. Hao, S. Cao, T. Ye, and G. Wang, “See and think: Embodied agent in virtual environment,” in _European Conference on Computer Vision_ . Springer, 2025, pp. 187–204. 

- [217] R. Gong, Q. Huang, X. Ma, H. Vo, Z. Durante, Y. Noda, Z. Zheng, S.-C. Zhu, D. Terzopoulos, L. Fei-Fei _et al._ , “Mindagent: Emergent gaming interaction,” _arXiv preprint arXiv:2309.09971_ , 2023. 

- [218] E. Coumans and Y. Bai, “Pybullet, a python module for physics simulation for games, robotics and machine learning,” 2016. 

- [219] W. Yu, J. Peng, Y. Ying, S. Li, J. Ji, and Y. Zhang, “Mhrc: Closedloop decentralized multi-heterogeneous robot collaboration with large language models,” _arXiv preprint arXiv:2409.16030_ , 2024. 

- [220] V. Bhat, A. U. Kaypak, P. Krishnamurthy, R. Karri, and F. Khorrami, “Grounding llms for robot task planning using closed-loop state feedback,” _arXiv preprint arXiv:2402.08546_ , 2024. 

- [221] K. B. Buldu, S. Özdel, K. H. C. Lau, M. Wang, D. Saad, S. Schönborn, A. Boch, E. Kasneci, and E. Bozkir, “Cuify the xr: An opensource package to embed llm-powered conversational agents in xr,” _arXiv preprint arXiv:2411.04671_ , 2024. 

- [222] F. De La Torre, C. M. Fang, H. Huang, A. Banburski-Fahey, J. Amores Fernandez, and J. Lanier, “Llmr: Real-time prompting of interactive worlds using large language models,” in _Proceed-_ 

32 

_ings of the CHI Conference on Human Factors in Computing Systems_ , 2024, pp. 1–22. 

- [223] A. Zala, J. Cho, H. Lin, J. Yoon, and M. Bansal, “Envgen: Generating and adapting environments via llms for training embodied agents,” _arXiv preprint arXiv:2403.12014_ , 2024. 

- [224] R. Wang, G. Todd, Z. Xiao, X. Yuan, M.-A. Côté, P. Clark, and P. Jansen, “Can language models serve as text-based world simulators?” _arXiv preprint arXiv:2406.06485_ , 2024. 

- [225] S. Shah, D. Dey, C. Lovett, and A. Kapoor, “Airsim: High-fidelity visual and physical simulation for autonomous vehicles,” in _Field and Service Robotics: Results of the 11th International Conference_ . Springer, 2018, pp. 621–635. 

- [226] E. Kolve, R. Mottaghi, W. Han, E. VanderBilt, L. Weihs, A. Herrasti, M. Deitke, K. Ehsani, D. Gordon, Y. Zhu _et al._ , “Ai2thor: An interactive 3d environment for visual ai,” _arXiv preprint arXiv:1712.05474_ , 2017. 

- [227] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun, “Carla: An open urban driving simulator,” in _Conference on robot learning_ . PMLR, 2017, pp. 1–16. 

- [228] G. Liu, T. Sun, W. Li, X. Li, X. Liu, and J. Cui, “Eai-sim: An opensource embodied ai simulation framework with large language models,” in _2024 IEEE 18th International Conference on Control & Automation (ICCA)_ . IEEE, 2024, pp. 994–999. 

- [229] F. Yao, Y. Yue, Y. Liu, X. Sun, and K. Fu, “Aeroverse: Uav-agent benchmark suite for simulating, pre-training, finetuning, and evaluating aerospace embodied world models,” _arXiv preprint arXiv:2408.15511_ , 2024. 

- [230] M. Deitke, D. Schwenk, J. Salvador, L. Weihs, O. Michel, E. VanderBilt, L. Schmidt, K. Ehsani, A. Kembhavi, and A. Farhadi, “Objaverse: A universe of annotated 3d objects,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 13 142–13 153. 

- [231] R. Gao, Y.-Y. Chang, S. Mall, L. Fei-Fei, and J. Wu, “Objectfolder: A dataset of objects with implicit visual, auditory, and tactile representations,” _arXiv preprint arXiv:2109.07991_ , 2021. 

- [232] S. K. Ramakrishnan, A. Gokaslan, E. Wijmans, O. Maksymets, A. Clegg, J. Turner, E. Undersander, W. Galuba, A. Westbury, A. X. Chang _et al._ , “Habitat-matterport 3d dataset (hm3d): 1000 large-scale 3d environments for embodied ai,” _arXiv preprint arXiv:2109.08238_ , 2021. 

- [233] S. Rodrigues, H. K. Rayat, R. M. Kurichithanam, and S. Rukhande, “Shriek: a role playing game using unreal engine 4 and behaviour trees,” in _2021 4th biennial international conference on nascent technologies in engineering (ICNTE)_ . IEEE, 2021, pp. 1–6. 

- [234] A. Mehta, Y. Kunjadiya, A. Kulkarni, and M. Nagar, “Exploring the viability of conversational ai for non-playable characters: A comprehensive survey,” in _2021 4th International Conference on Recent Trends in Computer Science and Technology (ICRTCST)_ . IEEE, 2022, pp. 96–102. 

- [235] F. R. Christiansen, L. N. Hollensberg, N. B. Jensen, K. Julsgaard, K. N. Jespersen, and I. Nikolov, “Exploring presence in interactions with llm-driven npcs: A comparative study of speech recognition and dialogue options,” in _Proceedings of the 30th ACM Symposium on Virtual Reality Software and Technology_ , 2024, pp. 1– 11. 

- [236] M. Kaup, C. Wolff, H. Hwang, J. Mayer, and E. Bruni, “A review of nine physics engines for reinforcement learning research,” _arXiv preprint arXiv:2407.08590_ , 2024. 

- [237] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [238] Z. Si, G. Zhang, Q. Ben, B. Romero, Z. Xian, C. Liu, and C. Gan, “Difftactile: A physics-based differentiable tactile simulator for contact-rich robotic manipulation,” _arXiv preprint arXiv:2403.08716_ , 2024. 

- [239] C. E. Mower, Y. Wan, H. Yu, A. Grosnit, J. Gonzalez-Billandon, M. Zimmer, J. Wang, X. Zhang, Y. Zhao, A. Zhai _et al._ , “Rosllm: A ros framework for embodied ai with task feedback and structured reasoning,” _arXiv preprint arXiv:2406.19741_ , 2024. 

- [240] C. L. Shek, X. Wu, D. Manocha, P. Tokekar, and A. S. Bedi, “Lancar: Leveraging language for context-aware robot locomotion in unstructured environments,” _arXiv preprint arXiv:2310.00481_ , 2023. 

- [241] R. Bovo, S. Abreu, K. Ahuja, E. J. Gonzalez, L.-T. Cheng, and 

   - M. Gonzalez-Franco, “Embardiment: an embodied ai agent for productivity in xr,” _arXiv preprint arXiv:2408.08158_ , 2024. 

- [242] T. Andrade and D. Bastos, “Extended reality in iot scenarios: Concepts, applications and future trends,” in _2019 5th Experiment International Conference (exp. at’19)_ . IEEE, 2019, pp. 107–112. 

- [243] H. Wan, J. Zhang, A. A. Suria, B. Yao, D. Wang, Y. Coady, and M. Prpa, “Building llm-based ai agents in social virtual reality,” in _Extended Abstracts of the CHI Conference on Human Factors in Computing Systems_ , 2024, pp. 1–7. 

- [244] G. Rossetti, M. Stella, R. Cazabet, K. Abramski, E. Cau, S. Citraro, A. Failla, R. Improta, V. Morini, and V. Pansanella, “Y social: an llm-powered social media digital twin,” _arXiv preprint arXiv:2408.00818_ , 2024. 

- [245] R. Kurai, T. Hiraki, Y. Hiroi, Y. Hirao, M. Perusquia-Hernandez, H. Uchiyama, and K. Kiyokawa, “Magicitem: Dynamic behavior design of virtual objects with large language models in a consumer metaverse platform,” _arXiv preprint arXiv:2406.13242_ , 2024. 

- [246] T. Hayase, S. Braun, H. Yanagawa, I. Orito, and Y. Hiroi, “Panotree: Autonomous photo-spot explorer in virtual reality scenes,” _arXiv preprint arXiv:2405.17136_ , 2024. 

- [247] D. Giunchi, N. Numan, E. Gatti, and A. Steed, “Dreamcodevr: Towards democratizing behavior design in virtual reality with speech-driven programming,” in _2024 IEEE Conference Virtual Reality and 3D User Interfaces (VR)_ . IEEE, 2024, pp. 579–589. 

- [248] J. Izquierdo-Domenech, J. Linares-Pellicer, and I. Ferri-Molla, “Virtual reality and language models, a new frontier in learning,” 2024. 

- [249] Z. Li, C. Gebhardt, Y. Inglin, N. Steck, P. Streli, and C. Holz, “Situationadapt: Contextual ui optimization in mixed reality with situation awareness via llm reasoning,” in _Proceedings of the 37th Annual ACM Symposium on User Interface Software and Technology_ , 2024, pp. 1–13. 

- [250] D. Chen, Y. Huang, S. Wu, J. Tang, L. Chen, Y. Bai, Z. He, C. Wang, H. Zhou, Y. Li _et al._ , “Gui-world: A dataset for gui-oriented multimodal llm-based agents,” _arXiv preprint arXiv:2406.10819_ , 2024. 

- [251] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “Voxposer: Composable 3d value maps for robotic manipulation with language models,” _arXiv preprint arXiv:2307.05973_ , 2023. 

- [252] R. Wang, G. Todd, E. Yuan, Z. Xiao, M.-A. Côté, and P. Jansen, “Bytesized32: A corpus and challenge task for generating taskspecific world models expressed as text games,” _arXiv preprint arXiv:2305.14879_ , 2023. 

- [253] B. Liu, Y. Jiang, X. Zhang, Q. Liu, S. Zhang, J. Biswas, and P. Stone, “Llm+ p: Empowering large language models with optimal planning proficiency,” _arXiv preprint arXiv:2304.11477_ , 2023. 

- [254] Y. Yang, T. Zhou, K. Li, D. Tao, L. Li, L. Shen, X. He, J. Jiang, and Y. Shi, “Embodied multi-modal agent trained by an llm from a parallel textworld,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 26 275–26 285. 

- [255] Z. Hu, A. Iscen, A. Jain, T. Kipf, Y. Yue, D. A. Ross, C. Schmid, and A. Fathi, “Scenecraft: An llm agent for synthesizing 3d scenes as blender code,” in _Forty-first International Conference on Machine Learning_ , 2024. 

- [256] H. Tang, D. Key, and K. Ellis, “Worldcoder, a model-based llm agent: Building world models by writing code and interacting with the environment,” _arXiv preprint arXiv:2402.12275_ , 2024. 

- [257] X. Ma, Y. Bhalgat, B. Smart, S. Chen, X. Li, J. Ding, J. Gu, D. Z. Chen, S. Peng, J.-W. Bian _et al._ , “When llms step into the 3d world: A survey and meta-analysis of 3d tasks via multi-modal large language models,” _arXiv preprint arXiv:2405.10255_ , 2024. 

- [258] S. Huang, Z. Jiang, H. Dong, Y. Qiao, P. Gao, and H. Li, “Instruct2act: Mapping multi-modality instructions to robotic actions with large language model,” _arXiv preprint arXiv:2305.11176_ , 2023. 

- [259] H. I. I. Tam, H. I. D. Pun, A. T. Wang, A. X. Chang, and M. Savva, “Scenemotifcoder: Example-driven visual program learning for generating 3d object arrangements,” _arXiv preprint arXiv:2408.02211_ , 2024. 

- [260] R. Volum, S. Rao, M. Xu, G. DesGarennes, C. Brockett, B. Van Durme, O. Deng, A. Malhotra, and W. B. Dolan, “Craft an iron sword: Dynamically generating interactive game characters by prompting large language models tuned on code,” in _Proceedings of the 3rd Wordplay: When Language Meets Games Workshop (Wordplay 2022)_ , 2022, pp. 25–43. 

33 

- [261] N. Numan, S. Rajaram, B. T. Kumaravel, N. Marquardt, and A. D. Wilson, “Spaceblender: Creating context-rich collaborative spaces through generative 3d scene blending,” in _Proceedings of the 37th Annual ACM Symposium on User Interface Software and Technology_ , 2024, pp. 1–25. 

- [262] W. Qian, C. Gao, A. Sathya, R. Suzuki, and K. Nakagaki, “Shapeit: Exploring text-to-shape-display for generative shape-changing behaviors with llms,” in _Proceedings of the 37th Annual ACM Symposium on User Interface Software and Technology_ , 2024, pp. 1– 29. 

- [263] M. Windrich, M. Grimmer, O. Christ, S. Rinderknecht, and P. Beckerle, “Active lower limb prosthetics: a systematic review of design issues and solutions,” _Biomedical engineering online_ , vol. 15, pp. 5–19, 2016. 

- [264] D. Farina, I. Vujaklija, R. Brånemark, A. M. Bull, H. Dietl, B. Graimann, L. J. Hargrove, K.-P. Hoffmann, H. Huang, T. Ingvarsson _et al._ , “Toward higher-performance bionic limbs for wider clinical use,” _Nature biomedical engineering_ , vol. 7, no. 4, pp. 473–485, 2023. 

- [265] M. Li, Z. Zhan, H. Yang, Y. Xiao, J. Huang, and R. Zhang, “Benchmarking retrieval-augmented large language models in biomedical nlp: Application, robustness, and self-awareness,” _arXiv preprint arXiv:2405.08151_ , 2024. 

- [266] J. Chen, X. Wang, R. Xu, S. Yuan, Y. Zhang, W. Shi, J. Xie, S. Li, R. Yang, T. Zhu _et al._ , “From persona to personalization: A survey on role-playing language agents,” _arXiv preprint arXiv:2404.18231_ , 2024. 

- [267] Y. Wang, Y. Liao, H. Liu, H. Liu, Y. Wang, and Y. Wang, “Mmsap: A comprehensive benchmark for assessing self-awareness of multimodal large language models in perception,” _arXiv preprint arXiv:2401.07529_ , 2024. 

- [268] Z. Yin, Q. Sun, Q. Guo, J. Wu, X. Qiu, and X. Huang, “Do large language models know what they don’t know?” _arXiv preprint arXiv:2305.18153_ , 2023. 

- [269] C. Wang, X. Liu, Y. Yue, X. Tang, T. Zhang, C. Jiayang, Y. Yao, W. Gao, X. Hu, Z. Qi _et al._ , “Survey on factuality in large language models: Knowledge, retrieval and domain-specificity,” _arXiv preprint arXiv:2310.07521_ , 2023. 

- [270] G. Prato, J. Huang, P. Parthasarathi, S. Sodhani, and S. Chandar, “Do large language models know how much they know?” in _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ , 2024, pp. 6054–6070. 

- [271] K. Liang, Z. Zhang, and J. F. Fisac, “Introspective planning: Guiding language-enabled agents to refine their own uncertainty,” _arXiv preprint arXiv:2402.06529_ , 2024. 

- [272] I. Song, S. Park, S. R. Pendse, J. L. Schleider, M. De Choudhury, and Y.-H. Kim, “Exploreself: Fostering user-driven exploration and reflection on personal challenges with adaptive guidance by large language models,” _arXiv preprint arXiv:2409.09662_ , 2024. 

- [273] Y. Wang, P. Li, M. Sun, and Y. Liu, “Self-knowledge guided retrieval augmentation for large language models,” _arXiv preprint arXiv:2310.05002_ , 2023. 

- [274] R. Laine, B. Chughtai, J. Betley, K. Hariharan, J. Scheurer, M. Balesni, M. Hobbhahn, A. Meinke, and O. Evans, “Me, myself, and ai: The situational awareness dataset (sad) for llms,” _arXiv preprint arXiv:2407.04694_ , 2024. 

- [275] T. R. Davidson, V. Surkov, V. Veselovsky, G. Russo, R. West, and C. Gulcehre, “Self-recognition in language models,” _arXiv preprint arXiv:2407.06946_ , 2024. 

- [276] Z. Wen, Z. Tian, Z. Jian, Z. Huang, P. Ke, Y. Gao, M. Huang, and D. Li, “Perception of knowledge boundary for large language models through semi-open-ended question answering,” _arXiv preprint arXiv:2405.14383_ , 2024. 

- [277] K. Pushpanathan, Z. W. Lim, S. M. E. Yew, D. Z. Chen, H. A. H. Lin, J. H. L. Goh, W. M. Wong, X. Wang, M. C. J. Tan, V. T. C. Koh _et al._ , “Popular large language model chatbots accuracy, comprehensiveness, and self-awareness in answering ocular symptom queries,” _Iscience_ , vol. 26, no. 11, 2023. 

- [278] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray _et al._ , “Training language models to follow instructions with human feedback,” _Advances in neural information processing systems_ , vol. 35, pp. 27 730–27 744, 2022. 

- [279] Q. Cheng, T. Sun, X. Liu, W. Zhang, Z. Yin, S. Li, L. Li, Z. He, K. Chen, and X. Qiu, “Can ai assistants know what they don’t know?” _arXiv preprint arXiv:2401.13275_ , 2024. 

- [280] F. Zhu and R. Simmons, “Bootstrapping cognitive agents with a large language model,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 38, no. 1, 2024, pp. 655–663. 

- [281] A. Amayuelas, K. Wong, L. Pan, W. Chen, and W. Wang, “Knowledge of knowledge: Exploring known-unknowns uncertainty with large language models,” _arXiv preprint arXiv:2305.13712_ , 2023. 

- [282] S. Feng, W. Shi, Y. Wang, W. Ding, V. Balachandran, and Y. Tsvetkov, “Don’t hallucinate, abstain: Identifying llm knowledge gaps via multi-llm collaboration,” _arXiv preprint arXiv:2402.00367_ , 2024. 

- [283] Z. Yao, W. Qi, L. Pan, S. Cao, L. Hu, W. Liu, L. Hou, and J. Li, “Seakr: Self-aware knowledge retrieval for adaptive retrieval augmented generation,” _arXiv preprint arXiv:2406.19215_ , 2024. 

- [284] X. Liang, S. Song, Z. Zheng, H. Wang, Q. Yu, X. Li, R.-H. Li, Y. Wang, Z. Wang, F. Xiong _et al._ , “Internal consistency and selffeedback in large language models: A survey,” _arXiv preprint arXiv:2407.14507_ , 2024. 

- [285] X. Peng and X. Geng, “Self-controller: Controlling llms with multi-round step-by-step self-awareness,” _arXiv preprint arXiv:2410.00359_ , 2024. 

- [286] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W.-t. Yih, T. Rocktäschel _et al._ , “Retrievalaugmented generation for knowledge-intensive nlp tasks,” _Advances in Neural Information Processing Systems_ , vol. 33, pp. 9459– 9474, 2020. 

- [287] Z. Jiang, F. F. Xu, L. Gao, Z. Sun, Q. Liu, J. Dwivedi-Yu, Y. Yang, J. Callan, and G. Neubig, “Active retrieval augmented generation,” _arXiv preprint arXiv:2305.06983_ , 2023. 

- [288] J. Wang, G. He, and Y. Kantaros, “Safe task planning for language-instructed multi-robot systems using conformal prediction,” _arXiv preprint arXiv:2402.15368_ , 2024. 

- [289] Q. Wu, G. Bansal, J. Zhang, Y. Wu, S. Zhang, E. Zhu, B. Li, L. Jiang, X. Zhang, and C. Wang, “Autogen: Enabling next-gen llm applications via multi-agent conversation framework,” _arXiv preprint arXiv:2308.08155_ , 2023. 

- [290] H. Liu, L. Lee, K. Lee, and P. Abbeel, “Instructionfollowing agents with multimodal transformer,” _arXiv preprint arXiv:2210.13431_ , 2022. 

- [291] Y. Xie, C. Yu, T. Zhu, J. Bai, Z. Gong, and H. Soh, “Translating natural language to planning goals with large-language models,” _arXiv preprint arXiv:2302.05128_ , 2023. 

- [292] K. Valmeekam, M. Marquez, S. Sreedharan, and S. Kambhampati, “On the planning abilities of large language models-a critical investigation,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 75 993–76 005, 2023. 

- [293] M. A. Graule and V. Isler, “Gg-llm: Geometrically grounding large language models for zero-shot human activity forecasting in human-aware task planning,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 568–574. 

- [294] T. Silver, S. Dan, K. Srinivas, J. B. Tenenbaum, L. Kaelbling, and M. Katz, “Generalized planning in pddl domains with pretrained large language models,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 38, no. 18, 2024, pp. 20 256–20 264. 

- [295] T. Silver, V. Hariprasad, R. S. Shuttleworth, N. Kumar, T. LozanoPérez, and L. P. Kaelbling, “Pddl planning with pretrained large language models,” in _NeurIPS 2022 foundation models for decision making workshop_ , 2022. 

- [296] Y. Zhai, H. Bai, Z. Lin, J. Pan, S. Tong, Y. Zhou, A. Suhr, S. Xie, Y. LeCun, Y. Ma _et al._ , “Fine-tuning large vision-language models as decision-making agents via reinforcement learning,” _arXiv preprint arXiv:2405.10292_ , 2024. 

- [297] S. S. Raman, V. Cohen, E. Rosen, I. Idrees, D. Paulius, and S. Tellex, “Planning with large language models via corrective re-prompting,” in _NeurIPS 2022 Foundation Models for Decision Making Workshop_ , 2022. 

- [298] W. Shi, X. He, Y. Zhang, C. Gao, X. Li, J. Zhang, Q. Wang, and F. Feng, “Large language models are learnable planners for longterm recommendation,” in _Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval_ , 2024, pp. 1893–1903. 

- [299] L. Guan, K. Valmeekam, S. Sreedharan, and S. Kambhampati, “Leveraging pre-trained large language models to construct and utilize world models for model-based task planning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 79 081–79 094, 2023. 

34 

- [300] S. Mahdavi, R. Aoki, K. Tang, and Y. Cao, “Leveraging environment interaction for automated pddl translation and planning with large language models,” _arXiv preprint arXiv:2407.12979_ , 2024. 

- [301] B. Paranjape, S. Lundberg, S. Singh, H. Hajishirzi, L. Zettlemoyer, and M. T. Ribeiro, “Art: Automatic multi-step reasoning and tooluse for large language models,” _arXiv preprint arXiv:2303.09014_ , 2023. 

- [302] K. F. Gbagbe, M. A. Cabrera, A. Alabbas, O. Alyunes, A. Lykov, and D. Tsetserukou, “Bi-vla: Vision-language-action model-based system for bimanual robotic dexterous manipulations,” _arXiv preprint arXiv:2405.06039_ , 2024. 

- [303] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3d-vla: A 3d vision-language-action generative world model,” _arXiv preprint arXiv:2403.09631_ , 2024. 

- [304] E. Jang, A. Irpan, M. Khansari, D. Kappler, F. Ebert, C. Lynch, S. Levine, and C. Finn, “Bc-z: Zero-shot task generalization with robotic imitation learning,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 991–1002. 

- [305] J. Lu, C. Clark, S. Lee, Z. Zhang, S. Khosla, R. Marten, D. Hoiem, and A. Kembhavi, “Unified-io 2: Scaling autoregressive multimodal models with vision language audio and action,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 26 439–26 455. 

- [306] P. Ding, H. Zhao, W. Zhang, W. Song, M. Zhang, S. Huang, N. Yang, and D. Wang, “Quar-vla: Vision-language-action model for quadruped robots,” in _European Conference on Computer Vision_ . Springer, Cham, 2025, pp. 352–367. 

- [307] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [308] P. Vogt, “The physical symbol grounding problem,” _Cognitive Systems Research_ , vol. 3, no. 3, pp. 429–457, 2002. 

- [309] M. Taddeo and L. Floridi, “Solving the symbol grounding problem: a critical review of fifteen years of research,” _Journal of Experimental & Theoretical Artificial Intelligence_ , vol. 17, no. 4, pp. 419–445, 2005. 

- [310] A. Newell and H. A. Simon, “Computer science as empirical inquiry: Symbols and search,” in _ACM Turing award lectures_ , 2007, p. 1975. 

- [311] A. Cangelosi, “Approaches to grounding symbols in perceptual and sensorimotor categories,” in _Handbook of categorization in cognitive science_ . Elsevier, 2005, pp. 719–737. 

- [312] K. F. MacDorman, “Grounding symbols through sensorimotor integration,” _Journal of the Robotics Society of Japan_ , vol. 17, no. 1, pp. 20–24, 1999. 

- [313] D. Pecher, I. Boot, and S. Van Dantzig, “Abstract concepts: Sensory-motor grounding, metaphors, and beyond,” in _Psychology of learning and motivation_ . Elsevier, 2011, vol. 54, pp. 217–248. 

- [314] Z. W. Pylyshyn, “Computation and cognition: Issues in the foundations of cognitive science,” _Behavioral and Brain sciences_ , vol. 3, no. 1, pp. 111–132, 1980. 

- [315] J. Searle, “Minds, brains, and programs,” 1980. 

- [316] J. A. Fodor, “The modularity of mind,” 1983. 

- [317] L. W. Barsalou, “Grounded cognition,” _Annu. Rev. Psychol._ , vol. 59, no. 1, pp. 617–645, 2008. 

- [318] J. A. Fodor, “Methodological solipsism considered as a research strategy in cognitive psychology1,” _Behavioral and brain sciences_ , vol. 3, no. 1, pp. 63–73, 1980. 

- [319] E. Meins, C. Fernyhough, B. Arnott, S. R. Leekam, and M. de Rosnay, “Mind-mindedness and theory of mind: Mediating roles of language and perspectival symbolic play,” _Child development_ , vol. 84, no. 5, pp. 1777–1790, 2013. 

- [320] G. Bajaj, V. L. Shalin, S. Parthasarathy, and A. Sheth, “Grounding from an ai and cognitive science lens,” _IEEE Intelligent Systems_ , vol. 39, no. 2, pp. 66–71, 2024. 

- [321] P. Smolensky, “Tensor product variable binding and the representation of symbolic structures in connectionist systems,” _Artificial intelligence_ , vol. 46, no. 1-2, pp. 159–216, 1990. 

- [322] E. P. Frady, D. Kleyko, and F. T. Sommer, “Variable binding for sparse distributed representations: Theory and applications,” _IEEE Transactions on Neural Networks and Learning Systems_ , vol. 34, no. 5, pp. 2191–2204, 2021. 

- [323] C. Glanois, Z. Jiang, X. Feng, P. Weng, M. Zimmer, D. Li, W. Liu, and J. Hao, “Neuro-symbolic hierarchical rule induction,” in 

   - _International Conference on Machine Learning_ . PMLR, 2022, pp. 7583–7615. 

- [324] P. Sen, B. W. Carvalho, I. Abdelaziz, P. Kapanipathi, F. Luus, S. Roukos, and A. Gray, “Combining rules and embeddings via neuro-symbolic ai for knowledge base completion,” _arXiv preprint arXiv:2109.09566_ , 2021. 

- [325] V. Belle, “Symbolic logic meets machine learning: A brief survey in infinite domains,” in _International conference on scalable uncertainty management_ . Springer, 2020, pp. 3–16. 

- [326] F. Correia, “Logical grounds,” _The review of symbolic logic_ , vol. 7, no. 1, pp. 31–59, 2014. 

- [327] S. Tellex, T. Kollar, S. Dickerson, M. R. Walter, A. G. Banerjee, S. Teller, and N. Roy, “Approaching the symbol grounding problem with probabilistic graphical models,” _AI magazine_ , vol. 32, no. 4, pp. 64–76, 2011. 

- [328] T. Kollar, S. Tellex, M. R. Walter, A. Huang, A. Bachrach, S. Hemachandra, E. Brunskill, A. Banerjee, D. Roy, S. Teller _et al._ , “Generalized grounding graphs: A probabilistic framework for understanding grounded language,” _Journal of Artificial Intelligence Research_ , pp. 1–35, 2013. 

- [329] S. Guo, Q. Wang, L. Wang, B. Wang, and L. Guo, “Jointly embedding knowledge graphs and logical rules,” in _Proceedings of the 2016 conference on empirical methods in natural language processing_ , 2016, pp. 192–202. 

- [330] D. Chaudhuri, M. R. A. H. Rony, and J. Lehmann, “Grounding dialogue systems via knowledge graph aware decoding with pre-trained transformers,” in _The Semantic Web: 18th International Conference, ESWC 2021, Virtual Event, June 6–10, 2021, Proceedings 18_ . Springer, 2021, pp. 323–339. 

- [331] S. Ji, S. Pan, E. Cambria, P. Marttinen, and S. Y. Philip, “A survey on knowledge graphs: Representation, acquisition, and applications,” _IEEE transactions on neural networks and learning systems_ , vol. 33, no. 2, pp. 494–514, 2021. 

- [332] L. de Penning, A. Garcez, L. C. Lamb, and J. Meyer, “A neuralsymbolic cognitive agent for online learning and reasoning,” in _Proceedings of the Twenty-Second international joint conference on Artificial Intelligence_ , vol. 2. International Joint Conferences on Artificial Intelligence, 2011, pp. 1653–1658. 

- [333] J. Liu, M. Zhang, W. Li, C. Wang, S. Li, H. Jiang, S. Jiang, Y. Xiao, and Y. Chen, “Beyond entities: A large-scale multi-modal knowledge graph with triplet fact grounding,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 38, no. 17, 2024, pp. 18 653–18 661. 

- [334] K. Cheng, N. K. Ahmed, R. A. Rossi, T. Willke, and Y. Sun, “Neural-symbolic methods for knowledge graph reasoning: A survey,” _ACM Transactions on Knowledge Discovery from Data_ , vol. 18, no. 9, pp. 1–44, 2024. 

- [335] D. Demeter and D. Downey, “Just add functions: A neuralsymbolic language model,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 34, no. 05, 2020, pp. 7634–7642. 

- [336] Z. Li, Y. Yao, T. Chen, J. Xu, C. Cao, X. Ma, and J. Lü, “Softened symbol grounding for neuro-symbolic systems,” _arXiv preprint arXiv:2403.00323_ , 2024. 

- [337] R. Zellers, A. Holtzman, M. Peters, R. Mottaghi, A. Kembhavi, A. Farhadi, and Y. Choi, “Piglet: Language grounding through neuro-symbolic interaction in a 3d world,” _arXiv preprint arXiv:2106.00188_ , 2021. 

- [338] J. Hsu, J. Mao, and J. Wu, “Ns3d: Neuro-symbolic grounding of 3d objects and relations,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 2614–2623. 

- [339] J. Mao, C. Gan, P. Kohli, J. B. Tenenbaum, and J. Wu, “The neurosymbolic concept learner: Interpreting scenes, words, and sentences from natural supervision,” _arXiv preprint arXiv:1904.12584_ , 2019. 

- [340] J. Deng, Z. Yang, D. Liu, T. Chen, W. Zhou, Y. Zhang, H. Li, and W. Ouyang, “Transvg++: End-to-end visual grounding with language conditioned vision transformer,” _IEEE transactions on pattern analysis and machine intelligence_ , 2023. 

- [341] E. Pavlick, “Symbols and grounding in large language models,” _Philosophical Transactions of the Royal Society A_ , vol. 381, no. 2251, p. 20220041, 2023. 

- [342] W. Huang, F. Xia, D. Shah, D. Driess, A. Zeng, Y. Lu, P. Florence, I. Mordatch, S. Levine, K. Hausman _et al._ , “Grounded decoding: Guiding text generation with grounded models for embodied agents,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

35 

- [343] Z. Li, Q. Xu, D. Zhang, H. Song, Y. Cai, Q. Qi, R. Zhou, J. Pan, Z. Li, V. Tu _et al._ , “Groundinggpt: Language enhanced multimodal grounding model,” in _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , 2024, pp. 6657–6678. 

- [344] X. Chen, S. Jia, and Y. Xiang, “A review: Knowledge reasoning over knowledge graph,” _Expert systems with applications_ , vol. 141, p. 112948, 2020. 

- [345] D. Fensel, U. ¸Sim¸sek, K. Angele, E. Huaman, E. Kärle, O. Panasiuk, I. Toma, J. Umbrich, A. Wahler, D. Fensel _et al._ , “Introduction: what is a knowledge graph?” _Knowledge graphs: Methodology, tools and selected use cases_ , pp. 1–10, 2020. 

- [346] Q. Wang, Z. Mao, B. Wang, and L. Guo, “Knowledge graph embedding: A survey of approaches and applications,” _IEEE transactions on knowledge and data engineering_ , vol. 29, no. 12, pp. 2724–2743, 2017. 

- [347] C. Rosset, C. Xiong, M. Phan, X. Song, P. Bennett, and S. Tiwary, “Knowledge-aware language model pretraining,” _arXiv preprint arXiv:2007.00655_ , 2020. 

- [348] W. Liu, P. Zhou, Z. Zhao, Z. Wang, Q. Ju, H. Deng, and P. Wang, “K-bert: Enabling language representation with knowledge graph,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 34, no. 03, 2020, pp. 2901–2908. 

- [349] Y. Sun, S. Wang, Y. Li, S. Feng, X. Chen, H. Zhang, X. Tian, D. Zhu, H. Tian, and H. Wu, “Ernie: Enhanced representation through knowledge integration,” _arXiv preprint arXiv:1904.09223_ , 2019. 

- [350] S. Pan, L. Luo, Y. Wang, C. Chen, J. Wang, and X. Wu, “Unifying large language models and knowledge graphs: A roadmap,” _IEEE Transactions on Knowledge and Data Engineering_ , 2024. 

- [351] H. Zhou, T. Shen, X. Liu, Y. Zhang, P. Guo, and J. Zhang, “Survey of knowledge graph approaches and applications,” _Journal on Artificial Intelligence_ , vol. 2, no. 2, pp. 89–101, 2020. 

- [352] B. Zhang and H. Soh, “Extract, define, canonicalize: An llm-based framework for knowledge graph construction,” _arXiv preprint arXiv:2404.03868_ , 2024. 

- [353] Z. Zhang, X. Liu, Y. Zhang, Q. Su, X. Sun, and B. He, “Pretrainkge: learning knowledge representation from pretrained language models,” in _Findings of the Association for Computational Linguistics: EMNLP 2020_ , 2020, pp. 259–266. 

- [354] H. Abu-Rasheed, C. Weber, and M. Fathi, “Knowledge graphs as context sources for llm-based explanations of learning recommendations,” _arXiv preprint arXiv:2403.03008_ , 2024. 

- [355] J. Z. Pan, S. Razniewski, J.-C. Kalo, S. Singhania, J. Chen, S. Dietze, H. Jabeen, J. Omeliyanenko, W. Zhang, M. Lissandrini _et al._ , “Large language models and knowledge graphs: Opportunities and challenges,” _arXiv preprint arXiv:2308.06374_ , 2023. 

- [356] J. Xu, Z. Wu, M. Lin, X. Zhang, and S. Wang, “Llm and gnn are complementary: Distilling llm for multimodal graph learning,” _arXiv preprint arXiv:2406.01032_ , 2024. 

- [357] X. Wang, T. Gao, Z. Zhu, Z. Zhang, Z. Liu, J. Li, and J. Tang, “Kepler: A unified model for knowledge embedding and pretrained language representation,” _Transactions of the Association for Computational Linguistics_ , vol. 9, pp. 176–194, 2021. 

- [358] H. Khorashadizadeh, F. Z. Amara, M. Ezzabady, F. Ieng, S. Tiwari, N. Mihindukulasooriya, J. Groppe, S. Sahri, F. Benamara, and S. Groppe, “Research trends for the interplay between large language models and knowledge graphs,” _arXiv preprint arXiv:2406.08223_ , 2024. 

- [359] T. Çöplü, A. Bendiken, A. Skomorokhov, E. Bateiko, and S. Cobb, “Prompt-time ontology-driven symbolic knowledge capture with large language models,” _arXiv preprint arXiv:2405.14012_ , 2024. 

- [360] O. Palagin, V. Kaverinskiy, A. Litvin, and K. Malakhov, “Ontochatgpt information system: Ontology-driven structured prompts for chatgpt meta-learning,” _arXiv preprint arXiv:2307.05082_ , 2023. 

- [361] C. Zhang, B. Peng, X. Sun, Q. Niu, J. Liu, K. Chen, M. Li, P. Feng, Z. Bi, M. Liu _et al._ , “From word vectors to multimodal embeddings: Techniques, applications, and future directions for large language models,” _arXiv preprint arXiv:2411.05036_ , 2024. 

- [362] J. X. Liu, A. Shah, G. Konidaris, S. Tellex, and D. Paulius, “Lang2ltl-2: Grounding spatiotemporal navigation commands using large language and vision-language models,” in _2nd CoRL Workshop on Learning Effective Abstractions for Planning_ , 2024. 

- [363] S. Hsu, O. Khattab, C. Finn, and A. Sharma, “Grounding by trying: Llms with reinforcement learning-enhanced retrieval,” _arXiv preprint arXiv:2410.23214_ , 2024. 

- [364] S. Zhao, Y. Yang, Z. Wang, Z. He, L. K. Qiu, and L. Qiu, “Retrieval augmented generation (rag) and beyond: A comprehensive survey on how to make your llms use external data more wisely,” _arXiv preprint arXiv:2409.14924_ , 2024. 

- [365] A. S. Lippolis, M. Ceriani, S. Zuppiroli, and A. G. Nuzzolese, “Ontogenia: Ontology generation with metacognitive prompting in large language models,” in _Proc. of the Extended Semantic Web Conference-Satellite Events, Springer, Crete, Grece_ , 2024. 

- [366] R. Wang, Z. Yang, Z. Zhao, X. Tong, Z. Hong, and K. Qian, “Llmbased robot task planning with exceptional handling for general purpose service robots,” _arXiv preprint arXiv:2405.15646_ , 2024. 

- [367] H. B. Giglou, J. D’Souza, F. Engel, and S. Auer, “Llms4om: Matching ontologies with large language models,” _arXiv preprint arXiv:2404.10317_ , 2024. 

- [368] H. Babaei Giglou, J. DSouza, and S. Auer, “Llms4ol: Large language models for ontology learning,” in _International Semantic Web Conference_ . Springer, 2023, pp. 408–427. 

- [369] L. M. V. da Silva, A. Kocher, F. Gehlhoff, and A. Fay, “Toward a method to generate capability ontologies from natural language descriptions,” in _2024 IEEE 29th International Conference on Emerging Technologies and Factory Automation (ETFA)_ . IEEE, 2024, pp. 1–4. 

- [370] J. Camacho-Collados and M. T. Pilehvar, “From word to sense embeddings: A survey on vector representations of meaning,” _Journal of Artificial Intelligence Research_ , vol. 63, pp. 743–788, 2018. 

- [371] G. Tennenholtz, Y. Chow, C.-W. Hsu, J. Jeong, L. Shani, A. Tulepbergenov, D. Ramachandran, M. Mladenov, and C. Boutilier, “Demystifying embedding spaces using large language models,” _arXiv preprint arXiv:2310.04475_ , 2023. 

- [372] H. Lyre, “" understanding ai": Semantic grounding in large language models,” _arXiv preprint arXiv:2402.10992_ , 2024. 

- [373] V. Cohen, J. X. Liu, R. Mooney, S. Tellex, and D. Watkins, “A survey of robotic language grounding: Tradeoffs between symbols and embeddings,” _arXiv preprint arXiv:2405.13245_ , 2024. 

- [374] J. Vig, S. Gehrmann, Y. Belinkov, S. Qian, D. Nevo, Y. Singer, and S. Shieber, “Investigating gender bias in language models using causal mediation analysis,” _Advances in neural information processing systems_ , vol. 33, pp. 12 388–12 401, 2020. 

- [375] “Combining reinforcement learning with neuro-symbolic planning.” _Available online: https://medium.com/@ulzhalgasrakhman/combining-reinforcementlearning-with-neuro-symbolic-planning-bc19f7b06ca7 (accessed on 16 Feb. 2024)._ , 2024. 

- [376] H. Jacobsson, G.-J. Kruijff, and M. Staudte, “From rule extraction to active learning symbol grounding,” in _Proceedings of ICRA 2007 Workshop on Concept Learning for Embodied Agents_ , 2007. 

- [377] J. Kulick, M. Toussaint, T. Lang, and M. Lopes, “Active learning for teaching a robot grounded relational symbols.” in _IJCAI_ . Citeseer, 2013, pp. 1451–1457. 

- [378] B. Colle, “Improving embodied llm agents’ capabilities through collaboration,” 2024. 

- [379] D. Roy, “Semiotic schemas: A framework for grounding language in action and perception,” _Artificial Intelligence_ , vol. 167, no. 1-2, pp. 170–205, 2005. 

- [380] M. Zadem, Z. Ji _et al._ , “Llm to bridge human instructions with a dynamic symbolic representation in hierarchical reinforcement learning,” in _NeurIPS 2024 Workshop on Behavioral Machine Learning_ . 

- [381] J. Gehring, K. Zheng, J. Copet, V. Mella, T. Cohen, and G. Synnaeve, “Rlef: Grounding code llms in execution feedback with reinforcement learning,” _arXiv preprint arXiv:2410.02089_ , 2024. 

- [382] W. Tan, W. Zhang, S. Liu, L. Zheng, X. Wang, and B. An, “True knowledge comes from practice: Aligning llms with embodied environments via reinforcement learning,” _arXiv preprint arXiv:2401.14151_ , 2024. 

- [383] H. Li, H. N. Mahjoub, B. Chalaki, V. Tadiparthi, K. Lee, E. M. Pari, C. M. Lewis, and K. P. Sycara, “Language grounded multi-agent reinforcement learning with human-interpretable communication,” in _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ . 

- [384] A. Moroncelli, V. Soni, A. A. Shahid, M. Maccarini, M. Forgione, D. Piga, B. Spahiu, and L. Roveda, “Integrating reinforcement learning with foundation models for autonomous robotics: Methods and perspectives,” _arXiv preprint arXiv:2410.16411_ , 2024. 

- [385] Y. Cao, H. Zhao, Y. Cheng, T. Shu, Y. Chen, G. Liu, G. Liang, J. Zhao, J. Yan, and Y. Li, “Survey on large language modelenhanced reinforcement learning: Concept, taxonomy, and meth- 

36 

ods,” _IEEE Transactions on Neural Networks and Learning Systems_ , 2024. 

- [386] Y. Hong, H. Zhen, P. Chen, S. Zheng, Y. Du, Z. Chen, and C. Gan, “3d-llm: Injecting the 3d world into large language models,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 20 482–20 494, 2023. 

- [387] G. Cheng, C. Zhang, W. Cai, L. Zhao, C. Sun, and J. Bian, “Llm+ a: Grounding large language models in physical world with affordance prompting,” 2024. 

- [388] D. Vrandeˇci´c and M. Krötzsch, “Wikidata: a free collaborative knowledgebase,” _Communications of the ACM_ , vol. 57, no. 10, pp. 78–85, 2014. 

- [389] B. B. Mahria, I. Chaker, and A. Zahi, “Building knowledge graph from relational database,” in _Semantic AI in Knowledge Graphs_ . CRC Press, 2023, pp. 163–190. 

- [390] S. Sun, F. Meng, and D. Chu, “A model driven approach to constructing knowledge graph from relational database,” in _Journal of Physics: Conference Series_ , vol. 1584, no. 1. IOP Publishing, 2020, p. 012073. 

- [391] T. Zhang, S. G. Patil, N. Jain, S. Shen, M. Zaharia, I. Stoica, and J. E. Gonzalez, “Raft: Adapting language model to domain specific rag,” _arXiv preprint arXiv:2403.10131_ , 2024. 

- [392] S. Wang, J. Liu, S. Song, J. Cheng, Y. Fu, P. Guo, K. Fang, Y. Zhu, and Z. Dou, “Domainrag: A chinese benchmark for evaluating domain-specific retrieval-augmented generation,” _arXiv preprint arXiv:2406.05654_ , 2024. 

- [393] A. Parisi, Y. Zhao, and N. Fiedel, “Talm: Tool augmented language models,” _arXiv preprint arXiv:2205.12255_ , 2022. 

- [394] Y. Qin, S. Liang, Y. Ye, K. Zhu, L. Yan, Y. Lu, Y. Lin, X. Cong, X. Tang, B. Qian _et al._ , “Toolllm: Facilitating large language models to master 16000+ real-world apis,” _arXiv preprint arXiv:2307.16789_ , 2023. 

- [395] S. Panda and N. Kaur, “Revolutionizing language processing in libraries with sheetgpt: an integration of google sheet and chatgpt plugin,” _Library Hi Tech News_ , vol. 41, no. 5, pp. 8–10, 2024. 

- [396] B. Schölkopf, “Causality for machine learning,” in _Probabilistic and causal inference: The works of Judea Pearl_ , 2022, pp. 765–804. 

- [397] J. Pearl, “Causality,” 2009. [398] Y. Zhang, M. Gong, T. Liu, G. Niu, X. Tian, B. Han, B. Schölkopf, and K. Zhang, “Causaladv: Adversarial robustness through the lens of causality,” _arXiv preprint arXiv:2106.06196_ , 2021. 

- [399] M. Ren, Y.-L. Wang, and Z.-F. He, “Towards interpretable defense against adversarial attacks via causal inference,” _Machine Intelligence Research_ , vol. 19, no. 3, pp. 209–226, 2022. 

- [400] H. Debbi, “Causadv: A causal-based framework for detecting adversarial examples,” _arXiv preprint arXiv:2411.00839_ , 2024. 

- [401] A. Vlontzos, D. Rueckert, and B. Kainz, “A review of causality for learning algorithms in medical image analysis,” _arXiv preprint arXiv:2206.05498_ , 2022. 

- [402] J. Pearl, “The seven tools of causal inference, with reflections on machine learning,” _Communications of the ACM_ , vol. 62, no. 3, pp. 54–60, 2019. 

- [403] S. Lobentanzer, P. Rodriguez-Mier, S. Bauer, and J. SaezRodriguez, “Molecular causality in the advent of foundation models,” _Molecular Systems Biology_ , pp. 1–11, 2024. 

- [404] M. Willig, M. Zeˇcevi´c, D. S. Dhami, and K. Kersting, “Probing for correlations of causal facts: Large language models and causality,” 2023. 

- [405] U. Hasan and M. O. Gani, “Kcrl: A prior knowledge based causal discovery framework with reinforcement learning,” in _Machine Learning for Healthcare Conference_ . PMLR, 2022, pp. 691–714. 

- [406] A. C. Constantinou, Z. Guo, and N. K. Kitson, “The impact of prior knowledge on causal structure learning,” _Knowledge and Information Systems_ , vol. 65, no. 8, pp. 3385–3434, 2023. 

- [407] E. Kıcıman, R. Ness, A. Sharma, and C. Tan, “Causal reasoning and large language models: Opening a new frontier for causality,” _arXiv preprint arXiv:2305.00050_ , 2023. 

- [408] H. P. Stapp, “Correlation experiments and the nonvalidity of ordinary ideas about the physical world,” 1976. 

- [409] Z. Jin, Y. Chen, F. Leeb, L. Gresele, O. Kamal, L. Zhiheng, K. Blin, F. G. Adauto, M. Kleiman-Weiner, M. Sachan _et al._ , “Cladder: Assessing causal reasoning in language models,” in _Thirty-seventh conference on neural information processing systems_ , 2023. 

- [410] L. Zhang, X. Zhai, Z. Zhao, Y. Zong, X. Wen, and B. Zhao, “What if the tv was off? examining counterfactual reasoning abilities of multi-modal language models,” in _Proceedings of the IEEE/CVF_ 

_Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 21 853–21 862. 

- [411] J. Zhang, H. Zhang, W. Su, and D. Roth, “Rock: Causal inference principles for reasoning about commonsense causality,” in _International Conference on Machine Learning_ . PMLR, 2022, pp. 26 750–26 771. 

- [412] A. Feder, Y. Wald, C. Shi, S. Saria, and D. Blei, “Causal-structure driven augmentations for text ood generalization,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [413] X. Liu, D. Yin, C. Zhang, Y. Feng, and D. Zhao, “The magic of if: Investigating causal reasoning abilities in large language models of code,” _arXiv preprint arXiv:2305.19213_ , 2023. 

- [414] Z. Chen, Q. Gao, A. Bosselut, A. Sabharwal, and K. Richardson, “Disco: Distilling counterfactuals with large language models,” _arXiv preprint arXiv:2212.10534_ , 2022. 

- [415] J. Zhang, J. Jennings, A. Hilmkil, N. Pawlowski, C. Zhang, and C. Ma, “Towards causal foundation model: on duality between causal inference and attention,” _arXiv preprint arXiv:2310.00809_ , 2023. 

- [416] Y. Li, M. Xu, X. Miao, S. Zhou, and T. Qian, “Prompting large language models for counterfactual generation: An empirical study,” _arXiv preprint arXiv:2305.14791_ , 2023. 

- [417] S. Koch, “Babbling stochastic parrots? on reference and reference change in large language models,” 2023. 

- [418] A. Wu, K. Kuang, M. Zhu, Y. Wang, Y. Zheng, K. Han, B. Li, G. Chen, F. Wu, and K. Zhang, “Causality for large language models,” _arXiv preprint arXiv:2410.15319_ , 2024. 

- [419] Z. Jin, J. Liu, Z. Lyu, S. Poff, M. Sachan, R. Mihalcea, M. Diab, and B. Schölkopf, “Can large language models infer causation from correlation?” _arXiv preprint arXiv:2306.05836_ , 2023. 

- [420] L. Du, X. Ding, K. Xiong, T. Liu, and B. Qin, “e-care: a new dataset for exploring explainable causal reasoning,” _arXiv preprint arXiv:2205.05849_ , 2022. 

- [421] D. Dalal, P. Buitelaar, and M. Arcan, “Calm-bench: A multi-task benchmark for evaluating causality-aware language models,” in _Findings of the Association for Computational Linguistics: EACL 2023_ , 2023, pp. 296–311. 

- [422] A. Rawal, A. Raglin, D. B. Rawat, B. M. Sadler, and J. McCoy, “Causality for trustworthy artificial intelligence: Status, challenges and perspectives,” _ACM Computing Surveys_ , 2024. 

- [423] C. Glymour, K. Zhang, and P. Spirtes, “Review of causal discovery methods based on graphical models,” _Frontiers in genetics_ , vol. 10, p. 524, 2019. 

- [424] D. H. Jonassen, M. Yacci, and K. Beissner, _Structural knowledge: Techniques for representing, conveying, and acquiring structural knowledge_ . Routledge, 2013. 

- [425] F. J. Pinto, “Structured methods of representation of the knowledge,” in _Distributed Computing and Artificial Intelligence, Special Sessions, 15th International Conference 15_ . Springer, 2019, pp. 213– 221. 

- [426] T. Shen, Y. Mao, P. He, G. Long, A. Trischler, and W. Chen, “Exploiting structured knowledge in text via graph-guided representation learning,” _arXiv preprint arXiv:2004.14224_ , 2020. 

- [427] L. Yang, H. Chen, Z. Li, X. Ding, and X. Wu, “Chatgpt is not enough: Enhancing large language models with knowledge graphs for fact-aware language modeling,” _arXiv preprint arXiv:2306.11489_ , 2023. 

- [428] G. Yu, X. Wang, Q. Li, and Y. Zhao, “Fusing llms and kgs for formal causal reasoning behind financial risk contagion,” _arXiv preprint arXiv:2407.17190_ , 2024. 

- [429] Y. Wang, Z. Chu, X. Ouyang, S. Wang, H. Hao, Y. Shen, J. Gu, S. Xue, J. Zhang, Q. Cui _et al._ , “Llmrg: Improving recommendations through large language model reasoning graphs,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 38, no. 17, 2024, pp. 19 189–19 196. 

- [430] Y. Susanti and M. Färber, “Knowledge graph structure as prompt: improving small language models capabilities for knowledgebased causal discovery,” in _International Semantic Web Conference_ . Springer Nature Switzerland Cham, 2024, pp. 87–106. 

- [431] R. Ravi, “An exploration of causality in social media data with knowledge graphs,” 2024. 

- [432] F. Elwert, “Graphical causal models,” in _Handbook of causal analysis for social research_ . Springer, 2013, pp. 245–273. 

- [433] D. Cheng, J. Li, L. Liu, J. Liu, and T. D. Le, “Data-driven causal effect estimation based on graphical causal modelling: A survey,” _ACM Computing Surveys_ , vol. 56, no. 5, pp. 1–37, 2024. 

37 

- [434] Z. Li, X. Ding, K. Liao, B. Qin, and T. Liu, “Causalbert: Injecting causal knowledge into pre-trained models with minimal supervision,” _arXiv preprint arXiv:2107.09852_ , 2021. 

- [435] N. R. Ke, O. Bilaniuk, A. Goyal, S. Bauer, H. Larochelle, B. Schölkopf, M. C. Mozer, C. Pal, and Y. Bengio, “Learning neural causal models from unknown interventions,” _arXiv preprint arXiv:1910.01075_ , 2019. 

- [436] V. Khetan, R. Ramnani, M. Anand, S. Sengupta, and A. E. Fano, “Causal bert: Language models for causality detection between events expressed in text,” in _Intelligent Computing: Proceedings of the 2021 Computing Conference, Volume 1_ . Springer, 2022, pp. 965–980. 

- [437] K. Wang, X. Zhang, H. Liu, S. Han, H. Ma, and T. Hu, “Credes: Causal reasoning enhancement and dual-end searching for solving long-range reasoning problems using llms,” _arXiv preprint arXiv:2410.01696_ , 2024. 

- [438] C. Samarajeewa, D. De Silva, E. Osipov, D. Alahakoon, and M. Manic, “Causal reasoning in large language models using causal graph retrieval augmented generation,” in _2024 16th International Conference on Human System Interaction (HSI)_ . IEEE, 2024, pp. 1–6. 

- [439] P. Li, X. Wang, Z. Zhang, Y. Meng, F. Shen, Y. Li, J. Wang, Y. Li, and W. Zhu, “Realtcd: Temporal causal discovery from interventional data with large language model,” in _Proceedings of the 33rd ACM International Conference on Information and Knowledge Management_ , 2024, pp. 4669–4677. 

- [440] T. Ban, L. Chen, X. Wang, and H. Chen, “From query tools to causal architects: Harnessing large language models for advanced causal discovery from data,” _arXiv preprint arXiv:2306.16902_ , 2023. 

- [441] C. Liu, Y. Chen, T. Liu, M. Gong, J. Cheng, B. Han, and K. Zhang, “Discovery of the hidden world with large language models,” _arXiv preprint arXiv:2402.03941_ , 2024. 

- [442] V.-A. Darvariu, S. Hailes, and M. Musolesi, “Large language models are effective priors for causal graph discovery,” _arXiv preprint arXiv:2405.13551_ , 2024. 

- [443] I. Sheth, S. Abdelnabi, and M. Fritz, “Hypothesizing missing causal variables with llms,” _arXiv preprint arXiv:2409.02604_ , 2024. 

- [444] E. Goldvarg and P. N. Johnson-Laird, “Naive causality: A mental model theory of causal meaning and reasoning,” _Cognitive science_ , vol. 25, no. 4, pp. 565–610, 2001. 

- [445] A. Hafri and C. Firestone, “The perception of relations,” _Trends in Cognitive Sciences_ , vol. 25, no. 6, pp. 475–492, 2021. 

- [446] F. Baradel, N. Neverova, J. Mille, G. Mori, and C. Wolf, “Cophy: Counterfactual learning of physical dynamics,” _arXiv preprint arXiv:1909.12000_ , 2019. 

- [447] N. A. Jones, H. Ross, T. Lynam, P. Perez, and A. Leitch, “Mental models: an interdisciplinary synthesis of theory and methods,” _Ecology and society_ , vol. 16, no. 1, 2011. 

- [448] J. R. Kubricht, K. J. Holyoak, and H. Lu, “Intuitive physics: Current research and controversies,” _Trends in cognitive sciences_ , vol. 21, no. 10, pp. 749–759, 2017. 

- [449] A. Cherian, R. Corcodel, S. Jain, and D. Romeres, “Llmphy: Complex physical reasoning using large language models and world models,” _arXiv preprint arXiv:2411.08027_ , 2024. 

- [450] P. Zhao, N. Cheng, H. Hu, X. Zhang, X. Xu, Z. Jin, F. Meng, J. Zhou, J. Xu, and W. Han, “Bridging the reality gap: A benchmark for physical reasoning in general world models with various physical phenomena beyond mechanics.” 

- [451] O. Ahmed, F. Träuble, A. Goyal, A. Neitz, Y. Bengio, B. Schölkopf, M. Wüthrich, and S. Bauer, “Causalworld: A robotic manipulation benchmark for causal structure and transfer learning,” _arXiv preprint arXiv:2010.04296_ , 2020. 

- [452] Q. Xue, X. Yin, B. Yang, and W. Gao, “Phyt2v: Llm-guided iterative self-refinement for physics-grounded text-to-video generation,” _arXiv preprint arXiv:2412.00596_ , 2024. 

- [453] G. Gui and O. Toubia, “The challenge of using llms to simulate human behavior: A causal inference perspective,” _arXiv preprint arXiv:2312.15524_ , 2023. 

- [454] Ö. Gürcan, “Llm-augmented agent-based modelling for social simulations: Challenges and opportunities,” _HHAI 2024: Hybrid Human AI Systems for the Social Good_ , pp. 134–144, 2024. 

- [455] L. S. Piloto, A. Weinstein, P. Battaglia, and M. Botvinick, “Intuitive physics learning in a deep-learning model inspired by developmental psychology,” _Nature human behaviour_ , vol. 6, no. 9, pp. 1257–1267, 2022. 

- [456] Z. Hao, S. Liu, Y. Zhang, C. Ying, Y. Feng, H. Su, and J. Zhu, “Physics-informed machine learning: A survey on problems, methods and applications,” _arXiv preprint arXiv:2211.08064_ , 2022. 

- [457] W. Wang, L. Mao, R. Wang, and B.-C. Min, “Srlm: Humanin-loop interactive social robot navigation with large language model and deep reinforcement learning,” _arXiv preprint arXiv:2403.15648_ , 2024. 

- [458] S. Chaudhari, P. Aggarwal, V. Murahari, T. Rajpurohit, A. Kalyan, K. Narasimhan, A. Deshpande, and B. C. da Silva, “Rlhf deciphered: A critical analysis of reinforcement learning from human feedback for llms,” _arXiv preprint arXiv:2404.08555_ , 2024. 

- [459] A. R. Laleh and M. N. Ahmadabadi, “A survey on enhancing reinforcement learning in complex environments: Insights from human and llm feedback,” _arXiv preprint arXiv:2411.13410_ , 2024. 

- [460] Y.-C. Chan, G. Pu, A. Shanker, P. Suresh, P. Jenks, J. Heyer, and S. Denton, “Balancing cost and effectiveness of synthetic data generation strategies for llms,” _arXiv preprint arXiv:2409.19759_ , 2024. 

- [461] J. Tremblay, A. Prakash, D. Acuna, M. Brophy, V. Jampani, C. Anil, T. To, E. Cameracci, S. Boochoon, and S. Birchfield, “Training deep networks with synthetic data: Bridging the reality gap by domain randomization,” in _Proceedings of the IEEE conference on computer vision and pattern recognition workshops_ , 2018, pp. 969–977. 

- [462] R. Versace, G. T. Vallet, B. Riou, M. Lesourd, É. Labeye, and L. Brunel, “Act-in: An integrated view of memory mechanisms,” _Journal of Cognitive Psychology_ , vol. 26, no. 3, pp. 280–306, 2014. 

- [463] A. Lavin, D. Krakauer, H. Zenil, J. Gottschlich, T. Mattson, J. Brehmer, A. Anandkumar, S. Choudry, K. Rocki, A. G. Baydin _et al._ , “Simulation intelligence: Towards a new generation of scientific methods,” _arXiv preprint arXiv:2112.03235_ , 2021. 

- [464] Y. Guo, M. Liu, T. Yang, and T. Rosing, “Improved schemes for episodic memory-based lifelong learning,” _Advances in Neural Information Processing Systems_ , vol. 33, pp. 1023–1035, 2020. 

- [465] J. Bang, H. Kim, Y. Yoo, J.-W. Ha, and J. Choi, “Rainbow memory: Continual learning with a memory of diverse samples,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2021, pp. 8218–8227. 

- [466] D. Kudithipudi, M. Aguilar-Simon, J. Babb, M. Bazhenov, D. Blackiston, J. Bongard, A. P. Brna, S. Chakravarthi Raja, N. Cheney, J. Clune _et al._ , “Biological underpinnings for lifelong learning machines,” _Nature Machine Intelligence_ , vol. 4, no. 3, pp. 196–210, 2022. 

- [467] Z. Zhang, Q. Dai, L. Chen, Z. Jiang, R. Li, J. Zhu, X. Chen, Y. Xie, Z. Dong, and J.-R. Wen, “Memsim: A bayesian simulator for evaluating memory of llm-based personal assistants,” _arXiv preprint arXiv:2409.20163_ , 2024. 

- [468] P. Anokhin, N. Semenov, A. Sorokin, D. Evseev, M. Burtsev, and E. Burnaev, “Arigraph: Learning knowledge graph world models with episodic memory for llm agents,” _arXiv preprint arXiv:2407.04363_ , 2024. 

- [469] N. A. Taatgen, “Cognitive architectures: innate or learned?” in _2017 aaai fall symposium series_ , 2017. 

- [470] P. Griffiths and S. Linquist, “The distinction between innate and acquired characteristics,” 2009. 

- [471] C. Feng, X. Zhang, and Z. Fei, “Knowledge solver: Teaching llms to search for domain knowledge from knowledge graphs,” _arXiv preprint arXiv:2309.03118_ , 2023. 

- [472] M. Li, H. Yang, Z. Liu, M. M. Alam, H. Sack, G. A. Gesese _et al._ , “Kgmistral: Towards boosting the performance of large language models for question answering with knowledge graph integration,” in _Workshop on Deep Learning and Large Language Models for Knowledge Graphs_ , 2024. 

- [473] A. Bendiken, “Know: A real-world ontology for knowledge capture with large language models,” _arXiv preprint arXiv:2405.19877_ , 2024. 

- [474] D. Allemang and J. Sequeda, “Increasing the llm accuracy for question answering: Ontologies to the rescue!” _arXiv preprint arXiv:2405.11706_ , 2024. 

- [475] I. Dasgupta and S. J. Gershman, “Memory as a computational resource,” _Trends in cognitive sciences_ , vol. 25, no. 3, pp. 240–251, 2021. 

- [476] P. Bordalo, J. J. Conlon, N. Gennaioli, S. Y. Kwon, and A. Shleifer, “Memory and probability,” _The Quarterly Journal of Economics_ , vol. 138, no. 1, pp. 265–311, 2023. 

- [477] M. B. Ganapini, M. Campbell, F. Fabiano, L. Horesh, J. Lenchner, A. Loreggia, N. Mattei, F. Rossi, B. Srivastava, and K. B. Venable, 

38 

- “Thinking fast and slow in ai: The role of metacognition,” in _International Conference on Machine Learning, Optimization, and Data Science_ . Springer, 2022, pp. 502–509. 

- [478] N. Spivack, S. Douglas, M. Crames, and T. Connors, “Cognition is all you need-the next layer of ai above large language models,” _arXiv preprint arXiv:2403.02164_ , 2024. 

- [479] A. Langdon, M. Botvinick, H. Nakahara, K. Tanaka, M. Matsumoto, and R. Kanai, “Meta-learning, social cognition and consciousness in brains and machines,” _Neural Networks_ , vol. 145, pp. 80–89, 2022. 

- [480] I. J. Goodfellow, M. Mirza, D. Xiao, A. Courville, and Y. Bengio, “An empirical investigation of catastrophic forgetting in gradient-based neural networks,” _arXiv preprint arXiv:1312.6211_ , 2013. 

- [481] D. M. Ziegler, N. Stiennon, J. Wu, T. B. Brown, A. Radford, D. Amodei, P. Christiano, and G. Irving, “Fine-tuning language models from human preferences,” _arXiv preprint arXiv:1909.08593_ , 2019. 

- [482] A. Aghajanyan, A. Shrivastava, A. Gupta, N. Goyal, L. Zettlemoyer, and S. Gupta, “Better fine-tuning by reducing representational collapse,” _arXiv preprint arXiv:2008.03156_ , 2020. 

- [483] J. Kirkpatrick, R. Pascanu, N. Rabinowitz, J. Veness, G. Desjardins, A. A. Rusu, K. Milan, J. Quan, T. Ramalho, A. GrabskaBarwinska _et al._ , “Overcoming catastrophic forgetting in neural networks,” _Proceedings of the national academy of sciences_ , vol. 114, no. 13, pp. 3521–3526, 2017. 

- [484] T. Tadros, G. P. Krishnan, R. Ramyaa, and M. Bazhenov, “Sleeplike unsupervised replay reduces catastrophic forgetting in artificial neural networks,” _Nature communications_ , vol. 13, no. 1, p. 7742, 2022. 

- [485] R. Figueroa, “Evaluating adaptive layer freezing through hyperparameter optimization for enhanced fine-tuning performance of language models,” Ph.D. dissertation, Massachusetts Institute of Technology, 2024. 

- [486] Y. Wang, M. Chen, N. Peng, and K.-W. Chang, “Deepedit: Knowledge editing as decoding with constraints,” _arXiv preprint arXiv:2401.10471_ , 2024. 

- [487] Z. Zhong, Z. Wu, C. D. Manning, C. Potts, and D. Chen, “Mquake: Assessing knowledge editing in language models via multi-hop questions,” _arXiv preprint arXiv:2305.14795_ , 2023. 

- [488] N. Zhang, Y. Yao, B. Tian, P. Wang, S. Deng, M. Wang, Z. Xi, S. Mao, J. Zhang, Y. Ni _et al._ , “A comprehensive study of knowledge editing for large language models,” _arXiv preprint arXiv:2401.01286_ , 2024. 

- [489] R. M. Schmidt, “Recurrent neural networks (rnns): A gentle introduction and overview,” _arXiv preprint arXiv:1912.05911_ , 2019. 

- [490] V. Mnih, N. Heess, A. Graves _et al._ , “Recurrent models of visual attention,” _Advances in neural information processing systems_ , vol. 27, 2014. 

- [491] A. Graves and A. Graves, “Long short-term memory,” _Supervised sequence labelling with recurrent neural networks_ , pp. 37–45, 2012. 

- [492] G. Van Houdt, C. Mosquera, and G. Nápoles, “A review on the long short-term memory model,” _Artificial Intelligence Review_ , vol. 53, no. 8, pp. 5929–5955, 2020. 

- [493] R. Dey and F. M. Salem, “Gate-variants of gated recurrent unit (gru) neural networks,” in _2017 IEEE 60th international midwest symposium on circuits and systems (MWSCAS)_ . IEEE, 2017, pp. 1597–1600. 

- [494] K. Hatalis, D. Christou, J. Myers, S. Jones, K. Lambert, A. AmosBinks, Z. Dannenhauer, and D. Dannenhauer, “Memory matters: The need to improve long-term memory in llm-agents,” in _Proceedings of the AAAI Symposium Series_ , vol. 2, no. 1, 2023, pp. 277– 280. 

- [495] A. Peysakhovich and A. Lerer, “Attention sorting combats recency bias in long context language models,” _arXiv preprint arXiv:2310.01427_ , 2023. 

- [496] C.-Y. Hsieh, Y.-S. Chuang, C.-L. Li, Z. Wang, L. T. Le, A. Kumar, J. Glass, A. Ratner, C.-Y. Lee, R. Krishna _et al._ , “Found in the middle: Calibrating positional attention bias improves long context utilization,” _arXiv preprint arXiv:2406.16008_ , 2024. 

- [497] N. F. Liu, K. Lin, J. Hewitt, A. Paranjape, M. Bevilacqua, F. Petroni, and P. Liang, “Lost in the middle: How language models use long contexts,” _Transactions of the Association for Computational Linguistics_ , vol. 12, pp. 157–173, 2024. 

- [498] A. Maharana, D.-H. Lee, S. Tulyakov, M. Bansal, F. Barbieri, and Y. Fang, “Evaluating very long-term conversational memory of llm agents,” _arXiv preprint arXiv:2402.17753_ , 2024. 

- [499] Y. Hou, H. Tamoto, and H. Miyashita, “" my agent understands me better": Integrating dynamic human-like memory recall and consolidation in llm-based agents,” in _Extended Abstracts of the CHI Conference on Human Factors in Computing Systems_ , 2024, pp. 1–7. 

- [500] Z. Wang, B. Yu, J. Zhao, W. Sun, S. Hou, S. Liang, X. Hu, Y. Han, and Y. Gan, “Karma: Augmenting embodied ai agents with long-and-short term memory systems,” _arXiv preprint arXiv:2409.14908_ , 2024. 

- [501] Z. Yin, Q. Sun, Q. Guo, Z. Zeng, Q. Cheng, X. Qiu, and X.-J. Huang, “Explicit memory learning with expectation maximization,” in _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ , 2024, pp. 16 618–16 635. 

- [502] D. Wu, H. Wang, W. Yu, Y. Zhang, K.-W. Chang, and D. Yu, “Longmemeval: Benchmarking chat assistants on long-term interactive memory,” _arXiv preprint arXiv:2410.10813_ , 2024. 

- [503] Z. Zhang, X. Bo, C. Ma, R. Li, X. Chen, Q. Dai, J. Zhu, Z. Dong, and J.-R. Wen, “A survey on the memory mechanism of large language model based agents,” _arXiv preprint arXiv:2404.13501_ , 2024. 

- [504] C. Packer, S. Wooders, K. Lin, V. Fang, S. G. Patil, I. Stoica, and J. E. Gonzalez, “Memgpt: Towards llms as operating systems,” _arXiv preprint arXiv:2310.08560_ , 2023. 

- [505] C. Hu, J. Fu, C. Du, S. Luo, J. Zhao, and H. Zhao, “Chatdb: Augmenting llms with databases as their symbolic memory,” _arXiv preprint arXiv:2306.03901_ , 2023. 

- [506] L. Liu, X. Yang, Y. Shen, B. Hu, Z. Zhang, J. Gu, and G. Zhang, “Think-in-memory: Recalling and post-thinking enable llms with long-term memory,” _arXiv preprint arXiv:2311.08719_ , 2023. 

- [507] Z. Qin, C. Luo, Z. Wang, H. Jiang, and Y. Sun, “Relational database augmented large language model,” _arXiv preprint arXiv:2407.15071_ , 2024. 

- [508] J. Jiang, K. Zhou, Z. Dong, K. Ye, W. X. Zhao, and J.-R. Wen, “Structgpt: A general framework for large language model to reason over structured data,” _arXiv preprint arXiv:2305.09645_ , 2023. 

- [509] L. Patel, S. Jha, C. Guestrin, and M. Zaharia, “Lotus: Enabling semantic queries with llms over tables of unstructured and structured data,” _arXiv preprint arXiv:2407.11418_ , 2024. 

- [510] L. Wen, D. Fu, X. Li, X. Cai, T. Ma, P. Cai, M. Dou, B. Shi, L. He, and Y. Qiao, “Dilu: A knowledge-driven approach to autonomous driving with large language models,” _arXiv preprint arXiv:2309.16292_ , 2023. 

- [511] Y. Zhang, Z. Yu, W. Jiang, Y. Shen, and J. Li, “Long-term memory for large language models through topic-based vector database,” in _2023 International Conference on Asian Language Processing (IALP)_ . IEEE, 2023, pp. 258–264. 

- [512] Z. Jing, Y. Su, Y. Han, B. Yuan, H. Xu, C. Liu, K. Chen, and M. Zhang, “When large language models meet vector databases: A survey,” _arXiv preprint arXiv:2402.01763_ , 2024. 

- [513] Y. Han, C. Liu, and P. Wang, “A comprehensive survey on vector database: Storage and retrieval technique, challenge,” _arXiv preprint arXiv:2310.11703_ , 2023. 

- [514] T. Schmied, F. Paischer, V. Patil, M. Hofmarcher, R. Pascanu, and S. Hochreiter, “Retrieval-augmented decision transformer: External memory for in-context rl,” _arXiv preprint arXiv:2410.07071_ , 2024. 

- [515] S. Wu, Y. Xiong, Y. Cui, H. Wu, C. Chen, Y. Yuan, L. Huang, X. Liu, T.-W. Kuo, N. Guan _et al._ , “Retrieval-augmented generation for natural language processing: A survey,” _arXiv preprint arXiv:2407.13193_ , 2024. 

- [516] H. Li, Y. Su, D. Cai, Y. Wang, and L. Liu, “A survey on retrievalaugmented text generation,” _arXiv preprint arXiv:2202.01110_ , 2022. 

- [517] H. Ali, P. Allgeuer, C. Mazzola, G. Belgiovine, B. C. Kaplan, L. Gajdošech, and S. Wermter, “Robots can multitask too: Integrating a memory architecture and llms for enhanced crosstask robot action generation,” in _2024 IEEE-RAS 23rd International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2024, pp. 811– 818. 

- [518] F. Minnella, J. Cortadella, M. R. Casu, M. T. Lazarescu, and L. Lavagno, “Mix & latch: An optimization flow for highperformance designs with single-clock mixed-polarity latches and flip-flops,” _IEEE access_ , vol. 11, pp. 35 830–35 840, 2023. 

- [519] P. Meaney, A. Mishra, and R. Rao, “Synchronous, low-latency, offmodule interface for the ibm z16 telum® processor,” _IEEE Micro_ , 2024. 

39 

- [520] F. Grötschla, G. L. Miotto, and R. Sipos, “Design of a request/response buffering application for i/o intensive workloads,” in _Journal of Physics: Conference Series_ , vol. 2438, no. 1. IOP Publishing, 2023, p. 012025. 

- [521] V. Leis, A. Alhomssi, T. Ziegler, Y. Loeck, and C. Dietrich, “Virtual-memory assisted buffer management,” _Proceedings of the ACM on Management of Data_ , vol. 1, no. 1, pp. 1–25, 2023. 

- [522] C. Wan, P. Cai, M. Wang, Y. Qian, W. Huang, and X. Chen, “Artificial sensory memory,” _Advanced Materials_ , vol. 32, no. 15, p. 1902434, 2020. 

- [523] X. Ji, Z. Dong, Y. Han, C. S. Lai, and D. Qi, “A brain-inspired hierarchical interactive in-memory computing system and its application in video sentiment analysis,” _IEEE transactions on circuits and systems for video technology_ , vol. 33, no. 12, pp. 7928– 7942, 2023. 

- [524] J. Lu, S. An, M. Lin, G. Pergola, Y. He, D. Yin, X. Sun, and Y. Wu, “Memochat: Tuning llms to use memos for consistent long-range open-domain conversation,” _arXiv preprint arXiv:2308.08239_ , 2023. 

- [525] J. S. Park, J. O’Brien, C. J. Cai, M. R. Morris, P. Liang, and M. S. Bernstein, “Generative agents: Interactive simulacra of human behavior,” in _Proceedings of the 36th annual acm symposium on user interface software and technology_ , 2023, pp. 1–22. 

- [526] G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan, and A. Anandkumar, “Voyager: An open-ended embodied agent with large language models,” _arXiv preprint arXiv:2305.16291_ , 2023. 

- [527] N. C. Waugh and D. A. Norman, “Primary memory.” _Psychological review_ , vol. 72, no. 2, p. 89, 1965. 

- [528] A. Baddeley, “Working memory,” _Science_ , vol. 255, no. 5044, pp. 556–559, 1992. 

- [529] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, “Reflexion: Language agents with verbal reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [530] H. Chen, R. Pasunuru, J. Weston, and A. Celikyilmaz, “Walking down the memory maze: Beyond context limit through interactive reading,” _arXiv preprint arXiv:2310.05029_ , 2023. 

- [531] M. Li, S. Zhang, Y. Liu, and K. Chen, “Needlebench: Can llms do retrieval and reasoning in 1 million context window?” _arXiv preprint arXiv:2407.11963_ , 2024. 

- [532] C. Xiao, P. Zhang, X. Han, G. Xiao, Y. Lin, Z. Zhang, Z. Liu, and M. Sun, “Inf **l** m: Training-free long-context extrapolation for llms with an efficient context memory,” in _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ , 2024. 

- [533] T. Chang, S.-H. Jo, and W. Lu, “Short-term memory to long-term memory transition in a nanoscale memristor,” _ACS nano_ , vol. 5, no. 9, pp. 7669–7676, 2011. 

- [534] A. Baddeley, C. Papagno, and G. Vallar, “When long-term learning depends on short-term storage,” _Journal of memory and language_ , vol. 27, no. 5, pp. 586–595, 1988. 

- [535] K. A. Ericsson and W. Kintsch, “Long-term working memory.” _Psychological review_ , vol. 102, no. 2, p. 211, 1995. 

- [536] P. Bekinschtein, M. Cammarota, C. Katche, L. Slipczuk, J. I. Rossato, A. Goldin, I. Izquierdo, and J. H. Medina, “Bdnf is essential to promote persistence of long-term memory storage,” _Proceedings of the National Academy of Sciences_ , vol. 105, no. 7, pp. 2711–2716, 2008. 

- [537] D. C. Park, A. D. Smith, G. Lautenschlager, J. L. Earles, D. Frieske, M. Zwahr, and C. L. Gaines, “Mediators of long-term memory performance across the life span.” _Psychology and aging_ , vol. 11, no. 4, p. 621, 1996. 

- [538] O. Hardt, K. Nader, and L. Nadel, “Decay happens: the role of active forgetting in memory,” _Trends in cognitive sciences_ , vol. 17, no. 3, pp. 111–120, 2013. 

- [539] G. Winocur, M. Moscovitch, and B. Bontempi, “Memory formation and long-term retention in humans and animals: Convergence towards a transformation account of hippocampal– neocortical interactions,” _Neuropsychologia_ , vol. 48, no. 8, pp. 2339–2356, 2010. 

- [540] A. Modarressi, A. Köksal, A. Imani, M. Fayyaz, and H. Schütze, “Memllm: Finetuning llms to use an explicit read-write memory,” _arXiv preprint arXiv:2404.11672_ , 2024. 

- [541] K. D. Yamada, “Developing appendable memory system towards permanent memory for artificial intelligence to acquire new knowledge after deployment,” _bioRxiv_ , pp. 2023–05, 2023. 

- [542] M. T. Ullman, “A neurocognitive perspective on language: The declarative/procedural model,” _Nature reviews neuroscience_ , vol. 2, no. 10, pp. 717–726, 2001. 

- [543] B. J. Gutiérrez, Y. Shu, Y. Gu, M. Yasunaga, and Y. Su, “Hipporag: Neurobiologically inspired long-term memory for large language models,” _arXiv preprint arXiv:2405.14831_ , 2024. 

- [544] M. Geva, R. Schuster, J. Berant, and O. Levy, “Transformer feed-forward layers are key-value memories,” _arXiv preprint arXiv:2012.14913_ , 2020. 

- [545] Z. Fountas, M. A. Benfeghoul, A. Oomerjee, F. Christopoulou, G. Lampouras, H. Bou-Ammar, and J. Wang, “Human-like episodic memory for infinite context llms,” _arXiv preprint arXiv:2407.09450_ , 2024. 

- [546] L. Bärmann, C. DeChant, J. Plewnia, F. Peller-Konrad, D. Bauer, T. Asfour, and A. Waibel, “Episodic memory verbalization using hierarchical representations of life-long robot experience,” _arXiv preprint arXiv:2409.17702_ , 2024. 

- [547] H. Aktas and E. Ugur, “Vq-cnmp: Neuro-symbolic skill learning for bi-level planning,” _arXiv preprint arXiv:2410.10045_ , 2024. 

- [548] H. Eichenbaum, “Declarative memory: Insights from cognitive neurobiology,” _Annual review of psychology_ , vol. 48, no. 1, pp. 547– 572, 1997. 

- [549] ——, “The hippocampus and mechanisms of declarative memory,” _Behavioural brain research_ , vol. 103, no. 2, pp. 123–133, 1999. 

- [550] B. Wang, T. Sun, H. Yan, S. Wang, Q. Cheng, and X. Qiu, “Inmemory learning: A declarative learning framework for large language models,” _arXiv preprint arXiv:2403.02757_ , 2024. 

- [551] E. Tulving and H. J. Markowitsch, “Episodic and declarative memory: role of the hippocampus,” _Hippocampus_ , vol. 8, no. 3, pp. 198–204, 1998. 

- [552] Y. Xiao, E. Sun, T. Liu, and W. Wang, “Logicvista: Multimodal llm logical reasoning benchmark in visual contexts,” _arXiv preprint arXiv:2407.04973_ , 2024. 

- [553] Z. Li, Y. Cao, X. Xu, J. Jiang, X. Liu, Y. S. Teo, S.-W. Lin, and Y. Liu, “Llms for relational reasoning: How far are we?” in _Proceedings of the 1st International Workshop on Large Language Models for Code_ , 2024, pp. 119–126. 

- [554] Z. Shao, Z. Yu, M. Wang, and J. Yu, “Prompting large language models with answer heuristics for knowledge-based visual question answering,” in _Proceedings of the IEEE/CVF Conference on computer vision and pattern recognition_ , 2023, pp. 14 974–14 983. 

- [555] S. Zheng, “An systematic evaluation on leading large language models and their factuality investigation as question answering systems,” Ph.D. dissertation, University of Illinois at UrbanaChampaign, 2024. 

- [556] M. Saeed, N. Ahmadi, P. Nakov, and P. Papotti, “Rulebert: Teaching soft rules to pre-trained language models,” _arXiv preprint arXiv:2109.13006_ , 2021. 

- [557] S. Zhou, T. Zhou, Y. Yang, G. Long, D. Ye, J. Jiang, and C. Zhang, “Wall-e: World alignment by rule learning improves world model-based llm agents,” _arXiv preprint arXiv:2410.07484_ , 2024. 

- [558] W. Sun, C. Zhang, X. Zhang, Z. Huang, H. Xu, P. Chen, S. He, J. Zhao, and K. Liu, “Beyond instruction following: Evaluating rule following of large language models,” _arXiv e-prints_ , pp. arXiv–2407, 2024. 

- [559] Y. Hu, K. Song, S. Cho, X. Wang, H. Foroosh, D. Yu, and F. Liu, “Can large language models do analytical reasoning?” _arXiv preprint arXiv:2403.04031_ , 2024. 

- [560] J. Jiang, K. Zhou, W. X. Zhao, Y. Song, C. Zhu, H. Zhu, and J.R. Wen, “Kg-agent: An efficient autonomous agent framework for complex reasoning over knowledge graph,” _arXiv preprint arXiv:2402.11163_ , 2024. 

- [561] E. Tulving, “Episodic and semantic memory, in organization of memory,” _(No Title)_ , p. 381, 1972. 

- [562] D. L. Schacter, “Implicit memory: History and current status.” _Journal of experimental psychology: learning, memory, and cognition_ , vol. 13, no. 3, p. 501, 1987. 

- [563] ——, “Priming and multiple memory systems: Perceptual mechanisms of implicit memory,” _Journal of cognitive neuroscience_ , vol. 4, no. 3, pp. 244–256, 1992. 

- [564] L. S. Hopkins, D. H. Schultz, D. E. Hannula, and F. J. Helmstetter, “Eye movements index implicit memory expression in fear conditioning,” _PLoS One_ , vol. 10, no. 11, p. e0141949, 2015. 

- [565] P. Spataro, C. Rossi-Arnaud, N. W. Mulligan _et al._ , “Implicit versus explicit memory,” in _Learning and memory: A comprehensive reference_ . Elsevier Inc., 2017, pp. 71–86. 

40 

- [566] R. Mon-Williams, G. Li, R. Long, W. Du, and C. Lucas, “Robotic embodied intelligence: Integrating language models, curated knowledge, and multimodal feedback for complex task success,” 2024. 

- [567] M. Kwon, Y. Kim, and Y. J. Kim, “Fast and accurate task planning using neuro-symbolic language models and multi-level goal decomposition,” _arXiv preprint arXiv:2409.19250_ , 2024. 

- [568] X. Li, L. Zhao, L. Zhang, Z. Wu, Z. Liu, H. Jiang, C. Cao, S. Xu, Y. Li, H. Dai _et al._ , “Artificial general intelligence for medical imaging analysis,” _IEEE Reviews in Biomedical Engineering_ , 2024. 

- [569] P. P. Ray, “Chatgpt: A comprehensive review on background, applications, key challenges, bias, ethics, limitations and future scope,” _Internet of Things and Cyber-Physical Systems_ , vol. 3, pp. 121–154, 2023. 

- [570] L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen, W. Peng, X. Feng, B. Qin _et al._ , “A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions,” _ACM Transactions on Information Systems_ , 2023. 

