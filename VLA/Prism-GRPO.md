---
title: "Prism-GRPO: Faster VLA Policy Optimization via Splitting Same-outcome Groups"
date: "2026-08-18"
authors: "Zeyun Deng; Yuzhe Lu; Yawei Wang; Linbo Liu; Qing Ping; Han Ding"
url: https://arxiv.org/abs/2608.17423
pdf: https://arxiv.org/pdf/2608.17423
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.17423)** / [論文ページ](https://arxiv.org/abs/2608.17423)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



# **Prism-GRPO: Faster VLA Policy Optimization via Splitting Same-outcome Groups** 

**Zeyun Deng**<sup>1∗</sup> **, Yuzhe Lu**<sup>2</sup> **, Yawei Wang**<sup>2</sup> **, Linbo Liu**<sup>2</sup> **, Qing Ping**<sup>2</sup> **, Han Ding**<sup>2</sup> **, Guande Wu**<sup>2</sup> **, Panpan Xu**<sup>2</sup> **, Jun Huan**<sup>2</sup> 

1Purdue University 2AWS AI 

#### **Abstract** 

GRPO is increasingly used for reinforcement learning of vision-language-action (VLA) policies because, unlike PPO, it does not require training a critic. This simplification comes with a sampling cost: group-relative advantages require multiple rollouts from each scene. Under binary success rewards, groups whose rollouts all succeed or all fail have zero advantage and are discarded by dynamic sampling. These groups are especially common early in training, when most rollouts fail, wasting much of the expensive robotic rollout budget. We introduce Prism-GRPO, which augments binary outcome reward with a weighted trajectory-level execution-quality score. By splitting same-outcome groups into a quality spectrum, Prism-GRPO recovers training signal while ensuring that every success still outranks every failure. Quality scores can be derived from simulator contacts, executed actions, or visual observations, avoiding task-specific progress rewards. We prove that Prism-GRPO never increases the probability that a sampled group is discarded for having zero advantages, and derive a gradient-alignment condition under which its combined update remains a local ascent direction for task success. Across four RoboTwin tasks spanning different horizons and coordination patterns, Prism-GRPO improves success and quality at matched rollout budgets and reaches target success rates with up to 56% fewer rollouts. It also suppresses a reward-hacking shortcut, with the cleaner behavior transferring under direct deployment to a real robot. Through ablations, we show consistent gains across contact-, smoothness-, and VLM-derived quality signals. 

## **1 Introduction** 

Reinforcement learning is a standard way to improve visionlanguage-action (VLA) policies beyond supervised finetuning, and GRPO (Shao et al. 2024) is attractive because it avoids a learned critic by comparing rollouts within a group. Under a binary success reward, however, GRPO can be highly sample-inefficient. If all trajectories in a group succeed, or all of them fail, every rollout receives the same reward. The group has no advantage spread, produces no gradient, and is discarded by dynamic sampling (Yu et al. 2026). GRPO therefore learns only from mixed-outcome groups, wasting the samples collected in degenerate groups. 

Recent LLM reasoning work revives degenerate groups using finer-grained signals. RL-ZVP uses the policy’s output entropy (Le et al. 2025), CAST uses self-teacher guidance (Li 

∗Work was done during an internship at AWS AI. 


Figure 1: **Illustrative overview.** Binary GRPO discards allsuccess and all-failure groups because identical rewards yield zero advantage. Prism-GRPO splits them by execution quality to recover informative, success-aligned updates. 

et al. 2026b), and LLM-as-a-Verifier (Kwok et al. 2026) uses an external verifier’s scoring-token logits. In robotics, the execution itself provides a natural signal. Two rollouts with the same outcome may differ in unintended contact, object disturbance, or motion smoothness. Unlike task progress, these properties describe how the task is executed rather than how far it has advanced, making them reusable across manipulation tasks. The only requirement is an observable trajectory score aligned with successful execution, leaving its definition and measurement flexible. We turn this observation into **Prism-GRPO** , **P** olicy optimization by **R** efining **I** dentical-outcome groups into a quality **S** pectrum for **M** ore efficient GRPO. As illustrated in Figure 1, Prism-GRPO uses execution quality to turn otherwise discarded same-outcome groups into informative updates. Breaking reward ties alone, however, does not guarantee progress toward task success. Prism-GRPO therefore preserves success dominance by construction; we further characterize when the recovered signal advances success. Our contributions are threefold: 

- We introduce Prism-GRPO for reinforcement learning of VLA policies on robotic tasks, combining binary task suc- 

cess with bounded trajectory quality to recover training signal from same-outcome rollouts. 

- We prove that Prism-GRPO never increases the expected number of rollouts needed to obtain an informative group. Under success–quality gradient alignment, its combined update is a first-order ascent direction for both objectives. 

- Across four RoboTwin tasks, Prism-GRPO reaches target success rates with up to 56% fewer rollouts while improving execution quality. The gains hold across contact-, smoothness-, and VLM-derived signals, and cleaner behavior transfers under direct real-robot deployment. 

## **2 Related Work** 

**Vision-language-action models.** Vision-language-action (VLA) models map visual observations and a language instruction to a robot action, typically the target pose and gripper state across the arm’s degrees of freedom, on top of a pretrained vision-language backbone. They split by how that action is represented. OpenVLA (Kim et al. 2024; Kim, Finn, and Liang 2025) discretizes each degree of freedom into bins and emits one token per degree of freedom, so control becomes next-token prediction over a fixed action vocabulary; the _π_ models (Black et al. 2024; Intelligence et al. 2025) instead use a flow-matching head that outputs continuous actions directly. Pretrained by imitation, these policies are capped at their demonstration quality; reinforcement learning is the standard fine-tuning stage that lifts them past it. 

**Reinforcement learning for VLA policies.** RL for continuous control has long relied on PPO (Schulman et al. 2017), which estimates advantages with a separate value network. GRPO (Shao et al. 2024) removes this critic, scoring a group of trajectories on the same input against their mean reward, and has driven much of the progress in LLM post-training. Carrying it over to VLA policies is harder than it looks: Liu et al. (2026) find that a single trajectory-level reward cannot fairly credit individual actions when each physically moves the agent. SimpleVLA-RL (Li et al. 2025) nonetheless makes GRPO effective for VLAs by adapting the rollout process to encourage exploration, through dynamic sampling that discards and resamples same-outcome groups, a raised upper clipping bound (clip-higher, following DAPO (Yu et al. 2026)), a higher rollout temperature, and no KL penalty. We build directly on this recipe. 

**Enriching the binary reward.** The binary reward used by SimpleVLA-RL (Li et al. 2025) is cheap to check but blind within an outcome: all successes score alike and so do all failures. A common way to add signal is to replace or augment success with graded feedback. RoboReward (Lee et al. 2026) learns a vision-language reward model from robot data, while stage-level process rewards such as StARe-VLA (Xu et al. 2025) use task-specific intermediate scores. LLM-asa-Verifier (Kwok et al. 2026) provides another source of graded feedback, computing continuous verifier scores from scoring-token logits rather than discrete judge outputs and using these scores as dense rewards. 

**Reviving degenerate groups.** Under binary rewards, same-outcome GRPO groups have zero advantage spread 

and provide no update. Recent LLM reasoning work asks whether these zero-variance groups can still provide useful signal, but differs in where that signal comes from. **RLZVP** (Le et al. 2025) is the closest baseline to ours and the first to treat zero-variance groups themselves as useful training data, reviving them with entropy from the policy’s own output distribution. Other methods add extra assistance. **EDGE-GRPO** (Zhang et al. 2025) combines entropy-driven advantages with guided error correction that supplies failed samples with oracle reference solutions, introducing additional supervision beyond the sampled rollouts. **CAST** (Li et al. 2026b) uses an additional self-teacher pass for tokenlevel guidance, while **LLM-as-a-Verifier** (Kwok et al. 2026) uses an external verifier’s scoring-token logits to produce continuous scores rather than discrete judge labels. These methods are designed around LLM reasoning, where intermediate reasoning quality is hard to measure directly. VLA rollouts are physical executions, so their trajectories already expose quality signals such as collisions, object disturbance, or smoothness. Prism-GRPO directly ranks same-outcome rollouts using trajectory signals, without oracle references, helper models, or policy-confidence proxies. 

**Gradient conflict in multi-objective learning.** Two objectives on one policy may have gradients that oppose each other, so the averaged update improves one at the other’s expense. Prior work addresses this by gating or projecting auxiliary gradients (Du et al. 2018; Yu et al. 2020), or by controlling their influence through learned weights or strict priorities (Gupta et al. 2023; Berducci et al. 2021). These methods assume conflict. We instead target manipulation settings where higher-quality behavior tends to support task completion, allowing the two rewards to be added directly. 

## **3 Preliminary** 

**GRPO with binary reward and compositional reward.** We cast VLA control as a Markov decision process ( _S, A, P, R, ρ_ 0): at each step the policy _πθ_ observes a state _st ∈S_ (images and the instruction), takes an action _at ∈A_ (a robot command), and the environment transitions by _P_ ( _st_ +1 _| st, at_ ). A full episode is a trajectory _τ_ = ( _s_ 0 _, a_ 0 _, . . ._ ), and RL seeks the _θ_ maximizing the expected return E _τ ∼πθ_ [ _R_ ( _τ_ )]. GRPO optimizes this objective without a learned value function: on each scene it samples a _group_ of _G_ trajectories from _πθ_ , scores them _R_ 1 _, . . . , RG_ , and forms each advantage by subtracting the group’s baseline reward, so the signal is purely relative (Shao et al. 2024). The reward itself is left to the practitioner. 

**Definition 1** (Degenerate group) **.** A group is degenerate if _R_ 1 = _· · ·_ = _RG_ , yielding zero advantages and no gradient; otherwise, it is informative. 

**Definition 2** (Objective gradients and alignment) **.** Let _πθ_ have parameters _θ ∈_ R<sup>_d_</sup> , and define the success and quality objectives as _J_ ( _θ_ ) = E _x,τ_ [success( _τ_ )] and _Q_ ( _θ_ ) = E _x,τ_ [ _q_ ( _τ_ )]. Their gradients _g_ success = _∇θJ_ ( _θ_ ) and _g_ quality = _∇θQ_ ( _θ_ ) lie in the same parameter space. They _align_ if _⟨g_ success _, g_ quality _⟩≥_ 0 and _conflict_ otherwise. 

#### **Algorithm 1** Prism-GRPO 

**Require:** _πθ_ , scene _x_ , group size _G_ , _λ ∈_ (0 _,_ 1) 

1: **repeat** 

- 2: sample _τ_ 1 _, . . . , τG ∼ πθ_ ( _· | x_ ) 

- 3: _Ri ←_ success( _τi_ ) + _λ q_ ( _τi_ ) 

4: **until** not all _Ri_ are equal {discard _G_ rollouts per retry} 5: _A_<sup>ˆ</sup> _i ← Ri − G−_ <u>1</u> 1 � _j̸_ = _i_<sup>_Rj_</sup> 6: update _θ_ using _{A_<sup>ˆ</sup> _i}_ 

## **4 Prism-GRPO** 

### **4.1 Reward design and problem formulation** 

**Tasks, scenes, trajectories.** A task _T_ (e.g. stacking two cubes) induces a distribution over scenes; we write _x ∼_ Scene( _T_ ) for a scene, consisting of an initial configuration together with its instruction. Running _πθ_ on _x_ produces a trajectory _τ ∼ πθ_ ( _· | x_ ), scored by a binary outcome success( _τ_ ) _∈{_ 0 _,_ 1 _}_ and a continuous quality score _q_ ( _τ_ ) _∈_ [0 _,_ 1], where _q_ ( _·_ ) is a measurement of quality, such as smoothness, larger the better. A GRPO group drawns _G_ trajectories on the same scene _x_ . 

**Quality-augmented reward.** Prism-GRPO starts with the binary outcome reward and adds execution quality. For a trajectory _τ_ , we define 


This turns tied binary rewards into a success-dominant reward spectrum. As illustrated in Figure 2, an all-failure group has all rewards equal to 0 under the binary reward, and vise versa; therefore, both have no spread of advantages. The quality term breaks these ties by refining failures within [0 _, λ_ ] and successes within [1 _,_ 1 + _λ_ ]. Since _λ <_ 1, the two bands remain separated: every success still scores above every failure, while quality only reorders trajectories within an outcome class. We pair this reward with the leave-one-out (RLOO) advantage estimator (Kool, van Hoof, and Welling 2019; Ahmadian et al. 2024), which subtracts the siblings’ mean but does not divide by the group standard deviation. This matters on same-outcome groups, where the entire reward spread is _λq_ : standard GRPO normalization would cancel the scale of _λ_ (Arora and Zanette 2025), while RLOO preserves the raw quality differences. 

**Analysis target.** Our goal is to improve rollout efficiency without sacrificing task success, while also improving execution quality. Relative to Binary GRPO, Prism-GRPO should reach the same target value of the success objective _J_ ( _θ_ ) using no more generated rollouts and, at that point, attain at least as large a value of the quality objective _Q_ ( _θ_ ). 

### **4.2 When Quality Supports Success** 

**Task-level correlation remains informative.** The quality term is useful only if higher-quality trajectories are also more likely to succeed. We measure this relationship directly from rollouts using the task-level correlation _κ_ 2 = Corr _x∼_ Scene( _T_ ) _, τ ∼πθ_ ( _·|x_ )[ _q_ ( _τ_ ) _,_ success( _τ_ )], where _x_ 


Figure 2: **Prism-GRPO splits same-outcome groups into a reward spectrum.** Colors indicate rewards. _λ_ =0.2. 

denotes a sampled scene, _τ_ a trajectory generated by the current policy _πθ_ , _q_ ( _τ_ ) the trajectory quality, and success( _τ_ ) _∈ {_ 0 _,_ 1 _}_ the task outcome. Although many GRPO groups become degenerate, _κ_ 2 remains meaningful because it is computed over all scenes rather than within a single group. Its covariance Cov( _q,_ success) decomposes as 


where _q_ ¯( _x_ ) = E[ _q_ ( _τ_ ) _| x_ ] and ¯ _s_ ( _x_ ) = E[success( _τ_ ) _| x_ ] are the average quality and success rate on scene _x_ . The withinscene term vanishes when a scene is saturated (all rollouts share the same outcome), but the between-scene term can remain positive because the policy tends to achieve higher quality on easier scenes where it succeeds more often. Consequently, _κ_ 2 continues to capture the overall quality–success relationship even when many GRPO groups are degenerate. 

**From correlation to gradient alignment.** Our theory assumes population-level alignment, _⟨g_ success _, g_ quality _⟩≥_ 0, where _g_ success = _∇θ_ E[success] and _g_ quality = _∇θ_ E[ _q_ ]. To study this condition, we analyze a single softmax decision and identify a sufficient mechanism for alignment. Let _ρ_ ( _s_ ) denote the policy-weighted correlation between the actions’ success and quality values. The proposition below shows that sufficiently high _ρ_ ( _s_ ) yields decision-level alignment. 

**Proposition 1.** _Consider a single softmax decision at state s over K actions, with distribution π_ = _πθ_ ( _· | s_ ) _. Let uk and vk denote the success and quality values of action k, and let ρ_ ( _s_ ) = Corr _k∼π_ ( _uk, vk_ ) _be their policy-weighted correlation. Assume both u and v take at least two distinct values under π. Let Dπ_ = diag( _π_ ) _, and let κπ ≥_ 1 _be its condition number on the policy-centered subspace. It measures how unevenly probability is distributed across actions: κπ_ = 1 _for a uniform policy and can increase as the policy becomes more concentrated. Appendix A.3 gives the precise definition and proof. Writing g_ success( _s_ ) _and g_ quality( _s_ ) _for the corresponding policy gradients,_ 


**Interpretation and scope.** The threshold ( _κπ −_ 1) _/_ ( _κπ_ + 1) depends on policy conditioning: it is 0 for a uniform policy and approaches 1 only under extreme concentration. Modern RL methods discourage such collapse through clip-higher, temperature sampling, and entropy regularization (Yu et al. 2026; Cui et al. 2025; Simoni et al. 2025); our implementation inherits clip-higher and temperature-1 sampling from SimpleVLA-RL (Li et al. 2025). For example, _π_ = (0 _._ 97 _,_ 0 _._ 015 _,_ 0 _._ 015) has _κπ ≈_ 2 _._ 9, requiring _ρ_ ( _s_ ) _≈_ 0 _._ 49 for decision-level alignment. This gives a tractable alignment mechanism at a single decision, but does not establish population-level alignment across scenes, states, and stochastic long-horizon trajectories. Finite rollouts yield noisy estimates, and reliable verification would require many batches with full-model gradient aggregation. We therefore retain _⟨g_ success _, g_ quality _⟩≥_ 0 as an explicit assumption, report correlation diagnostics in Appendix H, and evaluate it empirically in full Prism-GRPO training. 

### **4.3 The combined update points toward success** 

Under the alignment condition in Section 4.2, the combined gradient improves quality without sacrificing success. 

**Proposition 2** (The combined gradient ascends both success and quality) **.** _Whenever the population gradients align, ⟨g_ success _, g_ quality _⟩≥_ 0 _, the combined direction g_ combined = _g_ success + _λg_ quality _is a first-order ascent direction for both the success objective J_ ( _θ_ ) _and the quality objective Q_ ( _θ_ ) _. In particular, ⟨∇θJ, g_ combined _⟩≥∥g_ success _∥_<sup>2</sup> _and ⟨∇θQ, g_ combined _⟩≥ λ∥g_ quality _∥_<sup>2</sup> _. Both are non-negative and are strictly positive whenever the corresponding gradient is nonzero. The proof is given in Appendix A.2._ 

Proposition 2 shows that _g_ combined preserves first-order progress on success, with directional derivative at least _∥g_ success _∥_<sup>2</sup> , while also improving quality. Thus, the quality signal can improve execution quality without pulling the update away from the target success level. 

### **4.4 Improved sample efficiency** 

Dynamic sampling discards zero-advantage groups. We measure sample efficiency by rollouts per informative group. 

**Theorem 1** (The combined reward is at least as sample-efficient as the binary reward) **.** _Fix a scene with success rate p ∈_ (0 _,_ 1) _and group size G ≥_ 2 _, and let δ_ ( _p_ ) _be the probability that all G combined rewards in a group coincide. The expected rollouts per informative group are C_ binary( _p_ ) = _G/_ (1 _− p_<sup>_G_</sup> _−_ (1 _− p_ )<sup>_G_</sup> ) _and C_ combined( _p_ ) = _G/_ (1 _− δ_ ( _p_ )) _, respectively. They satisfy_ 


The proof, including coincident combined rewards, is given in Appendix A.1. For continuous conditional quality scores, exact ties occur with probability zero, so _C_ combined( _p_ ) = _G_ and every group is informative. At _p_ = 0 _._ 1 or 0 _._ 9, Binary GRPO then requires approximately 1 _._ 76 _×_ as many rollouts for _G_ = 8 and 2 _._ 91 _×_ for _G_ = 4. 

**Rescued groups train quality, yet still move success.** Theorem 1 is a fixed-scene statement: near _s_ ¯( _x_ ) = 0 or _s_ ¯( _x_ ) = 1 every rollout in the group shares an outcome, so the binary term is constant and the group’s entire advantage spread comes from _λq_ . Such a rescued group thus contributes only _g_ quality, and appears to train quality alone. It does not. By the alignment above, _g_ quality projects non-negatively onto _g_ success, so the quality-only gradient from a saturated scene still advances the task-level success objective, which Proposition 2 defines over all scenes rather than any one group. This fails only when _g_ success = 0 over the whole task, meaning _s_ ¯( _x_ ) = 1 everywhere, where the task is solved, or _s_ ¯( _x_ ) = 0 everywhere, where no trajectory ever succeeds. The zerosuccess case also defeats standard GRPO, which likewise assumes an SFT initialization with some task competence to bootstrap RL (Li et al. 2025); Ours requires no more. 

## **5 Experiments** 

**Benchmark and training setup.** All experiments use RoboTwin 2.0 (Chen et al. 2025a), a bimanual manipulation benchmark with domain randomization over clutter, lighting, background, tabletop height, and language instruction. Each randomized task instance defines a scene _x ∼_ Scene( _T_ ), and all rollouts in a GRPO group are sampled from the same scene. Thus, group degeneracy is determined per scene, while training aggregates updates across scenes. We evaluate four tasks: _Lift Pot_ , _Move Can Pot_ , _Handover Block_ , and _Beat Block Hammer_ , spanning effectively single-arm and bimanual control as well as short- to long-horizon manipulation. Task details are provided in Appendix C.1. Following SimpleVLA-RL (Li et al. 2025), we use _G_ = 8 and 512 rollouts per update, replacing the binary reward with success + _λq_ . We use _λ_ = 0 _._ 2 by default and ablate it in the main paper. Appendix G provides the _G_ ablation and shows that applying the combined reward to all groups is necessary to realize the full gains; thus, we use it for all groups in the main experiments. We train each configuration with five random seeds and report means with standard-error intervals. 

**Default quality signal.** In the main experiments, we derive _q_ from **GT-Max Force** , defined as the largest force applied to any non-target object during a rollout (Appendix B.1). For example, in _Lift Pot_ , the pot is the target object and all other objects are treated as non-target. We use this signal because unintended contacts are common, easy to measure, and can displace objects or interfere with later execution. Unless otherwise specified, the resulting quality score is used as _q_ during training. Figure 6 evaluates two additional collisionbased signals and three smoothness-based signals, showing that Prism-GRPO is not tied to a specific quality definition. 

**Evaluation metrics.** We evaluate both task success and execution quality. **Success rate** is the fraction of completed trials. **Calibrated success rate** discounts successful trajectories according to the number of non-target contacts, regardless of contact force. **Max-Force Quality** measures the severity of the strongest non-target contact and corresponds to the default GT-Max Force training signal. **Sum-Impulse Quality** aggregates impulse over all non-target contacts throughout the trajectory, capturing the overall collision burden. 


Figure 3: **Main results.** _λ_ = 0 _._ 2. Stars mark each curve’s peak mean success, and arrows show the rollouts saved by Prism-GRPO when matching Binary GRPO’s peak mean success. 

These metrics capture complementary aspects of collision quality. Unless otherwise specified, calibrated success rate and Max-Force Quality are our primary success and quality metrics. All non-binary metrics are normalized to [0 _,_ 1], with higher values indicating better performance. Appendix B.2 provides metric definitions, while Appendix G.1 reports all metrics for experiments not fully shown in the main paper. 

**Baselines.** We compare Prism-GRPO against four baselines. **Binary GRPO** is the SimpleVLA-RL configuration, using the binary success reward with standard groupstandardized advantages. **Binary RLOO** replaces this estimator with leave-one-out advantages. **Random quality** preserves the binary success term but replaces the quality score _q_ with a random scalar, testing whether the gains come from meaningful quality information rather than random variation. **RL-ZVP** (Le et al. 2025) revives degenerate groups using entropy-shaped advantages; we adapt it to manipulation with per-step action entropy. We exclude methods requiring extra supervision, such as external verifiers, self-teacher passes, or oracle demonstrations; external scoring is covered by the **VLM-Predicted** ablation. Full details are in Appendix E. 

### **5.1 Sample Efficiency and Execution Quality** 

**Prism-GRPO improves rollout efficiency and execution quality.** Figure 3 compares all methods against total generated rollouts across four tasks. At matched rollout budgets, Prism-GRPO improves rollout savings over Binary GRPO by 22–56%, with calibrated success following the same trend. The largest gain occurs on _Lift Pot_ , where Binary GRPO 

discards 70% of the earliest rollout batches and stabilizes at 20% through the rest of training, whereas Prism-GRPO keeps the discard rate at essentially 0% early on and around 14% throughout the remainder. Appendix G.1 reports detailed rollout statistics for all tasks. Moreover, when Prism-GRPO reaches a given target success rate, it also exhibits higher execution quality. Although Prism-GRPO is trained using Max-Force Quality, it also improves Sum-Impulse Quality at evaluation, demonstrating cross-metric generalization rather than overfitting to a specific collision measure. On Handover Block, RL-ZVP shows much worse quality than the other methods: catastrophic contacts with multiple objects can disrupt the tabletop scene, as illustrated in Figure 4(right). Overall, Prism-GRPO performs best among the baselines, except that RL-ZVP reaches higher raw success on _Move Can Pot_ ; however, its large gap between raw and calibrated success shows that many successful rollouts hacked the binary checker. We explain this shortcut behavior next. 

**Shove-cheat exploitation on** **_Move Can Pot_ .** The _Move Can Pot_ instruction requires the arm to lift the can and place it beside the pot, whereas the success checker considers only the final geometry: the can must end beside the pot, regardless of whether it was lifted or whether the pot moved. This mismatch permits a shove-cheat, where the arm pushes the pot toward a stationary can and is still marked successful. Figure 4 (left) illustrates the behavior qualitatively: RL-ZVP strikes and displaces the pot instead of performing the instructed lift-and-place. Figure 5 reports the shove-cheat rate, where a shove-cheat is defined as a successful rollout that 


Figure 4: **Qualitative examples. Left:** _Move Can Pot_ : RL-ZVP shove-cheat vs. clean executions by the other methods. **Right:** _Handover Block_ shows worse failures cause stronger unintended contacts and larger scene disturbance. 


Figure 5: **Shove-cheat behavior on** **_Move Can Pot_ .** 5 seeds each; ticks = per-seed rate, band = min–max, dot = mean. 

||||Ra|ndom||||Prism|-GR|PO||
|---|---|---|---|---|---|---|---|---|---|---|---|
|Task|Metric|0.2|0.5|0.9|1|2|0.2|0.5|0.9|1|2|
|Lift Pt|<sup>CS</sup>|**_×_**|**_×_**|**_×_**|**_× _**|**_×_**|**56**|49|45|25|53|
|o|<br>Q|**_×_**|**_×_**|**_×_**|**_× _**|**_×_**|11|14|15|14|26|
|Move|CS|24|33|**_×_**|**_× _**|**_×_**|**41**|48|41|3|**_×_**|
|Can Pot|Q|1|0|**_×_**|**_× _**|**_×_**|7|10|13|16|**_×_**|


Table 1: **Quality-weight** _λ_ **ablation.** CS is the rollout saving (%) to match Binary GRPO’s calibrated success; Q is the quality gain at that point. **_×_** denotes an unreached success. 

displaces the pot by at least 10 cm. RL-ZVP ranges from 0 _._ 6–20 _._ 0% and Binary GRPO from 0 _._ 7–7 _._ 0%, whereas all Prism-GRPO seeds remain within 0 _._ 6–1 _._ 3%. The highest RL-ZVP rate is over 15 _×_ that of Prism-GRPO. 

**Quality steers online RL away from reward shortcuts.** Online RL can discover behaviors beyond the SFT policy (Li et al. 2025), but imperfect success checkers may also reward unintended shortcuts (Skalse et al. 2022; Yao et al. 2026). On _Move Can Pot_ , shoving the pot satisfies the geometric checker, so Binary GRPO treats it as equivalent to a clean lift-and-place. RL-ZVP may further reinforce this shortcut through policy confidence without assessing execution quality. Prism-GRPO instead ranks successful trajectories by non-target contact, preserving exploration while favoring cleaner solutions. This reduces the shove-cheat rate to nearly zero and highlights execution quality as a natural signal available from robot trajectories. 

### **5.2 Sensitivity to Quality Weight** 

**Meaningful quality is robust to** _λ_ **, while random quality is not.** We vary _λ_ to test weight sensitivity and success dominance, and compare with random quality to verify the value of meaningful signals. Results are in Table 1, with full curves in Appendix G.2. Within the success-dominant regime, _λ <_ 1, Prism-GRPO consistently reaches the target, saving 45–56% of rollouts on _Lift Pot_ and 41–48% on _Move Can Pot_ , while improving quality by 11–15 and 7–13 points, respectively. Since _q ∈_ [0 _,_ 1], _λ <_ 1 preserves success dom- 

inance, whereas _λ ≥_ 1 allows failures to tie or outrank successes and yields less stable performance. The strong _λ_ = 2 result on _Lift Pot_ is an outlier, as the same setting fails to reach the target on _Move Can Pot_ . Figure 3 shows that Random quality can improve success early. By making reward ties unlikely, the random term revives all-failure groups that Binary GRPO would discard. Under GRPO clipping bias (Shao et al. 2025), these updates may reinforce favored actions and increase success. However, as the success rate approaches 0 _._ 5, mixed-outcome groups become common and this tiebreaking benefit largely vanishes. Because random quality provides no success- or quality-aligned signal, its gains are unstable and yield little execution-quality improvement. 

### **5.3 Generalization Across Quality Sources** 

We test Prism-GRPO across quality sources, treating quality as any observable trajectory signal aligned with success. 

**Quality-source generalization.** Figure 6 evaluates collision cleanliness and motion smoothness using signals from different sources. For collision quality, **Prism-Peak (Default)** uses the strongest force applied to any non-target object, **Prism-Count** uses the number of such contacts, and **Prism-VLM-Contact** replaces simulator contact data with a zero-shot Qwen3-VL judge to emulate settings in which such data are unavailable. These signals save 38–56% of rollouts while improving collision quality. Prism-VLM-Contact yields the weakest gains among them, consistent with its imperfect agreement with ground-truth contact labels (F1 


Figure 6: **Quality-source ablation.** Evaluated on _Lift Pot_ . 


Figure 7: **Real-world behaviors.** Top: clean placement from Prism-GRPO (Ours). Bottom: shove-cheat from RL-ZVP. 

_≈_ 0 _._ 765). For motion quality, **Prism-Flips** counts armjoint reversals, **Prism-Jerk** measures the largest abrupt action change, and **Prism-MeanFlips** averages reversal counts across action chunks. These signals save 25–44% of rollouts while improving motion quality. See Appendix B.1 for details. Overall, Prism-GRPO is not tied to a particular metric or source: a single trajectory can expose diverse quality signals that distinguish same-outcome rollouts. 

**Quality adds little training overhead.** Adding trajectory quality incurs little relative cost to training. Simulator- and VLM-derived quality add only 0.04% and 4.8% wall-clock time, respectively, Rollout generation cost remains dominant. 

### **5.4 Real-World Evaluation** 

Simulation may assign the same success label to behaviors with very different execution quality. The shove-cheat on _Move Can Pot_ provides a clear test case: both clean placement and shoving can succeed in simulation, allowing us to examine whether the higher-quality behavior favored by Prism-GRPO transfers more reliably to hardware at comparable success. We evaluate Binary GRPO, RL-ZVP, and Prism-GRPO on Piper over 25 trials each. 

**Execution quality improves sim-to-real reliability.** The real-world rollouts clarify why this shortcut emerges. In simulation, the appropriate arm depends on the can’s position relative to the pot: the right arm acts when the can is on the right, whereas the left arm should act when it is on the left. In some left-side scenes, however, the policy reuses the learned rightarm pickup motion and strikes the intervening pot. A strong simulated contact can displace the pot unrealistically far, allowing the shove to satisfy the geometric success checker 

|Metric|Binary GRPO|RL-ZVP|Prism-GRPO|
|---|---|---|---|
|Clean Success|4/25 (16%)|2/25 (8%)|**6/25 (24%)**|
|Shove-Cheat|1/25 (4%)|5/25 (20%)|**0/25 (0%)**|


Table 2: **Real-world results.** Clean Success counts trials that move the can beside the pot without using the shove-cheat. 

without executing the intended left-arm manipulation. On hardware, the same impact produces much less displacement because of real contact dynamics and safety-limited actuation, so these low-quality simulator successes often fail after deployment. Figure 7 contrasts an RL-ZVP shove-cheat with a clean Prism-GRPO placement. Consistent with simulation, RL-ZVP cheats most often, Binary GRPO occasionally, and Prism-GRPO not at all while maintaining comparable clean success (Table 2). Setup details are in Appendix I. 

## **6 Discussion and Conclusion** 

**Positioning.** To our knowledge, Prism-GRPO is the first VLA RL method to improve sample efficiency by recovering training signal from same-outcome groups. PolicyTrim and Z-1 instead target deployment and rollout-generation efficiency (Wang et al. 2026; Cao et al. 2026). RoboReward can break reward ties using continuous scores, but requires training an additional reward model (Lee et al. 2026). SmoothVLA improves motion quality among successful trajectories but does not target sample efficiency (Li et al. 2026a). TGRPO and GiGPO study credit assignment (Chen et al. 2025b; Feng et al. 2026), whereas RLinfVLA and VLAJS focus on scalable training and guided exploration (Zang et al. 2025; Moroncelli et al. 2026). These directions are complementary, but none directly recovers training signal from rollouts lost to same-outcome groups. 

**Limitations and conclusion.** Prism-GRPO requires an observable trajectory signal aligned with success. Such signals are readily available in robotics through contacts, actions, and vision, but may require proxies or external verifiers in other domains. Theoretically, Prism-GRPO never increases the rollout cost of obtaining an informative group and, when the population-level success and quality gradients align, its update improves both objectives. Verifying this alignment directly in full VLA models remains challenging. Overall, Prism-GRPO recovers degenerate groups while preserving success dominance, improving sample efficiency and execution quality across tasks, signals, and real-world deployment. 

## **Acknowledgments** 

Zeyun Deng at the DT Lab, Purdue University, would like to thank her advisor Ziran Wang and co-advisor Ruqi Zhang for their support in approving her summer internship. She also thanks Kai Cheng and Zhengyuan Li from Purdue University for helpful discussions. The authors would also like to sincerely thank the UCLA Mobility Lab for providing access to the robot platform and providing the basic camera synchronization code used in our real-world experiments, which significantly saved our development time. 

## **References** 

Ahmadian, A.; Cremer, C.; Gallé, M.; Fadaee, M.; Kreutzer, J.; Pietquin, O.; Üstün, A.; and Hooker, S. 2024. Back to basics: Revisiting REINFORCE-style optimization for learning from human feedback in LLMs. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , 12248–12267. 

Arora, D.; and Zanette, A. 2025. Training language models to reason efficiently. _arXiv preprint arXiv:2502.04463_ . 

Berducci, L.; Aguilar, E. A.; Ničković, D.; and Grosu, R. 2021. Hierarchical potential-based reward shaping from task specifications. _arXiv preprint arXiv:2110.02792_ . 

Black, K.; Brown, N.; Driess, D.; Esmail, A.; Equi, M.; Finn, C.; Fusai, N.; Groom, L.; Hausman, K.; Ichter, B.; et al. 2024. _π_ 0: A Vision-Language-Action Flow Model for General Robot Control. _arXiv preprint arXiv:2410.24164_ . Cao, L.; Chen, R.; Li, L.; Wang, P.; Peng, M.; and Li, Y. 2026. Z-1: Efficient Reinforcement Learning for Vision-LanguageAction Models. _arXiv preprint arXiv:2606.31846_ . 

Chen, T.; Chen, Z.; Chen, B.; Cai, Z.; Liu, Y.; Li, Z.; Liang, Q.; Lin, X.; Ge, Y.; Gu, Z.; et al. 2025a. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ . 

Chen, Z.; Niu, R.; Kong, H.; Wang, Q.; Xing, Q.; and Fan, Z. 2025b. Tgrpo: Fine-tuning vision-language-action model via trajectory-wise group relative policy optimization. _arXiv preprint arXiv:2506.08440_ . 

Cui, G.; Zhang, Y.; Chen, J.; Yuan, L.; Wang, Z.; Zuo, Y.; Li, H.; Fan, Y.; Chen, H.; Chen, W.; et al. 2025. The entropy mechanism of reinforcement learning for reasoning language models. _arXiv preprint arXiv:2505.22617_ . 

Du, Y.; Czarnecki, W. M.; Jayakumar, S. M.; Farajtabar, M.; Pascanu, R.; and Lakshminarayanan, B. 2018. Adapting auxiliary losses using gradient similarity. _arXiv preprint arXiv:1812.02224_ . 

Feng, L.; Xue, Z.; Liu, T.; and An, B. 2026. Group-ingroup policy optimization for llm agent training. _Advances in Neural Information Processing Systems_ , 38: 46375–46408. Gupta, D.; Chandak, Y.; Jordan, S.; Thomas, P. S.; and C da Silva, B. 2023. Behavior alignment via reward function optimization. _Advances in Neural Information Processing Systems_ , 36: 52759–52791. 

Intelligence, P.; Black, K.; Brown, N.; Darpinian, J.; Dhabalia, K.; Driess, D.; Esmail, A.; Equi, M.; Finn, C.; Fusai, N.; et al. 2025. _π_ 0 _._ 5: a Vision-Language-Action Model with Open-World Generalization. _arXiv preprint arXiv:2504.16054_ . 

Kim, M. J.; Finn, C.; and Liang, P. 2025. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ . 

Kim, M. J.; Pertsch, K.; Karamcheti, S.; Xiao, T.; Balakrishna, A.; Nair, S.; Rafailov, R.; Foster, E.; Lam, G.; Sanketi, P.; et al. 2024. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ . 

Kool, W.; van Hoof, H.; and Welling, M. 2019. Buy 4 reinforce samples, get a baseline for free! 

Kwok, J.; Li, S.; Atreya, P.; Liu, Y.; Jiang, Y.; Finn, C.; Pavone, M.; Stoica, I.; and Mirhoseini, A. 2026. LLM-as-aVerifier: A General-Purpose Verification Framework. _arXiv preprint arXiv:2607.05391_ . 

Le, T.-L. V.; Jeon, M.; Vu, K.; Lai, V.; and Yang, E. 2025. No prompt left behind: Exploiting zero-variance prompts in llm reinforcement learning via entropy-guided advantage shaping. _arXiv preprint arXiv:2509.21880_ . 

Lee, T.; Wagenmaker, A.; Pertsch, K.; Liang, P.; Levine, S.; and Finn, C. 2026. RoboReward: General-Purpose VisionLanguage Reward Models for Robotics. _arXiv preprint arXiv:2601.00675_ . 

Li, H.; Zuo, Y.; Yu, J.; Zhang, Y.; Yang, Z.; Zhang, K.; Zhu, X.; Zhang, Y.; Chen, T.; Cui, G.; et al. 2025. Simplevlarl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ . 

Li, J.; Shi, X.; Xie, H.; Shang, M.; and Lu, Y. 2026a. SmoothVLA: Aligning Vision-Language-Action Models with Physical Constraints via Intrinsic Smoothness Optimization. _arXiv preprint arXiv:2603.13925_ . 

Li, Y.; Xue, G.; Guo, Y.; Yuan, Y.; Hu, L.; and Ma, L. 2026b. CAST: Non-Privileged Clipped Asymmetric SelfTeaching with Advantage Flipping for GRPO. _arXiv preprint arXiv:2606.00172_ . 

Xu, F.; Zhai, G.; Kong, X.; Fu, T.; Gordon, D. F.; An, X.; and Busam, B. 2025. STARE-VLA: Progressive Stage-Aware Reinforcement for Fine-Tuning Vision-Language-Action Models. _arXiv preprint arXiv:2512.05107_ . 

Yao, J.; Wang, Y.; Zhang, A.; Sun, Z.; Wang, S.; Mei, L.; Ge, Y.; and Liu, S. 2026. Multimodal Reward Hacking in Reinforcement Learning. _arXiv preprint arXiv:2607.09492_ . 

Yu, Q.; Zhang, Z.; Zhu, R.; Yuan, Y.; Zuo, X.; Yue, Y.; Dai, W.; Fan, T.; Liu, G.; Liu, L.; et al. 2026. Dapo: An opensource llm reinforcement learning system at scale. _Advances in Neural Information Processing Systems_ , 38: 113222– 113244. 

Yu, T.; Kumar, S.; Gupta, A.; Levine, S.; Hausman, K.; and Finn, C. 2020. Gradient surgery for multi-task learning. _Advances in neural information processing systems_ , 33: 5824– 5836. 

Zang, H.; Wei, M.; Xu, S.; Wu, Y.; Guo, Z.; Wang, Y.; Lin, H.; Shi, L.; Xie, Y.; Xu, Z.; et al. 2025. Rlinf-vla: A unified and efficient framework for vla+ rl training. _arXiv preprint arXiv:2510.06710_ . 

Zhang, X.; Wen, S.; Wu, W.; and Huang, L. 2025. Edgegrpo: Entropy-driven grpo with guided error correction for advantage diversity. _arXiv preprint arXiv:2507.21848_ . 

Liu, J.; Gao, F.; Wei, B.; Chen, X.; Liao, Q.; Wu, Y.; Yu, C.; and Wang, Y. 2026. What can rl bring to vla generalization? an empirical study. _Advances in Neural Information Processing Systems_ , 38: 97121–97151. 

Moroncelli, A.; Zanetti, R.; Maccarini, M.; and Roveda, L. 2026. Vision-Language-Action Jump-Starting for Reinforcement Learning Robotic Agents. _arXiv preprint arXiv:2604.13733_ . 

Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; and Klimov, O. 2017. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ . 

Shao, R.; Li, S. S.; Xin, R.; Geng, S.; Wang, Y.; Oh, S.; Du, S. S.; Lambert, N.; Min, S.; Krishna, R.; et al. 2025. Spurious rewards: Rethinking training signals in rlvr. _arXiv preprint arXiv:2506.10947_ . 

Shao, Z.; Wang, P.; Zhu, Q.; Xu, R.; Song, J.; Bi, X.; Zhang, H.; Zhang, M.; Li, Y.; Wu, Y.; et al. 2024. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ . 

Simoni, M.; Fontana, A.; Rossolini, G.; Saracino, A.; and Mori, P. 2025. Gtpo: Stabilizing group relative policy optimization via gradient and entropy control. _arXiv preprint arXiv:2508.03772_ . 

Skalse, J.; Howe, N.; Krasheninnikov, D.; and Krueger, D. 2022. Defining and characterizing reward gaming. _Advances in Neural Information Processing Systems_ , 35: 9460–9471. 

Wang, X.; Chen, F.; Zhang, W.; Yan, H.; Wang, Z.; Li, C.; and Lei, Y. 2026. PolicyTrim: Boosting Intrinsic Policy Efficiency of Vision-Language-Action Models. _arXiv preprint arXiv:2606.22540_ . 

**A Proofs** at least _∥g_ success _∥_<sup>2</sup> and the second at least _λ∥g_ quality _∥_<sup>2</sup> , each strictly positive when the corresponding gradient is nonzero. 

### **A.1 Proof of Theorem 1** 

_Proof._ Fix a scene with success rate _p ∈_ (0 _,_ 1) and group size _G ≥_ 2. Let _t_ succ be the probability that all _G_ quality scores coincide given that all _G_ trajectories succeed, and let _t_ fail be the analogous probability given that all _G_ fail; both lie in [0 _,_ 1]. 

### **A.3 Proof of Proposition 1** 

Throughout this appendix we abbreviate _gS_ = _g_ success and _gQ_ = _g_ quality, and for a positive definite _A_ we write 

Under the binary reward every trajectory scores 0 or 1, so a group is degenerate exactly when all _G_ trajectories succeed or all _G_ fail. By independence this has probability _p_<sup>_G_</sup> +(1 _−p_ )<sup>_G_</sup> , and a group is informative with probability 1 _− p_<sup>_G_</sup> _−_ (1 _− p_ )<sup>_G_</sup> . Dynamic sampling draws fresh groups until the first informative one, so the number of groups is geometric with that success probability. At _G_ rollouts per group, 


for the _A_ -metric cosine between nonzero vectors _w, z_ , so that cos _I_ is the ordinary Euclidean cosine. 

**Lemma 1** (Metric cosine under bounded conditioning) **.** _Let A ≻_ 0 _be self-adjoint with eigenvalues in_ [ _m, M_ ] _and condition number κ_ = _M/m. For nonzero w, z with Euclidean cosine ρ_ = cos _I_ ( _w, z_ ) _,_ 


Under _R_ combined = success + _λq_ with 0 _< λ <_ 1, the success and failure reward ranges [1 _,_ 1+ _λ_ ] and [0 _, λ_ ] are disjoint, so a mixed-outcome group can never have all rewards equal. A combined-reward group is therefore degenerate only if all trajectories share an outcome and, given that outcome, all _G_ quality scores coincide, giving 

_In particular, if ρ ≥_ ( _κ −_ 1) _/_ ( _κ_ + 1) _then w_<sup>_⊤_</sup> _Az ≥_ 0 _._ 

_Proof._ The left side of (8) depends only on span _{w, z}_ . If _ρ_ = _±_ 1 then _w, z_ are collinear and cos _A_ ( _w, z_ ) = _ρ_ , so the claim holds. Assume _ρ ∈_ ( _−_ 1 _,_ 1), making the span twodimensional. Each of _w_<sup>_⊤_</sup> _Az_ , _w_<sup>_⊤_</sup> _Aw_ , _z_<sup>_⊤_</sup> _Az_ is unchanged when _A_ is replaced by its compression _PAP_ to this span, with _P_ the orthogonal projection onto it. By Rayleigh–Ritz the compression has eigenvalues in [ _m, M_ ], hence condition number _κ_<sup>_′_</sup> _≤ κ_ . Rescaling _A_ leaves cos _A_ unchanged, so we may take _A_ = diag(1 _, κ_<sup>_′_</sup> ) on this span. 


The combined cost never exceeds the binary one. Since _t_ succ _, t_ fail _≤_ 1, each term of (5) is at most the corresponding binary term, so _δ_ ( _p_ ) _≤ p_<sup>_G_</sup> +(1 _− p_ )<sup>_G_</sup> . A smaller degeneracy probability means a larger informative fraction 1 _− δ_ ( _p_ ), and hence fewer groups drawn: _C_ combined( _p_ ) _≤ C_ binary( _p_ ), which is (4). 

Normalize _∥w∥_ = _∥z∥_ = 1. Let _e ∥ w_ + _z_ and _f ∥ w − z_ be unit vectors; they are orthogonal, and 

The gap becomes extreme at the boundary. As _p →_ 1, the binary informative fraction 1 _−p_<sup>_G_</sup> _−_ (1 _−p_ )<sup>_G_</sup> _∼ G_ (1 _−p_ ) _→_ 0, so almost every group is degenerate and _C_ binary( _p_ ) _→_ + _∞_ ; the same holds as _p →_ 0. The combined cost does not blow up. Provided quality is not almost surely constant within an outcome, so that _t_ succ _, t_ fail _<_ 1, the quality term breaks most ties, keeping _δ_ ( _p_ ) _≤_ max( _t_ succ _, t_ fail) _<_ 1 and _C_ combined finite. Its limits are _G/_ (1 _− t_ succ) as _p →_ 1 and _G/_ (1 _− t_ fail) as _p →_ 0: at each boundary only one kind of degenerate group remains, since an all-failure group has probability (1 _− p_ )<sup>_G_</sup> _→_ 0 as _p →_ 1 and an all-success group has probability _p_<sup>_G_</sup> _→_ 0 as _p →_ 0. 


with _c_ = ~~�~~ (1 + _ρ_ ) _/_ 2, _σ_ = ~~�~~ (1 _− ρ_ ) _/_ 2, and _r_ = _σ_<sup>2</sup> _/c_<sup>2</sup> = (1 _− ρ_ ) _/_ (1 + _ρ_ ). Writing _E_ = _e_<sup>_⊤_</sup> _Ae_ , _F_ = _f_<sup>_⊤_</sup> _Af_ , _G_ = _e_<sup>_⊤_</sup> _Af_ , a direct calculation and _EF − G_<sup>2</sup> = det( _A_ ) = _κ_<sup>_′_</sup> give 


Let _θ_ be the angle between _e_ and the eigenvector of _A_ with eigenvalue 1, so _E_ = cos<sup>2</sup> _θ_ + _κ_<sup>_′_</sup> sin<sup>2</sup> _θ_ and _F_ = sin<sup>2</sup> _θ_ + _κ_<sup>_′_</sup> cos<sup>2</sup> _θ_ . As _θ_ ranges over [0 _, π_ ) the pair ( _w, z_ ) ranges over all configurations with the prescribed norms and _w_<sup>_⊤_</sup> _z_ = _ρ_ , so minimizing over _θ_ minimizes over all such pairs. Then 

### **A.2 Proof of Proposition 2** 

_Proof._ The change in an objective along a direction _w_ is its directional derivative _⟨∇θ_ ( _·_ ) _, w⟩_ . Since _∇θJ_ = _g_ success and _∇θQ_ = _g_ quality, substituting _w_ = _g_ combined = _g_ success + _λg_ quality and expanding gives 

_E − rF_ = (1 _− rκ_<sup>_′_</sup> ) cos<sup>2</sup> _θ_ + ( _κ_<sup>_′_</sup> _− r_ ) sin<sup>2</sup> _θ ≥_ 1 _− rκ_<sup>_′_</sup> _,_ 

since ( _κ_<sup>_′_</sup> _− r_ <u>)</u> _−_ <u>(1</u> _− rκ_<sup>_′_</sup> ) = ( _κ_<sup>_′_</sup> _−_ 1)(1 + _r_ ) _≥_ 0. The map _t �→ t/_ _~~√~~ t_<sup>2</sup> + 4 _rκ_<sup>_′_</sup> is increasing on R, and (1 _− rκ_<sup>_′_</sup> )<sup>2</sup> + 4 _rκ_<sup>_′_</sup> = (1 + _rκ_<sup>_′_</sup> )<sup>2</sup> , so from (10), 


By the alignment hypothesis, the cross term _⟨g_ success _, g_ quality _⟩_ is non-negative, so the first derivative is 


where the last equality follows by substituting _r_ = (1 _− ρ_ ) _/_ (1 + _ρ_ ). Finally _hκ_ ( _ρ_ ) is decreasing in _κ_ for _ρ ∈_ ( _−_ 1 _,_ 1), since 


so _κ_<sup>_′_</sup> _≤ κ_ gives _hκ′_ ( _ρ_ ) _≥ hκ_ ( _ρ_ ), proving (8). The final implication holds because the denominator of _hκ_ ( _ρ_ ) is positive for _ρ <_ 1, _κ ≥_ 1, so _hκ_ ( _ρ_ ) _≥_ 0 iff _ρ ≥_ ( _κ −_ 1) _/_ ( _κ_ + 1). 

_Proof of Proposition 1._ Fix the state _s_ , write _π_ = _πθ_ ( _· | s_ ) and _D_ = diag( _π_ ), and center the action values as ˜ _u_ = _u−u_ ¯ **1** and ˜ _v_ = _v−v_ ¯ **1** , where ¯ _u_ =<sup>�</sup> _k_<sup>_πkuk_and ¯</sup><sup>_v_= �</sup> _k_<sup>_πkvk_. For</sup> a single softmax decision the logit gradients are _gS_ = _Du_ ˜ and _gQ_ = _Dv_ ˜, so _⟨gS, gQ⟩_ = _u_ ˜<sup>_⊤_</sup> _D_<sup>2</sup> _v_ ˜. 

Put _w_ = _D_<sup>1</sup><sup>_/_2</sup> _u_ ˜ and _z_ = _D_<sup>1</sup><sup>_/_2</sup> _v_ ˜. Since ˜ _u,_ ˜ _v_ are _π_ -centered, _w_ and _z_ lie in the centered subspace 


Figure8: **Peaknon-targetcontact andobjectdisplacement on** **_Lift Pot_ .** Stronger unintended contact is associated with larger displacement of non-target objects. 

and the policy-weighted correlation is the Euclidean cosine of _w_ and _z_ , that is _ρ_ ( _s_ ) = cos _I_ ( _w, z_ ). 

Let _Pπ_ be the Euclidean projection onto _Hπ_ and set _Aπ_ = _PπDPπ|Hπ_ . Although _D_ need not preserve _Hπ_ , for _w, z ∈ Hπ_ we have _w_<sup>_⊤_</sup> _Aπz_ = _w_<sup>_⊤_</sup> _Dz_ , and therefore 


So the gradient cosine equals the _Aπ_ -metric cosine, cos _Aπ_ ( _w, z_ ), and _κπ_ is by definition the condition number of _Aπ_ on _Hπ_ . Applying Lemma 1 with _A_ = _Aπ_ , 


If _ρ_ ( _s_ ) _≥_ ( _κπ −_ 1) _/_ ( _κπ_ + 1) then _hκπ_ ( _ρ_ ( _s_ )) _≥_ 0, and since the gradient norms are positive under the non-degeneracy assumptions, _⟨gS, gQ⟩≥_ 0. 

For sharpness, when dim _Hπ ≥_ 2 let _e_ min _, e_ max be orthonormal eigenvectors of _Aπ_ with eigenvalues _mπ, Mπ_ . Given _ρ ∈_ ( _−_ 1 _,_ 1), set 


so _∥w∥_ = _∥z∥_ = 1 and _w_<sup>_⊤_</sup> _z_ = _ρ_ . Then _w_<sup>_⊤_</sup> _Aπz_ = 1+ _<u>ρ</u>_ 1 _−ρ_ 1+ _<u>ρ</u> mπ_ 2 _− Mπ_ 2 and _w_<sup>_⊤_</sup> _Aπw_ = _z_<sup>_⊤_</sup> _Aπz_ = _mπ_ 2 + _Mπ_ 1 _−_ 2 _<u>ρ</u>_<sup>, whose ratio is exactly</sup><sup>_hκπ_(</sup><sup>_ρ_). Setting ˜</sup><sup>_u_=</sup><sup>_D−_1</sup><sup>_/_2</sup><sup>_w_</sup> and _v_ ˜ = _D_<sup>_−_1</sup><sup>_/_2</sup> _z_ gives _π_ -centered action values attaining the bound. Letting _κπ →∞_ sends _hκπ_ ( _ρ_ ) _→−_ 1 for every _ρ <_ 1, so no nontrivial lower bound depending on _ρ_ alone can hold: bounded conditioning is necessary, not merely sufficient. 

## **B Quality** 

Prism-GRPO treats quality as a bounded trajectory-level score _q_ ( _τ_ ) _∈_ [0 _,_ 1], with larger values indicating cleaner 

or smoother execution. Every Prism variant uses the same success-dominant reward 


and the same RLOO advantage estimator. The variants differ only in how _q_ ( _τ_ ) is measured. This isolates the effect of the quality source while keeping the policy, success reward, and optimization procedure fixed. 

### **B.1 Quality Signals** 

**Collision signals.** We seek task-agnostic collision signals that describe how cleanly a trajectory is executed rather than how far the task has progressed. For each task, we designate the manipulated object as the target object. For example, the target is the pot in _Lift Pot_ and the can in _Move Can Pot_ . Contact with the target is required for manipulation and is therefore excluded, while contact between the robot and any other object is treated as non-target contact. 

**Simulator-based collision signals.** When simulator contact data are available, we derive two trajectory-level signals directly from the contact log. Let _C_ nt( _τ_ ) denote the set of non-target contact events in trajectory _τ_ , and let _I_ ( _c_ ) denote the impulse of event _c_ . We define 


with both quantities set to zero when no non-target contact occurs. **Prism-Peak (Default)** , referred to as **GT-Max Force** in the main paper, uses _I_ peak( _τ_ ) to capture collision severity. Stronger unintended contact is more likely to displace surrounding objects and affect subsequent execution, as illustrated in Figure 8. **Prism-Count** instead uses _N_ nt( _τ_ ) to capture collision frequency, assigning equal weight to each contact event regardless of its magnitude. 

**Prism-VLM-Contact.** When simulator contact logs are unavailable, **Prism-VLM-Contact** estimates collisions di- 

rectly from visual observations. A zero-shot Qwen3-VL235B judge receives eight temporally ordered frames and determines whether the robot contacts any object other than the task target. The prompt identifies the target, excludes its intended manipulation, and asks the judge to inspect both changes in the scene layout and brief contacts in intermediate frames. We convert its output into a binary quality signal indicating whether the trajectory is collision-free. On 256 trajectories, the judge achieves 78 _._ 9% accuracy and a contact-class F1 score of 69 _._ 0%, with 90 _._ 9% precision and 55 _._ 6% recall. It correctly recognizes 142 of 148 collision-free trajectories but detects only 60 of 108 trajectories containing contact, showing that it provides a conservative visual alternative to simulator-derived contact signals. 

#### **Full Lift Pot collision-judging prompt.** 

##### **Decision rule.** 

Decide whether the robot **COLLIDED** with anything other than its target object at any point during the trajectory. 

In this task the target object is: **THE POT** . 

Touching, gripping, closing on, lifting, holding, or moving **THE POT** is the task itself—it is **NOT** a collision, no matter how firm. The pot rising in the air, the gripper closing around the pot, and the pot leaving the table are all expected and are not counted. 

##### **What counts as a collision:** 

- The robot arm or gripper visibly contacts the table, including pressing into it, sliding along it, or pushing against it. 

- The robot contacts the wall behind it. 

- The robot bumps, knocks, slides, tips, or pushes any distractor object that is not the pot. 

- Any non-pot object visibly moves because of the robot. 

- Even a brief, light touch that displaces a non-target object counts; there is no “too gentle to count” threshold. 

##### **How to read the images:** 

- You are given _N_ frames sampled in temporal order from a single trajectory. The first image is the start of the trajectory, before the robot moves, and the last image is the end, after the robot has stopped. The middle frames are evenly spaced snapshots in between. 

- The frames are not independent. Read them as a short film. Anchor the judgment on the first frame, which shows the initial layout, and the last frame, which shows the final layout. Use the middle frames to identify contacts or displacements that occur only briefly. 

##### **How to look for collisions across frames:** 

1. Identify the pot and ignore its motion entirely because it is supposed to move. 

2. In the first frame, identify every other visible object, including the table surface, wall, and distractors. Note their positions, orientations, and stacking configurations as the reference state. 

3. Compare the last frame with the first frame for each non-target object: 

- Has it shifted left, right, forward, or backward? 

- Has it rotated, tipped, or fallen? 

- Has it been knocked off the table or scattered? 

- Any visible displacement of a non-target object between the first and last frames indicates that a collision occurred during the trajectory. 

4. Inspect the middle frames in temporal order and follow the robot arm and gripper path. Determine whether they visibly intersect the table surface, wall, or space occupied by a distractor. Contact in a middle frame counts even if the non-target object returns to its original position by the end. 

5. Look for indirect evidence, including motion blur on a distractor, the gripper momentarily pressed flat against the table, or a distractor’s shadow moving as the robot passes nearby. 

##### **Anchors:** 

- 2 — **No collision:** Comparing the last frame with the first frame, all non-pot objects remain in the same positions and orientations, and the robot never visibly contacts the table, wall, or a distractor. 

- 1 — **Collision:** At least one non-pot object visibly shifts, rotates, tips, or moves between the first and last frames, or the robot visibly contacts the table, wall, or a distractor in any frame. 

##### **Task, for context only—do not score task success:** 

Use both arms to lift the pot. 

Respond with the digit first, followed by a brief reason. Use exactly the following format: 

ANSWER: <1|2> REASON: <one short sentence naming the specific frame(s) and object(s) that drove your decision> 

**Smoothness signals.** We derive three task-agnostic smoothness signals from the executed action sequence, without requiring simulator contact data. For the 14-dimensional ALOHA action space, we use the twelve arm-joint dimensions and exclude the two gripper dimensions, so intended opening and closing motions are not treated as irregular behavior. Let _A_ denote the set of arm joints, _Kτ_ the number of action chunks in trajectory _τ_ , and _fj_ ( _τ_ ) the number of velocity-direction reversals of joint _j_ . Each signal captures a different form of irregular motion. 

**Prism-Flips.** This captures localized oscillation, where a single unstable joint repeatedly changes direction even when the remaining joints move smoothly. It uses the largest reversal count among the arm joints: 


The signal is therefore determined by the most oscillatory joint in the trajectory. 

**Prism-MeanFlips.** This captures reversals distributed across the entire arm rather than focusing on a single joint. It averages the reversal count over all arm joints: 


This signal reflects the overall level of oscillatory motion and is less sensitive to one isolated noisy joint. 


Figure 10: **Smoothness-threshold calibration on** **_Lift Pot_ .** 

**Prism-Jerk.** This captures abrupt changes in commanded arm motion rather than repeated direction reversals. Let **a**<sup>arm</sup> _t_ denote the arm-joint action vector at timestep _t_ , and let _Tτ_ denote the number of evaluated timesteps. We compute the average magnitude of the third-order action difference: 


Thus, Prism-Flips measures the most severe single-joint oscillation, Prism-MeanFlips measures oscillation across the arm, and Prism-Jerk measures the average magnitude of abrupt action changes. We evaluate the three signals separately. 

### **B.2 Metrics** 

**Quality signals and normalization.** We consider six trajectory-level quality signals. For collision, **Prism-Peak (Default)** , referred to as **GT-Max Force** in the main paper, uses the peak non-target contact impulse; **Prism-Count** uses the number of non-target contact events; and **PrismVLM-Contact** uses a zero-shot VLM to estimate non-target contacts from sampled trajectory frames. For smoothness, **Prism-Flips** uses the largest velocity-sign reversal count among the arm joints per action chunk, **Prism-MeanFlips** averages the reversal count across all arm joints, and **PrismJerk** measures action jerk. We convert each non-negative 

raw cost _r_ ( _τ_ ) into a quality score in [0 _,_ 1]: 


where larger values indicate cleaner or smoother execution. The threshold _T_ determines the normalization scale, while _r_ 0 is an optional floor for motion that is inherently required by the task. Collision signals always use _r_ 0 = 0. For PrismFlips on _Move Can Pot_ and _Beat Block Hammer_ , we use _r_ 0 = 12, estimated from the median flip count of successful SFT trajectories. This removes the reversals naturally required by grasp-and-place and lift-and-strike motions before measuring excess oscillation. 

**Calibration from the SFT policy.** Before reinforcement learning, we begin with the SFT policy. For each task, we run this policy on the same set of 256 validation scenes and examine the resulting distribution of each raw quality signal. We then choose _T_ from this distribution so that ordinary SFT trajectories retain useful variation in quality, while clearly excessive collision or motion values receive low scores. Once selected, the threshold is fixed for all subsequent RL runs and is not adjusted using RL performance, individual seeds, or reported checkpoints. 

**Collision thresholds.** For Prism-Peak, we examine the SFT distribution of peak non-target impulse for each task and place _T_ peak at the boundary between the low-impulse cluster and the high-impulse tail. The low-impulse region mainly 

contains gentle grazing or placement contacts, while the tail corresponds to more severe unintended interactions such as arm slams or object tipping. This choice preserves quality differences among relatively clean trajectories while assigning zero quality to clearly excessive contacts. As shown in Figure 9, the resulting thresholds are 10 N s for _Lift Pot_ , 6 N s for _Move Can Pot_ , and 3 N s for both _Handover Block_ and _Beat Block Hammer_ . The distributions are computed after applying the same target exemptions and grace filters used during training, including exempting task-required placement contact in _Handover Block_ and contact with the manipulated hammer in _Beat Block Hammer_ . For Prism-Count and cumulative-impulse quality, the SFT distributions have comparable scales across tasks, so we use the shared thresholds _Tn_ = 30 and _T_ Σ = 30. 

**Smoothness thresholds.** Figure 10 shows the SFT distributions used to calibrate the three smoothness thresholds on _Lift Pot_ . For Prism-Flips, we set _T_ flips = 12 near the upper tail because the signal is determined by the most oscillatory arm joint. For Prism-Jerk, we similarly set _TJ_ = 10 near the upper tail so that ordinary variation in commanded motion retains positive quality while unusually abrupt motion is penalized. Prism-MeanFlips instead averages reversals across all arm joints and has a more concentrated distribution around typical behavior. Placing its threshold at the upper tail would assign nearly all trajectories high quality and provide little distinction among them. We therefore set _T_ meanflips = 7 near the SFT median, preserving useful variation in the quality score. All three thresholds are selected before RL and remain fixed during training and evaluation. 

**Robustness to threshold choice.** The SFT-based calibration above provides a principled default for selecting _T_ , but the method should not depend critically on the exact placement of this threshold. We therefore test Prism-Peak on _Lift Pot_ using both the calibrated value _T_ peak = 10 N s and a substantially smaller value, _T_ peak = 3 N s. The latter changes the normalization scale by more than a factor of three and clips a much larger portion of the impulse distribution to zero. Despite this large change, Figure 11 shows similar learning behavior and rollout savings under both settings. This result suggests that the calibration rule provides a reasonable default, while Prism-GRPO remains effective over a broad range of threshold values and does not require precise tuning of _T_ . 

## **C Experimental Setup** 

The following configuration is shared by Prism-GRPO and all baselines. 

**Initialization.** We build directly on SimpleVLA-RL (Li et al. 2025), whose full code and supervised fine-tuning (SFT) checkpoints are publicly released. Every run in this paper, including Prism-GRPO and all baselines, starts from the same released SFT checkpoint for the corresponding task, so the methods differ only in the reinforcement-learning stage rather than initialization. 

**Algorithm 2** Adaptive gap-fill rollout generation 

- **Require:** Scene batch size _B_ , rollouts per scene _G_ , dataparallel size _D_ 

1: _V ←_ ∅ 2: _N_ gen _←_ 0 3: **while** _|V| < BG_ **do** 4: **if** _N_ gen = 0 **then** 5: _B_ req _← B_ 6: **else** 7: _N_ keep _←|V|_ 8: _r_ keep _←_ max�0 _._ 3 _,_<sup>_N_</sup> _N_<sup>kee</sup> gen<sup><u>p</u></sup> � 9: _N_ short _← BG − N_ keep 10: _B_ short _←_ <u>�</u> _<u>N</u>_ <u>short</u> _G_ � 11: _B_ � _←_ <u>1</u> _<u>.</u>_ <u>2</u> _<u>B</u>_ <u>short</u> � _r_ keep <u>�</u> 12: _B_ � _←_ max� _D,_ RoundUp( _B, D_<sup>�</sup> )� 13: _B_ req _←_ min( _B, B_<sup>�</sup> ) 14: **end if** 15: Generate _B_ req _G_ trajectories from fresh scenes 16: _N_ gen _← N_ gen + _B_ req _G_ 17: Apply dynamic filtering and append surviving trajectories to _V_ 18: **end while** 19: Retain the first _BG_ trajectories in _V_ for the policy update 

**Policy and action space.** The policy is OpenVLA-OFT with a discrete action head. Each degree of freedom is uniformly quantized into 256 bins, and one action token is emitted per degree of freedom. On RoboTwin with the ALOHA embodiment, each action chunk spans 25 steps with 14 action tokens per step. 

**Training configuration.** Each RL step samples 64 scenes with group size _G_ = 8, yielding 512 rollouts per step. We use _G_ = 8 as the default setting throughout the main paper, following the standard SimpleVLA-RL configuration; its effect is studied separately in Section G.4. We use a learning rate of 5 _×_ 10<sup>_−_6</sup> with constant warmup, gradient clipping at 1, PPO clip bounds (0 _._ 2 _,_ 0 _._ 28), no KL penalty or entropy bonus, and a rollout temperature of 1 _._ 6. 

**Avoiding unnecessary full-batch refills.** The original SimpleVLA-RL dynamic-sampling procedure refills the retained batch in fixed increments of 64 scenes, or 512 trajectories. After the initial batch is generated and degenerate groups are removed, it requests another full batch whenever the retained set falls below the target size, regardless of the remaining deficit. This can generate substantial surplus. For example, with a 95% keep rate, only about 26 additional trajectories are needed, yet the procedure still generates another 512. 

**Adaptive gap-fill rollout generation.** We replace the fixed-size refill with an adaptive strategy while keeping the optimizer batch unchanged. Each update targets _B_ = 64 retained scenes with _G_ = 8 rollouts per scene, for a total of 512 retained trajectories. After each filtering round, we 


Figure 11: **Sensitivity to the quality threshold on** **_Lift Pot_ .** Prism-Peak shows similar performance for _T_ peak _∈{_ 3 _,_ 10 _}_ N s, with 10 N s used as the default. 


Figure 12: **Task overview.** Four tasks under randomized object placements, clutter, lighting, and backgrounds. 

estimate the number of additional scenes required from the observed keep rate, lower-bound the keep-rate estimate by 0 _._ 3, add 20% headroom, round the request to a multiple of the data-parallel group size, and cap it at _B_ scenes. Refill rounds use fresh scenes and continue until the target batch is complete. Algorithm 2 gives the full procedure. All methods therefore update on the same number of retained trajectories, while every generated trajectory, including filtered and surplus trajectories, is counted toward rollout cost. 

### **C.1 Tasks** 

**Task selection.** We evaluate on four RoboTwin tasks that cover different manipulation skills and coordination patterns. _Lift Pot_ and _Handover Block_ require bimanual coordination, while _Move Can Pot_ and _Beat Block Hammer_ primarily use one arm. Together, the tasks include lifting, pick-and-place, handover, and tool use, and expose different failure modes such as unstable grasps, object tipping, inaccurate placement, failed transfer, and reward shortcuts. 

**_Lift Pot_ .** The robot uses both arms to grasp opposite sides of a pot and lift it while keeping the pot upright. The pot variant and scene configuration are randomized. Success requires a stable bimanual grasp, sufficient lifting height, and limited pot tilt. Common failures include one-sided grasps, gripper slip, and tipping during the lift. 

**_Beat Block Hammer_ .** The robot grasps a hammer with the arm closest to the block and strikes the block with the hammer head. The block pose is randomized across scenes. Success requires contact between the hammer head and the block with accurate horizontal alignment. Common failures include incorrect hammer orientation, poor strike alignment, and missing the block. 

**_Move Can Pot_ .** The robot picks up a can and places it beside a pot. The can pose, object variants, and instructed arm are randomized, while the pot remains near the center of the workspace. Success requires the can to be upright, released, and placed within the target region beside the pot. A characteristic failure is the shove-cheat, in which the policy moves the pot toward the stationary can instead of grasping 

and moving the can. 

**_Handover Block_ .** The left arm grasps a block, transfers it to the right arm, and places it on a target pad. The block and pad poses are randomized. Success requires completing the handover and releasing the block at the target location. Common failures include dropping the block during transfer, incomplete handover, and inaccurate final placement. 

## **D Advantage Calculation** 

This section describes how Prism-GRPO converts the combined reward into advantages and why the leave-one-out estimator provides learning signal for same-outcome groups whenever their trajectory qualities differ. 

**Combined reward.** Each trajectory receives _R_ ( _τ_ ) = success( _τ_ ) + _λq_ ( _τ_ ) with _λ_ = 0 _._ 2, where _q_ ( _τ_ ) _∈_ [0 _,_ 1] is the quality score defined in Section B.2. The quality term therefore lies in [0 _, λ_ ]. Any successful trajectory has reward at least 1, while any failed trajectory has reward at most _λ_ , so every success continues to outrank every failure. The quality term only distinguishes trajectories within the same outcome class and is applied to mixed- and same-outcome groups alike. 

**Leave-one-out advantage.** We use the leave-one-out estimator, which compares each trajectory with the mean reward of the remaining group members: 


Unlike standard group-normalized GRPO, RLOO does not divide by the within-group reward standard deviation. In a same-outcome group, every trajectory shares the same binary outcome _b_ , so _Ri_ = _b_ + _λqi_ . The constant outcome term cancels: 


Thus, whenever quality varies within a same-outcome group, the group receives nonzero advantages and contributes learning signal where a binary reward would give none. This behavior requires no special handling in the implementation; the same estimator in Equation (22) is applied to every group. Standard group normalization would retain the ordering induced by quality, but it would largely cancel the scale of _λ_ because the reward standard deviation in a same-outcome group is also proportional to _λ_ . RLOO instead preserves the intended magnitude of the quality term, which is why we use it throughout Prism-GRPO. We empirically ablate this design choice in Section G.6, where we compare RLOO with the standard group-normalized GRPO estimator. 

## **E Baseline Implementation** 

All baselines use the setup of Appendix C and differ from Prism-GRPO only in the reward and the advantage estimator. 

**Binary GRPO.** The reward is the binary success flag, _R_ = success. Advantages are the standard group-standardized GRPO values _Ai_ = ( _Ri − µ_ ) _/_ ( _σ_ + _ε_ ), where _µ_ and _σ_ are the mean and standard deviation over the _G_ group members. Zero-variance groups carry no advantage and are removed by the dynamic-sampling filter. This reproduces the SimpleVLA-RL configuration. The peak success values reported by SimpleVLA-RL are not directly comparable with the maximum of the mean training curve in our main paper because the two presentations aggregate checkpoints differently. SimpleVLA-RL reports the best-success checkpoint from each of three seeds and then aggregates the resulting scores, whereas our curves show the step-aligned mean over five seeds throughout training. For example, SimpleVLA-RL reports a 64 _._ 1% success rate on _Lift Pot_ . In our five Binary GRPO runs, the best success rates are 60 _._ 6% at step 39, 64 _._ 5% at step 34, 64 _._ 5% at step 49, 63 _._ 7% at step 29, and 64 _._ 8% at step 44. These per-seed maxima average to 63 _._ 6%, closely matching the reported result. However, because the maxima occur at different training steps, they do not appear simultaneously in the step-aligned five-seed mean curve and are therefore smoothed when the learning curves are averaged. 

**Binary RLOO.** The reward is identical to Binary GRPO; the only change is the estimator. Advantages use the leaveone-out baseline (22) with no standard-deviation division. Since Prism-GRPO also uses RLOO, this baseline isolates the contribution of the quality term from that of the estimator. Everything else is inherited unchanged. 

**Random reward.** Each trajectory receives _R_ = success+ _λu_ , where _u ∼_ Uniform(0 _,_ 1) is sampled independently for each rollout. The random term almost always introduces within-group reward variation, so same-outcome groups rarely remain zero-variance and are typically retained by the dynamic-sampling filter. However, because _u_ contains no information about task execution, it provides only noise rather than a meaningful quality signal. Random reward uses the same RLOO advantage estimator as Prism-GRPO, thereby isolating the effect of replacing the trajectory-derived quality signal with uninformative random scores while holding the reward scale, filtering behavior, and advantage estimator fixed. 

**RL-ZVP.** RL-ZVP (Le et al. 2025) was developed for LLM reasoning, where one decision is one output token. We port it to our discrete action head by treating one action-chunk step as one decision: we mean-pool the per-token entropies over the 14 action-token slots of a step to obtain a single entropy _Hi,t_ per decision, computed from the rollout policy and detached before use. A group is judged degenerate on the binary success signal, all-success or all-failure, rather than on reward variance; this is exact for a binary base reward. On a degenerate group the zeroed GRPO advantage is overwritten by 


with _α_ = 0 _._ 1 and max _k_ over the valid decisions of the trajectory. Mixed groups keep their standard GRPO advantage; 


Figure 13: **Dynamic-filtering statistics across four tasks.** Each task panel reports the percentage of zero-variance groups discarded by the trainer (left) and the total number of trajectories generated per optimizer step (right). Prism-GRPO consistently discards fewer groups and consequently remains closer to the minimum cost of 512 rollouts per step. 


Figure 14: **Rollout-generation cost.** Per-step generation time scales nearly linearly with the number of requested rollouts across ten RL runs (1 _,_ 295 measurements). Each color denotes one run. 

RL-ZVP composes only with group-standardized GRPO. So that the override sees degenerate groups, the dynamicsampling filter is disabled for this baseline. 

## **F Compute usage** 

**Hardware and per-run wall time.** Each task is trained on a single node with 8 _×_ NVIDIA H100-80 GB GPUs. A complete RL run takes approximately 12–16 hours, depending on the task horizon and rollout cost. Rollout generation accounts for roughly 8–12 hours and dominates the total wall time, with the remaining time spent on policy updates, dynamic filtering, and periodic validation. 

**Rollout savings translate directly to compute savings.** Figure 14 shows a near-linear relationship between rollout count and generation time, averaging approximately 0 _._ 81 s per rollout. Because rollout generation dominates training time, reducing the rollout budget yields an almost proportional wall-clock saving. For example, a 30% reduction from the 35 _,_ 000 rollouts required by Binary GRPO on _Lift Pot_ avoids 10 _,_ 500 rollouts, saving approximately 2 _._ 4 of the 7 _._ 9 hours spent on rollout generation. 

## **G Detailed Experimental Results** 

### **G.1 Full Statistics** 

Figure 13 examines how often the quality signal recovers same-outcome groups and how this reduction in filtering affects rollout cost across all four tasks. 

**Filter discard rate.** The filter discard rate is the fraction of generated groups whose final rewards are identical across all group members and are therefore removed before the policy update. Under Binary GRPO and Binary RLOO, every allsuccess or all-failure group has zero reward variance and is discarded. Under Prism-GRPO, the quality term introduces reward variation whenever trajectories with the same outcome differ in execution quality, allowing these groups to contribute to learning. The discard rate is not necessarily zero because a same-outcome group can still receive identical quality scores, such as an all-success group in which every trajectory has perfect quality. The reduction in discard rate therefore directly measures how much otherwise unusable same-outcome data is recovered by Prism-GRPO. 

**Rollouts per step.** This metric counts every trajectory generated to construct one optimizer batch, including filtered 


Figure 16: **Full smoothness-quality results.** 

trajectories and surplus trajectories produced during adaptive gap filling. Each update requires 64 retained groups with _G_ = 8, corresponding to 512 retained trajectories. The trainer first generates 512 trajectories and then samples additional scenes to replace discarded groups until the target batch is complete. A higher discard rate therefore requires more refill rollouts and increases the generation cost of each optimizer step. 

**Random and RL-ZVP incur no filtering.** We omit Random and RL-ZVP from Figure 13 because neither method produces discarded groups in our experiments. The filter removes a group only when all trajectories receive the same final score. Random uses _R_ = success + _λu_ , where an independent continuous random quality _u_ is sampled for each rollout, while RL-ZVP assigns trajectory-dependent policyconfidence values. These scores vary within every sampled group, giving both methods a zero discard rate and the minimum rollout cost of 512 trajectories per step. 

**Full quality metrics.** Due to space constraints, Figure 6 in the main paper contains one collision panel and one smoothness panel, each reporting a representative quality metric. Here, we provide the full collision and smoothness results in Figures 15 and 16. For collision quality, Max-Force Quality and Sum-Impulse Quality show similar trends despite measuring the strongest individual contact and the accumulated contact burden, respectively. The smoothness metrics likewise produce consistent trends across flip- and jerk-based measures. This cross-metric consistency indicates that the observed gains are not specific to a single evaluation metric. 

### **G.2 Quality Weight Ablation** 

Figures 19 and 20 report the full learning curves for _λ ∈ {_ 0 _._ 2 _,_ 0 _._ 5 _,_ 0 _._ 9 _,_ 1 _,_ 2 _}_ on _Lift Pot_ and _Move Can Pot_ . Each column corresponds to one value of _λ_ , and the rows report success rate, calibrated success rate, Max-Force Quality, and 

Sum-Impulse Quality. On both tasks, success rate and calibrated success rate follow similar trends, showing that the conclusions are not sensitive to contact-based success calibration. Likewise, Max-Force Quality and Sum-Impulse Quality exhibit consistent patterns despite measuring the strongest collision and cumulative collision burden, respectively. The main paper uses Max-Force Quality as the primary collision-quality metric because it directly corresponds to the default GT-Max Force training signal; the complete results here confirm that the same conclusions hold under the other reported metrics. 

### **G.3 Quality-Term Placement Ablation** 

**The quality term should be applied to all groups.** Figure 17 compares our default reward with variants that apply the quality term only to same-outcome groups or only to all-failure groups. Applying quality to every group nearly doubles the success rate relative to these restricted variants and produces a more stable quality curve. The quality term serves a useful role in every group type: in mixed groups, it distinguishes trajectories within each outcome class while preserving success dominance; in same-outcome groups, it provides the learning signal that the binary reward lacks. Restricting the quality term therefore discards informative execution differences from part of the training data, whereas the default combined reward uses them consistently across all groups. 

### **G.4 Effect of Group Size** 

We ablate the number of rollouts sampled per group using _G ∈{_ 8 _,_ 16 _,_ 32 _}_ , where _G_ = 8 is the default setting in the main experiments. To isolate the effect of group size, we keep the total number of generated rollouts per optimizer update fixed at 512 and adjust the number of groups accordingly. All other settings, including initialization, rollout budget, optimizer configuration, and quality weight, remain unchanged. 


Figure 18: **Effect of group size.** Each optimizer update uses 512 generated rollouts, while the group size varies over _G ∈ {_ 8 _,_ 16 _,_ 32 _}_ . Prism-GRPO provides the largest gain at _G_ = 8, while the gain decreases as the group size increases. 

Figure 18 shows that Prism-GRPO provides the largest improvement at _G_ = 8. The gain becomes smaller at _G_ = 16, and the results are nearly identical at _G_ = 32. This trend is consistent with the design of Prism-GRPO: as _G_ increases, all-success and all-failure groups become less frequent, so the binary baseline discards fewer groups and leaves less wasted rollout data for Prism-GRPO to recover. 

### **G.5 Effect of Quality-Weight Decay** 

A natural question is whether the quality weight _λ_ should decay during training. Early in training, failures dominate and many groups are all-failure, so the quality term is particularly useful for recovering learning signal. Later, as the success rate increases, one might expect that reducing _λ_ would shift the update increasingly toward task success. Figure 21 shows that decay does not improve performance for _λ_ = 0 _._ 2 or 0 _._ 5. For _λ_ = 0 _._ 9, decay reaches the target about 2K rollouts earlier, but the advantage is not clearly observable from the overall learning curves. Because decay provides no substantial or consistent improvement, we use a fixed quality weight throughout the main experiments. 

### **G.6 Effect of the Advantage Estimator** 

As discussed in Section D, RLOO preserves the scale of the quality term in same-outcome groups, whereas standard group normalization largely cancels this scale. We therefore compare the two estimators while keeping the reward and all other training settings unchanged. Figure 22 shows that RLOO produces more stable learning and consistently achieves the expected rollout-saving gains. Standard group-normalized GRPO exhibits less stable optimization and smaller, less consistent rollout savings. We therefore use RLOO throughout the main experiments. 

## **H Empirical Analysis of Success–Quality Alignment** 

### **H.1 Analysis Protocol** 

We empirically examine whether the trajectory-level quality signals used by Prism-GRPO are associated with task success. Correlations computed across all trajectories can be confounded by scene difficulty, since easier scenes may simultaneously produce higher success rates and cleaner execution. We therefore use two complementary diagnostics: a within-scene quality gap that compares success and failure under the same scene configuration, and a cross-scene Spearman correlation between scene success rate and mean quality. 

**Within-scene measure.** For each task, we evaluate its best-success checkpoint on 256 randomized scenes with 56 stochastic rollouts per scene, yielding 14 _,_ 336 trajectories per task. Rollouts from the same scene share an identical simulator initialization, including object poses, clutter, lighting, tabletop properties, and instruction; only policy sampling and simulator stochasticity vary. We apply no dynamic filtering and include every generated trajectory. For each scene containing at least one successful and one failed rollout, we define the within-scene quality gap as 


where the two terms denote the mean normalized quality of successful and failed trajectories, respectively. A positive gap indicates that successful trajectories have higher quality under the same scene configuration. Each mixed-outcome scene receives equal weight, and we report the mean gap with a 95% confidence interval obtained from 10 _,_ 000 scenelevel bootstrap resamples. 

**Cross-scene measure.** As a complementary populationlevel diagnostic, we compute Spearman’s _ρ_ between each 


Figure 19: **Quality-weight ablation on** **_Lift Pot_ .** 

scene’s success rate and mean trajectory quality. Each point in the corresponding scatter plot represents one scene, with the horizontal coordinate given by its success rate over the 56 rollouts and the vertical coordinate given by their mean quality. Spearman correlation measures whether scenes with higher success rates also tend to have higher quality, without assuming a linear relationship. Whereas the within-scene gap compares success and failure under an identical scene configuration, the cross-scene measure evaluates whether quality tracks success across the broader task distribution. We compute both diagnostics for the collision and smoothness signals defined in Appendix B. 

### **H.2 Collision-Based Alignment** 

Figure 23 reports both alignment diagnostics for Max-Force Quality, Contact-Count Quality, and Sum-Impulse Quality. Max-Force Quality is the default signal used in the main experiments, while the other two signals test whether the conclusion depends on a particular definition of unintended contact. For Max-Force Quality, the mean within-scene quality gap is approximately 0 _._ 55 on _Lift Pot_ , 0 _._ 45 on _Move Can Pot_ , 0 _._ 87 on _Handover Block_ , and 0 _._ 85 on _Beat Block Hammer_ , with 89 _._ 5%–100% of mixed-outcome scenes exhibiting a positive gap. The corresponding cross-scene Spearman correlations are also strongly positive, reaching 0 _._ 79, 0 _._ 68, 0 _._ 98, and 0 _._ 80, respectively. Contact-Count and SumImpulse Quality show the same qualitative pattern across all four tasks, despite measuring collision frequency and accumulated contact burden rather than the strongest individual contact. Together, these results show that success is strongly associated with cleaner execution both within identical scenes and across the task distribution, and that this 

relationship is robust to the particular collision statistic extracted from the trajectory. 

### **H.3 Smoothness-Based Alignment** 

Figure 24 reports both alignment diagnostics for **PrismFlips** , **Prism-MeanFlips** , and **Prism-Jerk** , labeled as Flips (Max), Mean Flips, and Max Jerk in the figure. Across all task–signal combinations, 87%–100% of mixed-outcome scenes have a positive within-scene quality gap, and the cross-scene correlations are consistently positive and strong. These results show that the success–smoothness relationship holds across multiple smoothness definitions rather than depending on a single metric. 

One implementation detail is needed for **Prism-Flips** on _Move Can Pot_ and _Beat Block Hammer_ , where successful execution naturally contains several joint-direction reversals during grasp-and-place or lift-and-strike motions. We therefore subtract a reversal floor automatically estimated as the median reversal count among successful trajectories before normalization, allowing Prism-Flips to measure excess oscillation beyond the motion required for task completion. The same data-driven estimation rule is applied without manual tuning, while no floor is needed for _Lift Pot_ or _Handover Block_ . Prism-MeanFlips and Prism-Jerk are computed without this adjustment. Our goal is not to identify the optimal smoothness metric, but to test whether several reasonable trajectory-derived signals are consistently associated with success; developing more specialized measures that better separate necessary motion from undesirable oscillation remains an interesting direction for future work. 


Figure 20: **Quality-weight ablation on** **_Move Can Pot_ .** 


Figure 21: **Quality-weight decay ablation.** Solid lines use a fixed quality weight, dashed lines use decay, and colors indicate different values of _λ_ . 

## **I Real-World Experiments** 

### **I.1 Deployment Setup** 

We evaluate the policies zero-shot on a Piper robot without additional real-world fine-tuning. The task is to move a can next to a pot. Observations are captured by an Orbbec DaBai DC1 camera at 640 _×_ 480 resolution and resized to the 240 _×_ 320 resolution used during training before being passed through the standard policy preprocessing pipeline. 

The policy predicts 25-step action chunks. Each executed action is seven-dimensional, consisting of six arm-joint targets and one gripper target. To prevent abrupt motions on the physical robot, we apply a proportional rate limit to the six arm-joint dimensions in each control tick: 


Here, ∆<sup>model</sup> is the model-requested joint displacement and _η_ limits the largest arm-joint change to 0 _._ 05 rad per control 

tick. When any requested joint displacement exceeds this limit, all six arm-joint dimensions are scaled by the same factor, preserving the relative direction of the commanded motion. The seventh action dimension controls the gripper and is exempt from this rate limit. 

### **I.2 Evaluation Protocol** 

The purpose of this experiment is to examine whether the shove-cheat behavior observed in the simulated _Move Can Pot_ task transfers to the real world. In this shortcut, the policy moves the pot toward the can instead of lifting and placing the can as instructed. To stress-test this behavior, for each method we select the checkpoint with the highest simulated shove-cheat rate among checkpoints with similar simulated success rates of approximately 65%. We conduct 25 trials for each policy. In every trial, the can is initially placed to the left of the pot. We manually reset the can and pot to approximately the same positions before each trial. 


Figure 22: **Effect of the advantage estimator.** RLOO yields more stable learning and more consistent rollout savings than standard group-normalized GRPO. _λ_ = 0 _._ 2 

### **I.3 Real-World Results** 

Table 2 reports clean success and shove-cheat behavior over 25 trials per method. Prism-GRPO achieves 6 _/_ 25 clean successes, compared with 4 _/_ 25 for Binary GRPO and 2 _/_ 25 for RL-ZVP. We do not interpret the difference between PrismGRPO and Binary GRPO as conclusive evidence of improved clean success, since their counts differ by only two trials. The more pronounced result is the occurrence of the shove-cheat behavior observed in simulation. Instead of moving the can beside the pot, the policy attempts to move the pot toward the stationary can. This shortcut occurs in 5 _/_ 25 RL-ZVP trials and 1 _/_ 25 Binary GRPO trials, but is not observed in any of the 25 Prism-GRPO trials. Thus, while the cleansuccess comparison should be interpreted cautiously, the shortcut pattern qualitatively supports the simulation finding that Prism-GRPO discourages undesirable task-completion strategies. 


Figure 23: **Collision-based success–quality alignment.** Each task is evaluated using Max-Force, Contact-Count, and SumImpulse Quality. Within-scene plots compare the mean quality of successful and failed trajectories generated from the same mixed-outcome scene; positive gaps indicate that successful trajectories are cleaner. Cross-scene plots report the Spearman correlation between scene success rate and mean quality. 


Figure 24: **Smoothness-based success–quality alignment.** Each task is evaluated using maximum joint reversals, mean joint reversals, and action jerk. The within-scene and cross-scene diagnostics follow the same definitions as Figure 23. 

