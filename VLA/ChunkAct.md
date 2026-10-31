---
title: "ChunkAct: Action Chunking for Agentic Robotics"
date: "2026-10-13"
authors: "Bingxin Xu; Wenrui Bao; Xinxin Liu; Jiawei Zhou; Yuzhang Shang; Emilio Ferrara"
url: https://arxiv.org/abs/2610.18874
pdf: https://arxiv.org/pdf/2610.18874
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.18874)** / [論文ページ](https://arxiv.org/abs/2610.18874)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ChunkAct: Action Chunking for Agentic Robotics** 

**Bingxin Xu**<sup>1</sup> **Wenrui Bao**<sup>2</sup> **Xinxin Liu**<sup>2</sup> **Jiawei Zhou**<sup>3</sup> **Yuzhang Shang**<sup>2</sup> **Emilio Ferrara**<sup>1</sup> 1University of Southern California 2University of Central Florida 3Stony Brook University 

## **Abstract** 

Agentic robotics places a large language model (LLM) agent in the robot control loop, where it composes perception, motion, and visionlanguage-action (VLA) tools under the guidance of a memory and thereby generalizes to new tasks without retraining. This generality comes at a steep price in efficiency. Every primitive requires a round of LLM reasoning over the full interaction history, so the cost of an episode grows with the number of primitives. We find this reasoning largely redundant: once a sub-goal is chosen, its primitives follow a routine already prescribed by memory. We present **ChunkAct** , which introduces action chunking to agentic robotics. Online, a single call launches a chunk of chained primitives, which executes autonomously and returns control only upon failure. Offline, **ChunkAct** compiles the memory into these chunks, so execution is memoryfree at test time and the planner is reserved for decisions that require reasoning. LLM computation therefore scales with the number of decisions rather than the number of primitives. On LIBERO-Pro, **ChunkAct** improves task success by 5.0 points over the state of the art in agentic robotics while requiring 2.9 _×_ fewer LLM calls, 4.4 _×_ fewer input tokens, and 2.3 _×_ fewer output tokens. 

## **1 Introduction** 

Agentic robotics has emerged as a new paradigm for robot manipulation (Liang et al., 2023; Kumar, 2026; Fu et al., 2026; Tsui et al., 2026; Zhang et al., 2026c; Jia et al., 2026; Xu et al., 2026b,a). Rather than training a policy that maps pixels and language directly to motor commands (Brohan et al., 2023a; Kim et al., 2024; Black et al., 2024), it places a large language model (LLM) agent in the control loop and equips it with perception, motion, and vision-language-action (VLA) tools, together with a memory of what has worked before. At each step, the agent observes the scene, consults the memory, reasons, and issues a single tool call (Figure 1, 

top). Because each task is composed by reasoning rather than learned from demonstrations, the agent handles new tasks without retraining and succeeds where end-to-end policies break down. For example, with no robot-specific training, GPT-6 Astra driven through a generic agent harness completes a real-arm pick-and-place task in 19 of 20 trials (OpenAI, 2026; Menon et al., 2026) and ranks above every public policy on the RoboDojo benchmark (Zhang et al., 2026b), which illustrates the generalization this paradigm affords. 

However, this generalization comes at a steep price in efficiency. The planner acts through primitives, i.e., robot skills invoked as tool calls, each of which requires a dedicated round of LLM reasoning. Every such round reprocesses the full interaction history, and reasoning models further consume output tokens before responding (Sui et al., 2025). Consequently, the number of calls and output tokens scales linearly with the number of primitives in an episode, while input tokens scale quadratically (Kapoor et al., 2024; Kim et al., 2026a), as illustrated in Fig.1 Top. For instance, a single pickand-place task requires 24.2 LLM calls and 2.2M input tokens on average, costing about $22 per episode with GPT-6 Astra and still $11 even with the cheaper GPT-5.5.<sup>1</sup> As tasks grow longer, this overhead quickly dominates the cost of execution, hindering the scalability of LLM-based agents. 

To address this inefficiency, we analyze the agent’s behavior and find that LLM reasoning is frequently redundant. Once a sub-goal is selected and its targets are localized, the subsequent primitives follow a fixed routine already encoded in memory, such that each additional call merely reproduces a decision that has already been made. Although a single read of memory suffices to capture this routine, the LLM tends to deliberate over each step and constantly returns to memory for 

> 1Estimated at OpenAI’s list API prices as of October 2026. 

1 


Figure 1: **ChunkAct introduces action chunking to agentic robotics, improving both task success and efficiency.** Top: prior methods invoke the LLM planner once per primitive, so the number of LLM calls and the context length grow with every step. Bottom: **ChunkAct** invokes the planner once to launch an action chunk, which executes autonomously and returns a typed error only upon failure. Right: **ChunkAct** gains both task success and efficiency. 

guidance. Furthermore, the memory retrieval and LLM reasoning become less reliable as the context grows (Liu et al., 2024; Laban et al., 2026). This overhead could therefore be eliminated by compiling memory into generalizable action sequences that execute without the planner’s step-by-step involvement. This concept also echoes the action chunk (Zhao et al., 2023) in robotics. 

Building on this observation, we propose **ChunkAct** (Action Chunking for Agentic Robotics), which consists of two complementary components: chunked execution at test time and memory internalization offline. **At test time, ChunkAct introduces action chunking to agentic robotics.** It composes the primitives that realize a sub-goal into an executable chunk, which the planner invokes with a single call and which then runs to completion autonomously. This design confines the LLM to where reasoning is genuinely required: understanding the physical scene, diagnosing failures, and redirecting the plan. To support this, a failed chunk returns a typed exit that specifies the failed primitive along with an error log, providing the planner with structured feedback for recovery. In this way, LLM computation scales with the number of decisions rather than the number of primitives (See Fig.1 Bottom). Offline, **ChunkAct** builds these chunks as generalizable routines with memory compiled into them. The parameters and procedural knowledge that govern each chunk are compiled from memory before deployment, making its actions inherently memory-conditioned. As a result, chunks run memory-free at test time, eliminating frequent memory retrieval and further improving 

the efficiency of the LLM. 

Together, these two components improve both efficiency and performance. By substantially reducing the number of LLM calls and the length of the context, **ChunkAct** lowers the overall cost of each episode. Meanwhile, because the planner reasons over a concise context and memory is internalized throughout execution, **ChunkAct** also achieves higher task success rates (See Fig.1 Right). To summarize, our contributions are threefold. 

- To our knowledge, **ChunkAct** is the first LLM agent for robot manipulation that commits to a chunk of chained perception and control primitives per call rather than to a single primitive. 

- **ChunkAct** compiles memory offline into generalizable action chunks, enabling memory-free execution at test time and reserving the LLM for decisions that genuinely require reasoning. 

- Compared with the previous SOTA agentic robotics approach, **ChunkAct** improves success by 5.0 points on LIBERO-Pro, while requiring 2.9 _×_ fewer LLM calls, 4.4 _×_ fewer input tokens, and 2.3 _×_ fewer output tokens. It also exhibits strong zero-shot transfer capability. 

## **2 Related Work** 

**Agentic robotics.** Language models entered manipulation as planners that sequence a fixed repertoire of skills, grounded in affordances and closed by textual feedback (Brohan et al., 2023b; Huang et al., 2022). Code as Policies turned the plan into a program over perception and control interfaces (Liang et al., 2023), and later work widened 

2 

what the program could express with structured prompts, foundation perception, and value maps (Singh et al., 2022; Huang et al., 2023a,b; Mu et al., 2024). A parallel line places a reasoning model above a learned policy rather than around it (Belkhale et al., 2024; Shi et al., 2025; Physical Intelligence et al., 2025). The two lines have converged in _agentic robotics_ , where an LLM agent sits in the control loop, calls perception, motion, and VLA tools, and keeps a memory of what has worked (Fu et al., 2026; Tsui et al., 2026; Kumar, 2026; Jia et al., 2026; Zhang et al., 2026c; Xu et al., 2026b,a). All of this work is measured by what the agent can accomplish, and none of it addresses the cost of consulting the planner before every primitive, which has been approached only by caching plans for tasks seen before (Zhang et al., 2026a; Kim et al., 2026a). To our knowledge, we are the first to improve efficiency in agentic robotics systems by consolidating recurring call sequences into reusable action routines. 

**Action chunking in robotics.** How many actions a policy commits to per decision is a design choice that trades reactivity against consistency and cost. Policies that query the model once per control step (Brohan et al., 2022, 2023a; Kim et al., 2024) tie inference cost to control frequency and let errors compound between queries. Action chunking, introduced by ACT (Zhao et al., 2023) and adopted by Diffusion Policy (Chi et al., 2025), predicts a short sequence of actions per inference, and VLA models have since built it into their action heads and tokenizers (Black et al., 2024; Kim et al., 2025; Pertsch et al., 2025). Subsequent work tunes the trade-off by interleaving chunks for closed-loop reactivity (Liu et al., 2025; Black et al., 2026), and world-action models extend chunked prediction from actions to future observations (Du et al., 2023; Wu et al., 2024; Kim et al., 2026b). In all of these, a chunk is a short sequence of motor commands from a learned policy, and how much an LLM agent should commit to per decision has been asked only in text environments (Yang et al., 2026). To our knowledge, we are _the first to explore action chunking in agentic robotics, where a chunk spans perception, control primitives, and internalized memory rather than motor commands_ . 

**Memory in agentic robotics.** Memory lets an LLM agent improve without weight updates, and its forms differ in what is stored rather than in how it is used. Reflective memory stores trajecto- 

ries or the lessons drawn from them and returns relevant entries to the prompt (Park et al., 2023; Shinn et al., 2023; Zhao et al., 2024; Packer et al., 2023). Procedural memory stores what worked as code, from skill libraries (Wang et al., 2023) to induced workflows (Wang et al., 2024) and robot programs adapted to new contexts (Kagaya et al., 2025; Woods and Seifi, 2026). Robot harnesses keep rule cards and task records written by the planner itself (Zhang et al., 2026c), transition conditions between subtasks (Xu et al., 2026b), or a demonstration video navigated at a chosen granularity (Anonymous, 2026). In every form, the planner decides what to retrieve and when, reads it into context, and interprets it before acting, so the memory is consumed at test time and its value is bounded by the planner’s ability to use it (Zhang et al., 2025). Li et al. (2025) comes closest to breaking this pattern by distilling recurring spans into a datastore that is emitted rather than read, yet its chunks remain text. We are the first work to explore compiling agentic memory offline into physical action, producing executable action chunks that require no memory access at deployment. 

## **3 Action Chunking for Agentic Robotics** 

### **3.1 Preliminaries** 

We begin by formalizing agentic robotics, the setting in which **ChunkAct** operates. 

**The agentic loop.** An agentic system solves a manipulation task with an LLM planner _G_ that sequentially composes primitives from a library _P_ , 


Here _ct_ denotes the context window of the planner at step _t_ , initialized with the task instruction as _c_ 0 = _ℓ_ . At each step, the planner reasons over _ct_ and outputs _at_ , which specifies the primitive to execute, _pt ∈P_ , and its arguments _θt_ . The primitive runs to completion and returns a result _yt_ , which is appended to the context with _at_ . The process repeats until the task is completed at _T_ . 

Notably, not every planner output is a robot action. Action primitives alter the physical state of the robot, whereas informational primitives leave the scene intact and only return content, either from perception or from a memory _M_ (Section B). Since every result is appended to _ct_ , an informational call is paid for not only once, but again as input at every subsequent step. 

3 


Figure 2: **Distribution of LLM planner’s tool calls on LIBERO.** Memory reads and perception dominate. 

As the planner re-reads its entire context at every call, a _T_ -step episode costs _T_ planner calls and 


input tokens, where _| · |_ counts tokens. Each call reasons before it answers, so calls and output tokens grow linearly in _T_ , while input tokens grow quadratically. Equation (2) identifies two quantities that govern the cost: the number of steps _T_ , and the length of each appended pair ( _as, ys_ ), which is paid again at every later step. For instance, Harness VLA takes on average 24.2 planner calls and 2.2M input tokens per episode (see Table 2). 

We analyze the planner’s tool calls and reveal two sources of inefficiency. ❶ The <u>planner</u> conflates deciding with executing. Every primitive incurs a full round of reasoning, even though, once a sub-goal is fixed, the primitives that realize it are largely determined by the memory; the planner is thus invoked far more often than the task demands decisions. ❷ The <u>planner</u> spends most of its calls <u>gathering</u> information rather than acting. Only 20.5% of calls invoke an action primitive, while memory reads and perception account for 31.7% and 44.3%, respectively (See Fig.2). Since _M_ is static across episodes, these reads retrieve the same knowledge again and again, inflating the context without informing new decisions. These two findings motivate **ChunkAct** , which **brings action chunking to agentic robotics** through offline action chunk building (Section 3.2) and online action chunk triggering (Section 3.3). 

### **3.2 Offline action chunk building** 

Targeting the ❶ issue, **ChunkAct** outputs action chunks rather than single primitives. The planner is reengaged only when the chunk fails, reserving LLM reasoning for the decisions that require it. 

The memory of an LLM agent already records the general, reusable success rules and and procedural context for tasks. **ChunkAct** compiles all memory once into executable chunk form rather 

than letting the planner re-derive it at every step (Figure 3(a)). Memory construction begins with a partition over task categories. A manipulation instruction decomposes into an ordered sequence of typed sub-goals, and the space of such types remains small even as the task set grows. For example, two types suffice to cover a broad range of tabletop manipulation: transport, which relocates an object onto or into a receptacle, and fixture, which actuates an articulated element of the scene. All memory entries pertaining to a given type, from general execution rules to task-specific records, are therefore consolidated into a single source and compiled into a unified chunk, parameterized by the object classes on which it operates. 

Compilation retains only the procedural knowledge that defines how a task type is executed: the ordering of stages, the primitive assigned to each stage, the stage-level parameters conditioned on object class, the fallback strategies to attempt when a stage fails, and the criteria used to verify each stage. The primitive assignment, for instance, preserves the division of labor recorded in memory, delegating contact-rich stages such as grasping or fixture actuation to the VLA policy and the remaining stages to analytic primitives. Conversely, any quantity unobservable at deployment time is excluded. Recorded coordinates and privileged simulator state are discarded, and all geometric quantities are re-estimated from live perception of the current scene. This decoupling allows a chunk to transfer to scenes whose layouts differ from those encountered during memory construction. 

The resulting chunk is an executable routine that captures the recurring procedure of its task type. A single chunk covers every task of its type, with class-dependent content resolved by lookup within the chunk. The planner is thus relieved of both memory retrieval and step-by-step primitive selection at run time. During execution, each stage is verified before the next begins, and the library is compiled once and kept frozen. 

### **3.3 Online action chunk triggering** 

To sovle the ❷ problem, **ChunkAct** internalizes the memory _M_ into executable chunks, allowing memory-free execution at run time. 

At test time the planner invokes chunks in place of primitives, through a single tool call (Figure 3(b) labels **ChunkAct** ). The instruction is parsed into its ordered sequence of typed sub-goals, each subgoal selects the chunk of its kind, and the planner’s 

4 


Figure 3: **The two stages of ChunkAct.** Left: offline, **ChunkAct** internalizes memory by compiling it into executable action chunks. Right: online, the LLM planner invokes **ChunkAct** via a single function call, which executes an entire action chunk autonomously and returns a typed error code to the planner only upon failure. 

interface to execution narrows to two operations, grounding a target in the current observation and launching the chunks. An episode therefore begins with the planner interpreting the task and the scene, grounding the first target, and issuing one call, after which the chunks run the sub-goals until the task is complete without any further request to the planner. No memory is read along the way, since everything the planner would have retrieved has been compiled into the chunks, and the planner’s context holds only the instruction, the observations it has requested, and the exits it has received. 

Chaining the stages under one call, rather than exposing each stage as a separate call, follows from where reasoning is actually needed. Compiling memory and perception into chunks removes the cost of retrieval and repeated observation, but a per-stage interface would still return control to the planner after every action, turning each step of execution into a round of deliberation. Most of these rounds involve no decision. 

Once its target is grounded, the stages of a subgoal follow a fixed order, so a successful stage already determines the next one and requires no reasoning to select it. A chunk therefore chains the stages directly and returns control to the planner only when a stage fails. 

Control returns to the planner only when a chunk fails, and it does so through a typed exit. Every stage of a chunk raises its own error code, so the exit names the stage that failed and the reason it failed, such as a perception call that cannot locate its target, a policy call that loses the object, or a 

verification that cannot confirm the sub-goal, and it carries the error log with the robot state and fresh observations (Section A). The planner then reperceives the scene from its true state, and chooses among three responses, namely grounding the target again and re-invoking the chunk, redoing a sub-goal whose verification failed, or falling back to the primitives for a situation the library does not cover. Each response is a decision that requires understanding the task and the scene, and none is a step of execution, so the planner is consulted at decision points and nowhere else. 

### **3.4 Role of LLM planner in agentic robotics** 

We examine how this design changes the role of the planner, from stepwise executor to sub-goal selector and failure handler. 

Taken together, the two stages redefine the role of the planner. In the per-primitive loop of Equation (1), the planner serves as both reasoner and executor, treating every step alike regardless of whether it requires judgment. **ChunkAct** separates the two: execution is delegated to the chunks, while the planner retains only what cannot be compiled, namely understanding the task and scene and responding to failure. This separation reshapes both sides of the loop. 

On the input side, the dominant sources of context are removed. Memory is internalized in the chunks rather than retrieved online, and perception is performed within each chunk rather than requested before every primitive. The context thus stays compact across an episode, containing only 

5 

Table 1: **Task success on LIBERO-Pro.** Task success rate (%) under instruction redirection (T) and position swap (S) for each suite. Harness VLA and **ChunkAct** both use GPT-5.6-sol with high thinking. Best entry is in bold. 

||**Method**|**Spat-T**|**Spat-S**|**Obj-T**|**Obj-S**|**Goal-T**|**Goal-S**|**L10-T**|**L10-S**|**Overall**|
|---|---|---|---|---|---|---|---|---|---|---|
||OpenVLA (Kim et al.,2024)|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|
||_π_0 (Black et al.,2024)|0.0|0.0|0.0|2.0|0.0|0.0|0.0|0.0|0.3|
||_π_0_._5 (Physical Intelligence et al.,2025)|1.0|20.0|1.0|17.0|2.0|38.0|1.0|8.0|11.0|
|A|MolmoAct (Lee et al.,2026)|0.0|0.0|0.0|6.0|0.0|0.0|6.0|0.0|1.5|
|VL|NORA (Hung et al.,2025)|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|
||X-VLA (Zheng et al.,2026)|0.0|0.0|8.0|2.0|9.0|1.0|10.0|0.0|3.8|
||AtomVLA (Sun et al.,2026)|1.0|16.0|0.0|10.0|11.0|2.0|9.0|1.0|6.3|
||_π_RLinf (Yu et al.,2026)|42.0|59.0|71.0|78.0|45.0|42.0|49.0|14.0|50.0|
|nt|CaP-X (Fu et al.,2026)|14.0|12.0|18.0|22.0|17.0|26.0|/|/|18.2|
|ge|Harness VLA (Zhang et al.,2026c)|**100.0**|80.0|80.0|**100.0**|70.0|80.0|**60.0**|60.0|78.8|
|A|+**ChunkAct**(ours)|94.0|**82.0**|**98.0**|**100.0**|**80.0**|**86.0**|**60.0**|**70.0**|**83.8**|


Table 2: **Efficiency analysis and LLM role ablation on LIBERO-Pro.** Average TSR (%), planner calls, input tokens (M), and output tokens (k) with GPT-5.6-sol in two reasoning settings. Green rows show the gain over Harness VLA. Last row runs chunks with no LLM call. 

|**Method**|**Reasoning**|**TSR **|**Calls **|**In (M) **|**Out (k)**|
|---|---|---|---|---|---|
|Harness VLA|High|78.8|24.2|2.2|8.5|
|+**ChunkAct**|High|**83.8**|**8.3**|**0.5**|**3.7**|
|||**+5.0**|**2.9**_×_|**4.4**_×_|**2.3**_×_|
|Harness VLA|None|56.0|24.9|2.4|6.4|
|+**ChunkAct**|None|**80.0**|**6.6**|**0.4**|**1.3**|
|||**+24.0**|**3.8**_×_|**6.0**_×_|**4.9**_×_|
|+**ChunkAct**|No planner|57.5|/|/|/|


the instruction, decision-time observations, and exits. On the output side, the unit of action shifts from a single primitive to a chained chunk. Each step _at_ is either a chunk launch or a response to an exit, so the planner is invoked per decision rather than per action, and reasoning is spent only where it is required. Episode cost therefore scales with the number of decisions rather than procedure length. 

## **4 Experiments** 

### **4.1 Setup** 

**Benchmarks.** We evaluate on two benchmarks from the LIBERO family. Our main experiments use LIBERO-Pro (Zhou et al., 2025), which perturbs the four LIBERO suites (Liu et al., 2023), Spatial, Object, Goal, and LIBERO-10, along objects, initial states, instructions, and environments. Following Zhang et al. (2026c), we evaluate the instruction and initial-state perturbations, denoted instruction redirection (T) and position swap (S). Each of the resulting eight suite and perturbation combinations contains 10 tasks. As in that protocol, we run 10 seeds per task, so that each combination aggregates 800 episodes. We further use LIBERO-Plus (Fei et al., 2025) benchmark, which 

varies the LIBERO tasks along seven axes: object layout, camera viewpoint, robot initial state, language, lighting, background, and sensor noise. As its 10,030 variants are too many to evaluate exhaustively, we run a single seed on every task under each of the seven perturbation axes, which covers the full range of perturbations at a tractable cost. 

**Metrics.** We measure performance by the task success rate (TSR), as determined by the environment’s termination signal. We measure efficiency by the number of planner calls and the numbers of input and output tokens per episode. 

**Baselines.** For the main experiment, we compare with eight end-to-end VLA models, OpenVLA (Kim et al., 2024), _π_ 0 (Black et al., 2024), _π_ 0 _._ 5 (Physical Intelligence et al., 2025), MolmoAct (Lee et al., 2026), NORA (Hung et al., 2025), X- VLA (Zheng et al., 2026), AtomVLA (Sun et al., 2026), and the RLinf-fine-tuned _π_ 0 _._ 5 checkpoint that serves as our VLA primitive, which we denote _π_ RLinf (Yu et al., 2026), and with CaP-X (Fu et al., 2026), an agent that writes code over perception and motion primitives without a VLA. Their results are those reported by Zhang et al. (2026c). Harness VLA and **ChunkAct** are run by us. For LIBERO-Plus experiment results, the VLA models’ performance are as reported by Fei et al. (2025). 

**Implementation.** The planner is GPT-5.6-sol at high reasoning effort running in Codex (OpenAI, 2025), with a budget of 100 LLM calls per episode. The VLA primitive is _π_ RLinf , and SAM 3 (Carion et al., 2026) provides segmentation. **ChunkAct** and Harness VLA (Zhang et al., 2026c) share the same set-up and the same task-specific and global memory. They differ only in how the memory is used: Harness VLA reads it at test time, whereas **ChunkAct** internalizes it offline into executable chunks and reads no explicit memory at test time. 

6 

Table 3: **Task success on LIBERO-Plus.** Task success rate (%) under all seven perturbation setting. **ChunkAct** runs GPT-5.6-sol at the high reasoning setting with seed 0. The best entry in each column is in bold. 

|**Method**|**Camera**|**Robot**|**Language**|**Light**|**Background**|**Noise**|**Layout**|**Overall**|
|---|---|---|---|---|---|---|---|---|
|OpenVLA (Kim et al.,2024)|1.1|4.1|26.8|4.4|25.3|19.3|31.6|16.1|
|OpenVLA-OFT (Kim et al.,2025)|59.7|37.2|81.5|85.8|92.4|76.7|77.1|72.9|
|OpenVLA-OFT_w_ (Kim et al.,2025)|16.8|43.7|73.2|68.2|**92.5**|51.4|72.3|59.7|
|OpenVLA-OFT_m_ (Kim et al.,2025)|57.9|30.6|83.6|91.6|83.6|76.3|73.2|71.0|
|_π_0 (Black et al.,2024)|15.8|6.6|61.0|79.6|78.5|79.4|70.4|55.9|
|_π_0-FAST (Pertsch et al.,2025)|66.4|24.8|63.3|73.0|67.7|75.8|70.3|63.0|
|NORA (Hung et al.,2025)|4.0|41.1|67.0|31.0|50.5|17.6|63.9|39.3|
|WorldVLA (Cen et al.,2025)|0.3|30.2|44.2|29.4|14.5|12.2|39.4|24.3|
|UniVLA (Bu et al.,2025)|4.3|50.3|71.8|59.1|80.0|25.3|34.3|46.4|
|RIPT-VLA (Tan et al.,2025)|58.3|36.7|80.1|87.9|90.4|73.8|76.5|72.0|
|+**ChunkAct**(ours)|**77.5**|**75.0**|**87.5**|**95.0**|82.5|**87.5**|**82.5**|**83.9**|


### **4.2 Main results** 

**Task success performance.** As shown in Table 1, **ChunkAct** achieves the highest task success rate on LIBERO-Pro, outperforming both endto-end VLAs and agentic robotic systems. It attains an overall success rate of 83.8%, exceeding the strongest prior method, Harness VLA, by 5.0 points. The perturbations in LIBERO-Pro, instruction redirection and position swap, require a policy to act on instructions and object layouts that differ from those seen in training, and end-to-end VLAs largely fail under them. This failure extends to _π_ RLinf , the checkpoint that **ChunkAct** invokes as its contact primitive, which trails **ChunkAct** by 43.8 points. Since the primitive alone does not generalize to these perturbations, whatever success an agent recovers must come from how it grounds the task in the current scene before the primitive is called. Placing an LLM planner above the VLA recovers much loss, as the agentic baselines show, yet Harness VLA stops at 78.8% despite sharing the same planner, primitive, perception, and memory with **ChunkAct** . The two systems differ only in how memory is used. Harness VLA retrieves memory at test time and relies on the planner to reinterpret past experience at every call, whereas **ChunkAct** compiles it offline into executable chunks that encode how each task succeeds. The gap therefore isolates the benefit of memory internalization. **Efficiency analysis.** As shown in Table 2, **ChunkAct** attains its higher success rate at a fraction of the LLM cost. The first two rows correspond to the Harness VLA and **ChunkAct** entries in Table 1. Relative to Harness VLA, **ChunkAct** issues 2.9 _×_ fewer LLM calls and consumes 4.4 _×_ fewer input tokens and 2.3 _×_ fewer output tokens, while improving success by 5.0 points. The third and fourth rows repeat this comparison with rea- 

soning disabled, and the efficiency advantage of **ChunkAct** grows further. Both observations stem from memory internalization. Harness VLA spends most LLM calls on perception queries and memory reads, and each result is appended to the context, so the context keeps growing over the episode. **ChunkAct** folds these steps into the executable chunks, so they run at test time without invoking the LLM and their results never enter the context window. The planner is called only at the decision points that the chunks leave open. Fewer calls over a shorter context reduce the input tokens, and fewer planning decisions reduce the output tokens. 

### **4.3 Analysis of LLM planner role in ChunkAct** 

**Analyzing the LLM planner reasoning impact.** As shown in Table 2, **ChunkAct** remains robust when the reasoning of LLM planner is disabled, whereas Harness VLA does not. The task success rate of **ChunkAct** stays stable across reasoning settings, while Harness VLA degrades sharply once reasoning is turned off. This contrast reflects how heavily each system relies on the planner. Harness VLA depends on the LLM at every step: each call must interpret the retrieved memory, decide what to perceive, and issue the correct next action, so the errors of a weaker planner accumulate over the episode. **ChunkAct** instead decouples the LLM from the execution it does not need to perform. With memory already internalized into the chunks, the planner is consulted only for the remaining decisions, which leaves a weaker planner far fewer opportunities to fail. 

**Quantifying the LLM agent’s contribution.** To measure how much the planner contributes within **ChunkAct** , the last row of Table 2 executes the chunks under a scripted driver that makes no LLM call. The chunks alone reach 57.5%, which cor- 

7 


Figure 4: **Demo of a successful rollout on LIBERO-Pro with ChunkAct.** Given the task “pick up the can and place it in the basket,” the LLM planner first perceives the scene and invokes ChunkAct to execute a chained action sequence. The can is grasped successfully but slips during transport, so ChunkAct returns the error code. The planner interprets this feedback, re-localizes the can, and invokes ChunkAct again, which completes the task. 

responds to episodes in which the compiled routines succeed without intervention. The LLM in **ChunkAct** without reasoning therefore accounts for the remaining 22.5 points. This contribution comes from recovery: when a chunk fails, the planner is invoked to interpret the current scene and direct the next step, which a scripted driver cannot. The LLM thus serves not as a step-by-step executor but as a recovery mechanism invoked where the compiled routine falls short, which is why it adds substantial success at a small cost in calls and tokens. 

### **4.4 Generalization to unseen perturbations** 

**Out-of-distribution test.** The memory of **ChunkAct** is compiled on LIBERO-Pro and includes task-specific memory, which prior work found necessary on that benchmark (Zhang et al., 2026c). To test whether **ChunkAct** overfits to these tasks, we apply it unchanged to LIBERO-Plus (Fei et al., 2025), which perturbs the LIBERO tasks along seven dimensions that the memory doesn’t cover. The chunk library and planner prompt are those of Section 4.2, so the evaluation is fully zeroshot, whereas the VLA baselines, whose numbers are taken from Fei et al. (2025), are fine-tuned on the benchmark data. 

**Zero-shot transfer. ChunkAct** achieves the best overall success rate in Table 3, exceeding the strongest prior method by 11.0 points and leading in six of the seven dimensions. The margin is widest under camera and robot initial-state perturbations, where **ChunkAct** stays above three quarters while the best VLA falls to two thirds and one half, respectively. Because a chunk recomputes its targets from perception in every episode, such changes alter the measured geometry but not the procedure. These results show zero-shot transfer of internalized memory to unseen perturbations rather than overfitting to the tasks it was compiled from. 

### **4.5 Qualitative analysis** 

Figure 4 follows a single LIBERO-Pro episode and shows how the planner’s eight calls are distributed over 22 seconds of execution. The planner is engaged at two points only. At the start it views the scene and launches a chunk, which grasps and lifts the can without further LLM request. During the move, however, the can slips out of the gripper, and the chunk terminates with a typed exit. It returns a hand-off block, a structured error report that adds context to the error code. The planner resumes from the true state of the scene rather than from its expectation of it, spends four calls re-pointing the can, and triggers ChunkAct again, which carries the can to the basket, places it, and finishes on its own once the environment reports success. The episode makes visible the division of labor that Table 2 quantifies. The planner is reserved for understanding, while the chunks handle execution. It plans the next action chunk from the scene, and re-plans when a chunk fails. 

## **5 Conclusion** 

Agentic robotics generalizes to novel tasks without retraining, but at a steep cost in efficiency. We identify two bottlenecks: the LLM planner reasons before every primitive, although the primitives of a sub-goal follow a recurring pattern, and most of its calls are spent on perception and memory retrieval rather than action. **ChunkAct** is the first work to introduce action chunking to agentic robotics, and it internalizes memory into executable chunks offline. The LLM is thereby decoupled from routine execution and engaged only where reasoning is genuinely required, which improves LLM efficiency significantly. On LIBERO-Pro, **ChunkAct** improves task success by 5.0 points over the SOTA method with 2.9 _×_ fewer LLM calls, 4.4 _×_ fewer input tokens, and 2.3 _×_ fewer output tokens, and it transfers zeroshot to unseen tasks on LIBERO-Plus. 

8 

## **References** 

Anonymous. 2026. Recursive video in-context learning for agentic robot. Under review. 

- Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quon Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. 2024. RT-H: Action hierarchies using language. _arXiv preprint arXiv:2403.01823_ . 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. 2024. _π_ 0: A vision-language-action flow model for general robot control. 

- Kevin Black, Manuel Y. Galliker, and Sergey Levine. 2026. Real-time execution of action chunking flow policies. In _Advances in Neural Information Processing Systems_ . 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. 2023a. RT-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ . 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. 2022. RT-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ . 

- Anthony Brohan, Yevgen Chebotar, Chelsea Finn, Karol Hausman, Alexander Herzog, Daniel Ho, Julian Ibarz, Alex Irpan, Eric Jang, Ryan Julian, et al. 2023b. Do as I can, not as I say: Grounding language in robotic affordances. In _Conference on Robot Learning (CoRL)_ . 

- Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. 2025. UniVLA: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ . 

- Nicolas Carion, Laura Gustafson, Yuan-Ting Hu, Shoubhik Debnath, Ronghang Hu, Didac Suris Coll-Vinent, Chaitanya Ryali, Kalyan Vasudev Alwala, Haitham Khedr, Andrew Huang, et al. 2026. Sam 3: Segment anything with concepts. In _International conference on learning representations_ . 

- Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. 2025. WorldVLA: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ . 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. 2025. Diffusion policy: Visuomotor policy learning via action diffusion. 

- Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. 2023. Learning universal policies via text-guided video generation. In _Advances in Neural Information Processing Systems_ . 

- Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. 2025. LIBERO-Plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ . 

- Letian Fu, Justin Yu, Karim El-Refai, Ethan Kou, Haoru Xue, Huang Huang, Wenli Xiao, Guanzhi Wang, Dantong Niu, Fei-Fei Li, et al. 2026. CaP-X: A framework for benchmarking and improving coding agents for robot manipulation. _arXiv preprint arXiv:2603.22435_ . 

- Siyuan Huang, Zhengkai Jiang, Hao Dong, Yu Qiao, Peng Gao, and Hongsheng Li. 2023a. Instruct2Act: Mapping multi-modality instructions to robotic actions with large language model. _arXiv preprint arXiv:2305.11176_ . 

- Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. 2023b. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ . 

- Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, et al. 2022. Inner monologue: Embodied reasoning through planning with language models. _arXiv preprint arXiv:2207.05608_ . 

- Chia-Yu Hung, Qi Sun, Pengfei Hong, Amir Zadeh, Chuan Li, U Tan, Navonil Majumder, Soujanya Poria, et al. 2025. NORA: A small open-sourced generalist vision language action model for embodied tasks. _arXiv preprint arXiv:2504.19854_ . 

- Mengzhao Jia, Yang Lin, Xixin Zhang, Zhihan Zhang, Xiaobai Liu, and Meng Jiang. 2026. Agent as policy for robotic manipulation. _arXiv preprint arXiv:2609.12541_ . 

- Tomoyuki Kagaya, Subramanian Lakshmi, Yuxuan Lou, Thong Jing Yuan, Jayashree Karlekar, Sugiri Pranata, Natsuki Murakami, Akira Kinose, and Yang You. 2025. Memory transfer planning: LLM-driven context-aware code adaptation for robot manipulation. _arXiv preprint arXiv:2509.24160_ . 

- Sayash Kapoor, Benedikt Stroebl, Zachary S Siegel, Nitya Nadgir, and Arvind Narayanan. 2024. AI agents that matter. _arXiv preprint arXiv:2407.01502_ . 

- Hojoon Kim, Yuheng Wu, and Thierry Tambe. 2026a. AgenticCache: Cache-driven asynchronous planning for embodied AI agents. In _Proceedings of Machine Learning and Systems_ . 

9 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. 2025. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ . 

- Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, et al. 2026b. Cosmos policy: Fine-tuning video models for visuomotor control and planning. _arXiv preprint arXiv:2601.16163_ . 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. 2024. OpenVLA: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ . 

- Vaishak Kumar. 2026. Act-observe-rewrite: Multimodal coding agents as in-context policy learners for robot manipulation. _arXiv preprint arXiv:2603.04466_ . 

- Philippe Laban, Hiroaki Hayashi, Yingbo Zhou, and Jennifer Neville. 2026. LLMs get lost in multi-turn conversation. In _International Conference on Learning Representations (ICLR)_ . 

- Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, et al. 2026. MolmoAct: Action reasoning models that can reason in space. In _IEEE International Conference on Robotics and Automation (ICRA)_ . 

- Yanhong Li, Karen Livescu, and Jiawei Zhou. 2025. Chunk-distilled language modeling. In _International Conference on Learning Representations (ICLR)_ . 

- Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. 2023. Code as policies: Language model programs for embodied control. In _2023 IEEE International conference on robotics and automation (ICRA)_ . 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. 2023. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems_ . 

- Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2024. Lost in the middle: How language models use long contexts. _Transactions of the Association for Computational Linguistics_ . 

- Yuejiang Liu, Jubayer Ibn Hamid, Annie Xie, Yoonho Lee, Max Du, and Chelsea Finn. 2025. Bidirectional decoding: Improving action chunking via guided test-time sampling. In _International Conference on Learning Representations_ . 

- Achu Menon, Sravanthi Machcha, Sabrina Zou, Tzu Kit Chan, and Jay Chooi. 2026. GPT-6 Astra on robotic manipulation. Robocurve evaluation report, https: //openai.robocurve.org/gpt-6-astra/. 

- Yao Mu, Junting Chen, Qinglong Zhang, Shoufa Chen, Qiaojun Yu, Chongjian Ge, Runjian Chen, Zhixuan Liang, Mengkang Hu, Chaofan Tao, et al. 2024. RoboCodeX: Multimodal code generation for robotic behavior synthesis. _arXiv preprint arXiv:2402.16117_ . 

- OpenAI. 2025. Codex CLI. https://github.com/ openai/codex. 

- OpenAI. 2026. Introducing GPT-6 Astra. https:// openai.com/index/gpt-6-astra/. 

- Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez. 2023. MemGPT: Towards LLMs as operating systems. _arXiv preprint arXiv:2310.08560_ . 

- Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. 2023. Generative agents: Interactive simulacra of human behavior. In _Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology_ . 

- Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. 2025. FAST: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ . 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. 2025. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ . 

- Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, et al. 2025. Hi robot: Open-ended instruction following with hierarchical vision-language-action models. _arXiv preprint arXiv:2502.19417_ . 

- Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion: Language agents with verbal reinforcement learning. In _Advances in Neural Information Processing Systems_ . 

- Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, Danfei Xu, Jonathan Tremblay, Dieter Fox, Jesse Thomason, and Animesh Garg. 2022. ProgPrompt: Generating situated robot task plans using large language models. _arXiv preprint arXiv:2209.11302_ . 

- Yang Sui, Yu-Neng Chuang, Guanchu Wang, Jiamu Zhang, Tianyi Zhang, Jiayi Yuan, Hongyi Liu, Andrew Wen, Shaochen Zhong, Na Zou, et al. 2025. 

10 

Stop overthinking: A survey on efficient reasoning for large language models. _arXiv preprint arXiv:2503.16419_ . 

- Xiaoquan Sun, Zetian Xu, Chen Cao, Zonghe Liu, Yihan Sun, Jingrui Pang, Ruijian Zhang, Zhen Yang, Kang Pang, Dingxin He, et al. 2026. AtomVLA: Scalable post-training for robotic manipulation via predictive latent world models. _arXiv preprint arXiv:2603.08519_ . 

- Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Krähenbühl. 2025. Interactive post-training for vision-language-action models. _arXiv preprint arXiv:2505.17016_ . 

- Brian Y Tsui, Alan Y Fang, and Tiffany J Hwu. 2026. Demonstration-free robotic control via llm agents. _arXiv preprint arXiv:2601.20334_ . 

- Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. 2023. Voyager: An open-ended embodied agent with large language models. _arXiv preprint arXiv:2305.16291_ . 

- Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, and Graham Neubig. 2024. Agent workflow memory. _arXiv preprint arXiv:2409.07429_ . 

- John Woods and Hasti Seifi. 2026. SkillComposer: Learning reusable skills for natural-language robot programming. _arXiv preprint arXiv:2608.14944_ . 

- Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. 2024. Unleashing large-scale video generative pre-training for visual robot manipulation. In _International Conference on Learning Representations (ICLR)_ . 

- Bingxin Xu, Yuzhang Shang, Zhen Dong, and Emilio Ferrara. 2026a. Coding agents with harness for safe robot control. _arXiv preprint arXiv:2609.20822_ . 

- Bingxin Xu, Yuzhang Shang, and Emilio Ferrara. 2026b. Don’t drop the BATON: Long-horizon robot manipulation via agentic subtask exploration and transitionaware memory. _arXiv preprint arXiv:2608.16889_ . 

   - Qizheng Zhang, Michael Wornow, and Kunle Olukotun. 2026a. Agentic plan caching: Test-time memory for fast and cost-efficient LLM agents. In _Advances in Neural Information Processing Systems_ . 

   - Wenbo Zhang, Kaixuan Wang, Yutao Ouyang, Xiaoyu Huang, Liyang Li, Kailun Su, Weiyang Jin, Wenhao Chai, Haotian Liang, et al. 2026b. An unexpected robot policy: Early evaluations of GPT-6 Astra on RoboDojo and beyond. _arXiv preprint arXiv:2609.24170_ . 

   - Yixian Zhang, Huanming Zhang, Feng Gao, Xiao Li, Zhihao Liu, Chunyang Zhu, Jiaxing Qiu, Yuchen Yan, Jiyuan Liu, Wenhao Tang, et al. 2026c. Harness VLA: Steering frozen VLAs into reliable manipulation primitives via memory-guided agents. _arXiv preprint arXiv:2607.08448_ . 

   - Zeyu Zhang, Quanyu Dai, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, , Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. 2025. A survey on the memory mechanism of large language model based agents. _ACM Transactions on Information Systems_ . 

   - Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu Lin, Yong-Jin Liu, and Gao Huang. 2024. ExpeL: LLM agents are experiential learners. In _Proceedings of the AAAI Conference on Artificial Intelligence_ . 

   - Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. 2023. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ . 

   - Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, et al. 2026. X-VLA: Softprompted transformer as scalable cross-embodiment vision-language-action model. In _International Conference on Learning Representations_ . 

   - Xueyang Zhou, Yangming Xu, Guiyao Tie, Yongchao Chen, Guowen Zhang, Duanfeng Chu, Pan Zhou, and Lichao Sun. 2025. LIBERO-PRO: Towards robust and fair evaluation of vision-language-action models beyond memorization. _arXiv preprint arXiv:2510.03827_ . 

- Yanting Yang, Can Jin, Jinman Zhao, Jiahao Wu, Yang Zhou, Zhepeng Wang, Zhendong Wang, Mu Zhou, and Dimitris N. Metaxas. 2026. Act more, decide less: Skill-guided adaptive action chunking for long-horizon LLM agents. _arXiv preprint arXiv:2609.02042_ . 

- Chao Yu, Yuanqing Wang, Zhen Guo, Hao Lin, Si Xu, Hongzhi Zang, Quanlu Zhang, Yongji Wu, Chunyang Zhu, Junhao Hu, et al. 2026. RLinf: Flexible and efficient large-scale reinforcement learning via macroto-micro flow transformation. In _20th USENIX Symposium on Operating Systems Design and Implementation (OSDI 26)_ . 

11 

Table 4: **The complete taxonomy of typed exits.** Each exit names the reason a chunk stopped and the reaction expected from the planner. 

|**Group**|**Exit**|**Meaning and expected planner reaction**|
|---|---|---|
|Success|terminated<br>placed_subgoal<br>done_covered|The environment reported success inside the chunk; the finish is recorded<br>and the planner session interrupted.<br>A non-final sub-goal was placed and verified; the chunk continues with the<br>next sub-goal (internal).<br>Every covered sub-goal was executed but the task did not terminate;<br>re-perceive and continue.|
|Hand-off|need_pixels<br>need_receptacle_pixels<br>receptacle_rejected<br>wrong_object_under_gripper<br>subgoal_unverified|The next object was not found by name, or the pixels back-projected off<br>the workspace; callapproachwith pixels on it.<br>The target region cannot be derived (push or beside, or the receptacle point<br>is implausibly high); pass_receptacle_pixels_.<br>The receptacle was not found by name, lies at an implausible height, or the<br>fixture geometry was not located; pass_receptacle_pixels_or use primitives.<br>The wrist camera sees the nearest object more than 5 cm from the pointed<br>spot; confirm or re-point.<br>The object was released but perception could not confirm the predicate;<br>check the image, then redo or continue.|
|Manipulation|grasp_failed<br>lost_at_lift<br>lost_in_carry<br>lost_in_descent<br>carry_stalled<br>delivered_unverified<br>placed_not_terminated|Up to four grasp attempts, nothing held.<br>The object slipped during the lift, twice.<br>The object slipped during the carry, leveling, pitched reach, or hover<br>re-centering.<br>The object left the gripper while lowering.<br>The arm stopped short of the point above the receptacle (reach limit).<br>The VLA carried the object away and released it; the gripper is clear.<br>The object was carried and released at the receptacle, but the task did not<br>terminate.|
|Fixture|open_unverified<br>not_terminated|The drawer handle did not move after the contact skill.<br>The close, turn-on, or door-sweep skill ran but the task did not terminate.|
|Scope|not_covered<br>error|The sub-goal or placement is not covered by any chunk; continue with<br>primitives.<br>Internal error, for instance no pixel can be back-projects; continue with<br>primitives.|


## **A Typed Exit Taxonomy** 

Table 4 lists all exit codes that a chunk may return upon failure, with its meaning and expected planner reaction. 

## **B Primitive Library** 

Table 5 lists all the primitives that constitute the library _P_ introduced in Section 3.1, which are employed in all experiments of Section 4. **ChunkAct** retains this library without modification and adds one call, shown in the last row. 

Table 5: **The primitive library** _P_ **.** Primitives of Harness VLA (Zhang et al., 2026c). The last row lists the single call that **ChunkAct** adds to this library. 

|**Type**|**Primitives**|
|---|---|
|Perception|view_env_state,segment,back_project,<br>view_camera_meta. Return the current images<br>and robot state, segment by text or point prompt,<br>and back-project pixels to 3D points.|
|Motion|move_to,move_pose,set_gripper,release,<br>rotate_pitch,rotate_wrist. These<br>primitives are executed in closed loop by an<br>analytic controller until the target pose or<br>gripper state is reached.|
|VLA|pi0_pick,pi0_doubled. Drive the frozen_π_0_._5<br>policy under a language command until a lift or<br>stop condition is met.|
|Memory|read_text_file,list_dir,<br>write_text_file. Read memory cards and<br>guides from_M_and write audit notes.|
|Control|finish. Declares the task complete.|
|**ChunkAct**|approach, which runs an action chunk.|


12 

