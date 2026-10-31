---
title: "Action Hallucination in Generative Vision-Language-Action Models"
date: "2026-02-06"
authors: "Harold Soh; Eugene Lim"
url: https://arxiv.org/abs/2602.06339
pdf: https://arxiv.org/pdf/2602.06339
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.06339)** / [論文ページ](https://arxiv.org/abs/2602.06339)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# ACTION HALLUCINATION IN GENERATIVE VISION-LANGUAGE-ACTION MODELS 

A PREPRINT 

**Harold Soh** and **Eugene Lim** 

1Department of Computer Science, School of Computing 

2Smart Systems Institute 

National University of Singapore `harold@nus.edu.sg elimwj@u.nus.edu` 

May 13, 2026 

### **ABSTRACT** 

Robot Foundation Models, such as VLAs, promise end-to-end generative robot policies with broad generalization. Yet it remains unclear whether they fundamentally resolve the core problem of action generation in embodied settings, or overcome the long-standing challenges of robotics. We address this question by analyzing action hallucinations that violate physical constraints and their extension to plan-level failures. Focusing on latent-variable generative policies, we show that hallucinations can arise from structural mismatches between feasible robot behavior and common model architectures. We study three such barriers—topological, precision, and horizon—and show how they impose unavoidable tradeoffs. Our analysis provides mechanistic explanations for reported empirical failures of generative robot policies and suggests principled directions for improving reliability and trustworthiness, without abandoning their expressive power. 

### **1 Introduction** 

Robot Foundation Models (RFMs) and Large-scale Vision-Language-Action (VLA) models (e.g., [1, 2, 3, 4]) promise a “GPT moment” for robotics: given image observations and a natural-language instruction, a single end-to-end policy produces a continuous control trajectory that solves the task. Recent generative VLAs such as _π_ 0 _._ 5 [5], Gr00T N1 [4], and MolmoAct [6] combine transformer encoders with conditional flow/diffusion models that map Gaussian noise into full action trajectories. Other contenders like diffusion policies [7, 8] and flow-matching policies [9] map Gaussian noise into action chunks that are executed sequentially. These models demonstrate impressive semantic generalization, yet substantial prior work [10, 11, 12, 13, 14] has shown they also generate actions that are physically invalid, e.g., grasps through objects or plans that do not result in goal achievement. We refer to this phenomenon as _action hallucination_ . 

Action hallucinations matter for two reasons. First, they are safety- and reliability-critical. Unlike hallucinated text, invalid actions are executed in the physical world and can cause damage or hazardous interactions. Second, these failures may not be confined to exotic corner cases. Even a model that is highly capable _on average_ can intermittently produce nonsensical actions, a risk that is amplified when robots are deployed at scale and over long periods of time. 

This paper argues that part of action hallucination is _structural_ : it arises from a mismatch between (i) the geometry/topology of physically valid behavior in robotics and (ii) the architectural regularities of modern generative action heads and planning pipelines. Concretely, many VLAs generate actions by sampling a _connected_ latent prior (typically Gaussian noise) and decoding it through a map that is continuous in the latent (as in diffusion, flow-matching, and conditional flows). At execution time, these models are often used sequentially and/or wrapped in test-time sampling (and possible verification). This work clarifies _when_ these design choices induce hallucinations (regardless of the data or model scale) and _what_ changes are needed to mitigate them. 

**Contributions.** We use largely elementary mathematical tools (topology, measure bounds, and probabilistic arguments) to construct a coherent theory of action hallucination that matches the architectural and algorithmic characteristics 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

of modern VLAs. This approach connects to classic insights in robotics and leads to a clean formal framework to analyze generative VLAs—the constraints of non-convexity, precision, and compounding errors are foundational to robotics [15, 16, 17] and our contribution is to study these constraints in the context of modern VLAs. Concretely, we contribute: 

- A **topological impossibility result** for hallucination-free multi-mode coverage under continuous latent heads, and a quantitative **isoperimetric lower bound** connecting hallucination to decoder smoothness and mode separation. 

- A **precision-barrier analysis** for contact tasks, including a lower bound and a **generative precision trilemma** (fold, collapse, or hallucinate), plus a refinement-step tradeoff that clarifies why iterative diffusion/flow-style generation helps. 

- A reliability-aware analysis of **verification-guided planning** for **long-horizon tasks** that identifies when test-time compute helps and why adaptive search is needed under verifier noise. 

Our theoretical analysis complements the growing body of empirical work on VLAs (e.g., [3, 6, 14, 13]) and helps clarify why VLAs work, as well as when and why they may fail. Our focus is not to develop new general mathematical theory, but rather, adapt existing tools to analyze the connection between generative models and embodied action generation. We discuss connections to recent experimental results and to practical system design choices, e.g., hybrid discrete-continuous structure, iterative refinement, and verification-guided planning. 

**Related Work.** Hallucination has been widely studied in LLMs and VLMs, where it is typically framed as fluent generation that violates an external correctness oracle such as factuality, groundedness, or visual consistency [18, 19, 20, 21, 22]. We adopt this oracle-based view, but replace textual truthfulness with _physical and task validity_ in embodied settings. 

Our analysis connects three previously separate threads. First, robotics has long recognized that feasible behavior is rarely convex or safely interpolatable: obstacles induce nonconvex and disconnected free spaces [15], narrow passages make feasible connections hard to find [16, 23], and contact-rich manipulation often requires hitting thin, lower-dimensional contact sets and mode transitions [24, 25, 26, 27]. Second, prior work on deep generative models shows that continuous generators with connected latent priors cannot exactly represent disconnected target supports, leading to mode dropping or bridging samples [28, 29, 30, 31, 32, 33, 34]. In this work, we interpret these bridge samples physically; in robot action spaces, they can correspond to collisions, infeasible contacts, joint-limit violations, or actions that fall into non-progress regions. Our precision analysis likewise quantifies the density concentration needed to hit thin feasible tubes, and shows how flow/DDIM-style samplers realize this concentration through local contraction across refinement steps. 

Finally, our work relates to long-horizon decision-making and verification-guided search. Multi-step planning is computationally hard [35, 36], and compounding error is a classic source of long-horizon failure in imitation learning [17]. Viewed probabilistically, long-horizon success becomes a rare event, motivating decomposition and adaptive sampling methods [37, 38]. To see if VLAs can bypass these constraints through scale or test-time compute [39, 40, 41], we formalize how horizon-induced rarity, verifier noise, and adaptive proposal mechanisms interact to reduce—or limit the reduction of—behavioral hallucinations. 

### **2 Preliminaries** 

In this section, we formalize robot environments, task instances, and generative robot policies, then use this framework to define action hallucinations in embodied AI. Due to space constraints, we focus on the core ideas; full proofs, formal arguments, and additional details are deferred to the appendix. 

**Environment Model and Tasks.** We consider a robot that operates in an environment and seeks to achieve a goal. **Definition 1** (Environment) **.** _An environment is a tuple E_ = ( _S, A,_ Ω _, O, T , C_ safe) _, where S ⊆_ R<sup>_n_</sup> _is the true physical state space, A ⊆_ R<sup>_d_</sup> _is the continuous action space,_ Ω _is the observation space, O_ : _S →_ Ω _is the observation map, T_ : _S × A →S is the transition map, and C_ safe _⊆S is the set of physically consistent and constraint-satisfying states._ **Definition 2** (Goal-reaching task instance) **.** _A task instance is I_ = ( _E, s_ 0 _, ℓ, G, T_ ) _, where s_ 0 _∈C_ safe _is the initial state, ℓ is the language instruction, G ⊆C_ safe _is the goal set, and T ∈_ N _is the horizon or action budget._ 

An action is generic in that it may denote a target pose, joint velocity, torque command, motion primitive, or action chunk. When _a_ is a chunk or trajectory, _T_ ( _s, a_ ) denotes the terminal state after execution. We use deterministic observations and dynamics for clarity; stochastic observations or transitions can be handled by replacing _O_ and _T_ with kernels and taking the probabilities below over this additional randomness. The deterministic setting is the special case where the kernels are point masses. The set _C_ safe is a ground-truth physical object used to define hallucination. 

2 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

**VLA Contexts and Latent Action Heads.** At time _t_ , the robot observes _ot_ = _O_ ( _st_ ). Let _ht_ = ( _o_ 0 _, a_ 0 _, . . . , ot−_ 1 _, at−_ 1 _, ot_ ) be the observation-action history. A VLA encoder maps history and language to a context _ct_ = _Eϕ_ ( _ht, ℓ_ ) _∈C._ The context may contain imagelanguage embeddings, proprioception, memory, or other internal representations. We define the oracle-state case as a special case _ct_ = _c_<sup>_⋆_</sup> ( _st, ℓ_ ). This setting deliberately _favors_ the policy: the action head receives all task-relevant state information, allowing us to isolate limitations of action generation itself rather than confounding them with perceptual errors or state estimation failures. We state our main results for this oracle-state specialization, but the same arguments extend to more general settings by replacing _s_ with the history/context. 

**Assumption 3** (Latent prior) **.** _The latent space Z is a nonempty, open, and path-connected subset of_ R<sup>_m_</sup> _. The latent prior pZ is absolutely continuous with respect to m- dimensional Lebesgue measure, and has a density ρZ such_ 


Figure 1: (Left) The prototypical generative VLA analyzed in this work. Given state observations, a task prompt, and a noise sample, the model outputs robot actions. Recent VLAs are structured into a high-level planner and a low-level action head, but part of our theory also applies to those that do not have this explicit structure (e.g., RDT [8]). (Right) An example where a robot is given a long-horizon task that involves multi-modality and precision. 

_that ρZ_ ( _z_ ) _>_ 0 _for almost every z ∈Z, and is bounded below on compact subsets of Z._ 

**Definition 4** (Latent-head VLA policy) **.** _A latent-head VLA policy is a map πθ_ : _C × Z →A. For each fixed context c, the map z �→ πθ_ ( _c, z_ ) _is continuous. The induced action distribution is pθ_ ( _· | c_ ) := � _πθ_ ( _c, ·_ )�#<sup>_pZ._</sup> 

This captures continuous generative action heads such as flow matching, DDIM, and conditional flow decoders. For stochastic diffusion samplers with fresh noise injected at multiple denoising steps, one can regard the full collection of injected noise variables as the latent input. In the oracle-state case, we write _pθ_ ( _· | s, ℓ_ ) := _pθ_ ( _· | c_<sup>_⋆_</sup> ( _s, ℓ_ )) _,_ and omit _ℓ_ when it is fixed. 

**Action and Plan Hallucination.** Given the structure of existing VLAs, we consider two major types of behavior hallucinations. At the low-level, an _action hallucination_ is an action (or action chunk / trajectory) whose induced rollout violates physical laws or environmental constraints (e.g., teleporting the robot, penetrating a solid obstacle, or exceeding kinematic limits). At the high-level, even physically valid actions can still fail to achieve the task goal. Hence, a _plan hallucination_ is a generated plan (sequence of actions) that violates constraints and/or fails to reach the goal. Plan hallucinations subsume action hallucinations but also include _goal failure_ . 

**Definition 5** (Physical validity oracle) **.** _For a fixed environment E, define f_ phys : _S×A →{_ 0 _,_ 1 _}, where f_ phys( _s, a_ ) = 1 _if executing a from state s respects the relevant physical and environmental constraints, and f_ phys( _s, a_ ) = 0 _otherwise._ 

For chunks or trajectories, _f_ phys checks all intermediate states, not only the terminal state. State-dependent action/admissibility constraints, such as torque limits and task-specific feasibility constraints, are folded into _f_ phys. Define the safe action set, _A_ safe( _s_ ) = _{a ∈A_ : _f_ phys( _s, a_ ) = 1 _}_ and the forbidden/unsafe action set _A_ forb( _s_ ) = _A \ A_ safe( _s_ ). 

**Definition 6** (Action hallucination) **.** _At physical state s and context c, a sampled action a_ = _πθ_ ( _c, z_ ) _is an action hallucination if f_ phys( _s, a_ ) = 0 _. Its probability is Hθ_ ( _s, c_ ) := Pr _Z∼pZ_ � _f_ phys� _s, πθ_ ( _c, Z_ )� = 0� _. In the oracle-state case, we write Hθ_ ( _s, ℓ_ ) := _Hθ_ ( _s, c_<sup>_⋆_</sup> ( _s, ℓ_ )) _, or simply Hθ_ ( _s_ ) _when ℓ is fixed._ 

A closed-loop VLA induces a finite action sequence when unrolled. Given _I_ = ( _E, s_ 0 _, ℓ, G, T_ ) and i.i.d. latents _z_ 0: _T −_ 1, define _ot_ = _O_ ( _st_ ), _ct_ = _Eϕ_ ( _ht, ℓ_ ), _at_ = _πθ_ ( _ct, zt_ ), and _st_ +1 = _T_ ( _st, at_ ). The induced plan is _τθ,ϕ_ ( _I, z_ 0: _T −_ 1) := ( _a_ 0 _, . . . , aT −_ 1) _∈A_<sup>_T_</sup> _._ Here “plan” means the grounded action sequence induced by closed-loop execution (which need not be a symbolic subtask sequence). 

**Definition 7** (Plan hallucination) **.** _For an action sequence τ_ = ( _a_ 0 _, . . . , aT −_ 1) _, let st_ +1 = _T_ ( _st, at_ ) _be its rollout from s_ 0 _. Define f_ plan( _s_ 0 _, τ_ ; _G_ ) = 1 _iff f_ phys( _st, at_ ) = 1 _for all t_ = 0 _, . . . , T −_ 1 _, and sT ∈G. Otherwise f_ plan( _s_ 0 _, τ_ ; _G_ ) = 0 _. A plan hallucination occurs when f_ plan( _s_ 0 _, τ_ ; _G_ ) = 0 _and its probability on instance I is Hθ,ϕ_<sup>plan(</sup><sup>_I_) := Pr</sup> � _f_ plan� _s_ 0 _, τθ,ϕ_ ( _I, Z_ 0: _T −_ 1); _G_ � = 0� _._ 

We call _I_ solvable if some _τ ∈A_<sup>_T_</sup> satisfies _f_ plan( _s_ 0 _, τ_ ; _G_ ) = 1, and focus on solvable instances. 

3 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 


Figure 2: **Topological barrier for latent-variable VLA policies.** ( **a** ) We study generative VLAs whose action head is a conditional latent-variable policy that maps a task-relevant state (or history of observations) and latent noise _z_ to a continuous action (or action chunk). In the illustrated navigation example, reaching the microwave requires going _left_ or _right_ around the kitchen island, inducing two qualitatively distinct modes of valid behaviors. ( **b** ) Schematic of the topological barrier (Lemma 9). The valid actions (bottom panel) decompose into disconnected components _U_ 1 and _U_ 2 (e.g., left vs. right), separated by a forbidden region _A_ forb. If _πθ_ ( _s, ·_ ) is continuous and maps _z �→ a ∈ U_ 1 and _z_<sup>_′_</sup> _�→ a_<sup>_′_</sup> _∈ U_ 2, then any continuous latent path between _z_ and _z_<sup>_′_</sup> must cross an _open seam Z_ seam = _πθ_ ( _s, ·_ )<sup>_−_1</sup> ( _A_ forb), implying non-zero hallucination probability. ( **c** ) Diffusion model trained on bimodal action data: red points in _Z_ (top) lie on the seam and decode to forbidden actions in _A_ (bottom). See Appendix D.1 for details. ( **d** ) Empirical trends for flow matching and diffusion. Hallucination rates _H_ can increase approximately linearly with the number of covered modes _M_ (top) and grows with _W/L_<sup>�</sup> (bottom), consistent with Theorem 11 ( _L_<sup>�</sup> is the numerically-estimated Lipschitz constant). 

### **3 Low-Level Action Hallucinations** 

#### **3.1 Topological Barrier for Multi-Mode Coverage** 

Recent VLAs and generative policies are often lauded for their ability to represent complex _multi-modal_ action trajectories (e.g., “go left” or “go right” around an obstacle). However, experiments show these models still produce invalid actions despite significant training [10, 11, 13] or drop action modes [42]. Figure 2 provides a high-level overview of our theoretical results below that explains why this can occur. 

Fix a physical state _s ∈S_ and instruction _ℓ_ . We first consider situations where the valid actions at a fixed state decompose into two distinct safe ‘modes’, _UL_ and _UR_ (e.g., two inverse-kinematics branches, two grasp approach directions), separated by physically forbidden actions (e.g., joint-limit violation, infeasible contact). 

**Assumption 8.** _For a given state s, assume that the safe action set A_ safe( _s_ ) _has at least two disjoint, nonempty path-connected components UL and UR in the subspace topology of A. Also assume that the forbidden region A_ forb( _s_ ) _is open in A and has nonempty interior._ 

In this setting, topology dictates that a latent action head that attempts to cover both modes must hallucinate. 

**Lemma 9** (Topological Barrier) **.** _Suppose Assumption 8 holds and there exist zL, zR ∈Z such that πθ_ ( _s, zL_ ) _∈ UL and πθ_ ( _s, zR_ ) _∈ UR. Define the_ seam set _, Z_ seam( _s_ ) := _{z ∈Z_ : _πθ_ ( _s, z_ ) _∈A_ forb( _s_ ) _}. Then Z_ seam( _s_ ) _is nonempty and open in Z. The hallucination probability at s is strictly positive, Hθ_ ( _s_ ) = Pr _z∼pZ_ [ _z ∈Z_ seam( _s_ )] _>_ 0 _._ 

Lemma 9 (proof in Appendix A.1) translates a geometric concept in deep generative modeling (e.g., [29, 30, 28]) to robotics—if there are distinct modes of valid behaviors at a given state, then any generative policy that is smooth in its latent input must create a “seam” of _in-between_ latents that decode to _in-between_ actions. The policy cannot assign probability mass to both modes without also assigning probability mass to the invalid or unsafe actions between them. 

Next, we derive a quantitative lower bound in a multi-mode setting ( _≥_ 2). Assumption 10 below extends the previous setup to one where the valid action set _A_ safe( _s_ ) splits into _M_ disconnected modes _U_ 1 _, U_ 2 _, . . . , UM_ . These modes in action space are separated by at least a distance 2 _W_ with a forbidden buffer of thickness _W_ around each mode. **Assumption 10.** _For a given state s, we assume that the safe set decomposes into M ≥_ 2 _nonempty, pairwise-disjoint, closed, path-connected components A_ safe( _s_ ) =<sup>�</sup><sup>_M_</sup> _i_ =1<sup>_Ui.AssumethereexistsW>_0</sup><sup>_suchthat_dist(</sup><sup>_Ui, Uj_):=</sup> 

4 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

inf _a∈Ui,a′∈Uj ∥a − a_<sup>_′_</sup> _∥≥_ 2 _W for all i̸_ = _j, and for each i, the W -neighborhood of Ui outside Ui itself is forbidden:_ � _a ∈A_ : 0 _<_ dist( _a, Ui_ ) _< W_ � _⊆A_ forb( _s_ ) _._ 

In the common Gaussian latent setting, we can lower-bound the hallucination rate of smooth policies that are locally Lipschitz in _z_ . 

**Theorem 11** (Isoperimetric lower bound on action hallucination) **.** _Fix a state s satisfying Assumption 10. Let Z ∼N_ (0 _, Im_ ) _and fix a radius R >_ 0 _. Assume that the latent-to-action head z �→ πθ_ ( _s, z_ ) _is L-Lipschitz on the typical-latent ball BR_ := _{z ∈_ R<sup>_m_</sup> : _∥z∥≤ R}, i.e., ∥πθ_ ( _s, z_ ) _− πθ_ ( _s, z_<sup>_′_</sup> ) _∥≤ L ∥z − z_<sup>_′_</sup> _∥∀z, z_<sup>_′_</sup> _∈ BR and L >_ 0 _. Let ϵ_ := _W/L. For each safe mode Ui, define the latent preimage Vi_ := _πθ_ ( _s, ·_ )<sup>_−_1</sup> ( _Ui_ ) _and the in-ball mass p_<sup>(</sup> _i_<sup>_R_)</sup> := Pr � _Z ∈ Vi ∩ BR_ � _. Let q_ ( _R_ ) = Pr � _∥Z∥ > R_ � _. Then the hallucination probability at s satisfies_ 


#### _where_ Φ _is the CDF of the standard normal distribution._ 

Compared to Lemma 9, Theorem 11 provides a quantitative lower bound that reveals key factors that influence the action hallucination rate. As before, the problem is interpolation between the _M_ modes. The more smoothly the policy varies with the latent, the more probability mass leaks into the forbidden seam. In addition to the number of modes _M_ , a key ratio to note is _ϵ_ = _W/L_ . _W_ measures how wide the unsafe gap is in action space, and _L_ measures how quickly actions can change as we adjust the latent _z_ . If the model is very smooth in the latent space, then it must transition gradually, and a larger set of latents produce intermediate invalid actions. The main idea underlying the proof (Appendix A.2) is to apply Gaussian isoperimetry to lower bound the mass of disjoint latent “halos” of radius _ϵ_ = _W/L_ around each safe-mode set. 

**Implications for VLAs.** Our analysis reveals a tension between _diversity_ and _safety_ . Datasets can be multi-modal (e.g., distinct grasp types or approach trajectories) and a low-level continuous policy trained to cover all _M_ modes equally faces a geometric dilemma: (i) **Accept Hallucination:** To cover all diverse modes, the policy is geometrically required to expose significant Gaussian surface area to the forbidden regions, resulting in invalid “interpolated” actions; or (ii) **Mode Collapse:** To reduce the hallucination rate (minimize _Hθ_ ), the policy can assign very little mass to some modes or drop modes entirely (reduce _M_ ). 

Crucially, this dilemma is a geometric consequence and does _not_ disappear with better optimization or more data. One theoretical solution is to break the continuity assumption: generative action heads can employ _hybrid_ designs that use discrete decisions to switch between modes (e.g., discrete tokens [43, 44, 45], diffusion options [46], or mixtureof-experts (MoE) gating [47]). Recent work provides suggestive empirical support for this prescription; VFP [10] uses a MoE flow decoder to encourage mode-specific action generation, while Hybrid Diffusion Planner [45] jointly samples discrete plan tokens and continuous trajectories to reduce long-horizon mode confusion. Both lead to better performance. In VLAs, the VLM/high-level planner can sample the mode before invoking the generative action head. However, this shifts the burden of hallucination avoidance to the planner (see Sec. 4). Theorem 11 also indicates that smoothness is a “double-edged sword” for contemporary models: on one hand, smoothness is generally encouraged in (learnt) policies as it is associated with more stable training [28] and robot behavior—we usually prefer the case that similar _z_ imply similar actions. On the other hand, smoothness likely has a _negative_ effect on action hallucination; all else being equal, in (1), each term Φ�Φ<sup>_−_1</sup> ( _p_<sup>(</sup> _i_<sup>_R_)</sup> ) + _ϵ_ � _− p_<sup>(</sup> _i_<sup>_R_)</sup> is increasing in _ϵ_ = _W/L_ . 

#### **3.2 Precision Barrier for Contact Tasks** 

Let us now shift our attention from multiple modes to the complementary regime of precision and contact-rich tasks. Once contact occurs, rigid-body non-penetration, admissible contact modes, and practical limits such as maximum contact wrench induce additional state-dependent constraints on which actions are physically allowed. The set of admissible actions forms a thin tube around a lower-dimensional set in action space. Here, we revisit this _precisionbarrier_ from classical robotics [23] and we show that, as tolerance around the tube shrinks, any policy with a _smooth, full-dimensional_ action density is almost guaranteed to hallucinate actions (See Fig. 3 for an overview). 

We model ideal contact configurations as a state-dependent _k_ -dimensional submanifold _M_ ( _s_ ): 

**Definition 12.** _Let M_ ( _s_ ) _⊂A be a compact C_<sup>1</sup> _submanifold of dimension k < d. For δ >_ 0 _, define the δ-tube around M_ ( _s_ ) _by Mδ_ ( _s_ ) := _{a ∈A_ : dist( _a, M_ ( _s_ )) _≤ δ}, where_ dist( _a, M_ ) = inf _x∈M ∥a − x∥. For a state s, suppose the safe terminal actions satisfy A_ safe( _s_ ; _δ_ ) _⊆Mδ_ ( _s_ ) _for a task-specific tolerance δ. Define the δ-tolerant success Sθ_ ( _s_ ; _δ_ ) := Pr [ _a ∈A_ safe( _s_ ; _δ_ )] _, and hallucination probabilities, Hθ_ ( _s_ ; _δ_ ) := Pr [ _a ∈A/_ safe( _s_ ; _δ_ )] = 1 _− Sθ_ ( _s_ ; _δ_ ) _._ 

5 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 


Figure 3: **Precision barrier for contact-rich tasks.** ( **a** ) Many manipulation tasks (e.g., grasping, peg-in-hole, handling tools / articulated / deformable objects) require high precision in that valid actions concentrate near a lower-dimensional feasible set. We model this as a _k_ -dimensional manifold _M ⊂A_ with tolerance tube _Mδ_ = _{a_ : dist( _a, M_ ) _≤ δ}_ (schematic). ( **b** ) Empirical distribution of distances _r_ = dist( _a, M_ ) for samples from flow matching and diffusion (log scales). The shaded region _r > δ_ corresponds to action hallucinations. See Appendix D.2 for experiment details. ( **c** ) Action hallucination rate _H_ ( _s_ ; _δ_ ) = Pr[ _r > δ_ ] versus tolerance _δ_ (log–log). Tightening tolerance sharply increases hallucinations, consistent with our precision barrier (Lemma 13) that shows maintaining low hallucination at small _δ_ requires increasingly concentrated mass near _M_ . ( **d** ) The geometric mean of per-step minimum singular values increases toward 1 as the number of sampler steps _K_ grows, indicating that the necessary overall contraction can be distributed across many mild refinement steps rather than a single severe collapse (Theorem 14 and Corollary 15). 

We fix a state _s_ and write _M_ := _M_ ( _s_ ) and _Mδ_ := _Mδ_ ( _s_ ). Assume that the dimensionality of the latent code _z_ is the same as the action, _m_ = _d_ (as is the case in flow-matching and DDIM models). Below, we show that hitting a low-dimensional contact manifold requires the action distribution to concentrate its probability density. 

**Lemma 13** (Precision Barrier) **.** _Fix a state s and adopt Definition 12. Assume that the induced action law µθ_ ( _· | s_ ) _is absolutely continuous with respect to d-dimensional Lebesgue measure on A, with density p_ ( _· | s_ ) _. Then, there exist constants CM >_ 0 _and δ_<sup>¯</sup> _>_ 0 _(depending only on M) such that for all_ 0 _< δ ≤ δ_<sup>¯</sup> _, Sθ_ ( _s_ ; _δ_ ) _≤ CMδ_<sup>_d−k_</sup> _·_ ess sup _a∈Mδ p_ ( _a | s_ ) _, and hence_ 


Lemma 13 (proof in Appendix B.1) captures a source of action hallucination that is _distinct_ from the topological barrier in Section 3.1. Even when the valid action set is connected (a single contact manifold), the policy needs to generate probability densities scaling as _O_ ( _δ_<sup>_−_(</sup><sup>_d−k_)</sup> ) inside the _δ_ -tube around _M_ . This becomes more challenging as the tolerance _δ_ shrinks or the codimension ( _d − k_ ) increases. The following theorem shows how a policy can supply this extreme density. 

**Theorem 14** (The Precision Trilemma: Collapse, Fold, or Hallucinate) **.** _Let m_ = _d and let the action be generated by a_ = _F_ ( _z_ ) _where Z ∼ pZ. Assume F is C_<sup>1</sup> _on an open set U ⊆Z containing the support of pZ, with bounded latent density ρZ_ ( _z_ ) _≤ ρ_<sup>max</sup> _Z . Define the active latent set as Zδ_ := _F_<sup>_−_1</sup> ( _Mδ_ ) _∩ U . Define local folding and local conditioning restricted to this active set: Nδ_ := ess sup _a∈Mδ_ # _{z ∈ Zδ_ : _F_ ( _z_ ) = _a}, and σ∗_ ( _δ_ ) := ess inf _z∈Zδ σ_ min( _JF_ ( _z_ )) _, where JF_ ( _z_ ) _is the Jacobian of F and σ_ min( _JF_ ( _z_ )) _its smallest singular value. Assume F is finite-to-one on Zδ (i.e., Nδ < ∞) and σ∗_ ( _δ_ ) _>_ 0 _. Then the induced action distribution admits a density on Mδ and the hallucination rate satisfies Hθ_ ( _s_ ; _δ_ ) _≥_ 1 _− CM δ_<sup>_d−k_</sup> _Nδ ρ_<sup>max</sup> _Z σ∗_ ( _δ_ )<sup>_−d_</sup> _. If the policy achieves a target hallucination level Hθ_ ( _s_ ; _δ_ ) _≤ η for some η ∈_ (0 _,_ 1) _, then the generator must satisfy_ 


_Hence, as precision tightens (δ →_ 0 _), any policy that maintains Hθ_ ( _s_ ; _δ_ ) _≤ η must either_ fold _space (Nδ →∞) or_ collapse _volume locally (σ∗_ ( _δ_ ) _→_ 0 _)._ 

Theorem 14 (proof in Appendix B.2) shows that near the tube, the induced action density satisfies _p_ ( _a | s_ ) ≲ _Nδ · ρ_<sup>max</sup> _Z · σ∗_ ( _δ_ )<sup>_−d_</sup> so the two architectural mechanisms to increase density are: (i) **Collapse** (Jacobian contraction): make _σ∗_ ( _δ_ ) small so _F_ compresses latent volume into a tiny region of action space; or (ii) **Fold** (many-to-one decoding): make _Nδ_ large so that many disjoint latent regions decode to the same actions. If neither occurs, the policy cannot place enough mass in the tube and will hallucinate actions. In short, as _δ →_ 0, the generative policy must either collapse, fold, or hallucinate. 

Modern VLAs often use flow-matching to generate actions. In theory, these are diffeomorphic generators with invertible steps so folding is not possible ( _Nδ_ = 1) and meeting the density requirement at tight tolerances requires Jacobian 

6 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

collapse. These methods apply a sequence of “refinement” (or denoising) steps and Corollary 15 below (proof in Appendix B.3) shows that to maintain a fixed hallucination rate at increasingly tight tolerances, a flow-like policy must either accumulate sufficient latent-space contraction across its _K_ refinement steps or allow individual steps to become increasingly ill-conditioned. 

**Corollary 15** ( _K_ -step precision tradeoff) **.** _Assume the decoder is a K-step composition F_<sup>(</sup><sup>_K_)</sup> = Φ _K−_ 1 _◦· · ·◦_ Φ0 _, where each_ Φ _t is a C_<sup>1</sup> _diffeomorphism and there exist constants λt >_ 0 _such that σ_ min( _J_ Φ _t_ ( _z_ )) _≥ λt for all z. Let σ∗_ ( _δ_ ) _≥_ inf _z∈Zδ σ_ min( _JF_<sup>(</sup><sup>_K_)</sup> ( _z_ )) _≥_<sup>�</sup><sup>_K_</sup> _t_ =0<sup>_−_1</sup><sup>_λt.Then, for all_0</sup><sup>_< δ≤δ_¯</sup><sup>_, H_</sup> _θ_<sup>(</sup><sup>_K_)</sup> ( _s_ ; _δ_ ) _≥_ 1 _− CMρ_<sup>max</sup> _Z t_ =0<sup>_λt_</sup> _δ_<sup>_d−k_</sup> _. In_ �� _K−_ 1 � _−d particular, if λt ≥ λ ∈_ (0 _,_ 1) _for all t, then a necessary condition to bound the hallucination rate Hθ_<sup>(</sup><sup>_K_)</sup> ( _s_ ; _δ_ ) _≤ η ∈_ <u>1</u> 1 _−η_ (0 _,_ 1) _is K ≥ d_ log(1 _/λ_ ) �( _d − k_ ) log<sup><u>1</u></sup> _δ_<sup>+ log</sup> _CMρ_<sup><u>max</u></sup> _Z_ � _._ 

**Implications for VLAs.** In this regime of contact-rich tasks, a policy _should_ concentrate probability mass onto the safe action manifold rather than preserve spurious variance that gives rise to action hallucinations. However, there is a cost. Theorem 14 shows that achieving this requires either Jacobian collapse or folding. Both make the latent space a poor coordinate system for optimization. A possible path around the precision barrier is to _project_ the VLA’s proposed action back onto the task’s feasible contact manifold (e.g., via a low-level controller, or external sensing like tactile feedback) or _parameterize_ the manifold (e.g., an atlas of local charts [48] or kinematically-valid trajectories [49]) so decoded actions stay on-manifold by construction. 

Corollary 15 suggests the iterative nature of modern flow and diffusion policies is not solely about sampling from complex action distributions, but rather, about decomposing an effectively singular projection into a product of gentle, well-behaved steps. The dependence on _δ_ enters only through a log(1 _/δ_ ) factor, so the required number of refinement steps grows only logarithmically with tolerance. Interestingly, very recent large-scale empirical evidence [42] on benchmarks supports this view and suggests that the advantage of diffusion/flow-style policies on challenging contactrich tasks is strongly associated with iterative computation and stochasticity injection, rather than distribution learning. Our theory serves to explain these empirical findings. 

### **4 Long-Horizon Plan Hallucinations** 

This section builds on the previous analysis of one-step action generation and extends it to long-horizon goal achievement. We now move one layer up to the VLM/VLA planner and develop a theoretical framework that complements empirical findings showing that VLMs/VLAs suffer sharp performance degradation on long-horizon tasks (e.g., [14, 50, 12, 39]) and recent explorations into test-time compute (e.g., [39, 40]). 

We begin by fixing a task instance _I_ with deterministic dynamics _T_ and defining time-bounded backward-reachable sets, Σ0 := _G_ , Σ _t_ := _{s ∈S_ : _∃a ∈A_ s.t. _f_ phys( _s, a_ ) = 1 and _T_ ( _s, a_ ) _∈_ Σ _t−_ 1 _}_ for _t ≥_ 1 _._ Thus, _s ∈_ Σ _t_ means that from state _s_ there exists a physically-valid action that lands in a state from which the goal is reachable in _t_ further steps. For a state _s_ and remaining horizon _t ≥_ 1 define the _progress set_ , _A_ prog( _s, t_ ) := _{a ∈A_ : _f_ phys( _s, a_ ) = 1 and _T_ ( _s, a_ ) _∈_ Σ _t−_ 1 _}_ . By construction, _s ∈_ Σ _t_ if and only if _A_ prog( _s, t_ ) _̸_ = _∅_ , and _A_ prog( _s, t_ ) _⊆A_ safe( _s_ ), i.e., progress actions are a subset of safe actions. **Lemma 16** (Horizon Barrier) **.** _Let_ ( _St_ )<sup>_T_</sup> _t_ =0<sup>_betherolloutfroms_0</sup><sup>_._</sup> _Define pt_ ( _s_ ) := Pr _Z∼pZ_ � _πθ_ ( _s, Z_ ) _∈ A_ prog( _s, t_ )� _and γt_ := sup _s∈_ Σ _t pt_ ( _s_ ) _. Then the rollout success probability factorizes and is upper bounded by_ Pr [ _f_ plan( _s_ 0 _, τθ_ ( _s_ 0 _, Z_ 0: _T −_ 1)) = 1] _≤_<sup>�</sup><sup>_T_</sup> _t_ =1<sup>_γt. Hence, H_</sup> _π_<sup>plan</sup> _θ_ ( _I_ ) _≥_ 1 _−_<sup>�</sup><sup>_T_</sup> _t_ =1<sup>_γt.In particular, if γt≤γ<_1</sup><sup>_for all_</sup> _t, then_ Pr[ _f_ plan( _s_ 0 _, τθ_ ) = 1] _≤ γ_<sup>_T_</sup> _and Hπ_<sup>plan</sup> _θ_ ( _I_ ) _≥_ 1 _− γ_<sup>_T_</sup> _._ 

Lemma 16 (proof in Appendix C.1) formalizes the horizon barrier as a _compounding reachability bottleneck_ . The idea is intuitive and well-known in robotics [17]: a length- _T_ valid rollout requires sampling a progress action at every step, so success is a product of conditional progress factors. Even if each _γt_ is only slightly below one, their product decays rapidly with horizon. This connects directly to the topological and precision barriers since both reduce per-step progress probability and the deficit compounds with _T_ (also see the discussion in Appendix C.6 on action chunking). 

Now suppose that a VLA can expend _test-time compute_ to _propose_ and _verify_ candidates or continuations, as in sampling, beam/tree search, or using simulator/world-model rollouts. Let _PI_ be a measurable space of complete grounded candidate continuations for instance _I_ ; each _τ ∈PI_ induces an action sequence, so _f_ plan( _s_ 0 _, τ_ ; _G_ ) is welldefined. Define the valid set _V_ := _{τ ∈PI_ : _f_ plan( _s_ 0 _, τ_ ; _G_ ) = 1 _}._ We study a _verification-guided planner_ that runs for at most _q_ rounds. At round _j_ , based on its search history, it chooses a proposal distribution _Qj_ over _PI_ , samples _τj ∼ Qj_ , queries a randomized verifier _f_<sup>˜</sup> _j_ ( _τj_ ), and outputs the first accepted candidate; if no candidate is accepted in _q_ 

7 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

rounds, it abstains and outputs _⊥_ . We assume verifier errors are uniformly bounded: given any history and proposed _τ_ , invalid candidates are accepted with probability at most _ε_ fp, and valid candidates are accepted with probability at least _c_ := 1 _− ε_ fn. 

Define hallucination and abstention probabilities, _H_ ( _I_ ) := Pr[ˆ _τ̸_ = _⊥∧ τ_ ˆ _∈/ V_ ] and _A_ ( _I_ ) := Pr[ˆ _τ_ = _⊥_ ]. The valid-output probability is _S_ ( _I_ ) = 1 _− A_ ( _I_ ) _− H_ ( _I_ ). Plan hallucination here differs slightly from Lemma 16 because the planner may abstain. We focus on the design of ( _α, β_ )-reliable VLAs: 

**Definition 17** (( _α, β_ )-reliability) **.** _Fix α, β ∈_ [0 _,_ 1] _with α_ + _β ≤_ 1 _. We say the planner is_ ( _α, β_ )-reliable _on instance I if H_ ( _I_ ) _≤ α and A_ ( _I_ ) _≤ β. Hence, an_ ( _α, β_ ) _-reliable planner outputs a valid plan with probability at least S_ ( _I_ ) _≥_ 1 _− α − β._ 

Let _Cj−_ 1 be the event that the planner reaches round _j_ . Define the round- _j conditional valid mass_ by _ρj_ := Pr[ _τj ∈ V | Cj−_ 1] = E[ _Qj_ ( _V_ ) _| Cj−_ 1] _,_ with the convention _ρj_ = 0 if Pr[ _Cj−_ 1] = 0. We refer to ( _ρj_ )<sup>_q_</sup> _j_ =1<sup>as the planner’s</sup> _amplification schedule_ . 

**Lemma 18** (Reliability search-budget window) **.** _Consider any verification-guided planner with budget q, verifier error rates_ ( _ε_ fp _, ε_ fn) _, and amplification schedule_ ( _ρj_ )<sup>_q_</sup> _j_ =1<sup>_. Let c_:= 1</sup><sup>_−ε_fn</sup><sup>_. Then H_(</sup><sup>_I_)</sup><sup>_≤ε_fp</sup> � _qj_ =1<sup>Pr[</sup><sup>_Cj−_1](1</sup><sup>_−ρj_)</sup><sup>_≤qε_fp</sup> _and A_ ( _I_ ) _≤_<sup>�</sup><sup>_q_</sup> _j_ =1<sup>(1</sup><sup>_−cρj_)</sup><sup>_. Consequently, the planner is certified as_(</sup><sup>_α, β_)</sup><sup>_-reliable whenever ε_fp</sup> � _qj_ =1<sup>Pr[</sup><sup>_Cj−_1](1</sup><sup>_−_</sup> _ρj_ ) _≤ α and_<sup>�</sup><sup>_q_</sup> _j_ =1<sup>(1</sup><sup>_−cρj_)</sup><sup>_≤β. The simpler sufficient certificate qε_fp</sup><sup>_≤α and_�</sup><sup>_q_</sup> _j_ =1<sup>(1</sup><sup>_−cρj_)</sup><sup>_≤βalso certifies_</sup> ( _α, β_ ) _-reliability._ 

Lemma 18 separates verifier-limited and planner-limited effects. Each query creates a chance to accept a valid plan, but also increases the worst-case (upper-bounded) cumulative risk of a hallucination. Thus test-time compute is useful only if the proposal mechanism increases _ρj_ fast enough before the certified hallucination budget is exhausted. A natural follow-up question is how fast a planner needs to grow _ρj_ ? The following theorem provides an answer for long horizon tasks. 

**Theorem 19** (Amplification-rate to beat the horizon barrier) **.** _Consider the planner above, with amplification schedule_ ( _ρj_ )<sup>_q_</sup> _j_ =1<sup>_.Any_(</sup><sup>_α, β_)</sup><sup>_-reliable planner must satisfy_�</sup><sup>_q_</sup> _j_ =1<sup>Pr[</sup><sup>_Cj−_1]</sup><sup>_ρj≥_1</sup><sup>_−α −β, Assume an exponentially small_</sup> _initial valid mass ρ_ 1 _≤ γ_<sup>_T_</sup> _for some γ ∈_ (0 _,_ 1) _. Then_ (i) **_Polynomial amplification is insufficient._** _If ρj ≤ ρ_ 1 _j_<sup>_p_</sup> _for some fixed p ≥_ 0 _, then meeting the necessary condition requires q ≥_ �1 +<sup><u>(</u></sup><sup>_<u>p</u>_</sup><sup><u>+1)(</u></sup> _γ_<sup>1</sup><sup>_T−α−β_</sup><sup><u>)</u></sup> �1 _/_ ( _p_ +1) _−_ 1 _. For fixed p, γ ∈_ (0 _,_ 1) _, and nontrivial reliability target_ 1 _− α − β >_ 0 _, this lower bound grows exponentially in T ;_ (ii) **_Geometric amplification is sufficient, if within the verifier budget._** _Assume c_ := 1 _− ε_ fn _>_ 0 _, β ∈_ (0 _,_ 1) _, and ρj ≥_ min _{_ 1 _, ρ_ 1 _r_<sup>_j−_1</sup> _} for some r >_ 1 _. Then qε_ fp _≤ α and_<sup>�</sup><sup>_q_</sup> _j_ =1<sup>min</sup><sup>_{_1</sup><sup>_, ρ_1</sup><sup>_rj−_1</sup><sup>_}≥c−_1 log(1</sup><sup>_/β_)</sup><sup>_certify_(</sup><sup>_α, β_)</sup><sup>_-_</sup> _reliability. In the unsaturated regime ρ_ 1 _r_<sup>_q−_1</sup> _≤_ 1 _, the second condition becomes ρ_ 1<sup>_<u>r</u>_</sup> _r_<sup>_q_</sup> _−_<sup>_−_</sup> 1<sup><u>1</u></sup><sup>_≥c−_1 log(1</sup><sup>_/β_)</sup><sup>_and it suffices_</sup> _that q ≥_ log _r_ �1 +<sup><u>(</u></sup><sup>_r−_1)</sup><sup>_c−_</sup> _ρ_<sup>1</sup> 1<sup>log(1</sup><sup>_<u>/β</u>_</sup><sup><u>)</u></sup> � _. Thus, for fixed r >_ 1 _, c >_ 0 _, and β ∈_ (0 _,_ 1) _, the geometric cumulative-mass condition is achieved at q_ = Θ(log 1 _/ρ_ 1) _rounds. If ρ_ 1 _≍ γ_<sup>_T_</sup> _, this becomes q_ = Θ( _T_ ) _._ Theorem 19 highlights a certificate-level feasibility constraint. When the horizon barrier makes the initial valid mass small, amplification that grows only polynomially with the number of rounds (e.g., simple accept/reject) cannot accumulate enough valid mass without _exponentially_ many queries. At the same time, Lemma 18 gives the sufficient hallucination certificate _qε_ fp _≤ α_ . If _ε_ fp is bounded away from zero, the certificate window can _close_ for large _T_ . In contrast, geometric amplification grows valid mass multiplicatively and can reach the abstention threshold quickly enough. 

**Implications for VLAs.** Our analysis above provides us with key takeaways. First, long-horizon planning is difficult because success is a product of conditional progress factors. This problem has been long recognized in robotics and remains applicable to contemporary VLAs. A practical (and historically natural) way to address the horizon barrier is to leverage hierarchy, e.g., verify and replan at intermediate semantic or skill boundaries, which turns one length- _T_ rare-event into many shorter-horizon problems. A complementary approach is to verify actions/plans. The verification-guided framework in Lemma 18 clarifies what test-time compute can and cannot buy with noisy verifiers. The prescriptive message is that high-level VLM/VLA planners should not treat verification as a binary filter on complete trajectories (more in Appendix C.3). They should use _feedback_ to reshape _Qj_ so that _ρj_ grows _multiplicatively_ . In robotics, gains often come from exploiting _structure_ ; planners use verifier tests/scoring (e.g., partial constraints or intermediate progress tests) to prune large families of continuations at once (e.g., via tree search). See Appendix C.7 for a short but more formal discussion. These methodologies have been recently adopted in LLMs (e.g., [51, 52, 53]) and are finding their way into VLAs [40, 41], and our theory makes clear when and why search is important. 

8 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

### **5 Conclusions, Discussion, and Future Work** 

Taken together, our results suggest that robust VLAs are unlikely to emerge from scale alone. A core challenge is _structural_ : hallucination-free and successful behavior lives on disconnected and thin subsets of action space, and long horizons turn small local errors into global failures. Our analysis points to design principles more specific than “scale the data”, “increase the number of layers”, or “add a verifier”: we should design VLA systems so that test-time computation is spent on multiplicative amplification of _valid_ behavior under controlled verification error, and _structure_ robot architectures to make that amplification possible. 

**Limitations and future work.** We view this work as a step toward a broader theory of VLAs and other RFMs such as World Action Models. Extending our theory to encompass perception, memory, and stochasticity is a natural step forward. Our verification-guided planning model also simplifies planning and verification; richer models could tighten amplification requirements and yield sharper algorithmic guidance. Beyond verification, future work can examine other reasoning approaches [54, 6, 49]. Finally, it would be interesting to extend our theory towards task distributions and to training/test-time interventions that reduce hallucinations. Progress along these lines can guide the development of next-generation VLAs that are not only more capable, but more _trustworthy_ . 

### **References** 

- [1] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In Jie Tan, Marc Toussaint, and Kourosh Darvish, editors, _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 2165–2183. PMLR, 06–09 Nov 2023. 

- [2] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model, 2024. 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [4] NVIDIA, :, Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi "Jim" Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. 

- [5] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [6] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, Winson Han, Wilbert Pumacay, Angelica Wu, Rose Hendrix, Karen Farley, Eli VanderBilt, Ali Farhadi, Dieter Fox, and Ranjay Krishna. Molmoact: Action reasoning models that can reason in space, 2025. 

- [7] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

- [8] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. RDT-1b: a diffusion foundation model for bimanual manipulation. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

9 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

- [9] Qinglun Zhang, Zhen Liu, Haoqiang Fan, Guanghui Liu, Bing Zeng, and Shuaicheng Liu. Flowpolicy: Enabling fast and robust 3d flow-based policy via consistency flow matching for robot manipulation, 2024. URL `https: //arxiv.org/abs/2412.04987` . 

- [10] Xuanran Zhai, Qianyou Zhao, Qiaojun Yu, and Ce Hao. Vfp: Variational flow-matching policy for multi-modal robot manipulation, 2025. 

- [11] Xiaobing Dai, Zewen Yang, Dian Yu, Fangzhou Liu, Hamid Sadeghian, Sami Haddadin, and Sandra Hirche. Safeflow: Safe robot motion planning with flow matching via control barrier functions, 2025. 

- [12] Rui Yang, Hanyang Chen, Junyu Zhang, Mark Zhao, Cheng Qian, Kangrui Wang, Qineng Wang, Teja Venkat Koripella, Marziyeh Movahedi, Manling Li, Heng Ji, Huan Zhang, and Tong Zhang. Embodiedbench: Comprehensive benchmarking multi-modal large language models for vision-driven embodied agents. In _Forty-second International Conference on Machine Learning_ , 2025. 

- [13] Xiaogang Jia, Denis Blessing, Xinkai Jiang, Moritz Reuss, Atalay Donat, Rudolf Lioutikov, and Gerhard Neumann. Towards diverse behaviors: A benchmark for imitation learning with human demonstrations. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- [14] Liu Dai, Haina Wang, Weikang Wan, and Hao Su. Manitaskgen: A comprehensive task generator for benchmarking and improving vision-language agents on embodied decision-making. 2025. 

- [15] Tomas Lozano-Pérez. Spatial planning: A configuration space approach. _IEEE Transactions on Computers_ , C-32 (2):108–120, 1983. 

- [16] D. Hsu, J.-C. Latombe, and R. Motwani. Path planning in expansive configuration spaces. In _Proceedings of International Conference on Robotics and Automation_ , volume 3, pages 2719–2726, 1997. 

- [17] Stéphane Ross and Drew Bagnell. Efficient reductions for imitation learning. In _Proceedings of the thirteenth international conference on artificial intelligence and statistics_ , pages 661–668. JMLR Workshop and Conference Proceedings, 2010. 

- [18] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, and Ting Liu. A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. _ACM Trans. Inf. Syst._ , 43(2), January 2025. ISSN 1046-8188. 

- [19] Sheng Liu, Haotian Ye, and James Zou. Reducing hallucinations in large vision-language models via latent space steering. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [20] Ziwei Xu, Sanjay Jain, and Mohan Kankanhalli. Hallucination is inevitable: An innate limitation of large language models, 2025. 

- [21] Adam Tauman Kalai and Santosh S. Vempala. Calibrated language models must hallucinate. In _Proceedings of the 56th Annual ACM Symposium on Theory of Computing (STOC)_ , 2024. 

- [22] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea Madotto, and Pascale Fung. Survey of hallucination in natural language generation. _ACM Comput. Surv._ , 55(12), March 2023. ISSN 0360-0300. 

- [23] David Hsu, Jean-Claude Latombe, and Hanna Kurniawati. On the probabilistic foundations of probabilistic roadmap planning. _The International Journal of Robotics Research_ , 25(7):627–643, 2006. 

- [24] Matthew T Mason. Compliance and force control for computer controlled manipulators. _IEEE Transactions on Systems, Man, and Cybernetics_ , 11(6):418–432, 1981. 

- [25] Matthew Mason. The mechanics of manipulation. In _Proceedings. 1985 IEEE International Conference on Robotics and Automation_ , volume 2, pages 544–548. IEEE, 1985. 

- [26] Tomas Lozano-Perez, Matthew T Mason, and Russell H Taylor. Automatic synthesis of fine-motion strategies for robots. _The International Journal of Robotics Research_ , 3(1):3–24, 1984. 

- [27] Kris Hauser and Jean-Claude Latombe. Multi-modal motion planning in non-expansive spaces. _The International Journal of Robotics Research_ , 29(7):897–915, 2010. 

- [28] Antoine Salmona, Valentin De Bortoli, Julie Delon, and Agnes Desolneux. Can push-forward generative models fit multimodal distributions? _Advances in Neural Information Processing Systems_ , 35:10766–10779, 2022. 

- [29] Mahyar Khayatkhoei, Maneesh K. Singh, and Ahmed Elgammal. Disconnected manifold learning for generative adversarial networks. In Samy Bengio, Hanna Wallach, Hugo Larochelle, Kristen Grauman, Nicolò Cesa-Bianchi, and Roman Garnett, editors, _Advances in Neural Information Processing Systems 31_ , pages 7354–7364. Curran Associates, Inc., 2018. 

10 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

- [30] Ugo Tanielian, Thibaut Issenhuth, Elvis Dohmatob, and Jeremie Mary. Learning disconnected manifolds: a no GAN’s land. In Hal Daumé III and Aarti Singh, editors, _Proceedings of the 37th International Conference on Machine Learning_ , volume 119 of _Proceedings of Machine Learning Research_ , pages 9418–9427. PMLR, 13–18 Jul 2020. 

- [31] Thibaut Issenhuth, Ugo Tanielian, Jeremie Mary, and David Picard. Unveiling the latent space geometry of push-forward generative models. In Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett, editors, _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pages 14422–14444. PMLR, 23–29 Jul 2023. 

- [32] George Papamakarios, Eric Nalisnick, Danilo Jimenez Rezende, Shakir Mohamed, and Balaji Lakshminarayanan. Normalizing flows for probabilistic modeling and inference. _Journal of Machine Learning Research_ , 22(57):1–64, 2021. 

- [33] Vincent Stimper, Bernhard Schölkopf, and Jose Miguel Hernandez-Lobato. Resampling base distributions of normalizing flows. In Gustau Camps-Valls, Francisco J. R. Ruiz, and Isabel Valera, editors, _Proceedings of The 25th International Conference on Artificial Intelligence and Statistics_ , volume 151 of _Proceedings of Machine Learning Research_ , pages 4915–4936. PMLR, 28–30 Mar 2022. 

- [34] Sumukh K Aithal, Pratyush Maini, Zachary Chase Lipton, and J Zico Kolter. Understanding hallucinations in diffusion models through mode interpolation. In _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ , 2024. URL `https://openreview.net/forum?id=aNTnHBkw4T` . 

- [35] John H Reif. Complexity of the mover’s problem and generalizations. In _20th Annual Symposium on Foundations of Computer Science (sfcs 1979)_ , pages 421–427. IEEE Computer Society, 1979. 

- [36] John Canny. _Complexity of Robot Motion Planning_ . PhD thesis, MIT, 1988. 

- [37] Herman Kahn and Theodore E Harris. Estimation of particle transmission by random sampling. _National Bureau of Standards applied mathematics series_ , 12:27–30, 1951. 

- [38] Reuven Y Rubinstein and Dirk P Kroese. _The cross-entropy method: a unified approach to combinatorial optimization, Monte-Carlo simulation and machine learning_ . Springer Science & Business Media, 2004. 

- [39] Jacky Kwok, Christopher Agia, Rohan Sinha, Matt Foutter, Shulu Li, Ion Stoica, Azalia Mirhoseini, and Marco Pavone. Robomonkey: Scaling test-time sampling and verification for vision-language-action models. In _Second Workshop on Out-of-Distribution Generalization in Robotics at RSS 2025_ , 2025. 

- [40] Jaesik Yoon, Hyeonseo Cho, Doojin Baek, Yoshua Bengio, and Sungjin Ahn. Monte carlo tree diffusion for system 2 planning. In _Forty-second International Conference on Machine Learning_ , 2025. 

- [41] Zirui Zhao, Wee Sun Lee, and David Hsu. Large language models as commonsense knowledge for large-scale task planning. In _Proceedings of the 37th International Conference on Neural Information Processing Systems_ , NIPS ’23, Red Hook, NY, USA, 2023. Curran Associates Inc. 

- [42] Chaoyi Pan, Giri Anantharaman, Nai-Chieh Huang, Claire Jin, Daniel Pfrommer, Chenyang Yuan, Frank Permenter, Guannan Qu, Nicholas Boffi, Guanya Shi, and Max Simchowitz. Much ado about noising: Dispelling the myths of generative robotic control, 2025. 

- [43] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang, Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao, Kanishka Rao, Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Mengyuan Yan, and Andy Zeng. Do as i can and not as i say: Grounding language in robotic affordances. In _arXiv preprint arXiv:2204.01691_ , 2022. 

- [44] Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, Danny Driess, Michael Equi, Adnan Esmail, Yunhao Fang, Chelsea Finn, Catherine Glossop, Thomas Godden, Ivan Goryachev, Lachy Groom, Hunter Hancock, Karol Hausman, Gashon Hussein, Brian Ichter, Szymon Jakubczak, Rowan Jen, Tim Jones, Ben Katz, Liyiming Ke, Chandra Kuchi, Marinda Lamb, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Yao Lu, Vishnu Mano, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Charvi Sharma, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, Will Stoeckle, Alex Swerdlow, James Tanner, Marcel Torne, Quan Vuong, Anna Walling, Haohuan Wang, Blake Williams, Sukwon Yoo, Lili Yu, Ury Zhilinsky, and Zhiyuan Zhou. _π_ 0<sup>_∗_</sup> _._ 6<sup>:a vla</sup> that learns from experience, 2025. 

11 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

- [45] Sigmund H Høeg, Aksel Vaaler, Chaoqi Liu, Olav Egeland, and Yilun Du. Hybrid diffusion for simultaneous symbolic and continuous planning. _IEEE Robotics and Automation Letters_ , 2026. 

- [46] Zeyu Feng, Hao Luan, Kevin Yuchen Ma, and Harold Soh. Diffusion meets options: Hierarchical generative skill composition for temporally-extended tasks. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 10854–10860, 2025. 

- [47] Ce Hao, Xuanran Zhai, Yaohua Liu, and Harold Soh. Abstracting robot manipulation skills via mixture-of-experts diffusion policies. In _The Fourteenth International Conference on Learning Representations_ , 2026. 

- [48] Léonard Jaillet and Josep M Porta. Path planning under kinematic constraints by rapidly exploring manifolds. _IEEE Transactions on Robotics_ , 29(1):105–117, 2013. 

- [49] NVIDIA, Yan Wang, Wenjie Luo, Junjie Bai, Yulong Cao, Tong Che, Ke Chen, Yuxiao Chen, Jenna Diamond, Yifan Ding, Wenhao Ding, Liang Feng, Greg Heinrich, Jack Huang, Peter Karkus, Boyi Li, Pinyi Li, Tsung-Yi Lin, Dongran Liu, Ming-Yu Liu, Langechuan Liu, Zhijian Liu, Jason Lu, Yunxiang Mao, Pavlo Molchanov, Lindsey Pavao, Zhenghao Peng, Mike Ranzinger, Ed Schmerling, Shida Shen, Yunfei Shi, Sarah Tariq, Ran Tian, Tilman Wekel, Xinshuo Weng, Tianjun Xiao, Eric Yang, Xiaodong Yang, Yurong You, Xiaohui Zeng, Wenyuan Zhang, Boris Ivanovic, and Marco Pavone. Alpamayo-r1: Bridging reasoning and action prediction for generalizable autonomous driving in the long tail, 2026. 

- [50] Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue Yin, Zuxuan Wu, Yu-Gang Jiang, and Xipeng Qiu. Vlabench: A large-scale benchmark for language-conditioned robotics manipulation with long-horizon reasoning tasks. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 11142–11152, October 2025. 

- [51] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: deliberate problem solving with large language models. In _Proceedings of the 37th International Conference on Neural Information Processing Systems_ , NIPS ’23, Red Hook, NY, USA, 2023. Curran Associates Inc. 

- [52] Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, and Yu-Xiong Wang. Language agent tree search unifies reasoning acting and planning in language models, 2023. 

- [53] Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling llm test-time compute optimally can be more effective than scaling model parameters, 2024. 

- [54] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. In _8th Annual Conference on Robot Learning_ , 2024. 

- [55] Piermarco Cannarsa, Marc-Olivier Czarnecki, et al. Minkowski content for reachable sets. _manuscripta mathematica_ , 131(3):507–530, 2010. 

- [56] Pertti Mattila. Rectifiability; a survey. _arXiv preprint arXiv:2112.00540_ , 2021. 

12 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

## **Supplementary Material for “Action Hallucination in Generative Vision-Language-Action Models”** 

### **A Topological Barrier: Proofs and Additional Details** 

#### **A.1 Proof of Topological Barrier (Lemma 9)** 

**Lemma 9** (Topological Barrier) **.** _Suppose Assumption 8 holds and there exist zL, zR ∈Z such that πθ_ ( _s, zL_ ) _∈ UL and πθ_ ( _s, zR_ ) _∈ UR. Define the_ seam set _, Z_ seam( _s_ ) := _{z ∈Z_ : _πθ_ ( _s, z_ ) _∈A_ forb( _s_ ) _}. Then Z_ seam( _s_ ) _is nonempty and open in Z. The hallucination probability at s is strictly positive, Hθ_ ( _s_ ) = Pr _z∼pZ_ [ _z ∈Z_ seam( _s_ )] _>_ 0 _._ 

_Proof._ We fix a state _s_ and suppress the dependence on _s_ to avoid clutter. 

**Nonemptiness.** By Assumption 3, _Z_ is path-connected, so there exists a continuous path _γ_ : [0 _,_ 1] _→Z_ with _γ_ (0) = _zL_ and _γ_ (1) = _zR_ . Define the action-space path _g_ : [0 _,_ 1] _→A_ by _g_ ( _t_ ) := _πθ_ ( _s, γ_ ( _t_ )). By continuity of _z �→ πθ_ ( _s, z_ ), the map _g_ is continuous. 

By assumption, _g_ (0) _∈ UL ⊆A_ safe( _s_ ) and _g_ (1) _∈ UR ⊆A_ safe( _s_ ). If _g_ ( _t_ ) _∈A_ safe( _s_ ) for all _t ∈_ [0 _,_ 1], then _g_ would be a continuous path in _A_ safe( _s_ ) connecting a point in _UL_ to a point in _UR_ , contradicting that _UL_ and _UR_ are distinct path-connected components of _A_ safe( _s_ ) (Assumption 8(i)). Therefore, there exists _t_<sup>_⋆_</sup> _∈_ (0 _,_ 1) such that _g_ ( _t_<sup>_⋆_</sup> ) _∈A/_ safe( _s_ ), i.e., _g_ ( _t_<sup>_⋆_</sup> ) _∈A_ forb( _s_ ). Let _z_<sup>_⋆_</sup> := _γ_ ( _t_<sup>_⋆_</sup> ); then _z_<sup>_⋆_</sup> _∈Z_ seam( _s_ ), so _Z_ seam( _s_ ) is nonempty. 

**Openness.** By Assumption 8(ii), _A_ forb( _s_ ) is open in _A_ , and by construction _Z_ seam( _s_ ) = _πθ_ ( _s, ·_ )<sup>_−_1</sup> ( _A_ forb( _s_ )). Since preimages of open sets under continuous maps are open, _Z_ seam( _s_ ) is open in _Z_ . 

**Positive probability.** Pick _z_<sup>_⋆_</sup> _∈Z_ seam( _s_ ). Since _Z_ seam( _s_ ) is open in _Z_ and _Z_ is open in R<sup>_m_</sup> , there exists _r >_ 0 such that the closed ball _K_ := _B_ ( _z_<sup>_⋆_</sup> _, r_ ) _⊂Z_ seam( _s_ ) and _K ⊂Z_ . By Assumption 3, there exists _ρ_ min( _K_ ) _>_ 0 such that _ρZ_ ( _z_ ) _≥ ρ_ min( _K_ ) for almost every _z ∈ K_ . Hence 


#### **A.2 Proof of Isoperimetric Lower-Bound (Theorem 11)** 

Our quantitative bound follows the same isoperimetric / latent pre-image boundary methodology used to prove precision limitations for Lipschitz pushforward generative models [28, 30, 31], but we adapt this methodology to state-conditional action generation and interpret boundary mass as unsafe-action probability under a physically meaningful forbidden buffer assumption, with a local-Lipschitz typical-set correction. 

**Theorem 11** (Isoperimetric lower bound on action hallucination) **.** _Fix a state s satisfying Assumption 10. Let Z ∼N_ (0 _, Im_ ) _and fix a radius R >_ 0 _. Assume that the latent-to-action head z �→ πθ_ ( _s, z_ ) _is L-Lipschitz on the typical-latent ball BR_ := _{z ∈_ R<sup>_m_</sup> : _∥z∥≤ R}, i.e., ∥πθ_ ( _s, z_ ) _− πθ_ ( _s, z_<sup>_′_</sup> ) _∥≤ L ∥z − z_<sup>_′_</sup> _∥∀z, z_<sup>_′_</sup> _∈ BR and L >_ 0 _. Let ϵ_ := _W/L. For each safe mode Ui, define the latent preimage Vi_ := _πθ_ ( _s, ·_ )<sup>_−_1</sup> ( _Ui_ ) _and the in-ball mass p_<sup>(</sup> _i_<sup>_R_)</sup> := Pr � _Z ∈ Vi ∩ BR_ � _. Let q_ ( _R_ ) = Pr � _∥Z∥ > R_ � _. Then the hallucination probability at s satisfies_ 


_where_ Φ _is the CDF of the standard normal distribution._ 

_Proof._ Fix _s_ and _ℓ_ . Let _BR_ := _{z ∈_ R<sup>_m_</sup> : _∥z∥≤ R}_ , _Z ∼N_ (0 _, Im_ ), and let _γm_ ( _·_ ) denote standard Gaussian measure on R<sup>_m_</sup> , so that Pr[ _Z ∈ E_ ] = _γm_ ( _E_ ) for measurable _E_ . 

For each mode _Ui_ , define _Ai_ := _Vi ∩ BR_ , and _p_<sup>(</sup> _i_<sup>_R_)</sup> := _γm_ ( _Ai_ ). Since _Ui_ is closed and _z �→ πθ_ ( _s, z_ ) is continuous, _Vi_ is closed. Hence _Ai_ is closed, and in particular Borel, so _p_<sup>(</sup> _i_<sup>_R_)</sup> is well-defined and Gaussian isoperimetry applies to _Ai_ . 

13 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

**Step 1: Separation of in-ball preimages.** Fix _i̸_ = _j_ . If either _Ai_ or _Aj_ is empty, the claimed separation is trivial. Otherwise, take any _z ∈ Ai_ and _z_<sup>_′_</sup> _∈ Aj_ . Then _z, z_<sup>_′_</sup> _∈ BR_ , so Lipschitzness gives _∥πθ_ ( _s, z_ ) _− πθ_ ( _s, z_<sup>_′_</sup> ) _∥≤ L∥z − z_<sup>_′_</sup> _∥._ Moreover, _πθ_ ( _s, z_ ) _∈ Ui_ and _πθ_ ( _s, z_<sup>_′_</sup> ) _∈ Uj_ . By Assumption 10, dist( _Ui, Uj_ ) _≥_ 2 _W,_ and therefore 

2 _W ≤∥πθ_ ( _s, z_ ) _− πθ_ ( _s, z_<sup>_′_</sup> ) _∥≤ L∥z − z_<sup>_′_</sup> _∥._ 

Thus _∥z − z_<sup>_′_</sup> _∥≥_ 2 _W/L_ = 2 _ϵ_ . Taking the infimum over _z ∈ Ai_ and _z_<sup>_′_</sup> _∈ Aj_ yields dist( _Ai, Aj_ ) _≥_ 2 _ϵ._ 

**Step 2: Disjoint halos and inclusion in the seam inside** _BR_ **.** Fix any radius _r ∈_ (0 _, ϵ_ ). For each _i_ , define the open _r_ -halo around _Ai_ by _Si_<sup>_r_:=</sup><sup>_{z∈_R</sup><sup>_m_:0</sup><sup>_<_dist(</sup><sup>_z, Ai_)</sup><sup>_< r}._If</sup><sup>_Ai_=</sup><sup>_∅_, we take</sup><sup>_S_</sup> _i_<sup>_r_=</sup><sup>_∅_.</sup> _Disjointness._ Suppose, for contradiction, that _z ∈ Si_<sup>_r∩S_</sup> _j_<sup>_r_for some</sup><sup>_i̸_=</sup><sup>_j_.Then there exist</sup><sup>_vi∈Ai_and</sup><sup>_vj∈Aj_such</sup> that _∥z − vi∥ < r_ and _∥z − vj∥ < r_ . Hence 

_∥vi − vj∥≤∥vi − z∥_ + _∥z − vj∥ <_ 2 _r <_ 2 _ϵ,_ contradicting dist( _Ai, Aj_ ) _≥_ 2 _ϵ_ . Therefore the sets _{Si_<sup>_r}_</sup> _i_<sup>_M_</sup> =1<sup>are pairwise disjoint.</sup> 

_Halo points inside BR map to forbidden actions._ Take any _z ∈ Si_<sup>_r∩BR_.By definition of</sup><sup>_S_</sup> _i_<sup>_r_, there exists</sup><sup>_v∈Ai_such</sup> that _∥z − v∥ < r < ϵ._ Since _z, v ∈ BR_ , Lipschitzness gives 

_∥πθ_ ( _s, z_ ) _− πθ_ ( _s, v_ ) _∥≤ L∥z − v∥ < Lϵ_ = _W._ 

Because _v ∈ Ai ⊆ Vi_ , we have _πθ_ ( _s, v_ ) _∈ Ui_ . Therefore dist( _πθ_ ( _s, z_ ) _, Ui_ ) _< W._ Also, _z ∈ Si_<sup>_r_implies</sup><sup>_z∈/Ai_.</sup> Since _z ∈ BR_ and _Ai_ = _Vi ∩ BR_ , it follows that _z ∈/ Vi_ , and hence _πθ_ ( _s, z_ ) _∈/ Ui._ Thus _πθ_ ( _s, z_ ) _∈A \ Ui_ and dist( _πθ_ ( _s, z_ ) _, Ui_ ) _< W._ By the forbidden-buffer condition in Assumption 10, _πθ_ ( _s, z_ ) _∈A_ forb( _s_ ) _._ Therefore _z ∈Z_ seam( _s_ ), and we conclude 


**Step 3: Gaussian isoperimetry.** For _r ∈_ (0 _, ϵ_ ), let _A_<sup>_r_</sup> _i_<sup>:=</sup><sup>_{z∈_R</sup><sup>_m_:dist(</sup><sup>_z, Ai_)</sup><sup>_<r}_denotetheopen</sup><sup>_r_-</sup> neighborhood of _Ai_ . Since _Ai_ is closed, _Si_<sup>_r_=</sup><sup>_Ar_</sup> _i_<sup>_\ Ai._Hence</sup> Pr[ _Z ∈ Si_<sup>_r_] =</sup><sup>_γm_(</sup><sup>_A_</sup> _i_<sup>_r_)</sup><sup>_−γm_(</sup><sup>_Ai_) =</sup><sup>_γm_(</sup><sup>_A_</sup> _i_<sup>_r_)</sup><sup>_−p_(</sup> _i_<sup>_R_)</sup> _._ 

By the Gaussian isoperimetric inequality, 

Therefore 


**Step 4: Sum halos and apply the tail correction.** Since the halos _Si_<sup>_r_are pairwise disjoint,</sup> 

Moreover, 


Combining this with Step 2 gives 


14 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

This bound holds for every _r ∈_ (0 _, ϵ_ ). Letting _r ↑ ϵ_ and using continuity of Φ, we obtain 


**Remark: Small** _ϵ_ **regime.** In the situation where _ϵ_ is small, we can obtain that 


where _ϕ_ is the standard normal PDF. To see this, fix _i_ and write _xi_ := Φ<sup>_−_1</sup> ( _p_<sup>(</sup> _i_<sup>_R_)</sup> ), so that Φ( _xi_ ) = _p_<sup>(</sup> _i_<sup>_R_)</sup> . Taylor’s theorem with Lagrange remainder gives 


Summing over _i_ and subtracting Pr[ _∥Z∥ > R_ ] yields (4). 

**Remark: Optimizing over the typical-set radius** _R_ **.** We can tighten the bound in Theorem 11; for any _R >_ 0 such that _π_ ( _s, ·_ ) is Lipschitz on _BR_ with constant _LR_ , define _ϵR_ = _W/LR_ . Then (1) holds with _ϵ_ replaced by _ϵR_ and _Hθ_ ( _s_ ) is lower bounded by the supremum of the RHS over _R_ , 


### **B Precision Barrier: Proofs and Additional Details** 

#### **B.1 Proof of Precision Barrier (Lemma 13)** 

We will make use of the following lemma about the volume of tubular neighborhoods, which is based on Theorem A in [55]. 

**Lemma 20** (Volume of Tubes Around Submanifolds) **.** _Let M ⊂_ R<sup>_d_</sup> _be a compact C_<sup>1</sup> _submanifold of dimension k < d. Then there exist constants CM >_ 0 _and δ_<sup>¯</sup> _>_ 0 _such that for all_ 0 _< δ ≤ δ_<sup>¯</sup> _,_ 


_where_ Vol _denotes the d-dimensional Lebesgue measure._ 

_Proof._ For _δ >_ 0, _Mδ_ is the closed _δ_ -neighborhood of _M_ : 


Let 


denote the _m_ -dimensional Lebesgue volume of the unit Euclidean ball. Since _M_ is a compact _C_<sup>1</sup> _k_ -dimensional submanifold of R<sup>_d_</sup> , it is _k_ -rectifiable [56]. Hence Theorem A [55] applies with _n_ = _d_ and _p_ = _k_ , and yields the existence of the (finite) limit 


15 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

where Area _k_ ( _M_ ) denotes the intrinsic _k_ -dimensional surface area of _M_ (i.e., the _k_ -dimensional Hausdorff measure). Let _LM_ := Area _k_ ( _M_ ) and define 


Then lim _δ→_ 0+ _f_ ( _δ_ ) = _LM_ . Taking _ε_ = 1 in the definition of convergence, there exists _δ_ 0 _>_ 0 such that for all 0 _< δ < δ_ 0, 

_|f_ ( _δ_ ) _− LM| <_ 1 _⇒ f_ ( _δ_ ) _< LM_ + 1 _._ 

Set _δ_<sup>¯</sup> := _δ_ 0 _/_ 2. Then for all 0 _< δ ≤ δ_<sup>¯</sup> , _f_ ( _δ_ ) _≤ LM_ + 1. Multiplying through gives 


Using Lemma 20, we prove our precision barrier below. 

**Lemma 13** (Precision Barrier) **.** _Fix a state s and adopt Definition 12. Assume that the induced action law µθ_ ( _· | s_ ) _is absolutely continuous with respect to d-dimensional Lebesgue measure on A, with density p_ ( _· | s_ ) _. Then, there exist constants CM >_ 0 _and δ_<sup>¯</sup> _>_ 0 _(depending only on M) such that for all_ 0 _< δ ≤ δ_<sup>¯</sup> _, Sθ_ ( _s_ ; _δ_ ) _≤ CMδ_<sup>_d−k_</sup> _·_ ess sup _a∈Mδ p_ ( _a | s_ ) _, and hence_ 


_Proof._ Fix 0 _< δ ≤ δ_<sup>¯</sup> (where _δ_<sup>¯</sup> will be chosen below). Since _A_ safe( _s_ ; _δ_ ) _⊆Mδ_ and _p_ ( _· | s_ ) _≥_ 0, 


Since _p_ ( _a | s_ ) _≤_ ess sup _u∈Mδ p_ ( _u | s_ ) for almost every _a ∈Mδ_ , 


Applying Lemma 20 to the compact _C_<sup>1</sup> _k_ -submanifold _M ⊂_ R<sup>_d_</sup> provides constants _CM >_ 0 and _δ_<sup>¯</sup> _>_ 0 such that for all 0 _< δ ≤ δ_<sup>¯</sup> , 


Combining the above yields 


and therefore 


Note that if _Hθ_ ( _s_ ; _δ_ ) _≤ η_ , then _Sθ_ ( _s_ ; _δ_ ) _≥_ 1 _− η_ , and rearranging the success bound gives 


#### **B.2 Proof of Generative Trilemma (Theorem 14)** 

**Theorem 14** (The Precision Trilemma: Collapse, Fold, or Hallucinate) **.** _Let m_ = _d and let the action be generated by a_ = _F_ ( _z_ ) _where Z ∼ pZ. Assume F is C_<sup>1</sup> _on an open set U ⊆Z containing the support of pZ, with bounded latent density ρZ_ ( _z_ ) _≤ ρ_<sup>max</sup> _Z . Define the active latent set as Zδ_ := _F_<sup>_−_1</sup> ( _Mδ_ ) _∩ U . Define local folding and local conditioning restricted to this active set: Nδ_ := ess sup _a∈Mδ_ # _{z ∈ Zδ_ : _F_ ( _z_ ) = _a}, and σ∗_ ( _δ_ ) := ess inf _z∈Zδ σ_ min( _JF_ ( _z_ )) _, where JF_ ( _z_ ) _is the Jacobian of F and σ_ min( _JF_ ( _z_ )) _its smallest singular value. Assume F is finite-to-one on Zδ (i.e., Nδ < ∞) and σ∗_ ( _δ_ ) _>_ 0 _. Then the induced action distribution admits a density on Mδ and the hallucination rate_ 

16 

Action Hallucination in Generative Vision-Language-Action Models A PREPRINT 

_satisfies Hθ_ ( _s_ ; _δ_ ) _≥_ 1 _− CM δ_<sup>_d−k_</sup> _Nδ ρ_<sup>max</sup> _Z σ∗_ ( _δ_ )<sup>_−d_</sup> _. If the policy achieves a target hallucination level Hθ_ ( _s_ ; _δ_ ) _≤ η for some η ∈_ (0 _,_ 1) _, then the generator must satisfy_ 


_Hence, as precision tightens (δ →_ 0 _), any policy that maintains Hθ_ ( _s_ ; _δ_ ) _≤ η must either_ fold _space (Nδ →∞) or_ collapse _volume locally (σ∗_ ( _δ_ ) _→_ 0 _)._ 

_Proof._ Consider the active set _Zδ_ = _F_<sup>_−_1</sup> ( _Mδ_ ) _∩ U_ . Since _σ_ min( _JF_ ( _z_ )) _≥ σ∗_ ( _δ_ ) _>_ 0 for almost every _z ∈ Zδ_ , the Inverse Function Theorem implies that _F_ is a local diffeomorphism in a neighborhood of any point in _Zδ_ . Since supp( _pZ_ ) _⊆ U_ , the density of the pushforward distribution _a_ = _F_ ( _z_ ) is fully determined by preimages in _U_ . Using the Area Formula (change-of-variables for many-to-one maps), for almost every _a ∈Mδ_ : 


If _a ∈Mδ_ , then any preimage _z ∈ F_<sup>_−_1</sup> ( _a_ ) _∩ U_ lies in _Zδ_ by definition. We bound the terms uniformly: 

1. Density: _ρZ_ ( _z_ ) _≤ ρ_<sup>max</sup> _Z_ . 


Substituting these bounds into the sum gives, for a.e. _a ∈Mδ_ , 


Taking the essential supremum over _a ∈Mδ_ yields 


Applying Lemma 13, 


Finally, if _Hθ_ ( _s_ ; _δ_ ) _≤ η_ , then the lower bound must not exceed _η_ , i.e., 


which we can rearrange to (3). 

#### **B.3 Proof of K-step tradeoff (Corollary 15)** 

**Corollary 15** ( _K_ -step precision tradeoff) **.** _Assume the decoder is a K-step composition F_<sup>(</sup><sup>_K_)</sup> = Φ _K−_ 1 _◦· · ·◦_ Φ0 _, where each_ Φ _t is a C_<sup>1</sup> _diffeomorphism and there exist constants λt >_ 0 _such that σ_ min( _J_ Φ _t_ ( _z_ )) _≥ λt for all z. Let σ∗_ ( _δ_ ) _≥_ inf _z∈Zδ σ_ min( _JF_<sup>(</sup><sup>_K_)</sup> ( _z_ )) _≥_<sup>�</sup><sup>_K_</sup> _t_ =0<sup>_−_1</sup><sup>_λt.Then, for all_0</sup><sup>_< δ≤δ_¯</sup><sup>_, H_</sup> _θ_<sup>(</sup><sup>_K_)</sup> ( _s_ ; _δ_ ) _≥_ 1 _− CMρ_<sup>max</sup> _Z t_ =0<sup>_λt_</sup> _δ_<sup>_d−k_</sup> _. In_ �� _K−_ 1 � _−d particular, if λt ≥ λ ∈_ (0 _,_ 1) _for all t, then a necessary condition to bound the hallucination rate Hθ_<sup>(</sup><sup>_K_)</sup> ( _s_ ; _δ_ ) _≤ η ∈_ <u>1</u> 1 _−η_ (0 _,_ 1) _is K ≥ d_ log(1 _/λ_ ) �( _d − k_ ) log<sup><u>1</u></sup> _δ_<sup>+ log</sup> _CMρ_<sup><u>max</u></sup> _Z_ � _._ 

_Proof._ Since each Φ _t_ is a diffeomorphism, their composition _F_<sup>(</sup><sup>_K_)</sup> is a diffeomorphism, hence _Nδ_ = 1. The singularvalue lower bound follows from the chain rule and the standard inequality _σ_ min( _AB_ ) _≥ σ_ min( _A_ ) _σ_ min( _B_ ). Apply Theorem 14 with _Nδ_ = 1 and _σ∗_ ( _δ_ ) _≥_<sup>�</sup> _t_<sup>_λt_to obtain the hallucination bound.Rearranging and taking logs gives the</sup> number of required steps _K_ . Note that the bound is vacuous when the right-hand side is negative. 

17 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

### **C Planning Hallucinations: Proofs and Additional Details** 

#### **C.1 Proof for Horizon Barrier (Lemma 16)** 

**Lemma 16** (Horizon Barrier) **.** _Let_ ( _St_ )<sup>_T_</sup> _t_ =0<sup>_betherolloutfroms_0</sup><sup>_._</sup> _Define pt_ ( _s_ ) := Pr _Z∼pZ_ � _πθ_ ( _s, Z_ ) _∈ A_ prog( _s, t_ )� _and γt_ := sup _s∈_ Σ _t pt_ ( _s_ ) _. Then the rollout success probability factorizes and is upper bounded by_ Pr [ _f_ plan( _s_ 0 _, τθ_ ( _s_ 0 _, Z_ 0: _T −_ 1)) = 1] _≤_<sup>�</sup><sup>_T_</sup> _t_ =1<sup>_γt. Hence, H_</sup> _π_<sup>plan</sup> _θ_ ( _I_ ) _≥_ 1 _−_<sup>�</sup><sup>_T_</sup> _t_ =1<sup>_γt.In particular, if γt≤γ<_1</sup><sup>_for all_</sup> _t, then_ Pr[ _f_ plan( _s_ 0 _, τθ_ ) = 1] _≤ γ_<sup>_T_</sup> _and Hπ_<sup>plan</sup> _θ_ ( _I_ ) _≥_ 1 _− γ_<sup>_T_</sup> _._ 

_Proof._ Let _Ek_ := _{πθ_ ( _Sk, Zk_ ) _∈A_ prog( _Sk, T − k_ ) _}_ for _k_ = 0 _, . . . , T −_ 1. Under deterministic dynamics and the definition of _A_ prog, the plan is valid if and only if<sup>�</sup><sup>_T_</sup> _k_ =0<sup>_−_1</sup><sup>_Ek_occurs.By the chain rule,</sup> 


where we re-indexed with _t_ = _T − k_ , i.e., _ηt_ := Pr[ _ET −t | E_ 0 _∩· · · ∩ ET −t−_ 1] 

On the event _E_ 0 _∩· · · ∩ ET −t−_ 1, the rollout state _ST −t_ must lie in Σ _t_ by definition of _A_ prog( _ST −t−_ 1 _, t_ + 1) and Σ _t_ . Therefore _pt_ ( _ST −t_ ) _≤_ sup _s∈_ Σ _t pt_ ( _s_ ) = _γt_ pointwise on this event, implying _ηt ≤ γt_ . Hence 


and the hallucination bounds follow by complement. The _γ_<sup>_T_</sup> specialization is immediate when _γt ≤ γ_ for all _t_ . 

#### **C.2 Proof for Reliability search budget window** 

**Lemma 18** (Reliability search-budget window) **.** _Consider any verification-guided planner with budget q, verifier error rates_ ( _ε_ fp _, ε_ fn) _, and amplification schedule_ ( _ρj_ )<sup>_q_</sup> _j_ =1<sup>_. Let c_:= 1</sup><sup>_−ε_fn</sup><sup>_. Then H_(</sup><sup>_I_)</sup><sup>_≤ε_fp</sup> � _qj_ =1<sup>Pr[</sup><sup>_Cj−_1](1</sup><sup>_−ρj_)</sup><sup>_≤qε_fp</sup> _and A_ ( _I_ ) _≤_<sup>�</sup><sup>_q_</sup> _j_ =1<sup>(1</sup><sup>_−cρj_)</sup><sup>_. Consequently, the planner is certified as_(</sup><sup>_α, β_)</sup><sup>_-reliable whenever ε_fp</sup> � _qj_ =1<sup>Pr[</sup><sup>_Cj−_1](1</sup><sup>_−_</sup> _ρj_ ) _≤ α and_<sup>�</sup><sup>_q_</sup> _j_ =1<sup>(1</sup><sup>_−cρj_)</sup><sup>_≤β. The simpler sufficient certificate qε_fp</sup><sup>_≤α and_�</sup><sup>_q_</sup> _j_ =1<sup>(1</sup><sup>_−cρj_)</sup><sup>_≤βalso certifies_</sup> ( _α, β_ ) _-reliability._ 

_Proof._ Let _Fj−_ 1 denote the _σ_ -field generated by the planner’s history up to round _j −_ 1, including past proposals and verifier outcomes. On _Cj−_ 1, the proposal distribution _Qj_ is _Fj−_ 1-measurable and _τj ∼ Qj_ . 

**Hallucination bound.** Let 


be the event that round _j_ produces a false acceptance. If the planner outputs an invalid candidate, then exactly one of the events _F_ 1 _, . . . , Fq_ occurs. Thus 


By the conditional false-positive guarantee, for every history and proposed invalid candidate _τ ∈ V_<sup>_c_</sup> , 

Pr[ _f_<sup>˜</sup> _j_ ( _τ_ ) = 1 _| Fj−_ 1 _, τj_ = _τ_ ] _≤ ε_ fp _._ 

Therefore, conditioning on _Fj−_ 1, 


Taking expectations gives 

Pr[ _Fj_ ] _≤ ε_ fpE� **1** _{Cj−_ 1 _}_ (1 _− Qj_ ( _V_ ))� _._ 

By the definition of _ρj_ , with the stated convention when Pr[ _Cj−_ 1] = 0, 


18 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

Hence 


**Abstention bound.** Let _Cj_ be the event that the planner reaches round _j_ +1, equivalently that no acceptance occurred in rounds 1 _, . . . , j_ . Then _A_ ( _I_ ) = Pr[ _Cq_ ] and _C_ 0 is the sure event. Let _Tj_ be the event that round _j_ gives a true acceptance: 


Using the conditional true-acceptance guarantee, 


Since every true acceptance prevents reaching the next round, 


This recursive inequality remains valid when Pr[ _Cj−_ 1] = 0. Iterating from Pr[ _C_ 0] = 1 yields 


The certification statements follow by requiring the corresponding upper bounds on _H_ ( _I_ ) and _A_ ( _I_ ) to be at most _α_ and _β_ , respectively. 

#### **C.3 Non-adaptive proposal-and-verify window and horizon fragility** 

Lemma 18 is a useful tool to study how fast adaptation must take place. We first specialize it to the common nonadaptive case, where the planner repeatedly samples from the same proposal distribution and only uses the verifier as an accept/reject filter. 

**Corollary 21** (Non-adaptive proposal-and-verify window and horizon fragility) **.** _Consider the verification-guided planner of Lemma 18. Assume it is non-adaptive in the sense that, on every reached round, Qj_ = _Q for a fixed proposal distribution Q over PI . Let ρ_ := _Q_ ( _V_ ) _and c_ := 1 _− ε_ fn _. Then_ 


_and_ 


_Consequently, if β ∈_ (0 _,_ 1) _, cρ ∈_ (0 _,_ 1) _, and ε_ fp(1 _− ρ_ ) _>_ 0 _, the sharper non-adaptive certification window is_ 


_The cruder instance-independent upper bound q ≤ α/ε_ fp _also suffices when ε_ fp _>_ 0 _. If ε_ fp(1 _−ρ_ ) = 0 _, the non-adaptive false-positive certificate imposes no upper bound on q._ 

_Moreover, assume c >_ 0 _, β ∈_ (0 _,_ 1) _, and ρ >_ 0 _. If Q is induced by rolling out a T -step sequential policy and the horizon barrier gives ρ_ = _Q_ ( _V_ ) _≤ γ_<sup>_T_</sup> _for some γ ∈_ (0 _,_ 1) _, then any q satisfying the abstention certificate_ (1 _− cρ_ )<sup>_q_</sup> _≤ β obeys_ 


_In particular, when cγ_<sup>_T_</sup> _≤_ 1 _/_ 2 _, this certificate requires_ 


_which is exponential in T ._ 

19 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

_Proof._ In the non-adaptive case, _Qj_ = _Q_ on every reached round. For false acceptances, the proof of Lemma 18 gives directly 

Pr[ _Fj_ ] _≤ ε_ fpE[ **1** _{Cj−_ 1 _}_ (1 _− Q_ ( _V_ ))] = _ε_ fp(1 _− ρ_ ) Pr[ _Cj−_ 1] _,_ 

and summing over _j_ yields the stated hallucination bound. Similarly, at each reached round the true-acceptance probability is at least _cρ_ , so 


Iterating gives _A_ ( _I_ ) _≤_ (1 _− cρ_ )<sup>_q_</sup> . 

The certification window follows by enforcing _qε_ fp(1 _− ρ_ ) _≤ α_ and (1 _− cρ_ )<sup>_q_</sup> _≤ β_ . Since _β ∈_ (0 _,_ 1) and _cρ ∈_ (0 _,_ 1), taking logs in the abstention inequality gives _q ≥_ log _β/_ log(1 _− cρ_ ). 

For the horizon-fragility statement, the abstention certificate implies 


The map _x �→−_ log(1 _− cx_ ) is increasing on [0 _,_ 1 _/c_ ) for _c >_ 0. Since _ρ ≤ γ_<sup>_T_</sup> , the denominator is at most _−_ log(1 _− cγ_<sup>_T_</sup> ), giving 


Finally, if _x_ := _cγ_<sup>_T_</sup> _≤_ 1 _/_ 2, then _−_ log(1 _− x_ ) _≤_ 2 _x_ , and therefore 


#### **C.4 Cumulative valid-mass condition for abstention control** 

**Corollary 22** (Cumulative valid-mass condition for abstention control) **.** _Under the assumptions of Lemma 18,_ 


_If c >_ 0 _and β ∈_ (0 _,_ 1) _, a sufficient condition for A_ ( _I_ ) _≤ β is_ 


_Proof._ From Lemma 18, 


Since _cρj ≥_ 0 and 1 _− x ≤ e_<sup>_−x_</sup> for all _x ≥_ 0, 


The sufficient condition follows by rearranging exp( _−c_<sup>�</sup> _j_<sup>_ρj_)</sup><sup>_≤β_.</sup> 

#### **C.5 Proof for Amplification-rate to beat the horizon barrier** 

**Theorem 19** (Amplification-rate to beat the horizon barrier) **.** _Consider the planner above, with amplification schedule_ ( _ρj_ )<sup>_q_</sup> _j_ =1<sup>_.Any_(</sup><sup>_α, β_)</sup><sup>_-reliable planner must satisfy_�</sup><sup>_q_</sup> _j_ =1<sup>Pr[</sup><sup>_Cj−_1]</sup><sup>_ρj≥_1</sup><sup>_−α −β, Assume an exponentially small_</sup> _initial valid mass ρ_ 1 _≤ γ_<sup>_T_</sup> _for some γ ∈_ (0 _,_ 1) _. Then_ (i) **_Polynomial amplification is insufficient._** _If ρj ≤ ρ_ 1 _j_<sup>_p_</sup> _for some fixed p ≥_ 0 _, then meeting the necessary condition requires q ≥_ �1 +<sup><u>(</u></sup><sup>_<u>p</u>_</sup><sup><u>+1)(</u></sup> _γ_<sup>1</sup><sup>_T−α−β_</sup><sup><u>)</u></sup> �1 _/_ ( _p_ +1) _−_ 1 _. For fixed p, γ ∈_ (0 _,_ 1) _, and nontrivial reliability target_ 1 _− α − β >_ 0 _, this lower bound grows exponentially in T ;_ (ii) 

20 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

**_Geometric amplification is sufficient, if within the verifier budget._** _Assume c_ := 1 _− ε_ fn _>_ 0 _, β ∈_ (0 _,_ 1) _, and ρj ≥_ min _{_ 1 _, ρ_ 1 _r_<sup>_j−_1</sup> _} for some r >_ 1 _. Then qε_ fp _≤ α and_<sup>�</sup><sup>_q_</sup> _j_ =1<sup>min</sup><sup>_{_1</sup><sup>_, ρ_1</sup><sup>_rj−_1</sup><sup>_}≥c−_1 log(1</sup><sup>_/β_)</sup><sup>_certify_(</sup><sup>_α, β_)</sup><sup>_-_</sup> _reliability. In the unsaturated regime ρ_ 1 _r_<sup>_q−_1</sup> _≤_ 1 _, the second condition becomes ρ_ 1<sup>_<u>r</u>_</sup> _r_<sup>_q_</sup> _−_<sup>_−_</sup> 1<sup><u>1</u></sup><sup>_≥c−_1 log(1</sup><sup>_/β_)</sup><sup>_and it suffices_</sup> _that q ≥_ log _r_ �1 +<sup><u>(</u></sup><sup>_r−_1)</sup><sup>_c−_</sup> _ρ_<sup>1</sup> 1<sup>log(1</sup><sup>_<u>/β</u>_</sup><sup><u>)</u></sup> � _. Thus, for fixed r >_ 1 _, c >_ 0 _, and β ∈_ (0 _,_ 1) _, the geometric cumulative-mass condition is achieved at q_ = Θ(log 1 _/ρ_ 1) _rounds. If ρ_ 1 _≍ γ_<sup>_T_</sup> _, this becomes q_ = Θ( _T_ ) _._ 

_Proof._ Define the valid set of plans, 

_E_ val := _{τ_ ˆ _̸_ = _⊥∧ τ_ ˆ _∈ V },_ 

so _S_ ( _I_ ) = Pr[ _E_ val]. If the planner outputs a valid candidate, then some reached round must have proposed a valid candidate. Therefore 

By the union bound, 


If the planner is ( _α, β_ )-reliable, then _S_ ( _I_ ) = 1 _− A_ ( _I_ ) _− H_ ( _I_ ) _≥_ 1 _− α − β_ . Hence 


**(i)** If _ρj ≤ ρ_ 1 _j_<sup>_p_</sup> and _ρ_ 1 _≤ γ_<sup>_T_</sup> , then 


where the last inequality follows from<sup>�</sup><sup>_q_</sup> _j_ =1<sup>_jp≤_</sup> �0 _q_<sup>(</sup><sup>_x_+ 1)</sup><sup>_p dx_.Combining this upper bound with the necessary</sup> condition and rearranging gives 


For fixed _p_ , _γ ∈_ (0 _,_ 1), and 1 _− α − β >_ 0, this grows exponentially in _T_ . 

**(ii)** Lemma 18 gives _H_ ( _I_ ) _≤ qε_ fp, so _qε_ fp _≤ α_ certifies the hallucination constraint. The same lemma also gives 


using 1 _− x ≤ e_<sup>_−x_</sup> . Under the assumed geometric lower bound, 


Thus _A_ ( _I_ ) _≤ β_ is certified whenever 


If _ρ_ 1 _r_<sup>_q−_1</sup> _≤_ 1, this sum is _ρ_ 1( _r_<sup>_q_</sup> _−_ 1) _/_ ( _r −_ 1), giving the displayed unsaturated sufficient condition and the equivalent lower bound on _q_ within that regime. 

21 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

It remains to justify the stated Θ(log(1 _/ρ_ 1)) scaling for the geometric cumulative-mass condition. Let _L_ := _c_<sup>_−_1</sup> log(1 _/β_ ) _>_ 0 be fixed. For an upper bound, take 

_q_ = _⌈_ log _r_ (1 _/ρ_ 1) _⌉_ + _⌈L⌉_ + 1 _._ 

By this time the terms min _{_ 1 _, ρ_ 1 _r_<sup>_j−_1</sup> _}_ have saturated, and there are at least _⌈L⌉_ unit terms, so the cumulative mass is at least _L_ . Thus _q_ = _O_ (log(1 _/ρ_ 1)) suffices. For a lower bound, if _q ≤_<sup><u>1</u></sup> 2<sup>log</sup><sup>_r_(1</sup><sup>_/ρ_1), then all terms are unsaturated for</sup> small _ρ_ 1 and 


which is eventually smaller than the fixed positive threshold _L_ . Hence any _q_ satisfying the cumulative-mass condition is Ω(log(1 _/ρ_ 1)), and the scaling is Θ(log(1 _/ρ_ 1)). If _ρ_ 1 _≍ γ_<sup>_T_</sup> , this becomes Θ( _T_ ). 

#### **C.6 Action Chunking and the Barriers** 

A common intuition is that if the primitive action is very low-level (e.g., small joint deltas), then the safe set _A_ safe( _s_ ) = _{a_ : _f_ phys( _s, a_ ) = 1 _}_ is often connected in many states, seemingly avoiding the topological barrier from Section 3.1. This is frequently true at the _one-step_ level, but it does _not_ remove multimodality for long-horizon goal-reaching. Chunking trades _fewer decisions_ against a _harder per-decision sampling problem_ : 

1. _Topology reappears at the progress/chunk level._ Even if _A_ safe( _s_ ) is connected for small one-step controls, the _progress_ set _A_ prog( _s, t_ ) can be disconnected at reachability bottlenecks. Two small safe actions can lead into different time-bounded reachable basins Σ _t−_ 1, while “in-between” actions can be safe but _non-progress_ (leading to dead ends or timeouts). Chunking amplifies this effect since the progress set typically decomposes into more separated components (distinct partial trajectories/contact-mode prefixes), activating the same “seam” phenomenon from Section 3.1, now with respect to progress/plan validity rather than one-step physical invalidity. 

2. _Precision compounds within a chunk._ In contact-rich tasks (Section 3.2), progress may require staying in a thin tube (or near a manifold) over multiple successive steps. Requiring consecutive steps in the chunk to remain in such a tube makes the feasible region effectively thinner, decreasing the per-sample mass of _A_ prog( _s, t_ ) (often sharply) as the chunk length grows. 

3. _Horizon compounding improves in count, worsens in mass._ If the policy outputs chunks of length _ℓ_ and commits to executing them, then Lemma 16 applies with an _effective_ horizon of roughly _⌈T/ℓ⌉_ . Increasing _ℓ_ reduces the number of factors in this product (helping the horizon barrier) but typically decreases each factor _γt_ (harder chunk feasibility due to topology/precision and open-loop drift), creating a natural “sweet spot” in _ℓ_ . 

This view also clarifies a common empirical design; predict long chunks for temporal coherence but execute only a short prefix before replanning (receding-horizon), which reduces open-loop compounding and delays irreversible mode commitment while still leveraging temporally structured proposals. 

#### **C.7 Family-level pruning and valid-mass amplification** 

This appendix subsection formalizes the intuition from the VLA discussion. Fix a round _j_ and write _ρ_ = _Qj_ ( _V_ ). Suppose a partial check identifies a measurable family of invalid continuations _Bj ⊆ V_<sup>_c_</sup> , discards this family, and preserves every valid continuation. Let _Q_<sup>+</sup> _j_<sup>be the proposal distribution obtained by renormalizing</sup><sup>_Qj_on</sup><sup>_PI\ Bj_.</sup> Assume _Qj_ ( _Bj_ ) _<_ 1. Then 


If the pruning step removes at least a _κ_ fraction of the invalid mass, namely _Qj_ ( _Bj_ ) _≥ κQj_ ( _V_<sup>_c_</sup> ) for some _κ ∈_ [0 _,_ 1], then 


In particular, while _Qj_ ( _V_ ) _≤_ 1 _/_ 2, 


Thus, a pruning operation that repeatedly removes a constant fraction of the currently invalid region can multiply the valid mass by a constant factor until the distribution is no longer dominated by invalid continuations. This is a simple analysis of what hierarchical decomposition, prefix feasibility tests, early collision checks, branch-and-bound, tree search, and replanning are meant to accomplish: they eliminate families of bad futures, rather than merely rejecting isolated completed samples. 

22 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

### **D Experimental Setup** 

#### **D.1 Topology Barrier** 

This appendix describes the implementation and hyperparameters used for the 2D band topology experiments in which we measure action hallucination and relate it to the isoperimetric lower bound. All experiments were run on a cloud server (4 vCPUs, 15 GB Memory) with two NVIDIA T4 GPUs. 

**Band action-space geometry and safe modes.** Actions are two-dimensional, _a_ = ( _x, y_ ) _∈_ R<sup>2</sup> , with an _action band_ 


Within this band, the safe set is the union of _M_ disconnected horizontal strips _{Ui}_<sup>_M_</sup> _i_ =1<sup>separated by forbidden gaps.</sup> Let _r_ denote the strip half-width and _W_ denote the gap half-width. The strip centers are placed symmetrically about 0 with spacing 2( _r_ + _W_ ), i.e. 


The safe strips are 


Any action outside the band, or in the gaps between strips, is forbidden and counted as a hallucination. 

**Training data distribution.** We train on i.i.d. safe actions sampled from the union of strips. In the experiments reported here, we perform the following: 

- sample mode index _i ∼_ Categorical( _π_ ) with _π_ uniform over modes, 

- sample _x ∼_ Uniform[ _x_ min _, x_ max], 

- sample _y ∼_ Uniform[ _µi − r, µi_ + _r_ ]. 

**Models.** All methods produce actions deterministically from a latent/noise variable in R<sup>2</sup> ; throughout, the base latent distribution is _Z ∼N_ (0 _, I_ 2). We implemented two models: 

- **Flow Matching.** We train a rectified flow vector field _vθ_ ( _x, t_ ) with _t ∈_ [0 _,_ 1] using flow-matching: 


with target velocity _v_<sup>_⋆_</sup> ( _xt, t_ ) = _x_ 1 _−x_ 0, optimized via MSE _∥vθ_ ( _xt, t_ ) _−v_<sup>_⋆_</sup> ( _xt, t_ ) _∥_ 2<sup>2. Sampling is deterministic</sup> Euler (or Heun) integration from _t_ = 1 to _t_ = 0 starting at Gaussian noise. 

- **Diffusion.** We train a v-pred diffusion model with cosine schedule (default _T_ = 200) and exponential moving average (EMA) of parameters. Training uses MSE on the _v_ -prediction target. Sampling is deterministic DDIM (i.e. _η_ = 0) with a user-specified number of sampling steps. 

Both the flow and diffusion networks use the same backbone: a sinusoidal time embedding of dimension 64, concatenated with the 2D input, followed by an MLP (depth 4 with hidden layers of width 256), with `LayerNorm` and `SiLU` activations, and a final linear layer to R<sup>2</sup> . We optimize with AdamW (default learning rate 2 _×_ 10<sup>_−_4</sup> , weight decay 10<sup>_−_4</sup> ), batch size 2048, and gradient-norm clipping at 1 _._ 0. Unless otherwise stated, we train each model for 100 _,_ 000 steps. 

**Evaluation protocol and metrics.** For each configuration (defined by ( _M, W_ ) and the “smoothness” settings), and for each random seed, we generate _N_ = 10<sup>6</sup> samples in batches of 4096. For each method we compute the (i) Hallucination probability, _H_ = Pr[ _a_ ( _Z_ ) _∈∪/_<sup>_M_</sup> _i_ =1<sup>_Ui_], where any sample outside the band or in the gaps counts as forbidden, and (ii)</sup> the mode masses: _pi_ = Pr[ _a_ ( _Z_ ) _∈ Ui_ ] for _i ∈{_ 1 _, . . . , M }_ . We estimate a distribution of local Lipschitz proxies on the typical latent ball _BR_ = _{z_ : _∥z∥≤ R}_ with _R_ = 3 _._ 0 by sampling 2048 points from _Z ∼N_ (0 _, I_ 2) truncated to _BR_ , and estimating _σ_ max( _z_ ) _≈∥J_ ( _z_ ) _∥_ op via finite differences with step size 0.01. 

#### **D.2 Precision Barrier** 

We study a controlled “glass/mug grasp” proxy in which valid actions lie on a low-dimensional manifold _M ⊂_ R<sup>_d_</sup> . Similar to the topological experiments, we train two generative models (Flow Matching and Diffusion, as in the topology 

23 

Action Hallucination in Generative Vision-Language-Action Models 

A PREPRINT 

experiments) on the same synthetic manifold distribution and compare them under consistent evaluation. Each action is represented by a 7D vector 


where yaw is encoded as (sin _,_ cos) to avoid discontinuities at _±π_ . Coordinates are normalized so that a Euclidean distance meaningfully mixes translational and rotational components. 

**Ideal side-grasp manifold.** The ideal grasp manifold _M_ is parameterized by two intrinsic coordinates: 

- _θ ∈_ [0 _,_ 2 _π_ ): angle around the mug, 

- _h_ in a valid height interval [ _h_ min _, h_ max]. 

This defines a _k_ = 2 dimensional manifold embedded in an ambient space of dimension _d_ = 7, hence codimension _d − k_ = 5. Points on _M_ satisfy: (i) ( _x, y_ ) lies on a ring of fixed radius _r_ (mug radius plus clearance), (ii) roll and pitch are zero, (iii) yaw points inward toward the mug center (a deterministic function of _θ_ ), and (iv) _h_ lies in [ _h_ min _, h_ max]. For any _a ∈_ R<sup>7</sup> , we compute 


where Π _M_ is an analytic projection that solves for the best _θ_<sup>_∗_</sup> (by jointly aligning the ( _x, y_ ) ring constraint and yaw (sin _,_ cos) consistency), clamps _h_ to [ _h_ min _, h_ max], and sets roll/pitch to 0. 

**Evaluation protocol and metrics.** For a trained model, we generate i.i.d. samples _{x_<sup>(</sup><sup>_i_)</sup> _}_<sup>_N_</sup> _i_ =1<sup>and evaluate the action</sup> hallucination curve 


over a log-spaced grid _δ ∈_ [ _δ_ min _, δ_ max]. To probe whether concentration near a lower-dimensional manifold requires illconditioned transformations, we analyze Jacobians of sampler maps. Let a sampler consist of step maps _xk_ +1 = _Fk_ ( _xk_ ), for _k_ = 0 _, . . . , K −_ 1, so the overall map is _G_ = _FK−_ 1 _◦· · · ◦ F_ 0. We compute per-step Jacobians _Jk_ = _∂Fk/∂x_ and the global Jacobian 


Conditioning is summarized via singular values _σ_ min( _J_ ) and diagnostics are computed along random sampler trajectories initialized from Gaussian noise. 

### **Author Contributions and LLM Usage** 

H. Soh conceived the central idea and wrote the majority of the manuscript. E. Lim verified the proofs and contributed improvements to the technical statements. LLMs were used to assist with idea exploration, proof development, code implementation, and manuscript editing. Illustrative images depicting the robot in various environments were generated using Gemini, while all schematic figures were created by the authors. All plots were produced from experiments described in the paper and appendix. The authors take full responsibility for the content of this work. 

24 

