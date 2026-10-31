---
title: "MotionVLA: Vision-Language-Action Model for Humanoid Motion"
date: "2026-06-13"
authors: "Nonghai Zhang; Siyu Zhai; Yanjun Li; Zeyu Zhang; Zhihan Yin; Yandong Guo"
url: https://arxiv.org/abs/2606.15142
pdf: https://arxiv.org/pdf/2606.15142
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.15142)** / [論文ページ](https://arxiv.org/abs/2606.15142)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **MotionVLA: Vision-Language-Action Model for Humanoid Motion** 

**Nonghai Zhang**<sup>1</sup><sup>_∗_</sup> **Siyu Zhai**<sup>1</sup><sup>_∗_</sup> **Yanjun Li**<sup>1</sup><sup>_∗_</sup> **Zeyu Zhang**<sup>1</sup><sup>_∗†_</sup> **Zhihan Yin**<sup>1</sup> **Yandong Guo**<sup>2</sup> **Boxin Shi**<sup>1</sup> **Hao Tang**<sup>1</sup><sup>_‡_</sup> 

1 School of Computer Science, Peking University 2 AI2 Robotics 

> _∗_ Equal contribution. _†_ Project lead. _‡_ Corresponding author: bjdxtanghao@gmail.com. 

## **Abstract** 

Generating realistic humanoid motion from scene images and text involves both low-frequency pose semantics and high-frequency physical dynamics. However, many existing methods tokenize motion with a single shared codebook, forcing heterogeneous motion signals into the same quantization space. Our frequencydomain analysis of human motion data reveals a clear mismatch between singlecodebook quantization and motion statistics: five DCT coefficients capture 93% of joint-position energy but only 37% of joint-velocity energy, which can bias quantization toward pose statistics and under-represent high-frequency velocity components. A second challenge lies in adapting a standard autoregressive model to effectively model high-frequency physical signals in motion sequences. Therefore, we propose **DSFT** , a dual-stream frequency tokenizer that separates motion into Base and physical streams and compresses them independently with DCT truncation and BPE. Furthermore, we present **MotionVLA** , a Qwen3.5based model that arranges Base and physical tokens in a unified sequence, where Phys tokens are predicted after Base tokens. Experiments on HumanML3D and MBench show that, despite using a lightweight 2B backbone, MotionVLA reduces the Diversity gap to real data by over 50% on HumanML3D and improves Motion-Condition Consistency by 3.8% on MBench, supporting frequency-aware dual-stream decoupling as an effective formulation for autoregressive motion generation. Code: `https://github.com/AIGeeksGroup/MotionVLA` . Website: `https://aigeeksgroup.github.io/MotionVLA` . 

## **1 Introduction** 

Fine-grained humanoid motion generation is a core capability for embodied intelligence, character animation, and scene-aware action synthesis. In recent years, progress in this area has largely followed an autoregressive paradigm, in which motion is discretized into token sequences and generated step by step with Transformer-based models [35, 10, 7, 32, 27, 15, 31]. At the same time, recent advances in vision-language-action (VLA) modeling [11, 2] highlight the value of grounding action generation in scene observations and language instructions, thereby motivating scene-aware vision-language-to-motion generation [13]. 

However, although recent studies have shown that applying DCT before quantization can bring clear advantages to long-horizon autoregressive generation [22, 34, 6], these tokenizers still encode motion within a unified tokenization space, implicitly treating heterogeneous motion components as if they followed similar statistics. Our analysis shows that this assumption does not hold well for human motion: joint positions are strongly low-frequency, with the first five DCT coefficients covering 93% of their energy, whereas joint velocities are markedly high-frequency, with the same five coefficients covering only 37%. Consequently, such a shared tokenization mechanism is naturally 

Preprint. 


Figure 1: Given a text description and a scene video as input, MotionVLA generates motions that closely track the ground truth (GT) across the full sequence (frames at 30%, 60%, and 90% shown). ViMoGen [13], which relies on a single-stream tokenizer, exhibits temporal drift and joint instability that accumulate over time (highlighted in white circles). 

biased toward low-frequency pose structure, while high-frequency physical signals are more easily under-represented. 

At the same time, this representation issue directly creates a second challenge for autoregressive generation. Because a standard autoregressive model predicts motion tokens from a unified codebook, it is naturally encouraged to model the dominant low-frequency pose structure first, while the weaker high-frequency physical signals are less reliably preserved. As generation proceeds over time, this imbalance makes it difficult for the model to faithfully maintain fine-grained physical dynamics, causing errors in contact and motion stability to accumulate. In practice, this often manifests as artifacts such as temporal drift, foot sliding, and contact distortion [4], especially in long-horizon generation [4, 25]. 

However, all existing tokenization methods, including frequency-domain ones, share an unresolved structural limitation: each frame of motion is represented by a single discrete token, forcing signals with fundamentally different frequency profiles into a single codebook. We quantify this imbalance directly on HumanML3D [8]. Joint positions are dominated by low frequencies: five DCT coefficients reconstruct 93% of position energy. Joint velocities, as first derivatives of positions, obey the differentiation theorem, which scales each DCT coefficient by its frequency index and inherently amplifies high-frequency components. The same five coefficients capture only 37% of velocity energy, a gap exceeding fifty percentage points. When BPE is applied to a single concatenated feature, low-frequency position statistics dominate the vocabulary, causing the codebook to effectively discard the high-frequency velocity signal as noise. The practical consequence is visible in Figure 1: motions generated with a single-stream tokenizer accumulate drift and joint instability over time, whereas our method tracks the ground truth throughout the sequence. Prior work has documented these artifacts, including foot sliding and contact distortion [4], and proposed post-hoc corrections at the decoding stage [4, 25], but no prior method removes the structural cause. 

To address these challenges, we propose MotionVLA, a vision-language-to-motion framework built on a dual-stream representation of human motion. Its core component, DSFT, separates motion into a Base stream that captures joint-position semantics and a physical stream that captures joint-velocity dynamics, and tokenizes them independently in the frequency domain. Building on this representation, MotionVLA arranges the two streams in a unified autoregressive sequence, where Phys tokens are generated after Base tokens so that physical-signal prediction can leverage the preceding pose context through causal attention. As show in Figure 1 our method explicitly decouples low-frequency semantic structure from high-frequency physical dynamics while preserving a simple autoregressive formulation. Our contributions are threefold. 

2 


Figure 2: Overview of MotionVLA. (a) DSFT performs dual-stream frequency tokenization by decomposing motion into Base and Phys components and converting them into discrete tokens. (b) During training, MotionVLA learns to autoregressively predict the unified motion token sequence under text and scene-image conditioning, supervised by DSFT tokens derived from ground-truth motion. (c) At inference time, the model generates Base and Phys tokens conditioned on multimodal inputs, which are then decoded and recombined to reconstruct the final motion sequence. 

- we propose **DSFT** , a dual-stream tokenizer that separates motion into Base and Phys streams and compresses them independently in the frequency domain, addressing the mismatch between unified tokenization and heterogeneous motion statistics. 

- We present **MotionVLA** , a vision-language-to-motion framework that models human motion generation as a unified autoregressive process over decoupled semantic and physical token streams. 

- Experiments on HumanML3D and MBench show that our method reduces the Diversity gap to real data by over 50% on HumanML3D, while improving Motion-Condition Consistency from 0.53 to 0.55 and reducing Foot Sliding from 0.0051 to 0.0049 on MBench. 

## **2 The Proposed Method** 

### **2.1 Overview** 

As illustrated in Figure 2, MotionVLA comprises two key components: DSFT, a dual-stream frequency tokenizer that converts motion sequences into discrete Base and Phys token streams, and a Qwen3.5-based autoregressive backbone that generates these tokens conditioned on scene images and text instructions. Given a scene image **I** and a text description **t** , the model encodes the multimodal context and autoregressively predicts a unified motion token sequence [ _M_ BOS _, b_ 1 _, . . . , bN , M_ SEP _, p_ 1 _, . . . , pM , M_ EOS], where Base tokens _bi_ capture low-frequency pose semantics and Phys tokens _pj_ encode high-frequency physical dynamics. After generation, the two streams are independently decoded through BPE inversion and inverse DCT, and then recombined to reconstruct the full motion sequence. This design preserves a unified autoregressive formulation while explicitly disentangling semantic structure from physical dynamics. 

### **2.2 DSFT: Dual-Stream Frequency-Domain Tokenizer** 

DSFT is motivated by a simple observation: human motion is not spectrally homogeneous. Joint positions and rotations evolve relatively smoothly over time and are therefore dominated by lowfrequency components, whereas joint velocities exhibit much stronger high-frequency behavior. This distinction follows naturally from the differentiation theorem, since temporal differentiation amplifies 

3 


Figure 3: Frequency-domain clustering of motion dimensions. (a) Per-dimension low-frequency ratio on HumanML3D. (b) Corresponding histogram on HumanML3D. (c/d) Corresponding plots on ViMoGen. Both datasets exhibit a consistent bimodal separation between low-frequency Base dimensions and high-frequency Phys dimensions. 

higher-frequency coefficients. To verify this property directly from data, we analyze the DCT energy distribution of each motion dimension on both HumanML3D (263 dimensions) and ViMoGen (276 dimensions), and characterize each dimension by its low-frequency ratio, defined as the fraction of energy covered by the first five DCT coefficients. As shown in Figure 3, the resulting distributions are strongly bimodal on both datasets, revealing a consistent separation between low-frequency semantic dimensions and high-frequency physical dimensions. 

Based on this observation, we partition motion into two streams according to physical semantics. The Base stream contains position- and rotation-related dimensions that primarily encode pose semantics, whereas the Phys stream contains velocity-related dimensions that primarily encode physical dynamics. Concretely, this yields ( _Db, Dp_ ) = (190 _,_ 73) for HumanML3D and (201 _,_ 75) for ViMoGen (see Appendix D for the exact per-field index mapping). We therefore represent a motion sequence **M** _∈_ R<sup>_T ×D_</sup> as 


This distinction is further quantified in Figure 4, which compares the cumulative DCT energy retained by the Base and Phys streams as the number of preserved coefficients increases. As shown in the figure, the Base stream is highly compressible: retaining only _K_ = 5 coefficients already covers about 86% to 93% of its energy across datasets. In contrast, the Phys stream is substantially more broadband, with the same _K_ = 5 covering only about 37% of its energy. Therefore, compressing both streams under a shared frequency budget would inevitably favor the low-frequency Base stream while discarding a large portion of high-frequency physical information. This also explains why single-stream tokenization tends to preserve pose structure more easily than physical dynamics, leading to systematic information loss in the latter. 

Accordingly, we retain different numbers of DCT coefficients for the two streams, using a small truncation length for the Base stream and a larger one for the Phys stream. Specifically, we set _Kb_ = 5 and _Kp_ = 25, and apply DCT independently to obtain 


After truncation, each stream is flattened and encoded by an independently trained BPE tokenizer, yielding a Base token sequence **b** and a Phys token sequence **p** . During decoding, we first recover the truncated coefficients by inverse BPE mapping, and then reconstruct the two time-domain streams by inverse DCT. Finally, the reconstructed Base and Phys streams are concatenated along the feature dimension to recover the complete motion sequence. 

In this way, DSFT converts continuous motion into two complementary token streams, which provide the foundation for the unified autoregressive generation framework described next. 

### **2.3 MotionVLA: Unified Sequence Formulation, Objective, and Inference** 

Given a scene image **I** and a text description **t** , MotionVLA formulates motion generation as a unified autoregressive sequence modeling problem. Specifically, each motion sample is represented as 


where _bi_ denotes Base tokens and _pj_ denotes Phys tokens. In this way, MotionVLA preserves a simple autoregressive formulation while imposing a structured semantic-to-physical generation order. 

4 


Figure 4: Energy coverage of the Base and Phys streams under different DCT truncation lengths. (a,b) Results on HumanML3D. (c,d) Corresponding results on ViMoGen. The Base stream is highly compressible with small _K_ , whereas the Phys stream requires substantially larger _K_ to preserve its energy. 

This ordering is important because physical dynamics are typically conditioned on the underlying pose structure. By placing Phys tokens after all Base tokens, MotionVLA allows each Phys prediction to attend to the complete preceding Base context through causal attention. As a result, the model can generate physical dynamics with access to the full semantic pose information, rather than predicting both streams in an entangled manner. This design enables a hierarchical semantic-to-physical generation process within a standard autoregressive transformer. 

To instantiate this sequence within the backbone token space, we extend the original vocabulary with motion tokens and three structural markers, yielding 


where _V_ LM denotes the original backbone vocabulary, and _V_ motion denotes the motion vocabulary induced by DSFT. 

During training, the scene image and text description serve as conditioning context, while the model is optimized to predict the motion portion of the sequence with teacher forcing. Let **y** denote the training targets, where non-motion positions are masked out. We optimize MotionVLA with a masked next-token prediction objective: 


where **z** denotes the output logits, and **m** is a logit mask that restricts prediction to valid motion tokens and structural markers. This objective prevents probability mass from being assigned to irrelevant vocabulary entries and focuses learning on the motion token space. 

During inference, we further impose a phase-aware generation constraint to preserve the intended Base-to-Phys order. Before generating _M_ SEP, only Base tokens and _M_ SEP are allowed; after _M_ SEP is produced, only Phys tokens and _M_ EOS are allowed. This phase-aware mask ensures that semantic structure is generated before physical dynamics, while preventing the model from mixing the two streams during decoding. The complete inference procedure is summarized in Algorithm 1. 

## **3 Experiments** 

### **3.1 Datasets and Evaluation Metrics** 

We conduct experiments on two settings. In the first setting, we train on **ViMoGen-228K** [13], a large-scale multimodal motion dataset, and evaluate on **MBench** [13], the associated fine-grained physical quality benchmark. In the second setting, we train and evaluate on **HumanML3D** [8] under the standard text-to-motion protocol. Table 1 summarizes dataset statistics; detailed metric definitions and evaluation protocols are provided in Appendix B. 

### **3.2 Baselines** 

We compare MotionVLA with representative baselines spanning three paradigms: discrete autoregressive generation, diffusion-based methods, and approaches with improved motion tokenization, as summarized in Table 8. On ViMoGen-228K and MBench, prior methods are evaluated under their original text-driven setting, whereas MotionVLA additionally conditions on the scene image. On HumanML3D, all methods follow the same standard text-to-motion protocol for a fair comparison. 

5 

**Algorithm 1** Phase-Aware Autoregressive Generation in MotionVLA 

**Require:** Scene image **I** , text instruction **t** , trained MotionVLA, phase-aware logit mask **m Ensure:** Reconstructed motion sequence **M** _∈_ R<sup>_T ×D_</sup> 1: Encode **I** , **t** through Qwen3.5 _→_ context representations 2: Initialize token buffer **s** _←_ [ _M_ BOS], _phase ←_ BASE 3: **while** last token _̸_ = _M_ EOS **do** 4: **if** _phase_ = BASE **then** 5: Apply mask: allow _{bi} ∪{M_ SEP _}_ only 6: **else** 7: Apply mask: allow _{pj} ∪{M_ EOS _}_ only 8: **end if** 9: Sample next token _τ ∼_ softmax(logits + **m** ) 10: Append _τ_ to **s** 11: **if** _τ_ = _M_ SEP **then** 12: _phase ←_ PHYS 13: **end if** 14: **end while** 15: Extract Base tokens **b** and Phys tokens **p** from **s** 16: **M** base _←_ IDCT�BPE<sup>_−_1</sup> ( **b** )� 17: **M** phys _←_ IDCT�BPE<sup>_−_1</sup> ( **p** )� 18: **return M** _←_ [ **M** base _∥_ **M** phys] _▷_ concatenate along spatial dimension 

Table 1: **Dataset statistics.** ViMoGen-228K is the training dataset; MBench is its associated evaluation benchmark (not a dataset subset). _†_ : optical motion capture with marker-based GT. _‡_ : inthe-wild video with pseudo-GT from SMPL estimation. #: generative synthesis with physics-based renderer. 

|**Dataset / Benchmark**|**#Clip**|**#Hour**|**Scene**|**Motion**|**Video**|**Role**|
|---|---|---|---|---|---|---|
|HumanML3D [8]|14,616|28.6|Indoor|GT|–|Train / Eval|
|ViMoGen-228K [13]|228,236|369.4|Mixed|Mixed|–|Train|
|_•_Optical MoCap<sup>_†_</sup>|171,542|292.7|Indoor|GT|–|Train|
|_•_In-the-Wild Video<sup>_‡_</sup>|41,971|61.4|In-the-Wild|Pseudo GT|✓|Train|
|_•_Synthetic Video<sup>#</sup>|14,723|16.6|In-the-Wild|Pseudo GT|✓|Not used|
|MBench [13]|450|–|In-the-Wild|GT|✓|Eval only|


### **3.3 Experimental Setup** 

Prior to model training, we train the DSFT tokenizer independently on each benchmark’s training split, ensuring that the discrete motion representation is adapted to the motion statistics of each dataset. Full training details and feature partition specifications are provided in Appendix C and D. 

We then conduct four groups of experiments to evaluate MotionVLA comprehensively: a main benchmark evaluation on MBench for scene-conditioned motion generation, a text-to-motion generalization evaluation on HumanML3D, a DSFT tokenizer reconstruction analysis to assess representation quality, and an ablation study to examine the impact of key design choices. Detailed hyperparameter settings are provided in Appendix C. 

### **3.4 Main Results on MBench** 

Table 2 reports the quantitative comparison on MBench, which evaluates models trained on ViMoGen228K across eight fine-grained quality dimensions. Despite using a lightweight 2B backbone, MotionVLA achieves the best results on Motion-Condition Consistency and Foot Sliding, while ranking second on Motion Generalizability and Jitter Degree. These gains indicate that the proposed framework is particularly effective at improving multimodal condition alignment and suppressing local temporal artifacts. 

At inference time, the target motion length T is provided externally, and MotionVLA generates DSFT tokens conditioned on this target horizon. This pattern is consistent with our design. Scene-aware 

6 

Table 2: **MotionVLA [13] evaluation on MBench.** _↑_ : higher is better; _↓_ : lower is better. _†_ : uses additional visual (scene) input. Best in **bold** <u>, second best underlined.</u> 

|**Method**|**Motion-Cond.**<br>**Consistency** _↑_|**Motion**<br>**Generaliz.**_↑_|<br>**Jitter**<br>**Degree**_↓_|**Dynamic**<br>**Degree**|_↑_<br>**Foot**<br>**Floating**_↓_|**Foot**<br>**Sliding**_↓_|**Body**<br>**Penetration**_↓_|<br>**Pose**<br>**Quality**_↓_|
|---|---|---|---|---|---|---|---|---|
|MDM [29] (ICLR’23)|0.42|0.51|0.0136|0.0376|0.156|0.0136|1.68|2.67|
|T2M-GPT [35] (CVPR’23)|0.39|0.38|0.0156|0.0349|0.209|0.0156|1.33|2.43|
|FineMoGen [37] (NeurIPS’24)|0.37|0.42|0.0118|0.0386|0.281|0.0091|1.18|2.28|
|MotionLCM [5] (ECCV’24)|0.48|0.55|0.0218|**0.0439**|0.193|0.0202|1.73|2.40|
|MoMask [7] (CVPR’24)|0.38|0.44|0.0147|0.0396|0.178|0.0147|1.48|2.67|
|MotionDiffuse [36] (TPAMI’24)|0.44|0.42|0.0111|0.0289|**0.126**|0.0063|1.35|2.21|
|MotionCraft [1] (CVPR’25)|0.42|0.45|0.0132|0.0420|0.402|0.0090|**1.15**|2.12|
|ViMoGen [13] (ICLR’26)|0.53|**0.68**|**0.0108**|0.0251|0.204|0.0064|1.78|2.38|
|ViMoGen-light [13] (ICLR’26)|0.47|0.55|0.0129|0.0294|0.155|0.0051|1.43|**2.10**|
|**MotionVLA (Ours)**<sup>_†_</sup>|**0.55**|0.66|0.0110|0.0419|0.149|**0.0049**|1.34|2.14|


Table 3: **Text-to-motion results on HumanML3D.** _↑_ : higher is better; _↓_ : lower is better; _→_ : closer to real is better. For Diversity, best and second best are determined by the distance to the Real score. _‡_ : GenM3 uses a retrained evaluator on 30 FPS data; GenM3<sup>_∗_</sup> uses only HumanML3D text pairs. _§_ : DisCoRD is applied on top of MoMask; Diversity is not reported in the original paper. 

|**Method**|**R-P Top-1**_↑_|**R-P Top-2**_↑_|**R-P Top-3**_↑_|**FID**_↓_|**MM-Dist**_↓_|**Diversity**_→_|**MModality**_↑_|
|---|---|---|---|---|---|---|---|
|Real|0_._511<sup>_±._003</sup>|0_._703<sup>_±._003</sup>|0_._797<sup>_±._002</sup>|0_._002<sup>_±._000</sup>|2_._974<sup>_±._008</sup>|9_._503<sup>_±._065</sup>|–|
|_Motion generation only_<br>TEMOS [23] (ECCV’22)|0_._424<sup>_±._002</sup>|0_._612<sup>_±._002</sup>|0_._722<sup>_±._002</sup>|3_._734<sup>_±._028</sup>|3_._703<sup>_±._008</sup>|8_._973<sup>_±._071</sup>|0_._368<sup>_±._018</sup>|
|TM2T [9] (ECCV’22)|0_._424<sup>_±._003</sup>|0_._618<sup>_±._003</sup>|0_._729<sup>_±._002</sup>|1_._501<sup>_±._017</sup>|3_._467<sup>_±._011</sup>|8_._589<sup>_±._076</sup>|2_._424<sup>_±._093</sup>|
|Guo et al. [8] (CVPR’22)|0_._455<sup>_±._003</sup>|0_._636<sup>_±._003</sup>|0_._736<sup>_±._002</sup>|1_._087<sup>_±._021</sup>|3_._347<sup>_±._008</sup>|9_._175<sup>_±._083</sup>|2_._219<sup>_±._074</sup>|
|MDM [29] (ICLR’23)|–|–|0_._611<sup>_±._007</sup>|0_._544<sup>_±._044</sup>|5_._566<sup>_±._027</sup>|–|2_._799<sup>_±._072</sup>|
|MotionDiffuse [36] (TPAMI’24)|0_._491<sup>_±._001</sup>|0_._681<sup>_±._001</sup>|0_._782<sup>_±._001</sup>|0_._630<sup>_±._001</sup>|3_._113<sup>_±._001</sup>|9_._410<sup>_±._049</sup>|1_._553<sup>_±._042</sup>|
|T2M-GPT [35] (CVPR’23)|0_._492<sup>_±._003</sup><br>|0_._679<sup>_±._002</sup><br>|0_._775<sup>_±._002</sup><br>|0_._141<sup>_±._004</sup><br>|3_._121<sup>_±._009</sup><br>|9_._722<sup>_±._082</sup><br>|1_._831<sup>_±._048</sup><br>|
|FineMoGen [37] (NeurIPS’24)|0_._504<sup>_±._002</sup>|0_._690<sup>_±._002</sup>|0_._784<sup>_±._002</sup>|0_._151<sup>_±._008</sup>|2_._998<sup>_±._008</sup>|9_._263<sup>_±._094</sup>|2_._696<sup>_±._079</sup>|
|MoMask [7] (CVPR’24)|0_._521<sup>_±._002</sup>|0_._713<sup>_±._002</sup>|0_._807<sup>_±._002</sup>|0_._045<sup>_±._002</sup>|2_._958<sup>_±._008</sup>|–|1_._241<sup>_±._040</sup>|
|MotionGPT [38] (AAAI’24)|–|–|–|0_._567|3_._775|9_._006|–|
|DisCoRD [4] (ICCV’25)<sup>_§_</sup>|0_._524<sup>_±._003</sup>|0_._715<sup>_±._003</sup>|0_._809<sup>_±._002</sup>|0_._032<sup>_±._002</sup>|2_._938<sup>_±._010</sup>|–|1_._288<sup>_±._043</sup>|
|GenM3<sup>_∗_</sup>[27] (ICCV’25)<sup>_‡_</sup>|0_._510<sup>_±._002</sup>|0_._702<sup>_±._002</sup>|0_._802<sup>_±._002</sup>|0_._053<sup>_±._002</sup>|2_._860<sup>_±._009</sup>|9_._629<sup>_±._077</sup>|–|
|GenM3 [27] (ICCV’25)<sup>_‡_</sup>|0_._511<sup>_±._003</sup>|0_._705<sup>_±._002</sup>|0_._804<sup>_±._002</sup>|0_._046<sup>_±._002</sup>|2_._852<sup>_±._009</sup>|9_._675<sup>_±._087</sup>|–|
|MG-MotionLLM [32] (CVPR’25)|0_._516<sup>_±._002</sup>|0_._706<sup>_±._002</sup>|0_._802<sup>_±._003</sup>|0_._303<sup>_±._010</sup>|2_._952<sup>_±._009</sup>|9_._960<sup>_±._073</sup>|2_._125<sup>_±._159</sup>|
|**MotionVLA (Ours)**|0_._507<sup>_±._002</sup>|0_._699<sup>_±._002</sup>|0_._798<sup>_±._002</sup>|0_._071<sup>_±._003</sup>|2_._906<sup>_±._009</sup>|9_._548<sup>_±._081</sup>|2_._821<sup>_±._091</sup>|


conditioning mainly improves semantic alignment, while the DSFT dual-stream tokenizer reduces local temporal artifacts such as jitter and foot sliding. Meanwhile, MotionVLA does not dominate all physical metrics, indicating that low-level geometric quality remains challenging under the smaller model scale. Overall, MotionVLA provides a favorable trade-off between multimodal controllability and physical motion quality on MBench. 

### **3.5 Results on HumanML3D** 

Table 3 reports text-to-motion generation results on HumanML3D under the standard benchmark setting. Although MotionVLA uses a lightweight 2B backbone and is designed for multimodal motion generation, it remains competitive on this purely text-driven benchmark, achieving the Diversity score closest to the real data distribution and the highest MModality among generated methods. Its R-Precision, FID, and MM-Dist scores also remain competitive with strong recent baselines, indicating that the proposed framework transfers beyond the multimodal training setting. 

This pattern is consistent with our design. Since HumanML3D removes visual conditioning, the gains mainly reflect the motion representation itself rather than scene input. By separating low-frequency motion semantics from high-frequency physical dynamics, DSFT preserves richer motion variation while maintaining competitive sample fidelity and text-motion alignment. Overall, these results show that MotionVLA generalizes effectively beyond ViMoGen and provides a strong diversity-quality trade-off even at a relatively small 2B model scale. 

### **3.6 DSFT Tokenizer Analysis** 

We analyze DSFT on HumanML3D through controlled comparisons within the DCT+BPE family. Compared with a single-stream DCT+BPE baseline, DSFT produces a more compact token sequence and a substantially lower reconstruction Fréchet inception distance (rFID), despite having higher 

7 

Table 4: **DSFT tokenizer reconstruction analysis on HumanML3D.** Smaller Tok./Frame indicates a more compact tokenization; lower rRMSE, MPJPE, and rFID are better. 

|**Method**|**Tok./Frame**|**rRMSE**|**MPJPE**|**rFID**|
|---|---|---|---|---|
|Single-Stream DCT+BPE|15.21|0.0164|0.0054|0.9461|
|DSFT (_Kp_=25)|11.24|0.0226|0.0093|0.1868|
|DSFT (_Kp_=10)|8.80|0.0240|0.0108|1.3404|
|DSFT (_Kp_=15)|9.74|0.0233|0.0102|0.5966|
|DSFT (_Kp_=20)|10.55|0.0228|0.0097|0.2895|
|DSFT (_Kp_=25)|11.24|0.0226|0.0093|0.1868|
|DSFT (_Kp_=30)|11.81|0.0224|0.0091|0.1380|


Table 5: **Backbone scale ablation on MBench.** _†_ : default configuration used in main experiments. _<u>↑</u>_ / _<u>↓</u>_ : higher/lower is better. 

|**Backbone**|**Params**|**Motion-Cond.**<br>**Consistency** _↑_|**Motion**<br>**Generaliz.**_↑_|**Jitter**<br>**Degree**_↓_|**Dynamic**<br>**Degree** _↑_|**Foot**<br>**Floating**_↓_|**Foot**<br>**Sliding**_↓_|**Body**<br>**Penetration**_↓_|**Pose**<br>**Quality**_↓_|
|---|---|---|---|---|---|---|---|---|---|
|Qwen3.5-0.8B|0.8B|0.51|0.60|0.0122|0.0364|0.162|0.0058|1.46|2.26|
|**Qwen3.5-2B**<sup>_†_</sup>|**2B**|0.55|0.66|0.0110|0.0419|0.149|0.0049|1.34|2.14|
|Qwen3.5-4B|4B|0.55|0.66|0.0109|0.0393|0.146|0.0049|1.31|2.12|
|Qwen3.5-9B|9B|0.56|0.68|0.0107|0.0396|0.144|0.0047|1.30|2.09|


reconstruction root mean square error (rRMSE) and MPJPE. This suggests that lower pointwise reconstruction error does not necessarily imply better tokenizer quality. 

As the Phys-stream truncation length _Kp_ increases, rRMSE, MPJPE, and rFID all improve consistently. We use _Kp_ =25 as the default setting because it already offers a strong compactness-fidelity trade-off while matching the main tokenizer configuration. 

Table 4 also shows that increasing the Phys-stream truncation length _Kp_ consistently improves reconstruction quality. As _Kp_ increases from 10 to 30, both rRMSE and MPJPE decrease, while rFID drops from 1.340 to 0.138. We therefore use _Kp_ =25 as the default setting, since it already provides a strong compactness-fidelity trade-off while matching the main tokenizer configuration. 

### **3.7 Ablation Studies** 

We conduct two ablation studies on MBench to examine the effect of backbone scale and the Physstream truncation length _Kp_ . Since HumanML3D does not provide visual observations, we focus the ablation analysis on the scene-conditioned ViMoGen-228K–MBench setting. 

**Backbone Scale.** Table 5 shows that scaling up the Qwen3.5 backbone yields consistent but diminishing gains on MBench. The largest improvement comes from 0.8B to 2B, while the gains from 2B to 4B and 9B are relatively small. For some metrics, the 2B and 4B models appear unchanged after rounding, since only two decimal places are reported in those columns. One possible explanation is that, under the current data scale and training recipe, the available supervision is not sufficient to fully exploit substantially larger backbones. Moreover, because MotionVLA predicts a fixed DSFT tokenization rather than continuous motion directly, the effective information carried by the token representation may also limit how much additional capacity can be translated into measurable gains. As a result, a 2B model already captures most of the achievable improvement in the current setting, making it a favorable default choice in terms of both performance and efficiency. 

**DSFT Truncation Parameter** _Kp_ **.** Table 6 studies the effect of the Phys-stream truncation length _Kp_ while fixing _Kb_ =5 under the default 2B backbone. As _Kp_ increases, Phys-stream energy coverage improves consistently, indicating that a larger frequency budget preserves more high-frequency physical dynamics. From _Kp_ =10 to _Kp_ =25, this added physical capacity is accompanied by clear improvements on most MBench metrics, showing that richer physical signals benefit overall motion quality. However, a larger _Kp_ also increases the motion sequence length, and the gains do not continue monotonically at _Kp_ =30, where several metrics slightly degrade. We therefore use _Kp_ =25 as the default setting, as it provides the best overall balance between physical detail preservation and sequence efficiency under the current 2B model scale. 

8 

Table 6: **DSFT** _Kp_ **ablation on MBench.** _Kb_ =5 fixed. Tok./Sample: average motion token count. _<u>↑</u>_ / _<u>↓</u>_ : higher/lower is better. 

|_Kp_|**Phys**<br>**Coverage**_↑_|**Tok./Sample**|**Motion-Cond.**<br>**Consistency** _↑_|**Motion**<br>**Generaliz.**_↑_|<br>**Jitter**<br>**Degree**_↓_|**Dynamic**<br>**Degree** _↑_|**Foot**<br>**Floating**_↓_|**Foot**<br>**Sliding**_↓_|**Body**<br>**Penetration**_↓_|**Pose**<br>**Quality**_↓_|
|---|---|---|---|---|---|---|---|---|---|---|
|10|_∼_50%|438|0.49|0.58|0.0131|0.0338|0.171|0.0062|1.48|2.28|
|15|_∼_63%|472|0.52|0.61|0.0121|0.0364|0.160|0.0054|1.41|2.21|
|20|_∼_73%|507|0.54|0.63|0.0116|0.0375|0.154|0.0051|1.37|2.17|
|**25**|_∼_80%|541|0.55|0.66|0.0110|0.0419|0.149|0.0049|1.34|2.14|
|30|_∼_85%|569|0.53|0.64|0.0113|0.0379|0.152|0.0052|1.38|2.16|


Table 7: **Human preference study** (%) on 100 prompts _×_ 5 experts. Ours: MotionVLA preferred; Tie: comparable; Base: ViMoGen preferred. 

||**Expert 1**|**Expert 2**|**Expert 3**|**Expert 4**|**Expert 5**|**Avg.**|
|---|---|---|---|---|---|---|
|**Ours (MotionVLA preferred)**|72|58|69|55|66|**64.0**|
|**Tie (Same taste)**|17|26|19|28|20|22.0|
|**Base (Vimogen preferred)**|11|16|12|17|14|14.0|


### **3.8 Simulation, Deployment and Human Preference Study** 

To complement automatic metrics, we evaluate MotionVLA in MuJoCo simulation, deploy it on a Unitree G1 EDU humanoid under the text-to-motion setting, and conduct a blinded human preference study against ViMoGen [13]. Given a text prompt, MotionVLA generates motion tokens that DSFT decodes into real-time joint-angle trajectories. Five domain experts assess 100 anonymized textconditioned motion pairs, producing 500 pairwise comparisons. Detailed simulation, deployment, and evaluation protocols are provided in Appendix F and E. 

As summarized in Table 7, MotionVLA is preferred in 64.0% of comparisons, compared with 14.0% for ViMoGen and 22.0% ties, indicating a clear perceptual advantage in overall motion quality. 

## **4 Discussions and Conclusions** 

In this work, we address humanoid motion generation through coordinated innovations in tokenizer design, autoregressive modeling, and evaluation. (1) We introduce DSFT, a dual-stream frequencydomain tokenizer that decomposes motion into Base and Phys streams, motivated by the observation that pose-related and dynamic signals exhibit different spectral characteristics and therefore should not be forced into a single shared tokenization space. By assigning separate frequency budgets to the two streams, DSFT better preserves both motion semantics and high-frequency physical dynamics. (2) Built on top of this tokenizer, MotionVLA adapts a standard vision-language autoregressive backbone to unified motion generation, showing that multimodal controllability and physical motion quality can be improved within a simple sequence modeling framework. (3) Experiments on HumanML3D and ViMoGen–MBench show strong performance on both automatic metrics and human preference evaluation, supporting the effectiveness of frequency-aware dual-stream tokenization for both multimodal generation and transfer to standard text-to-motion settings. More broadly, these results suggest that effective motion tokenization depends not only on compression or pointwise reconstruction quality, but also on how motion signals are organized before discretization. A detailed discussion of related work is provided in Appendix A. 

**Limitations and Future Work.** Our current study focuses on a lightweight 2B backbone and a limited set of benchmarks, and therefore does not yet support broader conclusions about scaling behavior or cross-dataset generalization. In addition, the current framework uses a fixed stream partition, fixed truncation lengths, and a predefined Base-to-Phys generation order, which may not be optimal for all motion types or sequence lengths. Future work will extend the evaluation to larger backbones, broader datasets, and more adaptive tokenization and dependency modeling schemes. 

## **References** 

- [1] Yuxuan Bian, Ailing Zeng, Xuan Ju, Xian Liu, Zhaoyang Zhang, Wei Liu, and Qiang Xu. MotionCraft: Crafting whole-body motion with plug-and-play multimodal controls. _AAAI Conference on Artificial Intelligence_ , 2024. 

9 

- [2] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv.org_ , 2024. 

- [3] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, K. Choromanski, Tianli Ding, Danny Driess, Kumar Avinava Dubey, Chelsea Finn, Peter R. Florence, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , 2023. 

- [4] Jungbin Cho, Junwan Kim, Jisoo Kim, Minseo Kim, Mingu Kang, Sungeun Hong, Tae-Hyun Oh, and Youngjae Yu. DisCoRD: Discrete tokens to continuous motion via rectified flow decoding. In _arXiv.org_ , 2024. Highlight. 

- [5] Wenxun Dai, Ling-Hao Chen, Jingbo Wang, Jinpeng Liu, Bo Dai, and Yansong Tang. MotionLCM: Real-time controllable motion generation via latent consistency model. In _European Conference on Computer Vision_ , 2024. 

- [6] Chenyang Gu, Mingyuan Zhang, Haozhe Xie, Zhongang Cai, Lei Yang, and Ziwei Liu. Bridging semantic and kinematic conditions with diffusion-based discrete motion tokenizer. _arXiv preprint arXiv:2603.19227_ , 2026. 

- [7] Chuan Guo, Yuxuan Mu, Muhammad Gohar Javed, Sen Wang, and Li Cheng. MoMask: Generative masked modeling of 3D human motions. In _Computer Vision and Pattern Recognition_ , 2023. 

- [8] Chuan Guo, Shihao Zou, Xinxin Zuo, Sen Wang, Wei Ji, Xingyu Li, and Li Cheng. Generating diverse and natural 3D human motions from texts. In _Computer Vision and Pattern Recognition_ , pages 5142–5151. IEEE, 2022. 

- [9] Chuan Guo, X. Zuo, Sen Wang, and Li Cheng. TM2T: Stochastic and tokenized modeling for the reciprocal generation of 3D human motions and texts. In _European Conference on Computer Vision_ , pages 580–597. Springer Nature Switzerland, 2022. 

- [10] Biao Jiang, Xin Chen, Wen Liu, Jingyi Yu, Gang Yu, and Tao Chen. MotionGPT: Human motion as a foreign language. In _Neural Information Processing Systems_ , pages 20067–20079. Neural Information Processing Systems Foundation, Inc. (NeurIPS), 2023. 

- [11] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, A. Balakrishna, Suraj Nair, Rafael Rafailov, E. Foster, Grace Lam, Pannag R. Sanketi, et al. OpenVLA: An open-source vision-language-action model. _Conference on Robot Learning_ , 2024. 

- [12] Zekun Li, Sizhe An, Chengcheng Tang, Chuan Guo, Ivan Shugurov, Linguang Zhang, Amy Zhao, Srinath Sridhar, Lingling Tao, and Abhay Mittal. LLaMo: Scaling pretrained language models for unified motion understanding and generation with continuous autoregressive tokens. _arXiv.org_ , 2026. 

- [13] Jing Lin, Ruisi Wang, Junzhe Lu, Ziqi Huang, Guorui Song, Ailing Zeng, Xian Liu, Chen Wei, Wanqi Yin, Qingping Sun, et al. The quest for generalizable motion generation: Data, model, and evaluation. In _arXiv.org_ , 2025. arXiv:2510.26794. 

- [14] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. _International Conference on Learning Representations_ , 2022. 

- [15] Mengyuan Liu, Sheng Yan, Yong Wang, Yingjie Li, Gui-Bin Bian, and Hong Liu. MoSa: Motion generation with scalable autoregressive modeling. _arXiv.org_ , 2025. 

- [16] Xingchao Liu, Chengyue Gong, and Qiang Liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. _International Conference on Learning Representations_ , 2022. 

- [17] Stephane Mallat. _A wavelet tour of signal processing_ . Elsevier, 1998. 

10 

- [18] Zichong Meng, Yiming Xie, Xiaogang Peng, Zeyu Han, and Huaizu Jiang. Rethinking diffusion for text-driven human motion generation: Redundant representations and evaluation. In _Computer Vision and Pattern Recognition_ , 2024. 

- [19] Aäron van den Oord, O. Vinyals, and K. Kavukcuoglu. Neural discrete representation learning. In _Neural Information Processing Systems_ , 2017. 

- [20] Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, Alex Bewley, et al. Open x-embodiment: Robotic learning datasets and rt-x models. In _ICRA_ , 2024. 

- [21] Georgios Pavlakos, Vasileios Choutas, Nima Ghorbani, Timo Bolkart, Ahmed A. A. Osman, Dimitrios Tzionas, and Michael J. Black. Expressive body capture: 3D hands, face, and body from a single image. In _Computer Vision and Pattern Recognition_ , pages 10967–10977. IEEE, 2019. 

- [22] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. FAST: Efficient action tokenization for vision-language-action models. _Robotics_ , 2025. 

- [23] Mathis Petrovich, Michael J. Black, and Gül Varol. TEMOS: Generating diverse human motions from textual descriptions. In _European Conference on Computer Vision_ , pages 480– 497. Springer Nature Switzerland, 2022. 

- [24] R. Pfeifer and F. Iida. Embodied artificial intelligence: Trends and challenges. _Embodied Artificial Intelligence_ , 2003. 

- [25] Yijie Qian, Juncheng Wang, Yuxiang Feng, Chao Xu, Wang Lu, Yang Liu, Baigui Sun, Yiqiang Chen, Yong Liu, and Shujun Wang. Think before you move: Latent motion reasoning for text-to-motion generation. _arXiv.org_ , 2025. 

- [26] Junlong Ren, Gangjian Zhang, Honghao Fu, Pengcheng Wu, and Hao Wang. WaMo: Waveletenhanced multi-frequency trajectory analysis for fine-grained text-motion retrieval. _arXiv.org_ , 2025. 

- [27] Junyu Shi, Lijiang Liu, Yong Sun, Zhiyuan Zhang, Jinni Zhou, and Q. Nie. GenM3: Generative pretrained multi-path motion model for text conditional human motion generation. In _arXiv.org_ , pages 13129–13139. IEEE, 2025. 

- [28] O. Team, Dibya Ghosh, H. Walke, Karl Pertsch, Kevin Black, Oier Mees, S. Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. In _Robotics: Science and Systems_ . Robotics: Science and Systems Foundation, 2024. 

- [29] Guy Tevet, Sigal Raab, Brian Gordon, Yonatan Shafir, Daniel Cohen-Or, and Amit Haim Bermano. Human motion diffusion model. In _International Conference on Learning Representations_ , 2022. 

- [30] Emanuel Todorov, Tom Erez, and Yuval Tassa. MuJoCo: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026–5033. IEEE, 2012. 

- [31] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Neural Information Processing Systems_ , 30, 2017. 

- [32] Bizhu Wu, Jinheng Xie, Keming Shen, Zhe Kong, Jianfeng Ren, Ruibin Bai, Rong Qu, and LinLin Shen. MG-MotionLLM: A unified framework for motion comprehension and generation across multiple granularities. In _Computer Vision and Pattern Recognition_ , pages 27849–27858. IEEE, 2025. 

- [33] Lixing Xiao, Shunlin Lu, Huaijin Pi, Ke Fan, Liang Pan, Yue Zhou, Ziyong Feng, Xiaowei Zhou, Sida Peng, and Jingbo Wang. MotionStreamer: Streaming motion generation via diffusionbased autoregressive model in causal latent space. In _arXiv.org_ , pages 10086–10096. IEEE, 2025. 

11 

- [34] Sheng Yan, Yong Wang, Xin Du, Junsong Yuan, and Mengyuan Liu. Language-guided transformer tokenizer for human motion generation. _arXiv.org_ , 2026. 

- [35] Jianrong Zhang, Yangsong Zhang, Xiaodong Cun, Shaoli Huang, Yong Zhang, Hongwei Zhao, Hongtao Lu, and Xi Shen. T2M-GPT: Generating human motion from textual descriptions with discrete representations. In _Computer Vision and Pattern Recognition_ , pages 14730–14740. IEEE, 2023. 

- [36] Mingyuan Zhang, Zhongang Cai, Liang Pan, Fangzhou Hong, Xinying Guo, Lei Yang, and Ziwei Liu. MotionDiffuse: Text-driven human motion generation with diffusion model. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2022. 

- [37] Mingyuan Zhang, Huirong Li, Zhongang Cai, Jiawei Ren, Lei Yang, and Ziwei Liu. FineMoGen: Fine-grained spatio-temporal motion generation and editing. In _Neural Information Processing Systems_ , pages 13981–13992. Neural Information Processing Systems Foundation, Inc. (NeurIPS), 2023. 

- [38] Yaqi Zhang, Di Huang, B. Liu, Shixiang Tang, Yan Lu, Lu Chen, Lei Bai, Q. Chu, Nenghai Yu, and Wanli Ouyang. MotionGPT: Finetuned LLMs are general-purpose motion generators. In _AAAI Conference on Artificial Intelligence_ , 2023. 

- [39] Yifan Zhong, Fengshuo Bai, Shaofei Cai, Xuchuan Huang, Zhan Chen, Xiaowei Zhang, Yuanfang Wang, Shaoyang Guo, Tianrui Guan, Ka Nam Lui, et al. A survey on vision-language-action models: An action tokenization perspective. _arXiv.org_ , 2025. 

- [40] Bingfan Zhu, Biao Jiang, Sunyi Wang, Shixiang Tang, Tao Chen, Linjie Luo, Youyi Zheng, and Xin Chen. MotionGPT3: Human motion as a second modality. _arXiv.org_ , 2025. 

12 

## **A Related Work** 

### **A.1 Human Motion Generation** 

Text-driven human motion generation aims to synthesize realistic 3D human motion sequences from natural language descriptions. Mainstream methods build generation frameworks upon VQ-VAE discretization and autoregressive Transformers. T2M-GPT [35] first combines VQ-VAE with GPT next-token prediction, establishing the representative paradigm in this line of work. MotionGPT [10] treats motion as a foreign language and jointly trains multiple motion tasks under a unified language model. MoMask [7] introduces Residual VQ (RVQ) hierarchical codebooks and Masked Transformers, reducing the FID to 0.045, while MG-MotionLLM [32] builds a multi-granularity motion-language framework with T5 as the backbone, extending semantic granularity from the sequence level to the segment level. GenM3 [27] collects 11 datasets and employs a multi-expert VQVAE along with a multi-path Transformer to handle data heterogeneity, achieving a state-of-the-art FID of 0.035. MoSa [15] proposes RQ-VAE and a scalable autoregressive framework, outperforming the 10-step inference speed of MoMask by 27%. More recently, MotionGPT3 [40] and LLaMo [12] shift towards continuous latent space autoregression to reduce the motion jitter caused by discrete quantization. Another line of work adopts diffusion models as the backbone. MDM [29] establishes the Transformer-based diffusion framework, and MotionDiffuse [36] extends it to support fine-grained control at the body-part level. FineMoGen [37] achieves fine-grained spatio-temporal synthesis using Spatial-Temporal Mixed Attention (SAMI) and sparse MoE, while MotionStreamer [33] combines diffusion with autoregression in a causal latent space for streaming generation. Recent systematic comparisons [18] indicate that VQ-based autoregressive methods still hold an overall advantage on standard metrics such as FID and R-Precision. 

### **A.2 Motion Tokenization and Representation** 

High-quality discrete motion representations form the basis of autoregressive generation methods. VQ-VAE [19] introduces discrete bottlenecks into sequence modeling, enabling efficient compression and generation of continuous data. T2M-GPT [35] adapts this paradigm to the human motion domain, showing that motion can be effectively tokenized for text-driven generation. MoMask [7] enhances hierarchical representation capabilities with Residual Vector Quantization (RVQ) [19], enabling multi-scale semantic abstraction. In the frequency domain, FAST [22] constructs an efficient robot action tokenizer by combining Discrete Cosine Transform (DCT) with Byte-Pair Encoding (BPE), showing that frequency-domain representations capture high-frequency fine-grained control signals more effectively. Following this direction, WaMo [26] applies wavelet multi-scale decomposition [17] to motion trajectory analysis, further validating that multi-frequency decomposition improves finegrained motion-text correspondence. Recent work also explores the integration of semantic guidance into the tokenization process: LG-Tok [34] proposes a language-guided Transformer tokenizer that introduces semantic alignment during the encoding stage, while MoTok [6] uses a diffusion decoder to decouple semantic abstraction from fine-grained reconstruction, maintaining high-fidelity reconstruction quality with single-layer tokens. DisCoRD [4] approaches the problem from the decoding end, mapping discrete tokens back to continuous motion via rectified flow [16] to partially reduce inter-frame jitter, yet leaves the structural cause (single-codebook quantization) intact at the representation level. These methods collectively point to a core open problem: simultaneously capturing semantic structure (e.g., action labels, phase transitions) and physical dynamics (e.g., velocity, acceleration, contact forces) during tokenization. Since these two types of signals occupy overlapping frequency bands, disentangling them within a single quantization space is difficult. Prior works [7, 6, 4] seek this balance within a unified representation; in contrast, DS-FAST resolves it orthogonally by separating the two signal types before quantization, thereby preserving both high-level structure and low-level motion quality. 

### **A.3 Vision-Language-Action Models** 

Vision-Language-Action (VLA) models unify visual perception, language understanding, and action generation within a single end-to-end framework, representing a core research direction in embodied AI [39, 24]. Among representative works, OpenVLA [11], trained with 7B parameters on approximately 970,000 multi-robot trajectories from the Open X-Embodiment dataset [20], demonstrates strong generalization across diverse robotic platforms and manipulation tasks. _π_ 0 [2] achieves end-to- 

13 

end generation of 50 Hz high-frequency dexterous manipulation using a flow matching paradigm [14], setting a new standard for fine manipulation tasks that demand precise temporal control. Other notable efforts include RT-2 [3], which uses vision-language models (VLMs) for grounded robot control, and Octo [28], a generalist robot policy trained on large-scale multi-embodiment data. A recent survey [39] identifies that the quality of discrete action representations remains one of the core bottlenecks constraining the fine-grained control capabilities of VLAs, particularly in tasks requiring high-frequency feedback and multi-modal conditioning. Unlike the aforementioned VLA works, which primarily focus on low-level robot control with short-horizon actions (typically <5 seconds), MotionVLA in this paper targets vision- and text-conditioned fine-grained human motion generation, a domain characterized by higher semantic complexity, longer temporal durations, and richer multimodal conditioning. Specifically, human motions are more diverse and nuanced than robotic actions, spanning a richer space of activities, emotions, and styles; motion sequences often span 10–30 seconds, requiring long-range temporal coherence; and generation must be grounded simultaneously in both visual context (e.g., scene layout, object affordances) and linguistic descriptions. By addressing these challenges, MotionVLA extends the VLA framework to the domain of human motion synthesis, connecting robotic action generation and human-centric animation. 

## **B Detailed datasets and metrics** 

**ViMoGen-228K and MBench.** ViMoGen-228K [13] is a large-scale multimodal motion dataset containing 228K motion sequences collected from three sources: optical motion capture, in-thewild video annotation, and synthetic generation. In our experiments, MotionVLA is trained on the ViMoGen-228K training split and evaluated on MBench [13], following the official protocol. MBench contains 450 held-out prompts and reports eight fine-grained evaluation dimensions, including MotionCondition Consistency, Motion Generalizability, Jitter Degree, Dynamic Degree, Foot Floating, Foot Sliding, Body Penetration, and Pose Quality. 

**HumanML3D.** HumanML3D [8] is a standard benchmark for text-driven human motion generation. In our experiments, we train and evaluate MotionVLA on the official HumanML3D split under the standard text-to-motion setting. Because HumanML3D does not provide visual inputs, the model is used in text-only mode. Following prior work [8], we report FID, R-Precision (Top-1/2/3), MM-Dist, Diversity, and MModality using the official pretrained feature extractor. 

Table 8: **Baselines across three paradigms.** _†_ denotes visual conditioning (MotionVLA only). All prior methods are text-driven. 

|**Method**|**Venue**|**Paradigm**|**Tokenizer**|
|---|---|---|---|
|_Discrete Autoregressive_||||
|T2M-GPT [35]|CVPR 2023|AR (GPT)|VQ-VAE|
|MoMask [7]|CVPR 2024|Masked AR|RVQ|
|MG-MotionLLM [32]|CVPR 2025|AR (T5)|VQ|
|GenM3 [27]|ICCV 2025|Multi-path AR|Multi-expert VQ|
|_Diffusion / Flow Matching_||||
|MDM [29]|ICLR 2023|Diffusion|–|
|ViMoGen [13]|ICLR 2026|Flow Matching|–|
|_Improved Tokenization_||||
|DisCoRD [4]|ICCV 2025|AR + Flow|VQ + Rect. Flow|
|**MotionVLA (Ours)**<sup>_†_</sup>|–|AR (Qwen LoRA)|**DS-FAST**|


**Evaluation Metrics.** On MBench, we follow the official benchmark protocol and report eight dimensions. Motion-Condition Consistency measures whether the generated motion matches the input condition; Motion Generalizability evaluates semantic plausibility and diversity under unseen prompts; Jitter Degree measures local temporal instability; Dynamic Degree evaluates motion expressiveness; Foot Floating and Foot Sliding quantify contact realism; Body Penetration measures self-intersection artifacts; and Pose Quality evaluates overall pose naturalness. 

14 

On HumanML3D, we follow the standard text-to-motion evaluation protocol. FID measures the distribution distance between generated and ground-truth motions in the feature space; R-Precision evaluates text-motion retrieval accuracy; MM-Dist measures multimodal alignment distance; Diversity measures sample diversity across generated motions; and MModality evaluates motion variation under the same text condition. 

**Data Splits and Protocol.** For ViMoGen-228K, we use the official training split for model training and report results on the MBench evaluation set. For HumanML3D, we follow the official train/test split and the standard evaluation pipeline. All reported numbers are obtained under the corresponding benchmark protocols, and additional implementation details are provided in Appendix C. 

## **C Implementation Details** 

**DS-FAST Tokenizer Training.** For **ViMoGen** , the tokenizer is trained on 41,971 in-the-wild video motions and 50,000 randomly sampled optical motion-capture sequences from AMASS. The 276-dim vector is split into Base ( _Db_ =201) and Phys ( _Dp_ =75) by index slicing. For **HumanML3D** , the tokenizer is trained on the 23,384 official training sequences; the 263-dim vector is split into Base ( _Db_ =190, indices [7:197]) and Phys ( _Dp_ =73, indices [0:7] _∪_ [197:263]). In both settings, DCT truncation lengths are _Kb_ =5 and _Kp_ =25, and two independent BPE vocabularies of size 4,096 are trained per dataset. The trained tokenizers are then applied to all training samples: 212,913 for ViMoGen (41,971 in-the-wild video + 170,942 optical mocap) and 23,384 for HumanML3D. 

**Phase 1 — Embedding Cold Start.** The 8,195 newly added motion token embeddings are randomly initialized. All Qwen3.5 transformer layers are frozen; only `embed_tokens` and `lm_head` are trained for 500 steps with learning rate 1 _×_ 10<sup>_−_3</sup> and the Adafactor optimizer to warm up the motion token embedding space. 

**Phase 2 — LoRA Fine-Tuning.** Starting from the Phase-1 checkpoint, LoRA adapters are applied to all linear projections, while `embed_tokens` and `lm_head` continue to be updated as full saved modules. Training runs for 10 epochs on 8 _×_ H100 (80 GB) GPUs. All base Q wenweights remain frozen throughout. 

**Training Data.** ViMoGen mixes _In-the-Wild Video_ (41,971 samples, image + text) and _Optical MoCap_ (170,942 samples, text-only, real GT from AMASS). HumanML3D uses the official train/val/test split (23,384 / 1,460 / 4,384) with text-only inputs. 

**Inference.** The model runs on a single H100 (80 GB) GPU. The phase-aware logit mask constrains autoregressive decoding to Base tokens before `SEP` and Phys tokens after `SEP` . Generated tokens are decoded via BPE inverse mapping followed by IDCT to reconstruct the full motion sequence (276-dim for ViMoGen, 263-dim for HumanML3D). 

**Hyperparameters.** Table 9 lists the complete configuration. 

## **D DS-FAST Feature Partition Details** 

The Base/Phys partition assigns each dimension to the stream whose frequency profile it matches, determined by the low-frequency energy ratio (LFR) threshold of 0 _._ 6. Table 10 gives the complete per-field mapping for both ViMoGen (276-dim, SMPL+X) and HumanML3D (263-dim). 

In the ViMoGen representation, velocity fields occupy non-contiguous index ranges: `joints_vel` ([192:258]) is interleaved between the Base `joints` block ([126:192]) and the Base `root_orient_6d` block ([258:264]). DS-FAST extracts both streams by explicit index slicing prior to DCT, ensuring that each stream contains only physically homogeneous features. 

In HumanML3D, the LFR boundary falls within two semantic fields rather than between them: the 21-joint `local_pos` block is split so that the root joint position ([4:7]) enters the Phys stream due to its high-frequency root dynamics, while the remaining non-root positions ([7:67]) remain in Base; similarly, the first four elements of the 66-dim joint velocity block ([193:197]), which correspond to 

15 

Table 9: Full hyperparameter configuration for MotionVLA training. 

|**Hyperparameter**|**Value**|
|---|---|
|_DS-FAST Tokenizer_||
|Base stream dims_Db_<br>|201 (ViMoGen) / 190 (HumanML3D)<br>|
|Phys stream dims_Dp_<br>|75 (ViMoGen) / 73 (HumanML3D)<br>|
|DCT truncation_Kb_|5|
|DCT truncation_Kp_|25|
|BPE vocabulary per stream|4,096|
|_Vocabulary Expansion_||
|Qwen3.5 original vocab|248,320|
|Total vocab after expansion|256,515|
|New motion token embeddings|8,195|
|_Phase 1 — Embedding Cold Start_||
|Trainable parameters|`embed_tokens`,`lm_head`<br>|
|Learning rate|1_×_10<sup>_−_3</sup>|
|Optimizer|Adafactor|
|Steps|500|
|_Phase 2 — LoRA Fine-Tuning_||
|LoRA rank_r_|32|
|LoRA scaling_α_|64|
|Applied to|All linear projections<br>|
|Learning rate|2_×_10<sup>_−_4</sup>|
|LR schedule|Cosine decay|
|Optimizer|AdamW|
|Epochs|10|
|Per-device batch size|3|
|Gradient accumulation steps|2|
|Effective batch size|48 (8GPUs_×_3_×_2)|
|Max sequence length|4,700 tokens|
|Hardware|8_×_H100 (80 GB)|
|_Training Data_||
|ViMoGen total samples|212,913|
|In-the-Wild Video|41,971 (image+text)|
|Optical MoCap|170,942 (text-only)|
|HumanML3D training samples|23,384 (text-only)|


the root joint and exhibit low LFR, are assigned to the Base stream. These splits reflect the data-driven LFR criterion and do not require any manual field-boundary annotation. 

## **E Human Preference Analysis** 

To complement the quantitative benchmarks reported in Section 3, we conducted a human preference study to assess the perceptual quality of motions generated by MotionVLA. Evaluations were carried out through a custom web-based interface (Figure 5) that presented anonymized side-by-side motion pairs to domain experts. 

**Study Design.** We invited five domain experts in human motion analysis and character animation to participate in a blinded pairwise preference evaluation. Each expert assessed **100 text-conditioned motion pairs** , where each pair comprised one motion generated by MotionVLA and the corresponding output from ViMoGen [13]. To enable a comprehensive visual assessment, every motion clip was rendered from two camera perspectives— _front view_ and _side view_ —yielding four synchronized video clips per evaluation trial. Each clip was rendered as a 3-second video at 20 fps with the conditioning text prompt displayed above both clips. The left/right assignment of MotionVLA and the baseline was randomized per trial; experts were not informed of which method produced either clip. All participants volunteered without monetary compensation. As the study involved only viewing and comparing AI-generated skeletal motion clips with no collection of personal data, IRB approval was not required under our institutional guidelines. 

16 

Table 10: Per-field breakdown of the ViMoGen 276-dim and HumanML3D 263-dim motion vectors into Base ( _Db_ , position/rotation) and Phys ( _Dp_ , velocity) streams. Index ranges index into the flat per-frame feature vector **d** . 

|**Field**|**Semantics**|**Dims**|**Index range**|**Stream**|
|---|---|---|---|---|
|**ViMoGen** (276 dim|s, Base_Db_=201, Phys_Dp_=75)||||
|_Base stream — pos_|_ition and rotation_||||
|`body_pose_6d`|21 joints_×_6D rotation|126|`[:, 0:126]`|Base|
|`joints`|22 joints_×_XYZ position|66|`[:, 126:192]`|Base|
|`root_orient_6d`|Root global orientation (6D)|6|`[:, 258:264]`|Base|
|`root_trans`|Root global translation (XYZ)|3|`[:, 270:273]`|Base|
|_Phys stream — velo_|_city_||||
|`joints_vel`|22 joints_×_XYZ velocity|66|`[:, 192:258]`|Phys|
|`root_vel_6d`|Root rotational velocity (6D)|6|`[:, 264:270]`|Phys|
|`root_trans_vel`|Root translational velocity (XYZ)|3|`[:, 273:276]`|Phys|
|**HumanML3D** (263|dims, Base_Db_=190, Phys_Dp_=73)||||
|_Base stream — pos_|_ition and rotation_||||
|`local_pos`|Non-root joints XYZ position (20_×_3)|60|`[:, 7:67]`|Base|
|`local_rot`|<br>21 joints_×_6D rotation|126|`[:, 67:193]`|Base|
|`root_joint_vel`|Root joint velocity (low LFR)|4|`[:, 193:197]`|Base|
|_Phys stream — velo_|_city and root dynamics_||||
|`root_ang_vel`|Root angular velocity (Y-axis)|1|`[:, 0:1]`|Phys|
|`root_lin_vel`|Root linear velocity (X, Z)|2|`[:, 1:3]`|Phys|
|`root_height`|Root height (Y)|1|`[:, 3:4]`|Phys|
|`root_pos`|Root joint XYZ position|3|`[:, 4:7]`|Phys|
|`local_vel`|Non-root joint velocities (62dims)|62|`[:, 197:259]`|Phys|
|`foot_contact`|<br>Foot contact binary labels|4|`[:, 259:263]`|Phys|
|**Total — ViMoGen**||**276**|`[:, 0:276]`|—|
|**Total — HumanML**|**3D**|**263**|`[:, 0:263]`|—|


**Evaluation Protocol.** For each pair, the expert selected one of three options: 

**Good (G):** The left clip is clearly better overall. **Same (S):** The two clips are of comparable quality. **Bad (B):** The right clip is clearly better overall. 

After de-anonymizing, **G** indicates a preference for MotionVLA, **S** indicates no clear preference, and **B** indicates a preference for the baseline. Preference rates (%) are reported over all 5 experts _×_ 100 prompts = 500 comparisons. 

**Aggregate Results.** Table 11 reports the GSB preference rates of MotionVLA against ViMoGen, aggregated across all 500 comparisons. MotionVLA receives a clear majority preference (G = 64.0%), while only 14.0% of evaluations favor the baseline, demonstrating a substantial and consistent advantage in perceived motion quality across both front and side views. 

Table 11: GSB pairwise preference study results (%). G = MotionVLA preferred; S = no preference; B = baseline preferred. Results aggregated over 5 experts _×_ 100 prompts = 500 comparisons. 

|**MotionVLA vs.**|**G (Ours Better)**|**S (Same)**|**B (Baseline Better)**|
|---|---|---|---|
|ViMoGen [13]|64.0|22.0|14.0|


## **F Simulation and Real-Robot Demonstration** 

### **F.1 MuJoCo Simulation** 

All qualitative motion visualizations in this paper are produced using MuJoCo [30], a physics engine widely used in locomotion and character animation research. 

17 


Figure 5: Screenshot of the GSB evaluation interface used in our human preference study. Each trial displays two motion clips—Motion A and Motion B—rendered from _front_ and _side_ viewpoints simultaneously, with the conditioning text prompt shown above. Experts select one of three options: **G** (left clip better), **S** (comparable quality), or **B** (right clip better). The right panel tracks per-question completion progress across five evaluation dimensions. 


Figure 6: Capsule-skeleton rendering produced by MuJoCo. The motion decoded from DS-FAST tokens is converted to SMPL-X joint positions and rendered with per-sequence ground-contact alignment. 

**Pipeline.** The generated motion token sequence is first decoded by DS-FAST into a per-frame motion vector (276-dim for ViMoGen, 263-dim for HumanML3D) through inverse BPE followed by inverse DCT. This vector is then converted to SMPL-X [21] body parameters (global orientation, 22-joint body pose, and root translation). In MuJoCo, each frame is visualized as a capsule-based skeleton, where bone segments connecting adjacent joints are drawn as capsule geometries and joint centers are marked by spheres. The scene is evaluated with `mj_forward` in pure kinematic mode (no physical integration), so the rendered motion exactly reflects the model output without any simulation correction. 

**Rendering Configuration.** Frames are rendered with the MuJoCo offscreen renderer (EGL backend) at 1280 _×_ 1024 resolution and composited at 20 fps under a fixed side-view camera. To ensure plausible ground contact, a per-sequence vertical offset aligns the lowest foot position with the floor plane. 

18 


(c) The person walks straight ahead and then turns. 

Figure 7: Real-robot deployment of MotionVLA on a Unitree G1 EDU humanoid robot. Each row shows three exocentric frames from one text-conditioned motion execution, captured at different time steps. 

### **F.2 Real-Robot Deployment** 

We further deploy MotionVLA on a Unitree G1 EDU humanoid robot to verify that the generated motions can be executed on real hardware. Given a text prompt, the model produces a motion token sequence, which DS-FAST decodes into joint-angle trajectories. These trajectories are retargeted to the G1 joint configuration and executed in real time. 

Figure 7 presents three deployment examples. Each row corresponds to one text prompt, showing three exocentric frames captured at successive time steps. 

## **G Case Study: Scene-Conditioned Motion Generation** 

## **End-to-End Generation Example #1** 

### **Text prompt** 

_“Generate motion for: The person takes off a shirt and puts it on their head, then bends down to pick up something from the ground.”_ 


19 

#### _Scene image input_ 

**Generated token sequence.** Structural markers are highlighted: <mark>`<mot_bos>`</mark> opens the sequence, <mark>`<mot_sep>`</mark> separates Base and Phys streams, <mark>`<mot_eos>`</mark> closes it. Blue = Base stream ( _bi_ ); orange = Phys stream ( _pj_ ). 

```
<mot_bos><mot_b_1496><mot_b_2644><mot_b_1521><mot_b_1410>
```

- `<mot_b_1600> <mot_b_1506> <mot_b_1477> <mot_b_1457> <mot_b_1515>` 

```
<mot_b_1477><mot_b_1528><mot_b_1494><mot_b_1474><mot_b_1547>
```

```
<mot_b_1422><mot_b_1585><mot_b_1494><mot_b_1624><mot_b_1506>
```

_· · ·_ <mark>`<mot_sep>`</mark> `<mot_p_0298> <mot_p_0908> <mot_p_0318> <mot_p_0413> <mot_p_0431> <mot_p_0299> <mot_p_0336> <mot_p_0458> <mot_p_0240> <mot_p_2556> <mot_p_2761> <mot_p_3571>` _· · ·_ <mark>`<mot_eos>`</mark> 

**Reconstructed motion.** Decoded by DS-FAST (inverse BPE _→_ inverse DCT per stream _→_ concatenate) from the token sequence above. 


_Reconstructed motion sequence visualized at uniform time intervals_ 

## **End-to-End Generation Example #2** 

### **Text prompt** 

_“Generate motion for: The man walks towards the camera.”_ 


_Scene image input_ 

20 

**Generated token sequence.** Structural markers are highlighted: <mark>`<mot_bos>`</mark> opens the sequence, <mark>`<mot_sep>`</mark> separates Base and Phys streams, <mark>`<mot_eos>`</mark> closes it. Blue = Base stream ( _bi_ ); orange = Phys stream ( _pj_ ). 

<mark>`<mot_bos>`</mark> `<mot_b_1802> <mot_b_1570> <mot_b_1783> <mot_b_2401> <mot_b_1802> <mot_b_1416> <mot_b_1735> <mot_b_1423> <mot_b_1549> <mot_b_1802> <mot_b_1530> <mot_b_1796> <mot_b_1413> <mot_b_1483> <mot_b_1795> <mot_b_2200> <mot_b_1754> <mot_b_1410> <mot_b_1543>` _· · ·_ <mark>`<mot_sep>`</mark> `<mot_p_0243> <mot_p_0247> <mot_p_1751> <mot_p_1152> <mot_p_0857> <mot_p_1152> <mot_p_0857> <mot_p_0493> <mot_p_1152> <mot_p_0857> <mot_p_0493>` _· · ·_ <mark>`<mot_eos>`</mark> 

**Reconstructed motion.** Decoded by DS-FAST (inverse BPE _→_ inverse DCT per stream _→_ concatenate) from the token sequence above. 


_Reconstructed motion sequence visualized at uniform time intervals_ 

21 

