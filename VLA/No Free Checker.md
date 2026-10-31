---
title: "No Free Checker: A Survey of Verifiers for Robot Policies"
date: "2026-09-08"
authors: "Yang Wan; Xihang Yue; Zhirui Liu; Ziyuan Chu; Shuxun Wang; Yuhan Chen"
url: https://arxiv.org/abs/2609.09250
pdf: https://arxiv.org/pdf/2609.09250
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.09250)** / [論文ページ](https://arxiv.org/abs/2609.09250)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Preprint** 

# **No Free Checker: A Survey of Verifiers for Robot Policies** 

**Yang Wan**<sup>1</sup> , **Xihang Yue**<sup>1</sup> , **Zhirui Liu**<sup>1</sup> , **Ziyuan Chu**<sup>1</sup> , **Shuxun Wang**<sup>1</sup> , **Yuhan Chen**<sup>1</sup> , **Xiaonan Jiang**<sup>2</sup> , **Xukun Zhu**<sup>1</sup> , **Yubo Dong**<sup>1</sup> , **Linchao Zhu**<sup>1</sup> 

- 1 Zhejiang University, 2 City University of Hong Kong 

   - Awesome-Robot-Verifier 

A verifier for robot policies reads a candidate behavior and returns a score for how well it did, used both to evaluate vision-language-action policies and to train them. Verifiers range from success detectors and reward models to runtime monitors, safety filters, and temporal-logic specifications. 

We survey roughly 150 verifiers and compare them along two properties. _Availability_ is how much a verdict costs, how early in a rollout the verdict arrives, and how often a verdict can be asked for. Availability rises as verdicts get cheaper, earlier, and denser. _Credibility_ is how much a high score tells us about the task. Credibility falls as the judgment becomes gameable and self-serving. We group the verifiers by who supplies the judgment: _human verifiers_ , _rule-based and formal verifiers_ , _learned and pretrained verifiers_ , and _model-intrinsic verifiers_ . Across the four families, we find that credibility falls as availability rises. Regardless of who supplies the judgment, **there is no free checker** . 

We then examine what validates a verifier itself, and how much a high score tells us. Three measures appear in the literature: agreement with human labels, the performance of the policy it trains, and behavior under reward hacking. We close with nine metrics that make a verifier claim checkable, and coordinates for the verifiers still to be built. 

**Keywords:** Robot policy evaluation, Reward models, Vision-language-action models, Runtime monitoring, Safety filters, Reward hacking, World models, Data curation for imitation learning 

1 

## **Contents** 

|**1**<br>**Introduction**|**3**|
|---|---|
|**2**<br>**Human Verifiers**|**4**|
|2.1<br>Comparing Trajectories . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>5|
|2.2<br>Scoring Trajectories . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>5|
|2.3<br>Intervening During Execution. . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>6|
|2.4<br>Validating Generated Rollouts. . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>7|
|**3**<br>**Rule-Based and Formal Verifiers**|**7**|
|3.1<br>Full-Trajectory Verification . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>8|
|3.2<br>Terminal-State Verification . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>10|
|3.3<br>Physical-Constraint Verification . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>11|
|**4**<br>**Learned and Pretrained Verifiers**|**13**|
|4.1<br>Evaluating Behavior and Policies . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>13|
|4.2<br>Inference-Time Verification . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>15|
|4.3<br>Feeding Verifier Feedback into Policy Learning. . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>15|
|**5**<br>**Model-Intrinsic Verifiers**|**17**|
|5.1<br>Policy-Based Self-Verification . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>17|
|5.2<br>Prediction-Based Outcome Verification . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>18|
|5.3<br>Beyond Action Verification: Task Selection . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>19|
|**6**<br>**Validating the Verifier**|**20**|
|6.1<br>Agreement on a Fixed Set of Rollouts. . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>20|
|6.2<br>Measuring a Verifier by the Policy It Trains. . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>21|
|6.3<br>Measuring a Verifier Under Optimization. . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>22|
|6.4<br>Metrics for Validating a Verifier . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . .<br>23|
|**7**<br>**Conclusion**|**23**|


2 

## **1 Introduction** 

In robot learning, vision-language-action (VLA) policies (1, 2, 3, 4, 5) and robot world models (6, 7) are scaling rapidly and becoming more capable. While scaling remains important, verification of training data and model behavior is also essential, as demonstrated by recent progress in large language models (8). Such verification signals are used at multiple stages of robot learning, including filtering and reweighting demonstrations for pre-training (9, 10, 11), providing reward signals during policy post-training (12, 13, 14), ranking candidate actions at inference time (15, 16, 17), and evaluating policy performance using rollouts generated by world models (18, 19, 20). We refer to the mechanisms that provide these verification signals collectively as _verifiers_ . 

A robot verifier is a mapping 

verifier : (context _,_ candidate) ↦−→ score _._ (1) 

The context comprises observations, a goal, and possibly a language instruction. The score can be boolean, scalar, vector-valued, or a distribution. The candidate varies the most of the three, running from a single action chunk up to an entire policy, with subtask segments and full trajectories in between. 

Building reliable _verifiers_ for robot learning is particularly difficult because the physical world lacks the cheap and well-defined criteria available in mathematics and code. First, determining whether a physical task has been completed correctly is costly because task success is often inferred from imperfect sensory observations (21, 22, 23). Second, evaluating a policy is expensive because testing a policy may require real-robot rollouts, which consume physical time and limit large-scale sampling (18, 20, 24). Third, verification often has to happen before the task is finished, because a single incorrect action is enough to cause task failure or hardware damage (25, 26, 27, 28, 29). Finally, task performance is often continuous, as robot behaviors can differ in progress, safety, and execution quality, making a single success-or-failure label insufficient (30, 31, 32, 33). 

Given these challenges, different verifiers offer different strengths and limitations in robot learning. To systematically understand existing methods, we survey roughly 150 works on verification in robot learning. Figure 1 places representative systems by family and year, and Table 1 records what each family’s score asserts. Further, we characterize these works along two properties, _availability_ and _credibility_ . _Availability_ is how much a verdict costs, how early in a rollout the verdict arrives, and how often a verdict can be asked for. _Credibility_ is how much a high score tells us about the task. 

The source of judgment strongly affects the _availability_ and _credibility_ of a verifier. We therefore group existing methods by judge source into four families: (a) **human verifiers** , where the judgment is provided directly by a person, (b) **rule-based and formal verifiers** , where the judgment is determined by predefined criteria, (c) **learned and pretrained verifiers** , where the judgment is produced by a neural model, (d) **model-intrinsic verifiers** , where the judgment comes from signals already computed by the model itself. 

- **Human verifiers** (Section 2). A person directly judges task success, compares trajectories, or intervenes during execution (34, 35, 36). In terms of _availability_ , human judgments are costly and sparse because judgments take human effort. In terms of _credibility_ , they provide a direct reference to task intent, although they may still be subjective or inconsistent. 

- **Rule-based and formal verifiers** (Section 3). The judgment is determined by predefined criteria, such as task predicates, temporal-logic specifications, or formal safety conditions (37, 38, 28). In terms of _availability_ , these verifiers are inexpensive and repeatable once the required state information is available. In terms of _credibility_ , they can provide strong and sometimes formal guarantees, but only when the predefined criteria, state estimates, and dynamics assumptions accurately represent the task. 

- **Learned and pretrained verifiers** (Section 4). A neural model produces the judgment, either after taskspecific training or directly from pretraining (39, 40, 33). In terms of _availability_ , these verifiers are inexpensive to query and can provide dense feedback across many tasks and trajectories. In terms of _credibility_ , their judgments depend on model accuracy, calibration, and generalization beyond the data on which they were trained or validated. 

- **Model-intrinsic verifiers** (Section 5). The judgment is derived from signals already computed by the policy or predictive model, such as action uncertainty, model uncertainty, or learned reachability (17, 41, 42). In terms of _availability_ , these signals are the easiest to obtain because they require little or no additional 

3 


**Figure 1** Representative systems by judge source and year, using the same five columns as Table 1. Disc area is the number of papers we cover in the corresponding year. Our search closes in early July 2026, so each 2026 disc carries a dashed ring at the full-year estimate, twice the observed count at the January-to-June rate. 

computation or external supervision. In terms of _credibility_ , model-intrinsic signals describe the model itself, and their relation to actual task performance is therefore indirect. 

Across these four families, the source of judgment shows a clear trade-off between _availability_ and _credibility_ . Human judgments and explicit task criteria provide a more direct measure of task performance, but human judgment is costly to collect at scale, and an explicit criterion holds only where its state estimates and physical assumptions represent the task (36, 37, 28). Learned and model-intrinsic signals are cheaper to query and can provide denser feedback, but a learned judgment depends on how well the model generalizes beyond its training data, and an intrinsic signal describes the model itself rather than task performance (21, 33, 17, 41). Therefore, in the physical world, obtaining both high _availability_ and high _credibility_ at the same time is costly. We refer to this observation as **no free checker** . 

We therefore examine in Section 6 how a verifier’s own error is measured, and why _credibility_ is difficult to establish in robotics. Three metrics appear, agreement with a fixed reference, the policy that results from training on the verifier, and the verifier’s behavior under a search for the inputs where its score is wrong. We close the section with the metrics whose reporting makes a verifier checkable by someone else. Section 7 concludes. 

## **2 Human Verifiers** 

A human verifier asks a person to look at what the policy did and say whether the behavior is good. The four methods in this section differ in what the person sees and in what the person is asked to return. The person sees two trajectories and says which one is better (§2.1). The person sees one trajectory and gives a score at every time step (§2.2). The person watches a policy while it runs, decides whether to take over, and supplies the correct action (§2.3). The fourth method changes the object rather than the question, showing the person a generated rollout and asking whether that rollout preserves the outcome the real execution would have reached (§2.4). All four methods share one limitation, that verdicts are costly to obtain. A human verdict can apply to any task and is the label closest to the intended task, so these verdicts also serve as training data for cheaper verifiers. Each subsection below covers how its labels enter the cheaper verifier’s training. 

4 

||||**Learned and pre i**|**trained verifiers**|||
|---|---|---|---|---|---|---|
|**What the score asserts**|**Human**|**Rules and**<br>**formal**|**Trained model**|**Training-free**<br>**model**|**Model-intrinsic**||
|_a claim about the behavior_|||||||
|task success|HIL-SERL (48)|MimicGen (58),<br>Eureka (59),<br>SimpleVLA-RL (12)|RECAP (40),<br>RoboMonkey (15),<br>SuccessVQA (39)|WorldEval (18),<br>WorldGym (19)|MG-Select (17)||
|progress|reward<br>sketching (35)||VIP (31),<br>VLAC (67), Robo-<br>Dopamine (23)|GVL (30),<br>TOPReward (33)|VIPER (76),<br>Sentinel (27)||
|safety, constraint|ThriftyDAgger (81),<br>HG-DAgger (82)|PNCBF (28),<br>RTD (50),<br>SafeManip (37),<br>ConformalSTL (56)|RealTimeVerif (83)|GRAPE (71)|LS3 (75), latent<br>safety filters (42)|2–3<br>4–6<br>7–11<br>12+|
|execution quality||RINSE (62),<br>Video2Reward (84)|RECAP (40), Robo-<br>Dopamine (23)|GRAPE (71)||none<br>1|
|human preference|PEBBLE (43),<br>RoboArena (36),<br>B-Pref (44)||Robometer (21)||||
|_a claim about the policy_|||||||
|failure, uncertainty|ThriftyDAgger (81),<br>Sirius (46)|Code-as-<br>Monitor (25)|Foresight (85),<br>AHA (86),<br>RoboFAC (87)|KnowNo (68),<br>FOREWARN (88)|SAFE (26),<br>Sentinel (27)||
|_a claim about the training da_|_ta_||||||
|training value of a<br>demonstration|Sirius (46)|RINSE (62)|Re-Mix (9),<br>DataMIL (11),<br>Demo-SCORE (10)||||


**Table 1** What the score asserts, plotted against the judge source supplying the criterion. Each cell names representative systems, and the fill depth is the number of papers there. Each paper is counted in exactly one judge-source column, and a paper asserting two properties appears in both rows. 

#### **2.1 Comparing Trajectories** 

A human preference comparison presents two trajectory segments and asks which segment shows better task performance, and the output is therefore a relative judgment. RoboArena uses this judgment directly, conducting double-blind comparisons of fixed policies and aggregating the human preferences into a policy ranking (36). 

Preference-based learning uses the same interface as supervision for a scalable learned verifier. Christiano et al. (34) train a reward model from human comparisons and iteratively use the predicted rewards of that model to train a policy model. PEBBLE reduces the required human labels through unsupervised pre-training and by relabelling stored experience whenever the reward model changes (43). B-Pref replaces people with simulated teachers whose controlled irrationalities test the robustness of preference-based reinforcementlearning algorithms (44). Across these methods, the interface remains pairwise, but the judge source moves from direct human judgment to a learned or simulated proxy. 

#### **2.2 Scoring Trajectories** 

Instead of comparing two trajectories, a person can provide scalar feedback by assigning a numerical score to each time step in a single trajectory. Cabi et al. (35) call this annotation procedure reward sketching. The annotator draws a curve with values from 0 to 1 over the timeline of a recorded robot trajectory, while the tool displays the video frame corresponding to the current point on the curve, and the curve therefore records perceived progress toward the target task frame by frame. A small set of these curves trains a reward model that then scores every time step of a much larger corpus. 

5 


**Figure 2** Four roles of the human verifier. A person can compare trajectories (§2.1), assign scalar or time-indexed scores (§2.2), or intervene during execution (§2.3). The first three roles judge policy behavior, and the fourth validates generated rollouts and the verifiers applied to them (§2.4). 

#### **2.3 Intervening During Execution** 

During execution, a human supervisor can watch the system and take over the controls when the policy model is about to act incorrectly. The intervention methods below split by who decides that the moment to take over has come, a person in the human-gated setting and a learned verifier in the robot-gated setting. 

In the human-gated setting, the person decides when autonomous control stops and supplies corrective actions. The intervention serves two purposes. An intervention can prevent an unsafe or unproductive action before that action causes failure, and it provides a corrective training example at a state where the policy model needs help. HG-DAgger studies this interaction in simulated and real-world autonomous driving (82), extending the correction-collecting loop of DAgger to a supervisor who chooses the moments (89). The driver takes over in unsafe states, and the corrective actions become demonstrations for training the policy model. Although the training-time interventions of HG-DAgger remain human-gated, HG-DAgger also calibrates a threshold on the policy’s own uncertainty using the states where the driver took over, and the trained policy model can therefore flag comparable states on its own. HACO applies human-gated interaction to simulated autonomous driving, using partial demonstrations to shape a proxy value function that guides policy optimization while discouraging reliance on further interventions (45). Sirius applies human-gated intervention to real-robot manipulation during deployment. The operator takes over at difficult states, and the recorded interventions are weighted by the robot’s past reliability at that state before entering the policy update (46). HIL-SERL keeps the operator in the loop through real-world reinforcement learning, where corrective takeovers enter the replay buffer alongside demonstrations and drive precise manipulation tasks to near-perfect success within a few hours (48). 

Continuous human monitoring is costly, and robot-gated methods therefore automate the intervention decision. In simulated and physical manipulation tasks, ThriftyDAgger uses a switching policy between robot and human control to request help when the current state is unfamiliar or likely to lead to task failure, subject to a human-intervention budget (81). AIM learns a proxy Q-function that approximates the human intervention rule and requests assistance when the learned proxy value indicates the policy model’s action deviates from the expert’s action, tested in autonomous-driving and grid-world navigation simulations (90). Sirius-Fleet moves the same decision to a deployed fleet, where visual world models predict failure ahead of time and the thresholds are relaxed as the policies improve (47). In both settings the person still supplies the corrective 

6 

actions. An intervention verifier must request help early enough to avoid failure but selectively enough to limit human effort. 

#### **2.4 Validating Generated Rollouts** 

The first three roles judge the behavior of a real robot. The fourth role judges a generated rollout, produced by a world model or a simulator in place of a real execution. Reading such a rollout takes two judgments, one on the task success of the policy that acted and one on the fidelity of the video the world model produced. The person is asked whether the rollout ends in the same success or failure that the real execution would have reached, and we call this property outcome preservation. GigaWorld-1 asks for both judgments in one number. Annotators rate long-horizon generated rollouts on a four-level World Model as Evaluator Score, which reads task success together with video fidelity (20). A fine-tuned vision-language model then reproduces these ratings across a corpus too large for any annotator to watch. VeoEval keeps a person as the judge of each generated rollout. VeoEval runs policies inside a Veo world simulator over nominal, out-of-distribution, and red-teaming conditions, and a person scores the success of each generated rollout (49). When outcome preservation fails, a generated rollout shows the task succeeding where the robot would have failed, and the policy then looks better than its real performance. The reference for outcome preservation is the outcome that the real execution would have reached, and with no real rollout available, a person reads the reference directly. A model tuned on the person’s judgments then applies that reference at scale. 

Across all four roles, the human verdict becomes supervision for a cheaper verifier. Comparisons and scores train reward models, interventions enter the replay buffer as corrective demonstrations, and ratings of generated rollouts train the model that rates the rest of the corpus. The cost of each substitution depends on how far the cheaper verifier’s training data is from the data the verifier is later applied to (§6.1). 

## **3 Rule-Based and Formal Verifiers** 

A rule-based or formal verifier applies a criterion written before the run, and therefore returns a verdict without asking a person at inference time. We group these procedures by what the criterion reads, a full trajectory (§3.1), a terminal state (§3.2), or a physical constraint (§3.3). Figure 3 shows the three groups, and Table 2 names the seven methods those groups contain. 

|**Method**|**Core Characteristic**|**Representative Work**|
|---|---|---|
||_Full-trajectory Verification_||
|Temporal-Logic Scoring (§3.1.1)|Quantifies**_how much_**a trajectory satisfies a formal<br>specification|ConformalSTL (56), TGPO (38)|
|Geometry-Based Scoring (§3.1.2)|Returns a**_smoothness_**score and a**_self-similarity_**<br>score against a smoothed version of the trajectory<br>itself|RINSE (62)|
|Model-Written Rules (§3.1.3)|LLM**_writes_**the verification code, ranked by a task<br>metric or only tested for execution|Eureka (59), Code-as-Monitor (25)|
||_Terminal-state Verification_||
|Goal Predicate (§3.2)|A**_true/false_**check on the final state, simulation<br>only|LIBERO (57), CALVIN (55)|
||_Physical-constraint Verification_||
|Invariance Certificate (§3.3)|A**_formal proof_** that holds for all possible<br>trajectories|PNCBF (28)|
|Reachability Check (§3.3)|A**_per-trajectory_**check of whether the robot’s<br>reachable states intersect an obstacle|RTD (50), ARMOUR (61)|
|Symbolic Feasibility (§3.3)|A**_pre-run check_**that a plan is physically possible|Text2Motion (91)|


**Table 2** Seven verification schemes with representative works. 

7 

### **Rule-Based and Formal Verifiers** 


**Figure 3** Overview of rule-based and formal verifiers. Full-trajectory methods (§3.1) score complete rollouts using temporal-logic specifications, trajectory geometry, or model-written code; terminal-state methods (§3.2) check whether the final state satisfies the goal; and physical-constraint methods (§3.3) verify safety through an invariance certificate or a reachability check on each candidate trajectory, and feasibility through a symbolic check before anything moves. 

#### **3.1 Full-Trajectory Verification** 

Trajectory-level verification methods process full state sequences. Three types appear, hand-written temporallogic scoring (§3.1.1), geometry-based trajectory scoring (§3.1.2), and model-written verification code (§3.1.3). 

##### **3.1.1 Temporal-Logic Scoring** 

Temporal-logic scoring is the trajectory-level method appearing most often in the work we cover. The method states the criterion as a formal specification and scores a trajectory by its distance from satisfying that specification. A specification states the required behavior and its timing, in a formal language a program can check a run against. This literature writes specifications in Signal Temporal Logic (STL), and the score is a real number called the satisfaction margin: 


The margin is positive when the specification is satisfied and negative when it is violated, and the magnitude of the margin gives how close the trajectory ran to the boundary. If the specification says “the gripper must close within 0.25m of the table”, closing at 0.1m gives a positive margin and 0.3m a negative margin, and 0.05m scores higher than 0.2m because it leaves more room. This quantity is called robustness in the temporal-logic literature. 

8 

The same satisfaction margin applies to a pre-recorded execution (37), to a simulated rollout (38), and to a future trajectory predicted by a trained model (56). The margin is computed the same way for every rollout source. Practical systems differ in one respect, whether an extra calibration step is added on top of the raw satisfaction margin. 

**Calibrated predictive runtime verification.** Predictive runtime verification calibrates the satisfaction margin with conformal prediction (56, 92). Conformal prediction is a method that attaches its own margin to the output of any predictor. The method runs the predictor on a held-out set with known outcomes, records the size of the resulting errors, and takes a quantile of those recorded errors as the margin carried by every later prediction. For example, a margin set at the ninety-fifth percentile of the held-out errors gives an interval that contains the true outcome in ninety-five percent of later cases. The bound holds for any predictor and any data distribution, as long as the held-out cases and the cases judged later are drawn from the same pool, so the order of the two sets carries no information about their errors. Drawing both from the same pool is the condition called exchangeability, and §6.3 shows how training a policy against a verifier breaks that condition. In Lindemann et al. (56), the trajectory predictor is treated as a black box and predicts future states from current observations. The calibrated error bounds of that predictor become an interval on the satisfaction margin, and the system can therefore warn that a specification is about to be violated several time steps in advance. 

Two extensions carry conformal bounds on the satisfaction margin into settings the original method excludes. First, robust conformal prediction handles a distribution shift between calibration and deployment (93). Second, a distributionally-robust version extends the approach to spatio-temporal specifications (92). A related method keeps the calibration and drops the specification. Nath et al. (94) work in the latent space of a world model, where they conformally calibrate the dynamics-prediction error and a learned safety-classifier score. The calibrated bounds build a robust constraint set for model-predictive control, and safety constraints are therefore enforced during closed-loop execution from pixels. 

**Uncalibrated specification evaluation.** Specifications can also be used without any calibration layer, either as an offline monitor or as an optimization reward. SafeManip defines temporal safety properties in Linear Temporal Logic over finite traces (LTLf), a logic for specifying sequences of discrete events over a finite time horizon. SafeManip compiles each property into an automaton and checks pre-computed simulation rollouts against these automata (37). The output is a boolean violation with a timestamp and duration. These safety properties read the simulator’s state directly, and the same checks on hardware therefore require perception, which SafeManip leaves for future work. 

When exact ground-truth states are available, the satisfaction margin can be used directly as an optimization reward, providing a dense learning signal at every time step of policy training. TGPO decomposes an STL formula into subgoals and invariant constraints, and builds a staged dense reward from them, solving the sparsity problem that makes specification-driven learning difficult (38). Cycle experience replay compiles LTL into an automaton and shapes a dense reward from its accepting cycles (95). 

##### **3.1.2 Geometry-Based Scoring** 

Geometry-based scoring reads the spatial shape of the trajectory alone, and no task specification has to be written by hand. This method applies wherever a set of recorded demonstrations is available. 

RINSE scores each demonstration with two geometric measures. Spectral arc length gives a smoothness score that penalizes high-frequency jitter, and trajectory envelope distance gives a self-similarity score, measuring how far the trajectory deviates from a Bézier-smoothed version of itself. Both scores are reference-free and need no other demonstrations to compare against. RINSE trains on the highest-scoring subset and performs better than training on the full set (62). 

Spectral arc length and envelope distance measure execution quality rather than task success, and a smooth trajectory can therefore still fail the task while a jerky trajectory can succeed. RINSE’s scores agree closely with the mixture weights that Re-Mix learns over a heterogeneous corpus (§4.3). These two scores therefore 

9 

serve as a lightweight filter over training data, and a separate check has to determine whether the task was completed. 

##### **3.1.3 Model-Written Rules** 

A model writes the verification logic itself. The generated code is used in two ways, as a training objective and as a runtime check. 

**Optimization.** A model asked for a reward function produces code, and a search loop keeps the candidates that train a good policy. Eureka runs the loop (59). Eureka reads the environment code and a task description, writes candidate reward functions in Python, trains a policy with each candidate, ranks the candidates by the environment’s own ground-truth task metric evaluated on those training runs, and mutates the best candidate, repeating the cycle. Ranking candidates by the task metric checks the generated code against what the task requires, and the monitoring systems below have no equivalent check. The reward Eureka converges to outperforms human-written rewards on most tasks in a large benchmark. DrEureka adds safety instructions and automatic domain-randomization ranges so the learned reward transfers to real hardware (96). Text2Reward and language-to-rewards generate dense reward code from natural language descriptions, using iterative human feedback instead of an evolutionary loop (97, 98). Video2Reward derives rewards for legged robot behavior from video instead of text (84). 

**Monitoring.** Code-as-Monitor uses a multimodal model to generate a spatio-temporal constraint verifier, and applies geometric abstractions of the constrained elements to keep the check fast enough for the control loop (25). Code-as-Monitor tests each generated verifier before use, to confirm that the generated code runs. ReKep uses a model to express manipulation goals as relational keypoint constraints, which a solver then optimizes into end-effector motion at control rate (60). Neither Code-as-Monitor nor ReKep checks the generated constraint against what the task requires. 

#### **3.2 Terminal-State Verification** 

A goal predicate is a simple true/false test on the final state. A goal predicate is a formal criterion like the temporal-logic specifications of §3.1.1, but it reads only the last state and returns a bit rather than a margin. Such a predicate needs the object’s pose, which a physics engine reports exactly but perception only estimates, so this method is confined to simulation. The same cheap test scores benchmarks, generates training data, and supplies reinforcement learning rewards. 

**Benchmark evaluation.** A goal predicate appears in policy benchmarks as the built-in success check. LIBERO defines the goal of each task as a predicate over simulator state, evaluates that predicate as the episode runs, and reports the fraction of episodes the predicate accepts, across four suites that vary spatial layout, objects, goals, and combinations of all three (57). Most of the reinforcement learning and test-time selection results in this survey are measured on LIBERO, and the sparse reward those runs optimize is exactly this success bit. CALVIN chains five language-conditioned subtasks and counts the number completed in order (55). VLABench and GenManip split the predicate into stages for the same reason, so that a long-horizon policy earns partial credit for the stages the policy did reach (99, 100). RoboCasa builds 100 kitchen tasks on the same simulator with generated scenes and assets (101). RoboVerse unifies embodiments and environments across simulators (102). ManiSkill provides parallelized simulation (103), and Isaac Lab-Arena runs a whole evaluation the same way, and the number of trials therefore stops being set by how long a robot takes to run one trial (104). RoboTwin adds strong domain randomization to a bimanual setting (105). BEHAVIOR-1K extends the task distribution toward everyday activities (106). THE COLOSSEUM holds the task fixed instead and reads one predicate under a fixed set of perturbations to appearance, lighting, and background (107). Each predicate is written once and then determines every result the benchmark produces, and an error in the predicate therefore affects the ranking of policies. A policy benchmark reports the policy’s success rate, and the error rate of the check behind that number is reported far less often (§6.1). 

10 

**Synthetic data generation and filtering.** A boolean check on exact simulator state costs almost nothing to run, so the same check can generate training data as well as verify it. MimicGen runs this generate-andverify loop (58). MimicGen takes a small number of human demonstrations, breaks each demonstration into object-centric segments, adapts those segments to new object poses to generate thousands of trials, runs the trials, and keeps only the trials that pass the task-level success check. Generation and verification are the same loop, and the predicate makes the loop run automatically. DexMimicGen uses the same approach for bimanual dexterous manipulation (108). DemoGen targets real hardware instead, where running the generated trials to verify them is expensive, and synthesizes spatially augmented point-cloud observations without running or checking any trial (109). 

Three systems move the task design itself into the loop. GenSim uses a language model to write simulation task code and expert demonstrations, and keeps a candidate task only if a single-task policy trained on that task achieves a success rate above a threshold (110). GenSim2 scales this method to articulated objects with a multimodal planner (111). RoboGen automates task proposal, scene construction, and supervision generation, and its authors note that verifying the resulting skills at scale remains an open problem (112). 

**Sparse reward for reinforcement learning.** A goal predicate also serves as a reinforcement learning reward, one bit per episode. SimpleVLA-RL shows this most directly (12). SimpleVLA-RL runs Group Relative Policy Optimization (GRPO) on a VLA model, uses the simulator’s success check as the only reward, and provides the parallel rendering and exploration changes needed to keep training stable. A policy initialized from just one trajectory per task then reaches near-perfect performance. RIPT-VLA achieves a similar result with leave-one-out policy-gradient estimation on the same sparse binary reward, deliberately avoiding shaped rewards, value functions, and reward models (13). RLinf-VLA provides the infrastructure for running such training across different algorithms and benchmarks (14). ConRFT applies a similar construction to real-world fine-tuning, substituting a binary classifier trained on human-labeled demonstrations for the simulator predicate. ConRFT combines behavior cloning and Q-learning in one objective under a consistency policy, shifting the weight from behavior cloning to Q-learning as training moves from offline to online (113). 

The predicate needs exact object pose, and the same question on hardware therefore requires a different verifier, where pretrained multimodal models have become the default (§4). The predicate also reads only the final state, and a run can satisfy the predicate exactly and still fail the task. A policy trained against such a check learns to aim at exactly the runs that satisfy the predicate without doing the task, a pattern demonstrated so far on LLM verifiers for inductive-reasoning tasks rather than on robot policies (114). Skalse et al. (115) define this failure mode and Manheim and Garrabrant (116) categorize its variants, and §6.3 examines how a robot verifier is measured against this failure mode. 

#### **3.3 Physical-Constraint Verification** 

Physical-constraint verification requires that the robot and the surrounding objects stay where they are allowed to be. For example, the arm must not touch the person standing next to the robot, and the cup at the edge of the table must not be pushed off. Three methods appear below, ordered by how many trajectories one verdict covers. First, an invariance certificate takes an analytical model of the system dynamics and tests whether the robot can be kept out of unsafe states. The proof covers every trajectory those dynamics can produce. Second, a reachability check computes the states the robot can reach while following a plan, either one candidate trajectory or a family of plans analyzed in advance. The verdict covers the plans that were analyzed. Third, a symbolic feasibility check takes the preconditions of each action and tests whether a plan is physically possible at all. It answers before any trajectory exists. 

**An invariance certificate that holds for every trajectory.** The certificate here is a control barrier function (117), a mathematical tool that takes the dynamics model and keeps the robot inside a safe set, the region of states the robot is allowed to occupy. The barrier function proves that a robot starting inside the region stays inside the region under the closed-loop dynamics, a property called forward invariance, and the guarantee therefore holds for every trajectory those dynamics can produce. So et al. (28) construct such a function from the value function of a nominal policy, and the result is a filter that makes any policy safe. A filter of this kind monitors the control input that a policy proposes and overrides that input when the input would leave the safe set, a construction that also covers predictive filters solving a short constrained optimization over a fixed 

11 

horizon at every control step (52, 118). The theorem applies to the exact value function. A neural network approximating that function carries the same guarantee only when a separate verification step checks the descent condition, and the experiments in So et al. (28) do not perform that step. Tan et al. (119) identify value functions with control barrier functions directly, and supply the verification step that PNCBF’s experiments skip. A theorem there extends the guarantee to an _𝜖_ -optimal approximate value function, and validity and coverage metrics check a learned approximation against that theorem. 

**A reachability check on each candidate trajectory.** The check here reads one candidate trajectory and tests whether the robot’s reachable states intersect an obstacle. The methods below differ in where the candidate comes from, running from a family of trajectories analyzed before the robot runs, to the trajectory a planner intends to execute, to the action a policy proposes while it trains. 

Before the robot runs, reachability-based trajectory design (RTD) computes every state the robot can reach while tracking any trajectory in a family described by a few parameters, with the tracking error of the controller included (50). At run time, the sensed obstacles are mapped through these precomputed states into constraints on the trajectory parameters, and the planner optimizes only over parameters that satisfy them, fast enough to fit inside the planning loop. Every trajectory in the family ends by braking to a stop, so when no candidate passes, the robot finishes its previous verified plan and stops. The computed set is conservative, so a candidate that is in fact safe can be rejected. Later methods apply the same computation to a manipulator with uncertain mass and inertia (61) and to full vehicle dynamics (120). PARC instead works backward from the goal, underapproximating the set of initial states and plan parameters from which the robot is guaranteed to reach the goal and avoid the obstacles, tightly enough that goal reaching stays feasible in a narrow gap (121). NeuralPARC extends that computation to a black-box robot by fitting a ReLU network to its trajectory data (122). Chou et al. (123) compute a reachable set of the same kind when the state is estimated from images, adding a bound on the error of a learned perception module that holds with high probability in a trusted domain near the training data. This family of parameterized plans verified before the robot runs is closely related to formally verified maneuver automata, in which each motion primitive is verified by reachability analysis (124). 

Fail-safe motion planning checks the trajectory a planner intends to execute (125). The planner executes that trajectory only while a second trajectory branching off it can bring the vehicle to states from which the vehicle stays safe for all future time, and a convex optimization finds that second trajectory online in dense urban traffic. When the obstacle is a person, SaRA computes the positions the person can reach within the planning horizon (53). 

A safety layer checks the action a policy proposes while it trains, so the verifier stays in the loop for the whole run. Thumm and Althoff (126) train a manipulation policy next to a person, in simulation with recorded human motion. The layer allows an action only if the arm can still come to a full stop before the person can enter the arm’s range, and brings the arm to that stop otherwise. Because safety-critical collisions no longer end the episode, the layer also improves the learned policy. RTS precomputes reachable sets in the same way as RTD and puts them in the loop, checking the trajectory parameter the agent picks and replacing it with a safe parameter when the check fails (51). BRSL computes the reachable states directly from data, without a model of the robot (54). Continuous action masking gives the policy the whole set of allowed actions rather than a verdict on a single action, and reports that focusing exploration this way also speeds up training (127). The allowed set is a safe action set in some of its tasks and a task-knowledge constraint in others. 

**A symbolic feasibility check before anything moves.** Symbolic feasibility checking tests whether the preconditions and affordances (the action possibilities offered by the environment) of a candidate plan can be satisfied (128). Such a check catches plans that sound reasonable but are physically impossible, before anything moves. A line of work called task and motion planning puts the check between a symbolic plan and the motions that realize the plan, and returns the plan to the symbolic layer when no motion satisfies it (129). Text2Motion applies the same test to plans that a language model proposes, scoring a candidate skill sequence by whether the policies for those skills can execute that sequence (91). The coverage of Text2Motion is limited by the symbolic abstraction it uses, and that abstraction is maintained by hand. 

12 

|**Applications**|**Trained verifier**|**Pretrained verifier**||
|---|---|---|---|
|Evaluating behaviour and policies<br>(§4.1)<br>Inference-time verification and<br>scaling (§4.2)|VIP (31), Robometer (21),<br>AHA (86), RoboFAC (87),<br>AutoEval (130)<br>RoboMonkey (15), RoVer (131),<br>Foresight (85), AHEAD (132)|GVL (30), TOPReward (33),<br>WorldEval (18), WorldGym (19)<br>KnowNo (68), FOREWARN (88)|1<br>2–3<br>4–6<br>7–11<br>12+|
|Feeding verifier feedback into<br>policy learning (§4.3)|RECAP (40), VLA-RL (133),<br>Demo-SCORE (10), RoboCat (66),<br>Re-Mix (9), SCIZOR (134)|SRPO (72)|none|


**Table 3** Verifier-based methods are organized along two complementary dimensions. The application role is evaluating behavior and policies, inference-time verification and scaling, or feeding verifier feedback into policy learning. The model source is task-trained or used directly from pretraining. Fill depth indicates the number of unique papers in each cell. 

## **4 Learned and Pretrained Verifiers** 

A learned or pretrained verifier returns its score from a forward pass of a neural network. Those networks come from two sources of supervision, training on task-specific robot data and pretraining alone, and Table 3 counts the papers under each source. The two sources call for different evidence that the verifier is right. A verifier trained on task-specific robot data can be compared with real outcomes on the robot the verifier will be used on, and a verifier that comes from pretraining alone has to transfer across embodiments and task distributions before any such comparison exists (§6.1). 

A learned or pretrained verifier appears in three roles, shown in Figure 4 and set side by side in Table 4. Such a verifier measures the performance of an execution or a policy (§4.1), picks among candidate actions, skills, or plans at inference time (§4.2), and feeds a score back into policy training or into the choice of training data (§4.3). 

|**Application subsection**|**Axis**|**Distinguishing feature**|
|---|---|---|
|Evaluating behavior and policies<br>(§4.1)<br>i|Evaluation|Measuring an execution at process or trajectory level|
|Inference-time verification and<br>scaling (§4.2)<br>i|Decision|Selecting the best action, skill, or plan during inference|
|Feeding verifier feedback into<br>policy learning (§4.3)|Optimization|Using scores to optimize the original policy|


**Table 4** The three applications of learned and pretrained verifiers and the distinguishing axes. 

#### **4.1 Evaluating Behavior and Policies** 

Models that score robot execution can be organized at two levels, set by the granularity of their outputs. A process-level verifier assigns a temporally localized score or categorical judgment to a state, transition, short clip, trajectory prefix, or bounded subtask. A trajectory-level verifier returns one holistic score or verdict for a completed rollout. Policy evaluations and rankings are then obtained by aggregating these outcomes across repeated rollouts. 

**Process-level scores within a rollout.** VIP learns an action-free, goal-conditioned value representation from human videos and derives dense, smooth rewards for unseen robotic tasks (31). LIV extends this formulation to goals given as either language or an image, and assigns a dense reward to each frame (32). Robo-Dopamine learns a general-purpose, step-aware process reward model from multi-view inputs (23), while ProcVLM grounds frame-level progress estimates in procedural stages and within-stage visual change (135). Robometer combines frame-level progress supervision with trajectory-comparison preference supervision, and the resulting reward stays available inside a rollout (21). VLAC outputs a dense progress increment together with a done signal from paired observations and a language goal (67). Large reward models scale the same dense per- 

13 


**Figure 4** Overview of how learned and pretrained verifiers are used in robot learning. They evaluate behavior and policies at process or trajectory level (§4.1), guide inference-time selection directly or through predictive lookahead (§4.2), and provide feedback for policy optimization and data curation (§4.3). 

frame reward, training one frame-level reward generator across two dozen data sources and using the frozen generator to refine a policy online in a closed loop (136). PRM-as-a-Judge turns a dense score of this kind into an evaluation protocol, on the argument that one success bit collapses the execution behind that bit (137). PRM-as-a-Judge reads policy execution from trajectory video and reports an outcome, a progress score built on a task-aligned potential, and a diagnosis. 

Pretrained VLMs can also provide localized feedback without requiring a separately trained robot reward model. Rocamonde et al. (70) establish the construction, using the similarity between a frame and a language description of the goal under a frozen vision-language model as the reward, and RoboCLIP builds the same similarity score from a single demonstration video but assigns that score once, as a sparse reward at the end of the episode, rather than to each frame (138). GVL presents shuffled trajectory frames to a frozen VLM and autoregressively predicts a task-completion percentage for each frame, producing in-context value estimates at frame level (30). TOPReward converts the likelihood of an affirmative completion token for a video prefix into a dense, instruction-conditioned reward and also supports terminal success detection (33). Other methods learn localized categorical judgments. SuccessVQA accepts a single image or short video clip, classifies each clip for success, and only subsequently consolidates the clip predictions into an episode-level decision (39). AHA, after being instruction-tuned on a large synthetic dataset of failure trajectories, predicts a binary success condition for the current subtask from the keyframes observed up to the subtask and generates a failure explanation when the prediction is negative (86). AHA follows REFLECT, which summarizes a robot’s sensory record into a hierarchy and lets a language model query it to explain a failure and propose a correction (69). 

14 

**Trajectory-level outcome judgments.** RoboFAC takes a complete manipulation video and determines whether the task was successfully completed. On a failed video, RoboFAC localizes the failure to a substage and returns corrective guidance, which the authors show can be fed back to a running VLA policy in real time to improve real-robot task success (87). WorldEval uses a video-language verifier to assign one binary success label to each policy-conditioned generated rollout (18). WorldGym passes the generated frame sequence and task instruction to a VLM and returns one rollout-level reward, optionally using a task-specific partial-credit rubric (19). AutoEval executes a policy for a fixed trial horizon and applies a learned success classifier to the terminal state, producing one binary outcome for each unattended hardware trial (130). RobotArena ∞ translates recorded real scenes into simulation and scores the rollouts that a policy produces there with a vision-language model (139). For generated rollouts, GigaWorld-1 presents a complete synchronized multi-view video to a tuned VLM, which outputs one ordinal World Model as Evaluator Score together with supporting rationales (20). The World Model as Evaluator Score reads video fidelity together with task success (§2.4). 

#### **4.2 Inference-Time Verification** 

At inference time a verifier can choose what the robot does next. The system generates several candidate actions, skills, or short-term plans, scores the candidates with the verifier, and executes the highest-scoring candidate. 

**Direct candidate selection.** RoboMonkey samples and perturbs policy outputs, scores the candidates with a multimodal verifier, and finds that action error falls as an exponentiated power law in the number of samples (15). RoVer adds an external test-time verifier and improves inference performance with the policy weights left frozen (131). Three further systems spend more computation at test time, on task-progress scoring, on an adaptive critic over relative actions, and on a general framework for scaling embodied inference (140, 141, 142). SayCan evaluates the candidate skills before execution (65); KnowNo uses conformal calibration to construct a prediction set over candidate actions and requests human assistance when multiple actions remain plausible (68). V-GPS uses a value function learned through offline reinforcement learning to re-rank action chunks generated by a frozen generalist policy (16). 

**Predictive lookahead with world models.** These methods use a world model to look ahead from the current state, either scoring candidate actions by their predicted consequence or monitoring the consequence of the chosen action. AHEAD rolls a motion-aware latent world model forward once to predict future scene tokens rather than candidate actions, and estimates uncertainty from the variance across five sampled rollouts before feeding the predicted tokens to a frozen action decoder (132). FOREWARN aligns a latent predictive model with a vision–language model, enabling the system to make semantic judgments about predicted outcomes and guide policy selection accordingly (88). Critics trained on a policy’s own successes and failures score the video-model-predicted terminal frames of fine-grained candidate actions (143). Unlike these methods, Foresight does not compare candidates. Foresight reads the latent representations of an action-conditioned world model to monitor the single action block the policy has committed to, detecting potential failures in long-horizon manipulation tasks and conformally calibrating these predictions using trajectory-level labels (85). 

#### **4.3 Feeding Verifier Feedback into Policy Learning** 

Verifier feedback can also change the policy itself, by entering the training objective or by deciding which data the policy is trained on. 

**Direct reward optimization.** The verifier’s output becomes a reward, an advantage, or a preference objective, and the policy parameters move with that output. RECAP trains a value function using demonstrations, onpolicy rollouts, and teleoperated interventions, and then extracts a policy through advantage conditioning. At deployment scale, RECAP more than doubles system throughput and roughly halves the failure rate on the most challenging household tasks (40). GRAPE decomposes tasks into stages, constructs a cost function for each stage, and trains the policy through trajectory-level preference optimization (71). RL-VLM-F trains a reward model from preferences provided by a multimodal model (144), a construction that Motif introduced by distilling a language model’s preferences over event captions into an intrinsic reward (145), whereas 

15 

VLA-RL fine-tunes a multimodal backbone into a process reward model that scores automatically extracted task segments (133). 

Some methods derive optimization signals purely from a world model’s latent representations, without decoding a video. SRPO compares states in a pretrained latent world model to construct a progress-shaped reward and can assign credit to useful behavior within failed trajectories (72). World value models put a value head on a world-model backbone instead of a vision-language backbone, on the argument that a backbone without temporal modeling cannot order states along a task (146). EVA instead generates a full video from the world model and rewards the policy for predictions from which an inverse dynamics model can recover executable actions (147). VLA-RFT performs reinforcement fine-tuning in a world simulator using verified rewards (148). Although these methods use world-model latent representations, as predictive lookahead does, their final purpose is to update policy parameters rather than to select the next action to execute. 

**Self-improvement and rollout filtering.** A verifier decides which newly generated rollouts re-enter training. That decision closes a generate-filter-train loop, and the policy improves on its own experience. Demo-SCORE learns to distinguish successful from failed rollouts and filters a heterogeneous demonstration set before retraining (10). RoboCat fine-tunes on a new task, generates its own interaction experience, and uses a verifier to select the experiences that enter subsequent training (66). Self-improving embodied foundation models derive both a reward function and a success detector from steps-to-go prediction, enabling autonomous practice with improved sample efficiency (149). Human-in-the-loop online rejection sampling combines corrective interventions with a reward-aware data filter on contact-rich tasks (150), while real-time verification scores intermediate results as embodied reasoning is generated and uses the verified reasoning data for subsequent skill learning (83). 

**Data curation and demonstration scoring.** A curation method scores, filters, or reweights a corpus recorded before the current policy existed. The property these methods score is the training value of a demonstration, the contribution that demonstration makes to the policy trained on it. The three groups below differ in the evidence they read for that contribution. 

The first group reads the demonstration by itself. DemInf scores a trajectory with a mutual-information estimate over its observations and actions, a quantity falling when the recorded actions look arbitrary given the robot’s observations (151). ILEED attributes quality to the person who recorded the trajectory and estimates each demonstrator’s expertise (64). DWBC trains a discriminator to separate expert demonstrations from the rest and weights each sample by the discriminator’s output (63), and DemoDICE keeps matching the expert distribution while still drawing on imperfect demonstrations (152). 

The second group reads the corpus around the demonstration. Re-Mix learns mixture weights over Open X-Embodiment (153), a corpus aggregated across embodiments and protocols. Re-Mix optimizes the worstperforming domain, so the weight a sub-dataset receives does not follow from its size, and the result outperforms uniform mixtures and hand-specified compositions (9). SCIZOR combines a self-supervised progress estimator that flags suboptimal sub-trajectories with a deduplication module that drops segments repeating what the corpus already holds, and ablations show the progress estimator contributes more of the two (134). 

The third group reads the policy the data produces. DataMIL fits datamodels that estimate the contribution of one training example to downstream performance, without running a new robot rollout (11). Curation needs this third quantity, and this quantity is also the most expensive to obtain, since it is defined through a training run. All three groups change the corpus. A policy can instead keep the corpus and take the demonstration’s training value as an input, training on the weaker demonstrations with a label that marks them and conditioning at test time on the behavior to follow (40). _𝜋_ 0 _._ 7 does the same with manually annotated quality and mistake labels in place of a trained value (5). Curation and conditioning need the same score, and only curation has to commit to that score before training begins. Two results bound the reach of any such score. The first distinguishes action divergence from transition diversity and finds that state diversity helps only in some settings (154), and the second finds that corpus composition matters more as the corpus grows (155). 

16 

#### **Model-Intrinsic Verifiers** 


**Figure 5** Model-intrinsic verifiers use information from a robot’s own policy or world model to evaluate behavior and guide task selection. Policy-based self-verification detects failures and selects candidates, prediction-based outcome verification judges a candidate by the outcome the world model predicts, and task selection prioritizes the next training environment, all without an independent external verifier. 

## **5 Model-Intrinsic Verifiers** 

A model-intrinsic verifier reads a quantity that the robot’s own policy or learned world model already computes, and we call that quantity a model-intrinsic score. _Policy-based self-verification_ reads the policy, either to detect a failure while an execution runs or to choose among candidate actions before one is executed (§5.1). _Predictionbased outcome verification_ reads a learned world model and judges a candidate by the outcome that the world model predicts for that candidate (§5.2). The same scores can then rank a whole task instead of a single action, and decide which environment the policy trains on next (§5.3). Figure 5 shows the three subsections. 

#### **5.1 Policy-Based Self-Verification** 

A robot policy produces more than its final action. The policy’s internal representations, the uncertainty or inconsistency in its action predictions, and the compatibility of the current observation-action trajectory with the training distribution can all provide evidence on whether the policy’s own behavior is reliable. Policy-based self-verification is used at two different stages. _Detection_ evaluates an ongoing execution and raises an alarm when the behavior begins to deviate from patterns associated with normal operation, often before failure becomes externally apparent. _Selection_ , in contrast, evaluates multiple candidate actions or trajectories before execution and chooses the candidate that the policy considers most reliable, without physically trying each alternative. 

**Verifying behavior during execution.** The detection methods below differ in the internal information they read and in the way that information becomes a failure prediction. SAFE provides a representative example (26). SAFE trains a lightweight predictor on the internal representations of a vision-language-action policy, motivated by the observation that successful and failed executions exhibit separable structure in the policy’s latent space, with failure-related patterns transferring across tasks. At runtime, the predictor maps the history of these representations to a scalar failure score, which is compared with a time-varying threshold calibrated 

17 

using functional conformal prediction. When calibration and test rollouts follow the same data distribution, this calibration bounds the probability of falsely flagging a successful rollout; however, the guarantee can fail under cross-task distribution shift, as calibration is performed on seen tasks while evaluation may involve unseen tasks. 

Other methods also read the policy’s own internal signals to judge whether the current execution is reliable, and these methods differ in the signal they read and in how the verifier is built. Sentinel monitors both action instability and task progress. Temporal inconsistencies in the policy’s action predictions are used to detect erratic behavior, while a separate VLM checks whether the task is still making progress (27). FIPER avoids failure examples by combining out-of-distribution signals from the policy’s observation embeddings with uncertainty in generated action chunks (156), and FAILDetect similarly learns only from successful rollouts, calibrating a time-varying conformal-prediction threshold band on their scores with a statistical guarantee on the false-positive rate (157). Tri-Info instead targets cross-policy transfer, scoring entropy and mutual information over states and actions, and the resulting measure therefore does not depend on a particular embedding architecture (158). HideAndSeek reduces the supervision requirement in another way, using only trajectory-level outcomes together with contrastive learning to identify which steps in a failed rollout carry failure signals (79). 

**Verifying candidates before execution.** MG-Select scores candidate action chunks by the change in their token probabilities when state and language inputs are masked, then executes the most input-dependent candidate (17). The base form of MG-Select needs no extra training and no external model, though the strongest results use a finetuned variant, and the method has only been evaluated on autoregressive policies with discrete action tokens. TACO instead selects candidates that are most familiar in the policy’s representation space, using a separately trained pseudo-count estimator while keeping the policy itself frozen (78). The central limitation of policy-based self-verification is that these scores measure whether a behavior looks reliable or familiar to the policy itself, not whether the task succeeded. A familiar-looking failure may therefore still receive a high score. 

#### **5.2 Prediction-Based Outcome Verification** 

A learned world model predicts how the environment may evolve. Those predictions can be used to evaluate whether an outcome is plausible, expected, or still achievable. Four model-intrinsic scores support such a judgment. _Trajectory likelihood_ measures how ordinary the trajectory looks to a video model, _latent discrepancy_ compares the predicted latent with the observed latent, _model uncertainty_ reads the disagreement inside an ensemble, and _reachability value_ says whether failure can still be avoided. 

**Trajectory likelihood.** VIPER scores a trajectory by its likelihood under a video prediction model (76). An autoregressive transformer is trained on expert video, and the prediction likelihoods become an action-free reward. The resulting agent reaches expert-level control across simulated control suites and manipulation tasks, and also demonstrates transfer across different arm–task combinations. Diffusion Reward instead uses the conditional entropy of a video diffusion model, based on the observation that conditioning on expert trajectories reduces generative diversity (77). A limitation of likelihood-based verification is that high generative likelihood does not necessarily correspond to semantically correct behavior under distribution shift. 

**Latent discrepancy.** A latent-discrepancy verifier encodes the observed outcome and compares the resulting latent with the predicted latent. Garrido et al. (159) use this discrepancy between predicted and observed latents to detect physical implausibility zero-shot, without training an additional detector. Garrido et al. (159) find that prediction in latent space performs substantially better than pixel-space prediction and than multimodal language models on this task. Within robotics, Foresight reads predicted latents of the same kind from an action-conditioned world model and trains a failure detector on those latents (§4.2). 

**Model uncertainty.** In model-based offline reinforcement learning, an imagined rollout is penalized in the regions where the learned dynamics model is uncertain. MOPO penalizes uncertain predictions from an ensemble of learned dynamics models (41). MOReL instead identifies unknown state–action pairs when an 

18 

ensemble of dynamics models makes inconsistent predictions (73). LOMPO extends this approach to the latent space of a trained model, allowing model uncertainty to be estimated from image observations (74). AHEAD reads the same ensemble disagreement inside a manipulation policy, taking the variance across five sampled latent rollouts as a per-step uncertainty and halting the lookahead once the variance exceeds a threshold (132). Ward et al. (160) calibrate the latent uncertainty of a compact action-conditioned world model and use that uncertainty to flag failures while the execution runs, and the detector therefore needs no failure examples of its own. Tested on a diffusion policy and on a real-world bimanual cable-manipulation dataset, a 570K-parameter version of the detector beats the next-best learned baseline by 3.8 points of failure-detection rate. 

**Reachability value.** A reachability value states whether failure can still be avoided from the current state under the predicted dynamics. Like the candidate scoring of §5.1, a reachability value judges an action before the action is executed. The judgment depends on the consequences the world model predicts rather than on how familiar the action looks to the policy. 

Nakamura et al. (42) implement this idea with a generative world model. A classifier first identifies observations that correspond to failure, while the world model predicts how different actions change future states. Hamilton– Jacobi reachability (161) then computes a value over these predicted dynamics, identifying states from which no available action can prevent a future failure. The resulting safety filter can therefore reject an unsafe action and switch to a safety-preserving action before the failure occurs. LS3 is an earlier, related construction from pixels (75). It learns a safe set from the states visited by earlier successful runs and constrains a model-predictive controller to plans that end inside that set. 

Follow-up work studies the behavior of this type of verification under partial observability, identifying errors from both state estimation and future prediction and proposing more conservative mitigation strategies (162). Three later methods change the quantity the filter is defined over. A parameterized latent constraint lets the unsafe region be set at run time rather than fixed when the filter is trained (80). An uncertainty term added to the value treats a state the model has not seen as a state to avoid (163). A learned control barrier function in place of the reachability value makes the filter intervene smoothly rather than switching (164). Lutkus et al. (165) give sufficient conditions under which a barrier function learned in a latent space keeps its guarantee on the original system, stated as an approximate conjugacy between the latent dynamics and the true dynamics. Gameplay Filters run the same forward reasoning in a physics simulator, evaluating safety by simulating interactions between a virtual adversary and the robot’s fallback policy (166). 

#### **5.3 Beyond Action Verification: Task Selection** 

A model-intrinsic score can also be read about a whole environment instead of a single action, and the score then decides which environment the policy trains on next. ACCEL scores each environment by the positive value loss of the policy running in it (167). The value loss is how much the policy’s own value function underestimates the return the policy actually received. The environments with the highest score are kept and edited further, and training therefore moves toward the environments the policy still misjudges. The quantity ACCEL’s score approximates is regret, which PAIRED introduced as the difference between the return a second agent achieves in an environment and the return the policy under training achieves (168). Measuring regret as this difference needs two agents run in the same environment, and the value loss instead obtains a proxy for regret from the single policy that is already running. Neither method was evaluated on a robot. PAIRED runs on grid-world maze navigation and a MuJoCo hopper domain, and ACCEL adds lava grids and a continuous-control walker. In each case the score decides the next environment to roll out, and says nothing about whether a completed behavior succeeded. 

Across the three subsections of Section 5, the model-intrinsic score comes from a model the robot is already running rather than from a separate verifier built to check that model. Taking the score from the model itself makes these scores the cheapest verifiers in this survey, and it also means the model gives a high score to a failure the model does not recognize (§6.3). 

19 

|**Use**|**How candidates arise**|**Requirement on the verifier**|**Cost of error**|
|---|---|---|---|
|Curation|fixed corpus, verifier unseen|average accuracy, split by error<br>type|a false positive trains on failure|
|Ranking and<br>off-policy evaluation|non-adversarial sampling|average accuracy, calibration|the wrong checkpoint ships|
|Training reward|closed loop, actively searched|no exploitable region|the policy satisfies the verifier without<br>doing the task|
|Runtime gating|closed loop, millisecond<br>budget|no exploitable region, plus<br>latency|hardware damage|


**Table 5** The four uses, ordered by whether the score is searched against. The top two select among non-adversarial candidates. The bottom two expose the score to a search for the regions where the score is wrong. Splitting by error type means counting false positives separately from false negatives, since curation incurs a different cost for each. 

## **6 Validating the Verifier** 

A verifier’s own error is worth measuring, because a verifier has four uses and a single verification error reaches all four uses. A verifier selects which demonstrations enter training, ranks one policy or one action above another, supplies the reward during post-training, and decides at run time whether an action may execute, for example by switching control to a stronger policy once the verifier flags a coming failure (29). One error therefore reaches the training data, the reported ranking, the reward, and the executed action together, and in each of the four uses that error looks like a correct result. Table 5 lists the same four uses, ordered by whether the score is searched against. Curation and ranking select among candidates produced without access to the score, and an error there averages out over the corpus. A training reward and a runtime gate are applied to candidates produced by a search for the inputs where the score is wrong, and one rare wrong-scoring region is then enough to make the score unusable. 

Throughout this section a _score_ is the output a verifier returns about a behavior, and a _metric_ is a quantity we compute about the verifier itself. Three metrics of a verifier’s own error appear in the literature. The first is agreement with a fixed reference (§6.1). The second is the policy that results from training on the verifier (§6.2). The third is the verifier’s behavior on candidates constructed to score highly without succeeding (§6.3). We then list the metrics whose reporting makes a verifier checkable by someone else (§6.4). 

#### **6.1 Agreement on a Fixed Set of Rollouts** 

An agreement benchmark fixes the rollouts, fixes a reference judgment for each rollout, and reports how often the verifier agrees with the reference. We first name the benchmarks built this way. An agreement rate then omits three things, how a disagreement splits between the verifier and the reference, the confidence interval around the rate, and the kind of rollout the rate was measured on. Table 6 closes the subsection with an audit of the resources the field relies on today. 

The reward benchmark released with TOPReward runs this benchmark design on 130 tasks across four robot platforms, scoring a candidate reward model by its agreement with human judgment (33). Three other benchmarks vary one element of the same benchmark design. The trajectory corpus behind Robometer is far larger, and that corpus was built for training rather than for auditing (21). RoboReward was built to diagnose verifier error, and among these four benchmarks RoboReward reports the lowest agreement at the time of writing (22). OpenGVL takes the true temporal order of the frames as its reference in place of a human label, and tests progress prediction on both robot and human embodiments, so OpenGVL measures whether a verifier still works on a new embodiment (169). The same benchmark design has also been applied to safety. There the reference states whether the behavior is dangerous rather than whether the task succeeded. ASIMOV renders situations taken from real injury reports into text scenarios and videos, then asks a frontier vision-language model to judge those scenarios directly, scoring how well the model recognizes physical danger and decides to intervene (170). A benchmark that reports task success and constraint satisfaction separately yields a number of the same kind (171). Some rollouts pass the success predicate and break a stated safety property, and the fraction of rollouts doing so is the false positive rate of the predicate. At present, the benchmarks that check a safety property separately from the success predicate agree on one finding: policies that complete more tasks 

20 

are not safer. Provael carries the same discipline into tooling. It scores a red-teaming attack against a fixed unsafe-region predicate over simulator state, and prints that predicate’s own false-positive rate beside every attack-success rate it reports; on the one policy measured so far, the predicate accepts two of fifty rollouts run with no attack applied (172). 

The first of the three things an agreement rate omits is how a disagreement splits between the verifier and the reference. A person is almost always the reference, and the error rate of that person is reported far less often than the agreement rate itself. The opposite case, where the verifier is wrong and the person is right, is also reported rarely. Lee et al. (22) find that frontier multimodal models used as rewards produce costly false positives and false negatives on tasks that a person judges without difficulty, including calling a failed drawer-opening a success. Such false positives and false negatives belong to the verifier being scored rather than to the human reference the verifier is scored against, so a low reference-error rate would still leave a hidden error on the verifier’s side. 

The second is the confidence interval around the rate. An agreement rate is reported as a single number, and the width of that interval sets how much evidence the rate provides. The rate itself is the fraction of trials the verifier judged correctly, over samples running from a hundred clips to a few thousand trajectories. Four designs on the policy side each supply one thing that a single number omits. First, blind randomized trials allocate the rollout budget in advance and report the size of that budget (173). Second, a test on the distribution of time to success reports the whole distribution in place of its mean (174). Third, bounds for a behavior-cloning policy state the task distribution the bounds hold over (175). Fourth, sequential designs let each next trial be chosen by the data collected so far, rather than fixing the schedule beforehand (176, 177, 178). The same machinery is standard outside robotics, in the interval estimators recommended for reinforcement learning comparisons run on too few seeds (179), and in the tests that stay valid when the person running them chooses the moment to stop (180). 

The third is the kind of rollout. An agreement rate holds for the rollouts the rate was computed on and not for rollouts of another kind. GE-Sim 2.0 makes the difference visible by scoring one verifier twice, on rollouts that its world model generated and on recorded video of the same tasks (181). A verifier’s error rate therefore depends on the kind of input as much as on the verifier itself, and an accuracy reported without naming the input omits the input, which is one of the two things that set the error rate. GE-Sim 2.0 attributes the resulting eight-point accuracy gap to artifacts that the world model itself introduces rather than to the difficulty of the task. The same question arises between simulation and hardware, where SureSim pairs a small number of real trials with simulated trials and shifts the simulated estimate by the average difference (182), and between embodiments, the difference that OpenGVL measures. Sim-to-real evaluation reads the sim-to-real gap directly, as the agreement between a ranking obtained in simulation and a ranking obtained on the robot, a metric that Yang et al. (183) propose but have not yet measured. RoboChallenge runs a shared real-robot fleet that executes a submitted policy and returns its score, and the hardware ranking is therefore available for comparison (184). MolmoSpaces reports the sim-to-real correspondence per task, while RoboLab reports the correspondence in aggregate across task suites tagged by the competency that each task requires (185, 186). 

Yu et al. (187) argue that a world model should be judged by the decisions made with it rather than by the fidelity of what it generates. The last column of Table 6 applies this standard to every resource in this survey. Two of its rows are world-model evaluations whose verifier error was never measured on generated rollouts. 

#### **6.2 Measuring a Verifier by the Policy It Trains** 

A verifier is built to train a better policy or to filter a better corpus. The gain in the resulting policy, rather than agreement with a reference judgment, is the quantity that actually matters. This gain is defined through a training run, and it is therefore expensive to obtain and correspondingly rare in the literature. 

An agreement rate and the gain in the trained policy diverge, and the mechanism is training itself. A verifier can agree with a person on ordinary rollouts and still fail on the rollouts that a training run drives the policy toward, because training moves the policy toward exactly those rollouts. Controlled measurements of the divergence between agreement and downstream gain exist on the language side, and we give one in §6.3. A robot verifier is optimized against in the same way, and the mechanism therefore applies on the robot side, where the corresponding measurement has yet to be run. 

21 

|**Resource**|**Object scored**|**Scale reported**|**Verifier**|**Serves**|**Verifier error measured on**<br>**its deployment distribution**|
|---|---|---|---|---|---|
|_Verifier-quality resources_||||||
|ManiRewardBench (33)|trajectory|130 tasks, 4 platforms|human|curation, ranking|✓|
|RBM-1M (21)|trajectory|_>_1M trajectories|human + auto|curation, ranking|✓|
|RoboReward (22)|trajectory|45k train, 2.8k verified test|human|curation, ranking|✓|
|RoboFAC (87)|trajectory|9,440 traj., 78,623 QA|human|curation|✓|
|OpenGVL (169)|trajectory|robot + human embodiments|temporal order|curation|✓|
|_Policy-evaluation substrate_|_s_|||||
|SIMPLER (188)|policy|2 robot suites|simulator rule|ranking|✓|
|AutoEval (130)|policy|24 h unattended|learned classifier|ranking|✓|
|RoboArena (36)|policy|600+ pairwise episodes|human|ranking|✓|
|PhAIL (174)|policy|4 VLAs, time-to-success CDF|rule + human anchor|ranking|✓|
|WorldEval (18)|policy|4 policies ranked|frontier VLM|ranking|×|
|WorldGym (19)|policy|across sizes, versions|VLM|ranking|×|
|WMBench (20)|world model|7 models, 324k rollouts|human + VLM|ranking|✓|
|GE-Sim 2.0 (181)|policy|6 tasks, 20 real-robot episodes each|learned verifier|ranking, reward|✓|


**Table 6** An audit of the resources used to establish that a verifier works. **Serves** names the use of the score from Table 5 that the resource supplies evidence for, and the last column states whether the verifier was evaluated on the kind of data the verifier is applied to. 

Two methods in this survey already compute the gain in the trained policy. A datamodel estimates the contribution of one demonstration to downstream performance (11), and a self-improvement loop lets a verifier decide which of a policy’s own rollouts re-enter training and then measures the result on the retrained policy (10, 66). Both methods define verifier quality by the performance of the retrained policy. The agreement rate and the downstream gain are reported separately and rarely for the same verifier, and the two numbers diverge most where a verifier is used as a training reward. 

#### **6.3 Measuring a Verifier Under Optimization** 

An agreement rate and a gain in the trained policy are both measured on a verifier that was never searched against. A verifier used as a training reward or a runtime gate has to meet one more requirement, that no region of inputs makes the score wrong in a way that a search can reach. Reward hacking is the failure of that requirement. Some inputs do make the score wrong, such as a run that satisfies a final-state predicate exactly and still fails the task (§3.2). A policy optimized against the score is driven toward such wrong-scoring inputs, since the score is highest there. Both measurements were taken on candidates produced without such a search, and both numbers therefore overstate the value of the verifier to a policy trained on it. 

Reward hacking is well studied on the language side. A scaling law measures how far a policy can be optimized against a reward model before the true objective starts to fall (189), a token-space attack finds inputs that a top-ranked reward model scores highest and should reject (190), and a survey documents the practice (191). Known fixes include information-theoretic bottlenecks and non-negative reward constructions (192, 193). A weak verifier produces reward gains that an independent panel does not confirm, and the gap widens as training continues (194). 

In robotics the same question, how far a policy can be optimized against a learned verifier before its score stops tracking the task, is largely undeveloped. Robustness to hacking is reported by the authors of each reward model, as a property of that model. A shared benchmark that holds the candidates fixed and scores the exploitability of each verifier has yet to appear. Li et al. (195) argue that the limit on reinforcement learning in embodied world models is unreliable verification rather than exploration. That work builds an agentic reward framework to resist hacking under distribution shift. One method reports on the embodied side of exploitability, letting a policy, a world model that simulates the policy, and a reward model that scores the result improve each other over several rounds (196). That method runs the co-adaptation described here as the intended procedure rather than as a failure. 

Optimization has two consequences for a verifier. The reward gain the verifier reports becomes an overestimate, and the calibration the verifier was released with stops holding. 

22 

**Verifiers held out from training.** One protocol would measure a robot verifier’s exploitability without waiting for a shared benchmark. Score the rollouts twice, once with the verifier that the policy was trained on and once with a panel of verifiers the policy never saw. A policy that genuinely improved passes both. A policy that only learned to satisfy its training verifier passes the first scoring and fails the panel. The panel on a robot is a set of trajectory verifiers, and the protocol runs at each checkpoint. Take the rollouts that the training verifier passed, hand those rollouts to the panel, and report the fraction the panel rejects. The simulators and the training setups this protocol needs are published (197, 12). 

**A calibration that optimization invalidates.** A conformal margin is a fixed number added to a verifier’s score so that the true outcome falls inside the resulting interval a stated fraction of the time. The margin comes from a held-out set (68, 26). A held-out set is a batch of rollouts whose outcomes are known and which the verifier did not see during its construction. The margin provides its stated coverage as long as the rollouts judged later come from the same pool as the held-out set. The requirement that later rollouts come from the same pool is exchangeability (§3.1.1). Filtering rollouts by the verifier’s own scores draws the later rollouts from a different pool, and the margin then no longer provides its stated coverage (198, 199). 

Training a policy against a verifier changes the data that the verifier will later receive (200). The verifier moves the distribution toward the region where the verifier is wrong, and a correction made once therefore stops holding after the next round of training. Conformal failure detection therefore holds for a frozen policy (85) and weakens for a policy trained against the detector (26), and the same exchangeability argument implies SureSim’s bias correction would need to be recomputed once a retrained policy changes the deployment distribution, though the original work evaluates only a single frozen policy (182). Online conformal methods answer this by recalibrating continuously (201), and the guarantee such methods provide is asymptotic rather than finite-sample. 

#### **6.4 Metrics for Validating a Verifier** 

We provide nine metrics for a verifier, and reporting the nine makes verifier claims comparable across papers. Guidance of this kind exists for evaluating robot policies empirically (202, 173, 174), and the verifier benchmarks of §6.1 put a verifier under test. Such a benchmark scores one verifier on one fixed set of rollouts against one fixed reference, and reports a single agreement rate. The nine metrics ask for what the rate omits, from the conditions it was measured under to what becomes of the verifier once a policy is optimized against it. Table 7 splits the nine by whether the score is used to select or optimized against. One of the nine is computed from two separate scorings, and we give the computation below. 

**Proxy gain that transfers.** This number measures the fraction of a reward gain that is real. Score the first and the last checkpoint under the training verifier and call the difference Δproxy. Score the same two checkpoints under a panel that the policy never trained against and call the difference Δpanel. Report the ratio Δpanel/Δproxy together with both differences, since the ratio becomes unstable when Δproxy is small. One means the panel confirms the whole gain, zero means the panel confirms none of the gain, and a negative number means the panel scores the policy lower while the training reward rises. The two differences behind the ratio are separately available in simulation. 

## **7 Conclusion** 

A verifier in robot learning decides what a policy is trained on and what the policy’s reported performance means. We surveyed roughly 150 verifiers and grouped them by who supplies the judgment, into human verifiers, rule-based and formal verifiers, learned and pretrained verifiers, and model-intrinsic verifiers. We compared the four families on their _availability_ and their _credibility_ . Across the four families, _availability_ and _credibility_ move in opposite directions. As the source of judgment moves closer to the model being evaluated, a verification signal becomes cheaper to obtain, arrives earlier, and can be queried more often, while the evidence that the signal reflects actual task performance becomes harder to assemble. 

The four families occupy different points on the availability-credibility trade-off. Human verifiers give the most direct reference to the intent of the task, and their verdicts are costly to obtain, so human verifiers appear 

23 

|**Metric**|**How it is computed**|**What it settles**|
|---|---|---|
|_For a score used to select: curation_|_and ranking_||
|Independent rollout count|count per condition, for every success rate given|the confidence interval can be rebuilt from the<br>count (§6.1)|
|Error rate by type|false positives and false negatives separately,<br>with the label count behind each|a false positive trains on a failure, a false<br>negative discards usable data|
|Rollout type|teleoperated, scripted, or sampled from the<br>policy being judged|a verifier scoring generated rollouts needs its<br>error measured on generated rollouts (§6.1)|
|Agreement with human labels|agreement rate with its label count, plus<br>agreement between two annotators|how far the verifier sits from the labels, and the<br>labels from each other|
|Calibration|score minus observed success rate of the rollouts<br>in that score bin|required of any continuous score consumed as a<br>reward|
|Cross-embodiment transfer|error on a held-out embodiment minus error on<br>the training embodiments|whether the verifier still works on a new robot<br>(169)|
|_For a score optimized against: trai_|_ning reward and runtime gating_||
|Proxy gain that transfers|Δpanel/Δproxy, with both gains reported|separates a real gain from a gain that only<br>satisfies the training verifier (194)|
|Verifier error over training|error on initial-checkpoint and on<br>final-checkpoint rollouts, labeled alike|the increase in verifier error produced by the<br>optimization|
|False positives under search|candidates found by searching the verifier for<br>inputs the verifier wrongly accepts (203)|the region a policy trained on this verifier moves<br>toward|


**Table 7** Nine metrics that make a verifier claim comparable across papers. Most of the upper block asks for numbers the authors have already measured. The lower block requires running a search against the verifier, which robotics has yet to do for a learned verifier. 

mostly as the small sample that validates the other three families (§2). Rule-based and formal verifiers are inexpensive and repeatable once the required state information is available, and they reach the strongest guarantees in this survey, though only where the predicate, the state estimate, and the dynamics assumptions represent the task (§3). Learned and pretrained verifiers are inexpensive to query and dense across many tasks and trajectories, and the error rate of such a model depends on the data the model was trained and validated on (§4). Model-intrinsic verifiers cost the least, because the policy or the predictive model already computes the model-intrinsic score. The model-intrinsic score describes the model rather than the task, and its relation to actual task performance is therefore indirect (§5). Learned and pretrained verifiers are the largest group in this survey, and model-intrinsic verifiers cost the least to obtain. Those are exactly the two families whose _credibility_ is least often established. 

Establishing _credibility_ is a separate task from building a verifier. We surveyed two ways of establishing credibility. One is a chain of comparisons ending at a set of human labels, and the error of those labels is rarely reported alongside the claim the labels support (§6.1). The other is a benchmark that puts the verifier under test and reports the verifier’s own error rate (§6.1). The demand on a verifier depends on how its score is used. Curation and ranking tolerate an average error rate, and a training reward and a runtime gate demand more, because the candidates they score come from a search for the inputs where the score is wrong. Every agreement rate and every downstream gain that this survey collected was measured on non-adversarial candidates (§6). _Availability_ and _credibility_ are meant as coordinates for the verifiers still to be built. Naming who supplies the judgment fixes how much a verifier costs, how often the verifier can be queried, and how much the verifier’s score can prove. Today, there is **no free checker** . Reaching high _availability_ and high _credibility_ together is the main future work in verification for robot learning. 

## **Use of Large Language Models** 

Parts of the text in this survey were drafted with a large language model. Every claim, citation, and count was checked by the authors against the cited papers. 

24 

## **References** 

- [1] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, et al. RT-2: Vision-language-action models transfer web knowledge to robotic control. In _Proceedings of the Conference on Robot Learning (CoRL)_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 2165–2183. PMLR, 2023. 

- [2] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. OpenVLA: An open-source vision-language-action model. In _Proceedings of the Conference on Robot Learning (CoRL)_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 2679–2713. PMLR, 2024. 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, et al. _𝜋_ 0: A visionlanguage-action flow model for general robot control. In _Proceedings of Robotics: Science and Systems (RSS)_ , Los Angeles, CA, USA, June 2025. doi: 10.15607/RSS.2025.XXI.010. 

- [4] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, et al. _𝜋_ 0 _._ 5: a Vision-Language-Action Model with Open-World Generalization. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [5] Physical Intelligence, Bo Ai, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Greg Balke, et al. _𝜋_ 0 _._ 7: a steerable generalist robotic foundation model with emergent capabilities, 2026. 

- [6] NVIDIA, Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, et al. Cosmos World Foundation Model Platform for Physical AI. _arXiv preprint arXiv:2501.03575_ , 2025. 

- [7] Google DeepMind. Genie 3: A new frontier for world models. Google DeepMind blog, 2025. URL `https: //deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/` . Accessed 202608-25. 

- [8] DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, et al. DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning. _Nature_ , 2025. 

- [9] Joey Hejna, Chethan Bhateja, Yichen Jiang, Karl Pertsch, and Dorsa Sadigh. ReMix: Optimizing Data Mixtures for Large Scale Imitation Learning. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [10] Annie S. Chen, Alec M. Lessing, Yuejiang Liu, and Chelsea Finn. Curating Demonstrations using Online Experience. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [11] Shivin Dass, Alaa Khaddaj, Logan Engstrom, Aleksander Madry, Andrew Ilyas, and Roberto Martín-Martín. DataMIL: Selecting Data for Robot Imitation Learning with Datamodels. In _International Conference on Learning Representations (ICLR)_ , 2026. 

- [12] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, et al. SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning. In _International Conference on Learning Representations (ICLR)_ , 2026. 

- [13] Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Krähenbühl. Interactive Post-Training for Vision-Language-Action Models. _arXiv preprint arXiv:2505.17016_ , 2025. 

- [14] Hongzhi Zang, Mingjie Wei, Si Xu, Yongji Wu, Zhen Guo, Yuanqing Wang, Hao Lin, Peihong Wang, et al. RLinf-VLA: A Unified and Efficient Framework for Reinforcement Learning of Vision-Language-Action Models. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2026. 

- [15] Jacky Kwok, Christopher Agia, Rohan Sinha, Matt Foutter, Shulu Li, Ion Stoica, Azalia Mirhoseini, Marco Pavone, et al. RoboMonkey: Scaling Test-Time Sampling and Verification for Vision-Language-Action Models. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [16] Mitsuhiko Nakamoto, Oier Mees, Aviral Kumar, and Sergey Levine. Steering Your Generalists: Improving Robotic Foundation Models via Value Guidance. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [17] Suhyeok Jang, Dongyoung Kim, Changyeon Kim, Youngsuk Kim, and Jinwoo Shin. Verifier-free Test-Time Sampling for Vision-Language-Action Models. In _International Conference on Learning Representations (ICLR)_ , 2026. 

- [18] Yaxuan Li, Yichen Zhu, Junjie Wen, Chaomin Shen, and Yi Xu. WorldEval: World Model as Real-World Robot Policies Evaluator. _arXiv preprint arXiv:2505.19017_ , 2025. 

- [19] Julian Quevedo, Ansh Kumar Sharma, Yixiang Sun, Varad Suryavanshi, Percy Liang, and Sherry Yang. WorldGym: World Model as An Environment for Policy Evaluation. In _International Conference on Learning Representations (ICLR)_ , 2026. 

- [20] GigaWorld Team, Angyuan Ma, Boyuan Wang, Bohan Li, Chaojun Ni, Guo Li, Guan Huang, Guosheng Zhao, et al. GigaWorld-1: A Roadmap to Build World Models for Robot Policy Evaluation. _arXiv preprint arXiv:2607.02642_ , 2026. 

- [21] Anthony Liang, Yigit Korkmaz, Jiahui Zhang, Minyoung Hwang, Abrar Anwar, Sidhant Kaushik, Aditya Shah, Alex S. Huang, et al. Robometer: Scaling General-Purpose Robotic Reward Models via Trajectory Comparisons. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2026. 

25 

- [22] Tony Lee, Andrew Wagenmaker, Karl Pertsch, Percy Liang, Sergey Levine, and Chelsea Finn. RoboReward: GeneralPurpose Vision-Language Reward Models for Robotics. _arXiv preprint arXiv:2601.00675_ , 2026. 

- [23] Huajie Tan, Sixiang Chen, Yijie Xu, Zixiao Wang, Yuheng Ji, Cheng Chi, Yaoxu Lyu, Zhongxia Zhao, et al. RoboDopamine: General Process Reward Modeling for High-Precision Robotic Manipulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2026. 

- [24] Yixuan Wang, Rhythm Syed, Fangyu Wu, Mengchao Zhang, Aykut Onol, Jose Barreiros, Hooshang Nayyeri, Tony Dear, et al. Interactive World Simulator for Robot Policy Training and Evaluation. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2026. 

- [25] Enshen Zhou, Qi Su, Cheng Chi, Zhizheng Zhang, Zhongyuan Wang, Tiejun Huang, Lu Sheng, He Wang, et al. Code-as-Monitor: Constraint-aware Visual Programming for Reactive and Proactive Robotic Failure Detection. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 

- [26] Qiao Gu, Yuanliang Ju, Shengxiang Sun, Igor Gilitschenski, Haruki Nishimura, Masha Itkina, and Florian Shkurti. SAFE: Multitask Failure Detection for Vision-Language-Action Models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [27] Christopher Agia, Rohan Sinha, Jingyun Yang, Zi ang Cao, Rika Antonova, Marco Pavone, and Jeannette Bohg. Unpacking Failure Modes of Generative Policies: Runtime Monitoring of Consistency and Progress. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [28] Oswin So, Zachary Serlin, Makai Mann, Jake Gonzales, Kwesi Rutledge, Nicholas Roy, and Chuchu Fan. How to Train Your Neural Control Barrier Function: Learning Safety Filters for Complex Input-Constrained Systems. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- [29] Josef Chen. AEGIS: A backup reflex for physical AI, 2026. 

- [30] Yecheng Jason Ma, Joey Hejna, Ayzaan Wahid, Chuyuan Fu, Dhruv Shah, Jacky Liang, Zhuo Xu, Sean Kirmani, et al. Vision Language Models are In-Context Value Learners. In _International Conference on Learning Representations (ICLR)_ , 2025. 

- [31] Yecheng Jason Ma, Shagun Sodhani, Dinesh Jayaraman, Osbert Bastani, Vikash Kumar, and Amy Zhang. VIP: Towards Universal Visual Reward and Representation via Value-Implicit Pre-Training. In _International Conference on Learning Representations (ICLR)_ , 2023. 

- [32] Yecheng Jason Ma, Vikash Kumar, Amy Zhang, Osbert Bastani, and Dinesh Jayaraman. LIV: Language-Image Representations and Rewards for Robotic Control. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2023. 

- [33] Shirui Chen, Cole Harrison, Ying-Chun Lee, Angela Jin Yang, Zhongzheng Ren, Lillian J. Ratliff, Jiafei Duan, Dieter Fox, et al. TOPReward: Token Probabilities as Hidden Zero-Shot Rewards for Robotics. _arXiv preprint arXiv:2602.19313_ , 2026. 

- [34] Paul F. Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep reinforcement learning from human preferences. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2017. 

- [35] Serkan Cabi, Sergio Gómez Colmenarejo, Alexander Novikov, Ksenia Konyushova, Scott Reed, Rae Jeong, et al. Scaling data-driven robotics with reward sketching and batch reinforcement learning. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2020. 

- [36] Pranav Atreya, Karl Pertsch, Tony Lee, Moo Jin Kim, Arhan Jain, Artur Kuramshin, Clemens Eppner, Cyrus Neary, et al. RoboArena: Distributed Real-World Evaluation of Generalist Robot Policies. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [37] Chengyue Huang, Khang Vo Huynh, Sebastian Elbaum, Zsolt Kira, and Lu Feng. SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation. _arXiv preprint arXiv:2605.12386_ , 2026. 

- [38] Yue Meng, Fei Chen, and Chuchu Fan. TGPO: Temporal Grounded Policy Optimization for Signal Temporal Logic Tasks. _arXiv preprint arXiv:2510.00225_ , 2025. 

- [39] Yuqing Du, Ksenia Konyushkova, Misha Denil, Akhil Raju, Jessica Landon, Felix Hill, Nando de Freitas, Serkan Cabi, et al. Vision-Language Models as Success Detectors. In _Proceedings of The 2nd Conference on Lifelong Learning Agents_ , 2023. 

- [40] Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, et al. _𝜋_<sup>∗</sup> 0 _._ 6<sup>:a VLA</sup> that learns from experience. _arXiv preprint arXiv:2511.14759_ , 2025. 

- [41] Tianhe Yu, Garrett Thomas, Lantao Yu, Stefano Ermon, James Zou, Sergey Levine, et al. MOPO: Model-based Offline Policy Optimization. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. 

- [42] Kensuke Nakamura, Lasse Peters, and Andrea Bajcsy. Generalizing Safety Beyond Collision-Avoidance via LatentSpace Reachability Analysis. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [43] Kimin Lee, Laura Smith, and Pieter Abbeel. PEBBLE: Feedback-Efficient Interactive Reinforcement Learning via Relabeling Experience and Unsupervised Pre-training. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2021. 

- [44] Kimin Lee, Laura Smith, Anca Dragan, and Pieter Abbeel. B-Pref: Benchmarking Preference-Based Reinforcement Learning. In _Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track_ , 2021. 

26 

- [45] Quanyi Li, Zhenghao Peng, and Bolei Zhou. Efficient Learning of Safe Driving Policy via Human-AI Copilot Optimization. In _International Conference on Learning Representations (ICLR)_ , 2022. URL `https://openreview. net/forum?id=0cgU-BZp2ky` . 

- [46] Huihan Liu, Soroush Nasiriany, Lance Zhang, Zhiyao Bao, and Yuke Zhu. Robot Learning on the Job: Human-in-theLoop Autonomy and Learning During Deployment. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. doi: 10.15607/RSS.2023.XIX.005. URL `https://roboticsproceedings.org/rss19/p005.html` . 

- [47] Huihan Liu, Yu Zhang, Vaarij Betala, Evan Zhang, James Liu, Crystal Ding, and Yuke Zhu. Multi-task interactive robot fleet learning with visual world models. In _Proceedings of the Conference on Robot Learning (CoRL)_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 4286–4313. PMLR, 2024. 

- [48] Jianlan Luo, Charles Xu, Jeffrey Wu, and Sergey Levine. Precise and Dexterous Robotic Manipulation via Human-inthe-Loop Reinforcement Learning. _Science Robotics_ , 2025. 

- [49] Gemini Robotics Team, Krzysztof Choromanski, Coline Devin, Yilun Du, Debidatta Dwibedi, Ruiqi Gao, et al. Evaluating Gemini Robotics Policies in a Veo World Simulator. _arXiv preprint arXiv:2512.10675_ , 2025. 

- [50] Shreyas Kousik, Sean Vaskov, Fan Bu, Matthew Johnson-Roberson, and Ram Vasudevan. Bridging the Gap between Safety and Real-Time Performance in Receding-Horizon Trajectory Design for Mobile Robots. _The International Journal of Robotics Research_ , 39(12):1419–1469, 2020. 

- [51] Yifei Simon Shao, Chao Chen, Shreyas Kousik, and Ram Vasudevan. Reachability-Based Trajectory Safeguard (RTS): A Safe and Fast Reinforcement Learning Safety Layer for Continuous Control. _IEEE Robotics and Automation Letters_ , 6(2):3663–3670, 2021. 

- [52] Kim P. Wabersich and Melanie N. Zeilinger. A predictive safety filter for learning-based control of constrained nonlinear dynamical systems. _Automatica_ , 129:109597, 2021. doi: 10.1016/j.automatica.2021.109597. 

- [53] Sven R. Schepp, Jakob Thumm, Stefan B. Liu, and Matthias Althoff. SaRA: A Tool for Safe Human-Robot Coexistence and Collaboration through Reachability Analysis. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 4312–4317, 2022. 

- [54] Mahmoud Selim, Amr Alanwar, Shreyas Kousik, Grace Gao, Marco Pavone, and Karl H. Johansson. Safe Reinforcement Learning Using Black-Box Reachability Analysis. _IEEE Robotics and Automation Letters_ , 7(4):10665–10672, 2022. 

- [55] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. CALVIN: A Benchmark for LanguageConditioned Policy Learning for Long-Horizon Robot Manipulation Tasks. _IEEE Robotics and Automation Letters_ , 7 (3):7327–7334, 2022. 

- [56] Lars Lindemann, Xin Qin, Jyotirmoy V. Deshmukh, and George J. Pappas. Conformal Prediction for STL Runtime Verification. In _Proceedings of the ACM/IEEE 14th International Conference on Cyber-Physical Systems (ICCPS)_ , 2023. 

- [57] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning. In _Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track_ , 2023. 

- [58] Ajay Mandlekar, Soroush Nasiriany, Bowen Wen, Iretiayo Akinola, Yashraj Narang, Linxi Fan, Yuke Zhu, Dieter Fox, et al. MimicGen: A Data Generation System for Scalable Robot Learning using Human Demonstrations. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [59] Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke Zhu, Linxi Fan, et al. Eureka: Human-Level Reward Design via Coding Large Language Models. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [60] Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, and Li Fei-Fei. ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2024. 

- [61] Jonathan Michaux, Patrick Holmes, Bohao Zhang, Che Chen, Baiyue Wang, Shrey Sahgal, Tiancheng Zhang, Sidhartha Dey, Shreyas Kousik, and Ram Vasudevan. Can’t Touch This: Real-Time, Safe Motion Planning and Control for Manipulators Under Uncertainty. _IEEE Transactions on Robotics_ , 41:4719–4740, 2025. 

- [62] Soham Kulkarni, Raayan Dhar, and Yuchen Cui. Learning from the Best: Smoothness-Driven Metrics for Data Quality in Imitation Learning. _arXiv preprint arXiv:2604.23000_ , 2026. 

- [63] Haoran Xu, Xianyuan Zhan, Honglei Yin, and Huiling Qin. Discriminator-Weighted Offline Imitation Learning from Suboptimal Demonstrations. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2022. 

- [64] Mark Beliaev, Andy Shih, Stefano Ermon, Dorsa Sadigh, and Ramtin Pedarsani. Imitation Learning by Estimating Expertise of Demonstrators. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2022. 

- [65] Brian Ichter, Anthony Brohan, Yevgen Chebotar, Chelsea Finn, Karol Hausman, Alexander Herzog, Daniel Ho, Julian Ibarz, et al. Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [66] Konstantinos Bousmalis, Giulia Vezzani, Dushyant Rao, Coline Devin, Alex X. Lee, Maria Bauza, Todor Davchev, Yuxiang Zhou, et al. RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation. _Transactions on Machine Learning Research_ , 2024. 

27 

- [67] Shaopeng Zhai, Qi Zhang, Tianyi Zhang, Fuxian Huang, Haoran Zhang, Ming Zhou, Shengzhe Zhang, Litao Liu, et al. A Vision-Language-Action-Critic Model for Robotic Real-World Reinforcement Learning. _arXiv preprint arXiv:2509.15937_ , 2025. 

- [68] Allen Z. Ren, Anushri Dixit, Alexandra Bodrova, Sumeet Singh, Stephen Tu, Noah Brown, Peng Xu, Leila Takayama, et al. Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [69] Zeyi Liu, Arpit Bahety, and Shuran Song. REFLECT: Summarizing robot experiences for failure explanation and correction. In _Proceedings of the Conference on Robot Learning (CoRL)_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 3468–3484. PMLR, 2023. 

- [70] Juan Rocamonde, Victoriano Montesinos, Elvis Nava, Ethan Perez, and David Lindner. Vision-language models are zero-shot reward models for reinforcement learning. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [71] Zijian Zhang, Kaiyuan Zheng, Zhaorun Chen, Joel Jang, Yi Li, Siwei Han, Chaoqi Wang, Mingyu Ding, et al. GRAPE: Generalizing Robot Policy via Preference Alignment. In _International Conference on Learning Representations (ICLR) Workshop on Reasoning and Planning for Large Language Models_ , 2025. 

- [72] Senyu Fei, Siyin Wang, Li Ji, Ao Li, Shiduo Zhang, Liming Liu, Jinlong Hou, Jingjing Gong, et al. SRPO: SelfReferential Policy Optimization for Vision-Language-Action Models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2026. 

- [73] Rahul Kidambi, Aravind Rajeswaran, Praneeth Netrapalli, and Thorsten Joachims. MOReL: Model-Based Offline Reinforcement Learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. 

- [74] Rafael Rafailov, Tianhe Yu, Aravind Rajeswaran, and Chelsea Finn. Offline Reinforcement Learning from Images with Latent Space Models. In _Proceedings of the 3rd Conference on Learning for Dynamics and Control (L4DC)_ , 2021. 

- [75] Albert Wilcox, Ashwin Balakrishna, Brijen Thananjeyan, Joseph E. Gonzalez, and Ken Goldberg. LS3: Latent Space Safe Sets for Long-Horizon Visuomotor Control of Sparse Reward Iterative Tasks. In _Proceedings of the Conference on Robot Learning (CoRL)_ , pages 959–969, 2022. 

- [76] Alejandro Escontrela, Ademi Adeniji, Wilson Yan, Ajay Jain, Xue Bin Peng, Ken Goldberg, et al. Video Prediction Models as Rewards for Reinforcement Learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2023. 

- [77] Tao Huang, Guangqi Jiang, Yanjie Ze, and Huazhe Xu. Diffusion Reward: Learning Rewards via Conditional Video Diffusion. In _Proceedings of the European Conference on Computer Vision (ECCV)_ , 2024. 

- [78] Siyuan Yang, Yang Zhang, Haoran He, Ling Pan, Xiu Li, Chenjia Bai, and Xuelong Li. Steering Vision-Language-Action Models as Anti-Exploration: A Test-Time Scaling Approach. _arXiv preprint arXiv:2512.02834_ , 2025. 

- [79] Seongheon Park, Wendi Li, Changdae Oh, Samuel Yeh, Zsolt Kira, Michael Hagenow, and Sharon Li. Hide-and-Seek in Trajectories: Discovering Failure Signals for VLA Runtime Monitoring. _arXiv preprint arXiv:2605.30834_ , 2026. 

- [80] Sankalp Agrawal, Junwon Seo, Kensuke Nakamura, Ran Tian, and Andrea Bajcsy. AnySafe: Adapting latent safety filters at runtime via safety constraint parameterization in the latent space. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2026. 

- [81] Ryan Hoque, Ashwin Balakrishna, Ellen Novoseller, Albert Wilcox, Daniel S. Brown, and Ken Goldberg. ThriftyDAgger: Budget-Aware Novelty and Risk Gating for Interactive Imitation Learning. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2022. 

- [82] Michael Kelly, Chelsea Sidrane, Katherine Rose Driggs-Campbell, and Mykel J. Kochenderfer. HG-DAgger: Interactive Imitation Learning with Human Experts. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8077–8083. IEEE, 2019. doi: 10.1109/ICRA.2019.8793698. 

- [83] Bo Yue, Shuqi Guo, Kaiyu Hu, Chujiao Wang, Benyou Wang, Kui Jia, and Guiliang Liu. Real-Time Verification of Embodied Reasoning for Generative Skill Acquisition. _arXiv preprint arXiv:2505.11175_ , 2025. 

- [84] Runhao Zeng, Dingjie Zhou, Qiwei Liang, Junlin Liu, Hui Li, Changxin Huang, Jianqiang Li, Xiping Hu, et al. Video2Reward: Generating Reward Function from Videos for Legged Robot Behavior Learning. In _Proceedings of the 27th European Conference on Artificial Intelligence (ECAI 2024)_ , 2024. 

- [85] Haoran Zhang, Yifu Lu, Boyang Wang, Xuhui Kang, Yen-Ling Kuo, Zezhou Cheng, Mengdi Wang, Odest Chadwicke Jenkins, et al. Foresight: Failure Detection for Long-Horizon Robotic Manipulation with Action-Conditioned World Model Latents. _arXiv preprint arXiv:2606.23085_ , 2026. 

- [86] Jiafei Duan, Wilbert Pumacay, Nishanth Kumar, Yi Ru Wang, Shulin Tian, Wentao Yuan, Ranjay Krishna, Dieter Fox, et al. AHA: A Vision-Language-Model for Detecting and Reasoning Over Failures in Robotic Manipulation. In _International Conference on Learning Representations (ICLR)_ , 2025. 

- [87] Zewei Ye, Weifeng Lu, Minghao Ye, Tao Lin, Shuo Yang, Junchi Yan, and Bo Zhao. RoboFAC: A Comprehensive Framework for Robotic Failure Analysis and Correction. _arXiv preprint arXiv:2505.12224_ , 2025. 

- [88] Yilin Wu, Thomas Tian, Gokul Swamy, and Andrea Bajcsy. From Foresight to Forethought: VLM-In-the-Loop Policy Steering via Latent Alignment. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

28 

- [89] Stéphane Ross, Geoffrey J. Gordon, and J. Andrew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the 14th International Conference on Artificial Intelligence and Statistics (AISTATS)_ , volume 15 of _Proceedings of Machine Learning Research_ , pages 627–635. PMLR, 2011. 

- [90] Haoyuan Cai, Zhenghao Peng, and Bolei Zhou. Robot-Gated Interactive Imitation Learning with Adaptive Intervention Mechanism. In _Proceedings of the International Conference on Machine Learning (ICML)_ , volume 267 of _Proceedings of Machine Learning Research_ , pages 6243–6256. PMLR, 2025. URL `https://proceedings.mlr.press/v267/ cai25e.html` . 

- [91] Kevin Lin, Christopher Agia, Toki Migimatsu, Marco Pavone, and Jeannette Bohg. Text2Motion: From Natural Language Instructions to Feasible Plans. _Autonomous Robots_ , 2023. 

- [92] Yiqi Zhao, Emily Zhu, Bardh Hoxha, Georgios Fainekos, Jyotirmoy V. Deshmukh, Lars Lindemann, et al. Distributionally Robust Predictive Runtime Verification under Spatio-Temporal Logic Specifications. _ACM Transactions on Cyber-Physical Systems_ , 2025. 

- [93] Yiqi Zhao, Bardh Hoxha, Georgios Fainekos, Jyotirmoy V. Deshmukh, and Lars Lindemann. Robust Conformal Prediction for STL Runtime Verification under Distribution Shift. In _2024 ACM/IEEE 15th International Conference on Cyber-Physical Systems (ICCPS)_ , 2024. 

- [94] Devesh Nath, Anutam Srinivasan, Haoran Yin, Ruitong Jiang, Jeffrey Fang, Glen Chou, et al. Pixels to Proofs: Probabilistically-Safe Latent World Model Control via Parallel Conformal Robust MPC. _arXiv preprint arXiv:2606.15594_ , 2026. 

- [95] Ameesh Shah, Cameron Voloshin, Chenxi Yang, Abhinav Verma, Swarat Chaudhuri, and Sanjit A. Seshia. LTLConstrained Policy Optimization with Cycle Experience Replay. _Transactions on Machine Learning Research_ , 2025. 

- [96] Yecheng Jason Ma, William Liang, Hung-Ju Wang, Sam Wang, Yuke Zhu, Linxi Fan, Osbert Bastani, and Dinesh Jayaraman. DrEureka: Language Model Guided Sim-To-Real Transfer. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- [97] Tianbao Xie, Siheng Zhao, Chen Henry Wu, Yitao Liu, Qian Luo, Victor Zhong, Yanchao Yang, Tao Yu, et al. Text2Reward: Reward Shaping with Language Models for Reinforcement Learning. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [98] Wenhao Yu, Nimrod Gileadi, Chuyuan Fu, Sean Kirmani, Kuang-Huei Lee, Montse Gonzalez Arenas, Hao-Tien Lewis Chiang, Tom Erez, et al. Language to Rewards for Robotic Skill Synthesis. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- [99] Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue Yin, et al. VLABench: A Large-Scale Benchmark for Language-Conditioned Robotics Manipulation with Long-Horizon Reasoning Tasks. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. 

- [100] Ning Gao, Yilun Chen, Shuai Yang, Xinyi Chen, Yang Tian, Hao Li, Haifeng Huang, Hanqing Wang, et al. GENMANIP: LLM-driven Simulation for Generalizable Instruction-Following Manipulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 

- [101] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, Yuke Zhu, et al. RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- [102] Haoran Geng, Feishi Wang, Songlin Wei, Yuyang Li, Bangjun Wang, Boshi An, Charlie Tianyue Cheng, Haozhe Lou, et al. RoboVerse: A Unified Platform, Benchmark and Dataset for Scalable and Generalizable Robot Learning. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [103] Stone Tao, Fanbo Xiang, Arth Shukla, Yuzhe Qin, Xander Hinrichsen, Xiaodi Yuan, Chen Bao, Xinsong Lin, et al. ManiSkill3: GPU Parallelized Robotics Simulation and Rendering for Generalizable Embodied AI. _arXiv preprint arXiv:2410.00425_ , 2024. 

- [104] Mayank Mittal, Yunrong Guo, Pascal Roth, David Hoeller, James Tigue, Antoine Richard, Octi Zhang, Peter Du, et al. Isaac lab: A GPU-accelerated simulation framework for multi-modal robot learning, 2025. Includes Isaac Lab-Arena, an open framework for large-scale policy evaluation. 

- [105] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, et al. RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2026. 

- [106] Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gokmen, Sanjana Srivastava, Roberto Martín-Martín, Chen Wang, Gabrael Levine, et al. BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation. _arXiv preprint arXiv:2403.09227_ , 2024. 

- [107] Wilbert Pumacay, Ishika Singh, Jiafei Duan, Ranjay Krishna, Jesse Thomason, and Dieter Fox. THE COLOSSEUM: A benchmark for evaluating generalization for robotic manipulation. In _Proceedings of Robotics: Science and Systems (RSS)_ , Delft, Netherlands, July 2024. 

- [108] Zhenyu Jiang, Yuqi Xie, Kevin Lin, Zhenjia Xu, Weikang Wan, Ajay Mandlekar, Linxi Fan, Yuke Zhu, et al. DexMimicGen: Automated Data Generation for Bimanual Dexterous Manipulation via Imitation Learning. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

29 

- [109] Zhengrong Xue, Shuying Deng, Zhenyang Chen, Yixuan Wang, Zhecheng Yuan, and Huazhe Xu. DemoGen: Synthetic Demonstration Generation for Data-Efficient Visuomotor Policy Learning. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [110] Lirui Wang, Yiyang Ling, Zhecheng Yuan, Mohit Shridhar, Chen Bao, Yuzhe Qin, Bailin Wang, Huazhe Xu, et al. GenSim: Generating Robotic Simulation Tasks via Large Language Models. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [111] Pu Hua, Minghuan Liu, Annabella Macaluso, Yunfeng Lin, Weinan Zhang, Huazhe Xu, and Lirui Wang. GenSim2: Scaling Robot Data Generation with Multi-modal and Reasoning LLMs. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [112] Yufei Wang, Zhou Xian, Feng Chen, Tsun-Hsuan Wang, Yian Wang, Katerina Fragkiadaki, Zackory Erickson, David Held, et al. RoboGen: Towards Unleashing Infinite Data for Automated Robot Learning via Generative Simulation. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2024. 

- [113] Yuhui Chen, Shuai Tian, Shugao Liu, Yingting Zhou, Haoran Li, and Dongbin Zhao. ConRFT: A Reinforced Finetuning Method for VLA Models via Consistency Policy. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [114] Lukas Helff, Quentin Delfosse, David Steinmann, Ruben Härle, Hikaru Shindo, Patrick Schramowski, et al. LLMs Gaming Verifiers: RLVR can Lead to Reward Hacking. _arXiv preprint arXiv:2604.15149_ , 2026. 

- [115] Joar Skalse, Nikolaus H. R. Howe, Dmitrii Krasheninnikov, and David Krueger. Defining and Characterizing Reward Hacking. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2022. 

- [116] David Manheim and Scott Garrabrant. Categorizing Variants of Goodhart’s Law. _arXiv preprint arXiv:1803.04585_ , 2018. 

- [117] Aaron D. Ames, Samuel Coogan, Magnus Egerstedt, Gennaro Notomista, Koushil Sreenath, and Paulo Tabuada. Control barrier functions: Theory and applications. In _2019 18th European Control Conference (ECC)_ , pages 3420–3431, Naples, Italy, 2019. doi: 10.23919/ECC.2019.8796030. 

- [118] Kai-Chieh Hsu, Haimin Hu, and Jaime F. Fisac. The safety filter: A unified view of safety-critical control in autonomous systems. _Annual Review of Control, Robotics, and Autonomous Systems_ , 7(1):47–72, 2024. doi: 10.1146/ annurev-control-071723-102940. 

- [119] Daniel C. H. Tan, Fernando Acero, Robert McCarthy, Dimitrios Kanoulas, and Zhibin Li. Value Functions are Control Barrier Functions: Verification of Safe Policies using Control Theory. _arXiv preprint arXiv:2306.04026_ , 2023. 

- [120] Jinsun Liu, Yifei Simon Shao, Lucas Lymburner, Hansen Qin, Vishrut Kaushik, Lena Trang, Ruiyang Wang, Vladimir Ivanovic, H. Eric Tseng, and Ram Vasudevan. REFINE: Reachability-Based Trajectory Design Using Robust Feedback Linearization and Zonotopes. _IEEE Transactions on Robotics_ , 40:2060–2080, 2024. 

- [121] Long Kiu Chung, Wonsuhk Jung, Chuizheng Kong, and Shreyas Kousik. Goal-Reaching Trajectory Design Near Danger with Piecewise Affine Reach-Avoid Computation. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. doi: 10.15607/RSS.2024.XX.117. 

- [122] Long Kiu Chung, Wonsuhk Jung, Srivatsank Pullabhotla, Parth Shinde, Yadu Sunil, Saihari Kota, Luis F. W. Batista, Cédric Pradalier, and Shreyas Kousik. Guaranteed Reach-Avoid for Black-Box Systems through Narrow Gaps via Neural Network Reachability. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 2326–2333, 2025. 

- [123] Glen Chou, Necmiye Ozay, and Dmitry Berenson. Safe Output Feedback Motion Planning from Images via Learned Perception Modules and Contraction Theory. In _International Workshop on the Algorithmic Foundations of Robotics (WAFR)_ , pages 349–367, 2022. 

- [124] Daniel Heß, Matthias Althoff, and Thomas Sattel. Formal Verification of Maneuver Automata for Parameterized Motion Primitives. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1474–1481, 2014. 

- [125] Christian Pek and Matthias Althoff. Fail-Safe Motion Planning for Online Verification of Autonomous Vehicles Using Convex Optimization. _IEEE Transactions on Robotics_ , 37(3):798–814, 2021. 

- [126] Jakob Thumm and Matthias Althoff. Provably Safe Deep Reinforcement Learning for Robotic Manipulation in Human Environments. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6344–6350, 2022. 

- [127] Roland Stolz, Hanna Krasowski, Jakob Thumm, Michael Eichelbeck, Philipp Gassert, and Matthias Althoff. Excluding the Irrelevant: Focusing Reinforcement Learning through Continuous Action Masking. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 37, pages 95067–95094, 2024. 

- [128] Caelan Reed Garrett, Rohan Chitnis, Rachel Holladay, Beomjoon Kim, Tom Silver, Leslie Pack Kaelbling, and Tomás Lozano-Pérez. Integrated Task and Motion Planning. _Annual Review of Control, Robotics, and Autonomous Systems_ , 4: 265–293, 2021. 

- [129] Siddharth Srivastava, Eugene Fang, Lorenzo Riano, Rohan Chitnis, Stuart Russell, and Pieter Abbeel. Combined Task and Motion Planning through an Extensible Planner-Independent Interface Layer. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2014. 

30 

- [130] Zhiyuan Zhou, Pranav Atreya, You Liang Tan, Karl Pertsch, and Sergey Levine. AutoEval: Autonomous Evaluation of Generalist Robot Manipulation Policies in the Real World. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [131] Mingtong Dai, Lingbo Liu, Yongjie Bai, Yang Liu, Zhouxia Wang, Rui SU, Chunjie Chen, Liang Lin, et al. RoVer: Robot Reward Model as Test-Time Verifier for Vision-Language-Action Model. _arXiv preprint arXiv:2510.10975_ , 2025. 

- [132] Shahram Najam Syed, Arthur Jakobsson, Haoran Hao, and Jeffrey Ichnowski. Intercepting the Future: Latent-Space Predictive World Model for Dynamic VLA Manipulation. _arXiv preprint arXiv:2606.02486_ , 2026. 

- [133] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, Ziwei Wang, et al. VLA-RL: Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning. _arXiv preprint arXiv:2505.18719_ , 2025. 

- [134] Yu Zhang, Yuqi Xie, Huihan Liu, Rutav Shah, Michael Wan, Linxi Fan, and Yuke Zhu. SCIZOR: A Self-Supervised Approach to Data Curation for Large-Scale Imitation Learning. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2026. 

- [135] Youhe Feng, Hansen Shi, Haoyang Li, Xinlei Guo, Yang Wang, Chengyang Zhang, Jinkai Zhang, Xiaohan Zhang, et al. ProcVLM: Learning Procedure-Grounded Progress Rewards for Robotic Manipulation. _arXiv preprint arXiv:2605.08774_ , 2026. 

- [136] Yanru Wu, Weiduo Yuan, Ang Qi, Vitor Guizilini, Jiageng Mao, and Yue Wang. Large reward models: Generalizable online robot reward generation with vision-language models, 2026. 

- [137] Yuheng Ji, Yuyang Liu, Huajie Tan, Xuchuan Huang, Fanding Huang, Yijie Xu, Cheng Chi, Yuting Zhao, Huaihai Lyu, Peterson Co, Mingyu Cao, Qiongyu Zhang, Zhe Li, Enshen Zhou, Pengwei Wang, Zhongyuan Wang, Shanghang Zhang, and Xiaolong Zheng. PRM-as-a-Judge: A dense evaluation paradigm for fine-grained robotic auditing, 2026. 

- [138] Sumedh A. Sontakke, Jesse Zhang, Sébastien M. R. Arnold, Karl Pertsch, Erdem Biıyik, Dorsa Sadigh, Chelsea Finn, and Laurent Itti. RoboCLIP: One demonstration is enough to learn robot policies. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 36, 2023. 

- [139] Yash Jangir, Yidi Zhang, Pang-Chi Lo, Kashu Yamazaki, Chenyu Zhang, Kuan-Hsun Tu, Tsung-Wei Ke, Lei Ke, Yonatan Bisk, and Katerina Fragkiadaki. RobotArena ∞: Scalable robot benchmarking via real-to-sim translation. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2026. 

- [140] Sizhe Zhao, Shengping Zhang, Shuo Yang, Weiyu Zhao, Shuigen Wang, and Xiangyang Ji. TapSampling: InferenceTime Sampling with a Task-Progress-Understanding Verifier for Robotic Manipulation. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2026. 

- [141] Wenhao Li, Xiu Su, Yichao Cao, Hongyan Xu, Xiaobo Xia, Shan You, Yi Chen, Chang Xu, et al. VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model. _arXiv preprint arXiv:2605.01194_ , 2026. 

- [142] Wen Ye, Peiyan Li, Tingyu Yuan, Yuan Xu, Xiangnan Wu, Chaoyang Zhao, Jing Liu, Nianfeng Liu, et al. E-TTS: A New Embodied Test-Time Scaling Framework for Robotic Manipulation. _arXiv preprint arXiv:2606.27268_ , 2026. 

- [143] Sruthi Sudhakar, Junbang Liang, Sreehari Rammohan, Pavel Tokmakov, Richard Zemel, and Carl Vondrick. Robot Critics that Sweat the Small Stuff. _arXiv preprint arXiv:2606.21572_ , 2026. 

- [144] Yufei Wang, Zhanyi Sun, Jesse Zhang, Zhou Xian, Erdem Biyik, David Held, and Zackory Erickson. RL-VLM-F: Reinforcement Learning from Vision Language Foundation Model Feedback. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2024. 

- [145] Martin Klissarov, Pierluca D’Oro, Shagun Sodhani, Roberta Raileanu, Pierre-Luc Bacon, Pascal Vincent, Amy Zhang, and Mikael Henaff. Motif: Intrinsic motivation from artificial intelligence feedback. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [146] Zhihao Wang, Jianxiong Li, Yu Cui, Yuan Gao, Xianyuan Zhan, Junzhi Yu, and Xiao Ma. World value models for robotic manipulation, 2026. 

- [147] Ruixiang Wang, Qingming Liu, Yueci Deng, Guiliang Liu, Zhen Liu, and Kui Jia. EVA: Aligning video world models with executable robot actions via inverse dynamics rewards, 2026. 

- [148] Hengtao Li, Pengxiang Ding, Runze Suo, Yihao Wang, Zirui Ge, Dongyuan Zang, Kexian Yu, Mingyang Sun, et al. VLA-RFT: Vision-Language-Action Reinforcement Fine-tuning with Verified Rewards in World Simulators. _arXiv preprint arXiv:2510.00406_ , 2025. 

- [149] Seyed Kamyar Seyed Ghasemipour, Ayzaan Wahid, Jonathan Tompson, Pannag Sanketi, and Igor Mordatch. SelfImproving Embodied Foundation Models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [150] Guanxing Lu, Rui Zhao, Haitao Lin, He Zhang, and Yansong Tang. Human-in-the-loop Online Rejection Sampling for Robotic Manipulation. _arXiv preprint arXiv:2510.26406_ , 2025. 

- [151] Joey Hejna, Suvir Mirchandani, Ashwin Balakrishna, Annie Xie, Ayzaan Wahid, Jonathan Tompson, Pannag Sanketi, Dhruv Shah, et al. Robot Data Curation with Mutual Information Estimators. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [152] Geon-Hyeong Kim, Seokin Seo, Jongmin Lee, Wonseok Jeon, HyeongJoo Hwang, Hongseok Yang, and Kee-Eung Kim. DemoDICE: Offline imitation learning with supplementary imperfect demonstrations. In _International Conference on Learning Representations (ICLR)_ , 2022. URL `https://openreview.net/forum?id=BrPdX1bDZkQ` . 

31 

- [153] Open X-Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, et al. Open X-Embodiment: Robotic Learning Datasets and RT-X Models. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- [154] Suneel Belkhale, Yuchen Cui, and Dorsa Sadigh. Data Quality in Imitation Learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2023. 

- [155] Fanqi Lin, Yingdong Hu, Pingyue Sheng, Chuan Wen, Jiacheng You, and Yang Gao. Data Scaling Laws in Imitation Learning for Robotic Manipulation. In _International Conference on Learning Representations (ICLR)_ , 2025. 

- [156] Ralf Römer, Adrian Kobras, Luca Worbis, and Angela P. Schoellig. Failure Prediction at Runtime for Generative Robot Policies. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [157] Chen Xu, Tony Khuong Nguyen, Emma Dixon, Christopher Rodriguez, Patrick Miller, Robert Lee, et al. Can We Detect Failures Without Failure Data? Uncertainty-Aware Runtime Failure Detection for Imitation Learning Policies. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- [158] Jinghan Yang, Yunchao Zhang, Wang Yuan, Haolun Wan, Jiaming Zhang, Zhengyang Hu, and Yanchao Yang. Tri-Info: Generalizable, Interpretable Failure Prediction for VLA Models via Information Theory. _arXiv preprint arXiv:2606.19998_ , 2026. 

- [159] Quentin Garrido, Nicolas Ballas, Mahmoud Assran, Adrien Bardes, Laurent Najman, Michael Rabbat, et al. Intuitive physics understanding emerges from self-supervised pretraining on natural videos. _arXiv preprint arXiv:2502.11831_ , 2025. 

- [160] Isaac R. Ward, Michelle Ho, Houjun Liu, Aaron Feldman, Joseph Vincent, Liam Kruse, Sean Cheong, Duncan Eddy, Mykel J. Kochenderfer, and Mac Schwager. Foundational world models accurately detect bimanual manipulator failures. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2026. 

- [161] Somil Bansal, Mo Chen, Sylvia Herbert, and Claire J. Tomlin. Hamilton-jacobi reachability: A brief overview and recent advances. In _2017 IEEE 56th Annual Conference on Decision and Control (CDC)_ , pages 2242–2253, 2017. doi: 10.1109/CDC.2017.8263977. 

- [162] Matthew Kim, Kensuke Nakamura, and Andrea Bajcsy. What You Don’t Know Can Hurt You: How Well do Latent Safety Filters Understand Partially Observable Safety Constraints? _arXiv preprint arXiv:2510.06492_ , 2025. 

- [163] Junwon Seo, Kensuke Nakamura, and Andrea Bajcsy. Uncertainty-aware latent safety filters for avoiding out-ofdistribution failures. In _Conference on Robot Learning (CoRL)_ , 2025. 

- [164] Kensuke Nakamura, Arun L. Bishop, Steven Man, Aaron M. Johnson, Zachary Manchester, and Andrea Bajcsy. How to train your latent control barrier function: Smooth safety filtering under hard-to-model constraints. In _Learning for Dynamics and Control Conference (L4DC)_ , 2026. 

- [165] Paul Lutkus, Kaiyuan Wang, Lars Lindemann, and Stephen Tu. Latent Representations for Control Design with Provable Stability and Safety Guarantees. In _IEEE Conference on Decision and Control (CDC)_ , pages 2937–2944, 2025. 

- [166] Duy P. Nguyen, Kai-Chieh Hsu, Wenhao Yu, Jie Tan, and Jaime F. Fisac. Gameplay Filters: Robust Zero-Shot Safety through Adversarial Imagination. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [167] Jack Parker-Holder, Minqi Jiang, Michael Dennis, Mikayel Samvelyan, Jakob Foerster, Edward Grefenstette, et al. Evolving Curricula with Regret-Based Environment Design. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2022. 

- [168] Michael Dennis, Natasha Jaques, Eugene Vinitsky, Alexandre Bayen, Stuart Russell, Andrew Critch, et al. Emergent Complexity and Zero-shot Transfer via Unsupervised Environment Design. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. 

- [169] Paweł Budzianowski, Emilia Wiśnios, Michał Tyrolski, Gracjan Góral, Igor Kulakov, Viktor Petrenko, et al. OpenGVL – Benchmarking Visual Temporal Progress for Data Curation. _arXiv preprint arXiv:2509.17321_ , 2025. 

- [170] Abhishek Jindal, Dmitry Kalashnikov, R. Alex Hofer, Oscar Chang, Divya Garikapati, Anirudha Majumdar, et al. Can AI Perceive Physical Danger and Intervene? _arXiv preprint arXiv:2509.21651_ , 2025. 

- [171] Jialiang Fan, Weizhe Xu, Oleg Sokolsky, Insup Lee, and Fanxin Kong. SafeVLA-Bench: A Benchmark for the Success-Safety Gap in Vision-Language-Action Models. _arXiv preprint arXiv:2606.00773_ , 2026. 

- [172] Sattyam Jain. Provael: Red-teaming vision-language-action robot policies in simulation, 2026. URL `https: //github.com/provael/provael` . Open-source repository, v0.41.2. 

- [173] TRI LBM Team, Jose Barreiros, Andrew Beaulieu, Aditya Bhat, Rick Cory, Eric Cousineau, et al. A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation. _Science Robotics_ , 2026. 

- [174] Sergey Arkhangelskiy. PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology. _arXiv preprint arXiv:2605.29710_ , 2026. 

- [175] Joseph A. Vincent, Haruki Nishimura, Masha Itkina, Paarth Shah, Mac Schwager, and Thomas Kollar. How generalizable is my behavior cloning policy? a statistical approach to trustworthy performance evaluation. _IEEE Robotics and Automation Letters_ , 9(10):8619–8626, 2024. 

- [176] David Snyder, Asher James Hancock, Apurva Badithela, Emma Dixon, Patrick Miller, Rares Andrei Ambrus, Anirudha Majumdar, Masha Itkina, et al. Is Your Imitation Learning Policy Better than Mine? Policy Comparison with Near-Optimal Stopping. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

32 

- [177] David Snyder, Apurva Badithela, Nikolai Matni, George Pappas, Anirudha Majumdar, Masha Itkina, and Haruki Nishimura. Beyond Binary Success: Sample-Efficient and Statistically Rigorous Robot Policy Comparison. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2026. 

- [178] Abrar Anwar, Rohan Gupta, Zain Merchant, Sayan Ghosh, Willie Neiswanger, and Jesse Thomason. Efficient Evaluation of Multi-Task Robot Policies With Active Experiment Selection. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [179] Rishabh Agarwal, Max Schwarzer, Pablo Samuel Castro, Aaron Courville, and Marc G. Bellemare. Deep reinforcement learning at the edge of the statistical precipice. In _Advances in Neural Information Processing Systems (NeurIPS)_ , volume 34, pages 29304–29320. Curran Associates, Inc., 2021. URL `https://proceedings.neurips.cc/ paper_files/paper/2021/file/f514cec81cb148559cf475e7426eed5e-Paper.pdf` . 

- [180] Aaditya Ramdas, Peter Grünwald, Vladimir Vovk, and Glenn Shafer. Game-theoretic statistics and safe anytime-valid inference. _Statistical Science_ , 38(4):576–601, 2023. doi: 10.1214/23-STS894. 

- [181] Boxiang Qiu, Liliang Chen, Yue Liao, Nan Wang, Lintao Wang, Jiayi Luo, et al. GE-Sim 2.0: A Roadmap Towards Comprehensive Closed-loop Video World Simulators for Robotic Manipulation. _arXiv preprint arXiv:2605.27491_ , 2026. 

- [182] Apurva Badithela, David Snyder, Lihan Zha, Joseph Mikhail, Matthew O’Kelly, Anushri Dixit, and Anirudha Majumdar. Reliable and Scalable Robot Policy Evaluation with Imperfect Simulators. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2026. 

- [183] Xuning Yang, Clemens Eppner, Jonathan Tremblay, Dieter Fox, Stan Birchfield, and Fabio Ramos. Robot policy evaluation for sim-to-real transfer: A benchmarking perspective, 2025. RSS 2025 Workshop on Robot Evaluation for the Real World. 

- [184] Adina Yakefu, Bin Xie, Chongyang Xu, Enwen Zhang, Erjin Zhou, Fan Jia, et al. RoboChallenge: Large-scale real-robot evaluation of embodied policies, 2025. 

- [185] Yejin Kim, Wilbert Pumacay, Omar Rayyan, Max Argus, Winson Han, Eli VanderBilt, et al. MolmoSpaces: A large-scale open ecosystem for robot navigation and manipulation, 2026. 

- [186] Jenai Xuning Yang, Rishit Dagli, Alex Zook, Hugo Hadfield, Ankit Goyal, Stan Birchfield, Fabio Ramos, and Jonathan Tremblay. RoboLab: A high-fidelity simulation benchmark for analysis of task generalist policies. In _Robotics: Science and Systems (RSS)_ , Sydney, Australia, 2026. 

- [187] Yang Yu, Shiyuan Zhang, Yifei Sheng, Haoxiang Ren, and Haoxin Lin. How should world models be evaluated for embodied decision-making? a decision-making-centric position, 2026. 

- [188] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, et al. Evaluating Real-World Robot Manipulation Policies in Simulation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [189] Leo Gao, John Schulman, and Jacob Hilton. Scaling Laws for Reward Model Overoptimization. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2023. 

- [190] Yuheng Zhang, Mingyue Huo, Minghao Zhu, Mengxue Zhang, and Nan Jiang. Beyond Semantic Manipulation: Token-Space Attacks on Reward Models. _arXiv preprint arXiv:2604.02686_ , 2026. 

- [191] Pei-Chi Pan, Yingbin Liang, and Sen Lin. Reward Modeling for Reinforcement Learning-Based LLM Reasoning: Design, Challenges, and Evaluation. _Transactions on Machine Learning Research_ , 2026. 

- [192] Yuchun Miao, Sen Zhang, Liang Ding, Rong Bao, Lefei Zhang, and Dacheng Tao. InfoRM: Mitigating Reward Hacking in RLHF via Information-Theoretic Reward Modeling. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

- [193] Zhibin Duan, Guowei Rong, Zhuo Li, Bo Chen, Mingyuan Zhou, and Dandan Guo. Mitigating Reward Hacking in RLHF via Bayesian Non-negative Reward Modeling. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2026. 

- [194] Anas Mahmoud, MohammadHossein Rezaei, Zihao Wang, Anisha Gunjal, Bing Liu, Yunzhong He, et al. Reward Hacking in Rubric-Based Reinforcement Learning. _arXiv preprint arXiv:2605.12474_ , 2026. 

- [195] Pu Li, Zhigang Lin, Qiang Wu, Yongxuan Lv, Fei Wang, Shan You, et al. Reward as An Agent for Embodied World Models. _arXiv preprint arXiv:2606.19990_ , 2026. 

- [196] Yanjiang Guo, Tony Lee, Lucy Xiaoyang Shi, Jianyu Chen, Percy Liang, and Chelsea Finn. VLAW: Iterative coimprovement of vision-language-action policy and world model. In _International Conference on Machine Learning (ICML)_ , 2026. 

- [197] Yanan Wang, Renxi Wang, Yongxin Wang, Xuezhi Liang, Fajri Koto, Timothy Baldwin, Xiaodan Liang, Haonan Li, et al. SimuScene: Training and Benchmarking Code Generation to Simulate Physical Scenarios. _arXiv preprint arXiv:2602.10840_ , 2026. 

- [198] Ryan J. Tibshirani, Rina Foygel Barber, Emmanuel J. Candes, and Aaditya Ramdas. Conformal Prediction Under Covariate Shift. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2019. 

- [199] Rina Foygel Barber, Emmanuel J. Candes, Aaditya Ramdas, and Ryan J. Tibshirani. Conformal prediction beyond exchangeability. _The Annals of Statistics_ , 2023. 

33 

- [200] Juan C. Perdomo, Tijana Zrnic, Celestine Mendler-Dünner, and Moritz Hardt. Performative Prediction. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2020. 

- [201] Isaac Gibbs and Emmanuel Candès. Adaptive Conformal Inference Under Distribution Shift. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021. 

- [202] Hadas Kress-Gazit, Kunimatsu Hashimoto, Naveen Kuppuswamy, Paarth Shah, Phoebe Horgan, Gordon Richardson, et al. Robot Learning as an Empirical Science: Best Practices for Policy Evaluation. _arXiv preprint arXiv:2409.09491_ , 2024. 

- [203] Jaideep Ray. Before the model learns the bug: Fuzzing RLVR verifiers, 2026. 

34 

