---
title: "A Physics-Consistent Benchmark for Contact-Rich Human-Robot Interaction in Assistive Care"
date: "2026-09-02"
authors: "Chengxiao He; Shanghai Yuan; Liuqun Fan; Shenzhen Zhu"
url: https://arxiv.org/abs/2609.02402
pdf: https://arxiv.org/pdf/2609.02402
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.02402)** / [論文ページ](https://arxiv.org/abs/2609.02402)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# A Physics-Consistent Benchmark for Contact-Rich Human–Robot Interaction in Assistive Care 

Chengxiao He<sup>1,†</sup> , Shenghai Yuan<sup>2,†</sup> , Liuqun Fan<sup>1,*</sup> , and Shenzhe Zhu<sup>3</sup> 

> 1 _School of Mechanical and Robotics Engineering, Tongji University_ , Shanghai, China 

> 2 _Centre for Advanced Robotics Technology Innovation, Nanyang Technological University_ , Singapore 

> 3 _College of Electronic and Information Engineering, Tongji University_ , Shanghai, China 

_{_ 2130238,lqfan,2531819 _}_ @tongji.edu.cn, shyuan@ntu.edu.sg 

**_Abstract_ —Conventional task-level evaluation asks whether a robot policy completes a specified action, but can miss failures that emerge only during physical human contact. This limitation is critical in contact-rich assistive tasks, where meaningful evaluation requires a physically responsive human, interactionquality assessment beyond task success, and a leak-free observation protocol. We introduce a physics-consistent benchmark for contact-rich human–robot interaction, instantiated in robotassisted bathing. The benchmark combines a deformable, passively responding human, physics-aware scores alongside tasklevel success, and a frozen vision-only / scorer-only evaluation protocol. To establish physical validity, region-wise simulated responses are calibrated against force–indentation measurements from Franka impedance pushes on a medical-care manikin. Under a frozen T1–T7 protocol with 140 runs per method, an LLMaugmented state machine (State Machine) achieves** 72 _._ 9% **task success but drops to** 56 _._ 4% **after correct-region and force-safety screening; VoxPoser produces lighter and more stable contact but completes only** 27 _._ 9% **of trials; and zero-shot** _π_ 0 _._ 5 **achieves** 0 _._ 7% **task success with no correct-region or safety-gated successes. These results show that task completion alone does not imply physically valid contact and motivate physics-aware screening before deployment of contact-rich assistive robot policies. Code and benchmark assets are available at https://anonymous.4open. science/r/Physics-Consistent-Benchmark** **<u>4 HRC-8DBF/.</u>** 

**_Index Terms_ —contact-rich human-robot interaction, simulation benchmark, physics-aware evaluation, assistive care** 

## I. INTRODUCTION 

Contact-rich human–robot interaction poses an evaluation challenge that conventional task-level metrics do not capture. This challenge is particularly evident in assistive-care tasks such as robot-assisted bathing, where physical contact is intrinsic to task execution. Unlike tabletop manipulation, where the environment can often be treated as rigid and success can be decided geometrically, physical interaction with a human body involves deformation, passive joint motion, contact force, and joint-limit constraints. A policy may reach the instructed body region while exerting excessive force, approaching a joint limit, or failing to maintain stable contact. Task completion therefore does not imply physically valid contact. 

Despite progress in assistive robotics and human–robot interaction, existing benchmarks remain limited in three respects. The physical response of the human is often simpli- 

> †Equal contribution. 

*Corresponding author: Liuqun Fan. 

fied as rigid or motion-replayed; for example, safety-aware HRC benchmarks such as Human-Robot Gym incorporate learning and online constraints but evaluate interaction with a motion-driven human [1], preventing contact-induced deformation, force transmission, and passive joint motion from emerging. Meanwhile, care systems such as Manip4Care and VTTB, together with language-grounding and foundationmodel pipelines including VoxPoser and _π_ 0 _._ 5, primarily evaluate whether a task is completed through success, trajectory, or collision measures rather than how physical contact is executed [2]–[8]. Finally, simulation-based protocols may expose privileged states such as ground-truth joint angles, soft-anchor states, or future contact labels to the tested policy, confounding policy capability with simulator access and breaking the intended sim-to-real observation contract. 

These limitations raise three **challenges** : how to model a human physically responding to robot contact, how to evaluate interaction quality beyond task success, and how to separate policy-visible observations from scorer-only physical states. 

To address these challenges, we introduce a physicsconsistent benchmark for evaluating robot policies under contact-rich human–robot interaction in assistive care, instantiated and evaluated in robotic bathing. Figure 1 summarizes the resulting human-in-the-loop pipeline and illustrates passive human motion under robot contact. The benchmark combines a deformable, passively responding human, physics-aware scores with task-level success as a baseline, and a frozen vision-only / scorer-only protocol. To establish physical validity of the environment, we calibrate simulated region-wise responses against force–indentation measurements on a medicalcare manikin. This correspondence grounds the benchmark; it is not offered as a standalone real-to-sim method. We do not introduce a new deformable solver: the physics stack is an implementation abstraction [9]–[12], and fidelity is judged by measured contact agreement rather than by solver novelty. 

The benchmark’s finding is that task-level scores can hide contact failure. Post-hoc physical screening can distinguish nominal task success from deployment-usable success: State Machine drops from 102 _/_ 140 to 79 _/_ 140 under a safety gate, while _π_ 0 _._ 5 retains 0 _/_ 140 gated success after 1 _/_ 140 original success. Our contributions are: 

1) A physics-consistent benchmark for contact-rich 


Fig. 1. Overview of the benchmark architecture and its contact-responsive human-in-the-loop evaluation. Language and RGB-D observations are processed by visual perception and spatial/language grounding before a policy/planner generates contact-aware robot actions. The benchmark environment contains an articulated human with deformable soft tissue and passive response; the two rendered interaction states illustrate contact-induced human motion. The resulting physical interaction is evaluated through C1 peak force, C2 joint-limit margin, C4 motion activity, and C5 force stability. Red links denote the physical-response and scoring pathway missing from conventional task-level benchmarks. 

human–robot interaction in assistive care, instantiated in robotic bathing as T1–T7 Touch / Scrub / Push. 

- 2) A benchmark construction with three necessary parts: a deformable, passively responding environment; manikincalibrated contact response; and a frozen vision-only / scorer-only protocol. 

- 3) A diagnostic evaluation of State Machine, VoxPoser, and a zero-shot _π_ 0 _._ 5 transfer probe revealing methodspecific failure modes in force, joint-limit margin, contact stability, and region grounding, and showing that task completion does not imply physically valid contact. 

The benchmark implementation and evaluation configurations are available at URL. 

Section 2 reviews the evaluation gap. Section 3 specifies the benchmark design. Section 4 reports environment validity and then the hidden failures. Section 5 states the finding. 

## II. RELATED WORK 

## _A. Care Systems and Policy Evaluation_ 

Early care systems such as I-SUPPORT explored pneumatic soft manipulators for elderly bathing [13], [14]. Manip4Care addresses limb grasping and repositioning for bed bathing [2]; VTTB studies visuo-tactile bed-bathing imitation on medical manikins [3]. These works show that robots can complete local care subtasks. They demonstrate task completion, not a reusable protocol that scores physical contact under a frozen observation contract. In parallel, language grounding 

and foundation VLA training have advanced rapidly [4], [5]. VoxPoser and ReKep map language to spatial value maps or keypoint constraints [6], [7]; end-to-end models such as _π_ 0, _π_ 0 _._ 5, and OpenVLA improve continuous control and open-set generalization [8], [15]. FAM-HRI further explores multimodal interaction for limited-mobility users [16]. Strong scores on general manipulation benchmarks, however, do not imply safe sustained contact with a deformable human body. 

## _B. Why Task-Level Benchmarks Miss Contact_ 

Human-Robot Gym provides a safety-aware HRC RL benchmark, but its human model is primarily motion-capture driven [1]. Soft-body methods including XPBD, VBD, SoftMAC, skeleton–soft coupling, and industrial engines such as Newton improve physical realism [9]–[12], [17]. For this paper, such engines are _infrastructure_ : the claim is a physicsconsistent benchmark with a calibrated human response. Accordingly, we judge the environment by real-to-sim agreement rather than by timestep or convergence contests against general-purpose engines. 

On the scoring side, ISO 15066 specifies collaborative force limits by body region [18]. Those limits are fixed rather than context-dependent, and the standard does not provide a reusable apparatus for scoring contact quality under a frozen observation contract. Behrens et al. report regionwise biomechanical pain-onset forces [19]; PrioriTouch discusses conservative scaling of those limits for contact preference [20]. Reviews of mental workload in HRI identify 

robot motion, rhythm, and predictability as workload-relevant factors [21]. Language-conditioned manipulation suites such as LIBERO and dataset-scale policy evaluation such as Open X-Embodiment complement this literature, but they are not designed around passive human joints or calibrated contact force [4], [22]. 

Existing systems provide important but largely separate ingredients, including care-task execution, deformable simulation, physical safety criteria, and policy evaluation. However, they do not jointly provide a deformable and passively responding human, calibrated contact response, leakfree policy observations, and physics-aware scoring within a unified evaluation protocol. Table I positions our benchmark with respect to these capabilities in the evaluated setting. Rather than introducing another task or simulation engine, our benchmark integrates these elements to evaluate whether successful contact-rich interaction is also physically valid. 

## III. BENCHMARK DESIGN 

The benchmark is specified as environment, tasks, then evaluation protocol. Detailed coupling derivations are provided in the supplementary material. We define physics consistency at the benchmark level rather than at the solver level. A benchmark is physics-consistent when (i) its simulated human response exhibits measurable correspondence with real interaction within the evaluated contact regime, (ii) contactinduced physical states—force, deformation, and passive joint motion—are dynamically generated rather than prescribed, and (iii) these states are evaluated without exposing privileged simulator information to the tested policy. The resulting properties are physical realism, physical validity, evaluation validity, and diagnostic capability. 

## _A. Benchmark Environment_ 

The benchmark requires a human that responds physically to contact rather than a kinematic target, together with an observation interface that evaluated policies can consume without simulator-state leakage. 

_a) Representation.:_ The simulated care recipient combines an articulated rigid skeleton with region-wise deformable soft-tissue shells. Body regions follow the kinematic joint tree: load-bearing areas (forearm, upper arm, abdomen, and related torso/limb patches) use flexible surface shells anchored to associated bone segments, while low-compliance parts (e.g., fingers and head) may be treated as rigid. Passive joint behavior is always enabled so that contact forces can induce posture change without an active human controller. Local deformation, force transmission, and passive response are environment requirements. 

_b) Physical interaction.:_ We use an existing physics simulation framework as an implementation abstraction and construct a benchmark environment whose physical response can be calibrated against real human–robot contact. The following equations summarize shell–bone load transfer in our stack. Contact on a soft region deforms the shell, transmits force to the skeleton through regional anchors, and can move passive 

TABLE I 

COMPARISON OF BENCHMARK-LEVEL CAPABILITIES RELEVANT TO OUR EVALUATION SETTING. 

|System|DHS|PJR|FC|LFO|PAS|
|---|---|---|---|---|---|
|Human-Robot|✗|✗|■|■|■|
|Gym [1]||||||
|LIBERO [22]|✗|✗|✗|■|✗|
|Open|✗|✗|✗|■|✗|
|X-Embodiment [4]||||||
|This benchmark|✓|✓|✓|✓|✓|


DHS: deformable-human simulation; PJR: passive-joint response; FC: force calibration; LFO: leak-free observation; PAS: physics-aware scoring. ✓: supported; ■: partially supported; ✗: not supported. Open X-Embodiment is dataset-scale policy evaluation rather than a protocol benchmark. 

joints. With skeleton coordinates _q_ , stacked shell coordinates _x_ , region-anchor Jacobians _Jc,r_ , and stacked anchor reaction _fc_ , 


where _S_ selects shell-side anchors, _fc_ = col( _fc_<sup>(1)</sup> _, . . . , fc_<sup>(</sup><sup>_R_)</sup> ), and _ϕ_ is the stacked anchor residual between shell and bone targets. The supplementary material provides symbol tables and solver variants. For evaluation, the consequence is behavioral: policies face deformation, tissue-mediated force, and passive joint motion—not a rigid mannequin. 

_c) Observation interface.:_ To keep evaluation leakagefree, the platform separates physics state from planner-visible perception. Rigid bones and flexible shells participate in mechanics only; an SMPL-X [23] visual skin is driven unidirectionally from _q_ for rendering. A virtual camera and robot TCP pose feed a snapshot query interface that exposes: 

- 1) RGB and depth images; 

- 2) 3D point clouds; 

- 3) zero-shot semantic segmentation masks for human, robot, and scene entities [24]; 

- 4) skeletal landmarks from vision-based keypoint estimators [25]. 

Ground-truth joint angles, anchor states, and scorer-only contact metadata remain closed to evaluated policies. All semantic and spatial information used by a subject must be inferred from the vision-facing modalities above, which preserves a fair sim-to-real evaluation contract. 

## _B. Benchmark Tasks and Evaluation Dimensions_ 

The suite emphasizes continuous physical interaction with deformable body regions rather than isolated rigid-object manipulation or language-ambiguity puzzles. We evaluate seven micro-tasks on three soft-relevant body regions. Unless noted, each trial starts from a supine care-recipient pose on a nursing bed with randomized comfort-arm orientation in a fixed angular range. Scrub tasks denote sustained sliding cleaning contact in the bathing sense (wipe family), not antipodal grasping. 

TABLE II 

BENCHMARK TASK SET. PUSH ON THE UPPER ARM IS OMITTED BECAUSE THE SHORT MOMENT ARM YIELDS LIMITED DISPLACEMENT DIVERSITY. 

|ID|Task|Purpose / primary cues|
|---|---|---|
|T1|Touch forearm|Contact establishment; localization;<br>force overshoot|
|T2|Push forearm|Deformation and displacement<br>under external force|
|T3|Scrub forearm<br>|Sustained sliding cleaning contact;<br>force stability; contact consistency<br>|
|T4<br>|Touch upper arm<br>|Region-dependent contact response<br>|
|T5|Scrub upper arm|Proximal soft-region scrubbing<br>contact|
|T6|Touch abdomen|Clear soft deformation; soft-contact<br>necessity|
|T7|Scrub abdomen|Soft-region scrubbing; pressure /<br>force distribution|


Natural-language prompts name the region and intent (e.g., “gently touch the right forearm,” “push the forearm,” “gently scrub the abdomen”). Tasks that mainly probe rigid skeletal landmarks without soft-tissue involvement, languageambiguity suites, and arm-reposition skills that reduce to conventional manipulation are excluded from this scoped task set. 

Scorer-only ground truth yields a task-level baseline and physics-aware scores (Table III). These dimensions are particularly relevant to assistive-care interaction; they are defined to describe physical contact, not as clinically validated care scores. 

Peak force is compared with region-wise biomechanical pain-onset limits _F_ pain( _b_ ) from Behrens et al. (Table 8, pinching force): 100 N on forearm muscle, 100 N on deltoid muscle, and 60 N on abdominal muscle [19]. All three task regions use muscle / soft-tissue entries, matching the softrelevant sites of Section III-B. We adopt a single conservative discount _γ_<sup>_′_</sup> = 0 _._ 35 applied uniformly across regions, so _F_ max( _b_ ) = _γ_<sup>_′_</sup> _F_ pain( _b_ ). The resulting safety gates are 35 N / 35 N / 21 N. In this work _F_ pain and _F_ max are two presentations of the same published limit—the literature pain threshold and a more conservative uniform deployment gate—not two independently measured quantities. 

## _C. Evaluation Protocol_ 

Each evaluated method consumes the planner-visible snapshot interface of Section III-A0c. State Machine derives its contact geometry from the initial RGB snapshot through conventional CV segmentation and scripted fitting of candidate contact keypoints and approach directions; no groundtruth coordinates or scorer-only state are provided to it. The protocol freezes the scorer–logger contract used for all trials in Section IV (Table IV). Scorer-only streams never include future contact labels, and vision-facing methods never receive ground-truth joint angles or soft-anchor states. 

## IV. EXPERIMENTS 

We first state how the benchmark is used, then ask whether the environment is physically valid, then whether it separates 

TABLE III 

EVALUATION DIMENSIONS. C3 IS THE TASK-LEVEL BASELINE; C1, C2, C4, AND C5 ARE PHYSICS-AWARE. SYMBOLS MATCH THE SCORER IMPLEMENTATION; ALL QUANTITIES ARE INVISIBLE TO EVALUATED POLICIES. 

|Layer|Metric|Definition|
|---|---|---|
|Physics-<br>aware|C1 Force|Peak _Fpeak_ = max_t ∥Fc_(_t_)_∥_during<br>contact; compared with Behrens<br>Table 8 _F_pain(_b_) and the uniform<br>_γ_<sup>_′_ </sup>= 0_._35 safety gate [19].<br>|
|Physics-<br>aware|C2 Joint-limit<br>margin|_Dlimit_ = min(_q −q_min_, q_max_−q_)<br>for the _simulated care recipient’s joints_<br>(human kinematic limits; not robot<br>joint limits).|
|Task-level|C3 Success|Closed-loop task completion under<br>geometric/contact gates, with failure<br>attribution to perception, planning,<br>execution, or safety truncation.|
|Physics-|C4 Motion|Active-motion fraction<br>|
|aware|activity|_ηact_ =_Tact/Ttotal_ after human settle<br>(pacing / temporal demand [26]).<br>|
|Physics-<br>aware|C5 Force<br>stability|Within-run population SD of _∥Fc∥_<br>over the contact window (lower is more<br>stable). Force–indentation coupling is<br>reported in Section IV-B rather than as<br>a separate deformation score.|


TABLE IV 

UNIFIED EVALUATION PROTOCOL FREEZE. ALL METHODS AND SELECTED TASKS SHARE THIS CONTRACT BEFORE METRIC AGGREGATION. 

|Item|Freeze rule|
|---|---|
|Assets / embodiment|Fixed nursing-bed scene; same human and<br>robot models across methods.|
|Randomization /<br>seeds|Comfort-arm orientation in [45<sup>_◦_</sup>_,_60<sup>_◦_</sup>]; fixed<br>seed set per task–method cell.|
|Trial budget|20 initializations _×_ 7 tasks = 140 runs per<br>method.|
|Success / safety gates|Task-specific geometric and contact gates for<br>C3; _γ_<sup>_′_</sup>-scaled safety force gates and human<br>joint envelopes as safety context.|
|Logger schema|RGB-D, point clouds, masks, robot<br>proprioception; scorer-only force / joint streams<br>offline.|
|Replay|Metrics regenerated from logged trajectories<br>under the same scorer binary.|
|NA rules|No valid contact _⇒_C1/C2/C5 reported as NA<br>and C3 = 0. Valid-data coverage is not C3.|


policies, then what task-level scores miss. Passive-joint response remains a required property of the care recipient, not an optional ablation switch. 

## _A. Benchmark Setup_ 

Before comparing methods, we use scripted probes to check that the scorer–logger parameters respond as intended: increasing commanded push depth increases C1; violating joint envelopes decreases C2; injecting stop–go execution decreases C4; larger within-window force fluctuation increases C5. These probes validate the evaluation apparatus, not the human-model calibration of Section IV-B. Policy runs below inherit the same seed and logging contract. 

_a) Evaluated methods.:_ We instantiate the benchmark with an LLM-augmented state machine (State Machine in 

tables) and VoxPoser on the full T1–T7 suite (20 initializations _×_ 7 tasks = 140 runs per method). The two subjects represent distinct policy paradigms—state-machine control versus spatial reasoning: 

- 1) **LLM-augmented state machine (State Machine in tables)** : an LLM-augmented controller consistent with finite-state coordination used in assistive bathing systems such as I-SUPPORT [27]. The method uses the same leakage-free observation contract as the other methods. From an initial RGB snapshot, conventional CV segmentation estimates the target-region geometry; scripted routines then fit candidate contact keypoints and approach directions and instantiate a bounded set of predefined Cartesian motion primitives, from which the LLM selects according to the language instruction. No ground-truth simulator state or scorer-only signal is used. The method is vision-based at initialization but does not update target geometry during execution, making it a structured, snapshot-conditioned reference rather than an end-to-end learned vision policy. 

- 2) **VoxPoser [6]** : zero-shot 3D value-map trajectories from LLMs/VLMs, using the vision interface of Section III-A0c. 

Separately, we evaluate the publicly released _π_ 0 _._ 5 DROID checkpoint [8] pretrained for Franka Panda generalization (pi05_droid), applied zero-shot to this contact-rich assistive-care setting without additional teleoperation or finetuning. This run is a zero-shot transfer stress test, not a third peer paradigm. 

Figure 2 shows the recorded T1–T7 contact scenes and the force, wrist, and local-deformation streams written by the logger. Metrics follow Section III-B. In later figures, _valid ratio_ is the fraction of runs that produced scoreable contact or trajectory data; it is not C3. Binary rates use Wilson 95% confidence intervals; continuous metrics are reported as medians. 

## _B. Physical Validity of the Benchmark_ 

Real contact trials use a Franka Panda with a gripper under Cartesian impedance control. The contact partner is a medical-care manikin with a compliant surface and movable joints. Each trial records robot pose, contact force, and the displacement needed to reconstruct a force–indentation curve. We do _not_ instrument physical recovery after unload, so unload recovery and energy dissipation are excluded from the real-tosim claim. 

Matched pose schedules, contact locations, and directions are replayed in simulation. Figure 3 shows the forearm and abdomen pushes together with the overlaid force–indentation curves: raw measured trials (gray), the identified response (gold dashed), and the calibrated simulation (blue). Agreement on these curves is the evidence that Flex parameters are calibrated against measured contact responses. The same plots make the force–deformation coupling explicit, which is why deformation is not sold as a separate metric in Table III. 


Fig. 2. Recorded language-conditioned interaction used by the scorer–logger. Left: Touch / Scrub / Push scenes on the forearm, upper arm, and abdomen. Right: logged contact force, wrist displacement, and local deformation. These traces illustrate the logging contract; deformation is not sold as a separate metric. 

The upper-arm simulation reuses the forearm calibration parameters and is not independently calibrated against a real upper-arm response; manikin upper-arm compliance may differ from human tissue, so upper-arm C1/C2/C5 results are benchmark-level comparative scores rather than independent region-specific biomechanical validation. 

## _C. Benchmark Evaluation_ 

Table V organizes the method-level binary results as a progression from evaluator success, through correct-region grounding, to safety-gated deployment success. State Machine attains the highest task-level completion (72 _._ 9% [65 _._ 0 _,_ 79 _._ 5]). That result shows the scorer can recognize successful execution for a structured method in which language selects among vision-derived, script-generated Cartesian candidates. The same method carries a heavy force tail (median peak 19 _._ 48 N) and the second-worst C5 (Table VI), so “finished” and “stable contact” remain distinct. The comparison characterizes distinct failure modes rather than establishing an architecture-neutral policy leaderboard. 

_Gate sensitivity._ We recompute safety-gated success under a continuous sweep of _γ_<sup>_′_</sup> over [0 _._ 20 _,_ 1 _._ 00]. VoxPoser’s and _π_ 0 _._ 5’s gated success remain unchanged throughout this range, at 27 _._ 9% and 0 _._ 0%, respectively. State Machine’s gated success increases monotonically with _γ_<sup>_′_</sup> —for example, 35 _._ 0% at _γ_<sup>_′_</sup> = 0 _._ 20, 56 _._ 4% at _γ_<sup>_′_</sup> = 0 _._ 35, 71 _._ 4% at _γ_<sup>_′_</sup> = 0 _._ 70, and 72 _._ 1% at _γ_<sup>_′_</sup> = 1 _._ 00—but remains below its 72 _._ 9% nominal success and above VoxPoser’s gated success throughout the sweep. We report _γ_<sup>_′_</sup> = 0 _._ 35 as a representative conservative point within this range rather than a precisely calibrated value; the nominal–gated dissociation and method ranking are preserved across the full sweep. 

C4 is an operational stop–go continuity proxy: a higher active-motion fraction indicates fewer execution interruptions. 


Fig. 3. Real-to-sim force–indentation calibration after impedance push on a medical-care manikin. (a) Forearm push. (b) Abdomen push. (c) Forearm force–indentation. (d) Abdomen force–indentation. Gray: measured trials. Gold dashed: identified response. Blue: calibrated simulation. 

### TABLE V 

METHOD-LEVEL BINARY RATES ON T1–T7 (140 RUNS/METHOD) WITH WILSON 95% CIS. SAFETY-GATED DEPLOYMENT SUCCESS REQUIRES ORIGINAL EVALUATOR SUCCESS, CORRECT-REGION CONTACT, AND PEAK FORCE WITHIN THE _γ_<sup>_′_</sup> = 0 _._ 35 GATE. TASK-LEVEL INTERVALS ARE REPORTED IN THE SUPPLEMENTARY MATERIAL. STATE MACHINE USES AN INITIAL RGB SNAPSHOT AND PERFORMS NO EXECUTION-TIME VISUAL REPLANNING. 

|Method|Task success _↑_|Region-correct _↑_|Safety-gated _↑_|
|---|---|---|---|
|SttMhin<sup>_†_</sup>|72.9%|72.9%|56.4%|
|ae ace|(65.0, 79.5)|(65.0, 79.5)|(48.2, 64.4)|
|VP|27.9%|27.9%|27.9%|
|oxoser|(21.1, 35.8)|(21.1, 35.8)|(21.1, 35.8)|
|<sup>_‡_</sup>|0.7%|0.0%|0.0%|
|_π_0_._5|(0.1, 3.9)|(0.0, 2.7)|(0.0, 2.7)|


Cell colors indicate numerical ranking within each column: best, second, worst. _↑_ / _↓_ denotes higher/lower is better.<sup>_†_</sup> State Machine uses an initial RGB snapshot to generate scripted Cartesian candidates and performs no execution-time visual replanning.<sup>_‡_</sup> All recorded _π_ 0 _._ 5 contacts are off-target. 

Robot-motion rhythm and predictability are workload-relevant in HRI [21]; in passive physical contact, stop–go interruptions may therefore be perceived as unpredictable and plausibly increase recipient anxiety. This experiential link is not measured here: C4 quantifies motion continuity only, and the hypothesis remains for future work. 

VoxPoser produces the lightest and most stable conditional contact (C1 1 _._ 46 N, C5 0 _._ 21 N) and a high motion-activity score, yet converts this into C3 only 27 _._ 9% of the time, concentrated on Touch. State Machine and VoxPoser differ in correct-region success and contact-force statistics (Table VII). Low force here is therefore not a contact skill: the motion is often too weak to complete Push or Scrub (Fig. 4(a)–(d)). 

The near-zero success rate of _π_ 0 _._ 5 (0 _._ 7%) is consistent with substantial sensitivity to zero-shot transfer from the DROID / Franka pretraining distribution into this setting. Its scoreable contact set is small (30 force runs, 6 Push-margin runs), and every recorded contact is on a _non-target_ body region. The 

TABLE VI 

POOLED T1–T7 PHYSICS-AWARE SCORES UNDER THE 140-RUN/METHOD PROTOCOL. EACH STATISTIC USES AVAILABLE SCOREABLE RUNS, SO VALID _n_ VARIES BY METRIC AND METHOD. 

|Method|C1 _↓_|C2 _↑_|C4 _↑_|C5 _↓_|
|---|---|---|---|---|
|State Machine|19_._48|_−_3_._61_×_10<sup>_−_4</sup>|0_._788|3_._52|
|VoxPoser|1_._46|_−_4_._07_×_10<sup>_−_4</sup>|0_._883|0_._21|
|_π_0_._5<sup>_†_</sup>|15_._39|_−_1_._37_×_10<sup>_−_3</sup>|0_._999|4_._42|


C1: median peak contact force (N); C2: median signed human joint-limit margin on Push (rad); C4: median active-motion fraction (higher indicates less stop–go execution); C5: median within-run force SD (N). _↑_ / _↓_ denotes higher/lower is better. Cell colors indicate numerical ranking within each directional metric: best, second, worst. _†_ For _π_ 0 _._ 5, C1/C5 statistics come entirely from off-target-region contact. 

TABLE VII 

PRE-SPECIFIED STATE MACHINE VERSUS VOXPOSER CONTRASTS UNDER THE 140-RUN/METHOD PROTOCOL. BINARY TESTS USE ALL TRIALS; CONTINUOUS TESTS USE AVAILABLE SCOREABLE RUNS. THESE ARE NOT A FULL PAIRWISE SCREEN; _π_ 0 _._ 5 IS OMITTED. 

|Outcome|Test|_p_|
|---|---|---|
|Correct-region success|Fisher exact|4_._74_×_10<sup>_−_14</sup>|
|Safety-gated success|Fisher exact|1_._99_×_10<sup>_−_6</sup>|
|Peak contact force|Mann–Whitney _U_|5_._72_×_10<sup>_−_40</sup>|
|Within-run force SD|Mann–Whitney _U_|4_._75_×_10<sup>_−_40</sup>|


C1/C5 numbers for _π_ 0 _._ 5 must not be read as target-region contact forces. Figure 4(e) shows TCP trajectories that fail to lock onto the instructed region. 

## _D. What Conventional Evaluation Misses_ 

For failure-mode analysis, we condition on trials that fail the region-correctness criterion; percentages therefore use these failed trials rather than all trials as the denominator (38 / 101 / 140 for State Machine / VoxPoser / _π_ 0 _._ 5). 

Region-wise contact (Table VIII) separates reaching the instructed site from finishing the action. State Machine and VoxPoser both establish target-region contact on 95 _._ 0% of forearm runs, yet VoxPoser’s original-evaluator success on that same forearm task set is only 33 _._ 3%: contact is not completion. _π_ 0 _._ 5 records 0 target-region contacts in all three sites. Valid ratio in Fig. 4 remains scoreable-data coverage, not C3. 

The main diagnostic is VoxPoser. Region-wise scores show a systematic gap between reaching a site and sustaining contact: on Touch, target-region contact is comparable to State Machine, yet Scrub and Push completion collapse, and the dominant failure is insufficient progress (68 _/_ 101) rather than localization error. High motion activity (C4 0 _._ 883) does not convert into task progress, consistent with persistent but poorly directed motion around a safety-oriented objective; C4 and C3 together show that a single score cannot decide effectiveness. Value-map methods that treat a safety-proxy metric as the sole objective can therefore reduce contact to a safe but ineffective regime. A concrete implication is that the value map’s role may need to narrow once contact is established: rather than continuing to shape the trajectory toward a low-cost configuration, a later phase can be driven by an explicit progress objective—for example a target sliding 


Fig. 4. Language-conditioned evaluation on T1–T7. (a) Touch contact force (run mean and within-run SD). (b) Scrub contact force. (c) Scrub effective stroke. (d) Push displacement, human joint-limit margin, and forearm force. (e) _π_ 0 _._ 5 TCP trajectories. (f) Motion-activity ratio (C4). (g) Primary failure mode by method. Valid ratio is scoreable-data coverage, not closed-loop success. Force and TCP panels for _π_ 0 _._ 5 show off-target-region contact. In (g) the denominator is failure runs after excluding correct-region successes (38 / 101 / 140 for State Machine / VoxPoser / _π_ 0 _._ 5); the single original-evaluator success of _π_ 0 _._ 5 is off-target and remains in the failure analysis. 

distance of the kind already reported as effective stroke for Scrub (Fig. 4(c)), or a target indentation of the kind already reported as wrist displacement for Push (Fig. 4(d))—so that sustained contact is driven by a progress signal rather than a safety proxy. Reaching and sustained-contact phases may therefore warrant distinct control regimes rather than a single value-map objective throughout. 

State Machine supplies a shorter supporting point: even with a structured candidate generator that deliberately narrows the action space, it still carries a force tail and drops from 102 _/_ 140 to 79 _/_ 140 under the safety gate (36 _/_ 140 exceedances, of which only a subset were originally successful and regioncorrect). The benchmark therefore still surfaces physical problems in a constrained reference with strong geometric scaffolding. 

The _π_ 0 _._ 5 outcome remains a short transfer probe: 1 _/_ 140 original success, 0 _/_ 140 correct-region success, and 0 _/_ 140 

gated success, consistent with sensitivity to zero-shot transfer from the DROID / Franka pretraining distribution. Its failures are almost entirely no target contact (106 _/_ 140) plus off-target contact (30 _/_ 140). Safe interaction is therefore not the same as effective interaction. More broadly, task completion does not imply physically valid contact. The benchmark can serve as a pre-deployment physical/safety screen for contact-rich care policies. 

## V. CONCLUSION 

This study uses 20 trials per task and is intended for benchmark characterization rather than population-level statistical estimation. The contact partner is a medical-care manikin, not human tissue; the upper-arm simulation reuses the forearm calibration; _Kc_ / _Dc_ sensitivity is not systematically studied; and the evaluated set is limited to a LLM-augmented statemachine reference, a spatial-reasoning planner, and one zero- 

TABLE VIII 

REGION-WISE CONTACT OUTCOMES ON T1–T7. RANKINGS ARE EVALUATED WITHIN EACH BODY REGION. 

|Region|Method|Target _↑_|Off-tgt _↓_|No-<br>contact _↓_|C3 _↑_|
|---|---|---|---|---|---|
|Forearm|State<br>Machine|57_/_60|0|0|54_/_60|
|Forearm|VoxPoser|57_/_60|0|2_/_60|20_/_60|
|Forearm|_π_0_._5|0|19_/_60|40_/_60|1_/_60|
|Upper arm|State<br>Machine|37_/_40|0|0|25_/_40|
|Upper arm|VoxPoser|34_/_40|0|3_/_40|11_/_40|
|Upper arm|_π_0_._5|0|6_/_40|32_/_40|0|
|Abdomen|State<br>Machine|39_/_40|0|0|23_/_40|
|Abdomen|VoxPoser|30_/_40|0|9_/_40|8_/_40|
|Abdomen|_π_0_._5|0|5_/_40|34_/_40|0|


Target: target-region contact; Off-tgt: off-target contact; No-contact: completed without contact; C3: original evaluator success. _↑_ / _↓_ denotes higher/lower is better. Cell colors indicate numerical ranking within each body region: best, second, worst; ties share the same color. Denominators are 60 runs for forearm and 40 runs each for upper arm and abdomen. Process failures are omitted from these columns: State Machine 3 _/_ 3 _/_ 1, VoxPoser 1 _/_ 3 _/_ 1, and _π_ 0 _._ 5 1 _/_ 2 _/_ 1 for forearm/upper arm/abdomen, respectively. All established _π_ 0 _._ 5 contacts are off-target. 

shot Franka-DROID checkpoint. State Machine instead builds a bounded set of scripted Cartesian candidates from an initial RGB snapshot and lets the LLM select among them, without execution-time visual replanning or privileged simulator state. The instantiation is a single robotic-bathing scenario. 

Within that scope, conventional task-level evaluation can hide contact failures. The physics-consistent benchmark makes those dissociations measurable: State Machine can finish with an unstable force tail, VoxPoser can remain light without completing sustained contact, and _π_ 0 _._ 5 can move continuously while remaining off-target. Task completion does not imply physically valid contact. The benchmark can serve as a predeployment physical/safety screen for contact-rich care policies. 

## REFERENCES 

- [1] J. Thumm, F. Trost, and M. Althoff, “Human-robot gym: Benchmarking reinforcement learning in human-robot collaboration,” in _Proc. IEEE Int. Conf. Robot. Autom. (ICRA)_ , 2024. 

- [2] Y. Koh and A. H. Qureshi, “Manip4care: Robotic manipulation of human limbs for solving assistive tasks,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)_ , 2025, pp. 11 435–11 442. 

- [3] Y. Gu and Y. Demiris, “VTTB: A visuo-tactile learning approach for robot-assisted bed bathing,” _IEEE Robot. Autom. Lett._ , vol. 9, pp. 5751– 5758, 2024. 

- [4] Open X-Embodiment Collaboration, “Open x-embodiment: Robotic learning datasets and rt-x models,” in _Proc. IEEE Int. Conf. Robot. Autom. (ICRA)_ , 2024. 

- [5] H. Zhang, N. Zantout, P. Kachana, J. Zhang, and W. Wang, “Iref-vla: A benchmark for interactive referential grounding with imperfect language in 3d scenes,” in _Proc. IEEE Int. Conf. Robot. Autom. (ICRA)_ , 2025. 

   - [8] K. Black, N. Brown, D. Driess, A. Esmail _et al._ , “ _π_ 0 _._ 5: a visionlanguage-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

   - [9] M. Macklin, M. M¨uller, and N. Chentanez, “XPBD: Position-based simulation of compliant constrained dynamics,” in _Proc. Int. Conf. Motion in Games (MIG)_ , 2016, pp. 49–54. 

   - [10] A. H. Chen, Z. Liu, Y. Yang, and C. Yuksel, “Vertex block descent,” _ACM Trans. Graph._ , vol. 43, no. 4, pp. 116:1–116:15, 2024. 

   - [11] M. Liu, G. Yang, S. Luo, and L. Shao, “SoftMAC: Differentiable soft body simulation with forecast-based contact model and two-way coupling with articulated rigid bodies and clothes,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)_ , 2024, arXiv:2312.03297. 

   - [12] L. Liu, K. Yin, B. Wang, and B. Guo, “Simulation and control of skeleton-driven soft body characters,” _ACM Trans. Graph._ , vol. 32, no. 6, pp. 215:1–215:8, 2013. 

   - [13] M. Manti, A. Pratesi, E. Falotico, M. Cianchetti, and C. Laschi, “Soft assistive robot for personal care of elderly people,” in _Proc. 6th IEEE Int. Conf. Biomed. Robot. Biomechatronics (BioRob)_ , 2016, pp. 833–838. 

   - [14] ——, “Towards the development of a soft manipulator as an assistive robot for personal care of elderly people,” _International Journal of Advanced Robotic Systems_ , vol. 14, no. 1, pp. 1–11, 2017. 

   - [15] K. Black _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

   - [16] Y. Lai, S. Yuan, P. Li, B. Zhang _et al._ , “FAM-HRI: Foundationmodel assisted multi-modal human-robot interaction combining gaze and speech,” _arXiv preprint arXiv:2503.16492_ , 2025. 

   - [17] NVIDIA, “Newton adds contact-rich manipulation and locomotion capabilities for industrial robotics,” NVIDIA Technical Blog, 2026, [Online]. Available: https://developer.nvidia.com/blog/newton-adds-contact-ric h-manipulation-and-locomotion-capabilities-for-industrial-robotics/. 

   - [18] International Organization for Standardization, “Robots and robotic devices—collaborative robots,” ISO, Tech. Rep. ISO 15066:2016, 2016. 

   - [19] R. Behrens, G. Pliske, M. Umbreit, S. Piatek, F. Walcher, and N. Elkmann, “A statistical model to determine biomechanical limits for physically safe interactions with collaborative robots,” _Frontiers in Robotics and AI_ , vol. 8, p. 667818, 2021. 

   - [20] R. Madan, J. Lin, M. Goel, A. Li _et al._ , “PrioriTouch: Adapting to user contact preferences for whole-arm physical human-robot interaction,” in _Proc. 9th Conf. Robot Learn. (CoRL)_ , ser. Proc. Mach. Learn. Res., vol. 305, 2025, pp. 1515–1530. 

   - [21] C. Carissoli, L. Negri, M. Bassi, F. A. Storm, and A. D. Fave, “Mental workload and human-robot interaction in collaborative tasks: A scoping review,” _Int. J. Hum.-Comput. Interact._ , vol. 40, no. 20, pp. 6458–6477, 2024. 

   - [22] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “LIBERO: Benchmarking knowledge transfer for lifelong robot learning,” in _Adv. Neural Inf. Process. Syst. (NeurIPS)_ , 2023. 

   - [23] G. Pavlakos, V. Choutas, N. Ghorbani, T. Bolkart, A. A. A. Osman, D. Tzionas, and M. J. Black, “Expressive body capture: 3d hands, face, and body from a single image,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , 2019, pp. 10 975–10 985. 

   - [24] T. Ren, S. Liu, A. Zeng _et al._ , “Grounded SAM: Assembling open-world models for diverse visual tasks,” in _arXiv preprint arXiv:2401.14159_ , 2024. 

   - [25] C. Lugaresi, J. Tang, H. Nash _et al._ , “MediaPipe: A framework for building perception pipelines,” in _arXiv preprint arXiv:1906.08172_ , 2019. 

   - [26] S. G. Hart and L. E. Staveland, “Development of NASA-TLX (task load index): Results of empirical and theoretical research,” in _Human Mental Workload_ , P. A. Hancock and N. Meshkati, Eds. Amsterdam, The Netherlands: North-Holland, 1988, pp. 139–183. 

   - [27] A. Zlatintsi, A. C. Dometios, N. Kardaris, I. Rodomagoulakis, P. Koutras _et al._ , “I-SUPPORT: A robotic platform of an assistive bathing robot for the elderly population,” _Robot. Auton. Syst._ , vol. 126, p. 103451, 2020. 

- [6] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “VoxPoser: Composable 3d value maps for robotic manipulation with language models,” in _Proc. 7th Conf. Robot Learn. (CoRL)_ , ser. Proc. Mach. Learn. Res., vol. 229, 2023, pp. 971–986. 

- [7] W. Huang, C. Wang, Y. Li, R. Zhang, and L. Fei-Fei, “ReKep: Spatiotemporal reasoning of relational keypoint constraints for robotic manipulation,” in _Proc. 8th Conf. Robot Learn. (CoRL)_ , ser. Proc. Mach. Learn. Res., vol. 270, 2025, pp. 4573–4602. 

