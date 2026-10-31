---
title: "When Faster VLA Deployment Changes Closed-Loop Behavior: Task Success-Latency Analysis of SmolVLA Across PyTorch and ONNX Variants"
date: "2026-09-12"
authors: "Rafiqul Islam"
url: https://arxiv.org/abs/2609.14146
pdf: https://arxiv.org/pdf/2609.14146
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.14146)** / [論文ページ](https://arxiv.org/abs/2609.14146)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# When Faster VLA Deployment Changes Closed-Loop Behavior: Task Success–Latency Analysis of SmolVLA Across PyTorch and ONNX Variants 

Rafiqul Islam Independent Researcher Email: rafiqul713@gmail.com 

**_Abstract_ —Vision-language-action (VLA) deployment can reduce inference latency while changing closed-loop task behavior. We evaluate HuggingFaceVLA/smolvla_libero on an RTX 2060 (6 GB) in LIBERO Spatial and Object (MuJoCo 3.3.2, LeRobot 0.6.1, seed 42), comparing PyTorch+AMP with ONNX Runtime CUDA Execution Provider (CUDA EP). The main evaluation uses 100 episodes/suite; a paired rollout uses 300 episodes/suite. PyTorch+AMP reaches 70.0%/88.0% Spatial/Object success at 1181 ms p99. ONNX export invocations requested as FP16 and INT8 yield tether-inspect p99 values of 601 ms and 532 ms, while Spatial success falls to 41.0% and 40.0% and Object remains at 89.0%; graph audit shows both artifacts are byte-identical FP32 graphs, so the requested-INT8 result is not operator-level INT8 quantization. A static languagewidth ablation (16/24/32 tokens) yields Spatial success of 41.0%, 75.0%, and 71.0%; widths 24 and 32 recover much of the Spatial drop while Object success and uniform-bench latency stay approximately stable. Width-24 ONNX Spatial success was 75.0%, close to the PyTorch+AMP baseline of 70.0%; their Wilson 95% confidence intervals overlap. Context width is an important contributor in this stack; it does not account for every PyTorchvs-ONNX difference. Deployment evaluation should jointly report latency, artifact inspection, interface constraints, and closed-loop success. Code: https://github.com/rafiqul713/smolvla-libero-onnx.** 

**_Index Terms_ —Deep Learning in Grasping and Manipulation, Software, Middleware and Programming Environments, Performance Evaluation and Benchmarking, AI-Based Methods, Machine Learning for Robot Control** 

### I. INTRODUCTION 

SmolVLA [1] reports strong LIBERO scores under floatingpoint PyTorch evaluation. A typical deployment path then changes several variables together: ONNX export, runtime, requested precision, kernels, and static input shapes. The question in this letter is not only whether inference becomes faster, but whether _closed-loop task success_ is preserved. 

Three quantities that are often treated as interchangeable are distinct: (i) open-loop numerical agreement on shared inputs; (ii) latency and memory on a given GPU; (iii) closed-loop success, where each action changes the next state and small output differences can accumulate. High values of (i) or (ii) do not imply (iii). 

OpenVLA [2] and _π_ 0 [3] established open VLA policies; NanoVLA [4] and LiteVLA-Edge [5] target smaller or on-device policies. QuantVLA [6] and EaqVLA [7] study post-training quantization, typically on datacenter GPUs. vla.cpp [8] reports SmolVLA latency on Jetson via GGUF without coupling those timings to LIBERO success under ONNX-style exports. This letter does not propose a new policy or quantizer. We study a narrower setting: HuggingFaceVLA/smolvla_libero on one RTX 2060 (6 GB), with a pinned LIBERO Spatial/Object protocol (MuJoCo 3.3.2, LeRobot 0.6.1, seed 42). Exports use tether [9]; ONNX latency uses CUDA Execution Provider (CUDA EP). TensorRT engine compilation was attempted but did not complete within 6 GB; we do not report TensorRT latency. 

The main observation is a deployment gap: the ONNX/CUDA EP configuration is substantially faster than PyTorch+AMP on this GPU (about 2 _×_ lower p99 on the respective benches) but shows substantially lower Spatial closed-loop success, while Object success remains comparable. The export tool’s default 16-token language width is a testable interface hypothesis for part of this asymmetry. We evaluate it with a 16/24/32-token re-export, holding checkpoint, tether version, runtime, hardware, and evaluation protocol fixed. 

_a) Contributions:_ 

- 1) Empirical evidence that a faster ONNX+CUDA-EP deployment configuration of SmolVLA need not preserve closed-loop LIBERO Spatial success, while Object success remains comparable (100-episode/suite main evaluation, seed 42). 

- 2) A controlled 16/24/32-token language-width ablation, with checkpoint, tether version, CUDA EP, hardware, and protocol held fixed, providing evidence that static language-context width is an important contributor to the Spatial gap in the tested stack. 

- 3) A graph-level audit showing that a requested precision flag need not imply actual conversion: the requestedINT8 artifact matches the requested-FP16 FP32 graph and contains no quantization operators. 

- 4) Evidence that open-loop numerical agreement does not 

TABLE I 

PINNED PROTOCOL. MAIN EVALUATION AND PAIRED ROLLOUTS DIFFER IN EPISODE COUNT AND HARNESS. 

|Setting|Value|
|---|---|
|Checkpoint|HuggingFaceVLA/smolvla_libero|
|MuJoCo / GL|3.3.2 / egl|
|Action / flow steps|1 / 10|
|Tasks per suite / batch / seed|10 / 1 / 42|
|Main evaluation|10 eps/task (100 eps/suite)|
|Paired rollout evaluation|30 eps/task (300 eps/suite)|
|PyTorch AMP|on|
|GPU / ONNX runtime|RTX 2060 6 GB / CUDA EP|
|Requested ONNX precision|fp16, int8 (Sec. III-C)|
|Language widths|16 / 24 / 32 tokens|


guarantee closed-loop task-success agreement, including a 300-episode/suite paired PyTorch–ONNX rollout (Spatial 56.7% vs. 33.0%; Object 73.3% vs. 74.0%) and an early adapter with _∼_ 0.98 per-step cosine similarity but 0% closed-loop success. 

Our PyTorch+AMP baseline (70% Spatial, 88% Object) is below the SmolVLA paper (96%/92%) [1]. This letter does not attempt to reproduce those headline rates; relative comparisons use one local stack. Code and measured results: https://github. com/rafiqul713/smolvla-libero-onnx. 

### II. EXPERIMENTAL SETUP 

### _A. Hardware, software, and protocol_ 

All runs used a Linux workstation with an NVIDIA RTX 2060 (6 GB, Turing sm <u>75),</u> driver 535.309.01, Python 3.12, LeRobot 0.6.1, PyTorch 2.5.1+cu121, MuJoCo 3.3.2 (MUJOCO_GL=egl), tether 0.12.0, and ONNX Runtime GPU 1.22.0. No Jetson device and no physical robot were used. 

SmolVLA [1] combines a SigLIP vision tower, a SmolLM2 backbone, and a ten-step flow-matching action expert (7-DoF actions). LIBERO [10] has four suites of ten tasks; we evaluate Spatial and Object [1], [11]. Scores are sensitive to MuJoCo version and action-step settings [12]. Table I lists the pinned protocol. PyTorch evaluation uses load_vlm_weights=false (weights from the LIBERO checkpoint; load-time only) and use_amp=true (torch.autocast defaults to float16 on CUDA in PyTorch 2.5). We therefore call this the _PyTorch+AMP baseline_ , not pure FP32 inference. 

### _B. Deployment variants and measurements_ 

Variants: (i) PyTorch+AMP; (ii) ONNX from tether export --precision fp16; (iii) ONNX from --precision int8; (iv) the same checkpoint reexported at language widths 24 and 32. Default tether traces language inputs at width 16. Requested precision is a flag; actual dtypes are established by graph audit (Section III-C), not by the flag. 

Latency uses 50 warmup + 1000 timed calls, batch 1, and ten flow steps, with CUDA synchronization around each call. Two ONNX benches exist and are not interchangeable: tether inspect bench (Table II) and a uniform ONNX 

Runtime script used for all three widths (Table V, Fig. 2). PyTorch latency uses a separate AMP bench. Reported latency values characterize those respective configurations and provide an empirical deployment comparison, not a fully controlled cross-runtime microbenchmark. Peak GPU memory is processlevel nvidia-smi during inference (indicative process-level footprint, not allocator peak). Open-loop agreement: cosine similarity and maximum absolute difference of action chunks (first 7 dimensions) on a stated input set. Closed-loop success: LIBERO episode success (%). We treat these as distinct metrics. 

Main closed-loop runs use lerobot-eval / scripts/libero_onnx_eval.py (100 episodes/suite). Paired PyTorch–ONNX runs use scripts/run_smolvla_verify.py on the same tether control loop (300 episodes/suite) to compare behavior under matched seeds and resets; they do not isolate a single deployment factor. An early adapter re-tokenized instructions with the export tokenizer and scored 0% at _∼_ 0.98 per-step cosine vs. PyTorch. The corrected adapter passes LeRobot lang_tokens and camera masks, padded or truncated to the graph width. 

TensorRT EP compilation was attempted after stripping unsupported ScatterND attributes and did not finish within 6 GB. All reported ONNX latency uses CUDA EP. 

### _C. Context-length ablation_ 

LeRobot appends a newline and tokenizes with the SmolVLM2 tokenizer (max_length=48). Some Spatial instructions then exceed 16 tokens at the ONNX boundary. Widths 24 and 32 cover the longest Spatial instruction in this suite (20 tokens including newline). Each width is a separate tether 0.12.0 export (same patches, opset 19, ten denoise steps). Fixed: hardware, CUDA EP, seed 42, 100-episode main protocol, and LeRobot tokens. 

Per width we measure: truncation frequency (tasks whose _fed_ token count exceeds the static width), Spatial/Object success, and uniform-bench p50/p99 and peak memory. A supporting outcome is Spatial recovery at width _≥_ 24 with Object and latency approximately stable. A weakening outcome is no Spatial recovery, in which case Table VI lists the remaining candidates. Either outcome is informative. 

### III. RESULTS 

### _A. Task success and latency under the main evaluation_ 

Table II reports the 100-episode/suite main evaluation (seed 42). PyTorch+AMP: 70.0% Spatial, 88.0% Object, p99 1181 ms, p50 903 ms, mean 917 ms, peak process memory 2208 MB (nvidia-smi). Object is within a few points of the SmolVLA paper (92%); Spatial is substantially lower (96% in [1]). We do not attribute that discrepancy to a single factor. 

Requested-FP16 and requested-INT8 ONNX (width 16) yield tether inspect bench p99 601 ms and 532 ms, Spatial 41.0% and 40.0%, and Object 89.0% in both runs. 

TABLE II MAIN 100-EPISODE/SUITE EVALUATION (SEED 42, WIDTH 16). SUCCESS IS LIBERO EPISODE SUCCESS (%); BRACKETS ARE WILSON 95% CIS ( _n_ =100). ONNX P99: T E T H E R I N S P E C T B E N C H (MS). VRAM: PROCESS-LEVEL N V I D I A-S M I (MB), NOT ALLOCATOR PEAK. 

|Runtime|Requested<br>Spatial|Object<br>p99|VRAM|
|---|---|---|---|
|PyTorch+AMP|AMP<br>70.0 [60.4, 78.1]|88.0 [80.2, 93.0]<br>1181|2208|
|ONNX CUDA EP|fp16<br>41.0 [31.9, 50.8]|89.0 [81.4, 93.7]<br>601|3200|
|ONNX CUDA EP|int8<br>40.0 [30.9, 49.8]|89.0 [81.4, 93.7]<br>532|—|
|SmolVLA paper [1]|FP32<br>96.0|92.0<br>—|—|
|Requested-fp16<br>conversions (S<br>cont|/int8 rows are export invoc<br>ection III-C). No TensorRT<br>rolled PyTorch-vs-ONNX|ations, not verified pre<br> row. Latency is not a <br>microbenchmark.|cision<br> fully|


TABLE III 

|PAIRED <br>SAM<br>MCN|300-EPIS<br>E TETHER <br>EMAR: CO|ODE/SUITE EVALUATION(30 EPISODES/TASK, SEED42,<br> LOOP). NOT THE100-EPISODE MAIN EVALUATION.<br>NTINUITY-CORRECTED_χ_<sup>2 </sup>ON PAIRED PER-EPISODE<br>SUCCESS/FAILURE.|
|---|---|---|
|Suite|PyTorch|ONNX (width 16)<br>Gap (pp)<br>McNemar _χ_<sup>2</sup><br>_p_|
|Spatial|56.7|33.0<br>_−_23_._7<br>35.77<br>2_._2_×_10<sup>_−_9</sup>|
|Object|73.3|74.0<br>+0_._7<br>0.014<br>0.90|


The uniform ONNX Runtime bench used later for width comparison (Table V) reports width-16 p99 583.6 ms; 601 ms versus 583.6 ms reflects harness differences (tether inspect bench versus direct ORT Session.run), not a different model. Relative to PyTorch+AMP, p99 is about 2 _×_ lower, Spatial drops by 29–30 percentage points, and Object stays within one point. These timings are CUDA EP, not TensorRT. ONNX peak process memory is about 3.2 GB (requested-INT8 VRAM was not recorded). Disabling AMP raises PyTorch p99 to 1261 ms (supporting measurement; not the baseline). 

The PyTorch _→_ ONNX step changes framework, graph, arithmetic (AMP kernels vs. an FP32 graph), kernels, and runtime together. The speedup characterizes that coupled configuration, not a single precision switch. 

### _B. Open-loop identity check and 300-episode paired rollouts_ 

On 200 shared random inputs (seed 42), the requested-FP16 and requested-INT8 ONNX artifacts produce cosine similarity 1.0000 and zero maximum absolute difference at the recorded precision. This is an identity/parity check between those two artifacts on that input set. It is not a PyTorch-vs-ONNX comparison, and it is not evidence that INT8 quantization preserves FP16 outputs. 

Paired rollouts compare native PyTorch with the width-16 ONNX export on the same tether loop (30 episodes/task _×_ 10 tasks = 300 episodes/suite, seed 42; Table III). PyTorch Spatial/Object: 56.7%/73.3%; ONNX: 33.0%/74.0%. Object is near-matched; Spatial shows a large ONNX deficit. Absolute rates differ from the 100-episode main evaluation because the harnesses differ; the Spatial-vs-Object pattern is the same. The pairing reduces some seed/reset variation but does not isolate one runtime factor. An earlier adapter with _∼_ 0.98 per-step cosine vs. PyTorch still scored 0% closed-loop success, which is consistent with open-loop numerical agreement not implying closed-loop task agreement. 

### _C. Graph audit of requested FP16 and INT8 artifacts_ 

The requested-FP16 and requested-INT8 artifacts were byteidentical and contained FLOAT initializers without quantization operators (same SHA-256 for model.onnx and the 2.3 GB weight file; 22 514 nodes). Consequently, the requested-INT8 result does not represent operator-level INT8 quantization, and the observed latency difference between the two runs (601 vs. 532 ms p99) cannot be attributed to INT8 quantization. That difference is consistent with run-to-run CUDA-EP/runtime variability; the present experiments do not isolate its cause. tether 0.12.0’s monolithic path does not apply --precision; the flag is consumed by the TensorRT build path, which did not complete within 6 GB, so no TensorRT INT8 latency is reported. The 200-input identity check is consistent with the audit and does not establish robustness of a genuine INT8 implementation. Spatial 41.0% vs. 40.0% (one episode in 100) bounds success noise for this configuration. 

### _D. Static language-context ablation_ 

LeRobot appends a newline and tokenizes with the SmolVLM2 tokenizer (max_length=48). _Fed_ counts include that newline; _raw_ counts omit it and are one token shorter. Spatial raw lengths are approximately 15–19 tokens (mean 16.0, 3/10 exceed 16, max 19); fed lengths are 15–20 tokens (mean 17.0), and 5 of 10 Spatial tasks exceed width 16 (tasks 0, 1, 4, 5, 6). Object fed lengths are 11–13 tokens (mean 12.0); none exceed 16. No instruction in these two suites exceeds 24 tokens (Fig. 1). Tables and grouping use fed counts. 

Table IV groups Spatial episodes by whether the task was truncated _at width 16_ (five tasks, 50 episodes). That grouping is fixed across rows; it does not mean the same tasks are truncated at widths 24 or 32. With PyTorch the two groups are comparable (38/50 vs. 32/50). With width16 ONNX, previously-truncated-at-16 tasks fall to 3/50 and 4/50 (requested-fp16/int8 runs) while untruncated-at-16 tasks remain 38/50 and 36/50. 

Table V reports the 16/24/32 experiment (100 episodes/suite; uniform CUDA-EP bench). Width 24 raises Spatial success from 41.0% (requested-FP16 width 16) to 75.0%; width 32 yields 71.0%. Width-24 ONNX Spatial success was 75.0%, close to the PyTorch+AMP baseline of 70.0%; their Wilson 95% confidence intervals overlap. A two-proportion _χ_<sup>2</sup> comparing these rates ( _p_ =0 _._ 53) does not establish equivalence. Width 24 therefore substantially recovers Spatial performance; width 32 does not show an additional improvement over width 24. The 75.0% vs. 71.0% difference should not be read as a statistically established width effect. Recovery is concentrated in previouslytruncated-at-16 tasks (3–4/50 _→_ 36/50 at width 24; 34/50 at width 32); untruncated-at-16 tasks stay in 36–39/50. Object success remains approximately stable (89.0%, 90.0%, 87.0%). Uniform-bench p50/p99 and peak memory change only slightly (Table V). 

This provides evidence that static language-context width is an important contributor to the Spatial gap in the tested stack. 

## Instruction length vs static ONNX width 


Fig. 1. Fed instruction lengths (newline included) for ten Spatial and ten Object tasks versus static ONNX widths. Spatial: 5/10 exceed 16, max 20. Object: 0/10 exceed 16, max 13. 

TABLE IV 

SPATIAL EPISODES SOLVED OF 50. COLUMNS USE A FIXED GROUPING: TASKS TRUNCATED AT WIDTH 16 VS. TASKS NOT TRUNCATED AT WIDTH 16. WIDTHS 24 AND 32 TRUNCATE NONE OF THESE TASKS. BRACKETS: WILSON 95% CI ON THE _n_ =50 PROPORTION (%). 

|Configuration|Prev. trunc. at 16|Untrunc. at 16|Total /100|
|---|---|---|---|
|PyTorch+AMP|38 [62.6, 85.7]|32 [50.1, 75.9]|70|
|ONNX w16 (req. fp16)|3 [2.1, 16.2]|38 [62.6, 85.7]|41|
|ONNX w16 (req. int8)|4 [3.2, 18.8]|36 [58.3, 82.5]|40|
|ONNX w24|36 [58.3, 82.5]|39 [64.8, 87.2]|75|
|ONNX w32|34 [54.2, 79.2]|37 [60.4, 84.1]|71|


It does not show that width accounts for every PyTorch-vsONNX difference, and it does not establish a universal optimal width. 

On matched random images, state, and noise, width-16 and width-24 graphs agree on an 11-token Object instruction (cosine 1.000000, max _|_ ∆ _|_ 3 _._ 8 _×_ 10<sup>_−_6</sup> ). On a 19-token encoding of Spatial task 0, width 16 differs from PyTorch sample_actions (cosine 0.952, max _|_ ∆ _|_ 1.73) whereas width 24 agrees more closely (cosine 0.99997, max _|_ ∆ _|_ 0.028). This is consistent with truncation changing the model input; it is one-instruction evidence, not a suite-wide open-loop test. 

Fig. 2 uses the _same_ uniform ONNX bench as Table V for all three widths (PyTorch p99 remains the separate AMP bench). Width-24/32 occupy the same latency region as width 16 but recover Spatial success, which is consistent with the observed Spatial degradation being partly attributable to the static language interface rather than to the small latency differences across the tested ONNX widths. 

### IV. DISCUSSION 

### _A. What the measurements support_ 

Faster VLA inference is not automatically behaviorpreserving. The ONNX/CUDA EP configuration is substantially faster than the PyTorch+AMP bench on this GPU (roughly half the measured p99 latency on the respective benches), yet default-width Spatial closed-loop success falls by about 30 percentage points in the 100-episode main evaluation 


Fig. 2. p99 latency versus Spatial closed-loop success (Object annotated). ONNX widths use the uniform CUDA-EP bench of Table V; PyTorch uses the separate AMP bench. These harnesses are not identical. The 601/532 ms tether-inspect values are not plotted. 

while Object does not. Those latency figures characterize the respective benches, not a fully controlled microbenchmark. The 200-input ONNX-vs-ONNX identity check does not detect the closed-loop Spatial change; it only confirms that the two requested-precision artifacts match on those inputs. 

Increasing width from 16 to 24 substantially improves Spatial success (41.0%/40.0% _→_ 75.0%); width 32 (71.0%) does not show an additional benefit. Object success (89.0% _→_ 90.0%/87.0%) and uniform-bench p99 (583.6 _→_ 587.7/591.3 ms) remain approximately stable. Truncation falls from 5/10 Spatial tasks to 0/10, and recovery is concentrated in previously-truncated-at-16 tasks (Table IV). This provides evidence that static language-context width is an important contributor to the Spatial gap in the tested stack. It does not show that width accounts for every PyTorch-vs-ONNX difference, or that the same failure appears for other exporters or VLAs. 

### _B. Coupled deployment factors_ 

Table VI records isolation status. Changing from PyTorch+AMP to ONNX/CUDA EP can jointly change runtime, graph representation, kernels, numerical execution, languagecontext handling, memory behavior, and scheduling. The width ablation is useful because it varies one interface parameter while holding checkpoint, tether version, CUDA EP, hardware, and protocol fixed. The letter does not perform a full factorial isolation of PyTorch vs. ONNX, AMP vs. nonAMP, graph conversion, CUDA-EP kernels, language width, true FP16/INT8 conversion, or TensorRT. The requested-INT8 export is a second invocation of an unconverted graph (Section III-C). TensorRT execution was not obtained. We therefore do not claim complete causal attribution for the PyTorch-vsONNX gap, and we do not claim that latency itself caused the Spatial degradation. 

TABLE V 

CONTEXT-LENGTH ABLATION (100 EPISODES/SUITE, SEED 42, UNIFORM CUDA-EP BENCH: 50 WARMUP, 1000 CALLS). TRUNCATION USES FED TOKEN COUNTS. WIDTH-16 SUCCESS IS THE REQUESTED-FP16 EXPORT; THE REQUESTED-INT8 REPLICATE IS 40.0%/89.0%. SUCCESS BRACKETS: WILSON 95% CIS ( _n_ =100). 

|Width|Spatial trunc.|Object trunc.|Spatial suc.|Object suc.|p50 (ms)|p99 (ms)|Peak mem. (MB)|
|---|---|---|---|---|---|---|---|
|16|5/10|0/10|41.0 [31.9, 50.8]|89.0 [81.4, 93.7]|537.5|583.6|3184|
|24|0/10|0/10|75.0 [65.7, 82.5]|90.0 [82.6, 94.5]|544.5|587.7|3178|
|32|0/10|0/10|71.0 [61.5, 79.0]|87.0 [79.0, 92.2]|549.2|591.3|3178|


#### TABLE VI 

DEPLOYMENT FACTORS EVALUATED IN CONTROLLED ABLATIONS. 

|Factor|Isolated?|
|---|---|
|Language width (16/24/32)|Yes|
|PyTorch vs. ONNX runtime|No|
|Graph conversion|No|
|AMP vs. FP32 graph|No|
|CUDA-EP kernels|No|
|True INT8 vs. FP16 conversion|No|
|TensorRT engine execution|No|


A plausible interpretation, consistent with the observed pattern, is that truncating Spatial instructions can remove taskdisambiguating information near the instruction tail, whereas Object instructions are shorter. This reading was not independently tested. 

### _C. Limitations_ 

- One GPU (RTX 2060 6 GB); simulation only; no physical robot; no edge-device latency. 

- LIBERO Spatial and Object only; Goal and Long are unevaluated. 

- One checkpoint; one main seed (42); main evaluation 10 episodes/task; paired evaluation 30 episodes/task. Suitelevel Wilson 95% CIs and paired McNemar tests are reported; we do not run a multi-seed analysis. 

- Reported significance tests (paired McNemar; independent two-proportion _χ_<sup>2</sup> for width-24 vs. PyTorch+AMP Spatial) are presented individually without multiplecomparison correction. A non-significant two-proportion test is not an equivalence result. 

- TensorRT compilation/benchmarking was not completed under the 6 GB constraint. 

- The requested-INT8 artifact is not operator-level INT8; the 200-input check compares those identical ONNX files, not PyTorch vs. ONNX. 

- Factors other than language width are not factorially isolated (Table VI). 

- Width ablation tests only 16/24/32 tokens in one exporter/toolchain. 

- The PyTorch+AMP Spatial score (70%) differs from the SmolVLA publication (96%) and is not a direct reproduction of that headline rate. 

- Results do not generalize to all VLAs, exporters, or platforms. 

### V. CONCLUSION 

ONNX/CUDA EP produced substantially lower measured p99 latency than PyTorch+AMP in the tested deployment configurations (1181 ms _→_ 601/532 ms on the respective benches). That faster configuration did not preserve Spatial closed-loop success under the default width-16 export (70.0% _→_ 41.0%/40.0% in the 100-episode main evaluation); Object success remained approximately stable (88.0% vs. 89.0%). The 300-episode paired evaluation showed the same qualitative Spatial/Object pattern (56.7% vs. 33.0%; 73.3% vs. 74.0%). Increasing static language-context width to 24 recovered Spatial success (75.0%); width 32 (71.0%) did not show an additional benefit, while Object success and uniform-bench latency stayed approximately stable. Width-24 ONNX Spatial success was 75.0%, close to the PyTorch+AMP baseline of 70.0%; their Wilson 95% confidence intervals overlap. The requested-INT8 artifact was not operator-level INT8 quantized—it matched the requested-FP16 FP32 graph—so artifact-level verification is important before attributing observed behavior or latency differences to numerical precision. 

Deployment evaluation should jointly consider system-level latency and closed-loop task success, together with interface constraints and exported-graph inspection. These measurements are for one model, one GPU, and two LIBERO suites. Artifacts: https://github.com/rafiqul713/smolvla-libero-onnx. 

### ACKNOWLEDGMENT 

The author thanks the Hugging Face LeRobot and SmolVLA teams for open checkpoints and simulation benchmarks. All experiments used personal hardware (NVIDIA RTX 2060); no employer resources were used. 

### REFERENCES 

- [1] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti, S. Alibert, M. Cord, T. Wolf, and R. Cadene, “SmolVLA: A vision-languageaction model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [2] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “OpenVLA: An open-source vision-language-action model,” in _Proceedings of The 8th Conference on Robot Learning (CoRL)_ , 2025, pp. 2679–2713, also available as arXiv:2406.09246. 

- [3] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky, “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [4] J. Chen, J. Wang, L. Chen, C. Cai, and J. Lu, “NanoVLA: Routing decoupled vision-language understanding for nano-sized generalist robotic policies,” _arXiv preprint arXiv:2510.25122_ , 2025. 

- [5] J. Williams, K. D. Gupta, R. George, and M. Sarkar, “LiteVLA-Edge: Quantized on-device multimodal control for embedded robotics,” _arXiv preprint arXiv:2603.03380_ , 2026. 

- [6] J. Zhang, Y. Hsieh, Z. Wan, H. Lin, X. Wang, Z. Wang, Y. Lei, and M. Zhang, “QuantVLA: Scale-calibrated post-training quantization for vision-language-action models,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2026, pp. 39 539–39 549, also available as arXiv:2602.20309. 

- [7] F. Jiang, Z. Zheng, X. Cui, M. Li, J. Chen, and X. Chen, “EaqVLA: Encoding-aligned quantization for vision-language-action models,” _arXiv preprint arXiv:2505.21567_ , 2025. 

- [8] K. D. Nguyen, H. T. Ho, C. T. Nguyen, T. Q. Duong, L. D. Le, D. M. H. Nguyen, V. A. Ngo, and A. T. Le, “vla.cpp: A unified inference runtime for vision-language-action models,” _arXiv preprint arXiv:2606.08094_ , 2026. 

- [9] FastCrest, “Tether: VLA deployment CLI,” https://github.com/FastCrest/ tether, 2026, software repository. 

- [10] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “LIBERO: Benchmarking knowledge transfer for lifelong robot learning,” in _Advances in Neural Information Processing Systems_ , 2023. 

- [11] Hugging Face, “LIBERO evaluation with LeRobot,” https://huggingface. co/docs/lerobot/libero, 2026, official LeRobot documentation. 

- [12] LeRobot contributors, “SmolVLA cannot reproduce results in LIBERO eval using official checkpoints,” GitHub Issue #3264, https://github.com/ huggingface/lerobot/issues/3264, 2026, community issue; documents evaluation sensitivity, not a peer-reviewed result. 

