---
title: "SPECPRUNE-VLA: ACCELERATING VISION-LANGUAGE-ACTION MOD- ELS VIA ACTION-AWARE SELF-SPECULATIVE PRUN-"
venue: "Submitted to ICLR 2026"
original: "ICLR 2026 投稿時の匿名版"
url: https://arxiv.org/abs/2509.05614
pdf: https://arxiv.org/pdf/2509.05614
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.05614)** / [論文ページ](https://arxiv.org/abs/2509.05614)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。
> ICLR 2026 投稿時の匿名版から変換しました。リンク先の公開版とは内容が異なる場合があります。

Under review as a conference paper at ICLR 2026 

**000 001** 

# SPECPRUNE-VLA: 

> **002** ACCELERATING VISION-LANGUAGE-ACTION MOD- **003 004** ELS VIA ACTION-AWARE SELF-SPECULATIVE PRUN- 

> **005** ING **006 007 008 Anonymous authors 009** Paper under double-blind review **010 011 012** ABSTRACT **013 014 015** Pruning is a typical acceleration technique for compute-bound models by remov- **016** ing computation on unimportant values. Recently, it has been applied to accelerate Vision-Language-Action (VLA) model inference. However, existing meth- **017** ods focus on local information from the current action step and ignore the global **018** context, leading to _>_ 20% success rate drop and limited speedup in some sce- **019** narios. In this paper, we point out **spatial-temporal consistency** in VLA tasks: **020** input images in consecutive steps exhibit high similarity, and propose the key in- **021** sight that token selection should combine local information with global context of **022** the model. Based on this, we propose SpecPrune-VLA, a training-free, two-level **023** pruning method with heuristic control. **(1) Action-level static pruning.** We lever- **024** age global history and local attention to statically reduce visual tokens per action. **025 (2) Layer-level dynamic pruning.** We prune tokens adaptively per layer based **026** on layer-wise importance. **(3) Lightweight action-aware controller:** We classify **027** actions as coarse- or fine-grained by the speed of the end effector. Fine-grained actions are pruning-sensitive, so the controller adjusts pruning aggressiveness ac- **028** cordingly. Extensive experiments show that, compared to the high-performing **029** VLA model OpenVLA-OFT, SpecPrune-VLA achieves up to **1.57** _×_ speedup in **030** the LIBERO simulation benchmark across different hardware configurations and **031** an average speedup of **1.70** _×_ in **real-world robotic tasks** with negligible degra- **032** dation in task success rate. **033 034** 

> **035** 1 INTRODUCTION **036** 

**037** 

Vision-Language-Action (VLA) models, built upon large language models (LLMs), have gained **038** attention for their ability to interpret multimodal inputs and generate robotic actions. Models like **039** RT-1 (Brohan et al., 2022) and OpenVLA Kim et al. (2024) demonstrate strong cross-task gener- **040** alization and instruction-following capabilities from real-world robot data. Follow-up works Team **041** et al. (2024); Li et al. (2024b); Black et al. (2024); Kim et al. (2025) further are proposed for real- **042** time performance improvement. As shown in Figure 1(a), VLA inference typically involves: (1) **043** tokenizers for encoding multimodal inputs, (2) an LLM backbone for processing multimodal tokens **044** and generating intermediate outputs, and (3) an action head for producing low-level actions. We **045** profile three representative models, OpenVLA Kim et al. (2024), CogACT Li et al. (2024b), and **046** OpenVLA-OFT Kim et al. (2025)in Figure 1(b) and reveal that the LLM is the critical inference **047** bottleneck( _e.g._ , _>_ 70% of the end-to-end latency in even the most efficient model). Therefore, **048** most works target on the LLM acceleration via various acceleration methods Xu et al. (2025b); Hong et al. (2024); Park et al. (2024); Yue et al. (2024); Xu et al. (2025a). However, they largely **049** overlook VLA-specific computation patterns, limiting their effectiveness. Nowadays, the latest **050** VLA models ( _e.g._ , CogACT and OpenVLA-OFT) adopt the single-step paradigm that the model **051** directly predicts a sequence of low-level actions through a single LLM forward( _i.e._ , only prefill **052** phase) with hundreds of multimodal tokens. As a result, from the perspective of arithmetic intensity **053** ( _i.e._ , the amount of computation per byte) in the hardware roofline model, the VLA inference is primarily compute-bound, shown in Figure 1(c), where latency mainly arises from the computation 

1 

Under review as a conference paper at ICLR 2026 


2 

Under review as a conference paper at ICLR 2026 

**108 Last Action 109** Multi-view Images **110 111** … … … **112 113** Instructions **114 Static Token Pruning Global information reuse** Put the wine bottle **at Action Level 115** on top of the cabinet. **Now Action 116 117** Multi-view Images **118** … … … **119 120 121 Dynamic Pruning Lightweight Action122 at Layer Level aware Controller 123** Figure 2: Overview of SpecPrune-VLA. We prune the visual tokens with global and local informa- **124** tion with a lightweight action-aware controller. **125** control frequency and temporal coherence, modern VLAs adopt ACT Zhao et al. (2023), diffusion **126** models Peebles & Xie (2023), or parallel decoding for chunked action generation Li et al. (2024a). **127 128** 2.2 TOKEN-LEVEL ACCELERATION FOR VLA MODEL **129 130** Recent works explore token caching or pruning. VLA-Cache Xu et al. (2025b) reuses cached key- **131** value pairs from unimportant tokens, but only reduces 17–25% of total FLOPs and introduces addi- **132** tional GPU memory access overhead. EfficientVLA Yang et al. (2025) prunes visual tokens using **133** single-layer attention heuristics and supplements with diverse patches — yet this risks introducing **134** task-irrelevant content and lacks global context awareness. SP-VLA Li et al. (2025) retains tokens **135** with high vision encoder saliency to preserve spatial-semantic structure, but still fails to filter semantically redundant tokens, leaving unnecessary computation. **136 137** 2.3 SELF-SPECULATIVE DECODING AND LIGHTWEIGHT PREDICTORS **138 139** Unlike standard speculative decoding Leviathan et al. (2023) requiring a separate draft model, Lay- **140** erSkip Elhoushi et al. (2024) uses early layers of the same model for drafting and deeper layers **141** for verification, reducing memory and latency. Separately, SpecEE Xu et al. (2025a) employs a **142** lightweight predictor to shrink the output vocabulary by filtering low-probability tokens, signifi- **143** cantly lowering decoding cost. **144 145** 3 KEY INSIGHTS **146 147** 3.1 WHAT REALLY MATTERS IN THE IMAGE **148 149** We systematically study which image components are critical for Vision-Language-Action (VLA) **150** models. As shown in Figure 3, Insight 1(a), attention patterns evolve across layers. In the task “put **151** the bowl on the plate”, shallow layers attend broadly, including background and irrelevant regions **152** (e.g., table) but miss important object (e.g. bowl and plate); middle layers focus on semantically relevant objects that inform task understanding even though they may not involve with the action **153** (e.g., cabinet); deep layers focus on action-centric tokens directly involved in execution (e.g. plate). **154 155** To assess the value of this hierarchical attention, we conduct a post-hoc token pruning experiment. **156** Using attention scores between visual to text ( equation 2)—a commonly used importance proxy **157** Zhang et al. (2024b;a); Ye et al. (2025)—we identify layer-wise important tokens. Actions are **158** first generated without execution, then tokens are pruned based on attention scores, and actions are regenerated from the compressed input and executed. **159 160** Results (Figure 3, Insight 1(e)) show that random pruning maintains performance only up to 12.5% **161** sparsity, beyond which accuracy drops sharply, which indicates redundancy exists but also informed pruning guidance is needed. Pruning guided by shallow layers performs poorly under high sparsity 

control frequency and temporal coherence, modern VLAs adopt ACT Zhao et al. (2023), diffusion models Peebles & Xie (2023), or parallel decoding for chunked action generation Li et al. (2024a). 

Recent works explore token caching or pruning. VLA-Cache Xu et al. (2025b) reuses cached keyvalue pairs from unimportant tokens, but only reduces 17–25% of total FLOPs and introduces additional GPU memory access overhead. EfficientVLA Yang et al. (2025) prunes visual tokens using single-layer attention heuristics and supplements with diverse patches — yet this risks introducing task-irrelevant content and lacks global context awareness. SP-VLA Li et al. (2025) retains tokens with high vision encoder saliency to preserve spatial-semantic structure, but still fails to filter semantically redundant tokens, leaving unnecessary computation. 

Unlike standard speculative decoding Leviathan et al. (2023) requiring a separate draft model, LayerSkip Elhoushi et al. (2024) uses early layers of the same model for drafting and deeper layers for verification, reducing memory and latency. Separately, SpecEE Xu et al. (2025a) employs a lightweight predictor to shrink the output vocabulary by filtering low-probability tokens, significantly lowering decoding cost. 

We systematically study which image components are critical for Vision-Language-Action (VLA) models. As shown in Figure 3, Insight 1(a), attention patterns evolve across layers. In the task “put the bowl on the plate”, shallow layers attend broadly, including background and irrelevant regions (e.g., table) but miss important object (e.g. bowl and plate); middle layers focus on semantically relevant objects that inform task understanding even though they may not involve with the action (e.g., cabinet); deep layers focus on action-centric tokens directly involved in execution (e.g. plate). 

To assess the value of this hierarchical attention, we conduct a post-hoc token pruning experiment. Using attention scores between visual to text ( equation 2)—a commonly used importance proxy Zhang et al. (2024b;a); Ye et al. (2025)—we identify layer-wise important tokens. Actions are first generated without execution, then tokens are pruned based on attention scores, and actions are regenerated from the compressed input and executed. 

3 

Under review as a conference paper at ICLR 2026 


4 

Under review as a conference paper at ICLR 2026 

**216 217 218** 

**219 220 221 222 223 224** 


where _A_<sup>_h_</sup> _l_<sup>(</sup><sup>_Vi, tj_)denotestheattentionweightfromvisualtoken</sup><sup>_Vi_totexttoken</sup><sup>_tj_inattention</sup> head _h_ of layer _l_ . We define _Vglobal_ as the set of the top- _Kglobal_ visual tokens with the highest such attention scores from the middle and deep layers (we choose the 15th and 32nd layers) in the prior inference step. Based on our key insight that global information exhibits temporal consistency across consecutive actions, we retain _Vglobal_ in the current step. 

### 4.1.2 SUPPLEMENTATION OF DYNAMIC TOKENS 

**225 226** Visual tokens undergoing significant changes between inference steps cannot be reliably pruned **227** using global information from the prior step. To preserve up-to-date content, we explicitly retain **228** these _dynamic_ tokens during static pruning. Given frames _Imm_ and _Inn_ , we partition each into _N × N × N N_ **229** patches according to the token size. Let **P**<sup>_i,j_</sup> _t_ denote the feature vector of patch ( _i, j_ ) in frame _Itt_ . **230** The cosine similarity between corresponding patches is: **231 P**<sup>_i,j_</sup> _<u>m</u>_<sup>_·_</sup><sup>**P**</sup><sup>_i,j_</sup> _<u>n</u>_ **232** Sim( **P**<sup>_i,j_</sup> _m_<sup>_,_</sup><sup>**P**</sup><sup>_i,j_</sup> _n_<sup>) =</sup> _∥_ **P**<sup>_i,j_</sup> _m_<sup>_∥_</sup> 2<sup>_∥_</sup><sup>**P**</sup><sup>_i,j_</sup> _n_<sup>_∥_</sup> 2 _._ **233** To identify dynamic tokens, we first filter patches with similarity **234** scores below a threshold _τ_ , then select the top- _k_ patches with the current **235** lowest similarity scores from the remaining candidates. Formally, **236** let _Pn_ = _{_ **P**<sup>_i,j_</sup> _n_<sup>_|_1</sup><sup>_≤i, j≤N}_be the set of all patches in frame</sup> (a)consecutive frameCompare with last **237** _In_ . We define the candidate dynamic patches as those with signifi- **238** cant changes: **239** _Cn_ = � **P**<sup>_i,j_</sup> _n_<sup>_∈Pn_</sup> �� Sim( **P** _mi,j_<sup>_,_</sup><sup>**P**</sup> _n_<sup>_i,j_)</sup><sup>_< τ_</sup> � _._ (3) **240** The most dynamic _Kdynamic_ tokens are then given by: **241** _Vdynamic_ = Low- _Kdynamic {_ Sim _i,j |_ **P** _t_<sup>_i,j_</sup> _∈Ct} ,_ (4) current **242** � � **243** Additionally, as shown in Figure 4(a), directly comparing adjacent (b) Compare with frame **244** frames can yield inaccurate results due to camera noise and light chosen by velocity changes, especially in real-world scenarios. Therefore, we propose Figure 4: Adaptive selection **245** a **_velocity-based frame sampling_** strategy. This method selects a strategy for frame compari- **246** historical reference frame that is _T_ frames before the current one, son. **247** where _T_ is calculated as: _T_ = _⌊b_ + _k · v⌋_ + 4. Here, _k_ = _−_ 1 and **248** _b_ = 7 are constants based on experimental results. _k_ inversely relates speed _v_ to _T_ , while _b_ adjusts **249** the baseline value of _T_ . The translational speed _v_ is discussed in Section 6. **250 251** 4.1.3 PRUNING BASED ON LOCAL INFORMATION **252** Due to changing sub-goals, we need to incorporate information of current generation by analyzing **253** attention-based importance using equation 2. Motivated by works in Section 2.3, we observed that **254** 80%–90% of top-k important tokens from the first two layers reappear in the final layer’s top-k **255** (Figure 5II, k=30), indicating early-layer attention provides reliable guidance for token selection. **256** Besides, the first layer alone shows a low hit rate and adding the third layer provides marginal gains **257** with extra latency. Considering precision and efficiency, we use the first two layers for speculation **258** to filter current important tokens. **259** In each layer, we select the _KL_ visual tokens with the highest attention scores to form a candidate set **260** _V_ (1) and _V_ (2) respectively, and take the union of these two sets as the local information representa- **261** tion: _Vlocal_ = _V_ (1) _∪V_ (2). Finally, all the retained token set is: _Vretain_ = _Vglobal ∪Vdynamic ∪Vlocal_ . **262 263** 5 LAYER-LEVEL DYNAMIC TOKEN PRUNING **264 265** To preserve the most important tokens in layers, we propose dynamic importance scoring mechanism **266** that leverages attention scores and layer confidence across LLM layers to prune tokens within layers. **267** 5.1 IMPORTANCE SCORE FORMULATION **268 269** The token importance score is initialized for the remaining visual tokens after static token pruning and subsequently updated in the target transformer layers. The importance score _s_<sup>(</sup> _i_<sup>_l_)</sup> takes into 

Visual tokens undergoing significant changes between inference steps cannot be reliably pruned using global information from the prior step. To preserve up-to-date content, we explicitly retain these _dynamic_ tokens during static pruning. Given frames _Imm_ and _Inn_ , we partition each into _N × N × N N_ patches according to the token size. Let **P**<sup>_i,j_</sup> _t_ denote the feature vector of patch ( _i, j_ ) in frame _Itt_ . The cosine similarity between corresponding patches is: 

5 

Under review as a conference paper at ICLR 2026 

**270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323** 


Figure 5: (I) Attention entropy differs across layers, but are similar throughout the task. (II) (a) Comparison of the hitrate between leveraging the first one, two, and three layers. (b) LLM latency comparison between leveraging the first one, two, and three layers. 

account both the relative importance weight of tokens and the layer contribution: 


where _ω_<sup>(</sup><sup>_l_)</sup> rank _,i_<sup>denotes</sup><sup>_rank-based weight_reflecting the token’s relative importance in attention rank-</sup> ing, _ω_ conf<sup>(</sup><sup>_l_)denotes</sup><sup>_layer confidence score_measuring the layer’s reliability</sup> 

**Rank-based Weight** For each attention head, visual tokens are ranked based on their image-to-text attention scores in equation 2. To emphasize the contribution of the most important tokens while maintaining a smooth decay in influence, we introduce a rank-based weighting scheme. This weight is defined as: _σ_ <u>(</u> _−k ·k · ·_ rank<sup>(</sup><sup>_l_))</sup> 


where rank<sup>(</sup> _i_<sup>_l_)</sup> is the attention ranking of token _ti_ in layer _l_ and _σ_ ( _x_ ) denotes the sigmoid function, which amplifies the differences between token rankings by mapping them to a smooth range, ensuring that higher-ranked tokens receive significantly more emphasis. 

**Layer Confidence Score** Inspired by Zhang et al. (2025), in Transformer layers, high attention entropy indicates a dispersed attention distribution, where the model fails to concentrate on salient tokens. As shown in Figure 5I, we observe that the attention entropy across layers in our VLA model varies significantly with depth, suggesting that different layers contribute unequally to identifying globally important information. 

We posit that layers with low entropy, focused attention are more reliable for token importance estimation. Let _A_<sup>(</sup><sup>_l_)</sup> _ij_<sup>denotetheattentionweightfromtextquerytoken</sup><sup>_i_toimagekeytoken</sup><sup>_j_in</sup> layer _l_ of the image-to-text attention. The average attention entropy is computed as: 


with _ϵ >_ 0 for numerical stability. Lower entropy corresponds to higher confidence, reflecting more focused and semantically grounded attention. This value is computed in the first inference step and reused thereafter due to high inter-step similarity (see Appendix A.4). 

### 5.2 DYNAMIC UPDATING MECHANISM 

The final importance score _Si_ for each token _ti_ is maintained through an exponential moving average across layers: 

_Si_<sup>(</sup><sup>_l_)</sup> = (1 _− β_ ) _· Si_<sup>(</sup><sup>_l−_1)</sup> + _β · s_<sup>(</sup> _i_<sup>_l_)</sup> (9) where _β_ is the learning rate controlling the update speed, set to 0.2, and _Si_<sup>(0)</sup> = 0 is set for initialization. For layers in update layer set, we prune 10% tokens with the lowest score. 

6 

Under review as a conference paper at ICLR 2026 

**324 325 326 327** 

## 6 LIGHTWEIGHT ACTION-AWARE CONTROLLER 

### 6.1 OBSERVATION AND INSIGHT 


**328** Empirically, aggressive token pruning leads to **(a) Coarse-grained** <mark>T</mark> otal Velocity **Fine-grained Coarse-grained Fine-grained 329** a drop in success rate. Frame-by-frame obser1.0 <mark>V</mark> ertical Velocity **330** vation reveals that failures predominantly oc0. <mark>5</mark> **331** curred during object-contact phases, such as **332** manipulation or placement (Figure 6(b)) where 0.0 even minor errors cause task failure. The task - 0. <mark>5</mark> **333 334** merely fails when those actions are success- 1.0 Timestep fully executed. This highlights that task suc- <mark>0 20 40 60 80 100 120</mark> **335** cess critically depends on _fine-grained_ actions, **336 337** whichtive to pruning.demand In contrast,high precision _coarse-grained_ and are sensi- ac- _Start_ **338** tions ( _e.g._ moving to a general location) toler- _Target Manipulate Transfer Place_ **339** ate more approximation. Specifically, when the **340** robot approaches an object, fine-grained con- **(b) 341** trol is essential for stable contact and success- **342** ful execution. Thus, action granularity dictates **343** the required level of visual fidelity and infer- **344** ence precision. **345** Inspired by this, we propose an action-aware **_Fail in manipulating Fail in placing object_ 346** pruning strategy: by detecting whether a step **347** requires fine or coarse control, our method preFigure 6: (a) The task process consists of four **348** serves more tokens during fine-grained phases stages, categorized into coarse- and fine-grained **349** and prunes more aggressively during coarseactions based on velocity. (b) Typical failures in **350** grained ones, improving both efficiency and fine-grained stages. success rate. **351 352 353** 6.2 METHOD **354** Robotic execution can be divided into four phases that reflects intrinsic task semantics : target- **355** ing, manipulating, transferring, and placing (Figure 6(a)). Manipulating and placing require high **356** precision and exhibit naturally low translational and rotational velocities, with non-positive _z_ -axis **357** displacement ∆ _z_ —a pattern inherent to fine-grained interaction. **358 359** Since actions span a fixed duration, end-effector velocity is measured as displacement per step. As **360** all training data are normalized prior to model input, the output displacements (∆ _x_<sup>_′_</sup> _,_ ∆ _y_<sup>_′_</sup> _,_ ∆ _z_<sup>_′_</sup> ) and **361** angular changes (∆ _α_<sup>_′_</sup> _,_ ∆ _β_<sup>_′_</sup> _,_ ∆ _γ_<sup>_′_</sup> ) are inherently in normalized form. This normalization ensures that velocity magnitudes lie in a consistent range across tasks and platforms, making our method **362** generalizable and independent of specific robot kinematics or environmental scaling.(Other settings **363** result in Appendix A.3) The translational and rotational velocities are computed as: **364** _vt_ = ~~�~~ (∆ _x_<sup>_′_</sup> )<sup>2</sup> + (∆ _y_<sup>_′_</sup> )<sup>2</sup> + (∆ _z_<sup>_′_</sup> )<sup>2</sup> _, vr_ = ~~�~~ (∆ _α_<sup>_′_</sup> )<sup>2</sup> + (∆ _β_<sup>_′_</sup> )<sup>2</sup> + (∆ _γ_<sup>_′_</sup> )<sup>2</sup> _,_ (10) **365 366** Analysis of trajectory data in Figure 6 reveals bimodal velocity distributions between coarse and **367** fine-grained phases. From this, we empirically identify thresholds: _vt_<sup>th,</sup><sup>_v_</sup> _r_<sup>th, and a small</sup><sup>_v_</sup> _z_<sup>th</sup><sup>_>_0.The</sup> **368** system enters precise mode when _vt < vt_<sup>th,</sup><sup>_vr<v_</sup> _r_<sup>th, and ∆</sup><sup>_z≤_0, and exits upon exceeding</sup><sup>_v_</sup> _t_<sup>thor</sup> **369** _vr_<sup>th(</sup><sup>_e.g._, during lifting).This adaptive control balances accuracy and efficiency (Alg 1, Appendix).</sup> **370 371** 7 EXPERIMENT **372 373** 7.1 EXPERIMENTAL SETTINGS **374 375 Simulation Benchmarks and Platforms** To validate the generalization of our method, we con- **376** duct evaluations both on the LIBERO simulation benchmark Liu et al. (2023a) and in the real world. **377** In simulation, we employ four task suites, LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long, to evaluate the model’s capabilities in spatial reasoning, object understanding, goal- 

7 

Under review as a conference paper at ICLR 2026 

**378** LIBERO benchmark Success Rate (%) Avg. Avg. **379** FLOPs **380** Method Spatial Object Goal Long Speedup SR(%) **381** OpenVLA-OFT 97.6% 96.5% 97.9% 94.5% 1.00 _×_ 96.6% 100% **382** SparseVLM 96.8% 94.2% 97.6% 93.6% 1.28 _×_ 95.6% 77% FastV 94.6% 95.8% 94.0% 88.8% 1.44 _×_ 93.3% 57% **383** DivPrune 92.4% 91.2% 89.0% 84.8% 1.46 _×_ 89.4% 54% **384** VLA-Cache 99.0% 97.7% 97.4% 93.6% 1.07 _×_ 96.9% 83% **385** EfficientVLA 96.5% 91.1% 96.0% 72.1% 1.52 _×_ 88.9% 35% **386** **<mark>Ours</mark>** <mark>(prune rate=0.8) 97.4% 95.8% 97.7% 93.4% 1.46</mark> _<mark>×</mark>_ <mark>96.1% 43%</mark> **387** Table 1: Performance Evaluation (Success Rate and Average Speedup) **388 389** directed planning and execution, and long-horizon task completion, respectively. All main experi- **390** ments are conducted on a Linux workstation with an NVIDIA A800-80GB GPU. **391 Implementation Details** We select the OpenVLA-OFT Kim et al. (2025) as the code base for **392** the implementation of our techniques. We report end-to-end latency, average speedup and success **393** rate in our result. The latency and speedup may fluctuate slightly across tasks due to the changing **394** environment and our method’s adaptability, we report the detail in the Appendix. We repeat every **395** task of every task suite for 40 to 50 times to mitigate the impact of random errors. The latency **396** here is defined as the time duration from when the model receives the input to when it generates the **397** action. We report the average inference time over the ten tasks within each task suite. **398 Baselines** We select OpenVLA-OFT and _π_ 0 as our target model( _π_ 0 result is in Appendix). It **399** utilizes DINOv2 Oquab et al. (2023) and SigLIP Zhai et al. (2023) as visual encoders to extract **400** visual features, Llama2-7B as the backbone LLM, and a four-layer MLP as an action head to gen- **401** erate continuous actions. The model receives two-view images: the third-person view and the wrist **402** view. We also consider five optimization methods: SparseVLM Zhang et al. (2024b), a framework **403** that adaptively sparsifies less important visual tokens and recycles their information to minimize **404** performance loss, DivPrune Alvar et al. (2025) selects diverse visual tokens to preserve information **405** and maintain accuracy. FastV Chen et al. (2024) prunes redundant visual tokens early in the model based on observed sparse attention patterns for efficient inference. EfficientVLA Yang et al. (2025), **406** a visual pruning approach for VLA models, and VLA-Cache Xu et al. (2025b) , which leverages **407** image similarity to cache features across time steps. **408 409 410** 7.2 PARAMETER SETUP **411 412** Our base K values are chosen to maximize the temporal consistency of important information, mea- **413** sured by the **_Recall of Important Tokens_** ( equation 1) as mentioned in our motivation. For the **414** _Kglobal_ , we evaluated value of 20, 30, 40 and observed the average recall rate Recall( _Vt−_ 1 _, Vt_ ) = **415** _|Vt−_ 1 _∩ Vt|/|Vt|_ is the highest when _Kglobal_ equals 30. For _Klocal_ and _Kdynamic_ , we tested several **416** pairs: (12, 15), (24, 20), (36, 30). The token set _V_<sup>ˆ</sup> _t_ ( _Vt_ supplemented by local and dynamic tokens), **417** reaches the highest recall rate Recall( _Vt−_ 1 _, V_<sup>ˆ</sup> _t_ ) = _|Vt−_ 1 _∩ V_<sup>ˆ</sup> _t|/|V_<sup>ˆ</sup> _t|_ when the pair equals (24, 20). **418** Therefore, we set the base value _Kglobal_ =30, _Klocal_ =24 and _Kdynamic_ =20. **419** Speedup ( ) **420** <mark>0.80 0.95</mark> 2 (a) (b) (c) **421** <mark>0.70 0.85</mark> **422** 0 1 **423** <mark>0.60 0.75</mark> 1.00 <mark>1.51 1</mark> .45 1.40 **424** <mark>0.50 0.65</mark> 0 **425** 100 20 30 40 (12, 10) (24, 20) (36, 30) **426** (d) **427428** 90 97. <mark>6 97.4 9</mark> 7.6 97.6 96. <mark>5 93.2 9</mark> 5.8 96.3 <mark>97.9 96.0 9</mark> 7.7 <mark>97.9</mark> 94. <mark>5 91.2 9</mark> 3.4 94.0 96. <mark>6 94.7 9</mark> 6.1 96.5 **429** 80 **430** LIBERO-Spatial LIBERO-Object LIBERO-Goal LIBERO-10 Average <mark>O</mark> penVLA-OFT <mark>α</mark> =0.6 <mark>α</mark> =0.8 <mark>α</mark> =1.0 **431** 

Figure 7: Ablation on base K value and prune rate 

8 

Under review as a conference paper at ICLR 2026 

**432 433** 

### 7.3 DESIGN SPACE EXPLORATION 

We use the prune ratio _α_ to adjust the overall K values by scaling _Ki_ = _α · Ki_ (The detail setup is in A.6.2) to control the aggressiveness of our pruning. Therefore we conduct a design space exploration to explore the impact of different prune ratios. The smaller the prune ratio, the more tokens are pruned, leading to a drop in success rate and a rise in speedup. To balance accuracy and speed, we set the prune ratio to 0.8 for universal setup. 

**434 435** is in A.6.2) to control the aggressiveness of our pruning. Therefore we conduct a design space exploration to explore the impact of different prune ratios. The smaller the prune ratio, the more **436** tokens are pruned, leading to a drop in success rate and a rise in speedup. To balance accuracy and **437** speed, we set the prune ratio to 0.8 for universal setup. **438 439** 7.4 EVALUATION ON SPEEDUP AND SUCCESS RATE **440 441** Table 1 shows the end-to-end evaluation on success rate (SR), latency and speedup on four LIBERO **442** task suits. SpecPrune-VLA reduces FLOPs by 57% and achieves an average speedup of 1.45 _×_ with negligible loss ( _<_ 0 _._ 5%)) in success rate. SparseVLM yields limited speedup and degraded **443** SR, as its pruning, recycling, and merging strategy only minimally reduces computation and is not **444** suited for precise action generation. Compared to FastV and DivPrune (both retaining similar token **445** counts with our method for fairness), our method achieves comparable speedup but superior SR. **446** FastV prunes tokens using early-layer attention without training, ignoring global context; DivPrune **447** maximizes feature diversity but neglects task-relevant token importance in VLA models. VLA- **448** Cache maintains high SR by mitigating noise and improving motion continuity through caching, **449** yet achieves limited speedup due to small computation reduction (17%) and GPU memory access **450** overhead. EfficientVLA (L=28, T=112) attains higher speedup by skipping layers and aggressive **451** token pruning, but suffers notable SR drops in certain scenarios by compromising critical action- **452** related information in hidden states—this approach was originally designed for VLA models with a **453** diffusion-based action expert, which may better tolerate perturbations in action outputs. **454** 7.5 ABLATION STUDY **455 456 Ablation on global attention reuse** We compare recall rate as equation 1 and success rate of **457** pruning with and without global attention reuse in static pruning stage. The recall rate represents the **458** overlap between final retain token and ground-truth important token set. For fair comparison, we **459** set _K_ local= 54 when without global attention reuse, otherwise, we set= 54 when without global attention reuse, otherwise, we set _K_ local = 24,, _K_ global = 30.. As **460** shown in Table 2, incorporating global context yields better token recall and higher success rates, **461** indicating that prior-step attention provides valuable, task-relevant and action-centric guidance. This **462** supports our key insight: spatio-temporal coherence in robotic tasks makes previous-step global **463** attention a reliable prior for the current inference step. **464 Ablation on entropy-based layer weight** We compare recall rate and success rate of pruning **465** with and without entropy-based layer weighting in dynamic pruning stage in Table 3. From the **466** perspective of recall rate, average weighting utilizes uncertain information from high-entropy layers **467** and mistakenly prunes globally important tokens, thus achieving poorer success rate. **468** Method Recall (%) LIBERO SR (%) Method Recall (%) LIBERO SR (%) **469 470** w/ global attn. 92% 96.1% Entropy-based 88% 96.1% **471** w/o global attn. 84% 93.4% Average 66% 92.0% **472** Table 2: Ablation on global attention ablation Table 3: Ablation on entropy-based layer weight **473 Ablation on three techniques** To evaluate the effectiveness of our proposed method, we conducted **474** an ablation study on the LIBERO-Spatial task suit (Figure 8(a)). Our full model achieves a success **475** rate(SR) of 97.4%, comparable to the baseline (97.6%), and it significantly reduces latency from **476** 109ms to 72.3ms, resulting in a speedup of 1.51 _×_ compared to OpenVLA-OFT. This demonstrates **477** the efficiency gains of our approach while maintaining competitive accuracy. The ablation study **478** further highlights the importance of each component: Static (Tech 1) and Dynamic (Tech 2) pruning **479** slightly affect the SR (96.8%) but reduce latency to 70.8ms, indicating that pruning contributes to **480** the overall latency reduction. The introduction of the action-aware controller increases the success rate and causes negligible latency (1.5ms). This suggests that the controller plays a crucial role in **481** maintaining high accuracy. **482 483** 7.6 EXTENDED EVALUATION **484 485 Evaluation on Various Computing Platforms** To validate the applicability of our method on different devices, we conduct experiments on NVIDIA GeForce RTX 3090. As illustrated in Fig- 

Table 1 shows the end-to-end evaluation on success rate (SR), latency and speedup on four LIBERO task suits. SpecPrune-VLA reduces FLOPs by 57% and achieves an average speedup of 1.45 _×_ with negligible loss ( _<_ 0 _._ 5%)) in success rate. SparseVLM yields limited speedup and degraded SR, as its pruning, recycling, and merging strategy only minimally reduces computation and is not suited for precise action generation. Compared to FastV and DivPrune (both retaining similar token counts with our method for fairness), our method achieves comparable speedup but superior SR. FastV prunes tokens using early-layer attention without training, ignoring global context; DivPrune maximizes feature diversity but neglects task-relevant token importance in VLA models. VLACache maintains high SR by mitigating noise and improving motion continuity through caching, yet achieves limited speedup due to small computation reduction (17%) and GPU memory access overhead. EfficientVLA (L=28, T=112) attains higher speedup by skipping layers and aggressive token pruning, but suffers notable SR drops in certain scenarios by compromising critical actionrelated information in hidden states—this approach was originally designed for VLA models with a diffusion-based action expert, which may better tolerate perturbations in action outputs. 

**Ablation on global attention reuse** We compare recall rate as equation 1 and success rate of pruning with and without global attention reuse in static pruning stage. The recall rate represents the overlap between final retain token and ground-truth important token set. For fair comparison, we set _K_ local= 54 when without global attention reuse, otherwise, we set= 54 when without global attention reuse, otherwise, we set _K_ local = 24,, _K_ global = 30.. As shown in Table 2, incorporating global context yields better token recall and higher success rates, indicating that prior-step attention provides valuable, task-relevant and action-centric guidance. This supports our key insight: spatio-temporal coherence in robotic tasks makes previous-step global attention a reliable prior for the current inference step. 

9 

Under review as a conference paper at ICLR 2026 

**486** 100 2.0 300 100 **487** 98 <mark>(</mark> a <mark>) 1.42</mark> 1.54 1.51 1.5 225 1.65 (b) 75 **488489** 96 <mark>1.00</mark> 1.0 150 **1.67** × **1.53** × **1.64** × **1.43** × <mark>158.1 1.65</mark> **1.57** × 50 94 **490** 92 0.5 75 75.6 **2.09** × 25 **491** <mark>97.6 97.6 96.8 97.4</mark> 47.3 47.3 90 0.0 0 0 **492** None Tech.1 Tech.1&2 Tech.1&2&3 Spatial Object Goal Long Average **493** <mark>S</mark> uccess rate <mark>S</mark> peedup Ours OpenVLA-OFT Success rate Tokenizer LLM Action Head **494** Figure 8: (a) Ablation study in LIBERO-spatial. (b) Extended evaluation on NVIDIA 3090 GPU **495** ure 8(b), our method achieves an average speedup of **2.09** _×_ in LLM inference time and **1.57** _×_ in **496** end-to-end latency. The results consistently demonstrate improved inference efficiency, underscor- **497** ing the scalability and effectiveness of our approach under diverse computational conditions. **498 Generalization and Robustness analysis** We conduct experiments on LIBERO-plus Fei et al. **499** (2025) with prune ratio ( _α_ ) = 0.8 to validate the generalization and robustness. LIBERO-plus in- **500** cludes far more and challenging tasks. We choose 200 different long-horizon and object-recognition **501** tasks that adding perturbations to camera viewpoint, light condition, background and noise. With **502** degradation in success smaller than 0.6%, the results confirm that our configuration generalizes well **503** to unseen conditions and is robust to perturbations. **504 505 Method Camera Light Background Noise Avg. SR (%) 506** OpenVLA-OFT 96.0% 88.5% 95.0% 97.0% 94.1% **507** Ours ( _α_ =0.8) 94.0% 87.8% 95.0% 97.0% 93.5% **508** Figure 9: Generalization and robustnessperformance on LIBERO-plus **509** under various perturbations. **510 511** 7.7 EVALUATION ON REAL ROBOT Figure 10: LIBERO-plus **512 Primary 513 Experimantal settings** In this section, we evaluate **Camera 514** the real-world performance of our method. We use a Flexiv Rizon4 arm with three cameras with different **Intel RealSense Wrist 515 D435i Side Camera 516** viewpoints as the Figure 11 shows. We finetune the **Camera** model via LoRA Hu et al. (2022) with our collected **517** demonstration data following the configuration in the **518** OpenVLA-OFT training process. More configuration **519** and training details are in the Appendix. **Flexiv Rizon 4 520 521 Results** Table 4 reports the performance of Figure 11: Our real world robot: A Flexiv **522** SpecPrune-VLA in real-world tasks. Our method Rizon4 arm equipped with a gripper and achieves a 1.70 _×_ speedup while maintaining the sucthree Intel cameras. The cameras are **523 524** cess rate. The results show that SpecPrune-VLA is a mounted separately at three locations: on highly potential acceleration method for VLA models. the wrist, on its side, and above its head. **525 526 Success Rate (%) Avg Avg Method 527** Pick&Place TransferTube PickUpCup MultiCubeTask **Latency (ms) Speedup 528** OpenVLA-OFT 96.7 85.0 91.7 95.0 187.7 1 _._ 00 _×_ **529** Ours 96.7 82.0 90.0 95.0 110.2 1 _._ 70 _×_ **530 531** Table 4: Performance comparison on real-world robot tasks. **532 533** 8 CONCLUSION **534** We propose SpecPrune-VLA, a training-free, two-level token pruning method that combines lo- **535** cal and global information for efficient token selection. On the LIBERO benchmark, it achieves **536** 1.46 _×_ and 1.57 _×_ speedups on NVIDIA A800 and RTX 3090 GPUs respectively, with negligible **537** success rate drop. In real-world tasks, it delivers a 1.70× speedup without compromising success **538** rate, demonstrating robust cross-hardware performance and strong real-world generalization. **539** 

Figure 11: Our real world robot: A Flexiv Rizon4 arm equipped with a gripper and three Intel cameras. The cameras are mounted separately at three locations: on the wrist, on its side, and above its head. 

10 

Under review as a conference paper at ICLR 2026 

#### **540 541** 

## REPRODUCIBILITY STATEMENT 

**542** To ensure reproducibility, we provide full details of hyperparameter settings, experimental environ- **543** ments (including benchmarks, hardware, and training procedures) in the main experiment section **544** and in the appendix in the experiment part. **545 546** REFERENCES **547 548** Saeed Ranjbar Alvar, Gursimran Singh, Mohammad Akbari, and Yong Zhang. Divprune: Diversity- **549** based visual token pruning for large multimodal models. In _Proceedings of the Computer Vision_ **550** _and Pattern Recognition Conference_ , pp. 9392–9401, 2025. **551 552** Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo **553** Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. **554 555** Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, **556** Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics **557** transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. **558 559** Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and **560** Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. **561 562** Liang Chen, Haozhe Zhao, Tianyu Liu, Shuai Bai, Junyang Lin, Chang Zhou, and Baobao Chang. **563** An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large vision- **564** language models. In _European Conference on Computer Vision_ , pp. 19–35. Springer, 2024. **565 566** Mostafa Elhoushi, Akshat Shrivastava, Diana Liskovich, Basil Hosmer, Bram Wasti, Liangzhen Lai, **567** Anas Mahmoud, Bilge Acun, Saurabh Agarwal, Ahmed Roman, et al. Layerskip: Enabling early exit inference and self-speculative decoding. _arXiv preprint arXiv:2404.16710_ , 2024. **568 569** Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo **570** Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of vision-language-action **571** models. _arXiv preprint arXiv:2510.13626_ , 2025. **572 573** Ke Hong, Guohao Dai, Jiaming Xu, Qiuli Mao, Xiuhong Li, Jun Liu, Kangdi Chen, Yuhan Dong, **574** and Yu Wang. Flashdecoding++: Faster large language model inference with asynchronization, flat gemm optimization, and heuristics. _Proceedings of Machine Learning and Systems_ , 6:148– **575** 161, 2024. **576 577** Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, **578** Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. **579 580** Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, **581** Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. **582 583** Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Opti- **584** mizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. **585 586** Yaniv Leviathan, Matan Kalman, and Yossi Matias. Fast inference from transformers via speculative **587** decoding. In _International Conference on Machine Learning_ , pp. 19274–19286. PMLR, 2023. **588** Jinhao Li, Jiaming Xu, Shan Huang, Yonghua Chen, Wen Li, Jun Liu, Yaoxiu Lian, Jiayi Pan, **589** Li Ding, Hao Zhou, et al. Large language model inference acceleration: A comprehensive hard- **590** ware perspective. _arXiv preprint arXiv:2410.04466_ , 2024a. **591 592** Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, **593** Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024b. 

11 

Under review as a conference paper at ICLR 2026 

**594** 

**595 596 597** 

- Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024c. 

**598** Ye Li, Yuan Meng, Zewen Sun, Kangye Ji, Chen Tang, Jiajun Fan, Xinzhu Ma, Shutao Xia, Zhi **599** Wang, and Wenwu Zhu. Sp-vla: A joint model scheduling and token pruning approach for vla **600** model acceleration. _arXiv preprint arXiv:2506.12723_ , 2025. **601** Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: **602** Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information_ **603** _Processing Systems_ , 36:44776–44791, 2023a. **604 605** Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances_ **606** _in neural information processing systems_ , 36:34892–34916, 2023b. **607 608** Huaping Liu, Xinghang Li, Peiyan Li, Minghuan Liu, Dong Wang, Jirong Liu, Bingyi Kang, Xiao **609** Ma, Tao Kong, and Hanbo Zhang. Towards generalist robot policies: What matters in building vision-language-action models. 2025. **610 611** Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Lily Lee, Kaichen Zhou, Pengju An, Senqiao Yang, **612** Renrui Zhang, Yandong Guo, and Shanghang Zhang. Robomamba: Multimodal state space model **613** for efficient robot reasoning and manipulation. _arXiv e-prints_ , pp. arXiv–2406, 2024. **614** 

**615** Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, **616** Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning **617** robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. **618** 

- **618** Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham **619** Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: **620** Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE_ **621** _International Conference on Robotics and Automation (ICRA)_ , pp. 6892–6903. IEEE, 2024. **622** 

- **623** Seongmin Park, Hyungmin Kim, Wonseok Jeon, Juyoung Yang, Byeongwook Jeon, Yoonseon Oh, **624** and Jungwook Choi. Quantization-aware imitation-learning for resource-efficient robotic control. **625** _arXiv preprint arXiv:2412.01034_ , 2024. **626** 

   - William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 4195–4205, 2023. 

- **627 628** 

- **629** Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep **630** Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot **631** policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

**632** 

- Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, 

- **633** Jialin Wang, Wenbin Ge, Yang Fan, Kai Dang, Mengfei Du, Xuancheng Ren, Rui Men, Dayiheng 

- **634** Liu, Chang Zhou, Jingren Zhou, and Junyang Lin. Qwen2-vl: Enhancing vision-language model’s 

- **635** perception of the world at any resolution, 2024. URL https://arxiv.org/abs/2409.12191. 

**635 636** 

- **637** Junjie Wen, Yichen Zhu, Minjie Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Xiaoyu Liu, Chaomin **638** Shen, Yaxin Peng, and Feifei Feng. Diffusionvla: Scaling robot foundation models via unified **639** diffusion and autoregression. In _Forty-second International Conference on Machine Learning_ , 2025. 

**640** 

**641** 

- Jiaming Xu, Jiayi Pan, Yongkang Zhou, Siming Chen, Jinhao Li, Yaoxiu Lian, Junyi Wu, and Guo- 

- **642** hao Dai. Specee: Accelerating large language model inference with speculative early exiting. In 

- **643** _Proceedings of the 52nd Annual International Symposium on Computer Architecture_ , pp. 467– **644** 481, 2025a. 

- **644 645** 

- **646** Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Towards **647** efficient vision-language-action model via adaptive token caching in robotic manipulation. _arXiv preprint arXiv:2502.02175_ , 2025b. 

12 

Under review as a conference paper at ICLR 2026 

**648** Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei, Chang Zou, Zhipeng Zhang, Chuan Wen, **649** and Linfeng Zhang. Efficientvla: Training-free acceleration and compression for vision-language- **650** action models. _arXiv preprint arXiv:2506.10100_ , 2025. **651 652** Weihao Ye, Qiong Wu, Wenhao Lin, and Yiyi Zhou. Fit and prune: Fast and training-free visual **653** token pruning for multi-modal large language models. In _Proceedings of the AAAI Conference on_ **654** _Artificial Intelligence_ , volume 39, pp. 22128–22136, 2025. **655** Yang Yue, Yulin Wang, Bingyi Kang, Yizeng Han, Shenzhi Wang, Shiji Song, Jiashi Feng, and Gao **656** Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot **657** execution. _Advances in Neural Information Processing Systems_ , 37:56619–56643, 2024. **658 659** Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , **660** pp. 11975–11986, 2023. **661 662** Qizhe Zhang, Aosong Cheng, Ming Lu, Zhiyong Zhuo, Minqi Wang, Jiajun Cao, Shaobo Guo, **663** Qi She, and Shanghang Zhang. [cls] attention is all you need for training-free visual token prun- **664** ing: Make vlm inference faster. _arXiv e-prints_ , pp. arXiv–2412, 2024a. **665** Yuan Zhang, Chun-Kai Fan, Junpeng Ma, Wenzhao Zheng, Tao Huang, Kuan Cheng, Denis Gu- **666** dovskiy, Tomoyuki Okuno, Yohei Nakata, Kurt Keutzer, et al. Sparsevlm: Visual token sparsifi- **667** cation for efficient vision-language model inference. _arXiv preprint arXiv:2410.04417_ , 2024b. **668 669** Zhisong Zhang, Yan Wang, Xinting Huang, Tianqing Fang, Hongming Zhang, Chenlong Deng, **670** Shuaiyi Li, and Dong Yu. Attention entropy is a key factor: An analysis of parallel context en- **671** coding with full-attention-based pre-trained language models. In _Proceedings of the 63rd Annual_ **672** _Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pp. 9840– 9855, 2025. **673 674** Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual **675** manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. **676 677** Zixuan Zhou, Xuefei Ning, Ke Hong, Tianyu Fu, Jiaming Xu, Shiyao Li, Yuming Lou, Luning Wang, Zhihang Yuan, Xiuhong Li, et al. A survey on efficient inference for large language **678** models. _arXiv preprint arXiv:2404.14294_ , 2024. **679 680** Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, **681** Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge **682** to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. **683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701** 

- Weihao Ye, Qiong Wu, Wenhao Lin, and Yiyi Zhou. Fit and prune: Fast and training-free visual token pruning for multi-modal large language models. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pp. 22128–22136, 2025. 

13 

Under review as a conference paper at ICLR 2026 

**702 703 704 705** 

## A APPENDIX 

### A.1 USE OF LLM 

We used a large language model (LLM) solely for language editing purposes, including grammar correction, sentence restructuring, and clarity improvement. All technical content, methodology, experiments, and conclusions were developed and validated entirely by the authors. 

**706** We used a large language model (LLM) solely for language editing purposes, including grammar **707** correction, sentence restructuring, and clarity improvement. All technical content, methodology, **708** experiments, and conclusions were developed and validated entirely by the authors. **709 710** A.2 THE OVEREALL ALGORITHM OF ACTION-AWARE PRUNING **711 712** To clearly illustrate the control flow of our action-aware controller and pruning method, we present **713** in Algorithm 1. For each layer of the LLM, the input is the visual tokens from the previous layer (or initial input), and the output is the pruned set of visual tokens. **714** 

**715** If the current layer is among the first two layers, we select the top- _Klocal_ tokens according to their **716** attention scores and add them to the local important token set. After the second layer, we initialize **717** the retained token set _V_ retain with the top- _Kglobal_ globally important tokens inferred from the previ- **718** ous action step, and then augment it with locally inferred important tokens (top- _K_ base from Layer 1 **719** and 2) and _Kdynamic_ dynamically selected tokens based on low frame similarity. This constitutes the **static pruning at the action level** . **720 721** Subsequently, for each layer, we implement **dynamic pruning at layer level** . We dynamically **722** update token importance scores _s_<sup>(</sup> _i_<sup>_l_)</sup> based on layer-wise confidence and intra-layer attention ranking. **723** At designated pruning layers _L_ prune(see(see A.4), we perform a further pruning step, retaining only the **724** top _α × γ_ % tokens with the highest cumulative importance scores _Si_<sup>(</sup><sup>_l_).</sup> **725** 

Subsequently, for each layer, we implement **dynamic pruning at layer level** . We dynamically update token importance scores _s_<sup>(</sup> _i_<sup>_l_)</sup> based on layer-wise confidence and intra-layer attention ranking. At designated pruning layers _L_ prune(see(see A.4), we perform a further pruning step, retaining only the 

**726** The two-level pruning is scheduled by the action-aware controller. It determines the current action mode(fine or coarse grained) and adaptively adjusts the retain token from current local information. **727** 

**728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746** 

**Algorithm 1** Action-Aware Pruning in One Layer 

**Input** : Full token set _V_ (visual tokens from previous layer or initial input) **Parameters** : Pruning ratio _α_ , Velocity thresholds _vt_<sup>_th, v_</sup> _r_<sup>_th_,Decayfactor</sup><sup>_β_,Top-Ksizes</sup> 

_Klocal, Kdynamic, Kglobal_ and _γ_ %, Layer sets _Lprune_ 

**Output** : Retained token set _Vretain_ 

   - 1: **Action-aware Controller** 

   - 2: Compute translational velocity _vt_ and rotational velocity _vr_ from action history 

   - 3: **if** _vt < vt_<sup>_th_</sup> **and** _vr < vr_<sup>_th_</sup><sup>**and**∆</sup><sup>_z≤_0</sup><sup>**then**</sup> 

   - 4: Enter **fine-grained** 

   - 5: **else** 

   - 6: Enter **coarse-grained** 

   - 7: **end if** 

   - 8: **Static Token Pruning at Action Level** 

   - 9: _Vglobal ←_ top- _Kglobal_ tokens based on attention scores from the previous action step 

   - 10: Compute frame similarity _Sim_ ( _Pt, Pt−T_ ) _{_ Adaptive temporal window based on velocity _}_ 

   - 11: _Vdynamic ←_ lowest _Kdynamic_ similarity patches 

   - 12: For layers _l_ = 1 and _l_ = 2, compute attention scores: 

   - 13: _Vlocal_<sup>(</sup><sup>_l_)</sup><sup>_←_top-</sup><sup>_Klocal_tokens by attention score in layer</sup><sup>_l_</sup> 

   - 14: _Vlocal ← Vlocal_<sup>(1)</sup><sup>_∪V_</sup> _local_<sup>(2)</sup> 

- **747** 15: _Vretain ← Vglobal ∪ Vdynamic ∪ Vlocal {_ Initial retained set _}_ 

- **748** 16: **Dynamic Token Pruning at Layer Level** 

   - 17: **if** current layer _l ∈/ Lprune_ **then** 

**749** 

- 18: _s_<sup>(</sup> _i_<sup>_l_)</sup> _← ωrank,i_<sup>(</sup><sup>_l_)</sup><sup>_× ω_</sup> _conf_<sup>(</sup><sup>_l_)</sup><sup>_{_Token importance score</sup><sup>_}_</sup> 

**750** 

- **751** 19: _Si_<sup>(</sup><sup>_l_)</sup> _←_ (1 _− β_ ) _· Si_<sup>(</sup><sup>_l−_1)</sup> + _β · s_<sup>(</sup> _i_<sup>_l_)</sup> _{_ Exponential moving average _}_ 

- **752** 20: **else** 

- **753** 21: _Vretain ←_ tokens with top _α × γ_ % highest _Si_<sup>(</sup><sup>_l_)</sup> **754** 22: **end if 755** 23: **return** _Vretain_ 

14 

Under review as a conference paper at ICLR 2026 

**756 757 758 759 760 761 762 763** <mark>T</mark> ranslational Velocity **764** <mark>V</mark> ertical Velocity <mark>R</mark> otational Velocity **765 766 767 768** Timestep **769 770** Task: Put egg plant in basket **771 772 773 774 775 776** _Start_ _~~Target Manipulate Transfer Place~~_ **777 778** Figure 12: The task process is categorized into coarse- and fine-grained actions based on velocity. **779 780 781 782** A.3 GENERALIZATION OF ACTION MODE RECOGNITION **783 784** In Section 6.2, we observe that the execution process can be segmented into fine-grained and coarse- **785** grained modes based on thresholds for translational, vertical, and rotational velocities. Our results in **786** both the LIBERO simulation (using a Franka Emika Panda 6-DoF arm) and real-world experiments (using a Flexiv Rizon 4 7-DoF arm) demonstrate the generalization of this method. Furthermore, we **787** show that this characteristic is independent of the specific model, robot, or environment. To validate **788** this, we conduct experiments using a different VLA model, UniVLA Bu et al. (2025) within the **789** SimplerEnv Li et al. (2024c) simulation framework. Notably, SimplerEnv employs a WidowX-250 **790** 6-DoF robotic arm, which differs significantly in kinematics and control characteristics from the **791** previous platforms. As shown in the speed profile in Figure 12, the chosen thresholds consistently **792** distinguish between fine-grained and coarse-grained actions across different setups. **793 794** A.4 COMPLEXITY ANALYSIS **795 796 797** Consider a Transformer model with _N_ layers. The computational cost (in FLOPs) per layer when processing _L_ tokens is approximately: **798 799** FLOPslayer( _L_ ) = 4 _LD_<sup>2</sup> + 2 _L_<sup>2</sup> _D_ + 2 _LDM_ where: **800 801** • _L_ : sequence length (number of tokens) **802 803** • _D_ : hidden dimension **804 805** • _M_ : number of attention heads **806 807** In typical configurations, _D ≫ L_ and _D ≫ M_ , making the term 4 _LD_<sup>2</sup> the dominant component, **808** FLOPslayer( _L_ ) = 4 _LD_<sup>2</sup> + 2 _L_<sup>2</sup> _D_ + 2 _LDM ≈_ 4 _LD_<sup>2</sup> . Thus, the computation is primarily driven **809** by the feed-forward and attention projections in the hidden layers, and the overall complexity scales linearly with both sequence length. 

In Section 6.2, we observe that the execution process can be segmented into fine-grained and coarsegrained modes based on thresholds for translational, vertical, and rotational velocities. Our results in both the LIBERO simulation (using a Franka Emika Panda 6-DoF arm) and real-world experiments (using a Flexiv Rizon 4 7-DoF arm) demonstrate the generalization of this method. Furthermore, we show that this characteristic is independent of the specific model, robot, or environment. To validate this, we conduct experiments using a different VLA model, UniVLA Bu et al. (2025) within the SimplerEnv Li et al. (2024c) simulation framework. Notably, SimplerEnv employs a WidowX-250 6-DoF robotic arm, which differs significantly in kinematics and control characteristics from the previous platforms. As shown in the speed profile in Figure 12, the chosen thresholds consistently distinguish between fine-grained and coarse-grained actions across different setups. 

Consider a Transformer model with _N_ layers. The computational cost (in FLOPs) per layer when processing _L_ tokens is approximately: 

15 

Under review as a conference paper at ICLR 2026 

**Static Token Pruning** The static token pruning strategy reduces an average of 360 tokens from **811** the original about 600 tokens( _i.e._ 60% sparsity in input), let _Lr_ = 0 _._ 4 _· L_ denote the number of **812** retained tokens. **813 814** Prune Ratio _α_ 0.6 0.8 1.0 **815 816** Pruned Tokens 382 360 336 **817** Visual Retention 25.4% 29.8% 34.4% **818 819** Table 5: Number of pruned tokens and visual retention rate under different prune ratios. **820 821 822** Thus, for layers with _Lr_ length input, the FLOPs become FLOPs( _Lr_ ). For a model with H layers, **823** FLOPsstatic = 2FLOPs( _L_ ) + ( _H −_ 2)FLOPs( _Lr_ ) 

**824 825 Dynamic Token Pruning** We apply progressive token pruning in the depth interval [10 _,_ 25], with **826** pruning layers selected at regular intervals of _T_ . The set of pruning layers is defined as: **827** _S_ = _{sk_ = 10 + ( _k −_ 1) _T | sk ≤_ 25 _, k_ = 1 _,_ 2 _, . . .} ,_ **828** At each pruning layer _skk_ , we reduce the token count by a retention factor _γ_ = 0 _._ 9.. Starting from an initial retained length _Lrr_ , after the _k_ -th pruning step ( _i.e._ , at layer _skk_ ), the token count becomes **829** _γ_<sup>_k_</sup> _Lrr_ . The pruning interval is T layers. **830 831** The total computational cost is then: **832** _|S|−_ 1 **833834** FLOPsfinal = 2� _·_ FLOPs�� ( _L_ <u>�)</u> + 8� _·_ FLOPs�� ( _Lr_ <u>�)</u> + _k_ <u>�=1</u> _T ·_ FLOPs( _γ_<sup>_k_</sup> _Lr_ ) **835** early layers shallow layers � dynamic pruning�� <u>�</u> (11) **836** + ( _H −_ 10 _−_ ( _|S| −_ 1) _T_ ) _·_ FLOPs( _γ_<sup>_|S|_</sup> _Lr_ ) _,_ **837** <u>� �� �</u> **838** late layers **839** where _H_ is the total number of layers, and _Lr_ is the token count after static pruning. **840 841 Overall FLOPs reduction** In our configuration, the model has 32 layers and T is set to 5. There- **842** fore, FLOPsstatic = 0 _._ 44FLOPs( _L_ ), FLOPsfinal = 0 _._ 85FLOPsstatic = 0 _._ 37FLOPs( _L_ ). Dynamic **843** pruning leads 15% decrease in overall token-level computation across the model. The overall FLOPs reduction in LLM module is 63%. **844 845** COMPUTATION OVERHEAD **846 847 Patch similarity:** Calculating patch similarity introduces extra computations. The cosine similarity **848** is calculated based on the raw patches before the image being encoded. The similarity between **849850** corresponding patches in two frames is computed as Sim( _Pm_<sup>_i,j, P_</sup> _n_<sup>_i,j_)=</sup> _∥PPm_<sup>_i,j_</sup> _<u>m</u>_<sup>_i,j∥_</sup> 2<sup>_·∥ PP_</sup> _<u>n</u>_<sup>_i,j_</sup> _n_<sup>_i,j∥_</sup> 2 , For N **851** patches and patch size p ,this operation has complexity _O_ ( _N · p_<sup>2</sup> ). Here N=256, p=14. **852 853 Attention entropy:** As defined in equation 7, the attention entropy is computed over the _L × L × L L_ **854** attention matrix at layer _l_ . Its complexity is _O_ ( _L_<sup>2</sup> ) and introduces 1ms latency. and introduces 1ms latency. Naively computing **855** it at every step would incur 32ms latency. To avoid this, we observe that entropy patterns are stable **856** across inference steps within the same task in Figure 5I. Therefore, we compute the layer confidence scores only once during the first inference and reuse them in subsequent steps. **857 858** Breakdown of every module shows that the computation overhead (calculating patch similarity cal- **859** culation and attention entropy) only introduces about 4.5% latency on average, which is negligible. **860 861** A.5 FURTHER ANALYSIS ON DIFFERENT VIEW OF IMAGES **862 863** Different camera viewpoints present distinct characteristics. In this section, we provide a systematic exposition of the first key insight. 

#### **810** 

At each pruning layer _skk_ , we reduce the token count by a retention factor _γ_ = 0 _._ 9.. Starting from an initial retained length _Lrr_ , after the _k_ -th pruning step ( _i.e._ , at layer _skk_ ), the token count becomes _γ_<sup>_k_</sup> _Lrr_ . The pruning interval is T layers. 

**Attention entropy:** As defined in equation 7, the attention entropy is computed over the _L × L × L L_ attention matrix at layer _l_ . Its complexity is _O_ ( _L_<sup>2</sup> ) and introduces 1ms latency. and introduces 1ms latency. Naively computing it at every step would incur 32ms latency. To avoid this, we observe that entropy patterns are stable across inference steps within the same task in Figure 5I. Therefore, we compute the layer confidence scores only once during the first inference and reuse them in subsequent steps. 

16 

Under review as a conference paper at ICLR 2026 

**864** 

**865 866 867 868 869 870 871 872 873 874 875 876 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 897** 

||**Latency Breakdown**|||
|---|---|---|---|
|**Similarity calculation**|**First 2 layers**<br>**Attention Entropy**|**Our Method**|**Original Model**|
|1_._8_±_0_._1ms|5_._5_±_0_._2ms<br>1_._0_±_0_._2ms|72–78ms|109_._0ms|


Table 6: Latency breakdown per module and comparison with the original model. 

**In the fixed view(** **_e.g._ third-person)** , such as high camera and side camera, the robot arm and the objects it touches are the dynamic components, while the task-related patches ( _e.g._ objects on the table) are relatively static, as Figure 13 shows. Therefore, the key is to extract the intersection of both — the regions that involve the dynamic and the task-relevant pixels. 

**In the dynamic view(** **_e.g._ wrist-mounted camera)** , although all objects are in motion, the pixel patches along object boundaries exhibit more significant changes. We process and interpret the temporal signal of a pixel patch using the Fourier transform: 


Here _p_ ( _t_ ) represents pixel intensity at time _t_ , _P_ ( _f_ ) denotes the frequency-domain representation of the signal, _f_ stands for frequency. Since objects have different colors from the background, the boundary patches will change color at a certain time. Therefore, in these regions, the resulting signal _p_ ( _t_ ) contains more abrupt changes, which correspond to higher energy in the high-frequency components of _P_ ( _f_ ). This indicates that boundary patches carry richer temporal dynamics. As a result, task-related patches and dynamic patches can be complementary to some extent, and their intersection can also be used to identify the most critical regions. 

### A.6 EXPERIMENT DETAILS 

### A.6.1 IMPLEMENTATION OF COMPARATIVE METHODS 

We provide details on the implementation of the baseline and comparative methods. All models were implemented on one A800 GPU. 

**OpenVLA-OFT** The latency and the success rate on four datasets are similar to the data in the original paper. 

**SparseVLM** SparseVLM is a visual pruning method for Vision-Language models. It dynamically prunes redundant image tokens layer-wise by leveraging self-attention mechanisms and textual guidance. 

**898 SparseVLM** SparseVLM is a visual pruning method for Vision-Language models. It dynamically **899** prunes redundant image tokens layer-wise by leveraging self-attention mechanisms and textual guid- **900** ance. **901 902 FastV** FastV prunes visual tokens inVLMs by learning adaptive attention patterns in early layers **903** and removing less attended tokens in subsequent layers, using the LLM’s signal to guide pruning in **904** a plug-and-play manner. **905 906 DivPrune** DivPrune formulates token pruning as a Max-Min Diversity Problem (MMDP), se- **907** lecting a subset of visual tokens that maximizes diversity to reduce redundancy, enabling effective **908** performance at high pruning ratios without fine-tuning or calibration. **909 910 VLA-Cache** While the original method was developed on the OpenVLA model, its authors **911** adapted and extended it to the OpenVLA-OFT. All results reported in our experiments are obtained **912** using the authors’ official implementation to ensure reproducibility. **913** 

**FastV** FastV prunes visual tokens inVLMs by learning adaptive attention patterns in early layers and removing less attended tokens in subsequent layers, using the LLM’s signal to guide pruning in a plug-and-play manner. 

**DivPrune** DivPrune formulates token pruning as a Max-Min Diversity Problem (MMDP), selecting a subset of visual tokens that maximizes diversity to reduce redundancy, enabling effective performance at high pruning ratios without fine-tuning or calibration. 

**914 EfficientVLA** The method focuses on VLA models with diffusion action expert and it also opti- **915** mizes the action expert. Besides, it has not been open-sourced. As a result, we only re-implement **916** it according to the details of visual token pruning and layer pruning provided in the original paper. **917** Following the reported setup, we retain 28 LLM layers and 112 visual tokens (total of two images) throughout inference. 

17 

Under review as a conference paper at ICLR 2026 

**918** A.6.2 PARAMETER SETUP **919 920 Base values for top-Ks** In static token pruning stage, the base value for top-Ks are _Kglobal_ =30, **921** _Klocal_ =24 and _Kdynamic_ =20 according to Section 7.2. The prune ratio _α_ adjust the overall K values **922** by scaling _Ki_ = _α · Ki_ . In fine-grained mode, _Kglobal_ =30 and _Klocal_ =40 which are higher because **923** the model needs more information to generate fine-grained action. _Kdynamic_ =10, which is lower **924** because, in fine-grained mode, the speed is much lower, resulting in fewer dynamic tokens will appear. **925 926** _Kglobal_ = _α ×_ 30 **927** coarse-grained mode _, Klocal_ = _α ×_ **928** �4024 _,,_ fine-grained mode _._ **929** coarse-grained mode _,_ **930** _Kdynamic_ = _α ×_ �1020 _,,_ fine-grained mode _._ **931** 

**932 The threshold** _τ_ **for Dynamic Token Selection** The threshold _τ_ for Dynamic Token Selection **933** filters patches with low change magnitude to avoid false positives caused by lighting or camera **934** noise. Since we select the top- _Kdynamic_ most dissimilar patches among those below _τ_ , the exact **935** value is not highly sensitive. In simulation, we set _τ_ =0.95 ; in real-world settings with higher noise, **936** we use _τ_ =0.8 . Experiments shows performance remains stable within a range of _τ ∈_ [0.9,0.99] in **937** simulation and _τ ∈_ [0.6,0.9] in real world, confirming robustness. **938** 

**939 Update Rate** _β_ **in dynamic pruning** Empirically, in exponential moving average (EMA) formu- **940** lations of the form _Si_<sup>(</sup><sup>_l_)</sup> = (1 _− β_ ) _· Si_<sup>(</sup><sup>_l−_1)</sup> + _β · s_<sup>(</sup> _i_<sup>_l_)</sup> , update rate is often set to a small value to ensure **941** smooth calculation. In our method, _β_ can be set in a loose range (0.1 - 0.3) without performance **942** loss. However, large value( _>_ 0.6) will cause loss in task success rate. This is because overly aggres- **943** sive updates amplify noise from early layers, causing unimportant tokens to be incorrectly assigned **944** high importance scores, while critical tokens may be mistakenly pruned. 

**945 946 Velocity threshold distinguishing action mode** Based on empirical data from Figure 12, 6, we set the final thresholds as _vt_<sup>th=0</sup><sup>_._5and</sup><sup>_v_</sup> _r_<sup>th=0</sup><sup>_._2.When</sup><sup>_vt<v_</sup> _t_<sup>th,</sup><sup>_vr<v_</sup> _r_<sup>th,and∆</sup><sup>_z≤_0,the</sup> **947** fine-grained action mode is triggered. An ablation study on the threshold values is conducted on the **948** LIBERO-spatial dataset, as summarized in Table 7. **949 950** _vt_<sup>th</sup> 0.3 0.5 0.7 _vr_<sup>th</sup> 0.1 0.2 0.4 **951** Success Rate 96 _._ 8 % 97 _._ 4 % 97 _._ 6 % Success Rate 96 _._ 8 % 97 _._ 4 % 97 _._ 4 % **952** Table 7: Ablation study of success rate under different threshold settings on LIBERO-spatial. **953** The results show that when the threshold values are too small, the majority of actions are classified **954** as “coarse-grained,” leading to aggressive pruning, which causes a noticeable drop in performance **955** (e.g., success rate drop by 0.6%). Conversely, when the threshold values are too large, nearly the **956** entire process is classified as “fine-grained,” resulting in more tokens being retained. Although this **957** yields minimal improvement in success rate, it introduces additional latency. Therefore, the chosen **958** thresholds ( _vt_<sup>th</sup> = 0 _._ 5, _vr_<sup>th=0</sup><sup>_._2)achieveanoptimalbalancebetweenaccuracyandefficiency,</sup> **959** ensuring high task success while maximizing inference acceleration. **960 961** A.6.3 DETAIL RESULTS **962** The detailed latency and speedup of baseline and different methods are listed in Table 8. **963 964** The results of different prune ratio are listed in Table 11. **965** We conducted multiple independent experiments using different random seeds to comprehensively **966** evaluate the performance stability of both the original model and our method. The results are re- **967** ported as mean success rates with fluctuation ranges, reflecting performance consistency across runs. **968** The data show that, despite minor variations, our method consistently achieves success rates very **969** close to those of the original model. In several cases, our approach demonstrates improved stability. **970** This indicates that our method maintains strong performance while achieving the intended improve- **971** ments, demonstrating its effectiveness and robustness. Values are reported as mean _±_ half-range ( _i.e._ , _±_<sup><u>max</u></sup><sup>_−_</sup> 2<sup><u>min</u></sup> ) over multiple runs. 

18 

Under review as a conference paper at ICLR 2026 

**972** Latency (ms) / Speedup Avg. Avg. **973** Method Latency(ms) Speedup **974** Spatial Object Goal Long **975** OpenVLA-OFT 109.0 / 1.00 _×_ 109.0 / 1.00 _×_ 109.0 / 1.00 _×_ 109.0 / 1.00 _×_ 109.0 1.00 _×_ **976** SparseVLM 85.3 / 1.28 _×_ 85.3 / 1.28 _×_ 85.3 / 1.28 _×_ 85.3 / 1.28 _×_ 85.3 1.28 _×_ **977** VLA-Cache 101.8 / 1.07 _×_ 101.8 / 1.07 _×_ 101.8 / 1.07 _×_ 101.8 / 1.07 _×_ 101.8 1.07 _×_ **978** EfficientVLA 71.7 / 1.52 _×_ 71.7 / 1.52 _×_ 71.7 / 1.52 _×_ 71.7 / 1.52 _×_ 71.7 1.52 _×_ **979** **<mark>Ours(</mark>** _<mark>α</mark>_ **<mark>= 0.8)</mark>** <mark>74.8 / 1.46</mark> _<mark>×</mark>_ <mark>74.5 / 1.46</mark> _<mark>×</mark>_ <mark>74.8 / 1.46</mark> _<mark>×</mark>_ <mark>75.8 / 1.44</mark> _<mark>×</mark>_ <mark>75.1 1.46</mark> _<mark>×</mark>_ **980** Table 8: Performance Evaluation (Latency and Speedup) **981 982** Success Rate (%) / Speedup Avg. Avg. Prune Ratio _α_ **983** SR (%) Speedup Spatial Object Goal 10 **984 985** None (OpenVLA-OFT) 97.6 / 1.00 _×_ 96.5 / 1.00 _×_ 97.9 / 1.00 _×_ 94.5 / 1.00 _×_ 96.6 1.00 _×_ **986** _α_ =1.0 97.6 / 1.41 _×_ 96.3 / 1.43 _×_ 97.9 / 1.40 _×_ 94.0 / 1.38 _×_ 96.5 1.40 _× α_ **=0.8 97.6 / 1.46** _×_ **95.8 / 1.46** _×_ **97.7 / 1.46** _×_ **93.4 / 1.44** _×_ **96.1 1.46** _×_ **987** _α_ =0.6 97.4 / 1.52 _×_ 93.2 / 1.50 _×_ 96.0 / 1.52 _×_ 92.2 / 1.51 _×_ 94.7 1.51 _×_ **988 989** Table 9: Ablation study on prune rate _α_ . Success rates (%) and speedup factors are reported per task. **990** Our method achieves optimal trade-off at _α_ = 0 _._ 8, achieving 1 _._ 45 _×_ average speedup with minimal **991** accuracy drop. **992 993 Result on more models** We also implement our method on _π_ 0 Black et al. (2024), a Transformer **994** based VLA model with a flow-matching action expert. Our method achieves 1.31 _×_ speedup with **995** only 0.7% degradation in success rate. This result consistently demonstrates the generalization ca- **996** pability of our method across different model architectures. The speedup is slightly lower compared to OpenVLA-OFT. Because the flow-matching action expert contains more parameters and requires **997** multiple denoising iterations during inference, resulting in a higher proportion of end-to-end latency. **998** Consequently, acceleration of the LLM backbone has a relatively smaller impact on the overall end- **999** to-end performance. In the future, exploration on optimizing the flow-matching module to improve **1000** its efficiency can be made. **1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 1023 1024 1025** 

19 

Under review as a conference paper at ICLR 2026 

**1026 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 1069 1070 1071 1072 1073 1074 1075 1076 1077 1078 1079** 

|Method|LIBERO-Spatial|Success Rat<br>LIBERO-Object|e (%)<br>LIBERO-Goal|LIBERO-10|Avg.<br>SR (%)|
|---|---|---|---|---|---|
|OpenVLA-OFT|98.2_±_0.6|96.9_±_0.35|97.2_±_0.4|94.8_±_0.25|96.8|
|Ours|98.0_±_0.5|96.1_±_0.7|97.0_±_0.6|94.3_±_0.25|96.4|


Table 10: Average success rates (%) with fluctuation ranges across datasets for the original model and our method. 

|Method||Success Rate (%)|/ Speedup||Avg.|Avg.|
|---|---|---|---|---|---|---|
||LIBERO-Spatial|LIBERO-Object|LIBERO-Goal|LIBERO-10|Speedup|SR (%)|
|_π_0|96.8 / 1.00_×_|98.8 / 1.00_×_|95.8 / 1.00_×_|85.2 / 1.00_×_|1.00_×_|94.2|
|_π_0+Ours|96.6 / 1.32_×_|98.0 / 1.31_×_|95.2 / 1.32_×_|84.2 / 1.30_×_|1.31_×_|93.5|


Table 11: Performance evaluation on _π_ 0 model. 

20 

Under review as a conference paper at ICLR 2026 


21 

Under review as a conference paper at ICLR 2026 

**1134 1135** 

### A.6.5 REAL WORLD EXPERIMENT 

**1136 Finetuning** Hyper parameters for OpenVLA-OFT training on real-world tasks are shown in Ta- **1137** ble 12. We train until the mean L1 loss between predicted and ground-truth normalized actions **1138** (scaled between [-1,+1]) falls below 0.01. We decay the learning rate from 5e-4 to 5e-5 after 50K **1139** steps. **1140 Hyperparameter Value 1141** # GPUs 8 × NVIDIA H200 (141GB VRAM) **1142** Learning rate (LR) 5e-4 (decays to 5e-5 after 50K steps for all tasks) **1143** Total batch size 64 (8 per GPU) **1144** # Train steps “Pick up the cube and place it in the pan.”: 80K **1145** “Remove the cube from the tube rack.”: 100K **1146** “Pick up the purple cube and put it in the pot.”: 80K **1147** “Lift the cup from the tray.”: 80K **1148** Input images 1 third-person + 1 side view + 1 wrist camera **1149** Image size 224 × 224 px **1150** Obs. history Single-step (no history) LoRA rank 32 **1151** Action chunk size 25 steps (open-loop execution) **1152** Use proprio Yes **1153** Use FiLM Yes **1154** Trainable params 853M total: 111M (LoRA) + 269M (action head) + 17M (proprio proj.) + 456M **1155** (FiLM proj.) **1156** Image augmentations Random crops (90%), color jitter: **1157** — Brightness: ±0.2 **1158** — Contrast: 0.8–1.2 **1159** — Saturation: 0.8–1.2 — Hue: ±0.05 **1160 1161** — Crop scale/ratio: [0.9, 0.9] / [1.0, 1.0] **1162** Table 12: OpenVLA-OFT hyperparameters for real-world experiments. Includes parallel decoding, **1163** action chunking, continuous actions with L1 regression, and additional inputs (wrist/side cameras + **1164** robot state). **1165 1166 Evaluation Details** All evaluations were performed on a single NVIDIA RTX 4090 GPU (24GB **1167** VRAM) as the inference machine. **1168** Real-world task details: **1169 1170** 1. **“Pick up the cube and place it in the pan.” 1171** • Task: Use the single-arm robot to grasp the cube and place it in the pan **1172** • Dataset: 52 demonstrations (52 training) **1173** • Episode length: 10576 timesteps (353 seconds) **1174** 2. **“Remove the cube from the tube rack.” 1175** • Task: Use the single-arm robot to grasp the tube and carefully place it on the desk **1176** • Dataset: 50 demonstrations (50 training) **1177** • Episode length: 10397 timesteps (347 seconds) **1178** 3. **“Pick up the purple cube and put it in the pot.” 1179 1180** • Task: Use the single-arm robot to grasp the purple cube and place it into the pot **1181** • Dataset: 56 demonstrations (56 training) **1182** • Episode length: 17129 timesteps (571 seconds) **1183** 4. **“Lift the cup from the tray.” 1184** • Task: Use the single-arm robot to reach for and lift the cup with a stable grasp **1185** • Dataset: 51 demonstrations (51 training) **1186** • Episode length: 11788 timesteps (393 seconds) **1187** 

Evaluation result: See Figure 14 

22 

Under review as a conference paper at ICLR 2026 


23 

