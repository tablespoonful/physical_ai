---
title: "LessMimic: Long-Horizon Humanoid Interaction with Unified Distance Field Representations"
date: "2026-02-25"
authors: "Yutang Lin; Jieming Cui; Yixuan Li; Baoxiong Jia; Yixin Zhu; Siyuan Huang"
url: https://arxiv.org/abs/2602.21723
pdf: https://arxiv.org/pdf/2602.21723
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.21723)** / [論文ページ](https://arxiv.org/abs/2602.21723)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **LESSMIMIC** : Long-Horizon Humanoid Interaction with Unified Distance Field Representations 

Yutang Lin<sup>˚</sup><sup>_,_1</sup><sup>_,_2</sup><sup>_,_3</sup><sup>_,_5</sup><sup>_,_6</sup><sup>_,_7</sup> Jieming Cui<sup>˚</sup><sup>_,_1</sup><sup>_,_2</sup><sup>_,_3</sup><sup>_,_5</sup><sup>_,_6</sup><sup>_,_7</sup> Yixuan Li<sup>4</sup><sup>_,_2</sup><sup>_,_5</sup> Baoxiong Jia<sup>�</sup><sup>_,_2</sup><sup>_,_5</sup> Yixin Zhu<sup>�</sup><sup>_,_3</sup><sup>_,_1</sup><sup>_,_5</sup><sup>_,_6</sup><sup>_,_7</sup> Siyuan Huang<sup>�</sup><sup>_,_2</sup><sup>_,_5</sup> 

> ˚Equal contribution � Corresponding Author Project Website: https://lessmimic.github.io 

> 1Institute for AI, Peking University 2Beijing Institute for General Artificial Intelligence (BIGAI) 

> 3School of Psychological and Cognitive Sciences, Peking University 

> 4School of Computer Science and Technology, Beijing Institute of Technology 

> 5State Key Lab of General AI 6Beijing Key Laboratory of Behavior and Mental Health, Peking University 

> 7Embodied Intelligence Lab, PKU-Wuhan Institute for Artificial Intelligence 


(a) **Shape and size generalization.** The same policy lifts objects ranging from a 23 cm box to a 60 cm-diameter cylinder. 


(c) **Long-horizon skill composition.** A single policy executes push, pick-up, carry, and sit-stand sequentially without resets. 

Fig. 1: **Generalizable long-horizon humanoid interaction via LESSMIMIC.** A single DF-conditioned policy supports (a) online failure recovery through continuous geometric feedback, (b) generalization to unseen object shapes and scales without retraining, and (c) longhorizon composition of heterogeneous interaction skills within a single policy. 

**_Abstract_ —Humanoid robots that autonomously interact with physical environments over extended horizons represent a central goal of embodied intelligence. Existing approaches rely on reference motions or task-specific rewards, tightly coupling policies to particular object geometries and precluding multiskill generalization within a single framework. A unified interaction representation enabling reference-free inference, geometric** 

**generalization, and long-horizon skill composition within one policy remains an open challenge. Here we show that Distance Field (DF) provides such a representation: LESSMIMIC conditions a single whole-body policy on DF-derived geometric cues—surface distances, gradients, and velocity decompositions— removing the need for motion references, with interaction latents encoded via a Variational Auto-Encoder (VAE) and post-trained** 

**using Adversarial Interaction Priors (AIP) under Reinforcement Learning (RL). Through DAgger-style distillation that aligns DF latents with egocentric depth features, LESSMIMIC further transfers seamlessly to vision-only deployment without motion capture (MoCap) infrastructure. A single LESSMIMIC policy achieves 80–100% success across object scales from 0** _._ **4** ˆ **to 1** _._ **6** ˆ **on PickUp and SitStand where baselines degrade sharply, attains 62.1% success on 5 task instances trajectories, and remains viable up to 40 sequentially composed tasks. By grounding interaction in local geometry rather than demonstrations, LESSMIMIC offers a scalable path toward humanoid robots that generalize, compose skills, and recover from failures in unstructured environments.** 

TABLE I: **Comparison of humanoid-object interaction methods.** We compare representative reference-based and reference-free methods across three axes: whether (i) a unified observation space is shared across tasks, (ii) inference requires no motion references, and (iii) a single policy supports autonomous long-horizon skill composition. 

|**Method**|**Type**|**Task-unified**<br>**observation**|**No motion at**<br>**inference**|**Long-horizon**<br>**skill composition**|
|---|---|---|---|---|
|HDMI [51]|Ref-based|✗|✗|✗|
|ResMimic [62]|Ref-based|✗|✗|✗|
|CLONE [26]|Ref-based|✗|✗|✓|
|Op3-Soccer [10]|Ref-free|✗|✗|✗|
|PhysHSI [50]|Ref-free|✗|✓|✗|
|**Ours**|Ref-free|✓|✓|✓|


## I. INTRODUCTION 

Consider a humanoid tasked with tidying a room: push a chair aside, pick up a box, carry it across the room, and sit down to rest. Each sub-task involves distinct contact patterns, object geometries, and body configurations—yet a skilled human executes the entire sequence fluidly, without consulting a motion script. Replicating this capability on hardware is an open problem in embodied intelligence [34, 21, 6]. Recent progress in whole-body humanoid control has produced impressive results in locomotion and dynamic motion [12, 27, 61, 24, 26, 7], yet translating these skills into persistent, contactrich interaction with varied objects remains out of reach. 

The core obstacle is representational. How should a robot perceive and reason about its relation to an object during interaction, and what form should that representation take to remain useful across geometries, scales, and task horizons? Current approaches split into two camps, each sacrificing something essential. **Reference-based methods** [54, 51, 62, 27, 61] achieve high-fidelity motions by conditioning policies on recorded demonstrations, but this motion-centric formulation rigidly entangles object geometry with specific reference trajectories, creating a dual limitation. First, the policy becomes a geometric specialist that memorizes training instances and fails on novel shapes. Second, and more critically, it forfeits steering flexibility: any real-time deviation from the reference trajectory is penalized as a tracking failure, not interpreted as an adaptive response. To recover this lost maneuverability, recent variants [53, 32, 8, 56, 26, 58] introduce higher-level planners or human-in-the-loop teleoperation, but these additions merely circumvent the representational bottleneck at the cost of perceptual complexity and full autonomy. **Reference-free methods** [50, 10] take the opposite stance, discarding motion references to gain flexibility, but without a principled interaction signal they resort to task-specific reward engineering and produce isolated policies that cannot compose across skills. Neither camp provides what is ultimately needed: a geometryaware, task-unified representation that decouples interaction logic from specific motion patterns, enabling seamless skill composition without sacrificing adaptive maneuverability. 

We argue that the Distance Field (DF) [35] is precisely this representation. A DF assigns to every point in space its distance to the nearest object surface, yielding a continuous, differentiable field whose gradient encodes surface normals everywhere—including during contact. This is not merely a convenient geometric abstraction; it has concrete consequences 

for learning. Where point clouds and voxels discretize space and lose gradient information, and where implicit neural representations are too slow for high-frequency control, the DF provides dense, directional geometric cues at negligible query cost. Crucially, the local DF structure near a hand grasping an object is largely invariant to object size and approach direction, making the representation inherently shape- and scale-agnostic. Beyond static geometry, first-order DF cues— surface gradients and velocity decompositions into normal and tangential components—capture the directional dynamics of ongoing contact, providing precisely the interaction signal needed for contact-rich whole-body coordination. 

Guided by this insight, we introduce **LESSMIMIC** , a reference-free framework that places the DF at the center of humanoid interaction. **LESSMIMIC** extracts a velocitydecomposed, history-dependent interaction feature from the DF—capturing approach intensity, surface traversal, and geometric evolution—and encodes it into a compact latent via a VAE. A single whole-body policy is then trained on this latent using a three-stage pipeline: behavior cloning from a teacher for stable initialization, RL fine-tuning with our proposed AIP for geometric generalization across randomized object geometries, and visual distillation for deployment without MoCap. At inference, **the policy requires only a target root trajectory and the current DF observation—no motion references, no task-specific rewards, no separate planners** . 

The result is a single policy that simultaneously achieves what prior methods treat as competing objectives. Across four interaction tasks (PickUp, SitStand, Push, Carry) and object scales from 0 _._ 4ˆ to 1 _._ 6ˆ, **LESSMIMIC** attains 80–100% success on PickUp and SitStand where both reference-based and reference-free baselines degrade sharply. For long-horizon execution, the unified DF representation enables implicit skill transitions without explicit sequencing: **LESSMIMIC** achieves 62.1% success on 5-task trajectories and remains viable across sequences of up to 40 heterogeneous task instances sequence—a regime where all ablated variants collapse to zero. 

In summary, our contributions are threefold: 

- ‚ A DF-based interaction representation that encodes local geometric relationships as lightweight, differentiable, and shape-agnostic cues, enabling a single policy to generalize across diverse object geometries without retraining. 

- ‚ A three-stage training pipeline—behavior cloning, AIPguided RL, and visual distillation—that produces a wholebody interaction policy requiring only a root trajectory command at inference, with no motion references. 

- ‚ Demonstration that a single **LESSMIMIC** policy can execute, transition between, and recover from heterogeneous interaction skills over horizons of up to 40 consecutive task instances, extending the practical scope of long-horizon humanoid interaction. 

## II. RELATED WORK 

## _A. Reference-based Humanoid-Object Interaction_ 

Recent advances in RL have driven significant progress in whole-body humanoid control, producing increasingly capable systems for dynamic motion and physical interaction [33, 9, 12, 18]. A dominant paradigm formulates humanoid-object interaction through motion-centric representations, conditioning policies on reference motions as explicit supervision targets to stabilize learning and produce physically plausible behaviors [51, 27, 61, 62, 56, 1, 53]. While effective, this formulation tightly couples the learned policy to the object geometries and configurations present in the reference data [38, 37]: when object properties deviate from the training distribution, the prescribed motions become invalid, leading to brittle behavior on novel objects [21, 17]. 

To recover adaptability, several works introduce teleoperation or human-in-the-loop strategies that use closed-loop human guidance to generate or correct reference motions online [26, 58, 57, 32, 23, 12, 9, 13]. These approaches improve robustness under object and contact variation, but the dependence on motion references remains structural: human intervention adds supervision overhead and limits scalability, while the policy remains constrained by the topology of observed motions [2, 43, 5]. The result is a persistent trade-off between interaction fidelity, policy autonomy, and generalization that motion-centric representations cannot resolve. 

## _B. Reference-free Humanoid-Object Interaction_ 

Eliminating motion references at inference time has been widely recognized as a key step toward greater autonomy [31]. Early attempts drew inspiration from model-based control [40, 44, 14] and online optimization [45, 15], generating behaviors from task objectives without prerecorded motions. While these approaches offer strong controllability, their reliance on accurate system models and short planning horizons limits applicability to complex, contact-rich scenarios. 

More recently, learning-based reference-free methods have gained traction [24, 25] by conditioning policies directly on task-relevant state information, enabling tighter perceptionaction coupling and simpler real-world deployment [50, 39, 48, 60, 22, 10]. Such formulations show promising robustness under real-world sensing conditions and greater flexibility on out-of-distribution objects and environments. However, most rely on task-specific observations, rewards, or handcrafted interaction cues [30], producing specialized policies that cannot generalize across tasks or compose skills over extended 

horizons. The absence of a unified interaction representation limits the robust multi-skill behavior within a single policy. 

## _C. Representation for Human-Object Interaction_ 

Geometric representations for human–object interaction span a broad design space, each with distinct trade-offs between expressiveness and computational cost. Voxel-based and occupancy representations [29, 16, 49, 52, 20] explicitly model geometry and collisions but incur high memory and compute costs that preclude real-time whole-body control. Point-based [63, 19, 3, 28] and mesh-based [59, 46, 36, 11] representations capture detailed surface geometry and are well-suited for perception and offline planning, yet lack the continuous distance information needed for contact-aware control. Implicit neural representations [47, 55, 41, 4] offer expressive continuous geometry, but their inference cost makes integration into high-frequency control loops impractical. 

The DF [35] bypasses these limitations by encoding geometric proximity as a continuous, differentiable field that can be queried at negligible cost. Unlike discrete representations that lose gradient information or implicit neural representations that incur high inference latency, DFs provide analytical surface gradients essential for contact-aware coordination. For humanoid interaction, where interpenetration is absent, unsigned distance magnitude and local gradients constitute a sufficient geometric description—a simplification that retains the cues necessary for contact-rich control while ensuring the efficiency required for real-time deployment. 

## III. THE **LESSMIMIC** FRAMEWORK 

We introduce **LESSMIMIC** , a reference-free framework that leverages Distance Field (DF) as a unified interaction representation, enabling a single policy to acquire diverse and generalizable humanoid interaction skills. Fig. 2 provides a high-level view of **LESSMIMIC** at deployment; the overall architecture, illustrated in Fig. 3, integrates geometry-aware perception with whole-body control to support long-horizon interaction across objects of varying shapes and sizes. We first formulate the DF-based interaction representation in 


Fig. 2: **LESSMIMIC framework overview.** The policy takes as input a root trajectory command, humanoid proprioception, and a unified DF-based interaction representation that captures current humanoid-object spatial- and temporal-relation. The representation is constructed from MoCap or depth image and encoded into a compact latent _zt_ via a VAE. The policy is trained in two stages (interaction skill pre-training and discriminative post-training) and outputs actions to a whole-body controller at deployment. 


Fig. 3: **Training pipeline of LESSMIMIC.** (a) Object observations from either MoCap or an egocentric depth camera yield per-link DF features **u** _t_ , which are velocity-decomposed and encoded into an interaction latent representation _zt_ via a VAE. (b) During interaction skill pre-training, a teacher policy _π_ mimic tracks retargeted human motions to generate physically valid data, from which _π_ base is trained via behavior cloning without access to reference motions, but takes root trajectory command _ct_<sup>root</sup> , humanoid proprioception _o_<sup>prop</sup> and the DF latent _zt_ . (c) During discriminative post-training, _π_ base is fine-tuned with RL guided by AIP, a discriminator that regularizes interaction validity in the geometric domain across randomized object geometries, yielding _π_ full. (d) During visual-motor distillation, _π_ full is distilled into _π_ vis via DAgger-style supervision, replacing MoCap inputs with egocentric depth features for portable real-world deployment. 

Sec. III-A, then detail the three-stage training pipeline: pretraining (Sec. III-B), discriminative post-training (Sec. III-C), and visual-motor distillation (Sec. III-D). 

## _A. DF-based Interaction Representation_ 

Methods conditioned on absolute motion trajectories or object-specific representations entangle interaction logic with particular spatial layouts, producing brittle behavior under geometric variation. **LESSMIMIC** instead constructs a geometryaware state space in which interaction is described through local DF relationships rather than global coordinates. This formulation enables the policy to reason about contact and relative motion invariantly to object shape and scale, capturing the essential structure of an interaction rather than memorizing absolute trajectories. 

Formally, we denote the DF as Φ : R<sup>3</sup> Ñ R, serving as a dynamic local reference frame anchored to the object’s geometry. At time _t_ , for a humanoid link ( _e.g_ ., a hand or pelvis) at position **x** _t_ P R<sup>3</sup> with linear velocity **v** _t_ P R<sup>3</sup> , the DF yields the distance to the object surface Φp **x** _t_ q and the local surface orientation _∇_ Φp **x** _t_ q—the gradient at the projection of **x** _t_ onto the zero-level set of Φ—supplying geometry-aligned cues for contact-aware interaction control. 

Position alone is insufficient to characterize interaction dynamics, as it captures neither kinetic state nor directional intent relative to the object surface. We therefore decompose **v** _t_ into 

two orthogonal components using _∇_ Φp **x** _t_ q as the local surface normal: motion along the normal direction, corresponding to approach or force application, and motion within the tangent plane, corresponding to sliding or surface traversal. Formally: 


where **v** _t_<sup>norm</sup> captures the interaction intensity relative to the surface and **v** _t_<sup>tan</sup> captures the flow across the surface geometry, together projecting the global velocity into the local coordinate system defined by the object’s surface. 

To capture the temporal evolution of the interaction, we collect the per-link tuple **u** _t_ “ rΦp **x** _t_ q _, ∇_ Φp **x** _t_ q _,_ **v** _t_<sup>norm</sup> _,_ **v** _t_<sup>tansat</sup> each time step over a set of task-relevant links, and define the _interaction representation It_ as a trajectory of these local geometric features over a temporal window of length _l_ : 


Since _It_ is defined entirely through the robot’s relation to the DF, it is invariant to the object’s global pose and scale: interactions with objects of different sizes, shapes, or placements exhibit similar geometric structure, allowing the policy to learn the underlying geometry of interaction behaviors rather than memorizing absolute trajectories, and thereby supporting generalization across object geometries. An example of the DF distance and gradient evolution during interaction is shown in 


Fig. 4: **An example of the DF signals during a sitting interaction.** The blue curve shows the mean DF distance between the humanoid and the chair across all joints, with the shaded region indicating the full range; the red curve shows the mean DF gradient magnitude. As the humanoid approaches and makes contact with the chair, the distance decreases while the gradient magnitude increases, reflecting the intensifying geometric coupling. Vertical dashed lines indicate transitions between interaction phases (Stand, Sit, Sit, Stand). 

Fig. 4. Prior to policy training, _It_ is encoded by a VAE into a smooth latent _zt_ , improving robustness to sensor noise and facilitating convergence during training. 

## _B. Interaction Skill Pre-Training_ 

Learning the DF-based interaction representation requires data that is both semantically meaningful and physically feasible. Purely retargeted human MoCap data frequently violates physical constraints in simulation, while collecting highquality interaction data at scale is costly. To balance feasibility and scalability, we generate training data in simulation via a mimic policy _π_ mimic that tracks retargeted reference motions under full physics. Following [62], _π_ mimic augments motion tracking with a residual module to compensate for dynamic mismatches during object interaction, producing physically valid state-action trajectories for downstream training. Further implementation details are provided in Sec. A-A. 

We pre-train the target policy _π_ base via behavior cloning on data generated by _π_ mimic, with the goal of initializing the policy under the inference-time observation setting. Unlike _π_ mimic, which has access to privileged reference motions, _π_ base operates solely on _o_ base “ r _o_ prop _, ct_<sup>_root_</sup> _, zt_ s, comprising proprioception _o_ prop, a sparse root-trajectory command _ct_<sup>_root_</sup> , and the DF interaction latent _zt_ . To mitigate covariate shift between training and rollout distributions, we apply DAgger [42] by rolling out _π_ base and querying _π_ mimic for corrective actions. Training minimizes the Mean Squared Error (MSE) loss between the actions of the base and teacher policies: 


where _o_ mimic includes privileged full-body reference motions 

unavailable at inference. This stage yields a stable initialization that grounds the DF interaction representation in whole-body control, preparing the policy for geometry-aware generalization in the subsequent post-training stage. 

## _C. Discriminative Post-Training_ 

Pre-training yields a stable initialization, but _π_ base is trained on a fixed set of objects paired with reference motions, which encourages memorization of specific kinematic trajectories rather than learning the underlying geometric rules of interaction. To promote genuine geometric generalization, we fine-tune the policy using RL in a procedurally augmented environment where object geometries are randomized across scale, shape, and surface properties. 

In this setting, motion-tracking rewards and hand-crafted shaping terms are deliberately excluded: reference motions are unavailable under procedural object variation, and task-specific reward terms would require redefinition across geometries. Instead, we introduce Adversarial Interaction Priors (AIP) as a geometry-aware supervision signal. Inspired by Adversarial Motion Priors (AMP) [39], which regularizes motion naturalness, AIP instead regularizes _interaction validity_ in the geometric domain. The key insight is that while the absolute joint configurations required for interaction vary with object geometry, the local geometric relationship between the robot and the object surface—captured by the interaction latent _zt_ —remains consistent across geometries and can serve as a transferable supervision signal. 

We train a discriminator _D_ to distinguish interaction latents generated by the policy on novel objects from those stored in a reference interaction buffer _B_ ref, using a least-squares GAN objective: 


The policy is simultaneously trained to maximize a composite reward _rt_ “ _r_ task ` _λir_ interact ` _λsr_ style, where _r_ task penalizes deviation from the target root command, _r_ interact is derived from the discriminator output, and _r_ style is a standard AMP loss that regularizes motion naturalness: 


By conditioning the discriminator on _zt_ rather than the full robot state, AIP encourages the policy to reproduce the _geometric signature_ of valid interactions without constraining it to a specific kinematic template, allowing the robot to synthesize novel poses for unseen geometries while maintaining stable and physically plausible contact. The resulting policy is denoted _π_ full. More details of the post-training process are provided in Sec. A-B 

## _D. Visual-Motor Policy Distillation_ 

While **LESSMIMIC** achieves strong performance across interaction tasks, it relies on global object information from 

TABLE II: **Comparison of baselines, ablations, and LESSMIMIC under object-scale variation in simulation.** Four interaction tasks (PickUp, SitStand, Push, Carry) are evaluated across object scales from 0 _._ 4ˆ to 1 _._ 6ˆ, with the training scale at 1 _._ 0ˆ. Reference-based baselines track fixed demonstration motions; reference-free baselines and ablated variants operate without motion references. Each ablation removes one component from the full system: _AIP_ removes the adversarial interaction prior, _Syn._ removes synthetic physicalization, _Rand._ disables geometry randomization, _RL_ removes reinforcement learning fine-tuning, and _Trans._ replaces the Transformer with an MLP backbone. Results report mean ˘ std over 3 random seeds. _Rsucc_ : task success rate; _Rcont_ : hand contact rate over total task duration. **Bold** and underline denote the best and second-best results per column.<sup>˚</sup> : implemented by ourselves. 

|**Method**||**Pic**|**kUp** _Rsucc_ **(**|Ò,%)||**SitS**|**tand** _Rsucc_|**(**Ò,%)|**P**|**ush** _Rcont_ **(**|Ò,%)|**Carry** _Rsucc_ **(**Ò,%)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**0.4**|**0.6**|**1.0**|**1.4**|**1.6**|**0.4**|**1.0**|**1.6**|**0.6**|**1.0**|**1.4**||
|**Reference-ba**|**sed baselines**||||||||||||
|HDMI<sup>˚</sup>|0_._0p˘0_._0q|99_._7<br>p˘0_._5q|**100.0**p˘0_._0q|40_._7p˘3_._3q|1_._7p˘1_._2q|0_._0p˘0_._0q|99_._0<br>p˘0_._0q|1_._7p˘0_._5q|0_._3p˘0_._0q|**97.3**p˘0_._5q|**10.6**p˘2_._9|q<br>27_._4p˘0_._3q|
|ResMimic<sup>˚</sup>|0_._0p˘0_._0q|18_._3p˘1_._2q|**100.0**p˘0_._0q|**99.7**p˘0_._5q|63_._0p˘10_._2q|0_._0p˘0_._0q|**100.0**p˘0_._0q|93_._7p˘0_._5q|0_._4p˘0_._2q|93_._1<br>p˘1_._2q|2_._2p˘0_._7q|32_._9p˘1_._5q|
|VisualMimic|0_._0p˘0_._0q|0_._0p˘0_._0q|**100.0**p˘0_._0q|0_._0p˘0_._0q|0_._0p˘0_._0q|–|–|–|–|20_._6p˘9_._0q|–|–|
|**Reference-fre**|**e baselines**||||||||||||
|PhysHSI|23_._1p˘2_._4q|70_._5p˘2_._6q|**100.0**p˘0_._0q|47_._9p˘2_._8q|39_._9p˘2_._8q|61_._3p˘2_._7q|76_._2p˘2_._3q|71_._8p˘2_._4q|–|–|–|81_._6<br>p˘1_._9q|
|**Ablation stud**|**y**||||||||||||
|Ours - AIP|0_._0p˘0_._0q|0_._7p˘0_._5q|23_._3p˘5_._0q|57_._3p˘1_._2q|64_._0p˘2_._9q|**98.7**p˘0_._5q|98_._3p˘0_._5q|89_._0p˘0_._8q|**82.9**p˘1_._1q|72_._5p˘1_._9q|6_._5<br>p˘1_._9q|0_._0p˘0_._0q|
|Ours - Syn.|34_._0p˘6_._7q|94_._3p˘2_._5q|99_._3<br>p˘0_._9q|**99.7**p˘0_._5q|**99.7**p˘0_._5q|95_._3p˘1_._7q|30_._0p˘2_._2q|86_._3p˘3_._9q|0_._0p˘0_._0q|41_._9p˘2_._1q|3_._5p˘1_._6q|66_._5p˘2_._0q|
|Ours - Rand.|0_._0p˘0_._0q|0_._0p˘0_._0q|0_._0p˘0_._0q|0_._0p˘0_._0q|0_._0p˘0_._0q|0_._0p˘0_._0q|81_._3p˘3_._4q|**97.7**p˘1_._2q|0_._0p˘0_._0q|67_._0p˘1_._6q|2_._1p˘1_._0q|0_._0p˘0_._0q|
|Ours - RL|0_._0p˘0_._0q|2_._0p˘0_._8q|31_._7p˘2_._6q|37_._0p˘2_._4q|9_._7p˘1_._7q|1_._7p˘1_._2q|64_._7p˘3_._1q|15_._0p˘2_._8q|0_._0p˘0_._0q|67_._3p˘0_._7q|0_._0p˘0_._0q|5_._3p˘1_._5q|
|Ours - Trans.|0_._0p˘0_._0q|0_._0p˘0_._0q|0_._0p˘0_._0q|0_._0p˘0_._0q|0_._0p˘0_._0q|98_._0<br>p˘0_._8q|77_._7p˘0_._5q|95_._7<br>p˘2_._1q|18_._3<br>p˘1_._4q|85_._7p˘2_._4q|3_._0p˘0_._6q|0_._0p˘0_._0q|
|Ours (Mocap)|63_._0<br>p˘5_._0q|**100.0**p˘0_._0q|**100.0**p˘0_._0q|88_._0<br>p˘1_._6q|94_._0<br>p˘1_._6q|79_._0p˘0_._0q|80_._3p˘2_._1q|61_._7p˘1_._2q|13_._9p˘0_._2q|51_._3p˘1_._6q|2_._0p˘0_._3q|**82.9**p˘1_._4q|
|Ours (Vision)|**63.7**p˘3_._1q|94_._7p˘1_._9q|91_._0p˘3_._3q|**99.7**p˘0_._5q|93_._0p˘1_._6q|–|–|–|1_._2p˘0_._1q|35_._2p˘1_._3q|1_._9p˘0_._8q|35_._8p˘2_._7q|


a MoCap system, which is unavailable in most real-world deployments. To relax this assumption, we distill _π_ full into a vision-based policy _π_ vis that operates solely on egocentric depth observations, and evaluate it on the same tasks and metrics as the MoCap-based model to enable direct comparison. 

The vision-based policy observes _o_ vis “ r _o_ prop _, ct, St_ s, where _St_ denotes a history of egocentric depth frames. It comprises a visual encoder _Eϕ_ followed by the same control head as _π_ full, where _Eϕ_ maps _St_ to a compact latent _zt_ — effectively learning to recover the geometric cues previously provided explicitly by _It_ . 

We adopt a DAgger-style [42] distillation procedure. At each iteration, _π_ vis interacts with the environment to collect trajectories, and the frozen teacher _π_ full is queried at every encountered state to provide supervision. The student minimizes the MSE loss against the teacher’s actions: 


Throughout distillation, we apply extensive domain randomization to facilitate sim-to-real transfer, including perturbations of camera extrinsics, additive noise on depth observations, and randomization of physical properties. These perturbations encourage _Eϕ_ to learn geometry-relevant features robust to sensor noise and modeling discrepancies, enabling reliable execution of contact-rich interactions from onboard perception alone. Additional details are provided in Appendix B. 

## IV. EXPERIMENTS 

We evaluate **LESSMIMIC** across two complementary dimensions: its **generalization** to variations in object size and shape (Sec. IV-B), and its capability for **long-horizon composition** of diverse interaction skills (Sec. IV-C). Our analysis considers two primary policy variants: a MoCap-based model, _π_ full, and a closed-loop visual-motor model, _π_ vis. To ensure a rigorous assessment, **LESSMIMIC** is compared against 

representative reference-based and reference-free baselines under identical training and evaluation conditions. We further conduct ablation studies (Sec. IV-E) to isolate the specific contributions of individual system components. Finally, we demonstrate the robustness and transferability of our approach by validating all methods in both high-fidelity simulation and on a physical real-world humanoid platform. 

## _A. Experimental Setup_ 

_Tasks:_ We evaluate on four representative interaction tasks that span a range of contact modes and object configurations. _PickUp_ requires lifting a box of varying sizes from the ground using both hands and maintaining a stable grasp. _SitStand_ evaluates seated interaction by requiring pelvis contact with chairs of different heights. _Push_ focuses on bimanual contact-rich interaction in which the robot pushes a target object while continuously maintaining hand contact. _Carry_ requires picking up a box and transporting it to a target location under continuous bimanual contact. 

_Evaluation Metrics:_ Task success is defined by geometric and contact-based criteria matched to each task. _PickUp_ succeeds if the box is lifted above a height threshold and stably held. _SitStand_ succeeds when stable pelvis contact with the chair is established within a valid root height range. _Carry_ and multi-task success are measured by tracking the manipulated object along predefined trajectories, with deviations constrained within a fixed tolerance. For _Push_ , success is measured by the hand–object contact rate, with bodydominated contact considered failure. 

_Baselines:_ We compare **LESSMIMIC** against two state-of-the-art reference-based methods—HDMI [51] and ResMimic [62]—which explicitly track motion demonstrations of object interaction, as well as VisualMimic [56], a referencebased variant that operates with reduced sensory input (depth observations only). PhysHSI [50] serves as the reference- 


Fig. 5: **Real-world generalization of LESSMIMIC.** (a) The policy successfully picks up a box, one of the training geometries. (b) The same policy generalizes to a soccer ball—a spherical object entirely unseen during training—demonstrating shape generalization beyond the training distribution. (c) The policy performs _SitStand_ across two chair heights (12 cm and 46 cm), maintaining stable pelvis contact across diverse seat geometries. 

free baseline. Additional details on motion sources, MoCap processing, controller design, and observation dimensions are provided in Appendix B. 

## _B. Generalization on Object Sizes_ 

Object shape and size variations can substantially affect humanoid interaction success: for large-amplitude motions ( _e.g_ ., reaching the ground) or long-horizon execution ( _e.g_ ., 40 task instances sequence), geometric discrepancies accumulate and compound across time steps. To evaluate generalization beyond the training distribution (scale 1 _._ 0ˆ), we vary object scale from 0 _._ 4ˆ to 1 _._ 6ˆ across all tasks and, for _PickUp_ , additionally vary object shape between box, spherical, and cylindrical geometries (Fig. 1 and Fig. 5). This setting directly tests whether policies adapt based on local geometric relations or rely on memorized motion patterns. 

As shown in Tab. II, reference-based methods degrade predictably with scale deviation. HDMI [51] and ResMimic [62] achieve high success near the reference scale but deteriorate sharply at extreme sizes, and VisualMimic [56] exhibits the 

TABLE III: **Long-horizon skill composition with increasing task length in simulation.** Success rate (%) for completing sequences of _N_ randomly ordered heterogeneous tasks under a single policy without environment resets. Each ablation removes one component from the full system; see Tab. II for ablation descriptions. All ablated variants collapse to zero beyond short sequences, whereas **LESSMIMIC** (Mocap) maintains non-zero success up to _N_ “ 40. Results report mean ˘ std over 3 random seeds. **Bold** denotes the best result per column. 

|**Method**|**N=5**|**N=10**|**N=15**|**N=25**|**N=40**|
|---|---|---|---|---|---|
|**Ablation stud**|**y**|||||
|Ours - AIP|5_._2 p˘0_._2q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|0_._0<br>p˘0_._0q|0_._0<br>p˘0_._0q|
|Ours - Syn.|22_._1<br>p˘0_._8q|4_._9<br>p˘0_._2q|1_._0<br>p˘0_._3q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|
|Ours - Rand.|1_._9 p˘0_._1q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|
|Ours - RL|3_._2 p˘0_._2q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|
|Ours - Trans.|1_._7 p˘0_._1q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|
|**Our method**||||||
|Ours (Mocap)|**61.7** p˘1_._7q|**38.1** p˘1_._6q|**23.5** p˘1_._2q|**9.0** p˘0_._6q|**2.1** p˘0_._2q|
|Ours (Vision)|15_._9 p˘0_._6q|2_._5 p˘0_._1q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|0_._0 p˘0_._0q|


same trend despite its visual inputs. In contrast, **LESSMIMIC** demonstrates consistent robustness to geometric variation across all four tasks. For _PickUp_ , success rates remain above 90% across most tested scales, degrading only gradually at the smallest object size (15 cm<sup>3</sup> ) where all methods struggle. Similar trends hold for _SitStand_ and _Push_ , where **LESSMIMIC** maintains stable success and contact rates across scales, outperforming the strongest baselines by 15–20% at larger object sizes. For _Carry_ , **LESSMIMIC** achieves the highest success rate among both reference-based and reference-free methods under scale variation. 

## _C. Long-Horizon Skill Composition_ 

Beyond single-skill evaluation, we assess long-horizon execution by randomly composing multiple interaction tasks into a single trajectory applied under a single policy without environment resets. Since reference-based baselines rely on predefined motions and reference-free baselines use taskspecific policy, neither can be directly applied to randomly generated task compositions; we therefore compare ablated variants of **LESSMIMIC** to analyze the contribution of each design choice. 

As shown in Tab. III, the full model achieves 62.1% success on 5-task trajectories and maintains 2.1% viability even at 40 sequentially composed tasks. All ablated variants, by contrast, collapse to zero success beyond short sequences, underscoring the necessity of each component. This long-horizon capability emerges from implicit skill transitions driven by the unified DF representation: rather than relying on explicit task sequencing, the policy continuously adapts to changing geometric contexts, enabling sustained execution of heterogeneous task sequences over extended horizons (see Fig. 6). 

## _D. Distilling_ **LESSMIMIC** _to Visual Input_ 

As shown in Tab. II, the vision-based variant preserves the overall performance trends of _π_ full but with a consistent reduction in success rates across tasks. For _PickUp_ , performance decreases from near-perfect levels to the 90% range 

TABLE IV: **Real-world deployment of LESSMIMIC on a physical humanoid platform.** Both the MoCap-based and vision-based variants are evaluated on _PickUp_ (22 cm<sup>3</sup> and 60 cm<sup>3</sup> ) and _SitStand_ (12 cm and 46 cm seat heights) under repeated executions. _Rsucc_ reports discrete task success rate; _Racc_ reports root trajectory tracking accuracy, measured via external MoCap for evaluation only. The vision-based variant is not evaluated on _SitStand_ due to limited egocentric observability of back-side contacts. 

|**Meth**|**od**|**PickUp** 22|_cm_<sup>3 </sup>(Ò,%)|**PickUp** 60|_cm_<sup>3 </sup>(Ò,%)|**SitStand** 1|2_cm_ (Ò,%)|**SitStand**|46_cm_ (Ò,%)|
|---|---|---|---|---|---|---|---|---|---|
|||**Real** _Rsucc_|**Root** _Racc_|**Real** _Rsucc_|**Root** _Racc_|**Real** _Rsucc_|**Root** _Racc_|**Real** _Rsucc_|**Root** _Racc_|
|Ours|(Mocap)|10 / 10|94.44|8 / 10|81.39|8 / 10|84.89|10 / 10|91.88|
|Ours|(Vision)|8 / 10|89.15|7 / 10|75.24|–|–|–|–|


Fig. 6: **Long-horizon skill composition in the real world.** A single **LESSMIMIC** policy executes a sequence of heterogeneous interaction skills without environment resets: pushing a cabinet to a target location, then picking up and carrying a box along the commanded trajectory (indicated by the yellow arrow). This demonstrates the policy’s ability to implicitly transition between distinct interaction modes under a unified DF-based representation. 

at larger scales and degrades further at smaller scales. Similar reductions are observed in _Push_ and _Carry_ , where success and contact rates remain below those of the MoCap-based model but are comparable to or exceed reference-free and visionguided reference-based baselines. Notably, for _PickUp_ under scale generalization, the vision-based policy achieves 63.7– 99.7% success at scales where all baseline methods exhibit near-zero performance. _SitStand_ is excluded from visionbased evaluation due to limited egocentric observability of back-side contacts. Across the remaining tasks, the moderate performance reduction is attributable to perceptual uncertainty introduced by the depth observations. 

## _E. Ablation Study_ 

To isolate the contribution of each component, we evaluate five ablated variants of the full system. As shown in Tab. II, removing the interaction prior ( _Ours - AIP_ ) significantly reduces robustness to scale variation, confirming that AIP is the primary mechanism enforcing geometry-consistent interaction across object geometries. Removing synthetic physicalization ( _Ours - Syn_ ), which replaces teacher-generated physically valid trajectories with raw retargeted MoCap data, most severely affects contact-rich tasks such as _Carry_ while leaving others relatively intact, suggesting that data physical feasibility matters most when sustained contact is required. Disabling geometry randomization ( _Ours - Rand_ ) causes severe overfit- 

ting with near-zero success outside training scales, confirming its necessity for scale-invariant generalization. Removing RL fine-tuning ( _Ours - RL_ ) yields limited performance and poor generalization, demonstrating that behavior cloning alone is insufficient to bridge the gap to novel geometries. Finally, replacing the Transformer with an MLP backbone ( _Ours - Trans_ ) severely degrades performance on _PickUp_ and _Carry_ , reflecting insufficient model capacity for capturing the temporal dependencies required in multi-skill interaction. 

## _F. Real-World Deployment_ 

We evaluate **LESSMIMIC** on a physical humanoid platform to assess robustness beyond simulation. Experiments cover _PickUp_ and _SitStand_ across varying object sizes (22 cm<sup>3</sup> and 60 cm<sup>3</sup> ) and chair heights (12 cm and 46 cm), with both the MoCap-based and vision-based variants evaluated under identical conditions using repeated executions. 

As shown in Tab. IV, real-world performance is largely consistent with simulation trends in Tab. II. The MoCapbased model achieves 10/10 success on _PickUp_ (22 cm<sup>3</sup> ) and _SitStand_ (46 cm), with root tracking accuracy above 90% in both cases. The vision-based variant achieves 8/10 and 7/10 on the two _PickUp_ conditions respectively, with slightly reduced tracking accuracy. For _SitStand_ , the MoCap-based model remains robust across seat heights; the vision-based variant is not evaluated due to limited observability of backside contacts (see project website). 

## V. CONCLUSION 

We present **LESSMIMIC** , a reference-free framework leveraging DFs as a unified representation for generalizable, longhorizon humanoid interaction. The key insight is that local DF geometry—surface distances, gradients, and velocity decompositions—provides a shape- and scale-invariant signal, enabling a single policy to master diverse skills. A threestage pipeline of behavior cloning, AIP-guided RL, and visualmotor distillation grounds this into robust, transferable wholebody control. In simulation, **LESSMIMIC** achieves 80–100% success on _PickUp_ and _SitStand_ across extreme object scales (0 _._ 4ˆ to 1 _._ 6ˆ). Notably, it executes 5-task trajectories with 62.1% success and remains viable up to 40 sequential tasks—a horizon where all baselines collapse. Real-world deployment confirms these capabilities transfer reliably across varying object geometries and seat heights. Future work will extend the DF-based representation to articulated and deformable objects, and improve robustness under partial observability. 

## ACKNOWLEDGMENTS 

This work is supported in part by the National Key Research and Development Program of China (2025YFE0218200), the National Natural Science Foundation of China (62376009), the PKU-BingJi Joint Laboratory for Artificial Intelligence, the Wuhan Major Scientific and Technological Special Program (2025060902020304), the Hubei Embodied Intelligence Foundation Model Research and Development Program, and the National Comprehensive Experimental Base for Governance of Intelligent Society, Wuhan East Lake High-Tech Development Zone. 

## REFERENCES 

- [1] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. In _Conference on Robot Learning (CoRL)_ , 2025. 

- [2] Brenna D Argall, Sonia Chernova, Manuela Veloso, and Brett Browning. A survey of robot learning from demonstration. _Robotics and Autonomous Systems_ , 57(5):469–483, 2009. 

- [3] Eugenio Chisari, Nick Heppert, Max Argus, Tim Welschehold, Thomas Brox, and Abhinav Valada. Learning robotic manipulation policies from point clouds with conditional flow matching. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [4] Qiyu Dai, Yan Zhu, Yiran Geng, Ciyu Ruan, Jiazhao Zhang, and He Wang. Graspnerf: Multiview-based 6-dof grasp detection for transparent and specular objects using generalizable nerf. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [5] Kourosh Darvish, Luigi Penco, Joao Ramos, Rafael Cisneros, Jerry Pratt, Eiichi Yoshida, Serena Ivaldi, and Daniele Pucci. Teleoperation of humanoid robots: A survey. _IEEE Transactions on Robotics (T-RO)_ , 39(3):1706–1727, 2023. 

- [6] Alexander Dietrich, Christian Ott, and Alin Albu-Sch¨affer. An overview of null space projections for redundant, torquecontrolled robots. _International Journal of Robotics Research (IJRR)_ , 34(11):1385–1400, 2015. 

- [7] Yushi Du, Yixuan Li, Baoxiong Jia, Yutang Lin, Pei Zhou, Wei Liang, Yanchao Yang, and Siyuan Huang. Learning humanhumanoid coordination for collaborative object carrying. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [8] Yuhui Fu, Feiyang Xie, Chaoyi Xu, Jing Xiong, Haoqi Yuan, and Zongqing Lu. Demohlm: From one demonstration to generalizable humanoid loco-manipulation. _IEEE Robotics and Automation Letters (RA-L)_ , pages 1–8, 2026. 

- [9] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [10] Tuomas Haarnoja, Ben Moran, Guy Lever, Sandy H Huang, Dhruva Tirumala, Jan Humplik, Markus Wulfmeier, Saran Tunyasuvunakool, Noah Y Siegel, Roland Hafner, et al. Learning agile soccer skills for a bipedal robot with deep reinforcement learning. _Science Robotics_ , 9(89):eadi8022, 2024. 

- [11] Kris Hauser. Robust contact generation for robot simulation with unstructured meshes. In _International Symposium on Robotics Research_ , 2016. 

- [12] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous human-to-humanoid wholebody teleoperation and learning. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [13] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning human-to-humanoid 

real-time whole-body teleoperation. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2024. 

- [14] Alexander Herzog, Nicholas Rotella, Sean Mason, Felix Grimminger, Stefan Schaal, and Ludovic Righetti. Momentum control with hierarchical inverse dynamics on a torque-controlled humanoid. _Autonomous Robots_ , 40(3):473–491, 2016. 

- [15] Michael A Hopkins, Alexander Leonessa, Brian Y Lattimer, and Dennis W Hong. Optimization-based whole-body control of a series elastic humanoid robot. _International Journal of Humanoid Robotics_ , 13(01):1550034, 2016. 

- [16] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. In _Conference on Robot Learning (CoRL)_ , 2023. 

- [17] Jemin Hwangbo, Joonho Lee, Alexey Dosovitskiy, Dario Bellicoso, Vassilios Tsounis, Vladlen Koltun, and Marco Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 4(26):eaau5872, 2019. 

- [18] Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2026. 

- [19] Xiaogang Jia, Qian Wang, Anrui Wang, Han A Wang, Bal´azs Gyenes, Emiliyan Gospodinov, Xinkai Jiang, Ge Li, Hongyi Zhou, Weiran Liao, et al. Pointmappolicy: Structured point cloud processing for multi-modal imitation learning. In _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [20] Zhenyu Jiang, Yifeng Zhu, Maxwell Svetlik, Kuan Fang, and Yuke Zhu. Synergies between affordance and geometry: 6- dof grasp detection via implicit representations. In _Robotics: Science and Systems (RSS)_ , 2021. 

- [21] Oussama Khatib, Luis Sentis, Jaeheung Park, and James Warren. Whole-body dynamic behavior and control of human-like robots. _International Journal of Humanoid Robotics_ , 1(01):29– 43, 2004. 

- [22] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra Malik. Rma: Rapid motor adaptation for legged robots. In _Robotics: Science and Systems (RSS)_ , 2021. 

- [23] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, Ri-Zhao Qiu, and Xiaolong Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. In _Robotics: Science and Systems (RSS)_ , 2025. 

- [24] Yitang Li, Zhengyi Luo, Tonghe Zhang, Cunxi Dai, Anssi Kanervisto, Andrea Tirinzoni, Haoyang Weng, Kris Kitani, Mateusz Guzek, Ahmed Touati, Alessandro Lazaric, Matteo Pirotta, and Guanya Shi. Bfm-zero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning. In _Proceedings of International Conference on Learning Representations (ICLR)_ , 2025. 

- [25] Yitang Li, Yuanhang Zhang, Wenli Xiao, Chaoyi Pan, Haoyang Weng, Guanqi He, Tairan He, and Guanya Shi. Hold my beer: Learning gentle humanoid locomotion and end-effector stabilization control. In _Conference on Robot Learning (CoRL)_ , 2025. 

- [26] Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu, Wei Liang, Yixin Zhu, and Siyuan Huang. Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks. In _Conference on Robot Learning (CoRL)_ , 2025. 

- [27] Qiayuan Liao, Takara E. Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C. Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [28] Minghua Liu, Xuanlin Li, Zhan Ling, Yangyan Li, and Hao Su. Frame mining: a free lunch for learning robotic manipulation from 3d point clouds. In _Conference on Robot Learning (CoRL)_ , 2022. 

- [29] Weiheng Liu, Yuxuan Wan, Jilong Wang, Yuxuan Kuang, Xuesong Shi, Haoran Li, Dongbin Zhao, Zhizheng Zhang, and He Wang. Fetchbot: Learning generalizable object fetching in cluttered scenes via zero-shot sim2real. In _Conference on Robot Learning (CoRL)_ , 2025. 

- [30] Qingzhou Lu, Yao Feng, Baiyu Shi, Michael Piseno, Zhenan Bao, and C Karen Liu. Gentlehumanoid: Learning upper-body compliance for contact-rich human and object interaction. _arXiv preprint arXiv:2511.04679_ , 2025. 

- [31] Gianni Lunardi, Thomas Corb`eres, Carlos Mastalli, Nicolas Mansard, Thomas Flayols, Steve Tonneau, and Andrea Del Prete. Reference-free model predictive control for quadrupedal locomotion. _IEEE Access_ , 12:689–698, 2023. 

- [32] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Casta˜neda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, Xingye Da, Runyu Ding, Cyrus Hogg, Lina Song, Edy Lim, Eugene Jeong, Tairan He, Haoru Xue, Wenli Xiao, Zi Wang, Simon Yuen, Jan Kautz, Yan Chang, Umar Iqbal, Linxi ”Jim” Fan, and Yuke Zhu. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [33] Federico L Moro and Luis Sentis. Whole-body control of humanoid robots. In _Humanoid Robotics: a Reference_ , pages 1161–1183. Springer Dordrecht, 2019. 

- [34] Yoshihiko Nakamura, Hideo Hanafusa, and Tsuneo Yoshikawa. Task-priority based redundancy control of robot manipulators. _International Journal of Robotics Research (IJRR)_ , 6(2):3–15, 1987. 

- [35] Stanley Osher and James A Sethian. Fronts propagating with curvature-dependent speed: Algorithms based on hamiltonjacobi formulations. _Journal of Computational Physics_ , 79(1): 12–49, 1988. 

- [36] Jia Pan, Sachin Chitta, and Dinesh Manocha. Fcl: A general purpose library for collision and proximity queries. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2012. 

- [37] Xue Bin Peng. Mimickit: A reinforcement learning framework for motion imitation and control. _arXiv preprint arXiv:2510.13794_ , 2025. 

- [38] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions on Graphics (TOG)_ , 37(4):1–14, 2018. 

- [39] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (TOG)_ , 40(4):1–20, 2021. 

- [40] Michael Posa and Russ Tedrake. Direct trajectory optimization of rigid body dynamical systems through contact. In _Tenth Workshop on the Algorithmic Foundations of Robotics_ , 2013. 

- [41] Carlos Quintero-Pena, Wil Thomason, Zachary Kingston, Anastasios Kyrillidis, and Lydia E Kavraki. Stochastic implicit neural signed distance functions for safe motion planning under sensing uncertainty. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- [42] St´ephane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to noregret online learning. In _International Conference on Artificial Intelligence and Statistics (AISTATS)_ , 2011. 

- [43] Stefan Schaal. Is imitation learning the route to humanoid robots? _Trends in Cognitive Sciences_ , 3(6):233–242, 1999. 

- [44] John Schulman, Yan Duan, Jonathan Ho, Alex Lee, Ibrahim Awwal, Henry Bradlow, Jia Pan, Sachin Patil, Ken Goldberg, and Pieter Abbeel. Motion planning with sequential convex optimization and convex collision checking. _International Journal of Robotics Research (IJRR)_ , 33(9):1251–1270, 2014. 

- [45] Luis Sentis and Oussama Khatib. Synthesis of whole-body 

   - behaviors through hierarchical control of behavioral primitives. _International Journal of Humanoid Robotics_ , 2(04):505–518, 2005. 

- [46] Bokui Shen, Fei Xia, Chengshu Li, Roberto Mart´ın-Mart´ın, Linxi Fan, Guanzhi Wang, Claudia P´erez-D’Arpino, Shyamal Buch, Sanjana Srivastava, Lyne Tchapmi, et al. igibson 1.0: A simulation environment for interactive tasks in large realistic scenes. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2021. 

- [47] Minseok Song, JeongHo Ha, Bonggyeong Park, and Daehyung Park. Implicit neural-representation learning for elastic deformable-object manipulations. In _Robotics: Science and Systems (RSS)_ , 2025. 

- [48] Chen Tessler, Yoni Kasten, Yunrong Guo, Shie Mannor, Gal Chechik, and Xue Bin Peng. Calm: Conditional adversarial latent models for directable virtual characters. In _ACM SIGGRAPH Conference Papers_ , 2023. 

- [49] Jacob Varley, Chad DeChant, Adam Richardson, Joaqu´ın Ruales, and Peter Allen. Shape completion enabled robotic grasping. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2017. 

- [50] Huayi Wang, Wentao Zhang, Runyi Yu, Tao Huang, Junli Ren, Feiyu Jia, Zirui Wang, Xiaojie Niu, Xiao Chen, Jiahe Chen, Qifeng Chen, Jingbo Wang, and Jiangmiao Pang. Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system. _arXiv preprint arXiv:2510.11072_ , 2025. 

- [51] Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [52] Zhenjia Xu, Zhanpeng He, Jiajun Wu, and Shuran Song. Learning 3d dynamic scene representations for robot manipulation. In _Conference on Robot Learning (CoRL)_ , 2020. 

- [53] Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao, Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng, Guanya Shi, Trevor Darrell, Koushil Sreenath, and Shankar Sastry. Leverb: Humanoid whole-body control with latent vision-language instruction. _arXiv preprint arXiv:2506.13751_ , 2025. 

- [54] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C. Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [55] Wen Yang and Wanxin Jin. Contactsdf: Signed distance functions as multi-contact models for dexterous manipulation. _IEEE Robotics and Automation Letters (RA-L)_ , 2025. 

- [56] Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C. Karen Liu, and Jiajun Wu. Visualmimic: Visual humanoid locomanipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- [57] Yanjie Ze, Zixuan Chen, Joao Pedro Ara´ujo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, and C Karen Liu. Twist: Teleoperated whole-body imitation system. In _Conference on Robot Learning (CoRL)_ , 2025. 

- [58] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C. Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [59] Ryan S Zesch, Vismay Modi, Shinjiro Sueda, and David IW Levin. Neural collision fields for triangle primitives. In _SIGGRAPH Asia Conference Papers_ , 2023. 

- [60] Xiang Zhang, Changhao Wang, Lingfeng Sun, Zheng Wu, Xinghao Zhu, and Masayoshi Tomizuka. Efficient sim-toreal transfer of contact-rich manipulation skills with online 

admittance residual learning. In _Conference on Robot Learning (CoRL)_ , 2023. 

- [61] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Jiangran Lyu, Huaping Liu, He Wang, and Li Yi. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

- [62] Siheng Zhao, Yanjie Ze, Yue Wang, C. Karen Liu, Pieter Abbeel, Guanya Shi, and Rocky Duan. Resmimic: From general 

- motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 

- [63] Haoyi Zhu, Yating Wang, Di Huang, Weicai Ye, Wanli Ouyang, and Tong He. Point cloud matters: Rethinking the impact of different observation spaces on robot learning. In _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

## APPENDIX A 

## THE **LESSMIMIC** FRAMEWORK 

This section provides additional implementation details for the three training stages introduced in Sec. III. We elaborate on network architectures, training procedures, and reward formulations to facilitate reproducibility and clarify key design choices. All training hyperparameters are summarized in Tab. A1. 

## _A. Interaction Skill Pre-Training_ 

During interaction skill pre-training, we learn a base policy _π_ base that maps DF-based interaction representations to wholebody actions. Rather than training on static offline data, the policy is trained via DAgger-style distillation using trajectories generated by rolling out _π_ base itself, allowing the training distribution to track the student’s evolving behavior. 

_Teacher Policy:_ The effectiveness of behavior cloning depends directly on the quality of the demonstrations provided by the teacher. To provide the student policy with initial weights capable of physically valid interactions, the teacher must achieve a high success rate on the collected interaction dataset. We therefore employ ResMimic [62] as _π_ mimic, which augments standard motion tracking with a residual module specifically designed to compensate for dynamic mismatches that arise during contact-rich interaction. This choice ensures that the expert demonstrations are not only kinematically reasonable but also physically feasible under full simulation dynamics—a critical property for the downstream behavior cloning objective. 

_Network Architecture:_ We employ a Transformer-based architecture to jointly model the observation structure, interaction encoding, and policy learning objective. The Trans- 

TABLE A1: **Training hyperparameters for each stage of the LESSMIMIC pipeline.** All three stages—interaction skill pre-training, discriminative post-training, and policy distillation—share the same policy architecture but differ in their optimization configurations. The batch size notation _M_ ˆ 8 denotes _M_ samples across 8 parallel environments. 

|**Hyperparameter**|**Symbol**|**Value**|
|---|---|---|
|**Interaction Skill Pre-training**|||
|Learning rate|_η_pre|1ˆ10<sup>´3</sup>|
|Batch size|_B_pre|4096ˆ8|
|Number of training iterations|_N_pre|24_,_000|
|Optimizer|Adam|–|
|**Discriminative Post-Training**|||
|Policy learning rate|_η_pol|1ˆ10<sup>´3</sup><br>|
|Discriminator learning rate|_η_disc|2ˆ10<sup>´4</sup>|
|Discount factor|_γ_|0_._99|
|Reward weight|_λ_|1_._5<br>|
|Entropy coefficient|_α_ent|5ˆ10<sup>´4</sup>|
|Number of environments|_N_env|4096ˆ8|
|Number of environment steps|_N_rl|240_,_000|
|**Policy Distillation**|||
|Learning rate|_η_dist|1ˆ10<sup>´3</sup>|
|Batch size|_B_dist|2048ˆ8|
|Number of distillation iterations|_N_dist|120_,_000|


former’s ability to capture long-range temporal dependencies across the interaction history makes it particularly well-suited for multi-skill whole-body control, where the relevant geometric context may span many time steps. Critically, this design aligns training-time supervision with inference-time observation settings while eliminating any dependency on reference motions during deployment. 

_Observations._ The observation provided to _π_ base at time step _t_ is defined as 


where _o_ prop denotes humanoid proprioceptive states, including joint DoF positions and velocities; _c_<sup>root</sup> _t_ is a sparse target root trajectory command specifying the desired root motion; and _zt_ is the DF-based interaction latent defined in Eq. (2) of the main paper. Importantly, this observation contains no reference motion or task-specific supervision signal, and exactly matches the observation structure used at inference time. This design choice is deliberate: by training _π_ base under the same observation constraints it will face at deployment, we avoid the distributional mismatch that would otherwise arise if the policy were trained with privileged information and then deployed without it. 

_Interaction Encoder._ The interaction history _It_ “ t _ut_ ´ _l_ `1 _, . . . , ut_ u captures the recent geometric evolution between the humanoid and the object across a temporal window of length _l_ . To process this sequence into a form suitable for policy conditioning, we utilize a VAE to encode each pertimestep feature _u_ into a low-dimensional latent space. Specifically, the VAE encoder maps each _u_ to a latent representation _z_ using the reparameterization trick to maintain end-to-end differentiability during training. Both encoder and decoder are implemented as MLPs with ReLU activations. The resulting sequence of latents t _zt_ ´ _l_ `1 _, . . . , zt_ u is then concatenated to form a compact, structured geometric summary of the interaction history, which is passed as input to the policy network. The VAE bottleneck serves two complementary purposes: it smooths out sensor noise present in the raw DF measurements, and it provides a fixed-dimensional input to the policy regardless of the temporal window length _l_ , simplifying the policy architecture. 

_Policy Architecture._ The base policy _π_ base is implemented as a Transformer that takes as input the concatenation of proprioception _o_ prop, root command _ct_<sup>root</sup> , and interaction latent _zt_ , and outputs whole-body joint actions. All hidden layers use ReLU activation functions; the final output layer uses a linear activation to allow unconstrained action outputs. Notably, the same policy architecture is used across all three training stages—pre-training, post-training, and visual-motor distillation—with only the training objective, supervision signal, and environment configuration varying between stages. This architectural consistency simplifies the overall pipeline and ensures that the weights learned during pre-training can be directly carried over to subsequent stages without any architectural modification. 

TABLE A2: **Reward components used in discriminative post-training.** The composite reward consists of task and style rewards that drive interaction quality, and regularization penalties that ensure motion stability and physical safety. Interaction Style operates on the DF-based interaction latent _zt_ via the AIP discriminator; Motion Style operates on the full robot state via the AMP discriminator to encourage natural gait and posture. Weights listed are baseline values and may be adjusted per task. 

|**Reward Term**|**Formulation**|**Weight **|**Description**|
|---|---|---|---|
|**Task and Style Rewards**||||
|Root Tracking|´}_x_<sup>root</sup><br>_t_<br>´_c_<sup>root</sup><br>_t_<br>}<sup>2</sup>|1_._0|Follow target root trajectory without motion references.|
|Interaction Style|Eq. (6)|2_._0|Discriminator-based prior on distance-field representation.|
|Motion Style|1´0_._25p_D_p_s_q ´1q<sup>2</sup>|1_._0|Discriminator-based motion prior for natural gait/posture.|
|Object Tracking|expp´}_x_<sup>obj</sup><br>_t_<br>´˜_x_<sup>obj</sup><br>_t_ <sup>}2{</sup><sup>_σ_2q</sup>|1_._0|Ensures object follows the desired manipulation trajectory.|
|**Regularization and Penalties**||||
|Action Reg.|}∆_at_}<sup>2</sup>|5_._0|Penalizes abrupt changes to improve control stability.|
|Termination|Constant|´10_._0|Applied upon early termination (falls or loss of balance).|
|Joint Limit|_n_exceed|´5_._0|Penalty when joints exceed specified soft limits.|


_Teacher–Student Setup:_ The teacher–student framework is designed around a deliberate asymmetry in the information available to each policy. The teacher _π_ mimic follows a motion-tracking formulation with residual learning, granting it access to privileged information including full-body reference motions via _o_ mimic. This privileged access enables _π_ mimic to generate high-quality, physically valid interaction trajectories even for complex contact-rich scenarios. The student _π_ base, by contrast, operates solely on _o_ base, which excludes all reference motion information. This asymmetric information design is intentional: it forces the student to ground its behavior entirely in the DF-based interaction latent _zt_ rather than relying on reference cues, ensuring that the learned policy is fully compatible with reference-free inference at deployment. The teacher’s role is thus not to be imitated directly at inference, but to provide a high-quality supervision signal during training that helps the student discover effective interaction strategies expressible within the reference-free observation space. 

_Training Objective:_ Interaction skill pre-training is performed using behavior cloning rather than reinforcement learning. No task-specific reward is introduced at this stage; the sole objective is to minimize the discrepancy between the actions predicted by _π_ base and those generated by _π_ mimic on the same states: 


where _o_ mimic includes privileged observations and reference motions available only to the teacher and not at inference time. To mitigate covariate shift between the supervised training distribution and the student’s own rollout distribution, we adopt a DAgger-style procedure [42]: at each training iteration, _π_ base is rolled out in the environment to generate on-policy trajectories, and _π_ mimic is queried at each encountered state to provide corrective action labels. This on-policy data collection is crucial: it ensures that the student learns to recover from the kinds of states it will actually encounter during its own execution, rather than merely fitting the teacher’s behavior on the teacher’s state distribution—a distribution the student may never visit if it deviates even slightly from the expert trajectory. 

_B. Discriminative Post-Training_ 

Discriminative post-training further refines _π_ base to improve robustness and generalization under novel object geometries and interaction conditions. This stage retains the same policy architecture and observation structure as interaction skill pretraining, but differs fundamentally in its training objective, supervision signal, and environment configuration. The key motivation is that behavior cloning on a fixed dataset, however high-quality, inevitably encourages the policy to memorize specific kinematic trajectories rather than learning the underlying geometric rules of interaction. Post-training addresses this by exposing the policy to procedurally varied geometries under a geometry-aware adversarial supervision signal that rewards valid interaction patterns regardless of the specific object shape or scale encountered. 

_Training Setup:_ Post-training is conducted in a procedurally augmented simulation environment in which object geometry, scale, and physical properties are randomized across episodes. This procedural variation is essential: it prevents the policy from overfitting to the specific object configurations seen during pre-training, and forces it to discover interaction strategies that generalize across the geometric distribution. In contrast to pre-training, no reference motions are available during this stage, and motion-tracking losses are deliberately excluded. Introducing motion-tracking rewards here would be counterproductive, as the reference motions were collected at a fixed object geometry and would not constitute valid interaction guidance for novel shapes and scales. The policy is instead optimized using reinforcement learning with a geometry-aware reward signal described below. 

_Adversarial Interaction Prior:_ To provide a transferable supervision signal without relying on task-specific shaping rewards, we introduce AIP, implemented via a discriminator _D_ p¨q. The key design choice is that the discriminator operates solely on the DF-based interaction latent _zt_ rather than on the full robot state. This is crucial: by conditioning on the geometric interaction signature rather than absolute joint configurations, the discriminator captures what a valid interaction looks like in geometric terms—an approach-contact-release pattern expressed in local DF coordinates—without encoding 

any information about the specific kinematic template used to achieve it. The discriminator is trained to distinguish interaction latents generated by the policy on novel objects from those stored in a reference interaction buffer _B_ ref collected during pre-training, using a least-squares GAN objective: 


where _B_ ref denotes interaction latent samples drawn from the reference buffer and _z_ „ _π_ denotes latents generated by the current policy during rollout. The least-squares formulation is preferred over the standard GAN cross-entropy objective for its more stable gradient behavior during adversarial training. 

_Policy Optimization:_ The policy is trained with reinforcement learning using a composite reward of the form 


where _r_ task encourages tracking of the root-level command, _r_ interact is derived from the AIP discriminator output, and _r_ style is derived from an AMP [39] discriminator that regularizes the naturalness of the robot’s full-body motion. The separation between _r_ interact and _r_ style is intentional: _r_ interact operates on the geometric interaction signature _zt_ and rewards valid contact patterns, while _r_ style operates on the full robot state and penalizes unnatural or physically implausible motion. Together, they provide complementary supervision—one ensuring the interaction is geometrically consistent, the other ensuring the resulting motion looks natural. Detailed reward formulations and coefficient values are provided in Tab. A2. 

_Key Differences from Pre-Training:_ It is worth summarizing the three essential changes introduced in discriminative post-training relative to the pre-training stage, as they collectively define the post-training’s role in the overall pipeline. First, reference motions are removed entirely from the training setup and replaced by the adversarial AIP supervision signal, which provides geometry-aware guidance without requiring any motion demonstrations. Second, the training environment is procedurally randomized across object geometries, scales, shapes, and physical properties, exposing the policy to a broad distribution of interaction conditions far beyond the pretraining dataset. Third, policy optimization is performed using reinforcement learning rather than behavior cloning, allowing the policy to discover novel interaction strategies not present in the original demonstrations. All other components—network architecture, observation definition, and the DF-based interaction representation—remain unchanged from pre-training, ensuring continuity across stages and allowing the posttraining to build directly on the stable initialization provided by behavior cloning. 

## APPENDIX B EXPERIMENTS 

This section provides supplementary details for the experimental evaluation presented in Sec. IV, covering domain randomization strategies, reward design, baseline implementations, and evaluation metrics. 

## _A. Domain Randomization_ 

Extensive domain randomization is applied during both post-training and policy distillation to improve robustness and facilitate sim-to-real transfer. Randomization spans six complementary dimensions that collectively expose the policy to a broad distribution of interaction conditions. 

_Object Geometry:_ For each episode, object geometry is randomized by jointly sampling scale and shape. Scale factors are drawn independently along each spatial dimension, allowing both uniform scaling and mild anisotropic deformation to avoid overfitting to isotropic objects. Object shape is alternated between box-like and cylindrical primitives for applicable tasks. Object orientation and placement are further perturbed within bounded ranges to prevent the policy from exploiting canonical initial poses. 

_Physical Properties:_ Object mass, surface friction coefficients, and contact restitution are randomized independently at the start of each episode. This exposes the policy to variations in inertial response and contact dynamics that are difficult to model accurately in simulation, encouraging stable interaction under uncertain physical parameters—a property critical for real-world deployment where these parameters are never precisely known. 

_Initial Conditions:_ The initial poses of both the humanoid and the manipulated objects are perturbed with small translational and rotational offsets. Joint configurations are randomized around nominal standing poses while maintaining balance constraints. This prevents the policy from learning to exploit fixed initial configurations, which would cause it to fail when deployed in environments where precise initialization is unavailable. 

_Command Perturbation:_ Target root trajectory commands are injected with bounded stochastic noise in both position and heading direction. This encourages the policy to remain stable under imperfect command execution—an important property for long-horizon task composition, where small tracking errors can compound across successive interaction phases. 

_Actuation Noise:_ During post-training, zero-mean Gaussian noise is added to the policy’s action outputs before they are applied to the low-level whole-body controller. This simulates actuation uncertainty arising from motor variability and controller latency, and has been found to improve control smoothness and stability during both training and real-world deployment. 

_Perceptual Randomization:_ For vision-based policy distillation, egocentric depth observations are augmented with camera pose jitter, depth quantization artifacts, random dropout, and additive sensor noise. Camera extrinsic parameters are additionally randomized across episodes to improve robustness to mounting inaccuracies that are common when deploying onboard sensors on a physical humanoid platform. 

## _B. Reward Design_ 

The reward function used during discriminative posttraining is summarized in Tab. A2. The overall reward structure is organized around two complementary objectives: pri- 

mary rewards that drive task completion and interaction quality, and auxiliary regularization terms that stabilize training and promote safe long-horizon execution. 

The primary rewards consist of four components. Root trajectory tracking penalizes deviation of the humanoid’s root position from the commanded trajectory, providing the primary task-level signal without requiring any motion reference. Interaction style, derived from the AIP discriminator operating on the DF-based interaction latent _zt_ , encourages the policy to reproduce geometrically consistent interaction patterns across object geometries. Motion style, derived from an AMP [39] discriminator operating on the full robot state, regularizes the policy toward natural and physically plausible humanoid motion. Object tracking provides an additional task-level signal by rewarding the policy when the manipulated object follows its desired trajectory within a tolerance _σ_ . 

The auxiliary regularization terms address practical concerns that arise during long-horizon execution and real-world deployment. Action regularization penalizes abrupt changes in control outputs to promote smooth, stable behavior and reduce mechanical wear on the robot. Early termination penalties discourage motions that lead to falls or loss of balance. Soft joint limit penalties prevent excessive joint excursions that could cause actuator overheating or mechanical stress during extended real-world operation—a concern that becomes increasingly important as task horizons grow. Together, these components form a balanced reward structure that enables robust interaction learning while maintaining motion naturalness and physical safety. 

ing policy is augmented with a learned residual controller to compensate for contact dynamics. We train a single ResMimic policy across all tasks using task-specific reference motions. During evaluation, the policy tracks the same reference motions without modification under object scale variation. 

**VisualMimic** [56] serves as a reference-based baseline that conditions the policy on egocentric visual observations in addition to motion references. Rather than training from scratch, we use the official pre-trained checkpoints provided by the authors to ensure a faithful evaluation. The policy tracks reference motions generated by a visual planner conditioned on egocentric observations, but remains subject to the architecture’s fundamental limitation of not adapting explicitly to unseen object geometries. 

**PhysHSI** [50] is a reference-free baseline that conditions the policy on handcrafted observation features encoding humanoid state and object-relative information. We use the original codebase and pre-trained checkpoints provided by the authors. While PhysHSI uses task-specific reward functions to facilitate interactions, it lacks a unified interaction representation, necessitating separate observation and reward designs for each task—a limitation that prevents it from being applied directly to the long-horizon multi-task setting evaluated in Sec. IV-C. 

For all baselines, simulation parameters are matched to those used by **LESSMIMIC** , and hyperparameters are tuned according to the original papers when available. When hyperparameters are unspecified, we select reasonable defaults to ensure stable training. All baseline results are averaged over three random seeds using identical evaluation protocols. 

## _C. Baselines_ 

## _D. Evaluation Metrics_ 

All baseline methods are evaluated under the same simulator, control frequency, and low-level whole-body controller as **LESSMIMIC** . All policies are trained and evaluated on the same task definitions, object configurations, and termination conditions, and no baseline has access to the DF-based interaction representation used by **LESSMIMIC** . Referencebased methods explicitly condition policy execution on motion demonstrations or reference trajectories at inference time, while reference-free methods operate on simplified taskrelevant observations. HDMI and ResMimic are each trained as a single policy that tracks task-specific reference motions across all tasks, while VisualMimic and PhysHSI are trained separately per task using task-specific planners or reward functions. 

**HDMI** [51] is reproduced following the training and inference procedures described in the original paper. Motion references are generated from retargeted human motion data corresponding to each interaction task, and the policy tracks these references using full-body pose and velocity supervision. The reference motions are fixed at a nominal object scale; no adaptation mechanism is applied when object geometry deviates from the training distribution, which is precisely the generalization condition evaluated in our experiments. 

**ResMimic** [62] is reproduced using its residual motionobject co-tracking formulation, in which a base motion track- 

_Success Rate:_ Task success is defined by geometric and contact-based criteria tailored to each task. For _PickUp_ , the task is considered successful if the box is lifted above 0 _._ 3 m from the ground and held stably for at least 3 s. For _SitStand_ , success requires the humanoid to establish stable contact with the chair with the root height falling within r0 _._ 3 m _,_ 0 _._ 6 ms, which filters out near-fall cases where the robot makes incidental low contact. For _Carry_ , the robot must pick up the box, transport it along a given trajectory, and place it at the destination, with a maximum allowable deviation of 0 _._ 6 m at any point during execution. For long-horizon evaluation, the same trajectory-following criterion is applied across all tasks in the composed sequence, with a per-step deviation tolerance of 0 _._ 6 m. 

_Contact Rate:_ For the _Push_ task, discrete success is not a well-defined criterion since the task requires maintaining continuous hand contact rather than reaching a terminal goal state. We therefore evaluate performance using the contact rate _R_ cont, defined as the proportion of time steps during which the humanoid’s end-effectors maintain active contact with the target object. High contact rates indicate sustained and controlled interaction, while low rates suggest flickering or failed contact—both of which would result in the object not being pushed along the desired trajectory. 

_Root Tracking Accuracy:_ For real-world deployment evaluation, discrete task success alone is insufficient to characterize execution quality across repeated trials. We therefore report root trajectory tracking accuracy _R_ acc, which measures how consistently the humanoid follows the commanded root trajectory over the course of task execution. Specifically, we compute the Euclidean distance between the humanoid’s root position and the commanded trajectory at each time step, and report the proportion of time steps for which this distance remains within 0 _._ 6 m. This metric provides a continuous measure of execution stability and is particularly informative for assessing whether performance differences between the MoCap-based and vision-based variants arise from high-level task failure or from degraded trajectory tracking quality. 

