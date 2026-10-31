---
title: "CKT-WAM: Parameter-Efficient Context Knowledge Transfer Between World Action Models"
date: "2026-05-07"
authors: "Yuhua Jiang; Yijun Guo; Hongbing Yang; Guojun Lei; Nuo Chen; Yinuo Zhang"
url: https://arxiv.org/abs/2605.06247
pdf: https://arxiv.org/pdf/2605.06247
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.06247)** / [論文ページ](https://arxiv.org/abs/2605.06247)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **CKT-WAM: Parameter-Efficient Context Knowledge Transfer Between World Action Models** 

**Yuhua Jiang**<sup>1</sup><sup>_,_2</sup> **, Yijun Guo**<sup>2</sup> **, Hongbing Yang**<sup>1</sup><sup>_,_2</sup> **, Guojun Lei**<sup>2</sup> **, Nuo Chen**<sup>1</sup> **, Yinuo Zhang**<sup>1</sup> **, Shaoqiang Yan**<sup>1</sup> **, Bo Lin**<sup>1</sup> **, Feifei Gao**<sup>1</sup> **, Biqing Qi**<sup>3</sup> 1 Tsinghua University 2 LivsynRobotics 3 Shanghai AI Laboratory 

## **Abstract** 

World action models (WAMs) provide a powerful generative framework for embodied control, yet transferring knowledge across heterogeneous WAMs remains challenging due to mismatched latent interfaces, high adaptation cost, and the rigidity of conventional distillation objectives. We propose **CKT-WAM** , a parameterefficient **C** ontext **K** nowledge **T** ransfer framework that transfers teacher WAM’s knowledge into a student WAM through a compact context in the text embedding space, rather than output imitation or dense hidden-state matching. Specifically, CKT-WAM extracts intermediate teacher hidden states, reduces the number of tokens via compressors’ learnable-query cross attention (LQCA), and transforms them through an always-on generalized adapter, a lightweight router, and sparsely activated specialized adapters. The resulting context is then appended to the student’s conditioning textual embeddings, thereby injecting the transferred knowledge into the student with minimal architectural modification. Experiments show that CKT-WAM consistently improves zero-shot generalization and achieves the best overall performance on LIBERO-Plus, reaching 86.1% total success rate with only 1.17% trainable parameters, while approaching full finetuning performance. Beyond simulation, CKT-WAM also demonstrates strong real-world long-horizon manipulation ability, achieving the best average success rate of 83.3% across four multi-step and long-horizon tasks. Code is available at `https://github.com/YuhuaJiang2002/CKT-WAM` . 

## **1 Introduction** 

World action models (WAMs) have emerged as a powerful paradigm for embodied intelligence, explicitly modeling how visual observations evolve under action to support purposeful behavior [Ye et al., 2026]. Unlike standard vision-language-action (VLA) models [Brohan et al., 2023, Zitkovich et al., 2023, Jiang et al., 2025], which primarily learn a direct, reactive mapping from visual and linguistic inputs to robotic actions, WAMs integrate a generative understanding of the physical world into the control loop. Building upon early latent dynamics research [Ha and Schmidhuber, 2018, Hafner et al., 2020], recent literature has formalized two dominant WAM architectures: _imagine-thenexecute_ models that causally generate future visual trajectories before predicting actions [Li et al., 2026, Feng et al., 2025], and _joint-modeling_ frameworks that denoise future video and action tokens within a shared generative process [Bi et al., 2025, Zhu et al., 2025]. While these developments provide a holistic scaffolding for downstream decision-making, their explicit video synthesis often incurs substantial test-time latency. This bottleneck has prompted parallel efforts to bypass explicit video decoding during inference—such as VPP [Hu et al., 2024], UVA [Li et al., 2025], and FastWAM [Yuan et al., 2026], which decouples video co-training from test-time future imagination to achieve real-time efficiency. This tension between generative capability and deployment efficiency naturally raises a critical question: **rather than scaling a single model in isolation, can we efficiently transfer action-relevant world knowledge between different WAMs?** 

Preprint. 

This question is of immense practical importance. In real-world deployments, practitioners often have access to a powerful but computationally heavy teacher WAM and a lightweight student WAM bounded by strict latency or memory budgets. However, transferring knowledge across generative WAMs is non-trivial. While knowledge distillation has seen immense success in vision and language models [Hinton et al., 2015, Touvron et al., 2021], applying it across heterogeneous action architectures presents unique challenges. Direct fine-tuning is prohibitively expensive. Output-level imitation, such as policy distillation or logit matching [Rusu et al., 2016], can be brittle when the teacher and student utilize disparate latent parameterizations or asymmetric action heads. Conversely, deep structural alignment via full hidden-state or attention-map matching [Romero et al., 2015, Zagoruyko and Komodakis, 2017, Wang et al., 2020] imposes rigid architectural constraints and introduces severe overhead by forcing layer-by-layer mimicry [Jiao et al., 2020]. What is needed is a transfer mechanism that is both _architecture-compatible_ and _parameter-efficient_ . 

In this paper, we propose **CKT-WAM** , a parameter-efficient _context knowledge transfer_ framework between WAMs. Our key idea is that knowledge need not be transferred through logits, actions, or full hidden-state supervision; instead, a teacher WAM can provide a compact _context interface_ that is directly consumable by the student’s native generative pipeline. Given an observation and instruction, CKT-WAM extracts hidden states from an intermediate DiT layer of a teacher WAM. We propose compressors that reduce the token count via learnable-query cross attention (LQCA), and then transform the compressed teacher states through an always-on generalized adapter, a lightweight router, and sparsely activated specialized adapters. The resulting routed context tokens preserve task-relevant sufficient statistics while avoiding the cost of transferring full representations, and are injected into the conditioning textual embeddings of the student WAM with minimal architectural modification. Experiments show that CKT-WAM consistently improves zero-shot generalization and achieves the best overall performance on LIBERO-Plus, reaching 86.1% total success rate with only 1.17% trainable parameters, while approaching full fine-tuning performance. Beyond simulation, CKT-WAM also demonstrates strong real-world long-horizon manipulation ability, achieving the best average success rate of 83.3% across four multi-step tasks. 

## **2 Related Work** 

**WAMs.** World models were first developed for latent dynamics learning in prediction, planning, and control [Ha and Schmidhuber, 2018, Hafner et al., 2019, 2020, 2023]. Recent work extends them to embodied control, where WAMs model future visual dynamics under actions [Ye et al., 2026]. Existing WAMs mainly follow two directions: _imagine-then-execute_ [Li et al., 2026, Feng et al., 2025] and _joint modeling_ [Bi et al., 2025, Zhu et al., 2025]. Our work instead studies efficient knowledge transfer from a stronger teacher WAM to a lightweight student WAM. 

**Knowledge Transfer.** Knowledge transfer has evolved from distillation to intermediate feature and attention transfer [Hinton et al., 2015, Romero et al., 2015, Zagoruyko and Komodakis, 2017, Jiao et al., 2020], and has also been explored in policy learning [Rusu et al., 2016]. However, most methods assume aligned outputs or representations, which is less suitable for WAM-to-WAM transfer. CKT-WAM instead transfers compact intermediate context tokens through the student’s native conditioning pathway, enabling flexible transfer across heterogeneous WAM pairs. 

**Parameter-Efficient Adapters.** Parameter-efficient fine-tuning (PEFT) provides an efficient alternative to full fine-tuning. LoRA learns low-rank task updates [Hu et al., 2022], while spectral variants such as PiSSA and KaSA highlight the role of initialization and singular-component selection [Meng et al., 2024, Wang et al., 2025a]. MoE-style PEFT further improves capacity through routed experts [Liu and Luo, 2024, Tian et al., 2024]. 

## **3 Method** 

### **3.1 Overview** 

We propose CKT-WAM, a parameter-efficient context knowledge transfer framework between a teacher WAM and a student WAM. Rather than transferring full representations, CKT-WAM transfers task-relevant sufficient knowledge through two stages: teacher-side context construction and student- 

2 


Figure 1: Overview of **CKT-WAM** . Hidden states from a selected intermediate layer of the teacher WAM are transformed by the CKT module. The compressors use learnable-query cross-attention (LQCA) for token compression. A routing module aggregates the relevant branches into a compact context _CA_ , which the student WAM concatenates with its original textual embeddings _Et_ . The input image embeddings are denoted by _Ei_ , and PE is short for parameter-efficient. 

side context injection. The teacher produces an action-relevant intermediate representation, which is compressed by LQCA into a fixed-length context _CA_ and processed by an always-on generalized adapter, a lightweight router, and sparsely activated specialized adapters. The resulting context is appended to the student’s conditioning textual tokens _Et_ , injecting teacher knowledge while leaving the student denoising backbone unchanged. Both backbones are frozen, and only the lightweight CKT module is optimized. 

### **3.2 Teacher-Side Hidden States Selection for Efficient and Single-Pass Extraction** 

Suppose the teacher WAM contains _L_<sup>tea</sup> transformer blocks, and let _Hℓ_<sup>tea</sup> _∈_ R<sup>_B×N×d_tea</sup> denote the hidden states after the _ℓ_ -th block, where _B_ is the batch size, _N_ is the sequence length, and _d_<sup>tea</sup> is the teacher hidden dimension. We extract transferable knowledge from an intermediate block _ℓ_<sup>_∗_</sup> _∈{_ 1 _, . . . , L_<sup>tea</sup> _}_ . Using an intermediate teacher representation offers a better cost–utility trade-off than relying on the deepest layer, since it is already semantically structured and action-aware while avoiding the most expensive final-stage features. 

To reduce both latency and memory overhead, we do not use the teacher WAM to explicitly predict future video or future actions during inference. Instead, the teacher is repurposed as a _single-pass observation encoder_ : its input contains only the observed image tokens, and its hidden states are used solely for one-shot context construction. Let _X_ img and _X_ text denote the teacher-side visual and textual tokens, respectively. We execute the teacher DiT once and obtain the intermediate hidden states of the teacher as: 


where the timestep is fixed to _t_<sup>_∗_</sup> = 0. The resulting hidden states are transformed into _CA_ once and then reused across the entire denoising trajectory of the student WAM. Hence, the student no longer requires teacher forwarding at every denoising step. We set _t_<sup>_∗_</sup> = 0 because the teacher is not used to model a future denoising trajectory, but only to encode the current scene into a stable world-aware representation. Using the clean endpoint avoids injecting timestep-specific noise corruption into 

3 

teacher features and yields representations that are more deterministic and easier to reuse across all student timesteps. This is also consistent with recent one-shot teacher-querying strategies for efficient world-model-assisted action generation. 

### **3.3 Parameter-Efficient CKT Module** 

**Compressor: learnable-query cross-attention (LQCA) for token compression.** We first map _HT_ into the student feature space through a shared bottleneck adapter: 


where _W_ down _∈_ R<sup>_d_tea</sup><sup>_×db_</sup> and _W_ up _∈_ R<sup>_db×d_stu</sup> are the down- and up-projection matrices, _d_<sup>stu</sup> is the dimension of the student’s textual embeddings, _db_ is the bottleneck dimension, _ϕ_ ( _·_ ) is a nonlinear activation function, LN( _·_ ) denotes layer normalization, and Drop( _·_ ) denotes dropout. 

The core role of the compressor is to reduce the teacher sequence from _N_ tokens to a much smaller set of transferable tokens through LQCA. To this end, we introduce two learnable query banks, _Qg ∈_ R<sup>1</sup><sup>_×Kg×d_stu</sup> and _Qs ∈_ R<sup>1</sup><sup>_×Ks×d_stu</sup> , for the generalized and specialized branches, respectively, where typically _Kg, Ks ≪ N_ . Let _Q_<sup>˜</sup> _g ∈_ R<sup>_B×Kg×d_stu</sup> and _Q_<sup>˜</sup> _s ∈_ R<sup>_B×Ks×d_stu</sup> be their batch-wise broadcast. We derive keys and values from _Z_ as _KZ_ = _ZWK, VZ_ = _ZWV ,_ where _WK, WV ∈_ R<sup>_d_stu</sup><sup>_×d_stu</sup> are learnable projections. The compressed teacher contexts are then obtained by 


where _∗_ = _g_ and _∗_ = _s_ correspond to the generalized and specialized branches, respectively, and MHCA( _Q, K, V_ ) denotes multi-head cross-attention. 

This design can be viewed as a token-level compression operator: instead of passing the full teacher sequence of length _N_ to subsequent adapters, the compressor summarizes it into only _Kg_ or _Ks_ learnable query-conditioned tokens. As a result, the module not only allows the generalized and specialized branches to extract different aspects of the teacher representation, but also substantially reduces the downstream transfer cost by replacing long teacher sequences with compact contexts. The compressor enforces a bottleneck that extracts only task-relevant information from teacher representations. 

**Always-on generalized adapter.** On top of _Cg_<sup>0,weapplyonealways-ongeneralizedresidual</sup> bottleneck adapter: 


where _W_ down<sup>(</sup><sup>_g_)</sup><sup>_∈_R</sup><sup>_d_stu</sup><sup>_×rg_,</sup><sup>_W_(</sup> up<sup>_g_)</sup><sup>_∈_R</sup><sup>_rg×d_stu,and</sup><sup>_r_</sup> _g_<sup>_≪d_stuisthebottleneckdimension.Thus,</sup> the generalized branch is itself parameter-efficient and remains active for every input, capturing task-agnostic transferable structure. 

**Routed specialized adapters.** To model input-dependent transfer patterns, we introduce _M_ specialized adapters _{Em}_<sup>_M_</sup> _m_ =1<sup>.Each adapter is parameterized as a lightweight residual bottleneck operating</sup> on the specialized compact context: 


where _W_ down<sup>(</sup><sup>_m_)</sup><sup>_∈_R</sup><sup>_d_stu</sup><sup>_×rs_,</sup><sup>_W_(</sup> up<sup>_m_)</sup> _∈_ R<sup>_rs×d_stu</sup> , and _rs ≪ d_<sup>stu</sup> is the bottleneck dimension. Thus, each specialized branch is also parameter-efficient, while the residual form preserves the base specialized context and adds only a low-rank input-adaptive correction. 

**Route-first sparse execution.** Unlike dense multi-adapter aggregation, we first compute routing scores and execute only the selected adapters. Specifically, we summarize the teacher hidden states by average pooling, _hr_ = _N_ <u>1</u> � _Ni_ =1<sup>_HT_[:</sup><sup>_, i,_:]</sup><sup>_∈_R</sup><sup>_B×d_tea,andfeeditintoalightweightrouter</sup> to obtain routing probabilities _p_ = softmax( _ϕ_ ( _hrW_ 1) _W_ 2) _∈_ R<sup>_B×M_</sup> , where _HT ∈_ R<sup>_B×N×d_tea</sup> , _W_ 1 _∈_ R<sup>_d_tea</sup><sup>_×d_gate</sup> , and _W_ 2 _∈_ R<sup>_d_gate</sup><sup>_×M_</sup> . For each instance _b_ , we select the top- _k_ adapters _Ib_ = 

4 

TopK( _pb, k_ ) and renormalize their routing weights as _p_ ¯ _b,m_ = _pb,m/_<sup>�</sup> _j∈Ib_<sup>_pb,j_for</sup><sup>_m∈Ib_.The</sup> final specialized context is then computed by weighted sparse aggregation: 


Stacking all instances yields _Cs ∈_ R<sup>_B×Ks×d_stu</sup> . 

**Transferred context and efficiency.** We form the final transferred context by concatenating the generalized and specialized branches: 


The parameter efficiency comes from two sources. First, both WAM backbones are frozen, so only the CKT module is trainable. Second, the specialized branch is sparse: although we maintain _M_ adapters in total, only _k ≪ M_ adapters are active per instance. Let _P_ sh, _Pg_ , _Pe_ , and _Pr_ denote the parameter counts of the shared trunk, generalized adapter, one specialized adapter, and the router, respectively. Then there is _P_ train = _P_ sh + _Pg_ + _MPe_ + _Pr_ and _P_ active = _P_ sh + _Pg_ + _kPe_ + _Pr,_ where _P_ active denotes the parameters involved in one forward pass. 

### **3.4 Student-Side Textual Context Injection** 

Let _Et ∈_ R<sup>_B×Lt×d_stu</sup> denote the student textual embeddings. We inject the transferred teacher context by appending the aggregated context _CA_ to the conditioning sequence: 


where _⟨_ SEP _⟩_ is a learnable separator token. The augmented sequence is fed into the frozen student backbone only through multi-head cross-attention: 


In this way, each future-frame patch receives a content-conditioned residual from _CA_ through the same conditioning pathway used during pretraining, while leaving the denoising backbone unchanged. 

Importantly, this design is also geometry-preserving. The student’s 3D RoPE is applied only in visual self-attention and depends solely on the spatio-temporal indices of visual tokens, while cross-attention uses no positional encoding on the conditioning side. Therefore, extending the conditioning sequence from _Et_ to _E_<sup>˜</sup> _t_ does not alter the rotary geometry of the visual stream. More details are provided in Appendix B.5. 

### **3.5 Training Objective** 

During training, both the teacher WAM and the student WAM are frozen, and only the parameterefficient CKT module is optimized. This preserves the pretrained dynamics of both models and constrains knowledge transfer to lightweight generalized adapters, a router, and sparsely activated specialized adapters. We train CKT module with the student’s original diffusion-style latent objective over both future-video and future-action latents. Let _v_ 0 _∈_ R<sup>_B×Tv×dv_</sup> be the clean VAE-compressed future-video latent sequence, and let _a_ 0 _∈_ R<sup>_B×Ta×da_</sup> be the clean future-action sequence. For each training instance _b_ , we sample a shared noise level from the base model’s log-normal distribution, ln( _σb_ ) _∼N_ ( _P_ mean _, P_ std<sup>2)</sup><sup>_,_then draw modality-specific Gaussian noise</sup><sup>_ϵv_</sup> _b_<sup>_, ϵa_</sup> _b_<sup>_∼N_(0</sup><sup>_, I_)</sup><sup>_._The noisy</sup> latents are constructed as 


where _µ_ ( _·, ·_ ) is determined by the underlying SDE parameterization. Using the same _σb_ aligns the corruption level across video and action, while preserving modality-specific perturbations. Conditioned on _E_<sup>˜</sup> _t_ , the frozen student predicts the clean future action ˆ _a_ 0 = _Da_ ( _an,b_ ; _E_<sup>˜</sup> _t_ ) and clean future video ˆ _v_ 0 = _Dv_ ( _vn,b_ ; _E_<sup>˜</sup> _t_ ). The corresponding losses are 


5 

Table 1: LIBERO-Plus benchmark zero-shot performance. Results are shown in success rate (%). 

|Model|Camera|Robot|Language|Light|Background|Noise|Layout|Total|
|---|---|---|---|---|---|---|---|---|
|OpenVLA [Kim et al., 2025b]|0.8|3.5|23.0|8.1|34.8|15.2|28.5|15.6|
|WorldVLA [Cen et al., 2025]|0.1|27.9|41.6|43.7|17.1|10.9|38.0|25.0|
|NORA [Hung et al., 2025]|2.2|37.0|65.1|45.7|58.6|12.8|62.1|39.0|
|UniVLA [Bu et al., 2025]|1.8|46.2|69.6|69.0|81.0|21.2|31.9|42.9|
|_π_0[Black et al., 2024]|13.8|6.0|58.8|85.0|81.4|79.0|68.9|53.6|
|_π_0-Fast [Pertsch et al., 2025]|65.1|21.6|61.0|73.2|73.2|74.4|68.8|61.6|
|_π_0_._5[Physical Intelligence et al., 2025]|75.4|77.5|85.6|96.9|94.6|89.7|85.7|85.7|
|OpenVLA-OFT [Kim et al., 2025a]|56.4|31.9|79.5|88.7|93.3|75.8|74.2|69.6|
|RIPT-VLA [Tan et al., 2025]|55.2|31.2|77.6|88.4|91.6|73.5|74.2|68.4|
|X-VLA [Zheng et al., 2025]|23.4|**89.7**|75.7|88.2|**96.0**|62.7|71.8|71.4|
|HoloBrain0-GD [Lin et al., 2026]|65.5|58.2|78.7|88.1|90.3|66.9|79.5|74.0|
|VLA-JEPA [Sun et al., 2026]|64.2|67.7|88.1|91.8|93.4|65.8|83.9|77.9|
|GE-Act [Liao et al., 2025]|60.7|77.0|77.4|95.8|86.0|90.9|80.2|80.3|
|VLANeXt [Wu et al., 2026]|71.6|63.4|81.4|93.7|91.8|89.5|77.7|80.1|
|ABot-M0 [Yang et al., 2026]|60.4|67.9|86.4|96.2|91.6|86.4|82.6|80.5|
|Cosmos-Policy [Kim et al., 2026]|75.8|63.3|81.7|96.5|88.9|92.7|82.2|82.2|
|**CKT-WAM (Ours)**|**77.4**|71.4|**86.7**|**98.2**|90.2|**94.8**|**88.5**|**86.1**|


where _ω_ ( _σb_ ) is the noise-dependent weight, _m_<sup>_a_</sup> _b,t_<sup>and</sup><sup>_mv_</sup> _b,t_<sup>are binary masks for valid action and</sup> future-video positions, and _Ta_ and _Tv_ denote the action-chunk and future-video lengths. 

To avoid routing collapse, we further use an MoE-style load-balancing loss. Let _Pm_ = _B_<sup><u>1</u></sup> � _Bb_ =1<sup>_pb,m_</sup> be the batch-averaged routing mass of adapter _m_ , and _fm_ = _kB_ <u>1</u> � _Bb_ =1<sup>I</sup><sup>_{m ∈Ib}_be its empirical</sup> top- _k_ selection frequency, where _Ib_ = Top-K( _{pb,m}m_<sup>_M_</sup> =1<sup>_, k_)</sup><sup>_._The auxiliary load balancing loss is</sup> _L_ bal = _M_<sup>�</sup><sup>_M_</sup> _m_ =1<sup>_fmPm,_and the overall objective is</sup> 


where _λ_ vid and _λ_ bal control the weights of future-video supervision and load balancing. 

## **4 Simulation Experiments** 

### **4.1 Experimental Settings** 

**Model setup.** We use Cosmos-Policy-2B as the student WAM and DreamZero-14B as the teacher WAM. The teacher and the student are kept frozen throughout training, while only the proposed CKT modules are optimized. For knowledge transfer, we use the hidden states from the _ℓ_<sup>_∗_</sup> = 20-th layer of the teacher, which has 40 layers in total. This choice provides an intermediate representation that is sufficiently informative for transfer, while avoiding the stronger task-specific bias often present in higher layers. 

**Training setup.** All models are trained on 8 NVIDIA A800 GPUs with distributed training in bfloat16. We use AdamW with _β_ 1 = 0 _._ 9, _β_ 2 = 0 _._ 95, weight decay 0 _._ 01, and a cosine learning-rate schedule with 1k warmup steps. Unless otherwise stated, the learning rate is set to 3 _×_ 10<sup>_−_4</sup> for adapter modules. For the shared projection in Eq. (2), we use bottleneck dimension _db_ = 512. For the compression of the teacher WAM’s knowledge, we use two learnable query banks of size _Kg_ = _Ks_ = 32, with 16 attention heads and 0.1 dropout rate. The compressed teacher context is computed once and reused by all downstream branches. Unless otherwise stated, we use _M_ = 8 routed branches with top-2 selection. The trainable parameters are only 187.4M (1.17%) parameters in the CKT module. We set _µ_ ( _v_ 0 _,b, σb_ ) = _v_ 0 _,b_ and _µ_ ( _a_ 0 _,b, σb_ ) = _a_ 0 _,b_ . The noise level is set as ln( _σ_ ) _∼N_ ( _P_ mean _, P_ std<sup>2), where</sup><sup>_P_mean=1</sup><sup>_._39 and</sup><sup>_P_std=1</sup><sup>_._2.We set the loss scaling factors as</sup> _λ_ vid = 1 and _λ_ bal = 0 _._ 01. 

### **4.2 LIBERO-Plus Results** 

We use LIBERO-Plus [Fei et al., 2025] as the simulation benchmark. The student WAM is initialized from the official Cosmos-Policy-LIBERO-Predict2-2B checkpoint. All models are trained on the combined training sets from all four suites of LIBERO [Liu et al., 2023], and evaluated in the 

6 

Table 2: Comparison with parameter-efficient adaptation methods on LIBERO-Plus. The column # Parameters denotes the ratio of trainable parameters to the overall parameters. 

|Model|# Parameters|Camera|Robot|Language|Light|Background|Noise|Layout|Total|
|---|---|---|---|---|---|---|---|---|---|
|Full Fine-tuning|100%|77.6|71.2|**87.5**|97.1|**91.0**|**95.7**|88.3|**86.3**|
|LoRA [Hu et al., 2022]|2.59%|76.1|67.9|81.6|95.9|88.1|90.4|84.7|82.8|
|PiSSA [Meng et al., 2024]|2.04%|75.2|68.5|84.2|96.1|88.4|90.6|85.1|83.3|
|DoRA [Liu et al., 2024]|2.06%|76.4|67.8|84.7|96.4|88.7|90.8|85.4|83.6|
|MiLoRA [Wang et al., 2025b]|1.73%|73.9|71.2|85.3|96.8|89.0|91.0|85.9|84.0|
|Mona [Yin et al., 2025]|1.65%|**79.2**|70.6|84.1|97.0|89.3|91.1|86.2|84.7|
|AdaMoLE [Liu and Luo, 2024]|1.69%|76.0|70.9|85.4|97.3|89.6|91.3|86.7|84.6|
|GOAT [Fan et al., 2025]|1.77%|75.0|71.0|86.1|97.7|89.9|91.6|87.4|84.8|
|**CKT-WAM (Ours)**|**1.17%**|77.4|**71.4**|86.7|**98.2**|90.2|94.8|**88.5**|86.1|


zero-shot setting under seven out-of-distribution dimensions: camera, robot, language, lighting, background, noise, and layout. 

As shown in Table 1, CKT-WAM achieves the best overall zero-shot performance on LIBEROPlus. Its advantage is not limited to a single perturbation type: the model attains the best results on camera, language, lighting, layout, and total success rate, while remaining competitive on the other dimensions. In particular, compared with prior VLA and WAM baselines, CKT-WAM shows stronger robustness under semantic variation and scene-level distribution shifts, suggesting that the transferred teacher knowledge improves both instruction grounding and generalization to unseen visual conditions. Although some competing methods are stronger on individual dimensions such as camera, robot, background, or noise, CKT-WAM delivers the most balanced performance across all out-of-domain (OOD) factors, which ultimately leads to the strongest aggregate generalization. 

### **4.3 Comparison with Parameter Efficient Adaptation Methods** 

To isolate the effect of different parameter-efficient adaptation strategies, we compare our method with a set of representative PEFT baselines, including LoRA [Hu et al., 2022], Mona [Yin et al., 2025], MiLoRA [Wang et al., 2025b], PiSSA [Meng et al., 2024], DoRA [Liu et al., 2024], GOAT [Fan et al., 2025], and AdaMoLE [Liu and Luo, 2024]. For all non-ours baselines, the hidden states extracted from the teacher WAM’s _ℓ_<sup>_∗_</sup> -th layer are first projected by a two-layer MLP and then concatenated with the student WAM’s textual input along the token dimension. When training baselines, the first _ℓ_<sup>_∗_</sup> -th layers of teacher WAM and the whole student WAM are adapted using the corresponding PEFT method. This setting keeps the teacher-student interaction interface fixed across baselines, so that the comparison mainly reflects the effectiveness of the adaptation mechanism itself. 

As shown in Table 2, CKT-WAM achieves the best overall performance among all PEFT baselines while using the smallest fraction of trainable parameters. Specifically, it improves the total success rate from 82.8% to 86.1% compared with LoRA, while reducing the trainable parameter ratio from 2.59% to 1.17%. It also consistently outperforms stronger recent PEFT methods such as AdaMoLE and GOAT, indicating that the gain does not come from increased adaptation capacity, but from a more effective mechanism for transferring teacher knowledge into the student WAM. The advantage of CKT-WAM is particularly clear under _robot_ , _light_ , and _layout_ shifts, where it achieves the best performance, and it remains highly competitive on the other dimensions. Compared with full finetuning, our method attains a nearly identical overall success rate (86.1% vs. 86.3%) using only 1.17% trainable parameters, while even surpassing it on _robot_ , _light_ , and _layout_ . Although full finetuning remains slightly stronger on _language_ , _background_ , and _noise_ , the gap in overall performance is marginal, suggesting that CKT-WAM captures most of the benefit of full adaptation at a tiny fraction of the optimization cost. Overall, these results demonstrate that CKT-WAM provides a substantially better trade-off between adaptation efficiency and zero-shot generalization than existing PEFT alternatives, while approaching the performance of full fine-tuning. 

### **4.4 Ablation Study** 

To understand the contribution of each component in CKT-WAM, we perform ablations on LIBEROPlus under the same zero-shot evaluation protocol. Specifically, “w.o. Generalized Adapter” removes the generalized adapter branch and keeps only the specialized adapter, “w.o. Specialized Adapters” 

7 

Table 3: Ablation study on LIBERO-Plus benchmark zero-shot performance. Results are shown in success rate (%). 

|Model|Camera|Robot|Language|Light|Background|Noise|Layout|Total|
|---|---|---|---|---|---|---|---|---|
|w.o. Context|75.8|63.3|81.7|96.5|88.9|92.7|82.2|82.2|
|w.o. Generalized Adapter|73.5|70.8|82.4|96.7|86.1|89.4|86.9|83.0|
|w.o. Specialized Adapters|72.8|68.1|82.3|97.0|88.7|90.6|85.7|82.7|
|w.o. Auxiliary Loss|75.0|70.9|83.6|97.6|86.9|92.2|86.9|84.1|
|**CKT-WAM (Ours)**|**77.4**|**71.4**|**86.7**|**98.2**|**90.2**|**94.8**|**88.5**|**86.1**|


Figure 2: Latency-success trade-off across different teacher intermediate layers _ℓ_<sup>_∗_</sup> . The left y-axis reports the zero-shot success rate on LIBERO-Plus, while the right y-axis reports inference latency in seconds per action chunk. 

removes the specialized adapter branch and retains only the generalized adapters, and “w.o. Auxiliary Loss” drops the auxiliary regularization while keeping the full architecture unchanged. 

As shown in Table 3, all three components of CKT-WAM contribute to the final zero-shot generalization performance, while their roles are not identical. Removing the specialized adapters causes the largest overall degradation, which suggests that instance-dependent specialization is particularly important for handling the diverse distribution shifts in LIBERO-Plus. Removing the generalized adapter also leads to a clear drop, indicating that the shared transfer branch provides a strong and stable foundation for cross-task knowledge injection. In contrast, removing the auxiliary loss yields the smallest degradation. This suggests that the auxiliary loss mainly acts as a regularizer that improves routing stability and adapter coordination, while the principal gains come from the joint use of generalized and specialized transfer pathways. Overall, these results validate that the full CKT-WAM design is necessary to obtain the strongest aggregate performance and the most balanced robustness across diverse OOD shifts. 

We ablate the teacher intermediate layer _ℓ_<sup>_∗_</sup> for context extraction under the LIBERO-Plus zero-shot setting. Figure 2 shows that success rate improves from 82 _._ 1% at _ℓ_<sup>_∗_</sup> = 0 to 86 _._ 1% at _ℓ_<sup>_∗_</sup> = 20, then saturates, while latency grows nearly linearly from 0 _._ 114 s to 0 _._ 587 s per action chunk. This suggests that intermediate teacher features provide the best balance between semantic usefulness and computational cost. We thus adopt _ℓ_<sup>_∗_</sup> = 20 as the default setting. 

## **5 Real-World Experiments** 

Our real-world evaluation focuses on _long-horizon, multi-step manipulation_ rather than single-step skills. As shown in Figure 3, we evaluate four representative tasks: clothes folding, fruit sorting, cube catching, and unmanned retail. All tasks require the policy to complete a sequence of dependent subgoals under continuous visual feedback. For each task, we conduct 45 trials in the real world and 

8 


Figure 3: Real-world long-horizon tasks in our evaluation. From left to right: ( **1** ) clothes folding, including removing distracting clothes, unfolding the garment, and folding it; ( **2** ) fruit sorting, placing the red apple and pear onto the designated plates; ( **3** ) cube catching, including opening the drawer, placing the purple block into the box, and closing the drawer; and ( **4** ) unmanned retail, picking target drinks from a cluttered shelf. All tasks require completing multiple ordered subgoals. 

Table 4: Real-world success rates (%) on four long-horizon and multi-step manipulation tasks. 

|Method|Clothes Folding|Fruit Sorting|Cube Catching|Unmanned Retail|Avg.|
|---|---|---|---|---|---|
|_π_0_._5[Physical Intelligence et al., 2025]|**77.8**|84.4|80.0|77.8|80.0|
|Cosmos Policy [Kim et al., 2026]|62.2|77.8|68.9|71.1|70.0|
|Fast-WAM [Yuan et al., 2026]|66.7|75.6|73.3|66.7|70.6|
|**CKT-WAM (Ours)**|73.3|**88.9**|**86.7**|**84.4**|**83.3**|


report the task success rate. Among these tasks, _clothes folding_ is particularly challenging because it involves **three consecutive stages** : removing distracting clothes, unfolding the target garment, and folding it. Failure at any intermediate stage can prevent successful task completion, making this setting a practical test of long-horizon real-world control. Detailed task descriptions and manipulation process are shown in Appendix B.3. 

As shown in Table 4, CKT-WAM achieves the best overall real-world performance, obtaining the highest average success rate of 83.3% across the four long-horizon tasks. Among the baselines, _π_ 0 _._ 5 is the strongest competitor with an average success rate of 80.0%, and it slightly surpasses our method on the most challenging _clothes folding_ task. Nevertheless, CKT-WAM achieves the best success rate on the other three tasks, namely _fruit sorting_ , _cube catching_ , and _unmanned retail_ . These results suggest that CKT-WAM provides stronger long-horizon planning and multi-stage execution ability in real-world settings, while remaining competitive on highly challenging deformable-object manipulation tasks. 

## **6 Conclusion** 

We presented CKT-WAM, a parameter efficient framework for transferring knowledge between world action models through a compact contextual interface. By combining intermediate-layer teacher representations, learnable-query compression, generalized and specialized sparse adapters, and lightweight conditioning-side injection, our method enables effective teacher–student transfer while keeping both backbones frozen. Experiments on LIBERO-Plus show that CKT-WAM delivers strong zero-shot generalization, outperforms representative PEFT baselines, and approaches full fine-tuning performance while updating only 1.17% of the parameters. Beyond simulation, CKT-WAM also demonstrates strong real-world long-horizon manipulation ability, achieving the best average success rate of 83.3% across four multi-step tasks. Together, these results highlight compact contextual transfer as a simple, efficient, and effective approach to enhancing WAMs. 

9 

## **References** 

- Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, et al. Motus: A unified latent action world model, 2025. arXiv preprint arXiv:2512.13030. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. URL `https://arxiv.org/abs/2410.24164` . 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alexander Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil J. Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Kuang-Huei Lee, Sergey Levine, Yao Lu, Utsav Malla, Deeksha Manjunath, Igor Mordatch, Ofir Nachum, Carolina Parada, Jodilyn Peralta, Emily Perez, Karl Pertsch, Jornell Quiambao, Kanishka Rao, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Kevin Sayed, Jaspiar Singh, Sumedh Sontakke, Austin Stone, Clayton Tan, Huong Tran, Vincent Vanhoucke, Steve Vega, Quan Vuong, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-1: Robotics transformer for real-world control at scale. In _Robotics: Science and Systems_ , 2023. 

- Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions, 2025. URL `https://arxiv.org/ abs/2505.06111` . 

- Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, Deli Zhao, and Hao Chen. Worldvla: Towards autoregressive action world model, 2025. URL `https://arxiv.org/abs/2506.21539` . 

- Shoufa Chen, Chongjian Ge, Zhan Tong, Jiangliu Wang, Yibing Song, Jue Wang, and Ping Luo. Adaptformer: Adapting vision transformers for scalable visual recognition. In _Advances in Neural Information Processing Systems_ , 2022. 

- Zhe Chen, Yuchen Duan, Wenhai Wang, Junjun He, Tong Lu, Jifeng Dai, and Yu Qiao. Vision transformer adapter for dense predictions. In _International Conference on Learning Representations_ , 2023. 

- Chenghao Fan, Zhenyi Lu, Sichen Liu, Chengfeng Gu, Xiaoye Qu, Wei Wei, and Yu Cheng. Make LoRA great again: Boosting LoRA with adaptive singular values and mixture-of-experts optimization alignment. In _Proceedings of the 42nd International Conference on Machine Learning_ , volume 267 of _Proceedings of Machine Learning Research_ , pages 15804–15832. PMLR, 2025. URL `https://proceedings.mlr. press/v267/fan25g.html` . 

- Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, Jinlan Fu, Jingjing Gong, and Xipeng Qiu. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 

- Yao Feng, Hengkai Tan, Xinyi Mao, Chendong Xiang, Guodong Liu, Shuhe Huang, Hang Su, and Jun Zhu. Vidar: Embodied video diffusion model for generalist manipulation. _arXiv preprint arXiv:2507.12898_ , 2025. 

- David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 

- Danijar Hafner, Timothy P. Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _Proceedings of the 36th International Conference on Machine Learning_ , volume 97 of _Proceedings of Machine Learning Research_ , pages 2555–2565, 2019. 

- Danijar Hafner, Timothy P. Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations_ , 2020. 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy P. Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- Geoffrey E. Hinton, Oriol Vinyals, and Jeffrey Dean. Distilling the knowledge in a neural network. _arXiv preprint arXiv:1503.02531_ , 2015. 

- Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. In _International Conference on Learning Representations_ , 2022. 

10 

- Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 

- Chia-Yu Hung, Qi Sun, Pengfei Hong, Amir Zadeh, Chuan Li, U-Xuan Tan, Navonil Majumder, and Soujanya Poria. Nora: A small open-sourced generalist vision language action model for embodied tasks, 2025. URL `https://arxiv.org/abs/2504.19854` . 

- Yuhua Jiang, Shuang Cheng, Yan Ding, Feifei Gao, and Biqing Qi. AsyncVLA: Asynchronous flow matching for Vision-Language-Action models, 2025. URL `https://arxiv.org/abs/2511.14148` . 

- Xiaoqi Jiao, Yichun Yin, Lifeng Shang, Xin Jiang, Xiao Chen, Linlin Li, Fang Wang, and Qun Liu. TinyBERT: Distilling BERT for natural language understanding. In _Findings of the Association for Computational Linguistics: EMNLP 2020_ , pages 4163–4174. Association for Computational Linguistics, 2020. 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success, 2025a. URL `https://arxiv.org/abs/2502.19645` . 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P. Foster, Pannag R. Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. In _Proceedings of The 8th Conference on Robot Learning_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 2679–2713, 2025b. 

- Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, and Jinwei Gu. Cosmos policy: Fine-tuning video models for visuomotor control and planning, 2026. URL `https://arxiv.org/abs/2601.16163` . 

- Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, et al. Causal world modeling for robot control. _arXiv preprint arXiv:2601.21998_ , 2026. 

- Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025. 

- Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Yue Hu, Jingbin Cai, Si Liu, Jianlan Luo, Liliang Chen, Shuicheng Yan, Maoqing Yao, and Guanghui Ren. Genie envisioner: A unified world foundation platform for robotic manipulation, 2025. URL `https://arxiv.org/abs/2508. 05635` . 

- Xuewu Lin, Tianwei Lin, Yun Du, Hongyu Xie, Yiwei Jin, Jiawei Li, Shijie Wu, Qingze Wang, Mengdi Li, Mengao Zhao, Ziang Li, Chaodong Huang, Hongzhe Bi, Lichao Huang, and Zhizhong Su. Holobrain-0 technical report, 2026. URL `https://arxiv.org/abs/2602.12062` . 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems_ , volume 36, pages 44776–44791, 2023. 

- Shih-Yang Liu, Chien-Yi Wang, Hongxu Yin, Pavlo Molchanov, Yu-Chiang Frank Wang, Kwang-Ting Cheng, and Min-Hung Chen. DoRA: Weight-decomposed low-rank adaptation. In _Proceedings of the 41st International Conference on Machine Learning_ , volume 235 of _Proceedings of Machine Learning Research_ , pages 32100–32121. PMLR, 2024. URL `https://proceedings.mlr.press/v235/liu24bn.html` . 

- Zefang Liu and Jiahua Luo. Adamole: Fine-tuning large language models with adaptive mixture of low-rank adaptation experts. In _Conference on Language Modeling_ , 2024. 

- Fanxu Meng, Zhaohui Wang, and Muhan Zhang. Pissa: Principal singular values and singular vectors adaptation of large language models. In _Advances in Neural Information Processing Systems_ , 2024. 

- Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models, 2025. URL `https://arxiv.org/abs/2501.09747` . 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. URL `https://arxiv.org/abs/2504.16054` . 

11 

- Adriana Romero, Nicolas Ballas, Samira Ebrahimi Kahou, Antoine Chassang, Carlo Gatta, and Yoshua Bengio. Fitnets: Hints for thin deep nets. In _International Conference on Learning Representations_ , 2015. 

- Andrei A. Rusu, Sergio Gómez Colmenarejo, Ça˘glar Gülçehre, Guillaume Desjardins, James Kirkpatrick, Razvan Pascanu, Volodymyr Mnih, Koray Kavukcuoglu, and Raia Hadsell. Policy distillation. In _International Conference on Learning Representations_ , 2016. 

- Jingwen Sun, Wenyao Zhang, Zekun Qi, Shaojie Ren, Zezhi Liu, Hanxin Zhu, Guangzhong Sun, Xin Jin, and Zhibo Chen. Vla-jepa: Enhancing vision-language-action model with latent world model, 2026. URL `https://arxiv.org/abs/2602.10098` . 

- Shuhan Tan, Kairan Dou, Yue Zhao, and Philipp Krähenbühl. Interactive post-training for vision-language-action models, 2025. URL `https://arxiv.org/abs/2505.17016` . 

- Chunlin Tian, Zhan Shi, Zhijiang Guo, Li Li, and Cheng-Zhong Xu. Hydralora: An asymmetric lora architecture for efficient fine-tuning. In _Advances in Neural Information Processing Systems_ , 2024. 

- Hugo Touvron, Matthieu Cord, Matthijs Douze, Francisco Massa, Alexandre Sablayrolles, and Hervé Jégou. Training data-efficient image transformers & distillation through attention. In _Proceedings of the 38th International Conference on Machine Learning_ , volume 139 of _Proceedings of Machine Learning Research_ , pages 10347–10357, 2021. 

- Fan Wang, Juyong Jiang, Chansung Park, Sunghun Kim, and Jing Tang. Kasa: Knowledge-aware singular-value adaptation of large language models. In _International Conference on Learning Representations_ , 2025a. 

- Hanqing Wang, Yixia Li, Shuo Wang, Guanhua Chen, and Yun Chen. MiLoRA: Harnessing minor singular components for parameter-efficient LLM finetuning. In _Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ , pages 4823–4836, Albuquerque, New Mexico, 2025b. Association for Computational Linguistics. doi: 10.18653/v1/2025.naacl-long.248. URL `https://aclanthology.org/2025. naacl-long.248/` . 

- Wenhui Wang, Furu Wei, Li Dong, Hao Cheng, Xiaodong Liu, Xia Song, and Jianfeng Gao. MiniLM: Deep self-attention distillation for task-agnostic compression of pre-trained transformers. In _Advances in Neural Information Processing Systems_ , volume 33, pages 5776–5788, 2020. 

- Xiao-Ming Wu, Bin Fan, Kang Liao, Jian-Jian Jiang, Runze Yang, Yihang Luo, Zhonghua Wu, Wei-Shi Zheng, and Chen Change Loy. Vlanext: Recipes for building strong vla models, 2026. URL `https: //arxiv.org/abs/2602.18532` . 

- Yandan Yang, Shuang Zeng, Tong Lin, Xinyuan Chang, Dekang Qi, Junjin Xiao, Haoyun Liu, Ronghan Chen, Yuzhi Chen, Dongjie Huo, Feng Xiong, Xing Wei, Zhiheng Ma, and Mu Xu. Abot-m0: Vla foundation model for robotic manipulation with action manifold learning, 2026. URL `https://arxiv.org/abs/2602. 11236` . 

- Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, et al. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 

- Dongshuo Yin, Leiyi Hu, Bin Li, Youqun Zhang, and Xue Yang. 5%>100%: Breaking performance shackles of full fine-tuning on visual recognition tasks. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 20071–20081, 2025. 

- Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-wam: Do world action models need test-time future imagination? _arXiv preprint arXiv:2603.16666_ , 2026. 

- Sergey Zagoruyko and Nikos Komodakis. Paying more attention to attention: Improving the performance of convolutional neural networks via attention transfer. In _International Conference on Learning Representations_ , 2017. 

- Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, Ya-Qin Zhang, Jiangmiao Pang, Jingjing Liu, Tai Wang, and Xianyuan Zhan. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model, 2025. URL `https://arxiv.org/abs/2510.10274` . 

- Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. _arXiv preprint arXiv:2504.0279_ , 2025. 

12 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 2165–2183, 2023. 

13 

## **A Technical Appendices and Supplementary Material** 

### **A.1 Statement for Use of LLMs** 

LLMs were only used to assist with language polishing in certain sections of this paper. 

### **A.2 Reproducibility Statement** 

We provide open-source code to reproduce all experiments. To facilitate reproducibility, we additionally include a minimal working example and environment setup instructions, enabling researchers to verify correctness and replicate our reported results with minimal effort. Code is available at `https://github.com/YuhuaJiang2002/CKT-WAM` . 

### **A.3 Impact Statement** 

This paper presents work whose goal is to advance the field of machine learning. We do not identify any specific impacts of this work that require particular emphasis here. 

### **A.4 Limitations and Future Work** 

A limitation of this work is that our study is currently focused on embodied control and WAM-toWAM transfer, and we do not explore whether the proposed context knowledge transfer mechanism can generalize to broader multimodal settings such as text modeling, visual question answering, or other non-robotic generative tasks. We view this as a scope choice rather than a fundamental restriction of the method, since the core design of CKT-WAM—compressing teacher-side intermediate representations into a compact transferable context and injecting it through a lightweight conditioning interface—is not inherently tied to robotics. An important direction for future work is therefore to investigate whether the same principle can serve as a general parameter-efficient transfer mechanism across heterogeneous foundation models in language-only and vision-language domains, especially in settings where full hidden-state alignment is costly or structurally mismatched. 

## **B More Experimental Results** 

### **B.1 Stage-wise Selection Patterns of Specialized Adapters** 

To further examine whether the routed specialized adapters learn meaningful functional roles, we analyze their selection patterns within a single long-horizon manipulation task, _cube catching_ . This task is naturally decomposed into four sequential stages: _drawer opening_ , _cube grasping_ , _cube placing_ , and _drawer closing_ . We randomly sample 120 episodes from this task and, for each stage, compute the average selection probability of each specialized adapter. 

As shown in Figure 4, the specialized adapters exhibit clear stage-dependent routing behavior even within the same task. Different stages concentrate probability mass on different small subsets of adapters, rather than relying on a fixed task-level activation pattern. Specifically, _drawer opening_ mainly activates Adapters 2 and 3, _cube grasping_ is dominated by Adapters 5 and 7, _cube placing_ concentrates on Adapters 5 and 1, and _drawer closing_ shifts the focus primarily to Adapters 6 and 4. Moreover, each stage mainly activates only one or two adapters, while the remaining adapters receive much lower probabilities. 

These results suggest that the routed specialized adapters do not behave as static modules assigned to the entire task. Instead, their activation changes dynamically with the current manipulation sub-stage, indicating fine-grained functional specialization within a single trajectory. The consistently sparse probability concentration also supports the effectiveness of our route-first sparse design, where only a small subset of experts is needed to capture the control demands of each stage. 

### **B.2 Experimental Settings** 

Table 5 summarizes the default experimental settings used throughout this work unless otherwise specified. Our setup follows a standard large-teacher/smaller-student knowledge transfer paradigm, 

14 


Figure 4: Stage-wise selection probabilities of specialized adapters in the _cube catching_ task. We sample 120 episodes and compute the average adapter selection probabilities for the four stages: _drawer opening_ , _cube grasping_ , _cube placing_ , and _drawer closing_ . Even within the same task, the dominant adapters vary substantially across stages, and each stage mainly activates only one or two experts. 

where a frozen DreamZero-14B teacher supervises a Cosmos-Policy-2B student. For transfer, we extract the hidden states from the intermediate teacher layer _ℓ_<sup>_∗_</sup> = 20 out of the 40-layer teacher, which provides a favorable trade-off between semantic richness and transferability. The compressed teacher context is computed once and reused by all downstream branches, which is also consistent with the efficiency-oriented design of our method. 

Unless otherwise stated, all experiments use the configuration in Table 5. In particular, the routing module uses _M_ = 8 branches with top- _k_ = 2 selection, while the CKT module adopts a bottleneck projection with _db_ = 512 and a shared query bank of size _K_ = 32. These choices provide a good balance between transfer capacity, routing flexibility, and computational efficiency in our experiments. 

### **B.3 Detailed Real-World Evaluation Setting** 

Our real-world evaluation is designed to test _long-horizon, multi-step manipulation_ rather than isolated one-step behaviors. In all tasks, the robot must complete a sequence of ordered subgoals under continuous visual feedback, and an episode is counted as successful only when all required stages are completed in the correct order. This setting is more challenging than standard short-horizon evaluation because an error in an early stage can propagate and prevent successful completion of the later ones. 

As shown in Figure 5, the **Clothes Folding** task is a representative long-horizon manipulation problem with three explicitly ordered stages. First, the robot removes distracting clothes from the workspace to expose the target garment and create a clean manipulation area. Second, it unfolds the target shirt from a partially entangled or crumpled configuration into a flatter state that is suitable for precise bimanual interaction. Third, it performs the final folding motion to produce a compact folded shirt. This task is challenging because it requires sequential planning across multiple stages, large pose changes of deformable objects, and stable execution over an extended action horizon. 

Figure 5 also illustrates the **Fruit Sorting** task. In this task, the robot must identify the target fruits, grasp them one by one, and place them onto the designated plates in sequence. The task is not a single pick-and-place action: after placing the first fruit, the policy must preserve the intermediate arrangement, re-orient to the second target, and complete the remaining placement without disturbing 

15 

Table 5: Default experimental settings used in our method unless otherwise specified. 

|**Category**|**Setting**|
|---|---|
|Student WAM|Cosmos-Policy-2B|
|Teacher WAM|DreamZero-14B|
|Teacher depth|40 layers|
|Teacher hidden states selection from layer|_ℓ_<sup>_∗_</sup>= 20|
|Precision|`bfloat16`|
|Hardware|8_×_NVIDIA A800 GPUs|
|Training mode|Distributed training|
|Optimizer|AdamW|
|AdamW_β_1_, β_2|_β_1 = 0_._9_, β_2 = 0_._95|
|Weight decay|0_._01|
|Learning-rate schedule|Linear Warmup and Cosine decay|
|Warmup steps|1k|
|Learning rate|3_×_10<sup>_−_4 </sup>for adapter modules|
|Bottleneck dimension_db_|512|
|Query bank size_Kg, Ks_<br>Attention heads|_Kg_ =_Ks_ = 32<br>16|
|Dropout|0.1|
|Teacher hidden states extraction<br>Number of specialized adapters_M_|Computed once and reused for all student’s timesteps<br>8|
|<br>Routing strategy|top-_k_ = 2|
|<br>Noise levelln(_σ_)_∼N_(_P_mean_, P_ <sup>2</sup><br>std<sup>)</sup>|_P_mean = 1_._39and_P_std = 1_._2|
|Video loss scaling factor_λ_vid|_λ_vid = 1|
|Load balancing loss scaling factor_λ_bal|_λ_bal = 0_._01|


previously placed objects. This requires sustained visual grounding and consistent progress across multiple dependent subgoals. 

Figure 6 shows the **Cube Catching** task. In this task, the robot must first localize the target cube, move the gripper to a suitable pre-grasp pose, establish a stable grasp, and then transport the cube to the designated target area. Although the manipulated object is rigid and smaller than a garment, the task still requires several dependent stages, including accurate perception, grasp alignment, secure lifting, and controlled release. The evaluation therefore tests whether the policy can reliably chain together multiple primitive skills into a complete manipulation sequence. 

The same figure further presents the **Unmanned Retail** task, where the robot interacts with a cluttered shelf containing multiple beverages. Given a target item request, the robot must visually identify the correct product, reach into the shelf without colliding with surrounding objects, grasp the target drink, and retrieve it from the shelf. In multi-item settings, this process is repeated sequentially for different requested beverages. This task is particularly challenging because it jointly requires category-level recognition, motion planning in clutter, stable grasping in constrained spaces, and successful completion of multiple ordered retrieval steps. 

### **B.4 Trainable Parameter Budget of the CKT Module** 

In this section we provide a detailed accounting of the parameters introduced by our sparse CKT module. All numbers correspond to the default recipe used in the main experiments: a DreamZero– 14B teacher WAM with hidden dimension _d_ tea=5120, a Cosmos-Policy–2B student WAM with hidden dimension _d_ stu=2048, bottleneck dimension _db_ =512, _K_ =32 learnable query tokens, _M_ =8 specialized experts, top- _k_ with _k_ =2, 8-head cross-attention inside each adapter, and a router gating hidden size of 512. Both the teacher and the student backbones are kept frozen throughout training; the _only_ trainable parameters live in the CKT module. 

**Single adapter.** Each adapter branch consists of a shared projection trunk ( `down_proj` / `up_proj` with GELU, LayerNorm and Dropout), a set of learnable query tokens, a multi-head cross-attention block, and a post-attention LayerNorm. Its parameter breakdown is given in Table 6. 

16 


Figure 5: Detailed real-world examples for **Clothes Folding** and **Fruit Sorting** . The left three columns show representative intermediate states of the clothes-folding task, while the right two columns show the fruit-sorting task. 


Figure 6: Detailed real-world examples for **Cube Catching** and **Unmanned Retail** . The left part shows representative snapshots of the cube task, and the right part shows the unmanned-retail task with target beverage selection from a cluttered shelf. 

Observation: the _Q/K/V_ and output projections of the cross-attention block alone account for _∼_ 16 _._ 8M parameters, i.e. roughly 82% of a single adapter’s budget. This is expected, since the compressor operates in the student’s feature space ( _d_ stu=2048) and uses four 2048 _×_ 2048 projection matrices. 

**Full ADAPTERBANK.** The bank is composed of one always-on generalized adapter, _M_ =8 specialized adapters that are sparsely activated by the router, and a small two-layer gating network. Its overall parameter count is summarized in Table 7. 

Specialized adapters account for roughly 88% of all trainable parameters (164 _._ 3M of 187 _._ 4M), whereas the router adds only 2 _._ 6M. Note that although the router selects only _k_ =2 specialized experts 

17 

Table 6: Parameter breakdown of a single adapter branch. Dimensions: _d_ tea=5120, _d_ stu=2048, _db_ =512, _K_ =32, cross-attention with 8 heads. 

|Module|Shape|Role|# Params|
|---|---|---|---|
|`down_proj`|Linear(5120_→_512)|teacher_→_bottleneck|2_,_621_,_952|
|`up_proj`|Linear(512_→_2048)|bottleneck_→_student|1_,_050_,_624|
|`layer_norm`|LayerNorm(2048)|post-MLP norm|4_,_096|
|`query_tokens`|(1_,_32_,_2048)|learnable queries|65_,_536|
|`cross_attn`|MHA(_d_=2048_, h_=8)|compression to_K_ tokens|16_,_785_,_408|
|`post_attn_norm`|LayerNorm(2048)|post-attn norm|4_,_096|
|**Single adapter total**|||**20**_,_**531**_,_**712**|


Table 7: Parameter breakdown of the full ADAPTERBANK used in our main LIBERO experiments. The router is a two-layer MLP (5120 _→_ 512 _→_ 8) plus a single learnable noise scalar. 

|Component|# Instances|# Params per inst.|# Params (total)|
|---|---|---|---|
|Generalized adapter|1|20_,_531_,_712|20_,_531_,_712|
|Specialized adapters|8|20_,_531_,_712|164_,_253_,_696|
|Dynamic router (5120_→_512_→_8, + noise)|1|2_,_626_,_057|2_,_626_,_057|
|**Total trainable (ADAPTERBANK)**|||**187**_,_**411**_,_**465**|
|_(i.e. ≈_187_._4_M trainable parameters)_||||


per instance, top- _k_ routing affects _output composition_ , not parameter count: all _M_ adapters store their own weights and are therefore included in the total. 

**Cost relative to the frozen backbones.** Table 8 situates the CKT budget against the two frozen WAMs. Even with the full _M_ =8 expert configuration, the overhead remains below 1 _._ 2% of the combined teacher–student backbone size, justifying our characterization of CKT module as parameter efficient. 

Table 8: CKT trainable parameter overhead relative to frozen WAM backbones. All percentages are with respect to the approximate parameter counts of Cosmos-Policy–2B (student) and DreamZero– 14B (teacher). 

|Frozen reference|Approx. size|CKT overhead|
|---|---|---|
|Cosmos-Policy–2B (student)|_∼_2_._0B|9_._37%|
|DreamZero–14B (teacher)|_∼_14_._0B|1_._34%|
|Teacher+Student (combined)|_∼_16_._0B|1_._17%|


**Scaling considerations.** Two architectural knobs dominate the CKT budget: (i) the number of specialized experts _M_ , which scales the bank _linearly_ and accounts for the 164 _._ 3M specializedadapter term; and (ii) the per-adapter cross-attention block, which accounts for _∼_ 82% of a single branch. Consequently: • Halving the number of specialized experts from _M_ = 8 to _M_ = 4 reduces the bank to _≈_ 105M trainable parameters; setting _M_ = 2 yields _≈_ 64M. 

- Further reductions can be obtained by lowering the number of attention heads or by sharing the cross-attention projection across experts, at a potential cost to expert specialization. 

- The bottleneck dimension _db_ and the number of query tokens _K_ have a comparatively minor effect ( _∼_ 3 _._ 6M per adapter combined), so they can be tuned freely without strongly affecting the overall budget. 

Unless stated otherwise, all ablations in the main paper share the default configuration reported here. 

18 

### **B.5 Details of Student-Side Context Injection** 

This appendix expands Sec. 3.4: we (i) specify exactly how the augmented conditioning sequence _E_<sup>˜</sup> _t_ enters the frozen student DiT, (ii) prove that the 3D rotary position encoding of every future-frame visual token is invariant to the injection, (iii) describe the forward-hook implementation used in our codebase, and (iv) contrast our cross-attention K/V injection with the alternative of splicing _CA_ into the visual self-attention stream. 

### **B.5.1 How** _E_<sup>˜</sup> _t_ **shapes future-frame visual tokens** 

Each block _ℓ ∈{_ 1 _, . . . , L_<sup>stu</sup> _}_ of the student DiT implements the standard “self-attention _→_ crossattention _→_ FFN” pattern, gated by an AdaLN modulation _e_<sup>(</sup><sup>_ℓ_)</sup> derived from the diffusion timestep _τ_ : 


where, importantly, our injection only modifies the K/V argument of the cross-attention in (14); all attention heads, projection matrices and AdaLN parameters remain frozen at their pretrained values. Expanding (14) per head _h ∈{_ 1 _, . . . , H_ a _}_ , the residual delivered to a future-frame patch _z_ ( _t,hp,wp_ ) is 


with the attention weights 


Two observations follow directly from (16)–(17): 

- (i) Information flow is strictly one-directional: _CA_ contributes keys and values but never queries, so the cost of the cross-attention is _O_ ( _Lv L d_<sup>˜stu</sup> ) rather than the _O_ ( _L_<sup>2</sup> _v_<sup>_d_stu) it would incur if</sup><sup>_CA_</sup> were spliced into the self-attention stream. 

- (ii) Each patch admits a personalized mixture of teacher tokens, indexed by its spatio-temporal coordinate; this is the mechanism by which a single observation-level _CA_ can deliver locationspecific cues to spatially distinct regions of the predicted future frames. 

### **B.5.2 Position-encoding invariance** 

The student’s visual tokens are equipped with a _factorized 3D rotary position encoding_ (3D RoPE) applied inside the self-attention of (13). For a patch at index ( _t, hp, wp_ ) and head dimension _dh_ , write 


where _ϕT , ϕH , ϕW_ are the temporal, height- and width-axis rotation phases, allocated to disjoint slices of the head dimension. The rotary basis is materialised as 


with _R_ ( _·_ ) the standard block-diagonal rotation matrix. 

**Proposition 1** (Position-encoding invariance under context injection) **.** _For every block ℓ, every patch index_ ( _t, hp, wp_ ) _∈_ [ _T_ ] _×_ [ _H_ ] _×_ [ _W_ ] _, every denoising step τ , and every choice of CA and ⟨_ SEP _⟩, the rotary basis of (19) applied to that patch is unchanged when Et is replaced by E_<sup>˜</sup> _t in the cross-attention. Equivalently, neither the temporal index t, nor the spatial indices_ ( _hp, wp_ ) _, nor the rotation matrices R_ (Φ( _t,hp,wp_ )) _depend on L_<sup>˜</sup> _._ 

19 

_Proof._ The proposition follows from three properties of the student backbone, as detailed in App. B.5.3. 

- (P1) _RoPE indexing is geometry-bound, not sequence-bound._ The phases _ϕT_ ( _t_ ) _, ϕH_ ( _hp_ ) _, ϕW_ ( _wp_ ) in (18) are computed by enumerating the patch grid ( _T, H, W_ ) alone; they do not depend on the conditioning length _L_<sup>˜</sup> or on any token in _E_<sup>˜</sup> _t_ . Hence Φ( _t,hp,wp_ ) is identical under _Et_ and _E_<sup>˜</sup> _t_ . 

- (P2) _RoPE is applied only inside visual self-attention._ In (13), the queries and keys of the selfattention come from _Z_<sup>(</sup><sup>_ℓ_)</sup> exclusively; _E_<sup>˜</sup> _t_ is not routed into self-attention. Therefore (19) is computed on tensors that are independent of _E_<sup>˜</sup> _t_ . 

- (P3) _Cross-attention applies no positional encoding on either side._ In (14), the cross-attention used by the student WAM applies no positional encoding to its queries (visual) or its keys and values (textual + transferred context). Consequently, the absolute position of _CA_ inside _E_<sup>˜</sup> _t_ , and the presence of _⟨_ SEP _⟩_ , contribute only through their value embeddings via (16)–(17) and not through any positional kernel. 

Combining (P1)–(P3) yields the proposition. 

**Corollary: order-invariance of the conditioning sequence.** By (P3), the cross-attention output in (14) is invariant under any permutation of the rows of _E_<sup>˜</sup> _t_ . The exact ordering chosen in (8) – _Et_ first, then _⟨_ SEP _⟩_ , then _CA_ – is therefore a stylistic choice and does not affect the network’s outputs at initialization or after training.<sup>1</sup> 

### **B.5.3 Implementation as a forward hook** 

Because the augmentation in (8) acts only on the output of the student’s text-projection module, it is implemented as a single non-intrusive forward hook on _gθ_ : 


registered before each forward pass and cleared afterwards. This means in particular that: 

- **No edits to the student source code.** The DiT module file is loaded verbatim from the pretrained checkpoint; the injection lives entirely in our pipeline wrapper. 

- **Trainable parameters are confined to the CKT module.** The hook returns a concatenation, which has no learnable parameters of its own (apart from the optional _⟨_ SEP _⟩_ token); gradients flow only through _CA_ back into the CKT adapter bank and router. 

- **Amortization across denoising steps.** The teacher and the CKT module are evaluated once per observation, the resulting _CA_ is cached on the wrapper, and every subsequent call of the student’s _gθ_ – one per denoising step per CFG branch – reads the same cached _CA_ . The marginal compute relative to the unaugmented student is one extra K/V projection over _L_<sup>˜</sup> _− Lt −_ 1 tokens per cross-attention layer. 

### **B.5.4 Why not splice** _CA_ **into the visual stream?** 

A natural alternative is to concatenate _CA_ with the visual tokens in the self-attention stream of (13) instead of with the conditioning tokens. We deliberately avoid this design for three reasons. 

1. **It breaks the rotary basis.** The 3D RoPE in (18)–(19) requires the visual sequence length to equal _THW_ exactly; appending _Kg_ + _Ks_ extra tokens to _Zτ_ violates this invariant. Restoring it would require ad-hoc positional indices for the spliced tokens, all of which interact with the pretrained rotary basis in unpredictable ways and were observed in preliminary experiments to destabilize denoising. 

2. **It blows up self-attention cost.** Self-attention is _O_ (( _Lv_ + 2 _K_ )<sup>2</sup> _d_<sup>stu</sup> ) instead of _O_ ( _L_<sup>2</sup> _v_<sup>_d_stu), and</sup> unlike cross-attention the cost cannot be hidden behind FlashAttention’s K/V-asymmetric kernel. 

1In practice we still keep a fixed ordering at training and evaluation so that the student’s K/V cache layout is deterministic. 

20 


Figure 7: Training curves of the proposed method. **Left:** optimization trajectories of the total loss, the averaged student EDM loss, and the last-step student EDM loss. **Right:** trajectory of the load-balancing loss _L_ bal. The balancing term decreases steadily throughout training, while the overall objective remains stable. 

3. **It conflates roles.** Self-attention is the student’s pretrained spatial-temporal mixer over visual content; pushing teacher tokens through this pathway would force them to behave as pseudopatches competing with future-frame patches for the same attention budget. Cross-attention, in contrast, is the student’s native conditioning pathway, and is exactly the role _CA_ is meant to play. 

The injection in (8) thus realizes the smallest possible interface change to the frozen student that still grants every future-frame visual token access to the teacher’s transferred knowledge, while preserving its pretrained geometry, attention budget, and inference amortization. 

### **B.6 Training Dynamics of the Balancing Objective** 

Figure 7 shows the training dynamics of the proposed objective. Recall that the final loss is defined as _L_ = _L_ CKT + _λ_ bal _L_ bal, where 


with _λ_ bal = 0 _._ 01. This term penalizes routing imbalance by encouraging the marginal routing probabilities and actual selection frequencies to be more uniformly distributed across adapters. 

Several observations can be made. First, the optimization remains stable throughout training. As shown in the left panel, both the total loss and the averaged student EDM loss drop rapidly in the early stage and then enter a stable plateau, indicating that the auxiliary balancing term does not destabilize the total loss. The last-step student EDM loss exhibits visibly larger variance, which is expected since it is measured from a single denoising step and is therefore more sensitive to minibatch variation and timestep-dependent difficulty. Importantly, despite such local fluctuations, its overall scale remains bounded and does not show progressive drift, suggesting that training is well behaved. 

Second, the balancing objective is consistently optimized and improves routing utilization over time. In the right panel, _L_ bal steadily decreases from roughly 1 _._ 12 at the beginning of training to about 1 _._ 02 near convergence. This trend indicates that adapter usage becomes increasingly balanced as training proceeds, rather than collapsing to a small subset of adapters. Notably, under perfectly balanced routing, one would have _Pm_ = 1 _/M_ and _fm_ = 1 _/M_ for all _m_ , which yields 


Therefore, the final value close to 1 _._ 0 suggests that the learned router approaches a near-uniform operating regime while still preserving enough flexibility for input-dependent specialization. 

Third, the gap between the total loss and the student EDM loss remains small and stable, which further indicates that the balancing regularizer acts as a mild auxiliary constraint rather than dominating optimization. This behavior is desirable: the model continues to reduce the primary generation error, while the routing structure is simultaneously regularized toward healthier adapter utilization. 

21 

Table 9: LIBERO simulation benchmark results. Success rates (SR, %) across four LIBERO benchmark task suites [Liu et al., 2023]. 

|Method|Spatial|Object|Goal|Long|Average|
|---|---|---|---|---|---|
|Diffusion Policy|78.3|92.5|68.3|50.5|72.4|
|Dita|97.4|94.8|93.2|83.6|92.3|
|_π_0|96.8|98.8|95.8|85.2|94.2|
|UniVLA|96.5|96.8|95.6|92.0|95.2|
|_π_0_._5|98.8|98.2|98.0|92.4|96.9|
|OpenVLA-OFT|97.6|98.4|97.9|94.5|97.1|
|CogVLA|98.6|98.8|96.6|95.4|97.4|
|Cosmos Policy|98.1|**100.0**|98.2|97.6|98.5|
|CKT-WAM (Ours)|**99.0**|99.8|**98.6**|**97.8**|**98.8**|


Taken together, these curves support that the proposed balancing formulation achieves its intended effect—it improves adapter allocation without introducing noticeable optimization conflict with the main training objective. 

Overall, Figure 7 provides empirical evidence that the load-balancing term is both _effective_ and _nondisruptive_ : it steadily mitigates routing imbalance, drives the routing statistics toward the balanced regime, and preserves stable optimization of the student objective throughout training. 

### **B.7 Results on LIBERO Benchmark** 

Table 9 reports the results on the standard LIBERO simulation benchmark. The student WAM is initialized from the official Cosmos-Policy-LIBERO-Predict2-2B checkpoint. CKT-WAM achieves the best overall performance, reaching an average success rate of 98.8%, which improves over the strongest prior baseline, Cosmos Policy, by 0.3 points. Although the benchmark is already highly saturated for top-performing methods, CKT-WAM still delivers consistent gains on three out of four suites, including Spatial, Goal, and Long, while remaining competitive on Object. In particular, the improvement on the Long suite suggests that the proposed cross-model knowledge transfer is especially beneficial for temporally extended manipulation tasks, where reliable action generation over longer horizons is more critical. Overall, these results show that CKT-WAM not only preserves the strong in-domain capabilities of modern VLA policies, but also provides a more effective policy representation that translates into stronger and more consistent performance across diverse manipulation scenarios. 

## **C Detailed Implementation of the Load Balancing Auxiliary Loss** 

To encourage balanced utilization of specialized adapters and avoid routing collapse, we introduce an auxiliary load-balancing objective following the standard practice in sparse mixture-of-experts (MoE) models. Without such a regularizer, the router may over-concentrate probability mass on a small subset of adapters, causing under-utilization of the remaining capacity and limiting the effectiveness of specialization. 

Let _pb,m_ denote the routing probability assigned to the _m_ -th adapter for the _b_ -th instance in a minibatch of size _B_ , where _m ∈{_ 1 _, . . . , M }_ and _M_ is the total number of specialized adapters. We first define the batch-averaged routing mass of adapter _m_ as 


which measures how much routing probability, on average, is allocated to adapter _m_ over the batch. 

Since our routing is implemented in a sparse top- _k_ manner, each instance activates only a small subset of adapters. For the _b_ -th instance, we denote by _Ib_ = Top-K( _{pb,m}m_<sup>_M_</sup> =1<sup>_, k_) the index set of the</sup><sup>_k_</sup> adapters with the largest routing probabilities. Based on this selection set, we define the empirical 

22 

top- _k_ selection frequency of adapter _m_ as 


where I _{·}_ is the indicator function. Intuitively, _fm_ reflects how often adapter _m_ is actually selected for execution, while _Pm_ captures how much routing probability mass it receives before hard top- _k_ selection. 

Following sparse MoE formulations, we define the load-balancing loss as 


This objective is minimized when routing mass and selection frequency are distributed more evenly across adapters. In other words, it discourages degenerate solutions in which a few adapters dominate both the router probabilities and the actual top- _k_ assignments. The multiplicative factor _M_ is introduced only for scale normalization, so that the magnitude of the auxiliary term remains stable as the number of adapters varies. The final training objective is 


where _L_ CKT is the main training objective and _λ_ bal controls the strength of the auxiliary regularization. In practice, this term improves adapter utilization and stabilizes specialization by preventing the router from collapsing to a narrow subset of experts, while still allowing different adapters to develop distinct functional roles. 

## **D Detailed Related Work** 

### **D.1 World Action Models** 

Early world-model research focused on learning compact latent dynamics for prediction, planning, and imagination-based control [Ha and Schmidhuber, 2018, Hafner et al., 2019, 2020, 2023]. 

Building upon these foundations, recent literature has formally established WAMs as a powerful alternative for embodied control, explicitly modeling how visual observations may evolve under action [Ye et al., 2026]. Within this rapidly evolving landscape, two dominant generative paradigms have emerged. The first is the _imagine-then-execute_ (or causal) approach, where models such as LingBot-VA [Li et al., 2026] and Vidar [Feng et al., 2025] first generate future visual trajectories and subsequently condition action prediction on these imagined futures. The second paradigm involves _joint modeling_ , where future video and action tokens are denoised together within a shared generative architecture, as demonstrated by Motus [Bi et al., 2025] and other unified frameworks [Zhu et al., 2025]. 

Standard VLA models, while successful in scaling reactive visual-motor policies [Brohan et al., 2023, Zitkovich et al., 2023, Kim et al., 2025b], largely rely on static image-text pretraining and lack this explicit physical dynamics modeling. However, the explicit video synthesis utilized by most WAMs incurs substantial test-time latency due to iterative denoising. To mitigate this efficiency bottleneck, parallel efforts such as VPP [Hu et al., 2024] and UVA [Li et al., 2025] have begun exploring ways to utilize predictive representations while reducing or entirely bypassing explicit video decoding during inference. 

Our work is complementary to these architectural advances. Instead of proposing a new monolithic WAM, we study how action-relevant dynamics knowledge can be efficiently transferred _between_ WAMs. In particular, CKT-WAM focuses on a practical teacher–student setting, where a stronger teacher WAM provides compact intermediate context to a more lightweight and efficient student WAM. 

### **D.2 Knowledge Transfer** 

Knowledge transfer in neural networks has evolved from output-space teacher–student learning [Hinton et al., 2015] to richer forms of intermediate supervision. FitNets introduced the idea of 

23 

transferring hidden-layer hints [Romero et al., 2015], while attention transfer showed that structured attention maps can serve as an effective transfer target [Zagoruyko and Komodakis, 2017]. In reinforcement learning, policy distillation demonstrated that action policies can be transferred from a teacher to a student network [Rusu et al., 2016]. For Transformer-based models, works such as TinyBERT further explored multi-level transfer over hidden states and attention patterns [Jiao et al., 2020]. 

Despite this progress, most prior transfer methods operate by matching teacher and student outputs, hidden representations, or attention statistics directly. Such formulations are often most natural when the teacher and student share closely aligned prediction spaces or architectures. By contrast, WAM-to-WAM knowledge transfer introduces additional challenges, since different models may use different latent parameterizations, token interfaces, or denoising backbones. 

CKT-WAM therefore adopts a different perspective. Rather than treating transfer as direct output imitation or full representation matching, we cast it as _contextual knowledge transfer_ : the teacher provides a compact set of transferable context tokens extracted from an intermediate block, and the student consumes these tokens through its native conditioning pathway. This design preserves architectural flexibility, reduces transfer overhead, and is naturally suited to heterogeneous teacher– student WAM pairs. 

### **D.3 Parameter Efficient Adapters** 

Parameter-efficient fine-tuning (PEFT) has emerged as a practical alternative to full fine-tuning when adapting large pretrained backbones to downstream tasks. A representative line is low-rank reparameterization, where LoRA models task-specific updates in a low-dimensional subspace with substantially reduced trainable parameters [Hu et al., 2022]. Building on this idea, recent spectral variants such as PiSSA and KaSA show that the choice of singular components and initialization can substantially affect optimization efficiency and knowledge preservation [Meng et al., 2024, Wang et al., 2025a]. Orthogonally, MoE-style PEFT methods further increase adaptation capacity through routed low-rank experts without reverting to full parameter updates, as exemplified by AdaMoLE and HydraLoRA [Liu and Luo, 2024, Tian et al., 2024]. In vision, however, effective adaptation depends not only on parameter count but also on whether the adapter design matches visual inductive biases: AdaptFormer demonstrates that lightweight bottleneck adapters can effectively adapt frozen vision transformers across image and video recognition tasks [Chen et al., 2022], ViT-Adapter injects task-relevant visual priors to make plain ViTs competitive for dense prediction [Chen et al., 2023], and the recent Mona argues that visual adaptation should move beyond NLP-style linear adapters by introducing multi-cognitive visual filters, showing that lightweight adapter tuning can even outperform full fine-tuning on several visual recognition benchmarks [Yin et al., 2025]. Our method is related to this line of work, but differs in emphasizing a structured parameter-efficient adaptation design tailored to balancing general knowledge retention and task-specific specialization. 

24 

## **NeurIPS Paper Checklist** 

1. **Claims** 

Question: Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope? 

Answer: [Yes] 

Justification: The main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope. 

Guidelines: 

   - The answer [NA] means that the abstract and introduction do not include the claims made in the paper. 

   - The abstract and/or introduction should clearly state the claims made, including the contributions made in the paper and important assumptions and limitations. A [No] or [NA] answer to this question will not be perceived well by the reviewers. 

   - The claims made should match theoretical and experimental results, and reflect how much the results can be expected to generalize to other settings. 

   - It is fine to include aspirational goals as motivation as long as it is clear that these goals are not attained by the paper. 

2. **Limitations** 

Question: Does the paper discuss the limitations of the work performed by the authors? Answer: [Yes] 

Justification: Limitations are discussed in the 5th section. 

Guidelines: 

   - The answer [NA] means that the paper has no limitation while the answer [No] means that the paper has limitations, but those are not discussed in the paper. 

   - The authors are encouraged to create a separate “Limitations” section in their paper. 

   - The paper should point out any strong assumptions and how robust the results are to violations of these assumptions (e.g., independence assumptions, noiseless settings, model well-specification, asymptotic approximations only holding locally). The authors should reflect on how these assumptions might be violated in practice and what the implications would be. 

   - The authors should reflect on the scope of the claims made, e.g., if the approach was only tested on a few datasets or with a few runs. In general, empirical results often depend on implicit assumptions, which should be articulated. 

   - The authors should reflect on the factors that influence the performance of the approach. For example, a facial recognition algorithm may perform poorly when image resolution is low or images are taken in low lighting. Or a speech-to-text system might not be used reliably to provide closed captions for online lectures because it fails to handle technical jargon. 

   - The authors should discuss the computational efficiency of the proposed algorithms and how they scale with dataset size. 

   - If applicable, the authors should discuss possible limitations of their approach to address problems of privacy and fairness. 

   - While the authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection, a worse outcome might be that reviewers discover limitations that aren’t acknowledged in the paper. The authors should use their best judgment and recognize that individual actions in favor of transparency play an important role in developing norms that preserve the integrity of the community. Reviewers will be specifically instructed to not penalize honesty concerning limitations. 

3. **Theory assumptions and proofs** 

Question: For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof? 

Answer: [Yes] 

25 

Justification: Appendix contains Proposition 1 and its corresponding formal proof regarding position-encoding invariance. 

Guidelines: 

- The answer [NA] means that the paper does not include theoretical results. 

- All the theorems, formulas, and proofs in the paper should be numbered and crossreferenced. 

- All assumptions should be clearly stated or referenced in the statement of any theorems. 

- The proofs can either appear in the main paper or the supplemental material, but if they appear in the supplemental material, the authors are encouraged to provide a short proof sketch to provide intuition. 

- Inversely, any informal proof provided in the core of the paper should be complemented by formal proofs provided in appendix or supplemental material. 

- Theorems and Lemmas that the proof relies upon should be properly referenced. 

### 4. **Experimental result reproducibility** 

Question: Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)? 

Answer: [Yes] 

Justification: All the information needed to reproduce the main experimental results of the paper is shown in the 3rd and 4th sections. 

Guidelines: 

- The answer [NA] means that the paper does not include experiments. 

- If the paper includes experiments, a [No] answer to this question will not be perceived well by the reviewers: Making the paper reproducible is important, regardless of whether the code and data are provided or not. 

- If the contribution is a dataset and/or model, the authors should describe the steps taken to make their results reproducible or verifiable. 

- Depending on the contribution, reproducibility can be accomplished in various ways. For example, if the contribution is a novel architecture, describing the architecture fully might suffice, or if the contribution is a specific model and empirical evaluation, it may be necessary to either make it possible for others to replicate the model with the same dataset, or provide access to the model. In general. releasing code and data is often one good way to accomplish this, but reproducibility can also be provided via detailed instructions for how to replicate the results, access to a hosted model (e.g., in the case of a large language model), releasing of a model checkpoint, or other means that are appropriate to the research performed. 

- While NeurIPS does not require releasing code, the conference does require all submissions to provide some reasonable avenue for reproducibility, which may depend on the nature of the contribution. For example 

- (a) If the contribution is primarily a new algorithm, the paper should make it clear how to reproduce that algorithm. 

- (b) If the contribution is primarily a new model architecture, the paper should describe the architecture clearly and fully. 

- (c) If the contribution is a new model (e.g., a large language model), then there should either be a way to access this model for reproducing the results or a way to reproduce the model (e.g., with an open-source dataset or instructions for how to construct the dataset). 

- (d) We recognize that reproducibility may be tricky in some cases, in which case authors are welcome to describe the particular way they provide for reproducibility. In the case of closed-source models, it may be that access to the model is limited in some way (e.g., to registered users), but it should be possible for other researchers to have some path to reproducing or verifying the results. 

### 5. **Open access to data and code** 

26 

Question: Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental material? 

Answer: [Yes] 

Justification: We provide open access to the data and code in the Reproducibility Statement Section 

Guidelines: 

   - The answer [NA] means that paper does not include experiments requiring code. 

   - Please see the NeurIPS code and data submission guidelines ( `https://neurips.cc/ public/guides/CodeSubmissionPolicy` ) for more details. 

   - While we encourage the release of code and data, we understand that this might not be possible, so [No] is an acceptable answer. Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark). 

   - The instructions should contain the exact command and environment needed to run to reproduce the results. See the NeurIPS code and data submission guidelines ( `https: //neurips.cc/public/guides/CodeSubmissionPolicy` ) for more details. 

   - The authors should provide instructions on data access and preparation, including how to access the raw data, preprocessed data, intermediate data, and generated data, etc. 

   - The authors should provide scripts to reproduce all experimental results for the new proposed method and baselines. If only a subset of experiments are reproducible, they should state which ones are omitted from the script and why. 

   - At submission time, to preserve anonymity, the authors should release anonymized versions (if applicable). 

   - Providing as much information as possible in supplemental material (appended to the paper) is recommended, but including URLs to data and code is permitted. 

6. **Experimental setting/details** 

Question: Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer) necessary to understand the results? 

Answer: [Yes] 

Justification: All the training and test details are shown in the Experiments section. 

Guidelines: 

   - The answer [NA] means that the paper does not include experiments. 

   - The experimental setting should be presented in the core of the paper to a level of detail that is necessary to appreciate the results and make sense of them. 

   - The full details can be provided either with the code, in appendix, or as supplemental material. 

7. **Experiment statistical significance** 

Question: Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments? 

Answer: [Yes] 

Justification: We report the number of trials in real-world experiments. 

Guidelines: 

- The answer [NA] means that the paper does not include experiments. 

- The authors should answer [Yes] if the results are accompanied by error bars, confidence intervals, or statistical significance tests, at least for the experiments that support the main claims of the paper. 

- The factors of variability that the error bars are capturing should be clearly stated (for example, train/test split, initialization, random drawing of some parameter, or overall run with given experimental conditions). 

- The method for calculating the error bars should be explained (closed form formula, call to a library function, bootstrap, etc.) 

27 

   - The assumptions made should be given (e.g., Normally distributed errors). 

   - It should be clear whether the error bar is the standard deviation or the standard error of the mean. 

   - It is OK to report 1-sigma error bars, but one should state it. The authors should preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis of Normality of errors is not verified. 

   - For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g., negative error rates). 

   - If error bars are reported in tables or plots, the authors should explain in the text how they were calculated and reference the corresponding figures or tables in the text. 

8. **Experiments compute resources** 

Question: For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments? 

Answer: [Yes] 

Justification: The paper provides sufficient information on the computer resources in the Experiments Section. 

Guidelines: 

   - The answer [NA] means that the paper does not include experiments. 

   - The paper should indicate the type of compute workers CPU or GPU, internal cluster, or cloud provider, including relevant memory and storage. 

   - The paper should provide the amount of compute required for each of the individual experimental runs as well as estimate the total compute. 

   - The paper should disclose whether the full research project required more compute than the experiments reported in the paper (e.g., preliminary or failed experiments that didn’t make it into the paper). 

9. **Code of ethics** 

Question: Does the research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics `https://neurips.cc/public/EthicsGuidelines` ? 

Answer: [Yes] 

Justification: The research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics. 

Guidelines: 

   - The answer [NA] means that the authors have not reviewed the NeurIPS Code of Ethics. 

   - If the authors answer [No] , they should explain the special circumstances that require a deviation from the Code of Ethics. 

   - The authors should make sure to preserve anonymity (e.g., if there is a special consideration due to laws or regulations in their jurisdiction). 

10. **Broader impacts** 

Question: Does the paper discuss both potential positive societal impacts and negative societal impacts of the work performed? 

Answer: [Yes] 

Justification: the paper discusses both potential positive societal impacts and negative societal impacts of the work performed. 

Guidelines: 

- The answer [NA] means that there is no societal impact of the work performed. 

- If the authors answer [NA] or [No] , they should explain why their work has no societal impact or why the paper does not address societal impact. 

28 

- Examples of negative societal impacts include potential malicious or unintended uses (e.g., disinformation, generating fake profiles, surveillance), fairness considerations (e.g., deployment of technologies that could make decisions that unfairly impact specific groups), privacy considerations, and security considerations. 

- The conference expects that many papers will be foundational research and not tied to particular applications, let alone deployments. However, if there is a direct path to any negative applications, the authors should point it out. For example, it is legitimate to point out that an improvement in the quality of generative models could be used to generate Deepfakes for disinformation. On the other hand, it is not needed to point out that a generic algorithm for optimizing neural networks could enable people to train models that generate Deepfakes faster. 

- The authors should consider possible harms that could arise when the technology is being used as intended and functioning correctly, harms that could arise when the technology is being used as intended but gives incorrect results, and harms following from (intentional or unintentional) misuse of the technology. 

- If there are negative societal impacts, the authors could also discuss possible mitigation strategies (e.g., gated release of models, providing defenses in addition to attacks, mechanisms for monitoring misuse, mechanisms to monitor how a system learns from feedback over time, improving the efficiency and accessibility of ML). 

### 11. **Safeguards** 

Question: Does the paper describe safeguards that have been put in place for responsible release of data or models that have a high risk for misuse (e.g., pre-trained language models, image generators, or scraped datasets)? 

Answer: [NA] 

Justification: the paper poses no such risks. 

Guidelines: 

- The answer [NA] means that the paper poses no such risks. 

- Released models that have a high risk for misuse or dual-use should be released with necessary safeguards to allow for controlled use of the model, for example by requiring that users adhere to usage guidelines or restrictions to access the model or implementing safety filters. 

- Datasets that have been scraped from the Internet could pose safety risks. The authors should describe how they avoided releasing unsafe images. 

- We recognize that providing effective safeguards is challenging, and many papers do not require this, but we encourage authors to take this into account and make a best faith effort. 

### 12. **Licenses for existing assets** 

Question: Are the creators or original owners of assets (e.g., code, data, models), used in the paper, properly credited and are the license and terms of use explicitly mentioned and properly respected? 

Answer: [Yes] 

Justification: the creators and original owners of assets are properly credited, and the license and terms of use are explicitly mentioned and are properly respected. 

Guidelines: 

- The answer [NA] means that the paper does not use existing assets. 

- The authors should cite the original paper that produced the code package or dataset. 

- The authors should state which version of the asset is used and, if possible, include a URL. 

- The name of the license (e.g., CC-BY 4.0) should be included for each asset. 

- For scraped data from a particular source (e.g., website), the copyright and terms of service of that source should be provided. 

29 

- If assets are released, the license, copyright information, and terms of use in the package should be provided. For popular datasets, `paperswithcode.com/datasets` has curated licenses for some datasets. Their licensing guide can help determine the license of a dataset. 

- For existing datasets that are re-packaged, both the original license and the license of the derived asset (if it has changed) should be provided. 

- If this information is not available online, the authors are encouraged to reach out to the asset’s creators. 

### 13. **New assets** 

Question: Are new assets introduced in the paper well documented and is the documentation provided alongside the assets? 

Answer: [Yes] 

Justification: Codes introduced in the paper are well documented in the anonymous code link. 

Guidelines: 

   - The answer [NA] means that the paper does not release new assets. 

   - Researchers should communicate the details of the dataset/code/model as part of their submissions via structured templates. This includes details about training, license, limitations, etc. 

   - The paper should discuss whether and how consent was obtained from people whose asset is used. 

   - At submission time, remember to anonymize your assets (if applicable). You can either create an anonymized URL or include an anonymized zip file. 

14. **Crowdsourcing and research with human subjects** 

Question: For crowdsourcing experiments and research with human subjects, does the paper include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)? 

Answer: [NA] 

Justification: the paper does not involve crowdsourcing nor research with human subjects. Guidelines: 

   - The answer [NA] means that the paper does not involve crowdsourcing nor research with human subjects. 

   - Including this information in the supplemental material is fine, but if the main contribution of the paper involves human subjects, then as much detail as possible should be included in the main paper. 

   - According to the NeurIPS Code of Ethics, workers involved in data collection, curation, or other labor should be paid at least the minimum wage in the country of the data collector. 

15. **Institutional review board (IRB) approvals or equivalent for research with human subjects** 

Question: Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained? 

Answer: [NA] 

Justification: the paper does not involve crowdsourcing nor research with human subjects. Guidelines: 

- The answer [NA] means that the paper does not involve crowdsourcing nor research with human subjects. 

- Depending on the country in which research is conducted, IRB approval (or equivalent) may be required for any human subjects research. If you obtained IRB approval, you should clearly state this in the paper. 

30 

   - We recognize that the procedures for this may vary significantly between institutions and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the guidelines for their institution. 

   - For initial submissions, do not include any information that would break anonymity (if applicable), such as the institution conducting the review. 

16. **Declaration of LLM usage** 

Question: Does the paper describe the usage of LLMs if it is an important, original, or non-standard component of the core methods in this research? Note that if the LLM is used only for writing, editing, or formatting purposes and does _not_ impact the core methodology, scientific rigor, or originality of the research, declaration is not required. 

Answer: [Yes] 

Justification: the paper describes the usage of LLMs in the appendix. 

Guidelines: 

- The answer [NA] means that the core method development in this research does not involve LLMs as any important, original, or non-standard components. 

- Please refer to our LLM policy in the NeurIPS handbook for what should or should not be described. 

31 

