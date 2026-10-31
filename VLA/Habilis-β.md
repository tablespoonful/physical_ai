---
title: "Habilis-$β$: A Fast-Motion and Long-Lasting On-Device Vision-Language-Action Model"
date: "2026-02-21"
authors: "Tommoro Robotics;  :; Jesoon Kang; Taegeon Park; Jisu An; Soo Min Kimm"
url: https://arxiv.org/abs/2602.18813
pdf: https://arxiv.org/pdf/2602.18813
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.18813)** / [論文ページ](https://arxiv.org/abs/2602.18813)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



# **Habilis-** **_β_ : A Fast-Motion and Long-Lasting On-Device VisionLanguage-Action Model** 

Tommoro Robotics<sup>*</sup> 

```
https://tommoro.ai
```


**Figure 1: Habilis-** **_β_ Overview.** _(Left)_ **Training Pipeline:** The model is trained in three stages to achieve FastMotion and Long-Lasting capabilities. Stage 1 learns a robust, task-agnostic interaction prior via play data pretraining. Stage 2 post-trains on cyclic task demonstrations, utilizing Spatially Aware Downsampling (ESPADA) to compress casual free-space motions. Stage 3 distills the multi-step flow matching action expert into an efficient rectified flow model. _(Right)_ **Inference Pipeline:** To enable On-Device operation, a pre-trained VLM prefix fuses multimodal observations to condition the distilled action expert. The reduced inference cost is reinvested into High-Frequency Control, using shorter action chunks for rapid closed-loop reactivity. Finally, Classifier-Free Guidance (CFG) acts as a deployment-time knob to dynamically balance instruction adherence and learned interaction priors. 

**Abstract** We introduce Habilis- _β_ , a fast-motion and long-lasting on-device vision-language-action (VLA) model designed for real-world deployment. Current VLA evaluation remains largely confined to single-trial success rates under curated resets, which fails to capture the fast-motion and long-lasting capabilities essential for practical operation. To address this, we introduce the Productivity–Reliability Plane (PRP), which evaluates performance through Tasks per Hour (TPH) and Mean Time Between Intervention (MTBI) under a continuous-run protocol that demands both high-speed execution and sustained robustness. Habilis- _β_ achieves high-performance by integrating language-free pre-training on large-scale play data for robust interaction priors with post-training on cyclic demonstrations that capture state drift across consecutive task iterations. The system further employs ESPADA for phase-adaptive motion shaping to accelerate free-space transit, utilizes rectified-flow distillation to enable high-frequency control on edge devices, and incorporates classifier-free guidance (CFG) as a deployment-time knob to dynamically balance instruction adherence and learned interaction priors. In 1-hour continuous-run evaluations, Habilis- _β_ achieves strong performance under the PRP metrics, compared to _π_ 0 _._ 5 in both simulation and real-world environments. In simulation, Habilis- _β_ achieves 572 _._ 6 TPH and 39 _._ 2s MTBI (vs. 120 _._ 5 TPH and 30 _._ 5s for _π_ 0 _._ 5), while in a real-world humanoid logistics workflow it achieves 124 TPH and 137 _._ 4s MTBI (vs. 19 TPH and 46 _._ 1s for _π_ 0 _._ 5). Finally, Habilis- _β_ achieves the highest reported performance on the standard RoboTwin 2.0 leaderboard across representative tasks, validating its effectiveness in complex manipulation scenarios. 

## **1. Introduction** 

Vision-language-action (VLA) models [26, 3, 29, 44, 17, 59, 5] have advanced rapidly. Motivated by generalization in language and vision [46], recent work asks whether a similar generalization can be achieved in physical robot control. 

However, several obstacles still prevent general VLA systems from working reliably in the real world. First, many VLA systems move slowly [28, 18, 2]. They produce conservative, temporally dense actions that underuse fast 

> *See _Contributions and Acknowledgements_ for the full author list. For correspondence: `research@tommoro.ai` . 

© 2026 Tommoro Robotics. All rights reserved. 


free-space motion and show limited closed-loop reactivity, reducing throughput. Second, evaluation protocols still emphasize single-attempt trials under curated reset conditions [31]. This hides what happens in extended operation, where tasks repeat, initial states drift, and small execution errors accumulate until the system fails and requires intervention. Third, end-to-end latency remains a practical bottleneck [51, 6, 26]. Large VLA stacks can require heavy computing and may rely on networked components, adding delay and reducing predictability when a fast reaction is necessary. These limitations matter for generality, and they are especially costly in industrial settings where productivity, reliability, and operating cost are hard constraints. 

Accordingly, **Habilis-** **_β_** focuses on three deployment requirements: Fast-Motion, Long-Lasting, and On-Device. _Fast-Motion_ means maintaining high speed when precision is not critical, while switching to careful control near contact and during fine manipulation. _Long-Lasting_ means sustaining performance under repeated execution as initial states drift and small errors accumulate, with minimal human intervention or resets. _On-Device_ means running the perception-to-action loop locally on an edge device while preserving Fast-Motion and Long-Lasting performance, enabling predictable latency and reduced dependence on network or service variability under tight compute and power budgets. 

Meeting these requirements requires evaluation protocols that reflect repeated execution and real-time constraints. We revisit a common assumption in VLA training and evaluation: episodes are treated as independent, singletrial trajectories [31]. Under this “non-cyclic” regime, the success rate measures how often a model completes a task once from a carefully prepared initial state. However, we further argue that the single-trial success rate is not a sufficient deployment metric. It collapses the speed–accuracy trade-off and qualitatively different failure modes into one number, and it is insensitive to long-run degradation and intervention frequency. In deployment, failures come in many forms (e.g., timeouts, aborts) and they do not have a single clean definition. What matters operationally is whether the run can continue without external help [7]. 

We therefore propose a Productivity-Reliability Plane (PRP) where we employ Tasks per Hour (TPH) and Mean Time Between Intervention (MTBI) as our metrics. TPH measures sustained throughput under realistic operating constraints and serves as a primary measure of Fast-Motion capability. MTBI measures the average operating time between events that require external intervention and serves as a primary measure of Long-Lasting capability. To make long-duration evaluation well-defined, we treat any such event that requires model-external assistance (e.g., reset or recovery) as an _intervention_ . Considering both metrics jointly exposes the productivity-reliability tradeoff that dominates real deployments and distinguishes systems that otherwise look similar under the single-trial success rate. 

These deployment metrics also reshape what we want from data. In our early experiments, we find that models trained under standard episode segmentation can achieve a high single-trial success rate, yet deteriorate rapidly under repetition [32, 19]. A plausible driver is distribution shift: repeated execution induces drifting initial states and recovery situations that non-cyclic data rarely contain [53, 48]. We therefore leverage _play_ data and _cyclic_ task data as complementary mechanisms to broaden coverage and better match the state distribution encountered in continuous operation. 

We leverage play data [41, 42] as a scalable way to learn a broad interaction prior grounded in physical behavior. Play data refers to unstructured, unsegmented demonstration data collected from a human teleoperating a robot without any explicit task labels or goal specifications. Because it is relatively cheap to collect, we use it for language-unconditioned pre-training to learn a task-agnostic motion prior. 

We then post-train on task demonstrations using a “cyclic” dataset formulation that better matches the state distribution encountered in continuous operation. Concretely, instead of segmenting data as success-then-stop episodes, cyclic data records continuous trajectories where the robot repeatedly executes the same instruction across many cycles, linking the end of one success to the start of the next. Training on cyclic data encourages the model to learn recovery behavior and to retain performance over long runs, which are central to deployment. 

The same mismatch appears on the productivity side. When evaluation focuses on one-shot success, datasets and policies have little incentive to learn when fast-motion is appropriate, learned behaviors often remain temporally dense and overly conservative. We address this by shaping demonstrations so that free-space motion can be executed quickly, while contact-rich phases remain precise and reactive. Specifically, we apply ESPADA [28], our recent method that compresses redundant action sequences and prioritizes high-impact interactions. This reduces 

2 


unnecessary temporal density in the learned behavior and mitigates slow motion, improving throughput without sacrificing task success. 

Additionally, to achieve end-to-end responsiveness, we combine rectified flow distillation [37] with high-frequency control. Distillation reduces the inference cost and frees the latency budget under on-device or local-machine constraints. Rather than spending this budget solely on a single slow pass, we allocate it to more frequent reinference. This improves closed-loop reactivity and enables rapid adaptation to unexpected events while keeping latency predictable. 

Finally, we optionally apply classifier-free guidance (CFG) [23], interpolating between instruction-conditioned and instruction-free predictions. In practice, increasing guidance strengthens instruction adherence, shifting the policy toward more proactive behavior and often increasing execution speed and behavioral aggressiveness. CFG therefore serves as a convenient deployment-time knob for navigating the speed–reliability trade-off. 

For the evaluation, we build a continuous-run environment in both simulation and the real world. Instead of singletrial episodes, we run policies in long-horizon autonomous cycles where tasks repeat back-to-back, initial states drift, and occasional interventions become necessary. This makes the productivity–reliability trade-off explicit and yields stable measurements of TPH, MTBI, and success rate under sustained operation. 

In this continuous-run regime, Habilis- _β_ improves all three deployment metrics. Overall, Habilis- _β_ substantially outperforms the strongest baseline _π_ 0 _._ 5 in both simulation and the real world under long-horizon operation. In simulation, Habilis- _β_ achieves 572 _._ 6 TPH, 39 _._ 2s MTBI, and a 78 _._ 5% success rate, compared to _π_ 0 _._ 5 at 120 _._ 5 TPH, 30 _._ 5s MTBI, and a 47 _._ 8% success rate. In the real world, under a 1-hour continuous-run protocol, Habilis- _β_ achieves 124 TPH, 137 _._ 4s MTBI, and an 82 _._ 7% success rate, compared to _π_ 0 _._ 5 at 19 TPH, 46 _._ 1s MTBI, and a 19 _._ 6% success rate. 

We further benchmark on the RoboTwin 2.0 [9] suite using its standard single-trial evaluation protocol and report results on three representative tasks: `Dump Bin Bigbin` , `Place Dual Shoes` , and `Stack Bowls Three` . Habilis- _β_ records the best reported performance on these RoboTwin 2.0 tasks at the time of release. 

## **2. Problem Setup and Metrics** 

We evaluate deployment readiness along two operational axes: _productivity_ (how much work it completes per unit time under the same deployment protocol) and _reliability_ (how long the system can run without human intervention). 

### **2.1. Deployment Protocol: Continuous-Run Evaluation** 

We use a continuous-run protocol that mirrors production operation. The robot repeatedly executes a fixed task cycle for a fixed wall-clock duration, while the environment is re-initialized only when necessary. For each model/setting, we run the system for a fixed duration _T_ (typically _T_ = 3600 seconds). During the run, the robot continuously attempts task cycles. We record interventions whenever the execution cannot proceed without external human assistance, after which the run resumes (e.g., via reset/restart). In our experiments, interventions are defined by two mechanisms. First, a _timeout rule_ : if the robot fails to complete a task cycle within a task-specific time limit, we record an intervention and reset. Second, an _abort_ (real-world only): any operator-initiated termination (e.g., an E-stop) that requires external recovery is recorded as an intervention.<sup>1</sup> This protocol emphasizes performance retention under repetition and makes compounding drift, stuck accumulation, and recovery failures measurable. 

> 1We use task-specific timeouts to avoid unfairly penalizing tasks with inherently different nominal cycle times. Exact timeouts are reported per task in Section 4. 

3 


### **2.2. Productivity Metric: Tasks per Hour (TPH)** 

Productivity is measured as TPH, i.e., the number of completed tasks per hour under the same continuous-run protocol. Let _N_ succ be the number of successful task completions during the run. Our primary reporting uses wall-clock normalization: 


### **2.3. Reliability Metric: Mean Time Between Intervention (MTBI)** 

Reliability is quantified by Mean Time Between Intervention (MTBI), defined as the average continuous run time between required external interventions. Let _K_ be the number of interventions during a continuous run of duration _T_ seconds. We compute 


Under the standard one-hour protocol ( _T_ = 3600), this simplifies to MTBI = 3600 _/K_ . 

### **2.4. Productivity-Reliability Plane** 

To evaluate productivity and reliability jointly, we visualize each model/setting as a point on a 2D plane: 

- x-axis: TPH (productivity), 

- y-axis: MTBI (reliability). 

We refer to this visualization as the Productivity-Reliability Plane (PRP). A method improves deployment readiness if it achieves higher MTBI and higher TPH under the same continuous-run protocol. 

## **3. Habilis-** _β_ **: Fast-Motion, Long-Lasting, On-Device VLA** 

### **3.1. System Overview** 


**Figure 2: Model Architecture.** Habilis- _β_ ’s prefix-suffix architecture uses a pre-trained VLM prefix to process multimodal inputs, conditioning a suffix action expert that generates continuous action chunks. 

Figure 2 illustrates the model architecture of Habilis- _β_ . The model takes multi-view observations and a high-level instruction as input and outputs H-step continuous action chunk ( _at, · · · , at_ + _H−_ 1) [57, 39]. Each camera view is embedded by a ViT [14] encoder, and the resulting visual tokens are fused by a pre-trained VLM backbone. 

4 


An action expert then consumes the proprioception _st_ and generates the action chunk. At inference time, we optionally apply CFG [23] by mixing an instruction-conditioned prediction and an instruction-masked prediction. 

### **3.2. Model Architecture and Training** 

### _3.2.1. Flow Matching Action Expert_ 

The action expert in Habilis- _β_ uses flow matching [35] to model continuous action chunks. At an environment time _t_ , an observation is given by _ot_ = ( _It, st, ℓ_ ) where _It_ is a set of images, _st_ is a state, and _ℓ_ is an instruction. We define a linear interpolation (also called noisy action) _xτ_ between a demonstrated action chunk _a ∈_ R<sup>_H×d_</sup> and Gaussian noise _ϵ ∈_ R<sup>_H×d_</sup> with action horizon _H_ and action dimension _d_ : 


Here, _τ_ is denoising time sampled from a Beta distribution Beta(1 _._ 5 _,_ 1) affinely mapped to [0 _._ 001 _,_ 1 _._ 0]. The model predicts a velocity field _vθ_ ( _o, xτ , τ_ ) over the entire horizon _H_ where _θ_ denotes the learnable parameters. It is trained to match the target velocity field _uτ_ . We follow a prefix-suffix design [4] where a pre-trained VLM processes multimodal inputs and the action expert is a suffix-conditioned decoder. To enable controllable guidance at inference, we apply language-only unconditioning during training. The model is trained using flow matching regression with a CFG-style masking mechanism: 


where _D_ is the dataset of trajectory-language pairs. Here, _o_ ˜ refers to the observation with stochastically masked instructions for learning unconditional dynamics. This learning objective encourages the model to separate instructioninduced bias (task selection) from the low-level action prior that supports stable interaction. 

### _3.2.2. Rectified Flow Distillation_ 

To minimize inference latency without degrading generation quality, we adopt the **Rectified Flow** [37, 38, 58, 15]. Specifically, we leverage its distillation [21] capability to compress a multi( _≥_ 10)-step teacher model to a twostep student model. In our implementation, the teacher model _vθ_ ( _ot, xτ , τ_ ) with a learnable parameter _θ_ is a transformer that generates an action chunk through iterative ODE integration from noise to data. The student model _vϕ_ ( _ot, xτ , τ_ ) with a learnable parameter _ϕ_ is trained to bypass this iterative process by learning to predict the teacher’s terminal target-induced velocity. The distillation objective is defined as: 


_ot_ is the multimodal observation context at environment time _t_ , processed by the VLM prefix. _xτ_ is an intermediate state at denoising step _τ_ along the teacher’s ODE trajectory. _x_ 1 is the final action chunk reached by the teacher’s full integration.<sup>_<u>x</u>_</sup> 1<sup><u>1</u></sup><sup>_−_</sup> _−_<sup>_<u>x</u>_</sup> _τ_<sup>_<u>τ</u>_</sup> is the target velocity, representing the straight line direction required to solve a two-step jump. By minimizing this regression loss, the student model learns to internalize the straightened flow enabling the robot to execute complex tasks using only two function evaluations during inference. 

### _3.2.3. Classifier-Free Guidance (CFG)_ 

We optionally apply CFG [23] to trade off instruction adherence and a learned interaction prior at inference time. To enable instruction-free predictions, we train the policy with instruction masking: during training, the instruction is replaced with a learned null instruction token with probability _p_ masked. 

We obtain two predictions: a conditional prediction _v_ cond with the instruction, and an instruction-free prediction _v_ uncond by replacing the instruction with a null token. We then form a guided velocity field by linearly combining these two predictions: 


5 


where _w_ controls the strength of guidance. We treat _w_ as an operational knob controlling how strongly the instruction biases the prior. In practice, strong guidance can make the policy more proactive in following the instruction, which can cause overly aggressive motion when _w ≫_ 1. 

To stabilize, we apply a guidance rescaling step after the affine combination. Concretely, we match the norm of the guided output to the norm of the conditional output [34]: 


with _ε_ = 1 _×_ 10<sup>_−_6</sup> for numerical stability. 

### _3.2.4. High-Frequency Control_ 

We reinvest the latency reduction from distillation not merely to idle the processor, but to unlock a more responsive control regime. By reducing inference time, we can afford to shorten the execution horizon and re-infer more frequently under the same real-time budget. This “high-frequency feedback” design directly counters the accumulation of drift and timing errors, boosting MTBI in dynamic real-world settings. This design is especially effective when ESPADA is applied: because downsampling reduces the temporal density of demonstrations, we correspondingly shorten the action chunk horizon, which we find generally improves performance in practice. Finally, we run the full perception-to-action loop on-device to eliminate network latency and ensure predictable response times. 

### **3.3. Data Strategy: From Play to Task** 

### _3.3.1. Data collection interfaces_ 

To support both unstructured play and deployment-aligned cyclic demonstrations, we built a unified data collection pipeline with multiple interfaces: (1) Universal Data Device (UDD), a modular robot-free device that mounts the deployment gripper to minimize embodiment mismatch; (2) Meta Quest hand-tracking for upper-body teleoperation (retargeted to either hands or an “easy-gripper” abstraction); and (3) manufacturer-provided leader-arm teleoperation for robot-native demonstrations. See Appendix B for detailed data collection methods. 

### _3.3.2. Play Dataset: Building a Robust Prior_ 

While task demonstrations provide the optimal trajectory for success, they fundamentally lack coverage of the state space required for recovery. In contrast, play data consists of unstructured teleoperated interactions and naturally captures a diverse range of behaviors, including regrasping, repositioning, and local corrections [41, 13]. Leveraging this, we collect a large-scale play corpus to serve as a foundation for general manipulation priors. We do not treat play data as a substitute for task data. Instead, it expands coverage around the task manifold and increases exposure to recovery-adjacent behavior. By pre-training on this language-unconditioned play data, the action expert acquires a robust, task-agnostic understanding of physical interaction, captured by the unconditional prior. 

### _3.3.3. Cyclic Task Dataset: Aligning for Continuity_ 

Standard imitation learning datasets typically consist of isolated, “success-then-stop” episodes initiated from curated initial states [47]. We refer to this as **non-cyclic data** . As shown in Section 4, policies trained on noncyclic data struggle under continuous repetition because they do not learn to handle the state drift across cycles. To address this, we introduce a cyclic trajectory dataset formulation. Instead of resetting after each success, we collect demonstrations as continuous streams of repeated task execution. This exposes the model to the transition between cycles, connecting the end of one iteration to the beginning of the next, and to the drift that accumulates over time. We refer to this collection of continuous, reset-free demonstrations as the **cyclic data** . For task-specific alignment, we curate a focused cyclic dataset totaling approximately 10 hours for the target workflow. This dataset serves two purposes. First, it is the sole training corpus for our baseline comparisons, establishing performance without play data priors. Second, it is the fine-tuning target for our method. By posttraining on these demonstrations, we project the broad, task-agnostic motion prior acquired from play data onto 

6 


the precise manifold of the target task, ensuring that the policy retains high-level goal adherence while benefiting from low-level robust behavior. 

### _3.3.4. Spatially Aware Downsampling (ESPADA)_ 

To increase physical execution speed, we apply **Spatially Aware Downsampling (ESPADA)** [28] to demonstrations. Uniform downsampling can alias short, contact-rich interactions. ESPADA avoids this by using a VLM-LLM pipeline to semantically segment trajectories into “casual” (transit) and “precision” (contact-rich) phases based on 3D gripper-object spatial relations. We then apply selective acceleration via a replicate-before-downsample strategy, aggressively compressing casual segments while preserving high-frequency control in precision phases. To maintain policy stability under acceleration, we enforce geometric consistency by rescaling the action chunk horizon _H_<sup>_′_</sup> = _⌈ N_<sup>_<u>H</u>⌉_withthedownsamplingfactor</sup><sup>_N_suchthatthespatialdisplacementmatches:</sup> 


where ∆ _x_ represents the original end-effector displacement, and ∆ _x_<sup>_′_</sup> represents the accelerated version. This ensures that the policy learns consistent spatial action distributions even when temporal density varies, mitigating slow conservative motion without sacrificing manipulation success. 

## **4. Experiments** 

To evaluate our deployment metrics, we conduct 1-hour continuous-run experiments both in simulation and in the real world. 

### **4.1. Models and Baselines** 

We benchmark Habilis- _β_ against two strong publicly available VLA architectures. To ensure a fair comparison of architectural and methodological capabilities, all models are evaluated under the identical 1-hour continuous-run protocol. 

- **Habilis-** **_β_ (Ours):** We follow all aforementioned procedures for training and inference. 

- _π_ 0 _._ 5 **:** We fine-tune the publicly available _π_ 0 _._ 5 checkpoint [3] under two training conditions: one following the standard dataset protocol and the other using our Play+Cyclic multi-task dataset. 

- GR00T N1.5: Similarly, we fine-tune the official GR00T N1.5 checkpoint [44] under two training conditions. 

All models are trained in a multi-task setting, where a single policy handles multiple tasks. 

### **4.2. Simulation Experiments** 

### _4.2.1. Simulation Setup_ 

We leverage the RoboTwin 2.0 [9] simulation suite equipped with an Aloha bimanual manipulator [57] as our primary testbed. To bridge the gap between episodic simulation and continuous real-world operation, we reengineered the standard evaluation environments to support long-horizon continuous task execution. 

**Simulation Tasks.** We evaluate on three simulation tasks: `Dump Bin Bigbin` (DBB), `Place Dual Shoes` (PDS), and `Stack Bowls Three` (SBT), in the same top-to-bottom order shown in Figure 3. 

`Dump Bin Bigbin` tests long-horizon bimanual coordination with a multi-stage sequence: the agent first approaches and secures a stable grasp on one of five table bin variants, then reorients and transports the bin toward the target area; depending on the spawn location, it may include an additional repositioning step to move the object into a region that is reachable by the left hand, performs a hand-to-hand transfer when direct reach is constrained, and finally tilts the bin to dump all contents into the large destination bin. 

7 


**Figure 3: Simulation Task Setup.** Simulation tasks used in our continuous-run benchmark are (top to bottom): `Dump Bin Bigbin` (DBB), `Place Dual Shoes` (PDS), and `Stack Bowls Three` (SBT). Detailed task procedures are described in the _Simulation Task_ paragraph below. 

`Place Dual Shoes` evaluates precise object placement through an ordered two-object routine: the policy identifies left/right shoe instances, performs a coordinated bimanual pickup in which both hands grasp the two shoes simultaneously when feasible, aligns its orientation to the designated placement frame, places the first shoe, and then repeats the same sequence for the second shoe while preserving pair-level spatial consistency. 

`Stack Bowls Three` evaluates compositional manipulation via progressive stacking: the agent picks a base bowl and establishes a stable first placement, retrieves the second bowl and aligns it concentrically on top of the base, then places the third bowl to complete the stack while continuously correcting pose errors to prevent toppling. 

Across all tasks, object instances and initial poses are randomized per trial to measure robustness and generalization under continuous operation. 

**Continuous-run Evaluation Protocol.** We subject the policy to a continuous 1-hour autonomous cycle. The evaluation protocol follows a strict success-or-reset rule with task-specific time limits: for `Dump Bin Bigbin` and `Place Dual Shoes` , a trial is deemed successful if completed within 15 seconds, whereas `Stack Bowls Three` uses a 30-second limit. Upon success, the environment immediately re-spawns a new target, allowing the agent to transition seamlessly to the next trial. Failure to complete a trial within its time limit is classified as a timeout state, triggering a forced reset (intervention). 

**Table 1: Simulation Deployment Performance.** We report results for policies trained and evaluated on three simulated tasks: `Dump Bin Bigbin` , `Place Dual Shoes` , and `Stack Bowls Three` . For each task, we compute TPH, MTBI, and Success Rate under the continuous-run protocol, and report the average across the three tasks. 

|**Method**|**Data Regime**|**TPH**|**MTBI(s)**|**Success Rate(%)**|
|---|---|---|---|---|
|_π_0_._5|Normal|120.5|30.5|47.8|
|_π_0_._5|Play + Cyclic|207.1|49.9|69.3|
|GR00T N1.5|Normal|1.2|20.4|0.5|
|GR00T N1.5|Play + Cyclic|5.0|20.6|2.1|
|**Habilis-****_β_ (w/o ESPADA)**|Play + Cyclic|250.5|**72.4**|76.8|
|**Habilis-****_β_**|Play + Cyclic + ESPADA|**572.6**|39.2|**78.5**|


8 


### _4.2.2. Simulation Results_ 

We compare Habilis- _β_ against the _π_ 0 _._ 5, GR00T N1.5 baselines. We report metrics averaged over three tasks, each evaluated for 1-hour across three evaluation seeds. TPH, MTBI, and success rate are computed per run and then averaged. Our empirical results are summarized in Table 1. Compared to _π_ 0 _._ 5, Habilis- _β_ increases TPH from 120 _._ 5 to 572 _._ 6, improves MTBI from 30 _._ 5 to 39 _._ 2, and raises success rate from 47 _._ 8% to 78 _._ 5%. 


**Figure 4: Simulation Per-Task Results.** We break down the continuous-run performance metrics (TPH, MTBI, and Success Rate) for each simulation task. Habilis- _β_ consistently outperforms baselines across all tasks, with ESPADA significantly boosting throughput (TPH) while maintaining high success rates. 

A per-task comparison across methods is shown in Figure 4. Across all tasks, Habilis- _β_ achieves the highest TPH and success rate. However, applying ESPADA leads to a consistent reduction in MTBI. As illustrated in Figure 5, this reflects a clear productivity–reliability trade-off. Training with ESPADA substantially accelerates execution, yielding a large gain in productivity (TPH) while largely preserving success rate. However, this speedup comes with increased intervention frequency, which reduces MTBI compared to the non-ESPADA counterpart. Intuitively, executing successful trials faster can shift the composition of outcomes: for a fixed evaluation horizon and comparable success rate, more successes per hour also imply more opportunities to encounter (time-limited) failures, increasing the share of timeout episodes that trigger interventions. These results suggest that ESPADA primarily shifts the operating point along the PRP. It improves productivity by enabling faster motion, but can 

9 


**Figure 5: Simulation Productivity-Reliability Plane.** We plot the deployment performance of different methods in simulation. Habilis- _β_ (w/o ESPADA) achieves the highest reliability (MTBI), while the full Habilis- _β_ dramatically increases throughput (TPH), offering a configurable trade-off for different operational needs. 

make the system more prone to timeouts unless paired with additional robustness mechanisms. 

### _4.2.3. Standard RoboTwin 2.0 Single-Trial Evaluation_ 

To validate the fundamental manipulation capability of Habilis- _β_ against state-of-the-art methods, we also conduct evaluations using the standard RoboTwin 2.0 benchmark[9]. Unlike our continuous-run setting, this protocol measures the success rate over 100 independent single-trial episodes with curated resets. We compare Habilis- _β_ against the task-wise top-performing models on the RoboTwin 2.0 leaderboard: DP3 [55] for `Dump Bin Bigbin` , and _π_ 0 [4] for `Place Dual Shoes` and `Stack Bowls Three` . 


**Figure 6: Standard RoboTwin 2.0 Benchmark Results.** Success rates are measured over 100 independent episodes with curated resets under the standard RoboTwin 2.0 benchmark. Habilis- _β_ results are averaged across three evaluation runs to reduce seed variance. 

As shown in Figure 6, Habilis- _β_ also achieves strong performance on the single-trial benchmark, ranking highest on the leaderboard and outperforming these baselines. 

10 


**Figure 8: Real-world Task Setup.** We conduct continuous sequential execution of the `Dual-Bin Conveyor Packing` task. The workflow involves: (1) picking an item with the right hand, (2) picking an item with the left hand, (3) waiting for the conveyor, (4) dropping the right-hand object at the correct timing, (5) dropping the lefthand object at the correct timing, and (6) immediately transitioning to the next cycle (picking with the right hand). This setup challenges the policy to maintain precise timing and coordination over long-duration runs. 

### **4.3. Real-world Experiments** 

### _4.3.1. Real-world Setup_ 

We evaluate on an RB-Y1 humanoid robot in a repetitive industrial-style workflow. One of the target logistics tasks requires the humanoid to perform `Dual-Bin Conveyor Packing (DBCP)` : the robot retrieves an object from one of two source bins, establishes a stable bimanual grasp, and places the item into an open box moving on a conveyor, requiring both precise timing and collision-free insertion. 

**Robot Platform.** We utilize the RB-Y1 humanoid platform developed by Rainbow Robotics (Figure 7). This bimanual system is equipped with a multi-camera setup for robust perception: a ZED 2i stereo camera mounted on the head for global scene understanding, and Intel RealSense D405 cameras mounted on each wrist for fine-grained manipulation feedback. The end-effectors are two-finger parallel grippers designed for versatile grasping. For on-device inference, we run the full perception-to-action stack on an NVIDIA Jetson Orin. 


**Task Specification:** `Dual-Bin Conveyor Packing` . We evaluate our system **Figure 7: RB-Y1.** We used on a high-frequency industrial workflow requiring precise bimanual coordination a humanoid platform in realand dynamic temporal synchronization. As shown in Figure 8, the task cycle is world experiments. structured into three phases: (1) _Right-hand Pick_ , where the robot grasps an object from the right supply bin; (2) _Left-hand Pick_ , where the left arm retrieves an object from the left bin; and (3) _Dynamic Placement_ , where the agent must synchronize with a moving conveyor belt to accurately deposit both items into a passing target box. This task serves as a rigorous stress test for handling external timing constraints and maintaining throughput under continuous operation. The supply bins contain over 100 objects piled in random spatial distributions. Each trial alters the configuration of objects due to physical interactions, creating a dynamic and cluttered environment where precise grasping requires robust adaptation to varying object poses and occlusions. Measured TPH metric reflects not only the robot’s execution speed but also its ability to 

11 


consistently meet these external synchronization windows without missing a cycle. 

**Definition of Intervention.** Unlike the simulation setting, which relies solely on timeouts, real-world interventions are categorized into two distinct failure modes: _Abort_ (operator-initiated termination in exceptional states requiring external recovery, e.g., an E-stop) and _Timeout_ (failure to complete the task within the allocated window despite continued activity). For instance, if the robot picks an incorrect number of objects, it must autonomously recognize the mistake and recover within the allotted window; otherwise, the episode cannot meet the success criteria in time and is recorded as a _Timeout_ , which we count as an intervention. 

**Habilis Agent.** We use **Habilis Agent** as a high-level monitoring console and logging module. While it supports broader functionality (e.g., workflow specification and supervisory control), in this work it serves to mediate interventions and provide structured, real-time logs for a fair, isolated comparison of VLA policies. When the operator determines that the current trial has entered a _Timeout_ or _Abort_ condition, they trigger a reset by clicking the corresponding action in the Habilis Agent UI; the intervention type is then automatically recorded, and the robot/environment is reset before the next trial. 

**Continuous-run Evaluation Protocol.** Following the simulation protocol, we conduct a continuous 1-hour evaluation in the real-world environment. To ensure rigorous and fair assessment of long-term robustness, we standardize the operational maintenance procedures: 

- **Initial Conditions:** Each run begins with fully stocked supply bins. 

- **Intervention-Triggered Reset:** Recognizing that grasping difficulty is highly sensitive to object distribution, we implement a standardized reset rule. If the system triggers 5 consecutive interventions, we manually shuffle the supply bins to resolve potentially adversarial clutter. 

- **Replenishment Logic:** As bins deplete, grasping difficulty naturally increases. To maintain a consistent task challenge, if the fill level drops below 10% and the system encounters 3 consecutive failures, we replenish the supply bins before resuming the run. 

### _4.3.2. Real-world Experimental Results_ 

We quantify the deployment readiness of each method by measuring its Productivity (TPH) and Reliability (MTBI) under the standardized 1-hour continuous protocol. 

**Table 2: Real-world Deployment Performance.** We compare Habilis- _β_ against baselines under a 1-hour continuous-run protocol. While baselines struggle with drift, Habilis- _β_ yields a 6 _._ 53 _×_ improvement in productivity (TPH) and 2 _._ 98 _×_ reliability (MTBI) compared to the _π_ 0 _._ 5 baseline. 

|**Method**|**Data Regime**|**TPH**|**MTBI(s)**|**Success Rate(%)**|
|---|---|---|---|---|
|_π_0_._5|Normal|19|46.1|19.6|
|_π_0_._5|Play + Cyclic|79|94.6|67.5|
|GR00T N1.5|Normal|33|53.7|33.0|
|GR00T N1.5|Play + Cyclic|63|78.2|57.7|
|**Habilis-****_β_**|**Play + Cyclic + ESPADA**|**124**|**137.4**|**82.7**|


**The Productivity-Reliability Plane.** Table 2 and Figure 9 summarize real-world performance, while Figure 10 provides per-cycle execution timelines and intervention events over the same 1-hour runs. With standard fine-tuning, both _π_ 0 _._ 5 and GR00T N1.5 are strongly productivity-constrained (19–33 TPH) and achieve only moderate reliability (46 _._ 1–53 _._ 7s MTBI). Moving to the Play+Cyclic data regime improves both throughput and reliability for both baselines, indicating that our data formulation provides a broadly useful training signal beyond our model. However, Habilis- _β_ further advances the operating point to the top-right of the PRP, achieving 124 TPH and 137 _._ 4s MTBI, along with the highest success rate (82 _._ 7%). 

12 


**Figure 9: Real-world Productivity-Reliability Plane.** We visualize the performance landscape, where the ideal system resides in the top-right quadrant (high throughput, high robustness). 


**Figure 10: Real-World Continuous Execution Timelines.** We show 1-hour continuous-run execution logs for each method. Green segments indicate successful task completions, whereas dark blue segments indicate failed attempts that do not complete within the allowed window or are terminated by the operator, and thus trigger an intervention. Markers denote intervention categories: orange diamonds for _Timeout_ and red triangles for _Abort_ . Compared to baselines, Habilis- _β_ achieves a higher density of successes with fewer interventions, supporting its longlasting robustness. 

13 


## **5. Discussion** 

While Habilis- _β_ achieves strong performance on real-world workflows, its overall generalization remains limited and has not yet reached human-level task accuracy. We expect this gap to narrow with continued scaling and engineering progress, including larger and more diverse data, improved robot hardware, and advances in foundationmodel training. 

Beyond scaling, our experiments highlight three practical considerations. First, the PRP view makes explicit that productivity (TPH), reliability (MTBI), and success rate are tightly coupled under a fixed operating horizon. Notably, higher productivity and success rates do not guarantee higher reliability: as the system attempts more cycles per hour, the absolute frequency of interventions may rise, effectively reducing MTBI. This aligns with industrial requirements prioritizing sustained operation, differing from conventional single-trial evaluation protocols. 

Second, regarding ESPADA, while it reduces redundant motion, its semantic segmentation is mediated by an LLM. Consequently, the same demonstration may produce slightly different downsampled trajectories across runs, introducing variance that can complicate reproducibility. 

Third, using CFG requires learning a strong instruction-unconditioned prior, which remains challenging given the limited scale of current robot datasets. Empirically, the optimal guidance scale varies across tasks; in some settings, disabling CFG yields the best performance. We therefore view CFG as a deployment-time parameter requiring task-specific tuning rather than a universally optimal default. 

## **6. Future Work** 

Future work will focus on three directions that we believe will be important in the long run. First, our current robot-free interfaces provide limited supervision for dexterous embodiments; we plan to extend these to improve action/observation alignment for five-finger manipulation. Second, the system lacks tactile feedback; we will incorporate tactile inputs to enhance robustness in contact-rich phases and under partial observability. Finally, to address the static nature of offline training, we will explore safe online adaptation and continual learning, allowing the system to correct recurring failure modes discovered during long-term deployment. 

## **References** 

- [1] ISO 22400-2:2014 — Automation systems and integration — Key performance indicators (KPIs) for manufacturing operations management — Part 2: Definitions and descriptions, 2014. Accessed: 2026-02-20. 

- [2] Nadun Ranawaka Arachchige, Zhenyang Chen, Wonsuhk Jung, Woo Chul Shin, Rohan Bansal, Pierre Barroso, Yu Hang He, Yingyan Celine Lin, Benjamin Joffe, Shreyas Kousik, and Danfei Xu. Sail: Faster-than-demonstration execution of imitation learning policies. In Joseph Lim, Shuran Song, and Hae-Won Park, editors, _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 721–749. PMLR, 27–30 Sep 2025. 

- [3] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, brian ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In Joseph Lim, Shuran Song, and Hae-Won Park, editors, _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 17–40, PMLR, 27–30 Sep 2025. PMLR. 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, Laura Smith, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A Vision-Language-Action Flow Model for General Robot Control. In _Proceedings of Robotics: Science and Systems_ , Los Angeles, CA, USA, June 2025. 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alexander Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Kuang-Huei Lee, Sergey Levine, Yao Lu, Utsav Malla, Deeksha Manjunath, Igor Mordatch, Ofir Nachum, Carolina Parada, Jodilyn Peralta, 

14 


Emily Perez, Karl Pertsch, Jornell Quiambao, Kanishka Rao, Michael S Ryoo, Grecia Salazar, Pannag R Sanketi, Kevin Sayed, Jaspiar Singh, Sumedh Sontakke, Austin Stone, Clayton Tan, Huong Tran, Vincent Vanhoucke, Steve Vega, Quan H Vuong, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. RT-1: Robotics Transformer for Real-World Control at Scale. In _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, July 2023. 

- [6] Pawe�l Budzianowski, Wesley Maa, Matthew Freed, Jingxiang Mo, Winston Hsiao, Aaron Xie, Tomasz M�loduchowski, Viraj Tipnis, and Benjamin Bolte. Edgevla: Efficient vision-language-action models, 2025. 

- [7] Achim Buerkle, William Eaton, Ali Al-Yacoub, Melanie Zimmer, Peter Kinnell, Michael Henshaw, Matthew Coombes, Wen-Hua Chen, and Niels Lohse. Towards industrial robots as a service (iraas): Flexibility, usability, safety and business models. _Robotics and Computer-Integrated Manufacturing_ , 81:102484, 2023. 

- [8] Quan Chen, Chenrui Shi, Qi Chen, Yuwei Wu, Zhi Gao, Xintong Zhang, Rui Gao, Kun Wu, and Yunde Jia. Long-horizon visual imitation learning via plan and code reflection, 2025. 

- [9] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, Weiliang Deng, Yubin Guo, Tian Nian, Xuanbing Xie, Qiangyu Chen, Kailun Su, Tianling Xu, Guodong Liu, Mengkang Hu, Huan ang Gao, Kaixuan Wang, Zhixuan Liang, Yusen Qin, Xiaokang Yang, Ping Luo, and Yao Mu. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation, 2025. 

- [10] Zhaoyang Chen and Cody Fleming. Modular diffusion policy training: Decoupling and recombining guidance and diffusion for offline rl, 2025. 

- [11] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

- [12] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, July 2024. 

- [13] Zichen Jeff Cui, Yibin Wang, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. From play to policy: Conditional behavior generation from uncurated robot data. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- [14] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby. An image is worth 16x16 words: Transformers for image recognition at scale. In _International Conference on Learning Representations_ , 2021. 

- [15] Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas M¨uller, Harry Saini, Yam Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel, Dustin Podell, Tim Dockhorn, Zion English, and Robin Rombach. Scaling rectified flow transformers for high-resolution image synthesis. In _Forty-first International Conference on Machine Learning_ , 2024. 

- [16] Yiguo Fan, Shuanghao Bai, Xinyang Tong, Pengxiang Ding, Yuyang Zhu, Hongchao Lu, Fengqi Dai, Wei Zhao, Yang Liu, Siteng Huang, Zhaoxin Fan, Badong Chen, and Donglin Wang. Long-vla: Unleashing long-horizon capability of vision language action model for robot manipulation. In Joseph Lim, Shuran Song, and Hae-Won Park, editors, _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 2018–2037. PMLR, 27–30 Sep 2025. 

- [17] Dibya Ghosh, Homer Rich Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Quan Vuong, Ted Xiao, Pannag R Sanketi, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An Open-Source Generalist Robot Policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, July 2024. 

- [18] Lingxiao Guo, Zhengrong Xue, Zijing Xu, and Huazhe Xu. Demospeedup: Accelerating visuomotor policies via entropyguided demonstration acceleration. In Joseph Lim, Shuran Song, and Hae-Won Park, editors, _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 599–609. PMLR, 27–30 Sep 2025. 

- [19] Abhishek Gupta, Justin Yu, Tony Z. Zhao, Vikash Kumar, Aaron Rovinsky, Kelvin Xu, Thomas Devlin, and Sergey Levine. Reset-free reinforcement learning via multi-task learning: Learning dexterous manipulation behaviors without human intervention. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6664–6671, 2021. 

- [20] Pranav Guruprasad, Harshvardhan Sikka, Jaewoo Song, Yangyue Wang, and Paul Pu Liang. Benchmarking vision, language, & action models on robotic learning tasks, 2024. 

15 


- [21] Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. Distilling the knowledge in a neural network, 2015. 

- [22] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin, editors, _Advances in Neural Information Processing Systems_ , volume 33, pages 6840–6851. Curran Associates, Inc., 2020. 

- [23] Jonathan Ho and Tim Salimans. Classifier-free diffusion guidance, 2022. 

- [24] Daniel Honerkamp, Harsh Mahesheka, Jan Ole von Hartz, Tim Welschehold, and Abhinav Valada. Whole-body teleoperation for mobile manipulation at zero added cost. _IEEE Robotics and Automation Letters_ , 10(4):3198–3205, April 2025. 

- [25] International Electrotechnical Commission (IEC). IEV 192-05-13: Mean time between failures (MTBF), n.d. Accessed: 2026-02-20. 

- [26] Gi-Cheon Kang, Junghyun Kim, Kyuhwan Shim, Jun Ki Lee, and Byoung-Tak Zhang. CLIP-RT: Learning LanguageConditioned Robotic Policies from Natural Language Supervision. In _Proceedings of Robotics: Science and Systems_ , Los Angeles, CA, USA, June 2025. 

- [27] Kento Kawaharazuka, Jihoon Oh, Jun Yamada, Ingmar Posner, and Yuke Zhu. Vision-language-action models for robotics: A review towards real-world applications. _IEEE Access_ , 13:162467–162504, 2025. 

- [28] Byungju Kim, Jinu Pahk, Chungwoo Lee, Jaejoon Kim, Jangha Lee, Theo Taeyeong Kim, Kyuhwan Shim, Jun Ki Lee, and Byoung-Tak Zhang. Espada: Execution speedup via semantics aware demonstration data downsampling for imitation learning, 2025. 

- [29] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success. In _Proceedings of Robotics: Science and Systems_ , Los Angeles, CA, USA, June 2025. 

- [30] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. In Pulkit Agrawal, Oliver Kroemer, and Wolfram Burgard, editors, _Proceedings of The 8th Conference on Robot Learning_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 2679–2713. PMLR, 06–09 Nov 2025. 

- [31] Hadas Kress-Gazit, Kunimatsu Hashimoto, Naveen Kuppuswamy, Paarth Shah, Phoebe Horgan, Gordon Richardson, Siyuan Feng, and Benjamin Burchfiel. Robot learning as an empirical science: Best practices for policy evaluation, 2024. 

- [32] Michael Laskey, Jonathan Lee, Roy Fox, Anca Dragan, and Ken Goldberg. Dart: Noise injection for robust imitation learning. In Sergey Levine, Vincent Vanhoucke, and Ken Goldberg, editors, _Proceedings of the 1st Annual Conference on Robot Learning_ , volume 78 of _Proceedings of Machine Learning Research_ , pages 143–156. PMLR, 13–15 Nov 2017. 

- [33] Hang Li, Qian Feng, Zhi Zheng, Jianxiang Feng, Zhaopeng Chen, and Alois Knoll. Language-guided object-centric diffusion policy for generalizable and collision-aware manipulation. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 12834–12841, 2025. 

- [34] Shanchuan Lin, Bingchen Liu, Jiashi Li, and Xiao Yang. Common diffusion noise schedules and sample steps are flawed. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ , pages 5404–5411, January 2024. 

- [35] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- [36] Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Pengju An, Xiaoqi Li, Kaichen Zhou, Senqiao Yang, Renrui Zhang, Yandong Guo, and Shanghang Zhang. Robomamba: Efficient vision-language-action model for robotic reasoning and manipulation. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, _Advances in Neural Information Processing Systems_ , volume 37, pages 40085–40110. Curran Associates, Inc., 2024. 

- [37] Xingchao Liu, Chengyue Gong, and qiang liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- [38] Xingchao Liu, Xiwen Zhang, Jianzhu Ma, Jian Peng, and qiang liu. Instaflow: One step is enough for high-quality diffusion-based text-to-image generation. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- [39] Yuejiang Liu, Jubayer Ibn Hamid, Annie Xie, Yoonho Lee, Max Du, and Chelsea Finn. Bidirectional decoding: Improving action chunking via guided test-time sampling. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [40] Yuang Lu, Song Wang, Xiao Han, Xuri Zhang, Yucong Wu, and Zhicheng He. Enhancing diffusion policy with classifier-free guidance for temporal robotic tasks. In _2025 IEEE 37th International Conference on Tools with Artificial Intelligence (ICTAI)_ , pages 1023–1029, 2025. 

16 


- [41] Corey Lynch, Mohi Khansari, Ted Xiao, Vikash Kumar, Jonathan Tompson, Sergey Levine, and Pierre Sermanet. Learning latent plans from play. In Leslie Pack Kaelbling, Danica Kragic, and Komei Sugiura, editors, _Proceedings of the Conference on Robot Learning_ , volume 100 of _Proceedings of Machine Learning Research_ , pages 1113–1132. PMLR, 30 Oct–01 Nov 2020. 

- [42] Corey Lynch and Pierre Sermanet. Language conditioned imitation learning over unstructured data. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2021. 

- [43] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

- [44] NVIDIA. Gr00t n1.5: An improved open foundation model for generalist humanoid robots. Online, 2025. 

- [45] NVIDIA, Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi ”Jim” Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. 

- [46] OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, Red Avila, Igor Babuschkin, Suchir Balaji, Valerie Balcom, Paul Baltescu, Haiming Bao, Mohammad Bavarian, Jeff Belgum, Irwan Bello, Jake Berdine, Gabriel BernadettShapiro, Christopher Berner, Lenny Bogdonoff, Oleg Boiko, Madelaine Boyd, Anna-Luisa Brakman, Greg Brockman, Tim Brooks, Miles Brundage, Kevin Button, Trevor Cai, Rosie Campbell, Andrew Cann, Brittany Carey, Chelsea Carlson, Rory Carmichael, Brooke Chan, Che Chang, Fotis Chantzis, Derek Chen, Sully Chen, Ruby Chen, Jason Chen, Mark Chen, Ben Chess, Chester Cho, Casey Chu, Hyung Won Chung, Dave Cummings, Jeremiah Currier, Yunxing Dai, Cory Decareaux, Thomas Degry, Noah Deutsch, Damien Deville, Arka Dhar, David Dohan, Steve Dowling, Sheila Dunning, Adrien Ecoffet, Atty Eleti, Tyna Eloundou, David Farhi, Liam Fedus, Niko Felix, Sim´on Posada Fishman, Juston Forte, Isabella Fulford, Leo Gao, Elie Georges, Christian Gibson, Vik Goel, Tarun Gogineni, Gabriel Goh, Rapha Gontijo-Lopes, Jonathan Gordon, Morgan Grafstein, Scott Gray, Ryan Greene, Joshua Gross, Shixiang Shane Gu, Yufei Guo, Chris Hallacy, Jesse Han, Jeff Harris, Yuchen He, Mike Heaton, Johannes Heidecke, Chris Hesse, Alan Hickey, Wade Hickey, Peter Hoeschele, Brandon Houghton, Kenny Hsu, Shengli Hu, Xin Hu, Joost Huizinga, Shantanu Jain, Shawn Jain, Joanne Jang, Angela Jiang, Roger Jiang, Haozhun Jin, Denny Jin, Shino Jomoto, Billie Jonn, Heewoo Jun, Tomer Kaftan, �Lukasz Kaiser, Ali Kamali, Ingmar Kanitscheider, Nitish Shirish Keskar, Tabarak Khan, Logan Kilpatrick, Jong Wook Kim, Christina Kim, Yongjik Kim, Jan Hendrik Kirchner, Jamie Kiros, Matt Knight, Daniel Kokotajlo, �Lukasz Kondraciuk, Andrew Kondrich, Aris Konstantinidis, Kyle Kosic, Gretchen Krueger, Vishal Kuo, Michael Lampe, Ikai Lan, Teddy Lee, Jan Leike, Jade Leung, Daniel Levy, Chak Ming Li, Rachel Lim, Molly Lin, Stephanie Lin, Mateusz Litwin, Theresa Lopez, Ryan Lowe, Patricia Lue, Anna Makanju, Kim Malfacini, Sam Manning, Todor Markov, Yaniv Markovski, Bianca Martin, Katie Mayer, Andrew Mayne, Bob McGrew, Scott Mayer McKinney, Christine McLeavey, Paul McMillan, Jake McNeil, David Medina, Aalok Mehta, Jacob Menick, Luke Metz, Andrey Mishchenko, Pamela Mishkin, Vinnie Monaco, Evan Morikawa, Daniel Mossing, Tong Mu, Mira Murati, Oleg Murk, David M´ely, Ashvin Nair, Reiichiro Nakano, Rajeev Nayak, Arvind Neelakantan, Richard Ngo, Hyeonwoo Noh, Long Ouyang, Cullen O’Keefe, Jakub Pachocki, Alex Paino, Joe Palermo, Ashley Pantuliano, Giambattista Parascandolo, Joel Parish, Emy Parparita, Alex Passos, Mikhail Pavlov, Andrew Peng, Adam Perelman, Filipe de Avila Belbute Peres, Michael, Pokorny, Michelle Pokrass, Vitchyr H. Pong, Tolly Powell, Alethea Power, Boris Power, Elizabeth Proehl, Raul Puri, Alec Radford, Jack Rae, Aditya Ramesh, Cameron Raymond, Francis Real, Kendra Rimbach, Carl Ross, Bob Rotsted, Henri Roussez, Nick Ryder, Mario Saltarelli, Ted Sanders, Shibani Santurkar, Girish Sastry, Heather Schmidt, David Schnurr, John Schulman, Daniel Selsam, Kyla Sheppard, Toki Sherbakov, Jessica Shieh, Sarah Shoker, Pranav Shyam, Szymon Sidor, Eric Sigler, Maddie Simens, Jordan Sitkin, Katarina Slama, Ian Sohl, Benjamin Sokolowsky, Yang Song, Natalie Staudacher, Felipe Petroski Such, Natalie Summers, Ilya Sutskever, Jie Tang, Nikolas Tezak, Madeleine B. Thompson, Phil Tillet, Amin Tootoonchian, Elizabeth Tseng, Preston Tuggle, Nick Turley, Jerry Tworek, Juan Felipe Cer´on Uribe, Andrea Vallone, Arun Vijayvergiya, Chelsea Voss, Carroll Wainwright, Justin Jay Wang, Alvin Wang, Ben Wang, Jonathan Ward, Jason Wei, CJ Weinmann, Akila Welihinda, Peter Welinder, Jiayi Weng, Lilian Weng, Matt Wiethoff, Dave Willner, Clemens Winter, Samuel Wolrich, Hannah Wong, Lauren Workman, Sherwin Wu, Jeff Wu, Michael Wu, Kai Xiao, Tao Xu, Sarah Yoo, Kevin Yu, Qiming Yuan, Wojciech Zaremba, Rowan Zellers, Chong Zhang, Marvin Zhang, Shengjia Zhao, Tianhao Zheng, Juntang Zhuang, William Zhuk, and Barret Zoph. Gpt-4 technical report, 2024. 

- [47] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, Andrew Wang, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony 

17 


Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben BurgessLimerick, Beomjoon Kim, Bernhard Sch¨olkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter B¨uchler, Dinesh Jayaraman, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guanzhi Wang, Hao Su, Hao-Shu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan Schneider, Jasmine Hsu, Jeannette Bohg, Jeffrey Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun Yang, Jitendra Malik, Jo˜ao Silv´erio, Joey Hejna, Jonathan Booher, Jonathan Tompson, Jonathan Yang, Jordi Salvador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran Lekkala, Kirsty Ellis, Krishan Rana, Krishnan Srinivasan, Kuan Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen, Lerrel Pinto, Li Fei-Fei, Liam Tan, Linxi Jim Fan, Lionel Ott, Lisa Lee, Luca Weihs, Magnum Chen, Marion Lepert, Marius Memmel, Masayoshi Tomizuka, Masha Itkina, Mateo Guaman Castro, Max Spero, Maximilian Du, Michael Ahn, Michael C. Yip, Mingtong Zhang, Mingyu Ding, Minho Heo, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Ning Liu, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Osbert Bastani, Pannag R Sanketi, Patrick Tree Miller, Patrick Yin, Paul Wohlhart, Peng Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet, Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Mart´ın-Mart´ın, Rohan Baijal, Rosario Scalise, Rose Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Shan Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham Sonawani, Shuran Song, Sichun Xu, Siddhant Haldar, Siddharth Karamcheti, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Subramanian Ramamoorthy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung, Vidhi Jain, Vincent Vanhoucke, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiaolong Wang, Xinghao Zhu, Xinyang Geng, Xiyuan Liu, Xu Liangwei, Xuanlin Li, Yao Lu, Yecheng Jason Ma, Yejin Kim, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao, Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang, Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff Cui, Zichen Zhang, and Zipeng Lin. Open x-embodiment: Robotic learning datasets and rt-x models : Open x-embodiment collaboration0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903, 2024. 

- [48] Abhishek Paudel. Learning for robot decision making under distribution shift: A survey, 2022. 

- [49] Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Score-based generative modeling through stochastic differential equations. In _International Conference on Learning Representations_ , 2021. 

- [50] Songsheng Wang, Rucheng Yu, Zhihang Yuan, Chao Yu, Feng Gao, Yu Wang, and Derek F. Wong. Spec-VLA: Speculative decoding for vision-language-action models with relaxed acceptance. In Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng, editors, _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , pages 26928–26940, Suzhou, China, November 2025. Association for Computational Linguistics. 

- [51] Justin Williams, Kishor Datta Gupta, Roy George, and Mrinmoy Sarkar. Lite vla: Efficient vision-language-action control on cpu-bound edge robots, 2025. 

- [52] Ge Yan, Jiyue Zhu, Yuquan Deng, Shiqi Yang, Ri-Zhao Qiu, Xuxin Cheng, Marius Memmel, Ranjay Krishna, Ankit Goyal, Xiaolong Wang, and Dieter Fox. Maniflow: A general robot manipulation policy via consistency flow training. In _9th Annual Conference on Robot Learning_ , 2025. 

- [53] Hyung-Suk Yoon and Seung-Woo Seo. How to mitigate the distribution shift problem in robotics control: A robust and adaptive approach based on offline to online imitation learning, 2026. 

- [54] Yang Yue, Yulin Wang, Bingyi Kang, Yizeng Han, Shenzhi Wang, Shiji Song, Jiashi Feng, and Gao Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, _Advances in Neural Information Processing Systems_ , volume 37, pages 56619–56643. Curran Associates, Inc., 2024. 

18 


- [55] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, July 2024. 

- [56] Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue Yin, Zuxuan Wu, Yu-Gang Jiang, and Xipeng Qiu. Vlabench: A large-scale benchmark for language-conditioned robotics manipulation with long-horizon reasoning tasks. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 11142–11152, October 2025. 

- [57] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. In _Proceedings of Robotics: Science and Systems_ , Daegu, Republic of Korea, July 2023. 

- [58] Yuanzhi Zhu, Xingchao Liu, and Qiang Liu. Slimflow: Training smaller one-step diffusion models with rectified flow. In Aleˇs Leonardis, Elisa Ricci, Stefan Roth, Olga Russakovsky, Torsten Sattler, and G¨ul Varol, editors, _Computer Vision – ECCV 2024_ , pages 342–359, Cham, 2025. Springer Nature Switzerland. 

- [59] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In Jie Tan, Marc Toussaint, and Kourosh Darvish, editors, _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 2165–2183. PMLR, 06–09 Nov 2023. 

19 


## **Appendix** 

## **A. Contributions and Acknowledgements** 

**Core Contributors.** Jesoon Kang, Taegeon Park, Jisu An, Soo Min Kimm, Jaejoon Kim **Contributors.** Jinu Pahk, Byungju Kim, Junseok Lee, Namheon Baek, Sungwan Ha, Hojun Baek, Eduardo Ayerve Cruz, Wontae Kim, Junghyeon Choi, Yousuk Lee, Joonmo Han, Sunghyun Cho, Sunghyun Kwon, Soyoung Lee **Advisors.** Jun Ki Lee, Seung-Joon Yi, Byoung-Tak Zhang **Project Lead.** Theo Taeyeong Kim 

We thank the data collection team for their efforts in collecting and curating the dataset. Special thanks go to Soo Beom Hwang, Jaehyun Jeong, and Jaehun Heo for their contributions to assembling the `Dual-Bin Conveyor Packing` task dataset. We are also grateful to Robot Field Engineer Kangin Lee for his essential technical support and hardware maintenance throughout the experiments. 

## **B. Data Collection Interfaces** 

**Universal Data Device.** Universal Manipulation Interface (UMI) [12] proposes a portable demonstration interface based on a hand-held, sensorized gripper and an aligned observation/action interface for policy learning. It emphasizes (1) portability for collecting demonstrations outside the lab, and (2) transferability across robot platforms by using inference-time latency matching and a relative-trajectory action representation. In our setting, however, the target embodiments vary substantially across deployments (e.g., different grippers/end-effectors and mounting geometries). This made a one-size-fits-all handheld interface insufficient: even small differences in grasp geometry, actuation limits, and camera extrinsics can induce systematic distribution shifts that accumulate in long-horizon, repeated execution [24]. 

To address the above, we designed Universal Data Device (UDD) as a modular data collection device whose _front-end is the actual robot gripper_ (or a mechanically equivalent gripper module). The core design goal is to minimize the action/observation embodiment gap by anchoring demonstrations to the end-effector that will be used at deployment time, while still enabling robot-free data collection. Concretely, UDD provides: 

- **Universal gripper mounting** : a quick-swap mechanical/electrical interface that allows attaching different manufacturer grippers without redesigning the rest of the device. 

- **Pose tracking for 6D actions** : visual-inertial tracking (and/or equivalent onboard sensing) to recover end-effector pose trajectories with sufficient fidelity for fast motions and contact-rich segments. 

- **Gripper actuation logging** : direct sensing of gripper instructions/states (e.g., width/force/trigger signals depending on the gripper), recorded in sync with pose and vision streams. 

With UDD, collecting VLA trajectories no longer depends on bringing the full robot to every environment. Instead, the device preserves the deployed end-effector’s geometry and control constraints, making the collected data compatible with diverse robot embodiments via a consistent interface layer. 

**Meta Quest teleoperation via hand tracking.** In addition to device-based demonstrations, we developed an upper-body teleoperation pipeline using Meta Quest hand tracking. The system provides time-synchronized 3D hand poses (and joint configurations) and retargets them to either (1) a hand embodiment or (2) a lightweight “easy gripper” abstraction in which pinch/open gestures are mapped to gripper commands. Notably, this setup captures dexterous human hand motion using only an off-the-shelf VR device, eliminating the need for expensive external motion-capture hardware, markers, or dedicated tracking infrastructure. 

**Leader-arm robot demonstrations.** Finally, our dataset includes demonstrations collected using manufacturer provided leader-arm (master) interfaces. This provides high-precision robot-native demonstrations that complement the broader coverage and diversity of UDD/hand-tracking data. 

20 


## **C. Habilis Agent** 

Habilis Agent is a software system designed for defining robot workflows, integrating components (e.g., VLAs, navigation), and monitoring inference. In this work, we primarily utilize it as a structured logging interface for long-horizon evaluation. Operators use the UI to label trial states (e.g., _Timeout_ or _Abort_ ) and trigger resets; the system automatically executes the reset procedure and records the intervention. Additionally, Habilis Agent logs a comprehensive execution timeline—tracking successes, timeouts, and aborts, to facilitate debugging and enable reliable TPH/MTBI measurement across long-duration experiments. 

## **D. Habilis Console** 

Habilis Console is a platform for collecting robot demonstration data by connecting diverse robots and teleoperation devices, managing datasets, and training Robot Foundation Models (RFMs). Most of our data collection pipeline and model training, covering both the baselines and Habilis- _β_ , were conducted within Habilis Console. 

Further details are available at `https://tommoro-ai.github.io/habilis-console/` , and the platform is scheduled for an official release in March 2026. 

## **E. Related Works** 

### **E.1. Vision-Language-Action Models** 

**Foundations of Generalist Robot Policies.** The success of foundation models in NLP and vision introduced a new paradigm for robotics: a single, high-capacity model, pre-trained on diverse data, that can solve new tasks with little or no task-specific adaptation [27]. This idea has taken shape as VLA models. Early systems like RT-1 [5] tokenized continuous actions into a discrete vocabulary, utilizing transformers to map image-text inputs to action tokens. RT-2 [59] then demonstrated that large pre-trained vision-language models (VLMs) can be adapted to output robot actions, leveraging broad semantic representations and language-grounded reasoning. In parallel, scaling efforts and open-source work have produced generalist policies such as Octo [17]. More recently, approaches such as OpenVLA [30, 29] fine-tune VLM backbones to output robot actions directly, further strengthening the VLM-centric direction. 

**Action Generation with Diffusion and Flow Matching.** Alongside model scaling, action generation in robot policies has increasingly relied on generative modeling. Diffusion-based policies [11, 55], grounded in diffusion/score-based models [22, 49], gained early traction for their ability to represent multimodal action distributions, albeit at the cost of iterative denoising and higher inference latency. 

To mitigate this computational burden, flow matching objectives were introduced as an alternative that learns a direct (often deterministic) transport from noise to actions, enabling substantially fewer inference steps [35]. Representative early applications in robotics include ManiFlow [52] and _π_ 0 [4], which demonstrated that flow-based action generation can preserve action quality while improving sampling efficiency. 

More recently, these two paradigms have been adopted in foundation-scale VLA systems. For example, GR00T N1.5 [45] follows a diffusion-style action generator, while _π_ 0 _._ 5 [3] builds upon flow-matching-style generation. This progression highlights the practical trade-off between action expressivity and inference cost in deployed control loops. 

However, capability gains do not automatically translate to deployment readiness. In repetitive industrial settings, generalist models can struggle to sustain high throughput and stable operation over long runs, where both productivity and reliability are first-class constraints. 

### **E.2. Fast-Motion** 

While VLAs have improved in semantic understanding, physical execution speed remains a major bottleneck for deployment. In practice, many policies produce overly fine-grained, temporally dense action sequences, taking many small steps even in phases where rapid motion would be safe. This conservative temporal behavior often 

21 


reflects the granularity of teleoperation data and directly reduces throughput in repetitive workflows. 

**Data-level Speed Shaping.** Recent efforts attempt to increase action-level speed by modifying the temporal structure of demonstrations. Heuristics such as DemoSpeedup [18] and SAIL [2] compress demonstrations or vary control rates to accelerate free-space motion. While these methods can improve throughput, they are largely heuristic and may risk instability when contact-rich phases are compressed. 

**The Need for Semantic-Temporal Adaptivity.** Fast-motion requires more than uniformly running at a higher speed; it requires reasoning about when to move fast. A deployment-oriented policy should treat free-space motion differently from contact and precision phases. Free-space segments can be coarse and fast, while interaction segments must remain fine-grained and reactive. This motivation underpins our adoption of ESPADA [28] in Habilis- _β_ , which adjusts temporal granularity using task-relevant semantics to accelerate transit while preserving contact-critical control. 

### **E.3. Long-Lasting** 

**Industrial Metrics vs. Academic Success Rates.** In traditional manufacturing, production performance is often tracked using Overall Equipment Effectiveness (OEE) [1], alongside reliability metrics such as Mean Time Between Failures (MTBF) [25]. In contrast, much of academic VLA research emphasizes episode-level success rate under short horizons and curated resets. Recent long-horizon works (e.g., Long-VLA [16], LoHoVLA [8]) extend the context length, but they are not explicitly designed for long-lasting, repetitive deployment where policies must sustain performance under continual execution with minimal human intervention. 

**The “Intervention” Bottleneck.** In production, the dominant cost is often not a single failure on a difficult task. It is the frequency of human intervention caused by drift, accumulated error, or frozen states over hours of operation. Yet standardized evaluation protocols that measure this “intervention-free” capability remain limited [56, 20, 43]. To bridge this gap, we adopt Mean Time Between Intervention (MTBI). MTBI measures the average operating time between events that require external intervention. We argue that industrially viable VLA systems must incorporate priors that prevent drift and support recovery, which is a central design goal in Habilis- _β_ . 

**Play Data.** Large-scale play data is attractive for learning robust, low-level interaction skills because it can be collected without task segmentation, language annotation, or curated resets. Beyond lowering data acquisition cost, play data often includes recovery-adjacent states and diverse contact configurations that are underrepresented in success-only demonstrations. This matters for sustained operation under repetition. Prior works [41, 42] show how play data can be structured into reusable latents and leveraged for downstream goal-directed control, improving robustness and retry behavior even without explicit task labels. 

### **E.4. On-Device** 

On-device execution matters because it makes end-to-end latency and reliability less sensitive to network variability and remote service dependencies. However, running the full perception-to-action loop locally imposes tight compute and power budgets, motivating VLA models and runtimes designed explicitly for efficient inference. Recent works explore efficiency from multiple angles, including lightweight language-conditioned policies [26] and dynamic inference mechanisms that adapt computation to the current control context [54]. Architectural and decoding strategies such as RoboMamba [36] (SSM-based backbones) and Spec-VLA [50] (speculative decoding) further target reduced inference latency for real-time control. 

**Rectified Flow.** For generative action models, deployment constraints often translate to a need to reduce iterative sampling while preserving action quality. Distillation and step-reduction techniques address this by compressing multi-step generation into a small number of solver steps, enabling higher-frequency re-inference within 

22 


a fixed latency budget. Rectified flow [37] offers a framework that supports such step-reduction via trajectory rectification and related distillation-style constructions. 

### **E.5. Classifier-Free Guidance (CFG)** 

**Classifier-Free Guidance.** CFG [23] offers an inference-time control knob by mixing conditional and unconditional predictions to adjust how strongly the model follows task conditioning versus learned priors. While CFG has appeared in several policy-learning settings [40, 10, 33], our use follows the traditional conditional generation setup. 

23 

