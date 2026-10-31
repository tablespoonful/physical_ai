---
title: "Stable Language Guidance for Vision-Language-Action Models"
date: "2026-01-07"
authors: "Zhihao Zhan; Yuhao Chen; Jiaying Zhou; Qinhan Lyu; Hao Liu; Keze Wang"
url: https://arxiv.org/abs/2601.04052
pdf: https://arxiv.org/pdf/2601.04052
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.04052)** / [論文ページ](https://arxiv.org/abs/2601.04052)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Stable Language Guidance for Vision–Language–Action Models** 

## **Zhihao Zhan**<sup>**1**</sup> **, Yuhao Chen**<sup>**1**</sup> **, Jiaying Zhou**<sup>**1**</sup> **, Qinhan Lyu**<sup>**1**</sup> **, Hao Liu**<sup>**1**</sup> **, Keze Wang**<sup>**1,2,3**</sup> , **Liang Lin**<sup>**1,2,3**</sup> , **Guangrun Wang**<sup>**1,2,3***</sup> 

1Sun Yat-sen University 

2Guangdong Key Lab of Big Data Analysis & Processing 

3X-Era AI Lab 

zhanzhh6@mail2.sysu.edu.cn, wanggrun@gmail.com 

## **Abstract** 

Vision-Language-Action (VLA) models have demonstrated impressive capabilities in generalized robotic control; however, they remain notoriously brittle to linguistic perturbations. We identify a critical “modality collapse” phenomenon where strong visual priors overwhelm sparse linguistic signals, causing agents to overfit to specific instruction phrasings while ignoring the underlying semantic intent. To address this, we propose **Residual Semantic Steering (RSS)** , a probabilistic framework that disentangles physical affordance from semantic execution. RSS introduces two theoretical innovations: (1) **Monte Carlo Syntactic Integration** , which approximates the true semantic posterior via dense, LLM-driven distributional expansion, and (2) **Residual Affordance Steering** , a dual-stream decoding mechanism that explicitly isolates the causal influence of language by subtracting the visual affordance prior. Theoretical analysis suggests that RSS effectively maximizes the mutual information between action and intent while suppressing visual distractors. Empirical results across diverse manipulation benchmarks demonstrate that RSS achieves state-of-the-art robustness, maintaining performance even under adversarial linguistic perturbations. We release our code at https://github.com/Doo-mon/RSS. 

## **1 Introduction** 

The core promise of Embodied AI is the ability to map high-level intent to low-level control. Formally, we seek a policy _π_ ( _a|o, z_ ) where _o_ is the observation and _z_ is the latent semantic intent. However, in practice, we only have access to linguistic realizations _l ∼ p_ ( _l|z_ ). Current Vision-Language-Action (VLA) models approximate _π_ ( _a|o, l_ ), but often learn a degenerate mapping where _π_ ( _a|o, li_ ) _̸ ≈ π_ ( _a|o, lj_ ) even when _li_ and _lj_ share the same intent _z_ . 

*Corresponding author. 


Figure 1: **Taxonomy of Language Instruction Perturbations.** We identify three distinct failure modes in VLA instruction following: (1) **Destructive Instruction Overwriting** , where critical semantic tokens are lost or masked (e.g., masking the drawer location); (2) **Obfuscated Instruction Reinterpretation** , where the model fails to ground synonymous or verbose descriptions (e.g., “beverage container” vs. “mug”); and (3) **Out-of-Distribution Semantic Transfer** , where the instruction targets a valid but unlearned goal configuration (e.g., placing on a “cabinet” instead of the training-set “stove”). 

Recent empirical audits validate this failure mode. Analyses on the **Libero-Plus** (Fei et al., 2025) and **RADAR** (Chen et al., 2026) benchmarks reveal a pervasive “instruction blindness,” where models frequently ignore language inputs entirely, defaulting to the most probable action given the scene alone. Furthermore, evidence from **LiberoPro** highlights a critical lack of grounding; even when language is processed, models exhibit an overdependence on rote pattern execution rather than true semantic interpretation, leading to catastrophic failure when instructions deviate from training templates (Zhou et al., 2025). As illustrated in Figure 1, these failures manifest through three primary categories of linguistic variation: destructive instruction overwriting, obfuscated reinterpretation of synonyms, and out-of-distribution semantic transfer. 

We argue that this fragility stems from two 

sources: 

1. **Manifold Sparsity:** The training data covers a vanishingly small support of the syntactic distribution _p_ ( _l|z_ ), leading to overfitting on surface statistics. 

2. **Prior Dominance:** In the high-dimensional joint distribution _p_ ( _a|o, l_ ), the visual signal _o_ contains dense, high-frequency information (edges, textures) that dominates the gradient, causing the model to default to a “visual affordance prior” (e.g., “grasp the nearest object”) regardless of the text. 

We introduce **Residual Semantic Steering (RSS)** , a framework that addresses these challenges through two theoretical innovations. First, to resolve manifold sparsity, we employ **Monte Carlo Syntactic Integration** . Instead of relying on single data points, we treat the instruction as a seed and utilize an Oracle Teacher (LLM) to generate a dense syntactic neighborhood. By optimizing an Expected Semantic Loss over this expanded distribution, we force the policy to marginalize out syntactic noise and approximate the true posterior _π_ ( _a|o, z_ ). Second, to counteract prior dominance, we introduce **Residual Affordance Steering** . We reinterpret the “unconditional” forward pass not as a null baseline, but as the Base Affordance Distribution _s_ ( _a|o, ∅_ )—capturing physically feasible actions independent of intent. By subtracting this visual prior from the conditional logits, we isolate a Pure Semantic Signal that represents the causal influence of language. Unlike standard ClassifierFree Guidance (CFG) (Ho and Salimans, 2022), which acts as a “quality booster” in generative models, RSS functions as a Bias Suppressor in control, mathematically penalizing actions driven solely by visual instinct. 

**Contributions.** Our main contributions are summarized as follows: 

- We introduce Monte Carlo Syntactic Integration, a training strategy that utilizes an Oracle Teacher to generate dense linguistic neighborhoods. By optimizing an Expected Semantic Loss over this expanded distribution, we approximate the true semantic posterior, ensuring the policy is invariant to surface-level syntactic perturbations. 

- We propose Residual Affordance Steering that acts as a Bias Suppressor. By subtracting the 

Base Affordance Distribution (visual prior) from the conditional logits, it isolates the Pure Semantic Signal, effectively restoring the rank of linguistic features relative to visual dominators. 

- We empirically demonstrate that RSS achieves state-of-the-art robustness, effectively mitigating “instruction blindness” and preventing rote pattern execution by decoupling semantic intent from visual affordances. 

## **2 Related Work** 

**Vision-Language-Action Architectures.** The field has rapidly evolved from early large-scale imitators like RT-1 (Brohan et al., 2022) and RT2 (Zitkovich et al., 2023) to efficient open-source models like OpenVLA (Kim et al., 2024). Recent autoregressive approaches focus on specific capabilities: SpatialVLA (Qu et al., 2025) incorporates 3D spatial cues, OpenVLA-OFT (Kim et al., 2025) optimizes continuous action tuning, and _π_ 0 FAST (Pertsch et al., 2025) enhances training efficiency. Parallel work integrates chain-of-thought reasoning to guide planning (CoT-VLA (Zhao et al., 2025), GR-1 (Wu et al., 2023)). Simultaneously, diffusion-based control has matured from the seminal Diffusion Policy (Chi et al., 2023) to scalable transformers like CogACT (Li et al., 2024b) and RDT (Liu et al., 2024). State-of-the-art generalist frameworks now employ flow matching ( _π_ 0 (Black et al., 2024), _π_ 0 _._ 5 (Intelligence et al., 2025)), _E_ 0 (Zhan et al., 2025), dual-system designs (OneTwoVLA (Lin et al., 2025), GR00T N1 (Bjorck et al., 2025)), and decoupling approaches (Li et al., 2025) to achieve broad physical generalization (Zhou et al., 2026; Chen et al., 2026). 

**Language Guidance and Modality Imbalance.** Despite these architectural advances, balancing multi-modal inputs remains a critical bottleneck (Chen et al., 2026). Recent audits on the **LiberoPlus** (Fei et al., 2025) and **Libero-Pro** (Zhou et al., 2025) benchmarks reveal that VLA agents frequently suffer from “instruction blindness” or rote execution, as dense high-frequency visual signals tend to overwhelm sparse linguistic tokens. A notable architectural solution is **RDT-1B** (Liu et al., 2024), which mitigates this text overshadowing by eschewing simultaneous token injection. Instead, it employs an alternating cross-attention mechanism, injecting image and text tokens in successive layers. 

This strategy explicitly preserves the magnitude of linguistic gradients during deep fusion, ensuring that instruction signals are not drowned out by the visual affordance prior. 

## **3 Methodology: The RSS Framework** 

### **3.1 Preliminaries** 

Vision-language-action(VLA) models are commonly trained via imitation learning on large-scale robot demonstration datasets _D_ . Given an observation _ot_ and a natural language task instruction _l_ , the objective is to maximize the log-likelihood of an action (or an action chunk) _at_ : _t_ + _H_ : 


(1) 

The observation _ot_ typically comprises one or more visual inputs _{It_<sup>1</sup><sup>_, . . . , I_</sup> _t_<sup>_n}_andaproprioceptive</sup> state _qt_ encoding the robot’s joint configurations. 

Modern VLA architectures inherit the design principles of large vision-language models, employing modality-specific tokenizers to map visual, linguistic, and action inputs into either discrete or continuous token representations (Brohan et al., 2022; Zitkovich et al., 2023; Pertsch et al., 2025; Black et al., 2024; Intelligence et al., 2025). These tokens are processed by a large autoregressive transformer backbone, whose parameters are commonly initialized from pretrained vision-language models. By encoding observations, instructions, and actions into a unified token sequence, the imitation learning objective can be reformulated as a standard next-token prediction problem, enabling the use of scalable training techniques from contemporary language modeling. 

We consider a VLA policy parameterized by _θ_ . Our goal is to ensure the policy is invariant to linguistic noise _ϵl_ such that _π_ ( _a|o, l_ ) _≈ π_ ( _a|o, l_ + _ϵl_ ). 

To achieve this, we propose the **Residual Semantic Steering (RSS)** framework. As illustrated in Figure 2, RSS operates as a dual-stage mechanism: it densifies the linguistic supervision signal via _Monte Carlo Syntactic Integration_ to enforce semantic invariance; it actively suppresses visual priors via _Residual Affordance Steering_ to isolate the pure semantic intent. 

### **3.2 Monte Carlo Syntactic Integration** 

Standard Maximum Likelihood Estimation (MLE) minimizes _L_ = _−_ log _pθ_ ( _a|o, l_ ). However, a single instruction _l_ is a noisy estimator of the true 

intent _z_ . For instance, consider the latent intent _z_ as “grasping the apple.” This intent can be realized through various instructions _l_ , such as “Pick up the red fruit,” “Fetch the apple,” or “Grab it.” If the model is trained solely on “Pick up the red fruit,” it treats specific lexical choices (e.g., “fruit” vs. “apple”) as an essential signal rather than what they truly are: syntactic noise partially obscuring the underlying semantic intent. To learn the true semantic policy _p_ ( _a|o, z_ ), we must marginalize over the nuisance variable of syntax: 


Since this integral is intractable, we employ a **Monte Carlo approximation** using an Oracle Teacher (e.g., a high-capability LLM). We treat the original instruction _lorig_ as a seed and generate a dense neighborhood _N_ ( _lorig_ ) = _{l_ 1 _, ..., lK}_ via the Teacher, sampling from the induced distribution _p_ ˆ( _l|z_ ).We then optimize the **Expected Semantic Loss** : 


This formulation forces the encoder to map disparate linguistic inputs _{lk}_ to a unified region in the latent embedding space, explicitly minimizing the conditional entropy _H_ ( _A|L_ ) with respect to syntactic variation. 

### **3.3 Residual Affordance Steering** 

Standard CFG combines conditional and unconditional scores. We re-interpret this for the action space to distinguish our method from generative diffusion. Let _s_ ( _a|o, l_ ) be the logit score of an action. We decompose the decision process into two components: 

1. **The Affordance Prior** _s_ ( _a|o, ∅_ ) **:** The probability of an action based solely on visual scene geometry (what is _possible_ ). 

2. **The Semantic Modulation:** The specific shift induced by the instruction. 

Standard VLA inference uses _s_ ( _a|o, l_ ). However, we observe that _s_ ( _a|o, l_ ) _≈ s_ ( _a|o, ∅_ ) when the language signal is weak or the visual features are overpowering. 

To extract the **Pure Semantic Signal** , we calculate the **Residual Vector** ∆ _sem_ : 


Figure 2: **Overview of Residual Semantic Steering (RSS).** To combat instruction blindness, RSS operates in two stages. **Left:** _Monte Carlo Syntactic Integration_ utilizes an Oracle Teacher to generate a dense linguistic neighborhood around a seed instruction. Optimizing over this distribution forces the policy to learn representations that are invariant to syntactic perturbations. **Right:** _Residual Affordance Steering_ mitigates visual prior dominance. By subtracting the unconditioned “visual instinct” (Base Affordance) from the standard prediction, we isolate and amplify the residual semantic signal, ensuring the policy follows the specific user intent rather than generic visual attractors. 

This subtraction cancels out the visual bias. If the robot wants to grasp a red cup ( _ared_ ) simply because it is close (visual bias), _s_ ( _ared|o, ∅_ ) will be high. The residual ∆ _sem_ removes this bias, leaving only the text’s contribution. 

The final **Steered Policy** is: 


where _γ >_ 1 is the **Steering Coefficient** . 

**Novelty vs. Standard Classifier-Free Guidance (CFG) (Ho and Salimans, 2022):** While mechanically similar to CFG, RSS differs conceptually. CFG in diffusion acts as a quality booster (trading diversity for fidelity). RSS acts as a **Bias Suppressor** . We use the null-text pass to explicitly model the “visual instinct” of the robot and then mathematically penalize actions that are driven _only_ by that instinct and not confirmed by the text. 

### **3.4 Theoretical Analysis** 

**Proposition 1 (Visual Bias Decoupling).** Let the logit function be approximated linearly as 

_S_ ( _o, l_ ) = _Wvϕ_ ( _o_ ) + _Wlψ_ ( _l_ ) + _C_ , where _C_ represents confounding interactions, _ϕ_ ( _o_ ) _∈_ R<sup>_d_</sup> is the visual embedding vector, _ψ_ ( _l_ ) _∈_ R<sup>_d_</sup> is the linguistic embedding vector, _Wv, Wl ∈_ R<sup>_d_</sup> are the projection weights for the visual and linguistic modalities, respectively, _ϵ_ represents higher-order interaction terms and bias, assumed to be negligible for this first-order analysis. The standard inference yields a signal-to-noise ratio dependent on _∥Wv∥/∥Wl∥_ . In VLA tasks, _∥Wv∥≫∥Wl∥_ .The Residual Steering yields: 


By setting _γ >_ 1, we artificially restore the rank of the language features, effectively orthogonalizing the semantic vector from the visual manifold. 

## **4 Experiment** 

### **4.1 Training Setting** 

We adopt _π_ 0 (Black et al., 2024) and _π_ 0 _._ 5 (Intelligence et al., 2025) as our baseline models. The pre- 

Table 1: **Robustness evaluation under Destructive Instruction Overwriting.** Results are reported as task Success Rates (SR) in percentages (%). **Bold** and <u>underlined</u> entries denote the best and second-best performance per column, respectively. Values in parentheses represent the absolute improvement over the corresponding baseline. **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

|**Model**|**Origin**<br>SR (%)_↑_|**Multi**<br>SR (%)_↑_|**Blank**<br>SR (%)_↑_|**Rand**<br>SR (%)_↑_|**M2**<br>SR (%)_↑_|**M4**<br>SR (%)_↑_|**M6**<br>SR (%)_↑_|**M8**<br>SR (%)_↑_|**Simple**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|---|---|---|---|---|---|
|||||_π_0(B|lack et al.,2|024)|||||
|base|94.15|91.30|25.20|89.35|72.65|42.50|22.15|7.80|26.25|52.37|
|+ RAS|90.65|89.90|63.40|88.70|78.45|55.05|33.55|17.95|62.50|64.46(+12.09)|
|+ MCSI|94.55|93.45|41.85|92.95|88.85|77.75|63.85|52.80|39.85|71.77(+19.40)|
|+ RAS & MCSI|93.35|91.35|69.65|94.95|92.05|85.85|77.95|69.90|64.90|82.22(+29.85)|
|||||_π_0_._5(Inte|lligence et a|l.,2025)|||||
|base|95.15|95.45|50.05|95.20|92.65|82.70|69.55|55.45|46.90|75.90|
|+ RAS|96.65|96.80|**70.50**|95.95|93.90|86.65|79.30|71.05|69.10|84.43<br>(+8.53)|
|+ MCSI|**98.25**|**98.00**|46.20|**97.45**|96.05|87.20|73.40|57.95|46.20|77.86(+1.96)|
|+ RAS & MCSI|96.60|97.50|70.25|**97.45**|**96.35**|**92.00**|**84.55**|**77.50**|**70.60**|**86.98**(+11.08)|


Table 2: **Obfuscated instruction reinterpretation result. Bold** entries denote the best results per column, and <u>underlined entries</u> indicate the second-best. Values in parentheses report the absolute SR improvement (in percentage points) over the corresponding baseline under the same setting. All numbers are percentages (%). **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

|**Model**|**R0**<br>SR (%)_↑_|**R1**<br>SR (%)_↑_|**R2**<br>SR (%)_↑_|**R3**<br>SR (%)_↑_|**R4**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|---|---|
|||_π_0(B|lack et al.,2|024)|||
|base|91.4|55.8|7.4|28.4|42.4|45.08|
|+ RAS|90.0|59.0|11.4|40.2|46.0|49.32(+4.24)|
|+ MCSI|92.6|83.6|28.0|71.2|58.6|66.80(+21.72)|
|+ RAS & MCSI|88.4|85.4|26.8|80.0|47.0|65.52(+20.44)|
|||_π_0_._5(Inte|lligence et al|.,2025)|||
|base|95.0|93.2|30.4|**90.6**|68.6|75.56|
|+ RAS|97.0|94.6|26.4|86.4|77.6|76.40<br>(+0.84)|
|+ MCSI|97.0|94.6|**31.4**|84.4|70.6|75.60(+0.04)|
|+ RAS & MCSI|**97.6**|**97.2**|30.2|89.4|**79.0**|**78.68**(+3.12)|


trained vision language model backbone is based on Gemma (Team et al., 2024). The initial base weights are obtained through large-scale pretraining on a diverse and heterogeneous collection of robotic datasets (O’Neill et al., 2024). Building upon these pretrained representations, we fine-tune the models on task-specific data and incorporate our proposed modifications. 

To implement _Monte Carlo Syntactic Integration_ , we utilize Qwen2.5-VL (Bai et al., 2025) as an oracle teacher to generate dense semantic neighborhoods during training. At evaluation time, we employ ChatGPT-5.2 (OpenAI, 2025) to systematically rewrite all task instructions, ensuring consistent and controlled linguistic variations across experiments. 

Each model was trained for a total of 30 _,_ 000 steps with a batch size of 32. The learning rate followed a cosine decay schedule, implemented as 

_CosineDecaySchedule_ , with a warm-up phase of 10 _,_ 000 steps, a peak learning rate of 5 _×_ 10<sup>_−_5</sup> and a final learning rate of 5 _×_ 10<sup>_−_5</sup> . An exponential moving average (EMA) with a decay rate of 0 _._ 999 was applied. During inference, a single NVIDIA RTX 3090 GPU was used for model evaluation and deployment on the server side. 

### **4.2 Simulation Experiment** 

We adopt **LIBERO** (Liu et al., 2023) as our primary simulation benchmark for evaluating VLA models. It comprises four task categories ( _LIBERO-Spatial_ , _LIBERO-Object_ , _LIBERO-Goal_ , and _LIBERO-10_ ) which jointly challenge VLA models along multiple dimensions, including spatial reasoning, objectcentric manipulation, goal specification, and multistep task execution. As a result, it has become a highly competitive benchmark, with many state-ofthe-art methods employing sophisticated architec- 

Table 3: **Examples of obfuscated instruction reinterpretation variants (R0–R4) on LIBERO-Goal.** All variants preserve the original task semantics while introducing different forms of linguistic perturbations. 

|**Variant**|**Function**|**Examples**|
|---|---|---|
|Original|/|Put the wine bottle on top of the cabinet.|
|R0|Multiword Substitution|Move the wine bottle onto the cabinet top.|
|R1|Distraction|Once you’ve got a steady hold, put the wine bottle on the cabinet top.|
|R2|Common Sense|Set the sealed container typically used for pouring grape-based drinks on the<br>upper face of the standing storage furniture.|
|R3|Reasoning Chain|Move the bottle over the cabinet, then release it once it is stable on top.|
|R4|Confusion|Regardless of the drawers being open or closed, place the wine bottle on top of<br>the cabinet.|


Table 4: **Out-of-distribution semantic transfer result. Bold** entries denote the best results per column. The base model is _π_ 0 _._ 5 (Intelligence et al., 2025). **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

|**Model**|**10-steps**<br>SR (%)_↑_|**100-steps**<br>SR (%)_↑_|**1000-steps**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|
|base|27.0|31.0|91.0|49.67|
|+ RAS|17.0|29.0|**98.0**|48.00|
|+ MCSI|28.0|**42.0**|97.0|**55.67**|
|+ RAS & MCSI|**31.0**|31.0|97.0|53.00|


tural designs and advanced training strategies to maximize performance. 

To further investigate how natural language instructions guide VLA models, we extend LIBERO with a set of _controlled instruction variants_ that explicitly probe linguistic robustness and generalization. Specifically, we consider three categories of instruction perturbations (See Figure 1). (1) **Destructive instruction overwriting** , where critical semantic components of the original instruction are intentionally corrupted or removed, thereby disrupting the instruction’s compositional meaning. (2) **Obfuscated instruction reinterpretation** , which introduces syntactically valid yet semantically peripheral or potentially distracting descriptions while preserving the original task intent to evaluate robustness against semantic distraction rather than outright corruption. (3) **Outof-distribution (OOD) semantic transfer** , where novel task instructions are constructed by recombining object concepts observed during training into previously unseen compositions, resulting in tasks that do not appear in the original training distribution. 

**Destructive instruction overwriting.** To explicitly probe the extent to which VLA policies rely on genuine language grounding rather than spurious 


Figure 3: **Comparison on the LIBERO variant** **_R3Reasoning Chain_ .** In the "open the top drawer and put the bowl inside" task, our model consistently outperforms the baseline under reasoning-chain–perturbed instructions, demonstrating a stronger ability to follow multi-step semantic constraints and accurately complete the task despite increased linguistic complexity. 

correlations, we design a set of _destructive instruction overwriting_ variants that deliberately corrupt or erase critical semantic information in the original task instructions. Specifically, we consider five types of perturbations: **Blank** , where the instruction is replaced by an empty string, completely removing linguistic input; **Simple** , where all instructions are substituted with a generic and uninformative phrase (e.g., “Do something”); **Multi** , where we leverage a large language model to generate multiple paraphrases of the original instruction via word substitution or rephrasing, and randomly sample one variant during evaluation; **Rand** , which randomly permutes the word order within the instruction, disrupting syntactic structure while preserving the vocabulary; and **Mask** , where each word is independently replaced by a <MASK> token with varying probabilities, progressively degrading 

semantic content. 

As shown in Table 1, these destructive perturbations lead to substantial performance degradation across most settings, particularly under **Blank** , **Simple** , and high-ratio **Mask** conditions, indicating that removing or severely corrupting linguistic cues significantly hinders task execution. Notably, models augmented with RAS and MCSI demonstrate improved resilience under destructive overwriting, achieving higher average success rates across all variants. This observation implies that richer vision–language alignment can partially mitigate the reliance on brittle instruction patterns, encouraging more semantically grounded policy behavior rather than shortcut exploitation. 

**Obfuscated instruction reinterpretation.** We introduce a set of semantically preserved but potentially obfuscated instruction variants to evaluate linguistic robustness on the LIBERO-Goal benchmark. Specifically, we consider: **R0 (Multiword Substitution)** , which applies lightweight synonym or phrase replacements; **R1 (Distraction)** , which augments instructions with task-irrelevant contextual content; **R2 (Common Sense)** , which replaces object names with commonsense-based descriptive phrases; **R3 (Reasoning Chain)** , which reformulates instructions to emphasize implicit reasoning or final-state constraints; and **R4 (Confusion)** , which introduces distractor objects via explicit negation while preserving the original task goal. 

As shown in Table 2, there are clear performance disparities across different reinterpretation variants, highlighting how VLA models respond to semantically preserved yet linguistically challenging instructions. Among all settings, **R0** incurs only minor degradation, indicating that most models are largely insensitive to superficial lexical substitutions. In contrast, **R1** and **R2** lead to more pronounced drops, suggesting that additional irrelevant context and abstract commonsense descriptions substantially increase the difficulty of extracting task-relevant semantics. 

Notably, **R3** and **R4** constitute the most challenging conditions. **R3** requires the model to correctly interpret implicit reasoning structures and final-state constraints, while **R4** explicitly introduces distractor objects that co-occur in other tasks, stressing the model’s ability to resist spurious correlations. Performance under these two variants, therefore, serves as a stronger indicator of true lan- 

guage grounding rather than shallow pattern matching. 

Across most variants, models augmented with RAS and MCSI demonstrate improved robustness, achieving the highest average success rate. This trend suggests that richer vision–language alignment encourages policies to rely less on brittle lexical cues and more on semantically grounded representations, improving generalization under obfuscated yet valid instructions. 

**Out-of-distribution semantic transfer.** To construct a controlled out-of-distribution (OOD) evaluation setting, we remove two target tasks from the original LIBERO-Goal training set, while ensuring that the objects involved still appear in other training tasks. This design isolates distribution shift at the level of _object–goal composition_ , rather than introducing entirely unseen objects. To avoid trivial failure due to complete task absence, we first fine-tune the baseline model for 6,000 steps using the remaining in-distribution data, corresponding to approximately 20% of full training. We then perform few-step adaptation using a small number of demonstrations from the two held-out OOD tasks, and evaluate performance under varying step budgets. 

As shown in Table 4, the vanilla model exhibits limited generalization under low-step regimes, particularly with 10-steps adaptation, indicating difficulty in transferring previously learned object semantics to novel task compositions. Meanwhile, although the average success rate of the baseline appears relatively high (in 100-steps and 1,000-steps adaptation), a closer inspection reveals that this performance is dominated by overfitting to a single held-out task, while consistently failing on the other OOD task. In contrast, our method achieves successful execution across both held-out tasks, reflecting improved robustness to compositional distribution shifts. 

Notably, RAS and MCSI improve few-step performance to different extents across regimes, with MCSI consistently achieving stronger gains. While combining RAS with MCSI offers additional benefits, MCSI alone delivers the most effective improvement, indicating its dominant role in enhancing semantic transfer and reducing reliance on taskspecific memorization. 


Figure 4: **Ablation of steering coefficient and denoising steps on destructive instruction overwriting.** Success rates (SR, %) across instruction variants under different steering coefficients for _π_ 0 (a) and _π_ 0 _._ 5 (b), and different denoising steps for _π_ 0 (c) and _π_ 0 _._ 5 (d), illustrating the effect of guidance and generation depth on robustness to instruction perturbations. 


Figure 5: **Training loss curves.** We report the training loss trajectories of different model variants throughout optimization. **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

### **4.3 Ablation Study** 

We conduct a comprehensive ablation study on two key hyperparameters in RSS: the Residual Affordance Steering (RAS) coefficient and the number of denoising steps. All evaluations are performed under destructive instruction overwriting benchmarks. 

**Residual Affordance Steering.** Figure 4 (a) and Figure 4 (b) report performance under different RAS coefficients with the number of denoising steps fixed to 10. We observe that moderate steering coefficients consistently improve robustness under semantic-preserving perturbations, by strengthening the alignment between language conditions and action generation. However, excessively large coefficients significantly amplify sensitivity to corrupted or obfuscated instructions, leading to pronounced performance drops under destructive perturbations. This trend indicates that over-strong RAS encourages over-conditioning on unreliable linguistic signals, thereby exacerbating shortcut exploitation. More details can be found in the Table 14. 

**Denoising steps.** Figure 4 (c) and Figure 4 (d) analyze the effect of varying the number of denois- 

ing steps with the RAS coefficient fixed at 1.5 and 1.25, respectively. While increasing the number of steps can improve success rates in certain individual settings, we observe that larger step counts do not consistently translate to higher overall performance, and in some cases lead to a slight degradation in average success rate. This suggests that excessive denoising primarily refines low-level action details without providing additional semantic benefits. 

**Joint effect.** When considering the interaction between RAS and denoising steps, we find that the overall impact of varying the number of denoising steps is relatively limited under smaller steering coefficients. In this regime, the model is less sensitive to sampling depth, as weaker conditional forcing mitigates over-reliance on potentially noisy language inputs. Overall, the optimal configuration reflects a trade-off between conditional strength and sampling stability, with moderate RAS coefficients and a moderate number of denoising steps yielding the most robust performance across language perturbations. 

### **4.4 Different VLM Teachers.** 

To demonstrate that MCSI is not merely overfitting to the specific linguistic patterns of the training teacher, we conducted the following analyses without retraining (See Table 5). 

We tested the MCSI model on instructions paraphrased by DeepSeek-R1 (Guo et al., 2025) and Qwen-3.5 (Qwen Team, 2026). Despite distinct lexical choices and sentence structures, MCSI demonstrated significantly higher stability than the baseline. Specifically, when instructions were rephrased by DeepSeek-R1, the baseline _π_ 0 _._ 5 model suffered a performance drop of 10.54%, whereas our method (add MCSI) declined by only 1.28%. Similarly, with Qwen-3.5, the baseline dropped 5.10% 

Table 5: **Generalization to paraphrased instructions generated by different VLMs on LIBERO.** Without retraining, **MCSI** consistently improves robustness to linguistic variations and reduces performance drift compared to the baseline _π_ 0 _._ 5 (Intelligence et al., 2025). **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

|**Model**|**R1**<br>SR (%)_↑_|**R2**<br>SR (%)_↑_|**R3**<br>SR (%)_↑_|**R4**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|**Drift**|
|---|---|---|---|---|---|---|
|In|structions g|enerated by|**ChatGPT5**|**.2 (OpenAI, **|**2025)**||
|base|93.2|30.4|90.6|68.6|70.70|0|
|+ MCSI|94.6|31.4|84.4|70.6|70.25|0|
|+ RAS & MCSI|97.2|30.2|89.4|79.0|73.95|0|
|Ins|tructions ge|nerated by**D**|**eepSeek-R**|**1 (Guo et al**|**., 2025)**||
|base|84.8|26.6|84.4|57.2|63.25|-10.54%|
|+ MCSI|92.2|35.0|81.8|68.4|69.35|-1.28%|
|+ RAS & MCSI|92.2|26.6|87.2|77.4|70.85|-4.19%|
|In|structions g|enerated by|**Qwen3.5 (Q **|**wen Team, **|**2026)**||
|base|90.0|32.8|72.8|72.8|67.10|-5.10%|
|+ MCSI|95.0|34.4|71.6|75.2|69.05|-1.71%|
|+ RAS & MCSI|95.0|34.4|85.4|85.2|75.00|+1.41%|


Table 6: **Utilize different VLMs for instruction generation to train the MCSI & RAS model. MCSI** and **RAS** shows consistent performance across VLM choices with minimal variation, indicating robustness to the choice of instruction generator and generalization to underlying task semantics. 

|**VLM**|**R1**<br>SR (%)_↑_|**R2**<br>SR (%)_↑_|**R3**<br>SR (%)_↑_|**R4**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|**Drift**|
|---|---|---|---|---|---|---|
|Qwen2.5-VL (Bai et al.,2025)|97.2|30.2|89.4|79.0|73.95|0|
|InternVL3 (Chen et al.,2024)|96.8|34.0|93.0|79.2|75.75|+2.43%|
|LLaVA-OneVision (Li et al.,2024a)|96.2|33.6|91.2|73.2|73.55|-0.54%|


compared to just 1.71% for our method. 

Beyond using VLMs for rewriting, we also investigate using different VLMs for instruction generation: Beyond the original Qwen2.5-VL (Bai et al., 2025), we tested InternVL3 (Chen et al., 2024) and LLaVA-OneVision (Li et al., 2024a) for generating syntactic neighborhoods. The performance variance was minimal (2.43% and 0.54%, respectively), confirming that current VLMs provide similarly effective spatial understanding for our method (See Table 6). 

These results empirically confirm that MCSI generalizes to the underlying semantic intent of the task rather than overfitting to the specific syntax of the training teacher. 

### **4.5 Training Loss Curves** 

Figure 5 illustrates the training loss trajectories of different model variants. Across all settings, the loss decreases rapidly during the early training stage and gradually stabilizes as optimization proceeds, indicating stable convergence behavior. Compared to their corresponding baseline models, variants equipped with RAS and MCSI achieve 

lower loss values when training. This suggests that the proposed components provide a more effective training signal and facilitate smoother optimization, leading to improved learning efficiency rather than merely affecting the final performance. 

## **5 Conclusion** 

We identify a core limitation of current VLA models: their failure to robustly ground linguistic intent, resulting in instruction blindness and overreliance on visual affordance priors. To address this, we propose **Residual Semantic Steering (RSS)** , which combines **Monte Carlo Syntactic Integration** to overcome instruction manifold sparsity with **Residual Affordance Steering** to suppress visually driven biases. By explicitly disentangling semantic intent from visual priors, RSS restores consistent language–action alignment and enables robust generalization under diverse linguistic perturbations. Empirical results demonstrate that RSS significantly improves instruction robustness and semantic grounding, establishing a principled path toward reliable language-conditioned robotic control. 

## **Limitations** 

A limitation of Residual Affordance Steering (RAS) is its conservative behavior when presented with extremely vague or underspecified instructions (e.g., generic prompts like “do something”). Because our inference mechanism explicitly suppresses the “Base Affordance Distribution”—which drives standard models to aggressively execute the most common visual trajectory regardless of input—our model may exhibit hesitation or inaction when the language signal lacks sufficient semantic content to steer the policy. Unlike baseline methods that tend to ignore linguistic ambiguity and revert to rote visual pattern matching (often executing an action simply because it was frequent in the training set), our framework effectively requires semantically meaningful commands to initiate motion. This dependency prevents the model from “hallucinating” actions based on visual priors alone, ensuring that the robot does not default to unsafe autopilot behaviors when the user’s intent is unclear. 

## **Acknowledgments** 

This work was supported in part by National High-Level Young Talent Program (Grant 2025HY00260104), in part by the Fundamental Research Funds for Higher Education Institutions allocated to Sun Yat-sen University (Grant 25hytd007), in part by the Guangdong Provincial High-Level Young Talent Program (Grant 2025HYSPT0707), in part by the Tuoyuan (Grant HT-99982025-0564), in part by the Faculty Start-up Research Fund (Grant 67000-12255002), in part by the Huawei Strategic Research Institute Talent Fund, and in part by the Key Development Project of the Artificial Intelligence Institute of Sun Yat-sen University (Grant 2025RGZN009). 

## **References** 

- Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, and 1 others. 2025. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ . 

- Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, and 1 others. 2025. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ . 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, and 1 others. 2024. Pi0: A Vision-Language-Action Flow Model for General Robot Control. _arXiv preprint arXiv:2410.24164_ . 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, and 1 others. 2022. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ . 

- Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. 2025. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ . 

- Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, and 1 others. 2025. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ . 

- Yuhao Chen, Zhihao Zhan, Xiaoxin Lin, Zijian Song, Hao Liu, Qinhan Lyu, Yubo Zu, Xiao Chen, Zhiyuan Liu, Tao Pu, and 1 others. 2026. Radar: Benchmarking vision-language-action generalization via real-world dynamics, spatial-physical intelligence, and autonomous evaluation. _arXiv preprint arXiv:2602.10980_ . 

- Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, and 1 others. 2024. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 24185–24198. 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. 2023. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , page 02783649241273668. 

- Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, and 1 others. 2025. Libero-plus: Indepth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ . 

- Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, and 1 others. 2025. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ . 

- Jonathan Ho and Tim Salimans. 2022. Classifierfree diffusion guidance. _arXiv preprint arXiv:2207.12598_ . 

- Zhi Hou, Tianyi Zhang, Yuwen Xiong, Haonan Duan, Hengjun Pu, Ronglei Tong, Chengyang Zhao, Xizhou Zhu, Yu Qiao, Jifeng Dai, and 1 others. 2025. Dita: Scaling diffusion transformer for generalist vision-language-action policy. _arXiv preprint arXiv:2503.19757_ . 

- Chia-Yu Hung, Qi Sun, Pengfei Hong, Amir Zadeh, Chuan Li, U Tan, Navonil Majumder, Soujanya Poria, and 1 others. 2025. Nora: A small open-sourced generalist vision language action model for embodied tasks. _arXiv preprint arXiv:2504.19854_ . 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, and 1 others. 2025. Pi0.5: A Vision-Language-Action Model with Open-World Generalization. _arXiv preprint arXiv:2504.16054_ . 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. 2025. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ . 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, and 1 others. 2024. Openvla: An opensource vision-language-action model. _arXiv preprint arXiv:2406.09246_ . 

- Bo Li, Yuanhan Zhang, Dong Guo, Renrui Zhang, Feng Li, Hao Zhang, Kaichen Zhang, Peiyuan Zhang, Yanwei Li, Ziwei Liu, and Chunyuan Li. 2024a. Llavaonevision: Easy visual task transfer. _Transactions on Machine Learning Research_ . 

- Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, and 1 others. 2024b. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ . 

- Weiqi Li, Quande Zhang, Ruifeng Zhai, Liang Lin, and Guangrun Wang. 2025. Vla models are more generalizable than you think: Revisiting physical and spatial modeling. _arXiv preprint arXiv:2512.02902_ . 

- Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. 2025. Onetwovla: A unified vision-language-action model with adaptive reasoning. _arXiv preprint arXiv:2505.11917_ . 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. 2023. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791. 

- Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. 2024. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ . 

- Oier Mees, Dibya Ghosh, Karl Pertsch, Kevin Black, Homer Rich Walke, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, and 1 others. 2024. Octo: An open-source generalist robot policy. In _First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024_ . 

- OpenAI. 2025. Chatgpt. https://chat.openai. com/. Version 5.2. 

- Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, and 1 others. 2024. Open x- embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE. 

- Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. 2025. FAST: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ . 

- Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and 1 others. 2025. Spatialvla: Exploring spatial representations for visual-languageaction model. _arXiv preprint arXiv:2501.15830_ . 

- Qwen Team. 2026. Qwen3.5: Towards native multimodal agents. 

- Moritz Reuss, Ömer Erdinç Ya˘gmurlu, Fabian Wenzel, and Rudolf Lioutikov. 2024. Multimodal diffusion transformer: Learning versatile behavior from multimodal goals. _arXiv preprint arXiv:2407.05996_ . 

- Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Krähenbühl. 2025. Interactive post-training for vision-language-action models. _arXiv preprint arXiv:2505.17016_ . 

- Gemma Team, Thomas Mesnard, Cassidy Hardin, Robert Dadashi, Surya Bhupatiraju, Shreya Pathak, Laurent Sifre, Morgane Rivière, Mihir Sanjay Kale, Juliette Love, and 1 others. 2024. Gemma: Open models based on gemini research and technology. _arXiv preprint arXiv:2403.08295_ . 

- Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. 2023. Unleashing large-scale video generative pre-training for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ . 

- Zhihao Zhan, Jiaying Zhou, Likui Zhang, Qinhan Lv, Hao Liu, Jusheng Zhang, Weizheng Li, Ziliang Chen, Tianshui Chen, Ruifeng Zhai, Keze Wang, Liang Lin, and Guangrun Wang. 2025. E0: Enhancing generalization and fine-grained control in vla models via tweedie discrete diffusion. _arXiv preprint arXiv:2511.21542_ . 

- Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, and 1 others. 2025. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713. 

- Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daumé III, Andrey Kolobov, Furong Huang, and Jianwei Yang. 2024. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ . 

- Jiaying Zhou, Zhihao Zhan, Ruifeng Zhai, Qinhan Lyu, Hao Liu, Keze Wang, Liang Lin, and Guangrun Wang. 2026. Tag: Target-agnostic guidance for stable object-centric inference in vision-language-action models. _arXiv preprint arXiv:2603.24584_ . 

- Xueyang Zhou, Yangming Xu, Guiyao Tie, Yongchao Chen, Guowen Zhang, Duanfeng Chu, Pan Zhou, and Lichao Sun. 2025. Libero-pro: Towards robust and fair evaluation of vision-language-action models beyond memorization. _arXiv preprint arXiv:2510.03827_ . 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, and 1 others. 2023. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR. 

## **A Proof of Proposition 1: Visual Bias Decoupling via Residual Steering** 

In this section, we provide a formal derivation of Proposition 1, demonstrating how Residual Semantic Steering (RSS) restores the rank of linguistic features in the presence of dominant visual priors. 

- _Wv, Wl ∈_ R<sup>_d_</sup> are the projection weights for the visual and linguistic modalities, respectively. 

- _ϵ_ represents higher-order interaction terms and bias, assumed to be negligible for this firstorder analysis. 

**Assumption 1 (Visual Dominance):** In VLA models, the gradient flow during training is dominated by the dense visual signal, leading to spectral norms such that _∥Wv∥≫∥Wl∥_ . This implies that standard inference is driven primarily by _ϕ_ ( _o_ ). 

**Assumption 2 (Null-Text Baseline):** When the instruction is dropped (denoted as _∅_ ), the linguistic feature vector collapses to a null or bias state, denoted as _ψ_ ( _∅_ ) _≈_ **0** . Thus, the unconditional forward pass represents the pure visual affordance: 


### **A.2 Derivation of Residual Steering** 

The Residual Semantic Steering formula is defined as: 


where _γ_ is the steering coefficient. 

Substituting the linear approximations into the residual term: 


### **A.1 Setup and Definitions** 

Let _S_ ( _a|o, l_ ) _∈_ R denote the logit score for a specific action _a_ , given observation _o_ and instruction _l_ . We analyze the behavior of the model’s final layer. We assume the logit can be approximated as a linear combination of the disentangled features in the penultimate layer: 

Note that the visual term _Wv_<sup>_⊤ϕ_(</sup><sup>_o_) is explicitly can-</sup> celled out in the residual term. 

Now, we reconstruct the full steered logit _S_<sup>˜</sup> ( _a_ ): 


### **A.3 Analysis of Signal-to-Noise Ratio (SNR)** 


where: 

- _ϕ_ ( _o_ ) _∈_ R<sup>_d_</sup> is the visual embedding vector. 

- _ψ_ ( _l_ ) _∈_ R<sup>_d_</sup> is the linguistic embedding vector. 

We define the Semantic Signal-to-Noise Ratio (SNR) as the ratio of the linguistic contribution to the visual contribution. 

**Case 1: Standard Inference (** _γ_ = 1 **)** 


Given Assumption 1 ( _∥Wv∥≫∥Wl∥_ ), SNR _std →_ 0. The text has minimal impact on the action ranking. 

**Case 2: Residual Steering (** _γ >_ 1 **)** 


By choosing _γ ≫_ 1, we linearly amplify the linguistic contribution without altering the visual affordance landscape. Effectively, we synthesize a new weight vector _W_<sup>˜</sup> _l_ = _γWl_ , artificially restoring the balance between modalities. This proves that RSS orthogonalizes the semantic intent from the visual prior, as stated in Proposition 1. □ 

## **B More results on LIBERO-Plus** 

To more convincingly demonstrate the effectiveness of the proposed method, we evaluate our model on LIBERO-Plus (Fei et al., 2025) using the trained checkpoint without any additional retraining. 

As shown in the Table 7, our method demonstrates superior performance. Crucially, it not only outperforms baselines in language-perturbed subsets but also achieves the best overall performance across the benchmark compared to competitors. This confirms that our semantic integration method improves robustness without becoming sensitive to the visual domain shifts present in Libero-Plus. We will include these results in the final revision. 

## **C Detailed Results** 

This section provides a comprehensive breakdown of task-level performance across all LIBERO subtasks. Unlike the aggregated results reported in the main paper, the tables in this section present success rates for each individual subtask, enabling a fine-grained examination of model behavior under different instruction conditions. 

Specifically, Table 8 reports performance under the original, unmodified instructions, serving as a reference for canonical task execution. Tables 9, 10, 11, 12, and 13 report detailed subtask-level success rates under different instruction perturbation settings. 

## **D Detailed Ablation Results** 

Tables 14, 15, and 16 present detailed ablation results on the steering coefficient (SC) and the number of denoising steps under destructive instruction 

overwriting. All results are reported as average success rates across different language perturbation benchmarks. 

As shown in Table 14, the steering coefficient plays a critical role in balancing robustness and over-steering. Excessively large coefficients lead to noticeable performance degradation. This indicates that overly strong residual affordance steering can dominate the policy update, thereby reducing adaptability under corrupted language inputs. 

Tables 15 and 16 further show the effect of denoising steps for _π_ 0 and _π_ 0 _._ 5, respectively. Notably, _π_ 0 _._ 5 exhibits stronger overall stability across different step configurations, indicating that a stronger base language grounding reduces sensitivity to inference-time hyperparameters. 

Overall, these results demonstrate that robustness under destructive instruction overwriting depends on a careful balance between steering strength and inference depth. Moderate steering coefficients combined with sufficient denoising steps yield the most stable and consistent performance across language perturbations. 

## **E Qualitative Analysis under Destructive Instruction Overwriting** 

Figures 6 and 7 present qualitative rollouts under _destructive instruction overwriting_ , where key linguistic tokens are removed from the command. In this setting, the vanilla policies exhibit brittle behavior: although the scene remains visually unchanged, the policy fails to consistently localize the wine bottle or align it with the cabinet-top affordance, resulting in unstable grasps or premature terminations. 

Applying **MCSI** improves robustness to syntactic variation by aggregating multiple rewritten instructions; however, when critical semantic content is missing, MCSI alone is insufficient to recover the correct action intent. In contrast, **RAS** explicitly injects residual affordance signals derived from visual observations, steering the policy toward taskrelevant object–target configurations even when language supervision is severely degraded. 

Notably, the combination of **RAS+MCSI** achieves the most reliable performance. By jointly mitigating linguistic uncertainty and reinforcing visual affordance alignment, the policy consistently executes the correct placement behavior across all evaluated rollouts. This result highlights that robustness to destructive language perturbations re- 

Table 7: **LIBERO-Plus task performance (success rate, SR) results. Bold** denotes the best performance per column, respectively. Values in parentheses represent the absolute improvement over the corresponding baseline. **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

|**Model**|**Camera**<br>SR (%)_↑_|**Robot**<br>SR (%)_↑_|**Language**<br>SR (%)_↑_|**Light**<br>SR (%)_↑_|**Background**<br>SR (%)_↑_|**Noise**<br>SR (%)_↑_|**Layout**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|---|---|---|---|
|OpenVLA (Kim et al.,2024)|0.8|3.5|23.0|8.1|34.8|15.2|28.5|15.6|
|WorldVLA (Cen et al.,2025)|0.1|27.9|41.6|43.7|17.1|10.9|38.0|25.0|
|NORA (Hung et al.,2025)|2.2|37.0|65.1|45.7|58.6|12.8|62.1|39.0|
|UniVLA (Bu et al.,2025)|1.8|46.2|69.6|69.0|81.0|21.2|31.9|43.9|
|_π_0(Black et al.,2024)|13.8|6.0|58.8|85.0|81.4|79.0|68.9|53.6|
|OpenVLA-OFT (w) (Kim et al.,2025)|10.4|38.7|70.5|76.8|93.6|49.9|69.9|55.8|
|_π_0FAST (Pertsch et al.,2025)|65.1|21.6|61.0|73.2|73.2|74.4|68.8|61.6|
|OpenVLA-OFT (m) (Kim et al.,2025)|55.6|21.7|81.0|92.7|91.0|78.6|68.7|67.9|
|OpenVLA-OFT (Kim et al.,2025)|56.4|31.9|79.5|88.7|93.3|75.8|74.2|69.6|
|RIPT-VLA (Tan et al.,2025)|55.2|31.2|77.6|88.4|91.6|73.5|74.2|68.4|
|OpenVLA-OFT (plus) (Fei et al.,2025)|**92.8**|30.3|85.8|94.9|93.9|89.3|77.6|79.6|
|_π_0_._5(Intelligence et al.,2025)|64.8|71.8|83.0|93.5|92.2|78.8|85.5|81.4|
|_π_0_._5+ RAS|76.0|74.0|88.0|**97.0**|96.0|83.0|86.0|86.0(+4.6)|
|_π_0_._5+ MCSI|86.0|83.0|83.0|**97.0**|**98.0**|**92.0**|**87.0**|**90.0**(+8.6)|
|_π_0_._5+ RAS & MCSI|81.0|**88.0**|**90.0**|**97.0**|96.0|90.0|86.0|**90.0**(+8.6)|


Table 8: **LIBERO (original instruction) task performance (success rate, SR) results.** Results are reported on the four standard LIBERO sub-tasks (Libero-Spatial, Libero-Object, Libero-Goal, and Libero-Long) along with the overall average. This setting evaluates model performance under unmodified, canonical task instructions. **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

|**Model**|**Libero-Spatial**<br>SR (%)_↑_|**Libero-Object**<br>SR (%)_↑_|**Libero-Goal**<br>SR (%)_↑_|**Libero-Long**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|---|
|Diffusion Policy (Chi et al.,2023)|78.3|92.5|68.3|50.5|72.40|
|MDT (Reuss et al.,2024)|78.5|87.5|73.5|64.8|76.10|
|OpenVLA (Kim et al.,2024)|84.7|88.4|79.2|53.7|76.50|
|Octo (Mees et al.,2024)|78.9|85.7|84.6|51.1|75.10|
|Dita (Hou et al.,2025)|84.2|96.3|85.4|63.8|82.40|
|TraceVLA (Zheng et al.,2024)|84.6|85.2|75.1|54.1|74.80|
|SpatialVLA (Qu et al.,2025)|88.2|89.9|78.6|55.5|78.10|
|_π_0FAST (Pertsch et al.,2025)|96.4|96.8|88.6|60.2|85.50|
|_π_0(Black et al.,2024)|96.8|98.8|95.8|85.2|94.15|
|_π_0+ RAS|91.4|97.4|92.2|81.6|90.65|
|_π_0+ MCSI|96.6|99.8|94.8|87.0|94.55|
|_π_0+ RAS & MCSI|97.4|98.8|93.4|83.8|93.35|
|_π_0_._5(Intelligence et al.,2025)|95.4|98.4|97.2|89.6|95.15|
|_π_0_._5+ RAS|97.8|99.4|96.6|92.8|96.65|
|_π_0_._5+ MCSI|99.8|99.6|99.6|94.0|98.25|
|_π_0_._5+ RAS & MCSI|98.6|99.2|95.8|92.8|96.60|


Table 9: **LIBERO (blank instruction) task performance (success rate, SR) results.** In this variant, task instructions are fully blanked to remove explicit linguistic guidance. **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

|**Model**|**Libero-Spatial**<br>SR (%)_↑_|**Libero-Object**<br>SR (%)_↑_|**Libero-Goal**<br>SR (%)_↑_|**Libero-Long**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|---|
|_π_0(Black et al.,2024)|29.8|41.2|4.6|25.2|25.20|
|_π_0+ RAS|77.4|95.4|6.8|74.0|63.40|
|_π_0+ MCSI|57.0|50.8|9.8|49.8|41.85|
|_π_0+ RAS & MCSI|88.0|98.8|9.8|82.0|69.65|
|_π_0_._5(Intelligence et al.,2025)|65.0|51.8|11.4|72.0|50.05|
|_π_0_._5+ RAS|87.0|99.4|10.8|84.8|70.50|
|_π_0_._5+ MCSI|43.4|50.2|13.8|77.4|46.20|
|_π_0_._5+ RAS & MCSI|88.4|99.4|10.2|83.0|70.25|


Table 10: **LIBERO (simple-word instruction) task performance (success rate, SR) results.** All task instructions are replaced by a single generic command (e.g., ”do something“), completely removing the original semantic content. **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

|**Model**|**Libero-Spatial**<br>SR (%)_↑_|**Libero-Object**<br>SR (%)_↑_|**Libero-Goal**<br>SR (%)_↑_|**Libero-Long**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|---|
|_π_0(Black et al.,2024)|29.2|43.4|2.2|30.2|26.25|
|_π_0+ RAS|79.0|96.2|5.4|69.4|62.50|
|_π_0+ MCSI|58.6|48.8|9.0|43.0|39.85|
|_π_0+ RAS & MCSI|86.6|93.4|9.4|70.2|64.90|
|_π_0_._5(Intelligence et al.,2025)|47.8|56.2|10.8|72.8|46.90|
|_π_0_._5+ RAS|86.6|99.2|9.2|81.4|69.10|
|_π_0_._5+ MCSI|43.2|48.2|15.0|78.4|46.20|
|_π_0_._5+ RAS & MCSI|88.0|100.0|10.0|84.4|70.60|


Table 11: **LIBERO (multi-word instruction) task performance (success rate, SR) results.** Instructions are rewritten by replacing words in the original sentence with simple lexical alternatives, while largely preserving the overall task semantics. **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

|**Model**|**Libero-Spatial**<br>SR (%)_↑_|**Libero-Object**<br>SR (%)_↑_|**Libero-Goal**<br>SR (%)_↑_|**Libero-Long**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|---|
|_π_0(Black et al.,2024)|88.6|97.6|91.4|87.6|91.30|
|_π_0+ RAS|91.2|98.4|90.0|80.0|89.90|
|_π_0+ MCSI|96.0|99.8|92.6|85.4|93.45|
|_π_0+ RAS & MCSI|97.2|99.0|88.4|80.8|91.35|
|_π_0_._5(Intelligence et al.,2025)|95.2|99.0|95.0|92.6|95.45|
|_π_0_._5+ RAS|98.4|98.6|97.0|93.2|96.80|
|_π_0_._5+ MCSI|99.8|99.8|97.0|95.4|98.00|
|_π_0_._5+ RAS & MCSI|97.6|99.0|97.6|95.8|97.50|


Table 12: **LIBERO (random-lang instruction) task performance (success rate, SR) results.** Instructions are constructed by randomly shuffling the word order of the original sentence, disrupting syntactic structure while retaining the same lexical content. **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

|**Model**|**Libero-Spatial**<br>SR (%)_↑_|**Libero-Object**<br>SR (%)_↑_|**Libero-Goal**<br>SR (%)_↑_|**Libero-Long**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|---|
|_π_0(Black et al.,2024)|83.0|97.4|91.6|85.4|89.35|
|_π_0+ RAS|91.6|94.6|89.8|78.8|88.70|
|_π_0+ MCSI|94.2|99.2|97.0|81.4|92.95|
|_π_0+ RAS & MCSI|96.8|99.8|95.4|87.8|94.95|
|_π_0_._5(Intelligence et al.,2025)|96.4|98.8|94.8|90.8|95.20|
|_π_0_._5+ RAS|97.4|99.0|93.2|94.2|95.95|
|_π_0_._5+ MCSI|98.2|100.0|95.6|96.0|97.45|
|_π_0_._5+ RAS & MCSI|98.6|99.8|97.0|94.4|97.45|


Table 13: **LIBERO (random-mask instruction) task performance (success rate, SR) results.** Each word in the instruction is independently masked with a predefined probability, introducing controlled semantic degradation while preserving the original word order. **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 

|**Model**|**Libero-Spatial**<br>SR (%)_↑_|**Libero-Object**<br>**L**<br>SR (%)_↑_|**ibero-Goal**<br>SR (%)_↑_|**Libero-Long**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|---|
||**Rando**|**m Mask Rate = 0.2**||||
|_π_0(Black et al.,2024)|53.4|90.2|74.8|72.2|72.65|
|_π_0+ RAS|69.6|94.6|75.4|74.2|78.45|
|_π_0+ MCSI|94.2|97.4|81.0|82.8|88.85|
|_π_0+ RAS & MCSI|96.4|99.8|92.6|79.4|92.05|
|_π_0_._5(Intelligence et al.,2025)|95.0|97.4|89.6|88.6|92.65|
|_π_0_._5+ RAS|96.0|98.6|88.2|92.8|93.90|
|_π_0_._5+ MCSI|98.4|99.2|91.8|94.8|96.05|
|_π_0_._5+ RAS & MCSI|98.4|99.6|92.0|95.4|96.35|
||**Rando**|**m Mask Rate = 0.4**||||
|_π_0(Black et al.,2024)|15.2|75.0|33.0|46.8|42.50|
|_π_0+ RAS|34.2|83.8|44.8|57.4|55.05|
|_π_0+ MCSI|87.8|93.6|51.8|77.8|77.75|
|_π_0+ RAS & MCSI|93.6|100.0|71.8|78.0|85.85|
|_π_0_._5(Intelligence et al.,2025)|87.2|90.8|67.6|85.2|82.70|
|_π_0_._5+ RAS|89.6|98.8|64.6|93.6|86.65|
|_π_0_._5+ MCSI|87.6|95.4|72.0|93.8|87.20|
|_π_0_._5+ RAS & MCSI|97.0|100.0|75.6|95.4|92.00|
||**Rando**|**m Mask Rate = 0.6**||||
|_π_0(Black et al.,2024)|7.4|51.0|10.0|20.2|22.15|
|_π_0+ RAS|18.2|66.8|20.4|28.8|33.55|
|_π_0+ MCSI|81.4|84.0|24.8|65.2|63.85|
|_π_0+ RAS & MCSI|92.2|97.4|50.6|71.6|77.95|
|_π_0_._5(Intelligence et al.,2025)|71.8|79.2|43.4|83.8|69.55|
|_π_0_._5+ RAS|87.4|99.4|44.0|86.4|79.30|
|_π_0_._5+ MCSI|70.8|85.2|46.6|91.0|73.40|
|_π_0_._5+ RAS & MCSI|93.6|100.0|50.6|94.0|84.55|
||**Rando**|**m Mask Rate = 0.8**||||
|_π_0(Black et al.,2024)|0.8|13.6|5.4|11.4|7.80|
|_π_0+ RAS|9.0|36.0|8.8|18.0|17.95|
|_π_0+ MCSI|73.4|69.2|12.8|55.8|52.80|
|_π_0+ RAS & MCSI|89.0|95.0|29.2|66.4|69.90|
|_π_0_._5(Intelligence et al.,2025)|60.0|63.2|24.6|74.0|55.45|
|_π_0_._5+ RAS|83.0|97.4|23.0|80.8|71.05|
|_π_0_._5+ MCSI|50.8|69.4|27.0|84.6|57.95|
|_π_0_._5+ RAS & MCSI|89.0|99.6|29.8|91.6|77.50|


Table 14: **Ablation on steering coefficient (SC) across different language perturbation benchmarks.** Denoising steps are fixed to 10. All values are average success rate (SR, %). 

|**SC**|**Origin**<br>SR (%)_↑_|**Multi**<br>SR (%)_↑_|**Blank**<br>SR (%)_↑_|**Rand**<br>SR (%)_↑_|**M2**<br>SR (%)_↑_|**M4**<br>SR (%)_↑_|**M6**<br>SR (%)_↑_|**M8**<br>SR (%)_↑_|**Simple**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|---|---|---|---|---|---|
|||||_π_0(Bl|ack et al.,20|24) + RAS|||||
|1.25|92.45|91.00|63.25|91.05|80.40|61.00|39.45|24.15|63.40|67.35|
|1.5|90.65|89.90|63.40|88.70|78.45|55.05|33.55|17.95|62.50|64.46|
|2.0|89.50|87.95|66.15|87.90|71.75|45.45|22.05|9.00|62.05|60.20|
|3.0|81.95|82.15|64.00|79.20|58.00|25.80|7.90|1.90|58.80|51.08|
|||||_π_0_._5(Intel|ligence et al|.,2025) + R|AS||||
|1.05|97.50|96.70|69.95|96.75|93.05|84.30|77.95|71.80|70.55|84.28|
|1.1|97.25|97.05|70.35|96.15|93.25|84.50|77.30|72.30|69.80|84.22|
|1.2|97.50|97.00|69.25|95.85|93.50|85.20|79.05|72.40|69.90|84.41|
|1.25|97.40|96.80|70.00|96.55|94.70|86.85|78.30|72.20|70.10|**84.77**|
|1.5|96.65|96.80|70.50|95.95|93.90|86.65|79.30|71.05|69.10|84.43|
|1.75|96.90|96.50|70.00|96.10|94.85|85.90|77.75|69.20|69.75|84.11|
|2.0|96.70|97.00|69.45|96.25|94.00|86.00|77.40|66.90|69.15|83.65|
|3.0|96.45|96.90|68.80|96.60|94.75|87.60|75.35|55.65|68.55|82.29|


Table 15: **Ablation on denoising steps across different** **_destructive instruction overwriting_ benchmarks.** The base model is _π_ 0 (Black et al., 2024). The steering coefficient is fixed to 1.5. All values are average success rate (SR, %). 

|**Steps**|**Origin**<br>SR (%)_↑_|**Multi**<br>SR (%)_↑_|**Blank**<br>SR (%)_↑_|**Rand**<br>SR (%)_↑_|**M2**<br>SR (%)_↑_|**M4**<br>SR (%)_↑_|**M6**<br>SR (%)_↑_|**M8**<br>SR (%)_↑_|**Simple**<br>SR (%)_↑_|**Average**<br>SR (%)_↑_|
|---|---|---|---|---|---|---|---|---|---|---|
|5|93.55|92.50|66.10|91.80|80.65|56.15|34.95|18.65|65.00|66.59|
|10|90.65|89.90|63.40|88.80|78.45|55.05|33.55|17.95|62.50|64.46|
|15|90.60|89.05|63.50|89.05|75.15|53.05|32.25|16.90|62.55|63.57|


Table 16: **Ablation on denoising steps across different** **_destructive instruction overwriting_ benchmarks.** The base model is _π_ 0 _._ 5 (Intelligence et al., 2025). The steering coefficient is fixed to 1.25. All values are average success rate (SR, %). 

|**St**|**Origin**|**Multi**|**Blank**|**Rand**|**M2**|**M4**|**M6**|**M8**|**Simple**|**Average**|
|---|---|---|---|---|---|---|---|---|---|---|
|**eps**|SR (%)_↑_|SR (%)_↑_|SR (%)_↑_|SR (%)_↑_|SR (%)_↑_|SR (%)_↑_|SR (%)_↑_|SR (%)_↑_|SR (%)_↑_|SR (%)_↑_|
|5|96.90|97.35|69.90|96.65|93.90|86.50|78.70|71.45|68.90|84.47|
|15|97.40|97.20|69.35|95.60|94.30|85.00|78.90|72.00|69.60|84.37|
|20|96.85|96.60|70.30|96.65|93.45|85.60|78.05|71.60|69.80|84.32|


quires not only syntactic integration but also explicit affordance-level correction. 

## **F Instruction Rewriting Examples on Obfuscated Instruction Reinterpretation** 

As illustrated in Figures 8, 9, 10, and 11, we employ ChatGPT-5.2 (OpenAI, 2025) to automatically rewrite the original task instructions into a set of semantically equivalent but linguistically obfuscated variants. These examples demonstrate how different rewriting strategies introduce increasing levels of surface variation, contextual distraction, and semantic indirection while strictly preserving the underlying task goal. Specifically, R1 and R2 introduce task-irrelevant context and commonsensebased object descriptions, respectively. R3 further reformulates instructions by emphasizing implicit reasoning or final-state constraints, and R4 explicitly injects object-level distractors via negation. 


Figure 6: **Qualitative comparison under destructive instruction overwriting (** _π_ 0 _._ 5 **).** We visualize representative rollout trajectories for the task “Put the wine bottle on top of the cabinet” when the instruction is partially blanked. The base model is _π_ 0 _._ 5 (Intelligence et al., 2025). **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 


Figure 7: **Qualitative comparison under destructive instruction overwriting (** _π_ 0 **).** We visualize representative rollout trajectories for the task “Put the wine bottle on top of the cabinet” when the instruction is partially blanked. The base model is _π_ 0 _._ 5 (Black et al., 2024). **RAS** : Residual Affordance Steering; **MCSI** : Monte Carlo Syntactic Integration. 


Figure 8: **R1-Distraction.** The instruction is augmented with task-irrelevant conversational or contextual content, such as background descriptions or auxiliary remarks, while keeping the core action and target unchanged. 


Figure 9: **R2-Common Sense.** Object names are replaced with commonsense-based descriptive phrases that implicitly convey their functional or physical properties. Although the task intent remains unchanged, this variant requires the model to extract relevant semantics from more abstract and verbose descriptions. 


Figure 10: **R3-Reasoning Chain.** The instruction is reformulated to emphasize implicit reasoning, execution order, or final-state constraints, either by introducing lightweight reasoning cues or by abstracting intermediate steps. The target task remains identical, but the linguistic form encourages reasoning-based interpretation. 


Figure 11: **R4-Confusion.** The instruction explicitly introduces distractor objects or actions through negation or contrast, while still specifying the correct target object and goal. This variant probes the model’s ability to resist object-level confusion and focus on task-relevant semantics. 

