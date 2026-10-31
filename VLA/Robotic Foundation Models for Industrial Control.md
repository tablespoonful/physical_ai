---
title: "Robotic Foundation Models for Industrial Control: A Comprehensive Survey and Readiness Assessment Framework"
date: "2026-03-06"
authors: "David Kube; Simon Hadwiger; Tobias Meisen"
url: https://arxiv.org/abs/2603.06749
pdf: https://arxiv.org/pdf/2603.06749
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.06749)** / [論文ページ](https://arxiv.org/abs/2603.06749)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Robotic Foundation Models for Industrial Control: A Comprehensive Survey and Readiness Assessment Framework 

David Kube<sup>1,2*</sup> , Simon Hadwiger<sup>1,2</sup> and Tobias Meisen<sup>2</sup> 

- 1*Factory Automation, Siemens AG, Gleiwitzer Straße 555, Nuremberg, 90475, Germany. 

   - 2Institute for Technologies and Management of Digital Transformation, Bergische Universit¨at Wuppertal, Gaußstraße 20, Wuppertal, 42119, Germany. 

*Corresponding author(s). E-mail(s): david.kube@siemens.com; Contributing authors: simon.hadwiger@siemens.com; meisen@uni-wuppertal.de; 

##### **Abstract** 

Robotic foundation models (RFMs) are emerging as a promising route towards flexible, instructionand demonstration-driven robot control, however, a critical investigation of their industrial applicability is still lacking. This survey gives an extensive overview over the RFM-landscape and analyses, driven by concrete implications, how industrial domains and use cases shape the requirements of RFMs, with particular focus on collaborative robot platforms, heterogeneous sensing and actuation, edge-computing constraints, and safety-critical operation. We synthesise industrial deployment perspectives into eleven interdependent implications and operationalise them into an assessment framework comprising a catalogue of 149 concrete criteria, spanning both model capabilities and ecosystem requirements. Using this framework, we evaluate 324 manipulation-capable RFMs via 48,276 criterion-level decisions obtained via a conservative LLM-assisted evaluation pipeline, validated against expert judgements. The results indicate that industrial maturity is limited and uneven: even the highest-rated models satisfy only a fraction of criteria and typically exhibit narrow implicationspecific peaks rather than integrated coverage. We conclude that progress towards industry-grade RFMs depends less on isolated benchmark successes than on systematic incorporation of safety, realtime feasibility, robust perception, interaction, and cost-effective system integration into auditable deployment stacks. 

**Keywords:** Robotic Foundation Models, Industrial Robotics, Industrial Maturity Assessment, Robot Manipulation, Industrial AI, Collaborative Robotics 

## **1 Introduction** 

Over the past decades, industrial robotics is undergoing a transition from isolated, highly optimised automation towards flexible and increasingly collaborative deployment paradigms. In particular, the growing adoption of Collaborative Robots (cobots) reflects a shift towards automation solutions that can be commissioned rapidly, 

redeployed across frequently changing processes, and operated in closer proximity to human workers. While these platforms offer high mechanical precision and repeatability alongside comparatively restrained power consumption, their industrial utility is increasingly limited by the availability of robust, adaptive and intuitive control methods rather than by actuation performance alone. This motivates a renewed focus on learning-based 

1 

robot intelligence that can cope with variability in tasks, environments, actuation and sensing, while respecting industrial constraints such as safety, reliability, low-latency operation and cost-effective integration. Recent progress in large-scale learning has led to the emergence of Foundation Models (FMs), which promise to reduce manual engineering effort by transferring knowledge across tasks – a capability particularly attractive in highmix, low-volume industrial settings. Within this development, Robotic Foundation Models (RFMs) aim to supply generalist competence for embodied decision-making by providing a flexible platform for transfers across tasks, interfaces and embodiments. In this survey, we focus on models capable of generating low-level actions for direct robot actuation – RFMs for control or integrated RFMs as per our definition in Section 2 – because this interface is central for real-world deployment and exposes the strongest coupling to industrial constraints (e.g. latency, safety gating, and hardware-specific action spaces). While paradigms for building such models vary widely – including diffusion-based approaches [1, 2], dreaming-based methods [3, 4], and dual-system designs [5–7] – we deliberately chose not to review architectural taxonomy, as related works already cover those topics; for architectural-centred surveys, we thus refer to Section 4. Instead, we use the industrial lens to connect the rapid RFMs’ methodological progress to the practical constraints that determine whether such systems can be deployed in industrial environments. To structure this discussion and to position RFMs within the broader evolution of robot control, we propose a comprehensible categorisation of robotic control methods, summarised by the hierarchy in Figure 1: 

1. **Predefined/Rule-based** : Employ fixed trajectories or simple triggers, lacking dynamic adaptation. _Transition_ : Upgraded by integrating sensor-driven, dynamic input. 

2. **Reactive/Parametrised** : Enable limited adaptation via sensors and parameter adjustment. _Transition_ : Move beyond predefined behaviours by introducing learning capabilities. 

3. **Specialised/Narrow** : Solutions tailored for a specific problem on a given hardware setup. _Transition_ : Achieve generic, multi-purpose competence. 


**Fig. 1** : Robotic control-method hierarchy: _Each level increases flexibility, intelligence and generalisation capabilities, while reducing manual engineering effort and required expertise for operation and adaptation._ 

4. **Foundational** : Broadly pretrained systems capable of efficient fine-tuning with minimal dedicated engineering. _Transition_ : Eliminate need for further manual tuning and enable online adaptation. 

5. **Generalist** : Deliver zero-shot or in-context generalisation to new tasks and configurations, requiring only high-level instructions or online demonstration, akin to human operators in industry. 

This hierarchy highlights the core developmental trajectory relevant to industrial deployment: moving from rigid, task-specific automation towards adaptable, instruction- and demonstration-driven operation with decreasing commissioning effort. The introduction of FMs in robotics expressively marked the progression from specialised control systems (3.) to foundational robotics (4.), producing cross-embodiment and multi-task control systems. Yet, as our subsequent analysis shows, this step does not automatically yield industrygrade autonomy: reaching the next level towards truly generalist systems (5.) requires capabilities such as robust online adaptation, dependable instruction following, and safe operation under uncertainty – capabilities that are particularly important in dynamic, cost-driven industrial environments. The pace at which the field is moving makes a dedicated, industrially grounded review a necessity. As shown in Figure 2, publications rel- 

2 


Accordingly, this survey is structured to progressively connect foundational concepts to industrial requirements and, subsequently, to a systematic assessment of current RFMs (cf. Figure 3): We first define RFMs and position them within the robotics control landscape (Section 2). We then describe our review methodology and corpora composition (Section 3), followed by related works (Section 4) and further background to motivate industrial relevance: the rise of cobots and their deployment domains (Section 5) as well as the practical constraints of hardware, sensing, and edge computing that shape feasible RFM deployment (Section 6). 

**Fig. 3** : Table of Contents. _Highlighting preliminary sections in red, background in purple and the main review in green._ 

Building on these foundations, we distil industrial deployment viewpoints into general implications and operationalise them into an explicit assessment framework (Section 7). Finally, we apply this framework to the manipulation-capable RFM landscape, providing both an overview and a criteria-based industrial maturity evaluation 

3 

(Section 8), before concluding with a synthesis and discussion of our findings (Section 9). A key preview of our results is that, despite impressive benchmark-level progress and increasing breadth of contributions, industrial maturity remains limited and uneven across the field: current models tend to address a small number of enabling dimensions at a time, rather than offering integrated coverage of the deployment-critical requirements that dominate real industrial settings. This motivates our primary goal: to move the discussion from isolated benchmark successes towards a traceable, implication-grounded view of what it would mean for RFMs to be credible candidates for industrial deployment. Our main contributions are: 

1. A clear categorisation of robotic control approaches that situates RFMs within the broader progression from rule-based automation to generalist robotic intelligence (Figure 1). 

2. A concrete definition and clustering of RFMs (Section 2). 

3. A comprehensive overview of the current RFM literature and state of the art, with a focus on manipulation-capable systems (Table D5). 

4. An industrially motivated perspective on the rise of cobots, clarifying why their adoption amplifies the need for more general, instructable and adaptable control methods (Sections 5 and 6). 

5. A synthesis of domain-agnostic industrial deployment implications distilled from industrial literature into eleven interdependent viewpoints (Section 7.1). 

6. An extensive, implication-grounded criteria catalogue comprising 149 items to assess industrial maturity of RFMs (including ecosystem requirements), which we believe has not previously been developed in this form for RFM-centred industrial readiness assessment (Section 7.3). 

7. A large-scale evaluation of the current RFM landscape against this catalogue, elucidating strengths, weaknesses, and research gaps that must be addressed to advance towards industry-grade RFMs (Sections 8 and 9). 

## **2 Robotic Foundation Models** 

FMs represent a significant milestone in artificial intelligence, forming the basis for highly generalisable systems that can be efficiently adapted to diverse downstream tasks. These models are trained on extensive, heterogeneous datasets, often employing self-supervised learning methods to extract patterns and relationships well beyond their original training objectives [8–10]. This breadth of data enables FMs to exhibit emergent behaviour – capabilities and skills that substantially exceed the sum of their training data and initial design intentions. As Marsh [11] describes, emergent behaviour is “greater than the sum of the parts”. In practice, this capability is shown in Large Language Models (LLMs), trained simply to predict the next word in a sentence, which demonstrate abilities in arithmetic, programming, and reasoning that were never explicitly targeted during training, but arise from their scale and dataset diversity [8]. Thus, as seen in domains like Natural Language Processing (NLP) where input-output formats and modalities can often be standardised, these models deliver robust, adaptable performance across a variety of tasks that previous methods were unable to solve [8–10]. A fundamental interpretability challenge in FMs centres around their dualistic nature: on the one hand, they may function as single, general models whose mechanisms are widely applicable; on the other hand, their ability to adapt to profoundly different tasks may stem from an inherent collection of specialised expert models, each tailored to a specific context [8]. To efficiently interpret the behaviour of FMs and enable both their adaptation and the creation of new FMs for novel domains, it is vital to understand the mechanisms by which a FM acquires, represents, and processes knowledge. However, when extending the FM paradigm to robotics, additional domainspecific complexities emerge: The robotic context introduces high-dimensional, closed-loop decision processes, in which a robot’s actions directly and recurrently influence the environment’s state, thus its sensory feedback and subsequent behaviour – a dynamic fundamentally distinct from static, offline data scenarios prevalent in language and vision tasks [8]. Moreover, robotic platforms display vast heterogeneity in physical embodiments, configurations, and operational contexts. For this 

4 

reason, classical control solutions are typically tailored to specific robots, environments, and tasks. These systems are characterised by determinism, yet inflexibility and have historically lacked generalisability across tasks or hardware, highlighting the need for control methods that are inherently task-agnostic, cross-embodiment, and open-ended. [9] Foundational methods – capable of leveraging highly diverse robotic datasets – can fill this gap, when satisfying criteria implicated by industrial use cases and needs. We argue that, analogous to how FMs in NLP seamlessly handle varied languages or dialects, emergence in robotic-specific FMs could result in the capability to operate across different robot embodiments, modalities, and environments. In effect, such RFMs could be modelled to interpret every robot platform and configuration simply as yet another dialect or language, enabling generalisable control, reasoning, and planning capacity irrespective of the current task or embodiment. 

Definitions of RFMs vary among researchers: Hu et al. [12] distinguish between ”single-purpose” RFMs (focused on one modular capability, e.g. perception, planning, or control) and ”generalpurpose” RFMs – models that can span perception, planning, control, and even non-robotic tasks. However, we argue that only the latter, models capable of integrating perception with actionable outputs (such as control, trajectory or plan generation), qualify as true RFMs. Methods restricted to perception or control alone lack the necessary generalism, functioning more as encoders, decoders or specialised solutions rather than _holistic_ foundational models. Furthermore, recent perspectives sometimes conflate VisionLanguage-Action Models (VLAs) and RFMs, suggesting those terms are equivalent [13]. However, similar to Xiang et al. [14] defining VLAs as a class of RFMs, we also consider VLAs a distinct RFM sub-category. In particular, VLAs employ multimodal inputs, incorporating language and vision, to provide human-like instructability and generalisation, generating actions for robot control. Zhou et al. [15] note that VLAs unify vision, language, and action by aligning all modalities into a common format, such as tokens, thus allowing end-to-end training and prediction. Xu et al. [16] describe VLAs as typically built from three modules: perception, reasoning/planning, and action. While this categorisation may be true for certain 

candidates, we think that models not explicitly modelling or defining a strict separation of those concerns also qualify as VLAs. Beyond modalities, Zhong et al. [17] highlight that VLAs belong to both digital- and embodied-Artificial Intelligence (AI), thus need to bridge digital intelligence with physical interaction, demanding robust adaptability to real-world complexity and robot hardware constraints. 

Synthesising these interpretations, we define **Robotic Foundation Models (RFMs)** as highly adaptable, data-driven models specialised for addressing robotic tasks, distinguished by a generalist core: The ability to efficiently adapt to varied tasks, settings, embodiments and hardware configurations with low dedicated engineering or retraining effort – e.g. through high-level instructions, flexibility in action representation/ interpretation or providing a generalist foundation for task-specific tuning. A model that does not exhibit such a generalist core, e.g. in the sense of cross-task or cross-embodiment adaptability, does not qualify as an RFM under our definition. To satisfy their multi-purpose nature, RFMs must encompass: 

- **Multi-Modality** : Capability to ingest diverse proprio- and exterioceptive signals, such as sensor data, images and Natural Language (NL). 

- **Output flexibility** : Producing actions, plans, trajectories or similar outputs suitable for a spectrum of robots and task domains. 

- **Adaptability** : Ability to adapt or generalise to tasks, environments or embodiments with little manual intervention. 

Given the above definition, it becomes clear that VLAs form a prominent and distinct sub-category within the broader class of RFMs [14], as VLAs fulfil RFMs’ key criteria: they harness multimodal inputs in the form of natural language instructions and visual perception, which grants them the flexibility to be intuitively prompted by human operators across a wide array of tasks, while producing low-level actions for direct robot actuation as output. However, RFMs are not constrained to producing low-level actions, hence they can be categorised according to the principal functions they perform within robotic systems, such as (but not limited to): 

5 

- **RFMs for Control** : These models directly generate low-level action outputs for robot actuation, such as motor commands, joint velocities or force/torque signals, across diverse embodiments and environments. 

- **RFMs for Planning** : These models focus on high-level reasoning, task decomposition, (re)planning or explainability generation. They may operate by integrating multimodal perception and context, producing sequential plans or sub-goals that downstream controllers execute. 

- **Integrated RFMs** : Advanced models jointly combining planning and control capabilities. These models most closely align with the vision of general-purpose robotic intelligence, capable of internal reasoning, failure-explanation or -recovery and long-horizon (re)planning combined with direct robot control. 

A similar taxonomy (control & planning) has been proposed by Ma et al. [13] for VLAs, however, we contend that particularly planners align more closely with the overarching RFM paradigm, as their outputs are predominantly of a highlevel nature. Other than through NL leveraged in VLAs, adaptability can equally arise through alternative modalities, methodologies or instructioning mechanisms – such as using goal images, state representations, or exhibiting a general high adaptability to novel tasks, e.g. through demonstration. Therefore, subcategories like VisionAction Models (VAs), such as DP [1] or Dreamitate [4], devoid of NL understanding, still qualify as RFMs if they possess a multi-purpose nature, such as robust foundations for adaptation to various tasks/ embodiments or multi-task/ domain integration. 

RFMs also encompass a myriad of specialised subclasses, targeting specific application areas or domains such as manipulation [18–20], locomotion/navigation [21–23] or aerial [24] and underwater [25] robotics. Others target combinations thereof, such as mobile-manipulation [26– 29]. Such specialisation to embodiments or taskcategories often stems from predefined action spaces or fine-tuning data composition. In the context of industrial deployment, manipulation stands out as the most pertinent capability, underpinning essential functions like (dis)assembly, pick-and-place operations, sorting, and dexterous 

material handling. Arguably, manipulation constitutes one of the central challenges to resolve in general robotics, laying the groundwork for mastering other domains such as locomotion or navigation, which themselves can be interpreted as a form of self-manipulation. Ultimately, however, RFMs should pursue the goal to be _both_ application- and embodiment-independent, underscoring their foundational nature. In summary, within the scope of this survey, a model qualifies as an RFM only if it exhibits a generalist core in the sense of cross-task or cross-embodiment adaptability, while providing multimodal input integration and flexible output generation. Models lacking these properties are considered specialised or narrow approaches rather than RFMs. 

## **3 Review Methodology & Corpora Composition** 


**Fig. 4** : Overview of all utilised corpora and number of considered publications, as presented within this section. 

This section provides a detailed description of the procedures used to assemble, filter, and categorise the literature corpora that underpin this survey. Our methodology is designed to ensure systematic coverage, transparency, volume management and reproducibility throughout all phases 

6 

of literature acquisition and analysis. Figure 4 presents an overview of all main corpora – comprising the principal RFM-related corpora (main), the industrial implication corpus, and further supplementary sets – together with the proportion of all considered publications. In the following subsections, we describe the automated acquisition pipeline, filtering strategies, and post-processing steps for each corpus, as well as the criteria guiding their composition and specific role within the wider context of this review. 

### **3.1 Literature Acquisition Procedure** 

To ensure both comprehensive coverage and reproducibility of our literature acquisition, we developed a modular Python pipeline for automated article retrieval and filtering as depicted in Figure 5. This approach was designed to maximise retrieval breadth across relevant literature while minimising blind spots, standardising the literature research procedure throughout all stages of corpora generation, and reducing manual intervention. 

The main tool in our pipeline (DB-Search) starts with following user-provided information: 

- One or multiple search queries formulated in a novel, structured Academic Search Query Syntax (ASQS), tailored to thoroughly capture all relevant literature domains. 

- The publication date range to be applied for article retrieval (e.g. from 2020 to the present). 

- Selection of target Databases (DBs) used for querying, from the list of implemented DBs (arXiv, GoogleScholar, OpenAlex, Scopus and SemanticScholar). 

- Specification of retrieval preference methodology (latest vs. most relevant results). 

- Upper bounds for the number of articles to retrieve per DB-query combination, serving as a cut-off to manage volume (e.g. 100 results per DB-query pair). 

The pipeline then automatically translates each ASQS query into the respective syntax of each target DB, relaxing unsupported features where necessary (such as proximity operators or fuzzy matching). All selected DBs are then automatically scanned for each specified query – resulting 


**Fig. 5** : General Literature Acquisition Pipeline Procedure: _Manual user involvement is required only for the Manual Refinement steps (highlighted in pink); all other processes execute automatically based on user-input. Only the Query Proposal and Filter Process modules leverage LLMs, while the DB-Search is fully deterministic._ 

in the usage of all possible DB-query permutations. During the search process, all metadata returned by the used APIs for the resulting articles are merged. Thereafter, identified duplicates, based on unique identifiers (such as DOIs), are initially removed for all articles containing sufficient information to permit duplicate removal. Subsequently, the system retrieves missing metadata from auxiliary APIs (e.g. SemanticScholar, arXiv, 

7 

Crossref) to ensure completeness. Metadata validity is programmatically checked – e.g. by verifying consistency between titles and abstracts. Articles lacking essential information (not uniquely identifiable) or presenting errors (e.g. title-abstract mismatch) are excluded from the results. Another round of duplicate removal is performed after these checks. 

The resulting collection of validated articles is stored in serialised files (JSON or YAML), and, if desired, also exported to PDF format with structured details including, but not limited to: title, URL, authors, abstract, DOI, originating query, and unique identifier assigned by the retrievalpipeline. Comprehensive reports documenting the entire retrieval process and its results are automatically generated. These include: 

- **Overall Retrieval Report:** 

- Actual (ASQS-derived) queries employed per database. 

- Time span and database selection. 

- Maximum and actual number of retrieved results. 

- Pipeline execution timestamps. 

- **Per-DB-Query Combination:** 

- Unique query ID, timestamp, ASQS/base and translated query. 

- Applied time and sorting restrictions. 

- Actual and maximum possible number of results returned. 

After the main retrieval, an LLM-based filtering tool (Filter Process) using GPT-4o is leveraged on-demand for semantic relevance scoring. This tool splits the corpus for parallel processing and individually passes each article’s title and abstract, alongside the user-intended relevance criteria, through the LLM. It outputs a binary relevance label, a floating-point relevance score in the interval [0 _,_ 1] and a concise NL justification of its decision. Sequential or layered filtering can be adopted, using progressively stricter relevance criteria to optimise classification accuracy within the resulting corpora. 

The pipeline is further supplemented by another component (Query Proposal) for initial query recommendation generation, utilising two further LLM-instances of GPT-4o. Given the ASQS syntax-definition and user intent, they jointly 

craft and propose a suite of search queries. This assists in establishing a robust baseline for exploration and iterative query refinement. Combining these tools, we developed all principal literature corpora used throughout this work and presented within the following subsections. The pipeline’s results were then complemented by manual post-processing, including enrichment (with articles from references or iterative handsearches), correction, and the application of additional manual filters to ensure quality, completeness, and relevance. 

### **3.2 RFM-Related Corpora** 

The RFM-related corpus constitutes the principal literature base for this survey, aiming to target all major research directions regarding RFMs and their associated domains. This includes not only 


**Fig. 6** : Literature Acquisition Pipeline: _Process of gathering the RFM-related corpora (see Figure 7). Results yielded by manual cross-search are included for simplicity._ 

RFM themselves, but also adjacent contributions such as training protocols, universal extensions, concrete applications and evaluation studies as well as broader considerations on RFMs (e.g. safety, robustness, or adversarial challenges). As we focus on RFMs capable of direct low-level control – as per our definition from Section 2: RFMs for control & integrated RFMs – we separate 

8 

those approaches from LLM-based, high-level or narrow (too specialised) approaches, denoted as ”High-Level”. In addition, we cluster literature concerning datasets, benchmarks and simulators, especially those highly relevant to RFM research. To give an overview of related works (see Section 4), survey and review publications relating to RFMs or general embodied AI form the last category to be distinguished within the main corpus. 

To get an initial overview of the literaturelandscape and obtain both a comprehensive and up-to-date corpus, we performed _two_ iterations of large-scale literature retrievals using our proposed standardised Python pipeline (Section 3.1), each configured with identical parameters and subsequently merged to maximise article coverage. Figure 6 shows the concrete retrieval process combining both searches, for which the following settings were applied: 

- **Queries:** Eleven extensive ASQS-queries, defined to ensure broad coverage across the complete scope of the main corpus (as shown in Table B2 of the Appendix). 

- **Publication Year Range:** From 2022 to date of search (see below). 

- **Databases:** arXiv, GoogleScholar, OpenAlex, Scopus and SemanticScholar. 

- **Results Per Query:** A retrieval limit of 400 articles per database ( _x_ 5) per query ( _x_ 11), leading to a maximal possible result set of 22 _,_ 000 articles. 

We intentionally combined a large set of nonrestrictive and targeted queries with a high cut-off value, to ensure a comprehensive result list, while managing volume with targeted filters afterwards. **Search 1:** Executed on the 4 _th_ of July 2025, returning 10 _,_ 728 valid article entries, of which 5 _,_ 035 were determined unique after deduplication. _Purpose: Initial overview._ **Search 2:** Conducted on the 30 _th_ of October 2025, returned 12 _,_ 027 valid articles, yielding 4 _,_ 999 unique entries after improved duplicate removal. _Purpose: Currentness._ Notably, despite identical parameters, the initial corpus increased significantly in this short period, illustrating the rapid pace of the field and increased database coverage. Additionally, the duplicate removal algorithm was improved 

between search 1 & 2 leading to fewer unique articles in the latter. 

These two result sets were merged, followed by a cautious duplicate removal protocol that erred on the side of retaining ambiguous entries, resulting in a base corpus of 6 _,_ 497 as unique classified articles. This base was then filtered and refined through a multi-stage process: 

1. **Robotics-Relevant Filtering:** A coarse LLM-based filter was first applied to remove articles not relevant to robotics. Of the 6 _,_ 497 publications, 4 _,_ 834 were retained as relevant, while 1 _,_ 663 were disregarded. 

2. **RFM-Relevant Filtering:** The remaining 4 _,_ 834 articles were subjected to a stricter LLM filter, targeting relevance for RFMs, VLAs, and additional foundational approaches or relevant publications as per our targeted specification for this corpus. This yielded 1 _,_ 408 relevant articles. 

For both filter stages, the not-relevant entries were manually sampled and cross-checked. Within this process no false negative cases were identified. The resulting set of 1 _,_ 408 records then became the subject of _manual_ in-depth review, further filtering, enrichment (e.g. inclusion of key references and works found through manual chainsearching), and categorisation. Duplicates not resolved algorithmically (e.g. due to identifier inconsistencies) were discarded manually. The procedure resulted in the following final, categorised main corpus (see also Figure 7): 

- **Total articles:** 1 _,_ 025 unique and highly relevant works. 

- **Models:** 341 control or integrated RFMs, of which 324 focus on manipulation, mobile manipulation, or are generally applicable to multiple robotic domains. The remaining 17 target other specific embodiments or domains (drones, surgical robots, locomotion, navigation or underwater). 

- **Related Works:** 321 articles, e.g. training protocols, extensions (not further categorised for this review). 

- **High-Level:** 231 articles, covering LLM-based (multi-agent) systems, as well as foundational but more narrowly scoped models or RFMs for planning. 

9 

- **Data and Benchmarks:** 77 articles, including dataset, simulators, benchmark suites, and data generation procedures. 

- **Surveys:** 55 literature survey and review papers, comprising 24 on general or embodied AI, and 31 that include RFMs (of which 11 focus specifically on RFMs). Across the 55, only 2 focus on industrially relevant topics. For more detail, see Section 4. 


Total: 1025 

**Fig. 7** : Main RFM-Related Corpus Composition 

This categorised corpus provides the reference set for all subsequent, review-related analyses, ensuring broad and systematic coverage of RFM and closely associated fields. 

### **3.3 Industrial Implication Corpus** 

To systematically capture the requirements, challenges, and context-specific attributes of realworld robotic applications in industrial domains, we gathered an industrial implication corpus, utilising the same modular literature research pipeline described in Section 3.1. The intention underlying this corpus was dual: to gather (1) studies of concrete industrial robotics applications and use cases that _implicitly_ reveal relevant industrial requirements, and (2) works providing _explicit_ discussions or analyses of robotics requirements, constraints, and challenges unique to industrial environments. 


**Fig. 8** : Literature Acquisition Pipeline: _Process of gathering the industrial implication-related corpus._ 

For this purpose, a comprehensive search depicted in Figure 8 was conducted according to the following parameters: 

- **Queries:** Seven broad ASQS queries (as shown in Table B3 of the Appendix), to ensure coverage across a variety of industrial fields, including applications, case studies, analyses, and review papers. 

- **Publication Year Range:** From 2015 up to July 2025. 

- **Databases:** arXiv, GoogleScholar, OpenAlex, Scopus and SemanticScholar. 

- **Results Per Query:** A retrieval limit of 50 articles, yielding a maximum possible result set of 1 _,_ 750 publications. 

The pipeline yielded 1 _,_ 240 valid entries, of which 892 were determined to be unique after deduplication. To reduce the volume and focus on relevant material, a coarse LLM-based relevance filter, configured with the same intent as the original search, was applied. As a result, the corpus was narrowed to 296 relevant articles and 596 classified as unrelated. Thereafter, a manual in-depth review was performed on 125 of the relevant articles that were assigned the highest LLM-based relevance score (relevance _≥_ 0 _._ 9). We chose to focus on this subset of most relevant articles, since the volume seemed sufficient for the process of gathering 

10 

industrial implications. Lesser-scored entries (relevance _<_ 0 _._ 9) were not included in the detailed review. The insights distilled from this core set have been iteratively synthesised, clustered, and mapped to industrial implications for robotic systems. An overview and in-depth discussion of the extracted implications and their interpretation within the RFM paradigm are provided in Section 7. 

### **3.4 Further Corpora & Manual Searches** 

In addition to the two main corpora presented in the previous sections, additional automated and manual searches about industrial robots, cobots, compute hardware, sensors, manipulators, efficiency considerations, and further related fields as well as norms/ standards have been performed, resulting in a total of 113 auxiliary publications. Those have been considered and used throughout the process of crafting and writing of this work. 

## **4 Related Works** 

Within our extensive literature review, as described in Section 3.2, we identified a total of 55 relevant survey and review articles. Figure 9 


**Fig. 9** : Identified Related Works (Survey corpus) composition: _GEA=general embodied AI, +RFMs=including RFMs, IND=industrial-focus._ 

shows the distribution of this survey corpus across general embodied AI (GEA), those including RFMs (+RFMs), and with explicit industrial focus (IND). A comprehensive list of all gathered surveys is provided in the Appendix (Table A1). Here, however, we concentrate on works that are most relevant to our objectives: surveys focused on RFMs, as well as those dedicated to industrial scenarios – even if their main scope does not extend to RFMs. Most surveys to date have concentrated on VLAs (as distinct sub-category of RFMs as discussed in Section 2) and their associated aspects, including architectures, challenges, learning paradigms and other core considerations as illustrated in Table 1. There are several specialised surveys addressing particular facets of the VLA landscape, such as action tokenisation [17], dualsystem architectures [31] or post-training strategies [14]. Some also discuss related model classes, like LLMs, Vision Language Models (VLMs) or Vision Foundation Models (VFMs) [12, 13, 15, 17]. Focusing on the RFM perspective, Table 1 compares the 11 surveys (20% of the 55 total) which specifically target the RFM field. Importantly, none of these works present an explicit industrial focus and almost all centre on VLAs, which forms only one distinct subset of RFMs. Merely two of those diverge from a VLA-centric approach: On the one hand, Zhou et al. [15] investigate languageconditioned manipulation, therefore bearing close resemblance to the VLA category. On the other hand, Hu et al. [12] discuss the overarching RFM paradigm, but primarily give an overview over current methodologies. Consequently, although there is a myriad of recent surveys around VLAs, comprehensive investigation of the broader RFM concept remains largely unaddressed, with virtually no attention given to further RFM subcategories – such as Vision-Action models or other control-oriented and integrated RFMs, as defined in Section 2. 

Considering industrial relevant-reviews, Figure 9 and Table 2 reveal that only 2 out of the 55 analysed surveys (3 _._ 6%) possess a clear industrial application focus. Furthermore, neither emphasises the implications of RFMs within industrial domains: Fan et al. [35] explicitly focuses on VLMs in Human-Robot Collaboration (HRC) for smart manufacturing – thus only a narrow subset of what we consider important for industrial robotics 

11 

**Table 1: RFM:** Overview of most relevant survey/ review papers with RFM focus. _Reporting the focus area, the review’s main considerations (Scope), the types of targeted model families (Models), the timespan of reviewed papers (Span), whether the survey is considered concise or extensive (Broad), and the survey’s publication year._ 

|**Ref**|**Focus Area**|**Scope**|**Models**|**Span**|**Broad**|**Year**|
|---|---|---|---|---|---|---|
|[13]|VLAs for<br>embodied AI|Architectures, challenges, components, control, datasets,<br>objectives, resources, simulators, tasks, task planning,<br>taxonomy|Encoder,<br>LLM, VLA,<br>VLM|14-24|✓|2025|
|[17]|Action<br>tokenisation<br>in VLAs|Action token categorisation: (affordance, code, goal state,<br>language, latent, raw action, reasoning, trajectory),<br>datasets, FM evolution|LFM, VFM,<br>VLA, VLM|17-25|✓|2025|
|[16]|Challenges<br>and roadmap<br>in VLAs|Applications, challenges: (dataset and evaluation,<br>execution, generalization, representation, safety),<br>evolution, roadmap, milestones, modules, opportunities|VLA|22-25|✓|2025|
||Language-|Auxiliary tasks, challenges, datasets, evaluation,|||||
|[15]|conditioned<br>robot<br>manipulation|environments, learning paradigms, limitations,<br>neuro-symbolic, planning, reasoning, reward shaping,<br>semantics extraction, task representation|FM, LLM,<br>VLA, VLM|18-24|✓|2025|
|||Architectures (hierarchical, monolithic), benchmarks,|||||
|[30]|Large VLM-<br>based VLAs|characteristics, datasets, task planning, learning<br>paradigms, memory mechanisms, multi-agents,<br>operational strengths, taxonomy|VLA|23-25|✓|2025|
|[31]|Dual-System<br>VLAs|Architectures, definition, design-elements, empirical<br>evaluation, training strategies|VLA|24-25|✗|2025|
||Post-training|Challenges, embodiment awareness, model development,|||||
|[14]|strategies for<br>VLAs|multi-component integration, perception, post-training<br>methods, task comprehension, taxonomy|VLA|23-25|✓|2025|
||VLA|Applications, architectures, benchmarks, challenges,|||||
|[32]|overview and<br>taxonomy|classification, datasets, hardware, paradigms, simulators,<br>taxonomy|VLA|21-25|✓|2025|
||VLA design|Design choices (architectures, backbones,|||||
|[33]|and<br>guidelines|cross-embodiment), guidelines, performance comparison,<br>RoboVLMs|VLA|22-24|✗|2025|
|[34]|VLA<br>advancement<br>synthesis|Agentic AI, architectures, challenges, concepts, control,<br>cross-embodiment, domains, evolution, foundations,<br>planning, real-time, training strategies|VLA|22-25|✓|2025|
||FMs for|Benchmarks, challenges (generalisation, data scarcity,|||||
|[12]|general-<br>purpose<br>robotics|safety, requirements, task specification), control, datasets,<br>FM application, manipulation, perception, RFM<br>characteristics, task planning, taxonomy|LLM, RFM,<br>VFM, VLM|22-24|✓|2024|


**Table 2: IND:** Overview of most relevant survey/ review papers with industrial focus. 

|**Ref**|**Focus Area**|**Scope**<br>|**Models**|**Span**|**Broad**|**Year**|
|---|---|---|---|---|---|---|
|[35]<br>[36]|VLMs in HRC for<br>smart manufacturing<br>Embodied<br>intelligence in smart<br>manufacturing|Architectures, human-robot skill transfer,<br>limitations, manipulation, navigation, pretraining,<br>task planning<br>Applications, architecture, challenges,<br>characteristics, capabilities, limitations|LLM, VLM<br>N/A|20-24<br>N/A|✓<br>✗|2025<br>2024|


applications (see Section 7) – while also focusing solely on higher-level VLMs, rather than on RFMs. Ren et al. [36] conceptually address general embodied intelligence, evaluating capabilities and limitations in industrial contexts, but they do not consider any specific models or what the industrial use case may imply for a given type of model. Synthesising these findings, we expose a pronounced gap in the literature: given our corpus, there is currently no survey dedicated to the industrial application of RFMs or implications of 

industrial use cases on RFMs, not even within the restrictively narrower context of VLAs. Industrially focused surveys are predominantly either too general or limited to specific facets (e.g. VLMs in HRC). By contrast, our work diverges from the prevailing focus on VLAs’ architectural or functional paradigms. Instead, besides discussing taxonomy and giving an extensive overview over the RFM landscape, we provide a detailed analysis of the attributes and capabilities demanded of RFMs by industrial use cases, elucidating how 

12 

such requirements should shape or be integrated into future RFM design and how industrial maturity can be evaluated in given approaches – a perspective unmet in current literature. 

## **5 Rise of Cobots in Industry** 

Recent advances in RFMs are predominantly demonstrated alongside cobots, yet these developments are frequently confined to laboratory, table-top or kitchen settings. To highlight the broader industrial significance of this trend, it is essential to first consider the evolution of industrial robotics and the transition toward more collaborative robotic systems. 

### **5.1 Landscape of Industrial Robotics: Tradition & Transformation** 

Industrial robots have long constituted a fundamental component of automated manufacturing, typically defined as automatically controlled, reprogrammable multipurpose manipulators, programmable in three or more axes and intended for use in industrial automation applications [37, 38]. Core to their design is an incomplete-machine architecture, requiring the integration of additional tooling such as grippers or welding torches to fulfil specified tasks. Their flexibility stems from complex series structures – kinematic chains with multiple rotational degrees of freedom – which provide mobility and adaptability across a broad range of production processes. [38, 39] However, traditional industrial robots are primarily programmed for pre-defined, automated function and demand specialised expertise for complex reprogramming. Due to their high speeds and significant payload capacities, they typically operate in designated spaces separated from human workers for safety reasons and are thus commonly deployed for heavy-duty, repetitive or hazardous industrial tasks. [40–42] 

To solve varying tasks within automation, several industrial robotic configurations have emerged, ranging from highly specialised parallel structures to general-purpose articulated arms. They typically make use of revolute (R) or prismatic (P) joints and can be classified into six categories [41, 43, 44], which are shown in order of increasing similarity to cobots within Table 3. 

**Table 3:** Main industrial robot configuration categories. [41, 45–48], [49, pp. 72, 222, 452, 1393] 

|**Type**|**Config**|**Comments**|
|---|---|---|
|Delta|(PPP)<br>Parallel|• Several symmetric kinematic<br>chains<br>• High speed & acceleration<br>• Redundancy increases<br>accuracy|
|Cartesian|(PPP)<br>Serial|• Perpendicular prismatic joints<br>• Smooth linear movement<br>• Rectangular workspace|
|Cylindrical|(RPP)<br>Serial|• Rotational base combined<br>with two prismatic joints<br>• Cylindrical workspace|
|SCARA|(RRP)<br>Serial|• Both revolute joints along the<br>same axis<br>• High accuracy & repeatability<br>• Planar positioning|
|Spherical<br>Arm|(RRP/RRR)<br>Serial|• Revolute axes intersect at a<br>common center point<br>• Simplifies collision &<br>reachability analysis<br>• Spherical workspace|
|Articulated|(RRR)<br>Serial|• Revolute joints’ axes<br>typically offset<br>• Similar to human arm<br>• Flexible 3D workspace|


Despite their varied forms and operational strengths, these traditional industrial robot types inherently lack the flexibility, adaptability, safe direct HRC and Human-Robot Interaction (HRI) – attributes now increasingly demanded by modern manufacturing, especially Small- and Mediumsized Enterprises (SMEs)[50–53]. **Cobots** have emerged as a dedicated response to these limitations. Initially introduced as intrinsically passive devices designed for operator guidance and constrained movement [54, 55], cobots have evolved into a distinct subcategory of industrial articulated robots engineered to operate safely and efficiently alongside humans. Contemporary definitions emphasise their lower payloads, reduced speeds, rounded geometries and sensor suites for real-time contact or human detection, allowing safe intentional HRC [39, 56–58]. Importantly, cobots are tailored for flexible deployment, intuitive HRI and programming as well as rapid reconfiguration – minimising downtime, setup costs and enable frequent application changes. This makes them particularly attractive for SMEs requiring high product variability and small batch sizes. [39, 56–59] The principal differentiator from 

13 

traditional industrial robots lies in their functional ethos: while conventional robots are generally engineered to replace human involvement – automating entire processes within isolated environments – cobots are expressly intended to enhance human capability by enabling joint execution of complex, variable, or ergonomically challenging tasks. Rather than aiming for maximal speed or payload, cobots prioritise safe cooperation, ease of integration and efficiency gains through shared workflows. [40] 

### **5.2 Productive Cobot Applications & Domains** 

Due to their increased flexibility and safety compared to traditional industrial robots, modern cobots have exceeded their origins in laboratory and demonstrator settings to become integral elements across a wide spectrum of real-world industrial and commercial domains, from manufacturing floors to healthcare and logistics: **Manufacturing and Assembly:** Cobots are frequently deployed in the manufacturing sector, particularly in tasks that require consistent precision alongside adaptability, such as assembly, pickand-place operations, machine tending, quality inspection, palletising, packaging, general material handling and welding or gluing [50, 60, 61]. Concrete examples include the use of Universal Robots’ UR10e cobots at PSA and Fiat Chrysler automotive assembly plants for activities such as door, hood and soft-top assembly, alongside riveting and mounting [60]. Further applications include repetitive pick-and-place tasks in plant nurseries, automated packaging in board manufacturing or assistance in soldering, drilling and arc welding processes in metal working environments. [50, 60, 62]. 

**Quality Control and Inspection:** By leveraging advanced sensor and computer vision systems, cobots perform real-time inspection of part dimensions, assembly integrity and defect detection. In electronics manufacturing, for example, UR3s are efficiently utilised for quality inspection of automotive touchscreen panels [60]. These inspection roles leverage the cobots’ repeatability, adaptable end-effectors and their capacity to be easily reconfigured for frequent product changes. [50, 60, 61] **Material Handling, Logistics, and Mobile** 

**Manipulation:** Industrial environments frequently integrate cobot arms with Autonomous Mobile Robot (AMR) platforms, resulting in mobile manipulators that can transport goods between workstations, feed machines and thus enable flexible and precise in-factory logistics. Concrete use cases include the movement of assembly components using MiR200 AMRs in appliance manufacturing [60], as well as the management of heavy, repetitive, or ergonomically challenging transport tasks, thus enabling more agile and just-in-time production processes. [42, 59, 60]. 

**Healthcare:** Cobots support patient handling, rehabilitation, medication dispensing and precise surgical assistance. Applications include robotic surgery, manipulation of medical tools and remote ultrasound or endoscope positioning [50, 52, 63]. **Agriculture:** Tasks include precise planting, harvesting and sorting in harsh or unpredictable environments. During periods of high-volume workloads, continuous 24/7 operation can reduce reliance on manual seasonal labour for highly repetitive tasks. [60, 63] 

**Retail and Service:** Cobots assist with shelf stocking, object retrieval and customer engagement, thereby improving service quality and operational efficiency in commerce and hospitality sectors [52, 63]. 

**Military, Security and Inspection:** To increase throughput and operator safety, cobots equipped with specialised sensors, are employed in luggage scanning, dangerous substance detection, bomb disposal, facility inspection, cleaning and delicate manipulation tasks in environments such as spacecraft maintenance, hazardous material operations, airport and public security contexts. [50, 63, 64] In particular, cobots have been employed to inspect and clean the Space Rider orbiter’s surfaces during extended missions [52], for bomb defusing during military operations using specialised tools [63], or for assistance of military personnel during border inspection [50]. 

### **5.3 Drivers of the Industrial Shift Toward Cobots** 

As implied by the adoption of cobots across diverse sectors outlined in Section 5.2, there has been a notable shift within industrial and commercial domains from exclusive reliance on 

14 

manual labour or traditional industrial robots towards increasing adoption of cobots. This shift is driven by a broad array of factors – technological, organisational and economical – that collectively highlight the growing necessity for adaptable, user-friendly and interactive automation solutions within diverse industrial domains. Traditional industrial robots, with their high payload capacities, precision and speed, have long been essential for large-scale manufacturers focusing on high-volume, repetitive processes. However, these systems, which are complex, expensive, and difficult to reconfigure, often prove unsuitable, especially for SMEs whose operational requirements centre around low-volume, high-mix production. [59, 65, 66] Cobots directly address these needs through their more flexible design, compact footprint and comparable ease of programming, enabling straightforward redeployment across varying tasks and locations within manufacturing environments [59, 60, 67]. Notably, cobots claim to offer user-friendly interfaces and intuitive teach modes, thereby reducing the need for specialised engineering expertise and minimising integration time [61, 67]. Aside from increasing operational efficiency, cobots are intended to directly assist human workers by taking over repetitive, physically demanding, or hazardous tasks, thus enhancing workplace safety and allowing human operators to focus on assignments requiring higher cognitive skills and problemsolving abilities [40, 58, 59]. In contrast to conventional industrial robotics, their design enables direct HRC, allowing the combination of human creativity with robotic reliability and precision in shared workspaces [58, 67]. Several safety features – including real-time sensor integration, force/torque monitoring and intelligent behaviour adaptation – are intended to enable cobots to operate closely with people, reducing the need for impractical and expensive barriers or isolated cages for a respective use cases [39, 60, 61, 63]. In addition to optimising available production space, this also enables workflow modernisation and a reduction in ancillary costs. 

The increasing demand for cobots is reflected in both industrial practice and research trends. While the total volume of publications on traditional industrial robots remains higher, Khedr et al. [56] showed in their survey, that the growth rate of cobot-focused research has accelerated 

rapidly in recent years – over 5-fold within a single decade – underscoring their expanding role in advanced manufacturing and their rising relevance for future automation solutions [56]. This is also supported by the absolute number of global installations: Annual cobot deployments have increased from 11,000 units in 2017 to 55,000 units in 2022, reflecting not only ongoing innovation but also expanding industrial uptake alongside continued strong deployment of conventional robots [41, 68]. Correspondingly, the International Federation of Robotics has noted a consistent increase in the proportion of cobots relative to traditional industrial robots [68]. Beyond hardware, advanced technologies such as computer vision and adaptive control algorithms have extended cobot capabilities, paving the way for more sophisticated and autonomous interaction within dynamic industrial settings [60, 69]. This ongoing evolution aligns with the principles of Industry 4 _._ 0, where digitalisation, interconnectivity and smart automation require flexible systems competent of both autonomous operation and collaborative behaviour. Given sufficiently capable control methods, cobots could be increasingly integrated as key components of smart factories, to connecting with other industrial Internet of Things (IoT) devices and AI-driven systems, enable data-driven optimisation, remote operation and rapid reconfiguration for changing market demands [59, 61, 68, 69]. 

### **5.4 Towards Intelligent & Collaborative Automation** 

Despite these advances, there remain specific challenges and requirements for cobot deployment in industrial environments. While cobots are effective at supplementing human labour and undertaking routine or ergonomic tasks, their ability to autonomously handle complex, cognitive, or dexterous processes is still limited [40]. Issues such as real-time hazard detection, continuous safe operation, as well as trustworthy HRI and HRC call for further development of sophisticated control strategies and intelligent interfaces. This is particularly pertinent regarding trust and transparency during both initial deployment and ongoing operation, which are regarded as critical success factors for the introduction of cobots [40, 58]. In this context, RFMs – as introduced in Section 2 – have 

15 

the potential to address many of these emerging challenges. RFMs, when integrated in industrial cobot platforms, can provide powerful tools for intuitive instruction, autonomous decision-making and real-time adaptation by leveraging natural language inputs, multisensor fusion and advanced reasoning capabilities. Both, cobots’ productive use cases and their current limitations form a perfect fit for RFM integration, making the assessment of emerging RFMs’ industrial applicability crucial. Future research must focus on ensuring that these models are not designed solely for controlled laboratory settings, but are robust and effective within the complex, variable and safetycritical landscapes of actual industrial operation. In summary, the ongoing move from traditional industrial robots to cobots reflects a broader reorientation of manufacturing towards collaborative, intelligent and flexible automation. This transition underscores two key aspects: (a) the industrial relevance and necessity of RFMs, which have high potential to directly shape the capabilities, accessibility and trustworthiness of next-generation collaborative robotics; but conversely (b) cobots also create the deployment pressure that exposes the limitations and weak points of current RFMs for productive use. 

## **6 Cobot & Compute Hardware** 

To meaningfully assess the maturity and applicability of RFMs in industry, it is essential to first understand the capabilities and typical platforms for deployment. As discussed in Section 5, contemporary cobots still inherently lack the ability to autonomously handle complex or cognitive tasks – gaps that RFMs are well positioned to address. However, evaluating RFMs without reference to the practical capabilities, such as reach, payload, accuracy and utilised perception or manipulation hardware of commonly used cobots, we would risk incomplete analysis. Additionally, considerations such as power consumption and inference hardware, which are often overlooked in scientific studies, are critical for translating laboratory results to industrial applications. Clear insight into typical industrial computing platforms and their real-world performance is thus necessary. Therefore, this section provides an overview of the key hardware and system components required for the deployment of cobots in industrial settings. We 

examine the quantitative capabilities and power consumption profiles of contemporary cobots in Section 6.1, the characteristics and suitability of industrial edge computing platforms necessary for real-time control and inference in Section 6.3, and the essential sensing and manipulation hardware required for real-world robotic applications in Section 6.2. Through a combination of survey data and representative hardware comparison, we elucidate technical prerequisites for integrating RFMs in cobotic environments, considering robot capability, computational infrastructure, sensor integration and operational efficiency. 

### **6.1 Cobot Capabilities & Power Consumption** 

To highlight aforementioned prerequisites for RFM integration and to assess cobots suitability across various industrial tasks, a quantitative understanding of contemporary cobots’s capabilities is crucial. To this end, an extensive survey of cobots by Taesi et al. [50] provides comprehensive data, which we have synthesised in Tables 4 and 5, reporting minimum, maximum, mean, and median values across key specifications. In the following, only the articulated anthropomorphic cobots of [50] are considered, consistent with the typical definition of cobots as presented in Section 5.1. 

**Table 4:** Composed cobot configuration and capability statistics. [50] _Values are rounded to two decimal places._ 

|_n_= 180|**DoF**|**Payload**|**Reach**|**Accuracy**|
|---|---|---|---|---|
|||**(kg)**|**(mm)**|**(mm)**|
|**Min**|4|0.3|280|0.01|
|**Max**|7|170|2790|1|
|**Mean**|6.09|8.56|970.12|0.09|
|**Median**|6|5.5|910|0.05|


Table 4 aggregates statistics from 180 articulated cobot models, focusing on Degree of Freedoms (DOFs), payload, reach, and accuracy. The majority of cobots feature a mean of 6 _._ 09 DOFs, underscoring the dominance of six-axis articulated robots in collaborative applications. Typical payload capacity spans a median of 5 _._ 5kg (mean: 8 _._ 56kg), clearly indicating that most commercially available cobots are optimised for handling 

16 

moderate loads. The average reach is approximately 910mm (mean: 970mm) and positioning accuracy is typically very precise, ranging from a median value of 0 _._ 05mm to a mean of 0 _._ 09mm. Notably, there is a significant spread in both payload and reach, with extreme cases such as the Comau Aura, which offers a payload up to 170kg and a reach of 2790mm. While the presence of high-payload outliers slightly biases the mean values upwards, these statistics capture the core capabilities of most cobots deployed in industrial contexts and confirm the suitability of cobots for applications prioritising moderate payloads, high repeatability and operational flexibility across a diverse range of industrial fields as specified in Section 5.2. 

**Table 5:** Composed peak cobot TCP velocity and power consumption statistics. [50] _Showing only values for typical cobots with a payload between_ 0 _._ 5 _and_ 20 _kg as in the wattage comparison of Taesi et al. [50]. Values are rounded to two decimal places._ 

|_n_= 63|**Payload**|**TCP**<br>**Velocity**|**Power**<br>**Consumption**|
|---|---|---|---|
||**(kg)**|**(m/s)**|**(kW)**|
|**Min**|0.5|0.2|0.06|
|**Max**|20|6|0.9|
|**Mean**|6.69|1.68|0.31|
|**Median**|5|1.1|0.25|


Table 5 provides insight into the dynamic performance and power requirements of typical cobots rated for payloads between 0 _._ 5 and 20 kg – as those more accurately represent the average cobot identified in table 4. The maximum Tool Center Point (TCP) velocity for these models ranges from 0 _._ 2 to 6 m/s, typically between 1 _._ 1 and 1 _._ 68 m/s. Power consumption is remarkably restrained compared to conventional industrial robots: typically between 0 _._ 25 and 0 _._ 31 kW, with a maximum of 0 _._ 9 kW for heavier-duty models within this class of cobots as shown in table 5. This is in strong contrast to traditional industrial robots, whose average power usage has been estimated at around 3 kW by Barnett et al. [70], with peak draws measured as high as 12 kW (KUKA KR60HA) [71] or 

over 15 kW (KUKA KR210 R2700) [72] and sustained values near 6 kW under typical acceleration or velocity [71, 72]. The lower energy requirements of cobots yield significant operational cost advantages, facilitate use in environments with lower power infrastructure and enable deployment on mobile or battery-powered platforms. Importantly, these comparatively low power requirements have direct effect on the hardware selection and computational strategy for cobots control, thus RFMs: Successful real-time deployment requires models that operate efficiently within the constrained energy budgets typical of cobotic systems, particularly for mobile or battery-powered applications. Achieving low-latency inference on hardware that adheres to strict industrial power limits underscores the importance of model efficiency. 

### **6.2 Sensing & Manipulation Hardware** 

**Sensors** are essential to the functional operation of cobots, serving as the primary means for environmental perception and self-monitoring. Their central role covers key industrial aspects such as HRC, HRI, autonomous navigation, manipulation and real-time task execution [52, 73]. A variety of sensor types are commonly deployed in both research and industrial cobotic settings [40, 42, 50, 52, 57, 61, 62, 65, 73–75]: 

- **Visual:** RGB (single/stereo), depth, ChargeCoupled Device (CCD) and 2D/3D vision sensors 

- **Range:** Light Detection and Ranging (LiDAR), Radio Detection and Ranging (RADAR), Sound Navigation and Ranging (Sonar), ultrasonic, Time-of-flight (TOF)/Photonic Mixing Device (PMD) and laser scanners 

- **Dynamics:** Inertial Measurement Units (IMUs), gyroscopes, accelerometers, force/torque sensors, tactile and pressure sensors 

- **Position and Identification:** Encoders, Radio Frequency Identification (RFID), infrared, Global Positioning System (GPS), odometry and magnetic sensors 

- **Specialised:** Acoustic, thermal and similar sensors 

17 

Advanced applications, such as RFMs, can benefit from sensor fusion, combining modalities such as vision with proximity, inertial, or force/torque measurements to increase perception robustness and accuracy [52]. Configurations can involve redundant or complementary sensing to support safety, compliance, and reliable manipulation – for example, using visual and tactile feedback for precise object handling, or adding force sensors to detect unwanted contact in collaborative settings. **End-effectors** constitute the physical interface for manipulation tasks and are tailored to specific application requirements. As outlined in Section 5.1, the integration of these interfaces is essential for enabling an industrial robot/ cobot to perform its designated tasks. Concrete examples include grippers with configurable fingers and pads, suction cups, dual-stage end-effectors incorporating both gripping and suction capabilities or custom tooling such as drills and polishers for advanced operations [62, 65]. Many end-effectors embed their own dedicated sensors [42] – such as force feedback for manipulation tasks or embedded vision modules for object detection and pose estimation. Notably, the modularity of modern cobot end-effectors allows quick adaptation to varying industrial tasks, which increases reusability and operational uptime. Nonetheless, attaining this level of modularity assumes similar flexibility in action-space of the control algorithm. Overall, the selection and integration of sensors and end-effectors play a pivotal role in the industrial applicability of cobots and must be considered for deploying robust and efficient RFMs in real-world scenarios. Specifically, the sheer amount of sensing and manipulation hardware results in an even greater number of observation/action-space permutations, further highlighting the need for multi-modality and output flexibility in modern control algorithms – capabilities central to RFMs (cf. Section 2). 

### **6.3 Industrial Edge PCs** 

Given the low-latency requirements of cobotic applications, computational platforms for realtime AI-control and -perception are often realised as edge devices – hardware installed as close to the robot and its data sources as feasible, often directly integrated into the cobot’s controller or platform. They are characterised by processing 

real-time data locally rather than relying on cloud or external datacentres. [80] This proximity is vital for latency-sensitive robotic applications, especially for mobile or remote environments, where network traffic must be kept to a minimum [81]. Alternative paradigms such as fog or cloud computing can provide scalable resources but come at the cost of additional infrastructure or third-party service requirements. Fog computing, as defined by Yi et al. [82], encompasses distributed and collaborative architectures involving heterogeneous devices close to the edge, but still depends on nonlocal hardware and stable networking. Classical cloud computing, while enabling on-demand computational resources, is generally associated with higher latency, lower throughput and an increased risk of service interruption – limitations that are particularly problematic for time-critical robotic control. [82–84] According to Ismail et al. [85], moving computation closer to the edge grows increasingly important for industrial deployments, due to a drop in compute costs and the operational advantage of minimising recurring networking expenses [85]. Accordingly, we provide an overview of currently available, representative edge devices to clarify relevant hardware requirements for industrial RFM deployment and to establish a foundation for real-world inference evaluation and power consumption considerations. For the quantitative hardware analysis presented in Table 6, we selected NVIDIA as the representative manufacturer for several reasons. Their Jetson devices are among the most widely adopted platforms for edge AI in robotics research and industrial applications, offering a standardised and scalable portfolio (from the compact Nano to the new high-end Thor series). Most importantly, relevant performance metrics, pricing, and other specifications are consistently documented and publicly available for the entire product family. This transparency enables an accurate, fair, and reproducible comparison of hardware options and their suitability for running modern robotic control methods, predominantly based on AI models. While Table 6 concentrates on the Jetson portfolio, a range of alternative manufacturers – such as Siemens, AMD (Xilinx), Intel, Advantech or Beckhoff among others [86] – also provide relevant edge devices. However, for many of these alternatives, comparable and up-to-date public data on 

18 

**Table 6:** Comparison of NVIDIA edge devices’ AI performance in INT8 precision (dense) [76–78]. _Prices for all Jetson devices correspond to single-unit purchases from the same NVIDIA-specified retailer_ [79] _, collected on the same date. Operational costs are estimated for 24/7 usage with 0.25$/kWh. All values are rounded to two decimal places. Su = Super, DK = Developer Kit, IND = Industrial_ 

|**Jetson**|**Price**|**TOPS**|**Memory**|**Power**|**GOPS**|**TOPS**|**Memory**|**$**|**TOPS**|
|---|---|---|---|---|---|---|---|---|---|
|**Device**|**($)** _↓_|**(INT8)** _↑_|**(GB)** _↑_|**(W)** _↓_|**/$** _↑_|**/W** _↑_|**(MB)/$** _↑_|**/year** _↓_|**/y$** _↑_|
|Orin Nano 4GB|229|34|4|25|148.47|1.36|17.47|54.75|0.62|
|Orin Nano 8GB|249|67|8|25|269.08|2.68|32.13|54.75|1.22|
|Orin Nano SuDK|249|67|8|25|269.08|2.68|32.13|54.75|1.22|
|Orin NX 8GB|479|117|8|40|244.26|2.93|16.7|87.6|1.34|
|Orin NX 16GB|699|157|16|40|224.61|3.93|22.89|87.6|1.79|
|Orin AGX 32GB|999|200|32|40|200.2|5|32.03|87.6|2.28|
|Orin AGX 64GB|1799|275|64|60|152.86|4.58|35.58|131.4|2.09|
|Orin AGX DK|1999|275|64|60|137.57|4.58|32.02|131.4|2.09|
|Orin AGX IND|2349|248|64|75|105.58|3.31|27.25|164.25|1.51|
|Xavier NX|502|21|8|15|41.83|1.4|15.94|32.85|0.64|
|Xavier NX 16GB|579|21|16|20|36.27|1.05|27.63|43.8|0.48|
|Xavier AGX|999|32|32|30|32.03|1.07|32.03|65.7|0.49|
|Xavier AGX 64GB|1399|32|64|30|22.87|10.7|45.75|65.7|0.49|
|Xavier AGX IND|1449|30|32|40|20.7|0.75|22.08|87.6|0.34|
|Thor T5000|3199|517|128|130|161.61|3.98|40.01|284.7|1.82|
|Thor AGX DK|3499|517|128|130|147.76|3.98|36.58|284.7|1.82|
|**Min**|229|21|4|15|20.7|0.75|15.94|32.85|0.34|
|**Max**|3499|517|128|130|269.08|5|45.75|284.7|2.28|
|**Mean**|1292.31|163.13|42.25|49.06|138.42|2.77|29.26|107.45|1.27|
|**Median**|999|92|32|40|148.11|2.8|32.02|87.6|1.28|
|RTX 5090<sup>_a_</sup>|_2600_|838|N.A.|575|322.31|1.46|N.A.|1259.25|0.67|


_aPricing estimated due to fluctuation and local availability at time of writing. As Jetson Devices use low-power DDR memory (LPDDR) for the complete system and the RTX cards are supplied with dedicated graphics memory (GDDR), those values are not considered._ 

prices, performance (in AI-relevant metrics) and efficiency is often limited or unavailable. We additionally report the specifications of a desktop-class Graphics Processing Unit (GPU), the RTX 5090, to provide context for typical platforms used in academic benchmarking of foundation and control models. While the RTX 5090 is not an edge device, but a standalone GPU intended for workstations and servers, it serves as a reference point for the upper bound of single-device computational performance in recent literature. Comparing the RTX 5090 to integrated Jetson devices highlights the trade-offs between desktop/workstation-grade and edge-class hardware. Examining the comparative statistics in Table 6 reveals several significant trends relevant to both industrial and research 

applications. The Orin Nano series stands out for its exceptionally low entry cost and high performance relative to purchase price, making it more suitable for cost-sensitive or large-scale deployments. On the other hand, the entry-level Xavier NX – while more expensive – provides the lowest overall AI compute performance in the lineup. However, its 8GB variant is noteworthy for having the lowest maximum power consumption across all compared models, potentially favoring applications where minimal energy draw is of essence. The mid-tier, such as the Orin AGX 32GB, provide a balance between increased computational capability and moderate power requirements. Notably, the Orin AGX 32GB emerges as the most efficient device in terms of compute power per operational 

19 

cost, offering a strong compromise for applications prioritising both capability and efficiency. At the high end of the spectrum, devices like the Jetson Thor series or workstation-class desktop GPUs exhibit strong increases in computational throughput. However, this heightened performance is directly linked to substantial rises in both energy consumption and annual operational costs – a factor that can restrict their scalability and render them impractical for mobile, battery-powered, or energy-constrained robotics platforms. Particularly, the RTX 5090 can consume more than twice the power of a median cobot as shown in Table 5. This contrast towards edge devices’ power draw, underscores that desktop GPUs are designed for short, intensive workloads or for environments where energy is abundant, whereas edge devices are optimized for consistent, energy-efficient use in real-world, often resource-constrained settings. Thus, a trade-off emerges: deploying larger and more capable RFMs is constrained by both compute and energy efficiency considerations, underscoring the importance of aligning model design with operational cost and industrial practicality. Additionally, industrial-class devices (IND) frequently employ features such as ECC-memory for increased reliability, which can raise both initial and operational expenses or lower computational power compared to standard research hardware. 

## **7 General & RFM-specific Industrial Implications** 

Industrial deployment settings impose constraints and expectations that systematically differ from laboratory environments: they combine heterogeneous hardware, tight safety and compliance obligations, high reliability targets, and continuous operational pressures. This section therefore distils the recurring industrial viewpoints extracted from our industrial implication corpus (Section 3.3) – aligned with our discussions in Sections 5 and 6 – into an assessmentoriented structure that can be used to analyse how well current and future RFMs comply with real-world industrial demands. We proceed in three steps: First, Section 7.1 synthesises the corpus into eleven _general industrial implications_ that capture the dominant, domainagnostic requirements reported across industrial 

robotics applications and that are supported by our cobot- and hardware-related considerations. Second, Section 7.2 translates these implications into a structured set of _attributes_ that enable a more fine-grained discussion of where industrial constraints can manifest in practice within RFMs and their surrounding ecosystem. Third, Section 7.3 consolidates these considerations into a comprehensive criteria catalogue intended to support a consistent, transparent evaluation of industrial maturity across existing RFMs. 

### **7.1 General Industrial Implications** 

To derive general, domain-agnostic implications from the industrial implication corpus (Section 3.3), we conducted an iterative qualitative synthesis across the 125 manually reviewed works. Concretely, we (1.) extracted statements that described recurring industrial requirements, constraints, and deployment challenges for robotic systems (both explicitly and as implied by described industrial case studies), (2.) grouped these excerpts into thematic clusters, and (3.) iteratively refined and consolidated the most prominent clusters until they formed a compact set of implications that was sufficiently expressive to capture the dominant industrial viewpoints while remaining actionable for later assessment of RFMs. Throughout this process, we noticed no explicitly contradictory themes, instead found the implications to be _interdependent_ rather than mutually exclusive: industrial authors frequently discuss the same practical challenge (e.g. human presence) through different lenses such as safety, interaction design, robustness, or perception, and our synthesis preserves these overlaps by separating _what is demanded_ from _why it is demanded_ . The resulting set comprises eleven implications, each reflecting a recurring industrial expectation about deployed robotic applications and, by extension, about learning-based robot control and foundation-model-based approaches. In the following, we motivate each detected implication by summarising the corresponding clusters from the literature corpus. 

#### **_Implication 1: Adaptability_ &** **_Flexibility_** 

Across industrial domains, authors consistently describe variability as a defining property of real deployments: processes change, product variants 

20 

proliferate, and boundary conditions shift, which in turn increases re-parameterisation effort and uncertainty [87–89]. Multiple works contrast this with classical industrial automation, emphasising that traditional solutions are often designed for repetitive, tightly structured workflows and tend to be brittle under even minor process changes [36, 90, 91]. As a consequence, adaptability is framed not merely as a convenience but as a key enabler for future “fast and low-cost” production and for increasing personalisation [36, 92, 93]. The corpus further highlights that industrial environments are frequently dynamic, partially known, or unstructured, with unpredictable events and random disruptions being expected rather than exceptional [51, 89, 94]. This is intensified when humans are present in the workspace [51, 95]. Several authors therefore argue for robots and control methods that can adjust behaviour online, be reconfigurable across products and processes, and reduce costly reprogramming cycles [88, 95–97]. In addition, sector-specific discussions (e.g. logistics/warehousing, outdoor industry) underscore that environmental variation (lighting, weather, clutter) can materially affect operation and must be handled robustly [98, 99]. Additionally, as outlined in Sections 5 and 6.2, cobots are seeing growing adoption in industry due to their flexible design and ease of reconfiguration. However, such adaptations must also be reflected within the applied control system. Only methods that are intrinsically agnostic to changing tasks, embodiments or sensor setups and quality would enable cobots to realise their full intended potential. Taken together, the literature motivates adaptability and flexibility as a primary industrial implication: systems are expected to cope with frequent task, process, and environment variation while avoiding extensive downtime and engineering overhead [91, 96, 100]. 

#### **_Implication 2: Safety_ &** **_Compliance_** 

Safety is consistently portrayed as a gating factor for industrial deployment, particularly in shared workspaces, physical interaction, and other highconsequence settings [51, 101, 102]. This is of especial relevance owing to the expanding implementation of cobots, as described in Section 5: Despite being intended to significantly reduce the need for physical separation between workers and robots, deploying cobots in shared workspaces requires an equally safety-aware control logic. Such safety 

awareness spans both general considerations that injuries must be prevented in human-shared environments [51, 103] and more explicit arguments that intelligent or adaptive robots must be tested, certified, and equipped with appropriate safety features prior to deployment [96]. Critically, multiple works connect safety to standards and certification frameworks as a prerequisite for industrial acceptability. The literature cites the role of ISO standards for safe installation and operation of robotic systems (e.g. ISO10218) and for collaborative operation and contact-related constraints (e.g. ISO/TS15066), as well as further regional standards [104–106]. Beyond formal compliance, several authors emphasise that safety must be maintained under dynamic and unpredictable conditions, including human behavioural variability and sensing uncertainty [34, 36, 107]. Industrial discussions also note that safety mechanisms can reduce efficiency if they trigger overly conservative stops or interruptions, motivating approaches that integrate safety-aware reasoning and sensing to preserve productivity without compromising protection [68, 108, 109]. Overall, the corpus motivates safety and compliance as a distinct implication: industrially viable systems must satisfy relevant safety norms and preserve safe operation under realistic uncertainty, including failures and Out-Of-Distribution (OOD) inputs [34, 94, 107]. 

#### **_Implication 3: HRI_ &** **_HRC_** 

In line with the drivers for the rising adoption of cobots discussed in Section 5.3, a significant segment of the literature likewise envisions future industrial robotics as inherently human-centric, where robots and humans work in proximity or physical collaboration to combine human flexibility and cognitive skills with robotic repeatability and precision [110–112]. The literature uses established interaction taxonomies (e.g. differentiating coexistence, cooperation, and collaboration; and distinguishing remote, proximity, and physical interaction) to emphasise that industrial scenarios span multiple interaction regimes and thus demand correspondingly diverse interface and coordination solutions [93, 103, 113]. Works addressing HRC further highlight that direct physical collaboration is valued for its flexibility, but requires the robot to perceive contact and respond appropriately [92, 114]. Beyond 

21 

physical coordination, authors repeatedly emphasise that communication quality and interface usability are decisive for acceptance and productivity. This includes calls for more intuitive, comfortable, and natural interaction, including speech and other modalities, to reduce reliance on expert programming and to better support operators in real time [36, 115, 116]. Several works discuss that current industrial control and programming workflows remain labour-intensive, motivating approaches that allow operators to instruct, supervise, and correct systems more directly [88, 97, 117]. The literature also points out that collaborative scenarios require reactive methods that can handle uncertainty and unexpected behaviour to maintain fluid workflow between humans and robots [103, 118]. Hence, HRI and HRC emerge as a separate implication: industrial systems are expected to support humancentred collaboration with effective, natural communication and continuous operator involvement, particularly for complex, variable, and partially automatable tasks [35, 51, 104]. 

#### **_Implication 4: Robustness_ &** **_Reliability_** 

Industrial environments are repeatedly characterised as uncertain, noisy, and prone to disturbances and component imperfections. Authors discuss both internal uncertainties (e.g. unmodelled dynamics, friction effects, sampling delays) and external uncertainties (e.g. measurement errors and environmental noise) as persistent challenges for deployed systems [100, 119]. This leads to calls for robust methodologies that can integrate perception, planning, and control under uncertainty, especially in complex systems such as warehouse automation or autonomous mobility [51, 120]. Reliability is also linked to monitoring and timely status updates in order to support reactive planning and practical operation [108]. Importantly, the corpus extends robustness beyond stochasticity to include resilience against faulty sensors and OOD inputs, noting that invalid sensor readings can induce unpredictable outputs in learning-based systems and may be particularly dangerous in safety-critical contexts [107]. Further, some works explicitly consider adversarial and cybersecurity threats as integral requirements for industrial robots [121, 122]. Accordingly, robustness and reliability form a distinct implication: deployed systems are expected to maintain 

stable operation under uncertainty, disturbances, sensor degradation and security threats, while providing operationally meaningful status and fault awareness [34, 102, 107, 121]. 

#### **_Implication 5: Precision_ &** **_Accuracy_** 

While flexibility and generalisation are emphasised, the industrial corpus simultaneously stresses that robots derive value from high precision, repeatability, and quality-critical execution [110, 123]. Several works frame industrial competitiveness in terms of efficiency _and_ accuracy, reflecting that many tasks require both throughput and reliable outcome quality [124, 125]. Moreover, accuracy is not restricted to actuation: sensing and perception accuracy is treated as foundational for safe and correct operation [121, 126]. Shen et al. [126] further note that current systems can exhibit insufficient grasping and positioning accuracy in demanding settings, motivating improved sensing and algorithms. In the context of vision/language-guided robot control, Fan et al. [35] explicitly highlight the gap between householdstyle demonstrations and industrial requirements, including the need for higher precision and improved motion planning accuracy while retaining flexibility and generalisation. Therefore, precision and accuracy form an implication in their own right: industrial deployment demands consistent, quality-aligned execution and perception accuracy, often under noisy or varying sensing and environmental conditions, while preserving the required throughput to enable efficient workflows [35, 100, 124, 125]. 

#### **_Implication 6: Real-Time Performance_** 

Real-time capability is presented as a pervasive constraint affecting sensing, decision-making, interaction and control. The corpus references execution-time considerations (e.g. action-level and task-level timing) [51] and highlights low-level requirements such as real-time communication and motion control in integrated robotic systems [53]. For industrial autonomy more broadly, authors emphasise real-time sensing and processing needs, including the acquisition of real-time environmental information and the integration of multi-modal signals to enable both sudden responses and higher-level reasoning [36, 52, 127]. Several works connect real-time feasibility to computational and resource constraints, especially for 

22 

edge deployment, and note that data-driven methods are often limited by computational complexity and large training/inference requirements [115, 128, 129]. Indeed, as illustrated in Table 6, even the most capable contemporary edge-devices lag significantly behind modern workstation GPUs in computational power, as their design prioritises reasonable energy consumption. Nevertheless, real-time performance must still be achieved on these resource-constrained platforms. Besides computational concerns, real-time planning in dynamic scenes is explicitly identified as an unresolved challenge in vision-language(-action) discussions, while recent work also points to the possibility of smaller models enabling real-time inference in constrained settings [34, 35]. As a result, real-time performance emerges as an implication spanning the full system: industrial robots must perceive, decide, communicate, and act within tight latency bounds despite environmental complexity and limited compute budgets [119, 130]. 

#### **_Implication 7: Cost-Effectiveness_ &** **_Integration Capabilities_** 

A recurring industrial framing is that automation must be economically justified, including for low-volume production and for SMEs. Authors argue that solutions must reduce manual effort, errors, and operational costs, and that high system cost remains a barrier to wider adoption of advanced autonomy [108, 116, 124]. Multiple works explicitly discuss that frequent product changes increase reprogramming effort and costs, motivating approaches that reduce commissioning overhead and ease reconfiguration [88, 96]. Beyond acquisition cost, Triantafyllou et al. [120] stress integration as a practical obstacle: deploying state-of-the-art research components in industrial systems requires coherent integration methodologies, yet community-wide standards and guidelines are described as lacking. This concern is also reflected in specific domains such as AGVs/AMRs, where robust integration into factory architectures is highlighted as necessary for smart manufacturing success [131]. Further, authors link industrial adoption to scalability and cost-effectiveness of intelligent control, as well as to the ability to operate with cost-sensitive hardware and sensing configurations [132, 133], aligning with our observation that an efficient deployment of control methods on low-power edge 

devices is a necessity, as modern high-tier GPUs can consume more than twice the power of a median cobot itself (cf. Section 6.3). Hence, costeffectiveness and integration capabilities emerge as an implication: industrial solutions must be economically viable and practically integrable into existing production environments, including under heterogeneous, resource-limited hardware and organisational constraints [35, 68, 132]. 

#### **_Implication 8: Explainability_ &** **_Trust_** 

Authors repeatedly link the adoption of AIdriven robotics to transparency, interpretability, and operator trust – particularly in settings where failures have severe consequences. Alt et al. [134] argue that explainability mechanisms, together with suitable user interfaces for presenting explanations, are key enablers for practical uptake of AI in industry. For safety- and risk-sensitive deployments, the limited adoption of perception models is explicitly attributed to the difficulty of understanding and trusting model outputs under potential failure consequences, motivating explainable approaches beyond simple classification settings [102]. Trust is also discussed as a determinant of acceptance in collaborative work, with concerns that fear of failure can reduce productivity and that appropriate trust levels are important success factors [58, 103, 125]. Related literature additionally emphasises psychological and ergonomic aspects – operators should feel comfortable and safe, and interfaces should provide visibility into system status and feedback about actions and responses [106, 112]. Empirical observations further suggest that limitations in sensing and flexibility can negatively affect perceived safety and trust in industrial collaboration [116]. Therefore, explainability and trust form an implication: industrial systems are expected not only to perform well, but also to provide comprehensible accounts of their behaviour and status to support acceptance, oversight, and safe collaboration [117, 134]. 

#### **_Implication 9: Sensor Fusion_ &** **_Perception_** 

Authors frequently describe perception as a central capability limiting automation scope, particularly in shared industrial workspaces and variable environments. Seleem et al. [52] explicitly state that no single sensing modality is sufficient to handle varying complex situations in real time, 

23 

motivating multi-modal sensing and fusion. This includes combining internal and external sensors for detecting humans and obstacles [52, 131] and using complementary sensing such as vision and tactile feedback to extend perception and improve safe collaboration [92, 107]. The corpus further connects sensor fusion to robustness: occlusions, dust, lighting variation, and sensor degradation can impair single-sensor solutions, and multiple works describe fusion or multi-sensor setups as mitigation strategies [105, 135]. At the same time, perception is framed as a prerequisite for real-time HRC, requiring holistic scene understanding that includes object recognition, environment parsing, and human recognition [93, 107]. Authors also highlight that advanced industrial tasks often require customised toolings and additional sensors, implying that control systems must accommodate heterogeneous and evolving observation spaces [69, 136]. Hence, when implemented on cobots, industry requires control methods that can accommodate the diverse and dynamic modalities arising from the sensor configurations commonly used in conjunction with cobots (cf. Section 6.2). Consequently, sensor fusion and perception emerge as an implication: industrial deployment demands multi-modal, robust perception pipelines that can support safe, reliable operation and collaboration under real-world sensing limitations [36, 99]. 

#### **_Implication 10: Standardised Benchmarking_ &** **_Evaluation_** 

Multiple works emphasise the need for replicable, standardised performance assessment to support adoption and comparability across systems. For example, standard test methods are described as necessary so that reported measurements can be reproduced with limited cost and effort [131]. At the same time, Yang et al. [42] identify a lack of unified standards and metrics for complex, component-rich industrial robotic systems, which complicates evaluation and hampers dissemination. Further, Sarathkumar et al. [129] argue more generally for benchmark and protocol development for intelligent control algorithms, including best practices that improve interoperability and reliability. In manufacturing-focused discussions, there is an explicit expectation for training and evaluation systems that can replay manufacturing tasks precisely and provide suitable interfaces, 

reflecting dissatisfaction with benchmarks that do not reflect industrial task realities [94]. Complementary perspectives highlight the role of virtualisation and digital twins as an enabler for testing and monitoring industrial systems [68, 104]. In addition, in our own prior work we argue for using multiple, distinct benchmarks to better characterise generalisation and distribution shifts rather than relying on a single testbed [137]. Overall, the literature motivates standardised benchmarking and evaluation as an implication: credible industrial adoption requires reproducible assessments that meaningfully reflect industrial tasks, conditions, and system complexity [94, 129]. 

#### **_Implication 11: Data Requirements_ &** **_Usage_** 

Finally, a consistent theme is that industrial robotics is data-constrained and that learningbased methods must address both data scarcity and deployment gaps. Several works explicitly note limited labelled data in industrial domains and the difficulty of building representative datasets [115, 133]. Related observations include that small datasets limit the strength of conclusions for specialised industrial use cases, underscoring how narrow and expensive data collection can be in practice [102]. In parallel, authors caution that many advanced approaches demand large volumes of training data and substantial computational resources, which can be misaligned with agile manufacturing contexts [91, 129]. Calder´on-cordova et al. [100] also discuss the importance of bridging simulated and realworld conditions, noting limitations of simulation fidelity and the resulting transfer gap for visionbased inputs. Digital-twin perspectives reinforce that data infrastructure is foundational for industrial modelling and services [87]. For future embodied intelligence and mass personalisation, Ren et al. [36] argue for continuous adaptation over time, enabled by automatic data collection and continual learning. In the specific context of vision-language(-action) approaches, the literature highlights the need for large-scale multimodal data and sim-to-real adaptation strategies to improve transfer and robustness, alongside calls to reduce data and compute requirements for industrial deployment [34, 35]. Finally, dataefficient methods, such as few-shot learning, are explicitly motivated as a practical necessity in 

24 

industrial settings [138]. Thus, data requirements and usage form a distinct implication: industrially relevant learning-based robotics must contend with limited, costly, and heterogeneous data while supporting transfer and adaptation under realistic deployment gaps [34, 100, 133, 138]. 

**_Synthesis_ &** **_relevance for industrial assessment of RFMs_** 

In summary, the implication corpus does not merely enumerate desirable properties, rather it repeatedly frames them as adoption bottlenecks and as reasons why laboratory-grade learningbased approaches often fail to translate into production environments [91, 94, 116]. The eleven proposed implications above therefore serve as the organising structure for the remainder of this section: they are used to discuss which attributes are required for RFMs to be credible candidates for industrial deployment (Section 7.2), and motivate a later, explicit assessment framework for industrial readiness that is grounded in the recurring requirements identified in the reviewed literature (Section 7.3). 

### **7.2 Attributes of Industry-Grade RFMs** 

To operationalise the eleven industrial implications from Section 7.1 for the RFM paradigm, we performed a second synthesis step that translates the largely qualitative, application-facing observations of the implication corpus into a structured set of _model- and deployment-relevant viewpoints_ . The motivation for this step is that the implications themselves describe _what_ industry expects (e.g. safe collaboration, robustness under uncertainty, or real-time feasibility), but do not yet specify _where_ in an RFM-based system such expectations could manifest. 

We therefore analysed each implication individually through a set of derived attributes that capture the principal degrees of freedom of industrial RFM deployment. This attribute set was designed to be sufficiently broad to cover both implications regarding embodied-operation (e.g. hardware, sensing, actions) and organisation (e.g. documentation, compliance), while remaining granular enough to express typical failure modes and deployment bottlenecks discussed across the industrial robotics literature (Section 7.1). 

In total, we consolidated 47 attributes as shown in Table 7. Using these attributes, we conducted an iterative mapping procedure in which we revisited each of the eleven implications and asked, for each attribute, what the implication would demand from an RFM-based robotic system when that system is viewed through the lens of the respective attribute. This yields 11 _×_ 47 = 517 implication-attribute combinations, forming a conceptual matrix in which each cell captures the relevant industrial concerns and constraints for that attribute under the given implication, and their specific interpretation in terms of RFM development and deployment. 

This matrix-based perspective is particularly important because the implications are interdependent: for industrial deployments, safety is not separable from perception, and real-time feasibility is not separable from interaction or robustness. Similarly, issues such as authorisation, adversarial robustness, and fault handling naturally span multiple implications (e.g. safety, robustness, trust, and integration). By enforcing a systematic traversal across all implication-attribute pairs, we aimed to reduce the risk of under-representing industrial requirements that might otherwise be subsumed under a single headline implication. 

The primary outcome of this step is a consolidated, implication-grounded view of what it would mean for RFMs to be _industry-grade_ . Rather than proposing a single, monolithic list of requirements, the attribute set enables a structured discussion of how industrial expectations manifest at different layers – ranging from sensing and action interfaces, over adaptation behaviour, to governance-related aspects such as compliance and documentation. 

At the same time, the full matrix is too extensive to be reproduced verbatim in this work without disproportionate volume. We therefore use the attribute set as a compact, transparent intermediate representation: it makes explicit which viewpoints were considered during the synthesis of the proposed criteria catalogue (Section 7.3), and it provides traceable coverage of the industrial concerns extracted from the implication corpus (Section 7.1). In the succeeding subsection, these structured considerations are subsequently distilled into an explicit assessment framework for industrial readiness, enabling a consistent evaluation of existing RFMs against the industrial 

25 

**Table 7:** Consolidated list of the 47 attributes considered for each implication. 

|**(1)** Hardware|**(13)** Security|**(25)** Actions/ Outputs|**(37)** Precision & Accuracy|
|---|---|---|---|
|**(2)** Tasks|**(14)** Detection, Recognition &<br>Understanding|**(26)** Skills|**(38)** Trust|
|**(3)** Environment|**(15)** Multimodal Inputs/<br>Outputs|**(27)** Observation/ Input|**(39)** Goal Specification &<br>Interpretation|
|**(4)** Objects/ Materials|**(16)** Integration|**(28)** External Influences/<br>Disturbances|**(40)** Solution Strategy|
|**(5)** Instructability/<br>Commanding|**(17)** Safety|**(29)** Reaction|**(41)** Offline Adaptation<br>(Finetuning/ Retraining)|
|**(6)** Distractors/ Distractions|**(18)** Compliance|**(30)** Validation/ Benchmark/<br>Evaluation|**(42)** Energy|
|**(7)** Adaptability/<br>Generalisation/ Flexibility|**(19)** Supervision|**(31)** Realtime Performance &<br>Inference Frequency|**(43)** Data|
|**(8)** Online Adaptation/<br>Learning|**(20)** Fault Tolerance &<br>Recovery/ Safeguards|**(32)** Noise|**(44)** Documentation/<br>Open-Source|
|**(9)** Internal Interfaces/<br>Representations|**(21)** Reasoning/ Intention|**(33)** Autonomy|**(45)** (Self-)Awareness/<br>Assessment & Monitoring|
|**(10)** ID/ OOD Robustness|**(22)** Model Feedback to User|**(34)** Consistency & Stability|**(46)** Memory|
|**(11)** Adversarial Robustness|**(23)** External Guidance/<br>Correction to Model|**(35)** Explainability/ Insights|**(47)** Anomaly/ Fault/ Error<br>Detection & Recognition|
|**(12)** Authorisation|**(24)** Interaction/<br>Collaboration|**(36)** Repeatability||


expectations highlighted throughout the literature. 

### **7.3 Evaluating Industrial Maturity: A Criteria Catalogue** 

The eleven implications in Section 7.1 describe _what_ industrial settings recurrently demand from deployed robotic systems. However, for RFMs, these expectations must be made concrete at the level of model capabilities, interfaces, and the surrounding deployment stack. Building on the 517 implication-attribute combinations from Section 7.2, we therefore translated the implication-grounded requirements into an explicit criteria catalogue that can be used to reason about, compare, and ultimately rate the industrial readiness of existing and future RFMs. For each implication-attribute combination, we collected and refined the key questions that an industrial deployment would have to answer (e.g. what happens under distribution shifts, how failures are detected and handled, how human input is interpreted and verified, and which artefacts are required for audit and integration). We iteratively consolidated these questions into a **catalogue of 149 criteria (C) – shown in the Appendix, Table C4 –** spanning all eleven general industrial implications (I). While comprehensive, we do not 

consider this catalogue final: it is intended as a living foundation that can be extended as additional industrial constraints or regulatory expectations emerge. 

#### **_Criteria scope: RFMs_ &** **_their deployment ecosystem_** 

Although most criteria target RFMs directly, industrial readiness is not determined by the model alone. Industrial deployments require an ecosystem – robot software stack, interfaces, safety infrastructure, monitoring, logging, and documentation – that must satisfy similar constraints. Consequently, the catalogue includes criteria that (a) are primarily RFM-centric (e.g. adaptive behaviour under changing observations/actions), (b) are primarily ecosystem-centric (e.g. the presence and maintenance of accessible documentation on training data composition and transfer behaviour), or (c) require joint support by model and ecosystem (e.g. a model producing structured signals that can be persistently logged and leveraged by the surrounding system). 

#### **_Intentional redundancy across implications_** 

Because the industrial implications are interdependent (cf. Section 7.2), certain criteria 

26 

re-appear _deliberately_ across different implications, albeit with different emphasis. We therefore avoided merging superficially similar criteria across implications when doing so would remove an aspect that is essential for assessing maturity with respect to a particular implication. For example, hot-swapping appears under adaptability (I1-C2), integration/cost (I7-C4), and perception (I9-C12), but each instance stresses a different industrial concern: autonomous adjustment of observation/action spaces, recognition and handling of various interface changes during commissioning, or modularity of the observation space alone and its documentation. Retaining these criteria within their respective implications preserves the ability to diagnose _why_ an RFM is immature in a specific industrial dimension rather than merely concluding that it ”lacks hot-swapping support”. 

#### **_Key paradigms reflected in the catalogue_** 

Many of the catalogue’s central motifs are rarely discussed _jointly_ in prior work and often not yet implemented in current RFMs, however, most are already being investigated as distinct research directions scattered across the RFM, VLA/LLM or general robotics control landscapes. We therefore use the following paradigms as _anchor points_ to illustrate that a substantial subset of the catalogue’s requirements is directly supported by emerging literature, and that our contribution lies in consolidating these partially disconnected strands and enriching them from an industrial viewpoint to craft a single, implication-grounded assessment framework. 

Central to criteria on multi-hardware support, hot-swapping, and dimensionality adaptation is the treatment of changing observation and action interfaces. Recent work has begun to explicitly adapt VLAs to new embodiments by learning unified action representations and steering pretrained policies towards platform-specific action distributions during downstream adaptation [139] or by enabling architectures to handle differing sized action and observation spaces [140]. These approaches align closely with our emphasis that industrial deployment requires transfer across morphologies, whereas a natural extension emerges in runtime resilience to interface changes and sensor/actuator substitutions. 

Changing action- and observation spaces naturally motivate concerns about handling OOD scenarios. Challenging industrial environments are indeed characterised by disturbances, clutter, and changes that are not exhaustively covered during training, requiring robustness against distribution shifts, anomalies, and deliberate manipulation. Accordingly, our catalogue places repeated emphasis on online detection, confidence signalling, and fallback behaviour. Complementary to this, emerging evidence suggests that current VLA systems may inherit security weaknesses known from LLMs and VLMs, amplifying their consequences. Both textual attacks that can persist over long horizons and vision-side attacks (e.g. through disrupting patch exposure) have been shown to substantially degrade performance or even obtain absolute control authority of VLAs, highlighting that adversarial robustness cannot be treated as an optional add-on for physically embodied systems. [141, 142] In parallel, anomaly prediction has been explored as a proactive mechanism, for instance by forecasting action outcomes and anticipating whether they lead to anomalous states [143]. This combination motivates why our catalogue repeatedly requires threat/attack detection, anomaly handling, and explicit recovery pathways: in industrial settings, models must differentiate between benign novelty and adversarial or safety-critical deviations. 

These mechanisms also depend on the system’s ability to quantify and communicate uncertainty in a usable manner. We therefore include multiple confidence-related criteria (spanning operational readiness, safety margin, real-time compliance, perceptual certainty, and velocity/ precision & accuracy (v/P&A) fulfilment), reflecting the view that trust requires calibrated estimates rather than raw success rates. This is supported by work that explore confidence calibration in VLAs for uncertainty quantification [144], as well as methods that align uncertainty to trigger helpseeking behaviour with statistical guarantees for LLM-based planning settings [145]. Such capabilities enable explicit halting, logging, clarification requests, or escalation to supervisors when the system’s own predicted reliability degrades. Confidence also naturally links to interactive clarification and feedback, repeatedly mentioned in our catalogue, which are essential for industrial 

27 

HRI/HRC where instructions can be ambiguous, incomplete, or safety-constrained. Recent approaches explicitly reason about linguistic ambiguity grounded in the scene and generate targeted follow-up questions, thereby reducing downstream execution failures caused by NL command-misinterpretation [146]. Conversely, other works demonstrate that NL can serve as an intuitive channel for fine-grained trajectory modification and incremental corrections, suggesting practical routes towards mid-execution trajectory adjustability and operator-in-the-loop refinement as demanded by several criteria [147, 148]. More broadly, collaboration frameworks that incorporate expert interventions during deployment indicate that interactive supervision can simultaneously improve immediate reliability and collect data for future refinement [143, 149]. 

A further recurring motif within our catalogue is the need for explicit supervisory or verification layers that monitor execution quality and safety independently of the core policy. This direction is reflected by Zhou et al. [150] that leverage VLMs for reactive and proactive failure detection, and methods designed for general failure detection across multiple tasks rather than narrow, task-specific detectors [151], which is essential for task-agnostic policies. Related efforts target the gap between semantic failure understanding and actionable correction by explicitly bridging high-level reflection and low-level action adjustment [152]. Such results substantiate the repeated insistence on decoupled safety gating, redundant safety mechanisms, fault categorisation, and explainable recovery behaviour: industrial assurance typically requires independent checks, predictable intervention pathways, and evidence of consistent handling across task variation. Finally, several works reinforce why the catalogue treats memory, data governance, and documentation as recurring concerns. Methods that add lightweight memory modules to VLAs highlight that exploiting historical context can materially improve long-horizon performance [153], while other frameworks explicitly summarise prior experience to support failure reasoning and replanning [154]. At the same time, privacy-preserving training mechanisms for VLAs [155] imply that industrial adoption may be constrained by data protection requirements, not by model capability alone. In addition, dataset construction efforts 

that deliberately incorporate failures and recoveries imply that training data must cover various edge- or failure-cases to enable robust deployment behaviour [156]. These developments collectively support the inclusion of criteria on persistent logging, memory mechanisms, data composition variation and transparency, privacy compliance, and learning from faults and incidents. Taken together, these strands illustrate that many catalogue requirements correspond to active research directions – the industrial immaturity is less the absence of isolated technical proposals than the lack of their systematic combination into a deployable, auditable, and safety-governed RFM ecosystem. The criteria catalogue therefore consolidates these partially disconnected lines into a unified framework that is directly grounded in the implication corpus and tailored to the operational constraints of industrial deployment, serving as a structured bridge between industrial expectations and RFM assessment: it translates the implication-level requirements into concrete items that can be used to analyse where current RFMs are industrial mature, where they are incomplete, and which research directions are likely necessary for credible industrial uptake. In the survey section that follows, we use this framework as a reference lens to discuss existing RFMs and to highlight gaps between current capabilities and the implication-derived expectations. 

## **8 RFM Overview & Evaluation** 

This section provides a structured overview of the current landscape of manipulation-capable RFMs and assesses their industrial readiness using the implication-grounded criteria catalogue introduced in Section 7.3. For transparency and overview, we report the full corpus of all 324 surveyed models in the Appendix (Table D5). We evaluate each model against the 149 catalogue criteria, enabling both an overall maturity score per paper and implication-wise maturity profiles. We describe the resulting evaluation methodology and procedure in Section 8.1, including the design decisions required to scale the assessment to the full corpus, corresponding to 324×149=48,276 criterion-level decisions. 

We additionally report an agreement and consistency check of our evaluation pipeline against 

28 

expert judgements on a small ground-truth subset in Section 8.1. Finally, we summarise the strongest-performing RFMs (Section 8.2) and provide a broader industrial applicability analysis over the full corpus and the Top-50 subset (Section 8.3). The combination of those results is used to characterise the current industrial maturity of RFMs, highlight which industrial implications are most and least addressed, and finally provide an evidence-based baseline for the synthesis and outlook in Section 9. 

### **8.1 Evaluation Procedure** 

To assess industrial readiness across the manipulation-capable RFM landscape, we evaluated all 324 manipulation-focused or generalist RFMs contained in the models sub-corpus of our main RFM-related corpus (out of 341 total model publications; cf. Section 3.2). Each paper was assessed against the 149 criteria of our implication-grounded catalogue (cf. Section 7.3, = Appendix D5), yielding 324 _×_ 149 48 _,_ 276 criterion-level decisions. A fully manual expert annotation of this scale is infeasible within a fixed time frame and would furthermore restrict the analysis to a small, subjectively filtered subset, limiting the validity of corpus-level conclusions. We therefore adopted an automated, LLM-based evaluation pipeline to (a) enable a completecorpus assessment, (b) reduce reviewer-dependent variability via a fixed and mostly repeatable procedure, and (c) obtain both a global maturity score per paper (fraction of fulfilled criteria) and implication-wise maturity profiles (fraction of fulfilled criteria per implication). 

Our evaluation was implemented as an objective, structured pipeline that leverages an LLM (GPT-5.1 in our case) to extract evidence from the full text of a paper and to decide whether a single criterion is fulfilled by the proposed model and/or its deployment ecosystem (as defined by the criterion; cf. Section 7.3). A key design goal was to minimise cross-contamination between papers and between criteria. Accordingly, each _single_ evaluation run was performed under two strict isolation constraints: (a) the LLM received exactly one criterion at a time (and was not informed about any other criteria), and (b) the retrieval context contained exactly one paper (including figures), provided through a dedicated 

vector store that was created for that evaluation run only. After the decision for that criterionpaper pair, the vector store was deleted, the session was closed, and the next criterion-paper pair was evaluated in a fresh run. This enforced independence across the 48 _,_ 276 evaluations and prevented leakage of information or implicit calibration across different models or criteria. Importantly, **all papers were processed using private, Siemens-internal infrastructure** . In particular, no papers were uploaded to public servers, and the evaluation was executed on private systems where the processed documents are not used for any training/ learning. This ensured that the large-scale assessment did not create any disclosure or copyright-related risks. 

For every paper-criterion pair, the LLM was required to produce a structured output with the following fields: a binary judgement of criterion fulfilment, a flag indicating whether the property was directly stated, a confidence score in the range [0 _,_ 1] indicating explicitness and evidence strength, a boolean evidence-availability signal, textual extracted quotes (or an explicit statement that no relevant information was found), and a brief rationale connecting evidence to the decision. Importantly, we instructed the LLM to decide conservatively: if a criterion was not supported clearly and in-scope by the paper, it was to be marked as _not_ fulfilled. This makes the resulting maturity estimates intentionally cautious, particularly for criteria that are only partially addressed, or for capabilities that are not sufficiently documented in the publication. The complete corpus run required over 5 days under rate limits, further underscoring why a purely manual evaluation is practically unattainable at this scale. 

#### **_Expert Agreement Comparison_** 

Because the pipeline is used to draw corpuslevel conclusions, we evaluated its reliability against expert judgements on a small groundtruth subset. Specifically, we created three blind expert-rated catalogue evaluations: two models were annotated by an expert prior to running the automated pipeline, and one additional model was annotated after the automated run had completed (the best-scoring model according to the LLM results). These three papers serve as a check on whether the procedure generates results with 

29 

sufficient accuracy to draw corpus-level conclusions. Table 8 shows absolute values, specifying how many criteria per paper-implication pair have been marked as fulfilled by expert and LLM. The table reveals that the LLM-based procedure closely reproduces the implication-level patterns of the expert assessments for these representative cases. In particular, the qualitative conclusion is preserved across all three models: Gemini Robotics 1.5 [157] attains substantially higher industrial maturity than OpenVLA [18], while _π_ 0 [26] remains limited across most implications. Across the three expert-annotated papers, Table 9 reports strong criterion-level agreement ( _N_ = 447): the LLM reaches an accuracy of 0 _._ 966 and an _F_ 1 score of 0 _._ 762 for the positive (fulfilled) class, with substantial agreement beyond chance (Cohen’s _κ_ = 0 _._ 744). Crucially for the maturity estimator, the false-positive rate is low ( _FPR_ = 1 _._ 9%), indicating that the LLM rarely over-attributes industrial capabilities that the expert does not confirm. The false-negative rate is higher ( _FNR_ = 22 _._ 6%), consistent with our conservative decision policy. Consequently, the derived maturity values should be interpreted as a cautious, lower-bound estimate rather than an optimistic readiness score. Restricting the analysis to those cases where the LLM reports information found as _true_ , (Table 9, _InfoFound_ ) does not increase the _F_ 1 score and slightly reduces _κ_ . This supports our intention that the information-found flag primarily captures evidence availability in the text, rather than serving as a reliable filter for correctness. 

At the per-paper level (Table 10), agreement between expert and LLM is high for both Gemini Robotics 1.5 and OpenVLA, especially supported by strong _κ_ and _J_<sup>+</sup> (Jaccard similarity for fulfilled cases). For _π_ 0, the expert positive rate at only 2 _._ 7% is notably low, with the corresponding _F_ 1, _κ_ and _J_<sup>+</sup> substantially lower than for the other two papers. This underlines that even a small number of disagreements can dominate positive-class metrics when positives are rare, however, also explains the higher false negative rates reported in Table 9. Therefore, per-paper metrics should be read with care in _very_ lowpositivity cases. 

Nevertheless, lower agreement cases as reported for _π_ 0 do not necessarily reflect substantial judgment errors, rather often report interpretation 

differences: e.g. Black et al. [26] include a brief evaluation of language-following capabilities and report an increased task success rate when providing intermediate language commands to the policy. The expert acknowledged this as sufficient for I1-C11 (”Mid-Execution Feedback Responsiveness”), whereas the LLM argued that only an increase in success rate does not necessarily imply the requested ability of course corrections. In fact, we observed a few patterns within our criteria that may inflate reported disagreement, while not necessarily introducing hard errors. As stated for the above example, some criteria may leave some room for interpretation, even among experts: regarding the ”Low-Data Adaptation & Few-Shot Requirements” criterion (I11-C1), OpenVLA reports requiring on average 10-150 episodes for downstream task adaptation [18] – the LLM interpreted this as few-shot and marked the criterion fulfilled, whereas our expert judgement considered up to 150 episodes too demanding for an industrial-ready ”low-data adaptation” interpretation. This implies that some criteria may need stricter boundaries to ensure higher evaluator agreement. In contrast, other criteria are inherently stringent (e.g. formulations that imply guarantees such as ”always”), which leads the LLM to often mark such criteria as not fulfilled, even when the capability is basically implemented, but the paper does not state a near 100% guarantee of adherence. Taken together, the agreement comparison indicates that the proposed pipeline provides sufficiently reliable, conservative estimates for our goal of scaling industrial maturity assessment to hundreds of RFMs. The low over-claiming rate supports its use for comparing models and identifying implication-level blind spots in the current state of the art, while the elevated miss rate and the interpretative latitude of some criteria motivate caution when analysing individual, fine-grained criterion outcomes. Accordingly, in the following, we treat criterion-level results as indicative and focus primarily on implication-level trends and cross-corpus patterns. 

### **8.2 Highest Rated RFMs** 

Across the 324 evaluated RFMs (cf. Table D5), the overall highest-rated models, as depicted in Table 11, reach total maturity scores of only 

30 

**Table 8:** Comparison between expert- and LLM-based evaluation results per implication for three representative RFMs. 

||Gemini Robotics 1.5 [157]|OpenVLA|[18]|_π_0|[26]|
|---|---|---|---|---|---|
|Implication|Expert<br>LLM|Expert|LLM|Expert|LLM|
|I1|9<br>8|3|4|1|1|
|I2|1<br>1|0|0|0|0|
|I3|1<br>1|0|0|0|0|
|I4|1<br>1|1|1|0|0|
|I5|0<br>0|0|0|0|0|
|I6|0<br>0|0|0|0|0|
|I7|0<br>0|0|0|0|0|
|I8|1<br>1|0|0|0|0|
|I9|1<br>2|0|0|1|0|
|I10|2<br>3|5|5|1|1|
|I11|2<br>1|0|1|1|1|
|�|18<br>18|9|11|4|3|


**Table 9:** LLM-expert agreement on criterion fulfillment. _Reporting the number of N evaluations considered, the overall Accuracy (Acy), F_ 1 _-score, Cohen’s kappa agreement (κ) and false positive/ negative rates (FPR/FNR)._ 

|Setting|_N_|Acy|F1|_κ_|FPR/FNR|
|---|---|---|---|---|---|
|All|447|0.966|0.762|0.744|1.9%/22.6%|
|InfoFound|304|0.951|0.762|0.734|2.9%/22.6%|


**Table 10:** Per-paper agreement. _Pos% reports the expert positive rate and J_<sup>+</sup> _the Jaccard similarity index, computed only for the positive class to ignore the dominating negatives._ 

|Paper|Pos%|Acy|F1|_κ_|_J_<sup>+</sup>|
|---|---|---|---|---|---|
|Gemini 1.5|[157] 0.121|0.960|0.833|0.810|0.714|
|OpenVLA|[18]<br>0.060|0.973|0.800|0.786|0.667|
|_π_0 [26]|0.027|0.966|0.286|0.269|0.167|


0 _._ 11 _−_ 0 _._ 12, i.e. they satisfy roughly one out of ten catalogue criteria on average. Although possibly lower-bound, this pronounced ceiling effect is informative in itself: even the strongest current approaches cover only a narrow subset of the industrial requirements captured by our 

implication-grounded framework, and thus no single model can yet be regarded as comprehensively industry-grade. 

A commonality among the five best models is that they do not merely present a monolithic visuomotor policy, but explicitly introduce and focus on single mechanisms that address failure modes and operational bottlenecks frequent to industrial settings: structured reasoning, human-in-the-loop guidance, self-correction, and improved perception/data utilisation. Accordingly, their maturity profiles exhibit pronounced peaks on a small number of implications while remaining low elsewhere (cf. Table 11 and Figure 10). This implies that recent RFM work seems to advance one or two enabling dimensions at a time, but do not yet integrate the broader industrial requirements captured by our catalogue. 

Specifically, Gemini Robotics 1.5 [157] achieves the highest total score (0 _._ 12) and the strongest value on adaptability/flexibility (I1: 0 _._ 44). A plausible reason for this scoring is that it combines two complementary components (Gemin Robotics 1.5 as a VLA, and Gemini Robotics 1.5-ER as a VLM), which can be combined to an agentic framework, rather than relying on a single controller in isolation. From an industrial perspective, this implies that near-future deployments may 

31 

**Table 11:** Overview of the five highest rated RFMs ( **total** ) of the 324 evaluated. _Reporting their proportional industrial applicability ratings for each individual implication, and a total score over all implications. Per-criterion ratings are created utilising the publication’s context, by leveraging our LLM-based pipeline as described in Section 8.1. Highest values within the five RFMs for each implication are shown in green, lowest in red. Values are rounded to two decimal places._ 

|**Ref**|**Model**|**Total**_↓_|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[157]|Gemini<br>Robotics<br>1.5|0.12|0.44|0.06|0.07|0.07|0.00|0.00|0.00|0.07|0.14|0.23|0.09|
|[158]|Collab<br>VLA|0.11|0.28|0.00|0.20|0.07|0.08|0.11|0.00|0.07|0.21|0.08|0.09|
|[159]|GF-<br>VLA|0.11|0.28|0.00|0.00|0.14|0.08|0.00|0.00|0.07|0.14|0.23|0.27|
|[6]|OneTwo<br>VLA|0.11|0.33|0.00|0.20|0.14|0.00|0.11|0.10|0.07|0.14|0.00|0.09|
|[160]|SC-<br>VLA|0.11|0.33|0.06|0.00|0.21|0.23|0.11|0.00|0.00|0.00|0.15|0.09|


**Fig. 10** : Proportional implication fulfillment. _Depicting the five overall highest-rated RFMs (see Table 11 for detailed values)._ 

demand layered systems where high-level reasoning, verification, and interaction are distinct from low-level action generation. As Gemini’s leading score is not driven by uniformly higher values across all implications, it suggests that hybrid or multi-component designs may only be one part of the puzzle towards industrial maturity, primarily aiding flexibility. 

In general, we noticed a strong consistency in 

positive evaluator agreement across the 5 highest ranked RFMs: CollabVLA [158] attains the highest scores within this group for HRI/HRC (I3: 0 _._ 20) and sensor fusion/perception (I9: 0 _._ 21). Those implications highly correlate, since perception of human/ operator detection is a prerequisite for HRC (cf. Section 7.1). Importantly, this concentration directly matches the paper’s explicit objective of moving from a closed-loop visuomotor policy towards a collaborative agent by incorporating human guidance into action generation [158]. An equally strong agreement is obvious in data requirements and usage (I11: 0 _._ 27) for GF-VLA [159]. The authors focus on learning from human demonstrations aiming to improve generalisation beyond low-level trajectory imitation, framing the efficient utilisation of demonstration data as their main goal [159]. Similar to Gemini, OneTwoVLA [6] shows high flexibility (I1: 0 _._ 33) and also employs more than one component, however, explicitly distinguishes between a fast acting mode (System One) and a slower reasoning mode (System Two) and switches between them during execution [6]. SC-VLA [160]’s high values on robustness/reliability (I4: 0 _._ 21) and precision/accuracy (I5: 0 _._ 23) are equally well explained by the model’s main intention: Li et al. [160] integrate a fast action prediction with a slower reflection mechanism to correct failed actions for more robust manipulation. Such failure recovery could naturally translate to a more robust system. 

32 

**Table 12:** Overview of the highest rated RFMs **per implication** of the 324 total evaluated. _Per-criterion ratings are created utilising the publication’s context, by leveraging our LLM-based pipeline as described in Section 8.1. Highest values within the respective implication are highlighted in green. Values are rounded to two decimal places. The entry ”Multiple” represents the fact that several works have the similar highest score of 0.11 for I6, which are thus consolidated in one row._ 

|**Ref**|**Model**_↑_|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[158]|Collab<br>VLA|0.11|0.28|0.00|0.20|0.07|0.08|0.11|0.00|0.07|0.21|0.08|0.09|
|[161]|FuSe|0.05|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.21|0.00|0.27|
||Gemini|||||||||||||
|[157]|Robotics<br>1.5|0.12|0.44|0.06|0.07|0.07|0.00|0.00|0.00|0.07|0.14|0.23|0.09|
|[162]|GraphCoT<br>VLA|0.05|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.21|0.14|0.00|0.09|
|[163]|HAMSTER|0.07|0.11|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.07|0.23|0.36|
|[164]|HiBer<br>NAC|0.10|0.22|0.11|0.00|0.00|0.08|0.11|0.10|0.00|0.21|0.15|0.09|
|[165]|LCIL|0.07|0.11|0.00|0.27|0.00|0.00|0.11|0.00|0.00|0.00|0.08|0.18|
|[166]|NanoVLA|0.07|0.11|0.00|0.00|0.07|0.08|0.00|0.20|0.00|0.00|0.31|0.00|
|[18]|OpenVLA|0.07|0.22|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.38|0.09|
|[167]|PaLM-<br>E|0.09|0.33|0.00|0.00|0.29|0.00|0.00|0.00|0.00|0.07|0.00|0.18|
|[160]|SC-<br>VLA|0.11|0.33|0.06|0.00|0.21|0.23|0.11|0.00|0.00|0.00|0.15|0.09|
|[143]|Sirius-<br>Fleet|0.10|0.39|0.22|0.00|0.14|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[168]|Smol<br>VLA|0.04|0.06|0.00|0.00|0.07|0.00|0.00|0.20|0.00|0.00|0.15|0.00|
|[169]|UniVLA|0.07|0.11|0.00|0.00|0.00|0.08|0.00|0.00|0.07|0.00|0.23|0.36|
|–|_Multiple_|–|–|–|–|–|–|0.11|–|–|–|–|–|


Taken together, Table 11 and Table 12 illustrate a consistent trend: the strongest models predominantly optimise for one or two identified bottlenecks, and this intent is reflected by implication-specific peaks in the evaluation. However, even the best per-implication results remain limited in absolute terms: the highest proportional fulfilment observed across all implications is 0 _._ 44 by Gemini Robotics 1.5 on I1, and this is the only value over all evaluated RFMs to exceed 0 _._ 4 at all (cf. Table D5). This indicates that, while individual industrial concerns are beginning to be addressed, current RFMs do not yet attempt – nor achieve – integrated coverage across the full set of industrial implications. In the following 

subsection, we therefore move beyond the topranked models to provide a broader view of how industrial maturity is distributed across the full RFM landscape, and which implications remain systematically underrepresented. 

### **8.3 Industrial Applicability Overview** 

To provide a corpus-level perspective beyond the highest-ranked models (Section 8.2), we analysed the distribution of implication-wise fulfilment across all 324 evaluated RFMs (cf. Table D5) and the stronger Top-50 model subset, leveraging the total and per-implication industrial maturity scores. We report two complementary views: 

33 

(a) a brief temporal stability overview of which implications are addressed (Figure 11), and (b) breadth-versus-depth of coverage per implication for the full corpus and the Top-50 (Figure 12, with exact values in Table 13). Finally, we contextualise these trends by inspecting which individual criteria are most frequently fulfilled (Table 14) and by quantifying whether criteria are widely discussed yet rarely met (Table 15). 

#### **_Temporal Stability Overview_** 

Figure 11 shows the normalised, per-implication 

##### Yearly Criterion Fulfillment Ratio 


**Fig. 11** : Normalised per-implication criteria coverage. _Each value represents the sum over all criteria fulfilled within the given implication_ & _year, divided by the total number of papers published in the respective year._ 

criteria coverage aggregated by publication year. Across the years depicted, the overall profile is highly consistent: the same small subset of implications dominates the addressed space, while the remaining implications remain persistently low. In particular, the corpus repeatedly concentrates on adaptability/flexibility (I1), benchmarking/evaluation (I10), and data requirements/usage (I11), whereas safety/compliance (I2), HRI/HRC (I3), real-time performance (I6), and cost-effectiveness/integration (I7) remain comparatively underrepresented. The absence of 

a clear, monotonic rise in any single implication suggests that current RFM research is not (yet) converging towards progressively more holistic industrial coverage at the implication level – rather, the field appears to deepen within a relatively stable set of research emphases. 

#### **_Breadth vs. Depth Analysis_** 

A central question to our industrial applicability analysis is, whether the literature does not mention an implication at all, merely mentions it, or provides substantive, multi-criterion coverage. We therefore contrast two metrics per implication: (a) 1+-Coverage, the share of papers meeting at least one criterion, representing _breadth_ of implication considerations, and (b) Average Criteria Coverage (ACC), the average fraction of criteria met per paper, implying consideration _depth_ . The combined view of Figure 12 and Table 13, reveals a consistent breadth-depth mismatch across the current RFM landscape: While many papers touch a subset of implications, far fewer demonstrate multi-criterion, implementationrelevant coverage within those implications (note scale differences of Figure 12a and Figure 12b). Concretely, the **full corpus** exhibits strong breadth for only three implications: Adaptability/flexibility (I1: (1+=0 _._ 756)), benchmarking/evaluation (I10: (1+=0 _._ 753)), and data requirements/usage (I11: (1+=0 _._ 707)). Yet even for these leading implications, depth remains low: their ACC values stay below (0 _._ 10) (I10: (0 _._ 099), I11: (0 _._ 097), I1: (0 _._ 089)). This pattern indicates that on average, papers satisfy only a small fraction of the criteria within the implications they most frequently address. Additionally, several implications central to industrial deployment remain already weak at the 1+Criterion level – most notably safety/compliance (I2: (1+=0 _._ 034)), HRI/HRC (I3: (1+=0 _._ 052)), real-time performance (I6: (1+=0 _._ 049)), and costeffectiveness/integration (I7: (1+=0 _._ 071)). The persistently low coverage for these implications aligns with the temporal stability observation in Figure 11: the research field’s emphasis appears comparatively stable over time and does not show a clear shift towards holistic industrial requirement satisfaction at the implication level. Restricting attention to the **Top-50** models strengthens the same overall picture rather than changing it. Breadth becomes near-universal for 

34 


(a) 1+-Coverage over evaluated RFMs: _The metric specifies the percentage of works that meet at least one criterion for the respective implication (I) within the given (sub)corpus._ 

(b) ACC for evaluated RFMs: _ACC specifies the average percentage of criteria each paper meets for the respective implication (I) within the given (sub)corpus._ 

**Fig. 12** : Implication-specific evaluation coverage across the full set of 324 RFMs (Full Corpus) and the Top-50 subset. 

**Table 13:** Detailed comparison of 1+-Coverage and ACC between the full evaluated corpus (324) and the Top 50: _For visualisation, see Figure 12. Values are rounded to three decimal places._ 

|Metric|Corpus|I1|I2|I3|I4|I5|I6|I7|I8|I9|I10|I11|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1+|Full|0.756|0.034|0.052|0.172|0.167|0.049|0.071|0.219|0.213|0.753|0.707|
||Top 50|1.0|0.22|0.34|1.0|1.0|0.32|0.46|1.0|1.0|1.0|1.0|
|ACC|Full|0.089|0.003|0.007|0.016|0.014|0.005|0.008|0.017|0.019|0.099|0.097|
||Top 50|0.238|0.019|0.043|0.096|0.086|0.036|0.05|0.081|0.097|0.232|0.227|


seven implications (I1, I4, I5, I8, I9, I10, I11 all at (1+=1 _._ 0)), suggesting that higher-performing RFMs increasingly include at least some features, experiments, or claims related to these dimensions. However, the remaining implications still lag even in the Top-50 subset (I2: (0 _._ 22), I3: (0 _._ 34), I6: (0 _._ 32), I7: (0 _._ 46)). Depth improves substantially but remains far from comprehensive: the highest Top-50 ACC values are again concentrated in I1 (0 _._ 238), I10 (0 _._ 232), and I11 (0 _._ 227), whereas safety/compliance (I2: 0 _._ 019) and realtime performance (I6: 0 _._ 036) remain particularly low. Thus, even among the strongest papers, industrial maturity is characterised more by 

selective advances than by broad, high-coverage satisfaction across implications. 

Table 14 sharpens this conclusion by showing which capabilities are most frequently met. The ten most commonly fulfilled criteria cluster heavily in the same three implications that dominate in depth (I1, I10, I11). The top entries – MultiTask Generalisation (I1: 0 _._ 4938), Flexible Data Type Acceptance (I11: 0 _._ 4877), Repeatability & Reproducibility (I10: 0 _._ 4475), and Low-Data Adaptation & Few-Shot Requirements (I11: 0 _._ 4198) – indicate that the present RFM literature prioritises generality across tasks, flexible use of available (and heterogeneous) data, and 

35 

**Table 14:** Top 10 most frequently fulfilled **criteria** across all papers. _Reporting each criterion’s implication (I1-I11), absolute count and rate of fulfillment, explicitness among fulfilled cases (Expl(fulf)), evidence availability (Evid), and mean confidence when fulfilled (ConfFul). Values are rounded to four decimal places._ 

|**Criterion**|**Impl**|**Fulfilled**|**Rate**_↓_|**Expl(fulf)**|**Evid**|**ConfFul**|
|---|---|---|---|---|---|---|
|Multi-Task Generalisation|I1|160|0.4938|0.2812|0.9938|0.8605|
|Flexible Data Type Acceptance|I11|158|0.4877|0.3671|0.9907|0.8693|
|Repeatability & Reproducibility|I10|145|0.4475|0.2483|0.9815|0.8474|
|Low-Data Adaptation & Few-Shot<br>Requirements|I11|136|0.4198|0.8088|0.9907|0.9102|
|Module & Skill-Specific Benchmarking|I10|129|0.3981|0.0698|0.9938|0.8517|
|Generalisation to Environmental Variation|I1|101|0.3117|0.5446|0.9815|0.8739|
|Generalisation & Adaptation Assessment|I10|90|0.2778|0.1111|1.0000|0.8676|
|Autonomous Handling of<br>Distractors/Obstacles|I1|87|0.2685|0.5057|0.9568|0.8655|
|Performance Benchmarking & OOD<br>Feedback|I8|63|0.1944|0.2063|0.9877|0.8367|
|Online/Mid-Execution Adaptation|I1|49|0.1512|0.5306|0.9907|0.8771|


**Table 15:** Evidence-Fulfilled-Gap analysis: _Reporting the gap score gc alongside its evidence availability (EvidRate) and full-corpus fulfillment rate (FulfillRate) for each implication’s criterion with the highest evidence rate. Values are rounded to four decimal places._ 

|**Impl** _↑_|**Criterion**|_gc_|**EvidRate**_↓_|**FulfillRate**|
|---|---|---|---|---|
|I1|Multi-Task Generalisation|0.5000|0.9938|0.4938|
|I2|Reactive, Real-Time Safety|0.8086|0.8117|0.0031|
|I3|Collaborative Adaptation|0.8735|0.8981|0.0247|
|I4|Environmental Robustness & Adaptation|0.9475|0.9907|0.0432|
|I5|Consistency Over Time & Contexts|0.8796|0.9969|0.1173|
|I6|Goal-Responsive Solution Strategies|0.9352|0.9722|0.0370|
|I7|Flexible Input/Output Adaptation|0.9815|0.9815|0.0000|
|I8|Performance Benchmarking & OOD Feedback|0.7932|0.9877|0.1944|
|I9|Multimodal Sensor Acceptance & Fusion|0.9660|1.0000|0.0340|
|I10|Generalisation & Adaptation Assessment|0.7222|1.0000|0.2778|
|I11|Low-Data Adaptation & Few-Shot Requirements|0.5710|0.9907|0.4198|


benchmark-driven reporting. At the same time, the explicitness values for several of these frequently fulfilled criteria are relatively low: e.g. Multi-Task Generalisation (0 _._ 2812) and Repeatability & Reproducibility (0 _._ 2483), suggesting that fulfilment is often inferred from experimental set-ups or evaluation sections rather than being framed as a directly stated requirement. The comparatively high explicitness for Low-Data Adaptation (0 _._ 8088) is consistent with this topic 

being frequently highlighted explicitly as a contribution, though – as discussed in Section 8.1 – the interpretation latitude of this criterion may also inflate fulfilment rates. In general, however, the most fulfilled criteria support what we would expect of RFMs: systems adaptive to multiple tasks that can digest various forms of data for behaviour modulation. 

Finally, Table 15 indicates that many criteria are discussed in the current literature, however, 

36 

most seem to be not, or only partially fulfilled. The gap score _gc_ (EvidRate _c −_ FulfillRate _c_ ) is large for the top-evidence criterion in almost every implication, frequently exceeding (0 _._ 8). As EvidRate reflects the rate of evidence found in the given texts, these large gaps imply that many criteria-relevant aspects are widely mentioned or at least documentable, yet rarely satisfied under the (binary, conservative) fulfilment policy of our evaluation. In combination with the low ACC values in Table 13, this points to a broader tendency: the corpus increasingly acknowledges industrial constraints and desiderata, but typical papers still implement or document only limited, criterion-incomplete solutions – particularly for implications tied to deployment integration (I7), safety/ compliance (I2), real-time performance (I6), and HRC/HRI (I3). 

## **9 Summary & Discussion** 

Industrial robotics is undergoing a discernible transition from isolated, highly optimised automation towards flexible, collaborative deployment paradigms in which humans and robots share workspaces and responsibilities. A driver of this shift is the uptake of cobots, particularly in highmix, low-volume settings and in SMEs, where traditional automation is often economically or organisationally impractical due to commissioning effort, frequent production changes, and the need for specialised expertise (cf. Section 5). While modern cobots provide the hardware foundations for such a transition – safe physical design, appropriate payload and sizing, comparatively low operating power – they do not, by themselves, resolve the central bottleneck: robust, deployment-ready intelligence that can flexibly adapt behaviour to changing tasks, environments, and multimodal input without imposing prohibitive engineering overhead. 

Our synthesis therefore frames RFMs as a promising enabling technology for this industrial transformation, because they target precisely the dimensions in which classical control and even specialised learning-based approaches remain limited: multi-task competence, cross-domain generalisation, and instruction- or demonstration-driven/ low-effort reconfiguration (cf. Section 2). However, the same factors that make industrial cobot 

deployments attractive – shared workspaces, continuous operation, heterogeneous actuation/ sensing stacks and cost pressure – also amplify the demands on any learning-based control paradigm. In particular, typical cobots exhibit high mechanical precision and repeatability, moderate payload capability, and low median power draw in the widely deployed 0 _._ 5-20kg class (cf. Section 6.1). These characteristics imply that industrial value is frequently limited not by actuation quality but by perception and decision-making under real-world variability, and they simultaneously constrain RFM deployment to low-latency, energy-aware inference on industrial edge platforms rather than workstation-grade hardware (cf. Section 6.3). The practical prevalence of multi-sensor configurations, sensor fusion, and modular end-effectors further highlights that industrial intelligence must be interface-flexible: it must tolerate changing observation and action spaces that arise from tool changes, sensor substitutions, and integration into existing automation infrastructure (cf. Section 6.2). To capture these deployment realities systematically, we distilled eleven general interdependent implications (Section 7.1) from industrial literature and translated them into a structured assessment framework (Section 7.3). 

The key contribution of this step is not merely a list of desirable properties, but a traceable operationalisation: As foundation for our assessment framework, we started with 11 implications of what industry generally demands from robotic applications, extracted 47 deployment-relevant attributes to create an implication-attribute matrix of 11 _×_ 47 = 517 considerations, to finally retrieve an implication-grounded, assessable criteria catalogue of 149 concrete items spanning both model capabilities and ecosystem requirements (cf. Section 7). Our observations clearly show that raw success rates alone are not sufficient for industrial application. Rather, capability is inseparable from deployability: safety depends on perception and verification, real-time feasibility depends on compute constraints and system integration, and trust depends on observable and auditable behaviour rather than raw benchmark success. When applying this framework to the manipulation-capable RFM landscape, our evaluation results paint a consistent picture: the field is progressing rapidly, e.g. in research breadth, 

37 

yet remains at an early stage of industrial maturity (cf. Section 8). Across the 324 discovered and evaluated models and 48 _,_ 276 criterion-level decisions, even the top-ranked RFMs reach only 0 _._ 11-0 _._ 12 overall maturity – roughly one out of ten criteria met on average (cf. Section 8.2) and most models only score (comparably) high on a maximum of two to three varying implications. This implies that the primary limiting factor for industrial deployment is not the absence of isolated technical ideas, but the incomplete and non-systematic integration of those ideas into comprehensive, deployable RFM stacks. The frontier models further indicate how progress is currently realised. The five strongest systems exhibit implication-wise ”peaks” rather than balanced coverage, typically by introducing targeted mechanisms such as structured reasoning, human-in-the-loop interaction, self-correction, or improved data utilisation (cf. Section 8.2). Gemini Robotics 1 _._ 5, for example, leads overall and reaches the highest observed implication fulfilment on adaptability/flexibility (I1: 0 _._ 44), yet remains near zero on multiple deployment-critical implications, underscoring that hybrid or layered architectures may advance flexibility without automatically closing safety, integration, or realtime gaps. Similarly, models that score comparatively well in HRI/HRC and perception emphasise collaborative mechanisms and richer observation handling, but do not simultaneously satisfy the broader criteria spectrum required for sustained industrial operation. Taken together, the current RFM state of the art appears to advance by isolating and optimising individual bottlenecks, yet comprehensive ”industry-grade” integration, by contrast, remains largely unaddressed. This interpretation is reinforced when expanding evaluation to the full corpus. Over time, the implication profile remains strikingly stable: research consistently concentrates on adaptability/flexibility (I1), benchmarking/evaluation (I10), and data requirements/usage (I11), while safety/compliance (I2), HRI/HRC (I3), real-time performance (I6), and cost-effectiveness/integration (I7) remain persistently underrepresented (cf. Section 8.3). The breadth-depth analysis of our evaluation sharpens the same conclusion: In the full corpus, several implications are frequently ”touched”, yet few papers satisfy more than a small fraction of criteria within those implications. 

Even the Top-50 subset does not convert their breadth into comprehensive satisfaction: depth remains modest even for leading implications (I1/I10/I11), and many deployment-critical implications (I2/I3/I6/I7) remain relatively weak both in breadth and depth (cf. Section 8.3). Hence, current progress is better characterised as wider acknowledgement of industrial concerns than as demonstrable, multi-criterion completion of those concerns. 

These findings suggest several concrete priorities for future work towards industry-grade RFMs: First, the field must move from isolated capability demonstrations towards deployable, layered systems in which planning, memory, action generation, verification, and safety gating are treated as central, independently testable components – an architectural direction implicitly supported by high-performing models, yet not broadly matured across the corpus (cf. Section 8.2). Second, industrial adoption may require bridging the persistent underrepresentation of safety/compliance, real-time feasibility, and integration concerns by developing evaluation protocols and artefacts that connect RFM capabilities to operational constraints: low-latency inference on edge hardware, structured logging and monitoring, and explicit handling of changing sensor and tooling interfaces (cf. Sections 6.3 and 7.3). Third, the strong and stable emphasis on benchmarking (I10) should be leveraged to improve industrial relevance rather than to merely report success rates in a diversity of benchmarks: evaluations must reflect deployment realities such as distribution shifts, failure recovery, human supervision, and long-horizon operation, and must enable diagnosing why a model fails under industrial conditions rather than only whether it succeeds on curated tasks. Finally, the large evidence-fulfilment gaps (cf. Section 8.3) indicate an opportunity and a requirement: many industrial desiderata are already recognised by the research community, yet the step from recognition to robust implementation, documentation, and validation remains a dominant obstacle. In conclusion, RFMs constitute a credible technological pathway to unlock the full potential of cobot-centred automation: they directly target the flexibility, reconfigurability, and intuitive instructioning demanded by modern industrial 

38 

production, especially in cost- and changeoversensitive settings (cf. Section 5). Nevertheless, our corpus-scale evaluation demonstrates that current RFM research is still predominantly laboratoryoriented when measured against deploymentgrounded industrial requirements. The presented implication synthesis and criteria catalogue provide a transparent _industrial readiness_ reference that can be used both to evaluate future RFMs and to guide their design towards auditable, safe, real-time-capable and integration-ready systems. Closing the identified gaps – particularly in safety/compliance, HRI/HRC, real-time performance, and cost-effectiveness/integration capabilities – therefore represents the central research agenda for translating the rapidly advancing field of RFMs into reliable industrial autonomy. 

## **References** 

- [1] Chi, C., Feng, S., Du, Y., Xu, Z., Cousineau, E., Burchfiel, B., et al.: Diffusion Policy: Visuomotor Policy Learning via Action Diffusion (2023) https://doi.org/10.48550/ arXiv.2303.04137 

- [2] Liang, Z., Li, Y., Yang, T., Wu, C., Mao, S., Nian, T., et al.: Discrete Diffusion VLA: Bringing Discrete Diffusion to Action Decoding in Vision-Language-Action Policies. arXiv (2025). https://doi.org/10. 48550/arXiv.2508.20072 

- [3] Zhang, W., Liu, H., Qi, Z., Wang, Y., Yu, X., Zhang, J., et al.: DreamVLA: A Vision-Language-Action Model Dreamed with Comprehensive World Knowledge. arXiv (2025). https://doi.org/10.48550/arXiv.2507.04447 

- [4] Liang, J., Liu, R., Ozguroglu, E., Sudhakar, S., Dave, A., Tokmakov, P., et al.: Dreamitate: Real-World Visuomotor Policy Learning via Video Generation. arXiv (2024). https://doi.org/10.48550/arXiv.2406.16862 

- [5] Bu, Q., Li, H., Chen, L., Cai, J., Zeng, J., Cui, H., et al.: Towards Synergistic, Generalized, and Efficient Dual-System for Robotic Manipulation. arXiv (2025). https: //doi.org/10.48550/arXiv.2410.08001 

- [6] Lin, F., Nai, R., Hu, Y., You, J., Zhao, J., Gao, Y.: OneTwoVLA: A Unified VisionLanguage-Action Model with Adaptive Reasoning. arXiv (2025). https://doi.org/10. 48550/arXiv.2505.11917 

- [7] Chen, H., Liu, J., Gu, C., Liu, Z., Zhang, R., Li, X., et al.: Fast-in-Slow: A Dual-System Foundation Model Unifying Fast Manipulation within Slow Reasoning. arXiv (2025). https://doi.org/10.48550/arXiv.2506.01953 

- [8] Bommasani, R., Hudson, D.A., Adeli, E., Altman, R., Arora, S., Arx, S., et al.: On the Opportunities and Risks of Foundation Models. arXiv (2022). https://doi.org/10. 48550/arXiv.2108.07258 

- [9] Firoozi, R., Tucker, J., Tian, S., Majumdar, A., Sun, J., Liu, W., et al.: Foundation Models in Robotics: Applications, Challenges, and the Future. arXiv (2023). https://doi. org/10.48550/arXiv.2312.07843 

- [10] Yuan, Y.: On the Power of Foundation Models (2022) https://doi.org/10.48550/arXiv. 2211.16327 

- [11] Marsh, G.E.: THE DEMYSTIFICATION OF EMERGENT BEHAVIOR (2013) https: //doi.org/10.48550/arXiv.0907.1117 

- [12] Hu, Y., Xie, Q., Jain, V., Francis, J., Patrikar, J., Keetha, N., et al.: Toward General-Purpose Robots via Foundation Models: A Survey and MetaAnalysis. arXiv (2024). https://doi.org/10. 48550/arXiv.2312.08782 

- [13] Ma, Y., Song, Z., Zhuang, Y., Hao, J., King, I.: A Survey on Vision-Language-Action Models for Embodied AI. arXiv (2025). https://doi.org/10.48550/arXiv.2405.14093 

- [14] Xiang, T.-Y., Jin, A.-Q., Zhou, X.-H., Gui, M.-J., Xie, X.-L., Liu, S.-Q., et al.: Parallels Between VLA Model Post-Training and Human Motor Learning: Progress, Challenges, and Trends. arXiv (2025). https:// doi.org/10.48550/arXiv.2506.20966 

- [15] Zhou, H., Yao, X., Mees, O., Meng, Y., Xiao, 

39 

   - T., Bisk, Y., et al.: Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation. arXiv (2025). https:// doi.org/10.48550/arXiv.2312.10807 

- [16] Xu, C., Zhang, S., Liu, Y., Sun, B., Chen, W., Xu, B., et al.: An Anatomy of VisionLanguage-Action Models: From Modules to Milestones and Challenges. arXiv (2025). https://doi.org/10.48550/arXiv.2512.11362 

- [17] Zhong, Y., Bai, F., Cai, S., Huang, X., Chen, Z., Zhang, X., et al.: A Survey on VisionLanguage-Action Models: An Action Tokenization Perspective. arXiv (2025). https: //doi.org/10.48550/arXiv.2507.01925 

- [18] Kim, M.J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., et al.: OpenVLA: An Open-Source VisionLanguage-Action Model. arXiv (2024). https://doi.org/10.48550/arXiv.2406.09246 

- [19] Li, X., Liu, M., Zhang, H., Yu, C., Xu, J., Wu, H., et al.: Vision-Language Foundation Models as Effective Robot Imitators. arXiv (2024). https://doi.org/10. 48550/arXiv.2311.01378 

- [20] Amin, A., Aniceto, R., Balakrishna, A., Black, K., Conley, K., Connors, G., et al.: _π_ 0 _∗_ .6: A VLA That Learns From Experience (2025) https://doi.org/10. 48550/arXiv.2511.14759 

- [21] Xiao, W., Xue, H., Tao, T., Kalaria, D., Dolan, J.M., Shi, G.: AnyCar to Anywhere: Learning Universal Dynamics Model for Agile and Adaptive Mobility. arXiv (2024). https://doi.org/10.48550/arXiv.2409.15783 

- [22] Zhang, J., Li, A., Qi, Y., Li, M., Liu, J., Wang, S., et al.: Embodied Navigation Foundation Model. arXiv (2025). https:// doi.org/10.48550/arXiv.2509.12129 

- [23] Cheng, A.-C., Ji, Y., Yang, Z., Gongye, Z., Zou, X., Kautz, J., et al.: NaVILA: Legged Robot Vision-Language-Action Model for Navigation. arXiv (2025). https://doi.org/ 10.48550/arXiv.2412.04453 

- [24] Fuentes, L.F.M., Khan, M.H., Cabrera, M.A., Serpiva, V., Iarchuk, D., Mahmoud, Y., et al.: VLH: Vision-Language-Haptics Foundation Model. arXiv (2025). https:// doi.org/10.48550/arXiv.2508.01361 

- [25] Gu, J., Wu, Z., Si, P., Qiu, S., Feng, Y., Sun, L., et al.: USIM and U0: A VisionLanguage-Action Dataset and Model for General Underwater Robots. arXiv (2025). https://doi.org/10.48550/arXiv.2510.07869 

- [26] Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., et al.: $ _π_ ~~0~~ $: A VisionLanguage-Action Flow Model for General Robot Control. arXiv (2024). https://doi. org/10.48550/arXiv.2410.24164 

- [27] Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., et al.: $ _π_ _~~{~~_ 0.5 _}_ $: A Vision-LanguageAction Model with Open-World Generalization. arXiv (2025). https://doi.org/10. 48550/arXiv.2504.16054 

- [28] Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., _et al._ : RT-1: Robotics Transformer for Real-World Control at Scale. In: Robotics: Science and Systems XIX. Robotics: Science and Systems Foundation, ??? (2023). https://doi.org/10. 15607/RSS.2023.XIX.025 

- [29] Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., et al.: RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. arXiv (2023). https://doi.org/10. 48550/arXiv.2307.15818 

- [30] Shao, R., Li, W., Zhang, L., Zhang, R., Liu, Z., Chen, R., et al.: Large VLM-based Vision-Language-Action Models for Robotic Manipulation: A Survey. arXiv (2025). https://doi.org/10.48550/arXiv.2508.13073 

- [31] Cui, C., Ding, P., Song, W., Bai, S., Tong, X., Ge, Z., et al.: OpenHelix: A Short Survey, Empirical Analysis, and OpenSource Dual-System VLA Model for Robotic Manipulation. arXiv (2025). https://doi. org/10.48550/arXiv.2505.03912 

40 

- [32] Zhang, D., Sun, J., Hu, C., Wu, X., Yuan, Z., Zhou, R., et al.: Pure Vision Language Action (VLA) Models: A Comprehensive Survey. arXiv (2025). https://doi.org/10. 48550/arXiv.2509.19012 

- [33] Liu, H., Li, X., Li, P., Liu, M., Wang, D., Liu, J., et al.: Towards Generalist Robot Policies: What Matters in Building Vision-Language-Action Models. researchsquare (2025). https://doi.org/10.21203/rs. 3.rs-5770637/v1 

- [34] Sapkota, R., Cao, Y., Roumeliotis, K.I., Karkee, M.: Vision-Language-Action Models: Concepts, Progress, Applications and Challenges. arXiv (2025). https://doi.org/ 10.48550/arXiv.2505.04769 

- [35] Fan, J., Yin, Y., Wang, T., Dong, W., Zheng, P., Wang, L.: Vision-language model-based human-robot collaboration for smart manufacturing: A state-of-the-art survey. Frontiers of Engineering Management **12** (1), 177–200 (2025) https://doi.org/10. 1007/s42524-025-4136-9 

- [36] Ren, L., Dong, J., Liu, S., Zhang, L., Wang, L.: Embodied Intelligence Toward Future Smart Manufacturing in the Era of AI Foundation Model. IEEE/ASME Transactions on Mechatronics, 1–11 (2024) https://doi. org/10.1109/tmech.2024.3456250 

- [37] EN ISO 10218-1:2011 (2011) 

- [38] Guertler, M., Tomidei, L., Sick, N., Carmichael, M., Paul, G., Wambsganss, A., _et al._ : WHEN IS A ROBOT A COBOT? MOVING BEYOND MANUFACTURING AND ARM-BASED COBOT MANIPULATORS. Proceedings of the Design Society **3** , 3889–3898 (2023) https://doi.org/10.1017/pds.2023.390 

- [39] Olszewski, M.: Modern Industrial Robotics. Pomiary Automatyka Robotyka **24** (1), 5–20 (2020) https://doi.org/10.14313/PAR ~~2~~ 35/ 5 

- [40] Borboni, A., Reddy, K.V.V., Elamvazuthi, I., AL-Quraishi, M.S., Natarajan, E., 

Azhar Ali, S.S.: The Expanding Role of Artificial Intelligence in Collaborative Robots for Industrial Applications: A Systematic Review of Recent Works. Machines **11** (1), 111 (2023) https://doi.org/10.3390/ machines11010111 

- [41] Amiri, P., M¨uller, M., Southgate, M., Theodoridis, T., Wei, G., Richards-Brown, M., _et al._ : A Statistical Analysis of Commercial Articulated Industrial Robots and Cobots. Journal of Manufacturing and Materials Processing **8** (5), 216 (2024) https: //doi.org/10.3390/jmmp8050216 

- [42] Yang, M., Yang, E., Zante, R.C., Post, M., Liu, X.: Collaborative mobile industrial manipulator: A review of system architecture and applications. In: 2019 25th International Conference on Automation and Computing (ICAC), pp. 1–6. IEEE, Lancaster, United Kingdom (2019). https://doi.org/10. 23919/iconac.2019.8895183 

- [43] Robotics, I.I.F.: International Federation of Robotics. https://ifr.org/industrial-robots 

- [44] Muru, J., Rass˜olkin, A.: A Scoping Review of Energy Consumption in Industrial Robotics. Machines **13** (7), 542 (2025) https://doi.org/10.3390/machines13070542 

- [45] Brinker, J., Funk, N., Ingenlath, P., Takeda, Y., Corves, B.: Comparative Study of SerialParallel Delta Robots With Full Orientation Capabilities. IEEE Robotics and Automation Letters **2** (2), 920–926 (2017) https:// doi.org/10.1109/LRA.2017.2654551 

- [46] Autsou, S., Rass˜olkin, A., Vaimann, T., Kudelina, K.: Analysis of possible faults and diagnostic methods of the Cartesian industrial robot. Proceedings of the Estonian Academy of Sciences **71** (3), 227 (2022) https://doi.org/10.3176/proc.2022.3.04 

- [47] Collins, F., Yim, M.: Design of a spherical robot arm with the Spiral Zipper prismatic joint. In: 2016 IEEE International Conference on Robotics and Automation (ICRA), pp. 2137–2143. IEEE, Stockholm, Sweden (2016). https://doi.org/10.1109/ICRA. 

41 

2016.7487363 

- [48] Suri, S., Jain, A., Verma, N., Prasertpoj, N.: SCARA Industrial Automation Robot. In: 2018 International Conference on Power Energy, Environment and Intelligent Control (PEEIC), pp. 173–177. IEEE, Greater Noida, India (2018). https://doi. org/10.1109/PEEIC.2018.8665440 

- [49] Khatib, O., Siciliano, B. (eds.): Springer Handbook of Robotics, 2nd ed. 2016 edn. Springer Handbooks. Springer, Cham (2016). https://doi.org/10.1007/ 978-3-319-32552-1 

- [50] Taesi, C., Aggogeri, F., Pellegrini, N.: COBOT Applications—Recent Advances and Challenges. Robotics **12** (3), 79 (2023) https://doi.org/10.3390/robotics12030079 

- [51] Johannsmeier, L., Haddadin, S.: A Hierarchical Human-Robot Interaction-Planning Framework for Task Allocation in Collaborative Industrial Assembly Processes. IEEE Robotics and Automation Letters **2** (1), 41– 48 (2017) https://doi.org/10.1109/lra.2016. 2535907 

- [52] Saleem, Z., Gustafsson, F., Furey, E., McAfee, M., Huq, S.: A review of external sensors for human detection in a human robot collaborative environment. Journal of Intelligent Manufacturing **36** (4), 2255–2279 (2025) https://doi.org/10.1007/ s10845-024-02341-2 

- [53] Tan, M., Liu, Z., Wang, P.: Application and Optimization of Robot Systems in Industrial Production Line. In: 2024 Second International Conference on Inventive Computing and Informatics (ICICI), pp. 701–706. IEEE, Bangalore, India (2024). https://doi. org/10.1109/icici62254.2024.00119 

- [54] Colgate, J.E., Wannasuphoprasit, W., Peshkin, M.A.: Cobots: Robots for Collaboration With Human Operators. In: Dynamic Systems and Control, pp. 433– 439. American Society of Mechanical Engineers, Atlanta, Georgia, USA (1996). https://doi.org/10.1115/IMECE1996-0367 

- [55] Peshkin, M.A., Colgate, J.E., Wannasuphoprasit, W., Moore, C.A., Gillespie, R.B., Akella, P.: Cobot architecture. IEEE Transactions on Robotics and Automation **17** (4), 377–390 (2001) https://doi.org/10.1109/70. 954751 

- [56] Khedr, M., Yang, E.: An overview of cobots for advanced manufacturing: Humanrobot interactions and research trends. MATEC Web of Conferences **401** , 12005 (2024) https://doi.org/10.1051/matecconf/ 202440112005 

- [57] Aziz, A.N.A., Yap, H.J., Sekaran, S.C., Ismail, A.H., Hisaburi, A.S.M., Tan, C.H.: Integration of Collaborative Robots in Aerospace Manufacturing: Enhancing Precision and Safety through Advanced Sensor and Communication Technologies. In: 2024 IEEE 12th Conference on Systems, Process &amp; Control (ICSPC), pp. 177–182. IEEE, Malacca, Malaysia (2024). https://doi.org/10.1109/ICSPC63060.2024. 10862208 

- [58] Kopp, T., Baumgartner, M., Kinkel, S.: Success factors for introducing industrial human-robot interaction in practice: An empirically driven framework. The International Journal of Advanced Manufacturing Technology **112** (3-4), 685–704 (2021) https: //doi.org/10.1007/s00170-020-06398-0 

- [59] Javaid, M., Haleem, A., Singh, R.P., Rab, S., Suman, R.: Significant applications of Cobots in the field of manufacturing. Cognitive Robotics **2** , 222–233 (2022) https:// doi.org/10.1016/j.cogr.2022.10.001 

- [60] Kakade, S., Patle, B., Umbarkar, A.: Applications of collaborative robots in agile manufacturing: A review. Robotic Systems and Applications **3** (1), 59–83 (2023) https://doi. org/10.21595/rsa.2023.23238 

- [61] George, D.A.S., A.S.Hovan George: The Cobot Chronicles: Evaluating the Emergence, Evolution, and Impact of Collaborative Robots in Next-Generation Manufacturing (2023) https://doi.org/10.5281/ ZENODO.8021406 

42 

- [62] El Zaatari, S., Marei, M., Li, W., Usman, Z.: Cobot programming for collaborative industrial tasks: An overview. Robotics and Autonomous Systems **116** , 162–180 (2019) https: //doi.org/10.1016/j.robot.2019.03.003 

- [63] Sen, R., Lohar, A., Panwar, A., Singh, A., Sahu, A., Gurjer, A., _et al._ : COBOT (COLLABORATIVE ROBOT) IN MANUFACTURING INDUSTRIES AND ASSEMBLY LINE. International Journal of Technical Research & Science **9** (Spl), 27–35 (2024) https://doi.org/10.30780/ specialissue-ISET-2024/047 

- [64] Saleem, M., Jameel, S., Hassan, A., Khan, Z.H.: Design and Fabrication of a Six DOF Gantry Robot for Welding Applications. In: 2024 ASU International Conference in Emerging Technologies for Sustainability and Intelligent Systems (ICETSIS), pp. 1940–1946. IEEE, Manama, Bahrain (2024). https://doi.org/10. 1109/ICETSIS61505.2024.10459371 

- [65] Yang, X., Zhou, Z., Sørensen, J.H., Christensen, C.B., ¨Unalan, M., Zhang, X.: Automation of SME production with a Cobot system powered by learning-based vision. Robotics and Computer-Integrated Manufacturing **83** , 102564 (2023) https:// doi.org/10.1016/j.rcim.2023.102564 

- [66] Sahan, A.S.M., Kathiravan, S., Lokesh, M., Raffik, R.: Role of Cobots over Industrial Robots in Industry 5.0: A Review. In: 2023 2nd International Conference on Advancements in Electrical, Electronics, Communication, Computing and Automation (ICAECA), pp. 1–5. IEEE, Coimbatore, India (2023). https://doi.org/10.1109/ ICAECA56562.2023.10201199 

- [67] Lefranc, G., Lopez-Juarez, I., OsorioCompar´an, R., Pe˜na-Cabrera, M.: Impact of Cobots on automation. Procedia Computer Science **214** , 71–78 (2022) https://doi.org/ 10.1016/j.procs.2022.11.150 

- [68] Grau, A., Indri, M., Lo Bello, L., Sauter, T.: Robots in Industry: The Past, Present, and 

Future of a Growing Collaboration With Humans. IEEE Industrial Electronics Magazine **15** (1), 50–61 (2021) https://doi.org/ 10.1109/MIE.2020.3008136 

- [69] Dzedzickis, A., Subaˇci¯ut˙e-Zemaitien˙e,<sup>ˇ</sup> J., Sutinys,<sup>ˇ</sup> E., Samukait˙e-Bubnien˙e, U., Buˇcinskas, V.: Advanced Applications of Industrial Robotics: New Trends and Possibilities. Applied Sciences **12** (1), 135 (2021) https://doi.org/10.3390/app12010135 

- [70] Barnett, N., Costenaro, D., Rohmund, I.: Direct and Indirect Impacts of Robots on Future Electricity Load. In: 2017 ACEEE Summer Study on Energy Efficiency In Industry (2017) 

- [71] Uhlmann, E., Reinkober, S., Hollerbach, T.: Energy Efficient Usage of Industrial Robots for Machining Processes. Procedia CIRP **48** , 206–211 (2016) https://doi.org/10.1016/j. procir.2016.03.241 

- [72] Gadaleta, M., Berselli, G., Pellicciari, M., Grassia, F.: Extensive experimental investigation for the optimization of the energy consumption of a high payload industrial robot with open research dataset. Robotics and Computer-Integrated Manufacturing **68** , 102046 (2021) https://doi.org/ 10.1016/j.rcim.2020.102046 

- [73] Li, P., Liu, X.: Common Sensors in Industrial Robots: A Review. Journal of Physics: Conference Series **1267** (1), 012036 (2019) https://doi.org/10.1088/1742-6596/ 1267/1/012036 

- [74] Dang, T., Nguyen, K., Huber, M.: ExtPerFC: An Efficient 2D and 3D Perception Hardware-Software Framework for Mobile Cobot. arXiv (2023). https://doi.org/10.48550/arXiv.2306.04853 

- [75] Scholz, C., Cao, H.-L., Imrith, E., Roshandel, N., Firouzipouyaei, H., Burkiewicz, A., _et al._ : Sensor-Enabled Safety Systems for Human–Robot Collaboration: A Review. IEEE Sensors Journal **25** (1), 65–88 (2025) https://doi.org/10.1109/JSEN.2024. 3496905 

43 

- [76] Buy the Latest Jetson Products _|_ NVIDIA Developer. https://developer.nvidia.com/buy-jetson (2025) 

- [77] Jetson T5000 Modules Datasheet DS11945001 v1.1. NVIDIA (2025) 

- [78] NVIDIA RTX Blackwell GPU Architecture v1.1. NVIDIA (2025) 

- [79] Arrow Electronics: Connect with Electronic Components _|_ Arrow.Com. https://www.arrow.com/en (2025) 

- [80] Samanta, A., Hatai, I., Mal, A.K.: A Survey on Hardware Accelerator Design of Deep Learning for Edge Devices. Wireless Personal Communications **137** (3), 1715–1760 (2024) https://doi.org/10.1007/ s11277-024-11443-2 

- [81] Woisetschl¨ager, H., Erben, A., Wang, S., Mayer, R., Jacobsen, H.-A.: Federated FineTuning of LLMs on the Very Edge: The Good, the Bad, the Ugly. In: Proceedings of the Eighth Workshop on Data Management for End-to-End Machine Learning, pp. 39– 50. ACM, Santiago AA Chile (2024). https: //doi.org/10.1145/3650203.3663331 

- [82] Yi, S., Hao, Z., Qin, Z., Li, Q.: Fog Computing: Platform and Applications. In: 2015 Third IEEE Workshop on Hot Topics in Web Systems and Technologies (HotWeb), pp. 73–78. IEEE, Washington DC, DC, USA (2015). https://doi.org/10. 1109/HotWeb.2015.22 

- [83] Atlam, H., Walters, R., Wills, G.: Fog Computing and the Internet of Things: A Review. Big Data and Cognitive Computing **2** (2), 10 (2018) https://doi.org/10.3390/ bdcc2020010 

- [84] Boss, G., Malladi, P., Quan, D., Legregni, L.: CLOUD ~~C~~ OMPUTING. Technical report, IBM (October 2007) 

- [85] Ismail, B.I., Khalid, M.F., Kandan, R., Ahmad, H., Mohd Mydin, M.N., Hong Hoe, O.: Cobot Fleet Management System Using 

Cloud and Edge Computing. In: 2020 IEEE 7th International Conference on Engineering Technologies and Applied Sciences (ICETAS), pp. 1–5. IEEE, Kuala Lumpur, Malaysia (2020). https://doi.org/10.1109/ ICETAS51660.2020.9484266 

- [86] Mystkowska, G., Monopoli, M., Nannipieri, P., Zulberti, L., Merodio Codinachs, D., Fanucci, L.: Hardware Platforms Enabling Edge AI for Space Applications: A Critical Review. IEEE Access **13** , 143939–143956 (2025) https://doi.org/ 10.1109/ACCESS.2025.3596326 

- [87] Huang, Z., Shen, Y., Li, J., Fey, M., Brecher, C.: A Survey on AI-Driven Digital Twins in Industry 4.0: Smart Manufacturing and Advanced Robotics. Sensors **21** (19), 6340 (2021) https://doi.org/10.3390/s21196340 

- [88] Herrero, H., Out´on, J., Puerto, M., Sall´e, D., L´opez De Ipi˜na, K.: Enhanced Flexibility and Reusability through State MachineBased Architectures for Multisensor Intelligent Robotics. Sensors **17** (6), 1249 (2017) https://doi.org/10.3390/s17061249 

- [89] Waseem, M., Chang, Q.: Enhancing Flexibility in Smart Manufacturing: System Property Enabled Multiagent Approach for Mobile Robot Scheduling in Multiproduct Flexible Manufacturing Systems. arXiv (2025). https: //doi.org/10.48550/ARXIV.2504.20053 

- [90] Tellaeche, A., Maurtua, I., Ibarguren, A.: Human robot interaction in industrial robotics. Examples from research centers to industry. In: 2015 IEEE 20th Conference on Emerging Technologies & Factory Automation (ETFA), pp. 1–6. IEEE, Luxembourg, Luxembourg (2015). https://doi. org/10.1109/etfa.2015.7301650 

- [91] Fan, H., Liu, X., Fuh, J.Y.H., Lu, W.F., Li, B.: Embodied intelligence in manufacturing: Leveraging large language models for autonomous industrial robotics. Journal of Intelligent Manufacturing **36** (2), 1141–1157 (2025) https://doi.org/10.1007/ s10845-023-02294-y 

44 

- [92] Mohammadi Amin, F., Rezayati, M., Van De Venn, H.W., Karimpour, H.: A MixedPerception Approach for Safe Human– Robot Collaboration in Industrial Automation. Sensors **20** (21), 6347 (2020) https:// doi.org/10.3390/s20216347 

- [93] Bonci, A., Cen Cheng, P.D., Indri, M., Nabissi, G., Sibona, F.: Human-Robot Perception in Industrial Environments: A Survey. Sensors **21** (5), 1571 (2021) https://doi. org/10.3390/s21051571 

- [94] Liu, Z., Liu, Q., Xu, W., Wang, L., Zhou, Z.: Robot learning towards smart robotic manufacturing: A review. Robotics and Computer-Integrated Manufacturing **77** , 102360 (2022) https://doi.org/10.1016/ j.rcim.2022.102360 

- [95] Liu, C., Tomizuka, M.: Robot Safe Interaction System for Intelligent Industrial CoRobots. arXiv (2018). https://doi.org/10. 48550/arXiv.1808.03983 

- [96] Abuzar Yaqoob Mulla, Gauri Ansurkar: AI and Robotics: Designing Intelligent and Adaptive Robots for Industrial Automation. International Journal of Scientific Research in Science and Technology, 817–824 (2023) https://doi.org/10.32628/ijsrst523102126 

- [97] Villani, V., Pini, F., Leali, F., Secchi, C., Fantuzzi, C.: Survey on HumanRobot Interaction for Robot Programming in Industrial Applications. IFACPapersOnLine **51** (11), 66–71 (2018) https: //doi.org/10.1016/j.ifacol.2018.08.236 

- [98] Li, K., Wang, J., Wu, X., Peng, X., Chang, R., Deng, X., et al.: Optimizing Automated Picking Systems in Warehouse Robots Using Machine Learning. arXiv (2024). https:// doi.org/10.48550/arXiv.2408.16633 

- [99] Wunderle, Y., Lyczkowski, E.: Sensor fusion for functional safety of autonomous mobile robots in urban and industrial environments. In: 2022 IEEE 27th International Conference on Emerging Technologies and Factory Automation (ETFA), pp. 1–4. IEEE, Stuttgart, Germany (2022). https:// 

doi.org/10.1109/etfa52439.2022.9921688 

- [100] Calder´on-Cordova, C., Sarango, R., Castillo, D., Lakshminarayanan, V.: A Deep Reinforcement Learning Framework for Control of Robotic Manipulators in Simulated Environments. IEEE Access **12** , 103133–103161 (2024) https://doi.org/10.1109/access.2024. 3432741 

- [101] Zhang, Z., Qian, K., Schuller, B.W., Wollherr, D.: An Online Robot Collision Detection and Identification Scheme by Supervised Learning and Bayesian Decision Theory. IEEE Transactions on Automation Science and Engineering **18** (3), 1144– 1156 (2021) https://doi.org/10.1109/tase. 2020.2997094 

- [102] Andres, A., Martinez-Seras, A., La˜na, I., Del Ser, J.: On the black-box explainability of object detection models for safe and trustworthy industrial applications. Results in Engineering **24** , 103498 (2024) https:// doi.org/10.1016/j.rineng.2024.103498 

- [103] Rodriguez-Guerra, D., Sorrosal, G., Cabanes, I., Calleja, C.: Human-Robot Interaction Review: Challenges and Solutions for Modern Industrial Environments. IEEE Access **9** , 108557–108578 (2021) https: //doi.org/10.1109/access.2021.3099287 

- [104] Othman, U., Yang, E.: Human–Robot Collaborations in Smart Manufacturing Environments: Review and Outlook. Sensors **23** (12), 5663 (2023) https://doi.org/10. 3390/s23125663 

- [105] Halme, R.-J., Lanz, M., K¨am¨ar¨ainen, J., Pieters, R., Latokartano, J., Hietanen, A.: Review of vision-based safety systems for human-robot collaboration. Procedia CIRP **72** , 111–116 (2018) https://doi.org/ 10.1016/j.procir.2018.03.043 

- [106] Robla-Gomez, S., Becerra, V.M., Llata, J.R., Gonzalez-Sarabia, E., Torre-Ferrero, C., Perez-Oria, J.: Working Together: A Review on Safe Human-Robot Collaboration in Industrial Environments. IEEE Access **5** , 26754–26773 (2017) https://doi. 

45 

org/10.1109/access.2017.2773127 

- [107] Nahavandi, S., Alizadehsani, R., Nahavandi, D., Lim, C.P., Kelly, K., Bello, F.: Machine Learning Meets Advanced Robotic Manipulation. arXiv (2023). https://doi.org/10. 48550/arXiv.2309.12560 

- [108] Duijkeren, N., Palmieri, L., Lange, R., Kleiner, A.: An Industrial Perspective on Multi-Agent Decision Making for Interoperable Robot Navigation Following the VDA5050 Standard. arXiv (2023). https:// doi.org/10.48550/arXiv.2311.14615 

- [109] Landi, C.T., Ferraguti, F., Costi, S., Bonfe, M., Secchi, C.: Safety Barrier Functions for Human-Robot Interaction with Industrial Manipulators. In: 2019 18th European Control Conference (ECC), pp. 2565–2570. IEEE, Naples, Italy (2019). https://doi.org/ 10.23919/ecc.2019.8796235 

- [110] Lins, R.G., Givigi, S.N.: Cooperative Robotics and Machine Learning for Smart Manufacturing: Platform Design and Trends Within the Context of Industrial Internet of Things. IEEE Access **9** , 95444–95455 (2021) https: //doi.org/10.1109/access.2021.3094374 

- [111] Liu, S., Wang, L., Wang, X.V.: Sensorless force estimation for industrial robots using disturbance observer and neural learning of friction approximation. Robotics and Computer-Integrated Manufacturing **71** , 102168 (2021) https://doi.org/10.1016/ j.rcim.2021.102168 

- [112] Prati, E., Villani, V., Grandi, F., Peruzzini, M., Sabattini, L.: Use of Interaction Design Methodologies for Human–Robot Collaboration in Industrial Scenarios. IEEE Transactions on Automation Science and Engineering **19** (4), 3126–3138 (2022) https:// doi.org/10.1109/tase.2021.3107583 

- [113] Nakhaeinia, D., Laferriere, P., Payeur, P., Laganiere, R.: Safe Close-Proximity and Physical Human-Robot Interaction Using Industrial Robots. In: 2015 12th Conference on Computer and Robot Vision, pp. 

237–244. IEEE, Halifax, NS, Canada (2015). https://doi.org/10.1109/crv.2015.38 

- [114] Hjorth, S., Chrysostomou, D.: Human– robot collaboration in industrial environments: A literature review on non-destructive disassembly. Robotics and Computer-Integrated Manufacturing **73** , 102208 (2022) https: //doi.org/10.1016/j.rcim.2021.102208 

- [115] De Simone, G., Greco, A., Rosa, F., Saggese, A., Vento, M.: Context-aware data augmentation for enhanced speech command recognition in industrial environments. Scientific Reports **15** (1) (2025) https://doi. org/10.1038/s41598-025-01886-3 

- [116] Weiss, A., Huber, A., Minichberger, J., Ikeda, M.: First Application of Robot Teaching in an Existing Industry 4.0 Environment: Does It Really Work? Societies **6** (3), 20 (2016) https://doi.org/10.3390/ soc6030020 

- [117] Patr´ıcio, L., Varela, L., Silveira, Z., Felgueiras, C., Pereira, F.: A Framework for Integrating Robotic Process Automation with Artificial Intelligence Applied to Industry 5.0. Applied Sciences **15** (13), 7402 (2025) https://doi.org/ 10.3390/app15137402 

- [118] Schreiter, T., Rudenko, A., R¨uppel, J.V., Magnusson, M., Lilienthal, A.J.: Multimodal Interaction and Intention Communication for Industrial Robots. arXiv (2025). https://doi.org/10.48550/arXiv.2502.17971 

- [119] Manonmani, A., Akash, S., Aswinraj, A., Manikandan, A.: Literature Review on Advanced Cloud Robotics for Enhanced Industrial Automation. In: 2025 International Conference on Electronics and Renewable Systems (ICEARS), pp. 46–51. IEEE, Tuticorin, India (2025). https://doi. org/10.1109/icears64219.2025.10940892 

- [120] Triantafyllou, P., Afonso Rodrigues, R., Chaikunsaeng, S., Almeida, D., Deacon, G., Konstantinova, J., _et al._ : A Methodology for Approaching the Integration of Complex 

46 

Robotics Systems: Illustration Through a Bimanual Manipulation Case Study. IEEE Robotics & Automation Magazine **28** (2), 88–100 (2021) https://doi.org/10.1109/mra. 2021.3064759 

- [121] Quarta, D., Pogliani, M., Polino, M., Maggi, F., Zanchettin, A.M., Zanero, S.: An Experimental Security Analysis of an Industrial Robot Controller. In: 2017 IEEE Symposium on Security and Privacy (SP), pp. 268–286. IEEE, San Jose, CA, USA (2017). https://doi.org/10.1109/sp.2017.20 

- [122] Lo Bello, L., Mubeen, S., Saponara, S., Mariani, R., Dutta Bordoloi, U.: Guest Editorial Embedded and Networked Systems for Intelligent Vehicles and Robots. IEEE Transactions on Industrial Informatics **15** (2), 1035–1037 (2019) https://doi.org/ 10.1109/tii.2018.2886529 

- [123] Abdullayev, V., Faizal, A., Seyidova, I., Mikayilov, S., Mammadova, R., Pirverdiyeva, L., _et al._ : Integration of Artificial Intelligence and Robotics into the industrial sector. Data and Metadata **4** , 209 (2025) https://doi.org/10.56294/dm2025209 

- [124] Prajapati, V.K., Shashank, S.A., Nithya, M.: Computer Vision Enabled Pick and Place Robot for Warehouse Automation. In: 2024 5th International Conference on Smart Electronics and Communication (ICOSEC), pp. 641–646. IEEE, Trichy, India (2024). https://doi.org/10. 1109/icosec61587.2024.10722718 

- [125] Mezg´ar, I., V´ancza, J., Paniti, I., T´oth, J.: Transforming Experimental Cobot Cell to Industrial Realization – an Ethical AI Approach. IFAC-PapersOnLine **56** (2), 7335–7341 (2023) https://doi.org/10.1016/ j.ifacol.2023.10.347 

- [126] Shen, J.: Progress And Comprehensive Analysis of Intelligent Grasping Technology for Robotic Arms Based on Computer Vision. Highlights in Science, Engineering and Technology **103** , 205–211 (2024) https: //doi.org/10.54097/3rj4ke82 

- [127] Yang, C., Kang, J., Eom, D.-S.: Enhancing ToF Sensor Precision Using 3D Models and Simulation for Vision Inspection in Industrial Mobile Robots. Applied Sciences **14** (11), 4595 (2024) https://doi.org/ 10.3390/app14114595 

- [128] Chen, S.-C., Pamungkas, R.S., Schmidt, D.: The Role of Machine Learning in Improving Robotic Perception and Decision Making. International Transactions on Artificial Intelligence (ITALIC) **3** (1), 32–43 (2024) https://doi.org/10.33050/italic.v3i1.661 

- [129] D, S., R, Anil.A., Sivadasan, J., Jayakumar, T., Manivel, M., C, A.: Intelligent control algorithms for industrial automation systems. In: 2025 IEEE International Students’ Conference on Electrical, Electronics and Computer Science (SCEECS), pp. 1– 6. IEEE, Bhopal, India (2025). https://doi. org/10.1109/sceecs64059.2025.10940929 

- [130] You, J., Wu, Z., Wei, W., Li, N., Yang, Y.: Evolution of Industrial Robots from the Perspective of the Metaverse: Integration of Virtual and Physical Realities and Human–Robot Collaboration. Applied Sciences **14** (14), 6369 (2024) https://doi.org/ 10.3390/app14146369 

- [131] Oyekanlu, E.A., Smith, A.C., Thomas, W.P., Mulroy, G., Hitesh, D., Ramsey, M., _et al._ : A Review of Recent Advances in Automated Guided Vehicle Technologies: Integration Challenges and Research Areas for 5G-Based Smart Manufacturing Applications. IEEE Access **8** , 202312–202353 (2020) https://doi.org/10.1109/access.2020. 3035729 

- [132] Pelleti, S., Kumar, J.R.R., Krushnasamy, V.S., Raj, G.B.M.: Intelligent Control Systems for Industrial Automation and Robotics. In: 2024 Ninth International Conference on Science Technology Engineering and Mathematics (ICONSTEM), pp. 1–5. IEEE, Chennai, India (2024). https://doi. org/10.1109/iconstem60960.2024.10568781 

- [133] Linder, T., Vaskevicius, N., Schirmer, R., Arras, K.O.: Cross-Modal Analysis of 

47 

Human Detection for Robotics: An Industrial Case Study. In: 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, Prague, Czech Republic (2021). https://doi.org/10.1109/ iros51168.2021.9636158 

- [134] Alt, B., Zahn, J., Kienle, C., Dvorak, J., May, M., Katic, D., _et al._ : Human-AI Interaction in Industrial Robotics: Design and Empirical Evaluation of a User Interface for Explainable AI-Based Robot Program Optimization. Procedia CIRP **130** , 591– 596 (2024) https://doi.org/10.1016/j.procir. 2024.10.134 

- [135] Menolotto, M., Komaris, D.-S., Tedesco, S., O’Flynn, B., Walsh, M.: Motion Capture Technology in Industrial Applications: A Systematic Review. Sensors **20** (19), 5687 (2020) https://doi.org/10.3390/s20195687 

- [136] Makulaviˇcius, M., Petkeviˇcius, S., Roˇz˙en˙e, J., Dzedzickis, A., Buˇcinskas, V.: Industrial Robots in Mechanical Machining: Perspectives and Limitations. Robotics **12** (6), 160 (2023) https://doi.org/10.3390/ robotics12060160 

- [137] Kube, D., Hadwiger, S., Meisen, T.: Beyond performance: Explaining generalisation failures of Robotic Foundation Models in industrial simulation. Biomimetic Intelligence and Robotics **5** (4), 100249 (2025) https:// doi.org/10.1016/j.birob.2025.100249 

- [138] Tsoumplekas, G., Li, V., Siniosoglou, I., Argyriou, V., Goudos, S.K., Moscholios, I.D., _et al._ : Evaluating the Energy Efficiency of Few-Shot Learning for Object Detection in Industrial Settings. In: 2024 IEEE 3rd Real-Time and Intelligent Edge Computing Workshop (RAGE), pp. 1–6. IEEE, Hong Kong, Hong Kong (2024). https://doi.org/ 10.1109/RAGE62451.2024.00016 

- [139] Zhang, Y., Wang, C., Lu, O., Zhao, Y., Ge, Y., Sun, Z., et al.: AlignThen-stEer: Adapting the Vision-Language Action Models through Unified Latent Guidance. arXiv (2025). https://doi.org/10. 48550/arXiv.2509.02055 

- [140] Bohlinger, N., Czechmanowski, G., Krupka, M., Kicki, P., Walas, K., Peters, J., et al.: One Policy to Run Them All: An End-to-end Learning Approach to MultiEmbodiment Locomotion. arXiv (2025). https://doi.org/10.48550/arXiv.2409.06366 

- [141] Jones, E.K., Robey, A., Zou, A., Ravichandran, Z., Pappas, G.J., Hassani, H., et al.: Adversarial Attacks on Robotic Vision Language Action Models. arXiv (2025). https: //doi.org/10.48550/arXiv.2506.03350 

- [142] Xu, H., Koh, Y.S., Huang, S., Zhou, Z., Wang, D., Sakuma, J., et al.: Model-Agnostic Adversarial Attack and Defense for Vision-LanguageAction Models. arXiv (2025). https: //doi.org/10.48550/arXiv.2510.13237 

- [143] Liu, H., Zhang, Y., Betala, V., Zhang, E., Liu, J., Ding, C., et al.: Multi-Task Interactive Robot Fleet Learning with Visual World Models. arXiv (2024). https://doi. org/10.48550/arXiv.2410.22689 

- [144] Zollo, T.P., Zemel, R.: Confidence Calibration in Vision-Language-Action Models. arXiv (2025). https://doi.org/10.48550/ arXiv.2507.17383 

- [145] Ren, A.Z., Dixit, A., Bodrova, A., Singh, S., Tu, S., Brown, N., et al.: Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners. arXiv (2023). https://doi.org/10.48550/arXiv.2307.01928 

- [146] Chisari, E., Hartz, J.O., Despinoy, F., Valada, A.: Robotic Task Ambiguity Resolution via Natural Language Interaction. arXiv (2025). https: //doi.org/10.48550/arXiv.2504.17748 

- [147] Bucker, A., Figueredo, L., Haddadin, S., Kapoor, A., Ma, S., Vemprala, S., _et al._ : LATTE: LAnguage Trajectory TransformEr. In: 2023 IEEE International Conference on Robotics and Automation (ICRA), pp. 7287–7294. IEEE, London, United Kingdom (2023). https://doi.org/10.1109/ ICRA48891.2023.10161068 

48 

- [148] Shi, L.X., Hu, Z., Zhao, T.Z., Sharma, A., Pertsch, K., Luo, J., et al.: Yell At Your Robot: Improving On-the-Fly from Language Corrections. arXiv (2024). https:// doi.org/10.48550/arXiv.2403.12910 

- [149] Xiang, T.-Y., Jin, A.-Q., Zhou, X.H., Gui, M.-J., Xie, X.-L., Liu, S.-Q., et al.: VLA Model-Expert Collaboration for Bi-directional Manipulation Learning. arXiv (2025). https://doi.org/10.48550/arXiv.2503.04163 

- [150] Zhou, E., Su, Q., Chi, C., Zhang, Z., Wang, Z., Huang, T., et al.: Code-as-Monitor: Constraint-aware Visual Programming for Reactive and Proactive Robotic Failure Detection. arXiv (2025). https://doi.org/10. 48550/arXiv.2412.04455 

- [151] Gu, Q., Ju, Y., Sun, S., Gilitschenski, I., Nishimura, H., Itkina, M., et al.: SAFE: Multitask Failure Detection for VisionLanguage-Action Models. arXiv (2025). https://doi.org/10.48550/arXiv.2506.09937 

- [152] Xia, W., Feng, R., Wang, D., Hu, D.: Phoenix: A Motion-based Self-Reflection Framework for Fine-grained Robotic Action Correction. arXiv (2025). https://doi.org/ 10.48550/arXiv.2504.14588 

- [153] Koo, M., Choi, D., Kim, T., Lee, K., Kim, C., Seo, Y., et al.: HAMLET: Switch Your Vision-Language-Action Model into a History-Aware Policy. arXiv (2025). https: //doi.org/10.48550/arXiv.2510.00695 

- [154] Liu, Z., Bahety, A., Song, S.: REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction. arXiv (2023). https://doi.org/10.48550/arXiv.2306.15724 

- [155] Miao, C., Chang, T., Wu, M., Xu, H., Li, C., Li, M., et al.: FedVLA: Federated VisionLanguage-Action Learning with Dual Gating Mixture-of-Experts for Robotic Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2508.02190 

- [156] Lin, Z., Duan, J., Fang, H., Fox, D., Krishna, R., Tan, C., et al.: FailSafe: Reasoning and 

Recovery from Failures in Vision-LanguageAction Models. arXiv (2025). https://doi. org/10.48550/arXiv.2510.01642 

- [157] Team, G.R., Abdolmaleki, A., Abeyruwan, S., Ainslie, J., Alayrac, J.-B., Arenas, M.G., et al.: Gemini Robotics 1.5: Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning, Thinking, and Motion Transfer. arXiv (2025). https: //doi.org/10.48550/arXiv.2510.03342 

- [158] Sun, N., Li, Y., Wang, C., Li, H., Liu, H.: CollabVLA: Self-Reflective VisionLanguage-Action Model Dreaming Together with Human. arXiv (2025). https://doi.org/ 10.48550/arXiv.2509.14889 

- [159] Li, S., Gao, L., Wang, J., Che, C., Xiao, X., Cao, J., et al.: Information-Theoretic Graph Fusion with Vision-Language-Action Model for Policy Reasoning and Dual Robotic Control. arXiv (2025). https://doi.org/10. 48550/arXiv.2508.05342 

- [160] Li, C., Liu, J., Wang, G., Li, X., Chen, S., Heng, L., et al.: A Self-Correcting VisionLanguage-Action Model for Fast and Slow System Manipulation. arXiv (2025). https: //doi.org/10.48550/arXiv.2405.17418 

- [161] Jones, J., Mees, O., Sferrazza, C., Stachowicz, K., Abbeel, P., Levine, S.: Beyond Sight: Finetuning Generalist Robot Policies with Heterogeneous Sensors via Language Grounding. arXiv (2025). https://doi.org/ 10.48550/arXiv.2501.04693 

- [162] Huang, H., Cen, M., Tan, K., Quan, X., Huang, G., Zhang, H.: GraphCoTVLA: A 3D Spatial-Aware Reasoning Vision-Language-Action Model for Robotic Manipulation with Ambiguous Instructions. arXiv (2025). https://doi.org/10. 48550/arXiv.2508.07650 

- [163] Li, Y., Deng, Y., Zhang, J., Jang, J., Memmel, M., Yu, R., et al.: HAMSTER: Hierarchical Action Models For Open-World Robot Manipulation. arXiv (2025). https: //doi.org/10.48550/arXiv.2502.05485 

49 

- [164] Wu, H., Zhang, H., Zhang, P., Wang, J., Wang, C.: HiBerNAC: Hierarchical Brainemulated Robotic Neural Agent Collective for Disentangling Complex Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2506.08296 

- [165] Lynch, C., Sermanet, P.: Language Conditioned Imitation Learning over Unstructured Data. arXiv (2021). https://doi.org/ 10.48550/arXiv.2005.07648 

- [166] Chen, J., Wang, J., Chen, L., Cai, C., Lu, J.: NanoVLA: Routing Decoupled VisionLanguage Understanding for Nano-sized Generalist Robotic Policies. arXiv (2025). https://doi.org/10.48550/arXiv.2510.25122 

- [167] Driess, D., Xia, F., Sajjadi, M.S.M., Lynch, C., Chowdhery, A., Ichter, B., et al.: PaLME: An Embodied Multimodal Language Model. arXiv (2023). https://doi.org/10. 48550/arXiv.2303.03378 

- [168] Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., et al.: SmolVLA: A Vision-LanguageAction Model for Affordable and Efficient Robotics. arXiv (2025). https://doi.org/10. 48550/arXiv.2506.01844 

- [169] Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., et al.: UniVLA: Learning to Act Anywhere with Task-centric Latent Actions. arXiv (2025). https://doi.org/10. 48550/arXiv.2505.06111 

- [170] Sun, J., Mao, P., Kong, L., Wang, J.: A Review of Embodied Grasping. Sensors **25** (3), 852 (2025) https://doi.org/10.3390/ s25030852 

- [171] Yuan, M., Yu, T., Ge, W., Yao, X., Wang, H., Chen, J., et al.: A Survey of Behavior Foundation Model: Next-Generation Whole-Body Control System of Humanoid Robots. arXiv (2025). https://doi.org/10. 48550/arXiv.2506.20487 

- [172] Gao, J., Belkhale, S., Dasari, S., Balakrishna, A., Shah, D., Sadigh, D.: A Taxonomy for Evaluating Generalist Robot 

Policies. arXiv (2025). https://doi.org/10. 48550/arXiv.2503.01238 

- [173] Liu, Y., Chen, W., Bai, Y., Liang, X., Li, G., Gao, W., et al.: Aligning Cyber Space with Physical World: A Comprehensive Survey on Embodied AI. arXiv (2025). https: //doi.org/10.48550/arXiv.2407.06886 

- [174] Li, J., Li, J., Yang, G., Yang, L., Chi, H., Yang, L.: Applications of Large Language Models and Multimodal Large Models in Autonomous Driving: A Comprehensive Review. Drones **9** (4), 238 (2025) https:// doi.org/10.3390/drones9040238 

- [175] Lisondra, M., Benhabib, B., Nejat, G.: Embodied AI with Foundation Models for Mobile Service Robots: A Systematic Review. arXiv (2025). https://doi.org/10. 48550/arXiv.2505.20503 

- [176] Xu, P.: Embodied AI: Bridging Simulation and Reality in Robotics. In: 2025 4th International Symposium on Robotics, Artificial Intelligence and Information Engineering (RAIIE), pp. 244–248. IEEE, Zhenjiang, China (2025). https://doi.org/10. 1109/RAIIE65740.2025.11140070 

- [177] Feng, T., Wang, X., Jiang, Y.-G., Zhu, W.: Embodied AI: From LLMs to World Models. arXiv (2025). https://doi.org/10.48550/ arXiv.2509.20021 

- [178] Chen, S.: Exploring Embodied Multimodal Large Models: Development, Datasets, and Future Directions. Elsevier BV (2025). https://doi.org/10.48550/arXiv.2502.15336 

- [179] Khan, M.T., Waheed, A.: Foundation Model Driven Robotics: A Comprehensive Review. arXiv (2025). https://doi.org/10. 48550/arXiv.2507.10087 

- [180] Sui, X., Tian, D., Sun, Q., Chen, R., Choi, D., Kwok, K., et al.: From Grounding to Manipulation: Case Studies of Foundation Model Integration in Embodied Robotic Systems. arXiv (2025). https://doi.org/10. 48550/arXiv.2505.15685 

50 

- [181] Zhang, K., Yun, P., Cen, J., Cai, J., Zhu, D., Yuan, H., et al.: Generative Artificial Intelligence in Robotic Manipulation: A Survey. arXiv (2025). https://doi.org/10. 48550/arXiv.2503.03464 

- [182] Liu, Y., Sun, Q., Kapadia, D.R.: Integrating Large Language Models into Robotic Autonomy: A Review of Motion, Voice, and Training Pipelines. AI **6** (7), 158 (2025) https://doi.org/10.3390/ai6070158 

- [183] Mehta, V., Sharma, C., Thiyagarajan, K.: Large Language Models and 3D Vision for Intelligent Robotic Perception and Autonomy. Sensors **25** (20), 6394 (2025) https:// doi.org/10.3390/s25206394 

- [184] Liang, W., Zhou, R., Ma, Y., Zhang, B., Li, S., Liao, Y., et al.: Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning. arXiv (2025). https://doi.org/10.48550/arXiv.2508.10399 

- [185] Borazjani, K., Abdisarabshali, P., Nadimi, F., Khosravan, N., Liwang, M., Wang, X., et al.: Multi-Modal Multi-Task (M3T) Federated Foundation Models for Embodied AI: Potentials and Challenges for Edge Integration. arXiv (2025). https://doi.org/10. 48550/arXiv.2505.11191 

- [186] Han, X., Chen, S., Fu, Z., Feng, Z., Fan, L., An, D., et al.: Multimodal Fusion and Vision-Language Models: A Survey for Robot Vision. arXiv (2025). https://doi. org/10.48550/arXiv.2504.02477 

- [187] Liu, J., Shi, X., Nguyen, T.D., Zhang, H., Zhang, T., Sun, W., et al.: Neural Brain: A Neuroscience-inspired Framework for Embodied Agents. arXiv (2025). https: //doi.org/10.48550/arXiv.2505.07634 

- [188] Sartor, S., Thompson, N.: Neural Scaling Laws in Robotics. arXiv (2025). https://doi. org/10.48550/arXiv.2405.14005 

- [189] Wang, Y., Sun, A.: Toward Embodied AGI: A Review of Embodied AI and the Road Ahead. arXiv (2025). https://doi.org/10. 48550/arXiv.2505.14235 

- [190] Salimpour, S., Fu, L., Rachwa�l, K., Bertrand, P., O’Sullivan, K., Jakob, R., et al.: Towards Embodied Agentic AI: Review and Classification of LLMand VLM-Driven Robot Autonomy and Interaction. arXiv (2025). https://doi.org/10.48550/arXiv.2508.05294 

- [191] Li, D., Jin, Y., Sun, Y., A, Y., Yu, H., Shi, J., et al.: What Foundation Models Can Bring for Robot Learning in Manipulation : A Survey. arXiv (2025). https://doi.org/10. 48550/arXiv.2404.18201 

- [192] Gao, H., Wang, Z., Li, Y., Long, K., Yang, M., Shen, Y.: A Survey for Foundation Models in Autonomous Driving. arXiv (2024). https://doi.org/10.48550/arXiv.2402.01105 

- [193] Jeong, H., Lee, H., Kim, C., Shin, S.: A Survey of Robot Intelligence with Large Language Models. Applied Sciences **14** (19), 8868 (2024) https://doi.org/10. 3390/app14198868 

- [194] Cohen, V., Liu, J.X., Mooney, R., Tellex, S., Watkins, D.: A Survey of Robotic Language Grounding: Tradeoffs between Symbols and Embeddings. arXiv (2024). https://doi.org/ 10.48550/arXiv.2405.13245 

- [195] Kim, Y., Kim, D., Choi, J., Park, J., Oh, N., Park, D.: A survey on integration of large language models with intelligent robots. Intelligent Service Robotics **17** (5), 1091–1107 (2024) https://doi.org/10.1007/ s11370-024-00550-5 

- [196] Xu, Z., Wu, K., Wen, J., Li, J., Liu, N., Che, Z., et al.: A Survey on Robotics with Foundation Models: Toward Embodied AI. arXiv (2024). https://doi.org/10.48550/ arXiv.2402.02385 

- [197] Banjanovi´c-Mehmedovi´c, L., Husakovi´c, A., Gurdi´c Ribi´c, A., Prljaˇca, N., Karabegovi´c, I.: Advancements in Robotic Intelligence: The Role of Computer Vision, DRL, Transformers and LLMs. In: Artificial Intelligence in Industry 4.0: The Future That Comes True, pp. 94–127. Academy of Sciences and Arts of Bosnia and Herzegovina, ??? (2024). 

51 

https://doi.org/10.5644/pi2024.215.05 

- [198] Sanghai, N., Brown, N.B.: Advances in Transformers for Robotic Applications: A Review. arXiv (2024). https://doi.org/10. 48550/arXiv.2412.10599 

- [199] Lin, M.-Y., Lee, O.-W., Lu, C.-Y.: Embodied AI with Large Language Models: A Survey and New HRI Framework. In: 2024 International Conference on Advanced Robotics and Mechatronics (ICARM), pp. 978–983. IEEE, Tokyo, Japan (2024). https://doi.org/10.1109/ICARM62033. 2024.10715872 

- [200] Naderi, H., Shojaei, A., Huang, L.: Foundation Models for Autonomous Robots in Unstructured Environments. arXiv (2024). https://doi.org/10.48550/ARXIV.2407. 14296 

- [201] Moroncelli, A., Soni, V., Shahid, A.A., Maccarini, M., Forgione, M., Piga, D., et al.: Integrating Reinforcement Learning with Foundation Models for Autonomous Robotics: Methods and Perspectives. arXiv (2024). https://doi.org/10.48550/arXiv.2410.16411 

- [202] Wang, J., Wu, Z., Li, Y., Jiang, H., Shu, P., Shi, E., et al.: Large Language Models for Robotics: Opportunities, Challenges, and Perspectives. arXiv (2024). https://doi. org/10.48550/arXiv.2401.04334 

- [203] Adebayo, A.S., Chukwurah, N., Ajayi, O.O.: Leveraging Foundation Models in Robotics: Transforming Task Planning and Contextual Execution. International Journal of Multidisciplinary Research and Growth Evaluation **5** (1), 1388–1394 (2024) https://doi.org/10.54660/.IJMRGE.2024.5. 1.1388-1394 

- [204] Atuhurra, J.: Leveraging Large Language Models in Human-Robot Interaction: A Critical Analysis of Potential and Pitfalls. arXiv (2024). https://doi.org/10.48550/arXiv.2405.00693 

- [205] Kawaharazuka, K., Matsushima, T., Gambardella, A., Guo, J., Paxton, C., Zeng, A.: Real-world robot applications of foundation models: A review. Advanced Robotics **38** (18), 1232–1254 (2024) https://doi.org/ 10.1080/01691864.2024.2408593 

- [206] Pashangpour, S., Nejat, G.: The Future of Intelligent Healthcare: A Systematic Analysis and Discussion on the Integration and Impact of Robots Using Large Language Models for Healthcare. Robotics **13** (8), 112 (2024) https://doi.org/10.3390/ robotics13080112 

- [207] McCarthy, R., Tan, D.C.H., Schmidt, D., Acero, F., Herr, N., Du, Y., et al.: Towards Generalist Robot Learning from Internet Video: A Survey. arXiv (2024). https://doi. org/10.48550/arXiv.2404.19664 

- [208] Google DeepMind: Demonstrating Large Language Models on Robots. In: Robotics: Science and Systems XIX. Robotics: Science and Systems Foundation, ??? (2023). https: //doi.org/10.15607/RSS.2023.XIX.024 

- [209] Zeng, F., Gan, W., Wang, Y., Liu, N., Yu, P.S.: Large Language Models for Robotics: A Survey. arXiv (2023). https://doi.org/10. 48550/arXiv.2311.07226 

- [210] Xiao, X., Liu, J., Wang, Z., Zhou, Y., Qi, Y., Cheng, Q., et al.: Robot Learning in the Era of Foundation Models: A Survey. arXiv (2023). https://doi.org/10. 48550/arXiv.2311.14379 

- [211] Huang, J., Wang, S., Lin, F., Hu, Y., Wen, C., Gao, Y.: Tactile-VLA: Unlocking Vision-Language-Action Model’s Physical Knowledge for Tactile Generalization. arXiv (2025). https://doi.org/10.48550/arXiv.2507.09160 

- [212] Zhong, Y., Huang, X., Li, R., Zhang, C., Chen, Z., Guan, T., et al.: DexGraspVLA: A Vision-LanguageAction Framework Towards General Dexterous Grasping. arXiv (2025). https://doi.org/10.48550/arXiv.2502.20900 

52 

- [213] Team, G.R., Abeyruwan, S., Ainslie, J., Alayrac, J.-B., Arenas, M.G., Armstrong, T., et al.: Gemini Robotics: Bringing AI into the Physical World. arXiv (2025). https: //doi.org/10.48550/arXiv.2503.20020 

- [214] Fang, H., Zhang, M., Dong, H., Li, W., Wang, Z., Zhang, Q., et al.: Robix: A Unified Model for Robot Interaction, Reasoning and Planning. arXiv (2025). https://doi.org/10. 48550/arXiv.2509.01106 

- [215] Liu, X., Fu, C., Yan, C., Wu, C., Gao, H., Zhang, Y.-F., et al.: VITA-E: Natural Embodied Interaction with Concurrent Seeing, Hearing, Speaking, and Acting. arXiv (2025). https://doi.org/10. 48550/arXiv.2510.21817 

- [216] Dai, Y., Lee, J., Fazeli, N., Chai, J.: RACER: Rich Language-Guided Failure Recovery Policies for Imitation Learning. In: 2025 IEEE International Conference on Robotics and Automation (ICRA), pp. 15657–15664. IEEE, Atlanta, GA, USA (2025). https://doi.org/10.1109/ ICRA55743.2025.11127799 

- [217] Yuan, Y., Cui, H., Huang, Y., Chen, Y., Ni, F., Dong, Z., et al.: Embodied-R1: Reinforced Embodied Reasoning for General Robotic Manipulation. arXiv (2025). https: //doi.org/10.48550/arXiv.2508.13998 

- [218] Chen, G., Wang, M., Cui, T., Mu, Y., Lu, H., Zhou, T., et al.: VLMimic: Vision Language Models Are Visual Imitation Learner for Fine-grained Actions. arXiv (2024). https://doi.org/10.48550/arXiv.2410.20927 

- [219] Chen, X., Chen, Y., Fu, Y., Gao, N., Jia, J., Jin, W., et al.: InternVLA-M1: A Spatially Guided Vision-Language-Action Framework for Generalist Robot Policy. arXiv (2025). https://doi.org/10.48550/arXiv.2510.13778 

- [220] Yang, Y., Duan, Z., Xie, T., Cao, F., Shen, P., Song, P., et al.: FPC-VLA: A Vision-Language-Action Framework with a Supervisor for Failure Prediction and Correction. arXiv (2025). https://doi.org/10. 48550/arXiv.2509.04018 

- [221] Li, J., Zhu, Y., Tang, Z., Wen, J., Zhu, M., Liu, X., et al.: CoA-VLA: Improving VisionLanguage-Action Models via Visual-Textual Chain-of-Affordance. arXiv (2025). https:// doi.org/10.48550/arXiv.2412.20451 

- [222] Huang, C.-P., Wu, Y.-H., Chen, M.-H., Wang, Y.-C.F., Yang, F.-E.: ThinkAct: Vision-Language-Action Reasoning via Reinforced Visual Latent Planning. arXiv (2025). https://doi.org/10.48550/arXiv. 2507.16815 

- [223] Lee, J., Duan, J., Fang, H., Deng, Y., Liu, S., Li, B., et al.: MolmoAct: Action Reasoning Models That Can Reason in Space. arXiv (2025). https://doi.org/10. 48550/arXiv.2508.07917 

- [224] Belkhale, S., Ding, T., Xiao, T., Sermanet, P., Vuong, Q., Tompson, J., et al.: RT-H: Action Hierarchies Using Language. arXiv (2024). https://doi.org/10. 48550/arXiv.2403.01823 

- [225] Huang, W., Wang, C., Zhang, R., Li, Y., Wu, J., Fei-Fei, L.: VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models. arXiv (2023). https: //doi.org/10.48550/arXiv.2307.05973 

- [226] Bu, Q., Zeng, J., Chen, L., Yang, Y., Zhou, G., Yan, J., et al.: Closed-Loop Visuomotor Control with Generative Expectation for Robotic Manipulation. arXiv (2024). https: //doi.org/10.48550/arXiv.2409.09016 

- [227] Kang, G.-C., Kim, J., Shim, K., Lee, J.K., Zhang, B.-T.: CLIPRT: Learning Language-Conditioned Robotic Policies from Natural Language Supervision. arXiv (2025). https://doi.org/10.48550/arXiv.2411.00508 

- [228] Li, M., Zhao, Z., Che, Z., Liao, F., Wu, K., Xu, Z., et al.: SwitchVLA: Execution-Aware Task Switching for Vision-Language-Action Models. arXiv (2025). https://doi.org/10. 48550/arXiv.2506.03574 

- [229] Li, S., Gao, Y., Sadigh, D., Song, S.: Unified Video Action Model. arXiv (2025). https:// 

53 

doi.org/10.48550/arXiv.2503.00200 

- [230] Liu, H., Tong, Y., Liu, G., Ju, Z., Zhang, Z.: IDAGC: Adaptive Generalized Human-Robot Collaboration via Human Intent Estimation and Multimodal Policy Learning. arXiv (2025). https://doi.org/10. 48550/arXiv.2507.04620 

- [231] Xu, K., Xia, X., Wang, K., Yang, Y., Mao, Y., Deng, B., et al.: Efficient Alignment of Unconditioned Action Prior for Language-conditioned Pick and Place in Clutter. arXiv (2025). https://doi.org/10. 48550/arXiv.2503.09423 

- [232] Black, K., Nakamoto, M., Atreya, P., Walke, H., Finn, C., Kumar, A., et al.: Zero-Shot Robotic Manipulation with Pretrained Image-Editing Diffusion Models. arXiv (2023). https://doi.org/10.48550/ arXiv.2310.10639 

- [233] Pan, M., Zhang, J., Wu, T., Zhao, Y., Gao, W., Dong, H.: OmniManip: Towards General Robotic Manipulation via ObjectCentric Interaction Primitives as Spatial Constraints. In: 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 17359–17369. IEEE, Nashville, TN, USA (2025). https: //doi.org/10.1109/CVPR52734.2025.01618 

- [234] Liu, L., Wang, W., Han, Y., Xie, Z., Yi, P., Li, J., et al.: FoAM: Foresight-Augmented Multi-Task Imitation Policy for Robotic Manipulation. arXiv (2025). https://doi. org/10.48550/arXiv.2409.19528 

- [235] Zhang, C., Hao, P., Cao, X., Hao, X., Cui, S., Wang, S.: VTLA: Vision-Tactile-LanguageAction Model with Preference Learning for Insertion Manipulation. arXiv (2025). https: //doi.org/10.48550/arXiv.2505.09577 

- [236] Ze, Y., Yan, G., Wu, Y.-H., Macaluso, A., Ge, Y., Ye, J., et al.: GNFactor: Multi-Task Real Robot Learning with Generalizable Neural Feature Fields. arXiv (2024). https: //doi.org/10.48550/arXiv.2308.16891 

- [237] Wen, J., Zhu, M., Zhu, Y., Tang, Z., Li, 

J., Zhou, Z., et al.: Diffusion-VLA: Generalizable and Interpretable Robot Foundation Model via Self-Generated Reasoning. arXiv (2025). https://doi.org/10. 48550/arXiv.2412.03293 

- [238] Li, P., Wu, H., Huang, Y., Cheang, C., Wang, L., Kong, T.: GR-MG: Leveraging Partially Annotated Data via Multi-Modal Goal-Conditioned Policy. arXiv (2024). https://doi.org/10.48550/arXiv.2408.14368 

- [239] Nasiriany, S., Kirmani, S., Ding, T., Smith, L., Zhu, Y., Driess, D., et al.: RTAffordance: Affordances Are Versatile Intermediate Representations for Robot Manipulation. arXiv (2024). https://doi.org/10. 48550/arXiv.2411.02704 

- [240] Yang, S., Li, H., Chen, Y., Wang, B., Tian, Y., Wang, T., et al.: InstructVLA: Vision-Language-Action Instruction Tuning from Understanding to Manipulation. arXiv (2025). https://doi.org/10.48550/arXiv.2507.17520 

- [241] Bharadhwaj, H., Vakil, J., Sharma, M., Gupta, A., Tulsiani, S., Kumar, V.: RoboAgent: Generalization and Efficiency in Robot Manipulation via Semantic Augmentations and Action Chunking. In: 2024 IEEE International Conference on Robotics and Automation (ICRA), pp. 4788–4795. IEEE, Yokohama, Japan (2024). https://doi.org/ 10.1109/ICRA57147.2024.10611293 

- [242] Li, C., Wen, J., Peng, Y., Peng, Y., Feng, F., Zhu, Y.: PointVLA: Injecting the 3D World into Vision-Language-Action Models. arXiv (2025). https://doi.org/10.48550/ arXiv.2503.07511 

- [243] Qu, D., Song, H., Chen, Q., Chen, Z., Gao, X., Ye, X., et al.: EO-1: Interleaved VisionText-Action Pretraining for General Robot Control. arXiv (2025). https://doi.org/10. 48550/arXiv.2508.21112 

- [244] Tang, W., Jing, D., Pan, J.-H., Lu, Z., Liu, Y.-H., Li, L.E., et al.: Incentivizing Multimodal Reasoning in Large Models for Direct Robot Manipulation. arXiv (2025). https: 

54 

//doi.org/10.48550/arXiv.2505.12744 

//doi.org/10.48550/arXiv.2506.13751 

- [245] Zhai, A., Liu, B., Fang, B., Cai, C., Ma, E., Yin, E., et al.: Igniting VLMs toward the Embodied Space. arXiv (2025). https://doi. org/10.48550/arXiv.2509.11766 

- [246] Feng, Y., Tan, H., Mao, X., Xiang, C., Liu, G., Huang, S., et al.: Vidar: Embodied Video Diffusion Model for Generalist Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2507.12898 

- [247] Li, H., Yang, S., Chen, Y., Chen, X., Yang, X., Tian, Y., et al.: CronusVLA: Towards Efficient and Robust Manipulation via Multi-Frame Vision-LanguageAction Modeling. arXiv (2025). https://doi. org/10.48550/arXiv.2506.19816 

- [248] Singh, I., Goyal, A., Birchfield, S., Fox, D., Garg, A., Blukis, V.: OG-VLA: Orthographic Image Generation for 3D-Aware Vision-Language Action Model. arXiv (2025). https://doi.org/10.48550/arXiv. 2506.01196 

- [249] Huang, H., Liu, F., Fu, L., Wu, T., Mukadam, M., Malik, J., et al.: OTTER: A Vision-LanguageAction Model with Text-Aware Visual Feature Extraction. arXiv (2025). https://doi.org/10.48550/arXiv.2503.03734 

- [250] Team, G., Ye, A., Wang, B., Ni, C., Huang, G., Zhao, G., et al.: GigaBrain-0: A World Model-Powered Vision-LanguageAction Model. arXiv (2025). https://doi. org/10.48550/arXiv.2510.19430 

- [251] Sun, Q., Hong, P., Pala, T.D., Toh, V., Tan, U.-X., Ghosal, D., et al.: Emma-X: An Embodied Multimodal Action Model with Grounded Chain of Thought and Lookahead Spatial Reasoning. arXiv (2024). https://doi.org/10.48550/arXiv.2412.11974 

- [252] Xue, H., Huang, X., Niu, D., Liao, Q., Kragerud, T., Gravdahl, J.T., et al.: LeVERB: Humanoid Whole-Body Control with Latent Vision-Language Instruction. arXiv (2025). https: 

- [253] Yan, G., Zhu, J., Deng, Y., Yang, S., Qiu, R.-Z., Cheng, X., et al.: ManiFlow: A General Robot Manipulation Policy via Consistency Flow Training. arXiv (2025). https: //doi.org/10.48550/arXiv.2509.01819 

- [254] Stone, A., Xiao, T., Lu, Y., Gopalakrishnan, K., Lee, K.-H., Vuong, Q., et al.: Open-World Object Manipulation Using Pre-trained Vision-Language Models. arXiv (2023). https://doi.org/10.48550/arXiv. 2303.00905 

- [255] Liu, Z., Liu, J., Xu, J., Han, N., Gu, C., Chen, H., et al.: MLA: A Multisensory Language-Action Model for Multimodal Understanding and Forecasting in Robotic Manipulation. arXiv (2025). https: //doi.org/10.48550/arXiv.2509.26642 

- [256] Garcia, R., Chen, S., Schmid, C.: Towards Generalizable Vision-Language Robotic Manipulation: A Benchmark and LLM-Guided 3D Policy. In: 2025 IEEE International Conference on Robotics and Automation (ICRA), pp. 8996–9002. IEEE, Atlanta, GA, USA (2025). https://doi.org/ 10.1109/ICRA55743.2025.11127315 

- [257] Guhur, P.-L., Chen, S., Garcia, R., Tapaswi, M., Laptev, I., Schmid, C.: InstructionDriven History-Aware Policies for Robotic Manipulations. arXiv (2022). https://doi. org/10.48550/arXiv.2209.04899 

- [258] Li, P., Chen, Y., Wu, H., Ma, X., Wu, X., Huang, Y., et al.: BridgeVLA: InputOutput Alignment for Efficient 3D Manipulation Learning with Vision-Language Models. arXiv (2025). https://doi.org/10.48550/ arXiv.2506.07961 

- [259] Wang, R., Mao, J., Hsu, J., Zhao, H., Wu, J., Gao, Y.: Programmatically Grounded, Compositionally Generalizable Robotic Manipulation. arXiv (2023). https: //doi.org/10.48550/arXiv.2304.13826 

- [260] Kuang, Y., Ye, J., Geng, H., Mao, J., Deng, C., Guibas, L., et al.: RAM: Retrieval-Based 

55 

Affordance Transfer for Generalizable ZeroShot Robotic Manipulation. arXiv (2024). https://doi.org/10.48550/arXiv.2407.04689 

- [261] Luo, G., Yang, G., Gong, Z., Chen, G., Duan, H., Cui, E., et al.: Visual Embodied Brain: Let Multimodal Large Language Models See, Think, and Control in Spaces. arXiv (2025). https://doi.org/10. 48550/arXiv.2506.00123 

- [262] Zheng, J., Li, J., Liu, D., Zheng, Y., Wang, Z., Ou, Z., et al.: Universal Actions for Enhanced Embodied Foundation Models. arXiv (2025). https://doi.org/10.48550/ arXiv.2501.10105 

- [263] Ma, Y., Chi, D., Wu, S., Liu, Y., Zhuang, Y., Hao, J., et al.: Actra: Optimized Transformer Architecture for Vision-Language-Action Models in Robot Learning. arXiv (2024). https://doi.org/10. 48550/arXiv.2408.01147 

- [264] Goyal, A., Blukis, V., Xu, J., Guo, Y., Chao, Y.-W., Fox, D.: RVT-2: Learning Precise Manipulation from Few Demonstrations. arXiv (2024). https://doi.org/10. 48550/arXiv.2406.08545 

- [265] Niu, Y., Zhou, S., Li, Y., Den, Y., Wang, L.: Time-Unified Diffusion Policy with Action Discrimination for Robotic Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2506.09422 

- [266] Zhang, J., Hu, Y., Guo, Y., Chen, X., Liu, Y., Chen, W., et al.: UniCoD: Enhancing Robot Policy via Unified Continuous and Discrete Representation Learning. arXiv (2025). https://doi. org/10.48550/arXiv.2510.10642 

- [267] Gu, J., Kirmani, S., Wohlhart, P., Lu, Y., Arenas, M.G., Rao, K., et al.: RT-Trajectory: Robotic Task Generalization via Hindsight Trajectory Sketches. arXiv (2023). https: //doi.org/10.48550/arXiv.2311.01977 

- [268] Zhang, J., Wu, S., Luo, X., Wu, H., Gao, L., 

Shen, H.T., et al.: InSpire: Vision-LanguageAction Models with Intrinsic Spatial Reasoning. arXiv (2025). https://doi.org/10. 48550/arXiv.2505.13888 

- [269] Bai, Y., Wang, Z., Liu, Y., Luo, K., Wen, Y., Dai, M., et al.: Learning to See and Act: Task-Aware Virtual View Exploration for Robotic Manipulation. arXiv (2025). https: //doi.org/10.48550/arXiv.2508.05186 

- [270] Wang, L., Chen, X., Zhao, J., He, K.: Scaling Proprioceptive-Visual Learning with Heterogeneous Pre-trained Transformers. arXiv (2024). https://doi.org/10.48550/ arXiv.2409.20537 

- [271] Song, H., Qu, D., Yao, Y., Chen, Q., Lv, Q., Tang, Y., et al.: Hume: Introducing System-2 Thinking in Visual-LanguageAction Model. arXiv (2025). https://doi. org/10.48550/arXiv.2505.21432 

- [272] Stepputtis, S., Campbell, J., Phielipp, M., Lee, S., Baral, C., Amor, H.B.: LanguageConditioned Imitation Learning for Robot Manipulation Tasks. arXiv (2020). https:// doi.org/10.48550/arXiv.2010.12083 

- [273] Ye, S., Jang, J., Jeon, B., Joo, S., Yang, J., Peng, B., et al.: Latent Action Pretraining from Videos. arXiv (2025). https://doi.org/ 10.48550/arXiv.2410.11758 

- [274] Fang, H., Grotz, M., Pumacay, W., Wang, Y.R., Fox, D., Krishna, R., et al.: SAM2Act: Integrating Visual Foundation Model with A Memory Architecture for Robotic Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2501.18564 

- [275] Hu, Y., Guo, Y., Wang, P., Chen, X., Wang, Y.-J., Zhang, J., et al.: Video Prediction Policy: A Generalist Robot Policy with Predictive Visual Representations. arXiv (2025). https://doi.org/10.48550/arXiv.2412.14803 

- [276] Li, H., Feng, Q., Zheng, Z., Feng, J., Chen, Z., Knoll, A.: Language-Guided ObjectCentric Diffusion Policy for Generalizable and Collision-Aware Manipulation. In: 2025 IEEE International Conference on Robotics 

56 

   - and Automation (ICRA), pp. 12834– 12841. IEEE, Atlanta, GA, USA (2025). https://doi.org/10.1109/ICRA55743.2025. 11127231 

- [277] Fan, C., Jia, X., Sun, Y., Wang, Y., Wei, J., Gong, Z., et al.: Interleave-VLA: Enhancing Robot Manipulation with Interleaved Image-Text Instructions. arXiv (2025). https://doi.org/10.48550/arXiv.2505.02152 

- [278] Team, T.L., Barreiros, J., Beaulieu, A., Bhat, A., Cory, R., Cousineau, E., et al.: A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2507.05331 

- [279] Saxena, S., Sharma, M., Kroemer, O.: MResT: Multi-Resolution Sensing for RealTime Control with Vision-Language Models. arXiv (2024). https://doi.org/10.48550/ arXiv.2401.14502 

- [280] Niu, D., Sharma, Y., Xue, H., Biamby, G., Zhang, J., Ji, Z., et al.: Pre-Training Autoregressive Robotic Models with 4D Representations. arXiv (2025). https://doi.org/ 10.48550/arXiv.2502.13142 

- [281] Xu, J., Nie, X.: SPECI: Skill Prompts Based Hierarchical Continual Imitation Learning for Robot Manipulation. arXiv (2025). https://doi.org/10.48550/arXiv.2504.15561 

- [282] Reed, S., Zolna, K., Parisotto, E., Colmenarejo, S.G., Novikov, A., Barth-Maron, G., et al.: A Generalist Agent. arXiv (2022). https://doi.org/10.48550/arXiv.2205.06175 

- [283] Lin, T., Li, G., Zhong, Y., Zou, Y., Du, Y., Liu, J., et al.: Evo-0: Vision-LanguageAction Model with Implicit Spatial Understanding. arXiv (2025). https://doi.org/10. 48550/arXiv.2507.00416 

- [284] Huang, W., Chen, C., Qi, H., Lv, C., Du, Y., Yang, H.: MoTVLA: A Vision-LanguageAction Model with Unified Fast-Slow Reasoning. arXiv (2025). https://doi.org/10. 48550/arXiv.2510.18337 

- [285] Zhang, H., Ding, P., Lyu, S., Peng, Y., Wang, D.: GEVRM: Goal-Expressive Video Generation Model For Robust Visual Manipulation. arXiv (2025). https://doi. org/10.48550/arXiv.2502.09268 

- [286] Wen, J., Zhu, Y., Li, J., Zhu, M., Tang, Z., Wu, K., _et al._ : TinyVLA: Toward Fast, Data-Efficient Vision-LanguageAction Models for Robotic Manipulation. IEEE Robotics and Automation Letters **10** (4), 3988–3995 (2025) https: //doi.org/10.1109/LRA.2025.3544909 

- [287] Yang, Y., Sun, J., Kou, S., Wang, Y., Deng, Z.: LoHoVLA: A Unified Vision-LanguageAction Model for Long-Horizon Embodied Tasks. arXiv (2025). https://doi.org/10. 48550/arXiv.2506.00411 

- [288] Shi, H., Xie, B., Liu, Y., Sun, L., Liu, F., Wang, T., et al.: MemoryVLA: Perceptual-Cognitive Memory in Vision-Language-Action Models for Robotic Manipulation. arXiv (2025). https://doi.org/10.48550/arXiv.2508.19236 

- [289] Liu, S., Wu, L., Li, B., Tan, H., Chen, H., Wang, Z., et al.: RDT-1B: A Diffusion Foundation Model for Bimanual Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2410.07864 

- [290] NVIDIA, Bjorck, J., Casta˜neda, F., Cherniadev, N., Da, X., Ding, R., et al.: GR00T N1: An Open Foundation Model for Generalist Humanoid Robots. arXiv (2025). https: //doi.org/10.48550/arXiv.2503.14734 

- [291] Wu, H., Jing, Y., Cheang, C., Chen, G., Xu, J., Li, X., et al.: Unleashing Large-Scale Video Generative Pre-training for Visual Robot Manipulation. arXiv (2023). https: //doi.org/10.48550/arXiv.2312.13139 

- [292] Jiang, Y., Gupta, A., Zhang, Z., Wang, G., Dou, Y., Chen, Y., et al.: VIMA: General Robot Manipulation with Multimodal Prompts. arXiv (2023). https://doi.org/10. 48550/arXiv.2210.03094 

57 

- [293] Jang, E., Irpan, A., Khansari, M., Kappler, D., Ebert, F., Lynch, C., et al.: BC-Z: Zero-Shot Task Generalization with Robotic Imitation Learning. arXiv (2022). https:// doi.org/10.48550/arXiv.2202.02005 

- [294] Chen, Y., Gu, K., Wen, Y., Zhao, Y., Wang, T., Nie, L.: IntentionVLA: Generalizable and Efficient Embodied Intention Reasoning for Human-Robot Interaction. arXiv (2025). https://doi.org/10.48550/arXiv.2510.07778 

- [295] Shridhar, M., Manuelli, L., Fox, D.: CLIPort: What and Where Pathways for Robotic Manipulation. arXiv (2021). https: //doi.org/10.48550/arXiv.2109.12098 

- [296] Xia, S., Fang, H., Lu, C., Fang, H.-S.: CAGE: Causal Attention Enables DataEfficient Generalizable Robotic Manipulation. arXiv (2024). https://doi.org/10. 48550/arXiv.2410.14974 

- [297] Wang, S., You, J., Hu, Y., Li, J., Gao, Y.: SKIL: Semantic Keypoint Imitation Learning for Generalizable Data-efficient Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2501.14400 

- [298] Yang, D., Zhao, Z., Liu, Y.: ARVRM: Imitating Human Motions for Visual Robot Manipulation with Analogical Reasoning. arXiv (2025). https://doi.org/10.48550/arXiv.2508.07626 

- [299] Sun, L., Xie, B., Liu, Y., Shi, H., Wang, T., Cao, J.: GeoVLA: Empowering 3D Representations in Vision-Language-Action Models. arXiv (2025). https://doi.org/10.48550/ arXiv.2508.09071 

- [300] Liang, Z., Mu, Y., Ma, H., Tomizuka, M., Ding, M., Luo, P.: SkillDiffuser: Interpretable Hierarchical Planning via Skill Abstractions in Diffusion-Based Task Execution. In: 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 16467–16476. IEEE, Seattle, WA, USA (2024). https://doi.org/10.1109/ CVPR52733.2024.01558 

- [301] Chen, H., Guo, J., Wang, B., Zhang, T., 

Huang, X., Zheng, B., et al.: Goal-VLA: Image-Generative VLMs as Object-Centric World Models Empowering Zero-shot Robot Manipulation. arXiv (2025). https://doi. org/10.48550/arXiv.2506.23919 

- [302] Lin, J., Taherin, A., Akbari, A., Akbari, A., Lu, L., Chen, G., et al.: VOTE: VisionLanguage-Action Optimization with Trajectory Ensemble Voting. arXiv (2025). https: //doi.org/10.48550/arXiv.2507.05116 

- [303] Wu, S., Zhu, Y., Huang, Y., Zhu, K., Gu, J., Yu, J., et al.: AffordDP: Generalizable Diffusion Policy with Transferable Affordance. arXiv (2025). https://doi.org/ 10.48550/arXiv.2412.03142 

- [304] Ranasinghe, K., Li, X., Nguyen, E.-R., Mata, C., Park, J., Ryoo, M.S.: Pixel Motion as Universal Representation for Robot Control. arXiv (2025). https://doi. org/10.48550/arXiv.2505.07817 

- [305] Cheang, C.-L., Chen, G., Jing, Y., Kong, T., Li, H., Li, Y., et al.: GR-2: A Generative Video-Language-Action Model with Web-Scale Knowledge for Robot Manipulation. arXiv (2024). https://doi.org/10. 48550/arXiv.2410.06158 

- [306] Reuss, M., Zhou, H., R¨uhle, M., Ya˘gmurlu, ¨O.E., Otto, F., Lioutikov, R.: FLOWER: Democratizing Generalist Robot Policies with Efficient Vision-Language-Action Flow Policies. arXiv (2025). https://doi.org/10. 48550/arXiv.2509.04996 

- [307] Chi, X., Ge, K., Liu, J., Zhou, S., Jia, P., He, Z., et al.: MinD: Learning A Dual-System World Model for Real-Time Planning and Implicit Risk Analysis. arXiv (2025). https: //doi.org/10.48550/arXiv.2506.18897 

- [308] Chen, Y., Ge, Y., Tang, W., Li, Y., Ge, Y., Ding, M., et al.: Moto: Latent Motion Token as the Bridging Language for Learning Robot Manipulation from Videos. arXiv (2025). https://doi.org/10. 48550/arXiv.2412.04445 

- [309] Mandi, Z., Bharadhwaj, H., Moens, 

58 

   - V., Song, S., Rajeswaran, A., Kumar, V.: CACTI: A Framework for Scalable Multi-Task Multi-Scene Visual Imitation Learning. arXiv (2023). https://doi.org/10.48550/arXiv.2212.05711 

- [310] Kang, J.H., Joshi, S., Dhanaraj, N., Gupta, S.K.: Task-Context-Aware Diffusion Policy with Language Guidance for Multi-task Disassembly. In: 2025 IEEE 21st International Conference on Automation Science and Engineering (CASE), pp. 609–616. IEEE, Los Angeles, CA, USA (2025). https://doi. org/10.1109/CASE58245.2025.11163846 

- [311] Shentu, Y., Wu, P., Rajeswaran, A., Abbeel, P.: From LLMs to Actions: Latent Codes as Bridges in Hierarchical Robot Control. arXiv (2025). https://doi.org/10. 48550/arXiv.2405.04798 

- [312] Argus, M., Bratulic, J., Masnavi, H., Velikanov, M., Heppert, N., Valada, A., et al.: cVLA: Towards Efficient CameraSpace VLAs. arXiv (2025). https://doi.org/ 10.48550/arXiv.2507.02190 

- [313] Cheang, C., Chen, S., Cui, Z., Hu, Y., Huang, L., Kong, T., et al.: GR-3 Technical Report. arXiv (2025). https://doi.org/ 10.48550/arXiv.2507.15493 

- [314] Xiong, Z., Li, K., Wang, Z., Jackson, M., Foerster, J., Whiteson, S.: HyperVLA: Efficient Inference in Vision-Language-Action Models via Hypernetworks. arXiv (2025). https://doi.org/10.48550/arXiv.2510.04898 

- [315] Chen, A., Yang, Y., Zhu, Z., Xu, K., Zhou, Z., Xiong, R., et al.: Toward Embodiment Equivariant Vision-Language-Action Policy. arXiv (2025). https://doi.org/10. 48550/arXiv.2509.14630 

- [316] Ji, Y., Tan, H., Shi, J., Hao, X., Zhang, Y., Zhang, H., et al.: RoboBrain: A Unified Brain Model for Robotic Manipulation from Abstract to Concrete. arXiv (2025). https://doi.org/10.48550/arXiv.2502.21257 

- [317] Mao, J., Guan, J., Tang, Y., Hu, Q., Li, Z., Yu, J., et al.: OmniD: Generalizable Robot 

Manipulation Policy via Image-Based BEV Representation. arXiv (2025). https://doi. org/10.48550/arXiv.2508.11898 

- [318] Yu, J., Liu, H., Yu, Q., Ren, J., Hao, C., Ding, H., et al.: ForceVLA: Enhancing VLA Models with a Force-aware MoE for Contact-rich Manipulation. arXiv (2025). https://doi.org/10.48550/arXiv.2505.22159 

- [319] Chen, J., Zhao, W., Meng, Z., Mao, D., Song, R., Pan, W., et al.: VisionLanguage Model Predictive Control for Manipulation Planning and Trajectory Generation. arXiv (2025). https://doi.org/10. 48550/arXiv.2504.05225 

- [320] Collins, J.A., Cheng, L., Aneja, K., Wilcox, A., Joffe, B., Garg, A.: AMPLIFY: Actionless Motion Priors for Robot Learning from Videos. arXiv (2025). https://doi.org/10. 48550/arXiv.2506.14198 

- [321] Vo, T.V., Nguyen, T.Q., Nguyen, K.M., Nguyen, D.H.M., Vu, M.N.: ReFineVLA: Reasoning-Aware Teacher-Guided Transfer Fine-Tuning. arXiv (2025). https://doi.org/ 10.48550/arXiv.2505.19080 

- [322] Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., et al.: CogACT: A Foundational Vision-Language-Action Model for Synergizing Cognition and Action in Robotic Manipulation. arXiv (2024). https://doi.org/10.48550/arXiv.2411.19650 

- [323] Zhang, Z., Zheng, K., Chen, Z., Jang, J., Li, Y., Han, S., et al.: GRAPE: Generalizing Robot Policy via Preference Alignment. arXiv (2025). https://doi.org/ 10.48550/arXiv.2411.19309 

- [324] Yan, G., Wu, Y.-H., Wang, X.: DNAct: Diffusion Guided Multi-Task 3D Policy Learning. arXiv (2024). https://doi.org/10. 48550/arXiv.2403.04115 

- [325] Yang, J., Tan, R., Wu, Q., Zheng, R., Peng, B., Liang, Y., et al.: Magma: A Foundation Model for Multimodal AI Agents. arXiv (2025). https://doi.org/10. 48550/arXiv.2502.13130 

59 

- [326] Cai, S., Zhang, B., Wang, Z., Lin, H., Ma, X., Liu, A., et al.: GROOT-2: Weakly Supervised Multi-Modal Instruction Following Agents. arXiv (2024). https://doi.org/ 10.48550/arXiv.2412.10410 

- [327] Liu, Z., Gu, Y., Zheng, S., Fu, Y., Xue, X., Jiang, Y.-G.: TriVLA: A Triple-SystemBased Unified Vision-Language-Action Model with Episodic World Modeling for General Robot Control. arXiv (2025). https://doi.org/10.48550/arXiv.2507.01424 

- [328] Wang, B., Sridhar, N., Feng, C., Merwe, M.V., Fishman, A., Fazeli, N., et al.: This&That: LanguageGesture Controlled Video Generation for Robot Planning. arXiv (2025). https://doi.org/10.48550/arXiv.2407.05530 

- [329] Hu, S., Nagai, T., Horii, T.: TARAD: Task-Aware Robot Affordance-Centric Diffusion Policy Learned From LLMGenerated Demonstrations. IEEE Robotics and Automation Letters **10** (10), 10122–10129 (2025) https: //doi.org/10.1109/LRA.2025.3598998 

- [330] Yu, A., Mooney, R.J.: Using Both Demonstrations and Language Instructions to Efficiently Learn Robotic Tasks. arXiv (2023). https://doi.org/10.48550/arXiv.2210.04476 

- [331] Shao, L., Migimatsu, T., Zhang, Q., Yang, K., Bohg, J.: Concept2Robot: Learning Manipulation Concepts from Instructions and Human Demonstrations (2020) 

- [332] Jia, X., Wang, Q., Wang, A., Wang, H.A., Gyenes, B., Gospodinov, E., et al.: PointMapPolicy: Structured Point Cloud Processing for MultiModal Imitation Learning. arXiv (2025). https://doi.org/10.48550/arXiv.2510.20406 

- [333] Dalal, M., Liu, M., Talbott, W., Chen, C., Pathak, D., Zhang, J., _et al._ : Local Policies Enable Zero-Shot Long-Horizon Manipulation. In: 2025 IEEE International Conference on Robotics and Automation (ICRA), pp. 13875–13882. IEEE, Atlanta, GA, USA (2025). https://doi.org/10.1109/ 

ICRA55743.2025.11128407 

- [334] Chen, H., Sun, B., Zhang, A., Pollefeys, M., Leutenegger, S.: VidBot: Learning Generalizable 3D Actions from In-the-Wild 2D Human Videos for Zero-Shot Robotic Manipulation. arXiv (2025). https://doi. org/10.48550/arXiv.2503.07135 

- [335] Ahn, M., Brohan, A., Brown, N., Chebotar, Y., Cortes, O., David, B., et al.: Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. arXiv (2022). https:// doi.org/10.48550/arXiv.2204.01691 

- [336] Chen, S., Liu, J., Qian, S., Jiang, H., Li, L., Zhang, R., et al.: AC-DiT: Adaptive Coordination Diffusion Transformer for Mobile Manipulation. arXiv (2025). https: //doi.org/10.48550/arXiv.2507.01961 

- [337] Zhao, W., Ding, P., Zhang, M., Gong, Z., Bai, S., Zhao, H., et al.: VLAS: Vision-Language-Action Model With Speech Instructions For Customized Robot Manipulation. arXiv (2025). https://doi.org/10.48550/arXiv.2502.13508 

- [338] Myers, V., Zheng, B.C., Mees, O., Levine, S., Fang, K.: Policy Adaptation via Language Optimization: Decomposing Tasks for Few-Shot Imitation. arXiv (2024). https:// doi.org/10.48550/arXiv.2408.16228 

- [339] Zheng, R., Liang, Y., Huang, S., Gao, J., Daum´e, H., Kolobov, A., et al.: TraceVLA: Visual Trace Prompting Enhances SpatialTemporal Awareness for Generalist Robotic Policies. arXiv (2025). https://doi.org/10. 48550/arXiv.2412.10345 

- [340] Chen, X., Wei, H., Zhang, P., Zhang, C., Wang, K., Guo, Y., et al.: Villa-X: Enhancing Latent Action Modeling in VisionLanguage-Action Models. arXiv (2025). https://doi.org/10.48550/arXiv.2507.23682 

- [341] Wang, Y., Zhang, Y., Huo, M., Tian, R., Zhang, X., Xie, Y., et al.: Sparse Diffusion Policy: A Sparse, Reusable, and Flexible Policy for Robot Learning. arXiv (2024). https://doi.org/10.48550/arXiv.2407.01531 

60 

- [342] Spiridonov, A., Zaech, J.-N., Nikolov, N., Gool, L.V., Paudel, D.P.: Generalist Robot Manipulation beyond Action Labeled Data. arXiv (2025). https://doi. org/10.48550/arXiv.2509.19958 

- [343] Bharadhwaj, H., Dwibedi, D., Gupta, A., Tulsiani, S., Doersch, C., Xiao, T., et al.: Gen2Act: Human Video Generation in Novel Scenarios Enables Generalizable Robot Manipulation. arXiv (2024). https: //doi.org/10.48550/arXiv.2409.16283 

- [344] Yan, F., Liu, F., Zheng, L., Zhong, Y., Huang, Y., Guan, Z., et al.: RoboTronMani: All-in-One Multimodal Large Model for Robotic Manipulation. arXiv (2025). https://doi.org/10.48550/arXiv.2412.07215 

- [345] Zhang, J., Bai, C., He, H., Xia, W., Wang, Z., Zhao, B., et al.: SAM-E: Leveraging Visual Foundation Model with Sequence Imitation for Embodied Manipulation. arXiv (2024). https://doi.org/10. 48550/arXiv.2405.19586 

- [346] Liu, J., Chen, H., An, P., Liu, Z., Zhang, R., Gu, C., et al.: HybridVLA: Collaborative Diffusion and Autoregression in a Unified Vision-Language-Action Model. arXiv (2025). https://doi.org/10. 48550/arXiv.2503.10631 

- [347] Yang, J., Shi, Y., Zhu, H., Liu, M., Ma, K., Wang, Y., et al.: CoMo: Learning Continuous Latent Motion from Internet Videos for Scalable Robot Learning. arXiv (2025). https://doi.org/10.48550/arXiv.2505.17006 

- [348] Zhang, J., Guo, Y., Chen, X., Wang, Y.J., Hu, Y., Shi, C., et al.: HiRT: Enhancing Robotic Control with Hierarchical Robot Transformers. arXiv (2025). https://doi. org/10.48550/arXiv.2410.05273 

- [349] Zheng, R., Wang, J., Reed, S., Bjorck, J., Fang, Y., Hu, F., et al.: FLARE: Robot Learning with Implicit World Modeling. arXiv (2025). https://doi.org/10. 48550/arXiv.2505.15659 

- [350] Tian, Y., Yang, S., Zeng, J., Wang, P., 

Lin, D., Dong, H., et al.: Predictive Inverse Dynamics Models Are Scalable Learners for Robotic Manipulation. arXiv (2024). https: //doi.org/10.48550/arXiv.2412.15109 

- [351] Wen, J., Zhu, M., Liu, J., Liu, Z., Yang, Y., Zhang, L., et al.: dVLA: Diffusion VisionLanguage-Action Model with Multimodal Chain-of-Thought. arXiv (2025). https:// doi.org/10.48550/arXiv.2509.25681 

- [352] Yang, J., Tan, W., Jin, C., Yao, K., Liu, B., Fu, J., et al.: Transferring Foundation Models for Generalizable Robotic Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2306.05716 

- [353] Hou, Z., Zhang, T., Xiong, Y., Duan, H., Pu, H., Tong, R., et al.: Dita: Scaling Diffusion Transformer for Generalist VisionLanguage-Action Policy. arXiv (2025). https://doi.org/10.48550/arXiv.2503.19757 

- [354] Yao, Y., Liu, S., Song, H., Qu, D., Chen, Q., Ding, Y., et al.: Think Small, Act Big: Primitive Prompt Learning for Lifelong Robot Manipulation (2025) https://doi.org/ 10.48550/arXiv.2504.00420 

- [355] Karamcheti, S., Nair, S., Chen, A., Kollar, T., Finn, C., Sadigh, D., _et al._ : Language-Driven Representation Learning for Robotics. In: Robotics: Science and Systems XIX. Robotics: Science and Systems Foundation, ??? (2023). https://doi.org/10. 15607/RSS.2023.XIX.032 

- [356] Jiang, Y., Huang, S., Xue, S., Zhao, Y., Cen, J., Leng, S., et al.: RynnVLA-001: Using Human Demonstrations to Improve Robot Manipulation. arXiv (2025). https: //doi.org/10.48550/arXiv.2509.15212 

- [357] Lan, Z., Mao, W., Li, H., Wang, L., Wang, T., Fan, H., et al.: BFA: Best-Feature-Aware Fusion for Multi-View Fine-grained Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2502.11161 

- [358] Reuss, M., Ya˘gmurlu, ¨O.E., Wenzel, F., Lioutikov, R.: Multimodal Diffusion Transformer: Learning Versatile Behavior from 

61 

Multimodal Goals. arXiv (2024). https:// doi.org/10.48550/arXiv.2407.05996 

- [359] Meng, Y., Bing, Z., Yao, X., Chen, K., Huang, K., Gao, Y., et al.: Preserving and Combining Knowledge in Robotic Lifelong Reinforcement Learning. In Review (2024). https://doi.org/10. 21203/rs.3.rs-4353532/v1 

- [360] Ko, P.-C., Mao, J., Du, Y.: LEARNING TO ACT FROM ACTIONLESS VIDEOS THROUGH DENSE CORRESPONDENCES (2024) 

- [361] Shafiullah, N.M.M., Rai, A., Etukuru, H., Liu, Y., Misra, I., Chintala, S., et al.: On Bringing Robots Home. arXiv (2023). https: //doi.org/10.48550/arXiv.2311.16098 

- [362] Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., et al.: SpatialVLA: Exploring Spatial Representations for Visual-LanguageAction Model. arXiv (2025). https://doi. org/10.48550/arXiv.2501.15830 

- [363] Deng, S., Yan, M., Wei, S., Ma, H., Yang, Y., Chen, J., et al.: GraspVLA: A Grasping Foundation Model Pre-trained on Billionscale Synthetic Action Data. arXiv (2025). https://doi.org/10.48550/arXiv.2505.03233 

- [364] Yang, R., Chen, G., Wen, C., Gao, Y.: FP3: A 3D Foundation Policy for Robotic Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2503.08950 

- [365] Li, Q.: Task Reconstruction and Extrapolation for $ _π_ ~~0~~ $ Using Text Latent. arXiv (2025). https://doi.org/10.48550/arXiv. 2505.03500 

- [366] Fu, M., Huang, H., Datta, G., Chen, L.Y., Panitch, W., Liu, F., _et al._ : ICRT: InContext Imitation Learning via Next-Token Prediction. In: 2025 IEEE International Conference on Robotics and Automation (ICRA), pp. 5937–5944. IEEE, Atlanta, GA, USA (2025). https://doi.org/10.1109/ ICRA55743.2025.11128272 

Karri, R., Khorrami, F.: 3D CAVLA: Leveraging Depth and 3D Context to Generalize Vision Language Action Models for Unseen Tasks. arXiv (2025). https://doi. org/10.48550/arXiv.2505.05800 

   - [368] Zhao, W., Li, G., Gong, Z., Ding, P., Zhao, H., Wang, D.: Unveiling the Potential of Vision-Language-Action Models with Open-Ended Multimodal Instructions. arXiv (2025). https://doi.org/10.48550/arXiv.2505.11214 

   - [369] Huang, J., Yong, S., Ma, X., Linghu, X., Li, P., Wang, Y., et al.: An Embodied Generalist Agent in 3D World. arXiv (2024). https://doi.org/10.48550/arXiv.2311.12871 

   - [370] Li, W., Zhang, R., Shao, R., He, J., Nie, L.: CogVLA: CognitionAligned Vision-Language-Action Model via Instruction-Driven Routing & Sparsification. arXiv (2025). https://doi.org/10.48550/arXiv.2508.21046 

   - [371] Song, W., Zhou, Z., Zhao, H., Chen, J., Ding, P., Yan, H., et al.: ReconVLA: Reconstructive Vision-Language-Action Model as Effective Robot Perceiver. arXiv (2025). https://doi.org/10.48550/arXiv.2508.10333 

   - [372] Radosavovic, I., Xiao, T., James, S., Abbeel, P., Malik, J., Darrell, T.: Real-World Robot Learning with Masked Visual Pretraining. arXiv (2022). https://doi.org/10. 48550/arXiv.2210.03109 

   - [373] Wen, J., Zhu, Y., Li, J., Tang, Z., Shen, C., Feng, F.: DexVLA: Vision-Language Model with Plug-In Diffusion Expert for General Robot Control. arXiv (2025). https://doi. org/10.48550/arXiv.2502.05855 

   - [374] Mees, O., Borja-Diaz, J., Burgard, W.: Grounding Language with Visual Affordances over Unstructured Data. In: 2023 IEEE International Conference on Robotics and Automation (ICRA), pp. 11576–11582. IEEE, London, United Kingdom (2023). https://doi.org/10.1109/ICRA48891.2023. 10160396 

- [367] Bhat, V., Lan, Y.-H., Krishnamurthy, P., 

62 

- [375] Ze, Y., Zhang, G., Zhang, K., Hu, C., Wang, M., Xu, H.: 3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations. arXiv (2024). https:// doi.org/10.48550/arXiv.2403.03954 

- [376] Luo, H., Feng, Y., Zhang, W., Zheng, S., Wang, Y., Yuan, H., et al.: Being-H0: Vision-Language-Action Pretraining from Large-Scale Human Videos. arXiv (2025). https://doi.org/10.48550/arXiv.2507.15597 

- [377] Fang, H., Wang, C., Wang, Y., Chen, J., Xia, S., Lv, J., et al.: AirExo-2: Scaling up Generalizable Robotic Imitation Learning with Low-Cost Exoskeletons. arXiv (2025). https: //doi.org/10.48550/arXiv.2503.03081 

- [378] Shridhar, M., Manuelli, L., Fox, D.: Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation. arXiv (2022). https://doi.org/10.48550/arXiv.2209.05451 

- [379] Bi, H., Wu, L., Lin, T., Tan, H., Su, Z., Su, H., et al.: H-RDT: Human Manipulation Enhanced Bimanual Robotic Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2507.23523 

- [380] Yang, J., Zhu, H., Wang, Y., Wu, G., He, T., Wang, L.: Tra-MoE: Learning Trajectory Prediction Model from Multiple Domains for Adaptive Policy Conditioning. arXiv (2025). https://doi.org/10. 48550/arXiv.2411.14519 

- [381] Zhen, H., Qiu, X., Chen, P., Yang, J., Yan, X., Du, Y., et al.: 3D-VLA: A 3D Vision-Language-Action Generative World Model. arXiv (2024). https://doi.org/10. 48550/arXiv.2403.09631 

- [382] Ito, H., Ichiwara, H., Yamamoto, K., Mori, H., Ogata, T.: Integrated Learning of Robot Motion and Sentences: Real-Time Prediction of Grasping Motion and Attention based on Language Instructions. In: 2022 International Conference on Robotics and Automation (ICRA), pp. 5404–5410. IEEE, Philadelphia, PA, USA (2022). https://doi. org/10.1109/ICRA46639.2022.9811815 

- [383] Wang, Y., Ding, P., Li, L., Cui, C., Ge, Z., Tong, X., et al.: VLA-Adapter: An Effective Paradigm for Tiny-Scale Vision-LanguageAction Model. arXiv (2025). https://doi. org/10.48550/arXiv.2509.09372 

- [384] Mees, O.: What Matters in Language Conditioned Robotic Imitation Learning Over Unstructured Data (2022) 

- [385] Kobayashi, M., Buamanee, T.: Bi-VLA: Bilateral Control-Based Imitation Learning via Vision-Language Fusion for Action Generation. arXiv (2025). https://doi.org/10. 48550/arXiv.2509.18865 

- [386] Lyu, J., Li, Z., Shi, X., Xu, C., Wang, Y., Wang, H.: DyWA: Dynamics-adaptive World Action Model for Generalizable Non-prehensile Manipulation. arXiv (2025). https://doi.org/10.48550/arXiv.2503.16806 

- [387] Hou, Z., Zhang, T., Xiong, Y., Pu, H., Zhao, C., Tong, R., et al.: Diffusion Transformer Policy. arXiv (2025). https://doi. org/10.48550/arXiv.2410.15959 

- [388] Staroverov, A., Gorodetsky, A.S., Krishtopik, A.S., Izmesteva, U.A., Yudin, D.A., Kovalev, A.K., _et al._ : Fine-Tuning Multimodal Transformer Models for Generating Actions in Virtual and Real Environments. IEEE Access **11** , 130548–130559 (2023) https: //doi.org/10.1109/ACCESS.2023.3334791 

- [389] Bousmalis, K., Vezzani, G., Rao, D., Devin, C., Lee, A.X., Bauza, M., et al.: RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation. arXiv (2023). https: //doi.org/10.48550/arXiv.2306.11706 

- [390] Chen, X., Guo, J., He, T., Zhang, C., Zhang, P., Yang, D.C., et al.: IGOR: Image-GOal Representations Are the Atomic Control Units for Foundation Models in Embodied AI. arXiv (2024). https://doi.org/10.48550/ arXiv.2411.00785 

- [391] Zhao, T.Z., Kumar, V., Levine, S., Finn, C.: Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. arXiv (2023). 

63 

https://doi.org/10.48550/arXiv.2304.13705 

- [392] Dong, Y., Ge, H., Zeng, Y., Zhang, J., Tian, B., Zhu, H., _et al._ : ImitDiff: Transferring Foundation-Model Priors for DistractionRobust Visuomotor Policy. IEEE Robotics and Automation Letters **10** (11), 12125– 12132 (2025) https://doi.org/10.1109/LRA. 2025.3619835 

- [393] Ren, P., Zhang, K., Zheng, H., Li, Z., Wen, Y., Zhu, F., et al.: Surfer: Progressive Reasoning with World Models for Robotic Manipulation. arXiv (2024). https://doi. org/10.48550/arXiv.2306.11335 

- [394] Mazzaglia, P., Sancaktar, C., Peschl, M., Dijkman, D.: Hybrid Training for VisionLanguage-Action Models. arXiv (2025). https://doi.org/10.48550/arXiv.2510.00600 

- [395] Kim, M.J., Finn, C., Liang, P.: Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success. arXiv (2025). https: //doi.org/10.48550/arXiv.2502.19645 

- [396] Huang, K., Li, T., Liu, Y., Zhang, Z., Wang, J., Han, L.: VLM-TDP: VLM-guided Trajectory-conditioned Diffusion Policy for Robust LongHorizon Manipulation. arXiv (2025). https://doi.org/10.48550/arXiv.2507.04524 

- [397] Myers, V., He, A., Fang, K., Walke, H., Hansen-Estruch, P., Cheng, C.-A., et al.: Goal Representations for Instruction Following: A Semi-Supervised Language Interface to Control. arXiv (2023). https://doi.org/ 10.48550/arXiv.2307.00117 

- [398] Goyal, A., Xu, J., Guo, Y., Blukis, V., Chao, Y.-W., Fox, D.: RVT: Robotic View Transformer for 3D Object Manipulation. arXiv (2023). https://doi.org/10. 48550/arXiv.2306.14896 

- [399] Liu, H., Lee, L., Lee, K., Abbeel, P.: Instruction-Following Agents with Multimodal Transformer. arXiv (2023). https:// doi.org/10.48550/arXiv.2210.13431 

- [400] Ma, J., Qin, Y., Li, Y., Liao, X., Guo, Y., 

Zhang, R.: CDP: Towards Robust Autoregressive Visuomotor Policy Learning via Causal Diffusion. arXiv (2025). https://doi. org/10.48550/arXiv.2506.14769 

- [401] Fan, S., Yang, Q., Liu, Y., Wu, K., Che, Z., Liu, Q., et al.: Diffusion Trajectory-Guided Policy for Long-Horizon Robot Manipulation (2025) https://doi.org/10.1109/LRA. 2025.3619794 

- [402] Zhong, Z., Yan, H., Li, J., Liu, X., Gong, X., Zhang, T., et al.: FlowVLA: Visual Chain of Thought-based Motion Reasoning for Vision-Language-Action Models. arXiv (2025). https://doi.org/10.48550/ arXiv.2508.18269 

- [403] Tan, X., Yang, Y., Ye, P., Zheng, J., Bai, B., Wang, X., et al.: Think Twice, Act Once: Token-Aware Compression and Action Reuse for Efficient Inference in VisionLanguage-Action Models. arXiv (2025). https://doi.org/10.48550/arXiv.2505.21200 

- [404] Li, J., Wang, Z., Zheng, J., Zhou, X., Wang, G., Song, G., et al.: Robo-MUTUAL: Robotic Multimodal Task Specification via Unimodal Learning. arXiv (2024). https:// doi.org/10.48550/arXiv.2410.01529 

- [405] Gao, C., Zhang, H., Xu, Z., Cai, Z., Shao, L.: FLIP: Flow-Centric Generative Planning as General-Purpose Manipulation World Model. arXiv (2025). https://doi.org/10. 48550/arXiv.2412.08261 

- [406] Deng, Y., Mo, K., Xia, C., Wang, X.: Learning Language-Conditioned Deformable Object Manipulation with Graph Dynamics. In: 2024 IEEE International Conference on Robotics and Automation (ICRA), pp. 7508–7514. IEEE, Yokohama, Japan (2024). https://doi.org/10.1109/ICRA57147.2024. 10610890 

- [407] Song, W., Chen, J., Ding, P., Zhao, H., Zhao, W., Zhong, Z., et al.: Accelerating Vision-Language-Action Model Integrated with Action Chunking via Parallel Decoding. arXiv (2025). https://doi.org/10. 48550/arXiv.2503.02310 

64 

- [408] Yang, J., Glossop, C., Bhorkar, A., Shah, D., Vuong, Q., Finn, C., et al.: Pushing the Limits of Cross-Embodiment Learning for Manipulation and Navigation. arXiv (2024). https://doi.org/10.48550/arXiv.2402.19432 

- [409] Doshi, R., Walke, H., Mees, O., Dasari, S., Levine, S.: Scaling CrossEmbodied Learning: One Policy for Manipulation, Navigation, Locomotion and Aviation. arXiv (2024). https://doi.org/10.48550/arXiv.2408.11812 

- [410] Zhang, H., Zhuang, Z., Zhao, H., Ding, P., Lu, H., Wang, D.: ReinboT: Amplifying Robot Visual-Language Manipulation with Reinforcement Learning. arXiv (2025). https://doi.org/10.48550/arXiv.2505.07395 

- [411] Shen, W., Liu, Y., Wu, Y., Liang, Z., Gu, S., Wang, D., et al.: Expertise Need Not Monopolize: Action-Specialized Mixture of Experts for Vision-Language-Action Learning. arXiv (2025). https://doi.org/10. 48550/arXiv.2510.14300 

- [412] Griebenow, S.: Open-Vocabulary Robotic Object Manipulation using Foundation Models (2025) 

- [413] Ma, T., Zhou, J., Wang, Z., Qiu, R., Liang, J.: Contrastive Imitation Learning for Language-guided Multi-Task Robotic Manipulation. arXiv (2024). https://doi. org/10.48550/arXiv.2406.09738 

- [414] Ren, P., Zhang, K., Zheng, H., Li, Z., Wen, Y., Zhu, F., et al.: Surfer: A World Model-Based Framework for VisionLanguage Robot Manipulation (2025) 

- [415] He, H., Bai, C., Pan, L., Zhang, W., Zhao, B., Li, X.: Learning an Actionable Discrete Diffusion Policy via Large-Scale Actionless Video Pre-Training. arXiv (2024). https:// doi.org/10.48550/arXiv.2402.14407 

- [416] Wen, J., Zhu, Y., Zhu, M., Li, J., Xu, Z., Che, Z., et al.: Object-Centric Instruction Augmentation for Robotic Manipulation. arXiv (2024). https://doi.org/10. 48550/arXiv.2401.02814 

- [417] Thomas, G., Cheng, C.-A., Loynd, R., Frujeri, F.V., Vineet, V., Jalobeanu, M., et al.: PLEX: Making the Most of the Available Data for Robotic Manipulation Pretraining. arXiv (2023). https://doi.org/10. 48550/arXiv.2303.08789 

- [418] Huang, S., Chen, L., Zhou, P., Chen, S., Jiang, Z., Hu, Y., et al.: EnerVerse: Envisioning Embodied Future Space for Robotics Manipulation. arXiv (2025). https://doi. org/10.48550/arXiv.2501.01895 

- [419] Zhang, X., Liu, Y., Chang, H., Schramm, L., Boularias, A.: Autoregressive Action Sequence Learning for Robotic Manipulation. arXiv (2025). https://doi.org/10. 48550/arXiv.2410.03132 

- [420] Huang, H., Chen, X., Chen, Y., Li, H., Han, X., Wang, Z., et al.: RoboGround: Robotic Manipulation with Grounded Vision-Language Priors. arXiv (2025). https://doi.org/10.48550/arXiv.2504.21530 

- [421] Lei, Y., Mao, S., Zhou, S., Zhang, H., Li, X., Luo, P.: Dynamic Mixture of Progressive Parameter-Efficient Expert Library for Lifelong Robot Learning. arXiv (2025). https: //doi.org/10.48550/arXiv.2506.05985 

- [422] Zhu, M., Zhu, Y., Li, J., Zhou, Z., Wen, J., Liu, X., et al.: ObjectVLA: End-to-End Open-World Object Manipulation Without Demonstration. arXiv (2025). https://doi. org/10.48550/arXiv.2502.19250 

- [423] Liu, F., Yan, F., Zheng, L., Feng, C., Huang, Y., Ma, L.: RoboUniView: Visual-Language Model with Unified View Representation for Robotic Manipulation. arXiv (2024). https: //doi.org/10.48550/arXiv.2406.18977 

- [424] Wen, Y., Gu, K., Liu, H., Zhao, Y., Wang, T., Fan, H., et al.: ROSA: Harnessing Robot States for Vision-Language and Action Alignment. arXiv (2025). https:// doi.org/10.48550/arXiv.2506.13679 

- [425] Zhao, Q., Lu, Y., Kim, M.J., Fu, Z., Zhang, 

65 

Z., Wu, Y., et al.: CoT-VLA: Visual Chainof-Thought Reasoning for Vision-LanguageAction Models. arXiv (2025). https://doi. org/10.48550/arXiv.2503.22020 

- [426] Tian, J., Wang, L., Zhou, S., Wang, S., Li, J., Sun, H., _et al._ : PDFactor: Learning Tri-Perspective View Policy Diffusion Field for Multi-Task Robotic Manipulation. In: 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 15757–15767. IEEE, Nashville, TN, USA (2025). https://doi.org/10.1109/ CVPR52734.2025.01469 

- [427] Liu, I.-C.A., He, S., Seita, D., Sukhatme, G.: VoxAct-B: Voxel-Based Acting and Stabilizing Policy for Bimanual Manipulation. arXiv (2024). https://doi.org/10. 48550/arXiv.2407.04152 

- [428] Fan, Y., Ding, P., Bai, S., Tong, X., Zhu, Y., Lu, H., et al.: Long-VLA: Unleashing Long-Horizon Capability of Vision Language Action Model for Robot Manipulation (2025) https://doi.org/10.48550/arXiv. 2508.19958 

- [429] Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., _et al._ : Octo: An Open-Source Generalist Robot Policy. In: Robotics: Science and Systems XX. Robotics: Science and Systems Foundation, ??? (2024). https://doi.org/10.15607/RSS. 2024.XX.090 

- [430] Caesar, A., ¨Ozdemir, O., Weber, C., Wermter, S.: Enabling action crossmodality for a pretrained large language model. Natural Language Processing Journal **7** , 100072 (2024) https://doi.org/10.1016/j.nlp.2024. 100072 

- [431] Ge, Y., Macaluso, A., Li, L.E., Luo, P., Wang, X.: Policy Adaptation from Foundation Model Feedback. In: 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 19059–19069. IEEE, Vancouver, BC, Canada (2023). https: //doi.org/10.1109/CVPR52729.2023.01827 

- [432] Ding, P., Ma, J., Tong, X., Zou, B., Luo, X., Fan, Y., et al.: Humanoid-VLA: Towards Universal Humanoid Control with Visual Integration. arXiv (2025). https://doi.org/ 10.48550/arXiv.2502.14795 

- [433] Wang, S., Liu, S., Wang, W., Shan, J., Fang, B.: RoboBERT: An End-to-end Multimodal Robotic Manipulation Model. arXiv (2025). https://doi.org/10.48550/arXiv.2502.07837 

- [434] Zhu, R., Sun, E., Huang, G., Celiktutan, O.: Efficient Continual Adaptation of Pretrained Robotic Policy with Online MetaLearned Adapters. arXiv (2025). https:// doi.org/10.48550/arXiv.2503.18684 

- [435] Yang, R., Yu, Q., Wu, Y., Yan, R., Li, B., Cheng, A.-C., et al.: EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos. arXiv (2025). https: //doi.org/10.48550/arXiv.2507.12440 

- [436] Silva, A., Moorman, N., Silva, W., Zaidi, Z., Gopalan, N., Gombolay, M.: LanConLearn: Learning With Language to Enable Generalization in Multi-Task Manipulation. IEEE Robotics and Automation Letters **7** (2), 1635–1642 (2022) https://doi.org/10. 1109/LRA.2021.3139667 

- [437] James, S., Wada, K., Laidlow, T., Davison, A.J.: Coarse-to-Fine Q-attention: Efficient Learning for Visual Robotic Manipulation via Discretisation. arXiv (2022). https:// doi.org/10.48550/arXiv.2106.12534 

- [438] Nguyen, E.-R., Zhang, Y., Ranasinghe, K., Li, X., Ryoo, M.S.: Pixel Motion Diffusion Is What We Need for Robot Control. arXiv (2025). https://doi.org/10. 48550/arXiv.2509.22652 

- [439] Liu, M., Shu, J., Chen, H., Li, Z., Zhao, C., Yang, J., et al.: StaMo: Unsupervised Learning of Generalizable Robot Motion from Compact State Representation. arXiv (2025). https://doi.org/10. 48550/arXiv.2510.05057 

- [440] Davies, T., Huang, Y., Liu, Y., Chen, X., 

66 

   - Liu, H., Hu, L.: Tenma: Robust CrossEmbodiment Robot Manipulation with Diffusion Transformer. arXiv (2025). https:// doi.org/10.48550/arXiv.2509.11865 

- [441] Wang, Y., Zhu, H., Liu, M., Yang, J., Fang, H.-S., He, T.: VQ-VLA: Improving VisionLanguage-Action Models via Scaling VectorQuantized Action Tokenizers. arXiv (2025). https://doi.org/10.48550/arXiv.2507.01016 

- [442] Lu, W., Wu, X., Gao, S., He, W., Zhao, Q., Zhang, L., _et al._ : Research on Task Decomposition and Motion Trajectory Optimization of Robotic Arm Based on VLA Large Model. In: 2024 5th International Conference on Machine Learning and Computer Application (ICMLCA), pp. 80–85. IEEE, Hangzhou, China (2024). https://doi.org/ 10.1109/ICMLCA63499.2024.10754333 

- [443] Yang, G., Zhang, T., Hao, H., Wang, W., Liu, Y., Wang, D., et al.: Vlaser: VisionLanguage-Action Model with Synergistic Embodied Reasoning. arXiv (2025). https: //doi.org/10.48550/arXiv.2510.11027 

- [444] Wei, Y., Sun, Y., Zheng, R., Vemprala, S., Bonatti, R., Chen, S., _et al._ : Is Imitation All You Need? Generalized DecisionMaking with Dual-Phase Training. In: 2023 IEEE/CVF International Conference on Computer Vision (ICCV), pp. 16175–16185. IEEE, Paris, France (2023). https://doi.org/ 10.1109/ICCV51070.2023.01486 

- [445] Roy, K., Dissanayake, A., Tidd, B., Moghadam, P.: M2Distill: MultiModal Distillation for Lifelong Imitation Learning. arXiv (2025). https://doi.org/10.48550/arXiv.2410.00064 

- [446] Wen, Y., Lin, J., Zhu, Y., Han, J., Xu, H., Zhao, S., et al.: VidMan: Exploiting Implicit Dynamics from Video Diffusion Model for Effective Robot Manipulation. arXiv (2024). https://doi.org/10.48550/arXiv.2411.09153 

- [447] Han, B., Kim, J., Jang, J.: A Dual Process VLA: Efficient Robotic Manipulation Leveraging VLM. arXiv (2024). https://doi.org/ 10.48550/arXiv.2410.15549 

- [448] Lv, Q., Kong, W., Li, H., Zeng, J., Qiu, Z., Qu, D., et al.: F1: A Vision-LanguageAction Model Bridging Understanding and Generation to Actions. arXiv (2025). https: //doi.org/10.48550/arXiv.2509.06951 

- [449] Zhang, J., Chen, Y., Xu, Y., Huang, Z., Zhou, Y., Yuan, Y.-J., et al.: 4D-VLA: Spatiotemporal VisionLanguage-Action Pretraining with Cross-Scene Calibration. arXiv (2025). https://doi.org/10.48550/arXiv.2506.22242 

- [450] Gervet, T., Xian, Z., Gkanatsios, N., Fragkiadaki, K.: Act3D: 3D Feature Field Transformers for Multi-Task Robotic Manipulation. arXiv (2023). https://doi.org/10. 48550/arXiv.2306.17817 

- [451] Zhang, J., Guo, Y., Hu, Y., Chen, X., Zhu, X., Chen, J.: UP-VLA: A Unified Understanding and Prediction Model for Embodied Agent. arXiv (2025). https://doi.org/10. 48550/arXiv.2501.18867 

- [452] Zhuo, F., He, Y., Yu, F., Li, P., Zhao, Z., Sun, X.: ABM: Attention before Manipulation. In: Proceedings of the Thirty-ThirdInternational Joint Conference on Artificial Intelligence, pp. 1816–1824. International Joint Conferences on Artificial Intelligence Organization, Jeju, South Korea (2024). https://doi.org/10.24963/ijcai.2024/201 

- [453] Cen, J., Yu, C., Yuan, H., Jiang, Y., Huang, S., Guo, J., et al.: WorldVLA: Towards Autoregressive Action World Model. arXiv (2025). https://doi.org/10.48550/arXiv.2506.21539 

- [454] Wang, Y., Li, X., Wang, W., Zhang, J., Li, Y., Chen, Y., et al.: Unified VisionLanguage-Action Model. arXiv (2025). https://doi.org/10.48550/arXiv.2506.19850 

- [455] Wang, H., Xiong, C., Wang, R., Chen, X.: BitVLA: 1-Bit Vision-Language-Action Models for Robotics Manipulation. arXiv (2025). https://doi.org/10.48550/arXiv. 2506.07530 

67 

- [456] Zhou, Z., Zhu, Y., Wen, J., Shen, Tactile Sensing. arXiv (2025). https: C., Xu, Y.: ChatVLA-2: Vision//doi.org/10.48550/arXiv.2508.08706 Language-Action Model with Open-World Embodied Reasoning from Pre[464] Driess, D., Springenberg, J.T., Ichter, trained Knowledge. arXiv (2025). B., Yu, L., Li-Bell, A., Pertsch, K., et https://doi.org/10.48550/arXiv.2505.21906 al.: Knowledge Insulating Vision-Language- 

   - [464] Driess, D., Springenberg, J.T., Ichter, B., Yu, L., Li-Bell, A., Pertsch, K., et al.: Knowledge Insulating Vision-LanguageAction Models: Train Fast, Run Fast, Generalize Better. arXiv (2025). https://doi. org/10.48550/arXiv.2505.23705 

- [457] Yue, Y., Wang, Y., Kang, B., Han, Y., Wang, S., Song, S., et al.: DeeR-VLA: Dynamic Inference of Multimodal Large Language Models for Efficient Robot Execution. arXiv (2024). https://doi.org/10. 48550/arXiv.2411.02359 

   - [465] Fang, X., Huang, B.-R., Mao, J., Shone, J., Tenenbaum, J.B., LozanoP´erez, T., et al.: Keypoint Abstraction Using Large Models for Object-Relative Imitation Learning. arXiv (2024). https://doi.org/10.48550/arXiv.2410.23254 

- [458] Patratskiy, M.A., Kovalev, A.K., Panov, A.I.: Spatial Traces: Enhancing VLA Models with Spatial-Temporal Understanding. arXiv (2025). https: //doi.org/10.48550/arXiv.2508.09032 

   - [466] Jiang, T., Jiang, X., Ma, Y., Wen, X., Li, B., Zhan, K., et al.: The Better You Learn, The Smarter You Prune: Towards Efficient Vision-language-action Models via Differentiable Token Pruning. arXiv (2025). https: //doi.org/10.48550/arXiv.2509.12594 

- [459] Dey, S., Zaech, J.-N., Nikolov, N., Gool, L.V., Paudel, D.P.: ReVLA: Reverting Visual Domain Limitation of Robotic Foundation Models. arXiv (2025). https://doi. org/10.48550/arXiv.2409.15250 

   - [467] Su, Y., Zhan, X., Fang, H., Li, Y.-L., Lu, C., Yang, L.: Motion Before Action: Diffusing Object Motion as Manipulation Condition. arXiv (2025). https://doi.org/ 10.48550/arXiv.2411.09658 

- [460] Jin, C., Tan, W., Yang, J., Liu, B., Song, R., Wang, L., et al.: AlphaBlock: Embodied Finetuning for Vision-Language Reasoning in Robot Manipulation. arXiv (2023). https: //doi.org/10.48550/arXiv.2305.18898 

   - [468] Song, H., Le, L.: Avi: Action from Volumetric Inference. arXiv (2025). https://doi.org/ 10.48550/arXiv.2510.21746 

- [461] Bonatti, R., Vemprala, S., Ma, S., Frujeri, F., Chen, S., Kapoor, A.: PACT: Perception-Action Causal Transformer for Autoregressive Robotics Pre-Training. In: 2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 3621–3627. IEEE, Detroit, MI, USA (2023). https://doi.org/10.1109/ IROS55552.2023.10342381 

   - [469] Zhou, Z., Zhu, Y., Zhu, M., Wen, J., Liu, N., Xu, Z., et al.: ChatVLA: Unified Multimodal Understanding and Robot Control with VisionLanguage-Action Model. arXiv (2025). https://doi.org/10.48550/arXiv.2502.14420 

   - [470] Li, J., Gao, Q., Johnston, M., Gao, X., He, X., Shakiah, S., et al.: Mastering Robot Manipulation with Multimodal Prompts through Pretraining and Multi-task Finetuning. arXiv (2024). https://doi.org/10. 48550/arXiv.2310.09676 

- [462] Xu, R., Shen, Y., Li, X., Wu, R., Dong, H.: NaturalVLM: Leveraging Fine-grained Natural Language for Affordance-Guided Visual Manipulation. arXiv (2024). https: //doi.org/10.48550/arXiv.2403.08355 

   - [471] Bing, Z., Koch, A., Yao, X., Huang, K., Knoll, A.: Meta-Reinforcement Learning via Language Instructions. arXiv (2022). https: //doi.org/10.48550/arXiv.2209.04924 

- [463] Cheng, Z., Zhang, Y., Zhang, W., Li, H., Wang, K., Song, L., et al.: OmniVTLA: Vision-Tactile-LanguageAction Model with Semantic-Aligned 

68 

- [472] Tan, W., Wang, B., Zhi, H., Liu, C., Li, Z., Liu, J., et al.: BLM$ ~~1~~ $: A Boundless Large Model for Cross-Space, Cross-Task, and Cross-Embodiment Learning. arXiv (2025). https://doi.org/10.48550/arXiv.2510.24161 

- [473] Hu, Y., Song, P., Wen, K., Detry, R.: Mini Diffuser: Fast Multi-task Diffusion Policy Training Using Two-level Minibatches. arXiv (2025). https://doi.org/10. 48550/arXiv.2505.09430 

- [474] Wu, K., Zhu, Y., Li, J., Wen, J., Liu, N., Xu, Z., _et al._ : Discrete Policy: Learning Disentangled Action Space for MultiTask Robotic Manipulation. In: 2025 IEEE International Conference on Robotics and Automation (ICRA), pp. 8811–8818. IEEE, Atlanta, GA, USA (2025). https://doi.org/ 10.1109/ICRA55743.2025.11127630 

- [475] Physical, I.: PI06 

- [476] Hung, C.-Y., Sun, Q., Hong, P., Zadeh, A., Li, C., Tan, U.-X., et al.: NORA: A Small Open-Sourced Generalist Vision Language Action Model for Embodied Tasks. arXiv (2025). https://doi.org/10. 48550/arXiv.2504.19854 

- [477] Li, Z., Ren, L., Yang, J., Zhao, Y., Wu, X., Xu, Z., et al.: VIRT: Vision Instructed Transformer for Robotic Manipulation. arXiv (2024). https://doi.org/10. 48550/ARXIV.2410.07169 

- [478] Chen, S., Garcia, R., Schmid, C., Laptev, I.: PolarNet: 3D Point Clouds for LanguageGuided Robotic Manipulation. arXiv (2023). https://doi.org/10.48550/arXiv. 2309.15596 

- [479] Zhang, R., Dong, M., Zhang, Y., Heng, L., Chi, X., Dai, G., et al.: MoLe-VLA: Dynamic Layer-skipping Vision Language Action Model via Mixture-of-Layers for Efficient Robot Manipulation. arXiv (2025). https://doi.org/10.48550/arXiv.2503.20384 

- [480] AgiBot-World-Contributors, Bu, Q., Cai, J., Chen, L., Cui, X., Ding, Y., et al.: AgiBot 

World Colosseo: A Large-scale Manipulation Platform for Scalable and Intelligent Embodied Systems. arXiv (2025). https:// doi.org/10.48550/arXiv.2503.06669 

- [481] Chebotar, Y., Vuong, Q., Irpan, A., Hausman, K., Xia, F., Lu, Y., et al.: Q- Transformer: Scalable Offline Reinforcement Learning via Autoregressive Q- Functions. arXiv (2023). https://doi.org/10. 48550/arXiv.2309.10150 

- [482] Wen, Y., Li, H., Gu, K., Zhao, Y., Wang, T., Sun, X.: LLaDA-VLA: Vision Language Diffusion Action Models. arXiv (2025). https: //doi.org/10.48550/arXiv.2509.06932 

- [483] Liang, W., Sun, G., He, Y., Ren, Y., Dong, J., Cong, Y.: NeverEnding Behavior-Cloning Agent for Robotic Manipulation. arXiv (2025). https://doi.org/10.48550/arXiv.2403.00336 

- [484] Li, H., Yan, S., Li, Y., Wang, X.: Towards Fast, Memory-based and Data-Efficient Vision-Language Policy. arXiv (2025). https://doi.org/10.48550/arXiv.2503.10322 

- [485] Zheng, B., Zhou, J., Chen, F.: Interpretable Robotic Manipulation from Language. arXiv (2024). https://doi.org/10. 48550/arXiv.2405.17047 

- [486] Liu, J., Liu, M., Wang, Z., An, P., Li, X., Zhou, K., et al.: RoboMamba: Efficient Vision-Language-Action Model for Robotic Reasoning and Manipulation. arXiv (2024). https://doi.org/10.48550/arXiv.2406.04339 

- [487] Jang, H., Yu, S., Kwon, H., Jeon, H., Seo, Y., Shin, J.: ContextVLA: Vision-LanguageAction Model with Amortized Multi-Frame Context. arXiv (2025). https://doi.org/10. 48550/arXiv.2510.04246 

- [488] Koo, J., Cho, T., Kang, H., Pyo, E., Oh, T.G., Kim, T., et al.: RetoVLA: Reusing Register Tokens for Spatial Reasoning in Vision-Language-Action Models. arXiv (2025). https://doi.org/10.48550/ arXiv.2509.21243 

69 

- [489] Zhang, T., Duan, H., Hao, H., Qiao, Y., Dai, J., Hou, Z.: Grounding Actions in Camera Space: Observation-Centric VisionLanguage-Action Policy. arXiv (2025). https://doi.org/10.48550/arXiv.2508.13103 

- [490] Li, P., Wu, Y., Xi, Z., Li, W., Huang, Y., Zhang, Z., et al.: ControlVLA: Few-shot Object-centric Adaptation for Pre-trained VisionLanguage-Action Models. arXiv (2025). https://doi.org/10.48550/arXiv.2506.16211 

- [491] Dasari, S., Mees, O., Zhao, S., Srirama, M.K., Levine, S.: The Ingredients for Robotic Diffusion Transformers. arXiv (2024). https://doi.org/10.48550/ arXiv.2410.10088 

- [492] Chen, Y., Li, P., Huang, Y., Yang, J., Chen, K., Wang, L.: EC-Flow: Enabling Versatile Robotic Manipulation from ActionUnlabeled Videos via Embodiment-Centric Flow. arXiv (2025). https://doi.org/10. 48550/arXiv.2507.06224 

- [493] Xian, Z., Gkanatsios, N., Gervet, T., Ke, T.-W., Fragkiadaki, K.: ChainedDiffuser: Unifying Trajectory Diffusion and Keypose Prediction for Robotic Manipulation (2023) 

- [494] Li, Y., Zhang, T., Wei, X., Li, J., Zhao, L., Huang, D., et al.: Object-Focus Actor for Data-efficient Robot Generalization Dexterous Manipulation. arXiv (2025). https: //doi.org/10.48550/arXiv.2505.15098 

- [495] Sejnova, G., Vavrecka, M., Stepanova, K.: Bridging Language, Vision and Action: Multimodal VAEs in Robotic Manipulation Tasks. In: 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 12522–12528 (2024). https://doi.org/10.1109/IROS58592.2024. 10802160 

- [496] Abouzeid, A., Mansour, M., Sun, Z., Song, D.: GeoAware-VLA: Implicit Geometry Aware Vision-LanguageAction Model. arXiv (2025). https: //doi.org/10.48550/arXiv.2509.14117 

- [497] Song, W., Chen, J., Ding, P., Huang, Y., Zhao, H., Wang, D., et al.: CEED-VLA: Consistency Vision-Language-Action Model with Early-Exit Decoding. arXiv (2025). https://doi.org/10.48550/arXiv.2506.13725 

- [498] Wang, S., Yu, R., Yuan, Z., Yu, C., Gao, F., Wang, Y., et al.: Spec-VLA: Speculative Decoding for Vision-Language-Action Models with Relaxed Acceptance. arXiv (2025). https://doi.org/10.48550/ARXIV. 2507.22424 

- [499] Li, X., Wang, S., Chen, C., Wei, H., Shi, Y., Mo, H.: RoboFlamingo-Plus: Fusion of Depth and RGB Perception with VisionLanguage Models for Enhanced Robotic Manipulation. In: 2025 IEEE International Conference on Real-time Computing and Robotics (RCAR), pp. 311–316. IEEE, Toyama, Japan (2025). https://doi.org/10. 1109/RCAR65431.2025.11139480 

- [500] Nguyen, N., Vu, M.N., Ta, T.D., Huang, B., Vo, T., Le, N., et al.: Robotic-CLIP: Finetuning CLIP on Action Data for Robotic Applications. arXiv (2024). https://doi.org/ 10.48550/arXiv.2409.17727 

- [501] Budzianowski, P., Maa, W., Freed, M., Mo, J., Hsiao, W., Xie, A., et al.: EdgeVLA: Efficient VisionLanguage-Action Models. arXiv (2025). https://doi.org/10.48550/arXiv.2507.14049 

- [502] Niu, D., Sharma, Y., Biamby, G., Quenum, J., Bai, Y., Shi, B., et al.: LLARVA: VisionAction Instruction Tuning Enhances Robot Learning. arXiv (2024). https://doi.org/10. 48550/arXiv.2406.11815 

- [503] Ge, S., Zhang, Y., Xie, S., Zhang, W., Zhou, M., Wang, Z.: VGGT-DP: Generalizable Robot Control via Vision Foundation Models. arXiv (2025). https://doi.org/10.48550/ arXiv.2509.18778 

- [504] Zhu, M., Zhu, Y., Li, J., Wen, J., Xu, Z., Liu, N., _et al._ : Scaling Diffusion Policy in Transformer to 1 Billion Parameters for Robotic Manipulation. In: 2025 IEEE International Conference on Robotics and Automation 

70 

(ICRA), pp. 10838–10845. IEEE, Atlanta, GA, USA (2025). https://doi.org/10.1109/ ICRA55743.2025.11128074 

## **Appendix A Related Works** 

71 

**Table A1:** Full list of identified related works/ surveys. _Total 55 publications from survey corpus as depicted in Figure 9._ 

|**Ref**|**Title**|**Year** _↓_|
|---|---|---|
|[170]|A Review of Embodied Grasping|2025|
|[171]|A Survey of Behavior Foundation Model: Next-Generation Whole-Body Control System<br>of Humanoid Robots|2025|
|[13]|A Survey on Vision-Language-Action Models for Embodied AI|2025|
|[17]|A Survey on Vision-Language-Action Models: An Action Tokenization Perspective|2025|
|[172]|A Taxonomy for Evaluating Generalist Robot Policies|2025|
|[173]|Aligning Cyber Space with Physical World: A Comprehensive Survey on Embodied AI|2025|
|[16]|An Anatomy of Vision-Language-Action Models: From Modules to Milestones and<br>Challenges|2025|
|[174]|Applications of Large Language Models and Multimodal Large Models in Autonomous<br>Driving: A Comprehensive Review|2025|
|[15]|Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation|2025|
|[175]|Embodied AI with Foundation Models for Mobile Service Robots: A Systematic Review|2025|
|[176]|Embodied AI: Bridging Simulation and Reality in Robotics|2025|
|[177]|Embodied AI: From LLMs to World Models|2025|
|[178]|Exploring Embodied Multimodal Large Models: Development|2025|
|[179]|Foundation Model Driven Robotics: A Comprehensive Review|2025|
|[180]|From Grounding to Manipulation: Case Studies of Foundation Model Integration in<br>Embodied Robotic Systems|2025|
|[181]|Generative Artificial Intelligence in Robotic Manipulation: A Survey|2025|
|[182]|Integrating Large Language Models into Robotic Autonomy: A Review of Motion|2025|
|[183]|Large Language Models and 3D Vision for Intelligent Robotic Perception and Autonomy|2025|
|[184]|Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied<br>Learning|2025|
|[30]|Large VLM-based Vision-Language-Action Models for Robotic Manipulation: A Survey|2025|
|[185]|Multi-Modal Multi-Task (M3T) Federated Foundation Models for Embodied AI:<br>Potentials and Challenges for Edge Integration|2025|
|[186]|Multimodal Fusion and Vision-Language Models: A Survey for Robot Vision|2025|
|[187]|Neural Brain: A Neuroscience-inspired Framework for Embodied Agents|2025|
|[188]|Neural Scaling Laws in Robotics|2025|
|[31]|OpenHelix: A Short Survey|2025|
|[14]|Parallels Between VLA Model Post-Training and Human Motor Learning: Progress|2025|
|[32]|Pure Vision Language Action (VLA) Models: A Comprehensive Survey|2025|
|[189]|Toward Embodied AGI: A Review of Embodied AI and the Road Ahead|2025|
|[190]|Towards Embodied Agentic AI: Review and Classification of LLM- and VLM-Driven<br>Robot Autonomy and Interaction|2025|
|[33]|Towards Generalist Robot Policies: What Matters in Building Vision-Language-Action<br>Models|2025|


_continued on next page_ 

72 

|**Ref**<br>[35]|**Title**<br>Vision-Language Model-Based Human-Robot Collaboration for Smart Manufacturing:<br>A State-of-the-Art Survey|**Year**<br>2025|
|---|---|---|
|[34]|Vision-Language-Action Models: Concepts, Progress, Applications and Challenges|2025|
|[191]|What Foundation Models Can Bring for Robot Learning in Manipulation : A Survey|2025|
|[192]|A Survey for Foundation Models in Autonomous Driving|2024|
|[193]|A Survey of Robot Intelligence with Large Language Models|2024|
|[194]|A Survey of Robotic Language Grounding: Tradeoffs between Symbols and Embeddings|2024|
|[195]|A Survey on Integration of Large Language Models with Intelligent Robots|2024|
|[196]|A Survey on Robotics with Foundation Models: Toward Embodied AI|2024|
|[197]|Advancements in Robotic Intelligence: The Role of Computer Vision|2024|
|[198]|Advances in Transformers for Robotic Applications: A Review|2024|
|[199]|Embodied AI with Large Language Models: A Survey and New HRI Framework|2024|
|[36]|Embodied Intelligence Toward Future Smart Manufacturing in the Era of AI<br>Foundation Model|2024|
|[200]|Foundation Models for Autonomous Robots in Unstructured Environments|2024|
|[201]|Integrating Reinforcement Learning with Foundation Models for Autonomous Robotics:<br>Methods and Perspectives|2024|
|[202]|Large Language Models for Robotics: Opportunities|2024|
|[203]|Leveraging Foundation Models in Robotics: Transforming Task Planning and<br>Contextual Execution|2024|
|[204]|Leveraging Large Language Models in Human-Robot Interaction: A Critical Analysis of<br>Potential and Pitfalls|2024|
|[205]|Real-World Robot Applications of Foundation Models: A Review|2024|
|[206]|The Future of Intelligent Healthcare: A Systematic Analysis and Discussion on the<br>Integration and Impact of Robots Using Large Language Models for Healthcare|2024|
|[12]|Toward General-Purpose Robots via Foundation Models: A Survey and Meta-Analysis|2024|
|[207]|Towards Generalist Robot Learning from Internet Video: A Survey|2024|
|[208]|Demonstrating Large Language Models on Robots|2023|
|[9]|Foundation Models in Robotics: Applications|2023|
|[209]|Large Language Models for Robotics: A Survey|2023|
|[210]|Robot Learning in the Era of Foundation Models: A Survey|2023|


73 

## **Appendix B Literature Research** 

74 

**Table B2:** All eleven ASQS Queries used for the RFM-related (main) corpus retrieval process as described in Section 3.2. _Characters are escaped as used within the Python Script, each query is shown before being translated for the respective database._ 

- `["(robot* OR robotic) AND (general* OR generalist OR generalisation OR generalization OR foundation OR \"multi-task\" OR multitask OR \"multi task\" OR \"pre-trained\" OR pretrained OR \"pre trained\") AND (control OR manipulation OR action OR learning) AND (transformer OR model* OR policy OR agent* OR system) AND (\"vision-based\" OR \"vision based\" OR \"vision-language\" OR \"vision language\" OR \"language-guided\" OR \"language guided\" OR \"natural language\" OR \"natural-language\" OR \"multi-modal\" OR \"multi modal\" OR multimodal)",` 

- `"(robot* OR robotic) AND \"foundation model*\"~3",` 

- `"(robot* OR robotic) AND (\"vision-language-action\" OR \"vision language action\"~3) AND model*",` 

- `"(robotic OR robot*) AND (\"foundation model\" OR \"general-purpose model\"~3 OR \"large-scale AI\"~3 OR \"pretrained AI\" OR \"generalist AI\") AND (\"multi-modal\" OR multimodal OR \"diverse datasets\" OR \"robot demonstration\" OR \"shared representation\" OR \"transfer learning\") AND (generalization OR versatility OR transferability OR adaptation OR \"broad capabilities\"~3) AND (perception OR \"decision-making\" OR actuation) NOT (\"specialized task\" OR \"specific kinematics\" OR \"highly-specialized\")",` 

- `"(robot* OR robotic OR robotics) AND (\"foundation model\" OR \"general-purpose model\" OR \"large-scale model\" OR \"generalist AI\") AND (multimodal OR \"multi-modal\" OR \"diverse datasets\" OR \"robot demonstrations\" OR \"sensor data\" OR \"visual data\") AND (control OR perception OR actuation OR \"decision-making\" OR intelligence) AND (generalization OR transfer OR \"adaptable intelligence\" OR \"transferable capabilities\") NOT (specialized OR \"specific kinematics\" OR \"specific tasks\" OR \"highly-specialized\")",` 

- `"(robot* OR robotic) AND (\"foundation model*\" OR \"pretrained model*\" OR versatile OR transferable OR generalist OR \"shared representation*\") AND (multimodal OR \"robot sensors\" OR \"sensor data\" OR (image OR text OR dataset*)) AND (perception OR intelligence OR actuation OR \"robot behavior\") AND (generalization OR adaptation OR versatility) NOT (specific OR specialized OR \"highly-specialized task\" OR kinematic*)",` 

- `"(\"robot* foundation model\"~3 OR \"robot* generalist model\"~3 OR \"general-purpose robot* model\"~3) AND ((multimodal OR \"multi-modal\" OR \"multi modal\") AND (pretrained OR \"pre-trained\" OR \"pre trained\")) AND (generalization OR generalisation OR transfer OR adaptability OR versatility OR \"broad capabilities\") AND (perception OR \"decision-making\" OR actuation OR control) NOT (\"task-specialized\" OR \"specific robot kinematics\" OR \"highly-specialized model*\")",` 

- `"(\"vision-language-action\" OR \"vision language action\"~3 OR VLA OR (vision AND language AND action)) AND ((model OR architecture OR system) AND (multimodal OR \"multi-modal\" OR \"multi modal\")) AND (robot* OR robotics) AND (manipulat* OR navigat* OR control OR action OR behavior) AND (versatile OR \"general-purpose\" OR general*) NOT (\"single-modality\" OR specialized OR narrow)",` 

- `"(\"vision-language-action\"~3 OR \"vision NEAR/3 language NEAR/3 action\" OR VLA OR (multimodal AND (vision OR perception) AND language AND action)) AND (robot* OR robotics OR robotic) AND (model OR system OR architecture) AND (control OR behavior OR movement OR manipulation OR navigation) AND (\"general-purpose\" OR versatile OR integration) NOT (\"single-modality\" OR \"perception-only\" OR \"language-only\" OR narrow OR specialized)",` 

- `"(multimodal AND (vision AND language AND action)) AND (robot* OR robotics) AND (\"control signals\" OR behaviors OR actions OR navigation OR manipulation) AND (versatile OR \"general-purpose\" OR integrated) NOT (narrow OR \"single-modality\" OR specialized)",` 

- `"(\"vision-language-action\" OR \"vision language action\"~3 OR VLA) AND (robot* OR robotics OR \"robotic system\") AND (AI OR \"artificial intelligence\" OR \"machine learning\") AND (control OR behavior OR action OR manipulation OR navigation) AND (multimodal OR \"multi-modal\" OR integrated OR \"multi modal\") AND (model OR framework) NOT (\"perception only\" OR \"single modality\" OR \"language modeling alone\" OR \"narrow task\")"]` 

75 

**Table B3:** All seven ASQS Queries used for the industrial implication corpus retrieval process as described in Section 3.3. _Characters are escaped as used within the Python Script, each query is shown before being translated for the respective database._ 

- `["(robot OR robotics) AND (industrial OR \"industrial application\"~3 OR \"industrial use-case\"~3 OR \"applied robotics\"~3 OR \"industrial environment\"~2) AND (review OR analysis OR viewpoint OR guideline OR perspective) AND (hardware OR sensor OR \"compute resource\"~2 OR integration OR compliance OR standards OR workflow)",` 

- `"(robotics system* OR \"industrial robotics\" OR \"applied robot*\"~2) AND (design OR performance OR deployment OR scalability OR robustness OR reliability OR safety OR operator interaction) AND (industrial needs OR \"industrial requirement*\"~2 OR \"industrial-focused\" OR \"real-world application\"~3)",` 

- `"(robotics OR robot* OR \"robotic systems\") AND (industrial OR \"industry-specific\" OR \"industrial automation\") AND (design OR deployment OR \"performance requirement*\"~2) AND (\"machine learning\" OR ML OR \"artificial intelligence\" OR AI) AND (analyze OR review OR implication* OR considerations)",` 

- `"(\"industrial robots\" OR robotics OR \"robot hardware\" OR \"robotic systems\") AND (sensor* OR \"compute resources\" OR integration OR standards OR compliance OR regulatory) AND (manufacturing OR logistics OR assembly OR inspection OR \"quality control\") AND (property OR characteristic OR \"industrial requirements\")",` 

- `"(\"industrial deployment\" OR \"industrial automation\" OR \"real-world deployment\") AND (\"robotics\" OR \"robot\") AND (\"challenges\" OR scalability OR robustness OR reliability OR safety OR \"operator interaction\") AND (\"machine learning\" OR AI)",` 

- `"(robotics OR AI) AND (review OR \"case study\" OR analysis) AND (industrial OR \"manufacturing environments\" OR logistics OR \"assembly line\" OR warehouse OR inspection OR \"quality assurance\") AND (constraints OR \"sector-specific needs\" OR adaptability)",` 

- `"(industrial robotics OR \"robotic system\") AND (hardware OR \"compute resources\" OR sensor OR \"sensor types\" OR integration OR \"regulatory compliance\" OR standards OR \"performance requirements\") AND (manufacturing OR logistics OR factory OR automotive OR electronics OR warehousing) NOT (academic OR prototype)"]` 

76 

## **Appendix C Industrial Implications** 

77 

**Table C4:** Full criteria catalogue for industrial applicability rating as discussed in Section 7.3. _Derived from the general industrial implications (see Section 7.1)_ 

|**Implication**|**Category/ Criterion**|
|---|---|
|**I1:**|A. Multi-Hardware and Configuration Adaptability|
|**Adaptability &**<br>**Flexibility**|1. _Multi-Hardware Support:_ Operates with different kinematics, sensors, and<br>end-effectors without retraining.<br>2. _Hot-Swappable_ & _Dimensionality Adaptation:_ Sensors/actuators can be replaced,<br>added, or removed during operation. Automatically detects and configures<br>input/output channels at runtime according to connected hardware and environmental<br>context: Flexibly adapts the dimensionality, type and interpretation without manual<br>intervention or system restart.<br>B. Task Adaptability and Strategy Flexibility<br>3. _Multi-Task Generalisation:_ Handles multiple task types/categories, including unseen<br>variations thereof, without retraining. Adapts strategies dynamically for task variations<br>and can switch between tasks online.<br>4. _Restricted Autonomous Task Switching:_ Only switches between distinct tasks upon<br>explicit user instruction: autonomy remains bounded, so adherence to the operator’s<br>goal stays primary (may autonomously adapt solution approaches/ strategies).<br>5. _Strategy-Goal Alignment:_ Any adaptation of solution strategies ensures adherence to<br>the commanded task goal: deviating too far from user instructions triggers feedback,<br>halt, or request for approval.<br>C. Environmental Adaptation and Robustness<br>6. _Generalisation to Environmental Variation:_ Maintains consistent performance across<br>diverse environmental conditions (lighting, weather, background, friction, etc.),<br>object/material variations, and scene clutter, with minimal degradation.<br>7. _Autonomous Handling of Distractors/Obstacles:_ Identifies and robustly manages/<br>handles unknown, distracting, or non-required objects in the scene or obstacles along<br>the path/ trajectory (including incorporation into task strategy if needed).<br>8. _Online Environment Adaptation_ & _Response:_ Recognises and continuously adapts to<br>environmental changes, such as errors, faults, sensor degradation or external influences<br>during operation: e.g. logging, halting, or feedback-requesting as confidence drops.<br>9. _Autonomous Fallbacks:_ Capable of autonomously choosing context-appropriate<br>error/fault responses (e.g. request feedback, switch input modalities, logging, etc.) and<br>behaviour (e.g. continue operation, transition to safe state, adapt strategy, etc.)<br>without requiring predefined fallback behaviour.|
||D. Instruction and Feedback Flexibility<br>10. _Multimodal Command Interface:_ Accepts user-input (task instructions,<br>correction/feedback, etc.) via diverse modalities (natural language in multiple<br>languages, images, teaching by demonstration, video, etc.).<br>11. _Mid-Execution Feedback Responsiveness:_ Remains receptive to user feedback and<br>correction throughout execution, enabling course correction and adjustment without<br>re-initiating trajectories.<br>E. Self-Flexibility and Adaptive Behaviour|


78 

|**Implication**|**Category/ Criterion**|
|---|---|
||12. _Operational Adaptation Confidence:_ Continuously outputs a confidence score<br>reflecting its present predicted ability to execute the instructed task using the currently<br>(adapted) solution strategy, in the current environment, with the currently active<br>hardware configuration and sensor context. The score may be used to trigger automatic<br>logging, operator feedback requests, or safe halting if confidence drops below a set<br>threshold, ensuring transparent awareness and operational safety during dynamic<br>adaptation.<br>13. _Autonomous Incorporation of Skills:_ Dynamically selects and integrates known<br>robot skills (e.g. action primitives) as needed for current task/environment into the<br>current solution strategy (like tool-calling).<br>14. _Online/Mid-Execution Adaptation:_ Integrates operator/environmental feedback,<br>(input/ task)-quality degradation and detected faults dynamically during operation,<br>adapting strategy, input importance or output.<br>15. _Explained Adaptation Decisions:_ Explains, upon request, its performed/ intended<br>adaptation of strategies, handling of distractors, input importance/quality (for each<br>modality), and response to uncertainties or noise.<br>16. _Memory of Previous Faults/Distractors:_ Remembers prior encountered variations,<br>distractors, faults, anomalies, environmental changes and corresponding solutions,<br>reducing the need for repeated user intervention for recurring scenarios.<br>17. _Energy/System-Aware Adaptation:_ Adapts solution strategies and predicted actions<br>based on real-time resource constraints and consumption (e.g. battery charge, system<br>health, energy/ compute utilisation).<br>18. _Self-Evaluation_ & Command Adherence: Continuously self-evaluates its own<br>adapted behaviour and adherence to user command(s): Flags or readjusts if deviation<br>from expected outcome or operator intent is detected.|
|**I2:**|A. Verification, Standards, and Certification|
|**Safety &**<br>**Compliance**|1. _Standards-Compliant:_ Behaviour and safety features are checked to align with<br>relevant industrial standards, evaluated by reproducible tests.<br>2. _Integrable Safety Systems:_ System interfaces and safety signals are compatible with<br>industrial plant safety infrastructure, supporting seamless integration and monitoring<br>(e.g. model-generated safety stop can be directly used to stop respective production line).<br>3. _Safety Documentation_ & _Traceability:_ All safety features, integration, and reasoning<br>are well documented, including considered safety rules, internal processes, output<br>explanations, and verified compliance with standards.<br>B. Safety Reasoning, Adaptation, and Confidence<br>4. _Safety Confidence Output:_ Outputs a confidence score estimating the safety margin<br>of each predicted operation and for the complete task before starting operation (in the<br>current environment). The confidence score quantifies the system’s estimated likelihood<br>that all specified safety requirements are currently satisfied, using<br>sensor/hardware/context data.<br>5. _Persistence of Safety Capabilities in Adaptation:_ Safety rules/modules remain<br>enforced, and system safety is verified after any model adaptation, retraining, or<br>finetuning _→_standalone safety logic cannot be bypassed by learning changes.<br>6. _Reactive, Real-Time Safety:_ System performs continuous, real-time evaluation of<br>safety (considering sensor noise, hardware degradation, dynamic obstacles, harmful<br>objects, OOD, and environment changes) – e.g. leveraging confidence – with immediate<br>adaptation (halting/ triggering stop, slowing, or replanning) if risks arise.|


79 

##### **Implication** 

##### **Category/ Criterion** 

7. _Proactive, Plan-Level Safety:_ Safety reasoning is incorporated into high-level planning/solution strategies (not only reactive), evaluating alternative actions and solutions by their associated predicted safety confidence. C. Safety Rules, Enforcement, and Supervisory Control 8. _Rule-Adherence_ & _Autonomous Rejection:_ The system always respects predefined safety/behavioural rules and can autonomously reject operator goals/commands that pose unacceptable risk (e.g. “grab knife and throw”), e.g. supervised by independently certified controllers/modules. 9. _Command Compliance with Online-Safety:_ System adheres strictly to operator commands as long as safety requirements are not compromised: Command execution is continuously monitored and suspended/modified if unacceptable risk is detected, providing transparent feedback (to the user/ logs/ supervisor/ etc.). 10. _Redundant, Independent Safety Mechanisms:_ Employs multiple, independent (possibly redundant and diverse-modality) mechanisms for safety assessment and enforcement (e.g. dual model prediction, dedicated supervisor, independent safety layers). 11. _Decoupled, Real-Time Safety Control:_ Safety checks and action execution operate independently: a ”safety semaphore” or gating mechanism ensures actions are only predicted/executed when confidence exceeds threshold. D. Operator/User and External Interfaces 12. _Authorised Operator Detection_ & _Override:_ Only authorised/ recognised operators may control safety overrides or cause safety-critical actions; interfaces securely verify operator identity and permissions. 13. _External Safety Integration:_ Safety outputs/signals are shareable with other robots/systems in plant (including alarms, safe state signals, zone definitions, and status reports). E. Fault Detection and Recovery 14. _Fault Detection_ & _Sensing:_ Actively detects major faults or safety violations. Distinguishes between sensor fault and safety/ environmental hazard and the degree of severity. 15. _Safe, Autonomous Recovery:_ Recovers autonomously to a safe state after detecting major faults, safety loss, low safety-related confidence in own actions or accidents. 16. _Learning from Safety Events:_ Continuously adapts and improves safety confidence/logic or recovery behaviour based on feedback from operator, supervisor modules, comparison of actual vs. predicted safety outcomes and past incidents. F. Transparency and Logging 17. _Transparent Safety Reasoning:_ The system can explain its safety confidence, risk assessment, and chosen/blocked actions to operators, both live and retrospectively (with logs/reports or upon querying). 18. _Persistent Safety Logs:_ All safety-relevant events, decisions, adaptations, actions, and outcomes are logged, both user-readable and for self-improvement. **I3:** A. Communication Modalities & Operator Interfaces **HRI** 1. _Multimodal Instruction_ & _Output:_ Accepts and generates instructions, queries, and **&** feedback through multiple operator interfaces (speech, text, gesture, visual). Chooses **HRC** the most suitable modalities based on available hardware, environmental context (e.g. noise level, lighting), operator preferences, and task demands/ instruction. 

80 

|**Implication**|**Category/ Criterion**|
|---|---|
||2. _Instruction Confidence:_ For every operator command or query, provides a confidence<br>score reflecting certainty in both (a) correct recognition of the input (e.g. speech<br>recognition, gesture identification), and (b) correct interpretation of the operator’s<br>intent. When confidence is low, proactively seeks clarification or reframing from the<br>operator, and communicates the reason for uncertainty (ambiguity, low signal, novel<br>command, etc.).<br>3. _Intuitive Feedback Acceptance:_ Integrates operator clarifications, corrections, or input<br>refinements (e.g. specifying objects, adjusting approach, clarifying intent) online, into<br>the ongoing action interpretation or prediction – adapting its immediate responses and<br>future understanding, mostly without pausing or disrupting the main task flow.<br>B. Responsiveness & Interaction Control<br>4. _Real-time Interruptibility:_ Allows operators/ users to instantly and directly pause,<br>modify, query, or halt ongoing execution or task, providing full control and safe<br>intervention across all interfaces and modalities.<br>5. _Continuous Responsiveness:_ Maintains complete HRI/HRC accessibility and<br>interaction throughout all operational phases (idle, executing, transitioning,<br>recovering), ensuring operators can always intervene, instruct, or query – never leaving<br>the system ”locked out” or unresponsive.|
||C. Operator Management, Authorisation & Privacy|
||6. _Active Operator Exclusivity:_ Guarantees that only one authorised/ known operator/<br>user is ”active” and in control at any time. Enforces explicit, secure handover or<br>switching protocols, and reliably ignores unverified or distracting bystanders in both<br>input and output.<br>7. _Operator Identification_ & _Authorisation:_ Identifies and responds exclusively to<br>securely recognised and authorised personnel/ user. Actively prevents unauthorised<br>commands, even under disruptive or noisy conditions, and logs all identity-related<br>access attempts.<br>8. _Operator Data Privacy:_ Encrypts and protects operator-specific data and interaction<br>history; permits authorised deletion or review in accordance with relevant privacy<br>standards. Ensures only authorised personnel can access, modify, or request deletion of<br>such data.|


9. _Learned Operator Preferences:_ Adapts interface layout, communication style, behaviour, or task sequencing to individual operators/ users – learning and persisting preferences across sessions for efficiency and comfort unless instructed otherwise. 

D. Human-Robot Collaboration & Behaviour Adaptation 10. _Human Presence Awareness in Workspace:_ Continuously senses human presence and proximity throughout and beyond the workspace using multiple sensor modalities (vision, audio, proximity, etc.). Dynamically adapts operation speed, safety margins, and communication in response to detected changes (especially in cases of unexpected entries, operator absence, etc.). 11. _Collaborative Adaptation:_ Reactively modulates solution strategies, action plans, and interaction traits in direct response to real-time operator feedback, demonstrations, or correction. Behaves as an adaptive teammate, tailoring technical and social behaviours to maximise collaboration efficiency. 12. _Human-Centric Adaptation:_ Dynamically and autonomously adjusts behaviour, speed, and language/output based on human presence, operator skill/preference, perceived operator condition, task safety factors, and perceived risk. 

E. Reasoning, Standards & Exception Handling 

81 

|**Implication**|**Category/ Criterion**|
|---|---|
||13. _Transparent Reasoning Explanation:_ Provides operator-friendly, on-demand<br>explanations during operation of its own reasoning, uncertainty, behaviour, and<br>decision-making – using appropriate modalities (natural language, images, charts) and<br>tailoring explanations to the operator’s degree of expertise.<br>14. _Industrial HRI/HRC Standards Compliance:_ Adheres to relevant industrial safety,<br>communication, and collaboration standards and best-practices for HRI and HRC;<br>supports integration with company-specific norms, exception rules, and documentation<br>requirements.<br>15. _Exception Handling_ & _Safe State Transition:_ Reliably recognises faults, abnormal<br>human behaviours, and communication breakdowns during HRI/HRC. Notifies the<br>operator, explains the situation, and if necessary, transitions to a pre-defined safe state.|
|**I4:**|A. Fault Detection, Diagnosis & Monitoring|
|**Robustness**<br>**&**<br>**Reliability**|1. _Multi-Level Fault_ & _Anomaly Detection:_ Continuously detects and logs faults,<br>anomalies, and degradations not only in system hardware and sensors, but also in<br>environment, manipulated objects, operator actions, and internal representations –<br>utilising diverse sensor inputs, automatic evaluation, supervisor components or<br>confidence scores to spot issues before failures occur.<br>2. _Reproducible_ & _Benchmarked Fault Diagnosis:_ Integrated fault/anomaly detection<br>delivers consistent, reproducible evaluations under matching conditions, with detection<br>precision benchmarked against standardised scenarios.<br>3. _Threat_ & _Attack Detection:_ Autonomously monitors all inputs and interface signals<br>for security threats, adversarial manipulations, and unauthorised commands, triggering<br>alerts or adapting strategies or behaviour to mitigate risk and reduce attack impact.<br>B. Error Handling, Recovery & Adaptation<br>4. _Automated Recovery_ & _Safe-State Transition:_ Autonomously initiates recovery<br>routines or shifts into a safe state when critical faults, severe anomalies, unrecoverable<br>disturbances, or low confidences are detected (prioritisation of safety and system<br>integrity over performance and task completion).<br>5. _Graceful Degradation_ & _Strategy Adaptation:_ Adjusts execution plans, sensor usage,<br>and action strategies in real-time when encountering partial sensor failures,<br>orientation/config changes, or slightly degraded environmental conditions, striving to<br>maintain performance without outright task failure.<br>6. _Autonomous Fault Categorisation_ & _Severity Response:_ Recognises, categorises, and<br>prioritises faults by severity, autonomously selecting and executing the most<br>appropriate recovery behaviour, fallback routine, or adaptation strategy.<br>7. _Robust Redundancy_ & _Modality Management:_ Ensures reliable operation and fault<br>tolerance by accepting, integrating, and dynamically switching between redundant<br>input and output modalities. When any channel degrades or fails, the system<br>autonomously maintains task progress through alternative modalities, adapting<br>detection, execution, and communication strategies to suit the current hardware,<br>environment, and operator constraints.|
||C. Robustness to Disturbance, Environment & Variation|
||8. _Environmental Robustness_ & _Adaptation:_ Operates effectively across varying<br>environmental conditions (e.g. lighting, noise, object/material variation), detecting and<br>alerting for changes or disturbances that could risk execution reliability.|


82 

|**Implication**|**Category/ Criterion**|
|---|---|
||9. _Disturbance Resilience_ & _Continuous Operation:_ Maintains task progress and<br>adherence to commands even when exposed to distractors or minor disturbances,<br>recovering or adapting autonomously when possible. (e.g. arm pushed aside, etc.)<br>D. Learning, Feedback & Continuous Improvement|
||10. _Adaptive Error Learning_ & _Memorisation:_ Continuously learns from past faults,<br>errors, environmental changes, and operator feedback –memorising causes and<br>resolutions to improve future fault/ error detection, prediction, and recovery.|
||11. _Online Confidence_ & _Reliability Assessment:_ Continuously generates a clear<br>reliability confidence score for further operation, quantifying the risk and likelihood of<br>fault occurrence and successful execution.|
||E. Supervision, Oversight & Trust|
||12. _Supervisor Oversight_ & _Fault Review:_ Employs dedicated supervisor components to<br>monitor for faults in execution, hardware/sensor input, and operator commands,<br>critically evaluating instructions and requesting operator engagement for suspected<br>errors.<br>13. _Logging, Explanation_ & _Operator Guidance:_ Logs and communicates faults,<br>anomalies, and noise through varied modalities, providing operators with actionable<br>explanations (what/why/when/how to resolve) and performance insights for<br>transparency and trust.<br>14. _Consistent_ & _Documented Fault Handling:_ Ensures both fault/anomaly-detection<br>and response-behaviours remain reproducible and consistent across time and conditions,<br>with all capabilities and accepted modalities documented and evaluated.|
|**I5:**|A. Specification Compliance|
|**Precision &**<br>**Accuracy**|1. _v/P_&_A Instructability:_ For every task specification, the system can be instructed to<br>meet an explicit v/P&A target.<br>2. _Outcome Logging_ & _Failure Reasoning:_ Gathers/ creates and logs all available<br>v/P&A-relevant task execution metrics (such as velocity and, if sensor capabilities<br>permit, achieved precision & accuracy) after each run. If direct measurement is not<br>possible, the system leverages predicted values, confidence scores, or proxy indicators.<br>For any deviation or failure to meet specified standards, the system documents and<br>explains likely reasons based on the given information.<br>3. _User-Defined Trade-offs:_ Supports explicit operator input for v/P&A-trade-offs (e.g.<br>maximising speed at the cost of precision, or vice versa if either cannot be ensured),<br>before or during execution and ensures system behaviour adapts accordingly.|
||B. Evaluation, Reporting & Confidence|
||4. _v/P_&_A-Confidence Score_ & _Explanation:_ For every execution, outputs a confidence<br>score estimating the predicted likelihood that required v/P&A will be achieved,<br>factoring in task, object/material, environment, and other sensor data. When low<br>confidence is predicted, system can explain likely causes (e.g. out-of-distribution<br>scenario, sensor noise, disturbances).|
||5. _Achievable v/P_&_A-Proposals:_ Alongside the confidence score and explanation, the<br>system can propose and explain alternative v/P&A-combinations likely to succeed in the<br>given context (task, object, environment), helping users adjust requirements if needed.<br>6. _Transparent Documentation of v/P_&_A Capabilities:_ Achievable v/P&A-combinations<br>for every tested task, object, and context is provided alongside the model (including<br>limitations, known influence factors, etc.).<br>C. Consistency & Disturbance Handling|


83 

|**Implication**|**Category/ Criterion**|
|---|---|
||7. _Consistency Over Time_ & _Contexts:_ Demonstrates consistent v/P&A across known<br>tasks, objects, and environments, and under repeated test conditions.<br>8. _Disturbance_ & _Uncertainty Management:_ Identifies and factors in disturbances,<br>distractors, sensor anomalies, or environmental changes when predicting, achieving, and<br>reporting v/P&A metrics. Explains in real-time what current conditions may affect<br>v/P&A and adapts behaviour accordingly.<br>9. _Autonomous v/P_&_A Adaptation:_ Automatically adapts its own v/P&A-settings/<br>targets and solution strategies in response to changing conditions or goals (e.g. sensor<br>quality, energy saving) within the user-defined bounds (e.g. reduces speed within<br>user-defined limits to save energy).|
||D. Learning, Feedback & Continuous Improvement<br>10. _v/P_&_A Learning from Experience and Feedback:_ Memorises and utilises past<br>v/P&A-failures (e.g. slower than/ not as precise as demanded) and successful<br>adaptations of v/P&A to improve prediction confidence, action planning, and further<br>relevant decisions for similar future tasks.<br>11. _HRI/HRC Integration:_ Accepts v/P&A-related user/operator feedback during or<br>after execution to update confidence or task strategy and leverages help from operators<br>or other robots to meet v/P&A requirements.|
||E. External/ Separate Component Integration|
||12. _Skill Integration with Known v/P_&_A:_ Incorporates predefined and learned<br>skills/tools for improved v/P&A outcomes, selecting solutions with documented<br>effectiveness whenever possible.<br>13. _Supervision_ & _Verification Module:_ Includes separated modules or capabilities to<br>explicitly verify actual outcome v/P&A during and post-execution, not just prediction.<br>Alerts/warns model/operator if outcome may not meet requirements, explaining why<br>and offering alternatives.|
|**I6:**|A. Real-Time Robustness & Generality|
|**Real-time**<br>**Performance**|1. _Task, Input_ & _Environment Independence:_ Meets real-time requirements (e.g.<br>inference, control, responsiveness) regardless of task complexity, environment, objects,<br>input modality, number or dimensionality of in/outputs, or presence of distractors,<br>OOD conditions, or hardware degradation – demonstrated through benchmarked<br>worst-case test scenarios on a given hardware-setup.<br>2. _System-wide Real-time Compliance:_ Real-time operation is maintained holistically<br>across all relevant system components – perception, reasoning, actuation, sensing,<br>communication, feedback, and logging – rather than only for a subset.|
||B. Adaptive Resource & Real-Time Management|
||3. _Dynamic Resource Management_ & _Determinism:_ Autonomously adapts compute<br>usage (e.g. through output/inference frequency modulation) to maintain user- or<br>norm-specified real-time targets. When under load or during resource shortages, it<br>disables or degrades non-critical functions to uphold core real-time properties and safety<br>measures. Benchmarked under varying hardware constraints and external disturbances.<br>4. _Autonomous Adaptation_ & _Safety Response:_ Upon detecting real-time violations or<br>imminent deadline risks, triggers fallback routines, prioritises safety-critical<br>functionality, and can alert operators or other systems as needed. Adaptation and<br>prioritisation logic is explainable and logged.|


84 

|**Implication**|**Category/ Criterion**|
|---|---|
||5. _Goal-Responsive Solution Strategies:_ Comprehends and adapts to new or updated<br>user goals and instructions ”in real time” based on current workload – ensuring<br>planning and execution adaptation meets pre-defined latency requirements.<br>C. Monitoring, Reporting, & Continuous Improvement<br>6. _Live Metrics, Logging_ & _Explainability:_ Continuously monitors, reports, and logs<br>real-time metrics (e.g. frequencies, latencies, dropped cycles, deadline adherence), makes<br>these accessible, and provides clear explanations for performance drops, adaptation<br>events, or system changes (e.g. what, why, when a module was throttled/disabled).<br>7. _Real-Time Confidence/Alerting:_ Continuously outputs a confidence score predicting<br>current and future compliance with real-time constraints (factoring in compute status,<br>history, planned actions, hardware utilisation). Issues alerts or recommendations if<br>violation risk increases.<br>8. _Historical Data Utilisation:_ Integrates historical real-time performance/logs and<br>adaptation outcomes to optimise future resource use, prediction, confidence and<br>adaptation strategies, coupled with continued evaluation.<br>9. _Transparent Documentation_ & _Compliance:_ Maintains up-to-date, accessible<br>documentation on real-time system capabilities, adaptation mechanisms, hardware<br>requirements (e.g. which hardware-specifications are required for which set of enabled<br>functionalities) with evaluated compliance. All possible real-time related adaptations,<br>violation cases and countermeasures are documented.|
|**I7:**|A. Hardware & Operational Cost-Efficiency|
|**Cost-**<br>**effectiveness &**<br>**Integration**<br>**Capabilities**|1. _Low-Cost Hardware Readiness:_ Delivers reliable robot control and core model<br>capabilities on commercially available, affordable compute hardware (e.g. edge devices,<br>embedded platforms), supporting lower-spec sensors and actuators.<br>2. _Dynamic Resource Allocation:_ Dynamically adjusts its resource usage – such as<br>modulating inference frequency, simplifying/ deactivating optional model operations,<br>adapting velocity, etc. – minimising energy use or execution duration given current<br>environmental factors (e.g. current required throughput) to reduce operating/<br>production-line costs.<br>B. Universal & Modular Integration|
||3. _Universal Integration without Retraining:_ Seamlessly integrates with diverse robot<br>embodiments, kinematics, sensor and actuator types, and plant automation systems,<br>without requiring model retraining, software changes, or adaptation for each hardware<br>configuration change. Expected performance is preserved wherever hardware capacities<br>allow.<br>4. _Hot-Swapping_ & _Auto-Detection:_ Supports hot-plugging and automatic detection of<br>new, swapped, or removed input/output channels (sensors, actuators, interfaces,<br>communication), updating its operation and configuration with no need for manual<br>operator intervention.<br>C. Commissioning, Flexibility & Self-Adaptation<br>5. _Guided_ & _Autonomous Commissioning:_ Features intuitive commissioning workflows,<br>including automated calibration and adaptation procedures, providing feedback on<br>missing/ expected/ proposed in-/outputs or adjustments, enabling non-expert users to<br>deploy and onboard the model with minimal manual setup.|


85 

|**Implication**|**Category/ Criterion**|
|---|---|
||6. _Flexible Input/Output Adaptation:_ Automatically configures itself to accept changing<br>sensor modalities, command interfaces, and action outputs, functioning consistently<br>even if components are substituted, or temporarily degraded/ missing – requiring no<br>manual software changes.<br>7. _Autonomous Fault Handling_ & _Feedback:_ Autonomously detects and diagnoses<br>sensor, actuator or integration faults and missing interfaces – provides clear, actionable<br>feedback or explanations to users for resolution and continued safe operation.<br>D. Documentation & Integration Performance|
||8. _Comprehensive Integration Documentation:_ Includes detailed, accessible<br>documentation for all supported platforms, integration methods, autonomous<br>adaptation and recognition mechanisms, commissioning and troubleshooting steps,<br>supplemented with example configurations and practical best practices.<br>9. _Integration Performance Monitoring_ & _Learning:_ Continually logs integration<br>performance, adaptation strategies/ speed, and incident recoveries – using historical<br>deployment data to inform, accelerate, and improve future onboarding and<br>commissioning processes.<br>10. _Cost-Reduction Memory_ & _Adaptive Optimisation:_ Systematically records<br>operational experiences that relate to resource and cost efficiency – such as energy-<br>conserving behaviours, internal module optimisations, and hardware usage patterns –<br>and leverages this memory to autonomously propose or implement more cost-effective<br>action plans, configurations, and adaptation strategies in future deployments.|
|**I8:**|A. Capability, Limitation & Reasoning Transparency|
|**Explainability**<br>&<br>**Trust**|1. _Task Feasibility_ & _Capability Explanation:_ Supports clear, user-facing explanations of<br>what tasks it can or cannot solve – including limitations, current capabilities, and the<br>feasibility of the currently instructed task – both before and during execution, with<br>accessible rationale for any constraint.<br>2. _Reason Logging_ & _Accessible Justification:_ Autonomously generates, logs, and<br>exposes the reasoning behind its critical decisions, action choices, adaptations, and<br>detected failures, ensuring each is transparently documented and retrievable for audit,<br>debugging, self-improvement and user review.<br>3. _Explains Influences_ & _Disturbances:_ Provides explanations regarding environmental<br>factors (e.g. lighting, scene setup, object/material properties, distractors, detected<br>disturbances) and how these influence its reasoning, behaviour, or performance, along<br>with advice or solutions for mitigation.|
||B. Self-Assessment, Learning, & Feedback Integration|
||4. _Continuous Self-Assessment with Explainability:_ Consistently self-evaluates<br>capabilities, performance, and limitations and their impacts in the current context (e.g.<br>hardware, sensor setup, noise conditions, distribution shifts), providing the evaluation<br>alongside an explanation and leveraging these insights for ongoing online learning,<br>self-improvement and user-insight.<br>5. _User Feedback_ & _Adaptive Improvement:_ Supports intuitive interfaces for user<br>feedback and corrections during and after execution (e.g. thumbs up/down, follow-up<br>queries, correction inputs), acknowledges understanding, adapts behaviour accordingly,<br>and provides explanations of resulting changes; uses feedback to refine future reasoning.<br>6. _Monitors_ & _Logs Explainability for Learning:_ Keeps persistent records of all<br>generated explainability outputs (reasoning, assessment, error reports), using these logs<br>to continuously improve future behaviours, onboarding, and commissioning processes.|


86 

|**Implication**|**Category/ Criterion**<br>C. Explainability Methods, Interfaces & Outputs|
|---|---|
||7. _Flexible, Intuitive Explainability Interfaces:_ Offers explanation outputs in multiple<br>modalities (text, speech, visualisation, etc.), supporting both non-expert operators and<br>technical users, with methods to visualise/explain impact of user commands,<br>input/output importance, intermediate steps, and internal processes at runtime.<br>8. _Confidence Score Explanation:_ All confidence scores (for actions, predictions, or<br>decisions) are supplied with user-facing explanations – detailing what influenced high or<br>low values, such as data loss, fallback mode, sensor unreliability, or ambiguous scene<br>attributes.|
||9. _Explainability Across System Components:_ Integrates explainability tools and<br>interfaces across all modules, enabling explainable actions, outputs, and internal<br>reasoning during setup, operation, debugging, and benchmarking; all methods are<br>thoroughly documented with guidance for triggering and interpreting results.|
||D. Security, Compliance, & Benchmarking Explainability|
||10. _Security_ & _Authorisation Feedback:_ Detects and explains potential security issues,<br>adversarial attacks, or authorisation events – providing specifics on why the event was<br>flagged, input used, type of threat, and how to strengthen defences or permissions for<br>future operations.<br>11. _Rule_ & _Norm Compliance with Explainability:_ Evaluates and explains compliance<br>with operational guidelines, safety norms, and domain-specific rules (both upon being<br>instructed and during/after execution), visualising/documenting adherence, deviations,<br>and model reasoning behind its decision.<br>12. _Performance Benchmarking_ & _OOD Feedback:_ Integration of explainability<br>methods in benchmarking, evaluation, and reporting – e.g. visualising focus,<br>highlighting difficulties in OOD situations, or explaining how improvements, data<br>changes, or model modifications affect learned skills or generalisation, etc.<br>E. Trust & Transparency during Runtime<br>13. _Behaviour Consistency_ & _Pre-Adaptation Notification:_ Maintains consistent,<br>transparent explanations for identical inputs and conditions, avoids “super-hero<br>syndrome” (thinking to be capable to solve every task), and informs the user before<br>adapting behaviour due to error, environment change, or new context.<br>14. _Error, Anomaly_ & _Safeguard Explanations:_ Immediately triggers explanation<br>processes for detected errors, anomalies, or failed safeguards – detailing what happened,<br>why, and the recovery strategies attempted or proposed. Explanation is automatically<br>provided to relevant system components/ logs/ etc.|
|**I9:**|A. Multimodal Acceptance & Fusion|
|**Sensor Fusion**<br>&<br>**Perception**|1. _Multimodal Sensor Acceptance_ & _Fusion:_ Accepts diverse sensors and supports their<br>real-time fusion and processing across modalities (visual, tactile, audio, etc.), including<br>redundant interchangeable sensors, with the ability to interpret and combine inputs<br>from multiple simultaneous sources for robust perception.<br>2. _Flexible Input Combination_ & _Goal Specification:_ Accepts task instructions, goals,<br>and feedback through multiple modalities (speech/text, gesture, image, etc.), and can<br>leverage several modalities simultaneously for improved perception, understanding, and<br>command robustness.<br>3. _Security in Sensor Operations:_ Utilises various sensor sources/ modalities to detect<br>adversarial attacks, facilitates secure authorisation, and ensures safe detection of<br>humans/workers.|


87 

##### **Implication** 


##### **Category/ Criterion** 

##### B. Input Monitoring, Fault Tolerance & Adaptation 

4. _Continuous Input Monitoring_ & _Feedback:_ Continuously checks sensor inputs for noise, faults, degradation, absence, or sub-optimal orientation, providing real-time feedback during integration, commissioning and operation, reporting missing or degraded inputs as well as recommendations for improvement. 5. _Robust Fault Tolerance_ & _Degradation Handling:_ Detects and actively compensates for sensor failures, degradation, or external disturbances by dynamically shifting input weighting, switching perception strategies, or prioritising the most reliable sensor(s) for the current scene, environment, and task context. 6. _Autonomous Disturbance Recognition_ & _Countermeasures:_ Recognises environmental disturbances that critically affect perception (e.g. poor lighting, moisture, obstructed view) and initiates context-sensitive countermeasures (like halting, alerting users, removing obstacles, or activating cleaning routines), and adapts perception strategies online. 

##### C. Dynamic Input Prioritisation & Adaptation 

7. _Dynamic Sensor Prioritisation:_ Automatically ranks and prioritises active sensors and modalities based on current instruction, scene conditions, quality, relevance, historical context and reliability, adapting input strategy in real-time to environmental changes and operational demands. 8. _Online Learning for Perception Skills:_ Continuously learns and adapts perception strategy (e.g. how to interpret or counteract noisy or degraded sensor values, shifting focus to non-degraded sensors, . . . ) using historical data and reasoning explanations to improve future sensor fusion and perception capabilities. 

##### D. Scene Understanding, Interpretation & Output 

9. _Comprehensive Scene Understanding via Fusion:_ Recognises objects, materials, spatial arrangements and environmental constraints by integrating information from multiple, complementary modalities – supplies rich scene interpretation, spatial awareness, and accurate environmental representations for downstream robot control. 10. _Perceptual Confidence_ & _Explanation Output:_ Provides a perceptual confidence score, summarising the certainty of scene/object perception and input quality. Complemented by interpreting input importance (which sensors/modalities influenced results) and supply of user-friendly explanations visualising/ describing reasoning behind understanding, degraded input handling, and current limitations. 

11. _Perceptual Feature Exposure_ & _Modularity:_ Exposes interpretable intermediate representations and perceptual features to system components or external interfaces, supporting modularity, human supervision, and transparent debugging of perception skills. 

E. Evaluation, Documentation & Knowledge Exchange 12. _Modular Integration_ & _Documentation:_ Enables flexible, exchangeable or adaptive observation spaces (autonomous/manual adaptation; fine-tuning optional) with support for hot-swapping sensor setups, providing clear feedback during integration and maintaining up-to-date documentation of all supported sensor types, modality usage, and perception features. 

13. _Perception Evaluation_ & _Benchmarking:_ Benchmarks and documents perception skills (input importance ranking, noise adaptation, consistency, and reproducibility), and supplies results for model evaluation, external audit, and improvement. 

14. _Peer-to-Peer Perception Knowledge Exchange:_ Can exchange sensor/perception information and interpretations with other systems, enabling collective/global perception enhancement and collaborative scene/environmental understanding. 

88 

|**Implication**|**Category/ Criterion**|
|---|---|
|**I10:**|A. Coverage of Tasks, Domains, & Environments|
|**Standardised**<br>**Benchmarking**<br>&<br>**Evaluation**|1. _Benchmark Diversity_ & _Scope:_ Evaluated using standardised benchmarks that span a<br>wide range of tasks, domains, environments, object types, and material properties –<br>including known, partially known, and unknown scenarios – explicitly testing<br>performance in worst-case distribution shift or OOD situations.<br>2. _Hardware Platform Benchmarking:_ Evaluates model on multiple hardware platforms/<br>uses a hardware-aware benchmark, documenting resource utilisation, energy<br>consumption, real-time performance, and cost-effectiveness across devices and<br>sensor/actuator setups.<br>B. Robustness, Generalisation & Transparency|
||3. _Repeatability_ & _Reproducibility:_ Demonstrates repeatable, reproducible<br>model/system behaviour in benchmark runs, validating consistency over multiple trials,<br>hardware settings, and environmental variations.<br>4. _Robustness_ & _Fault Tolerance Evaluation:_ Systematically benchmarks performance<br>against faults, disturbances, distractor objects, sensor degradation, and intentional<br>adversarial attacks; measures recovery strategies, fallback/safeguard execution, and<br>online adaptation when exposed to (un)seen disturbances.<br>5. _Generalisation_ & _Adaptation Assessment:_ Evaluates the model’s generalisation and<br>online adaptation capabilities – including response to distribution shifts, novel<br>commands, unknown inputs, and task or environmental changes – using both synthetic<br>and real-world scenarios.<br>6. _Transparent Metrics_ & _Reporting:_ Publishes clear, traceable benchmark metrics –<br>including performance, accuracy (v/P&A), safety, robustness, fault tolerance, energy<br>usage, real-time performance and compliance – with full documentation for all test<br>scenarios.|
||C. Instruction, Output & Integration Assessment<br>7. _Instruction, Command_ & _Modality Coverage:_ Benchmarks instructability and goal<br>specification for all supported input modalities (e.g. speech, text, images, gestures),<br>focusing on interpretation accuracy, and solution strategy adherence.<br>8. _Integration_ & _Commissioning Evaluation:_ Assesses ease and effectiveness of<br>integration into different systems and workflows, including input/output adaptation,<br>fine-tuning procedures, and usability before, during, and after commissioning.|


D. Specific Benchmarking 9. _Module_ & _Skill-Specific Benchmarking:_ Separate evaluation of (a) independent core modules, learned skills, tool selection quality, etc. and (b) whole-system-level performance/ metrics. 10. _Safety, Security_ & _Norm Compliance Validation:_ Explicitly evaluates implemented authorisation, safety features, resilience against adversarial inputs, and system compliance with relevant industrial standards, rules, and domain-specific guidelines. 11. _Explainability, Reasoning_ & _Feedback Benchmarks:_ Evaluation of built-in explainability methods, overall reasoning transparency, feedback usage/ usability, and correction/ user guidance understanding – demonstrating black-box mitigation and feedback consistency. 12. _Data Requirement_ & _Autonomous Runtime Assessment:_ Verifies the model’s data requirements for pretraining, fine-tuning, and online adaptation. Benchmarks autonomous self-evaluation during runtime learning, adaptation, and self-improvement. 

89 

|**Implication**|**Category/ Criterion**|
|---|---|
||13. _Human Interaction_ & _Object Recognition Evaluation:_ Evaluates human-robot<br>interaction and cooperation capabilities. Benchmarks HRC/HRI-related object/human<br>recognition for known and unknown cases, considering detection rates, explanation<br>quality, and adaptation of resulting behaviour.|
|**I11:**|A. Data Efficiency & Finetuning|
|**Data**<br>**Requirements**<br>&<br>**Usage**|1. _Low-Data Adaptation_ & _Few-Shot Requirements:_ Needs only few or zero new<br>examples for effective adaptation to novel tasks, environments, hardware, or operators,<br>using suitable techniques (e.g. in-context learning, online self-adaptation, modular<br>fine-tuning) with minimal resource utilisation.<br>2. _Efficient Task, Environment_ & _Modality Adaptation:_ Supports adaptation of<br>observation/action spaces or input modalities without needing retraining or extensive<br>new data and supports independent module adaptation to minimise both overall and<br>domain-specific data requirements.<br>B. Pretraining Coverage & Robustness<br>3. _Comprehensive_ & _Diverse Pretraining Dataset:_ Pretraining covers broad task types,<br>environments, domains, object/material variations, instruction modalities, distractors,<br>noise, faults, adversarial attacks, redundant/fallback routines, and safety/data privacy<br>scenarios, using both synthetic and real-world data for robust generalisation and OOD<br>handling.<br>4. _Documented Data Composition_ & _Simulation-Real Transfer:_ Maintains accessible<br>documentation on training/finetuning data composition, variation, and procedures.<br>Including evaluation of transfer between simulation and real-world settings and tracks<br>performance on transfer degradation.|
||C. Data Sufficiency, Self-Assessment & Explainability|
||5. _Automatic Data Sufficiency Assessment_ & _Feedback:_ Continuously analyses historic<br>and incoming data for sufficiency, coverage gaps, redundancy, and quality issues during<br>adaptation or operation. Provides alerts and actionable recommendations for missing,<br>underrepresented, or low-quality data (e.g. based on task, scene understanding, . . . ).<br>6. _Explainability on Data Usage_ & _Improvement:_ Supplies explainable analyses of data<br>composition/ identified gaps, adaptation impact, improvement, and focus shift during<br>training/finetuning. Recommends targeted data enrichment or refinement to address<br>detected blind spots or weaknesses.|
||D. Data Flexibility, Interface & Compliance|
||7. _Flexible Data Type Acceptance:_ Accepts and learns (on- and offline) from diverse data<br>formats and modalities (e.g. trajectory, demonstration, egocentric, multi-modal sensory).<br>8. _Compliance with Privacy, Ethics_ & _Law:_ Ensures all data usage can comply with<br>provided legal, ethical, and corporate policies – leveraging privacy safeguards (e.g. data<br>anonymisation, operator-specific data isolation, encrypted logging, . . . ) where needed.<br>E. Ongoing Monitoring, Confidence & Robustness|
||9. _Ongoing Adaptation/Finetuning Confidence Scores:_ Outputs initial and ongoing<br>confidence scores after (fine)tuning and during online adaptation, estimating both data<br>sufficiency/appropriateness and the model’s expected operational robustness and<br>readiness under changing environments, hardware, or tasks.<br>10. _Resilience Through Redundancy_ & _Fault Tolerance:_ Incorporates redundancy, noise,<br>faults, and fallback examples in pretraining and fine-tuning to support robust<br>adaptation, autonomous countermeasure activation, and continued reliable operation<br>under adverse data scenarios.|


90 

**Implication Category/ Criterion** 11. _Self-Assessment to Reduce Input_ & _Modalities:_ Evaluates and documents own data and input usage, minimising dependence on unnecessary modalities and optimising resource efficiency during all operational phases. 

91 

## **Appendix D RFM-Overview** 

92 

**Table D5:** Overview of all 324 identified RFMs that include manipulation capabilities (for control & integrated; see Section 3.2 for composition details). _Reporting their proportional industrial applicability ratings for each individual implication, and a total score over all implications. Per-criterion ratings are created utilising the publication’s context, by leveraging our LLM-based pipeline as described in Section 8.1. Values are rounded to two decimal places._ 

|**Ref**|**Model**<br>|**Total**_↓_|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Gemini|||||||||||||
|[157]|Robotics<br>1.5|0.12|0.44|0.06|0.07|0.07|0.00|0.00|0.00|0.07|0.14|0.23|0.09|
|[158]|Collab<br>VLA|0.11|0.28|0.00|0.20|0.07|0.08|0.11|0.00|0.07|0.21|0.08|0.09|
|[159]|GF-<br>VLA|0.11|0.28|0.00|0.00|0.14|0.08|0.00|0.00|0.07|0.14|0.23|0.27|
|[6]|OneTwo<br>VLA|0.11|0.33|0.00|0.20|0.14|0.00|0.11|0.10|0.07|0.14|0.00|0.09|
|[160]|SC-<br>VLA|0.11|0.33|0.06|0.00|0.21|0.23|0.11|0.00|0.00|0.00|0.15|0.09|
|[164]|HiBer<br>NAC|0.10|0.22|0.11|0.00|0.00|0.08|0.11|0.10|0.00|0.21|0.15|0.09|
|[143]|Sirius-<br>Fleet|0.10|0.39|0.22|0.00|0.14|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[211]|Tactile-<br>VLA|0.10|0.28|0.00|0.00|0.07|0.15|0.00|0.00|0.14|0.07|0.15|0.18|
|[212]|DexGrasp<br>VLA|0.09|0.28|0.00|0.00|0.07|0.08|0.00|0.00|0.07|0.00|0.31|0.18|
|[213]|Gemini<br>Robotics|0.09|0.22|0.00|0.00|0.07|0.00|0.00|0.00|0.14|0.14|0.23|0.18|
|[214]|Robix|0.09|0.22|0.11|0.20|0.00|0.00|0.00|0.00|0.00|0.00|0.31|0.09|
|[215]|VITA-<br>E|0.09|0.28|0.11|0.20|0.00|0.00|0.11|0.00|0.07|0.00|0.08|0.09|
|[167]|PaLM-<br>E|0.09|0.33|0.00|0.00|0.29|0.00|0.00|0.00|0.00|0.07|0.00|0.18|
|[216]|RACER|0.09|0.28|0.00|0.00|0.07|0.00|0.00|0.00|0.14|0.00|0.15|0.27|
|[217]|Embodied-<br>R1|0.09|0.28|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.14|0.23|0.18|
|[218]|VLMimic|0.08|0.33|0.00|0.00|0.14|0.00|0.00|0.00|0.07|0.00|0.15|0.09|
|[219]|Intern<br>VLA-<br>M1|0.08|0.28|0.00|0.07|0.07|0.00|0.00|0.00|0.00|0.07|0.15|0.18|
|[220]|FPC-<br>VLA|0.08|0.28|0.06|0.00|0.14|0.08|0.00|0.00|0.00|0.00|0.23|0.00|
|[163]|HAMSTE|R 0.07|0.11|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.07|0.23|0.36|
|[221]|CoA-<br>VLA|0.07|0.11|0.00|0.00|0.00|0.08|0.00|0.10|0.07|0.14|0.23|0.09|
|[222]|ThinkAct|0.07|0.28|0.00|0.00|0.14|0.00|0.00|0.00|0.00|0.00|0.15|0.18|


_continued on next page_ 

93 

|**Ref**|**Model**|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[223]|MolmoAct|0.07|0.17|0.00|0.07|0.00|0.08|0.00|0.00|0.07|0.07|0.15|0.18|
|[224]|RT-H|0.07|0.22|0.00|0.13|0.00|0.08|0.00|0.00|0.07|0.07|0.00|0.18|
|[18]|OpenVLA|0.07|0.22|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.38|0.09|
|[5]|RoboDual|0.07|0.17|0.00|0.00|0.00|0.00|0.11|0.00|0.00|0.07|0.23|0.27|
|[225]|VoxPoser|0.07|0.17|0.00|0.13|0.07|0.15|0.00|0.00|0.00|0.00|0.15|0.09|
|[169]|UniVLA|0.07|0.11|0.00|0.00|0.00|0.08|0.00|0.00|0.07|0.00|0.23|0.36|
|[226]|CLOVER|0.07|0.28|0.00|0.00|0.07|0.00|0.00|0.00|0.07|0.00|0.23|0.00|
|[166]|NanoVLA|0.07|0.11|0.00|0.00|0.07|0.08|0.00|0.20|0.00|0.00|0.31|0.00|
|[227]|CLIP-<br>RT|0.07|0.17|0.00|0.13|0.07|0.00|0.00|0.00|0.07|0.00|0.08|0.18|
|[165]|LCIL|0.07|0.11|0.00|0.27|0.00|0.00|0.11|0.00|0.00|0.00|0.08|0.18|
|[228]|Switch<br>VLA|0.06|0.22|0.00|0.07|0.00|0.00|0.11|0.00|0.00|0.00|0.08|0.18|
|[229]|UVA|0.06|0.11|0.00|0.00|0.07|0.08|0.00|0.00|0.00|0.00|0.31|0.09|
|[230]|IDAGC|0.06|0.11|0.00|0.13|0.00|0.00|0.00|0.00|0.00|0.14|0.08|0.18|
|[231]|A2|0.06|0.06|0.00|0.00|0.00|0.15|0.00|0.00|0.07|0.07|0.15|0.18|
|[232]|SuSIE|0.06|0.11|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.23|0.27|
|[233]|Omni<br>Manip|0.06|0.28|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[234]|FoAM|0.06|0.17|0.00|0.00|0.07|0.08|0.00|0.00|0.00|0.00|0.08|0.27|
|[235]|VTLA|0.06|0.06|0.00|0.00|0.14|0.08|0.00|0.00|0.00|0.07|0.15|0.18|
|[236]|GNFactor|0.06|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.15|0.18|
|[237]|Diffusion-<br>VLA|0.06|0.22|0.00|0.00|0.07|0.00|0.00|0.00|0.07|0.07|0.00|0.18|
|[238]|GR-<br>MG|0.06|0.22|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.23|0.18|
|[239]|RT-<br>Affordance|<sup>0.06</sup>|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.08|0.27|
|[240]|Instruct<br>VLA|0.06|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.23|0.09|
|[241]|Robo<br>Agent|0.05|0.17|0.00|0.00|0.14|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[242]|PointVLA|0.05|0.06|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.23|0.27|
|[243]|EO-1|0.05|0.11|0.00|0.00|0.00|0.00|0.11|0.00|0.00|0.07|0.15|0.18|
|[244]|Reason<br>Manip|0.05|0.22|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.14|0.08|0.09|
|[245]|WALL-<br>OSS|0.05|0.17|0.00|0.07|0.00|0.00|0.11|0.00|0.00|0.00|0.08|0.18|
|[246]|Vidar|0.05|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.15|0.27|
|[247]|Cronus<br>VLA|0.05|0.06|0.00|0.00|0.14|0.00|0.00|0.00|0.07|0.00|0.23|0.09|


_continued on next page_ 

94 

|**Ref**|**Model**<br>|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[248]|OG-<br>VLA|0.05|0.11|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.31|0.09|
|[249]|OTTER|0.05|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.23|0.09|
|[250]|Giga<br>Brain-0|0.05|0.06|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.14|0.08|0.27|
|[251]|Emma-<br>X|0.05|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.23|0.09|
|[252]|LeVERB|0.05|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.23|0.18|
|[253]|ManiFlow|0.05|0.11|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.23|0.18|
|[1]|Diffusion<br>Policy|0.05|0.11|0.06|0.00|0.14|0.08|0.11|0.00|0.00|0.00|0.08|0.00|
|[254]|MOO|0.05|0.22|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.27|
|[255]|MLA|0.05|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.14|0.15|0.09|
|[256]|GemBench|0.05|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.31|0.00|
|[257]|IDHAP|0.05|0.17|0.00|0.00|0.07|0.00|0.00|0.00|0.07|0.00|0.08|0.18|
|[258]|Bridge<br>VLA|0.05|0.17|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.23|0.09|
||PRO-|||||||||||||
|[259]|GRAM<br>PORT|0.05|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.15|0.18|
|[260]|RAM|0.05|0.22|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.08|0.18|
|[261]|VeBrain|0.05|0.28|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.08|0.09|
|[262]|UniAct|0.05|0.11|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.23|0.18|
|[263]|Actra|0.05|0.17|0.00|0.00|0.07|0.00|0.00|0.00|0.07|0.00|0.08|0.09|
|[264]|RVT-2|0.05|0.17|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[265]|TUDP|0.05|0.00|0.00|0.00|0.00|0.08|0.00|0.10|0.00|0.07|0.15|0.18|
|[266]|UniCoD|0.05|0.17|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.15|0.09|
|[267]|RT-<br>Trajectory|0.05|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.15|0.18|
|[268]|InSpire|0.05|0.22|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.15|0.00|
|[269]|TVVE|0.05|0.11|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.31|0.00|
|[270]|HPT|0.05|0.06|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.15|0.27|
|[271]|Hume|0.05|0.22|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.15|0.00|
|[272]|LCIL2|0.05|0.11|0.00|0.00|0.07|0.00|0.00|0.00|0.07|0.07|0.08|0.09|
|[273]|LAP-<br>VLA|0.05|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.23|0.27|
|[28]|RT-1|0.05|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.15|0.09|
|[161]|FuSe|0.05|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.21|0.00|0.27|
|[274]|SAM2<br>Act|0.05|0.11|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.31|0.00|


_continued on next page_ 

95 

|**Ref**|**Model**<br>Video|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[275]|Predic-<br>tion<br>Policy|0.05|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.15|0.27|
|[276]|Lan-<br>o3dp|0.05|0.17|0.06|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[277]|Interleave<br>VLA|0.05|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.08|0.18|
|[278]|LBMfDM|0.05|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.23|0.27|
|[279]|MResT|0.05|0.11|0.00|0.00|0.00|0.08|0.11|0.00|0.00|0.07|0.08|0.09|
|[162]|GraphCoT<br>VLA|0.05|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.21|0.14|0.00|0.09|
|[280]|ARM4R|0.05|0.17|0.00|0.00|0.07|0.08|0.00|0.00|0.00|0.00|0.08|0.09|
|[281]|SPECI|0.04|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.18|
|[282]|Gato|0.04|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.15|0.27|
|[283]|Evo-0|0.04|0.11|0.00|0.00|0.07|0.08|0.00|0.00|0.00|0.00|0.15|0.00|
|[284]|MoT<br>VLA|0.04|0.11|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[285]|GEVRM|0.04|0.11|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[286]|Tiny<br>VLA|0.04|0.17|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.15|0.00|
|[287]|LoHo<br>VLA|0.04|0.22|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[288]|Memory<br>VLA|0.04|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.23|0.00|
|[289]|RDT-<br>1B|0.04|0.11|0.00|0.00|0.00|0.08|0.11|0.00|0.00|0.00|0.00|0.18|
|[290]|GR00T<br>N1|0.04|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.27|
|[291]|GR-1|0.04|0.17|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[292]|VIMA|0.04|0.17|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[293]|BC-Z|0.04|0.11|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|
|[294]|Intention<br>VLA|0.04|0.17|0.00|0.00|0.00|0.00|0.11|0.00|0.00|0.07|0.08|0.00|
|[295]|CLIPort|0.04|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.23|0.09|
|[7]|Fast-in-<br>Slow|0.04|0.17|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.08|0.09|
|[296]|CAGE|0.04|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.23|0.09|
|[297]|SKIL|0.04|0.06|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.15|0.18|
|[298]|AR-<br>VRM|0.04|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.08|0.18|
|[299]|GeoVLA|0.04|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.31|0.09|


_continued on next page_ 

96 

|**Ref**|**Model**<br>Skill|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[300]|Dif-<br>fuser|0.04|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.15|0.00|
|[301]|Goal-<br>VLA|0.04|0.11|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.15|0.09|
|[302]|VOTE|0.04|0.11|0.00|0.00|0.00|0.08|0.00|0.10|0.00|0.00|0.15|0.00|
|[303]|AffordDP|0.04|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.27|
|[304]|LangToMo|0.04|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.15|0.09|
|[305]|GR-2|0.04|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[20]|_π_0_∗._6|0.04|0.00|0.00|0.00|0.07|0.15|0.00|0.00|0.07|0.00|0.08|0.09|
|[306]|FLOWER|0.04|0.22|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.00|
|[307]|MinD|0.04|0.00|0.00|0.00|0.14|0.00|0.00|0.00|0.07|0.07|0.15|0.00|
|[308]|Moto|0.04|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.08|0.18|
|[309]|CACTI|0.04|0.22|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[310]|TCADP-<br>LG|0.04|0.06|0.00|0.00|0.00|0.08|0.00|0.10|0.00|0.07|0.08|0.09|
|[311]|LCB|0.04|0.11|0.00|0.07|0.00|0.00|0.00|0.10|0.07|0.07|0.00|0.00|
|[168]|Smol<br>VLA|0.04|0.06|0.00|0.00|0.07|0.00|0.00|0.20|0.00|0.00|0.15|0.00|
|[312]|cVLA|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.27|
|[313]|GR-3|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|
|[314]|Hyper<br>VLA|0.03|0.06|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.15|0.09|
|[315]|E2VLA|0.03|0.06|0.00|0.00|0.07|0.08|0.00|0.00|0.07|0.00|0.00|0.09|
|[316]|Robo<br>Brain|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.14|0.00|0.08|0.09|
|[317]|OmniD|0.03|0.00|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.23|0.09|
|[318]|Force<br>VLA|0.03|0.11|0.00|0.00|0.14|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[319]|VLMPC|0.03|0.11|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.15|0.00|
|[320]|AMPLIFY|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.18|
|[321]|ReFine<br>VLA|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.14|0.07|0.00|0.00|
|[322]|CogACT|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.23|0.00|
|[323]|GRAPE|0.03|0.11|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.15|0.00|
|[324]|DNAct|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.15|0.00|
|[325]|Magma|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.27|
|[326]|GROOT-<br>2|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.08|0.09|
|[327]|TriVLA|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[328]|This&That|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.15|0.09|
|[329]|TARAD|0.03|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|


_continued on next page_ 

97 

|**Ref**|**Model**|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[330]|DeL-<br>TaCo|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.18|
|[331]|Concept2<br>Robot|0.03|0.06|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.15|0.09|
|[332]|Point<br>Map<br>Policy|0.03|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.15|0.09|
|[333]|LP-ZS-<br>LH|0.03|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[334]|VidBot|0.03|0.06|0.06|0.00|0.00|0.00|0.11|0.00|0.00|0.00|0.08|0.09|
|[335]|SayCan|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.08|0.00|
|[336]|AC-<br>DiT|0.03|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.15|0.09|
|[337]|VLAS|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.15|0.09|
|[338]|PALO|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[339]|Trace<br>VLA|0.03|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.00|
|[340]|Villa-X<br>Sparse|0.03|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.23|0.09|
|[341]|Diffu-<br>sion<br>Policy|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.00|0.09|
|[342]|GRM-<br>BALD|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.18|
|[343]|Gen2Act<br>|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.00|0.18|
|[344]|Robo<br>Tron-<br>Mani|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.15|0.09|
|[345]|SAM-E|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.08|0.09|
|[346]|Hybrid<br>VLA|0.03|0.11|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.00|
|[147]|LATTE|0.03|0.11|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.08|0.09|
|[347]|CoMo|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.18|
|[348]|HiRT|0.03|0.17|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.00|
|[349]|FLARE|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.18|
|[350]|Seer|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[351]|dVLA|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.07|0.00|0.09|
|[352]|TPM|0.03|0.06|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[353]|Dita|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
||Think|||||||||||||
|[354]|Small-<br>PPL|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.08|0.09|
|[355]|LDRL|0.03|0.11|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.08|0.00|


_continued on next page_ 

98 

|**Ref**|**Model**|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Rynn|||||||||||||
|[356]|VLA-<br>001|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.00|0.08|0.09|
|[357]|BFA<br>MM|0.03|0.00|0.00|0.00|0.00|0.00|0.00|0.10|0.07|0.07|0.08|0.00|
|[358]|Diff<br>Tran|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|
|[359]|Robo<br>LL-RL|0.03|0.06|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.15|0.00|
|[360]|LAA<br>VTDC|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[361]|Dobb·E|0.03|0.00|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.00|0.15|0.09|
|[19]|Robo<br>Flamingo|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.00|0.08|0.09|
|[362]|Spatial<br>VLA|0.03|0.11|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[27]|_π_0_._5<br>|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[363]|Grasp<br>VLA|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|
|[364]|FP3|0.03|0.11|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[365]|_π_0-<br>Text<br>Latent|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.15|0.00|
|[366]|ICRT|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[367]|3D-<br>CAVLA|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.08|0.09|
|[368]|OE-<br>VLA|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.09|
|[369]|LEO|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.08|0.09|
|[370]|Cog<br>VLA|0.03|0.06|0.00|0.00|0.00|0.08|0.00|0.00|0.07|0.00|0.08|0.00|
|[371]|Recon<br>VLA|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.08|0.00|
||Real|||||||||||||
|[372]|World-<br>RL-<br>MVP|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|
|[373]|DexVLA|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[374]|GLVA|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.00|
||3DDif-|||||||||||||
|[375]|<br>fusion<br>Policy|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[376]|Being-<br>H0|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|


_continued on next page_ 

99 

|**Ref**|**Model**<br>|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[377]|AirExo-<br>2|0.03|0.00|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.07|0.15|0.00|
|[29]|RT-2|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[378]|Perceiver-<br>Actor|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|
|[379]|H-RDT|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|
|[380]|Tra-<br>MoE|0.03|0.00|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.15|0.09|
|[381]|3D-<br>VLA|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.08|0.09|
|[382]|ILRMS|0.03|0.00|0.00|0.00|0.07|0.00|0.00|0.00|0.07|0.00|0.00|0.18|
|[383]|VLA-<br>Adapter<br>|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.23|0.00|
|[384]|Lang<br>Cond-<br>RoboIL|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[385]|Bi-<br>VLA|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[386]|DyWA|0.03|0.06|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.15|0.00|
|[3]|Dream<br>VLA<br>Diffusion|0.03|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.08|0.09|
|[387]|Trans-<br>former<br>Policy|0.03|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.00|0.09|
|[26]|_π_0|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[388]|Rozum<br>Former|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.27|
|[389]|RoboCat|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[390]|IGOR|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[391]|ACT|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.00|0.08|0.09|
|[392]|ImitDiff|0.02|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[393]|Surfer|0.02|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[394]|HyT-<br>VLA|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.15|0.00|
|[395]|Open<br>VLA<br>OFT|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[396]|VLM-<br>TDP|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.00|
|[397]|GRIF|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|
|[398]|RVT|0.02|0.00|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.15|0.00|
|[399]|Instruct<br>RL|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|


_continued on next page_ 

100 

|**Ref**|**Model**|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[400]|CDP|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[401]|DTP|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[402]|Flow<br>VLA|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[403]|FLASH<br>VLA|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.00|0.08|0.09|
|[404]|Robo-<br>MUTUAL|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[405]|FLIP|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.08|0.00|
|[406]|LCDOM|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[407]|PD-<br>VLA|0.02|0.06|0.00|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[408]|Cross<br>EmbL|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[409]|Cross<br>Former|0.02|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[410]|ReinboT|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|
|[411]|AdaMoE|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.00|
|[412]|OWL×T5<br>|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[413]|�-<br>agent|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.08|0.00|
|[414]|Surfer|0.02|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[415]|ADDP-<br>AVP|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|
|[416]|OCI|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.09|
|[417]|PLEX|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[418]|EnerVerse|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.08|0.09|
|[419]|ARP|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.08|0.00|
|[420]|Robo<br>Ground|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.08|0.00|
|[421]|DMPEL|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[422]|Object<br>VLA|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.18|
|[423]|Robo<br>Uni<br>View<br>Discrete|0.02|0.06|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.08|0.00|
|[2]|Diffu-<br>sion<br>VLA|0.02|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[424]|ROSA|0.02|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[425]|CoT-<br>VLA|0.02|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.08|0.09|


_continued on next page_ 

101 

|**Ref**|**Model**|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[426]|PDFactor|0.02|0.00|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.08|0.09|
|[427]|VoxAct-<br>B|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.00|0.08|0.00|
|[428]|Long-<br>VLA|0.02|0.11|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[429]|Octo|0.02|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[430]|CrossT5|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[431]|PAFMF|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.00|
|[432]|Humanoid<br>VLA|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[433]|Robo<br>BERT|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[434]|OMLA|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[4]|Dreamitate|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.00|
|[435]|EgoVLA|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[436]|LanCon-<br>Learn|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[437]|CtF Q-<br>attention|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[438]|DAWN|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.08|0.00|
|[439]|StaMo|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[440]|Tenma|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[441]|VQ-<br>VLA|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[442]|VLA-<br>Arm-<br>TDMTO|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.15|0.00|
|[443]|Vlaser|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[444]|DualMind|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.00|0.09|
|[445]|M2Distill|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[446]|VidMan|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[447]|DP-<br>VLA|0.01|0.00|0.00|0.00|0.00|0.00|0.11|0.00|0.00|0.00|0.08|0.00|
|[448]|F1|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.08|0.00|
|[153]|HAMLET|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.08|0.00|
|[449]|4D-<br>VLA|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[450]|Act3D|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[451]|UP-<br>VLA|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[452]|ABM|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[453]|World<br>VLA|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|


_continued on next page_ 

102 

|**Ref**|**Model**|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[454]|UniVLA|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[455]|BitVLA<br>|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.00|0.00|0.09|
|[456]|Chat<br>VLA-2|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[457]|DeeR-<br>VLA|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.00|0.00|0.00|
|[458]|Spatial<br>Traces|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[459]|ReVLA|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[460]|Alpha<br>Block|0.01|0.06|0.00|0.07|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|[461]|PACT|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.18|
|[462]|Natural<br>VLM|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[463]|Omni<br>VTLA|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.00|0.09|
|[464]|KIVLA|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[465]|KALM|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[466]|Light<br>VLA|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.10|0.07|0.00|0.00|0.00|
|[467]|MBA|0.01|0.00|0.00|0.00|0.00|0.08|0.00|0.00|0.00|0.00|0.08|0.00|
|[468]|Avi|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.07|0.00|0.00|
|[469]|Chat<br>VLA|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[470]|MIDAS|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[471]|Meta<br>RL-LI|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[472]|BLM1<br>Mini|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[473]|Dif-<br>fuser|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[474]|Discrete<br>Policy|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.09|
|[475]|_π_0_._6<br>(model<br>card)|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[476]|NORA|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|[477]|VIRT|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[478]|PolarNet|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[479]|MoLe-<br>VLA|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.10|0.00|0.00|0.00|0.00|
|[480]|AgiBot<br>World<br>Colosseo|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|


_continued on next page_ 

103 

|**Ref**|**Model**<br>|**Total**|**I1**|**I2**|**I3**|**I4**|**I5**|**I6**|**I7**|**I8**|**I9**|**I10**|**I11**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|[481]|Q-<br>Trans-<br>former|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[482]|LLaDA-<br>VLA|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|[483]|NBAgent|0.01|0.06|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|[484]|LiteVLP|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[485]|Ex-<br>PERACT|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[486]|Robo<br>Mamba|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[487]|Context<br>VLA|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[488]|RetoVLA<br>|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.08|0.00|
|[489]|OC-<br>VLA|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[490]|Control<br>VLA|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[491]|RoboDiT<br>|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[492]|EC-<br>Flow|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[493]|Chained<br>Dif-<br>fuser|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[494]|OFA<br>VAE|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[495]|-<br>Rob<br>Manip|0.01|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.09|
|[496]|Geo<br>Aware-<br>VLA|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|[497]|CEED-<br>VLA|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|[498]|Spec-<br>VLA|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
||Robo|||||||||||||
|[499]|Flamingo-<br>Plus|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|[500]|Robotic-<br>CLIP|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|[501]|EdgeVLA|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|[502]|LLARVA|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|[503]|VGGT-<br>DP|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|
|[504]|ScaleDP|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|0.00|


104 

**Table D6:** Criterion fulfilment for I1 – Adaptability & Flexibility. 

|**Criterion**|�_↓_|**%**<br>**fulfilled**|**Table D7:** Criterion fulfilment for<br>Compliance.|I2 – Safety &|
|---|---|---|---|---|
|Multi-Task Generalisation|160|49.38%|**Criterion**|�_↓_<br>**%**|
|Generalisation to Environmental|101|3117%||**fulfilled**|
|Variation||.|Redundant, Independent Safety<br>|5<br>1.54%|
|Autonomous Handling of|87|2685%|Mechanisms||
|Distractors/Obstacles||.|Command Compliance with|4<br>123%|
|Online/Mid-Execution|49|1512%|Online-Safety|.|
|Adaptation||.|Proactive, Plan-Level Safety|3<br>0.93%|
|Autonomous Incorporation of<br>Skills|22|6.79%|Learning from Safety Events<br>|2<br>0.62%|
||||Decoupled, Real-Time Safety||
|Online Environment Adaptation<br>|21|6.48%|Control|1<br>0.31%|
|and Response|||Reactive, Real-Time Safety|1<br>0.31%|
|Self-Evaluation & Command<br>Adherence|19|5.86%|Rule-Adherence & Autonomous<br>Rejection|1<br>0.31%|
|Multi-Hardware Support|16|4.94%|Authorised Operator Detection||
|Mid-Execution Feedback<br>|14|4.32%|& Override|0<br>0.00%|
|Responsiveness|||External Safety Integration|0<br>0.00%|
|Explained Adaptation Decisions|10|3.09%|Fault Detection & Sensing|0<br>0.00%|
|Multimodal Command Interface<br>|7|2.16%|Integrable Safety Systems|0<br>0.00%|
|Memory of Previous<br>Faults/Distractors|4|1.23%|Persistence of Safety Capabilities<br>in Adaptation|0<br>0.00%|
|Restricted Autonomous Task<br>Switching|3|0.93%|Persistent Safety Logs|0<br>0.00%|
|Autonomous Fallbacks|2|0.62%|Safe, Autonomous Recovery|0<br>0.00%|
|Energy/System-Aware<br>Adaptation<br>|1|0.31%|Safety Confidence Output<br>Safety Documentation &<br>Traceability|0<br>0.00%<br>0<br>0.00%|
|Operational Adaptation<br>Confidence|1|0.31%|Standards-Compliant|0<br>0.00%|
|Strategy-Goal Alignment|1|0.31%|Transparent Safety Reasoning|0<br>0.00%|
|Hot-Swappable & Dimensionality<br>Adaptation|0|0.00%|||


105 

**Table D9:** Criterion fulfilment for I4 – Robustness & Reliability. 

**Table D8:** Criterion fulfilment for I3 – HRI & HRC. 

|**Criterion**|�_↓_|**%**<br>**fulfilled**|
|---|---|---|
|Intuitive Feedback Acceptance|13|4.01%|
|Collaborative Adaptation|8|2.47%|
|Transparent Reasoning<br>Explanation|5|1.54%|
|Real-time Interruptibility|4|1.23%|
|Continuous Responsiveness|2|0.62%|
|Active Operator Exclusivity|0|0.00%|
|Exception Handling & Safe State<br>Transition|0|0.00%|
|Human Presence Awareness in<br>Workspace|0|0.00%|
|Human-Centric Adaptation|0|0.00%|
|Industrial HRI/HRC Standards<br>Compliance|0|0.00%|
|Instruction Confidence|0|0.00%|
|Learned Operator Preferences|0|0.00%|
|Multimodal Instruction &<br>Output|0|0.00%|
|Operator Data Privacy|0|0.00%|
|Operator Identification &<br>Authorisation|0|0.00%|


|**Criterion**|�_↓_|**%**<br>**fulfilled**|
|---|---|---|
|Disturbance Resilience &<br>Continuous Operation|44|13.58%|
|Environmental Robustness &<br>Adaptation|14|4.32%|
|Graceful Degradation & Strategy<br>Adaptation|6|1.85%|
|Reproducible & Benchmarked<br>Fault Diagnosis|5|1.54%|
|Adaptive Error Learning &<br>Memorisation|3|0.93%|
|Logging, Explanation & Operator<br>Guidance|1|0.31%|
|Automated Recovery & Safe-State<br>Transition|0|0.00%|
|Autonomous Fault Categorisation<br>& Severity Response|0|0.00%|
|Consistent & Documented Fault<br>Handling|0|0.00%|
|Multi-Level Fault & Anomaly<br>Detection|0|0.00%|
|Online Confidence & Reliability<br>Assessment|0|0.00%|
|Robust Redundancy & Modality<br>Management|0|0.00%|
|Supervisor Oversight & Fault<br>Review|0|0.00%|
|Threat & Attack Detection|0|0.00%|


106 

**Table D11:** Criterion fulfilment for I6 – Real-time Performance. 

**Table D10:** Criterion fulfilment for I5 – Precision & Accuracy. 

|**Criterion**|�_↓_|**%**<br>**fulfilled**|
|---|---|---|
|Consistency Over Time & Contexts|38|11.73%|
|Skill Integration with Known<br>v/P&A|9|2.78%|
|v/P&A Learning from Experience<br>& Feedback|6|1.85%|
|HRI/HRC Integration|3|0.93%|
|User-Defined Trade-offs|2|0.62%|
|Disturbance & Uncertainty<br>Management|1|0.31%|
|v/P&A Instructability|1|0.31%|
|Achievable v/P&A-Proposals|0|0.00%|
|Autonomous v/P&A Adaptation|0|0.00%|
|Outcome Logging & Failure<br>Reasoning|0|0.00%|
|Supervision & Verification Module|0|0.00%|
|Transparent Documentation of<br>v/P&A Capabilities|0|0.00%|
|v/P&A-Confidence Score &<br>Explanation|0|0.00%|


|**Criterion**|�_↓_|**%**<br>**fulfilled**|
|---|---|---|
|Goal-Responsive Solution<br>Strategies|12|3.70%|
|Historical Data Utilisation|2|0.62%|
|System-wide Real-time Compliance|1|0.31%|
|Task, Input & Environment<br>Independence|1|0.31%|
|Autonomous Adaptation & Safety<br>Response|0|0.00%|
|Dynamic Resource Management &<br>Determinism|0|0.00%|
|Live Metrics, Logging &<br>Explainability|0|0.00%|
|Real-Time Confidence/Alerting|0|0.00%|
|Transparent Documentation &<br>Compliance|0|0.00%|


**Table D12:** Criterion fulfilment for I7 – Cost-effectiveness & Integration Capabilities. 

|**Criterion**|�_↓_|**%**<br>**fulfilled**|
|---|---|---|
|Dynamic Resource Allocation|16|4.94%|
|Low-Cost Hardware Readiness|8|2.47%|
|Comprehensive Integration<br>Documentation|1|0.31%|
|Autonomous Fault Handling &<br>Feedback|0|0.00%|
|Cost-Reduction Memory &<br>Adaptive Optimisation|0|0.00%|
|Flexible Input/Output Adaptation|0|0.00%|
|Guided & Autonomous<br>Commissioning|0|0.00%|
|Hot-Swapping & Auto-Detection|0|0.00%|
|Integration Performance<br>Monitoring & Learning|0|0.00%|
|Universal Integration without<br>Retraining|0|0.00%|


107 

**Table D13:** Criterion fulfilment for I8 – Explainability & Trust. 

**Table D14:** Criterion fulfilment for I9 – Sensor Fusion & Perception. 

|**Criterion**|�_↓_|**%**<br>**fulfilled**|**Criterion**|�_↓_|**%**<br>**fulfilled**|
|---|---|---|---|---|---|
|Performance Benchmarking &<br>OOD Feedback|63|19.44%|Perceptual Feature Exposure &<br>Modularity<br>|32|9.88%|
|Explains Influences & Disturbances|4|1.23%|Comprehensive Scene<br>Understanding via Fusion|29|8.95%|
|Reason Logging & Accessible<br>Justification|3|0.93%|Multimodal Sensor Acceptance &<br>Fusion|11|3.40%|
|Task Feasibility & Capability<br>Explanation|3|0.93%|Flexible Input Combination &<br>Goal Specification|10|3.09%|
|Error, Anomaly & Safeguard<br>Explanations|2|0.62%|Dynamic Sensor Prioritisation|2|0.62%|
|User Feedback & Adaptive<br>Improvement|2|0.62%|Peer-to-Peer Perception<br>Knowledge Exchange<br>|1|0.31%|
|Behaviour Consistency &<br>Pre-Adaptation Notification|0|0.00%|Autonomous Disturbance<br>Recognition & Countermeasures<br>|0|0.00%|
|Confidence Score Explanation|0|0.00%|Continuous Input Monitoring &<br>Feedback|0|0.00%|
|Continuous Self-Assessment with<br>Explainability|0|0.00%|Modular Integration &<br>Documentation|0|0.00%|
|Explainability Across System<br>Components|0|0.00%|Online Learning for Perception<br>Skills|0|0.00%|
|Flexible, Intuitive Explainability<br>Interfaces|0|0.00%|Perception Evaluation &<br>Benchmarking|0|0.00%|
|Monitors & Logs Explainability for<br>Learning|0|0.00%|Perceptual Confidence &<br>Explanation Output|0|0.00%|
|Rule & Norm Compliance with<br>Explainability|0|0.00%|Robust Fault Tolerance &<br>DegradationHandling|0|0.00%|
|Security & Authorisation Feedback|0|0.00%|<br>Security in Sensor Operations|0|0.00%|


108 

**Table D15:** Criterion fulfilment for I10 – Standardised Benchmarking & Evaluation. 

|**Criterion**|�_↓_|**%**<br>**fulfilled**|
|---|---|---|
|Repeatability & Reproducibility|145|44.75%|
|Module & Skill-Specific<br>Benchmarking|129|39.81%|
|Generalisation & Adaptation<br>Assessment|90|27.78%|
|Benchmark Diversity & Scope|47|14.51%|
|Instruction, Command, &<br>Modality Coverage|3|0.93%|
|Explainability, Reasoning, &<br>Feedback Benchmarks|1|0.31%|
|Integration & Commissioning<br>Evaluation|1|0.31%|
|Data Requirement & Autonomous<br>Runtime Assessment|0|0.00%|
|Hardware Platform Benchmarking|0|0.00%|
|Human Interaction & Object<br>Recognition Evaluation|0|0.00%|
|Robustness & Fault Tolerance<br>Evaluation|0|0.00%|
|Safety, Security, & Norm<br>Compliance Validation|0|0.00%|
|Transparent Metrics & Reporting|0|0.00%|


**Table D16:** Criterion fulfilment for I11 – Data Requirements & Usage. 

|**Criterion**|�_↓_|**%**<br>**fulfilled**|
|---|---|---|
|Flexible Data Type Acceptance|158|48.77%|
|Low-Data Adaptation & Few-Shot<br>Requirements|136|41.98%|
|Documented Data Composition &<br>Simulation-Real Transfer|33|10.19%|
|Efficient Task, Environment, &<br>Modality Adaptation|14|4.32%|
|Resilience Through Redundancy &<br>Fault Tolerance|2|0.62%|
|Self-Assessment to Reduce Input<br>& Modalities|1|0.31%|
|Automatic Data Sufficiency<br>Assessment & Feedback|0|0.00%|
|Compliance with Privacy, Ethics,<br>& Law|0|0.00%|
|Comprehensive, Diverse<br>Pretraining Dataset|0|0.00%|
|Explainability on Data Usage &<br>Improvement|0|0.00%|
|Ongoing Adaptation/Finetuning<br>Confidence Scores|0|0.00%|


109 

