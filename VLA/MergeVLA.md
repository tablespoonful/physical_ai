---
title: "MergeVLA: Cross-Skill Model Merging Toward a Generalist Vision-Language-Action Agent"
date: "2025-11-24"
authors: "Yuxia Fu; Zhizhen Zhang; Yuqi Zhang; Zijian Wang; Zi Huang; Yadan Luo"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2511.18810
pdf: https://arxiv.org/pdf/2511.18810
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.18810)** / [論文ページ](https://arxiv.org/abs/2511.18810)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 


# **: Cross-Skill Model Merging Toward a Generalist Vision-Language-Action Agent** 

Yuxia Fu<sup>*</sup> Zhizhen Zhang<sup>*</sup> Yuqi Zhang Zijian Wang Zi Huang Yadan Luo<sup>_†_</sup> UQMM Lab, The University of Queensland 

_{_ yuxia.fu, zhizhen.zhang, yuqi.zhang, zijian.wang, helen.huang, y.luo _}_ @uq.edu.au 

## **Abstract** 

## **1. Introduction** 

_Recent Vision-Language-Action (VLA) models reformulate vision-language models by tuning them with millions of robotic demonstrations. While they perform well when fine-tuned for a single embodiment or task family, extending them to multi-skill settings remains challenging: directly merging VLA experts trained on different tasks results in near-zero success rates. This raises a fundamental question: what prevents VLAs from mastering multiple skills within one model? With an empirical decomposition of learnable parameters during VLA fine-tuning, we identify two key sources of non-mergeability: (1) Finetuning drives LoRA adapters in the VLM backbone toward divergent, task-specific directions beyond the capacity of existing merging methods to unify. (2) Action experts develop interblock dependencies through self-attention feedback, causing task information to spread across layers and preventing modular recombination. To address these challenges, we present_ **_MergeVLA_** _, a merging-oriented VLA architecture that preserves mergeability by design. MergeVLA introduces sparsely activated LoRA adapters via task masks to retain consistent parameters and reduce irreconcilable conflicts in the VLM. Its action expert replaces self-attention with cross-attention-only blocks to keep specialization localized and composable. When the task is unknown, it uses a test-time task router to adaptively select the appropriate task mask and expert head from the initial observation, enabling unsupervised task inference. Across LIBERO, LIBERO-Plus, RoboTwin, and multi-task experiments on the real SO101 robotic arm, MergeVLA achieves performance comparable to or even exceeding individually finetuned experts, demonstrating robust generalization across tasks, embodiments, and environments. Project page: https://mergevla.github.io/_ 

> *Equal contribution.<sup>_†_</sup> Corresponding author. 

Vision-Language-Action (VLA) models [2–4, 17, 18, 22, 27, 28, 39, 40, 49, 56, 66] have recently enabled robot agents to perform complex manipulation tasks by finetuning large vision-language models (VLMs) with millions of robotic demonstrations. By reformulating action learning as a language generation or policy decoding problem, VLA models inherit broad visual grounding and semantic understanding from VLMs, and have shown notable performance in single-task or single-embodiment settings. However, real-world generalist agents must support _multiple_ skills, embodiments, and environments, requiring the ability to consolidate many independently fine-tuned VLA models into a single unified policy. 

A natural approach is _model merging_ , which has proven effective in large language and vision models [8, 20, 21, 34, 41, 51, 59–61]. Those techniques can integrate multiple specialized models without joint retraining or revisiting their original datasets. Yet, when these approaches are applied to VLA experts fine-tuned on distinct manipulation tasks, the merged model exhibits **near-zero** success rate. This failure suggests that VLA finetuning induces structural specialization incompatible across tasks, which is rarely observed in conventional VLM merging. 

To uncover the root causes, as shown in Figure 1, we perform a fine-grained decomposition of trainable parameters across representative VLA architectures and identify two major sources of _non-mergeability_ : First, LoRA updates [19] within the VLM backbone diverge sharply across tasks. Each manipulation task reshapes the pretrained representation space to satisfy its own perception-control alignment. Direct averaging [21, 41] or sign-resolved merging [51] thus reactivates irrelevant or even contradictory parameters, corrupting shared vision-language subspaces and degrading task-invariant semantics. Second, the train-fromscratch action decoders accumulate strong task-specific dependencies across blocks through self-attention feedback. This coupling spreads localized task information globally, breaking modularity and preventing compositional merging 

22335 

even under identical architectures and initialization. 

Built upon these findings, we introduce **MergeVLA** , a merge–oriented VLA architecture that preserves mergeability by design. When executing a specific task, MergeVLA applies sparsely activated LoRA adapters, implemented via task masks, to selectively activate the merged parameters contributing to task-relevant responses while suppressing those that mislead other tasks. Moreover, MergeVLA reconfigures the action expert to remove self-attention propagation, relying solely on cross-attention pathways. This eliminates the sustained accumulation of task dependence across blocks, allowing most layers to be effectively merged using simple weight averaging. Due to these architectural modifications, it surprisingly shows strong out-ofdistribution (OOD) generalization by 13.4% higher success rate than VLA-Adapter under varying corruptions. However, the deeper blocks of the action expert, referred to as the _expert head_ , remain unmergeable due to their strong task specialization. Consequently, each task keeps its own expert head, which in practice is typically the final block _L_ . To address the challenge of _mixed-task evaluation_ [20, 41], where the task identity is unknown at inference time, we adopt a training-free _test-time task router_ that identifies the most relevant task directly from the input features. For each candidate task, the router runs the VLM with its corresponding task mask to obtain its hidden states, and then measures its response against principal components extracted from the value projections of a shared merged action expert. It selects the task with the highest response and activates the associated task mask and expert head. This allows MergeVLA to generalize to different tasks without additional supervision, enabling a single merged model to adaptively activate the right skill components for execution. 

Extensive experiments show that MergeVLA achieves success rates of **90** _._ **2** %, **62** _._ **5** %, and **70** _._ **7** % on the LIBERO [31], LIBERO-Plus [14], and RoboTwin [6] benchmarks under the _mixed-task_ evaluation setting, and **90** _._ **0** % on real-world experiments with the SO101 robotic arm, demonstrating its effectiveness and robustness across cross-skill, cross-environment, and cross-embodiment evaluations. These results show that model merging is not only feasible for VLAs, but can serve as a scalable path toward generalist embodied agents. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

Recent VLA models build on large-scale VLMs [26, 29, 53, 64] pretrained on internet data to leverage the commonsense knowledge [33, 57, 63], and are fine-tuned on largescale robotic trajectory data [4, 38, 45, 66] in an end-toend manner to obtain more generalizable visuomotor policies [1, 4, 13, 24, 25, 45, 66]. Among them, OpenVLA [27] 


Figure 1. **Comparison between the structures of different VLAs.** OpenVLA uses a standard VLM for token-based action generation. VLA-Adapter adds an action expert with cross- and self-attention layers. MergeVLA simplifies this design by removing non-mergeable self-attention layers for effective merging. 

is a widely used open-source model based on Prismatic7B [26], which discretizes robot actions into rarely used vocabulary tokens and generates them autoregressively. Similarly, _π_ 0 [3] builds on existing VLMs with a dual-system VLA architecture, introducing a lightweight action expert that uses conditional flow matching to generate continuous action chunks for faster inference. Building on this, _π_ 0 _._ 5 [22] retains the text-generation ability of the VLM, enabling simultaneous high-level subtask descriptions and low-level action prediction. Recently, VLA-Adapter [47] proposed a 0.5B-parameter dual-system model that coordinates the VLM and action expert through a novel mechanism, employing chunk-wise autoregressive generation for faster inference and strong performance at a small scale. While existing VLAs perform well on widely used robotic benchmarks [6, 31, 36, 44], their multi-task ability relies on joint training [3, 22, 27, 47], making them inefficient. Besides, their tightly coupled dual systems [3, 5, 9, 47, 62] also hinder model merging. 

### **2.2. Model Merging** 

Model merging [7, 54, 55] enables efficient knowledge reuse by combining existing model weights to construct a unified model capable of performing multiple tasks. Early studies [15, 23, 35, 37, 50] showed that simple weighted averaging of checkpoints can improve performance and introduce multi-task capability. Task Arithmetic (TA) [21] treats the parameter difference between fine-tuned and pretrained models as a task vector and merges them to integrate task-specific knowledge. Nonetheless, it overlooks various conflicts that may arise among different task vectors. Subsequent methods [8, 10, 12, 42, 51, 58, 59] handle conflicts via parameter pruning or rescaling, whereas subspacebased ones [16, 32, 34, 41] apply low-rank decomposition ( _e.g.,_ SVD) for more consistent merging. Other studies [41, 60, 61, 65] design merging methods specifically for parameter-efficient fine-tuning (PEFT) [19, 30] modules. In contrast to these pre-merge approaches, methods like [20, 32, 43, 46, 52] perform test-time [48] merging 

22336 


Figure 2. **Overview of MergeVLA architecture.** (1) To address destructive LoRA parameter interference in finetuned VLM, task masks are applied to all merged LoRA modules to selectively activate the merged parameters contributing to task-relevant responses while suppressing those that mislead other tasks. (2) To solve the incompatibility of action experts, the architecture is redesigned to contain only cross-attention blocks and use sigmoid gate to preserve and rely on robust VLM features. Most blocks then can be merged except deeper blocks named **expert head** are left unmerged due to their task specification. (3) To address the setting where the task identity is unknown at inference time, a training-free test-time task router is adopted to dynamically select task-specified components by computing task relevance from VLM hidden states in the value-based subspace of the merged action expert. 

to handle severe task interference, substantially improving performance. Yet, little work has explored model merging in VLA models. The recent ReVLA [11] applies merging to gradually reverse the vision backbone to mitigate visual catastrophic forgetting and enhance domain generalization, rather than to enable multi-task VLA capabilities. To bridge this gap, we propose MergeVLA which enables lightweight multi-task robotic learning. 

## **3. Preliminary** 

**Task Formulation.** We consider a collection of singleskill imitation learning datasets D = _{Dm}_<sup>_M_</sup> _m_ =1<sup>where</sup> each dataset _Dm_ corresponds to a distinct manipulation task. Each training set is denoted as _Dm_ = _{_ **I**<sup>_v_</sup> _t_<sup>_,_</sup><sup>**I**</sup><sup>_w_</sup> _t_<sup>_, L}T_</sup> _t_ =1<sup>,</sup> where **I**<sup>_v_</sup> _t_<sup>isthethird-personviewimage,</sup><sup>**I**</sup><sup>_w_</sup> _t_ the wristmounted image, _L_ the task instruction at each time step _t_ . Finetuning a pretrained VLA model on each dataset yields _M_ task-specific weights. The objective of model merging is to unify task-specific _{_ Θ1 _, . . . ,_ Θ _M }_ into a single general agent Θmerge without retraining. 

**VLA Architectures.** Figure 1 illustrates the architectures of different VLAs. Some VLA models [27, 28, 39, 49, 56] directly build upon existing VLMs, where only the language component is _non-mergeable_ as refered to our experiments in Table 1. Others introduce an additional action expert [3, 22, 47], among which VLA-Adapter trains its action expert from scratch. However, this tightly coupled dual-system design makes the overall model difficult to merge. MergeVLA simplifies this structure by removing the non-mergeable self-attention layers, enabling all components except the expert head to be merged effectively. 

## **4. Our Approach: MergeVLA** 

Finetuning VLA models on individual manipulation tasks, while effective, produces isolated experts that cannot be trivially merged. As discussed in Section 5.2, applying standard model merging approaches to VLA specialists trained on LIBERO [31] results in a complete breakdown, with all merged variants achieving **zero success rate** . This failure is unexpected given the success of merging strategies in language-only and vision-language domains, and suggests that VLA merging presents a _more severe_ challenge. To understand this phenomenon, we conduct a systematic analysis of the parameter space and architectural behavior of mainstream VLAs. Our findings, as depicted in Figure 3, show that VLA unmergeability arises from two complementary failure modes: 

1. **Destructive LoRA Parameter Interference** : As shown in the left plot, task-specific LoRA updates activate largely disjoint subsets of channels. When merging only four tasks, the proportion of _parameters that are relevant to exactly one task_ ( _i.e.,_ selfish parameters) already exceeds 75%. Such extreme task exclusivity produces severe parameter conflicts, which directly cause na¨ıve model-merging strategies to fail. 

2. **Architectural Incompatibility of Action Experts** : More critically, resolving LoRA interference is necessary but not sufficient. Even when the VLM is perfectly merged, simply averaging the action experts in architectures such as VLA-Adapter [47] still yields 0% success. The right plot explains why: although the shallow blocks remain moderately aligned across tasks, the pa- 

22337 

rameter distance _explodes_ in the final layers. Such divergence arises because the action expert is trained entirely from scratch and contains self-attention layers that accumulate task-specific differences over depth. Instead of providing modular transformations, these layers propagate and amplify task-dependent signals, causing deeper blocks to become pathologically specialized to individual tasks. As a result, their parameters are inherently _irreconcilable_ under any merging scheme. 

Additionally, prior merging studies [20, 41] also note that the _mixed-task_ setting is considerably more challenging than per-task evaluation, where the task identity is unknown. In practice, many approaches rely on hand-picked priors, _e.g.,_ task identity or an expert-specific prompt, to perform well, and degrade rapidly without them. Motivated by these insights, we therefore structure **MergeVLA** as a unified framework that addresses these challenges by: (1) Stabilizing VLM merging via task-specific masking (Sec 4.1) to address extreme LoRA parameter conflict ( **Q1** ); (2) redesigning the action expert (Sec 4.2) to mitigate architectural incompatibility ( **Q2** ); (3) introducing a learning-free task routing mechanism (Sec 4.3) to enable operation without a task identity at test time ( **Q3** ). 

### **4.1. Task Conflicts in LoRA-Finetuned VLM** 

To address **Q1** , we first consider a standard LoRA update. Let Θ0 denote the pretrained checkpoint and Θ _m_ the LoRAfinetuned weights after finetuning on task _m ∈{_ 1 _, . . . , M }_ . The task vector for task _m_ is defined as _τm_ = Θ _m −_ Θ0. Most data-free methods _R_ ( _·_ ) construct a single merged update _τ_ merge by merging the updates [16, 20, 21, 41, 51]: 


where _α_ is the scaling factor. As _τ_ merge is unusable directly due to the conflicts we identified, we therefore move beyond a single global update. We leverage a task-specific binary masking strategy **S** _m_ that isolates components in Θmerge beneficial to task _m_ , while suppressing those encoding conflicts. Formally, 


where _⊙_ denotes element-wise multiplication. The mask **S** _m_ is constructed by a _parameter-level consistency_ test: A parameter is retained if and only if its task-specific _τm_ is both (1) significant and (2) dominant over the scaled residual difference with _τ_ merge, indicating that it aligns with the overall merge and contributes positively to task _m_ : 


where I[ _·_ ] is the indicator function that returns 1 if the condition is true and 0 otherwise, and mask ratio _λ_ controls the tolerance for disagreement. This principled approach of 


Figure 3. **Left:** Selfish ratio of the masks from TA [21] and TIES [51] by merging different numbers of tasks. The selfish ratio is computed following Equation 4. **Right:** The average relative L2 distance across blocks between all pairs of action experts. 

pruning parameters based on their alignment consistency, adapted here for LoRA merging, shares its core formulation with task-vector compression methods [46]. 

**Analysis of Parameter Selfishness.** Based on this formulation, we compute the proportion of _selfish parameters_ , namely those _retained by exactly on_ e task mask: 


Empirically, as Figure 3 (left) shows, this selfish ratio on LIBERO for two merging methods as the number of merged tasks increases from 2 to 4. In all cases, ratioselfish rises at around 75%, indicating that most parameters are selfish (kept exclusively by a single task) and underscoring the importance of task-specific masking to mitigate cross-task interference. Notably, applying the task mask encourages some LoRA-finetuned parameters to revert toward their pretrained weights, improving merge stability. A similar effect was observed in ReVLA [11], where VLA finetuning was shown to overwrite pretrained visual knowledge. This forgetting becomes more pronounced when multiple experts are merged, as conflicting task updates distort the shared feature space. By sparsely activating merged LoRA parameters through the proposed mask, MergeVLA preserves pretrained visual–language representations and mitigates cross-task conflicts, enabling more consistent and stable merging across tasks. 

### **4.2. Redesigning the Action Expert for Mergeability** 

Our diagnosis proved that stabilizing the VLM ( **Q1** ) is insufficient; the action expert itself is a fundamental barrier ( **Q2** ). As shown in Section 5.2, applying only the LoRA task mask still results in **0% success rate** . Our analysis pinpoints the incompatibility with the VLA-Adapter [47] architecture (Fig. 1), which consists of _L_ transformer blocks trained from scratch. Each block contains a _self-attention_ layer on the block input **x**<sup>_i_</sup> , two _cross-attention_ layers conditioned on the VLM-provided hidden states **h**<sup>_i_</sup> T<sup>(task) and</sup> **h**<sup>_i_</sup> A<sup>(action),andafeed-forwardnetwork(FFN).Agating</sup> 

22338 

function is applied to the task stream, _i.e._ , **h**<sup>ˆ</sup><sup>_i_</sup> T<sup>=</sup><sup>_g_(</sup><sup>**h**</sup> T<sup>_i_),</sup> with _g_ ( _·_ ) implemented as tanh. 

Different from its flawed design, MergeVLA’s redesign (Fig. 2) is a principled response to nonmergeability diagnosis, introducing two key modifications: 

- **Remove Self-Attention:** We eliminate the self-attention layers, retaining cross-attention _only_ . Since the expert is trained from scratch, self-attention layers develop strong, task-specific biases that are irreconcilable. Removing them forces the expert to rely on the robust, shared VLM features. 

- **Replace Gating:** We replace the tanh gate with a sigmoid gate. The original tanh gate can suppress VLM signals via negative activations, forcing the expert to rely on its own scratch-trained (and task-specific) parameters. sigmoid ensures VLM information is always preserved and balanced. 

These two architectural changes alone are remarkably effective, achieving a _13.4%_ higher success rate on the out-ofdistribution (OOD) LIBERO-Plus [14] testbed. This confirms our new design better leverages the VLM’s _robustness_ and is inherently more _generalizable_ . 

**Merging via Specialization Hierarchy.** Since the action expert is trained from scratch, existing task vector-based merging approaches are inapplicable here, as there is no shared initialization among different experts. Therefore, we adopt a simple weight-averaging strategy to merge the parameters of the action experts across tasks. We observe that such averaging works surprisingly well for the _shallow_ blocks of the action expert. However, it fails for the _deeper_ blocks, where the parameter discrepancy tasks increase sharply. 

This reflects strong task-specific specialization, and we refer to these divergent layers collectively as the **expert head** , denoted as **H**<sup>_l→L_</sup> , spanning blocks _l_ through _L_ . In most cases, _l_ = _L_ , meaning that only the final block requires separate handling. We hypothesize that under regression-based training objectives, each expert head becomes _highly specialized_ to the action distribution of its corresponding task. Even _small_ discrepancies between these distributions can lead to incompatible weights, making simple parameter averaging ineffective. This effect is particularly pronounced in fine-grained manipulation tasks, where minor output deviations can cause entire trajectories to fail. Therefore, we leave the expert heads _unmerged_ and allow the model to use the corresponding head for each task. 

### **4.3. Test-time Task Routing** 

When the task identity is known, MergeVLA can already accomplish each skill by manually selecting the corresponding task mask **S** _m_ and expert head **H**<sup>_l_</sup> _m_<sup>_→L_</sup> . However, to operate without a known task identity ( **Q3** ) at inference time, the model must dynamically select these components 

based solely on the input observations, enabling _cross-skill_ ability at a _joint-task_ level [41]. To this end, we propose a test-time task routing mechanism that infers task relevance directly from the model’s internal parameter subspaces, inspired by recent observations that fine-tuning pushes different tasks into distinguishable parameter subspaces [43]. Given the merged LoRA parameters _τ_ merge and task masks _{_ **S** _m}_<sup>_M_</sup> _m_ =1<sup>, we obtain</sup><sup>_M_masked VLM variants by applying</sup> each mask to the merged weights: 


Each masked VLM produces hidden states � **h**<sup>_l_</sup> T<sup>_,_</sup><sup>**h**</sup><sup>_l_</sup> A� from block _l_ , which is then forwarded to the corresponding _l_ -th block of the action expert. Inside this block, two cross-attention paths are present: one conditioned on the task hidden state **h** T<sup>_l_withparameters(</sup><sup>**Q**</sup> T<sup>_l,_</sup><sup>**K**</sup> T<sup>_l,_</sup><sup>**V**</sup> T<sup>_l_),and</sup> the other conditioned on the action hidden state **h** A<sup>_l_with</sup> ( **Q** A<sup>_l,_</sup><sup>**K**</sup> A<sup>_l,_</sup><sup>**V**</sup> A<sup>_l_).</sup> 

A key design choice is _which_ subspace to use for routing. We hypothesize that query **Q** and **K** govern attentional selection, thus being sensitive to input scaling and risk collapsing into task-specific subspaces. Empirically, _value-based_ subspaces provide more stable and discriminative signals for routing, as they directly encode the taskdependent information written into the hidden states. We therefore analyze the principal components of the value projection matrices **V** of the _l_ -th block for both paths via singular value decomposition (SVD): 


We retain the top- _kr_ right singular vectors in each path to form the dominant content components of the expert subspace: **P** T<sup>_l∈_R</sup><sup>_kr×d,_</sup><sup>**P**</sup><sup>_l_</sup> A<sup>_∈_R</sup><sup>_kr×d,_formedbytakingthe</sup> first _kr_ rows of ( **R** T<sup>_l_)</sup><sup>_⊤_and (</sup><sup>**R**</sup> A<sup>_l_)</sup><sup>_⊤_, respectively.For each</sup> task _m_ , the hidden state from its masked VLM is projected onto these two subspaces to measure its _activation strength_ , 


Let **r** T _,_ **r** A _∈_ R<sup>_M_</sup> collect the scores _{r_ T _,m}m_<sup>_M_</sup> =1<sup>and</sup> _{r_ A _,m}m_<sup>_M_</sup> =1<sup>, respectively.Here, the combined score vector</sup> is given by **r** =<sup><u>1</u></sup> 2 � **r** T + **r** A�. The routing probabilities are calculated by softmax _pm_ = softmax( **r** ) _m._ Then we can use arg max _m pm_ to choose the task index _m_<sup>_∗_</sup> . Once _m_<sup>_∗_</sup> is determined, the model uses the corresponding task mask **S** _m∗_ and expert head H<sup>_l_</sup> _m_<sup>_→∗L_</sup> to perform the forward pass. This design allows the router to infer the underlying task purely from the input-driven hidden representations of the masked VLMs, without any additional training or supervision. In practice, we find that a _single routing step_ using the initial observation at _t_ =0 is sufficient to identify the correct 

22339 

task. The selected task mask and expert head are then fixed for the rest of the episode, avoiding repeated routing during inference. Although this mechanism requires maintaining _M_ task masks and their corresponding action heads, the additional computational and parameter overhead is minimal. 

## **5. Experiments** 

### **5.1. Experimental Setup** 

**Simulation Benchmarks.** We evaluate MergeVLA on three simulation benchmarks: 

- **LIBERO** [31] is a comprehensive benchmark consisting of four distinct task suites: Spatial, Object, Goal, and Long. The benchmark enables the assessment of the robot’s multiskill competence, including spatial relationships, object interactions, and task-specific objectives. 

- **LIBERO-Plus** [14] builds upon the original LIBERO benchmark by introducing seven distinct perturbations, as shown in Figure 4. The benchmark comprises 10,030 tasks, providing diverse settings for evaluating model generalization and robustness under shifts. 

- **RoboTwin 2.0** [6] serves as a cross-embodiment benchmark for dual-arm manipulation. As shown in Figure 5, we select three embodiments and four tasks for a comprehensive assessment of the cross-embodiment cross-skill ability. - **Real-World Experiments** are provided in the Appendix. 


Figure 4. Seven perturbation types in the **LIBERO-Plus** benchmark, used to evaluate robustness under visual and language shifts. 


Figure 5. Experimental setup in the **RoboTwin** environment, featuring three robotic embodiments and a suite of manipulation tasks for cross-embodiment evaluation. 

MergeVLA enables efficient knowledge reuse and strong multi-task performance with a compact VLA model. 

### **5.3. Results on LIBERO-Plus** 

### **5.2. Results on LIBERO** 

We first reproduce results of OpenVLA [27] and VLAAdapter [47] on four tasks, as highlighted in grey in Table 1. OpenVLA performs notably worse than the others, with an average success rate of 76.5% and only 53.7% on the longhorizon LIBERO-Long task. Our MergeVLA, modified from VLA-Adapter to be merge-friendly, achieves comparable fine-tuning performance, indicating that our structural changes preserve the original capability. We have tried evaluating single-task finetuned models on unseen tasks ( _e.g.,_ testing a Spatial expert on the Object suite), all methods achieve _0%_ success across tasks. This suggests that existing VLA models lack cross-skill generalization. The lower part of Table 1 reports the merging results. Directly applying TA [21] to OpenVLA fails entirely, while merging only the vision and projector components improves to 44.2%. Adding a task-specific mask further raises the average success rate to 62.4%, though performance remains unbalanced. On VLA-Adapter, tight coupling between the VLM and action expert makes merging difficult even with masking, unless the final action block is excluded. As shown in the blue-highlighted rows, our MergeVLA consistently outperforms other merging baselines. With TIES [51] and WUDI [8], it achieves balanced results across all four tasks (Avg. 90.2%) , while remaining lightweight and only 6.5% below fine-tuning performance. These results confirm that 

Experiments on the LIBERO benchmark verify that MergeVLA achieves strong cross-task performance within known environments. To further examine the model’s _generalization and robustness to unseen scenes_ , we conduct additional evaluations on **LIBERO-Plus** , a variant of LIBERO that introduces controlled distribution shifts in both visual appearance and language descriptions. We use the same models trained on LIBERO and directly test them on the shifted LIBERO-Plus environments without any additional finetuning. This setting allows us to rigorously assess MergeVLA’s ability to maintain performance under out-of-distribution visual and linguistic conditions. 

From Table 2, we first observe that when using singletask finetuned checkpoints evaluated on their own tasks, MergeVLA exhibits stronger robustness under various perturbations than existing VLA models. This improvement stems from its architecture design, which preserves the pretrained VLM’s inherent robustness to visual and language perturbations. Secondly, in the model-merging setting, we find that applying different merging methods with MergeVLA maintains similar robustness even under crosstask evaluation. Notably, when using TA and TIES merging, the merged model even surpasses OpenVLA, _π_ 0, and VLAAdapter in the single-task setting, demonstrating that our MergeVLA can effectively transfer and preserve robustness across tasks. 

22340 

Table 1. **LIBERO results across task splits.** Comparison between finetuned and merged variants of MergeVLA. All numbers are success rates (%). **S** indicates that task masks are used during merging. “Params (B)” denotes the total number of model parameters (in billions) required to evaluate on all four tasks, including the LLM backbone and the action expert. Gray-highlighted rows correspond to per-task finetuned checkpoints evaluated on their own tasks, serving as upper-bound references for model merging. 

|**Method**|**Merge Method**|**Merge Part**|**Params (B)**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|---|---|---|
|**Single-task Finetune**|**d Model**||||||||
|OpenVLA[27]|-|-|7_×_4|84.7|88.4|79.2|53.7|76.5|
|VLA-Adapter[47]|-|-|0.68_×_4|99.6|99.6|98.2|96.4|98.5|
|MergeVLA|-|-|0.68_×_4|98.0|98.6|95.0|95.0|96.7|
|**Merged Model**|||||||||
|OpenVLA|TA [21]|Vision Backbones|7_×_4|56.6|58.0|55.6|6.6|44.2|
|OpenVLA|TA [21]|All|7|0.0|0.0|0.0|0.0|0.0|
|OpenVLA|TA [21] +**S**|All|7|74.2|82.6|68.8|24.0|62.4|
|VLA-Adapter|TA [21]|All|0.68|0.0|0.0|0.0|0.0|0.0|
|VLA-Adapter|TA [21] +**S**|All|0.68|0.0|0.0|0.0|0.0|0.0|
|VLA-Adapter|TA [21] +**S**|Except**H**<sup>_L→L_</sup>|0.70|50.2|34.6|0.0|7.4|23.1|
|MergeVLAEMR|EMR [20]|||96.0|63.2|62.0|40.6|65.5|
|MergeVLATSV|TSV [16] +**S**|||**99.4**|97.8|74.4|54.8|81.6|
|MergeVLAKnOTS|KnOTS[41] +**S**|||96.8|98.8|84.8|71.4|88.0|
|MergeVLATA|TA [21] +**S**|Except**H**<sup>_L→L_</sup>|0.70|98.0|**98.8**|85.4|76.6|89.7|
|MergeVLAWUDI|WUDI [8] +**S**|||97.6|98.2|85.6|78.2|89.9|
|MergeVLATIES|TIES [51] +**S**|||94.8|94.6|**91.8**|**79.4**|**90.2**|


Table 2. **Robustness of different models under visual and language shifts on LIBERO-Plus.** All results are success rates (%) averaged over 4 task suites. Gray-highlighted rows correspond to per-task finetuned checkpoints evaluated on their own tasks, serving as upperbound references for model merging. **Shift definitions:** S1 – Background Textures; S2 – Camera Viewpoints; S3 – Language Instructions; S4 – Lighting Conditions; S5 – Object Layout; S6 – Robot States; S7 – Sensor Noise. 

|**Method**|**S1**|**S2**|**S3**|**S4**|**S5**|**S6**|**S7**|**Avg.**|
|---|---|---|---|---|---|---|---|---|
|**Single-task Finetuned**|**Model**||||||||
|OpenVLA[27]|34.8|0.8|23.0|8.1|28.5|3.5|15.2|16.3|
|_π_0 [3]|81.4|13.8|58.8|85.0|68.9|6.9|**79.0**|56.3|
|VLA-Adapter[47]|76.6|36.4|73.8|71.0|70.2|37.4|57.2|59.0|
|MergeVLA|92.7|**62.4**|75.7|**92.7**|73.7|**46.4**|74.7|**72.4**|
|**Merged Model**|||||||||
|VLA-Adapter[47]|15.7|6.6|17.6|11.2|15.0|4.1|7.1|10.8|
|MergeVLATSV|64.3|44.8|58.8|72.9|59.4|30.4|52.7|53.5|
|MergeVLATA|78.2|**53.1**|**68.4**|79.0|65.0|**34.6**|62.7|61.6|
|MergeVLATIES|**85.7**|50.7|66.0|**84.2**|**68.1**|30.3|**66.0**|**62.5**|


### **5.4. Results on RoboTwin** 

While evaluations on the LIBERO and LIBERO-Plus benchmarks demonstrate that MergeVLA attains high performance and robustness in cross-task settings, these tests are limited to a single embodiment. To examine the effectiveness of MergeVLA under _cross-embodiment merging_ , we selected **RoboTwin-2.0** as our evaluation platform, since it supports multiple dual-arm robots and enables a broad assessment of generalization across hardware. Specifically, we designed two experimental settings: _A:_ Three dual-arm robots, Aloha-Agilex, ARX-X5, and Piper, each perform the same manipulation task PLACE CONTAINER PLATE. _B:_ The same three robots each per- 

form a different task: PLACE CONTAINER PLATE, HANDOVER BLOCK, and OPEN MICROWAVE, respectively. For each combination of _{_ embodiment,task _}_ , we collected 50 demonstration trajectories for finetuning. We report the success rate of (i) single- _{_ task, embodiment _}_ fine-tuned models, and (ii) merged models obtained using TA and TIES strategies under the MergeVLA framework. The detailed results are presented in Table 3, where each result is the success rate over 50 trials. Unlike the experiments on LIBERO and LIBERO-Plus, merging across different embodiments in RoboTwin poses a greater challenge for the test-time task router. We find that only keeping the final block _L_ as expert head is insufficient, as embodiment-specific differences in 

22341 

Table 3. **RoboTwin success rates (%) of different variants of MergeVLA across embodiments and tasks. T** 1: PLACE CONTAINER PLATE, **T** 2: HANDOVER BLOCK, **T** 3: OPEN MICROWAVE. Gray-highlighted rows correspond to per-task finetuned checkpoints evaluated on their own tasks. 

|_Setting A:_**_Cross em_**|**_bodiment_**|**_s_**_, Single_|_task_||
|---|---|---|---|---|
|**Method**|Aloha|**T**1<br>ARX|Piper|Avg.|
|Single-task Finetuned|90.0|90.0|84.0|88.0|
|MergeVLATA_,_**H**(_L−_1)_→L_|86.0|82.0|68.0|78.7|
|MergeVLATIES_,_**H**(_L−_1)_→L_|**88.0**|**92.0**|**86.0**|**88.7**|
|_Setting B:_**_Cross em_**|**_bodiment_**|**_s, Cross_**|**_task_**||
|**Method**|**T**1<br>Aloha|**T**2<br>ARX|**T**3<br>Piper|Avg.|
|Single-task Finetuned|90.0|46.0|92.0|76.0|
|MergeVLATA_,_**H**(_L−_1)_→L_|80.0|0.0|66.0|48.7|
|MergeVLATA_,_**H**(_L−_2)_→L_|82.0|0.0|66.0|49.3|
|MergeVLATIES_,_**H**(_L−_1)_→L_|**90.0**|0.0|**88.0**|59.3|
|MergeVLATIES_,_**H**(_L−_2)_→L_|88.0|**38.0**|86.0|**70.7**|


morphology and action space introduce stronger specialization and conflicts within the action heads. For _Setting A_ , routing **H**<sup>(</sup><sup>_L−_1)</sup><sup>_→L_</sup> preserves the performance of individually finetuned policies, indicating that the earlier merged blocks still capture transferable knowledge across different embodiments. For _Setting B_ , routing **H**<sup>(</sup><sup>_L−_2)</sup><sup>_→L_</sup> and TIES merging are need to maintain comparable performance, especially for the HANDOVER BLOCK task, which requires coordinated dual-arm motion and thus induces stronger conflicts in the action space. Overall, these findings highlight MergeVLA’s ability for cross-embodiment generalization. 

### **5.5. Ablation Study** 

**Impact of Mask Ratio.** We analyze the effect of the task mask under different _λ_ , which controls the active ratio of the mask. We vary _λ_ from 0.2 to 0.9 and obtain the merged task vector using Task Arithmetic (TA). Figure 6 (a) shows the active ratio of the mask across four tasks. As _λ_ increases, fewer parameters remain active, with the LIBERO-Spatial task consistently showing the highest activation ratio, indicating its dominant weight contribution. We further evaluate the impact of _λ_ on the model’s performance in the LIBERO-Long task, as shown in Figure 6 (b). When _λ_ is small ( _e.g.,_ 0.2), the mask activates too many parameters, leading to severe task interference and even complete failure. In contrast, when _λ_ lies between 0.6 and 0.9, the success rate exceeds 70%. These results suggest that moderate sparsity enables an effective balance between taskspecific and merged task vectors. When the parameter differences across tasks are large, relying more on the pretrained model yields better results, whereas emphasizing the 


Figure 6. The ablation study and analysis of _λ_ . (a) The mask active ratio across different _λ_ of LIBERO. (b) The success rate across different _λ_ of LIBERO-Long. 

Table 4. Ablation results of MergeVLA with different subspaces used for routing on LIBERO. 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|Only**K**|**98.0**|0.0|39.6|**76.6**|53.6|
|**K**&**V**|**98.0**|0.0|**85.8**|**76.6**|65.1|
|Only**V**|**98.0**|**98.8**|85.4|**76.6**|**89.7**|


merged task vector becomes effective only when the taskspecific weights dominate. 

**Impact of the Subspace Used for Routing.** To validate our task router design, we experiment on all four LIBERO task suites using three configurations: (1) using **K** projections, (2) using **V** projections, and (3) using **K** and **V** projections jointly, while fixing _λ_ = 0 _._ 6 for the task-specific mask and adopting TA for VLM merging. The results are summarized in Table 4. We observe that for Spatial and Long tasks, the choice of projection combination has little effect on performance. Yet, for Object and Goal, using only **K** or combining **K** and **V** leads to a dramatic drop in success rate, and even complete failure in some cases. By inspecting the router’s task selection, we find that when using **K** , the router tends to misassign tasks. From the perspective of attention interaction, the value projection captures the actual behavioral semantics retrieved by the query, whereas the key projection primarily defines the similarity structure of the query. Consequently, value-based alignment provides a more reliable indicator of task identity. 

## **6. Conclusion** 

The lack of cross-skill capability in existing VLA models remains a critical yet unexplored challenge. We show that current model merging techniques cannot be directly applied to VLAs due to destructive LoRA parameter interference and architectural incompatibility of action experts. We propose MergeVLA, a framework for merging VLA models that is compatible with mainstream merging methods toward an embodied generalist. Experiments across three benchmarks demonstrate MergeVLA’s strong multitask ability and robustness under distribution shifts, with transferability across embodiments. Future work will explore this promising direction further, including whether larger VLM backbones remain compatible with our framework and whether pretraining on diverse robot datasets can further enhance merging effectiveness. 

22342 

## **7. Acknowledgments** 

This work was partially supported by ARC DE240100105, DP240101814, DP230101196, BA24006, and ARC Industrial Transformation Research Hubs IH230100013. 

## **References** 

- [1] Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham Tulsiani, and Vikash Kumar. Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. In _IEEE International Conference on Robotics and Automation, ICRA 2024, Yokohama, Japan, May 13-17, 2024_ , pages 4788– 4795. IEEE, 2024. 2 

- [2] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith LLontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. GR00T N1: an open foundation model for generalist humanoid robots. _CoRR_ , abs/2503.14734, 2025. 1 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control. _CoRR_ , abs/2410.24164, 2024. 2, 3, 7 

- [4] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alexander Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil J. Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Kuang-Huei Lee, Sergey Levine, Yao Lu, Utsav Malla, Deeksha Manjunath, Igor Mordatch, Ofir Nachum, Carolina Parada, Jodilyn Peralta, Emily Perez, Karl Pertsch, Jornell Quiambao, Kanishka Rao, Michael S. Ryoo, Grecia Salazar, Pannag R. Sanketi, Kevin Sayed, Jaspiar Singh, Sumedh Sontakke, Austin Stone, Clayton Tan, Huong T. Tran, Vincent Vanhoucke, Steve Vega, Quan Vuong, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. RT-1: robotics transformer for real-world control at scale. In _Robotics: Science and Systems XIX, Daegu, Republic of Korea, July 1014, 2023_ , 2023. 1, 2 

- [5] Qingwen Bu, Hongyang Li, Li Chen, Jisong Cai, Jia Zeng, Heming Cui, Maoqing Yao, and Yu Qiao. Towards synergistic, generalized, and efficient dual-system for robotic manipulation. _CoRR_ , abs/2410.08001, 2024. 2 

- [6] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin 

Liu, Qiwei Liang, Zixuan Li, Xianliang Lin, Yiheng Ge, Zhenyu Gu, Weiliang Deng, Yubin Guo, Tian Nian, Xuanbing Xie, Qiangyu Chen, Kailun Su, Tianling Xu, Guodong Liu, Mengkang Hu, Huan-ang Gao, Kaixuan Wang, Zhixuan Liang, Yusen Qin, Xiaokang Yang, Ping Luo, and Yao Mu. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _CoRR_ , abs/2506.18088, 2025. 2, 6 

- [7] Zhuoxiao Chen, Junjie Meng, Mahsa Baktashmotlagh, Yonggang Zhang, Zi Huang, and Yadan Luo. MOS: model synergy for test-time adaptation on lidar-based 3d object detection. In _The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 2428, 2025_ . OpenReview.net, 2025. 2 

- [8] Runxi Cheng, Feng Xiong, Yongxian Wei, Wanyun Zhu, and Chun Yuan. Whoever started the interference should end it: Guiding data-free model merging via task vectors. _CoRR_ , abs/2503.08099, 2025. 1, 2, 6, 7 

- [9] Can Cui, Pengxiang Ding, Wenxuan Song, Shuanghao Bai, Xinyang Tong, Zirui Ge, Runze Suo, Wanqi Zhou, Yang Liu, Bofang Jia, Han Zhao, Siteng Huang, and Donglin Wang. Openhelix: A short survey, empirical analysis, and opensource dual-system VLA model for robotic manipulation. _CoRR_ , abs/2505.03912, 2025. 2 

- [10] MohammadReza Davari and Eugene Belilovsky. Model breadcrumbs: Scaling multi-task model merging with sparse masks. In _Computer Vision - ECCV 2024 - 18th European Conference, Milan, Italy, September 29-October 4, 2024, Proceedings, Part LXXV_ , pages 270–287. Springer, 2024. 2 

- [11] Sombit Dey, Jan-Nico Zaech, Nikolay Nikolov, Luc Van Gool, and Danda Pani Paudel. Revla: Reverting visual domain limitation of robotic foundation models. In _IEEE International Conference on Robotics and Automation, ICRA 2025, Atlanta, GA, USA, May 19-23, 2025_ , pages 8679– 8686. IEEE, 2025. 3, 4 

- [12] Guodong Du, Junlin Lee, Jing Li, Runhua Jiang, Yifei Guo, Shuyang Yu, Hanting Liu, Sim Kuan Goh, Ho-Kin Tang, Daojing He, and Min Zhang. Parameter competition balancing for model merging. In _Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024_ , 2024. 2 

- [13] Frederik Ebert, Yanlai Yang, Karl Schmeckpeper, Bernadette Bucher, Georgios Georgakis, Kostas Daniilidis, Chelsea Finn, and Sergey Levine. Bridge data: Boosting generalization of robotic skills with cross-domain datasets. In _Robotics: Science and Systems XVIII, New York City, NY, USA, June 27 - July 1, 2022_ , 2022. 2 

- [14] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, Jinlan Fu, Jingjing Gong, and Xipeng Qiu. Libero-plus: Indepth robustness analysis of vision-language-action models, 2025. 2, 5, 6 

- [15] Jonathan Frankle, Gintare Karolina Dziugaite, Daniel M. Roy, and Michael Carbin. Linear mode connectivity and the lottery ticket hypothesis. In _Proceedings of the 37th International Conference on Machine Learning, ICML 2020, 13-18 July 2020, Virtual Event_ , pages 3259–3269. PMLR, 2020. 2 

22343 

- [16] Antonio Andrea Gargiulo, Donato Crisostomi, Maria Sofia Bucarelli, Simone Scardapane, Fabrizio Silvestri, and Emanuele Rodol`a. Task singular vectors: Reducing task interference in model merging. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2025, Nashville, TN, USA, June 11-15, 2025_ , pages 18695–18705. Computer Vision Foundation / IEEE, 2025. 2, 4, 7 

- [17] Dibya Ghosh, Homer Rich Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Quan Vuong, Ted Xiao, Pannag R. Sanketi, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Robotics: Science and Systems XX, Delft, The Netherlands, July 15-19, 2024_ , 2024. 1 

- [18] Asher J. Hancock, Xindi Wu, Lihan Zha, Olga Russakovsky, and Anirudha Majumdar. Actions as language: Finetuning vlms into vlas without catastrophic forgetting. _CoRR_ , abs/2509.22195, 2025. 1 

- [19] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. In _The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022_ . OpenReview.net, 2022. 1, 2 

- [20] Chenyu Huang, Peng Ye, Tao Chen, Tong He, Xiangyu Yue, and Wanli Ouyang. Emr-merging: Tuning-free highperformance model merging. In _Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024_ , 2024. 1, 2, 4, 7 

- [21] Gabriel Ilharco, Marco T´ulio Ribeiro, Mitchell Wortsman, Ludwig Schmidt, Hannaneh Hajishirzi, and Ali Farhadi. Editing models with task arithmetic. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . OpenReview.net, 2023. 1, 2, 4, 6, 7 

- [22] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0.5: a vision-language-action model with open-world generalization. _CoRR_ , abs/2504.16054, 2025. 1, 2, 3 

- [23] Xisen Jin, Xiang Ren, Daniel Preotiuc-Pietro, and Pengxiang Cheng. Dataless knowledge fusion by merging weights of language models. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . OpenReview.net, 2023. 2 

- [24] Dmitry Kalashnikov, Alex Irpan, Peter Pastor, Julian Ibarz, Alexander Herzog, Eric Jang, Deirdre Quillen, Ethan Holly, Mrinal Kalakrishnan, Vincent Vanhoucke, and Sergey 

Levine. Qt-opt: Scalable deep reinforcement learning for vision-based robotic manipulation. _CoRR_ , abs/1806.10293, 2018. 2 

- [25] Dmitry Kalashnikov, Jacob Varley, Yevgen Chebotar, Benjamin Swanson, Rico Jonschkowski, Chelsea Finn, Sergey Levine, and Karol Hausman. Mt-opt: Continuous multitask robotic reinforcement learning at scale. _CoRR_ , abs/2104.08212, 2021. 2 

- [26] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024_ . OpenReview.net, 2024. 2 

- [27] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Paul Foster, Pannag R. Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. In _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , pages 2679–2713. PMLR, 2024. 1, 2, 3, 6, 7 

- [28] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _CoRR_ , abs/2502.19645, 2025. 1, 3 

- [29] Lingdong Kong, Shaoyuan Xie, Zeying Gong, Ye Li, Meng Chu, Ao Liang, Yuhao Dong, Tianshuai Hu, Ronghe Qiu, Rong Li, Hanjiang Hu, Dongyue Lu, Wei Yin, Wenhao Ding, Linfeng Li, Hang Song, Wenwei Zhang, Yuexin Ma, Junwei Liang, Zhedong Zheng, Lai Xing Ng, Benoit R. Cottereau, Wei Tsang Ooi, and Ziwei Liu. The robosense challenge: Sense anything, navigate anywhere, adapt across platforms. _CoRR_ , abs/2601.05014, 2026. 2 

- [30] Jia Syuen Lim, Zhuoxiao Chen, Zhi Chen, Mahsa Baktashmotlagh, Xin Yu, Zi Huang, and Yadan Luo. Dipex: Dispersing prompt expansion for class-agnostic object detection. In _Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024_ , 2024. 2 

- [31] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023_ , 2023. 2, 3, 6 

- [32] Zhenyi Lu, Chenghao Fan, Wei Wei, Xiaoye Qu, Dangyang Chen, and Yu Cheng. Twin-merging: Dynamic integration of modular expertise in model merging. In _Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024_ , 2024. 2 

- [33] Hao Luo, Yicheng Feng, Wanpeng Zhang, Sipeng Zheng, Ye Wang, Haoqi Yuan, Jiazheng Liu, Chaoyi Xu, Qin Jin, and Zongqing Lu. Being-h0: Vision-language-action pre- 

22344 

training from large-scale human videos. _arXiv preprint arXiv:2507.15597_ , 2025. 2 

- [34] Daniel Marczak, Simone Magistri, Sebastian Cygert, Bartlomiej Twardowski, Andrew D. Bagdanov, and Joost van de Weijer. No task left behind: Isotropic model merging with common and task-specific subspaces. _CoRR_ , abs/2502.04959, 2025. 1, 2 

- [35] Michael Matena and Colin Raffel. Merging models with fisher-weighted averaging. In _Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022_ , 2022. 2 

- [36] Oier Mees, Luk´as Hermann, Erick Rosete-Beas, and Wolfram Burgard. CALVIN: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics Autom. Lett._ , 7(3):7327–7334, 2022. 2 

- [37] Behnam Neyshabur, Hanie Sedghi, and Chiyuan Zhang. What is being transferred in transfer learning? In _Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual_ , 2020. 2 

- [38] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alexander Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, Andrew E. Wang, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Sch¨olkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter B¨uchler, Dinesh Jayaraman, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan Paul Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guanzhi Wang, Hao Su, Haoshu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I. Christensen, Hiroki Furuta, Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan Schneider, Jasmine Hsu, Jeannette Bohg, Jeffrey T. Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun Yang, Jitendra Malik, Jo˜ao Silv´erio, Joey Hejna, Jonathan Booher, Jonathan Tompson, Jonathan Yang, Jordi Salvador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran Lekkala, Kirsty El- 

lis, Krishan Rana, Krishnan Srinivasan, Kuan Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen, Lerrel Pinto, Li FeiFei, Liam Tan, Linxi Jim Fan, Lionel Ott, Lisa Lee, Luca Weihs, Magnum Chen, Marion Lepert, Marius Memmel, Masayoshi Tomizuka, Masha Itkina, Mateo Guaman Castro, Max Spero, Maximilian Du, Michael Ahn, Michael C. Yip, Mingtong Zhang, Mingyu Ding, Minho Heo, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J. Joshi, Niko S¨underhauf, Ning Liu, Norman Di Palo, Nur Muhammad (Mahi) Shafiullah, Oier Mees, Oliver Kroemer, Osbert Bastani, Pannag R. Sanketi, Patrick Tree Miller, Patrick Yin, Paul Wohlhart, Peng Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet, Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Mart´ın-Mart´ın, Rohan Baijal, Rosario Scalise, Rose Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante-Gomez, Sean Kirmani, Sergey Levine, Shan Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham D. Sonawani, Shuran Song, Sichun Xu, Siddhant Haldar, Siddharth Karamcheti, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Subramanian Ramamoorthy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung, Vidhi Jain, Vincent Vanhoucke, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiaolong Wang, Xinghao Zhu, Xinyang Geng, Xiyuan Liu, Liangwei Xu, Xuanlin Li, Yao Lu, Yecheng Jason Ma, Yejin Kim, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao, Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang, Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff Cui, Zichen Zhang, and Zipeng Lin. Open x- embodiment: Robotic learning datasets and RT-X models : Open x-embodiment collaboration. In _IEEE International Conference on Robotics and Automation, ICRA 2024, Yokohama, Japan, May 13-17, 2024_ , pages 6892–6903. IEEE, 2024. 2 

- [39] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. Spatialvla: Exploring spatial representations for visual-language-action model. _CoRR_ , abs/2501.15830, 2025. 1, 3 

- [40] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andr´es Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and R´emi Cad`ene. Smolvla: A vision-language-action model for affordable and efficient robotics. _CoRR_ , abs/2506.01844, 2025. 1 

- [41] George Stoica, Pratik Ramesh, Boglarka Ecsedi, Leshem Choshen, and Judy Hoffman. Model merging with SVD to 

22345 

tie the knots. In _The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 2428, 2025_ . OpenReview.net, 2025. 1, 2, 4, 5, 7 

- [42] Wenju Sun, Qingyong Li, Yangli-ao Geng, and Boyang Li. CAT merging: A training-free approach for resolving conflicts in model merging. _CoRR_ , abs/2505.06977, 2025. 2 

- [43] Anke Tang, Li Shen, Yong Luo, Shuai Xie, Han Hu, Lefei Zhang, Bo Du, and Dacheng Tao. SMILE: zero-shot sparse mixture of low-rank experts construction from pre-trained foundation models. _CoRR_ , abs/2408.10174, 2024. 2, 5 

- [44] Stone Tao, Fanbo Xiang, Arth Shukla, Yuzhe Qin, Xander Hinrichsen, Xiaodi Yuan, Chen Bao, Xinsong Lin, Yulin Liu, Tse-kai Chan, Yuan Gao, Xuanlin Li, Tongzhou Mu, Nan Xiao, Arnav Gurha, Zhiao Huang, Roberto Calandra, Rui Chen, Shan Luo, and Hao Su. Maniskill3: GPU parallelized robotics simulation and rendering for generalizable embodied AI. _CoRR_ , abs/2410.00425, 2024. 2 

- [45] Homer Rich Walke, Kevin Black, Tony Z. Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, Abraham Lee, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata V2: A dataset for robot learning at scale. In _Conference on Robot Learning, CoRL 2023, 6-9 November 2023, Atlanta, GA, USA_ , pages 1723–1736. PMLR, 2023. 2 

- [46] Ke Wang, Nikolaos Dimitriadis, Guillermo Ortiz-Jim´enez, Franc¸ois Fleuret, and Pascal Frossard. Localizing task information for improved model merging and compression. In _Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024_ . OpenReview.net, 2024. 2, 4 

- [47] Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, Siteng Huang, Yifan Tang, Wenhui Wang, Ru Zhang, Jianyi Liu, and Donglin Wang. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. _CoRR_ , abs/2509.09372, 2025. 2, 3, 4, 6, 7 

- [48] Zixin Wang, Yadan Luo, Liang Zheng, Zhuoxiao Chen, Sen Wang, and Zi Huang. In search of lost online test-time adaptation: A survey. _Int. J. Comput. Vis._ , 133(3):1106–1139, 2025. 2 

- [49] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, and Jian Tang. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _CoRR_ , abs/2409.12514, 2024. 1, 3 

- [50] Mitchell Wortsman, Gabriel Ilharco, Samir Ya Gadre, Rebecca Roelofs, Raphael Gontijo-Lopes, Ari S Morcos, Hongseok Namkoong, Ali Farhadi, Yair Carmon, Simon Kornblith, et al. Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time. In _International conference on machine learning_ , pages 23965–23998. PMLR, 2022. 2 

- [51] Prateek Yadav, Derek Tam, Leshem Choshen, Colin A. Raffel, and Mohit Bansal. Ties-merging: Resolving interference when merging models. In _Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Or-_ 

_leans, LA, USA, December 10 - 16, 2023_ , 2023. 1, 2, 4, 6, 7 

- [52] Kunda Yan, Min Zhang, Sen Cui, Zikun Qu, Bo Jiang, Feng Liu, and Changshui Zhang. CALM: consensusaware localized merging for multi-task learning. _CoRR_ , abs/2506.13406, 2025. 2 

- [53] An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tianyi Tang, Tingyu Xia, Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. Qwen2.5 technical report, 2025. 2 

- [54] Enneng Yang, Li Shen, Guibing Guo, Xingwei Wang, Xiaochun Cao, Jie Zhang, and Dacheng Tao. Model merging in llms, mllms, and beyond: Methods, theories, applications and opportunities. _CoRR_ , abs/2408.07666, 2024. 2 

- [55] Huitong Yang, Zhuoxiao Chen, Fengyi Zhang, Zi Huang, and Yadan Luo. Codemerge: Codebook-guided model merging for robust test-time adaptation in autonomous driving. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 2 

- [56] Jianwei Yang, Reuben Tan, Qianhui Wu, Ruijie Zheng, Baolin Peng, Yongyuan Liang, Yu Gu, Mu Cai, Seonghyeon Ye, Joel Jang, Yuquan Deng, and Jianfeng Gao. Magma: A foundation model for multimodal AI agents. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2025, Nashville, TN, USA, June 11-15, 2025_ , pages 14203–14214. Computer Vision Foundation / IEEE, 2025. 1, 3 

- [57] Ruihan Yang, Qinxi Yu, Yecheng Wu, Rui Yan, Borui Li, An-Chieh Cheng, Xueyan Zou, Yunhao Fang, Xuxin Cheng, Ri-Zhao Qiu, Hongxu Yin, Sifei Liu, Song Han, Yao Lu, and Xiaolong Wang. Egovla: Learning vision-language-action models from egocentric human videos, 2025. 2 

- [58] Zongzhen Yang, Binhang Qi, Hailong Sun, Wenrui Long, Ruobing Zhao, and Xiang Gao. CABS: conflict-aware and balanced sparsification for enhancing model merging. _CoRR_ , abs/2503.01874, 2025. 2 

- [59] Le Yu, Bowen Yu, Haiyang Yu, Fei Huang, and Yongbin Li. Language models are super mario: Absorbing abilities from homologous models as a free lunch. In _Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024_ . OpenReview.net, 2024. 1, 2 

- [60] Fanhu Zeng, Haiyang Guo, Fei Zhu, Li Shen, and Hao Tang. Robustmerge: Parameter-efficient model merging for mllms with direction robustness, 2025. 2 

- [61] Jinghan Zhang, Shiqi Chen, Junteng Liu, and Junxian He. Composing parameter-efficient modules with arithmetic operations. _CoRR_ , abs/2306.14870, 2023. 1, 2 

- [62] Jianke Zhang, Yanjiang Guo, Xiaoyu Chen, Yen-Jen Wang, Yucheng Hu, Chengming Shi, and Jianyu Chen. Hirt: Enhancing robotic control with hierarchical robot transformers. 

22346 

In _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , pages 933–946. PMLR, 2024. 2 

- [63] Zhizhen Zhang, Lei Zhu, Zhen Fang, Zi Huang, and Yadan Luo. Provable ordering and continuity in vision-language pretraining for generalizable embodied agents, 2025. 2 

- [64] Zecheng Zhao, Zhi Chen, Zi Huang, Shazia Sadiq, and Tong Chen. Generative recall, dense reranking: Learning multiview semantic ids for efficient text-to-video retrieval. _CoRR_ , abs/2601.21193, 2026. 2 

- [65] Shenghe Zheng, Hongzhi Wang, Chenyu Huang, Xiaohui Wang, Tao Chen, Jiayuan Fan, Shuyue Hu, and Peng Ye. Decouple and orthogonalize: A data-free framework for lora merging. _CoRR_ , abs/2505.15875, 2025. 2 

- [66] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong T. Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. RT-2: vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning, CoRL 2023, 6-9 November 2023, Atlanta, GA, USA_ , pages 2165–2183. PMLR, 2023. 1, 2 

22347 

