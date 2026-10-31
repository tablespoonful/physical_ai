---
title: "EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference"
date: "2026-10-09"
authors: "Anxhelo Diko; Jieyu Lin; Stefano Ambrogio; Ziyun Li; Mahmoud Assran; Théo Moutakanni"
url: https://arxiv.org/abs/2610.14324
pdf: https://arxiv.org/pdf/2610.14324
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.14324)** / [論文ページ](https://arxiv.org/abs/2610.14324)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference** 

**Anxhelo Diko**<sup>1</sup><sup>_,∗_</sup> , **Jieyu Lin**<sup>1</sup><sup>_,∗_</sup> , **Stefano Ambrogio**<sup>1</sup> , **Ziyun Li**<sup>1</sup> , **Mahmoud Assran**<sup>2</sup> , **Théo Moutakanni**<sup>2</sup> , **Barbara De Salvo**<sup>1</sup> , **Chiao Liu**<sup>1</sup> 

> 1Meta Reality Labs Research, 2FAIR at Meta 

- _∗_ Equal contribution. 

Foundation models like V-JEPA are increasingly deployed across a heterogeneous edge–cloud continuum spanning smart glasses, phones, robots, and servers. Yet, they are typically trained as rigid, fixedcapacity networks bound to one device, supporting neither reconfigurable compute budgets nor collaborative execution. Existing approaches address only one axis at a time: slimmable and NASbased methods provide width elasticity but assume single-device inference, whereas split-computing methods enable cross-device collaboration only for fixed partitions and static capacities. We introduce Elastic V-JEPA (EV-JEPA), a single model trained once and deployable everywhere along the continuum. Its width is reconfigurable, and it is natively partitionable across heterogeneous devices. At its core is Transition-Aware Triplet Training (T3). At each step we pick a narrow and a wide width, and train three paths: each width alone, plus a hybrid path that runs the early layers narrow and the rest wide. The hybrid switch point is where one device hands off to another, so the same weights learn both single-device and cross-device execution. Across various benchmarks, EV-JEPA falls within 1 accuracy point of independently trained baselines while improving over previous elastic training approaches by up to 11 accuracy points. Narrow-to-wide cross-device hybrid execution recovers to within 1.1 points of the highest-capacity standalone model and supports many-to-one, any-to-any, and variable-split configurations. Finally, we show that the elastic principle extends beyond the backbone to an elastic token compression mechanism that exposes controllable trade-offs among on-device computation, latency, and accuracy. 

**Date:** October 16, 2026 


## **1 Introduction** 

Vision foundation models (VFMs) like V-JEPA [2] are a cornerstone of modern computer vision and AI, powering applications that range from classification [1; 2] to action anticipation and planning [1; 11]. Traditionally, these models are designed to run on powerful accelerators. However, the rise of wearable smart glasses [14] and robotics [32] is reshaping where such models must operate. Rather than relying on a centralized cloud, the deployment infrastructure is evolving into a distributed edge-cloud continuum [44; 13]. A heterogeneous, multi-tier architecture where edge devices (e.g. smart glasses and robots) with different compute budgets and remote servers cooperate to serve inference. Conventionally, such cooperation has involved edge devices streaming raw video to the cloud for processing, which is at odds with the need for smart glasses and robots to assist and act in the physical world in real time. Streaming is power-hungry and slow due to low-bandwidth wireless links the edge relies on [12], making transmission a primary bottleneck. These constraints motivate research on efficient VFMs [27; 21; 33; 26], promoting on-device compute. Yet, these approaches share two key limitations: i) they train a separate model per compute budget, and ii) they treat each device in isolation, so an edge device is capped at its own budget and the collaborative compute still relies on video streaming. 

To address i), one line of work makes a single network serve multiple compute budgets, whether by extracting sub-architectures from a supernetwork [4] or through variable widths [10; 42; 20]. These methods differ in how far elasticity reaches, from a single sublayer’s width [10] to the hidden dimension itself [42], but not in what they produce: a set of self-contained models (one per compute budget) whose representations are not cross-width compatible. They are intended to serve different individual devices, but not to split a single 

1 

inference across them. A separate line of work addresses ii) by splitting the network’s workload across multiple heterogeneous compute nodes [12]. While effective for exploiting distributed hardware, they assume a fixed partition and a static per-node capacity, forfeiting standalone execution and treating distributed inference as a requirement rather than an option. As a result, existing approaches either provide width elasticity or collaboration, but not both. The two failures interlock as elastic methods cannot carry a representation across widths, and split methods can serve only rigid architectures. This raises a fundamental question: can we train neural networks that are both elastic and collaborative, and be able to run fully on a single device and seamlessly split their computation across multiple ones when needed? 

To answer this question, we introduce a novel approach that achieves both width elasticity and collaborative execution instantiated on the self-supervised predictive V-JEPA [2] model named as **Elastic V-JEPA (EV-JEPA)** (Fig. 1). EV-JEPA builds on a vision transformer backbone and supports full-width elasticity across all layer components (Fig. 1 **Standalone Inference** ). In addition, beyond standalone width elasticity, we depart from previous works by introducing a _hybrid_ (mixed-width) execution mode in which early layers run at a smaller width and the remainder at a larger one, transitioning at a variable split layer. This allows a small device to initiate inference and a more capable one to complete it, thereby improving inference accuracy by streaming tokens rather than videos. However, it imposes a requirement that no elastic method has had to satisfy: representations that are cross-width compatible. 

At the core of our approach is a novel training paradigm we term Transition-Aware Triplet Training (T3). Unlike prior elastic approaches that optimize a randomly selected width [10] or rigid _{smallest, random, largest}_ triplet [38; 39], often resulting in performance degradation at intermediate capacities, T3 continuously samples a _{smaller, hybrid, larger}_ triplet. The same width pair is therefore optimized simultaneously as two standalone configurations, and as the endpoints of the hybrid path that connects them, so cross-width compatibility is trained directly as a native capability. Additionally, T3 builds on the same training frameworks as the original V-JEPA with one additional twist: the self-evolving EMA teacher is replaced with a fixed pretrained V-JEPA 2 [1] encoder to provide a stable target space across all widths. This means EV-JEPA is trained with a dense predictive objective where the student must estimate teacher representations per token, an objective significantly stricter than agreeing on a global representation (i.e., classification) [38; 10; 42], making elasticity even harder. To our knowledge, this is the first elastic framework proposed on a densely supervised model. Finally, to close the gap between a network that can be split in principle and one that runs efficiently over a device continuum connected through low-bandwidth links, we also experiment coupling hybrid execution with an elastic, controllable token-compression layer to ease the cross-device communication. 

We extensively evaluate our elastic-collaborative framework on video understanding benchmarks, including Something-Something V2 [17] and Kinetics-400 [23], as well as the predictive task of action anticipation on Epic-Kitchens 100 [9]. Our empirical results demonstrate that EV-JEPA trained with T3 achieves superior performance compared to other training regimes and also resolves the intermediate subnetwork degradation [42; 38]. In summary, our contributions are threefold. First, we introduce **EV-JEPA** , an elastic VFM whose width is reconfigurable across all layer components and that natively supports hybrid mixed-width execution. Second, we propose **T3** which optimizes a width pair simultaneously as two standalone configurations and as the endpoints of the hybrid path connecting them, making cross-width compatibility a trained property rather than an emergent one. Third, we show across multiple benchmarks that EV-JEPA stays within 1 accuracy point of independently trained standalone baselines while improving over prior elastic training by up to 11 accuracy points, and that narrow-to-wide hybrid execution recovers to within 1.1 accuracy points of the highest-capacity under different configurations. We further show that the elastic principle extends to a token compressor, reducing intermediate communication, transfers to vision-language understanding under VL-JEPA[6] setting, and applies to convolutional backbones to support deployment and partition across compact, low-memory devices. 

## **2 Related Works** 

**Elastic Networks.** A first family of approaches supporting heterogeneous deployment stems from one-shot NAS. OFA [4] and BigNAS [40] train large convolutional supernets that treat width, depth, kernel size, and resolution as elastic dimensions, from which specialized sub-architectures are extracted after training; subsequent works refine training and search procedures [18; 35]. While powerful, these methods frame elasticity as a search 

2 


**Figure 1 One elastic model for the device continuum.** We propose a single _elastic network_ that is trained once and deployed across the entire continuum: (1) its width is reconfigurable at inference time, allowing the same parameters to serve any compute budget **(Standalone Inference)** ; and (2) its computation can be _split_ between devices, with early layers executed on-device and remaining layers on a stronger device, communicating only compact intermediate representations **(Hybrid Inference)** . 

problem, and as the gap between the smallest and largest deployable configurations grows, the resulting search space expands combinatorially, making sub-architectures searching prohibitive. Slimmable approaches emerged as a complementary alternative that trades search for a fixed family of nested widths sharing weights. US-Net [39; 38] introduced this idea in the convolutional setting by jointly training a set of fixed widths with switchable batch normalization, the sandwich training rule, and in-place distillation, becoming the standard recipe for slimmable training. These ideas were later transferred to transformers, first by DynaBERT [20], which adapts both width and depth of BERT through a two-stage distillation procedure, and then to vision transformers (ViT) [19; 42], led by MatFormer [10], which applies the matryoshka principle [24] to FFN blocks, training a fixed set of nested dimensions by sampling one granularity per step under a tunable probability distribution. A third line of work bridges these two families by combining weight-sharing supernets with NAS-style search over transformer architectures [7; 8; 16]. Despite their progress, all of these methods share two limitations relevant to our setting: 1) degenerated performance in intermediate widths [5], and 2) networks are designed to run on isolated hardware. Our work directly addresses both, producing a single elastic model whose width is reconfigurable across all layer components and that natively supports hybrid mixed-width execution that splits compute from a smaller to a bigger device. 

**Split Computing.** A complementary line of work addresses distributed inference by partitioning a network across devices. Neurosurgeon [22] pioneered layer-granularity splitting between mobile and cloud, selecting the partition point at runtime based on network conditions and device load. SPINN [25] extended this idea by combining early-exit mechanisms with device-cloud splitting, co-optimizing both policies at runtime for latency-constrained settings. SplitNets [12] specifically targeted head-mounted systems, designing neural architectures for efficient distributed computation across wearable sensors and edge servers. While these methods demonstrate the value of collaborative execution, they operate on fixed architectures running only in distributed mode. Our work bridges these two lines by producing a single model that is both elastic and natively splits compute, trained end-to-end to support standalone and collaborative inference across heterogeneous devices. 

3 


**Figure 2 Elastic architecture and Transition-Aware Triplet Training (T3). (a)** Weight slicing. All width configurations share a single set of parameters: for a layer weight _W ∈_ R<sup>_w_max</sup><sup>_×w_max</sup> , a width- _w_ subnetwork uses the top-left slice _W_<sup>(</sup><sup>_w_)</sup> = _W_ [1: _w,_ 1: _w_ ], so all configurations are nested submatrices of the same _W_ . **(b)** T3 training. At each iteration we sample a width pair ( _ws, wl_ ) and a split layer _k_ , and jointly optimize three paths over the _same_ masked input: a **small** standalone encoder _Eθ_ ( _ws_ ), a **large** standalone encoder _Eθ_ ( _wl_ ), and a hybrid path that runs the first _k_ layers at _ws_ and transitions to _wl_ at layer _k_ via the elastic operator _Pws→wl_ . Each encoder feeds a predictor _Gθ_ together with a learned mask token **m** ; the three paths produc _L_ small, _L_ hybrid, and _L_ large, all regressed against targets from a frozen V-JEPA teacher _T_ on the unmasked video. The predictor width is set by a capped rule _wG_ = min( _wG_<sup>max</sup> _,_<sup><u>1</u></sup> 2<sup>_wE_)(Eq.9)</sup> and is therefore _not_ tied to the encoder width; the labels “Small”/“Large” denote which path a predictor serves, not its capacity. 

## **3 Method** 

### **3.1 Problem Formulation** 

We consider the setting of _elastic & distributed inference_ , where a model operates across multiple compute capacities and optionally distributes computation across devices. Let _fθ_ denote a model parameterized by _θ_ , and _L_ be the number of layers in the model. Instead of a fixed architecture, we assume the model supports a set of _width configurations w ∈W_ where _W_ is a predefined set of supported widths corresponding to different compute budgets (e.g., _W_ = _{_ 192 _,_ 384 _, . . . ,_ 1408 _}_ ). For a given width _w_ , we denote the corresponding subnetwork as: 


which represents the model executed entirely at width _w_ . Elastic inference requires that a single set of parameters _θ_ performs well across all configurations _w ∈W_ . In distributed deployments, inference may also be _split across devices_ . A resource-constrained device may execute an initial portion of the model using width _ws_ , after which the intermediate representation is transferred to a stronger device that continues computation using a larger width _wl_ , with _ws < wl_ . We therefore define a _hybrid configuration_ 


where the first _k_ layers operate with width _ws_ and the remaining _L − k_ layers operate with width _wl_ . The goal of our training framework is therefore twofold. First, the model should achieve strong performance across all standalone configurations _fθ_<sup>(</sup><sup>_w_)</sup> , enabling deployment on devices with different compute budgets. Second, the model should support _distributed execution_ , where computation can be distributed across devices. 

### **3.2 Elastic Transformer Architecture** 

We design a transformer architecture whose hidden dimension can vary across a predefined set of widths _W_ . Each width configuration corresponds to a subnetwork obtained by selecting the first _w_ channels of the model parameters. Concretely, following slimmable networks [39] and Matformer [10], the parameters of the largest model with width _w_ max are shared across all configurations through weight slicing. Consider a transformer 

4 

layer with attention projections _WQ, WK, WV ∈_ R<sup>_w_max</sup><sup>_×w_max</sup> . As shown in Fig. 2 (a), a smaller configuration with _w < w_ max uses the sliced parameters: 


The same principle applies to the feed-forward network. Given the full FFN parameters _W_ 1 _∈_ R<sup>_rw_max</sup><sup>_×w_max</sup> and _W_ 2 _∈_ R<sup>_w_max</sup><sup>_×rw_max</sup> , with _r_ being the upscaling factor, a width- _w_ uses the slices: 


This nested parameterization allows all subnetworks to reuse a single set of weights while maintaining architectural compatibility across widths. The supported _W_ form a discrete set due to the constraint that the hidden dimension must remain divisible by the attention head size. 

For hybrid configuration where smaller earlier layers are connect to larger later layers, the architecture supports width transitions between layers. When computation transitions from width _ws_ to a larger width _wl_ at layer _k_ , the intermediate representation _h_<sup>(</sup> _k_<sup>_ws_)</sup> _∈_ R<sup>_ws_</sup> is expanded to R<sup>_wl_</sup> through a learned linear projection _P_ . The operator is itself elastic: we maintain a single matrix _P ∈_ R<sup>_w_max</sup><sup>_×w_max</sup> , and for any transition ( _ws, wl_ ) we use the slice: 


so that _h_<sup>(</sup> _k_<sup>_wl_)</sup> = _Pws→wl_ ( _h_<sup>(</sup><sup>_ws_)</sup> ). This nested parameterization mirrors the slicing scheme of the transformer blocks where a single set of projection parameters is shared across all ( _ws, wl_ ) pairs. The same _P_ is further reused across all possible split layers _k ∈{_ 2 _, . . . , L}_ , making the operator invariant to where the transition occurs. This design yields a single compact transition module shared across the entire elastic configuration space and split layers _k_ . 

### **3.3 Transition-Aware Triplet Training** 

Our architecture introduces a capability absent from prior elastic methods: _hybrid execution_ , where computation transitions from width _ws_ to a larger width _wl_ at a split layer _k_<sup>1</sup> . This capability is orthogonal to standalone elasticity. Our objective is therefore to train a single model that performs well both at any standalone width _w ∈W_ and across hybrid configurations ( _ws, wl, k_ ). We formalize this by extending the configuration space. Traditional elastic training optimizes standalone subnetworks sampled from the width set _W_ : 


In contrast, our formulation expands the configuration space to include hybrid executions, 

_C_ = _W ∪{_ ( _ws, wl, k_ ) : _ws, wl ∈W, ws < wl, k ∈{_ 2 _, . . . , L −_ 1 _}},_ 

and optimizes configurations drawn from this joint space: 


In this formulation, hybrid execution _fθ_<sup>(</sup><sup>_ws,wl,k_)</sup> is treated as a first-class configuration rather than as an emergent property of training. This naturally allows existing sampling strategies to be extended to the hybrid setting. We consider two such extensions as baselines: 

• **Distributional sampling (Matformer-style)** [10]: a configuration _c ∼ p_ ( _C_ ) is sampled independently at each iteration. While this provides wide coverage of the configuration space, configurations are optimized independently. 

> 1Note that this capability is different from mix and match from Matformer[10]. Mix and match works because the input and output dims remain unchanged in the original Matformer. 

5 

- **Sandwich rule (US-Net-style)** [38]: the smallest and largest widths are optimized together with one random configuration _c_ rand _∼ p_ ( _C_ ) per iteration. This provides strong supervision at the boundaries of the elastic space, but intermediate widths _w_ (i.e, _w_ min _< w < w_ max) now compete with hybrid configurations for the same sampling slot. 

As a more suitable strategy for the joint standalone and hybrid objective, we propose **Transition-Aware Triplet Training (T3)** . At each iteration, we sample: 


and optimize the triplet: 


which mirrors the three deployment modes: standalone small, hybrid execution, and standalone large. T3 differs from the extended baselines in one key respect: the same width pair ( _ws, wl_ ) appears simultaneously as standalone configurations and as the endpoints of a hybrid path within the same iteration. This couples the three configurations through **shared gradients** , directly optimizing both standalone performance and cross-width compatibility, rather than relying on these to emerge from independent sampling. 

### **3.4 Training** 

We train the elastic model under a V-JEPA-style masked latent prediction objective [1; 2]. V-JEPA follows an encoder–predictor regime in which a student model observes a masked video and predicts latent representations for the masked regions from the visible context using the predictor and a learned mask token **m**<sup>2</sup> . In our setting, we retain this predictive training structure but replace the original teacher mechanism with distillation from a frozen pretrained V-JEPA model. Concretely, the student receives a masked input video, predicts latent embeddings for the masked tokens, and is optimized to match target representations produced by the frozen teacher on the corresponding full video. 

Given an input video _v_ , it is first split into a sequence of spatio-temporal tokens _X_ = _{x_ 1 _, . . . , xN }_ . A subset of tokens is masked according to the multi-block masking strategy introduced in V-JEPA [2]. Specifically, we sample spatially contiguous blocks and extend them across the full temporal extent of the clip, producing tubelet masks whose union defines the masked index set _M ⊂{_ 1 _, . . . , N }_ and its complement _V ⊂{_ 1 _, . . . , N } \ M_ indexes the visible (unmasked) tokens. For an index set _V_ we write _XV_ = _{xi}i∈V_ . _XV_ are passed to the student encoder _Eθ_ , while the predictor _Gθ_ predicts latent representations for the masked positions _i ∈M_ . This training setup is shared across all configurations _c ∈C_ . In particular, the same ( _X, M_ ) pair is used for all configurations in a T3 triplet so that standalone and hybrid paths are exposed to the same predictive task. 

_Student._ The student is our parametrized learnable model _fθ_ , a composition of our learnable modules including the encoder _Eθ_ and the predictor _Gθ_ , both built on the elastic transformer architecture according to the weight-sharing policy defined in Section 3.2. A sampled configuration _c ∈C_ determines how the encoder is executed. A standalone configuration is specified by a single width _w ∈W_ , with all encoder layers run at width _w_ . A hybrid configuration is specified by a tuple ( _ws, wl, k_ ), where the first _k_ encoder layers run at width _ws_ and the remaining _L − k_ layers run at width _wl_ . In both cases, we write _wE_ ( _c_ ) for the encoder output width, where _wE_ ( _c_ ) = _w_ for standalone configurations and _wE_ ( _c_ ) = _wl_ for hybrid configurations. Then, the predictor’s elastic width is derived from the _wE_ ( _c_ ) by the following rule: 


so the predictor tracks half the encoder width up to a cap _wG_<sup>max</sup> . The cap _wG_<sup>max</sup> = 384 matches the predictor width of the original V-JEPA [1; 2] while the half-width rule scales the predictor _below_ this reference for smaller encoders, deliberately limiting predictor capacity so that the encoder is forced to carry the representational load. Once the widths are defined, for a sampled configuration _c ∈C_ , the student prediction for a masked token _i ∈ M_ is: 


> 2Check the appendix for more V-JEPA details 

6 

**Table 1 Elastic Model Setup.** In the default setting, every smaller width transitions to the largest width in its range, i.e., _w → w_ max _, ∀ w ∈W\{w_ max _}_ . The total number of configurations is _|C|_ = _|W|_ + ( _|W| −_ 1) _· K_ , where _K_ is the number of candidate split layers. Reported values correspond to _K_ =1. 

|Model|_W_|Hybrid|_L_|Params Range|(M)<br>_|C|_|
|---|---|---|---|---|---|
|EV-JEPA-B|_W_1 :_{_192_,_384_,_768_,_1024_}_|_w→_1024|12|5.6–152.6|7|
|EV-JEPA-L|_W_2 :_{_192_,_384_,_768_,_1024_,_1280_}_|_w→_1280|12|5.6–238.0|9|
|EV-JEPA-H|_W_3 :_{_192_,_384_,_768_,_1024_,_1280_,_1408_}_|_w→_1408|14|6.5–335.5|11|


where _W_ proj<sup>(</sup><sup>_wE_(</sup><sup>_c_)</sup><sup>_→wG_(</sup><sup>_c_))</sup> is an elastic linear projection that maps the encoder output to _wG_ ( _c_ ), and **m** _∈_ R<sup>_wG_(</sup><sup>_c_)</sup> is the learned mask token inserted at the masked positions _i ∈ M_ . Both _W_ proj and **m** are sliced under the same weight-sharing policy as Section 3.2, so the predictor input is fully defined at width _wG_ ( _c_ ) for every configuration _c_ . 

**Teacher.** Target representations are produced by a frozen, pretrained V-JEPA 2 ViT-G teacher [1], denoted _T_ . Unlike the original V-JEPA formulation, where the teacher is updated via an exponential moving average (EMA) of the student, we keep _T_ fixed throughout training. An EMA teacher is ill-suited to the elastic setting: since the student is sampled at a different configuration _c ∈C_ at each iteration, an EMA target would average parameters across configurations of varying capacity, yielding an unstable and width-dependent learning signal. A frozen full-capacity teacher instead provides a stable target shared across all configurations, anchoring every subnetwork to the same representation space. Exploring EMA-style updates in the elastic regime is beyond the scope of this work. Given the full (unmasked) input, the teacher produces target embeddings 


for the masked positions. Because the teacher operates at a fixed hidden dimension that differs in general from the student’s configuration-dependent output dimension, we align student and teacher representations through a lightweight learned elastic head _hϕ_ applied to the student predictions. For notational simplicity, we fold _hϕ_ into _zS,i_<sup>(</sup><sup>_c_)inwhatfollows.</sup> 

**Loss.** Following V-JEPA, we use an _ℓ_ 1 regression loss on the masked tokens: 


This objective is applied to each of the configurations in the triplet _TT_ 3 = _{fθ_<sup>(</sup><sup>_ws_)</sup> _, fθ_<sup>(</sup><sup>_ws,wl,k_)</sup> _, fθ_<sup>(</sup><sup>_wl_)</sup> _}_ , giving _L_ small = _L_ ( _ws_ ) _, L_ hybrid = _L_ (( _ws, wl, k_ )) _, L_ large = _L_ ( _wl_ ) _,_ (13) 

and the total training loss is optimized jointly per iteration: 


Since the teacher _T_ is frozen, all three configurations are regressed toward a single consistent target, which stabilizes elastic training and prevents divergence between subnetworks observed under distributional sampling (Section 3.3). 

## **4 Experiments** 

### **4.1 Experimental Setup** 

_Data and teacher._ We pretrain all elastic backbones using the masked latent prediction objective described in Section 3.4. The pretraining set is the union of unlabeled videos proposed in V-JEPA [2], including Something-Something V2 (SSv2) [17] Kinetics-710 (K710) [23], and HowTo100M [28]. Each input clip contains 16 frames sampled at 4 FPS and resized to 256 _×_ 256. Videos are tokenized with 16 _×_ 16 _×_ 2 tubelets, 

7 

so each token spans a 16 _×_ 16 spatial patch over two consecutive frames. Masking follows the long-range spatiotemporal strategy of V-JEPA [2]: we sample two spatial block masks with scale up to 70% and extend them across the full temporal duration of the clip. Target representations are produced by a frozen V-JEPA 2 ViT-G teacher that receives the same input clip as the student but unmasked. 

**Model configurations.** All elastic models instantiate the same elastic transformer architecture of Section 3.2, with a fixed attention-head dimension of 64 and an MLP expansion ratio of 4 _×_ . As summarized in Table 1, we train three EV-JEPA model families. EV-JEPA-B is our base model, with set widths _W_ 1 ranging from 192 to 1024, 12 layers, and 5.6M–152.6M parameters. EV-JEPA-L uses the same 12-layer depth using the set of widths _W_ 2 with maximum width of 1280, covering approximately 5.6M–238M parameters. EV-JEPA-H is our largest configuration, with set of widths _W_ 3 ranging from 192 to 1408, 14 layers, and approximately 6.5M–335.5M parameters. LayerNorm parameters are shared across widths, and no width-specific normalization is used. Hybrid configurations employ the shared elastic projection **P** , sliced according to the source and destination widths. Unless otherwise noted, hybrid execution uses the middle split layer, i.e., layer 6 for 12-layer models. In our default many-to-one setting (i.e., the hybrid setting only supports going from smaller widths to _wmax_ ) with a single fixed split point, the configuration set contains _|W|_ standalone configurations and _|W| −_ 1 hybrid paths into the largest width (i.e. _|C|_ = _|W|_ + ( _|W| −_ 1)). More generally, with _K_ candidate split points, the number of configurations is _|C|_ = _|W|_ + ( _|W| −_ 1) _K_ . 

**Training strategies.** We compare four training strategies. The _standalone_ baseline trains a separate fixed-width model for each width; each standalone model is trained for the same number of epochs and with the same per-model compute capacity as the elastic models. The three elastic variants, _MatFormer-style EV-JEPA_ , _US-Net-style EV-JEPA_ , and our proposed _T3 EV-JEPA_ , share the same architecture, teacher, data, masking, optimizer, and configuration set. They differ only in how configurations are selected during pretraining, as formalized in Section 3.3. 

**Optimization.** All EV-JEPA models are pretrained with 300 epochs and AdamW ( _β_ 1 = 0 _._ 9, _β_ 2 = 0 _._ 999) in bf16 precision on 128 GPUs (16 nodes _×_ 8), with a constant weight decay of 0 _._ 04. The learning rate follows a three-phase schedule: a linear warmup from 1 _×_ 10<sup>_−_4</sup> to the peak, a constant phase at the peak, and a half-period cosine anneal toward a final learning rate of 5 _×_ 10<sup>_−_5</sup> . Following V-JEPA, the cosine period is stretched by a factor of 1 _._ 25 relative to the training length, so training stops before the anneal completes and the final learning rate remains above. Schedule lengths and peak learning rates differ by student family. See Table 2 for the detailed training configurations for each student family. Inputs are 16-frame clips at 256 _×_ 256 sampled at 4 fps, drawn from a mixture of Kinetics-710, Something-Something v2 and HowTo100M with sampling weights 0 _._ 335 _/_ 0 _._ 100 _/_ 0 _._ 565. 

|Student|Layers|_wmax_<br>Warm/|Cons|t/Decay<br>Peak LR|Clip|Batch|/GPU|
|---|---|---|---|---|---|---|---|
|EV-JEPA-B/L|12|1024/1280<br>40|/ 200|/ 60<br>5_._25_×_10<sup>_−_4</sup>|0_._025||24|
|EV-JEPA-H|14|1408<br>40|/ 200|/ 60<br>5_._25_×_10<sup>_−_4</sup>|0_._025||24|
|CNN|20|384<br>20|/ 80 /|200<br>3_×_10<sup>_−_3</sup>|0_._025||12|


**Table 2** Optimization schedules by student family. All runs decay to a final learning rate of 5 _×_ 10<sup>_−_5</sup> . 

### **4.2 Elastic Training and Range Scaling on SSv2** 

We begin our evaluation on SSv2, a benchmark whose temporal sensitivity requires combining spatial recognition with fine-grained motion reasoning, making it a rigorous testbed for elastic representations that must remain useful across widely different capacities. Three questions guide our analysis. First, under a controlled setting in which all methods share the configurations, how does T3 compare to MatFormer- and US-Net-style training? Second, does this behavior remain stable as the elasticity scales from EV-JEPA-B ( _W_ 1) to EV-JEPA-L ( _W_ 2) and EV-JEPA-H ( _W_ 3)? Third, does the hybrid inference help smaller models recover performance when transitioning to _wmax_ ? 

Figure 3(a) **<u>Standalone</u>** row reports the controlled comparison on EV-JEPA-B for the set of widths _W_ 1 and addresses our first question. Notably, MatFormer-style training trails the other regimes by a wide margin, suggesting that sampling a single configuration and having isolated parameter updates in each step produces unstable performance across configurations. US-Net-style sandwich training mitigates this by supervising the boundary widths at every iteration, ensuring that all shared parameters receive a gradient signal at each step. 

8 


**Figure 3 SSv2 standalone and hybrid inference across increasing elastic ranges.** Columns correspond to a) EV-JEPA-B ( _W_ 1), b) EV-JEPA-L ( _W_ 2), and c) EV-JEPA-H ( _W_ 3). The top row reports standalone elastic inference as a function of model parameters. The bottom row reports many-to-one hybrid execution _w → w_ max, where the first half of the encoder runs at source width _w_ , and the remaining layers run at _wmax_ . In the bottom row, _T3 EV-JEPA w_ and _T3 EV-JEPA w_ max are shown as _w_ -only and full-width T3 references, respectively, to measure hybrid recovery. 

However, it comes at the cost of configurations between the two endpoints degrading. T3 avoids both failure modes. By coupling a small path ( _f_<sup>_ws_</sup> ), a larger path ( _f_<sup>_wl_</sup> )<sup>3</sup> , and its hybrid transition ( _f_<sup>(</sup><sup>_ws,wl,k_)</sup> ) within the same iteration, every parameter is supervised at every step, and intermediate widths are explicitly drawn into the gradient. As a result, T3 tracks the independently trained baseline references most closely across the range. 

Having established US-Net as the strongest competing baseline, we use it as the main benchmark in Figures 3 b) and 3 c), which extend the elastic range to _W_ 2 with EV-JEPA-L and _W_ 3 with EV-JEPA-H. The trend is clear, T3 stays close to the references throughout, whereas US-Net progressively worsens at intermediate widths, with the gap reaching up to 11 accuracy points in EV-JEPA-H. Endpoint supervision alone is therefore increasingly insufficient as the range grows. T3, in contrast, drops the fixed-boundary anchoring and provides a stable optimization signal across the entire range. 

The **Hybrid** row of Figure 3 addresses our third question. Because hybrid accuracy is upper-bounded by the destination width _w_ max, two criteria are relevant: whether T3 outperforms US-Net-style training, and whether a low-width model can be compatible with a high-capacity continuation to recover the performance gap with the _wmax_ standalone model. To make this recovery explicit, we plot two T3 references alongside the hybrid curve: the standalone _w_ -only execution as a lower bound and the standalone _w_ max execution as an upper bound. The vertical distance from the _w_ -only curve to the hybrid curve thus quantifies the accuracy gained by continuing computation at _w_ max, while the distance from the hybrid curve to the _w_ max reference captures the residual loss relative to executing the _wmax_ model end-to-end. Across all three ranges, T3 hybrid execution recovers nearly _wmax_ -level accuracy even with source widths as small as _w_ = 192. Particularly, EV-JEPA-H ( _w_ = 192) model gains over 10 accuracy points when continued to _w_ max and falls within 1 point of the standalone _wmax_ model, with analogous trends in EV-JEPA-B and EV-JEPA-L. Cross-width compatibility is therefore preserved across different ranges, validating T3 as a principled training regime for 

> 3Note, for this specific experiment settings, _wl_ = _wmax_ . 

9 


**Figure 4 Standalone and hybrid inference on K400 for action recognition and EK100 for action anticipation.** _Standalone_ panels (1st, 3rd) report elastic inference as a function of model parameters. _Hybrid_ panels (2nd, 4th) report hybrid execution _w → w_ max, where the first half of the encoder runs at source width _w_ , and the remaining layers continue at _w_ max. 

distributed inference. 

### **4.3 Evaluation on Recognition (K400) and Action Anticipation (EK100)** 

Having analyzed elastic and hybrid behavior on SSv2, we now ask whether similar conclusions transfer to settings with a different discriminative structure. K400 is appearance- and scene-biased, stressing spatial– semantic capacity, while EK100 moves from recognition to _action anticipation_ . For action anticipation, we use frozen pretrained elastic predictor (following equation 9 convention) for evaluation. Following the analysis in Section 4.2, we retain US-Net as the strongest competing elastic baseline, and we report all results on the full-range EV-JEPA-H model ( _W_ 3, _w_ max = 1408). K400 is evaluated with Top-1 accuracy and EK100 with mean Top-5 recall (recall@5), the standard action-anticipation metric [15; 11]. 

_Standalone._ The standalone panels of Fig. 4 (1st, 3rd) show that on both K400 and EK100, T3 tracks the independently trained references across the full width range, whereas US-Net degrades at intermediate widths, with the gap reaching up to 5 accuracy points on K400 and 5 recall@5 points on EK100. 

_Hybrid._ The hybrid panels (2nd, 4th) report many-to-one execution _w → w_ max, with the T3 _w_ -only and _w_ max standalone curves plotted as lower and upper bounds. On both benchmarks, continuing a small-width encoder at _w_ max recovers most of the gap to the standalone _w_ max model. Even at source width _w_ = 192, hybrid execution gains +9.8 Top-1 points on K400 and +12.6 recall@5 points on EK100, falling within 1 point(s) of the full-width reference, while consistently outperforming US-Net-style hybrid execution. Crosswidth compatibility, therefore, holds for appearance-biased recognition and for egocentric anticipation alike, supporting T3 as a general training regime for distributed inference rather than one tuned to a single benchmark. 

### **4.4 Any-to-Any Hybrid Execution** 

The hybrid experiments so far adopt the many-to-one setting ( _w → w_ max), our default throughout the paper. Here we verify the more general claim that computation can transition from _any_ source width to _any_ larger destination width. Because the any-to-any configuration set is more expensive to train than the many-to-one default, we conduct this study on the smallest and largest ranges, _W_ 1 = _{_ 192 _,_ 384 _,_ 768 _,_ 1024 _}_ and _W_ 3 = _{_ 192 _,_ 384 _,_ 768 _,_ 1024 _,_ 1280 _,_ 1408 _}_ , with a single mid-network split ( _k_ = 6 for the 12-layer model _W_ 1 and _k_ = 7 for the 14-layer model _W_ 3). Figure 5 reports SSv2 Top-1 for every valid source–destination pair ( _ws, wl_ ) with _ws < wl_ . Note that the upscaling projection layer _Pws→wl_ is the same for each configuration, as in the many-to-one approach. 

Two observations emerge. First, the any-to-any T3 model retains strong standalone quality across the full width range, its standalone accuracy closely tracks both the independently trained baselines and the many-to-one T3 elastic network (Fig. 5 **left** ), incurring only a small trade-off of less than 1 point relative to the many-to-one model (in some configurations the any-to-any performs better than the many-to-one) as the price of supporting the larger any-to-any configuration space. Second, hybrid accuracy is governed primarily by the destination width _wl_ (similar to the many-to-one T3 model). For _wl_ =1024, all sources fall within 

10 


**Figure 5 SSv2 any-to-any hybrid inference.** In the any-to-any setting, a model executing at any source width _ws_ can upscale at _any_ larger width _wl > ws_ . On the **Hybrid Inference** plots, each curve fixes a destination _wl_ and sweeps the source _ws_ . The star and dotted line mark the standalone accuracy of that destination width. Across all pairs, hybrid execution recovers close to each destination’s standalone accuracy, even at _ws_ =192, which is within _∼_ 1 point of the standalone largest width. Accuracy is therefore governed by the destination (continuation) width, confirming that a small device can pair with any larger device at minimal loss. 


**Figure 6 Exit point, source width, and elastic token compression trade-offs. (left)** SSv2 Top-1 for hybrid execution as a function of the exit layer _k_ , for source widths _w∈{_ 192 _,_ 384 _,_ 768 _}_ and target width _wl_ = 1024. **(middle)** SSv2 Top-1 versus _k_ for the single path 192 _→_ 1024 under different elastic compression ratios. **(right)** Transmission latency at each compression ratio over a theoretical 1 Mbps BLE link, computed as the transmitted payload divided by link bandwidth. 

0 _._ 9 points of one another and within 1 _._ 1 points of the standalone _w_ =1024 reference (73 _._ 4), including the smallest source _ws_ =192 at 72 _._ 3. On the other hand, for _wl_ =1408 ( _W_ 3), all sources fall within 0 _._ 3 points of one another and within 0 _._ 65 points of the standalone _w_ =1408 reference (74 _._ 96). Together, these confirm that a small originating device can hand off to an arbitrarily larger continuation device and recover near-destination accuracy, extending the many-to-one result of Section 4.2 to the full any-to-any setting at negligible standalone cost in some configuration. 

### **4.5 Variable Exit Points and Elastic Token Compression** 

_Variable splitting layer k._ The hybrid experiments so far have relied on a fixed exit point _k_ , placing the transition at the middle of the network. The architecture, however, does not constrain us to a single split layer: because the same projection _P_ is reused for every _k_ (Section 3.3), supporting multiple exit points adds no parameters. We therefore conduct a variable- _k_ experiment on our _W_ 1 configurations, with widths ranging from 192 to 1024 and exit points _k ∈{_ 4 _,_ 6 _,_ 8 _}_ in a 12-layer network. Figure 6 ( _left_ ) reports SSv2 Top-1 as a function of the exit layer for three hybrid paths _w →_ 1024 with _w ∈{_ 192 _,_ 384 _,_ 768 _}_ ; each curve fixes the source width and sweeps _k_ . Two effects are visible. First, accuracy decreases monotonically with _k_ for every source width: a later exit leaves fewer layers to the larger continuation width _wl_ , whereas an earlier handoff leaves more of the network at _wl_ and recovers more of its standalone accuracy. Second, how much a late exit costs is governed by the source width. At the earliest exit ( _k_ =4) the three paths are nearly indistinguishable, within 0 _._ 43 points of one another, so even the narrowest _w_ =192 source reaches essentially the accuracy of a 4 _×_ wider one; by _k_ =8 the curves fan out and the _w_ =192 path degrades the most, falling 2 _._ 0 points below _w_ = 768. On-device capacity and on-device depth are therefore substitutable: the earlier 

11 

the handoff, the less the source width matters. This exposes the exit point as a deployment knob, while the policy that selects an operating point is application-specific and outside our scope. The compressor is trained in a separate post-training stage with all remaining network elements frozen, using an _ℓ_ 1 reconstruction loss shown in figure 7. 


**Figure 7 Elastic token compression for hybrid execution.** A learned compressor is inserted at the exit point _k_ of the source device. The ’compress module’ compresses the intermediate representation before transmission, reducing the number of tokens; the ’decompress module’ reconstructs the token grid on the target device, after which the shared elastic projection _Pws→wl_ upscales to _wl_ , and the remaining _L − k_ layers execute. During training, all modules except the compress–decompress pair remain frozen. 

_Elastic token compression._ Hybrid execution assumes the transmission of an intermediate representation from the source device to the continuation device, where the communication of a large amount of data can incur high latency and high power consumption. To reduce transmitted data, we attach a learned compressor at the exit of the source device, realized as a single encoder-decoder 3D convolution (more details in the appendix). The encoder runs as one additional layer and the decoder reconstructs the representation on the destination device before the remaining _L − k_ layers execute. The compressor reduces the number of transmitted tokens. Following the nested weight-sharing scheme of Section 3.2, compression is made elastic by slicing the convolution kernel along its spatiotemporal dimension, 


where the input and output channel dimensions are fixed at _C_ in = _C_ out = _ws_ , and the sliced ( _κt, κh, κw_ ) and strides set the spatiotemporal downsampling factor and hence the number of retained tokens. A single set of kernel weights thus spans the entire range of compression ratios, so one on-device layer can adjust compression elastically at inference time in the same way the backbone adjusts width. 

_Compressor configuration._ We instantiate the compressor on EV-JEPA-B ( _W_ 1 = _{_ 192 _,_ 384 _,_ 768 _,_ 1024 _}_ , _L_ = 12) for the hybrid configuration _fθ_<sup>(</sup><sup>_ws,wl,k_)</sup> with source width _ws_ = 192, destination width _wl_ = _w_ max = 1024 at a given split-layer _k_ , so the compressor sits exactly where the source device hands off to the continuation device. Up to layer _k_ the encoder _Eθ_ runs at _ws_ , so the quantity to be transmitted is the intermediate representation _h_<sup>(</sup> _k_<sup>_ws_)</sup> _∈_ R<sup>_N×ws_</sup> . For a 16-frame 256 _×_ 256 clip tokenized with 16 _×_ 16 _×_ 2 tubelets, this is _N_ = _T × H × W_ = 8 _×_ 16 _×_ 16 = 2048 tokens of width _ws_ = 192. The _compress_ module reshapes these _N_ tokens back into a _ws × T × H × W_ volume and applies a single strided 3D convolution with the sliced kernel _K_<sup>(</sup><sup>_κ_)</sup> of Eq. 15, followed by GroupNorm (8 groups) and GELU. The sliced extent ( _κt, κh, κw_ ), together with the matching stride ( _σt, σh, σw_ ) and per-axis padding _p_ = _⌊_ ( _κ − σ_ ) _/_ 2 _⌋_ , fixes the retained grid 

12 

**Table 3** Per-ratio configurations of the elastic encoder–decoder for an input grid of 8 _×_ 16 _×_ 16 = 2048 tokens. Kernel, stride, and padding are given as (time, height, width). _τ_ = _N/N_<sup>_′_</sup> is the token-reduction factor set by the sliced kernel (Eq. 15), and _ρ_ is the resulting payload compression ratio relative to raw RGB (Eq. 18), which is the quantity reported in Fig. 6. 

|_τ_|Kernel|Stride|Padding|Latent grid (_T _<sup>_′_</sup>_×H_<sup>_′_</sup>_×W _<sup>_′_</sup>)|/ tokens<br>_ρ_|
|---|---|---|---|---|---|
|8_×_|(4_,_4_,_4)|(2_,_2_,_2)|(1_,_1_,_1)|4_×_8_×_8 / 256|64_×_|
|16_×_|<br>(6_,_4_,_4)|<br>(4_,_2_,_2)|<br>(1_,_1_,_1)|2_×_8_×_8 / 128|128_×_|
|32_×_|(4_,_6_,_6)|(2_,_4_,_4)|(1_,_1_,_1)|4_×_4_×_4 / 64|256_×_|
|64_×_|(6_,_6_,_6)|(4_,_4_,_4)|(1_,_1_,_1)|2_×_4_×_4 / 32|512_×_|


_N_<sup>_′_</sup> = _T_<sup>_′_</sup> _× H_<sup>_′_</sup> _× W_<sup>_′_</sup> and hence the token-reduction factor _τ_ = _N/N_<sup>_′_</sup> , while the channel dimension/width is kept to _C_ out = _ws_ = 192. The _N_<sup>_′_</sup> tokens of width _ws_ are what crosses the link, giving the payload _P_ comp of Eq. 18. The _decompress_ module mirrors this on the continuation device: a 3 _×_ 3 _×_ 3 convolution with GroupNorm and GELU, a strided 3D transposed convolution with GroupNorm and GELU that restores the original _T × H × W_ grid at width _ws_ , and a LayerNorm over the channel dimension. The reconstructed tokens _h_ ˆ<sup>(</sup> _k_<sup>_ws_)</sup> then enter the same shared elastic projection _Pws→wl_ = _P_ [1: _wl,_ 1: _ws_ ] of Sec. 3.2 (here _P_ 192 _→_ 1024), after which the remaining _L − k_ layers execute at _wl_ , exactly as in uncompressed hybrid execution (Fig. 7). Elasticity follows the same nested weight-sharing policy as the backbone: the strided convolution and the transposed convolution each store a single 6 _×_ 6 _×_ 6 kernel _K_ , and every token-reduction factor _τ_ selects the leading sub-kernel _K_<sup>(</sup><sup>_κ_(</sup><sup>_τ_))</sup> via Eq. 15. One set of kernel weights therefore spans the whole range, so _τ_ becomes an inference-time knob in the same sense as the standalone width _w_ , the hybrid pair ( _ws, wl_ ), and the split layer _k_ . Table 3 lists ( _κ, σ, p_ ), the retained grid _N_<sup>_′_</sup> , and the corresponding payload ratio _ρ_ = 8 _τ_ for each configuration. 

_Compressor training._ The compressor is trained in a second, post-training stage on top of a T3-pretrained EV-JEPA-B (stage 1), with every other module frozen, so the elastic encoder behaves exactly as during pretraining and the reported numbers isolate the cost of compression alone. Writing _θ_ for the frozen pretrained parameters, the reference path is the uncompressed hybrid configuration _fθ_<sup>(</sup><sup>_ws,wl,k_)</sup> and the trained path is the same configuration with the compress–decompress pair inserted at layer _k_ , denoted _fθ_<sup>(</sup><sup>_ws,wl,k,τ_)</sup> at token-reduction factor _τ_ ; only the compressor parameters receive gradients. Two things differ from Sec. 3.4. First, this stage operates on unmasked clips: there is no masked index set _M_ , no mask token **m** , and no predictor _Gθ_ , so supervision is applied at the encoder output over _all N_ tokens rather than over _M_ alone. Second, the objective is the _ℓ_ 1 regression of Eq. 12 _regularized_ by a reconstruction term at the split layer, which anchors the transmitted representation itself rather than only its downstream effect. Concretely, let _h_<sup>(</sup> _k_<sup>_ws_)</sup> _∈_ R<sup>_N×ws_</sup> denote the source tokens at split layer _k_ and _h_<sup>ˆ(</sup> _kτ_<sup>_ws_)</sup> _∈_ R<sup>_N×ws_</sup> denote their reconstruction after compress–decompress at factor _τ_ , and let _z_<sup>_τ_</sup> and _z_ denote the layer-normalized final encoder features of the compressed and uncompressed (frozen model from pretraining or stage 1) paths on an unmasked clip _x_ . For a single _τ_ , 


and the stage optimizes the mean over the set of token-reduction factors _R_ = _{_ 8 _,_ 16 _,_ 32 _,_ 64 _}_ (equivalently _ρ ∈{_ 64 _×,_ 128 _×,_ 256 _×,_ 512 _×}_ ): 


At every iteration the trained path is run once at each _τ ∈R_ and the gradients are summed before a single optimizer step. This mirrors the T3 principle of Sec. 3.3 one level down: rather than sampling one ratio per step, all ratios are supervised jointly, so the shared kernel _K_ is optimized for every compression level at once and no ratio is left to compete for a sampling slot. Optimization: 100 epochs of 300 iterations with a global batch of 4096 clips drawn from the same pretraining corpus (K710, SSv2, and HowTo100M, sampling 

13 

weights 0 _._ 335 _/_ 0 _._ 100 _/_ 0 _._ 565) in bf16, AdamW with weight decay 0 _._ 04, a 10-epoch linear warmup from 10<sup>_−_4</sup> to 5 _._ 25 _×_ 10<sup>_−_4</sup> and cosine decay to 5 _×_ 10<sup>_−_5</sup> . 

_Accuracy under compression._ Figure 6 ( _middle_ ) isolates a single hybrid path, _ws_ =192 _→ wl_ =1024, and sweeps the same exit points _k ∈{_ 4 _,_ 6 _,_ 8 _}_ at four compression ratios — 64 _×_ , 128 _×_ , 256 _×_ , and 512 _×_ — with the uncompressed hybrid path plotted as the _No-Compression_ reference. Two observations follow. First, the ordering with respect to _k_ is preserved at every ratio: all curves decrease with a later exit and none cross, so the exit point and the compression ratio behave as two independent knobs rather than interacting ones. Second, accuracy decreases monotonically with the compression ratio, and the degradation is graceful at the low end: at 64 _×_ the compressed path tracks the No-Compression curve within 0 _._ 7 Top-1 points, and only at 512 _×_ does the penalty grow to 5 _._ 1 points. 

_Payload and trade-off._ We define compression relative to transmitting the input as raw 8-bit RGB, the worst case for an always-on sensor without a hardware video codec. For an intermediate representation of _N_ tokens reduced to _N_<sup>_′_</sup> tokens of dimension _ws_ , the transmitted payload is _P_ comp = _N_<sup>_′_</sup> _· ws · b_ bits, and the compression ratio is _ρ_ =<sup>_P_RGB</sup> _, P_ RGB = _F · H · W ·_ 3 _·_ 8 _,_ (18) _P_ comp 

with _F_ , _H_ , _W_ the clip length and frame resolution and _b_ = 8 the bits per transmitted element. The elastic token reduction reaches up to 512 _×_ payload reduction relative to raw RGB. All reported accuracies are end-toend, measured after the decoder reconstructs the token grid and the continuation layers run, so they reflect the true cost of compressing the transmitted representation. Together, the exit point and the compression ratio form two orthogonal knobs that expose a controllable trade-off among on-device computation, transmission latency, and accuracy. Regarding the compression network, it is trained in a separate post-training stage with all the remaining network elements frozen using an L1 reconstuction loss. 

### **4.6 Comparison With SOTA** 

**Table 4** Comparison with state-of-the-art models for action recognition on SSv2 and K400. **Bold** marks the best result per column, <u>underline</u> the second best. Avg. is the mean of SSv2 and K400. 

||_Motion_|_Appearance_||
|---|---|---|---|
|Method<br>Param.|SSv2|K400|Avg.|
|_Image encoders Evaluated Using Same Protocol_||||
|DINOv2 [30]<br>1.1B|50_._7|83_._6|67_._2|
|PEcoreG [3]<br>1.9B|55_._4|88.5|72_._0|
|SigLIP2 [34]<br>1.2B|49_._9|87_._3|68_._6|
|_Video encoders Evaluated Using Same Protocol_||||
|VideoMAEv2 [36]<br>1.0B|56_._1|82_._8|69_._5|
|InternVideo2-1B [37]<br>1.0B|67_._3|87_._9|77_._6|
|VideoPrism [43]<br>1.0B|68_._5|87_._6|78_._0|
|InternVideo2s2-1B [37]<br>1.0B|69_._7|**89.4**|79_._6|
|V-JEPA 2 ViT-L [1]<br>300M|73_._7|85_._1|79_._4|
|V-JEPA 2 ViT-H [1]<br>600M|74_._0|85_._3|79.7|
|V-JEPA 2 ViT-G [1]<br>1.0B|75.3|86_._6|**81.0**|
|_Distilled from V-JEPA 2 ViT-G_||||
|_Non-Elastic_ Baseline (_w_=1408)<br>335M|75_._0|85_._5|80_._3|
|**EV-JEPA-H** (_w_=1408)<br>335M|**75.4**|86_._5|**81.0**|


Table 4 compares EV-JEPA-H at full width ( _w_ =1408) against state-of-the-art image and video foundation models on SSv2 (motion) and K400 (appearance), all evaluated under the same attentive-probe protocol. Because EV-JEPA-H is distilled from a frozen V-JEPA 2 ViT-g teacher, this is not a like-for-like comparison against models trained from scratch, and we therefore include a _Non-Elastic_ Baseline distilled under identical teacher, data, masking, and compute budget. This control isolates the accuracy cost of elasticity from the effect of distillation, which is a quantity of interest. 

14 

**Table 5** Action anticipation on EK100. **Bold** marks the best result per column. Frozen-backbone rows attach an anticipation head to a frozen encoder. 

||_Action _|_anticipatio_|_n (EK100)_|
|---|---|---|---|
|Method<br>Param.|Verb|Noun|Action|
|InAViT [31]<br>160M|51_._9|52_._0|25_._8|
|Video-LLaMA [41]<br>7.0B|52_._9|52_._0|26_._0|
|PlausiVL [29]<br>8.0B|55_._6|54_._2|27_._6|
|_Frozen backbone_||||
|V-JEPA 2 ViT-L<br>300M|57_._8|53_._8|32_._7|
|V-JEPA 2 ViT-H<br>600M|59_._2|54_._6|36_._5|
|V-JEPA 2 ViT-g<br>1.0B|**61.2**|**55.7**|**38.0**|
|_Frozen backbone Distilled from V-JEPA 2 ViT_|_-g_|||
|_Non-Elastic_ Baseline (_w_=1408)<br>335M|58_._0|53_._2|34_._1|
|**EV-JEPA-H** (_w_=1408)<br>335M|58_._2|53_._2|34_._6|


Read this way, three results stand out. First, elasticity is obtained at no measurable accuracy cost. EV-JEPAH matches the _Non-Elastic_ Baseline across the board (75.4 vs. 75.0 on SSv2, 86.5 vs. 85.5 on K400, 81.0 vs. 80.3 average), despite the same weights additionally serving every smaller width and every cross-device hybrid configuration. We do not read the small margin in our favour as evidence that elasticity _improves_ full-width accuracy, though it is consistent with the multi-configuration objective of T3 acting as a regulariser. Second, this operating point is competitive with fixed-capacity specialists: EV-JEPA-H attains the best SSv2 accuracy (75.4), edging its own ViT-g teacher (75.3, 1.0B) at roughly 3 _×_ fewer parameters, and far surpassing appearance-biased image encoders such as PEcoreG (55.4) and DINOv2 (50.7) on this motion-centric benchmark. On the SSv2/K400 average it reaches 81.0, matching V-JEPA 2 ViT-g while exceeding ViT-L (79.4, 300M) and ViT-H (79.7, 600M). Third, on the appearance-dominated K400, EV-JEPA-H (86.5) falls within 0.1 points of ViT-g and is competitive with the strongest video encoders, though encoders trained on larger labelled corpora (e.g. InternVideo2s2, 89.4) remain ahead, consistent with the motion-versus-appearance trade-off inherent to the V-JEPA objective. 

On action anticipation (EK100, Table 5), EV-JEPA-H at full width reaches 34.6 action recall@5, again matching the _Non-Elastic_ Baseline distilled under identical conditions (34.1). Elasticity is therefore free on anticipation as well as on recognition. This also clarifies how to read the remaining gap to the frozen V-JEPA 2 ViT-H backbone (36.5): it is a capacity effect rather than a cost of our training regime, since a fixed-width model at the same 335M parameters and the same teacher lands below EV-JEPA-H. Relative to the broader literature, EV-JEPA-H outperforms recent 7–8B video–language models (PlausiVL, 27.6, and Video-LLaMA, 26.0) by roughly seven points at a fraction of their size, and sits between the frozen ViT-L (32.7) and ViT-H (36.5) backbones at only 335M parameters. Crucially, these numbers are the full-width operating point of a _single elastic_ model, not a separately trained specialist. The same weights that place EV-JEPA-H at or above the state of the art at _w_ =1408 also serve every smaller width and cross-device hybrid configuration. EV-JEPA thus matches fixed-capacity state-of-the-art models at its high end while additionally offering the reconfigurable compute and collaborative execution that none of these baselines provide. 

### **4.7 Vision-Language Transfer with VL-JEPA** 

Sections 4.2 and 4.3 probe the visual representation directly through task-specific heads. We now ask whether the same elastic encoder also transfers to vision-language understanding, where the representation must align with language rather than a discriminative head. We adopt VL-JEPA [6], a joint-embedding vision-language model that predicts continuous text embeddings, and replace its frozen V-JEPA 2 ViT-L vision encoder with our frozen EV-JEPA-H encoder, training only the connector and predictor. Following VL-JEPA, we report Top-1 accuracy on SSv2 open-vocabulary classification. 

As shown in Table 6, in standalone inference, the full-width configuration ( _w_ =1408) matches and slightly exceeds the VL-JEPA ViT-L baseline, while reducing to _w_ =1024 stays within one point at only 179M parameters, about 60% of the ViT-L encoder. In hybrid cross-device execution, where the early layers 

15 

**Table 6** Vision–language transfer on SSv2 (Top-1, open-vocabulary classification) under the VL-JEPA framework. All elastic rows use a single frozen EVJEPA-H encoder. 

**Table 7** Elasticity beyond Transformers. SSv2 Top-1 for a slimmable factorized 3D-CNN with a lightweight linear-attention layer. A single nested model serves all standalone widths and their cross-width hybrids. 

|Configuration|Param.|SSv2|
|---|---|---|
|V-JEPA 2 ViT-L [6]|300M|73_._2|
|_Standalone_|||
|_w_=1408|335M|**73.6**|
|_w_=1024|179M|72_._2|
|_Hybrid_|||
|384_→_1408|203M|72_._9|
|192_→_1408|194M|72_._6|


|Configuration|Param.|GFLOPs|SSv2|
|---|---|---|---|
|_Standalone_||||
|_w_=128|2.3M|11|56_._0|
|_w_=192|4.1M|20|58_._6|
|_w_=256|6.4M|30|60_._7|
|_w_=384|12.2M|57|**63.5**|
|_Hybrid_||||
|128_→_384|11.7M|50|63_._2|
|192_→_384|11.8M|51|63_._2|
|256_→_384|12.0M|53|63_._4|


run at a small source width and the remaining layers continue at _w_ max so that only compact intermediate features are transmitted, the 384 _→_ 1408 and 192 _→_ 1408 configurations reach within one point of the baseline while activating only 194M–203M parameters. A single frozen EV-JEPA encoder therefore extends both its standalone width-elasticity and its cross-device hybrid capability from recognition and anticipation to vision-language tasks, confirming that elasticity and language alignment compose without a per-budget encoder. 

### **4.8 Elasticity Beyond Transformers: Convolutional Backbones** 

The transition-aware training behind EV-JEPA is not specific to the Transformer. We distill the ViT-g teacher into a slimmable factorized 3D-CNN, augmented with a single lightweight linear-attention layer for global context. The CNN channel widths are sliced under the same weight-sharing policy (Section 3.2), so smaller subnets are strict channel slices of the largest and one set of weights serves every width. We use channels-first LayerNorm so that a single set of statistics-free normalizers stays valid across widths. Trained with the same T3 regime (Section 3.3), a single nested CNN scales monotonically on SSv2 (Table 7): from 56.0 at _w_ =128 (2.3M parameters, 11 GFLOPs), to 63.5 at _w_ =384 (12.2M, 57 GFLOPs). This extends EV-JEPA’s elasticity to the low-cost, low-memory regime most relevant to always-on, on-device deployment, confirming that transition-aware triplet training yields a single reconfigurable, partitionable model for convolutional backbones as well. 

## **5 Limitations** 

EV-JEPA offers a practical solution for deploying models across heterogeneous inference infrastructures, both for standalone execution and for cross-device collaboration. However, it comes with three limitations that are worth noting. First, EV-JEPA is tied to a teacher, as training requires a pretrained V-JEPA model to provide the target space. Whether the stability that a frozen teacher provides across widths (Section 3.4) can be recovered without an external teacher, for instance, through an EMA scheme adapted to the elastic regime, is left to future work. Second, our elasticity is confined to width. The depth _L_ is fixed for every standalone configuration, including the smallest, so the narrowest subnetwork still pays the full sequential cost of _L_ layers. Extending T3 to depth is not immediate, since the split layer _k_ that defines a hybrid path is itself indexed by depth. Third, T3 operates over a fixed set of widths, and the cost of training grows with that set. Supporting a broader range of devices, therefore, increases training time. Future work will address these specific problems to make EV-JEPA and the next generation of T3 even more practical in real-world scenarios. 

## **6 Conclusions** 

We introduced EV-JEPA, a single self-supervised video model that is at once width-elastic and natively partitionable across a heterogeneous edge-cloud continuum. Its core enabler is Transition-Aware Triplet 

16 

Training (T3), which at every step optimizes a width pair both as two standalone configurations and as the endpoints of the hybrid path connecting them, making cross-width compatibility a trained property rather than an emergent one, and doing so under a dense predictive objective for the first time. A single trained model spans a wide capacity range: across SSv2, K400, and EK100 action anticipation, T3 stays within 1 accuracy points of independently trained standalone baselines and improves over prior elastic training by up to 11 points of at intermediate widths, while resolving the intermediate-subnetwork degradation of earlier approaches. Beyond standalone use, hybrid cross-device execution lets a small on-device encoder be completed at full width on a stronger device, recovering to within 1.1 points of the highest-capacity standalone model from an on-device _w_ =192 model, and supporting many-to-one, any-to-any, and variable-split configurations. At full width, the same model matches or exceeds fixed-capacity state-of-the-art encoders (75.4 SSv2, 81.0 average) at roughly a third of their parameters. Finally, the elastic principle extends beyond the backbone: to an elastic token compressor that cuts transmitted payload by up to 512 _×_ , to vision-language transfer under VL-JEPA, and to convolutional architectures. Together, these results show that a single model, trained once, can serve the entire device continuum with reconfigurable compute and collaborative execution, rather than a family of rigid, per-device networks. 

## **References** 

- [1] M. Assran, A. Bardes, D. Fan, Q. Garrido, R. Howes, M. Muckley, A. Rizvi, C. Roberts, K. Sinha, A. Zholus, et al. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- [2] A. Bardes, Q. Garrido, J. Ponce, X. Chen, M. Rabbat, Y. LeCun, M. Assran, and N. Ballas. V-jepa: latent video prediction for visual representation learning. In _ICLR_ , 2024. 

- [3] D. Bolya, P.-Y. Huang, P. Sun, J. H. Cho, A. Madotto, C. Wei, T. Ma, J. Zhi, J. Rajasegaran, H. Bangalath, et al. Perception encoder: The best visual embeddings are not at the output of the network. _NeurIPS_ , 38:60884–60937, 2026. 

- [4] H. Cai, C. Gan, T. Wang, Z. Zhang, and S. Han. Once-for-all: Train one network and specialize it for efficient deployment. In _ICLR_ , 2020. 

- [5] Y.-H. Cao, P. Sun, and S. Zhou. Three guidelines you should know for universally slimmable self-supervised learning. In _CVPR_ , 2023. 

- [6] D. Chen, M. Shukor, T. Moutakanni, W. Chung, J. Yu, T. Kasarla, Y. Bang, A. Bolourchi, Y. LeCun, and P. Fung. Vl-jepa: Joint embedding predictive architecture for vision-language. _arXiv preprint arXiv:2512.10942_ , 2025. 

- [7] M. Chen, H. Peng, J. Fu, and H. Ling. Autoformer: Searching transformers for visual recognition. In _ICCV_ , 2021. 

- [8] M. Chen, K. Wu, B. Ni, H. Peng, B. Liu, J. Fu, H. Chao, and H. Ling. Searching the search space of vision transformer. In _NeurIPS_ , 2021. 

- [9] D. Damen, H. Doughty, G. M. Farinella, A. Furnari, E. Kazakos, J. Ma, D. Moltisanti, J. Munro, T. Perrett, W. Price, et al. Rescaling egocentric vision: Collection, pipeline and challenges for epic-kitchens-100. _IJCV_ , 2022. 

- [10] Devvrit, S. Kudugunta, A. Kusupati, T. Dettmers, K. Chen, I. Dhillon, Y. Tsvetkov, H. Hajishirzi, S. Kakade, A. Farhadi, and P. Jain. Matformer: Nested transformer for elastic inference. In _NeurIPS_ , 2024. 

- [11] A. Diko, D. Avola, B. Prenkaj, F. Fontana, and L. Cinque. Semantically guided representation learning for action anticipation. In _ECCV_ , pages 448–466. Springer, 2024. 

- [12] X. Dong, B. De Salvo, M. Li, C. Liu, Z. Qu, H.-T. Kung, and Z. Li. Splitnets: Designing neural architectures for efficient distributed computing on head-mounted systems. In _CVPR_ , pages 12559–12569, 2022. 

- [13] S. Dustdar, V. C. Pujol, and P. K. Donta. On distributed computing continuum systems. _IEEE Transactions on Knowledge and Data Engineering_ , 35(4):4092–4105, 2022. 

- [14] J. Engel, K. Somasundaram, M. Goesele, A. Sun, A. Gamino, A. Turner, A. Talattof, A. Yuan, B. Souti, B. Meredith, et al. Project aria: A new tool for egocentric multi-modal ai research. _arXiv preprint arXiv:2308.13561_ , 2023. 

- [15] A. Furnari and G. M. Farinella. Rolling-unrolling lstms for action anticipation from first-person video. _IEEE TPAMI_ , 43(11):4021–4036, 2020. 

17 

- [16] C. Gong, D. Wang, M. Li, X. Chen, Z. Yan, Y. Tian, Q. Liu, and V. Chandra. Nasvit: Neural architecture search for efficient vision transformers with gradient conflict aware supernet training. In _ICLR_ , 2022. 

- [17] R. Goyal, S. Ebrahimi Kahou, V. Michalski, J. Materzynska, S. Westphal, H. Kim, V. Haenel, I. Fruend, P. Yianilos, M. Mueller-Freitag, et al. The" something something" video database for learning and evaluating visual common sense. In _ICCV_ , 2017. 

- [18] Z. Guo, X. Zhang, H. Mu, W. Heng, Z. Liu, Y. Wei, and J. Sun. Single path one-shot neural architecture search with uniform sampling. In _ECCV_ , pages 544–560, 2020. URL https://www.ecva.net/papers/eccv_2020/papers_ ECCV/papers/123610528.pdf. 

- [19] J. Haberer, A. Hojjat, and O. Landsiedel. Hydravit: Stacking heads for a scalable vit. In _NeurIPS_ , 2024. 

- [20] L. Hou, Z. Huang, L. Shang, X. Jiang, X. Chen, and Q. Liu. Dynabert: Dynamic bert with adaptive width and depth. In _NeurIPS_ , 2020. 

- [21] A. G. Howard, M. Zhu, B. Chen, D. Kalenichenko, W. Wang, T. Weyand, M. Andreetto, and H. Adam. Mobilenets: Efficient convolutional neural networks for mobile vision applications. _arXiv preprint arXiv:1704.04861_ , 2017. 

- [22] Y. Kang, J. Hauswald, C. Gao, A. Rovinski, T. Mudge, J. Mars, and L. Tang. Neurosurgeon: Collaborative intelligence between the cloud and mobile edge. In _Proceedings of the Twenty-Second International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS)_ , pages 615–629, 2017. 

- [23] W. Kay, J. Carreira, K. Simonyan, B. Zhang, C. Hillier, S. Vijayanarasimhan, F. Viola, T. Green, T. Back, P. Natsev, et al. The kinetics human action video dataset. _arXiv preprint arXiv:1705.06950_ , 2017. 

- [24] A. Kusupati, G. Bhatt, A. Rege, M. Wallingford, A. Sinha, V. Ramanujan, W. Howard-Snyder, K. Chen, S. Kakade, P. Jain, and A. Farhadi. Matryoshka representation learning. In _NeurIPS_ , 2022. 

- [25] S. Laskaridis, S. I. Venieris, M. Almeida, I. Leontiadis, and N. D. Lane. Spinn: Synergistic progressive inference of neural networks over device and cloud. In _Proceedings of the 26th Annual International Conference on Mobile Computing and Networking (MobiCom)_ , pages 1–14, 2020. 

- [26] L. Maes, Q. Le Lidec, D. Scieur, Y. LeCun, and R. Balestriero. Leworldmodel: Stable end-to-end joint-embedding predictive architecture from pixels, 2026. _URL: https://arxiv. org/abs/2603.19312_ , 2026. 

- [27] S. Mehta and M. Rastegari. Mobilevit: light-weight, general-purpose, and mobile-friendly vision transformer. In _ICLR_ , 2021. 

- [28] A. Miech, D. Zhukov, J.-B. Alayrac, M. Tapaswi, I. Laptev, and J. Sivic. Howto100m: Learning a text-video embedding by watching hundred million narrated video clips. In _CVPR_ , pages 2630–2640, 2019. 

- [29] H. Mittal, N. Agarwal, S.-Y. Lo, and K. Lee. Can’t make an omelette without breaking some eggs: Plausible action anticipation using large video-language models. In _CVPR_ , pages 18580–18590, 2024. 

- [30] M. Oquab, T. Darcet, T. Moutakanni, H. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- [31] D. Roy, R. Rajendiran, and B. Fernando. Interaction region visual transformer for egocentric action anticipation. In _CVPR_ , pages 6740–6750, 2024. 

- [32] D. Shah, A. Sridhar, A. Bhorkar, N. Hirose, and S. Levine. Gnm: A general navigation model to drive any robot. In _Int. Conf. on Robot. and Automation_ , pages 7226–7233. IEEE, 2023. 

- [33] M. Tan and Q. Le. Efficientnet: Rethinking model scaling for convolutional neural networks. In _ICML_ , pages 6105–6114. PMLR, 2019. 

- [34] M. Tschannen, A. Gritsenko, X. Wang, M. F. Naeem, I. Alabdulmohsin, N. Parthasarathy, T. Evans, L. Beyer, Y. Xia, B. Mustafa, et al. Siglip 2: Multilingual vision-language encoders with improved semantic understanding, localization, and dense features. _arXiv preprint arXiv:2502.14786_ , 2025. 

- [35] D. Wang, M. Li, C. Gong, and V. Chandra. Attentivenas: Improving neural architecture search via attentive sampling. In _CVPR_ , pages 6418–6427, 2021. 

- [36] L. Wang, B. Huang, Z. Zhao, Z. Tong, Y. He, Y. Wang, Y. Wang, and Y. Qiao. Videomae v2: Scaling video masked autoencoders with dual masking. In _CVPR_ , pages 14549–14560. IEEE, 2023. 

18 

- [37] Y. Wang, K. Li, X. Li, J. Yu, Y. He, G. Chen, B. Pei, R. Zheng, Z. Wang, Y. Shi, et al. Internvideo2: Scaling foundation models for multimodal video understanding. In _ECCV_ , pages 396–416. Springer, 2024. 

- [38] J. Yu and T. S. Huang. Universally slimmable networks and improved training techniques. In _ICCV_ , 2019. 

- [39] J. Yu, L. Yang, N. Xu, J. Yang, and T. S. Huang. Slimmable neural networks. In _ICLR_ , 2019. 

- [40] J. Yu, P. Jin, H. Liu, G. Bender, P.-J. Kindermans, M. Tan, T. Huang, X. Song, R. Pang, and Q. V. Le. Bignas: Scaling up neural architecture search with big single-stage models. In _ECCV_ , 2020. 

- [41] H. Zhang, X. Li, and L. Bing. Video-llama: An instruction-tuned audio-visual language model for video understanding. In _Empirical Methods in Natural Lang. Process._ , pages 543–553, 2023. 

- [42] Y. Zhang, H. Coskun, X. Ma, H. Wang, K. Ma, X. Chen, D. H. Hu, and Y. Fu. Slicing vision transformer for flexible inference. In _NeurIPS_ , 2024. 

- [43] L. Zhao, N. B. Gundavarapu, L. Yuan, H. Zhou, S. Yan, J. J. Sun, L. Friedman, R. Qian, T. Weyand, Y. Zhao, et al. Videoprism: A foundational visual encoder for video understanding. _arXiv preprint arXiv:2402.13217_ , 2024. 

- [44] Z. Zhou, X. Chen, E. Li, L. Zeng, K. Luo, and J. Zhang. Edge intelligence: Paving the last mile of artificial intelligence with edge computing. _Proceedings of the IEEE_ , 107(8):1738–1762, 2019. 

19 

