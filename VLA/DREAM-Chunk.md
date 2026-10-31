---
title: "DREAM-Chunk: Reactive Action Chunking with Latent World Model"
date: "2026-06-17"
authors: "Wenxi Chen; Kaidi Zhang; Chi Lin; Zhiyuan Zhang; Yu She; Yuejiang Liu"
url: https://arxiv.org/abs/2606.18589
pdf: https://arxiv.org/pdf/2606.18589
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.18589)** / [論文ページ](https://arxiv.org/abs/2606.18589)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **DREAM-Chunk: Reactive Action Chunking with Latent World Model** 

**Wenxi Chen**<sup>1</sup> **Kaidi Zhang**<sup>1</sup><sup>_,†∗_</sup> **Chi Lin**<sup>1</sup><sup>_,†_</sup> **Zhiyuan Zhang**<sup>1</sup> **Yu She**<sup>1</sup> **Yuejiang Liu**<sup>2</sup> **Raymond A. Yeh**<sup>1</sup> **Shaoshuai Mou**<sup>1</sup> **Yan Gu**<sup>1</sup> 1Purdue University 2Stanford University 

## **Abstract** 

Action chunking has become a common interface for vision-language-action (VLA) models, enabling low-frequency policy inference to drive high-frequency robot execution. However, once a chunk is committed, its open-loop execution can be brittle under stochastic dynamics, hardware execution errors, and partially observed state. We propose `DREAM-Chunk` , a test-time scaling method that augments chunking-based policies with a lightweight latent world model without requiring additional policy fine-tuning. At test time, `DREAM-Chunk` samples multiple candidate action chunks, rolls out their predicted latent futures, and selects actions from the chunk whose “dreamed” state best matches the observed rollout. In this way, `DREAM-Chunk` uses additional test-time computation to cover multiple plausible stochastic rollouts and improve reactivity during long-horizon chunk execution. On the Kinetix benchmark, `DREAM-Chunk` improves robustness under increasing action noise and benefits from larger candidate sample sizes, especially when demonstrations contain corrective behaviors. We conduct empirical validation on four manipulation tasks across two robot platforms and two VLA policies for various stochasticity sources. Across simulation and hardware experiments, `DREAM-Chunk` improves action-chunking policies in stochastic dynamics. Project page: `https://wenxichen2746.github.io/DREAM-Chunk/` . 

## **1 Introduction** 

Vision-language-action (VLA) models aim to bring foundation-model capabilities into physical control by learning language-conditioned visuomotor policies from large-scale robot demonstration data [42, 9, 4]. In parallel, world models provide a complementary route toward embodied intelligence by learning predictive structure from trajectory data, enabling models to reason about how future states evolve under actions. Recent VLA studies have begun to connect these two directions, for example, by incorporating video prediction or world-action modeling objectives to improve spatiotemporal understanding [39, 6, 24]. The recent _π_ 0 _._ 7 system from Physical Intelligence [28] also reflects this trend, using a video-generation world model to provide context for VLA inference. These developments suggest a modular path 


Figure 1: Illustration of chunk switch to handle external perturbation and stochastic dynamics. 

> _∗_ Kaidi Zhang and Chi Lin made equal contributions to the experimental work. 

Preprint. 

toward practically deployable embodied intelligence [14], integrating advances across complementary areas of robotics research, including VLA and world model studies [12]. 

A widely used approach in learning from demonstration is action chunking [41], where a policy predicts a short sequence of future actions rather than a single-step action. By modeling temporally coherent action segments, action chunking has been effective for imitation learning and generative visuomotor policy learning [7, 26]. Recent VLAs have increasingly adopted this chunked action interface, in part because it allows low-frequency policy inference to drive higher-frequency robot execution. Representative VLA models either use generative “action experts” to directly sample action chunks, as in _π_ 0 _._ 5 [4, 29], Octo [25], and SmolVLA [32], or predict action tokens that are decoded into short action chunks, as in RT-2 [42], OpenVLA [15], and FAST [27, 29, 28]. 

This chunked interface makes large VLAs more practical for real-time deployment. The interface has been shown to help handle inference latency through asynchronous execution [32, 34] while preserving mode consistency when learning from diverse demonstrations [7, 41]. However, these benefits come with an important limitation: once a chunk is committed, the robot executes it largely open-loop, causing errors to accumulate during execution [17]. Liu et al. [20] analyzes that longhorizon execution can provide an information advantage when the policy’s implicit internal model correctly predicts unobserved future states, but this advantage can be substantially weakened under stochastic dynamics. 

Recent efforts to improve VLAs’ reactivity include repeatedly replanning new action chunks while conditioning on future states [34], training lightweight VLAs for faster inference [37], adjusting execution horizons adaptively [33, 19], and training residual modules to correct generated chunks [38, 31]. However, existing approaches still face important limitations. Frequent replanning can be computationally expensive and may waste the long-horizon plans already predicted by the policy, while improving reactivity through lightweight architectural modifications may limit the potential of scaling to larger models and broader training tasks. 

Motivated by the emerging connection between VLA policies and world models, we ask whether lightweight prediction can improve long-horizon chunk execution at test time without modifying the base policy. We propose **Dreamed-state REactive Action Matching for Action Chunking (** `DREAM-Chunk` **)** , which keeps the base policy fixed, samples multiple candidate chunks, and predicts their latent futures with a lightweight world model. During execution, `DREAM-Chunk` matches the observed state to phase-aligned predicted rollouts and selects the action from the most consistent candidate chunk, enabling reactive switching when stochastic dynamics move the robot away from the nominal rollout. Fig. 1 illustrates this process: yellow dashed lines denote candidate rollouts, and the green arrow denotes stochastic effects such as external perturbations or varying object velocities. The chunk horizon and mode differences are exaggerated for clarity. 

**Our main contributions are threefold: (i)** We propose `DREAM-Chunk` , a policy-agnostic testtime scaling framework that improves the reactivity of action-chunking policies under stochastic dynamics without modifying or fine-tuning the base VLA. **(ii)** In controlled Kinetix simulations [22], `DREAM-Chunk` outperforms representative test-time chunking baselines under high stochasticity, and our analysis studies the effects of corrective expert demonstrations and latent representations from R2-Dreamer [23], LeWorldModel [21], and EB-JEPA [35]. **(iii)** We validate `DREAM-Chunk` on four real-world manipulation tasks across SO-101 and Franka Panda using SmolVLA and _π_ 0 _._ 5, covering hardware execution errors, partial observability, and external perturbations; across these settings, `DREAM-Chunk` improves success rates, including increasing open-loop _π_ 0 _._ 5 from 10% to 65% on a precise insertion task under external perturbation. 

## **2 Related Works** 

**Test-time scaling for action chunking.** We use test-time scaling broadly to refer to methods that allocate additional computation or modify the sampling procedure at inference time to improve action-chunking policies. Bidirectional Decoding (BID) [20] samples multiple candidate chunks and selects one that is consistent with the previous trajectory while avoiding actions similar to those from a poor policy. Real-Time Action Chunking (RTC) [5] guides the sampling of a new action chunk via inpainting so that the new chunk aligns with the previously executed chunk, which requires backpropagation at test time. Self-Guidance [33] applies classifier-free-style guidance during action sampling, using two forward passes of both current and previous observations to push actions away 

2 


Figure 2: Naive open-loop action chunk execution cannot correct actions until the next inference step. `DREAM-Chunk` samples batched action chunks from VLA and switches among them using worldmodel predictions. The latent world model, which is much more lightweight than VLA, predicts future rollouts from the current observation: each new observation is encoded by the encoder and compared with predictions from the latent dynamics model. The executed action, indicated by the dashed red arrow, is selected from the chunk whose dreamed state best matches the real-world rollout. This allows sampled chunks to provide alternative rollouts that keep actions valid under stochasticity. 

from distributions induced by prior observations. They also propose adaptive chunking to balance reactivity and consistency, which repeatedly infers new chunks and switches execution when the new action differs sufficiently from the current chunk. Recent methods use uncertainty across batched chunk samples to adapt execution: Liang et al. [19] adjust the execution horizon based on action entropy, while HiPolicy [40] samples coarse-to-fine chunks at multiple frequencies and uses entropy to determine the execution frequency. Beyond chunk-specific mechanisms, RoboMonkey [16] uses test-time action sampling and a fine-tuned VLM verifier to select among candidate actions. In contrast, `DREAM-Chunk` treats chunk execution itself as the test-time decision problem: it samples multiple chunks once and selects among their phase-aligned actions using new observations during execution. 

**World models** have emerged as another major path toward generalist intelligence, spanning diverse efforts from video generation [1] to model-based reinforcement learning [10]. One line of work aims to learn foundation-scale models that predict future observations and actions, where visual reconstruction provides an auxiliary training signal for spatiotemporal understanding and enables scaling from large-scale video data [39, 6, 24]. Another line instead learns latent dynamics models without requiring a visual decoder, using the learned latent transition structure for policy learning [10, 23] or online action planning [21, 35]. Efforts have been made to leverage latent world models to improve the performance of VLA models. For instance, FOREWARN [36] uses a latent world model to predict candidate action outcomes and lets a latent-aligned VLM choose the best action plan based on high-level user intent and semantic constraints. 

## **3 Preliminary** 

We briefly review the necessary background to establish a common notation. 

**Action chunking policy.** We consider an action-chunking policy parameterized as a generative model _π_ ( _At | ot_ ) taking observation _ot_ as input, where each action chunk _At_ = _{at, at_ +1 _, . . . , at_ + _L−_ 1 _}_ is a sequence of actions with chunk length _L_ . The policy is trained from an offline dataset of expert demonstrations _{_ ( _ot, at_ ) _}_ by minimizing the discrepancy between generated action chunks and action segments sliced from the demonstration trajectories. At test time, the policy typically executes only part of each predicted chunk before replanning. We denote this effective number of executed actions as the execution horizon _H_ . 

**Reactive long-horizon control.** Since the whole chunk is generated from the observation available at inference time, later actions are executed based on increasingly outdated state information. To 

3 

formalize this mismatch, let _At_ = _{at, . . . , at_ + _H−_ 1 _} ∼ π_ ( _· | ot_ ) denote an action chunk sampled at time _t_ , and let _At_ [ _τ_ ] be its _τ_ -th action. Ideally, the action executed at phase _τ_ should remain aligned with the decision that the same policy would make if it were re-inferred from the realized observation _ot_ + _τ_ . For an executed action _at_ + _τ_ , we define this alignment as 


where _A_<sup>ˆ</sup> _t_ + _τ_ [0] is the first action of a chunk inferred from the current observation _ot_ + _τ_ . 

**Objective.** We use the expected alignment as a measure of reactivity for a chunk execution strategy _η_ , which selects the executed action _a_<sup>_η_</sup> _t_ + _τ_<sup>fromavailableactionchunksduringrollout.</sup> Here, _Pη_ ( _ot_ +1: _t_ + _H | ot_ ) denotes the rollout distribution induced by the stochastic dynamics _ot_ + _τ_ +1 _∼ P_ ( _· | ot_ + _τ , a_<sup>_η_</sup> _t_ + _τ_<sup>).We define the reactivity objective</sup> 


A more reactive execution strategy achieves a larger _J_ react( _η_ ) by keeping executed actions aligned with what the policy would choose under realized observations. Stochastic dynamics can move the rollout away from the nominal trajectory of the original chunk, causing later open-loop actions to become misaligned with the current policy decision. We denote the per-step probability of such deviation as _p_ dyn. Directly evaluating _J_ react( _η_ ) would require repeatedly re-inferring the VLA at each realized observation; `DREAM-Chunk` instead uses latent matching as a lightweight surrogate, selecting candidate chunks whose dreamed latent states best match the realized rollout. 

## **4 Method** 

`DREAM-Chunk` augments a chunking-based VLA policy with an auxiliary world model and defines an execution strategy over candidate chunks sampled from the fixed policy _π_ . As shown in Fig. 2, the method maintains a set of candidate action chunks, rolls out their latent consequences with the world model, and reactively selects which chunk to follow based on latent-state compatibility. 

**Auxiliary world model.** `DREAM-Chunk` uses an auxiliary world model consisting of an encoder and a latent dynamics model. The encoder maps high-dimensional observations, such as images and robot joint measurements, into a latent state space, _st_ = _e_ ( _ot_ ). The latent dynamics model then predicts the next latent state from the current latent state and action, ˜ _st_ +1 = _f_ ( _st, at_ ). Since the world model is trained on the same offline expert demonstrations as the action-chunking policy, we expect it to capture latent transition structure that is broadly aligned with the policy’s implicit internal model [20]. 

**Intuition.** `DREAM-Chunk` samples multiple plausible short-horizon plans from the current observation and uses an auxiliary world model to predict their latent rollouts. During execution, it selects the chunk whose predicted latent state best matches the observed state, allowing the robot to switch away from a rollout that has become inconsistent under stochastic dynamics. `DREAM-Chunk` therefore does not invent new recovery behaviors at test time; instead, it exposes and selects corrective behaviors already present in the policy’s sampled action distribution. We further analyze when `DREAM-Chunk` can outperform high-frequency short-horizon control in Appendix A1.3. 

### **4.1 Batched Action Chunks Inference and Parallel Latent Rollouts** 

At each replanning step _t_ , `DREAM-Chunk` samples _N_ candidate action chunks from the chunking policy, 


The current observation _ot_ is encoded as _st_ = _e_ ( _ot_ ), and this latent state is duplicated across the candidate dimension to initialize a batched latent tensor, 


Starting from _S_<sup>˜</sup> _t_ , `DREAM-Chunk` rolls out the latent consequences of all candidate chunks in parallel. At each phase _τ_ = 0 _, . . . , H −_ 1, the batched latent dynamics model updates 


4 

**Algorithm 1** `DREAM-Chunk` Execution under Asynchronous Inference 

**Require:** chunking policy _π_ , encoder _e_ , latent dynamics model _f_ **Require:** execution horizon _H_ , overlap step _d_ , number of candidate chunks _N_ 1: _A_ = _{A_<sup>(</sup><sup>_j_)</sup> _}_<sup>_N_</sup> _j_ =1<sup>_←π_(</sup><sup>_ot_)</sup> 2: _st ← e_ ( _ot_ ) 3: _S_<sup>˜</sup> _t ←_ Repeat( _st, N_ ) _▷ S_<sup>˜</sup> _t ∈_ R<sup>_N×dz_</sup> for batched rollout 4: **while** not terminated **do** 5: **for** _τ_ = 0 _, . . . , H −_ 1 **do** 6: _st_ + _τ ← e_ ( _ot_ + _τ_ ) 7: _i ←_ arg min _j∈{_ 1 _,...,N }_ ��� _st_ + _τ − S_ ˜ _t_ + _τ_ [ _j_ ]���2 8: _at_ + _τ ← A_<sup>(</sup> _τ_<sup>_i_); execute</sup><sup>_a_</sup> _t_ + _τ_ 9: **if** _τ_ = _H −_ 1 _− d_ **then** 10: _S ←{st_ + _τ }_<sup>_N_</sup> _j_ =1<sup>;</sup> _A_<sup>next</sup> _← π_ ( _ot_ + _τ_ ) asynchronously 11: **end if** 12: _S_ ˜ _t_ + _τ_ +1 _← f_ � _S_ ˜ _t_ + _τ , {A_<sup>(</sup> _τ_<sup>_j_)</sup><sup>_}N_</sup> _j_ =1� 13: **end for** 14: _A ←A_<sup>next</sup> ; _S_ ˜ _← S_ ; _i ←_ 1 15: **end while** 

where _S_<sup>˜</sup> _t_ + _τ_ [ _j_ ] denotes the dreamed latent state for candidate chunk _j_ at execution phase _τ_ and _Aτ_<sup>(</sup><sup>_j_)</sup> is the _τ_ -th action in candidate chunk _A_<sup>(</sup><sup>_j_)</sup> . This produces a phase-aligned latent rollout for each candidate chunk. Importantly, the dreamed states are not reset using future observations during the rollout; they represent the expected latent evolution induced by each sampled action chunk. 

This procedure acts as a form of test-time scaling: additional inference-time computation is used to sample more candidate chunks and predict more possible latent futures. Instead of committing to a single open-loop chunk, `DREAM-Chunk` maintains a batched set of imagined rollouts that can be queried online as new observations arrive. 

### **4.2 Execution via Reactive Latent Matching** 

During execution, the robot receives a new observation _ot_ + _τ_ at each phase _τ ∈{_ 0 _, . . . , H −_ 1 _}_ and encodes it as _st_ + _τ_ = _e_ ( _ot_ + _τ_ ). `DREAM-Chunk` compares this observed latent state with the phasealigned dreamed states from the batched rollout and selects the candidate chunk whose prediction best matches the realized state: 


This rule allows `DREAM-Chunk` to switch among candidate chunks when the observed trajectory deviates from the predicted rollout of the currently followed chunk. Because the matching with the observed latent state is performed only against dreamed states at the same execution phase, the switch remains temporally aligned with the action sequence rather than jumping to an earlier or later stage of another rollout. `DREAM-Chunk` can also be incorporated with asynchronous inference by storing the true latent state at policy inference, as stated in Alg. 1. 

### **4.3 Auxiliary World Model Formulation** 

The latent state representation could be deterministic, following the line of works on JEPA [18, 21], or stochastic ( _s_ = ( _h, z_ ), where _h_ is deterministic, and _z_ is stochastic) as formulated in the Recurrent State-Space Model (RSSM) adopted in the Dreamer series [11, 23]. Our experiment will show that the `DREAM-Chunk` method can be adapted to both formulations as shown in our ablation study in Fig. 5. Further, we want to highlight that this latent dynamics model is substantially lighter than VLA models and does not introduce significant computation overhead. For example, a JEPA world model can only have 15 million parameters, while a small-scale VLA like SmolVLA has around 

5 


Figure 3: Kinetix simulation result on performance and latent similarity. Reported values are averaged over 12 environments. 

450 million parameters, and larger models like _π_ 0 _._ 5 can have more than 2 billion parameters. In our hardware experiments, VLA inference takes more than 100 ms, and world model encoding and prediction take less than 10 ms, as listed in Tab. A2. 

## **5 Experiment** 

We evaluate `DREAM-Chunk` in both controlled simulation and real-world hardware settings. In Sec. 5.1, we use the Kinetix benchmark to study how `DREAM-Chunk` behaves under controlled action noise, including the effects of sample count, corrective behaviors in demonstrations, and latent world model design. In Sec. 5.2, we deploy `DREAM-Chunk` on real robot manipulation tasks to test whether the same mechanism improves robustness under real-world stochasticity like hardware execution imperfections, partial observability, and external perturbations. 

### **5.1 Kinetix Simulation** 

Our simulation experiments are designed to answer three questions: (1) Does increasing the number of sampled chunks improve `DREAM-Chunk` ’s performance under stochastic dynamics? (2) What conditions are necessary for test-time scaling with `DREAM-Chunk` to be effective? (3) How does the learned latent representation of the auxiliary world model affect performance? 

Kinetix [22] is a 2D agentic simulation benchmark spanning locomotion, manipulation, and Atari-like control tasks. Following the RTC evaluation setting [5], we train a flow-matching action-chunking policy by imitation learning from RL expert demonstrations collected with different random seeds. We introduce environmental stochasticity by adding Gaussian noise to the executed action, _a_ exec = _a_ + _ϵ_ , where _ϵ ∼N_ (0 _, σ_<sup>2</sup> _I_ ) and _σ_ controls the noise level. 


Figure 4: The figure reports the solve rate of DreamChunk under action noise 0 _._ 3 with different sample size _N_ , where the behavior cloning policy is trained on demonstrations from experts trained with different action-noise levels. 

**Implementation detail.** We compare `DREAM-Chunk` against naive asynchronous execution [32, 34], RTC [5], BID [20], and Adaptive Chunking (AC) [33]. For BID and RTC, we follow the settings provided in [5]. BID uses 10 sampled action chunks and uses an early checkpoint as a weak policy. We only display the performance of the RTC variant with soft-masking as championed by the original paper. We implement AC following [33], using cosine similarity as the switching metric with a threshold of 0 _._ 97. Unless otherwise specified, reported `DREAM-Chunk` performance uses an RSSM-based world model trained with one-step prediction loss and Barlow Twins regularization [23]. 

**Performance under stochasticity.** As shown in Fig. 3a, `DREAM-Chunk` gains larger improvements as the number of sampled chunks increases. This comparison highlights the benefit of improving _withinchunk reactivity_ . In contrast, BID and RTC mainly target _cross-chunk consistency_ by improving the transition between independently inferred chunks. Under low stochasticity, both directions provide similar gains over naive asynchronous execution. However, as the variance of the action noise increases, `DREAM-Chunk` achieves a larger advantage, suggesting that within-chunk reactivity becomes more important when the realized trajectory deviates from the nominal open-loop rollout. 

6 

AC also aims to improve reactivity by adaptively changing the execution horizon, but its performance is often close to the naive one-step replanning baseline on dynamic tasks, suggesting that it tends to replan frequently rather than preserve longer chunk execution. We provide additional results across execution horizons in Appendix Fig. A1, where `DREAM-Chunk` shows particular strength under midto long-horizon execution. 

To test whether more candidate chunks provide closer predicted futures to the states actually reached under stochastic execution, we measure the average nearest-neighbor distance between the encoded latent state reached during execution and the dreamed latent states predicted by candidate chunks. As shown in Fig. 3b, increasing the number of sampled chunks reduces this distance, indicating better coverage of realized rollouts. Higher environmental stochasticity leads to larger distances, reflecting the increased difficulty of predicting future states under stronger execution noise. 

**Corrective behavior in demonstrations.** We next study when `DREAM-Chunk` is most effective. As `DREAM-Chunk` selects among action chunks already sampled from the policy, its benefit depends on whether the policy distribution contains useful corrective behaviors and whether the auxiliary world model provides a latent space that can reliably distinguish the consequences of these candidate chunks. That is, `DREAM-Chunk` requires the action-chunking policy to generate useful recovery options under stochastic dynamics. The Kinetix setting allows us to control this factor by training RL experts under different levels of action noise before collecting demonstrations. As shown in Fig. 4, `DREAM-Chunk` scales more effectively with the same number of sampled chunks when the imitation policy is trained on demonstrations from experts exposed to higher action noise. In contrast, when the policy is trained only on demonstrations from experts trained with low action noise, e.g., _σ_ = 0 _._ 1, increasing the sample count provides smaller gains. This suggests that test-time scaling is most useful when the demonstration data already contains corrective behaviors that the learned policy can sample at inference time. 

**Latent representation matters.** We now study how the choice of auxiliary world model affects `DREAM-Chunk` . We evaluate several decoder1.0 free latent dynamics models, including an LEWM EB-JEPA Naive Async R2-Dreamer Policy Encoder Random Switch RSSM variant adapted from R2-Dreamer [23], 0.9 LeWorldModel (LEWM) [21], and energybased JEPA (EB-JEPA) [35]. For R2-Dreamer, 0.8 


we remove the reward and continuation predictors and train with only the Barlow Twins, dynamics, and representation losses. For LEWM and EB-JEPA, we use one-step prediction with latent regularization: SigReg for LEWM and VICReg [3] for EB-JEPA. We also test a variant that freezes the action-chunking policy encoder and trains only a one-step latent dynamics predictor. As references, we include naive openloop execution and a Random Switch baseline, 

Figure 5: Ablations on different world model architectures. All methods are evaluated under action noise _σ_ = 0 _._ 2, _N_ = 20 for `DREAM-Chunk` . 

which samples batched chunks but switches among them randomly during execution. 

Fig. 5 shows that latent representation strongly affects `DREAM-Chunk` performance. EB-JEPA degrades under longer execution horizons, likely because accumulated rollout errors make latent matching unreliable. Its performance remains above Random Switch, suggesting that its predictions retain some useful structure, but are insufficient for reliable long-horizon matching. In contrast, the frozen-policy-encoder variant regresses toward Random Switch, suggesting that these features, after the one-layer MLP projection, do not provide enough predictive information for identifying policy-intended future states. LEWM performs competitively and can even outperform the RSSM variant, indicating that `DREAM-Chunk` does not require an explicitly stochastic world model. Its core requirement is a latent representation and dynamics model that supports reliable phase-aligned matching among candidate chunks. 

### **5.2 Hardware Deployment** 

We evaluate `DREAM-Chunk` on real robot hardware to study whether it improves action-chunking policies under stochastic dynamics in physical manipulation. We focus on three sources of uncertainty that commonly arise in hardware deployment: (i) noisy execution due to hardware limitations (we 

7 


Figure 6: We design four hardware experiments on the SO-101 robot arm and Franka Emika Panda robot. The stochasticity mainly arises from inaccurate hardware execution on SO-101. In the movingobject grasping task, additional uncertainty comes from the uncertain velocity of the rolling object. In the last pick and insert can test, we manually perturb the target box before insertion. The figure shows representative failure modes caused by dynamic stochasticity. 

provide further discussion on servo precision in Appendix A1.2), (ii) partial observability of task state, and (iii) external perturbations that alter the environment during execution. We design four manipulation tasks across the SO-101 and Franka robot arms, with representative failure modes shown in Fig. 6. 

- (1) _Unplug and insert USB (SO-101):_ The robot unplugs a USB connector from the right port and inserts it into the left port. Limited motor precision can cause the connector to get stuck or miss the target port. 

- (2) _Catch and place moving object (SO-101):_ The robot catches a rolling object and places it into a basket. Varying object velocity and single-frame observation make the dynamics partially observed, leading to missed catches or inaccurate drops. 

- (3) _Pick and insert object (SO-101):_ The robot picks up a toy block and inserts it at the correct location. End-effector oscillations can cause grasp failures or inaccurate placement. 

- (4) _Insert can under perturbation (Franka):_ The robot picks up a can and inserts it into a target slot while the container is manually perturbed. Failure to react can cause missed insertion, while imprecise grasping can lead to dropping the can. 

**Implementation details.** We collect approximately 50 to 100 expert demonstration episodes per task through teleoperation. A key observation is consistent with our simulation results: `DREAM-Chunk` is most effective when demonstrations contain corrective behaviors that can be sampled as recovery options under rollout deviations. We fine-tune SmolVLA [32] for the SO-101 experiments and _π_ 0 _._ 5 [4] for the Franka experiment. All hardware experiments use the R2-Dreamer latent world model formulation, trained on the same offline demonstration dataset used for policy training. During evaluation, we set the control rate to 30 Hz for SO-101 and 10 Hz for Franka, matching the frame rates used during demonstration collection. For the four tasks, we use execution horizons of 30, 20, 30, and 10 steps, respectively. These horizons are chosen to be long enough to avoid frequent idle transitions in the demonstrations, while remaining short enough to support timely inference in dynamic tasks. 

**Computation hardware.** We report the overhead of test-time scaling under two hardware setups. SO-101/SmolVLA latency was measured on a workstation with an NVIDIA RTX 5090 GPU and Intel Core Ultra 9 CPU. Franka/ _π_ 0 _._ 5 latency was measured in a distributed setup, with robot control 

8 

on a local PC with an Intel i7-11700KF CPU and RTX 3080 GPU, and inference on a remote workstation with an AMD Threadripper PRO 5995WX CPU and RTX A6000 GPU communicating via WebSocket. All reported values are averaged over one test session. 

**Hardware results.** Tab. 1 reports the success rates on the hardware tasks using SmolVLA on the SO-101 platform, where `DREAM-Chunk` uses _N_ = 10 candidate chunks. `DREAM-Chunk` improves performance across all tasks, suggesting that reactive chunk selection helps mitigate uncertainty from hardware inaccuracy, partially observed object motion, and external perturbations. Tab. 2 further reports the performance and latency Table 1: Success rates over 20 rollouts on of _π_ 0 _._ 5 on the Franka arm. Under local inference, three SO-101 tests with SmolVLA. `DREAM-Chunk` with _N_ = 5 substantially improves the success rate over open-loop execution, although Task Open-loop Ours this setting uses sequential inference rather than paralUSB unplug/insert 75% **95%** lel batched sampling and therefore introduces visible Pick moving object 60% **80%** pauses during execution, as shown in the supplementary Pick and insert toy 35% **45%** videos. 

Next, we also evaluate remote inference to enable parallel sampling with larger candidate pools. Despite the added communication delay (1s), remote `DREAM-Chunk` still outperforms the local openloop baseline. However, increasing _N_ further does not improve performance, likely because the added inference delay offsets the benefits of within-chunk reactivity. We provide experiment videos in the supplementary material and summarize the observed failure modes in Tab. A1. 

Table 2: Performance and inference latency for the can insertion task with _π_ 0 _._ 5 on the Franka arm. 

|able 2: Performance<br>sertion task with_π_0_._|and i<br>5 on|nference latenc<br>the Franka arm|y for the can<br>.|Table<br>`DREAM`|3:<br>`-Chunk`|Latency<br>’s<br>world|breakdown<br>of<br>model<br>compo-|
|---|---|---|---|---|---|---|---|
|Method|_N_|Inference Time|Performance|nents.||||
|Naive open loop (local)|1|194.68 ms|10%|_N_|Encoder|Predictor|Latent Matching|
|`DREAM-Chunk`(local)<br>`DREAM-Chunk`(remote)|5<br>10|634.77 ms<br>697.93 ms|**65%**<br>40%|5<br>|1.41 ms<br>|1.83 ms<br>|0.16 ms<br>|
|`DREAM-Chunk`(remote)|15|1001.27 ms|30%|10<br>|1.40 ms<br>|2.74 ms<br>|0.17 ms<br>|
|`DREAM-Chunk`(remote)|20|1303.82 ms|35%|20|1.56 ms|3.09 ms|0.18 ms|


**Inference latency.** Tab. 2 also reports the inference latency of _π_ 0 _._ 5 under different sample sizes and hardware settings. Policy inference becomes slower as the number of sampled chunks increases, but the measured latency does not grow linearly with _N_ . In contrast, Tab. 3 shows that the worldmodel-related computation remains at the millisecond level: increasing the batched latent rollout from _N_ = 5 to _N_ = 20 adds only about 1 _._ 2 ms of delay. We additionally report the inference latency of SmolVLA in Tab. A2. 

**Nature of the corrective behaviors.** Although we initially expected `DREAM-Chunk` to produce more apparent within-chunk reactivity, such as switching to a substantially different behavior mode to catch a missed moving object as illustrated in Fig. 1, the observed corrections are mostly local variations around the current action mode. This is consistent with the analysis by Pan et al. [26], which suggests that the strength of generative policies often lies less in distributional learning and more in iterative refinement around likely actions. In our hardware experiments, sampled action chunks rarely exhibit distinct high-level modes. Instead, they mainly provide small corrective variations around an imperfect nominal behavior. Consequently, increasing the number of samples in `DREAM-Chunk` helps primarily by exposing more of these local correction options, rather than by discovering qualitatively different strategies. 

## **6 Conclusion** 

We presented `DREAM-Chunk` , a test-time scaling method for improving the reactivity of actionchunking policies under stochastic dynamics. `DREAM-Chunk` samples multiple candidate chunks, rolls out their latent consequences with a lightweight world model, and selects actions through latent matching at each step, enabling online correction. In Kinetix, our approach’s gains increase with stochasticity and sample count, and depend on corrective behaviors in the demonstration data and reliable latent dynamics. On real hardware, `DREAM-Chunk` improves performance across four manipulation tasks involving execution noise, partial observability, and external perturbations. These results suggest that lightweight predictive models can act as practical reactive modules for robust long-horizon VLA control. 

9 

## **References** 

- [1] Eloi Alonso, Adam Jelley, Vincent Micheli, Anssi Kanervisto, Amos Storkey, Tim Pearce, and François Fleuret. Diffusion for world modeling: Visual details matter in atari. In _Proc. NeurIPS_ , 2024. 3 

- [2] Juan Alvarez-Padilla, John Z Zhang, Sofia Kwok, John M Dolan, and Zachary Manchester. Real-time whole-body control of legged robots with model-predictive path integral control. In _Proc. ICRA_ , 2025. 16 

- [3] Adrien Bardes, Jean Ponce, and Yann LeCun. VICReg: Variance-invariance-covariance regularization for self-supervised learning. In _Proc. ICLR_ , 2022. 7 

- [4] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. In _Proc. CoRL_ , 2025. 1, 2, 8 

- [5] Kevin Black, Manuel Y. Galliker, and Sergey Levine. Real-time execution of action chunking flow policies. In _Proc. NeurIPS_ , 2026. 2, 6 

- [6] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. WorldVLA: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 1, 3 

- [7] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _IJRR_ , 2025. 2 

- [8] Franka Emika GmbH. Panda Technical Data. `https://www.generationrobots.com/med ia/panda-franka-emika-datasheet.pdf` , 2018. Datasheet, accessed 2026-05-04. 14 

- [9] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing AI into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 1 

- [10] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2019. 3 

- [11] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 5 

- [12] Bohan Hou, Gen Li, Jindou Jia, Tuo An, Xinying Guo, Sicong Leng, Haoran Geng, Yanjie Ze, Tatsuya Harada, Philip Torr, et al. World model for robot learning: A comprehensive survey. _arXiv preprint arXiv:2605.00080_ , 2026. 2 

- [13] Hugging Face LeRobot. SO-101. `https://huggingface.co/docs/lerobot/so101` , 2026. LeRobot documentation, accessed 2026-05-04. 14 

- [14] Joonkyung Kim, Wenxi Chen, Davood Soleymanzadeh, Yi Ding, Xiangbo Gao, Zhengzhong Tu, Ruqi Zhang, Fan Fei, Sushant Veer, Yiwei Lyu, et al. Modular safety guardrails are necessary for foundation-model-enabled robots in the real world. _arXiv preprint arXiv:2602.04056_ , 2026. 2 

- [15] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. OpenVLA: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 2 

10 

- [16] Jacky Kwok, Christopher Agia, Rohan Sinha, Matt Foutter, Shulu Li, Ion Stoica, Azalia Mirhoseini, and Marco Pavone. Robomonkey: Scaling test-time sampling and verification for vision-language-action models. _arXiv preprint arXiv:2506.17811_ , 2025. 3 

- [17] Michael Laskey, Jonathan Lee, Roy Fox, Anca Dragan, and Ken Goldberg. Dart: Noise injection for robust imitation learning. In _Proc. CoRL_ , 2017. 2 

- [18] Yann LeCun et al. A path towards autonomous machine intelligence version 0.9.2, 2022-06-27. _OpenReview_ , 2022. 5 

- [19] Yuanchang Liang, Xiaobo Wang, Kai Wang, Shuo Wang, Xiaojiang Peng, Haoyu Chen, David Kim Huat Chua, and Prahlad Vadakkepat. Adaptive action chunking at inference-time for vision-language-action models. _arXiv preprint arXiv:2604.04161_ , 2026. 2, 3, 16 

- [20] Yuejiang Liu, Jubayer Ibn Hamid, Annie Xie, Yoonho Lee, Max Du, and Chelsea Finn. Bidirectional decoding: Improving action chunking via guided test-time sampling. In _Proc. ICLR_ , 2025. 2, 4, 6, 16 

- [21] Lucas Maes, Quentin Le Lidec, Damien Scieur, Yann LeCun, and Randall Balestriero. LeWorldModel: Stable end-to-end joint-embedding predictive architecture from pixels. _arXiv preprint arXiv:2603.19312_ , 2026. 2, 3, 5, 7, 14 

- [22] Michael Matthews, Michael Beukman, Chris Lu, and Jakob Nicolaus Foerster. Kinetix: Investigating the training of general agents through open-ended physics-based control tasks. In _Proc. ICLR_ , 2025. 2, 6 

- [23] Naoki Morihira, Amal Nahar, Kartik Bharadwaj, Yasuhiro Kato, Akinobu Hayashi, and Tatsuya Harada. R2-Dreamer: Redundancy-reduced world models without decoders or augmentation. In _Proc. ICLR_ , 2026. 2, 3, 5, 6, 7 

- [24] Chaojun Ni, Cheng Chen, Xiaofeng Wang, Zheng Zhu, Wenzhao Zheng, Boyuan Wang, Tianrun Chen, Guosheng Zhao, Haoyun Li, Zhehao Dong, et al. SwiftVLA: Unlocking spatiotemporal dynamics for lightweight VLA models at minimal overhead. _arXiv preprint arXiv:2512.00903_ , 2025. 1, 3 

- [25] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 2 

- [26] Chaoyi Pan, Giri Anantharaman, Nai-Chieh Huang, Claire Jin, Daniel Pfrommer, Chenyang Yuan, Frank Permenter, Guannan Qu, Nicholas Boffi, Guanya Shi, et al. Much ado about noising: Dispelling the myths of generative robotic control. _arXiv preprint arXiv:2512.01809_ , 2025. 2, 9 

- [27] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. FAST: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 2 

- [28] Physical Intelligence. _π_ 0.7: A steerable model with emergent capabilities. `https://www.pi .website/blog/pi07` , 2026. Blog post, accessed April 20, 2026. 1, 2 

- [29] Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, et al. _π_ 0<sup>_∗_</sup> _._ 6<sup>:a VLA</sup> that learns from experience. _arXiv preprint arXiv:2511.14759_ , 2025. 2 

- [30] Robo9. Testing of feetech sts3215 servomotor: Backlash, repeatability, and torque. `https: //robonine.com/testing-of-feetech-sts3215-servomotor-backlash-repeatabi lity-and-torque/` , 2025. Accessed: 2026-05-04. 14 

- [31] Kohei Sendai, Maxime Alvarez, Tatsuya Matsushima, Yutaka Matsuo, and Yusuke Iwasawa. Leave no observation behind: Real-time correction for VLA action chunks. _arXiv preprint arXiv:2509.23224_ , 2025. 2 

11 

- [32] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. SmolVLA: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 2, 6, 8 

- [33] Junhyuk So, Chiwoong Lee, Shinyoung Lee, Jungseul Ok, and Eunhyeok Park. Improving generative behavior cloning via self-guidance and adaptive chunking. In _Proc. NeurIPS_ , 2025. 2, 6 

- [34] Jiaming Tang, Yufei Sun, Yilong Zhao, Shang Yang, Yujun Lin, Zhuoyang Zhang, James Hou, Yao Lu, Zhijian Liu, and Song Han. Vlash: Real-time vlas via future-state-aware asynchronous inference. _arXiv preprint arXiv:2512.01031_ , 2025. 2, 6 

- [35] Basile Terver, Randall Balestriero, Megi Dervishi, David Fan, Quentin Garrido, Tushar Nagarajan, Koustuv Sinha, Wancong Zhang, Mike Rabbat, Yann LeCun, et al. A lightweight library for energy-based joint-embedding predictive architectures. _arXiv preprint arXiv:2602.03604_ , 2026. 2, 3, 7, 14 

- [36] Yilin Wu, Ran Tian, Gokul Swamy, and Andrea Bajcsy. From foresight to forethought: VLMin-the-loop policy steering via latent alignment. _arXiv preprint arXiv:2502.01828_ , 2025. 3 

- [37] Haozhe Xie, Beichen Wen, Jiarui Zheng, Zhaoxi Chen, Fangzhou Hong, Haiwen Diao, and Ziwei Liu. DynamicVLA: A vision-language-action model for dynamic object manipulation. _arXiv preprint arXiv:2601.22153_ , 2026. 2 

- [38] Charles Xu, Jost Tobias Springenberg, Michael Equi, Ali Amin, Adnan Esmail, Sergey Levine, and Liyiming Ke. Precise manipulation with efficient online RL. `https://www.pi.website /research/rlt` , 2026. Research blog post, accessed April 20, 2026. 2 

- [39] Angen Ye, Boyuan Wang, Chaojun Ni, Guan Huang, Guosheng Zhao, Hao Li, Hengtao Li, Jie Li, Jindi Lv, Jingyu Liu, et al. GigaWorld-Policy: An efficient action-centered world–action model. _arXiv preprint arXiv:2603.17240_ , 2026. 1, 3 

- [40] Jiyao Zhang, Zimu Han, Junhan Wang, Xionghao Wu, Shihong Lin, Jinzhou Li, Hongwei Fan, Ruihai Wu, Dongjiang Li, and Hao Dong. HiPolicy: Hierarchical multi-frequency action chunking for policy learning. _arXiv preprint arXiv:2604.06067_ , 2026. 3 

- [41] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _Proc. RSS_ , 2023. 2 

- [42] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. RT-2: Vision-language-action models transfer web knowledge to robotic control. In _Proc. CoRL_ , 2023. 1, 2 

12 

## **A1 Technical appendices and supplementary material** 

### **A1.1 Additional Experiment Results** 


Figure A1: Solve rates across 12 environments in Kinetix with action noise _σ_ = 0 _._ 2. Adaptive chunking method is considered not to have a fixed execution horizon, and we report its performance as a horizontal line. 

Table A1: Failure modes observed in hardware experiments. 

|**Task**|**Failure mode**|**DreamChunk**|**Open-loop**|
|---|---|---|---|
||Inaccurate placement|3|5|
|Toy stacking|Missed grasp|5|8|
||Stuck in placement|3|0|
|G i bt|Failed to intercept|4|6|
|rasp movng ojec|Inaccurate placement|0|2|
|USB l d it|Stuck at unplugging|0|3|
|unpug an nser|Incorrect-angle insertion|1|2|
|C ii ll_N_5|Failed to pick up|0|9|
|an nserton (oca  =)|Missed insertion|7|9|


We provide the additional experiment results in this section. Figure. A1 display the performance in 12 Kinetix environments at different execution horizon with inference delay _d_ = 1 and action noise _σ_ = 0 _._ 2. 

As shown in Table A2, increasing the number of sampled chunks raises the action-inference latency of SmolVLA from 129.25 ms for the baseline to 303.70 ms, 326.72 ms, and 358.51 ms for 

13 

`DREAM-Chunk` with _N_ = 5, 10, and 15, respectively. In contrast, the additional world-model computation is lightweight: encoding, latent prediction, and latent matching take only 4.64 ms, 2.36 ms, and 0.20 ms, respectively. 

### **A1.2 Implementation Details** 

**World model architecture in simulation.** For the R2-Dreamer world model, we use MLP modules together with a GRU-like recurrent transition to process vector observation from Kinetix environment. Since the observation vector has length around 700, the observation encoder is a two-layer MLP with dimensions `obs_dim` _→_ 512 _→_ 256. The prior and posterior RSSM heads use hidden size 512, with two hidden layers for the prior and one hidden layer for the posterior by default. The deterministic dynamics are implemented with a blockwise GRU update using deterministic width 256, a stochastic state of size 32 _×_ 16 flattened to 512 dimensions, transition hidden size 512, one tran- 

Table A2: Inference latency of SmolVLA and RSSM for SO-101 tests. 

|Component|Latency (ms)|
|---|---|
|Baseline inference|129.25|
|Action inference,_N_ = 5|303.70|
|Action inference,_N_ = 10|326.72|
|Action inference,_N_ = 15|358.51|
|WM encoder|4.64|
|WM predictor|2.36|
|WM latent matching|0.20|


sition hidden layer, and 8 blocks. For deterministic JEPA-style world models including EB-JEPA and LEWM, we use a fully MLP-based architecture without recurrent dynamics. The model consists of an observation encoder `obs_dim` _→_ 512 _→_ 256, an action encoder `action_dim` _→_ 256 _→_ 256, a predictor with one hidden stage that maps the concatenated observation-action representation from 256 + 256 dimensions to a 512-dimensional hidden layer and then to a 256-dimensional output with residual connection and LayerNorm, and a projector 256 _→_ 512 _→_ 256. LEWM and EB-JEPA differ only in their latent regularization objective: LEWM uses SIGReg [21], whereas EB-JEPA uses variance-covariance regularization [35]. 

**Hardware-induced execution uncertainty.** We further clarify the uncertainty introduced by imprecise hardware execution in our experimental task design. The low-cost SO-101 arm uses Feetech STS3215 bus servos, whose manufacturer specifications report a nominal encoder resolution of 0 _._ 088<sup>_◦_</sup> and a gearbox backlash limit of 0 _._ 5<sup>_◦_</sup> [13]. An independent online test of the same servo model reported that practical backlash can exceed this nominal limit and lead to millimeter-scale endeffector displacement on an 86 mm single-link setup [30]. Consistent with this observation, we found that the SO-101 end-effector position is affected by accumulated errors across multiple servo joints, making precise manipulation challenging even during teleoperation. As a point of comparison, the industrial-grade Franka Emika Panda provides substantially higher positioning precision: its official datasheet specifies a 7-DoF arm with 855 mm reach, 3 kg payload, and end-effector repeatability of _±_ 0 _._ 1 mm [8]. This contrast highlights that our SO-101 experiments are conducted on a low-cost hardware platform with non-negligible actuation uncertainty. 

### **A1.3 Analysis of Reactivity** 

**Reactivity failure.** We provide a simplified analysis to relate `DREAM-Chunk` to the reactive objective in Eq. (2). Recall that _J_ react( _η_ ) measures whether an execution strategy _η_ selects actions that remain aligned with the decision that the same policy would make if re-inferred from the realized observation. We say that a reactivity failure occurs at phase _τ_ when the executed action has low alignment with the current policy decision, Align( _a_<sup>_η_</sup> _t_ + _τ_<sup>_, ot_+</sup><sup>_τ_)</sup><sup>_< ϵ_align</sup><sup>_,_</sup> (A7) 

where _ϵ_ align is an alignment threshold. This definition captures the central issue of open-loop chunk execution: stochastic dynamics, partial observability, or execution noise can move the system to a realized observation where the remaining actions in the originally sampled chunk no longer match what the policy would choose if queried again. 

**Open-loop misalignment.** Let _p_ dyn denote the per-step probability that such a stochastic deviation causes the open-loop action from the original chunk to become misaligned with the policy decision conditioned on the realized observation. For a standard open-loop execution strategy _η_ open that executes the original chunk for horizon _H_ , the probability that no such misalignment occurs during 

14 

the execution window is 


Therefore, the probability that open-loop execution encounters at least one phase that degrades _J_ react( _η_ open) is 


This expression captures the benefit of shortening the execution horizon: a smaller _H_ reduces the chance that the policy continues executing stale actions before the next inference step. 

**Candidate coverage.** `DREAM-Chunk` takes a different approach. Instead of shortening the execution horizon, it keeps a longer horizon but samples multiple candidate chunks and uses the world model to maintain a pool of phase-aligned dreamed future states. Let _pδ_ denote the probability that one sampled chunk contains, at execution phase _δ_ , an action whose dreamed latent state is compatible with the realized observation and whose action is therefore aligned with the policy decision re-inferred at that observation. This probability is induced by the policy distribution and depends on whether the learned policy can sample corrective actions around perturbed rollouts. With _N_ independently sampled chunks, the probability that at least one candidate provides an aligned corrective action at phase _δ_ is 


This is the same coverage effect measured empirically by the nearest-dreamed-state distance: increasing _N_ makes it more likely that the dreamed-state pool contains a candidate close to the realized trajectory, which serves as a surrogate for higher alignment under _J_ react( _η_ ). 

**World-model reliability.** However, coverage alone is not sufficient. `DREAM-Chunk` also requires the auxiliary world model to provide a latent space in which phase-aligned matching can identify the candidate whose action is most compatible with the realized observation. We therefore introduce a reliability term _r_ wm _∈_ [0 _,_ 1], which represents the probability that latent matching selects an aligned corrective chunk when such a chunk exists in the candidate pool. The effective probability that a stochastic deviation can be corrected is approximated as 


Accordingly, the per-step probability that a misalignment occurs and remains unrecovered is 


For `DREAM-Chunk` with a longer execution horizon _HL_ , the probability of encountering at least one unrecovered misalignment can be approximated as 


**Comparison with shorter-horizon execution.** Now consider a shorter-horizon baseline with execution horizon _HS < HL_ . Since it does not maintain a candidate pool for within-horizon correction, its probability of encountering at least one misalignment is 


`DREAM-Chunk` is expected to achieve higher reactivity than this shorter-horizon baseline when it has a smaller probability of unrecovered misalignment: 


Substituting the two failure probabilities gives 


Equivalently, 


For small _p_ dyn, using the first-order approximation (1 _− x_ )<sup>_H_</sup> _≈_ 1 _− Hx_ , this condition becomes 


15 

When _p_ dyn _>_ 0, we can cancel _p_ dyn and obtain 


This inequality gives a simple interpretation of the trade-off. A longer-horizon `DREAM-Chunk` strategy can compensate for its larger exposure to stochastic deviations if its candidate pool is sufficiently likely to contain an aligned corrective action and if the world model can reliably identify that candidate. In other words, shortening the execution horizon reduces the probability that stale actions become misaligned, whereas `DREAM-Chunk` increases the probability that an aligned correction is available when misalignment occurs. 

**Implications.** This analysis also clarifies when `DREAM-Chunk` should be effective. The coverage term _P_ cover( _N, δ_ ) depends on the diversity of sampled action chunks and on whether the demonstration data contains corrective behaviors that the learned policy can sample. If the policy distribution only produces small variations around a nominal trajectory and the demonstrations do not contain recovery behaviors, then _pδ_ remains small and increasing _N_ provides limited benefit. In contrast, when demonstrations include reactions to stochastic dynamics, increasing _N_ can expose more local correction options and improve the chance of maintaining high _J_ react( _η_ ). The world-model reliability term _r_ wm is equally important: even if the candidate pool contains an aligned corrective action, `DREAM-Chunk` can only use it when the learned latent dynamics and matching metric correctly identify the candidate whose dreamed state is compatible with the realized observation. Meanwhile, _p_ dyn is determined by the environment and hardware: stronger action noise, partial observability, external perturbations, or low-precision actuation all increase the probability that open-loop actions become misaligned with the realized observation. Thus, `DREAM-Chunk` is most useful in an intermediate regime where stochastic deviations occur often enough that open-loop execution becomes brittle, but the learned policy and world model still provide enough corrective coverage and matching reliability for latent matching to recover. 

### **A1.4 Discussion** 

**Limitation.** The proposed method requires additional computational resources at test time to sample batched action chunks, which is deployable using remote reasoning on a PC but the sample size would be much more limited at edge device. We also discussed the nature of corrective behavior is largely confined by the expressiveness of generative policies, our experiment shows the sampled action chunks does not have distinct mode different, limiting `DREAM-Chunk` to demonstrate significant strategy change during within-chunk execution. Further, the effectiveness of proposed methods depends on whether expert demonstration includes responses to stochastic dynamics, posing requirement in data collection. 

**Extension.** We aim to let the proposed method innovate the use of world models in VLA studies, taken inspirations from well-established model-based robotics studies like model predictive control, robust control, and model predictive path integral [2]. Since `DREAM-Chunk` method samples multiple action chunks at test-time, it can also be integrated with other test-time scaling algorithms. For instance, adding the backward loss from BID [20] into chunk selection can improve cross-chunk consistency, apply cross-chunk entropy [19], and provide measures on adaptively changing execution horizon. To reduce the overhead of batched action sampling, future implementations could amortize VLM backbone inference by computing the visual-language embedding once and reusing it across candidate chunks, while sampling different noise inputs in the action expert to generate diverse actions. 

**Social impact.** This work contributes to embodied intelligence and robot learning by improving the robustness of robot policies under stochastic dynamics, hardware uncertainty, and partial observability. Such capabilities could benefit assistive robotics, manufacturing, and logistics, where safer and more adaptive robot behavior is valuable. However, more robust robot policies may also increase risks in harmful or poorly regulated applications, including weaponized automation, unsafe autonomous systems. Broader advances in robotic automation may also affect labor demand in some sectors. These risks are not unique to `DREAM-Chunk` , but motivate task-specific safety constraints, human oversight, misuse monitoring, and deployment restrictions in high-risk domains. 

16 

