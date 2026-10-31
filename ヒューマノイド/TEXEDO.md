---
title: "TEXEDO : Test Time Scaling for Controller-aware Language-conditioned Humanoid Motion Generation"
date: "2026-06-22"
authors: "Jianuo Cao; Yuxin Chen; Yuzhen Song; Masayoshi Tomizuka; Chenran Li; Thomas Tian"
url: https://arxiv.org/abs/2606.22998
pdf: https://arxiv.org/pdf/2606.22998
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.22998)** / [論文ページ](https://arxiv.org/abs/2606.22998)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# TEXEDO : Test Time Scaling for Controller-aware Language-conditioned Humanoid Motion Generation 

Jianuo Cao<sup>_∗_1</sup><sup>_,_2</sup> , Yuxin Chen<sup>_∗_2</sup> , Yuzhen Song<sup>2</sup><sup>_,_3</sup> , Masayoshi Tomizuka<sup>2</sup> , Chenran Li<sup>2</sup> , Thomas Tian<sup>2</sup> 1 _Nanjing University_ 2 _University of California, Berkeley_ 3 _Southern University of Science and Technology_ 


Fig. 1: **TEXEDO overview.** Given a language prompt, the TEXT stage samples multiple whole-body motions from a textconditioned motion generator. The SEE stage evaluates each candidate with two grounded verifiers: a dynamic score that predicts controller executability and a semantic score that measures text-motion alignment. The DO stage selects a deployable motion by first filtering out dynamically infeasible candidates and then choosing the most semantically aligned one. 

**_Abstract_ —Text-conditioned motion generation has become a promising interface for programming humanoid robots, but current generators are often trained on human motion datasets retargeted to robot morphology. While such data provides rich semantic kinematic priors, it does not capture the nuances of the whole-body tracking controller, including balance, contact, actuation limits, and controller-specific failure modes. Therefore, generated motions can be semantically plausible yet difficult or impossible for the robot to execute. We propose TEXEDO, a testtime scaling framework for humanoid motion generation that improves motion quality without requiring a stronger underlying generator. Given a text prompt, our method samples multiple motions from the pre-trained text-conditioned generator and selects the best executable and task-aligned motion. The reward model combines a dynamic feasibility verifier, distilled from whole-body tracking rollouts to predict physical executability, with a semantic alignment verifier that measures text-motion alignment in a learned co-embedding space. Our pipeline treats dynamic feasibility as a hard constraint and semantic alignment as the selection objective within the feasible set. Across large-scale simulation studies and real-world deployment on a Unitree G1, we show that our test-time scaling strategy consistently improves both tracking fidelity and text alignment, demonstrating that grounded verification is an effective path toward deployable language-guided humanoid motion generation. Please checkout our website for robot videos, code and data: Project Website.** 

## I. INTRODUCTION 

Recent progress on language-controlled humanoids has been a story of scaling at the two ends of a single deployment pipeline. On the _motion generation_ side, text-conditioned motion generation models have grown from small task-specific networks into large models that produce whole-body motions directly from a language prompt [8, 24, 21, 6, 25, 18]. On the _whole-body control_ side, learning-based whole-body tracking controllers have evolved from task-specific controllers into multi-task controllers that can, in principle, execute essentially any kinematic reference on real hardware [17, 12, 10, 13]. 

Despite this progress, these two scaling trends remain only weakly coupled. Most motion-generation models learn from human motion corpora, often after re-targeting the kinematics to a robot skeleton [14, 5], but their training objective does not expose them to the downstream controller that must realize the motion. As a result, a generated motion may be semantically faithful yet still fall outside the feasible set of the humanoid tracker due to balance constraints, contact timing, actuation limits, or controller-specific failure modes. In such cases, the burden is shifted to the controller: it must attempt to realize a reference motion that was never generated with its capabilities 

in mind. This leads to brittle and poorly specified behavior at deployment, where the executed motion may deviate from the intended semantics, lose balance, produce improper contacts, or saturate actuators. 

In language modeling, an increasingly successful way to improve generation at test time is to sample multiple candidates and use a verifier to select the best one [11, 19, 16, 7]. Recent work on vision-language-action policies suggests that a similar principle can improve robotic decision-making during deployment [9, 23]. However, importing this recipe to humanoid motion generation requires a more grounded notion of what “best” means. A good candidate motion must not only match the language prompt; it must also be executable by the particular whole-body controller on the particular humanoid platform. Thus, the verifier cannot merely judge abstract motion quality or text-motion similarity. It must be _controlleraware_ : evaluate whether a candidate trajectory lies within the balance, contact, and actuation budgets of the tracker that will actually execute it. 

We propose **TEXEDO** ( **Text-See-Do** ), a test-time scaling pipeline that turns a frozen text-to-motion generator into a controller-aware motion generator (Figure 1). Given a language prompt, TEXEDO first samples multiple candidate whole-body trajectories (TEXT). It then evaluates each candidate along two complementary axes (SEE): whether the motion is likely to be executable by the deployment-time tracker, and whether it remains semantically aligned with the language prompt. The first score is distilled from rollouts of the tracker itself, making it grounded in the balance, contact, and actuation limits of the target humanoid. The second score is learned from a contrastive text–motion embedding, allowing the selector to preserve the intended semantics of the prompt. Because dynamic feasibility and semantic alignment are not interchangeable, TEXEDO composes them asymmetrically (DO): it first removes motions that are unlikely to be trackable, and then selects the most semantically aligned candidate from the feasible set. In this way, TEXEDO converts additional inference-time samples into a single reference trajectory that is both language-aligned and grounded in the capabilities of the downstream controller, without modifying either the generator or the tracker. 

The contributions of this work are threefold. First, we formulate controller-aware, language-conditioned whole-body humanoid motion generation as a test-time scaling problem, where additional inference-time samples are used to improve the single reference motion ultimately commanded to the robot. Second, we introduce two complementary grounded verifiers for controller-aware selection: a Dynamic Feasibility Verifier, distilled from rollouts of the deployment-time tracker to predict whether a reference motion can be realized on the target humanoid, and a Semantic Alignment Verifier, trained directly on robot-skeleton motions to measure text–motion alignment. Third, we show that semantic alignment and dynamic feasibility define competing selection criteria, and propose an asymmetric filter-then-rerank strategy that treats feasibility as a constraint before selecting the most semantically 

aligned motion. Empirically, TEXEDO improves both motion execution quality and task alignment, transfers zero-shot to unseen motion generators, generalizes to out-of-distribution prompts, and yields consistent gains over vanilla sampling without selection in real-world experiments on a physical Unitree G1 humanoid. 

## II. PROBLEM FORMULATION 

We formulate controller-aware whole-body motion generation as a _test-time scaling_ problem: instead of committing to the first motion sampled from a generator, we spend inferencetime compute to sample multiple candidate motions and select the one most suitable for execution. Formally, let _ℓ_ denote a natural-language instruction and let **m** _∈_ R<sup>_T ×D_</sup> denote a whole-body reference motion, where _T_ is the sequence length and _D_ is the dimension of the target humanoid’s root pose and joint configuration. A text-to-motion generator _G_ induces a distribution _G_ ( _· | ℓ_ ) over such motions. At deployment, rather than executing a single sample from this distribution, we draw a candidate set and use a selector to choose a motion that is both dynamically feasible for the downstream tracker and semantically aligned with the instruction. 

## III. METHOD 

Given a language instruction _ℓ_ , TEXEDO follows a TEXT– SEE–DO runtime selection pipeline. Section III-A (TEXT): A language-conditioned generator samples _N_ candidate motions _{_ **m** _i}_<sup>_N_</sup> _i_ =1<sup>from</sup><sup>_ℓ_;SectionIII-B(SEE):groundedverifiers</sup> score their dynamic feasibility and semantic alignment; and Section III-C (DO): a filter-then-rerank rule selects one deployable motion. Both the generator and deployment-time tracker remain frozen. 

## _A. Language-Conditioned Motion Generator_ (TEXT) 

The TEXT stage provides the candidate motions that the subsequent SEE and DO stages operate on. Given a language instruction _ℓ_ , we assume access to a language-conditioned motion generator _G_ that can sample a set of candidate reference trajectories _MN_ ( _ℓ_ ) = _{_ **m** _i}_<sup>_N_</sup> _i_ =1<sup>_,_</sup><sup>**m**</sup><sup>_i∼G_(</sup><sup>_· | ℓ_)</sup><sup>_._Inour</sup> framework, _G_ is treated as a black box: the verifiers consume only the decoded reference trajectories _{_ **m** _i}_ and do not rely on the generator architecture. 

For the main experiments, we instantiate _G_ with FSQ-GPT, a discrete autoregressive text-to-motion generator for wholebody humanoid trajectories. FSQ-GPT first compresses continuous robot motions into discrete motion tokens using an FSQ tokenizer [15], and then fine-tunes a Flan-T5-base model [4] to generate these tokens autoregressively from language instructions. At inference time, sampled token sequences are decoded back into continuous whole-body reference trajectories, forming the candidate set _MN_ ( _ℓ_ ). We sample with temperature and top- _k_ truncation to control candidate diversity. Full training and sample details for FSQ-GPT are provided in Appendix B. 


Fig. 2: **Dual verifier design.** _R_ dyn estimates dynamic feasibility from the motion alone and _R_ text measures text-motion alignment in a learned embedding space. 

## _B. Dynamic Feasibility And Semantic Alignment Evaluation_ 

(SEE) 

What turns a pool of candidate motions into a single deployable trajectory is, ultimately, a definition of _motion quality_ . The SEE stage answers this question with two scalars assigned to every candidate: a dynamic score _R_ dyn( **m** ) _∈_ [0 _,_ 1] measuring whether the motion is dynamically feasible on the deployment-time tracker, and a semantic score _R_ text( _ℓ,_ **m** ) _∈_ [0 _,_ 1] measuring whether it depicts what the prompt describes. The design of both verifiers is illustrated in Figure 2. 

**Dynamic feasibility verifier.** A kinematically plausible motion may still fail under the deployment-time tracker because of balance, contact, or actuation constraints. However, evaluating each candidate by an actual roll-out at selection time is prohibitive. Thus, we proceed in two steps: 

_Oracle quality of roll-outs._ For each candidate **m** , an offline tracker roll-out produces three complementary signals: a binary success indicator _ys ∈{_ 0 _,_ 1 _}_ , a normalized tracking quality score _qd ∈_ [0 _,_ 1], and a progress ratio _qg ∈_ [0 _,_ 1] measuring the percentage of reference completed before early termination. We adopt the early-termination criterion of BeyondMimic [10] as the common failure definition for both _ys_ and _qg_ , and details are reported to Appendix C. 

To jointly capture these signals, we collapse the three signals into a single oracle quality: 


Here, _α_ controls how much motion-tracking quality modulates the reward for a _successful_ roll-out, while _β_ sets the partial-credit weight assigned to _failed_ roll-outs based on their progress and tracking quality. In particular, we set _β <_ 1 _/_ (1+ _α_ ), so that _Q_<sup>_∗_</sup> assigns successful roll-outs a higher score than any failed roll-outs, while retaining the graded information within the all success or all failure group. 

_Motion-only surrogate._ After obtaining the oracle quality labels, we train a lightweight temporal Transformer to predict (ˆ _ps,_ ˆ _qd,_ ˆ _qg_ ) from **m** , and feed the predictions back through Eq. (1): 


the surrogate and its supervision signal share exactly one algebraic form. The three heads are trained jointly under a weighted sum of a positive-balanced binary cross-entropy on _p_ ˆ _s_ , an MSE on _q_ ˆ _d_ , and an MSE on _q_ ˆ _g_ masked to failed rollouts. Full architecture and training details are in Appendix C. 

**Semantic alignment verifier.** While dynamic realizability is essential, a motion is only successful if it also realizes the semantic intent of the text instruction. Following the T2M [5], we train bidirectional GRU text and motion encoders, _φ_ text and _φ_ motion, _directly_ on the target robot skeleton, so that the embedding space is consistent with the candidates produced by the TEXT stage. With _dij_ = _∥φ_ text( _ℓi_ ) _− φ_ motion( **m** _j_ ) _∥_ 2, we optimize an all-pairs margin contrastive objective: 


where [ _x_ ]+ =max(0 _, x_ ) and _B_ is batch size. The all-pairs term exposes the encoders to _O_ ( _B_<sup>2</sup> ) informative negatives per step rather than the single random negative used in the original T2M formulation. At test time, the semantic score is defined as the exponentiated negative embedding distance: 


so a higher _R_ text indicates better text–motion alignment. 

_C. Test-Time Selection_ (DO) 

This stage converts the verifier scores into a single deployable reference motion. Given a prompt _ℓ_ and candidate motions _{_ **m** _i}_<sup>_N_</sup> _i_ =1<sup>,wefirstfiltercandidatespredictedtobe</sup> dynamically infeasible and then select the most semantically aligned survivor: 


The rule here is deliberate and reflects a deployment-safety priority: on physical hardware, a semantically perfect but dynamically infeasible motion can cause falls or actuator saturation, whereas a feasible but slightly less-aligned motion merely underperforms. We therefore treat dynamic feasibility as a hard constraint to be satisfied first, and semantic alignment as the objective to optimize only within the executable pool. We set _θ_ = 0 _._ 8 from validation roll-outs and the empty-set fallback _S_<sup>ˆ</sup> = ∅ is triggered on only 1 _._ 18% of test prompts. 


Fig. 3: **Best-of-** _N_ **curves for dynamic feasibility on FSQ-GPT.** Subplots report Succ, _E_ mpjpe-l, _E_ acc, _E_ vel, and _Q_<sup>_∗_</sup> as _N_ increases from 1 to 32. Across metrics, _R_ dyn **-only** consistently outperforms **Random** and closely approaches **Oracle** . 

## IV. EXPERIMENTS 

We evaluate TEXEDO as a deployable test-time scaling system for language-conditioned humanoid motion generation along three axes: test-time selection performance, zero-shot generalization, and real-world transfer. **Q1.** Do the grounded verifiers and their composition select motions that are both executable by the whole-body controller and aligned with the language instruction (Section IV-B)? **Q2.** Can the verifiers transfer plug-and-play to an unseen generator and out-ofdistribution prompts without retraining? (Section IV-C)? **Q3.** Do the simulation gains carry over to real-world execution on a Unitree G1 humanoid (Section IV-D)? 

## _A. Experimental Setup_ 

**Robot set up and model training.** We use a Unitree G1 humanoid as our robot platform with SONIC [13] as the frozen whole-body controller. We train our text-to-motion generator using AMASS [14] and CLAW [2]. More implementation details can be found in Appendix B. 

**Baselines.** We compare **TEXEDO** against four selection strategies: (i) **Base** ( _N_ =1), a single sample from the generator (no-test-time-scaling); (ii) _R_ dyn **-only** , arg max _i R_ dyn( **m** _i_ ), a purely physical selector; (iii) _R_ text **only** , arg max _i R_ text( _ℓ,_ **m** _i_ ), a purely semantic selector; and (iv) **Oracle** , a privileged selector that rolls out _every_ candidate in _MN_ ( _ℓ_ ) through SONIC and picks the one that actually scores best on each metric. Note that **Oracle** requires _N_ SONIC rollouts per prompt (three orders of magnitude more expensive than scoring with the verifiers) and is therefore impractical at deployment time; we report it only as an upper bound on any selector over the same pool. 

**Evaluation metrics.** We evaluate selected motions along two complementary dimensions. _Dynamic fidelity_ measures whether a reference motion can be faithfully executed by the downstream tracker. We report tracking success rate (Succ), root-relative mean per-joint position error ( _E_ mpjpe, mm), joint acceleration error ( _E_ acc, mm/frame<sup>2</sup> ), joint velocity error ( _E_ vel, mm/frame), and the composite oracle quality _Q_<sup>_∗_</sup> defined in Equation (1). _Semantic alignment_ measures whether the selected motion matches the language instruction, using VLM- 

as-Judge as our primary evaluation. Full details of metric definitions and the VLM-based evaluation method are provided in the Appendix E. 

**Inference-time budget.** All timings are measured on a single NVIDIA A100-SXM4 40GB GPU. Because the _N_ candidates for a prompt are sampled and scored as a single batch, the cost of test-time scaling grows sublinearly in _N_ . Sampling 32 candidates from FSQ-GPT takes 2 _._ 62 s on average, and scoring 32 candidates adds only 15 _._ 12 ms (Dynamic Feasibility Verifier) and 11 _._ 93 ms (Semantic Alignment Verifier) on average, so a full _N_ =32 sample and selection completes in roughly 3 _._ 5 s end-to-end. 


Fig. 4: **Semantic alignment verifier turns larger candidate pools into better prompt alignment.** For each prompt, _R_ text **only** selects the candidate with the highest _R_ text score; the selected motions improve consistently with increasing _N_ when evaluated by an independent VLM Judge. 

## _B. Effectiveness Of_ **TEXEDO** _For Test-Time Scaling_ 

**Effectiveness of individual verifiers.** We first isolate the effect of each verifier under the same best-of- _N_ setting. For each prompt, we sample a candidate pool of _N_ different samples and select one motion using either the Dynamic Feasibility Verifier or the Semantic Alignment Verifier alone. 

Figure 3 reports the dynamic feasibility metrics of the selected motions as the candidate budget _N_ increases, comparing _R_ dyn **-only** against **Random** and **Oracle** . As _N_ increases, 

TABLE 1: **TEXEDO balances the complementary strengths of** _R_ dyn **and** _R_ text **.** Pushing either verifier to its extreme costs the other, and **TEXEDO** achieves strong performance on both axes simultaneously. 

|**Strategy**<br>**S**|**emantic alignmen**|**t**|**Motion e**|**xecution **|**quality**||
|---|---|---|---|---|---|---|
||VLM-Judge_↑_|Succ_↑_|_E_mpjpe _↓_|_E_acc _↓_|_E_vel _↓_|_Q_<sup>_∗_</sup>_↑_|
|**Base** (_N_=1)|5.722|0_._873|44_._34|6_._09|11_._82|0_._829|
|_R_dyn**-only** (_N_=32)|4.924|**0.990**|**38.15**|**3.30**|**5.91**|**0.945**|
|_R_text**-only** (_N_=32)|**6.110**|0_._885|42_._97|4_._90|10_._03|0_._847|
|**TEXEDO** (_N_=32)|6_._054|0_._984|39_._09|4_._26|7_._78|0_._926|


TABLE 2: **Zero-shot transfer to Kimodo. TEXEDO** , trained only on FSQ-GPT rollouts, improves both VLM-Judge and physical execution metrics when applied zero-shot to the unseen Kimodo motion generator. 

|**Method**|**Semantic alignment**||**Motion e**|**xecution **|**quality**||
|---|---|---|---|---|---|---|
||VLM-Judge_↑_|Succ_↑_|_E_mpjpe _↓_|_E_acc _↓_|_E_vel _↓_|_Q_<sup>_∗_</sup>_↑_|
|Kimodo (**Base**, _N_=1)|4.823|0_._937|38_._62|1_._84|5_._33|0_._918|
|Kimodo+_R_dyn**-only** (_N_=32)|5.020|**0.955**|**35.47**|**1.42**|**4.28**|**0.937**|
|Kimodo+_R_text**-only**(_N_=32)|**5.717**|0_._942|38_._02|1_._87|5_._43|0_._919|
|Kimodo+**TEXEDO** (_N_=32)|5.381|0_._954|37_._49|1_._70|4_._97|0_._935|


_R_ dyn **-only** consistently outperforms **Random** and approaches **Oracle** across physical metrics, showing that the learned verifier recovers much of the improvement available from oraclebased selection. This is important because **Oracle** requires rolling out every candidate with high-fidelity simulation, making it impractical as an online selection rule. 

A similar trend holds for semantic alignment. When selecting candidates by _R_ text, the VLM-as-Judge score (independent third-party judge) increases monotonically with the candidate budget, from 5 _._ 722 at _N_ =1 to 6 _._ 110 at _N_ =32 (Figure 4). 

Together, these results show that the two verifiers convert additional test-time compute budgets into improvements along their intended axes: _R_ dyn improves executability, while _R_ text improves semantic alignment. 

**Effectiveness of TEXEDO** . We next evaluate the full selector, which composes the two verifiers through an asymmetric filter-then-rerank rule. Given a candidate pool, we first filter out motions predicted to be dynamically infeasible, and then selects the most semantically aligned motion among the remaining candidates. 

Table 1 compares **TEXEDO** against **Base** and two singleverifier selectors ( _R_ dyn **-only** and _R_ text **-only** ) at _N_ =32. Optimizing feasibility alone is not neutral to semantics but detrimental: _R_ dyn **-only** drives the VLM-Judge score down to 4 _._ 924, _below_ the no-selection **Base** (5 _._ 722), as the most trackable candidates tend to be conservative motions that drift from the prompt’s intent. Symmetrically, _R_ text **-only** reaches 6 _._ 110 in alignment but yields little improvement in execution (Succ 0 _._ 885 vs. **Base** ’s 0 _._ 873, far below _R_ dyn **-only** ’s 0 _._ 990). Since pushing either verifier to its extreme costs the other, TEXEDO resolves the tension by composition rather than compromise: it recovers execution close to _R_ dyn **-only** (Succ 0 _._ 984 vs. 0 _._ 990) while largely preserving the semantic alignment of _R_ text **-only** 

## (6 _._ 054 vs. 6 _._ 110). 

**Qualitative comparison.** Figure 5 shows four representative case studies, illustrating different failure modes of the baselines and a successful case of **TEXEDO** . 

## _C. Out-Of-Distribution Generalization_ 

**Zero-shot transfer to an unseen motion generator.** A key advantage of **TEXEDO** is that its verifiers operate on decoded robot motions rather than generator-specific internals. The Dynamic Feasibility Verifier consumes only the candidate reference motion, and the Semantic Alignment Verifier consumes only the motion and the language instruction. As a result, the selection rule is not tied to the architecture, tokenization scheme, or latent space of the generator used to produce the candidates. 

To test this generator-agnostic property, we apply the same verifiers trained on FSQ-GPT rollouts directly to Kimodo [18], an independently trained motion generator zeroshot. As shown in Table 2, **TEXEDO** improves both execution quality and semantic alignment on this unseen generator, demonstrating that the learned criteria transfer beyond the generator distribution used to train the verifiers. 

**Out-of-distribution (OOD) generalization.** We further test whether **TEXEDO** remains effective on language instructions outside the training distribution. The base generator is trained on the combined AMASS [14] and CLAW [2] datasets, whereas the OOD evaluation uses 50 prompts sampled from BONES-SEED [1]. This setting tests whether the verifierbased selection rule can improve generation when the prompt composition differs from the data used to train the generator and verifiers. As shown in Table 3, **TEXEDO** improves over the base generator on both ID and OOD prompts along both axes. On the OOD split, it raises tracking success from 0 _._ 860 


Fig. 5: **Qualitative comparison.** Representative case studies in MuJoCo simulation. **Top-left:** a success case of **TEXEDO** , where the generated motion is dynamically feasible and semantically aligned. **Top-right:** a failure case of _R_ dyn **-only** produces a stable but semantically generic motion. **Bottom-left:** a failure case of _R_ text **-only** selects a semantically aligned but untrackable motion. **Bottom-right:** a failure case of **Base** fails with a dynamically infeasible and semantically inconsistent motion. 

TABLE 3: **Out-of-distribution generalization.** Evaluated on prompts from unseen dataset BONES-SEED [1], **TEXEDO** achieves a strong balance between dynamics fidelity and semantic alignment. 

|**Setting**|**Method**|**Semantic alignment**||**Motion ex**|**ecution **|**quality**||
|---|---|---|---|---|---|---|---|
|||VLM-Judge_↑_|Succ_↑_|_E_mpjpe _↓_|_E_acc _↓_|_E_vel _↓_|_Q_<sup>_∗_</sup>_↑_|
|ID|**Base**(_N_=1)|5.722|0.873|44.34|6.09|11.82|0.829|
||**TEXEDO** (_N_=32)|**6.054**|**0.984**|**39.09**|**4.26**|**7.78**|**0.926**|
|OOD|**Base**(_N_=1)|4.116|0.860|36.22|8.36|15.71|0.804|
||**TEXEDO** (_N_=32)|**4.401**|**0.980**|**26.64**|**3.65**|**3.88**|**0.942**|


to 0 _._ 980 and oracle quality _Q_<sup>_∗_</sup> from 0 _._ 804 to 0 _._ 943 and substantially reducing tracking errors. These results indicate that the feasibility verifier generalizes well beyond the training distribution. In contrast, the semantic gain is smaller than on ID prompts, likely because the learned semantic embedding transfers less readily to unseen prompts. 

## _D. Real-Robot Deployment_ 

We deploy **TEXEDO** on a physical Unitree G1 humanoid across 30 text prompts spanning locomotion, upper-body gestures, and their combinations. Using N=32 candidates per prompt, **TEXEDO** successfully executes all 30 prompts on hardware. Figure 6 shows representative qualitative results: **TEXEDO** consistently selects motions that execute stably and match the intended behavior. Full deployment details including 

hardware setup, prompt construction, and per-prompt tracking results are provided in Appendix D-0b. 

## V. CONCLUSION 

In this work, we presented TEXEDO, a test-time scaling framework that turns a frozen language-conditioned motion generator into a controller-aware humanoid motion system. By sampling multiple candidate motions and selecting among them with two complementary verifiers for dynamic feasibility and semantic alignment, TEXEDO improves the single reference ultimately commanded to the whole-body tracker without retraining either component. 

Our evaluation shows that the verifiers are effective along their intended axes: the Dynamic Feasibility Verifier selects motions that are more executable by the downstream tracker, while the Semantic Alignment Verifier selects motions that 


Fig. 6: **Real-robot execution results on the Unitree G1.** Across diverse prompt types spanning locomotion, upper-body gestures, and their combinations, TEXEDO consistently selects motions that execute stably and faithfully realize the intended semantics on physical hardware. 

better preserve the language instruction. The proposed filterthen-rerank rule combines these complementary signals to select motions that improve both execution quality and semantic alignment. The same verifiers transfer plug-and-play to an unseen generator and out-of-distribution prompts without retraining, and the resulting gains carry over to real-world execution on a Unitree G1 humanoid. These findings demonstrate the effectiveness of the proposed method for improving deployable language-guided humanoid motion generation. 

## VI. LIMITATIONS 

**Candidate-set and latency trade-off.** As a test-time selection framework, TEXEDO is bounded by the quality and diversity of the sampled candidate motions. If the generator rarely produces motions that are both semantically aligned and dynamically feasible, or if the tracker is too weak to realize any motions, selection alone cannot recover a successful motion. Increasing the number of samples _N_ can improve the chance of finding a valid candidate, but this introduces an inferencetime trade-off between selection quality and latency; future work could address this with adaptive sampling mechanisms that allocate additional samples only when needed. 

**Verifier data and tracker adaptation.** The grounded verifiers need diverse reference motions and tracker roll-outs to learn reliable semantic and dynamic scores. Moreover, because dynamic feasibility is tracker-specific, changing the tracker requires rerunning roll-outs to update oracle feasibility labels and adapt the Dynamic Verifier. However, the cost of this 

adaptation process can be effectively mitigated through a data reuse mechanism: the reference-motion corpus is not tied to a particular generator, and even under tracker changes the same references can be reused for relabeling, which is substantially less costly than collecting a new motion corpus or retraining the motion generator. Future work could further reduce this cost by investigating more efficient fine-tuning procedures for verifier adaptation. 

## REFERENCES 

- [1] Bones Studio. BONES-SEED: Skeletal everyday embodiment dataset, 2026. URL https://huggingface.co/ datasets/bones-studio/seed. 

- [2] Jianuo Cao, Yuxin Chen, and Masayoshi Tomizuka. Claw: Composable language-annotated whole-body motion generation. _arXiv preprint arXiv:2604.11251_ , 2026. 

- [3] Yuxin Chen, Jianglan Wei, Chenfeng Xu, Boyi Li, Masayoshi Tomizuka, Andrea Bajcsy, and Ran Tian. Reimagination with test-time observation interventions: Distractor-robust world model predictions for visual model predictive control. _arXiv preprint arXiv:2506.16565_ , 2025. 

- [4] Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus, Yunxuan Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, et al. Scaling instruction-finetuned language models. _Journal of Machine Learning Research_ , 25(70):1–53, 2024. 

- [5] Chuan Guo, Shihao Zou, Xinxin Zuo, Sen Wang, Wei Ji, Xingyu Li, and Li Cheng. Generating diverse and natural 3d human motions from text. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 5152–5161, 2022. 

- [6] Chuan Guo, Yuxuan Mu, Muhammad Gohar Javed, Sen Wang, and Li Cheng. Momask: Generative masked modeling of 3d human motions. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1900–1910, 2024. 

- [7] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 

- [8] Biao Jiang, Xin Chen, Wen Liu, Jingyi Yu, Gang Yu, and Tao Chen. Motiongpt: Human motion as a foreign language. _Advances in Neural Information Processing Systems_ , 36:20067–20079, 2023. 

- [9] Jacky Kwok, Christopher Agia, Rohan Sinha, Matt Foutter, Shulu Li, Ion Stoica, Azalia Mirhoseini, and Marco Pavone. Robomonkey: Scaling test-time sampling and verification for vision-language-action models. _arXiv preprint arXiv:2506.17811_ , 2025. 

- [10] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [11] Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In _International Conference on Learning Representations_ , volume 2024, pages 39578–39601, 2024. 

- [12] Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 

- [13] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castaneda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [14] Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard Pons-Moll, and Michael J Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

_OpenAI Blog_ , 2024. https://openai.com/index/ learning-to-reason-with-llms/. 

   - [17] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

   - [18] Davis Rempe, Mathis Petrovich, Ye Yuan, Haotian Zhang, Xue Bin Peng, Yifeng Jiang, Tingwu Wang, Umar Iqbal, David Minor, Michael de Ruyter, et al. Kimodo: Scaling controllable human motion generation. _arXiv preprint arXiv:2603.15546_ , 2026. 

   - [19] Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling llm test-time compute optimally can be more effective than scaling model parameters. _arXiv preprint arXiv:2408.03314_ , 2024. 

   - [20] Zelin Tao, Zeran Su, Peiran Liu, Jingkai Sun, Wenqiang Que, Jiahao Ma, Jialin Yu, Jiahang Cao, Pihai Sun, Hao Liang, et al. Heracles: Bridging precise tracking and generative synthesis for general humanoid control. _arXiv preprint arXiv:2603.27756_ , 2026. 

   - [21] Guy Tevet, Sigal Raab, Brian Gordon, Yonatan Shafir, Daniel Cohen-Or, and Amit H Bermano. Human motion diffusion model. _arXiv preprint arXiv:2209.14916_ , 2022. 

   - [22] Wanjiang Weng, Xiaofeng Tan, Junbo Wang, Guo-Sen Xie, Pan Zhou, and Hongsong Wang. Realign: text-tomotion generation via step-aware reward-guided alignment. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, pages 10621–10629, 2026. 

   - [23] Yilin Wu, Ran Tian, Gokul Swamy, and Andrea Bajcsy. From foresight to forethought: Vlm-in-the-loop policy steering via latent alignment. _arXiv preprint arXiv:2502.01828_ , 2025. 

   - [24] Jianrong Zhang, Yangsong Zhang, Xiaodong Cun, Yong Zhang, Hongwei Zhao, Hongtao Lu, Xi Shen, and Ying Shan. Generating human motion from textual descriptions with discrete representations. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 14730–14740, 2023. 

   - [25] Mingyuan Zhang, Zhongang Cai, Liang Pan, Fangzhou Hong, Xinying Guo, Lei Yang, and Ziwei Liu. Motiondiffuse: Text-driven human motion generation with diffusion model. _IEEE transactions on pattern analysis and machine intelligence_ , 46(6):4115–4128, 2024. 

   - [26] Zewei Zhang, Kehan Wen, Michael Xu, Junzhe He, Chenhao Li, Takahiro Miki, Clemens Schwarke, Chong Zhang, Xue Bin Peng, and Marco Hutter. Learning whole-body humanoid locomotion via motion generation and motion tracking. _arXiv preprint arXiv:2604.17335_ , 2026. 

- [15] Fabian Mentzer, David Minnen, Eirikur Agustsson, and Michael Tschannen. Finite scalar quantization: Vq-vae made simple. In _International Conference on Learning Representations_ , volume 2024, pages 51772–51783, 2024. 

- [16] OpenAI. Learning to reason with LLMs. 

## APPENDIX A RELATED WORK 

**Language-conditioned motion generation.** A prominent line of work represents continuous motion as discrete token sequences. MotionGPT [8] and T2M-GPT [24] first learn a VQVAE-style motion tokenizer and then train an autoregressive language-model backbone to generate motion tokens from text. MoMask [6] follows the same discrete-token perspective, but uses an RVQ-VAE to construct hierarchical residual motion tokens and generates them through iterative masked prediction rather than left-to-right autoregressive decoding. In parallel, diffusion-based methods such as MDM [21] and MotionDiffuse [25] formulate text-to-motion generation as an iterative denoising process, providing an alternative paradigm with strong motion diversity, controllability, and flexible conditioning. More recently, Kimodo [18] scales kinematic motion diffusion with a large motion-text dataset and supports text prompting together with rich kinematic constraints such as keyframes, waypoints, joint constraints, and foot contacts. While these works primarily focus on improving the quality and diversity of generated motions, our work addresses the deployment-time trade-off between semantic alignment and downstream tracker compatibility as a plug-in selection module for existing text-conditioned motion generators. 

**Aligning motion generation with tracking.** To improve the executability of generated motions, many prior works align motion generation and tracking during training by using the same motion corpus for both the generator and the tracker. This encourages distributional alignment between generated references and the tracker’s training data [13, 20]. Some methods further fine-tune the tracker with RL under randomized commands, terrains, or environment configurations while keeping the generator fixed [26]. Such training-time alignment can improve executability, but it couples executability to how the generator and tracker are trained together. In contrast, our work keeps the generator and tracker fixed and introduces controller awareness through a lightweight runtime verifier, which can be adapted without retraining the motion generator. **Test-time scaling of robot motion generation models.** Largescale pretraining has been the dominant route to capable generative models, but it is computationally expensive and ties each model’s behavior to its training distribution. Recently, test-time scaling, generating multiple candidates and using a verifier to select among them, has emerged as a powerful complement in large language models [11, 19, 16, 7]. Its appeal is that it leverages the diversity already latent in a frozen model to adapt to deployment-time signals (e.g., human preference, task constraints, downstream executability) without retraining the model itself. The same paradigm has recently begun to be applied to vision–language–action (VLA) policies [9, 3, 23], where additional inference-time samples paired with a learned verifier improve manipulation precision; this line of work, however, has so far targeted relatively simple embodiments and arm-only end-effector actions. In this work, we bring the same generate-then-verify paradigm to language- 

conditioned humanoid whole-body motion generation, where it differs along three axes. The candidates are whole-body high-dimensional motions rather than just end-effector actions, so verification must operate in a much more complex action space. Instead of a reward model trained only to evaluate the semantic or kinematic quality of the generated motion, as in recent text-to-motion test-time alignment methods such as ReAlign [22], whose step-aware reward scores candidate motions on semantic alignment and kinematic realism alone, we make the verifier controller-aware by distilling it from whole-body tracker rollouts. This is critical for humanoid whole-body motion: a kinematically plausible reference can still fall outside the tracker’s executable envelope due to balance, contact, or actuation limits, so a motion-only reward cannot certify deployability, only a controller-grounded one can. 

## APPENDIX B 

## LANGUAGE-CONDITIONED MOTION GENERATOR 

This appendix details the FSQ-GPT generator _G_ used in the TEXT stage (Section III-A): the motion corpus and its preprocessing (Section B-A), the FSQ tokenizer that discretizes motion (Section B-B), and the language model that generates motion tokens from text (Section B-C). 

## _A. Data Construction_ 

_a) Motion representation:_ All motions are expressed in a 36-dimensional Unitree G1 representation per frame: root position **p** root _∈_ R<sup>3</sup> , root quaternion (wxyz) **q** root _∈_ R<sup>4</sup> , and 29 joint positions **_θ_** _∈_ R<sup>29</sup> , sampled at 50 Hz. 

_b) Corpora and splits:_ The generator is trained on a combined corpus of AMASS [14] datasets retargeted to G1 (using HumanML3D captions as the text source) and the CLAW [2] dataset. The merged dataset is split 8:1:1 into train/val/test, and this split is fixed before training any downstream module so that the FSQ tokenizer, the language model, the Dynamic Feasibility Verifier, and the Semantic Alignment Verifier all share the same held-out test motions. Sample counts are reported in Table 4. Each motion is paired with 2-5 language instructions, resulting in a total of 9,116 heldout test prompts. 

_c) Module-specific preprocessing:_ Each downstream module normalizes the shared 36-dim motion differently: the FSQ tokenizer applies per-channel standardization; the Dynamic Feasibility Verifier augments each frame with firstand second-order finite differences and applies z-score normalization with clipping (Section C-A); and the Semantic Alignment Verifier replaces the root _XY_ position with frame-toframe velocity to obtain a global-position-invariant embedding (Section C-B). 

## _B. FSQ Tokenizer_ 

_a) Architecture:_ The tokenizer is a Finite Scalar Quantization (FSQ) motion VAE [15]. A 50 Hz, 36-dim G1 motion is encoded by two stride-2 temporal layers (encoder width 512, depth 3, LayerNorm, ReLU) into a code sequence of 

TABLE 4: Sample counts of the combined motion corpus after preprocessing. 

|**Corpus**|**Train**|**Val**|**Test**|**Total**|
|---|---|---|---|---|
|AMASS (with HumanML3D text)|14148|1768|1768|17684|
|CLAW|11977|1497|1497|14971|
|Combined|26125|3265|3265|32655|


TABLE 5: FSQ reconstruction loss weights _λc_ . 

|root pos|root quat|joint pos|root vel|joint vel|root acc|joint acc|
|---|---|---|---|---|---|---|
|1_._0|1_._0|2_._0|1_._0|1_._0|0_._5|0_._5|


length _L_ = _T/_ 4. The FSQ quantizer uses the level vector [3 _,_ 3 _,_ 3 _,_ 3 _,_ 3 _,_ 2 _,_ 2 _,_ 2 _,_ 2 _,_ 2], yielding a fixed codebook of _K_ = � _i_<sup>_ℓi_= 7</sup><sup>_,_776 entries. We adopt FSQ over a learned VQ-VAE</sup> codebook to avoid codebook collapse on our comparatively small humanoid corpus, which we found important for stable training. 

_b) Reconstruction loss:_ Inputs are per-channel standardized and supervised with a SmoothL1 reconstruction loss on the pose together with its first- and second-order temporal derivatives: 


with per-term weights _λc_ given in Table 5. Joint positions are weighted most heavily because they directly drive the downstream tracker. 

_c) Training:_ Optimization and schedule hyperparameters are summarized in Table 6; the tokenizer is trained over sliding windows of 100 frames. 

## _C. Language Model_ 

_a) Tokenized sequence-to-sequence interface:_ We cast text-to-motion as a sequence-to-sequence problem over a shared vocabulary. The frozen FSQ tokenizer maps a continuous motion **m** _∈_ R<sup>_T ×_36</sup> to a discrete code sequence **z** = ( _z_ 1 _, . . . , zL_ ) with _L_ = _T/_ 4 and _zℓ ∈{_ 1 _, . . . , K}_ , _K_ = 7 _,_ 776. We extend the Flan-T5-base [4] vocabulary with these _K_ codes together with three reserved special tokens marking the start, end, and padding of a motion sequence; the end-of-motion token lets the decoder determine the generated motion length at inference time. Text is truncated to 50 sub-word tokens and motion to [16 _,_ 2048] frames, i.e. [4 _,_ 512] motion tokens after the tokenizer’s 4 _×_ temporal downsampling. 

_b) Architecture:_ We initialize from an instruction-tuned Flan-T5 ( _∼_ 220M parameters), whose encoder provides a strong language-understanding prior for conditioning on diverse instructions, while the decoder weights serve as a warm start for autoregressive generation over the extended motiontoken vocabulary. 

_c) Training objective:_ The model is fine-tuned on paired ( _ℓ,_ **m** ) data with teacher forcing under the standard autore- 

gressive cross-entropy over motion tokens, 


where enc( _ℓ_ ) denotes the T5 encoder states for the instruction. 

_d) Sampling for candidate generation:_ At inference, the _N_ candidates of the TEXT stage (Section III-A) are drawn i.i.d. by ancestral sampling, **z** _i ∼ pθ_ ( _· | ℓ_ ), and each token sequence is decoded back to a 36-dim trajectory by the frozen FSQ decoder. The diversity of the candidate pool is controlled by the sampling temperature _τ_ together with top- _k_ / nucleus (top- _p_ ) truncation: a larger _τ_ widens the feasible and semantic spread that the verifiers select from, at the cost of more lowquality samples. All training and sampling hyperparameters are summarized in Table 6. 

## APPENDIX C VERIFIER TRAINING 

## _A. Dynamic Feasibility Verifier_ 

_a) SONIC roll-outs and oracle labels:_ Oracle feasibility labels are collected by rolling out every reference motion offline through the SONIC whole-body tracker [13] in MuJoCo. Each episode is initialized from the first reference frame and advances until the clip ends or an early-termination condition fires. We adopt the height-based termination criteria of BeyondMimic [10]; to avoid duplication, the precise thresholds, the success flag _ys_ , and the progress ratio _qg_ are defined once in Section E and reused verbatim here. Each roll-out thus yields the three signals consumed by Equation (1): the binary success flag _ys_ , the progress ratio _qg_ , and a normalized tracking quality 


_b) Ordering guarantee:_ The constraint _β <_ 1 _/_ (1 + _α_ ) makes _Q_<sup>_∗_</sup> _feasibility-first_ : any successful roll-out scores above any failed one, regardless of other metrics. 

**Proposition 1** (Feasibility-first ordering) **.** _For α, β >_ 0 _, ys ∈{_ 0 _,_ 1 _} and qd, qg ∈_ [0 _,_ 1] _, the quality Q_<sup>_∗_</sup> _of Equation_ (1) 

TABLE 6: Training and sampling configuration of the FSQ-GPT generator. 

||**FSQ Tokenizer**|**Language Model**|
|---|---|---|
|Backbone / init|temporal-conv VAE|Flan-T5-base (instr.-tuned)|
|Optimizer|AdamW|AdamW|
|Learning rate|4_×_10<sup>_−_5</sup>|8_×_10<sup>_−_4</sup>|
|(_β_1_, β_2)|(0_._9_,_0_._99)|(0_._9_,_0_._99)|
|Weight decay|0|0|
|LR schedule|cosine|cosine|
|Batch size|256|32|
|Epochs|100|early-stop (val.)|
|Sampling|—|temp. 1_._0, top-_k_=50, top-_p_=0_._95|


TABLE 7: Prediction accuracy of the three Dynamic Verifier heads on the held-out test set. 

|**Head**|**Metric**||**Value**|
|---|---|---|---|
||AUROC_↑_||0_._979|
|ˆ_ps_ (success)|AUPRC_↑_||0_._997|
||Fail recall_↑_||0_._930|
|ˆ(dnmi)|Spearman _ρ_ vs.|_E_acc_↓_|_−_0_._936|
|_qd_ yacs|Spearman _ρ_ vs.|_E_vel_↓_|_−_0_._932|
|ˆ(roress)|Spearman _ρ_ vs.|progress ratio_↑_|0_._238|
|_qg_ pg|Spearman _ρ_ vs.|progress (on failures)_↑_|0_._925|


_satisfies Q_<sup>_∗_</sup> (1 _, ·, ·_ ) _> Q_<sup>_∗_</sup> (0 _, ·, ·_ ) _for all arguments if and only if β <_ 1+1 _α_<sup>_._</sup> 

_Proof:_ With _qd, qg ∈_ [0 _,_ 1], the two regimes of Equation (1) are bounded as 


and both lower/upper endpoints are attained ( _qd_ = 0 and _qd_ = _qg_ = 1, respectively). The successful range therefore lies strictly above the failed range iff its lower end exceeds the failed upper end, i.e. 1+1 _α_<sup>_> β_.</sup> 

The same bounds show _Q_<sup>_∗_</sup> stays graded _within_ each group: it increases in _qd_ among successes and in _qgqd_ among failures, so the “least-bad” candidate is still preferred when all candidates fail (Table 9). 

TABLE 8: _R_ dyn **ranks candidates in close agreement with the simulator oracle without ever running it.** Within-prompt Kendall _τ_ between _R_ dyn and the oracle quality _Q_<sup>_∗_</sup> on 9,116 held-out prompts. 

|**Prompt type**|**#Prompts**|**Kendall** _τ ↑_|
|---|---|---|
|Mixed (success + failure)|6,759|0_._674|
|All-failure|46|0_._357|
|All-success|2,311|0_._608|
|Overall|9,116|**0.656**|


_c) Model structure and training strategy:_ Each raw 36dim frame is expanded into a 94-dim feature (root dynamics 7, joint positions 29, velocities 29, accelerations 29), z-score normalized and clipped to [ _−_ 10 _,_ 10]. An input projection encodes each semantic group to 128-dim and fuses them into a 256-dim token; a 4-layer causal Transformer ( _d_ model = 256, 4 heads, pre-LayerNorm) followed by mean-attention pooling and three lightweight MLP heads outputs (ˆ _ps,_ ˆ _qd,_ ˆ _qg_ ), which are recombined through Equation (2) with _α_ = 0 _._ 4 _, β_ = 0 _._ 6. The three heads are trained jointly by minimizing, over each batch _B_ , 


where _λd_ = 0 _._ 6, _λg_ = 0 _._ 8, BCE _w_ + is a binary cross-entropy with positive-class weight _w_<sup>+</sup> to offset class imbalance, and the first two terms are averaged over _B_ . The factor (1 _− ys_ ) masks the progress loss to _failed_ roll-outs: a success completes the reference, so _qg ≡_ 1 is a constant copy of _ys_ that carries no gradient, whereas on failures _qg_ varies and is exactly where accurate progress estimates are needed for partial-credit ranking, hence the head is weak on progress overall but strong on failures (Table 7). 

_d) Fidelity studies:_ We validate _R_ dyn on held-out data along two axes: per-head prediction accuracy (Table 7) and 

TABLE 9: Reward-design ablation at _N_ =8. Model weights are fixed; only the inference-time reward formula varies.<sup>_†_</sup> mean progress on all-failure prompts. 

||**Reward formula**|**Succ**_↑_|¯_Q_<sup>_∗_</sup>_↑_|**All-fail prog.**<sup>_† _</sup>_↑_|
|---|---|---|---|---|
|(a)|ˆ_ps_ only|**0.984**|0_._922|0_._395|
|(b)|ˆ_qd_ only|0_._953|0_._916|0_._416|
|(c)|ˆ_qg_ only|0_._982|0_._921|**0.427**|
|(d)|ˆ_ps ·_ˆ_qd_|0_._981|**0.931**|0_._411|
|(e)|ˆ_ps ·_ˆ_qg_|**0.984**|0_._922|0_._395|
|(f)|_Q_<sup>_∗_</sup>formula, Equation (2) (ours)|0_._983|**0.931**|0_._425|


end-to-end ranking agreement with the oracle (Table 8). The success head _p_ ˆ _s_ is highly discriminative (AUROC 0 _._ 979, AUPRC 0 _._ 997) and maintains 0 _._ 930 recall on the minority failure class, so infeasible candidates are rarely mislabeled as feasible. The dynamics head _q_ ˆ _d_ is strongly rank-correlated with both tracking-error signals (Spearman _ρ_ = _−_ 0 _._ 936 and _−_ 0 _._ 932 against acceleration and velocity errors, negative by construction). The progress head _q_ ˆ _g_ has a weak global correlation with the progress ratio ( _ρ_ = 0 _._ 238) because most successful roll-outs cluster near _qg_ = 1, but becomes highly informative on the failed roll-outs where progress genuinely varies ( _ρ_ = 0 _._ 925), precisely the regime where partial-credit ranking is needed. At the composite level, the within-prompt Kendall _τ_ between _R_ dyn and _Q_<sup>_∗_</sup> over 9 _,_ 116 held-out prompts is 0 _._ 656 overall, rising to 0 _._ 674 on _mixed_ prompts containing both feasible and infeasible candidates (Table 8), confirming that _R_ dyn recovers the bulk of the oracle ordering without invoking the tracker. 

_e) Ablation studies:_ We ablate the two design choices that turn the three heads into a single selection reward: the functional _form_ of the recombination, and the _weights_ it places on each term. Table 9 varies the inference-time reward formula at _N_ =8 with the model weights held fixed. Using _p_ ˆ _s_ alone yields the highest raw success rate but collapses to near-random ordering once every candidate in a prompt fails, because it provides no signal to separate equally-infeasible motions; conversely, _q_ ˆ _d_ alone breaks the success-first hierarchy and lets smooth-but-failing candidates win. The full _Q_<sup>_∗_</sup> formula of Equation (2) strikes the best balance: it matches the strongest variants on global quality ( _Q_<sup>¯</sup><sup>_∗_</sup> = 0 _._ 931) while retaining a high all-failure progress score (0 _._ 425), so it still selects the “least bad” candidate when no motion succeeds. 

## _B. Semantic Alignment Verifier_ 

_a) Model structure and training strategy:_ The semantic verifier follows the T2M co-embedding design [5] but is trained _directly_ on the G1 skeleton so that its embedding space is consistent with the candidates produced by the TEXT stage. The motion encoder applies two temporal Conv1d downsampling layers (a MovementConvEncoder) followed by a BiGRU to produce a 512-dim motion embedding _φ_ motion( **m** ); the text encoder sums 300-dim word and 15-dim part-ofspeech embeddings and feeds them through a BiGRU to obtain 

_φ_ text( _ℓ_ ). The ConvEncoder is first pretrained as a motion autoencoder and frozen, after which the two BiGRU encoders are trained jointly with the all-pairs margin contrastive objective in Equation (3) ( _δ_ = 2 _._ 0). The test-time score _R_ text is the exponentiated negative embedding distance. 

_b) Fidelity studies:_ We verify that the contrastive embedding behind _R_ text has actually learned a separating geometry. On the 9 _,_ 116 held-out pairs and a 32-distractor pool, _R_ text attains R@1 = 0 _._ 747 and R@3 = 0 _._ 935 in motion-to-text retrieval, far above the 1 _/_ 32 random baseline (Table 10); shuffling the motion input collapses retrieval to near-random, confirming that the score captures text–motion correspondence rather than a marginal motion prior. 

TABLE 10: _R_ text **separates paired text and motion.** Retrieval sanity check on the held-out test set with a 32-distractor pool. Shuffling the motion input collapses every metric to nearrandom. 

|**Metric**|**Paired (test)**|**Shuffled (control)**|
|---|---|---|
|R@1_↑_|**0.747**|0_._014|
|R@2_↑_|**0.885**|0_._059|
|R@3_↑_|**0.935**|0_._102|
|Matching score_↓_|**0.248**|2_._977|
|Gap (neg_−_pos)_↑_|**2.835**|0_._019|


## APPENDIX D REAL-WORLD RESULTS 

_a) Hardware setup and motion collection:_ All real-world experiments are conducted on a Unitree G1 humanoid robot using the SONIC whole-body tracking policy [13]. We evaluate 30 text prompts spanning locomotion, upper-body gestures, and their combinations. These motions are used to assess whether the references selected by **TEXEDO** can be executed reliably on physical hardware. 

_b) Results:_ **TEXEDO** successfully executes all 30 realworld trajectories on the physical robot. Figure 6 in the main text shows representative execution sequences, and Table 11 reports the per-prompt real-world tracking metrics. 

TABLE 11: Per-prompt real-world deployment metrics. A checkmark indicates that the robot completes the trajectory without falling or early termination. Tracking errors are reported in mm, mm/frame, and mm/frame<sup>2</sup> , respectively; the overall row reports frame-weighted averages. 

|**Prompt**|**Success**|_E_mpjpe-l _↓_|_E_vel _↓_|_E_accel _↓_|
|---|---|---|---|---|
|the man is doing salsa dance|✓|39.14|5.60|3.60|
|the person took a big step over something.|✓|26.18|2.84|1.90|
|a person walks in a circle clockwise.|✓|23.11|3.13|2.42|
|A person appears happy while throwing punches and squatting forward.|✓|47.38|4.68|2.59|
|a person walks forward slowly.|✓|20.04|1.97|1.35|
|The person holds an object and moves forward.|✓|29.35|3.43|1.72|
|A person is carrying something heavy while moving forward.|✓|42.22|3.64|2.21|
|A person throws a right hook ahead.|✓|40.76|5.46|3.08|
|A person dances happily ahead.|✓|32.18|4.90|2.83|
|a person walks straight forward|✓|17.93|2.12|1.55|
|A person executes a left jab forward with force and then throws a left hook ahead with full force.|✓|46.58|6.27|3.40|
|A person moves cautiously right.|✓|21.70|2.33|1.44|
|The person moves while boxing and walking forward.|✓|32.67|4.26|2.51|
|A person jabs right forward and performs a happy dance.|✓|41.41|4.30|2.50|
|A person advances while boxing ahead aggressively.|✓|38.68|4.31|2.20|
|the person is stretching, with their arms above their head.|✓|34.59|0.90|0.66|
|A person carries an object sideways to the right balancing carefully.|✓|43.68|2.99|1.93|
|A person throws a left hook ahead with full force.|✓|41.04|6.70|4.00|
|spinning in a circle in the air.|✓|48.91|11.41|11.09|
|A person shambles left lifelessly.|✓|41.55|4.66|2.60|
|a man is doing jumping jacks.|✓|33.68|6.12|4.15|
|a person walking forward aggressively|✓|21.24|2.37|1.92|
|A person dances joyfully forward with enthusiasm.|✓|30.10|4.76|2.75|
|A person pivots right while moving cheerfully.|✓|49.25|5.98|3.38|
|A person rotates right while sneaking.|✓|33.77|4.77|2.56|
|A person moves while crouching rearward low to the ground.|✓|58.24|4.49|2.08|
|A person bounces along sideways to the left cheerfully and then scurries away rearward frantically.|✓|39.62|2.75|1.71|
|A person scurries away sideways to the left in a panic.|✓|36.96|3.83|2.32|
|a man raises his right hand to his head and then returns it to his side|✓|23.47|1.82|1.43|
|The person stumbles backward in a slow, zombie-like shamble.|✓|36.30|3.36|2.09|
|**Overall**|**30/30**|**37.41**|**4.35**|**2.67**|


where **g** = (0 _,_ 0 _, −_ 1)<sup>_⊤_</sup> is the gravity direction, _B_ ee is the set of end-effector bodies, **p** ˜ denotes anchor-relative body positions, and ( _ha, co, he_ ) = (0 _._ 25 _,_ 0 _._ 8 _,_ 0 _._ 25). Let _τ_ be the first frame at which Equations (10) to (12) fire, or _τ_ = _T_ if the roll-out reaches the end of the reference. Equation (11) compares the _z_ -component of gravity projected into the reference and robot anchor frames, i.e. the deviation in anchor tilt. 

## APPENDIX E METRICS 

We report two families of metrics. Physical metrics measure how well the deployment-time tracker executes the selected motion; the semantic metric measures whether the motion realizes the text instruction. 

_a) Notation:_ A roll-out tracks a reference of _T_ frames over _J_ rigid bodies. At frame _t_ let **p**<sup>ref</sup> _t_<sup>_,j_</sup> _,_ **p**<sup>rob</sup> _t_<sup>_,j_</sup> _∈_ R<sup>3</sup> be the world position of body _j_ in the reference and in the realized robot state, and let **q**<sup>ref</sup> _t_<sup>_,_0</sup> _,_ **q**<sup>rob</sup> _t_<sup>_,_0</sup> be the orientation of the anchor body (pelvis, _j_ =0). We write [ _·_ ] _z_ for the vertical component and **R** ( **q** ) _∈_ SO(3) for the rotation matrix of a quaternion. 

_c) Success and progress:_ 


_b) Termination criteria:_ Following BeyondMimic [10], the episode is terminated at the first frame _t_ at which any of the following _height-based_ conditions fires: 

so a roll-out is **successful** ( _↑_ ) only if it reaches the final reference frame without any termination, and the progress ratio _qgg_ is the fraction of the reference completed before termination. 


mm, mm/frame, and mm/frame<sup>2</sup> ) are 


_E_ mpjpe-l ( _↓_ ) is the root-relative (pelvis-anchored) mean perbody position error; _E_ vel ( _↓_ ) and _E_ accel ( _↓_ ) penalize first- and second-order kinematic mismatch and the factor 10<sup>3</sup> converts m to mm. As in the main experiments, _E_ mpjpe-l, _E_ vel, and _E_ accel are averaged over the executed frames of _successful_ rollouts only, so that tracking error is not confounded with early termination. Finally, _Q_<sup>_∗_</sup> ( _↑_ , Equation (1)) collapses success, tracking quality, and progress into the single oracle quality used as the Dynamic Verifier supervision target. 

_e) Semantic metric:_ To obtain an independent, scalable measure of how well a rendered rollout realizes its text prompt, we adopt a VLM-as-judge ensemble that scores each (text, rendered-rollout video) pair with several lowtemperature VLM calls and reports their mean as a single score in [1 _,_ 10]. The ensemble varies along two main axes to ensure robustness. First, to mitigate the risk of the metric inheriting the idiosyncratic biases of any single model, we query two distinct VLMs from different families, namely GPT-5.5 and `gemini-2.5-flash` , and average their outputs. Second, each model evaluates the video under a 2 _×_ 2 grid combining two evaluation rubrics and two frame counts. The first rubric is a holistic rubric, which tags five key semantic units (ACTION, BODY-PART, SPATIAL, TEMPORAL, ATTRIBUTE) as MATCH, PARTIAL, or MISMATCH, mapping the total fraction of successful matches to a 1–10 scale. The second is a per-axis rubric, which scores the same five dimensions individually on a _{_ 0 _,_ 1 _,_ 2 _}_ scale and sums them. Both rubrics are evaluated at both 8 and 16 uniformly-sampled frames. The denser 16-frame sampling is crucial for catching temporal failures, such as incorrect repetition counts, improper pacing, or trajectory reversals, that might be aliased or missed at 8 frames. Additionally, both rubrics incorporate an agentequivalence clause, which dictates that the humanoid robot stands in for any human referent in the prompt, as well as strict floor caps. These floor caps ensure that a single critical failure, such as an incorrect primary action or an opposite-direction translation, cannot be masked or inflated by matching minor filler details. The final reported semantic score is the mean across all eight configuration calls (2 models _×_ 2 rubrics _×_ 2 frame counts). The full prompts and rubrics are detailed in Section F. 

## APPENDIX F 

## VLM-JUDGE PROMPTS 

This appendix reproduces, verbatim, the two VLMjudge rubrics used by the ensemble of the previous sec- 

tion. Each rubric is issued to both models (GPT-5.5 and `gemini-2.5-flash` ) at two temporal resolutions (8 and 16 uniformly-sampled frames) and at temperature 0, giving the eight calls whose mean is the reported semantic score. 

## _A. Holistic Rubric_ 

```
#AGENTEQUIVALENCE--readfirst
```

```
Thevideoshowsahumanoidrobotperformingamotion.For
allevaluationpurposes,treattherobotasastand-in
foranyhumanreferentinthetext("aperson","the
man","they","thisperson").RobotidentityisNEVERa
reasontolabelaBODYunitasMISMATCH;onlyassess
whetherthereferencedbodypartiscorrectlyinvolved.
```

### `# YOUR ROLE` 

```
Youareastrictevaluatorfortext-conditionedrobot
motiongeneration.Yourjobistofindfailuremodes--
donotbecharitabletothegenerator.Judgeonlyon
observableevidenceinthevideo.Ifevidenceismissing
orambiguous,doNOTdefaulttoMATCH.
```

### `# INPUT` 

- `Text: a natural language description of the target` 

- `motion.` 

```
-Video:eitheranativemp4,orNuniformly-sampled
framesintemporalorder.**Treatthegapsbetween
samplesascontinuousmotionyoudidnotdirectly
observe.**Amomentaryairbornephasebetweenadjacent
framesisnormalforwalkingandisNOTevidenceagainst
"walking".
```

### `# THREE-STEP PROTOCOL` 

```
##Step1--SemanticDecomposition
```

```
Parsethetextintoatomicsemanticunits.**Compound
verbsMUSTbedecomposedintocomponentprimitives.**
Examples:
```

- `"crouch-walks forward" -> ACTION 'crouch posture' +` 

- `ACTION 'walking gait' + SPATIAL 'forward'` 

- `"throws a right hook" -> ACTION 'throw' + BODY 'right` 

- `arm' + ACTION 'hook (curved trajectory)'` 

- `"steps backwards" -> ACTION 'step' + SPATIAL 'backward'` 

- `- "carries an object back and then strides sideways to the right" -> ACTION 'carry object' + SPATIAL 'back' + TEMPORAL 'then' + ACTION 'stride' + SPATIAL 'sideways right'` 

```
Categories(eachunitMUSTgetexactlyone):
-ACTION:averbormovementprimitive("walk","throw",
"wave","jab","swim")
```

- `BODY: a body part or end-effector ("right arm", "both` 

- `hands"). Skip BODY units that just restate the agent -- do NOT create BODY='a person' / BODY='the man'. - SPATIAL: a direction, trajectory, or target ("forward", "sideways right", "above head", "in front of them") - TEMPORAL: sequencing or duration ("first ... then", "after a moment", "several times", "quickly", "then stops")` 

```
-ATTRIBUTE:stylisticquality,magnitude,orspeed
("happily","powerfully","slightly","joyfully").Ifa
worddescribeshowaunitisexecutedratherthanwhatis
executed,it'sanATTRIBUTE.
```

```
DoNOTcreateemptyfillerunits(noACTION='doing',no
BODY='person').Ifapieceoftextaddsnonew
constraint,skipit.Aimfor2-6unitsforsimple
prompts,upto8forcompoundprompts.MarktheFIRST
ACTIONunityouextractasthe**primaryACTION**--it's
theonewhosefailurecapsthescore.
```

```
##Step2--Per-UnitVerification
```

```
Foreachunitassignonelabel.Citeframenumbers(or
timestampsifanativevideo)asevidence.
-MATCH:clearlysatisfiedwithconcretevisible
evidence.
```

```
-PARTIAL:roughlysatisfiedbutwithanoticeable
deviation.Examples:textsays"quickly"butmotionis
normalspeed;textsays"smallsteps"butstepslook
normal-sized;textsays"forward"andnettranslationis
forwardbutminimal.
```

```
-MISMATCH:absent,contradicted,orviolated.**Ifthe
unit'srealizationcannotbeverifiedfromthevideo,
labelMISMATCH--absenceofevidenceisNOTevidenceof
MATCH.**
```

```
Bestrict.Ifyoufindyourselfhedging("seemsto
roughlyresemble..."),thelabelisatbestPARTIAL.
```

```
{"id":3,"category":"ATTRIBUTE","content":
"slowly","label":"PARTIAL","rationale":"Pacelooks
likenormalwalking,notslow."}
```

```
],
```

```
"score":7,
```

```
"justification":"PrimaryACTION'walk'MATCHand
SPATIALMATCH,butATTRIBUTE'slowly'isPARTIAL.f=(2
+0.5*1)/3=0.83,band{7,8}.Floorcapfromone
PARTIAL:<=8.Final:7,downgradedinsidetheband
becausethespeeddeviationisnotminor."
}
```

```
ProduceexactlythatJSONshape(samekeys,same
nesting).Eachunitidisanintegerstartingat1and
incrementing.Scoreisaninteger1..10.Noother
top-levelkeys.
```

```
##Step3--HolisticScoring(DETERMINISTIC)
```

## _B. Per-Axis Rubric_ 

```
ThefinalscoreisderivedfromStep2labels--donot
picka"vibe"number.
```

- `**a) Floor rules (apply first, take the lowest applicable cap):**` 

### `# AGENT EQUIVALENCE` 

```
Thevideoshowsahumanoidrobot.Treattherobotasa
stand-inforany"person"/"man"/"they"referencedin
thetext.Robotidentityisneverareasontopenalize.
```

- `If the video shows no motion related to the text at all` 

- `-> score = 1.` 

- `If the primary ACTION unit is MISMATCH -> score <= 3.` 

- `- If a SPATIAL unit is MISMATCH because the motion is in the opposite direction (e.g., text says "forward" but motion is backward) -> score <= 3.` 

- `If >= 50% of units are MISMATCH -> score <= 3.` 

- `If any unit is MISMATCH and any other unit is MISMATCH` 

- `or PARTIAL -> score <= 7.` 

- `If any unit is PARTIAL (and no MISMATCH) -> score <= 8.` 

```
**b)Candidatescorefromlabelfraction:**
LetM=numberofMATCH,P=numberofPARTIAL,X=
numberofMISMATCH,N=M+P+X.
Computef=(M+0.5*P)/N.Then:
```

- `f >= 0.95 -> candidate in {9, 10}` 

- `0.75 <= f < 0.95 -> candidate in {7, 8}` 

- `0.50 <= f < 0.75 -> candidate in {5, 6}` 

- `0.25 <= f < 0.50 -> candidate in {3, 4}` 

- `f < 0.25 -> candidate in {1, 2}` 

```
Insideeachband,choosethehigherintegerifthe
matchedunitsincludetheprimaryACTIONandnodeviation
feelssevere;otherwisethelowerone.
```

```
**c)Finalscore=min(floor_cap,candidate).**
```

```
Youmayfreelyassign2,4,7,8,9--theyarevalid
scores.Donotcollapsetoroundnumberslike1/3/5/10.
```

```
#OUTPUT--JSONonly,nomarkdownfences,nocommentary
beforeorafter
```

```
OutputasinglevalidJSONobjectwithexactlythefields
shownbelow.Userealintegersandrealstrings--doNOT
includeangle-bracketplaceholderslike`<int>`inyour
output.
```

```
Workedexampleforahypotheticalprompt"walkforward
slowly"wheretherobotwalksforwardbutatnormal
speed:
```

```
{
```

```
"semantic_units":[
```

```
{"id":1,"category":"ACTION","content":"walk",
"label":"MATCH","rationale":"Robotperformsabipedal
walkinggaitwithalternatingstepsfromframe2through
frame8."},
```

```
{"id":2,"category":"SPATIAL","content":
"forward","label":"MATCH","rationale":"Robot
translatesforwardacrossthefloorpattern;visible
positionchangebetweenframe1andframe8."},
```

### `# YOUR ROLE` 

```
Youareastrictevaluatorfortext-conditionedrobot
motion.Judgeonlyonvisibleevidenceintheframes.
Treatunsampledgapsbetweenframesascontinuousmotion
youdidn'tobserve--doNOTusethosegapsasevidence
offailure.
```

- `# INPUT` 

- `Text: a description of the target motion.` 

- `Video: a native mp4, or N uniformly-sampled frames in` 

- `temporal order.` 

### `# FIVE-AXIS PROTOCOL` 

```
Foreachaxisbelow,assignanintegerscorein{0,1,
2}:
```

```
**AxisA--PRIMARYACTION**:themainverbofthetext
(walk,jab,wave,swim,crawl,dance,...).
```

- `2 = robot clearly performs the primary action.` 

```
-1=robotdoessomethingresemblingtheprimary
actionwithsignificantdeviation,ORperformsanaction
thatoverlapspartially.
```

- `0 = robot does something unrelated, or no discernible` 

- `motion.` 

```
**AxisB--BODYPARTCORRECTNESS**:didthecorrectbody
part(s)executetheaction?(e.g.,"rightarm"jabbed,
"bothhands"waved.)
```

- `2 = exactly the body parts named in the text.` 

- `1 = wrong-side limb, OR additional body parts also` 

- `involved beyond what was specified.` 

- `0 = action executed by a completely wrong body part,` 

- `OR the named body part is idle while another acts.` 

- `If the text does not specify a body part, score 2 by` 

- `default.` 

```
**AxisC--SPATIALCORRECTNESS**:direction,trajectory,
target("forward","sidewaysright","infrontofthem",
"backandthentotheside").
```

- `2 = all spatial constraints satisfied.` 

- `1 = some satisfied, some violated; OR direction` 

- `approximately right but small/limited.` 

- `0 = opposite or unrelated direction. If the text says` 

- `"forward" and motion is backward, this is 0.` 

- `If the text has no spatial component, score 2 by` 

- `default.` 

```
**AxisD--TEMPORAL/COUNT/SEQUENCING**:ordering
("first...then"),duration("afteramoment"),
repetitioncount("severaltimes"),pace("quickly").
```

```
-2=repetitioncountandsequencingmatchclearly
(citeframeindicesshowingeachrepetition).
-1=motiontyperightbutcount/duration/order
partiallyoff(e.g.,textsays"severaltimes"butmotion
onlyrepeatsonceortwice;ortextsays"thenstops"but
motioncontinues).
```

```
-0=notemporal/countcomponentsatisfiedatall.
```

```
-Ifthetexthasnotemporal/countcomponent,score2
bydefault.
```

```
**AxisE--ATTRIBUTE/STYLE**:speed,magnitude,
intensity,mood("slowly","powerfully","happily","with
force","slightly").
```

```
-2=thenamedqualityisclearlyobservable.
```

```
-1=partiallyevident(e.g.,"powerfully"--motion
isfastbutnotvisiblyforceful;"joyfully"--motionis
dynamicbutnoclearcelebratoryquality).
```

```
-0=thenamedqualityisabsentorcontradicted.
```

```
-Ifthetexthasnoattribute,score2bydefault.
```

```
#SCOREMAPPING(DETERMINISTIC)
LetS=A+B+C+D+E(sum,range0..10).
```

```
Finalscore=max(1,S).However,applythesefloorcaps
first:
```

```
-IfA=0->finalscore<=3.
```

```
-IfC=0ANDtexthasaspatialcomponent->final
score<=3.
```

- `If A <= 1 -> final score <= 7.` 

```
#OUTPUT--JSONonly
```

```
Workedexamplefortext"Apersonwavesbothhandsat
theirsideseveraltimes.":
{
```

```
"axes":{
```

```
"A_primary_action":{"score":2,"rationale":"Robot
raisesbothhandsandoscillatesthembetweenframes2-8,
consistentwithwaving."},
"B_body_part":{"score":2,"rationale":"Both
handsareclearlyinvolved(textrequired'both
hands')."},
"C_spatial":{"score":1,"rationale":"Hands
moveatchest/facelevelratherthan'attheirside';
minorspatialdeviation."},
"D_temporal":{"score":1,"rationale":"Only
~2visiblewavesintheclip;textsays'severaltimes'
whichimpliesmorethan2."},
"E_attribute":{"score":2,"rationale":"No
attributeintext--default2."}
},
"sum":8,
```

```
"floor_cap_applied":"none",
```

```
"score":8,
```

```
"justification":"Actionandbodypartscorrect;minor
spatialandcountdeviationsbringthisto8."
}
```

```
ProduceaJSONobjectwithexactlythesameshape.Use
realintegers0/1/2foraxisscores.Scoreisinteger
1..10.Nomarkdownfences,nocommentary.
```

