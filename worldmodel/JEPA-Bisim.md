---
title: "JEPA-Bisim: Learning Robust Visual Representations for Planning with Joint-Embedding Predictive World Models"
date: "2026-02-20"
authors: "Leonardo F. Toso; Davit Shadunts; Yunyang Lu; Gloria Geng; Nihal Sharma; Donglin Zhan"
url: https://arxiv.org/abs/2602.18639
pdf: https://arxiv.org/pdf/2602.18639
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.18639)** / [論文ページ](https://arxiv.org/abs/2602.18639)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# JEPA-Bisim: Learning Robust Visual Representations for Planning with Joint-Embedding Predictive World Models 

Leonardo F. Toso<sup>_∗,†_1</sup> , Davit Shadunts<sup>_∗_1</sup> , Yunyang Lu<sup>_∗_1</sup> , Gloria Geng<sup>_∗_1</sup> , Nihal Sharma<sup>2</sup> , Donglin Zhan<sup>1</sup> , Nam H. Nguyen<sup>2</sup> , and James Anderson<sup>1</sup> 

> 1Columbia University, USA 

> 2Capital One, USA 

> *Equal contribution 

##### **Abstract** 

World models learned from high-dimensional visual observations allow agents to make decisions and plan directly in latent space, avoiding pixel-level reconstruction. However, recent latent predictive architectures (JEPAs), including the DINO world model (DINO-WM), display a degradation in test time robustness due to their sensitivity to “slow features”. These include visual variations such as background changes and distractors that are irrelevant to the task being solved. We address this limitation by augmenting the predictive objective with a bisimulation encoder that enforces control-relevant state equivalence, mapping states with similar transition dynamics to nearby latent states while limiting contributions from slow features. We evaluate our model on a navigation task (PointMaze) and on a manipulation task (PushT) under different test-time background changes and visual distractors. Across all benchmarks, our model consistently improves robustness to slow features while operating in a reduced latent space, up to 10 _×_ smaller than that of DINO-WM. Moreover, our model is agnostic to the choice of pretrained visual encoder and maintains robustness when paired with DINOv2, SimDINOv2, and iBOT features. 

## **1 Introduction** 

World models support planning and control by learning latent dynamics from high-dimensional visual observations. An impactful line of recent work centers on Joint Embedding Predictive Architectures (JEPAs), which eschew reconstruction of raw observations in favor of learning representations by predicting future latent embeddings (Grill et al., 2020; Caron et al., 2021; LeCun, 2022; Assran et al., 2023; Sobal et al., 2025; Balestriero and LeCun, 2025). Building on JEPAs, the DINO world model (DINO-WM) (Zhou et al., 2025) learns a latent predictive dynamic by encoding visual observations through a pretrained DINOv2 feature extractor (Oquab et al., 2023). This yields zero-shot planning, with a pretrained, reward-free world model on entirely new tasks. 

Despite their empirical success, JEPAs suffer from a fundamental limitation: they pay too much attention to _slowly changing_ and _task-irrelevant features_ (LeCun, 2022; Sobal et al., 2022). These are aspects of the raw observations that evolve temporally, such as background textures, lighting, camera viewpoints, and distractors. While they frequently co-occur with the related task-irrelevant visual variations (nuisance factors like dynamic distractors, for example), slow features are distinct in that they have no bearing on the control-relevant transition dynamics. But given their disproportional ease of predictability, they also present a degenerate solution to the JEPA objective by _only_ encoding these temporally consistent slow features. Consequently, any downstream world models trained with these poor input representations fail to generalize to 

> †Correspondence to: `leonardo.toso@columbia.edu` . 

1 

test-time environments with _identical_ dynamics to those in training, and diverging in the slow features present in the observations. Indeed, Sobal et al. (2022) verify this behavior empirically. We also observe this in Figure 2. 

Importantly, this limitation _cannot_ be fully resolved by larger visual foundation models alone (such as DINOv2 (Oquab et al., 2023), SimDINOv2 (Wu et al., 2025), iBOT (Zhou et al., 2021), masked autoencoders (He et al., 2022), among others) as they also extract control-irrelevant information. Even with invariant perception modules, the learned latent dynamics may still entangle control-relevant states with nuisance visual features, leading to brittle planning under visual distribution shifts at test time. Ideally, a world model should encode only those aspects of the state that are relevant for predicting future states, while being invariant to task-irrelevant visual factors. 

**Question.** Can we learn latent world models that retain the joint-embedding predictive strengths while also being robust to the slow features? 

We address this question using bisimulation metrics for learning invariant representations on top of pretrained visual feature extractors (i.e., DINOv2, SimDINOv2, iBOT). These metrics define state equivalences based on immediate rewards and transition dynamics, and have been studied as a principled foundation for state abstraction in Markov Decision Processes (MDPs) (Ferns et al., 2004; Castro et al., 2009), transfer learning (Castro and Precup, 2010), and invariant representation learning (Zhang et al., 2021; Kemertas and AumentadoArmstrong, 2021; Tkachev and Abate, 2011; Shimizu and Tomizuka, 2025). By construction, encoders trained with a bisimulation regularizer discard nuisance features that do not affect control, making it a natural candidate for addressing 


Figure 1: Visually distinct observations that differ only in background (checkerboard and gradient) are first mapped to latent embeddings _Z_ and _Z_<sup>_′_</sup> by a pretrained encoder (initial state in green, goal in red). A bisimulation encoder then projects these into lowerdimensional representations _W_ and _W_<sup>_′_</sup> , which are equivalent under on-policy transition dynamics. 

the slow-feature limitation of JEPAs. Compared to methods that learn distance-aware representations (Park et al., 2024; Wang et al., 2026), our approach specifically targets the adaptation of rich pretrained visual feature spaces (DINOv2, SimDINOv2, iBOT) for planning, leveraging their semantic richness while suppressing control-irrelevant information. 

**Key Point.** DINO-WM (Zhou et al., 2025) displays a substantial degradation in performance on relatively simple navigation tasks (e.g., PointMaze (Fu et al., 2020)) when evaluated under background changes and visual distractors at test time (see Figure 2). To address this, we propose a _bisimulation encoder_ for visual world models that augments latent dynamics with an on-policy bisimulation objective, enforcing invariance in the learned latent space. The bisimulation encoder is trained jointly with the transition model, enforcing states with similar transition behavior to be mapped to nearby latent embeddings while discarding task-irrelevant visual information (see Figure 1). Importantly, we also show that the reward signal is not fundamental to learning invariant world-model representations, thus simplifying training. 

2 

#### **Contributions.** Our main contributions are as follows: 

_•_ We propose a bisimulation encoder for visual world models that enforces control-relevant state equivalence while discarding task-irrelevant visual features from pretrained visual feature extractors (e.g., DINOv2, SimDINOv2, iBOT). 

_•_ We integrate the bisimulation objective into a latent predictive world model architecture (see Figure 3), showing that invariant representations can be learned jointly with the transition model _without_ relying on reward prediction. 

_•_ We show that our bisimulation encoder yields robust planning performance under several background changes and moving distractors for navigation and manipulation tasks, with latent embeddings dimensions that are 10 _×_ smaller than DINO-WM. 

Apart from the works referenced above, we also draw inspiration from the myriad works on joint embedding predictive architectures, introduced in LeCun (2022); Sobal et al. (2025), as well as the seminal works of Castro et al. (2009); Castro and Precup (2010); Zhang et al. (2021) on bisimulation metrics and invariant representations. As a result, this paper is also closely related to work at the intersection of modelbased control and latent world models (Sun et al., 2024; Lim et al., 2025). We refer the reader to Appendix A.1 for a more detailed discussion. 


Figure 2: Rollouts for PointMaze navigation under a background change at test time. For clarity, the background change is not depicted in the figure. See Section 4.2 for details on background changes. While DINOWM fails to reach the goal due to background change our model succeeds. 

## **2 Preliminaries** 

Throughout, we consider a vision- 

based control task given by a partially observable MDP (POMDP) that evolves in discrete time _t ∈{_ 0 _,_ 1 _,_ 2 _, . . . }_ . An observation is an RGB image _ot ∈O_ , an action is denoted by _at ∈A_ , and a trajectory is a sequence ( _ot, at, ot_ +1 _, at_ +1 _, . . ._ ). We denote the data distribution induced by a behavior policy _π_ by _Dπ_ , meaning that ( _ot, at, ot_ +1) _∼Dπ_ when rollouts are generated by playing the environment with _π_ . We use E _Dπ_ [ _·_ ] to denote the expectation with respect to this data distribution. We use _B_ to denote the replay buffer (distinct from the data distribution _Dπ_ ); the replay buffer stores previously collected transitions and is used for pairwise comparisons in the bisimulation loss (see Appendix A.2). 

### **2.1 Joint-Embedding Predictive Architectures** 

JEPAs learn a visual encoder _fθ_ : _O →_ R<sup>_dz_</sup> that maps an observation _ot_ to a latent embedding, i.e., _zt_ = _fθ_ ( _ot_ ) _∈_ R<sup>_dz_</sup> _,_ where _dz_ is the embedding dimension and _θ_ is the vector of encoder parameters. Jointly, a predictor (i.e., latent dynamics model) _T_<sup>˜</sup> _ϕ_ : R<sup>_dz_</sup> _× A →_ R<sup>_dz_</sup> is trained to 

3 


Figure 3: Model architecture and training objectives. 

map the current latent state and action to a predicted next latent state _z_ ˆ _t_ +1 = _T_<sup>˜</sup> _ϕ_ ( _zt, at_ ) _,_ with parameters _ϕ_ . 

Since representations are defined up to arbitrary invertible transformations, JEPA training includes a target embedding. The target is denoted by _zt_ +1 = _fθ_ ( _ot_ +1). The JEPA objective minimizes the prediction loss between _z_ ˆ _t_ +1 and _zt_ +1, 


where _ℓ_ : R<sup>_dz_</sup> _×_ R<sup>_dz_</sup> _→_ R+ is the mean squared error. 

We emphasize that DINO-WM (Zhou et al., 2025), follow this principle, with the key distinction that the visual encoder parameters _θ_ are fixed and not learned during training. The motivation for using frozen pretrained encoders rather than learning from scratch is twofold: (i) large-scale pretrained visual features (DINOv2, SimDINOv2, iBOT) provide semantically rich representations that improve sample efficiency for dynamics learning, and (ii) fixing the encoder decouples representation learning from dynamics learning, enabling modular composition with different visual backbones. The bisimulation encoder then adapts these fixed features to be control-relevant, combining the best of both worlds. Therefore, observations are first mapped to latent embeddings using a pretrained visual foundation model (e.g., DINOv2 (Oquab et al., 2023)), and a predictive dynamics model is trained on top of that latent space. Here, we also treat the pretrained visual encoder as fixed and train an extra bisimulation encoder jointly with the dynamics on top of it. 

**Remark 2.1** (Slow Features) **.** _We emphasize that JEPAs inadvertently focus on the slow features. In particular, when observations contain static backgrounds or persistent distractors that vary slowly relative to task-relevant dynamics, the prediction loss_ (1) _can be minimized by encoding such features into the latent embedding zt_ = _fθ_ ( _ot_ ) _, since they induce small temporal differences ∥zt_ +1 _− zt∥. As a result, slowly varying nuisance information may dominate the predictive objective, leading to latent embeddings that fail to capture the underlying task structure (Sobal et al., 2022) and thus are not generalizable to background changes at test time (see Figure 2). This limitation motivates the use of bisimulation. By defining latent distances in terms of on-policy transition behavior, bisimulation induces representations that collapse nuisance visual features while preserving the task-relevant information for planning._ 

### **2.2 Bisimulation Metric** 

Let us now (informally) revisit the definition of on-policy bisimulation metrics from Castro (2020). Intuitively, two latent states, in the pretrained visual encoder space, _z_ and _z_<sup>_′_</sup> are 

4 

“bisimilar” if they induce similar immediate rewards (for optimality equivalence) and similar future state evolution (for dynamics equivalence) under the same actions. 

Here, the environment is partially observed and represented through latent embeddings obtained from a visual encoder (e.g., DINOv2, SimDINOv2, iBOT). The goal is to learn a lower-dimensional representation _w_ = _hη_ ( _z_ ) _∈_ R<sup>_dw_</sup> , with _dw ≪ dz_ , that preserves controlrelevant structure while discarding nuisance visual variation. We formalize state equivalence with the _on-policy_ bisimulation metric (Castro, 2020). 

**Definition 2.1** (On-Policy Bisimulation Metric (Castro, 2020)) **.** _Given a policy π, a reward function r_ ( _z, a_ ) _, and a transition kernel Pπ_ ( _· | z_ ) _induced by π, the on-policy bisimulation metric is_ 


_where γ ∈_ (0 _,_ 1) _is the discount factor and W_ 1 _denotes the_ 1 _-Wasserstein distance._ 

**On Dropping the Reward Term.** Note that _dπ_ ( _z, z_<sup>_′_</sup> ) has two terms: a reward similarity term _|rπ_ ( _z_ ) _− rπ_ ( _z_<sup>_′_</sup> ) _|_ and a dynamics similarity term measured via the 1-Wasserstein distance (Givens and Shortt, 1984). The reward term ensures that if two state trajectories are similar, they are not collapsed if they yield different rewards. In particular, such reward discrepancy is crucial when bisimulation is used for policy transfer or value-function approximation (Ferns et al., 2004; Castro et al., 2009; Castro and Precup, 2010). However, for the purpose of learning an invariant representation for JEPAs, we claim that this term is not fundamental. That is because the transition term alone induces a meaningful notion of equivalence: states that exhibit similar evolution under the same action sequences are mapped to nearby latent representations in the bisimulation latent space (see our illustration in Figure 1). 

Moreover, dropping the reward term is well aligned with JEPAs, which are trained without reward signal on offline trajectory data and rely on predictive consistency in latent space rather than task-specific reward structure. Incorporating rewards would require task-specific supervision and would break the modularity between representation learning and zero-shot downstream planning, i.e., a core design principle of JEPAs (LeCun, 2022). Accordingly, we omit the reward term in our implementation and rely only on approximating the Wasserstein transition similarity to enforce invariance. This design choice is also supported numerically in Appendix A.8, where a reward predictor is included. 

### **2.3 Learning Invariant Representations** 

Now, we discuss the invariant representation learning problem for our joint-embedding predictive world model. Recall that _zt_ = _fθ_ ( _ot_ ) _∈_ R<sup>_dz_</sup> typically contains both control-relevant information and nuisance features. Our goal is to learn an encoder _wt_ = _hη_ ( _zt_ ) _∈_ R<sup>_dw_</sup> _,_ that limits the contribution of the slow features in the transition dynamics. 

To do so, we jointly learn the dynamics in the bisimulation space through _Tϕ_ : R<sup>_dw_</sup> _× A →_ R<sup>_dw_</sup> _,_ such that _w_ ˆ _t_ +1 = _Tϕ_ ( _wt, at_ ) predicts the next latent state. With the notation set up in Section 2.1, we have the predictive dynamics augmented with the bisimulation encoder, i.e., _Tϕ_ ( _hη_ ( _fθ_ ( _ot_ )) _, at_ ), where again _θ_ is fixed. 

To connect invariance to bisimulation, we consider an abstract state space _W ⊆_ R<sup>_dw_</sup> equipped with the metric _dπ_ . We aim to learn _hη_ and _Tϕ_ jointly so that the distances in 

5 

_W_ approximate an on-policy bisimulation metric, meaning that states that are equivalent for control under rollouts are mapped nearby in such latent space. We do this by optimizing a bisimulation objective that aligns pairwise latent distances with a target quantity that compares on-policy dynamics. Concretely, for a pair of observation, action, and next observation ( _ot, at, ot_ +1) and � _o_<sup>_′_</sup> _t_<sup>_, a′_</sup> _t_<sup>_, o′_</sup> _t_ +1� drawn from _Dπ_ , we have the latent states 


The transition dynamics _Tϕ_ is trained using 


and we note that, in practice, as we do not have _Dπ_ , we compute the empirical mean (MSE) instead. 

On the other hand, for invariance, our loss encourages the distance _∥wt − wt_<sup>_′∥_</sup> 2<sup>tomatcha</sup> control-relevant similarity signal measured by the bisimulation metric. We define the on-policy one-step bisimulation target between states as ∆bisim( _η, ϕ_ ) ≜ _γ ∥Tϕ_ ( _wt, at_ ) _− Tϕ_ ( _wt_<sup>_′, a′_</sup> _t_<sup>)</sup><sup>_∥_</sup> 2<sup>_,_</sup> where it compares the predicted next latent states under the learned dynamics. Note that the actions _at_ and _a_<sup>_′_</sup> _t_<sup>aredrawnindependentlyfromthetwoseparatetrajectoriessampledfrom</sup> the replay buffer _B_ ; they are not required to be the same. This is consistent with the on-policy bisimulation formulation of Castro (2020), where the metric averages over the policy’s action distribution. In practice, using independently sampled actions provides a diverse set of comparisons across the replay buffer, which stabilizes training. We fit the bisimulation encoder by minimizing the following loss: 


Finally, we define the overall training objective as follows: 


with _λ_ bisim _>_ 0 being the regularization weight. 

Minimizing the loss formalizes our goal of learning a compact latent space that preserves on-policy predictive structure for planning while suppressing task-irrelevant visual features. We next describe the architecture, loss instantiation, and planning in the learned bisimulation space. 


## **3 Our World Model** 

Figure 4: Bisimulation encoder with patch-based design, with 196 of patches and 32 output patch dimension. 

We now describe our architecture for with 196 of patches and 32 output patch dimension. learning invariant world models that builds on pretrained visual features (DINOv2, SimDINOv2, and iBOT) and augments them with a bisimulation encoder to suppress task-irrelevant information. The model learns latent transition dynamics and performs planning with CEM. An overview of the pipeline objectives is shown in Figure 3. 

6 

### **3.1 Pretrained Encoders** 

In our experiments, we consider three self-supervised visual encoders: DINOv2 (Oquab et al., 2023) (with ViT-S/14), SimDINOv2 (Wu et al., 2025) (with ViT-B/16), and iBOT (Zhou et al., 2021) (with ViT-S/16). These are trained on large-scale image datasets using joint embedding or masked prediction objectives and have been shown to produce semantically rich visual features (Jiang et al., 2023). We include SimDINOv2 as a variant of DINOv2 that incorporates codingrate regularization for improved feature quality, and iBOT as a masked-prediction alternative. These pre-trained encoders allow us to assess whether the bisimulation encoder’s benefits are agnostic to the choice of visual backbone. When using DINOv2 features, we refer to our model as DINO-Bisim. 

### **3.2 Bisimulation Encoder** 

Given pretrained visual embeddings _zt_ , we learn a bisimulation encoder _hη_ : R<sup>_Np×dz_</sup> _→_ R<sup>_Np×dw_</sup> _,_ where _wt_ = _hη_ ( _zt_ ) _,_ as discussed in Section 2.2. We note that in contrast to Zhang et al. (2021); Shimizu and Tomizuka (2025), our bisimulation encoder is designed in patches (we refer the reader to Appendix A.2.3 for details). Such encoder consists of a per-patch residual MLP projection head (Linear-ResMLP-Linear) that maps each DINOv2 patch embedding (or raw image patch) into a _dw_ = 32 dimensional latent, followed by learned spatial positional embeddings and LayerNorm. 

This encoder is trained to ensure that distances in the _w_ -space reflect on-policy bisimulation distances, as defined in (2). To this end, we _flatten_ the spatial patch features prior to computing the previously defined losses and compare states across different trajectories that are stored in a replay buffer _B_ , following Zhang et al. (2021). However, minimizing the bisimulation loss admits degenerate solutions as mapping all states to a single representation trivially minimizes pairwise distances, and we refer to this as the representation _collapse_ . To circumvent such collapse, prior work (Bardes et al., 2021; Zhu et al., 2023) has adopted variance-invariancecovariance regularization (VICReg) to guarantee that each latent dimension keeps sufficient variance over batches of states (i.e., to guarantee that the latents are sufficiently spread). We refer the reader to (Bardes et al., 2021, Section 4.1) for an excellent overview of the approach. Here, invariance is given by the bisimulation loss. 

In our setting, however, the standard VICReg (Bardes et al., 2021) _may be_ insufficient. This is because, for the pretrained visual encoders considered in this work (i.e., DINOv2, SimDINOv2, and iBOT) a large fraction of the variance is often concentrated in a Figure 5: Visualization of the first principal component small number of principal compo(PC1) of latent embeddings produced by different visual nents that correlate with the slow feature encoders for a PointMaze observation. In all cases, features rather than task-relevant PC1 predominantly encodes background and layout information rather than control-relevant features, motivating dynamics. Therefore, imposing a uniform variance across all coordiour PCA-based VC-Reg in the bisimulation encoder. nates may preserve nuisance visual features, preventing the bisimulation encoder from collapsing the task-irrelevant information. 

Figure 5: Visualization of the first principal component (PC1) of latent embeddings produced by different visual feature encoders for a PointMaze observation. In all cases, PC1 predominantly encodes background and layout information rather than control-relevant features, motivating our PCA-based VC-Reg in the bisimulation encoder. 

Leveraging this insight, we propose a PCA-based variance-covariance regularization (VCReg) loss, which adapts VICReg to pretrained visual embeddings by guaranteeing a minimum variance in directions that are not dominated by a large fraction of slow features. Throughout 

7 

the paper, we use VICReg to refer to the original formulation of Bardes et al. (2021), which enforces variance, invariance, and covariance regularization uniformly across all latent dimensions. We use VC-Reg (or PCA-VC-Reg) to refer to our variant, which applies variance and covariance regularization selectively in the PCA basis, omitting the invariance term (handled by the bisimulation loss instead). 

### **3.3 PCA-based Variance Covariance Regularization** 

As illustrated in Figure 5, the pretrained visual embeddings from DINOv2, SimDINOv2, and iBOT allocate a large amount of variance to the first principal component (PC1), which are correlated with task-irrelevant features coming from backgrounds and distractors. This concentration of task-irrelevant variance in the leading PC is a common property of self-supervised visual encoders: as noted in the DINOv2 paper (Oquab et al., 2023), background information tends to dominate the first principal component and can be attenuated by thresholding it. While this property may not hold universally for all encoders or environments, it is observed consistently for DINOv2, SimDINOv2, and iBOT in our PointMaze setting (see Figure 5 and Appendix A.3). If we use the standard VICReg loss with uniform variance across the coordinates of the bisimulation latent space, the optimizer may still preserve such irrelevant directions simply to satisfy the variance threshold, conflicting with the goal of learning a representation invariant to those slow features. Therefore, we do VC-Reg in the PCA basis of the current batch (see Appendix A.3 for more details). 

We emphasize that if the visual encoder does not isolate control-irrelevant features within a dominant principal component, the PCA-based VC-Reg regularization becomes _optional_ . In this case, the bisimulation-based encoder alone can mitigate, though only partially, the influence of task-irrelevant variations in the learned representation. 

### **3.4 Transition Model** 

We model latent dynamics using a vision transformer that predicts the next state in the bisimulation latent space. Following DINO-WM (Zhou et al., 2025), the vision transformer architecture (Dosovitskiy, 2020) is suitable for processing the underlying patch-based embeddings. Since the bisimulation latent states are already represented as sequences of patch embeddings, we remove the ViT tokenization layer, yielding a transformer architecture operating directly on patchlevel bisimulation features without a separate tokenization step (analogous to a “decoder-only” design in LLMs, where the transformer processes tokens causally without a separate encoder). 

The transition model takes as input a history of past bisimulation latent states and actions across multiple trajectories, _{_ ( _wj,t−H_ : _t−_ 1 _, aj,t−H_ : _t−_ 1) _}_<sup>_N_</sup> _j_ =1<sup>traj</sup><sup>_,_where</sup><sup>_H_denotesthecontextlength</sup> and _N_ traj the number of trajectories, and it predicts the next latent state _w_ ˆ _t_ (i.e., in the bisimulation space). Note that the subscript _j_ denotes the trajectory embedding and action at time step _t_ . To respect temporal causality, a causal attention mask is implemented (as in Zhou et al. (2025)) ensuring that predictions at time _t_ depend only on past latent states and actions. More precisely, each patch embedding _wt_<sup>_i_attendstothecorrespondingpatch</sup> embeddings _{wt_<sup>_i_</sup> _−H_ : _t−_ 1<sup>_}N_</sup> _i_ =1<sup>_p_overthecontext.Predictingallpatchesjointlyyieldsglobalspatial</sup> structure and temporal dynamics that improve temporal generalization as discussed in Zhou et al. (2025). 

By “filtering out” task-irrelevant visual features, the bisimulation encoder enables the transition model to learn dynamics that are invariant to nuisance visual factors (backgrounds, distractors), focusing only on control-relevant state transitions. The learned joint-embedding predictive world model is then used for planning via MPC (Kouvaritakis and Cannon, 2016), with actions selected using the cross-entropy method (CEM). 

8 

### **3.5 Planning** 

Given an initial observation _o_ 0 and a goal observation _o_ g, we encode _w_ 0 = _hη_ ( _fθ_ ( _o_ 0)) and the goal _w_ g = _hη_ ( _fθ_ ( _o_ g)). For a fixed goal, we define the latent goal-reaching cost as follows: 


We optimize the action sequence **_a_** = ( _a_ 0 _, . . . , aT −_ 1) through the learned latent dynamics: 


We solve this terminal-cost objective using CEM with a planning horizon of _T_ = 5 in a recedinghorizon MPC scheme, executing the first action and replanning at each step. Our bisimulation latent space is 10 _×_ smaller than DINO-WM’s, reducing the computational cost of latent rollouts. 

### **3.6 A Generalization Bound** 

Before turning to the experiments, we also provide a theoretical justification for learning bisimulation-based representations on top of JEPA latents. Let us first define the _T_ -step onpolicy cost-to-go as follows: 


where the expectation is taken over trajectories _{zt}_<sup>_T_</sup> _t_ =0<sup>inducedbypolicy</sup><sup>_π_andtransition</sup> kernel _Pπ_ starting from a visual pretrained latent state _z_ 0 = _z_ . We defer the proof of Theorem 3.1 to Appendix A.11. 

**Theorem 3.1** (Reward-free planning generalization bound) **.** _Suppose hη_ ( _·_ ) _ε-approximately preserves the reward-free bisimulation metric in the sense that_ 


_In addition, suppose that hη_ ( _·_ ) _is uniformly bounded as ∥hη_ ( _z_ ) _∥_ 2 _≤ Hw for all z and thus ∥wg∥_ 2 _≤ Hw. Then for any two pretrained visual latent embeddings z, z_<sup>_′_</sup> _,_ 


We also note that the linear dependence on the horizon _T_ contrasts with the (1 _−γ_<sup>_T_</sup> ) _/_ (1 _−γ_ ) dependence from (Zhang et al., 2021; Shimizu and Tomizuka, 2025). This difference arises from dropping the reward term in the bisimulation metric: while reward-aware bisimulation enables geometric discounting of cost discrepancies through immediate reward alignment, a reward-free metric propagates the discrepancies through the transition dynamics, yielding a cumulative horizon-dependent bound. In this sense, the _T_ factor can be interpreted as the price paid for enforcing control-relevant invariance without task-specific reward supervision. 

**Key Takeaway.** The above result implies that if two latent states in the pretrained visual encoder space differ only due to nuisance visual variations, such as slow features, then their induced planning behavior remains similar. More concretely, let _z_ = _fθ_ ( _o_ ) embed a PointMaze scene with a checkerboard background, and let _z_<sup>_′_</sup> = _fθ_ ( _o_<sup>_′_</sup> ) embed the same scene with a gradient background (see Figure 1), since these visual changes do not affect on-policy transition behavior, the bisimulation distance _dπ_ ( _z, z_<sup>_′_</sup> ) is small. Consequently, the difference in the induced planning cost is bounded by _O_ ( _dπ_ ( _z, z_<sup>_′_</sup> ) _T_ ). Therefore, robustness of planning when starting from _w_ or _w_<sup>_′_</sup> in the bisimulation latent space is governed by their distance in that space. 

9 

## **4 Experiments** 

We now evaluate<sup>1</sup> our world model by comparing it with DINO-WM Zhou et al. (2025) and domain randomization (DR) Tobin et al. (2017) for a navigation task (PointMaze) and a manipulation task (PushT) under different visual conditions, and pretrained visual encoders. Further details on the task setup are provided in Appendix A.4. 

**Evaluation Metric.** We evaluate each condition using 50 independently sampled initial and goal pairs and define success rate (SR) as the fraction of successful episodes. We report the absolute SR under the native background (NC) and the relative degradation under each shifted condition _s_ , defined as ∆ _s_ = 100 _×_ (1 _−_ SR _s/_ SRNC). Positive values indicate a percentage decrease relative to the same model’s native-background performance, while negative values indicate improvement. We also report the mean relative degradation across the five shifted conditions (SC, C, LC, LCG, and D). Lower degradation is better. 

### **4.1 Baseline** 

We compare our model with two baselines: DINO-WM Zhou et al. (2025) and domain DR Tobin et al. (2017). Both baselines are evaluated under the same task, planning horizon, and evaluation metric previously described. 


Figure 6: Visual distribution shifts used to evaluate robustness on **PointMaze** (top) and **PushT** (bottom). From left to right, the conditions are: **NC** : No Change, **SC** : Slight Change, **C** : Color Gradient, **LC** : Large Color Change, **LCG** : Large Color Gradient, and **D** : moving Distractors. 

**DINO-WM.** We use the original bustness on **PointMaze** (top) and **PushT** (bottom). DINO-WM architecture as proposed From left to right, the conditions are: **NC** : No Change, in Zhou et al. (2025). The model **SC** : Slight Change, **C** : Color Gradient, **LC** : Large Color operates directly on pretrained DIChange, **LCG** : Large Color Gradient, and **D** : moving DisNOv2 patch embeddings with 196 tractors. patches, each of dimensionality 384, and learns latent dynamics without explicit invariance regularization. DINO-WM is trained with a batch size of 32. 

### **4.2 Background Changes** 

**Domain Randomization (DR).** We also train DINO-WM with domain randomization Tobin et al. (2017). In particular, we randomize the visual appearance of the task for 40% of the training dataset by applying background color changes and gradient-based background modifications, for the PointMaze task. To avoid introducing spurious temporal artifacts, the randomized background is kept consistent across trajectories. We refer the reader to Appendix A.7. 

Our model adopts the same number of visual patches (i.e., 196) as DINO-WM, but introduce a bisimulation encoder that maps each patch to a 32-dimensional latent embedding (see Figure 4). This leads to a latent space that is 10 _×_ lower-dimensional than the 384-dimensional patch embeddings used by DINO-WM. Our model is trained with a batch size of 20. We refer the reader to Appendix A.2.4 for details on the model hyperparameters. 

10 

Table 1: **PointMaze.** Absolute success rate under NC ( _↑_ ) and relative degradation (%, _↓_ ) under shifts. Negative values indicate improvement. Avg.: mean degradation over the five background shifts. 

|**Model**|**NC**<br>(Abs.)|**SC**<br>(Rel.%)|**C**<br>(Rel.%)|**LC**<br>(Rel. %)|**LCG**<br>(Rel.%)|**D**<br>(Rel.%)|**Avg**<br>(Rel.%)|
|---|---|---|---|---|---|---|---|
|_Comparison with D_|_R_|||||||
|DINO-WM|0.8|10.0|25.0|30.0|40.0|2.5|21.5|
|DINO-WM w/DR|0.82|0.0|0.0|17.1|22.0|0.0|7.8|
|**Ours (DINOv2)**|0.78|_−_2_._6|2.6|_−_10_._3|0.0|_−_5_._1|_−_**3**_._**1**|
|_Encoder ablation_||||||||
|End-to-End|0.68|35.3|_−_2_._9|61.8|47.1|5.9|29.4|
|SimDINOv2|0.40|5.0|10.0|_−_5_._0|_−_5_._0|10.0|3.0|
|iBOT|0.72|2.8|_−_2_._8|0.0|0.0|0.0|**0**_._**0**|


### **4.3 Results** 

We consider different background changes and moving distractors (see Figure 6) that alter the visual appearance of the scene while preserving the underlying transition dynamics. These changes are applied only at test time, unless otherwise stated, and are designed to isolate the effect of slow features on the planning performance. The moving distractors (colored dots) move continuously within the maze but do not collide with or affect the agent. 

Table 1 reports the absolute success rate under NC and relative degradation under background changes and a moving distractor for PointMaze. Negative degradation indicates improvement over the same model’s native-background performance. 

**Robustness to the background.** DINO-WM degrades when the visual background differs from the one seen during training, with relative degradation ranging from 10 _._ 0% under SC to 40 _._ 0% under LCG. In contrast, our model largely preserves its native-background performance, with degradation ranging from _−_ 10 _._ 3% to 2 _._ 6% across background changes. These results are consistent with the bisimulation encoder reducing sensitivity to background-dependent features, supporting reliable planning despite visual changes. 

**Comparison with DR.** Domain randomization preserves performance under SC and C, with 0 _._ 0% degradation in both conditions. However, degradation increases to 22 _._ 0% under LCG, an aggressive background change not covered by the randomized training distribution. Our model exhibits 0 _._ 0% degradation under this condition, retaining its native-background performance. 

**Moving distractor.** Under the moving distractor, DINO-WM exhibits a small relative degradation of 2 _._ 5%, while domain randomization preserves its native-background performance. Our model achieves _−_ 5 _._ 1% degradation, corresponding to a small observed improvement over its NC baseline. 

Table 2 evaluates visual robustness on PushT in a data-scarce setting, with both models trained on only 1 _,_ 000 samples. DINO-Bisim achieves a mean relative degradation of 7 _._ 8% across the five visual shifts, compared to 47 _._ 6% for DINO-WM. The advantage is larger under aggressive background changes: degradation under LC and LCG is 11 _._ 0% for DINO-Bisim, 

> 1Code to reproduce the results can be found at `https://github.com/jd-anderson/dino_bsmpc` . 

11 

Table 2: **PushT under data scarcity.** Both models are trained on 1 _,_ 000 samples. We report absolute success rate under NC ( _↑_ ) and relative degradation (%, _↓_ ) under five visual shifts. Avg. denotes mean relative degradation across the shifted conditions. 

||**NC**|**SC**|**C**|**LC**|**LCG**|**D**|**Avg.**|
|---|---|---|---|---|---|---|---|
|**Model**|(Abs.)|(Rel.%)|(Rel.%)|(Rel.%)|(Rel.%)|(Rel.%)|(Rel.%)|
|DINO-WM|0.48|21.0|21.0|71.0|50.0|75.0|47.6|
|DINO-Bisim|0.36|0.0|0.0|11.0|11.0|17.0|**7.8**|


compared to 71 _._ 0% and 50 _._ 0%, respectively, for DINO-WM. Under moving distractors, DINOBisim also exhibits lower degradation (17 _._ 0% versus 75 _._ 0%). 

Despite its lower native success rate (0 _._ 36 versus 0 _._ 48), DINO-Bisim achieves higher average absolute success across the five shifted conditions. These results support improved robustness under visual shifts when training data are limited. 

### **4.4 On Different Pretrained Visual Encoders** 

Table 1 compares native-background success rates and relative degradation across visual encoders. End-to-end training (i.e., training a visual encoder from scratch) yields 29 _._ 4% mean degradation, compared to _−_ 3 _._ 1% with DINOv2, suggesting that pretrained features support robustness when combined with our bisimulation encoder. SimDINOv2 and iBOT also retain their native-background performance, with mean degradation of 3 _._ 0% and 0 _._ 0%, respectively. Thus, robustness extends across pretrained encoders. 

## **5 Discussions and Future Work** 

We show that DINO-WM is not robust under background changes and distractors. By enforcing control-relevant invariance via bisimulation on top of pretrained visual features, we obtain latent embeddings 10 _×_ lower-dimensional than that of DINO-WM that are robust for planning under visual shifts, without reward supervision. 

Our work has two main limitations: it relies on informative pretrained visual features, as suggested by reduced robustness without pretraining (i.e., End-to-End in Table 1), and its rewardfree bisimulation analysis yields a horizon-dependent bound that is looser than its reward-aware counterpart. Future work includes integrating the bisimulation encoder into gradient-based planning (Parthasarathy et al., 2025), adapting representations online to new visual conditions, extending the analysis to reward-aware bisimulation, and evaluating more complex manipulation and long-horizon tasks. 

## **6 Acknowledgments** 

Leonardo F. Toso is funded by the Center for AI and Responsible Financial Innovation (CAIRFI) Fellowship and the Columbia Presidential Fellowship. James Anderson is partially funded by NSF grants EECS 2144634 and CNS 2535097 and the Center of AI Technology (CAIT) in collaboration with Amazon. 

12 

## **References** 

- Abate, A. (2013). Approximation metrics based on probabilistic bisimulations for general statespace markov processes: a survey. _Electronic Notes in Theoretical Computer Science_ , 297:3– 25. 

- Assran, M., Duval, Q., Misra, I., Bojanowski, P., Vincent, P., Rabbat, M., LeCun, Y., and Ballas, N. (2023). Self-supervised learning from images with a joint-embedding predictive architecture. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15619–15629. 

- Balestriero, R. and LeCun, Y. (2025). Lejepa: Provable and scalable self-supervised learning without the heuristics. _arXiv preprint arXiv:2511.08544_ . 

- Bardes, A., Ponce, J., and LeCun, Y. (2021). Vicreg: Variance-invariance-covariance regularization for self-supervised learning. _arXiv preprint arXiv:2105.04906_ . 

- Caron, M., Touvron, H., Misra, I., J´egou, H., Mairal, J., Bojanowski, P., and Joulin, A. (2021). Emerging properties in self-supervised vision transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 9650–9660. 

- Castro, P. and Precup, D. (2010). Using bisimulation for policy transfer in mdps. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 24, pages 1065–1070. 

- Castro, P. S. (2020). Scalable methods for computing state similarity in deterministic markov decision processes. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 34, pages 10069–10076. 

- Castro, P. S., Panangaden, P., and Precup, D. (2009). Equivalence relations in fully and partially observable markov decision processes. In _IJCAI_ , volume 9, pages 1653–1658. 

- Dosovitskiy, A. (2020). An image is worth 16x16 words: Transformers for image recognition at scale. _arXiv preprint arXiv:2010.11929_ . 

- Ferns, N., Panangaden, P., and Precup, D. (2004). Metrics for finite markov decision processes. In _UAI_ , volume 4, pages 162–169. 

- Ferns, N., Panangaden, P., and Precup, D. (2011). Bisimulation metrics for continuous markov decision processes. _SIAM Journal on Computing_ , 40(6):1662–1714. 

- Fu, J., Kumar, A., Nachum, O., Tucker, G., and Levine, S. (2020). D4rl: Datasets for deep data-driven reinforcement learning. _arXiv preprint arXiv:2004.07219_ . 

- Givens, C. R. and Shortt, R. M. (1984). A class of wasserstein metrics for probability distributions. _Michigan Mathematical Journal_ , 31(2):231–240. 

- Grill, J.-B., Strub, F., Altch´e, F., Tallec, C., Richemond, P., Buchatskaya, E., Doersch, C., Avila Pires, B., Guo, Z., Gheshlaghi Azar, M., et al. (2020). Bootstrap your own latent-a new approach to self-supervised learning. _Advances in neural information processing systems_ , 33:21271–21284. 

- Ha, D. and Schmidhuber, J. (2018). World models. _arXiv preprint arXiv:1803.10122_ , 2(3). 

- Hafner, D., Lillicrap, T., Ba, J., and Norouzi, M. (2020). Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations_ . 

13 

- Hafner, D., Lillicrap, T., Fischer, I., Villegas, R., Ha, D., Lee, H., and Davidson, J. (2019). Learning latent dynamics for planning from pixels. In _International conference on machine learning_ , pages 2555–2565. PMLR. 

- He, K., Chen, X., Xie, S., Li, Y., Doll´ar, P., and Girshick, R. (2022). Masked autoencoders are scalable vision learners. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 16000–16009. 

- Jiang, D., Liu, Y., Liu, S., Zhao, J., Zhang, H., Gao, Z., Zhang, X., Li, J., and Xiong, H. (2023). From clip to dino: Visual encoders shout in multi-modal large language models. _arXiv preprint arXiv:2310.08825_ . 

- Kemertas, M. and Aumentado-Armstrong, T. (2021). Towards robust bisimulation metric learning. _Advances in Neural Information Processing Systems_ , 34:4764–4777. 

- Kouvaritakis, B. and Cannon, M. (2016). Model predictive control. _Switzerland: Springer International Publishing_ , 38(13-56):7. 

- LeCun, Y. (2022). A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. _Open Review_ , 62(1):1–62. 

- Lenz, I., Knepper, R. A., and Saxena, A. (2015). Deepmpc: Learning deep latent features for model predictive control. In _Robotics: Science and Systems_ , volume 10, page 25. Rome, Italy. 

- Lim, J. Y., Ikram, Z., Yu, S., Ma, H., Leong, T.-Y., and Liu, D. (2025). Jedi: Latent end-toend diffusion mitigates agent-human performance asymmetry in model-based reinforcement learning. _arXiv preprint arXiv:2505.19698_ . 

- Maes, L., Lidec, Q. L., Scieur, D., LeCun, Y., and Balestriero, R. (2026). Leworldmodel: Stable end-to-end joint-embedding predictive architecture from pixels. _arXiv preprint arXiv:2603.19312_ . 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec, M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., El-Nouby, A., et al. (2023). Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ . 

- Park, S., Kreiman, T., and Levine, S. (2024). Foundation policies with hilbert representations. _arXiv preprint arXiv:2402.15567_ . 

- Parthasarathy, A., Kalra, N., Agrawal, R., LeCun, Y., Bounou, O., Izmailov, P., and Goldblum, M. (2025). Closing the train-test gap in world models for gradient-based planning. _arXiv preprint arXiv:2512.09929_ . 

- Rubinstein, R. Y. and Kroese, D. P. (2004). _The cross-entropy method: a unified approach to combinatorial optimization, Monte-Carlo simulation and machine learning_ . Springer Science & Business Media. 

- Shimizu, Y. and Tomizuka, M. (2025). Bisimulation metric for model predictive control. In _International Conference on Learning Representations_ . 

- Sobal, V., SV, J., Jalagam, S., Carion, N., Cho, K., and LeCun, Y. (2022). Joint embedding predictive architectures focus on slow features. _arXiv preprint arXiv:2211.10831_ . 

14 

- Sobal, V., Zhang, W., Cho, K., Balestriero, R., Rudner, T. G., and LeCun, Y. (2025). Learning from reward-free offline data: A case for planning with latent dynamics models. _arXiv preprint arXiv:2502.14819_ . 

- Sun, R., Zang, H., Li, X., and Islam, R. (2024). Learning latent dynamic robust representations for world models. _arXiv preprint arXiv:2405.06263_ . 

- Terver, B., Balestriero, R., Dervishi, M., Fan, D., Garrido, Q., Nagarajan, T., Sinha, K., Zhang, W., Rabbat, M., LeCun, Y., et al. (2026). A lightweight library for energy-based joint-embedding predictive architectures. _arXiv preprint arXiv:2602.03604_ . 

- Tkachev, I. and Abate, A. (2011). On infinite-horizon probabilistic properties and stochastic bisimulation functions. In _2011 50th IEEE Conference on Decision and Control and European Control Conference_ , pages 526–531. IEEE. 

- Tobin, J., Fong, R., Ray, A., Schneider, J., Zaremba, W., and Abbeel, P. (2017). Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pages 23–30. IEEE. 

- Villani, C. et al. (2008). _Optimal transport: old and new_ , volume 338. Springer. 

- Wang, Y., Bounou, O., Zhou, G., Balestriero, R., Rudner, T. G., LeCun, Y., and Ren, M. (2026). Temporal straightening for latent planning. _arXiv preprint arXiv:2603.12231_ . 

- Williams, G., Wagener, N., Goldfain, B., Drews, P., Rehg, J. M., Boots, B., and Theodorou, E. A. (2017). Information theoretic mpc for model-based reinforcement learning. In _2017 IEEE international conference on robotics and automation (ICRA)_ , pages 1714–1721. IEEE. 

- Wu, Z., Zhang, J., Pai, D., Wang, X., Singh, C., Yang, J., Gao, J., and Ma, Y. (2025). Simplifying dino via coding rate regularization. _arXiv preprint arXiv:2502.10385_ . 

- Zhang, A., McAllister, R. T., Calandra, R., Gal, Y., and Levine, S. (2021). Learning invariant representations for reinforcement learning without reconstruction. In _International Conference on Learning Representations_ . 

- Zhou, G., Pan, H., LeCun, Y., and Pinto, L. (2025). DINO-WM: World models on pre-trained visual features enable zero-shot planning. In _International Conference on Machine Learning_ . 

- Zhou, J., Wei, C., Wang, H., Shen, W., Xie, C., Yuille, A., and Kong, T. (2021). ibot: Image bert pre-training with online tokenizer. _arXiv preprint arXiv:2111.07832_ . 

- Zhu, J., Evtimova, K., Chen, Y., Shwartz-Ziv, R., and LeCun, Y. (2023). Variance-covariance regularization improves representation learning. _arXiv preprint arXiv:2306.13292_ . 

15 

## **A Appendix** 

This appendix provides additional details that complement the main text. We expand on the related work discussed in the introduction (Section 1) below. We include specifics on the architecture and implementation of the proposed bisimulation encoder and transition model, further discussion of the PCA-based variance-covariance regularization, and extended descriptions of the experimental setup, including task configurations, domain randomization, and planning details. We also provide the proofs for the generalization bound in Section 3.6. We begin with a detailed discussions on relevant existing works. 

### **A.1 Related Work** 

**Joint embedding predictive architectures (JEPAs).** Joint embedding predictive architectures learn feature representations by predicting future latent states rather than reconstructing observations (Grill et al., 2020; Caron et al., 2021; LeCun, 2022; Assran et al., 2023; Sobal et al., 2025; Balestriero and LeCun, 2025; Maes et al., 2026). Most relevant to our work is DINO-WM (Zhou et al., 2025) that learns latent dynamics directly in the space of pretrained DINOv2 visual features (Oquab et al., 2023), avoiding pixel-level reconstruction. Other recent joint embedding predictive world models include PLDM (Sobal et al., 2025), which trains the encoder from scratch with an offline reward-free objective, and EB-JEPA (Terver et al., 2026), which leverages energy-based objectives. In contrast to these approaches, our method operates on top of frozen pretrained visual features, leveraging their semantic richness without retraining them. However, latent prediction in DINO-WM remains sensitive to slow, control-irrelevant features. We address this limitation by augmenting the predictive objective with a bisimulation encoder to enforce control-relevant invariances. 

**Bisimulation metrics and invariant representations.** Bisimulation provides a principled way of behavioral equivalence in MDPs by quantifying approximate equivalence through reward discrepancies and mismatches in future state distributions for different states under the same policy (Ferns et al., 2011; Abate, 2013). Most relevant to our work is BS-MPC in (Shimizu and Tomizuka, 2025), which incorporates a bisimulation metric loss for model predictive control Kouvaritakis and Cannon (2016); Lenz et al. (2015); Williams et al. (2017). In contrast to (Shimizu and Tomizuka, 2025), we leverage bisimulation metrics to “filter out” control-irrelevant information from a pretrained feature space (e.g., that of DINOv2, SimDINOv2, iBOT). Moreover, we jointly train our prediction model without relying on reward prediction. Distance-aware representation learning methods such as HILP (Park et al., 2024) share the goal of learning metrically structured latent spaces, but are typically applied in the context of goal-conditioned policy learning rather than world-model-based planning on top of frozen visual features. 

**Model-based control with latent world models.** Model-based RL with world models enable planning by rolling out learned dynamics in a compact latent space, which has been effective for high-dimensional tasks (Ha and Schmidhuber, 2018; Hafner et al., 2019, 2020). In robotics, latent dynamics models are commonly paired with sampling-based optimizers for action selection, including the cross-entropy method (CEM), which is widely used for planning with learned world models (Rubinstein and Kroese, 2004; Zhou et al., 2025). Our control stack follows this line, we plan with CEM with the learned latent dynamics, and focus on the representation learning side, i.e., how to learn a latent space that is robust to slow features so that planning remains reliable under visual distribution shifts in test time. Approaches for improving robustness to visual distractors in model-based RL include HRSSM (Sun et al., 2024) and JEDI (Lim et al., 2025), which address distractor robustness via stochastic state models 

16 


Figure 7: Overview of the DINO-Bisim architecture. 

and diffusion-based planning respectively. These methods typically learn representations endto-end from scratch, while our approach adapts frozen pretrained visual features and focuses on suppressing control-irrelevant directions via bisimulation. 

### **A.2 Model Architecture** 

This section provides additional details on the architecture of the proposed joint-embedding predictive world model with bisimulation encoder. 

#### **A.2.1 Overview** 

The DINO-Bisim model takes visual observations, proprioceptive inputs, and actions at the current timestep and predicts the next bisimulation latent state, along with an optional reward prediction (see Figure 7). Visual observations are encoded using a pretrained DINOv2 ViT-S/14 visual encoder Oquab et al. (2023), followed by a bisimulation encoder implemented as an MLP to produce the latent state. Proprioceptive inputs and actions are embedded using lightweight 1D convolutional encoders. The resulting embeddings are concatenated and processed by a 6- layer transformer to predict the next bisimulation latent state. A separate reward MLP predicts the reward from the latent state, however, this component is not used in our experiments, as discussed in Section 4 and throughout the main text. 

#### **A.2.2 Bisimulation Memory Buffer (Replay Buffer)** 

Recalling the definition of the bisimulation metric introduced in Section 2.2 and in Castro (2020), the corresponding loss involves computing differences between selected pairs of states. Since a single training iteration can only leverage the current batch of 20 states, we introduce a bisimulation memory buffer that stores up to 1000 previously generated states, also following Zhang et al. (2021). This buffer allows comparisons with a larger and more diverse set of past states, thereby improving the stability and effectiveness of the bisimulation representation learning. 

#### **A.2.3 Patch design in Bisimulation Model** 

**Why Patch-based Design?** The bisimulation model adopts a patch-based design, in which visual inputs are partitioned into spatial patches and each patch is encoded independently. This 

17 

Table 3: Shared hyperparameters for DINOBisim training. 

Table 4: Bisimulation encoder hyperparameters. 

|**Name**|**Value**|**Name**|**Value**|
|---|---|---|---|
|Image size|224|Bisimulation memory buffer size|1000|
|Optimizer|AdamW|Bisimulation state comparison size|200|
|Decoder learning rate|3e_−_4|Action dim.|10|
|Predictor learning rate|1e_−_5|Num patches|196|
|Action encoder learning rate|1e_−_4|Latent dim.|32|
|Bisimulation learning rate|5e_−_7|Patch dim.|32|
|Action embedding dim.|10|Patch embedding dim.|384|
|Proprio embedding dim.|10|||
|Epochs|50|||
|Batch size|20|||


design builds upon the bisimulation encoder in Shimizu and Tomizuka (2025) and naturally aligns with the output format of DINOv2 and other patch-based visual encoders. Beyond architectural compatibility, the patch-based formulation substantially reduces the number of trainable parameters, leading to a more compact and efficient model while empirically improving performance. 

More concretely, an example architecture using the hyperparameters in Table 4 is illustrated in Figure 4. Rather than flattening a feature map of size 14 _×_ 14 _×_ 384 into a 75264-dimensional vector as input to the first layer, the patch-based bisimulation encoder performs 196 parallel forward passes using a shared MLP whose input dimension is 384. As a result, the number of parameters in the first layer is reduced from (75 _,_ 264 _×_ 256) + 256 = 19 _,_ 267 _,_ 840 to (384 _×_ 256) + 256 = 98 _,_ 560, where 256 is the hidden layer dimension, with only negligible additional overhead from the spatial embedding parameters. 

**Latent Space Dimensionality Comparison.** DINO-WM operates on patch-based visual representations produced by DINOv2, consisting of 196 patches with 384-dimensional embeddings each, resulting in a latent representation of size 196 _×_ 384. In contrast, our patchbased bisimulation encoder preserves the same spatial structure but maps each patch to a low-dimensional latent embedding. This yields a representation of size 196 _×_ 32. Consequently, our model operates in a latent space that is more than 10 _×_ smaller than that of DINO-WM, while maintaining improved robustness to slow, task-irrelevant features. 

#### **A.2.4 Hyperparameters** 

We now summarizes the hyperparameters used in our experiments in Tables 3 and 4. 

We list below the main hyperparameters used by the bisimulation encoder and transition model. These parameters control the dimensionality of the latent representation, the size of the comparison set used for bisimulation representation learning, and the dimensionality of visual and action embeddings. 

**Bisimulation Memory Buffer Size and Comparison Size.** The capacity of the bisimulation memory buffer and the number of stored latent states used for pairwise comparisons when computing the bisimulation loss. 

**Action Dimension (** `action` ~~`d`~~ `im` **).** The dimensionality of the encoded action representation, used as input to the reward predictor that is not in use for our experiments. 

18 

**Number of Patches (** `num` ~~`p`~~ `atches` **).** The number of spatial patches output by the bisimulation encoder, matching the patch decomposition of the visual pretrained encoder. 

**Latent Dimension (** `latent` ~~`d`~~ `im` **).** The dimensionality of the bisimulation latent space for each patch. 

**Patch Dimension (** `patch` ~~`d`~~ `im` **).** The dimensionality of each patch embedding produced by the bisimulation encoder; in our implementation, this is set equal to `latent` ~~`d`~~ `im` . 

**Patch Embedding Dimension (** `patch` ~~`e`~~ `mb` ~~`d`~~ `im` **).** The dimensionality of the input patch embeddings provided by the pretrained visual encoder, matching the output dimension of DINOv2. 

### **A.3 PCA-based Variance Covariance Regularization** 

We now discuss the implementation of our PCA-based variance covariance regularization. Let _Wc_ ≜ �( _w_ 1 _− w_ ¯)<sup>_⊤_</sup> _. . ._ ( _wB − w_ ¯)<sup>_⊤_�</sup> _,_ be the matrix with centered embeddings in the batch of size _B_ , where _w_ ¯ is the average. We define the empirical covariance Σ ≜ _WBc_<sup>_⊤_</sup> _−_<sup>_W_</sup> 1<sup>_c_,</sup> and further compute its eigendecomposition as Σ = _U_ Λ _U_<sup>_⊤_</sup> , where Λ = diag( _λ_ 1 _, . . . , λdw_ ) with eigenvalues sorted in descending order ( _λ_ 1 _≥ λ_ 2 _≥· · · ≥ λdw ≥_ 0; non-negativity is guaranteed since Σ is a positive semi-definite empirical covariance matrix). We extract the PCA coordinates _w_ ˜ _b_ = _U_<sup>_⊤_</sup> ( _wb − w_ ¯), and let _W_<sup>˜</sup> _c_ be the batch matrix with rows _w_ ˜ _b_<sup>_⊤_.</sup> 

To construct the PCA-based VC-Reg loss, we only enforce the variance floor on the tail PCs, namely indices _i ∈{i_ 0 _, . . . , dw}_ , where _i_ 0 is a cutoff index (e.g., _i_ 0 = 2). Let _κi_ ≜ _σ_ min _−_<sup>_~~√~~_</sup> _λi_ + _ϵ_ and write the variance term 


where _ϵ >_ 0 is a small constant for numerical stability (ensuring the square root is well-defined even for near-zero eigenvalues) and _σ_ min denotes a minimum standard deviation. On the other hand, we regularize cross-covariances as 


where Σ<sup>˜</sup> _pq_ denotes the ( _p, q_ ) entry of the covariance in PCs coordinates, namely, the covariance matrix Σ.<sup>˜</sup> Therefore, we combine the two PCA-based terms 


with weights _α_ v _, α_ c _>_ 0, to the predictive loss (2). 

**Setup.** Our experiments use DINOv2, SimDINOv2 and iBOT as pretrained visual encoder, which encode background appearance along the dominant principal components (see Section 3.3). As noted in the DINOv2 paper Oquab et al. (2023), background information can be attenuated by thresholding the first principal component. Consistent with this observation and our illustration in Figures 5 and 9, we make the preliminary assessment that task-irrelevant appearance factors predominantly align with the first principal component direction in the latent feature space. 

**Method.** The bisimulation encoder is initialized with random parameters and is first trained using the standard VICReg objective for a small number of epochs to stabilize representation 

19 


Figure 8: First two principal components (PCs) of three distinct states (colors) observed under three different backgrounds (marker shapes) for the PointMaze task. The goal of the bisimulation encoder is to map identical states across backgrounds to nearby latent representations. **Left.** DINOv2 embeddings _zt_ = _fθ_ ( _ot_ ) show strong separation along the first PC for identical states under different backgrounds, indicating that background variation dominates the leading principal direction. **Middle.** Bisimulation embeddings _wt_ = _hη_ ( _zt_ ) after 50 epochs with standard VICReg still exhibit separation along the first PC, preserving background-dependent variation. **Right.** Bisimulation embeddings after 90 epochs with PCA-based VICReg (activated at epoch 50) show improved clustering of identical states across backgrounds, consistent with suppression of task-irrelevant variation. 

learning. We then perform a one-time principal component analysis to identify the dominant direction associated with task-irrelevant variation. After a number of warm-up epochs, we replace the standard VICReg loss with the proposed PCA-based VICReg objective, which helps to suppresses variance along the identified principal component directions. 

An example training run with a vectorized bisimulation latent representation of dimension 196 _×_ 32 (corresponding to the number of patches and per-patch latent dimensionality), where PCA-based VICReg is enabled after _k_ = 50 epochs, is shown in Figure 8. 

**Result.** While this staged regularization approach improves the stability of invariant representation learning, we hypothesize that a tighter integration of PCA-based regularization throughout training and planning, rather than a discrete loss swap, could further enhance invariance. Exploring such joint objectives is an interesting direction for future work. 

### **A.4 Additional Information on the Navigation Task** 

**Task Description.** This section provides additional details on the simple navigation task used in our experiments, complementing the high-level description in the main text. PointMaze Fu et al. (2020) is a force-actuated 2-DoF navigation environment in which a ball moves in the Cartesian _x_ – _y_ plane with the objective of reaching a target location. The agent observes proprioceptive state information and evolves under continuous dynamics that capture velocity, acceleration, and inertia. For a fair comparison, we train all models on 2000 fully random trajectories, matching the data setup in Zhou et al. (2025). See Figure 10 for a sequence of frames that illustrates the planning from an initial state to a goal state. 

Fig. 12 and Fig. 13 and shows representative MPC rollouts on PointMaze under six test-time 

20 


Figure 9: First twp principal components (PC1 and PC2) of latent embeddings produced by DINOv2, SimDINOv2, and iBOT for a PointMaze observation. In all cases, PC1 captures a large percentage of the total variance that predominantly encodes background and layout information rather than control-relevant features. 


Figure 10: PointMaze task, from leftmost the initial state to the rightmost the goal state 

visual conditions (columns) over six replanning steps (rows). DINO-WM (top/bottom-left pairs) fails under strong appearance shift while DINO-Bisim (paired success rows) reaches the goal from the same start and target. For this additional illustration we have also considered different background changes and more “aggressive” distractors compared to those in the discussed in the main body of the paper. 

### **A.5 Additional Information on the Manipulation Task** 

**Task Description.** PushT environment consists of a pusher agent interacting with a T-shaped object. Starting from a randomly initialized configuration, the agent must drive both itself and the T-block to a known feasible target state, requiring both entities to reach their respective target positions (see Figure 11). Unlike prior setups, the fixed green T does not indicate the target pose of the object and instead serves solely as a visual anchor for reference. We train the model on 18500 samples exact same with Zhou et al. (2025), for the best performance comparison. 

**Raw success scores.** Fig. 14 and Fig. 15 and shows representative MPC rollouts on PointMaze under six test-time visual conditions (columns) over six replanning steps (rows). DINO-WM (top/bottom-left pairs) fails under strong appearance shift while DINO-Bisim (paired success rows) reaches the goal from the same start and target. 

21 


Figure 11: Push T Task, from leftmost the start state to the rightmost the goal state 


Figure 12: **PointMaze planning failure (DINO-WM).** Six MPC steps (rows) under six visual conditions (columns: NC, SC, C, LC, LCG, D). Markers: start (orange), goal (green); red line: rollout path. Same init/goal as Fig. 13. DINO-WM fails to reach the goal, especially under LC/LCG. 

22 


Figure 13: **PointMaze planning success (DINO-Bisim).** Same layout and shared episode as Fig. 12. Bisimulation-aligned representations yield a goal-reaching trajectory across all six appearance conditions. 

23 


Figure 14: **PushT planning failure (DINO-WM).** Six MPC steps _×_ six visual conditions; start/goal markers and executed path overlaid. Matched init/goal with Fig. 15. WM misaligns the block with the target pose under shifted backgrounds. 

24 


Figure 15: **PushT planning success (DINO-Bisim).** Same episode as Fig. 14. DINO-Bisim completes the push despite lighting/color perturbations at test time. 

25 


Figure 16: Examples of domain-randomized visual observations for the PointMaze task. During training, background appearance is randomized across trajectories using color shifts, gradient backgrounds, and fixed distractors (i.e., the dot outside the maze) while the underlying maze layout and transition dynamics remain unchanged. 

### **A.6 Planning** 

We optimize the action sequence using CEM. At each step, CEM samples multiple candidate action sequences, rolls them out using the learned model, selects the sequences with lowest cost (3), and updates the sampling distribution accordingly. The first action of the optimized sequence is played, and the process repeats with a receding horizon. 

Although gradient-based planning methods have recently been proposed and validated in (Parthasarathy et al., 2025) for DINO-WM, we focus on CEM for a fair comparison with the planning approach used in DINO-WM Zhou et al. (2025). 

### **A.7 Domain Randomization for the PointMaze Task** 

To evaluate robustness through data augmentation, we apply domain randomization to the PointMaze task by modifying the visual appearance of the environment during training. In particular, 40% of the training data are rendered with randomized visual backgrounds, while the remaining trajectories retain the default appearance. The randomization includes background color changes and gradient-based background modifications, as illustrated in Figure 16. 

To avoid introducing spurious temporal artifacts that could make the transition dynamics learning harder, the randomized background is kept fixed within each trajectory but varies across different trajectories. Importantly, these visual modifications do not alter the underlying environment dynamics, agent behavior, or goal locations, ensuring that domain randomization affects only task-irrelevant visual features. 

### **A.8 Reward-aware Bisimulation Encoder: Training Metrics** 

Let us now analyze the training dynamics of the reward-aware bisimulation encoder to assess the contribution of the reward prediction term relative to the transition-based objectives. Following prior work on bisimulation-based MPC Shimizu and Tomizuka (2025), we include an auxiliary reward predictor during training, although it is not used for training nor planning in our experiments. 

26 


Figure 17: Training losses value versus the epochs. Ground-truth reward distance is shown only as a diagnostic and is not used during training. 

Figure 17 reports the evolution of the main loss components throughout training. We observe that the reward prediction loss rapidly converges to near zero early in training and remains negligible afterwards. This indicates that, for the navigation task considered, reward prediction provides little additional learning signal beyond what is already captured by the transition dynamics. As a result, the reward term has a negligible influence on the learned latent representation. 

On the other hand, the transition losses and representation regularization terms (including the VICReg and bisimulation objectives) remain active throughout training and dominate the optimization process. These components are responsible for making the latent space to preserve control-relevant dynamics while suppressing task-irrelevant visual features. This empirical observation supports the design choice adopted in the main experiments, where we drop the reward prediction term and rely only on transition-based bisimulation to enforce invariance. 

### **A.9 Moving Distractors** 

To evaluate robustness to dynamic but task-irrelevant visual variations, we consider two moving distractors in the PointMaze task. As illustrated in Figure 18, we augment the environment with colored distractor objects (yellow and magenta dots) that move continuously within the maze while remaining decoupled from the agent dynamics and task objectives. 

The distractors introduce persistent motion that can dominate DINO-WM latent dynamics, despite being irrelevant for control. On the other hand our bisimulation-based representation is designed to suppress such task-irrelevant motion by enforcing equivalence between states that exhibit identical on-policy transition behavior. As a result, planning performance remains stable in the presence of moving distractors, whereas DINO-WM tend to drop in performance. 

### **A.10 Ablation (planning horizon)** 

Table 5 evaluates the effect of the MPC planning horizon on PointMaze under NC, SC, and C. Increasing the horizon from _T_ = 5 to _T_ = 10 improves the success rate from 0 _._ 78, 0 _._ 80, and 0 _._ 76, respectively, to 0 _._ 88 in all three conditions. Further benefit is also observed at moderate horizons: _T_ = 25 achieves the highest mean success rate across the three conditions (0 _._ 92, compared to 0 _._ 78 at _T_ = 5). However, the improvement is not monotonic, and extending the horizon to _T_ = 50 or _T_ = 100 yields a lower mean success rate of approximately 0 _._ 89. 

27 


Figure 18: Moving distractor setting in PointMaze. Yellow and magenta dots move continuously within the maze, introducing dynamic but task-irrelevant visual variation while preserving the underlying transition dynamics. 

These results suggest that moderate planning horizons improve goal-reaching performance while preserving robustness to the evaluated background changes. 

Table 5: **PointMaze.** Planning-horizon ablation for DINO-Bisim. Absolute success rates under the native background (NC) and background changes (SC and C). Higher is better. 

|**Horizon**|**NC**|**SC**|**C**|
|---|---|---|---|
|5|0.78|0.80|0.76|
|10|0.88|0.88|0.88|
|15|0.94|0.88|0.92|
|20|0.88|0.92|0.90|
|25|0.94|0.94|0.88|
|50|0.84|0.90|0.92|
|100|0.86|0.92|0.88|


### **A.11 Reward-Free Generalization Bound: Proof of Theorem 3.1** 

We first provide an auxiliary lemma regarding the 1-Wasserstein distance which we use in the proof of Theorem 3.1. 

**Lemma A.1** (Kantorovich-Rubinstein duality Villani et al. (2008)) **.** _Let µ, and ν be two probability measures on the metric space_ (Ω _, dπ_ ) _, then_ 


We will later invoke the auxiliary result above in the proofs of Theorem 3.1. To make this step explicit, we first show how the Kantorovich-Rubinstein duality implies a Lipschitz-based bound on differences of expectations. Let _µ_ ≜ _Pπ_ ( _· | z_ ) _,_ and _ν_ ≜ _Pπ_ ( _· | z_<sup>_′_</sup> ) _,_ be two probability measures on the metric space (Ω _, dπ_ ), and define a scalar-valued function _s_ (˜ _z_ ) on the latent space _z_ . Assuming that _s_ ( _z_ ) is a _L_ -Lipschitz with respect to _dπ_ , i.e., 


By Kantorovich-Rubinstein duality (Lemma A.1), we have 


28 

where _∥f ∥L ≤_ 1 denotes that _f_ is 1-Lipschitz with respect to _dπ_ . Now define the rescaled function _l_ ( _·_ ) ≜ _L_<sup><u>1</u></sup><sup>_s_(</sup><sup>_·_)</sup><sup>_._Then</sup><sup>_l_is1-Lipschitzsince,forall</sup><sup>_u, v∈_Ω,wehave</sup> 


Thus _l_ is feasible for the supremum in (6), implying that 


Rearranging the terms, we obtain 


**Proof of Theorem 3.1:** We begin the proof by first noticing that the goal-reaching cost used for planning is Lipschitz on the bounded set of bisimulation latent states, i.e., _{w_ : _∥w∥_ 2 _≤ Hw}_ . Indeed, for any _w, w_<sup>_′_</sup> with _∥w∥_ 2 _, ∥w_<sup>_′_</sup> _∥_ 2 _, ∥wg∥_ 2 _≤ Hw_ , we have the following expression 


so _c_ ( _w_ ) is 4 _Hw_ -Lipschitz. 

We further write the recursion 


where we assume that _J_ 0<sup>_π_(</sup><sup>_z_)</sup><sup>_≡_0.</sup> 

We then prove by induction that _JT_<sup>_π_is</sup><sup>_LT_-Lipschitzwithrespectto</sup><sup>_dπ_(</sup><sup>_z, z′_),with</sup><sup>_LT_≜</sup> 8 _HwT_ , which implies (5). For _T_ = 0 it holds trivially. Assume it holds for _T −_ 1. Then for any _z, z_<sup>_′_</sup> , 


Note that the first term is bounded by the quantity 4 _Hw∥hη_ ( _z_ ) _− hη_ ( _z_<sup>_′_</sup> ) _∥_ 2. On the other hand, for the second term, since _JT_<sup>_π_</sup> _−_ 1<sup>is</sup><sup>_LT−_1-Lipschitzwithrespectto</sup><sup>_dπ_(</sup><sup>_z, z′_),wecanuse</sup> Kantorovich-Rubinstein duality to bound ��E _z_ ˜ _∼Pπ_ ( _·|z_ ) _JTπ−_ 1<sup>(˜</sup><sup>_z_)</sup><sup>_−_E</sup><sup>_z_˜</sup><sup>_′∼P_</sup> _π_<sup>(</sup><sup>_·|z′_)</sup><sup>_J_</sup> _T_<sup>_π_</sup> _−_ 1<sup>(˜</sup><sup>_z′_)</sup> �� with the expression _LT −_ 1 _W_ 1 ( _Pπ_ ( _· | z_ ) _, Pπ_ ( _· | z_<sup>_′_</sup> )) _,_ i.e., by using (7). 

Using the definition of the bisimulation metric, with the reward term dropped, we have _W_ 1 ( _Pπ_ ( _· | z_ ) _, Pπ_ ( _· | z_<sup>_′_</sup> )) = _γ_<sup>_−_1</sup> _dπ_ ( _z, z_<sup>_′_</sup> ). Therefore, we obtain 


As we assume that _∥hη_ ( _z_ ) _− hη_ ( _z_<sup>_′_</sup> ) _∥_ 2 _≤ dπ_ ( _z, z_<sup>_′_</sup> ) + _ε_ , then 


Unrolling the recursion and assuming that _ϵ_ is sufficiently small, i.e., _ϵ ≤ dπ_ ( _z, z_<sup>_′_</sup> ), then _LT_ ≜ 8 _HwT_ , which implies the bound as stated in Theorem 3.1. 

29 

