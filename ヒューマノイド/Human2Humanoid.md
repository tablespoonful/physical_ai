---
title: "Human2Humanoid: Physics-Aware Cross-Morphology Motion Retargeting for Humanoid Robots"
date: "2026-06-02"
authors: "Tianchen Huang; Feiyang Yuan; Junchi Gu; Shurui Fang; Xiaohu Zhang; Yu Wang"
url: https://arxiv.org/abs/2606.03476
pdf: https://arxiv.org/pdf/2606.03476
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.03476)** / [論文ページ](https://arxiv.org/abs/2606.03476)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Human2Humanoid: Physics-Aware Cross-Morphology Motion Retargeting for Humanoid Robots** 

Tianchen Huang, Feiyang Yuan, Junchi Gu, Shurui Fang, Xiaohu Zhang, Yu Wang, Wei Gao and Shiwu Zhang 

**_Abstract_ —Retargeting human motion to humanoid robots is critical for teleoperation, imitation learning and human-robot interaction. However, it remains challenging because of substantial morphological discrepancies between humans and robots, including differences in skeletal topology, limb proportions and degrees of freedom, as well as the scarcity of paired motion data. This paper presents Human2Humanoid, an unsupervised motion retargeting framework that transfers human motions to humanoid robot behaviors with high fidelity. To bridge the domain gap under unpaired data, we adopt a CycleGAN-based architecture equipped with a skeleton-aware graph convolutional network to capture topology-dependent motion features. To address crossdomain scale mismatches, we introduce a morphology-invariant end-effector consistency loss that aligns normalized end-effector trajectories to preserve motion semantics across embodiments. To improve physical plausibility and reduce contact artifacts, we impose explicit physics-aware feasibility constraints to encourage reproduction of the contact patterns in the source motion. Experimental results show that the proposed method successfully retargets human motion to the Unitree G1 humanoid robot without paired data, and outperforms existing methods in both downstream controllability and physical feasibility.** 

## I. INTRODUCTION 

The rapid development of humanoid robots has opened new frontiers in teleoperation, imitation learning and humanrobot interaction [1]–[3]. A fundamental requirement of these applications is the ability to transfer rich human motion priors into executable robot behaviors, which is also known as motion retargeting. In modern learning-based pipelines, motion retargeting has served as the critical bridge between human demonstration and robot control. However, it remains highly challenging because of substantial embodiment gaps arising from two main aspects: morphological discrepancies in skeletal topology, limb proportions and degrees of freedom (DoFs) [4], [5], and the scarcity of high-quality paired data, namely synchronized human-robot motion sequences [6]. 

Traditional retargeting methods rely on inverse kinematics and constrained optimization to enforce robot-specific feasibility constraints, such as joint limits, body balance, collision avoidance and contact conditions [7], [8]. Although effective 

This work was supported in part by the National Science and Technology Major Project (Grant No. 2026ZD1609100), in part by the National Natural Science Foundation of China under Grants U22B2040, in part by the Key Science & Technology Project of Anhui Province (202523j08050001), in part by the Major Project of Anhui Province’s Science and Technology Innovation Breakthrough Plan (202423h08050003), and in part by the Fundamental Research Funds for the Central Universities with grant No. YD2090002019. (Corresponding authors: Wei Gao; Yu Wang.) 

The authors are with the Institute of Humanoid Robots, Department of Precision Machinery and Precision Instrumentation, University of Science and Technology of China, Hefei, Anhui 230026, China. weigao@ustc.edu.cn; wangyuustc@ustc.edu.cn 

and interpretable, these methods are sensitive to initial conditions, objective weights and embodiment mismatches, and may produce semantically distorted or contact-inconsistent robot motions [9], [10]. Data-driven methods offer an alternative by learning human-robot motion mappings, but supervised approaches depend heavily on paired human-robot motion data, which is difficult to acquire and scale across different embodiments [11], [12]. On the other hand, unpaired retargeting methods based on adversarial or cycle-consistency objectives have been explored in computer graphics and animation [13]– [15]. Nevertheless, direct application of these methods to humanoid robots is unrealistic because they mainly focus on visual plausibility but not executable joint-space trajectories, stable ground contacts or robot-specific kinematic feasibility. 

Therefore, motion retargeting through learning-based methods for humanoid robots must address two coupled challenges. The first is semantic preservation under severe morphology mismatches. When body sizes, limb proportions and joint structures differ substantially across embodiments, pose-level geometric alignment alone is insufficient, because the same action semantics may correspond to very different absolute coordinates and reachable configurations. The second is physical plausibility under unpaired learning. Distribution-level alignment alone cannot prevent contact-related artifacts such as foot skating and ground penetration, which may compromise executability on real robots. Furthermore, these two challenges are tightly coupled: methods that focus only on feasibility may distort the semantics of source motion, while methods that focus only on appearance or distribution matching may produce physically unreliable robot behaviors. 

To address these challenges, this paper proposes **Human2Humanoid** , an unpaired motion retargeting framework for humanoid robots. The central idea is to cast retargeting as unpaired cross-domain transfer anchored by morphologyinvariant semantic structure and explicit physical priors. Specifically, it builds upon a CycleGAN-style architecture [13] and incorporates a Skeleton-Aware Graph Convolutional Network to model the native topological structure of skeletal motions. To preserve action semantics across embodiments with large scale mismatches, a _Morphology-Invariant End-Effector Consistency Loss_ is introduced to align end-effector trajectories that are normalized relative to the T-pose of each embodiment rather than directly matching absolute coordinates. To improve physical plausibility during generation, _PhysicsAware Feasibility Constraints_ are further imposed to reproduce the contact patterns of source motion while suppressing foot skating and ground penetration. Consequently, the proposed framework learns cross-embodiment motion transfer without 

relying on paired human-robot data, and becomes more compatible with downstream control tasks. 

The proposed method is validated on the Unitree G1 platform, with the experimental results showing that Human2Humanoid can outperform representative baselines in both semantic fidelity and physical realism. In addition, the ablation study confirms that the physics-aware training objectives make essential contributions to the overall performance. The main contributions of this work are summarized as: 

- Proposing _Human2Humanoid_ , an unpaired motion retargeting framework for heterogeneous humanoid robots that reduces dependence on robot-specific paired datasets. 

- Introducing a _Morphology-Invariant End-Effector Consistency Loss_ that preserves motion semantics under large cross-embodiment scale mismatches by aligning endeffector trajectories that are normalized relative to each embodiment’s T-pose. 

- Incorporating _Physics-Aware Feasibility Constraints_ into the generative training process, improving physical plausibility by mitigating contact-related artifacts such as foot skating, body floating and ground penetration. 

## II. RELATED WORK 

## _A. Motion Retargeting in Robotics_ 

Motion retargeting for humanoid robots has traditionally been addressed through inverse kinematics and constrained optimization. Ayusawa and Yoshida jointly optimize morphology parameters and robot motion to reduce geometric mismatches while reproducing source-motion characteristics [16]. Penco _et al._ formulate real-time whole-body retargeting as a constrained inverse kinematics and quadratic programming problem for humanoid teleoperation [17]. More recently, Araujo _et al._ show that retargeting artifacts such as foot skating, self-collision and physical infeasibility can substantially degrade downstream humanoid motion tracking, and propose General Motion Retargeting (GMR) to combine non-uniform local scaling with constrained optimization [10]. These optimization-based methods are interpretable and can impose physical constraints directly. However, they remain sensitive to initial conditions, objective weights and per-motion tuning. Under large morphology mismatches, geometric fitting can produce poses that are reachable but semantically distorted, such as compressed strides, shifted arm trajectories or unstable stance phases. 

Learning-based methods aim to reduce this engineering burden by learning human-robot mappings from data. A central difficulty, however, is that supervised training requires paired human-robot motion data, which are expensive to collect and difficult to scale across different embodiments. S3LE reduces manual data collection through a self-supervised generation procedure, but its learning process still depends on paired human poses and robot configurations [6]. Moreover, its evaluation focuses mainly on upper-body motion of the COMAN humanoid robot, leaving stable lower-body control such as root displacement and foot-ground contacts not addressed. Recent neural retargeting methods further improve feasibility by constructing physically refined supervision. For example, NMR 

proposes a Clustered-Expert Physics Refinement pipeline that curates human motions, performs optimization-based retargeting and filtering, and uses expert-policy rollouts in simulation to generate physics-consistent human-robot motion pairs [18]. This strategy improves tracking quality, but its effectiveness still depends on morphology-specific paired supervision generated within a pre-curated robot-feasible motion subspace. Therefore, extending it to a new robot embodiment requires rebuilding the same robot-specific data-construction pipeline, with its key stages reconfigured for the target morphology and dynamics. Moreover, because the source motions are filtered to retain the ones that the robot can in principle execute and the paired targets are further repaired for tracking feasibility, the learned mapping may be biased toward dynamically trackable motions rather than preserving the full diversity and fine-grained semantics of open-ended human motions. This limitation is especially relevant for motions involving explicit environmental geometry or external contacts, such as sitting, stepping onto stairs or object manipulation. 

Generative models provide another direction for crossembodiment retargeting. G-DReaM represents heterogeneous embodiments with graph structures and uses energy-guided retargeting losses to train a graph-conditioned diffusion model when ground-truth target motions are unavailable [19]. This direction improves scalability across embodiments, but reliable humanoid robot deployment still requires semantic structure preservation, contact consistency and kinematic feasibility in target motions. 

Overall, existing methods for robots either rely on explicit optimization, which is interpretable but sensitive to tuning, or learned mappings, which often reintroduce paired supervision through data collection, curation and physics-based refinement. This motivates an unpaired retargeting framework that eliminates the need for paired supervision while preserving cross-morphology semantics and enforcing contact-related physical plausibility. 

## _B. Motion Retargeting in Animation and Computer Graphics_ 

Motion retargeting has also been extensively studied in computer graphics and animation with the goal of reusing motion assets across characters with different body shapes or skeletons. Early works formulate the problem as constrained motion editing. For example, Gleicher uses spacetime constraints to preserve key motion properties such as foot-ground contacts while adapting motions across characters [4]. Since these formulations are closely related to the optimization methods used in robotic retargeting, they share similar shortcomings. 

Learning-based retargeting in animation provides an important reference for unpaired motion transfer. Neural Kinematic Networks combine an analytic forward-kinematics layer with cycle-consistency and adversarial objectives, enabling unsupervised retargeting without paired motion sequences [14]. PMnet separates local pose transfer from global movement adaptation, reducing drift and distortion caused by aligning motions only in joint space [20]. Skeleton-Aware Networks further introduce topology-aware convolution, pooling and 

unpooling operators to encode homeomorphic skeletons into a shared latent space, enabling unpaired cross-character retargeting [5]. Pose-to-Motion extends this idea to data-scarce scenarios by using static target poses as priors and synthesizes plausible target motions [15]. These studies show that paired motion supervision is not strictly necessary when structural priors and cycle-style objectives are properly designed. 

Recent methods in computer graphics also consider geometry, contact and generative modeling more explicitly. R2ET uses separate residual modules for skeleton-semantic preservation and geometry-aware correction, reducing artifacts such as interpenetration and missing contacts [11]. ReConForM starts from contact semantics and uses a set of transferable key mesh vertices to improve contact accuracy and motion smoothness across diverse character morphologies [21]. MoReFlow formulates retargeting as unsupervised flow matching between character-specific motion embedding spaces and emphasizes that different application domains prioritize different retargeting objectives, _i.e._ style and visual plausibility for animation, and task-space alignment and executability for robotics [22]. 

Despite these advances, these retargeting methods are commonly evaluated by visual plausibility. They cannot be directly applied to humanoid robots where joint trajectories that satisfy embodiment-specific joint limits, whole-body stability, ground clearance and slip suppression are required. In addition, they often assume consistent topology, homeomorphic skeletons and transferable mesh correspondences across embodiments, which does not match the human-to-humanoid setting with different degrees of freedom and mechanical constraints. Therefore, augmentation of these unpaired retargeting methods regarding robot-specific semantics and physical constraints is necessary for human-to-humanoid motion retargeting. 

## III. METHOD 

This section presents details of Human2Humanoid. The goal is to learn an unpaired mapping _GB→A_ from the human motion domain _B_ to the humanoid robot motion domain _A_ . As shown in Fig. 1, the framework comprises two generators _GB→A_ and _GA→B_ , as well as two discriminators _DA_ and _DB_ . We assume access to two unpaired motion collections _QA_ = _{qA}_ and _QB_ = _{qB}_ from domains _A_ and _B_ , respectively. _QA_ and _QB_ have no temporal alignment or frame-wise correspondence. During training, fixed-length temporal windows are uniformly sampled from each collection to form mini-batches for adversarial and cycle learning. To address morphological discrepancies and ensure physical feasibility, we integrate Skeleton-Aware Graph Convolutional Networks (GCNs) and introduce Morphology-Invariant EndEffector Consistency Loss alongside Physics-Aware Feasibility Constraints. 

## _A. Network Architecture_ 

_1) Skeleton-Aware Generator:_ To effectively handle skeletal data with hierarchical structures, Skeleton-Aware GCNs [5] are adopted in our generators, differing from prior methods that treat poses as simple vectors. The generator consists of 

an encoder, a latent space and a decoder. Instead of flattening joint features, the encoder utilizes _SkeletonConv_ layers. This convolution operation explicitly leverages the skeletal topology defined by the adjacency matrix. For a joint _j_ , the feature aggregation involves not only itself but also its neighboring joints _N_ ( _j_ ), expressed as 


where _fin_ ( _k_ ) denotes the input feature of joint _k_ , _fout_ ( _j_ ) denotes the output feature of joint _j_ after neighborhood aggregation, _Wk_ is a learnable weight for joint _k_ , and _b_ is a bias term. The union _N_ ( _j_ ) _∪{j}_ indicates that the aggregation includes both the joint and its neighboring joints. Furthermore, topology-based pooling strategies are employed to compress high-dimensional skeletal features into a lowdimensional latent space, followed by unpooling operations to recover the target topology. This design allows the network to capture local joint correlations and adapt to different kinematic chain structures. The SkeletonConv and topology pooling/unpooling operate on the spatial skeleton graph at each time step. Temporal coherence is modeled by applying the generator in a sliding window over motion sequences, which encourages smooth frame-to-frame transitions while preserving local spatial kinematics. 

Note that a per-joint correspondence between embodiments is not required. The skeleton-aware layers operate on each domain’s native kinematic graph, while cross-domain coupling is imposed by the cycle objective and a set of shared semantic end-effectors used in the morphology-invariant constraints. 

_2) Frame-wise Pose Discriminator:_ The discriminator operates in a frame-wise manner. Given an input pose sequence represented by per-joint rotation features, latent joint features are first extracted by a joint-shared embedding module implemented with 1 _×_ 1 convolutions and LeakyReLU activations. Let the resulting pose feature tensor be _F ∈_ **R**<sup>_N×C×T ×V_</sup> , where _N_ is the mini-batch size, _T_ is the temporal window length, _V_ is the number of joints, and _C_ = 32 is the latent feature dimension. To score each frame independently while preserving the joint dimension, _F_ is reshaped to **R**<sup>(</sup><sup>_N·T_)</sup><sup>_×C×V_</sup> by folding the temporal dimension into the batch dimension. 

Based on this frame-level pose representation, the discriminator contains two complementary branches. The joint-wise pose branch, denoted as _Deach_ , predicts joint-wise realism scores using joint-specific linear heads, where each head maps the latent feature of one joint from **R**<sup>_C_</sup> to **R** . The full-body pose branch, denoted as _Dall ∈_ **R**<sup>(</sup><sup>_N·T_)</sup><sup>_×_1</sup> , flattens the fullbody latent pose feature and predicts a pose-level coherence score through a Multi-Layer Perceptron. Before combining the two branches, _Dall_ is broadcast along the joint dimension, yielding _D_<sup>�</sup> _all ∈_ **R**<sup>(</sup><sup>_N·T_)</sup><sup>_×V_</sup> . The final joint-wise discriminator output _D ∈_ **R**<sup>(</sup><sup>_N·T_)</sup><sup>_×V_</sup> is obtained by 


where _weach_ controls the contribution of the joint-wise branch. 


Fig. 1: Overview of the proposed Human2Humanoid framework. 

For the adversarial objective, the discriminator output is kept as joint-wise scores instead of being collapsed into a single scalar score. The LSGAN loss is then applied to each joint score independently, and the resulting squared errors are eventually averaged over all joints and frames within the sampled temporal window. 

## _B. Morphology-Invariant End-Effector Consistency Loss_ 

Humans and humanoid robots often exhibit significant discrepancies in limb lengths and proportions. For instance, human arms are much longer than those of compact robots like Unitree G1. Directly constraining absolute positions in Cartesian space can lead to semantic collapse, _e.g._ , hands failing to reach expected targets. Hence, a Morphology-Invariant EndEffector Consistency Loss is proposed to address this problem. 

Instead of aligning absolute coordinates, end-effector trajectories are aligned in a morphology-invariant space defined relative to the rest pose (T-pose). Specifically, given a source human motion _qB_ and the generated robot motion _q_ ˆ _A_ = _GB→A_ ( _qB_ ), end-effector positions can be computed by forward kinematics and the displacements from the corresponding T-poses can be compared. Let _E_ denote the set of shared semantic end-effectors (left/right hands and feet) defined in both domains, and let FK _k_ ( _q, t_ ) return the position of endeffector _k_ at frame _t_ . The corresponding displacements are normalized by the embodiment-specific constant body scale 

_S_ computed from the rest pose to avoid variation across sequences within the same embodiment: 


where **E** [ _·_ ] denotes expectation over the sampled temporal window, and _qB_<sup>_Tpose_</sup> and _qA_<sup>_Tpose_</sup> denote the T-pose configurations in the human and robot domains, respectively. 

## _C. Physics-Aware Feasibility Constraints_ 

Unsupervised retargeting often suffers from physically infeasible artifacts such as foot skating, base floating and violation of mechanical limits. To enhance deployability on real robots, explicit foot contact, foot height and joint limit constraints are introduced during training. Unless otherwise specified, the following constraints are applied to the generation of robot motion _q_ ˆ _A_ through _GB→A_ . 

_1) Foot Contact Constraint:_ A binary contact indicator _c_<sup>(</sup> _B_<sup>_m_)</sup> is inferred from the source human motion (domain _B_ ) using the foot speed. Let _m ∈F_ index the feet and let _t_ denote time, thus 


where _vB_<sup>(</sup><sup>_m_)</sup> ( _t_ ) is the source foot velocity and _τ_ is a small threshold. Using this contact gate, foot skating is suppressed in the generated robot motion in domain _A_ by penalizing the target foot velocity as 


where _ϵ_ is a small constant for numerical stability, preventing division by zero when no source foot is detected in contact. 

_2) Foot Height Constraint:_ To further improve physical plausibility during stance, foot hovering is also penalized in the generated robot motion. Let _h_<sup>(</sup> _A_<sup>_m_)(</sup><sup>_t_)and</sup><sup>_h_(</sup> _B_<sup>_m_)(</sup><sup>_t_)denote</sup> the vertical heights of robot and human foot _m_ at time _t_ , respectively. For each domain, a nominal foot contact height is pre-computed from the T-pose, denoted as _h_<sup>_ref_</sup> _A,m_<sup>and</sup><sup>_href_</sup> _B,m_<sup>.A</sup> stance-weight mask is then computed using the source domain data as 


This additional height-based filter removes spurious lowvelocity detections. Consequently, an anti-floating hinge penalty is applied on the target foot height as 


where _h_<sup>_ref_</sup> _A,m_<sup>encouragesthetargetfoottoremainclosetoits</sup> nominal grounded height during source-inferred contact. _3) Joint Limit Constraints:_ Since humanoid robots have strict mechanical ranges of motion, generated motions that exceed these limits may damage hardware or trigger emergency stops. Therefore, a joint limit loss is introduced to penalize the predicted robot joint angles _q_ ˆ<sup>_A_</sup> falling outside the range [ _qmin, qmax_ ] as 


where _j_ is the joint index. 

## _D. Full Objective Function_ 

The training of Human2Humanoid is driven by a composite objective. In addition to the retargeting-specific losses introduced in III-B and III-C, we also employ adversarial losses to match data distributions, cycle-consistency losses to ensure motion reversibility, and identity losses for regularization. 

To stabilize training and improve generation quality, the Least Squares GAN (LSGAN) objective [23] is adopted. Let _PA_ and _PB_ denote the empirical motion distributions induced by the unpaired collections _QA_ and _QB_ , respectively. Thus, samples _qA ∼ PA_ and _qB ∼ PB_ are drawn during training. For each sampled window, the discriminators output scores for each joint at each frame. We therefore implement the 

LSGAN objective element-wise and average the squared errors over all joints and frames. Let _DA,t,j_ ( _q_ ) denote the score of discriminator _DA_ for joint _j_ at frame _t_ , and analogously for _DB_ , thus 


On the other hand, the generators are trained to fool the discriminators by regressing generated samples to 1 as 


The cycle-consistency and identity losses are defined using the _L_ 1 norm as 


Therefore, the full generator objective can be written as 


where the _λ_ terms are scalar weights balancing the corresponding objectives. Eventually, the generators are optimized by minimizing _LG_ , while the discriminators are optimized by minimizing _L_<sup>_D_</sup> _LSGAN_<sup>.</sup> 

IV. EXPERIMENTS 

## _A. Experimental Setup_ 

To evaluate Human2Humanoid under substantial differences in skeletal topology, scale and degrees of freedom, we train and evaluate the model on two unpaired motion domains. The human domain is constructed from Motion-X [24], which provides large-scale 3D full-body motion annotations in the SMPL-X format and covers a broad range of motion semantics and scenarios. The robot domain is constructed from the Unitree G1 subset of PHUMA (Physically-Grounded Humanoid Locomotion Dataset) [25]. PHUMA applies physics-based filtering and optimization to reduce common artifacts such 

as foot skating and ground penetration, providing a target distribution that better reflects executable robot motions. 

_1) Preprocessing:_ Since Motion-X and PHUMA differ in original frame rates and motion representations, a unified preprocessing is applied. Sequences in both domains are resampled to 30 Hz. Each long sequence is segmented into fixedlength temporal clips of 64 frames using a sliding window with a one-frame stride, so adjacent clips overlap by 63 frames. Then, pose parameters in Motion-X are converted to joint rotation matrices, and G1 joint data in PHUMA are also converted into rotation-matrix form, augmented with rootrelated features. For the root, the absolute world translations are not used. Instead, the frame-wise differences are used to compute the root linear velocity as input, yielding translation invariance to absolute position. Meanwhile, the root global rotation matrix is kept as input and no yaw-normalization (de-heading) is applied during training. Train/test splits are performed independently within each domain. No temporal synchronization or semantic correspondence is used during training, strictly adhering to the unpaired learning assumption. 

_2) Baselines:_ Comparison against representative robot retargeting baselines for Unitree G1 is conducted, including two optimization-based pipelines and one industrial-quality reference. (i) PHC retargeting [26] is an optimization-based SMPL-to-humanoid retargeting pipeline commonly used to produce executable reference motions for humanoid robots. (ii) GMR [10] is an optimization-based retargeting method with a two-stage constrained solver and feasibility-oriented constraints. (iii) Unitree Retarget (closed-source reference) is a set of reference motions for G1 humanoid robot produced by an industrial pipeline. It is used as a high-quality reference rather than a learnable baseline. 

## _B. Evaluation Metrics_ 

The retargeted motions are evaluated in simulation on Unitree G1 under a fixed tracking policy from two aspects: (i) downstream controllability, and (ii) physical feasibility. 

_1) Downstream Controllability:_ The pretrained Unitree G1 tracking policy from the open-source humanoid-generalmotion-tracking project [2] is used to evaluate whether retargeted motions are easy to track. The tracking policy is kept fixed to help evaluation focus on the controllability of reference motion and enables a fair comparison across retargeting methods. The resulting reference trajectory from each retargeted motion clip is fed into the project’s simulation evaluation pipeline and the policy is rolled out under the same configuration. The corresponding evaluation metrics include (i) Success Rate (SR), indicating the fraction of clips whose rollouts complete without falling/termination under the project’s default termination conditions, and (ii) Tracking Error (TE), representing the average tracking error computed using the project’s default definition and logged quantities. 

_2) Physical Feasibility:_ Unless otherwise specified, physical feasibility metrics are computed on the test split using the same forward-kinematics routines and coordinate conventions as in training. The following two evaluation metrics are used: 

_a) Foot Skating (FS):_ FS measures the fraction of frames where the robot exhibits excessive horizontal slip during ground contact. Ground contact is inferred from the minimum height of the foot geometry as 


where _m ∈F_ indexes the feet, _F_ denotes the foot set, and _hcontact_ is a contact height threshold. A skating event is incurred if the foot’s horizontal velocity exceeds a tolerance threshold _τ_ tol during contact. Therefore, FS is computed as 


with _h_ contact = 0 _._ 0025 m and _τ_ tol = 0 _._ 30 m _/_ s. 

_b) Ground Penetration (GP):_ GP measures the average ground penetration depth of the robot feet and is defined as 


## _C. Evaluation Results_ 

The quantitative results are summarized in Table I. 

_1) General Discussion:_ Under the same tracking policy, Human2Humanoid achieves the best TE among the compared methods, indicating that its generated reference motions are generally easier to track. GMR obtains competitive SR, but its average TE, FS and GP remain higher than those of Human2Humanoid, suggesting that stronger SR does not fully eliminate contact-related artifacts. PHC achieves the lowest average FS, but exhibits substantially lower SR on several challenging motions, indicating that contact feasibility alone does not necessarily lead to reliably executable reference motions. The Unitree Retarget provides an industrial-quality reference, yet Human2Humanoid achieves higher average SR and lower TE under the same evaluation protocol. Besides, Human2Humanoid achieves the lowest average GP among all compared methods, indicating better ground penetration suppression. Its average FS is also lower than those of GMR and Unitree Retarget. Overall, these results show that Human2Humanoid provides a more trackable reference motion distribution than the compared baselines. 

_2) Failure cases of the optimization-based baselines:_ Although optimization-based pipelines can enforce explicit constraints, it is observed that they may still produce catastrophic artifacts on hard motions, especially near joint limits or under large morphology mismatches. Fig. 2 shows two representative examples. In PHC, when the motion approaches the robot’s joint limits, the solver may switch to a different local solution branch, causing untrackable joint “snapping”. In GMR, some sequences require non-trivial per-clip parameter tuning to avoid noticeable jitter. Such failures are difficult to fully filter out without manual inspection, while the proposed method can reduce these catastrophic cases. 

_3) Qualitative comparison:_ Qualitative comparisons are also provided in Fig. 3. Compared with the optimization-based 

TABLE I: Per-motion quantitative comparison of retargeting performance from human to Unitree G1. G, P, U and O denote GMR, PHC, Unitree Retarget and Ours (Human2Humanoid), respectively. The best and second-best results are highlighted in bold and with underscores, respectively. 

|**Motion**||**SR (**|**%)** _↑_|||**TE**|_↓_|||**FS **|**(%)** _↓_|||**GP **|**(cm)** _↓_||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||G|P|U|**O**|G|P|U|**O**|G|P|U|**O**|G|P|U|**O**|
|Walk1|**95.0**|45.0|**95.0**|90.0|0.12|0.16|0.16|**0.11**|23.7|**3.5**|37.6|17.7|0.55|0.24|1.80|**0.03**|
|Walk2|**90.0**|25.0|**90.0**|85.0|0.13|0.17|0.16|**0.11**|19.3|**4.0**|30.3|14.1|0.32|0.30|0.97|**0.02**|
|Walk3|85.0|35.0|90.0|**100.0**|0.15|0.17|0.17|**0.10**|13.9|**1.9**|9.5|11.5|0.19|0.13|0.10|**0.00**|
|Hop1|70.0|10.0|**90.0**|85.0|0.16|0.16|0.17|**0.11**|**0.0**|**0.0**|3.5|0.2|**0.00**|**0.00**|**0.00**|**0.00**|
|Jump1|**90.0**|5.0|**90.0**|85.0|0.14|0.18|0.18|**0.12**|21.8|**8.4**|33.0|16.1|0.56|0.64|1.69|**0.03**|
|Box1|**95.0**|0.0|0.0|**95.0**|0.14|0.18|0.21|**0.10**|0.2|**0.0**|**0.0**|0.1|**0.00**|**0.00**|**0.00**|0.04|
|Box2|**80.0**|0.0|0.0|70.0|**0.13**|0.17|0.19|**0.13**|0.3|**0.0**|2.5|0.7|**0.00**|**0.00**|**0.00**|0.55|
|Crouch1|**50.0**|0.0|0.0|**50.0**|0.29|0.92|0.56|**0.21**|**0.0**|0.3|**0.0**|**0.0**|**0.00**|**0.00**|**0.00**|**0.00**|
|Backward1|90.0|95.0|**100.0**|**100.0**|**0.10**|0.14|0.12|0.11|2.2|**0.0**|9.8|1.3|**0.00**|**0.00**|**0.00**|**0.00**|
|Backward2|85.0|35.0|90.0|**95.0**|0.12|0.16|0.13|**0.11**|0.4|**0.0**|3.6|**0.0**|**0.00**|**0.00**|**0.00**|**0.00**|
|Backward3|**100.0**|75.0|**100.0**|**100.0**|0.09|0.14|0.11|**0.08**|0.8|**0.0**|8.0|**0.0**|**0.00**|**0.00**|**0.00**|**0.00**|
|Turn1|**100.0**|35.0|90.0|95.0|0.13|0.15|0.17|**0.09**|0.2|**0.0**|0.2|**0.0**|**0.00**|**0.00**|**0.00**|**0.00**|
|Stand1|**100.0**|65.0|90.0|**100.0**|**0.12**|0.15|0.17|**0.12**|5.5|0.3|6.5|**0.0**|**0.00**|0.16|**0.00**|**0.00**|
|Avg.|86.9|32.7|71.2|**88.5**|0.14|0.22|0.19|**0.12**<br>ACCAD|6.8<br>_D9|**1.4**<br>**O**|11.1<br>**urs**|4.7|0.12<br>**PHC**|0.11|0.35<br>**GM**|**0.05**<br>**R**|
||(a)||||(b)|||ACCAD|_G7||||||||


Fig. 2: Representative failure cases of the optimization-based baselines on challenging motions. (a) PHC shows joint-limit induced discontinuity. (b) GMR shows jitter without permotion tuning. 

baselines (PHC/GMR), Human2Humanoid produces visually more stable contacts with fewer penetration artifacts under the large embodiment mismatches. 

Fig. 3: Qualitative comparisons between Human2Humanoid and the optimization-based baselines (PHC/GMR). 

## _D. Ablation Study_ 

To identify the contribution of each component, a controlled ablation study is conducted under the same human-to-UnitreeG1 retargeting setting as Table I. A separate set of evaluation motions is selected for the ablation analysis. All ablation models share the same architecture, training schedule and evaluation protocol as the full model. Specifically, the two considered ablation cases are: (i) w/o _LEE_ , which removes the morphology-invariant end-effector consistency loss while keeping the others unchanged, and (ii) w/o _Lcon_ , _Lhei_ , which removes the physics-aware contact and height constraints. The same metric suite (SR, TE, FS and GP) is used to show how each component affects controllability and feasibility. 

The results are summarized in Table II. Removing _LEE_ decreases the tracking success rate and increases tracking error, indicating that morphology-invariant end-effector consistency is important for preserving trackable motion semantics. Removing the contact and height constraints increases both FS and GP and slightly worsens TE, indicating that the physicsaware objectives mainly improve contact-related feasibility, especially ground-penetration reduction. 

TABLE II: Ablation study results ( _↓_ : lower is better, _↑_ : higher is better). 

|**Variant**|**SR (%)** _↑_|**TE** _↓_|**FS (%)** _↓_|**GP (cm)** _↓_|
|---|---|---|---|---|
|Full|92.8|0.099|6.89|0.264|
|w/o _LEE_|85.7|0.104|6.61|0.271|
|w/o _Lcon, Lhei_|85.7|0.106|7.02|0.326|


## V. CONCLUSION 

This paper presents **Human2Humanoid** , an unpaired motion retargeting framework for heterogeneous humanoid robots, achieving a more robust balance between semantic fidelity and physical executability. To address the pronounced human-robot discrepancies in skeletal topology and scale, as well as the scarcity of high-quality paired motion data, we build upon a CycleGAN-style unpaired learning architecture and incorporate skeleton-aware graph convolutional modeling. We further introduce a morphology-invariant end-effector consistency loss that uses the T-pose as reference and aligns crossembodiment end-effector trajectories via scale normalization, thereby preserving motion semantics more reliably under large embodiment mismatches. Meanwhile, physical conditions such as contact consistency and joint limits are explicitly integrated into the training objective, which helps suppress deploymentcritical artifacts including foot skating, base floating and ground penetration during generation. Experimental results show that Human2Humanoid enables high-quality retargeting without relying on paired data, and yields consistent improvements on both semantic and physical metrics. The ablation studies further validate the contribution of each key component. Future work will focus on generalizing to a broader range of non-humanoid robots with substantial topological differences, and on end-to-end coupling with downstream wholebody control policies to further improve real-robot robustness in complex interaction scenarios. 

## REFERENCES 

- [1] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne, “Deepmimic: example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions on Graphics_ , vol. 37, no. 4, p. 1–14, Jul. 2018. [Online]. Available: http://dx.doi.org/10.1145/3197517.3201311 

- [2] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang, “Gmt: General motion tracking for humanoid whole-body control,” _arXiv:2506.14770_ , 2025. 

- [3] M. A. Goodrich and A. C. Schultz, “Human–robot interaction: A survey,” _Foundations and Trends in Human-Computer Interaction_ , vol. 1, no. 3, pp. 203–275, 01 2008. [Online]. Available: https: //doi.org/10.1561/1100000005 

- [4] M. Gleicher, “Retargetting motion to new characters,” in _Proceedings of the 25th Annual Conference on Computer Graphics and Interactive Techniques_ , ser. SIGGRAPH ’98. New York, NY, USA: Association for Computing Machinery, 1998, p. 33–42. [Online]. Available: https://doi.org/10.1145/280814.280820 

   - [7] K. Ayusawa and E. Yoshida, “Motion retargeting for humanoid robots based on simultaneous morphing parameter identification and motion optimization,” _IEEE Transactions on Robotics_ , vol. 33, no. 6, pp. 1343– 1357, 2017. 

   - [8] K. Darvish, Y. Tirupachuri, G. Romualdi, L. Rapetti, D. Ferigo, F. J. A. Chavez, and D. Pucci, “Whole-body geometric retargeting for humanoid robots,” 2019. [Online]. Available: https://arxiv.org/abs/1909.10080 

   - [9] H. Dai, G. Izatt, and R. Tedrake, “Global inverse kinematics via mixed-integer convex optimization,” _Int. J. Rob. Res._ , vol. 38, no. 12–13, p. 1420–1441, Oct. 2019. [Online]. Available: https: //doi.org/10.1177/0278364919846512 

   - [10] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu, “Retargeting matters: General motion retargeting for humanoid motion tracking,” 2025. [Online]. Available: https://arxiv.org/abs/2510.02252 

   - [11] J. Zhang, J. Weng, D. Kang, F. Zhao, S. Huang, X. Zhe, L. Bao, Y. Shan, J. Wang, and Z. Tu, “Skinned motion retargeting with residual perception of motion semantics and geometry,” 2023. [Online]. Available: https://arxiv.org/abs/2303.08658 

   - [12] HuLei, ZhangZihao, ZhongChongyang, JiangBoyuan, and XiaShihong, “Pose-aware attention network for flexible motion retargeting by body part,” _IEEE Transactions on Visualization and Computer Graphics_ , 2024. 

   - [13] J. Y. Zhu, T. Park, P. Isola, and A. A. Efros, “Unpaired image-to-image translation using cycle-consistent adversarial networks,” _arXiv e-prints_ , 2017. 

   - [14] R. Villegas, J. Yang, D. Ceylan, and H. Lee, “Neural kinematic networks for unsupervised motion retargetting,” 2018. [Online]. Available: https://arxiv.org/abs/1804.05653 

   - [15] Q. Zhao, P. Li, W. Yifan, O. Sorkine-Hornung, and G. Wetzstein, “Pose-to-motion: Cross-domain motion retargeting with pose prior,” 2023. [Online]. Available: https://arxiv.org/abs/2310.20249 

   - [16] K. Ayusawa and E. Yoshida, “Motion retargeting for humanoid robots based on simultaneous morphing parameter identification and motion optimization,” _Robotics, IEEE Trans. on (T-RO)_ , vol. 33, no. 6, p. 15, 2017. 

   - [17] L. Penco, B. Clement, V. Moduano, E. M. Hoffman, and S. Ivaldi, “Robust real-time whole-body motion retargeting from human to humanoid,” _IEEE_ , 2018. 

   - [18] Q. Zhao, K. Yang, X. Wang, S. Zhao, Y. Lu, X. Zhang, W. Yin, Q. Shen, X.-X. Long, and X. Cao, “Make tracking easy: Neural motion retargeting for humanoid whole-body control,” 2026. [Online]. Available: https://arxiv.org/abs/2603.22201 

   - [19] Z. Cao, B. Liu, S. Li, W. Zhang, and H. Chen, “G-dream: Graphconditioned diffusion retargeting across multiple embodiments,” 2025. [Online]. Available: https://arxiv.org/abs/2505.20857 

   - [20] J. Lim, H. Chang, and J. Choi, “Pmnet: Learning of disentangled pose and movement for unsupervised motion retargeting,” _British Machine Vision Association, BMVA_ , 2019. 

   - [21] T. Cheynel, T. Rossi, B. Bellot-Gurlet, D. Rohmer, and M.-P. Cani, “Reconform : Real-time contact-aware motion retargeting for more diverse character morphologies,” 2025. [Online]. Available: https://arxiv.org/abs/2502.21207 

   - [22] W. Kim, T. Li, and S. Ha, “Moreflow: Motion retargeting learning through unsupervised flow matching,” 2025. [Online]. Available: https://arxiv.org/abs/2509.25600 

   - [23] X. Mao, Q. Li, H. Xie, R. Y. K. Lau, Z. Wang, and S. P. Smolley, “Least squares generative adversarial networks,” 2017. [Online]. Available: https://arxiv.org/abs/1611.04076 

   - [24] J. Lin, A. Zeng, S. Lu, Y. Cai, R. Zhang, H. Wang, and L. Zhang, “Motion-x: A large-scale 3d expressive whole-body human motion dataset,” 2024. [Online]. Available: https://arxiv.org/abs/2307.00818 

   - [25] K. Lee, S. Kim, M. Park, H. Kim, D. Hwang, H. Lee, and J. Choo, “Phuma: Physically-grounded humanoid locomotion dataset,” 2025. [Online]. Available: https://arxiv.org/abs/2510.26236 

   - [26] Z. Luo, J. Cao, A. W. Winkler, K. Kitani, and W. Xu, “Perpetual humanoid control for real-time simulated avatars,” in _International Conference on Computer Vision (ICCV)_ , 2023. 

- [5] K. Aberman, P. Li, D. Lischinski, O. Sorkine-Hornung, D. Cohen-Or, and B. Chen, “Skeleton-aware networks for deep motion retargeting,” _ACM Trans. Graph._ , vol. 39, no. 4, Aug. 2020. [Online]. Available: https://doi.org/10.1145/3386569.3392462 

- [6] S. Choi, M. J. Song, H. Ahn, and J. Kim, “Self-supervised motion retargeting with safety guarantee,” 2021. [Online]. Available: https://arxiv.org/abs/2103.06447 

