---
title: "Learning Native Continuation for Action Chunking Flow Policies"
date: "2026-02-13"
authors: "Yufeng Liu; Hang Yu; Juntu Zhao; Bocheng Li; Di Zhang; Mingzhu Li"
url: https://arxiv.org/abs/2602.12978
pdf: https://arxiv.org/pdf/2602.12978
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.12978)** / [論文ページ](https://arxiv.org/abs/2602.12978)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Learning Native Continuation for Action Chunking Flow Policies 

Yufeng Liu<sup>1,2</sup> , Hang Yu<sup>2,4</sup> , Juntu Zhao<sup>1,2</sup> , Bocheng Li<sup>2,5</sup> , Di Zhang<sup>2,4</sup> , Mingzhu Li<sup>2</sup> , Wenxuan Wu<sup>2</sup> , Yingdong Hu<sup>3</sup> , Junyuan Xie<sup>2</sup> , Junliang Guo<sup>2‡</sup> , Dequan Wang<sup>1†</sup> , Yang Gao<sup>2,3†</sup> 

> 1Shanghai Jiao Tong University 

> 2Spirit AI 3Tsinghua University 

> 4Tongji University 5University of Science and Technology of China 

Project page: lyfeng001.github.io/Legato/ 

**_Abstract_ —Action chunking enables Vision Language Action (VLA) models to run in real time, but naive chunked execution often exhibits discontinuities at chunk boundaries. Real-Time Chunking (RTC) alleviates this issue but is external to the policy, leading to spurious multimodal switching and trajectories that are not intrinsically smooth. We propose Legato, a trainingtime continuation method for action-chunked flow-based VLA policies. Specifically, Legato initializes denoising from a scheduleshaped mixture of known actions and noise, exposing the model to partial action information. Moreover, Legato reshapes the learned flow dynamics to ensure that the denoising process remains consistent between training and inference under per-step guidance. Legato further uses randomized schedule condition during training to support varying inference delays and achieve controllable smoothness. Empirically, Legato produces smoother trajectories and reduces spurious multimodal switching during execution, leading to less hesitation and shorter task completion time. Extensive real-world experiments show that Legato consistently outperforms RTC across five manipulation tasks, achieving approximately 10% improvements in both trajectory smoothness and task completion time.** 


## I. INTRODUCTION 

Action chunking [20] has become a widely adopted strategy for deploying large Vision Language Action (VLA) models in real-world robotic systems [7, 19, 37–43, 46]. By predicting sequences of action vectors, chunking amortizes inference cost and enables high-frequency control. However, naive chunked execution introduces a fundamental drawback: due to inference delay and the intrinsic multimodality of flow-based policies [24], transitions between consecutive chunks are often not smooth, leading to visible discontinuities during execution. 

Real-Time Chunking (RTC) [8] was proposed to mitigate this issue by applying inference-time inpainting [29, 32] that partially constrains newly generated action chunks to previously generated actions in their overlapping regions. While RTC improves continuity compared to naive chunked execution, its continuation mechanism is applied only at inference time and is not learned as part of the policy. As a result, the policy is prone to spurious multimodal switching across chunk boundaries and producing trajectories that are not intrinsically smooth. Spurious multimodal switching often manifests as hesitation and abrupt direction changes, resulting in prolonged task completion time, as shown in fig. 1. 

> This work was done during the internship at Spirit AI. 

> † Corresponding authors. ‡ Project leader. 

Fig. 1. Legato reduces task completion time while improving trajectory smoothness compared to RTC [8]. Across five real-world manipulation tasks, Legato consistently achieves shorter execution time and lower NSPARC [2] (indicating smoother trajectories, discussed in section IV-A2) than RTC. The bottom plot shows an example execution trace on the _pour_ task, as defined in section IV-A1, where Legato produces smoother action trajectories with fewer hesitation-induced slowdowns than RTC. 

In this work, we argue that stable chunked execution requires chunk continuation to be a native, learned property of the policy. Achieving this entails two requirements: **(i) perstep guidance** , where guidance is applied repeatedly across denoising steps, and **(ii) training-inference consistency** . We propose Legato, a training-time continuation mechanism for action-chunked flow-based VLA policies. Rather than learning the canonical flow-matching velocity field [6, 24] and relying on inference-time correction, Legato internalizes chunk-tochunk continuation into the learned denoising dynamics. 

To satisfy requirement _per-step guidance_ , we first define a guidance schedule that specifies how strongly each timestep should adhere to the guidance actions. Unlike Training-time RTC [9], which enforces continuation via a hard clamp on the prefix, Legato uses a smooth schedule: it anchors the beginning of the chunk to known actions and gradually ramps 


Fig. 2. Overview of Legato with schedule-shaped continuation dynamics. The schedule parameters are defined as follows: _s_ is the executed length per cycle, _d_ sets the fully guided prefix (inference delay), and _r_ controls the ramp-down length of the guidance schedule over the remaining horizon. Given **_ω_** , Legato initializes actions via an action–noise mixture and learns a reshaped velocity field so that the native schedule effect is realized during multi-step denoising. 

the guidance strength down to zero. During training, the known actions are the ground-truth of the same chunk [8]. During inference, the known actions correspond to the overlapping prefix of the previously generated chunk. This scheduleshaped design provides fine-grained control over the continuity strength between adjacent chunks. 

With the schedule-shaped guidance, we enforce requirement _training-inference consistency_ under per-step guidance. At inference time, action generation proceeds through multiple denoising steps, and empirically proved by section III-B, effective continuation requires per-step guidance before every denoising step. 

Training-time RTC [9] achieves this by hard-fixing the executed prefix and learning to denoise only the remaining horizon. In contrast, Legato trains the policy to generate the entire chunk under per-step, schedule-shaped guidance by reshaping the velocity field. This yields strict traininginference consistency, as shown in fig. 2. 

To make the above dynamics usable in real-world deployments, we account for variations in inference latency and desired continuation strength. In real-world deployment, inference latency can vary across hardware and runtime optimizations [8]. Under a fixed guidance schedule, such variations lead to mismatched overlap regions and require retraining to maintain consistent behavior. At the same time, we may want to adjust the schedule (i.e., ramp length) to control how strongly continuation is enforced. To handle both factors, we randomize the schedule parameters during training and condition the policy on the resulting schedule, so the same model can adapt to different latencies and ramp lengths. 

We evaluate Legato extensively in real-world environments to assess the necessity of learning action continuation as part of the policy dynamics. We consider five diverse robotic manipulation tasks. Across all settings, Legato consistently produces 

smoother trajectories and achieves significantly shorter task completion time by suppressing spurious multimodal switching compared to RTC, as shown in fig. 1. Additional ablation studies further validate the robustness of Legato across different guidance schedules, VLA models, and conditioning strategies, demonstrating that its learned continuation behavior generalizes well under varying inference conditions. 

Our work offers three main contributions: 

- We propose Legato, a training-time continuation framework that enables per-step, schedule-shaped guidance while maintaining strict training-inference consistency by reshaping the flow dynamics of action-chunked policies. 

- We introduce randomized schedule conditioning to support varying inference delays and to provide flexible control over trajectory smoothness. 

- Extensive real-robot experiments across five manipulation tasks show that Legato consistently outperforms RTC and training-time RTC, producing smoother trajectories and shorter task completion time. 

II. RELATED WORKS 

## _A. VLA and Action Chunking Methods_ 

Recent Vision Language Action (VLA) models couple large vision–language representations with learned heads to enable end-to-end visuomotor policies [5–7, 11, 22, 25, 33–35, 44, 45]. Most VLA systems generate actions in chunks, predicting a sequence of future controls per inference step [30, 35, 42]. Action chunking has been successfully combined with a variety of generative policy formulations, including diffusionbased [3, 13, 14, 21, 27, 36, 38], flow-based [6, 7, 10, 23], and discrete action representations [4, 28]. However, chunked execution trades off responsiveness for smoothness [8], and inference latency further increases discontinuities between successive chunks, motivating methods to improve continuation. 

## _B. Trajectory Continuation in Learned Policies_ 

Building on action chunking, a common approach to improve responsiveness is asynchronous execution, where action generation overlaps with execution [31, 43]; however, without explicit continuation constraints, independently generated chunks can exhibit abrupt multimodal switches at their boundaries. Bidirectional decoding (BID) [26] uses rejection sampling to keep continuity across chunks. Real-time chunking (RTC) [8] addresses continuation under asynchronous inference by conditioning new action chunks on previously issued actions that are guaranteed to execute. While RTC effectively mitigates boundary artifacts caused by inference latency, it is an inference-time mechanisms, leaving open the question of how to induce robust trajectory continuation without additional test-time intervention. 

## _C. Conditioning in Diffusion- and Flow-Based Policies_ 

Recent diffusion- [16] and flow-based [24] policies explore conditioning mechanisms to improve temporal coherence and execution efficiency. Diffusion Forcing [12] and Fast Policy Synthesis with Variable Noise Diffusion Models [17] adopt a timestep-level diffusion formulation, generating a single action per inference step and improving reactivity through noise modulation, but without explicitly modeling continuation across action chunks. Rolling Diffusion Policy [18] similarly operates at the timestep level, incrementally refining future actions via rolling denoising to enhance temporal awareness. In contrast, SAIL [1] performs chunk-level conditioning by leveraging overlapping actions between consecutive chunks using classifier-free guidance [15], which mitigates discontinuities under fast execution but provides only soft alignment and limited control over continuation strength. Concurrent with our work, training-time RTC [9] introduces continuation during training by conditioning on a hard action prefix that simulates inference delay. While this exposes the policy to prefix-based continuation, the conditioning remains an external constraint and does not account for the effective denoising dynamics induced by repeated, schedule-shaped guidance at inference time, leaving continuation outside the learned policy dynamics. 

## III. METHODOLOGY 

## _A. Preliminaries_ 

We consider Vision Language Action (VLA) policies that generate action sequences in fixed-length chunks using flowbased generative models. Let **A** _∈_ R<sup>_H×Da_</sup> denote a groundtruth action chunk of horizon _H_ , where _Da_ is the action dimension, and let **_ϵ_** _∼N_ ( **0** _,_ **I** ) denote Gaussian noise of the same shape. Flow matching (FM) [24] constructs a continuoustime interpolation between noise and action, and trains a neural velocity field to transport samples along this path. 

_1)_ **_Flow matching_** _:_ Given a time variable _t ∈_ [0 _,_ 1], standard flow matching defines the interpolation 


Fig. 3. Continuous chunk execution and guidance construction: _d_ (full guidance), _r_ (ramp-down), _s_ (executed length), _r_ + _s_ + _d_ = _H_ . 

and supervises the model to predict the corresponding velocity field 


At inference time, action generation begins from an initial noise sample **_ϵ_** and progressively transforms it into an action chunk by integrating the learned velocity field from _t_ = 0 to _t_ = 1. 

_2)_ **_Real-Time Chunking_** _:_ Real-Time Chunking (RTC) [8] enforces continuity between successive action chunks through a test-time guidance mechanism inspired by inpainting, which encourages partial agreement with previously generated actions. 

Beyond continuity, RTC also introduces an asynchronous execution scheme that overlaps inference and action execution to mitigate model latency. For an action chunk of horizon _H_ , the first _d_ timesteps correspond to inference latency, during which the robot continues executing the previous chunk. The next _s_ timesteps correspond to the portion of the current chunk that will be executed before the next inference completes. Once ( _s − d_ ) timesteps of this portion have been executed, inference for the next chunk is triggered while execution continues, enabling overlapped computation and control. 

RTC further employs a structured guidance schedule over the chunk horizon. The initial _d_ timesteps receive full guidance to strictly enforce continuity with past actions, followed by a ramp-down phase. Let _r_ denote the length of this ramp; the schedule commonly satisfies 


This design enforces strong adherence to previously executed actions near the chunk boundary while gradually relaxing constraints toward the end of the horizon. 

Our method draws inspiration from RTC in both its use of previously executed actions and its structured guidance scheduling, as shown in fig. 3, green regions indicate actual execution. 

## _B. Why per-step guidance matters?_ 

We aim to learn a policy that remains strictly consistent between training and inference. To satisfy this requirement, guidance must be incorporated during training. Under the standard FM formulation, training optimizes the velocity field that transports samples from an initial noise to the groundtruth action. The only inference strategy that remains strictly consistent with training is to apply guidance only once at initialization and then perform multi-step denoising. 


Fig. 4. One-shot prefix guidance cannot preserve prefix constraints during denoising. Trajectories show three dimensions of the overlap (prefix) actions across denoising steps; colors indicate diffusion times _t_ (from 1 to 0), and GT denotes the ground-truth prefix. Although clamped at initialization, the overlap actions drift from the reference as denoising proceeds, motivating the need for per-step guidance. Evaluated on the _pour_ task, as defined in section IV-A1. 

To verify whether the one-shot guidance is enough for continuous guidance, we trained a flow policy where the standard noise initialization was replaced with a prefix-guided variant **_ϵ_**<sup>_′_</sup> . Let **m** _∈{_ 0 _,_ 1 _}_<sup>_H_</sup> denote a horizon-wise mask for the overlap region, and let **A** ref be the ground-truth reference actions on this overlap. We construct the guided noise: 


where _⊙_ denotes element-wise multiplication. Training follows standard flow matching, but with **_ϵ_**<sup>_′_</sup> as the start point: 


During inference, we apply the same prefix clamp only at initialization, **X** 0 = **_ϵ_**<sup>_′_</sup> , and then perform standard multi-step denoising without any intermediate guidance. 

However, empirical results reveal that one-shot guidance is insufficient for continuous guidance. As the denoising process iterates, the overlap region in the generated chunk progressively deviates from the reference actions as shown in fig. 4 (details are shown in the appendix). The prefix part moves away from the desired constraint without repeated guidance. 

This study leads to a crucial conclusion: **effective continuation requires per-step guidance.** However, simply applying per-step guidance on the standard FM remains inconsistent with the training objective. This dilemma motivates Legato: we reshape the flow dynamics during training so that the model can support per-step, schedule-shaped guidance while remaining fully consistent with the training objective. 

## _C. Native Continuation for Action Chunk Generation_ 

We aim to make action continuation a _native property_ of the learned policy. This entails two requirements: **(i) per-step guidance** as discussed in section III-B, where guidance is applied repeatedly across denoising steps, and **(ii) traininginference consistency** . 

Accordingly, we first construct a schedule-shaped training path, then derive the induced guided dynamics, and finally reshape the velocity field to eliminate the train-test mismatch. 

_1)_ **_Action-noise mixture_** _:_ To incorporate guidance into training, we introduce a horizon-wise continuation vector **_ω_** _∈_ [0 _,_ 1]<sup>_H_</sup> , which encodes the guidance schedule over the chunk horizon, i.e., full guidance near the chunk beginning and a gradual ramp-down toward the end of the horizon. 

**Algorithm 1** Legato: Training and Inference 


21: **end if** 

Using **_ω_** , we define an action-noise mixture 


where _⊙_ denotes element-wise multiplication and **_ϵ_** eff represents the _effective noise initialization_ induced by continuation guidance, interpolating between the action chunk and pure noise in a horizon-wise manner. 

Based on this mixture, we construct the interpolation path 


which reduces to the standard flow-matching path when **_ω_** = **0** and collapses to the action chunk for all _t_ when **_ω_** = **1** . 

The corresponding flow-matching velocity is 


reflecting a horizon-wise modulation of the FM velocity. 

**Multimodal persistence and smoothness:** Eq. (8) reveals a _schedule-shaped_ velocity: the target transport magnitude is modulated by **_ω_** . In timesteps with large **_ω_** _i_ (strong continuation), the effective _u_<sup>FM</sup> _i_ is suppressed as _u_<sup>FM</sup> _i ∝_ (1 _−_ **_ω_** _i_ ), making the overlap and the ramp region intrinsically less mutable than the none-guidance region during denoising. This discourages frequent switching among competing action modes in highly multimodal tasks. 

Moreover, since **_ω_** decreases from 1 along the horizon, the effect of continuation is gradually relaxed through a ramp, yielding a smooth transition from strict guidance to free generation. As a result, Legato reduces chunk-boundary 

discontinuities and improves trajectory smoothness. 

_2)_ **_Effective dynamics of repeated continuation guidance_** _:_ The velocity construction above specifies the schedule-shaped guidance. At inference time, continuation requires per-step guidance to keep effective. We therefore derive the exact dynamics induced by the per-step guidance. 

At each denoising step _k_ , the current noisy action is first guided toward the reference action according to the guidance schedule **_ω_** : 


where **A** denotes the reference action and **X** _k_ is the current noisy action before guidance. 

We then perform one denoising update: 


after which the same guidance in eq. (9) is applied again at the next step, as shown in fig. 2. 

Eliminating **X** _k_ yields the exact recurrence 

**Y** _k_ +1 = **_ω_** _⊙_ **A** +( **1** _−_ **_ω_** ) _⊙_ **Y** _k_ +( **1** _−_ **_ω_** ) _⊙_ ∆ _t fθ_ ( **Y** _k, tk_ ) _._ (11) 

Taking the continuous-time limit, this recurrence corresponds to the ordinary differential equation 


Importantly, eq. (12) is not an approximation: it is the exact continuous-time system whose Euler discretization reproduces repeated continuation guidance. 

_3)_ **_Training-inference consistency_** _:_ Having characterized the dynamics induced by per-step guidance, we now turn to the second requirement: training-inference consistency. Standard flow matching supervises the velocity field **u**<sup>FM</sup> , whereas inference with repeated continuation guidance follows the dynamics in eq. (12). To eliminate this mismatch, we require the executed velocity field to coincide with the flow-matching target: 


Solving eq. (13) for _fθ_ yields the _Legato velocity field_ 


where the inverse is taken element-wise. 

Substituting eq. (7) and eq. (8) into eq. (14), we obtain a closed-form target velocity 


The network is trained by regressing _fθ_ ( **Y** _t, o, t,_ **_ω_** ) to **v** target. Thus, Legato preserves the geometric direction of standard flow matching while reshaping the velocity magnitude to internalize continuation dynamics. 

**Inference:** At inference time, we use the previously generated (but haven’t been executed) chunk as the reference for continuation. We construct a reference action chunk **A** ref from the previous prediction using the alignment procedure as 


Fig. 5. Real-world evaluation tasks on a dual-arm robot. We consider five manipulation tasks (stack bowls, pour things, pick and place, fold towel and open drawer) covering diverse motion patterns and multimodal choices such as alternative grasp goals and left/right arm selection. 

shown in algorithm 1. We then instantiate the guidance term in eq. (12) by setting **A** _←_ **A** ref . Given a schedule **_ω_** , we initialize 


We integrate eq. (12) forward in time from _t_ = 0 to _t_ = 1 using the learned velocity field in eq. (14), with the same discretization (number of denoising steps _N_ ) as used during training. This enable the strict training-inference alignment. 

## _D. Schedule Randomization and Conditioning_ 

In our framework, the continuation schedule over an action chunk of horizon _H_ is fully specified by two scalar parameters: the inference delay _d_ and the ramp length _r_ . Given ( _d, r_ ), the guidance schedule **_ω_** _∈_ [0 _,_ 1]<sup>_H_</sup> is uniquely determined, consisting of a full-guidance prefix of length _d_ followed by a ramp part of length _r_ . 

In real-world deployment, effective inference delay varies across hardware platforms, model sizes, and inference optimizations. To account for this variability while enabling flexible control over continuation smoothness, we randomize ( _d, r_ ) during training, thereby exposing the policy to a diverse family of guidance schedules. 

When training with randomized schedules, the policy must be informed of the schedule at inference time. We therefore explicitly condition the action decoder on the schedule. Concretely, if the noisy action **Y** _t ∈_ R<sup>_H×Da_</sup> , where _Da_ denotes the action dimension, we append the guidance schedule along the feature dimension, resulting in an noisy action of shape ( _H, Da_ + 1). At inference time, adapting to a new continuation regime only requires changing the guidance schedule **_ω_** , without retraining the model. Empirically, this schedule conditioning substantially improves robustness across hardware platforms and inference budgets. 

IV. EXPERIMENTS 

## _A. Experimental Setups_ 

_1)_ **_Tasks and Environments_** _:_ We evaluate our method on five real-world manipulation tasks: (i) stack the bowls, (ii) pour 

TABLE I 

MAIN REAL-WORLD RESULTS COMPARING RTC AND LEGATO ACROSS FIVE TASKS. WE REPORT TASK SCORE ( _↑_ ), COMPLETION TIME IN SECONDS ( _↓_ ), AND SMOOTHNESS METRICS ( _↓_ ): NLDLJ (NEGATIVE LOG DIMENSIONLESS JERK [1, 2]), NSPARC (NEGATIVE LINEAR AND ANGULAR SPECTRAL ARC LENGTH [1, 2]), AND OVERLAP RMSE (ROOT MEAN SQUARED ERROR, _×_ 10<sup>3</sup> ). VALUES ARE REPORTED AS MEAN _±_ STANDARD ERROR. 

|**Task**<br>**Score** _↑_<br>**Completion Time (s)** _↓_<br>**Smoothness** _↓_<br>**NLDLJ** _↓_<br>**NSPARC** _↓_<br>**Overlap RMSE** (_×_10<sup>3</sup>) _↓_|
|---|
|RTC<br>Legato<br>RTC<br>Legato<br>RTC<br>Legato<br>RTC<br>Legato<br>RTC<br>Legato|
|Bowls<br>8.68 _±_ 0.35<br>**9.08** _±_ **0.33**<br>52.88 _±_ 3.54<br>**42.66** _±_ **2.68**<br>36.00 _±_ 0.34<br>**35.86** _±_ **0.38**<br>1.82 _±_ 0.04<br>**1.63** _±_ **0.02**<br>6.83 _±_ 0.50<br>**4.58** _±_ **0.17**<br>Pour<br>9.34 _±_ 0.18<br>**9.72** _±_ **0.13**<br>95.07 _±_ 2.86<br>**75.73** _±_ **1.51**<br>39.82 _±_ 0.15<br>**39.50** _±_ **0.13**<br>2.85 _±_ 0.24<br>**1.65** _±_ **0.08**<br>7.64 _±_ 0.70<br>**5.14** _±_ **0.17**<br>PickPlace<br>9.47 _±_ 0.15<br>**9.53** _±_ **0.12**<br>35.53 _±_ 1.24<br>**30.37** _±_ **0.65**<br>34.42 _±_ 0.18<br>**34.34** _±_ **0.14**<br>2.10 _±_ 0.08<br>**1.89** _±_ **0.05**<br>10.17 _±_ 0.66<br>**5.98** _±_ **0.40**<br>Drawer<br>9.20 _±_ 0.16<br>**9.50** _±_ **0.13**<br>25.97 _±_ 0.74<br>**21.80** _±_ **0.72**<br>32.73 _±_ 0.13<br>**28.55** _±_ **0.26**<br>2.24 _±_ 0.05<br>**1.99** _±_ **0.08**<br>12.11 _±_ 0.66<br>**11.74** _±_ **0.55**<br>Towel<br>7.33 _±_ 0.62<br>**8.17** _±_ **0.56**<br>25.93 _±_ 0.98<br>**20.00** _±_ **0.78**<br>32.79 _±_ 0.20<br>**32.43** _±_ **0.24**<br>2.17 _±_ 0.07<br>**1.97** _±_ **0.05**<br>11.28 _±_ 0.55<br>**6.22** _±_ **0.66**|
|**_RTC_**<br>**_Grasp Goal_**<br>**_Changing_**<br>**_Execution Arm_**<br>**_Changing_**<br>**_Grasp Goal_**<br>**_Changing_**|
|**_Legato_**<br>**_More Stable Goal and Execution Arm_**|


Fig. 6. Legato suppresses spurious multimodal switching across chunk boundaries. In a representative bowl-stacking rollout, RTC alternates (arrow) between competing grasp goals (green circle) and execution arms (red circle) over successive chunks, producing visibly hesitant corrections. Legato preserves a consistent grasp goal and arm choice (blue circle), leading to steadier progress. 

things into the bowl, (iii) put all the items into the box, (iv) fold the towel, and (v) open the drawer, as shown in fig. 5. These tasks jointly test different action patterns (e.g., rotation- or translation-dominant motions) and multimodal action selection (e.g., multiple valid grasp goals or the choice of different arms for execution). All tasks are evaluated with a fixed time cutoff of 120 s. Details are provided in the appendix. 

_2)_ **_Evaluation Metrics_** _:_ The following evaluation metrics are used to assess real-world experimental performance. 

**Task completion score.** Each rollout is assigned a taskspecific completion score based on task progress and failure cases (e.g., partial success, object drops, or incorrect actions). Higher scores indicate better task completion. 

**Task completion time.** We measure the total time required to complete each task. This metric reflects the execution efficiency of the policy, capturing delays caused by hesitation or spurious action switching during real-world execution. 

**Trajectory smoothness metrics.** Following prior work on action smoothness, we evaluate smoothness on the model output commands rather than robot executed states. This decouples model behavior from low-level controller performance. Specifically, we report three smoothness-related metrics that capture complementary aspects of trajectory quality [1, 2]: 

- **Negative SPARC (NSPARC)** , where SPARC [1, 2] (Linear and Angular Spectral Arc Length) measures the smoothness of the velocity profile in the frequency domain over the _entire trajectory_ . Lower values of NSPARC 

indicate smoother global speed modulation with reduced high-frequency fluctuations. 

- **Negative LDLJ (NLDLJ)** , where LDLJ [1, 2] (Log Dimensionless Jerk) quantifies high-order geometric smoothness by integrating squared jerk over the _entire trajectory_ . Lower NLDLJ correspond to reduced overall jerk energy and smoother motion at a global level. 

- **Chunk-overlap RMSE** , computed over the overlapping delay segment between consecutive action chunks, which evaluates _local trajectory continuity_ at chunk connections rather than global smoothness. 

Except for the task completion score, lower values indicate better performance for all metrics. Details of all metrics are provided in the appendix. 

_3)_ **_Models and Training Protocol_** _:_ We compare the RTC baseline and our proposed Legato method under a strictly controlled setting. Both methods are initialized from the same _π_ 0 _._ 5 pretrained checkpoint, trained on identical task datasets, and optimized using the same training hyperparameters and number of training steps. 

## _B. Main Results_ 

In this section, we report real-world evaluation results of Legato and RTC across five manipulation tasks executed on physical robotic platforms. As summarized in table I, Legato consistently outperforms RTC across all evaluated tasks. 

TABLE II 

COMPARISON OF TRAINING-TIME RTC AND LEGATO. THE GUIDANCE CONFIGURATION OF LEGATO IS _d_ =8, _s_ =30, _r_ =22. VALUES ARE REPORTED AS MEAN _±_ STANDARD ERROR. 

|**Metric**|Training-time RTC|Legato|
|---|---|---|
|Score _↑_|9.46 _±_ 0.16|**9.72** _±_ **0.13**|
|Completion Time (s) _↓_|81.73 _±_ 1.12|**75.73** _±_ **1.51**|
|NSPARC _↓_|2.46 _±_ 0.14|**1.65** _±_ **0.08**|
|NLDLJ _↓_|39.95 _±_ 0.13|**39.50** _±_ **0.13**|


_1)_ **_Task efficiency_** _:_ Legato consistently achieves shorter task completion time than RTC across all tasks. As analyzed in section III-C, the schedule-shaped velocity reweighting increases the difficulty of switching between competing action modes, effectively suppressing frequent multimodal oscillations during execution. 

Empirically, this leads to more decisive action generation with reduced hesitation before execution, thereby shortening overall task duration. The effect is particularly pronounced in the bowl-stacking task, where multiple visually similar bowls induce a large number of plausible action modes, as shown in fig. 6. In such settings, RTC often alternates between competing strategies, while Legato maintains consistent mode selection and completes the task more efficiently. 

_2)_ **_Trajectory smoothness_** _:_ Legato also demonstrates clear advantages in trajectory smoothness compared to RTC. With the exception of NLDLJ, all smoothness-related metrics show statistically significant improvements in favor of Legato. 

Specifically, Legato consistently achieves lower NSPARC values across all tasks. This result indicates that Legato produces commands with reduced high-frequency velocity fluctuations and more regular speed modulation. Such improvements correspond to smoother and more visually coherent motions observed during real-world execution, as shown in the trajectories in fig. 1. 

In addition, Legato substantially reduces the chunk-overlap RMSE across tasks. The observed improvements indicate that Legato generates more coherent chunk-to-chunk transitions, leading to improved continuity at action boundaries and smoother chunk-to-chunk stitching. 

In contrast, improvements in NLDLJ do not consistently reach statistical significance across all tasks. NLDLJ measures high-order geometric smoothness by integrating squared jerk over the entire trajectory and is therefore dominated by motion segments outside the chunk overlap regions. Importantly, NLDLJ does not degrade under Legato compared to RTC, indicating that while trajectory continuity is improved at chunk boundaries, the remaining portions of the trajectory do not exhibit degraded smoothness. 

_3)_ **_Task success_** _:_ Finally, Legato exceeds the task completion scores achieved by RTC. This confirms that the observed improvements in execution efficiency and trajectory smoothness do not come at the cost of task success, but instead translate into more reliable and effective real-world manipulation performance. 


Fig. 7. Schedule ablation reveals a controllable trade-off between local overlap consistency and smoothness. Across schedule configurations ( _d, s, r_ ), Legato outperforms RTC on completion time and smoothness. Decreasing stride strengthens overlap coupling but can increase high-frequency content; shortening the ramp partially recovers frequency-domain smoothness at the cost of weaker overlap alignment. 

## _C. Comparison with Training-Time RTC_ 

We compare Legato with the recently proposed trainingtime RTC [9] on the _pour_ task, which also introduces continuation during training by constraining overlapping action segments. We implement training-time RTC following the original formulation and compare it against Legato under the same experimental settings. As shown in table II, Legato achieves higher task scores, shorter completion times, and improved smoothness metrics compared to training-time RTC. 

To contextualize this comparison, when the ramp length in our guidance schedule is set to zero, the schedule reduces to a hard overlap constraint that is similar in form to trainingtime RTC. However, this similarity is limited to the constraint shape: the two approaches differ fundamentally in how continuation is incorporated into the learned policy. Training-time RTC treats continuation as an external constraint via hard prefix conditioning while leaving the underlying flow dynamics unchanged. In contrast, Legato reshapes the learned flow dynamics to match the effective denoising behavior induced by repeated, schedule-shaped guidance, so continuation becomes a native property of the policy dynamics. 

Overall, these results suggest that reshaping the policy dynamics (rather than enforcing hard overlap constraints alone) is important for effective chunk continuation, and that using a non-zero ramp further enables smoother transitions between consecutive action chunks. 

## _D. Ablation Studies_ 

In this section, we conduct a comprehensive set of ablation studies to analyze the applicability and robustness of the proposed method. Specifically, we examine: (i) the effect of different guidance schedule settings at inference time, (ii) the role of the condition row used in our policy, and (iii) the performance of Legato across different VLA models. 

TABLE III 

ABLATION STUDY ON ROBUSTNESS TO INFERENCE DELAY. WE VARY THE INFERENCE DELAY _d_ WITH A FIXED EXECUTION STRIDE _s_ , WHERE THE RAMP LENGTH _r_ CHANGES ACCORDINGLY DUE TO THE SCHEDULE CONSTRAINT. VALUES ARE REPORTED AS MEAN _±_ STANDARD ERROR. 

|(_d, s, r_)|**Method**|**NSPARC** _↓_|**Overlap RMSE** _↓_|
|---|---|---|---|
|(103020)|RTC|2.03 _±_ 0.08<br>|9.23 _±_ 0.75<br>|
|,,|Legato|**1.68** _±_ **0.09**|**7.00** _±_ **0.50**|
|(83022)|RTC|2.10 _±_ 0.09|7.00 _±_ 0.52|
|,,|Legato|**1.50** _±_ **0.07**|**5.94** _±_ **0.38**|
|(63024)|RTC|2.03 _±_ 0.08|9.23 _±_ 0.75|
|,,|Legato|**1.38** _±_ **0.05**|**5.44** _±_ **0.31**|


_1)_ **_Varying the execution stride s_** _:_ RTC recommends setting the execution stride _s_ to at least half of the action chunk length. However, since _s_ directly determines the effective inference frequency, a larger stride inevitably reduces the model’s responsiveness. This reveals an inherent trade-off between inference efficiency and control reactivity, motivating a detailed ablation over guidance schedule configurations. 

When the execution stride _s_ becomes smaller than half of the chunk length, the ramp segment may extend beyond the immediate next chunk. To avoid that, we shorten the ramp segment as _s_ decreases, ensuring that the ramp always remains confined within the next chunk. We evaluate several guidance schedule configurations on the _pour_ task, as illustrated in fig. 7. 

TABLE IV 

ABLATION STUDY ON THE EFFECT OF THE CONDITION ROW UNDER DIFFERENT GUIDANCE CONFIGURATIONS. WE VARY THE INFERENCE DELAY _d_ AND RAMP LENGTH _r_ TO CONSTRUCT DIFFERENT SCHEDULES. VALUES ARE REPORTED AS MEAN _±_ STANDARD ERROR. 

|(_d, s, r_)|**Method**|**NSPARC** _↓_|**Overlap RMSE** _↓_|
|---|---|---|---|
|(103020)|w/o cond|**1.64** _±_ **0.07**|7.88 _±_ 0.70|
|,,|w/ cond|1.68 _±_ 0.09|**7.00** _±_ **0.50**|
|83022|w/o cond|1.52 _±_ 0.09|7.21 _±_ 0.68|
|(,,)|w/ cond|**1.50** _±_ **0.07**|**5.94** _±_ **0.38**|
|63024|w/o cond|1.49 _±_ 0.10|6.40 _±_ 0.52|
|(,,)|w/ cond|**1.38** _±_ **0.05**|**5.44** _±_ **0.31**|


TABLE V ABLATION RESULTS ON THE _π_ 0 AND GR00T N1.6 MODEL COMPARING RTC AND LEGATO UNDER THE SAME GUIDANCE CONFIGURATION ( _d_ =8, _s_ =30, _r_ =22). VALUES ARE REPORTED AS MEAN _±_ STANDARD ERROR. 

|**Metric**|_π_0 + RTC|_π_0 + Legato|
|---|---|---|
|Completion Time _↓_|92.93 _±_ 1.90|**88.30** _±_ **1.29**|
|NSPARC _↓_|2.00 _±_ 0.09|**1.83** _±_ **0.08**|
|NLDLJ _↓_|40.48 _±_ 0.21|**40.27** _±_ **0.09**|
|Overlap RMSE _↓_|8.63 _±_ 0.65|**7.50** _±_ **0.49**|
|**Metric**|Gr00t + RTC|Gr00t + Legato|
|Completion Time _↓_|91.60 _±_ 2.30|**84.90** _±_ **1.30**|
|NSPARC _↓_|2.99 _±_ 0.17|**2.63** _±_ **0.06**|
|NLDLJ _↓_|39.91 _±_ 0.07|**39.62** _±_ **0.12**|
|Overlap RMSE _↓_|9.43 _±_ 0.46|**8.75** _±_ **0.36**|


Our findings can be summarized as follows: 

_a)_ **_Legato consistently outperforms RTC on almost all metrics_** _:_ The only exception is the overlap RMSE in the _d_ = _s_ = _r_ = 8 setting, which is discussed in the appendix. 

_b)_ **_Reducing the execution stride_** _s_ **_improves chunkto-chunk consistency but can degrade global smoothness_** _:_ Under the constraint _r_ + _s_ + _d_ = _H_ , a smaller _s_ implies a larger ramp length _r_ , which improves chunk-to-chunk continuity, as reflected by lower overlap RMSE. At the same time, smaller strides lead to more frequent overlap regions, causing highfrequency components to accumulate and resulting in degraded whole-trajectory smoothness metrics. 

_c)_ **_Shortening the ramp while keeping_** _s_ **_small improves frequency-domain smoothness at the expense of overlap consistency_** _:_ When _s_ remains small but the ramp length is shortened, NSPARC improves, indicating smoother frequencydomain behavior. However, this reduces overlap consistency, reflecting a weaker coupling between adjacent chunks. 

Overall, these results demonstrate that the execution stride _s_ and ramp length jointly control a fundamental trade-off between local chunk connection quality and global frequencydomain smoothness. By adjusting their relative proportions, Legato enables flexible control over trajectory smoothness. 

_2)_ **_Varying the inference delay d_** _:_ In addition to the execution stride, the inference delay _d_ also plays an important role in shaping trajectory smoothness. To isolate its effect, we fix the execution stride _s_ and vary the delay length _d_ , conducting evaluations on the _pour_ task. The quantitative results are summarized in table III. 

Across all evaluated metrics, Legato consistently outper- 

forms RTC, demonstrating the robustness of the proposed method to variations in inference latency. When analyzing Legato specifically, we find that reducing the delay length decreases the size of the overlap region while simultaneously increasing the relative length of the ramp segment. This leads to improved chunk-to-chunk continuity and smoother execution, as reflected by better overlap consistency and frequencydomain smoothness metrics. 

Overall, these results indicate that both execution stride _s_ and inference delay _d_ provide effective control knobs for shaping smoothness properties of generated trajectories. Legato can flexibly adapt to different schedule configurations while consistently maintaining superior performance over RTC. 

_3)_ **_Condition Row_** _:_ To evaluate whether the condition row is useful, we conduct an ablation study in which the guidance schedule is no longer provided as an explicit condition. 

We perform this ablation on the _pour_ task, and report the results in table IV. As shown, removing the condition row leads to a degradation in performance, particularly in trajectory smoothness and execution stability. This suggests that explicitly providing the guidance schedule helps the model disambiguate different continuation regimes induced by varying ( _d, r_ ) pairs, and enables more reliable adaptation to dynamic inference conditions. 

_4)_ **_Different Models_** _:_ In the main results table I, we evaluate our method on the _π_ 0 _._ 5 model. To evaluate whether the proposed method generalizes across different VLA models, we further conduct experiments on the _π_ 0 and Gr00t N1.6 model. We select the representative task _pour things_ . As shown in 

TABLE VI 

COMPARISON OF TE AND LEGATO ON THE POUR TASK. 

|**Method**|**Score**_↑_|**Time (s)**_↓_|**NSPARC**_↓_|
|---|---|---|---|
|TE|9.17 _±_ 0.16|96.87 _±_ 2.79|2.96 _±_ 0.23|
|Legato|**9.67** _±_ **0.10**|**76.43** _±_ **1.46**|**1.50** _±_ **0.07**|


TABLE VII 

NSPARC METRIC RESULTS UNDER VARYING INFERENCE _N_ (TRAINED FOR _N_ =5 ON POUR TASK) OF LEGATO. 

||_N_=1|_N_|=3<br>_N_=10|_N_=15|
|---|---|---|---|---|
|w/o cond. row|1_._98_±_0_._17|1_._85_±_|0_._07<br>1_._77_±_0_._18|1_._97_±_0_._09|
|w/ cond. row|_unstable motion_|2_._65_±_|0_._11<br>1_._82_±_0_._16|2_._11_±_0_._13|


Fig. 8. Left: Legato vs. RTC, Training-time RTC, and BID in Kinetix. Right: Ablation result on the schedule randomization. 

## _F._ **_Deployment guidelines_** 

table V, Legato outperforms RTC on the _π_ 0 and Gr00t N1.6 model on the pour task. 

These results demonstrate that the proposed method is not tied to a specific policy backbone or training configuration, and can be effectively transferred across different flow-based VLA models, highlighting its robustness and model generality. 

_5)_ **_Different Smoothing Methods_** _:_ As diffusion-based methods are not directly comparable, we compare with the trajectory smoothing baseline Temporal Ensembling (TE) [43]. This method maintains a buffer of predicted chunks and executes averaged actions for each timestep. As shown in table VI, Legato outperforms TE in both execution time and continuation quality, benefiting from its native continuation mechanism. 

_6)_ **_Sensitivity to denoising steps_** _:_ Training velocity implicitly depends on the denoising step count _N_ , while we additionally evaluate generalization under different inference-time denoising schedules. To improve robustness across varying _N_ , we apply a heuristic rescaling _ωi_<sup>_′_=clamp(1</sup><sup>_−_(1</sup><sup>_−ωi_)</sup><sup>_·_(</sup><sup>_N_train</sup><sup>_/N_infer)</sup><sup>_,_0</sup><sup>_,_1)atinferencetime.</sup> Although this rescaling introduces a mild training-inference mismatch, since the velocity field is trained under a fixed _N_ train, we find that it substantially reduces sensitivity to the inference denoising step count in practice. Without the condition row, Legato even remains effective under single-step denoising, as shown in table VII. 

## _E._ **_Simulation Results on Kinetix_** 

We test Legato in Kinetix, using identical settings to Training-time RTC. As shown in Figure 8 (left): Legato outperforms all methods when delay _>_ 0. In Kinetix, the policy is a based on a UNet, shown the generalization of Legato across different flow-based policies. 

We also ablate schedule randomization during training in Kinetix. As shown in Figure 8 (right), fixing _d_ during training degrades performance at other _d_ values during evaluation, highlighting the importance of delay randomization. Notably, when the randomized delay range does not include _d_ =0, the policy becomes severely out-of-distribution at the first denoising step without guidance, leading to near-complete failure during evaluation. 

We recommend the following hyper-parameters for deployment: _d_ = max(recent delays), _s_ =0 _._ 5 _H_ , _r_ = _H−d−s_ . In practice, following RTC, we maintain a short history of recent inference delays and use the maximum observed delay as the deployment-time _d_ . For variable- _N_ inference, we recommend using the w/o-condition-row variant. 

Additionally, we find that finetuning from a strong base policy leads to more stable convergence and reduces the tendency of excessive guidance training to impair reactivity. Therefore, we recommend initializing Legato from a strong pretrained base policy. 

## V. CONCLUSION 

In this work, we propose Legato, a training-time continuation method for action-chunked flow-based VLA policies. Legato reshapes the learned flow dynamics to align training and inference under schedule-shaped, per-step continuation, making chunk continuation a native property of the policy. This design improves trajectory smoothness and reduces spurious multimodal switching at chunk boundaries, leading to smoother action and more consistent action modes, less hesitation, and shorter task completion time. By conditioning on randomized schedules, a single policy can adapt to different inference delays and flexibly control trajectory smoothness. 

In the current formulation, the denoise step is specified at training time, limiting the ability to adjust it during inference. Future work could investigate more flexible native continuation schemes with consistent training and inference dynamics. 

## ACKNOWLEDGMENTS 

This research was conducted with the support of the Shanghai Qi Zhi Institute & Spirit AI Innovation Program and the Tsinghua University Dushi Program. Funding and support for this work were also provided by the Tsinghua University - Keystone Electrical (Zhejiang) Co.,Ltd Joint Research Center for Embodied Multimodal Artificial Intelligence (JCEMAI). Additionally, we would like to extend our thanks to the Xiongan AI Institute. 

## REFERENCES 

- [1] Nadun Ranawaka Arachchige, Zhenyang Chen, Wonsuhk Jung, Woo Chul Shin, Rohan Bansal, Pierre Barroso, Yu Hang He, Yingyang Celine Lin, Benjamin Joffe, 

Shreyas Kousik, et al. Sail: Faster-than-demonstration execution of imitation learning policies. _arXiv preprint arXiv:2506.11948_ , 2025. 

- [2] Sivakumar Balasubramanian, Alejandro MelendezCalderon, Agn`es Roby-Brami, and Etienne Burdet. On the analysis of movement smoothness. _Journal of NeuroEngineering and Rehabilitation_ , 12, 2015. 

- [3] Jose Barreiros, Andrew Beaulieu, Aditya Bhat, Rick Cory, Eric Cousineau, Hongkai Dai, Ching-Hsin Fang, Kunimatsu Hashimoto, Muhammad Zubair Irshad, Masha Itkina, et al. A careful examination of large behavior models for multitask dexterous manipulation. _arXiv preprint arXiv:2507.05331_ , 2025. 

- [4] Suneel Belkhale and Dorsa Sadigh. Minivla: A better vla with a smaller footprint, 2024. 

- [5] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [6] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A visionlanguage-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [7] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y Galliker, et al. _π_ 0 _._ 5: a vision-language-action model with openworld generalization. In _9th Annual Conference on Robot Learning_ , 2025. 

- [8] Kevin Black, Manuel Y Galliker, and Sergey Levine. Real-time execution of action chunking flow policies. _arXiv preprint arXiv:2506.07339_ , 2025. 

- [9] Kevin Black, Allen Z Ren, Michael Equi, and Sergey Levine. Training-time action conditioning for efficient real-time chunking. _arXiv preprint arXiv:2512.05964_ , 2025. 

- [10] Max Braun, No´emie Jaquier, Leonel Rozo, and Tamim Asfour. Riemannian flow matching policy for robot motion learning. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 5144–5151. IEEE, 2024. 

- [11] Chilam Cheang, Sijin Chen, Zhongren Cui, Yingdong Hu, Liqun Huang, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Xiao Ma, et al. Gr-3 technical report. _arXiv preprint arXiv:2507.15493_ , 2025. 

- [12] Boyuan Chen, Diego Mart´ı Mons´o, Yilun Du, Max Simchowitz, Russ Tedrake, and Vincent Sitzmann. Diffusion forcing: Next-token prediction meets full-sequence diffusion. _Advances in Neural Information Processing Systems_ , 37:24081–24125, 2024. 

- [13] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal manipulation interface: In-thewild robot teaching without in-the-wild robots. _arXiv_ 

_preprint arXiv:2402.10329_ , 2024. 

- [14] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

- [15] Jonathan Ho and Tim Salimans. Classifier-free diffusion guidance. _arXiv preprint arXiv:2207.12598_ , 2022. 

- [16] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _Advances in neural information processing systems_ , 33:6840–6851, 2020. 

- [17] Sigmund H Høeg, Yilun Du, and Olav Egeland. Streaming diffusion policy: Fast policy synthesis with variable noise diffusion models. _arXiv preprint arXiv:2406.04806_ , 2024. 

- [18] Chanhyuk Jung, Dasom Ahn, Sangwon Kim, In-su Jang, Kwang-Ju Kim, Sungkeun Yoo, and Byoung Chul Ko. Rolling diffusion policy for robotic action prediction: Enhancing efficiency and temporal awareness. In _ICRA 2025 Workshop on Foundation Models and NeuroSymbolic AI for Robotics_ , 2025. 

- [19] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [20] Lucy Lai, Ann Zixiang Huang, and Samuel J Gershman. Action chunking as policy compression. _PsyArXiv_ , 2022. 

- [21] Zhixuan Liang, Yizhuo Li, Tianshuo Yang, Chengyue Wu, Sitong Mao, Tian Nian, Liuao Pei, Shunbo Zhou, Xiaokang Yang, Jiangmiao Pang, et al. Discrete diffusion vla: Bringing discrete diffusion to action decoding in vision-language-action policies. _arXiv preprint arXiv:2508.20072_ , 2025. 

- [22] Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. Onetwovla: A unified vision-language-action model with adaptive reasoning. _ArXiv_ , abs/2505.11917, 2025. 

- [23] Tao Lin, Yilei Zhong, Yuxin Du, Jingjing Zhang, Jiting Liu, Yinxinyu Chen, Encheng Gu, Ziyan Liu, Hongyi Cai, Yanwen Zou, et al. Evo-1: Lightweight visionlanguage-action model with preserved semantic alignment. _arXiv preprint arXiv:2511.04555_ , 2025. 

- [24] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- [25] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- [26] Yuejiang Liu, Jubayer Ibn Hamid, Annie Xie, Yoonho Lee, Maximilian Du, and Chelsea Finn. Bidirectional decoding: Improving action chunking via closed-loop resampling. _arXiv preprint arXiv:2408.17355_ , 2024. 

- [27] Tim Pearce, Tabish Rashid, Anssi Kanervisto, Dave Bignell, Mingfei Sun, Raluca Georgescu, Sergio Valcar- 

   - cel Macua, Shan Zheng Tan, Ida Momennejad, Katja Hofmann, et al. Imitating human behaviour with diffusion models. _arXiv preprint arXiv:2301.10677_ , 2023. 

- [28] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [29] Ashwini Pokle, Matthew Muckley, Ricky T. Q. Chen, and Brian Karrer. Training-free linear image inverses via flows. _Trans. Mach. Learn. Res._ , 2024, 2023. 

- [30] Delin Qu, Haoming Song, Qizhi Chen, Zhaoqing Chen, Xianqiang Gao, Xinyi Ye, Qi Lv, Modi Shi, Guanghui Ren, Cheng Ruan, et al. Eo-1: Interleaved visiontext-action pretraining for general robot control. _arXiv preprint arXiv:2508.21112_ , 2025. 

- [31] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- [32] Jiaming Song, Arash Vahdat, Morteza Mardani, and Jan Kautz. Pseudoinverse-guided diffusion models for inverse problems. In _International Conference on Learning Representations_ , 2023. 

- [33] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- [34] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [35] Yating Wang, Haoyi Zhu, Mingyu Liu, Jiange Yang, HaoShu Fang, and Tong He. Vq-vla: Improving visionlanguage-action models via scaling vector-quantized action tokenizers. _ArXiv_ , abs/2507.01016, 2025. 

- [36] Junjie Wen, Minjie Zhu, Jiaming Liu, Zhiyuan Liu, Yicun Yang, Linfeng Zhang, Shanghang Zhang, Yichen Zhu, and Yi Xu. dvla: Diffusion vision-language-action model with multimodal chain-of-thought. _arXiv preprint arXiv:2509.25681_ , 2025. 

- [37] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient 

vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [38] Yuqing Wen, Hebei Li, Kefan Gu, Yucheng Zhao, Tiancai Wang, and Xiaoyan Sun. Llada-vla: Vision language diffusion action models. _arXiv preprint arXiv:2509.06932_ , 2025. 

- [39] Bin Yu, Shijie Lian, Xiaopeng Lin, Yuliang Wei, Zhaolong Shen, Changti Wu, Yuzhuo Miao, Xinming Wang, Bailing Wang, Cong Huang, et al. Twinbrainvla: Unleashing the potential of generalist vlms for embodied tasks via asymmetric mixture-of-transformers. _arXiv preprint arXiv:2601.14133_ , 2026. 

- [40] Hang Yu, Juntu Zhao, Yufeng Liu, Kaiyu Li, Cheng Ma, Di Zhang, Yingdong Hu, Guang Chen, Junyuan Xie, Junliang Guo, et al. Point what you mean: Visually grounded instruction policy. _arXiv preprint arXiv:2512.18933_ , 2025. 

- [41] Juntu Zhao, Wenbo Lu, Di Zhang, Yufeng Liu, Yushen Liang, Tianluo Zhang, Yifeng Cao, Junyuan Xie, Yingdong Hu, Shengjie Wang, et al. Do you need proprioceptive states in visuomotor policies? _arXiv preprint arXiv:2509.18644_ , 2025. 

- [42] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, Ankur Handa, Ming-Yu Liu, Donglai Xiang, Gordon Wetzstein, and Tsung-Yi Lin. Cot-vla: Visual chain-of-thought reasoning for visionlanguage-action models. _2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 1702–1713, 2025. 

- [43] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- [44] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3dvla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 

- [45] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 

- [46] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

APPENDIX 

## _A._ **_Task Details_** 

We evaluate all methods on five real-world manipulation tasks that span diverse object interactions, action patterns, and execution characteristics. Across all tasks, the robot starts from an identical initial configuration for all models. Unless otherwise specified, object positions, orientations, and appearances are randomized per trial but kept identical across different models to ensure fair comparison. Unless otherwise noted, for all tasks except bowl, each model is evaluated over 30 trials. All ablation studies follow the same evaluation protocol, with 30 trials conducted per model for each task. 

_1)_ **_Bowl Stacking (bowl)_** _:_ The objective of this task is to stack all bowls placed on a tabletop into a single vertical stack. We consider five settings with the number of bowls equal to _{_ 3 _,_ 4 _,_ 5 _,_ 6 _,_ 7 _}_ . For each setting, 10 trials are conducted, resulting in a total of 50 trials. In each trial, the initial positions and colors of the bowls are randomly sampled. To ensure fair comparison, the same set of 50 initial configurations is used across all models. A trial is considered successful if all bowls are stacked into one pile without any bowl falling off the table. 

_2)_ **_Pouring (pour)_** _:_ This task evaluates coordinated grasping, lifting, and rotational control. Two bowls of different colors are placed on the tabletop, one of which initially contains a set of small blocks. The robot is required to grasp the bowl containing the blocks, pour all blocks into the empty bowl, then grasp the second bowl and pour the blocks back into the original bowl. This sequence constitutes one complete pouring operation, as illustrated in fig. 1. Each trial consists of three consecutive pouring operations. 

_3)_ **_Pick-and-Place (pickplace)_** _:_ In this task, the robot must place all items on the table into a white box. The objects include a small jar, a marker pen, and a small ball. The white box and all three objects are randomly placed on the tabletop at the beginning of each trial, with configurations shared across models. A trial is considered successful if all three objects are fully placed inside the box. 

_4)_ **_Drawer Opening (drawer)_** _:_ This task requires the robot to open the second drawer of a white three-layer drawer cabinet. At the beginning of each trial, the drawer cabinet is placed on the table with a randomly sampled position and orientation, while remaining consistent across models. The task is considered successful if the second drawer is pulled open beyond a predefined distance threshold. 

_5)_ **_Towel Folding (towel)_** _:_ The objective of this task is to fold a towel placed on the tabletop. The towel’s initial position and orientation are randomly sampled for each trial and kept identical across models. A trial is considered successful if the towel is folded into a compact configuration according to predefined geometric criteria. 

## _B._ **_Delay Construction Details_** 

In our experiments, the guidance schedule is fully determined by two parameters: the inference delay _d_ and the ramp length _r_ . Once these two parameters are specified, the corresponding guidance schedule is uniquely defined. This 

section details how the delay parameter _d_ is constructed and controlled in our experiments. 

All experiments are conducted using the _π_ 0 _._ 5 model on a single RTX 4090 GPU. Without enabling inference-time optimizations, a single forward pass of the model takes approximately 170 ms. We adopt an action chunk size of 60, where each chunk corresponds to 2 seconds of continuous actions. Under this setting, the minimum delay induced by inference latency corresponds to approximately 6 timesteps. 

Through careful empirical measurements, we observe that when running on the same hardware, the inference delay remains stable across executions and does not exhibit large fluctuations, typically staying within a one-timestep variation. To ensure experimental consistency and precise control over the delay parameter, we explicitly construct the effective delay duration. Specifically, after generating an action chunk, if the actual inference time does not occupy the prescribed number of delay timesteps, we introduce additional idle time to ensure that the total delay equals the target value. 

In the main experiments, we fix the delay to _d_ = 8 timesteps. This corresponds to an effective delay of approximately 266.7 ms. For the delay ablation study, we evaluate three different delay settings with _d ∈{_ 6 _,_ 8 _,_ 10 _}_ timesteps, corresponding to delays of approximately 200 ms, 266.7 ms, and 333.3 ms, respectively. 

We emphasize that this explicit construction of delay is introduced solely to control experimental variables and ensure fair comparison across different settings. Our experiments show that the proposed method maintains strong performance across a range of delay values. In practical real-world deployments, the delay does not need to be fixed and can instead be handled using a delay buffer, similar to the strategy adopted in Real-Time Chunking (RTC), allowing the guidance schedule to adapt dynamically to runtime conditions. 

## _C._ **_Experiments Details_** 

We clarify the experimental protocol for the _pour_ task. The main experiments and the ablation studies were conducted with a time gap of approximately one month. To ensure that potential changes in the environment or updates to the robot system did not affect the reported results, experiments with identical settings to the main experiments were re-run during the ablation phase to enable fully fair comparisons. 

Specifically, the main experiments reported in table 1 and table 2, together with the preliminary study shown in table A.2, were conducted in the same experimental batch. The remaining ablation experiments were performed at a later time. By reevaluating overlapping settings, we ensure that all reported comparisons reflect methodological differences rather than changes in the experimental setup. 

## _D._ **_Metric Details_** 

_1)_ **_Task Completion Score_** _:_ Trajectory smoothness is only one of several factors that influence a model’s final task performance. Whether a task can be successfully completed also depends on factors such as the generalization of the training 

TABLE A.1 

TASK COMPLETION SCORING SCHEMES FOR ALL FIVE TASKS. POSITIVE SCORES ARE AWARDED FOR COMPLETING TASK-RELEVANT STEPS, WHILE PENALTIES ARE APPLIED FOR EXECUTION ERRORS. EACH PENALTY ITEM IS CAPPED AT A MAXIMUM DEDUCTION OF 3 POINTS PER TRIAL. 

|**Task**|**Scoring Item**|**Score**|
|---|---|---|
|Bowl|Successfully stack one bowl<br>Bowl tipping or falling<br>Empty grasp<br>Grasping an already stacked bowl|**+2**<br>_−_1<br>_−_1<br>_−_1|
|Pour|Complete one pouring operation<br>Bowl tipping or falling|**+** <sup>**10**</sup><br>**3**<br>_−_1|
||Empty grasp<br>Blocks spilled outside the bowl|_−_1<br>_−_1|
||All three objects placed into the box|**+10**|
|PickPlace|Object dropped|_−_1|
||Empty grasp|_−_1|
||Object not placed into the container|_−_1|
||Successfully open the drawer|**+10**|
|Drawer|Pushing the drawer cabinet|_−_1|
||Empty grasp|_−_1|
||Incorrect pulling direction|_−_1|
|Towel|Complete the first fold|**+5**|
||Complete the second fold|**+5**|


RMSE. All metrics are reported such that _smaller values indicate smoother trajectories_ . For clarity, NSPARC and NLDLJ are defined as the negations of SPARC and LDLJ, respectively. 

_a)_ **_NSPARC (Negative SPARC)_** _:_ SPARC (Spectral Arc Length) measures smoothness in the frequency domain by quantifying the arc length of the normalized velocity magnitude spectrum. Given a scalar velocity signal _v_ ( _t_ ) sampled at interval ∆ _t_ , we first compute its discrete Fourier transform and obtain the magnitude spectrum _|V_ ( _ω_ ) _|_ . The spectrum is normalized by its DC component, 


An adaptive cutoff frequency _ωc_ is selected as the smallest frequency at which _V_<sup>ˆ</sup> ( _ω_ ) falls below a predefined threshold, bounded by a maximum cutoff. The frequency axis is normalized as 


and the spectral arc length is computed as 


We report the negated quantity 


data, the consistency between the deployment environment and the data collection setup, and the overall quality of model training. As a result, using a single binary success rate is insufficient to fully characterize model performance, especially for long-horizon manipulation tasks. 

In long-horizon settings, early execution errors can propagate and significantly affect subsequent actions. Under such conditions, a binary success metric fails to reflect partial progress or distinguish between qualitatively different failure modes. To more accurately measure task performance, we introduce a task completion score that provides graded feedback based on the extent to which task objectives are achieved. 

For each task, we define a structured scoring scheme in which completing meaningful intermediate steps yields positive scores, while execution errors incur penalties. The scoring design follows two principles. First, executions that complete more task-relevant steps receive higher scores than those completing fewer steps. Second, trajectories that complete the task with recoverable errors receive higher scores than those that fail to complete the task, but lower scores than trajectories that complete the task without errors. 

We design task-specific completion criteria and penalty rules for all five tasks to ensure that the resulting scores consistently reflect execution quality and task progress, rather than relying solely on a binary notion of success or failure, as shown in table A.1. 

_2)_ **_Smoothness Metrics_** _:_ We evaluate trajectory smoothness using three complementary metrics that capture different aspects of execution quality: NSPARC, NLDLJ, and overlap 

such that smaller NSPARC values correspond to smoother trajectories. 

For multi-dimensional end-effector trajectories, SPARC is computed separately for translational and rotational motion. Translational NSPARC is computed using the Euclidean norm of the 3D linear velocity, while rotational NSPARC is computed using the magnitude of the angular velocity after unwrapping the rotation representation. The final NSPARC score is obtained by averaging over all end-effectors and motion types. 

NSPARC primarily captures the distribution of motion energy across frequencies. Trajectories with oscillations, hesitation, or frequent corrective motions introduce higherfrequency components and yield larger NSPARC values, whereas smooth, continuous motions concentrate energy in low frequencies and result in smaller NSPARC values. 

_b)_ **_NLDLJ (Negative LDLJ)_** _:_ LDLJ (Log Dimensionless Jerk) is a time-domain smoothness metric that penalizes rapid changes in acceleration. Given a trajectory of duration _T_ with scalar velocity _v_ ( _t_ ) and scalar jerk _j_ ( _t_ ), LDLJ is defined as 


where _v_ peak = max _t |v_ ( _t_ ) _|_ is the peak velocity. We report the negated quantity 


so that smaller NLDLJ values indicate smoother motion. 

TABLE A.4 

HYPERPARAMETER CONFIGURATION USED IN THE MAIN EXPERIMENTS AND ABLATION STUDIES. 

|**Symbol**|**Description**|**Value**|
|---|---|---|
|_H_|Action chunk size|60|
|_f_|Action execution frequency|30Hz|
|_N_|Number of denoising steps|5|
|_d ∼_Uni[_·_]|Training-time delay range|Uni[0_,_ 10]|
|_r ∼_Uni[_·_]|Training-time ramp range|Uni[0_,_ 50]|


Fig. A.1. Legato outperforms RTC and Training-time RTC on two new precision tasks. 

TABLE A.2 

ABLATION RESULTS COMPARING ONE-SHOT GUIDANCE AND LEGATO UNDER THE SAME GUIDANCE CONFIGURATION ( _d_ =8, _s_ =30, _r_ =22). VALUES ARE REPORTED AS MEAN _±_ STANDARD ERROR. 

|**Metric**|One-shot Guidance|Legato|
|---|---|---|
|Completion Time _↓_|88.44 _±_ 1.~~67~~|**75.73** _±_ **1.51**|
|NSPARC _↓_|1.77 _±_ 0.17|**1.65** _±_ **0.08**|
|NLDLJ _↓_|40.69 _±_ 0.21|**39.50** _±_ **0.13**|
|Overlap RMSE _↓_|12.69 _±_ 1.55|**5.14** _±_ **0.17**|


consecutive chunks and smoother continuation behavior at chunk boundaries. 

## _E._ **_Results on More Challenging Tasks_** 

We selected two other tasks: Skewer Fruit and Insert Pen. Both require fine manipulation and smoothness, as jitter easily causes failure. Legato shows advantages in time and smoothness, with improved success rates (20 trials per method). Success rate is not the sole metric: improvements in smoothness and mode-switching suppression benefit low-level control stability and execution time, both critical for execution quality. 

## _F._ **_Experiment on the Smoothness–Reactivity Trade-off_** 

We design a reactive task: when the gripper is about to reach the ball, we pull the ball via a rope along the direction perpendicular to the gripper’s motion with **Approaching Rope** fixed speed. We select _d_ =8, _s_ =8, _r_ =22 to achieve higher inference **Pulling away** frequency, enabling fair compariFig. A.2. Reactive task setup. son of reactivity and smoothness between Legato and RTC. ReTABLE A.3 sults show similar reactivity but REACTIVITY TRADE-OFF. significant smoothness improvement, demonstrating that Legato’s Method Succ. _↑_ NSPARC _↓_ smoothness gains do not comproRTCLegato 0.70.7 11 _.._ 9748 _±±_ 00 _.._ 1418 mise reactivity. 

## _G._ **_Preliminary Study Details_** 

For multi-dimensional trajectories, jerk is computed by successively differentiating position or rotation vectors to obtain vector jerk, followed by taking the Euclidean norm. NLDLJ is computed separately for translational and rotational motion, and the final score is averaged across all end-effectors. To avoid artificially inflated jerk values at chunk boundaries, jerk samples corresponding to chunk connection points are excluded from the computation. 

NLDLJ measures smoothness in terms of higher-order temporal continuity. Trajectories with abrupt acceleration changes or sharp corrective motions yield larger NLDLJ values, while trajectories with gradual acceleration profiles achieve smaller NLDLJ values. 

_c)_ **_Overlap RMSE_** _:_ Overlap RMSE directly measures consistency across consecutive action chunks. Let **a**<sup>(</sup> 1:<sup>_k_</sup> _H_<sup>)and</sup> **a**<sup>(</sup> 1:<sup>_k_</sup> _H_<sup>+1)</sup> denote two consecutive predicted action chunks of length _H_ , and let the last _O_ steps of **a**<sup>(</sup><sup>_k_)</sup> overlap with the first _O_ steps of **a**<sup>(</sup><sup>_k_+1)</sup> . The overlap RMSE is defined as 


Overlap RMSE explicitly measures inter-chunk consistency. Lower overlap RMSE values indicate better alignment between 

This appendix provides additional empirical evidence supporting the conclusion in section. III-B that one-shot guidance is insufficient for effective continuation and that guidance must be applied before every denoising step. 

We compare a one-shot guidance baseline with Legato on the _pour_ task. Both methods are evaluated under the same experimental conditions as the main experiments. For the oneshot baseline, guidance is applied only at initialization, after which standard multi-step denoising is performed without any intermediate guidance. Legato, in contrast, applies guidance before every denoising step while remaining consistent with the training objective. 

We use a guidance schedule with stride _s_ = 30, delay _d_ = 8, and ramp length _r_ = 22 for both methods. Quantitative results are reported in table A.2. The results show that Legato significantly outperforms the one-shot baseline, with particularly pronounced improvements in overlap RMSE. This indicates that without repeated guidance, the overlap region progressively deviates from the desired continuation, even when the initial condition is properly constrained. 

These results empirically confirm the observation in section. III-B that guidance applied only at initialization cannot reliably preserve constraints throughout the denoising process. Repeated, per-step guidance is necessary to maintain consistent continuation across action chunks. 


Fig. A.3. Trajectory example for the _pour_ task under the _d_ = _s_ = _r_ =8 configuration. The top panels show a full pouring operation, and the bottom panels show a zoomed-in view of the first 5 seconds. Red dashed lines indicate chunk boundaries. RTC exhibits pronounced low-frequency, large-amplitude oscillations, with direction changes occurring mostly within chunks, indicating increased spurious multimodal switching. Despite achieving lower overlap RMSE, RTC produces visibly less smooth trajectories in this regime. 

## _H._ **_Robot Hardware Configuration_** 

All experiments are conducted on the same dual-arm robotic platform. The robot is equipped with a left arm and a right arm, where each arm consists of seven actuated joints and a gripper, resulting in eight degrees of freedom per arm. 

The perception system includes one head-mounted RGB camera providing a global view of the workspace, as well as one wrist-mounted RGB camera on each arm. In total, the robot uses three cameras for visual observation. 

For VLA training and inference, actions are represented in the end-effector space. Each arm’s action consists of a 6-dimensional end-effector pose, including 3D position and 3D rotation vector, together with a 1-dimensional gripper command. As a result, the full action space for the dual-arm system is 14-dimensional. 

## _I._ **_Hyperparameter Configuration_** 

Table A.4 summarizes the hyperparameter configuration used in the main experiments and ablation studies. Unless otherwise specified, all experiments share the same configuration. We note that _d_ and _r_ denote the delay and ramplength parameters of the guidance schedule; they are fixed at evaluation time, while during training we optionally randomize them by uniform sampling within specified ranges. 

## _J._ **_Results Analysis_** 

_1)_ **_Analysis of the d=s=r=8 setting_** _:_ We analyze an abnormal behavior observed under the _d_ = _s_ = _r_ =8 configuration, where RTC exhibits counterintuitive trends on specific smoothness metrics. 

Under this setting, the model initiates the next inference immediately after generating each action chunk. When the delay _d_ is fixed, setting _s_ = _r_ = _d_ corresponds to the highest possible inference frequency. 

In this regime, the oscillatory behavior of RTC becomes visually apparent, with motion fluctuations reaching amplitudes that are clearly observable. To better understand this phenomenon, we visualize the executed trajectories in fig. A.3. The plots reveal large-amplitude oscillations in RTC trajectories, whereas Legato produces substantially smoother motion. 

The lower panels show a zoomed-in view of the first 5 seconds of execution. The vertical red dashed lines indicate chunk boundaries. Notably, most direction changes occur _within_ individual chunks rather than at chunk boundaries. This suggests that under frequent re-inference, RTC suffers from more severe spurious multimodal switching inside each chunk, rather than discontinuities caused purely by chunk transitions. 

Under this setting, NSPARC more faithfully reflects the perceived smoothness difference between RTC and Legato. Since NSPARC captures the spectral distribution of motion energy, it is particularly sensitive to low-frequency, largeamplitude oscillations, which dominate RTC trajectories in this regime. In contrast, Legato suppresses such oscillatory behavior by maintaining stronger mode persistence across denoising steps, as shown in fig. A.3 and fig. 6. 

Interestingly, RTC achieves a lower overlap RMSE than Legato in this configuration. This observation indicates that overlap RMSE may fail to fully capture smoothness degradation when oscillations are dominated by low-frequency, largeamplitude motion. Although the overlap between consecutive chunks remains numerically consistent, the resulting trajectory still exhibits pronounced oscillations that negatively impact execution quality. This case highlights a limitation of overlap RMSE as a standalone smoothness indicator under highfrequency inference settings. 

_2)_ **_Analysis of the condition row_** _:_ We further analyze the effect of introducing the condition row in the guidance schedule. As shown in table IV, adding the condition row does not lead to a significant improvement in NSPARC, whereas it consistently yields a substantial reduction in overlap RMSE across different guidance configurations. This suggests that the condition row primarily improves inter-chunk consistency rather than intra-chunk smoothness. 

When the delay _d_ decreases and the ramp length _r_ correspondingly increases due to parameter constraints, the overlap RMSE of models _without_ the condition row also decreases. 

Although adding the condition row provides clear benefits under identical ( _d, s, r_ ) configurations, we observe that a model without the condition row under ( _d, s, r_ ) = (6 _,_ 30 _,_ 24) achieves better overlap RMSE than a model with the condition row under ( _d, s, r_ ) = (10 _,_ 30 _,_ 20). This observation suggests that when the delay _d_ is sufficiently small, acceptable continuation behavior can be achieved even without the condition row. In such regimes, omitting the condition row may serve as a viable alternative with reduced conditioning overhead. 

