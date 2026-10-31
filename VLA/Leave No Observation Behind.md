---
title: "Leave No Observation Behind: Real-time Correction for VLA Action Chunks"
date: "2025-09-27"
authors: "Kohei Sendai; Maxime Alvarez; Tatsuya Matsushima; Yutaka Matsuo; Yusuke Iwasawa"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2509.23224
pdf: https://arxiv.org/pdf/2509.23224
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.23224)** / [論文ページ](https://arxiv.org/abs/2509.23224)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# LEAVE NO OBSERVATION BEHIND: REAL-TIME CORRECTION FOR VLA ACTION CHUNKS 

**Kohei Sendai Maxime Alvarez Tatsuya Matsushima** The University of Tokyo 

_{_ kohei.sendai, maxime.alvarez, matsushima _}_ @weblab.t.u-tokyo.ac.jp 

**Yutaka Matsuo Yusuke Iwasawa** The University of Tokyo _{_ matsuo, iwasawa _}_ @weblab.t.u-tokyo.ac.jp 

## ABSTRACT 

To improve efficiency and temporal coherence, Vision-Language-Action (VLA) models often predict action chunks; however, this action chunking harms reactivity under inference delay and long horizons. We introduce _Asynchronous Action Chunk Correction (A2C2)_ , which is a lightweight real-time chunk correction head that runs every control step and adds a time-aware correction to any off-the-shelf VLA’s action chunk. The module combines the latest observation, the predicted action from VLA (base action), a positional feature that encodes the index of the base action within the chunk, and some features from the base policy, then outputs a per-step correction. This preserves the base model’s competence while restoring closed-loop responsiveness. The approach requires no retraining of the base policy and is orthogonal to asynchronous execution schemes such as Real Time Chunking (RTC). On the dynamic KINETIX task suite (12 tasks) and LIBERO SPATIAL, our method yields consistent success rate improvements across increasing delays and execution horizons (+23% point and +7% point respectively, compared to RTC), and also improves robustness for long horizons even with zero injected delay. Since the correction head is small and fast, there is minimal overhead compared to the inference of large VLA models. These results indicate that A2C2 is an effective, plug-in mechanism for deploying high-capacity chunking policies in real-time control. 

## 1 INTRODUCTION 

Recent advances in large vision–language–action (VLA) models have significantly expanded the capability of robots to generalize across tasks and environments (Black et al., 2024; Gemini Robotics Team et al., 2025; NVIDIA et al., 2025; TRI LBM Team et al., 2025). However, large model size requires high computational cost to output the actions for each step, which leads to high inference latency (Kawaharazuka et al., 2025; Black et al., 2025). Especially in dynamic control, such delays become critical. A robot relying on long action sequences predicted from outdated observations can drift, overlook cues, or fail in tasks demanding rapid reactions, such as catching moving objects or stabilizing unstable systems. 

The trend of scaling up neural network policies using foundation models brings representational benefits (Sartor & Thompson, 2025), but also incurs a latency problem. For instance, large VLA models such as _π_ 0 (Black et al., 2024) or OpenVLA (Kim et al., 2024) have billions of parameters and often require hundreds of milliseconds to generate a single action chunk. These action chunks are predicted solely from the previous observation and then executed in an open-loop manner, without incorporating new sensory input during their execution. In addition, latency not only delays execution but also prevents the policy from incorporating the latest observations, thereby weakening its ability to produce reactive behaviors. This is particularly problematic in tasks where the environment changes rapidly during inference. For instance, following a moving object on a cluttered table or grasping a utensil while other objects are being placed, the robot should adjust its action sequence to new sensory inputs. In these scenarios, actions computed from outdated observations accumulate 

1 


Figure 1: Illustration of asynchronous action chunk execution and its problem. _H_ denotes the horizon length of an action chunk. _e_ is the execution horizon, and _d_ is the inference delay caused by policy inference. (Policy generates a horizon _H_ length action chunk. Inference of the policy takes _d_ steps. While the next chunk is inferred, we execute _e_ steps from the current chunk. Each executed action is based on an observation at least _d_ steps old, and in the worst case, the action may correspond to an observation that is _d_ + _e_ steps old. 

errors over time, which lowers success rates and, in some cases, leads to task failure. This is the central challenge we address in this work. 

Conventional approaches attempt to mitigate the latency of large models through action chunking (Zhao et al., 2023; Black et al., 2024). By predicting long sequences of actions at once, these methods reduce the frequency of expensive inference calls. However, the chunking strategies can impact performance; robots may experience waiting time during inference, and inconsistencies can arise between successive chunks (Liu et al., 2025). To address this, SmolVLA (Shukor et al., 2025) introduces synchronous execution of the policy, and Real Time Chunking (RTC) (Black et al., 2025) ensures smoother continuity between chunks under asynchrony for diffusion-based action generation. However, these methods still assume that the model predicts fixed-length horizons, which means reactivity to new sensory input remains limited. 

Another line of work adopts hierarchical architectures inspired by dual-system reasoning (Kahneman, 2011). Large models serve as a high-level planner (System 2), while smaller policies act as fast executors (System 1). Examples include Hi Robot (Shi et al., 2025), which combines a VLM at the high level with a VLA at the low level, and GR00T-N1 (NVIDIA et al., 2025), which uses a compact policy to refine continuous action chunks. However, since the low-level executor has to wait for predictions from the high-level model, the latency still persists. Consequently, while chunking and hierarchical approaches alleviate some issues, they do not fundamentally solve the challenge of maintaining responsiveness to new observations under the inference delays inherent to VLAs with a large number of parameters. 

To mitigate this problem, in this paper, we propose _Asynchronous Action Chunk Correction (A2C2)_ , which is a lightweight correction head that can be executed at every timestep to complement the outputs of large VLA models. Unlike conventional approaches such as action chunking and asynchronous inference, our method introduces a lower-level correction layer that directly integrates the most recent observation referring to the action chunks that high-level model outputs. This correction head does not compete with base (high-level) policies like diffusion- or VLA-based chunk generators; instead, it enhances them by injecting real-time feedback to maintain responsiveness under inference delays and long horizons. Through this design, the proposed framework achieves robustness against dynamic environmental changes and external disturbances, thereby mitigating the critical latency bottleneck in deploying large-scale VLA models for real-time robotic control. 

2 

In our experiments on the Kinetix tasks, we measure a 35% point increase in success rate over naive execution and 23% point increase over RTC in the presence of delay. For long execution horizons, we measure a 12% point success rate increase over naive execution and 7% point increase over RTC. 

In summary, the contributions of this work are as follows: 

- We first formulated delays in policy inference with VLAs that generate action chunks. 

- A lightweight add-on action correction policy ( _A2C2_ ) is introduced to improve reactivity, which can be applied to any VLA model independent of the underlying architecture. 

- The method showed substantial improvements in success rates on dynamic tasks and robot manipulation benchmarks with varied inference delays. 

## 2 PROBLEM FORMULATION 

We consider an action chunk execution with an imitation learning (IL) policy. As illustrated in Figure 1, an action chunk _At_ = _{at, . . . , at_ + _H−_ 1 _}_ is from IL policy _π_ based on the observation _ot_ and a language instruction _l_ . _H_ is the horizon length, the training sequence length of the IL model _π_ . We assume it uses _e_ steps of the action chunk, and define it as the execution horizon. Policy predicts the action chunk every _e_ steps as follows: 


Also, there is an inference latency. We define the _delay d_ as the number of control steps between receiving an observation _ot_ and obtaining the corresponding action chunk _At_ . Formally, it is computed as 


where _δ_ represents the combined inference and communication time, and ∆ _t_ denotes the duration of a single control step. 

To control delayed, chunked action execution, the agent executes one action per step till a new chunk arrives asynchronously. Additionally, we assume that the policy server can handle only one inference at a time. If the execution horizon _e_ is shorter than the delay _d_ , there will be no action during the model inference, which leads to waiting time. On the other hand, if the execution horizon _e_ is longer than _H − d_ , there is no action remaining during the inference time. Therefore, the execution horizon _e_ needs to be longer than the delay _d_ , and _e_ must be shorter than _H − d_ ( _d ≤ e ≤ H − d_ ). 

In this setting, the agent needs to use the actions that are always based on past observations. Each executed action corresponds to an observation at least _d_ steps old. And in the worst case, the agent may need to execute an action that is generated from the _d_ + _e_ steps past observations. 

## 3 METHOD 

### 3.1 OVERVIEW 

We extend the action chunk–based policy _π_ by _Asynchronous Action Chunking Correction (A2C2)_ , introducing a lightweight **correction head** _πa_ 2 _c_ 2 that refines each action within a predicted chunk using the most recent observation, features of the base policy, and a temporal position feature. This framework enables step-wise online correction without retraining the base policy and is complementary to methods such as RTC (Black et al., 2025). 

At time t, Observation _ot_ is sent to the policy server. Then, the base policy _π_ generates the action chunk _At_ = _{a_<sup>base</sup> _t , . . . , a_<sup>base</sup> _t_ + _H−_ 1<sup>_}_within inference delay</sup><sup>_d_as</sup> 


Subsequently, at time _t_ + _k_ ( _d ≤ k ≤ d_ + _e_ ), time feature _τk_ , and base action _at_ + _k_ , latest observation _ot_ + _k_ , base policy latest representation _zt_ and language instruction _l_ are added to the correction head _πa_ 2 _c_ 2. The positional feature _τk_ is represented by a sinusoidal embedding that provides periodic structure over the chunk length (sin(2 _π H_<sup>_<u>k</u>_)</sup><sup>_,_cos(2</sup><sup>_π_</sup> _H_<sup>_<u>k</u>_)).Thecorrectionheadintegratesthis</sup> information and predicts the residual action ∆ _at_ + _k_ as 


3 


Figure 2: The Base policy _π_ outputs an action chunk _At_ = _{at, . . . , at_ + _H−_ 1 _}_ from the current observation _ot_ . For each step within the chunk, a lightweight correction head refines the corresponding base action _at_ + _k_ using the latest observation _Ot_ + _k_ and a time feature _τk_ indicating the relative position within the chunk. The refined actions _a_<sup>_exec_</sup> _t_ + _k_<sup>mitigate performance degradation under inference</sup> delays _d_ and long horizons _H_ . 


Base policy _π_ infers an action chunk every _e_ steps with _d_ delay. On the other hand, we assume that the model size of the correction head _πa_ 2 _c_ 2 is small enough to run every step, which means the inference time of the head is smaller than the duration of a single control step ∆ _t_ . Refer to Figure 2 for the overview. 

Our method differs from existing approaches for asynchronous inference in the following aspects: 

- **Time-aware correction:** The correction head explicitly conditions on the position within the action chunking VLA using a temporal feature. 

- **Chunk-level smoothness:** By specifying which element of the chunk is being corrected, the method produces smoother corrections across horizons. 

- **Data compatibility:** Training uses the same demonstration datasets as the base VLA policy, which does not require reinforcement learning fine-tuning. 

- **Real-time feedback:** New observations are always incorporated, improving robustness under inference delay in dynamic tasks. 

### 3.2 MODEL TRAINING PROCEDURE 

First, we train the base policy _π_ with the dataset 

_Dbase_ = _{{{ot, at}_<sup>_n_</sup> _t_ =0 _...Tn_<sup>_, ln}n_=1</sup><sup>_...N},_</sup> (6) where _N_ denotes the number of episodes in the dataset. Afterward, we add the output action chunk _A_ ˆ _t_ of the inference from base policy _π_ for each step in the dataset _Dbase_ as 

_A_ ˆ _t_ = _{a_ ˆ _t, ...,_ ˆ _at_ + _H−_ 1 _}_ = _π_ ( _ot, l_ ) _._ (7) 

4 

With these inference results, we created a new dataset for correction head training _Dcor_ as 


_a_ ˆ<sup>_k_</sup> _t−k_<sup>is the k-th action in the action chunk inferred by the base policy from the observation at time</sup> _t − k_ . Then, the Correction head _πa_ 2 _c_ 2 is trained to predict the residual action, i.e., the difference between the target action and the base policy output. The target action is the action in the dataset that was originally collected from expert demonstrations. Formally, given the target action _a_ target and the base policy output _a_ base, the residual target is defined as 


_a_ ˆ is a base action inferred by the base policy. There are some possible combinations of the base action with different time features _τ_ . The predicted residual action is denoted by ∆ _a_ residual. The loss function is the mean squared error (MSE): 


Where _N_ denotes the batch size, i.e., the number of training samples in a mini-batch. 

## 4 EXPERIMENTAL SETUP 

### 4.1 BENCHMARK AND DATASETS 

We use the two simulation environments, Kinetix and LIBERO Spatial, for the experiments. Kinetix is first used for evaluating the performance under highly dynamic manipulation and locomotion tasks. Secondly, we used the LIBERO Spatial benchmark to evaluate the performance as a standard benchmark of robot manipulation. Especially, because Shukor et al. (2025) reports that long-horizon significantly degrades performance in LIBERO Spatial, making the task a natural choice for evaluating robustness under long horizons. 

### 4.1.1 KINETIX 

We used the **Kinetix** , which provides demonstrations across 12 highly dynamic (see Appendix A.1 ). It includes environments ranging from locomotion and grasping to game-like settings. Importantly for our setting, Kinetix contains highly dynamic environments where delayed or inconsistent action generation quickly leads to failure. This makes it a natural testbed for studying the limitations of action chunking and for benchmarking inference-time algorithms such as RTC, which aim to preserve responsiveness and continuity under latency. 

Unlike quasi-static benchmarks, Kinetix environments employ torque- and force-based actuation, making asynchronous inference crucial. Kinetix consists of 12 tasks without language input. 1 million steps data was collected by using expert model. Following RTC experiments, we first train expert policies using RPO (Rahman & Xue, 2022) and a binary success reward. For each environment, 1-million transition dataset is generated with the expert policy. 

### 4.1.2 LIBERO 

LIBERO is a benchmark suite designed to study lifelong robot learning with a focus on knowledge transfer across tasks (Liu et al., 2023). They offer several task suites and datasets. In this work, we specifically use the LIBERO Spatial dataset, which emphasizes spatial reasoning in manipulation tasks as a widely used benchmark for robot manipulation. 

For benchmarking 3D robot manipulation, we used **LIBERO spatial** benchmark, which provides 432 episodes and 52,970 frames across 10 tasks. The dataset consists of multimodal input, including top and wrist RGB images (256 _×_ 256), an 8-dimensional state, and language instructions. 

### 4.2 MODEL TRAINING 

In Kinetix, we used a flow-matching policy as the base model, following prior work on RTC Black et al. (2025). The Correction head network is a 3-layer multilayer perceptron (MLP). The input layer receives the concatenation of the state vector (2722-dim), the base action (6-dim), and the 

5 


Figure 3: Correction head architecture in the Kinetix environment. The MLP takes as input the current state, the base action, and a positional embedding indicating the index within the action chunk. It outputs a residual action that is added to the base action, yielding the refined action. 


Figure 4: Architecture of the proposed Correction head in the LIBERO environment. The base policy is a SmolVLA that produces an action chunk from image, language instruction, and state inputs. A transformer encoder processes the latent representation from smolVLM _zt_ , state _st_ + _k_ , base action _at_ + _k_ , image feature, entire action chunk, time feature _τk_ , and language instruction _l_ to produce a latent representation _et_ + _k_ . A lightweight MLP predicts a residual action∆ _a_<sup>_residual_</sup> _t_ + _k_ , based on the latent representation from the transformer encoder and base action _at_ + _k_ , state _st_ + _k_ , and time feature _τk_ . Then, added to the selected base action to obtain the refined action executed in the environment. 

2-dimensional sinusoidal positional feature. We did not use language instructions or latent representations from base policies, as the model was trained and evaluated separately for each task. Hidden layers have 512 units each with ReLU activation (Nair & Hinton, 2010) and layer normalization (Ba et al., 2016). The output layer produces a 6-dimensional residual vector, which is added elementwise to the base action. The total parameter count is 0.31M. Figure 3 shows the implementation detail for the Kinetix experiment. 

For LIBERO spatial, we adopted SmolVLA (Shukor et al., 2025) (450M parameters) as the base, since it provides competitive performance among VLA models. The correction head consists of a transformer encoder and a lightweight MLP. Visual observations (top and wrist cameras) are encoded into 512-dimensional tokens using a ResNet-18 (He et al., 2016) pretrained on ImageNet (Deng et al., 2009). Language instructions are embedded by the smolVLM encoder provided in the base policy. The base action, latent features of the base policy, and the sinusoidal time embedding are also 

6 


(a) Average Success rate as a function of inference delay _d_ with execution horizon fixed at _e_ = max( _d,_ 1). A2C2 (red) consistently outperforms both naive and real-time baselines, maintaining higher success rates even under large delays. 


(b) Average Success rate as a function of execution horizon _e_ with delay fixed at _d_ = 1. A2C2 (red) remains robust across horizons, while baselines degrade as horizon length increases. 

Figure 5: Overall performance comparison in Kinetix tasks. Each data point averages over 2048 rollouts. Residual correction improves robustness under both increasing inference delay and longer execution horizons. 

projected into 512-dim tokens. All tokens are concatenated and processed by a 6-layer transformer encoder. The pooled embedding, along with the base action and state vector, is passed through a 3-layer MLP (hidden size 512) to predict the residual action. The number of total parameters is 32M. Figure 4 shows the implementation detail for the LIBERO experiment. We also release the source code for both Kinetix and LIBERO experiments. See Appendix A.3 for the details. 

## 5 RESULTS 

### 5.1 KINETIX 

We evaluate the proposed action chunk correction framework in the Kinetix benchmark under varying inference delays _d_ and execution horizons _e_ . Figure 5 reports success rates aggregated across all 12 tasks. There are two baseline comparisons. First is Naive async. This strategy does not pay attention to the previous action chunk at all when generating a new one, naively switching chunks as soon as the new one is ready. Second is RTC. As expected, both the naive async and RTC baselines degrade significantly as either the delay _d_ increases or the horizon _H_ becomes longer. In particular, when _d ≥_ 3, the na¨ıve baseline suffers a sharp drop in success rate due to compounding errors from executing outdated action chunks. RTC inference partially mitigates this issue by overlapping prediction and execution, but performance still declines as the execution horizon increases. 

In contrast, the action chunk correction maintains consistently higher success rates across all settings. Because it refines each action using the most recent observation, the action chunk correction can counteract both the temporal misalignment introduced by inference delay and the drift that accumulates within long action horizons. For example, at delay _d_ = 4, our proposed method achieves nearly 35% higher success than the na¨ıve baseline, and remains above 85% even for horizons _H_ = 7. This demonstrates that real-time correction of action chunks maintains performance both with inference delays and with long-horizon execution. 

### 5.2 LIBERO SPATIAL 

Figure 6 and Table 1 summarize the evaluation on the LIBERO Spatial benchmark. We tested the Na¨ıve async and A2C2 on this setting. Across 10 manipulation tasks with multimodal inputs, the correction head consistently improved success rates over the na¨ıve baseline under both long horizons and injected delays. For example, with execution horizon _H_ = 40 and delay _d_ = 10, the na¨ıve baseline achieved only 67% success, whereas the A2C2 reached 84%. Even when no delay was present, Action chunk correction provided notable gains at long horizons ( _H_ = 50, _d_ = 0), raising success from 72.2% to 81.6%. These results demonstrate that residual refinement by correction head mitigates the degradation caused by outdated action chunks and restores closed-loop 

7 


(a) Success Rate vs Inference Delay _d_ (Execution (b) Success Rate vs Execution Horizon _e_ (Inference Horizon: e=40). A2C2 remains robust under inferDelay: d=0). A2C2 consistently improves perforence delays. mance across horizons. 

Figure 6: Results of LIBERO Spatial: Comparison of Success Rate under different conditions. (a) Effect of inference delay with fixed execution horizon. (b) Effect of execution horizon with no inference delay. Each data point is evaluated on 10 tasks, each with 10 rollouts, resulting in a total of 100 rollouts. 

Table 1: LIBERO Spatial: success rate (%). 50 rollouts per task. Action chunk correction mitigates performance degradation under delay and long horizons. 

|Method|Execution horizon_e_|Delay_d_|Success Rate (%)|
|---|---|---|---|
|Na¨ıve|10|0|81.8|
|A2C2 (Ours)|10|0|**89.2**|
|Na¨ıve|40|10|64.4|
|A2C2(Ours)|40|10|**84.2**|
|Na¨ıve|50|0|72.2|
|A2C2(Ours)|50|0|**81.6**|


responsiveness, enabling large VLA models to maintain high success rates that require fine-grained spatial reasoning. 

## 6 RELATED WORK 

**Imitation learning and VLAs:** Imitation learning (IL) trains agents from demonstrations provided by humans or expert policies, and has been a representative approach in learning robotic control (Osa et al., 2018). Recent advances have introduced generative sequence models to improve consistency and scalability. Diffusion Policy (Chi et al., 2023) utilizes diffusion models for action generation, enabling it to handle the multimodality of data distribution in imitation learning. In parallel, the Action Chunking Transformer (ACT) (Zhao et al., 2023) proposes a transformer-based policy that outputs action chunks rather than single-step actions, producing coherent behaviors while enabling faster inference. In addition, flow-based approaches, such as Flow Policy (Zhang et al., 2024), generate actions by learning continuous transport maps instead of iterative denoising. 

Building on these foundations, a new class of vision–language–action (VLA) foundation models has emerged (Kawaharazuka et al., 2024), including _π_ 0 Black et al. (2024), openVLA Kim et al. (2024), GR00T NVIDIA et al. (2025), and SmolVLA Shukor et al. (2025). These models adopt chunk-based prediction as the de facto standard for inference, similar to ACT (Zhao et al., 2023). Vision–Language–Action (VLA) models achieve broad task generalization by aligning multimodal inputs, but their architectures are considerably larger than diffusion- or transformer-based imitation policies. For instance, _π_ 0 has about 3B parameters and openVLA around 7B, which makes inference latency significant even on modern GPU-accelerated hardware. While these models demonstrate the promise of scaling and multimodal grounding, their computational footprint exacerbates the latency problem in real-time control. 

8 

**Asynchronous chunk execution:** As model sizes increase, inference latency becomes a significant bottleneck, motivating asynchronous policy frameworks. In particular, the SmolVLA (Shukor et al., 2025) proposed a server–client architecture for mitigating inference delays. In this setup, the server receives observations and performs inference with a delay of _d_ control steps (including communication latency), then transmits an action chunk of horizon _H_ to the client. Then, the client executes these actions sequentially. However, because the _d_ delayed actions are not yet available at execution time, the client continues executing actions from the previous chunk until the new chunk arrives. This design ensures continuity but introduces the risk of inconsistency between consecutive chunks. For example, the earlier chunk may predict avoiding an obstacle by moving left, while the newly received chunk may instead suggest moving right. Such mismatches across chunks can cause jerky motion and noticeable performance degradation, especially in dynamic environments. 

To fix the chunk mismatches, Real Time Chunking (RTC) (Black et al., 2025) is proposed. It is an inference-time algorithm that enables smooth asynchronous execution for action-chunking policies by posing chunk switching as an inpainting problem. Specifically, it generates the next action chunk while executing the current one, “freezing” actions guaranteed to execute and “inpainting” the rest. 

**Reducing inference latency:** One natural way to enhance a model’s real-time performance is to reduce its inference time. Streaming Diffusion Policy (Høeg et al., 2024) or Streaming Flow Policy (Jiang et al., 2025) presents a new training procedure that enables faster inference. More generally, optimizations such as model compression (Lin et al., 2024) or memory optimization (Kwon et al., 2023) of models can also improve the inference speeds. However, as long as model scale and communication overhead prevent action generation from being faster than the control step, the challenges highlighted in this work remain unresolved. 

## 7 CONCLUSION 

In this paper, we propose Asynchronous Action Chunk Correction (A2C2), which introduces a lightweight action correction head by augmenting a large base policy, such as VLAs. A2C2 addresses the challenge of preserving reactivity under inference delays and long execution horizons of action chunking policies. The correction head is trained on the same dataset as the base policy and, in principle, can be added to any off-the-shelf VLAs. Our experiments in both the Kinetix simulation suite and the LIBERO Spatial benchmark demonstrated that Asynchronous Action Chunk Correction (A2C2) consistently maintained high success rates, even in settings where na¨ıve or RTC degraded significantly. 

While our approach adds minimal overhead compared to full model inference, further work is needed to validate its scalability to richer language instructions, out-of-distribution settings, and more dynamic tasks beyond those in LIBERO Spatial. Addressing these challenges would broaden the applicability of action chunk correction and strengthen its role as a general mechanism for enhancing reactivity in large policy architectures. 

Recently, Large Language Models (LLMs) and Vision-Language Models (VLMs) have demonstrated improved generality through parameter scaling, as established by neural scaling laws (Kaplan et al., 2020). Since recent VLA policies are built upon these models, it is reasonable to expect that future VLAs will continue to grow in size to support deployment across diverse environments and tasks. Our work can be viewed as a step toward enabling such scaled VLAs to operate in real time without sacrificing responsiveness by introducing a lightweight correction mechanism that mitigates the effects of inference latency. 

Moreover, inference of models with billions of parameters already exceeds the computational capacity of on-board processors on most robotic platforms. In practice, this motivates client–server architectures where the VLA runs on a remote server and the robot queries it over a network. In this setting, by explicitly treating communication delay as part of the inference latency in our formulation, our framework naturally extends to client–server architectures where large VLAs are executed remotely. Thus, our framework provides a pathway to leverage the generalization benefits of largescale VLAs while still maintaining reactivity in real-world deployments, enabling the design of next-generation VLA systems that combine scalability with responsiveness. 

9 

## ETHICS STATEMENT 

This work does not involve human subjects, personally identifiable information, or sensitive data. All experiments were conducted on publicly available datasets. 

## REPRODUCIBILITY STATEMENT 

We provide implementation details and dataset preprocessing in the Appendix, and full hyperparameter settings in the appendix. We released our source code for the experiments below: 

- **Kinetix:** https://github.com/k1000dai/a2c2-kinetix 

- **LIBERO:** https://github.com/k1000dai/a2c2-libero 

## REFERENCES 

Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton. Layer normalization. _arXiv preprint arXiv:1607.06450_ , 2016. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A visionlanguage-action flow model for general robot control, 2024. URL https://arxiv.org/ abs/2410.24164. 

- Kevin Black, Manuel Y. Galliker, and Sergey Levine. Real-time execution of action chunking flow policies, 2025. URL https://arxiv.org/abs/2506.07339. 

- Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, and Li Fei-Fei. Imagenet: A large-scale hierarchical image database. In _2009 IEEE conference on computer vision and pattern recognition_ , pp. 248–255. Ieee, 2009. 

- Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pp. 770–778, 2016. 

- Sigmund H. Høeg, Yilun Du, and Olav Egeland. Streaming diffusion policy: Fast policy synthesis with variable noise diffusion models, 2024. URL https://arxiv.org/abs/2406. 04806. 

- Sunshine Jiang, Xiaolin Fang, Nicholas Roy, Tom´as Lozano-P´erez, Leslie Pack Kaelbling, and Siddharth Ancha. Streaming flow policy: Simplifying diffusion _/_ flow-matching policies by treating action trajectories as flow trajectories, 2025. URL https://arxiv.org/abs/2505. 21851. 

- Daniel Kahneman. _Thinking, Fast and Slow_ . Farrar, Straus and Giroux, New York, 2011. ISBN 9780374275631. 

- Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models, 2020. URL https://arxiv.org/abs/2001.08361. 

10 

- Kento Kawaharazuka, Tatsuya Matsushima, Andrew Gambardella, Jiaxian Guo, Chris Paxton, and Andy Zeng. Real-world robot applications of foundation models: A review. _Advanced Robotics_ , 38(18):1232–1254, 2024. 

- Kento Kawaharazuka, Jihoon Oh, Jun Yamada, Ingmar Posner, and Yuke Zhu. Vision-languageaction models for robotics: A review towards real-world applications. _IEEE Access_ , 13:162467– 162504, 2025. doi: 10.1109/ACCESS.2025.3609980. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model, 2024. URL https://arxiv.org/ abs/2406.09246. 

- Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model serving with pagedattention, 2023. URL https://arxiv.org/abs/2309.06180. 

- Ji Lin, Jiaming Tang, Haotian Tang, Shang Yang, Wei-Ming Chen, Wei-Chen Wang, Guangxuan Xiao, Xingyu Dang, Chuang Gan, and Song Han. Awq: Activation-aware weight quantization for llm compression and acceleration, 2024. URL https://arxiv.org/abs/2306.00978. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning, 2023. URL https://arxiv. org/abs/2306.03310. 

- Yuejiang Liu, Jubayer Ibn Hamid, Annie Xie, Yoonho Lee, Maximilian Du, and Chelsea Finn. Bidirectional decoding: Improving action chunking via guided test-time sampling, 2025. URL https://arxiv.org/abs/2408.17355. 

- Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_ , 2017. 

- Michael Matthews, Michael Beukman, Chris Lu, and Jakob Foerster. Kinetix: Investigating the training of general agents through open-ended physics-based control tasks, 2025. URL https: //arxiv.org/abs/2410.23208. 

- Vinod Nair and Geoffrey E Hinton. Rectified linear units improve restricted boltzmann machines. In _Proceedings of the 27th international conference on machine learning (ICML-10)_ , pp. 807–814, 2010. 

- NVIDIA, Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi ”Jim” Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. URL https://arxiv.org/abs/2503.14734. 

- Takayuki Osa, Joni Pajarinen, Gerhard Neumann, J Andrew Bagnell, Pieter Abbeel, Jan Peters, et al. An algorithmic perspective on imitation learning. _Foundations and Trends® in Robotics_ , 7(1-2): 1–179, 2018. 

- Md Masudur Rahman and Yexiang Xue. Robust policy optimization in deep reinforcement learning, 2022. URL https://arxiv.org/abs/2212.07536. 

- Sebastian Sartor and Neil Thompson. Neural scaling laws in robotics, 2025. URL https:// arxiv.org/abs/2405.14005. 

- Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, Adrian Li-Bell, Danny Driess, Lachy Groom, Sergey Levine, and Chelsea Finn. Hi robot: Open-ended instruction following with hierarchical vision-language-action models, 2025. URL https://arxiv.org/abs/2502. 19417. 

11 

- Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and Remi Cadene. Smolvla: A vision-language-action model for affordable and efficient robotics, 2025. URL https://arxiv.org/abs/2506.01844. 

- TRI LBM Team, Jose Barreiros, Andrew Beaulieu, Aditya Bhat, Rick Cory, Eric Cousineau, Hongkai Dai, Ching-Hsin Fang, Kunimatsu Hashimoto, Muhammad Zubair Irshad, Masha Itkina, Naveen Kuppuswamy, Kuan-Hui Lee, Katherine Liu, Dale McConachie, Ian McMahon, Haruki Nishimura, Calder Phillips-Grafflin, Charles Richter, Paarth Shah, Krishnan Srinivasan, Blake Wulfe, Chen Xu, Mengchao Zhang, Alex Alspach, Maya Angeles, Kushal Arora, Vitor Campagnolo Guizilini, Alejandro Castro, Dian Chen, Ting-Sheng Chu, Sam Creasey, Sean Curtis, Richard Denitto, Emma Dixon, Eric Dusel, Matthew Ferreira, Aimee Goncalves, Grant Gould, Damrong Guoy, Swati Gupta, Xuchen Han, Kyle Hatch, Brendan Hathaway, Allison Henry, Hillel Hochsztein, Phoebe Horgan, Shun Iwase, Donovon Jackson, Siddharth Karamcheti, Sedrick Keh, Joseph Masterjohn, Jean Mercat, Patrick Miller, Paul Mitiguy, Tony Nguyen, Jeremy Nimmer, Yuki Noguchi, Reko Ong, Aykut Onol, Owen Pfannenstiehl, Richard Poyner, Leticia Priebe Mendes Rocha, Gordon Richardson, Christopher Rodriguez, Derick Seale, Michael Sherman, Mariah Smith-Jones, David Tago, Pavel Tokmakov, Matthew Tran, Basile Van Hoorick, Igor Vasiljevic, Sergey Zakharov, Mark Zolotas, Rares Ambrus, Kerri Fetzer-Borelli, Benjamin Burchfiel, Hadas Kress-Gazit, Siyuan Feng, Stacie Ford, and Russ Tedrake. A careful examination of large behavior models for multitask dexterous manipulation. 2025. URL https://arxiv.org/abs/2507.05331. 

- Qinglun Zhang, Zhen Liu, Haoqiang Fan, Guanghui Liu, Bing Zeng, and Shuaicheng Liu. Flowpolicy: Enabling fast and robust 3d flow-based policy via consistency flow matching for robot manipulation, 2024. URL https://arxiv.org/abs/2412.04987. 

- Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware, 2023. URL https://arxiv.org/abs/2304.13705. 

12 

## A APPENDIX 

### A.1 KINETIX SIMULATION DETAIL 

### A.1.1 ENVIRONMENT 

We reused the 12 tasks from the Kinetix benchmark (Matthews et al., 2025) used in the RTC paper Black et al. (2025). A sample visualization of each of the environments is shown in Figure 7. The Kinetix environment has an observation space with 2722 dimensions which do not include any images. Instead, it encodes information about polygons, circles, joints, thrusters, gravity, and the states of motors and thrusters described below. For entities not used in a given task, their corresponding entries are zero-padded. The action space has 6 dimensions. The first four correspond to motor controls, and the last two correspond to thruster controls. For unused actuators, their entries are set to zero via padding. 


Figure 7: Visualization of the 12 tasks from the Kinetix simulation environment. Each subfigure corresponds to one task used in our experiments. 

### A.1.2 DATASET GENERATION AND TRAINING DETAIL 

An imitation learning dataset was required to test the flow policy and our correction head. In the Kinetix simulation, we follow the RTC implementation. First, we trained the expert policy with RPO (Rahman & Xue, 2022) on 8 seeds per task for 64 million environment steps each. For each task, we load the best-performing checkpoint for each seed and discard some seeds if they did not reach a certain success threshold. Then, we used the expert model to generate 1 million environment steps for each task. After that, we train the flow policy with the generated dataset. We saved the checkpoints for each, but used the last checkpoint for the evaluation. 

13 

Table 2: Training hyperparameters for the Kinetix flow policy. 

|Hyperparameter|Value|
|---|---|
|Learning rate|3_×_10<sup>_−_4</sup>|
|Gradient norm clip|10_._0|
|Weight decay|1_×_10<sup>_−_2</sup>|
|Warmup steps|1000|
|Batch size|512|
|Number of epochs|32|


Table 3: Training hyperparameters for the Kinetix Correction head. 

|Hyperparameter|Value|
|---|---|
|Batch size|512|
|Number of epochs|16|
|learning rate|1_×_10<sup>_−_4</sup>|
|weight decay|1_×_10<sup>_−_3</sup>|
|Gradient norm clip|5_._0|
|Warmup steps|500|


The correction head is then trained with the flow policy. The correction policy requires the base action from the base policy, so at every step, we infer the action chunk from the base policy and use it and the dataset to train the correction head. During the base flow policy training, we used a constant learning rate and added some warmup state. See Table 2 for more details on the settings. For the Correction Head training, we used the parameters shown in Table 3. In both the flow policy and A2C2 training, the AdamW optimizer (Loshchilov & Hutter, 2017) was used. 

### A.1.3 EVALUATION DETAILS 

In the evaluation, we rolled out 2048 per task and computed the success rate for different delays and execution horizon lengths. In the Kinetix simulation, we tested all combinations of delay and execution horizons compatible with the chosen action chunk size. All results are in Table 4. 

### A.2 LIBERO SIMULATION DETAIL 

### A.2.1 ENVIRONMENT 

LIBERO Spatial consists of 10 tasks. We evaluated all tasks, and the corresponding language instructions are listed below. The language instructions are: 

1. pick up the black bowl between the plate and the ramekin and place it on the plate 

2. pick up the black bowl next to the ramekin and place it on the plate 

3. pick up the black bowl from the table center and place it on the plate 

4. pick up the black bowl on the cookie box and place it on the plate 

5. pick up the black bowl in the top drawer of the wooden cabinet and place it on the plate 

6. pick up the black bowl on the ramekin and place it on the plate 

7. pick up the black bowl next to the cookie box and place it on the plate 

8. pick up the black bowl on the stove and place it on the plate 

9. pick up the black bowl next to the plate and place it on the plate 

10. pick up the black bowl on the wooden cabinet and place it on the plate 

14 

Table 4: Kinetix: success rate (percent) under different execution horizons ( _e_ ) and inference delays ( _d_ ). 10 tasks and 10 rollouts per task. Residual correction consistently improves over the na¨ıve baseline. The first, second, and third row of each cell denote the success rate of Na¨ıve, RTC (Black et al., 2025), and A2C2(Ours), respectively. 

||||E|xecution|Horizon (_e_|)|||
|---|---|---|---|---|---|---|---|---|
|Delay (_d_)|1|2|3|4|5|6|7|8|
||90.8|90.4|89.8|88.9|88.1|87.4|86.6|86.0|
|0|90.9|90.0|89.2|88.6|87.5|86.6|86.3|86.0|
||90.3|89.5|89.6|88.9|88.8|88.9|88.2|87.8|
||78.1|83.7|82.6|80.9|78.5|77.4|75.7||
|1|88.2|87.5|86.3|84.8|83.1|81.1|80.2|-|
||89.5|88.8|88.4|88.3|87.9|87.3|87.8||
|||75.7|72.7|70.1|67.3|66.4|||
|2|-|84.1|81.4|79.3|76.4|74.8|-|-|
|||87.4|87.5|87.5|87.1|86.6|||
||||59.3|59.5|56.5||||
|3|-|-|74.8|71.0|67.5|-|-|-|
||||87.4|87.2|86.0||||
|||||51.2|||||
|4|-|-|-|62.9|-|-|-|-|
|||||86.5|||||


### A.2.2 DATASET AND TRAINING DETAIL 

We used the LIBERO Dataset with the LeRobot dataset format available on Huggingface and we used the LeRobot framework to read the dataset. LeRobot also has a well-organized training pipeline and makes it easy to create and try new architectures. 

First, we trained SmolVLA as a base policy. There is an option for training the policy from scratch or fine-tuning the pretrained model. In our setting, we chose the training from scratch because SmolVLA is pretrained mainly with S0-101, which is a different embodiment from the Franka arm used in the LIBERO benchmark. 

In the Kinetix simulation, the base policy predicts the action chunk every time in the correction head training. However, it is too time-consuming with a large VLA model. Then, we added the inference result of SmolVLA on the dataset for training the correction head. The new dataset has all the LIBERO Spatial data, the action chunk result, and the VLM latent representation from the SmolVLA policy for each step. 

After that, we trained the correction head with the dataset we created. For SmolVLA training, we trained a model from scratch with a cosine learning scheduler, which is the default setting for SmolVLA training. The parameter for SmolVLA training is in Table 5 

For Correction head training, we use a constant learning rate of 1e-5. High learning rates, such as 1e-4, do not work well for the Correction head training. See Table 6 

In both SmolVLA and Correction head training, the AdamW optimizer was used (Loshchilov & Hutter, 2017). 

### A.2.3 EVALUATION DETAIL 

For the evaluation, we tested various combinations of delay steps and horizon steps first. We tested 10 rollouts per task, and LIBERO Spatial has 10 tasks. Then, to evaluate more precisely, we select 3 pairs of delay and horizon, (0,10), (10,40), (0,50), and rollouts 50 per task. All results for LIBERO Spatial are shown in Table 7. 

15 

Table 5: Training hyperparameters for LIBERO with SmolVLA. 

|Hyperparameter|Value|
|---|---|
|Learning rate|1_×_10<sup>_−_4</sup>|
|Scheduler|Cosine|
|Warmup steps|1000|
|Decay steps|30000|
|Minimum learning rate|2_._5_×_10<sup>_−_6</sup>|
|Batch size|64|
|Training steps|100000|
|Optimizer_ϵ_|1_×_10<sup>_−_8</sup>|
|Optimizer weight decay|1_×_10<sup>_−_10</sup>|
|Gradient norm clip|10|


Table 6: Training hyperparameters for LIBERO Correction head. 

|Hyperparameter|Value|
|---|---|
|Learning rate|1_×_10<sup>_−_5 </sup>(constant)|
|Batch size|64|
|Training steps|200000<br>|
|Optimizer weight decay|1_×_10<sup>_−_5</sup>|
|Model dimension|512|
|Number of heads|8|
|Number of encoder layers|6|


### A.3 SOURCE CODE FOR EXPERIMENTS 

To facilitate reproducibility, we have released the source code for our experiments: 

- **Kinetix:** https://github.com/k1000dai/a2c2-kinetix 

- **LIBERO:** https://github.com/k1000dai/a2c2-libero 

### A.4 COMPUTATIONAL RESOURCES 

We trained both models on NVIDIA RTX A6000 and H200 GPUs. Training in Kinetix required about 20 minutes per task on A6000, while LIBERO residual training (200k steps) took about 4 hours on H200. 

### A.5 INFERENCE TIME COMPARISON 

We benchmarked the average inference time per step for SmolVLA (450M parameters) and our Correction head (32M parameters) over 100 trials each. All measurements were performed on an NVIDIA RTX 5080 laptop GPU (16GB VRAM). 

The results confirm that the correction head is significantly faster, with an average step time of 0 _._ 0047s compared to SmolVLA’s 0 _._ 101s. This _∼_ 20 _×_ speed difference highlights that the proposed correction head can be integrated into high-frequency control loops without introducing prohibitive overhead, while still preserving the benefits of large foundation models at the chunk level. 

A.6 THE USE OF LARGE LANGUAGE MODELS 

We used Large Language Models to polish our writing. 

16 

Table 7: LIBERO Spatial: success rate under different execution horizons and inference delays. 10 tasks and 10 rollouts per task. Residual correction consistently improves over the na¨ıve baseline. 

|Execution Horizon|Inference Delay_d_|Na¨ıve|A2C2 (Ours)|
|---|---|---|---|
|40|10|0.67|0.84|
|40|5|0.66|0.86|
|40|3|0.65|0.86|
|40|1|0.74|0.83|
|10|10|0.75|0.88|
|10|5|0.82|0.92|
|10|3|0.81|0.89|
|10|1|0.83|0.92|
|50|0|0.71|0.84|
|40|0|0.79|0.89|
|30|0|0.79|0.89|
|10|0|0.85|0.87|
|5|0|0.83|0.85|
|1|0|0.77|0.84|


Table 8: Average inference time per step (seconds). 100 trials. 

|Model|Avg. Inference Time|
|---|---|
|SmolVLA (base policy)|101 msec|
|Correction head (Ours)|4.7 msec|


17 

