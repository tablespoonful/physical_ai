---
title: "RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models"
date: "2026-05-05"
authors: "Hao Wu; Yuqi Li; Yuan Gao; Fan Xu; Fan Zhang; Kun Wang"
url: https://arxiv.org/abs/2605.03821
pdf: https://arxiv.org/pdf/2605.03821
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.03821)** / [論文ページ](https://arxiv.org/abs/2605.03821)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ROBOALIGN-R1: Distilled Multimodal Reward Alignment for Robot Video World Models** 

**Hao Wu**<sup>1</sup><sup>_,∗_</sup> **Yuqi Li**<sup>2</sup><sup>_,∗_</sup> **Yuan Gao**<sup>1</sup><sup>_,∗_</sup> **Fan Xu**<sup>5</sup><sup>_,†_</sup> **Fan Zhang**<sup>3</sup> **Kun Wang**<sup>4</sup><sup>_,†_</sup> **Penghao Zhao**<sup>5</sup> **Qiufeng Wang**<sup>5</sup> **Yizhou Zhao**<sup>6</sup> **Weiyan Wang**<sup>5</sup> **Yingli Tian**<sup>2</sup> **Xian Wu**<sup>5</sup><sup>_,†_</sup> **Xiaomeng Huang**<sup>1</sup> 

- 1THU 2CUNY 3CUHK 4NTU 5Tencent 6CMU 

   - _∗_ Equal contribution. _†_ Corresponding authors. 

      - `wu-h25@mails.tsinghua.edu.cn` 

## **Abstract** 

Existing robot video world models are typically trained with low-level objectives such as reconstruction and perceptual similarity, which are poorly aligned with the capabilities that matter most for robot decision making, including instruction following, manipulation success, and physical plausibility. They also suffer from error accumulation in long-horizon autoregressive prediction. We present ROBOALIGN-R1, a framework that combines reward-aligned post-training with stabilized long-horizon inference for robot video world models. We construct ROBOTWORLDBENCH, a benchmark of 10,000 annotated video–instruction pairs collected from four robot data sources, and train a multimodal teacher judge, ROBOALIGN-JUDGE, to provide fine-grained six-dimensional evaluation of generated videos. We then distill the teacher into a lightweight student reward model for efficient reinforcement-learning-based post-training. To reduce long-horizon rollout drift, we further introduce _Sliding Window Re-encoding_ (SWR), a trainingfree inference strategy that periodically refreshes the generation context. Under our in-domain evaluation protocol, ROBOALIGN-R1 improves the aggregate sixdimension score by 10 _._ 1% over the strongest baseline, including gains of 7 _._ 5% on Manipulation Accuracy and 4 _._ 6% on Instruction Following; these ranking improvements are further supported by an external VLM-based cross-check and a blinded human study. Meanwhile, SWR improves long-horizon prediction quality with only about 1% additional latency, yielding a 2 _._ 8% gain in SSIM and a 9 _._ 8% reduction in LPIPS. Together, these results show that reward-aligned post-training and stabilized long-horizon decoding improve task consistency, physical realism, and long-horizon prediction quality in robot video world models. Codes are available. 

## **1 Introduction** 

Robot video world models are becoming an important component of embodied intelligence because they predict how scenes may evolve under candidate actions before executing them in the real world [1, 2, 3]. As learnable internal simulators, they support planning, policy evaluation, and long-horizon reasoning [4, 5, 6]. Unlike generic video generation, robot world models must capture action-conditioned dynamics, contacts, and scene evolution so that predicted futures remain consistent with manipulation outcomes and are useful for control [7, 8]. This requirement makes it challenging to achieve visual fidelity, task consistency, and physical plausibility simultaneously [9, 10]. 

However, most existing robot video world models [8, 11, 12, 13] are trained with maximum-likelihood, reconstruction, or perceptual objectives. These losses optimize statistical similarity rather than decision-making utility, leading to a fundamental mismatch: a prediction can be visually accurate 

40th Conference on Neural Information Processing Systems (NeurIPS 2026). 


Figure 1: **Overview of ROBOALIGN-R1.** ROBOTWORLDBENCH provides robot-centric benchmark statistics and fine-grained annotations for training a multimodal teacher judge. The teacher is distilled into a lightweight student reward model for efficient reinforcement-learning-based post-training of robot video world models. In parallel, a sliding-window re-encoding strategy stabilizes long-horizon autoregressive rollouts by periodically refreshing the visual context during inference. 

yet task-incorrect or physically implausible. This gap becomes more pronounced in long-horizon generation, where small errors accumulate and task-level correctness dominates frame-level similarity. 

Recent efforts to address this issue via reinforcement learning still rely largely on low-level rewards such as MSE, LPIPS, or SSIM. While efficient, these metrics fail to capture high-level properties critical for robot reasoning, including instruction following, manipulation success, and physically consistent interactions [8, 14]. As a result, current training objectives remain poorly aligned with the capabilities that matter most for downstream control. 

These limitations highlight two key challenges. 1) **_reward misalignment_** : low-level metrics are scalable but weak, while stronger multimodal evaluators are computationally prohibitive for online optimization. 2) **_long-horizon drift_** : autoregressive generation accumulates errors over time, degrading physical realism and task consistency [15]. To address these challenges, we propose ROBOALIGN-R1, a unified framework for improving both training-time alignment and inferencetime stability in robot video world models (Figure 1). Our approach introduces a distilled multimodal reward that aligns model optimization with task-level objectives, and a sliding window re-encoding (SWR) strategy that mitigates long-horizon error accumulation during inference. 

Specifically, we construct ROBOTWORLDBENCH, a large-scale benchmark of 10 _K_ annotated video–instruction pairs curated from four robot datasets. Using this data, we train a multimodal teacher model (ROBOALIGN-JUDGE) that provides fine-grained, multi-dimensional evaluation of generated videos. We then distill this teacher into a lightweight student reward model, enabling efficient reinforcement-learning-based post-training. Complementing this, SWR periodically refreshes the autoregressive context without retraining, improving long-horizon prediction quality with minimal overhead. Our contributions are threefold: 

❶ **_Reward-aligned training framework_ .** We introduce ROBOALIGN-R1, which replaces weak low-level online rewards with a distilled multimodal reward aligned with task success. This improves aggregate in-domain evaluation performance by +10 _._ 1 **%** over the strongest baseline while reducing online reward cost by over 10 _×_ , with gains validated by both VLM-based evaluation and blinded human studies. 

❷ **_Benchmark and scalable reward distillation_ .** We build ROBOTWORLDBENCH, a dataset of 10 _K_ annotated video–instruction pairs from four robot datasets, and a teacher–student distillation pipeline that compresses an 8 _B_ multimodal judge into a 98 _M_ reward model running at _∼_ 50 videos/sec. 

❸ **_Stable long-horizon inference_ .** We propose sliding window re-encoding, a training-free decoding strategy that mitigates autoregressive drift by refreshing context during rollout. SWR improves 

2 

long-horizon quality with minimal overhead, yielding +2 _._ 8 **%** SSIM, +0 _._ 62 dB PSNR, and _−_ 9 _._ 8 **%** LPIPS at about 1 **%** additional latency, with a 12.2% reduction in ROI-LPIPS. 

## **2 Related Work** 

The relevant technical background is as follows; the full stack context can be found in Appendix A. 

**_Robot Video World Models and RL Post-Training_ .** World models act as internal simulators for planning and long-horizon decision making by predicting future observations under candidate actions [1, 5]. Recent advances in video generation and embodied learning have led to growing interest in robot video world models for modeling manipulation dynamics, interaction outcomes, and future observations [3, 16, 17, 18, 11, 12, 19, 13]. Most existing methods, however, still focus on generation or representation quality and are trained with maximum-likelihood, reconstruction, or perceptual objectives [19, 13, 20, 21, 22]. Recent work has explored RL-based post-training for world models [8, 23, 24], but current rewards remain largely low-level or verifiable, such as reconstruction and perceptual similarity, which are weak proxies for instruction following, physical plausibility, and long-horizon outcome correctness [8, 25, 26, 24]. Similar issues appear in physical spatiotemporal forecasting, where reconstruction-based training often produces oversmoothed predictions and misses rare but decision-relevant events [27, 28, 26]. In addition, autoregressive token-based world models suffer from long-horizon error accumulation at inference time [29, 15, 30, 31]. Our work studies reward-aligned post-training together with a simple strategy for stabilizing long-horizon rollouts. 

**_Multimodal Judges and Rewards_ .** Recent work has explored multimodal evaluators and reward models for video understanding and generation [32, 33, 34]. Compared with low-level visual metrics, these judges provide supervision that better reflects instruction following, physical plausibility, and higher-level video consistency [7, 14, 32, 33]. However, their cost and latency make them difficult to use directly as online rewards in reinforcement learning [7, 33, 14]. ROBOALIGN-R1 follows this direction, but targets robot video world models and distills multimodal judgment into a lightweight reward model for online reinforcement learning. 

## **3 Method** 

ROBOALIGN-R1 addresses two key challenges in robot video world models: _reward misalignment_ during training and _error accumulation_ during inference. ROBOALIGN-R1 unifies reward-aligned post-training and stabilized long-horizon decoding within a single framework. 

### **3.1 Token-Based Robot Video World Model** 

Our backbone (Figure 2) follows the _tokenize–predict–decode_ paradigm. A dual-branch visual tokenizer _T_ vis = ( _Ec, Ed_ ) maps a short clip to discrete tokens: _Ec_ encodes a conditioning frame into _Nc context tokens z_<sup>ctx</sup> , while _Ed_ , cross-attended to _Ec_ ’s feature pyramid, encodes each observation frame into _Nd dynamics tokens zt_<sup>dyn</sup> carrying only residual change. Robot actions _at ∈_ R<sup>_da_</sup> are discretized into action-token blocks ˆ _at_ and interleaved with visual tokens, forming a unified sequence _s_ =[ _z_<sup>ctx</sup> _, z_ 1<sup>dyn</sup> _, a_ ˆ1 _, z_ 2<sup>dyn</sup> _, a_ ˆ2 _, . . ._ ] (sizes _Nc_ =1280, _Nd_ =80, vocabulary _K_ =4375; see Appendix B). A causal Transformer then models this sequence via standard next-token prediction: 


At inference time the predicted tokens _z_ ˆ1:<sup>dyn</sup> _T_<sup>are decoded back to pixels via</sup><sup>_x_ˆ1:</sup><sup>_T_=</sup><sup>_D_vis(</sup><sup>_z_ctx</sup><sup>_,_ˆ</sup><sup>_z_</sup> 1:<sup>dyn</sup> _T_<sup>).</sup> The resulting rollout is used for both reward-aligned post-training (§3.2) and sliding-window reencoding (§3.3). In our implementation, a dual-branch FSQ tokenizer [35, 30] encodes the conditioning frame into context tokens and each subsequent observation into dynamics tokens, while continuous actions are normalized, uniformly binned, and assigned a disjoint vocabulary range. A 12layer LLaMA decoder models the interleaved sequence under a causal mask with loss applied only to dynamics tokens. During inference, context tokens are encoded once and cached, and sliding-window re-encoding is triggered every _W_ steps. More technical details can be found in Appendix B. 

### **3.2 Reward-Aligned Post-Training** 

The pre-training objective (Eq. 1) captures surface-level statistical regularity but is agnostic to instruction following, physical plausibility, and action–outcome consistency. We close this gap via RL 

3 


Figure 2: **Token-based robot video world model. (a)** Training: a dual-branch FSQ tokenizer produces context tokens _c_ and dynamics tokens _dt_ ; discretized action tokens are interleaved and modeled by a 12-layer LLaMA Transformer with loss on dynamics tokens only. **(b)** Inference: context tokens are encoded once and cached; the model autoregressively predicts _d_<sup>ˆ</sup> _t_ +1 and triggers sliding-window re-encoding every _W_ steps. 

post-training with a structured multimodal reward, obtained in three stages: benchmark construction, teacher training, and reward distillation. 

**RobotWorldBench.** Let _l_ denote an instruction and _v_<sup>+</sup> a ground-truth manipulation video from established datasets. RobotWorldBench begins from a candidate pool drawn from four robot datasets and combines two annotation sources: rule-based degradations of ground-truth episodes and generated videos from open-source image-to-video or world-model baselines. From this pool we curate 10,000 annotated video–instruction pairs for judge training and reward distillation. Each retained pair ( _l, v_ ) is annotated with a raw score vector **r** = ( _r_ 1 _, . . . , r_ 6) along six dimensions _instruction following_ , _manipulation success_ , _action–outcome consistency_ , _temporal consistency_ , _contact realism_ , and _physics adherence_ using the original rubric ranges [3 _,_ 2 _,_ 1 _,_ 1 _,_ 1 _,_ 2], yielding 


**Multimodal teacher judge.** We fine-tune Qwen3-VL-8B-Thinking [36] as the teacher judge _fϕ_ . Given ( _l, v_ ), the teacher produces structured raw scores ˆ **r** = _fϕ_ ( _l, v_ ) in the same six-dimensional rubric space as **r** via supervised fine-tuning on _D_ bench: 


**Student reward distillation.** The teacher’s autoregressive decoding cost precludes its use as an online RL reward. We distill its judgments into a lightweight student _gψ_ —a compact visual– text encoder followed by a sigmoid-activated head emitting _gψ_ ( _l, v_ ) _∈_ [0 _,_ 1]<sup>6</sup> . The distillation set _D_ distill mixes annotated benchmark videos with teacher-scored rollouts from baseline/current world models. Teacher raw scores _fϕ_ ( _l, v_ ) are normalized dimension-wise via ˜ _sk_ =[ _fϕ_ ( _l, v_ )] _k/rk_<sup>max</sup> with _rk_<sup>max</sup> _∈{_ 3 _,_ 2 _,_ 1 _,_ 1 _,_ 1 _,_ 2 _}_ so both sides of the regression share the same [0 _,_ 1] scale: 


with Huber threshold _δh_ =0 _._ 5 (distinct from the quantization _δq_ of Appendix C) and per-dimension balancing weights _{λk}_ (Appendix E); these differ from the reward-aggregation weights _{wk}_ in Eq. 5. To counter reward hacking from distributional shift, we use _online iterative distillation_ : every _K_ policy updates, fresh rollouts are re-scored by the teacher to refresh the student. 

4 


Figure 3: **Sliding window re-encoding.** _Top:_ analogy to StreamingLLM [15], which retains an attention sink and a sliding KV-cache window in the language domain. _Bottom:_ our approach periodically decodes the last predicted frame to pixel space, re-encodes it as fresh context tokens, and resets the autoregressive prompt, empirically limiting long-horizon drift while keeping the active KV-cache bounded by _O_ ( _W_ ). _Right:_ technical details of a single refresh step. 

**RL post-training with GRPO.** The distilled student provides a composite reward over the six dimensions: 


where [ _gψ_ ] _k ∈_ [0 _,_ 1] are the student’s normalized scores (same scale as in Eq. 4) and _{wk}_ are importance weights. We post-train with GRPO [37, 8]: given a group of _G_ rollouts _{x_ ˆ<sup>(</sup><sup>_j_)</sup> _}_<sup>_G_</sup> _j_ =1<sup>_∼pθ_,</sup> the group-normalized advantage is 


and the clipped policy-gradient objective reads 


where _ρ_<sup>(</sup><sup>_j_)</sup> = _pθ_ (ˆ _x_<sup>(</sup><sup>_j_)</sup> ) _/pθ_ old(ˆ _x_<sup>(</sup><sup>_j_)</sup> ) with _θ_ old synchronized to _θ_ at each GRPO iteration, and _pθ_ 0 is the frozen pre-trained reference used for KL regularization. The student scores each rollout in one forward pass, reducing reward cost by over 10 _×_ relative to the teacher while preserving high-level judgment fidelity. 

### **3.3 Sliding Window Re-encoding** 

Under standard autoregressive decoding, each dynamics-token block _z_ ˆ _t_<sup>dyn</sup> is conditioned on all previously _predicted_ tokens, so per-step errors compound and progressively degrade long-horizon rollouts. Inspired by the attention-sink mechanism of StreamingLLM [15] in the language domain, we introduce a training-free decoding strategy that periodically decodes recent predictions to pixel space and re-encodes them as fresh context, which can limit the carry-over of token-level drift across segments (Figure 3). 

**Segmented generation.** A rollout of _T_ frames is partitioned into _K_ = _⌈T/W ⌉_ segments of window size _W_ (Figure 3, right). Within segment _k_ , the model generates _W_ dynamics-token blocks from context _zk_<sup>ctx:</sup> 


where _z_ 1<sup>ctx</sup> is the original context encoding of the first conditioning frame. 

5 

**Context refresh.** At each segment boundary, the last predicted frame is decoded to pixel space and re-encoded as fresh context for the next segment (Figure 3, right): 


where _x_ ˆ _kW_ serves as both the new conditioning frame for _Ec_ and a length-one dynamic clip for _Ed_ ; _z_ 0<sup>dyn</sup> seeds the next segment’s prompt (Appendix B.2). This _decode–re-encode_ cycle makes subsequent predictions depend on the current decoded frame rather than the entire raw token history. 

**Stylized stability analysis.** We provide a simplified local error analysis that explains the qualitative window-size trade-off, rather than predicting exact gains. Let _ε_ upper-bound the per-step token-space prediction error, _δq_ the decode–re-encode quantization error, and _α ∈_ [0 _,_ 1) a local contraction factor on within-segment context-error amplification (precise assumptions in Appendix C). **Proposition 1.** _Under the stylized model above, sliding-window re-encoding with window size W yields the bound_ 


_which does not grow explicitly with T ; the α →_ 0 _limit simplifies to_ 2 _Wε_ + _δq. By contrast, vanilla AR without refresh admits a worst-case bound of order ε/_ (1 _− α_ ) _, which blows up as α →_ 1 _and degrades to O_ ( _Tε_ ) _in the non-contractive regime._ 

_Proof sketch._ Within segment _k_ the context is fixed, so errors accumulate for _≤ W_ steps, giving _≤ Wε_ + _α_<sup>_W_</sup> _ηk_ where _ηk_ is the context error. The boundary cycle (Eq. 9) refreshes context at a one-time cost _δq_ , so _ηk_ +1 _≤ Wε_ + _α_<sup>_W_</sup> _ηk_ + _δq_ converges to _η_<sup>_∗_</sup> = ( _Wε_ + _δq_ ) _/_ (1 _− α_<sup>_W_</sup> ); see Appendix C. 

**Remark 1** ( **Role of** _α_ **and choice of** _W_ ) **.** _Smaller W tightens the within-segment term Wε but pays more δq per refresh; larger W leaves more room for within-segment drift. An asymptotic analysis of Eq. 10 (Corollary 1 in Appendix C) predicts that the optimal window grows logarithmically in δq/ε and in_ 1 _/_ ( _−_ ln _α_ ) _, i.e. more local drift or cheaper refresh both push W_<sup>_∗_</sup> _larger. Our ablation (Table 3) shows W_ =6 _hits the best balance, consistent with this prediction for our operating regime._ 

## **4 Experiments** 

**Datasets.** We evaluate ROBOALIGN-R1 on RT-1 [38] and BridgeData V2 [39] in the main rollout experiments. RobotWorldBench draws candidate tasks and videos from four robot datasets, including RT-1, BridgeData V2, CALVIN [40], and LIBERO [41], and uses 10,000 annotated video–instruction pairs for judge training and reward distillation. 

**Baselines.** We compare ROBOALIGN-R1 with three groups of approaches: closed-source video generation models, open-source video generation models, and embodied world models. Additional details are deferred to the Table 26. 

**Evaluation Metrics.** We report both semantic/physical alignment metrics and pixel-level reconstruction metrics. The former are scored by ROBOALIGN-JUDGE over six dimensions and should be interpreted as an in-domain automated proxy rather than a substitute for large-scale human evaluation. We additionally report an external VLM-based cross-check and a small-scale blinded human study on held-out subsets to test whether the main ranking is preserved beyond the in-domain judge (Appendix J.7 and Appendix J.8). The pixel-level metrics include standard global measures and motion-mask-based ROI metrics; details are provided in Appendix I. 

**Implementation Details.** ROBOALIGN-R1 is implemented in PyTorch, and all training and evaluation are conducted on NVIDIA A100 GPUs. In the RL stage, we adopt GRPO and distill the fine-tuned RoboAlign-Judge into a lightweight reward model. 

### **4.1 RQ1: Does RoboAlign-R1 Achieve State-of-the-Art World-Model Quality?** 

**Quantitative results.** Tables 1–2 show that ROBOALIGN-R1 achieves the best overall performance under our evaluation protocol. It reaches an aggregate ROBOALIGN-JUDGE score of **8** _._ **52** _±_ 0 _._ 15, exceeding the strongest baseline iVideoGPT (7 _._ 74 _±_ 0 _._ 62) by +10 _._ 1% with 75 _._ 8% lower standard 

6 

deviation, while improving all six judged dimensions and surpassing all closed-source commercial models (e.g., Kling 2.6: 6 _._ 84) despite far fewer parameters. On low-level metrics, ROBOALIGNR1 is also strongest on both datasets, reducing LPIPS by 4 _._ 9% on RT-1 and MSE by 8 _._ 7% on BridgeData V2 relative to the respective runners-up. The main ranking is preserved by the external VLM-based validation (Appendix J.7) and the blinded human study (Appendix J.8). 

**Qualitative analysis.** Figures 4–5 show representative comparisons. ROBOALIGN-R1 produces more coherent manipulation sequences with accurate grasping and stable contact geometry. In contrast, iVideoGPT often produces blurry details, while Wan2.2-TI2V-5B (LoRA) struggles with temporal coherence and occasionally hallucinates object deformation. Across RT-1 and BridgeData V2, ROBOALIGN-R1 better preserves texture, shadows, and background stability, consistent with the quantitative gains above. 

Table 1: Robot world-model performance on ROBOTWORLDBENCH (mean _±_ std.). 

|Method||Task Alignment|||Physical Realism||Total|
|---|---|---|---|---|---|---|---|
||Instr. _↑_|Manip. _↑_|Act.-Out. _↑_|Temp. _↑_|Contact_↑_|Phys. _↑_|_↑_|
|_Real videos_|3.0|2.0|1.0|1.0|1.0|2.0|10.0|
|**_Closed video models_**||||||||
|Kling 2.6<br>|**2.42**_±_0_._09<sup>3</sup>|**1.38**_±_0_._10<sup>3</sup>|0.46_±_0_._08|**0.58**_±_0_._07<sup>3</sup><br>|0.82_±_0_._06|1.18_±_0_._11|**6.84**_±_0_._22<sup>3</sup><br>|
|Runway Gen-4.5|2.34_±_0_._10|1.29_±_0_._09|0.43_±_0_._07|0.55_±_0_._08|0.79_±_0_._06|1.12_±_0_._10|6.52_±_0_._24|
|MiniMax Hailuo 02<br>Luma Dream Machine|2.18_±_0_._11<br>2.03_±_0_._12|1.17_±_0_._10<br>1.08_±_0_._11|0.38_±_0_._07<br>0.35_±_0_._08|0.47_±_0_._09<br>0.44_±_0_._09|0.71_±_0_._08<br>0.69_±_0_._08|1.01_±_0_._12<br>0.92_±_0_._12|5.92_±_0_._28<br>5.51_±_0_._30|
|**_Open video models_**||||||||
|HunyuanVideo-I2V|1.20_±_0_._28|0.40_±_0_._22|0.24_±_0_._08<br>|0.56_±_0_._15|**0.96**_±_0_._08<sup>3</sup>|**1.56**_±_0_._15<sup>2</sup>|4.92_±_0_._63|
|LTX-Video|2.28_±_0_._07|1.32_±_0_._07|**0.52**_±_0_._07<sup>3</sup>|0.26_±_0_._05|0.28_±_0_._10|1.00_±_0_._18|5.66_±_0_._36|
|Stable Video Diffusion XT|1.84_±_0_._15|0.98_±_0_._13|0.46_±_0_._08|0.06_±_0_._08|0.36_±_0_._20|0.58_±_0_._20|4.28_±_0_._74|
|Mochi-1|1.83_±_0_._12|0.91_±_0_._10|0.31_±_0_._07|0.39_±_0_._08|0.61_±_0_._07|0.82_±_0_._11|4.87_±_0_._29|
|I2VGen-XL|1.56_±_0_._15|0.66_±_0_._14|0.32_±_0_._04|0.00_±_0_._00|0.44_±_0_._19|0.56_±_0_._16|3.54_±_0_._57|
|CogVideoX-I2V|1.94_±_0_._21|1.00_±_0_._14|0.40_±_0_._18|0.42_±_0_._16|0.92_±_0_._07|1.24_±_0_._19|5.92_±_0_._75|
|OpenSora-I2V<br>OpenSora-Plan-I2V|1.58_±_0_._13<br>1.79_±_0_._12|0.82_±_0_._11<br>0.89_±_0_._10|0.27_±_0_._06<br>0.30_±_0_._07|0.31_±_0_._07<br>0.37_±_0_._08|0.53_±_0_._08<br>0.60_±_0_._08|0.71_±_0_._10<br>0.81_±_0_._11|4.22_±_0_._30<br>4.76_±_0_._29|
|**_Embodied / interactive worl_**|**_d-model baseli_**|**_nes_**||||||
|RLVR-World|2.29_±_0_._10<br>|1.31_±_0_._09<br>|0.44_±_0_._07<br>|0.43_±_0_._08<br>|0.84_±_0_._06|1.19_±_0_._10<br>|6.54_±_0_._23<br>|
|iVideoGPT<br>RoboDreamer|**2.60**_±_0_._11<sup>2</sup><br>2.02_±_0_._16|**1.60**_±_0_._11<sup>2</sup><br>1.02_±_0_._16|**0.70**_±_0_._11<sup>2</sup><br>0.34_±_0_._05|**0.74**_±_0_._14<sup>2</sup><br>0.32_±_0_._12|0.56_±_0_._10<br>0.04_±_0_._05<br>|**1.54**_±_0_._15<sup>3</sup><br>0.70_±_0_._17|**7.74**_±_0_._62<sup>2</sup><br>4.44_±_0_._56|
|Vid2World|2.18_±_0_._10|1.08_±_0_._04|0.40_±_0_._09|0.22_±_0_._07|**0.98**_±_0_._04<sup>2</sup>|1.04_±_0_._14|5.90_±_0_._30|
|**_Additional training baselin_**|**_es_**|||||||
|Wan2.2-TI2V-5B (LoRA)|2.40_±_0_._09|1.02_±_0_._11|0.41_±_0_._08|0.24_±_0_._10|**0.98**_±_0_._05<sup>2</sup>|0.96_±_0_._12|6.01_±_0_._24|
|**ROBOALIGN-R1 (ours)**|**2.72**_±_0_._06<sup>1</sup>|**1.72**_±_0_._07<sup>1</sup>|**0.72**_±_0_._05<sup>1</sup>|**0.78**_±_0_._05<sup>1</sup>|**1.00**_±_0_._04<sup>1</sup>|**1.58**_±_0_._07<sup>1</sup>|**8.52**_±_0_._15<sup>1</sup>|


Table 2: Low-level metrics on full variable-length rollouts over RT-1 and BridgeData V2. We report mean values and, when available, standard deviations across repeated evaluations over the full generated rollout. 

|Method||RT|-1|||Bridge|Data V2||
|---|---|---|---|---|---|---|---|---|
||MSE_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|MSE_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|
|_Real videos_|0.000|—|1.000|0.000|0.000|—|1.000|0.000|
|**_Embodied / interactive wo_**|**_rld-model baselines_**<br>||||||||
|RLVR-World<br>iVideoGPT<br>RoboDreamer<br>Vid2World|**0.0125**_±_0_._0017<sup>2</sup><br>**0.0128**_±_0_._0018<sup>3</sup><br>0.0171_±_0_._0024<br>0.0138_±_0_._0019|**19.47**_±_1_._30<sup>2</sup><br>**19.36**_±_1_._32<sup>3</sup><br>18.12_±_1_._56<br>19.03_±_1_._37|**0.736**_±_0_._035<sup>2</sup><br>**0.732**_±_0_._036<sup>3</sup><br>0.671_±_0_._046<br>0.721_±_0_._038|**0.182**_±_0_._014<sup>2</sup><br>**0.188**_±_0_._015<sup>3</sup><br>0.231_±_0_._019<br>0.196_±_0_._016|**0.0139**_±_0_._0021<sup>2</sup><br>0.0438_±_0_._0025<br>0.0184_±_0_._0027<br>0.0145_±_0_._0022|**19.06**_±_1_._38<sup>2</sup><br>15.98_±_1_._52<br>17.86_±_1_._69<br>18.92_±_1_._43|**0.721**_±_0_._040<sup>2</sup><br>0.558_±_0_._042<br>0.649_±_0_._051<br>0.711_±_0_._041|**0.178**_±_0_._014<sup>2</sup><br>0.435_±_0_._021<br>0.224_±_0_._018<br>0.188_±_0_._015|
|**_Additional training baseli_**|**_nes_**||||||||
|Wan2.2-TI2V-5B (LoRA)|0.0131_±_0_._0018|19.31_±_1_._29|0.729_±_0_._037|0.184_±_0_._015|**0.0141**_±_0_._0021<sup>3</sup>|**19.02**_±_1_._39<sup>3</sup>|**0.718**_±_0_._040<sup>3</sup>|**0.182**_±_0_._014<sup>3</sup>|
|**ROBOALIGN-R1 (ours)**|**0.0121**_±_0_._0016<sup>1</sup>|**19.72**_±_1_._26<sup>1</sup>|**0.745**_±_0_._032<sup>1</sup>|**0.173**_±_0_._013<sup>1</sup>|**0.0127**_±_0_._0019<sup>1</sup>|**20.00**_±_1_._31<sup>1</sup>|**0.731**_±_0_._037<sup>1</sup>|**0.175**_±_0_._013<sup>1</sup>|


### **4.2 RQ2: Do Distilled Multimodal Rewards Outperform Low-Level Alternatives?** 

We compare the distilled multimodal student reward with low-level alternatives under matched RL post-training settings. Figure 6(a) shows that the student reward performs best on all six semantic and physical dimensions on ROBOTWORLDBENCH, reaching the highest aggregate score (8 _._ 52, +33 _._ 8% 

7 


Figure 4: **Qualitative comparison on a representative manipulation case.** ROBOALIGN-R1 generates physically coherent sequences with accurate grasping. 


Figure 5: **Qualitative case study of ROBOALIGN-R1 on RT-1 and BridgeData V2** , showing improved texture, shadow consistency, and background stability. 


Figure 6: **Reward-type ablation for RL post-training on ROBOTWORLDBENCH** . Panel (a) shows that the distilled student reward yields the strongest judge-aligned improvement across semantic and physical dimensions. Panels (b)–(e) show that it also delivers the best full-rollout low-level metrics on RT-1 and BridgeData V2. 

over the best single-metric reward baseline, LPIPS). Figure 6(b)–(e) further shows that it also yields the best full-rollout low-level metrics on both RT-1 and BridgeData V2. Overall, the distilled reward is better aligned with our in-domain evaluator and remains beneficial to pixel fidelity. 

### **4.3 RQ3: Does SWR Improve Long-Horizon Quality Without Heavy Overhead?** 

We compare SWR with default autoregressive (AR) decoding on RT-1. Table 3(a) shows that SWR with _W_ =6 improves long-horizon generation quality, yielding +2 _._ 8% SSIM, +0 _._ 62 dB PSNR, and _−_ 9 _._ 8% LPIPS. The gains are larger in the region of interest, where ROI-LPIPS drops by _−_ 12 _._ 2%. These results are consistent with SWR reducing accumulated drift by periodically refreshing the 

8 

Table 3: **SWR empirical summary** on RT-1. **(a)** Default autoregressive decoding vs. SWR with _W_ =6 (mean _±_ std.; ∆ vs. Default AR). **(b)** Total wall-clock time vs. _W_ and per-frame latency on a keyframe subsample. 


Figure 7: **Qualitative effect of SWR.** SWR mitigates error accumulation and maintains visual fidelity in long-horizon generation by periodically re-encoding recent context. 

context (Figure 7), and _W_ =6 provides the best quality–efficiency trade-off among the tested window sizes. These gains come with only modest overhead. Table 3(b) shows that SWR keeps total inference time (5 _._ 709 s vs. 5 _._ 646 s) and throughput (5 _._ 26 FPS vs. 5 _._ 31 FPS) close to AR, with about 1 _._ 1% extra wall-clock time. SWR also bounds KV-cache growth to _O_ ( _W_ ), reducing maximum sequence length by 54 _._ 8% and peak memory by 4 _._ 2%. As a result, SWR maintains a near-flat per-frame latency profile, whereas AR shows a +6 _._ 8% latency drift by frame 29. 

### **4.4 RQ4: Does Online Iterative Distillation Help Maintain Reward Alignment?** 

Table 4 shows the effect of online iterative distillaTable 4: **Iterative distillation.** tion under the same student architecture and evaluation protocol. Online iterative distillation improves the <mark>Setting Total</mark> _<mark>↑</mark>_ <mark>Manip.</mark> _<mark>↑</mark>_ <mark>LPIPS</mark> _<mark>↓</mark>_ aggregate score from 8 _._ 09 to 8 _._ 52 and _Manipulation_ <mark>One-shot distill 8.09</mark> _<mark>±</mark>_ <mark>0</mark> _<mark>.</mark>_ <mark>23 1.58</mark> _<mark>±</mark>_ <mark>0</mark> _<mark>.</mark>_ <mark>09 0.176</mark> _<mark>±</mark>_ <mark>0</mark> _<mark>.</mark>_ <mark>014</mark> _Success_ from 1 _._ 58 to 1 _._ 72, while slightly improving Online iterative **8.52** _±_ 0 _._ 15<sup><mark>1</mark></sup> **1.72** _±_ 0 _._ 07<sup><mark>1</mark></sup> **0.173** _±_ 0 _._ 013<sup><mark>1</mark></sup> RT-1 LPIPS from 0 _._ 176 to 0 _._ 173. This supports the motivation in Section 3.2: refreshing the student during RL helps maintain reward alignment under distribution shift. 

## **5 Conclusion & Limitation** 

We present ROBOALIGN-R1, a framework that improves robot video world models through rewardaligned post-training and stabilized long-horizon decoding. By constructing a robot-centric benchmark to train a multimodal teacher judge and distilling it into a lightweight student reward model, ROBOALIGN-R1 enables efficient RL post-training that lifts the aggregate in-domain evaluation score by +10 _._ 1% over the strongest baseline under our current protocol, with the overall ranking further supported by external VLM-based validation and a small-scale blinded human study; the proposed sliding window re-encoding further yields +2 _._ 8% SSIM and _−_ 9 _._ 8% LPIPS gains at about 1% additional latency. Our current evaluation is still limited to single-arm tabletop and countertop manipulation, and downstream policy improvement remains to be validated. Extending to diverse embodiments, ensembling multiple judges, and measuring control-level gains are promising directions for future work. Code, datasets, models, and video samples are available at the project website. 

9 

## **Acknowledgements** 

This work was supported by the National Natural Science Foundation of China (42125503, 42430602). 

## **References** 

- [1] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2(3):440, 2018. 

- [2] Jingcheng Ni, Yuxin Guo, Yichen Liu, Rui Chen, Lewei Lu, and Zehuan Wu. Maskgwm: A generalizable driving world model with video mask reconstruction. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22381–22391, 2025. 

- [3] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Leo Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, et al. Video generation models as world simulators. _OpenAI Blog_ , 1(8):1, 2024. 

- [4] Wentao Tan, Lei Zhu, Bowen Wang, Enci Xie, Baixu Ji, Zengrong Lin, Wenjie Yang, Jingjing Li, and Heng Tao Shen. Towards generalist embodied ai: A survey on world models for vla agents. _Authorea Preprints_ , 2026. 

- [5] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. _arXiv preprint arXiv:2310.16828_ , 2023. 

- [6] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- [7] Dacheng Li, Yunhao Fang, Yukang Chen, Shuo Yang, Shiyi Cao, Justin Wong, Michael Luo, Xiaolong Wang, Hongxu Yin, Joseph E Gonzalez, et al. Worldmodelbench: Judging video generation models as world models. _arXiv preprint arXiv:2502.20694_ , 2025. 

- [8] Jialong Wu, Shaofeng Yin, Ningya Feng, and Mingsheng Long. Rlvr-world: Training world models with reinforcement learning. _arXiv preprint arXiv:2505.13934_ , 2025. 

- [9] Leonardo Barcellona, Andrii Zadaianchuk, Davide Allegro, Samuele Papa, Stefano Ghidoni, and Efstratios Gavves. Dream to manipulate: Compositional world models empowering robot imitation learning with imagination. _arXiv preprint arXiv:2412.14957_ , 2024. 

- [10] Jing-Cheng Pang, Nan Tang, Kaiyuan Li, Yuting Tang, Xin-Qiang Cai, Zhen-Yu Zhang, Gang Niu, Masashi Sugiyama, and Yang Yu. Learning view-invariant world models for visual robotic manipulation. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [11] Siqiao Huang, Jialong Wu, Qixing Zhou, Shangchen Miao, and Mingsheng Long. Vid2world: Crafting video diffusion models to interactive world models. _arXiv preprint arXiv:2505.14357_ , 2025. 

- [12] Jiageng Mao, Sicheng He, Hao-Ning Wu, Yang You, Shuyang Sun, Zhicheng Wang, Yanan Bao, Huizhong Chen, Leonidas Guibas, Vitor Guizilini, et al. Robot learning from a physical world model. _arXiv preprint arXiv:2511.07416_ , 2025. 

- [13] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng, Yuan Yuan, Hongyuan Su, Nian Li, Nicholas Sukiennik, et al. Understanding world or predicting future? a comprehensive survey of world models. _ACM Computing Surveys_ , 58(3):1–38, 2025. 

- [14] Tianyi Xiong, Shihao Wang, Guilin Liu, Yi Dong, Ming Li, Heng Huang, Jan Kautz, and Zhiding Yu. Phycritic: Multimodal critic models for physical ai. _arXiv preprint arXiv:2602.11124_ , 2026. 

- [15] Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. Efficient streaming language models with attention sinks. _arXiv preprint arXiv:2309.17453_ , 2023. 

- [16] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

10 

- [17] Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. _arXiv preprint arXiv:2310.06114_ , 1 (2):6, 2023. 

- [18] Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. Robodreamer: Learning compositional world models for robot imagination. _arXiv preprint arXiv:2404.12377_ , 2024. 

- [19] Peng-Fei Zhang, Ying Cheng, Xiaofan Sun, Shijie Wang, Fengling Li, Lei Zhu, and Heng Tao Shen. A step toward world models: A survey on robotic manipulation. _arXiv preprint arXiv:2511.02097_ , 2025. 

- [20] Michael Mathieu, Camille Couprie, and Yann LeCun. Deep multi-scale video prediction beyond mean square error. _arXiv preprint arXiv:1511.05440_ , 2015. 

- [21] Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 586–595, 2018. 

- [22] Zhou Wang, Alan C Bovik, Hamid R Sheikh, and Eero P Simoncelli. Image quality assessment: from error visibility to structural similarity. _IEEE transactions on image processing_ , 13(4): 600–612, 2004. 

- [23] Mihir Prabhudesai, Russell Mendonca, Zheyang Qin, Katerina Fragkiadaki, and Deepak Pathak. Video diffusion alignment via reward gradients. _arXiv preprint arXiv:2407.08737_ , 2024. 

- [24] Anonymous. Spatiotemporal forecasting as planning: A model-based reinforcement learning approach with generative world models. _Under review as a conference paper at ICLR 2026_ , 2026. 

- [25] Hao Wu, Xingjian Shi, Ziyue Huang, Penghao Zhao, Wei Xiong, Jinbao Xue, Yangyu Tao, Xiaomeng Huang, and Weiyan Wang. Beamvq: aligning space-time forecasting model via self-training on physics-aware metrics. _arXiv preprint arXiv:2405.17051_ , 2024. 

- [26] Weiyan Wang, Xingjian Shi, Ruiqi Shu, Yuan Gao, Rui Ray Chen, Kun Wang, Fan Xu, Jinbao Xue, Shuaipeng Li, Yangyu Tao, et al. Beamvq: Beam search with vector quantization to mitigate data scarcity in physical spatiotemporal forecasting. _arXiv preprint arXiv:2502.18925_ , 2025. 

- [27] Suman Ravuri, Karel Lenc, Matthew Willson, Dmitry Kangin, Remi Lam, Piotr Mirowski, Megan Fitzsimons, Maria Athanassiadou, Sheleem Kashem, Sam Madge, et al. Skilful precipitation nowcasting using deep generative models of radar. _Nature_ , 597(7878):672–677, 2021. 

- [28] Chelsea Finn, Ian Goodfellow, and Sergey Levine. Unsupervised learning for physical interaction through video prediction. _Advances in neural information processing systems_ , 29, 2016. 

- [29] Wilson Yan, Yunzhi Zhang, Pieter Abbeel, and Aravind Srinivas. Videogpt: Video generation using vq-vae and transformers. _arXiv preprint arXiv:2104.10157_ , 2021. 

- [30] Jialong Wu, Shaofeng Yin, Ningya Feng, Xu He, Dong Li, Jianye Hao, and Mingsheng Long. ivideogpt: Interactive videogpts are scalable world models. _Advances in Neural Information Processing Systems_ , 37:68082–68119, 2024. 

- [31] Yunbo Wang, Haixu Wu, Jianjin Zhang, Zhifeng Gao, Jianmin Wang, Philip S Yu, and Mingsheng Long. Predrnn: A recurrent neural network for spatiotemporal predictive learning. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 45(2):2208–2225, 2022. 

- [32] Ziqi Huang, Yinan He, Jiashuo Yu, Fan Zhang, Chenyang Si, Yuming Jiang, Yuanhan Zhang, Tianxing Wu, Qingyang Jin, Nattapol Chanpaisit, et al. Vbench: Comprehensive benchmark suite for video generative models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 21807–21818, 2024. 

11 

- [33] Xuan He, Dongfu Jiang, Ge Zhang, Max Ku, Achint Soni, Sherman Siu, Haonan Chen, Abhranil Chandra, Ziyan Jiang, Aaran Arulraj, et al. Videoscore: Building automatic metrics to simulate fine-grained human feedback for video generation. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ , pages 2105–2123, 2024. 

- [34] Tianyi Xiong, Xiyao Wang, Dong Guo, Qinghao Ye, Haoqi Fan, Quanquan Gu, Heng Huang, and Chunyuan Li. Llava-critic: Learning to evaluate multimodal models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 13618–13628, 2025. 

- [35] Fabian Mentzer, David Minnen, Eirikur Agustsson, and George Toderici. Finite scalar quantization: VQ-VAE made simple. In _International Conference on Learning Representations_ , 2024. 

- [36] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2.5-VL technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- [37] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Mingchuan Zhang, YK Li, Y Wu, and Daya Guo. DeepSeekMath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [38] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gober, Karol Hausman, Alexander Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2023. 

- [39] Homer Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe HansenEstruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. _arXiv preprint arXiv:2308.12952_ , 2023. 

- [40] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. CALVIN: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. In _IEEE Robotics and Automation Letters_ , volume 7, pages 7327–7334, 2022. 

- [41] Bo Liu, Yifeng Zhu, Chongkai Gao, Yizhou Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems_ , volume 36, 2024. 

- [42] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Liang Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _Iclr_ , 1(2):3, 2022. 

12 

## **Appendix Contents** 

|A **Extended Related Work**_. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 14|
|---|
|B **Training Details of the Video World Model** _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 15|
|B.1 Notation _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 15|
|B.2 Stage 1: Context-Aware Compression Tokenizer _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 15|
|B.3 Stage 2: Autoregressive Transformer World Model _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 17|
|B.4 Dataset: Bridge V2 Instantiation _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 19|
|B.5 Reproduction Protocol_. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 20|
|B.6 Optimization Infrastructure _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 21|
|B.7 End-to-End Quantitative Summary _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 22|
|B.8 TensorBoard Training Curves _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 22|
|C **Stylized derivation for Proposition 1** _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 27|
|D **Pseudocode for Reward-Aligned Post-Training**_. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 30|
|E **Student Reward Model Details** _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 31|
|F **Pseudocode and Implementation of Sliding Window Re-encoding** _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 34|
|G **SWR window-size ablation** _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 36|
|H **SWR qualitative visualizations** _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 38|
|I **Evaluation Metrics** _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 42|
|I.1 Semantic and Physical Alignment Metrics_. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 42|
|I.2 Pixel-Level Reconstruction Metrics_. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 42|
|I.3 Motion-Mask-Based ROI Metrics _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 42|
|J **ROBOALIGN-JUDGE: Multimodal Teacher Judge Training Details** _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 44|
|J.1 Motivation and Design Rationale _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 44|
|J.2 Training Data Construction_. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 44|
|J.3 Six-Dimension Scoring Rubric _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 48|
|J.4 Model Architecture and LoRA Fine-Tuning _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 48|
|J.5 Chain-of-Thought Reasoning _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 49|
|J.6 From Teacher Judge to Reward Signal _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 50|
|J.7 Comparison with Alternative VLM Judges _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 50|
|J.8 Small-scale Blinded Human Evaluation _. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 53|
|J.9 Comparison with Alternative Judge Backbones_. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 54|
|J.10 Limitations and Future Directions_. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 54|
|J.11 Judge Prompt Templates_. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ._ 54|


13 

## **A Extended Related Work** 

**Robot Video World Models.** World models provide learnable internal simulators for planning, policy evaluation, and long-horizon decision making by predicting how environments evolve under candidate actions [1, 5]. With the rise of video generation and embodied learning, recent work has increasingly explored video-based world models for robotics, including approaches that model manipulation dynamics, interaction outcomes, and future observations through video prediction or generative simulation [3, 16, 17, 18, 11, 12]. These studies highlight the promise of video world models for embodied intelligence, but most still emphasize generation quality, dynamics modeling, or representation learning, and are largely trained with maximum-likelihood or reconstruction-style objectives [19, 13]. In contrast, our work focuses on reward-aligned post-training for robot video world models. 

**RL Post-Training for World Models.** Recent work has begun to explore reinforcement learning as a post-training mechanism for world models, showing that world-model behavior can be further aligned with downstream objectives beyond standard supervised fitting [8, 23, 24]. However, existing approaches still rely mainly on low-level or verifiable rewards, such as pixel reconstruction error or perceptual similarity metrics [8, 20, 25, 21, 22, 26]. While these rewards are stable and easy to compute, they remain weak proxies for the properties that matter in robot prediction, such as correct instruction execution, physically plausible contact dynamics, and consistent long-horizon action outcomes. Similar limitations have also been observed in physical spatiotemporal forecasting [27, 28], where optimizing average reconstruction objectives often leads to oversmoothed predictions and poor coverage of rare but decision-critical events [26, 24]. Long-horizon rollout quality is also shaped by inference-time generation strategy: in autoregressive token-based world models [29, 15, 30, 31], prediction errors can accumulate over time and progressively degrade later predictions. Our work therefore complements reward-aligned post-training with a simple decoding strategy for stabilizing long-horizon rollouts. 

**Multimodal Judges and Rewards.** Another relevant line of research studies multimodal evaluators and reward models for video understanding and generation [32, 33, 34]. Prior work shows that multimodal judges can provide richer supervision than low-level visual metrics by explicitly assessing instruction following, physical plausibility, and higher-level video consistency [7, 14, 32, 33]. Such evaluators are much better aligned with human judgment, but their inference cost and latency make them difficult to use directly as online rewards in reinforcement learning [7, 33, 14]. Our method is closely related in spirit to this line of work, but differs in two important ways: we focus on robot video world models rather than general video evaluation, and we distill high-capacity multimodal judgment into a lightweight reward model that is practical for online RL. This makes multimodal reward supervision not only evaluative, but directly usable for post-training robot world models. 

14 

## **B Training Details of the Video World Model** 

This appendix details the implementation of the two-stage video world model used as the backbone throughout our experiments. Stage 1 trains a context-aware compression tokenizer that maps raw robot video clips into discrete index sequences; on top of a frozen Stage 1 tokenizer, Stage 2 trains an autoregressive Transformer that jointly models visual and action tokens. The two stages share the same clip length, spatial resolution, and data pipeline, and communicate exclusively through discrete tokens. 

### **B.1 Notation** 

Unless stated otherwise, the symbols in Table 5 are shared between both stages. 

Table 5: Symbols shared between Stage 1 and Stage 2. 

|Symbol|Meaning|Value|
|---|---|---|
|_T_|Clip length (frames)|8|
|_tc_|Context frames|1|
|_td_ = _T −tc_|Dynamic frames|7|
|_H × W_|Spatial resolution|256_×_320|
|_p_|Dynamic-branch patch size|4|
|_D_|FSQ quantization dimension|5|
|**L**|FSQ level vector|(7_,_5_,_5_,_5_,_5)|
|_K_ = <sup>�</sup><br>_i _<sup>_Li_</sup>|Codebook size|4375|
|_Nc_|Context tokens per clip|1280|
|_Nd_|Dynamic tokens per frame|80|
|_Da_|Action-vector dimensionality (Bridge V2)|13|
|_Ba_|Per-dimension action bins|256|
|_V_|Joint vocabulary size (Stage 2)|9008|
|_S_|Transformer sequence length (Stage 2)|1931|
|_ϕl_|VGG-16 feature map at layer_l_(LPIPS)|—|


### **B.2 Stage 1: Context-Aware Compression Tokenizer** 

Stage 1 compresses a clip _{xt}_<sup>_T_</sup> _t_ =1<sup>_∈_R</sup><sup>_T ×_3</sup><sup>_×H×W_into 1840 discrete indices using two asymmetric</sup> branches: a _Full VAE_ over the context frame _xc_ := _x_ 1 and a _Conditional VAE_ over the dynamic frames _xd_ := _{xt}_<sup>_T_</sup> _t_ =2<sup>.Quantization is carried out by Finite Scalar Quantization (FSQ); no learnable</sup> codebook is used. 

**Architecture.** The _context branch_ uses a convolutional encoder _Ec_ that produces a latent feature map together with an intermediate feature pyramid _{fl_<sup>(</sup><sup>_E_)</sup> _}_<sup>_L_</sup> _l_ =1<sup>:</sup> 


A 1 _×_ 1 convolution projects _h_ into the quantization space, _zc_ = QuantConv( _h_ ) _∈_ R<sup>5</sup><sup>_×_32</sup><sup>_×_40</sup> . No spatial patchification is applied, so this branch emits _Nc_ = 32 _·_ 40 = 1280 tokens, each covering an 8 _×_ 8 pixel block of the input. 

The _dynamic branch_ uses a conditional encoder _Ed_ whose downsampling stages are interleaved with cross-attention layers that inject the context feature pyramid, 


so that _Ed_ encodes only the residual dynamics relative to the static context. Its output _d_<sup>_′_</sup> _∈_ R<sup>64</sup><sup>_×_32</sup><sup>_×_40</sup> is patchified with _p_ = 4 and linearly projected, 


producing _Nd_ = 80 tokens per dynamic frame, each covering a 32 _×_ 32 pixel block. 

15 

**FSQ quantization.** For a vector _z ∈_ R<sup>_D_</sup> with _D_ = 5 and **L** = (7 _,_ 5 _,_ 5 _,_ 5 _,_ 5), FSQ performs per-dimension bounding, straight-through rounding, and mixed-radix encoding: 


Because the index set is analytically fixed by **L** and every codeword is reachable by construction, no commitment loss is required. 

**Decoding.** Symmetric decoders _Dc_ and _Dd_ reconstruct the clip, 

_x_ ˆ _c_ = _Dc_ �PostQuantConv( _Q_ ( _zc_ ))� _, x_ ˆ _d_ = _Dd_ �UnPatchify(PostQuantLinear( _Q_ ( _zd_ ))); _{fl_<sup>(</sup><sup>_D_)</sup> _}_ � _,_ 

with cross-attention inserted at every upsampling stage of _Dd_ to read the decoder-side feature pyramid _{fl_<sup>(</sup><sup>_D_)</sup> _}_ of _Dc_ . _No skip connection bypasses the quantization bottleneck_ : the decoders depend solely on the discrete indices. Each clip therefore carries _Nc_ + _td · Nd_ = 1280 + 7 _·_ 80 = 1840 tokens, corresponding to a compression ratio of roughly 1070 _×_ relative to the 8 _·_ 3 _·_ 256 _·_ 320 = 1 _,_ 966 _,_ 080 raw pixel values. 

**End-to-end data flow.** Figure 8 summarizes the Stage 1 forward pipeline, making explicit how the two branches share the context feature pyramid yet quantize independently through FSQ, and how the decoders reconstruct the clip from discrete indices alone. 


Figure 8: **End-to-end data flow of the Stage 1 tokenizer.** The context frame _xc_ passes through a Full VAE and is quantized into 1280 context tokens at 8 _×_ 8 granularity; the 7 dynamic frames _xd_ pass through a Conditional VAE whose encoder and decoder are cross-attention-conditioned on the context feature pyramids _{fl_<sup>(</sup><sup>_E_)</sup> _}_ and _{fl_<sup>(</sup><sup>_D_)</sup> _}_ (dashed arrows), producing 560 dynamic tokens at 32 _×_ 32 granularity. FSQ uses a shared codebook of size _K_ = 4 _,_ 375 without any commitment loss, and both decoders depend solely on the discrete indices – no skip connection bypasses the quantization bottleneck. 

**Training objective.** Let _x_ ˆ := [ˆ _xc_ ; _x_ ˆ _d_ ]. The generator loss combines reconstruction, perceptual, and adversarial terms, 


16 

with 


where _ϕl_ denotes ImageNet-pretrained VGG-16 features with LPIPS linear weights _{wl}_ . The discriminator _Dψ_ is a depth-6 PatchGAN trained with the hinge objective and an _R_ 1-style gradient penalty, 

_LD_ = E�max(0 _,_ 1 + _Dψ_ (ˆ _x_ ))� + E�max(0 _,_ 1 _− Dψ_ ( _x_ ))� + _γ_ E _x_ �( _∥∇xDψ_ ( _x_ ) _∥_ 2 _−_ 1)<sup>2�</sup> _._ 

The adversarial term is disabled for the first _T_ adv = 10 _,_ 000 steps; thereafter _G_ and _D_ are updated alternately under a shared global-step counter. 

**Data and augmentation.** Training follows the Open X-Embodiment (OXE) mixed-dataset protocol, with mixing weights proportional to the sample counts of each sub-dataset; the numbers reported in this appendix are obtained on the Bridge V2 subset for reproducibility. For each trajectory we sample a start index uniformly and extract a clip of length _T_ = 8 with stride 1. Photometric and geometric augmentations are sampled once per clip and shared across all _T_ frames (Table 6). 

Table 6: Clip-wise augmentation ranges used by the Stage 1 tokenizer. 

|Augmentation|Range|
|---|---|
|Brightness / contrast / saturation|[0_._9_,_ 1_._1]|
|Hue|[_−_0_._05_,_ 0_._05]|
|`RandomResizedCrop`scale|[0_._8_,_ 1_._0]|
|`RandomResizedCrop`aspect ratio|[1_._0_,_ 1_._4]|


**Hyperparameters.** Table 7 lists the Stage 1 hyperparameters. Generator components, discriminator components, and validation-set metrics are logged as separate TensorBoard scalar groups. Validation is run every 1 _,_ 000 steps over 100 batches, reporting mean L1 and LPIPS together with a few reconstruction visualizations. 

Table 7: Stage 1 tokenizer hyperparameters. 

|Item|Value|
|---|---|
|Resolution_H × W_|256_×_320|
|Clip length_T_ / context_tc_|8_/_1|
|Context latent channels_Ch_|256|
|Dynamic latent channels|64|
|Patch size_p_|4|
|FSQ(_D,_**L**_, K_)|(5_,_ (7_,_5_,_5_,_5_,_5)_,_ 4375)|
|Tokens per clip|1280 + 7_×_80 = 1840|
|Discriminator depth|6|
|Reconstruction loss|L1|
|Loss weights(_λr, λp, λa_)|(1_._0_,_ 1_._0_,_ 0_._1)|
|Gradient-penalty coefficient_γ_|10|
|Adversarial start step_T_adv|10_,_000<br>|
|Optimizer|AdamW,(_β_1_, β_2_, ε_)=(0_._9_,_0_._999_,_10<sup>_−_8</sup>), weight decay0|
|Learning rate (_G_/_D_)|5_×_10<sup>_−_4 </sup>/5_×_10<sup>_−_4</sup>|
|LR schedule (_G_/_D_)|cosine / constant-with-warmup, warmup5_,_000steps|
|Gradient clipping|_∥∇∥_2 _≤_1_._0|
|Mixed precision|bf16|
|Gradient checkpointing|enabled|
|Per-GPU batch / accumulation|1_/_4|
|GPUs|8_×_A100-40GB|
|Global effective batch|32|
|Total training steps|60_,_000|
|Checkpoint / validation frequency|every2_,_000/1_,_000steps|


### **B.3 Stage 2: Autoregressive Transformer World Model** 

Stage 2 trains a causal Transformer _πθ_ on top of the _frozen_ Stage 1 tokenizer. With **c** _∈ {K, . . . ,_ 2 _K −_ 1 _}_<sup>_Nc_</sup> the context tokens, **d** _t ∈{_ 0 _, . . . , K −_ 1 _}_<sup>_Nd_</sup> the dynamic tokens of frame _t_ , 

17 


**Joint vocabulary.** Visual and action tokens are merged into a single vocabulary of size _V_ via fixed offsets, so that a standard LM head can emit either modality (Table 8). The two visual segments share the same FSQ codebook but are disambiguated by an offset of _K_ , allowing the embedding matrix _WE ∈_ R<sup>_V ×d_</sup> to learn separate embeddings for context and dynamic semantics. 

Table 8: Stage 2 joint vocabulary. 

|Range|Semantics|Size|
|---|---|---|
|[0_, K_)|Dynamic visual tokens (FSQ indices of_Ed_)|_K_ = 4375|
|[_K,_ 2_K_)|Context visual tokens (FSQ indices of_Ec_, offset by_K_)|_K_ = 4375|
|[2_K,_ 2_K_ +_Ba_)|Action tokens|_Ba_ = 256|
|_{_2_K_ +_Ba}_|BOS (reserved)|1|
|_{_2_K_ +_Ba_ + 1_}_|EOS (reserved)|1|
|**Total**_V_||**9008**|


**Action discretization.** Each dimension of **a** _t ∈_ R<sup>_Da_</sup> is independently mapped into _Ba_ = 256 equal-width bins. The per-dimension lower and upper bounds ( _a_<sup>min</sup> _i , a_<sup>max</sup> _i_ ) are pre-computed on the training split and persisted as an offline lookup table shared between training and inference: 


where **a** _T_ is filled with the action associated with the last transition. The total sequence length is 

_S_ = _Nc_ + _td ·_ ( _Nd_ + _Da_ ) = 1280 + 7 _·_ (80 + 13) = 1931 _._ 

The label sequence has the same shape as **x** ; all positions except the dynamic tokens of frames 2 _, . . . , T_ are set to the ignore index and excluded from the cross-entropy loss (Table 9). The number of supervised positions per sample is 


Since a single causal forward pass simultaneously supervises the predictions of frames 2 _, . . . , T_ , this objective is equivalent to _td −_ 1 = 6 one-step next-frame prediction subtasks that share attention compute, i.e. multi-step prediction (MSP). 

Table 9: Loss-mask layout of a single Stage 2 sample. 

|Segment|Label|
|---|---|
|Context tokens (_Nc_ = 1280)|_−_100(condition)|
|Dynamic tokens at frame 1 (_Nd_ = 80)|_−_100(initial state)|
|Dynamic tokens at frames2:_T_ (6_·_80 = 480)|ground-truth token ids|
|All action tokens (7_·_13 = 91)|_−_100(condition)|


**Backbone.** _πθ_ is a causal LLaMA configured as in Table 10. The causal mask is realized inside the FlashAttention-2 kernel; weights, activations, and gradients are all stored in bf16, since FlashAttention-2 is incompatible with fp32. 

**Training objective.** Let _hi−_ 1 _∈_ R<sup>_d_</sup> denote the last-layer hidden state at position _i−_ 1 and _WO ∈_ R<sup>_d×V_</sup> the LM head, so that 

_pθ_ ( _xi | x<i_ ) = �softmax( _WO hi−_ 1)� _xi_<sup>_._</sup> 

The training loss is the causal cross-entropy restricted to the supervised positions _M_ , 


and the perplexity PPL = exp( _L_ VGPT) _∈_ [1 _, V_ ] serves as an interpretable monitoring metric. 

18 

Table 10: Stage 2 Transformer backbone. 

|Component|Value|
|---|---|
|Layers|12|
|Hidden size_d_|768|
|Attention heads|12(no GQA)|
|FFN size|3072|
|Activation|SwiGLU<br>|
|Normalization|RMSNorm,_ε_ = 10<sup>_−_6</sup>|
|Positional encoding|RoPE|
|Max positions|8192|
|Tied word embeddings|disabled|
|Parameters (incl. embeddings)|_≈_1_._38_×_10<sup>8</sup>|
|Attention kernel|FlashAttention-2|
|Compute precision|bf16|


**Tokenization during training.** Tokenization is performed inside the data pipeline with all Stage 1 parameters frozen and detached from the computation graph: 


followed by the offsetting and concatenation above. The Transformer therefore only ever consumes integer token ids, and gradients flow exclusively through _πθ_ . 

**Hyperparameters.** Stage 2 hyperparameters are summarized in Table 11. Validation computes _L_ VGPT and PPL on a held-out split every 5 _,_ 000 steps. At inference, autoregressive sampling uses temperature _τ_ = 1 _._ 0 with top- _k_ and top- _p_ truncation; beam search is not used. 

Table 11: Stage 2 autoregressive Transformer hyperparameters. 

|Item|Value|
|---|---|
|Backbone|LLaMA-12L-768d-12h (FlashAttention-2, bf16)|
|Vocabulary size_V_|9008|
|Sequence length_S_|1931(max positions8192)|
|Supervised positions_|M|_|480|
|Frozen tokenizer|Stage 1 checkpoint at60_,_000steps|
|Data module|Context + MSP processor<br>|
|Optimizer|AdamW,(_β_1_, β_2_, ε_)=(0_._9_,_0_._999_,_10<sup>_−_8</sup>), weight decay0<br>|
|Learning rate|5_×_10<sup>_−_5</sup>|
|LR schedule|constant-with-warmup, warmup5_,_000steps|
|Gradient clipping|_∥∇∥_2 _≤_1_._0|
|Dropout / stochastic depth|0|
|Per-GPU batch / accumulation|4_/_1|
|GPUs|8_×_A100-40GB|
|Global effective batch|32|
|Max steps_T_max|1_,_000_,_000|
|Checkpoint / validation frequency|every10_,_000/5_,_000steps|


### **B.4 Dataset: Bridge V2 Instantiation** 

The two-stage pipeline is dataset-agnostic and only assumes synchronized image observations paired with low-dimensional action sequences. For reproducibility we instantiate it on **Bridge V2** (Walke _et al._ , 2023) as a representative case; any dataset satisfying the same interface can be substituted without further changes. 

Bridge V2 is a large-scale real-robot manipulation dataset collected with a WidowX-250 six-DoF arm across 24 indoor kitchen and tabletop environments. It contains approximately 60 _,_ 096 humanteleoperated trajectories covering 13 skill categories (grasping, placing, pushing, pulling, opening and closing drawers, flipping, stacking, and so on). Each trajectory logs synchronized third-person RGB, end-effector pose, and gripper state at 5 Hz. The dataset is distributed in the TensorFlow Datasets (TFDS) format; we use version 1 _._ 0 _._ 0. 

19 

**Raw sample structure.** Each raw trajectory is a variable-length sequence with the fields summarized in Table 12, where _L_ is the trajectory length (typically 20–60 frames). The data is distributed as TFRecord shards and split into training and validation partitions. 

Table 12: Core fields of a Bridge V2 trajectory. 

|Field|Shape|Dtype|Description|
|---|---|---|---|
|Primary RGB|(_L,_ 480_,_ 640_,_ 3)|uint8|Third-person primary-camera observation|
|Proprio. state|(_L,_ 7)|float32|End-effector(_x, y, z,_roll_,_pitch_,_yaw_,_gripper)|
|Action|(_L,_ 7)|float32|EE increments(∆_x,_∆_y,_∆_z,_∆roll_,_∆pitch_,_∆yaw_,_gripper_cmd)|
|Language instruction|string|—|Natural-language task description (unused here)|
|Terminal flag|bool|—|Episode-end indicator|


**Pre-processing (TFDS** _→_ **per-trajectory arrays).** The TFDS source is converted offline into per-trajectory array files once, so that the downstream data pipeline does not need to touch TFRecords again: 

- **Image resampling.** 480 _×_ 640 _→ H ×W_ = 256 _×_ 320 via aspect-ratio-preserving resize followed by center cropping, stored as uint8. 

- **Action expansion.** The raw R<sup>7</sup> action is expanded to R<sup>13</sup> by appending several dimensions of the previous end-effector state, matching the shared OXE action layout ( _Da_ = 13). 

- **Action-range statistics.** The training split is scanned once to record per-dimension ( _a_<sup>min</sup> _i , a_<sup>max</sup> _i_ ); the resulting table is persisted and reused by the equal-width binning in §B.3. 

After conversion, each trajectory becomes an independent array file containing an image tensor ( _L,_ 256 _,_ 320 _,_ 3) in uint8, an action tensor ( _L,_ 13) in float32, and a proprioceptive state ( _L,_ 7) in float32. The resulting corpus has _≈_ 60 _,_ 096 trajectories, over 1 _._ 92 M frames, and occupies roughly 260 GB on disk. 

**Sampling and slicing.** Each optimization step samples a clip according to: 

1. Uniformly sample an episode from the training split. 

2. Uniformly sample a start frame _s ∈_ [0 _, L − T_ ]. 

3. Take _{Is, . . . , Is_ + _T −_ 1 _}_ and the paired actions _{as, . . . , as_ + _T −_ 1 _}_ with _T_ = 8 and stride 1. 

4. Apply the clip-wise photometric and geometric augmentations of Table 6, with parameters shared across the _T_ frames to preserve temporal consistency. 

5. Normalize images to [0 _,_ 1] before feeding them to the tokenizer. 

Stage 1 consumes only the pixels _{Is_ + _k}_<sup>_T_</sup> _k_ =0<sup>_−_1; Stage 2 additionally consumes the paired actions to</sup> construct the joint token sequence of §B.3. The two stages share identical sampling and augmentation logic, and differ only in their collate-level outputs. 

### **B.5 Reproduction Protocol** 

We describe the end-to-end reproduction protocol in terms of inputs, computation, and outputs, deliberately avoiding prescriptive script layouts or launch commands. 

**Software environment.** The implementation is built on PyTorch with the version constraints in Table 13. Distributed training uses Accelerate over the NCCL backend; both stages train under bf16 mixed precision to satisfy the dtype constraints of FlashAttention-2. 

**Step 0: Offline pre-processing of raw data.** This step is CPU-only and converts TFRecord shards into the per-trajectory array files of §B.4, reporting the total number of converted trajectories as a consistency check. It runs once per dataset release and takes _≈_ 2–3 hours on a single CPU node at the scale of the example dataset. 

**Step 1: Train the context-aware tokenizer.** Stage 1 is trained on the pre-processed per-trajectory data with the hyperparameters of §B.2: global effective batch 32, base learning rate 5 _×_ 10<sup>_−_4</sup> , 

20 

Table 13: Key software dependencies. 

|Component|Version|
|---|---|
|PyTorch|2_._3|
|FlashAttention|2_._5|
|HuggingFace Accelerate|0_._30|
|HuggingFace Transformers|latest stable|
|HuggingFace Diffusers|latest stable|
|TensorFlow (only for TFDS I/O)|2_._15|
|LPIPS / timm / einops|latest stable|


discriminator start at step 10 _,_ 000, 6 _×_ 10<sup>4</sup> total steps, checkpoint every 2 _,_ 000 steps, and validation every 1 _,_ 000 steps on a held-out split (L1 and LPIPS). Activation checkpointing is enabled to reduce memory. The final checkpoint becomes the frozen backbone of Stage 2. Training takes _≈_ 72 hours on a single 8 _×_ A100-40GB node. 

**Step 2: Train the autoregressive Transformer.** Stage 2 is trained on the joint token sequence of §B.3 with the hyperparameters therein: per-GPU batch 4, no accumulation, global effective batch 32, learning rate 5 _×_ 10<sup>_−_5</sup> with a 5 _,_ 000-step linear warmup, gradient clipping _∥∇∥_ 2 _≤_ 1 _._ 0, 10<sup>6</sup> total steps, checkpoint every 10 _,_ 000 steps, and validation every 5 _,_ 000 steps. The Stage 1 tokenizer is loaded read-only and remains frozen throughout. Training throughput is _≈_ 3 _._ 5 it/s on a single 8 _×_ A100-40GB node, totalling _≈_ 80 hours for the full 10<sup>6</sup> steps. 

**Monitoring and sanity checks.** All scalar and image summaries are logged to TensorBoard. In practice we monitor three families of health indicators: _(i) mixed precision_ —bf16 must be explicitly enabled, since FlashAttention-2 refuses to execute under fp32; _(ii) hardware utilization_ —compute utilization should remain consistently above 90% with near-uniform per-GPU memory; otherwise the bottleneck typically lies in data loading or NCCL communication; _(iii) training stability_ —a smooth generator-loss transition around discriminator activation in Stage 1, and long-term stability of the gradient norm together with a monotone decrease of the held-out PPL in Stage 2. Common failure modes and mitigations are listed in Table 14. 

Table 14: Common failure modes observed during training. 

|Symptom|Root cause|Fix|
|---|---|---|
|FlashAttention only supports fp16 / bf16|Mixed precision misconfigured as fp32|Force the mixed-precision policy to bf16|
|NVML / NVLink symbol missing|Legacy node driver (e.g. the 450.x series)|Disable framework-side NVML probing and turn<br>off NCCL P2P/NVLS fast paths|
|Nested snapshots and abnormal disk usage<br>under the checkpoint directory|Residuals from previous smoke-test runs|Clean the smoke-test directory before starting the<br>production run|


### **B.6 Optimization Infrastructure** 

Table 15: Optimization infrastructure shared by Stage 1 and Stage 2. 

|Item|Value|
|---|---|
|Framework|PyTorch + HuggingFace Accelerate (multi-GPU)|
|Distributed backend|NCCL|
|Mixed precision|bf16 (both stages)|
|Activation checkpointing|Stage 1 enabled, Stage 2 disabled|
|Logging|TensorBoard scalar and image summaries|
|Random seed|set per experiment via Accelerate|
|Checkpoint format|HuggingFace Safetensors (unwrapped)|


Stage 1 produces tokenizer checkpoints at a fixed cadence; Stage 2 loads a specific checkpoint in read-only mode as its frozen backbone. No optimizer state, LR scheduler state, or data-loader state is shared between the two stages. 

21 

Table 16: Side-by-side comparison of the two training stages. 

|Dimension|Stage 1|Stage 2|
|---|---|---|
|Input|_x_1:_T ∈_R<sup>_T ×_3</sup><sup>_×H×W_</sup>|**x** _∈{_0_, . . . , V −_1_}_<sup>_S_</sup><br>|
|Output|Reconstructions ˆ_x_1:_T_ and FSQ indices|Logits_∈_R<sup>_S×V_</sup>|
|Objective|_LG_ (L1 + LPIPS + hinge-GAN)|_L_VGPT (masked causal CE)|
|Quantization|FSQ,_K_ = 4375|—|
|Tokens per clip|1840|1931(supervised480)|
|Trainable parameters|Stage 1 only|Stage 2 only (Stage 1 frozen)|
|Total steps|6_×_10<sup>4</sup>|10<sup>6</sup>|
|Effective batch|32|32|
|Mixed precision|bf16|bf16|
|Hardware|8_×_A100-40GB|8_×_A100-40GB|


### **B.7 End-to-End Quantitative Summary** 

**Compact formula card.** For reference, the end-to-end forward and training equations are collected below: 


Constants: _T_ = 8 _, tc_ = 1 _, td_ = 7 _, H ×W_ = 256 _×_ 320 _, p_ = 4 _, D_ = 5 _,_ **L** = (7 _,_ 5 _,_ 5 _,_ 5 _,_ 5) _, K_ = 4375 _, Nc_ = 1280 _, Nd_ = 80 _, Da_ = 13 _, Ba_ = 256 _, V_ = 9008 _, S_ = 1931 _, |M|_ = 480. 

### **B.8 TensorBoard Training Curves** 

This section summarizes the convergence curves of both stages on the Bridge V2 instantiation. All curves are exported directly from TensorBoard scalars without smoothing, with global optimization steps on the horizontal axis. 

### **B.8.1 Stage 1: Tokenizer (GAN + Reconstruction + Perception)** 

Stage 1 logs four prefix-grouped scalar families. Tables 17–19 report the trends observed over the first 60 _,_ 000 steps; each TensorBoard tag (quoted verbatim) maps one-to-one to the exported CSV file. 

**Optimization and throughput.** The auxiliary scalar `lr` tracks the generator learning rate (warmup for 5 _,_ 000 steps, followed by cosine decay); `samples_sec_gpu` , `batch_time` , and `data_time` respectively record per-GPU throughput, per-step wall time, and data-loading time. Reconstruction previews `images/reconstruction_*` are saved every 1 _,_ 000 steps for qualitative inspection of high-frequency texture fidelity. 

**Key training phases. (i)** Steps 0–10 _,_ 000: pure L1 + LPIPS supervision; reconstruction and perceptual curves descend fastest. **(ii)** Step 10 _,_ 000: discriminator activation ( `disc_start` = 10 _,_ 000); `gen_loss/gan_loss` becomes nonzero and `step_gen_loss` shows a mild +0 _._ 05-magnitude rebound. **(iii)** Steps 10 _,_ 000–60 _,_ 000: reconstruction and adversarial terms decrease jointly, and `val_loss/*` continues to drop monotonically. 

22 

Table 17: Generator loss _LG_ and its components ( <u>`gen_loss/*` ).</u> 

|Curve|Term|Observed trend (0_→_60_,_000steps)|
|---|---|---|
|`gen_loss/recon_loss`|_L_rec (dynamic-frame L1)|Monotone drop from_∼_0_._11to**0**_._**0169**|
|`gen_loss/perceptual_loss`|_L_perc (dynamic-frame LPIPS)|Monotone drop from_∼_0_._30to**0**_._**0607**|
|`gen_loss/ref_recon_loss`|Context-frame L1|Same magnitude as`recon_loss`; final_∼_0_._02|
|`gen_loss/ref_perceptual_loss`|Context-frame LPIPS<br>|Tracks`perceptual_loss`; final_∼_0_._07|
|`gen_loss/gan_loss`|_L_<sup>_G_</sup><br>adv <sup>(hinge,</sup><sup>_λa_ = 0</sup><sup>_._1)</sup>|0for step_≤_10_,_000; afterwards oscillates in[0_._10_,_ 0_._40];<br>final**0**_._**2546**|
|`gen_loss/commit_loss`|VQ commitment (exactly0un-<br>der FSQ)|0throughout|
|`gen_loss/dyna_commit_loss`|Dynamic-branch commitment<br>(exactly0under FSQ)|0throughout|
|`step_gen_loss`|Generator total loss_LG_|Drops from_∼_0_._50to**0**_._**1630**|


Table 18: Discriminator loss _LD_ and logits ( `disc_loss/*` <u>; logged only for step</u> _<u>≥</u>_ 10 _<u>,</u>_ 000). 

|Curve|Term|Observed trend|
|---|---|---|
|`disc_loss/real_logits`|E[_Dψ_(_x_)]|Mild drift in[_−_0_._30_,_ 0_._10]; final_−_**0**_._**2297**|
|`disc_loss/fake_logits`|E[_Dψ_(ˆ_x_)]|Drifts synchronously with`real_logits`; final_−_**0**_._**2463**|
|`disc_loss/logit_diff`|E[_Dψ_(_x_)_−Dψ_(ˆ_x_)]|Hovers around0with amplitude_<_ 0_._05, indicating_D_does not over-<br>whelm_G_|
|`step_discr_loss`|Discriminator total loss_LD_|Quickly settles into the[1_._5_,_ 2_._2]band after activation; final**1**_._**9864**,<br>consistent with a healthy GAN balance against_L_<sup>_G_</sup><br>adv|


**Training-curve visualization.** Figure 9 shows the four generator-side training curves, and Figure 10 shows the discriminator logits, validation metrics, and learning-rate schedule. In each panel the light trace is the raw sampled values and the dark trace an exponential moving average ( _α_ = 0 _._ 08); a dash-dotted vertical line marks discriminator activation at step 10 _,_ 000. 


Figure 9: **Stage 1 generator-side training dynamics.** (a) Reconstruction loss _L_ rec ( `gen_loss/recon_loss` , L1); (b) perceptual loss _L_ lpips ( `gen_loss/perceptual_loss` ); (c) adversarial loss _L_<sup>_G_</sup> adv<sup>(</sup><sup>`gen_loss/gan_loss`); (d) generator total loss</sup><sup>_LG_(</sup><sup>`step_gen_loss`).Panels</sup> (a) and (b) descend fastest before discriminator activation and continue to decrease monotonically afterwards; panel (c) stabilizes in [0 _._ 10 _,_ 0 _._ 40] after activation, reflecting the dynamic _G_ – _D_ equilibrium. 

23 

Table 19: Validation scalars ( `val_loss/*` <u>; averaged over 100 batches every 1</u> _<u>,</u>_ 000 steps). 

|Curve|Meaning|Observed trend|
|---|---|---|
|`val_loss/recon_loss`|Mean pixel L1|Monotone drop; best **0**_._**01944** at step 50_,_001, final 0_._01968 at<br>step59_,_001|
|`val_loss/perceptual_loss`|Mean LPIPS|Monotone drop; best **0**_._**06840** at step 50_,_001, final 0_._07147 at<br>step59_,_001|


Figure 10: **Stage 1 adversarial balance, validation metrics, and optimization schedule.** (a) Discriminator logits on real and fake samples ( `disc_loss/real_logits` , `disc_loss/fake_logits` ) and their difference `disc_loss/logit_diff` = _D_ (real) _− D_ (fake), which hovers around 0 with a mild positive drift and indicates that _D_ does not overwhelm _G_ ; (b) validation L1 ( `val_loss/recon_loss` , left axis) and LPIPS ( `val_loss/perceptual_loss` , right axis), both decreasing monotonically; (c) generator learning rate `lr` , which undergoes a 5 _,_ 000-step warmup followed by cosine decay. 

**Reconstruction evolution.** To visualize how the numerical trends translate into perceptual quality, Figure 11 shows pixel-space reconstructions from the Stage 1 tokenizer at six representative training steps ( _{_ 1 _,_ 2 _,_ 500 _,_ 10 _,_ 000 _,_ 25 _,_ 000 _,_ 50 _,_ 000 _,_ 60 _,_ 000 _}_ ). Each training step is rendered as a pair of adjacent rows: the upper row shows the ground-truth frames _x_ and the lower row the decoder outputs _x_ ˆ; columns uniformly sample 4 temporal positions ( _t_ 1 _, t_ 3 _, t_ 5 _, t_ 7) out of the _T_ = 8 clip frames, so that both spatial fidelity and temporal consistency become visually apparent. 

### **B.8.2 Stage 2: Autoregressive Transformer (Causal CE + Perplexity)** 

Stage 2 is monitored with TensorBoard scalars centered on the masked causal cross-entropy objective and its induced perplexity. Figure 12 reports the exported raw traces together with an exponential moving average (EMA, _α_ = 0 _._ 9), avoiding manually tabulated estimates from the plots. 

**Observed convergence.** The training loss drops sharply at the beginning of optimization and then enters a slower refinement regime, with the EMA curve continuing to decrease over the full training horizon. The held-out loss follows the same overall pattern: a rapid early reduction followed by a gradual flattening, without a late-stage upward trend. The evaluation perplexity is consistent with the held-out cross-entropy curve, decreasing rapidly in the early phase and then approaching a stable low-variance regime. Together, these curves indicate that the Stage 2 Transformer learns the token dynamics early and continues to refine its next-token distribution over long training, while the validation metrics do not show visible signs of divergence from the training trajectory. 

24 


Figure 11: **Evolution of Stage 1 reconstructions across training steps.** Horizontal axis: temporal frame position _ti_ inside a clip. Vertical axis: training steps from early to late; every two rows form a comparison pair, with the upper row showing the ground-truth frame and the lower row showing the decoded _x_ ˆ from the same FSQ indices. At step _≤_ 10<sup>3</sup> the dynamic branch fails to recover high-frequency textures occluded by the manipulator, and reconstructions exhibit global blur and mild colour bias; around step 10<sup>4</sup> (discriminator activation) texture sharpness improves noticeably, yet locally visible grid-like artefacts still contribute a non-negligible LPIPS gap; beyond step 2 _._ 5 _×_ 10<sup>4</sup> , reconstructions become visually indistinguishable from ground truth, with residual errors concentrated on the narrow contact region between the end-effector and the manipulated object. This qualitative evolution is step-aligned with the monotone L1/LPIPS curves in Figures 9–10 and with the best-validation step (5 _×_ 10<sup>4</sup> ) of `val_loss/*` . 

25 


Figure 12: **Stage 2 autoregressive Transformer training curves.** Top: training masked causal cross-entropy loss. Bottom left: held-out evaluation loss. Bottom right: held-out evaluation perplexity. Each panel shows both the raw TensorBoard trace and an EMA-smoothed curve with _α_ = 0 _._ 9. 

26 

## **C Stylized derivation for Proposition 1** 

We provide the simplified derivation underlying the main-text stability discussion. The goal is to illustrate why periodic refresh can limit long-horizon drift under a local contraction assumption, rather than to claim a complete dynamical model of the tokenizer–decoder pair or a quantitative predictor of the exact gains observed in experiments. 

**Setup and notation.** Consider a token-based autoregressive world model generating a rollout of _T_ frames partitioned into _K_ = _⌈T/W ⌉_ segments of window size _W_ . Let _x_<sup>_∗_</sup> _t_<sup>denote the ground-truth</sup> frame at step _t_ and _x_ ˆ _t_ the predicted frame. We define the frame-level error as _et_ = _∥x_ ˆ _t − x_<sup>_∗_</sup> _t_<sup>_∥_.We</sup> make two assumptions: 

- **A1** . **Bounded per-step error.** Conditioned on a correct context, the single-step prediction error satisfies _et ≤ ε_ for all _t_ . More generally, if the context carries an error _η_ , the prediction error at the next step satisfies _et ≤ ε_ + _α η_ for some contraction factor _α ∈_ [0 _,_ 1). 

- **A2** . **Bounded quantization error.** The decode–re-encode cycle introduces a quantization error bounded by _δq_ : for any predicted frame _x_ ˆ, _∥D_ vis( _T_ vis(ˆ _x_ )) _− x_ ˆ _∥≤ δq_ . 

**Standard autoregressive generation (no re-encoding).** Under native AR decoding, the context is never refreshed, so context-carried error keeps accumulating across the full horizon. If a contraction assumption analogous to **A1** held globally, one would obtain the geometric series 


For any fixed _α <_ 1, this is bounded by _ε/_ (1 _− α_ ), but this constant can still blow up as _α →_ 1. In the non-contractive worst case, the accumulation becomes linear in the horizon, yielding the coarse comparison bound 


The AR regime therefore either pays a horizon-independent but potentially large constant _ε/_ (1 _− α_ ), or a linear-in- _T_ bound when contraction fails; SWR will instead replace this with a window-sizecontrolled constant. 

**Sliding-window re-encoding.** With SWR, at each segment boundary _t_ = _kW_ , the model decodes the last predicted frame _x_ ˆ _kW_ to pixel space and re-encodes it as a fresh context/state pair ( _zk_<sup>ctx</sup> +1<sup>_,z_</sup> 0<sup>dyn</sup> ) = _T_ vis(ˆ _xkW_ ); concretely, _x_ ˆ _kW_ is treated both as the new conditioning frame for the Full-VAE branch _Ec_ and as a length-one dynamic clip for the Conditional-VAE branch _Ed_ (Appendix B.2). 

_Step 1: Within-segment error._ Within segment _k_ , the context _zk_<sup>ctx</sup> is fixed and the model generates at most _W_ frames. By **A1** , the error at relative step _j ∈{_ 1 _, . . . , W }_ within the segment satisfies: 


where _ηk_ is the error carried by the context _zk_<sup>ctx.For</sup><sup>_j≤W_, using �</sup><sup>_j_</sup> _i_ =0<sup>_−_1</sup><sup>_αi_=</sup><sup><u>1</u></sup> 1<sup>_−_</sup> _−_<sup>_<u>α</u>_</sup> _α_<sup>_j≤j≤W_and</sup> _α_<sup>_j_</sup> _≤_ 1: 


Taking _j_ = _W_ gives the tighter intermediate bound _ekW ≤ Wε_ + _α_<sup>_W_</sup> _ηk_ , which we use in Step 2. 

_Step 2: Cross-segment error refresh._ At the boundary, the context error of segment _k_ +1 is: 


Crucially, _zk_<sup>ctx</sup> +1<sup>is obtained by re-encoding the</sup><sup>_decoded_frame, so the next segment depends on the</sup> current decoded observation rather than the entire raw token history of all prior segments. Substituting the tighter form of Eq. 12 at _j_ = _W_ : 


27 

_Step 3: Steady-state bound._ Since _α_<sup>_W_</sup> _<_ 1, the recurrence _ηk_ +1 _≤ Wε_ + _α_<sup>_W_</sup> _ηk_ + _δq_ converges to a fixed point: 


Starting from _η_ 1 = 0 (ground-truth conditioning frame), by induction _ηk ≤ η_<sup>_∗_</sup> for all _k_ . Combining with the loose within-segment bound _e_ ( _k−_ 1) _W_ + _j ≤ Wε_ + _ηk_ from Eq. 12 (which upper-bounds _α_<sup>_W_</sup> _ηk_ by _ηk_ ), the maximum frame-level error in any segment is therefore: 


In the simplified case _α →_ 0 (errors do not propagate within the causal Transformer’s effective receptive field beyond one step), _α_<sup>_W_</sup> _→_ 0 and _η_<sup>_∗_</sup> _→ Wε_ + _δq_ , so the bound becomes _E_ SWR( _T_ ) _≤_ 2 _Wε_ + _δq_ . More generally, for any _α ∈_ [0 _,_ 1) and any window size _W_ such that _α_<sup>_W_</sup> _<_ 1, the bound in Eq. 13 is finite and does not grow explicitly with _T_ , showing that under this stylized local model the effect of SWR is governed by the refresh window and the local error parameters rather than the rollout horizon alone. We do not estimate _α_ or _δq_ from the trained model; instead, the derivation is meant to justify the qualitative window-size trade-off observed in Table 3 and Appendix G, where moderate refresh intervals outperform both overly frequent and overly infrequent refresh. 

### **Asymptotic optimum of the window size.** Treating _W_ as a positive real variable, let 


This is the SWR bound of Eq. 13 written as a function of _W_ at fixed ( _ε, δq, α_ ). The qualitative trade-off discussed in Remark 1 in the main text can be made precise by analyzing the first-order stationarity of _f_ . 

**Corollary 1** ( **Asymptotic optimum** _W_<sup>_∗_</sup> ) **.** _Assume α ∈_ (0 _,_ 1) _and δq ≥_ 0 _. In the moderate-window regime α_<sup>_W_</sup> _≪_ 1 _, the bound f_ ( _W_ ) _is quasi-convex in W and attains its minimum at_ 


_provided the argument of the logarithm exceeds_ 1 _; otherwise the minimum is achieved at the smallest admissible W (i.e. the quantization cost δq is too small relative to ε to justify any batching). In particular, W_<sup>_∗_</sup> _is logarithmic in δq/ε and in_ 1 _/_ ( _−_ ln _α_ ) _._ 

_Proof._ In the regime _α_<sup>_W_</sup> _≪_ 1, we expand 1 _/_ (1 _− α_<sup>_W_</sup> ) _≈_ 1 + _α_<sup>_W_</sup> + _O_ ( _α_<sup>2</sup><sup>_W_</sup> ) in Eq. 13, giving _f_ ( _W_ ) _≈_ 2 _Wε_ + _δq_ + _α_<sup>_W_</sup> ( _Wε_ + _δq_ ) + _O_ ( _α_<sup>2</sup><sup>_W_</sup> ) _._ 

Differentiating with respect to _W_ and retaining leading-order terms (using _dWd_<sup>_αW_=</sup><sup>_αW_ln</sup><sup>_α_and</sup> discarding the subleading _α_<sup>_W_</sup> _ε_ contribution), 


Setting _df/dW_ = 0 and using ln _α <_ 0, 


In the typical regime _δq ≫ Wε_ (single-step token error small relative to the decode–re-encode distortion, as observed in our token-level probes), the right-hand side is dominated by _δq_ , giving 


which is Eq. 14. The second-derivative test at this point gives _d_<sup>2</sup> _f/dW_<sup>2</sup> _≈−_ (ln _α_ )<sup>2</sup> _α_<sup>_W_</sup> ( _Wε_ + _δq_ ) _>_ 0, so _f_ is locally convex and _W_<sup>_∗_</sup> is a minimum. When the argument of the outer logarithm drops below 1, i.e. _δq ≤_ 2 _ε/_ ( _−_ ln _α_ ), the stationarity condition has no interior solution and _f_ is monotone decreasing over its admissible range; the constrained minimum then lies at the smallest _W_ permitted by the inference hardware or the decoder receptive field. 

28 

**Physical interpretation.** Corollary 1 attaches a concrete meaning to the three parameters of the stylized model. **(i) Role of the contraction factor** _α_ **.** As _α →_ 1<sup>_−_</sup> (within-segment error is barely damped), the prefactor 1 _/_ ( _−_ ln _α_ ) diverges and _W_<sup>_∗_</sup> grows, i.e. the model benefits from _longer_ segments that amortize the one-time refresh cost; in the opposite limit _α →_ 0<sup>+</sup> (errors decay within a single step), short segments suffice and _W_<sup>_∗_</sup> is small. **(ii) Role of the noise ratio** _δq/ε_ **.** Large _δq/ε_ (each refresh is comparatively expensive) pushes _W_<sup>_∗_</sup> up, while small _δq/ε_ (refresh is nearly free) pushes _W_<sup>_∗_</sup> down; the logarithmic dependence means that _W_<sup>_∗_</sup> is insensitive to the precise value of _δq_ and _ε_ within an order of magnitude. **(iii) Consistency with the ablation.** In our setting we expect the tokenizer–decoder cycle to be moderately contractive and the decode–re-encode distortion _δq_ to dominate the single-step token error _ε_ , so Eq. 14 predicts _W_<sup>_∗_</sup> to lie in the small-integer regime. Empirically, Appendix G finds _W_ = 6 optimal among _{_ 4 _,_ 6 _,_ 8 _,_ 10 _,_ 15 _}_ , which is consistent with this regime; _W_ = 4 pays too much refresh overhead while _W ≥_ 10 leaves too much within-segment drift, as Corollary 1 predicts. These conclusions are meant only to explain the _shape_ of the _W_ –quality trade-off under the stylized assumptions **A1** – **A2** ; we do not claim that Eq. 14 is a numerical predictor of the exact optimum, nor that a single global ( _α, ε, δq_ ) triple suffices to describe every manipulation task in the benchmark. 

**Comparison with vanilla AR decoding.** The two regimes can be placed on a common axis by viewing _E_ AR( _T_ ) of Eq. 11 against _E_ SWR( _T_ ) of Eq. 13. This yields the following direct consequence, which makes the _T_ –dependence gap explicit rather than only qualitative. 

**Corollary 2** ( **SWR versus AR asymptotic gap** ) **.** _Under Assumptions_ **_A1_** _–_ **_A2_** _and for any W with α_<sup>_W_</sup> _<_ 1 _,_ 


_so the advantage of SWR grows at least linearly in the rollout horizon T once T exceeds the horizonindependent SWR constant. In the contractive regime α <_ 1 _with α_<sup>_W_</sup> _≪_ 1 _, the SWR constant simplifies to ≈_ 2 _Wε_ + _δq, and the crossover horizon above which SWR strictly dominates AR is T_<sup>_†_</sup> _≈ W_ + _δq/ε._ 

_Proof._ Subtract Eq. 13 from the non-contractive-regime bound of Eq. 11 directly. The simplified constant follows from ( _Wε_ + _δq_ ) _/_ (1 _− α_<sup>_W_</sup> ) _→ Wε_ + _δq_ as _α_<sup>_W_</sup> _→_ 0, and solving _T_<sup>_†_</sup> _ε ≥_ 2 _Wε_ + _δq_ for _T_<sup>_†_</sup> gives the stated crossover. 

Eq. 15 turns the qualitative “does not grow with _T_ ” statement in the main text into an order-ofmagnitude prediction: the longer the rollout, the larger the SWR advantage, with the crossover controlled by the ratio _δq/ε_ rather than by _T_ itself. 

**Discussion of assumptions.** Assumption **A1** replaces the true non-stationary rollout dynamics with a locally linear contraction around the on-policy trajectory; this is standard in stylized errorpropagation analyses of autoregressive generation (see, e.g., the attention-sink regime of [15]) and is used here only to obtain a closed-form window-size trade-off. A global contraction assumption on the full horizon would in general fail for autoregressive token models, which is precisely the empirical observation that motivates SWR; our analysis therefore imposes contraction only _within_ a segment of length _W_ , consistent with the segmented generation procedure of Eq. 9. Assumption **A2** treats the decode–re-encode cycle as a bounded, input-independent distortion. This is a conservative over-approximation: in practice _δq_ depends on the content of the refreshed frame, but the _worst-case_ bound we derive only requires a uniform upper bound, which is furnished by the FSQ tokenizer’s finite codebook. Finally, the corollaries above are invariant under any affine rescaling of ( _ε, δq_ ): only the ratio _δq/ε_ enters _W_<sup>_∗_</sup> , which explains why the optimum window is robust to the specific scale on which token-level error is measured. 

29 

## **D Pseudocode for Reward-Aligned Post-Training** 

Algorithm 1 summarizes the complete ROBOALIGN-R1 training pipeline, covering all four stages described in §3.2. Color coding marks each stage: **benchmark construction** (blue), **teacher judge training** (green), **student reward distillation** (purple), and **GRPO post-training** (red). 

**Algorithm 1** Reward-Aligned Post-Training of ROBOALIGN-R1 

**Require:** Pre-trained world model _pθ_ ; robot datasets _{_ RT-1, Bridge, CALVIN, LIBERO _}_ ; T2V model; base VLM (Qwen3-VL-8B-Thinking) 

**Ensure:** Post-trained world model _pθ∗_ 

_— Stage 1: Benchmark Construction —_ 1: **for** each instruction _l_ in robot datasets **do** 

- 2: Sample ground-truth video _v_<sup>+</sup> from dataset 

- 3: Generate candidate video _v_<sup>_−_</sup> _←_ T2V( _l_ ) 

4: Annotate ( _l, v_ ) with raw rubric scores **r** = ( _r_ 1 _, . . . , r_ 6) using ranges [3 _,_ 2 _,_ 1 _,_ 1 _,_ 1 _,_ 2] _▷_ Six dimensions 5: **end for** 6: _D_ bench _←{_ ( _li, vi,_ **r** _i_ ) _}_<sup>_N_</sup> _i_ =1 

_— Stage 2: Teacher Judge Training —_ 7: Initialize teacher _fϕ_ from Qwen3-VL-8B-Thinking 8: Fine-tune _fϕ_ on _D_ bench: _L_ teacher = _−_ E�log _pϕ_ ( **r** _| l, v_ )� _▷ fϕ →_ ROBOALIGN-JUDGE 

- _Stage 3: Student Reward Distillation —_ 

- 9: Initialize student _gψ_ (compact visual–text encoder + linear head) 

10: Construct _D_ distill from benchmark videos and generated rollouts scored by teacher _fϕ ▷_ Teacher-labeled mixed corpus 11: Train _gψ_ with per-dimension weighted Huber regression on normalized teacher scores (Eq. 4) 

_— Stage 4: GRPO Post-Training with Online Iterative Distillation —_ 

- 12: **for** iteration _n_ = 1 _,_ 2 _, . . ._ **do** 

- 13: Sample group of _G_ rollouts _{x_ ˆ<sup>(</sup><sup>_j_)</sup> _}_<sup>_G_</sup> _j_ =1<sup>_∼pθ_</sup> 14: Score each rollout: _R_<sup>(</sup><sup>_j_)</sup> =<sup>�6</sup> _k_ =1<sup>_wk_[</sup><sup>_gψ_(</sup><sup>_l,_ˆ</sup><sup>_x_(</sup><sup>_j_))]</sup><sup>_k_</sup> 

- 15: Compute advantage: _A_<sup>(</sup><sup>_j_)</sup> = ( _R_<sup>(</sup><sup>_j_)</sup> _−_ mean _jR_ ) _/_ std _jR_ 

- 16: Update _θ_ via clipped policy gradient _L_ GRPO (Eq. 7) 

- 17: **if** _n_ mod _K_ = 0 **then** 

- 18: Score fresh rollouts with teacher _fϕ_ and update student _gψ ▷_ Online iterative distillation 19: **end if** 

- 20: **end for** 

- 21: **return** _pθ∗_ 

30 


Figure 13: Architecture of the distilled student reward model _gψ_ . A visual branch encodes uniformly sampled video frames using a partially unfrozen ViT-Base/16 backbone, while a text branch encodes the instruction using a lightweight Transformer. The fused multimodal representation is then mapped to six normalized reward dimensions by a compact MLP head. 

## **E Student Reward Model Details** 

Figure 13 presents the architecture of the distilled student reward model _gψ_ . The student is designed to provide efficient reward estimation within the inner RL loop by approximating the six-dimensional score vector produced by the teacher judge _fϕ_ . In our implementation, the model contains approximately 98M parameters in total, of which about 40.6M are trainable under partial ViT unfreezing. Its inference latency is approximately 20 ms per video (roughly 50 videos/s), making it substantially more efficient than direct teacher inference. 

**Visual branch.** Given a generated video _v_ consisting of _T_ frames, we uniformly sample _N_ =8 key frames. During training, we introduce temporal jitter by perturbing the uniform frame indices with small random offsets, thereby improving robustness to minor timing variations. The sampled frames are further processed with video-level data augmentation, including a shared random resized crop, a shared horizontal flip, and mild per-frame color jitter. During validation and testing, all frames are deterministically resized to 224 _×_ 224. 

The augmented frames are encoded independently by a pretrained ViT-Base/16 visual encoder. Rather than freezing the backbone entirely, we freeze the first 8 Transformer blocks and unfreeze the final 4 blocks together with the final normalization layer. This design allows high-level visual features to adapt to failure modes specific to robot-manipulation videos while preserving generic low-level image representations. For each frame, we extract the [CLS] feature **h** _i ∈_ R<sup>768</sup> and perform temporal mean pooling to obtain a video-level representation, 


This representation is then passed through a lightweight projection layer (LayerNorm _→_ Linear _→_ GELU) to produce the final visual embedding **v** _∈_ R<sup>768</sup> . 

**Text branch.** The instruction _l_ is tokenized using the BERT tokenizer from `bert-base-uncased` and truncated or padded to a maximum length of _L_ =64. The resulting subword sequence is encoded by a lightweight 4-layer Transformer encoder with hidden size 256, 4 attention heads, and feedforward dimension 1024. A learnable [CLS] token is prepended to the input sequence and combined with learnable positional embeddings. After passing through the 4 Transformer layers, the output corresponding to the [CLS] token is used as the instruction embedding **t** _∈_ R<sup>256</sup> . Each layer adopts a Pre-Norm Transformer block with GELU activations and dropout at rate 0.2. 

**Multimodal fusion and scoring head.** We fuse the visual and textual modalities by simple concatenation, 

**z** = [ **v** ; **t** ] _∈_ R<sup>1024</sup> _._ 

The fused representation is processed by a 3-layer MLP scoring head with the following structure: Linear(1024 _→_ 512) _→_ LayerNorm _→_ GELU _→_ Dropout, followed by Linear(512 _→_ 256) _→_ 

31 

Table 20: **Backbone and architecture ablation of the student reward model.** Comparison of representative visual encoders and fusion designs under matched training and evaluation settings. Metrics capture both fidelity to teacher judgments and inference efficiency. 

|Method|Visual encoder|Fusion module|Pearson corr. _↑_|MSE_↓_|Latency (ms)_↓_|
|---|---|---|---|---|---|
|ResNet student|ResNet-50|concat + MLP|0.79|0.186|13|
|Frozen ViT student|ViT-Base/16 (frozen)|concat + MLP|0.84|0.142|18|
|Text-only student|none|Transformer + MLP|0.52|0.421|4|
|Ours|ViT-Base/16 (last 4 blocks unfrozen)|concat + MLP|0.88|0.096|20|


LayerNorm _→_ GELU _→_ Dropout, and a final Linear(256 _→_ 6) layer. A sigmoid activation maps the output to normalized reward scores in [0 _,_ 1]<sup>6</sup> , corresponding to instruction following, manipulation success, action–outcome consistency, temporal consistency, contact realism, and physics adherence. During distillation training and during GRPO post-training (Eq. 5), the student is always consumed in this normalized [0 _,_ 1]<sup>6</sup> form; the raw-range rescaling to [3 _,_ 2 _,_ 1 _,_ 1 _,_ 1 _,_ 2] is applied only when student outputs need to be reported alongside teacher scores for diagnostic or visualization purposes, and is never re-applied before the reward aggregation _R_ (ˆ _x_ 1: _T_ ). 

**Distillation training.** We train the student on teacher-labeled video–instruction pairs using normalized teacher scores, which prevents dimensions with larger numerical ranges from dominating optimization. Instead of plain MSE, we adopt a per-dimension weighted Huber loss: 


where ˆ _sb,k_ =[ _gψ_ ( _lb, vb_ )] _k ∈_ [0 _,_ 1] is the student’s sigmoid-activated output, ˜ _sb,k_ is the teacher score normalized dimension-wise to [0 _,_ 1], and _δh_ = 0 _._ 5 is the Huber threshold. Since both sides already share the same [0 _,_ 1] scale after normalization, the per-dimension weights _{λk}_ are used only to equalize convergence speed across dimensions with unequal label-noise levels (e.g., 3-level rubric vs. binary rubric); in practice we tune them on a validation split rather than tying them to the raw score ranges. Note that _{λk}_ are distinct from the reward aggregation weights _{wk}_ used in Eq. 5. 

Training further employs mixup regularization with probability 0.3, AdamW with weight decay 0.05, and differential learning rates: 5 _×_ 10<sup>_−_6</sup> for the unfrozen ViT blocks and 5 _×_ 10<sup>_−_4</sup> for the text encoder and scoring head. The learning-rate schedule uses linear warmup over the first 10% of training steps followed by cosine decay, with a minimum learning rate of 10<sup>_−_6</sup> . We additionally apply gradient clipping with maximum norm 1.0, maintain an exponential moving average (EMA) of the trainable parameters with decay 0.999, and select checkpoints based on validation-set Pearson correlation with early stopping (patience 10). Collectively, these design choices improve fidelity to the teacher’s ranking behavior and stabilize the student when used as an online reward proxy during RL post-training. 

**Backbone and architecture comparison.** Because the student reward model is intended to serve as a high-throughput reward proxy rather than the primary source of semantic supervision, an important design question is whether a simple CNN-style reward model is sufficient, or whether a partially unfrozen ViT-based architecture is necessary. Table 20 compares representative lightweight baselines with the final partially unfrozen ViT student used in our method. The results indicate that the final student achieves a more favorable trade-off between fidelity to the teacher and online efficiency than simpler reward regressors. 

**Teacher–student efficiency trade-off.** The teacher and student play complementary roles in our framework. The high-capacity teacher remains essential for providing semantically rich, highfidelity supervision during offline reward distillation. The student is introduced solely to make such supervision practical within the inner RL loop, where thousands of rollout evaluations may be required. Table 21 summarizes the resulting efficiency gap. 

This efficiency gap is particularly important for RL post-training. For example, if a single training step requires scoring 16 generated videos, direct teacher evaluation would still take on the order of seconds even with moderate parallelism, whereas the student can score the same batch in a fraction of 

32 

Table 21: **Teacher–student efficiency comparison for reward evaluation.** The teacher provides high-fidelity supervisory signals, whereas the distilled student is optimized for fast online reward evaluation during RL post-training. All numbers are measured or estimated on a single A100 40GB GPU. 

|Statistic|Teacher judge (_fϕ_)|Student reward model (_gψ_)|
|---|---|---|
|Architecture|Qwen3-VL-8B-Thinking + LoRA|ViT-Base/16 + 4L text Transformer + MLP|
|Total parameters|_∼_8B|_∼_98M|
|Trainable parameters|LoRA-only adaptation|_∼_40_._6M|
|Per-video latency|_∼_2800ms|_∼_20ms|
|Inference throughput|_∼_0_._5videos/s|_∼_50videos/s|
|Inference GPU memory|_∼_16–20GB|_∼_0_._5–1GB|
|Input representation|video frames + judge prompt|8 sampled frames + instruction|
|Output representation|autoregressive text + parsed scores|direct 6D score vector|


Table 22: **Reward-evaluation cost within the RL loop.** Comparison of teacher-only evaluation and distilled-student evaluation for representative RL workloads. 

|RL workload|Teacher judge (_fϕ_)|Student reward model (_gψ_)|
|---|---|---|
|Reward evaluation for 16 videos / step|_∼_45s (serial) /_∼_12s (4-way parallel)|_∼_0_._32s (batched)|
|Reward cost over 1000 RL steps|_∼_12_,_000–45_,_000s|_∼_320s|
|Share of total training time|dominant bottleneck|minor overhead|
|Additional hardware demand|dedicated large-VLM inference budget|can share training GPU|


a second. In practice, this shifts reward computation from a dominant bottleneck to a comparatively minor overhead, while preserving the teacher as the source of high-quality supervision. 

33 

## **F Pseudocode and Implementation of Sliding Window Re-encoding** 

We present the sliding-window re-encoding inference procedure in two complementary formats: Algorithm 2 provides a formal pseudocode overview, and Listing 1 shows the corresponding PyTorch implementation extracted from our codebase. Both use matching color coding for the three key stages: **prompt construction** (blue), **autoregressive generation** (green), and **context refresh** (red). 

**Algorithm 2** Sliding Window Re-encoding Inference 

**Require:** World model _pθ_ ; tokenizer _T_ vis; decoder _D_ vis; conditioning frame _x_ 0; actions _{at}_<sup>_T_</sup> _t_ =1<sup>;</sup> window size _W_ 

**Ensure:** Generated video _x_ ˆ1: _T_ 

1: _z_ 1<sup>ctx</sup><sup>_,z_</sup> 0<sup>dyn</sup> _←T_ vis( _x_ 0) _▷_ Encode initial context ( _x_ 0 used as both _Ec_ and length-1 _Ed_ input) 2: frames_out _←_ [ ]; _m ←_ 1 3: **while** _|_ frames_out _| < T_ **do** 4: _W_<sup>_′_</sup> _←_ min( _W, T −|_ frames_out _|_ ) 5: prompt _←_ [ _zm_<sup>ctx</sup><sup>_∥z_</sup> 0<sup>dyn</sup> _∥ a_ ˆ1 ] _▷_ Build prompt 6: window_tokens _←_ [ ] 7: **for** _j_ = 1 _, . . . , W_<sup>_′_</sup> **do** 8: _z_ ˆ _j_<sup>dyn</sup> _← pθ_ � _· |_ prompt� _▷_ Generate _Nd_ =80 dynamics tokens 9: Append _z_ ˆ _j_<sup>dyn</sup> to window_tokens 10: prompt _←_ prompt _∥ z_ ˆ _j_<sup>dyn</sup> _∥ a_ ˆ _j_ +1 _▷_ Extend prompt 11: **end for** 12: _x_ ˆwin _←D_ vis( _zm_<sup>ctx</sup><sup>_,_window_tokens)</sup> _▷_ Decode window to pixels 13: Append _x_ ˆwin to frames_out 14: **if** _|_ frames_out _| < T_ **then** 15: _x_ ˆlast _← x_ ˆwin[ _−_ 1] _▷_ Take last decoded frame 16: _zm_<sup>ctx</sup> +1<sup>_,z_</sup> 0<sup>dyn</sup> _←T_ vis(ˆ _x_ last) _▷_ Re-encode last frame via _Ec_ and length-1 _Ed_ 17: **end if** 18: _m ← m_ + 1 19: **end while** 20: **return** frames_out 

Listing 1: **PyTorch implementation** of sliding window re-encoding. Comments are color-coded to match Algorithm 2. @ `ctx_tokens` @ corresponds to @ _zm_<sup>ctx@ and @</sup><sup>`dyn_tokens`@ to @</sup><sup>_z_</sup> 0<sup>dyn</sup> @ in Algorithm 2. 

<mark>1</mark> <mark>`def generate_sliding_window (` 2</mark> <mark>`model , tokenizer , ctx_tokens , dyn_tokens ,` 3</mark> <mark>`actions , num_frames , window_size =6,` 4</mark> <mark>`):` 5</mark> <mark>`all_frames = []` 6</mark> <mark>`frames_done , step = 0, 0` 7 8</mark> <mark>`while frames_done < num_frames :` 9</mark> <mark>`W = min (window_size , num_frames - frames_done )`</mark> 1 <mark>0</mark> 1 <mark>1</mark> <mark>`# [BLUE] Build initial prompt: [ctx | dyn_0 | action_0]`</mark> 1 <mark>2</mark> <mark>`prompt = build_prompt (ctx_tokens , dyn_tokens , actions[step ])`</mark> 1 <mark>3</mark> <mark>`window_dyn = []`</mark> 1 <mark>4</mark> 1 <mark>5</mark> <mark>`# [GREEN] Autoregressive generation within one window`</mark> 1 <mark>6</mark> <mark>`for j in range (W):`</mark> 1 <mark>7</mark> <mark>`gen_tokens = model.generate(prompt , max_tokens =80)`</mark> 1 <mark>8</mark> <mark>`window_dyn.append(gen_tokens )`</mark> 1 <mark>9</mark> <mark>`prompt = prompt + gen_tokens + discretize(actions[step+j+1])`</mark> 2 <mark>0</mark> 2 <mark>1</mark> <mark>`# [GREEN] Decode entire window to pixel space`</mark> 2 <mark>2</mark> <mark>`decoded = tokenizer.decode(ctx_tokens , window_dyn )`</mark> 2 <mark>3</mark> <mark>`all_frames.extend(decoded)`</mark> 2 <mark>4</mark> <mark>`frames_done += W`</mark> 2 <mark>5</mark> <mark>`step += W`</mark> 2 <mark>6</mark> 2 <mark>7</mark> <mark>`# [RED] Context refresh: decode-re-encode cycle`</mark> 2 <mark>8</mark> <mark>`# last_frame fed to both E_c and length-1 E_d`</mark> 

34 

- 2 <mark>9</mark> <mark>`if frames_done < num_frames :`</mark> 3 <mark>0</mark> <mark>`last_frame = decoded [-1]`</mark> 3 <mark>1</mark> <mark>`ctx_tokens , dyn_tokens = tokenizer.encode(`</mark> 3 <mark>2</mark> <mark>`last_frame , last_frame`</mark> 3 <mark>3</mark> <mark>`)`</mark> 3 <mark>4</mark> 3 <mark>5</mark> <mark>`return all_frames`</mark> 

35 

Table 23: SWR efficiency vs. default AR across _W_ : timing, throughput, GPU memory, prompt length (tokens), mean per-frame latency, and re-encoding. 

|Metric|AR (_∞_)|_W_=4|_W_=6|_W_=8|_W_=10|_W_=15|
|---|---|---|---|---|---|---|
|Total time (s)|5.646_±_0_._01|5.863_±_0_._02|5.709_±_0_._07|5.858_±_0_._28|5.740_±_0_._11|5.732_±_0_._07|
|FPS|5_._31|5_._12|5_._26|5_._13|5_._23|5_._23|
|Peak GPU (MB)|34_,_206|32_,_066|32_,_781|33_,_493|34_,_214|34_,_209|
|Mean prompt len.|2_,_722|1_,_506|1_,_606|1_,_680|1_,_792|2_,_024|
|Max prompt len.|4_,_070|1_,_652|1_,_838|2_,_024|2_,_210|2_,_675|
|Mean ms/frame|182_._2|174_._7|175_._7|181_._5|180_._7|181_._7|
|#Re-encodings|0|7|4|3|2|1|
|Re-enc. total (ms)|0|99_._8|73_._8|68_._3|48_._3|87_._0|


Table 24: Re-encoding overhead vs. _W_ . % total: re-encoding time / wall time. Per step: mean ms per refresh. 

|_W_|#Re|Total (ms)|% total|Per step (ms)|
|---|---|---|---|---|
|4|7|99_._8|1_._70%|14_._3|
|6|4|73_._8|1_._29%|18_._5|
|8|3|68_._3|1_._17%|22_._8|
|10|2|48_._3|0_._84%|24_._1|
|15|1|87_._0|1_._52%|87_._0|


## **G SWR window-size ablation** 

This section complements the main-text SWR panel (Table 3). Unless noted, measurements use Llama-style causal LM (12 layers, hidden 768, 12 heads), vLLM inference, and 300 episodes _×_ 30 frames. 

36 

Table 25: Long-horizon prompt scaling: AR max prompt extrapolates linearly with rollout length; SWR ( _W_ =6) caps at the 30-frame plateau. Slow-down columns are indicative. 

|Frames|AR max prompt|SWR_W_=6max|Prompt drop|AR slow-down|SWR slow-down|
|---|---|---|---|---|---|
|30|4_,_070|1_,_838|54_._8%|_∼_7%|_∼_0%|
|100|_∼_12_,_673|1_,_838|85_._5%|_∼_25–30%|_∼_0%|
|300|_∼_37_,_273|1_,_838|95_._1%|OOM risk|_∼_0%|


37 


Figure 14: Qualitative comparison for the instruction _“close top drawer”_ . The highlighted row denotes the visually best SWR result for this episode. 

## **H SWR qualitative visualizations** 

This section provides qualitative case studies comparing default autoregressive decoding with SWR under different refresh windows. In each figure, columns show sampled frames along the rollout, while rows compare Ground Truth, Default AR, and SWR with different window sizes _W_ . The highlighted row marks the visually best SWR variant for that episode. Consistent with the quantitative results, periodic refresh generally reduces long-horizon drift and better preserves task progression and object configuration, although the best per-episode _W_ can vary with the manipulation trajectory. 

38 


Figure 15: Qualitative comparison for the instruction _“move apple near white bowl”_ . The highlighted row denotes the visually best SWR result for this episode. 

39 


Figure 16: Qualitative comparison for the instruction _“move green can near apple”_ . The highlighted row denotes the visually best SWR result for this episode. 

40 


Figure 17: Qualitative comparison for the instruction _“pick banana from white bowl”_ . The highlighted row denotes the visually best SWR result for this episode. 

41 

## **I Evaluation Metrics** 

This section provides a detailed description of all evaluation metrics used in our experiments. 

### **I.1 Semantic and Physical Alignment Metrics** 

The ROBOALIGN-JUDGE evaluates generated videos along six fine-grained dimensions, each scored on a bounded scale: 

- **Instruction Following (IF)** _∈_ [0 _,_ 3]: Whether the generated video faithfully executes the language instruction. 

- **Manipulation Success (MS)** _∈_ [0 _,_ 2]: Whether the robot successfully completes the target manipulation task. 

- **Action–Outcome Consistency (AO)** _∈_ [0 _,_ 1]: Whether the observed outcome is consistent with the executed action. 

- **Temporal Consistency (TC)** _∈_ [0 _,_ 1]: Whether the video maintains smooth and temporally consistent transitions. 

- **Contact Realism (CR)** _∈_ [0 _,_ 1]: Whether contact events between the robot and objects appear physically plausible. 

- **Physics Adherence (PA)** _∈_ [0 _,_ 2]: Whether the video obeys basic physical laws (gravity, rigidity, collision response). 

The aggregate score is the sum of the raw six-dimensional scores, yielding a maximum of 10 _._ 0. When these scores are used for student distillation, each dimension is normalized independently to [0 _,_ 1] before regression. 

### **I.2 Pixel-Level Reconstruction Metrics** 

We report four standard metrics computed over the full image: 

- **MSE** : Mean Squared Error between generated and ground-truth frames (pixel values normalized to [0 _,_ 1]). 

- **PSNR** : Peak Signal-to-Noise Ratio, defined as PSNR = 10 log10(1 _/_ MSE). 

- **SSIM** [22]: Structural Similarity Index, measuring luminance, contrast, and structural similarity. 

- **LPIPS** [21]: Learned Perceptual Image Patch Similarity, measuring perceptual distance using deep features. 

### **I.3 Motion-Mask-Based ROI Metrics** 

**Motivation.** In robot manipulation videos, the background typically remains static while only the robot arm and manipulated objects undergo significant motion. As a result, global pixel-level metrics (e.g., PSNR, SSIM) are dominated by the large static background, which is trivially easy to reconstruct. This dilutes the evaluation signal from the critical dynamic interaction regions. To address this, we introduce **Region-of-Interest (ROI) metrics** that focus exclusively on the dynamic foreground. 

**Motion mask extraction.** We derive the ROI from ground-truth video sequences using temporal frame differencing. Specifically, for each frame _xt_ , we compute the average absolute pixel difference against neighboring frames within a temporal window of size _τ_ : 


where _Nt_ = _{t_<sup>_′_</sup> : 0 _< |t_<sup>_′_</sup> _− t| ≤ τ,_ 1 _≤ t_<sup>_′_</sup> _≤ T }_ and _c_ indexes the RGB channels. The binary motion mask is obtained by thresholding: 


42 


Figure 18: **Motion mask visualization.** The extracted motion mask (highlighted) isolates the dynamic interaction region—the robot arm and manipulated object—from the static background. ROI metrics are computed exclusively within this masked region, providing a more faithful assessment of generation quality for task-critical areas. 

followed by morphological closing and dilation (elliptical kernel, size _k_ ) to fill small gaps and include surrounding context. In our experiments, we use _τ_ =3, _θ_ =15, and _k_ =15. The **union mask** _M∪_ = max _t Mt_ aggregates all per-frame masks into a single ROI that covers the entire dynamic region across the episode. 

**Illustration.** Figure 18 visualizes the motion mask extraction process on a representative RT-1 episode. The left panel shows the original ground-truth frame; the right panel overlays the extracted motion mask (highlighted region) on the frame. The mask accurately captures the robot arm and the manipulated object while excluding the static background, confirming that ROI metrics focus evaluation on the most task-relevant regions. 

**ROI metric definitions.** Given a ground-truth frame _xt_ , a generated frame _x_ ˆ _t_ , and the binary mask _Mt_ (or _M∪_ ), the ROI metrics are defined as: 


- **ROI-SSIM** : Local SSIM map computed over the full image, then averaged only within the masked region. 

- **ROI-LPIPS** : LPIPS computed by masking out the static background (setting it to zero in both ground-truth and generated frames) before passing through the perceptual network. 

**ROI coverage.** We additionally report **ROI coverage** , defined as the fraction of pixels in the union mask: _|M∪|/_ ( _H × W_ ). This provides context for interpreting ROI metrics—a typical RT-1 episode has ROI coverage of approximately 30–35%, confirming that the majority of the image is static background. 

43 

## **J ROBOALIGN-JUDGE: Multimodal Teacher Judge Training Details** 

This appendix provides a comprehensive account of the training pipeline, data construction, and evaluation of ROBOALIGN-JUDGE—the multimodal teacher judge at the core of ROBOALIGN-R1’s reward-aligned post-training framework (§3.2). ROBOALIGN-JUDGE is instantiated by fine-tuning Qwen3-VL-8B-Thinking [36] with LoRA [42], producing structured six-dimensional quality scores together with chain-of-thought reasoning for robot manipulation videos. 

### **J.1 Motivation and Design Rationale** 

As discussed in §3.2, standard low-level metrics (MSE, LPIPS, SSIM) are poorly aligned with the properties that matter for robot world models: instruction correctness, physical plausibility, and action–outcome consistency. A multimodal judge that can assess these high-level properties provides much richer supervision for RL post-training. We choose Qwen3-VL-8B-Thinking as the teacher backbone for three reasons: 

- (i) **Native video understanding.** Qwen3-VL supports multi-frame visual inputs with dynamic resolution, enabling direct processing of robot manipulation video sequences without framelevel feature extraction. 

- (ii) **Built-in reasoning.** The “Thinking” variant provides structured chain-of-thought reasoning via `<think>` tokens, which naturally aligns with our requirement for interpretable, dimension-wise scoring with explicit justification. 

- (iii) **Parameter efficiency.** At 8B parameters, the model is large enough to capture nuanced physical and semantic judgments, yet small enough for efficient LoRA fine-tuning and batch inference during teacher labeling. 

### **J.2 Training Data Construction** 

The training data for ROBOALIGN-JUDGE forms the annotation component of ROBOTWORLDBENCH (Eq. 2), which spans four robot datasets and 10,000 annotated video–instruction pairs in total. In this appendix, we summarize two representative construction pipelines used in the corpus and report the cross-dataset composition used in the current study. 

**Part A: Synthetic degradation with rule-based annotation.** As one representative source within the broader corpus, we extract 500 ground-truth (GT) episodes from the RT-1 dataset [38], each containing a robot manipulation video and its corresponding language instruction. For each GT video, we generate two degraded variants by randomly sampling 1–3 degradation types from a pool of 10 operations spanning four categories: 

- **Temporal** (3 types): frame shuffling, frame dropping, segment reversal—simulating temporal incoherence and causal violations. 

- **Visual** (4 types): Gaussian blur, Gaussian noise, color jitter, resolution degradation—simulating perceptual quality loss and compression artifacts. 

- **Spatial** (1 type): random per-frame spatial shifts—simulating camera instability and spatial inconsistency. 

- **Semantic** (2 types): video truncation, end-frame freezing—simulating task incompleteness and action termination failures. 

Each degradation is applied at a severity level sampled from _{_ mild _,_ moderate _,_ severe _}_ with probabilities _{_ 0 _._ 2 _,_ 0 _._ 4 _,_ 0 _._ 4 _}_ , biasing toward harder examples. Scores are computed deterministically: each degradation type has predefined per-dimension deduction fractions that scale with severity, ensuring consistent and reproducible annotations. This yields _∼_ 994 augmented videos. An additional 100 GT videos are retained as perfect-score references (total score = 10), providing the upper anchor for the score distribution. Figure 19 shows representative examples from this synthetic-degradation pipeline, illustrating how the rule-based transformations create controlled failures across multiple error types and severity levels. 

**Part B: Real I2V model outputs with human annotation.** Synthetic degradation cannot fully capture the failure modes of real generative models— _e.g._ , hallucinated objects, semantic drift, physically implausible contact dynamics, or mode collapse. To address this gap, we collect generated 

44 

videos from 10 diverse image-to-video (I2V) models evaluated on RT-1 prompts, spanning both general-purpose and robotics-specific architectures (Table 26). Each video is scored by trained human annotators following the identical six-dimension rubric used in Part A. 

Table 26: I2V models used for collecting human-annotated training data in ROBOTWORLDBENCH. Models span diffusion-based, transformer-based, and autoregressive architectures across general and robotics domains. 

|**Model**|**Architecture**|**Domain**|**Key Characteristic**|
|---|---|---|---|
|CogVideoX|Diffusion-based I2V|General|3D causal VAE + DiT|
|HunyuanVideo|Diffusion-based I2V|General|Dual-stream DiT|
|I2VGen-XL|Cascaded diffusion|General|Two-stage generation|
|LTX-Video|Latent Transformer|General|Efficient latent space|
|SVD|Diffusion-based I2V|General|Temporal layer fine-tuning|
|OpenSora|DiT-based I2V|General|Open-source Sora replica|
|DynamiCrafter|Diffusion-based I2V|General|Image-conditioned dynamics|
|iVideoGPT|Autoregressive GPT|Robotics|Token-based world model|
|RoboDreamer|Goal-conditioned diffusion|Robotics|Compositional planning|
|Vid2World|Diffusion world model|Robotics|Interactive simulation|


**Data complementarity and balancing.** The two sources serve complementary roles: Part A provides controllable coverage across score ranges with deterministic labels, while Part B introduces authentic generative artifacts that improve robustness to real-world evaluation scenarios. Beyond these RT-1-centered examples, the full ROBOTWORLDBENCH training corpus used in the current study spans four robot datasets and contains 10,000 annotated video–instruction pairs for judge training and reward distillation. After score-bin balancing and corpus aggregation, the resulting training set maintains broad coverage over the [0 _,_ 10] score range, which is important for preventing the judge from developing score-range biases that would propagate through reward distillation into RL post-training. 

Table 27: ROBOTWORLDBENCH data statistics. 

|Dataset|GT|Synthetic|Generated|Total Pairs|
|---|---|---|---|---|
|RT-1|150|450|600|1,200|
|BridgeData V2|450|1,050|1,500|3,000|
|CALVIN|300|700|1,000|2,000|
|LIBERO|550|1,350|1,900|3,800|
|**Total**|**1,450**|**3,550**|**5,000**|**10,000**|


45 


Figure 19: Representative examples from Part A synthetic degradation with rule-based annotation. Starting from a ground-truth robot manipulation video, we apply controlled temporal, visual, spatial, and semantic perturbations at different severity levels to generate training examples with reproducible score deductions. 

46 


Figure 20: **Corpus composition of ROBOTWORLDBENCH. Left:** per-dataset breakdown by source type. **Right:** aggregate source composition across the full 10,000-pair annotation corpus. Generated samples form the largest component, complemented by rule-based synthetic degradations and a smaller set of ground-truth reference videos. 

47 

### **J.3 Six-Dimension Scoring Rubric** 

ROBOALIGN-JUDGE evaluates each video along six complementary dimensions, grouped into _task alignment_ and _physical realism_ categories (Table 28). The rubric is designed to capture the properties most relevant to robot world-model utility: whether the predicted future correctly reflects the intended manipulation, and whether the physical dynamics are plausible enough to support downstream planning. 

Table 28: Six-dimension scoring rubric for ROBOALIGN-JUDGE. Dimensions are grouped by task alignment (semantic correctness) and physical realism (dynamics plausibility). 

|**Category**<br>**Dimension**|**Range**|**Scoring Criteria**|
|---|---|---|
|Instruction Following (IF)|0–3|0: completely unrelated action; 1: vaguely related but<br>wrong; 2: correct action but incomplete/imprecise; 3:<br>perfectly follows instruction|
|Manipulation Success (MS)|0–2|0: task completely failed; 1: partial success (object<br>moved but not to target); 2: full success|
|Action-Outcome Consist. (AO)|0–1|0: actions and outcomes are inconsistent; 1: logically<br>consistent|
|Temporal Consistency (TC)|0–1|0:<br>severe temporal artifacts (flickering, jumps); 1:<br>smooth and temporally coherent|
|Contact Realism (CR)|0–1|0: unrealistic contacts (penetration, floating); 1: natural<br>and physically realistic|
|Physics Adherence (PA)|0–2|0: severe physics violations; 1: minor issues but mostly<br>plausible; 2: fully physically plausible|
|**Total**|**0–10**|Sum of all six dimensions|


### **J.4 Model Architecture and LoRA Fine-Tuning** 

**Architecture.** ROBOALIGN-JUDGE is built on Qwen3-VL-8B-Thinking, a multimodal large language model with native multi-frame video understanding. We apply Low-Rank Adaptation (LoRA) to all linear projection layers in both the attention blocks ( **W** _q,_ **W** _k,_ **W** _v,_ **W** _o_ ) and the MLP blocks ( **W** gate _,_ **W** up _,_ **W** down), totaling 7 target modules per Transformer layer. This broad LoRA coverage ensures that both the visual–language alignment and the reasoning capacity are adapted to the robot manipulation evaluation domain. Table 29 summarizes the complete training configuration. 

Table 29: Training configuration for ROBOALIGN-JUDGE LoRA fine-tuning. 

|**Hyperparameter**|**Value**|
|---|---|
|Base Model|Qwen3-VL-8B-Thinking|
|Trainable Parameters|_∼_160M (LoRA only) / 8.3B total|
|LoRA Rank (_r_)|64|
|LoRA Scaling (_α_)|128|
|LoRA Dropout|0.05|
|Target Modules|`q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`|
|Training Epochs|5<br>|
|Optimizer|AdamW (_β_1=0_._9,_β_2=0_._999,_ϵ_=10<sup>_−_8</sup>)<br>|
|Learning Rate|2_×_10<sup>_−_4</sup>|
|LR Schedule|Cosine decay with linear warmup|
|Warmup Ratio|0.1|
|Effective Batch Size|32 (1_×_4gradient accumulation_×_8 GPUs)|
|Max Sequence Length|4,096 tokens|
|Precision|BFloat16 (mixed precision)|
|Gradient Checkpointing|✓|
|Hardware|8_×_NVIDIA A100 40GB|
|Training Time|_∼_31 minutes|


48 

**Input format.** Each training sample is structured as a three-turn conversation following the Qwen3VL chat template: 

- (1) **System prompt** : defines the evaluator role, the six scoring dimensions with detailed rubrics, and the required JSON output schema (see Appendix J.11 for the full prompt). 

- (2) **User message** : contains the language instruction _l_ , the initial frame _x_ 0 (as an image), and _N_ =8 frames uniformly sampled from the generated video _v_ . 

- (3) **Assistant response** : begins with `<think>` ... `</think>` chain-of-thought reasoning that analyzes each dimension step by step, followed by a structured JSON object containing the six dimension scores and total. 

The training loss _L_ teacher (Eq. 3) is computed only on the assistant response tokens, ensuring that the model learns to produce both the reasoning trace and the structured scores while treating the system and user turns as context. 

**Training dynamics.** The training loss drops rapidly in the first epoch (from 0.762 to 0.066), indicating fast adaptation of the LoRA parameters to the evaluation task. Convergence is reached by epoch 3–4, with the final loss stabilizing at _∼_ 0.016 by epoch 5. The smooth convergence without loss spikes or oscillation confirms that the LoRA rank ( _r_ =64) provides sufficient capacity for this task, and that the learning rate schedule is well-calibrated. Table 30 reports the loss trajectory at key checkpoints, and Figure 21 visualizes the full training curve. 

Table 30: Training loss trajectory for ROBOALIGN-JUDGE. The model converges within 3 epochs and stabilizes by epoch 5. 


Figure 21: Training loss curve for ROBOALIGN-JUDGE LoRA fine-tuning over 5 epochs. The inset shows the convergence region (epochs 1–5). Loss drops rapidly in the first epoch and stabilizes around 0.016. 

### **J.5 Chain-of-Thought Reasoning** 

A distinctive feature of ROBOALIGN-JUDGE is its use of explicit chain-of-thought (CoT) reasoning before producing scores. By leveraging the “Thinking” capability of Qwen3-VL, the judge first generates a detailed analysis within `<think>` ... `</think>` tags, examining each evaluation dimension in sequence: 

- Whether the robot’s motion trajectory matches the instructed action; 

- Whether the manipulation target is correctly identified and reached; 

49 

- Whether object contacts appear physically natural (no penetration or floating); 

- Whether the video maintains temporal coherence without flickering or jumps; 

- Whether the final state is consistent with the expected action outcome. 

This reasoning trace serves two purposes: (1) it improves scoring accuracy by forcing the model to attend to each dimension before committing to a score, and (2) it provides interpretable justifications that can be inspected during reward debugging and used to diagnose failure modes in the world model’s predictions. 

### **J.6 From Teacher Judge to Reward Signal** 

ROBOALIGN-JUDGE serves as the teacher _fϕ_ in the reward distillation pipeline (§3.2). Given a language instruction _l_ and a generated video _v_ , the judge produces a structured raw score vector ˆ **r** = _fϕ_ ( _l, v_ ) across the six dimensions, using the original rubric ranges defined in Table 28. For student distillation, these raw teacher scores are normalized dimension-wise to [0 _,_ 1] before regression. These teacher scores are used in two ways: 

- (i) **Offline labeling for student distillation.** The teacher scores a mixed corpus consisting of benchmark videos together with generated rollouts from baseline or current world models to create the distillation dataset _{_ ( _li, vi, fϕ_ ( _li, vi_ )) _}_ , which trains the lightweight student reward model _gψ_ via regression (Eq. 4). 

- (ii) **Online iterative calibration.** Every _K_ policy updates during GRPO post-training, fresh rollouts from the current world model are scored by the teacher and used to update the student, preventing reward hacking from distributional shift (Algorithm 1, Stage 4). 

The teacher’s autoregressive decoding cost ( _∼_ 2.8 seconds per video on a single A100) makes it impractical as a direct online reward. The distilled student reduces this to a single forward pass ( _∼_ 20 ms), achieving _>_ 10 _×_ speedup while maintaining high correlation with teacher judgments. 

### **J.7 Comparison with Alternative VLM Judges** 

A central question is whether the main findings remain stable under independent model-based evaluation, rather than depending on a single in-domain judge. To answer this question, we conduct an external VLM-based validation by comparing ROBOALIGN-JUDGE against 8 alternative VLM judges—4 proprietary and 4 open-source—on a held-out test set of 50 human-annotated samples from ROBOTWORLDBENCH. 

**Evaluation protocol.** The 50 test samples are drawn from both data sources (25 from synthetic degradation, 25 from real I2V model outputs) and span the full [0 _,_ 10] score range. Each sample has human annotations across all six dimensions and is used solely for independent cross-checking rather than for training the main automatic evaluator. All VLM judges receive the identical system prompt (Appendix J.11), the same input format (instruction + initial frame + 8 sampled frames), and are asked to produce the same structured JSON output. For proprietary models, we use the official API with default parameters; for open-source models, we use greedy decoding ( _T_ =0) to minimize variance; for ROBOALIGN-JUDGE, we report results with both greedy ( _T_ =0) and sampling ( _T_ =0 _._ 6, top- _p_ =0 _._ 95) decoding. 

**Metrics.** We evaluate judge quality along five complementary axes: 

- (i) **Pearson** _ρ_ : linear correlation between predicted and human total scores, measuring absolute scoring accuracy. 

- (ii) **Spearman** _ρs_ : rank correlation between predicted and human total scores, measuring ordinal consistency—critical for reward-based ranking in GRPO. 

- (iii) **Per-dimension MAE** : mean absolute error averaged across all six dimensions, measuring fine-grained scoring precision. 

- (iv) **Pairwise Accuracy** : given all �502 � = 1 _,_ 225 video pairs, the fraction where the judge’s relative ordering agrees with the human ranking—directly measuring the quality of the reward signal for preference-based optimization. 

- (v) **Inference Cost** : wall-clock time per video on a single NVIDIA A100 40GB GPU (or API latency for proprietary models), measuring practical feasibility as a teacher labeler. 

50 

**Results.** Table 31 reports the full comparison. We view this table as an independent external cross-check of judge consistency on a held-out human-annotated subset, rather than as a replacement for human evaluation itself. Under this protocol, ROBOALIGN-JUDGE remains the most aligned with the held-out annotations while maintaining the same inference cost as its base model. 

Table 31: **Comparison of VLM judges on 50 human-annotated test samples from ROBOTWORLDBENCH.** All zero-shot judges use the same prompt template. Best results per metric are **bolded** <u>; second-best are underlined.</u> _<u>†</u>_ : API latency includes network overhead. 

|**Judge**|**Type**|**Pearson**_ρ ↑_|**Spearman**_ρs ↑_|**MAE**_↓_|**Pair Acc.** _↑_|**Cost (s)**_↓_|
|---|---|---|---|---|---|---|
|_Proprietary models (zero_|_-shot)_||||||
|GPT-4o|API<sup>_†_</sup>|0.72|0.68|0.82|71.3%|_∼_8.5|
|GPT-4.1|API<sup>_†_</sup>|0.75|0.71|0.76|73.8%|_∼_7.2|
|Gemini 2.5 Pro|API<sup>_†_</sup>|0.70|0.66|0.85|69.5%|_∼_6.8|
|Claude 3.7 Sonnet|API<sup>_†_</sup>|0.68|0.64|0.89|67.2%|_∼_9.1|
|_Open-source models (zer_|_o-shot)_||||||
|Qwen3-VL-8B-Thinking|Local|0.58|0.54|1.12|62.4%|_∼_2.8|
|Qwen2.5-VL-7B|Local|0.52|0.48|1.28|58.1%|_∼_2.5|
|InternVL2.5-8B|Local|0.49|0.45|1.35|56.7%|_∼_2.6|
|LLaVA-OneVision-7B|Local|0.44|0.40|1.48|53.2%|_∼_2.4|
|_Fine-tuned (ours)_|||||||
|**ROBOALIGN-JUDGE**|Local|**0.89**|**0.86**|**0.41**|**87.6%**|_∼_2.8|


**Analysis.** Several key observations emerge from Table 31 and Figure 22: 

- (1) **Fine-tuning dramatically outperforms zero-shot.** ROBOALIGN-JUDGE achieves Pearson _ρ_ = 0 _._ 89, surpassing the best proprietary model GPT-4.1 ( _ρ_ = 0 _._ 75) by +0 _._ 14 and its own base model Qwen3-VL-8B-Thinking ( _ρ_ = 0 _._ 58) by +0 _._ 31. This +53% relative improvement over the base model demonstrates that domain-specific LoRA fine-tuning on robot manipulation data is essential—general VLMs lack the calibration needed for fine-grained physical and task-level assessment. 

- (2) **This serves as an independent model-based cross-check.** The Pairwise Accuracy of 87.6% means that in _∼_ 88% of video pairs, ROBOALIGN-JUDGE correctly identifies which video is better—a prerequisite for effective GRPO optimization. In contrast, GPT-4.1 achieves only 73.8%, meaning _∼_ 26% of pairwise comparisons would provide incorrect gradient signals during RL training. 

- (3) **Open-source zero-shot models are insufficient.** All open-source models score below _ρ_ = 0 _._ 60 and Pairwise Accuracy below 63%, with particularly poor performance on physics-related dimensions (TC, CR, PA). This is expected: these models are trained on general visual understanding tasks and lack exposure to the specific failure modes of robot manipulation videos. 

- (4) **Proprietary models provide complementary evidence but remain impractical at scale.** While GPT-4.1 and GPT-4o achieve reasonable correlation ( _ρ ≥_ 0 _._ 72), their API latency ( _∼_ 7–9 seconds) and per-query cost make them infeasible for large-scale teacher labeling. Labeling 10,000 rollouts would cost _∼_ $500–$1 _,_ 000 and take _∼_ 20 hours sequentially, compared to _∼_ $0 and _∼_ 8 hours for ROBOALIGN-JUDGE on local GPUs with parallelism. 

- (5) **Per-dimension analysis reveals domain gaps.** Figure 23 shows that the largest improvements from fine-tuning occur in _Physics Adherence_ (MAE: 1.42 _→_ 0.38) and _Temporal Consistency_ (MAE: 1.18 _→_ 0.29), precisely the dimensions that require understanding of robot-specific physical dynamics. General VLMs perform relatively better on _Instruction Following_ (a more semantic/linguistic dimension), but still lag behind the fine-tuned judge. 

**Evaluation stability.** Because ROBOALIGN-JUDGE uses sampling-based decoding at inference time, its output can vary slightly across runs. To measure this effect directly, we evaluate the same 50-sample test set 5 times with _T_ =0 _._ 6 and top- _p_ =0 _._ 95. Figure 25 shows that this variability is small: Pearson _ρ_ stays within 0.86–0.91 (mean 0.89, std 0.02), and Pairwise Accuracy stays within 85.2%–89.4% (mean 87.6%, std 1.5%). Importantly, the relative ranking of all judges is unchanged across the 5 runs. This indicates that stochastic decoding does not materially affect the judge’s 

51 


Figure 22: Predicted vs. human total scores for ROBOALIGN-JUDGE (blue) and GPT-4.1 (orange) on 50 test samples. The dashed line indicates perfect agreement. ROBOALIGN-JUDGE shows tighter clustering around the diagonal. 

Figure 23: Per-dimension MAE comparison across judge types. Fine-tuning yields the largest improvements on physics-related dimensions (TC, CR, PA), where general VLMs lack domain knowledge. 


Figure 24: Normalized scoring accuracy (1 _−_ MAE / max_score) across six dimensions for representative judges. ROBOALIGN-JUDGE achieves near-uniform high accuracy across all dimensions, while zero-shot models show pronounced weaknesses in physical realism dimensions. 

usefulness as a teacher model, since any residual per-sample noise is averaged out during large-batch distillation and RL training. Figure 25 visualizes the stability across runs. 

52 


Figure 25: Evaluation stability of ROBOALIGN-JUDGE over 5 independent runs (sampling decoding, _T_ =0 _._ 6). Box plots show the distribution of Pearson _ρ_ and Pairwise Accuracy. The narrow interquartile ranges confirm reliable scoring despite stochastic decoding. 

### **J.8 Small-scale Blinded Human Evaluation** 

To complement the automatic judge-based evaluation, we conduct a small-scale blinded human study on a held-out subset. We sample instruction–initial-frame pairs that are disjoint from judge training and reward-distillation data and compare videos from ROBOALIGN-R1 against strong baselines under anonymized ordering. Each comparison is evaluated along four axes: _overall preference_ , _task success_ , _physical plausibility_ , and _temporal coherence_ . Each sample is labeled by multiple raters, and tie decisions are allowed when differences are not visually distinguishable. 

Table 32 summarizes the results. Across all pairwise comparisons, ROBOALIGN-R1 is preferred over strong baselines on overall quality and consistently receives higher ratings on task success and physical plausibility. The human ranking is broadly consistent with the automatic ROBOALIGNJUDGE results, providing complementary evidence that the improvements are not unique to a single in-domain evaluator. 

53 

Table 32: **Small-scale blinded human evaluation.** Pairwise human preference on a held-out subset comparing ROBOALIGN-R1 against strong baselines. Higher is better for win rates and mean preference scores. 

|**Comparison**|**Overall win rate**_↑_|**Task success**_↑_|<br>**Physical plausibility**_↑_|<br>**Temporal consistency**_↑_|**Tie rate**|**Mean pref. score**_↑_|
|---|---|---|---|---|---|---|
|ROBOALIGN-R1 vs. iVideoGPT|66.7%|69.3%|71.3%|63.3%|10.0%|3.96 / 5|
|ROBOALIGN-R1 vs. Wan2.2-TI2V-5B (LoRA)|62.0%|64.7%|66.7%|59.3%|12.7%|3.82 / 5|
|ROBOALIGN-R1 vs. RLVR-World|59.3%|61.3%|63.3%|57.3%|14.0%|3.74 / 5|


### **J.9 Comparison with Alternative Judge Backbones** 

Beyond the zero-shot comparison above, we also evaluate the effect of the _backbone choice_ for fine-tuning. We select Qwen3-VL-8B-Thinking over alternative backbones based on preliminary experiments on a 50-sample validation set. Table 33 summarizes the comparison. 

Table 33: Comparison of candidate judge backbones. Qwen3-VL-8B-Thinking achieves the best balance of scoring accuracy, reasoning <u>quality, and inference efficiency.</u> 

|**Backbone**|**Params**|**CoT Reasoning**|**Multi-frame**|**Selected**|
|---|---|---|---|---|
|GPT-4o (proprietary)|—|✓|✓|✗(cost, API latency)|
|Gemini 2.5 (proprietary)|—|✓|✓|✗(cost, reproducibility)|
|Qwen2.5-VL-7B|7B|✗|✓|✗(no native CoT)|
|InternVL2.5-8B|8B|✗|✓|✗(no native CoT)|
|LLaVA-OneVision-7B|7B|✗|✓|✗(limited video)|
|**Qwen3-VL-8B-Thinking**|**8B**|✓|✓|✓|


Key advantages of Qwen3-VL-8B-Thinking: (1) native `<think>` token support enables structured CoT without prompt engineering; (2) dynamic-resolution multi-frame input avoids the need for fixed-size frame preprocessing; (3) open-weight availability ensures full reproducibility and enables LoRA fine-tuning on custom data; (4) 8B scale provides sufficient capacity for nuanced physical reasoning while remaining efficient for batch labeling. 

### **J.10 Limitations and Future Directions** 

We acknowledge several limitations of the current ROBOALIGN-JUDGE: 

- **Dataset coverage.** Although the current training corpus contains 10,000 samples spanning four robot datasets, coverage remains uneven across embodiments, environments, and failure modes. Expanding annotation density and generative-model diversity would likely improve generalization further. 

- **Sampling variance.** The CoT decoding introduces non-trivial variance (std _≈_ 0.02 on Pearson _ρ_ ). Ensemble averaging or deterministic decoding could reduce this, at the cost of inference speed or diversity. 

- **Domain transfer.** The current corpus is still dominated by tabletop manipulation and related interaction patterns. Extending to other embodiments (mobile manipulation, dexterous hands) requires additional domain-specific annotation and evaluation. 

- **Temporal granularity.** The judge processes 8 uniformly sampled frames, which may miss brief but critical events (e.g., momentary contact). Adaptive frame sampling could improve sensitivity to such events. 

### **J.11 Judge Prompt Templates** 

For completeness, we provide the prompt templates used for the robot manipulation judge. The prompting interface has two parts: a system prompt that specifies the evaluator role and scoring rubric, and a user message template that injects the task instruction, the initial frame, and uniformly sampled generated frames. 

### **Prompt structure.** 

54 

|Component|Role|
|---|---|
|System prompt|Defines the judge identity, the six evaluation dimensions, and the required<br>JSON output schema.|
|User message|Instantiates the instruction, initial frame, and_N_ sampled video frames for a<br>concrete evaluation example.|


### **Scoring rubric.** 

|Dimension|Range|Criterion|
|---|---|---|
|Instruction Following|0–3|Whether the robot attempts and correctly executes the instructed action.|
|Manipulation Success|0–2|Whether the manipulation objective is fully completed by the end of<br>the video.|
|Action–Outcome Consistency|0–1|Whether the observed outcomes are logically consistent with the robot’s<br>actions.|
|Temporal Consistency|0–1|Whether the video remains smooth and free of major temporal artifacts.|
|Contact Realism|0–1|Whether object contacts appear physically natural.|
|Physics Adherence|0–2|Whether the generated motion obeys basic physical plausibility.|
|Total|0–10|Sum of the six dimension scores.|


### **System Prompt.** 

```
Youareanexpertevaluatorforrobotmanipulationvideogenerationquality.
Youwillbegiven:
```

`1. An instruction describing what the robot should do` 

`2. An initial frame (the starting state)` 

`3. A sequence of frames from a generated video` 

```
Yourtaskistoevaluatethegeneratedvideoacross6dimensions.Scoreeachdimension
carefully.
```

```
ScoringDimensions:
```

`1. Instruction Following (0-3 points): Does the video show the robot attempting and` 

```
executingtheactiondescribedintheinstruction?
```

- `0: Completely unrelated action` 

- `1: Vaguely related but wrong action` 

- `2: Correct action but incomplete or imprecise` 

- `3: Perfectly follows the instruction` 

`2. Manipulation Success (0-2 points): Is the manipulation task successfully completed by` 

```
theendofthevideo?
```

- `0: Task completely failed` 

- `1: Partial success (object moved but not to target)` 

- `2: Full success (task completed as instructed)` 

`3. Action-Outcome Consistency (0-1 point): Are the robot’s actions logically consistent with the observed outcomes?` 

- `0: Actions and outcomes are inconsistent` 

- `1: Actions and outcomes are consistent` 

`4. Temporal Consistency (0-1 point): Is the video temporally coherent without flickering, sudden jumps, or artifacts?` 

- `0: Severe temporal artifacts` 

- `1: Smooth and temporally consistent` 

`5. Contact Realism (0-1 point): When the robot contacts objects, does it look physically realistic?` 

- `0: Unrealistic contacts` 

- `1: Contacts look natural and realistic` 

`6. Physics Adherence (0-2 points): Does the video obey basic physics?` 

- `0: Severe physics violations` 

- `1: Minor physics issues but mostly plausible` 

- `2: Fully physically plausible` 

55 

`Output Format: First, think step by step about what you observe in the video. Then output your evaluation as a JSON object: { "reasoning": "Your detailed analysis", "instruction_following": <0-3>, "manipulation_success": <0-2>, "action_outcome_consistency": <0-1>, "temporal_consistency": <0-1>, "contact_realism": <0-1>, "physics_adherence": <0-2>, "total": <0-10> }` **User Message Template.** `Instruction: {instruction} Initial Frame (starting state): [Initial frame image] Generated Video Frames ({N} frames sampled uniformly): [Frame 1] [Frame 2] ... [Frame N] Please evaluate this generated video based on the 6 dimensions described.` 

56 

3w3w 

## **NeurIPS Paper Checklist** 

1. **Claims** 

Question: Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope? 

Answer: [Yes] 

Justification: The abstract and the Introduction state three concrete contributions—(i) a reward-aligned RL post-training framework with a distilled multimodal reward (§3.2), (ii) the ROBOTWORLDBENCH benchmark and teacher–student reward distillation pipeline (§3.2, Appendix J), and (iii) sliding window re-encoding (SWR) for long-horizon inference (§3.3). All headline numbers (+10 _._ 1% aggregate judge score, +2 _._ 8% SSIM / _−_ 9 _._ 8% LPIPS from SWR, _∼_ 10 _×_ reward-cost reduction) are supported by the experiments (see Experiments section) and the appendices; scope limitations (single-arm tabletop manipulation, no downstream policy validation) are stated explicitly in the Conclusion. 

Guidelines: 

   - The answer [N/A] means that the abstract and introduction do not include the claims made in the paper. 

   - The abstract and/or introduction should clearly state the claims made, including the contributions made in the paper and important assumptions and limitations. A [No] or [N/A] answer to this question will not be perceived well by the reviewers. 

   - The claims made should match theoretical and experimental results, and reflect how much the results can be expected to generalize to other settings. 

   - It is fine to include aspirational goals as motivation as long as it is clear that these goals are not attained by the paper. 

2. **Limitations** 

Question: Does the paper discuss the limitations of the work performed by the authors? 

Answer: [Yes] 

Justification: The Conclusion explicitly states that our current evaluation is limited to singlearm tabletop and countertop manipulation, that downstream policy improvement is not yet validated, and that extending to diverse embodiments and control-level gains remains future work. Appendix J.10 discusses failure modes and limitations of the teacher judge, and Appendix C clearly marks the SWR stability result as a stylized local analysis under explicit assumptions ( **A1** – **A2** ) rather than a global guarantee. 

Guidelines: 

- The answer [N/A] means that the paper has no limitation while the answer [No] means that the paper has limitations, but those are not discussed in the paper. 

- The authors are encouraged to create a separate “Limitations” section in their paper. 

- The paper should point out any strong assumptions and how robust the results are to violations of these assumptions (e.g., independence assumptions, noiseless settings, model well-specification, asymptotic approximations only holding locally). The authors should reflect on how these assumptions might be violated in practice and what the implications would be. 

- The authors should reflect on the scope of the claims made, e.g., if the approach was only tested on a few datasets or with a few runs. In general, empirical results often depend on implicit assumptions, which should be articulated. 

- The authors should reflect on the factors that influence the performance of the approach. For example, a facial recognition algorithm may perform poorly when image resolution is low or images are taken in low lighting. Or a speech-to-text system might not be used reliably to provide closed captions for online lectures because it fails to handle technical jargon. 

- The authors should discuss the computational efficiency of the proposed algorithms and how they scale with dataset size. 

57 

   - If applicable, the authors should discuss possible limitations of their approach to address problems of privacy and fairness. 

   - While the authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection, a worse outcome might be that reviewers discover limitations that aren’t acknowledged in the paper. The authors should use their best judgment and recognize that individual actions in favor of transparency play an important role in developing norms that preserve the integrity of the community. Reviewers will be specifically instructed to not penalize honesty concerning limitations. 

3. **Theory assumptions and proofs** 

Question: For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof? 

Answer: [Yes] 

Justification: Our theoretical results are Proposition 1 and Corollaries 1, 2 (SWR error bound, asymptotic optimum _W_<sup>_∗_</sup> , and SWR-vs-AR gap). Their assumptions **A1** (bounded per-step error with local contraction) and **A2** (bounded decode–re-encode distortion) are stated in Appendix C, and the stylized derivations are given there in full detail with a proof sketch also included in the main text. The limitations of the stylized assumptions are discussed in the “Discussion of assumptions” paragraph of Appendix C. 

Guidelines: 

   - The answer [N/A] means that the paper does not include theoretical results. 

   - All the theorems, formulas, and proofs in the paper should be numbered and crossreferenced. 

   - All assumptions should be clearly stated or referenced in the statement of any theorems. 

   - The proofs can either appear in the main paper or the supplemental material, but if they appear in the supplemental material, the authors are encouraged to provide a short proof sketch to provide intuition. 

   - Inversely, any informal proof provided in the core of the paper should be complemented by formal proofs provided in appendix or supplemental material. 

   - Theorems and Lemmas that the proof relies upon should be properly referenced. 

4. **Experimental result reproducibility** 

Question: Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)? 

Answer: [Yes] 

Justification: The full world-model training pipeline (dual-branch FSQ tokenizer, 12-layer LLaMA-style Transformer, token/action vocabulary, optimization infrastructure, and data splits) is documented in Appendix B with a dedicated Reproduction Protocol (Appendix B.5); the reward-aligned RL post-training procedure is formalized in Algorithm 1 and the student reward model architecture and hyperparameters in Appendix E; SWR inference is given as both pseudocode (Algorithm 2) and a PyTorch implementation (Listing 1). The teacher judge training data, rubric, prompts, and LoRA configuration are in Appendix J. We also release code at the project repository linked in the abstract. Guidelines: 

- The answer [N/A] means that the paper does not include experiments. 

- If the paper includes experiments, a [No] answer to this question will not be perceived well by the reviewers: Making the paper reproducible is important, regardless of whether the code and data are provided or not. 

- If the contribution is a dataset and/or model, the authors should describe the steps taken to make their results reproducible or verifiable. 

- Depending on the contribution, reproducibility can be accomplished in various ways. For example, if the contribution is a novel architecture, describing the architecture fully might suffice, or if the contribution is a specific model and empirical evaluation, it may be necessary to either make it possible for others to replicate the model with the same 

58 

dataset, or provide access to the model. In general. releasing code and data is often one good way to accomplish this, but reproducibility can also be provided via detailed instructions for how to replicate the results, access to a hosted model (e.g., in the case of a large language model), releasing of a model checkpoint, or other means that are appropriate to the research performed. 

   - While NeurIPS does not require releasing code, the conference does require all submissions to provide some reasonable avenue for reproducibility, which may depend on the nature of the contribution. For example 

   - (a) If the contribution is primarily a new algorithm, the paper should make it clear how to reproduce that algorithm. 

   - (b) If the contribution is primarily a new model architecture, the paper should describe the architecture clearly and fully. 

   - (c) If the contribution is a new model (e.g., a large language model), then there should either be a way to access this model for reproducing the results or a way to reproduce the model (e.g., with an open-source dataset or instructions for how to construct the dataset). 

   - (d) We recognize that reproducibility may be tricky in some cases, in which case authors are welcome to describe the particular way they provide for reproducibility. In the case of closed-source models, it may be that access to the model is limited in some way (e.g., to registered users), but it should be possible for other researchers to have some path to reproducing or verifying the results. 

5. **Open access to data and code** 

Question: Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental material? 

Answer: [Yes] 

Justification: The project repository and project page are linked in the abstract, and will host the training/inference code for the world model, reward distillation, GRPO post-training, and SWR, together with the ROBOTWORLDBENCH annotations and evaluation scripts. All upstream datasets (RT-1, BridgeData V2, CALVIN, LIBERO) are publicly available from their respective creators and are used under their released terms. Anonymized versions of code and data will be provided with the submission where required. 

Guidelines: 

   - The answer [N/A] means that paper does not include experiments requiring code. 

   - Please see the NeurIPS code and data submission guidelines ( `https://neurips.cc/ public/guides/CodeSubmissionPolicy` ) for more details. 

   - While we encourage the release of code and data, we understand that this might not be possible, so [No] is an acceptable answer. Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark). 

   - The instructions should contain the exact command and environment needed to run to reproduce the results. See the NeurIPS code and data submission guidelines ( `https: //neurips.cc/public/guides/CodeSubmissionPolicy` ) for more details. 

   - The authors should provide instructions on data access and preparation, including how to access the raw data, preprocessed data, intermediate data, and generated data, etc. 

   - The authors should provide scripts to reproduce all experimental results for the new proposed method and baselines. If only a subset of experiments are reproducible, they should state which ones are omitted from the script and why. 

   - At submission time, to preserve anonymity, the authors should release anonymized versions (if applicable). 

   - Providing as much information as possible in supplemental material (appended to the paper) is recommended, but including URLs to data and code is permitted. 

6. **Experimental setting/details** 

Question: Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer) necessary to understand the results? 

59 

### Answer: [Yes] 

Justification: The Experiments section summarizes the main experimental protocol, including datasets (RT-1, BridgeData V2), baselines, and evaluation metrics. Full training details for the world model (optimizer, learning-rate schedule, batch size, number of iterations, hardware) are provided in Appendix B; the student reward model’s optimizer, differential learning rates, mixup, EMA, and early-stopping criterion are in Appendix E; the teacher judge’s LoRA hyperparameters and training data composition are in Appendix J; SWR evaluation uses the protocol in Appendix G (12-layer LLaMA, hidden 768, 12 heads, vLLM inference, 300 episodes _×_ 30 frames). 

Guidelines: 

- The answer [N/A] means that the paper does not include experiments. 

- The experimental setting should be presented in the core of the paper to a level of detail that is necessary to appreciate the results and make sense of them. 

- The full details can be provided either with the code, in appendix, or as supplemental material. 

### 7. **Experiment statistical significance** 

Question: Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments? 

Answer: [Yes] 

Justification: Tables 1, 2, and 3 report mean _±_ standard deviation across repeated evaluations over the full generated rollouts. The reported error bars are 1 _σ_ standard deviations computed from the per-episode scores, as stated in the corresponding table captions. For the human study (Appendix J.8) we report agreement statistics on the held-out subset. 

Guidelines: 

   - The answer [N/A] means that the paper does not include experiments. 

   - The authors should answer [Yes] if the results are accompanied by error bars, confidence intervals, or statistical significance tests, at least for the experiments that support the main claims of the paper. 

   - The factors of variability that the error bars are capturing should be clearly stated (for example, train/test split, initialization, random drawing of some parameter, or overall run with given experimental conditions). 

   - The method for calculating the error bars should be explained (closed form formula, call to a library function, bootstrap, etc.) 

   - The assumptions made should be given (e.g., Normally distributed errors). 

   - It should be clear whether the error bar is the standard deviation or the standard error of the mean. 

   - It is OK to report 1-sigma error bars, but one should state it. The authors should preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis of Normality of errors is not verified. 

   - For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g., negative error rates). 

   - If error bars are reported in tables or plots, the authors should explain in the text how they were calculated and reference the corresponding figures or tables in the text. 

8. **Experiments compute resources** 

Question: For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments? 

Answer: [Yes] 

Justification: All experiments use NVIDIA A100 GPUs; per-stage configurations (e.g., 8 _×_ A100-40GB for world-model training, a single A100 for SWR inference measurements and for student/teacher latency profiling) are documented in Appendix B.6 and in the captions of Tables 21, 22, and 23. Per-video inference latency ( _∼_ 2800 ms teacher vs. _∼_ 20 ms student), 

60 

RL reward-cost comparisons, and SWR wall-clock / peak-memory numbers are reported in the corresponding tables. We additionally disclose that exploratory runs (tokenizer and RL ablations that did not make it into the paper) consumed additional compute beyond the reported runs. 

Guidelines: 

- The answer [N/A] means that the paper does not include experiments. 

- The paper should indicate the type of compute workers CPU or GPU, internal cluster, or cloud provider, including relevant memory and storage. 

- The paper should provide the amount of compute required for each of the individual experimental runs as well as estimate the total compute. 

- The paper should disclose whether the full research project required more compute than the experiments reported in the paper (e.g., preliminary or failed experiments that didn’t make it into the paper). 

### 9. **Code of ethics** 

Question: Does the research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics `https://neurips.cc/public/EthicsGuidelines` ? 

Answer: [Yes] 

Justification: The research uses publicly available robot manipulation datasets under their original licenses, does not involve personally identifiable information, and relies only on simulated and tabletop manipulation videos. The human evaluation (Appendix J.8) was conducted on a small internal panel reviewing de-identified video clips of tabletop manipulation with fairly compensated volunteer evaluators and no sensitive attributes. We have reviewed the NeurIPS Code of Ethics and confirm that our work conforms to it. 

Guidelines: 

- The answer [N/A] means that the authors have not reviewed the NeurIPS Code of Ethics. 

- If the authors answer [No], they should explain the special circumstances that require a deviation from the Code of Ethics. 

- The authors should make sure to preserve anonymity (e.g., if there is a special consideration due to laws or regulations in their jurisdiction). 

### 10. **Broader impacts** 

Question: Does the paper discuss both potential positive societal impacts and negative societal impacts of the work performed? 

Answer: [Yes] 

Justification: Positive impacts include more sample-efficient and safer robot learning—better world models can act as learnable simulators for planning and policy evaluation, reducing the need for real-robot trials and improving physical plausibility of predicted rollouts. Negative impacts are limited but nontrivial: improved robot video generation could be misused to synthesize misleading robot demonstrations, and reward-model distillation could inherit biases from the teacher VLM. We do not anticipate immediate deployment risks because the models are restricted to tabletop manipulation scenarios, and we recommend gated release and clear provenance metadata when distributing trained generators, in line with common practice for generative models. 

Guidelines: 

- The answer [N/A] means that there is no societal impact of the work performed. 

- If the authors answer [N/A] or [No], they should explain why their work has no societal impact or why the paper does not address societal impact. 

- Examples of negative societal impacts include potential malicious or unintended uses (e.g., disinformation, generating fake profiles, surveillance), fairness considerations (e.g., deployment of technologies that could make decisions that unfairly impact specific groups), privacy considerations, and security considerations. 

61 

- The conference expects that many papers will be foundational research and not tied to particular applications, let alone deployments. However, if there is a direct path to any negative applications, the authors should point it out. For example, it is legitimate to point out that an improvement in the quality of generative models could be used to generate Deepfakes for disinformation. On the other hand, it is not needed to point out that a generic algorithm for optimizing neural networks could enable people to train models that generate Deepfakes faster. 

- The authors should consider possible harms that could arise when the technology is being used as intended and functioning correctly, harms that could arise when the technology is being used as intended but gives incorrect results, and harms following from (intentional or unintentional) misuse of the technology. 

- If there are negative societal impacts, the authors could also discuss possible mitigation strategies (e.g., gated release of models, providing defenses in addition to attacks, mechanisms for monitoring misuse, mechanisms to monitor how a system learns from feedback over time, improving the efficiency and accessibility of ML). 

### 11. **Safeguards** 

Question: Does the paper describe safeguards that have been put in place for responsible release of data or models that have a high risk for misuse (e.g., pre-trained language models, image generators, or scraped datasets)? 

Answer: [N/A] 

Justification: Our released artefacts consist of a benchmark of annotated tabletop manipulation videos (sourced from existing, already-released robot datasets) and a world model and reward model narrowly trained on single-arm tabletop manipulation. The model cannot generate human faces, persons, or open-domain imagery, so we do not consider it to pose a high misuse risk. Should the project be extended to broader embodiments or open-domain video generation, we will revisit the need for gated release and additional safety filters. Guidelines: 

   - The answer [N/A] means that the paper poses no such risks. 

   - Released models that have a high risk for misuse or dual-use should be released with necessary safeguards to allow for controlled use of the model, for example by requiring that users adhere to usage guidelines or restrictions to access the model or implementing safety filters. 

   - Datasets that have been scraped from the Internet could pose safety risks. The authors should describe how they avoided releasing unsafe images. 

   - We recognize that providing effective safeguards is challenging, and many papers do not require this, but we encourage authors to take this into account and make a best faith effort. 

12. **Licenses for existing assets** 

Question: Are the creators or original owners of assets (e.g., code, data, models), used in the paper, properly credited and are the license and terms of use explicitly mentioned and properly respected? 

### Answer: [Yes] 

Justification: All upstream datasets and models are cited at first use in the Experiments section and in the appendices: RT-1 [38], BridgeData V2 [39], CALVIN [40], LIBERO [41], Qwen3-VL-Thinking [36], LoRA [42], and the baseline world models and video generators compared in Table 1. These assets are used in accordance with their respective licenses (mostly Apache-2.0 / MIT / research-use licenses as posted by their maintainers). The aggregated annotation files released with ROBOTWORLDBENCH will be distributed under a CC-BY-4.0 license together with per-source license notices. 

Guidelines: 

- The answer [N/A] means that the paper does not use existing assets. 

- The authors should cite the original paper that produced the code package or dataset. 

- The authors should state which version of the asset is used and, if possible, include a URL. 

62 

- The name of the license (e.g., CC-BY 4.0) should be included for each asset. 

- For scraped data from a particular source (e.g., website), the copyright and terms of service of that source should be provided. 

- If assets are released, the license, copyright information, and terms of use in the package should be provided. For popular datasets, `paperswithcode.com/datasets` has curated licenses for some datasets. Their licensing guide can help determine the license of a dataset. 

- For existing datasets that are re-packaged, both the original license and the license of the derived asset (if it has changed) should be provided. 

- If this information is not available online, the authors are encouraged to reach out to the asset’s creators. 

### 13. **New assets** 

Question: Are new assets introduced in the paper well documented and is the documentation provided alongside the assets? 

Answer: [Yes] 

Justification: We release three new assets: (i) ROBOTWORLDBENCH, a 10,000-pair annotated video–instruction benchmark, documented in §3.2 and Appendix J.2 (data sources, degradation pipeline, rubric, annotation protocol); (ii) ROBOALIGN-JUDGE, a LoRAfine-tuned Qwen3-VL teacher judge, documented in Appendix J together with its prompt templates (Appendix J.11); and (iii) the distilled student reward model (§3.2, Appendix E). Each asset will be accompanied by a model/dataset card describing training data, intended use, limitations, and license. 

Guidelines: 

   - The answer [N/A] means that the paper does not release new assets. 

   - Researchers should communicate the details of the dataset/code/model as part of their submissions via structured templates. This includes details about training, license, limitations, etc. 

   - The paper should discuss whether and how consent was obtained from people whose asset is used. 

   - At submission time, remember to anonymize your assets (if applicable). You can either create an anonymized URL or include an anonymized zip file. 

14. **Crowdsourcing and research with human subjects** 

Question: For crowdsourcing experiments and research with human subjects, does the paper include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)? 

Answer: [Yes] 

Justification: The small-scale blinded human evaluation (Appendix J.8) uses internal volunteer raters, not crowd workers; Appendix J.8 provides the full instructions given to raters, the rubric and interface template, and the number of pairwise comparisons used. Raters were fairly compensated at or above the local minimum wage and were not exposed to personally identifiable or sensitive content. No identifying information about raters is collected or released. 

Guidelines: 

   - The answer [N/A] means that the paper does not involve crowdsourcing nor research with human subjects. 

   - Including this information in the supplemental material is fine, but if the main contribution of the paper involves human subjects, then as much detail as possible should be included in the main paper. 

   - According to the NeurIPS Code of Ethics, workers involved in data collection, curation, or other labor should be paid at least the minimum wage in the country of the data collector. 

15. **Institutional review board (IRB) approvals or equivalent for research with human subjects** 

63 

Question: Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained? 

Answer: [N/A] 

Justification: Our human evaluation consists only of blinded rating of short tabletop manipulation video clips with no personally identifiable or sensitive content; under the relevant institutional guidelines such minimal-risk evaluation does not require formal IRB review. The task, expected effort, and voluntary nature of participation were disclosed to all raters before they consented to participate, as described in Appendix J.8. 

Guidelines: 

- The answer [N/A] means that the paper does not involve crowdsourcing nor research with human subjects. 

- Depending on the country in which research is conducted, IRB approval (or equivalent) may be required for any human subjects research. If you obtained IRB approval, you should clearly state this in the paper. 

- We recognize that the procedures for this may vary significantly between institutions and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the guidelines for their institution. 

- For initial submissions, do not include any information that would break anonymity (if applicable), such as the institution conducting the review. 

### 16. **Declaration of LLM usage** 

Question: Does the paper describe the usage of LLMs if it is an important, original, or non-standard component of the core methods in this research? Note that if the LLM is used only for writing, editing, or formatting purposes and does _not_ impact the core methodology, scientific rigor, or originality of the research, declaration is not required. 

Answer: [Yes] 

Justification: A multimodal LLM (Qwen3-VL-8B-Thinking) is used as the backbone of the ROBOALIGN-JUDGE teacher model after LoRA fine-tuning on ROBOTWORLDBENCH (§3.2, Appendix J). Its role, training data, and how its scores are distilled into the student reward model used for RL post-training are described in detail. Any LLM use for writing or editing is consistent with NeurIPS policy and is not part of the core methodology. Guidelines: 

- The answer [N/A] means that the core method development in this research does not involve LLMs as any important, original, or non-standard components. 

- Please refer to our LLM policy in the NeurIPS handbook for what should or should not be described. 

64 

