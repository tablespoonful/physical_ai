---
title: "Proprioceptive-visual correspondence enables self-other distinction in humanoid robots"
date: "2026-06-11"
authors: "Yurun Chen; Tianyuan Gao; Yizhong Ge; Shikun Ban; Yizhou Wang; Hongkai Xiong"
url: https://arxiv.org/abs/2606.13222
pdf: https://arxiv.org/pdf/2606.13222
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.13222)** / [論文ページ](https://arxiv.org/abs/2606.13222)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Proprioceptive–visual correspondence enables self-other distinction in humanoid robots** 

**Yurun Chen**<sup>1,2</sup> **, Tianyuan Gao**<sup>3</sup> **, Yizhong Ge**<sup>1</sup> **, Shikun Ban**<sup>4</sup> **Yizhou Wang**<sup>3</sup> **, Hongkai Xiong**<sup>2,5 �</sup> **, Wenjun Zeng**<sup>1,6 �</sup> **, Wentao Zhu**<sup>1,6 �</sup> 

1Eastern Institute of Technology, Ningbo 2Shanghai Jiao Tong University 3Peking University 4Carnegie Mellon University 5East China Normal University 6Ningbo Institute of Digital Twin 

�Corresponding authors 

## **Abstract** 

Distinguishing self from others is a prerequisite for social intelligence, yet humanoid robots that increasingly share workspaces with humans still lack this ability. Here we show that a humanoid robot can learn selfother distinction from proprioceptive–visual correspondence, without any identity labels or kinematic models. Once established, this distinction bootstraps a predictive self-model that maps joint configurations to threedimensional body occupancy, capturing how the robot’s body changes with action. In multi-agent scenes involving humans or morphologically identical robots, the system reliably identifies itself, learns a 3D self-model, and supports downstream tasks including target reaching, collision-aware motion planning, and human-to-robot motion retargeting. Together, these results outline a route toward bodily self-representation in robots that act and coordinate alongside others in shared physical environments. Project page: https://euron-zc.github.io/humanoid-self-model/. 

## **1 Introduction** 

Distinguishing self from others is a fundamental capability for social intelligence (Gallagher, 2000; Decety & Sommerville, 2003; Steinbeis, 2016). Before an agent can imitate a demonstrator, coordinate with a partner, or simply avoid colliding with a bystander, it must resolve a prior question: “which body is mine?” Cognitive science points to proprioceptive–visual correspondence as a key mechanism: infants as young as three to five months detect the contingency between proprioceptive signals and visual feedback of their own limb movements, both temporally (Bahrick & Watson, 1985; Rochat & Striano, 2000) and spatially (Rochat & Morgan, 1995; Schmuckler, 1996), and use this match to distinguish self from non-self. In adults, synchrony between felt and seen body movements can induce body ownership even in the absence of tactile cues (Kalckert & Ehrsson, 2012), and subjects distinguish selfgenerated from observed movements by detecting mismatches between motor commands and visual feedback (Jeannerod, 2003). In each case, internal bodily signals serve as a private reference against which visible bodies are evaluated. 

The same question now confronts robots (Gold & Scassellati, 2009; Stoytchev, 2011; Lanillos et al., 2020). Humanoid robots are entering social environments (Song & Kim, 2022; Tong et al., 2024; Gu et al., 2026), where they coexist with humans and morphologically identical peers. To act effectively in such settings, they need to solve two coupled problems: _selfother distinction_ , identifying which body in the scene is itself, and _self-modeling_ , acquiring a predictive representation of that body and how it changes with action (Bongard et al., 2006; Kwiatkowski & Lipson, 2019), a capacity that recent work has shown can be learned from proprioceptive–visual experience in single-agent settings (Chen et al., 2022; Schulze & Lipson, 2024; Hu et al., 2025b;a). These two problems are logically coupled: distinguishing self from other presupposes some notion of one’s own body, yet learning about one’s 

1 


Figure 1: **Framework overview. a,** A humanoid robot in a shared scene faces two coupled problems: identifying which visible body is its own, and predicting how that body should appear under a given proprioceptive state. **b,** From only proprioceptive states and visual observations, the proposed framework first distinguishes self from other, then learns a kinematics-free self-model. **c,** Together, self-other distinction and the learned self-model enable downstream tasks including target reaching, collision-aware motion planning, and human-to-robot motion retargeting. 

body presupposes knowing which body to attend to. In this work, we consider the most natural and the most challenging instance of this problem: an agent that has _no identity label_ indicating which body in the scene is its own and _no prior knowledge_ of its own morphology: no kinematic model, no geometric description, nothing that specifies what it should look like. From only raw proprioceptive signals and visual observations, it needs to address both questions. 

A clue to this chicken-and-egg dilemma comes from developmental psychology: in human children, perceptual self-other distinction emerges before the maturation of detailed body representations (Brownell et al., 2007). Motivated by this ordering, we follow the same progression: we present a framework in which a humanoid robot first visually distinguishes itself from others in multi-agent scenes and then, from that distinction, learns a predictive self-model (Fig. 1a). 

For self-other distinction, our key insight is that the current proprioceptive state should match a specific body in the current frame (though which one is unknown), but is unlikely to match any body observed at a different moment. This structure provides natural contrastive 

2 

supervision without any explicit identity labels, and we show that it contains sufficient information for learning instance-level discrimination. For self-modeling, the distinguished self-masks supervise a neural occupancy field conditioned on proprioceptive states. The field predicts the probability of arbitrary 3D points belonging to the robot’s body, requiring no predefined kinematic model. In this way, self-other distinction provides the learning signal from which the self-model emerges. We show that accurate self-other distinction is sufficient to bootstrap a faithful self-model in a fully self-supervised manner. 

We evaluate the framework on a 29-degree-of-freedom (DoF) humanoid robot in both simulated and real-world multi-agent scenes. From only proprioceptive states and visual observations, and without any predefined kinematic model or identity label, the system achieves robust self-other distinction, learns a self-model that predicts 3D body occupancy, and supports downstream tasks including target reaching, collision-aware motion planning, and human-to-robot motion retargeting. These results suggest that proprioceptive–visual correspondence alone provides a sufficient basis for self-other distinction and self-modeling, opening a path in which robots acquire knowledge of their own bodies from experience rather than from manual specification. 

## **2 Results** 

We evaluate the framework by asking three questions: whether proprioception and vision alone can distinguish the robot’s own body from others without identity labels or kinematic priors; whether the resulting self-mask can supervise a kinematics-free self-model; and whether the learned self-model can support downstream physical interaction tasks. Experiments are conducted on a 29-DoF Unitree G1 humanoid robot observed from a fixed external RGB camera. We conduct both simulated and real-world experiments, which serve complementary purposes: simulation provides a controlled setting with accurate ground truth (GT) for quantitative evaluation, whereas real-world data test whether the framework remains robust under realistic conditions and human-robot interaction. 

#### **2.1 Distinguishing self from others with proprioception** 

We first ask whether a humanoid robot can identify its own body in a multi-agent scene using only proprioception and vision. Given the robot’s proprioceptive state (proprio.) and a set of candidate body masks from the visual frame, the task is to select the one that corresponds to its own body (Fig. 2b). Neither identity labels nor kinematic models are provided. The only learning signal is the temporal co-occurrence of proprioceptive states and visual observations, collected while the robot moves in scenes that also contain another agent. 

The key intuition is that this correspondence holds only within a frame. Within the current frame, a specific candidate mask corresponds to the robot, though we do not know which. In a frame captured at a different time, the candidate masks are unlikely to match the current proprioceptive state, because the robot will generally have moved to a different configuration. To exploit this asymmetry, two encoders embed the proprioceptive state and each candidate mask into a shared space. The per-mask similarities are then fused via attention into a single frame-level score. We treat the frame paired in time with the current state as the positive and all other frames in the batch as negatives, yielding a fully self-supervised contrastive signal that never requires labelling the correct mask. The full architecture and training protocol are described in the Methods. We train and test the model independently in two settings: 25,667 real-world human-robot frames, and, to probe whether self-identification survives a morphologically matched distractor, 9,000 simulated two-humanoid frames in which the distractor is another humanoid robot. 

We compare our model against zero-shot vision-language model (VLM) baselines and a direct fusion variant in both evaluation settings (Fig. 2a). The VLM baselines include two open-source models, LLaVA v1.6 (Liu et al., 2023) and InstructBLIP (Dai et al., 2023), as well as two closed-source frontier models, GPT-5.5 and Gemini 3.1 Pro Preview. Our model exceeds 99.5% accuracy in both, showing that the proposed approach robustly identifies 

3 


Figure 2: **Self-other distinction from proprioception. a,** Held-out accuracy across methods in two evaluation settings: a human-robot scene and a two-humanoid scene with a morphologically matched distractor. Comparisons include direct fusion training and visionlanguage baselines. **b,** Qualitative examples in which the robot selects its own candidate mask from a scene containing a distractor; the selected mask is marked by a check symbol. **c,** In the robot–robot setting with two morphologically identical robots, per-frame cosine similarity of the proprioceptive state to the self mask (proprio.–self) against its similarity to the other robot’s mask (proprio.–other), before and after training. **d,** Distributions of synchronous (proprioception and robot mask from the same frame) and asynchronous (from different frames) cosine similarities, before and after training. **e,** t-SNE projections (Van der Maaten & Hinton, 2008) of proprioceptive-state embeddings and humanoid robot mask embeddings before and after training. 

the robot’s own body across simulated and real-world settings. These VLMs, given the same visual scene and joint angles, perform at or only marginally above chance, indicating that current VLMs cannot bind a specific configuration of joint angles to the corresponding visible body. The direct fusion variant, which averages per-mask similarity scores rather than fusing them through attention, also degrades markedly: averaging gives the proprioceptionuncorrelated distractor mask equal weight in the frame-level score, whereas attention lets the candidate most consistent with proprioception dominate. This gap is most pronounced 

4 

in the human-robot setting. Figure 2b provides qualitative examples: across different poses, the model consistently selects the robot mask rather than the distractor mask. 

An alternative explanation in the human-robot setting is that the model might rely on appearance rather than proprioception, since the human distractor looks different from the robot. To rule this out, we study the problem from two perspectives. First, we turn to the robot–robot setting, where the two candidates are morphologically identical and appearance offers no cue at all. In addition to the accuracy of _>_ 99.5% in this setting (Fig. 2a), we examine the underlying similarities directly, comparing the proprioceptive feature against the self mask and against the other robot’s mask in each frame; after training, the proprioceptive feature stays consistently closer to the self mask than to the other robot’s mask in the same frame (Fig. 2c), so the model still selects the right body when the two are visually indistinguishable. Second, we ask whether the proprioceptive state aligns specifically with the visual observation from the same moment, comparing the synchronous similarity cos( **_f_** state<sup>_i_,</sup><sup>**_f_**</sup><sup>_i_</sup> image,robot<sup>), between the proprioceptive feature</sup><sup>**_f_**</sup><sup>_i_</sup> state<sup>and the robot mask from</sup> 

the same frame, against the asynchronous similarity cos( **_f_** state<sup>_i_,</sup><sup>**_f_**</sup><sup>_j_</sup> image,robot<sup>),betweenthe</sup> same feature and the robot mask from a different frame _j̸_ = _i_ (Fig. 2d); after training, the synchronous similarity is sharply higher than the asynchronous similarity. The same temporal correspondence is also visible in the embedding space: t-SNE projections (Van der Maaten & Hinton, 2008) (Fig. 2e) show that before training, proprioceptive-state embeddings and robot mask embeddings occupy separate regions and even same-frame pairs lie far apart, whereas after training the two modalities collapse onto the same region and pairs from the same frame map to nearby points. Together, these results suggest that the model binds the current proprioceptive state to the robot configuration at that moment, rather than to a generic robot silhouette. 

#### **2.2 Self-other distinction enables self-modeling** 

We next ask whether proprioceptive–visual correspondence can also support self-modeling. A person can imagine the position of their limbs even with their eyes closed; can a robot do the same? We formulate this as predicting a continuous three-dimensional (3D) occupancy field of the robot’s body from its joint state. 

Concretely, we model the humanoid body with a pose-conditioned implicit field that maps a 3D query point to two scalar values: a body density predicting whether the point belongs to the robot, and a view-dependent visibility predicting, for a given camera ray, how much that point contributes to the observation. To make this formulation tractable for a 29-DoF humanoid, the proprioceptive state is encoded with a part-aware encoder that processes the torso and bilateral limbs separately, while sampled 3D points and viewing directions use sinusoidal positional encoding. We train the field from 2D self-mask supervision using a bounded volumetric mask renderer, which accumulates density and visibility only within the calibrated near–far range of the robot body. This adapts neural radiance field (NeRF)-style transmittance (Mildenhall et al., 2020; Gao et al., 2022) to binary silhouette supervision and avoids treating the far end of the ray as an unbounded absorber. Qualitative and quantitative comparisons with reconstruction variants and an adapted reconstruction baseline further show that both the part-aware architecture and the bounded visibility-aware renderer contribute to reconstruction fidelity across held-out poses (Supplementary Figs. 1 and 2). 

The learned self-model produces coherent predictions in both simulation and the real world (Fig. 3a-b). To visualize the prediction, we threshold the learned density field to obtain a point cloud of the robot’s body. This point cloud tracks the body across poses and orientations, and remains confined to the robot even when a human is present in the scene. The self-other boundary established in the previous section is therefore preserved in the 3D self-model. Notably, the self-model is trained entirely from the pseudo-GT masks produced by self-other distinction. Here, “Ours” denotes training with the masks selected by the first-stage self-other distinction module. With self-other distinction at _>_ 99.5% accuracy, the resulting fidelity of the self-model closely matches an oracle model trained on GT masks 

5 

### **a** 


### **b** 


### **c** 


### **d** 

|**Metrics**|||**Pseu**|**do-GT acc**|**uracy**|||
|---|---|---|---|---|---|---|---|
||**50%**|**60%**|**70%**|**80%**|**90%**|**100%**|**Ours**|
|IoU_"_|0.107|0.522|0.716|0.770|0.867|**0.902**|0.902|
|MSE_#_|0.0280|0.0191|0.0119|0.0084|0.0037|**0.0024**|0.0024|
|MAE_#_|0.0558|0.0445|0.0331|0.0266|0.0119|**0.0055**|0.0055|
|CD_#_|0.9139|0.4518|0.1261|0.0970|0.0692|**0.0664**|0.0670|


**Bold** : best; underline: second best, based on unrounded metrics. 

Figure 3: **Kinematics-free self-modeling from proprioception. a,** Simulated examples in which the learned self-model predicts robot body occupancy under different poses and viewpoints. **b,** Real-world examples in which the predicted occupancy is projected onto the robot while a human distractor remains excluded. **c,** Qualitative effect of the percentage of correct pseudo-GT masks on the learned self-model. At high pseudo-GT accuracy, the predicted robot body remains identifiable but begins to show ghost occupancy around the distractor; as accuracy falls further, the distractor response strengthens and the self-other boundary breaks down. **d,** Quantitative self-model fidelity as a function of the percentage of correct pseudo-GT masks, measured by IoU, MSE, MAE and Chamfer Distance. Performance with the pseudo-GT masks produced by self-other distinction ( _>_ 99.5% accuracy) closely matches the oracle trained on GT masks, whereas artificially degraded pseudo-GT masks lead to progressive deterioration. 

6 

(Fig. 3c-d). These results show that it is possible to learn a faithful and stable self-model from imperfect, fully self-supervised supervision. 

To probe how sensitive self-modeling is to the accuracy of self-other distinction, we artificially reduce the percentage of correct pseudo-GT masks by randomly flipping a fraction of self and other masks. Mild corruption still preserves the main body shape but introduces ghost occupancy around the distractor, whereas stronger corruption makes the predicted body occupancy increasingly diffuse and can cause the self-other boundary to collapse (Fig. 3c). The same trend appears quantitatively: all four metrics deteriorate as the percentage of correct pseudo-GT masks decreases (Fig. 3d). Self-other distinction is not merely a precursor to self-modeling, because its accuracy directly determines whether self-modeling can succeed. The detailed design and full evaluation protocol are described in the Methods. 

#### **2.3 From self-model to physical interaction** 

Having shown that the robot can distinguish itself from others and learn a 3D representation of its own body, we next ask whether the knowledge of its own body can guide physical interaction with the real world. Each task can be cast as a spatial constraint on the robot’s body, whether the goal is to reach a target, avoid an obstacle, or imitate a demonstrated pose. Because the self-model provides a differentiable mapping from joint configurations to 3D body occupancy, these constraints translate into gradients over joint angles, allowing the robot to solve for the configuration that satisfies the task. We test this on three tasks of increasing complexity: target reaching, collision-aware motion planning, and human-torobot motion retargeting. 


Figure 4: **Target reaching and collision-aware motion planning. a,** Target reaching. A human places a tabletop night-light at different positions, and the robot reaches and touches it to light it up, shown from the front and top views. **b,** Collision-aware motion planning through a board with a circular aperture. Starting with the left arm hanging down, the robot raises the arm, passes it through the opening, and reaches the night-light. A temporal sequence is shown from the front and top views. 

We begin with target reaching (Fig. 4a), the most direct test of the self-model as a control interface. Specifically, a human places a small night-light at different positions on a tabletop, and the robot optimizes its seven left-arm joint angles to bring the centre of a hand-specific self-model to the target. The robot hand is approximately 140 mm long and 115 mm wide, and physical tests showed that the night-light could be activated when the optimized hand centre approached within 100 mm of the target. We therefore used 100 mm as the task-level 

7 

success threshold. We repeated the reaching test 50 times across different target placements. The mean best distance was 51.3 mm, and 44 of 50 trials met this criterion, corresponding to an 88.0% success rate. These results show that the self-model provides a differentiable geometric signal sufficient to guide physical reaching. 

Reaching only constrains the position of the hand. A harder test is whether the self-model can also reason about the geometry of the entire arm when the environment imposes constraints along the way. We therefore turn to collision-aware motion planning (Fig. 4b), where the night-light is placed behind a 400 mm _×_ 600 mm planar board with a circular aperture of radius 100 mm, so a direct gradient-descent trajectory toward the target would collide with the board. The seven left-arm joint angles are optimized as in the reaching task, but the learned full-body and hand occupancy models now serve as collision and goal queries inside a target-biased RRT planner. Across 14 constrained planning settings, 10 trajectories reached the target under the same 100 mm task-level success threshold, corresponding to a 71.4% success rate. Across all settings, the mean final distance was 89.3 mm and the average path length was 155.4 waypoints. 


Figure 5: **Human-to-robot motion retargeting.** A human demonstration (upper row) is retargeted to a robot motion sequence (lower row) by optimizing the robot’s joint configuration through the learned self-model. 

We further generalize from controlling a single arm to whole-body motion transfer through human-to-robot retargeting (Fig. 5). To support this, we extend the self-model with multiple part-specific output heads that share a common backbone, with one head for each body part of interest (e.g., hands and feet). More details can be found in Methods. Given a whole-body human demonstration, we extract 3D keypoints for these parts, map them to robot-compatible targets, and optimize the robot’s full 29-DoF configuration so that each predicted body part reaches its target. Because the self-model is a geometric rather than physical representation, the robot is externally supported during retargeting (see Discussion). The resulting robot joint sequence reproduces the human whole-body motion. To quantify this, we measure the per-keypoint distance between the optimized robot body parts and their targets across 50 poses, obtaining a mean error of 36.1 mm, corresponding to approximately 2.7% of the robot body height (1320 mm). This is achieved without any paired human-robot training data. 

## **3 Discussion** 

We have shown that a humanoid robot can identify its own body in a multi-agent scene from proprioceptive–visual correspondence alone, and that this distinction in turn supplies the supervision for a kinematics-free 3D self-model. This builds on self-supervised selfmodeling, previously studied in single-agent settings (Hu et al., 2025b). That prior work assumes the robot is the only body in the scene and demonstrates the idea on a 4-DoF robotic arm, so the question of which body to model does not arise. Our framework removes this assumption and addresses a fundamental question that emerges only in multiagent settings: which body is the self? Selfhood, in this framework, is defined operationally: 

8 

among the bodies visible in the scene, the self is the one whose visual configuration changes in agreement with the robot’s internal state. 

At first glance, self-other distinction and self-modeling appear to be mutually dependent. Yet proprioceptive–visual correspondence breaks this circularity by enabling the robot to recognize its own body without any prior body model, and the resulting distinction in turn bootstraps the supervision needed for self-modeling. The strength of this link is confirmed by the observation that self-model fidelity degrades progressively as self-other distinction accuracy is reduced, with severe degradation producing ghost occupancy and eventual loss of the self-other boundary. Notably, the same developmental ordering is observed in human infants, where perceptual self-other differentiation emerges well before detailed body representations (Brownell et al., 2007), suggesting that this bootstrapping sequence may reflect a general principle rather than a design choice. 

From an engineering perspective, the robot’s body region may be isolated through predefined geometric models or manual annotation, but these approaches presuppose precisely the prior knowledge of the robot’s own body that self-modeling aims to acquire. The more fundamental scientific question is whether proprioceptive–visual correspondence alone, the same mechanism that biological agents rely on, is sufficient to ground both self-other distinction and self-modeling without any such priors. Our results suggest that it is. No explicit identity label or kinematic prior is needed; the temporal coupling between proprioceptive and visual streams is itself a sufficient self-supervised signal. This echoes neurocognitive accounts of body ownership, in which the sense of one’s own body is constructed from the moment-to-moment congruence between proprioceptive and visual signals (Kalckert & Ehrsson, 2012). The fact that even modern VLMs, despite their strong semantic capabilities, fail to recover this binding further supports the view that self-other distinction is not a semantic recognition problem but one that requires learning the cross-modal correspondence from experience. 

Several aspects of the current study suggest natural extensions. First, candidate body masks are produced by an off-the-shelf segmentation and tracking model. In our experiments this front end was reliable enough that segmentation errors did not affect subsequent modeling, but in principle any upstream failure would propagate, and an end-to-end formulation is a natural way to remove this dependency. Second, our evaluation spans human distractors in the real world and morphologically identical humanoid distractors in simulation; scaling to denser scenes with more distractors is a natural next step that the same proprioceptive–visual mechanism should in principle support. Third, the learned self-model is a geometric representation: it maps joint configurations to body occupancy but does not model physics. Consequently, whole-body retargeting is demonstrated with the robot externally supported, because standing balance requires physical reasoning about gravity and contact. Existing systems that achieve free-standing retargeting rely on manually provided kinematic and dynamic models; achieving the same from a learned geometric representation alone, without such priors, is a substantially harder problem that warrants dedicated investigation. Moreover, although we validate the framework on a humanoid robot, the underlying principle, proprioceptive–visual correspondence, is not specific to any particular morphology. The part-aware encoder groups joints by body region rather than relying on humanoid-specific structure, and could in principle be applied to other articulated robots. 

Beyond these extensions, the capability demonstrated here occupies a specific position in the stack of social cognition. Higher-level social competences, such as imitation, coordination and theory of mind, all presuppose that the agent has already established a boundary between self and other, yet current work on these problems operates in settings where this boundary is predetermined. Our framework addresses this prerequisite directly: the learned self-other distinction, together with the self-model it supervises, provides a necessary foundation on which higher-level social competences could be built. More broadly, the building blocks of social cognition may also be acquired progressively from interaction, rather than engineered independently for each task. 

Taken together, these results suggest that bodily self-representation need not be engineered or provided a priori, but can emerge from the cross-modal structure of sensorimotor experi- 

9 

ence alone. Extending this representation to denser social scenes, diverse robot morphologies, and physical reasoning would take a further step toward robots that, like biological agents, come to know their own bodies through experience and act alongside others in shared physical environments. 

10 

## **4 Methods** 


Figure 6: **Method overview. a,** Self-other distinction compares proprioceptive and visual embeddings, selects the self-mask, and trains the alignment with attention-guided contrastive learning. **b,** Kinematics-free self-modeling uses the selected self-mask to learn a pose-conditioned density and visibility field through bounded volumetric mask rendering. 

#### **4.1 Problem formulation and method overview** 

We study kinematics-free self-modeling in a multi-agent visual scene. At time step _t_ , our model takes as input an RGB image _It_ captured by a single fixed-view external camera (Intel RealSense D455, RGB stream only) and the robot’s proprioceptive state from odometry and joint sensing. The full proprioceptive state is 


where **_q_** _t ∈_ **R**<sup>29</sup> denotes the 29-DoF joint configuration, **_r_** _t ∈_ **R**<sup>4</sup> is the root orientation represented as a quaternion, and **_p_** _t ∈_ **R**<sup>3</sup> is the root translation. The image may contain the 

11 

robot body, humans, other robots, and the static scene. The robot is not given an identity label linking its proprioceptive state to any particular visual body, and it is not given a forward-kinematics model, link geometry, CAD model, or Unified Robot Description Format (URDF) file. 

The method contains two modules (Fig. 6). The self-other distinction module uses a 30dimensional proprioceptive state, consisting of the 29 joint angles and the robot’s global yaw, to select the visual candidate whose shape is consistent with the robot’s current state. The self-modeling module then uses the selected self-mask as pseudo-GT supervision to train a 36-dimensional pose-conditioned implicit self-model. This model maps sampled 3D points, viewing directions, and the full robot state to body occupancy and visibility, yielding a differentiable representation that can be used for target reaching, collision-aware motion planning, and human-to-robot motion retargeting. 

#### **4.2 Data collection and input preparation** 

We collect real-world data with a Unitree G1 humanoid robot and a fixed Intel RealSense D455 RGB camera placed 1.93 m in front of the robot at a height of 0.7872 m. Each RGB frame is paired with the robot’s proprioceptive state from odometry and joint sensing. The real-world human-robot dataset contains 25,667 frames with a human distractor in the scene. We additionally generate 9,000 two-humanoid frames in Isaac Gym (Makoviychuk et al., 2021) using the same front-facing camera distance and height, and visualize the simulated scenes in PyBullet (Coumans & Bai, 2016). Candidate masks are extracted from the RGB images before training. Training and validation frames are kept separate, and each training sample uses the same input format: a 30D proprioceptive state and two candidate masks. 

#### **4.3 Self-other distinction from proprioception** 

**Candidate construction.** Candidate masks are extracted from the image using class-agnostic segmentation with the Segment Anything Model (SAM) 3 (Carion et al., 2025). Each training sample contains two candidate instances: one mask corresponding to the ego robot and one distractor mask, where the distractor can be either a human or another robot. Each singleinstance mask has spatial size 174 _×_ 232, and the two masks are placed into a combined 174 _×_ 464 canvas. The model does not use semantic category labels during optimization, and the corresponding evaluation label is updated only for accuracy measurement. 

We use separate pairing protocols for human and robot distractors. In the robot–robot simulated setting, simulated robot samples are divided into two disjoint pools and then randomly paired across pools, so that one robot instance serves as the ego candidate and the other serves as the distractor. In the real-world robot–human setting, each pair of robot and human masks comes from the same captured frame, preserving the real multi-agent scene observed by the camera. 

**Proprioceptive encoding.** The distinction stage excludes root translation to remove the influence of where the robot happens to stand in the scene. This design reflects the movement structure of humanoid robots and humans on the ground: global planar displacement should not determine identity, whereas global heading changes the projected silhouette. We therefore retain only the yaw angle from the quaternion **_r_** _t_ as the global proprioceptive component, while preserving the full-body joint configuration as the local proprioceptive component. The resulting state is 


where _ψt_ is the yaw extracted from **_r_** _t_ . We encode the joint configuration and yaw together with a proprioceptive state encoder, producing an L2-normalized feature **_f_** state. 

**Visual instance encoding.** The two candidate masks are cropped from their respective half-canvas regions and passed independently through an instance encoder. We apply position normalization and scale normalization before visual encoding, reducing the influence of where an agent appears in the image and how large it appears under different camera distances or viewpoints. The normalized masks are then processed by a shared 

12 

image encoder, implemented as a custom CNN encoder for mask regions followed by a projection head, to obtain L2-normalized instance features **_f_** image,1 and **_f_** image,2. Similarities are computed by dot product, 


The predicted self instance is the candidate with the larger similarity. Evaluation accuracy is computed as the proportion of frames in which the argmax similarity selects the robot mask. 

#### **4.4 Two-level self-supervised optimization** 

The main challenge in self-other distinction is that the correct instance is unknown during learning. In each frame, the robot knows its own proprioceptive state, but it does not know which candidate mask corresponds to that state. Conversely, the set of candidates from the same frame is guaranteed to contain the self instance in our training construction. We use this weak structure to form a two-level self-supervised objective. The inner level treats the candidate masks in a frame as a multiple-instance bag and softly selects the instance most compatible with the robot state (Ilse et al., 2018). The outer level supplies the learning signal by contrasting the selected same-frame bag against bags from other frames, whose proprioceptive states are unlikely to match the anchor state when sampled from sufficiently different moments in the motion sequence. 

**Inner level: latent self selection within a frame.** For sample _i_ , the model first compares the proprioceptive feature **_f_** state<sup>_i_with each candidate visual feature</sup><sup>**_f_**</sup><sup>_i_</sup> image, _k_<sup>, obtaining feature</sup> similarities _s_<sup>_i_</sup> _k_<sup>with Equation 3.These similarities are converted into attention weights via</sup> 


where _τa_ controls how sharply the model selects among the candidates. The frame-level visual representation is then formed as a weighted bag feature, 


This operation makes the unknown self-mask a latent variable rather than a supervised label. If a candidate consistently carries visual structure that covaries with the robot’s joint state and heading, it can receive increasing attention across training. If a candidate is a distractor, its shape changes independently of the robot’s proprioception and therefore cannot support stable cross-modal alignment. 

**Outer level: frame-wise contrastive alignment.** The outer level turns this latent selection into a trainable objective. For an anchor state **_θ_** _i_ , the positive visual representation is the bag feature from the same frame, **_f_** bag<sup>_i_.Bag features from other frames in the batch provide</sup> negatives because they are usually associated with different robot states; repeated or nearstatic poses can create occasional false negatives, but these cases are expected to be rare under diverse motion sampling. This temporal contrast is the key source of supervision: the model is rewarded when the bag selected from the current frame is closer to the current proprioceptive state than most bags selected from other frames. With batch size _B_ , the InfoNCE (Oord et al., 2018) objective is 


The denominator includes the positive same-frame bag and all other bags in the batch as negatives. This objective couples the two levels. The contrastive term cannot be minimized by selecting an arbitrary candidate within the frame, because the resulting bag feature 

13 

must also be predictive of the robot’s proprioceptive state relative to other frames. The attention mechanism therefore receives an indirect but consistent signal: selecting the robot mask improves same-frame proprioceptive–visual alignment, whereas selecting a human distractor weakens the positive pair and makes the frame harder to distinguish from negatives. In this way, instance-level self labels emerge from frame-level proprioceptive– visual correspondence. 

For all self-other distinction experiments, we use _τa_ = 0.003, _τl_ = 0.01, batch size _B_ = 32, learning rate 0.001, 100 training epochs and weight decay 0.01. We use AdamW optimization (Loshchilov & Hutter, 2017) with gradient clipping for the self-other distinction module. Ablation experiments for self-other distinction are reported in Supplementary Table 1. 

#### **4.5 Kinematics-free implicit self-modeling** 

After self-other distinction, the selected robot masks serve as pseudo-GT supervision for learning the robot’s self-model. This second stage uses the full 36-dimensional state _St_ because self-modeling requires both local articulation and root pose. The target supervision is a binary or near-binary foreground mask _Mt ∈{_ 0, 1 _}_<sup>_H×W_</sup> , obtained from the self-mask selected by the self-other distinction module. The self-modeling stage therefore learns from the visual instance that the robot has identified as its own, preserving the causal chain from self-other distinction to self-modeling. 

**Pose normalization.** To reduce global drift in real robot data, the first frame of each sequence is used as a local reference. Let **_R_** 0 and **_p_** 0 denote the root rotation and translation in the first frame. We transform later translations and rotations into this local coordinate system: 


The relative rotation is converted back to a quaternion **_r_** ˜ _t_ . As a sequence-level preprocessing step, and because **_r_** and _−_ **_r_** represent the same rotation, we enforce temporal continuity by flipping the quaternion sign whenever its dot product with the previous quaternion in the same sequence is negative. The reconstruction state is then 


**Ray sampling and pose-conditioned coordinates.** Camera rays are generated from calibrated intrinsics. For pixel ( _u_ , _v_ ) with intrinsics ( _fx_ , _fy_ , _cx_ , _cy_ ), the camera-frame direction is 


Points are sampled along each ray between near and far planes, with near = _d_ cam _− n f_ and far = _d_ cam + _n f_ . For depth sample _zk_ , the point is **_x_** _k_ = **_o_** + _zk_ **_d_** _uv_ . 

The sampled point is then transformed into a robot-centred canonical space using the relative root pose: 


where **_c_** = [0, _−_ 0.457, 0.793]<sup>_⊤_</sup> is the robot-centred offset used to align the canonical sampling volume. The vertical component corresponds to the root-joint height of the standing robot, and the lateral component accounts for the robot standing 0.457 m to the left of the scene centre in our camera view. This transformation lets the network model articulated body shape while factoring out global motion. 

**Visibility-based implicit self-model.** The reconstruction network learns an implicit function 


where _σk ≥_ 0 is volume density and _vk ∈_ [0, 1] is view-dependent visibility. The input dimension is 42, consisting of a 3D point, the 36D robot state, and a 3D viewing direction. 

14 

Spatial coordinates, pose groups, and viewing direction are encoded with sinusoidal positional encoding. The part-aware pose encoder partitions the 29 joint angles into torso, left leg, right leg, left arm, and right arm groups, processes each group with a part-specific MLP, and fuses the resulting features into a global posture representation. This part-aware pose encoding provides a structured inductive bias for the high-dimensional humanoid state without imposing an explicit kinematic model. Bilateral limbs use shared structure in the encoder. The density branch predicts body geometry, whereas the visibility branch models view-dependent mask contribution. 

**Bounded volumetric mask rendering and objective.** For consecutive samples along a ray, let 


This bounded volumetric mask renderer follows NeRF-style alpha compositing through the transmittance term _Tk_ , but adapts the terminal interval to binary silhouette supervision. Standard RGB NeRF (Mildenhall et al., 2020) implementations often assign an effectively infinite distance to the final sample so that the ray can terminate beyond the sampled points. In our setting, the reconstruction volume is finite and calibrated around the robot body. We therefore set the last interval to far _− zN_ rather than an unbounded value. This bounded terminal interval restricts the model to explaining occupancy within the near–far robot volume and avoids encouraging spurious opacity at the far end of background rays. Additional rendering comparisons are provided in Supplementary Figs. 1 and 2. 

Density is converted to alpha by 


and transmittance is 


The predicted foreground value for ray **_ρ_** is 


We can also render the foreground mask without the visibility term, using ∑ _k Tkαk_ , which still provides a strong reconstruction signal from density alone. The main reconstruction loss is 


Here, _R_ denotes the set of sampled camera rays used for mask supervision, and **_ρ_** denotes an individual ray. The self-model is trained mainly with this MSE objective, with a weak ray-wise density smoothness term used in real-world training to stabilize the learned field. Models are optimized with Adam (Kingma & Ba, 2014) and ReduceLROnPlateau scheduling. For the comparison with FFKSM (Hu et al., 2025b), we adapt the original formulation from its 4-DoF robotic-arm setting to our 29-DoF humanoid setting by enlarging the pose input dimension and scaling the network depth and feature width accordingly, and train the adapted model on the same selected self-masks, camera calibration, data split and evaluation metrics as our own model. 

**Pseudo-GT accuracy ablation.** To evaluate how errors in first-stage self-other distinction affect second-stage self-modeling, we construct controlled pseudo-GT mask sets with different fractions of correct self-masks. The 100% condition uses oracle robot masks as supervision. For lower-accuracy conditions, we randomly replace a prescribed fraction of robot masks with the corresponding distractor masks, yielding pseudo-GT accuracies of 90%, 80%, 70%, 60% and 50%. The Ours condition uses the masks selected by the trained self-other distinction module. All conditions use the same self-model architecture, training protocol, camera calibration and evaluation split. Reconstruction quality is evaluated on 6,013 test samples using IoU at an occupancy threshold of 0.5, MSE and MAE against GT masks, and Chamfer Distance against GT 3D point clouds. 

15 

#### **4.6 Downstream spatial reasoning with the learned self-model** 

The learned implicit self-model provides a differentiable mapping from proprioceptive state to body occupancy. We use this property to evaluate whether the representation can support human-related downstream tasks, rather than only reconstructing the robot’s appearance. We consider three applications in human-robot collaborative settings: target reaching toward objects placed by a human, collision-aware motion planning through a constrained aperture, and human-to-robot motion retargeting. 

**Left-hand self-model for target reaching.** For object-reaching tasks, the relevant occupied volume is the robot hand rather than the entire body. We therefore train a dedicated left-hand self-model that predicts the occupancy density of the left hand conditioned on the full-body proprioceptive state. Because the hand occupies only a small part of the full humanoid volume, we represent its 3D position by the density-weighted centre of the learned hand occupancy. Given query points _{_ **_x_** _i}i_<sup>_N_</sup> =1<sup>and predicted hand density</sup><sup>_σ_hand(</sup><sup>**_x_**</sup><sup>_i_,</sup><sup>_S_), the hand</sup> position is 


Given a target point **_p_**<sup>_∗_</sup> _∈_ **R**<sup>3</sup> on the tabletop, the robot optimizes the seven left-arm joints while keeping the remaining state components fixed, yielding a full-body state _S_ ( **_q_** arm) that minimizes 


Gradients are back-propagated through the learned hand self-model to update the joint angles. This procedure is a neural inverse-kinematics objective defined directly on the learned self-model, without using a predefined forward-kinematics chain or URDF-based controller. 

**Collision-aware joint-space planning.** Target reaching becomes more difficult when the hand must move through a constrained environment. For the aperture-reaching task, the workspace contains a 400 mm _×_ 600 mm planar board with a circular aperture of radius 100 mm, placed between the robot and the target so that a direct gradient-descent trajectory toward the target would collide with the board. We use learned occupancy models inside a target-biased rapidly exploring random tree (RRT) (LaValle, 1998). Each node in the tree is a joint vector. At each planning step, the planner samples a candidate configuration, extends the nearest valid node toward that sample, and queries both the full-body self-model and the left-hand self-model at the candidate state. The full-body model checks whether any occupied body region intersects the planar board outside the circular aperture, while the left-hand model provides an additional hand-level collision query. The left-hand model is also used to test whether the hand has reached the target region. Candidate states that violate the collision checks are rejected while accepted states are added to the tree until the left hand reaches the target. This combines global search in joint space with collision and goal information supplied by the learned self-models. 

**Human-to-robot motion retargeting.** For human-to-robot motion retargeting, we adapt the self-model from single-hand reaching to whole-body retargeting. The full pipeline is illustrated in Supplementary Fig. 3. A monocular video of a human demonstration is first processed with a human pose estimator (Yin et al., 2025; Araujo et al., 2025) to obtain a sparse sequence of 3D body keypoints. We use 11 keypoints: the pelvis, left and right shoulders, elbows, hands, knees, and feet (ankle joints). These keypoints are transformed from the camera coordinate frame into the robot coordinate frame. Because human and robot limb lengths differ, we do not directly use the raw human keypoint positions as targets. Instead, we preserve the direction of each human body segment and rescale the corresponding segment to the humanoid robot’s body dimensions, producing robot-compatible spatial targets for each key body part. 

The retargeted spatial targets do not directly specify robot joint angles. We therefore solve a neural inverse-kinematics problem using learned body-part occupancy models. Given a candidate 29-DoF joint vector **_q_** , the model predicts a density field for each body part. We summarize each predicted body part by its density-weighted centre, using the same form as 

16 

Equation 17. For a set of retargeted target keypoints _{_ **_c_**<sup>_∗_</sup> _k_<sup>_}_</sup> _k_<sup>_K_</sup> =1<sup>, the optimized keyframe pose</sup> minimizes 


Gradients are back-propagated through the learned occupancy models to update the 29 robot joint angles, which are clamped to feasible ranges after each step. We optimize a sparse set of keyframes rather than every video frame, initializing each keyframe optimization from the same nominal robot pose. 

## **References** 

- Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- Lorraine E. Bahrick and John S. Watson. Detection of intermodal proprioceptive–visual contingency as a potential basis of self-perception in infancy. _Developmental Psychology_ , 21 (6):963–973, 1985. doi: 10.1037/0012-1649.21.6.963. 

- Josh Bongard, Victor Zykov, and Hod Lipson. Resilient machines through continuous self-modeling. _Science_ , 314(5802):1118–1121, 2006. doi: 10.1126/science.1133687. URL https://www.science.org/doi/abs/10.1126/science.1133687. 

- Celia A. Brownell, Stephanie Zerwas, and Geetha B. Ramani. “So big”: The development of body self-awareness in toddlers. _Child Development_ , 78(5):1426–1440, 2007. doi: 10.1111/j. 1467-8624.2007.01075.x. 

- Nicolas Carion, Laura Gustafson, Yuan-Ting Hu, Shoubhik Debnath, Ronghang Hu, Didac Suris, Chaitanya Ryali, Kalyan Vasudev Alwala, Haitham Khedr, Andrew Huang, et al. Sam 3: Segment anything with concepts. _arXiv preprint arXiv:2511.16719_ , 2025. 

- Boyuan Chen, Robert Kwiatkowski, Carl Vondrick, and Hod Lipson. Fully body visual self-modeling of robot morphologies. _Science Robotics_ , 7(68):eabn1944, 2022. 

- Erwin Coumans and Yunfei Bai. Pybullet, a python module for physics simulation for games, robotics and machine learning, 2016. 

- Wenliang Dai, Junnan Li, Dongxu Li, Anthony Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale N Fung, and Steven Hoi. Instructblip: Towards general-purpose visionlanguage models with instruction tuning. _Advances in neural information processing systems_ , 36:49250–49267, 2023. 

- Jean Decety and Jessica A. Sommerville. Shared representations between self and other: a social cognitive neuroscience view. _Trends in Cognitive Sciences_ , 7(12):527–533, 2003. doi: 10.1016/j.tics.2003.10.004. 

- Shaun Gallagher. Philosophical conceptions of the self: implications for cognitive science. _Trends in cognitive sciences_ , 4(1):14–21, 2000. 

- Kyle Gao, Yina Gao, Hongjie He, Dening Lu, Linlin Xu, and Jonathan Li. Nerf: Neural radiance field in 3d vision, a comprehensive review. _arXiv preprint arXiv:2210.00379_ , 2022. 

- Kevin Gold and Brian Scassellati. Using probabilistic reasoning over time to self-recognize. _Robotics and autonomous systems_ , 57(4):384–392, 2009. 

- Zhaoyuan Gu, Junheng Li, Wenlan Shen, Wenhao Yu, Zhaoming Xie, Stephen McCrory, Xianyi Cheng, Abdulaziz Shamsah, Robert Griffin, C. Karen Liu, Abderrahmane Kheddar, Xue Bin Peng, Yuke Zhu, Guanya Shi, Quan Nguyen, Gordon Cheng, Huijun Gao, and Ye Zhao. Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning. _IEEE/ASME Transactions on Mechatronics_ , 31(2):2300–2330, 2026. doi: 10.1109/TMECH.2025.3579247. 

17 

- Yuhang Hu, Boyuan Chen, and Hod Lipson. Egocentric visual self-modeling for autonomous robot dynamics prediction and adaptation. _npj Robotics_ , 3, 06 2025a. doi: 10.1038/ s44182-025-00031-6. 

- Yuhang Hu, Jiong Lin, and Hod Lipson. Teaching robots to build simulations of themselves. _Nature Machine Intelligence_ , 7(3):484–494, 2025b. 

- Maximilian Ilse, Jakub Tomczak, and Max Welling. Attention-based deep multiple instance learning. In _International conference on machine learning_ , pp. 2127–2136. PMLR, 2018. 

- Marc Jeannerod. The mechanism of self-recognition in humans. _Behavioural Brain Research_ , 142(1):1–15, 2003. ISSN 0166-4328. doi: https://doi.org/10.1016/S0166-4328(02)00384-4. URL https://www.sciencedirect.com/science/article/pii/S0166432802003844. 

- Andreas Kalckert and H. Henrik Ehrsson. Moving a rubber hand that feels like your own: A dissociation of ownership and agency. _Frontiers in Human Neuroscience_ , 6:40, 2012. doi: 10.3389/fnhum.2012.00040. 

- Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. _arXiv preprint arXiv:1412.6980_ , 2014. 

- Robert Kwiatkowski and Hod Lipson. Task-agnostic self-modeling machines. _Science Robotics_ , 4(26):eaau9354, 2019. doi: 10.1126/scirobotics.aau9354. URL https://www. science.org/doi/abs/10.1126/scirobotics.aau9354. 

- Pablo Lanillos, Jordi Pages, and Gordon Cheng. Robot self/other distinction: active inference meets neural networks learning in a mirror. In _ECAI 2020: 24th European Conference on Artificial Intelligence, 29 August–8 September 2020, Santiago de Compostela, Spain–Including 10th Conference on Prestigious Applications of Artificial Intelligence (PAIS 2020)_ , pp. 2410–2416. SAGE Publications 1 Oliver’s Yard, 55 City Road, London, EC1Y 1SP, 2020. 

- Steven M. LaValle. Rapidly-exploring random trees : a new tool for path planning. _The annual research report_ , 1998. URL https://api.semanticscholar.org/CorpusID:14744621. 

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023. 

- Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_ , 2017. 

- Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. In _Computer Vision – ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part I_ , pp. 405–421, Berlin, Heidelberg, 2020. Springer-Verlag. ISBN 978-3-030-58451-1. doi: 10.1007/978-3-030-58452-8 _\_ ~~2~~ 4. URL https://doi.org/10.1007/978-3-030-58452-8 ~~2~~ 4. 

- Aaron van den Oord, Yazhe Li, and Oriol Vinyals. Representation learning with contrastive predictive coding. _arXiv preprint arXiv:1807.03748_ , 2018. 

- Philippe Rochat and Rachel Morgan. Spatial determinants in the perception of self-produced leg movements in 3- to 5-month-old infants. _Developmental Psychology_ , 31(4):626–636, 1995. doi: 10.1037/0012-1649.31.4.626. 

- Philippe Rochat and Tricia Striano. Perceived self in infancy. _Infant behavior and development_ , 23(3-4):513–530, 2000. 

18 

- Mark A. Schmuckler. Visual-proprioceptive intermodal perception in infancy. _Infant Behavior and Development_ , 19(2):221–232, 1996. ISSN 0163-6383. doi: https://doi.org/10. 1016/S0163-6383(96)90021-1. URL https://www.sciencedirect.com/science/article/ pii/S0163638396900211. 

- Lennart Schulze and Hod Lipson. High-degrees-of-freedom dynamic neural fields for robot self-modeling and motion planning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 3064–3070, 2024. doi: 10.1109/ICRA57147.2024.10611047. 

- Christina Soyoung Song and Youn-Kyung Kim. The role of the human-robot interaction in consumers’ acceptance of humanoid retail service robots. _Journal of Business Research_ , 146: 489–503, 2022. ISSN 0148-2963. doi: https://doi.org/10.1016/j.jbusres.2022.03.087. URL https://www.sciencedirect.com/science/article/pii/S014829632200323X. 

- Nikolaus Steinbeis. The role of self–other distinction in understanding others’ mental and emotional states: neurocognitive mechanisms in children and adults. _Philosophical Transactions of the Royal Society B: Biological Sciences_ , 371(1686), 2016. 

- Alexander Stoytchev. Self-detection in robots: a method based on detecting temporal contingencies. _Robotica_ , 29(1):1–21, 2011. 

- Yuchuang Tong, Haotian Liu, and Zhengtao Zhang. Advancements in humanoid robots: A comprehensive review and future prospects. _IEEE/CAA Journal of Automatica Sinica_ , 11(2): 301–328, 2024. 

- Laurens Van der Maaten and Geoffrey Hinton. Visualizing data using t-sne. _Journal of machine learning research_ , 9(11), 2008. 

- Wanqi Yin, Zhongang Cai, Ruisi Wang, Ailing Zeng, Chen Wei, Qingping Sun, Haiyi Mei, Yanjun Wang, Hui En Pang, Mingyuan Zhang, et al. Smplest-x: Ultimate scaling for expressive human pose and shape estimation. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 

19 

## **Supplementary Information** 


Supplementary Fig. 1: **Qualitative comparison of 2D reconstruction variants.** Rows show, from top to bottom, the GT mask, a scaled FFKSM baseline, our full method, our method without the visibility branch (Ours (density)), and our architecture combined with the FFKSM renderer (Ours (FFKSM renderer)). The comparison shows that the full model most closely matches the target silhouette, while the density-only variant remains competitive but loses view-dependent refinement. The FFKSM baseline and the variant that keeps our architecture but replaces the renderer with the FFKSM renderer indicate that both the part-aware reconstruction network and the bounded visibility-aware rendering formulation contribute to the final reconstruction quality. 

20 


FFKSM Ours (FFKSM renderer) Ours (density) Ours 

Supplementary Fig. 2: **Quantitative comparison of 2D reconstruction variants.** Quantitative evaluation of the same reconstruction variants shown in Supplementary Fig. 1: the scaled FFKSM baseline, our full method, our method without the visibility branch (Ours (density)), and our architecture combined with the FFKSM renderer (Ours (FFKSM renderer)). Reconstruction fidelity is measured by IoU, MSE, MAE and Chamfer Distance (CD), with higher IoU and lower MSE, MAE and CD indicating better performance. Bars show mean values, and error bars denote standard deviation across held-out evaluation samples. The full model achieves the best overall reconstruction accuracy, supporting the contribution of both the part-aware reconstruction architecture and the bounded visibility-aware rendering formulation. 

21 


Supplementary Fig. 3: **Human-to-robot motion retargeting pipeline.** A monocular human demonstration is first processed by a human pose estimator to obtain a sparse sequence of 3D body keypoints. The 11 keypoints used for retargeting include the pelvis, left and right shoulders, elbows, hands, knees and feet; these points are transformed into the robot coordinate frame and mapped to robot-compatible spatial targets by preserving human segment directions while rescaling segment lengths to the humanoid robot body. The retargeted targets are then converted into robot joint configurations through neural inverse kinematics on the learned self-model. Given a candidate 29-DoF joint vector, the partaware self-model predicts density fields for target body parts, whose density-weighted centres serve as differentiable robot keypoints. Gradients are back-propagated through the learned occupancy models to minimize the distance between predicted robot keypoints and retargeted targets, producing a whole-body robot motion sequence without paired human-robot demonstrations or a manually specified human-robot joint correspondence. In the diagram, **_p_**<sup>source</sup> denotes human keypoints, **_p_**<sup>target</sup> denotes robot-scaled target keypoints, _θ_ denotes the robot joint vector, _σk_ is the predicted density for body part _k_ , **_c_** ˆ _k_ is the densityweighted robot keypoint predicted by the self-model, and **_c_**<sup>_∗_</sup> _k_<sup>is the corresponding retargeted</sup> target. 

22 

Supplementary Table 1: **Comprehensive ablation study for self-other distinction.** Validation accuracy is reported for four design choices in the self-other distinction module. Each block varies one factor while keeping the remaining settings fixed, testing the effect of representation dimension, scale normalization, attention temperature, and negative sampling strategy. Higher accuracy indicates better performance. 

|**Dim**|**Scale norm**<br>**Attn temp**|**Sampling**|**Val acc.**|
|---|---|---|---|
|_Featu_<br>|_re dimension ablation_<br><br>|||
|8|ON<br>0.003|All|0.7538|
|16|ON<br>0.003|All|**0.9969**|
|32|ON<br>0.003|All|0.9340|
|64|ON<br>0.003|All|0.9860|
|_Scale_|_normalization ablation_|||
|16|ON<br>0.003|All|**0.9969**|
|16|OFF<br>0.003|All|0.8974|
|_Atten_|_tion temperature ablation_|||
|16|ON<br>0.003|All|**0.9969**|
|16|ON<br>0.03|All|0.8582|
|16|ON<br>0.3|All|0.6884|
|_Nega_|_tive sampling ablation_<br>|||
|16|ON<br>0.003|All|**0.9969**|
|16|ON<br>0.003|Single|0.8765|


23 

