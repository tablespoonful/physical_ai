---
title: "VLA-Corrector: Lightweight Detect-and-Correct Inference for Adaptive Action Horizon"
date: "2026-07-02"
authors: "Yi Pan; Miao Pan; Qi Lu; Jiaming Huang; Man Zhang; Siteng Huang"
url: https://arxiv.org/abs/2607.01804
pdf: https://arxiv.org/pdf/2607.01804
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.01804)** / [論文ページ](https://arxiv.org/abs/2607.01804)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**OmniAI Group of ZJU ACES Lab** 


## **OmniAI Group of ZJU ACES Lab** 

Zhejiang University 


# **VLA-Corrector: Lightweight Detect-and-Correct Inference for Adaptive Action Horizon** 

**Yi Pan**<sup>1</sup> , **Miao Pan**<sup>1</sup> , **Qi Lu**<sup>1</sup> , **Jiaming Huang**<sup>1</sup> , **Man Zhang**<sup>1</sup> , **Siteng Huang**<sup>2</sup> , **Xin Li**<sup>2</sup> , **Jie Zhang**<sup>1</sup> , **Yongliang Shen**<sup>1</sup> , **Xuhong Zhang**<sup>1</sup> , **Wenqi Zhang**<sup>1</sup> 

> 1Zhejiang University 2Alibaba DAMO Academy 

Vision-Language-Action (VLA) foundation models have recently achieved strong progress in embodied intelligence. To reduce policy-call frequency while preserving temporal coherence, most generative policies adopt an **action chunk** mechanism, executing multiple future actions in an open-loop manner under a fixed **action horizon** . However, this “predict-then-blindly-execute” paradigm sacrifices closedloop reactivity: in contact-rich physical interactions, even small local perturbations can rapidly amplify within the open-loop blind spot, leading to compounding errors and ultimately task failure. To address this limitation, we propose **VLA-Corrector** , a lightweight corrective inference framework for action-chunked VLA policies. Without modifying the backbone policy weights, VLA-Corrector introduces a lightweight **Latent-space Vision Monitor** (LVM) that continuously compares predicted and actual visual feature evolution, enabling online detection of visual dynamics deviations. Once persistent deviation is detected, the system triggers a truncation event, discards the remaining stale actions, and invokes corrective replanning via **Online Gradient Guidance** (OGG). The detect-andcorrect mechanism of VLA-Corrector naturally induces an **event-triggered adaptive action horizon** : it preserves long-horizon execution when the current chunk remains reliable, and invokes short-horizon corrective replanning when execution begins to drift. In doing so, VLA-Corrector mitigates the trade-off imposed by static horizons between execution robustness and policy-call frequency. It can be integrated into different VLA models without further retraining the VLA backbone, interrupting compounding errors while preserving much of the efficiency benefit of action chunking and substantially improving robustness in long-horizon, contact-rich robotic manipulation tasks. Our code is available at `https://github.com/ZJU-OmniAI/vla-corrector` . 

**Yi Pan:** `panyi0304@gmail.com` **Wenqi Zhang:** `zhangwenqi@zju.edu.cn` **Date:** October 2026 

## **Contents** 

|**1**<br>**Intr**|**oduction**|**3**|
|---|---|---|
|**2**<br>**Pre**|**liminaries**|**5**|
|**3**<br>**VL**|**A-Corrector: A Lightweight Corrective Inference Framework**|**5**|
|3.1|Training the External Latent Dynamics Corrector. . . . . . . . . . . . . . . . . .|. . . . . . .<br>5|
|3.2|Latent Visual Dynamics for Online Anomaly Detection. . . . . . . . . . . . . . .|. . . . . . .<br>6|
|3.3|Event-Triggered Truncation under Robust Online Monitoring . . . . . . . . . . .|. . . . . . .<br>6|
|3.4|Online Gradient Guidance for Corrective Inference . . . . . . . . . . . . . . . . .|. . . . . . .<br>7|
|**4**<br>**Exp**|**eriments**|**7**|
|4.1|Main Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>7|
|4.2|Mechanism Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>9|
|4.3|Real-World Evaluation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>10|
|4.4|Ablation Studies<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>11|
|**5**<br>**Con**|**clusion**|**11**|
|**A Rel**|**ated Work**|**15**|
|A.1|Generative VLA Models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>15|
|A.2|Action Chunk and Horizon Trade-off . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>15|
|A.3|Failure Recovery in Visuomotor Policies . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>15|
|**B Me**|**thod Details**|**16**|
|B.1|Details of Event-Triggered Truncation . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>16|
|B.2|LVM and OGG Runtime Parameters . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>16|
|**C Tra**|**ining and Implementation Details**|**16**|
|C.1|Benchmarks and Evaluation Protocol . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>16|
|C.2|External Corrector Architecture. . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>17|
|C.3|Corrector Training . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>17|
|C.4|Compute Resources. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>17|
|**D Add**|**itional Experimental Results**|**18**|
|D.1|Ablation Sensitivity<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>18|
|D.2|Cross-Domain Corrector Generalization<br>. . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>18|
|D.3|Full Performance–Efficiency Results<br>. . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>19|
|D.4|Data Efficiency of Corrector Training . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>19|
|D.5|Inference-Time Cost and Control Delay<br>. . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>20|
|D.6|Asynchronous and RTC Comparisons. . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>21|
|**E Rea**|**l-World Details**|**22**|
|E.1|Robot Platform and Task Suite . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>22|
|E.2|Per-Task Real-World Results<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>23|
|E.3|Real-World Protocol and Task Details . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>23|
|E.4|Observed Real-World Failure Modes . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>24|
|E.5|Real-World Demonstration Examples . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>24|


2 

## **1 Introduction** 

Vision-Language-Action (VLA) foundation models have emerged as a promising path toward general-purpose robot control, unifying perception, language, and action generation within a single framework Zitkovich et al. (2023); O’Neill et al. (2024); Kim et al. (2024); Black et al. (2024); Li et al. (2023); Bjorck et al. (2025); Intelligence et al. (2025); Ma et al. (2024); Wang et al. (2026a); Cen et al. (2025); Jiang et al. (2025b). Modern VLA policies often rely on generative action models, such as diffusion models and flow matching, to capture the high-dimensional and multi-modal nature of continuous robot actions Black et al. (2024); Chi et al. (2025); Jiang et al. (2025a); Wang et al. (2024); Lipman et al. (2022). However, the per-step latency of generative models precludes closed-loop replanning, creating a fundamental tension between action expressiveness and high-frequency feedback control. 

A common engineering compromise is to use an **action chunk** Zhao et al. (2023a): in a single forward pass, the policy predicts a sequence of future actions, while the controller only executes the first _H_ steps as the **action horizon** Jing et al. (2025); Liu et al. (2024); Sendai et al. (2025); Chi et al. (2025); Khan and Tanimura (2025); So et al. (2025). This design amortizes policy-call frequency and improves temporal smoothness, but it also creates an **open-loop blind spot** Wang et al. (2026b); Xu et al. (2026) that introduces two compounding risks. **First, the policy lacks real-time reactivity** . Fresh observations arrive at every control step, yet the system ignores them until the horizon ends, leaving it unable to respond to unexpected slippage, collision, or pose drift as they occur. **Second, errors can accumulate beyond the point that replanning can recover from during the blind spot** . If deviations go uncorrected long enough, the robot may drift into an out-of-distribution state that the policy has rarely encountered during training, at which point even the next replanning call cannot steer execution back to the intended trajectory Wang et al. (2026b); Liu et al. (2024); Sendai et al. (2025); Wu et al. (2026a); Xu et al. (n.d.), and the task ultimately fails. Crucially, both risks worsen as the horizon grows longer. As illustrated in Fig. 1, under a long horizon ( _H_ = 10), the robot keeps executing stale actions after a deviation and eventually gets stuck; in contrast, with _H_ = 1, the policy replans at every step and avoids the same error accumulation. 

Yet _H_ = 1 is not a practical solution: it requires a full VLA inference at every control step, negating the efficiency gains that action chunking was designed to provide. The contrast between these two extremes thus exposes a fundamental trade-off: smaller horizons improve closed-loop responsiveness but multiply policy-call frequency, while larger horizons amortize computation but widen the blind spot where errors silently accumulate. 

To quantify this trade-off, we conduct systematic experiments comparing task success rate and policy frequency across a range of action horizons on three VLA backbones. As shown in Fig. 2, larger horizons substantially reduce policy calls but also lead to lower success rates, and this trend is consistently observed across all three backbones. For _π_ 0 _._ 5 Intelligence et al. (2025), for example, increasing the horizon reduces policy calls by about 4 _×_ , but lowers success from about 64% to below 49%; similar trends hold for SmolVLA Shukor et al. (2025) 


**Figure 2 Performance–efficiency trade-off across fixed action horizons.** Smaller horizon achieves higher success rates, while larger horizon preserves the chunking efficiency. 

and X-VLA Zheng et al. (2025). Furthermore, since the best horizon depends on task difficulty, environmental dynamics, and sim-to-real mismatch, it is difficult to predefine a single static horizon that remains optimal across scenarios. This suggests that the key is not to choose a better fixed horizon, but to decide when the current chunk should stop being trusted. 

The above analysis raises two key questions: (1) How to **detect execution deviations in time** and **terminate stale actions** before errors compound beyond recovery; (2) How to **correct the trajectory after truncation** — since naive replanning alone is often insufficient: the VLA may re-generate actions that still fail to escape the 

3 


**Figure 1 Open-loop vs. Closed-loop execution.** The top row ( _H_ = 10) illustrates how blindly executing long action chunks leads to compounding errors, causing the robot to get stuck during a drawer-opening task. In contrast, the bottom row ( _H_ = 1) demonstrates strict closed-loop execution, which maintains environmental reactivity and yields a smooth, successful manipulation. 

deviated state, leaving the robot trapped again. 

Motivated by these insights, we propose **VLA-Corrector** , a lightweight corrective inference framework that addresses both questions. For the first, VLA-Corrector introduces a **Latent-space Vision Monitor** (LVM) that continuously compares predicted and actual visual evolution during open-loop execution; once persistent deviation is detected, it triggers an **interrupt event** that immediately truncates the remaining stale actions and invokes a new action generation. For the second, rather than relying on naive replanning, VLA-Corrector activates **Online Gradient Guidance** (OGG), which exploits the discrepancy between predicted and observed visual dynamics to inject a corrective gradient during new action generation—actively steering the robot back toward the intended trajectory, instead of simply hoping that re-inference will naturally recover. Together, LVM-triggered truncation and OGG-guided re-inference transform a fixed action horizon into an **adaptive action horizon** with **self-correcting re-inference** , preserving long-horizon efficiency and short-horizon responsiveness. 

These two mechanisms jointly improve success-per-call efficiency: the robot avoids wasting long chunks on stale actions, so each policy query contributes more effectively to task completion. For _π_ 0 _._ 5 at horizon 50, success rises from 48.7% to 58.7% while average policy calls drop from 5.15 to 4.98—a +24 _._ 6% success-per-call efficiency gain. Gains are consistent across all three backbones and grow larger at longer horizons, where the open-loop blind spot is widest. Beyond robustness, VLA-Corrector also improves sample efficiency: on LIBERO, a few-shot fine-tuned model augmented with VLA-Corrector reaches 97.8% average success, _surpassing_ the fully fine-tuned baseline (96.9%). 

Our contributions are summarized as follows: 

• We systematically quantify the performance–efficiency trade-off induced by fixed action horizon in actionchunked VLA policies, showing that the open-loop blind spot consistently affects robustness across different VLA backbones. 

- We propose VLA-Corrector, a lightweight inference-time framework that augments a frozen VLA backbone 

- with latent-space monitoring, event-triggered truncation, and guidance toward recovery-oriented inference. 

- We validate VLA-Corrector across simulation and real-world tasks, showing that it achieves stronger 

- robustness, higher success-per-call efficiency, and adaptive correction behavior. 

4 

## **2 Preliminaries** 

**VLA Policies with Action Chunks.** In embodied continuous control, the current visual observation _ot_ is first encoded into a latent representation _Zt_<sup>real</sup> = _E_ ( _ot_ ) by a visual encoder _E_ . To balance policy-call frequency and action smoothness, modern generative VLA policies parameterized by _θ_ commonly predict an **action chunk** in a single inference call, 


where _at_ denotes a single control action and _l_ is the language instruction. During deployment, only the first _H_ actions, with _H ≤ C_ , are executed sequentially, and we refer to this execution window as the _action horizon_ . The corresponding execution queue is _Qt_ = [ _at, at_ +1 _, . . . , at_ + _H−_ 1], during which the controller does not query the VLA policy again. 

## **3 VLA-Corrector: A Lightweight Corrective Inference Framework** 

VLA-Corrector addresses the open-loop blind spot of action-chunked VLA policies. During the action horizon, fresh observations are available, but the policy does not use them until the horizon ends. We therefore decouple _action generation_ from _execution monitoring_ : the VLA backbone generates action chunks, while VLA-Corrector monitors whether execution remains on track and intervenes only when drift emerges. We organize the method as follows: **(1) Corrector Training** describes the external latent dynamics corrector; **(2) LVM Detection** introduces online visual deviation detection; **(3) Event-Triggered Truncation** explains how persistent deviations induce adaptive horizons; and **(4) OGG Correction** presents corrective replanning after truncation. 

### **3.1 Training the External Latent Dynamics Corrector** 

VLA-Corrector is trained after a VLA policy has already been obtained. We first fine-tune the VLA backbone on the benchmark training set, then freeze the VLA and use its visual encoder _E_ to extract visual latents from demonstration trajectories. Given a transition ( _ot, at, ot_ + _k_ ), we compute 


where ∆ _Zt_<sup>_∗_</sup> + _k_<sup>isthetargetshort-horizonvisuallatentevolutioninducedbytheexecutedaction.Wethen</sup> train a lightweight external dynamics corrector _Mϕ_ to predict this residual evolution from the current latent state and action: 


Rather than predicting the absolute future latent state, _Mϕ_ instead predicts a residual visual latent evolution, which actively suppresses static scene content and encourages the model to focus on task-relevant dynamics. The training objective combines magnitude matching and directional consistency: 


where _β_ balances residual accuracy and directional alignment. The trainable component is therefore not the VLA policy itself, but a lightweight latent dynamics module trained separately on top of frozen VLA features. This modular design allows the corrector to be retrained or replaced for each benchmark without re-optimizing the expensive VLA backbone. The corrector is trained on benchmark demonstration trajectories because they are easy to obtain and broadly reflect successful task progress. Its goal is not to model all possible futures as a full world model would do, but to learn whether local latent dynamics remain consistent with on-track execution. Demonstrations are suitable for this purpose: although they may contain small teleoperation jitter or local imperfections, they still capture behavior that keeps the task progressing correctly. Since this is a local and low-dimensional prediction task, a lightweight MLP is sufficient in practice; in our experiments, a 40M corrector already provides an effective monitoring and corrective signal, which can be trained at a very low cost. 

5 


**Figure 3 Overview of VLA-Corrector.** Starting from a standard chunked VLA pipeline ( **A** ), we add a **Latent-space Vision Monitor** (LVM) that detects persistent execution drift and triggers an interrupt event ( **B** ). The event truncates stale actions and switches the next replan from normal flow matching to OGG-guided flow matching ( **C** ). OGG uses the expected and observed latent evolution to guide the replan back toward a recoverable trajectory ( **D** ). 

### **3.2 Latent Visual Dynamics for Online Anomaly Detection** 

After training _Mϕ_ , we use it online to monitor whether the current action chunk remains reliable. During execution, **Latent-space Vision Monitor** (LVM) compares the _expected_ latent visual evolution predicted by _Mϕ_ with the _actual_ evolution observed from fresh camera input, detecting deviations before they accumulate into failure. 

**Expected residual dynamics.** At control step _t_ , LVM uses the executed action _at_ and current latent state _Zt_<sup>real</sup> to predict the expected short-horizon latent residual, ∆ _Zt_<sup>exp</sup> + _k_<sup>=</sup><sup>_Mϕ_(</sup><sup>_Z_</sup> _t_<sup>real</sup> _, at_ ), where _k_ is the prediction interval. 

**Online inconsistency score.** During rollout, the latest observation remains available even though the policy is not re-queried. We encode the future observation and compute the actual residual ∆ _Zt_<sup>real</sup> + _k_<sup>=</sup><sup>_Z_</sup> _t_<sup>real</sup> + _k_<sup>_−Z_</sup> _t_<sup>real</sup> . LVM then measures the mismatch between expected and actual latent evolution: 


A larger _Et_ indicates stronger visual dynamics mismatch, providing a continuous signal for later event-triggered truncation. 

### **3.3 Event-Triggered Truncation under Robust Online Monitoring** 

Given the continuous inconsistency score _Et_ , we need to decide when a deviation is persistent enough to justify intervention. Directly thresholding _Et_ can be unstable, since transient visual outliers may cause false triggers. We therefore use a robust event-triggered rule based on dynamic thresholds and persistence checking. Specifically, we maintain a sliding window of recent scores, **E** _W_ = _{Et−w_ +1 _, . . . , Et}_ , and compute its median _Me_ and median absolute deviation, 


We then define two adaptive thresholds, 


where _T_ on confirms persistent deviation and _T_ off provides hysteresis for recovery. An interrupt event is triggered only when _Et > T_ on holds for _p_ consecutive steps; isolated spikes are ignored. 

6 

Once an interrupt is triggered, VLA-Corrector discards the remaining actions in the current queue and queries the policy again under corrective mode. If the controller has executed _h_ actions from the original queue, the realized horizon becomes _H_ adaptive = _h < H_ . Thus, the fixed action horizon is shortened only when sustained visual drift indicates that the current chunk has become stale. The full thresholding state machine is provided in Appendix B.1. 

### **3.4 Online Gradient Guidance for Corrective Inference** 

Truncation stops stale actions, but recovery still depends on the next replan. After an interrupt event, VLA-Corrector applies **Online Gradient Guidance** (OGG) Park et al. (2025) only to the single policy call immediately following the interrupt event, guiding this recovery replan toward a corrective latent direction. 

**Predicted action effect.** At denoising step _τ_ of flow matching, let _A_<sup>_τ_</sup> be the noisy action chunk. The VLA predicts a velocity field _vτ_ = _πθ_ ( _A_<sup>_τ_</sup> _, Zt_<sup>real</sup> _, τ_ ), from which we estimate the clean chunk _A_<sup>ˆ</sup> 0 = _A_<sup>_τ_</sup> _− τvτ_ and take its first action _a_ ˆ _t_ = _A_<sup>ˆ</sup> 0[0]. The corrector then predicts the latent effect of this candidate action: 


**Corrective target.** Let _t − k_ be the last stable step before an interrupt event. We define the expected residual ∆ _Z_ exp = ∆ _Zt_<sup>exp</sup> = _Mϕ_ ( _Zt_<sup>real</sup> _−k_<sup>_, at−k_),whichispredictedby</sup><sup>_Mϕ_fromstep</sup><sup>_t −k_.Theaccumulateddeviationis</sup> ∆ _Z_ dev = ∆ _Zt_<sup>_∗_=</sup><sup>_Z_</sup> _t_<sup>real</sup> _− Zt_<sup>real</sup> _−k_<sup>.Thecorrectivelatentdirectionis</sup> 


This direction preserves the intended local dynamics while compensating for the drift accumulated during open-loop execution. 

**Guided velocity update.** OGG aligns the predicted action effect with ∆ _Z_ corr through 


and injects the resulting gradient into the flow-matching velocity: 


Here, _η_ controls the guidance strength. Since OGG modifies the velocity field rather than directly perturbing action coordinates, it remains compatible with the original flow-matching process and yields smoother corrective replanning. 

## **4 Experiments** 

We evaluate VLA-Corrector on MetaWorld Yu et al. (2020), LIBERO Liu et al. (2023), RoboTwin v2.0 Chen et al. (2025b), and a real AgileX PiPER robot, using _π_ 0 _._ 5 Intelligence et al. (2025) as the main backbone and SmolVLA Shukor et al. (2025)/X-VLA Zheng et al. (2025) for cross-architecture evaluation. The experiments cover four aspects: **(1) Performance and policy-call efficiency** , evaluating success rate and success-per-call across benchmarks and horizons; **(2) Mechanism analysis** , examining LVM detection, truncation timing, and OGG recovery; **(3) Real-world transfer** , testing the method on physical robot manipulation; and **(4) Ablations** , analyzing component necessity and sensitivity. Detailed protocols, metrics, and compute resources are provided in Appendix C.1. 

### **4.1 Main Results** 

**Cross-Architecture Evaluation on MetaWorld.** VLA-Corrector consistently improves all three VLA backbones on MetaWorld, with larger gains on harder tasks. As shown in Table 1, the average success rate improves by 15.65 points for _π_ 0 _._ 5, 4.75 points for SmolVLA, and 4.05 points for X-VLA. The strongest gain appears on the Very Hard split of _π_ 0 _._ 5, increasing success from 41.0% to 65.0%. 

7 

**Table 1 Cross-architecture generalization on MetaWorld.** Success rate (%, _↑_ ) across difficulty splits. Green arrows show absolute improvements over the corresponding baseline. 

|**Backbone**|**Method**|**Easy**_↑_|**Medium**_↑_|**Hard**_↑_|**Very Hard**_↑_|**Avg.**_↑_|
|---|---|---|---|---|---|---|
||Baseline|70.5|45.0|38.3|41.0|48.70|
|_π_0_._5|**+ VLA-Corrector**|**83.2** _↑_12_._7|**61.7** _↑_16_._7|**47.5** _↑_9_._2|**65.0** _↑_24_._0|**64.35** _↑_15_._65|
|SmolVLA|Baseline|81.3|53.6|51.7|61.0|61.90|
||**+ VLA-Corrector**|**83.4** _↑_2_._1|**56.0** _↑_2_._4|**64.2** _↑_12_._5|**63.0** _↑_2_._0|**66.65** _↑_4_._75|
|XVLA|Baseline|72.5|46.4|48.3|55.0|55.55|
|-|**+ VLA-Corrector**|**74.4** _↑_1_._9|**50.0** _↑_3_._6|**50.0** _↑_1_._7|**64.0** _↑_9_._0|**59.60** _↑_4_._05|


**Table 2 RoboTwin v2.0 evaluation.** Success rate (%, _↑_ ), average policy calls per episode ( _↓_ ), and per-step wallclock latency ( _↓_ ). The benchmark covers all 50 tasks in clean and randomized configurations, with 50 episodes per task/configuration (5,000 episodes per method); the same frozen _π_ 0 _._ 5 backbone is used throughout. 

|**Method**|**Clean**_↑_|**Random**_↑_<br>**Overal**|**l (95% CI)**_↑_|**Calls/ep.**_↓_|**ms/step**_↓_|
|---|---|---|---|---|---|
|Baseline _H_ = 50|68.2|62.6<br>65.4|[64.1,66.7]|5.74|8.10|
|Baseline _H_ = 30 (latency-matched)|72.0|66.8<br>69.4|[68.1,70.7]|9.41|9.98|
|**VLA-Corrector** _H_ = 50|**76.0**|**70.2**<br>**73.1 **|**[71.9,74.3]**|6.88|10.02|


**Table 3 Sample efficiency on LIBERO.** Success rate (%, _↑_ ). Green arrows compare VLA-Corrector against the few-shot fine-tuned baseline. 

|**Mod**|**el**|**Object**_↑_|**Spatial**_↑_|**Goal**_↑_|**Long**_↑_|**Avg.**_↑_|
|---|---|---|---|---|---|---|
|_π_0_._5|(Full Fine-tuned)|99.4|98.2|97.8|92.4|96.95|
|_π_0_._5|(Few-shot Fine-tuned)|97.8|95.4|96.2|86.6|94.00|
|_π_0_._5|(Few-shot) **+ VLA-Corrector**|**99.8** _↑_2_._0|**100.0** _↑_4_._6|**98.0** _↑_1_._8|**93.4** _↑_6_._8|**97.80** _↑_3_._80|


**RoboTwin Evaluation.** On the broader RoboTwin v2.0 benchmark, VLA-Corrector improves overall success from 65.4% to 73.1% over the original _H_ = 50 baseline and from 69.4% to 73.1% over the latency-matched _H_ = 30 baseline. The gain over the matched baseline is 3.7 points while per-step latency remains nearly identical (10.02 vs. 9.98 ms); VLA-Corrector also uses 27% fewer policy calls than the matched baseline (6.88 vs. 9.41 calls/episode). The improvement persists in both clean and randomized configurations. A more comprehensive and detailed analysis can be found in Appendix D.6. 

**Sample Efficiency on LIBERO.** We further evaluate whether VLA-Corrector can compensate for limited task-specific data. Table 3 compares a fully fine-tuned _π_ 0 _._ 5 model with a few-shot fine-tuned counterpart on LIBERO. Starting from the publicly released LeRobot Cadene et al. (2026) few-shot checkpoint `pi05_libero_base` , VLA-Corrector improves the average success rate from 94.00% to 97.80%, even surpassing the fully fine-tuned baseline (96.95%). 

These results suggest that few-shot fine-tuning can already learn much of the normal task trajectories, but may lack coverage of drifted states and their recovery behaviors. Instead of improving recovery by exposing the backbone to more rare failure cases during training, VLA-Corrector makes recovery easier at inference time by interrupting error accumulation early and guiding corrective replanning, thereby alleviating the dependence on additional post-training data for robust recovery. 

**Performance–Efficiency Trade-off.** VLA-Corrector improves success-per-call efficiency across action horizons rather than simply querying the policy more often. As shown in Figure 4, the largest success-per-call gains reach 29.9% for _π_ 0 _._ 5, 45.3% for SmolVLA, and 39.1% for X-VLA. For example, on SmolVLA with horizon 10, success improves from 61.90% to 73.00% while policy calls decrease from 19.27 to 15.64. This suggests that VLA-Corrector makes each policy query more useful by interrupting stale chunks and guiding recovery. Full results are provided in Appendix D.3. 

8 


**Figure 4 Performance–efficiency analysis on** _π_ 0 _._ 5 **. Left** : performance–efficiency trade-off across action horizons. **Right** : success-per-call efficiency. VLA-Corrector improves success rate across action horizons and yields consistent efficiency gains. 

### **4.2 Mechanism Analysis** 

In this section, we will analyze the mechanisms behind VLA-Corrector from three perspectives: **1) LVM detection** , whether LVM provides a useful and well-timed drift signal; and **2) OGG correction** , whether OGG improves recovery after an interrupt event; **3) controlled recovery** , whether the full framework improves recovery in a controlled failure case. 


**Figure 5 LVM detection analysis. Left** : distribution of the inconsistency score _Et_ , where successful episodes concentrate at low values and failed episodes show a heavier high-score tail. **Right** : interrupt frequency, where failed episodes trigger more interrupt events than successful ones. 

**LVM Detection.** LVM provides an informative drift signal. As shown in Figure 5, successful episodes concentrate at low _Et_ , while failed episodes show a heavier high-score tail and trigger more interrupt events. This indicates that _Et_ captures failure-prone visual dynamics mismatch. 


**Figure 6 Task-phase analysis of LVM-triggered truncation.** We manually divide MetaWorld trajectories into _critical_ and _non-critical_ phases. **Left** : representative trajectories show that truncation is triggered much more frequently during critical phases. **Right** : 83.7% of truncations occur in critical phases, while only 16.3% occur in non-critical phases. 

LVM also intervenes at meaningful moments. We manually divide MetaWorld trajectories into _critical_ phases, such as precise grasping and alignment, and _non-critical_ phases, such as tolerant transport after a 

9 


**Figure 7 Controlled recovery case.** Given the same initial state and detected grasping error, the monitored baseline continues the original chunk and fails ( **top** ), while VLA-Corrector truncates stale actions, replans with OGG, and completes the task ( **bottom** ). 

stable grasp. Figure 6 shows that 83.7% of truncations occur in critical phases. This result verifies the core adaptive-horizon intuition of VLA-Corrector: it does not simply shorten the horizon everywhere, but instead preserves long-horizon efficiency in tolerant phases and restores short-horizon precision when the task enters error-sensitive phases. 

**OGG Correction.** We isolate OGG by comparing standard re-inference and OGG-guided re-inference after the same interrupt-triggered truncation. Recovery is counted when _Et < T_ off within the next 10 steps. As shown in Fig. 8, OGG improves recovery across all difficulty levels, with an average gain of 0.23. This indicates that, after truncation stops stale actions, OGG-guided re-inference further improves the quality of the recovery replan compared to standard re-inference. 


**Controlled Recovery Case.** Figure 7 shows a representative LIBERO episode where both methods start from the same initial state and encounter the same grasping error when approaching the cup handle. In the top row, the baseline rollout is only monitored by LVM for error alignment without truncating the remaining actions; after the deviation is detected, it continues executing the original action chunk, leading to an unstable grasp, cup drop, and task failure. In 

**Figure 8 Post-interrupt recovery.** OGG-guided inference consistently outperforms standard inference. 

the bottom row, VLA-Corrector detects the same deviation but actively truncates the stale actions and triggers corrective replanning, allowing the robot to recover a stable grasp and place the cup at the target location. This controlled comparison highlights the overall effectiveness of VLA-Corrector under the same initial condition and the same detected execution error. 

### **4.3 Real-World Evaluation** 

**Setup.** We evaluate VLA-Corrector on an AgileX PiPER 6-DoF arm using _π_ 0 _._ 5 as the backbone. The benchmark includes three task groups, each with three tasks and 20 trials: **1) Pick-and-place** tests standard manipulation, **2) Alignment** tests precision-sensitive placement or insertion, and **3) Disturbance recovery** tests recovery when objects or targets are manually shifted during execution. Full task definitions, protocols, failure analysis, and representative demonstrations are provided in Appendix E. 

**Results.** Table 4 shows that VLA-Corrector improves all three task groups, increasing average success from 55.6% to 73.3%. The gain is modest on pick-and-place (+8.3), larger on alignment (+16.6), and largest on disturbance recovery (+28.3). This trend matches the intended role of VLA-Corrector: it preserves standard execution performance, improves precision-sensitive manipulation, and is most beneficial when online disturbances make the remaining action chunk outdated. 

10 

**Table 4 Real-world evaluation on AgileX PiPER.** Success rate (%, _↑_ ) over three task groups. Each group contains three tasks with 20 trials per task. We report 95% binomial confidence intervals. 

|**Method**|**Pick-place**_↑_|**Alignment**_↑_|**Disturbance**_↑_|**Avg.**_↑_|
|---|---|---|---|---|
|_π_0_._5 Baseline|70.0 _±_ 11.6|56.7 _±_ 12.5|40.0 _±_ 12.4|55.6 _±_ 7.3|
|**+ VLA-Corrector**|**78.3** _±_ **10.4** _↑_8_._3|**73.3** _±_ **11.2** _↑_16_._6|**68.3** _±_ **11.8** _↑_28_._3|**73.3** _±_ **6.5** _↑_17_._7|


### **4.4 Ablation Studies** 

**Table 5 Component ablation on MetaWorld.** Success rate (%, _↑_ ). Green arrows indicate average improvement over the baseline. 

|**Variant**|**Easy**_↑_|**Medium**_↑_|**Hard**_↑_|**Very Hard**_↑_|**Avg.**_↑_|
|---|---|---|---|---|---|
|Baseline (Open-loop)|70.5|45.0|38.3|41.0|48.70|
|+ Truncation Only|81.8|53.6|**50.0**|56.0|60.35 _↑_11_._65|
|**+ Truncation + OGG**|**83.2**|**61.7**|47.5|**65.0**|**64.35** _↑_15_._65|


We ablate VLA-Corrector on _π_ 0 _._ 5 in MetaWorld, focusing on **(1) components** : necessity of truncation and OGG; **(2) detector design** : decoupling monitoring from backbone fine-tuning; and **(3) sensitivity** , with detailed results in Appendix D.1. 

**Component effects.** Table 5 shows that truncation alone raises average success from 48.70% to 60.35%, confirming the importance of stopping stale actions. Adding OGG further improves the average to 64.35%, showing that post-truncation recovery also benefits from guided re-inference. 

**Detector design and sensitivity.** We compare our decoupled LVM with an internal detection head trained during _π_ 0 _._ 5 fine-tuning using the same auxiliary latent-residual prediction target. The internal head takes the final-layer hidden state of the last token, combines it with the executed action, and predicts the same task as the external LVM. As shown in Appendix D.1, decoupled LVM improves average success from 49.55% to 64.35%, suggesting that separating monitoring from action generation preserves the backbone representation and yields a cleaner drift signal. The same appendix also shows that moderate guidance strength and a 40M LVM are sufficient; overly strong guidance or larger monitors provide little additional benefit. 

## **5 Conclusion** 

This paper studies the open-loop blind spot in action-chunked VLA policies, where fixed horizons improve policy-call efficiency but allow stale actions to accumulate errors. VLA-Corrector addresses this issue with a lightweight detect-and-correct layer that monitors latent visual dynamics, truncates stale actions when drift persists, and guides the next inference toward recovery. Our results show that small inference-time modules can provide targeted robustness gains without retraining the VLA backbone. Rather than replacing action chunking, VLA-Corrector makes it adaptive: long-horizon execution is preserved when reliable, while corrective replanning is invoked when the current chunk should no longer be trusted. 

## **References** 

> Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, and 1 others. 2025. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ . 

> Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, and 1 others. 2024. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ . 

> Remi Cadene, Simon Aliberts, Francesco Capuano, Michel Aractingi, Adil Zouitine, Pepijn Kooijmans, Jade Choghari, Martino Russi, Caroline Pascal, Steven Palma, and 1 others. 2026. Lerobot: An open-source library for end-to-end robot learning. _arXiv preprint arXiv:2602.22818_ . 

11 

- Jun Cen, Siteng Huang, Yuqian Yuan, Kehan Li, Hangjie Yuan, Chaohui Yu, Yuming Jiang, Jiayan Guo, Xin Li, Hao Luo, and 1 others. 2025. Rynnvla-002: A unified vision-language-action and world model. _arXiv preprint arXiv:2511.17502_ . 

- Hao Chen, Jiaming Liu, Chenyang Gu, Zhuoyang Liu, Renrui Zhang, Xiaoqi Li, Xiao He, Yandong Guo, Chi-Wing Fu, Shanghang Zhang, and 1 others. 2025a. Fast-in-slow: A dual-system foundation model unifying fast manipulation within slow reasoning. _arXiv preprint arXiv:2506.01953_ . 

- Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, and 1 others. 2025b. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ . 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. 2025. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704. 

- Danny Driess, Jost Tobias Springenberg, Brian Ichter, Lili Yu, Adrian Li-Bell, Karl Pertsch, Allen Z Ren, Homer Walke, Quan Vuong, Lucy Xiaoyang Shi, and 1 others. 2025. Knowledge insulating vision-language-action models: Train fast, run fast, generalize better. _arXiv preprint arXiv:2505.23705_ . 

- Yichao Fu, Xuewei Wang, Yuandong Tian, and Jiawei Zhao. 2025. Deep think with confidence. _arXiv preprint arXiv:2508.15260_ . 

- George Jiayuan Gao, Tianyu Li, and Nadia Figueroa. 2025. Out-of-distribution recovery with object-centric keypoint inverse policy for visuomotor imitation learning. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 9816–9828. IEEE. 

- Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, and 1 others. 2024. Octo: An open-source generalist robot policy. In _Robotics: Science and Systems (RSS)_ . 

- Ruiyu Gou. 2024. _Learning temporal action chunking for motor control_ . Ph.D. thesis, University of British Columbia. 

- Zhi Hou, Tianyi Zhang, Yuwen Xiong, Haonan Duan, Hengjun Pu, Ronglei Tong, Chengyang Zhao, Xizhou Zhu, Yu Qiao, Jifeng Dai, and 1 others. 2025. Dita: Scaling diffusion transformer for generalist vision-language-action policy. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 7686–7697. 

- Zheyuan Hu, Robyn Wu, Naveen Enock, Jasmine Li, Riya Kadakia, Zackory Erickson, and Aviral Kumar. 2025. Rac: Robot learning for long-horizon tasks by scaling recovery and correction. _arXiv preprint arXiv:2509.07953_ . 

- Nils Ingelhag, Jesper Munkeby, Michael C Welle, Marco Moletta, and Danica Kragic. 2025. Real-time operator takeover for visuomotor diffusion policy training. _arXiv preprint arXiv:2502.02308_ . 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, and 1 others. 2025. _\_ pi {_ 0.5 _}_ : a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ . 

- Arnav Kumar Jain, Vibhakar Mohta, Subin Kim, Atiksh Bhardwaj, Juntao Ren, Yunhai Feng, Sanjiban Choudhury, and Gokul Swamy. 2025. A smooth sea never made a skilled sailor: Robust imitation via learning to search. _arXiv preprint arXiv:2506.05294_ . 

- Sunshine Jiang, Xiaolin Fang, Nicholas Roy, Tomás Lozano-Pérez, Leslie Pack Kaelbling, and Siddharth Ancha. 2025a. Streaming flow policy: Simplifying diffusion/flow-matching policies by treating action trajectories as flow trajectories. _arXiv preprint arXiv:2505.21851_ . 

- Yuming Jiang, Siteng Huang, Shengke Xue, Yaxi Zhao, Jun Cen, Sicong Leng, Kehan Li, Jiayan Guo, Kexiang Wang, Mingxiu Chen, and 1 others. 2025b. Rynnvla-001: Using human demonstrations to improve robot manipulation. _arXiv preprint arXiv:2509.15212_ . 

- Dong Jing, Gang Wang, Jiaqi Liu, Weiliang Tang, Zelong Sun, Yunchao Yao, Zhenyu Wei, Yunhui Liu, Zhiwu Lu, and Mingyu Ding. 2025. Mixture of horizons in action chunking. _arXiv preprint arXiv:2511.19433_ . 

- Sarosh Khan and Ellie Tanimura. 2025. Test-time stochasticity estimation for adaptive action chunk selection. 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. 2025. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ . 

12 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, and 1 others. 2024. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ . 

- Wei Li, Renshan Zhang, Rui Shao, Jie He, and Liqiang Nie. 2025. Cogvla: Cognition-aligned vision-language-action model via instruction-driven routing & sparsification. _arXiv preprint arXiv:2508.21046_ . 

- Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, and 1 others. 2023. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ . 

- Yuanchang Liang, Xiaobo Wang, Kai Wang, Shuo Wang, Xiaojiang Peng, Haoyu Chen, David Kim Huat Chua, and Prahlad Vadakkepat. 2026. Adaptive action chunking at inference-time for vision-language-action models. _arXiv preprint arXiv:2604.04161_ . 

- Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. 2022. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ . 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. 2023. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791. 

- Isabella Liu, An-Chieh Cheng, Rui Yan, Geng Chen, Ri-Zhao Qiu, Xueyan Zou, Sha Yi, Hongxu Yin, Xiaolong Wang, and Sifei Liu. 2026. Long-horizon manipulation via trace-conditioned vla planning. _arXiv preprint arXiv:2604.21924_ . 

- Yuejiang Liu, Jubayer Ibn Hamid, Annie Xie, Yoonho Lee, Maximilian Du, and Chelsea Finn. 2024. Bidirectional decoding: Improving action chunking via guided test-time sampling. _arXiv preprint arXiv:2408.17355_ . 

- Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. 2024. A survey on vision-language-action models for embodied ai. _arXiv preprint arXiv:2405.14093_ . 

- Cyrus Neary, Omar G Younis, Artur Kuramshin, Ozgur Aslan, and Glen Berseth. 2025. Improving pre-trained vision-language-action policies with model-based search. _arXiv preprint arXiv:2508.12211_ . 

- Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, and 1 others. 2024. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE. 

- Minho Park, Kinam Kim, Junha Hyung, Hyojin Jang, Hoiyeong Jin, Jooyeol Yun, Hojoon Lee, and Jaegul Choo. 2025. Acg: Action coherence guidance for flow-based vla models. _arXiv preprint arXiv:2510.22201_ . 

- Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. 2025. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ . 

- Kohei Sendai, Maxime Alvarez, Tatsuya Matsushima, Yutaka Matsuo, and Yusuke Iwasawa. 2025. Leave no observation behind: Real-time correction for vla action chunks. _arXiv preprint arXiv:2509.23224_ . 

- Archit Sharma, Ahmed M Ahmed, Rehaan Ahmad, and Chelsea Finn. 2023. Self-improving robots: End-to-end autonomous visuomotor reinforcement learning. _arXiv preprint arXiv:2303.01488_ . 

- Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, and 1 others. 2025. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ . 

- Junhyuk So, Chiwoong Lee, Shinyoung Lee, Jungseul Ok, and Eunhyeok Park. 2025. Improving generative behavior cloning via self-guidance and adaptive chunking. _arXiv preprint arXiv:2510.12392_ . 

- Haoming Song, Delin Qu, Yuanqi Yao, Qizhi Chen, Qi Lv, Yiwen Tang, Modi Shi, Guanghui Ren, Maoqing Yao, Bin Zhao, and 1 others. 2025a. Hume: Introducing system-2 thinking in visual-language-action model. _arXiv preprint arXiv:2505.21432_ . 

- Wenxuan Song, Jiayi Chen, Pengxiang Ding, Han Zhao, Wei Zhao, Zhide Zhong, Zongyuan Ge, Jun Ma, and Haoang Li. 2025b. Accelerating vision-language-action model integrated with action chunking via parallel decoding. _arXiv preprint arXiv:2503.02310_ . 

- Zhanyi Sun and Shuran Song. 2025. Latent policy barrier: Learning robust visuomotor policies by staying in-distribution. _arXiv preprint arXiv:2508.05941_ . 

13 

- Libo Wang. 2025. Sigma: The key for vision-language-action models toward telepathic alignment. _arXiv preprint arXiv:2512.00783_ . 

- Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, and 1 others. 2026a. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. _Proceedings of the AAAI conference on artificial intelligence_ , 40(22):18638–18646. 

- Zhendong Wang, Zhaoshuo Li, Ajay Mandlekar, Zhenjia Xu, Jiaojiao Fan, Yashraj Narang, Linxi Fan, Yuke Zhu, Yogesh Balaji, Mingyuan Zhou, and 1 others. 2024. One-step diffusion policy: Fast visuomotor policies via diffusion distillation. _arXiv preprint arXiv:2410.21257_ . 

- Zihua Wang, Zhitao Lin, Ruibo Li, Yu Zhang, Xu Yang, Siya Mi, and Xiu-Shen Wei. 2026b. Open-loop planning, closed-loop verification: Speculative verification for vla. _arXiv preprint arXiv:2604.02965_ . 

- Junjie Wen, Yichen Zhu, Minjie Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Xiaoyu Liu, Chaomin Shen, Yaxin Peng, and Feifei Feng. 2025. Diffusionvla: Scaling robot foundation models via unified diffusion and autoregression. In _Forty-second International Conference on Machine Learning_ . 

- Pengyuan Wu, Pingrui Zhang, Zhigang Wang, Dong Wang, Bin Zhao, and Xuelong Li. 2026a. Closed-loop action chunks with dynamic corrections for training-free diffusion policy. _arXiv preprint arXiv:2603.01953_ . 

- Zhichao Wu, Junyin Ye, Zhilong Zhang, Yihao Sun, Haoxin Lin, Jiaheng Luo, Haoxiang Ren, Lei Yuan, and Yang Yu. 2026b. Speedup patch: Learning a plug-and-play policy to accelerate embodied manipulation. _arXiv preprint arXiv:2603.20658_ . 

- Changhua Xu, Jie Lu, Junyu Xuan, and En Yu. 2026. Vgas: Value-guided action-chunk selection for few-shot vision-language-action adaptation. _arXiv preprint arXiv:2602.07399_ . 

- Shaoqing Xu, Fang Li, Zhixiang Duan, Yifan Yang, Tianshi Xie, and Zhi-Xin Yang. n.d. Vla-in-the-loop: Online policy correction with world models for robust robotic grasping. OpenReview manuscript. ICLR 2026 submission. 

- Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. 2020. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pages 1094–1100. PMLR. 

- Thomas TCK Zhang, Daniel Pfrommer, Chaoyi Pan, Nikolai Matni, and Max Simchowitz. 2026. Action chunking and data augmentation yield exponential improvements in behavior cloning for continuous spaces. In _The Fourteenth International Conference on Learning Representations_ . 

- Chen Zhao, Zhuoran Wang, Haoyang Li, Shifeng Bao, Guanlin Li, Youhe Feng, Yang Li, Jie Tang, and Jing Zhang. 2026. Action draft and verify: A self-verifying framework for vision-language-action model. _arXiv preprint arXiv:2603.18091_ . 

- Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, and 1 others. 2025. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713. 

- Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. 2023a. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ . 

- Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. 2023b. Learning fine-grained bimanual manipulation with low-cost hardware. In _Robotics: Science and Systems (RSS)_ . 

- Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, and 1 others. 2025. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ . 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, and 1 others. 2023. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR. 

14 

# Appendix 

## **A Related Work** 

### **A.1 Generative VLA Models** 

Embodied intelligence is shifting from task-specific policies toward unified Vision-Language-Action (VLA) foundation models. Representative works have shown that combining large-scale vision-language pretraining with robot control can substantially improve cross-task generalization, semantic understanding, and crossplatform transfer O’Neill et al. (2024); Black et al. (2024); Zitkovich et al. (2023); Kim et al. (2024); Ghosh et al. (2024); Li et al. (2023); Bjorck et al. (2025); Pertsch et al. (2025); Song et al. (2025b). On the action modeling side, modern VLA and general robot policies often adopt generative frameworks to model high-dimensional, continuous, and multi-modal action distributions: diffusion models generate actions through iterative denoising Chi et al. (2025); Wen et al. (2025); Black et al. (2024); Chen et al. (2025a); Li et al. (2025); Zhao et al. (2025); Hou et al. (2025); Kim et al. (2025); Song et al. (2025a), while flow matching directly learns velocity fields along continuous trajectories. These approaches typically offer stronger action expressivity, but they also incur higher policy-call costWang et al. (2024). Consequently, reducing control latency without sacrificing generation quality has become a central challenge in deploying VLA models. 

### **A.2 Action Chunk and Horizon Trade-off** 

To alleviate the tension between high-frequency control and expensive policy inference, **action chunk** has been widely adopted in continuous control. The core idea is to predict multiple future actions in a single inference call and then execute them sequentially with a downstream controller Chi et al. (2025); Zhao et al. (2023b); Black et al. (2024); Shukor et al. (2025); Bjorck et al. (2025); Wang (2025); Driess et al. (2025). This design effectively amortizes policy-call frequency and improves temporal smoothness, but it also reduces the use of fresh observations within a fixed action horizon. A longer horizon further lowers inference frequency and maintains action consistency, but weakens responsiveness to environmental changes; a shorter horizon more closely resembles strict closed-loop control and often provides better local recovery, yet requires much more frequent policy calls Jing et al. (2025); Zhang et al. (2026); Liu et al. (2024); Khan and Tanimura (2025); So et al. (2025); Fu et al. (2025); Zhao et al. (2026); Liu et al. (2026). Most existing approaches therefore seek a compromise under a static horizon, whereas our work focuses on an event-triggered dynamic horizon: the system retains the efficiency of long chunks during stable phases and truncates them on demand to recover closed-loop responsiveness during local failures. 

### **A.3 Failure Recovery in Visuomotor Policies** 

Long-horizon visuomotor control commonly suffers from compounding errors and covariate shift: once execution drifts away from the training distribution, the policy often cannot recover on its own. Existing approaches can be broadly divided into two categories. One line of work expands the training distribution through additional interaction, human intervention, or recovery data collection, and then updates the policy accordingly Sharma et al. (2023); Ingelhag et al. (2025); Hu et al. (2025); Neary et al. (2025). Another line explicitly introduces recovery policies, search mechanisms, or distributional constraints to pull the system back to a safe region once it departs from the expert manifold Gao et al. (2025); Sun and Song (2025); Jain et al. (2025); Liang et al. (2026); Gou (2024); Wu et al. (2026b); Xu et al. (n.d.). These works collectively show that explicit recovery mechanisms can substantially improve the robustness of visuomotor policies; however, they typically rely on additional recovery data, separately trained recovery modules, or joint optimization tailored to a specific policy backbone. 

15 

## **B Method Details** 

### **B.1 Details of Event-Triggered Truncation** 

This section provides the full event-triggered truncation rule used by LVM. Given the online inconsistency score _Et_ , the monitor maintains a sliding window of recent scores, 


Let 


We use the median absolute deviation because it is less sensitive to transient score spikes than the mean and variance. Based on this robust statistic, we define asymmetric on/off thresholds, 


The higher threshold _T_ on is used to confirm abnormal deviation, while the lower threshold _T_ off provides hysteresis and prevents rapid oscillation between normal and abnormal states. 

To avoid triggering on isolated spikes, we maintain a persistence counter: 


An interrupt event is triggered when 


where _p_ is the patience parameter. After an interrupt event, the remaining actions in the current execution queue are discarded, the counter is reset, and the next policy query is performed under corrective mode. If _h_ actions have already been executed from the current queue, the realized action horizon is 


In this way, the system preserves long-horizon execution during stable phases, while shortening the horizon when persistent visual drift indicates that the current action chunk is no longer reliable. 

### **B.2 LVM and OGG Runtime Parameters** 

**LVM monitoring parameters.** The Latent-space Vision Monitor uses a robust online thresholding state machine. We maintain a sliding window of recent inconsistency scores with window size 15. The dynamic thresholds are computed using _λ_ on = 3 _._ 0 and _λ_ off = 2 _._ 0. An interrupt event is triggered only when the inconsistency score exceeds the activation threshold for _p_ = 5 consecutive steps. Similarly, the monitor requires 5 consecutive safe steps for reset. To avoid repeated triggers immediately after intervention, we use an interrupt cooldown of 10 steps. 

**OGG parameters.** Online Gradient Guidance is invoked only for the single policy query immediately following an interrupt-triggered truncation. When an interrupt event occurs, the remaining action queue is cleared, the next replan is marked as a guidance replan, and OGG is applied during that next action-chunk generation. Subsequent policy calls return to standard inference unless another interrupt event is detected. The guidance strength is controlled by _η_ . In our experiments, we use _η_ = 1 as the default setting for _π_ 0 _._ 5, SmolVLA, and X-VLA. The sensitivity of performance to _η_ is analyzed in Table 7. 

## **C Training and Implementation Details** 

### **C.1 Benchmarks and Evaluation Protocol** 

We evaluate VLA-Corrector on three simulation benchmarks: MetaWorld Yu et al. (2020), LIBERO Liu et al. (2023), and RoboTwin v2.0. MetaWorld tests contact-rich manipulation robustness across difficulty 

16 

splits, LIBERO evaluates language-conditioned long-horizon task execution, and RoboTwin broadens the evaluation to 50 tasks under clean and randomized scene configurations. We use _π_ 0 _._ 5 Intelligence et al. (2025) as the main backbone, and further test SmolVLA Shukor et al. (2025) and X-VLA Zheng et al. (2025) for cross-architecture evaluation. We report task success rate as the primary metric, together with policy calls, success-per-call efficiency, and post-interrupt recovery rate when applicable. 

For MetaWorld, tasks are grouped into four difficulty splits: _Easy_ , _Medium_ , _Hard_ , and _Very Hard_ . All online evaluations are conducted task by task within each split, and we report the average success rate over tasks in the corresponding split. Unless otherwise specified, each task is evaluated with 20 episodes. For the corrector data-scaling study, we use a fixed episode-level split before subsampling the training data: 10% of episodes are held out for validation, 10% are held out for testing, and the remaining episodes form the training pool. We then subsample this training pool according to the training ratio _r_ . In the multi-seed data-scaling analysis, we use split seeds _{_ 42 _,_ 123 _,_ 999 _}_ and require at least 20 episodes in the train, validation, and test partitions. All simulation experiments are conducted on 8 NVIDIA A100-SXM4-40GB GPUs. 

For RoboTwin v2.0, we evaluate all 50 tasks in both the clean and randomized configurations, using 50 episodes per task and configuration. Initial conditions and evaluation seeds are paired across methods, yielding 5,000 episodes per method. We compare the original fixed-horizon baseline ( _H_ = 50), a latency-matched baseline ( _H_ = 30), and VLA-Corrector ( _H_ = 50), all with the same frozen _π_ 0 _._ 5 backbone. We report clean, randomized, and pooled success rates with 95% Wilson confidence intervals, together with average policy calls per episode and measured wall-clock latency per environment step. 

### **C.2 External Corrector Architecture** 

The external corrector _Mϕ_ is implemented as a residual MLP for short-horizon latent dynamics prediction. We first map the executed action through a linear embedding layer, concatenate the resulting action feature with the current visual latent _Zt_<sup>real</sup> , and feed the combined representation into a stack of residual MLP blocks. The network predicts the short-horizon latent residual rather than the absolute future latent state. In all experiments, we use a four-layer hidden configuration with width [2048 _,_ 2048 _,_ 2048 _,_ 2048]. The exact number of parameters varies slightly across benchmarks and VLA backbones because both the action dimensionality and the visual latent dimensionality differ across settings. Overall, the correctors used in our experiments contain approximately 38–42M parameters, and we refer to this external module as a lightweight _∼_ 40M MLP corrector. 

### **C.3 Corrector Training** 

The corrector is trained after the VLA backbone has been fine-tuned on the benchmark training set. We freeze the VLA backbone and use its visual encoder to extract latent representations from demonstration trajectories. The corrector is then trained on these frozen latents to predict the short-horizon visual latent residual induced by the executed action. We use AdamW as the optimizer with learning rate 3 _×_ 10<sup>_−_4</sup> and weight decay 10<sup>_−_4</sup> . The learning rate is scheduled by cosine annealing with _η_ min = 0 _._ 01 _×_ lr. We train for 30 epochs with early stopping patience 5. For the ratio-sweep training runs, we use batch size 128 and evaluation batch size 256. For the deployed h1-k10 correctors used in evaluation, we use batch size 512, train for 30 epochs, and optimize a cosine-based training loss. The number of optimization steps depends on the number of training samples under each data ratio: 


where _N_ train is the number of training samples and _B_ is the batch size. 

### **C.4 Compute Resources** 

All simulation experiments are conducted on NVIDIA A100-SXM4-40GB GPUs. The main training and evaluation jobs are run on a server with 8 such GPUs. Corrector training is lightweight compared with VLA backbone fine-tuning because it only optimizes the external MLP on frozen VLA features. During online evaluation, LVM monitoring adds only a forward pass through the external corrector, while OGG introduces additional gradient computation only for the single recovery query following an interrupt event. 

17 

**Table 6 Coupled vs. decoupled detection.** Success rate (%, _↑_ ). Both variants use OGG; only the detector design differs. 

|**Detector**|**Easy**_↑_|**Medium**_↑_|**Hard**_↑_|**Very Hard**_↑_|**Avg.**_↑_|
|---|---|---|---|---|---|
|Internal Head + OGG|65.2|46.0|36.5|50.5|49.55|
|**Decoupled LVM + OGG**|**83.2** _↑_18_._0|**61.7** _↑_15_._7|**47.5** _↑_11_._0|**65.0** _↑_14_._5|**64.35** _↑_14_._80|


**Table 7 Ablation on OGG guidance strength** _η_ **.** Success rate (%, _↑_ ) on MetaWorld. The highlighted row is the default setting. 

|**Guidance Strength**|**Easy**_↑_|**Medium**_↑_|**Hard**_↑_|**Very Hard**_↑_|**Avg.**_↑_|
|---|---|---|---|---|---|
|_η_ = 0_._1|82.7|56.8|45.2|**66.0**|62.68|
|_η_ = 1 **(default)**|**83.2** _↑_0_._5|**61.7** _↑_4_._9|**47.5** _↑_2_._3|65.0 _↓_1_._0|**64.35** _↑_1_._67|
|_η_ = 10|82.5|56.8|38.3|65.0|60.65 _↓_3_._70|
|_η_ = 100|80.9|55.0|36.7|63.0|58.90 _↓_5_._45|


**Table 8 Ablation on LVM capacity.** Success rate (%, _↑_ ) on MetaWorld. The highlighted row is the default setting. 

|**Monitor Capacity**|**Easy**_↑_|**Medium**_↑_|**Hard**_↑_|**Very Hard**_↑_|**Avg.**_↑_|
|---|---|---|---|---|---|
|LVM-10M|78.5|52.4|39.8|55.6|56.58|
|**LVM-40M (default)**|**83.2** _↑_4_._7|61.7 _↑_9_._3|47.5 _↑_7_._7|**65.0** _↑_9_._4|**64.35** _↑_7_._77|
|LVM-160M|82.8 _↓_0_._4|**62.1** _↑_0_._4|**48.0** _↑_0_._5|64.2 _↓_0_._8|64.28 _↓_0_._07|


## **D Additional Experimental Results** 

### **D.1 Ablation Sensitivity** 

We provide additional ablations on detector design, OGG guidance strength, and LVM capacity. All experiments are conducted with _π_ 0 _._ 5 on MetaWorld. 

For the internal detector, we fine-tune _π_ 0 _._ 5 with an additional auxiliary loss that matches the prediction task of LVM: the final-layer hidden state of the last token is combined with the executed action and used to predict the same short-horizon latent residual. Table 6 shows that this coupled design performs much worse than the decoupled external LVM. This suggests that joint auxiliary detection training can interfere with the action-generation representation, whereas the external LVM preserves the backbone policy and provides a cleaner monitoring signal. 

Tables 7 and 8 show that VLA-Corrector does not require overly strong guidance or excessively large monitors. _η_ = 1 achieves the best average success, while larger guidance weakens performance on harder tasks. Increasing LVM capacity from 10M to 40M substantially improves success, but 160M provides almost no additional average gain. 

### **D.2 Cross-Domain Corrector Generalization** 

To examine whether the external corrector learns a transferable latent-dynamics signal rather than only memorizing benchmark-specific trajectories, we evaluate cross-domain corrector transfer on MetaWorld. We use the same _π_ 0 _._ 5 MetaWorld baseline policy and compare two VLA-Corrector variants: one using a corrector trained on LIBERO demonstrations, and the other using a corrector trained on MetaWorld demonstrations. Both are evaluated on MetaWorld under the same protocol. 

Table 9 shows that the LIBERO-trained corrector still improves the MetaWorld baseline from 48.7% to 51.8%, suggesting that the learned latent-dynamics consistency signal has limited but non-trivial cross-domain transfer. However, the MetaWorld-trained corrector achieves a much larger gain, improving the average success rate to 58.7%. This indicates that while the corrector can capture partially transferable notions of on-track visual dynamics, domain-matched demonstrations remain important for accurate deviation detection and effective corrective guidance. 

18 

**Table 9 Cross-domain corrector generalization on MetaWorld.** Success rate (%, _↑_ ) of the same _π_ 0 _._ 5 MetaWorld baseline equipped with correctors trained from different demonstration domains. Green arrows indicate absolute improvement over the baseline. 

|**Method**|**Easy**_↑_|**Medium**_↑_|**Hard**_↑_|**Very Hard**_↑_|**Avg.**_↑_|
|---|---|---|---|---|---|
|_π_0_._5 Baseline|70.5|45.0|38.3|41.0|48.7|
|+ LIBERO-trained Corrector|70.9 _↑_0_._4|50.5 _↑_5_._5|40.7 _↑_2_._4|45.0 _↑_4_._0|51.8 _↑_3_._1|
|+ MetaWorld-trained Corrector|**74.1** _↑_3_._6|**53.8** _↑_8_._8|**52.9** _↑_14_._6|**54.0** _↑_13_._0|**58.7** _↑_10_._0|


**Table 10 Performance–efficiency trade-off across VLA backbones and action horizons.** Success rate, average policy calls per episode, and relative efficiency gains are reported. The arrows ( _↑_ / _↓_ ) in the header explicitly indicate whether a higher or lower metric is optimal. 

|**Model**|**Horizon**|**Baseli**|**ne**|**Ours (LVM**|**+OGG)**|**I**|**mproveme**|**nts**|
|---|---|---|---|---|---|---|---|---|
|||**Succ** (%)_↑_|**Calls** _↓_|**Succ** (%)_↑_|**Calls** _↓_|∆**Succ** (%)_↑_|∆**Calls** _↓_|**Eff. Gain** (%)_↑_|
||10|64.50|20.41|**72.40**|**17.64**|_↑_7_._90|_↓_2_._77|**+29.9%**|
||20|61.40|10.77|**69.10**|**9.95**|_↑_7_._70|_↓_0_._82|**+21.8%**|
|_π_0_._5|30|56.10|7.97|**63.50**|**7.92**|_↑_7_._40|_↓_0_._05|**+13.9%**|
||40|54.45|5.96|**60.80**|6.04|_↑_6_._35|_↑_0_._08|**+10.2%**|
||50|48.72|5.15|**58.70**|**4.98**|_↑_9_._98|_↓_0_._17|**+24.6%**|
||10|61.90|19.27|**73.00**|**15.64**|_↑_11_._10|_↓_3_._63|**+45.3%**|
||20|58.90|11.32|**68.90**|**9.50**|_↑_10_._00|_↓_1_._82|**+39.4%**|
|**SmolVLA**|30|58.10|7.90|**65.20**|**7.60**|_↑_7_._10|_↓_0_._30|**+16.6%**|
||40|56.80|5.64|**67.20**|**5.13**|_↑_10_._40|_↓_0_._51|**+30.0%**|
||50|54.20|4.86|**62.90**|**4.68**|_↑_8_._70|_↓_0_._18|**+20.6%**|
||4|68.50|46.58|**72.00**|**35.20**|_↑_3_._50|_↓_11_._38|**+39.1%**|
||8|67.80|23.18|**72.10**|**19.48**|_↑_4_._30|_↓_3_._70|**+26.5%**|
|**X-VLA**|16|55.50|13.71|**60.90**|13.92|_↑_5_._40|_↑_0_._21|**+8.1%**|
||24|52.90|10.13|**59.20**|**9.92**|_↑_6_._30|_↓_0_._21|**+14.3%**|
||32|44.00|8.61|**54.40**|**8.34**|_↑_10_._40|_↓_0_._27|**+27.6%**|


∆ **Succ** : absolute success-rate improvement. ∆ **Calls** : absolute change in policy calls per episode. **Eff. Gain** : relative improvement in success-per-call over the baseline. 

### **D.3 Full Performance–Efficiency Results** 

Table 10 provides the full performance–efficiency results across all evaluated VLA backbones and action horizons. These results complement the main-text analysis by reporting the exact success rates, average policy calls, and success-per-call efficiency gains for each setting. Overall, VLA-Corrector consistently improves task success while maintaining or reducing the number of policy calls in most cases, leading to positive success-per-call efficiency gains across all backbones. The gains are especially pronounced at longer horizons, where the open-loop blind spot is larger and stale actions are more likely to accumulate errors before the next policy query. 

### **D.4 Data Efficiency of Corrector Training** 

**Analysis.** To quantify how much data is needed to train the external corrector, we subsample the MetaWorld demonstration set with training ratios _r ∈{_ 0 _._ 2 _,_ 0 _._ 4 _,_ 0 _._ 6 _,_ 0 _._ 8 _,_ 1 _._ 0 _}_ and evaluate the resulting VLA-Corrector on the same task suite. As shown in Table 11, the corrector is already effective with limited data: using only 20% of the demonstrations yields a 48.32% macro-average success rate. Performance improves as more data is added and reaches 52.20% at _r_ = 0 _._ 6, after which the gain becomes marginal. This suggests that the corrector does not require exhaustive coverage of all task variations; once it has seen enough examples of on-track local dynamics, it can provide a useful signal for detecting deviations and guiding recovery. 

The trend also shows that the corrector benefits from additional data, but with diminishing returns. Increasing 

19 

**Table 11 Data efficiency of corrector training on MetaWorld.** We compare the original open-loop baseline at NAS=50 with VLA-Corrector trained using different fractions of demonstration trajectories. The results show that moderate corrector data already surpasses the baseline and that performance largely saturates around 60% of the training set. Bold indicates the best result in each column. 

|**Method / Training Ratio**|**Easy**|**Medium**|**Hard**|**Very Hard**|**Macro Avg.**|
|---|---|---|---|---|---|
|Baseline (NAS=50)|70.54|45.00|38.33|41.00|48.72|
|VLA-Corrector (_r_ = 0_._2)|71.07|49.55|36.67|36.00|48.32|
|VLA-Corrector (_r_ = 0_._4)|70.36|45.91|38.33|42.00|49.15|
|VLA-Corrector (_r_ = 0_._6)|70.89|52.73|39.17|**46.00**|52.20|
|VLA-Corrector (_r_ = 0_._8)|71.07|53.64|38.33|**46.00**|52.26|
|VLA-Corrector (_r_ = 1_._0)|**73.21**|**55.91**|**44.17**|44.00|**54.32**|


**Table 12 LVM timing during deployment on MetaWorld.** We measure 500 held-out observations after removing 20 warm-up observations. “Full LVM computation” is all work done by the monitor; “wait added to control loop” is the part that the controller actually waits for. 

|**Component**|**Mean (ms)**|**p95 (ms)**|
|---|---|---|
|Preprocessing|1.79|2.06|
|Frozen vision encoder|21.31|21.46|
|40M residual MLP|2.79|2.93|
|Mismatch + threshold|0.91|1.08|
|**Full LVM computation**|**26.96**|**27.57**|
|**Wait added to control loop**|**0.008**|**0.009**|


**Table 13 OGG timing during deployment on an NVIDIA A100-SXM4-40GB.** We compare 200 matched ordinary/OGG pairs after 20 warm-up runs. The random state is restored for each pair, the order is balanced, and CUDA timing is synchronized; every OGG call uses two guidance steps. 

|**Call**|**Mean latency**|
|---|---|
|Ordinary|232.490 ms|
|OGG|243.223 ms|
|**Increment per trigger**|**10.733 ms**|
|95% CI|[10.430, 11.053] ms|


the training ratio from 0 _._ 2 to 0 _._ 6 brings a clear improvement, while increasing it further from 0 _._ 6 to 0 _._ 8 changes the macro average only slightly. Full-data training still achieves the best overall result, especially on the Hard split, but the relatively strong performance at moderate data ratios supports our design motivation: VLA-Corrector learns a local consistency signal rather than a full policy or heavy world model, making it data-efficient to train. On the Very Hard split, the small fluctuation across higher ratios indicates that extremely challenging contact-rich tasks are influenced by factors beyond corrector data scale alone, such as disturbance severity and backbone recovery capability. 

### **D.5 Inference-Time Cost and Control Delay** 

The monitor runs in parallel with the robot’s current action. We therefore report two different times: (1) the time needed to complete the monitor’s computation, and (2) the part of that time that actually makes the controller wait. We also measure the extra time used by the OGG recovery call. All measurements use synchronized CUDA timing. The LVM measurements are listed in Table 12, the OGG measurements in Table 13, and the physical-control check in Table 14. 

As shown in Table 12, the monitor performs 26 _._ 96 ms of computation on average and 27 _._ 57 ms at p95. Because this work runs while the robot is executing, it adds only 0 _._ 008 ms of average waiting time (0 _._ 009 ms at p95) to the control loop. Thus, the computation is real, but almost all of it is hidden by parallel execution; the 0 _._ 008 ms number is only the extra wait, not the total monitor cost. 

20 

**Table 14 Timing check on AgileX PiPER.** PiPER executes 10 actions per second, so the controller has 100 ms for each action. 

|**Quantity**|**Result**|
|---|---|
|Control period|100 ms/action (10 Hz)|
|Full LVM|26.96 ms mean / 27.57 ms p95|
|p95 remaining margin|72.43 ms|
|Deadline misses|0 / 500|
|Wait added to control loop|0.008 ms mean|


**Table 15 Asynchronous deployment-path accounting.** Intrinsic computation is measured with CUDA synchronization; exposed wait is the delay visible to the control loop after asynchronous pipelining. OGG is applied only to the single recovery query following an interrupt. 

|**Quantity**|**Measured result**|
|---|---|
|Full LVM intrinsic computation|26.96 ms mean / 27.57 ms p95|
|Exposed asynchronous control-path wait|0.008 ms mean / 0.009 ms p95|
|Ordinary policy call|232.490 ms|
|OGG-guided policy call|243.223 ms|
|Increment on the recovery call|10.733 ms/trigger, 95% CI [10.430, 11.053] ms|
|PiPER control period|100 ms/action (10 Hz)|
|Observed deadline misses|0/500|


**Table 16 RTC context under the 10 Hz control-period model.** The response intervals are obtained from the ordinary/guided call latencies and the persistence rule ( _p_ = 5); they clarify the difference between periodic scheduling and failure-aware truncation. 

|**Configuration**<br>**Requery rule**|**Calls/step**|**Relative calls**|**Response under the timing model**|
|---|---|---|---|
|LVM-gated truncation<br>_H_ = 50; extra replan after persistent mismatch|0.0379|1.0_×_|Stale suffix stopped at _≈_400 ms|
|Reviewer-style RTC<br>Periodic, _s_ = 3|0.333|8.8_×_|Replacement at 297–597 ms|
|Call-matched RTC<br>Periodic, _s ≈_26_._4|0.0379|1.0_×_|Replacement at _≈_297–2,937 ms|


Table 13 shows that an ordinary policy call takes 232 _._ 490 ms, while an OGG-guided call takes 243 _._ 223 ms. OGG therefore adds 10 _._ 733 ms only when it is used for recovery after an interrupt; it does not slow down ordinary policy calls. 

**Discussion.** Table 14 summarizes the physical check. MetaWorld is evaluated without a real-time clock, but PiPER must complete one action every 100 ms. The monitor’s p95 computation time is 27.57 ms, leaving 72.43 ms in each control period, and none of the 500 measured steps missed its deadline. The monitor therefore remains responsive in the physical setup: its full computation is accounted for, while only 0.008 ms of average waiting is added to the controller. OGG adds 10.733 ms only on the occasional recovery call. 

### **D.6 Asynchronous and RTC Comparisons** 

Because Real-Time Chunking (RTC) periodically refreshes action chunks while the previous chunk is executing, it overlaps with the asynchronous execution path of VLA-Corrector and is a natural comparison point. The two mechanisms nevertheless address different parts of the control problem: RTC schedules the next policy query, whereas VLA-Corrector uses the observed-vs. predicted visual-dynamics mismatch to produce an explicit error signal, stop stale actions, and guide the recovery replan. We therefore report both the deployment-path timing and a direct overlapped-execution success comparison. Table 15 collects the asynchronous timing measurements, Table 16 gives the RTC timing context, and Table 17 reports the direct overlapped-execution experiment. 

Table 15 makes the deployment claim precise: asynchronous execution does not remove the LVM’s 26.96 ms of intrinsic computation, but only 0.008 ms of mean waiting time is exposed on the control path. The OGG increment is similarly localized to the recovery call, rather than being charged to every action step. 

21 

**Table 17 Direct overlapped-execution comparison on MetaWorld-50.** All methods use the same frozen _π_ 0 _._ 5, horizon _H_ = 50, asynchronous execution path, and 50 paired episodes per task (2,500 episodes per method). The RTC baseline periodically alternates _s_ = 26. The three _Et_ -gated variants share the same detector and truncation settings and differ only in the triggered replan; the random direction is scaled to the mean OGG guidance norm. 

|**Method**|**Triggered guidance**|**Success (95% CI)**|**Calls/100 steps**|
|---|---|---|---|
|RTC, _s_ = 26|None|61.3 [59.4, 63.2]|3.85|
|_Et_-gated replan|None|62.4 [60.5, 64.3]|4.08|
|_Et_-gated random|Random|61.9 [60.0, 63.8]|4.12|
|_Et_**-gated OGG**|**OGG**|**67.1 [65.3, 68.9]**|**3.88**|


Table 16 gives an analytical timing context rather than a hardware benchmark. It shows that periodic RTC can deliver a newer ordinary chunk, but does not itself provide an explicit failure signal or a recovery-directed target. At the same call budget, RTC must distribute policy calls uniformly, whereas LVM-gated execution allocates the additional replan after an observed persistent mismatch. The direct experiment below tests whether this distinction remains visible in task success when all methods use overlapped execution. 

For clarity, all main-text experiments and the previously reported VLA-Corrector results use `rtc_config=None` : RTC itself is disabled in those experiments. This setting does not make LVM monitoring synchronous; the deployment-path measurements above still run the monitor asynchronously while the current action executes. To compare against RTC directly, we additionally run the experiment in Table 17 with asynchronous inference enabled for every method and with an RTC baseline included only for this comparison. For context, the RTC analysis reports 97 ms for inference-time RTC versus 76 ms for vanilla _π_ 0 _._ 5 on an RTX 4090, because prefix inpainting requires gradient computation; its training-time variant removes that inference operation only through a separately trained prefix-conditioned _π_ 0 _._ 6 checkpoint. These context figures are kept separate from the direct overlapped-execution experiment and the A100 deployment-path measurements above. 

As shown in Table 17, the additional experiment directly evaluates VLA-Corrector under overlapped execution rather than inferring its behavior from sequential timing. At comparable policy-call rates, _Et_ -gated OGG reaches 67.1% success versus 61.3% for periodic RTC, an improvement of 5.8 points (paired 95% CI [+4.4, +7.2], McNemar _p <_ 10<sup>_−_13</sup> ). Thus, the advantage persists when policy inference is overlapped with action execution and is not explained by a higher call frequency. The matched-norm random control reaches 61.9%, which is 5.2 points below _Et_ -gated OGG (95% CI [+3.8, +6.6], _p <_ 10<sup>_−_11</sup> ), and does not improve over the ordinary _Et_ -gated replan (61.9% vs. 62.4%). These results isolate the contribution of the recovery direction: the gain comes from using the LVM-derived error signal to guide OGG toward a corrective target, rather than from arbitrary perturbation or simply requesting another policy chunk. 

## **E Real-World Details** 

### **E.1 Robot Platform and Task Suite** 

**Robot platform.** All real-world experiments are conducted on an **AgileX PiPER** 6-DoF robotic arm. We use _π_ 0 _._ 5 as the action-chunked VLA baseline and evaluate VLA-Corrector on top of the same fine-tuned backbone. Both methods share the same RGB camera observation, language instruction, action horizon, and initial task conditions. Each task is evaluated with 20 trials per method. A trial is counted as successful if the robot completes the specified task without human reset after execution starts. 

**Task design.** We design three groups of real-world tasks with increasing difficulty. The first group evaluates standard pick-and-place behavior, where the original action chunk often remains valid. The second group evaluates precise alignment, where small accumulated errors can cause missed placement, collision, or failed insertion. The third group introduces online human disturbances during precision-sensitive phases, directly testing whether VLA-Corrector can recover when the remaining action chunk becomes stale. Table 18 summarizes the task definitions. 

22 

**Table 18 Real-world task suite on AgileX PiPER.** The benchmark contains three task groups and nine tasks in total. The disturbance group reuses manipulation skills from the first two groups but introduces online pose changes during precision-sensitive phases. 

|**Group**|**Task**|**Description**|
|---|---|---|
|Pick-and-place|Cube-to-region<br>Cube-to-drawer-top|Pick up a cube and place it inside a marked target region.<br>Pick up a cube and place it on top of a small drawer<br>platform.|
||Object-to-container|Pick up a cube and place it into a specific bowl.|
||Corner placement|Place a cube precisely at the upper-left corner of the|
|Alignment|Square-hole insertion<br>Edge alignment|drawer top.<br>Align and insert a small cube into a square hole or slot.<br>Align an object with a narrow marked edge or target<br>strip.|
||Moving-object grasp|Move the target object when the gripper is about to grasp|
|Disturbance recovery|Moving-placement target<br>Moving-insertion target|it.<br>Move the placement region after the object is grasped.<br>Move the square hole or alignment target before insertion.|


### **E.2 Per-Task Real-World Results** 

Table 19 reports per-task success rates. The gains are modest on pick-and-place tasks because the baseline can often complete the task when the object and target remain static. The gains become larger on alignment tasks, where small pose errors are less tolerable. The largest improvement appears in disturbance recovery tasks, where the current action chunk often becomes stale after the object or target is manually moved. 

**Table 19 Per-task real-world success rates.** Success rate (%, _↑_ ) over 20 trials per task on the AgileX PiPER 6-DoF arm. Group and overall rows report mean _±_ standard deviation across tasks. Green arrows indicate absolute improvement over the _π_ 0 _._ 5 baseline. 

|**Group**|**Task**|_π_0_._5 **Baseline**_↑_|**+ VLA-Corrector**_↑_|
|---|---|---|---|
||Cube-to-region|75.0|**85.0** _↑_10_._0|
|Pikdl|Cube-to-drawer-top|70.0|**80.0** _↑_10_._0|
|c-an-pace|Object-to-container|65.0|**70.0** _↑_5_._0|
||**Group Avg.**|**70.0** _±_ **5.0**|**78.3** _±_ **7.6** _↑_8_._3|
||Corner placement|60.0|**75.0** _↑_15_._0|
|Alinment|Square-hole insertion|50.0|**70.0** _↑_20_._0|
|g|Edge alignment|60.0|**75.0** _↑_15_._0|
||**Group Avg.**|**56.7** _±_ **5.8**|**73.3** _±_ **2.9** _↑_16_._6|
||Moving-object grasp|45.0|**75.0** _↑_30_._0|
|Ditrbnrr|Moving-placement target|40.0|**70.0** _↑_30_._0|
|suace ecovey|Moving-insertion target|35.0|**60.0** _↑_25_._0|
||**Group Avg.**|**40.0** _±_ **5.0**|**68.3** _±_ **7.6** _↑_28_._3|
|**Overall**|**Avg. across 9 tasks**|**55.6** _±_ **13.8**|**73.3** _±_ **7.1** _↑_17_._7|


### **E.3 Real-World Protocol and Task Details** 

**Evaluation protocol.** For each real-world task, we collect 10–30 human teleoperated demonstration trajectories and use them to fine-tune the _π_ 0 _._ 5 backbone for that task. The same fine-tuned backbone is then used by both the baseline and VLA-Corrector, so the comparison isolates the effect of the inference-time correction module. For each task and each method, we run 20 evaluation trials. Initial object poses are randomized within a small predefined region while keeping the task feasible for the 6-DoF PiPER arm. 

23 

**Pick-and-place tasks.** The pick-and-place group includes placing a cube into a marked region, placing a cube on top of a drawer platform, and placing a small object into a bowl. These tasks are relatively tolerant to small pose errors, so the original action chunk often remains usable. VLA-Corrector mainly helps when occasional drift occurs during approach or release. 

**Alignment tasks.** The alignment group increases the precision requirement. In corner placement, the robot must place a cube at a specific corner of the drawer top. In square-hole insertion, the cube must be aligned with a square opening before insertion. In edge alignment, the robot must align an object with a narrow visual marker or edge. These tasks are more sensitive to accumulated error, making stale action execution more harmful near the final contact. 

**Disturbance recovery tasks.** The disturbance group directly evaluates the open-loop blind spot. We introduce manual perturbations at predefined task phases rather than at fixed time steps. For moving-object grasp, the target object is shifted when the gripper is close to grasping it. For moving-placement target, the robot first grasps the object normally, and the target platform or placement region is shifted before release. For moving-insertion target, the square hole or alignment target is shifted when the robot is about to align or insert. The disturbance is applied once per trial, kept within the camera view, and constrained to a physically recoverable range. The same timing rule and disturbance range are used for both the baseline and VLA-Corrector. 

### **E.4 Observed Real-World Failure Modes** 

Despite the improvements, VLA-Corrector still fails in several real-world cases. If the target object or fixture is moved beyond the reachable region, or if the disturbance happens after the gripper has entered an unfavorable pose, the robot may no longer have enough workspace or time to recover through a single corrective replan. In tight alignment tasks, a 6-DoF arm without force feedback may fail due to contact geometry, friction, or small height errors even when the visual target is corrected. We also observe failures caused by visual ambiguity, such as partial occlusion by the gripper or poor contrast between the object and the target region. Finally, OGG still depends on the frozen _π_ 0 _._ 5 action prior: it can bias the next generation toward a better corrective direction, but it cannot create a recovery behavior that the backbone policy cannot represent. 

### **E.5 Real-World Demonstration Examples** 

We provide representative real-world demonstration examples mainly for the disturbance recovery tasks. In these cases, the object or target fixture is manually shifted during execution, allowing us to visualize the practical robustness of VLA-Corrector under human-induced disturbances. 


**Figure 9 Demo: Moving-object grasp.** The robot picks up the cube and places it into the white bowl, while a human manually changes the cube’s position during the process. 

24 


**Figure 10 Demo: Moving-placement target.** The robot picks up the cube and places it into the blue bowl, while a human manually changes the bowl’s position during the process. 


**Figure 11 Demo: Moving-insertion target.** The robot picks up the cube and places it at the upper-left corner of the drawer top, while a human manually changes the drawer’s position during the process. 

25 

