---
title: "Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control"
date: "2026-05-14"
authors: "Haozhe Jia; Honglei Jin; Yuan Zhang; Youcheng Fan; Shaofeng Liang; Lei Wang"
url: https://arxiv.org/abs/2605.14417
pdf: https://arxiv.org/pdf/2605.14417
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.14417)** / [論文ページ](https://arxiv.org/abs/2605.14417)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**DAJI** 

# **Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control** 

Haozhe Jia<sup>†1,2</sup> , Honglei Jin<sup>†1</sup> , Yuan Zhang<sup>†3</sup> , Youcheng Fan<sup>†1</sup> , Shaofeng Liang<sup>1</sup> , Lei Wang<sup>5,6</sup> , Shuxu Jin<sup>3</sup> , Kuimou Yu<sup>1</sup> , Zinuo Zhang<sup>3</sup> , Jianfei Song<sup>2</sup> , Wenshuo Chen<sup>*1,2</sup> and Yutao Yue<sup>*1,4</sup> 

_1The Hong Kong University of Science and Technology (Guangzhou)._ 

_2LimX Dynamics Technology Co., Ltd._ 

_3Shandong University._ 

_4Institute of Deep Perception Technology, Jiangsu Industrial Technology Research Institute (JITRI)._ 

_5Data61/CSIRO._ 

- _6Griffith University._ 

Draft prepared for arXiv on May 21, 2026 

### **Abstract** 

Natural language is an intuitive interface for humanoid robots, yet streaming whole-body control requires control representations that are executable now and anticipatory of future physical transitions. Existing language-conditioned humanoid systems typically generate kinematic references that a low-level tracker must repair reactively, or use latent/action policies whose outputs do not explicitly encode upcoming contact changes, support transfers, and balance preparation. We propose **DAJI** ( _Dynamics-Aligned Joint Intent_ ), a hierarchical framework that learns an anticipatory joint-intent interface between language generation and closed-loop control. DAJI-Act distills a future-aware teacher into a deployable diffusion action policy through student-driven rollouts, while DAJI-Flow autoregressively generates future intent chunks from language and intent history. Experiments show that DAJI achieves strong results in anticipatory latent learning, single-instruction generation, and streaming instruction following, reaching 94.42% rollout success on HumanML3D-style generation and 0.152 subsequence FID on BABEL. 

� **Project Page:** https://hxxxz0.github.io/DAJI_PAGE/ 

**Keywords:** _Humanoid control, Language-conditioned control, Streaming generation, Joint intent, Diffusion policy_ 

- Corresponding author: Yutao Yue. 

co-first authors. 

> † Haozhe Jia, Honglei Jin, Yuan Zhang, and Youcheng Fan contributed equally as 


**Figure 1. Teaser of DAJI.** Instead of using reference trajectories as the deployment interface, DAJI predicts executable and anticipatory joint-intent latents that improve future prediction and long-horizon humanoid control. 

**1** –20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

## **1. INTRODUCTION** 

**N** atural language is becoming a practical interface for humanoidrobots because it allows non-expert users to specify goals, styles, and temporal changes without teleoperation [10, 12]. This paper studies language-conditioned humanoid whole-body control in a streaming setting: given a language instruction and the robot’s recent motion history, the system should continuously produce behavior that is semantically aligned, physically executable, and extendable over long horizons. The central question is therefore not only how to generate plausible motion from language, but what intermediate representation should connect language understanding, motion generation, and closed-loop humanoid control [15, 16]. 

Recent progress has moved this problem beyond offline text-tomotion generation. Diffusion, flow-matching, and autoregressive motion models can synthesize diverse human motions from language [12– 14, 21–23, 27], and streaming generators improve online kinematic continuity by conditioning on motion history and incremental text inputs [39]. However, these models are mainly optimized in a kinematic space and do not specify how a humanoid robot should realize the motion under contact, balance, actuation, and feedback. Reference-driven humanoid systems address this by generating human or robot-native motion references and executing them with tracking policies [40, 44, 45]. This modular design has enabled impressive demonstrations, but the generated reference remains an external target: when its contact timing, root momentum, support transition, or recovery behavior is inconsistent with the robot’s current state, the tracker can only react by compromising either tracking accuracy or stability. Latent-driven or end-to-end approaches further reduce explicit retargeting by coupling language, motion latents, and policies more tightly [32, 33, 36, 38, 46]. Yet these latents are often treated as semantic skill codes, compact motion descriptors, or direct actionconditioning variables, rather than as closed-loop motor intents that also express what the body must prepare for next. 

This limitation is especially consequential in streaming deployment, where generated chunks are not independent clips: each execution alters the robot’s contact state, center of mass, momentum, and feasible continuation set. Consequently, a segment may be locally executable yet fundamentally myopic. Complex maneuvers, such as stepping, turning, or balance recovery require preparatory support shifts and angular-momentum regulation well before the primary motion manifests. Inspired by anticipatory postural adjustment (APA) in human motor control [1, 2], we argue that the key interface for languageconditioned humanoid control should be an anticipatory motor intent. This interface must remain executable under live proprioception while simultaneously encoding coarse future tendencies across contacts, balance shifts, and task progression. 

To this end, we propose _Dynamics-Aligned Joint Intent_ ( **DAJI** ), a hierarchical framework for streaming language-conditioned humanoid control. At deployment, DAJI replaces motion references with a closed-loop joint-intent interface between semantic generation and control [6, 18]. Instead of generating poses for a tracker, it learns compact intents through controller interaction, unlike decoupled latent skill spaces [20]. To make these intents anticipatory, a privileged teacher uses multi-horizon future references to capture upcoming support shifts, contact transitions, and balance demands. We then distill **DAJI-Act** in loop, so the policy is trained under its own closedloop state distribution. This shapes the latent space around humanoid dynamics and recovery, rather than offline reconstruction alone. 

On top of this executable intent space, DAJI trains **DAJI-Flow** , a language-conditioned flow-matching generator that autoregressively predicts future intent chunks. DAJI-Flow conditions on the language instruction and a compact encoding of recent joint-intent latent history, while scheduled self-conditioning exposes the generator to its own previously generated histories during training. At deployment, each generated joint intent is decoded with live proprioception by **DAJI-Act** , a lightweight diffusion action policy, into high-frequency 

joint-position actions. In this way, DAJI decouples semantic generation from feedback control while maintaining a shared representation that is both executable and anticipatory. Experiments show that the learned joint-intent latent contains information about upcoming motion transitions, improves temporal coherence over non-anticipatory alternatives, and leads to better long-horizon closed-loop success. These results support our central claim: for language-conditioned humanoid control, the interface between generation and control should not merely describe the desired motion; it should help prepare the body for what comes next. 

Our contributions are summarized as follows: 

- We propose an anticipatory intent-generation paradigm for streaming language-conditioned humanoid control, addressing the mismatch between language-conditioned semantic planning and closed-loop physical execution through predictive jointintent generation. 

- We introduce a dynamics-aligned joint-intent representation that couples immediate closed-loop executability with future motion tendency, enabling the controller to act on both the current command and the upcoming transition. 

- We propose DAJI, a hierarchical generation-to-execution framework that learns joint intents through future-aware privileged control and student-driven in-loop distillation, then generates them with language-conditioned flow matching and scheduled self-conditioning for long-horizon humanoid execution. 

## **2. RELATED WORK** 

**Reference interfaces for language-driven humanoids.** Languageconditioned humanoid control commonly converts instructions into motion targets that a robot controller can execute. This line builds on text-to-motion priors and generative models [4, 11–14, 21, 22, 26, 29]. Harmon uses human motion priors and VLM-based refinement to synthesize text-aligned humanoid motions [24]. FRoM-W1 generates whole-body human motions and then retargets and tracks them on humanoids [44]. TextOp makes this pipeline interactive by streaming short-horizon robot-skeleton references [45], while ECHO improves deployability with a compact robot-native representation between a cloud generator and an edge tracker [40]. These systems show that reference-based modularity is practical. However, the generated command remains a trajectory-like target. When its contact timing, support transition, momentum, or recovery behavior is inconsistent with the robot’s current state, the low-level policy must repair the mismatch reactively. DAJI instead uses a controller-distilled joint intent as the generation-control interface, so the command is learned to be executable rather than merely trackable. 

**Latent and streaming interfaces.** Recent methods reduce explicit retargeting by coupling language, latents, and whole-body policies more tightly. LangWBC trains an end-to-end language-conditioned policy with a CVAE latent structure [36]. RoboGhost conditions a diffusion policy on language-grounded motion latents and bypasses explicit motion decoding [33]. RoboForge further optimizes latentdriven generation with physical plausibility feedback [46]. SENTINEL directly predicts action chunks from language and proprioception [38], and UniAct uses a shared discrete codebook with a causal streaming pipeline for multimodal humanoid control [32]. More broadly, recent representation-centric work has explored structured generative spaces and physics-informed alignment objectives in adjacent domains [30, 35]. These works move beyond pure reference tracking, but the latent or action interface is not necessarily trained as an anticipatory command under its own closed-loop rollout. MotionStreamer shows that causal latents and self-conditioned autoregression help reduce delay and error accumulation in streaming human motion generation [39]. Unlike planner-controller unification strategies that merge planning and control into one model, DAJI keeps a modular hierarchy and 

2–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 


**Figure 2. DAJI framework.** DAJI separates online deployment and offline training. **DAJI-Flow** predicts joint-intent latents from language and latent history, while **DAJI-Act** decodes each intent with live proprioception. DAJI-Act learns the executable joint-intent interface through student-driven in-the-loop distillation from a future-aware privileged teacher. 

learns the interface between the two modules: **DAJI-Flow** generates future joint intents, while **DAJI-Act** executes them under closed-loop feedback. 

teacher actions with live proprioception. Although the bottleneck uses a Gaussian posterior and KL regularization, the latent is optimized as an executable control command rather than a reconstruction target. 

## **3. METHOD** 

We present DAJI, a hierarchical framework that maps language instructions to executable latent commands for humanoid whole-body control. The key design is a _joint-intent_ interface. Instead of asking a generator to produce kinematic references that a tracker must follow, DAJI generates compact latent intents that are learned through closed-loop control and can be decoded into joint-position actions. 

**Future-aware teacher.** A locally conditioned controller may track the current pose but fail to prepare for future transitions such as stepping, turning, or balance recovery. We therefore train a privileged teacher that observes not only the current robot state but also multi-horizon reference information. At time 𝑡, the teacher policy is 


### **3.1. Overview** 

Given a language instruction ℒ and recent robot observations, DAJI generates joint-position actions 𝐚1∶𝑇 over a rollout horizon 𝑇 while supporting streaming extension. We use 𝐨<sup>prop</sup> 𝑡 for deployable proprioception, 𝐨<sup>ref</sup> 𝑡 for training-time reference observations, and 𝐨<sup>priv</sup> 𝑡 for simulator-only privileged observations unavailable at deployment. Observation details are provided in Appendices B.1 and B.3.1. 

Instead of generating kinematic references that must be repaired by a low-level tracker, DAJI learns a joint-intent latent 𝐳𝑡 ∈ℝ<sup>𝑑𝑧</sup> as the interface between semantic generation and physical execution. This latent is both _executable_ , since DAJI-Act decodes it into stable whole-body actions using live proprioception, and _anticipatory_ , since it captures coarse information about upcoming contacts, balance shifts, and task progression. 

DAJI consists of two modules trained sequentially. **DAJI-Act** learns the executable joint-intent interface by distilling a future-aware privileged teacher into a deployable diffusion action policy through a stochastic intent bottleneck. During distillation, DAJI-Act drives the simulator itself, so the interface is trained on the student’s closedloop state distribution. **DAJI-Flow** then learns to autoregressively generate future joint-intent chunks from language and recent intent history. At deployment, DAJI-Flow predicts low-frequency intent chunks, while DAJI-Act decodes each latent with live proprioception at the control frequency. 

### **3.2. Learning DAJI-Act: Executable Joint-Intent Policy** 

DAJI-Act is the low-level module that decodes joint-intent latents into robot actions. It uses a stochastic intent bottleneck to compress futureaware reference information and a diffusion action head to imitate 

where 𝐨<sup>ref</sup> 𝑡 includes future target frames. The teacher is optimized with PPO [5] under whole-body tracking and robustness rewards. Our reward design follows common humanoid motion-tracking objectives and adapts selected tracking and regularization terms from recent compliance-aware whole-body tracking work [34]. Reward definitions, observation groups, symmetry augmentation, and domain randomization are provided in Appendix B.3.1. The teacher is used as a source of future-aware control behavior that will be compressed into the joint-intent latent. 

**Student-driven in-loop distillation.** Teacher-driven imitation collects states visited by the teacher, but the deployable policy must act under its own rollout distribution. DAJI therefore performs in-loop distillation on DAJI-Act-induced states. At each step, DAJI-Act decodes a joint-intent-conditioned action and applies it to the simulator. The frozen teacher then evaluates the same state and provides the target action 𝐚𝑡<sup>tea.This trains the intent bottleneck and diffusion action head</sup> under the distribution they will encounter at deployment. DAJI-Act has three parts: a proprioceptive encoder 𝐸prop, a stochastic intent encoder 𝐸ref , and a diffusion action head. The intent encoder 𝐸ref , parameterized by 𝜓, maps 𝐨<sup>ref</sup> 𝑡 to the stochastic intent distribution 𝑞𝜓(𝐳𝑡|𝐨𝑡<sup>ref) = 𝒩(𝝁</sup> 𝑡<sup>, diag(𝝈2</sup> 𝑡<sup>)), where 𝝁</sup> 𝑡<sup>and 𝝈</sup> 𝑡<sup>2denote the mean and</sup> variance of the intent distribution. We sample the latent by 


The control context is 𝐜𝑡 = [𝐸prop(𝐨𝑡<sup>prop</sup> ); 𝐳𝑡]. Given a noised teacher action 𝐱𝜏 at diffusion timestep 𝜏, 


3–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 


**Figure 3. Tracker-level rollout visualization in simulation.** DAJI decodes generated joint-intent latents into continuous whole-body humanoid motions, including dynamic and highly articulated behaviors. 

wherē 𝛼𝜏 is the cumulative noise schedule. Conditioned on 𝐜𝑡, a lightweight denoiser 𝒟𝜙 predicts the clean action. The DAJI-Act objective is 


Here, 𝛽 is the KL regularization weight. The first term trains the diffusion action head to imitate future-aware teacher actions on studentvisited states. The second term regularizes the stochastic joint-intent bottleneck so that the resulting intent space remains compact and smooth enough for DAJI-Flow. Since the latent is decoded into actions rather than reconstructed references, DAJI-Act should be understood as an executable intent policy rather than a reconstruction module. After distillation, we encode all retargeted reference motions into latent trajectories using the mean intent code from the intent encoder. These text–intent trajectory pairs train DAJI-Flow. The training-only intent encoder is discarded at deployment; DAJI-Act executes generated intents using only live proprioception. 

we use the path 𝐗𝑠 = (1 −𝑠)𝝐+ 𝑠𝐗0 and train the velocity field with 


At inference, the ODE is integrated for a small number of Euler steps, the resulting chunk is appended to the latent history, and generation continues autoregressively. DAJI-Flow therefore predicts executable future intent tendencies, while DAJI-Act handles high-frequency feedback, perturbation compensation, and contact-level stabilization. 

**Scheduled self-conditioning.** Teacher-forced training conditions DAJI-Flow on ground-truth latent histories, whereas deployment conditions it on its own previous predictions. To reduce this exposure bias, we train the generator with multi-chunk self-conditioning. The first chunk is predicted from ground-truth history; subsequent chunks are conditioned on a history buffer augmented with previously generated latent chunks. These generated chunks are detached before being appended to the history buffer. In our default setting, self-conditioning is disabled for the first 100k steps and linearly ramped to probability 1 over the next 40k steps. Details are provided in Appendix B.4.2. 

### **3.3. Learning DAJI-Flow: Streaming Joint-Intent Generation** 

Once DAJI-Act has learned an executable intent space, languageconditioned humanoid generation becomes the problem of streaming joint-intent latents. **DAJI-Flow** is a language-conditioned flowmatching DiT that predicts future intent chunks conditioned on the language instruction and recent executed intent history. A frozen language encoder maps ℒ to text features 𝐇<sup>text</sup> , and a temporal encoder maps the recent executed latent history to 𝐇<sup>obs</sup> . The conditioning sequence is 


DAJI-Flow generates the next clean latent chunk 𝐗0 ∈ℝ<sup>𝐻×𝑑𝑧</sup> , where 𝐻 is the chunk length. Given noise 𝝐 and flow time 𝑠∈[0, 1], 

### **3.4. Training and Deployment** 

DAJI is trained in three stages. Stage 1 trains the future-aware privileged teacher with PPO. Stage 2 trains **DAJI-Act** through studentdriven in-loop distillation, learning both the stochastic joint-intent bottleneck and the diffusion action head. After convergence, the training-only intent encoder is applied offline to reference motions to construct text–intent trajectory pairs. Stage 3 trains **DAJI-Flow** with flow matching and scheduled self-conditioning, with the language encoder frozen. 

At deployment, each newly received active instruction is encoded once and reused until the next instruction switch. For each chunk, **DAJI-Flow** predicts future joint-intent latents from the active text embedding and recent intent history. Each chunk contains 15 latent frames, corresponding to 0.3 s at the 50 Hz control frequency. Each 𝐳𝑡 is 

4–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

**Table 1. Execution interface validation.** The deployable **DAJI-Act** policy decodes joint intents with live proprioception and runs in real time on CPU. 

|**Variant**|**Succ.** (%)↑|**Fall**(%)↓|**L-MPJPE**↓|**Skate**↓|**Lat. (ms)**↓|
|---|---|---|---|---|---|
|Privileged teacher|**92.5**|**7.5**|**29.9**|**131.3**|**1.73**(GPU)|
|DAJI-Act (MLP, 64D)|**80.8**|**19.2**|**39.7**|**175.8**|4.71 (CPU)|
|DAJI-Act (MLP, 32D)|76.3|23.7|40.7|189.5|4.73 (CPU)|
|DAJI-Act (MLP, 16D)|49.5|50.5|58.3|223.3|**4.28**(CPU)|
|DAJI-Act (Transformer, 64D)|76.9|23.1|42.0|178.9|7.48 (CPU)|


**Table 2. Main comparison on HumanML3D.** → means closer to GT is better. The best non-GT result in each metric is bolded, and shading indicates relative rank among non-GT methods. 

|**Method**|**MM-D**↓|**R@1**↑|**R@2**↑|**R@3**↑|**FID**↓|**Div**→|**MM**↑|**Succ. (%)**↑|
|---|---|---|---|---|---|---|---|---|
|GT|0.968|0.720|0.878|0.919|0.000|1.372|–|100.00|
|GT (Sim)|1.002|0.687|0.847|0.900|0.059|1.320|–|94.50|
|LangWBC|1.462|0.205|0.328|0.412|0.510|1.045|0.365|70.50|
|ECHO|1.318|0.288|0.432|0.528|0.378|1.148|0.462|82.00|
|FRoM-W1|1.392|0.245|0.380|0.471|0.445|1.095|0.412|76.00|
|RoboGhost|1.275|0.325|0.468|0.562|0.335|1.178|0.501|85.00|
|MotionStreamer|1.225|0.378|0.542|0.645|0.278|1.205|0.585|87.50|
|TextOp|1.175|0.425|0.595|0.698|0.225|1.228|0.628|90.00|
|**DAJI**|**1.093**|**0.549**|**0.711**|**0.796**|**0.147**|**1.291**|**0.847**|**94.42**|


**Table 3. Long-term generation evaluation on BABEL.** Subsequence metrics evaluate segment-level text-motion quality, while transition metrics evaluate continuity around text-switching boundaries. 

|**Method**||**Subse**|**quence**|||**Transi**|**tion**||
|---|---|---|---|---|---|---|---|---|
||R@3↑|FID↓|Div→|MM-D↓|FID↓|Div→|PJ↓|MJ↓|
|GT|0.654|0.000|1.299|1.299|0.000|1.182|0.043|0.015|
|GT (Sim)|0.625|0.059|1.287|1.157|0.054|1.153|0.090|0.022|
|TextOp|0.287|0.538|0.985|1.514|0.594|0.784|0.231|0.156|
|**DAJI**|**0.443**|**0.152**|**1.219**|**1.237**|**0.236**|**1.033**|**0.115**|**0.054**|


decoded in real time by **DAJI-Act** conditioned on live proprioception. The privileged teacher and the training-only intent encoder are not used at deployment. DAJI-Flow and DAJI-Act run asynchronously: DAJI-Flow produces low-frequency intent chunks, while DAJI-Act provides low-latency physical execution of each generated latent. 

to decode DAJI’s joint-intent latents. We report standard text-motion metrics [47], execution success, and transition-continuity metrics. Detailed dataset construction, baseline execution, metric definitions, and default hyperparameters are provided in Appendix A. 

## **4. EXPERIMENTS** 

We evaluate DAJI as a language-conditioned streaming humanoid control framework. The central question behind our experiments is whether the learned joint-intent latent behaves as an anticipatory command rather than a state-like motion code: it should be executable by the controller, predictive of upcoming motion, and stable when generated autoregressively. We therefore evaluate DAJI along three complementary axes: whether the latent is a viable execution interface, whether its anticipatory temporal structure matters, and whether the resulting generation pipeline improves both single-instruction and streaming language-conditioned humanoid control. Since every generated command must be consumed by a closed-loop humanoid controller, we evaluate DAJI beyond offline language-to-motion metrics and treat rollout executability as a first-class outcome. 

### **4.1. Experimental Setup** 

We evaluate DAJI on two complementary settings: a HumanML3Dstyle robot motion benchmark for single-instruction languageconditioned generation, and BABEL [8] for long-horizon streaming generation with instruction switches. We compare with recent language-conditioned humanoid motion generation and control methods whenever their outputs can be evaluated under the same robotmotion pipeline. Reference-based baselines and GT (Sim) are executed using the same privileged teacher tracker, while DAJI-Act is used only 

### **4.2. Qualitative Results** 

Before quantitative comparisons, we visualize representative deployment results. Figure 4 shows physical hardware deployment, and Figure 3 presents simulation rollouts where the low-level controller decodes generated joint-intent latents into continuous whole-body humanoid motions. 

### **4.3. Execution Interface Validation** 

We first verify that the learned joint-intent latent is a deployable execution interface rather than an offline representation. The goal here is not to benchmark a universal tracking policy, but to test whether commands expressed in the joint-intent space can be decoded by the deployable controller into stable humanoid behavior under closedloop dynamics. 

Table 1 establishes that DAJI’s joint-intent latent is not merely useful for generation; it is a viable control interface. The 64D MLP student offers the best practical tradeoff, preserving strong local articulation accuracy and closed-loop stability while remaining real-time on CPU. Reducing the bottleneck to 16D sharply degrades success rate and physical quality, showing that this is not a trivial result of any compact latent. Replacing the 64D MLP with a Transformer also increases latency without improving execution quality, which supports the default controller design used throughout the paper. 

5–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 


**Figure 4. Qualitative deployment results on physical humanoid hardware.** DAJI produces executable motions under both streaming instruction switches and single-instruction generation. Any object-related phrases shown in qualitative prompts are interpreted only as body-motion descriptions; no object state or manipulation outcome is modeled or evaluated. 

### **4.4. Main Benchmarks** 

#### **_4.4.1. HumanML3D-Style Robot Motion Generation_** 

We first evaluate DAJI on the HumanML3D-style robot motion test set, where each sample is paired with a single language instruction. This benchmark measures whether the generator can produce semantically aligned robot motions while preserving executability after export to the humanoid control stack. 

Table 2 shows that DAJI improves both language-motion alignment and rollout executability. For a conservative comparison, referencebased baselines are executed with the same privileged teacher tracker used for GT (Sim), while DAJI-Act only decodes DAJI’s joint-intent latents. Thus, the gains mainly reflect the generation–control interface rather than a stronger tracking backend. By generating controller- 

distilled intents instead of external kinematic references, DAJI produces commands that remain semantically aligned and decodable under feedback control. The gap between GT and GT (Sim) further shows why rollout success should be treated as a first-class metric. 

#### **_4.4.2. Streaming Instruction Following on BABEL_** 

We next evaluate DAJI on BABEL, which exposes a different failure mode from single-instruction generation. Here the model must continue from its own latent history while adapting to new instructions at segment boundaries. This directly tests whether the interface remains coherent under long-horizon streaming rollout rather than merely producing one isolated clip. 

Table 3 shows that the advantage of DAJI becomes even clearer in streaming rollout. Compared with the closest compatible streaming 

6–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

**Table 4. Representation-level latent temporal design ablation.** Future-aware latents improve predictiveness, coherence, and long-horizon execution. 

|**Variant**|**Probe@40**↑|**Corr.@40**↑|**Succ.@20s (%)**↑|**Succ.@60s (%)**↑|
|---|---|---|---|---|
|No-Future|0.047|0.180|13|10|
|Short-Future|0.315|0.600|84|70|
|Full DAJI|**0.393**|**0.736**|**94**|**87**|


**Table 5. Generation-level ablation of joint-intent latent temporal design on HumanML3D.** All variants use the same DAJI-Flow configuration and differ only in the temporal offsets used to construct the DAJI-Act-distilled 64D joint-intent latent. → means closer to GT is better. 

|**Method**|**MM-D**↓|**R@1**↑|**R@2**↑|**R@3**↑|**FID**↓|**Div**→|**MM**↑|**Succ. (%)**↑|
|---|---|---|---|---|---|---|---|---|
|No-Future Latent|1.113|0.502|0.673|0.767|0.209|1.279|0.823|93.56|
|Short-Future Latent|1.139|0.466|0.626|0.722|0.180|1.250|**0.974**|93.65|
|Full DAJI|**1.093**|**0.549**|**0.711**|**0.796**|**0.147**|1.291|0.847|**94.42**|
|Dense-Future Latent|1.110|0.506|0.677|0.773|0.159|**1.294**|0.697|93.88|
|Long-Future Latent|1.148|0.436|0.595|0.697|0.194|1.262|0.848|93.61|


**Table 6. Ablation study of generator-side design on HumanML3D.** 

**Table 7. Temporal offset sets for joint-intent latent construction.** 

|**Method**|**R@3**↑|**FID**↓|**Succ.** (%)↑|**Variant**|**Temporal offsets**|
|---|---|---|---|---|---|
|Full DAJI|**0.796**|**0.147**|**94.42**|No-Future|{0, −1, −2, −4, −8, −12, −16}|
|w/o Self-Cond.|0.667|0.153|93.29|Short-Future|{0, +1, +2, −1, −2, −4, −8, −12, −16}|
|||||Full DAJI|{0, +1, +2, +3, +4, −1, −2, −4, −8, −12, −16}|
|||||Dense-Future|{0, +1, +2, +3, +4, +5, +6, +7, +8, −1, −2, −4, −8, −12, −16}|
|li DAJI i|bth b|lit|d bd|Long-Future|{0, +1, +2, +3, +4, +8, +12, +16, +20, −1, −2, −4, −8}|


baseline, DAJI improves both subsequence quality and boundary continuity. This is exactly the regime where anticipatory intent matters: instruction switches require the policy to prepare support transfer, root momentum, and posture adaptation before the visible transition is complete. Generating in the joint-intent space therefore improves not only semantic alignment but also the smoothness and stability of instruction-conditioned transitions. 

Table 4 shows that future-aware latent construction is critical at the representation level. Removing future offsets makes the latent largely reactive, reducing Probe@40 from 0.393 to 0.047 and 60s success from 87% to 10%. Short-Future remains functional but is less coherent and less stable over long horizons. Diagnostic definitions for Probe@40 and Corr.@40 are provided in Appendix C.1. 

Table 5 shows that the same conclusion carries over to languageconditioned generation. A state-like latent that only summarizes current and past references provides weaker information about upcoming support transfer and body transitions. Conversely, an overly dense or distant future target may contain more motion information but can become harder to infer from text and recent latent history. Dense-Future matches Full DAJI in FID but does not improve semantic alignment or success rate, while Long-Future degrades most generation metrics. The lower fixed-horizon success of No-Future here does not contradict its short-clip HumanML3D export success: the fixed-horizon diagnostic measures extended 20 s/60 s closed-loop continuation, whereas the HumanML3D metric evaluates bounded single-instruction clips after export. Taken together, these two tables support the default short-horizon future design as the best tradeoff between anticipatory structure, generative predictability, and closedloop executability. 

### **4.5. Ablations and Design Analysis** 

We next analyze which design choices make the joint-intent latent an anticipatory command rather than a state-like motion code, and which components stabilize autoregressive generation. 

**Generator training design.** We first evaluate the role of scheduled self-conditioning. The DAJI-Flow w/o Self-Conditioning variant removes predicted-history feedback during training and conditions the generator only on ground-truth latent history, corresponding to standard teacher-forced training. Full DAJI instead feeds generated latent chunks back into the history during training, gradually exposing the model to its own induced rollout distribution. 

Table 6 shows that scheduled self-conditioning improves language alignment under autoregressive rollout, as reflected by the higher R@3. The gain in success rate is modest but consistent, while FID remains comparable. This supports the role of self-conditioning in reducing the train-test mismatch once the model must condition on its own previously generated latent histories. 

**Text encoder ablation.** We further study the effect of the frozen text encoder used by DAJI-Flow. All variants use the same DAJI-Act intent space, DAJI-Flow architecture, training data, chunk size, selfconditioning schedule, and evaluation protocol; only the text encoder is changed. 

**Joint-intent latent temporal design.** We next study whether the temporal construction of the joint-intent latent determines whether it behaves as an anticipatory command rather than a reactive state code. This ablation changes only the latent target: for each design, we retrain the DAJI-Act-distilled intent encoder, extract text–latent trajectories, and train the same DAJI-Flow configuration. All variants share the same latent dimensionality, generator, chunk size, self-conditioning schedule, latent-history length, optimizer, data, and metrics. The compared designs differ only in which past and future reference frames are compressed into the latent. 

Table 8 shows that the choice of text encoder affects languageconditioned intent generation. Qwen3-VL-4B achieves the best semantic alignment metrics, including MM-D and R-precision, as well as the lowest FID and the highest rollout success. Qwen2.5-VL-3B gives slightly higher MultiModality, but Qwen3-VL-4B provides the strongest overall tradeoff. Since the language instruction is encoded only once when it is received or switched, the frozen text encoder is not invoked at every control step. The resulting text features are cached and reused during subsequent latent-chunk generation, so the use of a larger text encoder does not affect the high-frequency DAJI-Act control loop. Hyperparameter sensitivity to self-conditioning depth and latent-history length is reported in Appendix C.2. 

Table 7 summarizes the temporal offset sets used in this ablation. Offset 0 denotes the current frame, positive offsets denote future reference frames, and negative offsets denote past reference frames. 

7–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

**Table 8. Text encoder ablation on the HumanML3D-style benchmark.** All variants use the same DAJI-Flow configuration and differ only in the frozen text encoder. 

|**Text Encoder**|**MM-D**↓|**R@1**↑|**R@2**↑|**R@3**↑|**FID**↓|**MM**↑|**Succ. (%)**↑|
|---|---|---|---|---|---|---|---|
|CLIP|1.136|0.470|0.637|0.732|0.258|0.670|93.79|
|T5|1.109|0.511|0.701|0.790|0.185|0.756|93.61|
|Qwen2.5-VL-3B|1.105|0.513|0.683|0.778|0.159|**0.890**|94.11|
|Qwen3-VL-4B|**1.093**|**0.549**|**0.711**|**0.796**|**0.147**|0.847|**94.42**|


## **5. CONCLUSION** 

We presented DAJI, a hierarchical framework for streaming languageconditioned humanoid control. At deployment, DAJI replaces motion references with a dynamics-aligned joint-intent representation at the interface between semantic generation and closed-loop control. This representation is executable by a closed-loop controller and anticipatory of upcoming motion transitions. By learning it through future-aware privileged control and student-driven in-loop distillation, then generating it with language-conditioned flow matching, DAJI improves language-motion alignment, temporal coherence, and closed-loop executability on single-instruction and streaming benchmarks. These results suggest that the generation-control interface should not only specify the desired motion, but also help the robot prepare for what comes next. 

8–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

## **REFERENCES** 

- [1] J. Massion, “Movement, posture and equilibrium: Interaction and coordination”, _Progress in neurobiology_ , vol. 38, no. 1, pp. 35–56, 1992. 

- [2] S. Bouisset and M.-C. Do, “Posture, dynamic stability, and voluntary movement”, _Neurophysiologie Clinique/Clinical Neurophysiology_ , vol. 38, no. 6, pp. 345–362, 2008. 

- [3] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control”, in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , IEEE, 2012, pp. 5026– 5033. doi: 10.1109/IROS.2012.6386109 

- [4] M. Plappert, C. Mandery, and T. Asfour, “The kit motionlanguage dataset”, _Big Data_ , vol. 4, no. 4, pp. 236–252, 2016. 

- [5] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms”, _CoRR_ , vol. abs/1707.06347, 2017. arXiv: 1707.06347. [Online]. Available: http://arxiv.org/abs/1707.06347 

- [6] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physicsbased character skills”, _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [7] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models”, in _Advances in Neural Information Processing Systems_ , vol. 33, Curran Associates, Inc., 2020, pp. 6840–6851. [Online]. Available: https://proceedings.neurips.cc/paper/2020/file/ 4c5bcfec8584af0d967f1ab10179ca4b-Paper.pdf 

- [8] A. R. Punnakkal, A. Chandrasekaran, N. Athanasiou, A. QuirosRamirez, and M. J. Black, “Babel: Bodies, action and behavior with english labels”, in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , Jun. 2021, pp. 722–731. 

- [9] J. Song, C. Meng, and S. Ermon, “Denoising diffusion implicit models”, in _9th International Conference on Learning Representations, ICLR 2021_ , OpenReview.net, 2021. [Online]. Available: https://openreview.net/forum?id=St1giarCHLP 

- [10] M. Ahn et al., “Do as i can, not as i say: Grounding language in robotic affordances”, _arXiv preprint arXiv:2204.01691_ , 2022. 

- [11] C. Guo et al., “Generating diverse and natural 3d human motions from text”, in _CVPR_ , 2022. 

- [12] G. Tevet, S. Raab, B. Gordon, Y. Shafir, D. Cohen-Or, and A. H. Bermano, “Human motion diffusion model”, _arXiv preprint arXiv:2209.14916_ , 2022. 

- [13] C. Guo, Y. Mu, M. G. Javed, S. Wang, and L. Cheng, “Momask: Generative masked modeling of 3d human motions”, _arXiv preprint arXiv:2312.00063_ , 2023. 

- [14] V. T. Hu et al., “Motion flow matching for human motion synthesis and editing”, _arXiv preprint arXiv:2312.08895_ , 2023. 

- [15] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “Voxposer: Composable 3d value maps for robotic manipulation with language models”, _arXiv preprint arXiv:2307.05973_ , 2023. 

- [16] J. Liang et al., “Code as policies: Language model programs for embodied control”, in _2023 IEEE International conference on robotics and automation (ICRA)_ , IEEE, 2023, pp. 9493–9500. 

- [17] Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling”, in _The Eleventh International Conference on Learning Representations, ICLR 2023_ , OpenReview.net, 2023. [Online]. Available: https://openreview. net/forum?id=PqvMRDCJT9t 

- [18] Z. Luo, J. Cao, K. Kitani, W. Xu, et al., “Perpetual humanoid control for real-time simulated avatars”, in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2023, pp. 10 895–10 904. 

- [19] W. Peebles and S. Xie, “Scalable diffusion models with transformers”, in _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , Oct. 2023, pp. 4195–4205. 

- [20] C. Tessler, Y. Kasten, Y. Guo, S. Mannor, G. Chechik, and X. B. Peng, “Calm: Conditional adversarial latent models for directable virtual characters”, in _ACM SIGGRAPH 2023 conference proceedings_ , 2023, pp. 1–9. 

- [21] J. Zhang et al., “T2m-gpt: Generating human motion from textual descriptions with discrete representations”, in _CVPR_ , 2023. 

- [22] G. Barquero, S. Escalera, and C. Palmero, “Seamless human motion composition with blended positional encodings”, in _CVPR_ , 2024. 

- [23] W. chen et al., “Sato: Stable text-to-motion framework”, in _Proceedings of the 32nd ACM International Conference on Multimedia_ , ser. MM ’24, Melbourne VIC, Australia: Association for Computing Machinery, 2024, pp. 6989–6997, isbn: 9798400706868. doi: 10.1145/3664647.3681034 [Online]. Available: https://doi.org/10.1145/3664647.3681034 

- [24] Z. Jiang, Y. Xie, J. Li, Y. Yuan, Y. Zhu, and Y. Zhu, “Harmon: Whole-body motion generation of humanoid robots from language descriptions”, in _Conference on Robot Learning_ , 2024. arXiv: 2410.12773 `[cs.RO]` . 

- [25] S. Bai, Y. Cai, R. Chen, K. Chen, et al., “Qwen3-vl technical report”, _arXiv preprint arXiv:2511.21631_ , 2025. [Online]. Available: https://arxiv.org/abs/2511.21631 

- [26] W. Chen et al., “Ant: Adaptive neural temporal-aware textto-motion model”, in _Proceedings of the 33rd ACM International Conference on Multimedia_ , ser. MM ’25, ACM, Oct. 2025, pp. 9852–9861. doi: 10.1145/3746027.3755168 [Online]. Available: http://dx.doi.org/10.1145/3746027.3755168 

- [27] W. Chen et al., _Free-t2m: Robust text-to-motion generation for humanoid robots via frequency-domain_ , 2025. arXiv: 2501.18232 `[cs.CV]` . [Online]. Available: https://arxiv.org/abs/2501.18232 

- [28] W. Chen et al., _Polaris: Projection-orthogonal least squares for robust and adaptive inversion in diffusion models_ , 2025. arXiv: 2512.00369 `[cs.CV]` . [Online]. Available: https://arxiv.org/abs/ 2512.00369 

- [29] H. Jia et al., _Luma: Low-dimension unified motion alignment with dual-path anchoring for text-to-motion diffusion model_ , 2025. arXiv: 2509.25304 `[cs.CV]` . [Online]. Available: https: //arxiv.org/abs/2509.25304 

- [30] H. Jia et al., _Physics-informed representation alignment for sparse radio-map reconstruction_ , 2025. arXiv: 2501.19160 `[cs.CV]` . [Online]. Available: https://arxiv.org/abs/2501.19160 

- [31] H. Jia et al., “Physics-informed representation alignment for sparse radio-map reconstruction”, in _Proceedings of the 33rd ACM International Conference on Multimedia_ , ser. MM ’25, Dublin, Ireland: Association for Computing Machinery, 2025, pp. 12 352–12 360, isbn: 9798400720352. doi: 10.1145/3746027. 3758161 [Online]. Available: https://doi.org/10.1145/3746027. 3758161 

- [32] N. Jiang et al., _UniAct: Unified motion generation and action streaming for humanoid robots_ , 2025. arXiv: 2512.24321 `[cs.CV]` . 

- [33] Z. Li et al., _From language to locomotion: Retargeting-free humanoid control via motion latent guidance_ , 2025. arXiv: 2510. 14952 `[cs.RO]` . 

9–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

- [34] Q. Lu, Y. Feng, B. Shi, M. Piseno, Z. Bao, and C. K. Liu, _Gentlehumanoid: Learning upper-body compliance for contact-rich human and object interaction_ , 2025. arXiv: 2511.04679 `[cs.RO]` . [Online]. Available: https://arxiv.org/abs/2511.04679 

- [35] M. Ning et al., _Dctdiff: Intriguing properties of image generative modeling in the dct space_ , 2025. arXiv: 2412 . 15032 `[cs.CV]` . [Online]. Available: https://arxiv.org/abs/2412.15032 

- [36] Y. Shao et al., _LangWBC: Language-directed humanoid wholebody control via end-to-end learning_ , 2025. arXiv: 2504.21738 `[cs.RO]` . 

- [37] B. Tian, W. Chen, Z. Li, S. Lai, J. Wu, and Y. Yue, “Text2weight: Bridging natural language and neural network weight spaces”, in _Proceedings of the 33rd ACM International Conference on Multimedia_ , ser. MM ’25, Dublin, Ireland: Association for Computing Machinery, 2025, pp. 10 152–10 160, isbn: 9798400720352. doi: 10.1145/3746027.3755441 [Online]. Available: https://doi. org/10.1145/3746027.3755441 

- [38] Y. Wang, H. Jiang, S. Yao, Z. Ding, and Z. Lu, _SENTINEL: A fully end-to-end language-action model for humanoid whole body control_ , 2025. arXiv: 2511.19236 `[cs.RO]` . 

- [39] L. Xiao et al., “MotionStreamer: Streaming motion generation via diffusion-based autoregressive model in causal latent space”, in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2025. arXiv: 2503.15451 `[cs.CV]` . 

- [40] H. Jia et al., _ECHO: Edge-cloud humanoid orchestration for language-to-motion control_ , 2026. arXiv: 2603.16188 `[cs.CV]` . 

- [41] H. Li, W. Chen, S. Liang, L. Wang, K. Yuan, and Y. Yue, 𝑍<sup>2</sup> _- sampling: Zero-cost zigzag trajectories for semantic alignment in diffusion models_ , 2026. arXiv: 2604.23536 `[cs.CV]` . [Online]. Available: https://arxiv.org/abs/2604.23536 

- [42] H. Li, W. Chen, L. Wang, S. Liang, H. Jia, and Y. Yue, _Oracle noise: Faster semantic spherical alignment for interpretable latent optimization_ , 2026. arXiv: 2604.23540 `[cs.CV]` . [Online]. Available: https://arxiv.org/abs/2604.23540 

- [43] H. Li et al., _Delta score matters! spatial adaptive multi guidance in diffusion models_ , 2026. arXiv: 2604.26503 `[cs.CV]` . [Online]. Available: https://arxiv.org/abs/2604.26503 

- [44] P. Li et al., _FRoM-W1: Towards general humanoid whole-body control with language instructions_ , 2026. arXiv: 2601 . 12799 `[cs.RO]` . 

- [45] W. Xie et al., _TextOp: Real-time interactive text-driven humanoid robot motion generation and control_ , 2026. arXiv: 2602.07439 `[cs.RO]` . 

- [46] X. Yuan et al., _RoboForge: Physically optimized text-guided whole-body locomotion for humanoids_ , 2026. arXiv: 2603.17927 `[cs.RO]` . 

- [47] W. Chen, H. Jia, K. Yu, S. Lai, L. Wang, and Y. Yue, “Towards better evaluation metrics for text-to-motion generation”, in _The Second International Workshop on Transformative Insights in Multifaceted Evaluation at The Web Conference 2026_ . 

10–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

## **A. EVALUATION PROTOCOL AND EXPERIMENTAL SETUP DETAILS** 

This section first summarizes the datasets, baselines, metrics, and default configuration used throughout the paper, then gives the evaluator construction and the detailed HumanML3D-style and BABEL evaluation protocols. 

### **A.1. Datasets, Baselines, and Metrics** 

We evaluate DAJI on two complementary settings. The HumanML3D-style robot motion benchmark measures single-instruction languageconditioned generation using language annotations paired with robot motion trajectories. BABEL [8] evaluates long-horizon streaming generation with instruction switches. We use frame-level action annotations to construct text streams, generate each labeled segment for its original duration, and append the generated segment to the latent history before generating the next one. This enables evaluation of both segment-level semantic alignment and transition quality around instruction boundaries. 

We compare with recent language-conditioned humanoid motion generation and control methods, including LangWBC, ECHO, TextOp, FRoM-W1, RoboGhost and MotionStreamer, whenever their outputs can be evaluated under the same robot-motion pipeline. Methods that output human motions or kinematic references are converted into the common robot-motion representation and executed with the same privileged teacher tracker used for GT (Sim). DAJI-Act is used only to decode DAJI’s joint-intent latents, not external kinematic references. For policy-based methods, we evaluate executed robot trajectories when available. TextOp is the closest compatible streaming reference-based baseline on BABEL. This protocol gives reference-based baselines a strong tracking backend and is therefore conservative with respect to DAJI’s execution advantage, but the resulting success rates should still be interpreted as end-to-end interface validity rather than as a pure low-level controller comparison. 

We report standard text-motion metrics, including MM-D, R-precision at top 1/2/3, FID, Diversity, and MultiModality. For closed-loop execution, we report success rate, fall rate, local-frame MPJPE, foot skating, and latency. On HumanML3D, we additionally report rollout success after exporting generated motions to the robot-motion execution pipeline. On BABEL, we report subsequence-level generation metrics and transition-level continuity metrics, where transition FID and Diversity are computed on boundary-centered clips and smoothness is measured by peak jerk (PJ) and mean jerk (MJ). For anticipatory analysis, we further use future-prediction probes, latent temporal correlation, and long-horizon rollout success. 

Unless otherwise specified, DAJI uses eight self-conditioned chunks during training and conditions on 𝐾= 8 recent joint-intent chunks during inference. Each chunk contains 15 frames. The self-conditioning depth controls how many predicted chunks are fed back during training, while 𝐾 controls the latent-history length observed by the generator. 

**Compute resources and precision.** Teacher tracker and DAJI-Act training are conducted on 8 NVIDIA A100 GPUs, while DAJI-Flow generator training is conducted on 4 NVIDIA A100 GPUs. Unless otherwise specified, the frozen VLM runs in bfloat16 and the DiT generator head is trained in fp32. Reported controller latency is measured separately on CPU or GPU, as indicated in the corresponding tables. 

### **A.2. Evaluator** 

We use a text-motion evaluator to compute MM-D, R-precision, FID, Diversity, and MultiModality. The evaluator contains a text encoder and a motion encoder, which map language descriptions and robot motion clips into a shared embedding space. In our implementation, MM-D corresponds to the matching score computed by the evaluator, i.e., the average Euclidean distance between paired text and motion embeddings. R-precision is computed by retrieving the matched motion from a batch of candidate motions using the text embedding as query. FID, Diversity, and MultiModality are computed in the evaluator motion-feature space. 

The evaluator is trained on paired text-motion data using a contrastive objective. Matched text-motion pairs are pulled closer in the embedding space, while mismatched pairs in the same batch are pushed apart. For HumanML3D-style evaluation, the evaluator is trained on paired text descriptions and robot motion clips from the HumanML3D-style robot motion dataset. For BABEL evaluation, we construct text-motion pairs from frame-level action annotations, where each annotated segment provides a text label and a corresponding robot motion segment. The evaluator is frozen after training and is used only for evaluation. 

### **A.3. HumanML3D-style Evaluation** 

The HumanML3D-style benchmark contains language annotations paired with robot motion trajectories converted into our robot-motion representation. For each test prompt, the generator autoregressively predicts a sequence of 64-dimensional joint-intent latent chunks, which are then exported to robot motion for evaluation. 

We filter out motions shorter than 100 frames before evaluation. Motions are padded or truncated to a maximum length of 490 frames. We report two reference rows in the main table. GT denotes the original dataset motions. GT (Sim) denotes the trajectories obtained after passing the corresponding dataset motions through the same robot-motion export and simulation validation pipeline used for generated motions. The gap between GT and GT (Sim) reflects the degradation introduced by robot-motion export, tracking, and simulation validation, rather than errors from the text-conditioned generator. 

For generated methods, rollout success is computed over all generated samples. Text-motion metrics are computed only on successfully exported motions, while success rate is reported separately. This avoids hiding invalid generations inside text-motion metrics, so these metrics should be interpreted jointly with success rate rather than in isolation. 

### **A.4. Robot-Motion Execution and Validation** 

GT (Sim) is obtained by executing the dataset motion references in simulation with the privileged teacher tracker. For reference-based baselines that follow a generator–reference–tracker pipeline, we first convert their generated references into the common robot-motion representation and then execute them with the same teacher tracker. DAJI-Act is used only to decode DAJI’s joint-intent latents and is not used to execute external kinematic references. This keeps the execution backend consistent for GT (Sim) and reference-based baselines, so rollout success reflects the quality of the generated references under the same strong tracking policy. 

11–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

### **A.5. BABEL Long-Term Evaluation** 

BABEL provides frame-level action annotations over long motion sequences. We use these annotations to construct streaming text-conditioned rollouts. Given a BABEL sequence with annotated segments, DAJI generates the corresponding motion segments sequentially. Each segment is conditioned on its text label and generated for the same duration as the annotation. The generated segment is appended to the latent history before generating the next segment, so later segments are conditioned on previously generated latents rather than generated independently and stitched together afterwards. 

We evaluate each BABEL rollout from two perspectives. Subsequence metrics are computed on individual text-labeled motion segments and measure whether each generated segment matches its corresponding instruction. Transition metrics are computed on short clips centered around adjacent text-switching boundaries and measure whether the generated motion remains smooth and natural when the instruction changes. For a boundary at frame 𝑏, we extract a transition clip from 𝑏−15 to 𝑏+ 15, containing 15 frames before and 15 frames after the boundary. 

### **A.6. Transition Metrics** 

Transition FID and Diversity are computed using the evaluator motion encoder, but only on boundary-centered transition clips. Transition FID measures whether generated transition clips follow the distribution of real transition clips. Transition Diversity measures the spread of generated transition clips in motion-feature space. 

For transition smoothness, jerk is computed on the joint-position channels of the raw 38D robot representation, rather than on the full feature vector. Given a joint-position sequence 𝐱𝑡, we compute 


Peak Jerk (PJ) is the maximum jerk magnitude within the transition clip: 


Mean Jerk (MJ) measures the average jerk magnitude over the transition clip: 


PJ captures the largest abrupt motion change around the text-switching boundary, while MJ measures the overall smoothness of the transition. 

### **A.7. Rollout Success** 

For HumanML3D-style evaluation, a generated motion is considered successful if it can be exported and validated in the robot-motion pipeline without triggering termination conditions. We use the same termination criteria as in controller evaluation, including body-height termination and gravity-direction termination. Success rate is computed as 


Failed rollouts are counted in the denominator. Text-motion metrics are computed on successfully exported motions only, and success rate is reported separately to make invalid generations explicit. 

## **B. IMPLEMENTATION DETAILS** 

### **B.1. Key Dimensions and Training Constants** 

Table 9 summarizes the key dimensions and temporal constants used by DAJI. Symbols are introduced in the main text when they first appear. 

12–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

**Table 9.** Key dimensions and generation constants. 

|**Quantity**|**Value**|
|---|---|
|Joint-intent latent dim𝑑𝑧|64|
|DAJI-Act control context dim𝑑𝑐|192|
|Full non-privileged training/distillation observation dim𝑑train|1590|
|Deployment proprioceptive/state observation dim𝑑prop|812|
|Training-only reference/motion observation dim𝑑ref|778|
|Raw privileged observation dim𝑑priv|4558|
|Critic-only privileged dim𝑑priv_critic|3|
|Text hidden dim𝑑vlm|2560|
|Action dim𝑑act|29|
|Control frequency|50 Hz|
|Simulation timestep∆𝑡|0.02 s|
|Latent chunk length𝐻|15 frames (0.3 s)|
|Latent-history chunks𝐾|8|
|Max latent-history frames𝑇obs|120 (𝐾× 𝐻)|
|Self-conditioning depth𝐾sc|8 chunks|
|Default free-generation chunks𝑁|20|
|Euler integration steps𝑀|4|
|DDPM diffusion steps𝑇|50|


### **B.2. Architecture and Training Overview** 

#### **_B.2.1. Controller_** 

**Teacher.** The privileged encoder is an MLP [512] →256. The actor concatenates the non-privileged training observation with the privileged feature and passes through MLP [1024, 512, 512], outputting the mean of an independent Gaussian with learned diagonal covariance over 𝑑act = 29 joint-position actions. The critic uses the same MLP architecture. 

**DAJI-Act.** 𝐸prop is a 2-layer MLP [128, 128] with ELU activations, mapping the 812-dimensional deployment proprioceptive/state observation to a 128-dimensional feature. 𝐸ref is a 2-layer MLP [128, 128] with ELU activations, mapping the 778-dimensional training-only reference/motion observation to intent-distribution parameters 𝝁, log 𝝈<sup>2</sup> ∈ℝ<sup>64</sup> . The diffusion denoiser 𝒟𝜙 follows a compact DDPM-style parameterization with deterministic DDIM sampling at inference [7, 9]. It is implemented as a 4-layer MLP (width 256) with adaptive layer normalization (AdaLN): each residual block applies LayerNorm modulated by the time-condition embedding, followed by Linear(256)→SiLU→Linear(256) with a learned gate. The condition 𝐜𝑡 ∈ℝ<sup>192</sup> is projected to 256d and summed with the time embedding. Xavier uniform initialization; final AdaLN modulation and output projection are zero-initialized. At deployment, DAJI-Act conditions only on 𝐸prop(𝐨𝑡<sup>prop</sup> ) and the generated latent 𝐳𝑡; the training-only reference observation is not used. 

#### **_B.2.2. DAJI-Flow_** 

**VLM.** Qwen3-VL-4B-Instruct [25], frozen. 𝑑vlm = 2560. Runs in bfloat16. 

**Observation encoder** 𝐸obs **.** MLP: 𝑑𝑧 →768 →𝑑vlm with GELU activation, plus learned positional embeddings (max 120 positions), followed by LayerNorm. Truncates input to most recent 𝑇obs frames. 

**Flow-matching head.** DAJI-Flow predicts joint-intent latent chunks rather than low-level joint actions. We use a DiT-B flow-matching head [17, 19] with 16 transformer blocks, 12 attention heads, token width 768, output dimension 1024, cross-attention to 𝑑vlm conditioning tokens, AdaLayerNorm timestep modulation, and dropout 0.2. The noisy latent trajectory is embedded with sinusoidal flow-timestep encoding and learned latent-position embeddings. We prepend 32 learnable query tokens for internal aggregation, but only the 𝐻= 15 latent-frame tokens are decoded as the output chunk by an MLP 1024 →1024 →𝑑𝑧. 

#### **_B.2.3. Training Stages_** 

Table 10 summarizes which modules are trained or frozen in each of the three stages. 

**Table 10.** Training stage breakdown. ✓ = trained; × = frozen; − = not used. 

|**Module**|**1. Teacher**|**2. Distill**|**3. Generator**|
|---|---|---|---|
|Teacher (PPO actor + critic)|✓|×|−|
|Intent encoder + DAJI-Act diffusion head|−|✓|−|
|Qwen VLM|−|−|×|
|LatentObsEncoder + DiT head|−|−|✓|
|Data source|Simulation|Simulation|Latent dataset|
|Supervision|PPO reward|Teacher actions|Velocity field|


13–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

### **B.3. Observation, Privileged Inputs, and Rewards** 

#### **_B.3.1. Observation and Privileged Inputs_** 

Table 11 reports the deployment proprioceptive/state observation used by DAJI-Act at test time. During teacher/distillation training, this observation is paired with the training-only reference/motion block in Table 12 to form the 1590-dimensional non-privileged training observation. 

**Table 11.** Deployment proprioceptive/state observation used by DAJI-Act. For compactness, the 9-frame history uses offsets {0, 1, 2, 3, 4, 8, 12, 16, 20}. 

|**Observation block**|**Temporal form**|**Dim.**|
|---|---|---|
|Root angular velocity|3D body-frame vector over 9 offsets|27|
|Projected gravity|3D body-frame vector over 9 offsets|27|
|Joint positions|29D joint vector over 9 offsets|261|
|Joint velocities|29D joint-velocity vector over 9 offsets|261|
|Previous actions|29D action vector over 8 history steps|232|
|Boot indicator|scalar flag|1|
|Compliance flag|raw, threshold-scaled, and stiffness-scaled flags|3|
|**Total**|–|**812**|


**Table 12.** Training-only reference/motion observation used by the intent encoder and privileged teacher during distillation. 

|**Observation block**|**Temporal form**|**Dim.**|
|---|---|---|
|Command/reference state|root pose-related features|96|
|Target joint positions|future reference features|638|
|Target root height|11 future steps|11|
|Target projected gravity|3axes×11 future steps|33|
|**Total**|–|**778**|


The full non-privileged observation used during teacher/distillation training has dimension 1590, combining the 812-dimensional proprioceptive/state block with the 778-dimensional reference-motion block. At deployment, DAJI-Act does not consume this full 1590-dimensional input. Instead, it conditions on the 812-dimensional proprioceptive/state observation together with the generated joint-intent latent. During training, the privileged teacher and critic additionally use simulation-only privileged inputs, which are not available at deployment. 

In our implementation, the teacher actor receives the full non-privileged training observation together with a 256-dimensional privileged feature encoded from the raw privileged observation. The critic receives the concatenation of the full non-privileged training observation, the raw privileged observation, and a critic-only error signal. The raw privileged observation has dimension 4558, and the critic-only privileged signal has dimension 3. 

The non-privileged training observation contains deployable and task-related terms, including boot indicators, command/reference observations, target root height, target joint positions, target projected gravity, root angular-velocity history, projected-gravity history, jointposition history, joint-velocity history, and previous actions. Only the proprioceptive/state subset is available to deployed DAJI-Act. 

The raw privileged observation provides simulation-only information, including future target root positions and velocities in the body frame, target-current root orientation difference, body-height signals, foot contact forces, true root linear velocity, longer proprioceptive histories, current keypoint positions and velocities, target-current keypoint differences, applied actions, and applied torques. The critic-only privileged signal contains cumulative tracking errors over root, orientation, and keypoint terms. 

These privileged inputs are used to train the privileged teacher encoder and critic, but they are not available to the deployed DAJI-Act actor. 

#### **_B.3.2. Rewards and Domain Randomization_** 

**Table 13.** Tracking reward terms. All tracking rewards use an exponential kernel exp(−‖𝑒‖∕𝜎). 

|**Reward term**|**Weight**|𝝈|
|---|---|---|
|Root position|0.5|0.3|
|Root rotation (axis-angle)|0.5|0.4|
|Root linear velocity|1.0|1.0|
|Root angular velocity|1.0|3.0|
|Keypoint position (13 bodies)|1.0|0.3|
|Keypoint velocity|1.0|1.0|
|Keypoint rotation (6D)|1.0|0.4|
|Keypoint angular velocity|1.0|3.0|
|Lower-body keypoints|0.5|0.2|
|Upper-body keypoints|0.5|0.3|
|Joint position (29 DoF)|1.0|0.5|
|Joint velocity|0.5|3.0|


14–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

**Table 14.** Regularization reward terms. 

|**Reward term**|**Weight**|
|---|---|
|Survival bonus|3.0|
|Joint velocity L2|5×10<sup>−4</sup>|
|Action rate L2|0.01|
|Feet air time (ref-aligned)|5.0|
|Feet air time (dense)|1.0|
|Joint position limits (soft)|1.0|
|Joint torque limits (soft)|0.01|
|Joint acceleration L2 (teacher only)|4×10<sup>−8</sup>|


**Table 15.** Domain randomization ranges grouped by subsystem. 

|**Randomization**|**Range**|
|---|---|
|_Contact and solver_||
|CoM perturbation (pelvis, torso)|±0.03 m|
|Ankle friction|0.3–1.2|
|Solver time constant|0.015–0.03|
|Solver damping ratio|0.5–2.0|
|_Motor and joint_||
|Motor stiffness (arms)|0.9–1.1|
|Motor stiffness (legs)|0.5–2.0|
|Motor damping (arms)|0.9–1.1|
|Motor damping (legs)|0.5–2.0|
|Motor armature|0.75–1.25|
|Joint offset noise|±0.01 rad|
|Joint pos. bias (hip, knee, ankle)|𝜎= 0.1 rad|
|_Root perturbation_||
|Root drift velocity (xy)|±0.25 m∕s|
|Root drift velocity (z)|±0.05 m∕s|
|Root height offset|±0.03 m|
|Root velocity push (xy)|±0.5 m∕s|
|Root velocity push (z)|±0.2 m∕s|
|Root velocity push (roll, pitch)|±0.52 rad|
|<br>Root velocity push (yaw)|±0.78 rad|
|Push interval|4.0–6.0 s|
|Gravity perturbation|𝜎= 0.1 m∕s<sup>2</sup>|


**Domain randomization.** 

### **B.4. Training Details** 

#### **_B.4.1. Training Hyperparameters_** 

Tables 16 and 17 summarize the hyperparameters used for controller training, distillation, and DAJI-Flow generation. Unless otherwise specified, these settings are used for all main experiments and ablations. 

#### **_B.4.2. Scheduled Self-Conditioned Training_** 

DAJI-Flow is trained with scheduled self-conditioning to reduce the train-test mismatch of autoregressive latent generation. During standard teacher-forced training, the generator observes ground-truth latent histories. During deployment, however, it must condition on its own previously generated latent chunks. Scheduled self-conditioning exposes the generator to such predicted-history inputs during training. 

Given a ground-truth latent trajectory 𝐙1∶𝑇, we sample a starting index 𝑡 and take the recent ground-truth latent history as the initial history buffer: 


The generator is then unrolled for 𝐾sc chunks. In our default setting, 𝐾sc = 8 and each chunk contains 𝐻= 15 latent frames, corresponding to an 8-chunk, 120-frame unrolled training horizon. 

For the 𝑘-th chunk, the ground-truth target is 


DAJI-Flow predicts this chunk using the current history buffer ℋ<sup>(𝑘−1)</sup> and the language condition. The first chunk is conditioned on ground-truth history. For subsequent chunks, the history buffer is augmented with previously generated latent chunks: 


15–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

**Table 16.** Controller training hyperparameters. 

|**Parameter**|**Teacher (PPO)**|**Distill**|
|---|---|---|
|Discount𝛾|0.99||
|GAE𝜆|0.95||
|PPO clip𝜖|0.2||
|Entropy coefficient|0.01 →0.0025(linear)|0|
|Learning rate|5×10<sup>−4</sup>|1×10<sup>−4</sup>|
|PPO epochs|5||
|Optimization epochs per buffer||5|
|Minibatches|8|8|
|Gradient clipping|1.0|1.0|
|Total env frames|8×10<sup>9</sup>|∼8×10<sup>9</sup>|
|KL weight𝛽||1×10<sup>−4</sup>|
|Free bits||0.0|
|Inference mode||mean (deterministic)|
|DDPM steps𝑇||50|
|Noise schedule||Cosine|
|DDIM sampling steps||2|
|DDIM𝜂||0 (deterministic)|
|Symmetry loss weight (loc)|0.2||
|Symmetry loss weight (scale)|10.0||


**Table 17.** Generator hyperparameters. 

|**Parameter**|**Value**|
|---|---|
|𝐾(latent-history chunks)|8|
|𝐻(latent chunk length)|15 frames (current + 14 future)|
|𝑇obs(max observation frames)|120 (𝐾× 𝐻)|
|Self-conditioning depth|8 chunks|
|𝑀(Euler steps)|4|
|𝑁(default chunks per free rollout)|20|
|Flow time distribution|Beta(1.5, 1.0), rescaled to[0, 0.999]|
|Timestep buckets|1000|
|Obs encoder LR|1×10<sup>−4</sup>|
|DiT generator LR|1×10<sup>−4</sup>|
|LR schedule|Cosine, min_lr5×10<sup>−7</sup>|
|Warmup steps|5000|
|Gradient clipping|1.0|
|Mixed precision|bf16 (VLM), fp32 (DiT)|
|Max training steps|200,000|


where sg(⋅) denotes stop-gradient. Thus, generated chunks are used as predicted conditioning context, but gradients are not back-propagated through earlier sampling steps or ODE integrations. 

The self-conditioned training loss combines the primary one-step flow-matching loss with the average loss over later self-conditioned chunks: 


Here, ℒ<sup>(1)</sup> Flow<sup>is the standard teacher-forced flow-matching loss for the first chunk, while ℒ(𝑘)</sup> Flow<sup>for 𝑘≥2 is computed using histories augmented</sup> with previously generated chunks. We use 𝜆sc = 0.25. 

We apply this objective according to a training curriculum. Let 𝑢 denote the current training step. Self-conditioning is disabled for the first 100k training steps: 


It is then linearly increased to 1 over the next 40k steps: 


Afterwards, self-conditioning is always enabled: 


At each training step, the self-conditioned objective is used with probability 𝑝sc(𝑢); otherwise, the generator is trained with the standard single-chunk teacher-forced flow-matching objective. 

16–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

This training strategy does not change the generator architecture. It only changes the distribution of histories observed during training, making them closer to the predicted histories encountered during autoregressive deployment. 

## **C. ADDITIONAL EXPERIMENTS AND ANALYSIS** 

### **C.1. Representation-Level Latent Diagnostics** 

This section supplements the main-paper latent temporal design ablation by defining the representation-level diagnostics used in Table 4. We use these diagnostics to evaluate whether the learned joint-intent latent contains future-relevant information, evolves coherently over time, and remains executable in closed-loop control. 

#### **_C.1.1. Future-Prediction Probe_** 

Probe@40 evaluates whether the current latent contains information about future robot motion 40 frames later. Given the current 64dimensional joint-intent latent 𝐳𝑡 and robot joint positions 𝐪𝑡, we construct a future joint-motion target from the residual 


To obtain a compact target, we project these joint residuals onto their leading PCA components. We then train a linear ridge probe to predict this future-motion target from 𝐳𝑡. The probe is trained on the training split and evaluated on held-out motion sequences. Probe@40 reports the Pearson correlation between the predicted and ground-truth future-motion targets on held-out sequences. Higher values indicate that the current latent contains more predictive information about upcoming motion. 

#### **_C.1.2. Latent Temporal Correlation_** 

Corr.@40 measures the temporal coherence of the latent trajectory. We compute the cosine similarity between latents separated by 40 frames: 


The score is averaged over valid frames and motion sequences. Higher values indicate that the latent evolves more smoothly and consistently over time. 

#### **_C.1.3. Closed-Loop Success at Fixed Horizons_** 

Succ.@20s and Succ.@60s measure long-horizon closed-loop executability. For each latent temporal design, we evaluate the corresponding DAJI-Act controller in simulation for fixed horizons of 20 seconds and 60 seconds. A rollout is counted as successful if it reaches the evaluation horizon without triggering termination conditions such as body-height or gravity-direction failure. We report the percentage of successful rollouts. 

### **C.2. Hyperparameter Sensitivity** 

We analyze the sensitivity to self-conditioning depth and latent-history length on the HumanML3D-style benchmark. These results show that DAJI is not tied to a fragile hyperparameter choice, but works across a reasonably broad operating regime. 

**Table 18. Hyperparameter sensitivity on HumanML3D.** Each history chunk contains 15 frames. In each block, we vary one factor while keeping the remaining settings fixed. 

|||Self-Cond|itioning D|epth|||
|---|---|---|---|---|---|---|
|Depth|MM-D↓|R@1↑|R@3↑|FID↓|MM↑|Succ. (%)↑|
|4 chunks|1.181|0.398|0.618|0.176|0.516|93.34|
|6 chunks|1.115|0.483|0.754|0.148|0.689|93.47|
|8 chunks|**1.093**|**0.549**|**0.796**|**0.147**|**0.847**|**94.42**|
|||Latent H|istory Len|gth|||
|History|MM-D↓|R@1↑|R@3↑|FID↓|MM↑|Succ. (%)↑|
|K=4 (60f)|1.132|0.480|0.743|0.177|0.792|93.38|
|K=8 (120f)|**1.093**|**0.549**|**0.796**|**0.147**|**0.847**|**94.42**|
|K=12 (180f)|1.129|0.478|0.731|0.170|0.587|93.70|


Table 18 shows that the main trends are stable. Increasing self-conditioning depth improves semantic alignment and rollout success, which is consistent with reducing exposure bias over longer rollout horizons. For latent-history length, 𝐾= 8 gives the strongest overall tradeoff across alignment, diversity, and success, while both shorter and longer histories underperform on at least part of the metric set. We therefore use eight self-conditioned chunks during training and 𝐾= 8 latent-history chunks at inference. 

### **C.3. Qualitative Generation Results** 

Figure 5 provides representative text-conditioned execution examples within the MuJoCo [3] simulation environment, illustrating robust tracking across a variety of dynamic and complex whole-body maneuvers. 

17–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 


_“A man is waving his right hand.”_ 


**Figure 5. Sim (MuJoCo) Validation Results:** Robust tracking performance on simple gestures to complex maneuvers. Any prompt phrase is interpreted only as a body-motion description; no object state or manipulation outcome is modeled or evaluated. 

18–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

## **D. ADDITIONAL INFORMATION** 

### **D.1. Extended Formulas** 

#### **_D.1.1. DDIM Reverse Step_** 

The deterministic DDIM [28, 31, 35, 37, 41–43] reverse step (𝜂= 0) from 𝜏 to 𝜏<sup>′</sup> given the predicted̂ 𝐱0: 


#### **_D.1.2. Intent Bottleneck KL Regularization_** 

The KL regularization for the intent encoder 𝐸ref : 


optionally clamped at a free-bits threshold to prevent posterior collapse. 

#### **_D.1.3. Flow-Matching Time Sampling_** 

The flow time 𝑠 is sampled as 𝑠= 0.999 ⋅𝑢 with 𝑢∼Beta(1.5, 1.0), then treated as 𝑠∈[0, 1] in the main text for notational simplicity. This distribution biases samples toward larger flow times, placing more emphasis on less noisy states closer to the data endpoint. 

#### **_D.1.4. Cosine Noise Schedule (DDPM)_** 

The forward-process variancē 𝛼𝜏 with 𝑇= 50: 


### **D.2. Existing Assets and Terms of Use** 

Table 19 lists the main external assets used in this work together with their stated licenses or usage terms. For datasets with access restrictions or downstream dependencies, we follow the terms of the official distribution source rather than redistributing the underlying files. 

**Table 19.** Main external assets used in this work. 

|**Asset**|**Role**|**Source / version**|**License / terms**|
|---|---|---|---|
|HumanML3D<br>BABEL|Single-instruction text-<br>motion benchmark<br>Long-horizon stream-<br>ing action annotations|Official HumanML3D release [11]<br>Official BABEL release [8]|MIT License<br>BABEL dataset license<br>for non-commercial scien-<br>tific research|
|Qwen3-VL-4B-<br>Instruct|Frozen language en-<br>coder|Qwen3-VL-4B-Instruct checkpoint; technical report [25]|Apache License 2.0|
|MuJoCo|Physics simulation en-<br>vironment|MuJoCo simulator [3]|Apache License 2.0|


### **D.3. Broader Impact** 

Language-conditioned humanoid control could benefit assistive robotics, animation, embodied AI prototyping, and human–robot interaction by making whole-body behavior easier to specify. However, a system that maps language to humanoid motion also creates clear risks if deployed in safety-critical or unstructured physical environments: ambiguous or adversarial instructions can trigger unintended behavior, generated motions may be dynamically executable in simulation yet unsafe on hardware, and the same capabilities could be misused for harmful physical tasks. Our large-scale quantitative experiments are limited to simulation and controlled robot-motion validation, while physical-hardware deployment is used for qualitative demonstration. Real-world deployment would require instruction filtering, hardware-level safety constraints, perception robustness, human supervision, and fail-safe monitoring that are outside the scope of this paper. 

19–20 

Before the Body Moves: Learning Anticipatory Joint Intent for Language-Conditioned Humanoid Control 

### **D.4. Limitations** 

DAJI has several important limitations. First, although DAJI includes qualitative deployment on physical humanoid hardware, our large-scale quantitative evaluations are conducted in simulation and controlled robot-motion validation. Therefore, the reported quantitative results should be interpreted with the sim-to-real gap in mind, rather than as evidence of fully safe autonomous real-world deployment. Second, performance is constrained by the coverage and granularity of the paired motion-language datasets and by the frozen language encoder: rare actions, ambiguous instructions, long-horizon compositional commands, and object-centric phrases may be unreliable when they are underrepresented in training data or cannot be grounded in the available observations. Third, the current system is instruction-conditioned but not fully interactive. DAJI can generate streaming motions from language commands, but it does not yet support multi-turn user correction, clarification, or online adjustment of motion style during execution. Finally, our current evaluation does not report full multi-seed error bars for all experiments because full humanoid-control retraining is expensive, and some text-motion metrics are computed on successfully exported motions with rollout success reported separately. Improving dataset diversity, adding richer grounding and safety constraints, and incorporating interactive language feedback are important directions for future work. 

20–20 

