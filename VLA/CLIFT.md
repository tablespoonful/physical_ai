---
title: "CLIFT: Turning Gemini Robotics On-Device into Humanoid Specialists via Non-Invasive Closed-Loop Iterative Fine-Tuning"
date: "2026-07-31"
authors: "Yuxin Chen; Hari Srikanth; Nathan Jew; Menglin Wu; Pengcheng Wang; Junli Ren"
venue: "CoRL 2026"
url: https://arxiv.org/abs/2607.29172
pdf: https://arxiv.org/pdf/2607.29172
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.29172)** / [論文ページ](https://arxiv.org/abs/2607.29172)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **CLIFT: Turning Gemini Robotics On-Device into Humanoid Specialists via Non-Invasive Closed-Loop Iterative Fine-Tuning** 

**Yuxin Chen**<sup>1</sup> , **Hari Srikanth**<sup>1</sup> , **Nathan Jew**<sup>1</sup> , **Menglin Wu**<sup>1</sup> , **Pengcheng Wang**<sup>1</sup> , **Junli Ren**<sup>1</sup> , **Masayoshi Tomizuka**<sup>1</sup> , **Peng Xu**<sup>2</sup> , **Jinyu Xie**<sup>2</sup> , **Ran "Thomas" Tian**<sup>1</sup><sup>_,_3</sup> 

1University of California, Berkeley, 2Google DeepMind, 3NVIDIA Research 

While robot foundation models are growing increasingly capable, the strongest models are typically trained on proprietary data and have traditionally remained closed-source, limiting downstream users’ ability to adapt them to new tasks, embodiments, and deployment settings. Following the LLM community, an emerging access paradigm for closed-weight robot foundation models is the managed supervised fine-tuning (SFT) API, where users submit training data and receive a tuned policy without access to model weights, gradients, or training internals. While such APIs let downstream users leverage powerful proprietary foundation models, they restrict policy improvement to pure imitation, ruling out classical reinforcement learning and other closed-loop methods that rely on internal training signals. This limitation is particularly acute for agile, contact-rich humanoid manipulation, where the gap between policy outputs and deployed behavior is large due to novel states, action tracking dynamics, latency, and controller-specific failure modes. In this work, we study how effective this new managed-API regime is for humanoid adaptation, and how closed-loop improvement can be realized within it to push policies toward task mastery. We conduct one of the first empirical studies of managedAPI adaptation on a real humanoid, instantiated on Gemini Robotics On-Device (GROD). We found that direct SFT through the API already substantially outperforms a leading open-weight VLA trained on the same demonstrations, yet still falls short of deployment-level mastery on agile, contact-rich tasks. To close this gap, we introduce **CLIFT** : Closed-Loop Iterative FineTuning, which turns deployment-time reward feedback into API-compatible supervised data and enables closed-loop policy improvement without accessing weights, gradients, likelihoods, or losses—pushing GROD to near-perfect success after two flywheel cycles, all without “opening the model box.” 

**Keywords:** Robot Foundation Models, On-Device Closed-Loop Training 

**Website:** thomaschen98.github.io/clift 

**Code:** coming_soon 


1 


**Figure 1** | **CLIFT turns** **_closed-weight_ Gemini Robotics into a humanoid specialist. CLIFT** is an API-only, non-invasive flywheel that bridges managed SFT interfaces and closed-loop policy improvement for humanoid manipulation, without ever touching the model’s weights, gradients, or losses. Starting from an initial imitation policy, each flywheel cycle deploys the current policy to collect on-device closed-loop _rollouts_ , scores them with a preference-calibrated dense reward, and converts each rollout chunk into an SFT tuple carrying a special _advantage token_ derived from that reward. Fine-tuning on these tuples through GROD’s managed SFT API and conditioning on the positive advantage token at deployment yields the next policy, closing the flywheel. 

## **1 Introduction** 

Foundation vision-language action models (VLAs) trained on large and diverse datasets are producing robot policies with broad competence across tasks and embodiments. As these foundation VLA models grow stronger, they increasingly determine the ceiling of downstream adaptation: a stronger pretrained VLA can reduce the amount of task-specific data needed and improve generalization beyond the demonstration set [1, 2, 3, 4, 5, 6]. Yet a fundamental tension underlies this trend: _the strongest pretrained VLAs are also the least accessible_ . Many of today’s most capable robot foundation models are trained on proprietary robot data and remain as fully closed-source systems [2, 5, 6]. This creates a practical bind: the models with the highest adaptation ceiling are precisely the ones researchers cannot access. 

As the open- versus closed-source debate continues, a middle ground has emerged: _closed-weight_ models exposed through managed adaptation interfaces. In the LLM community, SFT APIs already let users customize proprietary models without accessing their weights or training pipelines [7, 8]. Robot foundation VLAs are entering this regime, where base-model access matters even more, since robot data is far harder to scale than language data [9]. Gemini Robotics On-Device (GROD) [10] is an early example—offering managed fine-tuning while keeping the “model box” closed—and Physical Intelligence’s partner API [11] signals the same trend. This positions closed-weight, API-exposed VLAs as an intermediate regime between fully closed systems and open-weight releases. 

These managed-APIs immediately enable fine-tuning on task-specific human demonstrations. However, for agile, contact-rich **humanoid tasks** , demonstration-only SFT, which remains the dominant recipe for recent humanoid VLA systems [4, 12], quickly hits a ceiling. It trains on a fixed human teleoperation distribution, while deployment occurs under the policy’s own closed-loop observation distribution. This mismatch is amplified by two factors. First, execution quality is not captured by task completion 

2 

alone: smoothness, contact quality, and safety all affect whether a humanoid execution is acceptable. Second, the VLA policy is tightly coupled to the downstream whole-body controller: the same action chunk from a policy can lead to different physical outcomes depending on tracking dynamics, latency, compliance, and contact with the environment [13]. Consistent with this limitation, recent humanoid VLA systems trained primarily through demonstration-based SFT remain far from deployment-level success rates on dexterous manipulation suites [12]. 

Crossing this ceiling requires **on-device closed-loop improvement** : the policy must practice on the actual robot–controller stack, observe its own behavior, and adapt from that feedback rather than from a fixed teleoperation set. Recent work has pursued this for robot VLAs along several axes—generating residual-RL data for SFT [14], running PPO-style RL with learned process rewards [15], and steering the policy at test time in its latent action space [16]. All of these approaches, however, reach into the learning system: they require auxiliary architectural components (e.g., critic networks or residual policy heads), modifications to the training loss, or access to internal signals such as policy gradients and action likelihoods. None of these levers are exposed by a restricted-access robot foundation model. This motivates the central question of our work: 

_How effective is the emerging managed-API access regime for humanoid adaptation, and how can closed-loop improvement be realized within this regime to push policies toward task mastery?_ 

We study this question using Gemini Robotics On-Device [10] (GROD) on an Unitree G1 humanoid across tasks with varying levels of contact, dexterity, and agility. We first evaluate direct adaptation by fine-tuning GROD on humanoid demonstrations. The resulting policy substantially outperforms a strong open-weight VLA, _𝜋_ 0 _._ 5 [17], trained on the same data, highlighting the value of a stronger closed-weight foundation model even under restricted access. However, a gap to deployment-level mastery remains, particularly on agile, contact-rich manipulation tasks. 

To close this gap, we present **CLIFT** : Closed-Loop Iterative Fine-Tuning, a non-invasive closed-loop adaptation pipeline that improves API-only robot foundation models by turning deployment experience into relabeled supervised training data. Our key insight is that **reinforcement feedback can be encoded directly into supervised training data** . Specifically, we score deployment rollouts with a preference-calibrated dense reward model and compare action chunks against chunks starting from visually similar states to estimate which behaviors are advantageous. Each rollout chunk is then converted into an SFT tuple: observation, language instruction, action chunk, and a special advantage token that encodes the alignment of the action chunk with the preference. At inference time, conditioning on the positive special advantage steers the policy toward high-quality actions. In our experiments, two flywheel cycles of CLIFT on top of GROD ultimately push the task success rate close to 100% with emergent behaviors not present in the demonstrations. As a controlled comparison, we also apply CLIFT to the open-weight _𝜋_ 0 _._ 5 model. CLIFT improves this model as well, but its absolute performance remains substantially lower under our protocol, including under the FiLM-style invasive adaptation evaluated in Sec. 4.1. 

**Contribution statement.** Our work studies an emerging setting at the intersection of two underexplored regimes: _closed-weight robot models_ , where a VLA can be adapted only by submitting SFT data to a managed fine-tuning API, and _humanoid closed-loop training_ , where VLA actions are tightly coupled to a whole-body controller. This combination amplifies the gap between demonstration learning and deployment behavior. Within this setting, we make the following contributions. First, we provide one of the first empirical studies of managed-API adaptation for a closed-weight foundation VLA on a real humanoid platform. Direct SFT through the API substantially outperforms an open-weight VLA trained on the same demonstrations, but still falls short of deployment-level mastery on agile, contact-rich tasks. Second, we introduce **CLIFT** , which turns deployment-time reward feedback 

3 

into API-compatible supervised data and enables closed-loop policy improvement without accessing weights, gradients, likelihoods, or loss functions, pushing Gemini Robotics On-Device towards task mastery after two flywheel cycles. This shows that managed SFT APIs can serve not only as customization interfaces, but also as practical interfaces for closed-loop policy improvement—offering a path toward task mastery without “opening the model box.” 

## **2 Problem Setting** 

We access a foundation VLA only through a _managed SFT interface_ , a black-box operator FSFT : D ↦→ _𝜋_ that maps a training dataset D = {( _𝑜𝑡, ℓ,_ **a** _𝑡_ )} of observation–instruction–action-chunk tuples to a fine-tuned policy _𝜋_ . It exposes no weights, gradients, losses, or action likelihoods, and is the _only_ available update operation. Our loop starts from the demonstration-trained policy _𝜋_ 0 := FSFT(Ddemo), where Ddemo is a fixed set of teleoperated demonstrations. We aim to improve _𝜋_ 0 under the closedloop distribution _𝑝𝜋_ it induces at deployment, using a preference-calibrated dense reward _𝑅𝜃_ . Formally, we target the KL-regularized objective 


where _𝛽>_ 0 anchors _𝜋_ to the initialization _𝜋_ 0 at deployment-visited states. Standard RL is incompatible with FSFT: PPO [18] needs log _𝜋_ ( _𝑎_ | _𝑜_ ) and backpropagation, and advantage-weighted regression [19] reweights losses by exp( _𝐴_ ( _𝑜, 𝑎_ )/ _𝛽_ )—neither is exposed. We instead approximate _𝜋_<sup>∗</sup> with a deployment-time data flywheel that operates entirely through D, leaving the model and training procedure untouched. 

## **3 Closed-Loop Iterative Fine-Tuning** 

Our pipeline comprises three steps: **(i)** bootstrap _𝜋_ 0 = FSFT(Ddemo) from teleoperated demonstrations; **(ii)** score rollouts with a preference-calibrated dense reward model _𝑅𝜃_ (Sec. 3.1) and label each chunk with a retrieval-based advantage token (Sec. 3.2); **(iii)** fine-tune the base model on the demonstrations and accumulated relabeled rollouts, then repeat (ii)–(iii) (Sec. 3.3). 

### **3.1 Preference-Calibrated Dense Reward Model** 

We seek a dense reward _𝑅𝜃_ ( _𝑜_ 1: _𝑇_ ; _ℓ_ ) → _𝑟_ 1: _𝑇_ that scores task progress, execution quality, and safety— the criteria a human operator uses to accept or reject a rollout. Existing approaches either prompt a zero-shot VLM [20] or train a reward model from human annotations: the former is scalable but miscalibrated toward surface progress and misses execution failures [9], while the latter is calibrated but requires prohibitive per-step labeling. We combine both via a two-stage _select-then-distill_ scheme: human preferences select calibrated rewards from VLM-generated candidates, which we then distill into a reusable reward model. We first build a comparison pool mixing human teleoperated trajectories with initial-SFT-policy rollouts, sample 100 pairs, and collect a human pairwise preference for each (which rollout better satisfies the task). For each rollout _𝑜_ 1: _𝑇_ in a sampled pair, we prompt a zero-shot VLM [20] with temperature sampling to obtain _𝐾_ candidate per-step reward sequences { _𝑟_ 1:<sup>(</sup><sup>_𝑘_</sup> _𝑇_<sup>)}</sup> _𝑘_<sup>_𝐾_</sup> =1<sup>.</sup> We keep the candidates { _𝑟_ 1:<sup>∗</sup> _𝑇_<sup>}whoseinducedcumulative-returnrankingsbestmatchthehuman</sup> preferences [9, 21], yielding dense per-step rewards that capture execution quality beyond coarse progress. Finally, we distill { _𝑟_ 1:<sup>∗</sup> _𝑇_<sup>}into a generative reward model</sup><sup>_𝑅𝜃_[15] by fine-tuning a VLM on</sup> these per-step labels; _𝑅𝜃_ then provides dense, preference-calibrated rewards across all flywheel cycles (more details on the reward model in App. B). 

4 


**Figure 2** | **Reward predictions and advantage labels on deployment rollouts.** For each rollout, the preferencecalibrated reward model _𝑅𝜃_ outputs a sequence of per-step quality scores; these are aggregated into per-chunk returns and binarized into positive/negative advantage labels via retrieval-based comparison against chunks from similar starting states. The labeling operates at the chunk level rather than the episode level: even within a successful rollout, some chunks receive negative labels for sub-optimal execution, while within a failed rollout, well-executed chunks still receive positive labels—providing fine-grained credit assignment that episode-level success/failure annotations cannot capture. 

### **3.2 Injecting Reward Signal via Retrieval-Based Advantage Conditioning** 

As the loop progresses, the policy produces rollouts of varying quality, and the next SFT cycle must know which chunks to amplify and which to suppress. We adopt the _advantage conditioning_ paradigm [5]: each action chunk is augmented with a binary token _𝐼_ ∈{positive _,_ negative} indicating whether it leads to better outcomes than alternatives from the same state. Both labels are used during SFT, and conditioning on _𝐼_ = positive at inference steers the policy toward high-quality actions. Assigning this label requires _state-aware credit assignment_ : a chunk must be judged relative to what is achievable from its starting state, since a given return may reflect excellent behavior in a hard recovery state but mediocre behavior in an easy one. 

Unlike [5], which estimates this advantage by retraining a value model each cycle from a binary success/failure reward—collapsing chunk value to a “time-to-success” measure blind to execution quality—we estimate it non-parametrically from our dense reward via retrieval. For each chunk _𝜏𝑖_ starting at _𝑡𝑖_ with initial observation _𝑜𝑡𝑖_ , we retrieve, from all rollouts, a comparison set of chunks whose initial observations are visually similar to _𝑜𝑡𝑖_ , and score _𝜏𝑖_ by its discounted return over a look-ahead window of _𝐻_ steps, _𝐺_ ( _𝜏𝑖_ ) =<sup>�</sup><sup>_𝑡_</sup> _𝑡_<sup>_𝑖_</sup> =<sup>+</sup> _𝑡𝑖_<sup>_𝐻𝛾𝑡_−</sup><sup>_𝑡𝑖𝑅𝜃_(</sup><sup>_𝑜𝑡_;</sup><sup>_ℓ_).The chunk is labeled</sup><sup>_positive_if</sup><sup>_𝐺_(</sup><sup>_𝜏𝑖_) lies</sup> in the top 30% of this set and _negative_ otherwise; because the comparison is restricted to similar states, the threshold auto-calibrates to state difficulty (details in App. C). Fig. 2 illustrates this chunk-level labeling on real rollouts. 

### **3.3 Iterative Self-Improvement** 

At each cycle _𝑘_ , we deploy _𝜋𝑘_ , score and advantage-label its rollout chunks (Sec. 3.2), and append them to a cumulative dataset D _𝑘_ = Ddemo ∪Drollout<sup>1:</sup><sup>_𝑘_, with demonstrations always labeled</sup><sup>_𝐼_= positive.</sup> Because the managed API fine-tunes the base model from scratch on each submission, we obtain _𝜋𝑘_ +1 = FSFT(D _𝑘_ ) from the base checkpoint rather than continuing from _𝜋𝑘_ —which also avoids compounding distributional drift and re-exploits the full pretrained capacity each cycle. The reward model _𝑅𝜃_ is trained once and held fixed throughout. 

5 


**Figure 3** | **Humanoid manipulation task suite.** Three contact-rich Unitree G1 tasks of increasing complexity: _Box Packing_ (single-object packing), _Cup Insertion_ (precise insertion), and _Bimanual Plate Handover_ (coordinated bimanual transfer). 

## **4 Experiments** 

We evaluate our method on a real humanoid across a diverse suite of agile, contact-rich tasks. Our experiments aim to study three questions: (1) Can our closed-loop self-improvement fine-tuning turn a API-only restricted-access foundation model into a humanoid specialist that achieves task mastery? (2) Does our pipeline generalize across different foundation models with different access regimes? (3) How does downstream performance compare between GROD and _𝜋_ 0 _._ 5 under the same self-improving fine-tuning pipeline? 

### **4.1 Experimental Setup** 

**Robot setup.** We use an Unitree G1 humanoid for experiments. The robot is equipped with dual arms, dexterous hands, and two head-mounted RGB cameras. Following [4], we adopt a hierarchical wholebody control scheme that decomposes the action space into upper-body and lower-body components: the upper-body action consists of target joint angles for the arms and hands, while the lower-body action specifies planar linear velocities and a target yaw angle. These commands are tracked by an RL-learned whole-body controller [22], which produces the full joint-level commands for execution. At each step, the policy outputs an action chunk spanning 1 _._ 6s into the future and replans after the action chunk is executed. More details can be found in App. D. 

**Tasks.** We evaluate on three contact-rich tasks on the Unitree G1 humanoid (Figure 3). Although tabletop, they are not fixed-base problems: the humanoid balances with its whole body throughout, so lower-body motions continually shift the camera viewpoint, end-effector pose, and contact geometry seen by the policy. **Box Packing** : grasp an object with the three-finger hand and place it in a box, stressing precise grasp formation and release. **Cup Insertion** : asymmetric bimanual coordination— one hand stabilizes a cup carrier while the other grasps a bottle and inserts it; small visual, contact, or torso-motion errors make the bottle collide, tilt, or miss. **Bimanual Plate Handover** : pick up a plate with one hand, transfer it to the other, and place it at a target, demanding precise inter-arm timing and stable finger contacts despite torso and base motion. 

6 

**Pre-trained VLA models for humanoid adaptation.** We apply **CLIFT** to two pre-trained VLA models that represent different access regimes. Gemini Robotics On-Device [10] is a closed-weight model exposed through a managed SFT API, while _𝜋_ 0 _._ 5 [17] is an open-weight VLA model released by Physical Intelligence, allowing direct access to model weights and training code. 

To enable a controlled comparison, we use the same teleoperated demonstrations, the same rollout collection budget at each flywheel cycle, the same preference-calibrated reward model _𝑅𝜃_ , and the reward injection procedure for both models. Both models are fine-tuned with a standard supervised loss on observation-action pairs for 10 epochs per flywheel cycle using their default fine-tuning configurations, without model-specific hyperparameter 


**Figure 4** | **Whole-body teleoperation setup.** The operator wears a VR headset, two handheld controllers, and two ankle IMU trackers, which together yield a real-time full-body SMPL pose that the whole-body controller [22] maps to robot joint commands. 

tuning. For each model, we perform two independent training runs and select the run with the lowest held-out demonstration loss as the final model. While the two foundation models also differ in architecture and scale, which our experiments cannot independently isolate, these controls ensure that any observed performance gap is not driven by mismatches in our adaptation training data, optimization procedure, or evaluation protocol. 

**Human demonstration collection.** We collect demonstrations via whole-body VR teleoperation (Figure 4). During each demonstration, we record the egocentric camera image, proprioceptive state, and executed actions to form training trajectories. For each task, we collect 2 hours of human teleoperated data. More details on demonstration collection can be found in App. D. 

**CLIFT protocol and evaluation.** We initialize _𝜋_ 0 by fine-tuning the base model on 2 hours of teleoperated demonstrations per task, and train the preference-calibrated reward model from 100 human pairwise comparisons over these demonstrations and initial SFT rollouts (Sec. 3.1). We then run 2 cycles of **CLIFT** (Sec. 3.3). A key property of the on-device setting is that deployment and evaluation coincide: each cycle deploys the current policy for 100 rollouts per task under a fixed evaluation suite, and these same rollouts both define its success rate and, once relabeled, form the training data for the next cycle. More details on evaluation can be found in App. E. 

### **4.2 Results** 

**CLIFT effectively turns GROD into a humanoid specialist that achieves task mastery.** We apply **CLIFT** to GROD following the protocol described in Sec. 4.1, and evaluate two API-compatible variants. In the _dense advantage-conditioned_ variant, every action chunk in the deployment rollouts is scored by the preference-calibrated reward model, assigned a positive or negative advantage label via retrieval-based comparison, and included in the next SFT dataset. In the _high-return episode selection_ variant, we use a DAgger-style data selection rule: deployment rollouts are ranked by accumulated reward, and only advantageous rollouts (top 30%) are added to the next SFT dataset. The two variants differ along two axes: the dense variant operates at the _chunk_ level and conditions on positive and negative advantage labels, whereas the episode-selection variant operates at the _rollout_ level, performing filtered imitation on the top-30% highest-return rollouts and discarding the rest. 

Figure 5 reports GROD’s success rate over the two flywheel cycles. Both variants improve the 

7 


**Figure 5** | **CLIFT lifts humanoid manipulation policies across foundation models and access regimes.** Success rate (%, over 100 trials) across two flywheel cycles on three humanoid tasks. Applied to Gemini Robotics On-Device, both **CLIFT** iteratively improves the demonstration-trained baseline, reaching higher performance at each cycle. The same pipeline also improves the open-weight _𝜋_ 0 _._ 5, but plateaus at a substantially lower ceiling. An _invasive_ adaptation of _𝜋_ 0 _._ 5 that injects the preference signal directly via FiLM-style conditioning (an architectural change) still does not close the gap to GROD. 

demonstration-trained policy at every cycle on all three tasks. The dense advantage-conditioned variant is strongest, lifting GROD from its SFT baseline to near-task mastery: 93% → 100% on Box Packing, 70% → 98% on Cup Insertion, and 53% → 96% on Bimanual Plate Handover—all through API-only access, with no additional human demonstrations. 

Interestingly, the two variants are comparable on Box Packing and Cup Insertion, both approaching perfect success, but diverge sharply on the hardest task, Bimanual Plate Handover, where the dense variant reaches 96% versus only ∼ 84% for episode selection. The two variants collect the same rollouts and differ only in what enters the next SFT dataset: episode selection keeps the top-30% highest-return rollouts and _discards the rest_ , whereas the dense variant retains every rollout and labels its chunks by advantage. On easy tasks, successful rollouts are plentiful, so discarding the low-return ones costs little and the two variants match. On hard tasks, however, successes are rare and most collected rollouts are failures—precisely the data that episode selection throws away. By instead retaining these failed rollouts and relabeling them at the chunk level, the dense variant recovers well-executed chunks as positive examples and exploits poorly-executed ones as contrastive negatives, converting failure into usable training signal (Fig. 2). The gain on Bimanual Plate Handover therefore comes specifically from learning from failed rollouts, rather than from successful trajectories alone. 

**CLIFT can adapt different foundation models to humanoid tasks.** To test whether **CLIFT** generalizes beyond GROD, we apply the identical pipeline—the same reward model _𝑅𝜃_ , rollout budget, and advantage relabeling—to the open-weight _𝜋_ 0 _._ 5 [17], which differs from GROD in architecture, pretraining scale, and access regime. **CLIFT** improves _𝜋_ 0 _._ 5 as well: over two flywheel cycles, success rate rises from 59% to 76% on Box Packing, 50% to 56% on Cup Insertion, and 5% to 30% on Bimanual Plate Handover. The same non-invasive mechanism therefore transfers across foundation models and access regimes, even though the absolute performance _𝜋_ 0 _._ 5 attains remains well below GROD—a gap we examine next. 

**Foundation model choice matters, even under API-only adaptation. CLIFT** improves both foundation models, but the absolute ceiling it reaches is set by the strength of the pretrained prior. _𝜋_ 0 _._ 5 builds on a PaliGemma backbone [23], whereas GROD builds on Gemma, pretrained on substantially larger and more diverse corpora. With the same pipeline and the same demonstrations, the policy initialized from the more extensively pretrained model attains higher success at _every_ flywheel cycle, and the gap widens with task difficulty: on the most agile, contact-rich tasks, Gemini reaches 84% 

8 


**Figure 6** | **Emergent behaviors after closed-loop fine-tuning.** By the final flywheel cycle, GROD exhibits behaviors not present in the teleoperated demonstrations. _Top (Box Packing):_ the policy reorients the box with its fingers and wrist to set up an easier grasp before lifting. _Bottom (Cup Insertion):_ the policy recovers from a failed first insertion attempt and succeeds on a second try, rather than aborting. 

versus _𝜋_ 0 _._ 5’s 46% on Bimanual Plate Handover, and 88% versus 46% on Cup Insertion. Critically, this gap does not stem from the API-only restriction. Even when _𝜋_ 0 _._ 5 is granted _invasive_ adaptation that injects the preference signal directly into the network via FiLM-style conditioning [24] (more details in App. F)—a lever **CLIFT** deliberately forgoes—it still trails Gemini adapted through the API alone (e.g., 40% vs. 84% on Bimanual Plate Handover, 48% vs. 93% on Cup Insertion). A stronger model adapted through a narrow SFT interface thus outperforms a weaker model granted full internal access. We evaluate a single invasive baseline and do not claim to rule out the broader space of full-access methods. Still, the pattern is consistent: the gap tracks pretrained capability rather than the level of training access. This is precisely the positioning of our introduction—when closed-loop adaptation is the bottleneck, the choice of base model can matter as much as the access regime, which is why securing API access to the strongest closed-weight foundation models is worthwhile even when their internals remain hidden. Though we only showed three representative tasks in Fig. 6, a detailed benchmarking between GROD and _𝜋_ 0 _._ 5 can be found in this interactive server at our Project Website. 

**Closed-loop practice elicits emergent behaviors absent from demonstrations.** The advantage of a stronger base model also shows up qualitatively. By the final flywheel cycle, GROD acquires corrective and pre-manipulation behaviors that never appear in the teleoperated demonstrations (Fig. 6). On Box Packing, the policy learns to first nudge and reorient the box with its fingers and wrist to set up an easier grasp, rather than grasping it in whatever pose it starts in. On Cup Insertion, it acquires a retry behavior: when the first insertion attempt fails, the policy re-approaches and succeeds on a second attempt instead of stalling. Because **CLIFT** reinforces high-return chunks recovered from the policy’s _own_ rollouts—including chunks salvaged from failed episodes—closed-loop practice does more than imitate demonstrated motions; it composes new behavior beyond the demonstration distribution, and a stronger pretrained prior is better able to acquire it. 

## **5 Conclusion** 

While robot foundation models grow increasingly capable, the strongest are typically trained on proprietary data and exposed only through managed supervised fine-tuning (SFT) APIs—users submit training data and receive a tuned policy, with no access to model weights, gradients, or training internals. In this work, we studied how effective this managed-API regime is for humanoid adaptation, and how closed-loop improvement can be realized within it to push policies toward task mastery. We provided one of the first empirical studies of managed-API adaptation on a real humanoid, instantiated 

9 

on Gemini Robotics model. Direct SFT through the API already substantially outperforms a leading open-weight VLA trained on the same demonstrations, yet still falls short of deployment-level mastery on agile, contact-rich tasks. To close this gap, we introduced **CLIFT** : Closed-Loop Iterative FineTuning, which turns deployment-time reward feedback into API-compatible supervised data and enables closed-loop policy improvement without accessing weights, gradients, likelihoods, or lossespushing Gemini Robotics model to near-perfect success after two flywheel cycles, all without “opening the model box.” 

**Limitations. CLIFT** relies on real-robot rollouts at each cycle to inject real-world deployment signal into the policy. This signal is especially valuable for complex embodiments, where coupling to a whole-body controller induces a large gap between a policy’s predicted actions and its deployed behavior; at the same time, such rollouts are costly and safety-sensitive to collect on hardware. We are excited to integrate a control-aware world model that anticipates deployment outcomes, reducing the number of risky real-robot rollouts required per cycle. In addition, we only evaluated one open-weight model and will expand the comparison to more open-weight models in future work. 

10 

## **References** 

- [1] Open X-Embodiment Collaboration. Open X-embodiment: Robotic learning datasets and RT-X models. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903, 2024. 

- [2] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- [3] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [4] Songlin Wei, Hongyi Jing, Boqian Li, Zhenyu Zhao, Jiageng Mao, Zhenhao Ni, Sicheng He, Jie Liu, Xiawei Liu, Kaidi Kang, et al. _𝜓_ 0: An open foundation model towards universal humanoid loco-manipulation. _arXiv preprint arXiv:2603.12263_ , 2026. 

- [5] Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Gavin Connors, James Darpinian, Karan Dhabalia, Joseph DiCarlo, Danny Driess, et al. _𝜋_<sup>∗</sup> 0 _._ 6<sup>:a VLA that learns from experience.</sup> _arXiv preprint arXiv:2511.14759_ , 2025. 

- [6] Figure AI. Helix: A vision-language-action model for generalist humanoid control, 2025. 

- [7] OpenAI. Fine-tuning – openai api documentation, 2025. Accessed: 2026-04-13. 

- [8] Google Cloud. About supervised fine-tuning for Gemini models – Vertex AI documentation, 2025. Accessed: 2026-04-13. 

- [9] Ran Tian, Yilin Wu, and Andrea Bajcsy. Position: Good embodied reward models need bad behavior data. In _International Conference on Machine Learning (ICML)_ , 2026. 

- [10] Google DeepMind. Gemini robotics on-device, 2025. Private preview, available via Trusted Tester Program. Accessed: 2026-04-13. 

- [11] Physical Intelligence. The physical intelligence layer, February 2026. Accessed: 2026-04-13. 

- [12] Zhenyu Zhao, Hongyi Jing, Xiawei Liu, Jiageng Mao, Abha Jha, Hanwen Yang, Rong Xue, Sergey Zakharov, Vitor Guizilini, and Yue Wang. Humanoid everyday: A comprehensive robotic dataset for open-world humanoid manipulation. _arXiv preprint arXiv:2510.08807_ , 2025. 

- [13] Antonia Bronars, Younghyo Park, and Pulkit Agrawal. Tune to learn: How controller gains shape robot policy learning. _arXiv preprint arXiv:2604.02523_ , 2026. 

- [14] Wenli Xiao, Haotian Lin, Andy Peng, Haoru Xue, Tairan He, Yuqi Xie, Fengyuan Hu, Jimmy Wu, Zhengyi Luo, Linxi Fan, Guanya Shi, and Yuke Zhu. Self-improving vision-language-action models with data generation via residual RL. _arXiv preprint arXiv:2511.00091_ , 2025. 

- [15] Huajie Tan et al. Robo-Dopamine: General process reward modeling for high-precision robotic manipulation. _arXiv preprint arXiv:2512.23703_ , 2025. 

- [16] Andrew Wagenmaker, Mitsuhiko Nakamoto, Yunchu Zhang, Seohong Park, Waleed Yagoub, Anusha Nagabandi, Abhishek Gupta, and Sergey Levine. Steering your diffusion policy with latent space reinforcement learning. _arXiv preprint arXiv:2506.15799_ , 2025. 

- [17] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, et al. _𝜋_ 0 _._ 5: a 

11 

vision-language-action model with open-world generalization. In _Proceedings of the 9th Conference on Robot Learning (CoRL)_ , volume 305, pages 17–40. PMLR, 2025. 

- [18] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [19] Xue Bin Peng, Aviral Kumar, Grace Zhang, and Sergey Levine. Advantage-weighted regression: Simple and scalable off-policy reinforcement learning. _arXiv preprint arXiv:1910.00177_ , 2019. 

- [20] Yecheng Jason Ma, Joey Hejna, Chuyuan Fu, Dhruv Shah, Jacky Liang, Zhuo Xu, Sean Kirmani, Peng Xu, Danny Driess, Ted Xiao, Osbert Bastani, Dinesh Jayaraman, Wenhao Yu, Tingnan Zhang, Dorsa Sadigh, and Fei Xia. Vision language models are in-context value learners. In _International Conference on Learning Representations (ICLR)_ , 2025. 

- [21] Ran Tian, Yilin Wu, Chenfeng Xu, Masayoshi Tomizuka, Jitendra Malik, and Andrea Bajcsy. Maximizing alignment with minimal feedback: Efficiently learning rewards for visuomotor robot policy alignment. _arXiv preprint arXiv:2412.04835_ , 2024. 

- [22] Unitree Robotics. XR-Teleoperate: An open-source teleoperation framework and data collection toolkit for embodied intelligence. https://github.com/unitreerobotics/xr_teleoperate, 2024. Accessed: 2026-02. 

- [23] Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. PaliGemma: A versatile 3B VLM for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- [24] Ethan Perez, Florian Strub, Harm de Vries, Vincent Dumoulin, and Aaron Courville. FiLM: Visual reasoning with a general conditioning layer. In _AAAI Conference on Artificial Intelligence_ , 2018. 

- [25] Oriane Siméoni, Huy V Vo, Maximilian Seitzer, Federico Baldassarre, Maxime Oquab, Cijo Jose, Vasil Khalidov, Marc Szafraniec, Seungeun Yi, Michaël Ramamonjisoa, et al. Dinov3. _arXiv preprint arXiv:2508.10104_ , 2025. 

- [26] Kevin Frans, Seohong Park, Pieter Abbeel, and Sergey Levine. Diffusion guidance is a controllable policy improvement operator. _arXiv preprint arXiv:2505.23458_ , 2025. 

12 

# Appendix 

## **A Related Work** 

**Closed-weight API-exposed foundation models** . Despite the rapid progress of open-source models, many of the most capable large language models and vision-language models remain closed-weight, as they are typically trained on proprietary datasets and supported by large-scale proprietary training infrastructure. As a result, downstream users often lack direct access to model weights and training pipelines. While the debate between open-source and closed-source models continues, the community has increasingly explored ways for downstream users to benefit from powerful closed-source models beyond inference alone. One emerging path is to expose managed adaptation interfaces, such as supervised fine-tuning APIs, that enable limited customization without releasing model weights or full training pipelines. Robot foundation models are beginning to enter this regime as well, but in a form where access to strong base models is arguably even more critical. Gemini Robotics On-Device [10] and Physical Intelligence’s partner API [11] are early examples of this model form in robotics: rather than exposing model weights, they provide managed fine-tuning interfaces that allow downstream users to adapt the underlying model on custom data while keeping the model internals and training pipeline inaccessible. This positions both as an intermediate model-access regime in robotics, bridging fully closed proprietary systems and open-weight robot foundation models. In this paper, we conduct the first study of how a closed-weight robot foundation model, accessed only through a managed fine-tuning API, can be specialized for challenging humanoid deployment settings. 

**Vision-Language-Action models for humanoid manipulation** . Vision-language-action (VLA) models have emerged as a dominant paradigm for instruction-following robot policies, leveraging large-scale pre-trained vision-language backbones to enable broad task and embodiment generalization [1, 17]. More recently, this paradigm has been extended to humanoid platforms, with models such as GR00T N1 [3], Ψ0 [4], and Helix [6] bringing VLA-style architectures to whole-body control, supported by growing efforts toward large-scale humanoid manipulation datasets [12]. However, these models are typically trained through supervised behavior cloning on expert teleoperation data—an imitation-only paradigm that fundamentally caps performance at demonstration quality and coverage. For agile, contact-rich humanoid tasks, where expert demonstrations are expensive to collect at scale and inherently noisy, this leaves a substantial gap between training and deployment-level mastery. In the paper, we study how to push humanoid VLAs beyond this demonstration-trained ceiling through deployment-time self-improvement, particularly under the constraint of API-only adaptation. 

**On-device closed-loop policy improvement for robot VLAs** . Imitation learning alone is often insufficient for robot deployment because it trains on a fixed demonstration distribution while inference occurs under the policy’s own closed-loop state distribution. This mismatch becomes more severe when preferences extend beyond task completion to execution quality, safety, and interaction with the low-level controller: the same high-level action can lead to different physical outcomes depending on tracking dynamics, latency, compliance, and contact with the environment [13]. These issues are particularly salient for humanoids, where a VLA policy must coordinate dexterous hands and upper-body motion while acting through a downstream whole-body controller. Closed-loop policy improvement addresses this mismatch by letting the policy practice, observe and learn from its own failures and partial successes. Recent work has shown that deployment experience can improve robot VLAs through residual-RL data generation [14], PPO-style RL with learned process rewards [15], and latent-space test-time policy steering [16]. However, these approaches typically assume invasive access to the learning system, such as trainable critics or residual policies, loss reweighting, policy gradients, or action likelihoods. They also primarily target embodiments whose action interfaces are 

13 

substantially simpler: fixed-base manipulators or low-DoF grippers where the gap between the VLA action chunk prediction and the deployment-time result is comparatively narrower. In contrast, our work studies closed-loop policy improvement at the intersection of two emerging but underexplored regimes: a restricted model-access regime, where the only available update operation is managed SFT, and a complex embodiment regime, where humanoid policies must coordinate dexterous manipulation through a whole-body controller. We express the improvement signal entirely as SFT-compatible data, enabling deployment-time self-improvement without modifying model internals. 

## **B Reward Model Implementation Details** 

We seek a dense reward _𝑅𝜃_ ( _𝑜_ 1: _𝑇_ ; _ℓ_ ) → _𝑟_ 1: _𝑇_ that scores task progress, execution quality, and safety— the criteria a human operator uses to accept or reject a rollout. Existing approaches either prompt a zero-shot VLM [20] or train a reward model from human annotations: the former is scalable but miscalibrated toward surface progress and misses execution failures [9], while the latter is calibrated but requires prohibitive per-step labeling. We combine both via a two-stage _select-then-distill_ scheme: human preferences select calibrated rewards from VLM-generated candidates, which we then distill into a reusable reward model. 

_Collecting human preferences._ To calibrate the reward model, we collect a small set of human pairwise preferences. We build a comparison pool that mixes human teleoperated trajectories (including failed attempts) with rollouts from the initial SFT policy, so that it spans the full spectrum of behavior quality, and sample 100 rollout pairs from it. Each pair is presented to a single expert evaluator as a synchronized, side-by-side replay from three viewpoints—the robot’s two egocentric head cameras (regular and wide-angle) and an external third-person view—so that both the fine manipulation and the whole-body motion are visible. Given the task description, the evaluator marks the rollout that better accomplishes the task while also exhibiting cleaner grasps, smoother motion, and safer contacts, yielding 100 rollout-level pairwise preference labels. 

_Generating and selecting preference-consistent rewards._ To obtain dense per-step rewards for the human-labeled rollouts, we use a VLM as a generator of candidate reward sequences, following the generative reward-modeling framework of [20]. For each rollout, we prompt the VLM (GPT-5.5) with the task description and the rollout frames and draw _𝐾_ = 12 candidate per-step reward sequences { _𝑟_ 1:<sup>(</sup><sup>_𝑘_</sup> _𝑇_<sup>)}12</sup> _𝑘_ =1<sup>under temperature sampling.The full prompt template is shown below, with task-specific</sup> content filled into the placeholders {TASK_INSTRUCTION}, {RUBRIC}, and {HARD_FAILURES}. 

Generative Reward Modeling Template 

You are an expert reward labeler for robot manipulation videos. 

TASK: {TASK_INSTRUCTION} 

REWARD RUBRIC (anchor scores in [0, 100]; interpolate between them): - 0: No relevant action; robot has not engaged with the task {RUBRIC} 

HARD FAILURES (override the rubric — if any condition below is visible in a frame, that frame’s task_reward MUST be 0, no matter what milestone was reached earlier): {HARD_FAILURES} 

14 

You will be shown _𝑁_ frames sampled from a robot rollout. The order has been shuffled — ignore frame order and judge each frame purely on its visual content. Each frame is labeled with a “frame_index” matching the order shown. 

Now label these _𝑁_ frames of the rollout and the reason for the score: Frame 1: `〈` image `〉` Frame 2: `〈` image `〉` . . . Frame _𝑁_ : `〈` image `〉` 

OUTPUT FORMAT — return a single JSON array of length _𝑁_ with one object per frame, in the SAME ORDER the frames were shown: [ {"frame_index": 1, "task_reward": `〈` int 0..100 `〉` , "frame_description": " `〈` one short sentence `〉` "}, {"frame_index": 2, "task_reward": `〈` int 0..100 `〉` , "frame_description": " `〈` one short sentence `〉` "}, . . . ] Output ONLY the JSON array. No prose, no markdown fences. 

_Placeholder semantics._ Each placeholder captures one axis of user-specified, task-level preference: 

- {TASK_INSTRUCTION}: a one- or two-sentence natural-language description of the task goal. 

- {RUBRIC}: a list of progress milestones, each tied to an anchor score in [0 _,_ 100]. The model linearly interpolates between anchors for intermediate frames. 

- {HARD_FAILURES}: a list of visually-checkable failure conditions that override the rubric and force _𝑟𝑡_ = 0, used to prevent partial credit for frames where a milestone was momentarily reached but the resulting state is actually a failure. 

Each of the _𝐾_ = 12 candidates assigns its own rollout a cumulative return; a single candidate therefore scores only the rollout it was generated for, not the entire pair set. Rather than labeling each pair independently, we choose one candidate sequence _per rollout_ so as to maximize the number of human-labeled pairs whose induced returns agree with the preference—writing _𝐺𝑋_<sup>(</sup><sup>_𝑘_)</sup> for the return of candidate _𝑘_ on rollout _𝑋_ , a pair _𝐴_ ≻ _𝐵_ agrees when the selected _𝐺 𝐴 > 𝐺𝐵_ [9, 21]. The resulting dense per-step labels { _𝑟_ 1:<sup>∗</sup> _𝑇_<sup>}are the distillation targets for the reward model</sup><sup>_𝑅𝜃_trained next.</sup> 

_Reward model training._ We instantiate _𝑅𝜃_ as a vision–language model that takes the rollout frames together with the task instruction and predicts a per-step scalar reward. We use Qwen3-VL as the backbone and regress its predicted per-step rewards onto the preference-selected dense labels { _𝑟_ 1:<sup>∗</sup> _𝑇_<sup>}</sup> under a mean-squared error loss. We pool the labeled data from _all_ tasks into a single training set and train one shared reward model rather than a per-task model: this lets _𝑅𝜃_ exploit notions of grasp quality, smoothness, and safety that transfer across tasks, and amortizes the human-preference budget over the whole suite. The same _𝑅𝜃_ then scores rollouts for every task and is held fixed across all flywheel cycles. Concretely, the training set comprises the ≈ 200 rollouts that make up the 100 preference pairs, each labeled with its VLM-selected dense reward; from each rollout we uniformly subsample 32 frames and resize them to the backbone’s native input resolution. We attach LoRA adapters of rank 128 ( _𝛼_ = 256, dropout 0 _._ 05) and optimize with AdamW (learning rate 1 × 10<sup>−4</sup> , 

15 

weight decay 0 _._ 01, cosine decay with a short linear warmup) for 5 epochs at an effective batch size of 32. 

## **C Retrieval and Advantage Labeling Details** 

Recall from Sec. 3.2 that the dense reward _𝑅𝜃_ is not directly a learning signal: the same return can reflect excellent behavior in a hard state but mediocre behavior in an easy one, so each chunk must be judged _relative to what is achievable from the state it started in_ . Rather than learn a value function for this baseline, we estimate it non-parametrically—retrieving chunks that began in visually similar states and ranking the current chunk against them to assign its advantage token. 

_Observation encoder._ We embed every frame of every rollout with a frozen, pre-trained vision encoder _𝜙_ (·) ∈ ℝ<sup>_𝑑_</sup> and _ℓ_ 2-normalize the output, so all embeddings live on the unit sphere ∥ _𝜙_ (·)∥2 = 1. By default _𝜙_ is DINOv3 (ViT-S/16, _𝑑_ =384) [25]. 

_Visual similarity and comparison set._ For a query chunk _𝜏𝑖_ , our goal is to gather _peer chunks_ from other rollouts that began in a visually similar state, so that their returns form a baseline against which _𝜏𝑖_ can be judged. We measure state similarity in embedding space: each observation _𝑜_ is encoded by the frozen vision encoder _𝜙_ and _ℓ_ 2-normalized, so that sim( _𝑜, 𝑜_<sup>′</sup> ) = ⟨ _𝜙_ ( _𝑜_ ) _, 𝜙_ ( _𝑜_<sup>′</sup> )⟩ is the cosine similarity between two states. Let _𝑜𝑡𝑖_ be the _query observation_ —the initial frame of _𝜏𝑖_ , taken from rollout _𝑒𝑖_ . We build the comparison set _one donor rollout at a time_ . Within each other rollout _𝑒_ ≠ _𝑒𝑖_ , we locate the single frame whose observation is most similar to the query, 


and admit that rollout only if this best match is close enough, sim( _𝑜_<sup>_𝑒_</sup> _𝑚𝑒_<sup>_,𝑜𝑡_</sup> _𝑖_<sup>)≥</sup><sup>_𝛿_.Restrictingeach</sup> rollout to its _single_ best frame prevents one trajectory—whose temporally adjacent frames are nearly identical—from flooding the set with near-duplicate neighbors. Every admitted rollout then contributes exactly one peer chunk, the sub-trajectory _𝜏_<sup>(</sup><sup>_𝑒_)</sup> that starts at its matched frame _𝑚𝑒_ : 


By construction, every chunk in N ( _𝜏𝑖_ ) starts from a state visually close to _𝑜𝑡𝑖_ ; the chunks therefore differ mainly in _what the policy did afterward_ , which is precisely the comparison needed to estimate _𝜏𝑖_ ’s advantage (next paragraph). The threshold _𝛿_ is a single global value, tuned so that each comparison set holds |N| neighbors on average. Figure 7 shows, for each task, a query observation alongside the most similar observations retrieved by this procedure. 

_Advantage token labeling._ Given the comparison set N ( _𝜏𝑖_ ) built above, we score every chunk by its discounted return over a fixed look-ahead window of _𝐻_ steps from its start, 


with discount factor _𝛾_ and a look-ahead horizon _𝐻_ spanning 1 _._ 8 seconds of future observations. We then assign _𝜏𝑖_ a binary advantage token by ranking its return _within_ its comparison set: it is labeled _positive_ if _𝐺_ ( _𝜏𝑖_ ) lies in the top 30% of the neighbors’ returns and _negative_ otherwise, 


16 


**Figure 7** | **Retrieved similar states for advantage estimation.** For each task (rows, top to bottom: Box Packing, Cup Insertion, Bimanual Plate Handover), we show a _query observation_ (left) and the _top-3 most similar observations_ (right) retrieved from other rollouts via cosine similarity of DINOv3 embeddings. The retrieved states closely match the query in arm pose, object placement, and contact configuration, confirming that the retrieval recovers genuinely comparable states against which chunk returns can be ranked. 

Because every chunk in N ( _𝜏𝑖_ ) started from a state visually similar to _𝑜𝑡𝑖_ , this percentile threshold adapts to state difficulty: in hard states where most attempts fail, a modest return still earns a positive token, whereas in easy states the bar is correspondingly higher. 

## **D Robot Setup** 

_Hardware._ All experiments use the Unitree G1 humanoid, which is equipped with two arms, two dexterous multi-fingered hands, and a head carrying two RGB cameras (a regular and a wide-angle lens) that together provide egocentric visual observation of both the workspace and the surrounding scene. 

_Action space and whole-body control._ Following [4], we adopt a hierarchical whole-body control scheme that decomposes the action space into upper-body and lower-body components. The upperbody action consists of target joint angles for the two arms and hands, while the lower-body action specifies planar linear velocities and a target yaw angle. These high-level commands are tracked by an RL-learned whole-body controller [22], which converts them into the full set of joint-level commands executed on the robot. This decomposition lets the VLA policy issue coarse, task-relevant targets while the low-level controller maintains balance and handles joint-level tracking. 

17 

_Observation space._ The policy observation _𝑜𝑡_ comprises the two head-camera images ( _𝐼𝑡_<sup>1</sup><sup>_, 𝐼_</sup> _𝑡_<sup>2)—regular</sup> and wide-angle—together with the whole-body proprioceptive state _𝑞𝑡_ , which includes the upper-body joint positions and the torso roll, pitch, and yaw as well as the base height. 

_Policy deployment._ At each control step the policy outputs an action chunk spanning 1 _._ 6 seconds into the future and replans after the chunk has been executed. All policy variants are deployed through a shared deployment function for fair comparison: at each query we condition the policy on _𝐼_ = positive and apply classifier-free guidance [26] with scale _𝛽_ = 0 _._ 2 to amplify its preference toward high-quality actions. The same deployment configuration—action-chunk length, replanning, conditioning token, and guidance scale—is used for every variant evaluated in this paper, so that performance differences arise solely from the training procedure rather than deployment-time choices. 

## **E Evaluations** 

### **E.1 Invasive fine-tuning baseline** 

The _𝜋_ 0 _._ 5 action expert is conditioned on a single AdaRMSNorm vector **c** ada ∈ ℝ<sup>_𝑑_</sup> produced from the flow-matching timestep and broadcast to every layer. We compute a per-sample FiLM modulator of **c** ada from the advantage indicator _𝐼𝑡_ : 


where _𝐸_ adv ∈ ℝ<sup>3×</sup><sup>_𝑑_</sup> is the indicator embedding vector, _𝑊_ 1<sup>adv</sup> ∈ ℝ<sup>_𝑑_×</sup><sup>_𝑑_</sup> and _𝑊_ 2<sup>adv</sup> ∈ ℝ<sup>_𝑑_×2</sup><sup>_𝑑_</sup> are the modulator weights. Specifically, _𝑊_ 2<sup>adv</sup> are initialized to zero, giving _𝜸_ = _𝜷_ = **0** at step 0, so _𝜋_<sup>Adv</sup> 0 _._ 5<sup>is identical to the</sup> loaded _𝜋_ 0 _._ 5 checkpoint at the start of every flywheel cycle. The modulated **c** ada replaces the original at every AdaRMSNorm site of the action expert. 

To include the case with no advantage prompt input, we extend _𝐸_ adv to three rows and route unlabeled chunks through a learnable _neutral_ class: 


All three classes use the same head and produce distinct modulators, so the model sees a single objective everywhere. We let the neutral class _𝐼𝑡_ =2 (neutral) play the role of the unconditional branch by giving unlabeled chunks their own embedding row. Training is therefore a single flow-matching pass with no indicator dropout and no auxiliary term: 


where _𝑣𝜃_ is the predicted action-chunk velocity, _𝑢𝜏_ is the flow-matching target, and _𝐼𝑡_ is the per-sample three-class indicator parsed from the prompt suffix. At inference the policy always conditions on _𝐼𝑡_ =1 (positive) with a single suffix pass. The invasive baseline is run under the same training and iteration setup as the non-invasive _𝜋_ 0 _._ 5+CLIFT entry. Every cycle re-initializes _𝜋_<sup>Adv</sup> 0 _._ 5<sup>from the public</sup> _𝜋_ 0 _._ 5 checkpoint, with the three FiLM modules initialized from scratch. 

### **E.2 Evaluation protocol** 

Evaluating manipulation policies on real hardware is an open problem. Unlike simulation, real rollouts cannot be reset to identical states, and small differences in initial object placement, lighting, or hardware wear can change task difficulty considerably. When different models or methods are 

18 


**Figure 8** | **Fixed evaluation configurations.** Initial scene layouts used to evaluate every model, variant, and flywheel cycle, varying object positions and orientations. Each task uses its own fixed set: 6 for Box Packing, 10 for Cup Insertion, and 5 for Bimanual Plate Handover. The same configurations are reused identically across all comparisons. 

each tested under their own loosely controlled conditions, the resulting success rates carry large, uncontrolled variance that can easily swamp the true performance differences between methods. 

To control this variance, we fix the evaluation conditions and share them across all comparisons. For each task we define a fixed set of evaluation configurations—6 for Box Packing, 10 for Cup Insertion, and 5 for Bimanual Plate Handover (Fig. 8). A configuration pins down the initial scene layout—the starting poses of the manipulated objects and their targets—and the configurations are chosen to span the workspace and the range of difficulty the policy must handle. Crucially, the _same_ configurations are reused identically for every model, every variant, and every flywheel cycle reported in this paper, so that differences in success rate reflect the policy under test rather than the luck of its initial conditions. 

In each flywheel cycle we run 100 rollouts per task under identical conditions, distributed across that task’s configurations, and report the average success rate per task. Before each rollout the scene is reset to its configuration’s layout, and the rollout is scored as a binary success or failure against a fixed, task-specific criterion. Because deployment and evaluation coincide in our on-device setting, these same rollouts also serve as the data relabeled for the next flywheel cycle (Sec. 3.3). All policies 

19 


**Figure 9** | **Representative** _𝜋_ 0 _._ 5 **failures.** Both tasks exhibit the same failure mode: the policy executes its scripted motion regardless of whether the underlying manipulation actually succeeded. _Top (Cup Insertion):_ the policy grasps the bottle (1), the grasp slips and the bottle tips over (2), yet the policy continues the insertion motion with an empty hand (3). _Bottom (Bimanual Plate Handover):_ the policy reaches to pick a plate (1), the pick fails (2), yet it proceeds to the handover empty-handed (3). This lack of reactivity to closed-loop feedback is a recurring failure mode for _𝜋_ 0 _._ 5. 

are run with the identical deployment configuration, so performance differences arise solely from training rather than deployment-time choices. 

## **F Additional Results** 

As shown in the main results (Fig. 5), applying the identical **CLIFT** pipeline—same reward model, rollout budget, advantage relabeling, and evaluation suite—to the open-weight _𝜋_ 0 _._ 5 improves it at every cycle but plateaus at a substantially lower ceiling than GROD, with the gap largest on the most contact-rich tasks. To understand where this gap comes from, we qualitatively examine _𝜋_ 0 _._ 5’s rollouts. 

_𝜋_ 0 _._ 5 _is less reactive to closed-loop feedback._ A recurring failure mode is that _𝜋_ 0 _._ 5’s actions do not track what is actually happening in the scene. When an initial grasp slips or misses, the policy frequently proceeds through the rest of the motion as if the grasp had succeeded—lifting and transporting an empty hand—instead of re-attempting the grasp. GROD, by contrast, more often detects the failed grasp and retries before continuing (cf. the emergent recovery behavior in Fig. 6). 

_𝜋_ 0 _._ 5 _shows weaker emergent behavior._ Relatedly, _𝜋_ 0 _._ 5 exhibits fewer of the corrective and premanipulation behaviors that emerge in GROD by the final flywheel cycle (Fig. 6). Its gains across cycles come mainly from sharpening behaviors already present in the demonstrations, whereas GROD 

20 

additionally composes new behaviors—reorienting objects before grasping, retrying after a failed attempt—that extend beyond the demonstration distribution. 

_Hypothesis: the gap reflects the pretrained prior._ Because the adaptation procedure is identical for both models, we attribute this gap to the strength of the pretrained prior rather than to the pipeline. Although GROD and _𝜋_ 0 _._ 5 share a conceptually similar VLA architecture, GROD is built on a foundation model trained on substantially more and more diverse robot data. We hypothesize that this broader pretraining yields more robust closed-loop perception and reactivity, which in turn lets the same **CLIFT** signal elicit richer corrective behavior and a higher performance ceiling. This is consistent with the controlled comparison in the main text, where even an invasive, full-access adaptation of _𝜋_ 0 _._ 5 fails to close the gap to GROD. 

21 

