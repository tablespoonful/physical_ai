---
title: "LIDAR-AD: A Decoder-Free Latent-Interaction Dreamer with Action-Residual Chains for Autonomous Driving"
date: "2026-07-12"
authors: "Yongzhi Liu; Yang Xiao; Zhong Cao; Zeng Kang; Sunan Zhang; Zhaozhi Dong"
url: https://arxiv.org/abs/2607.11964
pdf: https://arxiv.org/pdf/2607.11964
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.11964)** / [論文ページ](https://arxiv.org/abs/2607.11964)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

1 

# LIDAR-AD: A Decoder-Free Latent-Interaction Dreamer with Action-Residual Chains for Autonomous Driving 

Yongzhi Liu, Yang Xiao, Zhong Cao, Zeng Kang, Sunan Zhang, Zhaozhi Dong, Guojun Yu, and Weichao Zhuang, _Member, IEEE_ 

**_Abstract_ —Autonomous driving requires long-horizon closedloop decision making in dynamic traffic environments. Latent world models offer an effective framework for this problem by enabling imagination-based decision making in compact latent spaces. However, multi-source observations contain controlirrelevant redundancy, whereas reliable driving decisions rely on risk-relevant relations, future dynamics, and continuous action adjustments. This mismatch makes observation reconstruction and absolute action modeling suboptimal for learning decisionrelevant latent dynamics. We propose LIDAR-AD, a decoderfree Latent-Interaction Dreamer with Action-Residual Chains for autonomous driving. LIDAR-AD replaces observation reconstruction with redundancy-reduced latent alignment, encouraging compact representations of risk-relevant relations in multi-source driving inputs. It further models vehicle control as residual action updates and uses residual-action sequence contrastive learning to align multi-step residual-driven rollouts with future latent states. A deterministic analysis shows that the latent-tanh residual parameterization preserves interior action reachability while representing smooth long-horizon control as compact local updates. Together, these designs improve risk-aware state abstraction, continuous-control modeling, and long-horizon dynamics prediction. Extensive experiments across diverse simulated driving scenarios demonstrate that LIDAR-AD consistently outperforms world-model baselines, achieving the highest reward and the best success rate among learning-based methods. Evaluations on nuPlan-derived log-reconstructed scenarios further demonstrate the transferability of LIDAR-AD under real-world traffic layouts. The project page is available at Project Website.** 

**_Index Terms_ —Autonomous driving, world model, reinforcement learning, latent representation, residual actions.** 

## I. INTRODUCTION 

**A** UTONOMOUSdynamic, interactive, and partially observable traffic envi-driving requires reliable decisions in ronments [1]. Unlike standard continuous-control benchmarks, it is a long-horizon closed-loop problem governed by safety, 

This work was supported in part by the Excellent Youth Fund Project of the Jiangsu Basic Research Program under Grant BK20250172, in part by the Major Science and Technology Special Project of Jiangsu Province under Grant BG2025018, and in part by the National Natural Science Foundation of China (NSFC) under Grant 52441204. (Corresponding author: Weichao Zhuang.) 

Yongzhi Liu, Yang Xiao, Zeng Kang, Sunan Zhang, Zhaozhi Dong, and Weichao Zhuang are with the School of Mechanical Engineering, Southeast University, Nanjing, Jiangsu 211189, China (e-mail: yongzhiliu@seu.edu.cn; wezhuang@seu.edu.cn). 

Zhong Cao is with the Department of Civil and Environmental Engineering, University of Michigan, Ann Arbor, MI 48109, USA (e-mail: zhcao@umich.edu). 

Guojun Yu is with Xheart Technology Co., Ltd., Suzhou, Jiangsu 215100, China (e-mail: gavin.yu@xheart.com). 


Fig. 1. Compactness of residual-action space in real driving data. Statistics from NAVSIM and nuPlan show that consecutive steering and longitudinal commands are strongly correlated, while their residual changes are concentrated in a much narrower range. The residual-action horizon occupies 9.1 _×_ fewer cells than the absolute-action chain, indicating a more compact geometric structure for smooth long-horizon driving control. 

efficiency, and comfort. A driving policy must reason about surrounding traffic, maintain stable vehicle-level control, and anticipate the multi-step consequences of current decisions. Small errors in state representation, action smoothness, or dynamics prediction can therefore accumulate into unsafe or inefficient behavior in dense traffic, intersections, and roundabouts. Thus, closed-loop driving requires models that extract decision-relevant structure from complex observations while preserving smooth and predictive control. 

Reinforcement learning has been widely studied for autonomous driving, but model-free policies still require extensive environment interaction, which is costly for rare safetycritical events [2]. Model-based reinforcement learning alleviates this issue by learning predictive world models that 

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

2 

reuse collected experience for imagined rollouts, from shortrollout model learning to RSSM-based latent imagination and value-aware latent planning [3]–[7]. In autonomous driving, world models have been adapted through geometric priors, semantic abstraction, safety-aware optimization, risk-aware policy coordination, decoder-free training, and generative scene evolution [8]–[15]. These studies demonstrate the value of learned latent dynamics for prediction, planning, and decision making. However, two connected issues remain insufficiently addressed for closed-loop driving. First, many world models still allocate capacity to redundant or weakly decision-relevant observations, rather than organizing latent states around interaction changes that directly affect driving decisions. Second, conventional action conditioning treats each action as an independent input, offering little structure for continuous steering and longitudinal control. As a result, the model may fail to associate small control adjustments with future state transitions, while the policy may produce unnecessary action fluctuations during closed-loop execution. 

Observation reconstruction provides dense supervision for world model learning, but it can bias the latent state toward predictable regularities that are weakly related to control. Decoder-free representation learning addresses this limitation by optimizing latent embeddings directly through predictive, contrastive, redundancy-reduction, and joint-embedding objectives [16]–[20]. These objectives have also improved reinforcement learning and latent dynamics modeling through contrastive, predictive, or augmentation-based visual control [21]–[24]. Nevertheless, most decoder-free objectives are designed for holistic inputs or augmented views, and provide limited mechanisms for modeling structured relationships among heterogeneous driving modalities. In driving sequences, many observed factors remain temporally persistent, whereas safety-critical changes often appear sparsely around interaction boundaries, such as abrupt range variations, obstacle encounters, yielding, merging, or entering a conflict region. When the objective emphasizes generic observation prediction, the model may reduce loss by modeling persistence rather than identifying interaction changes that drive future decisions. This can consume modeling capacity and weaken long-horizon closed-loop decision making. 

Another limitation lies in how closed-loop driving actions are commonly represented. Many learning-based policies output a new control command at each decision step, which gives limited structure to the temporal continuity of steering and longitudinal control. Residual reinforcement learning and smoothcontrol regularization suggest that learning local corrections or suppressing abrupt action changes can improve continuouscontrol stability [25], [26]. Recent residual-action methods further use the previous action as the reference signal, reducing the effective search space and improving long-horizon prediction or action smoothness in visual control [27], [28]. In real driving, maneuvers such as lane changes, controlled stops, and collision avoidance are rarely produced by isolated commands; instead, they are formed by gradual adjustments around previous controls. As shown in Fig. 1, our statistics on NAVSIM and nuPlan show that consecutive driving commands are highly correlated, and their residual changes occupy a much smaller 

range than the full action space. This suggests that repeatedly predicting absolute actions may introduce unnecessary modeling burden, especially when temporally redundant control patterns persist over many steps. However, a single residual action describes only a local correction. Long-horizon driving instead requires modeling how intermediate control changes accumulate into future outcomes, an abstraction also reflected in sequence-level action generation and chain-style action modeling [29], [30]. Thus, the world model should learn how successive per-step residual-action inputs shape future driving states. 

Table I summarizes the methodological position of LIDARAD relative to representative decoder-free, residual-action, and world-model baselines. In contrast to methods that address representation compactness or residual control separately, LIDAR-AD combines decoder-free representation learning, group-level observation interaction, residual-action policy parameterization, residual-aware transition modeling, and multistep action contrast within one RSSM-based framework. 

To address these challenges, this paper proposes **LIDARAD** , a decoder-free latent-interaction Dreamer with actionresidual chains for autonomous driving. The central idea is to guide the world model toward decision-relevant interaction changes and continuous control evolution, rather than treating observation modeling and action prediction as separate one-step objectives. LIDAR-AD integrates **Decoder-Free Latent Interaction Representation (DLIR)** , a **ResidualAction World Model (RAWM)** , and **Residual-Action Chain Contrastive Learning (ARC-CL)** within a unified RSSM framework. This design reduces redundant observation modeling, provides a compact action space for smooth control, and aligns multi-step residual-action rollouts with future latent states. 

The main contributions of this paper are summarized as follows: 

- **Decoder-Free Latent Interaction Representation (DLIR).** We develop a lightweight representation learner that models interactions among ego state, range sensing, and navigation signals, and aligns the RSSM latent state with an interactionaware embedding without reconstructing the full observation. 

- **Residual-Action World Model (RAWM).** We introduce a residual-action parameterization into an RSSM-based world model, where the transition is conditioned on both the executed action and the residual adjustment. A deterministic analysis characterizes command invariance, interior reachability, and local compactness under a smooth-control assumption. 

- **Residual-Action Chain Contrastive Learning (ARC-CL).** We design a multi-step contrastive objective that aligns rollouts recursively driven by per-step residual-action inputs with true future latent states, improving the world model’s ability to capture cumulative control consequences. 

The remainder of this paper is organized as follows. Section II formulates the driving problem and defines the observation, action, and latent state spaces. Section III presents the LIDAR-AD framework. Section IV describes the experimental 

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

3 

TABLE I COMPONENT-LEVEL COMPARISON WITH RELATED METHODS 

|**Method**|**Decoder-Free**|**Group Interaction**|**Residual Actor**|**Residual-Aware Transition**|**Multi-Step Action Contrast**|
|---|---|---|---|---|---|
|DreamerV3 [5]|–|–|–|–|–|
|R2-Dreamer [12]|✓|–|–|–|–|
|ResAct [27]|–|–|✓|–|–|
|ResWM [28]|–|–|✓|✓|–|
|**LIDAR-AD(Ours)**|✓|✓|✓|✓|✓|


_Note:_ ✓ indicates that the method explicitly includes the corresponding component, while – indicates that the component is not part of the original method design. 

setup, and Section IV-B reports the results. Section V discusses implications and limitations, and Section VI concludes the paper. 

## II. PROBLEM FORMULATION 

## _A. Reinforcement Learning for Autonomous Driving_ 

We formulate autonomous driving as a partially observable sequential decision-making problem. At each timestep _t_ , the agent receives an observation _ot_ , executes a continuous control action _at_ , and obtains a reward _ρt_ from the environment. The task is modeled as a partially observable Markov decision process (POMDP): 


where _O_ is the observation space, _A_ is the continuous action space, _P_ ( _ot_ +1 _| o≤t, at_ ) denotes the unknown historyconditioned transition dynamics, _R_ ( _ot, at_ ) is the reward function, and _γ ∈_ [0 _,_ 1) is the discount factor. The policy _π_ ( _at | o≤t_ ) is optimized to maximize the expected discounted return: 


Here _ρt_ = _R_ ( _ot, at_ ) denotes the realized scalar reward at timestep _t_ . In our driving setting, _at_ denotes the executed continuous control command, including longitudinal and lateral control such as acceleration and steering. The concrete observation composition, action range, reward design, and simulator configuration are reported in Section IV. 

**RSSM latent state.** Following the reconstruction-free RSSM formulation in R2-Dreamer [12], we learn compact latent dynamics for policy optimization without reconstructing raw observations. The observation history is summarized into a latent state 


where _ht_ is a deterministic recurrent state and _zt_ is a stochastic latent state. The recurrent transition summarizes historical information as 


while the stochastic state is inferred from the current observation embedding or predicted from the prior: 


Fig. 2. Feature-aware supervision allocation for multi-source latent alignment. Uniform alignment is dominated by high-dimensional LiDAR inputs, while feature-aware weighting redistributes supervision across ego-state, navigation, and LiDAR-related latent bins. 

where _et_ denotes the latent embedding of the current observation. The transition input _ξt−_ 1 is the executed action _at−_ 1 in a conventional action-conditioned RSSM; in RAWM, it is replaced by the residual-action embedding _dt−_ 1 defined in Section II-B. The learned latent state supports reward prediction, continuation prediction, imagined rollout, and actor-critic policy learning. Different from reconstruction-based world models, the representation is optimized in latent space, reducing the need to supervise every raw observation coordinate and encouraging compact task-relevant dynamics. 

Fig. 2 illustrates this modality-size-induced supervision bias. It shows why a uniform alignment objective can become LiDAR-dominated when heterogeneous modalities have substantially different input dimensions, and motivates balancing the latent supervision across compact risk and interaction cues in DLIR. 

In this work, the RSSM backbone is not redesigned. Instead, we focus on how to make its latent dynamics more suitable for autonomous driving. Specifically, the observation embedding _et_ should preserve decision-relevant interactions among heterogeneous driving cues, and the transition model should account for the temporal continuity of executed control commands. The former is addressed by the proposed latent interaction representation, while the latter motivates residualaction-aware world modeling and multi-step action-sequence consistency learning. 

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

4 

## _B. Residual Actions and Multi-Step Alignment Target_ 

Driving control is inherently continuous over time. We therefore formulate residual control as an explicit modeling variable, rather than treating it as a post-hoc difference between consecutive executed actions. Let _at−_ 1 _∈_ ( _−_ 1 _,_ 1)<sup>_d_</sup> denote the previously executed action, and let ∆ _ut ∈_ R<sup>_d_</sup> be the residual command predicted by the actor at timestep _t_ . The residual is defined in the pre-tanh action space by first mapping the previous executed action back to its unconstrained coordinate: 


where _ϵ_ is a small constant introduced for numerical stability. The current executed action is then obtained as 

residual actions enter the transition, and ARC-CL aligns multistep action effects. DLIR encodes _ot_ into _e_<sup>DLIR</sup> _t_ , from which the RSSM posterior infers _s_<sup>_q_</sup> _t_<sup>=(</sup><sup>_ht, z_</sup> _t_<sup>_q_).Conditionedon</sup> _s_<sup>_q_</sup> _t_<sup>andthepreviouspre-tanhaction,theactorpredicts∆</sup><sup>_ut_;</sup> RAWM then decodes _at_ and forms the transition input _dt_ . 

For multi-step training, ARC-CL recursively applies the same transition over ( _dt, . . . , dt_ + _K−_ 1) and aligns the final prior state with the posterior inferred from the future observation. The ordered embeddings are used only as step-wise transition inputs, not as an additional chain-level feature. Thus, the overview pipeline is 


with ARC-CL extending the last transition over _K_ steps during training. 


Here, ∆ _ut_ denotes the actor-produced residual control command, whereas _at_ is the bounded action applied to the environment. 

To describe the temporal evolution of recent control adjustments, we use an ordered residual-action sequence over a short horizon _K_ : 


where _K_ denotes the rollout horizon. This notation does not introduce a standalone feature vector for the whole chain. It only identifies the per-step executed actions and residual commands used by ARC-CL to supervise a multi-step prior rollout. 

At each transition step, the latent world model receives the executed action and the residual command at that same step: 


Thus, the RSSM transition is conditioned on per-step joint action information, not on an encoded action-chain vector. ARC-CL later aligns the _K_ -step rollout obtained by repeatedly applying this transition over _Q_<sup>_K_</sup> _t_ with the future posterior state. The detailed transition parameterization and structural properties are presented in Section III-C and Section III-D. 

## III. METHOD 

LIDAR-AD is a decoder-free latent world-model framework for closed-loop autonomous driving. It uses the RSSM state _st_ = ( _ht, zt_ ) as a common latent interface for observation abstraction, residual control, and multi-step dynamics learning. Fig. 3 shows the architecture, and the following subsections define how DLIR, RAWM, and ARC-CL constrain the shared latent dynamics. 

## _B. Decoder-Free Latent Interaction Representation_ 

DLIR replaces observation reconstruction with decoder-free latent alignment for heterogeneous driving observations. It derives a deterministic risk descriptor from structured observations and fuses it with grouped modality embeddings to form interaction-aware latent features. The resulting embedding is aligned with the RSSM posterior state by a riskweighted redundancy-reduction objective inspired by Barlow Twins [18]. For two normalized batch embeddings _Y_<sup>_A_</sup> _, Y_<sup>_B_</sup> _∈_ R<sup>_B×D_</sup> , the cross-correlation matrix is 


where _Y_<sup>˜</sup> denotes batch-normalized embeddings. Unlike the standard equal-weight formulation, DLIR uses the risk embedding to weight latent dimensions, emphasizing interactionrelevant components without decoding the latent state. **Risk-guided grouped encoding.** Let the driving observation be divided into semantic groups, 


where each group corresponds to a different type of driving information. A deterministic risk descriptor for DLIR is computed as 


where Γ( _·_ ) summarizes proximity and route-consistency cues without introducing an additional supervised prediction target. In DLIR, _gt_ is used only to guide decoder-free latent alignment. 

**Risk descriptor construction.** We decompose the descriptor into LiDAR, navigation, and ego-state components, 


## _A. Framework Overview_ 

At each timestep _t_ , the agent receives the complete driving observation _ot_ = _{x_<sup>_m_</sup> _t_<sup>_}m∈M_,where</sup><sup>_xm_</sup> _t_ denotes the _m_ -th semantic observation group and _M_ is the set of observation groups. The framework imposes three complementary constraints on the shared RSSM dynamics: DLIR selects interaction-relevant observation content, RAWM specifies how 

which correspond to environmental proximity, route constraint, and vehicle-state risk, respectively. For LiDAR-like range sensing with beam distances _{dt,i}_<sup>_N_</sup> _i_ =1<sup>_l_,theproximitycom-</sup> ponent is 


5 

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 


Fig. 3. Overall architecture of LIDAR-AD. DLIR maps heterogeneous driving observations to the shared RSSM latent state, RAWM converts actor residuals into executable actions and per-step action-change embeddings, and ARC-CL aligns recursive multi-step prior rollouts with future posterior states. 


Fig. 4. Decoder-free latent interaction representation. Grouped driving observations and the deterministic risk descriptor are encoded separately, fused through gated pairwise interactions, and aligned with the RSSM posterior state by a risk-weighted redundancy-reduction objective without observation reconstruction. 

where _σl_ controls the distance decay. This assigns larger responses to nearby obstacles and suppresses distant returns. The navigation component is 


where _e_<sup>lat</sup> _t_ is lateral route error, _e_<sup>head</sup> _t_ is heading error, and _κt_ is local route curvature. When curvature is not directly provided by the navigation interface, it is estimated from successive navigation waypoints as _κt ≈|_ ∆ _ψt_<sup>nav</sup> _|/_ ∆ _s_ . The 

ego-state component is 


where _vt_ is ego speed, _δt_ is steering command, and _a_<sup>acc</sup> _t_ is longitudinal control. Before being encoded, each block is normalized as 


and the final descriptor is 


Unless otherwise stated, we use equal weights _λl_ = _λn_ = _λe_ = 1 _/_ 3. The descriptor is not used as a reward term; DLIR encodes it to generate the latent-alignment weights in Eq. (26). 

Each observation group and the risk descriptor are encoded by lightweight encoders: 


The encoders are kept separate to preserve the different semantics and scales of kinematic, range, navigation, and riskderived signals. 

**Latent interaction fusion.** DLIR obtains an interactionaware observation embedding by modeling pairwise dependencies among grouped observation embeddings. For each pair ( _m, n_ ) _∈P_ , the interaction feature is computed as 


6 

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 


Fig. 5. DLIR risk descriptor. The deterministic descriptor combines LiDAR proximity, navigation constraint, and ego-state control-boundary cues, and is used only inside the DLIR representation objective. 

where _⊙_ denotes element-wise multiplication and _Wm,n_ is a learnable projection. A context-dependent scalar gate then modulates each pairwise interaction, 


The final DLIR embedding fuses grouped embeddings, the risk embedding, and gated interaction features: 


The RSSM posterior is then inferred from the fused embedding: 


**Risk-weighted latent alignment.** DLIR treats the RSSM posterior state and the interaction-aware observation embedding as two views of the same driving state and projects them into a common space: 


where _Ps_ and _Pe_ are lightweight projection heads. For a batch of samples, the normalized cross-correlation matrix between _yt_ and _vt_ is computed as in Eq. (10). The risk embedding produces dimension-wise alignment weights: 


where _ωi >_ 0 and _D_ <u>1</u> � _i_<sup>_ωi_=1.TheDLIRlossisthen</sup> defined as 

The first term performs risk-weighted alignment, and the second reduces redundancy between weighted dimensions. Applied to _s_<sup>_q_</sup> _t_<sup>and</sup><sup>_e_DLIR</sup> _t_ , the loss jointly regularizes grouped encoders, interaction fusion, and RSSM posterior inference. When all _ωi_ = 1, it reduces to the equal-weight BT-style objective; in DLIR, _ω_ is risk-conditioned and componentselective. 

## _C. Residual-Action World Model_ 

RAWM is an action-conditioned RSSM world model with a residual action interface. It preserves the standard decomposition into posterior inference, prior transition, and prediction heads, but injects control through a joint embedding of the executed command and its residual change. This converts the temporal correlation in Fig. 1 into an explicit representation of local action evolution. 

**Model components.** Let _A_ = ( _−_ 1 _,_ 1)<sup>_d_</sup> be the executed action space. Given the DLIR posterior state _s_<sup>_q_</sup> _t_<sup>inEq.(24),RAWM</sup> uses the following components: 

**Inv. action:** _ut−_ 1 = atanh(clip( _at−_ 1 _, −_ 1 + _ϵ,_ 1 _− ϵ_ )) _,_ 


**RSSM trans.:** _ht_ +1 = _fϕ_ ( _ht, zt, dt_ ) _,_ **Stoch. prior:** _z_ ˆ _t_ +1 _∼ pϕ_ (ˆ _zt_ +1 _| ht_ +1) _,_ (33) 


Here _ϵ_ is used only for numerical stability near the action boundary. The induced latent-tanh residual map is 


Section III-D analyzes this map; here the equations define its role in the world model. 

## _D. Structural Analysis of Latent-Tanh Residual Actions_ 

We analyze command invariance, interior reachability, and local compactness of the latent-tanh residual map in Eq. (36). The argument applies elementwise, and vector notation is used for compactness. Since tanh( _·_ ) produces open-interval actions, the analysis uses _A_ = ( _−_ 1 _,_ 1)<sup>_d_</sup> ; the clipping in Eq. (28) is only a numerical safeguard near the boundary. Unless otherwise stated, the reachability statement characterizes the parameterization itself and assumes an unrestricted latent residual. **Proposition 1 (invariance, reachability, and smoothness).** For any _at−_ 1 _∈A_ , the map in Eq. (36) satisfies three properties. First, a zero residual preserves the previous command: 


IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

7 


which gives 


Third, for small ∆ _ut_ , 


_Proof._ The invariance property follows directly from the inverse relationship between tanh( _·_ ) and atanh( _·_ ) on ( _−_ 1 _,_ 1). For any target _a_<sup>_⋆_</sup> _t ∈A_ , atanh( _a_<sup>_⋆_</sup> _t_<sup>)isfinite.Substituting</sup> Eq. (38) into the latent-tanh residual map gives Eq. (39). Finally, applying a first-order Taylor expansion of tanh( _ut−_ 1+ ∆ _ut_ ) around _ut−_ 1 = atanh( _at−_ 1) gives Eq. (40). □ 

Proposition 1 shows that zero residuals preserve the previous command, unrestricted residuals reach any interior target in one step, and small residuals induce smooth local action changes. If a bounded residual head is used in implementation, the reachability result holds for target actions whose required latent residual lies within the admissible residual range. **Comparison with a naive action-space residual.** A naive alternative is to add the residual directly to the executed action, _at_ = tanh( _at−_ 1 + ∆ _ut_ ). Although this form can cover the interior of _A_ with unbounded residuals, a zero residual gives 


Repeated zero-residual updates therefore contract each nonzero action component toward zero. In contrast, the latenttanh form applies the residual in the pre-tanh action space and preserves the executed command, which is important when maintaining the current steering or throttle is a valid driving decision. 

**Proposition 2 (local geometric compactness).** Let _cϵ_ = atanh(1 _− ϵ_ ) and _Uϵ_ = [ _−cϵ, cϵ_ ]<sup>_d_</sup> denote the numerically valid latent action domain. For a finite-domain comparison, an absolute pre-tanh parameterization treats each step as selecting a new latent action _ut ∈Uϵ_ . If a smooth driving segment satisfies _∥ut − ut−_ 1 _∥∞ ≤ δ_ with _δ ≪ cϵ_ , then the same local transition is represented by the residual ∆ _ut_ = _ut − ut−_ 1 _∈_ [ _−δ, δ_ ]<sup>_d_</sup> . The relative hypervolume of this local residual region is 


_Proof._ Since ∆ _ut_ = _ut −ut−_ 1, the smooth-control condition restricts the residual to [ _−δ, δ_ ]<sup>_d_</sup> , whose volume is (2 _δ_ )<sup>_d_</sup> . The reference latent action domain has volume (2 _cϵ_ )<sup>_d_</sup> . Taking their ratio gives Eq. (42). □ 

This ratio is a geometric proxy for the local variation represented under the smooth-control assumption, not an actionspace restriction, because Proposition 1 preserves one-step interior reachability. 

**Corollary 1 (long-horizon residual chains).** Over a horizon of _K_ steps, residuals accumulate linearly in latent action space: 


If the smoothness condition holds at each step, the residual sequence lies in [ _−δ, δ_ ]<sup>_Kd_</sup> , whereas an unconstrained absoluteaction sequence lies in _Uϵ_<sup>_K_.Theirrelativehypervolumeis</sup> 


Thus, under a smooth-control assumption, coherent maneuvers can be described by compact residual chains while decoded commands remain in the original tanh action space. This view is consistent with Fig. 1, where residual-action chains occupy 9.1 _×_ fewer cells than absolute-action chains. 

## _E. Residual-Action Chain Contrastive Learning_ 

ARC-CL regularizes the world model with a contrastive objective on multi-step rollouts driven by successive joint action embeddings, as shown in Fig. 6. 

For a horizon _K_ , ARC-CL uses the ordered list of per-step joint action embeddings 


The predicted future state is _s_ ˆ<sup>_p_</sup> _t_ + _K_<sup>.Thelist</sup><sup>_D_</sup> _t_<sup>_K_</sup> specifies recursive rollout inputs only; it is not compressed into a chainlevel feature or fed to the transition as a single input. The rollout uses prior dynamics and per-step action embeddings without future observations. For world-model and ARC-CL training, each _dt_ + _k_ is constructed from the replayed action _at_ + _k_ and residual command ∆ _ut_ + _k_ produced by the behavior actor. It is not recomputed with the current actor, keeping the action embedding consistent with the realized replay transition. 

The predicted future state _s_ ˆ<sup>_p_</sup> _t_ + _K_<sup>isalignedwiththefuture</sup> posterior _s_<sup>_q_</sup> _t_ + _K_<sup>throughInfoNCE[16].Forabatch</sup><sup>_B_,define</sup> 


Positive pairs use _b_<sup>_′_</sup> = _b_ , and negatives use other trajectory segments. The contrastive loss is 


Here sim( _·, ·_ ) is cosine similarity and _τ_ is a temperature. The loss updates _Tϕ_ , _E_ act, and DLIR through _st_<sup>_q_;theresidual</sup> policy is updated separately by the latent actor objective during imagined rollouts. 

## _F. Optimization and Policy Learning_ 

The world model is trained with task prediction, RSSM regularization, decoder-free representation learning, and multistep action contrast: 


IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

8 


Fig. 6. Residual-action chain contrast. Starting from the shared posterior state, the transition model is recursively applied with one joint action embedding at each step, and the final predicted latent state is aligned with the true future posterior by InfoNCE. 

The reward and continuation heads are trained by negative log likelihood, while the two RSSM regularizers are 


The proposed losses act on the same posterior and prior states as the RSSM terms, enforcing compactness and multi-step predictive consistency in one latent space. 

**Latent actor-critic learning.** Following Dreamer-style latent imagination [5], [31], the actor and critic are optimized on trajectories generated by the learned world model. Imagined rollouts start from replay posterior states and use the residual action recursion in Eqs. (29), (30), and (31). The critic and actor objectives are 


where _Gt_ + _k_ = _vψ_ (ˆ _st_ + _k_ ) + _η H_ ( _πθ_ ( _· | s_ ˆ _t_ + _k, ut_ + _k−_ 1)). During imagination, _ut_ + _k_ = _ut_ + _k−_ 1+∆ _ut_ + _k_ is updated together with the latent state. 

**Training procedure.** Algorithm 1 summarizes data collection, world-model learning, and latent actor-critic optimization. The LIDAR-AD replay buffer stores the shared environment tuple ( _ot, at, ρt, ct_ ) and additionally records the actor-produced residual ∆ _ut_ required by RAWM and ARC-CL. During worldmodel and ARC-CL updates, ∆ _ut_ is read from replay rather than recomputed by the current actor. Non-residual baselines 

- **Algorithm 1** LIDAR-AD Training Procedure 

- **Require:** Environment, ARC-CL rollout horizon _K_ , imagination horizon _H_ imag, training steps _N_ . 

- 1: Initialize world model _ϕ_ , DLIR encoders, action encoder _E_ act, actor _θ_ , critic _ψ_ , and replay buffer _D_ . 

- 2: Set _a−_ 1 _←_ **0** and _s_ 0 _←_ **0** . 

- 3: **for** _n_ = 1 to _N_ **do** 

- 4: Observe _ot_ = ( _x_<sup>ego</sup> _t , x_<sup>lidar</sup> _t , x_<sup>nav</sup> _t_ ). 5: Compute _e_<sup>DLIR</sup> _t_ with DLIR and infer _s_<sup>_q_</sup> _t_<sup>byEq.(24).</sup> 6: Compute _ut−_ 1 by Eq. (28); sample ∆ _ut ∼ πθ_ ( _· | s_<sup>_q_</sup> _t_<sup>_, ut−_1).</sup> 

- 7: Compute _ut_ = _ut−_ 1 +∆ _ut_ and _at_ = tanh( _ut_ ); execute _at_ and receive reward _ρt_ . 

- 8: Store ( _ot, at,_ ∆ _ut, ρt, ct_ ) in _D_ . 

- 9: **if** _D_ has enough sequences **then** 

- 10: Sample a trajectory batch, including stored ( _at,_ ∆ _ut_ ), and infer posterior states _{s_<sup>_q_</sup> _t_<sup>_}_.</sup> 

- 11: Construct _dt_ = _E_ act([ _at_ ; ∆ _ut_ ]) from replayed actions and residuals; update RSSM priors with _Tϕ_ ( _st, dt_ ). 

- 12: Run _K_ -step prior rollouts using the ordered per-step embeddings _Dt_<sup>_K_; compute</sup><sup>_L_DLIR,</sup><sup>_L_ARC, and</sup><sup>_L_WM.</sup> 

- 13: Update world-model parameters by minimizing _L_ WM. 

- 14: Roll out imagined trajectories from replay posterior states using the residual actor. 

- 15: Update critic with Eq. (52) and actor with Eq. (53). 

- 16: **end if** 

17: **end for** 

18: **return** Trained world model, actor, and critic. 

store only the standard transition tuple under the same observation interface, action space, reward function, data budget, and evaluation protocol. 

## IV. EXPERIMENTAL EVALUATION 

## _A. Experiment Setup_ 

_1) Simulation Environment:_ We use MetaDrive [32] as the unified closed-loop simulation interface for both procedurally generated scenarios and real-world log-based scenarios. MetaDrive provides controllable road generation, traffic density, vehicle dynamics, and LiDAR-like range observations, enabling controlled evaluation under diverse geometry and interaction patterns. To evaluate transfer under real-world traffic layouts, nuPlan logs [33] are converted into MetaDrive-compatible scenarios through the official ScenarioNet middleware [34]. This setting allows policies trained and evaluated in a unified simulator interface to be tested on log-reconstructed urban scenarios, but it is not the official nuPlan closed-loop protocol and does not report official nuPlan planning metrics. Fig. 7 shows representative road blocks and composed routes used for scenario randomization. 

Each observation consists of ego-vehicle state, LiDARlike range sensing, and navigation information. The same observation interface is used for all learning-based methods to 

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

9 


Fig. 7. Scenario generation in MetaDrive. Elementary road blocks are randomly composed into mixed driving routes, enabling evaluation across diverse intersections, roundabouts, curves, and multi-road layouts under a unified closed-loop simulator interface. 

ensure a controlled comparison across algorithms and datasets. The action is a two-dimensional continuous command, 


where _a_ acc denotes normalized longitudinal control and _a_ steer denotes normalized steering control. For LIDAR-AD, this executed action is generated by the latent-tanh residual action parameterization in Section III-C. 

**Reward design.** The closed-loop reward follows the standard driving objective used in the simulator and is kept identical for all methods. At each step, the scalar reward is composed of route progress, speed incentive, goal completion, and safety penalties: 


where ∆ _lt_ is route progress, _v_ ¯ _t_ is normalized speed, and Igoal, Icol, and Ioff indicate goal arrival, collision, and offroad events, respectively. The coefficients are fixed across all methods, so the reported episode reward is directly comparable. 

_2) Baselines and Evaluation Metrics:_ **Baselines.** We compare LIDAR-AD with the following rule-based, model-free, and model-based methods: 

- **IDM+MOBIL** : a non-learning control baseline that combines the Intelligent Driver Model [35] with the MOBIL lane-change rule [36]. 

- **SAC** [37]: a model-free off-policy RL algorithm for continuous control. 

- **PPO** [38]: a model-free on-policy RL algorithm with a clipped policy update. 

- **DreamerV3** [5]: the standard RSSM-based latent worldmodel baseline. 

- **R2-Dreamer** [12]: a decoder-free world-model baseline and the closest reference to our representation-learning setting. 

All learning-based baselines use the same observation interface, action space, reward, and evaluation budget as LIDARAD. Module ablations are reported separately in Section IV-B to isolate the contributions of DLIR, ResAct, RAWM, and ARC-CL. 

**Evaluation metrics.** We report only metrics used in the quantitative results. For compact table presentation, each metric is first introduced by its full name followed by the abbreviation used in the tables: 

- **Reward (RW)** : the undiscounted episode return under Eq. (55). 

- **Success rate (SR)** : the percentage of episodes that reach the navigation goal without collision or off-road termination. 

- **Route completion (RC)** : the percentage of the planned route completed before termination. 

- **Average speed (AS)** : the mean driving speed over an episode, used to measure driving efficiency. 

- **Steering delta (SD)** and **longitudinal-control delta (LCD)** : the mean absolute change between consecutive steering or longitudinal commands, used to measure control smoothness. 

- **Normalized AUC at 1M steps (nAUC@1M)** : the normalized area under the training curve over the first one million environment steps, used for sample-efficiency comparison in ablations. 

_3) Implementation Details:_ LIDAR-AD is implemented in PyTorch with an RSSM backbone following the DreamerV3 training paradigm. Compared with DreamerV3, LIDAR-AD replaces the reconstruction-based observation encoder with DLIR, conditions the RSSM transition on the RAWM joint action embedding _dt_ , and adds ARC-CL to the world-model objective. The DLIR risk descriptor _gt_ is deterministically computed from structured driving observations as in Eqs. (13)– (18). The residual actor predicts ∆ _ut_ in the pre-tanh action space, and the action embedding network receives [ _at_ ; ∆ _ut_ ] at each transition step. The ARC-CL rollout horizon is set to _K_ = 10 unless otherwise stated. All methods are trained with Adam under matched compute and data budgets. For real-time feasibility checking, the trained policy is also deployed on an instrumented vehicle platform for inference-time testing, as shown in Fig. 8. This deployment is used only to examine execution feasibility on physical hardware; all closed-loop driving performance metrics reported below are obtained from the simulator and nuPlan-derived scenarios. 

_4) Experiment Settings:_ Training is conducted on randomized MetaDrive maps with varying road layouts and traffic configurations at the nominal traffic density of 0.20. Evaluation is performed on four representative scenario sets used in the main results: mixed scene, roundabout, T-intersection, and nuPlan-derived log-reconstructed scenarios imported through ScenarioNet. To evaluate traffic-density generalization from this nominal setting, we additionally test mixed, T-intersection, and roundabout scenarios at densities of 0.10, 0.20, and 0.30. All learned methods are trained and evaluated under the same data-collection budget and randomization protocol. Unless otherwise stated, results are reported as mean _±_ standard deviation across _N_ run independent training runs; each trained 

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

10 

TABLE II 

OVERALL DRIVING PERFORMANCE ACROSS METADRIVE AND NUPLAN-DERIVED SCENARIOS 

|**Method**|**Mixed **|**Scene**|**Rounda**|**bout**|**T-Interse**|**ction**|**nuPlan-**|**Derived**|
|---|---|---|---|---|---|---|---|---|
||RW _↑_|SR (%) _↑_|RW _↑_|SR (%) _↑_|RW _↑_|SR (%) _↑_|RW _↑_|SR (%) _↑_|
|IDM+MOBIL [35], [36]|_−_259_._01_±_0_._00|49_._42_±_0_._00|_−_245_._00_±_6_._00|10_._77_±_0_._25|_−_276_._00_±_8_._00|20_._67_±_0_._45|122_._41_±_10_._44|**99**_._**07**_±_**1**_._**42**|
|SAC [37]|420_._99_±_43_._93|27_._20_±_9_._17|454_._99_±_36_._14|73_._40_±_6_._75|384_._99_±_41_._09|79_._40_±_8_._74|194_._69_±_12_._28|84_._33_±_1_._67|
|PPO [38]|136_._42_±_10_._35|6_._26_±_3_._12|151_._42_±_8_._51|18_._66_±_2_._30|120_._42_±_9_._68|14_._16_±_2_._97|146_._23_±_38_._15|85_._00_±_5_._40|
|DreamerV3 [5]|802_._48_±_109_._65|85_._75_±_4_._68|836_._48_±_85_._05|85_._64_±_0_._83|768_._48_±_96_._69|81_._64_±_1_._07|207_._30_±_8_._20|87_._30_±_6_._40|
|R2-Dreamer [12]|861_._14_±_66_._20|90_._38_±_5_._37|895_._14_±_51_._35|91_._78_±_3_._73|827_._14_±_58_._38|88_._18_±_4_._82|233_._24_±_12_._28|91_._27_±_1_._67|
|**LIDAR-AD (Ours)**|**936**_._**41**_±_**21**_._**04**|**94**_._**80**_±_**3**_._**90**|**967**_._**41**_±_**17**_._**31**|**94**_._**46**_±_**2**_._**26**|**919**_._**41**_±_**19**_._**68**|**92**_._**36**_±_**2**_._**93**|**259**_._**74**_±_**9**_._**21**|97_._60_±_3_._20|


_Note:_ RW, reward; SR, success rate. All values are reported as mean _±_ standard deviation over _N_ run independent training runs. 


Fig. 8. Vehicle platform for real-time feasibility testing. The trained policy is deployed on an instrumented vehicle platform to examine inference-time execution on physical hardware, while quantitative closed-loop evaluation is conducted in MetaDrive and nuPlan-derived scenarios. 

policy is evaluated on the same fixed set of evaluation episodes for the corresponding scenario. 

## _B. Experimental Results_ 

_1) Overall Closed-Loop Performance:_ Table II reports closed-loop performance on mixed scene, roundabout, T- intersection, and nuPlan-derived log-reconstructed scenarios. LIDAR-AD achieves the highest reward in all scenarios and the highest success rate among learning-based methods. Relative to R2-Dreamer, it improves success rate by 4.42, 2.68, 4.18, and 6.33 percentage points on mixed scene, roundabout, T-intersection, and nuPlan-derived scenarios, respectively, increasing the average success rate from 90.40% to 94.81%. Although IDM obtains a slightly higher success rate on nuPlanderived scenarios, its substantially lower reward indicates more conservative behavior. These results show that LIDAR-AD improves task completion while preserving closed-loop driving efficiency. 

_2) Learning Efficiency and Stability:_ Fig. 9 compares training dynamics on the mixed MetaDrive scenario. Under the same data budget, LIDAR-AD reaches higher return and success levels with lower variance than the strongest world-model baselines, indicating improved learning stability in addition to final closed-loop performance. 

_3) Module Contributions:_ Table III isolates the contribution of each module on the mixed MetaDrive scenario by removing one component from the full model at a time, and Fig. 10 provides a visual summary. Removing DLIR reduces reward, success rate, route completion, control smoothness, and sample efficiency, showing the value of decoder-free latent interaction 


Fig. 9. Training curves on the mixed MetaDrive scenario. LIDAR-AD reaches higher return and success levels with lower variance than the strongest worldmodel baselines, indicating improved learning stability under the same data budget. 


Fig. 10. Ablation performance spectrum. The visualization summarizes the complementary effects of DLIR, ResAct, RAWM, and ARC-CL across driving performance, control smoothness, and sample efficiency. 

learning for state abstraction. Removing ResAct produces the largest increase in steering and longitudinal-control deltas, while removing the RAWM embedding lowers task performance, indicating that smooth residual actions and residualaware transitions provide complementary benefits. Removing ARC-CL has smaller effects on control deltas but reduces reward, success rate, and route completion, showing that the multi-step contrastive objective mainly improves task completion and rollout consistency. The full LIDAR-AD obtains the best reward, success rate, route completion, average speed, and steering smoothness. 

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

11 

TABLE III 

MODULE ABLATION STUDY ON THE MIXED METADRIVE SCENARIO 

|**Method**|**RW** _↑_|**SR (%)** _↑_|**RC (%)** _↑_|**AS** _↑_|**SD** _↓_|**LCD** _↓_<br>**nAUC@1M** _↑_|
|---|---|---|---|---|---|---|
|LIDAR-AD w/o DLIR|901_._73_±_37_._82|91_._46_±_3_._28|96_._72_±_1_._31|28_._86_±_0_._74|0_._047_±_0_._007|0_._058_±_0_._008 0_._812_±_0_._013|
|LIDAR-AD w/o ResAct|895_._62_±_42_._38|90_._73_±_3_._92|96_._41_±_1_._42|28_._94_±_0_._87|0_._057_±_0_._009|0_._071_±_0_._010 0_._781_±_0_._015|
|LIDAR-AD w/o RAWM Emb.|908_._46_±_34_._51|91_._88_±_3_._41|96_._95_±_1_._18|28_._57_±_0_._69|0_._043_±_0_._006|0_._059_±_0_._008 0_._818_±_0_._012|
|LIDAR-AD w/o ARC-CL|914_._87_±_28_._53|92_._13_±_1_._86|97_._18_±_0_._97|28_._41_±_0_._61|0_._041_±_0_._005|0_._052_±_0_._006 0_._829_±_0_._009|
|**LIDAR-AD (Ours)**|**936**_._**41**_±_**21**_._**04 **|**94**_._**80**_±_**3**_._**90 **|**98**_._**20**_±_**0**_._**72 **|**30**_._**02**_±_**0**_._**23 **|**0**_._**035**_±_**0**_._**004**|0_._051_±_0_._007 0_._832_±_0_._011|


_Note:_ Each row removes one component from the full LIDAR-AD model. ResAct denotes latent-tanh residual action parameterization, and RAWM Emb. denotes the residual-action-aware world-model embedding. RW, reward; SR, success rate; RC, route completion; AS, average speed; SD, steering delta; LCD, longitudinal-control delta; nAUC@1M, normalized AUC at 1M steps. All values are reported as mean _±_ standard deviation over _N_ run independent training runs. 


Fig. 11. Effect of the ARC-CL rollout horizon. A ten-step horizon provides the best aggregate driving performance and the smoothest control among the evaluated settings. 

_4) ARC-CL Horizon Sensitivity:_ Fig. 11 examines the rollout horizon used by ARC-CL while keeping the remaining components fixed. Among the evaluated horizons, _K_ = 10 achieves the best aggregate profile, with the highest reward, success rate, route completion, and average speed, as well as the lowest steering and longitudinal-control deltas. A onestep objective provides limited temporal supervision, whereas _K_ = 15 slightly weakens driving performance and control smoothness. We therefore use _K_ = 10 by default to balance multi-step control modeling and rollout error accumulation. 

_5) Traffic-Density Generalization from the Nominal Density:_ Table IV evaluates traffic-density generalization by training at the nominal density of 0.20 and testing mixed, T- intersection, and roundabout scenarios at densities of 0.10, 0.20, and 0.30. All methods degrade as density increases, confirming that dense traffic is a harder closed-loop decision problem. LIDAR-AD nevertheless achieves the highest success rate and route completion across all scenario-density pairs. At density 0.30, it maintains success rates of 89.21%, 89.92%, and 88.18% in mixed, T-intersection, and roundabout scenarios, whereas R2-Dreamer drops to 72.20%, 80.18%, and 80.72%. Together with Fig. 12, these results indicate improved robustness under high-variation traffic flow rather than only 

fitting the nominal training density. 

## V. DISCUSSION 

## _A. Mechanistic Interpretation_ 

The experimental results support the central design principle of LIDAR-AD: representation learning, residual control, and multi-step dynamics alignment should be optimized around the same RSSM latent state _st_ = ( _ht, zt_ ). Across mixed scene, roundabout, T-intersection, and nuPlan-derived log-reconstructed scenarios, LIDAR-AD improves the average success rate from 90.40% for R2-Dreamer to 94.81%, while achieving the highest reward in every scenario. The component-removal ablation further shows that these gains do not come from a single isolated component. Removing DLIR, ResAct, RAWM embedding, or ARC-CL consistently weakens at least one part of the performance profile, indicating that compact representation learning, residual control parameterization, action-aware dynamics, and multi-step rollout alignment provide complementary support for closed-loop driving. 

Fig. 13 provides a representation-level explanation for the performance gains. Compared with reconstruction-based latent learning, the risk-guided decoder-free alignment produces a more diagonal cross-correlation pattern, indicating lower interdimensional redundancy. This supports the role of DLIR as a capacity-allocation mechanism: the latent state is encouraged to preserve compact driving-relevant structure while avoiding supervision that scales mainly with raw modality size. 

Fig. 14 links the ablation evidence on steering and longitudinal deltas to actual control profiles. The residual-action policy produces smoother temporal evolution than absolute-action modeling, which is consistent with the lower action deltas observed after introducing ResAct and RAWM. Fig. 16 further suggests how this control regularity translates into closed-loop behavior: LIDAR-AD follows curved and roundabout routes more consistently, while the baselines show larger lateral deviations. Together, these qualitative analyses explain why the quantitative gains appear simultaneously in success rate, route completion, reward, and traffic-density robustness. 

## _B. Implications for Structured and Temporal Knowledge Learning_ 

From a structured knowledge representation perspective, DLIR addresses the challenge of organizing heterogeneous 

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

12 

TABLE IV 

TRAFFIC-DENSITY GENERALIZATION ACROSS METADRIVE SCENARIOS 

|**Scenario**|**Density**|**Dreame**|**rV3** [5]|**R2-Drea**|**mer** [12]|**LIDAR-A**|**D (Ours)**|
|---|---|---|---|---|---|---|---|
|||SR (%) _↑_|RC (%) _↑_|SR (%) _↑_|RC (%) _↑_|SR (%) _↑_|RC (%) _↑_|
||0_._10|90_._34_±_2_._48|96_._18_±_1_._35|92_._16_±_1_._92|97_._02_±_1_._11|**96**_._**42**_±_**0**_._**46 **|**99**_._**05**_±_**0**_._**38**|
|Mixed|0_._20<br>0_._30|85_._75_±_4_._68 <br>73_._95_±_4_._52|94_._11_±_2_._06 <br> 91_._26_±_2_._84|90_._38_±_5_._37 <br> 72_._20_±_3_._74|95_._63_±_1_._58 <br> 91_._88_±_2_._41|**94**_._**80**_±_**3**_._**90 **<br> **89**_._**21**_±_**0**_._**96 **|**98**_._**20**_±_**0**_._**72**<br> **96**_._**42**_±_**0**_._**69**|
||0_._10|90_._26_±_3_._06|95_._74_±_1_._54|93_._05_±_2_._15|97_._15_±_0_._96|**97**_._**08**_±_**0**_._**64 **|**99**_._**21**_±_**0**_._**31**|
|T-Intersection|0_._20|85_._64_±_0_._83|93_._82_±_1_._03|91_._78_±_3_._73|96_._11_±_1_._42|**94**_._**46**_±_**2**_._**26 **|**98**_._**37**_±_**0**_._**64**|
||0_._30|73_._52_±_4_._88|90_._74_±_2_._76|80_._18_±_3_._96|93_._48_±_2_._13|**89**_._**92**_±_**1**_._**05 **|**96**_._**85**_±_**0**_._**73**|
||0_._10|89_._84_±_4_._15|95_._36_±_1_._91|93_._68_±_3_._28|97_._31_±_1_._36|**98**_._**35**_±_**0**_._**93 **|**99**_._**42**_±_**0**_._**27**|
|Roundabout|0_._20<br>0_._30|81_._64_±_1_._07 <br>73_._28_±_6_._72|92_._48_±_1_._46 <br> 90_._22_±_3_._18|88_._18_±_4_._82 <br> 80_._72_±_5_._67|95_._04_±_1_._72 <br> 93_._12_±_2_._38|**92**_._**36**_±_**2**_._**93 **<br> **88**_._**18**_±_**1**_._**94 **|**97**_._**71**_±_**0**_._**81**<br> **95**_._**16**_±_**0**_._**92**|


_Note:_ SR, success rate; RC, route completion. All values are reported as mean _±_ standard deviation over _N_ run independent training runs. 

driving observations into a compact latent state. Ego kinematics, LiDAR-like range sensing, navigation context, and risk descriptors differ in scale, temporal behavior, and relevance to control. By encoding these groups separately, modeling pairwise interactions, and reducing latent redundancy without observation reconstruction, DLIR provides a structured route for fusing heterogeneous data into a decision-oriented representation. This allows the world model to organize heterogeneous driving signals into a compact control-relevant latent space without forcing the representation to reconstruct every observation detail. 

From a temporal knowledge learning perspective, RAWM and ARC-CL make action evolution part of the learned dynamics rather than treating each command as an independent absolute value. RAWM supplies the transition model with both the executed command and its local residual change, while ARC-CL aligns the future state reached by recursively applying a sequence of residual-action embeddings. This differs from single-step temporal contrastive learning such as CPC [16]: the contrastive target is the latent state reached after a control sequence, not merely the next observation or next latent state. For autonomous driving, this means the model 

is encouraged to distinguish action sequences that lead to different maneuver-level consequences, such as stable lane following, route deviation, or gap acceptance. 

Fig. 15 provides a complementary policy-level diagnostic of the learned world model. Across both driving layouts, LIDAR-AD concentrates saliency around the ego-relevant lane corridor, nearby agents, and conflict regions, whereas R2Dreamer and DreamerV3 show more diffuse or spatially shifted responses. This pattern is consistent with the intended role of DLIR and RAWM: the latent state is guided toward interaction and residual-control cues that directly affect the imagined transition and policy update. It helps explain why LIDAR-AD improves over other world-model baselines in closed-loop reward, success rate, and density generalization. 

## _C. Limitations and Future Directions_ 

The present evaluation is still bounded by simulator-based closed-loop testing and nuPlan-derived scenarios, which cannot fully reproduce real sensor noise, calibration error, weather variation, localization drift, or vehicle dynamics. LIDAR-AD also uses a fixed ARC-CL horizon of _K_ = 10, pairwise modality interactions, and compact LiDAR-like observations, 


Fig. 12. Traffic-density stress test. The grouped performance bars summarize mixed, T-intersection, and roundabout scenarios evaluated at traffic densities of 0.10, 0.20, and 0.30 after training at the nominal density of 0.20, where LIDAR-AD (Ours) maintains higher success rate and route completion than DreamerV3 and R2-Dreamer. 

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

13 


Fig. 13. Latent representation structure. Cross-correlation matrices show that risk-guided decoder-free alignment reduces off-diagonal correlations, indicating a more compact latent representation for world-model learning. 

leaving adaptive horizon selection, higher-order interaction modeling, and extension to denser sensing streams as natural next steps. Finally, although the method improves reward, success rate, route completion, and control smoothness, it does not yet impose explicit safety constraints inside latent imagination; future work should therefore prioritize real-world closed-loop validation and safety-aware latent planning. 

## VI. CONCLUSION 

This paper has presented **LIDAR-AD** , a decoder-free latentinteraction dreamer world model with residual-action rollout alignment for autonomous driving in simulated environments. LIDAR-AD addresses three fundamental limitations of existing world model approaches to autonomous driving: 

- 1) The inefficiency of full observation reconstruction for heterogeneous driving modalities, addressed by the **DecoderFree Latent Interaction Representation (DLIR)** module, 


Fig. 14. Temporal control profiles. Compared with absolute-action modeling, residual-action modeling produces smoother control evolution, consistent with the smooth-control bias introduced by RAWM. 


Fig. 15. Policy saliency over bird’s-eye-view driving layouts. The BEV column shows the scene layout, while warmer regions indicate higher policy saliency for each world-model policy. Compared with R2-Dreamer and DreamerV3, LIDAR-AD produces more localized responses around egorelevant lane and interaction regions, suggesting stronger alignment between the learned latent dynamics and control-relevant cues. 


Fig. 16. Representative closed-loop trajectories. LIDAR-AD follows the reference route more consistently through curved and roundabout segments, while the baselines show larger lateral deviations. 

which learns compact latent states through risk-guided grouped encoding, structured pairwise interaction modeling, and redundancy reduction—without requiring an observation decoder. 

- 2) The lack of temporal continuity in absolute action prediction, addressed by the **Residual-Action World Model (RAWM)** , which uses latent-tanh residual actions to preserve interior action reachability, keep zero-residual commands invariant, and enrich the dynamics transition with joint action context. 

- 3) The inability to capture cumulative consequences of continuous action sequences, addressed by **Residual-Action Chain Contrastive Learning (ARC-CL)** , which aligns multi-step prior rollouts recursively driven by per-step residual-action inputs with true future posterior states. 

These three modules operate on a shared RSSM latent state _st_ , forming a tightly integrated system where improvements in representation, control, and dynamics prediction mutually reinforce each other. The residual-action statistics in Fig. 1 and the latent-tanh analysis further characterize why RAWM can express smooth control as compact residual updates without 

IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING 

14 

restricting the interior executable action range. 

Experiments on mixed scene, roundabout, T-intersection, and nuPlan-derived log-reconstructed scenarios show that LIDAR-AD achieves the highest reward in all scenarios and the best success rate among learning-based methods. Its average success rate reaches 94.81%, compared with 90.40% for R2-Dreamer and 85.08% for DreamerV3. These results indicate that the proposed risk-guided representation, residualaction modeling, and multi-step residual-action contrastive objective provide complementary benefits under a unified world-model framework. 

Future work will prioritize real-world closed-loop validation and adaptive, safety-aware latent planning. 

## REFERENCES 

- [1] B. Paden, M. C´ap, S. Z. Yong, D. Yershov, and E. Frazzoli, “A survey of<sup>ˇ</sup> motion planning and control techniques for self-driving urban vehicles,” _IEEE Trans. Intell. Veh._ , vol. 1, no. 1, pp. 33–55, 2016. 

- [2] B. R. Kiran, I. Sobh, V. Talpaert, P. Mannion, A. A. A. Sallab, S. Yogamani, and P. Perez, “Deep reinforcement learning for autonomous driving: A survey,” _IEEE Trans. Intell. Transp. Syst._ , vol. 23, no. 6, pp. 4909–4926, 2022. 

- [3] M. Janner, J. Fu, M. Zhang, and S. Levine, “When to trust your model: Model-based policy optimization,” in _Adv. Neural Inf. Process. Syst. (NeurIPS)_ , 2019, pp. 12 519–12 530. 

- [4] D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson, “Learning latent dynamics for planning from pixels,” in _Proc. Int. Conf. Mach. Learn. (ICML)_ , 2019, pp. 2555–2565. 

- [5] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse domains through world models,” _arXiv preprint arXiv:2301.04104_ , 2023. 

- [6] N. A. Hansen, H. Su, and X. Wang, “Temporal difference learning for model predictive control,” in _Proc. Int. Conf. Mach. Learn. (ICML)_ , ser. Proc. Mach. Learn. Res., vol. 162, 2022, pp. 8387–8406. 

- [7] N. A. Hansen, H. Su, and X. Wang, “TD-MPC2: Scalable, robust world models for continuous control,” in _Proc. Int. Conf. Learn. Representations (ICLR)_ , 2024. 

- [8] A. Hu, G. Corrado, N. Griffiths, Z. Murez, C. Gurau, H. Yeo, A. Kendall, R. Cipolla, and J. Shotton, “Model-based imitation learning for urban driving,” in _Adv. Neural Inf. Process. Syst. (NeurIPS)_ , 2022. 

- [9] Z. Gao, Y. Mu, C. Chen, J. Duan, P. Luo, Y. Lu, and S. E. Li, “Enhance sample efficiency and robustness of end-to-end urban autonomous driving via semantic masked world model,” _IEEE Trans. Intell. Transp. Syst._ , vol. 25, no. 6, pp. 5678–5692, 2024. 

- [10] W. Huang, J. Ji, C. Xia, B. Zhang, and Y. Yang, “Safedreamer: Safe reinforcement learning with world models,” in _Proc. Int. Conf. Learn. Representations (ICLR)_ , 2024. 

- [11] Y. Liu, S. Zhang, C. Shen, X. Zhang, and W. Zhuang, “Risk-aware dual-policy coordination with world model for safe and adaptive highway autonomous driving,” in _Proc. IEEE Intell. Transp. Syst. Conf. (ITSC)_ , Gold Coast, Australia, Nov. 2025, pp. 776–782, doi: 10.1109/ITSC60802.2025.11423709. 

- [12] N. Morihira, A. Nahar, H. Bharadwaj, Y. Kato, A. Hayashi, and T. Harada, “R2-Dreamer: Redundancy-reduced world models without decoders or augmentation,” in _Proc. Int. Conf. Learn. Representations (ICLR)_ , 2026, arXiv:2603.18202. 

- [13] Q. Li, X. Jia, S. Wang, and J. Yan, “Think2Drive: Efficient reinforcement learning by thinking in latent world model for quasi-realistic autonomous driving,” in _Proc. Eur. Conf. Comput. Vis. (ECCV)_ , 2024. 

- [14] X. Wang, Z. Zhu, G. Huang, X. Chen, J. Zhu, and J. Lu, “DriveDreamer: Towards real-world-driven world models for autonomous driving,” in _Proc. Eur. Conf. Comput. Vis. (ECCV)_ , 2024. 

- [15] W. Zheng, R. Song, X. Guo, C. Zhang, and L. Chen, “GenAD: Generative end-to-end autonomous driving,” in _Proc. Eur. Conf. Comput. Vis. (ECCV)_ , 2024. 

- [16] A. van den Oord, Y. Li, and O. Vinyals, “Representation learning with contrastive predictive coding,” _arXiv preprint arXiv:1807.03748_ , 2018. 

- [17] J.-B. Grill, F. Strub, F. Altche, C. Tallec, P. H. Richemond, E. Buchatskaya, C. Doersch, B. A. Pires, Z. D. Guo, M. G. Azar, B. Piot, K. Kavukcuoglu, R. Munos, and M. Valko, “Bootstrap your own latent: A new approach to self-supervised learning,” in _Adv. Neural Inf. Process. Syst. (NeurIPS)_ , vol. 33, 2020, pp. 21 271–21 284. 

- [18] J. Zbontar, L. Jing, I. Misra, Y. LeCun, and S. Deny, “Barlow twins: Self-supervised learning via redundancy reduction,” in _Proc. Int. Conf. Mach. Learn. (ICML)_ , ser. Proc. Mach. Learn. Res., vol. 139, 2021, pp. 12 310–12 320. 

- [19] M. Assran, Q. Duval, I. Misra, P. Bojanowski, P. Vincent, M. Rabbat, Y. LeCun, and N. Ballas, “Self-supervised learning from images with a joint-embedding predictive architecture,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , 2023, pp. 15 619–15 629. 

- [20] A. Bardes, Q. Garrido, J. Ponce, X. Chen, M. Rabbat, Y. LeCun, M. Assran, and N. Ballas, “Revisiting feature prediction for learning visual representations from video,” _arXiv preprint arXiv:2404.08471_ , 2024, v-JEPA. 

- [21] M. Laskin, A. Srinivas, and P. Abbeel, “CURL: Contrastive unsupervised representations for reinforcement learning,” in _Proc. Int. Conf. Mach. Learn. (ICML)_ , ser. Proc. Mach. Learn. Res., vol. 119, 2020, pp. 5639– 5650. 

- [22] M. Schwarzer, A. Anand, R. Goel, R. D. Hjelm, A. Courville, and P. Bachman, “Data-efficient reinforcement learning with self-predictive representations,” in _Proc. Int. Conf. Learn. Representations (ICLR)_ , 2021. 

- [23] D. Yarats, I. Kostrikov, and R. Fergus, “Image augmentation is all you need: Regularizing deep reinforcement learning from pixels,” in _Proc. Int. Conf. Learn. Representations (ICLR)_ , 2021. 

- [24] D. Yarats, R. Fergus, A. Lazaric, and L. Pinto, “Mastering visual continuous control: Improved data-augmented reinforcement learning,” in _Proc. Int. Conf. Learn. Representations (ICLR)_ , 2022. 

- [25] T. Johannink, S. Bahl, A. Nair, J. Luo, A. Kumar, M. Loskyll, J. A. Ojea, E. Solowjow, and S. Levine, “Residual reinforcement learning for robot control,” in _Proc. IEEE Int. Conf. Robot. Autom. (ICRA)_ , 2019, pp. 6023–6029. 

- [26] S. Mysore, B. Mabsout, R. Mancuso, and K. Saenko, “Regularizing action policies for smooth control with reinforcement learning,” in _Proc. IEEE Int. Conf. Robot. Autom. (ICRA)_ , 2021. 

- [27] Z. Liu, P. Peng, and Y. Tian, “Visual reinforcement learning with residual action,” in _Proc. AAAI Conf. Artif. Intell._ , vol. 39, no. 18, 2025, pp. 19 050–19 058. 

- [28] J. Zhang, G. Adineera, J. Tan, and J. Kim, “ResWM: Residual-action world model for visual RL,” _arXiv preprint arXiv:2603.11110_ , 2026. 

- [29] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Robotics: Science and Systems (RSS)_ , 2023. 

- [30] W. Zhang, T. Hu, H. Zhang, Y. Qiao, Y. Qin, Y. Li, J. Liu, T. Kong, L. Liu, and X. Ma, “Chain-of-action: Trajectory autoregressive modeling for robotic manipulation,” in _Adv. Neural Inf. Process. Syst. (NeurIPS)_ , 2025. 

- [31] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” in _Proc. Int. Conf. Learn. Representations (ICLR)_ , 2020. 

- [32] Q. Li, Z. Peng, L. Feng, Q. Zhang, Z. Xue, and B. Zhou, “MetaDrive: Composing diverse driving scenarios for generalizable reinforcement learning,” _IEEE Trans. Pattern Anal. Mach. Intell._ , vol. 45, no. 3, pp. 3461–3475, 2023, arXiv:2109.12674. 

- [33] H. Caesar, J. Kabzan, K. S. Tan, W. K. Fong, E. M. Wolff, A. Lang, L. Fletcher, O. Beijbom, and S. Omari, “nuPlan: A closed-loop MLbased planning benchmark for autonomous vehicles,” _arXiv preprint arXiv:2106.11810_ , 2021. 

- [34] Q. Li, Z. Peng, L. Feng, Z. Liu, C. Duan, W. Mo, and B. Zhou, “ScenarioNet: Open-source platform for large-scale traffic scenario simulation and modeling,” in _Adv. Neural Inf. Process. Syst. (NeurIPS) Datasets and Benchmarks Track_ , 2023. 

- [35] M. Treiber, A. Hennecke, and D. Helbing, “Congested traffic states in empirical observations and microscopic simulations,” _Phys. Rev. E_ , vol. 62, no. 2, pp. 1805–1824, 2000. 

- [36] A. Kesting, M. Treiber, and D. Helbing, “General lane-changing model MOBIL for car-following models,” _Transp. Res. Rec._ , vol. 1999, no. 1, pp. 86–94, 2007. 

- [37] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,” in _Proc. Int. Conf. Mach. Learn. (ICML)_ , 2018, pp. 1861–1870. 

- [38] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

