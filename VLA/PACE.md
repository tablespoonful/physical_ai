---
title: "PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking"
date: "2026-05-30"
authors: "Junnan Nie; Jiayi Li; Chenghao Liu; Junyi Lao; Jiachen Zhang; Tianle Zhang"
url: https://arxiv.org/abs/2606.00537
pdf: https://arxiv.org/pdf/2606.00537
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.00537)** / [論文ページ](https://arxiv.org/abs/2606.00537)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking 

**Junnan Nie**<sup>1,2</sup> **, Jiayi Li**<sup>2</sup> **, Chenghao Liu**<sup>1</sup> **, Junyi Lao**<sup>1</sup> **, Jiachen Zhang**<sup>1</sup> **, Tianle Zhang**<sup>2</sup> **, Liang Lin**<sup>2</sup> **, Songfang Huang**<sup>1,†</sup> 

1Peking University. 

2JD Explore Academy. 

## **A** bstract 

Recent vision–language–action and diffusion-based robot policies often use action chunking, where each policy query predicts a sequence of future actions and the robot executes an open-loop prefix before re-querying. While this interface improves local motion continuity, deployment still requires choosing the _execution horizon_ : how much of each predicted chunk should be executed before acquiring a new observation. However, our experiments show that success is strongly task-dependent and non-monotonic with respect to the execution horizon, making a single constant horizon an unreliable deployment rule. We propose PACE (Phase-Aware Chunk Execution), a training-free test-time execution method that selects the execution horizon online from the predicted chunk itself. PACE exploits the phase-dependent kinematic structure of manipulation trajectories by identifying low-speed transition points in the predicted speed profile and using them as candidate replanning boundaries. Because PACE uses only the predicted action chunk, it is plug-and-play and requires no retraining or access to policy internals. We validate PACE through large-scale evaluations in both simulation and real-robot settings. On 50 RoboTwin2.0 tasks, PACE raises the average success rate from 57.8% to 64.2%. In real-robot experiments on bimanual ALOHA and single-arm Franka platforms, PACE improves the average task score from 60.7 to 77.7 and the average success rate from 50.7% to 70.4%. Ablations and rollout-level analyses show that PACE adapts execution horizons across manipulation phases, shortening near transitions while preserving longer execution during coherent motion. 


Figure 1: **Overview of PACE.** Fixed horizons can be unreliable because success varies with _H_ across tasks. PACE selects the executed prefix online from each predicted chunk, improving performance in simulation and real-robot experiments while adapting the horizon in a rollout. 

†Corresponding author. _Emails:_ jnnie25@stu.pku.edu.cn, 23121254@bjtu.edu.cn, chliu@stu.pku.edu.cn, jylao25@stu.pku.edu.cn, z89498323286@gmail.com, tianlezhang14@jd.com, linlng@mail.sysu.edu.cn, hsf@pku.edu.cn. 

## 1 Introduction 

Recent progress in vision-language-action models and diffusionbased robot policies has largely come from training-side gains. Larger backbones, broader demonstration data, and stronger multi-modal pretraining have all improved predictive performance [3, 8, 4, 18, 22, 12, 21, 14, 1, 28, 7]. At deployment, however, performance depends not only on how accurately a policy predicts, but also on how those predictions are executed. To improve local motion continuity, these policies often adopt action chunking [29, 7], where each query predicts a short sequence of future actions rather than a single-step command. 

Yet an action chunk only specifies what the policy predicts, not how much of that prediction the robot should execute. Its length fixes the prediction horizon, but a separate choice must still be made about how many actions to execute before acquiring a new observation and querying the policy again. We refer to this executed prefix length as the _execution horizon_ . Unlike the prediction horizon, the execution horizon is neither learned nor prescribed by the policy [7, 29]. It is an inference-time choice that trades off feedback frequency against within-chunk motion continuity. As such, the execution horizon is not a mere implementation detail, but a central variable for reliable deployment of action-chunking robot policies. 

In practice, the execution horizon is typically fixed to a constant _H_ throughout an episode [7, 29]. At each replanning step, the robot executes the first _H_ actions of the predicted chunk before querying the policy again, tying all chunks to the same replanning interval regardless of the motion they predict. A smaller _H_ incorporates new observations more often but can interrupt a coherent local motion, while a larger _H_ follows the predicted chunk longer but delays reactive correction. Without a principled selection criterion, _H_ is usually chosen empirically. 

The left panel of Fig. 1 shows that such an empirical choice is unreliable. Sweeping _H_ from 1 to 50 on three RoboTwin2.0 tasks, we observe that the success rate is strongly non-monotonic in _H_ and that the preferred horizon is highly task-dependent. On _Click bell_ , for instance, the success rate peaks near _H_ ≈ 6, drops by nearly 40 points around _H_ ≈ 25, and rebounds to a second peak near _H_ ≈ 35. On such a landscape, any fixed horizon risks falling into a region of sharply degraded performance on some task. An offline sweep does not resolve this problem either, since the best horizon identified on one task does not transfer to new tasks or to real-robot deployment. These findings indicate that the execution horizon must be decided at deployment time rather than fixed in advance. 

We propose PACE (Phase-Aware Chunk Execution), a testtime execution method that selects _hi_ online by analyzing the speed profile of the predicted action chunk. The method is grounded in the phased kinematic structure of manipulation trajectories: rather than being kinematically uniform, a manipulation trajectory consists of locally coherent segments with distinct motion characteristics, and transitions are typically marked by deceleration, e.g., during contact preparation or sub-stage hand-off. Such boundaries manifest as low-speed valleys in the speed profile, a structure preserved by policies trained via imitation learning. PACE treats these valleys as natural replanning points: it executes the chunk up to the earliest accepted valley, 

preserving one coherent motion segment, and re-queries the policy before the next begins. PACE introduces no learned component, requires no internal access to the policy, and requires no modification or retraining of the underlying model. 

On the RoboTwin2.0 benchmark [6] of 50 bimanual manipulation tasks, PACE improves the average success rate from 57.8% to 64.2% over the best fixed-horizon baseline. In realrobot experiments, it improves the average task score from 60.7 to 77.7 and the average success rate from 50.7% to 70.4%. We further provide ablations on phase-profile construction, sensitivity analyses on valley selection and the training prediction horizon, and fixed-horizon sweeps on representative tasks. A rollout-level analysis of successful and failure cases reveals the working mechanism of PACE and the failure modes it resolves or leaves unresolved. 

Our contributions are summarized as follows: 

- We identify the execution horizon as a critical yet overlooked test-time variable, and show that its effect on success is taskdependent and non-monotonic, indicating that no single fixed horizon provides a reliable default across tasks. 

- We propose _PACE_ , a plug-and-play test-time execution method that selects the executed prefix online from the phasedependent kinematic structure of predicted action chunks. It requires no auxiliary input, no learned module, and no modification or retraining of the underlying policy. 

- We validate PACE on 50 RoboTwin2.0 simulation tasks and in real-robot experiments, where it consistently surpasses representative fixed-horizon baselines. Ablations, sensitivity analyses, and rollout-level diagnostics further isolate its design choices and expose the mechanism behind the gains. 

## 2 Related Work 

**Robot policies with action chunking.** Action chunking, where a policy predicts a sequence of future actions rather than a single next action, has become a common interface for robot policy learning. It was popularized by ACT for fine-grained bimanual imitation learning and by Diffusion Policy for actionsequence generation in a receding-horizon loop [29, 7]. Since then, chunked action prediction has been adopted in mobile and bimanual manipulation, 3D diffusion policies, generalist robot policies, vision–language–action models, action-tokenized models, and world-action models [9, 27, 17, 21, 1, 19, 13, 20, 10, 5, 26]. These works mainly study how to generate better action chunks through architecture design, representation learning, tokenization, data scaling, or pretraining. PACE studies a complementary question at deployment time: once a chunk has already been predicted, how much of it should be executed before the policy is queried again? 

**Test-time execution of action chunks.** The execution of an action chunk is usually determined by a separate test-time rule. Many systems use a fixed rule: ACT combines overlapping predictions through temporal ensembling, while Diffusion Policy executes a fixed action horizon before replanning [29, 7]. Recent inference-time methods further address practical execution issues such as latency-induced discontinuities or stability during 

2 


Figure 2: **PACE framework.** PACE selects an execution horizon from low-speed valleys in the predicted chunk’s smoothed speed profile. The robot executes the selected prefix, discards the suffix, and then queries the policy again. 

chunk execution [2, 23]. Another line modifies training objectives or model design so that policies can reason over multiple horizons [11]. Closest to our setting, AutoHorizon selects execution horizons online, but it relies on action self-attention inside flow-based VLAs [24]. In contrast, PACE treats horizon selection as a policy-agnostic execution problem. It uses only the predicted action chunk, identifies candidate replanning boundaries from low-speed valleys in the chunk’s kinematic profile, and requires no attention maps, confidence scores, denoising states, auxiliary heads, retraining, or inference-engine changes. 

## 3 Method 

### _3.1 Problem Formulation_ 

We consider a manipulation policy with action chunking. At the _i_ -th policy query, the policy receives the observation _o_ τ _i_ and the language instruction ℓ, and outputs 


where _L_ is the prediction horizon and _da_ is the action dimension. Let _hi_ ∈{1, . . . , _L_ } denote the execution horizon, i.e., the number of predicted actions executed before the next policy query. After executing the prefix ( _ai_ ,1, . . . , _ai_ , _hi_ ), the next query occurs at τ _i_ +1 = τ _i_ + _hi_ . 

A fixed-horizon rule sets _h_<sup>fixed</sup> _i_ = _H_ for all _i_ , independent of the predicted chunk **A** _i_ . Such a rule is agnostic to chunk content: it commits to the same execution length whether **A** _i_ describes a smooth transit or straddles a contact event. As discussed in Sec. 1, this content blindness is the source of the task dependent horizon sensitivity that motivates our work. We therefore introduce **PACE** , which replaces this constant rule with a chunk-conditioned selection rule, 


The function _g_ is a deterministic, training-free procedure with a small set of fixed selection parameters, described at a high level in Sec. 3.2 and Sec. 3.3. It introduces no learnable parameters and is applied at test time without modifying the trained policy πθ; in particular, _L_ is kept as the policy’s training prediction horizon (examined in Sec. 4.3). 

### _3.2 Kinematic Profile Extraction_ 

Manipulation trajectories are not kinematically uniform. Prior work has modeled manipulation tasks as sequences of phases or motion primitives [16, 15]. Such trajectories typically consist of locally coherent motion segments separated by slower transition regions, such as contact preparation, grasping, release, or stabilization. Because these policies are trained to imitate expert action sequences, their predicted chunks can retain this phase structure, making the predicted motion profile a useful signal for deciding where to replan. 

For each policy query _i_ , let **A** _i_ = ( _ai_ ,1, . . . , _ai_ , _L_ ) denote the predicted action chunk. For each executed arm group _b_ ∈B, PACE maps the corresponding arm-motion component of **A** _i_ to a one-dimensional speed profile, 


where ψ _b_ (·) denotes the arm-specific kinematic profiling operator. The profile is then smoothed by an operator S, 


to suppress short-range fluctuations that would otherwise create spurious local minima. The resulting low-speed regions in **v** ˜<sup>_b_</sup> _i_ serve as candidate phase boundaries for selecting the execution horizon. 

### _3.3 Phase-Aware Execution Horizon Selection_ 

Given the smoothed kinematic profile **v** ˜<sup>_b_</sup> _i_<sup>foreachexecuted</sup> arm group _b_ ∈B, PACE selects an execution horizon _hi_ ∈ {1, . . . , _H_ max} for the current predicted chunk. The selection is based on the observation that manipulation phase transitions are often expressed as localized deceleration events in the predicted motion profile. Examples include contact preparation, alignment, grasping, release, and stabilization. Such events appear as low-speed valleys separating adjacent motion segments. 

For each arm group, PACE first extracts a set of candidate phase boundaries 


from the low-speed valleys of **v** ˜<sup>_b_</sup> _i_<sup>, subject to a minimum tempo-</sup> ral separation constraint. Each candidate _r_ ∈V _i_<sup>_b_is assigned a</sup> prominence score Φ<sup>_b_</sup> _i_<sup>(</sup><sup>_r_), which measures whether the valley cor-</sup> responds to a pronounced deceleration relative to its surrounding motion. This criterion prevents small fluctuations on already slow segments from triggering unnecessary replanning. 

The accepted replanning candidates are pooled across all executed arms: 


where δT is a task-level acceptance threshold calibrated from training demonstrations. PACE then chooses the earliest accepted boundary, or falls back to a longer execution horizon when no valid boundary is found: 


Here _H_ max ≤ _L_ denotes the maximum allowed execution horizon. 

3 

Table 1: **Comparison with fixed-horizon execution.** Success rates (%) on six representative RoboTwin2.0 tasks and the 50-task average. Fixed baselines use a constant execution horizon _H_ ; PACE selects horizons online from each predicted chunk. Values after the slash are absolute gains over the best fixed baseline in the same column. Each task-method pair is evaluated with 3 seeds and 3 independent 100-episode batches per seed, giving 900 episodes per task and 45,000 episodes per method for the 50-task average. 

|Model|Horizon|Short-H|orizon|Medium|-Horizon|Long-|Horizon|Succ|
|---|---|---|---|---|---|---|---|---|
|||Pick Bottles|Grab Roller|Place A2B|Dump Bin|Put Bottles|Stack Bowls|.|
||_H_ =5|13.3|89.9|20.0|58.7|0.3|88.7|48.8|
||_H_ =25|45.3|96.2|47.8|85.1|79.3|88.4|57.8|
|π0.5|_H_ =50|38.7|96.2|36.8|84.3|70.8|85.1|53.4|
||PACE|**48.2**/+2.9|**98.6**/+2.3|**54.6**/+6.8|**93.0**/+7.9|**88.9**/+9.6|**95.6**/+6.9|**64.2**/+6.4|


The threshold δT is calibrated once per task using training demonstrations only. This calibration does not use evaluation rollouts, success labels, or fixed-horizon sweeps. In singlearm settings, B contains only the executed arm. In multi-arm settings, the earliest accepted boundary across arms is used so that replanning occurs before any arm crosses a predicted phase boundary under stale observations. 

## 4 Simulation Experiments 

**Simulation setting.** We evaluate PACE on RoboTwin2.0 [6], a benchmark of 50 bimanual manipulation tasks with diverse temporal demands. For each task, we train one π0.5 checkpoint [10] under the standard RoboTwin2.0 protocol, using a prediction horizon of _L_ = 50. All compared methods use the same task checkpoint and receive the same observations and language instructions. They differ only in how much of each predicted action chunk is executed before replanning. This design isolates the effect of the execution scheme from differences in policy training, model capacity, or demonstration data. 

**Execution schemes.** We compare PACE with fixed-horizon execution, where the robot executes the first _H_ actions of each predicted chunk before querying the policy again. The fixed baselines use _H_ ∈{5, 25, 50}, corresponding to short, intermediate, and full-chunk execution under the prediction horizon _L_ = 50. These baselines are deployed as global constants and are not tuned separately for each task. PACE uses the same predicted chunks, but selects the executed prefix online from the predicted motion structure. Its threshold is calibrated from training demonstrations only; evaluation rollouts, success labels, and fixed-horizon sweeps are not used for calibration. 

**Evaluation protocol.** Unless otherwise noted, we adopt a full evaluation protocol. For each task and method, we evaluate three seeds, and for each seed we run three independent batches of 100 episodes. Thus, each task-method pair is evaluated over 3 × 3 × 100 = 900 episodes. Success is measured by the RoboTwin2.0 task success predicate. We report tasklevel success rates averaged over the nine evaluation batches, and compute the 50-task average as the equal-weight mean over tasks. The 50-task average is the primary metric, while task-level tables highlight six representative tasks balanced across short-, medium-, and long-duration groups. Full task-level results and evaluation details are provided in Appendix B. 

**Overview of experiments.** We organize the simulation evaluation around four questions. Sec. 4.1 asks whether PACE improves over fixed-horizon execution as a deployable default, without task-specific horizon tuning. Sec. 4.2 examines how PACE adapts its execution horizons within a rollout. Sec. 4.3 studies the design choices behind PACE, including the phase profile, the training prediction horizon, and the sensitivity to selection hyperparameters. Finally, Sec. 4.4 uses fixed-horizon sweeps as a diagnostic tool to separate task-specific horizon preference from the benefit of adaptive replanning timing. 

### _4.1 Simulation Results_ 

We first compare PACE with fixed-horizon execution as deployable test-time rules. The fixed baselines use _H_ ∈{5, 25, 50}, representing short, intermediate, and full-chunk execution under the prediction horizon _L_ = 50. These baselines are global schedules: the same _H_ is used throughout all rollouts of a task and is not tuned separately for each task. PACE uses the same policy checkpoint and predicted chunks, but chooses the executed prefix online at each policy query. 

Table 1 shows that PACE achieves the best 50-task average success rate. Among the fixed-horizon baselines, _H_ = 25 is the strongest global choice, reaching 57.8%. PACE improves this average to 64.2%, a gain of 6.4 points, without task-specific horizon sweeps or changes to the underlying policy. Because all methods share the same trained checkpoint within each task, the improvement is attributable to the test-time execution rule. 

PACE also outperforms the strongest fixed-horizon baseline on all six displayed tasks, covering short-, medium-, and longduration task groups. This supports the central motivation of PACE: rather than committing to one fixed feedback interval, the execution horizon should be selected according to the motion structure predicted at test time. Per-task results for all 50 tasks are provided in Appendix B. 

### _4.2 Visualizing Adaptive Execution Horizons_ 

We conduct a rollout-level visualization analysis on a representative `place_shoe` episode, as shown in Fig. 3. This analysis exposes two execution-level behaviors of PACE: the selected horizon changes across manipulation phases, and the unexecuted suffix of each predicted chunk is discarded before replanning from a new observation. Figure 3 shows that PACE does not follow a fixed replanning cadence. The selected horizons vary 

4 


Figure 3: **Rollout-level behavior of PACE.** The rollout is from `place_shoe` . Top: head and front camera observations at the six replanning timesteps. Middle: selected execution horizons between consecutive queries. Bottom: predicted action chunks along the rollout timeline, where solid segments are executed prefixes and dashed segments are discarded suffixes. Vertical dashed lines mark replanning boundaries. 

substantially within the same rollout (e.g., 32, 14, 37, 25, and 19 steps), and the variation is structured: longer horizons are used when the predicted chunk describes a coherent motion segment, while shorter horizons appear near low-speed transitions. A single fixed horizon cannot express this within-episode variation. 

The discarded suffixes further show how PACE limits openloop commitment to a single prediction. At each query, the policy predicts a full chunk, but PACE executes only the prefix up to the selected boundary and discards the remaining suffix. When the next observation is acquired, the newly predicted chunk can differ from the discarded suffix over the overlapping interval, as visible around _t_ =83. Thus, PACE avoids carrying stale predictions too far forward while still allowing long, continuous execution when the motion remains coherent. This behavior helps explain the performance gains over fixed-horizon execution in Sec. 4.1. 

### _4.3 Ablation Analysis_ 

We structure the ablation study around two design choices and one robustness question. First, we ablate the phase-profile con- 

struction by comparing joint-space and Cartesian speed profiles, with and without smoothing. This tests whether PACE depends on a particular motion representation or on noisy raw velocity signals. Second, we study the training prediction horizon _H_ train, which sets the supervised chunk length during policy training. This asks whether predicting farther into the future improves the quality of the prefix executed at test time, while _H_ eval is held fixed. Finally, we evaluate sensitivity to the selection hyperparameters that control candidate-boundary acceptance, testing whether PACE relies on a narrowly tuned setting. 

The phase-profile and hyperparameter-sensitivity analyses use all 50 RoboTwin2.0 tasks under the full evaluation protocol. The training-horizon ablation requires retraining policies for different _H_ train, so it is reported on the six representative tasks. Additional protocol details and expanded training-horizon results are provided in Appendix C. 

**Phase-profile construction.** We compare joint-space and Cartesian speed profiles, with and without smoothing, to test which signal is most suitable for identifying phase boundaries from predicted chunks. This ablation examines two aspects of the phase profile: the motion representation used to measure 

5 

Table 2: **Ablation studies. Left:** fixed-horizon reference and phase-profile ablation on all 50 RoboTwin2.0 tasks. The Baseline row uses fixed-horizon execution with _H_ = 25. ∆ Succ. denotes the absolute success-rate gain over this baseline. Avg. Horizon is the fixed execution horizon for the baseline and, for PACE variants, the mean executed horizon _hi_ selected by PACE over all policy queries in the evaluation rollouts. **Right:** training-horizon ablation on six representative tasks; each row fixes _H_ eval and varies _H_ train. Gain@50 is the gain of _H_ train=50 over the shortest feasible setting. Success rates are in %, and gains are in percentage points.<sup>†</sup> marks the default. The phase-profile ablation uses the full 50-task protocol with 900 episodes per task and configuration. The training-horizon ablation is evaluated on six representative tasks with seed 0 and three 100-episode batches per task-setting pair. 

|Configuration|Succ.|∆Succ.|Avg. Horizon|
|---|---|---|---|
|Baseline (_H_ =25)|57.8|–|25.0|
|Cartesian, raw|62.2|+4.4|11.3|
|Cartesian, smoothed|**64.5**|+**6.7**|19.5|
|Joint, raw|60.4|+2.6|16.7|
|Joint, smoothed<sup>†</sup>|64.2|+6.4|24.3|


|_H_eval\_H_train|10|20|30|40|50|Gain@50|
|---|---|---|---|---|---|---|
|10|57.2|68.7|69.9|74.6|77.9|+**20.7**|
|20|–|68.7|72.6|73.8|75.3|+**6.6**|
|30|–|–|70.2|71.4|73.8|+**3.6**|
|40|–|–|–|70.1|73.4|+**3.3**|
|50|–|–|–|–|71.4|+**0.0**|


speed, and whether local fluctuations should be smoothed before valley detection. Raw profiles can contain short-range oscillations that create spurious local valleys, while smoothing is expected to preserve the dominant phase structure and suppress noisy replanning triggers. 

Table 2 left shows that smoothing improves success in both spaces and increases the selected execution horizon. This suggests that smoothing removes noisy valleys that would otherwise cause overly frequent replanning. After smoothing, Cartesian and joint-space profiles perform comparably, indicating that PACE captures a phase structure shared across kinematic representations rather than relying on a specific motion space. We adopt the smoothed joint-space profile by default because it is within 0.3 points of the best variant, matches the policy action space, and avoids running forward kinematics at every replanning query. 

**Training prediction horizon.** We next ask whether the prediction horizon used during training affects the quality of the prefix that is executed at test time. This ablation is not a comparison of different execution horizons. Instead, each row of Table 2 right fixes _H_ eval, so all entries in the row execute the same number of actions before replanning. Only _H_ train changes, which isolates the effect of supervising the policy with shorter or longer action chunks. Pairs with _H_ train < _H_ eval are infeasible because the policy predicts too few actions to execute the requested prefix. 

Success increases monotonically with _H_ train, and the gain of _H_ train=50 over the shortest feasible target shrinks from +20.7 at _H_ eval=10 to +3.3 at _H_ eval=40. This trend suggests that longer training targets provide useful sequence-level supervision: they constrain not only the immediate action after the observation, but also how the motion should evolve across a longer expert segment. Because the executed prefix is predicted jointly with the rest of the chunk, it can inherit this temporal structure even when the suffix is later discarded. We therefore adopt _H_ train=50 as the default prediction horizon. 

Table 3: **Hyperparameter sensitivity.** All results use the smoothed joint-space phase profile and are averaged over all 50 RoboTwin2.0 tasks. Each ( _d_ min, ρ) configuration is evaluated under the full simulation protocol: 3 seeds, 3 independent 100-episode batches per seed, and 900 episodes per task. Thus, each configuration is evaluated over 45,000 episodes in total. Avg. Horizon denotes the mean executed horizon _hi_ selected by PACE, averaged over all policy queries in the evaluation rollouts. Success rates are in %.<sup>†</sup> marks the default. 

|_d_min|Metric||Percen|tileρ||
|---|---|---|---|---|---|
|||0|5|10|25|
|5|Succ.|**64.3**|63.5|63.3|62.5|
||Avg. Horizon|18.1|23.4|24.6|31.9|
|10|Succ.|64.0|64.2<sup>†</sup>|63.0|62.0|
||Avg. Horizon|19.8|24.3<sup>†</sup>|25.5|32.9|


We report both success and average execution horizon, since a stricter selection rule may improve stability by rejecting noisy boundaries but may also delay feedback by accepting too few boundaries. 

As shown in Table 3, PACE remains stable across nearby settings. The best setting, _d_ min=5, ρ=0, achieves 64.3% success, while the default setting, _d_ min=10, ρ=5, achieves a comparable 64.2% success rate with a moderate average execution horizon of 24.3 steps. Increasing ρ makes the acceptance criterion stricter, so fewer candidate boundaries are accepted and the average execution horizon becomes longer. Very strict settings, such as ρ=25, reduce success while pushing the average horizon above 30 steps, suggesting that rejecting too many phase boundaries delays feedback in contact-sensitive stages. We therefore use _d_ min=10, ρ=5 as the default because it provides high success without relying on overly short or overly long execution windows. 

### _4.4 PACE versus Fixed-Horizon Sweeps_ 

**Hyperparameter sensitivity.** We further examine whether PACE depends on a narrowly tuned set of selection hyperparameters. The two parameters in Table 3 affect how easily candidate replanning boundaries are accepted: _d_ min controls the minimum spacing between candidate boundaries, while the calibration percentile ρ determines the strictness of the acceptance threshold. 

We use fixed-horizon sweeps as a diagnostic tool to answer two questions. First, if each task were allowed to choose its best fixed horizon in hindsight, would PACE still reach the high-success region without such task-specific tuning? Second, when PACE and a fixed-horizon schedule query the policy at 

6 


Figure 4: **PACE compared with fixed-horizon sweeps.** Green curves show the seed-0 diagnostic sweep of fixed-horizon execution as _H_ is varied from 1 to 50 on each task. The red star marks PACE under the full three-seed evaluation: its horizontal coordinate is the mean executed horizon averaged over policy queries, and its vertical coordinate is the PACE success rate. PACE is shown as a point only for visualization and does not execute a fixed horizon at the star’s _x_ -coordinate. 

a similar average rate, does adaptive replanning timing still provide an advantage? To study these questions, we sweep _H_ = 1, . . . , 50 on six representative tasks. Such sweeps are not available during real deployment, so they should be viewed as diagnostic references rather than deployable baselines. 

Figure 4 addresses the first question. The fixed-horizon curves differ substantially across tasks: some tasks favor short horizons, others favor longer horizons, and several exhibit strongly non-monotonic success landscapes. Thus, the hindsightbest fixed horizon is highly task-dependent, and no single constant _H_ provides a reliable cross-task deployment rule. The red stars show that PACE reaches the high-success region of these tasks without running a task-specific horizon sweep. Importantly, the star’s horizontal coordinate is only the mean executed horizon selected by PACE over rollouts; PACE does not execute a constant horizon at that value. 

To address the second question, we compare PACE with a fixed-horizon schedule matched to its average execution length. For each task, we compute PACE’s mean selected horizon from the full evaluation protocol with seeds 0, 1, 2, and round it to the nearest integer to obtain the matched fixed horizon _H_ . The matched fixed-horizon baseline then executes this constant _H_ at every policy query, and its success rate is read from the seed-0 fixed-horizon sweep. This comparison is diagnostic rather than a same-budget primary benchmark: PACE and the matched fixed schedule have similar average replanning frequency, but differ in where replanning occurs within the rollout. 

Table 4 shows that, under this diagnostic comparison, PACE outperforms the matched fixed-horizon schedule on all 

Table 4: **Comparison at matched average execution horizon.** For each task, Matched _H_ is obtained by rounding PACE’s mean selected horizon under the full three-seed evaluation. The Fixed column is read from the seed-0 fixed-horizon sweep at this matched horizon. The PACE column reports the full threeseed PACE success rate / absolute gain over the matched fixed baseline. All success values are in %. 

|Task|Matched_H_|Fixed|PACE/ ∆|
|---|---|---|---|
|Pick Dual Bottles|26|46.7|**48.2**/+1.6|
|Grab Roller|29|96.0|**98.6**/+2.6|
|Place A2B Right|24|44.0|**54.6**/+10.6|
|Dump Bin Bigbin|23|88.7|**93.0**/+4.3|
|Put Bottles Dustbin|22|87.0|**88.9**/+1.9|
|Stack Bowls Two|20|88.3|**95.6**/+7.2|


six tasks. Since the matched fixed baseline executes a constant horizon chosen to match PACE’s average executed horizon, this comparison controls for average replanning frequency. The remaining difference is the placement of replanning boundaries. These gains therefore indicate that PACE does not merely benefit from using a shorter or longer average horizon; it improves performance by choosing more appropriate replanning points within the rollout, using the predicted chunk’s phase structure. 

Finally, the hindsight-best fixed horizon _H_<sup>⋆</sup> remains a useful upper reference but is non-deployable, because it is selected only after sweeping all _H_ = 1, . . . , 50 on the test task. PACE instead chooses horizons online from the predicted chunks and requires no task-specific evaluation sweep. 

7 


Figure 5: **Successful real-robot rollout on** `stack_bowls` **.** Blue markers indicate policy-query timesteps, and green labels indicate the execution horizon selected between consecutive queries. PACE selects long horizons during approach and transport, shortens the horizon near contact-sensitive stacking alignment, and expands it again once a coherent motion segment becomes available. 

Table 5: **Real-robot results.** We report baseline and PACE performance under the same metric; ∆ is the absolute gain of PACE over the baseline. _Succ._ denotes full-completion rate in percent. RoboChallenge tasks use 30 trials per method; the Franka task uses 5 × 20 trials per method. 

|Benchmark|Robot|Task||Score|||Succ.||
|---|---|---|---|---|---|---|---|---|
||||Baseline|PACE|∆|Baseline|PACE|∆|
|RoboChallenge|ALOHA|`stack_bowls`|73.0|**93.5**|+20.5|70.0|**90.0**|+20.0|
|RoboChallenge|ALOHA|`put_pen_into_pencil_case`|37.2|**51.7**|+14.5|10.0|**33.3**|+23.3|
|In-lab|Franka|`place_object_on_plate`|72.0|**88.0**|+16.0|72.0|**88.0**|+16.0|


## 5 Real-Robot Experiments 

We evaluate PACE in real-robot experiments that combine a public benchmark with an in-lab task family. For the benchmark component, we use RoboChallenge, a public real-robot evaluation benchmark for embodied policies with standardized task prompts, reset procedures, and grading rules [25]. Using RoboChallenge grounds the ALOHA evaluation in a public and standardized protocol, strengthening the reproducibility of the real-robot results. We evaluate two RoboChallenge tasks, `stack_bowls` and `put_pen_into_pencil_case` , on a bimanual ALOHA robot. To test whether PACE also applies beyond this bimanual benchmark setting, we evaluate an in-lab `place_object_on_plate` task family on a single-arm Franka robot, where the robot places one of five objects onto a target plate. 

Within each task, the baseline and PACE use the same finetuned π0.5 checkpoint and differ only in the test-time execution rule. For each RoboChallenge task, we run 30 trials per method. For the Franka task family, we run 5 × 20 trials per method across five object variants. We report task _Score_ , which gives task-specific partial credit, and full-completion rate _Succ._ ; for `place_object_on_plate` , Score is identical to success rate. Detailed task definitions, scoring rules, fine-tuning settings, and per-object Franka results are provided in Appendix E. 

### _5.1 Real-Robot Results_ 

Table 5 compares PACE with the corresponding baseline under the same real-robot setup and metric. PACE improves all three evaluated settings. On the two RoboChallenge tasks, it increases both the partial-credit Score and the full-completion rate. On the Franka `place_object_on_plate` task family, where Score and Succ. are identical, PACE improves performance from 

72.0% to 88.0%. Averaged over the three real-robot evaluations, PACE raises the Score from 60.7 to 77.7 and Succ. from 50.7% to 70.4%. 

Because the baseline and PACE share the same fine-tuned checkpoint within each task, these gains isolate the effect of the test-time execution rule. The results show that the proposed execution strategy improves real-robot deployment under both a public benchmark protocol and an additional in-lab single-arm setting. We next inspect one successful rollout and one failure case to illustrate how PACE changes execution behavior and where test-time execution control remains limited. 

### _5.2 PACE Horizon Selection in a Successful Rollout_ 

Figure 5 visualizes a successful `stack_bowls` rollout on the real ALOHA robot. This example illustrates how PACE adapts the execution horizon to different manipulation phases rather than following a fixed replanning cadence. During approach and transport, PACE selects long horizons (27, 30, and 31 actions), allowing the robot to preserve continuous motion while open-loop execution remains reliable. Near the contact-sensitive stacking phase, where small pose errors can determine whether the bowls align correctly, the horizon contracts to 7 actions so that the next query can incorporate an updated observation. After this alignment phase, the horizon expands again to 43 actions, showing that PACE does not remain in a high-frequency replanning mode once a coherent motion segment becomes available. 

This behavior mirrors the simulation analysis in Sec. 4.2 and helps explain the real-robot gains in Table 5. PACE introduces feedback where stale observations are most costly, while avoiding unnecessary queries during smooth, coherent motion. Additional rollout visualizations for representative RoboTwin2.0 and RoboChallenge tasks are provided in Appendix F. 

8 


Figure 6: **Failure case on** `put_pen_into_pencil_case` **.** The rollout is from the ALOHA robot. Blue markers indicate policy-query timesteps, and green labels indicate selected horizon lengths. The pencil case remains only partially opened while the right arm moves the pen toward it, showing a failure of the base policy rather than feedback timing. 

### _5.3 Failure Case and Scope of Test-Time Execution Control_ 

Figure 6 shows a failed `put_pen_into_pencil_case` rollout. This task is strictly sequential: the left gripper must first open the pencil case sufficiently before the right arm can insert the pen. In this rollout, PACE selects short horizons around the insertion phase (7 and 6 actions), causing the policy to refresh its action chunk multiple times from updated observations. Nevertheless, the pencil case remains only partially opened while the right arm moves the pen toward it, and the task fails. 

This case illustrates the scope of test-time execution control. PACE can decide when to query the policy and can shorten the execution horizon near contact-sensitive stages, but the refreshed chunks are still generated by the same base policy. When the policy distribution does not contain actions that complete the required subtask—here, fully opening the pencil case before insertion— better replanning timing alone cannot recover the rollout. Thus, PACE improves how predicted chunks are executed, but it cannot compensate for missing task-completing behavior in the underlying policy. 

## 6 Conclusion 

This work revisits test-time execution for robot policies with action chunking. Although action chunks improve local motion continuity, how much of each predicted chunk should be executed before replanning is often treated as a fixed implementation choice. We show that this execution horizon has a large, task-dependent, and non-monotonic effect on success, making a single fixed horizon unreliable. 

We proposed PACE, a training-free method that selects the execution horizon online from the predicted chunk itself. PACE uses low-speed valleys in the predicted speed profile as candidate replanning boundaries, preserving coherent motion segments while refreshing observations near phase transitions. Using only the predicted chunk, PACE requires no retraining, auxiliary heads, policy-internal signals, or inference-engine changes. 

Across 50 RoboTwin2.0 tasks, PACE improves over the strongest fixed-horizon baseline without task-specific horizon sweeps. Real-robot experiments further show gains on both bimanual ALOHA tasks and a single-arm Franka task family. Ablations, rollout analyses, and matched-horizon comparisons indicate that the gains come from better replanning timing rather than simply querying the policy more often. Overall, our results suggest that execution-horizon selection is a central component of reliable action-chunking policy deployment, and a useful complement to training-side improvements in robot policy learning. 

## 7 Limitations 

PACE improves how predicted action chunks are executed, but it does not change the action distribution of the underlying policy. If the base policy fails to generate actions that complete a required subtask, better replanning timing alone cannot recover the rollout. This appears in the failed `put_pen_into_pencil_case` rollout: PACE shortens the horizon near insertion, but the refreshed chunks still do not fully open the pencil case before the pen moves toward it. Thus, PACE should be viewed as an execution layer rather than a mechanism for repairing missing policy capabilities. 

PACE assumes that useful replanning boundaries are reflected in the kinematic structure of the predicted chunk, as is common in manipulation phases involving contact, grasping, release, or alignment. However, tasks whose key decision points are not expressed as low-speed valleys, or policies with noisy motion profiles, may provide weaker signals. 

Finally, our experiments cover a broad set of simulation tasks and real-robot settings, but use a single VLA policy family, π0.5. Future work should evaluate PACE on other chunkgenerating policies, including other VLA architectures, actiontokenized policies, and world-action models, to characterize its generality across different chunk-generation mechanisms. 

9 

## References 

- [1] Kevin Black et al. π0 _: A Vision-Language-Action Flow Model for General Robot Control_ . 2024. doi: `10.48550/ arXiv.2410.24164` . 

- [2] Kevin Black et al. _Real-Time Execution of Action Chunking Flow Policies_ . 2025. doi: `10.48550/arXiv.2506. 07339` . 

- [3] Anthony Brohan et al. _RT-1: Robotics Transformer for Real-World Control at Scale_ . 2022. doi: `10 . 48550 / arXiv.2212.06817` . 

- [4] Anthony Brohan et al. _RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control_ . 2023. doi: `10.48550/arXiv.2307.15818` . 

- [5] Jun Cen et al. _WorldVLA: Towards Autoregressive Action World Model_ . 2025. doi: `10.48550/arXiv.2506. 21539` . 

- [6] Tianxing Chen et al. _RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation_ . 2025. doi: `10.48550/arXiv.2506.18088` . 

- [7] Cheng Chi et al. _Di_ ff _usion Policy: Visuomotor Policy Learning via Action Di_ ff _usion_ . 2023. doi: `10.48550/ arXiv.2303.04137` . 

- [8] Danny Driess et al. _PaLM-E: An Embodied Multimodal Language Model_ . 2023. doi: `10.48550/arXiv.2303. 03378` . 

- [9] Zipeng Fu et al. _Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation_ . 2024. doi: `10.48550/arXiv.2401.02117` . 

- [10] Physical Intelligence et al. π0.5 _: A Vision-LanguageAction Model with Open-World Generalization_ . 2025. doi: `10.48550/arXiv.2504.16054` . 

   - [19] Karl Pertsch et al. _FAST: E_ ffi _cient Action Tokenization for Vision-Language-Action Models_ . 2025. doi: `10.48550/ arXiv.2501.09747` . 

   - [20] Mustafa Shukor et al. _SmolVLA: A Vision-LanguageAction Model for A_ ff _ordable and E_ ffi _cient Robotics_ . 2025. doi: `10.48550/arXiv.2506.01844` . 

   - [21] Octo Model Team et al. _Octo: An Open-Source Generalist Robot Policy_ . 2024. doi: `10.48550/arXiv.2405. 12213` . 

   - [22] Homer Walke et al. _BridgeData V2: A Dataset for Robot Learning at Scale_ . 2023. doi: `10.48550/arXiv.2308. 12952` . 

   - [23] Haoxuan Wang et al. _Real-Time Robot Execution with Masked Action Chunking_ . 2026. doi: `10.48550/arXiv. 2601.20130` . 

   - [24] Haoxuan Wang et al. _VLA Knows Its Limits_ . 2026. doi: `10.48550/arXiv.2602.21445` . 

   - [25] Adina Yakefu et al. _RoboChallenge: Large-scale Realrobot Evaluation of Embodied Policies_ . 2025. doi: `10. 48550/arXiv.2510.17950` . 

   - [26] Seonghyeon Ye et al. _World Action Models are Zero-shot Policies_ . 2026. doi: `10.48550/arXiv.2602.15922` . 

   - [27] Yanjie Ze et al. _3D Di_ ff _usion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations_ . 2024. doi: `10.48550/arXiv.2403.03954` . 

   - [28] Tianle Zhang et al. _JoyAI-RA 0.1: A Foundation Model for Robotic Autonomy_ . 2026. doi: `10.48550/arXiv. 2604.20100` . 

   - [29] Tony Z. Zhao et al. _Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware_ . 2023. doi: `10. 48550/arXiv.2304.13705` . 

- [11] Dong Jing et al. _Mixture of Horizons in Action Chunking_ . 2025. doi: `10.48550/arXiv.2511.19433` . 

- [12] Alexander Khazatsky et al. _DROID: A Large-Scale InThe-Wild Robot Manipulation Dataset_ . 2024. doi: `10. 48550/arXiv.2403.12945` . 

- [13] Moo Jin Kim et al. _Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success_ . 2025. doi: `10. 48550/arXiv.2502.19645` . 

- [14] Moo Jin Kim et al. _OpenVLA: An Open-Source VisionLanguage-Action Model_ . 2024. doi: `10.48550/arXiv. 2406.09246` . 

- [15] Oliver Kroemer et al. “Towards Learning Hierarchical Skills for Multi-Phase Manipulation Tasks”. In: _2015 IEEE International Conference on Robotics and Automation (ICRA)_ . 2015. doi: `10.1109/ICRA.2015.7139389` . 

- [16] Sang Hyoung Lee, Il Hong Suh, et al. “Autonomous Framework for Segmenting Robot Trajectories of Manipulation Task”. In: (2015). doi: `10.1007/s10514014-9397-9` . 

- [17] Songming Liu et al. _RDT-1B: A Di_ ff _usion Foundation Model for Bimanual Manipulation_ . 2024. doi: `10.48550/ arXiv.2410.07864` . 

- [18] Open X-Embodiment Collaboration et al. _Open X- Embodiment: Robotic Learning Datasets and RT-X Models_ . 2023. doi: `10.48550/arXiv.2310.08864` . 

10 

## A PACE Implementation Notes 

PACE is applied only at test time and does not modify or retrain the base policy. After each policy query, it analyzes the predicted action chunk and selects how many actions to execute before the next query. The selection is based on the kinematic structure of the predicted arm motion: PACE constructs a speed profile, suppresses short-range fluctuations, and identifies prominent low-speed regions as candidate phase boundaries. 

In multi-arm settings, candidate boundaries from all executed arms are considered jointly, and the earliest accepted boundary is used as the replanning point. This allows the policy to refresh its observation before an arm crosses a predicted phase boundary under stale context. If no valid boundary is found, PACE executes a longer prefix up to a maximum horizon. 

The acceptance rule for candidate boundaries is calibrated once from training demonstrations and is kept fixed during evaluation. This calibration does not use evaluation rollouts, success labels, or fixed-horizon sweeps. The same procedure applies to single-arm and multi-arm settings; the only difference is the set of executed arms used to construct the kinematic profiles. 

## B Simulation Evaluation Details 

This appendix provides the simulation evaluation protocol and the complete task-level results for the main comparison in Sec. 4.1. The ablation studies and fixed-horizon sweeps use separate evaluation budgets and are described in Appendix C and Appendix D, respectively. 

### _B.1 Benchmark and Execution Schemes_ 

We evaluate the main simulation results on the 50-task RoboTwin2.0 benchmark under the `demo_clean` setting. Each task uses one trained π0.5 checkpoint with prediction horizon _L_ = 50. Within a task, all execution schemes share the same checkpoint and receive the same observation and language-instruction inputs. They differ only in the test-time execution rule, which determines how much of each predicted action chunk is executed before the next policy query. 

We compare PACE with fixed-horizon execution using _H_ ∈{5, 25, 50}. Under fixed-horizon execution, the robot executes the first _H_ actions of each predicted chunk before re-querying the policy. The _H_ = 50 baseline corresponds to full-chunk execution under the training prediction horizon _L_ = 50. The fixed baselines are used as global execution rules and are not tuned separately for individual tasks. PACE uses the same predicted chunks, but selects the executed prefix online from the predicted motion structure. 

### _B.2 Evaluation Metric and Aggregation_ 

Success is measured by the RoboTwin2.0 task success predicate at the episode level. For each task T and method _m_ , we evaluate three seeds. For each seed, we run three independent batches of 100 episodes, giving 3 × 3 × 100 = 900 episodes per task-method pair. 

Let _S_ T , _m_ , _s_ , _b_ denote the success rate of method _m_ on task T , seed _s_ , and evaluation batch _b_ , computed over 100 episodes. The task-level success rate is 


The reported 50-task average is the equal-weight mean over all tasks: 


Thus, each task contributes equally to the aggregate success rate, regardless of task duration or the number of policy queries used during a rollout. 

### _B.3 Full 50-Task Results_ 

Table 6 reports the complete task-level results for the main simulation comparison. Values are success rates in percent, averaged over 900 episodes per task-method pair. The strongest global fixed-horizon baseline is _H_ = 25, with a 50-task average success rate of 57.8%. PACE improves the average success rate to 64.2%, while using the same task checkpoints as the fixed-horizon baselines. 

11 

Table 6: **Full main simulation results on 50 RoboTwin2.0 tasks.** All values are success rates (%). Each task-method value is averaged over 900 episodes: seeds 0, 1, 2, with three 100-episode batches per seed. 

|Task|_H_ =5|_H_ =25|_H_ =50|PACE|
|---|---|---|---|---|
|`adjust_bottle`|99.0|98.8|96.1|99.6|
|`beat_block_hammer`|81.1|67.7|66.6|80.7|
|`blocks_ranking_rgb`|7.3|50.0|36.1|61.4|
|`blocks_ranking_size`|23.9|18.6|9.2|32.9|
|`click_alarmclock`|92.4|65.3|65.9|87.6|
|`click_bell`|97.8|49.2|41.4|91.4|
|`dump_bin_bigbin`|58.7|85.1|84.3|93.0|
|`grab_roller`|89.9|96.2|96.2|98.6|
|`handoverblock`|3.6|33.2|52.6|53.1|
|`_`<br>`handover_mic`|77.2|97.7|96.8|99.4|
|`hanging_mug`|16.2|15.8|16.7|21.8|
|`lift_pot`|50.9|61.2|62.0|65.4|
|`move_can_pot`|55.4|74.3|58.2|72.3|
|`move_pillbottle_pad`|34.8|49.9|29.1|45.0|
|`move_playingcard_away`|79.2|79.7|69.6|79.3|
|`move_stapler_pad`|12.6|11.4|7.1|18.6|
|`open_laptop`|84.9|84.8|88.8|88.0|
|`open_microwave`|33.3|26.0|60.3|45.0|
|`pick_diverse_bottles`|13.4|23.9|24.1|35.7|
|`pick_dual_bottles`|13.3|45.3|38.7|48.2|
|`place_a2b_left`|54.6|52.7|43.2|55.9|
|`place_a2b_right`|20.0|47.8|36.8|54.6|
|`place_bread_basket`|55.3|53.9|30.3|49.1|
|`place_bread_skillet`|38.4|39.8|29.0|37.0|
|`place_burger_fries`|88.9|89.3|85.8|91.3|
|`place_can_basket`|18.1|56.8|38.2|53.6|
|`place_cans_plasticbox`|85.1|83.0|81.8|90.6|
|`place_container_plate`|88.3|81.7|91.6|96.1|
|`place_dual_shoes`|19.9|40.6|33.7|37.3|
|`place_empty_cup`|59.4|48.1|45.8|58.8|
|`place_fan`|35.3|34.0|25.8|39.1|
|`place_mouse_pad`|4.3|14.1|12.8|17.8|
|`place_object_basket`|35.9|59.4|58.0|70.2|
|`place_object_scale`|23.8|29.4|18.9|40.7|
|`place_object_stand`|64.2|57.3|53.4|59.2|
|`place_phone_stand`|52.9|59.9|54.7|58.7|
|`place_shoe`|43.9|64.4|56.1|62.8|
|`press_stapler`|68.2|60.6|56.0|61.8|
|`put_bottles_dustbin`|0.3|79.3|70.8|88.9|
|`put_object_cabinet`|7.6|51.9|50.6|57.4|
|`rotate_qrcode`|48.9|69.9|66.1|71.7|
|`scan_object`|20.9|43.1|28.9|40.3|
|`shake_bottle`|95.2|95.7|96.7|98.4|
|`shake_bottle_horizontally`|97.3|96.8|96.9|98.8|
|`stackblocksthree`|39.7|43.2|28.7|55.2|
|`__`<br>`stack_blocks_two`|12.4|80.1|63.9|82.3|
|`stackbowlsthree`|45.0|61.0|67.6|79.8|
|`__`<br>`stack_bowls_two`|88.7|88.4|85.1|95.6|
|`stamp_seal`|67.4|34.2|24.3|47.8|
|`turn_switch`|34.4|39.4|37.1|42.6|
|**Average**|**48.8**|**57.8**|**53.4**|**64.2**|


12 

## C Additional Ablation Details 

This appendix provides protocol details and expanded results for the ablation studies in Sec. 4.3. The main text reports summary results for phase-profile construction, training prediction horizon, and selection-parameter sensitivity. Here, we specify the evaluation budgets used by these ablations and provide the expanded training-horizon sweep. 

### _C.1 Ablation Protocol_ 

The phase-profile construction ablation and the selection-parameter sensitivity study are evaluated on all 50 RoboTwin2.0 tasks under the same full evaluation protocol as the main simulation comparison: seeds 0, 1, 2, three independent 100-episode batches per seed, and 900 episodes per task-method pair. For PACE variants, the reported average horizon is computed as the mean selected execution horizon over all policy queries in the corresponding evaluation rollouts. 

The training-prediction-horizon ablation requires retraining policies with different supervised prediction horizons _H_ train. We therefore evaluate this ablation on the six representative tasks used in the main text. For each setting, we use seed 0 and run three independent 100-episode evaluation batches. This gives 300 evaluation episodes per setting. Each row in the training-horizon analysis fixes the evaluation horizon _H_ eval and varies _H_ train, so entries within a row execute the same number of actions before replanning and differ only in the prediction horizon used during training. Settings with _H_ train < _H_ eval are infeasible because the policy does not predict enough actions to execute the requested prefix. 

### _C.2 Expanded Training-Horizon Results_ 

The main text reports a coarse grid of the training-prediction-horizon ablation. Here we provide the expanded sweep over _H_ train, _H_ eval ∈{5, 10, . . . , 50}, evaluated on six representative tasks. The goal is to isolate how the supervised prediction horizon used during training affects fixed-horizon execution at test time. 

For each evaluation horizon _H_ eval, we use the shortest feasible training horizon _H_ train = _H_ eval as the row-wise reference. Each cell in Fig. 7 reports the success-rate gain of a larger _H_ train relative to this reference. The diagonal is therefore zero by construction, and cells below the diagonal are left blank because _H_ train < _H_ eval is infeasible. 

Figure 7 shows three main patterns. First, for non-trivial execution horizons, increasing _H_ train generally improves fixed-horizon execution. For example, the gain reaches +20.7 at _H_ eval = 10, +13.0 at _H_ eval = 15, and +6.6 at _H_ eval = 20. This supports the interpretation that longer supervised chunks provide useful sequence-level supervision, and the executed prefix benefits from being predicted jointly with a longer future segment. 

Second, _H_ eval = 5 is an exception: most entries in this row are near zero or negative. When the policy is queried after only a very short prefix, performance is dominated by high-frequency feedback, and the advantage of training with longer prediction targets is less pronounced. 

Third, the benefit of increasing _H_ train becomes smaller as _H_ eval grows. When the executed prefix is already long, the additional supervision on the later part of the chunk contributes less to the actions that are actually executed before the next replanning step. This trend is consistent with the summary table in Sec. 4.3: longer training horizons are most beneficial when the executed prefix is short but non-trivial, which matches the operating regime of PACE. 

## D Fixed-Horizon Sweep Details 

This appendix provides additional details for the fixed-horizon sweep analysis in Sec. 4.4. The purpose of this analysis is diagnostic: it characterizes how sensitive each task is to the choice of a constant execution horizon, and it compares PACE with fixed schedules that have a similar average replanning frequency. It is not used as the primary simulation comparison, which is reported in Sec. 4.1 and Appendix B. 

### _D.1 Sweep Protocol_ 

For each of the six representative tasks in Sec. 4.4, we evaluate fixed-horizon execution for every integer 

### _H_ ∈{1, . . . , 50}. 

For a fixed value of _H_ , the robot executes the first _H_ actions of each predicted chunk before querying the policy again. All fixed-horizon evaluations in this sweep use seed 0 and three independent batches of 100 episodes, giving 300 episodes per horizon. Sweeping all 50 horizons over six tasks already requires 

6 × 50 × 3 × 100 = 90,000 

13 


Figure 7: **Expanded training prediction horizon ablation.** Each cell shows the success-rate gain of training horizon _H_ train (columns) relative to the shortest feasible training horizon for a given evaluation horizon _H_ eval (rows), i.e., _H_ train = _H_ eval. Blue indicates a gain, orange a loss; the diagonal is zero by construction. Cells below the diagonal are infeasible and left blank. 

episodes. Repeating the full sweep for three seeds would triple this diagnostic budget. We therefore use the seed-0 sweep to characterize the shape of the fixed-horizon success curve. 

The PACE quantities reported in this appendix follow the main evaluation protocol: they are computed using seeds 0, 1, 2, with three 100-episode batches per seed. Thus, PACE success rates and mean selected horizons are based on 900 episodes per task. We use this full PACE evaluation because it is the same estimate used in the main simulation results. The fixed-horizon sweep and the PACE point therefore have different evaluation budgets; this asymmetry is intentional and should be interpreted in light of the diagnostic role of the sweep. 

Let _S_<sup>(0)</sup> denote the PACE T<sup>(</sup><sup>_H_) denote the seed-0 success rate of fixed-horizon execution with horizon</sup><sup>_H_on task T .Let</sup><sup>_S_PACE</sup> T success rate under the full three-seed evaluation. We also compute the mean selected PACE horizon 


where QT is the set of all policy-query events in the PACE evaluation rollouts for task T , and _hq_ is the execution horizon selected at query _q_ . 

### _D.2 Diagnostic Reference Points_ 

The sweep provides two fixed-horizon reference points. First, we report the hindsight-best fixed horizon on the seed-0 sweep: 


When multiple horizons attain the same best success rate, all tied horizons are listed. This value is an oracle reference within the class of fixed-horizon schedules, because it can only be selected after evaluating all horizons on the test task. It is therefore not a deployable baseline. 

14 

Second, we compare PACE with a fixed-horizon schedule matched to its average execution length. We define 


The corresponding fixed baseline executes this constant horizon at every policy query, and its success rate is read from the seed-0 fixed-horizon sweep as _S_ T<sup>(0)(</sup><sup>_H_</sup> T<sup>match</sup> ). This comparison controls for average replanning frequency: PACE and the matched fixed schedule query the policy at a similar average rate, but differ in where replanning occurs within the rollout. 

Table 7: **Diagnostic fixed-horizon sweep summary.** Fixed-horizon columns are computed from the seed-0 sweep with 300 episodes per horizon. PACE columns use the full three-seed evaluation with 900 episodes per task. _H_<sup>⋆</sup> is the hindsight-best fixed horizon on the seed-0 sweep. Matched _H_ is the integer horizon nearest to PACE’s mean selected horizon. All success values are percentages. ∆ is the absolute gain of PACE over the fixed-horizon schedule at Matched _H_ . 

|Task|_H_<sup>⋆</sup>|Fixed at_H_<sup>⋆</sup>|PACE Mean_H_|Matched_H_|Fixed at Matched_H_|PACE|∆|
|---|---|---|---|---|---|---|---|
|Pick Dual Bottles|14|56.7|25.5|26|46.7|48.2|+1.6|
|Grab Roller|7, 9, 32|97.7|28.9|29|96.0|98.6|+2.6|
|Place A2B Right|11|53.3|23.8|24|44.0|54.6|+10.6|
|Dump Bin Bigbin|37|90.3|22.7|23|88.7|93.0|+4.3|
|Put Bottles Dustbin|18|88.7|22.3|22|87.0|88.9|+1.9|
|Stack Bowls Two|8|95.3|19.7|20|88.3|95.6|+7.2|


### _D.3 Interpretation_ 

The hindsight-best fixed horizon _H_<sup>⋆</sup> varies substantially across tasks. Some tasks prefer short horizons, such as _H_ = 7 or _H_ = 8, while others prefer much longer horizons, such as _H_ = 37. One task, _Grab Roller_ , has multiple tied best horizons. This spread confirms that the best constant execution horizon is strongly task-dependent. Since _H_<sup>⋆</sup> is selected after sweeping the test task, it is useful only as a diagnostic oracle and cannot be used as a practical deployment rule. 

The matched-horizon comparison asks a different question: whether PACE helps only because it changes the average number of policy queries, or because it places those queries at better moments. Table 7 shows that, under this diagnostic comparison, PACE outperforms the matched fixed-horizon schedule on all six representative tasks. Since the matched fixed baseline uses a constant horizon nearest to PACE’s mean selected horizon, this comparison controls for average replanning frequency. The remaining difference is the timing of replanning: the fixed baseline replans at uniform intervals, whereas PACE replans according to the predicted motion structure of each chunk. 

The sweep should therefore be read as diagnostic evidence rather than as a separate main benchmark. The fixed-horizon curves reveal the non-monotonic and task-dependent nature of horizon selection, while the matched-horizon comparison suggests that adaptive replanning timing contributes beyond the average query budget. The primary deployable comparison remains the global fixed-horizon baselines in Sec. 4.1, where no method is allowed to select a task-specific horizon by sweeping the test task. 

## E Real-Robot Evaluation Details 

This appendix provides additional details for the real-robot experiments in Sec. 5. We describe the task setups, metrics, scoring rules, fine-tuning configurations, evaluation protocol, and per-object results for the Franka task family. Across all real-robot experiments, the baseline and PACE use the same fine-tuned checkpoint within each task; they differ only in the test-time execution rule. 

### _E.1 Task Setups_ 

We evaluate three real-robot settings. Two tasks are from RoboChallenge: `stack_bowls` and `put_pen_into_pencil_case` , both evaluated on a bimanual ALOHA robot. RoboChallenge provides standardized task prompts, reset procedures, and grading rules, which makes the ALOHA results directly comparable under a public benchmark protocol. We additionally evaluate an in-lab `place_object_on_plate` task family on a single-arm Franka robot to test whether the same execution strategy transfers beyond the bimanual RoboChallenge setting. 

Figure 8 shows the initial observation frames for the two RoboChallenge tasks. In `put_pen_into_pencil_case` , the robot must coordinate both arms: one gripper opens the pencil case while the other manipulates the pen. In `stack_bowls` , the robot must grasp and nest the bowls in the correct order. These tasks stress different temporal structures: the pencil-case task is strongly sequential and contact-sensitive, while the bowl-stacking task contains repeated pick-and-place motions with precise alignment during stacking. 

15 

Table 8: **Real-robot task and data summary.** Demos denotes the number of demonstration episodes used for fine-tuning. Trials / method denotes the number of real-robot evaluation trials for each compared execution rule. 

|Task|Robot|Demos|Trials/method|
|---|---|---|---|
|`stack_bowls`|ALOHA|1,047|30|
|`put_pen_into_pencil_case`|ALOHA|1,220|30|
|`place_object_on_plate`|Franka|301|5×20|


Figure 8: **Initial frames of the RoboChallenge tasks.** Left: `put_pen_into_pencil_case` . Right: `stack_bowls` . Both tasks are evaluated on an ALOHA robot using the same fine-tuned checkpoint within each task; only the test-time execution rule differs between the baseline and PACE. 

For `place_object_on_plate` , the Franka robot must pick up a specified object and place it fully inside a target plate. We use five object variants: corn, cabbage, green pepper, red pepper, and garlic. A single fine-tuned checkpoint is shared across all five object variants. Each object is evaluated over 20 trials per method, giving 100 trials per method in total. 

### _E.2 Metrics and Scoring Rules_ 

We report two metrics: _Score_ and _Succ._ . For RoboChallenge tasks, Score is the official partial-credit task score, reported on a 0–100 scale. Let _pn_ denote the number of points achieved in trial _n_ , and let _P_ max = 10 denote the maximum possible points for a trial. For _N_ trials, we compute 

The full-completion rate is 


Thus, Score reflects partial progress, while Succ. counts only trials that complete the entire task. 

For the Franka `place_object_on_plate` task, each trial is binary: the object is either successfully placed fully inside the plate or not. Hence Score and Succ. are identical for this task family. 

`stack_bowls` **.** The task is to nest the bowls from largest to smallest. The scoring rule is: 

- 2.0 × 2 points: pick up a bowl with the gripper. 

- 2.5 × 2 points: successfully stack the bowls. 

- 1.0 point: retract the gripper to its original position. 

16 


Figure 9: **In-lab** `place_object_on_plate` **setup.** The task uses five objects—corn, cabbage, green pepper, red pepper, and garlic—and a fixed target plate. A single fine-tuned π0.5 checkpoint is used across all object variants, and each method is evaluated over 5 × 20 real-robot trials. 

`put_pen_into_pencil_case` **.** The task is to place the pen into the pencil case. In our evaluation setup and rollout videos, the left gripper opens the pencil case while the right arm manipulates the pen. We therefore describe the scoring steps using this observed arm assignment: 

- 2.0 points: left gripper reaches and opens the pencil case. 

- 2.0 points: the pencil case is sufficiently open for insertion. 

- 2.0 points: right arm picks up the pen. 

- 3.0 points: right arm places the pen into the pencil case. 

- 1.0 point: reset both arms. 

`place_object_on_plate` **.** A trial is successful only if the target object is fully inside the plate at the end of the trial. If any part of the object remains outside the plate, the object falls out of the plate, or the robot fails to release the object into the plate, the trial is counted as a failure. Each successful trial receives 1 point and each failed trial receives 0 points. 

### _E.3 Fine-Tuning Details_ 

For each RoboChallenge task, we fine-tune a task-specific π0.5 policy initialized from the π0.5 base checkpoint. Training is performed on four H200 GPUs with FSDP and bfloat16 precision. We use AdamW with a global batch size of 256, global gradient clipping at norm 1.0, EMA decay 0.99, and eight data-loader workers. The learning rate follows a cosine decay schedule with 1000 warmup steps, peak learning rate 2.5 × 10<sup>−5</sup> , decay horizon 30,000 steps, and final learning rate 2.5 × 10<sup>−6</sup> . For all reported RoboChallenge trials, we deploy the 30,000-step checkpoint. 

For `place_object_on_plate` , we fine-tune a single π0.5 checkpoint over all five object variants using 301 demonstrations. The training recipe follows the RoboChallenge setting except that we use a batch size of 32 and train on one RTX A6000 Pro GPU. We also deploy the 30,000-step checkpoint for all in-lab trials. 

17 

### _E.4 Evaluation Protocol_ 

Within each task, the baseline and PACE use the same fine-tuned checkpoint and receive the same observation and languageinstruction inputs. The comparison therefore isolates the effect of the test-time execution rule rather than differences in model architecture, data scale, training procedure, or checkpoint selection. 

The baseline executes the full predicted action chunk at test time, corresponding to _H_ = 50. PACE uses the same predicted action chunks, but selects the executed prefix online according to the execution rule described in Appendix A. No task-specific horizon tuning is performed during evaluation. 

For each RoboChallenge task and each method, we run 30 real-robot trials. For the Franka task family, we run 20 trials per object and evaluate five objects, giving 5 × 20 = 100 trials per method. All reported real-robot results in Sec. 5.1 use these trial counts. 

### _E.5 Per-Object Franka Results_ 

Table 9 reports per-object results for `place_object_on_plate` . PACE improves performance on all five object variants, indicating that the aggregate gain is not caused by a single object category. 

Table 9: **Per-object results for** <u>`place_object_on_plate`</u> **.** Each object variant is evaluated over 20 trials per method. 

|Object|Baseline|PACE|∆|
|---|---|---|---|
|Corn|16/20 (80.0%)|**18**/**20 (90.0%)**|+10.0|
|Cabbage|15/20 (75.0%)|**17**/**20 (85.0%)**|+10.0|
|Green pepper|13/20 (65.0%)|**18**/**20 (90.0%)**|+25.0|
|Red pepper|14/20 (70.0%)|**17**/**20 (85.0%)**|+15.0|
|Garlic|14/20 (70.0%)|**18**/**20 (90.0%)**|+20.0|
|**Total**|**72**/**100 (72.0%)**|**88**/**100 (88.0%)**|+16.0|


18 

## F Additional PACE Rollout Visualizations 

This appendix provides additional qualitative rollout visualizations for representative RoboTwin2.0 and RoboChallenge tasks. As in the main paper, the figures highlight the policy-query timesteps and the execution horizons chosen online by PACE from the predicted motion profile. These examples complement the quantitative results by showing how the same phase-aware execution rule adapts across different task families and robot platforms. 

### _F.1 RoboTwin2.0 Rollouts_ 

`place_can_basket` **.** This rollout illustrates a contact-sensitive placement task in which PACE shortens the execution horizon near the transition into the basket and uses longer prefixes during smoother transport phases. 


Figure 10: **PACE rollout visualization on** `place_can_basket` **.** The selected execution horizon adapts to the local phase structure of the rollout, with shorter prefixes near the placement transition and longer prefixes during smooth motion segments. 

19 

`hanging_mug` **.** This rollout shows a task with a pronounced interaction phase, where PACE reduces the execution horizon near the hanging transition and expands it again when the motion becomes smoother. 


Figure 11: **PACE rollout visualization on** `hanging_mug` **.** The execution horizon is shortened around the task transition that requires precise alignment and interaction, and lengthened during more stable motion segments. 

`scan_object` **.** This rollout highlights a task with a more gradual motion structure. PACE continues to adapt the execution horizon online, using longer prefixes during steady motion and shorter prefixes when the predicted chunk enters a low-speed transition. 


Figure 12: **PACE rollout visualization on** `scan_object` **.** PACE selects execution horizons from the predicted kinematic profile, allowing the rollout to keep longer open-loop segments when motion is smooth and to replan earlier around phase transitions. 

20 

### _F.2 RoboChallenge Rollout_ 

`stack_bowls` **.** This rollout on RoboChallenge shows the same phase-aware behavior on a bimanual stacking task. PACE keeps longer horizons during approach and transport and shortens the horizon near the stacking contact, where fresh observations are most valuable. 


Figure 13: **PACE rollout visualization on RoboChallenge** `stack_bowls` **.** The selected execution horizon is longer during smooth approach and transport, and shorter near the stacking phase, reflecting the same phase-aware replanning rule used throughout the paper. 

21 

