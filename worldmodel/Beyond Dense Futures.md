---
title: "Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation"
date: "2026-03-13"
authors: "Minghao Jin; Mozheng Liao; Mingfei Han; Zhihui Li; Xiaojun Chang"
url: https://arxiv.org/abs/2603.12553
pdf: https://arxiv.org/pdf/2603.12553
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.12553)** / [論文ページ](https://arxiv.org/abs/2603.12553)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Beyond Dense Futures: World Models as Structured Planners for Robotic Manipulation** 

Minghao Jin<sup>1</sup><sup>_∗_</sup> , Mozheng Liao<sup>1</sup><sup>_∗_</sup> , Mingfei Han<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> , Zhihui Li<sup>1</sup> , Xiaojun Chang<sup>1</sup><sup>_,_2</sup> 

> 1 University of Science and Technology of China 

> 2 Department of CV, MBZUAI 

```
https://wm-planner.github.io/structvla/
```

**Abstract.** Recent world-model-based Vision-Language-Action (VLA) architectures have improved robotic manipulation through predictive visual foresight. However, dense future prediction introduces visual redundancy and accumulates errors, causing long-horizon plan drift. Meanwhile, recent sparse methods typically represent visual foresight using high-level semantic subtasks or implicit latent states. These representations often lack explicit kinematic grounding, weakening the alignment between planning and low-level execution. To address this, we propose StructVLA, which reformulates a generative world model into an explicit structured planner for reliable control. Instead of dense rollouts or semantic goals, StructVLA predicts sparse, physically meaningful structured frames. Derived from intrinsic kinematic cues ( _e.g_ ., gripper transitions and kinematic turning points), these frames capture spatiotemporal milestones closely aligned with task progress. We implement this approach through a two-stage training paradigm with a unified discrete token vocabulary: the world model is first trained to predict structured frames and subsequently optimized to map the structured foresight into low-level actions. This approach provides clear physical guidance and bridges visual planning and motion control. In our experiments, StructVLA achieves strong average success rates of 75.0% on SimplerEnv-WidowX and 94.8% on LIBERO. Real-world deployments further demonstrate reliable task completion and robust generalization across both basic pick-and-place and complex long-horizon tasks. 

**Keywords:** Vision language action model · World model · Robotic manipulation 

## **1 Introduction** 

Robotic manipulation typically requires coupling coherent task planning with reliable physical control. Vision-Language-Action (VLA) models [2–4,6,8,14,16, 17,19,32–34,39,43,46,48] address this challenge by grounding natural language instructions in visual observations to directly output low-level actions. Recently, 

> * Equal contribution. 

2 M. Jin et al. 


**Fig. 1: Illustration of StructVLA (Structured Planner for Vision-LanguageAction).** Existing generative VLA methods either predict dense future observations _(bottom left)_ , which accumulate errors and cause long-horizon plan drift, or rely on semantic or latent planning _(bottom right)_ that lacks explicit geometric grounding and leads to physical misalignment. Our StructVLA _(top)_ learns a physically grounded structured planner by training a world model to predict sparse structured frames, and transfers this representation to action control. This design enables stable long-horizon manipulation and demonstrates strong generalization and robustness across simulation and real-world benchmarks. 

the integration of generative world models into VLA architectures [9,36,39] has emerged as a powerful paradigm for long-horizon manipulation. By internalizing environmental dynamics, these generative architectures provide predictive visual foresight, offering spatiotemporal context that enables the policy to anticipate future states beyond instantaneous perception. 

Despite these advantages, effectively representing this visual foresight remains a fundamental challenge. Many approaches represent foresight as dense or step-wise future predictions (pixel or latent) [5,16,33,39,43], which can amplify long-horizon errors when used as direct guidance. Moreover, dense representations contain massive visual redundancy, often obscuring essential task events within high-frequency, task-irrelevant noise. In addition, generating continuous temporal rollouts tend to accumulate prediction errors. Over extended horizons, local visual artifacts or physical inconsistencies compound and can result in plan drift. 

To mitigate the visual redundancy and error accumulation from dense rollouts, recent methods have explored sparse visual foresight [14,25,44]. While these paradigms effectively compress the prediction horizon, existing sparse frameworks also introduce structural limitations. Some approaches define subgoals in semantic space, where high-level abstractions may not specify the precise geometric grounding required for manipulation. Other approaches rely on implicit latent representations [41,43]; while these methods facilitate policy learning, they lack explicit, verifiable geometric targets for closed-loop control. Without clear 

World Models as Structured Planners for Robotic Manipulation 

3 

physical grounding, both representations struggle to provide actionable guidance for low-level kinematic execution, motivating a planning representation that is both physically grounded and control-effective. 

To address these fundamental limitations, we propose **StructVLA** , a framework that reformulates the generative world model into an explicit, physically grounded structured planner. StructVLA predicts sparse structured frames as mid-level visual subgoals that mark essential manipulation milestones. Rather than using semantic subtask boundaries to define subgoals, we derive these frames from intrinsic kinematic cues, such as gripper state transitions and kinematic turning points. Gripper transitions capture contact-state changes, while kinematic turning points reflect meaningful shifts in motion; together they provide progress anchors that are mechanically meaningful across tasks. As a result, the generated visual foresight provides actionable spatiotemporal cues and is tightly coupled to executable interaction phases. 

As illustrated in Fig. 2, StructVLA employs a two-stage training paradigm. In the first stage, the model autoregressively predicts explicit, discrete structured frames, which serve as explicit geometric targets and help reduce long-horizon drift. In the second stage, the model is optimized to generate low-level action tokens, leveraging the structured-planning capability learned in Stage 1. By representing vision, language, and action in a shared discrete vocabulary, StructVLA strengthens the coupling between visual planning and motion control. 

Our main contributions are summarized as follows: 

- **Physics-grounded structured planning targets.** We introduce an automated data curation pipeline that extracts structured frames from robotcentric kinematic cues, providing sparse, mechanically meaningful anchors without semantic subtask labeling. 

- **Unified StructVLA framework.** We present StructVLA, a unified framework that reformulates a world model into an explicit structured planner for control. It is trained in two stages: first autoregressively predicting structured frames as mid-level visual subgoals, then generating low-level action tokens by leveraging the structured-planning capability learned in the first stage, within a shared discrete token space. 

- **Strong empirical results.** StructVLA achieves average success rates of 75.0% on SimplerEnv-WidowX [20] and 94.8% on LIBERO [23], and demonstrates reliable task completion and robust generalization in real-world evaluations on both basic pick-and-place and complex long-horizon tasks. 

## **2 Related Work** 

**Vision-Language-Action Models.** Recent vision-language-action (VLA) models [2–4,6,8,14,16,17,19,32–34,39,43,46,48] have demonstrated strong performance for robotic manipulation. A common line of work builds on large visionlanguage models (VLMs) and learns to map multimodal representations to robot actions. For instance, OpenVLA [17] directly predicts action tokens from VLM, while _π_ 0 [2] and CogACT [19] augment the backbone with a flow-matching or 

4 M. Jin et al. 

diffusion-based action expert to improve continuous control. Villa-X [6] further introduces an intermediate latent-action expert before generating final actions. Recent extensions also incorporate 3D cues to strengthen spatial grounding, such as SpatialVLA [32] and GeoVLA [34]. Another line of work explores generative action modeling and video-diffusion-based control. Diffusion Policy [7] formulates action generation directly as a diffusion process, while VPP [13] exploits representations from video diffusion models for control. VIDAR [8] integrates action reasoning into a video diffusion model, and VideoVLA [33] further studies generalization in video-diffusion-based VLA frameworks. FlowVLA [46] uses optical flow as a motion-foresight cue for action prediction. DreamVLA [43] uses world-model forecasting to guide long-horizon action generation. In contrast, our planner predicts kinematically grounded structured frames as explicit progress anchors, making foresight directly actionable for long-horizon manipulation. 

**Generative models for robotic manipulation.** Many studies have applied world models [10,11,18,42] to robotic manipulation across both simulation and real-robot settings. DayDreamer [40] introduces the Dreamer algorithm into real-world robot learning, improving sample efficiency. CASCADE [42] expands world-model training coverage via collaborative exploration to improve generalization. SWIM [26] trains world models on human demonstration videos and uses them to guide manipulation. UWM [47] further unifies video diffusion and action diffusion for joint modeling of dynamics and policy learning. UniVLA [39] unifies vision, language, and action as an autoregressive discrete sequence and incorporates world-model post-training to capture temporal and causal structure for downstream policy learning. For joint forecasting, VideoVLA [33] employs a multimodal DiT [30] to jointly forecast an action sequence and future visual outcomes. Large Video Planner [5] leverages foundation-scale video pretraining to generate dense video plans, which are then post-processed into executable robot actions. Similarly, Cosmos Policy [16] adapts a pretrained video diffusion model via latent frame injection, and can optionally perform value-guided best-of- _N_ planning to evaluate candidate action trajectories, incurring higher test-time sampling cost. In contrast, we explore world models as explicit sparse structured planners, producing physically grounded progress anchors that are directly actionable for closed-loop control. 

**Task planning in robot learning.** Task planning is crucial for long-horizon manipulation. Many studies have explored decomposing language instructions into sub-tasks, such as utilizing code-generation models [21] to translate natural language into executable policies. Text2Motion [22] converts both long and short natural language instructions into symbolic task goals and feasible action sequences, while ThinkAct [15] leverages VLM reasoning for trajectorylevel planning. Complementary to language-centric planning, other approaches derive planning signals from visual dynamics. Track2Act [1] predicts pixel-level trajectories from internet videos to assist manipulation, and LDP [41] models latent actions between adjacent frames for trajectory planning. UniVLA (Bu et al.) [4] extracts task-centric latent actions from unannotated videos to enable cross-embodiment policy learning. More recently, generative foresight has been 

World Models as Structured Planners for Robotic Manipulation 

5 


**Fig. 2: Overview of StructVLA.** StructVLA is trained in two stages. **Stage 1 (Structured Planner):** an autoregressive world model predicts sparse structured frames that capture physically grounded progress anchors, conditioned on the instruction and visual context. **Stage 2 (Action Policy):** we fine-tune the structured planner for control by conditioning on the instruction together with interleaved observation and actions, transferring structured planning into low-level control. 

used to instantiate planners in different forms. ForeAct [44] and VISTA [25] employ generative models as high-level planners that provide subgoal guidance to separate low-level VLAs, while BagelVLA [14] and mimic-video [29] incorporate planning signals through implicit latent foresight. In particular, BagelVLA [14] and ForeAct [44] adopt subtask-anchored foresight, where subgoals are specified or sampled within semantic subtask segments. In contrast, StructVLA derives structured subgoals from kinematic interaction cues and reformulates the world model as a kinematically grounded planner, providing control-effective visual anchors for action generation. 

## **3 Method** 

Fig. 2 summarizes the overall design of StructVLA. We reformulate a single generative world model as a structured planner by introducing sparse structured frames as physically grounded visual subgoals. Sec. 3.1 describes an automated data curation pipeline for extracting these structured frames. We train StructVLA with a two-stage paradigm: Sec. 3.2 details Stage 1 for structured frame prediction, and Sec. 3.3 presents Stage 2 for transferring the structured foresight to action policy learning. 

### **3.1 Physics-Grounded Data Curation** 

At the core of our structured planner are structured frames, which serve as physically grounded visual subgoals. During offline data curation, an automated pipeline extracts these frames from raw robotic trajectories to exclusively supervise the generative world model. Instead of representing foresight as dense continuous rollouts, structured frames provide compact progress anchors that connect task intent to executable motion phases. By deriving them from robot-centric kinematic cues, our curation produces subgoals that are consistently aligned with interaction transitions in manipulation. 

6 M. Jin et al. 

Formally, consider a robotic manipulation trajectory _T_ = � _l, {_ ( _ot, at_ ) _}_<sup>_T_</sup> _t_ =0�, where _l_ denotes the language instruction, _ot_ is the visual observation, and _at_ represents the executed action at timestep _t_ . Within a trajectory, the most intuitive anchors are explicit milestones ( _e.g_ ., object grasped or placed), which define clear subtask boundaries. However, relying only on these sparse events omits critical task-progression details. In practice, many informative intermediate states are implicitly reflected in the motion trajectory, such as the kinematic turning point where the gripper aligns above a target before shifting direction to descend. To capture such physically meaningful states without manual annotation, we introduce an automated extraction procedure based on kinematic cues. Our offline pipeline first proposes candidate frames from robot-centric kinematic cues, and then applies filtering to remove redundancy and refine the candidates. **Kinematic Structured Frame Extraction.** To ensure robustness across diverse manipulation speeds and tasks, we compute adaptive kinematic thresholds for each episode from the distribution of end-effector motion magnitudes _∥vt∥_ , which is derived from the actions _at_ . Combined with Exponential Moving Average (EMA) smoothing to filter out high-frequency control noise, we extract structured frames using two primary kinematic cues: 

_Gripper State Transitions:_ We extract structured frames around gripper state changes (open or close), which often mark contact state transitions. Since raw gripper signals can be noisy and the physical actuation may lag behind the signal flip in practice, we apply a stabilization window _δ_ settle after each flip time _tc_ . We then select the last quasi static observation _ot∗_ immediately before the robot resumes a major motion, identified when the smoothed speed exceeds an adaptive threshold _τ_ high. Formally, for each flip time _tc_ , we define 


_Kinematic Turning Points:_ Even with a fixed gripper state, manipulation often involves brief slowdowns during motion regime transitions. For example, the endeffector may complete lateral alignment above the target and stabilize before initiating the downward approach. We identify such moments by applying a sliding window of length _W_ and selecting frames whose smoothed speed remains below an adaptive threshold _τ_ low throughout the window ending at timestep _t_ : 


_Temporal Coverage:_ To avoid extracting redundant frames from a prolonged lowspeed segment, we enforce a minimum temporal gap between selected frames. For unusually long segments where distinct kinematic events are sparse, we apply a gap filling step to ensure adequate subgoal coverage. Specifically, we sample additional observations _S_ fill by selecting frames with the smallest _L_ 2 change in consecutive action commands, _∆at_ = _∥at − at−_ 1 _∥_ 2, which serves as a proxy for low-motion, stable states within the segment. The union of these sets forms our initial candidate structured frame set _S_ = _S_ grip _∪ S_ turn _∪ S_ fill. 

World Models as Structured Planners for Robotic Manipulation 

7 

**Offline Trajectory Filtering.** While kinematic cues reliably detect interaction transitions, they provide limited task-level context and may occasionally propose false positives under hardware perturbations. To refine the final structured frames, we use a VLM, _i.e_ ., GPT-5.2 [27], strictly for offline refinement. Specifically, we provide the global instruction _l_ together with the candidate observations _S_ , and use a fixed prompt (detailed in the Appendix) with filtering rules to remove visually redundant or task-irrelevant frames. This verification refines the preliminary structured frames obtained from kinematic cues, so that the final sequence better reflects coherent and executable milestones. Crucially, the filtering is applied only offline during dataset construction. We train StructVLA solely on the curated data. During inference, we deploy the action policy with no additional curation or VLM assistance. 

### **3.2 Structured Planner (Stage 1: Visual Foresight)** 

To achieve this structured planning, we train the generative world model to predict the physically grounded structured frames _s ∈S_ identified during data curation. Formally, given a language instruction _l_ and a visual context window _Ot_ = _{ot−H_ +1 _, . . . , ot}_ , the model learns the conditional distribution _Pθ_ ( _s | l, Ot_ ) of a future structured frame _s_ . 

We employ the Emu3 [38] tokenizer with Vector Quantization (VQ) to discretize the language instructions and image frames into a shared vocabulary. Specifically, the language instruction _l_ is tokenized into _Tl_ , while the visual context window _Ot_ is transformed into a sequence of tokens _TOt_ = _{Tot−H_ +1 _, . . . , Tot}_ , where each _Toi_ represents the discretized features of observation _oi_ . Similarly, the target structured frame _s_ is represented by a discrete token sequence _Ts_ = _{z_ 1 _, z_ 2 _, . . . , zK}_ . 

Following the standard autoregressive generation paradigm, the model is trained to minimize the cross-entropy loss over the predicted visual tokens _Ts_ , conditioned on the tokenized instruction and historical observations: 


Through sequential token prediction, the model learns to forecast kinematically grounded structured frames, capturing key transitions in manipulation and developing an implicit awareness of task progress in its visual foresight. This provides stable visual guidance for subsequent action control. 

### **3.3 Action Policy (Stage 2: Plan-to-Act Transfer)** 

In Stage 2, the pretrained structured planner is directly formulated as an executable action policy by shifting the optimization objective to predicting action tokens. We discretize continuous actions into discrete tokens using the FAST tokenizer [31]. Crucially, these action tokens are integrated into a unified vocabulary shared with the visual and language modalities, enabling the model to directly output control signals through standard autoregressive generation. 

8 M. Jin et al. 

#### **Table 1: Results on SimplerEnv [20].** 

Each model is evaluated for task success rate across four manipulation tasks. StructVLA yields the strongest average performance. 

**Table 2: Results on LIBERO [23].** 

Comparison of task success rates across four suites. StructVLA outperforms prior baselines, especially on the LIBERO-Long suite. * denotes reproduced results. 

|**Model**|Spoon|Carrot|Stack|Eggplant|**Avg.**|**Method**|SPATIAL|OBJECT|GOAL|LONG **Avg.**|
|---|---|---|---|---|---|---|---|---|---|---|
|RT-1-X [28]|0.0%|4.2%|0.0%|0.0%|1.1%|DP [7]|78.3%|92.5%|68.3%|50.5% 72.4%|
|Octo-Base [35]|12.5%|31.9%|0.0%|43.1%|16.0%|Octo [35]|78.9%|85.7%|84.6%|51.1% 75.1%|
|Octo-Small [35]|47.2%|9.7%|4.2%|56.9%|29.5%|OpenVLA [17]|84.9%|88.4%|79.2%|53.7% 76.5%|
|OpenVLA [17]|0.0%|0.0%|0.0%|4.1%|1.0%|SpatialVLA [32]|88.2%|89.9%|78.6%|55.5% 78.1%|
|RoboVLMs [24]|45.8%|20.8%|4.2%|79.2%|37.5%|CoT-VLA [45]|87.5%|91.6%|87.6%|69.0% 81.1%|
|SpatialVLA [32]|16.7%|25.0%|29.2%|**100%**|42.7%|_π_0-FAST [31]|96.4%|96.8%|88.6%|60.2% 85.5%|
|VideoVLA [33]|75.0%|20.8%|**45.8%**|70.8%|53.1%|FlowVLA [46]|93.2%|95.0%|91.6%|72.6% 88.1%|
|mimic-video [29]|41.7%|54.2%|29.2%|**100%**|56.3%|DreamVLA [43]|**97.5%**|94.0%|89.5%|89.5% 92.6%|
|UniVLA [39]|83.3%|66.7%|33.3%|95.8%|69.8%|UniVLA* [39]|96.4%|**98.0%**|90.8%|89.6% 93.7%|
|**StructVLA (Our**|**s) 87.5% **|**75.0% **|**45.8%**|91.7%|**75.0%**|**StructVLA (Ours)**|95.4%|**98.0%**|**93.4% **|**92.2% 94.8%**|


During training, the conditioning context is explicitly constructed by concatenating the tokenized global language instruction _Tl_ with interleaved visual and action tokens. Specifically, for a given timestep _t_ and a context window of length _H_ , this multimodal history sequence is defined as _Ht_ = _{Tot−H_ +1 _, Tat−H_ +1 _, . . . , Tot}_ , where _Toi_ and _Tai_ represent the discretized tokens of the observation and action at timestep _i_ , respectively. Given this explicitly interleaved sequence, the model is optimized to autoregressively predict the sequence of discretized action tokens _Tat_ = _{a_ 1 _, a_ 2 _, . . . , aM }_ required to execute the current subtask. 

Following the standard next-token prediction paradigm, we restrict the supervision signal strictly to the action domain. The cross-entropy loss is computed exclusively over these sequentially generated action tokens: 


By dynamically shifting the prediction target within a unified vocabulary, this formulation allows the generative structured planner to directly translate its internalized visual foresight into reliable, low-level action control. 

## **4 Experiments** 

In this section, we comprehensively evaluate StructVLA across simulation benchmarks and real-world deployments. Sec. 4.1 introduces the simulation and realworld deployment settings, together with the curated datasets used for training. Sec. 4.2 details the model architecture and training configurations. Sec. 4.3 presents comparative results against representative baselines. Finally, Sec. 4.4 presents in-depth analyses and extended studies of the overall VLA pipeline. 

### **4.1 Experimental Setup** 

**SimplerEnv benchmark.** SimplerEnv [20] evaluates transfer and generalization of policies trained on real-world robot trajectories under controlled distribu- 

World Models as Structured Planners for Robotic Manipulation 

9 


**Fig. 3: Qualitative comparison of visual predictions.** Our structured planner generates coherent, long-horizon visual foresight, supporting robust planning, whereas the baseline world model struggles with long-range comprehension, producing short-horizon predictions with degraded image quality. Red boxes highlight key differences. 

**Fig. 4: More visualizations** (a) **Attention maps:** The planner (left) localizes task-critical interactions ( _e.g_ ., gripper–object contact), while the baseline (right) is diffuse. (b) **OOD predictions:** StructVLA retains world-model priors, enabling zero-shot visual planning on unseen scenes and tasks. (c) **Realworld deployment setup.** 

tion shifts ( _e.g_ ., lighting, texture, and camera pose) across WidowX and Google Robot platforms. We mainly report results on WidowX, which is commonly used. We train StructVLA on the standard BridgeData V2 [37] dataset. 

**LIBERO benchmark.** The LIBERO benchmark [23] evaluates multi-task manipulation and long-horizon consistency within a simulated Franka Emika Panda robot arm. There are four task suites including LIBERO-Spatial, LIBEROObject, LIBERO-Goal, and LIBERO-Long (LIBERO-10). Specifically, each suite comprises 10 distinct tasks with 50 expert demonstrations per task, and we jointly train a single model across the combined datasets of all suites. 

**Real-world evaluation.** We deploy StructVLA on a physical Franka arm to evaluate robustness under real-world noise and perturbations. Our setup includes four pick-and-place tasks (yellow bowl, biscuit box, toy, eggplant) and a longhorizon tidy-up task with distractors. We train a multi-task policy for the four tasks using 1,152 trajectories (288 per task) and a dedicated policy for tidyup using 648 trajectories. We compare against UniVLA [39] under identical conditions and evaluate zero-shot generalization to unseen objects (novel colors and geometries) and robustness under human interventions. 

10 M. Jin et al. 

### **4.2 Implementation Details** 

**Model structure.** Our world model adopts a purely autoregressive Transformer architecture with 8.5B parameters, initialized from the world model of UniVLA [39]. Images are tokenized using the Emu3 [38] VQ-based encoder with a spatial compression factor of 8. For action tokenization, we first apply 1st and 99th percentile normalization, and then utilize the FAST [31] tokenizer with a vocabulary size of 1024. We integrate actions by mapping them to the final 1024 token IDs of the language vocabulary. Consequently, vision, language, and action share a single discrete token space, enabling joint representation learning and cross-modal alignment. Visual observation setups vary by evaluation domain: (1) SimplerEnv: A single-view RGB image (256 × 256) is used across both stages; (2) LIBERO: Stage 1 uses a third-person view (200 × 200), supplemented by an additional wrist-view camera (200 × 200) for Stage 2; (3) Real-world: Stage 1 relies on the front-camera view (256 × 144), while Stage 2 incorporates a wrist-view image (240 × 135). 

**Structured planner training.** We train the world model to predict the next structured frame foresight from the instruction and visual context. We initialize the model with pretrained weights of world model from UniVLA [39]. Supervision is applied only to vision tokens, guiding the model to generate physically grounded visual foresight. Because training solely on structured frames is temporally sparse, we apply a sliding-window augmentation that slightly shifts the target timestep and resamples its context, densifying supervision and exposing the model to richer spatiotemporal patterns. The structured planner is trained with a universal batch size of 32 for 30K, 10K, and 2K steps on the SimplerEnv, LIBERO, and real-world setups, respectively. 

**Action policy training.** We fine-tune the planner to shift from visual foresight prediction to action prediction. The input sequence begins with the language instruction, followed by interleaved visual and action tokens. Supervision is applied solely to action tokens, allowing the model to learn an explicit action policy grounded in visual planning. Subsequently, the action policy is trained across the three domains with varying configurations: 20K steps (batch size 128) for SimplerEnv, 4K steps (batch size 196) for LIBERO, and 2K steps (batch size 32) for real-world deployments. 

**Efficient adaptation.** To specialize the pre-trained world model for generating task-semantic structured frames without costly full-model retraining, we employ LoRA [12] (rank=32) for parameter-efficient fine-tuning. This approach preserves the model’s foundational visual prediction capabilities while achieving high-quality foresight at a fraction of the computational cost, validating it as a highly effective adaptation strategy. 

### **4.3 Main Results** 

**SimplerEnv benchmark** As shown in Tab. 1, our StructVLA achieves an average success rate of 75.0% on the SimplerEnv-WidowX benchmark, outperforming all prior baselines. Beyond the overall score, StructVLA achieves consistently 

World Models as Structured Planners for Robotic Manipulation 

11 

strong performance across tasks. In particular, on the challenging _Stack Green on Yellow Block_ task, which requires sustained progress tracking and precise spatial execution, StructVLA matches VideoVLA and clearly outperforms the other baselines. We attribute these gains to structured frame foresight, which provides sparse, kinematically grounded progress anchors and helps stabilize closed-loop control over longer horizons. 

**LIBERO benchmark** As shown in Tab. 2, our StructVLA achieves 94.8% average success on LIBERO and shows strong performance overall, especially on LIBERO-Object, LIBERO-Goal, and LIBERO-Long. In particular, on the challenging LIBERO-Long suite, StructVLA performs notably better than prior methods, suggesting more reliable execution over extended horizons. We attribute this to the structured planner, which predicts structured frames at key interaction transitions and provides sparse mid-level visual subgoals for control. These subgoals act as progress anchors that guide the policy, reduce drift from accumulated errors, and improve consistency in multi-stage manipulation. 

**Real-world depolyments.** As shown in Fig. 5, StructVLA outperforms the baselines in real-world deployments. On the four pick-and-place tasks, StructVLA achieves an 87.5% average success rate, which is 20.0% higher than UniVLA, and reaches 10/10 on the eggplant task. On the long-horizon _tidy-up_ task, StructVLA completes 8/10 trials, compared with 4/10 for UniVLA and 2/10 for SpatialVLA, indicating stronger stability over extended execution. These results suggest that incorporating structured planning improves real-world robustness, especially for long-horizon execution where small deviations and environmental noise can otherwise compound over time. 

**Real-world generalization and robustness.** Beyond standard instruction following, we evaluate zero-shot generalization and robustness under dynamic perturbations (Fig. 7). On out-of-distribution pick-and-place with unseen colors ( _e.g_ ., a pink bowl) and novel geometries ( _e.g_ ., a blue cup), StructVLA achieves 80.0% success, compared to 30.0% for UniVLA. On the long-horizon tidy-up task, StructVLA generalizes to unseen objects and maintains 70.0% success. Under human interventions such as adding objects during execution, StructVLA retains 80.0% success versus 40.0% for UniVLA. We attribute these gains to structured planning with kinematically grounded milestones, which provides stable progress anchors and helps the policy remain consistent under appearance shifts and dynamic disturbances. 

### **4.4 Extended Analysis** 

Beyond the main performance results, this section provides a deeper analysis of StructVLA’s core properties through a series of empirical investigations and ablation studies. Specifically, we first evaluate the performance and mechanistic insights of the proposed structured planner. We then examine the training efficiency of our approach and investigate the correlation between grasp quality and overall task success. Finally, we analyze the role of historical context in ensuring accurate predictions, and present an extended comparative evaluation of real-world deployments. 

M. Jin et al. 

12 


**Fig. 5: Quantitative Results on Real-World Deployments.** Success rates on diverse physical manipulation tasks (10 trials per task). **StructVLA** matches or exceeds prior baselines on the foundation tasks and remains strong on the challenging longhorizon tidy-up task. 


**Fig. 6: Grasp Success vs. Task Success.** We analyze how grasp success translates to task completion. **StructVLA** attains the highest mean grasp success and a higher grasp-to-task conversion rate than the baseline UniVLA, indicating improved long-horizon stability with reduced drift and error accumulation. 

**Fig. 7: Real-World Generalization and Robustness.** Success rates for zero-shot generalization (novel object geometries) and dynamic human interventions. **StructVLA** outperforms the baseline in all settings. 

**Structured planner performance.** As shown in Fig. 3, our structured planner predicts the next structured frame from the current observation and instruction, maintaining coherent task progress over multi-step rollouts with less drift than a conventional world model. Even from a single observation, it rolls out a five-step sequence that stays consistent with the intended manipulation trajectory. In contrast, the baseline world model either produces near-static futures with weak progress cues or introduces distortions under larger state changes. These results suggest that training on structured frames yields more stable and informative foresight for long-horizon execution, providing intermediate visual targets that the downstream policy can follow more reliably. 

**Mechanistic insights of Structured planner.** We visualize attention maps from the final self-attention layer in Fig. 4(a) for both the structured planner and the baseline world model. During kinematic transitions, the planner places higher attention on motion related regions, most notably around the gripper, whereas the baseline exhibits a more diffuse distribution without a clear interaction focus. 

World Models as Structured Planners for Robotic Manipulation 

13 


**Fig. 8: Qualitative comparison of real-world deployments. (a) StructVLA (Ours):** Robust long-horizon execution with zero-shot generalization to OOD objects ( _e.g_ ., pink bowl, Coke can). **(b) UniVLA (Baseline):** Prone to error accumulation and grasp failures, consistent with dense-prediction drift and limited generalization. 

Fig. 4(b) evaluates the planner on out-of-distribution scenes and tasks excluded from Stage 1 training. The predictions remain visually coherent, suggesting that structured-frame finetuning preserves useful pretrained priors and generalizes to novel environments. 

**Training efficiency of StructVLA.** As shown in Tab. 3, StructVLA exhibits strong sample efficiency, reaching high success rates with substantially fewer training steps than prior methods under the same batch size. We attribute this to StructVLA’s structured planning, which encourages representations that capture task progress and reduces the policy’s effective search space, improving learning efficiency. This reduces the learning burden on the action policy and enables faster improvement with less training data. 

**Analysis of Grasp Quality vs. Task Success.** Beyond overall task success, Fig. 6 examines how grasp success translates into task completion. StructVLA achieves the highest mean grasp success (89.6%), although on _Put Eggplant_ it is slightly below two baselines (91.7% vs. 100%). More importantly, StructVLA attains a higher grasp-to-task conversion rate than the baseline UniVLA, indicating more consistent post-grasp execution. For instance, on _Stack Green on Yellow Block_ , StructVLA matches UniVLA in grasp success (95.8%) but achieves higher task success (45.8% vs. 33.3%), suggesting that structured planning improves multi-step, long-horizon execution beyond grasping alone and may reduce plan drift and error accumulation. 

**History context for accurate prediction.** On SimplerEnv, we evaluate history windows of 2, 3, and 4 in Tab. 4 and compare StructVLA with UniVLA under identical computation budgets. StructVLA improves as the history window increases, rising from 70.8% to 75.0%, whereas UniVLA drops from 69.8% to 66.7%. This ablation supports our claim that the structured planner benefits from longer temporal context because it uses the additional observations to forecast the next structured frame and capture long-range task progress, rather than being dominated by short-term visual details. As a result, larger history windows provide useful semantic and spatiotemporal evidence for planning and lead to better performance, instead of introducing distracting noise. 

M. Jin et al. 

14 

**Table 3: Learning Efficiency and Convergence Speed. Learning Efficiency and Convergence Speed.** Comparison of the training steps required for different models to reach peak success. All methods are trained under identical environments and hyperparameters ( _e.g_ ., batch size 128). 

|**Method**|**Batch**|**Steps**|**Accuracy**|
|---|---|---|---|
|RoboVLMs|128|50k|37.5%|
|UniVLA|128|12k|64.8%|
|**StructVLA**|128|**10k**|**66.7%**|


**Table 4: Historical Context Length.** Unlike UniVLA, StructVLA improves with longer context, effectively leveraging extended history for long-horizon reasoning and distant goal prediction. 

|**Method**|**History**|**Accuracy**|
|---|---|---|
||2|70.8%|
|StructVLA|3|71.9% _↑_1_._55%|
||4|**75.0%** _↑_**5**_._**93**%|
||2|**69.8%**|
|UniVLA|3|69.8% _−_0_._0|
||4|66.7% _↓_**4**_._**44**%|


As shown in 

**Comparative Evaluation of Real-World Deployments.** As shown in Fig. 8, StructVLA demonstrates reliable execution on the long-horizon _tidy-up_ task, successfully manipulating four objects and remaining stable under dynamic interventions with unseen objects such as a pink bowl and a coke can. In contrast, UniVLA shows weaker long-horizon stability and can suffer from error accumulation when task progress is not explicitly constrained. In our qualitative examples, UniVLA fails to grasp the towel and later knocks over the biscuit box due to compounding positional errors, and it also struggles to handle the novel pink bowl. Overall, these observations highlight a clear gap in deployment behavior, where StructVLA provides more consistent task completion and stronger zero-shot robust generalization in real-world settings. 

## **5 Conclusion** 

We presented **StructVLA** , a novel Vision-Language-Action framework that reformulates generative world models into explicit, physically grounded structured planners for action control. To achieve robust long-horizon planning and strict physical alignment, StructVLA predicts discrete structured frames grounded in kinematic cues. Through a two-stage training paradigm within a unified token vocabulary, StructVLA bridges the gap between high-level planning signals and low-level action generation. Extensive empirical evaluations demonstrate that StructVLA achieves highly competitive performance, delivering a 75.0% average success rate on the SimplerEnv-WidowX benchmark and 94.8% on LIBERO. Real-world deployments further validate its exceptional cross-category generalization and robustness in executing complex, long-horizon tasks. Ultimately, StructVLA moves beyond dense video generation and semantic planning, providing physically grounded visual foresight for reliable robot control. 

World Models as Structured Planners for Robotic Manipulation 

15 

**Limitations and Discussion.** While our results are promising, the primary limitation of this work is its experimental scale, constrained by computational resources. Future evaluation on larger, multi-domain datasets is thus essential to validate broader generalization. Promising research directions also include exploring advanced training strategies and architectural refinements to enhance model stability, and incorporating online reinforcement learning to improve the policy’s robustness for real-world deployment. 

## **References** 

1. Bharadhwaj, H., Mottaghi, R., Gupta, A., Tulsiani, S.: Track2act: Predicting point tracks from internet videos enables generalizable robot manipulation. In: European Conference on Computer Vision (ECCV) (2024) 

2. Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L.X., Tanner, J., Vuong, Q., Walling, A., Wang, H., Zhilinsky, U.: _π_ 0: A vision-language-action flow model for general robot control (2024), `https://arxiv.org/abs/2410.24164` 

3. Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al.: Rt-1: Robotics transformer for real-world control at scale. arXiv preprint arXiv:2212.06817 (2022) 

4. Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., Li, H.: Univla: Learning to act anywhere with task-centric latent actions. arXiv preprint arXiv:2505.06111 (2025) 

5. Chen, B., Zhang, T., Geng, H., Song, K., Zhang, C., Li, P., Freeman, W.T., Malik, J., Abbeel, P., Tedrake, R., et al.: Large video planner enables generalizable robot control. arXiv preprint arXiv:2512.15840 (2025) 

6. Chen, X., Wei, H., Zhang, P., Zhang, C., Wang, K., Guo, Y., Yang, R., Wang, Y., Xiao, X., Zhao, L., et al.: Villa-x: enhancing latent action modeling in visionlanguage-action models. arXiv preprint arXiv:2507.23682 (2025) 

7. Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., Song, S.: Diffusion policy: Visuomotor policy learning via action diffusion. The International Journal of Robotics Research p. 02783649241273668 (2023) 

8. Feng, Y., Tan, H., Mao, X., Liu, G., Huang, S., Xiang, C., Su, H., Zhu, J.: Generalist bimanual manipulation via foundation video diffusion models. arXiv e-prints pp. arXiv–2507 (2025) 

9. Gao, S., Zhou, S., Du, Y., Zhang, J., Gan, C.: Adaworld: Learning adaptable world models with latent actions. arXiv preprint arXiv:2503.18938 (2025) 

10. Ha, D., Schmidhuber, J.: World models (2018). `https://doi.org/10.5281/ ZENODO.1207631` , `https://zenodo.org/record/1207631` 

11. Hafner, D., Lillicrap, T., Ba, J., Norouzi, M.: Dream to control: Learning behaviors by latent imagination (2020), `https://arxiv.org/abs/1912.01603` 

12. Hu, E.J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W., et al.: Lora: Low-rank adaptation of large language models. ICLR **1** (2), 3 (2022) 

13. Hu, Y., Guo, Y., Wang, P., Chen, X., Wang, Y.J., Zhang, J., Sreenath, K., Lu, C., Chen, J.: Video prediction policy: A generalist robot policy with predictive visual representations. arXiv preprint arXiv:2412.14803 (2024) 

M. Jin et al. 

16 

14. Hu, Y., Zhang, J., Luo, Y., Guo, Y., Chen, X., Sun, X., Feng, K., Lu, Q., Chen, S., Zhang, Y., et al.: Bagelvla: Enhancing long-horizon manipulation via interleaved vision-language-action generation. arXiv preprint arXiv:2602.09849 (2026) 

15. Huang, C.P., Wu, Y.H., Chen, M.H., Wang, Y.C.F., Yang, F.E.: Thinkact: Visionlanguage-action reasoning via reinforced visual latent planning. arXiv preprint arXiv:2507.16815 (2025) 

16. Kim, M.J., Gao, Y., Lin, T.Y., Lin, Y.C., Ge, Y., Lam, G., Liang, P., Song, S., Liu, M.Y., Finn, C., et al.: Cosmos policy: Fine-tuning video models for visuomotor control and planning. arXiv preprint arXiv:2601.16163 (2026) 

17. Kim, M.J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al.: Openvla: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246 (2024) 

18. LeCun, Y.: A path towards autonomous machine intelligence (2022), `https:// openreview.net/pdf?id=BZ5a1r-kVsf` 

19. Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., Wei, F., Deng, Y., Xu, S., Zhang, Y., et al.: Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. arXiv preprint arXiv:2411.19650 (2024) 

20. Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H.R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., et al.: Evaluating real-world robot manipulation policies in simulation. arXiv preprint arXiv:2405.05941 (2024) 

21. Liang, J., Huang, W., Xia, F., Xu, P., Hausman, K., Ichter, B., Florence, P., Zeng, A.: Code as policies: Language model programs for embodied control. In: arXiv preprint arXiv:2209.07753 (2022) 

22. Lin, K., Agia, C., Migimatsu, T., Pavone, M., Bohg, J.: Text2motion: From natural language instructions to feasible plans. Autonomous Robots **47** (8), 1345–1365 (2023) 

23. Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., Stone, P.: Libero: Benchmarking knowledge transfer for lifelong robot learning. Advances in Neural Information Processing Systems **36** , 44776–44791 (2023) 

24. Liu, H., Li, X., Li, P., Liu, M., Wang, D., Liu, J., Kang, B., Ma, X., Kong, T., Zhang, H.: Towards generalist robot policies: What matters in building visionlanguage-action models (2025) 

25. Long, Q., Wang, Y., Song, J., Zhang, J., Li, P., Wang, W., Wang, Y., Li, H., Xie, S., Yao, G., et al.: Scaling world model for hierarchical manipulation policies. arXiv preprint arXiv:2602.10983 (2026) 

26. Mendonca, R., Bahl, S., Pathak, D.: Structured world models from human videos. In: Robotics: Science and Systems (RSS) (2023) 

27. OpenAI: Introducing gpt-5.2. `https://openai.com/index/introducing-gpt-52/` (2025), accessed: 2026-03-06 

28. O’Neill, A., Rehman, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., Pooley, A., Gupta, A., Mandlekar, A., Jain, A., et al.: Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In: 2024 IEEE International Conference on Robotics and Automation (ICRA). pp. 6892–6903. IEEE (2024) 

29. Pai, J., Achenbach, L., Montesinos, V., Forrai, B., Mees, O., Nava, E.: mimic-video: Video-action models for generalizable robot control beyond vlas. arXiv preprint arXiv:2512.15692 (2025) 

30. Peebles, W., Xie, S.: Scalable diffusion models with transformers. In: Proceedings of the IEEE/CVF international conference on computer vision. pp. 4195–4205 (2023) 

World Models as Structured Planners for Robotic Manipulation 

17 

31. Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., Levine, S.: Fast: Efficient action tokenization for vision-language-action models. arXiv preprint arXiv:2501.09747 (2025) 

32. Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al.: Spatialvla: Exploring spatial representations for visual-languageaction model. arXiv preprint arXiv:2501.15830 (2025) 

33. Shen, Y., Wei, F., Du, Z., Liang, Y., Lu, Y., Yang, J., Zheng, N., Guo, B.: Videovla: Video generators can be generalizable robot manipulators. In: The Thirty-ninth Annual Conference on Neural Information Processing Systems 

34. Sun, L., Xie, B., Liu, Y., Shi, H., Wang, T., Cao, J.: Geovla: Empowering 3d representations in vision-language-action models. arXiv preprint arXiv:2508.09071 (2025) 

35. Team, O.M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al.: Octo: An open-source generalist robot policy. arXiv preprint arXiv:2405.12213 (2024) 

36. Tharwat, B., Nasser, Y., Abouzeid, A., Reid, I.: Latent action pretraining through world modeling. arXiv preprint arXiv:2509.18428 (2025) 

37. Walke, H., Black, K., Lee, A., Kim, M.J., Du, M., Zheng, C., Zhao, T., HansenEstruch, P., Vuong, Q., He, A., Myers, V., Fang, K., Finn, C., Levine, S.: Bridgedata v2: A dataset for robot learning at scale. In: Conference on Robot Learning (CoRL) (2023) 

38. Wang, X., Zhang, X., Luo, Z., Sun, Q., Cui, Y., Wang, J., Zhang, F., Wang, Y., Li, Z., Yu, Q., et al.: Emu3: Next-token prediction is all you need. arXiv preprint arXiv:2409.18869 (2024) 

39. Wang, Y., Li, X., Wang, W., Zhang, J., Li, Y., Chen, Y., Wang, X., Zhang, Z.: Unified vision-language-action model (2025), `https://arxiv.org/abs/2506.19850` 

40. Wu, P., Escontrela, A., Hafner, D., Abbeel, P., Goldberg, K.: Daydreamer: World models for physical robot learning. In: Proceedings of The 6th Conference on Robot Learning (CoRL). pp. 2226–2240. PMLR (2023) 

41. Xie, A., Rybkin, O., Sadigh, D., Finn, C.: Latent diffusion planning for imitation learning. arXiv preprint arXiv:2504.16925 (2025) 

42. Xu, Y., Parker-Holder, J., Pacchiano, A., Ball, P.J., Rybkin, O., Roberts, S.J., Rocktäschel, T., Grefenstette, E.: Learning general world models in a handful of reward-free deployments. In: Advances in Neural Information Processing Systems (NeurIPS) 35 (2022) 

43. Zhang, W., Liu, H., Qi, Z., Wang, Y., Yu, X., Zhang, J., Dong, R., He, J., Lu, F., Wang, H., et al.: Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge. arXiv preprint arXiv:2507.04447 (2025) 

44. Zhang, Z., Yang, S., Hu, Q., Huang, L.J., Hou, J., Sun, Y., Lu, Y., Han, S.: Foreact: Steering your vla with efficient visual foresight planning. arXiv preprint arXiv:2602.12322 (2026) 

45. Zhao, Q., Lu, Y., Kim, M.J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al.: Cot-vla: Visual chain-of-thought reasoning for vision-languageaction models. In: Proceedings of the Computer Vision and Pattern Recognition Conference. pp. 1702–1713 (2025) 

46. Zhong, Z., Yan, H., Li, J., Liu, X., Gong, X., Zhang, T., Song, W., Chen, J., Zheng, X., Wang, H., et al.: Flowvla: Visual chain of thought-based motion reasoning for vision-language-action models. arXiv preprint arXiv:2508.18269 (2025) 

47. Zhu, C., Yu, R., Feng, S., Burchfiel, B., Shah, P., Gupta, A.: Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. In: Proceedings of Robotics: Science and Systems (RSS) (2025) 

18 M. Jin et al. 

48. Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al.: Rt-2: Vision-language-action models transfer web knowledge to robotic control. In: Conference on Robot Learning. pp. 2165–2183. PMLR (2023) 

World Models as Structured Planners for Robotic Manipulation 

1 

## **A Overview** 

This supplementary material provides additional implementation details and further analyses for StructVLA. It is organized as follows. 

In Sec. B, we present a detailed breakdown of the experimental setup to facilitate reproducibility. This includes the data curation pipeline and implementation details of the training setup. 

In Sec. C, we provide additional qualitative results and in-depth case studies. Through representative visualizations, we further illustrate StructVLA’s planning and execution behavior across a diverse range of task scenarios. 

We also provide a supplementary video demonstrating StructVLA on the real-world tidy-up task in the same folder as this supplementary PDF. 

## **B Details** 

In this section, we provide additional implementation details to facilitate reproducibility. We first describe the VLM-based offline filtering adopted during data curation, and then present the experimental setups and training configurations for the simulation benchmarks and real-world deployments.. 

### **B.1 Details for VLM-based Offline Filtering** 

After the initial candidate structured frames are extracted and saved in the keystep CSV file, we further refine them with a lightweight VLM-based filtering step. For each episode, we provide the VLM with the global task instruction, the candidate row indices from the original keystep CSV file, and the corresponding raw RGB images. Using the images as the primary evidence, the VLM removes only clearly unstable points, temporary false positives, and overly redundant candidates from dense local intervals. The retained row indices are then used to select the corresponding rows from the original CSV file and write a new filtered CSV file while preserving the original schema. In implementation, the VLM output is constrained to a fixed JSON schema containing a validity flag, an optional list of problems, and the retained row indices. 

### _Prompt used for VLM-based offline filtering._ 

```
Youarefilteringcandidatestructuredframesforarobotmanipulation
episodeusingimagesastheprimarysourceoftruth.
```

```
Theinputisanorderedlistofcandidatekeystepsfromtheoriginal
CSVfile,extractedfromrobot-centrickinematiccues.Eachcandidate
isidentifiedbyitsrowindexintheoriginalCSVfile,togetherwith
itsimageandthetaskinstruction.
```

```
Yourtaskisonlytoperformaconservativefilteringofthe
candidates.Donotrewritetheinstruction,donotaddnewevents,and
donotreconstructthesequence.
```

2 M. Jin et al. 

#### `Filtering goals:` 

- `1) Remove clearly unstable perturbation points caused by control noise, hardware jitter, or transient fluctuations.` 

- `2) Remove temporary false positives that clearly do not reflect a reasonable task progression.` 

- `3) Remove candidates that are visually too close to nearby neighbors and provide almost no additional information.` 

```
Importantprinciples:
```

- `Be conservative in filtering. Prefer keeping a candidate unless it` 

- `is clearly abnormal or clearly redundant.` 

- `When in doubt, keep the candidate rather than remove it.` 

- `Preserve sufficient temporal coverage of the episode. The remaining` 

- `candidates should still reflect the main progression of the manipulation process.` 

- `Do not over-prune the sequence. In most normal cases, the filtered` 

- `sequence should still contain multiple keyframes rather than collapsing to a single frame.` 

- `Only remove a candidate when there is clear visual evidence that it` 

- `is a noise point, a brief disturbance, or nearly duplicate with a nearby retained frame.` 

- `If several nearby candidates correspond to essentially the same` 

- `stable state, keep the earlier one.` 

- `Preserve the original temporal order of the remaining candidates.` 

- `Only delete candidates; do not add new ones.` 

- `Use the images as the primary evidence.` 

- `The task instruction is provided only as global context.` 

- `Do not apply extra semantic rules beyond visible task coherence and` 

- `local temporal consistency.` 

```
ReturnaJSONobjectwith:
```

- `filtered_ok: bool` 

- `problems: [str, ...]` 

- `kept_rows: [int, ...]` 

### **B.2 Implementation Details for Benchmarks** 

**Structured planner.** We train the structured planner by fine-tuning a pretrained world model. Unless otherwise specified, we use AdamW with a peak learning rate of 2 _×_ 10<sup>_−_4</sup> , weight decay of 0 _._ 1, and a cosine learning-rate schedule with warmup. At this stage, we primarily supervise the prediction of structured frames and disable gripper prediction, so that the planner focuses on forecasting future structured subgoals. Optionally, we retain a small auxiliary loss on the surrounding visual context to preserve the general visual modeling capability of the underlying world model. We adopt parameter-efficient fine-tuning via LoRA with rank _r_ = 32 and scaling factor _α_ = 32, applied to the major attention and MLP projection layers, while keeping the backbone weights frozen. This allows 

World Models as Structured Planners for Robotic Manipulation 

3 

the planner to adapt to the keystep-centric supervision without updating the full model. 

_SimplerEnv._ We fine-tune the structured planner on the BridgeData V2 dataset using 8 H100 GPUs for approximately 40 hours. The model is trained for 30k optimization steps. The per-device batch size is 2 with gradient accumulation of 2, resulting in an effective batch size of 32 sequences per optimization step. Each training sample contains up to 3 visual frames sampled around a structured frame with a temporal interval of 5 environment steps, providing local visual context for structured frame prediction, where we further apply a window-based sliding augmentation whose size matches the temporal interval to slightly shift the target timestep and resample its context. 

_LIBERO._ We fine-tune the same pre-trained world model on a mixed dataset consisting of all four LIBERO suites, using 8 H100 GPUs for approximately 10 hours. The model is trained for 10k optimization steps. The per-device batch size is 2 with gradient accumulation of 2, resulting in an effective batch size of 32 sequences per optimization step. Each training sample contains 4 visual frames with a temporal interval of 10 environment steps, where the same window-based sliding augmentation is applied with a size matched to the temporal interval. 

**Action policy.** In the second stage, we further fine-tune the structured planner from Stage 1 to learn an action policy. Unless otherwise specified, we use AdamW with a peak learning rate of 8 _×_ 10<sup>_−_5</sup> , weight decay of 0 _._ 1, and a cosine learning-rate schedule with warmup. At this stage, we supervise action prediction using a FAST action tokenizer, so the model is optimized as an action policy conditioned on visual observations and language instructions. 

_SimplerEnv._ We train the action policy using 8 H100 GPUs for approximately 30 hours. The model is trained for 20k optimization steps. The per-device batch size is 4, and gradients are accumulated for 4 steps across 8 GPUs, yielding an effective batch size of 128 sequences per optimization step. Each training sample contains 2 visual frames and a horizon of 5 action steps arranged in an interleaved video format. 

_LIBERO._ We train the action policy using 8 H100 GPUs for approximately 30 hours. The model is trained for 4k optimization steps. The per-device batch size is 2, and gradients are accumulated for 12 steps across 8 GPUs, yielding an effective batch size of 192 sequences per optimization step. Each training sample contains 4 visual frames and a horizon of 10 action steps arranged in an interleaved video format. Unlike SimplerEnv, wrist-camera observations are included at this stage. 

**Inference setting.** At inference time, we evaluate the trained model in the SimplerEnv-WidowX environment under different history context lengths _L ∈{_ 2 _,_ 3 _,_ 4 _}_ . Based on this ablation, we adopt _L_ = 4 as the default setting and report the corresponding results as the final model performance. Unless explicitly stated otherwise, all quantitative results and analyses that do not specifically compare different history lengths are obtained with history context length _L_ = 4. For LIBERO, we also use history context length _L_ = 4, following the default setting selected based on the SimplerEnv history-length ablation. 

4 M. Jin et al. 


**Fig. S1: Qualitative analysis of history context length on task execution.** We compare policy behavior under different history context lengths ( _L_ ) on two representative tasks: “Stack green cube on yellow cube” (top) and “Put spoon on towel” (bottom). With a short history ( _L_ = 2), the policy lacks sufficient spatio-temporal context to accurately infer task progress and interaction geometry. **Top:** this leads to imprecise placement, causing the cube to slip during stacking (red dashed box). **Bottom:** the policy exhibits temporal ambiguity and incorrectly re-grasps the object after it has already been placed. In contrast, a longer history ( _L_ = 4) provides richer temporal evidence and motion context, enabling accurate execution in both cases. 

### **B.3 Implementation Details on Real-world Deployment** 

As described in the main paper, we deploy our method on a real Franka robot arm and conduct experiments on both basic pick-and-place tasks and long-horizon tidy-up tasks. We conduct two separate training runs corresponding to these task categories, and the detailed training procedures are described below. 

_Structured planner._ For real-world experiments, we fine-tune the same pretrained world model on a real-robot dataset using 4 H100 GPUs for approximately 3 hours in the first-stage structured-planner training. We use AdamW with a peak learning rate of 6 _×_ 10<sup>_−_5</sup> , weight decay of 0 _._ 1, and a cosine learningrate schedule with warmup for 2k optimization steps. The per-device batch size is 4 with gradient accumulation of 2, resulting in an effective batch size of 32 sequences per optimization step. Each training sample contains 4 visual frames from the front-view camera only. The temporal interval is set to 3 steps for pickand-place tasks and 4 steps for tidy-up tasks, while the window-based sliding augmentation size is fixed to 3 in both settings. At this stage, we supervise only visual prediction. Unlike the simulated benchmarks, we directly fine-tune the model on the limited real-robot data with full-parameter training rather than using LoRA-based parameter-efficient fine-tuning. 

World Models as Structured Planners for Robotic Manipulation 

5 

_Action policy._ We further fine-tune the structured planner from Stage 1 to learn the action policy. Training is performed on 4 H100 GPUs for approximately 3 hours. We use AdamW with a peak learning rate of 6 _×_ 10<sup>_−_5</sup> , weight decay of 0 _._ 1, and a cosine learning-rate schedule with warmup for 2k optimization steps. The per-device batch size is 4 with gradient accumulation of 2, resulting in an effective batch size of 32 sequences per optimization step. Each training sample contains 2 visual frames and a horizon of 5 action steps arranged in an interleaved video format. At this stage, we supervise only action prediction using a FAST action tokenizer, and wrist-camera observations are also included. 

_Inference setting._ For real-world deployment, we adopt a server-client inference architecture. The trained model is hosted on a remote RTX 4090 GPU server and exposed through a Flask-based API. During execution, the robot-side client sends the current task description together with synchronized observations from the front and wrist cameras to the server. The server receives the incoming images, performs model inference, and returns a predicted action chunk to the robot client for execution. Empirically, we execute the first two actions from each predicted action chunk at every control cycle. This design decouples model inference from on-robot control and enables efficient interaction between the robot platform and the deployed policy model. 

For the baselines, we follow training conditions that are matched as closely as possible to those of our method, including the data setting and optimization protocol where applicable, to ensure fair comparison. 

## **C In-depth analysis and visualizations** 

In this section, we provide additional qualitative analyses to complement the quantitative results. Through a set of representative visualizations, we further examine the behavior of StructVLA and highlight how the structured planner captures task progress and supports long-horizon control. 

### **C.1 Task Understanding and History Context** 

We further present qualitative rollouts from the SimplerEnv environment to analyze how history context length affects task understanding and execution. When the available history is short, the planner may fail to accurately infer the current interaction stage and task progress, which can lead to suboptimal decisions. In some cases, this manifests as incorrect intermediate actions; in others, the policy continues issuing commands even after the task has effectively been completed. In StructVLA, increasing the history window substantially alleviates these issues, since richer temporal evidence allows the structured planner to better disambiguate the current state and form more stable long-horizon plans. 

As illustrated in the bottom example of Fig. S1, under short-history conditions StructVLA may misinterpret task status and occasionally attempt to re-execute an action that has already been completed. This behavior is consistent with the design of our model: StructVLA is built upon long-horizon visual 

6 M. Jin et al. 

foresight and predicts structured subgoals over extended spatiotemporal horizons, so sufficient temporal context is important for accurately grounding the current task phase. At the same time, compared with models based on dense future prediction, StructVLA reasons over sparse structured planning targets and can therefore make more effective use of extended context for planning and prediction, while being less affected by redundant visual information. 

### **C.2 Action Accuracy and Window-based Sliding Augmentation** 

During structured planner training, we adopt a window-based sliding augmentation strategy, in which the target timestep is slightly shifted and its local context is resampled around the annotated structured frame, thereby densifying supervision and exposing the planner to richer spatiotemporal patterns. This allows the model to observe a broader range of task phases and encourages it to model short-horizon future progression even when the current observation is already close to a structured frame. In practice, this improves execution efficiency and helps prevent the planner from becoming overly conservative around key stages of the trajectory. At the same time, the augmentation may introduce a mild temporal offset, in the sense that the predicted structured frame can be slightly shifted relative to the ideal next-step target, which may occasionally influence fine-grained execution precision. 

Our qualitative analysis in Fig. S1 suggests that this temporal offset can sometimes appear as minor execution bias when historical context is limited. For example, in the top example, it is reflected as slight spatial imprecision during placement. Increasing the amount of historical context helps alleviate this effect, since richer temporal evidence allows the planner to better resolve the intended interaction stage and compensate for local prediction offsets. This may be further explored through training or architectural refinements that improve fine-grained temporal alignment while preserving the robustness benefits of augmented supervision. 

### **C.3 More Visual Predictions from Structured Planner** 

Fig. S2 presents a broader set of representative predictions generated by our structured planner. These visualizations further demonstrate that the planner maintains strong long-horizon semantic understanding and spatiotemporal reasoning across diverse manipulation scenarios. Notably, consistent with the examples shown in Fig. S2, the planner still produces temporally coherent and task-relevant visual foresight under the window-based supervision strategy, indicating that this training design does not compromise the overall quality of structured planning. 

However, we observe a more noticeable challenge in articulated manipulation tasks, such as the “Open microwave” scenario shown in Fig. S2(e). Unlike rigid pick-and-place tasks, the key progress transitions in hinge-driven interactions are not naturally aligned with discrete gripper-state changes, but instead unfold through continuous geometric motion. As a result, our current structured-frame 

World Models as Structured Planners for Robotic Manipulation 

7 

extraction strategy, which is primarily built on robot-centric kinematic cues and contact-related transitions, is less well matched to these articulated motion patterns. While the planner can still capture the high-level goal progression, _e.g_ ., the microwave door being opened, the corresponding fine-grained arm motion is less precise. This limitation suggests that future improvements should focus on more geometry-aware structured-frame extraction for articulated tasks, for example by incorporating continuous motion-phase cues such as relative object pose evolution or articulation-state changes, so that the planner can better align visual foresight with the underlying interaction dynamics. 

M. Jin et al. 

8 


**Fig. S2: Extended visual foresight predictions of the structured planner.** These examples show that our planner predicts sparse yet informative visual subgoals that remain temporally coherent and physically grounded across diverse manipulation tasks. The predicted structured frames align with key interaction stages, such as approach, contact, transfer, and placement, supporting the central design of StructVLA: replacing dense future rollouts with compact structured foresight for control. In (e), we show a more challenging case involving complex kinematics, particularly for articulated or highly constrained object motions. 

