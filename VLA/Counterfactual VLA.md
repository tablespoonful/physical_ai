---
title: "Counterfactual VLA: Self-Reflective Vision-Language-Action Model with Adaptive Reasoning"
date: "2025-12-30"
authors: "Zhenghao \"Mark\" Peng; Wenhao Ding; Yurong You; Yuxiao Chen; Wenjie Luo; Thomas Tian"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2512.24426
pdf: https://arxiv.org/pdf/2512.24426
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.24426)** / [論文ページ](https://arxiv.org/abs/2512.24426)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Counterfactual VLA: Self-Reflective Vision-Language-Action Model with Adaptive Reasoning** 

Zhenghao Peng<sup>1,2*</sup> Wenhao Ding<sup>1</sup> Yurong You<sup>1</sup> Yuxiao Chen<sup>1</sup> Wenjie Luo<sup>1</sup> Thomas Tian<sup>1</sup> Yulong Cao<sup>1</sup> Apoorva Sharma<sup>1</sup> Danfei Xu<sup>1</sup> Boris Ivanovic<sup>1</sup> Boyi Li<sup>1</sup> Yan Wang<sup>1†</sup> Marco Pavone<sup>1,3†</sup> 1NVIDIA 2UCLA 3Stanford University 

## **Abstract** 

_Recent reasoning-augmented Vision-Language-Action (VLA) models have improved the interpretability of end-toend autonomous driving by generating intermediate reasoning traces. Yet these models primarily describe what they perceive and intend to do, rarely questioning whether their planned actions are safe or appropriate. This work introduces Counterfactual VLA (CF-VLA), a self-reflective VLA framework that enables the model to reason about and revise its planned actions before execution. CF-VLA first generates time-segmented meta-actions that summarize driving intent, and then performs counterfactual reasoning conditioned on both the meta-actions and the visual context. This step simulates potential outcomes, identifies unsafe behaviors, and outputs corrected meta-actions that guide the final trajectory generation. To efficiently obtain such self-reflective capabilities, we propose a rollout–filter–label pipeline that mines high-value scenes from a base (noncounterfactual) VLA’s rollouts and labels counterfactual reasoning traces for subsequent training rounds. Experiments on large-scale driving datasets show that CF-VLA improves trajectory accuracy by up to 17.6%, enhances safety metrics by 20.5%, and exhibits adaptive thinking: it only enables counterfactual reasoning in challenging scenarios. By transforming reasoning traces from one-shot descriptions to causal self-correction signals, CF-VLA takes a step toward self-reflective autonomous driving agents that learn to think before they act._ 

## **1. Introduction** 

Recent advances in Vision–Language–Action (VLA) models highlight the promise of test-time reasoning for embodied decision-making. By generating intermediate language traces that describe the scene and task, reasoning- 

> *Work done while the author was an intern at NVIDIA. 

> †Equal advising. 


Figure 1. **Counterfactual Vision-Language-Action (CF-VLA) Model.** Top: CF-VLA conducts reasoning adaptively. The model engages in reasoning more frequently and achieves more significant task performance gains in complex scenarios that have higher trajectory errors. Bottom: CF-VLA reflects on its own action plan and corrects it before generating the final trajectory. 

augmented VLAs have improved interpretability and robustness in manipulation [2, 3, 5, 22] as well as autonomous driving [16, 18, 20]. In these systems, a large visionlanguage backbone engages in a slower, more deliberative form of “thinking”, spending additional compute to verbalize the observation and justify the planned actions. 

However, the reasoning in current VLAs is largely descriptive rather than **_self-reflective_** . Existing models typically describe what they observe (e.g., “the cabbage next to the bowl” and “a pedestrian is crossing”) and what they intend to do (e.g., “place the cabbage into the container” and “I should be cautious”). As a result, the reasoning trace often serves as a one-shot commentary on the scene and action 

4022 

choice, without a self-reflective loop that verifies whether the model’s own command is appropriate: once the VLA model produces a textual intent, it is typically treated as ground truth and used to condition a low-level policy, rather than being checked for inconsistencies with visual cues and revised accordingly. 

Self-correction has been explored in embodied VLMs through replanning and failure recovery [11, 22], where the agent detects that an action it executed failed and then switches to an alternative plan. These mechanisms typically operate _after_ observing a mistake or via an external verifier, and do not enable the VLA itself to reason explicitly about the consequences of its own action plan _before_ execution. We refer to this desired ability as **_counterfactual reasoning_** . More recent robotics VLAs begin to incorporate world models to proactively simulate, verify, and select planning steps [6, 19, 26]. While these approaches move toward earlier detection of problematic actions, they fundamentally rely on an external future-prediction model to judge the quality of the proposed plan. This is qualitatively different from self-reflection: external simulation can evaluate a plan, but it cannot help the VLA understand its own reasoning process. This raises a central question: _can we obtain self-reflective, counterfactual reasoning inside the VLA itself, without an external world model or verifier, analogous to the self-reflection behaviors observed in language-only reasoning models?_ Two obstacles make this challenging. First, most VLAs lack an _action–language alignment_ : the action is represented by latent tokens [3], and there is no action _→_ language alignment, leaving the language model with no handle to talk about its actions. Second, standard training pipelines rarely teach models to answer _counterfactual questions_ such as: “Given the plan I just proposed, what will happen, and how should I change it?” 

In this paper, we propose **_Counterfactual VLA (CFVLA)_** , a VLA equipped with a _self-reflective_ reasoning loop that performs counterfactual analysis directly on its predicted controls. As illustrated in Fig. 1 (bottom), CF-VLA first predicts a sequence of language-based, time-segmented meta-actions that summarize the agent’s intent. Instead of treating them as final, the model then conditions a counterfactual chain-of-thought step on both the visual context and its own meta-actions, asking “If I follow this plan, what would happen and is that desirable?” It revises unsafe or suboptimal plans (e.g., from “accelerate toward the intersection” to “decelerate early and yield”) before committing to the final trajectory. This meta-actions _→_ counterfactual reasoning _→_ updated meta-actions _→_ trajectory loop upgrades reasoning from one-shot description to counterfactual analysis of the model’s own behavior, and turns that one-shot analysis into actionable self-correction. To realize such behavior in practice, CF-VLA combines meta-actions with a rollout–filter–label pipeline: 1) the current policy is 

rolled out to generate candidate meta-actions and trajectories; 2) high-value data points are automatically selected by checking if pre-filling ground-truth meta-actions substantially improves trajectories over model-generated metaactions; and 3) a teacher model is prompted to produce counterfactual reasoning traces that explain why the current plan is less preferable and how to adjust it. Training on a mixture of nominal and counterfactual-labeled datasets under a unified instruction prompt yields a single CF-VLA model that exhibits **_adaptive counterfactual reasoning_** : as shown in Fig. 1 (top), the model thinks more often and achieves larger task improvement in the hardest scenarios. 

We conduct extensive experiments on a large-scale internal dataset to validate our design. CF-VLA consistently outperforms trajectory-only and non-reflective meta-action baselines on trajectory metrics by 17.6% and 9%, respectively, and increases the safety metric by 14.7%. We further show that performance can be improved if we apply the trained CF-VLA again to the rollout-filter-label pipeline for multi-round training. Our core contributions are: 

- **1) Self-reflective counterfactual reasoning for VLA.** We propose a new reasoning-about-action paradigm to condition the reasoning of VLA on its own predicted metaactions, anticipate the consequences, and revise the plan before generating final actions. This upgrades reasoning from descriptive explanations to causal self-correction. 

- **2) Meta-actions and counterfactual data pipeline.** We use time-segmented meta-actions for action-language alignment and propose the rollout–filter–label pipeline to automatically curate counterfactual data from the rollout of the model, forming a self-improving loop that enhances both reasoning and action. 

- **3) Adaptive thinking in autonomous driving.** CF-VLA exhibits the ability to _think when necessary_ , concentrating counterfactual reasoning on the most challenging scenarios. Experiments show that CF-VLA improves trajectory accuracy, safety metrics, and meta-action alignment, while maintaining reasonable test-time compute by adapting its think rate to the scenario difficulty. 

## **2. Related Works** 

**VLA Models for Autonomous Driving.** Recent VLA models integrate language reasoning with visual context to generate control actions. Some use high-level commands [12, 21, 27], while others rely on intermediate trajectory tokens [18, 20, 23, 31]. SimLingo [20] introduces “action dreaming” to align language and control via offline counterfactual simulation. Alpamayo-R1 [18] incorporates a structured language abstraction and trajectory diffusion to improve long-tail generalization. AutoVLA [32] incorporates chain-of-thought (CoT) traces, but uses them primarily as one-pass rationales for interpretability. These 

4023 


Figure 2. **The framework of CF-VLA.** A base VLA is finetuned on a counterfactual reasoning dataset generated by a rollout–filter–label pipeline. The resulting CF-VLA supports both direct inference and self-reflective inference, in which counterfactual reasoning edits meta-actions before trajectory generation. 

models enhance interpretability but remain largely descriptive: they describe what the model sees and intends, without critiquing the proposed action itself. In contrast, our CFVLA explicitly conditions reasoning on the model’s own proposed behavior, enabling self-reflective revision through counterfactual analysis. 

**Counterfactual Reasoning and Self-Reflection.** Counterfactual reasoning models alternative actions and their consequences, but most prior work uses counterfactuals externally rather than as model-internal self-reflection. CAST [10], SimLingo [20], and VLAPS [17] generate counterfactual instruction–action pairs or search over simulated futures to improve instruction following or correct policies, while the underlying VLA does not itself reason about or revise its own plan. A separate line of work introduces reflective loops around the policy using auxiliary verifiers or planners [6, 11, 26]. Several works analyze failures and successes with large models to relabel data, synthesize rewards, or trigger replanning [1, 9, 13, 15]. In all these cases, counterfactual evaluation and reflection are implemented by external modules wrapped around the policy. In contrast, CF-VLA performs counterfactual reasoning over its _own_ predicted meta-actions inside the forward pass and revises them before trajectory generation, yielding an online self-correction mechanism without separate validators. 

**Adaptive Reasoning.** Adaptive reasoning dynamically selects between direct response and step-by-step thinking [4, 8, 24, 25, 28–30]. OneTwoVLA [14] uses control tokens to toggle between fast acting and slow reasoning, invoking language reasoning mainly at subtask boundaries (e.g., task completion or errors), so “slow thinking” is tied to task switching rather than scene difficulty. In contrast, CF-VLA learns to invoke reasoning from visual cues and its own behavior, focusing on challenging scenes and skipping reasoning in normal cases. AdaThinkDrive [16] categorizes scenarios into simple or challenging ones via rulebased heuristics and uses RL to fine-tune when to think. We instead show that adaptive reasoning can emerge from supervised fine-tuning alone: by identifying hard scenarios 

based on the model’s capability (Sec. 3.1) and training on a mixture of data, CF-VLA naturally allocates more test-time compute to difficult scenes (see Fig. 1). 

## **3. Method** 

End-to-end Vision-Language-Action (VLA) models have demonstrated promising progress in mapping visual context directly to control output. However, their reasoning processes are largely descriptive: when the agent proposes an incorrect plan, there is no mechanism for the model itself to analyze the plan and revise the decision before execution. This section introduces **_Counterfactual VLA (CFVLA)_** , which equips a VLA with a self-reflective loop that reasons about its own predicted actions and uses that reasoning to correct the plan. 

### **3.1. Self-Reflective Counterfactual Reasoning** 

Several challenges remain to empower a VLA with counterfactual (CF) reasoning. First, the model needs an intermediate representation that is both interpretable to the language backbone and tightly coupled to action. We address this with time-segmented meta-actions (Sec. 3.2), so the model can reason about and revise high-level intent in language space before decoding trajectories. Second, CF reasoning must relate meta-actions to their future consequences. To prepare data to fine-tune the model, we develop a rollout– filter–label pipeline (Sec. 3.3) that selects data and autogenerates high-value counterfactual reasoning traces. We consider CF reasoning as a plugged-in self-reflective mechanism on top of meta-actions. As shown in Fig. 2, instead of mapping meta-actions to trajectories (meta _→_ traj), CFVLA performs a self-reflective loop: 

meta-actions _→_ CF reasoning 

_→_ updated meta-actions _→_ trajectory. 

**Adaptive Thinking.** Adaptive reasoning allows a model to decide dynamically when to conduct reasoning and when to respond directly. This mechanism is essential because most scenarios are straightforward, and explicit reasoning on them increases hallucination risks and wastes test-time compute. As shown in Fig. 3(A), we use the same instruction for the model and allow it to implicitly decide whether to generate the reasoning traces. As both metaactions and reasoning operate in the language space, the CF reasoning behavior is controlled by the words (Action: or Thinking:) generated after the first meta-action sequence. Training on a mixture of samples with and without CF traces allows the model to implicitly learn when selfreflective inference is necessary. 

### **3.2. Meta-Actions** 

Meta-actions provide a language-native intermediate abstraction between reasoning and low-level action. Each 

4024 


Figure 3. **(A) Adaptive Reasoning** can be achieved by training models on a mixture of data with the unified instruction prompt. **(B) Data generation process.** We build a rollout–filter–label pipeline that runs the VLA, detects samples where its meta-actions are problematic, and labels counterfactual (CF) reasoning traces, forming a CF reasoning dataset. **(C) Data filtering process.** We use trajectory disagreement between trajectories that are free-generated and those induced by the ground-truth meta-actions to filter data. Each data point is colored by the meta-actions IOU in free generation. 

meta-action sequence expresses the ego vehicle’s intended behavior along three orthogonal dimensions: _longitudinal_ (Accelerate, Decelerate, Keep Speed, Wait, Reverse), _lateral_ (Straight, Left Turn, Right Turn), and _lane-level_ (Keep Lane, Left Lane Change, Right Lane Change). 

Though playing an analogous role to the low-level command used in manipulation VLAs [3, 22], navigation models [7] and autonomous driving VLAs [23, 32], our metaactions consider timing and are tightly coupled to the continuous trajectories. CF-VLA models meta-actions as **timepartitioned segments** covering the 6.4-second planning horizon. Within each of the three groups, meta-actions are defined over non-overlapping temporal intervals and together describe the intended evolution of driving behavior. This temporal format allows the model to reason compositionally about action transitions and to capture temporal intent and directly align language reasoning with the structure of the predicted trajectory. Example meta-action sequences can be found in Fig. 5. 

### **3.3. Rollout-Filter-Label Counterfactual Pipeline** 

As illustrated in Fig. 3(B), to supervise counterfactual reasoning, CF-VLA relies on a rollout–filter–label data curation pipeline that mines high-value scenes from the model’s own behavior. 

**Data Rollout.** Starting from a VLA trained with metaactions but without counterfactual reasoning, the model is rolled out on the training set. For each scene, two sets of trajectories are generated: 1) _Free generation_ **x** free: the model first predicts meta-actions and then decodes the trajectory conditioned on its _own_ meta-actions. 2) _Pre-filled metaactions_ **x** pf: the model is conditioned on the _ground-truth_ meta-actions and only decodes the trajectory. For robust- 

ness, 6 output trajectories are sampled per scene in each setting. This yields paired sets of trajectories ( **x** free _,_ **x** pf) for the same visual context. 

**Data Filtering.** Let minADE( **x** _, x_<sup>_⋆_</sup> ) denote the minimum displacement error between a set of predicted trajectories **x** and the expert future _x_<sup>_⋆_</sup> . We scatter each scenario based on (minADE( **x** free _, x_<sup>_⋆_</sup> ) _,_ minADE( **x** pf _, x_<sup>_⋆_</sup> )) in Fig. 3(C), where each data point is colored by the metaactions accuracy (IOU) in free generation. The key insight is that many scenes lie below the diagonal: the model performs poorly in free generation but matches the expert trajectory when meta-actions are pre-filled and they usually have low IOU. These are precisely the scenes where meta-actions are the bottleneck. CF-VLA uses **trajectory disagreement** between trajectories that are free-generated and those induced by ground-truth-filled meta-actions to filter data: minADE( **x** pf _, x_<sup>_⋆_</sup> ) _<_ minADE( **x** free _, x_<sup>_⋆_</sup> ) and minADE( **x** free _, x_<sup>_⋆_</sup> ) _> ϵ_ , where _ϵ_ = 0 _._ 5 avoids labels on already mastered scenarios. Intuitively, these are cases where improving meta-actions would significantly improve trajectory quality. As long as we improve the meta-actions to be closer to the ground truth, we can harvest task improvement. Samples above the diagonal already have good freegeneration trajectories, so counterfactual supervision brings limited benefit and is not needed. Sec. 4.3 shows the data filtering is crucial to the final performance. 

**Data Labeling.** For the filtered scenes, concise counterfactual traces are generated with a high-capacity teacher model (Qwen2.5-VL-72B-Instruct). The outline of the prompt to the teacher is presented in Fig. 3(B). The output is a single paragraph that: 1) diagnoses why the predicted meta-actions are less preferable than the expert plan, and 2) indicates how they should be adjusted. These labeled 

4025 


Figure 4. **The dataset composition.** We use a subset of the metaaction-labeled dataset _D_ meta as the validation set _D_ val. 

samples form the counterfactual reasoning dataset _D_ CF. The full teacher prompt is provided in the Appendix. 

### **3.4. Implementation Details** 

**Mixed-data Training.** We adopt a mixed-data training scheme combining the trajectory-only dataset _D_ traj, the meta-action–labeled dataset _D_ meta, and the counterfactual reasoning dataset _D_ CF as shown in Fig. 4. Training proceeds in stages. The base VLM is first trained on _D_ traj to learn basic trajectory generation (traj-only). Meta-actions are then introduced by fine-tuning on _D_ traj _∪D_ meta, yielding the meta-act model used in the initial rollout (Sec. 3.3). Finally, the full CF-VLA is obtained by further fine-tuning on the mixture _D_ traj _∪D_ meta _∪D_ CF. We unfreeze all parameters during training. 

**Loss Masking and Weighting.** The model is optimized with cross-entropy loss over assistant-generated tokens only; tokens from system or user prompts are masked. For counterfactual samples in _D_ CF, the loss on the _first_ (uncorrected) meta-action block is also masked to prevent the model from learning from prior mistakes. Within the assistant response, different token groups (meta-actions, reasoning, or trajectory tokens) have different loss weights. **Multi-round training.** An appealing property of CFVLA is that the trained model can be inserted back into the rollout–filter–label loop to create new rounds of CF data _D_ CF<sup>Round2</sup> . Unlike traditional CoT methods that generate mostly deterministic explanations for a given scene, CF-VLA’s reasoning is conditioned on the predicted metaactions and can therefore produce diverse reasoning traces for the same scenario. This allows us to further exploit the dataset and generate different reasoning traces with different meta-actions. As shown in Sec. 4.2, fine-tuning on another round of CF datasets further improves the model, realizing a self-improving counterfactual flywheel. 

**Model Architecture.** CF-VLA is similar in size and design to Alpamayo-R1 [18]. The model takes text prompts, two front-facing videos, and the ego-trajectory history as inputs. The text prompt defines the tasks: 1) pure trajectory prediction, or 2) meta-actions and trajectory prediction with optional counterfactual reasoning. A wide (120°) and a telephoto (30°) cameras provide 2 videos at 2 Hz over the past 2 s. The past 1.6 s of ego motion is embedded into a single trajectory-history token by an MLP-based trajectory 

history encoder. Future motion is represented by a compact set of discrete trajectory tokens. We expand the vocabulary of the VLM backbone to accommodate the new tokens introduced by the trajectory tokenizer, as well as additional _<_ begin ~~o~~ f ~~t~~ raj> and _<_ end ~~o~~ f ~~t~~ raj> tokens. 

## **4. Experiments** 

### **4.1. Experimental Setup** 

**Datasets.** We train and evaluate models on a large proprietary dataset consisting of 80,000 hours of human driving data from 25 countries, covering a variety of scenarios including highway and urban driving, weather conditions, and daytime and nighttime. The entire data corpus forms the trajectory-only dataset _D_ traj, which contains raw sensor data paired with ego-vehicle future trajectories. Within _D_ traj, we auto-labeled 3,000 hours of data and constructed the meta-action-labeled subset _D_ meta. Meta-action annotations are automatically extracted from expert trajectories through rule-based detectors operating on kinematic profiles. We label meta-actions at 10Hz over the balanced dataset curated based on Operational Design Domains (ODDs). We split _D_ meta into training and validation subsets, with the validation subset denoted as _D_ val. All of our results are reported on this evaluation set. The counterfactual reasoning dataset _D_ CF comes from the training set of _D_ meta. In summary, the base trajectory-only set _D_ traj contains about 11.6M 20second video clips and provides large-scale behavioral diversity. For _D_ meta, multiple samples are used for one video clip. The training set of _D_ meta includes 433K 20s clips and 801K 8.4s samples. There are 39K video clips and 73K samples in the validation set. The counterfactual reasoning dataset _D_ CF usually contains 200K samples. **Metrics.** We evaluate models along three dimensions: 

1) **Trajectory Accuracy** : We report _MinADE/AvgADE_ and _MinFDE/AvgFDE_ as mean/endpoint displacement errors over 6 predicted modes (lower is better), and _Corner Distance_ as the average deviation of vehicle-corner keypoints for measuring turning and lane-keeping precision. 

2) **Safety Characteristics** : _Collision Rate_ measures the proportion of predicted trajectories that collide with other road users’ trajectories within 5s, while _Out-of-road Rate_ quantifies whether the predicted trajectories violate the road boundary. These complement distance-based metrics by revealing whether small deviations lead to unsafe outcomes. 3) **Reasoning Quality** : _Meta-Action IOU_ measures the alignment between predicted and ground-truth meta-actions over 64 _×_ 3 bins (longitudinal, lateral, and lane). For CFVLA, we report IOU after self-reflection, i.e., for the updated meta-actions. We also record _Output Length_ (# tokens) and _Think Rate_ , the fraction of responses containing counterfactual reasoning, to quantify the test-time compute and adaptive reasoning. 

4026 

Table 1. **Evaluation results.** CF-VLA improves trajectory accuracy (ADE, FDE), behavioral safety (Corner Distance, Collision, Off-road), and reasoning quality (IOU). _↓_ lower is better, _↑_ higher is better. 

|**Model**|**ADE**_↓_<br>Min (Avg)|**FDE**_↓_<br>Min (Avg)|**Corner**<br>**Dist.**_↓_|**Collision**_↓_|**Off-road**_↓_|**IOU**_↑_<br>init_→_edited|**Output Len.**<br>**(Think Rate)**|
|---|---|---|---|---|---|---|---|
|traj-only|0.9283 (1.8284)|2.5912 (5.1150)|0.8563|0.0244|0.0720|–|10.00 (–)|
|lang-meta-act|0.8021 (1.5607)|2.2540 (4.4967)|0.7358|0.0206|0.0617|0.9183|144.28 (1.00)|
|meta-act(w/o route)|0.8411 (1.6216)|2.3647 (4.6616)|0.7720|0.0224|0.0625|0.9169|85.32 (–)|
|CF-VLA(w/o r., round1)|0.7650 (1.5606)|2.1416 (4.3307)|**0.6975**|**0.0191**|0.0601|0.9153_→_0.9212|113.36 (0.148)|
|CF-VLA(w/o r., round2)|**0.7647**(**1.5032**)|**2.1365**(**4.1927**)|0.6996|0.0194|**0.0583**|**0.9174**_→_**0.9228**|102.12 (0.083)|
|meta-act(w/ route)|0.7263 (1.4612)|1.9561 (3.9269)|0.6600|0.0196|0.0619|0.9236|87.20 (–)|
|CF-VLA(w/ r., round1)|**0.6712**(1.4574)|**1.7988**(3.9466)|0.6010|0.0177|0.0593|0.9207_→_0.9231|125.67 (0.219)|
|CF-VLA(w/ r., round2)|0.6813 (**1.3898**)|1.8291 (**3.7474**)|0.6168|**0.0174**|**0.0585**|**0.9238**_→_**0.9276**|109.36 (0.123)|


**Baselines.** All models are initialized from traj-only for fair comparison. We prepare two variants of the models to train with or without route information, which contain 20 waypoints spanning the future 80m with equal spacing. 

- traj-only: trained purely on _D_ traj without any metaaction or reasoning signals, serving as the standard endto-end Vision-Action model. No route is used. 

- meta-act: introduces meta-action sequence as intermediate control primitives before trajectory generation. 

- lang-meta-act: jointly predicts language reasoning, meta-actions, and trajectory. 

- CF-VLA: our fine-tuned models from meta-act and can perform counterfactual reasoning. The second round training of CF-VLA uses data from calling the data pipeline in Sec. 3.1 on the first round CF-VLA. 

### **4.2. Main Experiments** 

We evaluate whether counterfactual reasoning improves trajectory accuracy, safety characteristics, and reasoning quality. Quantitative results are reported in Table 1. 

**Impact of meta-actions and language.** Starting from traj-only, introducing meta-actions (meta-act w/o route) reduces trajectory error by about 9% in minADE and minFDE, showing that structured action abstraction provides stronger motion priors than direct trajectory generation. Adding language supervision (lang-meta-act) yields a further _∼_ 5% improvement over meta-act, which indicates that language helps align motion intent with scene semantics. With route information, meta-act (w/ route) provides an even stronger baseline. 

**Impact of counterfactual reasoning.** Compared to their non-reasoning counterparts, CF-VLA variants consistently improve both trajectory error and meta-action alignment. Without route, CF-VLA (round2) achieves around 9-10% lower minADE / minFDE than meta-act while also increasing meta-action IOU by roughly 0.5–1.0 absolute points after counterfactual editing. With route, CF-VLA (round1) similarly improves over meta-act across trajectory, safety, and IOU, confirming that self-reflective reason- 

ing leads to more expert-like meta-actions and trajectories. **Behavioral safety.** Gains from CF-VLA are not only geometric but also safety-critical. Relative to traj-only, the best CF models reduce collision rate by roughly 25–30% and off-road violations by about 15–20%, while also lowering corner distance by _∼_ 30%. Within each setting (with / without route), CF-VLA variants consistently achieve the lowest or near-lowest collision and off-road rates, indicating that counterfactual self-reflection translates into smoother, more stable, and more rule-consistent driving behavior. **Impact of multi-round counterfactual training.** Applying the data pipeline in Sec. 3.3 a second time yields additional gains while making reasoning more efficient. CF-VLA (w/o route, round2) outperforms CF-VLA (w/o route, round1) in AvgADE/FDE, off-road rate, and edited IOU, while using a lower think rate. With route information, CF-VLA (w/ route, round2, 3 ds) slightly trades minimum error for better average ADE/FDE and higher IOU, and further improves collision and off-road rates compared to CF-VLA (w/ route, round1). Importantly, the secondround models trained on 3 datasets reduce the think rate by almost half and shorten the average output length. This shows that a second CF round can simultaneously refine performance and substantially reduce test-time overhead, extracting more value from the same driving data. 

**Adaptive thinking and compute.** Reasoning inevitably increases sequence length compared to non-reasoning models, but CF-VLA uses test-time compute much more efficiently than models that always think. Compared with lang-meta-act, which reasons for every sample, CF-VLA (w/ route, round1) already achieves better performance with a think rate below 0.25. After the second CF training round, CF-VLA (w/ route, round2, 3 datasets) further reduces the think rate by roughly 40–45% while maintaining or improving average errors and IOU. A similar pattern appears in the no-route setting, indicating that the model learns **adaptive reasoning** . Another illustration is Fig. 1. It shows **_the model thinks more frequently when the scenario is harder_** . The top plot shows that 

4027 

Table 2. **Ablations on meta–trajectory alignment and adaptive counterfactual reasoning.** We train models without route information. 

|**Model**|**MinADE**_↓_|**AvgADE**_↓_|**MinFDE**_↓_|**AvgFDE**_↓_|**MinIOU**_↑_<br>(init_→_edited)|**Corner**<br>**Dist.**_↓_|**Output**<br>**Length**|**Think**<br>**Rate**|
|---|---|---|---|---|---|---|---|---|
|meta-act(baseline)|0.8411|1.6216|2.3647|4.6616|0.9169|0.7720|85.32|-|
|meta-act(pre-filled)|0.4831|0.9968|1.2412|2.5667|1.0|0.4399|8.00|-|
|CF-VLA(adaptive)|**0.7650**|1.5606|**2.1416**|4.3307|0.9153_→_**0.9212**|**0.6975**|113.36|0.1478|
|CF-VLA(force no think)|0.7897|1.4890|2.2178|4.1508|0.9133|0.7274|87.43|0.0|
|CF-VLA(force think)|0.9319|2.1144|2.8822|6.3699|0.9132_→_0.8565|0.8271|257.42|1.0|
|explicit(meta_→_act)|0.7968|**1.4686**|2.2426|**4.0922**|0.9127|0.7363|87.99|-|
|explicit(CF reasoning)|0.9331|2.0628|2.8647|6.1872|0.8902_→_0.8551|0.8339|258.06|0.9971|
|meta-act(multi-round)|0.7906|1.504|2.216|4.1995|0.9128|0.7275|88.3093|-|


Table 3. **Effect of our proposed data filtering pipeline.** Models are fine-tuned with route information from meta-act (w/ route). 

|**Model**|**MinADE**_↓_|**AvgADE**_↓_|**MinFDE**_↓_|**AvgFDE**_↓_|**MinIOU**_↑_<br>(init_→_edited)|**Corner**<br>**Dist.**_↓_|**Output**<br>**Length**|**Think**<br>**Rate**|
|---|---|---|---|---|---|---|---|---|
|CF-VLA(filtered ds)|0.6712|1.4574|1.7988|3.9466|0.9207_→_0.9231|0.6010|125.67|0.2190|
|CF-VLA(whole ds)|0.6811|1.4185|1.8296|3.8344|0.9207_→_0.9231|0.6128|191.14|0.6677|


the think rate correlates strongly with the trajectory error (minADE). Simple scenarios like vehicle following rarely trigger counterfactual reasoning, while high-uncertainty or high-risk scenarios, such as lane changes, turning maneuvers, and VRUs, induce significantly more CF reasoning. CF-VLA achieves better error reduction when the scenarios are harder, suggesting that CF-VLA not only reasons adaptively but learns when reasoning is most beneficial. 

#### **Key Takeaways** 

- **1)** Self-reflection via counterfactual reasoning in CF-VLA consistently improves both the precision and reliability of driving planners, delivering the largest gains in accuracy, safety, and IOU beyond single-shot reasoning models. 

- **2)** Multi-round CF training squeezes more value from the same data, improves performance while substantially reducing think rate, achieving the best accuracy–safety–compute trade-off. 

- **3)** The results establish a clear performance ladder: traj-only _<_ meta-traj 

   - _<_ lang-meta-traj _<_ CF-VLA. 

- **4)** CF-VLA learns adaptive reasoning: it saves computation on easy scenes and “thinks harder” in challenging scenarios, where counterfactual reasoning yields the largest error reductions. 

### **4.3. Ablation Studies** 

**Effect of meta-actions.** Table 1 has shown that adding meta-actions already improves over traj-only. Here we focus on how well the **meta-trajectory alignment** is by comparing meta-act (baseline) and meta-act (prefilled) in Table 2. Pre-filling the meta-actions with ground 

truth nearly halves the trajectory error and substantially reduces corner distance. This indicates that, once the metaactions are correct, the model already has a strong metaactions _→_ trajectory alignment, and most remaining error comes from imperfect meta-action prediction rather than the trajectory decoding. This observation motivates conducting counterfactual reasoning directly on meta-actions. 

**Effect of adaptive thinking.** We study whether the adaptive reasoning control learned by the model improves reasoning quality and action accuracy. We compare four variants: (1) CF-VLA (force no think), where reasoning is disabled by forcing the model to emit “Action:” after metaactions; (2) CF-VLA (force think), where “Thinking:” is appended after meta-actions; (3) explicit models that perform reasoning and action as two separate tasks under different user prompts; and (4) the proposed CF-VLA (adaptive), which autonomously decides whether to selfreflect. Results in Table 2 show that always thinking increases computational cost and even degrades trajectory accuracy, while never thinking underperforms on difficult scenes. The adaptive variant attains the best trade-off: lowest minADE among non-pre-filled models, higher edited IOU, and a moderate think rate, supporting that reasoning should be used selectively rather than uniformly, consistent with prior work on adaptive thinking [14]. 

**Data filtering pipeline.** We compare two CF-VLA models that differ only in this selection step. In the _Whole Dataset_ variant, reasoning traces are generated for all metaaction–labeled samples. In the _Filtered Data_ variant, CF traces are generated only for the subset that satisfies the trajectory-disagreement criterion (Sec. 3.3). The _Filtered Data_ model achieves better minADE and minFDE and a lower corner distance, despite emitting much shorter re- 

4028 


Figure 5. **Qualitative results of CF-VLA.** For three representative and safety-critical scenarios, each row shows the model’s initial metaactions ( **left** ), the reasoning trace ( **middle** ), and the updated meta-actions ( **right** ) together with the resulting trajectory. The counterfactual reasoning step identifies issues (missing lane changes, late turns, and failure to slow for pedestrians) and edits the meta-actions accordingly. 

sponses and <u>a lower</u> think rate. These results indicate that counterfactual supervision must be targeted: simply adding mo ~~re CF label~~ s and forcing the model to “think” on every scene <u>introduces</u> redundant or noisy reasoning signals, diluting the impact of informative counterfactual examples and ultimately harming the performance. The rollout–filter–label stage is therefore not merely a dataefficiency optimization, but a crucial component for extracting reliable self-reflection signals. 

**Multi-round training.** We additionally train a model on the counterfactual filtered dataset, namely using ( _D_ traj _∪D_ meta _∪ D_ CF). This model, meta-act (multi-round), is trained to predict only meta-actions and we discard the CF reasoning traces. The resulting meta-act (multi-round) in Table 2 shows that simply repeating high-value samples based on trajectory disagreement already yields a modest improvement over the single-round meta-act baseline. However, CF-VLA brings larger gains in trajectory error and IOU, indicating that learning to edit meta-actions is more effective than only reusing them as fixed labels. 

### **4.4. Qualitative Results** 

Fig. 5 visualizes the counterfactual self-reflection loop of CF-VLA in three representative scenarios. CF-VLA consistently identifies when its initial intent is misaligned with the scene and corrects it before trajectory generation. In (A) _Merging_ , the initial plan maintains speed and lane despite construction barriers and a slow van ahead, trapping 

the ego vehicle. The model opts for an early left lane change with acceleration to avoid congestion. In (B) _Turning Maneuver_ , the model identifies the stop sign and crossing traffic and corrects a late right turn that causes hesitation at the intersection, yielding a more decisive and efficient maneuver. In (C) _Vulnerable Road Users_ , the model notices a crossing pedestrian from the telephoto view and edits the dangerous actions to slow down and wait. These cases show that CF-VLA’s self-reflection produces targeted, scene-grounded corrections that improve safety, traffic efficiency, and semantic consistency. 

## **5. Conclusion** 

We introduced Counterfactual VLA (CF-VLA), a selfreflective VLA framework that critiques and corrects its own actions before execution. A rollout–filter–label counterfactual pipeline allows CF-VLA to mine its own failure cases and improve over multiple training rounds. Experiments on large-scale driving datasets show consistent gains in trajectory accuracy, safety, and reasoning quality, demonstrating up to 17.6% lower trajectory error and 20.5% lower collisions than non-reasoning baselines. The model demonstrates adaptive thinking: it reasons more in difficult, highrisk scenarios. CF-VLA thus demonstrates that counterfactual self-reflection can effectively bridge reasoning and control, offering a general paradigm for autonomous driving systems that learn to think before they act. 

4029 

## **References** 

- [1] Abbas Abdolmaleki, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Ashwin Balakrishna, Nathan Batchelor, Alex Bewley, Jeff Bingham, Michael Bloesch, et al. Gemini robotics 1.5: Pushing the frontier of generalist robots with advanced embodied reasoning, thinking, and motion transfer. _arXiv preprint arXiv:2510.03342_ , 2025. 3 

- [2] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 1 

- [3] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y Galliker, et al. _pi_ _~~{~~_ 0 _._ 5 _}_ : a vision-language-action model with open-world generalization. In _9th Annual Conference on Robot Learning_ , 2025. 1, 2, 4 

- [4] Sijia Chen and Baochun Li. Toward adaptive reasoning in large language models with thought rollback. _arXiv preprint arXiv:2412.19707_ , 2024. 3 

- [5] Xinyi Chen, Yilun Chen, Yanwei Fu, Ning Gao, Jiaya Jia, Weiyang Jin, Hao Li, Yao Mu, Jiangmiao Pang, Yu Qiao, et al. Internvla-m1: A spatially guided vision-languageaction framework for generalist robot policy. _arXiv preprint arXiv:2510.13778_ , 2025. 1 

- [6] Yuxin Chen, Jianglan Wei, Chenfeng Xu, Boyi Li, Masayoshi Tomizuka, Andrea Bajcsy, and Ran Tian. Reimagination with test-time observation interventions: Distractor-robust world model predictions for visual model predictive control. _arXiv preprint arXiv:2506.16565_ , 2025. 2, 3 

- [7] An-Chieh Cheng, Yandong Ji, Zhaojing Yang, Xueyan Zou, Jan Kautz, Erdem Biyik, Hongxu Yin, Sifei Liu, and Xiaolong Wang. Navila: Legged robot vision-language-action model for navigation. In _RSS_ , 2025. 4 

- [8] Stephen Chung, Wenyu Du, and Jie Fu. Thinker: Learning to think fast and slow. _arXiv preprint arXiv:2505.21097_ , 2025. 3 

- [9] Seyed Kamyar Seyed Ghasemipour, Ayzaan Wahid, Jonathan Tompson, Pannag Sanketi, and Igor Mordatch. Self-improving embodied foundation models. _arXiv preprint arXiv:2509.15155_ , 2025. 3 

- [10] Catherine Glossop, William Chen, Arjun Bhorkar, Dhruv Shah, and Sergey Levine. Cast: Counterfactual labels improve instruction following in vision-language-action models. _arXiv preprint arXiv:2508.13446_ , 2025. 3 

- [11] Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, YuChiang Frank Wang, and Fu-En Yang. Thinkact: Visionlanguage-action reasoning via reinforced visual latent planning. _arXiv preprint arXiv:2507.16815_ , 2025. 2, 3 

- [12] Bo Jiang, Shaoyu Chen, Qian Zhang, Wenyu Liu, and Xinggang Wang. Alphadrive: Unleashing the power of vlms in autonomous driving via reinforcement learning and reasoning. _arXiv preprint arXiv:2503.07608_ , 2025. 2 

- [13] Baicheng Li, Dong Wu, Zike Yan, Xinchen Liu, Zecui Zeng, Lusong Li, and Hongbin Zha. Reflection-based task adaptation for self-improving vla. _arXiv preprint arXiv:2510.12710_ , 2025. 3 

- [14] Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. Onetwovla: A unified visionlanguage-action model with adaptive reasoning. _arXiv preprint arXiv:2505.11917_ , 2025. 3, 7 

- [15] Zeyi Liu, Arpit Bahety, and Shuran Song. Reflect: Summarizing robot experiences for failure explanation and correction. _arXiv preprint arXiv:2306.15724_ , 2023. 3 

- [16] Yuechen Luo, Fang Li, Shaoqing Xu, Zhiyi Lai, Lei Yang, Qimao Chen, Ziang Luo, Zixun Xie, Shengyin Jiang, Jiaxin Liu, et al. Adathinkdrive: Adaptive thinking via reinforcement learning for autonomous driving. _arXiv preprint arXiv:2509.13769_ , 2025. 1, 3 

- [17] Cyrus Neary, Omar G Younis, Artur Kuramshin, Ozgur Aslan, and Glen Berseth. Improving pre-trained visionlanguage-action policies with model-based search. _arXiv preprint arXiv:2508.12211_ , 2025. 3 

- [18] NVIDIA, Yan Wang, Wenjie Luo, Junjie Bai, Yulong Cao, Tong Che, Ke Chen, Yuxiao Chen, Jenna Diamond, Yifan Ding, Wenhao Ding, Liang Feng, Greg Heinrich, Jack Huang, Peter Karkus, Boyi Li, Pinyi Li, Tsung-Yi Lin, Dongran Liu, Ming-Yu Liu, Langechuan Liu, Zhijian Liu, Jason Lu, Yunxiang Mao, Pavlo Molchanov, Lindsey Pavao, Zhenghao Peng, Mike Ranzinger, Ed Schmerling, Shida Shen, Yunfei Shi, Sarah Tariq, Ran Tian, Tilman Wekel, Xinshuo Weng, Tianjun Xiao, Eric Yang, Xiaodong Yang, Yurong You, Xiaohui Zeng, Wenyuan Zhang, Boris Ivanovic, and Marco Pavone. Alpamayo-R1: Bridging reasoning and action prediction for generalizable autonomous driving in the long tail, 2025. 1, 2, 5 

- [19] Han Qi, Haocheng Yin, Aris Zhu, Yilun Du, and Heng Yang. Strengthening generative robot policies through predictive world modeling. _arXiv preprint arXiv:2502.00622_ , 2025. 2 

- [20] Katrin Renz, Long Chen, Elahe Arani, and Oleg Sinavski. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment. In _Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 1, 2, 3 

- [21] Hao Shao, Yuxuan Hu, Letian Wang, Guanglu Song, Steven L Waslander, Yu Liu, and Hongsheng Li. Lmdrive: Closed-loop end-to-end driving with large language models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15120–15130, 2024. 2 

- [22] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 1, 2, 4 

- [23] Xiaoyu Tian, Junru Gu, Bailin Li, Yicheng Liu, Yang Wang, Zhiyong Zhao, Kun Zhan, Peng Jia, XianPeng Lang, and Hang Zhao. Drivevlm: The convergence of autonomous driving and large vision-language models. In _Conference on Robot Learning_ , pages 4698–4726. PMLR, 2025. 2, 4 

4030 

- [24] Xiangqi Wang, Yue Huang, Yanbo Wang, Xiaonan Luo, Kehan Guo, Yujun Zhou, and Xiangliang Zhang. Adareasoner: Adaptive reasoning enables more flexible thinking. _arXiv preprint arXiv:2505.17312_ , 2025. 3 

- [25] Siye Wu, Jian Xie, Yikai Zhang, Aili Chen, Kai Zhang, Yu Su, and Yanghua Xiao. Arm: Adaptive reasoning model. _arXiv preprint arXiv:2505.20258_ , 2025. 3 

- [26] Yilin Wu, Ran Tian, Gokul Swamy, and Andrea Bajcsy. From foresight to forethought: Vlm-in-the-loop policy steering via latent alignment. _arXiv preprint arXiv:2502.01828_ , 2025. 2, 3 

- [27] Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kwan-Yee K Wong, Zhenguo Li, and Hengshuang Zhao. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. _IEEE Robotics and Automation Letters_ , 2024. 2 

- [28] Zishun Yu, Tengyu Xu, Di Jin, Karthik Abinav Sankararaman, Yun He, Wenxuan Zhou, Zhouhao Zeng, Eryk Helenowski, Chen Zhu, Sinong Wang, et al. Think smarter not harder: Adaptive reasoning with inference aware optimization. _arXiv preprint arXiv:2501.17974_ , 2025. 3 

- [29] Zizheng Zhan, Ken Deng, Huaixi Tang, Wen Xiang, Kun Wu, Weihao Li, Wenqiang Zhu, Jingxuan Xu, Lecheng Huang, Zongxian Feng, et al. Kat-v1: Kwai-autothink technical report. _arXiv preprint arXiv:2507.08297_ , 2025. 

- [30] Jiajie Zhang, Nianyi Lin, Lei Hou, Ling Feng, and Juanzi Li. Adaptthink: Reasoning models can learn when to think. _arXiv preprint arXiv:2505.13417_ , 2025. 3 

- [31] Xingcheng Zhou, Xuyuan Han, Feng Yang, Yunpu Ma, and Alois C Knoll. OpenDriveVLA: Towards end-to-end autonomous driving with large vision language action model. _arXiv preprint arXiv:2503.23463_ , 2025. 2 

- [32] Zewei Zhou, Tianhui Cai, Seth Z Zhao, Yun Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. Autovla: A visionlanguage-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. _arXiv preprint arXiv:2506.13757_ , 2025. 2, 4 

4031 

