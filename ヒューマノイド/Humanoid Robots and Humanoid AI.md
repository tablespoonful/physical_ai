---
title: "Humanoid Robots and Humanoid AI: Review, Perspectives and Directions"
date: "2024-03-19"
authors: "Longbing Cao"
url: https://arxiv.org/abs/2405.15775
pdf: https://arxiv.org/pdf/2405.15775
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2405.15775)** / [論文ページ](https://arxiv.org/abs/2405.15775)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Humanoid Robots and Humanoid AI: Review, Perspectives and Directions** 

# LONGBING CAO, Frontier AI Research Centre, Macquarie University, Australia 

In the approximately century-long journey of robotics, humanoid robots made their debut around six decades ago. While current humanoids bear human-like appearances, none have embodied true humaneness, remaining distant from achieving human-like to human-level intelligence. The rapid recent advancements in generative AI and (multimodal) large language models have further reignited and escalated interest in humanoids towards real-time, interactive, and multimodal designs and applications, such as fostering humanoid workers, advisers, educators, medical professionals, caregivers, and receptionists. These unveil boundless opportunities of transforming 1) AI robotics into a research era of _humanoid AI_ , and 2) AI robots into new-generation _humanoid AI robots_ (AI humanoids). Our unique and comprehensive review of about 30 reported humanoids discloses a systematic terminology and a paradigmatic landscape of human-looking to human-like and human-level humanoids. It inspires comprehensive new perspectives and directions of humanoid AI as an area: transitioning from human-looking to humane humanoids, humanizing humanoids with functional and nonfunctional specifications, and cultivating technical and actionable advances of AI humanoids. Humanoid AI and AI humanoids nurture symbiotic advancements and future opportunities of synthesizing and transforming humanity modeling and conventional, generative to human-level AI into humanoid robotics. 

CCS Concepts: • **Computing methodologies** → **Artificial intelligence** . 

Additional Key Words and Phrases: AI Robots, Humanoid Robots, AI Humanoids, Humanoid AI, Generative AI, Human-level AI, Large Language Models, Multimodal Large Language Models, Humane Humanoids, Human-like Humanoids, Humanity 

#### **ACM Reference Format:** 

Longbing Cao. 2024. Humanoid Robots and Humanoid AI: Review, Perspectives and Directions. _ACM Comput. Surv._ 0, 0, Article 0 ( 2024), 35 pages. https://doi.org/XXXXXXX.XXXXXXX 

## **1 Introduction** 

In the rich history of robot development spanning a century [25], _humanoid robots_ emerged approximately 60 years ago as a groundbreaking advancement characterizing robots with anthropomorphic forms and appearance [87], forming _humanlooking humanoids_ with some of human structures and appearances. It wasn’t until about 30 years ago that humanoid robots began to exhibit notable human-like senses, behaviors, functions, interactions, or reasoning [40, 79]. This leverages the development of _AI robotics_ [56], fostering the first generation of AI humanoid robots (or humanoid AI robots, simply _AI humanoids_ for short) incorporated with (specific, predefined) capabilities of artificial narrow intelligence (ANI). Such early-stage AI humanoids, like Atlas, Geminoid [37], Pepper and Sophia, were propelled by specific techniques of pattern recognition, computer vision, natural language processing (NLP), signal processing, or shallow machine learning, enabling robot perception, conversation, interaction, collaboration, navigation, or teleoperation. These AI humanoids are typically featured by high-level coarse anthropomorphic structures (e.g. Pepper) with few characterized 

Author’s address: Longbing Cao, Frontier AI Research Centre, Macquarie University, Sydney, NSW, Australia. 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. © 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM. Manuscript submitted to ACM Manuscript submitted to ACM 1 

Cao 

2 

by static human appearance (like Geminoid and Sophia). They are empowered by on-robot, predefined, unimodal or specific tasks, rules, mechanisms, and functions for given, design-time and pretrained settings and environments. These also triggered a new area — _humanoid AI_ , marking the dawn of exploratory integration of AI developments into humanoid robotics. 

The recent rapid advancements in deep learning, generative AI (GenAI), artificial general intelligence (AGI), and human-level AI [33], particularly by (multimodal) large language models (LLMs, MLLMs) [52], have substantially transformed the area of humanoid AI and the developments of AI humanoids. _Human-like AI humanoids_ emerge as AI robots integrated by not only human-looking appearances and structures but also human-like behaviors, facial expressions and even other human qualities, particularly realtime decision-making. AI humanoids, such as the lifelike Ameca [29], while only a few, have witnessed remarkable progress, showcasing exceptional performance across various aspects and applications [85]. 

Underpinning AI humanoids is the disciplinary convergence of GenAI, AGI and human-level AI with humanoid robotics, reshaping the area of humanoid AI. _Humanoid AI_ migrates into a symbiotic field synthesizing disciplines and areas including robotics, AI, human science, and social science. It transforms AI robots into AI humanoids that are characterized by human-looking and -like structures and functions and are empowered with intelligent capabilities of undertaking both trained and sophisticated untrained tasks at either design or run time and in either static or dynamic settings. Humanoid AI boosts the development of humanoids with multimodal, multilevel, multitask, multiaspect and multipurpose machine intelligence and task capabilities of integrating perception, recognition, conversation, interaction, and operations. Examples of such AI humanoids include Ameca, Phoenix, Optimus, H1, GR-1 and Figure 01 and nonhumanoid robot Google Robot Transformer (RT2). 

Humanoid AI is reshaping the landscape of not only robotics and humanoids but also the intelligent digital economy, societies, and cultures at an unprecedented pace. The rapid developments and evolution of AI humanoids are particularly driven by commercial ambitions, strategies, policies, technology transformation, and investment from government, traditional manufacturing companies, and technology leaders. Projections suggest a substantial growth trajectory of humanoid robots, with the market size of humanoid robots anticipated to reach USD$38 billion or even USD$243 billion by 2035, boasting a staggering compound annual growth rate of 13.8-50% per year according to different market analysts. Meanwhile, GenAI commands an even larger market value, estimated at USD$2.6-4.4 trillion annually, with a projected 7% increase in global GDP<sup>1</sup> . 

Despite these promising projections and fast-paced developments, only a limited number of AI humanoids are empowered by LLMs or GenAI, and none actually hold human-level AI and human intelligence like humanity. This discrepancy is attributed not only to the so-called “uncanny valley effect” [54] but more fundamentally to the “humanoid humanity dilemma” (or more broadly, machine humanity dilemma). _Humanoid humanity dilemma_ refers to the plight of empowering human-looking humanoids with realistic to natural humanness. Both the uncanny valley effect and the humanoid humanity dilemma highlight significant untapped potential and significant gaps within the realm of humanoid AI, particularly in the foundation and design of realistic humanoids. Accordingly, discussion and speculation about the future trajectory of humanoid AI have to answer a foundational question: _What does the evolution and future hold for AI humanoids_ ? This has been intensified over the rapid evolution from ANI to AGI or even artificial superintelligence (ASI) [83] as well as other specialties including metaverse and decentralized AI [15, 48]. 

1) How will GenAI and AGI propel the evolution of humanoids? 

> 1Databricks. The great acceleration: CIO perspectives on generative AI, MIT Technology Review Insights, 2023. Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

3 

- 2) In what ways will human-level AI redefine the capabilities of humanoids towards human-level robots with human intelligence? 

- 3) How can human cognitive and social features be seamlessly incorporated into physically human-looking robots to enable humane humanoids? 

- 4) How will integrating GenAI, AGI, human science and social science into humanoids set apart humane humanoids from human-looking robots? 

- 5) With the advancements in metaverse and decentralized AI, how will humanoid AI integrate computing, learning and services over robot-edge-cloud and metaverse integrative virtual-real-mixed humanoids? 

Humanoid AI addressing these issues overturns the current emphasis on constructing humanoid robots with humanlike appearances falling short of achieving AGI. To bridge this gap, the integration, simulation, and implementation of human-level AI and human-like intelligence into humanoids will usher in new eras of human-like and ultimately human-level humanoids. Yet, the development of human-like to human-level humanoids must not only replicate human physical, cognitive, and social attributes but also address ethical, legal, and social concerns and challenges relating to humanity. This suggests _humane humanoids_ and humanoid humanity, replicating or simulating human systems, intelligence, quality and humaneness and can accomplish tasks humanly. This requires a revolutionary methodology to drive humanoid AI, such as metasynthetic intelligence and metasynthetic intelligent systems [12], and suggests a human-AI-robotics-web-integrative ecosystem of humanoid AI. Going beyond review alone, this motivates our critical and visionary perspectives on 

- 1) delineating the comprehensive landscape of humanoid robots from those possessing human appearances to early-stage AI humanoids with limited ANI functions and then more realistic AI humanoids driven by GenAI and AGI; 

- 2) articulating a systematic future of humanoid AI and humanoids attaining humane, human-like, or human-level capabilities embedded with AGI or even ASI. 

- 3) fostering a disciplinary conceptual map and landscape of humanoid AI from functional to nonfunctional specifications and from technical to practical perspectives. 

With these objectives and perspectives, our approach focuses not on mechanical, electronic, or biological aspects but rather treats AI humanoids as human-like intelligent systems, with a special emphasis on soft AI-powered humanoids and broadly the area of humanoid AI. We delve into the taxonomy, potential evolution and futures of transitioning physically human-looking humanoids into human-like, and ultimately human-level humane beings, empowered by advancements in ANI, AGI, or ASI for robotics and specifically humanoids. Our reflection of existing humanoids and the big potential nurtures new perspectives and directions of a transformational journey of developing human-like to human-level humanoids. Such advanced humanoids are poised to embody omni-intelligence integrating human-like to -level AI into humanoids and extending the capabilities of humanoids with new paradigms of intelligences, ultimately progressing towards an AGI and ASI-integrated robotic ecosystem. Furthermore, we explore various functional and nonfunctional requirements for human-like to human-level humanoids, as well as techniques and future prospects in modeling deep mind of AI humanoids. We emphasize the importance of enabling and integrating humanity with physical structures of humanoids and cultivating humane humanoids interactive with other objects and humans in humane, dynamic, real-time, and interactive environments. These expect to further advance new-generation humanoids and humanoid AI as a research area. 

Manuscript submitted to ACM 

Cao 

4 


Fig. 1. Nonexclusive paradigmatic progression and landscape of human-looking to human-like and human-level humanoid AI research and AI humanoid developments, resembling human structures, senses, behaviors and functions up to humanity, and intelligence. 

## **2 Paradigms and Categorization of Humanoid AI and AI Humanoids** 

Here, we review the paradigm shift of humanoid robots from human-looking humanoids to human-like humanoids. The conceptual ecosystem of humanoid AI is then discussed. Lastly, we present a taxonomy of AI humanoids in terms of both functional and nonfunctional objectives, specifications, tasks and intelligences. 

### **2.1 Evolution of Humanoid AI and AI Humanoids** 

The existing and future humanoid AI research and AI humanoid development can be decomposed and categorized into six aspects and stages with respective focused aims and tasks of 

- 1) _humanoid structures_ : translating human structures into human-looking humanoid structures; 

- 2) _humanoid senses_ : translating human senses into human-like humanoid senses; 

- 3) _humanoid behaviors_ : translating human behaviors into human-like behaviors; 

- 4) _humanoid functions_ : translating human functions into human-like humanoid functions; 

- 5) _humanoid humanity_ : translating humanity into human-like humanoid humanity; and 

- 6) _humanoid intelligence_ : translating human intelligence into human-level humanoid intelligence, respectively. 

Fig. 1 shows the nonexclusive (with overlap) evolutionary landscape and spectrum of human-looking to human-like and human-level humanoid AI research and AI humanoid developments. First, the development of _human-looking humanoid structures_ aims to replicate human structures and makes robot appearance with _human-looking structures_ in part or in full. Typically, a _full-body human-looking humanoid robot_ is built with human body structures such as human head, neck, chest, torso, arms, hands, legs and foot. A _half-body humanoid robot_ may only have the upper part of human-looking bodies, such as head, neck, shoulder, arm or chest. A humanoid head may be humanly expressive or non-expressive. Most humanoids are incorporated with non-expressive robot heads but with actuated stereo vision, neck or hearing. Few but more modern humanoids are decorated with lifelike expressive android heads, such as with facially expressive traits, artificial skins, neck, or hair. 

Second, the development of _human-like humanoid senses_ aims to replicate physiological and mental human senses and develop _human-like senses_ in humanoids. Accordingly, such humanoids are built with world perception and sensory modeling. Examples of human-like senses include a visual system for sight, an auditory system for audition, a gustatory system for taste, an olfactory system for smell, an external surface for feel, or cognitive components such as a brain Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

5 

with a vestibular system for balance, orientation, position, depth, and navigation. Most up-to-date humanoids are empowered with vision and audition, none has mental senses implemented. Humanoids like Ameca can express seven basic human feelings and emotions: happiness, sadness, anger, surprise, contempt, fear, and disgust. 

Third, the development of _human-like humanoid behaviors_ aims to replicate human behaviors to undertake or generate human-like behaviors or actions in humanoids. Such humanoid behaviors are programmed to humanoid body parts or learned from humans (in person or from video etc) for humanoids to simulate, infer or generate human-like actions. Typical humanoid behaviors include mimicking, inferring or transferring human eye movements, facial expression, and body postures with different hand or leg positions or movements. 

Fourth, the development of _human-like humanoid functions_ reproduces human functions of organization, responsiveness and movement in humanoids for them to perform human-like functions individually, in group, or collectively. Typical functions of the human body include speaking, singing, watching, listening, smelling, touching, feeling, grasping, dancing, walking, standing, sitting, and running, etc. These human-like functions are implemented through organizing, responding, moving or developing humanoid structures, senses, and behaviors. Most of humanoids are empowered with part of these functions. While unavailable at the moment, special purpose humanoids may even resemble human functions of metabolism, development, and reproduction. 

In addition, the development of _human-level humanoid humanity_ aims to make humanoids being humane and having _subjective human features, quality, and states_ beyond machines, fostering humanoid humanity. Such _humanoid humanity_ may include intention, consciousness, personality, trust, responsibility, preference, empathy, morality, satisfaction, accountability, and ethics. While rarely implemented on existing humanoids, humanoid humanity is essential and critical for humanoids to perform social, cultural, entertaining and industrial activities and interactions in a humane and quality manner. 

Lastly, the ultimate goal of humanoid AI and AI humanoids is to develop _human-level humanoid intelligence_ by simulating specific to comprehensive, and weak to strong human intelligence into humanoids. Human-level humanoids aim to simulate, infer, reconstruct or generate human-level cognition, vision, emotion and sentiment, communication/conversation, recognition, interaction, collaboration and control, as well as capabilities of analytics, reasoning and inference, learning, decision, and regulation. In general, vision, conversation, recognition, interaction, collaboration, learning and control are not difficult to implement thus widely present in humanoids such as Figure 01 and Optimus. Very few AI humanoids like Ameca can support emotion and sentiment, developing inference and regulation is essential for humane autonomous humanoids. It is an open area to develop humanoid mind though. 

### **2.2 Humanization Paradigm Shift: Human-looking, Human-like and Human-level Humanoids** 

Humanoid robots have experienced a fast progression and evolution<sup>2</sup> . By reviewing all humanoid robots and their developments over the six categorized stages of evolution in Fig. 1, humanoid AI studies have experienced a significant paradigm progression over different levels and intensities of humanization. We categorize it into three paradigm stages and aspects: 

- 1) _Human-looking humanoids_ , aiming for lookalike humanization with humanoid structures simulating human appearance with human-size and -looking body parts, with or without other human attributes or functions; 

- 2) _Human-like humanoids_ , aiming for functional humanization by developing humanoids to replicate human senses, behaviors, and functions; and 

> 2https://en.wikipedia.org/wiki/Humanoid_robot 

Manuscript submitted to ACM 

Cao 

6 

- 3) _Human-level humanoids_ , aiming for systematic humanization by nurturing humanoids embodied with substantial and systematic humanity and human intelligence. 

First, human-looking humanoids are mounted with humanoid structures to make humanoid look like human beings, with some having still or moving attributes. As shown in Table 2 [18], most of humanoids are equipped with simple and abstract human-looking parts, while robots like Geminoid and Junko Chihira are with more nuanced facial and head features. Humanoids may be driven by wheel and bipedal facilities. Then, human-like humanoids further humanize robots with representative human traits and functions. Humanoid senses, behaviors and functions make human-like humanoids not only look humanly but also behave and function humanly. Such humanoids tend to support humanfriendly immersive social interactions, such as by nuanced eye contact, and expressive facial and and postural response. Lastly, human-level humanoids narrow the gaps between humanoids being machine with machine intelligence and the clone (‘doppelganger’) of humans with some of simulated human uniqueness and identity of humanity and intelligence. 

A humanoid may blend humanoid structures with some of humanoid senses, behaviors and functions and specific humanoid intelligence suiting the humanoid objectives, tasks, and settings. More advanced human-looking robots tend to also embrace more expressive humanoid behaviors, such as body posture and actions, and even facial expressions. Most advanced AI humanoids may have electronic and AI-empowered brain, hands and legs and pursue humanoid functions such as conversation, speech, singing, dancing, walking, running, jumping, or grasping. 

There are about 30 types of humanoid robots available in the market and literature, while this number is rapidly updated. Table 2 in [18] provides an overview and comparison of 30 humanoid robots identifiable in public resources, which are endowed with certain human-like features and technical and AI-enabled functions. From the AI capacity perspective, we categorize existing humanoids into 1) _naive human-looking humanoids_ with some human appearance but limited to none AI functions, 2) _ANI-driven standalone humanoids_ with limited ANI functions on board only, and 3) _GenAI-enabled networked humanoids_ with on-humanoid and cloud-based operations and more capable AI functions in particular GenAI capabilities like Ameca with real-time connection to ChatGPT. Humanoids at these three capacity phases do not reach AGI capabilities on humanoid or on cloud. 

### **2.3 Ecosystem and Taxonomy of Humanoid AI and AI Humanoids** 

The six evolutionary stages of AI humanoid development and the three paradigms of humanoid AI research lay the foundation of the ecosystem, taxonomy and applications of humanoid AI and AI humanoids. Below presents a unique, multi-dimensional, multi-view and evolutionary taxonomy of humanoid robotics, humanoid AI, and AI humanoids. 

**2.3.1 Humanoid AI As A Field with Human-AI-Robotics-Web-Integrative Ecosystems** As a new research area, humanoid AI surpasses AI and robotics and transcends specific progresses such as GenAI, LLMs, and LMMs which are intensively applied in AI humanoids. Humanoid AI has ushered in a new era with revolutionary advancements and possibilities: 1) Transitioning from traditional task-specific hand engineering and programming methodologies to semi-task-specific, task-agnostic, or even open-task design, development, evaluation and deployment; fostering greater functional and task versatility and flexibility of humanoids. 2) Evolving from predefined, design-based and ruledriven robotic functioning, behaving and servicing to online, real-time, and active learning-driven tasking, execution and adaption; continuously improving humanoid performance, adaptability, real-world feedback, and experience. 3) Upgrading from individual robot-centric approaches to multi-robot, multi-task, multi-party, and entire process-oriented operations, control, planning, and task execution; enhancing humanoid efficiency and scalability in complex tasks, settings and environments. 4) Progressing design and development objectives from functional to nonfunctional and Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

7 

combining humanization in humanoid studies and system design; pursuing assurance of humanoid performance, quality and services in humane and natural settings and environments. 

The six evolutionary stages in Section 2.1 and the three paradigms in Section 2.2 address the above transitions and progressions of humanizing humanoids and developing humanoid AI over phase. They lay the foundation and sketch the scope of the area of humanoid AI. Building on and beyond individual areas and AI robotics [56], _humanoid AI_ emerges as the disciplinary synergy and metasynthesis [12] of robotics, AI, human science, and social science, specifically human systems, and intelligent systems, presenting as a human-AI-robotics-web-integrative ecosystem. 

**2.3.2 Taxonomy of AI Humanoids** With the ecosystem of humanoid AI, we further explore the interactions and synergy between AI and robotics and between human science and intelligent science. They result in the taxonomy of humanoid AI and AI humanoids, as shown in Fig. 2. 

First, on the high and technical level, _AI robotics_ [56] is the synergy of robotics and AI. In AI robotics, AI functions, tasks and techniques make robots more intelligent, enabled by cognitive science, computer vision, NLP, speech recognition, signal recognition, pattern recognition, machine and deep learning, data analytics, computational intelligence, knowledge representation, human-computer interaction, and machine ethics. AI robotics expand robotic functions, tasks, and techniques from replication to learning and generation. 

Second, _AI humanoid robotics_ incorporates humanoid features into AI robotics, producing AI humanoids and the field of humanoid AI. The foundations and enabling technologies of humanoid AI include conventional, general, generative, decentralized and emotional AI, as well as safe, ethical and responsible AI. Specialties include broad AI techniques, such as robotics, computer vision and pattern recognition, NLP/LLM, reinforcement learning, machine learning, deep learning, data science, and business informatics, human-machine interaction, and human and social science. 

Then, on the methodological level, AI humanoids incorporate elements and systems in human science and intelligent science respectively and integrate them into cross-disciplinary unification and transformation towards AI humanoid robotics. _Human science_ studies important traits and merits, such as human structures, senses, behaviors, functions, humanity, and intelligence. Incorporating such human systems into AI humanoids makes humanoids human alike and humanized. Further, _intelligent science_ have or implement various paradigms of intelligences. Such X-intelligences [16] may traverse traditional intelligence paradigms such as symbolic, connectionist, natural, social, domain, computational and networking intelligence to emerging paradigms including data, algorithmic, learning, generative, behavioral, emotion and cognitive intelligence. 

Further, _AI humanoid capabilities_ comprise both functional and nonfunctional aspects to implement humanoid senses, behaviors, functions, and nonfunctionalities. Functionally, AI humanoids interact, operate, communicate, coordinate, manipulate, navigate, automate, generate, simulate, replicate, generate, synthesize or meta-synthesize [12] traits and merits of human systems and intelligent systems. Nonfunctionally, AI humanoids may learn to empathize, interpret, secure, trust, derisk and comply. These functional and nonfunctional aspects expand, upgrade and transform robots toward a spectrum of humanoid/humanized functions. 

Accordingly, a family of _research areas_ of humanoid AI emerge, such as humanoid perception, planning, cognition, analytics, learning, reasoning, inference, reinforcement, reconstruction, generation, navigation, manipulation, control, regulation, compliance. Multi-humanoids may develop capabilities for communication, interaction, collaboration, and transfer. Humanity may be built into humanoids, such as emotion, intention and empathy. These humanoid AI research may apply to individual or group humanoids and for developing human-looking, -like and -level humanoids. 

Manuscript submitted to ACM 

Cao 

8 


Fig. 2. The taxonomy of humanoid AI and AI humanoids: Symbiosis of AI, robotics, human science, and intelligence science. 

**2.3.3 Applications of Humanoid AI and AI Humanoids** The applications of humanoid AI address various purposes and generate diversified types of AI humanoids. Functional humanoids can be categorized into social humanoids, industrial humanoids, and research humanoids. Their functional examples include walking, conversational, interactive, expressive, generative, manipulative, teleoperated, cognitive, and imitative humanoids. With regard to domains, AI humanoids are increasingly applied to widespread and specified situations and environments [40], professionalized into service, entertaining, convention, caregiving, assistant, advising, home, factory, manufacturing, logistic, workflow, online, arts, military, search, exploratory, security, compliance and social humanoids, and other task-specific humanoids. 

Examples of specific humanoid applications include _home, residential, personal and elderly assistance and caregiving humanoids_ for healthcare, home care, and aged care; _safety humanoids_ for work, road, transport and traffic safety detection, monitoring and assurance; _social humanoids_ for social services, activities and engagement; _education humanoids_ such as Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

9 

for primary education, inquiries, question/answering, and online learning; _marketing and customer services humanoids_ , such as for general inquiries, reception, chatbot, campaign, and activity organization and management; _hospitality humanoids_ such as for kitchen, food and catering services; _digital art humanoids_ such as for creating digital songs, dances and artworks; _health and medical research and service humanoids_ such as for prosthesis, orthosis, personalized healthcare aids, eldercare, companionship and nursing support, and supporting people with disabilities; _manufacturing and industrial humanoids_ such as for mining, assembly, sorting, painting, material handling, pick-and-place, and delivery, and operating specially designed equipment and vehicles, such as stuntronics and animatronic devices; _cognition and neuroscience research humanoids_ such as for human brain modeling and cognitive functions on neurorobots; _military humanoids_ for unmanned military agents, operations, and activities; _exploration humanoids_ such as for astronomy and space exploration; _emergency humanoids_ such as for disaster management and performing hazardous jobs such as nuclear and earthquake rescue; _event, demonstration and exhibition humanoids_ for their instruction, planning, coordination, monitoring, demonstration, and large-scale social activities such as for theme parks and exhibitions; and _entertainment, game and competition humanoids_ such as humanoid league for RoboCupand World Humanoid Robot Sports Games for half-marathon competition. 

## **3 Humane Humanoids: Functional and Nonfunctional Specifications** 

Humanoid AI develops AI-driven humane humanoids sufficing functional and nonfunctional specifications with corresponding criteria, constraints, and quality measures in performing their objectives, designs, tasks, and properties. This is applicable to human-looking to human-like and human-level paradigms and generations of humanoid AI and AI humanoids. Fig. 3 summarizes typical functional and nonfunctional specifications of AI humanoids. 

### **3.1 Functional Specifications of Humanoids** 

Functional specifications of human-like and lifelike humanoids define and enable how an AI humanoid look like, what it does, and how it implements its purposes, tasks, and operations, etc. They determine what humanoid structures, senses, behaviors and functions to implement and operate, as summarized in Table 3 [18]. While humanoids differ in their functions and none holds all functions, humanoids are expected to satisfy functional specifications defining mechanical, electrical, biological and social designs with anthropomorphic and mimetic features. Such humanoids imitate human intelligence by their enabling appearance, brain, perceptiveness, activeness, connectiveness, interaction, organization, knowledge, cybernetics, generalization, and system. 

**3.1.1 Humanoid Appearance: Anthropomorphism and Aesthetics** Anthropomorphism and aesthetics customize humanoid appearance. Humanoids are partially to fully embodied with anthropomorphic, humanly mimetic, morphological, animated or caricatured features. This humanoid anthropomorphism [87] and aesthetics include instantiations into: 1) _human-like or lifelike organs_ , such as electronic skin (e-skin), bionic and sensory tactile skin, prosthesis, wearables, and 3D surfaces; and 2) _human-like or lifelike functions, senses and traits_ embedded into anthropomorphic body parts, such as touch, pressure, force, contact, hardness and texture, or even humanly physiological features such as temperature, pain, pulse rate, blood pressure, and bodily fluids such as sweat and tears. Such _human mimetic mechanisms_ [3] and anthropomorphism further evolve into _human imitation_ , embedding humanoids with human-like and lifelike body structures and functions, such as skeletal structures and functions, human body proportions, link length, mass balance, muscle arrangement, insertion points, and joint performance with joint range and output power; _anthropomorphic behaviors and activities_ such as eye movement, head movement, skin sense, tactile sense, and hand gesture; and _human-like and lifelike body quality_ , such as degrees of freedom, expression intensity, and sense sensitivity. 

Manuscript submitted to ACM 

Cao 


Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

11 

Transferring human-like and lifelike features into humanoids fosters humanoid aesthetics. _Humanoid aesthetics_ synthesize human beauty, creation art, fashion, and visualization into humanoid beauty, typically embodied through avatars. For example, cybernetic avatars [37] may have very nuanced positions, shapes, colors and degrees of freedom of body parts, such as realistic facial skins and contours, and eyes with fine-designed eyelids, eyeballs, and eyebrows. Technological aesthetics may produce realistic to hyper-realistic humanoids, the alter ego of humans. Such near-perfect humanoids and avatars may trigger an experience of the uncanny to some people [54], also because of their lack of the nature of human mind, personhood, and humanity. Further developing digital mind and humanity, such as mental states, emotions, intention and ethics, into humanoids may leverage humanoid anthropomorphism and aesthetics with more humane characters, as further discussed in Sections 3.2 and 4.2. 

**3.1.2 Humanoid Brain: Mind and Cognition** Humanoid mind and cognition imitate human brain mechanisms to achieve human-like mental and cognitive thinking, consciousness, traits, and capabilities, etc., although rarely explored. Accordingly, developing humanoid mind and cognition requires to understand how human brain functions and to develop humanoid mental models simulating human functions and capabilities including reasoning, inference and decision-making mechanisms, as well as mentality like goal, intention, and emotion. _Humanoid mental modeling_ attributes the theory of mind with thoughts, desires and intentions etc. [76]. It formalizes mental representations shareable between humanoids and between humans and humanoids by characterizing and simulating the awareness, roles, responsibilities, knowledge structures, mechanisms and processes of human cognition, reasoning, teaming, interaction, communication and collaboration for achieving human-like problem-solving and decision-making. 

Specifically, _humanoid intentionality_ captures how humans make aims, objectives, and plans and develops robotic intention models. _Robotic emotions_ are implemented by hand-coded, automated, or learning-based designs and methods [64]. _Robotic affection_ further combines personality trait, attitude, emotion, mood and interpersonal stance [50]. Modeling humanoid intention, emotion and affection represents a new stage of developing humane humanoids by incorporating humanity and mentality into human-like, human-level machines. Humanity and mentality may be learned from human activities, scenes, behaviors, facial expressions, spoken emotions, postures, textual sentiments, and interaction attributes, etc. The generation, recognition, learning, transfer, alignment and adjustment of humanoid emotion, affection and intention may be guided by goals and tasks, in the wild, during performing activities, from multiple modalities, or during interaction and collaboration with humans. 

**3.1.3 Humanoid Perceptiveness: Vision, Speech, Hearing and Senses** _Humanoid perception_ simulates human sensing mechanisms of vision, speech, hearing, touch, taste, smell, and other sensations such as feeling. Humanoids perceive, represent, understand, recognize, fuse, adapt and respond to internal and contextual information, activities, and situations through sight, oral, auditory, tactile, olfactory, gustatory, and other sensory channels. Humanoids are equipped with proprioceptive and exteroceptive sensors to perceive and model internal states and behaviors, target objects and their states and behaviors, and interactions with objects w/wo context or environment. Internal states of humanoids may include information about their locomotion, position, velocity, depth, orientation and behaviors [66]. Humane humanoids may also perceive cognitive features such as attention, gaze movement, and facial expression or even emotion of a human. They also identify and recognize target objects and their layouts, states, behaviors, or activities, e.g., human pose and facial features. During humanoid-object interactions and human-humanoid interactions, humanoid further detects, recognizes and reacts to interaction modes, activities, types, modalities, and channels. Contextual perception captures the context, surroundings or environment of a humanoid and its objects. Humanoid perceptron identifies contextual materials and textiles, environmental states, conditions (e.g., lightening conditions), or layouts. 

Manuscript submitted to ACM 

Cao 

12 

With embedded cameras to enable robot vision [65], _humanoid vision_ can capture and enable humanoid gaze, gesture, pose, action, motion, expression, movement, collaboration, learning, and communication. 

Humanoid perception [66] is enabled by either _intrusive sensors_ such as actuated cameras, force, microphone, inertial measurement units, encoders, sensitive resistors, sonar, rotary, tactile, torque, laser scanner, joint and inclinometer, which may be placed in a humanoid’s head, neck, chest, torso, or hand etc body parts, or _non-intrusive sensors_ or facilities such as remote wireless cameras, radar, LiDAR, or Wifi. Sensors or multi-sensor fusion may capture internal and external states, signals or videos relating to vision, audio, olfactory, tactile, shape, curve, and posture of human body parts; human features such as emotion and facial expression; physiological signals of human body, such as heart rate, blood pressure, body temperature, brain activity, and muscle activation; and environmental range and layout, or contextual representation and memory, etc. In performing perception, humanoids recognize internal states such as stability, dynamics, safety, efficiency, and experience; and external aspects such as identifying, recognizing and locating external stimuli, layout and relationships with objects; and interactive states such as robustness and adaptability to dynamic and unforeseen environmental changes. Humanoid perception enables diverse humanoid tasking and functions like tracking, detection, recognition, identification, classification, control, localization, navigation, planning, mapping, manipulation, and grasping. Humanoid perception can also support specific tasks relating to human-humanoid interactions, object manipulation, gait planning, proprioceptive state estimation, action prediction, and emotion recognition. 

**3.1.4 Humanoid Activeness: Behaviors, Motions and Dynamics** Humanoid activeness are embodied through their behaviors, kinematics, and dynamics. The dynamics of human systems, behaviors, and intelligence are fundamental for human functions, operations, and evolution. Understanding human behaviors and dynamics can inform and transform humanoid behaviors and dynamics. _Humanoid behaviors_ capture how a humanoid behaves, acts, and reacts, etc., supporting various forms of operations, such as gesture, movement, and interactions with other robots or humans [5]. Behaviors emerge over the lifecycle of humanoid tasking, generating sequential and full-cycle state spaces with behavior attributes, processes, consequences, and impacts [10]. For example, _humanoid gestures_ [20] comprise human gesture-simulated appearances, behaviors, and states, enabling humanoid’s facial expression, eye gaze, communicative pointing and signs, and manipulative motions, etc. Humanoid movements embody actions such as eye, hand, and leg movement. These low-level behaviors further enable high-level _humanoid motions_ , implementing general behavioral functions and purposes such as communication, engagement, grasping, navigation, and teleoperation. Under specific tasks and scenarios, humanoids may take imitative, tactile, social, walking, grasping, acrobatic, or amphibious behaviors, which may be stylistic, personalized, safe or hazardous. 

_Humanoid navigation_ goes beyond robot navigation [53] of taking actions and following action trajectories to achieve goals and intention. In general, humanoids navigate passively, guided by visual, vocal or other types of perception, a map, demonstrations, simulation, or pretraining. Humanoids manipulate their gestures, movements, and actions to change and generate new dynamics [73], further driving mobility and dynamics of their kinematics, contact mechanics, and centroidal dynamics with bipedal or wheeled devices. Increasingly, humanoid _learning to navigate_ or _navigation by learning_ drives active, online, mapless or open-world exploration, learning, and reinforcement [81], enabled by unsupervised, active, online, adaptive, reinforced, and open-world learning. Humanoid learning-to-navigate capabilities handle not only general robotic but humanoid-specific tasks and settings, such as navigating while assisting elderly people for humanoid health care, which may fuse special navigation specifications (e.g., safety and trust check). 

_Humanoid teleoperation_ traverses robot teleoperations [26] of undertaking local behaviors and telebehaviors, such as telelocalization, teleperception, retargeting, mapping, planning, and control. The human-like nature makes humanoid 

Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

13 

more suitable for teletasking, telepresence, and teleexistence in remote environments, such as for telehealth and telenursing. Humanoids may be teleoperated in a whole-body, partial-body, bilateral, leader-follower, stereoscopic or even immersive manner, where humanoids may be manipulated by speech, position force control, eye gaze, bimmanual control, telelocomotion, imitation, demonstration, learning, or even virtual/mixed reality [60]. As discussed in Section 4.5, humanoid teleoperation can further integrate animation, virtual reality, digital twin, and metaverse technology for more immersive and realistic operations. In this regard, a typical example is the _cybernetic avatar_ [37], teleoperated by an operator, where the avatar and the operator coexist as a symbiosis. 

In addition, humanoid behavior cloning, imitation, animation, transformation, adaptation, and transfer can mimic, share, transform, generate or respond with new behaviors, fostering new humanoid functions and operations. These would further involve humanoid behavior analytics and computing [10] to understand, monitor, predict, and manage behaviors and their effects and improve humanoid goals, tasks, and performance. 

**3.1.5 Humanoid Connectiveness: Networking and Communication** Humanoid connectiveness builds on humanoid networking and communication [39, 57]. Humanoid networking builds connections within or between humanoids and between humanoids and external objects, humans and environments. Humanoid communication further imparts, transports, or exchanges information, materials, or energy within a humanoid, between humanoids, between a humanoid and its environment, or between humanoids and other objects such as humans. _Learning to communicate_ (LoC) rapidly overtakes roles of traditional communication methods, physical objects, and signals. LoC increasingly involves demonstrations, imitations, representations, or model parameters of physical or sensory materials, behaviors, or activities. Besides _communication participants_ like other humanoids, humans, or objects, LoC can involve _media_ such as in imagery, video-based, acoustic, textual, emotional, or behavioral form; _content_ such as speech, navigation, and actions; _indirect participants_ such as humans or objects for demonstrations or imitations; and _context_ such as topic areas and background. While biparty communications with another party like a human or another robot dominate existing studies, peer-to-multiparty interactions represent frontiers by enabling multiple parties, or a team with multiple humanoids, or humans and humanoids. Such human-to-humanoid communications can be unidirectional, directional, or multidirectional. Humanoid communications happen 1) within humanoids in various ways, e.g., for body part coordination between head and hands or between eye and hands through transiting and processing sensory information, and state or process transition or transformation such as from perception representation to conversation; 2) between humanoids or between humans and robots, e.g., between humanoids for collective tasks through goal sharing, task cooperation, or load negotiation; and 3) between humanoids and their static or dynamic contexts/environments, e.g., through tracking, representing, and transiting contextual information for navigation and operations; etc. 

LoC-driven humanoid communications expand _linguistic_ communications from speech, message-passing, and dialogue to query-answering, retrieval, and recommendations; and _non-linguistic_ communications from vision [39] and camera/eye contact to responsive emotions, and postural, gestural, behavioral, or graphical interactions or movements. These transform unimodal to multimodal LoC with language-based to multimodal communications. _Non-expressive_ communications such as through sensory information consumption and sharing are complemented by _expressive_ communications such as emotional, sentimental, affective, or behavioral expressions and exchange of facial expressions, spoken emotions, textual sentiments, or behaviors such as gestures, postures, body language, and actions. Besides multimodalities, _multimodal LoC_ also incorporates _multimodal transformation and translation_ in _bilateral_ manners, such as via text-to-speech translation, speech-to-text translation, image-to-text transformation, text-to-image transformation, 

Manuscript submitted to ACM 

Cao 

14 

vision-to-language transformation, and language-to-vision transformation; _multilateral_ , such as vision-language-toaction (VLA) transformation, or vision-language-to-emotion (VLE) transformation [48]; or _mechanism-based_ , e.g., demonstration-to-action, or imitation-to-action. These translation and transformation tasks undertake cross-modality or cross-mechanism information transport, which may take place in an _invasive_ , _non-invasive_ , or hybrid mode. 

**3.1.6 Humanoid Interaction: Collaboration and Competition** Humanoids connect, associate or relate one to another or to other objects or humans, forming humanoid interactions for collaboration or competition. Such interactions take place between humanoids, humans, or environments, and within humanoid communities, transforming humanrobot interactions (HRI) [34] to specific humanoid-humanoid, human-humanoid, or human-humanoid-environment interactions for humanoids. _Humanoid interactions_ may be directional, physical, cognitive, perceptual, behavioral, responsive, social, multi-party-based, contextual, or environmental, depending on their interaction settings, environments, and tasks. Specifically, humanoid interactions transcend general forms of robot and human-robot association, connection, recognition, identification, detection, or tracking to specific forms of humanoid or human-humanoid coordination, cooperation, negotiation, collaboration, or even conflicting, or competition. Humanoid interactions are associated with, during or for implementing tasks, such as grasping, assembly, communications, collaboration, or teleoperation. For example, _humanoid-human collaboration_ builds on robot collaboration or human-robot collaboration [6, 69] to fulfill tasks including forming teams, defining goal, plan, actions, strategies, and constraints, resolving conflicts, or enabling humanoid communications, analytics, and learning. With humanoid learning, _learning to collaborate_ grows its value in humanoid collaboration, empowering humanoids to _learn from data_ such as hand-crafted knowledge base, labeled samples, demonstrations, imitations, machine-generated samples, or protocols; and to learn by methods like pretraining, retraining, finetuning, or adaptive or continual learning. Learning from mixed reality and metaverse could also transform humanoid interactions in physical worlds. In contrast, _humanoid competition_ may be driven by goals, tasks, skills, resources, roles or scenarios. Adversarial competition may involve humanoid attack and defense. 

_Social humanoids_ engage _social interactions_ [44] in a humanoid society, agency, or human-humanoid coexisting community. Social humanoids follow social and cultural norms and express emotions and sentiments during social engagement and in fulfilling social skills and solving social problems. Social interactions incorporate _humanoid humanity_ , such as intention, emotion, affection, and empathy. For example, affective robot interactions [58] may enable better collaboration, assistance, imitation, coordination, cooperation, and general or multi-purpose communications. 

**3.1.7 Humanoid Organization: Planning and Search** Humanoid organization decides what, how, when, or where a humanoid behaves, undertaking robot planning and search [45] to navigate, move body parts, search information, take actions, or perform tasks. These enable path, motion [78], and task planning, or incorporate robot search, such as heuristic search, and stochastic search, into retrieving interested information or target, in known to unknown clutter environments with known to unknown obstacles. In doing these, humanoids optimize their target motions, movements, paths, or tasks and minimize concerning issues such as collisions, and time or energy consumption. 

With humanoids enabled by learning advances including LLMs and LMMs, _learn-to-plan_ , or _planning by learning_ [32], becomes a new fashion of humanoid planning in complex contexts. Humanoids navigate, search, respond and act per justifications, predictions, recommendations, or retrieved findings by techniques including probabilistic roadmap, evolutionary computing, geometric modeling, reinforcement learning, and deep learning. Learn-to-plan is particularly important for interacting with, manipulating, or responding to unseen objects, scenarios, tasks in semi-open to open worlds. For example, a robot enabled by a pretrained VLM can extract object category-specific features from images and texts [71]. Further, a robot can undertake actions or complete instructions with policies informed or constrained Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

15 

by categorized objects with imagery and textual instructions, such as SayCan [9] which _plans-to-act_ based on input language. Google RT-2 [86] is another VLM-based learn-to-plan advance, which builds on a VLM backbone, plans from both image and text commands, and conducts visually grounded planning. Its _chain-of-thought_ reasoning can enable learning long-horizon planning and low-level skills to achieve highly-improved robotic policies by instantiating VLAs based on PaLM-E [27] and PaLI-X [23]. RT-2 can significantly improve generalization performance and emergent capabilities using the power of web-scale _vision-language pretraining_ (VLP) [1]. 

**3.1.8 Humanoid Processing: Representation, Analytics, Learning, Reasoning and Recommendation** Humanoids are associated with their data, behaviors and environments. Humanoids represent, analyze, learn, discover, reason about and recommend them to knowledge to empower humanoid functions, operations, and performance. Humanoid knowledge enables their capabilities and quality of services through analytics and learning from data, behaviors, and environments of themselves or other humanoids, robots, humans, and objects. They undertake goals and tasks to gain and strengthen their specific to comprehensive humanoid intelligence, particularly by conducting machine vision, reasoning, reinforcement learning, and learning by demonstrations, imitations, interactions, behaviors, and feedback. As illustrated on learning to communicate and interact in Sections 3.1.5 and 3.1.6, autonomous and intelligent humanoids perform on-device and decentralized to cloud and online, shallow to deep, small to scalable, pretrained to finetuned, unsupervised to supervised, unimodal to multimodal, uni-task to multi-task, on-policy to off-policy, and specific to general learning in closed to open settings or worlds. In particular, generative AI especially LLMs and LMMs enables more scalable, self-supervised, scenario-based, and real-time humanoid intelligence, such as for real-time, interactive, affective multiparty conversation [48], which was impossible to achieve before. 

Humanoids perform knowledge representation, analytics, learning, and reasoning [13, 17] on 1) internal data, such as the sensory information, responses, and feedback (such as failures); 2) interaction data, such as with objects, and contexts; and 3) contextual data, such as with scenarios and environmental settings. These may be self, interactive, and contextual. Humanoids perform logical, causal, probabilistic, temporal, spatial, constrained, and multimodal reasoning and inference. Further, _humanoid analytics_ identify, detect or predict patterns or exceptions of and insights into humanoid body parts, signals, states, behaviors, movements, and trajectories, as well as external, contextual, and environmental factors, relations, and changes. Such humanoid analytics support functional and nonfunctional objectives and different paradigms of humanoid intelligences, as shown in Fig. 3, on historical, present, future/next, new/cold-start, or open/unknown data, behaviors, settings, scenarios, or contexts. 

_Deep learning, LLMs and GenAI_ [52] are substantially transforming humanoids with human-like intelligence. GenAI and LLMs can empower humanoids like Ameca with unprecedented capabilities of acquiring and analyzing diverse sources, modalities, or formats of large scale inputs through pretraining and finetuning. Pretraining makes humanoid patternable or informative for signals or videos acquired from sensors of humanoid body parts; activities and behaviors of robot body or parts; interactions, communications, or coordination between robots and between robots and their environments; and transitional processes such as from vision to language or translations such as from speech to image. Humanoid pretraining builds patterns, exceptions and knowledge into humanoids, which could be further finetuned towards test, new, or open tasks or environments. Various finetuning techniques emerge and apply, such as by prompt engineering, instruction, retraining, online, test-time, contrastive, iterative, reward-based, human feedback-based, reinforcement learning, and data augmentation, to adapt pretrained humanoids to test and new tasks. 

Humanoids learn by _humanoid programming_ , learning by demonstrations, simulations, or imitations. Humanoids learn by demonstration [2], simulation [55], or imitation [77] to develop knowledge, decisions and actions from training, 

Manuscript submitted to ACM 

Cao 

16 

examples, simulation, imitation, teleoperation, shadowing, sensors on teacher, or external observations for unsupervised, semi-supervised, and few-shot supervised learning tasks. During demonstration, simulation, or imitation, domain experts or end users teach humanoids to conduct specific tasks, so that humanoids can distill knowledge or skills from these demonstrations without pre-programmed knowledge to execute new tasks. With game theory, virtual reality, and metaverse, _humanoid learning by animation_ will extract and discover knowledge from animated or real videos or games, and virtual/augmented/mixed reality to transfer knowledge and skills from gamers and animators, design, develop, train and evaluate novel skills and applications at a cost-effective way through humanoid-metaverse integration. 

Another humanoid learning paradigm is _transformative/translational humanoid learning_ (THL), where humanoids learn to transform or translate. THL progresses from _vision-language modeling_ (VLM) [42, 71] to _vision-language-toaction_ (VLA) [86], _vision-language-to-emotion_ (VLE) [48], and _vision-language-to-behavior_ (VLB) modeling. These foster new directions of _multimodal modeling to actions_ (MMA) and _multimodal modeling to decisions_ (MMD) for actionable humanoid learning. In Section 4, we will further discuss humanoid analytics and directions of incorporating LLMs, GenAI and deep learning into humanoids, and specifically on opportunities including omnimodal perception-to-behavior and mind-to-action modeling for mindful, cognitive, and actionable humanoids in Section 4.4. 

These new analytics and learning directions induce predictions, recommendations, interventions for smart humanoids. They can substantially foster and expand humanoid capabilities through simulation-to-humanoid (Sim2Real), humanoidto-simulation (Real2Sim), animation-to-humanoid (Ani2Real), video-to-humanoid (Video2Real) transformations, and building animator-humanoid digital twin. They may further expand existing research on Sim2Real, Real2Sim, Image2Sim, and Video2Sim, etc., and tools like NVIDIA’s Audio2Face. 

**3.1.9 Humanoid Cybernetics: Manipulation and Control** Humanoid cybernetics manages robot manipulation and control. Humanoids may manipulate their body parts such as eye movements, facial expression, or postures, or external objects such as grasping objects. _Humanoid manipulation_ [56] serves various tasking purposes and involves diversified robot parts, which may be classified into typical types including system-centric manipulation, object-centric manipulation [71], action or state-centric manipulation, transition-centric manipulation, and process-centric manipulation. System-centric humanoid manipulation operates a robot part, e.g., manipulating the locomotion. Object-centric humanoid manipulation instructs, controls and manipulates robots toward specific objects under object background. Action-centric and state-centric humanoid manipulation guides, controls and operates robots towards taking specific actions or approaching target states, e.g., rearranging an object or reorienting a robot hand. Transition-centric humanoid manipulation focuses on robot state or behavior transition from one to another, e.g., raising a hand and then positing it toward a target object. Process-centric humanoid manipulation involves multiple steps of action or state progression or change, e.g., from perceiving the environment to moving a hand and then grasping an object. 

_Humanoid control_ represents a strong type of manipulation of humanoids or external objects, where a humanoid influences, directs or manages its behaviors, actions or their processes. The objectives and tasks of humanoid control are varied [63]. Humanoids may control its parts such as head, eyes, emotion, gait, legs and hands. They may perform control to implement their functions such as trajectory, horizon, gesture, posture, collaboration, interaction, behavior position, and speed. Humanoid control can execute specific tasks such as bipedal locomotion, omnidirectional walking or satisfy nonfunctional requirements such as safety. Humanoid robots may be controlled by different mechanisms. Functionally, humanoid control relies on the corresponding mechanical and electrical humanoid designs to implement specific objectives and tasks, such as optimization methods, dynamic models, bionic methods, reinforcement learning, demonstration learning, imitation learning, and prediction. Controls are incorporated into humanoid body parts, such 

Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

17 

as by a central nervous system, a motor controller, stability and balance measures such as zero moment point, capture point and centre of pressure, and data- and model-driven analytical and learning techniques. Control environment may be open, closed, semi-open or semi-closed in terms of interactions with environments. Control modes may be autonomous, semi-autonomous or hand-engineered in a static, dynamic or adaptive manner. Automated control may be driven by policies through real-time learning or rules predefined or hand-coded. 

_Learning-to-control_ and data-driven and behavior-based control represent new control modes and scenarios, where analytical and learning systems such as anomaly detection, predictive learning and generative AI are incorporated into robot engine for monitoring, detecting, predicting and preventing control failures, damages or accidents [72, 81]. In AI-empowered humanoids, a typical technique of learning-to-control is deep reinforcement learning, which obtains optimal actions or state-action combinations, i.e., policies and strategies, to decide and govern humanoid behaviors and actions. Humanoid learning-to-control may also apply learning by demonstration, imitation, prediction, and recommendation etc techniques to obtain control capabilities. 

Humanoid robots also involve new control problems or approaches, which may relate to humanized features, functions and tasks. For instance, facial expression control, eye and mouth movement control, human gesture and posture control, hand and leg movement control, and human-humanoid interaction can be guided by hand-engineered rules or policies or learning-driven findings. These require not only ergonomic design but also control, in particular, realtime, interactive and online control from multitask, multimodal and omnimodal VLA modeling and cognition-to-action translation from web-scale data, humanoid data, and external environments. 

**3.1.10 Humanoid Generalization: Adaptation and Optimization** Humanoid generalization enforces adaptation and optimization. Humanoid adaptation adjusts the states, behaviors/actions, policies/strategies, or even parameter settings of a humanoid or a humanoid team to fit their evolving goals, plans, tasks, processes, conditions, contexts or environments. Adaptation applies to all humanoid tasks. Such humanoids should have the adaptability and corresponding functions to sense changes, feed back deviations, arrange strategies, adjust actions, evaluate performance, and reflect on adaptation. Adaptive humanoid designs and capabilities include mechanical design with adaptive sensor motors, adaptive control techniques, online and active perception and recognition, evolving human-robot interaction, evolving learning, dynamic finetuning, predictive control, online motion generation [51], predictive next actions, and proactive risk and compliance management. 

Specifically, _general-purpose humanoids_ may live in real-life environments and face dynamics and changes of states, functions, and tasks in semi-open to open worlds, e.g., during conducting real-time automated capabilities. Accordingly, how to make general-purpose humanoids to act, reason and interact like a human being in real-world scenarios poses a fundamental challenge to humanoid robotics. Existing approaches such as sharing _mental models_ across all robots and enabling predefined flexibility for bipedal locomotion and dexterous manipulation in known evolving environments cannot capture novel or unseen scenarios. General-purpose humanoids in open, novel and uncertain dynamics require _learning to adapt_ , or _adaptation by learning_ , and human-supervised adaptation [82]. Humanoid adaptation by learning may demand predictive architectures, data-driven adaptive learning capabilities, neuro-inspired control, and evolutionary learning. For example, adaptive evolutionary humanoids may amalgamate biomimetic design, morphological computation, and evolutionary learning to enable adaptive mutation, crossover, selection, and optimization of actions, states, policies, and goals iteratively and sequentially. 

Manuscript submitted to ACM 

Cao 

18 

Humane real-world scenarios demand a real-time understanding and transferring human intention, emotions, empathy, and decision sequentially to humanoid tasking over time. In a humanoid or human-humanoid society, humanoid adaptation further requires understanding and obeying social norms during social interactions and activities. 

**3.1.11 Humanoid Design: Multiaspect Integration** Anthropomorphic and aesthetic humanoids are driven by their mechanical, electronic, electrical, biological, and social designs concerning robotic hardware, software and operational developments. These humanoid designs surpass robot designs [68] to empower humanoid-oriented sensors, processing units, mechanical structures, kinematics, electronic and electrical devices, power supply, and software architectures and implementations incorporated with humanoid social norms and activities to imitate human-like and lifelike appearance, functions, behaviors, and intelligence. 

_Humanoid mechanical design_ involves new technologies [30, 36] to enable anthropomorphic body and parts, such as android head, neck, torso, hand, fingers, leg, and foot, their covering skin and muscles, and their proportions, and distributions; skeletal and musculoskeletal structures with joint mechanisms with actuators and drive mechanisms for different body parts such as for hip, knee, and ankle; android operations and control, such as locomotion mechanisms, force and strength manipulation, legged or wheeled systems, joint movement, and transduction mechanisms and functions; anthropomorphic functions such as eye gaze, touch sense, grasping intensity, and assembly; humanoid behaviors such as mechanical enablers for movement, navigation, and tracking; android aesthetics for enabling humanlooking features such as eyeballs, eyebrows, and lip [37]; and humanoid control and assurance such as enabling humanoid safety, and preventing fall or slippage. 

_Humanoid electrical design_ integrates electrical and electronic technologies into robotic and humanoid structures, functionality, reliability, and adaptability, etc. [79]. Electrical designs enable humanoid sensors for proprioception, exteroception and processing; electrical actuators and motor drivers; power systems; networking and communications; embedded systems and integrated units; on-board signal and information processing; human-humanoid interaction systems; and quality assurance such as safety and failure management. These sensory and electronic mechanisms and functions are integrated with mechanical designs, mechanisms, and functions, as well as other mechanisms and systems such as resistive, capacitive, optical, piezoelectric, and magnetic mechanisms and devices. For humanoids with rich anthropomorphic features, such as the realistic Ameca head [29], advanced motors and articulation systems under the silicon skin drive and control nuanced lifelike features, functions, and performance, such as facial muscles, expressions, emotions, eyebrow movements, nose crinkle, lip and jaw movements, and arm movement. 

_Humanoid biological design_ is bioinspired and bionic. Biological design simulates biological and biomedical mechanisms, structures, materials and control of the human body in humanoids to create more natural, human-like, lifelike and rational structures and functions and more intricate tasking and performance of humanoids [46, 62]. Biological design specifies the appearance, structures, functions, behaviors, and performance of humanoid body and parts by mimicking various biomedical, ergonomic and neural mechanisms, parameters, and settings. They specify artificial body of humanoids [7, 37], including skeletal framework, artificial skin, muscles and tendons; synthetic textures, responses and degrees of freedom; physiological states and conditions, such as size, weight, strength, load, volume, mass; and neuromorphic features, such as emotional expression and mental states. Biological design inspires the definition and implementation of humanoid functions, such as walking, climbing, vision, hearing, and touch; and humanoid behaviors such as gestures, postures, mobility, interaction, and learning. 

_Humanoid social design_ defines social (interactive, collective), ethical, and emotional/affective mechanisms, activities, and norms of humanoids in a humanoid team or society or with humans [44]. Such social design provides technological Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

19 

supports (both connecting to mechanical, electrical and biological designs and sociality-specific designs [43]), social and ethical specifications, and even affective engagement for humanoids to interact, collaborate, cooperate, team, compete or even attack/defend with humans or other humanoids or agents individually or collectively. Human-humanoid interactions, teaming, collaborations or competition require enforcing social, ethical, emotional, psychological and cultural rules, norms or checklists for dos and don’ts in relation to their contracted goals and tasks, interactive objects and attributes, and embodied or embedded physical, remote or virtual situations, scenarios and environments [31], such as avoiding collision, and prohibiting attacking humans. Differing from non-humanoid social robots, social humanoids may require certain levels of human-likeness, life-likeness, humanness, and even humanity to facilitate humane interactions and address the uncanny valley effect. Social design also involves nonfunctional matters as discussed in Section 3.2, including _humanoid ethics_ to regulate social humanoids by trust, safety and privacy checks before and during interactions and enforcing their responsibility, and accountability. 

These humanoid mechanical, electronic, electrical, biological and social designs guide the implementation and integration of humanoid structures, senors, actuators, communications, interaction, networking, interface, and system performance. 

### **3.2 Nonfunctional Specifications of Humanoids** 

With the fast growth and advancement of robotic techniques and functions, humanoid robots are expected safe and secure in their operations and action-taking; trustful and responsible for their actions; transparent and explainable in their outputs; empathetic and rational during teaming, collaboration and interaction; and compliant, legal and ethical for integrity and regulation. Accordingly, the functions and quality of humanoids need to be ensured by various nonfunctional requirements, objectives and constraints. As summarized in Table 3 [18], they cover many aspects from traditional requirements on the robotic quality of services to new control problems relating to humanized requirements. We categorize such nonfunctional specifications into four aspects below: 1) human likeness satisfaction, 2) humanoid capability maturity, 3) humanoid performance measurement, and 4) humanoid impact estimation. 

**3.2.1 Human Likeness Satisfaction** _Human likeness satisfaction_ refers to the extent a humanoid resembles the cognition, appearance, behaviors, biometrics and social interactions of humans and their lives and the cultural alignment with them. These human anthropomorphism and life likeness of a humanoid can be categorized in terms of the humanoid cognitive likeness, physical likeness, biological likeness, behavioral likeness, and sociocultural likeness of humanoid design and development. 

**Humanoid cognitive likeness** refers to the extent that a humanoid resembles the cognitive, mental and subjective mechanisms, processes, states, traits, and abilities. It replicates human thought process, logic, intentionality, intuition as well as characters and personality [76]. Cognitive likeness also measures the humanoid ability to think, understand, communicate, analyze, learn, reason, infer, generalize, respond, and adapt as a human. In humanizing and personifying robots toward human-like, human-level and humane intelligent systems, humanoids are further humanized with mechanisms, properties and traits such as human-like aggressiveness, morality, consciousness and personality [49]. For example, a humanoid may present extroversive, agreeable, conscientious, neuroticive, open or aggressive personality, forming _humanoid personality_ in articulating robotic features and functions and in robotic tasking and employment. A humanoid may be rational with intentionality and consciousness for being or doing good, with moral and empathetic actions and behaviors during tasking or human-humanoid interaction, teaming and collaboration, which creates _humanoid intentionality_ and _humanoid rationality_ . Such humanoid personality, intentionality and empathy require bidirectional design and support. On one hand, a humanoid can access a human or other robot’s cognitive, emotional 

Manuscript submitted to ACM 

Cao 

20 

and affective states, and then behaves and interacts with them with empathy and morality and meeting human comfort. On the other hand, humans can fully access and control a humanoid’s intentional stance, and personality, and their behaviors can be managed and interpreted by a human being. 

**Humanoid physical likeness** measures the extent a humanoid resembles human physical structures, attributes, functions, and aesthetics by visual appearances, layouts, and interfaces [3]. These may be measured in terms of their resemblance dimensions, proportion, ratio, intensity and likelihood of a human body structure, facial components and features, and skin and surface texture. For example, Ameca Desktop focuses on mimicking human facial likeness, while the full-body Ameca [29] expands the anthropomorphism and aesthetics to the entire body of the humanoid. Cybernetic avatars [37] present nuanced human appearance including artificial skin, eyeballs and eyebrows. 

**Humanoid biological likeness** assesses the extent a humanoid replicates the internal and external systems, functions and features of human biological systems. Biological likeness complements physical likeness with the underlying bioinspired materials, structures, processes, behaviors and features of human biology and physiology [7, 46]. The resemblance of human sight, tactile, olfactory, taste, and hearing contributes to the phenomenal sensory capabilities, design and mechanisms in humanoids. In addition, a humanoid may mimic the skeletal framework of human anatomy for structural integrity and joint designs; the features, abilities, functions, sensitivity and adaptability of human skin and muscles for surface coverings, movement and dexterity. A humanoid may even resemble human biomedical features, e.g., nervous systems for sensory input and motor control, circulatory systems for energy and movement circulation, and respiratory and energy systems for metabolism, storage and control. 

**Humanoid behavioral likeness** refers to the extent that a humanoid emulates the actions, reactions, emotional expressions and interactions of human body parts and systems. Recalling humanoid behaviors in Section 3.1.4, behavioral likeness captures the body language, gestures, postures, and movement of body parts of humanoids over humanoid physical likeness. These reflect the design and functionality of humanoid locomotion in reproducing human-like movement mechanisms, styles and patterns [51], such as for humanoid walking, grasping, and dynamic adaptation and balance. Further, the likeness of humanoid gait, facial expressions, tone of speech, spoken and motion emotions facilitates human-like verbal and nonverbal communications, affections and interactions. In social contexts [10], behavioral likeness enables human-like social behaviors, teamwork, cooperation and collaboration, and adaptive responses during social interactions between humanoids and between humanoids and humans. 

**Humanoid sociocultural likeness** refers to the extent that a humanoid exhibits its functions, attributes and behaviors aligned with human ethical, moral and social norms, cultural appropriateness and values, and sociocultural traditions and boundaries during social contexts and dynamics. Social and cultural likeness characterizes humanoid abilities of respecting social roles, cultural cues, sociocultural norms and religious sensitivity while undertaking sociocultural tasks, behaviors, interactions and engagement [31, 44]. It determines the extent that situational humanoids are embodied with culturally relevant appearances, symbols, and settings and have the awareness of social and cultural norms, courtesy and etiquette. Humanoids demonstrate the language and dialect adaptation in human-humanoid conversations, the culturally appropriate gesture and body language during nonverbal communications, and the culturally sensitive emotional expressions and responses. Sociocultural humanoids also understand, respect and exhibit social intelligence, commonsense, empathy, and emotional appeal for engaging and pleasing user experience, and situational reasoning during social activities and contexts. 

**3.2.2 Humanoid Capability Maturity** _Humanoid capability maturity_ measures the proficiency of ability, functionality and sophistication of humanoids in pursuing their objectives and performing their tasks. Humanoid capabilities 

Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

21 

traverse cognitive, perceptual, physical, behavioral, emotional, communicational, linguistic, and interactive abilities. We structure humanoid capability maturity into three dimensions: _intelligence capacity_ of reproducing human intelligence, _functional capability_ of undertaking tasks, and _complexity resilience_ in handling sophisticated tasks, data and environments. While these may involve nonfunctional capabilities of humanoids, here we focus on functional competence which may be quantified in terms of their maturity levels and assessment specifications, criteria and measures. 

**Humanoid intelligence capacity** assesses the spectrum, capabilities and intensity of intelligence paradigms of humanoids in replicating human intelligence. Intelligence capacity spans over and meta-synthesizes diverse qualitative to quantitative human intelligence [12], including _cognitive intelligence_ for humanoid mental mechanisms, intentionality, and personality; _perceptual intelligence_ of humanoid vision, audition, and other sensory mechanisms and abilities; _emotional intelligence_ of humanoid emotion recognition and simulation; _interaction intelligence_ of humanoid collaboration and competition, and verbal and nonverbal communication; _social intelligence_ of humanoid-human interactions, cultural adaptation; _data intelligence_ of humanoid data acquisition, analytics and management; and _learning intelligence_ of humanoid representation, learning, reasoning, memorization, and generation. The capacity of humanoid intelligence builds on AI techniques and approaches [16] for implementing the paradigms of human intelligence. A humanoid may be empowered by individual or hybrid intelligences to perform their tasks and fulfill their functions. 

**Humanoid functional proficiency** refers to the degree of competence and skills of a humanoid in performing their tasks and functions illustrated in Section 3.1. Humanoid functional proficiency can be customized into _cognitive proficiency_ of implementing humanoid brain, _physical proficiency_ of implementing anthropomorphism, _perceptive proficiency_ of performing vision, speech, hearing and other sensory functions, _behavioral proficiency_ of achieving activeness, _connective proficiency_ of performing networking and communications, _interactive proficiency_ of conducting collaboration and competition, _organizational proficiency_ of planning and search, _knowledge proficiency_ of representation, analytics, learning, reasoning and recommendation, _cybernetic proficiency_ of conducting manipulation and control, _generalizable proficiency_ of achieving adaptation and optimization, and _system proficiency_ of humanoid design and implementation. Humanoid proficiency may also be categorized into _task-specific proficiency_ in undertaking a specific task, _nonfunctional proficiency_ and other specific types of proficiency [57], such as _emotional proficiency_ of demonstrating empathy, and _social proficiency_ of engaging humans and adapting to social, ethical and cultural norms. Most humanoids as shown in Table 2 [18] only possess basic to intermediate levels of proficiency of some of these aspects. For example, few humanoids like Ameca have the potential of incorporating _cognitive, sentimental or emotional states and features_ , such as facial expressions. In addition, social humanoids may hold humanized features and traits, such as personality as embodied by extroversion, agreeableness, conscientiousness, neuroticism and openness [31]. 

**Humanoid complexity resilience** refers to the ability of humanoids to robustly, flexibly and adaptively perform their tasks and functions in uncertain, sophisticated, difficult, and unexpected systems, conditions and environments [13]. Complexity resilience measures _goal complexity resilience_ of complex humanoid objectives and expected outcomes; _task complexity resilience_ of humanoid task complexities such as complex task settings, dynamics and evolution; _system complexity resilience_ of humanoid design and implementation complexities; _data complexity resilience_ of humanoid data complexities such as heterogeneity, non-IIDnesses and interactions [11]; and _environmental complexity resilience_ of environmental and contextual complexities such as heterogeneous, dynamic and coupled contexts. Humanoid resilience can also capture other aspects, such as _cognitive resilience_ in handling cognitive goals, tasks and contexts; _physical resilience_ in building robust structures and components and efficient designs; and _social resilience_ to cross-cultural contexts and diverse social practices. Humanoids are still in the early stage of embedding complexity resilience, with the current focus on task robustness in multimodal and changing contexts [77]. 

Manuscript submitted to ACM 

Cao 

22 

**3.2.3 Humanoid Performance Evaluation** _Humanoid evaluation_ verifies and validates functional and nonfunctional performance of executing their requirements and specifications. The evaluation criteria and measures are both objective and subjective, and technical and nontechnical. The aspects to evaluate spans over humanoid objectives, designs and performance [41], from state to behavior, from domestic to social, from individual to collective, from physical to virtual, and from implicit to explicit. These evaluation aspects can be inspected per _task performance_ at design time, _operational performance_ at running time, and _application usability_ by end users and for applications through design evaluation, simulation testing, field testing, stress testing, and user feedback. These evaluate whether a humanoid is technically and operationally capable, effective, efficient, usable, compatible, portable, trustful, responsible, explainable, transparent, safe, compliant, secure, accountable, reproducible, maintainable, and interoperable. 

**Humanoid task performance** evaluates how good a humanoid conducts its designs and functions, i.e., the quality of functions. Functional performance can be assessed in terms of goodness of functionality, design and tasking [13, 68]. First, the _goodness of humanoid functionality_ assesses the quality of functions, i.e., how good a humanoid performs its functions from part to whole. Functionality goodness can be quantified in terms of the completeness, creativity, maturity, effectiveness, stability, robustness, versatility, agility, dexterity, objectivity, trustfulness and responsibility of humanoid functions and technical capabilities. Humanoid robustness evaluates the generalizability of humanoid functions and designs. Humanoid objectivity measures the fairness and unbiasedness of humanoid components, algorithms, and their decision-making and results. Humanoid trustfulness evaluates the unidirectional, reciprocal and bidirectional human-humanoid reliability and confidence by humans in a humanoid’s roles, capabilities, actions, functions, decisions, and performance. Second, the _goodness of humanoid tasking_ examines the quality of performing tasks by customizing and configuring functions for specific tasks, scenarios, and use cases. Tasking goodness can be evaluated in terms of flexibility, configurability, adaptability, comparability, transferability and capacity of applying functions to ad hoc, specific, multiple and domain-oriented tasks and task execution performance. Task execution may be estimated by quantitative to qualitative performance measures, such as requirement met rate; throughput and capacity of transactions, tokens, requests and users to accommodate; successful completion rate, and task success rate; consistency within tasks and comparability across tasks and scenarios; adaptation to different tasks, domains, contexts, and applications, as well as common measures like accuracy and precision. Last but not least, the _goodness of design_ measures the quality of design. Design goodness may be evaluated in terms of measures such as design modularity, analyzability, reliability, scalability, transparency, explainablity, accountability, testability, reusability, reproducibility, and recoverability. Examples include modularity of interchangeable and independent components; reliability of available operational uptime, error and fault tolerance, failure rate, mean time between failures; durability of functionality and performance over time, changes or failures; analyzability of understanding algorithm, system and decision and diagnosing problems; scalability over user, load and request increase; reusability of components; recoverability from failures or faults and recovery time and effort; and testability of functional modules and their integration. 

_Humanoid trustfulness and responsibility_ . Factors influence human trust in humanoids may be various [43], e.g., lack of emotional intelligence, limited ability to adapt to new situations, unclear decision-making processes, privacy concerns, negative media portrayal, unclear code of ethics, or regulatory oversight. The trustfulness and responsibilities of humanoids are embodied by various functional and nonfunctional mechanisms and measures, such as reliability, adaptability, security measures, programmed ethical guidelines, intention transparency, ethical behaviors, ability to self-control and self-regulation, trustful past track record, and subjectivity such as empathy and responsibility. These humanoid trust factors and measures are embodied by the trustfulness [24] in humanoid design, behaviors, effect and performance, such as automation, live recognition, and real-time prediction and decision-making; the predictability Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

23 

and transparency of risk, safety, security and consequence; the detection, prevention and resolution of system issues such as faults, unsuccessful task completions, and irreparable mistakes. As subjective properties increasingly affect the humanization of robots, enforcing the morality of humanoids essentially enables what moral liability, accountability, rights and responsibilities a humanoid should hold and how such attributes should be distributed in multi-party settings. However, humanoid empathy would not serve as the final guard rail. Humanoid trust may further require robotic legal rights, such that a humanoid must not incur human injuries and must obey orders. This triggers the study on the rights of humanoids and artificial consciousness, e.g., whether a humanoid is a legal entity, and to what extent a humanoid can be given what legal rights comparable to humans. Humanoid legal rights are crucial for humanoid services like law enforcement and being a robo-adviser, an elderly companion, or a child caregiver. 

**Humanoid operational performance** evaluates how good a humanoid is operated, i.e., the quality of operations (or quality of services). Operational performance can be evaluated against performance measures [13], such as autonomy, standardizability, operability, interoperability, compatibility, transparency, explainability, efficiency, elasticity, safety, privacy preservation, risk compliance, and cost-effectiveness. _Humanoid autonomy_ refers to the level of automation when a humanoid operates and governs independently. _Humanoid standardizability_ measures the adherence to widelyacceptable development, industry and data exchange standards or protocols. _Humanoid operability_ measures operational competence under different scenarios and conditions, such as online and cloud-based development support, deployment environment of terrain and temperature, and service and testing facilities. _Humanoid interoperability_ and _compatibility_ determine the connection, communication, interaction, collaboration, and integration of a humanoid with other robots, devices, modules, systems, and environments, and mobility in different terrains and environments. _Humanoid efficiency_ may be quantified by measures such as computational efficiency, latency and response time of task and request, task execution time, CPU and GPU time, memory cost, bandwidth, resource consumption, energy efficiency, and decisionmaking efficiency. _Humanoid elasticity_ measures performance stability under changes, such as humanoid workload changes without efficiency degradation, and consistency across tasks. _Humanoid adaptability and flexibility_ measure operational performance under new or unexpected conditions, environments or contexts, with new objects or tasks, over time or space, and with responses to dynamics, changes and unexpected scenarios. 

The _humanoid transparency_ , or opacity, of robotic designs, behaviors and outcomes affects human confidence in humanoids and their applications and services. Two mechanisms to ensure humanoid transparency are explainability and reproducibility [35]. _Explainability_ provides mechanisms, tools and interfaces to understand and interpret humanoid designs, working mechanisms, behaviors, outputs, and consequences. _Reproducibility_ ensures the repeatability, consistency and integrity of humanoid designs and outputs under the same circumstances. Explainability and reproducibility become increasingly essential for complex humanoid designs and tasking. Transparency, accountability, auditability, explainability and reproducibility are essential in implementing humanoid automation, and on-the-fly and in-the-wild design, operation and decision-making with open settings. 

_Humanoid safety_ . _Physical safety_ includes no unintentional or unwanted contact between humanoids and humans or comfortable physical contact with force below thresholds or without physical harm [47, 63]. _Psychological safety_ comprises indirect psychological harm, discomfort or stress such as human trust, unexpected intention, and negative emotions. Safety can be ensured by careful programming, safety criteria and constraints such as biomechanical limits, injury prevention, control strategies, and assurance mechanisms such as detecting, predicting, preventing and intervening with force, collision, falling, crash, risky and abnormal activities. In open settings, safety monitoring, detection, prediction, prevention and intervention are essential for novel, cold-start, evolving and changing scenarios and accidents. _Humanoid security_ further enforces requirements on data and programming integrity with authentication 

Manuscript submitted to ACM 

Cao 

24 

and modification restriction, confidentiality of resources and IP for authorized users, authorization and permissions for users and developers, and auditing by monitoring, logging and tracing actions and non-repudiation of actions. 

_Humanoid risk and compliance_ . A humanoid may be exposed to various risky scenarios or actual risks [38]. They include methodological and technical risks, such as fragile generalization, faulty design, and incomplete compliance; malicious manipulation such as misuses, misinformation, malicious attacks, and manipulated behaviors and automation; and ethical issues such as deception and privacy concerns. Humanoids may also exhibit unexpectedness such as hallucination of automated generation, and singularity and superintelligence of self-improvement and intelligence emergence, when they gain control and rights beyond human perception and acceptance. As automating real-time, interactive, decentralized and personalized humanoid tasks and operations become predominant, _humanoid surveillance_ not only requires automated, real-time, tailored and predictive risk and compliance monitoring, diagnosis and management, but also human surveillance i.e. keeping human in the compliance loop. In this regard, significant challenges exist in real-time and automated scenario-oriented human-humanoid regulation, e.g., in accountable human-humanoid role allocation and responsibility sharing, efficient regulation in complex settings, privacy-preserving surveillance, risk-aware human-humanoid cooperation, and essential human-centered control and mitigation. 

**Humanoid application usability** assesses the applicability and user-friendliness of a humanoid in applications. Evaluation criteria and measures may include humanoid usability, deployability, installability, maintainability, satisfaction, learnability, accessibility, and recoverability [21, 37]. _Humanoid usability_ can be assessed by interface and interaction friendliness; ease of operations and use at different platforms, channels, network conditions; user experience, acceptance and satisfaction; learnability by new users; accessibility of disabled, aged or disadvantaged users; use efficiency of time and effort; error tolerance to errors, mistakes; noise level and disturbance; and ease of recovery. _Deployability_ measures humanoid conditions and constraints of deployable applications, areas, environments, facilities, networking, communication, and space. _Installability_ measures how easy to install, configure, debug and test the humanoid, its plug and play, and conditions and requirements on installation technicians and services. _Maintainability_ assesses the competence of modular design principles; ease of repairs, updates, modifications, and upgrades; recovery difficulty level; and maintenance interfaces, guidelines and wizards. _Supportability_ evaluates the technical support e.g. by documentation, visualization, virtual reality or training, and their service costs and time availability. 

**3.2.4 Humanoid Impact Estimation** The outcomes of applying a humanoid foster humanoid impact across intellectual, economic, environmental, social and ethical aspects. They measure the impact and benefits of humanoid technical advancement, market valuation, environmental sustainability, societal contribution, and ethical implication. 

**Humanoid intellectual impact** measures the influence of humanoid technologies, systems and processes on technological innovation, knowledge advancement and creation, and problem-solving capabilities. Humanoid technology fosters a new research area towards technological innovation and creation, and new research and development opportunities. This spans over both foundations of enabling and developing humanoids and applications of humanoids in diverse domains and sectors. The various and significant humanoid intellectual impacts include driving technical competitiveness, intelligence level, and automation; fostering new humanoid-related knowledge advancements, expansion and accessibility; augmenting human autonomy of amplifying human intellectual capabilities, efficiency, and performance; enabling human-humanoid collaborative superintelligent systems and services, unresolvable by human alone; amplifying personalized learning capabilities, methods, experience and effect; cultivating interdisciplinary innovation by integrating humanoids into other fields such as humanoid health and medicine; and inducing skill development and upgrading, and expertise transfer. These intellectual impacts will further drive economic, social, 

Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

25 

ethical and environmental impacts, such as promoting industrial performance improvements, cognitive load reduction, and production efficiency. Intellectual impact can be measured by relevant factors, such as technological advancement level, creativity level, technological adaptability, task efficiency, task success rate, and problem-solving efficiency. 

**Humanoid economic impact** is embodied through humanoid-enabled and -augmented economic opportunities and benefits [13, 67], such as novel products and services, job creation, productivity gain, efficiency augmentation, cost reduction, market expansion, industry transformation, and economic resilience. Humanoid technology is boosting the _humanoid industry_ and _humanoid economy_ , fostering new humanoid-driven industries, products, services, and activities [15]. The deployment of humanoids to diverse business domains, industry sectors, and social areas promotes _productivity gain_ and _efficiency augmentation_ such as by new manufacturing industry, industrial automation, augmenting production efficiency, automating production and services, and improving service quality and delivery by humanoids. Humanoid technology also transforms existing industry and economy, in particular, education, services, marketing, entertainment, and hospitality [13]. Humanoid can also deliver unique economic and social impact in areas like disaster response and rescue, agriculture, and defence and security industry. The _humanoid ecosystem_ further drives job creation, displacement, up-skilling and transformation with new job roles and responsibilities from humanoid R&D to production, logistics, sales, marketing and technical services. The economic resilience can be strengthened by humanoid technology, including humanoid technological affordability, maintainability, extendability, and upgradability of their purchase, operations and maintenance in daily work and life. Humanoid technology produces advantageous financial and productivity outcomes, measurable by economic impact factors, such as competitive advantages, market acceptance, automation level, production efficiency, revenue growth rate, cost efficiency and cost-benefit ratio, productivity gain, reduced operational costs, enhanced personalization of intelligent services. 

**Humanoid environmental impact** refers to the influence of humanoid technology on sustainable development and environmental areas, benefits and opportunities. The environmental impact can include developing sustainable humanoid technology, industrialization and economy, and contributing to environmental sustainability. _Sustainable humanoids_ comprise computing-, resource- and energy-efficient, sustainable humanoid design, innovation, development, production, logistics, services, and practices. Examples include light-weighted architectures; restricted consumption of CPU, GPU, network, communication and energy; resource utilization in production and operation; technological sustainability such as eco-friendliness and net-zero design, durability, maintenance costs, and lifecycle assessment; longevity such as period of functioning, expiry period, cost of maintenance, and extendability over time; and modular compatibility with other technologies and products. _Humanoid environmental sustainability_ measures the ecological consequences of humanoid technology and eco-friendly and sustainable applications and practices. Examples of humanoid ecological outcomes include depletion, emission, waster and pollution generation and reduction by humanoids; and recyclability of humanoid materials, components, and design. Examples of sustainable humanoid applications include protecting and restoring damaged environments; enabling renewable energy integration; and monitoring, analyzing and intervening environmental changes. Humanoid applications to environmental areas include humanoids for precision farming, weeding, irrigation and pest control; smart urban, home, society, city, transport, waste, recylcing and utility management and monitoring; diaster response; and wildlife protection and conservation. 

**Humanoid social impact** refers to the influence of humanoid technologies on human lives and societal areas, benefits and opportunities. Social impact may include improving social businesses and applications, social diversity, equity and inclusion (DEI), social interactions and community building, public safety and security, technology democratization, and life quality and social well-being through a societal acceptance of humanoids. Humanoids can benefit _social businesses_ [44] such as healthcare, welfare and wellness through assisting in urban-based, aged, elderly, disabled, or marginalized 

Manuscript submitted to ACM 

Cao 

26 

individuals and communities. Humanoids can promote _DEI objectives_ such as by expanding education accessibility, knowledge transformation, and personalized services to those disadvantaged areas and populations. Humanoids can also facilitate _social connections_ , cultural engagement and community cohesion. The roles of humanoids in monitoring, analyzing, intervening and improving _safety, emergency, threat, hazard and disaster_ accidents and aiding in search and rescue responses. Humanoids have been used to improve _life quality_ , such as engaging transportation, animation, digital arts, entertainment, and hospitality [31]. Humanoids can support _democratization of technologies and knowledge_ towards improving individual, organizational and social capabilities and benefits in rural, disadvantaged areas and less technology-savvy domains and communities; and _equity_ between social groups, such as equitable access to humanoid benefits by bridging digital and technological barriers. 

**Humanoid ethical impact** refers to the influence of humanoids on ethical concerns and opportunities. _Ethical concerns_ traverse uncanny valley effect, disruptions, and humanoid transparency, trust, fairness, privacy, vulnerability, and accountability [28]. _Ethical opportunities_ include addressing misinformation, improving humanoid humanization and intelligence, and leveraging human intelligence. Addressing eerie feelings of humanoids or negative emotional response of humans by human-looking humanoids concerns about the humanoid humanity dilemma - a humanoid realization of “almost but not quite" human, and the loss of human uniqueness and identity. Addressing this effect for widespread societal acceptance of humanoids should accommodate humanity into humanoid anthropomorphic likeness and address technical, material and operational complexities and constraints. Humanoids may induce social, cultural, societal, economic and ethical disruptions such as job displacement and humanoid-human-coexisting societies and norms. Humanoid ethical and technological adaptation must articulate subjective human traits in humanoids, such as humanoid personality, and societal, moral and legal considerations and requirements [44] on humanoid responsibility, trust and ethics. The development, management, governance and regulation of humanoids and their data, algorithms and platforms also require corresponding ethical, legal norms and laws, such as enforcing traceability to specific metrics, factors and modules; accountability of ownership and responsibility; transparency of decision criteria, process and outcomes; privacy concern in data processing, collection, algorithmic recommendation, and parameter sharing; and safety concern such as on human incidents, compliance with safety standards and design specifications, and threat or trouble to users and surroundings. While pursuing human-centric humanoid attributes, aesthetics and automation, it is also important to balance human creativity and humanoid intelligence, and assure humanity, human identity and well-being, including enforcing risk compliance on potential disinformation, misinformation, and fake information. 

_Humanoid ethics_ Robot ethics[28] concerns about the privacy, manipulation, opacity and bias of robotic systems and the equilibrium effect and consequence of robotic designs, mechanisms (e.g., autonomy and predictive decision-making) and behaviors during operations, decision-making and human-robot interaction. _Ethical humanoids_ are built with transparent, fair and unbiased design and decision-making; proactive compliance, due process and auditing to potential effects, influences, vulnerability, deception, misinformation, synthetic issues, failures, changes and uncertainty; and accountable compliance, interference and intervention measures and mechanisms. Humanoids may further involve humane aspects such as confirmation bias, deception, malicious design, attack and manipulation. Depending on the level of ethical enforcement, a humanoid may be explicitly ethical, implicitly ethical, or fully ethical. 

## **4 Realistic Humanoids: Other Perspectives** 

The comprehensive analysis of existing humanoids in Section 2, as outlined in Table 2 [18], and the systematic discussion on functional and nonfunctional specifications of humanoids in Section 3 disclose various gaps, limitations of existing work and the implications for building new-generation humane humanoids. Fig. 2 highlights other perspectives and Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

27 

directions in developing humanoid AI: humanoid humanity, mind-to-action, biomedicine, animation, virtual-real humanoid mapping and symbiosis, metaverse, humanoid-human symbiosis, generation, decentralization, standardization, and quality of services. With space limitation, this section expands Section 3 to several other perspectives and directions: cultivating humanoid humanity and subjectivity, building _mind-to-action_ mindful and actionable humanoids, supporting transitional omnimodal humanoid modeling, and hybridizing virtual-real humanoid-human-metaverse symbiosis. 

### **4.1 Addressing Humanoid Humanity Dilemma by Developing Humane Humanoids** 

Addressing the humanoid humanity dilemma is ambitious with many grand challenges. We briefly discuss the maturity and applicability of existing AI advances to humanoids, the constraints on humanoid systems, and the challenges in developing human-level humanoids. 

First, in addition to issues and challenges, such as hallucinations, of existing generative AI, humanizing humanoids is also challenged by data, modeling, evaluation, ethics, societal and human complexities relevant to humanoids. Typical issues include bias and fairness, distribution shift, contextual understanding, multimodal capabilities, personalized sparse satisfaction, adversarial attacks, misinformation and disinformation, manipulation and deception, observation and data overreliance, overfitting or overmanipulation, lack of thinking and humanity, and potential adoption of technical, security, privacy, ethical, economic, psychological, sociocultural or sociopolitical risks into humanoid systems. 

Second, humanoids pose specific constraints and challenges in developing humane and human-level robotic intelligence. There are limitations on humanoid locomotion, mechanics, sensing, responding capabilities, memory, degree of freedom, dimensionality, modality, and computational capabilities, which cannot support LLMs and LMMs on humanoids without edge and cloud networks. More fundamental limitations lie in the existing designs and mechanisms of enabling on-humanoid intelligence such as vision, perception, learning, memorization, control, planning, and actions. Simulating and replicating human intelligence into humanoids requires substantial theoretical and practical advancements in humanoid systems and their cognition, humanity, biomechanics, and behavioral studies, etc. To avoid the uncanny valley phenomena and risks of humanoids and issues like hallucinations of GenAI-driven humanoids, humanoid robotics expects not just human-looking machines but humanness [31] and humanity into humanoids. This requires humane expression, behaving, response, interaction, conservation, and collaboration to make users feel comfortable and safe emotionally and psychologically in interacting and collaborating with humanoids. 

Accordingly, human-level humanoids requires new-generation AI and human-level humanoid AI customized for humanoids toward developing human-like robotic intelligence before aiming for any superintelligence or superhuman intelligence [70]. Tangible opportunities include developing 1) on-humanoid encoding or decoding-based LLMs, VLP, VLM and LMMs; 2) humanoid-edge-integrative (local server or multiple humanoid networks) LLMs and LMMs; 3) partial humanoid humanity; 4) human-like humanoid intelligent capabilities such as inspired by children learning procedure, and human personality, intentionality, subjectivity and empathy under positive, negative and neutral scenarios and activities; 5) human-like social humanoid intelligent capabilities such as team coordination, cooperation, competition, and conflict resolution during social interactions. 

### **4.2 Cultivating Humanoid Humanity and Subjectivity** 

Without humanity and subjectivity, humanoids are only machines with issues like uncanny valley effect and the humanoid humanity dilemma. Characterizing humane and subjective traits, attributes, qualities and states of humanoids is fundamental for being humankind, human-like to human-level [17]. Humanoid humanity can be embodied through humane attributes such as personality, morality, intentionality, compassion, sentiment and emotion, enabling and 

Manuscript submitted to ACM 

Cao 

28 

managing responsible, trustworthy, sympathetic and ethical individual and collective disposition, behaviors and decisions by humanoids. 

Existing work on embodying such humane and subjective attributes, traits and qualities into humanoids is very limited but focuses on facial expressions, perception and observations. Examples are human mood modeling, such as visual facial expression recognition, textual semantics such as by topic modeling and sentiment analysis, and human body state modeling such as posture recognition [59, 61]. They are observational. Embodying and modeling humanoid humanity and subjectivity requires new thinking and theories beyond the existing humanoid design enabled by observations, such as modeling cognition and mental processes discussed in Section 3.1.2. 

Fundamentally, a theory of humanoid humanity and subjectivity is essential. This include designing humanoid humanity models, quantifying humanoid subjectivity, structuring humanoid trustfulness, simulating humanoid subjectivity, benchmarking humanoid subjectivity, and developing rules of law for humanoid humanity and subjectivity. 

- Characterizing humanoid humanity: characterizing and learning humanoid personality, intentionality, consciousness, empathy and trust in real time and live scenarios; defining, imitating and simulating attributes e.g. extroversion, conscientiousness, neuroticism, aggressivity, emotion and intention; and quantifying them in terms of multimodal vision-to-language and perception-to-action tasking, or self-motivated empathy etc. 

- Structuring humanoid trust and responsibilities: defining, specifying and simulating the trustfulness and responsibilities of humanoids by humans and humanoid perception and confidence in humans during humanoid and human interaction and collaboration; modeling trust [84] and responsibility in context of perception-toaction pretraining and finetuning, e.g., quantifying humanoid’s LLM and perception-to-action performance with performance measures and criteria such as robustness, reliability, accuracy, and user satisfaction; formulating humanoid’s self-regulation and self-assessment capability and mechanisms, e.g., accountability, interpretability, and exception resolution; exploring symbiosis between external regulatory agents and humanoids for humanoid ethical assurance, and functional and nonfunctional regulation and governance. 

- Humanoid humanity simulation: creating use cases, strategies and simulation testbeds for mimicking, generating, implementing, monitoring and adjusting humanoid personality, intentionality, empathy and trust; simulating humanity dynamics and evolution over interactions and collaborations; simulating and controlling subjective expectations under scenarios such as self-improving emergence, immoral and irrational actions, free of risk and compliance regulation. 

- Benchmarking humanoid humanity and subjectivity: developing benchmarkable database, use cases, testbed and checklist for experimentation and case studies of humanoid personality, intentionality, consciousness, empathy and trust; exploring open platforms for uncertain, diversified and large-scale scenarios such as self-improving emergence and hallucination, sampling and algorithmic biases, and irreparable mistakes. 

- Rules of law for humanoid humanity management: discovering and summarizing general principles, rules of law for monitoring, detecting, predicting, intervening and managing personality, intentionality, consciousness, empathy and trust of real-time, interactive and multimodal humanoids; identifying verifiable rules and code of conduct for different use cases, such as humanoid tasking, humanoid-human teaming and interactions. 

### **4.3 Mind-to-Action for Mindful and Actionable Humanoids** 

The concepts of AI mind, mindful AI with AI mindfulness, and AI action, actionable AI and AI actionability [14] apply to humanoid AI as well, aiming for producing mind-to-action-embodied mindful and actionable humanoids. Humanoid mind modeling is essential for enabling cognitive humanoids and cognition-to-action translation and transformation. Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

29 

First, making humanoids human-like and humane requires developing humanoid mind and mindful humanoids. A _mindful humanoid_ with AI mindfulness simulates and amalgamates human mind and mindfulness to develop _humanoid mind models_ and _humanoid mindfulness_ . Mindful humanoids may fulfill relevant human thinking mechanisms, cognitive and psychological traits, sensation, reasoning, and critical analysis capabilities. They are also mindful of their personality, intentionality and emotion while pursuing goals, plans, activities and effects. 

Second, humanoids undertake various actions relating to their mind, goals, tasks and environments. _Actionable humanoids_ not only conduct such actions but also make them meaningful and valuable technically and practically, i.e., making humanoids actionable. The _actionability_ [19] of humanoids, including their designs, actions, and performance, satisfies various performance measures, e.g., interpretable to end users, convertible to business value and impact, and satisfying business, social and economic measures, as outlined in Section 3.2. 

Further, a humanoid as a closed-form independent AI system needs the transformation from mind to action. _Humanoid mind-to-action_ enables a real-time translation and transfer from subjective mindfulness to actionable operations and activities; the reflection and feedback on actions to mind; and the iterative processes between mind and actions over a task period. This mind-to-action translation raises many research challenges and opportunities, such as building mind models for humanoids, and enabling mind representation (e.g. decomposed to intention representation, sentiment and emotion representation), dynamic and interactive alignment between mind and actions, and coordination between multiple thoughts and their corresponding actions. 

Mindful humanoids are cognitive, replicating and tailoring human cognitive intelligence, traits and properties into humanoid cognitive models. Humanoid cognition can be characterized by representing humanoid’s intention, affection, emotion, speech, gesture, actions, haptic signals, and physiological signals. The mind-to-action translation demands _cognition-to-action_ modeling and translation, integrating relevant modeling tasks such as personality modeling, intention learning, goal learning, emotion learning, action learning, and behavior learning, and translating learned knowledge on humanoid cognition to their actions. 

### **4.4 Transitional Omnimodal Humanoid Modeling** 

Humanoid mind-to-action builds on the quantification of humanoid subjectivity (e.g. personality, intention, sentiment and emotion) and the development of humanoid mind models. It also depends on the fitting, alignment, reasoning, inference and matching of omnimodal mind-to-action translation [17]. This requires further studies on transforming and translating from vision-language modeling and vision-to-action modeling into mind-to-action modeling and perception-to-behavior modeling. 

The _perception-to-behavior_ transition, translation and transformation involve multiple to omniversal modalities from visual, acoustic and textual to behavioral aspects. It further raises issues including multimodal to omnimodal perception fusion by synergizing visual, vocal, textual and behavioral representations; point-based, sequential, spatial or function-oriented fitting, alignment and matching between image (or video), sound and text for the same task or object; and temporal, spatial or spatiotemporal developments of multimodal perceptions and behaviors. 

In recent years, an increasing attention has been paid to multimodal deep learning and specifically LMMs, such as visual query-answering (VQA), VLMs, VLP, image-language pretraining, image-to-text generation, and text-to-image generation. Building on Google Robotic Transformer 1 (RT-1) on multitask modeling [8], Google Robotic Transformer 2 (RT-2) [86] further supports high-capacity VLA modeling on web data and robotic vision data, and translates the learned knowledge into generalized instructions to control robotic actions. RT-2 uses the pathways language and image model (PaLI-X) and pathways language model embodied (PaLM-E) as the backbone. 

Manuscript submitted to ACM 

Cao 

30 

### **4.5 Virtual-Real Humanoid-Human-Metaverse Symbiosis** 

### **4.5.1 Humanoid Digital Twins and Metaverse** While the integration of humanoids with digital twins and metaverse 

is an open area yet explored, it can nurture novel humanoid animation, humanoid societies, or even humanoid-human coexisted digital twins or metaverse continuum. By integrating techniques including humanoid robotics, LLMs and LMMs, digital twins, metaverse, decentralized AI, Web3, 3D design, and operating and software systems, humanoid digital twins and metaverse can augment humanoids, promote bidirectional humanoid virtuality-reality transfers, and cultivate virtuality-reality-symbiotic humanoid-human-coexisted metaverse ecosystems. 

First, humanoid digital twins and metaverse surpass humanoid capabilities and capacity. Metaverse, digital twin, and virtual, augmented and mixed reality techniques can assist human-humanoid interaction, interfacing and collaboration in creating metaverse-humanoid-human collaborative design, development, workplace and tasking settings [4, 22, 75, 80]. On-humanoid, on-body or on-environment animation, metaverse and mixed reality can augment humanoid’s collaborative programming, teleoperation in projected environment and background, navigation trajectory visualization, immersive and expressive perception and telepresence. For example, by creating a 3D presentation of a humanoid and its workplace, a humanoid can be operated, monitored or tutored for specific tasks in its working environment [37]. Instructors with multi-modal virtual, augmented and mixed reality devices can operate and control humanoids and conduct various tasks, such as imposing humanoid movement restrictions, trajectory teaching, changing humanoid joint angles, and creating task-specific programs. For human-unfriendly environments, humanoids can be teleoperated to undertake specific tasks remotely using projection mapping to facilitate robotic tasks [26]. 

Second, by integrating with simulation platforms and creative technologies, humanoids can be teleoperated in a digital twin. Initial physical scenes (such as medical test) could be captured and analyzed in the physical world, then converted into the virtual world (e.g., input into 3D simulators) for further manipulation and analysis. Optional actions (e.g., medical treatments) could be tested in the virtual world. Those verified by professionals (e.g., a doctor) could then be deployed to humanoids for actions (e.g., guiding a patient’s teletreatment). For example, a cybernetic avatar [37] is a teleoperated human-like and life-like alter ego of its human operator. Further, in a virtualized real world, a remote operator, its avatar, and a virtual agent (mapping of the avatar) may co-exist in a symbiotic society, where the operator manipulates the virtual agent, which further instructs the avatar to behave and perform like the operator. The avatar mimics facial expressions, eye gaze, gesture, spoken voice, and even mental state and personality of the operator, which are transited through the virtual agent in the avatar online operating platform. 

Last but not least, humanoid digital twins and metaverse can transform digital innovations, such as digital health, finance, marketing, customer services and disaster management [15, 37]. For example, a _humanoid general practitioner_ (HGP) may offer online telehealth services as follows [17]. Once receiving the appointment request by a patient, the HGP may launch its virtual digital twin or metaverse platform, where a virtual digital human illustrates, inquires and discusses health or medical concerns and symptoms with the patient. The patient can tell her problems, upload her medical test results to the metaverse. The HGP can then extract, process and analyze the uploaded materials, animate, illustrate and explain the patient’s problems through the digital twin mapped to the patient per her demographics and medical conditions, and make assessment of the patient’s complaints. Further diagnosis and treatment suggestions may be made and explained to the patient using the digital human. All discussion, materials and HGP diagnosis and analysis can be sent to a human doctor for verification, adjustment or confirmation. This HGP with health digital twin could save time, extend coverage, and augment service depth and health education of healthcare and telehealth. A similar example for digital finance would be humanoid robo-advising integrating humanoids with metaverse. 

Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

31 

### **4.5.2 Humanoid Animation, Imitation and Simulation to Operation** Simulation, imitation and animation can support humanoid virtuality-to-reality and augment humanoid capacity, operations and performance. 

**Humanoid Animation and Simulation to Operation** Large-scale humanoid experiments and practices are costly, risky, insecure, unsafe or unactionable. _Humanoid animation, simulation and programming_ provide theories and tools to mimic, evaluate, adjust, optimize and program humanoids in a virtualized cost-effective platform before their confirmation, production and deployment [37, 55]. Robotic animators and simulators may provide interfaces, methods and functions to describe, select, connect, code, expand and manage humanoid goals, types, parts, coordinates, objects, environments, functions, tools, workflow, paths and behaviors in a 2D or 3D animation or simulation platform. They can simulate physical systems, activities and processes and generate, compile and deploy animated, simulated or optimized programs into physical robots for further experiment, prototyping, production or deployment. Humanoid animation and simulation may clone, virtualize, imitate or replicate human body parts, attributes, behaviors, emotions, conversations and expressions, and generate humane robotic parts, properties, emotions and actions for more human-like appearance, presentation, and mechanisms. Further, humanoid learning, planning, control and interaction by animation and simulation emerge as essential mechanisms for humanoid robotics at scale. Humanoid animation, simulation and programming may face _simulation-to-reality gaps_ (Sim2Real) from real-life humanoid appearance, design, manipulation and experiment. This gap may relate to misalignment between simulation and reality, and the unrealisticness and poor anthropomorphism of simulation assumptions and constraints on simulation settings, platforms, essential and sufficient toolsets, programming tools, and simulator behavior settings, capabilities and capacity. 

**Humanoid Imitation to Operation** _Imitation learning_ is another type of simulation or demonstration. Humanoids learn by demonstrations or are taught by a supervisor, a demonstrator or examples, such as from virtual simulations or a filmed physical scenario (a video), and then clone, imitate or adjust the demonstrations or examples. Humanoids may also learn an underlying optimal reward function or policies from teachers, adapt to taught examples, develop or generate new behaviors [77]. Humanoid imitation thus supports behavior cloning, intent learning, behavior or scene prediction, recommendation or generation. By integrating techniques like DeepFake, animation, LLMs and digital twins, humanoid imitation could learn from sequential, hierarchical, multimodal and live human activities, and social activities; processes, mechanisms and strategies for handling complex tasks; general and specific skills for problem-solving; and intention, morality and humanity exhibited during human actions and interaction. Various extensions include learning by imitation, learning to imitate [74], generation by imitation, domain adaptation or domain transfer. Humanoid imitation also face issues like imitation-to-reality gaps, in particular, for unseen, new and open world objects, scenarios and tasks, and efficient and effective in-distribution, in-domain and in-context imitation and imitation at scale. 

**4.5.3 Humanoid Demonstration to Generation** Humanoid intelligence can also be learned, augmented and generated by demonstrations and generation, such as by GenAI and advanced models like LLMs, VLM and LMMs. 

**Humanoid Demonstration-to-Operation** _Humanoid demonstration_ illustrates robots with expected functions, tasks, scenarios, behaviors, actions, and processes. Humanoids can then learn from single, few or sequential demonstrations to operate, plan, navigate or evolve over existing, new, unseen, open or lifelong tasks or environments [2]. Humanoids may learn from human demonstrations [86], such as positioning, posture, behaving, emotional, vocal and facial expressions, and ethical responses, to improve, evolve or develop their world knowledge, human-like actions and responses. Humanoids may also clone, optimize and expand the learned knowledge, activities or intelligence from demonstrations and further forecast and generate new actions, knowledge or intelligence through generative AI. Humanoid _learning by demonstration_ leverages humanoid simulation and mitigates sim-to-real gaps by enhancing 

Manuscript submitted to ACM 

Cao 

32 

humanoid’s familiarity and realisticness of the world and building robot experience, memory and reasoning. Similar to humanoid simulation, humanoid demonstration faces _demonstration-to-reality gaps_ (Demo2Real gaps for short). Such gaps may be caused by demonstration biases, distribution shift, misalignment, or the limitation and insufficiency of demonstrations (e.g., from zero shot, one shot to few shots), settings, capabilities, and capacity. Humanoid learning by demonstration still faces significant challenges for unstructured, ill-structured, unseen-structured, unknown-structured, transitional, lifelong and nonstationary settings and environments. Both humanoid simulation and demonstration are also challenged by zero, new, evolving, unseen, unknown and open objects, contexts, scenarios or tasks. 

**Humanoid Generation-to-Operation** With the fast-pace development of GenAI including LLMs, LMMs, VQA, VLPs, VLMs and VLAs, _automated generation_ becomes feasible and essential in simulating and producing AI and realizing human-level intelligence, substantially improving the intelligence of humanoids. _Humanoid intelligence generation_ may present new opportunities and challenges than existing LLMs for image-to-text, video-to-text, textto-image, and text-to-video, making the generation suitable for humanoid settings. Examples are 1) single-modal generation, e.g., generating humanoid behaviors, actions, responses, and emotions; and 2) cross-modal generation, such as image-to-speech, image-to-conversation, image-to-emotion, animation-to-speech, animation-to-conversation, animation-to-singing, animation-to-dancing, text-to-speech, text-to-conversation, text-to-action, and text-to-emotion [51, 86]. Humanoid generation could be built on humanoid animation, simulation, imitation and demonstration, where animation, simulation, imitation and demonstration serve as supervision, providing one to few shots for robot learning and further generation. Zero-to-few shot learning, weakly-supervised learning, transfer learning, contrastive learning, and Knowledge distillation would be useful to augment humanoid learning and generation by LLMs or LMMs. 

## **5 Conclusions** 

Real-time, interactive, and realistic humanoid robots epitomize the pinnacle of systematic AI development, transcending traditional robotics and intelligent systems. These cutting-edge humanoids represent a new generation of AI robots seamlessly integrating mechanical, electrical, biological, psychological, physiological, ergonomic, aesthetic, and sociocultural technologies and achievements. Leveraging recent AI advancements, particularly in GenAI with LLMs, real-time, interactive, and realistic humanoids demonstrate unprecedented potential in embodying human-like features, senses, behaviors, functions, and intelligences. 

State-of-the-art humanoids still fall short of attaining human-like intelligence, although they showcase increasingly impressive AI applications. AI-empowered humanoids are propelling the evolution of human-looking robotics towards human-like and humane elements, features, functions, and qualities. Prior to reaching superintelligence or human-level intelligence, substantial focus will still be on addressing comprehensive functional and nonfunctional requirements, challenges, issues to make humanoids actionable, realistic, and humane. 

In addition, while the paper covers a comprehensive overall of the past, present and future of humanoids and humanoid AI, it does not have the capacity to specify and consolidate the relevant techniques in detail and to deepen the technical discussion on functional and nonfunctional specifications. In addition, more technical explorations could be made on how and why to advance humanoids. All of these deserve future substantial efforts over the course of humanoid AI research and development. 

## **Acknowledgments** 

This work is partially sponsored by the Australian Research Council Discovery grant DP240102050, ARC LIEF grant LE240100131, and ARC Linkage grant LP230201022. 

Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

33 

## **References** 

- [1] Aishwarya Agrawal, Damien Teney, and Aida Nematzadeh. 2022. Vision-Language Pretraining: Current Trends and the Future. In _ACL 2022 - Tutorial_ . 38–43. 

- [2] Brenna D. Argall, Sonia Chernova, Manuela M. Veloso, and Brett Browning. 2009. A survey of robot learning from demonstration. _Robotics Auton. Syst._ 57, 5 (2009), 469–483. 

- [3] Yuki Asano, Kei Okada, and Masayuki Inaba. 2017. Design principles of a human mimetic humanoid: Humanoid platform to study human intelligence and internal body system. _Science Robotics_ 2, 13 (2017), eaaq0899. 

- [4] Alessio Baratta, Antonio Cimino, Francesco Longo, and Letizia Nicoletti. 2024. Digital twin for human-robot collaboration enhancement in manufacturing systems: Literature review and direction for future developments. _Comput. Ind. Eng._ 187 (2024), 109764. 

- [5] Leonard Bärmann, Rainer Kartmann, Fabian Peller-Konrad, Alex Waibel, and Tamim Asfour. 2024. Incremental Learning of Humanoid Robot Behavior from Natural Interaction and Large Language Models. _Frontiers in Robotics and AI_ 11 (2024), 1455375. 

- [6] Andrea Maria Bauer, Dirk Wollherr, and Martin Buss. 2008. Human-Robot Collaboration: a Survey. _Int. J. Humanoid Robotics_ 5, 1 (2008), 47–66. 

- [7] Douglas Blackiston, Sam Kriegman, Josh C. Bongard, and Michael Levin. 2023. Biological Robots: Perspectives on an Emerging Interdisciplinary Field. _Soft robotics_ 10 (2023), 674–686. Issue 4. 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, and et al. 2023. RT-1: Robotics Transformer for Real-World Control at Scale. In _Robotics: Science and Systems XIX, Daegu, Republic of Korea, July 10-14, 2023_ . 

- [9] Anthony Brohan, Yevgen Chebotar, Chelsea Finn, Karol Hausman, Alexander Herzog, Daniel Ho, Julian Ibarz, Alex Irpan, Eric Jang, Ryan Julian, and et al. 2022. Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. In _Conference on robot learning_ , Vol. 205. PMLR, 287–318. 

- [10] Longbing Cao. 2010. In-depth behavior understanding and use: The behavior informatics approach. _Inf. Sci._ 180, 17 (2010), 3067–3085. 

- [11] Longbing Cao. 2014. Non-IIDness Learning in Behavioral and Social Data. _Comput. J._ 57, 9 (2014), 1358–1370. 

- [12] Longbing Cao. 2015. _Metasynthetic Computing and Engineering of Complex Systems_ . Springer. 

- [13] Longbing Cao. 2018. _Data Science Thinking: The Next Scientific, Technological and Economic Revolution_ . Springer International Publishing, Switzerland. ISBN: 978-3-319-95092-1. 

- [14] Longbing Cao. 2022. Beyond AutoML: Mindful and Actionable AI and AutoAI with Mind and Action. _IEEE Intell. Syst._ 37, 5 (2022), 6–18. 

- [15] Longbing Cao. 2022. Decentralized AI: Edge Intelligence and Smart Blockchain, Metaverse, Web3, and DeSci. _IEEE Intelligent Systems_ 37, 03 (2022), 6–19. 

- [16] Longbing Cao. 2022. A New Age of AI: Features and Futures. _IEEE Intell. Syst._ 37, 1 (2022), 25–37. 

- [17] Longbing Cao. 2024. Ai4tech: X-AI enabling X-Tech with human-like, generative, decentralized, humanoid and metaverse AI. _Int. J. Data Sci. Anal._ 18, 3 (2024), 219–238. 

- [18] Longbing Cao. 2025. Humanoid AI with Humanity Modeling: Bridging Humans and Virtual–Physical Humanoids. _Technical Report_ (2025), 1–38. 

- [19] Longbing Cao, Dan Luo, and Chengqi Zhang. 2007. Knowledge actionability: satisfying technical and business interestingness. _IJBIDM_ 2, 4 (2007), 496–514. 

- [20] Alessandro Carfì and Fulvio Mastrogiovanni. 2023. Gesture-Based Human-Machine Interaction: Taxonomy, Problem Definition, and Analysis. _IEEE Trans. Cybern._ 53, 1 (2023), 497–513. 

- [21] Niccolò Casiddu, Francesco Burlando, Claudia Porfirione, and Annapaola Vacanti. 2021. Humanoid robotics: guidelines for usability testing. In _’IHSED2020’_ . Springer, 102–109. 

- [22] Christine T. Chang and Bradley Hayes. 2024. A Survey of Augmented Reality for Human-Robot Collaboration. _arXiv_ 12, 8 (2024), 540. 

- [23] Xi Chen, Xiao Wang, Soravit Changpinyo, A. J. Piergiovanni, Piotr Padlewski, Daniel Salz, Sebastian Goodman, Adam Grycner, Basil Mustafa, Lucas Beyer, Alexander Kolesnikov, Joan Puigcerver, Nan Ding, Keran Rong, Hassan Akbari, Gaurav Mishra, Linting Xue, Ashish V. Thapliyal, James Bradbury, and Weicheng Kuo. 2023. PaLI: A Jointly-Scaled Multilingual Language-Image Model. In _ICLR 2023_ . 

- [24] Jin-Hee Cho, Kevin S. Chan, and Sibel Adali. 2015. A Survey on Trust Modeling. _ACM Comput. Surv._ 48, 2 (2015), 28:1–28:40. 

- [25] Paolo Dario and Guang-Zhong Yang. 2017. Humanoid robotics - History, current state of the art, and challenges. _Sci. Robotics_ 2, 13 (2017), eaar4043. 

- [26] Kourosh Darvish, Luigi Penco, Joao Ramos, Rafael Cisneros, Jerry E. Pratt, Eiichi Yoshida, Serena Ivaldi, and Daniele Pucci. 2023. Teleoperation of Humanoid Robots: A Survey. _IEEE Trans. Robotics_ 39, 3 (2023), 1706–1727. 

- [27] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine, Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch, and Pete Florence. 2023. PaLM-E: An Embodied Multimodal Language Model. In _ICML 2023_ , Vol. 202. 8469–8488. 

- [28] Paul Dumouchel. 2023. Ethics & Robotics, Embodiment and Vulnerability. _Int. J. Soc. Robotics_ 15, 12 (2023), 2087–2099. 

- [29] Engineered Arts. 2023. Ameca: The Future of Humanoid Robotics. https://engineeredarts.com/ 

- [30] Grzegorz Ficht and Sven Behnke. 2021. Bipedal Humanoid Hardware Design: A Technology Review. _Curr Robot Rep_ 2 (2021), 201–210. 

- [31] Terrence Fong, Illah R. Nourbakhsh, and Kerstin Dautenhahn. 2003. A survey of socially interactive robots. _Robotics Auton. Syst._ 42, 3-4 (2003), 143–166. 

Manuscript submitted to ACM 

Cao 

34 

- [32] Manikandan Ganesan, Sivanathan Kandhasamy, Bharatiraja Chokkalingam, and Lucian Mihet-Popa. 2024. A Comprehensive Review on Deep Learning-Based Motion Planning and End-to-End Learning for Self-Driving Vehicle. _IEEE Access_ 12 (2024), 66031–66067. 

- [33] Ben Goertzel. 2014. Artificial General Intelligence: Concept, State of the Art, and Future Prospects. _Journal of Artificial General Intelligence_ 5, 1 (2014), 1. 

- [34] Michael A. Goodrich and Alan C. Schultz. 2007. Human-Robot Interaction: A Survey. _Found. Trends Hum. Comput. Interact._ 1, 3 (2007), 203–275. 

- [35] Hatice Gunes, Frank Broz, Chris S Crawford, Astrid Rosenthal-von der Pütten, Megan Strait, and Laurel Riek. 2022. Reproducibility in human-robot interaction: furthering the science of HRI. _Current Robotics Reports_ 3, 4 (2022), 281–292. 

- [36] Kenji Hashimoto. 2020. Mechanics of humanoid robot. _Advanced Robotics_ 34, 21-22 (2020), 1390–1397. 

- [37] Hiroshi Ishiguro, Fuki Ueno, and Eiki Tachibana (Eds.). 2024. _Cybernetic Avatar_ (1 ed.). Springer Singapore. 

- [38] Joshua Anith Singh Jeeva. 2023. _Risk Assessment of Humanoid Robot EVE-r3_ . Master’s thesis. University of Twente. 

- [39] Li-Hong Juang. 2024. Intelligent communication of two humanoid robots based on computer vison. _Multim. Tools Appl._ 83, 23 (2024), 63459–63477. 

- [40] Shuuji Kajita, Hirohisa Hirukawa, Kensuke Harada, and Kazuhito Yokoi. 2014. _Introduction to Humanoid Robotics_ . Springer Tracts in Advanced Robotics, Vol. 101. Springer. 

- [41] Takayuki Kanda, Hiroshi Ishiguro, Michita Imai, and Tetsuo Ono. 2004. Development and evaluation of interactive humanoid robots. _Proc. IEEE_ 92, 11 (2004), 1839–1850. 

- [42] Kento Kawaharazuka, Yoshiki Obinata, Naoaki Kanazawa, Naoto Tsukamoto, Kei Okada, and Masayuki Inaba. 2024. Reflex-based open-vocabulary navigation without prior knowledge using omnidirectional camera and multiple vision-language models. _Adv. Robotics_ 38, 18 (2024), 1307–1317. 

- [43] Zahra Rezaei Khavas, Seyed Reza Ahmadzadeh, and Paul Robinette. 2020. Modeling Trust in Human-Robot Interaction: A Survey. In _ICSR 2020_ , Vol. 12483. Springer, 529–541. 

- [44] Oliver Korn. 2019. _Social Robots: Technological, Societal and Ethical Aspects of Human-Robot Interaction (Ed.)_ (1. ed.). Springer International Publishing. 

- [45] Vikas Kumar and Dayal R. Parhi. 2023. Chaos-based optimal path planning of humanoid robot using hybridized regression-gravity search algorithm in static and dynamic terrains. _Appl. Soft Comput._ 140 (2023), 110236. 

- [46] Derek F. Lahr, Hak Yi, and Dennis W. Hong. 2016. Biologically inspired design of a parallel actuated humanoid robot. _Adv. Robotics_ 30, 2 (2016), 109–118. 

- [47] Przemyslaw A. Lasota, Terrence Fong, and Julie A. Shah. 2017. A Survey of Methods for Safe Human-Robot Interaction. _Found. Trends Robotics_ 5, 4 (2017), 261–349. 

- [48] Peizhen Li, Longbing Cao, Xiao-Ming Wu, Xiaohan Yu, and Runze Yang. 2025. UGotMe: An Embodied System for Affective Human-Robot Interaction. , 5542–5548 pages. 

- [49] Liangyi Luo, Kohei Ogawa, Graham Peebles, and Hiroshi Ishiguro. 2022. Towards a Personality AI for Robots: Potential Colony Capacity of a Goal-Shaped Generative Personality Model When Used for Expressing Personalities via Non-Verbal Behaviour of Humanoid Robots. _Frontiers Robotics AI_ 9 (2022), 728776. 

- [50] Derek McColl, Alexander Hong, Naoaki Hatakeyama, Goldie Nejat, and Beno Benhabib. 2016. A Survey of Autonomous Human Affect Detection Methods for Social Robots Engaged in Natural HRI. _J. Intell. Robotic Syst._ 82, 1 (2016), 101–133. 

- [51] Xiang Meng, Zhangguo Yu, Xuechao Chen, Zelin Huang, Fei Meng, and Qiang Huang. 2024. Online Adaptive Motion Generation for Humanoid Locomotion on Non-Flat Terrain via Template Behavior Extension. _IEEE Trans Autom. Sci. Eng._ 21, 4 (2024), 6563–6574. 

- [52] Bonan Min, Hayley Ross, Elior Sulem, Amir Pouran Ben Veyseh, Thien Huu Nguyen, Oscar Sainz, Eneko Agirre, Ilana Heintz, and Dan Roth. 2024. Recent Advances in Natural Language Processing via Large Pre-trained Language Models: A Survey. _ACM Comput. Surv._ 56, 2 (2024), 30:1–30:40. 

- [53] Ronja Möller, Antonino Furnari, Sebastiano Battiato, Aki Härmä, and Giovanni Maria Farinella. 2021. A survey on human-aware robot navigation. _Robotics Auton. Syst._ 145 (2021), 103837. 

- [54] Masahiro Mori, Karl F. MacDorman, and Norri Kageki. 2012. The Uncanny Valley [From the Field]. _IEEE Robotics Autom. Mag._ 19, 2 (2012), 98–100. 

- [55] Fabio Muratore, Fabio Ramos, Greg Turk, Wenhao Yu, Michael Gienger, and Jan Peters. 2022. Robot Learning From Randomized Simulations: A Review. _Frontiers Robotics AI_ 9 (2022), 799893. 

- [56] Robin R Murphy. 2019. _Introduction to AI robotics_ . MIT press. 

- [57] Adam Norton, Henny Admoni, Jacob W. Crandall, Tesca Fitzgerald, Alvika Gautam, Michael A. Goodrich, Amy Saretsky, Matthias Scheutz, Reid G. Simmons, Aaron Steinfeld, and Holly A. Yanco. 2022. Metrics for Robot Proficiency Self-assessment and Communication of Proficiency in Human-robot Teams. _ACM Trans. Hum. Robot Interact._ 11, 3 (2022), 29:1–29:38. 

- [58] Temitayo A. Olugbade, Liang He, Perla Maiolino, Dirk Heylen, and Nadia Bianchi-Berthouze. 2023. Touch Technology in Affective Human-, Robot-, and Virtual-Human Interactions: A Survey. _Proc. IEEE_ 111, 10 (2023), 1333–1354. 

- [59] Ziggy O’Reilly, Davide Ghiglino, Nicolas Spatola, and Agnieszka Wykowska. 2021. Modulating the Intentional Stance: Humanoid Robots, Narrative and Autistic Traits. In _ICSR 2021 (Lecture Notes in Computer Science, Vol. 13086)_ . Springer, 697–706. 

- [60] Luigi Penco, Kazuhiko Momose, Stephen McCrory, Dexton Anderson, Nicholas Kitchel, Duncan Calvert, and Robert J. Griffin. 2024. Mixed Reality Teleoperation Assistance for Direct Control of Humanoids. _IEEE Robotics Autom. Lett._ 9, 2 (2024), 1937–1944. 

- [61] Jairo Pérez-Osorio and Agnieszka Wykowska. 2019. Adopting the Intentional Stance Towards Humanoid Robots. In _Wording Robotics - Discourses and Representations on Robotics_ , Jean-Paul Laumond, Emmanuelle Danblon, and Céline Pieters (Eds.). Springer Tracts in Advanced Robotics, Vol. 130. Springer, 119–136. 

- [62] Rolf Pfeifer and Josh C. Bongard. 2007. _How the body shapes the way we think - a new view on intelligence_ . MIT Press. Manuscript submitted to ACM 

Humanoid Robots and Humanoid AI: Review, Perspectives and Directions 

35 

- [63] Silvia Proia, Raffaele Carli, Graziana Cavone, and Mariagrazia Dotoli. 2022. Control Techniques for Safe, Ergonomic, and Efficient Human-Robot Collaboration in the Digital Industry: A Survey. _IEEE Trans Autom. Sci. Eng._ 19, 3 (2022), 1798–1819. 

- [64] Niyati Rawal and Ruth Maria Stock-Homburg. 2022. Facial Emotion Expressions in Human-Robot Interaction: A Survey. _Int. J. Soc. Robotics_ 14, 7 (2022), 1583–1604. 

- [65] Nicole L. Robinson, Brendan Tidd, Dylan Campbell, Dana Kulic, and Peter Corke. 2023. Robotic Vision for Human-Robot Interaction and Collaboration: A Survey and Systematic Review. _ACM Transactions on Human-Robot Interaction_ 12, 1 (2023), 1–66. 

- [66] Arindam Roychoudhury, Shahram Khorshidi, Subham Agrawal, and Maren Bennewitz. 2023. Perception for Humanoid Robots. _Curr Robot Rep_ 4 (2023), 127–140. 

- [67] Mario Arturo Ruiz Estrada. 2024. The Impact of Humanoid Robots (HR) in the Economy: From Microeconomic and Macroeconomic Perspective. (2024), 1–11. http://dx.doi.org/10.2139/ssrn.5001440 

- [68] Saeed Saeedvand, Masoumeh Jafari, Hadi S. Aghdasi, and Jacky Baltes. 2019. A comprehensive survey on humanoid robot development. _Knowl. Eng. Rev._ 34 (2019), e20. 

- [69] Francesco Semeraro, Alexander Griffiths, and Angelo Cangelosi. 2023. Human-robot collaboration and machine learning: A systematic review of recent research. _Robotics Comput. Integr. Manuf._ 79 (2023), 102432. 

- [70] Minkyu Shin, Jin Kim, Bas Van Opheusden, and Thomas L Griffiths. 2023. Superhuman artificial intelligence can improve human decision-making by increasing novelty. _Proceedings of the National Academy of Sciences_ 120, 12 (2023), e2214840120. 

- [71] Austin Stone, Ted Xiao, Yao Lu, Keerthana Gopalakrishnan, Kuang-Huei Lee, Quan Vuong, Paul Wohlhart, Brianna Zitkovich, Fei Xia, Chelsea Finn, and Karol Hausman. 2023. Open-World Object Manipulation using Pre-trained Vision-Language Models. (2023), 1–21. 

- [72] Rajesh Subburaman, Dimitrios Kanoulas, Nikos G. Tsagarakis, and Jinoh Lee. 2023. A survey on control of humanoid fall over. _Robotics Auton. Syst._ 166 (2023), 104443. 

- [73] Tomomichi Sugihara and Mitsuharu Morisawa. 2020. A survey: dynamics of humanoid robots. _Adv. Robotics_ 34, 21-22 (2020), 1338–1352. 

- [74] Jingkai Sun, Qiang Zhang, Yiqun Duan, Xiaoyang Jiang, Chong Cheng, and Renjing Xu. 2024. Prompt, Plan, Perform: LLM-based Humanoid Control via Quantized Imitation Learning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . 16236–16242. 

- [75] Ryo Suzuki, Adnan Karim, Tian Xia, Hooman Hedayati, and Nicolai Marquardt. 2022. Augmented Reality and Robotics: A Survey and Taxonomy for AR-enhanced Human-Robot Interaction and Robotic Interfaces. In _CHI ’22_ . 553:1–553:33. 

- [76] Aaquib Tabrez, Matthew B. Luebbers, and Bradley Hayes. 2020. A Survey of Mental Modeling Techniques in Human–Robot Teaming. _Current Robotics Reports_ 1 (2020), 259 – 267. 

- [77] Andrea Tagliabue and Jonathan P. How. 2024. Efficient Deep Learning of Robust Policies From MPC Using Imitation and Tube-Guided Data Augmentation. _IEEE Trans. Robotics_ 40 (2024), 4301–4321. 

- [78] Yuichi Tazaki and Masaki Murooka. 2020. A survey of motion planning techniques for humanoid robots. _Adv. Robotics_ 34, 21-22 (2020), 1370–1379. [79] Yuchuang Tong, Haotian Liu, and Zhengtao Zhang. 2024. Advancements in Humanoid Robots: A Comprehensive Review and Future Prospects. _IEEE/CAA Journal of Automatica Sinica_ 11, JAS-2023-1103 (2024), 301. 

- [80] Michael Walker, Thao Phung, Tathagata Chakraborti, Tom Williams, and Daniel Szafir. 2023. Virtual, Augmented, and Mixed Reality for Human-robot Interaction: A Survey and Virtual Design Element Taxonomy. _J. Hum.-Robot Interact._ 12, 4, Article 43 (2023), 39 pages. 

- [81] Xiaoying Wang and Tong Zhang. 2024. Reinforcement learning with imitative behaviors for humanoid robots navigation: synchronous planning and control. _Auton. Robots_ 48, 2 (2024), 5. 

- [82] Murphy Wonsick, Philip Long, Aykut Özgün Önol, Maozhen Wang, and Taskin Padir. 2021. A Holistic Approach to Human-Supervised Humanoid Robot Operations in Extreme Environments. _Frontiers Robotics AI_ 8 (2021), 550644. 

- [83] Roman V Yampolskiy. 2015. _Artificial Superintelligence: A Futuristic Approach_ . cRc Press. 

- [84] Yang Ye, Hengxu You, and Eric Jing Du. 2023. Improved Trust in Human-Robot Collaboration With ChatGPT. _IEEE Access_ 11 (2023), 55748–55754. 

- [85] Fanlong Zeng, Wensheng Gan, Yongheng Wang, Ning Liu, and Philip S. Yu. 2023. Large Language Models for Robotics: A Survey. _CoRR_ abs/2311.07226 (2023). https://doi.org/10.48550/ARXIV.2311.07226 

- [86] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, and et al. 2023. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. In _Conference on Robot Learning_ . PMLR, 2165–2183. 

- [87] Jakub Zlotowski, Diane Proudfoot, Kumar Yogeeswaran, and Christoph Bartneck. 2015. Anthropomorphism: Opportunities and Challenges in Human-Robot Interaction. _Int. J. Soc. Robotics_ 7, 3 (2015), 347–360. 

Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009 

Manuscript submitted to ACM 

