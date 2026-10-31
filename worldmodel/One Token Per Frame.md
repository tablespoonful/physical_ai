---
title: "One Token Per Frame: Reconsidering Visual Bandwidth in World Models for VLA Policy"
date: "2026-05-08"
authors: "Zuojin Tang; Shengchao Yuan; Xiaoxin Bai; Zhiyuan Jing; De Ma; Gang Pan"
url: https://arxiv.org/abs/2605.07931
pdf: https://arxiv.org/pdf/2605.07931
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.07931)** / [論文ページ](https://arxiv.org/abs/2605.07931)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Preprint 

# ONE TOKEN PER FRAME: RECONSIDERING VISUAL BANDWIDTH IN WORLD MODELS FOR VLA POLICY 

**Zuojin Tang**<sup>1</sup> **Shengchao Yuan**<sup>2</sup> **Xiaoxin Bai**<sup>3</sup> **Zhiyuan Jing**<sup>5</sup> **De Ma**<sup>1</sup> **Gang Pan**<sup>1</sup><sup>_∗_</sup> **Bin Liu**<sup>4</sup><sup>_∗_</sup> 1Zhejiang University 2Central South University 3Harbin Institute of Technology 4Embodied Intelligence General Platform Laboratory, Chery Auto 5E-surfing Digital Life Technology Co., Ltd., China Telecom 

> _∗_ Corresponding Author 

## ABSTRACT 

Vision-language-action (VLA) models can use visual prediction to anticipate future states, but dense visual features make the generative sequence grow with the number of camera views, prediction horizon, and encoder resolution. Whether such dense representations are necessary for effective control remains unclear. We introduce **OneWM-VLA** , which represents each retained camera view with one predictive token per future step. Adaptive Attention Pooling compresses visual features into compact latents, which are jointly generated with robot actions under a conditional flow-matching objective. Future observations provide the latent targets during training and are not required at inference. This design incorporates visual prediction into a pretrained VLA policy while keeping the generative sequence compact. On MetaWorld MT50, OneWM-VLA improves the average success rate of the _π_ 0 backbone from 47 _._ 91% to 61 _._ 53%, reaching 72 _._ 01% after 60k training steps. It also achieves 98 _._ 1% success on LIBERO and raises _Fold Cloth_ success on a real Piper arm from 20 _._ 0% to 60 _._ 0% relative to _π_ 0. Comparisons on two additional VLA backbones consistently favor one token over three across the evaluated checkpoints. A matched ablation at a longer action horizon further shows that removing the latent loss reduces success from 58 _._ 09% to 21 _._ 64%, supporting the benefit of future supervision for policy learning. 

## 1 INTRODUCTION 

Vision-language-action (VLA) models map visual observations, language instructions, and robot states to actions. Recent systems Brohan et al. (2022); Zitkovich et al. (2023); Kim et al. (2024; 2025); Chi et al. (2025); Black et al. (2026); Intelligence et al. (2025) show that large multimodal backbones can support many language-conditioned manipulation tasks. Long-horizon control, however, requires more than reacting to the current observation. A policy must retain task-relevant state, anticipate changes in contacts and object configurations, and keep local errors from accumulating over time. This has motivated VLA policies that augment action generation with predicted frames, latent states, or other future targets Cen et al. (2025b); Zhang et al. (2025b); Hu et al. (2024). 

Prediction creates a basic design tradeoff. Dense future features preserve spatial detail, but every retained view contributes another block of visual tokens at every future step. When one transformer co-generates predictions and actions, every additional predictive token participates in each sampling step. The sequence length therefore grows with both the prediction horizon and the encoder resolution. This cost is especially relevant when the predictive stream is added to a pretrained VLA under a limited adaptation budget. Recurrent state-space models Hafner et al. (2019; 2025) and joint-embedding predictors LeCun (2022); Bardes et al. (2024) suggest that useful future information need not take the form of dense reconstruction, but they do not determine how much visual information a generative VLA should retain for control. 

We refer to this allocation as _predictive visual bandwidth_ : the number of visual tokens assigned to each retained view and future step. This bandwidth controls both the capacity of the predictive representation and the length of the generated suffix. An overly narrow representation may discard 

1 

Preprint 


Figure 1: OneWM-VLA represents each retained camera view at each future step with one predictive token. Total suffix length grows with the horizon, while the per-step predictive bandwidth is independent of the encoder patch count. 

task-relevant changes, whereas a wide representation may increase memory and sampling cost without improving the action policy. This makes the operating point an empirical design choice for the joint visual–action generator, rather than a direct consequence of the encoder patch count. Our central question is whether a single predictive token per view can retain useful future structure while keeping the generated trajectory compact. 

We introduce **OneWM-VLA** (Fig. 1) to study this question. Adaptive Attention Pooling compresses the encoder features of each retained camera view into one token per frame. During training, the same module extracts targets from future frames, producing a compact latent trajectory aligned with the demonstrated actions. A conditional flow then generates the latent and action trajectories together. The interleaved sequence places each future latent block before its action block, allowing the action stream to use the current latent estimate while both trajectories are generated. The latent trajectory remains internal to the policy, while only the generated actions are executed. We initialize the policy from _π_ 0 Black et al. (2026) and adapt the backbone with LoRA Hu et al. (2022) together with the pooling and projection modules. 

We evaluate OneWM-VLA at three levels. At the policy level, it improves the average success rate of _π_ 0 from 47 _._ 91% to 61 _._ 53% under the primary MetaWorld MT50 protocol, reaches 98 _._ 1% on LIBERO, and, relative to _π_ 0, raises success on the real-world _Fold Cloth_ task from 20 _._ 0% to 60 _._ 0%. At the design level, we study predictive bandwidth, longer training, pooling, target construction, latent supervision, and action horizon, with additional bandwidth comparisons on _π_ 0 _._ 5 and SmolVLA. At the representation level, we test whether the latent representation collapses and whether it retains task structure. Together, these experiments evaluate the performance and cost of the compact interface across training durations and backbones. 

Our contributions are as follows: 

- We formulate predictive visual bandwidth as a design choice in generative VLA policies and study its relation to sequence length and control performance. 

- We introduce OneWM-VLA, which compresses each retained view into one predictive token and co-generates the latent and action trajectories in the same flow. 

- We evaluate the design across three manipulation settings, with longer training, additional VLA backbones, alternative target constructors, and representation diagnostics. 

## 2 RELATED WORK 

### 2.1 VISION-LANGUAGE-ACTION MODELS 

Progress in multimodal language models Beyer et al. (2024); Li et al. (2023); Wang et al. (2024); Bai et al. (2025b;a) and large robot datasets has led to VLA policies that map images, instructions, and robot state to actions Brohan et al. (2022); Zitkovich et al. (2023); Kim et al. (2024); Intelligence et al. (2025); Zhao et al. (2023); Chen et al. (2025); Black et al. (2026); Tang et al. (2025b); Qu et al. (2025); Bu et al. (2025); Zheng et al. (2025); Kim et al. (2025); Goyal et al. (2025); Team et al. (2024); Shukor et al. (2025). Diffusion and flow-matching policies Chi et al. (2025); Black et al. (2026); Intelligence et al. (2025); Liu et al. (2024) model multimodal action distributions; other methods add reasoning traces, auxiliary heads, or intermediate multimodal outputs Zhao et al. (2025); Ye et al. (2025); Zeng et al. (2025); Huang et al. (2025); Team et al. (2025); Li et al. (2024b). OneWM-VLA retains the existing flow-based action generator and studies how much bandwidth to allocate to its predictive visual stream. 

2 

Preprint 


Figure 2: **OneWM-VLA.** Adaptive Attention Pooling compresses the base and left-wrist views. The expert samples interleaved latent and action blocks with a shared flow time; only the actions are executed. 

### 2.2 PREDICTIVE REPRESENTATIONS AND LATENT PLANNING 

Compact visual representations and learned rewards have been widely studied for robotic control Nair et al. (2022); Ma et al. (2022; 2023); Li et al. (2024a). Pixel- and video-space methods predict future observations as goals or auxiliary targets Cen et al. (2025b); Bjorck et al. (2025); Cheang et al. (2024); Zhen et al. (2024); Xiao et al. (2025); Du et al. (2023); Jang et al. (2025), while subgoal generation and latent planning provide future guidance for downstream policies Xie et al. (2025); Liu et al. (2025); other systems generate visual futures and actions in a shared model Guo et al. (2024); Zhang et al. (2025a); Hu et al. (2024); Cen et al. (2025a); Jiang et al. (2025); Zhang et al. (2025b). Latent state-space models Hafner et al. (2019; 2025), joint-embedding prediction LeCun (2022); Bardes et al. (2024); Assran et al. (2023); Maes et al. (2026); Tang et al. (2026a); Chen et al. (2026); Tang et al. (2026b), and sequence models Chen et al. (2021); Tang et al. (2025a) show that useful prediction need not reconstruct every pixel. 

Across these lines of work, predictive targets range from dense observations to compact learned states, and joint visual–action generation is already established. OneWM-VLA studies a specific interface within a pretrained flow-based VLA: one predictive token per retained view and future step. Our contribution is the design and empirical evaluation of this compact configuration, including its measured cost and its dependence on target construction, training duration, and backbone. 

## 3 METHOD 

Flow matching learns a velocity field along a path between data and noise, and its conditional form provides a closed-form regression target without ODE integration during training Lipman et al. (2022). OneWM-VLA retains the straight path of the _π_ 0 action generator and extends it to visual latents. The method has two components (Fig. 2). Adaptive Attention Pooling maps each retained view to one latent target token (Sec. 3.1), and a shared flow generates the future latent and action trajectories together (Sec. 3.2). We use the _L_ 1 velocity-regression loss selected in Appendix C. 

### 3.1 PER-FRAME COMPRESSION VIA ADAPTIVE ATTENTION POOLING 

Adaptive Attention Pooling reduces each retained camera view to one token per frame (Fig. 3). For view _i_ , the pretrained PaliGemma encoder Beyer et al. (2024) produces _N_ =256 patch features, denoted by _{_ **x**<sup>(</sup> _i_<sup>_n_)</sup> _}_<sup>_N_</sup> _n_ =1<sup>.Each feature lies in R</sup><sup>_D_, with</sup><sup>_D_=2048.The pooling module scores these</sup> features in three complementary ways: 


3 

Preprint 

where _Qθi_ is a small view-specific MLP. Within each branch, a softmax over these scores at temperature _τp_ gives the patch weights. The MAX branch applies a coordinate-wise maximum to the weighted features, while the SUM and LEARN branches use weighted sums. This produces three pooled vectors **p** _i,m_ . 

Learned logits _αi,m_ define the branch weights that combine these vectors into the final token: 


where _M_ = _{_ MAX _,_ SUM _,_ LEARN _}_ . We apply the module independently to the base and left-wrist views, denoted by _V_ = _{b, w}_ . The patch weights adapt to each frame, while the branch weights are learned across the training set. The result is one compact token per retained view and frame, independent of the number of encoder patches. Across future steps, these tokens form the clean latent sequences used below. In the direct- _K_ bandwidth comparisons, _K_ counts the fused output tokens actually passed to the model per view and frame; branch fusion remains enabled at every token budget. 

### 3.2 JOINT LATENT–ACTION FLOW MATCHING 

A classical transition model predicts _p_ ( _st_ +1 _| st, at_ ). OneWM-VLA instead treats both future actions and visual latents as generated variables and models 


This defines a conditional flow over aligned action and latent sequences. The two streams share one flow time and are updated synchronously. At each future step, the action block can use the current latent iterates without waiting for a completed latent rollout. This differs from a two-stage latent planner followed by inverse dynamics: no observed future state or latent is available at inference, and action updates do not wait for the latent trajectory to finish. 

During training, the same visual encoder and pooling module are applied to the corresponding future frames to construct clean latent targets; 


Figure 3: **Adaptive Attention Pooling.** Three scoring branches aggregate patch features from each view, and learned branch weights fuse the pooled vectors into one predictive token. 

future frames are never inference inputs. Let _a_ denote the future action sequence and _zi_ the latent sequence for view _i_ . These latent variables enter the expert as continuous features. Following the straight path used by _π_ 0 Black et al. (2026), the action and latent variables share one sampled flow time: 


where the noise terms are sampled independently from a standard Gaussian. The target velocities are _u_<sup>_a_</sup> _t_<sup>=</sup><sup>_ϵa−a_and</sup><sup>_uz_</sup> _t_<sup>_i_=</sup><sup>_ϵz_</sup> _i_<sup>_−zi_.</sup> 

The pooled current-view tokens and language tokens form the conditioning prefix, followed by the current robot-state block; neither attends to the generated suffix. The suffix interleaves latent and action variables by future step, with the latent queries placed before the action query at each step. Each latent block attends to the conditioning blocks, latent blocks through the same future step, and action blocks at earlier steps. Each action query attends to the conditioning blocks, all earlier suffix blocks, its own noisy iterate, and the latent iterates at the same step. Training and inference use the same block-visibility pattern. 

A shared transformer predicts the action and latent velocity fields with the joint objective 


4 

Preprint 


Figure 4: Evaluation suites used in this work: the LIBERO and MetaWorld MT50 simulation benchmarks, and a real Piper robot arm. 

The latent and action streams share the generator, flow time, and attention layers, so their predictions evolve together during ODE sampling. View-specific linear input and output projections connect each latent stream to the expert, while a separate head predicts action velocity. Thus, the latent and action variables are updated in one conditional flow, while the visibility mask allows each action block to use the corresponding latent iterates. 

**Future-target supervision.** The latent velocity loss is the only objective that directly supervises the future-latent stream. Its clean endpoints are extracted from the corresponding observed future frames, tying each latent target to a specific future observation and time step. We examine target variation and task separation through covariance-spectrum and feature-space diagnostics in Sec. 4.3.3. 

At inference, let _c_ = ( _ot, ℓ, st_ ) denote the observed context and let **x** _t_ collect all action and viewspecific latent variables. Starting from **x** 1 _∼N_ (0 _, I_ ), we solve 


from _t_ =1 to _t_ =0. Only the action component of **x** 0 is executed; the generated latent trajectory remains internal to the policy. 

## 4 EXPERIMENTS 

We evaluate our method on MetaWorld MT50, LIBERO, and a real Piper arm. MetaWorld is the primary benchmark, with a five-step action horizon used for the primary _π_ 0 experiments unless stated otherwise. We then organize the remaining evidence as ablations and diagnostics of predictive bandwidth, target construction, latent supervision, representation quality, and temporal robustness. 

### 4.1 EXPERIMENTAL SETUP 

**Benchmarks. MetaWorld MT50** McLean et al. (2025) contains 50 manipulation tasks, grouped into Easy, Medium, Hard, and Very Hard tiers (Appendix A). We evaluate each task for 10 episodes, average task success rates within each tier, and report the unweighted mean of the four tier rates. This convention applies to all MetaWorld MT50 average success rates in the main text and appendix. A separate study evaluates longer action horizons of up to 30 steps. **LIBERO** Liu et al. (2023) contains the Spatial, Object, Goal, and Long suites, with Long emphasizing extended-horizon manipulation. Overall success is the unweighted mean of the four suite success rates. **Real-world Piper** uses a 6-DoF arm with a parallel gripper. We evaluate _Pick Banana_ , _Fold Cloth_ , and _Pull Drawer_ with 20 trials per task in each of two conditions: clean observations and combined perturbations involving lighting changes, object shifts, and unseen distractors. For each condition, overall success is the mean of the three task success rates. Training and inference use action chunks of 50 steps. Figure 4 summarizes the three evaluation settings. 

**Implementation.** We build OneWM-VLA on _π_ 0 Black et al. (2026) and use LoRA Hu et al. (2022) for adaptation. Dense non-LoRA Gemma weights remain frozen, while SigLIP, pooling, and projection modules are trained along with the LoRA adapters. Sampling uses 10 ODE steps; the action loss has weight 1 _._ 0, and each latent loss has weight 0 _._ 1. The primary MetaWorld models are trained for 30k steps on 8 NVIDIA A800 GPUs. For the main LIBERO evaluation, all suites share 

5 

Preprint 

Table 1: MetaWorld MT50 success rates (%). ∆ _π_ 0 is the percentage-point gain over _π_ 0 at the same horizon. The five-step setting is our primary protocol. 

|**Method**|**Horizon**|**Easy**|**Medium**|**Hard**|**Very Hard**|**Avg%**|∆_π_0|
|---|---|---|---|---|---|---|---|
|Diff. Policy|5|8.21|0.00|0.00|0.00|2.05|–|
|ACT|5|31.43|11.82|0.00|4.00|11.81|–|
|_π_0|5|71.79|**48.18**|41.67|30.00|47.91|–|
|**OneWM-VLA**|5|**79.29**|41.82|**65.00**|**60.00**|**61.53**|**+13.62**|
|Diff. Policy|10|9.64|0.00|0.00|0.00|2.41|–|
|ACT|10|47.50|7.27|0.00|4.00|14.69|–|
|_π_0|10|77.50|30.91|30.00|**48.00**|46.60|–|
|**OneWM-VLA**|10|**78.57**|**31.82**|**58.33**|40.00|**52.18**|**+5.58**|
|Diff. Policy|25|8.93|0.00|0.00|0.00|2.23|–|
|ACT|25|31.43|0.00|0.00|0.00|7.86|–|
|_π_0|25|73.93|27.27|**36.67**|22.00|39.97|–|
|**OneWM-VLA**|25|**74.64**|**30.00**|25.00|**54.00**|**45.91**|**+5.94**|
|Diff. Policy|30|6.43|0.00|0.00|0.00|1.61|–|
|ACT|30|31.43|0.00|0.00|0.00|7.86|–|
|_π_0|30|**80.00**|**35.45**|35.00|4.00|38.61|–|
|**OneWM-VLA**|30|72.86|33.64|**45.00**|**60.00**|**52.87**|**+14.26**|


one checkpoint trained with an action horizon of 20; inference settings are selected on a held-out validation set (Appendix D). 

**Baselines.** Our primary backbone baseline is _π_ 0 Black et al. (2026). The LIBERO and real-robot comparisons also include _π_ 0 _._ 5 Intelligence et al. (2025). We also report available results for Diffusion Policy Chi et al. (2025), ACT Zhao et al. (2023), Octo Team et al. (2024), OpenVLA Kim et al. (2024), SpatialVLA Qu et al. (2025), CoT-VLA Zhao et al. (2025), WorldVLA Cen et al. (2025b), GR00T-N1 Bjorck et al. (2025), and DreamVLA Zhang et al. (2025b). For methods drawn from prior work, we retain the values in their published evaluation records. Paired ablations use a common training and evaluation protocol within each study. 

### 4.2 OVERALL PERFORMANCE 

Table 2: Main results on LIBERO. Success rates (%) on the four suites. Inference-time configuration is detailed in Appendix D. 

|**Method**|**Spatial **|**Object **|**Goal **|**Long **|**Avg%**|
|---|---|---|---|---|---|
|Diffusion Policy|78.3|92.5|68.3|50.5|72.4|
|Octo|78.9|85.7|84.6|51.1|75.1|
|OpenVLA|84.7|88.4|79.2|53.7|76.5|
|SpatialVLA|88.2|89.9|78.6|55.5|78.1|
|CoT-VLA|87.5|91.6|87.6|69.0|83.9|
|WorldVLA|87.6|96.2|83.4|60.0|81.8|
|SmolVLA|93.0|94.0|91.0|77.0|88.8|
|GR00T-N1|94.4|97.6|93.0|90.6|93.9|
|DreamVLA|97.5|94.0|89.5|89.5|92.6|
|_π_0|96.8|98.8|95.8|85.2|94.2|
|_π_0_._5|**98.8**|98.2|98.0|92.4|96.9|
|**OneWM-VLA**|98.2|**99.6**|**99.0**|**95.6**|**98.1**|


Table 3: Real-world Piper manipulation results. Success rates (%) on three tasks under clean observations and combined perturbations. 

|**Method**<br>**P**|**.Banana**|**F.Cloth**|**P.Drawe**|**r Avg%**|
|---|---|---|---|---|
|_Clean conditions_|||||
|_π_0|**100.0**|20.0|30.0|50.0|
|_π_0_._5|**100.0**|25.0|50.0|58.3|
|**OneWM-VLA**|**100.0**|**60.0**|**55.0**|**71.7**|
|_With observation_|_noise_||||
|_π_0|65.0|0.0|10.0|25.0|
|_π_0_._5|60.0|10.0|25.0|31.7|
|**OneWM-VLA**|**75.0**|**40.0**|**35.0**|**50.0**|


**MetaWorld MT50.** At five steps, our method attains 61 _._ 53% average success, a 13 _._ 62-point gain over _π_ 0 (Tab. 1). The gain is concentrated on the Hard and Very Hard tiers; the Medium tier decreases from 48 _._ 18% to 41 _._ 82%, so the aggregate gain does not extend to every task group. The remaining rows use matched non-primary horizons and are analyzed separately in Sec. 4.3.4. 

6 

Preprint 

Table 4: **Predictive bandwidth ablation** on MetaWorld MT50 ( _H_ = 5, 30k training steps). _K_ is the number of tokens per view and frame. The _K_ = 1 result uses the primary _H_ = 5 setting in Tab. 1; OOM denotes out of memory. 

|_K_|Total tokens|Trainable (M)|Memory|Latency (ms)|Avg. Success (%)|
|---|---|---|---|---|---|
|256 (Full)|_>_2_,_500|488.83|OOM|–|–|
|6|126|482.78|Stable|52.95|59.43|
|3|90|482.76|Stable|52.47|60.63|
|**1**|**66**|**482.73**|**Stable**|**44.69**|**61.53**|


**LIBERO.** OneWM-VLA achieves 98 _._ 1% average success, above _π_ 0 and _π_ 0 _._ 5, with its clearest advantage on the Long suite (Tab. 2). The same checkpoint is used across all four suites; Appendix D lists the fixed inference settings. The Object and Goal suites are close to saturation for these three models, whereas the Long suite leaves a clearer margin. The larger margin on Long is consistent with the intended use of the design in extended interactions; the comparison evaluates the full policy and its validation-selected inference settings. 

**Real-world Piper.** Relative to _π_ 0, OneWM-VLA raises the clean-condition average from 50 _._ 0% to 71 _._ 7%, with the largest gain on _Fold Cloth_ , where success rises from 20 _._ 0% to 60 _._ 0% (Tab. 3). Under the combined observation-perturbation setting, it has the highest result on all three tasks. These results provide an initial real-robot validation of the design. The improvement is largest on the deformable-object task, while clean-condition Pick Banana is tied at 100 _._ 0% and Pull Drawer shows a smaller gain. 

Across the simulation benchmarks and the real robot, the largest observed gains occur on the more demanding settings: the Hard and Very Hard MetaWorld tiers, LIBERO-Long, and _Fold Cloth_ . LIBERO Object/Goal and clean-condition Pick Banana are near saturation, so the aggregate improvement is not a uniform shift across all task groups. This pattern motivates the controlled studies below, which examine the compact interface separately from the overall policy comparisons. 

### 4.3 ABLATIONS AND DIAGNOSTICS 

We organize the controlled studies around four questions: how much predictive bandwidth is needed, how the one-token target should be constructed, how the future-latent stream behaves, and whether the gains persist across action horizons. We first examine success and measured cost across token budgets, then training checkpoints and transfer across backbones. These studies evaluate the complete compression configurations; the remaining ablations examine target construction and representation quality. Each study is interpreted within its stated evaluation protocol. 

### 4.3.1 Q1: HOW MUCH PREDICTIVE BANDWIDTH IS NEEDED? 

We first investigate predictive bandwidth at an action horizon of _H_ = 5. Here, _K_ denotes the number of tokens retained per view and frame. Table 4 compares dense encoder features ( _K_ = 256) with compact configurations ( _K ∈{_ 1 _,_ 3 _,_ 6 _}_ ). All compact variants use direct- _K_ outputs: the three pooling branches remain fused, and _K_ is the number of fused tokens passed to the model. The same compression is used for current observations and future targets, so this study compares complete compression configurations. 

**Inference feasibility and compute overhead.** Preserving dense encoder features ( _K_ = 256) produces a recorded sequence of more than 2 _,_ 500 tokens and runs out of memory in the measured setup. All three compact configurations run within that memory budget. From _K_ = 1 to _K_ = 6, trainable parameters increase by 0 _._ 05 M, from 482 _._ 73 M to 482 _._ 78 M, while measured latency rises by 18 _._ 5%, from 44 _._ 69 ms to 52 _._ 95 ms. The table’s sequence counts should be distinguished from the generated suffix alone, whose length is _H_ (2 _K_ + 1) for two views and one action token per step. Latents and actions are sampled synchronously, rather than through an autoregressive rollout. 

**Policy grounding performance.** In the primary ablation (Tab. 4), the one-token configuration reaches 61 _._ 53% average success, compared with 60 _._ 63% and 59 _._ 43% for three and six tokens. 

7 

Preprint 

Table 5: Average success rates (%) across training checkpoints (horizon 5) on MetaWorld MT50. Bold marks each row’s highest value. 

|Checkpoint|_K_ = 1|_K_ = 3|_K_ = 6|
|---|---|---|---|
|10k|48.12|**48.72**|35.91|
|20k|**60.25**|49.37|58.92|
|30k|**61.53**|60.63|59.43|
|40k|58.10|58.07|**64.80**|
|50k|**68.31**|64.20|64.05|
|60k|**72.01**|62.03|61.49|


Table 6: OneWM performance across VLA backbones on MetaWorld MT50 at horizon 5: average success rates (%) and paired gains. 

|Backbone|Steps|_K_ = 1|_K_ = 3|Difference|
|---|---|---|---|---|
|_π_0_._5|10k|**62.4**|60.0|+2.4|
||20k|**65.4**|65.0|+0.4|
||30k|**70.6**|68.2|+2.4|
|SmolVLA|10k|**66.2**|61.4|+4.8|
||20k|**71.6**|68.2|+3.4|
||30k|**74.8**|69.6|+5.2|


Table 7: Pooling ablation on LIBERO at horizon 5 under the common 30k-step adaptation schedule. 

|**Method**|**Spatial **|**Object **|**Goal **|**Long **|**Avg%**|
|---|---|---|---|---|---|
|**OneWM-VLA**|**96.6**|**96.8**|**94.6**|**85.0**|**93.3**|
|Static avg-pooling|77.8|78.0|94.0|41.4|72.8|
|No branch fusion|72.4|70.4|43.0|4.4|47.6|


Table 8: Pooling branch ablation on MetaWorld MT50 (at horizon 5, 30k steps). 

|**Method**|**Easy **|**Medium **|**Hard **|**V-Hard **|**Avg%**|
|---|---|---|---|---|---|
|**OneWM-VLA**|79.29|**41.82**|**65.00**|60.00|**61.53**|
|Only LEARN|78.57|29.09|35.00|60.00|50.67|
|Only MAX|53.21|16.36|0.00|20.00|22.39|
|Only SUM|**86.43**|26.36|46.67|**62.00**|55.36|


Table 9: Adaptive pooling and sequence-to-one MLP targets across action horizons. Entries are MetaWorld average success rates; the last column averages the six horizons. 

|Constructor|_H_ = 5|10|15|20|25|30<br>Avg.|Success (%)|
|---|---|---|---|---|---|---|---|
|MLP|58.91|**52.36**|40.18|34.91|35.27|35.85|42.91|
|Adaptive pooling|**61.53**|52.18|**52.41**|**58.09**|**45.91**|**52.87**|**53.83**|


Together with its lower measured latency, these results support the compact configuration as a practical operating point. 

**Training checkpoints.** Table 5 compares _K ∈{_ 1 _,_ 3 _,_ 6 _}_ under the same training and evaluation settings. At 60k, success is 72 _._ 01%, 62 _._ 03%, and 61 _._ 49%, respectively: one token is higher by 9 _._ 98 points than the best wider configuration at this checkpoint. It is highest at four of the six reported checkpoints, with _K_ = 3 higher at 10k and _K_ = 6 higher at 40k. These results support the compact configuration at the longer training budget, while showing that its advantage varies during training. 

**Transfer across VLA backbones.** We also integrate OneWM into _π_ 0 _._ 5 and SmolVLA-0.45B. One token is higher than three in all six paired backbone/checkpoint comparisons (Tab. 6), with margins of 2 _._ 4 and 5 _._ 2 points at 30k on the two backbones. This extends the observed ordering beyond _π_ 0, although the smallest margin is only 0 _._ 4 points. Both variants include OneWM, so these comparisons measure the relative performance of two compression configurations after integration. 

4.3.2 Q2: HOW SHOULD THE PREDICTIVE TARGET BE CONSTRUCTED? 

We next examine how the encoder features are aggregated into predictive targets. The controlled studies compare the full adaptive multi-branch module with static pooling, removing fusion, and retaining one scoring branch. The LIBERO ablation uses a separate run with _H_ = 5 and 30k training steps, so its absolute values should not be compared directly with the main checkpoint in Tab. 2. The full pooling module has the highest aggregate in both studies. On LIBERO, it reaches 93 _._ 3%, compared with 72 _._ 8% for static averaging, and removing branch fusion is substantially worse; the largest separation appears on Long (Tab. 7). On MetaWorld, the fused module reaches 61 _._ 53%, above every individual branch (Tab. 8). The SUM branch is stronger on two individual tiers, so the aggregate advantage does not imply that the fused module is best on every tier. 

**Target constructor at fixed bandwidth.** We compare Adaptive Attention Pooling with a sequenceto-one MLP using identical encoder features and one-token, 2048-D targets, with the downstream flow, attention mask, training schedule, and evaluator held fixed. Adaptive pooling achieves higher 

8 

Preprint 

success at five of the six action horizons in Tab. 9, averaging 53 _._ 83% compared with 42 _._ 91% for the MLP, a gain of 10 _._ 92 percentage points. Over _H ∈{_ 15 _,_ 20 _,_ 25 _,_ 30 _}_ , the mean gain is 15 _._ 77 points; the MLP is higher at _H_ = 10 by 0 _._ 18 points. These results support Adaptive Attention Pooling as the target constructor across the tested action horizons. 

### 4.3.3 Q3: WHAT DOES FUTURE SUPERVISION CONTRIBUTE? 

We first compare the full model with an architecture-matched model trained without the latent loss, using 30k training steps and _H_ = 20 (Tab. 16). The architecture, training budget, horizon, camera settings, and evaluation protocol are identical; only the latent loss is removed. Average success falls from 58 _._ 09% to 21 _._ 64%, a 36 _._ 45-point decrease, with lower success in every difficulty group. This matched comparison supports the contribution of future-frame supervision to control. 

We then examine the variation retained by the compact representation. Appendix F details the representation diagnostics reported in Tab. 17. At 30k steps, the _H_ = 5 full model has a target entropy effective rank of 21 _._ 42 and a participation rank of 8 _._ 88, compared with 1 _._ 83 and 1 _._ 31 without the latent loss. The full model retains variation along multiple directions, while the no-loss control is close to rank one. We also compare the full-dimensional Fisher ratio be- 

Table 10: Task separation on LIBERO-Long with normalized within-task scatter. 

||tr(_SB_)|tr(_SW_)||
|---|---|---|---|
|**Representation**|**(norm.)**|**(norm.)**|_F_|
|Before pooling|0.524|1.000|0.524|
|After pooling|0.405|1.000|0.405|


fore and after pooling on the same time-aligned LIBERO-Long samples (Appendix G). The pooled representation retains 77 _._ 3% of the reference Fisher ratio (Tab. 10), decreasing from 0 _._ 524 to 0 _._ 405. Compression therefore weakens task separation while preserving measurable between-task variation relative to within-task variation. This measures retained task variation, rather than the preservation of every control-relevant factor. 

### 4.3.4 Q4: DO THE GAINS PERSIST ACROSS ACTION HORIZONS? 

We next examine the non-primary horizons in Tab. 1. OneWM-VLA has higher aggregate success than _π_ 0 at every matched horizon, but the margin is not monotonic. At the longest horizon, the gain is concentrated on Hard and Very Hard tasks, while _π_ 0 remains stronger on Easy and Medium tasks. These results show that the observed advantages extend across the evaluated action-chunk lengths, without increasing monotonically with horizon. 

## 5 CONCLUSION AND DISCUSSION 

We presented OneWM-VLA, which represents each retained camera view with one predictive token per future step and generates predictive latents and actions through a joint conditional flow. This design introduces future-frame supervision without carrying dense visual features through the generative sequence. Across MetaWorld MT50, LIBERO, and a real Piper arm, it achieves higher aggregate success than _π_ 0, with the clearest gains on difficult and extended interactions. The compact configuration has the highest success at the final checkpoint of the training comparison and outperforms the wider alternative in the paired studies on two additional VLA backbones. The ablations also highlight the roles of future-frame supervision, adaptive pooling, and future-target construction, while the representation analyses show nonconstant targets and retained task-related variation. Overall, our results support compact predictive latents as an effective interface between visual prediction and action generation in the evaluated settings. 

**Limitations.** Our results support one token as an effective configuration rather than a universal optimum. The bandwidth sweep changes current-observation and future-target token counts together. The collapse diagnostics are empirical and provide no general guarantee, which would require additional assumptions or explicit objective and architectural constraints. The real-robot evaluation covers only a small set of tasks; broader studies across tasks and robots, and controls that isolate future-token count, remain future work. 

9 

Preprint 

## REFERENCES 

- Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, and Nicolas Ballas. Self-supervised learning from images with a joint-embedding predictive architecture. In _2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 15619–15629. IEEE, 2023. 

- Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao, Chunjiang Ge, Wenbin Ge, Zhifang Guo, Qidong Huang, Jie Huang, Fei Huang, Binyuan Hui, Shutong Jiang, Zhaohai Li, Mingsheng Li, Mei Li, Kaixin Li, Zicheng Lin, Junyang Lin, Xuejing Liu, Jiawei Liu, Chenglong Liu, Yang Liu, Dayiheng Liu, Shixuan Liu, Dunjie Lu, Ruilin Luo, Chenxu Lv, Rui Men, Lingchen Meng, Xuancheng Ren, Xingzhang Ren, Sibo Song, Yuchong Sun, Jun Tang, Jianhong Tu, Jianqiang Wan, Peng Wang, Pengfei Wang, Qiuyue Wang, Yuxuan Wang, Tianbao Xie, Yiheng Xu, Haiyang Xu, Jin Xu, Zhibo Yang, Mingkun Yang, Jianxin Yang, An Yang, Bowen Yu, Fei Zhang, Hang Zhang, Xi Zhang, Bo Zheng, Humen Zhong, Jingren Zhou, Fan Zhou, Jing Zhou, Yuanzhi Zhu, and Ke Zhu. Qwen3-vl technical report, 2025a. URL https://arxiv.org/abs/2511.21631. 

- Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025b. 

- Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mahmoud Assran, and Nicolas Ballas. Revisiting feature prediction for learning visual representations from video. _arXiv preprint arXiv:2404.08471_ , 2024. 

- Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-languageaction flow model for general robot control, 2026. URL https://arxiv.org/abs/2410. 24164. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 

- Jun Cen, Siteng Huang, Yuqian Yuan, Kehan Li, Hangjie Yuan, Chaohui Yu, Yuming Jiang, Jiayan Guo, Xin Li, Hao Luo, et al. Rynnvla-002: A unified vision-language-action and world model. _arXiv preprint arXiv:2511.17502_ , 2025a. 

- Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025b. 

- Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 

- Kang Chen, Zhihao Liu, Tonghe Zhang, Zhen Guo, Si Xu, Hao Lin, Hongzhi Zang, Xiang Li, Quanlu Zhang, Zhaofei Yu, et al. _πRL_ : Online rl fine-tuning for flow-based vision-language-action models. _arXiv preprint arXiv:2510.25889_ , 2025. 

10 

Preprint 

- Lili Chen, Kevin Lu, Aravind Rajeswaran, Kimin Lee, Aditya Grover, Misha Laskin, Pieter Abbeel, Aravind Srinivas, and Igor Mordatch. Decision transformer: Reinforcement learning via sequence modeling. _Advances in neural information processing systems_ , 34:15084–15097, 2021. 

- Ronghan Chen, Yandan Yang, Zuojin Tang, Dongjie Huo, Tong Lin, Haoning Wu, Haoyun Liu, Yuzhi Chen, Lulu Zheng, Botai Yuan, et al. Abot-m0. 5: Unified mobility-and-manipulation world action model. _arXiv preprint arXiv:2607.00678_ , 2026. 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

- Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 

- Ankit Goyal, Hugo Hadfield, Xuning Yang, Valts Blukis, and Fabio Ramos. Vla-0: Building state-of-the-art vlas with zero modification. _arXiv preprint arXiv:2510.13054_ , 2025. 

- Yanjiang Guo, Yucheng Hu, Jianke Zhang, Yen-Jen Wang, Xiaoyu Chen, Chaochao Lu, and Jianyu Chen. Prediction with action: Visual policy learning via joint denoising process. _Advances in Neural Information Processing Systems_ , 37:112386–112410, 2024. 

- Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2019. 

- Danijar Hafner, Wilson Yan, and Timothy Lillicrap. Training agents inside of scalable world models. _arXiv preprint arXiv:2509.24527_ , 2025. 

- Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 

- Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, Yu-Chiang Frank Wang, and Fu-En Yang. Thinkact: Vision-language-action reasoning via reinforced visual latent planning. _arXiv preprint arXiv:2507.16815_ , 2025. 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5 : a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Joel Jang, Seonghyeon Ye, Zongyu Lin, Jiannan Xiang, Johan Bjorck, Yu Fang, Fengyuan Hu, Spencer Huang, Kaushil Kundalia, Yen-Chen Lin, et al. Dreamgen: Unlocking generalization in robot learning through video world models. _arXiv preprint arXiv:2505.12705_ , 2025. 

- Yuming Jiang, Siteng Huang, Shengke Xue, Yaxi Zhao, Jun Cen, Sicong Leng, Kehan Li, Jiayan Guo, Kexiang Wang, Mingxiu Chen, et al. Rynnvla-001: Using human demonstrations to improve robot manipulation. _arXiv preprint arXiv:2509.15212_ , 2025. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Yann LeCun. A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. _Open Review_ , 62(1):1–62, 2022. 

- Jianxiong Li, Jinliang Zheng, Yinan Zheng, Liyuan Mao, Xiao Hu, Sijie Cheng, Haoyi Niu, Jihao Liu, Yu Liu, Jingjing Liu, et al. Decisionnce: Embodied multimodal representations via implicit preference learning. _arXiv preprint arXiv:2402.18137_ , 2024a. 

11 

Preprint 

- Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024b. 

- Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 

- Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 

- Dongxiu Liu, Haoyi Niu, Zhihao Wang, Jinliang Zheng, Yinan Zheng, Zhonghong Ou, Jianming Hu, Jianxiong Li, and Xianyuan Zhan. Efficient robotic policy learning via latent space backward planning. _arXiv preprint arXiv:2505.06861_ , 2025. 

- Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- Yecheng Jason Ma, Shagun Sodhani, Dinesh Jayaraman, Osbert Bastani, Vikash Kumar, and Amy Zhang. Vip: Towards universal visual reward and representation via value-implicit pre-training. _arXiv preprint arXiv:2210.00030_ , 2022. 

- Yecheng Jason Ma, Vikash Kumar, Amy Zhang, Osbert Bastani, and Dinesh Jayaraman. Liv: Language-image representations and rewards for robotic control. In _International Conference on Machine Learning_ , pp. 23301–23320. PMLR, 2023. 

- Lucas Maes, Quentin Le Lidec, Damien Scieur, Yann LeCun, and Randall Balestriero. Leworldmodel: Stable end-to-end joint-embedding predictive architecture from pixels. _arXiv preprint arXiv:2603.19312_ , 2026. 

- Reginald McLean, Evangelos Chatzaroulas, Luc McCutcheon, Frank Röder, Tianhe Yu, Zhanpeng He, K.R. Zentner, Ryan Julian, J K Terry, Isaac Woungang, Nariman Farsad, and Pablo Samuel Castro. Meta-world+: An improved, standardized, RL benchmark. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ , 2025. URL https://openreview.net/forum?id=1de3azE606. 

- Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. _arXiv preprint arXiv:2203.12601_ , 2022. 

- Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-languageaction model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Younggyo Seo, Danijar Hafner, Hao Liu, Fangchen Liu, Stephen James, Kimin Lee, and Pieter Abbeel. Masked world models for visual control. In _Conference on Robot Learning_ , pp. 1332–1344. PMLR, 2023. 

- Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A visionlanguage-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- Zuojin Tang, Xiaoyu Chen, Yongqiang Li, and Jianyu Chen. Efficient and generalized end-to-end autonomous driving system with latent deep reinforcement learning and demonstrations. In _Joint European Conference on Machine Learning and Knowledge Discovery in Databases_ , pp. 179–197. Springer, 2025a. 

12 

Preprint 

- Zuojin Tang, Bin Hu, Chenyang Zhao, De Ma, Gang Pan, and Bin Liu. Vlascd: A visual language action model for simultaneous chatting and decision making. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , pp. 9223–9243, 2025b. 

- Zuojin Tang, Haoyun Liu, Xinyuan Chang, Changjie Wu, Dongjie Huo, Yandan Yang, Bin Liu, Zhejia Cai, Feng Xiong, Mu Xu, et al. Alam: Algebraically consistent latent action model for vision-language-action models. _arXiv preprint arXiv:2605.10819_ , 2026a. 

- Zuojin Tang, Feifan Luo, Haoyun Liu, Botai Yuan, Dekang Qi, Ronghan Chen, Yandan Yang, Tong Lin, Xinyuan Chang, Mu Xu, et al. Dlam: Distributional latent actions with temporal constraints. _arXiv preprint arXiv:2607.27138_ , 2026b. 

- Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 

- Junjin Xiao, Yandan Yang, Xinyuan Chang, Ronghan Chen, Feng Xiong, Mu Xu, Wei-Shi Zheng, and Qing Zhang. World-env: Leveraging world model as a virtual environment for vla post-training. _arXiv preprint arXiv:2509.24948_ , 2025. 

- Amber Xie, Oleh Rybkin, Dorsa Sadigh, and Chelsea Finn. Latent diffusion planning for imitation learning. _arXiv preprint arXiv:2504.16925_ , 2025. 

- Angen Ye, Zeyu Zhang, Boyuan Wang, Xiaofeng Wang, Dapeng Zhang, and Zheng Zhu. Vla-r1: Enhancing reasoning in vision-language-action models. _arXiv preprint arXiv:2510.01623_ , 2025. 

- Shuang Zeng, Dekang Qi, Xinyuan Chang, Feng Xiong, Shichao Xie, Xiaolong Wu, Shiyi Liang, Mu Xu, and Xing Wei. Janusvln: Decoupling semantics and spatiality with dual implicit memory for vision-language navigation. _arXiv preprint arXiv:2509.22548_ , 2025. 

- Jianke Zhang, Yanjiang Guo, Yucheng Hu, Xiaoyu Chen, Xiang Zhu, and Jianyu Chen. Up-vla: A unified understanding and prediction model for embodied agent. _arXiv preprint arXiv:2501.18867_ , 2025a. 

- Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, Fan Lu, He Wang, et al. Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge. _arXiv preprint arXiv:2507.04447_ , 2025b. 

- Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025. 

- Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 

- Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, et al. X-vla: Soft-prompted transformer as scalable crossembodiment vision-language-action model. _arXiv preprint arXiv:2510.10274_ , 2025. 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

13 

Preprint 

## A METAWORLD MT50 DIFFICULTY TIERS 

Following Seo et al. (2023), we divide the 50 MetaWorld MT50 tasks into four tiers by manipulation difficulty (Tab. 11). We use this partition for every tier-level result in the main text. The checkpoint sweep in Tab. 5 uses camera _x_ = 0 _._ 75 for all three token configurations. 

Table 11: MetaWorld MT50 task-difficulty partition used in our evaluation, following Seo et al. (2023). 

|**Difficulty**|**Tasks**|
|---|---|
|Easy (28)|button-press,<br>button-press-topdown,<br>button-press-topdown-wall,<br>button-press-wall,<br>coffee-button,<br>dial-turn,<br>door-close,<br>door-lock,<br>door-open,<br>door-unlock,<br>drawer-close,<br>drawer-open,<br>faucet-close, faucet-open, handle-press, handle-press-side,<br>handle-pull,<br>handle-pull-side,<br>lever-pull,<br>plate-slide,<br>plate-slide-back, plate-slide-back-side, plate-slide-side,<br>reach,<br>reach-wall,<br>window-close,<br>window-open,<br>peg-unplug-side|
|Medium (11)|basketball,bin-picking,box-close,coffee-pull,coffee-push,<br>hammer,peg-insert-side,push-wall,soccer,sweep,sweep-into|
|Hard (6)|assembly, hand-insert, pick-out-of-hole, pick-place, push,<br>push-back|
|Very Hard (5)|shelf-place,<br>disassemble,<br>stick-pull,<br>stick-push,<br>pick-place-wall|


## B SENSITIVITY TO THE FUSION TEMPERATURE 

We vary the pooling temperature _τp_ used for token scoring and branch fusion (Sec. 3.1). Among the three tested values, _τp_ =0 _._ 1 gives the highest average LIBERO success (Tab. 12). We therefore use it in the main experiments. 

Table 12: LIBERO success rates (%) for different pooling temperatures _τp_ . 

|_τp_|Spatial|Object|Goal|Long|Avg%|
|---|---|---|---|---|---|
|1.0|96.6|**97.8**|89.2|77.4|90.3|
|0.5|**97.4**|97.2|87.0|78.6|90.1|
|0.1|96.6|96.8|**94.6**|**85.0**|**93.3**|


## C FLOW-MATCHING DISTANCE METRIC 

We compare _L_ 1 and _L_ 2 distances for velocity regression in the action and latent branches, holding all other settings fixed (Tab. 13). The _L_ 1 _/L_ 1 configuration gives the highest average success among the three variants. We use it in the main experiments as an empirical velocity-regression choice; it does not inherit the conditional-mean guarantee associated with squared-error flow matching. 

Table 13: LIBERO success rates (%) for different distance metrics in the action and latent flowmatching losses. Training and inference both use _H_ =5. 

|Distance (Action / Latent)|Spatial|Object|Goal|Long|Avg%|
|---|---|---|---|---|---|
|_L_2/_L_2|94.8|94.6|87.0|74.2|87.7|
|_L_1/_L_2|96.4|**98.0**|88.2|78.2|90.2|
|_L_1/_L_1|**96.6**|96.8|**94.6**|**85.0**|**93.3**|


14 

Preprint 

## D LIBERO INFERENCE-TIME CONFIGURATION 

We use one checkpoint across all four LIBERO suites and select the inference action horizon and replan step on a held-out validation subset. Tab. 14 lists the fixed configurations used for evaluation. We also sweep these two settings on LIBERO-Long with the same checkpoint (Tab. 15). The gray row is the reference configuration of the same checkpoint, and the blue row is the highest-scoring setting in the sweep. The 20 _/_ 16 setting already exceeds the 92 _._ 4% result of _π_ 0 _._ 5, while 20 _/_ 20 is the longest inference horizon. Success ranges from 93 _._ 4% to 95 _._ 6% across the tested grid, while the representation stays fixed at one token per view and frame. For each suite, the selected pair is fixed for all evaluation rollouts and is not adapted per episode. 

Table 14: Inference-time configuration of OneWM-VLA on LIBERO. All suites use the checkpoint trained with an action horizon of 20; the inference horizon and replan step are selected per suite from a small validation grid. 

|**Suite**|**Inference horizon**|**Replan step**|**Avg. Success (%)**|
|---|---|---|---|
|Spatial|14|10|98.2|
|Object|14|10|99.6|
|Goal|18|7|99.0|
|Long|18|12|95.6|


## E LATENT-LOSS ABLATION ON METAWORLD MT50 

Table 16 compares the full OneWM-VLA model and its architecture-matched no-latent-loss control after 30k training steps, with _H_ = 20 at training and inference. Both use the same camera settings and evaluation protocol from Sec. 4.1. The control retains the latent tokens, projections, attention mask, and action objective; only the latent-loss weight is set to zero. The full model reaches 58 _._ 09% average success, compared with 21 _._ 64% for the control, a difference of 36 _._ 45 percentage points. 

## F REPRESENTATION-DIAGNOSTIC PROTOCOL 

Table 17 reports the target-spectrum and matching diagnostics. Both effective ranks are computed from the covariance of future-frame target vectors. 

**Checkpoints and samples.** We evaluate the full one-token model and its architecture-matched no-latent-loss control, both trained with _H_ = 5 for 30k steps. We use valid base-view records from 49 MetaWorld tasks and 245 episodes, yielding 1 _,_ 960 contexts. Five future steps per context produce _Mz_ =9 _,_ 800 target vectors. Both models use the same records and covariance calculation. 

**Spectral metrics.** Let _Z_<sup>�</sup> _∈_ R<sup>_Mz×D_</sup> contain the centered target vectors. We compute 


where _{λj}_ are the eigenvalues of _Cz_ . Zero covariance corresponds to a constant representation; for nonzero covariance, both effective ranks approach one as the variance concentrates in a single direction. 

**Matching diagnostics.** Queries are the generated 2048-D base-view latents for the five consecutive future frames _t_ + 1 _, . . . , t_ + 5, jointly sampled with actions conditioned on the current image, robot state, and language instruction under a common Gaussian initialization. For R@1, we subtract the corresponding global or within-task target mean from both queries and pooled future-frame targets, apply _ℓ_ 2 normalization, and rank targets at the same future offset by cosine similarity. The 

15 

Preprint 

Table 15: LIBERO-Long success rates (%) across inference action horizons and replan steps using a common checkpoint trained with an action horizon of 20. 

|Train/Infer.|Replan|Suffix tokens|Avg. Success (%)|
|---|---|---|---|
|20/15 (baseline)|10|45|93.4|
|20/16|10|48|94.0|
|20/18|10|54|94.8|
|20/18|11|54|95.4|
|20/18|12|54|**95.6**|
|20/20|10|60|94.0|


Table 16: Latent-loss ablation on MetaWorld MT50 ( _H_ = 20, 30k training steps). ∆full is the percentage-point difference from the full model. 

|**Method**|**Easy**|**Med.**|**Hard**|**V-Hard**|**Avg%**|∆full|
|---|---|---|---|---|---|---|
|**OneWM-VLA**|**79.64**|**42.73**|**60.00**|**50.00**|**58.09**|–|
|No latent loss|45.36|14.55|6.67|20.00|21.64|_−_36_._45|


Table 17: Representation diagnostics for the full one-token model and its architecture-matched no-latent-loss control, both trained with _H_ = 5 for 30k steps. The last row reports the separate architecture-matched policy evaluation at _H_ = 20 after 30k training steps. 

|**Diagnostic**|**Full one-token, 30k**|**No latent loss, 30k**|
|---|---|---|
|Target entropy effective rank|**21.42**|1.83|
|Covariance participation rank|**8.88**|1.31|
|Temporal discrimination|**77.09%**|50.04%|
|Cross-task discrimination|**73.52%**|49.18%|
|Global R@1|**0.510%**|0.051%|
|Global chance|0.051%|0.051%|
|Within-task R@1|**7.53%**|2.43%|
|Within-task chance|2.50%|2.50%|
|Policy avg. success (_H_ = 20)|**58.09%**|21.64%|


candidate sets contain 1 _,_ 960 global targets or 40 same-task targets, giving chance levels of 0 _._ 051% and 2 _._ 50%, respectively. Pairwise discrimination measures how often the matched target has a lower target-variance-normalized MSE than a negative, with a 50% chance level. Temporal negatives are constructed by cyclically shifting the eight anchors within each episode by four anchor positions; cross-task negatives are constructed by rotating task identities while preserving the episode slot, anchor slot, and future offset. 

**Interpretation.** The full model has target variance distributed across multiple directions, while the no-loss control is close to rank one. The separate _H_ = 20 policy evaluation at 30k also favors the full model by 36 _._ 45 percentage points (Tab. 16). The spectral measurements describe representation variation, while the policy evaluation measures the effect of removing the latent loss on task success. 

## G FEATURE-SPACE SEPARATION ANALYSIS 

**Features.** We extract visual features only, without language or action tokens. Before pooling, each sample contains the 256 visual tokens produced by the PaliGemma encoder. We average these tokens to obtain one feature vector per sample, so the reference is mean-pooled encoder features rather than the full patch sequence. After pooling, each sample is represented directly by the single output token of Adaptive Attention Pooling. This construction gives one full-dimensional feature vector per sample in both settings. 

16 

Preprint 

**Sampling.** We use 24 successful trajectories from each of the 10 LIBERO-Long tasks. One frame is extracted from each trajectory at the same relative time, yielding 240 samples in total. The same samples are used before and after pooling. 

**Fisher ratio.** Let _Ic_ contain the samples from task _c_ , let _Mc_ = _|Ic|_ , and let **_µ_** _c_ and **_µ_** denote the task and global feature means. We compute task separation in the original feature space as 


where _SB_ and _SW_ are the between-task and within-task scatter matrices. The metric is computed from the full feature vectors rather than a low-dimensional projection. 

Because the two representations have different feature scales, we normalize both scatter traces by tr( _SW_ ) within each setting when reporting Tab. 10. This sets the normalized within-task trace to one and leaves the Fisher ratio unchanged. The resulting comparison measures the relative change in task separation, rather than differences in raw feature magnitude. 

17 

