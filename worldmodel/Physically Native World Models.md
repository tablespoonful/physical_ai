---
title: "Physically Native World Models: A Hamiltonian Perspective on Generative World Modeling"
date: "2026-05-01"
authors: "Sen Cui; Jingheng Ma"
url: https://arxiv.org/abs/2605.00412
pdf: https://arxiv.org/pdf/2605.00412
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.00412)** / [論文ページ](https://arxiv.org/abs/2605.00412)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Physically Native World Models: A Hamiltonian Perspective on Generative World Modeling** 

**Sen Cui**<sup>_∗_</sup> 

Tsinghua University 

**Jingheng Ma** Tsinghua University 

## **Abstract** 

World models have recently re-emerged as a central paradigm for embodied intelligence, robotics, autonomous driving, and model-based reinforcement learning. However, current world model research is often dominated by three partially separated routes: 2D video-generative models that emphasize visual future synthesis, 3D scene-centric models that emphasize spatial reconstruction, and JEPAlike latent models that emphasize abstract predictive representations. While each route has made important progress, they still struggle to provide physically reliable, action-controllable, and long-horizon stable predictions for embodied decision making. In this paper, we argue that the bottleneck of world models is no longer only whether they can generate realistic futures, but whether those futures are physically meaningful and useful for action. We propose _Hamiltonian World Models_ as a physically grounded perspective on world modeling. The key idea is to encode observations into a structured latent phase space, evolve the latent state through Hamiltonian-inspired dynamics with control, dissipation, and residual terms, decode the predicted trajectory into future observations, and use the resulting rollouts for planning. We discuss how Hamiltonian structure may improve interpretability, data efficiency, and long-horizon stability, while also noting practical challenges in real-world robotic scenes involving friction, contact, nonconservative forces, and deformable objects. 

## **1 Introduction** 

The idea of learning internal simulators has regained prominence as a unifying objective across embodied AI, robotics, and decision making. This renewed interest is driven by two converging trends. First, large-scale foundation models have demonstrated strong semantic competence in language, vision, and multimodal reasoning [Radford et al., 2021, Alayrac et al., 2022, OpenAI, 2023, Driess et al., 2023, Brohan et al., 2023]. Second, embodied agents require predictive models that go beyond recognizing the current scene: they must anticipate how the world will change under their own actions. A robot, for example, should not only identify an object, but also predict whether pushing, grasping, or releasing it will lead to stable manipulation, collision, or task failure. This makes world modeling a natural bridge between perception, prediction, and decision making. 

The classical motivation for world models is to provide an internal simulator of the environment, enabling agents to imagine possible futures before acting. Early work showed that learned latent models can support control by compressing observations into compact predictive representations [Ha and Schmidhuber, 2018]. Model-based reinforcement learning further demonstrated that agents can plan or optimize policies inside learned latent dynamics, reducing the need for costly real environment interaction [Hafner et al., 2019, 2020, 2023]. In robotics, visual foresight and video prediction have been used to evaluate candidate actions before execution [Finn and Levine, 2017, Ebert et al., 2018]. In autonomous driving and interactive simulation, generative world models such as 

> _∗_ Corresponding author. Email: cuis@mail.tsinghua.edu.cn 

Preprint. 

GAIA-1 and Genie suggest that future scene generation can be conditioned on actions, text, or latent controls [Hu et al., 2023, Bruce et al., 2024]. Together, these developments have made “generating the future” an increasingly important research direction. 

However, generating future video is not equivalent to understanding the physical world. Modern video generative models can synthesize visually plausible sequences, but visual plausibility alone does not guarantee physical validity. A generated trajectory may look realistic over a short horizon while gradually violating object permanence, contact consistency, momentum conservation, or action-effect causality. This distinction is especially important for robotics and autonomous systems, where an incorrect future prediction can directly mislead planning and execution. For entertainmentoriented video synthesis, perceptual realism may be sufficient; for embodied decision making, the predicted future must also be dynamically feasible, controllable, and reliable. 

A key limitation of many current video world models is that their temporal evolution is learned through highly expressive but weakly constrained neural sequence models. In a typical latent formulation, the future state is predicted as 


where _zt_ is a learned latent state and _at_ is an action. Although this formulation is flexible and compatible with recurrent latent dynamics, diffusion-based video predictors, Transformers, and structured state-space models [Ha and Schmidhuber, 2018, Hafner et al., 2019, Ho et al., 2022, Blattmann et al., 2023, Vaswani et al., 2017, Gu et al., 2022, Gu and Dao, 2023], it does not specify what physical quantities the latent state represents or what structure the transition should preserve. As a result, the model may learn short-term correlations in pixel or latent space without acquiring stable physical dynamics. This often leads to compounding errors, long-horizon drift, poor out-of-distribution generalization, and high data requirements. 

This limitation suggests that the bottleneck of world models is no longer only visual fidelity. The more fundamental question is whether the generated future is physically coherent and useful for action. A world model should not merely predict what the next frames look like; it should represent how objects, agents, and their interactions evolve under interventions. Prior work on model-based control and robotic video prediction has already shown the practical value of imagined rollouts for planning [Finn and Levine, 2017, Ebert et al., 2018, Hafner et al., 2020, 2023]. Yet for such rollouts to support reliable decision making, the latent dynamics must be stable, interpretable, and constrained by the regularities of the physical world. 

We therefore argue that the next stage of world model research should move from visual generation toward physical structure modeling. In this view, video generation is an observation-level interface, while the core of a world model is its latent dynamics. The internal state should encode entities, relations, controllable variables, and physically meaningful structure; the transition should reflect constraints such as geometry, energy, contact, and action-conditioned causality; and the generated future should be treated as a rendering of an underlying state evolution. This perspective is consistent with broader efforts in structured dynamics learning, object-centric representation learning, and physics-informed machine learning [Battaglia et al., 2016, Greydanus et al., 2019, Toth et al., 2020, Raissi et al., 2019, Sanchez-Gonzalez et al., 2020, Kipf et al., 2020]. 

Motivated by this perspective, we propose to rethink world models through the lens of Hamiltonian dynamics. Hamiltonian mechanics provides a principled framework for describing physical evolution in phase space through generalized coordinates, momenta, and an energy function. Rather than asking a video model to discover physical laws purely from data, a Hamiltonian world model leverages energy-based dynamics in a learned phase space to govern latent evolution. This offers a path toward world models that are not only generative, but also physically interpretable, data-efficient, and stable under long-horizon rollout. 

## **2 Existing Three Routes Toward World Models** 

World model research has recently developed along several partially overlapping but conceptually distinct routes. In this paper, we group current approaches into three representative paradigms: _2D video-generative world models_ , _3D scene-centric world models_ , and _JEPA-like latent world models_ . This classification is not meant to be exhaustive, but it clarifies what different routes primarily optimize for. The 2D video route emphasizes future observation synthesis, the 3D route emphasizes 

2 

spatial and geometric reconstruction, and the JEPA-like route emphasizes predictive abstraction in latent representation space. 

**2D video-generative world models.** The first route treats world modeling as conditional future video generation. Given past observations, actions, language, maps, or other conditioning signals, the model predicts future visual observations: _pθ_ ( _ot_ +1: _t_ + _H | o≤t, at_ : _t_ + _H−_ 1 _, c_ ), where _ot_ denotes an observation, _at_ denotes an action or control input, and _c_ denotes additional context. This route is closely related to recent advances in video diffusion and latent video generation, which have significantly improved the quality and temporal coherence of generated videos [Ho et al., 2022, Blattmann et al., 2023]. In world modeling, GAIA-1 formulates autonomous driving world modeling as controllable generative sequence modeling over video, text, and action inputs [Hu et al., 2023], while Genie demonstrates that action-controllable interactive environments can be learned from large-scale videos [Bruce et al., 2024]. The strength of this route is that it provides an intuitive observation-level interface: the future is represented in the same visual space in which agents perceive the world. Its limitation is that a video may look realistic while still violating contact, momentum, action-effect consistency, or long-horizon stability. 

**3D scene-centric world models.** The second route emphasizes explicit spatial structure. Instead of representing the world primarily as a sequence of 2D frames, 3D scene-centric models aim to recover geometry-aware representations that support novel view synthesis, reconstruction, and spatial reasoning. Neural Radiance Fields model scenes as continuous volumetric radiance fields and have become a foundation for view-consistent scene representation [Mildenhall et al., 2020]. 3D Gaussian Splatting further improves real-time rendering efficiency and visual quality using explicit 3D Gaussian primitives [Kerbl et al., 2023]. This route is important because embodied agents must operate in three-dimensional space, and purely 2D video prediction may fail to capture view consistency, occlusion structure, and metric geometry. However, 3D reconstruction alone is not yet a complete world model. Many 3D scene representations are better suited to static or quasi-static reconstruction than to action-conditioned physical evolution. They can answer where objects are and how a scene looks from another view, but they do not necessarily answer how objects move, collide, deform, or respond to robot actions. 

**JEPA-like latent world models.** The third route focuses on predictive representation learning in latent space. Instead of reconstructing pixels, Joint-Embedding Predictive Architectures learn to predict abstract representations of missing or future inputs [Assran et al., 2023, Bardes et al., 2024]. This design is motivated by the idea that intelligent systems should predict high-level features rather than every low-level pixel. Compared with pixel-level generation, latent prediction can be more compact, more scalable, and less dominated by irrelevant visual details. This makes JEPA-like models attractive as a route toward abstract world representations. However, because these models are primarily designed for representation learning rather than explicit physical simulation, their latent variables are not necessarily aligned with physical quantities such as position, velocity, momentum, energy, or contact constraints. Therefore, while JEPA-like models may provide strong predictive abstractions, additional structure is needed if such representations are to support physically grounded planning and control. 

## **3 Limitations of Current World Models** 

Despite rapid progress, current world models still face several fundamental limitations when used for embodied decision making. These limitations do not simply reflect insufficient model scale or visual quality; rather, they may reveal a deeper mismatch between generating plausible observations and modeling physically reliable world dynamics. 

**Visual fidelity does not guarantee physical validity.** As noted above, video world models optimize perceptual realism more directly than physical consistency. This becomes critical in robotics and autonomous driving, where a generated future is useful only if it corresponds to a dynamically feasible outcome. 

**Data efficiency remains limited when physical priors are absent.** A purely data-driven world model must infer physical regularities from observed trajectories. This can require large and di- 

3 

verse datasets covering different objects, masses, contacts, materials, actions, and environmental conditions. In robotics, such data are expensive to collect, and unsafe exploration may be impractical. Model-based learning improves sample efficiency by reusing imagined trajectories [Ha and Schmidhuber, 2018, Hafner et al., 2020, 2023], but the quality of this advantage depends on the reliability of the learned model. 

**Latent transitions are often weakly structured.** Many latent world models represent dynamics with a generic neural transition that is learned end-to-end. This has been successful in model-based reinforcement learning [Hafner et al., 2019, 2020, 2023], but it does not specify what physical quantities the latent variables encode or what structure the transition should preserve. As a result, the latent state may entangle appearance, semantics, motion, and task-specific features without representing coordinates, velocities, momenta, forces, or constraints. Many modern video world models still rely primarily on high-capacity sequence modeling rather than explicit physical structure. 

**Long-horizon rollout remains vulnerable to compounding errors.** World models are most valuable when they can be rolled out over multiple steps for planning. Yet learned dynamics models are well known to suffer from compounding prediction errors: small one-step inaccuracies may accumulate and produce unreliable long-horizon trajectories [Talvitie, 2017, Janner et al., 2019]. This issue is especially severe when the model is queried on states or actions outside the training distribution during planning. 

**Generated futures are not always aligned with action usefulness.** A world model for embodied intelligence should support action selection, not merely future synthesis. Visual foresight methods explicitly use action-conditioned video prediction for model predictive control [Finn and Levine, 2017, Ebert et al., 2018], while latent imagination methods train policies from predicted trajectories [Hafner et al., 2020, 2023]. These works show that imagined futures can be useful for control, but they also reveal a key requirement: the prediction must preserve the causal effect of actions. If a model generates visually coherent futures that are weakly conditioned on actions, or if it fails to distinguish feasible from infeasible action outcomes, it becomes unreliable for planning. This limitation is particularly important for contact-rich manipulation, where small differences in force, momentum, or contact geometry can determine task success. 

## **4 Redefining World Models for Embodied Intelligence** 

The limitations of current world models suggest that the concept itself needs to be sharpened. We hypothesize a world model as a structured, action-conditioned, data-efficient, and physically grounded generative dynamical system that represents the current world state, predicts how it evolves under interventions, and supports reliable decision making. This definition is broader than classical latent dynamics models [Ha and Schmidhuber, 2018, Hafner et al., 2019, 2020, 2023], but also more constrained than generic video generation models [Ho et al., 2022, Blattmann et al., 2023, Hu et al., 2023, Bruce et al., 2024]. We do not claim these properties are universally necessary for all world modeling tasks; rather, we argue that their combination provides a useful design target for physically situated agents, and that Hamiltonian dynamics offers one principled way to satisfy them. 

**Physical grounding.** For physical agents, not every visually plausible future is dynamically feasible. A world model should respect physical regularities such as geometry, contact, inertia, energy variation, and interaction constraints. This does not mean that the model must be a hand-coded simulator. Rather, it should incorporate physical structure as an inductive bias in its representation, transition, or objective. For world models, physical grounding is especially important because imagined trajectories may be directly used for planning and control. 

**Data-efficient through physical priors.** Purely data-driven video or latent prediction can therefore become inefficient when the model must infer basic physical structure only from observed trajectories. A more scalable world model should incorporate physical priors that constrain the hypothesis space of possible dynamics. Physical priors may take the form of structured representations, relational inductive biases, geometric constraints, energy-based dynamics, or physics-informed objectives.[Battaglia et al., 2016, Sanchez-Gonzalez et al., 2020, Raissi et al., 2019, Greydanus et al., 2019, Cranmer et al., 2020]. For embodied world modeling, data efficiency should therefore be 

4 

treated as a core design requirement: the model should learn from data, but it should not require data to rediscover every basic law of physical interaction. 

**Compositional structure.** The physical world is compositional: objects, agents, tools, surfaces, and constraints interact through relations. A world model should therefore avoid representing the entire scene as an unstructured global vector whenever possible. Instead, it should encode entities and their interactions through structured latent variables, 


where each latent component may correspond to an object, an agent, or a dynamically relevant part of the scene. This view is supported by object-centric representation learning, interaction networks, and graph-based physical simulators, which show that relational structure improves generalization in physical domains [Battaglia et al., 2016, Sanchez-Gonzalez et al., 2020, Kipf et al., 2020]. A structured world model is easier to inspect and compose, and more suitable for modeling physical interactions than a monolithic latent representation. 

**Temporal consistency under rollout.** A static representation of the scene is insufficient for embodied agents. The defining property of a world model is its ability to roll the world forward: 


where _Tθ_ denotes a learned transition and _at_ denotes an action or intervention. This transitioncentric view is central to model-based reinforcement learning and planning [Sutton, 1991, Hafner et al., 2019, 2020, Schrittwieser et al., 2020, Hafner et al., 2023]. However, for embodied intelligence, evolvability should mean more than one-step prediction. A useful world model must remain stable under multi-step rollout, generalize beyond the training distribution, and preserve the relevant structure of the environment over time. 

**Causal action conditioning.** Embodied agents do not passively observe the world; they intervene in it. Therefore, a world model must answer counterfactual questions of the form: what will happen if the agent executes action _at_ ? Formally, the model should estimate 


or, at the latent level, 


This requirement distinguishes embodied world modeling from passive video prediction. Robotic visual foresight and latent imagination methods have demonstrated that action-conditioned prediction can support planning and policy learning [Finn and Levine, 2017, Ebert et al., 2018, Hafner et al., 2020, 2023]. Without strong action conditioning, a model may generate plausible futures but fail to represent the causal consequences of the agent’s choices. 

We therefore summarize these requirements compactly: 


where _Eθ_ encodes observations, _Tθ_ evolves latent dynamics, _Dθ_ renders future observations, and _U_ evaluates decision utility. This formulation separates four roles that are often conflated: perception, dynamics, generation, and planning. 

## **5 Physical Backbone: Hamiltonian Dynamics for World Models** 

If the core of a world model is its latent dynamics, then the choice of dynamical structure becomes central. For embodied intelligence, a useful world model should not only predict future observations, but also represent how physical states evolve under constraints, interactions, and interventions. Hamiltonian mechanics offers a natural candidate for such a backbone because it describes physical evolution through phase-space variables, energy functions, and structure-preserving dynamics. This makes it particularly suitable for rethinking world models as physically grounded generative dynamical systems rather than unconstrained video predictors. 

5 

**Phase space provides a natural latent state.** Many video world models rely on latent variables whose physical meaning is unclear. Hamiltonian mechanics instead begins with a structured state representation: 


where _qt_ denotes generalized coordinates and _pt_ denotes generalized momenta. This phase-space view is well aligned with the needs of embodied world modeling: an agent must reason not only about where objects are, but also about how they are moving and how they may respond to future actions. Prior work on Hamiltonian Neural Networks and Hamiltonian Generative Networks shows that phase-space structure can provide useful inductive bias for learning dynamics, including from high-dimensional observations [Greydanus et al., 2019, Toth et al., 2020]. Compared with an unstructured latent vector, a phase-space latent state makes the transition model more interpretable and more directly connected to physical evolution. 

**Energy functions induce structured dynamics.** A key strength of Hamiltonian modeling is that the dynamics are derived from a scalar energy function rather than predicted by an arbitrary vector field. Given a Hamiltonian _H_ ( _q, p_ ), the evolution follows 


Equivalently, with _z_ = [ _q, p_ ], 


This formulation changes the learning problem: instead of directly fitting _zt_ +1 = _fθ_ ( _zt, at_ ), the model learns an energy landscape that generates dynamics through its gradients. HNNs demonstrate that this design can improve generalization over unconstrained neural dynamics in physical systems [Greydanus et al., 2019]. For world models, this suggests a principled way to constrain latent transitions so that future rollouts are guided by physical structure rather than short-term statistical correlation alone. 

**Hamiltonian structure supports long-horizon stability.** World models are useful only if their rollouts remain reliable over multiple steps. However, generic learned dynamics often suffer from compounding errors and long-horizon drift [Talvitie, 2017, Janner et al., 2019]. Hamiltonian systems provide a different bias: their dynamics preserve phase-space structure, and when combined with symplectic integration, they can maintain more stable qualitative behavior over long rollouts. Structure-preserving numerical methods have long been used for physical simulation [Hairer et al., 2006]. Recent neural approaches, including Hamiltonian Neural Networks [Greydanus et al., 2019], Hamiltonian Generative Networks [Toth et al., 2020], and Symplectic ODE-Net [Zhong et al., 2020], further show that related structure-preserving principles can be incorporated into learned dynamics. This is especially relevant for embodied planning, where small errors in early imagined states may otherwise lead to unreliable action choices. 

**Physical priors improve data efficiency.** As argued in Section 4, physical priors are essential for data efficiency[Raissi et al., 2019, Battaglia et al., 2016, Sanchez-Gonzalez et al., 2020, Greydanus et al., 2019, Cranmer et al., 2020]. Hamiltonian dynamics specifically reduce the learning burden by replacing unconstrained local transitions with a global energy landscape; rather than fitting trajectories independently, the model learns a single structure that generalizes across initial conditions. 

**Hamiltonian dynamics makes latent evolution more interpretable.** Interpretability is important for world models because their predictions may be used for planning, safety checking, or failure diagnosis. In an unconstrained latent transition, it is often unclear whether prediction errors arise from perception, dynamics, control conditioning, or rendering. A Hamiltonian formulation separates these roles more clearly. The latent variables can be interpreted as phase-space coordinates, the Hamiltonian can be interpreted as an energy-like scalar, and the rollout can be inspected through phase trajectories, energy variation, and interaction terms. Hamiltonian Generative Networks demonstrate that such structure can be learned from pixels, suggesting that physically interpretable latent dynamics need not require direct access to low-dimensional ground-truth states [Toth et al., 2020]. For embodied world models, this interpretability is valuable because it enables diagnosis of whether an imagined future is physically plausible or merely visually plausible. 

6 


Figure 1: Overview of the proposed Hamiltonian World Model (HWM) architecture. **(1) Perception and Encoding:** past observations and actions are encoded into a structured latent phase state; **(2) Hamiltonian Dynamics:** the latent state is evolved through Hamiltonian-inspired dynamics; **(3) Video Generation:** the predicted latent trajectory is decoded into future visual observation; **(4) Planning and Decision:** candidate action sequences are rolled out through the world model. 

**Hamiltonian structure can be extended beyond ideal conservative systems.** A common concern is that real-world robotic scenes are not closed conservative systems. They involve actuation, friction, damping, impacts, contact switches, and unmodeled visual factors. This concern is valid: a useful Hamiltonian world model should not assume perfect energy conservation. Instead, Hamiltonian dynamics should be treated as a structural backbone that can be extended with control and dissipation. Prior work on controlled Hamiltonian dynamics and Symplectic ODE-Net supports the feasibility of incorporating control inputs into Hamiltonian-inspired neural dynamics [Zhong et al., 2020]. This extension is crucial: the goal is not to force the real world into an ideal conservative system, but to use Hamiltonian structure as a physically meaningful inductive bias. 

## **6 An Architectural View of Hamiltonian World Models** 

As we note in Section 5 , for embodied intelligence, the world model must connect perception, dynamics, generation, and decision making. We therefore outline a possible architecture for _Hamiltonian World Models_ : a physically grounded generative dynamical system that encodes visual observations into a structured latent phase space, evolves this state through Hamiltonian-inspired dynamics, renders future observations with a generative decoder, and uses the resulting rollouts for planning. This architecture is not intended to replace existing world models—whether latent dynamics models, which require stable and controllable latent rollouts [Ha and Schmidhuber, 2018, Hafner et al., 2019, 2020, 2023], or video-generative world models, which require physically consistent future synthesis [Hu et al., 2023, Bruce et al., 2024]—but to provide a physical backbone that can improve stability, interpretability, and decision relevance. At a high level, the architecture can be written as 


, shown in Figure 1. Here, _Eθ_ maps past observations into a latent state, _TH_ rolls the state forward under future actions, _Dθ_ renders future observations, and _U_ evaluates the predicted futures for decision making. Such separation is important because modern video generative models can synthesize realistic futures [Ho et al., 2022, Blattmann et al., 2023, Hu et al., 2023, Bruce et al., 2024], but physical reliability depends primarily on the structure of the latent dynamics. 

7 

The first component is a structured latent representation. Instead of compressing the entire scene into a single global vector, a Hamiltonian World Model represents the scene as a set of entity-level phase variables: 


where _qt_<sup>_i_denotes the generalized coordinate of entity</sup><sup>_i_, and</sup><sup>_p_</sup> _t_<sup>_i_denotes its generalized momentum.</sup> The entities may correspond to objects, robot links, tools, surfaces, or dynamically relevant regions. This object-centric representation is motivated by the compositional nature of physical scenes: objects interact through contact, geometry, force, and constraints. Prior work on interaction networks, graph-based simulators, and structured world models suggests that relational representations improve generalization in physical domains [Battaglia et al., 2016, Sanchez-Gonzalez et al., 2020, Kipf et al., 2020]. In the Hamiltonian view, these entity-level variables provide the substrate on which energy and interaction terms can be defined. 

The core transition is governed by a learned Hamiltonian function over the latent phase state: 


A natural parameterization decomposes the Hamiltonian into kinetic, potential, and interaction terms: 


This decomposition gives the latent dynamics a physical interpretation: _Kϕ_ captures motion-related energy, _Uϕ_ captures entity-level potential structure, and _Vϕ_ captures interactions between entities. The dynamics are then induced by Hamilton’s equations: 


Equivalently, with _zt_ = [ _qt, pt_ ], 


This follows the central insight of Hamiltonian Neural Networks and Hamiltonian Generative Networks: the model learns an energy landscape rather than an arbitrary vector field [Greydanus et al., 2019, Toth et al., 2020]. For world modeling, this changes the role of the latent transition from black-box prediction to energy-guided phase-space evolution. 

A practical world model, however, cannot assume that real environments are perfectly conservative. Robotics and embodied interaction involve control inputs, friction, damping, contact switches, non-elastic collisions, and perception uncertainty. Therefore, the Hamiltonian transition should be extended to a controlled-dissipative form: 


The Hamiltonian term provides the physical core, _Rψ_ ( _zt_ ) captures dissipative effects, _Gψ_ ( _zt_ ) _at_ models action-conditioned control, and _ϵψ_ ( _zt, at_ ) accounts for residual phenomena such as contact discontinuities or unmodeled visual dynamics. This design is consistent with prior work on controlled Hamiltonian learning and symplectic neural dynamics [Zhong et al., 2020, Hairer et al., 2006]. The residual term should remain constrained, for example through 


so that the model uses the Hamiltonian structure as the dominant explanation of dynamics rather than degenerating into a generic transition network. 

The predicted latent trajectory is then passed to a video generative decoder: 


Finally, a Hamiltonian World Model should expose a planning interface. Given a set of candidate action sequences _{a_<sup>(</sup> _t_ :<sup>_m_</sup> _t_ +<sup>)</sup> _H−_ 1<sup>_}_</sup> _m_<sup>_M_</sup> =1<sup>, the model can generate latent and visual rollouts:</sup> 


8 


The selected action is then obtained by maximizing a utility function _U_ over predicted futures: 


This is aligned with visual foresight, model predictive control, and latent imagination methods, where predicted futures are used to evaluate candidate behaviors before execution [Camacho and Bordons, 2013, Finn and Levine, 2017, Ebert et al., 2018, Hafner et al., 2020, 2023]. The difference is that the imagined futures are grounded in a structured phase-space rollout rather than produced by an unconstrained video predictor alone. 

The architectural principle is therefore simple: physical evolution and visual rendering should be separated but coupled. The Hamiltonian module provides structured latent dynamics; the video generator provides perceptual detail; the planning module evaluates action usefulness. This makes the model more interpretable than a monolithic video predictor and more suitable for embodied decision making than a purely generative simulator. In this sense, Hamiltonian World Models are not merely video models with a physics-regularized loss; they treat energy-structured latent dynamics as the core mechanism that constrains and guides the generative process. 

## **7 Distinctions and Challenges of Hamiltonian World Models** 

We treat Hamiltonian World Models as a different design perspective on what a world model ought to represent. From the above Section 2, existing paradigms can be roughly grouped into four families. _2D video-generative world models_ treat the world primarily as a stream of future observations to be synthesized [Ho et al., 2022, Blattmann et al., 2023, Hu et al., 2023, Bruce et al., 2024]. _3D scene-centric world models_ emphasize geometry, view consistency, and explicit spatial structure through radiance fields or scene reconstruction [Mildenhall et al., 2020, Kerbl et al., 2023]. _JEPAlike latent world models_ focus on predictive abstraction in representation space rather than pixellevel generation, aiming to learn compact and semantically meaningful predictive features [Assran et al., 2023, Bardes et al., 2024]. By contrast, _Hamiltonian World Models_ treat the world as a physically evolving dynamical system in latent phase space, where future observations are rendered from an underlying energy-structured evolution. 

Table 1 summarizes the main differences. In brief, 2D video-generative models are strong at perceptual realism and flexible conditional generation, but they often lack explicit physical structure and may drift under long rollouts [Hu et al., 2023, Bruce et al., 2024]. 3D scene-centric approaches provide stronger spatial grounding and multi-view consistency, but many are better suited to static or quasi-static scene representation than to action-conditioned long-horizon dynamics [Mildenhall et al., 2020, Kerbl et al., 2023]. While physical reasoning is not their intended goal, JEPA-like latent models are often weakly tied to explicit physical quantities such as momentum, energy, or contact constraints [Assran et al., 2023, Bardes et al., 2024]. Hamiltonian World Models aim to combine the advantages of structured latent prediction and physical inductive bias by modeling the world in phase space, using energy-based transitions that can, in principle, improve stability, interpretability, and data efficiency [Greydanus et al., 2019, Toth et al., 2020, Zhong et al., 2020]. 

**Challenges and boundaries.** Although Hamiltonian World Models offer an appealing physical perspective, their scope and limitations should be stated clearly. First, real embodied environments are not ideal Hamiltonian systems: they involve friction, control inputs, impacts, dissipation, partial observability, and often non-rigid interactions. A practical model must therefore treat Hamiltonian dynamics as a structural prior rather than a literal description of the full world [Zhong et al., 2020, Raissi et al., 2019]. Second, learning phase-space variables from high-dimensional observations remains difficult. Even if a latent state is written as ( _q, p_ ), inferring meaningful coordinates and momenta from pixels is a nontrivial representation learning problem [Toth et al., 2020]. Third, contact-rich manipulation, articulated systems, and deformable objects may require hybrid, graphbased, or event-driven extensions beyond smooth Hamiltonian flow [Battaglia et al., 2016, SanchezGonzalez et al., 2020]. Finally, current evaluation protocols still provide limited evidence about whether a world model has learned reusable physical regularities. This limitation is also a challenge for Hamiltonian World Models: their value cannot be established merely by lower reconstruction error or higher task reward. Without such evaluations, it remains difficult to distinguish a model that exploits task-specific correlations from one that has learned transferable physical dynamics. 

9 

Table 1: Comparison of different world model paradigms. 

|**Paradigm**|**Representation**|**Strength**|**Limitation**|
|---|---|---|---|
|**2D video-generative**<br>**world models**<br>e.g., Video Diffusion Models<br>[Ho et al., 2022], VideoLDM<br>[Blattmann et al., 2023], GAIA-1<br>[Hu et al., 2023], Genie<br>[Bruce et al., 2024]|<br>Image / video<br>sequences|Strong perceptual realism;<br>flexible conditional future<br>synthesis; intuitive<br>observation-level prediction|Weak explicit physical structure;<br>prone to long-horizon drift;<br>action consistency may be fragile|
|**3D scene-centric**<br>**world models**<br>e.g., NeRF<br>[Mildenhall et al., 2020]<br>3D Gaussian Splatting<br>[Kerbl et al., 2023]<br> <br>s|Geometry-aware 3D<br>cene representation|Strong spatial grounding,<br>view consistency, and explicit<br>scene structure|Reconstruction better than<br>dynamics; limited support for<br>action-conditioned physical<br>evolution|
|**JEPA-like latent**<br>**world models**<br>e.g., I-JEPA [Assran et al., 2023]<br>V-JEPA [Bardes et al., 2024]|Predictive latent<br>representation|Compact and abstract<br>prediction; avoids expensive<br>pixel reconstruction;<br>potentially scalable|Latent variables are often weakly<br>tied to explicit physics; limited<br>interpretability for control and<br>dynamics|
|**Hamiltonian /**<br>**physically native**<br>**world models**<br>|Structured latent<br>representation for<br>phase space(_q, p_)|Structured physical inductive<br>bias; improved<br>interpretability; potentially<br>better long-horizon stability<br>and data efficiency|Hard to learn from pixels;<br>real-world dynamics are not fully<br>conservative; contact-rich and<br>deformable phenomena remain<br>difficult|


## **8 Future Directions** 

The broader opportunity is to move from _video world models_ toward _physical world foundation models_ . In this transition, rather than replacing other paradigms, Hamiltonian World Models are viewed as providing a physically grounded axis along which world models can mature. Future systems may combine the perceptual richness of 2D video generation, the spatial grounding of 3D scene representations, the compact abstraction of JEPA-like latent prediction, and the stability of energy-based phase-space dynamics. A critical future direction is to move from scene-level physical rollout to open-ended physical generalization. Future Hamiltonian World Models may not merely model the interactions among entities in a fixed scene, but should learn reusable physical mechanisms that can be composed across unseen objects, materials, embodiments, and tasks. In this sense, the long-term goal is not only a more stable world model, but a physically native foundation model capable of continual physical abstraction, composition, and self-evolution. 

## **References** 

- Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katie Millican, Malcolm Reynolds, Roman Ring, Eliza Rutherford, Serkan Cabi, Tengda Han, Zhitao Gong, Sina Samangooei, Marianne Monteiro, Jacob Menick, Sebastian Borgeaud, Andrew Brock, Aida Nematzadeh, Sahand Sharifzadeh, Mikolaj Binkowski, Ricardo Barreira, Oriol Vinyals, Andrew Zisserman, and Karen Simonyan. Flamingo: A visual language model for few-shot learning. In _Advances in Neural Information Processing Systems_ , volume 35, pages 23716–23736, 2022. 

- Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, and Nicolas Ballas. Self-supervised learning from images with a joint-embedding predictive architecture. _arXiv preprint arXiv:2301.08243_ , 2023. 

- Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mahmoud Assran, and Nicolas Ballas. Revisiting feature prediction for learning visual representations from video, 2024. URL https://arxiv.org/abs/2404.08471. 

- Peter W. Battaglia, Razvan Pascanu, Matthew Lai, Danilo Jimenez Rezende, and Koray Kavukcuoglu. Interaction networks for learning about objects, relations and physics. In _Advances in Neural Information Processing Systems_ , volume 29, 2016. 

10 

- Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, Varun Jampani, and Robin Rombach. Align your latents: High-resolution video synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 22563–22575, 2023. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. URL https://arxiv.org/abs/2307.15818. 

- Jake Bruce, Michael Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, Yusuf Aytar, Sarah Bechtle, Feryal Behbahani, Stephanie Chan, Nicolas Heess, Luis Gonzalez, Simon Osindero, Sherjil Ozair, Scott Reed, Jingwei Zhang, Konrad Zolna, Jeff Clune, Nando de Freitas, Satinder Singh, and Tim Rockt¨aschel. Genie: Generative interactive environments. In _Proceedings of the 41st International Conference on Machine Learning_ , 2024. 

- Eduardo F. Camacho and Carlos Bordons. _Model Predictive Control_ . Springer, 2013. 

- Miles Cranmer, Sam Greydanus, Stephan Hoyer, Peter Battaglia, David Spergel, and Shirley Ho. Lagrangian neural networks. _arXiv preprint arXiv:2003.04630_ , 2020. 

- Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine, Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch, and Pete Florence. Palm-e: An embodied multimodal language model. _arXiv preprint arXiv:2303.03378_ , 2023. 

- Frederik Ebert, Chelsea Finn, Sudeep Dasari, Annie Xie Xie, Alex Lee, and Sergey Levine. Visual foresight: Model-based deep reinforcement learning for vision-based robotic control. In _arXiv preprint arXiv:1812.00568_ , 2018. 

- Chelsea Finn and Sergey Levine. Deep visual foresight for planning robot motion. In _2017 IEEE International Conference on Robotics and Automation_ , pages 2786–2793. IEEE, 2017. 

- Samuel Greydanus, Misko Dzamba, and Jason Yosinski. Hamiltonian neural networks. In _Advances in Neural Information Processing Systems_ , volume 32, 2019. 

- Albert Gu and Tri Dao. Mamba: Linear-time sequence modeling with selective state spaces. _arXiv preprint arXiv:2312.00752_ , 2023. 

- Albert Gu, Karan Goel, and Christopher R´e. Efficiently modeling long sequences with structured state spaces. In _International Conference on Learning Representations_ , 2022. 

- David Ha and J¨urgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 

- Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _Proceedings of the 36th International Conference on Machine Learning_ , pages 2555–2565. PMLR, 2019. 

- Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations_ , 2020. 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

11 

- Ernst Hairer, Christian Lubich, and Gerhard Wanner. _Geometric Numerical Integration: StructurePreserving Algorithms for Ordinary Differential Equations_ , volume 31. Springer, 2006. 

- Jonathan Ho, Tim Salimans, Alexey Gritsenko, William Chan, Mohammad Norouzi, and David J. Fleet. Video diffusion models, 2022. URL https://arxiv.org/abs/2204.03458. 

- Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- Michael Janner, Justin Fu, Marvin Zhang, and Sergey Levine. When to trust your model: Modelbased policy optimization. In _Advances in Neural Information Processing Systems_ , volume 32, 2019. 

- Bernhard Kerbl, Georgios Kopanas, Thomas Leimk¨uhler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. _ACM Transactions on Graphics_ , 42(4):1–14, 2023. 

- Thomas Kipf, Elise van der Pol, and Max Welling. Contrastive learning of structured world models. In _International Conference on Learning Representations_ , 2020. 

- Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. In _European Conference on Computer Vision_ , pages 405–421. Springer, 2020. 

- OpenAI. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision. In _Proceedings of the 38th International Conference on Machine Learning_ , pages 8748–8763. PMLR, 2021. 

- Maziar Raissi, Paris Perdikaris, and George Em Karniadakis. Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. _Journal of Computational Physics_ , 378:686–707, 2019. 

- Alvaro Sanchez-Gonzalez, Jonathan Godwin, Tobias Pfaff, Rex Ying, Jure Leskovec, and Peter W. Battaglia. Learning to simulate complex physics with graph networks. In _Proceedings of the 37th International Conference on Machine Learning_ , pages 8459–8468. PMLR, 2020. 

- Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, Timothy Lillicrap, and David Silver. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588 (7839):604–609, 2020. 

- Richard S. Sutton. Dyna, an integrated architecture for learning, planning, and reacting. _ACM SIGART Bulletin_ , 2(4):160–163, 1991. 

- Erik Talvitie. Self-correcting models for model-based reinforcement learning. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 31, 2017. 

- Peter Toth, Danilo J. Rezende, Andrew Jaegle, S´ebastien Racani`ere, Aleksandar Botev, and Irina Higgins. Hamiltonian generative networks. In _International Conference on Learning Representations_ , 2020. 

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need, 2017. URL https://arxiv. org/abs/1706.03762. 

- Yaofeng Desmond Zhong, Biswadip Dey, and Amit Chakraborty. Symplectic ode-net: Learning hamiltonian dynamics with control. In _International Conference on Learning Representations_ , 2020. 

12 

