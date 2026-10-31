---
title: "TAPDreamer: Transferable Adversarial Patches for World Action Models"
date: "2026-10-05"
authors: "Xuanyu Lu; Fengqing Jiang; Kaiyuan Zheng; Yichen Feng; Yaorui Ding; Yuetai Li"
url: https://arxiv.org/abs/2610.06814
pdf: https://arxiv.org/pdf/2610.06814
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.06814)** / [論文ページ](https://arxiv.org/abs/2610.06814)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



# **TAPDreamer: Transferable Adversarial Patches for World Action Models** 

**Xuanyu Lu**<sup>1</sup><sup>_†_</sup> **Fengqing Jiang**<sup>1</sup><sup>_†‡_</sup> **Kaiyuan Zheng**<sup>1</sup><sup>_†_</sup> **Yichen Feng**<sup>1</sup> **Yaorui Ding**<sup>1</sup> **Yuetai Li**<sup>1</sup> **Zhen Xiang**<sup>2</sup> **Bhaskar Ramasubramanian**<sup>1</sup><sup>_,_3</sup> **Basel Alomair**<sup>1</sup><sup>_,_4</sup><sup>_,_5</sup> **Luyao Niu**<sup>1</sup> **Radha Poovendran**<sup>1</sup> 1University of Washington 2University of Georgia 3Western Washington University 4King Abdulaziz City for Science and Technology 5HUMAIN _†_ Equal Contribution _‡_ Project Lead `tapdreamer.github.io` 

## **Abstract** 

**World models learn to predict how their environment will evolve, making them an important foundation for general-purpose robotic control. Yet World Action Models (WAMs) rely on camera inputs, and manipulating those inputs can corrupt the visual representations that underpin their tasks and action policies. Existing attacks on these models optimize against actions or predicted futures and require access to victim outputs or generation modules. We propose** **`TAPDreamer` , a transferable fixed local patch whose pixel optimization uses only a public visual encoder and requires no target-policy queries. Its design addresses two requirements: a local modification should affect representations beyond its footprint, and the resulting disturbance should persist across observations. We optimize a fixed local patch on six frames from one source task by maximizing the mean L1 distance between clean and patched encoder outputs over all latent positions and channels. Mechanism analysis reveals that interactions between patch-induced changes in attention weights and value vectors broadcast a nearly identical representation shift beyond the patch footprint, while a shared perturbation response persists across task observations despite differences in clean latents. In closed-loop evaluation, one frozen patch per benchmark, covering about 6.5% of the input, reduces FastWAM’s success rate from 97.65% to 0.00% across 40 LIBERO tasks and from 90.86% to 0.00% across 50 RoboTwin tasks; matched random patches retain 81.45% and 79.20% success. The same patches reduce success to 1.45% and 1.00% on two DreamWAM configurations and to 10.60% on Motus. Behavioral analysis connects these representation shifts to grasping failures and separates rapid command recovery after patch removal from persistent physical consequences. These results show that protecting downstream action generation alone is insufficient: WAM defenses must also secure shared visual encoders against persistent local perturbations.** 

## **1. Introduction** 

World Action Models (WAMs) are emerging as a powerful foundation for general-purpose robotic control. Rather than predicting actions from the current observation alone, a WAM learns how the visual world evolves together with the robot’s actions. This world-modeling objective captures objects, spatial relationships, and motion, and can support action generation either through explicit future imagination (Du et al., 2023; Zhou et al., 2024) or through representations learned during video prediction (Yuan et al., 2026b). By unifying visual prediction and control, WAMs promise policies that can reason about the consequences of their actions and replan as the environment changes (Zhu et al., 2025; Ye et al., 2026). 

This coupling, however, also creates a security risk. Current WAM pipelines implicitly trust the visual representation on which world prediction and action generation are built. This assumption is fragile. Cameras 

TAPDreamer: Transferable Adversarial Patches for World Action Models 


Figure 1: `TAPDreamer` constructs a patch using a public visual encoder and observations from one source task, then freezes it for deployment across tasks and WAMs within each benchmark. Examples compare clean and patched execution on drawer opening with FastWAM, pot placement with Motus, and bowl placement with DreamWAM. 

expose a direct, externally accessible input channel. Moreover, visual encoders are often reused across tasks and models, making the exposed channel transferable among tasks. A perturbation that corrupts this shared interface can therefore bypass model-specific action heads. If the channel remains exposed, a perturbation can be injected consistently. In this paper, we investigate whether an attacker can exploit this vulnerability and launch attacks against WAMs that transfer to unseen tasks and models. 

We propose `TAPDreamer` (illustrated in Figure 1), a _transferable attack_ that applies a patch on visual inputs to WAMs. `TAPDreamer` maximizes the displacement of the final latent produced by visual encoder. The search uses a few demonstration frames from a single source task. Once the patch is found, the patch pixels, area, and position are frozen and the same artifact is deployed unchanged throughout each episode and across target tasks and models. Throughout the attack, `TAPDreamer` does not require action labels, task rewards, simulator, victim-model weights, or policy outputs, making `TAPDreamer` simple and inexpensive to initiate. 

We evaluate `TAPDreamer` on 40 LIBERO tasks and all 50 RoboTwin tasks. `TAPDreamer` consistently outperforms attack baselines. On FastWAM, a single frozen patch covering approximately 6 _._ 5% of the input reduces task success from 97 _._ 65% to 0 _._ 00% on LIBERO and from 90 _._ 86% to 0 _._ 00% on RoboTwin. Random patches retain 81 _._ 45% and 79 _._ 20% success, respectively. The same frozen patches also transfer across WAM architectures without retraining or target-model queries: success falls from 84 _._ 55% and 86 _._ 10% with matched random patches to 1 _._ 45% and 1 _._ 00% on DreamWAM-uncond and DreamWAM-joint, and from 82 _._ 40% to 10 _._ 60% on Motus. We further validate `TAPDreamer` in real-world deployment on an SO-101 robot, with representative FastWAM executions shown in Figure 2. We also trace how a fixed patch causes failure during closed-loop control. Our results show that changing a small set of pixels distorts visual features across the scene, including those used to select actions, and thus leads to reduced task success rate. 

2 

TAPDreamer: Transferable Adversarial Patches for World Action Models 


Figure 2: Real-world FastWAM executions on SO-101 for “Pick up the banana and place it in the bowl.” Rows show clean execution, a same-size white patch, and TAPDreamer at two positions. 

## **2. World Action Model, Threat Model, and** **`TAPDreamer`** 

### **2.1. World Action Model** 

Let _𝑠𝑡_ denote the robot and environment state at step _𝑡_ , _𝑜𝑡_ the camera observations, _𝑞𝑡_ the robot’s proprioceptive state, _ℓ_ the task instruction, and _ℋ𝑡_ the available history. For a world model _𝑚_ , image preprocessing _𝐺𝑚_ produces the visual input _𝑥𝑡_ = _𝐺𝑚_ ( _𝑜𝑡_ ), and the visual encoder produces _𝑍𝑡_ = _𝐸_ ( _𝑥𝑡_ ). The downstream model constructs a context _𝐶𝑡_ = _𝐹𝜃_ ( _𝑍𝑡, ℓ, 𝑞𝑡, ℋ𝑡_ ) _,_ where _𝜃_ denotes the learnable parameters of the corresponding module. 

For a WAM that predicts future visual latents before generating actions, we denote visual predictions and generated action chunks as 


where _𝐾𝑣_ and _𝐾𝑎_ are the visual prediction and action horizons. Here, _𝑊𝜃_ and _𝐴𝜃_ denote conditional distributions over future latents and action chunks. During closed-loop execution, the robot executes the first _𝐾𝑒_ actions of each chunk and receives new observations: 


where 1 _≤ 𝐾𝑒 ≤ 𝐾𝑎_ , _ℱ_ is the environment transition, and _𝑂_ is the observation function. The WAM then encodes the new observations and generates the next chunk. A visual perturbation can therefore affect both the current action and subsequent observations through execution-induced state changes. 

### **2.2. Threat Model** 

**Attacker’s objective.** We consider an attacker who aims to reduce the task success rate of a WAM-controlled robot by modifying a small region of its visual input. This is an untargeted, test-time attack. 

3 

TAPDreamer: Transferable Adversarial Patches for World Action Models 

**Attacker’s knowledge and access.** The attacker has white-box access to a publicly released visual encoder, including its weights and gradients, and a small set of public demonstration images from one source task. We assume that the attacker knows the relevant visual preprocessing, including image normalization and camera-view composition. Patch optimization requires only the WAM’s encoder and a small set of demonstration frames from a single source task. The attacker does not require access to the downstream world model or action decoder or their gradients, action labels, or task rewards for pixel optimization. 

**Attacker’s capabilities.** The attacker can replace pixels within a fixed local region of the visual input before encoding. Let _𝑀_ be a fixed binary mask and _𝑝_ the patch. The attacked observation is 


where _⊙_ represents elementwise multiplication. The attacker chooses the patch content. At deployment, the patch content, position, and area remain unchanged. The same patch is reused across target tasks and models within each benchmark. The attack does not manipulate pixels outside the mask, language instructions, proprioceptive inputs, or policy parameters. The attacker cannot directly set the robot’s actions or the environment state. 

### **2.3. Attack Design and Implementation** 

**Design rationale.** The attack exploits the reuse of public visual encoders across WAMs with different downstream control architectures. The encoder output therefore provides an attack objective independent of a particular action interface. For local pixel changes to affect broader scene representations, they must exploit propagation pathways within the encoder. We maximize the difference between the encoder’s clean and patched representations over the entire latent output, including all spatial positions and channels. The same patch is optimized over multiple source observations. 

**Patch construction.** `TAPDreamer` samples _𝐽_ frames _{𝑥𝑗}_<sup>_𝐽_</sup> _𝑗_ =1<sup>from different demonstrations of a single source</sup> task, caches their clean latents, and optimizes 


Here, _𝑁𝑍_ is the total number of scalar elements in the final latent, and _𝒫_ local contains patches within the fixed mask that satisfy the valid pixel range. Algorithm 1 gives the construction procedure. Figure 3 illustrates the overall pipeline. 

**Algorithm 1** TAPDreamer Patch Optimization 

**Require:** Frozen encoder _𝐸_ , source images _{𝑥𝑗}_<sup>_𝐽_</sup> _𝑗_ =1<sup>, patch mask</sup><sup>_𝑀_, pixel range [</sup><sup>_𝑎, 𝑏_], iterations</sup><sup>_𝐾_, learning</sup> rate _𝜂_ **Ensure:** Optimized patch _𝑝_<sup>_⋆_</sup> 1: _𝑍𝑗_<sup>0</sup><sup>_←_StopGradient(</sup><sup>_𝐸_(</sup><sup>_𝑥𝑗_))</sup><sup>_,∀𝑗_</sup> 2: _𝑝_ 0 _∼𝒰_ ( _𝑎, 𝑏_ ); initialize Adam state _𝜃_ 0 3: **for** _𝑘 ←_ 0 to _𝐾 −_ 1 **do** 4: _𝑇𝑝𝑘_ ( _𝑥𝑗_ ) = (1 _− 𝑀_ ) _⊙ 𝑥𝑗_ + _𝑀 ⊙ 𝑝𝑘, ∀𝑗 ◁_ Eq. (3) _𝐽_ 1 5: _ℒ𝑘 ←_ ∑︁ _𝐸_ ( _𝑇𝑝𝑘_ ( _𝑥𝑗_ )) _− 𝑍𝑗_<sup>0</sup> 1 _𝐽𝑁𝑍 𝑗_ =1 6: ( _𝑝𝑘_ +1 _, 𝜃𝑘_ +1) _←_ Adam( _𝑝𝑘, −∇𝑝𝑘 ℒ𝑘, 𝜃𝑘_ ; _𝜂_ ) 7: **end for** 

8: **return** _𝑝𝐾_ 

4 

TAPDreamer: Transferable Adversarial Patches for World Action Models 


Figure 3: Overview of `TAPDreamer` . (a) Pixel updates maximize the latent displacement through a frozen public visual encoder. (b) The resulting patch is frozen and reused at each step across tasks and models within the <mark>same ben</mark> c <mark>hm</mark> ark. 

## **3.** **<mark>Experime</mark> nts** 

### **3.1. Experimental Setup** 

**Datasets and models.** We conduct closed-loop evaluation on LIBERO and RoboTwin (Liu et al., 2023; Chen et al., 2025). LIBERO contains four task categories (Spatial, Object, Goal, and Long-horizon) with 10 tasks each. RoboTwin contains 50 tasks. FastWAM is the default evaluation model. DreamWAM-uncond (DW-U), DreamWAM-joint (DW-J) (Yuan et al., 2026a), and Motus (Bi et al., 2026) are used for transfer evaluation within the same benchmark. Each model configuration retains its own action generation process and preprocessing. 

**Attack setup.** We run `TAPDreamer` using patches optimized on source tasks; cross-model transfer occurs within each benchmark. Patches are injected before encoding. On LIBERO, the external and wrist views form a 224 _×_ 448 canvas; the main patch occupies an 81 _×_ 81 region in the upper-left corner of the external view, covering 6.54% of the input. The corresponding coverage on RoboTwin is 6.59%. Patches remain visible throughout each trial in standard attack evaluations. Images used for optimization come from public LeRobot demonstrations. We filter episodes by source-task identifier, then select one frame from each of six episodes at temporal indices 5, 20, 40, 60, 15, and 35, respectively. When generating the patch, `TAPDreamer` sets _𝐽_ = 6 with 500 Adam gradient-ascent updates on patch pixels, using a learning rate of 0.02. Patch pixels are initialized uniformly within [ _−_ 1 _,_ 1]. After each update, they are projected back to this range, with support enforced by the fixed mask. 

**Real-world setup.** We additionally evaluate FastWAM and DreamWAM on an SO-101 robot for “Pick up the banana and place it in the bowl,” using 50 trials per model and condition and retaining the original patch size. The FastWAM patch is transferred to DreamWAM without modification or reoptimization. 

**Baselines.** We compare `TAPDreamer` with baselines to show its effectiveness. We evaluate the policy on unmodified observations to establish the **clean** baseline. For **random patch** , we replace the same image region with a random patch matched to the adversarial patch in position and area, to measure the effects of ordinary local occlusion and pixel replacement. Random patches are generated following a uniform distribution within admissible range of pixel values. Extra ablation of transferred VLA attack is deferred to Appendix A.2. 

5 

TAPDreamer: Transferable Adversarial Patches for World Action Models 

Table 1: Closed-loop FastWAM success rates (percent) on complete task sets. LIBERO and RoboTwin each use one fixed patch, optimized on `Spatial t6` and `pick diverse bottles` , respectively. Small subscripts report the signed success-rate difference from Clean, in percentage points. LIBERO Overall averages the four suites. 

|Setup|||LIBERO|||RoboTwin|
|---|---|---|---|---|---|---|
||Spatial|Object|Goal|Long-hor.|Overall||
|Clean|98.00_±_0_._00|99.60_±_0_._00|97.60_±_0_._00|95.40_±_0_._00|97.65_±_0_._00|90.86_±_0_._00|
|Random|85.60_−_12_._40|78.00_−_21_._60|90.00_−_7_._60|72.20_−_23_._20|81.45_−_16_._20|79.20_−_11_._66|
|`TAPDreamer`|0.00_−_98_._00|0.00_−_99_._60|0.00_−_97_._60|0.00_−_95_._40|0.00_−_97_._65|0.00_−_90_._86|


**Metrics.** We evaluate attack effectiveness using closed-loop task **success rate** (SR), defined as 


where _𝑁_ success is the number of successful trials and _𝑁_ trials is the total number of trials. A trial is successful if the robot completes the task according to the benchmark’s success criterion. Complete task sets contain both the source task and held-out tasks; cross-task transfer is evaluated on held-out tasks after freezing the patch. 

### **3.2. Experimental Results** 

**`TAPDreamer` reduces the success rate to zero on both benchmarks.** We evaluate FastWAM on all four LIBERO suites with 10 tasks each (4 _×_ 10 tasks), using 50 trials per task, and on all 50 RoboTwin tasks, using 100 trials per task. On LIBERO, FastWAM achieves 97.65% success with clean inputs, whereas the frozen `TAPDreamer` patch reduces performance to 0.00%. The same pattern holds on RoboTwin, where success decreases from 90.86% to 0.00%. Table 1 shows that success is 0.00% in all four LIBERO suites, covering different task configurations. 

Table 2: Frozen-patch transfer across models within each benchmark. LIBERO results use the first optimization initialization. Success rates are percentages; small subscripts report signed differences from Clean for the same model and suite, in percentage points. DW-U and DW-J denote DreamWAM-uncond and DreamWAM-joint. LIBERO Overall averages the four suites. 

|Victim|Suite|Clean|Random|`TAPDreamer`|
|---|---|---|---|---|
|**LIBERO**|||||
|DW-U|Spatial|96.20_±_0_._00|82.20_−_14_._00|0.00_−_96_._20|
|DW-U|Object|99.60_±_0_._00|96.00_−_3_._60|0.00_−_99_._60|
|DW-U|Goal|98.00_±_0_._00|90.00_−_8_._00|5.80_−_92_._20|
|DW-U|Long-horizon|96.20_±_0_._00|70.00_−_26_._20|0.00_−_96_._20|
|DW-U|Overall|97.50_±_0_._00|84.55_−_12_._95|1.45_−_96_._05|
|DW-J|Spatial|99.40_±_0_._00|84.20_−_15_._20|0.00_−_99_._40|
|DW-J|Object|100.00_±_0_._00|99.20_−_0_._80|0.00_−_100_._00|
|DW-J|Goal|98.00_±_0_._00|88.00_−_10_._00|4.00_−_94_._00|
|DW-J|Long-horizon|93.40_±_0_._00|73.00_−_20_._40|0.00_−_93_._40|
|DW-J|Overall|97.70_±_0_._00|86.10_−_11_._60|1.00_−_96_._70|
|**RoboTwin**|||||
|FastWAM|Overall|90.86_±_0_._00|79.20_−_11_._66|0.00_−_90_._86|
|Motus|Overall|86.62_±_0_._00|82.40_−_4_._22|10.60_−_76_._02|


6 

TAPDreamer: Transferable Adversarial Patches for World Action Models 

**`TAPDreamer` causes a much larger performance degradation than a matched random patch.** On LIBERO, the random patch retains an 81.45% success rate, compared with 0.00% for `TAPDreamer` . On RoboTwin, the corresponding success rates are 79.20% and 0.00%, respectively. Thus, the performance degradation caused by `TAPDreamer` cannot be attributed solely to obscuring the same image region; it depends on the optimized content of the `TAPDreamer` patch. 

**`TAPDreamer` transfers across downstream control architectures.** Keeping the patch fixed and changing the victim model reduces average success to 1.45% on DreamWAM-uncond, 1.00% on DreamWAM-joint, and 10.60% on Motus. The corresponding matched random patches retain 84.55%, 86.10%, and 82.40% success. Table 2 reports results by benchmark, model, and suite. Transfer uses no target-model feedback for reoptimization. 

DreamWAM-uncond does not read explicitly generated future frames to predict actions, yet it is still strongly affected. In these models, explicit test-time future-video generation is therefore not necessary for the attack. 

**Real-world results.** `TAPDreamer` reduces FastWAM’s success rate from 92% to 0% and DreamWAM’s from 80% to 20%; representative FastWAM executions are shown in Figure 2. 

We defer more experimental results along with ablation studies about patch variations to Appendix A. 

## **4. Mechanism and Behavioral Analysis** 

This section investigates how a local pixel change by `TAPDreamer` results in deviations in action execution. Figure 4 summarizes impacts on latents due to `TAPDreamer` . 

### **4.1. A local patch becomes a distributed latent shift** 

**Attention spreads the change introduced by** **`TAPDreamer` .** We compare clean and patched activations throughout the VAE encoder. Its bottleneck contains spatial self-attention on a 14 _×_ 28 grid. We call the projection of the patch region onto a feature grid the _patch footprint_ . Table 3 reports the fraction of squared magnitude of representation change outside this footprint. For `TAPDreamer` , it rises from less than 1% at the attention input to about 71% at its output and 79% in the final latent. A random patch of the same size 


Figure 4: Mechanism overview of `TAPDreamer` . Alocal patch-induced change spreads through bottleneck attention and propagates to the final latent. The changes across observations share a source-template component, with observation-specific residuals. 

7 

TAPDreamer: Transferable Adversarial Patches for World Action Models 

Table 3: Fraction of squared representation change outside the projected patch footprint: _‖_ ∆ _𝑋𝑂‖_<sup>2</sup> _𝐹_<sup>_/‖_∆</sup><sup>_𝑋‖_2</sup> _𝐹_<sup>,</sup> where ∆ _𝑋_ = _𝑋_<sup>_𝑝_</sup> _− 𝑋_ , _𝑋 ∈{𝑈, 𝐻, 𝑍}_ denotes attention input, attention output, and final latent, respectively, and _𝑂_ denotes positions outside the footprint at the corresponding layer. Values are medians over 48 states. 

||Attention input|Attention output|Final latent|
|---|---|---|---|
|Random|0.007|0.008|0.013|
|`TAPDreamer`|0.007|0.708|0.794|


leaves changes largely within the footprint. The attention layer helps the optimized local change reach distant positions. 

**Attention weights and values carry the change.** To identify what carries this change, write the clean attention output after residual addition as _𝐻_ = _𝑈_ + _𝐴𝑉𝑊𝑂_ , where _𝑈_ is the residual input, _𝐴_ the attention weights, _𝑉_ the value vectors, and _𝑊𝑂_ the output projection. Rows index spatial positions; for multiple heads, _𝐴𝑉_ denotes their concatenated outputs. Let _𝑋_<sup>_𝑝_</sup> denote the patched quantity and ∆ _𝑋_ = _𝑋_<sup>_𝑝_</sup> _− 𝑋_ , where _𝑋 ∈{𝐻, 𝑈, 𝑉, 𝐴}_ . We then have 


The terms capture changed values, changed attention weights, and their joint change, respectively. We observe that the joint change term ∆ _𝐴_ ∆ _𝑉_ is the largest measured component for `TAPDreamer` but is small for a random patch. This points to coordinated changes in weights and values, rather than greater attention to the patch alone. 

**Restoration tests the attention pathway.** In Figure 5(c), Full patch denotes the patched pass without intervention; Clean weights and Clean values restore _𝐴_ and _𝑉_ , respectively, to their clean counterparts. Restoring the attention branch, weights, or values to their clean counterparts while retaining the patched residual branch substantially reduces the latent and action changes. Perturbations outside the patch footprint are strongly suppressed, while the remaining perturbations are concentrated near the patch. The same interventions have little effect on the random patch. Figure 5 shows the spatial changes and their magnitude outside the footprint; Table 7 in Appendix B.1 reports the retained effects after each intervention. 

**The distributed shift is coherent.** The bottleneck positions outside the footprint receive change vectors with nearly identical directions and magnitudes. Let _𝑂_ be these positions and ∆ _𝐻𝑂_ their matrix of output changes. Define _𝑔_ = _|𝑂|_<sup>_−_1</sup> (∆ _𝐻𝑂_ )<sup>_⊤_</sup> **1** as the mean change vector and _𝑅𝐻_ = ∆ _𝐻𝑂 −_ **1** _𝑔_<sup>_⊤_</sup> as the position-specific residual. Then 


Here **1** _∈_ R<sup>_|𝑂|_</sup> is an all-ones vector. The inequality follows from the reverse triangle inequality: when the residual is small, the common change contributes across all _|𝑂|_ positions with aggregate magnitude proportional to ~~√~~ _|𝑂|_ . These results show how a small patch produces a coherent displacement over the full representation. 

### **4.2. The latent shift repeats across observations** 

**Measuring transfer of the response.** Section 4.1 explains how the patch reaches distant positions within one observation. Transfer across tasks also requires a similar response when the scene changes. For a fixed patch _𝑝_ , let ∆ _𝑍_ ( _𝑥, 𝑝_ ) = _𝐸_ ( _𝑇𝑝_ ( _𝑥_ )) _− 𝐸_ ( _𝑥_ ) be its final-latent change on observation _𝑥_ . We average the patchinduced latent changes in observations from 12 source-task states to form a fixed template ∆ _𝑍_ src( _𝑝_ ), then compare it with changes in observations from 36 held-out states. The statistics in Table 4 use latent positions 

8 

TAPDreamer: Transferable Adversarial Patches for World Action Models 


Figure 5: Spatial spread and attention restoration. (a,b) Per-position final-latent L2 changes with a shared color scale; dashed boxes mark the patch footprint. (c) Mean L2 change outside the footprint over 48 states, with 95% confidence intervals. The dotted line denotes the random patch. 

Table 4: Consistency of final-latent changes outside the patch footprint. CV denotes coefficient of variation. 

|Metric|`TAPDreamer`|Random|
|---|---|---|
|Cross-task cosine similarity|0.971|0.603|
|Magnitude CV|0.056|0.071|
|Template cosine similarity|0.981|0.716|
|Relative L1 residual|0.206|0.809|
|L1 bound ratio|0.833|0.069|


outside the projected patch footprint. Cross-task cosine similarity compares full final-latent displacement fields between tasks, while template cosine similarity compares each held-out field with the source template. Cosine similarities, relative residuals, and lower-bound ratios are reported as medians. Magnitude CV is the standard deviation of change magnitudes divided by their mean, computed over all 48 states. 

**One source template describes held-out scenes.** The source template has a median cosine similarity of 0.981 with held-out changes, and the median residual ∆ _𝑍𝑖 −_ ∆ _𝑍_ src 1<sup>_/ ‖_∆</sup><sup>_𝑍𝑖‖_1is 0.206 in Table 4, where</sup><sup>_𝑖_is</sup> the target held-out state. Clean representations from the same observations have a cross-task cosine similarity of 0.371, so the shared direction is specific to the patch-induced change. The random patch produces much weaker template agreement. Figure 6 shows that cross-observation alignment emerges early, while subsequent optimization mainly increases displacement on both source and held-out observations. Appendix B.2 reports the full trajectories, including the effective rank and frozen-template L1 bound during optimization. 

**The shared shift retains its magnitude.** `TAPDreamer` maximizes L1 displacement, so the size of the common response matters alongside its direction. For a held-out state _𝑖_ , write its change as the source template plus a residual _𝑒𝑖_ . The reverse triangle inequality gives 


Using the measured residual for each held-out state, we compute the ratio of the lower bound in Equation (8) to the observed L1 displacement. The median ratio is 0.833 (range 0.732–0.918). Thus, even after subtracting the observation-specific residual norm, the fixed source template yields a lower bound that retains much of the measured displacement. 

**Local features reproduce the broadcast.** About 95.3% of final-latent change energy outside the footprint lies in a shared spatial component. The direction of this component has a cross-task cosine similarity of about 0.997. To probe where this consistency begins, we replace keys and values within the patch footprint with source-task templates, retain a new image’s clean context, and recompute attention. This K/V template analysis also includes a second patch initialization. The resulting broadcast closely matches the actual patched pass 

9 

TAPDreamer: Transferable Adversarial Patches for World Action Models 


Figure 6: Optimization trajectories for three initializations: (a) latent L1 displacement and (b) source-template agreement. Dotted lines denote random-patch results. 

in direction and magnitude. Stable local keys and values thus help reproduce the distributed shift across observations. 

**Additional analysis.** We analyze how the latent shift changes actions in Appendix B.3. 

## **5. Related Work** 

**Transferable and localized adversarial attacks.** Adversarial perturbations can alter neural-network predictions (Goodfellow et al., 2015). Cross-model transfer has been studied using ensembles (Liu et al., 2017), momentum (Dong et al., 2018), and input diversity (Xie et al., 2019). Universal perturbations reuse a single perturbation across images (Moosavi-Dezfooli et al., 2017), with data-independent constructions such as Fast Feature Fool (Mopuri et al., 2017). Feature-level objectives have been explored through feature disruption (Ganeshan et al., 2019), feature importance (Wang et al., 2021), and neuron attribution (Zhang et al., 2022). Localized attacks include LaVAN (Karmon et al., 2018) and attention-aware Patch-Fool (Fu et al., 2022); physical attacks include robust object perturbations (Eykholt et al., 2018) and camera stickers (Li et al., 2019). PhotoGuard also studies encoder-level attacks on diffusion-based image editing (Salman et al., 2023). In sequential decision-making, adversarial policies can disrupt reinforcement-learning agents through an opponent’s behavior (Gleave et al., 2020). 

**Attack on vision-language-action policies.** Vision-language-action (VLA) policies such as OpenVLA (Kim et al., 2025) and _𝜋_ 0 (Black et al., 2025) map visual and language inputs to robot actions. Action-based attacks on VLA policies optimize action differences, motion directions, target actions, or action freezing (Wang et al., 2025a,b; Yan et al., 2025). Their gradient-based objectives require access through the corresponding action generation interfaces. Representation-based methods attack image–text alignment, feature displacement, projection features, attention relationships, or visual proprioception (Xu et al., 2025; Lu et al., 2026; Zhang et al., 2025; Fu et al., 2026; Zhang et al., 2026). Clean–perturbed representation distances already appear in prior attacks; here, we study their effectiveness for fixed local attacks on a public generative visual encoder and the mechanism of transfer. In the WAM pathway studied here, image–text interaction occurs downstream of the public VAE, so the corresponding alignment and attention objectives fall outside the default encoder-only access. We therefore define the objective directly on the encoder output and evaluate its effects on control through closed-loop experiments and mechanism interventions. 

10 

TAPDreamer: Transferable Adversarial Patches for World Action Models 

**Adversarial threats to world models and world action models.** BadWorld (Shen et al., 2026) evaluates attacks on generated videos, without testing closed-loop robotic tasks. BadWAM (Li et al., 2026) perturbs the full visual input through online target-model queries at each replanning step. Attacking the Trusted Imagination (Chen et al., 2026) optimizes observation perturbations using end-to-end gradients through the encoder and world model, corrupting future predictions used by downstream planning or safety checks. JailWAM (Liu et al., 2026) induces unsafe actions and requires attacker control over language instructions. Unlike these WAM threats, `TAPDreamer` achieves closed-loop attacks across tasks and WAM architectures with a fixed local patch optimized solely through a public visual encoder, without using target-policy action outputs or future predictions. 

## **6. Conclusion** 

`TAPDreamer` optimizes a fixed local patch using only a public visual encoder and six observations from one task, yet produces strong closed-loop interference across two complete benchmarks and different downstream action architectures. Mechanism analysis reveals that interactions between attention-weight and value changes broadcast local interference to distant representations, while optimized perturbation responses remain highly consistent across task observations. Behavioral analysis connects this representation vulnerability to grasping and pose interference, and separates the immediate effects of sustained visual input from state consequences accumulated through execution. These results show that WAM robustness must cover the full path from local visual input through representation, generation, and control. 

### **Ethics statement** 

This study aims to identify vulnerabilities of World Action Models to local visual perturbations to inform robot safety evaluation and defense research. All experiments were conducted in the LIBERO and RoboTwin simulation environments, with attacks implemented by modifying model input images. We recognize that such methods could be misused to disrupt normal robot operation and emphasize that their use should be restricted to authorized security testing and research. Our mechanism analysis suggests potential defenses that attenuate keys and values from suspicious image regions or train the encoder to preserve representations outside locally perturbed regions. These interventions target the attention-mediated spread of the patch-induced shift; their effectiveness against adaptive attacks and their impact on clean-task performance remain to be evaluated. 

## **References** 

- Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, and Jun Zhu. Motus: A Unified Latent Action World Model. In _CVPR_ , pp. 35101–35113, 2026. URL `https: //arxiv.org/abs/2512.13030` . 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _𝜋_ 0: A Vision-Language-Action Flow Model for General Robot Control. In _Robotics: Science and Systems (RSS)_ , 2025. URL `https://arxiv.org/abs/2410.24164` . 

- Linghan Chen, Kaiyan Ji, and Minyu Guo. Attacking the Trusted Imagination: Oracle-Level Integrity Attacks on Imagine-then-Act World Models. arXiv preprint arXiv:2606.22966, 2026. URL `https://arxiv.org/abs/ 2606.22966` . 

11 

TAPDreamer: Transferable Adversarial Patches for World Action Models 

- Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, Weiliang Deng, Yubin Guo, Tian Nian, Xuanbing Xie, Qiangyu Chen, Kailun Su, Tianling Xu, Guodong Liu, Mengkang Hu, Huan-ang Gao, Kaixuan Wang, Zhixuan Liang, Yusen Qin, Xiaokang Yang, Ping Luo, and Yao Mu. RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation. arXiv preprint arXiv:2506.18088, 2025. URL `https://arxiv.org/abs/2506.18088` . 

- Yinpeng Dong, Fangzhou Liao, Tianyu Pang, Hang Su, Jun Zhu, Xiaolin Hu, and Jianguo Li. Boosting Adversarial Attacks with Momentum. In _CVPR_ , pp. 9185–9193, 2018. URL `https://arxiv.org/abs/1710.06081` . 

- Yilun Du, Mengjiao Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Joshua B. Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning Universal Policies via Text-Guided Video Generation. In _NeurIPS_ , 2023. URL `https://arxiv.org/abs/2302.00111` . 

- Kevin Eykholt, Ivan Evtimov, Earlence Fernandes, Bo Li, Amir Rahmati, Chaowei Xiao, Atul Prakash, Tadayoshi Kohno, and Dawn Song. Robust Physical-World Attacks on Deep Learning Visual Classification. In _CVPR_ , pp. 1625–1634, 2018. URL `https://arxiv.org/abs/1707.08945` . 

- Jiyuan Fu, Kaixun Jiang, Jingkai Jia, Zhaoyu Chen, Xueyao Chen, Lingyi Hong, Shuyong Gao, Chenzhi Tan, Dingkang Yang, and Wenqiang Zhang. VLA-Hijack: A Transferable Patch Attack against Vision-LanguageAction Models via Visual Proprioception Hijacking. arXiv preprint arXiv:2605.28083, 2026. URL `https: //arxiv.org/abs/2605.28083` . 

- Yonggan Fu, Shunyao Zhang, Shang Wu, Cheng Wan, and Yingyan Celine Lin. Patch-Fool: Are Vision Transformers Always Robust Against Adversarial Perturbations? In _ICLR_ , 2022. URL `https://arxiv.org/ abs/2203.08392` . 

- Aditya Ganeshan, B. S. Vivek, and R. Venkatesh Babu. FDA: Feature Disruptive Attack. In _ICCV_ , 2019. URL `https://arxiv.org/abs/1909.04385` . 

- Adam Gleave, Michael Dennis, Cody Wild, Neel Kant, Sergey Levine, and Stuart Russell. Adversarial Policies: Attacking Deep Reinforcement Learning. In _ICLR_ , 2020. URL `https://arxiv.org/abs/1905.10615` . 

- Ian J. Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining and Harnessing Adversarial Examples. In _ICLR_ , 2015. URL `https://arxiv.org/abs/1412.6572` . 

- Danny Karmon, Daniel Zoran, and Yoav Goldberg. LaVAN: Localized and Visible Adversarial Noise. In _ICML_ , volume 80 of _Proceedings of Machine Learning Research_ , pp. 2507–2515, 2018. URL `https://arxiv.org/ abs/1801.02608` . 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. OpenVLA: An Open-Source Vision-LanguageAction Model. In _Conference on Robot Learning (CoRL 2024)_ , volume 270 of _Proceedings of Machine Learning Research_ , pp. 2679–2713, 2025. URL `https://arxiv.org/abs/2406.09246` . 

- Juncheng Li, Frank Schmidt, and Zico Kolter. Adversarial Camera Stickers: A Physical Camera-Based Attack on Deep Learning Systems. In _ICML_ , volume 97 of _Proceedings of Machine Learning Research_ , pp. 3896–3904, 2019. URL `https://arxiv.org/abs/1904.00759` . 

- Qi Li, Xingyi Yang, and Xinchao Wang. BadWAM: When World-Action Models Dream Right but Act Wrong. arXiv preprint arXiv:2607.15207, 2026. URL `https://arxiv.org/abs/2607.15207` . 

12 

TAPDreamer: Transferable Adversarial Patches for World Action Models 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning. arXiv preprint arXiv:2306.03310, 2023. URL `https: //arxiv.org/abs/2306.03310` . 

- Hanqing Liu, Songping Wang, Jiahuan Long, Jiacheng Hou, Jialiang Sun, Chao Li, Yang Yang, Wei Peng, Xu Liu, Tingsong Jiang, Yao Mu, and Wen Yao. JailWAM: Jailbreaking World Action Models in Robot Control. arXiv preprint arXiv:2604.05498, 2026. URL `https://arxiv.org/abs/2604.05498` . 

- Yanpei Liu, Xinyun Chen, Chang Liu, and Dawn Song. Delving into Transferable Adversarial Examples and Black-box Attacks. In _ICLR_ , 2017. URL `https://arxiv.org/abs/1611.02770` . 

- Hui Lu, Yi Yu, Yiming Yang, Chenyu Yi, Qixin Zhang, Bingquan Shen, Alex C. Kot, and Xudong Jiang. When Robots Obey the Patch: Universal Transferable Patch Attacks on Vision-Language-Action Models. In _CVPR_ , 2026. URL `https://arxiv.org/abs/2511.21192` . arXiv:2511.21192. 

- Seyed-Mohsen Moosavi-Dezfooli, Alhussein Fawzi, Omar Fawzi, and Pascal Frossard. Universal Adversarial Perturbations. In _CVPR_ , 2017. URL `https://arxiv.org/abs/1610.08401` . 

- Konda Reddy Mopuri, Utsav Garg, and R. Venkatesh Babu. Fast Feature Fool: A Data Independent Approach to Universal Adversarial Perturbations. In _BMVC_ , 2017. URL `https://arxiv.org/abs/1707.05572` . 

- Hadi Salman, Alaa Khaddaj, Guillaume Leclerc, Andrew Ilyas, and Aleksander Madry. Raising the Cost of Malicious AI-Powered Image Editing. In _ICML_ , volume 202 of _Proceedings of Machine Learning Research_ , pp. 29894–29918, 2023. URL `https://arxiv.org/abs/2302.06588` . 

- Linghui Shen, Mingyue Cui, and Xingyi Yang. BadWorld: Adversarial Attacks on World Models. arXiv preprint arXiv:2606.16519, 2026. URL `https://arxiv.org/abs/2606.16519` . 

- Taowen Wang, Cheng Han, James Chenhao Liang, Wenhao Yang, Dongfang Liu, Luna Xinyu Zhang, Qifan Wang, Jiebo Luo, and Ruixiang Tang. Exploring the Adversarial Vulnerabilities of Vision-Language-Action Models in Robotics. In _ICCV_ , 2025a. URL `https://arxiv.org/abs/2411.13587` . arXiv:2411.13587. 

- Xin Wang, Jie Li, Zejia Weng, Yixu Wang, Yifeng Gao, Tianyu Pang, Chao Du, Yan Teng, Yingchun Wang, Zuxuan Wu, Xingjun Ma, and Yu-Gang Jiang. FreezeVLA: Action-Freezing Attacks against Vision-Language-Action Models. arXiv preprint arXiv:2509.19870, 2025b. URL `https://arxiv.org/abs/2509.19870` . 

- Zhibo Wang, Hengchang Guo, Zhifei Zhang, Wenxin Liu, Zhan Qin, and Kui Ren. Feature Importance-aware Transferable Adversarial Attacks. In _ICCV_ , 2021. URL `https://arxiv.org/abs/2107.14185` . 

- Cihang Xie, Zhishuai Zhang, Yuyin Zhou, Song Bai, Jianyu Wang, Zhou Ren, and Alan Yuille. Improving Transferability of Adversarial Examples with Input Diversity. In _CVPR_ , 2019. URL `https://arxiv.org/ abs/1803.06978` . 

- Haochuan Xu, Yun Sing Koh, Shuhuai Huang, Zirun Zhou, Di Wang, Jun Sakuma, and Jingfeng Zhang. Modelagnostic Adversarial Attack and Defense for Vision-Language-Action Models. arXiv preprint arXiv:2510.13237, 2025. URL `https://arxiv.org/abs/2510.13237` . 

- Yuping Yan, Yuhan Xie, Yixin Zhang, Lingjuan Lyu, Handing Wang, and Yaochu Jin. When Alignment Fails: Multimodal Adversarial Attacks on Vision-Language-Action Models. arXiv preprint arXiv:2511.16203, 2025. URL `https://arxiv.org/abs/2511.16203` . 

- Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, Ayaan Malik, Kyungmin Lee, William Liang, Nadun Ranawaka, Jiasheng Gu, Yinzhen Xu, Guanzhi Wang, Fengyuan Hu, Avnish Narayan, Johan Bjorck, Jing Wang, Gwanghyun Kim, Dantong Niu, Ruijie Zheng, Yuqi Xie, Jimmy Wu, Qi Wang, Ryan Julian, Danfei Xu, Yilun Du, Yevgen 

13 

TAPDreamer: Transferable Adversarial Patches for World Action Models 

Chebotar, Scott Reed, Jan Kautz, Yuke Zhu, Linxi Fan, and Joel Jang. World Action Models are Zero-shot Policies. arXiv preprint arXiv:2602.15922, 2026. URL `https://arxiv.org/abs/2602.15922` . 

- Shanglin Yuan, Weiheng Zhao, Xin Shi, Haoyi Jiang, Xianda Guo, Liu Liu, Wenyu Liu, Wei Sui, and Xinggang Wang. DreamWAM: Beyond RGB Future Prediction for World Action Models. arXiv preprint arXiv:2608.04996, 2026a. URL `https://arxiv.org/abs/2608.04996` . 

- Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-WAM: Do World Action Models Need Test-time Future Imagination? arXiv preprint arXiv:2603.16666, 2026b. URL `https://arxiv.org/abs/2603.16666` . 

- Jianping Zhang, Weibin Wu, Jen-tse Huang, Yizhan Huang, Wenxuan Wang, Yuxin Su, and Michael R. Lyu. Improving Adversarial Transferability via Neuron Attribution-Based Attacks. In _CVPR_ , 2022. URL `https://arxiv.org/abs/2204.00008` . 

- Jinquan Zhang, Dongfu Yin, Run Yang, Yufeng Yan, Zhen Tian, and F. Richard Yu. Structure-Aware Robust Fine-Tuning: Defending Vision-Language-Action Robots Against Physical Attention Hijacking. arXiv preprint arXiv:2608.03231, 2026. URL `https://arxiv.org/abs/2608.03231` . 

- Naifu Zhang, Wei Tao, Xi Xiao, Qianpu Sun, Yuxin Zheng, Wentao Mo, Peiqiang Wang, and Nan Zhang. Attention-Guided Patch-Wise Sparse Adversarial Attacks on Vision-Language-Action Models. arXiv preprint arXiv:2511.21663, 2025. URL `https://arxiv.org/abs/2511.21663` . 

- Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. RoboDreamer: Learning Compositional World Models for Robot Imagination. In _ICML_ , volume 235 of _Proceedings of Machine Learning Research_ , pp. 61885–61896, 2024. URL `https://arxiv.org/abs/2404.12377` . 

- Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified World Models: Coupling Video and Action Diffusion for Pretraining on Large Robotic Datasets. In _Robotics: Science and Systems (RSS)_ , 2025. URL `https://arxiv.org/abs/2504.02792` . 

## **A. Experimental Result and Ablation Studies** 

### **A.1. Patch area and position** 

We examine how patch area affects attack effectiveness and whether the attack depends on patch position. We conduct the patch-area and patch-position ablations on FastWAM across all 40 LIBERO tasks, using 50 trials per task and keeping the remaining settings consistent with the standard experimental configuration. 

As shown in Figure 7, increasing patch area from 3.35% to 3.96% sharply reduces success from 65.60% to 3.85%, whereas the matched random patch changes success only from 90.80% to 89.25%. The sharp success-rate drop under `TAPDreamer` , compared with the small change under matched random patches, shows that the effect depends on optimized patch content rather than increased occlusion alone. 

We also study the effect of patch position. We consider four positions in the external camera view: upper left (0,0), upper right (0,143), lower left (143, 0), lower right (143, 143). Coordinates are ( _𝑦_ 0 _, 𝑥_ 0) in pixels. We consider two settings: **reoptimized** patches are freshly optimized at the given position, and **moved** patches are copied from the patch optimized at the upper-left corner without update. 

Our results are presented in Table 5. Reoptimizing a patch at each of the four tested positions achieves 0.00% success, but moving the unchanged upper-left patch to the other three corners yields 93.50%–95.00% success, close to the corresponding random-patch results. Thus, effective patches can be optimized at different positions, but a patch optimized at one position does not transfer directly to another. 

14 

TAPDreamer: Transferable Adversarial Patches for World Action Models 


Figure 7: Ablation study of patch area. Random patches use the same area and placement as `TAPDreamer` . 

Table 5: Ablation study of patch position. Reoptimized patches are optimized at the given position; moved patches are copies of the unchanged upper-left patch. Success rates are percentages; subscripts report signed differences from Random at the same position, in percentage points. 

|Setu|Upper left|Upper right|Lower left|Lower right|
|---|---|---|---|---|
|p|(0_,_0)|(0_,_143)|(143_,_0)|(143_,_143)|
|Random|81.45|97.55|96.20|93.80|
|Reoptimized|0.00_−_81_._45|0.00_−_97_._55|0.00_−_96_._20|0.00_−_93_._80|
|Moved|0.00_−_81_._45|93.50_−_4_._05|94.85_−_1_._35|95.00+1_._20|


### **A.2. Direct transfer of VLA patches** 

To further broaden the attack spectrum beyond our design, we explore the potential of existing VLA attacks. Due to the incompatibility of the VLA and WAM paradigms, we run only the transfer setting, i.e., the attack targets a VLA victim and transfers the optimized patches to a WAM victim. 

Table 6 reports direct transfer to FastWAM of patches constructed by UADA (Wang et al., 2025a) and UPA-RFAS (Lu et al., 2026). 

We train UPA-RFAS and UADA patches on their respective source VLAs using the original attack settings, with the patch area matched to `TAPDreamer` . We then transfer these patches directly to FastWAM without further optimization. Overall success is 76.55% for UPA-RFAS and 75.85% for UADA, compared with 81.45% for the random patch: reductions of 4.90 and 5.60 percentage points, respectively. `TAPDreamer` reduces success to 0% across all four suites. 

## **B. How the Latent Shift Changes Action** 

### **B.1. Attention-restoration interventions** 

We want to understand which patch-induced changes within attention contribute to perturbation propagation, particularly the roles of attention weights _𝐴_ and value vectors _𝑉_ in downstream representation and action 

15 

TAPDreamer: Transferable Adversarial Patches for World Action Models 

Table 6: Direct transfer of VLA patches to FastWAM. Values are LIBERO task success rates (percent); subscripts report signed differences from Clean in the same suite or Overall column, in percentage points. Clean, Random, and `TAPDreamer` use the reference results in Table 1. 

|Setup|||LIBERO|||
|---|---|---|---|---|---|
||Spatial|Object|Goal|Long-hor.|Overall|
|Clean|98.00|99.60|97.60|95.40|97.65|
|Random|85.60_−_12_._40|78.00_−_21_._60|90.00_−_7_._60|72.20_−_23_._20|81.45_−_16_._20|
|UPA-RFAS|84.20_−_13_._80|76.80_−_22_._80|77.40_−_20_._20|67.80_−_27_._60|76.55_−_21_._10|
|UADA|82.00_−_16_._00|77.00_−_22_._60|77.20_−_20_._40|67.20_−_28_._20|75.85_−_21_._80|
|`TAPDreamer`|0.00_−_98_._00|0.00_−_99_._60|0.00_−_97_._60|0.00_−_95_._40|0.00_−_97_._65|


changes. To investigate this, we conduct three restoration interventions: restoring the entire attention branch, restoring only the attention weights _𝐴_ , and restoring only the value vectors _𝑉_ . Each intervention retains the patched residual branch and replaces only the specified component. 

We measure the remaining change relative to the clean output, normalized by the change without restoration. For latent retention, both changes are measured using the L2 norm over the entire latent, including the patch footprint; action retention uses the corresponding L2 ratio for action outputs. The random patch is evaluated with the same latent-retention metric. Because attention reconstruction uses a different numerical precision from model inference, the patched reference without restoration is computed through the same reconstruction pathway. These ratios measure retained changes, not task success rates. 

Table 7 shows that all three interventions leave approximately 33% of the latent change and 32% of the action change induced by `TAPDreamer` . In comparison, random-patch latent retention remains approximately 1.000. Thus, restoring the attention branch, its weights, or its values removes most of the `TAPDreamer` -induced latent and action changes, while having little effect on the random patch. 

Table 7: Fraction of patch-induced change retained after attention restoration. Latent and action columns report `TAPDreamer` ; the last column reports random-patch latent retention. Values are medians over 48 states. 

||Latent|Action|Random latent|
|---|---|---|---|
|Restored component|retained|retained|retained|
|Restore clean attention branch|0.3327|0.321|1.000|
|Weights A restored to clean|0.3364|0.320|1.000|
|Values V restored to clean|0.3327|0.321|1.000|


### **B.2. Optimization trajectories** 

To examine when shared perturbation structure emerges, we track optimization across three initializations on 48 observations. Within 25 steps, template agreement reaches at least 0.964 and effective rank falls below 1.39, while source displacement is only about 12% of its final magnitude. Subsequent optimization mainly amplifies displacement on both source and held-out observations while maintaining high alignment. 

Figure 8(a) shows that displacement grows on both source and held-out observations, indicating that the amplified perturbation extends beyond the source states. The early rise in template agreement in (b) and the effective rank approaching one in (c) indicate that a common direction emerges early and becomes dominant across observations. The high lower-bound ratio in (d) shows that the source-derived template accounts for a substantial fraction of held-out displacement even after subtracting the residual. Together, these trajectories indicate that optimization first establishes a shared direction and then mainly increases its magnitude. 

16 

TAPDreamer: Transferable Adversarial Patches for World Action Models 


Figure 8: Evolution of perturbation structure across observations during optimization. For three initializations, the panels show displacement on source and held-out observations, source-template agreement, the effective rank of 48 perturbation fields, and the ratio of the frozen source-template lower bound to measured L1 displacement. In (a), solid and dashed curves denote source and held-out states, respectively. Dotted lines show results with random patches. 

**Metrics and legend.** At each optimization checkpoint in Figure 8, we measure the final-latent change ∆ _𝑍𝑖_ on the 356 spatial cells outside the projected patch footprint. The source template ∆ _𝑍_ src is the mean displacement field over 12 source states at that checkpoint and is held fixed when evaluating the 36 held-out states. Panel (a) reports the median _‖_ ∆ _𝑍𝑖‖_ 1 separately for the source and held-out states. Panel (b) reports the median cosine similarity _⟨_ ∆ _𝑍_ src _,_ ∆ _𝑍𝑖⟩/_ ( _‖_ ∆ _𝑍_ src _‖_ 2 _‖_ ∆ _𝑍𝑖‖_ 2) over held-out states, with displacement fields flattened into vectors. 

For panel (c), we stack the 48 flattened displacement fields as rows of a matrix. Its effective rank is exp( _−_<sup>∑︀</sup> _𝑗_<sup>_𝑞𝑗_log</sup><sup>_𝑞𝑗_),where</sup><sup>_𝑞𝑗_=</sup><sup>_𝜎_</sup> _𝑗_<sup>2</sup><sup>_/_∑︀</sup> _𝑘_<sup>_𝜎_</sup> _𝑘_<sup>2and</sup><sup>_𝜎𝑗_areitssingularvalues(with0 log 0=0).Avaluenear</sup> one indicates that the displacement fields largely share one direction. Panel (d) reports the median ratio ( _‖_ ∆ _𝑍_ src _‖_ 1 _−‖_ ∆ _𝑍𝑖 −_ ∆ _𝑍_ src _‖_ 1) _/‖_ ∆ _𝑍𝑖‖_ 1 over held-out states: the frozen-template lower bound in Equation (8) divided by the measured L1 displacement. 

Colors identify the three initializations in all panels. Only panel (a) uses solid lines with circles for source states and dashed lines with squares for held-out states; panels (b)–(d) show one summary curve 

17 

TAPDreamer: Transferable Adversarial Patches for World Action Models 

per initialization. Gray dotted horizontal lines show the corresponding random-patch results, rather than an additional initialization. 

### **B.3. Behavioral effects** 

The preceding analyses show how patch-induced perturbations propagate through attention and how optimization establishes a shared direction before amplifying its magnitude. We now ask how these representation changes affect action commands and, in turn, lead to task failure. 

**Visible execution failures.** The same representation shift can affect different actions as a task unfolds. In Figure 9, the patch drives the end effector below its clean trajectory and prevents task completion. We use same-state action comparisons, internal restoration, and patch removal to connect the shift to commands and physical consequences. 


(a) Put the alphabet soup and tomato sauce in the basket 

(b) End-effector trajectory 

Figure 9: Example of closed-loop behavior under `TAPDreamer` . Left: observation sequences under clean and perturbed conditions. Right: corresponding three-dimensional end-effector position trajectories. Green dashed and red solid paths denote Clean and `TAPDreamer` , respectively. The triangle marks the starting position and stars mark the endpoints; _𝑡_ counts environment execution steps. Positions are in meters in the world coordinate frame. 

**Immediate action changes.** Holding the physical state fixed, we compare actions from clean and patched observations before their trajectories diverge. In FastWAM, the patch suppresses lifting, biases pose commands downward, and shifts gripper commands toward opening. A fit in which each patched six-dimensional pose command mixes its clean counterpart with a shared target explains 78.2% of the variation across 1,500 paired commands. These are state-level measurements, not independent episodes. The same bias can prevent a lift, lose an object after grasping, or move the end effector away from its intended position, depending on the task stage. These action patterns emerge from the encoder-level objective, which specifies no target action. 

**Action pathways across models.** The disturbed visual representation also reaches actions through different downstream designs. In Motus, restoring the branch that represents visual world dynamics recovers about 93%–99% of the action change, whereas restoring the visual-language understanding branch recovers about 10%–27%. In DreamWAM-joint, restoring predicted future representations also substantially recovers actions. These interventions link encoder interference to control while showing that its route depends on the model’s action pathway. 

18 

TAPDreamer: Transferable Adversarial Patches for World Action Models 

**Continued exposure and recovery.** Gripper commands shift toward closing at the first clean replan after removal, indicating that the immediate command bias depends on continued visual interference. Whether the task recovers then depends on the physical state: some pose deviations can be corrected, while dropped or misplaced objects and missed manipulation opportunities may persist. In the duration sweep, some tasks finish after removal following 20 corrupted replans, whereas continuous exposure maintains strong failure. Repeated exposure lets the fixed patch keep injecting the same latent change as execution accumulates physical consequences. 

19 

