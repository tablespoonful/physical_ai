---
title: "VGAS: Value-Guided Action-Chunk Selection for Few-Shot Vision-Language-Action Adaptation"
date: "2026-02-07"
authors: "Changhua Xu; En Yu; Junyu Xuan; Jie Lu"
url: https://arxiv.org/abs/2602.07399
pdf: https://arxiv.org/pdf/2602.07399
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.07399)** / [論文ページ](https://arxiv.org/abs/2602.07399)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **VGAS: Value-Guided Action-Chunk Selection for Few-Shot Vision-Language-Action Adaptation** 

**Changhua Xu** , **En Yu** , **Junyu Xuan** , **Jie Lu** 

Australian Artificial Intelligence Institute (AAII), University of Technology Sydney, Australia changhua.xu@student.uts.edu.au; _{_ en.yu-1, junyu.xuan, jie.lu _}_ @uts.edu.au 

## **Abstract** 

Vision–Language–Action (VLA) models bridge multimodal reasoning with physical control, but adapting them to new tasks with scarce demonstrations remains unreliable. While fine-tuned VLA policies often produce semantically plausible trajectories, failures often arise from unresolved geometric ambiguities, where near-miss actions lead to divergent execution outcomes under limited supervision. We study few-shot VLA adaptation from a _generation–selection_ perspective and propose a novel framework **VGAS** ( **V** alue- **G** uided **A** ction-chunk **S** election). It performs inferencetime best-of- _N_ selection to identify action chunks that are both semantically faithful and geometrically precise. Specifically, **VGAS** employs a finetuned VLA as a high-recall proposal generator and introduces the Q-Chunk-Former, a geometrically grounded Transformer critic to resolve fine-grained geometric ambiguities. In addition, we propose _Explicit Geometric Regularization_ (EGR), which shapes a discriminative value landscape to preserve action ranking resolution among near-miss candidates while mitigating value instability under scarce supervision. Experiments and theoretical analysis demonstrate that **VGAS** consistently improves success rates and robustness under limited demonstrations and distribution shifts. Our code is available at https://github.com/Jyugo-15/VGAS. 

## **1 Introduction** 

Vision-Language-Action (VLA) models have emerged as a transformative paradigm for embodied AI, bridging multimodal reasoning with physical control [Brohan _et al._ , 2022; Zitkovich _et al._ , 2023; He _et al._ , 2026]. By pretraining on vast robotic datasets, these generalist policies learn to map complex visual observations and linguistic instructions directly into executable actions [Black _et al._ , 2024; Kim _et al._ , 2024; Team _et al._ , 2024; Intelligence _et al._ , 2025]. However, the reliability of VLAs in downstream applications remains heavily bottlenecked by the prevailing Supervised Fine-Tuning (SFT) paradigm [Kim _et al._ , 2025; Zhang _et al._ , 2025a]. SFT-based adaptation demands a high volume of expert demonstrations 


Figure 1: Illustration of near-miss action distribution under 5-shot VLA fine-tuning. 

to bridge the gap between generalist priors and task-specific requirements. This is often challenging in real-world environments where high-quality robotic data collection is costly, unscalable, and prone to out-of-distribution (OOD) uncertainties [Dass _et al._ , 2022; Xin _et al._ , 2024; Sapkota _et al._ , 2025; Yu _et al._ , 2026b]. Consequently, under data-scarce regimes, VLA policies often exhibit brittle performance, failing to generalize across even minor distribution shifts [Liu _et al._ , 2025; Li _et al._ , 2025a; Yu _et al._ , 2026a; Tan _et al._ , ; Guo _et al._ , 2025]. 

To study this data-scarce regime, we simulate a realistic few-shot adaptation setting by fine-tuning a pretrained VLA policy with only five demonstrations per task, and evaluating it on held-out demonstrations with different initial spatial configurations (e.g., object positions). As shown in Figure 1, the fine-tuned policy generally preserves the task semantics, producing actions toward the correct object. However, due to the limited state–action coverage, even slight variations in the initial spatial configuration can make the policy’s action predictions less concentrated, yielding dispersed near-miss predictions around the ground-truth actions. Although semantically reasonable, these predictions are often geometrically imprecise and can cause failures such as inaccurate grasps, end-effector pose deviations, or joint-angle overshoot [Kumar _et al._ , 2022; Zhao _et al._ , 2023]. This suggests that few-shot VLA adaptation is primarily limited by geometric precision under sparse supervision, rather than semantic understanding alone. Motivated by this, we reformulate adaptation as a value-guided selection problem: instead of requiring a gen- 

erative policy to jointly acquire semantic reasoning and finegrained geometric control end-to-end, we decouple adaptation into high-recall proposal generation and high-precision value-based selection, prioritizing candidates with the highest likelihood of long-horizon success. 

Offline Reinforcement Learning (ORL) provides a natural framework for this selection objective, as it learns an outcome-aware critic that maps long-horizon success into a scalar value signal [Sutton _et al._ , 1998]—perfectly suited for ranking candidate proposals [Ghasemipour _et al._ , 2021; Janner _et al._ , 2022; Luo _et al._ , ]. However, applying existing ORL methodologies to modern VLA policies exposes two fundamental limitations: _1) Structural and observational mismatch:_ Standard RL assumes per-step atomic actions, whereas modern VLAs output temporally extended action chunks, inducing an SMDP structure that complicates value learning and temporal credit assignment [Sutton _et al._ , 1999]. Moreover, most offline RL is evaluated with compact, near-Markovian state inputs; in contrast, VLA relies on high-dimensional vision–language observations with geometric grounding, making value estimation substantially harder and comparatively under-explored [Fu _et al._ , 2020; Lu _et al._ , 2022]. _2) Ranking resolution vs. conservatism:_ Offline RL often controls extrapolation to low-support actions via conservative objectives or behavior-regularized extraction [Kumar _et al._ , 2020; Kostrikov _et al._ , 2021]. In fewshot sparse-reward settings, however, such regularization can compress value gaps among proposal-supported near-miss candidates, yielding low-contrast gradients and weakening inference-time Best-of- _N_ selection [Lyu _et al._ , 2022]. These limitations raise two major research questions: **_RQ1._** _What critic architecture can robustly ground high-dimensional VLA observations into precise value estimates for temporally extended action chunks?_ and **_RQ2._** _How can a value function be trained under scarce demonstrations to maintain high ranking resolution among near-miss action chunks?_ 

To address these questions, we propose **VGAS** ( **V** alue- **G** uided **A** ction-chunk **S** election) for VLA adaptation via generation–selection decoupling. For **_RQ1_** , we introduce Q-Chunk-Former, a geometrically grounded critic architecture built on a Transformer backbone. By leveraging the Transformer’s sequence modeling capability, our design naturally captures temporal dependencies within action chunks. Crucially, our architecture preserves fine-grained, token-level features, allowing attention to explicitly focus on geometric cues that are critical for precise value estimation. For **_RQ2_** , we propose a hybrid offline RL objective that _anchors_ temporal consistency via a proposal-constrained Bellman backup, augmented by Explicit Geometric Regularization (EGR). Unlike traditional conservative methods that indiscriminately penalize out-of-distribution actions, EGR injects dense geometric supervision, shaping the value landscape into a smooth funnel anchored at expert demonstrations. This allows the critic to maintain high ranking resolution among near-miss candidates even under scarce supervision. Our contributions are summarized as follows: 

- We reformulate few-shot VLA adaptation as a valueguided selection problem and propose the novel **VGAS** method, shifting the paradigm from likelihood-based 

generation to outcome-aware ranking. 

- We propose Q-Chunk-Former, which enables precise geometric grounding for action-chunk evaluation. We introduce EGR, a regularization technique that injects dense geometric priors into offline RL to maintain high ranking resolution under data-scarce regimes. 

- We provide theoretical guarantees for the convergence of our chunk-level value operator and demonstrate through extensive experiments on the LIBERO benchmark that VGAS consistently outperforms SFT and standard ORL baselines, particularly in terms of success rate and robustness under distribution shifts. 

## **2 Preliminary** 

**Offline Reinforcement Learning.** We consider a Markov Decision Process (MDP) defined by _M_ = ( _S, A, P, r, ρ, γ_ ), where _s ∈S_ , _a ∈A_ , _P_ ( _s_<sup>_′_</sup> _| s, a_ ) is the transition kernel, _r_ ( _s, a_ ) _∈_ R is the reward function, _ρ_ 0 _∈_ ∆( _S_ ) is the initialstate distribution, and _γ ∈_ [0 _,_ 1) is the discount factor. The objective is to learn a policy _π_ maximizing the expected discounted return _J_ ( _π_ ) = E _π_ �� _t≥_ 0<sup>_γtr_(</sup><sup>_st, at_)</sup> �. 

Value-based methods estimate the optimal action-value function _Q_<sup>_⋆_</sup> as the fixed point of the Bellman optimality operator [Fujimoto _et al._ , 2019; Levine _et al._ , 2020]: 


In offline RL, the agent learns from a fixed dataset _D_ collected by a behavior policy _πβ_ , without additional environment interaction [Bacchiocchi _et al._ , 2024]. A key challenge is extrapolation error [Zhang and Tan, 2023]: the maximization over _a_<sup>_′_</sup> may select actions outside the data support, leading to overestimation and instability. Many offline RL methods [Shin and Kim, 2023] mitigate this via conservative regularization [Kumar _et al._ , 2020], which discourages high values on out-of-distribution actions. 

**Action Chunking in VLAs.** Modern VLAs condition on = multimodal inputs, which we denote by the state _st_ ( _It, Lt, pt_ ), comprising visual tokens _It_ , language instruction _Lt_ , and robot proprioception _pt_ [Zitkovich _et al._ , 2023]. With a slight abuse of notation, we treat this policy input as the MDP state. Instead of per-step control, these models often output a temporally extended _action chunk_ with horizon _h_ : 


**Few-shot VLA Adaptation Objective.** Given a few-shot expert dataset _D_ = _{τi}_<sup>_K_</sup> _i_ =1<sup>,wefirstobtainatask-aligned</sup> base chunk policy _πµ_ (A _| s_ ), for example via SFT on _D_ . In this regime, SFT can capture task semantics yet may struggle to resolve fine-grained geometric ambiguities. We therefore treat _πµ_ as a high-recall proposal distribution and assume non-trivial local support around each demonstrated chunk: 


for some _ε >_ 0 and _p_ 0 _>_ 0. Intuitively, _p_ 0 ensures the proposal covers valid near-miss candidates. Our goal is to improve upon _πµ_ by learning an offline-adapted chunk policy 


Figure 2: The overall framework of **VGAS** . **Generation:** A fine-tuned VLA policy proposes _N_ candidate action chunks from multimodal inputs. **Selection:** Q-Chunk-Former learns a scoring function _Q_ via the EGR+TD objective. Best-of- _N_ selection defines the induced policy _πµ,Q_<sup>(</sup><sup>_N_)bymaximizingoveradiscriminativevaluelandscapeshapedbyEGR,prioritizingexpert-alignedcandidatesandtherebymitigating</sup> geometric drift. 

within a proposal-constrained class Π _µ_ : 


where Π _µ_ denotes policies supported by (or centered at) the proposal _πµ_ . Under chunked execution, the return is 


where _tk_ = _kh_ denotes the start time of the _k_ -th chunk, A _tk ∼ π_ ( _· | stk_ ) is the action chunk, and _Rh_ ( _stk ,_ A _tk_ ) = � _hj_ =0 _−_ 1<sup>_γj r_(</sup><sup>_st_</sup> _k_<sup>+</sup><sup>_j, at_</sup> _k_<sup>+</sup><sup>_j_)isthediscountedcumulativere-</sup> ward over the chunk. 

## **3 Methodology** 

**Framework Overview. VGAS** reformulates few-shot VLA adaptation as a generate-then-select process. As illustrated in Figure 2, our pipeline decouples the policy into two components: a _high-recall generator_ and a _high-precision critic_ . First, we utilize a supervised fine-tuned (SFT) VLA model as the base policy _πµ_ (A _t | st_ ) to provide a proposal distribution covering plausible action chunks. At inference time, we sample _N_ candidates _{_ A<sup>(</sup> _t_<sup>_i_)</sup><sup>_}N_</sup> _i_ =1<sup>_∼πµ_(</sup><sup>_·|st_)and</sup> employ a learned critic _Qθ_ to execute Best-of- _N_ selection, A<sup>_⋆_</sup> _t_<sup>=arg max</sup><sup>_iQθ_(</sup><sup>_st,_A</sup> _t_<sup>(</sup><sup>_i_)).</sup> This strategy approximates policy improvement within the support of _πµ_ , prioritizing geometric precision without requiring online exploration. 

To realize this selection mechanism effectively, VGAS addresses two core challenges: _representation_ and _optimization_ . First, regarding critic representation (Sec.3.1), we introduce Q-Chunk-Former, a Transformer-based architecture tailored for VLA inputs. To prevent high-dimensional visual tokens 

from overwhelming physical cues, we design a State-Action Fusion (SAF) module that explicitly grounds action chunks in proprioceptive states before multimodal integration. Second, for critic optimization (Sec.3.2), we propose a hybrid learning objective that combines temporal and spatial supervision. We stabilize offline training using a _Proposal-Constrained Chunked Expected-Max_ backup, which enforces temporal consistency across action chunks. We further augment this with _Explicit Geometric Regularization_ (EGR), a dense supervision signal that directly shapes the value landscape based on geometric proximity to expert demonstrations, enabling the critic to reliably distinguish near-miss actions from failures even under sparse task rewards. 

### **3.1 Q-Chunk-Former** 

To optimize the few-shot adaptation objective in Eq. (4), the critic network must accurately estimate the long-horizon value of a temporally extended action chunk A _t_ given state _st_ . This imposes two key requirements, (i) Chunk-level evaluation with temporal structure: the critic must assign a single long-horizon value to an entire action chunk A _t_ for Bestof- _N_ selection (Eq. (9)), while preserving the within-chunk temporal ordering of actions; (ii) Multimodal fusion without geometric collapse: unlike classical critics operating on compact state vectors, VLA conditioning involves heterogeneous inputs such as vision, language, and proprioception, where naive compression can discard geometry-critical cues needed for feasibility-aware value estimation. 

Motivated by token-level multimodal modeling [Marafioti _et al._ , 2025], we introduce a Transformer-based critic. A naive design treats all modalities as a single concatenated token sequence: 


where [ _·_ ] denotes concatenation. However, in practice, the self-attention mechanism tends to be dominated by the abundant visual and linguistic tokens, so the single proprioceptive token _pt_ receives insufficient attention. This is detrimental because value estimation for manipulation requires joint reasoning over the external world context (from _It_ and _Lt_ ) and the internal robot state (embodiment and configuration encoded by _pt_ ). If _pt_ is under-utilized, the critic becomes less sensitive to geometric feasibility, weakening feasibilityaware value estimation. 

To address this, we introduce a lightweight State-Action Fusion (SAF) module that conditions the raw chunk A _t_ on _pt_ prior to mixing with high-dimensional perceptions. The SAF module produces proprioception-grounded action tokens A<sup>_p_</sup> _t_<sup>,</sup> 


where W _a_ and W _p_ are learnable projections mapping inputs to a shared latent space and Wfuse aggregates the concatenated features. This design enforces a high-fidelity interaction between action tokens and the proprioceptive state, ensuring that feasibility cues are embedded directly into the chunk representation. The grounded action tokens A<sup>_p_</sup> _t_<sup>arethenin-</sup> tegrated with the frozen perceptual tokens<sup>1</sup> and a learnable [VALUE] token v via a Transformer decoder, denoted as the Q-Former (QF). Finally, a Value Head (VH) maps the output embedding of v to a scalar Q-value: 


In summary, Q-Chunk-Former comprises SAF, QF, and VH modules. This architecture mitigates attention imbalance and ensures that value estimation is strictly grounded in geometric reality, providing a reliable signal for selection. 

### **3.2 Optimization Objective** 

Our goal is to learn a critic that supports _value-guided selection_ over a fixed proposal distribution. We assume access to a task-adapted base chunk policy _πµ_ (A _| s_ ) that generates semantically plausible action chunks. At inference time, we draw _N_ i.i.d. candidates from _πµ_ and select the best one according to a scoring rule _Q_ : 


Although the maximization in Eq. (9) is deterministic conditioned on the sampled set, proposal sampling induces a stochastic _selection policy_ . We denote this induced policy by _πµ,Q_<sup>(</sup><sup>_N_)(A</sup><sup>_| s_), defined as the distribution of A</sup> _Q_<sup>_⋆_(</sup><sup>_s_).</sup> 

To learn Q from a fixed offline dataset _D_ , we train the critic as a proxy for the long-horizon return of the induced policy _πµ,Q_<sup>(</sup><sup>_N_)in the chunk-induced SMDP. A reliable critic in</sup> the few-shot regime must satisfy two coupled desiderata: (i) **temporal consistency** , i.e., Bellman-style alignment with the expected _max_ return under best-of- _N_ selection over _πµ_ samples; and (ii) **spatial consistency** , i.e., preserving fine-grained 

> 1Perceptual tokens _It_ and _Lt_ are extracted from the pre-trained VLM encoder of the base policy to ensure feature alignment and computational efficiency. 

geometric ranking among near-miss proposals. We instantiate these principles with the following hybrid objective: 


**Temporal Consistency.** The primary goal of _L_ TD is to align critic learning with our inference-time execution, i.e., to learn the value function induced by Best-of- _N_ selection, _πµ,Q_<sup>(</sup><sup>_N_).</sup> This alignment requires two ingredients. First, since execution commits to a length- _h_ action chunk, the critic must evaluate the return of an entire chunk. We therefore adopt the chunk-level TD formulation from Q-Chunking [Li _et al._ , 2025b] and learn _Q_ ( _st,_ A _t_ ) that conditions on the full action chunk. 

Second, we must ensure that the _Bellman backup_ matches the same Best-of- _N_ rule used at inference. To this end, inspired by Expected-Max Q-learning (EMaQ) [Ghasemipour _et al._ , 2021], the key insight of EMaQ is to construct a Bellman backup that replaces the standard expectation under a policy with an expected maximization over a set of sampled proposals. By targeting this maximum, the objective ensures that the critic trained with this operator is guaranteed to converge to the value function of the corresponding Bestof- _N_ selection policy _πµ,Q_<sup>(</sup><sup>_N_).Thus,wedefinetheproposal-</sup> constrained _Chunked Expected–Max_ backup operator _Tµ_<sup>_N_as</sup> 


where _Rh_ is the discounted cumulative reward over the chunk and _Ph_ is the _h_ -step transition kernel. The inner maximization corresponds exactly to selecting A<sup>_⋆_</sup> _Q_<sup>(</sup><sup>_s′_)fromEq.(9),</sup> thereby enforcing strict train–test consistency. 

This operator formulation offers rigorous theoretical guarantees for offline adaptation, which we summarize below. **Proposition 1** (Chunked Expected–Max in tabular SMDPs) **.** _In the tabular chunk-induced SMDP, assume bounded rewards and γ_<sup>_h_</sup> _∈_ (0 _,_ 1) _. Then Tµ_<sup>_N_</sup> _in Eq._ (11) _is a γ_<sup>_h_</sup> _- contraction under ∥· ∥∞ and has a unique fixed point Q_<sup>_N_</sup> _µ_<sup>_._</sup> _Let πµ_<sup>(</sup><sup>_N_)</sup> := _πµ,Q_<sup>(</sup><sup>_N_)</sup><sup>_N_</sup> _µ_<sup>_betheinducedBest-of-Npolicy.Then_</sup> _Q_<sup>_N_</sup> _µ_<sup>=</sup><sup>_Qπ_</sup> _µ_<sup>(</sup><sup>_N_)</sup> _. Monotonicity in N and the N →∞ limit are given in Prop. 3 and Thm. 2 (App. B)._ 

Proposition 1 shows that the proposed backup is welldefined in the tabular induced SMDP and that its unique fixed point corresponds exactly to the value function of the induced Best-of- _N_ selection policy. A detailed proof of these properties in the tabular SMDP setting is provided in Appendix B.1. Based on this operator, we instantiate the final temporaldifference loss with a standard target network _Qθ_ ¯ for stability: 


Here, the proposals _{_ A<sup>_′_</sup> _t_<sup>_i_</sup> + _h_<sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>aresampledfromthe</sup> frozen proposal distribution _πµ_ ( _· | st_ + _h_ ) at the next decision state. This loss provides a stable, proposal-constrained 

temporal anchor for our critic, paving the way for the spatial regularization described next. 

**Spatial Consistency.** While the proposal-constrained TD loss provides a stable temporal anchor, offline critic learning remains vulnerable to extrapolation error, where OOD (off-demo) candidates deviating from the training data distribution receive spuriously high values. Standard conservative methods, such as CQL [Kumar _et al._ , 2020], mitigate this by indiscriminately suppressing values for all low-support actions. However, in the few-shot regime, this uniform penalty is overly aggressive, because it compresses the value dynamic range among proposal-supported candidates and reduces the fine-grained ranking resolution needed to distinguish plausible near-miss candidates from catastrophic failures. This value collapse directly undermines inference-time Best-of- _N_ selection. 

To address this, we introduce _Explicit Geometric Regularization (EGR)_ . Instead of uniformly suppressing off-demo actions, EGR serves as a structural regularizer. During training, we regularize the critic with off-demo candidates sampled from _ρ_ ( _· | st_ ), a proposal-centered mixture detailed in Appendix D.1. At inference time, Best-of- _N_ selects only among proposal samples from _πµ_ ( _· | st_ ). Accordingly, EGR targets two desiderata: ( **i** ) _TD-Anchored Calibration:_ anchor the value scale to the TD target _yt_ to _mitigate_ overestimation on off-demo candidates; ( **ii** ) _Geometric Discriminability:_ within the inference-time proposal set, preserve a graded preference for geometric proximity, providing a smooth signal to separate recoverable near-misses from divergence. 

We formalize EGR as the following weighted combination of _Anchoring_ and _Ranking_ losses. 


where _η ≥_ 0 balances the _absolute scale_ (Anchoring) and the _local ordering_ (Ranking). 

_a. Geometric anchoring (L_ anchor _)._ For any off-demo action chunk A<sup>ˆ</sup> _t ∼ ρ_ ( _· | st_ ), we define 


where sg( _·_ ) stops gradients and _yt_ is the TD target from Eq. (12). Crucially, we do not posit Euclidean distance as a global ground-truth metric; rather, we employ this surface as a _structural inductive bias_ to shape the value landscape in regions where task supervision is absent. In our setting, we employ a weighted metric _∥_ A<sup>ˆ</sup> _t −_ A _t∥_<sup>2</sup> _W_<sup>to prioritize crit-</sup> ical kinematic dimensions (e.g., end-effector position) within the normalized control space. This serves as a robust local proxy for geometric proximity: under smooth dynamics, small weighted action deviations tend to induce small shorthorizon trajectory deviations. (See Appendix D.3 for details). 

To satisfy TD-anchored calibration, we align the critic’s estimates on candidate chunks with the reference surface: 


where _ℓ_ ( _·, ·_ ) is the squared error. 

_b. Geometric ranking (L_ rank _)._ While anchoring constrains the absolute scale, it does not guarantee robust _local_ discrimination. To enforce geometric discriminability, we introduce 

a pairwise ranking loss. For any pair (A<sup>ˆ</sup><sup>_i_</sup> _t_<sup>_,_ˆA</sup> _t_<sup>_j_)</sup><sup>_∼ρ_(</sup><sup>_·|st_),</sup> define squared distances to the expert: 


By Eq. (14), the reference differential value satisfies _Y_ ( _st,_ A<sup>ˆ</sup><sup>_i_</sup> _t_<sup>)</sup><sup>_−Y_(</sup><sup>_st,_ˆA</sup><sup>_j_</sup> _t_<sup>) =</sup><sup>_β_(</sup><sup>_dj−di_).We thus encourage the</sup> critic to preserve the same relative differences among candidate chunks: 


**The Closed Loop of Spatio-Temporal Consistency.** The TD and EGR form a mutually reinforcing loop for safe and effective value learning. The Expected-Max TD objective provides a foundational safety layer by inherently operating within the support of the proposal distribution _πµ_ . However, this implicit constraint alone can still be vulnerable to selecting outlier candidates that are accidentally overestimated. EGR reinforces this safety by explicitly shaping the OOD value landscape into a geometric funnel. This structure actively biases the Best-of- _N_ maximization toward candidates that remain close to expert behavior, providing a tighter and more reliable bound on the TD target. This enhanced safety guarantee is formalized by the following proposition: 

**Proposition 2** (Best-of- _N_ bound under an EGR anchoring envelope) **.** _Fix a demonstration pair_ ( _st,_ A _t_ ) _∼D and a candidate distribution πµ_ ( _· | st_ ) _. Define the EGR reference surface Y_ ( _st,_ A<sup>_′_</sup> _t_<sup>) = sg(</sup><sup>_yt_)</sup><sup>_−β∥_A</sup><sup>_′_</sup> _t_<sup>_−_A</sup><sup>_t∥_2</sup> _W_<sup>_(Eq._(14)</sup><sup>_) and the_</sup> anchoring residual _δθ_ ( _st,_ A<sup>_′_</sup> _t_<sup>) :=</sup><sup>_Qθ_(</sup><sup>_st,_A</sup><sup>_′_</sup> _t_<sup>)</sup><sup>_−Y_(</sup><sup>_st,_A</sup><sup>_′_</sup> _t_<sup>)</sup><sup>_.As-_</sup> _sume it is uniformly upper-bounded on the candidate set:_ 


_See Appendix B.2 for the full statement and proof._ 

_TD Anchors and Calibrates EGR._ Conversely, the TD objective provides an essential grounding signal for EGR. The TD target _yt_ sets the absolute scale for the EGR reference surface, preventing the geometric shaping from degenerating into an uncalibrated ranking function. This synergy allows the TD-EGR loop to progressively correct value estimates: TD provides the return-aware scale, while EGR provides the finegrained geometric structure, jointly enabling robust ranking. 

## **4 Experiment** 

In our experiments, we aim to answer the following research questions: _RQ1: Does_ **_VGAS_** _benefit from a Transformerbased chunk critic (Q-Chunk-Former) for modeling finegrained geometric dependencies under multimodal inputs? RQ2: Does Explicit Geometric Regularization (EGR) improve value calibration and ranking over state–action-chunk candidates for Best-of-N selection?_ 

|||LIBER|O-Spatial|LIBER|O-Object|LIBE|RO-Goal|LIBER|O-Long|Av|erage|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Type|Method|SR (_↑_)|Rank (_↓_)|SR (_↑_)|Rank (_↓_)|SR (_↑_)|Rank (_↓_)|SR (_↑_)|Rank (_↓_)|SR (_↑_)|Rank (_↓_)|
|BC-Only|SmolVLA|46_._0|4|45_._8|4|52_._0|3|15_._5|4|39_._8|4|
||QC-M|46.0|4|42.1|5|49.2|5|14.4|5|37.9|5|
|BC + RL|QC-M+CQL|47.8|2|50.3|2|54.2|2|16.5|3|42.2|2|
||QC-T+CQL|47.7|3|50.1|3|51.9|4|17.5|2|41.8|3|
||**VGAS (Ours)**|**56.2**|**1**|**59.0**|**1**|**60.8**|**1**|**20.0**|**1**|**49.0**|**1**|


Table 1: Results on LIBERO (5-shot per task). SR denotes success rate (%). 

### **4.1 Experiment Settings** 

**Benchmark and Architecture.** We evaluate **VGAS** on the widely used simulation benchmark, LIBERO [Liu _et al._ , 2023]. LIBERO is a lifelong learning benchmark focused on language-guided manipulation tasks across diverse object types, task specifications, and environments scenarios. Specifically, it includes 4 suites: Goal, Spatial, Object, and Long. Each suite is designed to evaluate a specific aspect of object manipulation and containing 10 distinct tasks. We use SmolVLA-0.5B [Shukor _et al._ , 2025] as the base chunk policy. We initialize Q-Chunk-Former with the first two decoder layers of the pre-trained SmolVLM2 [Marafioti _et al._ , 2025], keeping the critic’s token space aligned with the policy. Comprehensive architectural details are provided in Appendix D. 

**Baselines.** We compare **VGAS** against baselines covering VLA fine-tuning and offline value-based improvement. **BConly** fine-tunes SmolVLA with behavior cloning. **CQL** [Kumar _et al._ , 2020] serves as a representative conservative offline RL objective and is widely used in VLA settings [Song _et al._ , 2025; Chebotar _et al._ , 2023; Huang _et al._ , 2025; Nakamoto _et al._ , 2025; Chen _et al._ , 2025]. **QC-M** follows Q-Chunking [Li _et al._ , 2025b], training an MLP critic with standard TD learning over action chunks. **QC-M+CQL** augments **QC-M** with the CQL regularizer. Finally, **QC-T+CQL** retains the same objective but replaces the MLP with our Q- Chunk-Former, enabling a controlled comparison of critic architectures under identical conservative constraints. Implementation details are provided in Appendix D.2. 

### **4.2 Main Results** 

Table 1 reports LIBERO success rates. The unregularized Q- Chunking baseline ( **QC-M** ) underperforms BC (37 _._ 9% vs. 39 _._ 8%), reflecting a maximization issue in offline RL. With sparse demonstrations, the critic can overestimate slightly off-demonstration near-miss chunks due to function approximation error, and Best-of- _N_ selection then preferentially picks these overvalued outliers, inducing compounding drift as rollouts enter poorly covered state–action regions [Kumar _et al._ , 2020; Mark _et al._ , 2024]. 

Adding CQL alleviates this failure, improving QC-M from 37 _._ 9% to 42 _._ 2% ( **QC-M+CQL** ), but the gain over BC remains modest. Replacing the MLP with our Transformer backbone yields a similar result (41 _._ 8% for **QC-T+CQL** ), suggesting that indiscriminate conservative suppression com- 

presses value gaps among proposal-supported candidates, leaving Best-of- _N_ with insufficient ranking resolution. 

Finally, **VGAS** achieves 49 _._ 0%, outperforming **QCT+CQL** by a clear margin. Since both methods share the same Q-Chunk-Former backbone, this improvement is primarily attributed to Explicit Geometric Regularization (EGR). See Sec. 4.4 for further comparative analysis. 

### **4.3 Ablation Studies** 

Table 2 isolates the contribution of each component. The dominant gain arises from _Explicit Geometric Regularization_ ( _L_ EGR). Removing _L_ EGR leads to a sharp drop in success rate from 49 _._ 0% to 36 _._ 4%, effectively collapsing performance back to the unregularized QC-M baseline (37 _._ 9%). This regression suggests that, without geometric shaping, the critic is susceptible to a canonical offline RL failure mode: it assigns spuriously high values to off-demo candidates, and the subsequent Best-of- _N_ maximization amplifies these overestimations. These results indicate that EGR plays a dual role: beyond suppressing erroneous high values on offdemo actions, it explicitly structures the local value landscape around demonstrations, preserving the ranking resolution required for reliable Best-of- _N_ selection. In addition, ablating the temporal consistency term ( _L_ TD) reduces performance to 45 _._ 5%, showing that while EGR provides strong spatial guidance, a TD-based anchor remains necessary to stabilize longhorizon value estimates. 

|Variants|Spatial|Object|Goal|LONG|Avg|
|---|---|---|---|---|---|
|w/o SAF|51.8|54.2|56.8|17.4|45.1|
|w/oQCF|53.4|55|55.9|16.8|45.3|
|w/o_L_EGR|42.6|42.3|48.2|12.5|36.4|
|w/o_L_TD|55.2|54.5|56.0|16.4|45.5|
|**VGAS**|56.2|59.0|60.8|20.0|49|


Table 2: Ablation study on LIBERO (success rates (%)). 

Architectural choices prove equally critical. We denote our Transformer-based critic as QCF (Q-Chunk-Former). Replacing QCF with a standard MLP backbone (w/o QCF) yields 45 _._ 3%, validating the necessity of the Transformer’s attention mechanism for modeling complex multimodal dependencies. Notably, ablating the State-Action Fusion mod- 


Figure 3: Visualization of the Proposal-Candidate Value Landscape: CQL vs. EGR (Ours) 


Figure 4: Multi-view Spatial Rollouts of Action Chunks and **VGAS** Selection. Trajectories are reconstructed via temporal integration in orthogonal views. **VGAS** identifies the trajectory aligning with the expert across 3D space. 

ule (w/o SAF) further lowers performance to 45 _._ 1%. This suggests that without explicit grounding, the critic struggles to resolve fine-grained geometric ambiguities amidst highdimensional visual features. 

To assess execution precision, we visualize the spatial rollouts induced by action chunks on held-out task instances. Although these instances remain semantically aligned with the training demonstrations, they contain subtle yet consequential spatial variations. The SFT baseline (blue) exhibits pronounced dispersion, producing a “cloud” of candidates that frequently drifts away from the target. This indicates poor geometric generalization under few-shot supervision: the policy tends to memorize demonstration-specific trajectories rather than adapt its execution to instance-level spatial configurations. In contrast, **VGAS** acts as a geometric stabilizer. By enforcing structural consistency rather than exact path memorization, the learned critic suppresses this variance and selects the candidate (orange) that best matches the current spatial arrangement. Consequently, **VGAS** corrects execution drift induced by rigid imitation in the base policy. Additional experiments on other VLA baselines, inference-budget sensitivity, demonstration-budget scaling, and hyperparameter sensitivity are provided in Appendix E. 

### **4.4 Visualization Analysis** 

Figure 3 visualizes the landscape of estimated action-chunk values projected onto a 2D plane, with _Q_ -values normalized to [ _−_ 1 _,_ 1] for comparison. As shown in the top row, standard conservative regularization (CQL) results in a collapsed value landscape. It indiscriminately suppresses the Q-values of all proposal candidates (white dots) to a uniformly low level. Consequently, the critic loses the resolution to differentiate recoverable near-miss proposals from failures, rendering the selection process ineffective. In contrast, the bottom row demonstrates that VGAS successfully restores finegrained ranking resolution. Instead of uniform suppression, the value signal exhibits a graded geometric preference that decays smoothly as candidates deviate from the expert actions (red dot). This structure ensures that the critic can meaningfully rank candidates based on their physical proximity to the optimal solution. The detailed analysis is in Appendix C. 

## **5 Conclusion and Limitations** 

We propose **VGAS** , which reformulates few-shot VLA adaptation as value-guided selection by decoupling highrecall proposal generation from a high-precision geometric critic. Two components jointly address the near-miss failure mode: Q-Chunk-Former grounds multimodal observations into chunk-level value estimates, and EGR prevents value-landscape collapse to preserve ranking resolution. On LIBERO, **VGAS** consistently outperforms SFT and offline RL baselines. Despite these improvements, two practical limitations remain. First, inference-time Best-of- _N_ selection incurs computational latency, limiting applicability in highfrequency control. Second, extending **VGAS** to real-world platforms remains an important direction for future work. 

## **Acknowledgments** 

The work was supported by the Australian Research Council (ARC) under Laureate project FL190100149. 

## **References** 

- [Bacchiocchi _et al._ , 2024] Francesco Bacchiocchi, Francesco Emanuele Stradi, Matteo Papini, Alberto Maria Metelli, Nicola Gatti, et al. Online learning with offpolicy feedback in adversarial mdps. In _Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence (IJCAI-24)_ , pages 3697–3705, 2024. 

- [Black _et al._ , 2024] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [Brohan _et al._ , 2022] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for realworld control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [Cadene _et al._ , 2024] Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, Steven Palma, Pepijn Kooijmans, Michel Aractingi, Mustafa Shukor, Dana Aubakirova, Martino Russi, Francesco Capuano, Caroline Pascal, Jade Choghari, Jess Moss, and Thomas Wolf. Lerobot: State-of-the-art machine learning for real-world robotics in pytorch. https://github.com/ huggingface/lerobot, 2024. 

- [Chebotar _et al._ , 2023] Yevgen Chebotar, Quan Vuong, Karol Hausman, Fei Xia, Yao Lu, Alex Irpan, Aviral Kumar, Tianhe Yu, Alexander Herzog, Karl Pertsch, et al. Q-transformer: Scalable offline reinforcement learning via autoregressive q-functions. In _Conference on Robot Learning_ , pages 3909–3928. PMLR, 2023. 

- [Chen _et al._ , 2025] Yuhui Chen, Shuai Tian, Shugao Liu, Yingting Zhou, Haoran Li, and Dongbin Zhao. Conrft: A reinforced fine-tuning method for vla models via consistency policy. _arXiv preprint arXiv:2502.05450_ , 2025. 

- [Chi _et al._ , 2025] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

- [Dass _et al._ , 2022] Shivin Dass, Karl Pertsch, Hejia Zhang, Youngwoon Lee, Joseph J Lim, and Stefanos Nikolaidis. Pato: Policy assisted teleoperation for scalable robot data collection. _arXiv preprint arXiv:2212.04708_ , 2022. 

- [Duan _et al._ , 2025] Wei Duan, Jie Lu, En Yu, and Junyu Xuan. Bandwidth-constrained variational message encoding for cooperative multi-agent reinforcement learning. _arXiv preprint arXiv:2512.11179_ , 2025. 

- [Fu _et al._ , 2020] Justin Fu, Aviral Kumar, Ofir Nachum, George Tucker, and Sergey Levine. D4rl: Datasets for 

deep data-driven reinforcement learning. _arXiv preprint arXiv:2004.07219_ , 2020. 

- [Fujimoto _et al._ , 2019] Scott Fujimoto, David Meger, and Doina Precup. Off-policy deep reinforcement learning without exploration. In _International conference on machine learning_ , pages 2052–2062. PMLR, 2019. 

- [Ghasemipour _et al._ , 2021] Seyed Kamyar Seyed Ghasemipour, Dale Schuurmans, and Shixiang Shane Gu. Emaq: Expected-max q-learning operator for simple yet effective offline and online rl. In _International Conference on Machine Learning_ , pages 3682–3691. PMLR, 2021. 

- [Guo _et al._ , 2025] Yanjiang Guo, Jianke Zhang, Xiaoyu Chen, Xiang Ji, Yen-Jen Wang, Yucheng Hu, and Jianyu Chen. Improving vision-language-action model with online reinforcement learning. _arXiv preprint arXiv:2501.16664_ , 2025. 

- [He _et al._ , 2026] Keji He, Yan Huang, Ya Jing, Qi Wu, and Liang Wang. Fine-grained alignment supervision matters in vision-and-language navigation. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 48(6):6525– 6540, 2026. 

- [Hendrycks, 2016] D Hendrycks. Gaussian error linear units (gelus). _arXiv preprint arXiv:1606.08415_ , 2016. 

- [Huang _et al._ , 2025] Dongchi Huang, Zhirui Fang, Tianle Zhang, Yihang Li, Lin Zhao, and Chunhe Xia. Corft: Efficient fine-tuning of vision-language-action models through chunked offline reinforcement learning. _arXiv preprint arXiv:2508.02219_ , 2025. 

- [Intelligence _et al._ , 2025] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [Janner _et al._ , 2022] Michael Janner, Yilun Du, Joshua B Tenenbaum, and Sergey Levine. Planning with diffusion for flexible behavior synthesis. _arXiv preprint arXiv:2205.09991_ , 2022. 

- [Kim _et al._ , 2024] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [Kim _et al._ , 2025] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- [Kingma, 2014] Diederik P Kingma. Adam: A method for stochastic optimization. _arXiv preprint arXiv:1412.6980_ , 2014. 

- [Kong _et al._ , 2024] Rui Kong, Chenyang Wu, Chen-Xiao Gao, Zongzhang Zhang, and Ming Li. Efficient and stable offline-to-online reinforcement learning via continual policy revitalization. In _Proceedings of the Thirty-Third_ 

_International Joint Conference on Artificial Intelligence, IJCAI-24_ , pages 4317–4325, 2024. 

- [Kostrikov _et al._ , 2021] Ilya Kostrikov, Ashvin Nair, and Sergey Levine. Offline reinforcement learning with implicit q-learning. _arXiv preprint arXiv:2110.06169_ , 2021. 

- [Kumar _et al._ , 2020] Aviral Kumar, Aurick Zhou, George Tucker, and Sergey Levine. Conservative Q-learning for offline reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. 

- [Kumar _et al._ , 2022] Aviral Kumar, Anikait Singh, Frederik Ebert, Mitsuhiko Nakamoto, Yanlai Yang, Chelsea Finn, and Sergey Levine. Pre-training for robots: Offline rl enables learning new tasks from a handful of trials. _arXiv preprint arXiv:2210.05178_ , 2022. 

- [Levine _et al._ , 2020] Sergey Levine, Aviral Kumar, George Tucker, and Justin Fu. Offline reinforcement learning: Tutorial, review, and perspectives on open problems. _arXiv preprint arXiv:2005.01643_ , 2020. 

- [Li _et al._ , 2025a] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025. 

- [Li _et al._ , 2025b] Qiyang Li, Zhiyuan Zhou, and Sergey Levine. Reinforcement learning with action chunking. _arXiv preprint arXiv:2507.07969_ , 2025. 

- [Liu _et al._ , 2023] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- [Liu _et al._ , 2025] Jijia Liu, Feng Gao, Bingwen Wei, Xinlei Chen, Qingmin Liao, Yi Wu, Chao Yu, and Yu Wang. What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , 2025. 

- [Lu _et al._ , 2022] Cong Lu, Philip J Ball, Tim GJ Rudner, Jack Parker-Holder, Michael A Osborne, and Yee Whye Teh. Challenges and opportunities in offline reinforcement learning from visual observations. _arXiv preprint arXiv:2206.04779_ , 2022. 

- [Luo _et al._ , ] Kairong Luo, CAIWEI XIAO, Zhiao Huang, Zhan Ling, Yunhao Fang, and Hao Su. Dreamfuser: Valueguided diffusion policy for offline reinforcement learning. 

- [Lyu _et al._ , 2022] Jiafei Lyu, Xiaoteng Ma, Xiu Li, and Zongqing Lu. Mildly conservative q-learning for offline reinforcement learning. _Advances in Neural Information Processing Systems_ , 35:1711–1724, 2022. 

- [Marafioti _et al._ , 2025] Andr´es Marafioti, Orr Zohar, Miquel Farr´e, Merve Noyan, Elie Bakouch, Pedro Cuenca, Cyril Zakka, Loubna Ben Allal, Anton Lozhkov, Nouamane Tazi, et al. Smolvlm: Redefining small and efficient multimodal models. _arXiv preprint arXiv:2504.05299_ , 2025. 

- [Mark _et al._ , 2024] Max Sobol Mark, Tian Gao, Georgia Gabriela Sampaio, Mohan Kumar Srirama, Archit 

Sharma, Chelsea Finn, and Aviral Kumar. Policy agnostic rl: Offline rl and online rl fine-tuning of any class and backbone. _arXiv preprint arXiv:2412.06685_ , 2024. 

- [Nakamoto _et al._ , 2025] Mitsuhiko Nakamoto, Oier Mees, Aviral Kumar, and Sergey Levine. Steering your generalists: Improving robotic foundation models via value guidance. In _Conference on Robot Learning_ , pages 4996–5013. PMLR, 2025. 

- [Peng _et al._ , 2025] Bo Peng, Jie Lu, Yonggang Zhang, Guangquan Zhang, and Zhen Fang. Distributional prototype learning for out-of-distribution detection. In _Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 1_ , pages 1104–1114, 2025. 

- [Pertsch _et al._ , 2025] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [Sapkota _et al._ , 2025] Ranjan Sapkota, Yang Cao, Konstantinos I Roumeliotis, and Manoj Karkee. Vision-languageaction models: Concepts, progress, applications and challenges. _arXiv preprint arXiv:2505.04769_ , 2025. 

- [Schulman _et al._ , 2017] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [Shao _et al._ , 2024] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [Shin and Kim, 2023] Wonchul Shin and Yusung Kim. Guide to control: Offline hierarchical reinforcement learning using subgoal generation for long-horizon and sparsereward tasks. In _IJCAI_ , pages 4217–4225, 2023. 

- [Shukor _et al._ , 2025] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- [Song _et al._ , 2025] Haoming Song, Delin Qu, Yuanqi Yao, Qizhi Chen, Qi Lv, Yiwen Tang, Modi Shi, Guanghui Ren, Maoqing Yao, Bin Zhao, et al. Hume: Introducing system2 thinking in visual-language-action model. _arXiv preprint arXiv:2505.21432_ , 2025. 

- [Sutton _et al._ , 1998] Richard S Sutton, Andrew G Barto, et al. _Reinforcement learning: An introduction_ , volume 1. MIT press Cambridge, 1998. 

- [Sutton _et al._ , 1999] Richard S Sutton, Doina Precup, and Satinder Singh. Between mdps and semi-mdps: A framework for temporal abstraction in reinforcement learning. _Artificial intelligence_ , 112(1-2):181–211, 1999. 

- [Tan _et al._ , ] Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Kr¨ahenb¨uhl. Interactive post-training for vision-languageaction models (2025). _arXiv preprint arXiv:2505.17016_ . 

- [Team _et al._ , 2024] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

   - [Zitkovich _et al._ , 2023] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

- [Xin _et al._ , 2024] Jimmy Xin, Linus Zheng, Kia Rahmani, Jiayi Wei, Jarrett Holtz, Isil Dillig, and Joydeep Biswas. Programmatic imitation learning from unlabeled and noisy demonstrations. _IEEE Robotics and Automation Letters_ , 9(6):4894–4901, 2024. 

- [Yang _et al._ , 2025] Xiaoyu Yang, Jie Lu, and En Yu. Adapting multi-modal large language model to concept drift from pre-training onwards. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [Yang _et al._ , 2026] Xiaoyu Yang, Jie Lu, and En Yu. Walking the tightrope: Autonomous disentangling beneficial and detrimental drifts in non-stationary custom-tuning. _Advances in Neural Information Processing Systems_ , 38:116167–116193, 2026. 

- [Yu _et al._ , 2020] En Yu, Jing Li, Li Wang, Jia Zhang, Wenbo Wan, and Jiande Sun. Multi-class joint subspace learning for cross-modal retrieval. _Pattern Recognition Letters_ , 130:165–173, 2020. 

- [Yu _et al._ , 2026a] En Yu, Jie Lu, Xiaoyu Yang, Guangquan Zhang, and Zhen Fang. Learning robust spectral dynamics for temporal domain generalization. _Advances in Neural Information Processing Systems_ , 38:148725–148751, 2026. 

- [Yu _et al._ , 2026b] En Yu, Jie Lu, and Guangquan Zhang. Generalized incremental learning under concept drift across evolving data streams. In _Proceedings of the ACM Web Conference 2026_ , WWW ’26, page 3905–3916, 2026. 

- [Zhang and Tan, 2023] Zhe Zhang and Xiaoyang Tan. Adaptive reward shifting based on behavior proximity for offline reinforcement learning. In _IJCAI_ , pages 4620–4628, 2023. 

- [Zhang _et al._ , 2025a] Dapeng Zhang, Jing Sun, Chenghui Hu, Xiaoyan Wu, Zhenlong Yuan, Rui Zhou, Fei Shen, and Qingguo Zhou. Pure vision language action (vla) models: A comprehensive survey. _arXiv preprint arXiv:2509.19012_ , 2025. 

- [Zhang _et al._ , 2025b] Tianlin Zhang, En Yu, Yi Shao, and Jiande Sun. Multimodal inverse attention network with intrinsic discriminant feature exploitation for fake news detection. In _Proceedings of the Thirty-Fourth International Joint Conference on Artificial Intelligence, IJCAI25_ , pages 7940–7948. International Joint Conferences on Artificial Intelligence Organization, 8 2025. 

- [Zhao _et al._ , 2023] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost arms. In _Robotics: Science and Systems (RSS)_ , 2023. 

## **A Related Work** 

### **A.1 Vision-Language-Action Models.** 

The intersection of computer vision and robotic control has been advanced by Vision-Language-Action (VLA) models, which endow high-capacity Vision-Language Models (VLMs) with actuation capabilities to map multimodal inputs (visual observations and natural language instructions) to executable robot actions [Zitkovich _et al._ , 2023; Yang _et al._ , 2026]. Representative architectures such as RT-2 [Zitkovich _et al._ , 2023], Octo [Team _et al._ , 2024], OpenVLA [Kim _et al._ , 2024], and related works [Brohan _et al._ , 2022; Black _et al._ , 2024; Intelligence _et al._ , 2025] demonstrate strong generalization across diverse tasks. A common paradigm is large-scale pre-training followed by supervised fine-tuning (SFT) on robotic demonstrations, which grounds semantic knowledge into physical control. 

Despite this progress, pure imitation remains limited for efficient adaptation. SFT typically requires substantial expert coverage and can degrade sharply in few-shot regimes. Moreover, many VLAs generate actions via open-loop chunking [Zhao _et al._ , 2023], without an intrinsic mechanism to evaluate or rank candidate chunks by physical fidelity. This motivates adapting pretrained VLAs beyond static imitation by introducing explicit value-based evaluation for action-chunk selection. 

### **A.2 Value-based Offline Reinforcement Learning.** 

Reinforcement learning (RL) [Levine _et al._ , 2020; Duan _et al._ , 2025; Yang _et al._ , 2026] seeks policies that maximize long-horizon return [Kong _et al._ , 2024]. In the offline setting, value functions can be learned from static datasets without additional interaction, making critic-centric methods attractive when online rollouts [Bacchiocchi _et al._ , 2024] are costly or unsafe. To prevent extrapolation errors, Conservative offline RL methods [Kumar _et al._ , 2020] mitigate extrapolation error by suppressing values of out-of-distribution (OOD) actions [Zhang and Tan, 2023; Yang _et al._ , 2025; Peng _et al._ , 2025], while implicit approaches like IQL [Kostrikov _et al._ , 2021] tend to avoid OOD actions via behaviorregularized policy extraction. 

_Sampling-based Maximization (Best-of-N )._ In continuous action spaces, directly computing max _a Q_ ( _s, a_ ) is often intractable. A widely used surrogate is _proposal-constrained maximization_ : sample _N_ candidate actions from a behavior-aligned proposal (or a learned generative model) and select the argmax under a critic. BCQ [Fujimoto _et al._ , 2019] is a canonical example, using a state-conditioned generative model to produce in-distribution candidates and choosing the highest-valued action via a learned Q-function. EMaQ [Ghasemipour _et al._ , 2021] formalizes this principle via an _Expected-Max_ backup operator that interpolates between evaluation and maximization through the number of samples _N_ , providing an operator-level view of Best-of- _N_ style policy improvement. More recently, generative planners such as Diffuser [Janner _et al._ , 2022] and value-guided diffusion methods [Luo _et al._ , ] similarly combine sampling with value-based guidance or reranking over action sequences or trajectories, sharing the core idea of improving decision quality through learned value signals. 

### **A.3 RL for VLA Models.** 

Integrating RL into VLA models aims to combine semantic reasoning with return-driven optimization. A core challenge is that modern VLAs often execute _action chunks_ (temporally extended sequences) rather than atomic actions, which shifts both credit assignment and value estimation from the single-step regime to the chunk level. Moreover, unlike traditional RL that operates on compact state vectors, VLAs condition on high-dimensional multimodal inputs (vision, language, and proprioception), making stable value learning sensitive to cross-modal fusion and representation balance. 

_Action Chunk Value learning._ Recent works extend value learning to action chunking by treating a short-horizon action sequence as a single decision unit [Li _et al._ , 2025b], showing that chunk-level Q-functions can improve temporal consistency. This line of work also introduces unbiased _n_ -step backup targets to stabilize and accelerate TD learning under temporally extended actions. While promising in low-dimensional state settings, scaling chunk-level critics to high-dimensional multimodal inputs (vision, language, and proprioception) remains challenging. 

_Online Fine-tuning._ A line of work fine-tunes VLAs via online RL or interactive learning [Li _et al._ , 2025a; Tan _et al._ , ; Mark _et al._ , 2024; Guo _et al._ , 2025]. These methods typically do not learn an explicit Q-function; instead, they update the policy using on-policy algorithms such as PPO [Schulman _et al._ , 2017] or GRPO [Shao _et al._ , 2024], where policy gradients are estimated from trajectory-level advantage signals. While effective, online fine-tuning can incur substantial interaction costs and safety concerns, making it less practical for rapid few-shot adaptation. Moreover, trajectory-level supervision can provide relatively coarse credit assignment, which may be insufficient to correct fine-grained geometric errors in long-horizon manipulation. 

_Offline Value Learning._ Alternatively, approaches such as Q-Transformer [Chebotar _et al._ , 2023] learn Q-functions from offline data to enable end-to-end control. More closely related to our setting, V-GPS [Nakamoto _et al._ , 2025] and Hume [Song _et al._ , 2025] also learn value functions from offline datasets and make decisions by scoring and selecting among candidate actions. Similarly, ConRFT [Chen _et al._ , 2025] improves VLA policies via offline RL. However, most of these methods are primarily formulated for single-step action evaluation and thus do not directly align with chunk-based VLA policies that execute temporally-extended action sequences. Moreover, these approaches [Chebotar _et al._ , 2023; Nakamoto _et al._ , 2025; Song _et al._ , 2025; Yu _et al._ , 2020; Zhang _et al._ , 2025b] typically compress multimodal observations into a single latent vector for value prediction, which can discard fine-grained cues needed for accurate value estimation and precise action ranking. 

## **B Theoretical Analysis** 

In this appendix, we provide proofs for the convergence properties of the _Proposal-Constrained Chunked Expected-Max_ operator introduced in Sec. 3.2. Our analysis adapts the operator-level argument of EMaQ [Ghasemipour _et al._ , 2021] to the induced semi-Markov decision process (SMDP) formed by length- _h_ action chunks. 

### **B.1 Convergence of the Chunked Expected-Max Operator** 

**Induced SMDP and bounded function space.** Let A = ( _a_ 0 _, . . . , ah−_ 1) _∈A_<sup>_h_</sup> denote an action chunk. We consider the induced SMDP with (i) the chunked discounted return 


(ii) the _h_ -step transition kernel _P_<sup>_h_</sup> ( _· | s,_ A), and (iii) the effective discount factor _γ_<sup>_h_</sup> . Assume bounded one-step rewards _|r_ ( _s, a_ ) _| ≤ r_ max and _γ ∈_ (0 _,_ 1). Then 


Let _B_ denote the space of bounded real-valued functions over chunk state-action pairs: 


(We assume _Q_ is bounded and measurable; the analysis extends to continuous _A_<sup>_h_</sup> (equivalently _B_ = _L∞_ ( _S × A_<sup>_h_</sup> ) under _∥· ∥∞_ ).) **Definition 1** (Chunked Expected-Max Operator) **.** _Fix a proposal distribution πµ_ (A _| s_ ) _over action chunks and an integer N ≥_ 1 _. Define Tµ_<sup>_N_</sup> : _B →B by_ 


**Lemma 1** (Well-definedness) **.** _Assume |r_ ( _s, a_ ) _| ≤ r_ max _and γ ∈_ (0 _,_ 1) _, hence |Rh_ ( _s,_ A) _| ≤ R_ max _as in_ (20) _. Then for any Q ∈B,_ 


_In particular, Tµ_<sup>_NQ ∈B._</sup> 

_Proof._ For any _Q ∈B_ and ( _s,_ A), let _s_<sup>_′_</sup> _∼P_<sup>_h_</sup> ( _· | s,_ A). We have: 


since max _i |Q_ ( _s_<sup>_′_</sup> _,_ A<sup>_′_</sup> _i_<sup>)</sup><sup>_| ≤∥Q∥∞_.Taking sup</sup> ( _s,_ A)<sup>yields the claim.</sup> 

**Lemma 2** (Non-expansiveness of expected max) **.** _Let u, v be bounded functions and let X_ 1 _, . . . , XN be random variables. Then_ 


_Proof._ Using _|_ E[ _Z_ ] _| ≤_ E[ _|Z|_ ], 


For any realizations _{xi}_ , 


Taking expectation completes the proof. 

**Theorem 1** ( _γ_<sup>_h_</sup> -Contraction) **.** _For any N ≥_ 1 _, the operator Tµ_<sup>_Nis a γh-contraction under ∥· ∥∞:_</sup> 

_∥Tµ_<sup>_NQ_1</sup><sup>_−T_</sup> _µ_<sup>_NQ_2</sup><sup>_∥∞≤γh∥Q_1</sup><sup>_−Q_2</sup><sup>_∥∞,_</sup> _∀ Q_ 1 _, Q_ 2 _∈B. Consequently, Tµ_<sup>_Nadmits a unique fixed point QN_</sup> _µ_<sup>_∈B and_(</sup><sup>_T_</sup> _µ_<sup>_N_)</sup><sup>_kQ_0</sup><sup>_→QN_</sup> _µ_<sup>_for any Q_0</sup><sup>_∈B._</sup> 

_Proof._ Fix ( _s,_ A) and let _Q_ 1 _, Q_ 2 _∈B_ . The reward terms cancel: 


where 


Applying Lemma 2 to _u_ ( _·_ ) = _Q_ 1( _s_<sup>_′_</sup> _, ·_ ) and _v_ ( _·_ ) = _Q_ 2( _s_<sup>_′_</sup> _, ·_ ) yields _|gN_ ( _Q_ 1)( _s_<sup>_′_</sup> ) _− gN_ ( _Q_ 2)( _s_<sup>_′_</sup> ) _| ≤∥Q_ 1 _− Q_ 2 _∥∞_ for all _s_<sup>_′_</sup> . Thus _|_ ( _Tµ_<sup>_NQ_1)(</sup><sup>_s,_A)</sup><sup>_−_(</sup><sup>_T_</sup> _µ_<sup>_NQ_2)(</sup><sup>_s,_A)</sup><sup>_| ≤γh∥Q_1</sup><sup>_−Q_2</sup><sup>_∥∞._</sup> 

Taking sup( _s,_ A) gives the contraction inequality. Since _γ_<sup>_h_</sup> _<_ 1 and Lemma 1 ensures _Tµ_<sup>_N_</sup> : _B →B_ , Banach’s fixed-point theorem implies existence/uniqueness and convergence. 

**Proposition 3** (Monotonicity in _N_ ) **.** _Let Q_<sup>_N_</sup> _µ_<sup>_denote the unique fixed point of T_</sup> _µ_<sup>_N.For any integers N> M≥_1</sup><sup>_, we have_</sup> 


_Proof._ For any bounded _Q_ and any ( _s,_ A), draw A<sup>_′_</sup> 1: _N_<sup>_∼πµ_(</sup><sup>_· | s′_) once and use the first</sup><sup>_M_samples for the</sup><sup>_M_-sample backup.</sup> Then for every realization, 


Taking expectation over A<sup>_′_</sup> 1: _N_<sup>and</sup><sup>_s′_yields (</sup><sup>_T_</sup> _µ_<sup>_NQ_)(</sup><sup>_s,_A)</sup><sup>_≥_(</sup><sup>_T_</sup> _µ_<sup>_MQ_)(</sup><sup>_s,_A).Now apply the above pointwise inequality to</sup><sup>_QM_</sup> _µ_<sup>.</sup> Since _Q_<sup>_M_</sup> _µ_<sup>=</sup><sup>_T_</sup> _µ_<sup>_MQM_</sup> _µ_<sup>, we have</sup><sup>_QM_</sup> _µ_<sup>_≤T_</sup> _µ_<sup>_NQM_</sup> _µ_<sup>.Moreover,</sup><sup>_T_</sup> _µ_<sup>_N_is order-preserving in</sup><sup>_Q_(max and expectation preserve order),</sup> hence ( _Tµ_<sup>_N_)</sup><sup>_kQM_</sup> _µ_<sup>_≥QM_</sup> _µ_<sup>for all</sup><sup>_k_.Taking</sup><sup>_k→∞_and using Theorem 1 yields</sup><sup>_QN_</sup> _µ_<sup>= lim</sup><sup>_k→∞_(</sup><sup>_T_</sup> _µ_<sup>_N_)</sup><sup>_kQM_</sup> _µ_<sup>_≥QM_</sup> _µ_<sup>.</sup> 

**Theorem 2** (Limit as _N →∞_ (sketch)) **.** _Under standard regularity assumptions (e.g., no ties / continuous proposal density), the fixed points {Q_<sup>_N_</sup> _µ_<sup>_}N≥_1</sup><sup>_converge pointwise to the optimal value function whose actions are restricted to the support of πµ,_</sup> _denoted Q_<sup>_⋆_</sup> _πµ_<sup>_:_</sup> 


_Proof sketch._ For any fixed _Q_ and state _s_<sup>_′_</sup> , define 


Then _gN_ ( _Q_ )( _s_<sup>_′_</sup> ) is non-decreasing in _N_ and converges to the essential supremum of _Q_ ( _s_<sup>_′_</sup> _,_ A) over A _∼ πµ_ ( _· | s_<sup>_′_</sup> ). Consequently, _Tµ_<sup>_N_</sup> converges (pointwise) to the support-restricted optimality operator. Monotonicity in _N_ (Prop. 3), together with contraction (Thm. 1), yields convergence of the fixed points; see the corresponding EMaQ analysis [Ghasemipour _et al._ , 2021]. 

### **B.2 EGR Anchoring Envelope and Best-of-** _N_ **Bound** 

We formalize how the EGR regression objective induces an _upper-envelope_ inequality over off-demo candidates sampled from _ρ_ ( _· | st_ ), and how such an envelope immediately bounds the Best-of- _N_ maximization used in the chunked TD target. 

**Setup.** Fix a data (demonstration) pair ( _st,_ A _t_ ) _∼D_ and an auxiliary candidate distribution _ρ_ ( _· | st_ ). Recall the EGR reference surface (Eq. (14)): 


where _β >_ 0 and _yt_ is the chunk-level TD anchor (Eq. (12)). Define the pointwise EGR residual 


**From EGR regression to an upper envelope.** The anchoring loss encourages _δθ_ ( _st,_ A<sup>_′_</sup> _t_<sup>) to be small on candidates A</sup> _t_<sup>_′∼ρ_(</sup><sup>_· |_</sup> _st_ ). To make this statement explicit, we assume the residual is uniformly upper-bounded on the candidate set. **Lemma 3** (Anchoring-induced upper envelope via a residual bound) **.** _Assume the residual admits a uniform upper bound on the candidate set:_ 


_Proof._ From the residual definition in (24), for any A<sup>_′_</sup> _t_<sup>we have the identity</sup> 

_Qθ_ ( _st,_ A<sup>_′_</sup> _t_<sup>) =</sup><sup>_Y_(</sup><sup>_st,_A</sup><sup>_′_</sup> _t_<sup>) +</sup><sup>_δθ_(</sup><sup>_st,_A</sup><sup>_′_</sup> _t_<sup>)</sup><sup>_._</sup> (27) For any A<sup>_′_</sup> _t_<sup>_∈_supp(</sup><sup>_ρ_(</sup><sup>_·|st_)),theboundEq.(25)implies</sup><sup>_δθ_(</sup><sup>_st,_A</sup><sup>_′_</sup> _t_<sup>)</sup><sup>_≤ε_.SubstitutingintoEq.(27)yields</sup><sup>_Qθ_(</sup><sup>_st,_A</sup><sup>_′_</sup> _t_<sup>)</sup><sup>_≤_</sup> _Y_ ( _st,_ A<sup>_′_</sup> _t_<sup>) +</sup><sup>_ε._Finally, plugging in Eq. (23) gives Eq. (26).</sup> 

**Bounding Best-of-** _N_ **under the envelope.** We now show the envelope immediately bounds the Best-of- _N_ maximization. Recall that the EGR loss is minimized over a broad OOD distribution _ρ_ ( _· | st_ ). In our implementation (Appendix D), _ρ_ is constructed as a mixture that explicitly includes samples from the proposal policy _πµ_ . Consequently, supp( _πµ_ ) _⊆_ supp( _ρ_ ). Thus, if the envelope holds for _ρ_ , it naturally holds for _πµ_ . 

**Proposition 4** (Best-of- _N_ bound under an EGR-style upper envelope) **.** _Let_ ( _st,_ A _t_ ) _∼D and let πµ_ ( _· | st_ ) _be the candidate sampling distribution. Draw N candidates {_ A<sup>_′_</sup> _t_<sup>_i}N_</sup> _i_ =1<sup>_∼πµ_(</sup><sup>_· | st_)</sup><sup>_.If the envelope Eq._(26)</sup><sup>_holds for all_A</sup> _t_<sup>_′∈_supp(</sup><sup>_πµ_(</sup><sup>_· | st_))</sup> _(inherited from ρ), then_ 


_Proof._ Apply Eq. (26) to each sampled candidate A<sup>_′_</sup> _t_<sup>_i_:</sup> 


Taking max _i∈_ [ _N_ ] on both sides gives 


Since sg( _yt_ ) and _ε_ do not depend on _i_ , and _−β_ ( _·_ ) is decreasing in the distance term, 


which proves the first inequality in Eq. (28). The second inequality follows since min _i ∥_ A<sup>_′_</sup> _t_<sup>_i−_A</sup><sup>_t∥_2</sup> _W_<sup>_≥_0.</sup> 

**Remark.** The residual bound Eq. (25) is not an additional algorithmic constraint: it is a compact way to express that the EGR regression error on the candidate set is small. In practice, _ε_ can be interpreted as the worst-case anchoring fit error over candidates drawn from _πµ_ ( _· | st_ ). 

## **C Visualization Methodology and Detailed Analysis** 

Figure 3 visualizes the landscape of estimated state-action-chunk values on the LIBERO-Object benchmark. To interpret the high-dimensional action chunks (dimension _h × d_ action), we use Principal Component Analysis (PCA) to project proposal candidates and ground-truth (GT) demonstrations onto a 2D plane, normalizing estimated _Q_ -values to [ _−_ 1 _,_ 1] for comparison. The color gradient—from yellow (high value) to dark blue (low value)—reveals clear differences in landscape topology between the two approaches. The top row shows that CQL-style regularization results in a collapsed value landscape: it indiscriminately suppresses all proposal candidates (white dots) to a uniformly low value regardless of their quality, failing to differentiate “near-miss” proposals from failures. In contrast, the bottom row demonstrates that VGAS (with EGR) yields a discriminative value landscape. Instead of a binary plateau, the value signal exhibits a graded geometric preference, decaying smoothly as candidates deviate from the expert trajectory. This confirms that EGR acts as a structural inductive bias, enabling the critic to meaningfully rank candidates based on their physical proximity to the optimal solution. 

We further observe distinct spatial and temporal characteristics in the learned landscapes. Spatially, there is a visible gap between the proposal distribution and the GT (red dot); we attribute this to the mean-seeking bias of the SFT policy, which tends to generate smoothed trajectories compared to the sharper, high-frequency control signals of human experts. Crucially, VGAS maintains a valid gradient across this gap, guiding selection toward the expert mode despite the distribution shift. Temporally, the value maps exhibit dynamic coherence: adjacent timesteps ( _t_ = 0 and _t_ = 1) share similar topologies, whereas distant steps ( _t_ = 50 and _t_ = 120) show significant structural differences. This indicates that the VGAS does not merely memorize static geometric relations but adaptively adjusts its estimation according to evolving real-world dynamics, providing state-aware guidance throughout the entire task horizon. 


Figure 5: Offline Ranking Evaluation on Held-out Data. 

## **D Implementation Details** 

### **D.1 Experimental Setup** 

**(i) Reward function.** Consistent with real-world scenarios where explicit rewards are scarce, the LIBERO dataset contains no reward annotations. We therefore construct a sparse binary reward by labeling the last _h_ steps of each demonstration rollout as successful. Following [Nakamoto _et al._ , 2025], we set _h_ = 3. Additionally, we use shifted rewards _{−_ 1 _,_ 1 _}_ instead of _{_ 0 _,_ 1 _}_ , which we found to yield more stable learning in practice. 

**(ii) Training protocol.** We first perform supervised fine-tuning (SFT) of the VLA model using 5-shot expert demonstrations per task, randomly sampled from the LIBERO dataset. We then train a critic using different variants of offline RL (ORL) objectives on the resulting offline data. 

**(iii) OOD candidate generation.** Following the conservative offline RL intuition (e.g., CQL) that penalizes actions with low support under the offline dataset, we construct OOD candidates by sampling from _ρ_ ( _· | st_ ), instantiated as a mixture of: (i) proposals from the frozen VLA policy _πµ_ ( _· | st_ ); (ii) Gaussian perturbations of the demonstration (ground-truth) chunk A _t_ (GT+noise); (iii) prefix-truncated variants of A _t_ (early-terminated chunks); and (iv) linear interpolations between the demonstration chunk and a policy proposal, i.e., A<sup>˜</sup> _t_ = _α_ A _t_ + (1 _− α_ ) A<sup>ˆ</sup> _t._ and _α ∈_ [0 _,_ 1]. 

**(iv) Backbone Architecture Details.** We adopt SmolVLA-0.5B [Shukor _et al._ , 2025] as the underlying policy backbone. Built upon the SmolVLM2 architecture, it employs a SigLIP visual encoder to process high-dimensional observations. These visual tokens are fused with language instructions and proprioceptive states within a decoder-only Transformer. The policy head utilizes a flow-matching objective to generate high-dimensional action chunks in parallel, which serves as the proposal distribution for our VGAS framework. 

### **D.2 Baseline Implementation Details** 

**Base Policy Training.** To evaluate performance in a realistic data-scarce regime, we adopt a standardized two-stage training protocol for all methods. First, we obtain the base proposal policy _πµ_ by fine-tuning the SmolVLA backbone using only 5 expert demonstrations per task, randomly sampled from the LIBERO benchmark<sup>2</sup> . This fine-tuning is conducted via the official LeRobot [Cadene _et al._ , 2024] repository<sup>3</sup> . In the second stage, we freeze this few-shot adapted policy to serve as a 

> 2https://huggingface.co/datasets/HuggingFaceVLA/libero 

> 3https://github.com/huggingface/lerobot 

Table 3: Hyperparameters for VGAS. 

|**Hyperparameter**|**Value**|
|---|---|
|Learning rate|0.0001|
|Optimizer|Adam [Kingma, 2014]|
|Warm up step|1000|
|Gradient steps|12000 (default), 20000 (Libero-Goal, Libero-long)|
|Gradient-clip|10.0|
|Minibatch size|32|
|Q-chunk-Former layers|2|
|Q-chunk-Former hidden dimensions|960|
|State-Action-Fusion Mlp dimensions|960|
|Q chunk len|32(default), 50 (Libero Long)|
|N-action-step|20|
|Vlaue Head MLP dimensions|[512, 512]<br>|
|Vlaue head Nonlinearity|GELU [Hendrycks, 2016]|
|Target network smoothing coefficient|0.005|
|Discount factor_γ_|0.98 (default), 0.99 (Libero-Long)|
|Clipped double Q-learning|True|
|Q aggregation (twin critics)|Min|


Table 4: Hyperparameters for Different Task suit. 

|Task suit|_λ_|_β_|_η_|w|
|---|---|---|---|---|
|Libero-Spatial|5.0|5.0|1.0|5 5 5 1 1 1 1|
|Libero-Goal|5.0|5.0|1.0|5 5 5 1 1 1 1|
|Libero-Object|2.0|2.0|1.0|5 5 5 1 1 1 1|
|Libero-Long|5.0|5.0|1.0|5 5 5 1 1 1 1|


static proposal generator. Crucially, the offline dataset _D_ used to train the critic (for both VGAS and baselines) is constructed exclusively from these same 5-shot demonstrations, ensuring that value learning operates under the same strict data-scarce constraints. 

**Baseline Configurations.** Unless stated otherwise, all methods keep _πµ_ fixed and differ only in the critic objective and architecture. 

- **BC-Only:** This baseline directly executes the base policy _πµ_ obtained in the first stage without any test-time selection. 

- **QC-M (Q-Chunking-MLP):** Q-Chunking [Li _et al._ , 2025b] proposes two variants: QC (Best-of- _N_ backup) and QC-FQL (Flow Matching distillation). We adopt the QC variant for direct comparison. Following the official implementation, we use an MLP critic with hidden dimensions [512 _,_ 512 _,_ 512 _,_ 512]. For state encoding, we pool the VLM tokens ( _It, Lt_ and _pt_ ) from the backbone into a fixed representation (dim=960). The action chunk ( _h × da_ ) is flattened and projected via an MLP to match the state dimension. Finally, the state and action chunk representations are concatenated and fed into the critic. 

- **QC-M+CQL:** We augment QC-M by adding the CQL regularization term. We use the default coefficient _α_ = 5 _._ 0, which performs comparably to alternative choices (e.g., _α_ = 2 _._ 0) in our validation. The negative (OOD) action pool is sampled from the proposal-centered distribution _πµ_ ( _· | st_ ), ensuring alignment with our method’s _ρ_ ( _· | st_ ) construction for fair comparison 

- **QC-T+CQL:** We retain the QC-M+CQL objective but replace the MLP backbone with our Transformer-based Q-ChunkFormer. This baseline isolates the effect of critic architecture under identical conservative constraints. 

**Shared rollout settings.** Unless otherwise specified, all methods use the same chunk length _h_ = 32 (or _h_ = 50 for LIBEROLong) to estimate _Q_ ( _st,_ A _t_ ), where A _t_ := ( _at, at_ +1 _, . . . , at_ + _h−_ 1) denotes an _h_ -step action chunk. During execution, we apply only the first _n_ exec = 20 action steps of each selected chunk, i.e., ( _at, at_ +1 _, . . . , at_ + _n_ exec _−_ 1) with _n_ exec _< h_ . 

**VGAS.** We report the complete list of hyperparameters in Table 3, and task-specific overrides in Table 4. Our Q-ChunkFormer is initialized from the first two layers of the SmolVLM backbone. We directly reuse the multimodal features extracted by the frozen SmolVLM (i.e., the output of the SmolVLA encoder) as the vision–language input to Q-Chunk-Former. In our notation, the _Q-chunk length h_ denotes the length of an action chunk, while _N -action-step_ indicates that we execute only the 

first _N_ primitive actions within each predicted chunk at rollout. We use clipped double Q-learning: the TD target is computed using the minimum of the two target critics. 

### **D.3 Weighted metric implementatipn Details** 

In the Explicit Geometric Regularization (EGR) objective (Eq. 14 and Eq. 16), the term _∥_ A<sup>ˆ</sup> _t −_ A _t∥_<sup>2</sup> _W_<sup>denotes a</sup><sup>_weighted squared_</sup> _Euclidean distance_ , averaged over the valid horizon of an action chunk. This metric prioritizes critical action dimensions (e.g., end-effector translation) and supports variable-length chunks via a padding mask. 

Let A _∈_ R<sup>_h×da_</sup> be the ground-truth action chunk and A<sup>ˆ</sup> _∈_ R<sup>_h×da_</sup> be a candidate chunk, where _h_ is the chunk size and _da_ is the action dimension ((for LIBERO, typically _da_ = 7: 3D end-effector position, 3D end-effector orientation (a 3-parameter representation), and 1D gripper control) ). Let w _∈_ R<sup>_da_</sup> be a nonnegative weight vector. We define the masked, weighted squared distance as 


where: 

- _mk ∈{_ 0 _,_ 1 _}_ is a binary mask indicating whether time step _k_ is valid (i.e., non-padding), 

- _a_ ˆ _k,j_ and _ak,j_ denote the _j_ -th action dimension at step _k_ for A<sup>ˆ</sup> and A, respectively, 

- w = [ _w_ 1 _, . . . , wda_ ] specifies the relative importance of each control dimension. 

**Weight configuration.** As shown in Table 4, we set w = [5 _,_ 5 _,_ 5 _,_ 1 _,_ 1 _,_ 1 _,_ 1], assigning weight 5 _._ 0 to translational components ( _x, y, z_ ) and weight 1 _._ 0 to rotation and gripper states. Empirically, penalizing position errors more heavily encourages the critic to emphasize trajectory precision, which is crucial for manipulation success. 

## **E Additional Experimental Results and Analysis** 

### **E.1 Training Dynamics and Critic Ranking Resolution** 

To verify the critic’s generalization ability, we evaluate it offline on a held-out set of 45 unseen expert episodes per task. For each observation, we sample _N_ = 8 proposal candidates and report the Top-1 Hit Rate (the probability of selecting the proposal that is geometrically closest to the expert) and the Spearman correlation. Fig. 5 reveals three key findings. First, VGAS consistently assigns higher scores to candidates that remain close to the expert, which reduces overestimation on geometrically divergent OOD actions and supports safer selection on unseen states where the policy may drift. Second, the high hit rate indicates that VGAS builds a discriminative value landscape within the proposal set. In contrast, CQL tends to flatten local value differences, weakening ranking resolution. VGAS preserves a clear ordering among “near-miss” candidates, making superior candidates easier to separate from inferior ones. Finally, comparing the “With Expert” setting (middle row) and the “Candidates Only” setting (top row) highlights an important difference. CQL can assign high scores to the expert action when it is included, but its local ranking becomes less reliable when only proposal candidates are available. VGAS performs well in both settings. Although geometric proximity is not a perfect proxy for task success, it provides a practical signal in the few-shot imitation regime, where unconstrained maximization is brittle. 


Figure 6: Impact of Inference Budget _N_ . Evaluation on LIBERO-Goal showing monotonic improvement from the baseline ( _N_ = 1) to saturation around _N_ = 8. 


Figure 7: Additional VLA baselines under the 5-shot LIBERO setting. VGAS improves over the SmolVLA base policy and achieves the best average success rate among the compared methods. 

### **E.2 Sensitivity to Inference Budget** 

We study how the number of sampled proposals _N_ affects VGAS, using the LIBERO-Goal suite as a representative case. As shown in Fig. 6, the success rate increases monotonically with the inference budget. Starting from the base policy ( _N_ =1, 52 _._ 0%), applying Best-of- _N_ selection yields substantial gains, reaching 60 _._ 2% with only _N_ =4. This rapid improvement indicates that the proposal policy often generates high-quality “near-miss” candidates that are not selected under greedy sampling but can be reliably retrieved by our geometrically regularized critic. Beyond _N_ =8 (60 _._ 6%), the gains diminish, with only a marginal improvement at _N_ =16 (61 _._ 2%). We therefore use _N_ =8 as the default, balancing performance against inference latency in the main experiments. 

### **E.3 Additional Policy Baselines** 

Beyond the SmolVLA backbone used in our main controlled experiments, we also compare VGAS with two additional policies under the same 5-shot LIBERO setting: _π_ 0-FAST and Diffusion Policy. _π_ 0-FAST [Pertsch _et al._ , 2025] is an autoregressive action-token VLA policy that represents a continuous action chunk as a discrete token sequence and decodes the generated tokens back into continuous control. Diffusion Policy [Chi _et al._ , 2025] directly models continuous action sequences through iterative denoising. For both baselines, we follow the official implementations and use their default hyperparameter settings unless otherwise specified. 

As shown in Fig. 7, VGAS achieves the best average success rate and consistently improves over the SmolVLA base policy, showing that value-guided selection provides gains beyond the underlying VLA proposal generator. _π_ 0-FAST performs poorly in the 5-shot setting, likely due to the sensitivity of autoregressive action-token generation to token-level errors under scarce supervision. Diffusion Policy performs reasonably on LIBERO-Spatial and LIBERO-Long, but remains below VGAS on average. These results further support the effectiveness of value-guided action-chunk selection in few-shot adaptation. 

### **E.4 Scalability Across Demonstration Budgets** 

We further evaluate VGAS under different demonstration budgets to assess its scalability beyond the default 5-shot setting. As shown in Fig. 8(a), VGAS consistently improves over the BC baseline across all four LIBERO suites in the 10-shot setting. Fig. 8(b) further shows that VGAS maintains a positive improvement over BC on LIBERO-Goal across 5, 10, 20, and 30 demonstrations. 

The gains are generally larger in low-data regimes, where the base policy remains semantically plausible but geometrically under-constrained. As the number of demonstrations increases, the BC baseline becomes more accurate, reducing the potential improvement from value-guided selection. This trend is consistent with our motivation. VGAS is particularly effective in few-shot regimes where the base policy has not yet learned sufficiently precise geometric control, but still retains enough local recall to generate candidates close to successful behavior. In such cases, value-guided selection can identify a better action chunk from the candidate set. 

### **E.5 Hyperparameter Sensitivity** 

We evaluate the sensitivity of VGAS to key critic hyperparameters on LIBERO-Goal under the 5-shot setting. We conduct a controlled one-at-a-time sweep over _λ_ , _β_ , and _η_ , fixing the remaining coefficients to a common reference setting. All runs use Best-of- _N_ inference with _N_ = 8 and results are averaged over five evaluation seeds. As shown in Fig. 9, VGAS remains stable across all three sweeps. The success rate varies only mildly, with ranges of 1 _._ 80, 0 _._ 72, and 2 _._ 32 points for _λ_ , _β_ , and _η_ , respectively, and consistently stays above the BC baseline. 


Figure 8: Scalability across demonstration budgets. (a) Per-suite results under the 10-shot LIBERO setting. (b) Scaling trend on LIBEROGoal with 5, 10, 20, and 30 demonstrations. VGAS consistently improves over the BC baseline, with larger gains in lower-data regimes and gradually diminishing margins as more demonstrations are provided. 


Figure 9: Hyperparameter sensitivity on LIBERO-Goal under the 5-shot setting. We sweep one coefficient at a time: (a) _λ ∈{_ 0 _._ 5 _,_ 1 _,_ 5 _,_ 10 _}_ with _β_ = 5 _, η_ = 5; (b) _β ∈{_ 1 _,_ 5 _,_ 10 _}_ with _λ_ = 5 _, η_ = 5; and (c) _η ∈{_ 1 _,_ 2 _,_ 5 _,_ 10 _}_ with _λ_ = 5 _, β_ = 5. The green star marks the common reference setting used in this sensitivity study, and the orange dashed line denotes the BC baseline. 

