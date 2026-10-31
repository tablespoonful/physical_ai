---
title: "Technical Report: One-Step Drifting Action Heads for GR00T N1.7"
date: "2026-09-16"
authors: "Xihe Shao"
url: https://arxiv.org/abs/2609.18108
pdf: https://arxiv.org/pdf/2609.18108
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.18108)** / [論文ページ](https://arxiv.org/abs/2609.18108)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Technical Report: One-Step Drifting Action Heads for GR00T N1.7 

Xihe Shao 

ZJU-UIUC Institute, Zhejiang University Hangzhou, China Intern, LimX Dynamics, Shenzhen, China xihe.25@intl.zju.edu.cn 

**_Abstract_ —One-step action generation can substantially reduce the inference cost of vision-language-action (VLA) policies, but its effect on closed-loop task success remains an open question. This technical report studies a GR00T N1.7 variant in which the iterative diffusion-transformer action head is replaced by a onestep drifting action head, together with an overlap-conditioned extension for asynchronous chunk replacement. All multi-seed drifting runs were trained on two NVIDIA A800 GPUs. On LIBERO, the action head reduces the mean model-forward time of the action head from approximately** 45 _._ 3 ms **to** 5 _._ 0 ms **, while the measured backbone-plus-head time falls from approximately** 70 _._ 0 ms **to** 30 _._ 6 ms **. However, this speedup is accompanied by a systematic reduction in task success. Across three drifting seeds, success is** 64 _._ 0 _±_ 4 _._ 0% **on LIBERO-Spatial,** 52 _._ 0 _±_ 1 _._ 0% **on LIBERO-Goal, and** 26 _._ 0 _±_ 2 _._ 6% **on LIBERO-Long. The low seed variance indicates that the degradation is not explained by random initialization alone. We report the result as a speed– success trade-off rather than an overall improvement, and discuss likely contributing factors including deterministic one-step mode averaging, batch-dependent geometry estimation, long openloop chunk execution, and the fact that synchronous LIBERO evaluation does not exercise the asynchronous overlap path.** 

**_Index Terms_ —vision-language-action models, action chunking, one-step generation, drifting models, inference acceleration, robot manipulation** 

## I. INTRODUCTION 

Vision-language-action (VLA) models have demonstrated strong capabilities in robotic manipulation, but their computational cost and inference latency can limit deployment on real-time robot platforms. Existing efficiency methods reduce different parts of the VLA pipeline. Model-level approaches include fast–slow architectures [1], lightweight backbones [2], token caching [3], and adaptive early-exit inference [4]. System-level approaches include quantization [5], graph optimization, and custom operators [6]. Iterative action generation can nevertheless remain an important source of latency because diffusion and flow-matching heads require multiple network evaluations per action chunk. 

This report studies whether the iterative action head of GR00T N1.7 [7] can be replaced by a one-step drifting action head. The base training objective is inherited from Implicit Drifting Policy (IDP) [8]; this report does not claim a new generative objective. The implemented head retains the GR00T vision-language backbone and preprocessing stack, replaces the iterative flow-matching action generator with a 

deterministic conditional transformer, and predicts a complete action chunk in one action-head evaluation. 

A second issue appears in asynchronous action prefetching. If a replacement chunk is generated while the current chunk is still being executed, the new prediction may not account for commands that have already been committed to the controller. To address this issue, we implement an overlap-conditioned variant, called DrifOv, inspired by training-time real-time chunking [9]. DrifOv conditions on a valid action prefix, an overlap length, and an estimated execution offset, and copies the committed prefix exactly while generating only the unknown suffix. 

The report has both positive and negative findings. The positive result is a large and highly stable action-head speedup. The negative result is that this speedup does not currently preserve task success: under the evaluated training protocol, the drifting variants are substantially less successful than the GR00T reference on three LIBERO suites. The three drifting seeds show low variance, so the gap is systematic rather than attributable only to a single unlucky initialization. 

The contributions of this technical report are: 

- We implement and describe a one-step drifting action head for GR00T N1.7, including its inherited training objective, model dimensions, and one-evaluation inference path. 

- We implement an overlap-conditioned extension that represents an already committed action prefix, its coordinatewise validity, the overlap length, and an estimated execution offset while preserving valid prefix coordinates exactly. 

- We provide a multi-seed LIBERO study in which all drifting seed runs use the same two-A800 training setup. We report latency and success separately and do not average suites with missing measurements. 

- We identify several hypotheses for the observed speed– success trade-off and specify the experiments needed to isolate them. The current evidence does not establish that the drifting objective itself causes the entire degradation. 

- We record preliminary real-robot deployment and datacollection experience. These experiments are presented as engineering observations, not as controlled policy comparisons. 

This is a preliminary technical report, not a claim of stateof-the-art performance. The timing measurements include only the VLM backbone and the action head. They exclude preprocessing, postprocessing, networking, action transmission, controller execution, and scheduling. The reported speedups therefore should not be interpreted as equal reductions in endto-end robot latency. 

## II. RELATED WORK 

## _A. Efficient VLA Inference_ 

VLA efficiency has been approached by reducing the size or frequency of VLM computation. TinyVLA [2] uses a compact vision-language backbone for data-efficient control. VLA-Cache [3] reuses vision-language tokens across an action trajectory. Fast-in-Slow [1] separates slow reasoning from fast action generation, and DEER [4] dynamically terminates reasoning when further computation is not needed. Quantization and optimized execution engines [5], [6] reduce the cost of the remaining network evaluations. 

These methods are complementary to the action-head replacement studied here. In the GR00T N1.7 configuration considered in this report, the VLM backbone dominates the measured model-forward time even after the action head is reduced to approximately 5 ms. For this reason, an actionhead-only latency reduction cannot by itself make the complete pipeline real-time. 

## _B. Action Chunking and Real-Time Chunking_ 

Action-chunking policies predict multiple future actions in one policy call and execute a queue of actions before the next request. This reduces VLM calls but creates a trade-off between open-loop execution length and feedback frequency. Real-time chunking (RTC) [9] begins the next request before the current chunk is exhausted and constrains a new chunk to remain consistent with the unexecuted actions that will execute while inference is in flight. 

DrifOv follows the same asynchronous timeline but does not use iterative inference-time guidance. Instead, it learns prefixconditioned one-step generation. Committed coordinates are copied exactly after decoding, while the suffix is generated jointly in a single action-transformer evaluation. 

## _C. Drifting Models and One-Step Generation_ 

The base action head uses the training objective of Implicit Drifting Policy (IDP) [8]. For each observation-action pair, IDP constructs a geometry-weighted potential around the expert action instead of regressing an explicit continuous drifting field. At deployment, a zero action seed is mapped directly to a complete action chunk. 

The extension in this report is not the drifting objective itself. The implementation adds an action-prefix interface and overlap-aware suffix generation so that a successor chunk can be conditioned on commands already committed to the controller. The report evaluates the implementation as an engineering replacement for the GR00T flow-matching action head. 

## III. METHOD 

## _A. Scope and Architecture_ 

The implementation retains the GR00T N1.7 preprocessing and Cosmos-Reason2/Qwen3 vision-language backbone. Hidden features are read from layer 16 and projected to the action-head dimension. Robot state is encoded by an embodiment-specific MLP, and actions are encoded by an embodiment-specific action encoder. The action head is a 12block transformer with model dimension 1024, 16 attention heads, feed-forward dimension 4096, and dropout 0 _._ 1. Each block contains self-attention over action and state tokens, cross-attention to vision-language memory, and a feed-forward network. The cross-attention alternates between image and text tokens across blocks. 

The default action chunk length is _H_ = 40. The maximum state and action dimensions are both 132, and the state history length is one. At deployment, the head receives a zero action seed and produces the complete chunk in one actiontransformer evaluation. The number of inference steps is fixed to one. 

## _B. Inherited Drifting Objective_ 

The base action head uses the IDP objective [8]. For an observation-action pair ( _oi, a_<sup>_∗_</sup> _i_<sup>),let</sup><sup>_Mi⪰_0beadetached</sup> diagonal geometry matrix. The potential is 


The corresponding correction is 


Training evaluates the network at two locations. The proposal prediction starts from a zero action seed at time zero: 


The proximal prediction starts near the expert action: 


with _t∗_ = 0 _._ 9 in the reported configuration. The inherited objective is 


where _λ_ prox = 81 _._ 0 in the reported implementation. 

## _C. Geometry Weighting_ 

For a minibatch of observation-action pairs, normalized observation features are compared by inner product. The similarities are row-standardized and converted to neighbor weights _wij_ with a softmax. For action coordinate _d_ , the conditional variance is estimated as 


The reference variance _vd_<sup>ref</sup> is computed from the same minibatch. Normalized inverse variances are compared to form the diagonal geometry excess 


where _s_<sup>cond</sup> and _s_<sup>ref</sup> are normalized precision scales. The geometry matrix is detached and used only to weight the training potential. 

Two implementation details are relevant to the interpretation of the experiments. First, the reference variance is estimated within the current minibatch, so its quality depends on batch size and batch composition. Second, the current implementation includes the query sample in the neighbor set, although the IDP equation excludes _j_ = _i_ . This report treats these choices as limitations rather than validated design decisions. 

## _D. Overlap-Conditioned Suffix Generation_ 

DrifOv extends the one-step head with an explicit action prefix. Let 


where _h_ indexes action-chunk positions, _j_ indexes action coordinates, _L_ is the number of committed prefix rows, and _νh,j_ is the valid-action mask. The prefix rows _p_ 0: _L−_ 1 are supplied to the head together with a prefix-validity mask, the overlap length _L_ , and an execution offset. 

The action query for output position _h_ is formed from: 


- 3) an overlap-length embedding, 4) an execution-offset embedding, and 

- 5) a positional embedding. 

The decoder jointly processes all _H_ action queries and crossattends to the vision-language and state-conditioning tokens. For each valid prefix coordinate, the decoded value is replaced by the supplied prefix value: 


Thus, committed actions cannot be rewritten by the learned head. The prefix still influences the suffix through selfattention. The model is trained to generate only the unknown suffix. 

## _E. Overlap-Aware Training_ 

For each training action chunk, an overlap length is sampled from zero through _H −_ 1. The reported configuration also samples a zero-overlap example with probability 0 _._ 2. A nonempty prefix is copied from the expert action chunk. The implementation then perturbs the prefix with probability 0 _._ 5 using Gaussian noise with standard deviation 0 _._ 02 and clips the perturbation to [ _−_ 0 _._ 05 _,_ 0 _._ 05]. The execution offset is sampled between zero and the selected overlap length. Prefix conditioning can be disabled for an unconditioned baseline. 

The generation loss is the inherited potential evaluated only on suffix coordinates. Let 


select the coordinates for which the model is responsible. The suffix loss is 


The same objective is applied to the proximal prediction, with prefix coordinates replaced by the supplied prefix before loss evaluation. 

The implementation optionally adds boundary terms at the first generated suffix action. In the reported configuration, the weights are 1 _._ 0 for the boundary action error and 0 _._ 1 for the finite-difference velocity error. The acceleration weight is zero. These terms are intended to encourage continuity between the fixed prefix and the generated suffix. They do not turn the problem into a new generative model; they are auxiliary regularizers. 

## _F. One-Step Inference_ 

For synchronous LIBERO evaluation, no action prefix is supplied. The inference path therefore uses an empty prefix, mask, and overlap length. The action seed is zero, the time input is zero, and the model produces one complete action chunk in one action-head evaluation: 


This is the path measured in the LIBERO experiments in Section IV-B. It tests the unconditioned one-step head and does not test asynchronous overlap conditioning. 

For asynchronous deployment, the runtime can supply the remaining normalized action rows, their true length before padding, and an estimated inference delay. The committed rows are returned unchanged and only the unknown suffix is generated. A request is rejected if the estimated delay exceeds the available prefix rather than executing a suffix conditioned on an expired prefix. 

## _G. Relationship to the Proposed History-Latent Formulation_ 

An earlier design note proposed a causal history-memory branch and a delay-propagator that would update the latent state using actions executed while inference is in flight. That formulation is not implemented or evaluated in this report. The implemented method conditions only on the committed action prefix and global overlap metadata. The distinction is important: the experiments below do not establish the benefit of a history-latent model. 


## _A. Experimental Protocol_ 

The LIBERO experiments use the LIBERO benchmark [10], the lerobot/libero dataset, and the LeRobot training and evaluation stack. All multi-seed drifting checkpoints are 

TABLE I 

CONFIGURATION OF THE REPORTED EXPERIMENTS. 

|Item|Configuration|
|---|---|
|Training hardware|2_×_ NVIDIA A800|
|Deployment hardware|RTX 4090 + Intel 14900KF|
|Dataset|lerobot/libero|
|Training steps|20k|
|Batch size|32 per GPU, effective 64|
|Precision|bfloat16|
|Action chunk|_H_ = 40|
|LIBERO episodes|10 per subtask, 100 per suite|
|Drifting seeds|1, 42, 1000|


trained on two NVIDIA A800 GPUs. The documented seed1000 run uses batch size 32 per GPU, 20k optimization steps, and bfloat16 precision. The same named recipe is used for the archived seed-1, seed-42, and seed-1000 drifting runs. The primary comparison against GR00T uses the seed-1 and seed-42 runs from the archived seed-comparison directory. The seed-1000 GR00T checkpoint comes from an older archived evaluation and is reported only as a reference point. 

The success summaries use 10 episodes per LIBERO subtask, corresponding to 100 rollouts per suite. Latency is recorded by timing hooks around the backbone and the action head. Each hook performs a CUDA synchronization before and after the timed region. The reported values are means over all inference calls within a suite. They exclude preprocessing, postprocessing, networking, action transmission, and low-level control, and are therefore not end-to-end deployment latencies. 

## _B. LIBERO Latency and Success_ 

Table II reports the measured latency. The action head is approximately 9 _×_ faster across all suites, while the full measured model-forward path is approximately 2 _._ 2–2 _._ 4 _×_ faster. The VLM backbone remains nearly unchanged, confirming that action-head replacement addresses only one component of the inference pipeline. 

Table III reports success. The new drifting seed runs show a large and systematic gap relative to the GR00T reference. The low standard deviation across the three drifting seeds is important: the gap is not explained by one failed initialization. 

The three drifting seeds produce similar success within each suite: Spatial 60 _/_ 64 _/_ 68%, Goal 52 _/_ 51 _/_ 53%, and Long 28 _/_ 27 _/_ 23%. In contrast to the near-constant latency, the loss of task success grows with task horizon. The largest degradation appears on LIBERO-Long, where the policy must sustain progress over a longer sequence of action chunks. 

## _C. Legacy LIBERO Profile_ 

An earlier single-run study used a different checkpoint and training regime. Those measurements are not part of the primary comparison. Figure 2 reproduces the legacy profile only to document the development history. Its success values should not be compared directly to the multi-seed results. 

## _D. Training Memory Observation_ 

Figure 3 shows GPU-memory telemetry recorded while running the GR00T and drifting training jobs on the same server. Selected peaks are 45 _._ 748 GiB for the GR00T run and 17 _._ 752 GiB for the drifting run. This observation is anecdotal rather than a controlled memory benchmark. We therefore do not attribute the difference solely to the action head, but record it as a potential practical benefit for resource-limited training. 

## _E. Preliminary Real-Robot Deployment_ 

The policy stack was deployed on a LimX Tron2 robot with an RTX 4090 and Intel 14900KF workstation. We collected and annotated data for three manipulation settings. These experiments demonstrate system integration and data collection, but they are not controlled success-rate comparisons. 

_a) Task 1: toy placement.:_ The first setting places toys and writing tools into specified bins. The annotation interface used for the task variants is shown in Fig. 4. Success and failure labels are recorded for data curation, but the collected labels were not collected under a fixed policy evaluation protocol. 

_b) Task 2: industrial accessory packaging.:_ The second setting places packaged industrial accessories into a target tray. A total of 2,562 annotated rollout trajectories were collected. A representative interface is shown in Fig. 5. The dataset is substantially larger than the exploratory LIBERO seed runs, but no matched policy comparison was completed on this task. 

_c) Task 3: cloth folding.:_ The third setting contains cloth-folding data, including successful demonstrations, failed attempts, and human takeover segments. The annotation overview is shown in Fig. 6. These data were collected to study deformable-object manipulation, but the reported technical snapshot does not contain a controlled policy-success comparison. 

## _F. Results Excluded from the Primary Comparison_ 

The pi0.5 evaluation reported 0 _._ 0% success on every LIBERO suite in the archived timing directory. Because an allzero result across suites is more consistent with an evaluation or action-mapping failure than a policy result, it is excluded from the primary comparison. The timing CSV and summary JSON also disagree for several pi0.5 tasks. 

The legacy drif_ov_libero0809 checkpoint is excluded from the controlled comparison for two reasons. First, it was trained with four A800 GPUs, batch size 256 per GPU, and 15k steps, whereas the multi-seed checkpoints use the two-A800 20k-step recipe. Second, its reported success comes from a single exploratory run. The legacy results are retained in the appendix as a development record, not as evidence of method quality. 

## V. DISCUSSION 

## _A. What the Current Results Establish_ 

The results establish a large and repeatable model-forward speedup. The action head is approximately nine times faster, and the backbone-plus-head path is approximately 2 _._ 2–2 _._ 4 

TABLE II 

MEASURED MODEL-FORWARD LATENCY ON LIBERO. VALUES ARE MEANS OVER THE RECORDED SEEDS AND INFERENCE CALLS. “TOTAL” IS BACKBONE PLUS ACTION HEAD. THE MEASUREMENTS EXCLUDE PREPROCESSING, POSTPROCESSING, AND CONTROL OVERHEAD. 

|Task|Model|Seeds|Backbone (ms)|Action head (ms)|Total (ms)|Head speedup|
|---|---|---|---|---|---|---|
|Spatial|GR00T N1.7|3|24_._99_±_0_._28|45_._36_±_0_._17|70_._35_±_0_._19|1_._0_×_|
|Spatial|DrifOv|3|24_._42_±_0_._11|4_._96_±_0_._08|29_._38_±_0_._05|9_._1_×_|
|Goal|GR00T N1.7|3|25_._03_±_0_._45|45_._43_±_0_._19|70_._46_±_0_._50|1_._0_×_|
|Goal|DrifOv|3|26_._47_±_3_._69|5_._07_±_0_._30|31_._54_±_3_._97|9_._0_×_|
|Long|GR00T N1.7|2|24_._14_±_0_._43|45_._18_±_0_._07|69_._33_±_0_._36|1_._0_×_|
|Long|DrifOv|3|25_._92_±_3_._46|5_._04_±_0_._27|30_._95_±_3_._72|9_._0_×_|
|Object|GR00T N1.7|3|26_._21_±_1_._42|45_._80_±_0_._12|72_._01_±_1_._51|1_._0_×_|
|Object|DrifOv|3|24_._30_±_0_._14|4_._94_±_0_._04|29_._25_±_0_._16|9_._3_×_|


TABLE III 

LIBERO SUCCESS RATE. THE MULTI-SEED DRIFTING RESULTS USE SEEDS 1, 42, AND 1000. GR00T USES SEEDS 1 AND 42 FOR THE MATCHED SEED-COMPARISON RUNS; THE GR00T SPATIAL, GOAL, AND LONG VALUES ALSO INCLUDE AN OLDER SEED-1000 REFERENCE CHECKPOINT. OBJECT SUCCESS IS UNAVAILABLE FOR THE DRIFTING SEED RUNS AND IS NOT AVERAGED. 

|Task|Model|Seeds|Success (%)|Per-seed success (%)|Coverage|
|---|---|---|---|---|---|
|Spatial|GR00T N1.7|3|82_._3_±_6_._8|77, 90, 80|3/3|
|Spatial|DrifOv|3|64_._0_±_4_._0|60, 64, 68|3/3|
|Goal|GR00T N1.7|3|82_._3_±_4_._0|80, 87, 80|3/3|
|Goal|DrifOv|3|52_._0_±_1_._0|52, 51, 53|3/3|
|Long|GR00T N1.7|2|74_._5_±_10_._6|67, 82|2/2|
|Long|DrifOv|3|26_._0_±_2_._6|28, 27, 23|3/3|
|Object|GR00T N1.7|1|88.0|88|1/3|
|Object|DrifOv|0|N/A|N/A|0/3|


times faster. The speedup is stable across seeds and suites. The VLM backbone remains the dominant component after the replacement, so the measured improvement does not make the complete vision-language-action pipeline real-time by itself. 

The results also establish a negative outcome. Under the evaluated two-A800 training recipe, the drifting seeds are consistently less successful than the GR00T reference on Spatial, Goal, and Long. The failure is largest on LIBEROLong. Because the seed variance is small, random initialization is not a sufficient explanation. 

The experiments do not isolate which change causes the degradation. The following hypotheses are therefore stated as alternatives rather than conclusions. 

## _B. Deterministic One-Step Mode Averaging_ 

The inherited objective applies an isotropic error plus a coordinate-wise geometry penalty. This is still a regression target toward a demonstration action. In a one-step deterministic generator, observations with multiple valid modes can produce a prediction near the conditional mean of those modes. Near the mean, no demonstrated trajectory may exist. A multi-step diffusion or flow generator can move between modes over its trajectory, while the one-step model must commit to one location immediately. 

The action-chunk space is high-dimensional and may contain several valid continuations even when each individual action is roughly unimodal. This mechanism is consistent with the increase in failure as the task horizon grows, but the current experiments do not measure mode coverage directly. Useful 

diagnostics would compare one-step prediction error as a function of the number of expert modes near each observation and evaluate whether a latent or discrete mode variable reduces the error. 

## _C. Batch-Dependent Geometry Estimation_ 

The geometry matrix is estimated from the current minibatch. The reported two-A800 runs use 32 samples per local batch. Neighbor weights, conditional variances, and reference variances therefore vary with batch composition. Changing batch size changes the effective geometry objective even when the optimization objective and data are otherwise matched. 

The current implementation also includes the query sample in the neighbor set, while the IDP equation excludes the selfneighbor term. Inclusion of the diagonal similarity can make the softmax neighborhood more concentrated and can alter the variance estimate. This report does not claim that either choice is correct; both require ablation. A retrieval-based or datasetlevel geometry estimate would remove the direct dependence on minibatch size. 

## _D. Open-Loop Chunk Execution_ 

The policy predicts _H_ = 40 actions, and the default evaluation executes the chunk before requesting the next one. A faster action head does not automatically reduce this openloop interval. Long-horizon error can therefore accumulate even though the head itself is fast. 

A direct engineering experiment is to vary the number of actions executed before replanning. Candidate settings are 1, 


Fig. 1. Summary of the speed–success trade-off. Panel (a) averages the measured model-forward time over Spatial, Goal, and Long. Panel (b) reports success for the three suites with complete or partially matched summaries. Error bars in panel (b) are standard deviations across the available training seeds. 


Fig. 2. Legacy LIBERO-Long profile from an earlier checkpoint. The legacy run is shown as an engineering record only; it is not the primary two-A800 seed comparison and is not used to estimate the method’s success. 

2, 5, 10, 20, and 40 actions. If task success improves as the execution horizon decreases, the reported latency advantage can be translated into higher feedback frequency rather than being spent on a fixed long chunk. This experiment is not included in the current snapshot. 

## _E. Untested Asynchronous Overlap Path_ 

The DrifOv training and inference code supports a committed prefix, but the synchronous LIBERO evaluation supplies an empty prefix. The measured LIBERO success therefore evaluates the unconditioned one-step path. It does not measure whether prefix conditioning improves chunk handoff, queue continuity, or asynchronous control. 

The training prefix is sampled from the expert chunk and optionally perturbed with bounded Gaussian noise. During asynchronous deployment, however, the prefix would be produced by the policy itself. The training distribution and the deployment distribution are not identical. Model-generated 

prefixes with physically consistent arrival states would be required to evaluate this mechanism properly. 

## _F. Training and Architecture Confounds_ 

Both GR00T and DrifOv retain the same backbone and preprocessing stack, but the action-head architecture, action-head initialization, and training objective differ. The current study does not include a direct MSE head, an ablation of the geometry term, or a comparison against a one-step consistencydistilled GR00T head. The low LIBERO scores may therefore reflect optimization difficulty, an architecture mismatch, an action-normalization issue, or the one-step objective rather than a single isolated factor. 

The report also does not use a pretrained GR00T action head as the initialization for the new head. The reported comparison is consequently a from-scratch action-head comparison rather than a fine-tuning comparison. 

## _G. Implications for Deployment_ 

The observed memory telemetry and the large action-head speedup suggest that one-step heads are worth continuing to investigate for resource-constrained systems. The current LIBERO evidence, however, does not support a claim that the action head can replace the iterative head without performance loss. 

A realistic next system design is a slow VLM backbone combined with a faster action head. The backbone could be refreshed at a lower rate while the action head is recomputed from cached visual features and the latest robot state. That design requires delay augmentation and arrival-state consistency training; it is not evaluated here. 

## _H. Threats to Validity_ 

The following factors limit the conclusions of this report: 

- The GR00T reference checkpoint for seed 1000 comes from an older archived evaluation and may not use the exact same protocol as the seed-comparison runs. 


Fig. 3. GPU-memory telemetry recorded during the drifting and GR00T training runs on the same server. The drifting run shows a lower selected peak than the GR00T run. These measurements are anecdotal rather than a controlled benchmark, because the telemetry also includes other jobs and idle periods. 


Fig. 4. Real-robot toy-placement and bin-sorting task variants used during data collection. 


Fig. 5. Annotation progress for the industrial accessory-packaging task. A total of 2,562 rollout trajectories were collected. 

- Object-suite success is missing for the drifting seeds. The object timing row is not accompanied by a controlled success comparison. 

- The pi0.5 results are excluded because the archived evaluation produced zero success on every suite and inconsistent summary files. 


Fig. 6. Cloth-folding datasets collected during real-robot deployment, including successful, failed, and human-takeover demonstrations. 

- Timing includes only the backbone and action head. It excludes preprocessing, networking, controller execution, and scheduling. 

- The real-robot section records data collection and system integration, but does not provide a controlled success-rate comparison. 

- The memory observation comes from shared server telemetry and is affected by other jobs. 

## VI. CONCLUSION 

This technical report studied a one-step drifting replacement for the iterative action head of GR00T N1.7. The implementation reduces the measured action-head time from approximately 45 _._ 3 ms to 5 _._ 0 ms and the measured backboneplus-head time from approximately 70 _._ 0 ms to 30 _._ 6 ms. It also includes an overlap-conditioned interface that can preserve a committed action prefix and generate only a successor suffix. 

The current LIBERO results do not support a claim that the speedup is obtained without a loss of task performance. Under a two-A800 training setup, three drifting seeds show 64 _._ 0 _±_ 4 _._ 0% success on Spatial, 52 _._ 0 _±_ 1 _._ 0% on Goal, and 26 _._ 0 _±_ 2 _._ 6% on Long. The seed stability indicates that the degradation is systematic, while the cause remains unresolved. 

The most useful next steps are controlled rather than promotional. They include matching the training and evaluation protocol for all baselines, removing the minibatch dependence of the geometry estimate, testing whether the query sample should be excluded from the neighborhood, reducing the number of actions executed per chunk, and evaluating the overlap path in an asynchronous rollout. A one-step policy should be judged not only by its action-head latency but by its speed–success frontier and by whether the latency reduction enables more frequent closed-loop feedback. 

## APPENDIX A 

## CHECKPOINT AND EVALUATION INVENTORY 

The primary multi-seed drifting checkpoints are: 

- Xihe666/drif_ov_libero_20k_seed1_0821 

- Xihe666/drif_ov_libero_20k_seed42_0821 

- Xihe666/drif_ov_libero_20k_seed1000_ 0822 

These runs were trained on two NVIDIA A800 GPUs. The documented seed-1000 configuration uses 20k steps, batch size 32 per GPU, and bfloat16 precision. The seed-1 and seed-42 runs are evaluated as part of the same multi-seed study. 

The matched GR00T seed-comparison checkpoints are: 

- Xihe666/gr00t_n17_libero_20k_seed1 

- Xihe666/gr00t_n17_libero_20k_seed42 

- The legacy single-run checkpoint is: 

   - [2] J. Wen, Y. Zhu, J. Li, M. Zhu, Z. Tang, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen _et al._ , “Tinyvla: toward fast, data-efficient vision-languageaction models for robotic manipulation,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 4, pp. 3988–3995, 2025. 

   - [3] S. Xu, Y. Wang, C. Xia, D. Zhu, T. Huang, and C. Xu, “Vlacache: Efficient vision-language-action manipulation via adaptive token caching,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 164 448–164 473, 2026. 

   - [4] Y. Yue, Y. Wang, B. Kang, Y. Han, S. Wang, S. Song, J. Feng, and G. Huang, “Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 56 619–56 643, 2024. 

   - [5] S. Park, H. Kim, W. Jeon, J. Yang, B. Jeon, Y. Oh, and J. Choi, “Quantization-aware imitation-learning for resource-efficient robotic control,” _arXiv preprint arXiv:2412.01034_ , 2024. 

   - [6] Y. Li, W. Mao, Z. Lan, J. Rong, M. Zhu, Y. Mao, B. Shen, and X. Huang, “FluxVLA Engine: A One-Stop VLA Engineering Platform for Embodied Intelligence,” Apr. 2026. [Online]. Available: https://github.com/FluxVLA/FluxVLA 

   - [7] NVIDIA, J. Bjorck, N. C. Fernando Casta˜neda, X. Da, R. Ding, L. J. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, J. Jang, Z. Jiang, J. Kautz, K. Kundalia, L. Lao, Z. Li, Z. Lin, K. Lin, G. Liu, E. Llontop, L. Magne, A. Mandlekar, A. Narayan, S. Nasiriany, S. Reed, Y. L. Tan, G. Wang, Z. Wang, J. Wang, Q. Wang, J. Xiang, Y. Xie, Y. Xu, Z. Xu, S. Ye, Z. Yu, A. Zhang, H. Zhang, Y. Zhao, R. Zheng, and Y. Zhu, “GR00T N1: An open foundation model for generalist humanoid robots,” in _ArXiv Preprint_ , March 2025. 

   - [8] Yang et al., “Implicit drifting policy,” _arXiv preprint arXiv:2606.01098_ , 2026. 

   - [9] K. Black, A. Z. Ren, M. Equi, and S. Levine, “Training-time action conditioning for efficient real-time chunking,” _arXiv preprint arXiv:2512.05964_ , 2025. 

   - [10] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “LIBERO: Benchmarking knowledge transfer for lifelong robot learning,” in _Advances in Neural Information Processing Systems_ , vol. 36, 2023, pp. 67 071–67 094. 

- Xihe666/drif_ov_libero0809 

It was trained with four A800 GPUs, batch size 256 per GPU, and 15k steps. It is retained only to document the development history and is excluded from the primary comparison. 

The raw latency CSV files and summary JSON files are stored under Experiment-result/latency_bench and Experiment-result/LIBERO_latency_stats. The aggregate summary used to construct the tables in this report is stored under Experiment-result/LIBERO_summary. 

## APPENDIX B 

## EXCLUDED MEASUREMENTS 

The archived pi0.5 evaluation reports 0 _._ 0% success for Spatial, Object, Goal, and Long. The timing CSV and summary JSON also disagree for several tasks. Because a uniform zero success rate is more likely to reflect an evaluation or actionmapping failure than a meaningful policy result, the pi0.5 table is excluded from the primary comparison. 

The archived object summary has no drifting success value. We therefore report the object latency measurement but leave object success as N/A. No missing success value is replaced by a legacy run or by the mean of other suites. 

## REFERENCES 

> [1] H. Chen, J. Liu, C. Gu, Z. Liu, R. Zhang, X. Li, X. He, Y. Guo, C.-W. Fu, S. Zhang _et al._ , “Fast-in-slow: a dual-system vla model unifying fast manipulation within slow reasoning,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 98 049–98 083, 2026. 

