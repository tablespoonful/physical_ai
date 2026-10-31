---
title: "RAPT: Model-Predictive Out-of-Distribution Detection and Failure Diagnosis for Sim-to-Real Humanoid Deployment"
date: "2026-02-02"
authors: "Humphrey Munn; Brendan Tidd; Peter Bohm; Marcus Gallagher; David Howard"
url: https://arxiv.org/abs/2602.01515
pdf: https://arxiv.org/pdf/2602.01515
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.01515)** / [論文ページ](https://arxiv.org/abs/2602.01515)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **RAPT: Model-Predictive Out-of-Distribution Detection and Failure Diagnosis for Sim-to-Real Humanoid Deployment** 

**Humphrey Munn** 

**Brendan Tidd** 

School of Electrical Engineering and Computer Science CSIRO Technology, Australia University of Queensland, QLD 4072, Australia CSIRO Technology, Australia 

```
[h.munn@uq.edu.au]
```

**Marcus Gallagher** 

**Peter B¨ohm Marcus Gallagher** CSIRO Technology, Australia School of Electrical Engineering and Computer Science University of Queensland, QLD 4072, Australia 

**David Howard** 

CSIRO Technology, Australia 

**Abstract:** Deploying learned control policies is risky because policies that appear robust in simulation can confidently enter out-of-distribution (OOD) states after Sim-to-Real transfer, causing silent failures and potential hardware damage. Existing anomaly detectors often fail to meet the requirements of high-rate control, extremely low false-positive rates, and interpretable failure feedback. We present **RAPT** (Recurrent Anomaly Probabilistic Trajectory Model), a lightweight, selfsupervised 50 Hz deployment monitor that learns nominal execution from largescale simulation and produces calibrated, per-dimension predictive-deviation signals online. RAPT enables OOD detection under strict false-positive constraints while localizing _when and where_ real execution departs from nominal behavior. For post-hoc diagnosis, RAPT combines temporal saliency, joint-kinematic summaries, and LLM-based semantic reasoning to classify likely failure causes in a zero-shot setting. In simulation across four Isaac Lab tasks, RAPT improves TPR by 37% over the strongest baseline at 0 _._ 5% episode-level FPR; on hardware, it achieves 89% TPR across 78 trials with fewer false positives than high-frequencycompatible baselines, and reaches 75% semantic failure diagnosis accuracy across 21 categories on a challenging OOD subset. Project website, code, and videos: `https://humphreymunn.github.io/RAPT/` . 

**Keywords:** Robot Safety, Out-of-Distribution Detection, Sim-to-Real Transfer 

## **1 Introduction** 

Deploying learned humanoid control policies is risky: policies that appear robust in simulation can confidently enter out-of-distribution (OOD) states after Sim-to-Real transfer, causing silent failures and potential hardware damage [1, 2, 3]. These failures can arise from unmodeled dynamics, sensor noise, latency, payload changes, terrain variation, or implementation errors, and are particularly concerning for high-dimensional humanoids where unsafe actions can rapidly lead to falls, self-collisions, or hardware faults. Figure 1 illustrates representative real-world OOD scenarios encountered during humanoid deployment, along with the corresponding safety responses triggered by RAPT. 


Figure 1: **RAPT overview.** Real-world out-of-distribution (OOD) scenarios during humanoid deployment. RAPT detects anomalies online and triggers predefined safety responses, including safe stopping, controlled falling, and recovery behaviors. 

Existing anomaly detectors do not fully satisfy the requirements of deployment-time humanoid monitoring. Uncertainty and ensemble methods can be computationally expensive at control rate, generative models such as LSTM-VAEs can suffer from likelihood miscalibration and input-complexity bias [4, 5], and generic time-series methods often treat proprioceptive channels as independent signals rather than coupled robot states [6, 7]. Most importantly, many approaches provide only a binary stop signal, offering limited insight into _when_ , _where_ , or _why_ execution departed from nominal behavior. 

In this work, we introduce **RAPT** (Recurrent Anomaly Probabilistic Trajectory Model), a lightweight deployment-time monitoring and diagnostic system for humanoid robots. RAPT runs alongside a pre-trained control policy and learns a probabilistic model of nominal spatio-temporal behavior from simulation. During deployment, it evaluates predictive deviation as calibrated, perdimension signals, enabling online OOD detection under strict false-positive constraints while localizing when and which proprioceptive channels depart from nominal behavior. By optionally calibrating these signals on a small amount of verified nominal real-world data, RAPT can suppress static Sim-to-Real bias while still flagging new real-world deviations such as collisions, payload changes, terrain shifts, sensor faults, or actuator degradation. RAPT complements domain randomization and system identification: rather than replacing methods that reduce the Sim-to-Real gap before deployment, it monitors the residual mismatch and unforeseen OOD events that remain during real execution. This provides an observable deployment-time signal for safety monitoring and debugging without modifying the underlying controller. 

Our primary contributions are: 

- **Simulation-trained, deployment-calibrated monitoring:** RAPT learns nominal humanoid behavior from large-scale simulation and calibrates thresholds using either simulation or brief verified real-world data, supporting both Sim-to-Real debugging and hardwaretime OOD detection. 

- **Low-FPR OOD detection for high-DOF humanoids:** RAPT uses probabilistic predictive-deviation modeling with calibrated per-dimension, global, and optional range gates, outperforming high-frequency-compatible baselines under strict episode-level falsepositive constraints. 

- **Localized evidence for failure diagnosis:** RAPT produces per-dimension negative loglikelihood (NLL) signals and temporal saliency through the recurrent model, enabling posthoc semantic diagnosis without labeled failure data during detector training. 

We validate RAPT in NVIDIA Isaac Lab and on a physical Unitree G1. In simulation, RAPT improves TPR by 37% over the strongest baseline at 0 _._ 5% episode-level FPR; on real hardware, it achieves 89% TPR across 78 trials while supporting semantic diagnosis of challenging OOD failures. Upon acceptance, we will publicly release the training pipeline, labeled real-world datasets, and C++ deployment code to support reproducibility and future benchmarking. 

2 

## **2 Related Work** 

OOD detection in reinforcement learning remains fragmented in terminology and evaluation protocols [8, 9]. Unlike supervised OOD detection, robotic deployment anomalies may arise from sensory corruptions, software errors, unmodeled dynamics, contact changes, external collisions, payload shifts, or other events absent from policy training [3, 9]. These failures are challenging because learned policies can continue to act confidently after entering unsupported regions of the state–action distribution. 

Uncertainty-based methods such as MC Dropout, DropConnect, and ensembles estimate epistemic uncertainty through stochastic forward passes or model disagreement [1]. While useful for detecting unfamiliar states, their inference cost scales with samples or models, and they may miss environment or transition shifts when the policy remains confidently wrong [8]. RAPT instead uses a single-pass probabilistic monitor: aleatoric uncertainty is represented through a heteroscedastic likelihood output, while epistemic-style deployment uncertainty is exposed by running an independent nominal-behavior model alongside the policy. 

Generative, reconstruction-based, and time-series detectors learn nominal observations and flag lowlikelihood inputs [4, 6, 7]. However, likelihood models can suffer from input-complexity bias [5], while generic time-series methods often treat proprioceptive channels as independent signals rather than coupled robot states. Dynamics-based methods model transitions such as _P_ ( _st_ +1 _| st, at_ ) and can detect mechanical or environmental perturbations [3, 8]. Conformal prediction provides finite-sample coverage guarantees under exchangeability assumptions [10], but high-frequency humanoid deployment requires thresholds across many dimensions, rare long-tailed nominal events dominate low-FPR behavior, and safety demands extremely low episode-level false-positive rates. RAPT therefore uses calibrated per-dimension and global predictive-deviation gates as a practical compromise for low-FPR real-time detection with localization. 

Control-theoretic safety methods provide stronger guarantees when accurate dynamics and constraints are available [11, 12, 13, 14, 15]. However, learned humanoid controllers often operate in high-dimensional proprioceptive spaces where explicit dynamics are incomplete, difficult to identify, or too conservative for agile behavior. RAPT targets the intermediate regime where a controller is already trained, but residual sim-to-real mismatch and unforeseen real-world OOD events must still be detected, localized, and diagnosed. It complements methods that reduce the Sim-to-Real gap before deployment by monitoring the residual mismatch and deployment events that remain after transfer. Unlike pipelines trained mainly from small nominal real-world datasets, RAPT uses large-scale simulation to collect diverse nominal behavior for self-supervised detector training, while controlled OOD perturbations with known categories are used for evaluation and ablation in simulation. These labels are not required at deployment, but allow systematic testing of detection and diagnosis assumptions before adapting RAPT through brief nominal real-world calibration. 

## **3 Methodology** 

RAPT is a lightweight monitor that runs alongside a pre-trained humanoid policy. The pipeline has four stages: (i) collect nominal execution data from expert policies in large-scale simulation; (ii) train a self-supervised probabilistic trajectory model; (iii) calibrate predictive-deviation thresholds using nominal simulation or verified real-world data; and (iv) diagnose detected failures using temporal saliency and semantic reasoning. Fig. 2 summarizes the pipeline; implementation details and hyperparameters are provided in the Supplementary Material. 

### **3.1 Nominal Data Collection** 

For each task, we execute a pre-trained expert policy in NVIDIA Isaac Lab and collect nominal proprioceptive trajectories **o** _t ∈_ R<sup>_d_obs</sup> from the Unitree G1 humanoid. These simulation trajectories define the nominal behavior manifold that RAPT should preserve during deployment. All observations are normalized to zero mean and unit variance prior to training. Because the detector is trained 

3 


Figure 2: **RAPT Method Overview:** (A) RAPT OOD-detection architecture. (B) Hierarchical OOD pipeline using three statistical gates for real-time ( _∼_ 1.6ms) monitoring. (C) Detected anomalies trigger gradient-based saliency generation ( _st_ ) for zero-shot diagnosis via a multi-modal LLM. 

independently of the policy, it can be attached to existing learned controllers without modifying the control architecture or reward function. 

### **3.2 Probabilistic Recurrent Trajectory Model** 

RAPT is trained as a self-supervised recurrent reconstruction model over nominal execution. The architecture consists of a residual state encoder, a GRU-based temporal bridge, a latent bottleneck, and a probabilistic decoder. Given an observation history **o** _≤t_ , the encoder, GRU, and bottleneck produce a latent temporal representation **z** _t_ , which the decoder maps to a diagonal Gaussian reconstruction distribution: 


The model is trained by minimizing the negative log-likelihood (NLL) of nominal observations under this predicted distribution. This probabilistic formulation captures heteroscedastic aleatoric uncertainty: dimensions with naturally higher variability can be assigned larger predictive variance, while consistent dimensions are penalized more strongly when they deviate. We use denoising and a moderate latent bottleneck to discourage trivial identity reconstruction. 

For velocity tracking, we also evaluate a forward-dynamics variant that conditions on the previous observation and action ( **o** _t−_ 1 _,_ **a** _t−_ 1) and predicts **o** _t_ rather than reconstructing **o** _t_ . This was the only task-dependent design choice in the ablation: forward dynamics performed best for velocity tracking, while pure reconstruction was preferred for the other tasks; the remaining components were consistently beneficial across tasks. Full architectural details, loss expressions, training hyperparameters, and ablations are provided in the Supplementary Material. 

### **3.3 Simulation-Trained, Deployment-Calibrated OOD Detection** 

At deployment, RAPT evaluates the per-dimension predictive deviation of each incoming observation under the nominal trajectory model. Let _ℓt,i_ denote the NLL contribution of observation dimension _i_ at time _t_ , and let _ℓ_<sup>¯</sup> _t_ denote the mean NLL across dimensions. Detection thresholds are calibrated using nominal data from either simulation or real-world operation, depending on the use case. When calibrated on a large nominal simulation batch, RAPT measures deviations from the simulation-trained behavior distribution, making residual Sim-to-Real mismatch visible during deployment. When calibrated on a brief verified nominal real-world run, RAPT adapts to 

4 

static deployment-domain offsets caused by sensor noise, actuation latency, contact differences, and hardware-specific dynamics, enabling detection of new OOD events relative to nominal hardware behavior. 

RAPT applies two gates for detection: a local gate that detects unusually large per-dimension deviations, and a global gate that detects broad shifts in the mean predictive deviation. In our implementation, thresholds are set using a max-plus- _kσ_ rule over the selected calibration data: 


Rare nominal spikes observed during calibration are treated as nominal, while persistent, localized, or distributed deviations beyond this envelope are flagged as OOD; local gates support channel-level localization and the global gate captures broader mismatch. 

### **3.4 Hybrid Safety Envelope** 

RAPT is optionally paired with a deterministic range detector to provide a simple safety envelope for observations outside calibrated nominal bounds. The final anomaly decision is the logical OR of the local RAPT gate, global RAPT gate, and range detector; range-bound construction is provided in the Supplementary Material. 

### **3.5 Temporal Saliency for Failure Localization** 

After an anomaly is detected, RAPT computes post-hoc temporal saliency to identify which observations contributed most strongly to the predictive deviation. Because the detector is recurrent, failures may accumulate over time before crossing the detection threshold. We therefore compute gradients of the final NLL with respect to a history window **X** _t_ = [ **o** _t−H , . . . ,_ **o** _t_ ], using integrated gradients through the recurrent model. This produces a spatio-temporal attribution map over observation dimensions and past timesteps, highlighting both _where_ and _when_ the execution first departed from nominal behavior. 

Using the NLL as the saliency objective naturally weights attributions by the model’s predictive uncertainty: deviations in high-confidence dimensions receive stronger attribution than deviations in noisy or intrinsically variable dimensions. This allows operators to distinguish sudden external disturbances, gradual actuator degradation, sensor drift, and other temporally structured failure modes. Full details of the saliency baseline, integration procedure, and visualization protocol are provided in the Supplementary Material. 

### **3.6 Semantic Failure Diagnosis** 

Saliency localizes anomalous features but does not by itself provide a semantic explanation. To support post-hoc diagnosis, we provide a multi-modal LLM with structured diagnostic evidence, including temporal saliency summaries, joint-kinematic trajectories, task context, and, when available, a synchronized visual keyframe. The LLM performs zero-shot classification over a predefined set of failure categories, producing a likely failure hypothesis for operator review. 

This diagnostic stage is not used for real-time safety triggering and is not intended to replace human judgment. Instead, it converts calibrated anomaly evidence into interpretable semantic labels that can accelerate post-incident debugging, such as distinguishing terrain/contact issues, external collisions, payload mismatch, sensor corruption, latency, or actuator faults. The failure taxonomy and prompt format are given in the Supplementary Material. 

## **4 Experimental Setup** 

### **4.1 Tasks, Policies, and Simulation Protocol** 

We evaluate RAPT on four Unitree G1 humanoid tasks: velocity-tracking locomotion, motion mimicry (Dance102 and Gangnam), and ballistic throwing. Locomotion and mimicry follow the 

5 

`unitree` ~~`r`~~ `l` ~~`l`~~ `ab` benchmark [16], while throwing follows [17]. For each task, we train five expert policies with different random seeds using GCR-PPO [18]. 

Large-scale OOD evaluation is performed in NVIDIA Isaac Lab using _N_ env = 4096 parallel environments per task. Each evaluation run uses a 50/50 split between nominal rollouts for false-positive evaluation and controlled OOD perturbations for true-positive evaluation. We inject 15 OOD categories spanning sensor faults, physics perturbations, actuator changes, initialization errors, and software/communication faults. A brief nominal calibration episode precedes evaluation to establish detector thresholds. Additional task, perturbation, and implementation details are provided in the Supplementary Material. 

### **4.2 Baselines** 

We compare RAPT against representative high-frequency-compatible anomaly detectors: PatchAD [7], LSTM-VAE [4], Deep SVDD [19], and Isolation Forest [20]. All methods are trained on identical nominal data and evaluated on the same logs. Where source code was unavailable, we re-implemented methods following the original specifications and selected hyperparameters for stable 50 Hz deployment under comparable computational budgets; full details are provided in the Supplementary Material. 

### **4.3 Real-World Deployment** 

We deploy RAPT on a physical Unitree G1 humanoid at 50 Hz. The real-world evaluation contains 78 runs: 15 nominal and 63 anomalous. A brief calibration set of 3 _×_ 1 min nominal runs is used to set thresholds; nominal evaluation includes 1, 2, 4, and 10 min runs, with half of the longer runs collected the day after calibration to test temporal robustness. Anomalous trials span contact, payload, actuation, latency, initialization, observation-ordering, pushes, collisions, motor failures, dynamics mismatch, and sensor-noise perturbations. All proprioceptive data and RAPT outputs are logged online, and baselines are evaluated offline on the same trajectories. 

### **4.4 Evaluation Metrics** 

In simulation, we report AUROC and Safety Score, defined as True Positive Rate (TPR) at a fixed episode-level False Positive Rate (FPR) of 0 _._ 5%, reflecting the low false-positive requirements of real deployment. We also report per-step inference runtime to assess suitability for 50 Hz control. Since all detectors operate at the same control frequency, detection delay is determined by anomalyscore dynamics rather than raw inference speed; category-specific delay statistics are reported in the Supplementary Material. 

On hardware, we report trial-level confusion counts where available, together with TPR and FPR. For semantic failure diagnosis, we evaluate zero-shot classification accuracy on the subset of detected OOD trials with complete diagnostic labels and synchronized evidence. 

## **5 Results** 

We evaluate RAPT along three axes: simulation detection accuracy, real-world generalization, and semantic failure diagnosis. 

### **5.1 Simulation Benchmarks** 

We evaluate anomaly detection performance in simulation following the protocol described in Section 4.1. Results are summarized using inference latency, AUROC, and Safety Score (TPR @ 0.5% FPR), as defined in the Experimental Setup. 

**Performance Analysis:** As shown in Table 1, RAPT attains the highest Safety Score and AUROC across all evaluated tasks while maintaining low inference latency (1.63 ms, _<_ 10% of the 20 ms 

6 

Table 1: **Safety & Performance Comparison.** Safety Score (TPR @ 0.5% FPR) reported per task, with aggregate AUROC. RAPT attains the highest values on both metrics across all tasks. Model Only and Hybrid denote performance without and with the Range Detector, respectively. Results averaged over 5 seeds (± std). * indicates RAPT trained with a forward dynamics objective; all others use reconstruction. 

|**Method**|**Glob**<br>**Latency**|**al Metrics**<br>**Avg AUROC**|**Sa**<br>**Throwing**|**fety Score (**<br>**Velocity**|**TPR @ 0.5% FPR**<br>**Mimic (Dance)**|**) by Task**_↑_<br>**Mimic (Gangnam)**|**Ablati**<br>**Model Only**|**on**<br>**Hybrid**|
|---|---|---|---|---|---|---|---|---|
|Isolation Forest|4.32 ms|0.69|0.24 ±0.04|0.34 ±0.03|0.42 ±0.01|0.38 ±0.00|0.18|0.34|
|PatchAD|11.45 ms|0.73|0.14 ±0.01|0.16 ±0.03|0.17 ±0.04|0.16 ±0.03|0.18|0.16|
|Deep SVDD|0.45 ms|0.67|0.29 ±0.03|0.31 ±0.10|0.41 ±0.01|0.37 ±0.01|0.14|0.34|
|LSTM-VAE|1.77 ms|0.77|0.30 ±0.02|0.36 ±0.02|0.44 ±0.01|0.42 ±0.01|0.32|0.38|
|Ours (RAPT)|1.63 ms|**0.92**|**0.72** ±0.05|**0.74**<sup>_∗_</sup>±0.02|**0.67** ±0.08|**0.75** ±0.02|**0.75**|**0.72**|


control budget). Compared to the strongest baseline (LSTM-VAE), RAPT achieves a +0.34 absolute improvement in Safety Score at the fixed false-positive operating point. 

Notably, the relative performance gap between RAPT and prior methods is more pronounced for Safety Score than AUROC. This suggests that several baselines achieve reasonable thresholdindependent separability, but struggle with sensitivity when false positives are tightly constrained. We attribute this to overlap between in-distribution and out-of-distribution tails, which degrades precision at low false-positive rates. 

**Hybrid vs. Model-Only Detection:** To ensure fair comparison, all methods were evaluated both with and without the auxiliary Range Detector. As shown in the _Model Only_ and _Hybrid_ columns of Table 1, shallow baselines (e.g., Isolation Forest, Deep SVDD) rely heavily on explicit range checks, exhibiting reduced performance when evaluated in isolation. In contrast, RAPT remains robust without the range detector (0.75 vs. 0.72 Safety Score), indicating that it internalizes much of the valid state manifold structure. The small drop in the hybrid setting is attributable to additional false positives introduced by conservative range thresholds. 

### **5.2 Ablation Studies** 

We analyze key design choices using a Taguchi L12 orthogonal array over 48 models, with full results in the Supplementary Material. The dominant factor is inference logic: per-dimension maximum aggregation improves Safety Score by +14.3% over global mean aggregation, indicating that OOD deviations are often localized to a subset of channels. Probabilistic NLL scoring improves robustness under heteroscedastic noise (+10.3%), while temporal recurrence (+8.5%), low latent compression (+7.8%), and residual connections (+4.5%) provide additional gains. These results motivate the final RAPT design. The results challenge the assumption that a single global anomaly score is sufficient for robot deployment: under strict low-FPR constraints, failures in high-DOF humanoid control are often expressed as localized deviations in a small subset of channels, making calibrated per-dimension evidence critical for both detection and interpretation. 

### **5.3 Real-World Deployment** 

We evaluate RAPT on physical hardware using the protocol in Section 4.3. As shown in Table 2, RAPT+Range achieves the strongest real-world performance, detecting 56 out of 63 anomalous runs with one false positive over 15 nominal trials (88.9% TPR, 6.7% episode-level FPR); the single false positive occurred during a deliberately challenging 10 min nominal run. PatchAD is omitted from the expanded table because many safety-terminated runs were shorter than its required context window; on the 27-run subset where PatchAD was applicable, it achieved 41.6% recall, compared with 66.7% for RAPT and 75.0% for RAPT+Range, all without false positives. RAPT detects dynamic interaction faults that do not necessarily violate explicit bounds, while the range detector captures hard state-space violations; their combination improves robustness across physical perturbations. Beyond quantitative detection, RAPT also flagged silent configuration errors during integration, such as under-tuned wrist PD gains, highlighting its use as a deployment verification tool. 

7 

Table 2: **Real-World Anomaly Detection on Unitree G1.** Results over _N_ = 78 trials: 15 nominal and 63 anomalous. PatchAD is omitted because many safety-terminated anomalous runs were shorter than its required context window. 

|**Method**|**TPR**_↑_|**FPR**_↓_|**TP**|**FN**|**TN**|**FP**|
|---|---|---|---|---|---|---|
|SVDD<br>Isolation Forest|28.3%<br>26.0%|60.0%<br>13.3%|18<br>16|45<br>47|6<br>13|9<br>2|
|LSTM-VAE|28.6%|13.3%|18|45|13|2|
|RAPT (Ours)<br>**RAPT + Range (Hybrid)**|85.7%<br>**88.9%**|6.7%<br>**6.7%**|54<br>**56**|9<br>**7**|14<br>**14**|1<br>**1**|


Table 3: **Semantic Failure Diagnosis Accuracy.** Top-1 and Top-3 classification accuracy across 16 real-world failure scenarios. 

|**Method**|**Top-1 Ac**|**curacy**|**Top-3 A**|**ccuracy**|
|---|---|---|---|---|
||**Count**|**%**|**Count**|**%**|
|Proprioceptive Only (RAPT)<br>**RAPT + Visual Keyframe**|12 / 16<br>**14 / 16**|75.0<br>**87.5**|14 / 16<br>**16 / 16**|87.5<br>**100.0**|
|_Improvement_|2 / 16|12.5|2 / 16|12.5|


### **5.4 Automated Root-Cause Diagnosis** 

We evaluate the diagnostic pipeline on 16 real-world failure logs with complete diagnostic data following successful anomaly detection by RAPT (Hybrid). The subset is intended to test whether temporal saliency through the recurrent detector provides useful diagnostic evidence, so we focus on failures that evolve over time rather than immediate, protocol-defined violations whose category is typically evident from the test condition. These cases include external disturbances, payload mismatch, terrain/contact changes, and physical obstructions, where diagnosis requires interpreting temporal proprioceptive and kinematic evidence. Each failure is classified into one of 21 predefined categories (see Supplementary Material), and results are reported for Proprioceptive Only and MultiModal variants, the latter using a single time-synchronized visual key-frame. 

As shown in Table 3, the Multi-Modal configuration improves both Top-1 and Top-3 accuracy relative to the proprioceptive-only baseline. Visual context helps disambiguate external disturbances from internal system faults, such as obstacle contact versus motor-dynamics mismatch. 

From an operational perspective, narrowing a failure to the relevant subsystem or signal group can substantially reduce post-incident debugging time. The diagnostic pipeline helps distinguish localized faults, such as an individual motor or sensor channel, from broader semantic shifts caused by external contact, payload mismatch, latency, or controller/configuration errors. In practice, this helped identify silent sim-to-real discrepancies, such as mismatched PD gains or implementationlevel inconsistencies in the deployed state pipeline. 

## **6 Limitations** 

RAPT has several limitations. Hardware evaluation remains constrained by safety, time, and platform availability: trials cover diverse OOD events, but only on a single humanoid over short-term deployments. RAPT is also a monitor rather than a formal safety guarantee: it detects deviations from calibrated nominal behavior and triggers predefined responses, but does not synthesize safe controls or prove constraint satisfaction. Calibration can trade false positives against sensitivity, with more conservative thresholds reducing false alarms at the cost of delayed or missed detections. Finally, semantic diagnosis is post-hoc and assistive, so ambiguous or compound failures may still require expert interpretation. 

## **7 Discussion and Conclusion** 

We presented RAPT, a lightweight self-supervised monitor for detecting and diagnosing OOD behavior during deployment of learned humanoid policies. RAPT learns a probabilistic spatiotemporal model of nominal execution and uses calibrated predictive deviations for high-frequency, 

8 

low-FPR detection. Unlike binary anomaly detectors, RAPT provides per-dimension evidence that localizes when and where execution departs from nominal behavior, enabling temporal saliency and semantic diagnosis. 

Across simulation and real-world experiments, RAPT outperforms high-frequency-compatible baselines while remaining real-time deployable. The results suggest that RAPT is useful for both safety triggering and deployment debugging, complementing domain randomization and system identification by monitoring residual mismatch and unforeseen OOD events after transfer. 

9 

### **Acknowledgments** 

If a paper is accepted, the final camera-ready version will (and probably should) include acknowledgments. All acknowledgments go at the end of the paper, including thanks to reviewers who gave useful comments, to colleagues who contributed to the ideas, and to funding agencies and corporate sponsors that provided financial support. 

## **References** 

- [1] A. P. Mohammed and M. Valdenegro-Toro. Benchmark for out-of-distribution detection in deep reinforcement learning. _arXiv preprint arXiv:2112.02694_ , 2021. 

- [2] T. Haider, K. Roscher, B. Herd, F. Schmoeller Roza, and S. Burton. Can you trust your agent? the effect of out-of-distribution detection on the safety of reinforcement learning systems. In _Proceedings of the 39th ACM/SIGAPP Symposium on Applied Computing_ , pages 1569–1578, 2024. 

- [3] T. Haider, K. Roscher, F. Schmoeller da Roza, and S. G¨unnemann. Out-of-distribution detection for reinforcement learning agents with probabilistic dynamics models. In _Proceedings of the 2023 International Conference on Autonomous Agents and Multiagent Systems_ , pages 851–859, 2023. 

- [4] D. Park, Y. Hoshi, and C. C. Kemp. A multimodal anomaly detector for robot-assisted feeding using an lstm-based variational autoencoder. _IEEE Robotics and Automation Letters_ , 3(3): 1544–1551, 2018. 

- [5] E. Nalisnick, A. Matsukawa, Y. W. Teh, D. Gorur, and B. Lakshminarayanan. Do deep generative models know what they don’t know? _arXiv preprint arXiv:1810.09136_ , 2018. 

- [6] A. Z. Sellam, I. Benaissa, A. Taleb-Ahmed, L. Patrono, and C. Distante. Mamba adaptive anomaly transformer with association discrepancy for time series. _arXiv preprint arXiv:2502.07858_ , 2025. 

- [7] Z. Zhong, Z. Yu, Y. Yang, W. Wang, K. Yang, and C. P. Chen. Patchad: A lightweight patchbased mlp-mixer for time series anomaly detection. _IEEE Transactions on Big Data_ , 2025. 

- [8] M. Prashant, A. Easwaran, S. Das, and M. Yuhas. Guaranteeing out-of-distribution detection in deep rl via transition estimation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pages 12452–12460, 2025. 

- [9] L. Nasvytis, K. Sandbrink, J. Foerster, T. Franzmeyer, and C. S. de Witt. Rethinking outof-distribution detection for reinforcement learning: Advancing methods for evaluation and detection. _arXiv preprint arXiv:2404.07099_ , 2024. 

- [10] C. Xu, T. K. Nguyen, E. Dixon, C. Rodriguez, P. Miller, R. Lee, P. Shah, R. Ambrus, H. Nishimura, and M. Itkina. Can we detect failures without failure data? uncertainty-aware runtime failure detection for imitation learning policies. _arXiv preprint arXiv:2503.08558_ , 2025. 

- [11] L. Brunke, M. Greeff, A. W. Hall, Z. Yuan, S. Zhou, J. Panerati, and A. P. Schoellig. Safe learning in robotics: From learning-based control to safe reinforcement learning. _Annual Review of Control, Robotics, and Autonomous Systems_ , 5:411–444, 2022. 

- [12] F. Berkenkamp, M. Turchetta, A. Schoellig, and A. Krause. Safe model-based reinforcement learning with stability guarantees. In _Advances in neural information processing systems_ , volume 30, 2017. 

- [13] Y. Chow, O. Nachum, A. Faust, E. Duenez-Guzman, and M. Ghavamzadeh. Lyapunov-based safe policy optimization for continuous control. _arXiv preprint arXiv:1901.10031_ , 2019. 

10 

- [14] R. Cheng, G. Orosz, R. M. Murray, and J. W. Burdick. End-to-end safe reinforcement learning through barrier functions for safety-critical continuous control tasks. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 33, pages 3387–3395, 2019. 

- [15] M. Alshiekh, R. Bloem, R. Ehlers, B. K¨onighofer, S. Niekum, and U. Topcu. Safe reinforcement learning via shielding. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 32, 2018. 

- [16] Unitree Robotics. unitree ~~r~~ l ~~l~~ ab: Reinforcement learning implementation for unitree robots based on isaaclab. `https://github.com/unitreerobotics/unitree_rl_lab` , 2024. 

- [17] H. Munn, B. Tidd, P. B¨ohm, M. Gallagher, and D. Howard. Whole-body dynamic throwing with legged manipulators. In _Proceedings of the 27th Australasian Conference on Robotics and Automation (ACRA)_ , Perth, Australia, Dec. 2025. Available at arXiv:2410.05681. 

- [18] H. Munn, B. Tidd, P. B¨ohm, M. Gallagher, and D. Howard. Scalable multi-objective robot reinforcement learning through gradient conflict resolution. _arXiv:2509.14816_ , 2025. 

- [19] L. Ruff, R. Vandermeulen, N. Goernitz, L. Deecke, S. A. Siddiqui, A. Binder, E. M¨uller, and M. Kloft. Deep one-class classification. In _International conference on machine learning_ , pages 4393–4402. PMLR, 2018. 

- [20] F. T. Liu, K. M. Ting, and Z.-H. Zhou. Isolation forest. In _2008 eighth ieee international conference on data mining_ , pages 413–422. IEEE, 2008. 

11 

