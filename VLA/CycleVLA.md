---
title: "CycleVLA: Proactive Self-Correcting Vision-Language-Action Models via Subtask Backtracking and Minimum Bayes Risk Decoding"
date: "2026-01-05"
authors: "Chenyang Ma; Kai Lu; Guangyu Yang; Jiuming Liu; Shitong Xu; Bill Byrne"
url: https://arxiv.org/abs/2601.02295
pdf: https://arxiv.org/pdf/2601.02295
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.02295)** / [論文ページ](https://arxiv.org/abs/2601.02295)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# **CycleVLA: Proactive Self-Correcting Vision-Language-Action Models via Subtask Backtracking and Minimum Bayes Risk Decoding** 

Chenyang Ma<sup>1</sup> , Kai Lu<sup>2</sup> , Guangyu Yang<sup>3</sup><sup>_†_</sup> , Jiuming Liu<sup>3</sup> , Shitong Xu<sup>1</sup> , Bill Byrne<sup>3</sup> , Ioannis Havoutis<sup>2</sup> , Niki Trigoni<sup>1</sup> , Andrew Markham<sup>1</sup> 


Fig. 1: **Vision–Language–Action models with proactive self-correction capabilities.** We introduce **CycleVLA** , which enables VLAs to anticipate incipient failures and recover before execution collapses. CycleVLA first augments a VLA to estimate subtask-level progress and flag critical subtask transition points, where failures most frequently occur. Then, at these points during inference, a VLM is queried to predict whether the current execution will fail and to decide whether to backtrack. Upon backtracking, the VLA retries using test-time scaling via Minimum Bayes Risk decoding to improve success. This cycle repeats until the task succeeds or execution terminates. 

**_Abstract_ —Current work on robot failure detection and correction typically operates in a post hoc manner, analyzing errors and applying corrections only after failures occur. This work introduces CycleVLA, a system that equips Vision-LanguageAction models (VLAs) with proactive self-correction, the capability to anticipate incipient failures and recover before they fully manifest during execution. CycleVLA achieves this by integrating a progress-aware VLA that flags critical subtask transition points where failures most frequently occur, a VLM-based failure predictor and planner that triggers subtask backtracking upon predicted failure, and a test-time scaling strategy based on Minimum Bayes Risk (MBR) decoding to improve retry success after backtracking. Extensive experiments on the LIBERO and LIBERO-Plus simulation benchmarks show that CycleVLA surpasses the state-of-the-art VLA** _π_ 0 _._ 5 **, improves success rates by correcting execution failures across VLAs of varying capability, from under-trained ones to fully converged policies, and that MBR serves as an effective zero-shot test-time scaling strategy for VLAs. On a real robot, CycleVLA reaches a 91% average success rate on one precise and two long-horizon manipulation tasks. We further conduct stress tests with multiple manually injected perturbations (e.g., swapping in a distractor at the expected location while relocating the true target object mid-execution), where CycleVLA corrects** _∼_ **80% of injected failures and maintains success rates comparable to unperturbed execution.** 

> 1Department of Computer Science, University of Oxford 

> 2Oxford Robotics Institute, University of Oxford 

> 3Department of Engineering, University of Cambridge 

> _†_ Corresponding author. 

## I. INTRODUCTION 

Humans constantly adjust their actions when they sense something going wrong, such as tightening their grip when a glass begins to slip, or adjusting the steering wheel before drifting out of a lane. These corrections happen during the act, not after, because a shattered glass cannot be recovered, and a car off the road is already in danger. Once an error has fully occurred, the opportunity for correction has passed. 

We call this _proactive self-correction_ [1], the ability to detect incipient errors during execution and adapt before failure fully manifests. Replicating this ability in robot agents remains an open challenge. For instance, such a robot should recognize that a grasp is misaligned and reposition its gripper before knocking the object over, completing the task within the execution episode without external intervention. This stands in contrast to most recent work on robot failure detection and correction, which operates in a post hoc manner: execution failures are identified only as or after they occur [2]–[8], and corrective actions are applied retrospectively, often as residual policies [9]–[12]. 

In this work, we aim to equip generalist robot foundation models, specifically Vision-Language-Action models (VLAs) [13]–[15], with proactive self-correcting capabilities, as shown in Fig. 1. Our approach, **CycleVLA** , is motivated by the observation that many robot task failures occur at subtask transitions [16]–[20], and that progress near subtask completion 

2 

provides strong cues for anticipating such failures (e.g., one can tell a peg is misaligned before it jams during insertion). Based on this insight, CycleVLA first introduces a finetuning pipeline that endows VLAs with explicit awareness of subtask progress, addressing a key limitation of existing VLAs that lack mechanisms for stopping or progress estimation [19]. We achieve this by decomposing demonstrations into aligned subtasks and finetuning the VLA with extended action dimensions that predict both a stop signal and subtask progress. 

With a progress-aware VLA, the next challenge is deciding whether to transition to the next subtask or intervene near subtask termination, before failure occurs. CycleVLA addresses this through an explicit backtracking mechanism [21]–[23] guided by a Vision-Language Model (VLM) [24]–[29]. At test time, the VLM acts as a zero-shot failure predictor and planner: if no failure is predicted, execution continues; otherwise, the system reverts to the earliest subtask that restores missing preconditions and retries. 

Finally, to improve the success of retries after backtracking, CycleVLA adopts a zero-shot test-time scaling strategy based on Minimum Bayes Risk (MBR) decoding [30]. Since most VLAs are trained via imitation learning [13], [31], [32], successful behaviors tend to cluster in high-density regions of the policy output space [33], [34], which makes consensus selection over multiple samples more likely to succeed. Inspired by recent applications of MBR decoding in large language models (LLMs) at inference time [35]–[37], we sample multiple trajectories from the VLA and select the one that minimizes expected risk under a distance metric. 

In summary, our main contributions are as follows: 

- We introduce CycleVLA, a system that enables proactive self-correction in VLAs by combining (a) a finetuning pipeline that extends VLAs with subtask progress prediction, (b) a VLM-based failure predictor and planner that uses progress cues to decide if to transit or backtrack between subtasks, and (c) an MBR-based test-time scaling strategy that improves recovery after backtracking. 

- We demonstrate that MBR decoding serves as a zero-shot test-time scaling strategy for improving the success rate of VLA policies. 

- Extensive experiments on LIBERO and LIBERO-Plus simulation benchmarks show that CycleVLA improves success rates by correcting execution failures across VLAs of varying capability, surpassing the state-of-the-art _π_ 0 _._ 5, and remaining effective on under-trained VLAs. 

- We validate CycleVLA on a real robot, reaching a 91% average success rate on one precise and two long-horizon manipulation tasks, and correcting _∼_ 80% of failures under stress tests with multiple manually injected perturbations. 

## II. RELATED WORK 

## _A. Robot Failure Detection and Correction_ 

Most prior work addresses robot failure detection in isolation. Given the scarcity of robot failure data, many approaches rely on failures observed at inference time, using conformal prediction [2], [5], [8], [38], [39], state-based anomaly detection [1], [4], [40], [41], or LLMs/VLMs for failure recognition [3], 

[5], [42]–[44]. Another line of work studies post hoc failure correction, applying retrospective analysis and residual recovery policies after failures occur [9]–[12], [45], [46]. More recent work explores proactive correction during execution, such as combining visuomotor policies with visual world models to anticipate future states [47]–[51], but these incur substantial overhead and architectural changes. In contrast, our work equips generalist robot foundation models with proactive selfcorrection via explicit VLM-based failure prediction, subtasklevel backtracking [21]–[23], and retry. The closest works are PAINT [1] and Bellman-Guided Retrials [23], but PAINT requires human intervention and the latter does not target generalist policies. 

## _B. Data Augmentation for VLAs_ 

VLA training lacks a standard data augmentation strategy, and recent work explores several directions. To tackle longhorizon tasks, some approaches decompose demonstrations into subtasks [16]–[20], [52]–[54], with the active subtask inferred at inference by an external system [18] or the VLA itself [17], [55]. Some works incorporate textual reasoning into training to enable explicit reasoning at inference [55]–[58]. Visual augmentation has also been explored: Cosmos [59] applies video style transfer, while others highlight task-relevant objects [60], [61], akin to visual prompting in VLMs [62]. Our work also adopts subtask decomposition, but specifically focuses on teaching VLAs when to stop at subtask transitions and to track their own progress—capabilities largely absent from existing VLAs [19]. 

## _C. Test-Time Scaling for VLAs_ 

Test-time scaling has proven effective for LLMs [63]– [65], and recent work explores its application to VLAs. RoboMonkey [33] samples actions with Gaussian perturbations and uses a trained VLM to select among candidates. Rover [34] and V-GPS [66] score sampled actions using learned reward or value models. In contrast, our MBR decoding [30], inspired by its use in LLMs [35]–[37], performs training-free consensus selection without external verifiers. 

## III. PRELIMINARIES 

We consider sequential decision-making with the current observation _ot_ (e.g., RGB images and proprioception) and a natural language goal _g_ . A VLA policy _πθ_ maps ( _ot, g_ ) to robot actions. We adopt a continuous end-effector delta action representation _at_ = [∆ _xt,_ ∆ _yt,_ ∆ _zt,_ ∆ _ut,_ ∆ _vt,_ ∆ _wt, γt_ ]<sup>_⊤_</sup> _∈_ R<sup>7</sup> , where (∆ _xt,_ ∆ _yt,_ ∆ _zt_ ) _∈_ R<sup>3</sup> and (∆ _ut,_ ∆ _vt,_ ∆ _wt_ ) _∈_ R<sup>3</sup> denote translational and rotational displacements, and _γt ∈{_ 0 _,_ 1 _}_ indicates the gripper’s open/close state. Unlike autoregressive formulations, we assume the VLA employs parallel decoding to produce a continuous chunk of future actions in a single forward pass, i.e., _πθ_ ( _at_ : _t_ + _H−_ 1 _| ot, g_ ) for chunk size _H_ . At inference time, we further assume the policy supports stochastic decoding, enabling the generation of a finite set of action sequence hypotheses _A_ = _{a_<sup>(1)</sup> _t_ : _t_ + _H−_ 1<sup>_, . . . , a_</sup> _t_<sup>(</sup> :<sup>_N_</sup> _t_ +<sup>)</sup> _H−_ 1<sup>_}_</sup> via repeated forward passes (e.g., stochastic latent variables, diffusion-based noise sampling). 

3 

## IV. CYCLEVLA 

Our goal is to equip VLAs with proactive self-correction capabilities. Our approach, CycleVLA (Fig. 3), builds on the observation that task failures often occur at subtask transitions, where progress near completion provides strong cues for anticipating failure. We first introduce a finetuning pipeline that constructs a subtask-decomposed dataset from demonstrations and trains VLAs to explicitly predict stop and progress signals with lightweight modifications (Sec. IV-A). At inference time, we use an off-the-shelf VLM as a failure predictor and planner to decide whether to transition or backtrack at subtask boundaries (Sec. IV-B). Finally, we apply MBR decoding as a zero-shot test-time scaling strategy to improve retry success after backtracking (Sec. IV-B). 

## _A. Learning Stop and Progress Signals for Subtask Execution_ 

**Constructing a Subtask-Decomposed Dataset.** Most robot demonstration datasets pair each trajectory with only a highlevel task instruction, without subtask labels or their timestamps (e.g., LIBERO [67] and RLBench [68], with few recent exceptions such as BEHAVIOR-1K [69]). We introduce a pipeline that uses LLMs to decompose demonstrations into subtasks with precise start/end timestamps and language instructions (Fig. 2), inspired by prior work [16], [55]. 

Given a task instruction _g_ , we first prompt an LLM to decompose it into a minimal sequence of atomic subtasks ( _g_ 1 _, . . . , gK_ ) using a constrained action vocabulary (e.g., move, rotate, open, close). In parallel, we extract per-step gripper states (open, close, or idle) and movement primitives (e.g., move forward, rotate clockwise, stop) [55] from robot proprio by computing state differences over a sliding window. 

We then align subtasks to the trajectory using gripper state transition segments, which provide reliable subtask boundaries in manipulation tasks (e.g., continuous open/close segments correspond to grasping or releasing objects, while idle segments indicate periods of robot translational or rotational motion with no gripper actuation). If the number of LLM-proposed subtasks matches the number of gripper state segments, we directly pair each subtask with the corresponding segment timestamps. Otherwise, we prompt an LLM with the extracted movement primitive sequence (downsampled to a fixed maximum length to reduce context length) to infer subtask timestamp boundaries, enforcing continuous assignment without gaps while filtering spurious stop or inconsistent primitives. 

**Subtask Finetuning with Extended Action Dims.** With the subtask-decomposed dataset, we finetune the VLA with extended action dimensions to predict stop and progress signals—capabilities not explicitly modeled in existing VLAs [19]. We extend the 7-dim action _at_ to 9-dim: _at_ = [∆ _xt,_ ∆ _yt,_ ∆ _zt,_ ∆ _ut,_ ∆ _vt,_ ∆ _wt, γt, st, pt_ ]<sup>_⊤_</sup> _∈_ R<sup>9</sup> , where _st ∈ {_ 0 _,_ 1 _}_ denotes a stop signal indicating subtask termination, and _pt ∈_ [0 _,_ 1] denotes subtask progress, discretized into bins of 0.1 based on the normalized timestep within each subtask. We explicitly separate these two signals because the stop signal must be precise to support correct subtask transitions, whereas the progress signal only needs to indicate proximity to subtask completion. Following NaVILA [70], we oversample 


Fig. 2: **Pipeline for constructing the subtask-decomposed dataset.** Following LLM subtask decomposition and extraction of movement primitives and gripper state segments, subtasks are directly aligned to gripper state segment timestamps when their counts match; otherwise, an LLM infers subtask boundaries from the movement primitive sequence. Please see Appendices B and F for implementation details and a human evaluation of subtask decomposition quality. 

the last action step of each subtask during training to emphasize termination detection. At inference time, we binarize _st_ via thresholding, as with the gripper signal _γt_ . 

We predict stop and progress jointly with end-effector delta actions as scalar outputs, rather than introducing separate classification heads. This design aligns with the continuous nature of the VLA action space: end-effector displacements are floating-point values, and the gripper signal _γt_ is a bounded scalar. Predicting _st_ and _pt_ in the same output space requires no architectural changes beyond widening the action dimension. 

## _B. Test-Time Scaling via Subtask Backtrack and MBR Decoding_ 

**VLM as a Failure Predictor and Planner.** With a progressaware VLA, we use an off-the-shelf VLM to predict failure and plan recovery at subtask boundaries. When the VLApredicted progress reaches a threshold _τp ∈_ [0 _,_ 1], we query the VLM with synchronized third-person and wrist-mounted camera views, the current subtask, and the subtask list. The VLM outputs a decision: transit to the next subtask, or backtrack to the earliest subtask that restores missing preconditions (e.g., if the grasped object drops midway, backtrack to the grasping subtask). We instruct the VLM to fuse global context from the third-person view (e.g., object identity, gripper pose, if the correct subtask is executed) with fine-grained cues from the wrist view (e.g., gripper alignment with the object, contact quality) via Chain-of-Thought reasoning [71] to decide. 

When backtracking is triggered, we restore the robot configuration to the beginning of the target subtask by reverseexecuting recorded delta actions [23]. Note that backtracking does not restore the object states; instead, the retried execution relies on the VLA re-perceiving the current scene, so CycleVLA works in real settings where the environment does not reset and errors, once they occur, must be corrected. 

4 


Fig. 3: **CycleVLA.** (a) A finetuning pipeline that equips a VLA with subtask-level stop and progress prediction via extended action expert dimension and augmented subtask-decomposed training data. (b) At inference, predicted progress triggers a VLM-based failure predictor and planner, which decides whether to transit to the next subtask or backtrack, and selects the subtask to backtrack to. (c) After backtracking, the VLA retries execution using test-time scaling via MBR decoding to improve success. (d) The workflow of CycleVLA compared to a monolithic VLA without failure correction. See Appendices C and G for MBR implementation details and VLM exact prompts. 

## **Algorithm 1** CycleVLA Inference 

**Sampling Actions and Ranking via MBR.** After backtracking restores a valid subtask precondition, the VLA retries the subtask from the same robot configuration. We apply test-time scaling by sampling multiple action chunk hypotheses and selecting a consensus one via MBR decoding [30]. From current observation _ott_ and subtask _gkk_ , we draw _N_ hypotheses _A_ = _{a_<sup>(1)</sup> _t_ : _t_ + _H−−_ 1<sup>_, . . . , a_(</sup> _t_ :<sup>_N_</sup> _t_ +<sup>)</sup> _H−−_ 1<sup>_}_fromthestochasticpolicy</sup><sup>_πθθ_(</sup><sup>_·|_</sup> _ot, gk_ ). 

**Require:** Task instruction _g_ , VLA policy _πθ_ , VLM _V_ , progress threshold _τp_ , action chunk size _H_ , sample number _N_ , max retries _R_ , timeout _T_ max **Ensure:** Episode success / failure 

1: Decompose _g_ into subtask list _G_ = ( _g_ 1 _, . . . , gK_ ) by _V_ selecting a consensus one via MBR decoding [30]. From current 2: _k ←_ 1; _t ←_ 0; phase _←_ INPROGRESS; _ott_ and subtask _gkk_ , we draw _N_ hypotheses _A_ = action queue _Q ←∅_ ; _r_ 1: _K ←_ 0 _H−−_ 1<sup>_, . . . , a_(</sup> _t_ :<sup>_N_</sup> _t_ +<sup>)</sup> _H−−_ 1<sup>_}_fromthestochasticpolicy</sup><sup>_πθθ_(</sup><sup>_·|_</sup> 3:4: **while** Observe _k ≤ Kot_ **and** _t < T_ max **do** 5: **if** _Q_ = _∅_ **then** MBR selects the hypothesis that minimizes the expected risk 6: Sample chunk _at_ : _t_ + _H−_ 1 _∼ πθ_ ( _· | ot, gk_ ) and push into _Q_ the policy distribution. Let _d_ ( _·, ·, · ·_ ) denote the distance 7: **end if** 8: Pop _at_ from _Q_ and parse _at_ = (˜ _at, st, pt_ ) with _a_ ˜ _t ∈_ R<sup>7</sup> two action chunks. MBR chooses: 9: Execute _a_ ˜ _t_ ; observe _ot_ +1; _t ← t_ + 1 10: **if** episode succeeds **then** _−_ 1<sup>=</sup> argmin E _a_<sup>_′_</sup> _t_ : _t_ + _H−−_ 1<sup>_∼πθπθθ_</sup> � _d_ ( _att_ : _t_ + _H−−_ 1 _, a_<sup>_′_</sup> _t_ : _t_ + _H−−_ 1<sup>)</sup> � _._ 11: **return** success _att_ : _t_ + _H−−_ 1 _∈A_ 12: **end if** (1) 13: **if** phase = INPROGRESS **and** CONFIRM( _pt ≥ τp_ ) **then** approximate the expectation via Monte Carlo using the 14: ( _j,_ dec) _←V_ ( _ot, gk, G_ ), dec _∈{_ transit _,_ backtrack _}_ set _A_ sampled from the policy _πθθ_ ( _· | ot, gk ot, gkt, gk, gkk_ ):: 15: **if** dec = backtrack **and** _rj < R_ **then** 16: _rj ← rj_ + 1 _N_ 17: Restore robot to start of _gj_ via reverse execution; _Q ←∅ L_ ( _a_<sup>(</sup> _t_ :<sup>_i_</sup> _t_<sup>)</sup> + _H−_ 1<sup>) =</sup> _N_<sup>1</sup> � _j_ =1 _d_ � _a_<sup>(</sup> _t_ :<sup>_i_</sup> _t_<sup>)</sup> + _H−_ 1<sup>_, a_(</sup> _t_ :<sup>_j_</sup> _t_<sup>)</sup> + _H−_ 1� _,_ (2) 18:19: SampleObserve _Ao_ =<sup>_′_</sup> _t_<sup>after</sup> _{a_<sup>(</sup> _t_ :<sup>_i_restoration</sup> _t_<sup>)</sup> + _H−_ 1<sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>with</sup><sup>_a_(</sup> _t_ :<sup>_i_</sup> _t_<sup>)</sup> + _H−_ 1<sup>_∼πθ_(</sup><sup>_· | o_</sup> _t_<sup>_′, gj_)</sup> _L_ is the estimated Bayes risk of an action chunk, yielding 20: Select _a_<sup>MBR</sup> _t_ : _t_ + _H−_ 1<sup>viaEq.(4)andset</sup><sup>_Q ←a_MBR</sup> _t_ : _t_ + _H−_ 1 21: _k ← j_ sampling-based _N_ -by- _N_ MBR objective [35]: 22: **else** 23: phase _←_ COMPLETE _a_<sup>MBR</sup> _t_ : _t_ + _H−_ 1<sup>=</sup> argmin _L_ ( _a_<sup>(</sup> _t_ :<sup>_i_</sup> _t_<sup>)</sup> + _H−_ 1<sup>)</sup><sup>_._</sup> (3) 24: **end if** _a_<sup>(</sup> _t_<sup>_i_</sup> : _t_<sup>)</sup> + _H−_ 1<sup>_∈A_</sup> 25: **else if** phase = COMPLETE **and** CONFIRM( _st_ = 1) **then** 26: _k ← k_ + 1; phase _←_ INPROGRESS; _Q ←∅_ instantiate _d_ using distance in predicted end-effector 27: **end if** 

MBR selects the hypothesis that minimizes the expected risk under the policy distribution. Let _d_ ( _·, ·, · ·_ ) denote the distance between two action chunks. MBR chooses: 


We approximate the expectation via Monte Carlo using the hypothesis set _A_ sampled from the policy _πθθ_ ( _· | ot, gk ot, gkt, gk, gkk_ ):: 

where _L_ is the estimated Bayes risk of an action chunk, yielding the sampling-based _N_ -by- _N_ MBR objective [35]: 

We instantiate _d_ using distance in predicted end-effector motion. For each sampled hypothesis _a_<sup>(</sup> _t_ :<sup>_i_</sup> _t_<sup>)</sup> + _H−_ 1<sup>,weaccumu-</sup> late translational and rotational deltas to obtain a predicted trajectory, represented by a feature vector _ϕ_ ( _a_<sup>(</sup> _t_ :<sup>_i_</sup> _t_<sup>)</sup> + _H−_ 1<sup>)</sup><sup>_∈_R6</sup><sup>_H_</sup> containing position ( _x, y, z_ ) and orientation ( _u, v, w_ ) at each step. MBR selects the consensus trajectory: 

28: **end while** 

29: **return** failure 

which minimizes the average pairwise distance over the _N × N_ distance matrix, favoring trajectories in high-density regions of the policy output space. 


**Overall Inference Procedure.** We summarize the complete CycleVLA inference procedure in Alg. 1. The algorithm 

5 

TABLE I: **LIBERO-Plus task performance** (success rates _↑_ ) under seven perturbation dimensions. Dark and light green cells denote the best and second-best results per column. Numbers in parentheses show the average improvement over the corresponding VLA backbone. _†_ OpenVLA-OFT-Diff is trained by us as a single policy across all LIBERO suites on third-person and wrist camera images and proprio, since the original OpenVLA-OFT [72] does not report its diffusion variant in this setting. Please see Appendix D for more details on this baseline. 

|**Method**|**Camera**|**Robot**|**Language**|**Light**|**Background**|**Noise**|**Layout**|**Average**|
|---|---|---|---|---|---|---|---|---|
|OpenVLA [13]|0.8|3.5|23.0|8.1|34.8|15.2|28.5|16.3|
|UniVLA [73]|1.8|46.2|69.6|69.0|81.0|21.2|31.9|45.8|
|OpenVLA-OFT-Diff <sup>_†_</sup>|40.3|40.0|79.2|77.9|79.6|68.1|71.6|65.2|
|_π_0 [14]|13.8|6.0|58.8|85.0|81.4|79.0|68.9|56.1|
|_π_0-FAST [74]|65.1|21.6|61.0|73.2|73.2|74.4|68.8|62.5|
|WorldVLA [75]|0.1|27.9|41.6|43.7|17.1|10.9|38.0|25.6|
|_π_0_._5 [17]|53.0|50.3|65.7|83.1|77.3|53.2|72.7|65.0|
|**CycleVLA** (OpenVLA-OFT-Diff)|46.7|41.7|91.1|85.8|84.6|77.2|81.2|72.6 (+7.4)|
|**CycleVLA** (_π_0_._5)|**74.2**|**72.9**|**96.7**|**96.5**|**91.3**|**86.1**|**84.5**|**86.0**(+21.0)|


alternates between two phases per subtask: INPROGRESS, where the robot executes until predicted progress triggers the VLM check, and COMPLETE, where execution continues until the stop signal confirms subtask termination. 

## V. SIMULATION EXPERIMENTS AND ANALYSIS 

We conduct experiments on simulation benchmarks to answer the following questions: 1) To what extent does our proactive self-correcting VLA improve task success rates, and how many failed trajectories can it recover compared to a monolithic VLA, even with under-trained VLAs? 2) How much does test-time scaling via MBR decoding contribute to performance gains in VLA inference? 3) What is the impact of each component on overall effectiveness? 

TABLE II: **LIBERO task performance** (success rates _↑_ ). All policies compared here are trained via supervised finetuning on demonstrations without RL-based post-training. Color and parenthesis conventions and the definition of _†_ follow Table I. 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|---|
|Diffusion Policy [83]|78.3|82.5|68.3|50.5|72.4|
|Octo-Base [84]|78.9|85.7|84.6|51.1|75.1|
|OpenVLA [13]|84.7|88.4|79.2|53.7|76.5|
|TraceVLA [79]|84.6|85.2|75.1|54.1|74.8|
|SpatialVLA [85]|88.2|89.9|78.6|55.5|78.1|
|CoT-VLA [48]|87.5|91.6|87.6|69.0|81.1|
|ThinkAct [80]|88.3|91.4|87.1|70.9|84.4|
|GR00T N1 [15]|94.4|97.6|93.0|90.6|93.9|
|OpenVLA-OFT-Diff <sup>_†_</sup>|91.7|92.2|90.9|88.4|90.8|
|_π_0_._5 [17]|98.8|98.2|**98.0**|92.4|96.9|
|**CycleVLA** (OpenVLA-OFT-Diff)|97.6|98.1|91.7|93.6|95.3 (+4.5)|
|**CycleVLA** (_π_0_._5)|**99.6**|**99.3**|97.5|**97.6**|**98.5**(+1.6)|


## _A. Implementation Details_ 

**Subtask Decomposition.** We use GPT-4.1 [76] (temperature 0.2) to propose subtasks and infer their timestamp boundaries. The last action step of each subtask is oversampled by a factor of 8. Please see Appendix B for more details. 

**Training and Inference.** We test our approach using two VLA backbones: _π_ 0 _._ 5 [17] and OpenVLA-OFT [72] with a diffusion-based action head (OpenVLA-OFT-Diff). Stochastic sampling is achieved by varying random seeds, which changes the noise sampling in the diffusion/flow matching process. Models are trained on 4 or 8 NVIDIA A100 GPUs (40GB VRAM) and evaluated on 1 NVIDIA A10 GPU (24GB VRAM) unless otherwise specified. We use GPT-5.2 [77] (temperature 1.0) as the VLM-based failure predictor and planner, queried when subtask progress reaches _τp_ = 0 _._ 9. For MBR decoding, we use an _L_ 2 distance metric ( _d_ ) with _N_ = 8 sampled hypotheses. Unless otherwise specified, all analyses beyond the main LIBERO [67] and LIBERO-Plus [78] comparisons use the OpenVLA-OFT-Diff-based CycleVLA on LIBERO. Please see Appendices C and D for more details. 

## _B. Evaluation on Simulation Benchmarks_ 

**Setup.** We evaluate on LIBERO [67] (four task suites: Spatial, Object, Goal, and Long) and LIBERO-Plus [78], which introduces seven dimensions of perturbation to probe CycleVLA’s generalization and robustness under unseen conditions. For 

LIBERO, we follow OpenVLA [13] for data preprocessing and evaluation. Each suite contains 10 tasks, evaluated over 50 rollouts with 3 random seeds. For finetuning, we follow [79]– [81] and train a single model jointly on data from all four suites, rather than training separate models per suite as in [13], [72], [82]. Joint training increases task and scene diversity and thus presents a more challenging learning setting. We report results alongside baseline numbers regardless of the finetuning paradigm. For LIBERO-Plus, we evaluate the same LIBEROtrained models directly on the perturbed environments without additional finetuning, isolating generalization from perturbationspecific adaptation. Evaluation follows LIBERO-Plus protocol. 

**LIBERO Task Performance.** As shown in Table II, prior methods often achieve lower success rates on LIBERO-Long due to its challenging long-horizon nature. CycleVLA achieves notably higher success rates on this task suite by predicting failures at subtask boundaries and backtracking to retry. This self-correcting mechanism is particularly effective for longhorizon tasks, where errors tend to accumulate across subtasks. CycleVLA improves both backbones, with average gains of +4.5 over OpenVLA-OFT-Diff and +1.6 over _π_ 0 _._ 5, the latter reaching the best average success rate (98.5) among all compared methods. OpenVLA-OFT-Diff benefits more, as _π_ 0 _._ 5’s near-saturated performance leaves less room for correction. We further study how much CycleVLA improves less robust VLAs in the under-trained VLA analysis below. 

6 


Fig. 4: **Qualitative examples of CycleVLA in simulation.** CycleVLA performs multiple cycles of failure prediction, backtracking, and retry within a single long-horizon task, correcting errors across subtasks and achieving successful completion. More examples can be found in Appendix D. 

**LIBERO-Plus Task Performance.** From Table I, CycleVLA improves robustness under unseen perturbations for both VLA backbones, with average gains of +7.4 over OpenVLA-OFTDiff and +21.0 over _π_ 0 _._ 5, considerably larger than those on clean LIBERO. We attribute this to the nature of perturbationinduced failures: perturbations rarely eliminate the policy’s ability to act, but instead cause recoverable execution errors such as misgrasps or misplaced objects. A monolithic VLA commits to such errors, whereas CycleVLA detects them at subtask boundaries and retries with newly sampled, MBRselected actions, converting near-misses into successes. Unlike on clean LIBERO, the stronger _π_ 0 _._ 5 backbone gains more here: being more capable, it typically knows what to do under perturbations and merely fails occasionally in execution, producing exactly the recoverable errors CycleVLA is designed to correct. Conversely, the gains are more modest under camera 

and robot-state perturbations for the OpenVLA-OFT-Diff-based variant, likely because these shifts more directly affect the underlying policy’s perception and control. In such cases, failure correction can recover from some execution errors, but its benefit is naturally limited when the base policy does not complete the subtask reliably. 

**Effectiveness on Under-Trained VLAs.** In practice, due to computational constraints or the high difficulty of certain robotic tasks, some VLAs may be under-trained. We investigate whether CycleVLA remains effective across VLAs with varying capacities. We select two intermediate checkpoints (trained after 200K and 350K steps) alongside our final 500K checkpoint, and compare performance before and after applying failure correction. In the no-correction setting, the policy naturally progresses to the next subtask when a stop signal is triggered. Results in Table III show that CycleVLA provides consistent 

TABLE III: **Recovery performance on under-trained VLAs.** Success rates _↑_ on LIBERO with and without failure correction (FC). 

|**Model**|**S**<br>w/o FC|**patial**<br>w/ FC|**O**<br>w/o FC|**bject**<br>w/ FC|w/o FC|**Goal**<br>w/ FC|w/o FC|**Long**<br>w/ FC|**A**<br>w/o FC|**verage**<br>w/ FC|
|---|---|---|---|---|---|---|---|---|---|---|
|CycleVLA-200K|84.7|89.1 (+4.4)|82.0|90.2 (+8.2)|63.6|74.2 (+10.6)|62.3|66.5 (+4.2)|73.2|80.0 (+6.8)|
|CycleVLA-350K|88.4|94.8 (+6.4)|93.8|97.5 (+3.7)|72.6|79.4 (+6.8)|77.9|85.3 (+7.4)|83.2|89.2 (+6.0)|
|CycleVLA-500K|91.1|97.6 (+6.5)|95.3|98.1 (+2.8)|86.5|91.7 (+5.2)|84.4|93.6 (+9.2)|89.3|95.3 (+6.0)|


TABLE IV: **Effect of number of hypotheses on MBR performance.** Estimated success probability ( _P_ succ _↑_ ). w/o FC denotes the average success rate of the base VLA on LIBERO without failure correction. 

|**Model**|**w/o FC**||**4**||**8**||**16**||**32**||**64**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||random|MBR|random|MBR|random|MBR|random|MBR|random|MBR|
|CycleVLA-200K|73.2|72.9|78.2 (+5.3)|71.7|78.5 (+6.8)|71.9|81.2 (+9.3)|72.2|79.7 (+7.5)|72.3|79.7 (+7.4)|
|CycleVLA-350K|83.2|80.5|88.0 (+7.5)|80.3|90.2 (+9.9)|80.2|91.3 (+11.1)|80.4|92.3 (+11.9)|80.7|92.2 (+11.5)|
|CycleVLA-500K|89.3|90.8|94.1 (+3.3)|90.2|95.5 (+5.3)|91.1|95.7 (+4.6)|90.7|95.7 (+5.0)|90.4|95.6 (+5.2)|


7 

TABLE V: **Effect of distance metric on MBR performance.** Estimated success probability ( _P_ succ _↑_ ). w/o FC denotes the average success rate of the base VLA on LIBERO without failure correction. 

|**Model**|**w/o FC**|**Random**|**MBR-**_L_1|**MBR-**_L_2|**MBR-**_L∞_|**MBR-**cos|**MBR-**_r_|
|---|---|---|---|---|---|---|---|
|CycleVLA-200K|73.2|71.7|**78.7 (+7.0)**|78.5 (+6.8)|77.8 (+6.1)|74.1 (+2.4)|73.5 (+1.8)|
|CycleVLA-350K|83.2|80.3|89.7 (+9.4)|**90.2 (+9.9)**|88.2 (+7.9)|87.5 (+7.2)|86.9 (+6.6)|
|CycleVLA-500K|89.3|90.2|94.7 (+4.5)|**95.5 (+5.3)**|94.3 (+4.1)|94.4 (+4.2)|94.8 (+4.6)|


gains across all checkpoints. Notably, CycleVLA bridges the gap between model sizes: the 200K and 350K checkpoints with CycleVLA approach the performance of the 350K and 500K checkpoints without it. 

**Qualitative Results.** We show qualitative examples of CycleVLA in Fig. 4 on tasks with varying horizons. 

## _C. Analysis of MBR Decoding_ 

**Setup.** We evaluate MBR decoding as a test-time scaling strategy for VLAs by measuring its ability to select successful action chunks from multiple stochastic hypotheses. For a given base VLA and MBR hyperparameter setting, results are averaged over 2 randomly selected tasks from each LIBERO task suite (8 tasks in total). 

For each task, we evaluate on _E_ = 200 episodes. In each episode, we execute the VLA for _N_ stochastic trials, following the same execution protocol as the no-correction setting. We record the resulting trajectories and their success outcomes, and treat these _N_ executions as hypotheses. For each episode _e_ , we define the set of decision steps (chunk boundaries) as _Te_ = _{_ 0 _, H,_ 2 _H, . . .}_ , where _H_ is the action chunk size. Each recorded trajectory is divided accordingly, yielding a temporally aligned set of chunk hypotheses _{a_<sup>(</sup> _t_ :<sup>_i_</sup> _t_<sup>)</sup> + _H−_ 1<sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>ateachstep</sup> _t ∈Te_ . 

At each step _t ∈Te_ , we compare two selection strategies over the same hypothesis set: 1) MBR decoding using Eq. (4), and 2) random selection of a single hypothesis. Let _ze,t_<sup>(</sup><sup>_i_)</sup><sup>_∈{_0</sup><sup>_,_1</sup><sup>_}_</sup> indicate whether hypothesis _i_ is successful at decision step _t_ in episode _e_ (inherited from the recorded rollout). For a selection method _m ∈{_ MBR _,_ RANDOM _}_ , let ˆ _ı_<sup>(</sup> _e,t_<sup>_m_)</sup><sup>_∈{_1</sup><sup>_, . . . , N}_denote</sup> the selected hypothesis index at step _t_ . For each episode, we compute a score by averaging the success of the selected chunks over all decision steps. The final estimated success probability is then obtained by averaging over episodes: 


This metric estimates the probability of choosing a successful action chunk from _N_ sampled hypotheses, averaged across trajectory timestamps and repeated runs. 

**Number of Hypotheses.** We study the effect of the number of hypotheses by varying _N ∈{_ 4 _,_ 8 _,_ 16 _,_ 32 _,_ 64 _}_ , using an _L_ 2 distance metric. Increasing _N_ generally improves MBR performance by better approximating expected risk (Eq. (1)), but with diminishing returns and higher computational cost due to increased sampling and pairwise distance evaluation. As shown in Table IV, most gains are achieved when increasing 

TABLE VI: **Ablation study on LIBERO.** Averaged success rate after removing individual components. LAO = last-action oversampling; UB = upper bound; LB = lower bound. 

|**Method**|**Success Rate** _↑_|
|---|---|
|CycleVLA (w/o MBR)|92.5|
|CycleVLA (alt. VLM)|92.8|
|CycleVLA (w/o stop + LAO)|91.1|
|CycleVLA (always-on MBR, UB)|96.9|
|CycleVLA (pred. failure cutoff, LB)|79.7|
|CycleVLA (main)|95.3|


_N_ from 4 to 8, while improvements plateau beyond _N_ = 16, with similar performance for _N_ = 32 and 64. 

Without MBR decoding, random selection achieves a success probability similar to the base VLA because it samples action chunks directly from the model’s stochastic output distribution. Averaging performance across chunks, episodes, and tasks therefore reflects the marginal behavior of the underlying policy, without introducing any bias toward higher-quality candidates. 

In contrast, MBR decoding consistently improves success probability across VLAs of varying capability, with larger gains observed for under-trained models (200K and 350K steps) compared to the fully trained 500K model. This trend aligns with observations in LLMs that weaker models benefit more from MBR-style selection [86], as stronger models tend to produce more self-consistent candidates, reducing the marginal benefit of hypothesis selection. 

**Choice of Distance Metric.** We analyze the sensitivity of MBR decoding to the choice of distance metric _d_ used in the pairwise distance computation (Eq. (4)). We evaluate common metrics, including _L_ 1, _L_ 2, Chebyshev ( _L∞_ ), cosine similarity (cos), and correlation ( _r_ ), with the number of hypotheses fixed to _N_ = 8. As shown in Table V, _L_ 2 consistently achieves the best performance across all VLAs, followed by _L_ 1, while cos and _r_ yield the smallest improvements. We hypothesize this is because translational components are dense along the trajectory, whereas rotational components are sparse, with limited rotation at many timesteps. Distance-based metrics such as _L_ 1 and _L_ 2 therefore better capture magnitude differences in action sequences, while cos and _r_ emphasize directional agreement. 

## _D. Ablation Studies_ 

We evaluate the effectiveness of each component by removing or replacing it with an alternative design. **1) Removing MBR decoding:** After backtracking, MBR decoding is replaced with random hypothesis selection. **2) Changing VLM backbone:** We replace GPT-5.2 [77] with the smaller LLaMA-3.211B [24] to assess robustness. **3) Removing stop signal and** 

8 


Fig. 5: **System setup.** (a) Follower arm end-effector with a wristmounted RealSense D405 camera and a gripper with 10 cm opening. (b) Workspace overview: the follower arm, and the leader arm operated by a human for teleoperated demonstration collection. (c) Front-view camera (RealSense D405) mounted above the workspace. 

**last-action oversampling:** We remove stop signal prediction and last-action oversampling during finetuning, reducing the action to _at_ = [∆ _xt,_ ∆ _yt,_ ∆ _zt,_ ∆ _ut,_ ∆ _vt,_ ∆ _wt, γt, pt_ ]<sup>_⊤_</sup> _∈_ R<sup>8</sup> , and consider a subtask complete when _pt ≥_ 0 _._ 95 at inference. **4) Always-on MBR decoding (upper bound):** MBR decoding is applied at initial execution and every high-progress subtask transitions, without using the VLM to decide if to transit or backtrack. **5) Predicted failure cutoff (lower bound):** When the VLM predicts a potential failure, the episode is immediately terminated and counted as a failure. In principle, the resulting success rate should match that of the VLA without failure correction (Table III), and thus serves to evaluate the robustness of VLM failure prediction. 

From Table VI, removing MBR leads to a moderate drop in success rate, as retrying up to _R_ times (Alg. 1) already provides partial robustness. Using the generally less powerful LLaMA-3.2-11B reduces success rate, as we observe that it more frequently chooses to transit rather than backtrack, missing correction opportunities. Removing stop signal and last-action oversampling degrades performance due to spurious high-progress predictions causing premature termination. The always-on MBR variant achieves the highest success rate, but this comes at a steep efficiency trade-off, requiring _∼_ 2.2 _×_ the inference time of our main method from MBR computation at every subtask transition; our VLM-gated design retains most of the gain at a fraction of the cost. Finally, terminating upon VLM-predicted failure causes a modest _∼_ 10% drop, illustrating LLM/VLM sycophancy [87]–[90]: when asked to predict failure, the VLM tends to confirm this assumption. 

## VI. REAL-WORLD EXPERIMENTS 

We validate CycleVLA on an AgileX PiPER arm, addressing two questions: 1) How does CycleVLA perform on a real robot, and can it detect and recover from errors arising from the VLA policy itself? 2) Under stress testing, where a human manually injects diverse error types, can CycleVLA still recover? 

## _A. Implementation Details_ 

**System Setup and Demonstration Collection.** We use an AgileX PiPER 6-DoF arm in a leader-follower configuration (Fig. 5). Demonstrations are collected via teleoperation, where a human operator moves the leader arm and the follower 


Fig. 6: **Tight tolerances in the teapot-hanging task.** Left: with the teapot body grasped, the remaining gripper clearance is only 1.5 cm. Right: with the peg inserted through the handle, the remaining clearance is only 1.7 cm, requiring accurate positioning when hanging. 

arm mirrors its motion. During policy execution, the leaderfollower mode is disabled and only the follower arm is actuated. Visual observations are captured by two Intel RealSense D405 cameras: a front camera mounted above the workspace and a wrist camera on the follower end-effector. See Appendix E for further details. 

**Training and Inference.** For the real-robot policy, we use _π_ 0 _._ 5 [17], trained on 8 NVIDIA A100 GPUs (40GB VRAM) and evaluated on a robot-local NVIDIA RTX 3090 GPU (24GB VRAM). Inference parameters follow the simulation setup. See Appendices D and E for more details. 

## _B. Evaluation Protocols: Natural Failures and Injected Errors_ 

**Tasks and Setup.** We evaluate on three tasks: 

- _Hang the green teapot on the mug holder._ A precision task where the teapot handle must pass over the wooden peg and the teapot body is only slightly narrower than the maximum gripper opening, requiring an accurate grasp position and orientation (Fig. 6). 

- _Place the grape on the red plate and the apple on the green plate._ A long-horizon task where errors are likely to accumulate across subtasks. 

- _Place the can of corn on the pan and the milk carton in the pot._ A long-horizon task involving reflective cookware surfaces, which challenge visual perception. 

For each task, we collect 100 teleoperated demonstrations with object positions randomized within _±_ 30 cm and orientations within _±_ 60<sup>_◦_</sup> ; subtask timestamps are recorded during teleoperation. Each setting is evaluated over 15 trials with randomized object positions and rotations. We evaluate CycleVLA under two settings of increasing difficulty: standard execution with natural failures, and stress testing with human-injected errors. 

**Standard Execution: Natural Failures.** In this evaluation setting, the robot executes each task autonomously, and failures arise only from the policy’s own execution. We compare CycleVLA against a baseline without failure correction, where the trained VLA transitions to the next subtask whenever it predicts a stop signal. 

**Stress Testing: Human-Injected Errors.** In this more challenging setting, a human manually injects an error into one subtask per trial. Since the closed-loop policy naturally absorbs early perturbations (e.g., the robot simply re-approaches a moved object), we inject errors near subtask completion, just before 

9 


Fig. 7: **Qualitative results of CycleVLA on a real robot.** Errors are injected via manual perturbations during execution. First row: a human perturbs the position and orientation of the mug holder and unhooks the teapot. Second row: a human displaces the grape and the green plate just as the robot is poised to grasp the grape and release the apple. Third row: a human relocates the corn can and the milk carton, placing a similar-looking pepper bottle and a mayonnaise bottle at their original locations, respectively. 

the progress threshold triggers the VLM query, so that each perturbation constitutes a genuine failure requiring correction. This setting directly measures how much CycleVLA can rescue: the VLM must detect the induced failure and backtrack to an appropriate earlier subtask rather than transitioning forward. For each task, we inject three progressively more challenging error types: 

- **Distractor Injection.** The target object remains unchanged, but we place a visually similar distractor nearby to test whether the robot distinguishes the correct target. For example, we add a pink teapot and a yellow mug as the robot approaches the green teapot. 

- **Target Displacement.** We perturb the position and orientation of the placement target during interaction and evaluate whether the robot detects the mismatch and backtracks. For instance, while the robot holds the teapot with the handle around the peg, we move and rotate the mug holder so the peg no longer passes through the handle; similarly, we relocate the plate as the robot is about to release the apple onto it. 

- **Target Substitution.** We replace the target object with an unrelated one and move the original target elsewhere. This error compounds the previous two, as a new object 


Fig. 8: **Real-robot evaluation** (success rates _↑_ ). The baseline uses the same policy without failure correction. CycleVLA is evaluated in the natural-failure setting and under three injected perturbations: distractor injection, target displacement, and target substitution. CycleVLA improves success rates over the baseline in the natural-failure setting and maintains robust performance across all perturbations. 

appears at the expected location while the true target is displaced. For example, as the robot is poised to grasp the grape, we swap in an eggplant under the gripper and relocate the grape. 

10 

**Results and Analysis.** Results are shown in Fig. 8. CycleVLA in the natural-failure setting consistently outperforms the baseline across all three tasks (0.87 vs. 0.73, 0.93 vs. 0.87, and 0.93 vs. 0.80), confirming that failure prediction and retry transfer to real-world execution. The teapot hanging task yields slightly lower success rates than the other tasks, as hanging the teapot onto the mug holder requires precise alignment. Under stress testing, since every trial contains an injected error, the success rate directly reflects the fraction of failures corrected: CycleVLA corrects _∼_ 80% of injected failures on average across all perturbation types and tasks. Across perturbation types, success rates decrease progressively from distractor injection to target displacement to target substitution, reflecting their increasing difficulty. Under target displacement, teapot hanging drops to 0.67 since the perturbation also relocates the mug holder, forcing the robot to retry the precise hanging motion at a new position. Under target substitution, all tasks use visually similar distractors (a pink pot for the teapot, an eggplant for the grape, and a red sausage for the apple), yet cookware packing scores lower than fruit sorting: the policy struggles to distinguish the corn can from the substituted white pepper bottle, possibly aggravated by reflections from the shiny pot wires near the target region. Qualitative examples of these correction behaviors are illustrated in Fig. 7. 

## VII. CONCLUSION AND DISCUSSION 

We introduce **CycleVLA** , a system that equips VLAs with proactive self-correction, the capability to anticipate incipient failures and recover before execution collapses. Experiments on simulation benchmarks and a real robot show that CycleVLA improves success rates by correcting execution failures across VLAs of varying capability, and remains robust under manually injected perturbations. We see our work as an early investigation into granting VLAs such abilities and exploring test-time scaling for VLAs. CycleVLA relies on an external VLM for failure prediction and replanning, and an explicit backtracking mechanism. Future work may investigate integrating these capabilities directly into VLAs to enable end-to-end failure reasoning and learned recovery behaviors, as well as tailored test-time scaling strategies for VLAs. 

**Limitations.** Our backtracking mechanism assumes reversible robot state transitions, which may not hold in highly dynamic or irreversible environments. Test-time scaling via MBR decoding requires multiple forward passes, which increases inference time and can be further optimized for contact-rich tasks requiring high control frequencies. 

11 

## REFERENCES 

- [1] A. Xie, F. Tajwar, A. Sharma, and C. Finn, “When to ask for help: Proactive interventions in autonomous reinforcement learning,” in _Advances in Neural Information Processing Systems_ , 2022. 

- [2] A. Farid, D. Snyder, A. Z. Ren, and A. Majumdar, “Failure prediction with statistical guarantees for vision-based robot control,” in _Robotics: Science and Systems_ , 2022. 

- [3] Y. Du, K. Konyushkova, M. Denil, A. Raju, J. Landon, F. Hill, N. de Freitas, and S. Cabi, “Vision-language models as success detectors,” in _Conference on Lifelong Learning Agents_ , 2023. 

- [4] C. Gokmen, D. Ho, and M. Khansari, “Asking for help: Failure prediction in behavioral cloning through value approximation,” in _International Conference on Robotics and Automation_ , 2023. 

- [5] C. Agia, R. Sinha, J. Yang, Z. Cao, R. Antonova, M. Pavone, and J. Bohg, “Unpacking failure modes of generative policies: Runtime monitoring of consistency and progress,” in _Conference on Robot Learning_ , 2024. 

- [6] R. Ramrakhya, M. Chang, X. Puig, R. Desai, Z. Kira, and R. Mottaghi, “Grounding multimodal llms to embodied agents that ask for help with reinforcement learning,” _arXiv preprint arXiv:2504.00907_ , 2025. 

- [7] N. Sun, Y. Li, C. Wang, H. Li, and H. Liu, “Collabvla: Self-reflective vision-language-action model dreaming together with human,” _arXiv preprint arXiv:2509.14889_ , 2025. 

- [8] Q. Gu, Y. Ju, S. Sun, I. Gilitschenski, H. Nishimura, M. Itkina, and F. Shkurti, “SAFE: multitask failure detection for vision-language-action models,” in _Advances in Neural Information Processing Systems_ , 2025. 

- [9] Z. Liu, A. Bahety, and S. Song, “REFLECT: summarizing robot experiences for failure explanation and correction,” in _Conference on Robot Learning_ , 2023. 

- [10] J. Duan, W. Pumacay, N. Kumar, Y. R. Wang, S. Tian, W. Yuan, R. Krishna, D. Fox, A. Mandlekar, and Y. Guo, “AHA: A vision-languagemodel for detecting and reasoning over failures in robotic manipulation,” in _International Conference on Learning Representations_ , 2025. 

- [11] K. Lu, C. Ma, C. Hori, and D. Romeres, “KitchenVLA: Iterative vision-language corrections for robotic execution of human tasks,” in _International Conference on Robotics and Automation Workshop on Safely Leveraging Vision-Language Foundation Models in Robotics_ , 2025. 

- [12] M. S. Sakib and Y. Sun, “STAR: A foundation model-driven framework for robust task planning and failure recovery in robotic systems,” _arXiv preprint arXiv:2503.06060_ , 2025. 

- [13] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “Openvla: An open-source vision-language-action model,” in _Conference on Robot Learning_ , 2024. 

- [14] P. Intelligence, “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [15] J. B. et al., “GR00T N1: an open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

- [16] V. Myers, C. Zheng, O. Mees, K. Fang, and S. Levine, “Policy adaptation via language optimization: Decomposing tasks for few-shot imitation,” in _Conference on Robot Learning_ , 2024. 

- [17] P. Intelligence, “ _π_ 0.5: a vision-language-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [18] L. X. Shi, B. Ichter, M. R. Equi, L. Ke, K. Pertsch, Q. Vuong, J. Tanner, A. Walling, H. Wang, N. Fusai, A. Li-Bell, D. Driess, L. Groom, S. Levine, and C. Finn, “Hi robot: Open-ended instruction following with hierarchical vision-language-action models,” in _International Conference on Machine Learning_ , 2025. 

- [19] R. Yang, Z. An, L. Zhou, and Y. Feng, “Seqvla: Sequential task execution for long-horizon manipulation with completion-aware vision-languageaction model,” _arXiv preprint arXiv:2509.14138_ , 2025. 

- [20] Y. Fan, P. Ding, S. Bai, X. Tong, Y. Zhu, H. Lu, F. Dai, W. Zhao, Y. Liu, S. Huang, Z. Fan, B. Chen, and D. Wang, “Long-vla: Unleashing longhorizon capability of vision language action model for robot manipulation,” in _Conference on Robot Learning_ , 2025. 

- [21] L. Ke, X. Li, Y. Bisk, A. Holtzman, Z. Gan, J. Liu, J. Gao, Y. Choi, and S. S. Srinivasa, “Tactical rewind: Self-correction via backtracking in vision-and-language navigation,” in _Conference on Computer Vision and Pattern Recognition_ , 2019. 

- [22] X. Shi, Z. Li, W. Lyu, J. Xia, F. Dayoub, Y. Qiao, and Q. Wu, “Smartway: Enhanced waypoint prediction and backtracking for zero-shot vision-andlanguage navigation,” in _International Conference on Intelligent Robots and Systems_ , 2025. 

- [23] M. Du, A. Khazatsky, T. Gerstenberg, and C. Finn, “To err is robotic: Rapid value-based trial-and-error during deployment,” _arXiv preprint arXiv:2406.15917_ , 2024. 

- [24] T. L. . Team, “The llama 3 herd of models,” _arXiv preprint arXiv:2407.21783_ , 2024. 

- [25] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. HerbertVoss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. M. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei, “Language models are few-shot learners,” in _Advances in Neural Information Processing Systems_ , 2020. 

- [26] C. Ma, K. Lu, T.-Y. Cheng, N. Trigoni, and A. Markham, “Spatialpin: Enhancing spatial reasoning capabilities of vision-language models through prompting and interacting 3d priors,” in _Neural Information Processing Systems_ , 2024. 

- [27] F. Yang, C. Ma, J. Zhang, J. Zhu, W. Yuan, and A. Owens, “Touch and go: Learning from human-collected vision and touch,” _Advances in Neural Information Processing Systems_ , 2022. 

- [28] H. Liu, C. Li, Y. Li, and Y. J. Lee, “Improved baselines with visual instruction tuning,” in _Conference on Computer Vision and Pattern Recognition_ , 2024. 

- [29] H. Liang, C. Ma, Y. Zhang, S. Shin, A. Markham, N. Trigoni, and Y. He, “Cairn: Cross-room 3d scene understanding with topology-aware large multimodal models,” _arXiv preprint arXiv:2607.06534_ , 2026. 

- [30] S. Kumar and W. J. Byrne, “Minimum bayes-risk decoding for statistical machine translation,” in _Human Language Technology Conference of the North American Chapter of the Association for Computational Linguistics_ , 2004. 

- [31] O. X.-E. Collaboration, “Open x-embodiment: Robotic learning datasets and RT-X models : Open x-embodiment collaboration,” in _International Conference on Robotics and Automation_ , 2024. 

- [32] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “RDT-1B: a diffusion foundation model for bimanual manipulation,” in _International Conference on Learning Representations_ , 2025. 

- [33] J. Kwok, C. Agia, R. Sinha, M. Foutter, S. Li, I. Stoica, A. Mirhoseini, and M. Pavone, “Robomonkey: Scaling test-time sampling and verification for vision-language-action models,” in _Conference on Robot Learning_ , 2025. 

- [34] M. Dai, L. Liu, Y. Bai, Y. Liu, Z. Wang, R. SU, C. Chen, L. Lin, and X. Wu, “Rover: Robot reward model as test-time verifier for visionlanguage-action model,” _arXiv preprint arXiv:2510.10975_ , 2025. 

- [35] B. Eikema and W. Aziz, “Sampling-based approximations to minimum bayes risk decoding for neural machine translation,” in _Empirical Methods in Natural Language Processing_ , 2022. 

- [36] J. Chen, G. Yang, W. Lin, J. Mei, and B. Byrne, “On extending direct preference optimization to accommodate ties,” in _Advances in Neural Information Processing Systems_ , 2025. 

- [37] G. Yang, J. Chen, W. Lin, and B. Byrne, “Direct preference optimization for neural machine translation with minimum bayes risk decoding,” in _Conference of the North American Chapter of the Association for Computational Linguistics_ , 2024. 

- [38] C. Xu, T. K. Nguyen, E. Dixon, C. Rodriguez, P. T. Miller, R. Lee, P. Shah, R. Ambrus, H. Nishimura, and M. Itkina, “Can we detect failures without failure data? uncertainty-aware runtime failure detection for imitation learning policies,” _arXiv preprint arXiv:2503.08558_ , 2025. 

- [39] F. Yang and C. Ma, “Sparse and complete latent organization for geospatial semantic segmentation,” in _Conference on Computer Vision and Pattern Recognition_ , 2022. 

- [40] J. Wong, A. Tung, A. Kurenkov, A. Mandlekar, L. Fei-Fei, S. Savarese, and R. Martín-Martín, “Error-aware imitation learning from teleoperation data for mobile manipulation,” in _Conference on Robot Learning_ , 2021. 

- [41] H. Liu, S. Dass, R. Martín-Martín, and Y. Zhu, “Model-based runtime monitoring with interactive imitation learning,” in _International Conference on Robotics and Automation_ , 2024. 

- [42] R. Sinha, A. Elhafsi, C. Agia, M. Foutter, E. Schmerling, and M. Pavone, “Real-time anomaly detection and reactive planning with large language models,” in _Robotics: Science and Systems_ , 2024. 

- [43] Y. Guo, Y. Wang, L. Zha, and J. Chen, “Doremi: Grounding language model by detecting and recovering from plan-execution misalignment,” in _International Conference on Intelligent Robots and Systems_ , 2024. 

- [44] C. Li, J. Liu, G. Wang, X. Li, S. Chen, L. Heng, C. Xiong, J. Ge, R. Zhang, K. Zhou, and S. Zhang, “A self-correcting vision-languageaction model for fast and slow system manipulation,” _arXiv preprint arXiv:2405.17418_ , 2025. 

- [45] C. Ma, K. Lu, R. Desai, X. Puig, A. Markham, and N. Trigoni, “Coopera: Continual open-ended human-robot assistance,” in _Advances in Neural Information Processing Systems_ , 2025. 

12 

- [46] C. He, S. Li, C. Ma, B. Zou, L. Sun, J. Chen, J. Xing, Y. Shi, and H. Ma, “Pact: Proactive asking for continual task assistance in human-robot collaboration,” _arXiv preprint arXiv:2605.24350_ , 2026. 

- [47] H. Liu, Y. Zhang, V. Betala, E. Zhang, J. Liu, C. Ding, and Y. Zhu, “Multi-task interactive robot fleet learning with visual world models,” in _Conference on Robot Learning_ , 2024. 

- [48] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn, A. Handa, T. Lin, G. Wetzstein, M. Liu, and D. Xiang, “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models,” in _Conference on Computer Vision and Pattern Recognition_ , 2025. 

- [49] Y. Feng, J. Han, Z. Yang, X. Yue, S. Levine, and J. Luo, “Reflective planning: Vision-language models for multi-stage long-horizon robotic manipulation,” _arXiv preprint arXiv:2502.16707_ , 2025. 

- [50] M. A. et al., “V-JEPA 2: Self-supervised video models enable understanding, prediction and planning,” _arXiv preprint arXiv:2506.09985_ , 2025. 

- [51] J. Tu, F. Yang, C. Ma, X. Yu, Z. Zeng, S. Wu, H. Zhao, Z. Tao, C. Zhang, H. Qian _et al._ , “Unitac: A unified multimodal model for cross-sensor tactile understanding and generation,” _arXiv preprint arXiv:2606.31451_ , 2026. 

- [52] J. Wen, Y. Zhu, J. Li, Z. Tang, C. Shen, and F. Feng, “Dexvla: Visionlanguage model with plug-in diffusion expert for general robot control,” in _Conference on Robot Learning_ , 2025. 

- [53] M. Yan, Y. Wang, Z. Liu, and J. Li, “RDD: retrieval-based demonstration decomposer for planner alignment in long-horizon tasks,” in _Advances in Neural Information Processing Systems_ , 2025. 

- [54] C. Ma, Y. Yang, R. Corcodel, S. Jain, A. Wu, C. Hori, and D. Romeres, “Furniturevla: Learning long-horizon bimanual furniture assembly with vision-language-action model,” _arXiv preprint arXiv:2607.01212_ , 2026. 

- [55] M. Zawalski, W. Chen, K. Pertsch, O. Mees, C. Finn, and S. Levine, “Robotic control via embodied chain-of-thought reasoning,” in _Conference on Robot Learning_ , 2024. 

- [56] Z. Zhou, Y. Zhu, M. Zhu, J. Wen, N. Liu, Z. Xu, W. Meng, R. Cheng, Y. Peng, C. Shen, and F. Feng, “Chatvla: Unified multimodal understanding and robot control with vision-language-action model,” in _Empirical Methods in Natural Language Processing_ , 2025. 

- [57] Z. Zhou, Y. Zhu, J. Wen, C. Shen, and Y. Xu, “Chatvla-2: Vision-languageaction model with open-world embodied reasoning from pretrained knowledge,” in _Advances in Neural Information Processing Systems_ , 2025. 

- [58] W. Chen, S. Belkhale, S. Mirchandani, O. Mees, D. Driess, K. Pertsch, and S. Levine, “Training strategies for efficient embodied reasoning,” in _Conference on Robot Learning_ , 2025. 

- [59] NVIDIA, “World simulation with video foundation models for physical ai,” _arXiv preprint arXiv:2511.00062_ , 2025. 

- [60] A. J. Hancock, A. Z. Ren, and A. Majumdar, “Run-time observation interventions make vision-language-action models more visually robust,” in _International Conference on Robotics and Automation_ , 2025. 

- [61] E. Hannus, M. Malin, T. N. Le, and V. Kyrki, “IA-VLA: input augmentation for vision-language-action models in settings with semantically complex tasks,” _arXiv preprint arXiv:2509.24768_ , 2025. 

- [62] A. Bar, Y. Gandelsman, T. Darrell, A. Globerson, and A. A. Efros, “Visual prompting via image inpainting,” in _Advances in Neural Information Processing Systems_ , 2022. 

- [63] C. Snell, J. Lee, K. Xu, and A. Kumar, “Scaling LLM test-time compute optimally can be more effective than scaling model parameters,” in _International Conference on Learning Representations_ , 2025. 

- [64] DeepSeek-AI, “Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning,” _arXiv preprint arXiv:2501.12948_ , 2025. 

- [65] O. AI, “Introducing openai o3 and o4-mini,” https://openai.com/index/ introducing-o3-and-o4-mini/, 2025. 

- [66] M. Nakamoto, O. Mees, A. Kumar, and S. Levine, “Steering your generalists: Improving robotic foundation models via value guidance,” in _Conference on Robot Learning_ , 2024. 

- [67] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “LIBERO: benchmarking knowledge transfer for lifelong robot learning,” in _Advances in Neural Information Processing Systems_ , 2023. 

- [68] S. James, Z. Ma, D. Rovick Arrojo, and A. J. Davison, “Rlbench: The robot learning benchmark & learning environment,” _Robotics and Automation Letters_ , 2020. 

- [69] C. L. et al., “Behavior-1k: A human-centered, embodied ai benchmark with 1,000 everyday activities and realistic simulation,” _arXiv preprint arXiv:2403.09227_ , 2024. 

   - [71] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi, Q. V. Le, and D. Zhou, “Chain-of-thought prompting elicits reasoning in large language models,” in _Advances in Neural Information Processing Systems_ , 2022. 

   - [72] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-language-action models: Optimizing speed and success,” in _Robotics: Science and Systems_ , 2025. 

   - [73] Y. Wang, X. Li, W. Wang, J. Zhang, Y. Li, Y. Chen, X. Wang, and Z. Zhang, “Unified vision-language-action model,” _arXiv preprint arXiv:2506.19850_ , 2025. 

   - [74] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “Fast: Efficient action tokenization for vision-language-action models,” _arXiv preprint arXiv:2501.09747_ , 2025. 

   - [75] J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang, D. Zhao, and H. Chen, “Worldvla: Towards autoregressive action world model,” _arXiv preprint arXiv:_ , 2025. 

   - [76] O. AI, “Introducing gpt-4.1 in the api,” https://openai.com/index/gpt-4-1/, 2025. 

   - [77] ——, “Introducing gpt-5.2,” https://openai.com/index/ introducing-gpt-5-2/, 2025. 

   - [78] S. Fei, S. Wang, J. Shi, Z. Dai, J. Cai, P. Qian, L. Ji, X. He, S. Zhang, Z. Fei, J. Fu, J. Gong, and X. Qiu, “LIBERO-Plus: A progressive robustness benchmark for vision-language-action models,” in _Conference on Computer Vision and Pattern Recognition_ , 2026. 

   - [79] R. Zheng, Y. Liang, S. Huang, J. Gao, H. D. III, A. Kolobov, F. Huang, and J. Yang, “Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies,” in _International Conference on Learning Representations_ , 2025. 

   - [80] C.-P. Huang, Y.-H. Wu, M.-H. Chen, Y.-C. F. Wang, and F.-E. Yang, “Thinkact: Vision-language-action reasoning via reinforced visual latent planning,” in _Advances in Neural Information Processing Systems_ , 2025. 

   - [81] Y. Yang, Z. Duan, T. Xie, F. Cao, P. Shen, P. Song, P. Jin, G. Sun, S. Xu, Y. You, and J. Liu, “FPC-VLA: A vision-language-action framework with a supervisor for failure prediction and correction,” _arXiv preprint arXiv:2509.04018_ , 2025. 

   - [82] W. Li, R. Zhang, R. Shao, J. He, and L. Nie, “Cogvla: Cognitionaligned vision-language-action model via instruction-driven routing & sparsification,” in _Advances in Neural Information Processing Systems_ , 2025. 

   - [83] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Robotics: Science and Systems_ , 2023. 

   - [84] D. Ghosh, H. R. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, J. Luo, Y. L. Tan, L. Y. Chen, Q. Vuong, T. Xiao, P. R. Sanketi, D. Sadigh, C. Finn, and S. Levine, “Octo: An open-source generalist robot policy,” in _Robotics: Science and Systems_ , 2024. 

   - [85] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, Y. Ding, Z. Wang, J. Gu, B. Zhao, D. Wang _et al._ , “Spatialvla: Exploring spatial representations for visual-language-action model,” _arXiv preprint arXiv:2501.15830_ , 2025. 

   - [86] D. Heineman, Y. Dou, and W. Xu, “Improving minimum bayes risk decoding with multi-prompt,” in _Empirical Methods in Natural Language Processing_ , 2024. 

   - [87] M. Sharma, M. Tong, T. Korbak, D. Duvenaud, A. Askell, S. R. Bowman, E. Durmus, Z. Hatfield-Dodds, S. R. Johnston, S. Kravec, T. Maxwell, S. McCandlish, K. Ndousse, O. Rausch, N. Schiefer, D. Yan, M. Zhang, and E. Perez, “Towards understanding sycophancy in language models,” in _International Conference on Learning Representations_ , 2024. 

   - [88] X. Qiu, H. Pan, W. Zhao, C. Ma, P. P. B. de Gusmao, and N. D. Lane, “Efficient vertical federated learning with secure aggregation,” in _Federated Learning Systems (FLSys) Workshop@ MLSys 2023_ , 2023. 

   - [89] X. Qiu, H. Pan, W. Zhao, C. Ma, P. P. Gusmao, and N. D. Lane, “vfedsec: Efficient secure aggregation for vertical federated learning via secure layer,” _arXiv preprint arXiv:2305.16794_ , 2023. 

   - [90] C. Ma, X. Qiu, D. Beutel, and N. Lane, “Gradient-less federated gradient boosting tree with learnable learning rates,” in _Proceedings of the 3rd Workshop on Machine Learning and Systems_ , 2023. 

   - [91] H. Sun, M. Haider, R. Zhang, H. Yang, J. Qiu, M. Yin, M. Wang, P. L. Bartlett, and A. Zanette, “Fast best-of-n decoding via speculative rejection,” in _Advances in Neural Information Processing Systems_ , 2024. 

   - [92] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis _et al._ , “Droid: A large-scale in-the-wild robot manipulation dataset,” _arXiv preprint arXiv:2403.12945_ , 2024. 

- [70] A.-C. Cheng, Y. Ji, Z. Yang, X. Zou, J. Kautz, E. Biyik, H. Yin, S. Liu, and X. Wang, “Navila: Legged robot vision-language-action model for navigation,” in _Robotics: Science and Systems_ , 2025. 

13 

# **Appendix for** **_CycleVLA_** 

## A. OVERVIEW 

This Appendix includes: 1) details and human evaluation of our subtask decomposition pipeline, 2) implementation details of our MBR decoding strategy, 3) additional experiments and methodology details, 4) real-world system details, and 5) prompt details for the LLM subtask decomposition and VLM failure predictor and planner. 

## B. DETAILS AND EVALUATION OF SUBTASK DECOMPOSITION 

TABLE VII: **Human evaluation of subtask decomposition quality on LIBERO.** 

|**Metric**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|---|
|Absolute Error (steps) _↓_|4.2|3.5|8.0|7.2|5.7|
|Relative Error (%) _↓_|3.9|2.5|5.8|3.0|3.8|


of consistent gripper actions. For an idle segment of length _L_ , if _L_ left + _L_ right _> L_ where _L_ left and _L_ right are the lengths of consecutive consistent gripper actions ( _−_ 1 or +1) on either side, we replace the idle segment with the surrounding value. 

## _B.1. Movement Primitive Extraction_ 

**List of Movement Primitives.** Same as ECoT [55]. Movement labels take the form: 

move [forward/backward] [left/right] [up/down], tilt [up/down], rotate [clockwise/counterclockwise], [close/open] gripper 

Components below threshold are omitted. If no movement is detected, the label is stop. 

**Sliding Window Classification.** Following [55], we classify movement primitives by computing the difference between robot states over a sliding window of 4 timesteps and thresholding each dimension to produce a discrete movement label. 

**Initial Thresholds.** For LIBERO, we convert axis-angle rotation to Euler angles and normalize gripper width from two finger positions to a single value in [0 _,_ 1] using max finger distance of 0.04 m. We use separate thresholds for translation, rotation, and gripper: 

LIBERO: [ _τ_ trans _, τ_ rot _, τ_ grip] = [0 _._ 02 _,_ 0 _._ 0075 _,_ 0 _._ 03] 

**Per-Trajectory Translation Threshold Optimization.** We optimize only the translation threshold per trajectory to minimize: 1) overlaps between translation and gripper movements, and 2) spurious stop labels. We grid search over _τ_ trans _∈_ [ _τ_ trans<sup>init</sup><sup>_−_0</sup><sup>_._01</sup><sup>_, τ_</sup> trans<sup>init+ 0</sup><sup>_._01]with50steps,minimizing:</sup> 


## _B.2. Gripper State Detection_ 

**Trajectory Segmentation.** We segment the trajectory into chunks by detecting transitions in gripper state _γt_ . Each chunk is labeled with its dominant gripper value: close ( _−_ 1), open (+1), or idle (0). 

**Multi-Threshold Voting.** To robustly detect gripper state changes, we run primitive extraction with three gripper thresholds: [0 _._ 028 _,_ 0 _._ 03 _,_ 0 _._ 032]. We extract the gripper dimension from each, average across thresholds, and round to obtain the final label _∈{−_ 1 _,_ 0 _,_ +1 _}_ (close, idle, open). Note that this voting scheme is applied only to gripper state detection, not to movement primitives. 

**Filtering Abnormal States.** We apply a post-filter to remove isolated idle segments that are surrounded by longer sequences 

## _B.3. Movement Primitive Downsampling for LLM-based Subtask Boundary Inference_ 

For trajectories whose length exceeds a fixed maximum threshold of 100 steps, we temporally downsample the movement primitive sequence before querying the LLM for subtask boundary inference. Given a trajectory of length _T >_ 100, we uniformly sample indices with stride _⌈T/_ 100 _⌉_ to preserve global temporal structure. The LLM predicts subtask boundaries over the downsampled index set, which are then projected back to the original trajectory by linear index mapping. 

## _B.4. Qualitative Results of Subtask-Decomposed Dataset_ 

We show qualitative examples of our constructed subtaskdecomposed dataset with timestamp boundaries (one example from each LIBERO task suite) in Fig. 10. 

## _B.5. Human Evaluation_ 

We evaluate the quality of the subtask-decomposed dataset via human annotation. For each LIBERO task suite, we randomly sample one demonstration from each of the 10 tasks (10 per suite, 40 total across four suites). For each sampled demonstration, human annotators inspect the subtask temporal boundaries predicted by the LLM and manually adjust the start and end timestamps when necessary. 

We recruit five human evaluators. We report the mean absolute timestamp deviation between LLM-predicted and human-corrected boundaries and the relative boundary error, defined as the absolute timestamp deviation divided by the average subtask duration (i.e., trajectory length) for each subtask. Results in Table VII demonstrate the precision of our pipeline; tasks with less distinct gripper state boundaries and high degrees of rotation (e.g., LIBERO-Goal) are more challenging to decompose into subtask trajectories. 

## C. IMPLEMENTATION DETAILS OF MBR DECODING 

We sample _N_ =8 hypotheses by re-running stochastic decoding with different random seeds, which changes the noise sampling in the diffusion/flow matching action expert. We compute the _N ×N_ pairwise _L_ 2 distance matrix over trajectory features, and select the hypothesis with minimum average distance. 

14 

TABLE VIII: **Finetuning hyperparameters for OpenVLA-OFT-Diff on LIBERO.** 

|**Hyperparameter**|**Value**|
|---|---|
|pretrained checkpoint|openvla-7b|
|# GPUs|4 _×_ NVIDIA A100 (40GB VRAM)|
|learning rate (LR)|5e-4 (decay to 5e-5 after 335K steps)|
|effective batch size|64 (2 per GPU, gradient accumulation of 8)|
|# train steps|500K|
|# diffusion steps|50|
|input images|1 third-person camera image, 1 wrist-mounted camera image|
|input image size|224 _×_ 224 px|
|use observation history|no (use single-step inputs)|
|LoRA rank|32|
|action chunk size (_H_)|8 steps (predict 8, execute all 8 open-loop at test time)|
|action dimensions|9 (7 robot + 1 stop + 1 progress)|
|use proprio (robot state)|yes|
|use FiLM|no|
|# trainable parameters|313M total (111M LoRA adapter + 185M action head + 17M proprio projector)|
|last-action oversampling|8_×_|
|image augmentations|90% random crops, color jitter:<br>random_resized_crop=dict(scale=[0.9, 0.9], ratio=[1.0, 1.0]),<br>random_brightness=[0.2], random_contrast=[0.8, 1.2],<br>random_saturation=[0.8, 1.2], random_hue=[0.05]|


**Trajectory Features.** For each hypothesis, we accumulate the predicted translational and rotational deltas along the chunk to obtain a cumulative end-effector trajectory. Accumulating deltas rather than comparing them step-wise ensures that the distance reflects divergence in the resulting motion, so that small early deviations that compound over the chunk are weighted accordingly. 

**Pairwise Distance and Selection.** We compute the full _N × N_ pairwise _L_ 2 distance matrix over these features, and select the hypothesis minimizing the average distance to all hypotheses in _A_ , following Eq. (4). The selected chunk is the medoid of the hypothesis set under _d ◦ ϕ_ , and is executed directly without further modification. 

## D. ADDITIONAL EXPERIMENTS AND METHODOLOGY DETAILS 

**Robust Stop and Progress Signal Detection.** Since predicted stop ( _st_ ) and progress ( _pt_ ) signals can be noisy, we apply a confirmation mechanism CONFIRM( _·_ ) before triggering subtask transitions or VLM checks. A high signal refers to either _pt ≥ τp_ (for progress) or _st_ = 1 (for stop). 

We track three quantities: 1) if a high signal has been observed (first_seen), 2) the count of consecutive high signals ( _c_ consec), and 3) the number of low-signal steps since the last high signal ( _c_ gap). A condition is confirmed if either: 

_c_ consec _≥_ 2 or (first_seen _∧ c_ gap _≥_ 2) _,_ (7) 

that is, two consecutive high signals, or a high signal that recurs after at least two low-signal steps. This filters isolated spurious predictions while remaining responsive to genuine transitions. 

**OpenVLA-OFT-Diff Baseline.** We finetune the OpenVLAOFT-Diff baseline ourselves, since the original OpenVLAOFT [72] reports its diffusion variant only in a single-camera configuration without wrist images or proprioceptive state. We train a single monolithic policy across all LIBERO task suites, with a third-person camera image, a wrist camera image, and proprioceptive state as inputs, and with FiLM deactivated. The baseline uses the standard 7-dimensional action space and otherwise shares the training hyperparameters in Table VIII, without the stop and progress dimensions or last-action oversampling used by our method. 

**Training Hyperparameters.** Hyperparameters for finetuning the OpenVLA-OFT [72] backbone with a diffusion-based action head (OpenVLA-OFT-Diff) on LIBERO are listed in Table VIII. For faster convergence, we decay the learning rate from 5e-4 to 5e-5 after 335K gradient steps. For the _π_ 0 _._ 5 [17] backbone, we perform full finetuning initialized from the publicly released _π_ 0 _._ 5-LIBERO checkpoint. Parameters are listed in Table X 

**Runtime Analysis of Test-Time Scaling.** We analyze the contribution of each component in CycleVLA to inference-time overhead under test-time scaling with the OpenVLA-OFT-Diff 

TABLE IX: **Runtime analysis of test-time scaling on LIBERO.** End-to-end runtime in seconds (s _↓_ ) for each component on different GPUs. Percentages indicate share of total inference time. 

|**GPU**|**VLM**|**Action Rollout**|**Action Sampling**|**MBR**|**Backtrack**|**Total**|
|---|---|---|---|---|---|---|
|A10|12.9 (6.0%)|147.6 (68.6%)|47.9 (22.2%)|0.003 (<0.1%)|6.9 (3.2%)|215.3|
|A100|15.3 (19.9%)|44.7 (58.1%)|11.9 (15.5%)|0.002 (<0.1%)|5.0 (6.5%)|76.9|


15 

TABLE X: **Finetuning hyperparameters for** _π_ 0 _._ 5 **on LIBERO and real-robot experiments.** 

|**Hyperparameter**|**Value**|
|---|---|
|pretrained checkpoint|pi05_libero|
|# GPUs|8 _×_ NVIDIA A100 (40GB VRAM)|
|finetuning method|full (all _∼_3.2B parameters trainable)|
|optimizer|AdamW (_β_1=0_._9, _β_2=0_._95, _ϵ_=10<sup>_−_8</sup>, weight decay 10<sup>_−_10</sup>, grad-norm clip 1_._0)|
|learning rate (LR)|5e-5 (constant after 10K linear warmup steps)|
|effective batch size|128 (16 per GPU _×_ 8 GPUs, FSDP sharding)|
|# train steps|30K|
|# denoising steps (inference)|10 (flow-matching)|
|input images|1 third-person camera image, 1 wrist-mounted camera image|
|input image size|224 _×_ 224 px|
|use observation history|no (single-step inputs)|
|action chunk size (_H_)|10 steps (predict 10, execute 5 open-loop at test time)|
|action dimensions|9 (7 robot + 1 stop + 1 progress)|
|use proprio (robot state)|yes (continuous input)|
|EMA decay|0.999|
|last-action oversampling|8_×_|
|image augmentations|Non-wrist: 95% random crop + resize back, _±_5<sup>_◦_</sup>rotation, color jitter (brightness 0.3, contrast 0.4,<br>saturation 0.5). Wrist: color jitter only|


backbone. For each task episode, we record the runtime of: 1) VLM failure prediction and planning (OpenAI API call, Tier-5 user), 2) VLA action inference and robot execution, 3) action sampling after backtracking, 4) MBR pairwise distance computation, and 5) backtracking execution. We compare runtime on NVIDIA A10 and A100 GPUs. From Table IX, standard action rollout remains the dominant bottleneck, while test-time scaling in CycleVLA adds only moderate overhead. With stronger GPUs, the relative proportion of VLM API latency increases, as action inference becomes faster. We consider this overhead acceptable, as test-time scaling methods in LLMs typically incur linear or near-linear runtime increases with the number of samples [63], [91]. 

We further note that the seemingly long end-to-end runtime is not primarily caused by CycleVLA itself. The dominant action rollout cost reflects the inference of the large-scale VLA backbone and the physical execution of the task, and is incurred by any policy regardless of failure correction. The components introduced by CycleVLA (VLM queries, action sampling, MBR computation, and backtracking) add only _∼_ 30% overhead on top of this baseline cost, with MBR selection itself being negligible (<0.1%). CycleVLA’s test-time scaling is thus efficient relative to the execution it corrects. 

**Inference Hyperparameters.** The VLM failure predictor is queried when subtask progress reaches _τp_ = 0 _._ 9. Each subtask allows up to _R_ = 3 retries before forcing completion. We sample _N_ = 8 hypotheses for MBR decoding with _L_ 2 distance. 

**More Qualitative Results.** We show more qualitative examples in Fig. 11. 

## E. ADDITIONAL DETAILS OF REAL SYSTEM 

**Control and Execution.** We use an AgileX PiPER 6-DOF robot arm with a single gripper, controlled via CAN bus. As in simulation, the system operates in end-effector space: at 


Fig. 9: **Example initializations of the three real-world tasks.** Left: teapot hanging. Middle: fruit sorting. Right: cookware packing. Object positions are randomized within _±_ 30 cm and orientations within _±_ 60<sup>_◦_</sup> across trials. 

each 20 Hz control step, the policy outputs a 9-dimensional action _at_ = [∆ _xt,_ ∆ _yt,_ ∆ _zt,_ ∆ _ut,_ ∆ _vt,_ ∆ _wt, γt, st, pt_ ]<sup>_⊤_</sup> , where (∆ _xt,_ ∆ _yt,_ ∆ _zt_ ) and (∆ _ut,_ ∆ _vt,_ ∆ _wt_ ) denote translational and rotational end-effector displacements, _γt_ is the gripper command, _st_ is the stop signal, and _pt_ is the subtask progress signal. The displacements are applied additively in Euler space (target = current + ∆, with orientation wrapped to ( _−π, π_ ]), and the firmware solves inverse kinematics internally via its Cartesian EndPoseCtrl interface. The policy produces action chunks of size _H_ = 10, of which the first 5 actions are executed open-loop before requerying. 

**Teleoperation and Gripper Handling.** During demonstrations, we teleoperate the PiPER arm using a leader–follower setup: the operator physically moves a leader arm by hand, and the follower mirrors its motion through a firmware-level CAN linkage. Since the operator continuously squeezes and releases the leader gripper, the recorded gripper trajectory is inherently continuous, unlike simulation environments where gripper actions are toggled. We retain this continuous gripper representation throughout training (i.e., _γt_ is continuous rather than binary on the real system). At deployment, however, the 

16 

policy’s continuous gripper output is binarized via an openingwidth threshold ( _γt ≤ τ_ close _→_ full close; _γt > τ_ close _→_ position-control tracking) to ensure firm grasps on physical objects. We use _τ_ close = 6 _._ 0 cm by default (fruit sorting and cookware packing) and _τ_ close = 8 _._ 25 cm for teapot hanging, where the wider threshold triggers a firm close earlier to hold the teapot handle securely. 

**Backtracking.** The system records joint positions at every control step during the forward rollout. When the VLM failure predictor triggers a backtrack, the arm rewinds deterministically by replaying the recorded joints in reverse via JointCtrl, then resumes in end-effector mode for the retry. 

**Task Setup and Initialization.** Fig. 9 shows an example initialization for each of the three real-world tasks. 

**Training.** Real-robot finetuning of _π_ 0 _._ 5 uses the same hyperparameters as in Table X, with demonstrations processed as described below. 

**Demonstration Processing.** We collect 100 demonstrations per task at 20 Hz using the leader–follower teleoperation setup. During recording, the operator presses a key to mark subtask boundaries; the per-frame subtask index is used offline to segment each episode and assign per-subtask language instructions. Two Intel RealSense D405 cameras (one wristmounted, one third-person) capture 640 _×_ 480 RGB images, which are resized with aspect-preserving padding to 224 _×_ 224 for the policy. Raw demonstrations undergo DROID-style [92] no-op filtering per subtask: frames whose motion from the previous _kept_ frame falls below threshold (position _<_ 0 _._ 5 mm, orientation _<_ 5 mrad, gripper _<_ 10<sup>_−_3</sup> ) are dropped, while the first and last frames of each subtask are always retained. End-effector delta actions are computed as consecutive-frame differences with orientation deltas wrapped to ( _−π, π_ ]; the gripper command _γt_ is the continuous absolute gripper position rather than a delta. 

Each subtask’s filtered frames receive a fractional progress signal _pt_ that rises from 0 _._ 1 to 0 _._ 9 over the subtask body, discretized in 0 _._ 1 bins. The tail is oversampled: the last frame is repeated 8 times with _st_ = 1 and _pt_ = 1 _._ 0, matching the simulation data pipeline. The 8-dimensional proprioceptive state is [EEF(6) _, γt, −γt_ ]: since the PiPER has a single gripper DOF while the pretrained model expects a two-finger gripper state from simulation, the gripper position fills both slots as [ _γt, −γt_ ] to match the expected input dimensionality. Normalization statistics absorb the scale difference between the real and simulated grippers. 

17 


Fig. 10: **Qualitative examples of subtask-decomposed dataset.** 

18 


Fig. 11: **Additional examples of CycleVLA.** 

19 

## F. PROMPT DETAILS OF SUBTASK DECOMPOSITION 

We show exact prompts for LLMs to propose subtasks and infer their timestamp boundaries based on movement primitive sequence. 

## **<mark>Subtask Proposal Prompt.</mark>** 

## Input: 

1. Task: {language_instruction} 

## Instruction: 

You are given a high-level robotic task description. Your job is to decompose this task into a minimal set of formal subtasks that a robot must perform to complete the task. 

## Rules: 

1. Minimal Subtask Decomposition 

- Focus on the necessary and sufficient actions to complete the task. 

- Do not over-decompose — prefer atomic but essential steps. 

- Ask: What does the robot must do to succeed, regardless of variations in execution? 

2. Object-Centric Reasoning 

- Use the presence and spatial arrangement of objects as key indicators. 

- Mention relative spatial cues (e.g., above the drawer handle) if implied in the task. 

3. Skillset Usage and Formal Language 

- Each subtask must begin with one of these actions (verbs): 

- 1) "Move the gripper ..." 

- 2) "Rotate the gripper ..." 

- 3) "Open the gripper ..." 

- 4) "Close the gripper ..." 

- Keep language precise, formal, and robotic. 

- As a rule of thumb: 

- 1) Move/Rotate is often followed by Close to grasp. 

- 2) Grasped objects are then moved, followed by Open to release. 

Output Format: 

Subtasks: ["<subtask_1>", "<subtask_2>", ...] Reasoning: "<Explain how and why you chose each subtask based on the instruction>" 

## **<mark>Subtask Timestamp Boundary Inference Prompt.</mark>** 

You are an expert reinforcement learning researcher. You have trained an optimal policy to control a robotic arm, which successfully completed a task as specified in natural language. The robot executed a sequence of actions to complete this task. Each action is recorded as a step in a trajectory. 

Input: 

1. Task: {language_instruction} 

2. Subtasks list: {subtasks} 

3. Trajectory features: Each entry in the dictionary corresponds to a single step on the trajectory and describes the move that is about to be executed. 

trajectory_features = {0: "<move_primitive>", 1: "<move_primitive>", ...} 

## Instruction: 

Decompose the entire trajectory into subtasks and assign a start and end step index to each subtask. The goal is to produce a mapping of the form: 

Labeled_dict = {"subtask_1": [start_idx, end_idx], "subtask_2": [start_idx, end_idx], ...} 

## Rules: 

1. Noisy Labels - The trajectory data contains noise. Apply the following rules carefully: 

- "stop" labels often appear even when the robot is still moving. 

- Treat "stop" as movement if it appears between meaningful motion steps. 

20 

- Do NOT segment a new subtask just because you see a "stop". 

- "open/close gripper" labels that persist for very short durations may be noise. However, gripper actions are generally more reliable than motion primitives. 

2. Robust Labeling Strategies 

- Brief, short, inconsistent movement descriptions that conflict with prior and subsequent steps are likely to be noise. 

- Cross-reference other movement labels to decide whether a short-duration label is meaningful or just noise. 

3. Exhaustive Coverage 

- You must not skip any steps. Every step in the trajectory should be assigned to exactly one subtask. 

- There should be no gaps in the index ranges. Subtasks must be labeled sequentially and cover the entire range of the trajectory indices. 

Output Format: Labeled_dict: {"subtask_1": [start_idx, end_idx], "subtask_2": [start_idx, end_idx], ...} Reasoning: "<Explain your logic for identifying and segmenting each subtask>" 

G. PROMPT DETAILS OF FAILURE PREDICTOR AND PLANNER 

We show exact prompts for VLMs to predict failure and plan recovery at subtask boundaries. 

## **<mark>VLM Failure Prediction and Planning Prompt.</mark>** 

You are an expert robot behavior annotator. Decide what the robot should do next given it is ~90% through the current subtask. Your job is to FORECAST whether the current subtask will likely succeed if we continue without corrective repositioning. 

## Input: 

1. Task instruction: {language_instruction} 

2. Subtask list: {subtasks} 

3. Current subtask: {current_subtask} 

4. Visual inputs (two synchronized views): 

- FRONT: third-person view (global alignment, object identity, spatial relations) 

- WRIST: close-up gripper view (detailed contact, local geometry, physical affordances) 

## Decision Rule (forecasting at ~90%): 

- Default to transit when success appears reasonably likely within the next few actions without corrective repositioning. 

- Choose backtrack if strong, unambiguous visual evidence indicates that the subtask will fail without repositioning. 

## View-Specific Fusion Instruction: 

- FRONT view provides global context: object identity, pose, global alignment, reachability, and path clearance. 

- WRIST view provides local interaction cues: gripper orientation, contact points, slip, stability, and detailed positioning relative to affordances. 

- Combine both views to reason about functional success: whether the current configuration supports the intended physical interaction (e.g., grasping, pulling, pushing). 

- FRONT dominates for global spatial reasoning and goal reachability. 

- WRIST dominates for local contact accuracy and grasp quality. 

## Affordance Reasoning Guidance: 

- Evaluate whether the gripper’s pose is consistent with the object’s intended use: 

   - 1) For a bowl: grasping the edge or rim is acceptable and often intended for lifting. 

   - 2) For a drawer: alignment with the handle is the key indicator of readiness. 

   - 3) For a push or pull action: confirm direction and surface contact match the required motion. 

- Do not penalize partial or asymmetric contacts if they serve a valid affordance and appear stable. 

## Wrong Object or Wrong Subtask Detection: 

- In addition to misalignment, detect late-stage "silent failures" involving wrong object engagement or wrong subtask execution. 

- If visual evidence indicates the gripper is interacting with an unintended object, target, or affordance (e.g., lifting or contacting a distractor, manipulating the wrong receptacle, or committing to a different subtask’s goal), output type: backtrack. 

21 

- Set next_subtask to the earliest subtask that restores correct target selection and preconditions (typically a reach, align, or target-identification step, NOT a trivial open/close gripper). 

## Backtracking Target: 

- Backtrack to the earliest subtask that restores the missing precondition (typically a positioning or alignment step that enables correct affordance engagement). 

## Output Format: 

next_subtask: <exact subtask from subtasks list> 

type: <transit / backtrack> 

reason: <explain in a concise paragraph, justifying the decision> 

front_view_evidence: 

- <concise observable cue 1> 

- <concise observable cue 2> 

- <concise observable cue 3> 

- <concise observable cue 4> 

## wrist_view_evidence: 

- <concise observable cue 1> 

- <concise observable cue 2> 

- <concise observable cue 3> 

- <concise observable cue 4> 

## assessment: 

- success_likelihood: <high | medium | low> 

- key_risks: <comma-separated brief phrases> 

- view_agreement: <agree | partial | disagree>; <short phrase on which view dominates and why> 

- decision_basis: <short phrase linking likelihood + dominant cues to decision> 

## Constraints: 

- Focus strictly on observable visual and physical evidence. 

- Keep each bullet concise ( _≤_ 12 words). 

- Use exact strings from subtasks for next_subtask. 

- type must be either transit or backtrack. 

- Return only the specified fields; no extra commentary. 

