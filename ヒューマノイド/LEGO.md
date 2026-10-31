---
title: "LEGO: Latent-space Exploration for Geometry-aware Optimization of Humanoid Kinematic Design"
date: "2026-04-09"
authors: "Jihwan Yoon; Taemoon Jeong; Jeongeun Park; Chanwoo Kim; Jaewoon Kwon; Yonghyeon Lee"
url: https://arxiv.org/abs/2604.08636
pdf: https://arxiv.org/pdf/2604.08636
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.08636)** / [論文ページ](https://arxiv.org/abs/2604.08636)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **LEGO: Latent-space Exploration for Geometry-aware Optimization of Humanoid Kinematic Design** 

Jihwan Yoon<sup>1</sup> , Taemoon Jeong<sup>1</sup> , Jeongeun Park<sup>1</sup> , Chanwoo Kim<sup>1</sup> , Jaewoon Kwon<sup>2</sup> , Yonghyeon Lee<sup>3</sup> , Kyungjae Lee<sup>4</sup> , and Sungjoon Choi<sup>1*</sup> 

**_Abstract_ — Designing robot morphologies and kinematics has traditionally relied on human intuition, with little systematic foundation. Motion–design co-optimization offers a promising path toward automation, but two major challenges remain: (i) the vast, unstructured design space and (ii) the difficulty of constructing task-specific loss functions. We propose a new paradigm that minimizes human involvement by (i) learning the design search space from existing mechanical designs, rather than hand-crafting it, and (ii) defining the loss directly from human motion data via motion retargeting and Procrustes analysis. Using screw-theory-based joint axis representation and isometric manifold learning, we construct a compact, geometry-preserving latent space of humanoid upper body designs in which optimization is tractable. We then solve design optimization in this latent space using gradient-free optimization. Our approach establishes a principled framework for data-driven robot design and demonstrates that leveraging existing designs and human motion can effectively guide the automated discovery of novel robot design. Project page: https://jihwan-yoon-page.github.io/legopt/** 

### I. INTRODUCTION 

In robot mechanical design, determining the morphology as well as the lengths of links and axes of joints is typically the very first step. In practice, however, this process often depends heavily on human intuition and lacks a principled, systematic foundation. To move toward design automation, a promising approach is motion–design co-optimization [1], which, given a set of target motions, seeks designs that are inherently suited to executing those motions – a direction to which this paper contributes. 

The major difficulty lies in the vast, combinatorial, and unstructured nature of the design space. To make optimization tractable, designers must first restrict the search space 

This work was supported by Institute of Information & communications Technology Planning & Evaluation (IITP) grant funded by the Korea government(MSIT): (No. RS-2024-00457882, AI Research Hub Project, 50%), (No. RS-2022-II220871, Development of AI Autonomy and Knowledge Enhancement for AI Agent Collaboration, 25%), Ministry of Trade, Industry, and Energy (MOTIE), Korea, under the “Global Industrial Technology Cooperation Center program” supervised by the Korea Institute for Advancement of Technology (KIAT). (Grant No. P0028435, 25%). 

> 1Jihwan Yoon, Taemoon Jeong, Jeongeun Park, Chanwoo Kim, and Sungjoon Choi are with the Department of Artificial Intelligence, Korea University, Seoul 02841, Republic of Korea (e-mail: _{_ yoonmungchi, taemoonjeong, baro0906, chanwoo-kim, sungjoon-choi _}_ @korea.ac.kr). 

> 2Jaewoon Kwon is with Contoro Robotics, Austin, TX 78758, USA (email: jaewoon@contoro.com). 

> 3Yonghyeon Lee is with the Department of Mechanical Engineering, Massachusetts Institute of Technology, Cambridge, MA 02139, USA (email: yhl@mit.edu). 

> 4Kyungjae Lee is with the Department of Statistics, Korea University, Seoul 02841, Republic of Korea (e-mail: kyungjae ~~l~~ ee@korea.ac.kr). 

> _∗_ Corresponding author. 

– for example, by exploiting task-specific heuristics, symmetry assumptions, or low-dimensional parametric families – before meaningful optimization can be performed [1]. Moreover, each new task often introduces unique constraints and parameters, necessitating repeated and costly redefinition of the design space. 

Another challenge lies in designing the loss (or reward) function for a given task. For example, given target robot behaviors (e.g., a specific style of dancing), defining an appropriate loss or reward is nontrivial. Even when possible, it typically requires many iterations, significant human involvement, and substantial time and computational resources. 

In this paper, we propose a new paradigm that minimizes human involvement. The main idea is twofold. First, instead of being hand-crafted, the search space is learned from existing mechanical designs used as training data. Although the available designs do not constitute a massive dataset on the scale of vision or language data, they are nevertheless diverse enough to capture meaningful structural patterns and priors for guiding design optimization – a point we demonstrate in this paper. 

Second, the loss function is defined directly from human motion data, requiring data but not heuristic or costly manual design. In this regard, we address the key challenge of reconciling the discrepancy between the human skeletal kinematic structure and the robot kinematic structure being optimized by leveraging motion retargeting techniques and Procrustes analysis. 

Regarding the search space, the first question that naturally arises is how to numerically represent existing designs. Adopting screw theory [2], [3], we model each joint as a 6D vector ( **_ω_** _,_ **q** ), with **_ω_** a unit axis and **q** the joint position in a common base frame. We focus on designs with broadly similar morphologies – such as humanoids with conventional kinematic trees – so that a design with _N_ joints corresponds to a point in R<sup>6</sup><sup>_N_</sup> , with padding applied for those with fewer joints. 

The next question is how to identify a lower-dimensional subspace of existing designs that enables efficient optimization. Although each design resides in a high-dimensional space of size 6 _N_ (e.g., humanoids with over 20 joints correspond to more than 100 dimensions), the set of realizable designs is expected to lie on a structured, lower-dimensional manifold. To capture this, we use an encoder–decoder framework for manifold learning [4]–[7], mapping designs into a compact, lower-dimensional yet expressive latent space. 

To further improve structure in the latent space, we em- 

Preprint. Accepted at IEEE International Conference on Robotics and Automation (ICRA), 2026. 

ploy an isometric regularization approach, which encourages smoothness and geometry preservation [7]–[10]. Optimization is then carried out directly in this latent space, with the loss function defined from human motion data – via Procrustes analysis – and solved using Voronoi Optimistic Optimization (VOO) [11]. 

The contributions of this paper are summarized as follows: 

- A screw-theory-based representation that enables intuitive and scalable encoding of kinematic structures. 

- A learning-based framework for search space design that leverages existing mechanical designs. 

- An integrated pipeline that combines an isometric autoencoder, a human-motion–retargeting-based loss function, and VOO. 

### II. RELATED WORK: LEARNING-BASED DESIGN OPTIMIZATION 

In this section, we review learning-based design methods, focusing on two main directions: latent-model–based optimization [12]–[14], which is closely related to our framework, and reinforcement learning approaches [15], [16]. 

To address the curse of dimensionality in robot design, some recent approaches propose learning low-dimensional latent spaces that retain design validity while enabling efficient optimization [12]–[14]. Grammar-guided Latent Space Optimization (GLSO) [12] embeds modular robot structures into a continuous latent space using a graph VAE, allowing Bayesian optimization to be performed with high sample efficiency. COIL [13] constrains the latent space to represent only valid designs and uses evolutionary strategies to search it. MorphVAE [14] applies VAE-based learning to soft robot morphology using continuous evolutionary sampling between tasks and generations. 

Other methods, such as MORPH [15] and N-LIMB [16], integrate reinforcement learning with differentiable or universal control policies to co-optimize morphology and behavior. However, these approaches are computationally inefficient, lack search-space reduction, and often explore spaces so large that they lead to designs that are not practically manufacturable. 

Our approach differs in three major ways: (i) prior works rely on graph or voxel representations, whereas we adopt a screw-theory-based representation; (ii) they depend on synthetic datasets generated under human-defined constraints, whereas we leverage real, existing robot designs; and (iii) their loss functions are manually designed, while ours is directly defined from human motion data. Taken together, these distinctions advance our framework toward more automated and less human-involved robot design. Additionally, while all of these methods remain limited to simulation studies, we present a real robot design, demonstrating the real-world applicability of our approach. 

### III. PRELIMINARIES 

Our framework consists of three main components: (i) representation of the kinematic structure, (ii) data-driven 

dimensionality reduction of the search space, and (iii) optimization via retargeting in the reduced space. To support these components, this section introduces screw theory, manifold learning, and motion retargeting with Procrustes analysis, which together serve as the fundamental building blocks of our design framework. 

### _A. Screw Theory_ 

According to the Chasles–Mozzi theorem, any rigid-body displacement can be expressed as a screw motion, i.e., a rotation combined with a translation along a fixed line in space called the screw axis [2], [17], [18]. The screw axis is defined as the line passing through a point **q** and oriented by a unit vector **_ω_** . The displacement consists of a rotation about **_ω_** by an angle _θ_ , together with a translation parallel to **_ω_** of magnitude _θh_ , where _h_ denotes the screw pitch. Then, the corresponding rigid-body motion is characterized by this screw motion: 


where 


and **v** = _−_ **_ω_** _×_ **q** + _h_ **_ω_** . Thus, ( **_ω_** _, h,_ **q** ) provides a complete parametrization of a rigid-body motion via its screw axis: **_ω_** specifies the axis direction, _h_ the screw pitch, and _q_ a point on the axis. In particular, the case _h_ = 0 corresponds to pure rotation, which we use as a compact geometric representation of each joint axis throughout the paper to effectively represent robot models. 

### _B. Manifold Learning and Isometric Regularization_ 

We view an autoencoder, consisting of an encoder _f_ that maps a data point **x** to a lower-dimensional latent variable **z** and a decoder _g_ : **z** _�→_ **x** , as learning a chart of the data manifold [4], [5], i.e., the decoder _g_ parametrizes the data manifold. The pullback metric on the latent space is given by _G_ ( **z** ) = _Jg_ ( **z** )<sup>_⊤_</sup> _Jg_ ( **z** ), where _Jg_ denotes the Jacobian of _g_ . The deviation of _G_ ( **z** ) from the identity matrix **I** quantifies local geometric distortion (to see why, consider _d_ **x** = _Jg_ ( **z** ) _d_ **z** and _d_ **x**<sup>_⊤_</sup> _d_ **x** = _d_ **z**<sup>_⊤_</sup> _Jg_<sup>_⊤Jgd_</sup><sup>**z**).</sup> 

Isometry regularization encourages the latent space to preserve the geometry of the data manifold by reducing distortion [7], [8], [10], i.e., encouraging _Jg_<sup>_⊤Jg_</sup> _≈ α_ **I** (isometry up to scale), and has also been shown to yield a (intrinsically) flatter manifold [6]. Specifically, the _isometric_ regularization term is derived as 


where E _z_ is over latent space data distribution, which in practice can be efficiently computed by using Jacobian-vector and vector-Jacobian products [7]. Isometric regularization stabilizes training with limited data and yields a well-conditioned, geometry-preserving latent design space, along with a smooth manifold well suited for our kinematic optimization. 


Fig. 1: Total pipeline for humanoid kinematic structure optimization. First, a dataset of robots is converted to a unified **Screw Representation** (( _ω, q_ )). An autoencoder with an **isometric regularization loss** learns a compact 2D latent space from these representations. Next, **Voronoi Optimistic Optimization (VOO)** iteratively samples and decodes candidates from the latent space. Each candidate is evaluated by its motion retargeting performance using **Procrustes analysis** . The process converges to an optimal kinematic structure that best performs the given task. 

### _C. Motion Retargeting and Procrustes Analysis_ 

We follow a motion retargeting strategy inspired by prior works on humanoid motion transfer [19]–[21]. Because direct joint mapping is generally infeasible due to morphological differences, we define the target positions of the robot’s joints of interest (JOI) using scaled directional vectors from the human skeleton. The corresponding joint angles are then computed by solving a numerical inverse kinematics problem under joint limit constraints. To quantify the similarity between the source and retargeted motions, we employ Procrustes analysis [22], an alignment method that removes differences in translation, rotation, and scale between trajectories. This yields the Procrustes Aligned Mean Per Joint Position Error (PA-MPJPE) [23]–[27], which serves as a normalized measure of motion similarity and provides the basis for evaluating candidate kinematic structures in our optimization framework. 

### IV. METHOD 

In this section, we present our pipeline for motion-specific humanoid upper body design optimization. We begin by formulating the problem as a structure–motion co-optimization task, where the goal is to identify a kinematic structure that minimizes the discrepancy between a target human motion and its retargeted execution on the robot. We then introduce a screw-theoretic representation ( _w, q_ ) to encode upper body humanoid structures in global coordinates, followed by a data curation process that unifies 30 diverse robot models into a consistent 120-dimensional feature vector. Next, we learn a compact latent design space using an isometric-regularized autoencoder, which preserves geometric continuity while reducing dimensionality. Finally, we perform optimization in this latent space with VOO, combining motion retargeting 

and Procrustes analysis to identify feasible, symmetric upperbody designs tailored to specific motions. 

### _A. Problem Formulation_ 

We are given a source motion _M_ src, represented as a set of joint trajectories captured from a source kinematic model (e.g., a human skeleton). Our objective is to identify a new kinematic structure **x** _∈X_ , together with its retargeted motion, such that the retargeted motion closely matches _M_ src. Here, _X_ denotes an abstract design space of admissible upper-body kinematic structures, whose precise instantiation will be specified later. 

To this end, we define a retargeting operator _M_ tar = _R_ ( **x** ; _M_ src) which maps the source motion _M_ src onto a candidate kinematic structure **x** , yielding the corresponding retargeted motion _M_ tar of **x** . The operator _R_ is treated as a black-box procedure: it does not require differentiability and, in practice, is not differentiable due to the discrete nature of joint mappings and inverse kinematics. The optimization problem is thus formulated as 


where the loss function _L_ measures the discrepancy between the source motion and the retargeted motion; in our experiments, we instantiate _L_ using Procrustes analysis [28]. Given the optimal kinematic structure **x**<sup>_∗_</sup> , its corresponding retargeted motion _M_<sup>_∗_</sup> is _M_<sup>_∗_</sup> = _R_ ( **x**<sup>_∗_</sup> ; _M_ src) _._ 

This general formulation captures the essence of our goal: to search over possible kinematic structures in _X_ and evaluate them by how well the retargeted motion aligns with the original source motion. In the following sections, we describe how this problem is addressed efficiently by 

introducing a learned latent design space and performing optimization therein. 

### _B. Screw Theory-based Representation_ 

Screw theory has been widely used to unify rotation and translation within a compact, globally consistent formulation [2]. For our goal of comparing and retargeting motions in various upper body morphologies, global joint level positional fidelity is essential: the traditional form ( **_ω_** _,_ **v** ), where **v** is the moment vector, does not directly encode absolute joint positions and depends on the choice of reference point, which can hinder spatial normalization and cross-morphology comparisons. 

We therefore represent each joint by _S_ = ( **_ω_** _,_ **q** ) _,_ **_ω_** _,_ **q** _∈_ R<sup>3</sup> _,_ where **_ω_** denotes the direction (unit vector) of the global joint axis and **q** a point on that axis given in the world frame. This ( **_ω_** _,_ **q** ) parameterization preserves explicit positional information, which is advantageous for motion retargeting and structural normalization. When needed (e.g., for revolute joints), the moment vector can be recovered as **v** = _−_ **_ω_** _×_ **q** . 

A practical challenge is that robots differ in the number of joints per anatomical group, whereas the learning stage requires fixed-length inputs. To avoid injecting artificial directional bias during padding, we assign an orientationless placeholder to missing axes by setting **_ω_** = **0** . Because this study considers only revolute joints, a zero axis should be interpreted solely as a placeholder rather than as an indicator of prismatic motion. For missing positions, we preserve spatial context by imputing **q** with the mean of the existing joints in the same group; when a group is entirely absent, **q** is inherited from the nearest parent group along the kinematic hierarchy. This scheme retains positional structure through **q** while keeping the axis channel uninformative wherever data are missing. 

While the ( **_ω_** _,_ **q** ) representation is interpretable and globally consistent, the resulting design vector remains highdimensional, making direct search inefficient and brittle. In the next subsections, we therefore learn a low-dimensional _latent design space_ from these screw-theoretic features and impose isometric regularization to obtain an optimizationfriendly embedding. 

### _C. Humanoid Model Data Curation_ 

We constructed our dataset using 30 diverse humanoid and bi-arm robot models [29]–[52], including representative examples such as Talos [30], Baxter [32], Valkyrie [37], and PR2 [38], selected to cover a wide range of sizes, joint configurations, and application domains. The complete list of 30 robots used in the dataset is visualized in Figure 3. Each robot was simulated in MuJoCo [53] and posed in an A-pose (or the closest feasible configuration) to standardize joint orientations, particularly at the elbows. For robots without existing MJCF files, URDF models were converted to MJCF. Global joint positions and axes were recorded in the world coordinate frame. 

Joints were categorized into 14 anatomical groups: torso and neck (no side), plus shoulder girdle, shoulder, upper 

arm, elbow, forearm, and wrist (left/right counterparts). Virtual joints were inserted only for missing wrists, as they serve as end-effectors and are necessary for maintaining structural consistency. 

For each group, we determined the maximum joint count across all robots and padded missing entries accordingly, imputing positions with the group mean when the group was partially present and inheriting from the nearest parent when it was entirely absent. The axis channel of padded entries followed the orientationless placeholder rule defined in our screw-theoretic representation, keeping the axis information intentionally uninformative wherever data were missing. 

Positions were normalized by the shoulder-to-base distance to ensure size invariance. To reduce redundancy and enforce symmetry, only right-side joints (excluding torso and neck) were retained in the data representation. This compact representation maintains morphological completeness through mirror reconstruction during optimization. The final representation for each robot was a (20 _,_ 6) array—20 joints with ( **_ω_** _,_ **q** ) screw parameters—flattened into a 120dimensional vector for downstream learning. 

### _D. Design manifold Learning_ 

We trained an autoencoder, an encoder _fθ_ and decoder _gθ_ modeled with neural networks, with isometric regularization [7] on the 120-dimensional screw-based vectors from our curated dataset. The network comprises two hidden layers (64 and 32 units) and a latent dimension of 2 (with additional tests at 3), using Tanh activations and L2 reconstruction loss. Isometric regularization encourages the local Jacobian to approximate the identity matrix, preserving geometric continuity and reducing curvature in the latent space – especially beneficial for small datasets to improve stability and generalization. 

### _E. Optimization within the Manifold_ 


where _R_ retargets _M_ src onto the decoded structure, and the PA-MPJPE [54] loss aligns motions via a Procrustes transform and then computes mean per-joint position error. _N_ tot( _·_ ) counts the _total_ number of active joints in the mirrored full upper body; a joint _j_ is considered active if _∥_ **_ω_** _j∥_ 2 _≥ ε_ , which ignores padded placeholders. This penalty discourages gratuitous articulation and biases the search toward parsimonious, task-specific designs. 

We optimize _L_ total over **z** using VOO, a gradient-free method effective in low-dimensional continuous spaces. Because our representation stores only right-side joints (plus torso and neck), we mirror the decoded right side across the sagittal plane to obtain the full upper body before evaluation and count _N_ tot. 

V. EXPERIMENTS 

In this section, we evaluate our proposed method on three upper-body CMU Mocap sequences through two primary experiments. First, we demonstrate the effectiveness of our screw-theory representation within an AE latent space by comparing it against the traditional DH parameterization and direct optimization in the naive 120-dimensional space, as detailed in Section V-B. Second, we validate that applying isometric regularization improves designs and that a compact, two-dimensional latent space is sufficient for effective optimization, as shown in Section V-C. 

### _A. Experimental Setup_ 

**Motions.** We use three CMU Mocap sequences as _M_ src: _141_ _~~1~~ 6 Wave Hello_ (arm-dominant; negligible torso), _18_ _~~1~~ 5 Chicken Dance_ (moderate torso yaw), and _79_ _~~0~~ 2 Swimming_ (torso yaw+pitch with dynamic arms) [55]. 

**Search space & optimizer.** Candidate structures are decoded as _gθ_ ( **z** ) from ( **_ω_** _,_ **q** ) features and mirrored to obtain the full upper body; for the retargeter _R_ , we used optimization-based retargeting method [21]. We search over **z** with VOO under a fixed evaluation budget shared across methods. **Objective & hyperparameters.** We minimize PA-MPJPE [54] penalized with number of joint, _J_ = PA-MPJPE + _λ_ joint _N_ tot, counting a joint active if _∥_ **_ω_** _j∥_ 2 _≥ ε_ ; we set _λ_ joint = 3 _._ 5 and _ε_ = 0 _._ 5. For DH baselines, near-zero links are clamped to zero when _|d| ≤_ 0 _._ 01 or _|a| ≤_ 0 _._ 01. 

**Protocol.** All methods use the same evaluation budget and ten shared seeds; the decoder _gθ_ is frozen during optimization. VOO searches the latent box **z** _∈_ [ _−_ 15 _,_ 15]<sup>_d_</sup> ( _d_ =2 for main results; _d_ =3 for the ablation) with _n_ init=16 uniformly drawn starts and _T_ =30 subsequent iterations (one evaluation each), i.e., _n_ eval= _n_ init + _T_ = 46 evaluations per run. Unless otherwise noted, we also report the total objective averaged over the three motions together with its two components (PA-MPJPE and _N_ tot). 

### _B. Representation and Manifold of Robot Structure_ 

We present a quantitative comparison of our method in Table I to show the effectiveness of screw-based representation and manifold learning. We report the best-within-budget total objective (mean _±_ std over 10 seeds) _per_ motion and also for the joint objective over _set_ of all three motions (sum of the three retargeting terms plus one joint-count penalty). To evaluate our approach, we compare our method against two baselines: Denavit–Hartenberg parameters (DH) [56], [57], which uses a learned manifold of traditional DH parameters, and a direct screw-theory based representation (baseline), which performs direct optimization on the highdimensional parameter space. We implemented standard DH parameterization, augmenting it with an axis offset to account for the humanoid upper-body topology—from the torso to the neck and shoulders—and for robots whose wrists terminate as links without an explicit joint, we introduced separate 

TABLE I: Best-within-budget total objective on three motions (mean _±_ std over 10 seeds; lower is better). Objective is PA-MPJPE + _λ_ joint _N_ tot with _λ_ joint = 3 _._ 5 and _ε_ = 0 _._ 5. 

|Rep.|Wave|Motion(_↓_)<br>Dance|Swimming|Motion Set(_↓_)|
|---|---|---|---|---|
|Baseline|152_._2_±_13_._9|153_._0_±_10_._2|154_._8_±_15_._4|274_._4_±_33_._9|
|DH [56]|162_._1_±_17_._4|148_._8_±_17_._3|150_._9_±_20_._9|315_._8_±_27_._3|
|**Ours**|**97****_._5****_±_ 3****_._6**|**100****_._6****_±_ 5****_._0**|**101****_._3****_±_ 3****_._6**|**178****_._4****_±_ 10****_._8**|


Fig. 2: Mean best-so-far objective across ten shared seeds(lower is better). The error bars represent the interquartile range (thick) and min–max (thin). Left inset: oracle distribution with dashed mean _µ_ on motion _chicken dance_ . 

tool center points (TCP) for each wrist in addition to the 14 anatomical joints. 

Compared with DH [56], [57] parameter-based representation, the reductions are 39.9% (Wave), 32.4% (Dance), 32.9% (Swimming) with a single-motion average of 35.0%, and 43.5% on the all-motions objective. The superior result of the screw-theoretic representation for optimization indicates that the screw-theoretic representation with isometric regularization provides both superior accuracy and stability, especially when a single structure must accommodate heterogeneous motions. 

By comparing our full method to baseline, which uses the same screw-theory parameters but optimizes in the full 120dimensional space without manifold learning, we observe massive and consistent performance gains. This approach yields objective score reductions of 36.0%, 34.2%, and 34.6% on the individual motions, and 35.0% on the joint all-motions task. This large margin highlights the difficulty of navigating high-dimensional parameter spaces, as learning a structured manifold of valid robot designs makes the optimization problem more tractable. 

### _C. Role of Isometric Regularization and Latent Dimension_ 

Figure 2 shows the mean best-so-far objective across ten shared seeds under a fixed evaluation budget on _18_ _~~1~~ 5 chicken dance_ motion compared with the use of the isometric regularizer (2D AE [58], [59]) and latent dimension size (2D IsoAE and 3D IsoAE). 2D IsoAE (Ours) achieves the lowest mean best-so-far objective over the entire 46-evaluation budget. It drops sharply in the first 5–10 evaluations, falls below the oracle mean _µ_ early, and then continues to improve monotonically before stabilizing around steps 30–35; its dispersion is tighter than 3D IsoAE, indicating that a 


Fig. 3: Latent map of 30 robots (2D IsoAE). Colors show _k_ -means clusters ( _k_ =5) with representative thumbnails, which demonstrate that the robots are semantically grouped based on their morphological similarity (e.g., full-body humanoids, dual-arm manipulators). The bottom strip interpolates eight points from rby1 to a starred design (sufficient for _Swimming_ ); joint birth/death is visible as markers appear/disappear under the activation rule. 

two-dimensional latent design space suffices. Compared with 2D AE (no isometry), 2D IsoAE remains uniformly better across all steps, evidencing the benefit of the isometric regularizer. In contrast, baseline (screw representation with 120 dimensions) starts higher, improves slowly, and stays near or above _µ_ with wide interquartile range (IQR)/min–max bands, highlighting the difficulty of high-dimensional search without representation learning. 

Beyond the ranking, three properties stand out. _Sample efficiency_ : within the first ten evaluations, 2D IsoAE already sits well below _µ_ and separates on the normalized right axis, while 3D IsoAE and 2D AE lag and the 120D baseline hovers around _µ_ . _Robustness_ : the IQR of 2D IsoAE tightens quickly and its min–max whiskers shrink after roughly 20 evaluations; by the final budget, the IQR bands of 2D IsoAE have little overlap with those of 3D IsoAE or 2D AE, indicating lower seed sensitivity. _Dimension effect_ : under a fixed budget, increasing latent dimensionality dilutes VOO’s sampling density (Voronoi cells effectively shrink in higher _d_ ), which hurts exploitation—consistent with the slower progress of 3D IsoAE and the 120D direct baseline. 

### _D. Discussion: structure of the learned design space_ 

Beyond its quantitative performance, our model learns a meaningful latent space for robot design. This is visualized in Figure 3, which shows how the manifold groups similar structures into distinct _k_ -means clusters ( _k_ =5) with representative thumbnails. The clusters align with intuitive morphology families: a “large full-body humanoids” group (e.g., Talos [30], JAXON [39], rby1 [52], etc.) occupies the upper-left region; dual-arm mobile-manipulators and 


Fig. 4: Hardware prototypes generated by our design framework under manufacturing constraints. Each prototype is optimized for a specific task (‘Waving Hello’, ‘Chicken Dance’, ‘Swimming’), resulting in different kinematic structures. 

upper-torso platforms (Baxter [32], PR2 [38], etc.) reside in the upper-right; compact social/service humanoids (Pepper, OP3, H1, etc.) concentrate near the origin; the iCub family (iCub [34], ergoCub [33]) forms a distinct basin in the lower-left; and a lighter research-platform cluster (e.g., ARMAR-4 [46], Sciurus [44]) appears in the lower-right. These groupings suggest that the isometric latent space preserves semantically meaningful kinematic traits (torso involvement, shoulder-girdle complexity, anthropomorphic proportion), providing a navigable atlas for design search. 

Interpolating through the latent space reveals both smooth morphing of link layouts and discrete changes like joint birth/death, showing that our decoder accommodates variable joint counts. Notably, optimal solutions for certain motions (starred) can lie on cluster boundaries, suggesting they blend 


Fig. 5: Demonstration of the three motion-optimized robots from Fig. 4 successfully executing Waving Hello, Chicken Dance, and Swimming via motion retargeting. For each robot snapshot, the human figure (upper right) shows the key pose from the source human motion (BVH file) used as input, while the photo shows the retargeted execution on the robot’s unique kinematics. The red and blue lines visualize the 3D end-effector trajectories of robot and source human motion. 

features from different design families. Overall, the space enforce hard manufacturability constraints. In particular, provides: (i) coherent clustering, (ii) smooth and discrete we do not impose (i) kinematic feasibility such as kinematic changes, and (iii) actionable starting points for discrete joint types and range limits, (ii) geometric validity future optimization. including self-collision avoidance, mesh/packaging/clearance _E. Hardware_ constraints, and (iii) dynamic plausibility with actuation limits, torque/energy budgets, and contact stability. Future To empirically validate the pipeline, we fabricated a sufwork will integrate these constraints via a structure-aware ficiently good hardware prototype under manufacturing and decoder (e.g., feasibility-projected decoding), lightweight schedule constraints. All kinematic structures were denorfeasibility filters (reject/repair with collision and range malized by applying a single scale factor such that, relative checks), and simulator-backed penalties (inverse dynamics, to a 170mm lower-body reference, the base-to-neck distance torque limits), moving toward multi-objective design and equals 124mm. Assembly was performed in the same A-pose real-hardware validation. 

To empirically validate the pipeline, we fabricated a sufficiently good hardware prototype under manufacturing and schedule constraints. All kinematic structures were denormalized by applying a single scale factor such that, relative to a 170mm lower-body reference, the base-to-neck distance equals 124mm. Assembly was performed in the same A-pose world frame used throughout the dataset. Joint axes and reference positions were nominally preserved; where unavoidable to accommodate packaging and assembly, we permitted local position adjustments up to 10mm (direction-agnostic). Left–right geometry was obtained by geometric mirroring about the sagittal plane, and all subsequent retargeting and evaluation used the as-built CAD/MJCF model. On the as-built platform, we executed the retargeted joint trajectories for all three source motions— _Wave Hello_ , _Chicken Dance_ , and _Swimming_ —using the same world frame and activation rule as in simulation. Without any architectural changes to the pipeline, the as-built upper-body humanoids smoothly tracked the commanded poses (see Fig. 5). 

### VI. CONCLUSION 

We presented a motion-to-structure pipeline for upperbody humanoid design optimization. The approach hinges on three components: (i) a screw-theoretic joint representation ( **_ω_** _,_ **q** ) that encodes global joint axes and positions and enables consistent cross-morphology reasoning; (ii) a compact latent design space learned with an isometric-regularized autoencoder to provide a smooth, optimization-friendly manifold; and (iii) gradient-free search in this manifold using VOO, driven by a _total objective_ that combines PA-MPJPE after retargeting with a mild joint-count penalty. Together, these elements turn human motion priors into actionable guidance for selecting kinematic structures, achieving _∼_ 34% lower average objective than direct search and _∼_ 39% than DH+IsoAE across three motions. 

### _F. Limitations_ 

While the retargeting-based objective promotes task fidelity and parsimony, our decoder and search do not yet 

REFERENCES 

- [1] J. Kwon, S. Kim, and F. C. Park, “Physically Consistent Lie Group Mesh Models for Robot Design and Motion Co-Optimization,” _IEEE Robot. Autom. Lett._ , vol. 7, no. 4, pp. 9501–9508, 2022. 

- [2] K. M. Lynch and F. C. Park, _Modern robotics_ . Cambridge University Press, 2017. 

- [3] F. C. Park, “Computational aspects of the product-of-exponentials formula for robot kinematics,” _IEEE Trans. Autom. Control_ , vol. 39, no. 3, pp. 643–647, 1994. 

- [4] Y. Lee, “A Geometric Perspective on Autoencoders,” _arXiv preprint arXiv:2309.08247_ , 2023. 

- [5] Y. Lee, H. Kwon, and F. Park, “Neighborhood Reconstructing Autoencoders,” _Adv. Neural Inf. Process. Syst. (NeurIPS)_ , vol. 34, pp. 536–546, 2021. 

- [6] Y. Lee and F. C. Park, “On Explicit Curvature Regularization in Deep Generative Models,” in _TAG-ML Workshops_ . Proc. Int. Conf. Mach. Learn. (ICML), 2023, pp. 505–518. 

- [7] Y. Lee _et al._ , “Regularized Autoencoders for Isometric Representation Learning,” in _Proc. Int. Conf. Learn. Represent. (ICLR)_ , 2022. 

- [8] J. Lim _et al._ , “Graph Geometry-Preserving Autoencoders,” in _Proc. Int. Conf. Mach. Learn. (ICML)_ , 2024. 

- [9] Y. Lee, “Motion Manifold Primitives With Parametric Curve Models,” _IEEE Trans. Robot._ , 2024. 

- [10] H. Heo _et al._ , “Isometric Regularization for Manifolds of Functional Data,” in _Proc. Int. Conf. Learn. Represent. (ICLR)_ , 2025. 

- [11] B. Kim _et al._ , “Monte Carlo Tree Search in Continuous Spaces Using Voronoi Optimistic Optimization with Regret Bounds,” in _Proc. AAAI Conf. Artif. Intell._ , 2020, pp. 9916–9924. 

- [12] J. Hu, J. Whitman, and H. Choset, “GLSO: Grammar-guided Latent Space Optimization for Sample-efficient Robot Design Automation,” in _Proc. Conf. Robot Learn. (CoRL)_ , 2022. 

- [13] P. J. Bentley _et al._ , “COIL: Constrained Optimization in Learned Latent Space – Learning Representations for Valid Solutions,” in _Proc. Genet. Evol. Comput. Conf. (GECCO)_ , 2022. 

- [14] J. Song _et al._ , “MorphVAE: Advancing Morphological Design of Voxel-Based Soft Robots with Variational Autoencoders,” in _Proc. AAAI Conf. Artif. Intell._ , vol. 38, no. 9, 2024, pp. 10 368–10 376. 

- [15] Z. He and M. Ciocarlie, “MORPH: Design Co-optimization with Reinforcement Learning via a Differentiable Hardware Model Proxy,” in _Proc. IEEE Int. Conf. Robot. Autom. (ICRA)_ , 2024. 

- [16] C. Schaff and M. R. Walter, “N-LIMB: Neural Limb Optimization for Efficient Morphological Design,” _arXiv preprint arXiv:2207.11773_ , 2022. 

- [17] R. M. Murray, Z. Li, and S. S. Sastry, _A mathematical introduction to robotic manipulation_ . CRC press, 2017. 

- [18] F. C. Park _et al._ , “Geometric Algorithms for Robot Dynamics: A Tutorial Review,” _Appl. Mech. Rev._ , vol. 70, no. 1, p. 010803, 2018. 

- [19] S. Choi and J. Kim, “Towards a Natural Motion Generator: a Pipeline to Control a Humanoid based on Motion Data,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)_ , 2019, pp. 4373–4380. 

- [20] T. Jeong _et al._ , “CoRe: A Hybrid Approach of Contact-Aware Optimization and Learning for Humanoid Robot Motions,” in _Proc. IEEERAS Int. Conf. Humanoid Robots (Humanoids)_ , 2025, pp. 293–300. 

- [21] T. Jeong _et al._ , “Robust and Expressive Humanoid Motion Retargeting via Optimization-Based Rig Unification,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)_ , 2025, pp. 21 619–21 626. 

- [22] C. Goodall, “Procrustes methods in the statistical analysis of shape,” _J. R. Stat. Soc. B_ , vol. 53, no. 2, pp. 285–321, 1991. 

- [23] J. Li _et al._ , “HybrIK: A Hybrid Analytical-Neural Inverse Kinematics Solution for 3D Human Pose and Shape Estimation,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , 2021, pp. 3383–3393. 

- [24] J. Liu _et al._ , “Normalized Human Pose Features for Human Action Video Alignment,” in _Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)_ , 2021, pp. 11 521–11 531. 

- [25] E. G¨artner _et al._ , “Differentiable Dynamics for Articulated 3d Human Motion Reconstruction,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , 2022, pp. 13 190–13 200. 

- [26] Z. Yang _et al._ , “SynBody: Synthetic Dataset with Layered Human Models for 3D Human Perception and Modeling,” in _Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)_ , 2023, pp. 20 282–20 292. 

- [27] E. G¨artner _et al._ , “Trajectory Optimization for Physics-Based Reconstruction of 3d Human Pose from Monocular Video,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , 2022, pp. 13 106–13 115. 

- [28] J. C. Gower, “Generalized procrustes analysis,” _Psychometrika_ , vol. 40, no. 1, pp. 33–51, 1975. 

- [29] A. Adu-Bredu, “DigitRobot.jl,” https://github.com/adubredu/ DigitRobot.jl, approved copyright permission for use in this paper by Agility Robotics. 

- [30] O. Stasse, T. Flayols _et al._ , “Talos: A new humanoid research platform targeted for industrial applications,” in _Proc. IEEE-RAS Int. Conf. Humanoid Robots (Humanoids)_ , 2017, pp. 689–695. 

- [31] K. Zakka, Y. Tassa, and MuJoCo Menagerie Contributors, “MuJoCo Menagerie: A collection of high-quality simulation models for MuJoCo.” [Online]. Available: http://github.com/google-deepmind/ mujoco ~~m~~ enagerie 

- [32] S. Cremer, L. Mastromoro, and D. O. Popa, “On the performance of the baxter research robot,” in _Proc. IEEE Int. Symp. Assem. Manuf. (ISAM)_ , 2016, pp. 106–111. 

- [33] iCub Tech, “ergoCub software,” https://github.com/icub-tech-iit/ ergocub-software, 2022. 

- [34] G. Metta _et al._ , “The iCub humanoid robot: An open-systems platform for research in cognitive development,” _Neural Netw._ , vol. 23, no. 8–9, pp. 1125–1134, 2010. 

- [35] IHMC Robotics, “IHMC Alex SDK,” https://github.com/ihmcrobotics/ ihmc-alex-sdk. 

- [36] C. Mastalli, G. Saurel, and example-robot-data Contributors, “Example Robot URDFs.” [Online]. Available: https://github.com/ Gepetto/example-robot-data 

- [37] N. A. Radford _et al._ , “Valkyrie: NASA’s First Bipedal Humanoid Robot,” _J. Field Robot._ , vol. 32, no. 3, pp. 397–419, 2015. 

- [38] B. Pitzer, S. Osentoski _et al._ , “PR2 Remote Lab: An Environment for Remote Development and Experimentation,” in _Proc. IEEE Int. Conf. Robot. Autom. (ICRA)_ , 2012, pp. 3200–3205. 

- [39] K. Kojima, T. Karasawa _et al._ , “Development of Life-Sized HighPower Humanoid Robot JAXON for Real-World Use,” in _Proc. IEEERAS Int. Conf. Humanoid Robots (Humanoids)_ , 2015. 

- [40] M. Okugawa _et al._ , “Proposal of inspection and rescue tasks for tunnel disasters — Task development of Japan virtual robotics challenge,” in _Proc. IEEE Int. Symp. Saf. Secur. Rescue Robot. (SSRR)_ , 2015, pp. 1–2. 

- [41] M. Lapeyre, P. Rouanet _et al._ , “Poppy: Open Source 3D Printed Robot for Experiments in Developmental Robotics,” in _Proc. IEEE Int. Conf. Dev. Learn. Epigenet. Robot. (ICDL-Epirob)_ , 2014. 

- [42] M. A. Diftler, J. S. Mehling _et al._ , “Robonaut 2 – The First Humanoid Robot in Space,” in _Proc. IEEE Int. Conf. Robot. Autom. (ICRA)_ , 2011. 

- [43] Tokyo Opensource Robotics Kyokai Association, “Nextage Open ros packages,” https://github.com/tork-a/rtmros ~~n~~ extage, accessed: 2024. 

- [44] RT Corporation, “Sciurus17 description package,” https://github.com/ rt-net/sciurus17 ~~d~~ escription, disclaimer: Development based on this model falls outside the scope of responsibility of RT Corporation. 

- [45] P. Allgeuer _et al._ , “igus® humanoid open platform,” _KI – K¨unstliche Intell._ , vol. 30, no. 2, pp. 223–227, 2016. 

- [46] T. Asfour _et al._ , “ARMAR-4: A 63 DOF torque controlled humanoid robot,” in _Proc. IEEE-RAS Int. Conf. Humanoid Robots (Humanoids)_ , 2013, pp. 390–396. 

- [47] T. Asfour _et al._ , “ARMAR-6: A high-performance humanoid for human–robot collaboration in real-world scenarios,” _IEEE Robot. Autom. Mag._ , 2019. 

- [48] SoftBank Robotics, “Pepper robot meshes,” https://github.com/ ros-naoqi/pepper ~~m~~ eshes, converted to MJCF for compatibility with MuJoCo environment. 

- [49] K. Kaneko, F. Kanehiro _et al._ , “Humanoid robot HRP-4: Humanoid robotics platform with lightweight and slim body,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)_ , 2011. 

- [50] Westwood Robotics, “BRUCE and THEMIS simulation models,” https://github.com/Westwood-Robotics/BRUCE ~~s~~ imulation ~~m~~ odels, https://github.com/Westwood-Robotics/THEMIS-Simulation-Model, used with Permission. 

- [51] Agibot Tech, “Agibot X1 training assets,” https://github.com/ AgibotTech/agibot ~~x~~ 1 ~~t~~ rain. 

- [52] Rainbow Robotics, “RBY1 sdk,” https://github.com/RainbowRobotics/ rby1-sdk. 

- [53] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)_ , 2012, pp. 5026–5033. 

- [54] R. Dabral, A. Mundhada _et al._ , “Learning 3d human pose from structure and motion,” in _Proc. Eur. Conf. Comput. Vis. (ECCV)_ , 2018, pp. 668–683. 

- [55] CMU Graphics Lab, “Carnegie–mellon mocap database,” 2007, online: http://mocap.cs.cmu.edu/. 

- [56] J. Denavit and R. S. Hartenberg, “A Kinematic Notation for LowerPair Mechanisms Based on Matrices,” _ASME J. Appl. Mech._ , vol. 22, no. 2, pp. 215–221, 1955. 

- [57] R. S. Hartenberg and J. Denavit, _Kinematic Synthesis of Linkages_ . New York: McGraw-Hill, 1964. 

- [58] G. E. Hinton and R. R. Salakhutdinov, “Reducing the Dimensionality of Data with Neural Networks,” _Science_ , vol. 313, no. 5786, pp. 504– 507, 2006. 

- [59] I. Goodfellow, Y. Bengio, and A. Courville, _Deep Learning_ . MIT Press, 2016. 

### APPENDIX 

## **Appendix A. Robot Dataset** 

### _A. Robot List_ 

We use 30 diverse robots collected from publicly available MJCF/URDF assets. Table II lists all robots included in the dataset. Each robot is classified as either Humanoid (bipedal, with articulated legs) or Non-bipedal (no legs, mounted on a fixed pedestal, wheeled base, or similar platform). Only the upper-body kinematics are used for all robots, and the legs of bipedal robots are kept in a fixed pose during data extraction. 

TABLE II: Robots included in the dataset. 

|#|Robot|Type|#|Robot|Type|
|---|---|---|---|---|---|
|1|Alex [35]|Non-bipedal|16|JVRC [40]|Humanoid|
|2|Apollo [31]|Humanoid|17|Nextage [43]|Non-bipedal|
|3|ARMAR-4 [46]|Humanoid|18|OP3 [31]|Humanoid|
|4|ARMAR-6 [47]|Non-bipedal|19|Pepper [48]|Non-bipedal|
|5|Baxter [32]|Non-bipedal|20|Poppy [41]|Humanoid|
|6|Booster [31]|Humanoid|21|PR2 [38]|Non-bipedal|
|7|Bruce [50]|Humanoid|22|RBY1 [52]|Non-bipedal|
|8|Digit [29]|Humanoid|23|Robonaut2 [42]|Humanoid|
|9|ergoCub [33]|Humanoid|24|Romeo [36]|Humanoid|
|10|G1 [31]|Humanoid|25|Sciurus [44]|Non-bipedal|
|11|H1 [31]|Humanoid|26|TALOS [30]|Humanoid|
|12|HRP-4 [49]|Humanoid|27|Themis [50]|Humanoid|
|13|iCub [34]|Humanoid|28|TIAGo Dual [31]|Non-bipedal|
|14|IGUS OP [45]|Humanoid|29|Valkyrie [37]|Humanoid|
|15|JAXON [39]|Humanoid|30|X1 [51]|Humanoid|


### _B. Joint Classification Taxonomy_ 

Each robot’s upper-body joints are classified into 14 anatomical groups for the screw representation. The groups are listed in Table III. For the DH representation, two additional groups, left and right Tool Center Point (TCP) are appended to represent virtual end-effectors, yielding 16 groups in total. When exploiting bilateral symmetry, only eight groups are used (torso, neck, and the six right-side groups), with the left side reconstructed via mirroring. 

The maximum number of joints per group across all 30 robots is summarized in Table IV. With six screw parameters per joint, the 14-group layout yields 30 _×_ 6 = 180 features. For the DH representation, two virtual TCP groups are appended—one per arm—to anchor the end-effector frame, yielding 32 joint slots and 32 _×_ 5 = 160 features. 

Because we exploit bilateral symmetry (Appendix B), only the torso, neck, and right-side arm groups are retained for 

TABLE III: Joint classification groups (screw representation, 14 groups). 

|Group|Description|
|---|---|
|Torso|Trunk joints originating from the base link|
|Neck|Neck joints following the torso chain|
|Left / Right Shoulder Girdle|Clavicle and scapula region|
|Left / Right Shoulder|Primary shoulder joint|
|Left / Right Upper Arm|Upper arm rotation|
|Left / Right Elbow|Elbow flexion / extension|
|Left / Right Forearm|Forearm pronation / supination|
|Left / Right Wrist|Wrist articulation|


TABLE IV: Maximum joint count per anatomical group. For the DH representation, one TCP group per arm is appended (1 slot each), giving 16 groups and 32 slots in total. 

|Group|Max|Group|Max|
|---|---|---|---|
|Torso|6|R. Shoulder Girdle|1|
|Neck|4|R. Shoulder|3|
|L. Shoulder Girdle|1|R. Upper Arm|1|
|L. Shoulder|3|R. Elbow|1|
|L. Upper Arm|1|R. Forearm|1|
|L. Elbow|1|R. Wrist|3|
|L. Forearm|1|(R. TCP)|1|
|L. Wrist|3|||
|(L. TCP)|1|||
|Screw total (14 group|s)|30 slots||
|DH total (16 groups)||32 slots||


training, discarding the left-side groups whose parameters are reconstructed by mirroring. This yields 20 joint slots: torso (6) + neck (4) = 10 for the central groups, and shoulder girdle (1) + shoulder (3) + upper arm (1) + elbow (1) + forearm (1) + wrist (3) = 10 for the right arm, corresponding to 20 _×_ 6 = 120 features for screw and 21 _×_ 5 = 105 for DH (the extra slot comes from the right-side TCP group). 

## **Appendix B. Kinematic Representations** 

### _A. Screw Axis Extraction (Product of Exponentials)_ 

Each revolute joint is represented by a six-dimensional screw coordinate: a three-dimensional unit rotation axis and a three-dimensional position of the joint anchor, both expressed in the world frame. To extract these parameters, each robot is first placed in a canonical A-pose (a neutral standing posture with arms slightly abducted) using MuJoCo’s forward kinematics. The rotation axis is then read directly from the simulator’s world-frame joint axis, and the position is taken from the joint anchor computed in that configuration. No additional transformation or fitting is required, making the extraction deterministic and exact for each MJCF model. The extracted world-frame quantities are subsequently centered and scaled as described in Appendix C. 

### _B. Standard DH Parameters Extraction_ 

As an alternative representation, each joint is described by five parameters: the joint angle theta (rotation about the previous z-axis), the link offset d (translation along the previous z-axis), the link length a (distance along the 

common normal), the twist angle alpha (rotation about the common normal), and an additional axis offset tau. The first four are the classical Denavit–Hartenberg parameters; tau is an augmentation that captures the displacement of the joint anchor along its own rotation axis relative to the DH-derived frame origin. This extra parameter is necessary because standard DH conventions assume that consecutive joint axes either intersect or share a well-defined common normal, whereas real robot designs often place joints at arbitrary offsets along their axes. Without tau, the reconstructed kinematic chain would accumulate positional errors at every such offset. All five parameters are computed numerically from consecutive joint-axis pairs extracted from the MJCF model in the A-pose configuration. 

### _C. Mirroring (Symmetric to Full Body)_ 

To exploit bilateral symmetry, only the right-side joint groups (plus torso and neck) are encoded. The left side is reconstructed by mirroring across the sagittal plane (the body’s median plane, perpendicular to the y-axis). For the screw representation, the y-components of both the rotation axis and the position vector are negated, reflecting all joint geometry through the y = 0 plane. For the DH representation, the joint angle theta and the twist angle alpha are negated while the link lengths d, a, and the axis offset tau are kept unchanged. This is because reflecting a kinematic chain across the sagittal plane reverses the sense of rotation about each joint axis (hence theta flips sign) and reverses the twist between consecutive axes (hence alpha flips sign), while the translational offsets along and perpendicular to the axes remain the same. 

are set to zero. Position entries of missing slots are replaced by the mean position of the valid joints within the same group. If the entire group is empty, a fallback hierarchy is used: for instance, a missing elbow position is substituted by the nearest available ancestor in the kinematic chain (upper arm, then shoulder, then torso, then base link). 

During reconstruction from the autoencoder, a separate activation threshold of 0.5 is applied to the decoded axis vectors: any axis whose norm falls below this value is zeroed out, effectively deactivating joints that the decoder assigns negligible rotation to. The extraction threshold (10<sup>_−_2</sup> ) identifies joints absent from the original robot model, whereas the activation threshold (0.5) determines whether the decoder has assigned a meaningful axis to a reconstructed joint slot. 

## **Appendix D. Autoencoder Architecture and Training** 

### _A. Architecture_ 

The autoencoder uses a symmetric encoder–decoder structure. The encoder maps the 120-dimensional input (20 joints times 6 screw parameters) through two hidden layers of size 64 and 32, respectively, down to the latent space of dimension _z_ . The decoder mirrors this structure, mapping from _z_ back to 120 dimensions through hidden layers of size 32 and 64. All hidden layers use the Tanh activation function. The latent dimension _z_ was swept from 2 to 3 across experiments. 

TABLE V: Autoencoder architecture. 

## **Appendix C. Normalization** 

### _A. Position Normalization (Screw)_ 

To make the screw representation comparable across robots of different scales, each robot’s joint positions are first centered by subtracting the base-link position. They are then divided by the robot’s upper-body reference height, defined as the Euclidean distance between the average shoulder position and the base position. This shoulder-to-base distance provides a consistent scale factor that is well-defined even for robots without a distinct neck joint. Since the rotationaxis vectors are already unit-length, no further normalization is applied to them. 

### _B. DH Normalization_ 

For the DH representation, the three length parameters (d, a, and tau) are scaled by the same shoulder-to-base distance used for the screw positions. The two angle parameters (theta and alpha) remain unscaled. In addition, the d-value of the first spine joint is rebased to account for the vertical offset of the base link from the world origin. 

### _C. Missing Data Handling_ 

Not every robot possesses joints in all 14 groups. A joint slot is considered missing when its rotation-axis norm falls below 10<sup>_−_2</sup> during extraction. For such slots, the axis entries 

|Component|Specification|
|---|---|
|Input dimension|120 (20 joints _×_ 6 screw parameters)|
|Hidden layers|[64, 32]|
|Latent dimension|2 – 3 (swept)|
|Activation|Tanh|
|Encoder path|120 _→_64 _→_32 _→z_|
|Decoder path|_z →_32 _→_64 _→_120|


### _B. Loss Function_ 

The total loss combines a reconstruction term and an isometric regularization term. The reconstruction loss is the mean squared error between the input and the reconstructed output. The isometric regularization, based on the Relaxed Distortion Measure, encourages the decoder mapping to locally preserve distances. It is computed from the Gram matrix of the decoder Jacobian: the ratio of the trace of the squared Gram matrix to the square of the trace of the Gram matrix. Latent-space augmentation is applied by interpolating (and slightly extrapolating) between pairs of encoded points: the mixing coefficient is drawn uniformly from [ _−_ 0 _._ 2 _,_ 1 _._ 2), allowing the regularization to act beyond the convex hull of the training encodings. The regularization weight was set to 10<sup>_−_7</sup> . 

### _C. Training Hyperparameters_ 

TABLE VI: Training hyperparameters. 

|Parameter<br>Value|
|---|
|Optimizer<br>Adam<br>|
|Learning rate<br>10<sup>_−_3</sup>|
|Epochs<br>1000|
|Batch size<br>10|
|Device<br>CUDA|


## **Appendix E. Voronoi Optimistic Optimization (VOO)** 

### _A. Algorithm_ 

At each iteration, VOO either performs a global uniform sample with probability _p_ global or a local sample near the current best point. For local sampling, the algorithm identifies the Voronoi radius _r_ of the best point (the squared distance to its nearest evaluated neighbor) and draws candidates within that radius. If no valid candidate is found within _n_ switch uniform trials, the sampler switches to a Gaussian centered on the best point with standard deviation _σ_ = _σc ·_ ~~�~~ _r / d_ , where _d_ is the search-space dimensionality. Each candidate is accepted as soon as its distance to the best point falls below the Voronoi radius, ensuring the new sample lies within the best point’s Voronoi cell. 

_B. Hyperparameters_ 

TABLE VII: VOO hyperparameters used in experiments. 

|Parameter|Value|
|---|---|
|Initial samples (_n_init)|16|
|Max iterations (_T_)|30|
|Total evaluations (_n_init+_T_)|46|
|Global sampling probability (_p_global)|0.55|
|Gaussian coefficient (_σc_)|0.6|
|Uniform-to-Gaussian switch (_n_switch)|20|
|Max inner loop|500|
|Search range [_x_min_, x_max]|[_−_15_,_ 15]|
|Independent runs per model|10|
|Master seed|123456789|


Each run uses _n_ init = 16 uniformly drawn initial samples followed by _T_ = 30 VOO iterations, yielding _n_ eval = 46 evaluations per run. The same search range [ _−_ 15 _,_ 15] is used for both the latent and the raw kinematic space; this is appropriate because the raw features are normalized by each robot’s shoulder-to-base distance (Appendix C), placing them on a comparable scale to the learned latent coordinates. 

