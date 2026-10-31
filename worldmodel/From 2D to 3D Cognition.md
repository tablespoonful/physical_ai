---
title: "From 2D to 3D Cognition: A Brief Survey of General World Models"
date: "2025-06-25"
authors: "Ningwei Xie; Zizi Tian; Lei Yang; Xiao-Ping Zhang; Meng Guo; Jie Li"
url: https://arxiv.org/abs/2506.20134
pdf: https://arxiv.org/pdf/2506.20134
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2506.20134)** / [論文ページ](https://arxiv.org/abs/2506.20134)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**From 2D to 3D Cognition: A Brief Survey of General World Models** 

NINGWEI XIE, China Mobile Research Institute, China ZIZI TIAN, China Mobile Research Institute, China LEI YANG<sup>∗</sup> , China Mobile Research Institute, China 

XIAO-PING ZHANG<sup>∗</sup> , Shenzhen Ubiquitous Data Enabling Key Lab, Shenzhen International Graduate School, Tsinghua University, China 

MENG GUO, China Mobile Research Institute, China 

JIE LI, China Mobile Research Institute, China 

World models have garnered increasing attention in the development of artificial general intelligence (AGI), serving as computational frameworks for learning representations of the external world and forecasting future states. While early efforts focused on 2D visual perception and simulation, recent 3D-aware generative world models have demonstrated the ability to synthesize geometrically consistent, interactive 3D environments, marking a shift toward 3D spatial cognition. Despite rapid progress, the field lacks systematic analysis to categorize emerging techniques and clarify their roles in advancing 3D cognitive world models. This survey addresses this need by introducing a conceptual framework, providing a structured and forward-looking review of world models transitioning from 2D perception to 3D cognition. Within this framework, we highlight two key technological drivers, particularly advances in 3D representations and the incorporation of world knowledge, as fundamental pillars. Building on these, we dissect three core cognitive capabilities that underpin 3D world modeling: 3D physical scene generation, 3D spatial reasoning, and 3D spatial interaction. We further examine the deployment of these capabilities in real-world applications, including embodied AI, autonomous driving, digital twin, and gaming/VR. Finally, we identify challenges across data, modeling, and deployment, and outline future directions for advancing more robust and generalizable 3D world models. 

CCS Concepts: • **General and reference** → **Surveys and overviews** ; • **Computing methodologies** → **Artificial intelligence** ; _Computer vision_ . 

Additional Key Words and Phrases: World Models, 3D Cognition, Physics-Aware 3D Modeling, Neural Radiance Fields, 3D Gaussian Splatting, Multimodal Fusion 

# **1 Introduction** 

World Models, computational frameworks that construct representations of the external world and predict its future states, have emerged as a central research area in the pursuit of AGI. Leading AI research organizations such as Meta and OpenAI have made significant strides in this domain, as exemplified by Meta’s self-supervised JEPA architecture[79] and OpenAI’s Sora video generation model[114]. JEPA enables abstract representation learning by modeling spatiotemporal regularities in latent space, while Sora exhibits strong video generation capabilities through implicit physical dynamics modeling. More recently, 3D-aware generative world models, including World Lab’s Large World Models (LWMs), Google DeepMind’s Genie 2[117], and Odyssey’s Explorer[113], have extended progress into the 3D domain. By leveraging advances in neural scene representations, these models enable the generation of geometrically consistent environments with persistent objects and coherent dynamics. This collective progress signifies a paradigm shift: world models are evolving from 2D simulations toward 3D cognitive systems that can perceive, reason, and interact with 

∗Corresponding authors 

Authors’ Contact Information: Ningwei Xie, China Mobile Research Institute, Beijing, China; Zizi Tian, China Mobile Research Institute, Beijing, China; Lei Yang, China Mobile Research Institute, Beijing, China; Xiao-Ping Zhang, Shenzhen Ubiquitous Data Enabling Key Lab, Shenzhen International Graduate School, Tsinghua University, Shenzhen, China; Meng Guo, China Mobile Research Institute, Beijing, China; Jie Li, China Mobile Research Institute, Beijing, China. 

Xie et al. 

2 

complex 3D environments. Despite these advances, a comprehensive and systematic understanding of this transition from 2D perceptual to 3D cognitive world modeling remains underexplored. As research approaches an inflection point, there is an urgent need to categorize and analyze the core technical pathways, capabilities, and challenges that shape the ongoing development of 3D cognitive world models. This survey aims to fill this gap by providing a structured perspective, identifying 3D representations and world knowledge as fundamental pillars, outlining the core cognitive capabilities, and reviewing representative technical methodologies and application trajectories across key domains. 

# **1.1 Technological Evolution** 

The concept of world models can be traced back to the theory of Mental Models in the field of cognitive science[69]. Psychologist Kenneth Craik proposed that humans construct cognition and perform reasoning by abstracting the external world into simple elements and their interrelationships. J. W. Forrester, a pioneer in the field of system dynamics, applied similar principles to model complex systems, further demonstrating the utility of abstract representations in understanding and predicting system behavior[37]. This theory also laid the philosophical foundation for early research on reinforcement learning and robotic control by formalizing methods for agents to learn internal models of environmental dynamics. In 2018, D. Ha and J. Schmidhuber [46, 47] introduced an influential approach to world models in reinforcement learning research. Their hierarchical architecture synergistically integrates Variational Autoencoders (VAE) for spatial compression of high-dimensional perceptual inputs and Recurrent Neural Networks (RNN) for temporal dynamics modeling. Similar approaches [17, 48, 49, 134] enabled AI agents to internally simulate environment dynamics through spatiotemporal latent representations and predict hypothetical outcomes for unseen action sequences, outperforming traditional model-based reinforcement learning algorithms in complex decision-making scenarios such as racing navigation. 

In 2022, Yann LeCun proposed the Joint Embedding Predictive Architecture (JEPA), a framework inspired by biological learning mechanisms that enables machines to observe and understand the world in a manner akin to humans and animals[79]. This architecture represents a significant advancement in the paradigm of world models through its non-generative approach to predictive learning and hierarchical decomposition of complex tasks across multiple abstraction levels and temporal scales. First, JEPA processes multi-modal sensory inputs through a joint embedding space to generate abstract environment states. The joint embedding space achieves highly efficient encoding of world dynamics, facilitating the prediction of plausible future states and robust representation learning from limited observational data. Then, JEPA models multi-scale temporal dependencies by three operational layers: high-level predictors perform long-term goal planning, mid-level components coordinate action sequences, and low-level modules execute precise motion control. This helps to resolve long-range dependency limitations in conventional models while enhancing interpretability. V-JEPA[7] extends the JEPA architecture to video data, enabling hierarchical modeling of multi-scale temporal dependencies in visual representations. Another notable work in abstract reasoning within world models is Contrastive Predictive Coding[153], which learns compact latent representations through self-supervised contrastive learning, enabling temporal abstraction and state compression. 

Contrasting with the abstract and structured world modeling strategy, an alternative approach relies on generative AI paradigms, such as autoregressive and diffusion models, which learn world knowledge through explicit data reconstruction. These models generate multi-modal data, including text[29], images[6, 111, 120, 132, 181], and videos[11, 33, 41, 42, 44, 51, 75, 182]. Notable examples include the Large Language Models (LLMs)[2, 12, 130, 131] and Sora[114]. Autoregressive architectures based on Transformer’s global attention mechanisms effectively capture long-range 

From 2D to 3D Cognition: A Brief Survey of General World Models 

3 

spatiotemporal dependencies, enabling multi-step learning and prediction of world states. Diffusion models simulate data distributions by progressively introducing noise and subsequently learning the reverse denoising process to generate high-fidelity visual content. OpenAI characterizes Sora as a world simulator, proposing its potential to advance video generation frameworks as foundational tools for constructing comprehensive world simulations. Some analyses[23] indicate that Sora exhibits properties of a world model, demonstrating emergent capabilities in modeling basic physical phenomena. 

# **1.2 From 2D Visual Representation Toward 3D Cognition** 

Abstract reasoning and data-driven generation represent two primary technological approaches in world modeling, each excelling in 2D visual representation and prediction. JEPA/V-JEPA demonstrates foresight in task decomposition and logical reasoning, while models like Sora exhibit outstanding performance in 2D video fitting and generation diversity. However, both methodologies encounter limitations when addressing motion simulation, physical interaction, and causal reasoning within 3D environments. In JEPA/V-JEPA, hierarchical encoders discard low-level geometric details to enhance reasoning efficiency, which leads to degraded performance in dynamic occlusion scenarios [152]. Sora, on the other hand, learns pixel-level correlations that lack explicit 3D structure, limiting its ability to simulate complex physical dynamics or reason about spatial causality. These observations underscore the need to develop world models that can comprehend and interact with the 3D physical world, thereby moving beyond the inherent constraints of 2D-focused approaches. 

In parallel, the rising demand for precise 3D scene construction, understanding and interaction, especially in embodied AI, autonomous driving, and digital twins, has accelerated progress in 3D generative modeling. In 2024, World Labs and Google introduced models capable of generating interactive 3D scenes from a single image[113, 117, 179, 180]. While these models achieve geometric plausibility, they still face challenges in delivering physically grounded semantics and responsive interactivity. Therefore, this gap has motivated both academia and industry to pursue world models built upon explicit spatial representation and cognitive priors as a crucial next step. 

As illustrated in Fig. 1, we present a conceptual framework that characterizes the development of world models around two foundational components essential for enabling spatial cognitive capabilities. The first is the adoption of **3D representations** , capturing geometry, radiance, and spatial structure in a volumetric form. The second is the incorporation of **world knowledge** , including physical laws, spatial commonsense, and semantic or structural priors, which provides contextual grounding for world modeling. Based on these two components, the framework identifies three interdependent capabilities that form the cognitive core of world models: 

- **3D physical scene generation** , empowers models to reconstruct and synthesize volumetric environments that adhere to physical plausibility, ensuring geometric fidelity and dynamic realism. 

- **3D spatial reasoning** , enables inference over spatial relations, object semantics or functions, and environmental dynamics, integrating geometric computation with semantic priors and commonsense knowledge to guide planning and decision making. 

- **3D spatial interaction** , equips models with the capacity for goal-directed, physically consistent interaction, through embodied agent behaviors and user-driven editing, transforming them from passive observers to active participants in 3D environments. 

Xie et al. 

4 


Fig. 1. **A conceptual framework of this survey.** Recent works advance world models toward 3D cognition by leveraging explicit 3D representations and integrating world knowledge. This facilitates the development of three fundamental cognitive capabilities within world models: 3D physical scene generation, 3D spatial reasoning, and 3D spatial interaction. As a result, these advancements significantly expand the applicability of world models across diverse domains, including embodied AI, autonomous driving, digital twins, and gaming/VR. 

This capability triad mirrors the canonical perceive–think–act loop commonly used to describe intelligent systems[136], and also serves as an organizing principle for surveying and evaluating recent progress across four key application domains, including embodied AI, digital twins, autonomous driving, and gaming/VR. 

# **1.3 Comparison with Prior Surveys** 

To highlight the unique perspective of our survey, Table 1 compares our survey with prior works in terms of foundational focus, capability coverage, and thematic emphasis. While these works have advanced understanding in specific subdomains, such as multimodal learning[102], physical video synthesis[88], and dimensional scaling in generative models[58], they typically focus on either rendering realism or abstract structural modeling. Ding et al. (2024)[30] categorize world models by state representation versus future prediction, while place less focus on explicit volumetric representations or active interactivity. In contrast, our survey provides a unified and comprehensive perspective on world models evolving towards 3D cognition. We systematically analyze recent advances through the lens of two foundational pillars, 3D representations and world knowledge, and describe how these foundations support three core spatial capabilities: 3D physical scene generation, 3D spatial reasoning, and 3D spatial interaction. 

# **1.4 Structure of This Paper** 

To systematically explore the components and capabilities outlined above, the remainder of this paper is organized as follows. Section 2 presents the two fundamental pillars of 3D world modeling: 3D representations and world knowledge. Section 3, Section 4, and Section 5 respectively further discuss the three core cognitive capabilities: 3D physical generation, 3D spatial reasoning, and 3D spatial interaction. Section 6 illustrates how these capabilities are applied across key domains, 

From 2D to 3D Cognition: A Brief Survey of General World Models 

5 

Table 1. Comparison of our survey with previous surveys in terms of main topic, and emphasis. 

|**Survey**|**Year**|**D**|**M**<br>**Wld**|**ain Top**|**ic**||**Emphasis and Scope**|
|---|---|---|---|---|---|---|---|
|||**3**<br>**Rep.**|**or**<br>**Know.**|**Gen.**|**Reas.**|**Inter.**||
|Mai et al.[102]|2024|�|�|**�**|**�**|�|Emphasizes cross-modal integration and language grounding;<br>provides limited discussion on 3D generation and physical pri-<br>ors.|
|Lin et al.[88]|2025|**�**|�|�|**�**|�|Focuses on video generation under physical constraints; less<br>emphasis on 3D spatial reasoning or interaction.|
|Hu et al.[58]|2025|�|**�**|�|�|�|Highlights progression of data dimensionality (2D, video, 3D,<br>4D) in multimodal generative models; does not explicitly explore<br>active spatial interaction.|
|Ding et al.[30]|2024|**�**|�|�|�|�|Reviews general world modeling paradigms (state representa-<br>tion vs. future prediction); uplaces less focus on explicit 3D<br>representation and active interaction.|
|**Ours**|**2025**|�|�|�|�|�|Provides a structured review of general world models evolving<br>towards 3D cognition, unifying 3D representations, world priors,<br>and spatial cognitive capabilities across generation, reasoning,<br>and interaction.|


* “�”, “ **�** ” and “�” indicate comprehensive, partial, and no coverage, respectively. 

* Columns correspond to: **3D Rep.** = 3D representation, **World Know.** = world knowledge, **Gen.** = 3D physical scene generation, **Reas.** = 3D spatial reasoning, **Inter.** = 3D spatial interaction. 


Fig. 2. **3D representations** that are covered in this survey, including point cloud, mesh, 3D occupancy grid, SDF, NeRF, 3DGS. 

including embodied AI, autonomous driving, digital twins, and gaming/VR. Section 7 concludes with an overview of open challenges and promising directions for advancing toward general 3D world cognition. 

# **2 Fundamental Pillars** 

World models with 3D cognition are fundamentally grounded in 3D representations and enriched by world knowledge. This section overviews recent advances in 3D representations and introduces two key types of world knowledge: physical knowledge from physics simulation and learned knowledge via large pretrained models, forming the basis for the 3D cognitive capabilities discussed later. 

Xie et al. 

6 

# **2.1 3D Representations** 

We introduce 3D representations including point cloud, mesh, 3D occupancy grid, Signed Distance Function (SDF)[115], Neural Radiance Fields (NeRF)[107] and 3D Gaussian Splatting (3DGS)[71]. We provide a schematic illustration in Fig. 2. 

_2.1.1 Point cloud._ Point cloud is a widely adopted representation of 3D data, consisting of discrete sets of spatial points. Point clouds directly reflect the raw output from range sensors such as LiDARs and depth cameras, and offer an lightweight and flexible format for representing large-scale 3D scenes. PointNet[123, 124] pioneered learning directly on point sets, while more recent models like Point Transformer[188] introduce attention-based mechanisms to enhance point cloud feature extraction. These models have become backbones for a wide range of 3D understanding tasks. 

_2.1.2 Mesh._ Mesh comprises vertices, edges, and faces that define a 3D shape’s geometry and topology. Owing to its surface-aware structure and high geometric fidelity, mesh is widely adopted as output representations in 3D reconstruction tasks[76, 165]. Moreover, it is well-suited for parameterized, template-based modeling of dynamic objects. For example, a 3D morphable model of the human body, SMPL[118], deforms a canonical mesh based on learned shape and pose parameters to capture articulated motion. 

_2.1.3 3D occupancy grid._ 3D occupancy grid divides space into a regular voxel grid, where each voxel stores a binary or probabilistic value indicating whether its spatial location is occupied. Formally, an occupancy field is defined as O : R<sup>3</sup> →[0 _,_ 1]. O( _𝑣𝑖_ ) denoting the occupancy probability of a voxel centered at _𝑣𝑖_ . Here, O( _𝑣𝑖_ ) = 1 indicates full occupancy, while O( _𝑣𝑖_ ) = 0 represents free space. This structured representation supports spatial reasoning and incremental scene construction from sensor data. Beyond binary encoding, semantic labels can be integrated into voxels to jointly capture spatial structure and scene semantics [147]. Notably, Occupancy Networks [105] generalize this representation by learning a continuous occupancy field with neural networks, enabling multi-resolution mesh extraction. 

_2.1.4 Signed Distance Function (SDF)._ SDF is an implicit 3D representation that defines a continuous scalar field over space, assigning each point a signed distance to the nearest surface. Formally, S : R<sup>3</sup> → R, where S( _𝑥_ ) _>_ 0 denotes points outside the surface, S( _𝑥_ ) _<_ 0 inside, and S( _𝑥_ ) = 0 on the surface. A representative method, DeepSDF [115], learns such implicit surfaces using deep neural networks, predicting signed distances from input coordinates and latent shape codes to enable high-fidelity reconstruction and shape interpolation. 

_2.1.5 Neural Radiance Fields (NeRF)._ NeRF models 3D scenes as continuous volumetric fields by learning a function F that maps a 3D position x ∈ R<sup>3</sup> and viewing direction d ∈ R<sup>2</sup> to an RGB color c ∈ R<sup>3</sup> and volume density _𝜎_ , as defined in Eq.1. 


This mapping is typically parameterized by a multilayer perceptron (MLP) with parameters _𝜃_ . Novel views are synthesized through volumetric rendering by integrating color along camera rays. NeRF enables photorealistic view synthesis from sparse inputs, and has been widely adopted for high-fidelity static scene reconstruction. 

_2.1.6 3D Gaussian Splatting (3DGS)._ 3DGS explicitly encodes a radiance field using a set of Gaussian kernels P, where each kernel is defined by its center position x _𝑝_ and covariance matrices A _𝑝_ , and is associated with an opacity _𝑜𝑝_ and a view-dependent color function c _𝑝_ , _𝑝_ ∈P[71]. Given a rendering viewpoint, the Gaussian ellipsoids are projected onto the imaging plane, forming 2D Gaussian 

From 2D to 3D Cognition: A Brief Survey of General World Models 

7 


Fig. 3. **Illustration of world knowledge sources** . Top: Real-world physical laws are encoded via differentiable simulation techniques. Modern engines and platforms provide various simulation functionalities, supporting physical world modeling. Bottom: Learned knowledge from large pretrained models captures spatial commonsense and semantic priors, including relational, functional, and categorical cues. 

splats. Formally, the _𝑘_ -th pixel color is computed as Eq. 2. 


_𝐺𝑖_ ( _𝑘_ ) represents the 2D Gaussian weight of the _𝑖_ -th kernel at pixel _𝑘_ , r _𝑘_ denotes of the viewing direction of the camera. 3DGS supports direct optimization of point attributes and enables real-time rendering. 

Recent extensions of NeRF and 3DGS enable dynamic scene modeling[32, 34, 39, 116, 122, 172], or integrate with diffusion models for photorealistic 3D content creation[85, 86, 93, 106, 121, 144, 160], highlighting their representational flexibility. 

# **2.2 Physical Knowledge from Physics Simulation** 

Physics simulation is fundamental to physical world modeling, as it encodes physical laws into computable signals that can be incorporated into world model optimization[27, 127, 174]. We introduce classic simulation methods and supporting platforms that serve as the computational backbone for integrating physical priors into world models, as illustrated by the upper part of Fig. 3. 

_2.2.1 Physics simulation methods._ Three major methods have been widely explored in this context: 

Xie et al. 

8 

- **Material Point Method (MPM)** [143] discretizes materials into a set of Lagrangian particles that carry physical quantities such as mass, velocity, and stress. These particles transfer information to a background Eulerian grid, where Newton’s laws of motion are solved to compute forces and update momentum. The updated values are then mapped back to the particles, enabling stable simulation of large deformations and collisions. 

- **Position-Based Dynamics (PBD)** [101, 109] iteratively updates particle positions under physical constraint conditions, rather than computing forces explicitly. This constraint-based formulation enables stable and efficient simulation of soft-body dynamics and fluid-like behaviors. 

- **Finite Element Method (FEM)** [198] models physical systems by discretizing a continuous domain into a mesh of finite elements, within which partial differential equations are solved to simulate physical responses. It is particularly effective in modeling elastic and plastic deformations under complex boundary conditions. 

_2.2.2 Physics engines and platforms._ Modern differentiable physics engines are built on GPUaccelerated, gradient-enabled computational frameworks, such as Taichi[57] and Nvidia Warp[100], and support simulation of complex material behaviors[8, 26, 52, 55, 56, 64, 89, 148, 157, 164]. Notably, FluidLab[169] builds a unified simulation environment supporting solids, liquids, gases, and their interactions, enabling multi-material differentiation with high efficiency. Genesis[168] further extends differentiable physics into a generative platform that translates natural language prompts into physically plausible simulation sequences, demonstrating potential for general-purpose, usercontrollable physics simulation. 

Large-scale 3D simulation platforms provide physics-rich, multi-modal, and interactive environments that serve as canonical sources or testbeds for training and evaluating world models. By providing high-fidelity ground-truth state transitions and observations, these platforms underpin reliable sim-to-real transfer. AI2-THOR [74] simulates realistic indoor scenes with rich object manipulation, scene rearrangement, and step-wise metadata. Habitat [137] enables efficient rendering of building-scale environments at thousands of frames per second with realistic lighting and occlusion. ThreeDWorld[38] simulates multi-modal sensory streams, including RGB, depth, and audio, alongside high-fidelity physics for soft bodies, liquids, and deformable objects. MetaUrban[166] extends embodied simulation to outdoor, city-scale environments via a hierarchical procedural pipeline generating infinite street-block layouts, functional zones, and dynamic entities. 

Together, these simulation techniques and platforms provide foundational physical knowledge for world models, improving the realism of geometry and material representations in static scenes, and ensuring physically consistent motion and deformation in dynamic environments. 

# **2.3 Learned Knowledge via Large Pretrained Models** 

Recent advances in large pretrained models, especially LLMs and Vision-Language Models (VLMs), have enabled the extraction of high-level world knowledge from massive textual and visual corpora. We focus on two primary categories of learned knowledge that world models benefit from: spatial commonsense and semantic priors. 

_2.3.1 Spatial commonsense._ Spatial commonsense refers to intuitive knowledge about typical spatial relationships, functional arrangements and causal interactions of objects in the physical world, providing contextual concepts such as "a cup is typically found on a table," "a bed is placed along a wall". Recent studies show that pretrained LLMs, such as LLaMA[150] and PaLM[24] implicitly encode such spatial and causal knowledge. These models perform competitively on spatial commonsense benchmarks like PIQA[10], which test models’ abilities to infer plausible physical interactions. Moreover, the non-multimodal version of GPT-4V[2] exhibit emergent capabilities in 

From 2D to 3D Cognition: A Brief Survey of General World Models 

9 

interpreting the 3D environments through codes[13]. In parallel, some methods propose to elicit knowledge from pretrained LLMs by introducing prompting engineering strategies. In parallel, to more effectively elicit knowledge encoded by LLMs, various prompting strategies have been proposed. For instance, AutoPrompt[141] automates the generation of task-specific trigger tokens that activate latent knowledge in LLMs. Chain-of-thought prompting[161] facilitates the transfer of LLMs to tasks requiring hierarchical spatial and causal reasoning by decomposing complex problems into structured intermediate steps. 

_2.3.2 Semantic priors._ Semantic priors refer to knowledge about object categories and their associated visual attributes. These priors can be typically learned by powerful VLMs pretrained on large-scale visual-textual datasets[18]. Notably, the text-image alignment methods, represented by CLIP[129], link textual concepts with visual evidence by aligning textual and visual embeddings in a shared latent space via contrastive learning, providing strong semantic discriminability for object categories and attributes. Recent models such as BLIP[82, 83], GPT-4V[2], LLaVA[92] enhance abilities in encoding compositional semantics to support relational reasoning and context-aware visual understanding. Open-vocabulary grounding and segmentation models[15, 73, 77, 94, 133] have demonstrated impressive generalization to novel object categories and spatial concepts without requiring retraining. These models provide category-agnostic proposals and fine-grained pixel-level masks, enabling world models to incorporate high-level semantics at the object, region, and scene levels, which supports more informed scene understanding and interaction planning. Furthermore, 2D diffusion models such as Stable Diffusion[135] possess strong language-vision alignment through generative pretraining on text-image pairs. These models offer semantic-rich visual priors and have been leveraged to supervising 3D representations for controllable and semantically aligned 3D scene generation. 

As elaborated in the following sections, world models achieves generalized, interpretable spatial understanding and inference by querying or conditioning 3D representations on contextual and semantic information derived from these foundation models. 

# **3 3D Physical Scene Generation** 

Generating physically plausible 3D environments forms the perceptual foundation of world models with genuine 3D cognition. Unlike traditional 3D scene synthesis techniques that prioritize visual fidelity, this capability emphasizes geometric consistency, material plausibility, and physical coherence, ensuring that generated scenes are not only photorealistic but also adhere to the structural and dynamical principles of the real world. To this end, recent research trends increasingly advocate for the integration of world priors into 3D scene generation frameworks. 

In this section, we classify 3D physical scene generation methods into two major categories: static scene generation and dynamic scene generation. 

# **3.1 Static Scene Generation** 

This category focuses on methods that integrate structural and physical priors to generate 3D static scenes. Table 2 summarizes the representative methods, along with their 3D representations, incorporated priors or constraints and targeted applicability. 

_3.1.1 Layout-guided generation._ Early approaches guide object placement (including position, rotation, and scale) and scene composition using manually designed layout priors, to ensure spatial consistency and controllability. Set-the-Scene[25] allows users to place layout anchors that serve as global guidance for training locally controlled NeRFs, enabling controllable and globally consistent scene generation. Similarly, Comp3D[119] introduces a locally conditioned diffusion framework, where user-defined bounding boxes and corresponding text prompts jointly guide the generation 

Xie et al. 

10 

Table 2. Overview of representative works for static physical scene generation. 

|**Category**|**Method**|**3D Rep.**|**Priors**|**Applicability**|
|---|---|---|---|---|
||LI3D [91]|NeRF|||
|Layout-<br>uided|SceneTeller [112]|3DGS|LLM-inferred layouts (object<br>categories, location, size, orientation,|Scenes conforming to spatial<br>commonsense and semantic|
|g|GALA3D [195]|3DGS|appearance, etc.)|consistency|
||SceneWiz3D [186]|NeRF|||
||LayoutDreamer [197]|3DGS|Physical constraints (gravity, center-<br>of-mass stability, inter-object penetra-<br>tion)||
|Physics-<br>informed|PhyScene [177]|Latent 3D features|Physical<br>constraints<br>(reachability,<br>collision-avoidance)|Physically plausible and stable<br>sceness|
||Phy3DGen [175]|Mesh & SDF|Physical priors (stress, strain, displace-<br>ment)||
||PhysComp3D [43]|Mesh|Material priors (mechanical responses<br>under external forces)||


* Abbreviations: 3D Rep. = 3D Representation. 

of 3D scene components. Then, these components are then assembled into a coherent voxel-based NeRF representation, achieving object-level control and high spatial fidelity. 

Moving beyond hand-crafted priors, recent advances enhance scene layout learning by implicitly leveraging commonsense spatial knowledge encoded in LLMs. LI3D[91] treats LLMs as interpreters of layout instructions and integrates generative feedback mechanisms to iteratively refine the 3D scene generated by CompoNeRF[4]. By exploiting LLM’s pre-trained understanding of spatial relationships, the framework infers plausible coarse layouts, ultimately producing semantically consistent and visually realistic 3D scenes. SceneTeller[112] further leverages LLMs with in-context learning to parse textual descriptions into a set of 3D bounding boxes, each specifying an object’s type, position, size, and orientation. The derived layout is subsequently fitted with a 3DGS representation. GALA3D[195] enhances LLM-generated initial layouts by introducing an adaptive geometric control mechanism. It aligns 3D Gaussians with text-to-image diffusion priors through compositional optimization, ensuring high geometric and textural consistency in multi-object scenes. SceneWiz3D[186] utilizes LLMs to extract objects of interest (OOI) from input texts, initializes their 3D representations via text-to-3D retrieval. It also employs particle swarm optimization (PSO)[70] based on CLIP[129] similarity to automatically configure object placement, thereby satisfying both semantic and spatial consistencies. 

_3.1.2 Physics-informed generation._ In addition to structural and commonsense priors, some approaches incorporate explicit physical knowledge to ensure the generated layouts are physically valid. LayoutDreamer[197] introduces a physics-guided hierarchical layout optimization framework. It formulates physical knowledge as energy terms, including gravity, center-of-mass stability, anchoring, and inter-object penetration, in a two-stage optimization pipeline over a 3D Gaussian scene representation. By minimizing these energy functions, LayoutDreamer ensures that the resulting layouts are both physically stable and semantically coherent. PhyScene[177] proposes a diffusion-based generation framework augmented with differentiable physical constraint functions. It integrates layout regularization, collision avoidance, and reachability optimization into the denoising process, enabling the creation of physically interactable static scenes. 

Moreover, several approaches focus on improving the physical realism of individual object for compositional scene generation. Phy3DGen[175] introduces a differentiable physical layer inspired 

From 2D to 3D Cognition: A Brief Survey of General World Models 

11 

Table 3. Overview of representative works for dynamic physical scene generation. 

|**Category**|**Method**|**3D Rep.**|**Physics Simu-**<br>**lator**|**Priors**|**Applicability**|
|---|---|---|---|---|---|
|Physics-<br>|GausSim [139]|3DGS|—|Mass & momentum conserva-<br>tion regularization|Elastic objects|
|regularized|DeformGS [32]|3DGS|—|Momentum & local isometry<br>regularization|Large-deformable objects|
||ParticleNeRF [1]|NeRF|PBD|Collision-avoidance constraint|Rigid,<br>articulated,<br>de-<br>formable objects|
||PIE-NeRF [36]|NeRF|Q-GMLS|Elastodynamics|Large-deformable objects|
|Physics<br>simulation-based|PhysGaussian [172]|3DGS|MPM|Continuum mechanics|Diverse materials|
||Phy124 [87]|3DGS|MPM|Continuum mechanics|Elastic objects|
||Gaussian Splashing [35]|3DGS|PBD|Surface tension, fluid reflec-<br>tion/refraction effects|Solid-fluid interactions|
||PAC-NeRF [84]|NeRF|MPM|Continuum mechanics|Diverse materials|
||DANO [78]|NeRF|Dojo [55]|Rigid-body contact model|Rigid objects|
|Physics<br>simulation-based<br>|Spring-Gaus [193]|3DGS|Custom spring-<br>mass simulator|Elastic dynamics|Elastic objects|
|+ learnable<br>physical<br>properties|NeuMa [14]|3DGS|MPM|Expert-designed constitutive<br>models|Diverse materials|
||OmniPhysGS [90]|3DGS|MPM|Expert-designed constitutive<br>models|Diverse materials|
||PhysSplat [189]|3DGS|MPM|Physical commonsense via pre-<br>trained LLMs and VLMs|Diverse materials|


* Abbreviations: 3D Rep. = 3D Representation. 

by the FEM, which models solid mechanics using three key physical quantities, i.e., stress, strain, and displacement. This is incorporated into a text-to-3D diffusion model to jointly optimize the visual fidelity and physical accuracy. Specifically, Phy3DGen can generate 3D shapes with more uniform stress distribution, which conform to the principles of solid mechanics. PhysComp3D[43] proposes physical compatibility optimization, which refines the rest-shape geometry of 3D objects by modeling mechanical material properties and external forces. These precise-physics-driven approaches effectively produce static scenes capable of exhibiting accurate mechanical responses under load, enabling seamless downstream dynamic simulation. 

# **3.2 Dynamic Scene Generation** 

This category focuses on methods that generate dynamic scenes under physical constraints, capturing object deformation, motion, and contact dynamics. An overview of representative methods and their physical modeling characteristics is provided in Table 3. 

_3.2.1 Physics-regularized generation._ Some methods introduce explicit physics regularization to optimize physically plausible dynamics. GausSim[139] treats each 3D Gaussian kernel as a continuous piece of matter organized into explicit Center of Mass Systems (CMS). Leveraging explicit continuum-mechanics constraints, it effectively captures realistic elastic deformations of real-world objects. DeformGS[32] employs physics regularization terms, such as conservation of momentum and local isometry, to guide the deformation of 3D Gaussians. Concurrently, it utilizes a learnable deformation function, implemented via a multilayer perceptron (MLP) with neural-voxel encoding, to map canonical Gaussian properties to their deformed states in world 

Xie et al. 

12 

space. This combination allows DeformGS to effectively model scene flow in highly deformable scenes, balancing physical plausibility with the flexibility of data-driven learning. 

_3.2.2 Physics simulation-based generation._ A growling line of methods integrate physics simulatiors with NeRF and 3D Gaussian representations to model dynamic phenomena. In the NeRF setting, ParticleNeRF[1] introduces a particle-based encoding scheme for online NeRF optimization, where each particle carries local appearance and geometric features. It incorporates a PBD module into the NeRF formulation to update the motion of the particles under collision-avoidance constraint. PIE-NeRF[36] explicitly integrates elastodynamic simulation with NeRF, enabling photorealistic rendering of soft object deformations under external force. It introduces a mesh-free simulation scheme based on Quadratic Generalized Moving Least Squares (Q-GMLS), supporting real-time computation of nonlinear elastic responses governed by the material models. By adapting the simulation kernels to the NeRF density distribution, the framework enables large-deformation modeling and efficient force propagation within the volumetric NeRF representation. 

Due to their particle-based nature, 3D Gaussians can be endowed with physical properties and seamlessly integrated with physics simulators. PhysGaussian[172] and Phy124[87] extends each Gaussian with physical attributes based on a custom MPM, allowing the Gaussian kernels and their associated spherical harmonics to evolve according to the laws of continuum mechanics. These Gaussians act simultaneously as simulation particles and as renderable primitives. This design ensures consistency between physical dynamics and rendered appearance. Gaussian Splashing[35] generate fluid-solid dynamics within 3DGS scenes through PBD simulation. It separates solid simulation and rendering by simulating sampled particles and interpolating their deformations onto trained Gaussian kernels for rendering. For fluid simulation and rendering, it uses a unified set of Gaussian kernels and optimizes them to produce plausible diffuse, specular shadings and surface roughness. 

Beyond direct simulation, some approaches aim to learn or adapt physical properties for specific materials. PAC-NeRF[84] employs a hybrid Eulerian–Lagrangian approach, where static geometry is encoded via a voxel-based Eulerian NeRF, while dynamics are modeled using MPM-driven Lagrangian particles. Notably, it learns unknown geometry and physical parameters from multiview videos, enabling accurate dynamic modeling across diverse materials, including elastic solids, plasticine, and fluids. DANO[78] estimates inertial and friction properties and integrates the differentiable physics simulator Dojo[55] with NeRFs to model rigid-body contact dynamics. SpringGaus[193] develops a learnable, differentiable spring-mass simulator tailored for 3D Gaussians, jointly learning elasticity parameters and dynamic motion directly from multi-view video. Each Gaussian serves as a mass node connected by virtual springs, enabling physically consistent elastic dynamics via position updates governed by Hooke’s law. NeuMa[14] learns to correct expertdesigned physical models by fitting a neural material adaptor to ground-truth visual observations. It predicts latent material embeddings that capture actual intrinsic dynamics, to guide the generating of physically plausible trajectory and deformation of objects. OmniPhysGS[90] employs several learnable constitutive models to predict material responses for each Gaussian under specific mechanical conditions, which are then used to drive physical simulation within a differentiable MPM module. This design allows OmniPhysGS to model a wide range of material behaviors, including elasticity, plasticity, and viscoelasticity, within a unified generative framework. 

Different from these constitutive learning approaches, another line of work leverages LLMs to infer physical properties from visual observations. For example, PhysSplat[189] designs a multimodal LLMs (BLIP, CLIP, GPT-4V) to predict material categories and physical properties of dynamic objects based on input video. A Material Property Distribution Prediction (MPDP) module models 

From 2D to 3D Cognition: A Brief Survey of General World Models 

13 


Fig. 4. **Illustration of the role of world knowledge in generating static and dynamic physical scenes.** Left: Static scene generation leverages structural priors from LLM commonsense and explicit physical constraints to produce plausible layouts. Right: Dynamic scene generation builds on physics-enhanced 3D representations, where particles with physical properties are optimized via simulation or regularization to ensure temporal consistency and physical realism. 

plausible distributions over physical parameters, which are then used in a differentiable MPM simulator to generate physically consistent and generalizable dynamic scene synthesis. 

In summary, as a core capability of 3D world modeling, 3D physical scene generation advances world models from visually realistic renderers to physically grounded, cognitive systems. Recent developments reveal a clear trajectory toward unifying 3D representations with physically grounded world knowledge, as highlighted by Fig. 4. By incorporating spatial priors, physical constraints, and material-aware dynamics into neural generation frameworks, these methods enable physically plausible synthesis of both static and dynamic environments. 

# **4 3D Spatial Reasoning** 

3D spatial reasoning is essential for enabling world models to interpret and analyze spatial structure, semantic context, and dynamic changes of 3D environments, thereby supporting downstream tasks such as planning and decision-making. This capability requires high-level understanding grounded in volumetric representations and contextualized by world knowledge. 

In this section, we categorize 3D spatial reasoning into two complementary dimensions: static spatial understanding and dynamic spatial analysis. The former focuses on spatial relationships and semantics within static scenes, while the latter emphasizes forecasting environmental evolution and object trajectories over time. Both research lines reflect a growing trend toward integrating 3D perception with spatial commonsense and semantic priors via LLMs and VLMs, enabling semantic inference and high-level spatial comprehension. 

# **4.1 Static Spatial Understanding** 

Recent works in static spatial understanding have explored integrating pretrained LLMs and VLMs with 3D representations including point clouds, NeRF, and 3DGS to enhance spatial inference within 3D environments. Table 4 summarizes recent representative methods and presents their use of large pretrained models and supported reasoning tasks. 

_4.1.1 Point-language alignment for point cloud understanding._ A large number of recent methods transform unstructured point cloud data into tokenized spatial features, which are then aligned with 

Xie et al. 

14 

Table 4. Overview of representative works for static scene reasoning. 

|**Method**|**3D Rep.**|**LLMs**|**VLMs**|||**Reasonin**|**g tasks**|||
|---|---|---|---|---|---|---|---|---|---|
|||||**Cap.**|**QA**|**Obj. Grd.**|**Obj. Det.**|**Seg.**|**Gen.**|
|PointLLM [176]|Point cloud|✓||✓||||||
|Chat-3D [159]|Point cloud|✓||✓|✓|||||
|3D-LLM [54]|Point cloud|✓||✓|✓|✓||||
|Chat-Scene [59]|Point cloud|✓||✓|✓|✓||||
|LL3DA [20]|Point cloud|✓||✓|✓|||||
|Reason3D [62]|Point cloud|✓||✓|✓|✓|✓|✓||
|SpatialLM [104]|Point cloud|✓||||✓|✓|||
|GPT4Point [125]|Point cloud|✓|✓|✓|✓||||✓|
|Grounded 3D-LLM [22]|Point cloud|✓||✓|✓|✓|✓|✓||
|LERF [72]|NeRF||✓|||✓||||
|LLaNA [3]|NeRF|✓||✓|✓|||||
|LangSplat [128]|3DGS||✓|||✓||||
|ChatSplat [19]|3DGS|✓||✓|✓|||||
|ReasonGrounder [97]|3DGS||✓|||✓||||
|Query3D [16]|3DGS|✓||||||✓||
|SplatTalk [146]|3DGS|✓|✓||✓|||||


* Abbreviations: 3D Rep.=3D Representation, Cap.=Captioning, QA=Question Answering, Obj. Grd.=Object Grounding, Obj. Det.=Object Detection, Seg.=Segmentation, Gen.=Generation. 


Fig. 5. **Illustration of the point–language alignment paradigm for 3D scene understanding.** Recent methods leverage pretrained LLMs to align point cloud features with text tokens, enabling a unified representation space that incorporates both geometric and semantic information. Point–language models like Reason3D [62], Grounded 3D-LLM [22] extend this approach from single-object captioning to complex scene-level reasoning tasks. 

pretrained LLMs to achieve holistic understanding, as illustrated by Fig. 5. Notably, PointLLM[176] encodes geometry and color information of input point clouds into latent feature vectors, projects them into the embedding space of a pretrained LLM, and fuses these spatial features with text tokens. By leveraging the commonsense priors embedded in the LLM, PointLLM is capable of producing plausible and informative textual descriptions grounded in 3D geometry. 

This paradigm has been extended beyond single-object captioning to full-scene understanding[99]. Chat-3D[159] introduces 3D object segmentation and explicit spatial relation modeling. It first 

From 2D to 3D Cognition: A Brief Survey of General World Models 

15 

extracts object-level embeddings and then applies a relation module to capture inter-object spatial relationships. During training, it aligns both object-centric and scene-level features with a pretrained LLM in a staged manner, facilitating a progressively transition from understanding single-object attributes to modeling complex multi-object spatial relations. 3D-LLM[54] and ChatScene[59] extract multi-view semantic features and visual cues from rendered images of the input 3D scene, which are combined with 3D point embeddings to construct semantically enriched spatial representations. LL3DA[20] aggregates multimodal prompts, including user clicks, 3D box annotations, and textual instructions, along with global scene embeddings to form unified query tokens. By aligning user intentions with rich 3D representations, LL3DA demonstrates the potential of visual-instruction tuning for human-in-the-loop 3D reasoning and decision-making. 

Builds upon the point–language alignment strategy, some methods broaden the scope of scene point cloud understanding from question answering (QA) and captioning to encompass tasks such as fine-grained spatial analysis. Reason3D[62] guides the LLM backbone to generate structured outputs with task-specific control tokens, enabling seamless integration with dedicated downstream modules for hierarchical object search and segmentation. SpatialLM[104] extracts dense spatial features from raw point cloud data, acquired from monocular videos, RGB-D sensors, or LiDAR, and interprets them using a pretrained LLM to produce fine-grained, structured 3D scene representations. These representations include semantic categories, oriented object bounding boxes, and architectural elements such as walls, doors, and windows, thereby supporting 3D structural layout generation and agent action planning. GPT4Point[125] and Grounded 3D-LLM[22] propose two-stage frameworks to support various 3D reasoning tasks. They first performs point–text feature alignment through pretraining tasks designed to bridge geometric and linguistic modalities. Subsequently, they employ an LLM for multi-task instruction fine-tuning based on the aligned point cloud features. 

_4.1.2 Language-Guided Reasoning over NeRF and 3DGS._ In addition to point-cloud-based approaches, researchers also investigate distilling knowledge from pretrained LLMs or VLMs into NeRF[3, 5, 72] and 3DGS[16, 19, 97, 146], so that these 3D formats can be queried and analyzed via textual prompts. 

To support object grounding in NeRF scenes, LeRF learns a 3D language field by associating each spatial location with a CLIP embedding. It performs multi-scale volume rendering of these CLIP features along camera rays, aligning them with multi-view, multi-scale image-level CLIP embeddings. Additionally, a DINO-based regularization is applied to improve object boundary sharpness and ensure view consistency. LangSplat[128] and LE3DGS[140]extend this approach by leveraging 3DGS for faster rendering and improved semantic precision. They further incorporate hierarchical semantics via SAM-generated masks to refine object boundary delineation. Query3D[16] augments LE3DGS by introducing LLM-generated language queries to enrich the language embedding space, thereby improving open-vocabulary querying performance. ReasonGronder[97] further advances this line of work by mapping both language-aligned and instance-level features into the 3DGS space. It supervises language-aligned features with multi-view CLIP embeddings and distills instance-aware features from SAM masks using a contrastive loss. his hierarchical supervision boosts grounding accuracy in occluded regions and enhances generalization to implicit, open-vocabulary queries. 

Similar to the point-language models, some approaches propose to tokenize NeRF or 3DGS representations, and aligns them with pretrained LLMs for question answering. LLaNa[3] directly ingests the parameters of a trained NeRF MLP. Specifically, it introduces a meta-encoder (nf2vec) that compresses the raw network weights into a compact latent vector, which is injected as prefix tokens into a frozen LLM. This alignment allows the model to interpret and reason about the encoded 3D scene using textual prompts. ChatSplat[19] encodes view-, object-, and scene-level 

Xie et al. 

16 

features rendered from 3DGS and converts them into input tokens of a LLM, to achieve multi-level chatting over the 3D scene. SplatTalk[146] introduces a framework for 3D visual question answering over 3DGS representation. It begins by constructing a 3DGS scene from a set of posed RGB images and enriches each Gaussian with semantic features extracted from VLMs. These enriched Gaussians are then converted into 3D tokens, which are fed into a pretrained LLM for open-ended spatial reasoning. 

# **4.2 Dynamic Spatial Analysis** 

Beyond static spatial understanding, 3D spatial reasoning also involves dynamic spatial analysis. This entails modeling the temporal evolution of the 3D scene and forecasting its future states. 

Classic dynamic spatial analysis methods convert multi-source sensor data, including cameras, LiDAR, and radar, into Bird’s-Eye View (BEV) representations to capture spatiotemporal information for detecting and predicting dynamic objects[31, 190]. BEV representations inherently compress vertical geometry and occlude 3D structural details, limiting their capacity to characterize vertical structures and depict fine-grained internal geometric shapes of objects[173]. Modern approaches represent dynamic scenes as a series of 3D occupancy grids, which preserve full volumetric geometry of the scene over time[147, 149, 163]. Given a historical multi-view image sequence or LiDAR sequence, the goal is to learn a 3D semantic occupancy field for each time step. 

Recent methods further enhance occupancy-based dynamic scene analysis by introducing semantic priors from VLMs, i.e., pretrained open-vocabulary segmentation models[73, 94, 133], and employing neural rendering for self-supervision, thereby reducing reliance on 3D annotations. OccNeRF[183] parameterizes the occupancy field and employs neural rendering to generate multi-view depth maps, supervised by multi-frame photometric consistency. It further leverages Grounding DINO[94] and SAM[73] to guide semantic label prediction. OccGS[196] extracts semantic information using these VLMs, and align it with LiDAR points to construct semantic- and geometric-aware Gaussian representations of dynamic scenes. It enables zero-shot, semantically rich modeling of dynamic environments. 

Unlike the above-mentioned methods that predict per-frame occupancy independently, Let Occ Flow[96] introduces occupancy flow fields to capture temporal voxel-level motion in the horizontal plane, enabling explicit modeling of object dynamics. The method leverages semantic and optical flow cues extracted from the pretrained Grounded SAM[133] model, enabling effective dynamic decomposition and providing supervision for learning motion patterns. 

In summary, 3D spatial reasoning equips world models with the capability to comprehend both the static and dynamic aspects of 3D world. Recent efforts enrich 3D geometric representations with world knowledge encoded in pretrained LLMs or VLMs, enabling reasoning grounded in both spatial structure and semantic context. 

# **5 3D Spatial Interaction** 

3D spatial interaction equips world models with the ability to solve interactions with agents or humans, and manipulate 3D environments in a physically grounded and goal-directed manner. 

In this section, we categorize active 3D interaction methods according to the actor’s perspective and role within the interaction process: egocentric embodied interaction and exocentric scene manipulation. The former refers to scenarios where an embodied agent interacts with the environments, navigating, manipulating objects, or executing tasks based on physical and semantic understanding. The latter involves user-driven interaction with the scene from an external or top-down perspective, where users edit, rearrange, or transform elements within the environment to achieve desired outcomes. 

17 

From 2D to 3D Cognition: A Brief Survey of General World Models 


Fig. 6. **Illustration of egocentric embodied interaction.** A key challenge lies in capturing the coconstraining relationship between human/agent’s behaviors and the environment’s responses, where actions like sitting, placing objects, or navigating space should dynamically respect contact relations and collision constraints. 

# **5.1 Egocentric Embodied Interaction** 

This category focuses on modeling egocentric interactions where a human or an agent engages within the 3D environment, by predicting physically and semantically plausible actions and corresponding environment responses, as illustrated in Fig. 6. 

_5.1.1 Human-scene interaction._ methods synthesize physically plausible human motions by aligning language instructions, human motion, and 3D scene context. HUMANISE[158] introduces a large-scale synthetic dataset of language-grounded human–scene interactions and proposes a generative model that produces SMPL[118]-based full body motions conditioned on textual prompts and scene geometry. The model learns the joint embedding of the 3D scene and the language description as the condition to generate human motion. It employs auxiliary losses to enforce accurate object localization and action-specific motion generation, enhancing both physical plausibility and semantic coherence. TRUMANS[67] extends this idea to real-world data by contributing a motion capture dataset paired with scanned indoor scenes. Its diffusion-based model synthesizes contact-aware motion from 3D layouts using local occupancy perception. At each step, a local scene perceiver queries global occupancy to maintain 3D-aware collision avoidance, while action progression embeddings condition the diffusion process, achieving real-time and generalizable egocentric behavior. 

Recent works have increasingly investigated bidirectional agent-environment interactions, acknowledging that agent behaviors and environmental configurations are interdependent and co-constraining, as illustrated by Fig 6. CHOIS[81] presents a conditional diffusion framework that synchronizes human–object interactions under sparse waypoints and natural language instruction, and designs guidance terms to enforce contact constraints between actors and objects. For example, it can follow the textual instructions, such as “move the desk lamp next to the sofa”, to generate corresponding synchronized human-object motions while accurately handling hand-object contact and object-floor collision avoidance. ZeroHSI[80] further enhances the representation of humanscene interaction using heterogeneous 3D Gaussians to handle object transformation and occlusion. It proposes a combination of the parameterized Gaussian human, transformed Gaussian object and static Gaussian scene, and joint optimizes egocentric camera pose, body motion, and object motion. It refines body motion using a pretrained pose prior derived from human motion-capture data, and employs hand-object contact and human pose smoothness losses to enforce physically consistency of interaction sequences. 

Xie et al. 

18 

Table 5. Overview of representative works for exocentric scene manipulation 

|**Category**|**Method**|**3D Rep.**|**Prompts**|**Priors**|**Applicability**|
|---|---|---|---|---|---|
||Instruct- NeRF2NeRF [50]|NeRF|Text|2D diffusion prior|Contextual edition, object<br>stylization|
|Static scene<br>|SIn-NeRF2NeRF [53]|NeRF|Text|2D diffusion prior, segmenta-<br>tion&inpainting|Object translation, rotation,<br>scaling|
|manipulation|CLIP-NeRF [154]|NeRF|Text/image|Text-visual prior via CLIP|Object stylization|
||GaussianEditor [155]|3DGS|Text|Diffusion prior, LLM-guided<br>segmentation|Region-level<br>removal,<br>styling|
||Point’n Move [61]|3DGS|2D click|Segmentation & inpainting|Object translation, rotation,<br>removal|
||Instruct 4D-to-4D [108]|NeRF|Text|2D diffusion prior|Scene stylization|
|Dynamic scene<br>|4D-Editor [66]|NeRF|User’s stroke|Semantic prior via DINO|Object translation, removal,<br>recoloring|
|manipulation|Neuphysics [126]|SDF|Physics<br>pa-<br>rameters|Differentiable physics engine|Object removal, duplication,<br>recoloring|
||SC-GS [63]|3DGS|Control<br>points|ARAP rigidity constraint|Object motion edition|


* Abbreviations: 3D Rep. = 3D Representation. 

_5.1.2 Agent-scene interaction._ focuses on predicting precise, high-degree-of-freedom (high-DOF) manipulation actions in 3D environments. Recent methods reconstruct voxel- or point cloud-based workspace representations, integrate pretrained language models to interpret instructions and embed spatial commonsense, then combine spatial and linguistic features to predict actions such as translation, rotation, and gripper state. Perceiver-Actor[142] reconstructs a voxel grid from RGB-D sensor inputs and encodes language instructions using a pretrained language model. It then extracts RGB-D voxel patches and fuses semantic and geometric information through cross-modal attention. Finally, it predicts a sequence of continuous actions using a voxel decoder, formulating action selection as a per-voxel classification task. PolarNet[21] proposes a point cloud-based approach that combines a point cloud encoder with a CLIP text encoder by integrating their intermediate features through a multi-layer transformer. A point cloud decoder is then employed to predict scene and agent transitions, including per-point position offsets, as well as the gripper’s rotation and open state. 3DAPNet[110] adopts a point cloud-based framework that encodes language instructions with a pretrained transformer and jointly models object affordance region and affordance-conditioned action poses, enabling fine-grained and instruction-aligned manipulation. 

# **5.2 Exocentric Scene Manipulation** 

Interactive scene manipulation refers to user-initiated interaction with 3D environments from an external viewpoint, where users edit elements of a scene to achieve specific goals. These approaches build on neural 3D representations, notably NeRFs or 3DGS, as editable substrates and often leverage language prompts, pixel inputs, or other visual cues to guide interactive editing. 

_5.2.1 Static scene manipulation._ has increasingly leveraged text and image prompts to enable intuitive and fine-grained manipulations. A series of NeRF-based approaches integrate pretrained 2D diffusion models or vision-language priors, achieving semantic coherent edits. Instruct-NeRF2NeRF[50] proposes a text-driven NeRF editing pipeline that iteratively edits the training images of a NeRF using a pretrained 2D image-conditioned diffusion model, and re-optimizes the NeRF for multiview consistency. Building on this, SIn-NeRF2NeRF[53] enhances object-specific manipulation 

From 2D to 3D Cognition: A Brief Survey of General World Models 

19 

by disentangling object and background regions using multi-view segmentation and background inpainting, supporting object-level transformations like translation and resizing. CLIP-NeRF[154] distills open-vocabulary visual concepts from CLIP[129] into a disentangled conditional NeRF architecture. Given a text prompt or reference image, CLIP encoders extract shape and appearance cues, which guide the NeRF to perform targeted edits with separate control over geometry and texture. A CLIP-based similarity loss is applied to ensure that the edited NeRF maintains multi-view semantic consistency with the input prompts. 

Recent methods extend manipulation to 3DGS-based representations for improved efficiency and editability. GaussianEditor[155] introduces a text-driven 3DGS editing framework that supports fine-grained, region-level manipulation. It first employs an LLM to identify regions of interest (ROI) based on the scene description and user instructions. These textual ROIs guide image-space segmentation via Grounding-DINO and SAM, which is then lifted to 3D space. A pretrained textto-image diffusion model generates edited images from the instructions, serving as supervision to optimize the corresponding 3D Gaussians, thus enabling semantically consistent and localized 3D edits. 

Beyond text prompts, interactive approaches empower users with direct control over object manipulation. Point’n Move[61] presents an interactive 3DGS editing framework based on user’s 2D clicks. Its two-stage self-prompting segmentation strategy first associates user clicks with the appropriate 3D object regions, then propagates the segmentation across multiple views. Upon object selection, the system supports direct manipulations such as translation, rotation, removal by inpainting exposed regions in the 3DGS representation. 

_5.2.2 Dynamic scene manipulation._ poses additional challenges, such as maintaining spatiotemporal coherence and handling object motion. Instruct 4D-to-4D [108] treats a dynamic 4D scene as a collection of pseudo-3D videos. It adopts a pretrained 2D diffusion model augmented with anchor-aware attention to batch-edit key frames consistently. The edits are then propagated both temporally via optical-flow warping and spatially via depth-based projection to other views, achieving sharp, spatially and temporally coherent 4D scene edits. 4D-Editor[66] supports stroke-based editing on dynamic NeRFs. It incorporates semantic priors distilled from a pretrained DINO[15] teacher model and recursive refinement to enhance object tracking and segmentation across time, and employs multi-view temporal inpainting to ensure spatiotemporal coherence. 

Beyond appearance editing, some methods focus on physically plausible dynamic manipulation. NeuPhysics[126] proposes a physics-based framework for dynamic scene manipulation from monocular RGB videos. It represents dynamic scenes using a time-varying signed distance field (SDF) and jointly estimates geometry, appearance, motion, and physics parameters through a differentiable physics engine. By modifying these parameters, it enables dynamic object editing, such as removal, duplication, or recoloring, while maintaining physical plausibility and temporal coherence. For motion-level control, SC-GS[63] enables motion editing of dynamic objects by introducing a set of sparse control points, which guide the deformation of Gaussians over time via a learned deformation MLP. To preserve physical plausibility and spatial continuity, it incorporates an As-Rigid-As-Possible (ARAP) loss that enforces local rigidity during deformation. 

In summary, 3D spatial interaction enables world models to engage with and reshape 3D environments. Egocentric embodied interaction focuses on modeling plausible human/agent behaviors and environment responses, while exocentric scene manipulation emphasizes user-guided scene editing through language, visual, or spatial inputs. Together, these approaches highlight the growing importance of interaction-aware 3D representations that integrate physical constraints, semantic priors, and intuitive control interfaces, laying the groundwork for more intelligent and responsive 3D world models. 

Xie et al. 

20 

# **6 Application** 

World models are powering a wide range of real-world applications, including embodied AI, autonomous driving, digital twins, and gaming/VR. Each of these domains presents unique requirements and constraints. In this section, we investigate the recent advancements of specialized models and platforms that combine the core cognitive capabilities of 3D world modeling to tackle domain-specific challenges and support complex tasks. 

# **6.1 Embodied AI** 


Fig. 7. **Representative paradigm of end-to-end generative world models for embodied AI.** The agent receives raw sensor inputs from the environment and language instructions from the user, and performs alignment using LLMs to generate reasoning and action responses for tasks such as captioning, QA, and task-planning. End-to-end models such as 3D-VLA[191] and LEO[60] leverage this framework to enable intelligent agents to interpret, reason, and act in complex real-world scenes. 

In embodied AI systems, agents must form a deep 3D understanding of their surroundings, by reasoning about spatial relationships, predicting plausible actions, to succeed in complex tasks under real-world scenarios. 

Recent end-to-end generative world models for embodied AI unify perception, reasoning, and action within a shared 3D spatial and semantic representation, enabling agents to understand and interact with complex environments, as illustrated in Fig 7. 3D-VLA[191] introduces a generative vision-language-action model. It builds on a pretrained 3D-centric LLM backbone augmented with interaction tokens, which ingests both textual instructions and 3D observations in a shared embedding space to understanding 3D states and user’ intentions. Then, a series embodied diffusion models are trained and their latent features are aligned with the 3D-LLM’s representation, thus enabling the model to reconstruct current scenes and imagine goal states in form of both RGB-D and point clouds. During inference, given a natural language command, 3D-VLA alternates between invoking the diffusion decoders to predict future observations and using the 3D-LLM to decode corresponding action tokens, effectively closing the loop from perception through prediction to planning in a single forward pass. LEO [60] is a 3D embodied multimodal world models for perception, grounding, reasoning, planning, and action in 3D environments. It first achieves 3D vision–language alignment by using a 2D image encoder for egocentric views and a 3D point-cloud 

From 2D to 3D Cognition: A Brief Survey of General World Models 

21 

encoder for global views. The resulting visual tokens, interleaved with text tokens, form a unified multimodal sequence that is fed into a decoder-only LLM. Then, extending the vocabulary to include both text tokens and discrete action tokens reframes tasks as sequence prediction, enabling end-toend instruction following across diverse tasks. AETHER[145] realizes a unified world modeling framework by co-optimizing 4D dynamic reconstruction, action-conditioned future prediction, and goal-conditioned action planning. Its reconstruction head recovers temporally consistent 3D scene geometry and motion fields from input video sequences. Then, an action-conditioned predictor is trained to forecast future frames given past observations and candidate camera or actor trajectories, leveraging task-interleaved feature learning to share representations between reconstruction and prediction tasks. Finally, a goal-conditioned planner head maps predicted scene changes to camera paths and motion commands. Crucially, losses for reconstruction, prediction, and planning are backpropagated through a shared backbone, enabling jointly optimization and synergistic knowledge transfer. GenEx[98] constructs an explorable 360° panoramic environment from a single RGB image via diffusion-based world generator trained on large-scale, physics-grounded Unreal Engine data. GenEx allows the agent to explore the synthesized panoramic environment and uses the same diffusion model to forecast unseen regions. These imagined observations help the GPT-based planner to update agent’s internal understanding of its surroundings and generate navigation or manipulation commands. In this way, GenEx performs a perception–prediction–planning loop within a unified framework, without relying on an external motion planner. 

Overall, this emerging paradigm paves the way toward more capable and generalizable agents. Future efforts might focus on continual adaptation of internal 3D representations during real-world operation, and seamless integration of learned world models with reactive control loops to enable truly generalist, high-DOF robotic autonomy. 

# **6.2 Autonomous Driving** 

World models for autonomous driving demand real-time performance, long-horizon consistency, and multi-sensor fusion to manage complex traffic environments[151]. Recent advances leverage 3D representations, especially 3D occupancy grids and point clouds, enriched with road priors and spatiotemporal modeling, enabling prediction, planning, and question answering in dynamic driving scenarios. 

OccWorld[192] proposes 3D semantic occupancy grids as its core scene representation, capturing both static infrastructure and dynamic elements. It employs a self-supervised VQVAE “scene tokenizer” to convert dense occupancy grids into discrete tokens encoding structural and semantic information. A GPT-style spatiotemporal transformer then performs spatial mixing for multi-scale context understanding and causal temporal attention for future prediction, jointly forecasting scene evolution and ego-vehicle trajectories. OccLLaMA[162] extends OccWorld by integrating vision, language, and action within a shared token framework. It combines VQVAE-generated scene tokens with language and action vocabularies, processed jointly by LLaMA, enabling multiple tasks such as occupancy forecasting, motion planning, and visual question answering. 

OccSora[156] and DynamicCity[9] further explore 4D generative modeling of long-term driving scene evolution. OccSora leverages a diffusion-based Transformer on compressed temporal tokens for long-horizon generation. DynamicCity[9] introduces HexPlane VAE and DiT diffusion to synthesize high-fidelity future LiDAR or occupancy scenes conditioned on ego trajectories or layout constraints. In parallel, DFIT-OccWorld[184] decomposes scene generation into static occupancy and dynamic flow, integrating camera-derived features via differentiable rendering to strengthen multi-sensor fusion and spatiotemporal coherence, enabling more robust and accurate voxellevel predictions. NeMo[65] employs a two-stage, end-to-end sensorimotor framework that learns 

Xie et al. 

22 

occupancy and motion flow via neural rendering and fuses current and predicted volumetric features for action planning. 

On the point-cloud side, Copilot4D[185] formulates an unsupervised world model on raw LiDAR point clouds. It tokenizes raw LiDAR into discrete tokens using VQVAE and models future states with a discrete diffusion Transformer yielding high-fidelity and physically consistent point-cloud forecasts for autonomous planning. ViDAR[178] introduces a self-supervised pretraining framework termed visual point cloud forecasting. Rather than modeling point clouds directly, ViDAR predicts future LiDAR scans from historical camera images. It projects dense visual features into 3D space and autoregressively generates future point clouds, enabling the joint learning of semantic, geometric, and temporal representations in a self-supervised manner. 

Despite employing different 3D backbones, these world models all unify static and dynamic scene elements into a single latent space, embed road-environment priors to ground predictions in physically plausible structures, and leverage spatiotemporal modeling to ensure long-horizon consistency and capture scene evolution. Future work will focus on integrating richer semantic information, tighter multi-sensor fusion, and more efficient 3D representations to further improve robustness and adaptability in real-world driving. 

# **6.3 Digital Twins** 

Digital twins require precise digital replicas of real-world entities, encompassing both their static geometry and dynamic behaviors. Cutting-edge world models in digital twin city harness efficient 3D representations and embed urban-scene priors, such as structural layouts, road networks, and architectural semantics, to enable scalable, controllable generation of expansive urban environments. 

CityDreamer[170] establishes a compositional framework for unbounded city generation. Operating on a bird’s-eye structural layout, it decomposes urban scenes into background neural fields (roads, greenery) and building instance fields. It uses generative hash grids and periodic embeddings to ensure consistency in geometry and texture while supporting diverse building appearances. CityGaussian[95] builds on this by focusing on efficient, real-time rendering of large cities via 3DGS. It trains a global Gaussian prior to capture overall geometry and appearance and partitions the scene into adaptive blocks. At runtime, Gaussian splats are selected and merged based on view distance, ensuring smooth visual continuity and sustaining interactive frame rates (40–65 FPS) on unbounded cityscapes. CityDreamer4D[171] enhances static city models by explicitly modeling dynamic entities like vehicles. It decouples traffic scenario generation from static layout creation and utilizes three specialized NeRF-based generators to separately model the static city background, buildings, and dynamic vehicles at each time step. This design effectively captures the diversity of different elements within the city, while also supporting local editing of individual building and vehicle instances, enabling fine-grained control and realistic scene composition. 

Procedural controllable generation frameworks automate and customize city creation. SceneX[194] and CityCraft[28], harness LLMs to translate high-level directives into executable scene-creation workflows including asset placements and layout generation. Specifically, CityCraft generates 2D layouts via a diffusion Transformer and uses LLM guidance and asset retrieval tools for diverse, rich urban scenes. CityX[187] further integrates multimodal inputs, including OpenStreetMap (OSM), semantic maps, satellite imagery, and modular procedural plugins for real-time, iterative city editing. UrbanWorld[138] presents an end-to-end generative urban world model that automatically constructs customizable 3D urban environments under flexible control conditions. It first generates coarse 3D layouts from OSM, utilizes an urban-specialized multimodal LLM for asset placement, and applies progressive 3D diffusion to refine geometry and textures. A final LLM-guided polishing 

From 2D to 3D Cognition: A Brief Survey of General World Models 

23 

step aligns global scene consistency. The result is an interactive 3D urban world navigable by embodied agents. 

Collectively, these digital twin world models highlight advancements toward data-driven, controllable, and scalable generation of realistic urban environments. By combining efficient 3D representations with domain priors such as urban layouts and architectural semantics, they enable high-fidelity modeling of both static structures and dynamic agents. Future work will likely explore deeper integration of multimodal inputs, enhanced interactivity, and stronger physical and behavioral consistency to support a broader range of simulation, planning, and decision-making tasks in digital twin cities. 

# **6.4 Gaming/VR** 

In gaming and VR, crafting a physically plausible, immersive, and real-time interactive environments is essential for a compelling user experience. Traditional graphics pipelines rely on complex, costly manual modeling to develop high-quality interactive virtual worlds. Recently, 3D world models grounded in physical knowledge have transformed content generation, enabling automatic 3D scene synthesis and realistic physics-based interactions. 

Video2Game[167] presents an end-to-end pipeline that converts real-world video into interactive, photorealistic game environments. It first trains a large-scale NeRF capturing scene geometry and appearance, then distills it into a UV-mapped neural-textured mesh optimized for real-time rendering. Finally, a physics module integrates rigid-body dynamics and collision constraints, allowing virtual characters to navigate and interact realistically, such as kicking a football governed by real-world physics. VR-GS[68] is an interactive VR system that employs 3DGS alongside a sparse volumetric structure VDB to construct interactive object-level 3D scenes. By integrating a two-level embedding framework with XPBD[101]-based deformable body simulations, it enables real-time, physics-driven interactions and dynamic shadows, supporting intuitive VR gameplay such as petting virtual animals or grasping objects with natural responses. LIVE-GS[103] constructs realistic, interactive VR environments by integrating spatial and physical commonsense through pretrained LLMs and physics simulation. It leverages GPT-4o to analyze physical properties of objects represented as 3D Gaussians, guiding the resulting dynamics to align with real-world behavior. Its PBD-based physics simulation framework supports a wide range of physical forms, including rigid, soft, and granular bodies, enabling rich, semantically grounded interactions without the need for extensive manual design. 

These approaches unify 3D representations with real-world physics, enabling synthesis of interactive VR environments, realistic object behaviors, and natural user interactions. Future advances may include context-aware physics where gameplay intent dynamically shapes simulations and lightweight volumetric streaming for expansive worlds. 

# **7 Challenges and Breakthrough Paths** 

As world models progress toward achieving comprehensive 3D cognition, they encounter a series of persistent challenges that span data, modeling, and deployment. Addressing these obstacles is critical for advancing toward more robust, intelligent, and embodied world models. 

# **7.1 Data** 

World models require jointly reasoning over text, images, video, 3D captures and other sensor streams. However, several challenges impede effective multimodal fusion: 

- **Modality heterogeneity and semantic misalignment:** Disparities in data formats, sampling rates, and feature distributions across various modalities complicate alignment 

Xie et al. 

24 

and synchronization processes. Additionally, semantic gaps between modalities hinder seamless fusion and joint reasoning, often introducing cross-modal noise that degrades the quality of the fused representation. 

- **Data quality and robustness issues in 3D captures:** Real-world 3D data frequently suffer from sensor-induced noise, occlusions, and missing values, adversely affecting model robustness. These quality issues pose significant challenges in accurately capturing and interpreting complex environments, especially in safety-critical applications like autonomous driving. 

- **Dataset limitations and annotation constraints:** Existing datasets often underrepresent rare scenarios, such as extreme weather conditions or unusual traffic incidents, limiting model generalizability. Furthermore, the high cost of dense 3D annotation, particularly for volumetric or point cloud data, restricts the scale and diversity of available training datasets. The lack of synchronized trajectory, control, and state-interaction annotations further impedes progress toward truly interactive and temporally coherent 3D cognition. 

To address these challenges, it is essential to develop standardized data formats and sampling protocols to facilitate alignment across modalities. Employing advanced fusion techniques that account for semantic and distributional differences can enhance integration. Implementing noisereduction algorithms and robust preprocessing methods can mitigate the impact of sensor noise and occlusions. Expanding datasets to include rare and critical scenarios, possibly through data augmentation or simulation, will improve model generalizability. Investing in semi-automated or AI-assisted annotation tools can reduce the costs associated with dense 3D data labeling. Finally, incorporating synchronized trajectory and state-interaction data will enable the modeling of dynamic, interactive environments, advancing the capabilities of world models. 

# **7.2 Modeling** 

World models aim to represent and simulate complex, dynamic environments. However, several challenges impede the development of efficient and accurate models: 

- **Scalability and memory efficiency in 3D scene representations:** Traditional voxel grids and point-cloud networks suffer from cubic (or worse) memory growth as scene scale increases, rendering them inefficient for handling city-level modeling. While sparse structures, such as octrees and Gaussian-splatting representations, can partially alleviate memory demands, achieving an optimal balance between preserving fine-scale geometric or radiance detail and constraining overall memory consumption remains an unresolved challenge. 

- **Integration of complex physical dynamics:** Embedding accurate fluid dynamics, material deformations, and multi-object interactions into neural scene representations remains challenging. High-precision, real-time simulation of complex dynamics is still computationally prohibitive, limiting the applicability of current models in scenarios requiring detailed physical interactions. 

- **Development of real-time, multimodal instruction-to-action pipelines:** Robust pipelines for real-time instruction-to-action, which integrate voice, touch, and visual cues into spatially grounded reasoning and planning, have not been fully developed. The lack of such integrated systems hampers the ability of models to perform real-time, context-aware actions based on multimodal inputs. 

In light of these limitations, the integration of geometric perception architectures with hierarchical sequence models is being explored to enhance 3D representation capabilities. By incorporating physical priors into model training, researchers aim to improve the realism and dynamic stability 

From 2D to 3D Cognition: A Brief Survey of General World Models 

25 

of generated scenes. Furthermore, advancing cross-modal fusion techniques facilitates the coordination of language, vision, and action, which is essential for developing truly interactive and responsive 3D environments. 

# **7.3 Deployment** 

Deploying world models in real-world scenarios presents several challenges that hinder real-time, scalable, and coherent operation: 

- **High model complexity and inference latency:** Large-scale or physics-aware representations often entail substantial computational demands, leading to inference delays that preclude fine-grained, real-time interaction in dynamic 3D environments. This latency undermines the responsiveness required for applications such as autonomous navigation and interactive simulations. 

- **Scalability and coherence in multi-agent systems:** Deploying multiple embodied agents within a shared 3D space introduces challenges related to scalability, real-time responsiveness, and the maintenance of global coherence. Ensuring consistent and synchronized behavior among agents is essential for robust real-world systems. 

Several approaches have emerged to address these challenges. Implementing model compression techniques, such as pruning and quantization, alongside distributed edge computing strategies can reduce latency and computational overhead. Leveraging federated learning, multi-task learning, and transfer learning frameworks further enhances adaptability and generalization across diverse environments. Some approaches suggest that integrating causal reasoning frameworks is critical in specific domains[40], such as embodied intelligence[45], to enable interpretable, multi-factor decision-making and robust planning in novel scenarios. 

# **8 Conclusion** 

This survey explores the evolution of world models, focusing on their transition from 2D visual representations to 3D cognition. By highlighting recent breakthroughs in the field of 3D representation learning, such as NeRF and 3DGS, as well as the integration of world knowledge, we elucidate the three fundamental capabilities required for achieving genuine 3D cognition: 3D physical scene generation, 3D spatial reasoning, and 3D spatial interaction. Through a detailed analysis of practical applications in embodied AI, autonomous driving, digital twins, and gaming/VR, we demonstrate how world models apply these capabilities to complex, dynamic environments. Finally, by analyzing the unresolved challenges in this rapidly evolving field, we emphasize several promising breakthrough directions. Through the synergistic innovation of data, modeling, and deployment, we envision that next-generation world models will progressively evolve into intelligent systems capable of perceiving, reasoning, and acting within richly structured 3D environments, thus bringing us closer to the ultimate goal of achieving robust, general-purpose artificial intelligence. 

# **References** 

> [1] Jad Abou-Chakra, Feras Dayoub, and Niko Sünderhauf. 2024. ParticleNeRF: A Particle-Based Encoding for Online Neural Radiance Fields. In _Proceedings of the 2024 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ . 5975–5984. 

> [2] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, et al. 2024. Gpt-4 Technical Report. arXiv:2303.08774 [cs.CL] 

> [3] Andrea Amaduzzi, Pierluigi Zama Ramirez, Giuseppe Lisanti, Samuele Salti, and Luigi Di Stefano. 2024. LLaNA: Large Language and NeRF Assistant. _Advances in Neural Information Processing Systems_ 37 (2024), 1162–1195. 

> [4] Haotian Bai, Yuanhuiyi Lyu, Lutao Jiang, Sijia Li, Haonan Lu, Xiaodong Lin, and Lin Wang. 2023. CompoNeRF: Text-Guided Multi-Object Compositional NeRF with Editable 3D Scene Layout. arXiv:2303.13843 [cs.CV] 

Xie et al. 

26 

- [5] Francesco Ballerini, Pierluigi Zama Ramirez, Roberto Mirabella, Samuele Salti, and Luigi Di Stefano. 2024. Connecting NeRFs Images and Text. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 866–876. 

- [6] Fan Bao, Shen Nie, Kaiwen Xue, Chongxuan Li, Shi Pu, Yaole Wang, et al. 2023. One Transformer Fits All Distributions in Multi-Modal Diffusion at Scale. In _Proceedings of the 40th International Conference on Machine Learning (ICML)_ . 1692–1717. 

- [7] Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mido Assran, and Nicolas Ballas. 2024. Revisiting Feature Prediction for Learning Visual Representations from Video. _Transactions on Machine Learning Research_ (2024). 

- [8] Deniz A Bezgin, Aaron B Buhendwa, and Nikolaus A Adams. 2023. JAX-Fluids: A Fully-Differentiable High-Order Computational Fluid Dynamics Solver for Compressible Two-Phase Flows. _Computer Physics Communications_ 282 (2023), 108527. 

- [9] Hengwei Bian, Lingdong Kong, Haozhe Xie, Liang Pan, Yu Qiao, and Ziwei Liu. 2025. DynamicCity: Large-Scale 4D Occupancy Generation from Dynamic Scenes. In _Proceedings of the 13th International Conference on Learning Representations (ICLR)_ . 

- [10] Yonatan Bisk, Rowan Zellers, Ronan Le Bras, Jianfeng Gao, and Yejin Choi. 2020. PIQA: Reasoning about Physical Commonsense in Natural Language. In _Proceedings of the AAAI conference on artificial intelligence_ , Vol. 34. 7432–7439. 

- [11] Andreas Blattmann, Robin Rombach, Huan Ling, Tim Dockhorn, Seung Wook Kim, Sanja Fidler, and Karsten Kreis. 2023. Align Your Latents: High-Resolution Video Synthesis with Latent Diffusion Models. In _Proceedings of the 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 22563–22575. 

- [12] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language Models are Few-Shot Learners. _Advances in Neural Information Processing Systems_ 33 (2020), 1877–1901. 

- [13] Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, et al. 2023. Sparks of Artificial General Intelligence: Early experiments with GPT-4. arXiv:2303.12712 [cs.CL] 

- [14] Junyi Cao, Shanyan Guan, Yanhao Ge, Wei Li, Xiaokang Yang, and Chao Ma. 2024. Neuma: Neural Material Adaptor for Visual Grounding of Intrinsic Dynamics. _Advances in Neural Information Processing Systems_ 37 (2024), 65643–65669. 

- [15] Mathilde Caron, Hugo Touvron, Ishan Misra, Hervé Jégou, Julien Mairal, Piotr Bojanowski, and Armand Joulin. 2021. Emerging Properties in Self-Supervised Vision Transformers. In _Proceedings of the 2021 IEEE/CVF International Conference on Computer Vision (ICCV)_ . 

- [16] Amirhosein Chahe and Lifeng Zhou. 2025. Query3D: LLM-Powered Open-Vocabulary Scene Segmentation with Language Embedded 3D Gaussians. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ . 1051–1060. 

- [17] Chang Chen, Yi-Fu Wu, Jaesik Yoon, and Sungjin Ahn. 2024. TransDreamer: Reinforcement Learning with Transformer World Models. arXiv:2202.09481 [cs.LG] 

- [18] Hong Chen, Xin Wang, Yuwei Zhou, Bin Huang, Yipeng Zhang, Wei Feng, et al. 2024. Multi-Modal Generative AI: Multi-modal LLM, Diffusion and Beyond. arXiv:2409.14993 [cs.AI] 

- [19] Hanlin Chen, Fangyin Wei, and Gim Hee Lee. 2024. ChatSplat: 3D Conversational Gaussian Splatting. arXiv:2412.00734 [cs.CV] 

- [20] Sijin Chen, Xin Chen, Chi Zhang, Mingsheng Li, Gang Yu, Hao Fei, et al. 2024. Ll3da: Visual interactive instruction tuning for omni-3d understanding reasoning and planning. In _Proceedings of the 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 26428–26438. 

- [21] Shizhe Chen, Ricardo Garcia, Cordelia Schmid, and Ivan Laptev. 2023. PolarNet: 3D Point Clouds for Language-Guided Robotic Manipulation. In _Proceedings of the 7th Annual Conference on Robot Learning (CoRL)_ . 

- [22] Yilun Chen, Shuai Yang, Haifeng Huang, Tai Wang, Runsen Xu, Ruiyuan Lyu, Dahua Lin, and Jiangmiao Pang. 2024. Grounded 3D-LLM with Referent Tokens. arXiv:2405.10370 [cs.CV] 

- [23] Joseph Cho, Fachrina Dewi Puspitasari, Sheng Zheng, Jingyao Zheng, Lik-Hang Lee, Tae-Ho Kim, et al. 2024. Sora as an AGI World Model? A Complete Survey on Text-to-Video Generation. arXiv:2403.05131 [cs.AI] 

- [24] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, et al. 2023. Palm: Scaling language modeling with pathways. _Journal of Machine Learning Research_ 24, 240 (2023), 1–113. 

- [25] Dana Cohen-Bar, Elad Richardson, Gal Metzer, Raja Giryes, and Daniel Cohen-Or. 2023. Set-the-Scene: Global-Local Training for Generating Controllable NeRF Scenes. In _Proceedings of the 2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ . 2920–2929. 

- [26] Erwin Coumans. 2015. Bullet Physics Simulation. _ACM SIGGRAPH 2015 Courses_ (2015), 1. 

- [27] Filipe de Avila Belbute-Peres, Kevin Smith, Kelsey Allen, Josh Tenenbaum, and J Zico Kolter. 2018. End-to-End Differentiable Physics for Learning and Control. _Advances in Neural Information Processing Systems_ 31 (2018). 

From 2D to 3D Cognition: A Brief Survey of General World Models 

27 

- [28] Jie Deng, Wenhao Chai, Junsheng Huang, Zhonghan Zhao, Qixuan Huang, Mingyan Gao, Jianshu Guo, et al. 2024. CityCraft: A Real Crafter for 3D City Generation. arXiv:2406.04983 [cs.CV] 

- [29] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In _Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1_ . 

- [30] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng, et al. 2024. Understanding World or Predicting Future? A Comprehensive Survey of World Models. arXiv:2411.14499 [cs.CL] 

- [31] Xinlong Dong, Peicheng Shi, Heng Qi, Aixi Yang, and Taonian Liang. 2024. TS-BEV: BEV Object Detection Algorithm Based on Temporal-Spatial Feature Fusion. _Displays_ 84 (2024), 102814. 

- [32] Bardienus P Duisterhof, Zhao Mandi, Yunchao Yao, Jia-Wei Liu, Jenny Seidenschwarz, Mike Zheng Shou, et al. 2024. DeformGS: Scene Flow in Highly Deformable Scenes for Deformable Object Manipulation. _WAFR_ (2024). 

- [33] Patrick Esser, Johnathan Chiu, Parmida Atighehchian, Jonathan Granskog, and Anastasis Germanidis. 2023. Structure and Content-Guided Video Synthesis with Diffusion Models. In _Proceedings of the 2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ . 7346–7356. 

- [34] Jiemin Fang, Taoran Yi, Xinggang Wang, Lingxi Xie, Xiaopeng Zhang, Wenyu Liu, et al. 2022. Fast Dynamic Radiance Fields with Time-Aware Neural Voxels. In _SIGGRAPH Asia 2022 Conference Papers_ . 

- [35] Yutao Feng, Xiang Feng, Yintong Shang, Ying Jiang, Chang Yu, Zeshun Zong, Tianjia Shao, Hongzhi Wu, Kun Zhou, Chenfanfu Jiang, et al. 2025. Gaussian Splashing: Unified Particles for Versatile Motion Synthesis and Rendering. In _Proceedings of the 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 518–529. 

- [36] Yutao Feng, Yintong Shang, Xuan Li, Tianjia Shao, Chenfanfu Jiang, and Yin Yang. 2024. Pie-NeRF: Physics-Based Interactive Elastodynamics with NeRF. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 4450–4461. 

- [37] J. W. Forrester. 1971. Counterintuitive Behavior of Social Systems. _Theory and Decision_ 2, 2 (1971), 109–140. 

- [38] Chuang Gan, Jeremy Schwartz, Seth Alter, Damian Mrowca, Martin Schrimpf, James Traer, et al. 2021. ThreeDWorld: A Platform for Interactive Multi-Modal Physical Simulation. In _Proceedings of the 35th Conference on Neural Information Processing Systems (NeurIPS)_ . 

- [39] Chen Gao, Ayush Saraf, Johannes Kopf, and Jia-Bin Huang. 2021. Dynamic View Synthesis from Dynamic Monocular Video. In _Proceedings of the 2021 IEEE/CVF International Conference on Computer Vision (ICCV)_ . 5712–5721. 

- [40] Quentin Garrido, Nicolas Ballas, Mahmoud Assran, Adrien Bardes, Laurent Najman, Michael Rabbat, Emmanuel Dupoux, and Yann LeCun. 2025. Intuitive physics understanding emerges from self-supervised pretraining on natural videos. arXiv:2502.11831 [cs.CV] 

- [41] Zhiqi Ge, Hongzhe Huang, Mingze Zhou, Juncheng Li, Guoming Wang, Siliang Tang, and Yueting Zhuang. 2024. WorldGPT: Empowering LLM as Multimodal World Model. In _Proceedings of the 32nd ACM International Conference on Multimedia_ . 7346–7355. 

- [42] Rohit Girdhar, Mannat Singh, Andrew Brown, Quentin Duval, Samaneh Azadi, Sai Saketh Rambhatla, et al. 2024. Emu Video: Factorizing Text-to-Video Generation by Explicit Image Conditioning. arXiv:2311.10709 [cs.CV] 

- [43] Minghao Guo, Bohan Wang, Pingchuan Ma, Tianyuan Zhang, Crystal Owens, Chuang Gan, et al. 2024. Physically Compatible 3D Object Modeling from A Single Image. _Advances in Neural Information Processing Systems_ 37 (2024), 119260–119282. 

- [44] Agrim Gupta, Lijun Yu, Kihyuk Sohn, Xiuye Gu, Meera Hahn, Fei-Fei Li, et al. 2024. Photorealistic Video Generation with Diffusion Models. In _Proceedings of the 2024 European Conference on Computer Vision (ECCV)_ . 393–411. 

- [45] Tarun Gupta, Wenbo Gong, Chao Ma, Nick Pawlowski, Agrin Hilmkil, Meyer Scetbon, Marc Rigter, Ade Famoti, Ashley Juan Llorens, Jianfeng Gao, Stefan Bauer, Danica Kragic, Bernhard Schölkopf, and Cheng Zhang. 2024. The Essential Role of Causality in Foundation World Models for Embodied AI. arXiv:2402.06665 [cs.AI] 

- [46] David Ha and Jürgen Schmidhuber. 2018. Recurrent World Models Facilitate Policy Evolution. _Advances in Neural Information Processing Systems_ 31 (2018), 1. 

- [47] David Ha and Jürgen Schmidhuber. 2018. World Models. (2018). 

- [48] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and et al. 2020. Dream to Control: Learning Behaviors by Latent Imagination. In _Proceedings of the 37th International Conference on Machine Learning (ICML)_ . 

- [49] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. 2021. Mastering Atari with Discrete World Models. In _Proceedings of the 38th International Conference on Machine Learning (ICML)_ . 

- [50] Ayaan Haque, Matthew Tancik, Alexei A Efros, Aleksander Holynski, and Angjoo Kanazawa. 2023. InstructNeRF2NeRF: Editing 3D Scenes with Instructions. In _Proceedings of the 2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ . 19740–19750. 

- [51] Jonathan Ho, Tim Salimans, Alexey Gritsenko, William Chan, Mohammad Norouzi, and David J Fleet. 2022. Video Diffusion Models. 8633–8646 pages. 

Xie et al. 

28 

- [52] Philipp Holl, Nils Thuerey, and Vladlen Koltun. 2020. Learning to Control PDEs with Differentiable Physics. In _Proceedings of the 8th International Conference on Learning Representations (ICLR)_ . 

- [53] Jiseung Hong, Changmin Lee, and Gyusang Yu. 2024. SIn-NeRF2NeRF: Editing 3D Scenes with Instructions through Segmentation and Inpainting. arXiv:2408.13285 [cs.CV] 

- [54] Yining Hong, Haoyu Zhen, Peihao Chen, Shuhong Zheng, Yilun Du, Zhenfang Chen, and Chuang Gan. 2023. 3D-LLM: Injecting the 3D World into Large Language Models. _Advances in Neural Information Processing Systems_ 36 (2023), 20482–20494. 

- [55] Taylor A. Howell, Simon Le Cleac’h, Jan Brüdigam, J. Zico Kolter, Mac Schwager, and Zachary Manchester. 2023. Dojo: A Differentiable Physics Engine for Robotics. arXiv:2203.00806 [cs.RO] 

- [56] Yuanming Hu, Luke Anderson, Tzu-Mao Li, Qi Sun, Nathan Carr, Jonathan Ragan-Kelley, and Fredo Durand. 2020. DiffTaichi: Differentiable Programming for Physical Simulation. In _Proceedings of the 8th International Conference on Learning Representations (ICLR)_ . 

- [57] Yuanming Hu, Tzu-Mao Li, Luke Anderson, Jonathan Ragan-Kelley, and Frédo Durand. 2019. Taichi: A Language for High-Performance Computation on Spatially Sparse Data Structures. _ACM Transactions on Graphics (TOG)_ 38, 6 (2019), 1–16. 

- [58] Yuqi Hu, Longguang Wang, Xian Liu, Ling-Hao Chen, Yuwei Guo, Yukai Shi, et al. 2025. Simulating the Real World: A Unified Survey of Multimodal Generative Models. arXiv:2503.04641 [cs.CV] 

- [59] Haifeng Huang, Yilun Chen, Zehan Wang, Rongjie Huang, Runsen Xu, Tai Wang, Luping Liu, Xize Cheng, Yang Zhao, Jiangmiao Pang, and Zhou Zhao. 2024. Chat-Scene: Bridging 3D Scene and Large Language Models with Object Identifiers. In _Proceedings of the 38th Annual Conference on Neural Information Processing Systems (NeurIPS)_ . 

- [60] Jiangyong Huang, Silong Yong, Xiaojian Ma, Xiongkun Linghu, Puhao Li, Yan Wang, Qing Li, Song-Chun Zhu, Baoxiong Jia, and Siyuan Huang. 2024. An Embodied Generalist Agent in 3D World. In _Proceedings of the 41st International Conference on Machine Learning (ICML)_ . 

- [61] Jiajun Huang, Hongchuan Yu, Jianjun Zhang, and Hammadi Nait-Charif. 2024. Point’n Move: Interactive Scene Object Manipulation on Gaussian Splatting Radiance Fields. _IET Image Processing_ 18, 12 (2024), 3507–3517. 

- [62] Kuan-Chih Huang, Xiangtai Li, Lu Qi, Shuicheng YAN, and Ming-Hsuan Yang. 2025. Reason3D: Searching and Reasoning 3D Segmentation via Large Language Model. In _Proceedings of the 2025 International Conference on 3D Vision (3DV)_ . 

- [63] Yi-Hua Huang, Yang-Tian Sun, Ziyi Yang, Xiaoyang Lyu, Yan-Pei Cao, and Xiaojuan Qi. 2024. SC-GS: Sparse-Controlled Gaussian Splatting for Editable Dynamic Scenes. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 4220–4230. 

- [64] Zhiao Huang, Yuanming Hu, Tao Du, Siyuan Zhou, Hao Su, Joshua B. Tenenbaum, and Chuang Gan. 2021. PlasticineLab: A Soft-Body Manipulation Benchmark with Differentiable Physics. arXiv:2104.03311 [cs.LG] 

- [65] Zanming Huang, Jimuyang Zhang, and Eshed Ohn-Bar. 2024. Neural Volumetric World Models for Autonomous Driving. In _Proceedings of the 2024 European Conference on Computer Vision (ECCV)_ . 195–213. 

- [66] Dadong Jiang, Zhihui Ke, Xiaobo Zhou, and Xidong Shi. 2025. 4D-Editor: Interactive Object-Level Editing in Dynamic Neural Radiance Fields via Semantic Distillation. In _Proceedings of the 2025 IEEE/CVF International Conference on 3D Vision (3DV)_ . 

- [67] Nan Jiang, Zhiyuan Zhang, Hongjie Li, Xiaoxuan Ma, Zan Wang, Yixin Chen, et al. 2024. Scaling Up Dynamic Human-Scene Interaction Modeling. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 1737–1747. 

- [68] Ying Jiang, Chang Yu, Tianyi Xie, Xuan Li, Yutao Feng, Huamin Wang, Minchen Li, et al. 2024. VR-GS: A Physical Dynamics-Aware Interactive Gaussian Splatting System in Virtual Reality. In _Proceedings of the ACM SIGGRAPH Conference on Computer Graphics and Interactive Techniques (SIGGRAPH)_ . 

- [69] P. N. Johnson-Laird. 1980. Mental Models in Cognitive Science. _Cognitive Science_ 4, 1 (1980), 71–115. 

- [70] James Kennedy and Russell Eberhart. 1995. Particle Swarm Optimization. In _Proceedings of the International Conference on Neural Networks (ICNN’95)_ , Vol. 4. IEEE, 1942–1948. 

- [71] Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, and George Drettakis. 2023. 3D Gaussian Splatting for Real-Time Radiance Field Rendering. _ACM Transactions on Graphics_ 42, 4 (July 2023). 

- [72] Justin Kerr, Chung Min Kim, Ken Goldberg, Angjoo Kanazawa, and Matthew Tancik. 2023. LERF: Language Embedded Radiance Fields. In _Proceedings of the 2023 IEEE/CVF International Conference on Computer Vision (CVPR)_ . 19729–19739. 

- [73] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Dollar, and Ross Girshick. 2023. Segment Anything. In _Proceedings of the 2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ . 4015–4026. 

- [74] Eric Kolve, Roozbeh Mottaghi, Winson Han, Eli VanderBilt, Luca Weihs, Alvaro Herrasti, and othersi. 2022. AI2-THOR: An Interactive 3D Environment for Visual AI. arXiv:1712.05474 [cs.CV] 

From 2D to 3D Cognition: A Brief Survey of General World Models 

29 

- [75] Dan Kondratyuk, Lijun Yu, Xiuye Gu, José Lezama, Jonathan Huang, Grant Schindler, et al. 2024. VideoPoet: A Large Language Model for Zero-Shot Video Generation. In _Proceedings of the 41st International Conference on Machine Learning (ICML)_ , Vol. 235. 25105–25124. 

- [76] Chen Kong, Chen-Hsuan Lin, and Simon Lucey. 2017. Using Locally Corresponding CAD Models for Dense 3D Reconstructions from A Single Image. In _Proceedings of the 2017 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 4857–4865. 

- [77] Xin Lai, Zhuotao Tian, Yukang Chen, Yanwei Li, Yuhui Yuan, Shu Liu, and Jiaya Jia. 2024. LISA: Reasoning Segmentation via Large Language Model. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 

- [78] Simon Le Cleac’h, Hong-Xing Yu, Michelle Guo, Taylor Howell, Ruohan Gao, Jiajun Wu, Zachary Manchester, and Mac Schwager. 2023. Differentiable Physics Simulation of Dynamics-Augmented Neural Objects. _IEEE Robotics and Automation Letters_ 8, 5 (2023), 2780–2787. 

- [79] Yann LeCun. 2022. _A Path Towards Autonomous Machine Intelligence Version 0.9.2_ . Tech. Rep. 62(1). OpenReview. 1–62 pages. Version 0.9.2, published June 27, 2022. 

- [80] Hongjie Li, Hong-Xing Yu, Jiaman Li, and Jiajun Wu. 2025. ZeroHSI: Zero-Shot 4D Human-Scene Interaction by Video Generation. arXiv:2412.18600 [cs.CV] 

- [81] Jiaman Li, Alexander Clegg, Roozbeh Mottaghi, Jiajun Wu, Xavier Puig, and C Karen Liu. 2024. Controllable Human-Object Interaction Synthesis. In _Proceedings of the 2024 European Conference on Computer Vision (ECCV)_ . 54–72. 

- [82] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. 2023. BLIP-2: Bootstrapping Language-Image Pre-Training with Frozen Image Encoders and Large Language Models. In _Proceedings of the 40th International Conference on Machine Learning (ICML)_ . 

- [83] Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. 2022. BLIP: Bootstrapping Language-Image Pre-Training for Unified Vision-Language Understanding and Generation. In _Proceedings of the 39th International Conference on Machine Learning (ICML)_ . 

- [84] Xuan Li, Yi-Ling Qiao, Peter Yichen Chen, Krishna Murthy Jatavallabhula, Ming Lin, Chenfanfu Jiang, and Chuang Gan. 2023. PAC-NeRF: Physics Augmented Continuum Neural Radiance Fields for Geometry-Agnostic System Identification. In _Proceedings of the 11th International Conference on Learning Representations (ICLR)_ . 

- [85] Yixun Liang, Xin Yang, Jiantao Lin, Haodong Li, Xiaogang Xu, and Yingcong Chen. 2024. LucidDreamer: Towards High-Fidelity Text-to-3D Generation via Interval Score Matching. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 6517–6526. 

- [86] Chen-Hsuan Lin, Jun Gao, Luming Tang, Towaki Takikawa, Xiaohui Zeng, Xun Huang, et al. 2023. Magic3D: HighResolution Text-to-3D Content Creation. In _Proceedings of the 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 

- [87] Jiajing Lin, Zhenzhong Wang, Yongjie Hou, Yuzhou Tang, and Min Jiang. 2024. Phy124: Fast Physics-Driven 4D Content Generation from a Single Image. arXiv:2409.07179 [cs.CV] 

- [88] Minghui Lin, Xiang Wang, Yishan Wang, Shu Wang, Fengqi Dai, Pengxiang Ding, et al. 2025. Exploring the Evolution of Physics Cognition in Video Generation: A Survey. arXiv:2503.21765 [cs.CV] 

- [89] Xingyu Lin, Zhiao Huang, Yunzhu Li, David Held, Joshua B. Tenenbaum, and Chuang Gan. 2022. DiffSkill: Skill Abstraction from Differentiable Physics for Deformable Object Manipulations with Tools. In _Proceedings of the 10th International Conference on Learning Representations (ICLR)_ . 

- [90] Yuchen Lin, Chenguo Lin, Jianjin Xu, and Yadong MU. 2025. OmniPhysGS: 3D Constitutive Gaussians for General Physics-Based Dynamics Generation. In _Proceedings of the 13th International Conference on Learning Representations (ICLR)_ . 

- [91] Yiqi Lin, Hao Wu, Ruichen Wang, Haonan Lu, Xiaodong Lin, Hui Xiong, and Lin Wang. 2023. Towards Languageguided Interactive 3D Generation: LLMs as Layout Interpreter with Generative Feedback. arXiv:2305.15808 [cs.CV] 

- [92] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. 2023. Visual Instruction Tuning. _Advances in Neural Information Processing Systems_ 36 (2023), 34892–34916. 

- [93] Ruoshi Liu, Rundi Wu, Basile Van Hoorick, Pavel Tokmakov, Sergey Zakharov, and Carl Vondrick. 2023. Zero-1-to-3: Zero-Shot One Image to 3D Object. In _Proceedings of the 2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ . 9298–9309. 

- [94] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Qing Jiang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, and Lei Zhang. 2024. Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection. In _Proceedings of the 2024 European Conference on Computer Vision (ECCV)_ . 38–55. 

- [95] Yang Liu, Chuanchen Luo, Lue Fan, Naiyan Wang, Junran Peng, and Zhaoxiang Zhang. 2024. CityGaussian: Real-time High-Quality Large-Scale Scene Rendering with Gaussians. In _Proceedings of the 2024 European Conference on Computer Vision (ECCV)_ . 265–282. 

Xie et al. 

30 

- [96] Yili Liu, Linzhan Mou, Xuan Yu, Chenrui Han, Sitong Mao, Rong Xiong, and Yue Wang. 2024. Let Occ Flow: Self-Supervised 3D Occupancy Flow Prediction. In _Proceedings of the 8th Annual Conference on Robot Learning (CoRL)_ . 

- [97] Zhenyang Liu, Yikai Wang, Sixiao Zheng, Tongying Pan, Longfei Liang, Yanwei Fu, and Xiangyang Xue. 2025. ReasonGrounder: LVLM-Guided Hierarchical Feature Splatting for Open-Vocabulary 3D Visual Grounding and Reasoning. In _Proceedings of the 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 3718–3727. 

- [98] TaiMing Lu, Tianmin Shu, Alan Yuille, Daniel Khashabi, and Jieneng Chen. 2025. GenEx: Generating an Explorable World. In _Proceedings of the 13th International Conference on Learning Representations (ICLR)_ . 

- [99] Xiaojian Ma, Silong Yong, Zilong Zheng, Qing Li, Yitao Liang, Song-Chun Zhu, and Siyuan Huang. 2023. SQA3D: Situated Question Answering in 3D Scenes. In _Proceedings of the 11th International Conference on Learning Representations (ICLR)_ . 

- [100] Miles Macklin. 2022. Warp: A High-Performance Python Framework for GPU Simulation and Graphics. In _NVIDIA GPU Technology Conference (GTC)_ . https://github.com/nvidia/warp 

- [101] Miles Macklin, Matthias Müller, and Nuttapong Chentanez. 2016. XPBD: Position-Based Simulation of Compliant Constrained Dynamics. In _Proceedings of the 9th International Conference on Motion in Games_ . 49–54. 

- [102] Xinji Mai, Zeng Tao, Junxiong Lin, Haoran Wang, Yang Chang, Yanlan Kang, et al. 2024. From Efficient Multimodal Models to World Models: A Survey. arXiv:2407.00118 [cs.LG] 

- [103] Haotian Mao, Zhuoxiong Xu, Siyue Wei, Yule Quan, Nianchen Deng, and Xubo Yang. 2025. LIVE-GS: LLM Powers Interactive VR by Enhancing Gaussian Splatting. In _Proceedings of the 2025 IEEE Conference on Virtual Reality and 3D User Interfaces Abstracts and Workshops (VRW)_ . 1234–1235. 

- [104] Yongsen Mao, Junhao Zhong, Chuan Fang, Jia Zheng, Rui Tang, Hao Zhu, Ping Tan, and Zihan Zhou. 2025. SpatialLM: Training Large Language Models for Structured Indoor Modeling. arXiv:2506.07491 [cs.CV] 

- [105] Lars Mescheder, Michael Oechsle, Michael Niemeyer, Sebastian Nowozin, and Andreas Geiger. 2019. Occupancy Networks: Learning 3D Reconstruction in Function Space. In _Proceedings of the 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 4460–4470. 

- [106] Gal Metzer, Elad Richardson, Or Patashnik, Raja Giryes, and Daniel Cohen-Or. 2023. Latent-NeRF for Shape-Guided Generation of 3D Shapes and Textures. In _Proceedings of the 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 12663–12673. 

- [107] Ben Mildenhall, Pratul P Srinivasan, Matthew Tancik, Jonathan T Barron, Ravi Ramamoorthi, and Ren Ng. 2021. NeRF: Representing Scenes As Neural Radiance Fields for View Synthesis. _Commun. ACM_ 65, 1 (2021), 99–106. 

- [108] Linzhan Mou, Jun-Kun Chen, and Yu-Xiong Wang. 2024. Instruct 4D-to-4D: Editing 4D Scenes as Pseudo-3D Scenes Using 2D Diffusion. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 20176–20185. 

- [109] Matthias Müller, Bruno Heidelberger, Marcus Hennix, and John Ratcliff. 2007. Position Based Dynamics. _Journal of Visual Communication and Image Representation_ 18, 2 (2007), 109–118. 

- [110] Toan Nguyen, Minh Nhat Vu, Baoru Huang, Tuan Van Vo, Vy Truong, Ngan Le, et al. 2024. Language-Conditioned Affordance-Pose Detection in 3D Point Clouds. In _Proceedings of 2024 IEEE International Conference on Robotics and Automation (ICRA)_ . 3071–3078. 

- [111] Alex Nichol, Prafulla Dhariwal, Aditya Ramesh, Pranav Shyam, Pamela Mishkin, Bob McGrew, Ilya Sutskever, and Mark Chen. 2022. GLIDE: Towards Photorealistic Image Generation and Editing with Text-Guided Diffusion Models. In _Proceedings of the 39th International Conference on Machine Learning (ICML)_ . 

- [112] Başak Melis Öcal, Maxim Tatarchenko, Sezer Karaoğlu, and Theo Gevers. 2024. SceneTeller: Language-to-3D Scene Generation. In _Proceedings of the 2024 European Conference on Computer Vision (ECCV)_ . 362–378. 

- [113] Odyssey. 2024. World Models for Film, Gaming, and Beyond. Online. https://odyssey.world/introducing-explorer Accessed: 2025-04-28. 

- [114] OpenAI. 2024. Sora: Creating Video from Text. Online. https://openai.com/research/sora Accessed: 2025-04-28. [115] Jeong Joon Park, Peter Florence, Julian Straub, Richard Newcombe, and Steven Lovegrove. 2019. DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation. In _Proceedings of the 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 165–174. 

- [116] Keunhong Park, Utkarsh Sinha, Jonathan T Barron, Sofien Bouaziz, Dan B Goldman, Steven M Seitz, and Ricardo Martin-Brualla. 2021. Nerfies: Deformable Neural Radiance Fields. In _Proceedings of the 2021 IEEE/CVF International Conference on Computer Vision (ICCV)_ . 5865–5874. 

- [117] Jack Parker-Holder and et al. 2024. Genie 2: A Large-Scale Foundation World Model. Online. https://deepmind.com/ research/publications/2024/genie-2-a-large-scale-foundation-world-model Accessed: 2025-04-28. 

- [118] Georgios Pavlakos, Vasileios Choutas, Nima Ghorbani, Timo Bolkart, Ahmed AA Osman, Dimitrios Tzionas, and Michael J Black. 2019. Expressive Body Capture: 3D Hands, Face, and Body from A Single Image. In _Proceedings of the 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 10975–10985. 

From 2D to 3D Cognition: A Brief Survey of General World Models 

31 

- [119] Ryan Po and Gordon Wetzstein. 2024. Compositional 3D Scene Generation Using Locally Conditioned Diffusion. In _Proceedings of the 2024 International Conference on 3D Vision (3DV)_ . IEEE, 651–663. 

- [120] Dustin Podell, Zion English, Kyle Lacey, Andreas Blattmann, Tim Dockhorn, Jonas Müller, Joe Penna, and Robin Rombach. 2024. SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis. In _Proceedings of the 12th International Conference on Learning Representations (ICLR)_ . 

- [121] Ben Poole, Ajay Jain, Jonathan T. Barron, and Ben Mildenhall. 2023. DreamFusion: Text-to-3D using 2D Diffusion. In _Proceedings of the 11th International Conference on Learning Representations (ICLR)_ . 

- [122] Albert Pumarola, Enric Corona, Gerard Pons-Moll, and Francesc Moreno-Noguer. 2021. D-NeRF: Neural Radiance Fields for Dynamic Scenes. In _Proceedings of the 2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 10318–10327. 

- [123] Charles R Qi, Hao Su, Kaichun Mo, and Leonidas J Guibas. 2017. PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation. In _Proceedings of the 2017 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 652–660. 

- [124] Charles Ruizhongtai Qi, Li Yi, Hao Su, and Leonidas J Guibas. 2017. PointNet++: Deep Hierarchical Feature Learning on Point Sets in A Metric Space. _Advances in Neural Information Processing Systems_ 30 (2017). 

- [125] Zhangyang Qi, Ye Fang, Zeyi Sun, Xiaoyang Wu, Tong Wu, Jiaqi Wang, Dahua Lin, and Hengshuang Zhao. 2024. Gpt4point: A Unified Framework for Point-Language Understanding and Generation. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 26417–26427. 

- [126] Yi-Ling Qiao, Alexander Gao, and Ming Lin. 2022. NeuPhysics: Editable Neural Geometry and Physics from Monocular Videos. _Advances in Neural Information Processing Systems_ 35 (2022), 12841–12854. 

- [127] Yi-Ling Qiao, Junbang Liang, Vladlen Koltun, and Ming C Lin. 2020. Scalable Differentiable Physics for Learning and Control. In _Proceedings of the 37th International Conference on Machine Learning (ICML)_ . 

- [128] Minghan Qin, Wanhua Li, Jiawei Zhou, Haoqian Wang, and Hanspeter Pfister. 2024. LangSplat: 3D Language Gaussian Splatting. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 20051–20060. 

- [129] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, et al. 2021. Learning Transferable Visual Models from Natural Language Supervision. In _Proceedings of the 38th International Conference on Machine Learning (ICML)_ . 8748–8763. 

- [130] Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever, et al. 2018. Improving Language Understanding by Generative Pre-Training. (2018). 

- [131] Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. 2019. Language Models are Unsupervised Multitask Learners. _OpenAI blog_ 1, 8 (2019), 9. 

- [132] Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec Radford, Mark Chen, and Ilya Sutskever. 2021. Zero-Shot Text-to-Image Generation. In _Proceedings of the 38th International Conference on Machine Learning (ICML)_ . 8821–8831. 

- [133] Tianhe Ren, Shilong Liu, Ailing Zeng, Jing Lin, Kunchang Li, He Cao, Jiayu Chen, Xinyu Huang, Yukang Chen, Feng Yan, Zhaoyang Zeng, Hao Zhang, Feng Li, Jie Yang, Hongyang Li, Qing Jiang, and Lei Zhang. 2024. Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks. arXiv:2401.14159 [cs.CV] 

- [134] Jan Robine, Marc Höftmann, Tobias Uelwer, and Stefan Harmeling. 2023. Transformer-based World Models are Happy with 100k Interactions. In _Proceedings of the 11th International Conference on Learning Representations (ICLR)_ . 

- [135] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. 2022. High-Resolution Image Synthesis with Latent Diffusion Models. In _Proceedings of the 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 

- [136] Stuart J Russell and Peter Norvig. 2016. _Artificial Intelligence: A Modern Approach_ . pearson. [137] Manolis Savva, Abhishek Kadian, Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, et al. 2019. Habitat: A platform for embodied ai research. In _Proceedings of the 2019 IEEE/CVF International Conference on Computer Vision (ICCV)_ . 9339–9347. 

- [138] Yu Shang, Yuming Lin, Yu Zheng, Hangyu Fan, Jingtao Ding, Jie Feng, Jiansheng Chen, Li Tian, and Yong Li. 2024. UrbanWorld: An Urban World Model for 3D City Generation. arXiv:2407.11965 [cs.CV] 

- [139] Yidi Shao, Mu Huang, Chen Change Loy, and Bo Dai. 2025. GausSim: Foreseeing Reality by Gaussian Simulator for Elastic Objects. arXiv:2412.17804 [cs.CV] 

- [140] Jin-Chuan Shi, Miao Wang, Hao-Bin Duan, and Shao-Hua Guan. 2024. Language Embedded 3D Gaussians for Open-Vocabulary Scene Understanding. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 5333–5343. 

- [141] Taylor Shin, Yasaman Razeghi, Robert L. Logan IV, Eric Wallace, and Sameer Singh. 2020. AutoPrompt: Eliciting Knowledge from Language Models with Automatically Generated Prompts. In _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ . 4222–4235. 

Xie et al. 

32 

- [142] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. 2023. Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation. In _Proceedings of the 7th Annual Conference on Robot Learning (CoRL)_ . PMLR, 785–799. 

- [143] Deborah Sulsky, Zhen Chen, and Howard L Schreyer. 1994. A Particle Method for History-Dependent Materials. _Computer Methods in Applied Mechanics and Engineering_ 118, 1-2 (1994), 179–196. 

- [144] Jiaxiang Tang, Jiawei Ren, Hang Zhou, Ziwei Liu, and Gang Zeng. 2024. DreamGaussian: Generative Gaussian Splatting for Efficient 3D Content Creation. In _Proceedings of the 12th International Conference on Learning Representations (ICLR)_ . 

- [145] Aether Team, Haoyi Zhu, Yifan Wang, Jianjun Zhou, Wenzheng Chang, Yang Zhou, Zizun Li, et al. 2025. Aether: Geometric-Aware Unified World Modeling. arXiv:2503.18945 [cs.CV] 

- [146] Anh Thai, Songyou Peng, Kyle Genova, Leonidas Guibas, and Thomas Funkhouser. 2025. SplatTalk: 3D VQA with Gaussian Splatting. arXiv:2503.06271 [cs.CV] 

- [147] Xiaoyu Tian, Tao Jiang, Longfei Yun, Yucheng Mao, Huitong Yang, Yue Wang, Yilun Wang, and Hang Zhao. 2023. Occ3D: A Large-Scale 3D Occupancy Prediction Benchmark for Autonomous Driving. _Advances in Neural Information Processing Systems_ 36 (2023), 64318–64330. 

- [148] Emanuel Todorov, Tom Erez, and Yuval Tassa. 2012. MuJoCo: A physics engine for model-based control. In _Proceedings of the 2012 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . 5026–5033. 

- [149] Wenwen Tong, Chonghao Sima, Tai Wang, Li Chen, Silei Wu, Hanming Deng, et al. 2023. Scene As Occupancy. In _Proceedings of the 2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ . 8406–8415. 

- [150] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, et al. 2023. Llama 2: Open Foundation and Fine-Tuned Chat Models. arXiv:2307.09288 [cs.CL] 

- [151] Simeng Tu, Xiaowei Zhou, Dehong Liang, Xiaojie Jiang, Yifan Zhang, Xiaojun Li, and Xiaodong Bai. 2025. The Role of World Models in Shaping Autonomous Driving: A Comprehensive Survey. arXiv:2502.10498 [cs.CV] 

- [152] Nico Uhlemann, Felix Fent, and Markus Lienkamp. 2023. Evaluating Pedestrian Trajectory Prediction Methods with Respect to Autonomous Driving. _Computing Research Repository (CoRR)_ (2023). 

- [153] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. 2019. Representation Learning with Contrastive Predictive Coding. arXiv:1807.03748 [cs.LG] 

- [154] Can Wang, Menglei Chai, Mingming He, Dongdong Chen, and Jing Liao. 2022. CLIP-NeRF: Text-and-Image Driven Manipulation of Neural Radiance Fields. In _Proceedings of the 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 3835–3844. 

- [155] Junjie Wang, Jiemin Fang, Xiaopeng Zhang, Lingxi Xie, and Qi Tian. 2024. GaussianEditor: Editing 3D Gaussians Delicately with Text Instructions. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 20902–20911. 

- [156] Lening Wang, Wenzhao Zheng, Yilong Ren, Han Jiang, Zhiyong Cui, Haiyang Yu, and Jiwen Lu. 2024. OccSora: 4D Occupancy Generation Models as World Simulators for Autonomous Driving. arXiv:2405.20337 [cs.CV] 

- [157] Tsun-Hsuan Wang, Pingchuan Ma, Andrew Everett Spielberg, Zhou Xian, Hao Zhang, Joshua B. Tenenbaum, et al. 2023. SoftZoo: A Soft Robot Co-design Benchmark For Locomotion In Diverse Environments. In _Proceedings of the 11th International Conference on Learning Representations (ICLR)_ . 

- [158] Zan Wang, Yixin Chen, Tengyu Liu, Yixin Zhu, Wei Liang, and Siyuan Huang. 2022. HUMANISE: Languageconditioned Human Motion Generation in 3D Scenes. _Advances in Neural Information Processing Systems_ 35 (2022), 14959–14971. 

- [159] Zehan Wang, Haifeng Huang, Yang Zhao, Ziang Zhang, and Zhou Zhao. 2023. Chat-3D: Data-efficiently Tuning Large Language Model for Universal Dialogue of 3D Scenes. arXiv:2308.08769 [cs.CV] 

- [160] Zhengyi Wang, Cheng Lu, Yikai Wang, Fan Bao, Chongxuan Li, Hang Su, and Jun Zhu. 2023. ProlificDreamer: High-Fidelity and Diverse Text-to-3D Generation with Variational Score Distillation. _Advances in Neural Information Processing Systems_ 36 (2023), 8406–8441. 

- [161] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, et al. 2022. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. _Advances in neural information processing systems_ 35 (2022), 24824–24837. 

- [162] Julong Wei, Shanshuai Yuan, Pengfei Li, Qingda Hu, Zhongxue Gan, and Wenchao Ding. 2024. OccLLaMA: An Occupancy-Language-Action Generative World Model for Autonomous Driving. arXiv:2409.03272 [cs.CV] 

- [163] Yi Wei, Linqing Zhao, Wenzhao Zheng, Zheng Zhu, Jie Zhou, and Jiwen Lu. 2023. SurroundOcc: Multi-Camera 3D Occupancy Prediction for Autonomous Driving. In _Proceedings of the 2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ . 21729–21740. 

- [164] Keenon Werling, Dalton Omens, Jeongseok Lee, Ioannis Exarchos, and C Karen Liu. 2021. Fast and Feature-Complete Differentiable Physics for Articulated Rigid Bodies with Contact. In _Proceedings of the 17th Robotics: Science and Systems_ . 

- [165] Jiajun Wu, Chengkai Zhang, Xiuming Zhang, Zhoutong Zhang, William T Freeman, and Joshua B Tenenbaum. 2018. Learning Shape Priors for Single-View 3D Completion and Reconstruction. In _Proceedings of the 2018 European_ 

From 2D to 3D Cognition: A Brief Survey of General World Models 

33 

_Conference on Computer Vision (ECCV)_ . 646–662. 

- [166] Wayne Wu, Honglin He, Jack He, Yiran Wang, Chenda Duan, Zhizheng Liu, Quanyi Li, and Bolei Zhou. 2025. MetaUrban: An Embodied AI Simulation Platform for Urban Micromobility. In _Proceedings of the 13th International Conference on Learning Representations (ICLR)_ . 

- [167] Hongchi Xia, Zhi-Hao Lin, Wei-Chiu Ma, and Shenlong Wang. 2024. Video2Game: Real-Time Interactive Realistic and Browser-Compatible Environment from a Single Video. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 4578–4588. 

- [168] Zhou Xian, Qiao Yiling, Xu Zhenjia, Wang Tsun-Hsuan, Chen Zhehuan, Zheng Juntian, et al. 2024. _Genesis: A Universal and Generative Physics Engine for Robotics and Beyond_ . https://github.com/Genesis-Embodied-AI/Genesis 

- [169] Zhou Xian, Bo Zhu, Zhenjia Xu, Hsiao-Yu Tung, Antonio Torralba, Katerina Fragkiadaki, and Chuang Gan. 2023. FluidLab: A Differentiable Environment for Benchmarking Complex Fluid Manipulation. In _Proceedings of the 11th International Conference on Learning Representations (ICLR)_ . 

- [170] Haozhe Xie, Zhaoxi Chen, Fangzhou Hong, and Ziwei Liu. 2024. CityDreamer: Compositional Generative Model of Unbounded 3D Cities. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 9666–9675. 

- [171] Haozhe Xie, Zhaoxi Chen, Fangzhou Hong, and Ziwei Liu. 2025. CityDreamer4D: Compositional Generative Model of Unbounded 4D Cities. arXiv:2501.08983 [cs.CV] 

- [172] Tianyi Xie, Zeshun Zong, Yuxing Qiu, Xuan Li, Yutao Feng, Yin Yang, and Chenfanfu Jiang. 2024. PhysGaussian: Physics-Integrated 3D Gaussians for Generative Dynamics. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 4389–4398. 

- [173] Huaiyuan Xu, Junliang Chen, Shiyu Meng, Yi Wang, and Lap-Pui Chau. 2025. A Survey on Occupancy Perception for Autonomous Driving: The Information Fusion Perspective. _Information Fusion_ 114 (2025), 102671. 

- [174] Jie Xu, Viktor Makoviychuk, Yashraj Narang, Fabio Ramos, Wojciech Matusik, Animesh Garg, and Miles Macklin. 2022. Accelerated Policy Learning with Parallel Differentiable Simulation. In _Proceedings of the 10th International Conference on Learning Representations (ICLR)_ . 

- [175] Qingshan Xu, Jiao Liu, Melvin Wong, Caishun Chen, and Yew-Soon Ong. 2024. Precise-Physics Driven Text-to-3D Generation. arXiv:2403.12438 [cs.CV] 

- [176] Runsen Xu, Xiaolong Wang, Tai Wang, Yilun Chen, Jiangmiao Pang, and Dahua Lin. 2024. PointLLM: Empowering Large Language Models to Understand Point Clouds. In _Proceedings of the 2024 European Conference on Computer Vision (ECCV)_ . 131–147. 

- [177] Yandan Yang, Baoxiong Jia, Peiyuan Zhi, and Siyuan Huang. 2024. PhyScene: Physically Interactable 3D Scene Synthesis for Embodied AI. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . 16262–16272. 

- [178] Zetong Yang, Li Chen, Yanan Sun, and Hongyang Li. 2024. Visual Point Cloud Forecasting Enables Scalable Autonomous Driving. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 14673–14684. 

- [179] Hong-Xing Yu, Haoyi Duan, Charles Herrmann, William T Freeman, and Jiajun Wu. 2025. WonderWorld: Interactive 3D Scene Generation from a Single Image. In _Proceedings of the 2025 IEEE/CVF Computer Vision and Pattern Recognition Conference (CVPR)_ . 5916–5926. 

- [180] Hong-Xing Yu, Haoyi Duan, Junhwa Hur, Kyle Sargent, Michael Rubinstein, William T Freeman, et al. 2024. WonderJourney: Going from Anywhere to Everywhere. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 6658–6667. 

- [181] Jiahui Yu, Yuanzhong Xu, Jing Yu Koh, Thang Luong, Gunjan Baid, Zirui Wang, et al. 2024. Scaling Autoregressive Models for Content-Rich Text-to-Image Generation. In _Proceedings of the 12th International Conference on Learning Representations (ICLR)_ . 

- [182] Yan Zeng, Guoqiang Wei, Jiani Zheng, Jiaxin Zou, Yang Wei, Yuchen Zhang, and Hang Li. 2024. Make Pixels Dance: High-Dynamic Video Generation. In _Proceedings of the 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 8850–8860. 

- [183] Chubin Zhang, Juncheng Yan, Yi Wei, Jiaxin Li, Li Liu, Yansong Tang, Yueqi Duan, and Jiwen Lu. 2024. OccNeRF: Self-Supervised Multi-Camera Occupancy Prediction with Neural Radiance Fields. arXiv:2312.09243 [cs.CV] 

- [184] Haiming Zhang, Ying Xue, Xu Yan, Jiacheng Zhang, Weichao Qiu, Dongfeng Bai, Bingbing Liu, Shuguang Cui, and Zhen Li. 2024. An Efficient Occupancy World Model via Decoupled Dynamic Flow and Image-assisted Training. arXiv:2412.13772 [cs.CV] 

- [185] Lunjun Zhang, Yuwen Xiong, Ze Yang, Sergio Casas, Rui Hu, and Raquel Urtasun. 2024. Copilot4D: Learning Unsupervised World Models for Autonomous Driving via Discrete Diffusion. In _Proceedings of the 12th International Conference on Learning Representations (ICLR)_ . 

Xie et al. 

34 

- [186] Qihang Zhang, Chaoyang Wang, Aliaksandr Siarohin, Peiye Zhuang, Yinghao Xu, Ceyuan Yang, Dahua Lin, Bolei Zhou, Sergey Tulyakov, and Hsin-Ying Lee. 2024. Towards Text-Guided 3D Scene Composition. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 6829–6838. 

- [187] Shougao Zhang, Mengqi Zhou, Yuxi Wang, Chuanchen Luo, Rongyu Wang, Yiwei Li, Zhaoxiang Zhang, and Junran Peng. 2024. CityX: Controllable Procedural Content Generation for Unbounded 3D Cities. _Computing Research Repository (CoRR)_ (2024). 

- [188] Hengshuang Zhao, Li Jiang, Jiaya Jia, Philip HS Torr, and Vladlen Koltun. 2021. Point Transformer. In _Proceedings of the 2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 16259–16268. 

- [189] Haoyu Zhao, Hao Wang, Xingyue Zhao, Hao Fei, Hongqiu Wang, Chengjiang Long, and Hua Zou. 2025. PhysSplat: Efficient Physics Simulation for 3D Scenes via MLLM-Guided Gaussian Splatting. arXiv:2411.12789 [cs.CV] 

- [190] Junhui Zhao, Jingyue Shi, and Li Zhuo. 2024. BEV Perception for Autonomous Driving: State of The Art and Future Perspectives. _Expert Systems with Applications_ 258 (2024), 125103. 

- [191] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 2024. 3D-VLA: A 3D Vision-Language-Action Generative World Model. In _Proceedings of the 41st International Conference on Machine Learning (ICML)_ . 

- [192] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. 2024. OccWorld: Learning a 3D Occupancy World Model for Autonomous Driving. In _Proceedings of the 2024 European Conference on Computer Vision (ECCV)_ . 55–72. 

- [193] Licheng Zhong, Hong-Xing Yu, Jiajun Wu, and Yunzhu Li. 2024. Reconstruction and Simulation of Elastic Objects with Spring-Mass 3D Gaussians. In _Proceedings of the 2024 European Conference on Computer Vision (ECCV)_ . 407–423. 

- [194] Mengqi Zhou, Yuxi Wang, Jun Hou, Shougao Zhang, Yiwei Li, Chuanchen Luo, Junran Peng, and Zhaoxiang Zhang. 2025. SceneX: Procedural Controllable Large-Scale Scene Generation. In _Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)_ , Vol. 39. 10806–10814. 

- [195] Xiaoyu Zhou, Xingjian Ran, Yajiao Xiong, Jinlin He, Zhiwei Lin, Yongtao Wang, Deqing Sun, and Ming-Hsuan Yang. 2024. Gala3D: Towards Text-to-3D Complex Scene Generation via Layout-Guided Generative Gaussian Splatting. In _Proceedings of the 41st International Conference on Machine Learning (ICML)_ . 

- [196] Xiaoyu Zhou, Jingqi Wang, Yongtao Wang, Yufei Wei, Nan Dong, and Ming-Hsuan Yang. 2025. OccGS: Zero-shot 3D Occupancy Reconstruction with Semantic and Geometric-Aware Gaussian Splatting. arXiv:2502.04981 [cs.CV] 

- [197] Yang Zhou, Zongjin He, Qixuan Li, and Chao Wang. 2025. LayoutDreamer: Physics-Guided Layout for Text-to-3D Compositional Scene Generation. arXiv:2502.01949 [cs.CV] 

- [198] Olgierd Cecil Zienkiewicz and Robert Leroy Taylor. 2005. _The Finite Element Method for Solid and Structural Mechanics_ . Elsevier. 

