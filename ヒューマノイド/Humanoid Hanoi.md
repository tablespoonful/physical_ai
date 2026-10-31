---
title: "Humanoid Hanoi: Investigating Shared Whole-Body Control for Skill-Based Box Rearrangement"
date: "2026-02-14"
authors: "Minku Kim; Kuan-Chia Chen; Aayam Shrestha; Li Fuxin; Stefan Lee; Alan Fern"
url: https://arxiv.org/abs/2602.13850
pdf: https://arxiv.org/pdf/2602.13850
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.13850)** / [論文ページ](https://arxiv.org/abs/2602.13850)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Humanoid Hanoi: Investigating Shared Whole-Body Control for Skill-Based Box Rearrangement** 

**Minku Kim**<sup>_∗_</sup> **Kuan-Chia Chen**<sup>_∗_</sup> **Aayam Shrestha Li Fuxin Stefan Lee Alan Fern** Oregon State University `Project Page: https://osudrl.github.io/Humanoid_Hanoi` 

**Abstract:** We introduce _Humanoid Hanoi_ , a challenge problem for long-horizon humanoid skill composition that requires a robot to repeatedly sequence pickup, locomotion, and placement skills to rearrange stacked boxes in simulation and on hardware. This symbolically simple task exposes a weakness in a common modular humanoid architecture, where reusable high-level skills are learned on top of a shared, task-agnostic whole-body controller (WBC). While such a WBC provides a unified low-level interface for skill composition, it may not be sufficiently hardened to execute the full collection of learned skills under domain randomization and long-horizon closed-loop execution. We compare strategies for addressing this issue, including skill-specific WBC fine-tuning, residual low-level adaptation, and task-driven data aggregation that expands the shared-WBC training distribution with closed-loop trajectories induced by learned skills while preserving its original tracking objective. In our evaluated system, the shared-WBC approach achieves the strongest long-horizon robustness. A direct transition-smoothing intervention further shows that low-level controller handoffs account for a substantial part of the composition loss observed with non-shared controllers. 

**Keywords:** Humanoid Learning, Hierarchical Control, Long-Horizon Challenge 

## **1 Introduction** 

Long-horizon humanoid box rearrangement requires repeated object interaction while maintaining balance, object stability, and task constraints. In this setting, success is not determined by isolated skill competence alone. Small errors in manipulation or locomotion can accumulate across closedloop interactions, changing the states encountered by later skills. These effects are often hidden in short-horizon demonstrations or single-skill evaluations, but become critical in extended horizons. 

To study this problem, we introduce _Humanoid Hanoi_ , a long-horizon humanoid box rearrangement challenge problem inspired by the Tower of Hanoi puzzle. The robot must repeatedly pick, transport, and place boxes under stacking constraints, while action errors affect the initial conditions of later ones. This makes _Humanoid Hanoi_ a compact testbed for evaluating repeated skill reuse, accumulated execution error, transition robustness, and recovery from off-nominal robot-object configurations. The challenge problem is agnostic to the control architecture and humanoid model. 

We use _Humanoid Hanoi_ to study a common modular humanoid architecture in which independently trained skills execute through an always-on, shared, task-agnostic whole-body controller (WBC). In our system, _GoTo_ , _GoTo-with-Box_ , _Pickup_ , and _Place_ skills output task-level directives, while the WBC maps these directives and robot proprioception to joint-level commands. This sharedWBC structure enables reusable skill composition without switching low-level controllers during long-horizon execution. However, our experience in _Humanoid Hanoi_ revealed a key weakness of this architecture: a pretrained WBC may not be sufficiently hardened to robustly execute the full collection of learned skills under domain randomization and long-horizon closed-loop execution. As 

> _∗_ Equal contribution. 

10th Conference on Robot Learning (CoRL 2026), Austin TX, USA. 


**Figure 1:** A problem instance from _Humanoid Hanoi_ . The robot moves boxes between three towers (T1–T3) while respecting stacking constraints. The panels illustrate representative stages of a successful hardware execution (5+ min), with the corresponding symbolic state shown on the bottom. 

new skills are integrated, they can induce robot states and command distributions that fall outside the WBC’s training coverage, reducing robustness over extended horizons. 

We investigate several task-agnostic approaches for addressing this issue. These include skillspecific WBC fine-tuning, residual low-level adaptation, and a rollout aggregation procedure that expands the closed-loop coverage of the shared WBC using executions from individual skills while preserving the original task-agnostic tracking objective. This comparison tests whether long-horizon robustness is better achieved by specializing low-level control for each skill or by expanding the coverage of a shared controller as new skills are added. 

We evaluate in simulation and on the Digit V3 humanoid robot. In simulation, _Humanoid Hanoi_ exposes a gap between isolated skill performance and long-horizon task success. Skill-specific methods can improve individual skill metrics, but switching low-level controllers at skill boundaries can perturb subsequent execution and reduce overall task reliability. In contrast, shared-WBC coverage expansion improves individual skill robustness while preserving a consistent low-level interface, achieving the strongest long-horizon performance. On hardware, we demonstrate successful _Humanoid Hanoi_ trials over three configurations and report practical failure modes. 

In summary, the main contributions of this paper are: 

- **Humanoid Hanoi:** a long-horizon humanoid box rearrangement challenge with a standardized evaluation protocol for studying accumulated execution error, repeated skill reuse, and skilltransition robustness. 

- **Shared vs. non-shared WBC analysis:** an empirical study showing that shared-WBC longhorizon success closely follows isolated skill reliability, while non-shared WBC methods can suffer additional composition losses from low-level controller switching. 

- **Shared-WBC maintenance through task-driven data aggregation:** we study a datasetaggregation strategy that incorporates closed-loop trajectories induced by newly learned skills into the WBC training distribution while preserving its task-agnostic objective. 

2 


**Figure 2:** Long-horizon _Humanoid Hanoi_ execution. Sequential snapshots show a complete Tower of Hanoi style box rearrangement episode. Transparent overlays visualize the executed robot trajectory over time, and **T1** , **T2** , and **T3** denote the target tower locations. Each problem instance is divided into seven _moves_ , each consisting of a sequence of _GoTo_ , _Pickup_ , _GoTo-with-Box_ , and _Place_ skills. 

## **2 Related Work** 

Learning-based humanoid loco-manipulation has made rapid progress using teleoperation, motion capture, imitation learning, and reinforcement learning [1, 2, 3, 4, 5, 6]. These systems demonstrate increasingly capable whole-body behaviors, including object pickup, carrying, contact-rich manipulation, and fixed manipulation routines. However, many learned controllers are tied to a particular task definition or horizon, and do not directly support arbitrary resequencing of reusable skills. Recent systems such as ViRAL [7] demonstrate extended operation through repeated execution, but long-horizon humanoid rearrangement with flexible sequencing of distinct learned skills remains relatively underexplored. 

Box pickup, transport, and stacking have also been studied with model-based planning and control [8, 9] and optimization-based whole-body control [10, 11]. These methods provide strong structure but can be sensitive to modeling assumptions and are not typically evaluated as learned long-horizon rearrangement systems. Closest to our setting is [12], which composes separate endto-end pickup, locomotion, and put-down policies using explicit transition handling. In contrast, we execute all learned skills through a single shared, task-agnostic WBC, so skill composition changes the high-level directive stream rather than switching the low-level controller. 

Our work further studies how to maintain this shared WBC as new skills are introduced. Our coverage-expansion procedure is related to dataset-aggregation approaches such as DAgger [13], in that closed-loop rollouts are used to expand the training distribution. However, rather than learning a task policy from corrective labels, we use skill-induced rollouts to expand the training distribution of an existing task-agnostic whole-body controller while preserving its original tracking objective. We therefore view the procedure as task-driven dataset aggregation for shared-WBC maintenance rather than as a new dataset-aggregation algorithm. 

## **3 Humanoid Hanoi Challenge Problem** 

To systematically evaluate long-horizon box rearrangement, we introduce _Humanoid Hanoi_ , a publicly available challenge problem with benchmark-style metrics inspired by the classical Tower of Hanoi puzzle. _Humanoid Hanoi_ provides a compact problem distribution that exercises many of the core elements of _obstacle-free_ humanoid box rearrangement. In this setting, locomotion does not require obstacle avoidance, and pickup and placement need only account for the manipulated boxes and their support surfaces. The key challenge is that long-horizon rearrangement performance is 

3 


**Figure 3:** Independently trained high-level skills generate task-level commands that are executed through a shared, task-agnostic whole-body controller (WBC). The WBC produces joint-level PD targets that are tracked by a low-level PD controller on the robot. Closed-loop rollouts from composed execution are aggregated to retrain the shared controller, improving robustness while preserving a unified control interface. The base action _a_<sup>base</sup> _t_ specifies base locomotion commands, including a stand bit, planar velocity targets, and yaw rate. 

determined not only by single-skill competence but also by robustness to the off-nominal states induced by prior actions and transitions between skills. Small imperfections in earlier locomotion and placement naturally accumulate into a wide distribution of subsequent robot and box configurations, providing a realistic diagnostic stress test for repeated skill reuse. The challenge is designed to support different humanoids and control architectures in simulation and can be evaluated on hardware. 

Each randomized task requires the robot to move and stack three boxes under Tower of Hanoi style rules: only one box may be moved at a time, and boxes have a fixed ordering (e.g., by size or index) such that higher-ordered boxes may not be placed on lower-ordered ones. Solving a task requires repeated sequencing and reuse of the same loco-manipulation skills over extended horizons, including (i) placement and stacking at different heights (including the floor), (ii) manipulation of boxes with different sizes and masses, (iii) pickup and placement from non-uniform robot and box poses induced by prior GoTo and placement errors, and (iv) varied locomotion paths, including rotation, both with and without a carried box. Full instance generation details are provided in Appendix C.1. 

A trial is successful if all three boxes are stacked at the goal and satisfy the Tower of Hanoi stacking constraints. Each method is evaluated over 100 randomized episodes, and we report success rate and final box pose error metrics (Table 6), which measure the box pose error relative to the ideal tower. An example _Humanoid Hanoi_ execution is shown in Fig. 2. 

## **4 Shared WBC System Overview** 

Our system addresses long-horizon humanoid box rearrangement, where the robot must transform an initial configuration of boxes into a target configuration under placement and stacking constraints. We assume access to the SE(3) pose and size of each box, which define task goals and condition the learned skills. The system uses a small library of reusable skills: _GoTo_ for unloaded locomotion, _GoTo-with-Box_ for transport, and _Pickup_ and _Place_ for manipulation and stacking. 

Fig. 3 shows our control architecture. Each skill is an independent policy that outputs task-level whole-body directives rather than joint commands. These directives are executed by a shared wholebody controller (WBC) [14]. The WBC takes robot proprioception and a partially specified motion 

4 

directive, then outputs joint-level PD targets tracked by a fixed-gain PD controller. By keeping the WBC fixed across skills, composing skills does not switch low-level control laws, and skill composition corresponds primarily to changes in the high-level command. 

Our architecture is agnostic to the task-level sequencer. In this paper, we focus on long-horizon execution and robustness, and generate skill sequences for _Humanoid Hanoi_ using the Tower of Hanoi recursion from perceived box poses. We also implement a symbolic planner interface using PDDL [15], but do not evaluate planning performance beyond this setting. Additional details on the WBC interface and skill training are provided in Appendix A.1 and Appendix B. 

## **5 Shared WBC Coverage Expansion** 

A key practical challenge with a shared WBC is maintaining high reliability as new skills induce state and command distributions that were not well represented during pretraining. In our system, initial skills learned via reinforcement learning achieve high reward in simulation when executed in isolation, yet we observe systematic failures in composed execution and under sim-to-real stressors. For example, low-height pick-ups and other extreme configurations can produce execution errors under domain randomization even when the skill policy outputs reasonable commands. 

We hypothesize that limited coverage in the pretrained WBC is one contributor to these failures. More broadly, a pretrained controller may not cover all of the configurations, contact modes, and command patterns induced by newly learned skills. As the skill library grows, long-horizon composition can expose configurations and command patterns that are poorly represented in the original training distribution, especially under disturbances and sim-to-real shift. This motivates WBC coverage expansion, where we treat the shared WBC as a maintained component whose training distribution can be incrementally expanded as skills are added. 

In particular, rather than changing the architecture or learning skill-dependent low-level control, we expand the WBC training distribution using directive sequences induced by learned skills. For _Extended_ , we augment the reference set with nine successful directive sequences each from _Pickup_ and _Place_ , collected without dynamics randomization. The updated WBC is trained using the same tracking objective, domain-randomization ranges, and disturbance process as the original WBC. Intuitively, this robustifies the shared WBC in the parts of trajectory space that the new skills rely on, improving closed-loop reliability while preserving a unified control interface. In Section 6, we quantify the benefits of this coverage expansion approach and compare against common alternatives that modify the low-level controller on a per-skill basis, such as residual policies [16] and skillspecific fine-tuning. This strategy is agnostic to how skills are learned. Details are provided in Appendix A.2. 

## **6 Simulation Experiments** 

### **6.1 Approaches Compared** 

We compare methods for adapting the pretrained WBC as new skills are added. All simulation experiments use state-based policies rather than visual observations. For all methods except _Joint_ , the learned high-level skill policies are fixed and only the WBC is modified (with regularization), allowing us to isolate the effect of low-level adaptation on skill execution and long-horizon composition. _Joint_ is included as an end-to-end task-objective baseline that removes the shared-WBC interface and directly trains a skill policy together with a low-level controller to output full joint-level PD targets. This setting is motivated by the observation that many failures arise from whole-body tracking and balance: the skill policies often produce reasonable task-level directives, but the WBC may not robustly execute the induced state and command distributions. 

**Base.** _Base_ uses a frozen pretrained shared WBC with no task-specific adaptation. 

5 

|**Metric**|**Skill**|**Base**|**Finetune**|**Residual**|**Extended**|**Joint**|**E2E**<sup>_~~∗~~_</sup>**[12]**|
|---|---|---|---|---|---|---|---|
||||**Full Height Di**|**stribution(**_µ ± σ_|¯_x_**)**|||
|S Rt %|Pickup|89_._43_±_0_._22|92_._83_±_0_._28|**93.15**_±_0_._31|**96.92**_±_0_._15|91_._39_±_0_._35|81_._11_±_0_._36|
|uccess ae ()_↑_|Place|89.75_±_0_._27|**93.51**_±_0_._35|90.76_±_0_._27|**93.03**_±_0_._32|91_._94_±_0_._21|91_._18_±_0_._33|
|CM E|Pickup|5.455_±_0_._017|**5.104**_±_0_._016|5.176_±_0_._019|**4.160**_±_0_._010|5_._394_±_0_._016|4.546_±_0_._016|
|o rror (cm)_↓_|Place|5.480_±_0_._025|**4.908**_±_0_._010|5.901_±_0_._016|**4.339**_±_0_._009|5_._494_±_0_._019|3.904_±_0_._019|
|F Ditibti|Pickup|0.4432_±_0_._0008|**0.4323**_±_0_._0008|0.4341_±_0_._0009|**0.3930**_±_0_._0006|0.4453_±_0_._0008|0.3958_±_0_._0005|
|orce sruon_↓_|Place|0.4254_±_0_._0013|0.4340_±_0_._0005|**0.4179**_±_0_._0010|**0.3714**_±_0_._0007|0_._4279_±_0_._0011|0_._4088_±_0_._0011|
|Box Position Error(cm) _↓_|Place|4.895_±_0_._015|**4.623**_±_0_._016|4.855_±_0_._017|**4.781**_±_0_._020|4_._906_±_0_._020|6_._398_±_0_._026|
|Box Yaw Error(<sup>_~~◦~~_</sup>) _↓_|Place|2.64_±_0_._35|3.71_±_0_._37|**2.34**_±_0_._26|2.48_±_0_._37|**2.33**_±_0_._19|11_._1_±_0_._13|
||||**Low Box Hei**|**ghts(**_<_ 0_._2**m) (**|_µ_**)**|||
|S Rt %|Pickup|85.00|**89.43**|**89.43**|**95.03**|86_._46|73_._13|
|uccess ae ()_↑_|Place|85.06|**90.40**|86.93|**91.50**|85.53|91.26|
|CM E|Pickup|5.676|**5.455**|5.520|**2.731**|5.550|5.068|
|o rror (cm)_↓_|Place|5.515|**4.690**|5.798|**4.216**|5.461|4.639|
|Force|Pickup|0.4714|0.4705|0.4685|**0.3854**|**0.4679**|0.4096|
|Distribution _↓_|Place|0.4739|0.4556|**0.4339**|**0.4065**|0.4775|0.4139|


> _∗_ Prior E2E is a non-hierarchical end-to-end controller from [12], included only as an external reference and is not part of the comparison. **Table 1:** Performance on _Pickup_ and _Place_ across box heights with dynamics randomization. **Top:** box and target heights are sampled from the full distribution (mean _µ_ and standard error _σx_ ¯) over 10 fixed random seeds (1000 episodes per seed). **Bottom:** low box and target heights ( _<_ 0 _._ 2m), reporting mean performance over 3000 episodes. **Gold** and **Silver** cells denote the best and second-best results, respectively. 

**Finetune.** _Finetune_ adapts the WBC separately for each skill by finetuning using the corresponding skill reward. This produces skill-specific WBCs that are switched according to the active skill. 

**Residual.** _Residual_ learns a skill-specific residual on top of the frozen WBC, optimized with the corresponding skill reward. This is similar to [6], except that target motions are generated by policies rather than mocap. 

**Extended.** _Extended_ maintains a single shared WBC and expands its coverage via task-driven data aggregation. (Section 5). 

**Joint.** _Joint_ jointly trains the skill policy and low-level controller using the corresponding skill reward. Unlike the other methods, it does not preserve the WBC directive interface and directly outputs joint-level PD targets. 

### **6.2 Individual Skill Evaluation** 

We evaluate the baselines on _Pickup_ and _Place_ across randomized box parameters, target heights, and domain randomization. We omit _GoTo_ since _Base_ already achieves strong locomotion performance. We report task success, stability metrics including center-of-mass (CoM) error and foot force distribution, and box pose error for _Place_ . In addition to the hierarchical methods, as a point of reference, we include individual skill results for prior box loco-manipulation work [12] that used end-to-end training for each skill. 

Table 1 shows that adaptation generally improves over _Base_ , but _Extended_ produces the most consistent gains across success and stability metrics. In particular, _Extended_ achieves the largest reductions in CoM error and force imbalance across both _Pickup_ and _Place_ , including the challenging low-height regime where stability margins are small. 

A possible explanation is that reward-based adaptation is a harder optimization problem than extending the pretrained WBC objective. _Extended_ preserves the existing tracking and stabilization structure of the WBC while expanding its state-command coverage. In contrast, _Finetune_ , _Residual_ , and _Joint_ adapt low-level control through task rewards that only indirectly supervise stabilization, despite acting in a high-dimensional whole-body action space. Although these methods improve over the frozen _Base_ controller, they produce less consistent gains across success and stability metrics than _Extended_ . In our setting, preserving the pretrained WBC objective while expanding its training distribution produces more consistent gains than directly adapting low-level control using the evaluated task-reward objectives. 

6 


**Figure 4:** Cumulative task success rates for Humanoid Hanoi. Each _move_ consists of four skills: _GoTo_ , _Pickup_ , _GoTo with Box_ , and _Place_ , shown as small markers, with large markers indicating move completion. Drops between consecutive points indicate failures in the subsequent skill (e.g., a drop from _Pickup_ to _GoTo with Box_ indicates failures during the _GoTo with Box_ execution). End-to-end results from [12] are omitted because they achieved only 1/100 complete-task success without DR and 0/100 with DR. 

### **6.3 Humanoid Hanoi Evaluation** 

We evaluate long-horizon skill composition on the same 100 randomized Humanoid Hanoi instances for every method, generated using a fixed seed. Each instance is solved by executing the standard Tower of Hanoi recursion, which results in seven sequential _moves_ , each consisting of four skills, shown in yellow and red arrows in Fig. 2. Each instance randomizes the tower layout within a workspace radius of 1.5–2.5 m, with a minimum tower separation of 0.9 m. Box sizes (0.26–0.35 m), masses (0.5–3.0 kg), and friction are also randomized. We evaluate both with and without robot dynamics randomization. 

Fig. 4 reports _task survival_ as execution progresses. Without dynamics randomization (DR), _Extended_ achieves approximately 70% complete-task success, yielding the highest overall completion rate. In contrast, while _Finetune_ , _Residual_ , and _Joint_ can improve performance at individual skill stages, their survival drops sharply under long-horizon composition, and their complete-task success is worse than _Base_ . A similar trend holds under DR. While _Extended_ ’s complete-task success decreases to 47%, it maintains a substantial margin over the other methods throughout the horizon, indicating improved robustness to environmental variability and skill-induced distribution shift. 

As a diagnostic, we compare _Humanoid Hanoi_ complete-task success with an estimate obtained by multiplying the corresponding _Pickup_ and _Place_ success rates from Table 1 over the seven _Humanoid Hanoi_ moves. Interestingly, the shared-WBC methods ( _Base_ and _Extended_ ) approximately match this estimate: _Base_ achieves 24% success rate compared with a 21.45% estimate, and _Extended_ achieves 47% compared with a 48.44% estimate. In contrast, the non-shared methods fall substantially below their isolated-skill estimates: _Finetune_ , _Residual_ , and _Joint_ achieve 21%, 19%, and 16% success rates, compared with estimates of 37.13%, 30.87%, and 29.56%, respectively. This suggests that the shared-WBC architecture better preserves the relationship between isolated skill reliability and long-horizon task success, making improvements to individual skills more predictive of gains in full-task performance. 

### **6.4 Controller Consistency in Long-Horizon Composition** 

The gap between isolated-skill estimates and observed _Humanoid Hanoi_ success suggests that nonshared WBCs introduce additional errors during skill composition. We analyze this effect at transitions into _Place_ , where most long-horizon failures occur. We compare the shared _Extended_ WBC and the non-shared _Finetune_ baseline over 100 trials. 

Fig. 5 (Top) shows a representative lower-body response around the transition into _Place_ . Although both controllers are initialized from the same pretrained WBC, _Finetune_ produces an abrupt change in the PD target at the skill boundary, followed by a corresponding motor position transient. In contrast, _Extended_ exhibits substantially smaller command and state changes because the same lowlevel WBC remains active across skills. This indicates that skill-specific WBCs can introduce discontinuities in closed-loop behavior even when they perform well in isolation. 

7 


**Figure 5:** Top: Representative hip-yaw response around the transition into _Place_ , Bottom: Box state changes after the transition into _Place_ over 100 _Humanoid Hanoi_ trials, comparing _Extended_ and _Finetune_ . 

These transients are particularly important for _Place_ , which begins with the box already in hand. Changes in robot motion at the skill boundary can therefore perturb the object state that initializes placement. To quantify this effect, Fig. 5 (Bottom) compares box state changes after the transition into _Place_ over 100 _Humanoid Hanoi_ trials. We observe that _Finetune_ exhibits larger accumulated box-height and pitch deviations exceeding the randomization used during training compared to _Extended_ . Appendix C.2 further shows that failed _Place_ attempts exhibit larger early box pose perturbations than successful attempts. These results provide evidence that controller-switching transients can disturb the _Place_ handoff state and contribute to long-horizon composition loss. 

These observations motivate a direct test of whether controller switching contributes to the composition gap. We repeat the same 100-instance Humanoid Hanoi evaluation while replacing each abrupt handoff between non-shared low-level controllers with a 10-step linear interpolation between the outgoing and incoming controller outputs. The trained policies, task instances, and evaluation conditions are otherwise unchanged. 

Transition smoothing improves complete-task success from 21% to 32% for _Finetune_ , from 19% to 32% for _Residual_ , and from 16% to 38% for _Joint_ . Because the trained policies and evaluation conditions are unchanged and only the low-level handoff is modified, these gains provide direct evidence that abrupt controller switching is one contributor to long-horizon composition loss. Transition smoothing does not fully eliminate the performance gap as _Extended_ remains at 47% complete-task success. Thus, abrupt controller switching explains an important part, but not all, of the degradation observed with the evaluated non-shared approaches. 

## **7 Hardware Experiments** 

On hardware, AprilTags detected by head-mounted cameras provide box pose estimates and robot localization, supplemented by IMU odometry when localization tags are not visible. The policies operate on these state estimates rather than raw images. Additional hardware and perception details are provided in Appendix E. 

8 


**Figure 6:** Three Humanoid Hanoi configurations (C1–C3) where **T1** , **T2** , and **T3** denote the tower locations defining the stack positions. 

The hardware experiments are intended to test real-world feasibility of _Humanoid Hanoi_ and to identify practical failure modes. We additionally show individual skill stability comparisons between _Base_ and _Extended_ on _Pickup_ and _Place_ . Individual-skill hardware comparisons are provided in Appendix D, and full-task hardware details and failure analyses are provided in Appendix E. 

For _Humanoid Hanoi_ , we evaluate three fixed workspace configurations (Fig. 6) with five consecutive trials each. Successful trials complete the full seven-move sequence in approximately five minutes. Across the three configurations, _Extended_ succeeds in 3/5, 2/5, and 1/5 trials, respectively, for an overall success rate of 6/15 (40%) and averages 4.2 completed moves per trial, including failed trials. By comparison, other baselines achieve 0/15 complete task success in the same setting, providing hardware evidence that WBC coverage expansion improves robustness in our system. 

## **8 Conclusion and Limitations** 

We introduced _Humanoid Hanoi_ , a long-horizon humanoid box rearrangement challenge problem that exposes failures from accumulated execution error and skill transitions. Using this challenge problem, we studied a hierarchical framework in which independently learned skills are executed through a shared, task-agnostic whole-body controller (WBC). We do not imply that all skill-specific low-level controllers are unsuitable for long-horizon humanoid composition. 

Rather, our experiments show that the evaluated skill-specific adaptations can incur additional composition loss when low-level controller transitions are not explicitly handled. A direct transitionsmoothing intervention improves all three non-shared methods without retraining, providing evidence that abrupt controller handoffs are one mechanism behind long-horizon degradation. However, transition smoothing alone does not close the full performance gap, whereas maintaining a shared WBC avoids low-level controller switching and better preserves isolated-skill reliability during long-horizon composition. Task-driven data aggregation ( _Extended_ ) further improves the shared WBC’s robustness by expanding its training coverage to behaviors induced by newly learned skills. 

Our framework has two main limitations. First, our analysis of non-shared WBCs identifies controller-switching transients as one important mechanism for long-horizon degradation, but we do not exhaustively characterize all possible non-shared controller designs. Second, our policies are state-based and do not address vision-based perception, occlusion, pose-estimation noise, partial observability, or fine-grained visual alignment. This design choice allows _Humanoid Hanoi_ to isolate the control and skill-composition challenges of long-horizon box rearrangement, but leaves perception-driven failures outside the scope of this study. Future work can use _Humanoid Hanoi_ as a testbed for vision-based policies and precision stacking, with box-pose metrics in Appendix C.3 providing one way to quantify such errors. Detailed failure-mode analyses are provided in Appendix C.4 and Appendix E.3. 

### **Acknowledgments** 

This work was supported by NSF Award 2321851 and DARPA Contract HR0011-24-9-0423. We gratefully acknowledge Intel for providing access to the vLab academic compute cluster, which supported the computational experiments conducted in this work. 

9 

## **References** 

- [1] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn. Humanplus: Humanoid shadowing and imitation from humans. In _8th Annual Conference on Robot Learning_ , 2024. URL `https: //openreview.net/forum?id=WnSl42M9Z4` . 

- [2] M. Seo, S. Han, K. Sim, S. H. Bang, C. Gonzalez, L. Sentis, and Y. Zhu. Deep imitation learning for humanoid loco-manipulation through human teleoperation. In _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ , pages 1–8. IEEE, 2023. 

- [3] C. Zhang, W. Xiao, T. He, and G. Shi. Wococo: Learning whole-body humanoid control with sequential contacts. In _8th Annual Conference on Robot Learning_ , 2024. URL `https: //openreview.net/forum?id=Czs2xH9114` . 

- [4] F. Liu, Z. Gu, Y. Cai, Z. Zhou, H. Jung, J. Jang, S. Zhao, S. Ha, Y. Chen, D. Xu, et al. Opt2skill: Imitating dynamically-feasible whole-body trajectories for versatile humanoid locomanipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [5] M. Murooka, T. Hoshi, K. Fukumitsu, S. Masuda, M. Hamze, T. Sasaki, M. Morisawa, and E. Yoshida. Tact: Humanoid whole-body contact manipulation through deep imitation learning with tactile modality. _IEEE Robotics and Automation Letters_ , 2025. 

- [6] S. Zhao, Y. Ze, Y. Wang, C. K. Liu, P. Abbeel, G. Shi, and R. Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 

- [7] T. He, Z. Wang, H. Xue, Q. Ben, Z. Luo, W. Xiao, Y. Yuan, X. Da, F. Casta˜neda, S. Sastry, C. Liu, G. Shi, L. Fan, and Y. Zhu. Viral: Visual sim-to-real at scale for humanoid locomanipulation. _arXiv preprint arXiv:2511.15200_ , 2025. 

- [8] K. Harada, S. Kajita, H. Saito, M. Morisawa, F. Kanehiro, K. Fujiwara, K. Kaneko, and H. Hirukawa. A humanoid robot carrying a heavy object. In _Proceedings of the 2005 IEEE International Conference on Robotics and Automation_ , pages 1712–1717. IEEE, 2005. 

- [9] H. Arisumi, J.-R. Chardonnet, A. Kheddar, and K. Yokoi. Dynamic lifting motion of humanoid robots. In _Proceedings 2007 IEEE International Conference on Robotics and Automation_ , pages 2661–2667. IEEE, 2007. 

- [10] A. Adu-Bredu, G. Gibson, and J. Grizzle. Exploring kinodynamic fabrics for reactive wholebody control of underactuated humanoid robots. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 10397–10404. IEEE, 2023. 

- [11] J. Li and Q. Nguyen. Multi-contact mpc for dynamic loco-manipulation on humanoid robots. In _2023 American Control Conference (ACC)_ , pages 1215–1220, 2023. doi: 10.23919/ACC55779.2023.10156397. 

- [12] J. Dao, H. Duan, and A. Fern. Sim-to-real learning for humanoid box loco-manipulation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 16930– 16936. IEEE, 2024. 

- [13] S. Ross, G. Gordon, and D. Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- [14] P. Dugar, A. Shrestha, F. Yu, B. van Marum, and A. Fern. Learning multi-modal whole-body control for real-world humanoid robots. In _Proceedings of the AAAI Symposium Series_ , pages 650–657, 2025. 

10 

- [15] C. Aeronautiques, A. Howe, C. Knoblock, I. D. McDermott, A. Ram, M. Veloso, D. Weld, D. W. Sri, A. Barrett, D. Christianson, et al. Pddl—the planning domain definition language. _Technical Report, Tech. Rep._ , 1998. 

- [16] T. Silver, K. Allen, J. Tenenbaum, and L. Kaelbling. Residual policy learning. _arXiv preprint arXiv:1812.06298_ , 2018. 

- [17] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [18] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 

- [19] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [20] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel. Sim-to-real transfer of robotic control with dynamics randomization. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 3803–3810. IEEE, 2018. 

- [21] P. Dugar, M. S. Gadde, J. Siekmann, Y. Godse, A. Shrestha, and A. Fern. No more marching: Learning humanoid locomotion for short-range se (2) targets. In _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , pages 1–8. IEEE, 2025. 

11 

## **A Shared Whole-Body Controller** 

### **A.1 WBC Interface** 

For whole-body control, we use the pre-trained Masked Humanoid Controller (MHC) [14] as the shared WBC used by all skills. The MHC is a learned policy trained to execute _partially specified motion directives_ , where a directive consists of a target motion sequence paired with a binary mask indicating which pose components are active constraints. The pose representation includes the root state (position, orientation, linear and angular velocity) and joint positions, enabling a unified control interface at varying levels of specificity. 

The masking mechanism is a lightweight command specification, not a skill-specific controller design. The mask simply selects which components of the existing directive space are provided by the active skill. For example, locomotion skills primarily activate root velocity and heading-related directives, while manipulation skills additionally activate torso or upper-body targets. Thus, adding a new skill does not require designing a new low-level controller or mask; it only requires choosing which existing directive components the skill controls and training the skill policy to output those targets. 

Given a masked directive, the WBC completes unspecified degrees of freedom according to the behavior learned during pretraining. This allows different skills to constrain different subsets of the body while using the same dynamically consistent whole-body behavior. At runtime, the WBC takes the robot’s proprioceptive state and the masked motion directive produced by the active skill and outputs joint-level PD position targets for all actuated joints ( _a ∈_ R<sup>20</sup> ), which are tracked by a fixed-gain PD controller. Using a single shared WBC keeps the low-level closed-loop control structure fixed across skills, so skill composition changes the high-level directive stream rather than switching low-level controllers. 

### **A.2 Rollout-Based Data Aggregation** 

We implement coverage expansion via a simple data aggregation procedure that expands the reference motion set used to define the WBC training distribution. The procedure is intentionally minimal: it changes only the WBC training distribution while preserving the original tracking objective, architecture, and shared runtime interface. Let _R_ denote a set of reference trajectories. The MHC training process induces a distribution over masked motion directives, which we denote by _D_ [ _R_ ]. Concretely, sampling from _D_ [ _R_ ] consists of (i) selecting a reference trajectory _r ∈R_ and a time index along _r_ , (ii) applying a binary mask to specify which pose components are active constraints, and (iii) sampling additional randomized command targets (e.g., locomotion and upper-body targets) according to the original MHC command distribution [14]. This defines the distribution of directives used to train the shared WBC. 

The pretrained MHC is trained under _D_ [ _R_ 0], where _R_ 0 contains reference trajectories from the AMASS dataset [17] and trajectory-optimization-derived motions. When a new high-level skill _πi_ is trained, we execute the hierarchical system with the current shared WBC (without domain randomization) and record the resulting closed-loop _directive sequences_ (targets and masks) issued to the WBC during successful rollouts. We treat these directive sequences as skill reference trajectories, forming a set _Si_ , which we then expand incrementally: 


so that the updated WBC training distribution becomes _D_ [ _Ri_ ]. 

Finally, we continue training the shared WBC on _D_ [ _Ri_ ] using the _same training objective_ as in its original pretraining [14], while applying domain randomization and disturbance injection. This yields a single updated shared WBC that improves robustness on the skill-induced behaviors without introducing additional parameters, skill-specific losses, or architectural changes. In this work, we aggregate nine successful reference trajectories, each for Pickup and Place skills (18 in total), collected from closed-loop executions spanning extreme box lateral positions and heights. We did not 

12 

|**Upper Body Tracking**|**Base**|**Extended**|
|---|---|---|
|Upperjoint MAE(median[IQR]) _↓_|0.1246[0.1763]|0.0805[0.1535]|
|Success Rate(%) _↑_|95|100|


**Table 2:** Upper-body tracking performance comparing the pretrained WBC ( _Base_ ) and the WBC trained with data aggregation ( _Extended_ ), on trajectories from the baseline training dataset. 

|Skill|Name<br>|Reward (_r_)<br><br>|Weight (_w_)<br>(up/ down)|Scale (_α_)<br>(up/ down)|
|---|---|---|---|---|
||hand contact position|_∥_**p**<sup>current</sup><br>hand<br>_−_**p**<sup>target</sup><br>elbow<sup>_∥_2</sup>|0.5|–|
||base pitch roll|(_|θ_base_|_+_|θ_base + 0_._15_|_)<br>|0.2|15|
||box rotation|_|θ_box_|_+_|ϕ_box_|_if contact(L_∧_R)<br>|0.1|10|
|Pickup|box acceleration|_∥_**˙v**box_∥_2<br>|0.05|0.02|
|Policy|table force|_F_table<br>mg <sup>if contact(L</sup><sup>_∧_R)</sup>|0.05|2.0|
||motor vel|mean(**v**motor _⊙W_weights)<br>|0.05|0.4|
||torque penalty|mean(_|_**_τ_**_|/τ_max)|0.05|0.05|
||foot velocity|_∥_**v**L_∥_2 +_∥_**v**R_∥_2|0.05|2.0|
||collisionpenalty|**1**[self-collision]<br>|-1.0|–|
||box target|_∥_**p**<sup>target</sup><br>box,xy <sup>_−_</sup><sup>**p**current</sup><br>box,xy<sup>_∥_2</sup>|0.15|15|
||box rotation|_|ψ_box _−ψ_target_|_|0.15|15|
|Place|hand contact bonus<br>|**C**hand,current _≡_**C**hand,require<br><br>|0.05|–|
|Policy|elbow position error|_|_**p**<sup>current</sup><br>elbow <sup>_−_</sup><sup>**p**target</sup><br>elbow<sup>_∥_2</sup>|0.2|5.0|
||base roll error|_|θ_base_|_<br>|0.1|15|
||base position error|**1**(_∥_**p**<sup>current</sup><br>base<br>_∥_2 _>_ 0_._12)|-0.2|–|
||soft table contact|**1**(_F_table _>_ 30)<br>|-0.1|–|
||hand traj tracking|_|_**p**<sup>current</sup><br>hand<br>_−_**p**<sup>target</sup><br>hand <sup>_|_</sup><br>|0.1 / 0.12|5.5|
||hand roll|_|θ_L,hand_|_+_|θ_R,hand_|_<br><br>|0.05 / 0.1|1.0 / 10|
||base height error|_∥z_<sup>current</sup><br>base<br>_−z_<sup>target</sup><br>base <sup>_∥_2</sup>|0.5 / 0.6|8 / 10|
||base pitch limit|**1**(_|ϕ_base_| >_ 0_._25)<br>|-0.1|–|
|Shared|CoP stability error|��**p**current<br>CoP<br>_−_**p**<sup>target</sup><br>foot<br>��<br>2|0.15|20|
|Rewards|stance width error|_||y_L,foot _−y_R,foot_| −_0_._33_|_|0.05|25|
||stand parallel|_|x_L,foot _−x_R,foot_|_<br>|0.05|10.0|
||foot orientation|_d_quat(**q**<sup>current</sup><br>foot<br>_,_**q**<sup>target</sup><br>foot <sup>)</sup><br><br>|0.05|20|
||action smoothness|1<br>_n_ <sup>_|_</sup><sup>**a**skill</sup><br>_t_<br>_−_**a**<sup>skill</sup><br>_t−_1<sup>_|_</sup><br><br>|0.1|6.0|
||low-level cmd|1<br>_n_ <sup>_|_</sup><sup>**a**llc</sup><br>_t _<sup>_−_</sup><sup>**a**llc</sup><br>_t−_1<sup>_|_</sup>|0.05|5.0|
||height cmdpenalty|**1**(_az <_ 0_._1 _∨az >_ 0_._9)|-0.1|–|


**Table 3:** Reward components grouped by skill. For values with two entries, the first value corresponds to the _Pickup_ policy and the second to the _Place_ policy. Terms without scale ( _α_ ) do not use the exponential kernel. 

tune the number of aggregated trajectories and did not perform a sensitivity sweep over this count. The GoTo skills already perform reliably with the pretrained WBC and are therefore not included in aggregation. 

Table 2 shows that using the rollout-based data aggregation method still preserves performance on upper body tracking and even improves over the pretrained WBC on this task, despite the augmented data not being specifically collected for it. 

## **B Skill Learning** 

This section describes the learning setup and training details for the learned _Pickup_ , _Place_ , and _GoTo/GoTo-with-box_ skills. 

**Policy Architecture and Training.** Each skill is a two-layer LSTM policy (64-D hidden state) running at 50 Hz that observes robot proprioception and skill-specific conditioning inputs (e.g., box pose/dimensions and target poses). The policy outputs a skill-dependent WBC motion directive, which the shared WBC converts (with proprioception) into PD position targets for the 20 actuated joints, tracked by a fixed-gain PD controller at 2 kHz. Skills are trained with reinforcement learning (RL) in MuJoCo [18] on Digit V3 using PPO [19] with dynamics randomization [20] (Table 5) for robustness using 160 cores on a dual Intel Xeon Platinum 8280 server on the Intel vLab Cluster. Unless otherwise specified, rewards are weighted sums of bounded exponential terms _w_ exp( _−αc_ ). 

**Pickup Skill.** We train a _Pickup_ policy to grasp boxes with varying pose (yaw), dimensions, and mass and return to stable standing while holding the box. The policy observes robot proprioception, the initial box pose in the robot root frame, and box dimensions, and outputs a masked WBC directive consisting of arm joint targets plus base pitch and height commands ( _a ∈_ R<sup>10</sup> ). Training uses a 

13 

|Skill|Name|Reward(_r_)<br><br>|Weight(_w_)|Scale(_α_)|
|---|---|---|---|---|
||constellation|�9<br>_i_=1 <sup>_∥_</sup><sup>**p**current</sup><br>_i_<br>_−_**p**<sup>target</sup><br>_i_<br>_∥_2<br><br>|1.0|0.5|
||base position error|_∥_**p**<sup>current</sup><br>base<br>_∥_2<br>|0.2|5.0|
||base yaw error|_|ψ_base_|_<br><br>|0.2|3.0|
||foot orientation|_d_quat(**q**<sup>current</sup><br>foot<br>_,_**q**<sup>target</sup><br>foot <sup>)</sup>|0.05|4.0|
|GoTo|stance width error|_||y_L,foot _−y_R,foot_| −_0_._33_|_|0.2|1.0|
|Policy|stand parallel|_|x_L,foot _−x_R,foot_|_<br><br><br>|0.2|1.0|
||action smoothness|1<br>_n_ <sup>_|_</sup><sup>**a**skill</sup><br>_t_<br>_−_**a**<sup>skill</sup><br>_t−_1<sup>_|_</sup>|0.1|8.0|
||torque penalty|mean(_|_**_τ_**_|/τ_max)|0.02|5.0|
||energy penalty|mean(_|_**_τ_** _⊙_**_vjoint_**_|_)|0.1|0.1|
||acceleration penalty|_|_**˙v**base_|_|0.05|0.01|
||commandpenalty|_∥_**at**_∥_2|-0.05|–|
||hand roll|_|θ_L,hand_|_+_|θ_R,hand_|_|0.05|10.0|
|w/ Box|contact|**1**(contact with box)<br>|0.05|–|
||box orientation|_d_quat(**q**<sup>current</sup><br>box<br>_,_**q**<sup>initial</sup><br>box <sup>)</sup><br><br><br>|0.1|5.0|
||box baseposition|_∥_**p**<sup>base</sup><br>box <sup>_−_</sup><sup>**p**base</sup><br>box,init<sup>_∥_2</sup>|0.05|5.0|


**Table 4:** Reward components for the _GoTo_ policy and additional rewards for the _GoTo-with-Box_ policy. Terms without scale ( _α_ ) do not use the exponential kernel. 


phased pickup curriculum ( _approach_ , _contact_ , _lift_ , _stand_ ) with a distance-based trajectory-tracking reward [12] on end-effector motion and base height. The _approach_ duration is adapted to the box height, 

_t_ approach = 100 _×_ (0 _._ 9 _−_ box height) + 30 _,_ 

while _contact_ and _lift_ run for 25 and 35 steps, and _stand_ is set by distance to the target standing height (0.8 m). We apply domain randomization over box properties, dynamics, and communication delay (Table 5). A support table is removed 45 steps after _contact_ to force full lifting, and episodes end on timeout, box drop, or invalid hand contact. In addition to tracking, the reward includes grasp and stability terms (hand-face contact bonus, foot-force balance, base pitch/stance regularization) and hardware-oriented smoothness terms (action-rate penalty, height bounds, and an extended terminal stand of 120 steps). 

**Place Skill.** We train a _Place_ policy to set a held box at an upright, yaw-only target pose while maintaining whole-body stability. The policy observes robot proprioception, current and target box poses in the robot root frame, and box dimensions, and outputs the same directive space as _Pickup_ ( _a ∈_ R<sup>10</sup> ). Since _Place_ is harder to train, we use a privileged critic with additional inputs (hand and base poses, hand/table contact forces, and box mass). 

To encourage consistent contacts and dynamically feasible placement, we generate reference motions by _reversing successful pickup rollouts_ . We collect 60k successful _Pickup_ trajectories (including 10k at challenging heights: box heights [70 _,_ 90] cm, sizes [15 _,_ 50] cm) and reverse recorded end-effector, base-height, contact, and box/table state sequences to obtain _Place_ references (mapping pickup _lift/stand_ to place _approach/place_ ). Episodes start from standing with a box in hand, and we randomize target distance ([40 _,_ 50] cm) and support height ([0 _,_ 75] cm) under the same domain randomization as _Pickup_ (Table 5), and inject box pitch disturbances ([ _−_ 30<sup>_◦_</sup> _,_ 5<sup>_◦_</sup> ]) while keeping the target upright. In addition to reference tracking, explicit base-pitch constraints were critical, which penalized excessive forward leaning during lowering. 

**GoTo Skills.** The _GoTo_ locomotion skill drives the robot to SE(2) targets ( _x, y,_ yaw) using the constellation reward for target-oriented locomotion [21]. We train two variants: _GoTo_ for unloaded 

14 

walking and _GoTo-with-Box_ for walking while carrying a box. Both are conditioned on a local-frame goal (∆ _x,_ ∆ _y,_ ∆yaw) that is periodically resampled during training. _GoTo-with-Box_ additionally observes the box dimensions and box pose relative to the base. Policies output WBC directives consisting of planar base velocity and heading commands ( _a ∈_ R<sup>3</sup> ), and _GoTo-with-Box_ includes upper-body targets to stabilize transport ( _a ∈_ R<sup>8</sup> ); base height and pitch are fixed (0.85 m, 0 rad). 

Episodes initialize at (0 _,_ 0) with randomized yaw and _GoTo-with-Box_ samples feasible robot/box initial states from a collected dataset. Both variants terminate on falls/instability (excess roll/pitch, low base height), self-collision, or excessive speed, and _GoTo-with-Box_ also terminates on loss of box contact. Training uses dynamics randomization and external perturbations (Table 5). Beyond the constellation objective, regularizers encourage stable foot pose, smooth actions, and low effort, with additional box-specific terms for transport. 

**Skill Reward Components.** Table 3 summarizes the reward components used to train the _Pickup_ and _Place_ policies, consisting of both skill-specific rewards and a set of shared rewards applied to both policies. Table 4 summarizes the reward components used to train the _GoTo_ policy variants. For _GoTo-with-Box_ tasks, the same _GoTo_ policy rewards are used, augmented with additional boxspecific reward terms listed under _w/ Box_ . 

We use **_p_** to denote Cartesian position vectors and **_q_** to denote quaternion orientations. **_τ_** and **_vjoint_** represent joint torques and joint velocities. ( _θ, ϕ, ψ_ ) correspond to roll, pitch, yaw angles, (∆ _x,_ ∆ _y,_ ∆ _yaw_ ) denote the relative pose difference between the target and the robot, expressed in the robot’s local frame and _dquat_ ( _·_ ) is the quaternion distance. Contact-related terms use binary contact indicators _C ∈{_ 0 _,_ 1 _}_ where equality constraints denote required contact conditions. **1** [ _·_ ] is the indicator function. 

## **C Humanoid Hanoi Simulation Evaluation** 

### **C.1 Simulation Setup** 

Each episode is initialized by sampling a workspace radius uniformly from [1 _._ 5 _,_ 2 _._ 5] m. Three tower locations are placed on the circumference of the circle and oriented outward from the circle center, with a minimum pairwise separation of 0.9 m. Depending on the sampled radius, the tower locations may be nearly collinear or span a wide range of orientations, resulting in diverse geometric configurations and approach directions for locomotion. 

Box properties are randomized at the start of each episode. Box sizes are sampled from three categories: _small_ [0 _._ 26 _,_ 0 _._ 29] m, _medium_ [0 _._ 29 _,_ 0 _._ 32] m, and _large_ [0 _._ 32 _,_ 0 _._ 35] m. The sliding friction coefficient is uniformly sampled from [0 _._ 5 _,_ 0 _._ 7] to capture variability in real-world cardboard box interactions. The box mass is randomized within [0 _._ 5 _,_ 3 _._ 0] kg, including a 0.3 kg point mass attached at the center of the bottom to simulate boxes containing internal items. Standard dynamics randomization (DR) from Table 5 is applied to the robot model in the with-DR setting shown in Fig. 4, while the without-DR setting uses nominal robot parameters. 

### **C.2 Transition Statistics for Successful and Failed Place** 

To examine whether transition perturbations are associated with downstream failures, we analyze _Place_ transitions from 400 Humanoid Hanoi trials using the _Finetune_ baseline. Fig. 7 separates successful and failed _Place_ attempts. Failed placements exhibit larger cumulative vertical and pitch displacements after the transition, indicating more disturbed handoff states or stronger immediate perturbations when switching into _Place_ . While this analysis is correlational, it provides additional evidence that controller-switching transients are associated with long-horizon composition failures. 

15 


**Figure 7:** Box state changes after the transition into _Place_ over 400 _Humanoid Hanoi_ trials for _Finetune_ , comparing successful and failed placements. 

|**Metric**|**Base**|**Finetune**|**Residual**|**Extended**|
|---|---|---|---|---|
||**No Dynam**|**ics Randomizati**|**on(**_µ ± σ_**)**||
|_xerr_ (cm)_↓_|4_._71_±_3_._46<br>|5_._79_±_4_._10<br>|5_._35_±_3_._73<br>|5_._47_±_3_._60<br>|
|_yerr_ (cm)_↓_<br>|5_._26_±_3_._58|5_._75_±_4_._27|5_._24_±_3_._71|5_._60_±_3_._69|
|_θerr_ (<sup>_◦_</sup>) _↓_|2_._89_±_2_._74|2_._65_±_2_._34|2_._66_±_2_._57|3_._59_±_3_._96|
||**Dynami**|**cs Randomization**|**(**_µ ± σ_**)**||
|_xerr_ (cm)_↓_|5_._36_±_4_._12|5_._72_±_3_._95|5_._87_±_5_._28|5_._42_±_3_._82|
|_yerr_ (cm)_↓_<br>|5_._23_±_4_._27|5_._33_±_3_._57|5_._87_±_5_._13|5_._99_±_3_._93|
|_θerr_ (<sup>_◦_</sup>) _↓_|2_._89_±_3_._08|2_._59_±_2_._32|3_._43_±_6_._18|3_._30_±_6_._64|


**Table 6:** Humanoid Hanoi placement accuracy for successful trials. Final box position and orientation errors for the _Place_ skill, reported as mean _µ_ and standard deviation _σ_ . 

### **C.3 Box Pose Error** 

Table 6 reports final box-pose errors over each method’s successful trials. Because the set of successful episodes differs across methods, these statistics are subject to a selection effect: methods that succeed on more difficult configurations may be evaluated on a broader subset of episodes. 

To provide an apples-to-apples comparison, Table 7 additionally evaluates only the intersection of episodes successfully completed by all methods. On this common subset, no method consistently achieves lower error across _x_ , _y_ , and yaw. This supports our interpretation that _Extended_ ’s primary benefit is improved long-horizon robustness rather than improved placement precision on nominal successful episodes. 

### **C.4 Humanoid Hanoi Analysis of Failure Modes** 

We analyze failures on Humanoid Hanoi to identify the dominant limitations of the current system and to motivate future improvements. Fig. 8 shows that most failures occur during _Place_ , which combines precise end-effector pose control with tight balance margins and stack stability constraints. 

**Placement-Induced Failures.** A common failure pattern is unintended box pitch rotation during placement. Small control errors and contact transients can introduce orientation misalignment, leading to unstable support and eventual stack collapse. We also observe failures during post-placement stabilization: after releasing the box, the robot may take forward recovery steps that inadvertently contact and disturb the stack. 

**Upstream Errors Accumulate into Placement.** Several failure modes originate before _Place_ but become critical at placement time. First, off-centered grasps during _Pickup_ introduce residual box pose errors in the gripper, which then propagate into placement errors and accumulate over multiple moves. Second, residual localization error after _GoTo-with-box_ reduces placement margin. In our system, the robot transitions to _Place_ once it is within 5 cm of the target SE(2) pose; remaining base pose errors at this point directly translate into placement offsets and can destabilize the stack in later stages. 

**Object-Unaware Locomotion.** Finally, failures also occur during transitions from _Place_ back to _GoTo_ . Because _GoTo_ is not object-aware, backward walking combined with in-place rotation can collide with the stack, displacing boxes and causing task failure. 

16 


**Figure 8:** Failure counts across skills in Humanoid Hanoi for each baseline, shown with and without dynamics randomization. 

## **D Per-skill Hardware Evaluation** 

We qualitatively compare the _Base_ and _Extended_ WBCs on consecutive low-height _Pickup_ and _Place_ executions on hardware. As shown in Fig. 9, the _Base_ WBC exhibits unstable whole-body behavior, including large posture changes, object disturbance, and forward stepping during the sequence. In contrast, the _Extended_ WBC executes the same sequence with more stable body motion and controlled box handling. This supports the simulation results showing that coverage expansion improves WBC robustness in low-margin manipulation regimes. 

## **E Humanoid Hanoi Hardware Evaluation** 

### **E.1 Hardware Setup** 

All experiments are conducted using the Digit V3 humanoid robot. The robot is equipped with two Intel RealSense D455 RGB-D cameras mounted on the top of the head. Both cameras face downward, with one pitched at 67<sup>_◦_</sup> and the other at 20<sup>_◦_</sup> relative to the head frame, providing complementary fields of view for detecting AprilTags on boxes and in the environment. 

Perception and control computations are performed onboard using an Intel NUC with a 10thgeneration CPU. Both cameras are directly connected to the NUC. The NUC communicates with the Digit V3 robot over Ethernet using UDP and transmits joint-level proportional–derivative (PD) control commands. 

### **E.2 Humanoid Hanoi Hardware Configuration** 

In the hardware evaluation, each box is equipped with a fiducial marker (AprilTag) that is used to estimate the pose of each box relative to the robot base for pick-and-place execution. In addition, three AprilTags are mounted behind each target tower location (T1–T3) in the hardware environment and are used for global localization of the robot. 

When one or more of the AprilTags are detected by the onboard camera, the robot uses the AprilTags to estimate its current position and orientation in the world frame. The world coordinate frame is defined such that the origin corresponds to the centroid of the three tower locations, and the world _xy_ plane is the ground plane. 

17 


**Figure 9:** Qualitative hardware comparison of consecutive low-height _Pickup_ and _Place_ executions with the _Base_ WBC and _Extended_ WBC. Frames 1–4 show _Pickup_ ; frames 5–8 show _Place_ . 

When AprilTags are not visible, the robot relies on onboard inertial sensing. A built-in inertial measurement unit (IMU) is used to estimate the robot’s pose. At the beginning of each Humanoid Hanoi trial, the IMU odometry is initialized with the world origin set to (0, 0) and a heading angle of 0<sup>_◦_</sup> . We reset the IMU odometry after completing each box pickup to reduce accumulated drift and improve localization accuracy. 

At the start of each trial, three boxes are stacked directly in front of the AprilTags associated with the initial tower (T1). The robot is required to transport the three boxes to the target location while following the Tower of Hanoi rules (i.e., only one box may be moved at a time, and larger boxes may not be placed on top of smaller ones). 

We evaluate three Humanoid Hanoi configurations that differ in box size and target tower distance. The box dimensions for the _small_ , _medium_ , and _large_ configurations are [33.65, 33.65, 34.92] cm, [35.56, 35.56, 34.92] cm, and [37.78, 37.78, 34.92] cm, respectively. The corresponding radial distances from the robot’s initial standing position to the target towers are 150 cm, 165 cm, and 180 cm. A trial is considered a failure if the robot drops a box at any point during execution, causes a tower to collapse, or violates the Tower of Hanoi constraints. We conduct five consecutive trials for each configuration to obtain the final results. 

18 


**Figure 10:** Simplified two-tower hardware setup used to reduce yaw-localization demands. The robot successfully completes five consecutive three-box stacking trials in this setting, suggesting that yaw-localization is a significant bottleneck in _Humanoid Hanoi_ . 

### **E.3 Hardware Failure Modes** 

Across the trials, failures fell into three categories: (i) perception/state estimation, (ii) navigation/alignment at skill handoffs, and (iii) physical interaction during manipulation/placement. The most common were AprilTag perception failures during _Pickup_ (2 trials), box flipping during _Place_ from unintended contact (2), and yaw misalignment at handoff (2). Remaining failures included a large lateral localization error causing an unsuccessful grasp (1), an IMU fault that degraded walking and led to tag loss (1), and a box being kicked during placement/stand-up (1). Overall, these results indicate that hardware robustness is currently limited by tag robustness, base-pose accuracy entering _Place_ , and clearance-aware body motion during placement and recovery. 

### **E.4 Simplified Hardware Stacking Evaluation** 

The full _Humanoid Hanoi_ hardware evaluation includes several sources of failure beyond wholebody control, including AprilTag loss, yaw localization, grasp alignment, and physical interaction during placement. These factors make hardware results best interpreted as end-to-end feasibility, while controlled attribution is provided primarily by the simulation ablations. In particular, yawlocalization errors were a hardware-specific failure mode: they were not observed in simulation because the simulated environment uses ground-truth robot and object state, whereas the hardware system relies on AprilTag localization and onboard odometry. 

To reduce yaw-localization errors, we additionally evaluate a simplified two-tower hardware setup shown in Fig. 10. The two towers are arranged approximately collinearly, so the robot mainly transports boxes along a single axis and does not require the large yaw reorientation used in the full three-tower _Humanoid Hanoi_ setting. 

The robot successfully completes five consecutive three-box stacking trials in this simplified setup. The next trial was terminated by a robot reset due to motor heating rather than a manipulation or placement failure. These results are consistent with yaw-localization errors being an important contributor to hardware failures and demonstrate repeated stacking in a setting with reduced yawreorientation demands. 

19 

