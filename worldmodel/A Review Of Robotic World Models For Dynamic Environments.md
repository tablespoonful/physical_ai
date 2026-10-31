---
title: "A Review Of Robotic World Models For Dynamic Environments Based On Factor And Scene Graphs"
date: "2026-07-27"
authors: "Marco Giberna; Miguel Fernandez-Cortizas; Jose Luis Sanchez Lopez; Holger Voos"
url: https://arxiv.org/abs/2610.08800
pdf: https://arxiv.org/pdf/2610.08800
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.08800)** / [論文ページ](https://arxiv.org/abs/2610.08800)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

A Review Of Robotic World Models For Dynamic Environments Based On Factor And Scene Graphs 

Marco Giberna, Miguel Fernandez-Cortizas, Jose Luis Sanchez Lopez, and Holger Voos 

# **Abstract** 

Models based on graphs have emerged in robotics as a powerful foundation for internal world representations, where factor and scene graphs are among the most prominent model types found in the related literature and in successful robotic solutions. Initially, many of these models were assuming static environments as a simplification. Herein, factor graphs mainly provide uncertainty-aware geometric estimations while scene graphs enable a structured semantic abstraction. However, real-world robotic environments are often dynamic, posing severe challenges for purely static world representations. Therefore, this review presents a comprehensive view on how dynamic aspects of real-world environments can be addressed in such graph-based world models. We organize our assessments around three main aspects: (I) suitable representations, (II) pipelines to construct and update the representations, and (III) their exploitation for downstream tasks. We review approaches that are either based on factor or scene graphs, but put special emphasis on novel approaches that combine both types to form hybrid models. We mainly analyze how different types of dynamics can be modeled herein, and categorize common architectural patterns. Finally, emerging trends and open challenges are identified, including uncertainty propagation from learned perception through the representation layers, the observability of dynamic-entity motion and scale under minimal sensing, scalable lifelong maintenance, and the lack of datasets and evaluation protocols that ground world-model quality in downstream task performance under dynamics. **Keywords:** Factor Graphs, Scene Graphs, Robotic World Models, SLAM, Autonomous Mobile Robots. 

# **1 Introduction** 

Robotic autonomy relies on the ability to construct, maintain and exploit internal representations of the world. These representations serve as a robot’s mental map, enabling the grounding of perception into action and supporting decision-making and action generation 

Authors are with the Automation and Robotics Research Group, Interdisciplinary Centre for Security, Reliability and Trust (SnT), University of Luxembourg. Holger Voos is also associated with the Faculty of Science, Technology and Medicine, University of Luxembourg, Luxembourg. **Acknowledgment:** This work was partially funded by the Fonds National de la Recherche of Luxembourg (FNR) through the DEUS project (Ref. C22/IS/17387634/DEUS) and the project PCS-GRAPHS (Ref. C25/IS/19613768/PCS-GRAPHS). 

to achieve desired tasks. World representations are necessary for mobile robots, even if they only come in a simple static form. Geometric maps such as point clouds, occupancy grids, or meshes provide the spatial substrate required for localization, navigation, and collision-free motion planning [1]. Without such representations, even basic tasks like obstacle avoidance and exploration in any environment would be infeasible. 

Beyond low-level geometry, many robotic applications require richer and more structured representations. Mobile manipulation and object retrieval, for instance, require identifying not only where the robot is, but also _what_ objects exist, _where_ they are located, and _how_ they relate to one another (e.g. a human _sitting on_ the chair _next to_ the table _in_ the kitchen) [2]. Similarly, longhorizon task planning and human-robot interaction depend on representations that support abstraction and reasoning, aligning the robot and human’s understanding of the environment. Commands expressed in natural language cannot be grounded directly in metric maps, but require semantic entities, relational structure, and symbolic reasoning over space [3] [4]. Models based on graph structures provide an expressive framework for constructing such required world representations. In particular, factor graphs and scene graphs have emerged as the two most prominent, yet complementary graphbased approaches that bridge perception, estimation, and reasoning. 

Initially, based on the insight that probabilistic approaches were much better suited to cope with the uncertainty inherent in robotic applications than deterministic ones, Probabilistic Graphical Models (PGMs) and especially factor graphs became very successful in robot perception and especially in simultaneous localization and mapping (SLAM) [1]. They offer a very suitable mathematically grounded uncertainty-aware representation of the environment, explicitly modeling the dependencies between uncertain robot states, landmarks, objects and noisy sensor measurements into a unified PGM, see e.g., [5], [6]. Their formulation enables scalable inference through optimization, making them well suited for common robotic tasks such as SLAM, sensor fusion in the presence of noise and partial observability [6], but also probabilistic approaches for planning and control [7]. Scene graphs, on the other hand, emphasize structure and semantics by representing the environment as entities (nodes, subjects, and objects) and relations (edges, predicates). They capture spatial, functional, and semantic relationships at multiple levels of abstractions by inferring concepts from the raw perception [8], [9]. Recent works such as [10], [11] increas- 

1 

ingly combine these paradigms, yielding hybrid representations in which factor graphs provide a probabilistic mathematical model of the geometric aspects of the environment while scene graphs support semantic abstraction and reasoning in parallel. 

Factor and scene graphs were originally widely adopted in static robotic world representations. However, those are fundamentally limited in real-world settings, as most environments for mobile robot applications such as homes, offices, construction sites, or warehouses, are inherently dynamic [12], [2]. Objects move, humans interact with and alter the environment, furniture is rearranged, doors open and close, and entire structures evolve over time. All of these dynamic processes can be organized across different temporal scales, ranging from continuously moving agents to longterm structural changes, as described later in more detail. Static maps implicitly assume permanence and consistency, making them less accurate when employed in situations presenting persistent motion or long-term changes [13]. This mismatch leads to, for example, a decreasing localization accuracy, incorrect data association, spurious landmarks, and eventually the failure in downstream tasks. Moreover, static representations cannot capture temporal phenomena such as object lifetimes, motion patterns, or recurring routines, essential for future state prediction and long-term robot autonomy [14], [15]. 

These limitations have motivated a growing body of research on dynamic world representations, where time, changes, and uncertainty are paramount and the center of attention, and also led to related extensions of models based on factor and scene graphs. They enable robots not only to estimate _what is currently true_ , but also to reason about _what has changed_ , _what persists_ , and _what is likely to happen next_ from a lower geometric and uncertainty grounded space up to higher semantic and abstracted layers [15] [16]. As the number of such solutions is currently quickly expanding, this review aims to organize this landscape by addressing three main research questions: 

1. **Which representations (world models) based on factor and scene graphs do exist for robotic autonomy in dynamic environments?** We analyze the strengths and limitations of the usage of factor graphs, scene graphs and especially hybrid representations with respect to a taxonomy of dynamic aspects of the environment. 

2. **How can such representations be constructed and maintained?** We review methods for perception, data association, temporal modeling, uncertainty handling, and inference using graph-based approaches, highlighting how different works generate dynamic world models from sensor data. 

3. **How can such representations be exploited?** We examine how dynamic graph-based world models can be used for downstream tasks such as navigation, manipulation, task planning, predictive in- 

teraction and semantic reasoning, and how evaluation metrics can be used for an assessment. 

By organizing and assessing existing works around these questions, this review provides a comprehensive perspective on spatio-temporal scene modeling through the specific use of graph-based representations, namely factor graphs and scene graphs, showcasing current trends and identifying open challenges, to provide a foundation for future research in long-term, robust robotic situational awareness in dynamic environments [2]. This review is not only a catalog of existing approaches, but also discusses a conceptual combination of factor and scene graphs for dynamic world modeling. We intentionally organize prior work through the lens of representational choices, inference structure, and temporal dynamics. 

# **2 Background and Related Works** 

## **2.1 Mobile Robot Graph-Based World Models** 

In this section we first briefly summarize the use of factor graphs, scene graphs and hybrid forms of both for robotic world modeling. We then define _dynamics_ in the context of robotics and finally provide an overview of existing surveys and reviews of the use of factor and scene graphs, particularly for modeling _dynamic_ robot environments, and identify research gaps herein, which motivate this review article. 

### **2.1.1 Factor Graphs** 

Factor graphs have emerged as a primary mathematical framework mainly for geometric world models, providing a flexible approach for integrating various sensor data and prior knowledge into a unified, probabilistic optimization problem [17] [18]. In general, a factor graph describes the structure of a factorization of a function. For instance, consider a function _J_ ( _X_ ) of a set of variables _X_ = _{x_ 1 _, . . . , xn}_ , that factors into a product of _r_ local functions or “factors” _ϕj_ ( _Xj_ ) of a subset _Xj_ of _X_ , respectively: 


A factor graph _G_ = _{X, F, E}_ is an undirected bipartite graph that consists of the set of variable nodes _X_ , typically depicted as circles, and the set of factor nodes _F_ , typically depicted as squares. The set _E_ involves the edges connecting variable nodes and factor nodes. The example in Figure 1 shows a factor graph with 5 variables _X_ = _{x_ 1 _, . . . , x_ 5 _}_ and 8 factors _F_ = _{ϕ_ 1 _, . . . , ϕ_ 8 _}_ , representing the factorization 


2 


Figure 1: Factor graph example. 

In a probabilistic formulation, factor graphs can be used as a PGM representing the factorization of a joint probability distribution over state variables [18]. Within probabilistic robotic world modeling, a factor graph encodes all forms of uncertainty, such as for instance those arising from noisy sensor measurements. In this case, the variables _X_ represent quantities to be estimated, such as robot poses ( _Xk_ ), static map points ( _Mj_ ) or, crucial in dynamic settings, objects and agent poses ( _Lk,t_ ) and motion transformations ( _Hk,t_ ) [19] [20] [16]. The factors _ϕ_ encode constraints or measurements, such as odometry ( _ϕodom_ ), visual reprojection errors ( _ϕrepr_ ), point-to-plane ( _ϕICP_ ), structural priors ( _ϕpose−plane_ , _ϕwall−room_ ) or semantic motion priors ( _ϕmot_ ) [16] [18] [19] [21]. In the example in Figure 1, _x_ 1 _, x_ 2 _, x_ 3 might be robot poses, while _x_ 4 _, x_ 5 might represent two landmark poses. The factors _ϕ_ 1 _, ϕ_ 7 _, ϕ_ 8 represent pose priors, _ϕ_ 2 _, ϕ_ 3 could be odometry measurements, and _ϕ_ 4 _, ϕ_ 5 _, ϕ_ 6 represent measurements of the landmark poses from the related robot poses, respectively. 

The strength of factor graphs lies in their capacity to combine diverse types of constraints while explicitly handling uncertainty and measurement noise [22]. Variables are typically modeled under the assumption of zero-mean Gaussian noise, where the information matrix (i.e., the inverse of the covariance matrix) determines the weight of each factor. Factor graphs are often exploited (e.g., in SLAM) to estimate the most likely value of all variables using Maximum A Posteriori (MAP) inference in form of nonlinear least-squares optimization [17]. 

### **2.1.2 Scene Graphs** 

Scene Graphs were originally invented in computer vision, based on the intention to describe the detailed semantics of a scene shown in a digital image. A scene graph encodes object instances, attributes of objects, and relationships between objects [23]. This simple formulation is powerful enough to describe visual scenes in great detail because it places no restriction on the types of objects, attributes, and relationships that can be represented. Figure 2 shows an example of a scene graph (right) of a captured image (left). This example illustrates that object instances may be physical objects (“robot”), locations (“floor”), things (“storage case”) 

or parts of other objects. Attributes can describe color (“robot is yellow”), type (“quadruped”), shape or pose. Relationships describe the connections between pairs of objects and can encode geometry (“in front of”) or positions, actions (“stands on”), or object parts (“shelf contains cases”). These relationships are usually expressed as _⟨ subject - predicate - object ⟩_ triplets. 

Formally, given a set of object classes _C_ , a set of attribute types _A_ , and a set of relationship types _R_ , a scene graph _G_ is defined as a tuple _G_ = ( _O_ ; _E_ ) where _O_ = _{o_ 1; _. . ._ ; _on}_ is a set of objects and _E ⊆O × R × O_ is a set of edges. Each object has the form _oi_ = ( _ci_ ; _Ai_ ) where _ci ∈C_ is the class of the object and _Ai ⊆A_ are the attributes of the object [8]. 

The generation of scene graphs is mainly based on machine learning approaches and can be roughly divided into three parts: feature extraction, contextualization, and graph construction and reasoning [24]. Herein, the process of feature extraction is mainly responsible for encoding objects or object pairs in the image. Contextualization plays the role of associating different entities and is mainly used to enhance the contextual information between entities. Finally, these contextual information are used to predict the predicate and complete the construction and inference of the graph. There are currently two main types of scene graph generation [24], [8]. The topdown methods comprise two sequential stages, namely object detection and pairwise relationship recognition, while the bottom-up method involves jointly detecting and recognizing the objects and their relationships [25]. 

As scene graphs can abstract objects and the relationships between them in a more explicit and easierto-understand way, they became quite popular for visual scene understanding in general computer vision, but also in robotics. The conceptual shift from dense, low-level metric maps towards scene graphs represents a significant advancement in robotic world modeling. In robotics, scene graphs offer an abstract, layered representation that bridges the gap between the raw geometric perception and high-level symbolic reasoning [2]. By decomposing an environment into a scene graph structure robots can move beyond flat representations, such as occupancy grids or point clouds, to models that capture the semantic and relational architecture of the world. 

As scene graphs might rapidly grow in real-world complex environments, the literature distinguishes between two primary structural paradigms: 

- Flat Scene Graphs: these models treat all entities 


Figure 2: Example image of a scene (left) and related scene graph (right). 

3 

equally at a single level of representation, focusing on object-level nodes and their direct relationships [9]. Approaches such as ConceptGraphs [26] and SceneGraphFusion [27] utilize this approach to manage open-vocabulary object recognition and incremental updates in cluttered scenes where clear structural hierarchies may be emergent rather than predefined. 

- Hierarchical Scene Graphs: these represent the environment across multiple levels of abstraction, grouping lower level elements into semantically richer containers, e.g. objects within rooms, rooms within buildings [28] [11]. This multi-resolution approach is crucial for scalability in large-scale environments, as it allows robots to perform long-term planning and inference over compact abstractions rather than dense data [9]. 

Hierarchical frameworks like Hydra [10] or S-Graphs [11] adopt a bottom-up stack comprising distinct layers specifically for indoor environments: (1) MetricSemantic Mesh, Pointcloud, (2) Objects and Agents, (3) Places and Structures, (4) Rooms and Floors, and (5) Building. An example that extends these works to outdoor scenes is [29] that proposes a hierarchical scene graph of a traffic scenario comprising 6 layers: (1) Keyframes & Point clouds, (2) Lane Graph, (3) Vehicles, (4) Landmarks, (5) Roads & Intersections, and (6) Environment. 

As real-world scenes are three-dimensional, the idea of scene graphs has been extended to 3D space, leading to 3D scene graphs (3DSG) [30] [31]. Edges in a 3DSG encode the connections within the world model through several relationship types, such as: 

- Spatial Relations: These include geometric constraints such as _on_ , _in_ , _adjacent to_ and _support_ [9] [32]. 

- Visibility and Proximity: _Co-visibility_ edges link objects seen simultaneously, while _close-to_ edges often use nearest-neighbourg k-d tree to define spatial proximity [33]. 

- Functional Relations: a newer class of edges representing operational dependencies. OpenFunGraph models these as directed edges between “interactive elements”, such as switches and handles, and objects that they influence, e.g. _controls_ a light, _opens_ a cabinet [34]. 

- Affordances: attributes or edges that define possible interactions which can change the entities states, such as _sit on_ , _opening_ , _pulling_ , providing the robot with actionable knowledge [9]. 

- Containment and Affiliation: Inter-layer edges such as _part of_ , _located in_ or _contains_ facilitate hierarchical queries [9] [33]. 

This structured abstraction allows robots to move beyond simple obstacle avoidance, static mapping and localization, towards actionable spatial perception, where 

the world model serves as a persistent, queryable memory for complex multi-step tasks in evolving robothuman shared spaces. Two examples of a 3DSG are shown in Figure 3. 


Figure 3: Example of 3DSGs created by (a) Kimera [35] and (b) S-Graphs [36]. 

### **2.1.3 Hybrid Models using Factor and Scene Graphs** 

A scene graph answers _“what exists and how it relates”_ , while a factor graph answers _“where it is, and how certain, consistent it is with sensor measurements”_ . Therefore, it seems promising to combine these two paradigms to a more comprehensive world representation. Recent robotics 3DSG solutions explicitly include a pose-graph layer as the uncertainty-bearing backbone, and the integration of the two paradigms creates a multi-resolution framework which bridges metric-semantic perception with high-level symbolic reasoning [35] [36]. In this hybrid paradigm, factor graphs serve as the probabilistic geometric backbone, while scene graphs provide the relational architecture necessary for task-level autonomy in dynamic environments [9] [28]. 

The literature converges to a small set of recurring architectural patterns for coupling the two paradigms, each representing a different trade-off between integra- 

4 

tion tightness and modularity. The most prevalent pattern is the **layered stack with factor graph backbone** : the factor graph simultaneously optimizes the robot’s trajectory and the metric-semantic mesh, whose globally and temporally consistent output is then fed to a separate scene graph parser that builds the relational structure on top. Hydra [10] and Kimera [35] support this approach, where a dedicated parsing thread incrementally constructs the scene graph from the optimized metric layer. The advantage is modularity, where the scene graph logic can be developed independently of the SLAM back-end, but the disadvantage is a onedirectional information flow: the scene graph is informed by the factor graph, but semantic information rarely propagates back to improve localization. 

A tighter alternative is the **single unified optimizable graph** , in which scene graph entities are incorporated directly as variables and factors within the same factor graph that optimizes robot poses. S-Graphs [11] and its visual counterpart vS-Graphs [37] introduced this pattern, merging SLAM and scene graph into a single multi-layered jointly optimizable factor graph where walls, rooms, and floors appear as semantic variables constrained by geometric factors. This enables bidirectional information flow: geometric observation constrain semantic entity positions, but semantic structural priors in turn constrain and regularize ego-trajectory estimation, demonstrably reducing drift compared to purely geometric approaches. 

A third pattern, the **loosely coupled parallel architecture** , maintains the factor graph and scene graph as separate optimization problems connected only through shared node positions, avoiding the computational cost of joint optimization at the expense of weaker consistency guarantees [28]. 

## **2.2 Dynamics in the Context of Robotics** 

It is necessary to fix what we mean by _dynamics_ , since the term is used inconsistently across robotics and adjacent fields. In classical mechanics, dynamics concerns forces and torques and their effect on motion; in dynamical system theory, it describes the time-evolution of a point in a geometric state space; in computer science, a “dynamic“ data structure refers to memory organization rather than physical change. Within mobile robotics, the terms is used more narrowly and typically refers to external, uncontrolled moving entities, such as pedestrians and vehicles, that a robot must perceive and account for during localization and mapping [38]. 

This robotics-specific usage, however, is itself too narrow for our purpose. Hahnel et al. [39] offered one of the first attempts to define dynamics as an environmental property, stating that an environment is dynamic if it changes over time or if moving objects are present within it. This definition is useful but indirect, and, being framed around discrete macroscopic objects, does not make explicit how motion that is never directly observed, e.g. a chair found in a new location, should be treated. Therefore, we adopt the definition of dynamics given in [38]: 

**Definition 1 (Dynamics)** _Dynamics are any directly or indirectly perceivable motions._ 

This formulation is deliberately broad. _Direct_ perceivability covers motion observed as it occurs given an appropriate sensor. _Indirect_ perceivability covers semistatic entities, such as relocated furniture, whose motion is never itself observed but whose resulting change of state is. This distinction between direct and indirect perceivability, rather than any specific list of entity types or timescales, is what we take to be the essential content of Definition 1, and it is this distinction, not a fixed taxonomy, that Kucner et al. [38] leave open for further specialization within a given application domain. 

Definition 1 tells us _what_ qualifies as dynamics. It does not by itself prescribe how a world model should organize or respond to difference instances of it. In Section 3, we build on this definition to introduce a taxonomy of dynamics tailored to graph-based robotic world models, organized primarily around the temporal horizon at which a perceivable motion or change occurs. 

## **2.3 Assessment of Previous Surveys and Reviews** 

Probabilistic Graphical Models provide the foundational framework for modeling large-scale inference problems in robotics, with factor graphs serving as a bipartite representation where variables denote unknown states and factors represent local constraints derived from sensor data [5] [6]. Traditional reviews trace the maturity of SLAM from early formulations based on Kalman filters and Bayesian estimation toward modern graph-based optimization paradigms [40] [1]. Systematic surveys of spatial perception frameworks have categorized scene modeling techniques into three primary layers: metric, metric-semantic, and metric-semantic-topological [40]. This highlights a trend shifting away from purely geometric representations like point clouds or meshes, toward advanced data structures that incorporate highlevel concepts such as instances and places [2]. 

Complementary to reviews of metric frameworks, existing reviews of scene graphs define them as structured representations that encode semantic entities and their interrelationships to facilitate human-like reasoning [8] [41] [42]. Early literature in this domain primarily focused on offline image retrieval and 2D scene graph generation, though more recent reviews highlight advancements in 3D scene graphs capable of capturing metrics, semantics and objects (also including dynamic agents) within a unified actionable model [8] [42]. 

Notably, these two types of reviews have developed largely independently: reviews of factor graphs assess uncertainty-aware geometric estimation, while reviews of scene graphs assess semantic and relational abstraction, but very few works survey both representations _jointly_ as complementary layers of a single world model. A first recent attempt in this direction is the review of Catalano et al. [9], which focuses on works that combine geometry, semantics, and action within unified representations; however, this overview does not center on 

5 

dynamics, nor does it systematically analyze the coupling patterns, uncertainty propagation, or construction pipelines that arise when factor and scene graphs are combined specifically to handle non-stationary environments. 

The landscape of SLAM in dynamic environments has been analyzed as a progressive evolution from purely geometric methods to advanced semantic-based paradigms [43] [44] [45]. Existing surveys categorize solution approaches into those that maintain localization stability by excluding dynamic elements as outliers and those that perform active Simultaneous Localization, Mapping and Moving Object Tracking (SLAMMOT) [12] [46]. Furthermore, dedicated reviews on feature requirements in dynamic SLAM weight the trade-offs between low-level primitives, such as points or lines, and highlevel semantic labels, suggesting that robust robotic autonomy may require the integrated usage of both feature levels [46]. These dynamic-SLAM surveys, however, largely set aside the scene-graph literature, and consequently do not address how semantic-relational structure should be maintained under dynamics, nor how it interacts with the probabilistic backbone of the factor graph. 

A separate line of work addresses dynamics as a phenomenon in its own right, independent of any specific representation. Kucner et al. [38] survey Maps of Dynamics (MoDs) and propose a general definition and characterization of dynamics for mobile robotics, which we adopted and extended in Section 2.2 and organize into a temporal-horizon taxonomy in Section 3. While their survey provides a rigorous treatment of _what_ dynamic phenomena are and how they can be statistically modeled over space and time, it is agnostic to the underlying world-model representation, and does not address factor graphs, scene graphs, or their hybrid forms. 

Despite the depth of reviews in individual subfields, critical gaps in the existing review or survey literature can be identified. Key surveys often focus on isolated areas like perception or planning while overlooking the practical integration of these components [47] [2]. Gaps also remain in analyzing the long-term usability of maps in complex dynamic scenes and handling the non-rigid deformations inherent in highly dynamic environments [44] [1]. Taken together, these limitations reveal a fragmented landscape in which probabilistic estimation (factor graphs), semantic scene understanding (scene graphs), and the characterization of dynamics have each matured in relative isolation, with limited cross-pollination between the three. To the best of our knowledge, no existing survey or review jointly addresses the full pipeline from probabilistic spatio-temporal estimation to structured semantic reasoning especially in _dynamic_ environments, nor does any work systematically analyze how these two paradigms can be combined to achieve robust, long-term or even lifelong situational awareness. 

This review addresses these gaps directly. We first establish a shared characterization of dynamics (Section 3), building on and extending the definition of Kucner et al. [38] and based on the surveyed literature, and then assess existing works with respect to three ques- 

Table 1: Primary temporal-horizon axis used to organize dynamics in graph-based robot world models. 

|**Tier**|**Timesca**|**leDescription**|
|---|---|---|
|Short-<br>Term<br>Dynamics|Continuo<br>/ Now|us<br>Independently<br>moving<br>entities<br>whose<br>pose<br>changes during observation, such as humans,<br>vehicles, or robots|
|Semi-<br>Static<br>Changes|Minutes–<br>Days|Entities that are static during a single observa-<br>tion but may be relocated, added, removed, or<br>change state between observations|
|Long-<br>Term<br>Structural<br>Changes|Days–<br>Years|Persistent modifications to the built environ-<br>ment itself, such as layout changes, renovations,<br>or seasonal structural variations|


tions: which graph-based representations are suited to dynamic environments (Section 4), how they are constructed and maintained (Section 5), and how they are exploited for downstream tasks (Sections 6–7). Additionally,we present the commonly used evaluation protocols, datasets, and metrics for tesing in 8, and a comprehensive comparison of existing related works in 9. Finally, we conclude this review by highlighting the open challenges identified and outlining future research directions in 10. In doing so, this review provides a unified perspective on the synergy between factor graphs and scene graphs as complementary and mutually reinforcing tools for long-term robotic autonomy under dynamics. 

# **3 Taxonomy of Dynamic Aspects in Robotic World Models** 

Before analyzing how factor graphs and scene graphs represent, construct and exploit non-stationary environment, we first set the vocabulary this review adopts to describe _dynamics themselves_ . The literature is not consistent here: the same underlying phenomenon, e.g., a chair being moved between visits, is variously described as a _semi-static change_ [48], a _movable_ object [22] or a node with a _persistence_ attribute [33]. Establishing a shared characterization upfront allows us to classify representations, pipelines, and applications along consistent axes for the remainder of the review. 

We organize dynamics along three axes: _when_ a change occurs relative to observation (Temporal Horizon), _what_ kind of entity undergoes it (Entity Typology), and _how_ the change manifests in the representation (State Expression). A fourth property, the _predictability_ of a dynamic entity’s behavior, is briefly noted at the end of this section since it is only sparsely addressed by the surveyed literature. 

## **3.1 Primary Axis: Temporal Horizon** 

The dimension that structures most consistently both individual models and this review is _when_ a change occurs relative to the robot’s observation stream, since it directly governs the memory allocation, data association strategy, and update frequency a world model must support. We distinguish three tiers: 

6 

- **Short-Term Dynamics** (continuous motion, now): humans, moving vehicles, and other independently moving entities whose pose changes within the timescale of a single operating session, requiring real-time tracking and motion-aware data association [19] [16] [15]. 

- **Semi-Static Changes** (minutes to days): objects that are stationary during any single observation but relocated, added, removed, or statetransitioned between observations, e.g., furniture rearrangement or a door’s open/closed state [48] [21] [15]. 

- **Long-Term Structural Changes** (days to years): modifications to the built environment itself, e.g., renovations or seasonal layout shifts, requiring inter-session alignment and lifelong map maintenance [49] [50]. 

Table 2: Secondary axes used to characterize dynamic entities within each temporal tier. 

|**Axis**|**Category**|**Description**|
|---|---|---|
|Entity<br>Typology|Rigid<br>Articulated<br>Deformable|_SE_(3) pose change, constant ge-<br>ometry<br>Kinematic chain, constrained in-<br>ternal DoF<br>Non-rigid shape/topology change|
|State<br>Expression|Geometric-Kinematic<br>Semantic-Affordance|Position,<br>velocity,<br>boundary<br>change<br>Functional/operational<br>state<br>change|
||Topological|Connectivity change in the scene<br>graph|
|Behavioral<br>Intent|Deterministic<br>Physics-Based|Motion strictly governed by fixed<br>laws<br>Motion governed by physics-based<br>probabilities|
||Goal-Driven|Motion governed by internal deci-<br>sions or social compliance|


## **3.3 Adopted Characterization** 

This tiering is not merely descriptive: it maps directly onto the mechanism a world model must implement, from the tightly-coupled SLAMMOT formulations used for Short-Term Dynamics, through the persistence and containment reasoning used for Semi-Static Changes, to multi-session change detection used for Long-Term Structural Changes. We adopt this three-tier distinction as the primary organizing axis for the remainder of the paper. A summary is depicted in Table 1. 

## **3.2 Secondary Axes: Entity Typology and State Expression** 

Within each temporal tier, two further properties are useful for characterizing _what_ is changing and _how_ that change is expressed in the graph. Table 2 summarizes both. 

**Entity Typology** distinguishes dynamic elements by the structural assumption their motion model requires. _Rigid_ entities undergo _SE_ (3) pose change with constant geometry and dominate the surveyed factor-graph formulation [19] [51]. _Articulated_ entities are constrained by internal kinematic chains, relevant both to manipulable objects such doors and drawers [34] and to parametric human body models [52] [53]. _Deformable_ entities, whose shape or topology changes non-rigidly, remain largely outside the scope of the probabilistic graphbased systems surveyed here. 

**State Expression** distinguishes _how_ a change manifests once represented. _Geometric-kinematic_ changes are variations in position, velocity, or boundary and are the traditional target of factor graph estimation. _Semantic-affordance_ changes affect an entity’s functional or operational state, e.g., a light turning on or off, and are typically encoded as node attributes in 3D scene graphs [9] [54]. _Topological_ changes modify the connectivity of the environment itself, e.g., a closed door removing the traversable edge between two rooms, and are of particular relevance to hierarchical scene graph maintenance [9]. 

We adopt **Temporal Horizon** as the primary organizing dimension of this review, using the three tier distinction to structure this paper’s analysis. Entity Typology and State Expression are used as secondary, descriptive dimensions throughout, applied where relevant to characterize individual systems without constituting an independent organizational axis. A fourth property, _Behavioral Intent_ , that is the degree to which a dynamic entity’s future motion is deterministic, physics-based or goal-driven, is addressed by only a small subset of the reviewed literature [14] [55] and remains largely decoupled from probabilistic world-model construction. 

# **4 Graph-Based Robotic World Models For Dynamic Environments** 

The evolution of world model representation in robotics has undergone a significant paradigm shift, transitioning from rigid, static geometric maps to adaptive, spatiotemporal structure capable of handling and reasoning about dynamic environments [2] [35]. In this section, we first review factor graphs as geometric probabilistic backbones (Section 4.1.1), scene graphs as semantic abstractions (Section 4.1.2) in dynamic environments, and finally discuss how dynamics themselves are represented (Section 4.2). 

## **4.1 Representational Foundations** 

### **4.1.1 Factor Graphs as Dynamic Geometric World Models** 

To mitigate the impact of outliers and non-stationarity in dynamic environments, factor graph-based systems employ a range of probabilistic robustness mechanisms. A common approach is the use of **robust cost functions** , such as the Huber loss, which reduce the influence of large residuals during nonlinear least-squares 

7 

optimization while preserving sensitivity to small, consistent measurement errors [56]. This allows the optimizer to tolerate transient violations of the static-world assumption, caused for instance by moving objects or short-time occlusions, without destabilizing the global solution. Complementary to robust kernels, **dynamic information reweighting strategies** explicitly modulate the contribution of individual factors based on their consistency with the current state estimate [57]. Techniques such as Dynamic Covariance Scaling (DCS) or switchable constraints introduce latent scaling variables that adaptively downweight measurements whose residuals are incompatible with the inferred global structure, providing a principled outlier rejection. Beyond measurement-level robustness, more expressive models introduce **latent mobility or existence variables** associated with landmarks or objects, which explicitly encode the likelihood that an entity linked to that variable is static, movable, or currently in motion [57]. By scaling the corresponding factor covariances or relaxing constraints when mobility is inferred, these approaches prevent dynamic or semi-static entities from corrupting the static map while still allowing them to be represented within the same probabilistic framework. Together, these mechanisms transform factor graphs from purely static geometric estimators into uncertainty-aware models capable of reasoning under dynamic, partially observable conditions. Recently, many works [19] [21] [22] [17] integrated semantic priors transforming the factor graph from a purely geometric map into a context-aware reasoning engine, facilitating the coupling with other graphical models such as scene graphs. 

Traditional SLAM systems are optimized for a static world treating moving objects and agents as outliers to be rejected [13] [11]. Modern dynamic SLAM instead incorporates these dynamic entities into the graph, moving towards a coupled SLAMMOT approach that is examined in detail in Section 4.2.1. 

### **4.1.2 Scene Graphs as Structured Abstraction in Dynamic World Models** 

Dynamics in scene graphs are typically handled through three complementary mechanisms operating at different temporal and semantic levels. **Spatio-temporal consistency** is addressed by separating short-term dynamics from long-term structure: systems such as Khronos maintain a fast _active window_ to absorb immediate changes due to moving humans or objects, while a slower global process detects persistent changes and updates the long-term scene graph accordingly [15]. Beyond short-term consistency, some approaches explicitly model recurring temporal patterns. The Aion framework augments hierarchical scene graphs with _Maps of Dynamics_ (MoDs), attaching directional, time-dependent **dynamic temporal flow** statistics to navigational nodes in order to capture typical or seasonal human motion patterns, while using _Temporal Ownership Transfer_ to preserve these dynamics under loop closures and graph reorganization [14]. Finally, **belief and persistence reasoning** is used to cope with partial observability and object permanence. Be- 


Figure 4: Graphical representation of the uncertainty boundary in the hybrid layered-stack architecture. 

lief Scene Graphs introduce probabilistic _blind nodes_ to represent entities expected to exist but not currently observed, inferred from learned commonsense co-occurrence patterns [58], while interaction-driven systems such as DovSG perform localized graph updates during human–object interactions, reflecting state changes without requiring a full scene rescan [32]. 

### **4.1.3 Uncertainty Propagation, Failure Modes, Scalability** 

Uncertainty management within the factor graph is wellestablished: variables carry covariance matrices, factors encode information matrices, and the optimizer propagates uncertainty through the Hessian of the nonlinear least-squares problem [6]. The difficulty arises at the boundary: how does the uncertainty of the pose nodes in a factor graph propagate into the semantic and relational claims made by a scene graph node? In the layered-stack architecture, this propagation is largely absent, as shown in Figure 4. Scene graph nodes that are instantiated from a poorly constrained region of the pose graph carries the same confidence as one from a well constrained area. In dynamic settings, where uncertainty is generally higher and crucial for spatio-temporal estimation and prediction, this is a large drawback. Systems that adopt the unified optimizable graph architecture handle this more naturally: by representing semantic entities as factor graph variables, their uncertainty is directly encoded in the Hessian and propagates through joint optimization [11]. Recent work by Millan-Romera et al. [59] demonstrates that incorporating learned uncertainty estimates for semantic factors, rather than fixed information matrices, further improves SLAM accuracy, particularly in edge cases where semantic concepts are the only cues preserving geometric consistency. In dynamic environments the uncertainty is paramount. A poorly-constrained dynamic entity node produces an unreliable trajectory estimate that, if allowed to influence loop-closure candidates, can corrupt the static map, too [21]. Khronos [15] mitigates this by attaching explicit 4D metric uncertainty to its object fragments before they are committed to the global graph, rather than treating every instantiated node as equally confident. The broader challenge, i.e., consistent propagation of geometric and temporal uncertainty 

8 

into semantic relations, (e.g., how certain is the _on_ edge between an object and a table, given the covariance on both their pose nodes?) remains largely open and represent one of the key research gaps identified in Section 10. 

A related failure mode in dynamic environments is the corruption of higher-level scene graph abstractions by incorrect dynamic entity handling. If a moving person is incorrectly associated with a static wall node during a period of high dynamics, the resulting factor introduces a misleading constraint into the joint optimization that can displace the wall node and corrupt the room topology built on top. This cross-layer error propagation is difficult to detect and correct a posteriori, motivating the use of explicit confidence gating to prevent semantically inconsistent observation from entering the graph [60]. 

The trade-off between representational richness and real-time inference is a challenge for hybrid factor graphscene graph systems. As the environment grows, both the factor graph and the scene graph accumulate nodes and edges, and the computational cost of optimization scales with graph density. Several strategies have been developed to manage this. _Hierarchical optimization_ exploits the layered structure of scene graphs to scope optimization to the relevant subgraph: S-Graphs 2.0 [11] runs room-level local optimization continuously and floor-level global optimization only on loop closure, avoiding full re-optimization of the entire graph at each update. _Marginalization and sparsification_ are applied at the factor graph layer to maintain a bounded-size active window, with older variables marginalized into prior factors. DynoSAM [16] and its hybrid world-object centric formulation [61] use embedded-frame anchoring (Section 5.3) to preserve sparsity as dynamic object maps grow. _Task-driven graph pruning_ , detailed in Section 6.2, reduces the relational superstructure to a minimal actionable subgraph relevant to the current task, as in Clio [3] and SayPlan [4], preventing the planning complexity from growing with the full map. Together these strategies allow hybrid systems like Khronos [15] and DynEMo-SLAM [21] to achieve real-time performance in complex large indoor environments. However, the scalability of unified optimizable graphs to large-scale, highly dynamic outdoor scenes where both the agent population and the structural complexity are greater, remains an active research direction and will be discussed in more detail in Section 5.3. 

Figure 5 summarizes this hybrid architecture, showing how the factor graph backbone and scene graph superstructure connect through shared dynamic modeling and graph-maintenance stages to support downstream querying, reasoning and action. This unified representation enables actionable spatial perception, where the world model is not merely a passive map but a persistent, query-able substrate for planning, interaction, and scene prediction. 


Figure 5: Conceptual architecture of a hybrid probabilistic graph-based dynamic world model. 


Figure 6: Diagram showing the adopted dynamic distinction ontology, with each group spanning different timescale. Relevant works are reported for each, or group of, type of dynamics. 

## **4.2 Representing Dynamics in GraphBased World Models** 

The evolution of world model representations for robotics in non-stationary scenarios has progressed from treating environmental change as outlier noise toward a systematic, relational and probabilistic characterization of dynamics across multiple temporal scales [28] [15]. This section presents the most common characterization of dynamic entities in dynamic world modeling. Specifically, we emphasize the integration of factor graphs and 3DSGs to handle short-term dynamics (Section 4.2.1), semi-static changes (Section 4.2.2), and long-term structural evolution (Section 4.2.3). Figure 6 depicts the dynamic distinction we adopt, based on the type and temporal scale of expected motion, highlighting some relevant works focusing on each of them. 

### **4.2.1 Short-Term Dynamics** 

In environment populated by humans and/or moving objects, the world model must resolve the “motion ambiguity” where pixel or point displacement is a compound effect of the simultaneous robot’s ego motion and the independent motion of other entities [62]. 

9 

Early paradigms typically treated short-term dynamic entities as outliers to be masked or rejected [13] to preserve the consistency of purely static map. Contemporary loosely coupled systems often maintain these as separate threads, using the camera pose as a prior for multi object tracking (MOT) but without allowing object measurements to refine the ego-localization [63] [63] [64]. In this way, a uni-directional flow of information is generated, allowing the optimized static map data, output of the SLAM process, to enhance MOT but not the other way around. 

Modern representations employ a tightly-coupled SLAMMOT approach, where the factor graph backend jointly optimizes camera poses, static landmarks, and the trajectories of dynamic objects or agents within a unified optimization manifold [62]. Systems like DynaSLAM II [19], DynEMo-SLAM [21], SMMFSLAMMOT [62] support a tightly-coupled approach where robot poses, static landmarks, and dynamic entity trajectories are jointly optimized in a unified factor graph. This paradigm requires spatio-temporal reprojection factors to introduce cross-terms between camera poses and object motions, ensuring that the estimation of self and the surrounding is mutually beneficial. To address the computational effort of joint optimization, DynoSAM [16] and Hybrid iSAM2 [61] formulations anchor rigid body motions to “embedded frames”, preserving graph sparsity as each object map grows while enabling efficient incremental inference by a Bayes Tree. 

Humans represent a particularly important and challenging sub-class of short-term dynamics, often referred to as _dynamic agents_ : they are simultaneously the most common source of dynamics in real-world environments and the most structurally complex entity to model. This stems from the fact that humans fall into the challenging _articulated_ and _goal-driven_ categories along the typology and behavioral intent axes, respectively. Systems like Kimera [35] and Khronos [15] represent humans with dedicated node types combining 3D pose graph trajectories with non-rigid models, ensuring the world models account for both articulated motion and volumetric presence. BodySLAM [52] and its successor BodySLAM++ [53] push this further, pioneering the joint optimization of camera trajectory and dense human body shape and pose within a single factor graph, where each human observation is a parametric body model linked to the camera pose graph via reprojection factors. BodySLAM++ [53] extends this to multiple simultaneous human instances, integrating inertial factors in a real-time fashion, improving robustness to occlusion in crowded scenes. In both cases, the structured prior provided by the body model regularizes an otherwise underconstrained problem, the same role played by rigid-body kinematic priors for object-class short-term dynamics, like for instance in [51] accounting for dynamic articulated objects. 

The choice of the body model determines the degrees of freedom exposed to the optimizer and the computational costs of inference. Parametric models dominate in SLAM-integrated systems: SMPL [65] represents the body as a compact, differentiable parameter vector via linear blend skinning, making it naturally compatible 

with factor graph optimization [52] [53]. SMPL-X [66] extends this to hands and face, while STAR [67] reduces blend skinning artifacts at extreme poses. For monocular initialization without depth sensors, video-based regressors such as VIBE [68], FrankMocap [69] [70] and PromptHMR [71] provide practical SMPL estimates. At the opposite end, non-parametric approaches such as METRO [72] and neural representations such as InstantAvatar [73] offer greater shape fidelity but sacrifice the compact differentiable structure required for realtime factor graph integration. The prevailing trade-off is therefore between the structured compactness of SMPLfamily models and the expressiveness of learned representations, summarized in Table 3. 

### **4.2.2 Semi-Static Changes** 

Semi-static dynamics involve objects that are stationary during observation but relocated over time, ending up displaced in future observations [22] [21]. This requires the model to distinguish between “moving” and “movable” states. Additionally, it is needed to learn what kinds of changes a specific entity can undergo and how to handle object disappearance. 

Nodes in modern 3DSGs are annotated with dynamic attributes such as _open/closed_ or _on/off_ [54]. These properties, often inferred via Vision-Language Models [75], define _functional scene graphs_ [76] [34] where interactive elements like handles are linked to the objects they trigger, ending up to change their states. 

The key question of permanence is handled via hierarchy and containment edges (for instance an object in a drawer) [33] [32]. System like Lost & Found [33] maintain object permanence by updating these relations online. If a human hides an item in a drawer, the _contains_ edge ensures the robot _remembers_ the location despite total occlusion. 

Decisions to prune the graph are often governed by probabilistic decay rates [48] or explicit geometric verification [15]. In DPG-SLAM [49], sectors of a node are turned off if they intersect with evidence of removal. A node is marked inactive if a threshold of sectors is off, but it is only deleted if it no longer provides useful topological information, thereby managing complexity without losing historical data. 

### **4.2.3 Long-Term Structural Changes** 

Lifelong autonomy necessitates a world model that can align multiple sessions and detect structural shifts in the environment [17] [9], precluding the assumption of staticity in entities or parts of the map which would otherwise be considered unmovable in shorter or singlesession campaigns. 

At geometric level, structural change detection compares observations from different sessions to classify map regions as stable, changed or newly appeared. DPG-SLAM [49] addresses this by continuously comparing current sensor data against submaps from previous sessions. Regions where contradictions occur are marked as changed, and associated nodes are pruned. LT-mapper [50] extends this to large-scale outdoor Li- 

10 

Table 3: Comparison of human body representations relevant to robotic world modeling. ✓ = supported, × = not supported, _∼_ = partial support. RT: real-time capable. 

|**Model**|**Input**|**RT**|**Hardware**|**Traini**|**ng**|**Output**|**Body Parts**|**Realism**|**Use Case**|
|---|---|---|---|---|---|---|---|---|---|
|SMPL [65]|Shape/pose params|✓|CPU/GPU|Offline|(scan-based)|Parametric mesh|Body only|Low|SLAM, MOT, animation|
|SMPL-X [66]|Shape/pose/expr. params|_∼_|GPU|Offline|(scan-based)|Parametric mesh|Body + hands + face|Low|Expressive HRI, animation|
|STAR [67]|Shape/pose params|✓|CPU/GPU|Offline|(scan-based)|Parametric mesh|Body only|Low|SLAM, extreme pose recovery|
|Anny [74]|Phenotype params|✓|CPU/GPU|None (s|can-free)|Parametric mesh|Body + hands + face|Low|Diverse pop. modeling, HMR|
|VIBE [68]|Monocular video|_∼_|GPU|Offline|(video data)|SMPL params/frame|Body only|Low|Video-based pose init.|
|FrankMocap [69] [70]|RGB image|✓|GPU|Offline|(images)|SMPL-X params|Body + hands|Low|Real-time monocular HMR|
|METRO [72]|RGB image|×|GPU (high-end)|Offline|(images)|Raw mesh vertices|Body + hands|Medium|Accurate shape recovery|
|InstantAvatar [73]|Monocular video|×|GPU (high-end)|Per-sub|ject online|Neural field + mesh|Full body|High|Avatar reconstruction|


DAR SLAM through anchor-node-based inter-session loop factors that align drifted session pose graphs into a shared coordinate frame, applying then set-difference operations to identify positive and negative changes at keyframe level. 

Merging observations from multiple sessions into a globally consistent factor graph requires solving both the inter-session pose offset and the data association between observation of potentially changed structures. The standard mechanism is the introduction of intersession loop closure factors, i.e., constraints between nodes from different sessions that share stable landmarks [50]. Memory management is critical to keep this tractable. As shown in [77], a hierarchical shortterm/working/long-term memory structure can bound the number of loop closure candidates, enabling multisession operation under computational constraints. 

A complementary approach to multi-session alignment uses prior structural knowledge, typically in form of Building Information Models (BIM) or architectural plans, to anchor the factor graph to a known coordinate frame and constrain the estimation of structural elements. BIM-SLAM [78] models both the robot’s SLAM graph and the architectural plan as hierarchical factor graph, then detects inter-session loop closure between them. DiS-Graphs [79] extends this to jointly estimate deviations between the planned and the built environments, incorporating BIM-derived structural priors as soft constraints in the factor graph to remain accurate even when the real building deviates from its original plans. The key insight in both works lies in the hierarchical scene graph structure, e.g., walls, rooms, floors, which provides a natural alignment target that is more robust to partial scene change than point-level descriptors. The graph update policy in these systems therefore distinguishes between permanent structural entities, even in case of deviations or changes, which are retained and used for inter-session alignment, and semistatic or movable entities. 

# **5 Dynamic World Model Construction** 

Dynamic world model construction refers to the end-toend process by which raw sensor observations are transformed into a persistent, probabilistically grounded, and semantically structured representation of a nonstationary environment. In hybrid representations combining factor graphs and scene graphs, this process spans multiple tightly interacting stages, from front-end 

perception and data association to back-end inference and long-term graph maintenance. 

Rather than a monolithic pipeline, modern systems adopt modular yet interdependent components, where design choices at early stages (e.g., detection granularity or association strategy) strongly influence the stability, scalability, and expressiveness of the resulting world model under dynamics. This section organizes existing approaches around four core stages that recur across the literature: front-end perception (Section 5.1), data association (Section 5.2), back-end inference and optimization (Section 5.3), and graph maintenance (Section 5.4). A general pipeline overview is depicted in Figure 7. 

## **5.1 Front-End Perception** 

The front-end perception stage is responsible for extracting candidate entities, attributes and relations from raw sensor data. In dynamic environments, this stage must operate under partial observability, occlusion and motion ambiguity, while providing sufficiently rich primitives for downstream probabilistic inference. 

### **5.1.1 Geometric and Semantic Primitives** 

At the geometric level, front-ends extract low-level features such as points, lines, planes or surfels, which remain the backbone of factor graph-based SLAM systems [6] [35]. However, dynamic scenes increasingly require object- and agent-level primitives, motivating the integration of instance segmentation, 3D bounding volumes, or parametric object models [19] [16] [15]. 

Semantic perception pipelines typically produce: 

- **Object detections and instances** , often classlabeled and possibly open-vocabulary [32] [26]; 

- **Agent hypotheses** , including humans or vehicles, sometimes with articulated or rigid-body structure [52] [51]; 

- **Attribute estimates** , such as object state (open/close, on/off) [54]; 

- **Relation hypotheses** , e.g., spatial (on, in, nextto) or functional (controls, supports) [9] [34]. 

In hybrid FG-SG systems like Kimera [35] or Khronos [15], these outputs are deliberately redundant: dense geometric observations coexist with higher-level semantic abstraction, resulting in robustness to perception failures. 

11 

### **5.1.2 Temporal Grouping and Tracking** 

To cope with dynamics, front-ends often incorporate _short-term temporal aggregation_ , producing tracklets or object fragments prior to global optimization. Optical flow, frame-to-frame association, or local tracking modules are commonly used to stabilize detections before they enter the global world model [16] [15]. Khronos [15], for example, explicitly constructs temporally consistent object fragments ahead of the active-window integration described in Section 4.1.2, postponing commitment to the global model until sufficient evidence is accumulated. 

This early temporal coherence reduces spurious node creation and limits the combinatorial computational effort on later data association stages. 

## **5.2 Data Association** 

Data association is the process of determining which observations correspond to which existing entities in the world model, or whether they should instantiate new ones. In dynamic environments, association errors are among the primary failure reasons, as incorrect correspondences can propagate across time, capturing both geometric estimation and semantic structure. 

### **5.2.1 Deterministic and Probabilistic Association** 

Classical SLAM systems rely on deterministic association mechanisms, such as nearest-neighbor matching or Hungarian assignment based on geometric or appearance similarity [57] [64]. While efficient, these approaches degrade quickly under occlusion and fast motion. 

To address this, many dynamic-world-model systems employ _probabilistic multi-hypothesis association_ , including: 

- **Joint Probabilistic Data Association (JPDA)** , which marginalizes over multiple correspondence hypotheses [18]; 

- **Multiple Hypothesis Tracking (MHT)** , which explicitly maintains competing association trees over time [80]; 

- **Learned association** , where neural embeddings (e.g. CLIP features) define similarity metrics for object re-identification [26] [32]. 

In factor-graph formulations, association decisions are often represented implicitly via latent correspondence variables or explicitly through switchable or weighted constraints [21] [57]. 

### **5.2.2 Association under Dynamics** 

Dynamic environments needs distinguishing between moving agents, movable but stationary objects, and ephemeral observations, like transient clutter or false positives. Several works incorporate _movability or existence variables_ to mediate association decisions [22] [48]. 

From a probabilistic perspective, Random Finite Set (RFS)-based formulations (Section 5.4) provide a mechanism for handling association, birth and death jointly [81] [82], although full integration with scene graph construction remains limited. 

## **5.3 Back-End Inference/Optimization** 

The back-end integrates associated observations into a globally consistent world model, resolving the geometric, semantic and temporal constraints through probabilistic inference. 

### **5.3.1 Incremental Factor Graph Optimization** 

Most modern systems rely on _incremental smoothing_ over factor graphs, using solvers such as iSAM2 [83] or g2o [84] to maintain real-time performance under continuous updates [6] [16] [36]. Variables typically include robot poses, static landmarks, dynamic objects states, and sometimes higher-level structural entities (walls, rooms) [11]. 

Dynamic environments additionally introduce new challenges: 

- **Spatio-temporal factors** couple robot motion and object motion [16] [62]; 

- **Switchable or robust factors** downweight inconsistent measurements caused by dynamic entities [56] [57]; 

- **Motion priors** (e.g. constant velocity) regularize underconstrained trajectories [16] [21] [19]. 

### **5.3.2 Continuous Motion Modeling** 

Continuous dynamics are primarily modeled as trajectories of robot poses ( _Xk_ ) or dynamic object poses ( _Lk_ ) and motions ( _Hk_ ). Morris et al. [85] highlights a fundamental dichotomy in coordinate frame representation, presenting World-Centric and Object-Centric Formulations. Traditional object-centric models express dynamic points in a local body frame, where they appear static. However, this necessitates estimating the pose of each object at every timestep, often leading to instability because these frames are not directly observable. On the other side, world-centric representation describe rigid-body motion directly using variables in the world frame. Recent “hybrid” formulations [61] anchor motion to an embedded frame ( _Le_ ) initialized upon the first observation, which preserves factor graph sparsity and enhances convergence for incremental solvers like iSAM2. 

When it comes to the design of kinematic motion models, most frameworks adopt a constant velocity model [19] [16], to regularize the optimization problem. Some higher-fidelity models include constant acceleration [22] or specific zero velocity priors to handle humans or robots that may remain stationary for intervals of time [28]. 

These motion priors are realized in the back-end through spatio-temporal factors that couple camera 

12 

poses with object motion vertices, introducing crossterms in the Hessian matrix that improve accuracy and efficiency compared to independent spatial factors [62]. 

### **5.3.3 Loop Closure and Multi-layer Consistency** 

Loop closure remains essential for long-term consistency but is particularly risky under dynamics. Incorrect loop closures induced by moved objects or agents can catastrophically corrupt the map [21]. Systems like Khronos [15] and DPG-SLAM [49] delay or gate loop closure decisions using geometric verification and temporal consistency checks. 

In hybrid FG-SG systems, back-end inference must also ensure _cross-layer consistency_ . First, geometric optimization updates metric nodes poses. Furthermore, scene graph abstractions (e.g. room belonging and containment relations) must be updated accordingly. Unified optimizable representations, like S-Graphs [11], handle this naturally, while layered architectures require explicit synchronization policies [10] [35]. 

## **5.4 Graph Maintenance** 

Beyond inference, dynamic world models must remain computationally tractable, stable and meaningful over long time horizons. Graph maintenance governs how nodes and edges are added, updated, kept, or removed. 

The Probability Hypothesis Density (PHD) filter extends this to the multi-entity case by propagating the first-order moment of the multi-target posterior, avoiding explicit data association while jointly estimating the number and locations of dynamic entities [86]. Its application to SLAM [86] showed that modeling the landmark map as an RFS rather than a random vector provides a principled treatment of feature appearance, disappearance, missed detections and clutter within a single Bayesian recursion, and has since been applied directly to SLAMMOT [87]. This separation into a static factor graph layer and a dynamic PHD layer mirrors the architectural splits between the factor graph backbone and the dynamic node layer of hybrid FG-SG systems. 

For the full multi-entity case with explicit track management, the Poisson Multi-Bernoulli Mixture (PMBM) filter provides a Bayes-optimal conjugate prior [82]. A Poisson Point Process describes the existence of yet undetected targets, while a Multi-Bernoulli Mixture describes the distribution of already-detected targets [88]. This maps naturally onto robotic world modeling: undetected entities correspond to the PPP intensity, while confirmed tracks carry an explicit existence probability _rk_<sup>_i_updatedateachtimestep[89],withtrackpruning</sup> by thresholding [90]. The PMBM formulation has been extended directly to SLAM [91], and more recently combined with a graph-based SLAM back-end [92] to bridge RFS-based entity management with factor graph optimization. 

### **5.4.1 Node Lifecycle: Birth, Persistence, Death** 

Entity lifecycle management is central in dynamic environments. Common strategies include: 

- **Evidence accumulation thresholds** for node 

- birth [15]; 

- **Temporal decay or confidence scores** governing persistence [48]; 

- **Geometric verification** (e.g. ray tracing) to distinguish occlusion from true removal [15]. 

These heuristics can be grounded in a more principled probabilistic treatment. The Random Finite Set (RFS) framework elevates birth and death from heuristic thresholds to first-class elements of the Bayesian filtering recursion [81]. In this formulation, the set of tracked entities is itself a random variable, and existence is modeled explicitly through a binary latent variable _ϵk ∈{_ 0 _,_ 1 _}_ evolving as a first-order Markov chain with transition probabilities _pB_ (birth) and _pS_ (survival). The Bernoulli filter propagates an existence probability _rk ∈_ [0 _,_ 1] alongside the spatial density, decomposing additively into a survival term _pS · rk−_ 1 and a birth term (1 _− rk−_ 1) _· pB_ [81]. This formulation has a direct and underexplored connection to dynamic world models: each scene graph node representing a potentially transient entity, e.g. a movable chair, a walking human, a momentarily occluded object, can in principle be equipped with such an existence probability, making node lifecycle a Bayesian inference problem rather than a threshold-based engineering decision. 

The appearance rate of new entities can itself be modeled with a Poisson process of intensity _λB_ ( _·_ ) over the state space [82]; non-homogeneous variants let this birth intensity adapt over time, capturing phenomena such as increased agent density during peak hours [93]. This connects naturally to Aion’s MoD (Section 4.1.2), readable as a time-varying birth intensity learned empirically over navigational nodes rather than specified a priori. Semantic extensions such as the Semantic PHD filter [94] further augment existence estimation with class labels, bridging the RFS tracking layer and the semantic node types of scene graphs. 

Ray-tracing offers a geometric instantiation of this Bayesian update: if a ray from the robot’s current pose to a background vertex passes through a previously mapped object’s volume and returns a longer-thanexpected depth, the system confirms removal rather than occlusion [15]. Belief Scene Graphs’ blind nodes (Section 4.1.2) correspond conceptually to the PPP component of the PMBM framework, a distribution over undetected but plausible entities, though implemented via Graph Convolutional Networks rather than closedform Bayesian recursion [58]. In systems like Aion [14], motion dynamics are initially stored in a spatial hash cell and only bound to a navigational node once the local topology has stabilized (after a loop closure); if a node is removed, its temporal history is retained in the hash space for potential re-association, providing a mechanism for soft deletion analogous to track dormancy in PMBM-based trackers. 

13 

### **5.4.2 Discrete State Transition Modeling** 

Beyond continuous motion and existence, semi-static entities exhibit discrete state changes that must be captured mechanistically rather than only taxonomically. A common approach assigns latent indicator variables to each feature: _xi,t_ , whether it is currently moving, and _mi,t_ , whether it is capable of movement [22]. This allows the system to distinguish between an inherently shortterm dynamic entity and a movable object (semi-static) that happens to be static. 

Some models avoid binary classification in favor of a continuous “object probability” or “movability” score [48], capturing the likelihood of finding an object in its last known location based on long-term experience, allowing robots to learn the “rhythm” of a dynamic household. 

### **5.4.3 Structural Stability and Forgetting** 

Lifelong systems must prevent unbounded graph growth. Approaches such as DPG-SLAM [49] and Lost & Found [33] introduce **selective forgetting** , pruning nodes only when they no longer contribute topological or semantic information. Hierarchical scene graphs further localize updates, allowing changes to be absorbed at appropriate abstraction levels (object vs. room vs. floor). 

### **5.4.4 Handling Errors and Recovery** 

Incorrect associations or transient perception failures are inevitable. Robust systems therefore incorporate: 

- **Local graph repair** , updating only affected subgraphs [32]; 

- **Fragment-based representations** , isolating inconsistent observations [15]; 

- **Delayed commitment** , postponing semantic or structural decisions until sufficient confidence is reached [15], mainly to overcome data association issues. 

Graph maintenance thus acts as the final safeguard against error accumulation, ensuring that the world model remains usable for downstream tasks even under sustained dynamics. 

# **6 Interaction: Querying, Reasoning, and Action** 

The shift from static environmental representations to _actionable spatio-temporal perception_ marks a fundamental transition where the world model is no longer a passive record of geometry but an active substrate for robot reasoning and decision-making [28] [2]. The convergence of factor graphs, providing metric-semantic consistency, and (3D) scene graphs, offering hierarchical relational logic, enables a rich set of interaction modalities, encompassing multi-modal querying, hierarchical planning, and closed-loop maintenance. 


Figure 7: Per-frame operational pipeline of the hybrid world model. 

## **6.1 Multi-Modal Query Paradigms** 

The literature identifies three primary query modalities that leverage the structured nature of hybrid world models: 

**Geometric-Metric Queries:** leveraging the low-level metric semantic mesh or factor-graph-backed pose and places layers, agents execute queries for fast collision checking via Bounding Volume Hierarchies [35] and metric path planning [9], e.g. _A_<sup>_∗_</sup> or Dijkstra. 

**Symbolic-Semantic Queries:** hierarchical 3D Scene Graphs support high level symbolic commands, such as “get the medication bottle from the nightstand” [9], often assisted by LLMs to achieve long-term trajectory prediction [55]. By grounding abstract terms in specific room or object nodes, the model resolves spatial relationships, such as _on_ , _inside_ , to isolate target entities. Open-vocabulary frameworks further extend this to previously unseen categories using CLIP-based embeddings. 

**Probabilistic-Expectation Queries:** systems like Belief Scene Graphs [58] repurpose blind nodes (Section 4.1.2) to answer “what is likely present, even if unobserved”, using the same GCN-based co-occurence priors to predict object or, potentially, agent locations. 

While these three paradigms differ in representation and reasoning mechanism, Table 4 reveals a shared limitation: each is fundamentally a query over a _static_ world snapshot. Geometric-metric queries assume the underlying mesh remains valid until the next re-planning trigger; symbolic-semantic queries assume the scene graph reflects the current arrangement of entities, requiring re-detection or change-point tracking to remain accurate; and probabilistic-expectation queries model uncertainty over _unobserved_ space rather than uncertainty over _time_ , leaving moving or transient objects largely unaddressed. Bridging this gap, recent work on dynamic scene graphs and continual re-localization (e.g., [95]) begins to treat the world model itself as a temporally 

14 

evolving belief, suggesting that future query paradigms may need to fuse the spatial reasoning surveyed above with explicit temporal consistency mechanisms. 

## **6.2 Action Coupling and Hierarchical Planning** 

Interaction with the environment is increasingly handled through abstractions that trade off model fidelity for computational efficiency [95]. 

**Hierarchical and Multi-Resolution Planning** : 3D Scene Graphs enable robots to decompose complex tasks across abstraction layers. For instance, path planning can occur first at building or room level before refining to traversable place nodes, accelerating query times by several orders of magnitude compared to dense volumetric approaches [96] [97] [95] [98], and allowing for easier storage of pre-computed path when replanning is necessary [95]. 

**Task-Conditioned Subgraphs:** To manage the scale of massive environmental graphs, frameworks like _SayPlan_ [4] and _Clio_ [3] use “task-driven” abstraction. These systems interactively shrink the 3D Scene Graph by clustering and pruning nodes irrelevant to the current natural language mission, creating a minimal, actionable subgraph ready to use for the planner. 

**Control-Centric Hierarchy:** Some architectures incorporates an _Action Layer_ directly into the scene graph [99]. This layer represents candidate robot actions, such as _forward_ , _turn_ , as graph nodes connected to semantic elements, grounding affordances, and next-step reasoning within the spatial model. 

## **6.3 Dynamic Updates and Closed-Loop Consistency** 

In non-stationary environments, maintaining the accuracy of the world model requires the continuous correction of nodes and edges as the scene evolves. **Re-Perception and Credibility Loops:** Systems like SG-Nav [100] implement a re-perception mechanism that evaluates the credibility of goal candidates. If a classification is found to be ambiguous or incorrect during closer inspection, the agent dynamically adjusts the graph structure in real time. 

**Interaction-Aware Updates:** DovSG [32] and Lost&Found [33] detect hand-object contact events to update object poses and parent-child relations locally, without requiring a full-dense scene reconstruction. **Geometric Verification:** Khronos [15] applies the removal-vs-occlusion check at the interaction layer, back-propagating confirmed removals to prune stale nodes and maintain temporal consistency. 

## **6.4 Functional Interaction and ActionEffect Reasoning** 

Beyond spatial relations, recent world models explicitly encode _functional_ structure that captures how robot actions induce state changes in the environment. Functional Scene Graphs model interactive elements such as handles, switches, and control surfaces as first-class 

nodes, and represent causal dependencies through directed functional relations (e.g. _controls_ , _opens_ , _enables_ ) [34] [76]. This representation allows robots to reason about which actions are required to achieve a desired state change, effectively grounding manipulation and task planning directly in the world model. 

Crucially, functional relations are activated through interaction: they are updated when actions are executed or when human–object interactions are observed. This enables localized, semantically meaningful graph updates without requiring global re-optimization or dense scene reconstruction, as demonstrated in interactionaware systems such as DovSG [32] and Lost & Found [33]. By encoding action–effect couplings explicitly, functional scene graphs bridge symbolic task reasoning and geometric execution, providing a structured model for multi-step manipulation and interaction in dynamic environments. 

# **7 Applications** 

The dynamic world models presented throughout this paper are not limited in their generation, but their value is realized through the downstream tasks they can enable. The shift from static, geometric maps to hybrid probabilistic graph representations that jointly handle geometry, semantics and temporal changes unlocks a richer set of robotic capabilities. This section organizes these applications around four themes that progress from self-localization to high-level reasoning: robust SLAM and consistent world modeling under dynamics (Section 7.1), multi-object tracking and interaction understanding (Section 7.2), navigation and hierarchical planning (Section 7.3), scene understanding, memory and long-term retrieval (Section 7.4). 

## **7.1 Robust SLAM and Consistent World Modeling under Dynamics** 

The most immediate application of dynamic world models is improving the robustness of self-localization and map building and updating when the environment contains moving or movable entities. In static-world SLAM, dynamic elements degrade trajectory estimation through incorrect data associations and inconsistent landmark observations, leading to the standard approach of outlier rejection but ending up discarding information that a richer model could exploit. Tightlycoupled systems such as DynaSLAM II [19], DynoSAM [16], BodySLAM++ [53] and AirDOS [51] demonstrate that the joint-optimization formulation introduced in Section 4.2.1 improves ego-trajectory accuracy compared to outlier-rejection baselines, since the cross-terms make self-localization and dynamic-entity tracking mutually reinforcing. DynEMo-SLAM [21] applies this formulation in practice, allowing the SLAM back-end to benefit from semantic priors on entity motion while producing a richer joint world model. 

The world model also needs to remain consistent across sessions and under long-term changes. Khronos [15] applies the spatio-temporal mechanisms described 

15 

Table 4: Comparison of the three query paradigms over hybrid world models. 

|**Dimension**|**Geometric-Metric**|**Symboli**|**c-Semantic**||**Probab**|**ilistic-Expectation**|
|---|---|---|---|---|---|---|
|Representation|Metric-semantic mesh, factor-graph pose<br>layers, occupancy/TSDF volumes|Hierarchi<br>(room/o|cal<br>3D<br>scene<br>bject/relation nodes)|graph|Scene gr<br>_nodes_ a|aph augmented with latent _blind_<br>nd learned priors|
|Core question|Is this space free? What is the shortest<br>path from A to B?|Where is<br>tion _R_ to|object X? What satisi<br> _Y_?|fies rela-|What is<br>served?|_likely_ present, even if unob-|
|Typical methods|BVH collision checks [35], _A_<sup>_∗_</sup>, Dijkstra,<br>RRT*, ESDF planners|Graph<br>grounded<br>tion [55]<br>retrieval|traversal/matching,<br><br>language-to-node<br>, CLIP-based open-vo|LLM-<br>resolu-<br>cabulary|GCNs,<br>Bayesian|learned<br>co-occurrence<br>priors,<br> belief updates [58]|
|Granularity|Fine-grained, continuous/metric|Discrete,|categorical, relational||Discrete<br>unobser|, but probability-weighted over<br>ved nodes|
|Failure modes|Degrades under sensor noise/incomplete<br>reconstruction; costly at scale without<br>hierarchical pruning|Sensitive <br>novel cat<br>port|to grounding errors; b<br>egories without open-vo|rittle to<br>cab sup-|Priors c<br>node coi|an encode dataset bias; blind-<br>nfidence is hard to calibrate|
|Role of dynamics|Assumes quasi-static mesh; requires re-<br>planning triggers on change|Assumes <br>updates|static graph; needs inc<br>from re-detection|remental|Models<br>not tem|unobserved-space<br>uncertainty,<br>poral/moving-object uncertainty|


in Section 4.1.2 and 5.4 at system scale, demonstrating that the same active-window/global-process split supports lifelong operation across extended deployments. Systems like DPG-SLAM [49] implement explicit forgetting policies, pruning nodes only when they no longer contribute topological information, thereby managing graph complexity without losing historical data. These mechanisms are essential for robots operating across extended deployment horizons, such as warehouses, offices, and hospitals, where the entity population changes between sessions, and represent a direct application of the probabilistic birth-death modeling discussed in Section 5.4. 

## **7.2 Multi-Object Tracking and Interaction Understanding** 

Beyond robust self-localization, dynamic world models serve as the substrate for understanding the agents and objects that populate the environment. In tightlycoupled SLAMMOT paradigm, the factor graph backend estimates object trajectories jointly with the robot pose, providing smoothed, geometrically consistent tracks that outperform pure MOT systems which cannot benefit their estimates from a broader scene understanding. DynoSAM [16], BodySLAM [52] and AirDOS [51] generate 4D spatio-temporal maps of dynamic objects and agents as an output of their unified optimization, enabling downstream tasks such as trajectory prediction and collision forecasting. 

For human agents specifically, BodySLAM [52] and BodySLAM++ [53] recover full SMPL body shape and pose jointly with camera trajectory (Section 4.2.1), producing a world model that captures postural state directly relevant to human-robot interaction and intention prediction. The structured prior provided by the parametric body model acts as a strong regularizer that improves both the human pose estimate and the camera trajectory, particularly in scenes where humans occlude most of the field of view and purely geometric features tracking fails. At the level of intentions and trajectories, Gorlo et al. [55] use the temporal structure of 3D dynamic scene graph, e.g. recognizing that a person moving toward a doorway is likely to exit, rather than relying solely on kinematic history. Aion [14] extends this predictive capability to activity forecasting, building a 

model of human rhythms that lets the robot anticipate congestion before it occurs. 

Scene graphs enrich this tracking with semantic understanding of interactions, like Lost & Found [33] and its human-object interactions triggering updates at graph edge level, effectively building a running causal system for tracking how the scene has changed due to human activity without requiring a full scene reconstruction after each interaction. 

## **7.3 Navigation and Hierarchical Planning** 

Dynamic world models directly inform navigation and planning by providing structured, multi-resolution representations that support both metric path execution and high-level task decomposition. The hierarchical layers of 3D scene graphs allows planners to operate appropriate level of abstraction for the current task, consistently reducing computation compared to planning over dense volumetric maps [98] [97]. Ejaz et al. [95] demonstrate this computation efficiency through situationallyaware path planning over 3D scene graphs, using the relational structure of the graph to select traversal sequences that account for both metric cost and semantic context. 

The key advantage of advantage of factor graphbacked scene graph in this context is geometric consistency: because the scene graph nodes are grounded in a factor graph optimization, the metric positions used by the path planner are globally consistent and uncertainty-aware, avoiding the drift that would otherwise accumulate during long navigation tasks. SayPlan [4] and Clio [3] apply the task-driven pruning described in Section 6.2 to reduce planning complexity by orders of magnitude in large environments. 

In dynamic environments, however, static planning assumptions break down: a path computed over the current scene graph may become infeasible as agents move, objects are displaced, or passageways are shut. The connection between the factor graph dynamics layer and the planning layer remains largely open. Current systems either replan from scratch on graph updates or maintain pre-computed paths that are invalidated when dynamic nodes change [95], a limitation that Aion’s predictive 

16 

flow statistics (Section 4.1.2) begin to address by routing around congestion proactively [14]. 

## **7.4 Scene Understanding, Memory, and Long-Term Retrieval** 

The fourth identified application area treats the dynamic world model as a persistent, queryable memory that supports object retrieval, semantic localization and long-term scene understanding. DovSG [32] demonstrates this for mobile manipulation, where the open-vocabulary 3D scene graph serves as the robot’s persistent object memory, supporting natural language queries for object retrieval even after objects have been displaced by human interaction. 

Belief Scene Graphs [58] extend this memory to unobserved regions, transforming the world model from reactive record into a predictive spatial memory that can guide active exploration under partial observability. 

Across all four application areas, the common thread is that the dynamic world model serves an active layer, not a passive geometric record but a probabilistically maintained, semantically structured representation that simultaneously supports estimation, prediction, planning and interaction. These works demonstrate that hybrid factor graph-scene graph representations are uniquely positioned to provide this layer, suggesting that hybrid representations can enable downstream applications that are difficult to achieve with either paradigm in isolation. 

# **8 Evaluation Protocols, Datasets and Metrics** 

## **8.1 Protocols** 

A thorough analysis of the evaluation protocols reveals a rigorous methodological framework designed to validate the robustness of world models against non-stationary environments. These protocols go beyond traditional SLAM metrics, including stochastic analysis, longitudinal studies and modular ablations to isolate the effect of various architectural components. Moreover, research in dynamic SLAM has shifted towards validating the efficacy of the system in and for specific use cases. 

### **8.1.1 Per-Sequence and Multi-Run Evaluation** 

To address the inherent non-determinism in multithreaded systems and the randomness introduced by dynamic entities, researchers employ a protocol of repeated trials: 

- **Per-Sequence Analysis** : Results are almost universally reported on a per-sequence basis to account for varying environmental conditions as traffic density and feature availability [63] [21] [62]. 

- **Stochasticity Management** : To mitigate the impact of random initialization in particle filters or the 

non-deterministic nature of multi-threaded optimization, experiments are executed multiple times. Standard protocols include running each sequence multiple times and reporting the median value [62] or average [125]. Other collaborative frameworks report mean and standard deviation over several randomly initialized runs to quantify stability [29]. 

### **8.1.2 Dynamic Severity Sweeps** 

Evaluation protocols frequently involve sweeping through levels of environmental complexity to test the limits of dynamic robustness. 

- **Entity Density Scalability** : The uHumans and uHumans2 datasets are used to evaluate how spatial perception engines handle environments with increasing numbers of dynamic entities, ranging from 12 to 60 human agents [28]. Similar approaches are partaken when the dynamics in the scene are displaced objects rather than continuously moving humans [126]. Also self-collected datasets are generated accounting for different progressive levels, densities and complexities of dynamic entities populating the scene [21]. 

- **Dynamic Entity Types** : Taking into account that different kinds of dynamics can occur in the scene, e.g. persistently moving agents and occasionally displaced objects, the systems’ generalization capabilities are often evaluated testing for subsets or different configurations of possible dynamics occurring in the scene [21]. 

- **Clutter and Deviation Levels** : In BIM-based localization, scenarios are designed to progressively increase the level of clutter, thereby decreasing the overlap with permanent building objects [78] [79]. 

- **Controlled Configuration Sweeps** : Navigation models are tested against varying obstacles configurations to ensure that learned policies generalize across different collision trajectories [129]. 

### **8.1.3 Relocalization Dropouts and Success Rate** 

The robustness of the world model is tested through its ability to recover from tracking loss, particularly when dynamic occlusion causes feature dropouts. 

- **Sequential Retrieval Tests** : Systems are evaluated by sequentially feeding data from different session and counting the number of successful against unsuccessful relocalization events [109]. 

- **Convergence Metrics** : Success is often defined by a threshold-based protocol, where a method is deemed to have converged if the pose estimate, either of the exploring robot’s trajectories or detected entities, stabilizes within a specific distance of the ground truth within a set percentage of the sequence length [78] [85]. 

17 

Table 5: Public Datasets and Benchmarks for Dynamic SLAM and Object Tracking 

|**Dataset**|**Key Features**|**Environment**|**Dynamics**|**Use Case**|**Sensors**|**Used In**|
|---|---|---|---|---|---|---|
|||**I. Public Outd**|**oor and Urban Drivi**|**ng Benchmarks**|||
|KITTI<br>Track-<br>ing/Odometry<br>[101]|Grayscale<br>and<br>RGB stereo, GPS,<br>IMU,<br>3D<br>LiDAR<br>(Velodyne<br>HDL-<br>64E)|Urban/Highway|Vehicles, pedestri-<br>ans|High-speed<br>dy-<br>namics,<br>ego-<br>motion ambiguity|GPS, IMU, 3D Li-<br>DAR, Camera|[19], [22], [85], [63],<br>[102]|
|nuScenes [103]|3D<br>MOT<br>(AMOTA),<br>urban<br>LiDARdetections|Urban|High traffic density|Multi-object track-<br>ing, accuracy eval-<br>uation|LiDAR, Camera|[80]|
|Virtual<br>KITTI<br>[104]|<br>Synthetic,<br>photo-<br>realistic,<br>ground<br>truth<br>cam-<br>|Urban/Highway|Vehicles, pedestri-<br>ans|Depth error isola-<br>tion,<br>object<br>seg-<br>mentation|Camera,|[105]|
|Victoria Park [106]|era/object poses<br>2D<br>odometry,<br>landmark<br>obser-<br>vations<br>(trees),<br>simulated<br>north-<br>wardmovement|Urban|Corrupted<br>land-<br>marks|Solver<br>divergence,<br>robustness testing|Laser, GPS|[57]|
|Alcazar of Seville<br>[107]|<br>Visual-stereo,<br>dy-<br>namic pedestrians|Indoor/Outdoor|Pedestrian dynam-<br>ics|Re-localization,<br>landmark stability|Laser, RGB|[57]|
|||**II. Public Indo**|**or and Semantic Ma**|**pping Datasets**|||
|OpenLORIS-<br>Scene [108]|Office<br>and<br>super-<br>market<br>environ-<br>ments,<br>lifelong<br>SLAM|Indoor|Pedestrian<br>occlu-<br>sion, scene changes|Long-term SLAM,<br>furniture<br>reloca-<br>tion|RGB-D,<br>Semantic<br>Labels|[109], [110]|
|ScanNet [111]|1500+<br>RGB-D<br>sequences,<br>indoor<br>spaces|Indoor|Static and dynamic<br>objects|3D<br>scene<br>graph<br>construction,<br>ob-<br>ject<br>relationships<br>&reconstruction|RGB-D,<br>Semantic<br>Labels|[31]|
|Matterport3D<br>[112]|35<br>semantic<br>classes,<br>residen-<br>tial/commercial<br>|Indoor|Room layouts, ob-<br>jects|<br>Learning<br>co-<br>occurrence, spatial<br>distribution|RGB-D, 3D Mod-<br>els|[58]|
|TUM RGB-D [113]|spaces<br>Office<br>sequences,<br>Kinect<br>sensors,<br>Vicon motion cap-<br>t|Indoor|Walking,<br>desk<br>movements|High/Low dynam-<br>ics, object tracking|RGB-D,<br>Motion<br>Capture|[109]|
|Bonn RGB-D Dy-<br>namic [114]|ure<br>Moving<br>people<br>interacting<br>with<br>movingobjects|Indoor|Humans, Objects|Multi-object track-<br>ing<br>Scene<br>recon-<br>struction|RGB-D|[115]|
|Oxford<br>Multi-<br>motion<br>Dataset<br>|<br>Swinging<br>cubes,<br>unconstrained|Indoor|Non-planar,<br>fast-<br>moving objects|Challenging<br>dy-<br>namic tracking|Stereo,<br>RGB-D,<br>IMU,<br>Vicon<br>mo-|[64], [85], [16]|
|(OMD) [116]|motion<br>**III**|**. Synthetic and **|**Semi-Synthetic Envi**|**ronment Simulato**|tion capture<br>**rs**||
|TESSE<br>Simulator<br>[117]|Short-term<br>dy-<br>namics,<br>long-term<br>changes,<br>precise<br>dtth|Indoor|Walking, bouncing<br>balls,<br>furniture<br>changes|Controlled<br>abla-<br>tion studies|RGB, Depth|[15]|
|VirtualHome [118]|groun ru<br>Object movements<br>in household rou-<br>ti50d|Indoor|Object<br>movement<br>in<br>routine<br>activi-<br>ti|Object<br>tracking,<br>daily activities|RGB|[119]|
|CARLA Simulator<br>[120]|nes, + ays<br>Urban<br>scene<br>graph partitioning,<br>weather dynamics|Urban|es<br>Traffic, pedestrian<br>dynamics|Scene<br>graph<br>par-<br>titioning, dynamic<br>environments|Camera, LiDAR|[29]|
|Dynamic<br>House<br>Simulator / iGrid-<br>son [121]|Household<br>dy-<br>namic<br>objects,<br>movement between|Indoor|Object movement,<br>probabilistic<br>dy-<br>namics|Link<br>prediction,<br>dynamic<br>environ-<br>ments|RGB|[121]|
||furniture|**IV. Specialized **|**Benchmarks and Sel**|**f-Collected Data**|||
|VIODE [122]|UAV-based visual-<br>inertial<br>odometry,<br>extreme<br>motions,<br>li|Outdoor|UAV<br>in<br>park-<br>ing<br>lot,<br>dynamic<br>agents|Real-time<br>update,<br>occlusion handling|Synthetic<br>ground<br>truth|[16]|
|TartanAir Shibuya<br>[123]|occuson<br>30+ humans, dense<br>urban crossing|Urban|Non-rigid, crowded<br>scenes|Robustness<br>in<br>crowded<br>environ-<br>|Ground<br>truth<br>poses|[16] [51]|
|uHumans/uHumans<br>[35]|2<br>Unity-based simu-<br>lator,<br>12-60<br>hu-<br>man agents, SMPL<br>h|Indoor/Outdoor|Dense<br>human<br>tracking|ments<br>Human<br>interac-<br>tion,<br>dynamic<br>tracking|Ground<br>truth<br>poses|[35]|
|FunGraph3D [34]|meses<br>iPad<br>Pro<br>video,<br>high-fidelity<br>laser<br>scans,<br>Apple<br>Vi-<br>|Indoor/Outdoor|Functional<br>rela-<br>tionships<br>(e.g.,<br>switches)|Functional annota-<br>tion,<br>relationship<br>tracking|Functional annota-<br>tions|[34]|
|OC-NaVQA [124]|sion Pro<br>Object-centric<br>NaVQA,<br>spatio-<br>temporal Q&A|Indoor/Outdoor|Static and dynamic<br>environments|Question<br>an-<br>swering,<br>memory<br>sequences|Ground<br>truth<br>Q&A labels|[124]|
|Husky/Spot<br>Field<br>Tests|Real<br>university<br>halls/offices,<br>Li-<br>DAR and RGB-D<br>sensors|Indoor|Dynamic<br>agents<br>(robots,<br>pedes-<br>trians),<br>dynamic<br>objects<br>18|Real-time<br>perfor-<br>mance validation|LiDAR, RGB-D|[15], [21]|


Table 6: Metric catalog for dynamic SLAM (FG) and scene graph (SG) evaluation. Use as a checklist and to standardize naming across encountered works. 

|**Metric**|**Type**|**What it measures / notes**|**Used in**|
|---|---|---|---|
|**ATE (RMSE/median)**|Trajectory|Absolute<br>trajectory<br>error<br>vs<br>ground<br>truth;<br>re-<br>port<br>RMSE<br>+<br>median,<br>and<br>whether<br>aligned<br>SE3Si3|[...]|
|**RPE (**∆_t_ **/** ∆_s_**)**|Trajectory|(()/m()).<br>Relative pose error; clarifies short-term drift; specify<br>interval|[...]|
|**Drift (m/100m, deg/100m)**|Trajectory|.<br>Aggregate drift over distance; common in automo-<br>tivedatasets|[35]|
|**Relocalization success rate**|Trajectory|.<br>Fraction of trials where tracking is recovered after<br>dt/li|[78] [109]|
|**CS-R (Correctness Score of Re-Localization)**|Trajectory|ropouoccuson.<br>Reliability<br>of<br>re-localization<br>events<br>in<br>dynamic<br>scenes; typically validates that a declared relocal-<br>izationiscorrect(notafalseositive)|[109]|
|**Failure rate / time-to-failure**|System|p.<br>Robustness under dynamics; define failure criterion<br>(e.g. lost tracking _>_ N frames).|[125]|
|**Runtime (Hz/FPS), latency (ms)**|System|Throughput and per-module latency; note hardware<br><br>[|33] [19] [15]|
|**CPU/GPU, memory footprint**|System|and whether real-time.<br>Resource profile for deployability comparisons.|[126]|
|**Point cloud Accuracy and Completeness / ICP residual**|Map|Geometric<br>map<br>quality<br>vs<br>reference<br>(dense<br>h|[35] [32]|
|Map IoU (occupancy)|Map|scan/mes).<br>Overlap between predicted and GT occupancy grids;<br>specify resolution and thresholding.|[35]|
|**TP rate (2D / BEV / 3D)**|Map|True positive rate for occupancy estimation across<br>viewpoints/representations; report the correspond-<br>ingFP/FNdefinitions|[62] [19]|
|**SCDA (Scene Change Detection Accuracy)**|Change|i.<br>Accuracy of detecting voxel-level or object-level<br>changes over time;<br>clarify temporal window and<br>whetherclass-conditioned|[32]|
|**Completeness / accuracy**|Map|.<br>Surface coverage or distance-to-surface statistics (of-<br>ten pairs).|[35]|
|**Mask IoU / mIoU**|Semantics|Segmentation quality for dynamic masking or seman-<br>ilbl|[35]|
|**Precision/Recall/F1 (objects)**|Semantics|tc aes.<br>Detection/instance metrics; specify IoU threshold<br>(e05)|[15]|
|**Motion Error (ME)**|Motion|.g. ..<br>Frame-agnostic object motion error evaluated in the<br>ground-truth object frame; helps compare methods<br>using different reference frame conventions.|[16] [61]|
|**MOTA / AMOTA / MOTP**|Tracking|Classic multi-object tracking metrics (association +<br>localization); sensitive to thresholds and missed de-<br>i<br>[<br>[|64] [63] [80]<br>62] [64] [19]|
|**ID Switches**<br>**Fragments (track fragmentation)**|Tracking<br>Tracking|tectons.<br>Counts identity swaps in tracking; lower is better.<br>Counts interruptions/splits in a trajectory; measures<br>tiitftk|[62] [80]<br>[62]|
|**IDF1**|Tracking|connuy o racs.<br>Identity-based F1; balances correct associations over<br>time.|[62]|
|**Node Precision/Recall/F1**|Graph|Correctness<br>of<br>entity<br>discovery<br>(rooms/walls/objects)<br>in<br>scene<br>graphs;<br>depends<br>on<br>matching<br>policy<br>between<br>predicted<br>and<br>GT<br>d|[34] [126]|
|**Edge Precision/Recall/F1 / edge prediction/accuracy**|Graph|noes.<br>Correctness of predicted relations (adjacent-to, in-<br>room, supports, etc.); report relation set and match-<br>inrules|[34]|
|**Spurious & Missing Entities**|Graph|g .<br>Human-judgment metric counting incorrect (spuri-<br>ous) or omitted (missing) nodes/edges in constructed<br>SGs|[31]|
|**Precision/Recall of scene parsing**|Parsing|.<br>Accuracy of partitioning places into rooms or higher-<br>level structures (often computed from segmentation<br>orreionadjacenc)|[28] [127]|
|**Graph Edit Distance (GED)**|Graph|g y.<br>Structural<br>similarity<br>to<br>GT<br>graph;<br>sensitive<br>to<br>node/edgelabelsandmatching|[55]|
|**Temporal stability / churn**|Graph-time|.<br>Persistence of nodes/edges over time (e.g., addi-<br>tions/deletions per minute, or lifetime distributions).|[14]|
|**NDCG (Normalized Discounted Cumulative Gain)**|Ranking|Quality of predicted rankings (e.g., likelihood-ranked<br>object locations); requires relevance labels and a cut-<br>off _K_.|[121]|
|**NEES /** _χ_<sup>2</sup> **consistency**|Prob. (FG)|Consistency of estimated uncertainty;<br>important<br>when works claim probabilistic reliability.|[85]|
|**Descriptive question accuracy (SQA)**|Reasoning|Accuracy on spatio-temporal question answering us-<br>|[124]|
|**ADE (Avg. Displacement Error)**|Prediction|ing 4D/temporal scene graphs.<br>Average distance between predicted and GT trajec-<br>|[55]|
|**BoN ADE (Best-of-N ADE)**|Prediction|tories (e.g., human motion).<br>Minimum ADE over _N_ sampled predictions; mea-<br>|[55]|
|**Task success rate**|Task|sures multi-modal forecasting quality.<br>Completion rate of robot tasks informed by the world<br>model (e.g., pick-and-place); specify task definition<br>andfailuremodes|[32]|
|**BLEU / METEOR / BERTScore**|Language|.<br>Similarity of generated textual SG annotations to<br>references; report whether multiple references are<br>used and tokenization details.|[128]|


19 

- **Initialization and Hand-off** : Some protocols evaluate the efficiency of switching from stochastic global localizer to a precise graph-based localization algorithm once a covariance threshold is met [125]. 

- **8.1.4 Multi-Session and Long-Term Change Protocols** 

Lifelong autonomy is validated though longitudinal data collection and multi-pass traversal. 

- **Long-Term Monitoring** : Systems are evaluated on their ability to update object probabilities across extensive periods [48] [119]. 

- **Incremental Pass Validation** : Protocols include repeated traversals of the same environment to determine if the model can successfully “forget” ephemeral data and identify static static structural components [49]. 

- **Consecutive Task Execution** : Robots are tested on their ability to complete consecutive manipulation tasks without manual resets, ensuring the updated 3D scene graph remains actionable after manual modification of the environment [32]. 

### **8.1.5 Systematic Ablation Studies** 

Ablation protocols are essential for isolating the contribution of proposed factors, modules and policies. 

- **Dynamic Filtering Modules** : Protocols isolate the dynamic entities or features removal module to identify the best trade-off for loop closure quality [21]. 

- **Scene Graph Update Policies** : Researchers ablate the logic used for graph maintenance, such as the effectiveness of _sequential reasoning_ in functional graphs [34] or the utility of _region clustering_ and _frame selection heuristics_ [124] or _keyframe selection policies_ [21] in 4D scene graph generation. 

- **Factor-Level Ablations** : In tightly-coupled systems, models are evaluated with and without specific constraints, such as _non-rigid factors_ for humans or _rigid factors_ for objects, to verify their individual contributions to trajectory accuracy and world model generation [21] [110]. 

## **8.2 Datasets** 

The evaluation of hybrid world models, integrating scene graphs and/or factor graphs, and spatio-temporal dynamics, relies on a hierarchical selection of commonly employed datasets ranging from established autonomous driving benchmarks to specialized indoor semantic simulator. Additionally, to assess the system behavior on specific situations, self-collected datasets presenting peculiar kinds of environments and dynamics are created, either in real world or simulation. These datasets can be categorized by their environmental focus, sensor suites, and the specific nature of the dynamics they encapsulate. Table 5 reports the most commonly used publicly available datasets, benchmarks and simulators. 

## **8.3 Metrics** 

The metrics employed to assess any proposed method depend on the downstream use of it and its tackled problem. When it comes to the evaluation of GMs, either factor graphs or scene graphs, specifically developed for dynamic environments, the attention is focused on assessing the systems performance on different levels: the robot/self trajectory, the map geometry, the semantics detection and segmentation, the graph structure, the system performance in terms of runtime and memory usage, and the probabilistic consistency of the graph. Additionally, when SGs are exploited or augmented with the employment of LLM methods for task accomplishment, capabilities like language semantic reasoning and downstream task success are evaluated. Table 6 reports the most commonly used metric in these scenarios. 

# **9 Comparative Analysis of Representative Systems** 

The literature on world modeling in dynamic environments spans a wide range of representational choices, inference strategies and application targets. While individual systems are often described in isolation, a comparative perspective is necessary to understand how these design decisions relate to one another and how different combinations of graphical models, dynamic handling, and uncertainty treatments emerge in practice. This section provides a structured comparison of the surveyed _systems_ themselves, classifying graph-based dynamic world models for robotics along a set of common axes. Rather than ranking methods by performance, the comparison aims to map the design space, highlighting recurring architectural patterns and characteristic trade-offs across factor-graph-based, scenegraph-based and hybrid representations. 

## **9.1 Axes of Comparison** 

The analysis organizes existing approaches along several dimensions that recur throughout the surveyed literature: 

- **Graph Stack** : the primary representational backbone employed by the system, distinguishing between factor graphs (FG), scene graph (SG), and hybrid architectures in which the two are explicitly coupled; 

- **Dynamics Type** : the class of environmental change modeled, using the same three-tier Temporal Horizon distinction introduced in Section 3 (short-term dynamics, semi-static changes, and long-term structural evolution); 

- **Represented Scene** : the operational context, such as indoor, outdoor, or any environment; 

- **Data Association Strategy** : the mechanism used to link observations over time, ranging from deterministic matching to probabilistic multihypothesis methods or learned similarity models; 

20 

- **Inference Policy** : the underlying inference method, including batch maximum a posteriori (MAP) optimization, incremental smoothing, filtering-based approaches, or variational inference; 

- **Uncertainty Treatment** : whether uncertainty is modeled explicitly in a probabilistic sense or handled through heuristic confidence measures; 

- **Sensor** : the employed sensing inputs used to build the world model; 

- **System Properties** : practical characteristics such as real-time capability, open-vocabulary support, and multi-robot operation. 

- **Downstream Usage** : the primary tasks specifically enabled or targeted by the representation, such as robust SLAM, navigation, manipulation, interaction understanding, or prediction. 

These axes stem from the three research questions posed in Section 1: Graph Stack, Dynamics Type, and Represented Scene characterize _what is represented_ (RQ1); Data Association Strategy, Inference Policy, Uncertainty Treatment, and Sensor characterize _how the representation is constructed and maintained_ (RQ2); and System Properties, and Downstream Usage characterize _how the representation is exploited_ (RQ3). Together, these axes provide a unified lens through which heterogeneous systems can be compared across all three questions simultaneously, without assuming a notion of optimality. 

## **9.2 Comparison of Existing Approaches** 

Table 7 summarizes representative works in the literature according to the comparison dimensions defined above. The listed systems are grouped by their underlying graph stack, enabling a direct comparison between factor-graph-based methods, scene-graph-centric approaches, and hybrid representations that integrate probabilistic estimation with semantic abstraction. 

The table illustrates the variety of design choices explored, from tightly-coupled SLAMMOT systems that extend classical factor graphs with dynamic entity modeling, to scene-graph-based frameworks emphasizing semantic structure and interaction, finally to hybrid systems that combine geometric consistency with relational reasoning. 

## **9.3 Cross-Comparison** 

Across the surveyed works, four recurring architectural patterns emerge, showed in Figure 8, distinguished primarily by which graph stack a system commits to and, for hybrid systems, how tightly the two stacks are coupled. Two patterns rely on a single representational backbone, factor graphs alone or scene graphs alone, while two combine both, differing in whether information flows in one direction or both. 


Figure 8: Four distinct architectures have emerged throughout the literature for representing dynamic environment, specifically _factor graph-centric_ (top left), _scene graphcentric_ (bottom right), _hybrid - loosely coupled_ (top right) and _hybrid - tightly-coupled_ (bottom left). 

**Tightly-Coupled SLAMMOT (FG-centric)** Systems in this pattern, like DynaSLAM II [19], DynoSAM [16], AirDOS [51], BodySLAM [52], BodySLAM++ [53], Gou et al. [64], adopt the joint-optimization approach detailed in Section 4.2.1, treating dynamic entities as first-class factor graph variables rather than outliers.The trade-off is that this template primarily addresses continuously moving agents, while semi-static displacement and lifelong structural changes are typically outside its scope, and no explicit semantic abstraction layer is provided for higher-level reasoning tasks. 

**Layered Stack with FG Backbone (Hybrid, loosely coupled)** Kimera [35] and Hydra [10] exemplify a layered architecture in which a factor graph optimizer provides a globally consistent geometric foundation, while a separate scene graph parser constructs the semantic-relational superstructure. The advantage is modularity: the scene graph logic can be developed independently of the SLAM back-end. The disadvantage is one-directional information flow: the scene graph is informed by the factor graph, but semantic information rarely propagates back to improve localization, so geometric uncertainty never reaches the semantic layer. 

**Unified Optimizable Graph (Hybrid, tightlycoupled)** S-Graphs [11] and DynEMo-SLAM [21] incorporate semantic entities directly as variables and factors within the same factor graph that optimizes robot poses. This enables bidirectional information flow: semantic structural priors constrain ego-trajectory estimation, while geometric observations refine semantic entity states. DynEMo-SLAM extends this template to dynamic entities by constraining entity pose variables with semantic motion priors and structural relations. 

21 

Table 7: Comparative analysis of representative probabilistic graph-based _systems_ for robotics in dynamic environments. 

|**Work**|**Grap**<br>**stack**|**h**<br>**Nodes**|**Representati**<br>**Edges**|**on**<br>**Dynamics**<br>**type**|**Rep-**<br>**re-**<br>**sented**<br>**scene**|**Cons**<br>**Associa-**<br>**tion**|**truction & **<br>**Inference**|**Maintenan**<br>**Uncer-**<br>**tainty**|**ce**<br>**Sen-**<br>**sors**|**Exp**<br>**RT OVM**|**loitation**<br>**R**<br>**Downstream**<br>**use**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||_Fa_|_ctor gra_|_ph (FG) only_||||||
|DynaSLAM II<br>Bescos et al.<br>(2021) [19]|FG|Camera pose,<br>object pose,<br>velocity,<br>points|reprojection<br>error,<br>motion error|short-term ✓<br>semi-static ✗<br>lifelong ✗|Out-<br>door|determinis-<br>tic<br>(ORB +<br>IoU)|batch<br>MAP|explicit<br>covariances|Stereo<br>or<br>RGB-D|✓<br>✗<br>✗|Collision<br>avoidance<br>+ SLAMMOT|
|Brink<br>(2016) [22]|FG|Image fea-<br>tures,<br>velocity|same-object<br>probabilistic<br>dependency|short-term ✓<br>semi-static ✓<br>lifelong ✗|Any|determinis-<br>tic<br>(Delaunay<br>triangulation|)<br>incremental<br>loopy BP|explicit<br>Gaussian|Stereo|✗<br>✗<br>✗|Dynamic<br>object<br>detection|
|DynoSAM<br>Morris et al.<br>(2025) [16]|FG|Camera<br>poses,<br>object<br>motions/pose<br>map points|s,<br>point meas.,<br>odometry,<br>object mo-<br>tion,<br>obj. smooth-<br>ing,<br>prior factors|short-term ✓<br>semi-static ✗<br>lifelong ✗|Any|optical flow<br>+ instance<br>seg.|incremental<br>smoothing|explicit<br>covariances|RGB-D|✓<br>✗<br>✗|4D dynamic<br>reconstruction|
|Gou et al.<br>(2024) [64]|FG|Camera<br>poses,<br>landmarks,<br>objects|static re-<br>proj.,<br>camera<br>meas.,<br>dynamic<br>reproj.,<br>object mo-<br>tion|short-term ✓<br>semi-static ✗<br>lifelong ✗|Any|Hungarian<br>algorithm|local/global<br>BA|explicit<br>Gaussian|RGB-D|✓<br>✗<br>✗|Industrial<br>inspection|
|Gomez et al.<br>(2020) [48]|FG|Poses,<br>objects<br>(cuboid<br>centroids)|Geometric<br>spatial<br>relations|short-term ✗<br>semi-static ✓<br>lifelong ✗|Any|area of<br>influence|multi-<br>session<br>adaptation|explicit<br>prob. pres-<br>ence|RGB-D|✓<br>✗<br>✗|Autonomous<br>indoor<br>service robots|
|Zaech et al.<br>(2022) [80]|FG|Object<br>observations,<br>object tracks|data<br>association|short-term ✓<br>semi-static ✗<br>lifelong ✗|Any|learned<br>matching<br>(NMP)|filtering<br>(Kalman)|explicit<br>(prob.<br>edges)|LiDAR|✓<br>✗<br>✗|3D multi-object<br>tracking|
|BodySLAM<br>Henning et al.<br>(2022) [52]|FG|Camera<br>poses,<br>human centre<br>poses, SMPL<br>body params|reprojection<br>error, human<br>motion<br>model<br>(temporal)|short-term ✓<br>semi-static ✗<br>lifelong ✗|Any|OpenPose<br>keypoints|batch<br>MAP|explicit<br>covariances|Monoc-<br>ular|✗<br>✗<br>✗|Human pose<br>+ camera<br>trajectory<br>estimation|
|BodySLAM++<br>Henning et al.<br>(2023) [53]|FG|Camera<br>poses,<br>IMU states,<br>human pose<br>+shape(SMP|L)<br>repr. error,<br>IMU factors,<br>human mo-<br>tion<br>constraints|short-term ✓<br>semi-static ✗<br>lifelong ✗|Indoor|learned<br>(HMR)|incremental<br>smoothing<br>(OKVIS2)|explicit<br>covariances|Monoc-<br>ular<br>+ IMU|✓<br>✗<br>✗|Real-time<br>human +<br>camera state<br>estimation|
|AirDOS<br>Qiu et al.<br>(2022) [51]|FG|Camera<br>poses,<br>object mo-<br>tion,<br>rigid part<br>structure<br>(3D points)|rigidity and<br>motion<br>constraints,<br>reprojection<br>error|short-term ✓<br>semi-static ✗<br>lifelong ✗|Out-<br>door|ORB fea-<br>tures<br>+ instance<br>segmentatio|n<br>batch<br>MAP|explicit<br>covariances|Stereo|✗<br>✗<br>✗|4D spatio-<br>temporal maps,<br>crowded<br>urban SLAM|
||||||_Hybrid (_|_FG + SG)_||||||
|DynEMo-<br>SLAM<br>Giberna et al.<br>(2025) [21]|Hy-<br>brid|Keyframes,<br>entity obs.,<br>planes, floor|KF-entity,<br>intra-entity,<br>floor-entity|short-term ✓<br>semi-static ✓<br>lifelong ✗|Indoor|determinis-<br>tic<br>(AprilTags)|–|explicit<br>information<br>matrix|LiDAR<br>+<br>camera|✓<br>✗<br>✗|Metric-<br>semantic<br>reconstruction<br>in<br>crowdedenvs.|
|Kimera<br>Rosinol et al.<br>(2021) [35]|Hy-<br>brid|Free space,<br>agents/object<br>rooms,<br>building|s,<br>Semantic<br>relations|short-term ✓<br>semi-static ✗<br>lifelong ✗|Indoor|TEASER++<br>+ seg.|iSAM2 +<br>batch pars-<br>ing|explicit<br>(Bayesian)|Vis.-<br>inertial<br>+ RGB-<br>D|✓<br>✗<br>✓|<br>Hierarchical<br>metric-semantic<br>reconstruction<br>+ planning|
|Khronos<br>Schmid et al.<br>(2024) [15]|Hy-<br>brid|Poses, ob-<br>jects,<br>object<br>fragments|associations,<br>odometry|short-term ✓<br>semi-static ✓<br>lifelong ✗<br>|Indoor<br>|volumetric<br>IoU<br>(multi-hyp.)<br>|async<br>global<br>optimizatio|n<br>explicit<br>4D metric|RGB-D|✓<br>✓<br>✗|Lifelong<br>spatio-temporal<br>maps|
|Lost & Found<br>Behrens et al.<br>(2025) [33]|SG|Objects,<br>object parts,<br>points|Semantic<br>spatial<br>relations|_S_<br>short-term ✓<br>semi-static ✓<br>lifelong ✗|_cene grap_<br>Indoor|_h (SG) only_<br>image-based<br>detection|visual point<br>tracking|heuristic<br>confidence|RGB-D|✓<br>✓<br>✗|Object<br>tracking +<br>manipulation|
|DovSG<br>Yan et al.<br>(2025) [32]|SG|Objects<br>(labels,<br>color,<br>material)|Semantic<br>spatial<br>relations|short-term ✓<br>semi-static ✓<br>lifelong ✗|Indoor|similarity-<br>based<br>(CLIP fea-<br>tures)|online logic<br>updates|heuristic<br>confidence|RGB-D|✓<br>✓<br>✗|Mobile<br>manipulation<br>+ task<br>planning|
|CURB-SG<br>Greve et al.<br>(2024) [29]|SG|Environment,<br>roads and<br>intersections,<br>landmarks|spatial<br>relations|short-term ✓<br>semi-static ✗<br>lifelong ✗|Out-<br>door|scan match.<br>+ local<br>search|pose graph<br>opt. (PGO)|explicit<br>(fitness<br>score)|LiDAR|✓<br>✗<br>✓|Automated<br>driving|
|Aion<br>Catalano et al.<br>(2025) [14]|SG|Entity obs.,<br>navigational<br>flows, seman-<br>tic<br>abstraction|spa-<br>tial/semantic<br>rels., plan-<br>ning<br>connectivity,<br>traversal|short-term ✓<br>semi-static ✗<br>lifelong ✗|Indoor|pos.-<br>invariant<br>indexing|FreMEn<br>(frequency)|explicit<br>probabilisti|c<br>RGB-D<br>/<br>Stereo|✓<br>✗<br>✗|Forecasting<br>human<br>activity for<br>navigation|
|Functional SG<br>Zhang et al.<br>(2025) [34]|SG|Objects and<br>interactive<br>elements|costs<br>functional<br>relationships|short-term ✗<br>semi-static ✓<br>lifelong ✗|Indoor|learned<br>matching|sequential<br>LLM rea-<br>soning|learned<br>confidence|RGB-D|✗<br>✓<br>✗|3D VQA<br>+ manipulation|
|Saucedo et al.<br>(2025) [58]|SG<br>(BSG|)<br>Building,<br>rooms,<br>objects|Semantic<br>and<br>geometric<br>spatial rel.|short-term ✗<br>semi-static ✓<br>lifelong ✗|Indoor|learned<br>matching|variational<br>(GCN<br>pred.)|explicit<br>probabilisti|c<br>RGB-D|✗<br>✓<br>✗|Unvisited<br>scene<br>completion|


**Legend: Graph stack** : FG (factor graph), SG (scene graph), Hybrid (FG-backed SG / SG-constrained FG). **Dynamics type** : (i) short-term, (ii) semi-static, (iii) lifelong/structural change. **Represented Scene** : Indoor, Outdoor, Any. **Association** : data association (deterministic, MHT, JPDA, learned matching). **Inference** : batch MAP, incremental smoothing, filtering, variational, particle/mixture. **Uncertainty** : explicit probabilistic treatment versus heuristic confidence only. **RT/OV/MR** : real-time / open-vocabulary / multi-robot. 

22 

The pattern is particularly expressive in environments where structural semantics are stable and informative, while its applicability to large-scale, dynamic outdoor settings, where the number and identity of semantic entities grow rapidly, has not yet been demonstrated. 

**Belief-Augmented and Dynamic Scene Graph (SG-centric)** DovSG [32], Lost & Found [33], BSG [58], Aion [14], and Functional Scene Graphs [34] emphasize the scene graph as a persistent and explicitly dynamic world model, maintained primarily through semantic reasoning and graph-level updates rather than joint probabilistic optimization. Persistence, forgetting, and state transition are central to this pattern: Lost & Found distinguishes object removal from occlusion through the containment mechanism described in Section 4.1.2. Aion further extends this paradigm by encoding temporal activity patterns directly into the scene graph structure. These approaches excel at long-term object permanence, natural language grounding, and interaction aware updates. Their reliance on heuristic or learned confidence measures, rather than trajectory level covariances, reflects a different trade-off between semantic expressiveness and probabilistic state estimation. 

## **9.4 Trends in Graph-based World Modeling** 

Three directional trends cut across the surveyed approaches and collectively reshape the design space of probabilistic world modeling in dynamic environments. 

**From Closed-Vocabulary to Open-Vocabulary Association** Early dynamic SLAM systems defined a fixed ontology of entities types at design type, like pedestrians, vehicles, or furniture, and relied on classifiers trained on these predefined categories. More recent systems increasingly leverage vision-language embeddings, including CLIP-based representations and visionlanguage models, to support open-vocabulary perception and association. Frameworks such as DovSG [32] and ConceptGraphs [26] demonstrate that open-set object discovery and association can be integrated into real-time robotic systems, enabling world models to accommodate previously unseen categories without retraining. 

**From Reactive Maps to Predictive Spatial Memory** Early dynamic world models were predominantly reactive, updating internal representations only in response to incoming observations and answering queries about the current state of the environment. A clear trend in more recent work is the incorporation of predictive components that encode expectations about unobserved entities and future activity, of which Aion’s flow statistics (discussed below) are a representative case [14]. Belief Scene Graphs’ blind nodes (Section 4.1.2) similarly estimate likely object locations from learned co-occurrence patterns [58], while Gorlo et al. [55] leverage relational scene context to forecast long-term human 

trajectories. Altogether, these approaches extend world models from reactive state estimates toward representations that encode spatio-temporal patterns. 

**From Static Hierarchy to 4D Spatio-Temporal Representations** Conventional 3D scene graph formulations organize the environment into a spatial hierarchies, such as objects, places, rooms, and buildings, that are largely static in their structural definition. Recent work has shifted from this assumption by explicitly incorporating temporal information into the representation [15]. Aion [14] is the clearest instance of this shift: by attaching time-dependent flow statistics directly to navigational nodes, it extends the scene graph into a four-dimensional representation that captures not only spatial structure but temporal patterns of activity. This shift reflects a broader trend toward world models that encode when and how frequently interactions occur, rather than treating temporal variation as a sequence of independent snapshots. 

# **10 Open Challenges and Future Directions** 

The works surveyed throughout this paper collectively demonstrate that probabilistic graph-based representations, i.e. combining factor graphs for geometric consistency with scene graphs for semantic abstraction, form a powerful paradigm for dynamic world modeling. Yet the synthesis presented in Sections 4–9 shows that this paradigm is still evolving. Several fundamental tensions remain unresolved: between geometric uncertainty and semantic expressiveness, between short-term agent tracking and lifelong changes detections, between representational richness and computational tractability, and between single-robot operation and distributed autonomy. This section organizes open challenges around the three research questions presented in Section 1, clarifying where the field has progressed and where substantial work remains. 

## **10.1 Representation: What to Model and How** 

**Uncertainty Propagation** This survey has identified the FG-SG uncertainty boundary as a recurring structural gap, with an illustrative example in Figure 4. Within the factor graph layer, uncertainty is principled: variables carry covariance (or information) matrices, factors are weighted according to measurement quality, and the Hessian of the non-linear least-squares problem propagates uncertainty globally through the graph [6]. In many hybrid systems, this stops at the interface between layers. In layered-stack architectures, the most prevalent pattern, scene graph nodes are often instantiated from the geometric layer without inheriting pose uncertainty, such that a node extracted from a poorly constrained region of the map may be treated with the same confidence as one from a wellconstrained area. The unified optimizable graph pat- 

23 

tern (e.g. S-Graphs [11], DynEMo-SLAM [21]) partially mitigates this by representing semantic entities as factor graph variables. However, propagation of geometric uncertainty into _relational_ edges remains largely unaddressed (e.g. how certain is an _on_ relation given the covariance of both object pose nodes?). The work of Millan-Romera et al. [59] is a step toward learned uncertainty estimates for semantic factors, but a general framework for uncertainty-aware scene-graph relations in dynamic environments does not yet exist. Lost & Found [33] explicitly acknowledges that principled uncertainty quantification for tracked object states under interaction is a critical missing piece. 

A symmetric and largely unexamined problem exists at the opposite boundary too, between the perception front-ends and the factor graph itself. The probabilistic machinery described in Section 2 rests on the assumption of zero-mean, temporally independent Gaussian measurement noise. As front-ends increasingly replace geometric primitives with learned geometric priors, this assumption is systematically violated: monocular depth foundation models, designed for single images, exhibit temporally inconsistent, flickering predictions across consecutive frames of a video [130], producing errors that are correlated over time and biased rather than zero-mean. Such errors are particularly damaging for dynamic entities, where the multi-view temporal fusion used to stabilize depth on static structure [130] is unavailable, since independent object motion breaks the underlying temporal consistency constraints. While learned depth and its uncertainty have been integrated into factor graph estimation for the static case [131] [132], no equivalent framework calibrates the error statistics of learned geometric priors before their injection into dynamic-entity factors; the learned semantic covariances of [133] address the semantic factor class only. 

Closing these gaps, at both perception-factor graph and factor graph-scene graph boundaries, appears increasingly important for safety-critical deployment, where a robot must know not only _what_ its world model asserts, but also _how much_ to trust each assertion. 

**Non-Rigid Deformation Modeling** The surveyed works are largely restricted to rigid-body dynamics: agents are modeled as rigid objects with 6-DoF pose trajectories, and structures are assumed piecewise rigid. Non-rigid deformation, such as soft objects, cloth, liquids, deformable tools, remains almost entirely absent from probabilistic graph-based representations. The body-model comparison in Section 4.2.1 and Table 3 shows the spectrum: SMPL-family parametric models handle articulated human motion through skeletal kinematics, but treat the body surface as a predefined template with limited expressiveness for atypical morphologies or extreme deformation, while neural representation such as InstantAvatar [73] achieve higher fidelity at the cost of losing differentiability with respect to classical factor-graph optimization. Extending factor graphs to non-rigid entities requires defining suitable state spaces, motion priors, and measurement models, a challenge 

connected to the broader problem of deformable SLAM and still an open research frontier [1]. 

**Completeness of Dynamics Coverage** As summarized by Table 7 (Section 9), no current system in the surveyed literature handles all three levels of dynamics (continuously moving agents, semi-static changes, and long-term structural evolution) simultaneously within a single unified probabilistic framework. Systems that handle agents well (DynoSAM [16], AirDOS [51]) typically do not model semi-static change; systems that handle semi-static change well (Khronos [15], DynEMoSLAM [21]) generally lack principled lifelong structural maintenance. This gap reflects not only engineering constraints but also a deeper modeling difficulty: these dynamics occur at timescales that differ by order of magnitude, and the most effective probabilistic treatments are not trivially composable (e.g. tightly-coupled factorgraph optimization for agent motion, persistence/decay mechanism for semi-static change, and inter session change detection with loop closure for structural evolution). Unifying these regimes without sacrifying tractability remains an open problem. 

**Metric Scale Observability of Dynamic Entities under Minimal Sensing** A structural pattern visible in Table 7 but rarely made explicit in the literature is that the coverage of dynamics reported above is conditioned on metrically informative sensing: nearly all surveyed factor-graph formulations rely on stereo, RGB-D, or LiDAR input [19] [16] [51] [64]. This is not incidental. For an independently moving entity observed monocularly, the entity’s structure scale, its motion, and the ego-motion scale are mutually entangled: unlike static structure, whose metric scale can be recovered from inertial measurements or transferred from the ego solution, the observed image displacements of a dynamic entity hinder ego-motion and object motion, making ratio-based scale transfer invalid. The few monocular systems that do estimate dynamic entities resolve this only through strong metric priors: learned object dimensions [134], parametric human body models [52] [53], or rigid-body kinematic structure [51]. Existing analysis of dynamic SLAM formulations address coordinate frame choices [85] and estimation efficiency [105], but to the best of our knowledge no principled observability analysis exists that characterizes which components of a dynamic entity’s _SE_ (3) trajectory and scale are recoverable given a specific sensor suite, nor which shared static structure can serve as a metric anchor in the absence of direct depth. Closing this gap is a precondition for deploying the dynamic world models surveyed here on low-cost, weight-constrained platforms such as micro aerial vehicles and AR devices, where monocular-inertial sensing is often the only option. 

**Gaussian Splatting as a Geometric Substrate** 3D Gaussian Splatting (3DGS) [135], a differentiable, high-fidelity alternative to point clouds and meshes, is an emerging geometric substrate not yet integrated with the probabilistic graph-based frameworks surveyed 

24 

here. Dynamic extensions [136] [137] [138] [139] separate static and dynamic Gaussian primitives, but largely follow an outlier-rejection paradigm rather than a probabilistic SLAMMOT formulation. A natuaral next step is a tripartite representation in which a factor graph provides the probabilistic trajectory backbone, a Gaussian-splatting layer the geometric-photometric substrate, and a scene graph the relational semantic abstraction, raising open questions on propagating factorgraph uncertainty into Gaussian primitives, extracting scene-graph entities from Gaussian fields, and jointly optimizing all three layers in real time. 

## **10.2 Construction and Maintenance: How to Build and Maintain** 

**Scalable Lifelong Graph Maintenance** Long-term autonomy requires world models that remain tractable and accurate across sessions separated by hours, days, or months. DPG-SLAM [49] established a core principle: a graph cannot grow indefinitely, and an explicit forgetting policy, such as pruning nodes when they no longer contribute topological information, is essential for lifelong operation. LT-mapper [50] demonstrated this principle at large scale for outdoor LiDAR SLAM. However, as the dynamics and structural complexity of the environment increase, the decision between what to keep and what to discard becomes harder to resolve reliably. Many existing forgetting policies are primarily geometric or heuristic, and do not explicitly reason about the downstream utility of information for future tasks. A promising direction is task-informed graph maintenance [3], where the decision to retain, update or prune nodes is conditioned on anticipated task distributions, eventually linking memory management to the planning and interactions layers described in Sections 7 and 6. 

**Open-Vocabulary Association under Severe Dynamics** The shift toward open-vocabulary perception (Section 9.4) is a significant advance, but current openvocabulary systems are often evaluated under relatively controlled conditions. Under severe dynamics, like dense crowd occlusion, rapid viewpoint change, and simultaneous motion of many agents, the vision-language embeddings used for association (e.g. CLIP features in [32], [26]) may become unstable, and the lack of closedform data-association uncertainty increases vulnerability to catastrophic misassociations. Integrating openvocabulary perception into principled multi-hypothesis association frameworks (Section 5.2) within this domain remains open, as does the question of how to bound false-association rates in scenes with many visually similar entities in motion. 

**Multi-Robot Shared Dynamic World Models** As shown in Table 7, explicit multi-robot capability (MR) is rare across the surveyed works: only Kimera [35] and CURB-SG [29] explicitly target it, and neither addresses the full complexity of shared dynamic world modeling in which multiple robots simultaneously observe, track, and update a common representation of 

moving agents and changing structures. Multi S-Graphs [140] demonstrates that semantic-relational information can be exchanged efficiently to improve map merging, but extending this to dynamic entity tracking, where an agent observed by robot _A_ must be correctly associated with the track maintained by robot _B_ despite occlusion, viewpoint and time differences, introduces cross-agent data-association challenges that remain largely unaddressed. PMBM-based formulations [92] offer a theoretically grounded starting point towards a distributed extension, but have not yet been coupled to scene-graphlevel semantic reasoning and maintenance policies. 

## **10.3 Exploitation** 

The applications surveyed in Section 7 demonstrate that hybrid probabilistic graph representations can support a qualitatively richer set of downstream capabilities than either factor graphs or scene graphs alone. Yet the exploitation layer reveals its own set of open challenges, which are distinct from the representation and maintenance gaps above: even a perfectly maintained world model cannot be fully exploited by current task-level systems. 

**Uncertainty-Aware Downstream Tasks and Proactive Planning under Dynamics** The probabilistic machinery underlying factor graphs produces rich uncertainty estimates, such as pose covariances and existence probabilities for dynamic entities, that are largely discarded at task execution time. In practice, planners exploit scene graph nodes as point estimates, manipulation systems act on deterministic object poses, and task reasoners treat scene state as binary truth, regardless of how well constrained the underlying map is. This disconnection is particularly problematic near the boundaries of map reliability, where sparse loop closures or recent dynamics induce high uncertainty but do not influence decision-making. Planning over scene graphs has begun to address graph updates [95], yet broader questions remain open: how map uncertainty should affect task selection, action sequencing, or the decision to actively seek additional observations. A closely related limitation appears in planning under dynamics. Current systems either replan reactively when scene graph nodes change or invalidate precomputed paths [95], while predictive approaches, such as Aion’s temporal flow statistics [14] or trajectory forecasting from scene graph context [55], remain decoupled from probabilistic task planning. Bridging factor-graph uncertainty and predictive temporal models into task-level planning objectives, so that actions are conditioned on the expected future state of the world rather than its instantaneous estimate, remains a largely open challenge. 

**Closing the Exploitation-to-Representation Loop: Active Perception** All surveyed systems are effectively open-loop between exploitation and representation: task execution consumes the world model but does not feed information back to guide 

25 

its refinement. A robot that fails to grasp an object because its pose estimate was uncertain has acquired evidence about which part of the map is unreliable, but no current system uses task-execution outcomes to trigger targeted re-observation or prioritize re-mapping of specific regions. The active perception literature addresses related problems, but largely in isolation from the structured world models surveyed here. Coupling the task layer to the maintenance layer, so that downstream failures or high-uncertainty decisions trigger directed exploration to reduce map uncertainty in task-relevant regions, would close the loop between the three research questions. This direction is conceptually previewed by task-informed graph pruning in Clio [3], which uses task context to decide what to retain, but the inverse direction, using task failures to decide what to re-observe, remains entirely open. 

**Temporal Consistency of Language-Grounded Task Plans** Systems like SayPlan [4] and SG-Nav [100] ground natural language instructions in scene graph state to produce task plans. This grounding is computed at a single moment in time and assumed stable for the duration of task execution. In dynamic environments, however, the scene graph changes continuously: objects are displaced by human interaction, agents move, doors open and close. A task plan grounded in a scene graph that was valid at planning time may refer to entities or relations that no longer hold at execution time, leading to silent failures that are difficult to detect and recover from. No current system monitors the temporal consistency between an active task plan and the evolving world model, or triggers re-planning when the graph changes in ways that invalidate the current plan’s preconditions. This is particularly acute for multi-step manipulation tasks in humanpopulated environments, where the interval between planning and execution may span multiple human interactions. The connection between dynamic graph update policies (Section 5.4) and plan validity monitoring is entirely unaddressed in the surveyed literature. 

**Evaluation Gap: Task Performance as a Function of World Model Quality** A methodological gap cuts across all exploitation challenges: there is currently no benchmark or evaluation protocol that measures downstream task performance as a function of world model accuracy under dynamics. This limitation stems primarily from the lack of challenging datasets in which the tight integration of dynamic handling and reasoning is required for the system to succeed on them. Most work relies on commonly used and accepted datasets (Section 8.2) which are not built to create a realistic, challenging scenario regarding the dynamicity level of the environment. This results on under-validated works or the requirement for them to generate self-collected datasets to showcase the effective benefit of the proposed contributions [21]. This limitation is compounded by a more basic one: accurate 6-DoF ground truth for the dynamic entities themselves is essentially only available inside motion-capture volumes [113] [114] [116], re- 

stricting validation to room-scale scenes, or as humanannotated 3D bounding boxes in driving benchmarks [101] [103], whose accuracy and domain do not transfer to indoor and mixed indoor-outdoor robotics. No existing dataset provides metrically accurate object trajectories for handheld or robot-mounted sequences at building scale, which is the regime targeted by most systems in Table 7, and a further reason why simulation [35] [123] and self-collected data [21] dominate current evaluations. Existing evaluation protocols (Section 8.1) assess trajectory accuracy, map geometry, graph structure, and tracking metrics largely in isolation from task outcomes. The connection between, for instance, a 10% increase in object pose RMSE under crowded dynamics and the resulting manipulation success rate degradation is not measured by any of the surveyed evaluation frameworks. This gap makes it difficult to quantify the practical benefit of more accurate dynamic world models for robotic autonomy, and to motivate the computational cost of the more expressive representations described in this survey. Developing task-conditioned evaluation protocols, where world model quality is assessed through its effect on downstream task success under varying levels of environmental dynamics, would provide a more grounded benchmark for future progress. This connects naturally to the consecutive task execution protocols already adopted by works like DovSG [32], which could be extended to include controlled degradation of world model quality as an independent variable. 

The open challenges above allow the three research questions presented in Section 1 to be summarized. Regarding _which representations_ are suited to dynamic environments, the taxonomy shows that no single graph stack dominates; instead, key limitations arise at the interfaces between paradigms (notably uncertainty transfer across the FG-SG boundary and incomplete coverage across dynamics timescales). Regarding _how representations can be constructed and maintained_ , the pipeline is increasingly well understood for single sessions with moderate dynamics, but scalable lifelong maintenance, robust open-vocabulary association under severe dynamics, and multi-robot shared construction remain unresolved. Regarding _how representations can be exploited_ , downstream capabilities are already broad, yet their reliability depends on representations that remain consistent under change and can quantify confidence across geometric and semantic layers. In this context, tighter integration between probabilistic factor graphs, semantically rich scene graphs, and emerging dense geometric substrates, in our view, one of the central challenges, and a promising direction, for long-term robotic situational awareness in dynamic environments. 

# **References** 

- [1] Luca Carlone, Ayoung Kim, Timothy Barfoot, Daniel Cremers, and Frank Dellaert, _SLAM Handbook. From Localization and Mapping to Spatial Intelligence_ . Cambridge University Press, 2025. 

26 

- [2] H. Bavle, J. L. Sanchez-Lopez, C. Cimarelli, A. Tourani, and H. Voos, “From SLAM to Situational Awareness: Challenges and Survey,” _Sensors_ , vol. 23, no. 10, p. 4849, May 2023. [Online]. Available: https://www.mdpi. com/1424-8220/23/10/4849 

- [3] D. Maggio, Y. Chang, N. Hughes, M. Trang, D. Griffith, C. Dougherty, E. Cristofalo, L. Schmid, and L. Carlone, “ _Clio:_ Real-Time Task-Driven Open-Set 3D Scene Graphs,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 10, pp. 8921–8928, Oct. 2024. [Online]. Available: https://ieeexplore.ieee.org/document/10659066/ 

- [4] K. Rana, J. Haviland, S. Garg, J. AbouChakra, I. Reid, and N. Suenderhauf, “Sayplan: Grounding large language models using 3d scene graphs for scalable robot task planning,” 2023. [Online]. Available: https://arxiv.org/abs/2307. 06135 

- [5] F. Dellaert, “Factor Graphs: Exploiting Structure in Robotics,” _Annual Review of Control, Robotics, and Autonomous Systems_ , vol. 4, no. 1, pp. 141–166, May 2021. [Online]. Available: https://www.annualreviews.org/doi/ 10.1146/annurev-control-061520-010504 

- [6] F. Dellaert and M. Kaess, “Factor Graphs for Robot Perception,” _Foundations and Trends in Robotics_ , vol. 6, no. 1-2, pp. 1–139, 2017. [Online]. Available: http://www.nowpublishers. com/article/Details/ROB-043 

- [7] M. Mukadam, J. Dong, X. Yan, F. Dellaert, and B. Boots, “Continuous-time gaussian process motion planning via probabilistic inference,” _The International Journal of Robotics Research_ , vol. 37, no. 11, pp. 1319–1340, 2018. 

- [8] X. Chang, P. Ren, P. Xu, Z. Li, X. Chen, and A. Hauptmann, “A Comprehensive Survey of Scene Graphs: Generation and Application,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 45, no. 1, pp. 1– 26, Jan. 2023. [Online]. Available: https: //ieeexplore.ieee.org/document/9661322/ 

- [9] I. Catalano, C. C. Zumaya, J. A. Placed, J. Civera, W. M. Bessa, and J. Pe˜naQueralta, “3D Scene Graphs in Robotics: A Unified Representation Bridging Geometry, Semantics, and Action,” Aug. 2025. [Online]. Available: https://www.techrxiv.org/doi/full/10. 36227/techrxiv.175561766.62405781 

- [10] N. Hughes, Y. Chang, and L. Carlone, “Hydra: A Real-time Spatial Perception System for 3D Scene Graph Construction and Optimization,” in _Robotics: Science and Systems XVIII_ . Robotics: Science and Systems Foundation, Jun. 2022. [Online]. Available: http://www. roboticsproceedings.org/rss18/p050.pdf 

- [11] H. Bavle, J. L. Sanchez-Lopez, M. Shaheer, J. Civera, and H. Voos, “S-Graphs 2.0–A Hierarchical-Semantic Optimization and Loop Closure for SLAM,” _arXiv preprint arXiv:2502.18044_ , 2025. 

- [12] K. Wang, J. Guo, K. Chen, and J. Lu, “An In-Depth Examination of SLAM Methods: Challenges, Advancements, and Applications in Complex Scenes for Autonomous Driving,” _IEEE Transactions on Intelligent Transportation Systems_ , vol. 26, no. 7, pp. 11 066–11 087, Jul. 2025. [Online]. Available: https://ieeexplore.ieee. org/document/10908366/ 

- [13] B. Bescos, J. M. Facil, J. Civera, and J. Neira, “DynaSLAM: Tracking, Mapping, and Inpainting in Dynamic Scenes,” _IEEE Robotics and Automation Letters_ , vol. 3, no. 4, pp. 4076–4083, Oct. 2018. [Online]. Available: https://ieeexplore.ieee.org/document/8421015/ 

- [14] I. Catalano, E. Montijano, J. Civera, J. A. Placed, and J. Pena-Queralta, “Aion: Towards Hierarchical 4D Scene Graphs with Temporal Flow Dynamics,” 2025, version Number: 1. [Online]. Available: https://arxiv.org/abs/2512. 11903 

- [15] L. Schmid, M. Abate, Y. Chang, and L. Carlone, “Khronos: A Unified Approach for SpatioTemporal Metric-Semantic SLAM in Dynamic Environments,” in _Proc. of Robotics: Science and Systems (RSS)_ , Delft, Netherlands, Jul. 2024. 

- [16] J. Morris, Y. Wang, M. Kliniewski, and V. Ila, “DynoSAM: Open-Source Smoothing and Mapping Framework for Dynamic SLAM,” _IEEE Transactions on Robotics_ , pp. 1–19, 2025. [Online]. Available: https://ieeexplore.ieee.org/ document/11288097/ 

- [17] A. Deeb, M. L. Seto, and Y. Pan, “Model-based Dynamic Pose Graph SLAM in Unstructured Dynamic Environments,” in _2019 19th International Conference on Advanced Robotics (ICAR)_ . Belo Horizonte, Brazil: IEEE, Dec. 2019, pp. 123–128. [Online]. Available: https://ieeexplore.ieee.org/document/8981632/ 

- [18] D. Gulati, F. Zhang, D. Malovetz, D. Clarke, and A. Knoll, “Robust cooperative localization in a dynamic environment using factor graphs and probability data association filter,” in _2017 20th International Conference on Information Fusion (Fusion)_ . Xi’an, China: IEEE, Jul. 2017, pp. 1–6. [Online]. Available: http://ieeexplore.ieee. org/document/8009654/ 

- [19] B. Bescos, C. Campos, J. D. Tardos, and J. Neira, “DynaSLAM II: Tightly-Coupled MultiObject Tracking and SLAM,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 3, pp. 5191–5198, Jul. 2021. [Online]. Available: https: //ieeexplore.ieee.org/document/9385844/ 

27 

- [20] A. Deeb, M. Seto, and Y.-J. Pan, “Piecewisedeterministic Quasi-static Pose Graph SLAM in Unstructured Dynamic Environments,” _Journal of Intelligent & Robotic Systems_ , vol. 106, no. 2, p. 34, Oct. 2022. [Online]. Available: https: //link.springer.com/10.1007/s10846-022-01739-5 

- [21] M. Giberna, M. Shaheer, M. Fernandez-Cortizas, J. A. Millan-Romera, J. L. Sanchez-Lopez, and H. Voos, “DYNEMO-SLAM: Dynamic Entity and Motion-Aware 3D Scene Graph SLAM,” Dec. 2025, arXiv:2503.02050 [cs]. [Online]. Available: http://arxiv.org/abs/2503.02050 

- [22] D. Brink, “Using probabilistic graphical models to detect dynamic objects for mobile robots,” Ph.D. dissertation, Stellenbosch University, 2016. [Online]. Available: http://hdl.handle.net/10019. 1/100224 

- [23] J. Johnson, R. Krishna, M. Stark, L.-J. Li, D. Shamma, M. Bernstein, and L. Fei-Fei, “Image retrieval using scene graphs,” in _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2015. 

- [24] H. Li, G. Zhu, L. Zhang, Y. Jiang, Y. Dang, H. Hou, P. Shen, X. Zhao, S. A. A. Shah, and M. Bennamoun, “Scene graph generation: A comprehensive survey,” _Neurocomputing_ , vol. 566, p. 127052, 2024. 

- [25] G. Adaimi, D. Mizrahi, and A. Alahi, “Composite relationship fields with transformers for scene graph generation,” in _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , 2023, pp. 52–64. 

- [26] Q. Gu, A. Kuwajerwala, S. Morin, K. M. Jatavallabhula, B. Sen, A. Agarwal, C. Rivera, W. Paul, K. Ellis, R. Chellappa, C. Gan, C. M. de Melo, J. B. Tenenbaum, A. Torralba, F. Shkurti, and L. Paull, “ConceptGraphs: OpenVocabulary 3D Scene Graphs for Perception and Planning,” 2023, version Number: 1. [Online]. Available: https://arxiv.org/abs/2309.16650 

- [27] S.-C. Wu, J. Wald, K. Tateno, N. Navab, and F. Tombari, “SceneGraphFusion: Incremental 3D Scene Graph Prediction from RGB-D Sequences,” in _2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . Nashville, TN, USA: IEEE, Jun. 2021, pp. 7511–7521. [Online]. Available: https://ieeexplore.ieee.org/document/9578559/ 

- [28] A. Rosinol, A. Gupta, M. Abate, J. Shi, and L. Carlone, “3D Dynamic Scene Graphs: Actionable Spatial Perception with Places, Objects, and Humans,” in _Robotics: Science and Systems XVI_ . Robotics: Science and Systems Foundation, Jul. 2020. [Online]. Available: http: //www.roboticsproceedings.org/rss16/p079.pdf 

- [29] E. Greve, M. B¨uchner, N. V¨odisch, W. Burgard, and A. Valada, “Collaborative Dynamic 3D Scene Graphs for Automated Driving,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . Yokohama, Japan: IEEE, May 2024, pp. 11 118–11 124. [Online]. Available: https://ieeexplore.ieee.org/document/10610112/ 

- [30] I. Armeni, O. Sener, A. R. Zamir, H. Jiang, I. Brilakis, M. Fischer, and S. Savarese, “3D Semantic Parsing of Large-Scale Indoor Spaces,” in _2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , Jun. 2016, pp. 1534–1543. 

- [31] U.-H. Kim, J.-M. Park, T.-j. Song, and J.H. Kim, “3-D Scene Graph: A Sparse and Semantic Representation of Physical Environments for Intelligent Agents,” _IEEE Transactions on Cybernetics_ , vol. 50, no. 12, pp. 4921– 4933, Dec. 2020, conference Name: IEEE Transactions on Cybernetics. [Online]. Available: https://ieeexplore.ieee.org/document/8796400 

- [32] Z. Yan, S. Li, Z. Wang, L. Wu, H. Wang, J. Zhu, L. Chen, and J. Liu, “Dynamic OpenVocabulary 3D Scene Graphs for Long-Term Language-Guided Mobile Manipulation,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 5, pp. 4252–4259, May 2025. [Online]. Available: https://ieeexplore.ieee.org/document/10909193/ 

- [33] T. Behrens, R. Zurbr¨ugg, M. Pollefeys, Z. Bauer, and H. Blum, “Lost & Found: Tracking Changes From Egocentric Observations in 3D Dynamic Scene Graphs,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 4, pp. 3739– 3746, Apr. 2025. [Online]. Available: https: //ieeexplore.ieee.org/document/10897827/ 

- [34] C. Zhang, A. Delitzas, F. Wang, R. Zhang, X. Ji, M. Pollefeys, and F. Engelmann, “OpenVocabulary Functional 3D Scene Graphs for RealWorld Indoor Spaces,” 2025, version Number: 1. [Online]. Available: https://arxiv.org/abs/2503. 19199 

- [35] A. Rosinol, A. Violette, M. Abate, N. Hughes, Y. Chang, J. Shi, A. Gupta, and L. Carlone, “Kimera: from SLAM to Spatial Perception with 3D Dynamic Scene Graphs,” 2021, version Number: 3. [Online]. Available: https://arxiv. org/abs/2101.06894 

- [36] H. Bavle, J. L. Sanchez-Lopez, M. Shaheer, J. Civera, and H. Voos, “Situational Graphs for Robot Navigation in Structured Indoor Environments,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 4, pp. 9107–9114, Oct. 2022, conference Name: IEEE Robotics and Automation Letters. [Online]. Available: https: //ieeexplore.ieee.org/document/9826367 

- [37] A. Tourani, S. Ejaz, H. Bavle, M. FernandezCortizas, D. Morilla-Cabello, J. L. Sanchez-Lopez, 

28 

and H. Voos, “vs-graphs: Tightly coupling visual slam and 3d scene graphs exploiting hierarchical scene understanding,” _IEEE Robotics and Automation Letters_ , 2026. 

- [38] T. P. Kucner, M. Magnusson, S. Mghames, L. Palmieri, F. Verdoja, C. S. Swaminathan, T. Krajn´ık, E. Schaffernicht, N. Bellotto, M. Hanheide, and A. J. Lilienthal, “Survey of maps of dynamics for mobile robots,” _The International Journal of Robotics Research_ , vol. 42, no. 11, pp. 977–1006, 2023. [Online]. Available: https://doi.org/10.1177/02783649231190428 

- [39] D. Hahnel, R. Triebel, W. Burgard, and S. Thrun, “Map building with mobile robots in dynamic environments,” in _2003 IEEE International Conference on Robotics and Automation (Cat. No. 03CH37422)_ , vol. 2. IEEE, 2003, pp. 1557–1563. 

- [40] R. Mascaro and M. Chli, “Scene Representations for Robotic Spatial Perception,” _Annual Review of Control, Robotics, and Autonomous Systems_ , vol. 8, no. 1, pp. 351–377, May 2025. [Online]. Available: https://www.annualreviews.org/content/ journals/10.1146/annurev-control-040423-030709 

- [41] C. I. Amuche, X. Zhang, H. N. Monday, G. U. Nneji, C. C. Ukwuoma, O. C. Chikwendu, Y. Hyeon Gu, and M. A. Al-antari, “Advancements, Challenges, and Future Directions in Scene-Graph-Based Image Generation: A Comprehensive Review,” _Electronics_ , vol. 14, no. 6, p. 1158, Mar. 2025. [Online]. Available: https://www.mdpi.com/2079-9292/14/6/1158 

- [42] T. Lai, “A Review on Visual-SLAM: Advancements from Geometric Modelling to LearningBased Semantic Scene Understanding Using Multi-Modal Sensor Fusion,” _Sensors_ , vol. 22, no. 19, p. 7265, Sep. 2022. [Online]. Available: https://www.mdpi.com/1424-8220/22/19/7265 

- [43] Y. Wang, Y. Tian, J. Chen, K. Xu, and X. Ding, “A Survey of Visual SLAM in Dynamic Environment: The Evolution From Geometric to Semantic Approaches,” _IEEE Transactions on Instrumentation and Measurement_ , vol. 73, pp. 1–21, 2024. [Online]. Available: https: //ieeexplore.ieee.org/document/10577209/ 

- [44] K. Chen, J. Xiao, J. Liu, Q. Tong, H. Zhang, R. Liu, J. Zhang, A. Ajoudani, and S. Chen, “Semantic Visual Simultaneous Localization and Mapping: A Survey,” _IEEE Transactions on Intelligent Transportation Systems_ , vol. 26, no. 6, pp. 7426–7449, Jun. 2025. [Online]. Available: https://ieeexplore.ieee.org/document/11005698/ 

- [45] S. Wen, P. Li, Y. Zhao, H. Zhang, F. Sun, and Z. Wang, “Semantic visual SLAM in dynamic environment,” _Autonomous Robots_ , vol. 45, no. 4, pp. 493–504, May 2021. [Online]. Available: https://doi.org/10.1007/s10514-021-09979-4 

- [46] Z. Xu, Z. Rong, and Y. Wu, “A survey: which features are required for dynamic visual simultaneous localization and mapping?” _Visual Computing for Industry, Biomedicine, and Art_ , vol. 4, no. 1, p. 20, Dec. 2021. [Online]. Available: https://vciba.springeropen.com/articles/10. 1186/s42492-021-00086-w 

- [47] M. T. Khan and A. Waheed, “Foundation Model Driven Robotics: A Comprehensive Review,” 2025, version Number: 1. [Online]. Available: https://arxiv.org/abs/2507.10087 

- [48] C. Gomez, A. C. Hernandez, E. Derner, R. Barber, and R. Babuska, “Object-Based Pose Graph for Dynamic Indoor Environments,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 4, pp. 5401–5408, Oct. 2020. [Online]. Available: https://ieeexplore.ieee.org/document/9134440/ 

- [49] A. Walcott-Bryant, M. Kaess, H. Johannsson, and J. J. Leonard, “Dynamic pose graph SLAM: Long-term mapping in low dynamic environments,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . Vilamoura-Algarve, Portugal: IEEE, Oct. 2012, pp. 1871–1878. [Online]. Available: http:// ieeexplore.ieee.org/document/6385561/ 

- [50] G. Kim and A. Kim, “Lt-mapper: A modular framework for lidar-based lifelong mapping,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022, pp. 7995–8002. 

- [51] Y. Qiu, C. Wang, W. Wang, M. Henein, and S. Scherer, “Airdos: Dynamic slam benefits from articulated objects,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022. 

- [52] D. F. Henning, T. Laidlow, and S. Leutenegger, “BodySLAM: Joint Camera Localisation, Mapping, and Human Motion Tracking,” 2022, version Number: 3. [Online]. Available: https://arxiv.org/abs/2205.02301 

- [53] D. F. Henning, C. Choi, S. Schaefer, and S. Leutenegger, “BodySLAM++: Fast and Tightly-Coupled Visual-Inertial Camera and Human Motion Tracking,” 2023, version Number: 1. [Online]. Available: https://arxiv.org/abs/2309.01236 

- [54] E. Olivastri, J. Francis, A. Pretto, N. S¨underhauf, and K. Rana, “Multi-Modal 3D Scene Graph Updater for Shared and Dynamic Environments,” 2024, version Number: 1. [Online]. Available: https://arxiv.org/abs/2411.02938 

- [55] N. Gorlo, L. Schmid, and L. Carlone, “LongTerm Human Trajectory Prediction Using 3D Dynamic Scene Graphs,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 12, pp. 10 978– 10 985, Dec. 2024. [Online]. Available: https: //ieeexplore.ieee.org/document/10720207/ 

29 

- [56] S. Song, Q. Zhu, and H. Hu, “RTSSLAM: Robust, Tightly-Coupled, and SemanticEnhanced LiDAR-Inertial SLAM,” _IEEE Sensors Journal_ , pp. 1–1, 2025. [Online]. Available: https://ieeexplore.ieee.org/document/11174098/ 

- [57] Lingzhu Xiang, Zhile Ren, Mengrui Ni, and O. C. Jenkins, “Robust graph SLAM in dynamic environments with moving landmarks,” in _2015 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . Hamburg, Germany: IEEE, Sep. 2015, pp. 2543–2549. [Online]. Available: http://ieeexplore.ieee.org/document/7353723/ 

- [58] M. A. V. Saucedo, V. K. Viswanathan, C. Kanellakis, and G. Nikolakopoulos, “Estimating Commonsense Scene Composition on Belief Scene Graphs,” May 2025, arXiv:2505.02405 [cs]. [Online]. Available: http://arxiv.org/abs/2505.02405 

- [59] J. A. Millan-Romera, M. Shaheer, M. FernandezCortizas, M. R. Oswald, H. Voos, and J. L. Sanchez-Lopez, “Generation of uncertainty-aware high-level spatial concepts in factorized 3d scene graphs via graph neural networks,” 2026. [Online]. Available: https://arxiv.org/abs/2409.11972 

- [60] J. Zhang, L. Yuan, T. Ran, Q. Tao, and Z. Wu, “Outlier elimination for monocular object slam based on spatiotemporal consistency constraints,” _IEEE Sensors Journal_ , vol. 23, no. 8, pp. 8887– 8898, 2023. 

- [61] J. Morris, Y. Wang, and V. Ila, “Online Dynamic SLAM with Incremental Smoothing and Mapping,” 2025, version Number: 1. [Online]. Available: https://arxiv.org/abs/2509.08197 

- [62] T. Zhang, N. Li, G. Gong, and X. Lin, “Semantic-integrated multi-model fitting for realtime VSLAM in highly dynamic environments,” _The Visual Computer_ , vol. 42, no. 1, p. 56, Jan. 2026. [Online]. Available: https://link.springer. com/10.1007/s00371-025-04235-7 

- [63] X. Tian, Z. Zhu, J. Zhao, G. Tian, and C. Ye, “DL-SLOT: Tightly-Coupled Dynamic LiDAR SLAM and 3D Object Tracking Based on Collaborative Graph Optimization,” _IEEE Transactions on Intelligent Vehicles_ , vol. 9, no. 1, pp. 1017–1027, Jan. 2024. [Online]. Available: https://ieeexplore.ieee.org/document/10255288/ 

- [64] R. Gou, G. Chen, X. Pu, X. Liao, and R. Chen, “A Visual SLAM With Tightly Coupled Integration of Multiobject Tracking for Production Workshop,” _IEEE Internet of Things Journal_ , vol. 11, no. 11, pp. 19 949– 19 962, Jun. 2024. [Online]. Available: https: //ieeexplore.ieee.org/document/10443596/ 

- [65] M. Loper, N. Mahmood, J. Romero, G. PonsMoll, and M. J. Black, “SMPL: a skinned multi-person linear model,” _ACM Transactions_ 

_on Graphics_ , vol. 34, no. 6, pp. 1–16, Nov. 2015. [Online]. Available: https://dl.acm.org/doi/10. 1145/2816795.2818013 

- [66] G. Pavlakos, V. Choutas, N. Ghorbani, T. Bolkart, A. A. A. Osman, D. Tzionas, and M. J. Black, “Expressive body capture: 3D hands, face, and body from a single image,” in _Proceedings IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2019, pp. 10 975–10 985. 

- [67] A. A. A. Osman, T. Bolkart, and M. J. Black, “STAR: A sparse trained articulated human body regressor,” in _European Conference on Computer Vision (ECCV)_ , 2020, pp. 598–613. [Online]. Available: https://star.is.tue.mpg.de 

- [68] M. Kocabas, N. Athanasiou, and M. J. Black, “Vibe: Video inference for human body pose and shape estimation,” in _The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2020. 

- [69] Y. Rong, T. Shiratori, and H. Joo, “Frankmocap: A monocular 3d whole-body pose estimation system via regression and integration,” in _IEEE International Conference on Computer Vision Workshops_ , 2021. 

- [70] H. Joo, N. Neverova, and A. Vedaldi, “Exemplar fine-tuning for 3d human pose fitting towards inthe-wild 3d human pose estimation,” _3DV_ , 2021. 

- [71] Y. Wang, Y. Sun, P. Patel, K. Daniilidis, M. J. Black, and M. Kocabas, “Prompthmr: Promptable human mesh recovery,” _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025. 

- [72] K. Lin, L. Wang, and Z. Liu, “End-to-end human pose and mesh reconstruction with transformers,” in _CVPR_ , 2021. 

- [73] T. Jiang, X. Chen, J. Song, and O. Hilliges, “Instantavatar: Learning avatars from monocular video in 60 seconds,” June 2023. 

- [74] R. Bregier, G. Fiche, L. Bravo-Sanchez, T. Lucas, M. Armando, P. Weinzaepfel, G. Rogez, and F. Baradel, “Human mesh modeling for anny body,” 2025. [Online]. Available: https://arxiv. org/abs/2511.03589 

- [75] R. Shao, W. Li, L. Zhang, R. Zhang, Z. Liu, R. Chen, and L. Nie, “Large VLM-based Vision-Language-Action Models for Robotic Manipulation: A Survey,” 2025, version Number: 2. [Online]. Available: https://arxiv.org/abs/2508.13073 

- [76] D. Rotondi, F. Scaparro, H. Blum, and K. O. Arras, “FunGraph: Functionality Aware 3D Scene Graphs for Language-Prompted Scene Interaction,” Aug. 2025, arXiv:2503.07909 [cs]. [Online]. Available: http://arxiv.org/abs/2503. 07909 

30 

- [77] M. Labbe and F. Michaud, “Online global loop closure detection for large-scale multi-session graph-based slam,” in _2014 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, 2014, pp. 2661–2666. 

- [78] M. A. Vega Torres, A. Braun, and A. Borrmann, “BIM-SLAM: Integrating BIM Models in Multisession SLAM for Lifelong Mapping using 3D LiDAR,” in _Proceedings of the 40th International Symposium on Automation and Robotics in Construction (IAARC)_ , Jul. 2023, pp. 521–528. 

- [79] M. Shaheer, J. A. Millan-Romera, H. Bavle, M. Giberna, J. L. Sanchez-Lopez, J. Civera, and H. Voos, “Tightly Coupled SLAM with Imprecise Architectural Plans,” _arXiv preprint arXiv:2408.01737v2_ , 2025. 

- [80] J.-N. Zaech, A. Liniger, D. Dai, M. Danelljan, and L. Van Gool, “Learnable Online Graph Representations for 3D Multi-Object Tracking,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 2, pp. 5103–5110, Apr. 2022. [Online]. Available: https://ieeexplore.ieee.org/document/ 9691806/ 

- [81] B. Ristic, B.-T. Vo, B.-N. Vo, and A. Farina, “A tutorial on bernoulli filters: theory, implementation and applications,” _IEEE Transactions on Signal Processing_ , vol. 61, no. 13, pp. 3406–3430, 2013. 

- [82] A.<sup>´</sup> F. Garc´ıa-Fern´andez, J. L. Williams, K. Granstr¨om, and L. Svensson, “Poisson multi-bernoulli mixture filter: Direct derivation and implementation,” _IEEE Transactions on Aerospace and Electronic Systems_ , vol. 54, no. 4, pp. 1883–1901, 2018. 

- [83] M. Kaess, H. Johannsson, R. Roberts, V. Ila, J. Leonard, and F. Dellaert, “isam2: Incremental smoothing and mapping with fluid relinearization and incremental variable reordering,” in _2011 IEEE international conference on robotics and automation_ . IEEE, 2011, pp. 3281–3288. 

- [84] R. K¨ummerle, G. Grisetti, H. Strasdat, K. Konolige, and W. Burgard, “G2o: A general framework for graph optimization,” Jun. 2011, pp. 3607– 3613. 

- [85] J. Morris, Y. Wang, and V. Ila, “The Importance of Coordinate Frames in Dynamic SLAM,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . Yokohama, Japan: IEEE, May 2024, pp. 13 755–13 761. [Online]. Available: https://ieeexplore.ieee.org/document/10610840/ 

- [86] J. Mullane, B.-N. Vo, M. D. Adams, and B.-T. Vo, “A random-finite-set approach to bayesian slam,” _IEEE transactions on robotics_ , vol. 27, no. 2, pp. 268–282, 2011. 

- [87] P. M. Siew, R. Linares, and V. Bageshwar, “Simultaneous localization and mapping with moving object tracking in 3d range data using probability hypothesis density (phd) filter,” in _2018 AIAA Information Systems-AIAA Infotech@ Aerospace_ , 2018, p. 0507. 

- [88] K. Granstr¨om, M. Fatemi, and L. Svensson, “Poisson multi-bernoulli mixture conjugate prior for multiple extended target filtering,” _IEEE Transactions on Aerospace and Electronic Systems_ , vol. 56, no. 1, pp. 208–225, 2019. 

- [89] H. Deusch, S. Reuter, and K. Dietmayer, “The labeled multi-bernoulli slam filter,” _IEEE Signal Processing Letters_ , vol. 22, no. 10, pp. 1561–1565, 2015. 

- [90] S. Reuter, B.-T. Vo, B.-N. Vo, and K. Dietmayer, “The labeled multi-bernoulli filter,” _IEEE Transactions on Signal Processing_ , vol. 62, no. 12, pp. 3246–3260, 2014. 

- [91] H. Kim, K. Granstr¨om, L. Svensson, S. Kim, and H. Wymeersch, “Pmbm-based slam filters in 5g mmwave vehicular networks,” _IEEE Transactions on Vehicular Technology_ , vol. 71, no. 8, pp. 8646– 8661, 2022. 

- [92] Y. Ge, O. Kaltiokallio, Y. Xia, A.<sup>´</sup> F. Garc´ıaFern´andez, H. Kim, J. Talvitie, M. Valkama, H. Wymeersch, and L. Svensson, “Batch slam with pmbm data association sampling and graphbased optimization,” _IEEE Transactions on Signal Processing_ , 2025. 

- [93] Q. Li, R. Gan, J. Liang, and S. J. Godsill, “An adaptive and scalable multi-object tracker based on the non-homogeneous poisson process,” _IEEE Transactions on Signal Processing_ , vol. 71, pp. 105–120, 2023. 

- [94] J. Chen and P. Dames, “Multi-class target tracking using the semantic phd filter,” in _The International Symposium of Robotics Research_ . Springer, 2019, pp. 526–541. 

- [95] S. Ejaz, M. Giberna, M. Shaheer, J. A. MillanRomera, A. Tourani, P. Kremer, H. Voos, and J. L. Sanchez-Lopez, “Situationally-aware path planning exploiting 3d scene graphs,” 2025. [Online]. Available: https://arxiv.org/abs/2508. 06283 

- [96] V. K. Viswanathan, M. A. V. Saucedo, S. G. Satpute, C. Kanellakis, and G. Nikolakopoulos, “xflie: Leveraging actionable hierarchical scene representations for autonomous semantic-aware inspection missions,” 2024. [Online]. Available: https://arxiv.org/abs/2412.19571 

- [97] V. K. Viswanathan, A. Patel, M. A. V. Saucedo, S. Satpute, C. Kanellakis, and G. Nikolakopoulos, “Spade: Towards scalable path planning architecture on actionable multi-domain 

31 

3d scene graphs,” 2025. [Online]. Available: https://arxiv.org/abs/2505.19098 

- [98] A. Ray, C. Bradley, L. Carlone, and N. Roy, “Task and motion planning in hierarchical 3d scene graphs,” 2024. [Online]. Available: https://arxiv.org/abs/2403.08094 

- [99] Z. Ravichandran, L. Peng, N. Hughes, J. D. Griffith, and L. Carlone, “Hierarchical Representations and Explicit Memory: Learning Effective Navigation Policies on 3D Scene Graphs using Graph Neural Networks,” _arXiv:2108.01176 [cs]_ , Aug. 2021, arXiv: 2108.01176. [Online]. Available: http://arxiv.org/abs/2108.01176 

- [100] H. Yin, X. Xu, Z. Wu, J. Zhou, and J. Lu, “Sgnav: Online 3d scene graph prompting for llmbased zero-shot object navigation,” _arXiv preprint arXiv:2410.08189_ , 2024. 

- [101] A. Geiger, P. Lenz, and R. Urtasun, “Are we ready for autonomous driving? The KITTI vision benchmark suite,” in _2012 IEEE Conference on Computer Vision and Pattern Recognition_ . Providence, RI: IEEE, Jun. 2012, pp. 3354–3361. [Online]. Available: http://ieeexplore.ieee.org/ document/6248074/ 

- [102] R. Tian, Y. Zhang, L. Yang, J. Zhang, S. Coleman, and D. Kerr, “DynaQuadric: Dynamic Quadric SLAM for Quadric Initialization, Mapping, and Tracking,” _IEEE Transactions on Intelligent Transportation Systems_ , vol. 25, no. 11, pp. 17 234–17 246, Nov. 2024. [Online]. Available: https://ieeexplore.ieee.org/document/10591477/ 

- [103] H. Caesar, V. Bankiti, A. H. Lang, S. Vora, V. E. Liong, Q. Xu, A. Krishnan, Y. Pan, G. Baldan, and O. Beijbom, “nuScenes: A multimodal dataset for autonomous driving,” 2019, version Number: 5. [Online]. Available: https://arxiv.org/abs/1903.11027 

- [104] A. Geiger, P. Lenz, C. Stiller, and R. Urtasun, “Vision meets robotics: The KITTI dataset,” _The International Journal of Robotics Research_ , vol. 32, no. 11, pp. 1231–1237, Sep. 2013. [Online]. Available: https://journals.sagepub.com/doi/10. 1177/0278364913491297 

- [105] M. Henein, J. Zhang, R. Mahony, and V. Ila, “Dynamic SLAM: The Need For Speed,” 2020, version Number: 2. [Online]. Available: https: //arxiv.org/abs/2002.08584 

- [106] J. E. Guivant, F. R. Masson, and E. M. Nebot, “Simultaneous localization and map building using natural features and absolute information,” _Robotics and Autonomous Systems_ , vol. 40, no. 2-3, pp. 79–90, Aug. 2002. [Online]. Available: https://linkinghub.elsevier. com/retrieve/pii/S0921889002002336 

- [107] R. Ram´on-Vigo, J. P´erez, F. Caballero, and L. Merino, “Navigating among people in crowded environment: Datasets for localization and human robot interaction,” in _Proceedings of the Workshop on Robots in Clutter: Perception and Interaction in Clutter, IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2014. 

- [108] X. Shi, D. Li, P. Zhao, Q. Tian, Y. Tian, Q. Long, C. Zhu, J. Song, F. Qiao, L. Song, Y. Guo, Z. Wang, Y. Zhang, B. Qin, W. Yang, F. Wang, R. H. M. Chan, and Q. She, “Are We Ready for Service Robots? The OpenLORIS-Scene Datasets for Lifelong SLAM,” 2019, version Number: 2. [Online]. Available: https://arxiv.org/abs/1911.05603 

- [109] Y. Wang, Y. Zhang, L. Hu, W. Wang, G. Ge, and S. Tan, “A Semantic Topology Graph to Detect Re-Localization and Loop Closure of the Visual Simultaneous Localization and Mapping System in a Dynamic Environment,” _Sensors_ , vol. 23, no. 20, p. 8445, Oct. 2023. [Online]. Available: https://www.mdpi.com/1424-8220/23/20/8445 

- [110] P. Ding, W. Wang, X. Wu, K. Xu, D. Wu, and Z. Du, “Dynamic SLAM by Combining Rigid Feature Point Set Modeling and YOLO,” _Sensors_ , vol. 26, no. 1, p. 235, Dec. 2025. [Online]. Available: https://www.mdpi.com/1424-8220/ 26/1/235 

- [111] A. Dai, A. X. Chang, M. Savva, M. Halber, T. Funkhouser, and M. Nießner, “ScanNet: Richly-annotated 3D Reconstructions of Indoor Scenes,” 2017, version Number: 2. [Online]. Available: https://arxiv.org/abs/1702.04405 

- [112] A. Chang, A. Dai, T. Funkhouser, M. Halber, M. Nießner, M. Savva, S. Song, A. Zeng, and Y. Zhang, “Matterport3D: Learning from RGB-D Data in Indoor Environments,” _arXiv:1709.06158 [cs]_ , Sep. 2017, arXiv: 1709.06158. [Online]. Available: http://arxiv.org/abs/1709.06158 

- [113] J. Sturm, N. Engelhard, F. Endres, W. Burgard, and D. Cremers, “A benchmark for the evaluation of RGB-D SLAM systems,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . Vilamoura-Algarve, Portugal: IEEE, Oct. 2012, pp. 573–580. [Online]. Available: http://ieeexplore.ieee.org/document/6385773/ 

- [114] E. Palazzolo, J. Behley, P. Lottes, P. Gigu`ere, and C. Stachniss, “ReFusion: 3D Reconstruction in Dynamic Environments for RGB-D Cameras Exploiting Residuals,” 2019. [Online]. Available: https://www.ipb.uni-bonn.de/pdfs/ palazzolo2019iros.pdf 

- [115] S. Cheng, C. Sun, S. Zhang, and D. Zhang, “Sgslam: A real-time rgb-d visual slam toward dynamic scenes with semantic and geometric information,” _IEEE Transactions on Instrumentation and Measurement_ , vol. 72, pp. 1–12, 2022. 

32 

- [116] K. M. Judd and J. D. Gammell, “The Oxford Multimotion Dataset: Multiple SE(3) Motions With Ground Truth,” _IEEE Robotics and Automation Letters_ , vol. 4, no. 2, pp. 800– 807, Apr. 2019. [Online]. Available: https: //ieeexplore.ieee.org/document/8610209/ 

- [117] Z. Ravichandran, J. D. Griffith, B. Smith, and C. Frost, “Bridging Scene Understanding and Task Execution with Flexible Simulation Environments,” 2020, version Number: 1. [Online]. Available: https://arxiv.org/abs/2011. 10452 

- [118] X. Puig, K. Ra, M. Boben, J. Li, T. Wang, S. Fidler, and A. Torralba, “VirtualHome: Simulating Household Activities via Programs,” 2018, version Number: 1. [Online]. Available: https://arxiv.org/abs/1806.07011 

- [119] M. Patel and S. Chernova, “Proactive Robot Assistance via Spatio-Temporal Object Modeling,” 2022, version Number: 1. [Online]. Available: https://arxiv.org/abs/2211.15501 

- [120] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun, “CARLA: An Open Urban Driving Simulator,” 2017, version Number: 1. [Online]. Available: https://arxiv.org/abs/1711.03938 

- [121] A. Kurenkov, M. Lingelbach, T. Agarwal, E. Jin, C. Li, R. Zhang, L. Fei-Fei, J. Wu, S. Savarese, and R. Mart´ın-Mart´ın, “Modeling Dynamic Environments with Scene Graph Memory,” in _Proceedings of the 40th International Conference on Machine Learning_ , ser. Proceedings of Machine Learning Research, A. Krause, E. Brunskill, K. Cho, B. Engelhardt, S. Sabato, and J. Scarlett, Eds., vol. 202. PMLR, Jul. 2023, pp. 17 976– 17 993. [Online]. Available: https://proceedings. mlr.press/v202/kurenkov23a.html 

- [122] K. Minoda, F. Schilling, V. W¨uest, D. Floreano, and T. Yairi, “VIODE: A simulated dataset to address the challenges of visual-inertial odometry in dynamic environments,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 2, pp. 1343–1350, 2021. 

- [123] W. Wang, D. Zhu, X. Wang, Y. Hu, Y. Qiu, C. Wang, Y. Hu, A. Kapoor, and S. Scherer, “Tartanair: A dataset to push the limits of visual slam,” 2020. 

- [124] N. Gorlo, L. Schmid, and L. Carlone, “Describe Anything Anywhere At Any Moment,” 2025, version Number: 1. [Online]. Available: https: //arxiv.org/abs/2512.00565 

- [125] M. Vega Torres, A. Braun, and A. Borrmann, “OGM2PGBM: Robust BIM-based 2D-LiDAR localization for lifelong indoor navigation,” in _ECPPM 2022 - eWork and eBusiness in Architecture, Engineering and Construction 2022_ , 1st ed. London: CRC Press, Mar. 

2023, pp. 567–574. [Online]. Available: https: //www.taylorfrancis.com/books/9781003354222/ chapters/10.1201/9781003354222-72 

- [126] S. M. Ferraina, M. Brienza, F. Argenziano, E. Musumeci, V. Suriani, D. D. Bloisi, and D. Nardi, “LOST-3DSG: Lightweight OpenVocabulary 3D Scene Graphs with Semantic Tracking in Dynamic Environments,” 2026, version Number: 1. [Online]. Available: https: //arxiv.org/abs/2601.02905 

- [127] A. Rosinol, M. Abate, Y. Chang, and L. Carlone, “Kimera: An Open-Source Library for RealTime Metric-Semantic Localization and Mapping,” _Proceedings - IEEE International Conference on Robotics and Automation_ , pp. 1689–1696, 2020. 

- [128] S. Linok, V. Semenov, A. Trunova, O. Bulichev, and D. Yudin, “DyGEnc: Encoding a Sequence of Textual Scene Graphs to Reason and Answer Questions in Dynamic Scenes,” May 2025, arXiv:2505.03581 [cs]. [Online]. Available: http: //arxiv.org/abs/2505.03581 

- [129] L. Maguire, M. Van, K. Olayemi, and S. McLoone, “LiDAR-Only Navigation of UGVs in Dynamic Environments via Graph Attention Networks and Deep Reinforcement Learning,” in _2025 IEEE International Conference on Mechatronics (ICM)_ . Wollongong, Australia: IEEE, Feb. 2025, pp. 1–6. [Online]. Available: https: //ieeexplore.ieee.org/document/10934926/ 

- [130] S. Chen, H. Guo, S. Zhu, F. Zhang, Z. Huang, J. Feng, and B. Kang, “Video depth anything: Consistent depth estimation for super-long videos,” _arXiv:2501.12375_ , 2025. 

- [131] M. Bloesch, J. Czarnowski, R. Clark, S. Leutenegger, and A. J. Davison, “Codeslam—learning a compact, optimisable representation for dense visual slam,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2018, pp. 2560–2568. 

- [132] N. Yang, L. v. Stumberg, R. Wang, and D. Cremers, “D3vo: Deep depth, deep pose and deep uncertainty for monocular visual odometry,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2020, pp. 1281–1292. 

- [133] J. A. Millan-Romera, H. Bavle, M. Shaheer, M. R. Oswald, H. Voos, and J. L. SanchezLopez, “Learning High-level Semantic-Relational Concepts for SLAM,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 9803–9810. 

- [134] S. Yang and S. Scherer, “CubeSLAM: Monocular 3-D Object SLAM,” _IEEE Transactions on Robotics_ , vol. 35, no. 4, pp. 925–938, 2019. 

33 

- [135] B. Kerbl, G. Kopanas, T. Leimk¨uhler, and G. Drettakis, “3D Gaussian Splatting for RealTime Radiance Field Rendering,” Aug. 2023, arXiv:2308.04079 [cs]. [Online]. Available: http: //arxiv.org/abs/2308.04079 

- [136] H. Matsuki, R. Murai, P. H. J. Kelly, and A. J. Davison, “Gaussian Splatting SLAM,” Apr. 2024, arXiv:2312.06741 [cs]. [Online]. Available: http://arxiv.org/abs/2312.06741 

- [137] J. Zheng, Z. Zhu, V. Bieri, M. Pollefeys, S. Peng, and I. Armeni, “Wildgs-slam: Monocular gaussian splatting slam in dynamic environments,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025, pp. 11 461–11 471. 

- [138] R. B. Li, M. Shaghaghi, K. Suzuki, X. Liu, V. Moparthi, B. Du, W. Curtis, M. Renschler, K. M. B. Lee, N. Atanasov _et al._ , “Dynagslam: Real-time gaussian-splatting slam for online rendering, tracking, motion predictions of moving objects in dynamic scenes,” in _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , 2026, pp. 2434–2444. 

- [139] Y. Xu, H. Jiang, Z. Xiao, J. Feng, and L. Zhang, “Dg-slam: Robust dynamic gaussian splatting slam with hybrid pose optimization,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 51 577–51 596, 2024. 

- [140] M. Fernandez-Cortizas, H. Bavle, D. Perez-Saura, J. L. Sanchez-Lopez, P. Campoy, and H. Voos, “Multi S-Graphs: An Efficient Distributed Semantic-Relational Collaborative SLAM,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 6, pp. 6004–6011, Jun. 2024, conference Name: IEEE Robotics and Automation Letters. [Online]. Available: https://ieeexplore.ieee.org/document/ 10529513/?arnumber=10529513 

34 

