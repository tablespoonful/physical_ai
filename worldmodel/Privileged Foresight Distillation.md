---
title: "Privileged Foresight Distillation: Zero-Cost Future Correction for World Action Models"
date: "2026-04-28"
authors: "Pengcheng Fang; Hongli Chen; Xiaohao Cai"
url: https://arxiv.org/abs/2604.25859
pdf: https://arxiv.org/pdf/2604.25859
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.25859)** / [論文ページ](https://arxiv.org/abs/2604.25859)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# PRIVILEGED FORESIGHT DISTILLATION: ZERO-COST FUTURE CORRECTION FOR WORLD ACTION MODELS 

**Pengcheng Fang Hongli Chen Xiaohao Cai** The University of Southampton The University of Queensland The University of Southampton 

May 5, 2026 

## **ABSTRACT** 

World action models jointly predict future video and action during training, raising an open question about what role the future-prediction branch actually plays. A recent finding shows that this branch can be removed at inference with little to no loss on common manipulation benchmarks, suggesting that future information may act merely as a regularizer on the shared visual backbone. We propose instead that joint training induces an action-conditioned correction that privileged future observations impose on action denoising, and that current-only policies capture this correction only partially. Making the account precise, we formulate privileged foresight as a residual in the action-denoising direction—the difference between what a model predicts given the true future and what it predicts given only the current frame—and introduce _Privileged Foresight Distillation (PFD)_ , which transfers this residual from a training-time teacher into a small adapter on a current-only student. The teacher and student share the same backbone and differ only in the attention mask over video tokens; future video is never generated at inference. Controlled experiments support that this gain reflects a future-conditioned correction rather than a side effect of capacity or regularization. Empirically, PFD improves over Fast-WAM on LIBERO and RoboTwin manipulation benchmarks while preserving the current-only inference interface with only a slight adapter-induced latency overhead. This view reframes the role of future information in world action models: not as a target to predict, nor as a regularizer to absorb, but as a compressible correction to be distilled. Code is available at github.com/PengchengFang-cs/PFD. 

## **1 Introduction** 

Joint prediction of future video and action is a central design pattern in world action models, motivated by the intuition that visual foresight during training helps an agent choose better actions. A recent finding challenges this premise: a model trained jointly with video prediction can be deployed without test-time future generation while matching or exceeding the predictive variant [Yuan et al., 2026]. The result has been read as evidence that test-time future imagination is unnecessary—but it leaves a deeper question unanswered. If the future branch is not used at inference, what role does future information play during training, and is any of its action-specific content lost when the branch is removed? 

Two readings of this finding are possible. On a _regularizer_ reading, future video shapes the shared visual backbone but contributes nothing action-specific; the current-only policy captures everything useful, and there is nothing to recover. On a _privileged-foresight_ reading, future video induces a structured correction on the action-denoising direction itself—a correction that joint training transfers only partially to the current-only path. The two readings are observationally similar in the existing literature, yet they imply opposite methodological prescriptions: the first directs effort toward stronger visual backbones, the second toward better mechanisms for transferring the privileged signal. We find that the first reading is incomplete. Simply exposing the current-only policy to more training capacity—naïve finetuning of the same backbone layers—fails to improve performance (Section 4.3), so the gap between what joint training can teach and what the current-only policy learns is not a capacity gap. The interesting signal, if it exists, must lie in a direction that pure supervision on the action target does not reach. 

A PREPRINT - MAY 5, 2026 

We locate this signal by asking what privileged access to the future would change in the action-denoising process. During training, we instantiate the same backbone as two parallel paths, identical except for the attention mask over video tokens: a current-only student that sees only the current frame (matching the standard joint-training setup), and a privileged teacher that attends to the full future video. The teacher’s action-velocity prediction minus the student’s defines a _foresight residual_ —the component of the denoising direction that becomes predictable once future information is available. _Privileged Foresight Distillation (PFD)_ trains a small adapter on the student path to predict this residual from current-only context. The residual target is detached before use, so the inherited joint-training objective is not pulled away from the action target by a moving teacher signal. At inference, the teacher is discarded and the adapter augments the student’s prediction at each denoising step; the current-only inference interface is preserved exactly, with the foresight-induced correction restored through a residual head whose added latency is slight (Section 4). 

We design controlled experiments to interpret PFD’s gain, isolating it from confounds of capacity, regularization, and fine-tuning-budget reallocation. None of these alternatives accounts for the observed effect, supporting a specific reading of the transferred signal: privileged foresight is a future-conditioned correction that is not recovered by matched direct fine-tuning under the same budget, and a small adapter is sufficient to absorb it. 

**Contributions.** We make the following contributions. 

- **A new perspective on future information.** We propose that future information in world action models is best understood as an action-conditioned correction residual—a direction not recovered by matched direct fine-tuning under the same budget. 

- **PFD.** We introduce a training-only teacher–student construction that makes this view operational: the teacher accesses real future during training, a small adapter distills the teacher-minus-student residual, and the adapter preserves the current-only inference interface with no future generation at test time. 

- **Controlled evidence for the transferred signal.** We design experiments that isolate PFD’s gain from confounds of capacity, auxiliary regularization, and budget reallocation between backbone fine-tuning and adapter capacity, supporting the reading of the foresight residual as a future-conditioned correction. 

- **Empirical results.** PFD improves over the Fast-WAM backbone on LIBERO and RoboTwin, matching or exceeding several methods that rely on embodied pretraining, while adding only a slight inference overhead from the adapter. 

## **2 Related Work** 

**World action models and future video.** Recent robot policies combine video backbones with action heads, either by jointly predicting future frames and actions [Wu et al., 2024, Cheang et al., 2024, Hu et al., 2025] or by conditioning actions on externally generated future videos [Du et al., 2023, Black et al., 2024b]. In both settings, future materialization—as pixels or latent rollouts—is required at inference and often dominates computation. Fast currentonly policies remove this test-time future generation with a single forward pass [Yuan et al., 2026]. We ask whether action-relevant future information can still benefit such current-only policies, and in what form. 

**Uses of future information.** Prior work mainly uses future information in two ways. _Future-as-prediction_ explicitly generates future frames for action conditioning [Du et al., 2023, Black et al., 2024b], while _future-as-representation_ learns latent imagination rollouts for planning or representation learning [Hafner et al., 2023, Schrittwieser et al., 2020, Hansen et al., 2024]. Both require future content to exist at test time in some form. In contrast, PFD uses _future-as-correction_ : future video is available only during training, where it reveals what a current-only policy misses, and is distilled into a residual correction that is not reconstructed at inference. 

**Privileged information and adapter heads.** PFD builds on asymmetric teacher–student learning with privileged information [Vapnik and Vashist, 2009, Chen et al., 2019], commonly used to transfer supervision from more informed teachers to constrained students. Here, teacher and student share the same backbone parameters and differ only in their attention mask over video tokens, removing architectural confounds. Moreover, PFD defines the adapter target as the teacher–student residual rather than replacing the student with full teacher imitation; a weak teacher-consistency term is used only to stabilize the corrected output, isolating the component attributable to future access. This residual is carried by a small action-stream adapter; unlike generic parameter-efficient adapters [Hu et al., 2022], it is explicitly sized and trained to encode the foresight residual. 

2 

A PREPRINT - MAY 5, 2026 


Figure 1: **PFD (Privileged Foresight Distillation). Top:** Student and privileged teacher paths differ only in their attention mask: the student action tokens attend to the current-frame video tokens and action tokens, matching the Fast-WAM current-only inference interface, whereas the teacher action tokens attend to all video tokens, including real future frames available only during training. **Left:** During training, the same MoT backbone is evaluated under both masks, yielding a live student prediction _v_ base and a stop-gradient privileged prediction _v_ teacher. The detached residual target _r_ = sg( _v_ teacher _− v_ base) captures the action-denoising correction induced by future access. A small adapter _gϕ_ takes the live _v_ base and predicts _δ_<sup>ˆ</sup> to fit this residual, producing _v_ final = _v_ base + _δ_<sup>ˆ</sup> . **Right:** At inference, the teacher path and future video tokens are discarded. The model runs only the student mask and applies the adapter correction, preserving the current-only Fast-WAM interface with no test-time future generation and slight adapter-only compute cost. 

## **3 Method** 

PFD is a training-time mechanism that operationalizes the future-as-correction view of §1: a privileged path with future access produces an action-side correction signal, and a small adapter on the current-only path absorbs it. Inference uses the current-only path and the adapter; the privileged path is not instantiated. 

### **3.1 Preliminaries** 

Let _X_ = ( _X_ 1 _, . . . , XT_ ) denote a sequence of _T_ video frames with _X_ 1 the current frame, and let _A_ denote the corresponding action chunk. Following Yuan et al. [2026], we adopt a Mixture-of-Transformers backbone with parameters _θ_ , comprising a video expert and an action expert, with cross-stream information exchange controlled by a joint attention mask. 

Both streams are trained with flow matching. We sample timesteps _τv, τa ∈_ [0 _,_ 1] independently and draw independent Gaussian noise _εv, εa_ , yielding the corrupted inputs 


with action-velocity target _v_ target = _A − εa_ . We write _u_ video for the video-velocity output and _u_ target = _X − εv_ for its target. We write 

_v_ act( _Xτv , Aτa , τv, τa_ ; _M_ ) 

3 

A PREPRINT - MAY 5, 2026 

for the action-velocity output produced by the backbone when the joint self-attention is restricted by mask _M_ . The current-only forward used at inference adopts the _student mask M_ S, under which each action-token query attends to the current-frame video tokens _X_ 1 and to the other action tokens: 


Throughout the displayed equations we omit first-frame observation conditioning and the per-timestep scheduler weighting on the velocity outputs for clarity; both follow Yuan et al. [2026] and are applied identically to the student and teacher forwards introduced below. 

### **3.2 A privileged forward via attention masking** 

PFD adds a second action forward, identical to (2) in every respect except for the attention mask: 


The _teacher mask M_ T allows each action-token query to attend to the full set of video tokens _X_ 1 _, . . . , XT_ , including future frames; sg( _·_ ) denotes the stop-gradient operator. The teacher and student forwards share the same parameters _θ_ at every step—there is no exponential moving average, no frozen copy, and no distinct teacher network—and they consume the same noisy inputs ( _Xτv , Aτa_ ) generated from a single noise sample ( _εv, εa_ ). The two forwards differ only in the attention mask over video tokens, which isolates the effect of future access: capacity, parameterization, optimizer state, and noise realization are held identical, so any difference between _v_ teacher and _v_ base is attributable to the enlargement of the action queries’ attention support. The stop-gradient on (3) further removes the teacher from the optimization graph, so it contributes no parameter update of its own and serves only as a target source for the residual we now define. Because the two forwards share _θ_ , the residual _v_ teacher _− v_ base is a model-dependent foresight-induced correction at the current parameter state and evolves during training. 

### **3.3 The foresight residual and the residual adapter** 

Rather than have the student imitate _v_ teacher in full, PFD distills only the component that future access changes. We define the _foresight residual_ as 


since _v_ teacher is already detached, this is equivalent to _r_ = _v_ teacher _−_ sg( _v_ base). Targeting _r_ rather than _v_ teacher confines supervision to the component that future access changes at the current _θ_ ; whenever the two masks induce identical predictions, the target is zero and no teacher signal enters the loss. 

The residual is absorbed by a small _residual adapter gφ_ placed at the output of the action expert and applied token-wise: 


First, the adapter consumes _v_ base rather than sg( _v_ base); only the residual target _r_ in (4) is detached. As we discuss in §3.4, this asymmetry is what allows residual supervision to influence the backbone subset _θ_<sup>_′_</sup> at all under partial fine-tuning, rather than reducing to a pure adapter-fitting problem on _φ_ . Second, the adapter’s output projection is zero-initialized, so _δ_<sup>ˆ</sup> _≡_ 0 at the start of training and _v_ final = _v_ base identically; the corrected forward equals the standard Fast-WAM student forward at initialization, and any departure from it accumulates only as training drives _gφ_ to fit _r_ . 

### **3.4 Training objective and gradient routing** 

Let _θ_<sup>_′_</sup> _⊆ θ_ denote the subset of backbone parameters that are permitted to update; the adapter parameters _φ_ always update. PFD trains ( _θ_<sup>_′_</sup> _, φ_ ) against the inherited video flow-matching loss together with three action-side losses: 


where _wv_ ( _·_ ) and _wa_ ( _·_ ) are the per-timestep weighting schedules of Yuan et al. [2026]. The full PFD objective is 

_L_ = _λ_ video _L_ video + _λ_ gt _L_ gt + _λ_ res _L_ res + _λ_ teacher _L_ teacher _,_ (10) 

with non-negative scalar coefficients; the values used in all experiments are reported in §4.1. 

4 

A PREPRINT - MAY 5, 2026 

**Gradient routing.** The teacher forward is fully stop-gradiented at (3) and contributes no update to _θ_ . The residual target _r_ in (4) is also detached, which prevents _L_ res from being trivially reduced by moving its target instead of fitting it. However, because the adapter input in (5) is the live _v_ base rather than sg( _v_ base), _L_ res is not confined to updating _φ_ : under partial fine-tuning, gradient also flows from _L_ res through the dependence of _δ_<sup>ˆ</sup> on _v_ base and into _θ_<sup>_′_</sup> . Residual supervision therefore reshapes both the correction head and the backbone’s emitted current-only velocity, with the detached target ensuring that the reshaping pulls _v_ base toward the privileged prediction rather than away from it. 

_L_ res **versus** _L_ teacher **.** The two teacher-derived losses coincide in forward value but differ in gradient path. Substituting _v_ final = _v_ base + _δ_<sup>ˆ</sup> into (9) gives _∥δ_<sup>ˆ</sup> _−_ ( _v_ teacher _− v_ base) _∥_<sup>2</sup> , which equals _L_ res as a number. They diverge once gradients are computed: _L_ res uses a fully detached residual target and routes gradient primarily through _gφ_ , with a secondary path into _θ_<sup>_′_</sup> via the adapter’s dependence on _v_ base; _L_ teacher keeps the live _v_ base inside _v_ final on the prediction side and detaches only _v_ teacher, so its gradient pulls the current-only velocity itself toward the privileged prediction rather than routing through _gφ_ . PFD retains both terms: _L_ res supervises the adapter through a detached target, while _L_ teacher pulls _v_ base toward _v_ teacher through the live prediction path. 

PFD admits two regimes via the choice of _θ_<sup>_′_</sup> : _adapter-only_ ( _θ_<sup>_′_</sup> = ∅, the backbone is frozen) and _partial fine-tuning_ ( _θ_<sup>_′_</sup> unfreezes the last _Ka_ blocks of the action expert and the last _Kv_ blocks of the video expert); specific values and the default configuration are reported in §4.1. 

### **3.5 Inference** 

At inference, PFD preserves the current-only denoising interface of Fast-WAM. At each flow-matching denoising step, the model computes the student velocity _v_ base from (2) under the student mask _M_ S, applies the residual adapter, and uses 

_v_ final = _v_ base + _gφ_ ( _v_ base _, τa_ ) 

for the sampling update on _Aτa_ . The teacher mask _M_ T is never instantiated at inference, and the future video frames _X_ 2 _, . . . , XT_ are neither generated nor consumed. The only added cost relative to Fast-WAM is one forward pass through _gφ_ per denoising step. 

## **4 Experiments** 

### **4.1 Experimental setup** 

**Benchmarks.** We evaluate on LIBERO [Liu et al., 2023] and RoboTwin 2.0 [Chen et al., 2025], following FastWAM [Yuan et al., 2026]. LIBERO contains four suites (Spatial, Object, Goal, Long); for each, we train one model on 500 demonstrations over 10 tasks and report success rate over 500 trials. RoboTwin 2.0 is a bimanual dual-arm benchmark; we use its multi-task setup with 2 _,_ 500 clean-scene and 25 _,_ 000 randomized-scene demonstrations across more than 50 tasks, reporting success over 100 trials per task in each condition. 

**Baselines.** Our primary baseline is Fast-WAM in two forms: “Fast-WAM (released)” directly transcribes the numbers from Yuan et al. [2026], while “Fast-WAM (reproduced)” is re-trained with the released configuration, codebase, and schedule used by our PFD runs, and serves as the reference for reported gains. The reproduced numbers are slightly lower than the original report but follow consistent suite-level trends under a unified evaluation pipeline. For broader context, we also include published numbers for OpenVLA [Kim et al., 2024], _π_ 0 [Black et al., 2024a], _π_ 0 _._ 5 [Physical Intelligence et al., 2025], Motus [Bi et al., 2025], and LingBot-VA [Li et al., 2026], taken verbatim from Yuan et al. [2026]. These five context baselines use embodied pretraining (“Emb. PT.”), whereas Fast-WAM and PFD use the Wan2.2-5B backbone without embodied pretraining. 

**Training.** We train for 30 epochs on LIBERO and 15 on RoboTwin using 8 H100 GPUs, matching Fast-WAM’s batch size, schedule, and optimizer family. We use AdamW with cosine decay, weight decay 0 _._ 01, gradient clipping 1 _._ 0, and benchmark-specific learning rates following Fast-WAM defaults: 6 _×_ 10<sup>_−_5</sup> for LIBERO and 1 _×_ 10<sup>_−_4</sup> for RoboTwin. PFD adds only the privileged forward of §3.2, which shares backbone parameters and introduces one additional attention pass per step. 

**Inference.** Following Fast-WAM, we use 10 flow-matching denoising steps with classifier-free guidance scale 1 _._ 0. At each step, PFD runs one student forward under _M_ S and applies the residual adapter, _v_ final = _v_ base + _gφ_ ( _v_ base _, τa_ ), as in §3.5. The teacher mask _M_ T is never instantiated at inference, and no future video frames are generated or consumed. End-to-end latency is reported in §4.4. 

**Implementation.** All main results use the partial fine-tuning regime of §3.4, with trainable parameters _θ_<sup>_′_</sup> _∪ φ_ . Here, _θ_<sup>_′_</sup> contains the last _Ka_ action-expert blocks and last _Kv_ video-expert blocks, each expert having 30 blocks, and _φ_ denotes 

5 

A PREPRINT - MAY 5, 2026 

Table 1: LIBERO success rate (%) over 500 trials per suite. “Emb. PT.” indicates embodied pretraining; “(reproduced)” is re-trained under our codebase. Bold marks the rows and per-suite numbers where PFD (partial fine-tune) exceeds the reproduced Fast-WAM. 

|**Method**|**Emb. PT.**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|---|---|
|OpenVLA [Kim et al., 2024]|✓|84.7|88.4|79.2|53.7|76.5|
|_π_0 [Black et al., 2024a]|✓|96.8|98.8|95.8|85.2|94.1|
|_π_0_._5 [Physical Intelligence et al., 2025]|✓|98.8|98.2|98.0|92.4|96.9|
|Motus [Bi et al., 2025]|✓|96.8|99.8|96.6|97.6|97.7|
|LingBot-VA [Li et al., 2026]|✓|98.5|99.6|97.2|98.5|98.5|
|Fast-WAM (released) [Yuan et al., 2026]|–|98.2|100.0|97.0|95.2|97.60<br>|
|Fast-WAM (reproduced)|–|97.0|99.4|96.6|94.8|96_._95<sup>_±_0</sup><sup>_._08</sup>|
|**PFD (partial fine-tune, ours)**|–|**98.6**|99.2|**99.2**|**95.4**|98_._10<sup>_±_0</sup><sup>_._06</sup>|
|PFD (adapter-only,_θ_<sup>_′_ </sup>=∅)|–|97.2|98.8|96.6|93.8|96.60|


Table 2: RoboTwin 2.0 success rate (%) over 100 trials per task. “Emb. PT.” indicates embodied pretraining; “from Wan2.2” is re-trained on our backbone without embodied pretraining. 

|**Method**|**Emb. PT.**|**Clean**|**Randomized**|**Average**|
|---|---|---|---|---|
|_π_0 [Black et al., 2024a]|✓|65.92|58.40|62.2|
|_π_0_._5 [Physical Intelligence et al., 2025]|✓|82.74|76.76|79.8|
|Motus [Bi et al., 2025]|✓|88.66|87.02|87.8|
|Motus from Wan2.2|–|77.56|77.00|77.3|
|LingBot-VA [Li et al., 2026]|✓|92.90|91.50|92.2|
|LingBot-VA from Wan2.2|–|80.60|–|80.6|
|Fast-WAM [Yuan et al., 2026]|–|91.88|91.78|91_._8<sup>_±_0</sup><sup>_._22</sup>|
|**PFD (partial fine-tune, ours)**|–|**93.11**|**92.69**|**92**_._**9**<sup>_±_</sup><sup>**0**</sup><sup>_._</sup><sup>**12**</sup>|


the adapter. We set ( _Ka, Kv_ ) = (12 _,_ 12) for both benchmarks, unfreezing about 40% of blocks per expert. The adapter _gφ_ is a three-layer SiLU MLP of width 512; it takes a linear projection of the live base-action velocity _v_ base from (2) and a sinusoidal embedding of _τa_ broadcast over tokens, with zero-initialized output projection. Loss weights are fixed for all PFD runs: _λ_ video = _λ_ gt = 1 _._ 0, _λ_ res = 0 _._ 5, and _λ_ teacher = 0 _._ 1. 

### **4.2 Main results** 

**LIBERO.** Table 1 reports per-suite success rates. PFD raises the LIBERO average from 96 _._ 95 for the reproduced Fast-WAM to 98 _._ 10, a gain of +1 _._ 15 on the four-suite mean. The per-suite breakdown is +1 _._ 6 on Spatial, _−_ 0 _._ 2 on Object, +2 _._ 6 on Goal, and +0 _._ 6 on Long. PFD improves on three of the four suites; on Object, where both methods exceed 99%, the difference of 0 _._ 2 points is at the binomial standard-error scale of 500-trial evaluation. The gains are most pronounced on Goal, while Long also improves over the reproduced Fast-WAM baseline. Comparing against methods that use embodied pretraining, PFD surpasses Motus (97 _._ 7), _π_ 0 _._ 5 (96 _._ 9), and _π_ 0 (94 _._ 1), and trails LingBot-VA (98 _._ 5) by 0 _._ 40—without invoking a separate embodied pretraining stage. Adapter-only PFD ( _θ_<sup>_′_</sup> = ∅) reaches 96 _._ 60, competitive on Spatial, Object, and Goal but below the Fast-WAM baseline on Long; we therefore adopt partial fine-tuning as the default configuration and revisit the adapter-only regime as an ablation in §4.3. 

**RoboTwin 2.0.** Table 2 reports clean-scene, randomized-scene, and average success rates. PFD reaches 93 _._ 11 _/_ 92 _._ 69 on clean and randomized respectively, with an average of 92 _._ 9, improving over the Fast-WAM row by +1 _._ 23 on clean, +0 _._ 91 on randomized, and +1 _._ 10 on the average. PFD’s 92 _._ 9 also exceeds the strongest embodied-pretrain baseline (LingBot-VA at 92 _._ 2) by 0 _._ 7 despite using no embodied pretraining, and is the highest among all Wan2.2-based entries. 

### **4.3 Isolating the foresight signal** 

The aggregate gain reported in §4.2 is consistent with the privileged-foresight account but does not by itself rule out simpler explanations: extra trainable capacity in _θ_<sup>_′_</sup> , generic regularization from a second teacher forward, or a different allocation of the fine-tuning budget between backbone depth and adapter capacity. We design three controlled probes that share PFD’s training budget but each break exactly one ingredient of the foresight transfer, and verify whether breaking that ingredient erases the gain. We run probes on LIBERO; the four-suite split exposes capacity and 

6 

A PREPRINT - MAY 5, 2026 

Table 3: LIBERO epistemic probes (success rate %). The first three probes break, in turn, capacity, temporal correspondence, and the allocation of the fine-tuning budget between backbone depth and adapter width. The last two rows are supplementary ablations on the adapter regime and on fine-tune depth. 

|**Configuration**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|---|
|Fast-WAM (reproduced)|97.0|99.4|96.6|94.8|96.95|
|Pure finetune (_θ_<sup>_′_</sup>, no teacher)|96.4|99.2|96.4|94.8|96.70|
|Shuffled-future PFD|96.1|99.2|96.2|95.0|96.62|
|PFD, width1024at(_Ka, Kv_) = (12_,_6)|97.9|99.8|97.2|94.5|97.36|
|**PFD (default)**(_Ka, Kv_) = (12_,_12),_W_ = 512<br>|**98.6**|99.2|**99.2**|**95.4**|**98.10**|
|adapter-only (_θ_<sup>_′_ </sup>=∅)|97.2|98.8|96.6|93.8|96.60|
|fine-tune depth(_Ka, Kv_) = (6_,_6)|97.9|99.7|97.3|94.7|97.40|


correspondence dimensions independently of RoboTwin’s bimanual coordination, which we treat as an end-to-end test in §4.2. Numerical results are collected in Table 3 and visualized in Figure 2. 

**Matched-capacity control.** The first probe, _pure finetune_ , unfreezes the same backbone subset _θ_<sup>_′_</sup> = ( _Ka, Kv_ ) = (12 _,_ 12) and trains against the action ground truth alone, with no teacher forward and no adapter. If the PFD gain were attributable to the additional trainable capacity that _θ_<sup>_′_</sup> exposes, this control would match or exceed PFD. It does not: pure finetune scores 96 _._ 4 _/_ 99 _._ 2 _/_ 96 _._ 4 _/_ 94 _._ 8 for an average of 96 _._ 70, which is _−_ 0 _._ 25 below the reproduced Fast-WAM and _−_ 1 _._ 40 below PFD. Unfreezing the same subset of layers under direct action supervision slightly hurts the current-only policy at this training budget. The signal that PFD transfers is therefore not accessible to direct supervision on the action target, even when the layers permitted to update are identical. 

**Shuffled-future control.** The second probe, _shuffled-future_ PFD, replaces the teacher’s future frames _X_ 2 _, . . . , XT_ at every training step with frames drawn from an unrelated trajectory in the same batch. The teacher mask _M_ T, the adapter, the loss weights, and the schedule are otherwise identical to the default PFD run. If the gain reflected auxiliary-loss regularization or the mere presence of a second supervisory target, destroying the temporal correspondence between _X_ 1 and _X_ 2: _T_ should leave it largely intact, since the input statistics and loss magnitudes are preserved. Instead, shuffledfuture PFD scores 96 _._ 1 _/_ 99 _._ 2 _/_ 96 _._ 2 _/_ 95 _._ 0 for an average of 96 _._ 62, which is _−_ 0 _._ 33 below the reproduced Fast-WAM and _−_ 1 _._ 48 below PFD. The transferred signal therefore depends on genuine current-to-future correspondence, not on incidental properties of the teacher forward. 

**Depth–width trade-off probe.** The third probe asks whether reducing video-side fine-tuning depth while increasing residual-head width can substitute for the default full-depth PFD configuration. We double the adapter hidden width from 512 to 1024 and, to test a practical depth–width trade-off, halve the video-expert fine-tune depth from _Kv_ = 12 to _Kv_ = 6 (the action expert is held at _Ka_ = 12). This redirects the freed compute from updating the deeper video stack into a wider correction head. The resulting configuration scores 97 _._ 9 _/_ 99 _._ 8 _/_ 97 _._ 2 _/_ 94 _._ 5 for an average of 97 _._ 36, which is _−_ 0 _._ 74 below the default PFD at width 512. Redirecting fine-tuning budget from the video expert to a wider adapter therefore fails to recover the gain. We cannot rule out a clean adapter-width effect at fixed ( _Ka, Kv_ ) = (12 _,_ 12) and leave that question to future work. 

**Reading the probes together.** Relative to the default PFD average of 98.10, the three probes land at deltas of _−_ 1 _._ 40 (matched-capacity), _−_ 1 _._ 48 (shuffled-future), and _−_ 0 _._ 74 (budget-reallocation). Two readings split cleanly. _Ruled out_ : extra trainable capacity and auxiliary-loss regularization each erase the PFD gain when isolated, with the matchedcapacity row falling below the frozen baseline and the shuffled-future row matching it. _Argued against, not ruled out_ : budget-reallocation closes only part of the gap, and the supplementary _K_ = 6 row reported below scores similarly at 97 _._ 40 without any adapter widening, corroborating the reading that the residual gap from 97 _._ 40 to 98 _._ 10 tracks fine-tune depth on the video expert rather than adapter width. None of the three confounds reproduces the privileged-foresight residual _r_ in (4): _r_ is by construction the component of the action-velocity field that becomes available when the attention mask exposes future frames at the same parameters, and the alternatives examined here change capacity, target, or budget allocation while leaving that mask alone. 

**Fine-tune depth (supplementary).** As a supplementary check, we ablate the depth of the trainable backbone subset by halving _K_ = _Ka_ = _Kv_ from 12 to 6 at the default adapter width of 512. This configuration scores 97 _._ 9 _/_ 99 _._ 7 _/_ 97 _._ 3 _/_ 94 _._ 7 for an average of 97 _._ 40, which is _−_ 0 _._ 70 below default PFD but +0 _._ 45 above the reproduced Fast-WAM. Its close correspondence to the budget-reallocation row at 97.36 indicates that at the half-depth setting the gap to default PFD is already determined by _K_ and is not closed by adapter widening. The teacher therefore contributes useful signal even at half depth, and additional fine-tune depth on the video expert continues to absorb it. 

7 

A PREPRINT - MAY 5, 2026 


Figure 2: LIBERO average success rate for the three primary probes, Fast-WAM (reproduced), and PFD (default). Breaking matched-capacity (Pure FT) or temporal-correspondence (Shuffled Future) drops accuracy below the FastWAM baseline (red); the budget-reallocation control—redirecting video-side fine-tuning budget to a wider adapter (Width 1024 at _Kv_ = 6)—closes only part of the PFD gap (amber). The supplementary fine-tune-depth check ( _K_ = 6) is shown for comparison and lands at the similar level. 

### **4.4 Inference overhead** 

Table 4: End-to-end inference latency per action chunk. In our LIBERO setting, one chunk contains 32 actions. Slowdown is reported relative to the current-only Fast-WAM cached-context baseline. 

|**Method**|**Test-time future**|**Latency (ms/chunk)**|**Slowdown**|
|---|---|---|---|
|Fast-WAM-Joint|joint video+action denoising|786_._2|3_._05_×_|
|Fast-WAM-IDM|generate future, then IDM|1098_._1|4_._26_×_|
|Fast-WAM|none (current-only)|257_._7|1_._00_×_|
|**PFD (ours)**|none (current-only) + adapter|**271**_._**0**|**1**_._**05**_×_|


A central practical question for any future-aware policy is how much foresight costs at deployment time. Models that materialize future video at inference— either by jointly denoising future frames and actions, or by generating a future clip before an inverse-dynamics module (IDM)—pay a multiplicative latency penalty, because future frames must be produced before any action chunk can be emitted. To put PFD’s cost in context, we project the relative slowdowns reported by Fast-WAM onto our measured cached-context baseline: joint denoising and imagine-then-execute IDM inference would be approximately 3 _._ 05 _×_ and 4 _._ 26 _×_ slower than the current-only interface. 

Table 4 reports end-to-end latency per action chunk on a single H100, measured over 20 trials after discarding 5 warmup runs, under the 10 flow-matching denoising steps used throughout this paper. In our LIBERO setup, each `infer_action` call predicts a chunk of 32 actions. The current-only Fast-WAM cached-context baseline runs at 257 _._ 77 ms per chunk, while PFD runs at 271 _._ 04 ms per chunk, adding 13 _._ 27 ms or 5 _._ 15% overhead. We also evaluate the prompt-mode implementation of PFD, which runs at 282 _._ 29 ms per chunk and adds 7 _._ 80 ms, or 2 _._ 84%, over its corresponding prompt-mode baseline. 

These results show that the adapter cost remains small under both inference implementations. The added latency is attributable to one lightweight _gφ_ forward at each denoising step, which is slight compared with the Wan2.2-5B backbone. PFD never instantiates the teacher mask at inference and never generates future video frames, exactly as 

8 

A PREPRINT - MAY 5, 2026 

specified in §3.5; the deployment profile of the current-only interface is preserved while recovering the foresight-induced correction. 

## **5 Conclusion** 

We revisited the role of future video in world action models once test-time imagination is removed, and argued that future is best understood not as a prediction target nor as a regularizer to absorb, but as a compressible correction to be distilled. PFD operationalizes this view with a same-backbone teacher–student construction and a small output-side adapter that absorbs the foresight residual. Three epistemic probes—matched-capacity, shuffled-future, and budgetreallocation—attribute the gain to the foresight signal itself, and PFD improves over Fast-WAM on both LIBERO and RoboTwin with a slight adapter-only inference overhead while preserving the current-only inference interface exactly. 

**Limitations.** Two limitations are worth noting. First, the construction is deliberately simple: a single output-side MLP adapter, a full-horizon teacher mask, and a single backbone family. More expressive adapter designs—multiscale, gated, or cross-attentive—and richer teacher-mask schedules remain to be explored. Second, our claims are empirical: we observe that the foresight residual is absorbable by a small adapter and that capacity, regularization, and budget-reallocation alternatives do not account for the gain, but we do not provide a formal characterization of when the residual admits a low-capacity approximation. A theoretical account would tell us a priori which task families and backbones PFD should help. 

## **References** 

- Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, and Jun Zhu. Motus: A unified latent action world model. _arXiv preprint arXiv:2512.13030_ , 2025. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024a. 

- Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pre-trained image-editing diffusion models. In _International Conference on Learning Representations (ICLR)_ , 2024b. URL `https://openreview.net/forum?id=c0chJTSbci` . 

- Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, Hanbo Zhang, and Minzhao Zhu. GR-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. URL `https://arxiv.org/abs/2410.06158` . 

- Dian Chen, Brady Zhou, Vladlen Koltun, and Philipp Krähenbühl. Learning by cheating. In _Conference on Robot Learning (CoRL)_ , 2019. URL `https://arxiv.org/abs/1912.12294` . 

- Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, Weiliang Deng, Yubin Guo, Tian Nian, Xuanbing Xie, Qiangyu Chen, Kailun Su, Tianling Xu, Guodong Liu, Mengkang Hu, Huan-ang Gao, Kaixuan Wang, Zhixuan Liang, Yusen Qin, Xiaokang Yang, Ping Luo, and Yao Mu. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- Yilun Du, Mengjiao Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Joshua B. Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2023. URL `https://arxiv.org/abs/2302.00111` . 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. URL `https://arxiv.org/abs/2301.04104` . 

- Nicklas Hansen, Hao Su, and Xiaolong Wang. TD-MPC2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations (ICLR)_ , 2024. URL `https://arxiv.org/abs/2310. 16828` . 

- Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In _International Conference on Learning Representations (ICLR)_ , 2022. URL `https://openreview.net/forum?id=nZeVKeeFYf9` . 

9 

A PREPRINT - MAY 5, 2026 

- Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. In _International Conference on Machine Learning (ICML)_ , 2025. URL `https://arxiv.org/abs/2412.14803` . Spotlight. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, Yujun Shen, and Yinghao Xu. Causal world modeling for robot control. _arXiv preprint arXiv:2601.21998_ , 2026. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, Timothy Lillicrap, and David Silver. Mastering Atari, Go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, 2020. doi: 10.1038/s41586-020-03051-4. 

- Vladimir Vapnik and Akshay Vashist. A new learning paradigm: Learning using privileged information. _Neural Networks_ , 22(5–6):544–557, 2009. doi: 10.1016/j.neunet.2009.06.042. 

- Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In _International Conference on Learning Representations (ICLR)_ , 2024. URL `https://openreview.net/forum?id=NxoFmGgWC9` . 

- Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-WAM: Do world action models need test-time future imagination? _arXiv preprint arXiv:2603.16666_ , 2026. URL `https://arxiv.org/abs/2603.16666` . 

10 

