---
title: "When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLAs"
date: "2026-02-19"
authors: "Yu Fang; Yuchun Feng; Dong Jing; Jiaqi Liu; Yue Yang; Zhenyu Wei"
venue: "CoRL 2026"
url: https://arxiv.org/abs/2602.17659
pdf: https://arxiv.org/pdf/2602.17659
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.17659)** / [論文ページ](https://arxiv.org/abs/2602.17659)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# When Vision Overrides Language: Evaluating and Mitigating Counterfactual Failures in VLAs 

Yu Fang, Yuchun Feng, Dong Jing, Jiaqi Liu, Yue Yang, Zhenyu Wei, Daniel Szafir, Mingyu Ding University of North Carolina at Chapel Hill https://vla-cf.github.io/ 


Fig. 1. **Overview.** (a) Vision-Language-Action Models (VLAs) often suffer from _counterfactual failures_ due to _vision shortcuts_ , defaulting to well-learned scene-specific behaviors instead of faithfully following instructions. (b) We study this issue and introduce LIBERO-CF, _the first counterfactual benchmark_ for evaluating language following in VLAs. (c) We propose _Counterfactual Action Guidance (CAG)_ , a dual-branch inference scheme that mitigates counterfactual failures in VLAs. (d) Extensive experiments in both simulation and real-world experiments demonstrate the effectiveness of CAG across diverse VLAs. 

**_Abstract_ —Vision-Language-Action models (VLAs) promise to ground language instructions in robot control, yet in practice often fail to faithfully follow language. When presented with instructions that lack strong scene-specific supervision, VLAs suffer from** **_counterfactual failures_ : they act based on** **_vision shortcuts_ induced by dataset biases, repeatedly executing welllearned behaviors and selecting objects frequently seen during training regardless of language intent. To systematically study it, we introduce LIBERO-CF, the first counterfactual benchmark for VLAs that evaluates language following capability by assigning alternative instructions under visually plausible LIBERO layouts. Our evaluation reveals that counterfactual failures are prevalent yet underexplored across state-of-the-art VLAs. We propose Counterfactual Action Guidance (CAG), a simple yet effective dual-branch inference scheme that explicitly regularizes language conditioning in VLAs. CAG combines a standard VLA policy with a language-unconditioned Vision-Action (VA) module, enabling counterfactual comparison during action selection. This design reduces reliance on visual shortcuts, improves robustness on under-observed tasks, and requires neither additional demonstrations nor modifications to existing architectures or pretrained models. Extensive experiments demonstrate its plug-and-play integration across diverse VLAs and consistent improvements. For example, on LIBERO-CF, CAG improves** _π_ 0 _._ 5 **by 9.7% in language following accuracy and 3.6% in task success on underobserved tasks using a training-free strategy, with further gains** 

**of 15.5% and 8.5%, respectively, when paired with a VA model. In real-world evaluations, CAG reduces counterfactual failures of 9.4% and improves task success by 17.2% on average.** 

## I. INTRODUCTION 

Vision-Language-Action models (VLAs) have achieved impressive performance in general robotic manipulation by leveraging pretrained Vision-Language Models (VLMs) to ground language in perception and action [47, 5, 6, 26, 4]. Despite recent advances, we identify a prevalent and underexplored failure mode in VLAs: poor language following behavior. In particular, when presented with instructions that have limited scene-specific supervision, VLAs often disregard the given instructions and default to executing well-learned tasks in the scene or selecting objects frequently seen during training, termed as _counterfactual failures_ . Such behavior raises critical concerns about the reliability of VLAs as general-purpose robotic agents, as they cannot faithfully follow user intent even in familiar environments, posing significant risks to safety and usability for real-world deployment. 

We attribute this limitation to the nature of robotic datasets and model modality imbalance, which are typically task- 

specific and visually dominant. Under a fixed scene, demonstrations are often collected for only a small subset of tasks, encouraging VLAs to rely on _vision shortcuts_ rather than faithfully grounding language. As a result, language conditioning plays a limited role in action selection, hindering VLAs from fully realizing the generalization capabilities inherited from pretrained VLMs. Fig. 2 provides direct evidence of this phenomenon: even under counterfactual or empty instructions, VLAs tend to execute the training task associated with the scene, and removing the training-task object significantly improves counterfactual performance. 

Recent works have begun to explore the role of language in VLAs [17, 18, 51, 40, 53, 31]. LIBERO-PLUS [17] studies robustness to linguistic rephrasing within the same task distribution, while CAST [18] and CounterfactualVLA [40] mitigate counterfactual biases through data augmentation in navigation and driving domains. However, these data-centric approaches lack a systematic benchmark and a general solution for robotic VLAs, leaving an open question: to what extent, and how can VLAs handle counterfactual tasks and distinguish visually plausible yet linguistically distinct instructions under controlled counterfactual settings? 

To systematically study language following behavior of VLAs, we introduce LIBERO-CF, the first counterfactual benchmark specifically designed to evaluate the counterfactual failures of VLAs based on LIBERO. LIBERO-CF assigns alternative feasible language instructions under LIBERO scene layouts, covering different object instances, targeting objects that previously appeared only as background, long-horizon tasks, and out-of-distribution objects that are never observed during VLA finetuning. Using this benchmark, we demonstrate that existing VLAs exhibit severe counterfactual failures: all the models perform poorly on newly assigned instructions while defaulting to executing well-learned training tasks. 

To mitigate counterfactual failures, we propose Counterfactual Action Guidance (CAG), a dual-branch inference scheme that enhances language conditioning by mixing actions between a standard VLA and a language-unconditional visionaction (VA) policy. CAG is plug-and-play, compatible with diverse VLA architectures, and requires no modifications to existing model architectures or pretrained weights. Through extensive simulation and real-world experiments, we demonstrate consistent improvements over diverse state-of-the-art VLAs in both language grounding and task success across spatial, object, goal, long-horizon, and out-of-distribution instruction settings. 

To summarize, our contributions are as follows. 

- We introduce LIBERO-CF, the first counterfactual benchmark, designed to evaluate language-following in VLAs by distinguishing visually plausible yet linguistically distinct instructions under controlled counterfactual settings. 

- We propose Counterfactual Action Guidance, a universal dual-branch inference scheme that enhances language conditioning across diverse VLAs without changing existing architectures or pretrained models. 

- We provide a comprehensive analysis of vision shortcuts and 

counterfactual failures in VLAs, and demonstrate consistent improvements over state-of-the-arts through both LIBEROCF and real-world experiments. 

## II. RELATED WORK 

## _A. Vision-Language-Action Models_ 

Recent years have witnessed rapid and substantial progress in the field of Vision-Language-Action (VLA) models [5, 6, 57, 30, 50, 10, 3, 36, 11, 16, 14, 9, 59, 42, 28, 34, 15, 45, 61, 56, 49, 46, 23, 29, 58]. The core paradigm involves predicting future action sequences conditioned on visual inputs and user instructions. By iteratively executing predicted actions and updating observations, VLAs enable closed-loop robotic control. Current methods for constructing VLAs can be broadly categorized into two main streams. The first stream builds upon Vision-Language Models (VLMs) [1, 62, 52, 2, 63, 22] by integrating an action modality [13, 4]. The primary advantage of this approach lies in endowing robots with rich semantic priors, enabling them to leverage powerful language reasoning to tackle complex scenarios. The second stream [8, 32] prioritizes World Models, such as video generation models [21, 44], which excel in visual perception and prediction. These models offer a distinct advantage in their precise understanding of physical laws and environmental dynamics. Regarding action representation, diverse strategies have emerged, ranging from discrete tokenization [41, 26] and continuous representations [27] to generative approaches based on flow matching [4, 20] or diffusion models [12]. In summary, the capabilities of VLAs are rapidly expanding, and both academia and industry regard them as a highly promising pathway toward achieving general robotic manipulation. 

## _B. Modality Imbalance in MultiModal Models_ 

Modality Imbalance has been widely studied in Visual Question Answering (VQA) and Multimodal Large Language Models (MLLMs) [37, 48, 35, 43, 54, 55, 60]. Common mitigation strategies include counterfactual data augmentation [55], modality reweighting [60], and training-time regularization [37] to encourage balanced multimodal reasoning. In contrast, modality imbalance in VLAs remains underexplored, as they remain prone to losing instruction following capabilities [27]. Recent works have explored introducing visionlanguage co-training [20], instruction augmentation [17, 18], and architectural refinements [20]. However, the field still lacks a standardized benchmark for evaluating language following in VLAs and a universal solution to mitigate counterfactual failures. We address both gaps in this paper. 

## III. PROBLEM FORMULATION 

## _A. Preliminaries_ 

**Vision-Language-Action Models (VLAs).** In robotic manipulation, VLAs aim to learn a generalist robot policy _π_ ( _a|o, l_ ) that predicts an action chunk _a_ , given visual observations _o_ and a natural language instruction _l_ . During training, the policy is optimized to imitate expert actions conditioned on 


Fig. 2. **Evidence for Vision Shortcuts in VLAs.** (a) We visualize the distribution of grasp positions from 50 trials as heatmaps under different instructions. Even when given counterfactual or empty instructions, VLAs tend to execute the well-learned training task in the scene. (b) Removing the training-task object in the scene improves the success rates of VLAs on counterfactual instructions. 

both vision and language. At inference time, the policy maps ( _o, l_ ) to actions, enabling closed-loop control for manipulation. 

**Vision Bias in Datasets.** Large-scale robotic datasets have largely driven recent advances in VLAs [38, 25, 7]. Training samples typically consist of continuous multi-view observations and actions paired with a static language instruction shared across the entire trajectory. As a result, the diversity of textual data is significantly lower than that of visual and action modalities, while the absence of vision-language data during training may lead to the degradation of language capabilities [20]. The limited task types may lead to vision shortcuts, encouraging VLAs to prioritize visual cues over language grounding [17, 18, 51, 40, 53, 31]. 

**Vision Bias in Architectures.** In typical VLAs, language tokens (typically dozens) are vastly outnumbered by visual tokens (often hundreds/thousands), creating a risk where textual influence can be marginalized. While most VLAs are built upon pre-trained VLMs with strong vision-language priors, the alignment among the three modalities may still be insufficient. 

## _B. Problem Formulation from Bayesian Perspective_ 

We view a VLA policy as a conditional action distribution _P_ ( _a | o, l_ ), where _o_ denotes visual observation and _l_ denotes language instruction. From a Bayesian perspective, an ideal conditional distribution can be factorized as 


where _P_ ( _a | o_ ) denotes the vision-only prior over actions, and _P_ ( _l | a, o_ ) denotes a likelihood measuring the language–action compatibility. In practice, however, VLA policies are often dominated by visual cues, such that 


indicating that the posterior collapses toward the vision-only prior. This collapse reflects a vision-dominated inductive bias, where language has limited influence on action prediction. 

We attribute this behavior to a common modality imbalance during VLA training. In addition to vision bias in robotic datasets, consider a typical scenario that, under a fixed visual observation _o_ , there exists a set of feasible tasks _Lo_ = _{lo_<sup>1</sup><sup>_, l_</sup> _o_<sup>2</sup><sup>_, · · ·, l_</sup> _o_<sup>_n}_.DuringVLAfinetuningforaspecificscene,</sup> only a limited subset _L_<sup>in</sup> _o_<sup>_⊂Lo_iscollectedwithsufficient</sup> expert demonstrations. The remaining tasks _L_<sup>out</sup> _o_ = _Lo \ L_<sup>in</sup> _o_ are under-observed during this scene-specific adaptation, even if they appear in large-scale pretraining. As a result, actions of _L_<sup>in</sup> _o_<sup>becomestronglyassociatedwith</sup><sup>_o_,whilethosein</sup><sup>_L_out</sup> _o_ remain weak, leading to vision shortcuts. 

In this paper, given a trained VLA policy _π_ ( _a|o, l_ ), we investigate its predicted actions _a_ under different language instructions _l ∈ Lo_ , when presented with identical or highly similar visual observations _o_ . In particular, we validate and mitigate the counterfactual failures that VLAs typically fail to follow the instructions in _L_<sup>out</sup> _o_<sup>,andinsteadignoreand</sup> default to executing tasks in _L_<sup>in</sup> _o_<sup>thatarewell-learnedunder</sup><sup>_o_.</sup> Notably, our problem formulation differs from prior settings that focus on rephrasing language instructions within the same task [17]. Instead, we study counterfactual instructions and directly probe language following behaviors in VLAs. 

## IV. THE LIBERO-CF BENCHMARK 

## _A. Benchmark Design_ 

To systematically evaluate the language-following capability of VLAs, we present LIBERO-CF, a counterfactual benchmark that assigns _counterfactual instructions_ under LIBERO scene layouts. LIBERO [33] is a widely used robotic manipulation benchmark that provides a standardized dataset for VLA finetuning and evaluation. While VLAs are finetuned on the original LIBERO dataset, which covers only in-domain manipulation tasks, LIBERO-CF evaluates whether these models can follow counterfactual instructions, i.e., alternative feasible tasks under the same layouts but are under-observed or entirely unseen during finetuning. 

TABLE I 

**EVIDENCE OF VISION SHORTCUTS ON THE LIBERO BENCHMARK.** 

|**Model**|**Mod**<br>**V**|**ality**<br>**L**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|---|---|
|OVLA|✓|✓|97.6%|98.4%|97.9%|94.5%|97.1%|
|pen<br>OFT|✓||83.2%|98.2%|10.0%|85.0%|69.1%|
|-||✓|0.0%|0.0%|3.4%|0.0%|0.9%|
||✓|✓|96.8%|98.8%|95.8%|85.2%|94.2%|
|_π_0|✓||28.0%|26.8%|3.4%|15.6%|18.5%|
|||✓|0.0%|0.0%|2.2%|0.0%|0.6%|
||✓|✓|98.8%|98.2%|98.0%|92.4%|96.9%|
|_π_0_._5|✓||68.2%|56.6%|10.2%|71.6%|51.7%|
|||✓|0.0%|0.0%|0.0%|0.0%|0.0%|


**Suites.** We construct four suites to form the LIBERO-CF benchmark: _CF-Spatial_ , _CF-Object_ , _CF-Long_ , and _CF-OOD_ . 

- _CF-Spatial_ (15 tasks). Evaluates spatial language grounding by targeting the objects that originally served only as background objects. 

- _CF-Object_ (10 tasks). Evaluates alternative object-centric instructions targeting different objects. 

- _CF-Long_ (10 tasks). Evaluates long-horizon language following with multi-step instructions involving new targets. 

- _CF-OOD_ (15 tasks). Evaluates generalization to out-ofdistribution settings with entirely unseen objects. 

**Metrics.** To quantitatively evaluate language following behaviors, we define a _grounding rate_ (“grounding”), which measures whether the gripper makes contact with the target object specified in the instruction, regardless of task completion. This metric reflects how faithfully the model follows the given language instructions. In addition, we report the _success rate_ (“success”), which measures whether the robot completes the task, providing a stricter measure of task execution. 

**Evaluation Dimensions.** In addition to reporting performance, we quantify how often a VLA defaults to well-learned scene-specific behaviors. In the tables, we denote “Faithful” when the model follows the instructed task, and “Biased” when it instead follows the original training task. 

## _B. Validating Vision Shortcuts of VLAs_ 

**VLA Baselines.** We discuss the language-following ability of representative and widely used VLAs. OpenVLA-OFT [27] is a large-scale 7B VLA that uses Prismatic VLM [24] as the backbone, and is pretrained on the Open-X-Embodiment dataset. _π_ 0 [4] is a 3B diffusion-based VLA built upon PaliGemma [24]. _π_ 0 _._ 5 [20] is an improved variant of _π_ 0 that adopts a hybrid pretraining procedure on large-scale robotic and non-robotic data, representing state-of-the-art performance. For all models, we use their officially released weights for the LIBERO benchmark in our evaluations. 

**Quantitative Results.** We validate the presence of vision shortcuts in VLAs using the LIBERO benchmark by ablating input modalities at inference time. Specifically, we evaluate three settings for each finetuned VLA: 1) standard inputs with both vision and language, 2) vision-only inputs, and 3) language-only inputs. The results are summarized in Table I. 

TABLE II 

**IMPACT OF TRAINING-TASK OBJECTS ON VISION SHORTCUTS.** 

|**Model**||**Metric**|**CF-Spatial**|**CF-Focused**|
|---|---|---|---|---|
|OpenVLA-OFT|[27]|<sup>Grounding</sup><br>Success|6.8%<br>1.1%|**31.9%**<br>**14.4%**|
|||Grounding|70.9%|**92.7%**|
|_π_0 [4]||Success|34.4%|**51.1%**|
|_π_0_._5 [20]||Grounding<br>Success|39.3%<br>24.4%|**68.5%**<br>**54.4%**|
|||Grounding|39.0%|**64.4%**|
|Avg.||Success|20.0%|**40.0%**|


All evaluated VLAs preserve high performance even when only vision is provided, while performance collapses to near zero when only language is given. This indicates that VLAs primarily rely on visual cues for action prediction. Notably, LIBERO-Goal shows relatively weaker vision reliance, with OpenVLA-OFT and _π_ 0 _._ 5 achieving 10.0% and 10.2% success rates under vision-only inputs, respectively. This is expected, as LIBERO-Goal only has a fixed scene while only varying task goals through instructions, strengthening the correlation between language and action. However, even in LIBEROGoal, where the language is most informative, language-only performance remains extremely limited. This suggests that language in current VLAs primarily functions as a secondary conditioning signal that modulates vision-driven policies. 

**Grasping Distributions.** In Fig. 2(a), we visualize the grasp positions from 50 trials on pick-and-place tasks in _CF-Spatial_ under different language instructions using _π_ 0 _._ 5 at inference time. When given the training-task instruction, grasp positions are tightly clustered around the corresponding training-task object, suggesting the task is well-learned. In contrast, under counterfactual instructions, the grasping distribution spreads not only around the instructed object but also around the training-task object. When given no instruction, the distribution still primarily centers on the training-task object. These results provide further evidence that VLAs tend to default to executing well-learned training tasks even when presented with alternative language instructions, offering insight into the nature of vision shortcuts and counterfactual failures. 

**Impact of Training-task Objects.** We investigate whether counterfactual failures are related to the visual distraction from training-task objects in the scene. To this end, as illustrated in Fig. 2(b), we construct a focused variant of _CF-Spatial_ by removing training-task objects from the scene, resulting in a new evaluation suite termed _CF-Focused_ . In Tab. II, we compare the performance of VLAs on _CF-Spatial_ and _CF-Focused_ . Although both suites use identical counterfactual instructions, all evaluated VLAs show consistently and drastically improved performance on _CF-Focused_ . On average, grounding and success rates increase by 25.4% and 20.0%, respectively. When present, such objects bias models toward executing the original training task, whereas removing them enables more faithful language-conditioned behavior. These results further validate the presence of vision shortcuts in 

VLAs and indicate that training-task objects act as strong visual attractors under counterfactual instructions. 

**Summary.** These observations provide evidence of _vision shortcuts_ in VLAs, and motivate the need for counterfactual evaluation and guidance to strengthen language conditioning. 

## V. METHOD: COUNTERFACTUAL ACTION GUIDANCE 

We aim to study a universal strategy across VLA models for likelihood sharpening for _P_ ( _l | a, o_ ), such that the predicted actions are more correlated to language instructions. 

## _A. Preliminary: Classifier-free Guidance_ 

Classifier-free guidance (CFG) is a conditioning technique to strengthen conditional generation without relying on an explicit classifier [19]. Given a conditional model trained to handle both conditioned and unconditioned inputs, CFG combines its conditional and unconditional predictions at inference time to amplify the influence of the conditioning signal. More specifically, let _f_ ( _x | c_ ) denote the model output conditioned on _c_ , and _f_ ( _x |_ ∅) denote the output under a null condition. CFG produces a guidance prediction 


where _s ≥_ 0 is the guidance scale that controls the strength of conditioning. Larger values of _s_ typically encourage stronger adherence to the condition, while excessively large values may degrade output quality. Notably, CFG operates only at inference time and does not require architectural changes, making it a flexible and model-agnostic mechanism for enhancing conditional fidelity. 

## _B. Counterfactual Action Guidance_ 

Inspired by classifier-free guidance, we introduce counterfactual action guidance (CAG), an inference-time action mixing rule for enhancing language conditioning in VLA policies. We consider the language instruction _l_ as the condition and consider two policies: a conditional policy _π_ cond( _a | o, l_ ) and an unconditional (vision-only) policy _π_ uncond( _a | o,_ ∅). We define the CAG policy as 


where _ω ≥_ 0 is a guidance scale controlling the strength of language conditioning. Intuitively, the difference between the conditional and unconditioned policies approximates the language-induced shift in action preference under the same observation. In this way, CAG can be interpreted as an inference-time reweighting of the posterior action distribution: 


where the guidance scale _ω_ controls the strength of the language likelihood relative to the action prior. This provides a mechanism for mitigating vision shortcuts in VLAs while preserving the underlying execution prior. 


Fig. 3. **Method.** We propose Counterfactual Action Guidance (CAG), a dualbranch inference scheme that enhances language conditioning by combining a VLA policy with a language-unconditioned Vision-Action (VA) branch. 

## _C. Dual-branch Inference with CAG_ 

To enhance language grounding in VLAs as described in Eq. 4, a language-conditioned policy _π_ cond and an unconditioned vision-only policy _π_ uncond are required to amplify the language-action likelihood. As shown in Fig. 3, we implement a CAG policy as a dual-branch inference scheme, where the conditioned policy is combined with an unconditioned policy. To present a universal solution across various VLA architectures, we design the CAG policy as an inference-time policy, while _π_ cond and _π_ uncond are finetuned separately ahead of time and assembled during inference time. While a standard VLA is used as _π_ cond, we introduce two options for preparing the unconditioned branch: 

**1) Training-Free Strategy (TF).** Without introducing additional finetuning efforts, we first consider directly using a standard trained VLA model to approximate both the conditioned and unconditioned policies. Specifically, we obtain the language-conditioned policy _π_ ( _a | o, ℓ_ ) with the language input, and derive an approximate unconditioned policy _π_ ( _a | o_ ) by dropping the language input at inference time. 

**2) Training a Vision-Action Prior (VA).** For stronger and more stable performance, we opt to train a separate VisionAction (VA) Model to explicitly represent the unconditioned policy _π_ ( _a | o_ ). Compared to standard VLAs, VA models provide a cleaner vision-only prior, which is decoupled from language supervision. At inference time, the VA model is paired with the language-conditioned VLA model within the same dual-branch guidance framework, resulting in improved language grounding and reduced vision shortcuts. 

## VI. SIMULATION EXPERIMENTS 

## _A. Implementation Details_ 

We conduct simulation experiments on the LIBERO-CF benchmark. For fair comparisons, we run 50 trials for each task across all methods. For the VLAs in our experiments, we use the official finetuned weights for the LIBERO benchmark. For the unconditional Vision-Action models, we finetune each VA model on the LIBERO dataset using the default training configurations as its corresponding VLA, except that the language input is dropped. We finetune VA models for _π_ 0 _._ 5 for 30k steps with a batch size of 32. 

TABLE III **QUANTITATIVE EVALUATION OF VLAS ON THE LIBERO-CF BENCHMARK.** 

||||**CF-S**|**patial**|**CF-O**|**bject**|**CF-L**|**ong**|**CF-O**|**OD**|**Aver**|**age**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**Metric**|**CAG**|||||||||||
||||**Faithful**<br>_↑_|**Biased**<br>_↓_|**Faithful**<br>_↑_|**Biased**<br>_↓_|**Faithful**<br>_↑_|**Biased**<br>_↓_|**Faithful**<br>_↑_|**Biased**<br>_↓_|**Faithful**<br>_↑_|**Biased**<br>_↓_|
|||/|6.8%|84.7%|2.0%|99.6%|4.0%|62.9%|6.0%|87.3%|4.7%|83.6%|
||Grounding|TF|11.1%|78.5%|1.6%|100.0%|4.9%|61.1%|5.6%|88.1%|5.8%|81.9%|
|OpenVLA-OFT<br>||VA|**26.5%**|**59.5%**|**3.8%**|**91.8%**|**6.9%**|**60.0%**|**7.9%**|**50.1%**|**11.3%**|**65.4%**|
|[27]||/|1.1%|80.7%|0.0%|97.6%|0.2%|54.4%|0.1%|81.7%|0.4%|78.6%|
||Success|TF|3.3%|73.3%|0.0%|94.4%|0.2%|54.0%|0.1%|83.5%|0.9%|76.3%|
|||VA|**7.9%**|**35.2%**|0.0%|**57.0%**|**0.4%**|**48.9%**|0.1%|**22.7%**|**2.1%**|**41.0%**|
|||/|70.9%|37.1%|6.0%|59.4%|20.4%|83.1%|18.0%|72.4%|28.8%|63.0%|
||Grounding|TF|74.5%|32.5%|12.2%|**50.6%**|19.6%|**81.8%**|21.1%|72.4%|31.9%|59.3%|
|_π_0 [4]||VA|**85.2%**|**24.4%**|**13.8%**|53.8%|**22.7%**|82.2%|**27.6%**|**47.5%**|**37.3%**|**52.0%**|
|||/|34.4%|19.1%|0.0%|45.0%|1.1%|63.1%|**2.7%**|52.9%|9.6%|45.0%|
||Success|TF|33.5%|14.4%|**0.6%**|**15.0%**|2.0%|**38.7%**|2.1%|42.3%|9.6%|27.6%|
|||VA|**36.7%**|**6.1%**|0.0%|29.2%|**2.9%**|48.7%|2.1%|**19.2%**|**10.4%**|**25.8%**|
|||/|39.3%|61.3%|11.4%|68.8%|51.6%|58.4%|20.7%|74.0%|30.8%|65.6%|
||Grounding|TF|**52.0%**|45.3%|24.6%|65.2%|60.7%|**56.7%**|24.8%|71.9%|40.5%|59.8%|
|_π_0_._5 [20]||VA|50.7%|**45.2%**|**34.0%**|**49.8%**|**64.2%**|61.1%|**36.4%**|**52.8%**|**46.3%**|**52.2%**|
|||/|24.4%|56.9%|5.8%|66.8%|15.8%|50.4%|6.9%|69.6%|13.2%|60.9%|
||Success|TF|27.3%|**33.3%**|9.2%|41.4%|20.9%|**36.7%**|9.9%|62.7%|16.8%|43.5%|
|||VA|**31.6%**|36.0%|**18.0%**|**29.8%**|**26.7%**|41.8%|**10.3%**|**37.1%**|**21.7%**|**36.2%**|


_B. Evaluating Counterfactual Behaviors_ 

In Tab. III, we report the performance of OpenVLAOFT [27], _π_ 0 [4], _π_ 0 _._ 5 [20] on the LIBERO-CF benchmark. 

**Performance of Baselines.** We observe that all evaluated VLAs suffer from severe counterfactual failures. OpenVLAOFT exhibits the most severe vision shortcuts, achieving only a 4.7% grounding rate and 0.4% success rate. Even _π_ 0 _._ 5, which reaches the best overall performance among the baselines, achieves only a 30.8% grounding rate and 13.2% success rate. This indicates almost complete inability to follow counterfactual instructions, with language conditioning playing a minimal role in action prediction. In contrast, they maintain high performance on biased metrics: even with counterfactual instructions, OpenVLA-OFT achieves 83.6% grounding rate and 78.6% success rate on original training tasks, while _π_ 0 _._ 5 achieves 65.6% grounding and 60.9% success. This disparity highlights the severity of counterfactual failures in current VLAs, which strongly default to executing well-learned scenespecific behaviors rather than following the given instructions. 

**Effectiveness of CAG.** We validate the effectiveness of Counterfactual Action Guidance across all evaluated VLAs using two alternative variants: the training-free strategy (denoted as _TF_ ) and a Vision-Action prior (denoted as _VA_ ). As shown in Tab. III, compared to the corresponding VLA baselines, both CAG variants consistently improve grounding and success rates on counterfactual tasks while simultaneously decreasing biased execution of the original training tasks. This demonstrates that CAG effectively mitigates vision shortcuts and corrects counterfactual failures by shifting the action posterior toward language-conditioned behaviors. For example, on _π_ 0 _._ 5, TF improves the average grounding rate from 30.8% to 40.5%, while VA further boosts it to 46.3% with corresponding 

success rates increasing from 13.2% to 21.7%. Importantly, these improvements are accompanied by a substantial reduction in counterfactual failures: for _π_ 0 _._ 5, VA reduces biased grounding by 13.4% and biased success by 24.7%. Notably, _π_ 0 _._ 5 with VA even achieves 36.4% grounding and 10.3% success on CF-OOD, demonstrating that vision shortcuts significantly suppress the generalization capabilities of VLAs. While our training-free strategy is already proven effective, VA generally yields stronger improvements, suggesting that explicitly modeling the vision-only prior provides a more reliable counterfactual correction than reusing a languageconditioned VLA policy as the unconditioned branch. 

**Variation in Counterfactual Failures across VLAs.** In Tab. III, we further observe that the prevalence of counterfactual failures and the effectiveness of CAG vary across different VLAs. In particular, while all evaluated VLAs benefit from CAG, CAG reduces counterfactual failures on _π_ 0 _._ 5 much more than on OpenVLA-OFT. This suggests that _π_ 0 _._ 5 exhibits a weaker form of vision shortcuts than OpenVLA-OFT (also in Tab. I), allowing CAG to reweight the action posterior more effectively. In contrast, OpenVLA-OFT demonstrates more rigid vision-dominated behaviors and requires stronger guidance to overcome its entrenched visual priors. Overall, these results indicate that counterfactual failures are not a binary phenomenon, but instead exist along a spectrum, influenced by model architecture, training strategy, and action modeling. 

## _C. Ablation Studies_ 

**Training Strategies.** We conduct ablation studies to investigate effective training strategies for CAG, using _π_ 0 _._ 5 on CFSpatial and CF-Long. Using the vanilla _π_ 0 _._ 5 as the baseline ( _R1_ ), we evaluate and compare several CFG-based variants: _R2_ : a VLA finetuned with random language dropout as both 

VII. REAL-WORLD EXPERIMENTS 

TABLE IV **INVESTIGATING TRAINING STRATEGIES FOR COUNTERFACTUAL ACTION GUIDANCE WITH** _π_ 0 _._ 5 **.** 

|**Me**|**tric**|**Strategy**|**CF-Sp**<br>|**atial**<br>|**CF-L**<br>|**ong**<br>|
|---|---|---|---|---|---|---|
||||**Faithful**|**Biased**|**Faithful**|**Biased**|
|||R1|39.3%|61.3%|51.6%|58.4%|
|||R2|9.5%|89.3%|34.0%|83.1%|
|Grou|nding|R3|52.0%|45.3%|60.7%|56.7%|
|||R4|**52.3%**|47.5%|**64.9%**|59.6%|
|||R5|50.7%|45.2%|64.2%|61.1%|
|||R1|24.4%|56.9%|15.8%|50.4%|
|||R2|3.7%|86.5%|2.7%|71.3%|
|Suc|cess|R3|27.3%|33.3%|20.9%|36.7%|
|||R4|27.7%|37.1%|26.4%|41.6%|
|||R5|**31.6%**|36.0%|**26.7%**|41.8%|
|60||**50.7**|**56.8**|**58.4**|_π_0.5(Gro<br>_~~π~~_0.5~~(Suc~~<br>|unding)<br>~~cess)~~<br>|
||||||OpenVLA|-OFT (Grounding)|
|40<br>**te (%)**|**24.4**<br>**39.3**|**~~31.6~~**|**28.8**<br>|**26.5**|<br>OpenVLA|**30.4**<br> <br>-OFT (Success)|
|20<br>**Ra**|**6.8**|**11.6**|**18.4**|**16.4**|||
|0|**1.1**|**2.9**|**~~5.9~~**|**~~7.9~~**||**~~4.1~~**|
||1.0|1.5|2.0<br>**Guidanc**|3.0<br>**e Scale**||4.0|


Fig. 4. **Investigation of guidance scale.** Increasing the guidance scale strengthens language conditioning and improves grounding accuracy. However, overly large scales degrade task success due to over-guidance. 

_π_ cond and _π_ uncond; _R3_ : a standard VLA used as both _π_ cond and _π_ uncond at inference time (aligned with _TF_ ); _R4_ : a standard VLA as _π_ cond paired with a LoRA-finetuned VA model as _π_ uncond; _R5_ : a standard VLA as _π_ cond paired with a fully finetuned VA model as _π_ uncond (aligned with _VA_ ). 

As shown in Tab. IV, even the training-free strategy ( _R3_ ) consistently improves both grounding and success rates over the baseline, demonstrating the effectiveness of CAG. When introducing a separately trained VA model, both R4 and R5 achieve stronger performance than R3, indicating that explicitly modeling the vision-only prior with a separate VA branch is more effective. R4 and R5 achieve comparable overall performance, suggesting both LoRA and full finetuning is effective for training a VA model. The fully finetuned VA model (R5) further improves success rates, e.g., by 4.3% on CF-Spatial, suggesting better manipulation accuracy. Notably, while dropout-based training (R2) is a common strategy for CFG in generative models, it performs poorly on VLAs: language dropout weakens instruction conditioning, leading to a severe degradation toward vision-dominated behaviors. 

**Guidance Scales.** As shown in Fig. 4, we study the effect of guidance scale _ω_ on _π_ 0 _._ 5 and OpenVLA-OFT. For both VLAs, increasing the guidance scale progressively mitigates vision shortcuts, but over-guidance degrades manipulation accuracy. OpenVLA-OFT requires a larger guidance scale, which is consistent with its stronger reliance on visual cues (in Tab. I). Empirically, to achieve the best manipulation performance, we set _ω_ = 1 _._ 5 for _π_ 0 and _π_ 0 _._ 5, and _ω_ = 3 _._ 0 for OpenVLA-OFT. 

## _A. Task Design_ 

To further evaluate vision shortcuts in VLAs and validate the effectiveness of CAG, we design extensive real-world evaluations to study different aspects of language grounding in real-world settings. Each scene is designed with three possible tasks: one belongs to well-learned in-domain tasks _L_<sup>in</sup> _o_<sup>with</sup> sufficient expert demonstrations, where the remaining two correspond to under-observed tasks _L_<sup>out</sup> _o_ with counterfactual instructions. 1) _Object Recognition_ : Three distinct objects are present in the scene, and tasks differ by the target object specified in the instruction; 2) _Spatial Reasoning_ : Three identical objects are placed at different spatial locations, requiring the robot to distinguish based on spatial language; 3) _Goal Targeting_ : Three tasks are defined for the same object, requiring the understanding of different goal specifications. 4) _Out-ofDistribution Generalization (OOD)_ : Distinguish one familiar and two entirely unseen objects in the finetuning dataset. 

## _B. Implementation Details_ 

**Setup.** We conduct real-world experiments using a Franka Research 3 equipped with a Robotiq-2F85 gripper. Our setup follows the DROID platform [25], including a ZED 2i stereo camera as the exterior camera and a ZED mini camera as the wrist camera. We randomly change the position of the objects during data collection and inference. During both data collection and inference, we place the objects with random positions. We perform 10 trials per instruction for evaluation. 

**Dataset and VLA Finetuning.** To reflect the practical bias toward a single dominant task, we collect 20 demonstrations for each _l ∈ L_<sup>in</sup> _o_<sup>.Foreach</sup><sup>_l∈L_out</sup> _o_<sup>,wecollectonlya</sup> single demonstration for minimal warm-up, while setting OOD tasks in a zero-shot manner. We set _π_ 0 _._ 5 as our baseline due to its strong real-world manipulation performance, and use it to demonstrate the effectiveness of Counterfactual Action Guidance with a VA model (aligned with _VA_ in Sec. VI-B). For each of the VLA and VA components, we fully finetune the _π_ 0 _._ 5-DROID model for 10k steps with a batch size of 32. 

## _C. Results_ 

In Fig. 5, we present the results of our real-world evaluations. For each scene, the first task corresponds to the welllearned in-domain task during finetuning, while the remaining two tasks are under-observed. 

**Object Recognition.** We begin with Coke/Sprite/Fanta, which share identical geometry and differ only in visual appearance. This setting represents a minimal counterfactual object recognition challenge, as these objects are common in large-scale robotic datasets [39, 25] and require identical manipulation skills. Despite this simplicity, _π_ 0 _._ 5 still exhibits grounding errors for under-observed tasks, indicating that vision shortcuts can hinder simple object recognition and degrade performance even when manipulation difficulty remains unchanged. We further evaluate a more challenging setting with Tape/Mustard/Pringles, which involves diverse object geometries and manipulation requirements. While _π_ 0 _._ 5 


Fig. 5. **Real-world experiments.** We study multiple aspects of language grounding in real-world evaluations, including object recognition, spatial reasoning, goal execution, and out-of-distribution generalization. CAG consistently reduces counterfactual failures and improves task success across all scenes. 

maintains strong performance on the in-domain training task, its performance drops sharply on the two under-observed tasks, reflecting significant counterfactual failures. With CAG, grounding and success rates on all under-observed tasks improve consistently, while performance on the in-domain task is preserved. Notably, CAG achieves a 100% average grounding rate across all instructions, and effectively improves the success rates by 13.3% in both scenes. These findings highlight the existence of vision shortcuts across objects and the effectiveness of CAG in mitigating them. 

**Spatial Reasoning.** We place three identical white cups and corn cans at different positions in _Middle/Left/Right_ and _Table/Plate/Bowl_ , respectively, isolating spatial language grounding as the primary challenge. However, _π_ 0 _._ 5 achieves only 20% and 30% grounding rates on under-observed targets (i.e., left, right) in _Middle/Left/Right_ , and 60% for Plate and 40% for Bowl in _Table/Plate/Bowl_ . These results show that VLAs are particularly prone to vision shortcuts in spatially differentiated tasks, often failing to select the correct object instance. In contrast, CAG mitigates this failure mode, improving grounding by 16.6% and task success by 13.3%, demonstrating its effectiveness in strengthening spatial language conditioning. 

**Goal Targeting.** In _Stack/Plate/Basket_ , we evaluate goallevel language grounding by assigning different goals to the same cup. While _π_ 0 _._ 5 shows decent grounding performance on under-observed goals, task success rates remain low, as the robot often fails to release the objects at the intended goal. 

Moreover, _π_ 0 _._ 5 sometimes places the cup at an incorrect goal even when given training-task instruction, further evidencing vision shortcuts. With CAG, grounding improves to 96.7%, and task success increases by 36.7%, demonstrating more reliable goal execution. These results suggest that counterfactual failures can manifest at the level of goal completion, and CAG effectively mitigates this failure mode. 

**OOD Generalization.** In _Cup/Cube/Basketball,_ we evaluate zero-shot language grounding on OOD objects. Although Cube and Basketball are never observed during finetuning, _π_ 0 _._ 5 still achieves 50% and 60% success rates, respectively, demonstrating strong zero-shot generalization enabled by large-scale pretraining. However, this capability is largely compromised by counterfactual failures: e.g., 4 out of 5 failures on Cube are counterfactual failures. CAG effectively mitigates this issue, and further unlocks zero-shot generalization ability of VLAs. 

**Summary.** Although _π_ 0 _._ 5 achieves high performance across all training tasks, it suffers from severe counterfactual failures due to vision shortcuts. CAG provides a simple yet effective solution across all evaluated dimensions, consistently improving both grounding and task success on under-observed tasks. Importantly, these improvements come without loss on the original training tasks, showing that CAG corrects counterfactual failures while preserving in-domain performance. 

VIII. CONCLUSION 

We provide a systematic study of vision shortcuts and counterfactual failures in VLAs. We introduce LIBERO-CF, the 

first counterfactual benchmark to study the language following capability of VLAs. We further propose Counterfactual Action Guidance (CAG), a simple yet effective dual-branch inference scheme that strengthens language conditioning in VLAs without changing existing architectures or weights. Extensive experiments in both simulation and the real world demonstrate the presence of vision shortcuts, and CAG effectively reduces counterfactual failures. Our insights can be applied across diverse VLAs, benefiting the large embodied AI communities. 

## APPENDIX 

The appendix includes three sections. 

- Appendix A provides a detailed derivation of Counterfactual Action Guidance. 

- Appendix B presents additional simulation experiments on an extra VLA (i.e., X-VLA [58]), together with further discussion of the dynamic guidance scale. 

- Appendix C includes extended real-world experiments on long-horizon reasoning, along with detailed scene descriptions and a complete breakdown of results across all evaluated scenes. 

## APPENDIX A 

## DETAILED EXPLANATION OF COUNTERFACTUAL ACTION GUIDANCE 

In this section, we provide a detailed derivation of Counterfactual Action Guidance (CAG) to supplement the formulation presented in Sec. V-B of the main paper. Recalling from the problem formulation in Sec. III-B, we decompose the ideal conditional distribution as: 


We define CAG policy as a linear combination of the unconditional and conditional policies: 


where _ω ≥_ 0 is a guidance scale controlling the strength of language conditioning. 

We rewrite this definition with log-probability: 


Next, we substitute the Bayesian decomposition from Eq. 7 into the term log _P_ ( _a | o, l_ ) in Eq. 9: 


The visual prior term log _P_ ( _a | o_ ) cancels out inside the parentheses, we obtain: 


Finally, we exponentiate both sides to recover the probability space: 

_P_ CAG( _a | o, l_ ) _∝_ exp(log _P_ ( _a | o_ ) + _ω ·_ log _P_ ( _l | a, o_ )) _._ (12) 

Using the exponential properties, we derive the final equation: 


This validates that CAG acts as an inference-time reweighting that sharpens the language likelihood _P_ ( _l | a, o_ ) with temperature _ω_ , while preserving the underlying execution prior. 

## APPENDIX B 

## EXTENDED SIMULATION EXPERIMENTS 

## _A. Supplementary Results_ 

**Additional VLA Baseline.** In addition to VLAs evaluated in the main paper, we include X-VLA [58] as an additional state-of-the-art baseline. X-VLA is a 0.9B VLA architecture that utilizes learnable soft-prompts to tackle cross-embodiment settings and learn across multiple domains ranging from simulation to real-world datasets. 

**Results.** In Tab. V, we report additional quantitative results of X-VLA [58] on the LIBERO-CF Benchmark. X-VLA shows counterfactual failures similar to other VLAs, further confirming that this failure mode is not specific to particular architectures. This reflects a strong reliance on scene-specific visual priors and limited robustness to alternative feasible instructions, consistent with the vision shortcut phenomenon observed in other VLAs. Notably, both variants of CAG improve language grounding for X-VLA. The training-free strategy (TF) increases average grounding from 37.3% to 39.7% and success from 13.8% to 19.5%, while reducing biased success on training tasks. Using a Vision–Action prior (VA) increases average grounding to 41.0% and success to 17.1%. Overall, these results further demonstrate that counterfactual failures are widespread across VLAs. Importantly, CAG consistently mitigates such failures without modifying model architectures or pretrained checkpoints, highlighting its general applicability across diverse VLA designs. 

## _B. Implementation Details_ 

**OpenVLA-OFT** [27]. OpenVLA-OFT adopts a continuous action representation and employs an optimized finetuning recipe with parallel decoding and action chunking. Unlike OpenVLA [26], actions are optimized via L1 regression instead of bin-wise classification. We directly use the officially released LIBERO-finetuned checkpoint trained on the combined four task suites. For the VA model, we provide empty 

TABLE V 

**QUANTITATIVE EVALUATION OF X-VLA ON THE LIBERO-CF BENCHMARK.** 

||||**CF-Sp**|**atial**|**CF-O**|**bject**|**CF-L**|**ong**|**CF-O**|**OD**|**Aver**|**age**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**Metric**|**CAG**|**Faithful**|**Biased**|**Faithful**|**Biased**|**Faithful**|**Biased**|**Faithful**|**Biased**|**Faithful**|**Biased**|
||||_↑_|_↓_|_↑_|_↓_|_↑_|_↓_|_↑_|_↓_|_↑_|_↓_|
|||/|22.1%|72.1%|1.4%|70.4%|**98.2**%|23.3%|27.3%|**58.4**%|37.3%|56.1%|
||Grounding|TF|22.3%|68.9%|0.0%|77.6%|95.6%|**12.2**%|**40.9**%|63.7%|39.7%|55.6%|
|X-VLA [58]||VA|**24.4**%|**68.8**%|**2.0**%|**59.6**%|96.7%|17.6%|40.8%|60.5%|**41.0**%|**51.6**%|
|||/|3.2%|58.9%|0.0%|50.2%|47.6%|9.1%|4.4%|38.8%|13.8%|39.3%|
||Success|TF|**8.9**%|62.3%|0.0%|56.6%|**59.1**%|3.8%|**10.1**%|47.9%|**19.5**%|42.6%|
|||VA|8.7%|**53.7**%|0.0%|**31.6**%|51.1%|**0.9**%|8.7%|**38.1**%|17.1%|**31.1**%|


language instructions to keep the remaining prompt structure unchanged, and follow the official LIBERO finetuning configuration. We LoRA finetune OpenVLA-7B with a batch size of 64 for 300k steps using the Adam optimizer, a learning rate of 5 _×_ 10<sup>_−_4</sup> . Since OpenVLA-OFT shows a stronger reliance on visual cues, we use a guidance scale of _ω_ = 3 _._ 0 for both the TF and VA variants in our experiments. 

_π_ 0 [4] **and** _π_ 0 _._ 5 [20]. We directly adopt the officially released LIBERO-finetuned checkpoints for the VLA baselines. For the VA model, we follow the same finetuning recipe but drop the language tokens. We fully finetune the base models with a batch size of 32 for 30k steps using the Adam optimizer, a learning rate of 5 _×_ 10<sup>_−_5</sup> , and an EMA decay of 0.999. For CAG, we use a guidance scale of _ω_ = 1 _._ 5 for both TF and VA. 

**X-VLA** [58]. For the VLA baseline, we finetune the officially released base model (X-VLA-Pt) on the LIBERO dataset in the absolute end-effector action space. We use bf16 mixed precision, a batch size of 16, a learning rate of 1e _−_ 4 with a learning-rate coefficient of 0.1, and train for 50k iterations with 2k warmup steps, freezing the backbone for the first 1k steps. For the VA model, we use the same finetuning configuration as the VLA baseline, but drop the language tokens so that the model is conditioned only on visual observations. For CAG, we use a guidance scale of _ω_ = 1 _._ 5 for both the TF and VA variants in all X-VLA experiments. 

## APPENDIX C 

## EXTENDED REAL-WORLD EXPERIMENTS 

## _A. Our Setup_ 

We illustrate our real-world setup in Fig. 6. We use a Franka Research 3 robot arm equipped with a Robotiq-2F85 gripper. We use a ZED 2i stereo camera as the exterior camera and a ZED mini camera as the wrist camera, following the DROID platform [25]. 

## _B. Details of Our Real-world Datasets_ 

We provide detailed task descriptions for each real-world scene in Tab. VI. All expert demonstrations are collected via teleoperation using the DROID platform [25]. For each indomain task in _L_<sup>in</sup> _o_<sup>,wecollect20expertdemonstrationsto</sup> ensure sufficient scene-specific supervision. For each underobserved task in _L_<sup>out</sup> _o_<sup>,weonlycollectasingledemonstration</sup> for minimal warm-up and treat these tasks as counterfactual 


Fig. 6. **Our real-world setup.** We conduct all real-world experiments using a Franka Research 3 robot arm with a Robotiq 2F85 gripper, with a ZED 2i and a ZED Mini. 

during evaluation. Our experiments focus on under-observed tasks to investigate counterfactual failures in VLAs and to validate the effectiveness of Counterfactual Action Guidance (CAG), while also reporting results on in-domain tasks to verify that CAG preserves performance on in-domain tasks. 

## _C. Additional Experiments for Long-Horizon Reasoning_ 

In the main paper, we study multiple aspects of language grounding in real-world settings, including: 1) _Object Recognition_ , 2) _Spatial Reasoning_ , 3) _Goal Targeting_ , and 4) _Outof-Distribution (OOD) Generalization_ . **In this appendix, we further extend our evaluation to an additional dimension: 5)** **_Long-Horizon Reasoning_ .** This examines the ability of VLAs to follow multi-step instructions and maintain language grounding over extended action horizons. 

**Task Design.** As in other dimensions, each scene includes three possible tasks, one belongs to well-learned in-domain tasks _L_<sup>in</sup> _o_<sup>withsufficientexpertdemonstrations,wherethe</sup> remaining two correspond to under-observed tasks _L_<sup>out</sup> _o_ with counterfactual instructions. We design two scenes: _Move and Pour_ and _Apple and Banana_ for long-horizon reasoning. We present our results in Fig. 7. 

**_Move and Pour_ .** We study whether VLAs can correctly ground the instructed objects during long-horizon, multi-step instructions. The in-domain task is “Move the cup to the right and pour the coke into the cup”, while counterfactual tasks replace the poured object with Sprite or Fanta. In 


Fig. 7. **Additional real-world experiments for long-horizon reasoning.** CAG improves the performance of _π_ 0 _._ 5 across both scenes, consistent with the discussed dimensions in the main paper. 

TABLE VI **REAL-WORLD TASK DESCRIPTIONS ACROSS SCENES.** 

|**Dimension**|**Scene**|**In-domain Tasks** _L_<sup>in</sup><br>_o_|**Under-observed tasks** _L_<sup>out</sup><br>_o_|
|---|---|---|---|
|ObjectReconition|Coke / Sprite / Fanta|Pick up the coke|Pick up the sprite<br>Pick up the fanta|
|g|Tape / Mustard / Pringles|Pick up the tape|Pick up the mustard<br>Pick up the pringles|
|SatialReasonin|Middle / Left / Right|Pick up the cup in the middle|Pick up the cup on the left<br>Pick up the cup on the right|
|p g|Table / Plate / Bowl|Pick up the corn can on the table|Pick up the corn can on the plate<br>Pick up the corn can in the bowl|
|Goal Targeting|Stack / Plate / Basket|Stack the cups|Put the cup on the plate<br>Put the cup in the basket|
|OOD Generalization|Cup / Cube / Basketball|Pick up the cup|Pick up the Rubik’s Cube<br>Pick up the basketball|
|Long-Horizon Reasoning|Move and Pour<br>Apple and Banana|Move the cup to the right<br>and pour the coke into the cup<br>Put the apple on the tray<br>and then put the banana on the tray|Move the cup to the right and pour the fanta into the cup<br>Move the cup to the right and pour the sprite into the cup<br>Put the banana on the tray and then put the apple on the tray<br>Put the apple on the tray|


Fig. 7, _π_ 0 _._ 5 shows clear counterfactual failures: It frequently pours the wrong drink, typically defaulting to the trainingtask object (coke). This indicates that counterfactual failures persist even when object grounding is required at later stages of long-horizon execution, and that VLAs tend to over-rely on memorized training-task objects when resolving ambiguity across steps. Notably, these failures occur more frequently than in the corresponding short-horizon object recognition task ( _Coke/Sprite/Fanta_ ), suggesting that vision shortcuts compound over time. CAG effectively strengthens language conditioning throughout the execution horizon, preventing early visual priors from dominating later decision points. 

**_Apple and Banana_ .** We investigate whether VLAs can correctly understand both _order_ and _cardinality_ of multi-step instructions. More specifically, while the in-domain task is 

“Put the apple on the tray and then put the banana on the tray”, we design two counterfactual tasks: 1) reversing the order (“Put the banana on the tray and then put the apple on the tray”), and 2) a partial instruction that requires only the first step (“Put the apple on the tray”). In Fig. 7, _π_ 0 _._ 5 shows clear counterfactual failures in both settings. For the reversed-order instruction, it often follows the original training order, placing the apple first despite explicit language specifying the opposite order. For the partial instruction, it frequently over-executes by completing the full training sequence, placing both objects instead of stopping after the apple. These failures indicate that counterfactual failures in VLAs can manifest as _temporal and compositional errors_ , where the model tends to fall back on memorized action sequences rather than faithfully following the instructions. We observe that CAG effectively mitigates 

these failures. Both grounding and success rates improve across all long-horizon variants, demonstrating that language guidance more effectively reweights the action distribution at each step. In particular, CAG significantly improves success on the “apple-only” task, showing that it can suppress false continuation of learned action sequence and enforce instruction termination. Overall, these results suggest that counterfactual failures become more severe over long horizons, and that CAG helps maintain language grounding throughout multistep execution. 

## _D. Detailed Results_ 

**Qualitative results.** In Fig. 8, we present the comparisons with and without Counterfactual Action Guidance. We further provide qualitative results from real-world rollouts using Counterfactual Action Guidance, including object recognition in Fig. 9, spatial reasoning in Fig. 10, goal targeting in Fig. 11, out-of-distribution generalization in Fig. 12, and long-horizon reasoning in Fig. 13. 

**Quantitative results.** To further analyze the failure patterns, we report the full breakdown of our real-world evaluation results in Tab. VII. For each task instruction, we conduct 10 trials and report each entry as successful executions / total attempts. For example, in the _Coke/Sprite/Fanta_ scene with _π_ 0 _._ 5, when given the instruction “Pick up the fanta”, the robot attempts the correct task 9 times and succeeds 6 times (reported as “6/9”), corresponding to a 90% grounding rate and a 60% task success rate. Notably, there is also one trial in which the robot instead grasps the coke and succeeds (reported as “1/1”), illustrating a concrete instance of a counterfactual failure. The “Fail” columns record trials in which the robot remains idle or do not show any clear grounding toward any specific object. This detailed breakdown enables fine-grained analysis of failure modes, allowing us to explicitly distinguish correct instruction following behavior from biased execution toward well-learned training tasks. 


Fig. 8. **Qualitative comparisons with and without Counterfactual Action Guidance.** 


Pick up the fanta 


Pick up the mustard 

Fig. 9. **Real-world rollouts using Counterfactual Action Guidance for object recognition.** 


Pick up the cup on the right 


Pick up the corn can in the bowl 

Fig. 10. **Real-world rollouts using Counterfactual Action Guidance for spatial reasoning.** 


Put the cup on the plate 


Put the cup in the basket 

Fig. 11. **Real-world rollouts using Counterfactual Action Guidance for goal targeting.** 


Pick up the basketball 


Pick up the Rubik’s Cube 

Fig. 12. **Real-world rollouts using Counterfactual Action Guidance for out-of-distribution generalization.** 


Move the cup to the right and pour the fanta into the cup 


Put the banana on the tray and then put the apple on the tray 

Fig. 13. **Real-world rollouts using Counterfactual Action Guidance for long-horizon reasoning.** 

TABLE VII 

**BREAKDOWN RESULTS IN REAL-WORLD EXPERIMENTS.** EACH ENTRY IS REPORTED AS SUCCESSFUL EXECUTIONS / TOTAL ATTEMPTS. ROWS DENOTE THE INSTRUCTED TARGET; COLUMNS DENOTE THE EXECUTED OUTCOME. 

||**Cok**<br>|**e / Sprite /**<br>|**Fanta**<br>||||**Tape **<br>|**/ Mustard **|**/ Pringles**|||
|---|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**Instruction**|**Coke**|**Sprite**|**Fanta**|**Fail**|**Model**|**Instruction**|**Tape**|**Mustard**|**Pringles**|**Fail**|
||“Coke”|8/10|||||“Tape”|10/10||||
|_π_0_._5|“Sprite”||6/10|||_π_0_._5|“Mustard”|3/3|3/6|0/1||
||“Fanta”|1/1||6/9|||“Pringles”||1/2|2/8||
||“Coke”|9/10|||||“Tape”|9/10||||
|_π_0_._5 + CAG|“Sprite”||8/10|||_π_0_._5 + CAG|“Mustard”||6/10|||
||“Fanta”|||7/10|||“Pringles”|||4/10||


||**Mi**<br>|**ddle / Left / **<br>|**Right**<br>||||**Ta**<br>|**ble / Plate /**|**Bowl**|||
|---|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**Instruction**|**Middle**|**Left**|**Right**|**Fail**|**Model**|**Instruction**|**Table**|**Plate**|**Bowl**|**Fail**|
||“Middle”|9/10|||||“Table”|7/9|1/1|||
|_π_0_._5|“Left”|8/8|1/2|||_π_0_._5|“Plate”||6/8|2/2||
||“Right”|7/7||3/3|||“Bowl”||4/5|4/5||
||“Middle”|10/10|||||“Table”|8/10||||
|_π_0_._5 + CAG|“Left”|6/7|3/3|||_π_0_._5 + CAG|“Plate”||7/7|3/3||
||“Right”|4/5|1/1|4/4|||“Bowl”||3/4|6/6||


||**Sta**|**ck / Plate / **|**Basket**||||**Cup **|**/ Cube / Ba**|**sketball**|||
|---|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**Instruction**|**Stack**|**Plate**|**Basket**|**Fail**|**Model**|**Instruction**|**Cup**|**Cube**|**Basketball**|**Fail**|
||“Stack”|5/9|1/1||||“Cup”|9/10||||
|_π_0_._5|“Plate”|0/1|2/7||2|_π_0_._5|“Cube”|0/1|5/6|3/3||
||“Basket”|||2/10|||“Basketball”|3/3||6/7||
||“Stack”|7/10|||||“Cup”|9/10||||
|_π_0_._5 + CAG|“Plate”||7/10|||_π_0_._5 + CAG|“Cube”||8/9|1/1||
||“Basket”|||6/9|1||“Basketball”|1/2||7/8||


|||**Move and P**|**our**||||**App**|**le and Ba**|**nana**|||
|---|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**Instruction**|**Coke**|**Sprite**|**Fanta**|**Fail**|**Model**|**Instruction**|**A+B**|**B+A**|**A**|**Fail**|
|_π_0_._5|“Coke”<br>“Sprite”|5/9<br>1/2|0/1<br>5/8|||_π_0_._5|“Apple+Banana”<br>“Banana+Apple”|9/10<br>4/4|5/6|||
||“Fanta”|2/3||3/7|||“Apple+/”|8/8||2/2||
||“Coke”|6/9||1/1|||“Apple+Banana”|8/10||||
|_π_0_._5 + CAG|“Sprite”||5/10|||_π_0_._5 + CAG|“Banana+Apple”|2/3|4/7|||
||“Fanta”||1/1|3/9|||“Apple”|3/3||7/7||


REFERENCES 

_arXiv preprint arXiv:2412.04445_ , 2024. 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- [2] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- [3] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A visionlanguage-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [6] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- [7] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A largescale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 

- [8] Jun Cen, Siteng Huang, Yuqian Yuan, Kehan Li, Hangjie Yuan, Chaohui Yu, Yuming Jiang, Jiayan Guo, Xin Li, Hao Luo, et al. Rynnvla-002: A unified visionlanguage-action and world model. _arXiv preprint arXiv:2511.17502_ , 2025. 

- [9] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- [10] Chilam Cheang, Sijin Chen, Zhongren Cui, Yingdong Hu, Liqun Huang, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Xiao Ma, et al. Gr-3 technical report. _arXiv preprint arXiv:2507.15493_ , 2025. 

- [11] Yi Chen, Yuying Ge, Yizhuo Li, Yixiao Ge, Mingyu Ding, Ying Shan, and Xihui Liu. Moto: Latent motion token as the bridging language for robot manipulation. 

- [12] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _arXiv preprint arXiv:2303.04137_ , 2023. 

- [13] Contributors. Starvla: A lego-like codebase for visionlanguage-action model developing. GitHub repository, 1 2025. 

- [14] Can Cui, Pengxiang Ding, Wenxuan Song, Shuanghao Bai, Xinyang Tong, Zirui Ge, Runze Suo, Wanqi Zhou, Yang Liu, Bofang Jia, et al. Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation. _arXiv preprint arXiv:2505.03912_ , 2025. 

- [15] Shengliang Deng, Mi Yan, Songlin Wei, Haixin Ma, Yuxin Yang, Jiayi Chen, Zhiqi Zhang, Taoyu Yang, Xuheng Zhang, Wenhao Zhang, Heming Cui, Zhizheng Zhang, and He Wang. Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data. 2025. 

- [16] Cunxin Fan, Xiaosong Jia, Yihang Sun, Yixiao Wang, Jianglan Wei, Ziyang Gong, Xiangyu Zhao, Masayoshi Tomizuka, Xue Yang, Junchi Yan, et al. Interleave-vla: Enhancing robot manipulation with interleaved imagetext instructions. _arXiv preprint arXiv:2505.02152_ , 2025. 

- [17] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 

- [18] Catherine Glossop, William Chen, Arjun Bhorkar, Dhruv Shah, and Sergey Levine. Cast: Counterfactual labels improve instruction following in vision-language-action models. _arXiv preprint arXiv:2508.13446_ , 2025. 

- [19] Jonathan Ho and Tim Salimans. Classifier-free diffusion guidance. _arXiv preprint arXiv:2207.12598_ , 2022. 

- [20] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [21] Joel Jang, Seonghyeon Ye, Zongyu Lin, Jiannan Xiang, Johan Bjorck, Yu Fang, Fengyuan Hu, Spencer Huang, Kaushil Kundalia, Yen-Chen Lin, et al. Dreamgen: Unlocking generalization in robot learning through video world models. _arXiv preprint arXiv:2505.12705_ , 2025. 

- [22] Dong Jing, Xiaolong He, Yutian Luo, Nanyi Fei, Wei Wei, Huiwen Zhao, Zhiwu Lu, et al. Fineclip: Selfdistilled region-based clip for better fine-grained understanding. _Advances in Neural Information Processing Systems_ , 37:27896–27918, 2024. 

- [23] Dong Jing, Gang Wang, Jiaqi Liu, Weiliang Tang, Zelong Sun, Yunchao Yao, Zhenyu Wei, Yunhui Liu, Zhiwu Lu, and Mingyu Ding. Mixture of horizons in action chunking. _arXiv preprint arXiv:2511.19433_ , 2025. 

- [24] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, 

Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visuallyconditioned language models. In _Forty-first International Conference on Machine Learning_ , 2024. 

- [25] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- [26] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [27] Moo Jin Kim, Chelsea Finn, and Percy Liang. Finetuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- [28] Fuhao Li, Wenxuan Song, Han Zhao, Jingbo Wang, Pengxiang Ding, Donglin Wang, Long Zeng, and Haoang Li. Spatial forcing: Implicit spatial representation alignment for vision-language-action model. _arXiv preprint arXiv:2510.12276_ , 2025. 

- [29] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025. 

- [30] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 

- [31] Shijie Lian, Bin Yu, Xiaopeng Lin, Laurence T Yang, Zhaolong Shen, Changti Wu, Yuzhuo Miao, Cong Huang, and Kai Chen. Bayesianvla: Bayesian decomposition of vision language action models via latent action queries. _arXiv preprint arXiv:2601.15197_ , 2026. 

- [32] Junbang Liang, Pavel Tokmakov, Ruoshi Liu, Sruthi Sudhakar, Paarth Shah, Rares Ambrus, and Carl Vondrick. Video generators are robot policies. _arXiv preprint arXiv:2508.00795_ , 2025. 

- [33] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776– 44791, 2023. 

- [34] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-languageaction model. _arXiv preprint arXiv:2503.10631_ , 2025. 

- [35] Shi Liu, Kecheng Zheng, and Wei Chen. Paying more attention to image: A training-free method for alleviating 

hallucination in lvlms. In _European Conference on Computer Vision_ , pages 125–140. Springer, 2024. 

- [36] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- [37] Yulei Niu, Kaihua Tang, Hanwang Zhang, Zhiwu Lu, Xian-Sheng Hua, and Ji-Rong Wen. Counterfactual vqa: A cause-effect look at language bias. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 12700–12710, 2021. 

- [38] Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, et al. Open x-embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 

- [39] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 

- [40] Zhenghao Peng, Wenhao Ding, Yurong You, Yuxiao Chen, Wenjie Luo, Thomas Tian, Yulong Cao, Apoorva Sharma, Danfei Xu, Boris Ivanovic, et al. Counterfactual vla: Self-reflective vision-language-action model with adaptive reasoning. _arXiv preprint arXiv:2512.24426_ , 2025. 

- [41] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [42] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- [43] Simon Schrodi, David T Hoffmann, Max Argus, Volker Fischer, and Thomas Brox. Two effects, one trigger: On the modality gap, object bias, and information imbalance in contrastive vision-language models. _arXiv preprint arXiv:2404.07983_ , 2024. 

- [44] Yu Shang, Xin Zhang, Yinzhou Tang, Lei Jin, Chen Gao, Wei Wu, and Yong Li. Roboscape: Physics-informed embodied world model. _arXiv preprint arXiv:2506.23135_ , 2025. 

- [45] Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, et al. Hi robot: Open-ended instruction following with hierarchical vision-language-action models. _arXiv preprint arXiv:2502.19417_ , 2025. 

- [46] Weiliang Tang, Dong Jing, Jia-Hui Pan, Zhiwu Lu, Yun-Hui Liu, Li Erran Li, Mingyu Ding, and Chi- 

Wing Fu. Incentivizing multimodal reasoning in large models for direct robot manipulation. _arXiv preprint arXiv:2505.12744_ , 2025. 

- [47] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [48] Can Udomcharoenchaikit, Wuttikorn Ponwitayarat, Patomporn Payoungkhamdee, Kanruethai Masuk, Weerayut Buaphet, Ekapol Chuangsuwanich, and Sarana Nutanong. Mitigating spurious correlation in natural language understanding with counterfactual inference. In _Proceedings of the 2022 conference on empirical methods in natural language processing_ , pages 11308–11321, 2022. 

- [49] Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model. _arXiv preprint arXiv:2506.19850_ , 2025. 

- [50] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pretraining for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ , 2023. 

- [51] Kechun Xu, Zhenjie Zhu, Anzhe Chen, Shuqi Zhao, Qing Huang, Yifei Yang, Haojian Lu, Rong Xiong, Masayoshi Tomizuka, and Yue Wang. Seeing to act, prompting to specify: A bayesian factorization of vision language action policy. _arXiv preprint arXiv:2512.11218_ , 2025. 

- [52] An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, et al. Qwen2. 5 technical report. _arXiv preprint arXiv:2412.15115_ , 2024. 

_of Robotics: Science and Systems_ , Daegu, Republic of Korea, July 2023. doi: 10.15607/RSS.2023.XIX.016. 

   - [58] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, et al. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-languageaction model. _arXiv preprint arXiv:2510.10274_ , 2025. 

   - [59] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 

   - [60] Xu Zheng, Chenfei Liao, Yuqian Fu, Kaiyu Lei, Yuanhuiyi Lyu, Lutao Jiang, Bin Ren, Jialei Chen, Jiawen Wang, Chengxin Li, et al. Mllms are deeply affected by modality bias. _arXiv preprint arXiv:2505.18657_ , 2025. 

   - [61] Zhide Zhong, Haodong Yan, Junfeng Li, Xiangchen Liu, Xin Gong, Tianran Zhang, Wenxuan Song, Jiayi Chen, Xinhu Zheng, Hesheng Wang, and Haoang Li. Flowvla: Visual chain of thought-based motion reasoning for vision-language-action models. _arXiv preprint arXiv:2508.18269_ , 2025. 

   - [62] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. Minigpt-4: Enhancing visionlanguage understanding with advanced large language models. _arXiv preprint arXiv:2304.10592_ , 2023. 

   - [63] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. _arXiv preprint arXiv:2504.10479_ , 2025. 

- [53] Zhihao Zhan, Yuhao Chen, Jiaying Zhou, Qinhan Lv, Hao Liu, Keze Wang, Liang Lin, and Guangrun Wang. Stable language guidance for vision-language-action models. _arXiv preprint arXiv:2601.04052_ , 2026. 

- [54] Chenyu Zhang, Minsol Kim, Shohreh Ghorbani, Jingyao Wu, Rosalind Picard, Patricia Maes, and Paul Pu Liang. When one modality sabotages the others: A diagnostic lens on multimodal reasoning. _arXiv preprint arXiv:2511.02794_ , 2025. 

- [55] Jusheng Zhang, Kaitong Cai, Yijia Fan, Jian Wang, and Keze Wang. Cf-vlm: Counterfactual vision-language fine-tuning. _arXiv preprint arXiv:2506.17267_ , 2025. 

- [56] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, He Wang, Zhizheng Zhang, Li Yi, Wenjun Zeng, and Xin Jin. Dreamvla: A vision-language-action model dreamed with comprehensive world knowledge. _CoRR_ , abs/2507.04447, 2025. doi: 10.48550/ARXIV.2507. 04447. 

- [57] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware. In _Proceedings_ 

