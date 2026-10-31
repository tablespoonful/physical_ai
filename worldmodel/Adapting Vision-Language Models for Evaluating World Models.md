---
title: "Adapting Vision-Language Models for Evaluating World Models"
date: "2025-06-22"
authors: "Mariya Hendriksen; Tabish Rashid; David Bignell; Raluca Georgescu; Abdelhak Lemkhenter; Katja Hofmann"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2506.17967
pdf: https://arxiv.org/pdf/2506.17967
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2506.17967)** / [論文ページ](https://arxiv.org/abs/2506.17967)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Preprint 

# ADAPTING VISION-LANGUAGE MODELS FOR EVALUATING WORLD MODELS 

**Mariya Hendriksen Tabish Rashid** University of Oxford<sup>_∗_</sup> Microsoft Research Oxford, United Kingdom Cambridge, United Kingdom 

**David Bignell** Microsoft Research Cambridge, United Kingdom 

**Raluca Georgescu Abdelhak Lemkhenter Katja Hofmann** Microsoft Research Microsoft Research Microsoft Research Cambridge, United Kingdom Cambridge, United Kingdom Cambridge, United Kingdom 

**Sam Devlin**<sup>_†_</sup> Microsoft Research Cambridge, United Kingdom 

**Sarah Parisot**<sup>_†_</sup> Microsoft Research Cambridge, United Kingdom 

## ABSTRACT 

World models – generative models that simulate environment dynamics conditioned on past observations and actions – are gaining prominence in planning, simulation, and embodied AI. However, evaluating their rollouts remains a fundamental challenge, requiring fine-grained, temporally grounded assessment of action alignment and semantic consistency – capabilities not captured by existing metrics. Vision-Language Models (VLMs) have shown promise as automatic evaluators of generative content due to their strong multimodal reasoning abilities. Yet, their use in fine-grained, temporally sensitive evaluation tasks remains limited and requires targeted adaptation. We introduce an evaluation protocol targeting two recognition tasks – action recognition and character recognition – each assessed across binary, multiple-choice, and open-ended formats. To support this, we present UNIVERSE (UNIfied Vision-language Evaluator for Rollouts in Simulated Environments), a VLM-based evaluator for video world model rollouts adapted under data and compute constraints. In our extensive experiments totaling over 5,154 GPU-days, we explore full, partial, and parameter-efficient adaptation methods across various task formats, context lengths, sampling methods, and data compositions. The resulting unified evaluator achieves parity with task-specific checkpoints. Human studies across seven diverse environments confirm strong alignment with human judgments, establishing UNIVERSE as a lightweight, adaptable, and semantics-aware evaluator for video world models. 

## 1 INTRODUCTION 

World models – generative models trained to predict future observations conditioned on past observations and actions (Ha & Schmidhuber, 2018; Hafner et al., 2025; Alonso et al., 2024) – are rapidly becoming central to interactive AI. They provide a powerful abstraction for learning, reasoning, and planning in complex interactive environments, and underpin advances in neural game engines (Kanervisto et al., 2025; Guo et al., 2025; Gao et al., 2025; Chen et al., 2025), embodied AI (Du et al.; Yang et al., 2024), and autonomous driving (Russell et al., 2025; Hu et al., 2023a; Ni et al., 2025). 

Yet, evaluating world models remains a bottleneck. Rollouts are semantically rich and temporally grounded, requiring metrics that assess (i) alignment between generated frames and action sequences at the timestamp level (Yang et al., 2024), and (ii) consistent entity tracking over time (Kanervisto et al., 2025). Existing approaches fall short: (i) early distributional metrics focus on images and 

> _∗_ Work done during an internship at Microsoft Research. 

> _†_ Co-senior authorship. 

1 

Preprint 


Figure 1: Performance and efficiency of UNIVERSE (orange bars throughout) compared to taskspecific baselines (multiple colours), all models trained for 10 epochs. **Left and Center:** Action recognition and Character Recognition accuracy across binary, multiple-choice, and open-ended settings. **Right:** Sample efficiency – our adaptation recipe achieves strong performance with substantially fewer training samples per epoch. 

are sensitive to low-level variations (Salimans et al., 2016; Heusel et al., 2017; Binkowski et al., 2018), (ii) motion-aware metrics like FVD (Unterthiner et al., 2018) lack semantic grounding, and (iii) multimodal metrics ignore timestamp-level action conditioning (Jayasumana et al., 2024). Emerging text-to-video benchmarks (Liu et al., 2024b; Huang et al., 2024; Liao et al., 2024) focus on open-ended generation but neglect the fine-grained control central to world model evaluation. Even cutting-edge LLMs fail in this setting (Appendix G.1, Figure 15). Human evaluation remains the gold standard (Agarwal et al., 2025; Analysis, 2024), however, it remains costly and hard to scale. 

To address this gap, we propose a novel evaluation protocol targeting two important dimensions of rollout quality: action alignment and character consistency, formalized as recognition tasks – Action Recognition (AR), Character Recognition (CR) – across formats of varying complexity. The protocol provides a foundation for semantic evaluation of rollouts, and extends upon existing evaluation method by providing insight into semantic quality of generated rollouts. Inspired by the LLM-as-aJudge research direction Zheng et al. (2023), we explore whether Vision-Language Models (VLMs) can serve as effective evaluators in this setting. VLMs have demonstrated strong generalization across multimodal tasks (Li et al., 2023; Driess et al., 2023; Chen et al., 2023; Wang et al., 2024; Abdin et al., 2024; Liu et al., 2024a; Deitke et al., 2024; McKinzie et al., 2024), and show promise as automatic judges of generative models (Lee et al., 2024; Mañas et al., 2024; Lin et al., 2024; Chen et al., 2024). Yet, off-the-shelf VLMs struggle with the temporal grounding and domain-specific knowledge (see Sec. 4, Zero-Shot Evaluation). Limited resources and sparse text supervision introduce another layer of complexity to the setting. 

We therefore conduct a systematic study of adaptation strategies under realistic data and compute constraints. Throughout the study totaling over 5,154 GPU-days, we analyze the impact of supervision regime, frame sampling strategy, visual context length, and training budget. The result of the study is UNIVERSE ( **UNI** fied **V** ision-language **E** valuator for **R** ollouts in **S** imulated **E** nvironments), a lightweight, adaptable, and semantics-aware evaluator for world models. UNIVERSE achieves parity with six task-specific checkpoints while using a single unified model (see Figure 1. To validate reliability, we conduct a large-scale human study on rollouts spanning diverse environments, model scales, and rollout fidelities. UNIVERSE’s judgments show strong agreement with human ratings, demonstrating its effectiveness as a practical, semantics-aware evaluator—particularly valuable in settings where ground-truth annotations are unavailable or prohibitively expensive. 

## 2 RELATED WORK 

**Challenges in Evaluating World Models.** World models are generative systems that learn predictive representations of environment dynamics (Ha & Schmidhuber, 2018), originally proposed for modelbased RL (Sutton, 1991) and now central to domains such as neural game engines (Kanervisto et al., 2025; Guo et al., 2025; Gao et al., 2025; Chen et al., 2025), embodied AI (Du et al.; Yang et al., 2024), and autonomous driving (Russell et al., 2025; Hu et al., 2023a; Ni et al., 2025). Recent models such as Dreamer v1–3 (Hafner et al., 2020; Hafner et al.; 2023; 2025), MuZero (Schrittwieser et al., 2020), IRIS (Micheli et al., 2023), UniSim (Yang et al., 2024), and DIAMOND (Alonso et al., 2024) have improved rollout fidelity and controllability. Yet evaluation largely focuses on downstream success metrics—e.g., game score or goal completion (Bellemare et al., 2013; Kaiser et al., 2020; 

2 

Preprint 

Guss et al., 2021; Baker et al., 2022; Beattie et al., 2016)—which provide only coarse, indirect signals of rollout quality. Genie (Bruce et al., 2024; Parker-Holder et al., 2024) decouples world model learning and agent training, but its evaluation still emphasizes visual quality and control, without probing semantic or causal fidelity. Cosmos (Agarwal et al., 2025) proposes a structured protocol that combines FID/FVD with structure-from-motion-based 3D consistency checks and human ratings on instruction following, object permanence, and visual verity. While insightful, this approach is tied to simulator-specific infrastructure and requires costly manual comparison. Human-in-the-loop protocols such as the Video Generation Arena (Analysis, 2024) also rely on pairwise comparison to assess rollout quality. These methods, though informative, are expensive and hard to scale. 

**Evaluation Metrics and Protocols for Visual Generation.** Early evaluations of generative models relied on full-reference metrics such as PSNR and SSIM (Wang et al., 2004), which capture pixel-level and perceptual similarity but are sensitive to spatial misalignments and fail to reflect semantic fidelity. To address this, distributional metrics like Inception Score (IS) (Salimans et al., 2016), Fréchet Inception Distance (FID) (Heusel et al., 2017), and Kernel Inception Distance (KID) (Binkowski et al., 2018). Other proposals such as PPL (Karras et al., 2019), Parzen likelihoods (Goodfellow et al., 2014), and HYPE (Zhou et al., 2019) attempt to quantify perceptual smoothness or human realism, but remain focused on static images. For video generation, FVD (Unterthiner et al., 2018) generalizes FID using I3D features (Carreira & Zisserman, 2017), introducing a motion-aware distributional baseline. Yet, FVD also lacks semantic grounding and does not account for causal structure or goal alignment. To improve semantic grounding, metrics based on text-image alignment have been proposed. CLIPScore (Hessel et al., 2021) and CLIPSIM (Wu et al., 2021) compute similarity between generated visuals and textual or visual references using CLIP embeddings (Radford et al., 2021), while Jayasumana et al. (2024) extend this to distributional comparisons via MMD. However, all operate at the frame level. Structured evaluation protocols using vision-language reasoning have also emerged. VQA Accuracy (Mañas et al., 2024) uses LLMs to score answers on static image questions, and VQAScore (Lin et al., 2024) probes alignment via templated binary queries. Lee et al. (2024) propose VLM evaluator to evaluate other VLMs responses given user criteria. These approaches introduce task structure but remain limited to single-frame evaluation. Recent text-tovideo (T2V) benchmarks such as EvalCrafter (Liu et al., 2024b), VBench (Huang et al., 2024), and DEVIL (Liao et al., 2024) introduce curated prompts and metrics covering text alignment, motion realism, and perceptual quality. While these protocols push forward evaluation of open-ended video generation, they lack timestamp-level action grounding. 

**Vision-Language Model Adaptation.** VLMs have emerged as powerful tools for multimodal understanding, demonstrating strong performance across tasks such as captioning, retrieval, visual question answering, and instruction following (Hendriksen et al., 2022; Li et al., 2023; Driess et al., 2023; Chen et al., 2023; Wang et al., 2024; Abdin et al., 2024; Liu et al., 2024a; Deitke et al., 2024; McKinzie et al., 2024). Adaptation approaches can be broadly categorized into prompt-level and weight-level methods. One prominent prompt-level adaptation techniques is prompt tuning, which injects task information directly into the input space (Miyai et al., 2023; Zhou et al., 2024; Wu et al., 2024a), and in-context learning (ICL), where models such as GPT-3 (Brown et al., 2020) and Flamingo (Alayrac et al., 2022) condition on task demonstrations at inference time without updating parameters. Retrieval-augmented generation (RAG) (Lewis et al., 2020) combines parametric models with non-parametric memory, and multimodal variants incorporate external visual or auditory context (Hu et al., 2023b; Chen et al., 2022a). While lightweight, these approaches are limited in their ability to model temporal dependencies or align with structured rollouts. Weight-level adaptation enables stronger domain alignment but incurs higher computational cost. Full finetuning remains effective yet costly, while partial finetuning (Ye et al., 2023) offers a trade-off by updating only selected layers. Parameter-efficient finetuning (PEFT) provides a scalable alternative and can be grouped into low-rank and adapter-based strategies (Han et al., 2024). Low-rank methods, such as LoRA (Hu et al., 2022), inject rank-constrained updates into frozen layers. Recent extensions improve upon this via weight decomposition (Liu et al.), quantization-aware adaptation (Dettmers et al., 2023; Xu et al., 2024), mixture-of-experts routing (Wu et al., 2024b), and long-context support (Chen et al.). Adapter-based methods insert lightweight modules between frozen layers to enable modular adaptation with minimal overhead (Luo et al., 2023; Zhao et al., 2024). A parallel line of work investigates multimodal few-shot learning. Frozen (Tsimpoukelli et al., 2021) was among the first to explore this setting, followed by works combining prompting and ICL for improved sample efficiency (Jin et al., 2022; Song et al., 2022), and works introducing a learnable meta-mapper to bridge frozen VLM components for few-shot meta-learning (Najdenkoska et al., 2023). 

3 

Preprint 

**Our Focus.** While prior efforts have explored related challenges, none directly address the evaluation of the structured, action-conditioned fidelity and semantics of world model rollouts using adapted VLM. To this end, we introduce: (i) an evaluation protocol for world model rollouts, targeting fine-grained, temporally grounded assessment of semantic fidelity; (ii) UNIVERSE, a VLM-based method to support the protocol. We validate its alignment with human judgments and demonstrate its scalability and semantic sensitivity across rollout conditions. 

## 3 METHODOLOGY 

We consider the problem of evaluating rollouts generated by _world models_ in interactive environments. A world model _W_ is trained to predict the next observation _ot_ given the past observations _o<t_ and actions _a<t_ : _W_ : ( _o<t, a<t_ ) _→ ot_ , where _ot ∈O_ represents the sensory observation at timestep _t_ , typically an RGB image. Rollouts consist of temporally grounded sequences that reflect the causal effects of control inputs. These outputs are semantically rich and visually complex, requiring timestamp-level assessment of correctness. 

To enable automatic evaluation, we propose UNIVERSE, an adapted Vision-Language Model (VLM) that serves as a structured evaluator for world model rollouts. Formally, it operates as a function: _E_ : ( _V, Q_ ) _→ A_<sup>ˆ</sup> , where _V_ = ( _ot_ 1 _, . . . , otk_ ) _∈O_<sup>_k_</sup> is a sequence of frames from a rollout, _Q ∈L_ is a natural language question, and _A_<sup>ˆ</sup> _∈L_ is the predicted answer. Evaluation quality is measured by comparing _A_<sup>ˆ</sup> to the reference answer _A_ using semantic similarity metrics. 

**Evaluation Protocol.** We define two structured recognition tasks: (i) _Action Recognition (AR)_ : Assesses whether generated sequences accurately reflect the effects of agent actions given the segment; (ii) _Character Recognition (CR)_ : Evaluates whether entities maintain consistent identity and appearance across time. Each task is framed as a visual QA problem: the evaluator receives a sequence of frames and a natural language prompt (binary, multiple-choice, or open-ended), and generates a textual response. Outputs are scored using Exact Match (EM) and ROUGE-F1 (ROUGE), capturing both literal and semantic alignment with the reference answer. Metric details are in Appendix E.2. 

**Dataset Construction.** Effective VLM adaptation for rollout evaluation requires a dataset that (i) captures realistic human behavior in interactive environments, and (ii) aligns with prior work in simulated settings to support comparability and reproducibility. To satisfy these constraints, we partnered with Ninja Theory and curated a dataset from both internal and public _Bleeding Edge_ gameplay recordings, focusing on the _Skygarden_ evnironment (Kanervisto et al., 2025). This dataset provides high visual and behavioral diversity (Pearce et al., 2025), includes a publicly available evaluation split, and is closely aligned with prior work in the domain (Kanervisto et al., 2025; Pearce et al., 2025; Tot et al., 2025; Sharma et al., 2024; Devlin et al., 2021), enabling fair comparison. 

Data preparation proceeds in three stages: (i) _Preprocessing:_ Segment gameplay into 14-frame clips with synchronized video, control logs, and metadata; (ii) _Description Generation:_ Convert structured annotations (e.g., actions, agent states) into natural language summaries; (iii) _Question-Answer Pair Construction:_ Generate six complimentary QA pairs per clip (binary, multiple-choice, and open-ended) spanning both AR and CR tasks. The final dataset contains 32.453 training clips and 8.113 validation clips, yielding 194.718 and 48.678 QA pairs, respectively. See Appendix D for details. 

**Model Architecture.** We adapt a model from the PaliGemma family (Beyer et al., 2024; Steiner et al., 2024), consisting of a vision encoder _MV_ , a projection head _MP_ , and a language decoder _ML_ . Based on initial zero-shot evaluations (Appendix G.2), we use a single configuration for all experiments—PaliGemma 2 3b, which includes a 2B-parameter Gemma 2 decoder pretrained on 2T tokens. Input frames are resized to 224 _×_ 224 and tokenized into 256 patches each. Model achitecture details are in Appendix E.1. 

Each model input sequence _S_ = _{SI, ST_<sup>PREF</sup> _, ST_<sup>SUFF</sup> _}_ consists of: visual tokens _SI_ from _k_ frames, a textual prefix _ST_<sup>PREF</sup> containing the task-language cue and question, and a suffix _ST_<sup>SUFF</sup> with the expected answer (used only during training). This format allows the decoder to attend jointly over visual and textual context. Full prompt details are provided in Appendix E.1. 

4 

Preprint 

**Training Objective.** We optimize a causal language modeling loss on the answer suffix: 


where _s_<sup>SUFF</sup> _t_ is the _t_ -th token in the suffix, and _t_<sup>_′_</sup> = _TI_ + _T_ PREF + _t_ is the token position in the flattened sequence. 

**Adaptation Strategies.** We explore a broad design space for adapting pretrained VLMs to temporally grounded rollout evaluation. Our study spans three core dimensions: _fine-tuning configurations_ , _frame sampling policy_ , and _supervision composition_ . 

_Fine-Tuning Configurations._ We compare five adaptation strategies varying in parameter count and modularity: (i) _Zero-shot prompting:_ No tuning; model is prompted directly. (ii) _Full fine-tuning:_ All parameters _θ_ = _θV ∪ θP ∪ θL_ are updated end-to-end. (iii) _Dual-component fine-tuning:_ Two of three modules are trained (e.g., _θP ∪ θL_ ). (iv) _Single-component fine-tuning:_ Only one module—vision, projection, or language—is updated. (v) _Parameter-efficient fine-tuning:_ We apply LoRA (Hu et al., 2022) adapters to attention and MLP layers in vision and language components: **W** _←_ **W** +<sup>_<u>α</u>_</sup> _r_<sup>**AB**</sup><sup>_,_</sup> _α_ = 8 _, r ∈{_ 8 _,_ 16 _,_ 32 _,_ 48 _,_ 64 _}_ . 

_Frame Sampling Policy._ We vary both the number of input frames and their sampling strategy. Specifically, we sweep over _k ∈_ [1 _,_ 8], and evaluate two selection methods: (i) _First-n_ : selecting the first _k_ frames from each rollout; (ii) _Uniform-n_ : sampling _k_ frames uniformly across the full clip. 

_Supervision Composition._ To support generalization across QA formats and tasks, we construct a multi-task dataset covering binary, multiple-choice, and open-ended prompts across both AR and CR. We perform a three-stage grid search to optimize the data mixture: (i) Varying AR/CR task ratios ( _α_ AR, _α_ CR) while fixing QA type proportions ( _β_ Binary _, β_ MC _, β_ OE); (ii) Tuning the proportion of open-ended supervision ( _β_ OE) for best performance; (iii) Adjusting _β_ Binary and _β_ MC. 

**UNIVERSE: UNIfied Vision-language Evaluator for Rollouts in Simulated Environments.** We distill our empirical findings into UNIVERSE, a lightweight and scalable adaptation method for temporally grounded evaluation of world model rollouts using VLMs. Designed for constrained compute and limited supervision, UNIVERSE delivers strong generalization across our evaluation protocol using a single, partially tuned model. The method combines three main components: I _Partial fine-tuning:_ We update only the projection head ( _θP_ ), training just 0.07% of model parameters. Despite this minimal footprint, it achieves the second-best performance among all strategies—trailing only vision encoder tuning, which requires _∼_ 11% of parameters and incurs significantly higher compute cost. II _Efficient frame sampling:_ Each input sequence includes _k_ = 8 frames sampled uniformly from a 14-frame rollout. This sparsity-aware strategy maintains long-range temporal structure while reducing token count and enabling efficient batching. III _Mixed supervision:_ We train on a hierarchical mixture of tasks and QA formats. The task distribution favors Action Recognition ( _α_ AR = 0 _._ 8) as it converges slower. Within each task, we emphasize open-ended questions ( _β_ OE = 0 _._ 8), while maintaining smaller proportions of binary ( _β_ binary = 0 _._ 15) and multiple-choice ( _β_ MC = 0 _._ 05) examples. 

## 4 EXPERIMENTS 

We evaluate UNIVERSE on ground truth video data, focusing on AR and CR across binary, multiplechoice, and open-ended formats. Our goals are twofold: (i) to benchmark performance against zero-shot and fine-tuned baselines, and (ii) to assess the trade-offs between adaptation strategies under constrained supervision and compute. 

**Baselines.** We compare UNIVERSE against two classes of baselines: (i) _Zero-shot VLMs:_ Seven off-the-shelf models, including VideoLLaMA3 (2B, 7B) (Boqiang Zhang, 2025) and three PaliGemma models: version 1 (3B) and version 2 (3B and 10B) (Beyer et al., 2024; Steiner et al., 2024), evaluated without domain adaptation using an 8-frame visual context window.<sup>1</sup> (ii) _Fine-tuned PaliGemma 2:_ Variants adapted via full, partial, and parameter-efficient tuning. This backbone is selected based on a 

1We also experimented with CLIPScore-based evaluation (Appendix G.3); results underperformed relative to selected baselines and were constrained to predefined candidate sets, further underscoring the need for model adaptation. 

5 

Preprint 


Figure 2: Comparison of UNIVERSE and baseline models on Action and Character Recognition, all models trained for 1 epoch. **Left** : UNIVERSE outperforms all baselines on AR. **Right** : On CR, it ranks third, behind models with either full vision encoder tuning or task-specific training with greater supervision. Trained under a unified protocol with minimal parameter updates (0.07%) and reduced per-task data, UNIVERSE delivers strong performance across both tasks. 

sweep over PaliGemma variants, using zero-shot performance as a guide (Appendix G.2). The adaptation space includes 8 primary baselines: (i) _Single-component fine-tuning_ : tuning only the vision encoder ( _F_ V), the multimodal projector ( _F_ P), or the language head ( _F_ L); (ii) _Two-component fine-tuning_ : jointly tuning pairs of components— _F_ V+P, _F_ V+L, and _F_ P+L; (iii) _Full-model fine-tuning_ : tuning all components simultaneously ( _F_ V+P+L); (iv) _LoRA-based tuning_ : Parameter-efficient adaptation with rank _r_ = 8, selected after observing minimal performance variation across _r ∈{_ 8 _,_ 16 _,_ 32 _,_ 48 _,_ 64 _}_ (see Appendix G.4 for details). All models are trained using 8-frame clips and a single epoch. 

**Results.** Figure 2 (left, center) summarizes performance across Action Recognition (AR) and Character Recognition (CR). Zero-shot VLMs perform poorly: VideoLLaMA3 variants stay below 12.7% (AR) and 6.4% (CR), while PaliGemma reaches 29.7% (AR) and 17.2% (CR), confirming that general-purpose models lack the temporal grounding and domain-specific semantics needed for rollout evaluation. In contrast, UNIVERSE outperforms all models on AR and ranks third on CR—despite tuning only the 2.66M-parameter projector (0.07% of the model) under a unified protocol spanning both tasks, all prompt formats, and reduced supervision. The two stronger CR baselines fine-tune either the full 400M-parameter vision encoder or use 5 _×_ more task-specific CR data. Its performance under these constraints underscores the efficiency and generality of our adaptation strategy for temporally grounded evaluation. 

## 5 ANALYSIS 

We find a consistent performance gap between AR and CR, highlighting the greater temporal and causal complexity of action understanding. This motivates our focus on AR as the more challenging and diagnostic task. Below, we analyze how adaptation choices shape performance on AR. 

**Supervision and Temporal Context.** We begin by analyzing how supervision (training budget) and temporal input (number of frames) influence UNIVERSE performance. By independently and jointly varying the number of training epochs and input frames, we disentangle the contributions of model capacity and temporal context to task success. 

_Results._ CR converges rapidly, achieving over 97% exact match after 12.5% of an epoch (~4K samples; Figure 5, bottom), and shows minor improvement with further training. In contrast, AR improves only modestly under extended training when limited to a single frame (Figure 5, top), suggesting that supervision alone is insufficient in the absence of temporal information. Motivated by this, we jointly scale both supervision and input length, varying the number of frames and epochs. As shown in Figure 3, performance on AR improves consistently across all formats, with the best results achieved under combined scaling. 

**Temporal Sampling Strategies.** Following the observation that AR requires both extended supervision and temporally rich input, we examine how frame selection impacts performance. We compare first- _n_ sampling, which selects the first _n_ consecutive frames from each rollout, to uniform- _n_ sampling, which draws _n_ evenly spaced frames across the entire sequence. We conduct experiments at varying context lengths, using _n ∈{_ 1 _,_ 2 _, . . . ,_ 8 _}_ frames. to evaluate the impact of both sampling method and input horizon. 

6 

Preprint 


Figure 3: Action Recognition performance as a function of training supervision (epochs) and temporal context (number of frames), evaluated across all formats. Performance improves along both axes, with highest accuracy achieved when both dimensions are scaled. 

Figure 4: Effect of frame sampling strategy on Action Recognition performance across all formats. Uniform- _n_ sampling (orange) consistently outperforms first- _n_ (blue), with especially large gains at low frame counts, and maintains an advantage as temporal context increases. 

_Results._ As shown in Figure 4, uniform- _n_ consistently outperforms first- _n_ across all evaluation formats. The effect is most pronounced at low frame counts. With only 2 input frames, uniform sampling improves exact match accuracy from 84.42% to 90.47% in Binary, from 65.53% to 83.93% in Multiple-Choice, and from 65.38% to 82.68% in Open-Ended formats. Gains persist even at 8 frames, where uniform sampling maintains an advantage across formats. 

**Optimizing Data Mix for Unified Multi-Task Evaluation.** We analyze how training data composition affects multi-task performance in UNIVERSE, with the goal of enabling a single model to generalize across AR and CR. Specifically, we study how the task-level ratio _α_ and format-level ratio _β_ influence performance across evaluation settings. We first conduct a hierarchical ablation to identify an optimized data mixture, then assess its impact by comparing against a default task mix with uniform sampling. 

_Data Mix Optimization._ To determine an effective training mixture for UNIVERSE, we perform a hierarchical ablation over task-level and format-level data ratios. We begin by varying the task-level proportion _α_ (AR vs. CR), holding the format distribution fixed at 


Figure 5: Exact Match accuracy for Action Recognition and Character Recognition. 

_β_ binary = _β_ MC = _β_ OE =<sup>1</sup> _/_ 3. As shown in Figure 6 (left), increasing _α_ AR improves AR performance—especially for multiple-choice—while CR remains stable, with a favorable tradeoff reached at _α_ AR = 0 _._ 8. However, open-ended accuracy shows little change, motivating format-specific rebalancing. Fixing _α_ AR = 0 _._ 8, we sweep the format ratio _β_ OE, and observe in Figure 6 (center) that AR-OE accuracy improves substantially with increased open-ended coverage, peaking at _β_ OE = 0 _._ 8, albeit at the cost of binary performance. To restore balance, we fix _β_ OE = 0 _._ 8 and allocate the remaining budget across binary and multiple-choice formats. As shown in Figure 6 (right), performance remains robust across configurations, with a slight preference for _β_ binary = 0 _._ 15 and _β_ MC = 0 _._ 05. Based on these findings, we adopt the following optimized data composition: _α_ AR = 0 _._ 8, _α_ CR = 0 _._ 2; _β_ binary = 0 _._ 15, _β_ MC = 0 _._ 05, and _β_ OE = 0 _._ 8. 

_Effectiveness of the Optimized Mix._ Having identified an optimized training mixture through hierarchical ablation, we now evaluate its impact in practice. We compare the final UNIVERSE model—trained 

7 

Preprint 


Figure 6: Hierarchical ablation of training data composition for UNIVERSE.. **Left** : Varying task-level ratio _α_ (AR vs. CR) with uniform format distribution ( _β_ = 1 _/_ 3) shows that increasing) shows that increasing _α_ AR improves AR performance, especially for multiple-choice, while open-ended remains flat. **Center** : Sweeping format-level ratio _β_ OE with fixed with fixed _α_ AR = 0 _._ 8 reveals that oversampling open-ended data ( reveals that oversampling open-ended data ( _β_ OE = 0 _._ 8)) improves AR-OE performance. **Right** : Fine-tuning binary and MC proportions under _β_ OE = 0 _._ 8 shows performance is stable across mixes, with slight gains from _β_ binary = 0 _._ 15,, _β_ MC = 0 _._ 05.. 

Figure 7: Comparison of two training regimes: a default data mix (equal task and format proportions) and the optimized mix derived from hierarchical tuning. The optimized configuration yields substantial gains on AR, while maintaining strong CR performance. 

with this optimized mix—to a baseline trained with a default task and format distribution. We train both models on 4 epochs. As shown in Figure 7, the optimized configuration yields substantial gains on AR, particularly for multiple-choice and open-ended formats, while maintaining competitive performance on CR. These results underscore the importance of data composition in enabling robust multi-task learning within a unified evaluator. 

## 6 EVALUATING WORLD MODEL ROLLOUTS WITH UNIVERSE 

We evaluate the reliability of UNIVERSE through a human study spanning eight distinct settings that vary in model scale, training data diversity, and output resolution. Our analysis considers two axes: (i) _in-domain accuracy_ , measured on Skygarden, and (ii) _generalization_ to six previously unseen environments. 

Concretely, we study rollouts generated by: (i) a large-scale model trained across multiple environments with higher-resolution rollouts (300 _×_ 180), and (ii) a smaller model trained on a single environment with lower-resolution rollouts (128 _×_ 128). These two model families expose complementary challenges: resolution mismatch, domain coverage, and rollout fidelity. We construct eight evaluation settings: settings 1–7 draw from the large-scale model across diverse environments, while setting 8 uses the smaller model in the fine-tuning environment. Each setting contains 30 rollouts, paired with six natural-language questions from our evaluation protocol, yielding 240 rollouts in total. UNIVERSE answers each question via majority vote over five greedy decoding samples. Human annotators rate responses on a four-point ordinal scale ( _Correct_ , _Partially Correct_ , _Incorrect_ , _Unclear_ ), with double annotation and adjudication on disagreements. Inter-rater reliability is measured using Cohen’s _κ_ . Full details of the annotation protocol are provided in Appendix F. 

8 

Preprint 


Figure 8: Example frames from the eight evaluation settings, spanning different model scales, rollout fidelities, and environments. Note the resolution difference: Settings 1-7 feature 300 _×_ 180 rollouts, whereas Setting 8 uses 128 _×_ 128. 


Figure 9: Graded accuracy of UNIVERSE across the eight evaluation settings. Performance improves with higher-fidelity rollouts and remains stable across unseen environments (2–7). Cohen’s _κ_ indicates substantial inter-rater agreement. 

_Results._ Figure 9 reports graded accuracy across all settings. Rollouts from the smaller, singleenvironment model yield lower evaluation accuracy, likely due to resolution mismatch, while the larger, multi-environment model provides higher-quality inputs. These results demonstrate that UNIVERSE generalizes across model scales, rollout fidelities, and environments, while remaining closely aligned with human judgments. 

## 7 CONCLUSION 

In this paper, we investigate the use of Vision-Language Models (VLMs) as automated evaluators for world model rollouts, addressing the fundamental challenge of fine-grained, temporally grounded evaluation. We introduce a structured evaluation protocol centered on action and character recognition tasks across binary, multiple-choice, and open-ended formats. To support this, we propose UNIVERSE, a unified method for adapting VLMs to this setting through mixed supervision, efficient frame sampling, and lightweight fine-tuning. Our large-scale study demonstrates that UNIVERSE matches the performance of all task-specific checkpoints using a single unified model and aligns closely with human judgments, establishing it as a scalable, semantics-aware evaluator for evaluating world models, particularly when explicit ground truth is unavailable or costly to obtain. 

**Limitations.** While our experiments focus on simulated environments, chosen both for their groundtruth availability and their direct relevance to large video-game and interactive-entertainment industries Kanervisto et al. (2025), evaluating UNIVERSE in real-world settings remains an important next step. Our protocol focuses on foundational semantic tasks, and extending it to cover higher-level reasoning represents an important direction for future work. Scaling UNIVERSE to long-horizon rollouts is also challenging, as fine-grained reasoning becomes harder with larger visual context. Our 

9 

Preprint 

frame-sampling analysis suggests that more intelligent sampling or hierarchical summarization could address this, and we plan to explore such strategies. Finally, as with all pretrained VLMs, UNIVERSE may inherit dataset biases and exhibit reduced reliability on ambiguous cases. While we examined them partially during evaluation, a deeper investigation into bias propagation is an exciting research direction for future work. 

## REFERENCES 

- Marah I. Abdin, Sam Ade Jacobs, Ammar Ahmad Awan, Jyoti Aneja, Ahmed Awadallah, Hany Awadalla, Nguyen Bach, Amit Bahree, Arash Bakhtiari, Harkirat S. Behl, Alon Benhaim, Misha Bilenko, Johan Bjorck, Sébastien Bubeck, Martin Cai, Caio César Teodoro Mendes, Weizhu Chen, Vishrav Chaudhary, Parul Chopra, Allie Del Giorno, Gustavo de Rosa, Matthew Dixon, Ronen Eldan, Dan Iter, Amit Garg, Abhishek Goswami, Suriya Gunasekar, Emman Haider, Junheng Hao, Russell J. Hewett, Jamie Huynh, Mojan Javaheripi, Xin Jin, Piero Kauffmann, Nikos Karampatziakis, Dongwoo Kim, Mahoud Khademi, Lev Kurilenko, James R. Lee, Yin Tat Lee, Yuanzhi Li, Chen Liang, Weishung Liu, Eric Lin, Zeqi Lin, Piyush Madan, Arindam Mitra, Hardik Modi, Anh Nguyen, Brandon Norick, Barun Patra, Daniel Perez-Becker, Thomas Portet, Reid Pryzant, Heyang Qin, Marko Radmilac, Corby Rosset, Sambudha Roy, Olatunji Ruwase, Olli Saarikivi, Amin Saied, Adil Salim, Michael Santacroce, Shital Shah, Ning Shang, Hiteshi Sharma, Xia Song, Masahiro Tanaka, Xin Wang, Rachel Ward, Guanhua Wang, Philipp Witte, Michael Wyatt, Can Xu, Jiahang Xu, Sonali Yadav, Fan Yang, Ziyi Yang, Donghan Yu, Chengruidong Zhang, Cyril Zhang, Jianwen Zhang, Li Lyna Zhang, Yi Zhang, Yue Zhang, Yunan Zhang, and Xiren Zhou. Phi-3 technical report: A highly capable language model locally on your phone. _arXiv preprint arXiv:2404.14219_ , 2024. 

- Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, Daniel Dworakowski, Jiaojiao Fan, Michele Fenzi, Francesco Ferroni, Sanja Fidler, Dieter Fox, Songwei Ge, Yunhao Ge, Jinwei Gu, Siddharth Gururani, Ethan He, Jiahui Huang, Jacob Samuel Huffman, Pooya Jannaty, Jingyi Jin, Seung Wook Kim, Gergely Klár, Grace Lam, Shiyi Lan, Laura Leal-Taixé, Anqi Li, Zhaoshuo Li, Chen-Hsuan Lin, Tsung-Yi Lin, Huan Ling, Ming-Yu Liu, Xian Liu, Alice Luo, Qianli Ma, Hanzi Mao, Kaichun Mo, Arsalan Mousavian, Seungjun Nah, Sriharsha Niverty, David Page, Despoina Paschalidou, Zeeshan Patel, Lindsey Pavao, Morteza Ramezanali, Fitsum Reda, Xiaowei Ren, Vasanth Rao Naik Sabavat, Ed Schmerling, Stella Shi, Bartosz Stefaniak, Shitao Tang, Lyne Tchapmi, Przemek Tredak, Wei-Cheng Tseng, Jibin Varghese, Hao Wang, Haoxiang Wang, Heng Wang, Ting-Chun Wang, Fangyin Wei, Xinyue Wei, Jay Zhangjie Wu, Jiashu Xu, Wei Yang, Lin Yen-Chen, Xiaohui Zeng, Yu Zeng, Jing Zhang, Qinsheng Zhang, Yuxuan Zhang, Qingqing Zhao, and Artur Zólkowski. Cosmos world foundation model platform for physical AI. _arXiv preprint arXiv:2501.03575_ , 2025. 

- Ibrahim M Alabdulmohsin, Xiaohua Zhai, Alexander Kolesnikov, and Lucas Beyer. Getting vit in shape: Scaling laws for compute-optimal model design. _Advances in Neural Information Processing Systems_ , 36:16406–16425, 2023. 

- Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, Roman Ring, Eliza Rutherford, Serkan Cabi, Tengda Han, Zhitao Gong, Sina Samangooei, Marianne Monteiro, Jacob L. Menick, Sebastian Borgeaud, Andy Brock, Aida Nematzadeh, Sahand Sharifzadeh, Mikolaj Binkowski, Ricardo Barreira, Oriol Vinyals, Andrew Zisserman, and Karén Simonyan. Flamingo: a visual language model for few-shot learning. _Advances in neural information processing systems_ , 35: 23716–23736, 2022. 

- Eloi Alonso, Adam Jelley, Vincent Micheli, Anssi Kanervisto, Amos J Storkey, Tim Pearce, and François Fleuret. Diffusion for world modeling: Visual details matter in atari. _Advances in Neural Information Processing Systems_ , 37:58757–58791, 2024. 

- Artificial Analysis. Video generation arena leaderboard, 2024. URL https://huggingface. co/spaces/ArtificialAnalysis/Video-Generation-Arena-Leaderboard. Accessed: 24 March 2025. 

- Bowen Baker, Ilge Akkaya, Peter Zhokov, Joost Huizinga, Jie Tang, Adrien Ecoffet, Brandon Houghton, Raul Sampedro, and Jeff Clune. Video pretraining (VPT): Learning to act by watching 

10 

Preprint 

unlabeled online videos. _Advances in Neural Information Processing Systems_ , 35:24639–24654, 2022. 

- Charles Beattie, Joel Z. Leibo, Denis Teplyashin, Tom Ward, Marcus Wainwright, Heinrich Küttler, Andrew Lefrancq, Simon Green, Víctor Valdés, Amir Sadik, Julian Schrittwieser, Keith Anderson, Sarah York, Max Cant, Adam Cain, Adrian Bolton, Stephen Gaffney, Helen King, Demis Hassabis, Shane Legg, and Stig Petersen. Deepmind lab. _arXiv preprint arXiv:1612.03801_ , 2016. 

- Marc G Bellemare, Yavar Naddaf, Joel Veness, and Michael Bowling. The arcade learning environment: An evaluation platform for general agents. _Journal of artificial intelligence research_ , 47: 253–279, 2013. 

- Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, Thomas Unterthiner, Daniel Keysers, Skanda Koppula, Fangyu Liu, Adam Grycner, Alexey A. Gritsenko, Neil Houlsby, Manoj Kumar, Keran Rong, Julian Eisenschlos, Rishabh Kabra, Matthias Bauer, Matko Bosnjak, Xi Chen, Matthias Minderer, Paul Voigtlaender, Ioana Bica, Ivana Balazevic, Joan Puigcerver, Pinelopi Papalampidi, Olivier J. Hénaff, Xi Xiong, Radu Soricut, Jeremiah Harmsen, and Xiaohua Zhai. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Lukas Biewald. Experiment tracking with weights and biases, 2020. URL https://www.wandb. com/. Software available from wandb.com. 

- Mikolaj Binkowski, Danica J. Sutherland, Michael Arbel, and Arthur Gretton. Demystifying MMD gans. In _6th International Conference on Learning Representations, ICLR 2018, Vancouver, BC, Canada, April 30 - May 3, 2018, Conference Track Proceedings_ , 2018. 

- Steven Bird and Edward Loper. NLTK: The natural language toolkit. In _Proceedings of the ACL Interactive Poster and Demonstration Sessions_ , pp. 214–217, Barcelona, Spain, July 2004. Association for Computational Linguistics. 

- Zesen Cheng Zhiqiang Hu Yuqian Yuan Guanzheng Chen Sicong Leng Yuming Jiang Hang Zhang Xin Li Peng Jin Wenqi Zhang Fan Wang Lidong Bing Deli Zhao Boqiang Zhang, Kehan Li. Videollama 3: Frontier multimodal foundation models for image and video understanding. _arXiv preprint arXiv:2501.13106_ , 2025. URL https://arxiv.org/abs/2501.13106. 

G. Bradski. The OpenCV Library. _Dr. Dobb’s Journal of Software Tools_ , 2000. 

- Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. _Advances in neural information processing systems_ , 33:1877–1901, 2020. 

- Jake Bruce, Michael D. Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, Yusuf Aytar, Sarah Bechtle, Feryal M. P. Behbahani, Stephanie C. Y. Chan, Nicolas Heess, Lucy Gonzalez, Simon Osindero, Sherjil Ozair, Scott E. Reed, Jingwei Zhang, Konrad Zolna, Jeff Clune, Nando de Freitas, Satinder Singh, and Tim Rocktäschel. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

- João Carreira and Andrew Zisserman. Quo vadis, action recognition? A new model and the kinetics dataset. In _2017 IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2017, Honolulu, HI, USA, July 21-26, 2017_ , pp. 4724–4733. IEEE Computer Society, 2017. 

- Soravit Changpinyo, Doron Kukliansky, Idan Szpektor, Xi Chen, Nan Ding, and Radu Soricut. All you may need for VQA are image captions. _arXiv preprint arXiv:2205.01883_ , 2022. 

- Dongping Chen, Ruoxi Chen, Shilin Zhang, Yaochen Wang, Yinuo Liu, Huichi Zhou, Qihui Zhang, Yao Wan, Pan Zhou, and Lichao Sun. Mllm-as-a-judge: Assessing multimodal llm-as-a-judge with vision-language benchmark. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Jingye Chen, Yuzhong Zhao, Yupan Huang, Lei Cui, Li Dong, Tengchao Lv, Qifeng Chen, and Furu Wei. Model as a game: On numerical and spatial consistency for generative games. _arXiv preprint arXiv:2503.21172_ , 2025. 

11 

Preprint 

- Wenhu Chen, Hexiang Hu, Xi Chen, Pat Verga, and William Cohen. Murag: Multimodal retrievalaugmented generator for open question answering over images and text. In _Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing_ , pp. 5558–5570, 2022a. 

- Xi Chen, Xiao Wang, Soravit Changpinyo, A. J. Piergiovanni, Piotr Padlewski, Daniel Salz, Sebastian Goodman, Adam Grycner, Basil Mustafa, Lucas Beyer, Alexander Kolesnikov, Joan Puigcerver, Nan Ding, Keran Rong, Hassan Akbari, Gaurav Mishra, Linting Xue, Ashish V. Thapliyal, James Bradbury, and Weicheng Kuo. Pali: A jointly-scaled multilingual language-image model. _arXiv preprint arXiv:2209.06794_ , 2022b. 

- Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, Siamak Shakeri, Mostafa Dehghani, Daniel Salz, Mario Lucic, Michael Tschannen, Arsha Nagrani, Hexiang Hu, Mandar Joshi, Bo Pang, Ceslee Montgomery, Paulina Pietrzyk, Marvin Ritter, A. J. Piergiovanni, Matthias Minderer, Filip Pavetic, Austin Waters, Gang Li, Ibrahim Alabdulmohsin, Lucas Beyer, Julien Amelot, Kenton Lee, Andreas Peter Steiner, Yang Li, Daniel Keysers, Anurag Arnab, Yuanzhong Xu, Keran Rong, Alexander Kolesnikov, Mojtaba Seyedhosseini, Anelia Angelova, Xiaohua Zhai, Neil Houlsby, and Radu Soricut. Pali-x: On scaling up a multilingual vision and language model. _arXiv preprint arXiv:2305.18565_ , 2023. 

- Yukang Chen, Shengju Qian, Haotian Tang, Xin Lai, Zhijian Liu, Song Han, and Jiaya Jia. Longlora: Efficient fine-tuning of long-context large language models. In _The Twelfth International Conference on Learning Representations_ . 

- Matt Deitke, Christopher Clark, Sangho Lee, Rohun Tripathi, Yue Yang, Jae Sung Park, Mohammadreza Salehi, Niklas Muennighoff, Kyle Lo, Luca Soldaini, Jiasen Lu, Taira Anderson, Erin Bransom, Kiana Ehsani, Huong Ngo, Yen-Sung Chen, Ajay Patel, Mark Yatskar, Chris CallisonBurch, Andrew Head, Rose Hendrix, Favyen Bastani, Eli VanderBilt, Nathan Lambert, Yvonne Chou, Arnavi Chheda, Jenna Sparks, Sam Skjonsberg, Michael Schmitz, Aaron Sarnat, Byron Bischoff, Pete Walsh, Chris Newell, Piper Wolters, Tanmay Gupta, Kuo-Hao Zeng, Jon Borchardt, Dirk Groeneveld, Jen Dumas, Crystal Nam, Sophie Lebrecht, Caitlin Wittlif, Carissa Schoenick, Oscar Michel, Ranjay Krishna, Luca Weihs, Noah A. Smith, Hannaneh Hajishirzi, Ross B. Girshick, Ali Farhadi, and Aniruddha Kembhavi. Molmo and pixmo: Open weights and open data for state-of-the-art multimodal models. _arXiv preprint arXiv:2409.17146_ , 2024. 

- Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. Qlora: Efficient finetuning of quantized llms. _Advances in neural information processing systems_ , 36:10088–10115, 2023. 

- Sam Devlin, Raluca Georgescu, Ida Momennejad, Jaroslaw Rzepecki, Evelyn Zuniga, Gavin Costello, Guy Leroy, Ali Shaw, and Katja Hofmann. Navigation turing test (ntt): Learning to evaluate human-like navigation. In _International Conference on Machine Learning_ , pp. 2644–2653. PMLR, 2021. 

- Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby. An image is worth 16x16 words: Transformers for image recognition at scale. In _9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021_ , 2021. 

- Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine, Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch, and Pete Florence. PaLM-E: An embodied multimodal language model. In _International Conference on Machine Learning_ , pp. 8469–8488. PMLR, 2023. 

- Yilun Du, Sherry Yang, Pete Florence, Fei Xia, Ayzaan Wahid, Brian Ichter, Pierre Sermanet, Tianhe Yu, Pieter Abbeel, Joshua B. Tenenbaum, Leslie Pack Kaelbling, Andy Zeng, and Jonathan Tompson. Video language planning. In _The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024_ . 

12 

Preprint 

- Patrick Esser, Robin Rombach, and Bjorn Ommer. Taming transformers for high-resolution image synthesis. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 12873–12883, 2021. 

- Shenyuan Gao, Siyuan Zhou, Yilun Du, Jun Zhang, and Chuang Gan. Adaworld: Learning adaptable world models with latent actions. _arXiv preprint arXiv:2503.18938_ , 2025. 

- Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron C. Courville, and Yoshua Bengio. Generative adversarial nets. In Zoubin Ghahramani, Max Welling, Corinna Cortes, Neil D. Lawrence, and Kilian Q. Weinberger (eds.), _Advances in Neural Information Processing Systems 27: Annual Conference on Neural Information Processing Systems 2014, December 8-13 2014, Montreal, Quebec, Canada_ , pp. 2672–2680, 2014. 

- Junliang Guo, Yang Ye, Tianyu He, Haoyu Wu, Yushu Jiang, Tim Pearce, and Jiang Bian. Mineworld: a real-time and open-source interactive world model on minecraft. _arXiv preprint arXiv:2504.08388_ , 2025. 

- William H Guss, Mario Ynocente Castro, Sam Devlin, Brandon Houghton, Noboru Sean Kuno, Crissman Loomis, Stephanie Milani, Sharada Mohanty, Keisuke Nakata, Ruslan Salakhutdinov, et al. The minerl 2020 competition on sample efficient reinforcement learning using human priors. _arXiv preprint arXiv:2101.11071_ , 2021. 

- David Ha and Jürgen Schmidhuber. Recurrent world models facilitate policy evolution. _Advances in Neural Information Processing Systems_ , 31:2451–2463, 2018. 

- Danijar Hafner, Timothy P Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. In _International Conference on Learning Representations_ . 

- Danijar Hafner, Timothy P. Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020_ , 2020. 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse control tasks through world models. _Nature_ , pp. 1–7, 2025. 

- Zeyu Han, Chao Gao, Jinyang Liu, Jeff Zhang, and Sai Qian Zhang. Parameter-efficient fine-tuning for large models: A comprehensive survey. _Transactions on Machine Learning Research_ , 2024. 

- Charles R. Harris, K. Jarrod Millman, Stéfan J. van der Walt, Ralf Gommers, Pauli Virtanen, David Cournapeau, Eric Wieser, Julian Taylor, Sebastian Berg, Nathaniel J. Smith, Robert Kern, Matti Picus, Stephan Hoyer, Marten H. van Kerkwijk, Matthew Brett, Allan Haldane, Jaime Fernández del Río, Mark Wiebe, Pearu Peterson, Pierre Gérard-Marchant, Kevin Sheppard, Tyler Reddy, Warren Weckesser, Hameer Abbasi, Christoph Gohlke, and Travis E. Oliphant. Array programming with NumPy. _Nature_ , 585(7825):357–362, September 2020. 

- Mariya Hendriksen, Maurits Bleeker, Svitlana Vakulenko, Nanne Van Noord, Ernst Kuiper, and Maarten De Rijke. Extending clip for category-to-image retrieval in e-commerce. In _European Conference on Information Retrieval_ , pp. 289–303. Springer, 2022. 

- Dan Hendrycks and Kevin Gimpel. Gaussian error linear units (gelus). _arXiv preprint arXiv:1606.08415_ , 2016. 

- Jack Hessel, Ari Holtzman, Maxwell Forbes, Ronan Le Bras, and Yejin Choi. Clipscore: A referencefree evaluation metric for image captioning. In _Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing_ , pp. 7514–7528, 2021. 

- Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter. Gans trained by a two time-scale update rule converge to a local nash equilibrium. In Isabelle Guyon, Ulrike von Luxburg, Samy Bengio, Hanna M. Wallach, Rob Fergus, S. V. N. Vishwanathan, and Roman Garnett (eds.), _Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, USA_ , pp. 6626–6637, 2017. 

13 

Preprint 

- Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023a. 

- Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. In _The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022_ , 2022. 

- Ziniu Hu, Ahmet Iscen, Chen Sun, Zirui Wang, Kai-Wei Chang, Yizhou Sun, Cordelia Schmid, David A Ross, and Alireza Fathi. Reveal: Retrieval-augmented visual-language pre-training with multi-source multimodal knowledge memory. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 23369–23379, 2023b. 

- Ziqi Huang, Yinan He, Jiashuo Yu, Fan Zhang, Chenyang Si, Yuming Jiang, Yuanhan Zhang, Tianxing Wu, Qingyang Jin, Nattapol Chanpaisit, et al. Vbench: Comprehensive benchmark suite for video generative models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 21807–21818, 2024. 

- John D Hunter. Matplotlib: A 2d graphics environment. _Computing in science & engineering_ , 9(03): 90–95, 2007. 

- Sadeep Jayasumana, Srikumar Ramalingam, Andreas Veit, Daniel Glasner, Ayan Chakrabarti, and Sanjiv Kumar. Rethinking FID: Towards a better evaluation metric for image generation. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2024, Seattle, WA, USA, June 16-22, 2024_ , pp. 9307–9315. IEEE, 2024. 

- Woojeong Jin, Yu Cheng, Yelong Shen, Weizhu Chen, and Xiang Ren. A good prompt is worth millions of parameters: Low-resource prompt-based learning for vision-language models. In _Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pp. 2763–2775, 2022. 

- Lukasz Kaiser, Mohammad Babaeizadeh, Piotr Milos, Blazej Osinski, Roy H. Campbell, Konrad Czechowski, Dumitru Erhan, Chelsea Finn, Piotr Kozakowski, Sergey Levine, Afroz Mohiuddin, Ryan Sepassi, George Tucker, and Henryk Michalewski. Model based reinforcement learning for atari. _ICLR_ , 1:2, 2020. 

- Anssi Kanervisto, Christian Scheller, and Ville Hautamäki. Action space shaping in deep reinforcement learning. In _2020 IEEE conference on games (CoG)_ , pp. 479–486. IEEE, 2020. 

- Anssi Kanervisto, David Bignell, Linda Yilin Wen, Martin Grayson, Raluca Georgescu, Sergio Valcarcel Macua, Shan Zheng Tan, Tabish Rashid, Tim Pearce, Yuhan Cao, Abdelhak Lemkhenter, Chentian Jiang, Gavin Costello, Gunshi Gupta, Marko Tot, Shu Ishida, Tarun Gupta, Udit Arora, Ryen W. White, Sam Devlin, Cecily Morrison, and Katja Hofmann. World and human action models towards gameplay ideation. _Nature_ , 638(8051):656–663, 2025. 

- Tero Karras, Samuli Laine, and Timo Aila. A style-based generator architecture for generative adversarial networks. In _IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2019, Long Beach, CA, USA, June 16-20, 2019_ , pp. 4401–4410. Computer Vision Foundation / IEEE, 2019. 

- Taku Kudo and John Richardson. SentencePiece: A simple and language independent subword tokenizer and detokenizer for neural text processing. In Eduardo Blanco and Wei Lu (eds.), _Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, EMNLP 2018: System Demonstrations, Brussels, Belgium, October 31 - November 4, 2018_ , pp. 66–71. Association for Computational Linguistics, 2018. 

- Seongyun Lee, Seungone Kim, Sue Park, Geewook Kim, and Minjoon Seo. Prometheus-vision: Vision-language model as a judge for fine-grained evaluation. In _Findings of the Association for Computational Linguistics ACL 2024_ , pp. 11286–11315, 2024. 

- Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. Retrieval-augmented generation for knowledge-intensive nlp tasks. _Advances in neural information processing systems_ , 33: 9459–9474, 2020. 

14 

Preprint 

- Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _International conference on machine learning_ , pp. 19730–19742. PMLR, 2023. 

- Mingxiang Liao, Qixiang Ye, Wangmeng Zuo, Fang Wan, Tianyu Wang, Yuzhong Zhao, Jingdong Wang, Xinyu Zhang, et al. Evaluation of text-to-video generation models: A dynamics perspective. _Advances in Neural Information Processing Systems_ , 37:109790–109816, 2024. 

- Zhiqiu Lin, Deepak Pathak, Baiqi Li, Jiayao Li, Xide Xia, Graham Neubig, Pengchuan Zhang, and Deva Ramanan. Evaluating text-to-visual generation with image-to-text generation. In _European Conference on Computer Vision_ , pp. 366–384. Springer, 2024. 

- Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 26296–26306, 2024a. 

- Shih-Yang Liu, Chien-Yi Wang, Hongxu Yin, Pavlo Molchanov, Yu-Chiang Frank Wang, KwangTing Cheng, and Min-Hung Chen. Dora: Weight-decomposed low-rank adaptation. In _Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024_ . 

- Yaofang Liu, Xiaodong Cun, Xuebo Liu, Xintao Wang, Yong Zhang, Haoxin Chen, Yang Liu, Tieyong Zeng, Raymond Chan, and Ying Shan. Evalcrafter: Benchmarking and evaluating large video generation models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 22139–22149, 2024b. 

- Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In _7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019_ , 2019. 

- Ilya Loshchilov and Frank Hutter. Sgdr: Stochastic gradient descent with warm restarts. In _International Conference on Learning Representations_ , 2022. 

- Gen Luo, Yiyi Zhou, Tianhe Ren, Shengxin Chen, Xiaoshuai Sun, and Rongrong Ji. Cheap and quick: Efficient vision-language instruction tuning for large language models. _Advances in neural information processing systems (NeurIPS)_ , 2023. 

- Oscar Mañas, Benno Krojer, and Aishwarya Agrawal. Improving automatic vqa evaluation using large language models. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pp. 4171–4179, 2024. 

- Sourab Mangrulkar, Sylvain Gugger, Lysandre Debut, Younes Belkada, Sayak Paul, and Benjamin Bossan. Peft: State-of-the-art parameter-efficient fine-tuning methods, 2022. URL https: //github.com/huggingface/peft. 

- Brandon McKinzie, Zhe Gan, Jean-Philippe Fauconnier, Sam Dodge, Bowen Zhang, Philipp Dufter, Dhruti Shah, Xianzhi Du, Futang Peng, Floris Weers, Anton Belyi, Haotian Zhang, Karanjeet Singh, Doug Kang, Hongyu Hè, Max Schwarzer, Tom Gunter, Xiang Kong, Aonan Zhang, Jianyu Wang, Chong Wang, Nan Du, Tao Lei, Sam Wiseman, Mark Lee, Zirui Wang, Ruoming Pang, Peter Grasch, Alexander Toshev, and Yinfei Yang. MM1: Methods, analysis and insights from multimodal LLM pre-training. In _European Conference on Computer Vision_ , pp. 304–323. Springer, 2024. 

- Thomas Mesnard, Cassidy Hardin, Robert Dadashi, Surya Bhupatiraju, Shreya Pathak, Laurent Sifre, Morgane Rivière, Mihir Sanjay Kale, Juliette Love, Pouya Tafti, Léonard Hussenot, Aakanksha Chowdhery, Adam Roberts, Aditya Barua, Alex Botev, Alex Castro-Ros, Ambrose Slone, Amélie Héliou, Andrea Tacchetti, Anna Bulanova, Antonia Paterson, Beth Tsai, Bobak Shahriari, Charline Le Lan, Christopher A. Choquette-Choo, Clément Crepy, Daniel Cer, Daphne Ippolito, David Reid, Elena Buchatskaya, Eric Ni, Eric Noland, Geng Yan, George Tucker, George-Cristian Muraru, Grigory Rozhdestvenskiy, Henryk Michalewski, Ian Tenney, Ivan Grishchenko, Jacob Austin, James Keeling, Jane Labanowski, Jean-Baptiste Lespiau, Jeff Stanway, Jenny Brennan, Jeremy Chen, Johan Ferret, Justin Chiu, and et al. Gemma: Open models based on gemini research and technology. _arXiv preprint arXiv:2403.08295_ , 2024. 

15 

Preprint 

- Vincent Micheli, Eloi Alonso, and François Fleuret. Transformers are sample-efficient world models. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- Atsuyuki Miyai, Qing Yu, Go Irie, and Kiyoharu Aizawa. Locoop: Few-shot out-of-distribution detection via prompt learning. _Advances in Neural Information Processing Systems_ , 36:76298– 76310, 2023. 

- Ivona Najdenkoska, Xiantong Zhen, and Marcel Worring. Meta learning to bridge vision and language models for multimodal few-shot learning. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ , 2023. 

- Jingcheng Ni, Yuxin Guo, Yichen Liu, Rui Chen, Lewei Lu, and Zehuan Wu. Maskgwm: A generalizable driving world model with video mask reconstruction. _arXiv preprint arXiv:2502.11663_ , 2025. 

- Jack Parker-Holder, Philip Ball, Jake Bruce, Vibhavari Dasagi, Kristian Holsheimer, Christos Kaplanis, Alexandre Moufarek, Guy Scully, Jeremy Shar, Jimmy Shi, Stephen Spencer, Jessica Yung, Michael Dennis, Sultan Kenjeyev, Shangbang Long, Vlad Mnih, Harris Chan, Maxime Gazeau, Bonnie Li, Fabio Pardo, Luyu Wang, Lei Zhang, Frederic Besse, Tim Harley, Anna Mitenkova, Jane Wang, Jeff Clune, Demis Hassabis, Raia Hadsell, Adrian Bolton, Satinder Singh, and Tim Rocktäschel. Genie 2: A large-scale foundation world model, 2024. URL https://deepmind.google/discover/blog/ genie-2-a-large-scale-foundation-world-model/. Accessed: 20 March 2025. 

- Tim Pearce, Tabish Rashid, Dave Bignell, Raluca Georgescu, Sam Devlin, and Katja Hofmann. Scaling laws for pre-training agents and world models. In _Proceedings of the 42nd International Conference on Machine Learning (ICML)_ , 2025. 

- AJ Piergiovanni, Weicheng Kuo, and Anelia Angelova. Pre-training image-language transformers for open-vocabulary tasks. _arXiv preprint arXiv:2209.04372_ , 2022. 

- Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. Language models are unsupervised multitask learners. _OpenAI blog_ , 1(8):9, 2019. 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision. _Proceedings of the International Conference on Machine Learning (ICML)_ , 2021. 

- Morgane Rivière, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhupatiraju, Léonard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ramé, Johan Ferret, Peter Liu, Pouya Tafti, Abe Friesen, Michelle Casbon, Sabela Ramos, Ravin Kumar, Charline Le Lan, Sammy Jerome, Anton Tsitsulin, Nino Vieillard, Piotr Stanczyk, Sertan Girgin, Nikola Momchev, Matt Hoffman, Shantanu Thakoor, Jean-Bastien Grill, Behnam Neyshabur, Olivier Bachem, Alanna Walton, Aliaksei Severyn, Alicia Parrish, Aliya Ahmad, Allen Hutchison, Alvin Abdagic, Amanda Carl, Amy Shen, Andy Brock, Andy Coenen, Anthony Laforge, Antonia Paterson, Ben Bastian, Bilal Piot, Bo Wu, Brandon Royal, Charlie Chen, Chintu Kumar, Chris Perry, Chris Welty, Christopher A. Choquette-Choo, Danila Sinopalnikov, David Weinberger, Dimple Vijaykumar, Dominika Rogozinska, Dustin Herbison, Elisa Bandy, Emma Wang, Eric Noland, Erica Moreira, Evan Senter, Evgenii Eltyshev, Francesco Visin, Gabriel Rasskin, Gary Wei, Glenn Cameron, Gus Martins, Hadi Hashemi, Hanna Klimczak-Plucinska, Harleen Batra, Harsh Dhand, Ivan Nardini, Jacinda Mein, Jack Zhou, James Svensson, Jeff Stanway, Jetha Chan, Jin Peng Zhou, Joana Carrasqueira, Joana Iljazi, Jocelyn Becker, Joe Fernandez, Joost van Amersfoort, Josh Gordon, Josh Lipschultz, Josh Newlan, Ju-yeong Ji, Kareem Mohamed, Kartikeya Badola, Kat Black, Katie Millican, Keelin McDonell, Kelvin Nguyen, Kiranbir Sodhia, Kish Greene, Lars Lowe Sjösund, Lauren Usui, Laurent Sifre, Lena Heuermann, Leticia Lago, and Lilly McNealus. Gemma 2: Improving open language models at a practical size. _arXiv preprint arXiv:2408.00118_ , 2024. 

- Lloyd Russell, Anthony Hu, Lorenzo Bertoni, George Fedoseev, Jamie Shotton, Elahe Arani, and Gianluca Corrado. Gaia-2: A controllable multi-view generative world model for autonomous driving. _arXiv preprint arXiv:2503.20523_ , 2025. 

16 

Preprint 

- Tim Salimans, Ian J. Goodfellow, Wojciech Zaremba, Vicki Cheung, Alec Radford, and Xi Chen. Improved techniques for training gans. In Daniel D. Lee, Masashi Sugiyama, Ulrike von Luxburg, Isabelle Guyon, and Roman Garnett (eds.), _Advances in Neural Information Processing Systems 29: Annual Conference on Neural Information Processing Systems 2016, December 5-10, 2016, Barcelona, Spain_ , pp. 2226–2234, 2016. 

- Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, Timothy P. Lillicrap, and David Silver. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, 2020. 

- Piyush Sharma, Nan Ding, Sebastian Goodman, and Radu Soricut. Conceptual captions: A cleaned, hypernymed, image alt-text dataset for automatic image captioning. In _Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pp. 2556–2565, 2018. 

- Sugandha Sharma, Guy Davidson, Khimya Khetarpal, Anssi Kanervisto, Udit Arora, Katja Hofmann, and Ida Momennejad. Toward human-ai alignment in large-scale multi-player games. In _ACL 2024 Worldplay Workshop_ , 2024. 

- Haoyu Song, Li Dong, Weinan Zhang, Ting Liu, and Furu Wei. Clip models are few-shot learners: Empirical studies on vqa and visual entailment. In _Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pp. 6088–6100, 2022. 

- Krishna Srinivasan, Karthik Raman, Jiecao Chen, Michael Bendersky, and Marc Najork. Wit: Wikipedia-based image text dataset for multimodal multilingual machine learning. In _Proceedings of the 44th international ACM SIGIR conference on research and development in information retrieval_ , pp. 2443–2449, 2021. 

- Andreas Steiner, André Susano Pinto, Michael Tschannen, Daniel Keysers, Xiao Wang, Yonatan Bitton, Alexey A. Gritsenko, Matthias Minderer, Anthony Sherbondy, Shangbang Long, Siyang Qin, R. Reeve Ingle, Emanuele Bugliarello, Sahar Kazemzadeh, Thomas Mesnard, Ibrahim Alabdulmohsin, Lucas Beyer, and Xiaohua Zhai. Paligemma 2: A family of versatile vlms for transfer. _arXiv preprint arXiv:2412.03555_ , 2024. 

- Richard S Sutton. Dyna, an integrated architecture for learning, planning, and reacting. _ACM Sigart Bulletin_ , 2(4):160–163, 1991. 

- Suramya Tomar. Converting video formats with ffmpeg. _Linux Journal_ , 2006(146):10, 2006. 

- Marko Tot, Shu Ishida, Abdelhak Lemkhenter, David Bignell, Pallavi Choudhury, Chris Lovett, Luis França, Matheus Ribeiro Furtado de Mendonça, Tarun Gupta, Darren Gehring, et al. Adapting a world model for trajectory following in a 3d game. In _ICLR 2025 Workshop on World Models_ , 2025. 

- Maria Tsimpoukelli, Jacob L Menick, Serkan Cabi, SM Eslami, Oriol Vinyals, and Felix Hill. Multimodal few-shot learning with frozen language models. _Advances in Neural Information Processing Systems_ , 34:200–212, 2021. 

- P Umesh. Image processing in python. _CSI Communications_ , 23, 2012. 

- Thomas Unterthiner, Sjoerd van Steenkiste, Karol Kurach, Raphaël Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric and challenges. _arXiv preprint arXiv:1812.01717_ , 2018. 

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Yang Fan, Kai Dang, Mengfei Du, Xuancheng Ren, Rui Men, Dayiheng Liu, Chang Zhou, Jingren Zhou, and Junyang Lin. Qwen2-VL: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 

17 

Preprint 

- Zhou Wang, Alan C Bovik, Hamid R Sheikh, and Eero P Simoncelli. Image quality assessment: from error visibility to structural similarity. _IEEE transactions on image processing_ , 13(4):600–612, 2004. 

- Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, and Jamie Brew. Huggingface’s transformers: State-of-the-art natural language processing. _arXiv preprint arXiv:1910.03771_ , 2019. 

- Chenfei Wu, Lun Huang, Qianxi Zhang, Binyang Li, Lei Ji, Fan Yang, Guillermo Sapiro, and Nan Duan. Godiva: Generating open-domain videos from natural descriptions. _arXiv preprint arXiv:2104.14806_ , 2021. 

- Mingrui Wu, Xinyue Cai, Jiayi Ji, Jiale Li, Oucheng Huang, Gen Luo, Hao Fei, Guannan Jiang, Xiaoshuai Sun, and Rongrong Ji. Controlmllm: Training-free visual prompt learning for multimodal large language models. _Advances in Neural Information Processing Systems_ , 37:45206–45234, 2024a. 

- Xun Wu, Shaohan Huang, and Furu Wei. Mixture of lora experts. In _ICLR_ , 2024b. 

- Yuhui Xu, Lingxi Xie, Xiaotao Gu, Xin Chen, Heng Chang, Hengheng Zhang, Zhengsu Chen, Xiaopeng Zhang, and Qi Tian. Qa-lora: Quantization-aware low-rank adaptation of large language models. In _The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024_ , 2024. 

- Sherry Yang, Yilun Du, Seyed Kamyar Seyed Ghasemipour, Jonathan Tompson, Leslie Pack Kaelbling, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. In _The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024_ , 2024. 

- Peng Ye, Yongqi Huang, Chongjun Tu, Minglei Li, Tao Chen, Tong He, and Wanli Ouyang. Partial fine-tuning: A successor to full fine-tuning for vision transformers. _arXiv preprint arXiv:2312.15681_ , 2023. 

- Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 11975–11986, 2023. 

- Bingchen Zhao, Haoqin Tu, Chen Wei, Jieru Mei, and Cihang Xie. Tuning layernorm in attention: Towards efficient multi-modal llm finetuning. In _ICLR_ , 2024. 

- Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging llm-as-a-judge with mt-bench and chatbot arena. _Advances in neural information processing systems_ , 36:46595–46623, 2023. 

- Sharon Zhou, Mitchell L. Gordon, Ranjay Krishna, Austin Narcomey, Li Fei-Fei, and Michael S. Bernstein. HYPE: A benchmark for human eye perceptual evaluation of generative models. In Hanna M. Wallach, Hugo Larochelle, Alina Beygelzimer, Florence d’Alché-Buc, Emily B. Fox, and Roman Garnett (eds.), _Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada_ , pp. 3444–3456, 2019. 

- Yiwei Zhou, Xiaobo Xia, Zhiwei Lin, Bo Han, and Tongliang Liu. Few-shot adversarial prompt learning on vision-language models. _Advances in Neural Information Processing Systems_ , 37: 3122–3156, 2024. 

18 

Preprint 

# ADAPTING VISION-LANGUAGE MODELS FOR EVALUATING WORLD MODELS 

APPENDIX 

## TABLE OF CONTENTS 

|**A **|**Bro**|**ader Impact**|**20**|
|---|---|---|---|
|**B**|**Rep**|**roducibility Statement**|**20**|
|**C**|**UNI**|**VERSE: Additional Details**|**21**|
||C.1|Implementation Overview<br>. . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>21|
||C.2|Adaptation to New Domains . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>21|
|**D **|**Dat**|**aset**|**22**|
||D.1|Construction Process . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>22|
|**E**|**Exp**|**erimental Details**|**24**|
||E.1|Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>24|
||E.2|Evaluation Metrics<br>. . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>27|
||E.3|Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>28|
|**F**|**Hum**|**an Annotation Study**|**29**|
||F.1|Study Design . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>30|
||F.2|Evaluation Metrics<br>. . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>35|
||F.3|Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>36|
|**G **|**Sup**|**plementary Experimental Results**|**37**|
||G.1|GPT-5 Performance . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>37|
||G.2|Zero-Shot Performance of PaliGemma Models<br>. . . . . . . . . .|. . . . . . . . .<br>37|
||G.3|CLIPScore Comparisons . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>37|
||G.4|Low-Rank Adaptation Comparisons . . . . . . . . . . . . . . . .|. . . . . . . . .<br>40|
|**H **|**Com**|**parison with Existing Evaluation Baselines**|**41**|
||H.1|Comparison with FVD . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>41|
||H.2|Correlation with VBench Metrics . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>42|


19 

Preprint 

## A BROADER IMPACT 

As world models become integral to simulation, planning, and decision-making in interactive environments, evaluation remains a key bottleneck for both research progress and safe deployment. We address this challenge by introducing a unified, sample-efficient framework for evaluating world model rollouts using adapted VLMs, designed for fine-grained, temporally grounded, and semantically coherent assessment. 

This capability has direct implications for high-impact domains such as neural game engines (Kanervisto et al., 2025; Guo et al., 2025; Gao et al., 2025; Chen et al., 2025), embodied AI (Du et al.; Yang et al., 2024), and autonomous driving (Russell et al., 2025; Hu et al., 2023a; Ni et al., 2025), where world models simulate environment dynamics and support downstream control and generalization. In such contexts, precise and interpretable evaluation is critical not only for benchmarking, but also for diagnosing failure modes and ensuring alignment with intended behaviors. 

By reducing dependence on human annotation and task-specific fine-tuning, UNIVERSE offers a scalable alternative that lowers the computational and environmental costs of rollout evaluation. However, reliance on automated evaluators introduces risks: adapted VLMs may inherit biases from pretraining, struggle under distributional shift, or yield unreliable judgments in edge cases. These risks are amplified in safety-critical settings, where miscalibrated evaluations can propagate downstream errors. 

We therefore advocate for cautious deployment, accompanied by human oversight, rigorous validation, and transparent reporting. While UNIVERSE advances the automation of world model evaluation, it must be situated within evaluation pipelines that foreground robustness, interpretability, and accountability. 

## B REPRODUCIBILITY STATEMENT 

To support reproducibility and facilitate future research, we provide detailed instructions for reproducing all main experiments. Detailed descriptions of model architectures, training procedures, and dataset construction are provided in Section 4 and Appendix E. A high-level overview of the overall implementation framework is included in Appendix C.1. All experiments have been repeated for three runs. Plots and tables with quantitative results show the standard deviation across these runs. 

_Use of Existing Assets._ We experiment with a range of open-weight VLMs, including three PaliGemma variants (version 1 (3B) (Beyer et al., 2024) and version 2 (3B and 10B) (Steiner et al., 2024)), VideoLLaMA3 (2B, 7B) (Boqiang Zhang, 2025), and CLIP (Radford et al., 2021) with the following vision encoder configurations: ViT-B/32, ViT-B/16, ViT-L/14, and ViT-L/14 with 336 _×_ 336 resolution. UNIVERSE is built on top of PaliGemma v2 (3B), using publicly released checkpoints for initialization. Further architectural and implementation details are provided in Appendix E.1. For our software stack, we use Matplotlib (Hunter, 2007) for plotting, NumPy (Harris et al., 2020) for data handling, openCV (Bradski, 2000), FFmpeg (Tomar, 2006) and PIL (Umesh, 2012) for video and image processing, and NLTK (Bird & Loper, 2004) for text processing. Parameter-efficient fine-tuning is implemented using the PEFT library (Mangrulkar et al., 2022). We log our experiments using Weights and Biases (Biewald, 2020). 

_Use of Large Language Models._ Portions of the manuscript were polished with the assistance of large language models (LLMs). The use of LLMs was limited to only improving readability and style; all ideas, and experimental designs were developed by the authors. 

_Compute Resources._ All experiments were conducted using NVIDIA A100 GPUs (40GB memory) on an internal compute cluster. Each model was trained and/or evaluated using 8 GPUs. The compute breakdown is as follows: zero-shot evaluation experiments consumed approximately 136 GPU-days; baseline fine-tuning experiments required around 864 GPU-days; analysis experiments contributed the bulk of usage, totaling 2,554 GPU-days. Human evaluation experiments—including rollout generation and response annotation using UNIVERSE—incurred an additional 1.125 GPU-days. Additional compute was required for preliminary experiments, and failed runs not included in the final paper. These development activities accounted for an estimated 1,599 GPU-days. In total, all experiments amounted to approximately 5,153 GPU-days, equivalent to 14.12 GPU-years. 

20 

Preprint 

## C UNIVERSE: ADDITIONAL DETAILS 

### C.1 IMPLEMENTATION OVERVIEW 

This section outlines the implementation of UNIVERSE in Python, presented as high-level pseudocode. The system is structured around two main stages: (i) _Adaptation:_ fine-tuning a VLM on task-specific question-answer (QA) supervision derived from ground truth; (ii) _Evaluation:_ using the adapted model to assess new rollouts via structured, prompt-based recognition tasks. 

### **Adaptation Pipeline.** 

The adaptation stage can be implemented as two modules: AdaptationDatasetBuilder and VLMAdapter. 

**AdaptationDatasetBuilder.** This class constructs an adaptation dataset from raw ground truth data, initialized via load_ground_truth_data (see Section 3 and Appendix D). The core method, build, takes four arguments: alpha_task, which specifies the task mixture ratio; beta_format, which controls the distribution over QA prompt formats; context_length, which determines the number of frames per QA instance; and sampling_strategy, which defines how frames are sampled from rollouts. The builder first applies stratified_sample to select a subset of annotated samples that match the specified configuration. For each sample, it invokes _sample_visual_context to extract the relevant frames, and constructs a triplet consisting of frames, question, and answer. 

**VLMAdapter.** This class applies an adaptation strategy to a base VLM, passed via the base_vlm argument. Given an adaptation dataset adaptation_data, a tuning strategy specified by the strategy parameter, and a fixed number of training steps num_steps, the adapter trains the model by iteratively sampling a batch, computing the loss via compute_loss, and applying updates with update_model. 

### **Evaluation Pipeline.** 

The evaluation stage can be implemented via two additional modules: RolloutsGenerator and Universe. 

**RolloutsGenerator.** This component autoregressively samples rollout trajectories from a world model (textttworld_model). Given an initial observation o_initial and an action sequence a_seq, the rollout method generates a sequence of predicted observations by maintaining lists of past observations (o_lt) and actions (a_lt). At each timestep, it calls predict_next_observation to obtain the next predicted frame, appends it to the rollout sequence o_seq, and continues until timestamps is reached. This process produces a full trajectory simulating environment dynamics. 

**Universe.** This module serves as the inference engine of our framework. It wraps an adapted VLM passed via adapted_vlm. Given a generated rollout and an evaluation specification, the method evaluate_rollout constructs a prompt using generate_question, parameterized by a recognition target and complexity level. It then calls evaluate, which queries the VLM with the resulting rollout and question, returning the model’s answer. 

### C.2 ADAPTATION TO NEW DOMAINS 

To adapt UNIVERSE to a new environment, one could collect a small set of reference trajectories that provide ground-truth observations and actions for the evaluation dimensions of interest. Question and answer templates can then be instantiated from these ground-truth signals to construct a mixedsupervision adaptation dataset. 

In practice, two complementary routes exist for obtaining such reference data: (i) partnerships with game studios (as in the present work) provide high-quality logs and metadata but are resourceintensive, (ii) bootstrapping from publicly available gameplay video datasets, where generative models or synthetic data can supply initial labels. 

21 

Preprint 

At inference time, the evaluator could process rollouts by emitting natural-language responses along the specified dimensions. These outputs may be used either as structured feedback for improving the world model or mapped to numerical scores and aggregated into a single trajectory-level quality measure. Although our experiments use 14-frame inputs, this is a design choice rather than a conceptual constraint: the same procedure can extend to longer rollouts by increasing the visual context window or applying a sliding-window scheme over 14-frame segments. 

Overall, deploying UNIVERSE as a standalone evaluator would require: (i) a small adaptation dataset of reference trajectories with ground-truth labels, (ii) the task specification, and (iii) the lightweight fine-tuning recipe. Once adapted, the evaluator could provide dimension-wise assessments that can be aggregated or used as feedback in downstream world-model training. 

## D DATASET 

This section details the construction and release of the dataset used to adapt VLMs for fine-grained evaluation of world model rollouts. We curate a realistic, human-centered dataset derived from actual gameplay in a complex multi-agent environment. Designed to provide temporally grounded and semantically structured supervision, the dataset aligns with the downstream evaluation setting and supports adaptation to both action and character recognition tasks across all QA formats. We describe the data construction pipeline, QA generation process, and release format below. 

### D.1 CONSTRUCTION PROCESS 

The ground truth dataset for adapting the evaluator (see Section 3) was developed in collaboration with _Ninja Theory_ using human gameplay recordings from _Bleeding Edge_ , a 4v4 multiplayer combat game. Data use was governed by a formal agreement with the studio, and collection adhered to the game’s End User License Agreement (EULA). All protocols were approved by our Institutional Review Board (IRB), and personally identifiable information (PII) was removed prior to analysis. 

Each gameplay session is represented as a tuple _s_ = ( _v, c, m_ ), where _v_ is a high-resolution MP4 video (60 FPS), _c_ is the synchronized controller action log, and _m_ contains structured metadata (e.g., player roles, agent identities, action categories, and map context). The full set of gameplay sessions is denoted by _S_ = _{_ ( _vi, ci, mi_ ) _}_<sup>_|S|_</sup> _i_ =1<sup>.</sup> 

The dataset construction pipeline proceeds in three stages: 

- (i) _Preprocessing_ . We begin by filtering out corrupted applying or inactive sessions and synchronizes the video, controller logs, and metadata streams using internal game timestamps: _S_ valid = Preprocessing( _S_ ). Each valid session is segmented into nonoverlapping clips of fixed length _L_ = 14 frames, each paired with controller input and shared metadata; formally, for a session _s_ = ( _v, c, m_ ) _∈S_ valid, the segmentation produces Segment( _v, c, m, L_ ) = _{_ ( _f_<sup>(1:</sup><sup>_L_)</sup> _, c_<sup>(1:</sup><sup>_L_)</sup> _, m_ ) _}_ , where _f_<sup>(1:</sup><sup>_L_)</sup> denotes the sequence of frames, _c_<sup>(1:</sup><sup>_L_)</sup> the aligned controller inputs, and _m_ the associated metadata. The complete set of extracted clips across all valid sessions is defined as _V_ =<sup>�</sup> _s∈S_ valid<sup>Segment(</sup><sup>_s, L_), where</sup> each element _v ∈V_ is a triplet ( _f_<sup>(1:</sup><sup>_L_)</sup> _, c_<sup>(1:</sup><sup>_L_)</sup> _, m_ ) consisting of video frames, corresponding controller inputs, and metadata. 

- (ii) _Description Generation_ . Next, for each sequence of frames _f_<sup>(1:</sup><sup>_L_)</sup> _∈V_ , we use the associated control log _c_<sup>(1:</sup><sup>_L_)</sup> to extract action information and the metadata _m_ to obtain character-related attributes. These are combined to generate a structured natural language description via _d_ = Describe( _c_<sup>(1:</sup><sup>_L_)</sup> _, m_ ), where Describe is a rule-based procedure that transforms the logged actions and metadata into textual descriptions used for constructing the QA supervision. This yields a set of paired video–text examples: _Z_ = �( _f_<sup>(1:</sup><sup>_L_)</sup> _, d_ ) _| f_<sup>(1:</sup><sup>_L_)</sup> _∈V_ �. 

- (iii) _Question-Answer Pair Construction_ . Finally, we generate six QA pairs per clip, spanning two predefined tasks (AR and CR), each instantiated in three question formats: binary, multiple-choice, and open-ended. To enable this, we define task-specific answer spaces using GetAnswerSpace( _Z_ ), which returns _Y_ AR for action categories and _Y_ CR for character identities, based on all video–text pairs in _Z_ . For each clip, we extract the task-specific ground-truth answer from the corresponding description as _y_ = ExtractLabel( _d, t_ ), 

22 

Preprint 

where _t ∈{_ AR _,_ CR _}_ . Each QA format is constructed as follows: (i) _Binary_ : Two binary question-answer pairs are generated per instance using FormatBinaryPrompt. The positive question _Q_<sup>pos</sup> is constructed using the correct label _y ∈Y_<sup>(</sup><sup>_t_)</sup> and paired with the positive answer _A_<sup>pos</sup> . The negative question _Q_<sup>neg</sup> is constructed using an incorrect label _y_ ˜ _∼_ SampleDistractor( _Y_<sup>(</sup><sup>_t_)</sup> _\{y}_ ) and paired with the negative answer _A_<sup>neg</sup> . (ii) _Multiple-Choice_ : A question _Q_ is generated using the full set of candidate options, formatted via FormatOptions( _Yt_ ). The question is constructed with FormatMCPrompt( _t, O_ ) and paired with the correct answer _y ∈Yt_ . (iii) _Open-Ended_ : A free-form question _Q_ is generated using FormatOEPrompt( _t_ ), prompting the model to produce the correct label _y ∈Yt_ without access to predefined answer choices. 

The final dataset is represented as _D_ = _{_ ( _fi_<sup>(1:</sup><sup>_L_)</sup> _, QAi_ ) _}_<sup>_|D|_</sup> _i_ =1<sup>, where each</sup><sup>_f_(1:</sup><sup>_L_)is a video clip and</sup> _QA_ = _{_ ( _Qj, Aj_ ) _}_<sup>6</sup> _j_ =1<sup>is the associated set of question–answer pairs, covering all combinations of</sup> three question formats (binary, multiple-choice, open-ended) and two tasks (Action Recognition and Character Recognition). A detailed data pipeline is provided in Algorithm 1. 

23 

Preprint 

**Algorithm 1:** Dataset Construction Process **Procedure** DatasetCreation( _S, L_ ) **:** _S_ valid _←_ Preprocessing( _S_ ) _V ←∅_ **for** ( _v, c, m_ ) _∈Svalid_ **do** _Vs ←_ Segment( _v, c, m, L_ ) _V ←V ∪Vs Z ←∅_ **for** ( _f_<sup>(1:</sup><sup>_L_)</sup> _, c_<sup>(1:</sup><sup>_L_)</sup> _, m_ ) _∈V_ **do** _d ←_ Describe( _m, c_<sup>(1:</sup><sup>_L_)</sup> ) _Z ←Z ∪{_ ( _f_<sup>(1:</sup><sup>_L_)</sup> _, d_ ) _} D ←∅ Y_ AR _, Y_ CR _←_ GetAnswerSpace( _Z_ ) **for** ( _f_<sup>(1:</sup><sup>_L_)</sup> _, d_ ) _∈V_ **do** _QA ←_ GenerateQAPairs( _d, Y_ AR _, Y_ CR) **for** ( _Q, A_ ) _∈QA_ **do** _D ←D ∪{_ ( _f_<sup>(1:</sup><sup>_L_)</sup> _, Q, A_ ) _}_ **return** _D_ **Procedure** GenerateQAPairs( _d, YAR, YCR_ ) **:** _QA ←∅_ **for** _t ∈{AR, CR}_ **do** _y ←_ ExtractLabel( _d, t_ ) _QA_<sup>_pos_</sup> bin<sup>_, QAneg_</sup> bin<sup>_←_CreateBinaryQA(</sup><sup>_t, y_)</sup> _QA ←QA ∪{QA_<sup>pos</sup> bin<sup>_, QA_neg</sup> bin<sup>_}_</sup> _QA_ mc _←_ CreateMCQA( _t, y, Yt_ ) _QA ←QA ∪ QA_ mc _QA_ oe _←_ CreateOpenEndedQA( _t, y_ ) _QA ←QA ∪ QA_ oe **return** _Q_ **Procedure** CreateBinaryQA( _t, y_ ) **:** _y_ ˜ _←_ SampleDistractor( _Yt \ {y}_ ) _Q_<sup>_pos_</sup> _←_ FormatBinaryPrompt( _t, y_ ) _Q_<sup>_neg_</sup> _←_ FormatBinaryPrompt( _t,_ ˜ _y_ ) **return** _{_ ( _Q_<sup>_pos_</sup> _, A_<sup>_pos_</sup> ) _,_ ( _Qy_ ˜ _, A_<sup>_neg_</sup> ) _}_ **Procedure** CreateMCQA( _t, y, Yt_ ) **:** _O ←_ FormatOptions( _Yt_ ) _Q ←_ FormatMCPrompt( _t, O_ ) **return** _Q, y_ **Procedure** CreateOpenEndedQA( _t, y_ ) **:** _Q ←_ FormatOEPrompt( _t_ ) **return** _Q, y_ 

## E EXPERIMENTAL DETAILS 

In this section, we provide a detailed description of the dataset preparation process, model architecture, prompt templates, training procedure. Additionally, we provide an overview of all results presented in the main paper in numerical table form, an report additional experimental results leveraging alternate fine-tuning solutions. 

### E.1 MODEL 

This section provides extended details on the architecture, pretraining configuration, and input formatting of the vision-language models used in our experiments. Our primary backbone is PaliGemma (Beyer et al., 2024; Steiner et al., 2024). 

24 

Preprint 

Table 1: Detailed architecture of the PaliGemma model, comprising a SigLIP-So400m vision tower, a multimodal projection head, and a Gemma-based language decoder. All transformer layers follow standard design and include residual connections around attention and MLP blocks. 

|**Component**|**Configuration**|
|---|---|
|_Vision_|_Tower: SigLIP-So400m_|
|Patch Embedding|Conv2d(in=3, out=1152, kernel=14, stride=14)|
|Position Embedding|Embedding(num_embeddings=256, emb_dim=1152)|
|Encoder|27 × Transformer Encoder Layers|
|Self-Attention|—|
|Query / Key / Value projection<br>Layer Normalization<br>MLP Block|Linear(1152_→_1152, bias=True)<br>LayerNorm((1152,), eps=1e-6)<br>—|
|Activation Function|GELU-Tanh|
|Feedforward layer (up)|Linear(1152_→_4304, bias=True)|
|Feedforward layer (down)|Linear(4304_→_1152, bias=True)|
|Layer Normalization|LayerNorm((1152,), eps=1e-6)|
|Post-Encoder Layer Norm|LayerNorm((1152,), eps=1e-6)|
|_Multi_|_modal Projection Head_|
|Linear Projection|Linear(1152_→_2304, bias=True)|
|_Lan_|_guage Model: Gemma_|
|Token Embedding|Embedding(vocab=257216, dim=2304)|
|<br>Decoder Stack|<br>26 × Transformer Decoder Layers|
|Self-Attention|—|
|Query projection|Linear(2304_→_2048, bias=False)|
|<br>Key projection|Linear(2304_→_1024, bias=False)|
|Value projection|Linear(2304_→_1024, bias=False)|
|<br>Output projection|Linear(2048_→_2304, bias=False)|
|MLP Block|—|
|Gating projection|Linear(2304_→_9216, bias=True)|
|<br>Down projection|<br>Linear(2304_→_9216, bias=True)|
|Up projection|Linear(9216_→_2304, bias=True)|
|Activation Function|GELU-Tanh|
|Normalization Layers|—|
|<br>Input Norm|RMSNorm(2304, eps=1e-6)|
|<br>Post-Attn Norm|<br>RMSNorm(2304, eps=1e-6)|
|Pre-FFN Norm|<br>RMSNorm(2304, eps=1e-6)|
|Post-FFN Norm|<br>RMSNorm(2304, eps=1e-6)|
|Rotary Embeddings|GemmaRotaryEmbedding|
|LM Head|Linear(2304_→_257216, bias=False)|


### E.1.1 OVERVIEW 

PaliGemma is a VLM that processes both images and text as input and autoregressively generates natural language output. It follows the training paradigm of PaLI-3 (Chen et al., 2023), combining a ViT-based vision encoder (Dosovitskiy et al., 2021) with a decoder-only Transformer language model. The model is publicly available (Wolf et al., 2019). The architecture is fully modular, comprising three parameterized components: (i) _Vision encoder_ ( _MV_ ): based on SigLIP (Zhai et al., 2023), specifically the “shape optimized” So400m (Alabdulmohsin et al., 2023). (ii) _Multimodal projection head_ ( _MP_ ): a single linear layer for projecting visual features into the language decoder’s embedding space. (iii) _Language decoder_ ( _ML_ ): a Transformer-based autoregressive model from the Gemma family (Mesnard et al., 2024; Rivière et al., 2024). Below, we discuss the architecture in more details, the general layer-level overview is also provided in Table 1. 

25 

Preprint 

Table 2: Component-wise parameter overview of the PaliGemma model. 

|**Component**|**Model / Variant**|**Details**|**# Params**|
|---|---|---|---|
|Vision Encoder|SigLIP-So400m|Input resolutions: 224px<sup>2</sup>, 448px<sup>2</sup>, 896px<sup>2</sup>|400M|
|Multimodal Projection|—|Connects vision and language components|2.66M|
||PG 1|Gemma 1 2B, pre-trained on 6T tokens|3B|
|Language Model|PG 2|Gemma 2 2B, pre-trained on 2T tokens|3B|
||PG 3|Gemma 2 9B, pre-trained on 8T tokens|9.7B|


**Vision Encoder: SigLIP-So400m.** The visual backbone _MV_ is a ViT-style encoder pretrained using a Sigmoid contrastive loss (SigLIP). It processes input images by dividing them into nonoverlapping 14 _×_ 14 patches. Each patch is linearly projected into a 1152-dimensional embedding via a convolutional stem. To encode spatial structure, learned positional embeddings are added before the representation is passed through a stack of 27 SigLIP encoder layers. Each encoder layer contains multi-head self-attention with projection layers for queries, keys, and values, followed by an MLP block with GELU-Tanh activations. All transformer blocks use LayerNorm and residual connections. The vision tower supports multiple input resolutions (224, 448, 896), though our experiments fix resolution at 224px<sup>2</sup> for consistency and efficiency. 

**Multimodal Projection Head.** The projection head _MP_ is a lightweight linear mapping from the vision encoder’s output dimension (1152) to the language decoder’s input dimension (2304). It contains approximately 2.66M parameters and is initialized with zero-mean weights. This head enables alignment between visual and linguistic modalities and is important for bridging the representation gap between the vision and language components. 

**Language Decoder: Gemma.** The language module _ML_ is a decoder-only Transformer with 26 layers and 2304-dimensional hidden states. Token embeddings are learned over a vocabulary of 257,216 tokens, encoded using the SentencePiece tokenizer (Kudo & Richardson, 2018). Each Transformer block contains a self-attention mechanism with separate linear projections for queries, keys, and values. The MLP block follows a gated architecture, where the input is processed through parallel down projection and gating projection layers, modulated by a GELU-Tanh activation (Hendrycks & Gimpel, 2016), combined via elementwise multiplication, and then passed through an up projection to return to the model’s hidden dimension. RMSNorm is applied before and after both attention and MLP sublayers to stabilize training. Rotary positional embeddings are added to enable relative position encoding. Output tokens are produced via a tied language modeling head that projects back to the vocabulary space. 

### E.1.2 CONFIGURATIONS 

Table 2 summarizes the architecture components and parameter counts of the PaliGemma configurations available for experimentation. While we focus on the PaliGemma 2 3b variant in our study, we include all publicly released configurations for completeness and to clarify how our selected model compares to other available options. All three variants share the same vision encoder and multimodal integration strategy, differing only in the language decoder. The first configuration, PaliGemma 1 3b, pairs the visual encoder with Gemma 1 (2B), pretrained on 6 trillion tokens, resulting in a total model size of approximately 3 billion parameters. The second configuration, PaliGemma 2 3b, replaces the decoder with Gemma 2 (2B), pretrained on 2 trillion tokens, and maintains a comparable total parameter count. The third and largest variant, PaliGemma 2 10b, uses Gemma 2 (9B) as the decoder, pretrained on 8 trillion tokens, yielding a total model size of approximately 9.7 billion parameters. 

### E.1.3 PROMPT FORMAT 

To generate textual responses, we adopt a unified prompt format for the decoder. Each input sequence consists of image tokens _SI_ , a textual prefix _ST_<sup>PREF</sup> containing the question, and a suffix _ST_<sup>SUFF</sup> containing the expected answer. The model autoregressively generates the answer tokens, and training loss is applied only to the suffix. 

26 

Preprint 

Let _n_ denote the number of input frames and _p_ the number of visual tokens (patch embeddings) per frame. In our setting, each frame is encoded as _p_ = 256 visual tokens. The overall input schema is as follows: 


Here, _SI_ contains visual tokens produced by the vision encoder _MV_ , and projected into _ML_ space using _MP_ . The prefix _ST_<sup>PREF</sup> starts with a special <BOS> token and includes a task-language cue (e.g., “answer en”), the question, and a separator <SEP>. The suffix _ST_<sup>SUFF</sup> contains the target answer, terminated with <EOS> and padded with <PAD> tokens for batching. 

### E.1.4 PRETRAINING DATA AND FILTERING 

PaliGemma is pretrained on a mixture of large-scale vision-language datasets, including WebLI (Chen et al., 2022b), CC3M-35L (Sharma et al., 2018), VQ<sup>2</sup> A-CC3M-35L (Changpinyo et al., 2022), OpenImages (Piergiovanni et al., 2022), and WIT (Srinivasan et al., 2021). Data quality and safety are maintained through pornographic content filtering, text safety and toxicity filtering, and privacy-preserving measures. 

### E.2 EVALUATION METRICS 

In this section, we provide additional details on metrics used for quantitative evaluation. We employ two complementary metrics: _Exact Match (EM)_ and _ROUGE-F1 (ROUGE)_ , which together capture both syntactic precision and semantic alignment. 

**Exact Match Accuracy (** _EM_ **)** measures whether the generated answer is identical to the expected answer, providing a high-precision signal for correctness. Formally, it is defined as: 


where _A_<sup>ˆ</sup> is the model’s prediction and _A_ is the corresponding ground-truth answer. This metric is especially informative for binary and multiple-choice formats where the output space is well-defined. 

**ROUGE F** 1 (ROUGE) captures token-level semantic overlap between generated and reference responses by computing the harmonic mean of precision and recall. This allows us to account for partially correct or paraphrased answers. For binary questions, we compute the metric on the bigram level, while for multiple-choice and open-ended formats, we use trigram-level evaluation. 

Formally, let _G_ and _GT_ denote the sets of _n_ -grams in the generated and ground truth answers, respectively. Precision and recall are defined as: 


where _|G ∩ GT |_ counts overlapping _n_ -grams. The ROUGE score is then computed as: 


Together, these metrics provide a robust view of model performance: EM reflects exact correctness, while ROUGE provides a softer measure of semantic fidelity, particularly useful for evaluating open-ended generations. 

27 

Preprint 

Table 3: Summary of hyperparameters used in our experiments. 

|**Hyperparameter**|**Value**|
|---|---|
|Input resolution|224_×_224|
|Image frames per input|1–8|
|Number of epochs|1–10|
|Batch size (per device)|1|
|Gradient accumulation steps|4|
|Optimizer|AdamW Loshchilov & Hutter (2019)|
|Learning rate|5_×_10<sup>_−_5</sup>, cosine annealing|
|Learning rate warmup|10%<br>|
|Weight decay|1_×_10<sup>_−_6</sup>|
|Gradient clipping|Global norm, threshold 1.0|
|VLM backbone|PaliGemma 2 (3B) Beyer et al. (2024)|


### E.3 RESULTS 

**Hyperparameters.** Table 3 summarizes the core training hyperparameters used across all adaptation experiments. We train all models on 8 NVIDIA A100 GPUs with a batch size of 1 per device and accumulate gradients over 4 steps, yielding an effective batch size of 32. Each epoch corresponds to a full pass over the adaptation dataset, and no early stopping is applied. Models were trained for 1–10 epochs depending on task and setting. Optimization is performed using AdamW (Loshchilov & Hutter, 2019) with parameters _β_ 1 = 0 _._ 9, _β_ 2 = 0 _._ 999, a base learning rate of 5 _×_ 10<sup>_−_5</sup> , and weight decay of 1 _×_ 10<sup>_−_6</sup> . We use cosine learning rate annealing (Loshchilov & Hutter, 2022) with a linear warmup over the first 10% of training steps. To stabilize training, we apply gradient clipping with a global norm threshold of 1.0. All models use PaliGemma 2 (3B) (Beyer et al., 2024) as the vision-language backbone unless otherwise noted. We vary the number of input frames between 1 and 8 depending on task, and all images are resized to a fixed resolution of 224 _×_ 224. Training is conducted in bfloat16 precision using data parallelism. Model selection is based on final validation accuracy. 

**Tabular Results Summary.** The following tables summarize primary experimental findings across our study. Each entry corresponds to a core evaluation or analysis in the paper, organized by experimental section and aligned with the corresponding table description. 

- _Zero-Shot Evaluation_ (Section 4): Table 4 reports ROUGE-F1 zero-shot performance of pretrained PaliGemma and VideoLLaMA3 models on Action and Character Recognition tasks. Models are evaluated in a zero-shot setting with 1 or 8 input frames, across binary, multiple-choice, and open-ended formats. 

- _Fine-Tuned Baselines_ (Section 4): Table 5 reports ROUGE-F1 and Exact Match performance of PaliGemma 2 variants fine-tuned using full, partial, and parameter-efficient strategies. All models are trained on a single frame for one epoch, and evaluated across binary, multiplechoice, and open-ended formats. 

- _Analysis: Supervision and Temporal Context_ (Section 5): Table 6 examines early-stage learning dynamics on Character Recognition (CR), with evaluation at sub-epoch intervals. Table 7 reports AR performance as a function of training budget, scaling the number of epochs with a single input frame. Table 8 extends this analysis to jointly vary training epochs and the number of input frames, disentangling the effects of temporal context and supervision on AR. 

- _Analysis: Temporal Sampling Strategies_ (Section 5): Table 9 compares first- _n_ and uniform- _n_ frame sampling strategies for Action Recognition, evaluating model performance across varying temporal context lengths ( _n ∈{_ 1 _, . . . ,_ 8 _}_ ). 

- _Analysis: Optimizing Data Mix for Unified Multi-Task Evaluation_ (Section 5): This analysis spans three tables. Table 10 explores task-level trade-offs when jointly training on Action and Character Recognition by varying _α_ AR vs. _α_ CR, with format distribution held uniform. Table 11 fixes _α_ AR = 0 _._ 8 and searches over format-level ratios ( _β_ ), revealing the impact 

28 

Preprint 

Table 4: Zero-shot ROUGE-F1-based evaluation of PaliGemma (PG) and VideoLLaMA3 (VL3) models on Action and Character Recognition tasks using 1 and 8 input frames. “MC” denotes multiple-choice and “OE” open-ended formats. 

|||**Ac**|**tion Recogniti**|**on**|**Cha**|**racter Recogni**|**tion**|
|---|---|---|---|---|---|---|---|
|**Fr**|**Model**|**Binary**|**MC**|**OE**|**Binary**|**MC**|**OE**|
||PG 1 3B|50.43_±_0.13|8.12_±_0.02|10.83_±_0.01|50.73_±_0.38|0.46_±_0.06|0.00_±_0.00|
||PG 2 3B|44.69_±_0.03|9.30_±_0.17|12.64_±_0.01|48.58_±_0.07|0.28_±_0.06|0.01_±_0.00|
|1|PG 2 10B|50.04_±_0.03|26.98_±_0.00|12.35_±_0.21|50.08_±_0.07|8.33_±_0.50|0.00_±_0.00|
||VL3-2B|3.24_±_0.00|18.52_±_0.06|6.27_±_0.05|8.76_±_0.04|3.44_±_0.08|0.50_±_0.01|
||VL3-7B|45.02_±_0.28|15.53_±_0.05|6.54_±_0.04|39.09_±_0.73|6.21_±_0.05|0.51_±_0.02|
||PG 1 3B|51.67_±_0.02|10.68_±_0.00|10.32_±_0.00|51.39_±_0.07|0.25_±_0.00|0.00_±_0.00|
||PG 2 3B|47.61_±_0.19|6.73_±_0.04|14.52_±_0.00|48.37_±_0.18|0.03_±_0.00|0.01_±_0.00|
|8|PG 2 10B|50.02_±_0.06|26.93_±_0.01|12.12_±_0.00|50.09_±_0.06|0.22_±_0.00|0.00_±_0.00|
||VL3-2B|13.92_±_0.13|3.47_±_0.02|0.32_±_0.01|13.92_±_0.13|3.46_±_0.04|0.32_±_0.01|
||VL3-7B|15.05_±_0.21|16.67_±_0.35|6.35_±_0.06|12.76_±_0.52|5.88_±_0.01|0.54_±_0.01|


Table 5: Performance of fine-tuned PaliGemma 2 variants on Action and Character Recognition tasks. We compare full, partial, and parameter-efficient tuning strategies. “MC” denotes multiple-choice and “OE” open-ended formats. 

||**Bin**|**ary**|**Multipl**|**e-choice**|**Open-**|**ended**|
|---|---|---|---|---|---|---|
|**Model**|**EM**|**ROUGE**|**EM**|**ROUGE**|**EM**|**ROUGE**|
||||**Action Recogn**|**ition**|||
|_FL_|50.00_±_0.00|50.00_±_0.00|13.13_±_0.00|27.57_±_0.00|13.13_±_0.00|27.57_±_0.00|
|_FP_|83.97_±_0.02|83.97_±_0.02|61.43_±_0.58|68.05_±_0.70|61.68_±_0.35|68.46_±_0.19|
|_FV_|83.70_±_0.97|83.70_±_0.97|63.40_±_0.45|69.87_±_0.44|66.03_±_0.10|71.92_±_0.08|
|_FP_+_L_|74.47_±_1.64|74.47_±_1.64|13.13_±_0.00|27.57_±_0.00|55.74_±_0.70|64.83_±_0.29|
|_FV_+_L_|75.80_±_0.16|75.80_±_0.16|13.13_±_0.00|27.57_±_0.00|13.13_±_0.00|27.57_±_0.00|
|_FV_+_P_|73.46_±_0.85|73.46_±_0.85|61.21_±_0.23|67.57_±_0.21|64.70_±_0.02|70.93_±_0.01|
|_Fall_|74.35_±_1.37|74.35_±_1.37|13.13_±_0.00|27.57_±_0.00|13.13_±_0.00|27.57_±_0.00|
|_FLoRA_|44.66_±_0.21|44.66_±_0.21|0.02_±_0.01|9.21_±_0.01|0.00_±_0.00|12.49_±_0.00|
|||**C**|**haracter Recog**|**nition**|||
|_FL_|50.00_±_0.00|50.00_±_0.00|98.92_±_0.00|98.92_±_0.00|98.98_±_0.00|98.99_±_0.01|
|_FP_|99.09_±_0.11|99.09_±_0.11|99.22_±_0.33|99.22_±_0.33|99.15_±_0.07|99.15_±_0.07|
|_FV_|99.31_±_0.01|99.31_±_0.01|99.14_±_0.42|99.14_±_0.42|99.61_±_0.12|99.61_±_0.12|
|_FP_+_L_|50.00_±_0.00|50.00_±_0.00|98.28_±_0.00|98.30_±_0.02|98.39_±_0.00|98.39_±_0.00|
|_FV_+_L_|50.00_±_0.00|50.00_±_0.00|96.88_±_0.00|96.88_±_0.00|98.45_±_0.00|98.45_±_0.00|
|_FV_+_P_|60.32_±_0.02|60.32_±_0.02|99.22_±_0.00|99.22_±_0.00|99.79_±_0.00|99.79_±_0.00|
|_Fall_|50.00_±_0.00|50.00_±_0.00|97.67_±_0.06|97.67_±_0.06|96.55_±_0.01|96.55_±_0.01|
|_FLoRA_|48.76_±_0.00|48.76_±_0.00|0.00_±_0.00|0.32_±_0.00|0.00_±_0.00|0.01_±_0.01|


of increased open-ended (OE) supervision. Table 12 further investigates this high-OE regime, balancing the remaining budget between binary and multiple-choice for optimal performance. 

## F HUMAN ANNOTATION STUDY 

This section provides full details of our human annotation study, including rollout generation, annotation procedures, inter-annotator agreement, and evaluation metrics. The goal is to validate the adapted VLM’s fine-grained predictions on generated video rollouts. 

29 

Preprint 

Table 6: _Supervision and Temporal Context:_ Training budget analysis for Character Recognition. Models are fine-tuned for sub-epoch durations and evaluated across binary, multiple-choice (MC), and open-ended (OE) formats. 

||**Bin**|**ary**|**Multipl**|**e-choice**|**Open-**|**ended**|
|---|---|---|---|---|---|---|
|**Ep**|**EM**|**ROUGE**|**EM**|**ROUGE**|**EM**|**ROUGE**|
|0.005|50.84_±_1.70|50.84_±_1.70|14.27_±_0.00|14.27_±_0.00|13.16_±_0.00|13.27_±_0.00|
|0.01|54.92_±_0.84|54.92_±_0.84|17.85_±_0.00|17.85_±_0.00|16.78_±_0.14|16.88_±_0.01|
|0.02|57.91_±_3.19|57.91_±_3.19|28.64_±_0.00|28.64_±_0.00|26.29_±_2.96|28.38_±_0.01|
|0.03|57.45_±_0.58|57.45_±_0.58|64.19_±_0.00|64.19_±_0.00|40.76_±_0.01|40.98_±_0.00|
|0.06|65.88_±_3.71|65.88_±_3.71|93.96_±_0.00|93.96_±_0.00|88.89_±_0.00|88.95_±_0.01|
|0.10|87.47_±_4.11|87.47_±_4.11|96.54_±_0.00|96.54_±_0.00|97.01_±_0.38|97.02_±_0.40|
|0.125|91.63_±_7.71|91.63_±_7.71|97.08_±_0.00|97.08_±_0.00|97.28_±_0.00|97.30_±_0.00|
|0.20|97.96_±_0.45|97.96_±_0.45|97.89_±_0.28|97.89_±_0.28|98.12_±_0.00|98.14_±_0.02|
|0.25|97.75_±_0.74|97.75_±_0.74|98.08_±_0.00|98.08_±_0.00|98.12_±_0.00|98.15_±_0.00|
|0.33|98.42_±_0.20|98.42_±_0.20|98.19_±_0.00|98.19_±_0.00|98.30_±_0.00|98.35_±_0.00|
|0.50|98.74_±_0.06|98.74_±_0.06|98.45_±_0.00|98.45_±_0.00|98.51_±_0.00|98.54_±_0.00|
|0.67|99.11_±_0.10|99.11_±_0.10|98.99_±_0.08|98.99_±_0.08|99.09_±_0.00|99.09_±_0.00|
|0.75|99.03_±_0.04|99.03_±_0.04|99.15_±_0.00|99.15_±_0.00|99.21_±_0.00|99.22_±_0.01|
|1|99.09_±_0.11|99.09_±_0.11|99.22_±_0.33|99.22_±_0.33|99.15_±_0.07|99.15_±_0.07|


Table 7: _Supervision and Temporal Context:_ Training budget analysis for Action Recognition, with models fine-tuned for up to 10 epochs. Evaluated using across binary, multiple-choice (MC), and open-ended (OE) formats. 

||**Bin**|**ary**|**Multiple**|**-Choice**|**Open-**|**Ended**|
|---|---|---|---|---|---|---|
|**Ep**|**EM**|**ROUGE**|**EM**|**ROUGE**|**EM**|**ROUGE**|
|1|83.97_±_0.02|83.97_±_0.02|61.43_±_0.58|68.05_±_0.70|61.68_±_0.35|68.46_±_0.19|
|2|84.92_±_0.23|84.92_±_0.23|64.90_±_0.15|71.17_±_0.01|64.05_±_0.01|70.36_±_0.01|
|4|85.37_±_0.30|85.37_±_0.30|64.58_±_0.69|70.89_±_0.55|64.79_±_0.31|70.88_±_0.27|
|8|85.18_±_0.20|85.18_±_0.20|63.53_±_0.35|69.95_±_0.37|63.43_±_0.28|69.91_±_0.18|
|10|85.11_±_0.41|85.11_±_0.41|62.88_±_1.35|69.34_±_1.20|66.82_±_3.75|72.34_±_3.04|


Figure 10: Reference slides shown to annotators during the human annotation study, illustrating the two recognition targets: _actions_ (left) and _characters_ (center and right). The slides include 20 exemplar videos (7 actions, 13 characters) to support consistent evaluation of VLM-generated responses. 

### F.1 STUDY DESIGN 

**Task Overview.** Human annotators were presented with short video clips generated by a world model, each paired with a natural language question and an answer generated by the VLM. They were asked to judge whether the model’s answer accurately described what was shown in the video. Each QA pair was rated using one of four categories: _Correct_ (score = 1), _Partially Correct_ (0.5), _Incorrect_ (0), or _Unclear / Cannot Tell_ (excluded from accuracy computation). 

**Annotation Setup and Interface.** Annotations were collected using a custom PowerPoint-based interface (see Figure 11). Each slide presented a short video, a question, and a generated answer. 

30 

Preprint 

Table 8: _Supervision and Temporal Context:_ Training budget and temporal context analysis for Action Recognition. Models are fine-tuned for up to 10 epochs and evaluated with up to 8 input frames. 

|||**Bin**|**ary**|**Multipl**|**e-choice**|**Open-**|**ended**|
|---|---|---|---|---|---|---|---|
|**Ep**|**Fr**|**EM**|**ROUGE**|**EM**|**ROUGE**|**EM**|**ROUGE**|
||1|83.97_±_0.02|83.97_±_0.02|61.43_±_0.58|68.05_±_0.70|61.68_±_0.35|68.46_±_0.19|
|1|2|84.42_±_0.06|84.42_±_0.06|65.53_±_0.27|72.03_±_0.06|65.38_±_0.06|71.74_±_0.23|
||4|90.97_±_0.10|90.97_±_0.10|83.11_±_0.08|87.13_±_0.04|82.26_±_0.14|87.02_±_0.06|
||8|93.85_±_0.28|93.85_±_0.28|88.89_±_0.14|93.40_±_0.76|87.80_±_0.20|92.23_±_0.16|
||1|85.10_±_0.02|85.10_±_0.02|64.93_±_0.06|71.09_±_0.11|64.05_±_0.01|70.36_±_0.01|
|2|2|86.53_±_0.45|86.40_±_0.26|69.20_±_0.88|75.02_±_0.67|68.83_±_0.47|72.45_±_2.76|
||4|92.26_±_0.34|92.26_±_0.34|84.19_±_0.10|88.46_±_0.11|83.34_±_0.15|87.84_±_0.06|
||8|95.05_±_0.15|95.05_±_0.15|89.27_±_0.14|93.30_±_0.22|89.42_±_0.22|93.25_±_0.15|
||1|85.37_±_0.30|85.37_±_0.30|64.58_±_0.69|70.89_±_0.55|64.79_±_0.31|70.88_±_0.27|
|4|2|86.89_±_0.06|86.89_±_0.06|69.89_±_0.83|75.49_±_0.69|70.04_±_0.08|75.74_±_0.06|
||4|92.58_±_0.18|92.58_±_0.18|85.13_±_0.19|89.28_±_0.17|84.61_±_0.07|88.81_±_0.04|
||8|95.29_±_0.07|95.29_±_0.07|90.64_±_0.00|94.09_±_0.04|90.18_±_0.16|93.81_±_0.11|
||1|85.04_±_0.00|85.04_±_0.00|63.53_±_0.35|69.95_±_0.37|63.62_±_0.00|70.03_±_0.00|
|8|2|87.27_±_0.40|87.27_±_0.40|69.84_±_0.66|75.44_±_0.45|70.11_±_0.65|75.75_±_0.52|
||4|92.97_±_0.49|92.97_±_0.49|85.32_±_0.08|89.27_±_0.08|84.93_±_0.21|89.05_±_0.11|
||8|95.48_±_0.21|95.48_±_0.21|90.71_±_0.14|94.15_±_0.13|91.02_±_0.28|93.96_±_0.71|
||1|85.40_±_0.00|85.40_±_0.00|62.88_±_1.35|69.34_±_1.20|66.82_±_3.75|72.34_±_3.04|
|10|2|87.17_±_0.22|87.17_±_0.22|70.18_±_0.00|75.64_±_0.00|69.59_±_0.20|75.37_±_0.07|
||4|92.96_±_0.37|92.96_±_0.37|85.02_±_0.58|89.05_±_0.49|84.71_±_0.08|88.94_±_0.06|
||8|96.03_±_0.05|96.03_±_0.05|90.75_±_0.04|94.22_±_0.05|91.00_±_0.11|94.33_±_0.09|


Table 9: Comparison of frame sampling strategies for Action Recognition. We evaluate first- _n_ vs. uniform- _n_ sampling across varying temporal context lengths ( _n ∈{_ 1 _, . . . ,_ 8 _}_ ). 

|||**Bin**|**ary**|**Multipl**|**e-choice**|**Open-**|**ended**|
|---|---|---|---|---|---|---|---|
||**Fr**|**EM**|**ROUGE**|**EM**|**ROUGE**|**EM**|**ROUGE**|
||1|83.97_±_0.02|83.97_±_0.02|61.43_±_0.58|68.05_±_0.70|61.68_±_0.35|68.46_±_0.19|
||2|84.42_±_0.06|84.42_±_0.06|65.53_±_0.27|72.03_±_0.06|65.38_±_0.06|71.74_±_0.23|
|N|3|87.93_±_0.28|87.93_±_0.28|75.73_±_0.18|81.07_±_0.06|74.68_±_0.16|80.21_±_0.08|
|st-|4|90.97_±_0.10|90.97_±_0.10|83.11_±_0.08|87.13_±_0.04|82.26_±_0.14|87.02_±_0.06|
|Fir|5|92.00_±_0.30|92.00_±_0.30|85.46_±_0.34|89.84_±_0.18|85.10_±_0.16|89.47_±_0.10|
||6|92.95_±_0.30|92.95_±_0.30|86.86_±_0.08|91.13_±_0.06|86.59_±_0.39|90.82_±_0.30|
||7|93.31_±_0.03|93.31_±_0.03|87.95_±_0.08|92.06_±_0.06|87.58_±_0.17|91.82_±_0.08|
||8|93.85_±_0.28|93.85_±_0.28|88.89_±_0.14|93.40_±_0.76|87.80_±_0.20|92.23_±_0.16|
||1|83.97_±_0.02|83.97_±_0.02|61.43_±_0.58|68.05_±_0.70|61.68_±_0.35|68.46_±_0.19|
||2|90.47_±_0.62|90.47_±_0.62|83.93_±_0.04|88.36_±_0.08|82.68_±_0.19|87.33_±_0.01|
|-N|3|93.59_±_0.07|93.59_±_0.07|88.90_±_0.11|92.85_±_0.10|88.49_±_0.24|92.57_±_0.04|
|rm|4|93.57_±_0.39|93.57_±_0.39|89.94_±_0.04|93.65_±_0.01|89.56_±_0.42|93.49_±_0.28|
|ifo|5|94.25_±_0.04|94.25_±_0.04|89.99_±_0.18|93.70_±_0.13|89.72_±_0.10|93.63_±_0.23|
|Un|6|94.01_±_0.57|94.01_±_0.57|90.03_±_0.04|93.73_±_0.06|90.09_±_0.18|93.88_±_0.16|
||7|93.96_±_0.16|93.96_±_0.16|90.34_±_0.23|94.00_±_0.10|89.94_±_0.11|93.73_±_0.10|
||8|94.62_±_0.48|94.62_±_0.48|90.72_±_0.12|94.30_±_0.10|90.30_±_0.04|94.01_±_0.02|


Annotators selected a rating from a predefined rubric. The full annotation guidelines – including action and character definitions and rating instructions – were embedded in the annotation deck for reference. For completeness, we also provide them in Table 13 and Figure 10. The annotation study was carried out by a subset of the authors with prior experience in the environment. Judging correctness required non-trivial familiarity with the visual dynamics and task ontology, making expert annotation necessary. All annotators were compensated above local minimum wage rates. Each QA pair was independently rated by two primary annotators. In cases of disagreement or if either annotator marked the example as _Unclear_ , a third, more experienced adjudicator reviewed the pair and assigned a final rating. 

31 

Preprint 

Table 10: _Optimizing Data Mix for Unified Multi-Task Evaluation:_ Performance tradeoffs under varying task-level allocation ratios for Action ( _α_ AR) vs. Character Recognition ( _α_ CR), with a fixed format distribution ( _β_ =<sup>1</sup> _/_ 3 per format). Evaluated across binary, multiple-choice (MC), and openended (OE) formats. 

|||**Bin**|**ary**|**Multipl**|**e-choice**|**Open**|**-ended**|
|---|---|---|---|---|---|---|---|
|**_α_**AR|**_α_**CR|**EM**|**ROUGE**|**EM**|**ROUGE**|**EM**|**ROUGE**|
||||**A**|**ction Recogniti**|**on**|||
|0.20|0.80|84.13_±_1.66|84.13_±_1.66|26.10_±_0.43|39.04_±_0.10|27.03_±_0.21|39.60_±_0.13|
|0.40|0.60|88.11_±_1.44|88.11_±_1.44|28.13_±_1.15|40.93_±_0.57|29.17_±_0.40|41.66_±_0.51|
|0.50|0.50|88.59_±_1.41|88.59_±_1.41|29.10_±_0.65|41.20_±_0.16|29.66_±_0.54|41.17_±_0.22|
|0.60|0.40|90.80_±_0.04|90.80_±_0.04|30.44_±_0.03|42.54_±_0.01|30.55_±_0.49|42.32_±_0.60|
|0.80|0.20|91.23_±_0.91|91.23_±_0.91|84.06_±_1.26|89.42_±_1.00|30.88_±_0.63|42.85_±_0.42|
||||**Ch**|**aracter Recogn**|**ition**|||
|0.20|0.80|98.57_±_0.47|98.57_±_0.47|98.95_±_0.16|98.95_±_0.16|98.94_±_0.22|98.97_±_0.21|
|0.40|0.60|98.51_±_0.53|98.51_±_0.53|98.77_±_0.16|98.77_±_0.16|98.98_±_0.06|98.98_±_0.06|
|0.50|0.50|96.33_±_1.81|96.33_±_1.81|98.03_±_0.06|98.03_±_0.06|98.23_±_0.06|98.23_±_0.06|
|0.60|0.40|93.22_±_3.38|93.22_±_3.38|96.91_±_1.81|96.94_±_1.77|97.93_±_0.02|97.93_±_0.02|
|0.80|0.20|80.53_±_0.49|80.53_±_0.49|89.08_±_0.49|89.08_±_0.49|89.02_±_0.25|89.18_±_0.39|


Table 11: _Optimizing Data Mix for Unified Multi-Task Evaluation:_ Performance on Action and Character Recognition under varying format-level sampling ratios ( _β_ ) for Binary, Multiple-choice (MC), and Open-ended (OE) questions. We fix _α_ AR = 0 _._ 8 and train all models on the first 8 frames. 

|||||**Bin**|**ary**|**Multiple**|**-Choice**||**Open-**|**Ended**||
|---|---|---|---|---|---|---|---|---|---|---|---|
|**Ep**|**_β_**binary|**_β_**MC|**_β_**OE|**EM**|**ROUGE**|**EM**|**ROUGE**|**E**|**M**|**RO**|**UGE**|
||||||**Action R**|**ecognition**||||||
||0.4|0.2|0.4|92.32_±_0.37|92.32_±_0.37|84.32_±_0.89|89.54_±_0.64|31.61|_±_0.23|43.51|_±_0.09|
|1|0.2|0.4|0.4|90.80_±_0.71|90.80_±_0.71|86.60_±_0.38|91.27_±_0.42|32.06|_±_0.18|43.58|_±_0.54|
||0.0|0.4|0.6|49.98_±_0.04|49.98_±_0.04|86.65_±_0.99|91.26_±_0.87|85.51|_±_1.78|90.13|_±_1.53|
||0.0|0.2|0.8|50.11_±_0.06|50.11_±_0.06|86.58_±_0.47|91.42_±_0.21|87.45|_±_0.09|91.78|_±_0.09|
||0.4|0.2|0.4|93.14_±_0.48|93.14_±_0.48|86.77_±_0.00|91.28_±_0.00|32.96|_±_0.00|44.00|_±_0.00|
|2|0.2|0.4|0.4|92.89_±_0.16|92.89_±_0.16|87.83_±_0.00|92.13_±_0.00|33.37|_±_0.00|44.13|_±_0.00|
||0.0|0.4|0.6|41.22_±_0.00|41.30_±_0.01|89.17_±_0.07|93.12_±_0.02|88.55|_±_0.00|93.65|_±_0.00|
||0.0|0.2|0.8|49.98_±_0.03|49.99_±_0.02|88.68_±_0.00|92.71_±_0.00|88.59|_±_0.00|92.56|_±_0.00|
||0.4|0.2|0.4|94.33_±_0.34|94.33_±_0.34|92.67_±_0.07|93.27_±_0.71|33.94|_±_0.01|43.96|_±_0.00|
|4|0.2|0.4|0.4|94.19_±_0.13|94.19_±_0.13|93.04_±_0.01|93.57_±_0.74|33.78|_±_0.00|44.73|_±_0.00|
||0.0|0.4|0.6|50.19_±_0.27|50.19_±_0.27|89.78_±_0.11|93.52_±_0.03|88.95|_±_0.05|92.75|_±_0.06|
||0.0|0.2|0.8|49.98_±_0.02|49.98_±_0.02|89.25_±_0.00|93.13_±_0.00|89.41|_±_0.00|93.16|_±_0.00|
||||||**Character**|**Recognition**||||||
||0.4|0.2|0.4|86.42_±_0.25|86.42_±_0.25|94.77_±_0.14|94.77_±_0.14|94.76|_±_0.08|94.63|_±_0.21|
|1|0.2|0.4|0.4|77.57_±_0.01|77.57_±_0.01|94.93_±_0.03|94.93_±_0.03|94.51|_±_0.57|94.15|_±_0.00|
||0.0|0.4|0.6|50.37_±_0.52|50.37_±_0.52|96.56_±_0.28|96.56_±_0.28|96.81|_±_0.39|96.82|_±_0.37|
||0.0|0.2|0.8|50.51_±_0.03|50.51_±_0.03|96.88_±_0.27|96.88_±_0.27|97.39|_±_0.18|97.39|_±_0.18|
||0.4|0.2|0.4|89.95_±_0.46|89.95_±_0.46|87.35_±_0.00|87.36_±_0.00|88.64|_±_0.00|88.64|_±_0.00|
||0.2|0.4|0.4|91.28_±_0.20|91.28_±_0.20|93.90_±_0.00|93.93_±_0.04|93.06|_±_0.00|93.09|_±_0.00|
|2|0.0|0.4|0.6|47.37_±_0.02|47.48_±_0.04|97.69_±_0.00|97.70_±_0.00|98.07|_±_0.00|98.07|_±_0.00|
||0.0|0.2|0.8|50.07_±_0.04|50.07_±_0.04|97.75_±_0.00|97.79_±_0.00|98.07|_±_0.00|98.07|_±_0.00|
||0.4|0.2|0.4|97.71_±_0.05|97.71_±_0.05|97.70_±_0.00|97.70_±_0.00|97.88|_±_0.01|97.91|_±_0.03|
|4|0.2|0.4|0.4|96.55_±_0.06|96.55_±_0.06|98.51_±_0.00|98.51_±_0.00|98.46|_±_0.00|98.46|_±_0.00|
||0.0|0.4|0.6|51.25_±_1.56|51.25_±_1.56|98.21_±_0.13|98.21_±_0.13|98.48|_±_0.06|98.49|_±_0.06|
||0.0|0.2|0.8|50.93_±_0.10|50.93_±_0.10|98.79_±_0.00|98.79_±_0.00|99.08|_±_0.00|99.09|_±_0.00|


**Selected World Models.** For our study, we aim to evaluate rollouts generated across different model scales, training diversities, and output resolutions, while keeping the underlying architecture general enough to apply broadly. To this end, we select two autoregressive world models (Kanervisto et al., 2025). The autoregressive formulation offers a flexible and widely adopted framework, and is the basis for many state-of-the-art private world models. 

32 

Preprint 

Table 12: _Optimizing Data Mix for Unified Multi-Task Evaluation:_ Performance on Action and Character Recognition under high open-ended (OE) supervision, with _β_ OE = 0 _._ 8 and remaining budget split between Binary and Multiple-choice (MC). 

|||||**Bin**|**ary**|**Multiple**|**-Choice**|**Open-**|**Ended**|
|---|---|---|---|---|---|---|---|---|---|
|**Ep**|**_β_**BN|**_β_**MC|**_β_**OE|**EM**|**ROUGE**|**EM**|**ROUGE**|**EM**|**ROUGE**|
||||||**Action**|**Recognition**||||
||0.15|0.05|0.80|88.85_±_0.04|88.85_±_0.04|81.93_±_0.00|89.08_±_0.00|86.72_±_0.00|91.33_±_0.00|
|1|0.10|0.10|0.80|87.38_±_0.59|87.38_±_0.59|85.58_±_0.00|90.50_±_0.00|86.88_±_0.00|91.25_±_0.00|
||0.05|0.15|0.80|85.67_±_0.19|85.67_±_0.19|86.38_±_0.09|91.21_±_0.06|86.84_±_0.02|91.34_±_0.03|
||0.15|0.05|0.80|92.45_±_0.11|92.45_±_0.11|87.52_±_0.00|91.90_±_0.00|87.97_±_0.63|92.19_±_0.41|
|2|0.10|0.10|0.80|92.11_±_0.18|92.11_±_0.18|88.42_±_0.00|92.54_±_0.00|88.50_±_0.00|92.54_±_0.00|
||0.05|0.15|0.80|91.98_±_0.24|91.98_±_0.24|88.72_±_0.00|92.78_±_0.00|88.56_±_0.00|92.66_±_0.00|
||0.15|0.05|0.80|92.98_±_0.21|92.98_±_0.21|88.93_±_0.00|93.02_±_0.00|89.64_±_0.00|93.34_±_0.00|
|4|0.10|0.10|0.80|92.81_±_0.11|92.81_±_0.11|91.40_±_2.81|93.88_±_0.70|89.43_±_0.00|93.20_±_0.00|
||0.05|0.15|0.80|91.52_±_0.37|91.52_±_0.37|89.80_±_0.00|93.54_±_0.01|89.81_±_0.01|93.49_±_0.06|
||||||**Characte**|**r Recognition**||||
||0.15|0.05|0.80|59.75_±_0.04|59.75_±_0.04|95.45_±_0.00|95.45_±_0.00|97.16_±_0.00|97.16_±_0.00|
|1|0.10|0.10|0.80|56.31_±_0.53|56.31_±_0.53|94.55_±_0.00|94.55_±_0.00|95.96_±_0.00|95.96_±_0.00|
||0.05|0.15|0.80|50.86_±_0.08|50.86_±_0.08|96.87_±_0.02|96.87_±_0.02|97.12_±_0.01|97.12_±_0.01|
||0.15|0.05|0.80|80.18_±_0.09|80.18_±_0.09|95.41_±_0.00|95.41_±_0.00|96.91_±_0.00|96.91_±_0.00|
|2|0.10|0.10|0.80|70.20_±_0.21|70.20_±_0.21|98.02_±_0.00|98.02_±_0.00|98.15_±_0.00|98.15_±_0.00|
||0.05|0.15|0.80|69.67_±_0.36|69.67_±_0.36|97.37_±_0.00|97.37_±_0.00|97.79_±_0.00|97.79_±_0.00|
||0.15|0.05|0.80|94.16_±_0.12|94.16_±_0.12|97.06_±_0.00|97.07_±_0.00|97.91_±_0.00|97.91_±_0.00|
|4|0.10|0.10|0.80|86.67_±_0.13|86.67_±_0.13|98.50_±_0.00|98.50_±_0.00|98.77_±_0.00|98.77_±_0.00|
||0.05|0.15|0.80|71.79_±_0.01|71.79_±_0.01|98.22_±_0.00|98.22_±_0.00|98.57_±_0.00|98.57_±_0.00|


The selected models generate sequences of visual frames and controller actions without textual supervision, using a decoder-only transformer (Radford et al., 2019; Vaswani et al., 2017) trained autoregressively on discrete tokens. Visual frames are encoded with a VQGAN (Esser et al., 2021), while joystick actions are tokenized using a learned discretization scheme based on action bucketization (Kanervisto et al., 2020). 

Each world model is implemented as a decoder-only transformer (Radford et al., 2019; Vaswani et al., 2017), trained to predict discrete tokens representing visual observations and actions. Visual frames are first compressed with a VQGAN (Esser et al., 2021), while joystick actions are tokenized using a learned discretization scheme based on action bucketization (Kanervisto et al., 2020). The objective is next-token prediction conditioned on prior visual and action tokens. We focus on the following model variants that differ in capacity, training diversity, and output resolution: (i) a large-scale model: 1.6B parameters, trained for 200K steps on gameplay from seven diverse environments (including Skygarden) at 300 _×_ 180, and (ii) a smaller model: 140M parameters, trained for 100K steps on gameplay from a single environment (Skygarden) at 128 _×_ 128 resolution. 

**Rollouts Generation.** Rollout generation follows a consistent protocol for both world models: at inference time, the model is conditioned on 1 second of ground-truth gameplay (visual and action tokens), after which it generates 10 seconds of future gameplay conditioned only on a se- 


Figure 11: Annotation interface example. Each instance includes a video clip, task instructions, and a table with: _Question_ (generated via evaluation protocol), _Response_ (VLM output), and _Score_ (human-assigned label). 

quence of held-out controller actions. For rollout generation, we use reference trajectories from the game dataset, which include time-aligned controller inputs and image frames. For each generated rollout, we randomly sample a 1-second context window (video frames and corresponding action tokens) from these trajectories. The world model is then conditioned on this context, which consists of an interleaved sequence of tokenized images and actions, and proceeds autoregressively to generate 

33 

Preprint 

Table 13: Annotation instructions provided to human raters as part of the study. The interface outlines task context, scoring criteria, general guidelines, and reference definitions for supported action categories. 

### **<mark>1. Task Overview</mark>** 

You will be presented with: 

- A short video clip; 

- A natural language question about the video; 

- An answer generated by a vision-language model. 

Your task is to evaluate whether the model’s answer accurately describes the events depicted in the <u>video.</u> 

### **<mark>2. How to Rate Each Answer</mark>** 

Assign one of the following categories: 

- _Correct (1.0)_ : Fully matches the event in the video; 

- _Partially Correct (0.5)_ : Captures the general idea but contains a minor error; 

- _Incorrect (0.0)_ : Wrong, hallucinated, or mismatched with the visual evidence; 

- _Unclear / Cannot Tell_ : Not enough evidence to confidently decide. 

### **<mark>3. General Guidelines</mark>** 

- Watch the full video before rating; 

- Base your decision solely on visible content; 

- Use provided action and character references; 

- If multiple plausible interpretations exist and the answer matches one, mark as _Correct_ ; 

- If unsure even after review, mark _Unclear / Cannot Tell_ ; 

- Optionally leave comments for ambiguous or interesting cases. 

### **<mark>5. Action Label Def</mark> i** **<mark>nitions</mark>** 

- _Evading Backwards_ : Moves backwards to avoid threat or reposition. 

- _Evading Forwards_ : Moves forwards. 

- _Evading Left / Right_ : Lateral movement left or right. 

- _Jumping Down_ : Jumps from a higher to a lower platform or level. 

- _Jumping on the Level_ : Jumps without elevation change. 

- _Jumping Up_ : Jumps upward to reach a higher platform. 

- _Mounting Hoverboard_ : Begins riding or is seen riding a hoverboard. 

latent image tokens and discretized action tokens. The generated rollout is then split into 14-frame chunks. This setup enables a comprehensive analysis of the UNIVERSE’s evaluation capabilities across two axes: (i) _in-domain performance_ : evaluating on Skygarden, the environment used for fine-tuning; (ii) _generalization_ : assessing performance on six unseen environments. It also allows comparison across generation quality and model capacity. We generate 82 rollouts for each model-environment setting, resulting in 656 rollouts in total. 

**Rollout Filtering.** To keep evaluation focused on challenging sequences, we remove only those rollouts that are either uninterpretable or uninformative. Specifically, annotators discard: (i) early segments with no meaningful interactions; (ii) rollouts dominated by occlusion; and (iii) sequences with no visible agents. These criteria target cases where neither humans nor models can extract actionable dynamics, while retaining all visually imperfect, ambiguous, and failure-prone generations. Thus, filtering eliminates only sequences that provide no evaluable signal. Figure 12 shows randomly sampled examples from each excluded category. 

**Complexity of Retained Rollouts.** Despite filtering out uninterpretable/uninformative sequences, many retained rollouts exhibit visual imperfections that make evaluation challenging. Annotators highlighted recurring generation failures including: (i) skin and appearance drift, where modelgenerated agent skins diverge from canonical silhouettes; (ii) missing or corrupted assets, such as hoverboards implied only through motion cues; and (iii) HUD-induced occlusion, where oversized or misplaced UI elements block important scene content. These imperfections arise from the underlying world models and introduce ambiguity while still permitting meaningful assessment. Figure 13 illustrates representative failure-prone cases, emphasizing that UNIVERSE is evaluated on realistic, imperfect rollouts rather than sanitized inputs. 

34 

Preprint 


Figure 12: Randomly sampled examples of rollouts excluded from the human evaluation study. 


Figure 13: Randomly sampled examples of rollouts retained for human evaluation. 

**UNIVERSE’s Response Generation.** To obtain responses from UNIVERSE, we provide it with a video segment (resized to match the evaluator’s input resolution) along with its corresponding question. We then sample five responses using greedy decoding and select the most frequent response as the final answer. In cases where all five responses are unique (i.e., no majority), one response is selected at random. The resulting dataset comprises rollouts from 8 settings: rollouts generated by a smaller model on Skygarden, and rollouts generated by a larger model across seven distinct environments. For each model–environment pair, we sample 30 rollouts. Each rollout is annotated with 6 question–answer (QA) pairs, along with a corresponding response from the adapted evaluator. Each of the resulting 1,440 QA instances was rated by 3 annotators, yielding 4,320 total human judgments. 

### F.2 EVALUATION METRICS 

We report two accuracy-based metrics using the adjudicated labels: 

35 

Preprint 

Table 14: Inter-annotator agreement and valid QA coverage across environments. We report Cohen’s _κ_ between the two primary annotators for each world model–map pair. The total number of valid examples excludes QA pairs marked as _Unclear_ by at least one annotator. 

|**Setting**|**Valid QA Pairs**|**Cohen’s**_κ_|
|---|---|---|
|1|29|0.91|
|2|28|0.67|
|3|28|0.74|
|4|29|0.87|
|5|30|0.67|
|6|29|0.61|
|7|30|0.59|
|8|24|0.79|


Table 15: Graded/strict accuracy of UNIVERSE on Action and Character Recognition tasks, evaluated by human annotators across different environments and question formats. We report results for Binary, Multiple-Choice (MC), and Open-Ended (OE) prompts, disaggregated by task and world model. All metrics are based on final adjudicated ratings. 

|||**Act**|**ion Recognit**|**ion**|**Character**|**Recognition**|
|---|---|---|---|---|---|---|
|**Setting**|**Binary**|**MC**|**OE**|**Binary**|**MC**|**OE**|
|1|98.3 / 96.7|51.7 / 46.7|75.0 / 73.3|93.3 / 93.3|83.3 / 83.3|93.3 / 93.3|
|2|96.7 / 96.7|60.0 / 60.0|65.0 / 60.0|99.9 / 99.9|90.0 / 90.0|93.3 / 93.3|
|3|96.7 / 96.7|63.3 / 63.3|80.0 / 80.0|99.9 / 99.9|86.7 / 86.7|93.3 / 93.3|
|4|93.3 / 93.3|43.3 / 43.3|73.3 / 73.3|96.7 / 96.7|96.7 / 96.7|99.9 / 99.9|
|5|80.0 / 76.7|76.7 / 73.3|93.3 / 93.3|96.7 / 96.7|99.9 / 99.9|99.8 / 99.8|
|6|71.7 / 70.0|56.7 / 56.7|75.0 / 70.0|96.7 / 96.7|93.3 / 93.3|96.7 / 96.7|
|7|68.3 / 66.7|50.0 / 46.7|80.0 / 76.7|93.3 / 93.3|90.0 / 90.0|96.7 / 96.7|
|8|92.9 / 89.3|35.7 / 32.1|41.1 / 39.3|85.7 / 85.7|10.7 / 10.7|60.7 / 60.7|


_Strict Accuracy._ : The proportion of QA pairs labeled as _Correct_ : 


_Graded Accuracy._ : Partial credit given to _Partially Correct_ responses: 


Only examples not marked _Unclear_ by adjudication are included in _N_ Answerable. 

_Inter-Annotator Agreement._ To quantify rating consistency, we compute Cohen’s _κ_ between the two primary annotators. The adjudicator’s label is used only when disagreement occurs and is excluded from agreement computation. Results are shown in Table 14. 

_Sample Size Justification._ We annotate 30 rollouts per model–environment pair. Assuming a standard deviation of _σ ≈_ 0 _._ 2 and a 95% confidence level, the confidence interval (CI) width is given by CI Width = _z_ 1 _−_ 2 _<u>C</u> ·_ _~~√~~_ _<u>σn</u>_<sup>.This yields an estimated CI of</sup><sup>_∼_7.1% for individual model–environment</sup> pairs ( _n_ = 30), and _∼_ 2.5% when aggregating across all eight pairs ( _n_ = 240), offering sufficient precision for comparative evaluation. 

### F.3 RESULTS 

Table 15 reports graded and strict accuracy across environments, recognition targets (Action and Character Recognition), and question formats (Binary, Multiple-Choice, Open-Ended). We observe a 

36 

Preprint 

clear gap in performance between rollouts generated by the two world models. UNIVERSE struggles with outputs from WHAM 140M, achieving substantially lower accuracy compared to WHAM 1.6B. This is likely due to a mismatch in image resolution: WHAM 140M generates frames at 128 _×_ 128 resolution, which must be upsampled to the UNIVERSE’s expected input of 224 _×_ 224. Despite resizing, the resulting frames often lack sharpness, making actions and characters harder to recognize. In contrast, UNIVERSE performs well on rollouts from WHAM 1.6B, even across diverse environments. On the in-domain setting (Environment A), the model achieves strong results—averaging 75.02% graded accuracy for AR and 90.00% for CR. When evaluating on the six unseen environments (Environments B–G), performance for AR drops slightly (from 75.02% to 73.52%), while CR remains stable or improves, suggesting strong generalization in character grounding and visual consistency tracking. 

**Qualitative Examples.** Figure 14 illustrates the diversity of generated rollouts across environments. WHAM 1.6B captures greater visual variation and scene composition compared to WHAM 140M. 

## G SUPPLEMENTARY EXPERIMENTAL RESULTS 

This section presents additional experimental results that support the main findings but are omitted from the main paper for clarity and space. These include: (i) a zero-shot analysis of PaliGemma variants to motivate backbone selection, (ii) CLIPScore-based baselines to contextualize performance without adaptation, and (iii) a study of low-rank adaptation (LoRA) across different rank values. While these results are not central to the unified evaluation framework proposed in the main text, they provide valuable insight into model selection, adaptation efficiency, and the limitations of standard evaluation proxies in our setting. 

### G.1 GPT-5 PERFORMANCE 

To demonstrate the complexity of the tasks that comprise our protocol, we conducted an evaluation of GPT-5 on randomly selected examples. We deliberately chose the simplest evaluation regime (binary action recognition) to test whether the model can succeed without adaptation. 

Figure 15 demonstrates that out of six random samples, GPT-5 produced incorrect answers in five cases. This consistent failure highlights the difficulty of the task. 

### G.2 ZERO-SHOT PERFORMANCE OF PALIGEMMA MODELS 

In this section, we benchmark three pretrained configurations—PaliGemma 1 3b, PaliGemma 2 3b, and PaliGemma 2 10b—under our proposed protocol and motivate our choice of PaliGemma 2 3b as the default backbone for subsequent experiments. Each model receives a natural language prompt along with either 1 or 8 image frames as input and produces a textual response. This experiment probes both model capacity and the role of temporal visual context in zero-shot settings. 

**Results.** Figure 16 reports ROUGE scores across task types, question formats, and visual context lengths. While zero-shot performance reveals some capacity for structured reasoning—particularly in the multiple-choice setting—it remains limited overall. Binary accuracy hovers near chance, and open-ended responses frequently lack specificity. Performance is strongest on action recognition (AR), likely reflecting pretrained models’ familiarity with generic visual dynamics. In contrast, character recognition (CR) lags behind, underscoring a lack of grounding in domain-specific entities. Increasing the number of input frames modestly improves AR, but yields diminishing returns for CR. Among the evaluated configurations, PaliGemma 2 10b performs best in absolute terms. However, the margin over PaliGemma 2 3b is narrow, and PaliGemma 2 3b offers a substantially smaller footprint while using a newer Gemma 2 decoder architecture. We therefore adopt PaliGemma 2 3b as the default model for all subsequent adaptation experiments, balancing performance, compute efficiency, and architectural recency. 

### G.3 CLIPSCORE COMPARISONS 

To further evaluate zero-shot recognition capabilities without adaptation, we apply CLIPScore to our rollout evaluation protocol. Specifically, we assess four pretrained CLIP variants – ViT-B/32, ViT- 

37 

Preprint 


Figure 14: Representative frames from rollouts across the eight evaluation settings, spanning different environments, scales, and resolutions. 

B/16, ViT-L/14, and ViT-L/14-336 – across both Action Recognition (AR) and Character Recognition (CR) tasks using 1-frame and 8-frame visual inputs. For each evaluation instance, we extract either 1 or 8 frames from the video segment and compute the cosine similarity between each image and a predefined set of textual labels (i.e., action verbs for AR, character names for CR). For single-frame 

38 

Preprint 


Figure 15: Performance of GPT-5 on six randomly sampled binary action recognition questions. Each panel shows the trial prompt, the model’s response, and the ground-truth label. Despite the apparent simplicity of the setup, GPT-5 fails on 5/6 trials, underscoring the difficulty of the task and the need for task-specific adaptation. 


Figure 16: Zero-shot evaluation results for PaliGemma variants across tasks, prompt formats, and visual context sizes. Overall performance remains limited, indicating the need for task-specific adaptation. 

settings, we select the label with the highest similarity score as the predicted class. In the multi-frame setting, we compute predictions for each frame independently and use a majority vote to produce the final prediction. We also report two reference baselines for context: a random classifier, which achieves 12.5% on AR and 7.7% on CR, and a majority-class predictor, which yields 35.5% and 17.6% respectively. These are included only for calibration. 

39 

Preprint 

Table 16: Zero-shot accuracy-based evaluation of CLIP models and baseline methods on Action and Character Recognition tasks using 1 and 8 input frames. 

|**Fr**|**Model**|**Action Recognition**|**Character Recognition**|
|---|---|---|---|
||CLIP ViT-B/32|24.04_±_0.00|13.32_±_0.00|
|1|CLIP ViT-B/16|52.67_±_0.00|16.47_±_0.00|
||CLIP ViT-L/14|24.60_±_0.00|9.95_±_0.00|
||CLIP ViT-L/14-336|12.17_±_0.00|8.85_±_0.05|
||CLIP ViT-B/32|36.22_±_0.00|14.41_±_0.00|
|8|CLIP ViT-B/16|57.36_±_0.00|17.24_±_0.00|
||CLIP ViT-L/14|17.57_±_0.00|10.10_±_0.00|
||CLIP ViT-L/14-336|23.12_±_0.00|8.64_±_0.00|


Table 17: Performance on Action and Character Recognition tasks after LoRA-based adaptation with varying ranks ( _r ∈{_ 8 _,_ 16 _,_ 32 _,_ 48 _,_ 64 _}_ ). Adapters are applied to attention and MLP layers in both vision and language components. 

||**Bin**|**ary**|**Multipl**|**e-choice**|**Open**|**-ended**|
|---|---|---|---|---|---|---|
|**Rank**|**EM**|**ROUGE**|**EM**|**ROUGE**|**EM**|**ROUGE**|
||||**Action Recogn**|**ition**|||
|8|44.66_±_0.21|44.66_±_0.21|0.02_±_0.00|9.21_±_0.00|0.00_±_0.00|12.49_±_0.00|
|16|44.47_±_0.43|44.47_±_0.43|0.02_±_0.00|9.21_±_0.00|0.00_±_0.00|12.49_±_0.00|
|32|44.59_±_0.03|44.59_±_0.03|0.02_±_0.00|9.21_±_0.00|0.00_±_0.00|12.49_±_0.00|
|48|46.71_±_3.20|46.71_±_3.20|0.02_±_0.00|9.21_±_0.00|0.00_±_0.00|12.49_±_0.00|
|64|48.67_±_0.13|48.67_±_0.13|0.02_±_0.00|9.21_±_0.00|0.00_±_0.00|12.49_±_0.00|
|||**C**|**haracter Reco**|**gnition**|||
|8|48.76_±_0.00|48.76_±_0.00|0.00_±_0.00|0.32_±_0.00|0.00_±_0.00|0.01_±_0.01|
|16|48.62_±_0.23|48.62_±_0.23|0.00_±_0.00|0.14_±_0.00|0.00_±_0.00|0.05_±_0.00|
|32|48.98_±_0.08|48.98_±_0.08|0.00_±_0.00|0.14_±_0.00|0.00_±_0.00|0.05_±_0.00|
|48|48.91_±_0.09|48.91_±_0.09|0.00_±_0.00|0.14_±_0.00|0.00_±_0.00|0.05_±_0.00|
|64|48.72_±_0.06|48.72_±_0.06|0.00_±_0.00|0.14_±_0.00|0.00_±_0.00|0.05_±_0.00|


**Results.** Table 16 demonstrates the results. While CLIP ViT-B/16 performs relatively well on AR in both input settings, performance remains inconsistent across model scales and tasks. In particular, CR accuracy remains low, reflecting CLIP’s limited grounding in domain-specific visual semantics and fine-grained identity resolution. Larger CLIP models such as ViT-L/14 do not consistently outperform smaller variants, and 8-frame inputs provide only marginal gains over single-frame inputs. 

Overall, these results suggest that while CLIPScore offers a lightweight and scalable evaluation proxy, it lacks the temporal grounding and semantic specificity required for structured rollout evaluation. Performance falls short relative to our selected baselines, and the method is inherently constrained to predefined candidate sets—limiting its applicability to open-ended or compositional tasks. As such, we exclude CLIP-based scores from our primary comparisons and instead focus on adapted, generative VLM-based evaluators. 

### G.4 LOW-RANK ADAPTATION COMPARISONS 

This section presents an extended analysis of low-rank adaptation (LoRA) as a parameter-efficient strategy for adapting vision-language models to our protocol. We systematically vary the rank parameter _r_ and measure its impact on Action and Character Recognition performance across all prompt formats. All experiments in this section are conducted using PaliGemma 2 (3B) as the backbone model, consistent with the main fine-tuning results. These experiments assess whether increasing rank provides meaningful gains, and inform our decision to report only the rank-8 setting in the main paper. 

40 

Preprint 

Table 18: Pearson correlation between FVD and UNIVERSE across experimental settings. None of the correlations are statistically significant (all _p >_ 0 _._ 05). 

|**Setting**|**Action Recognition**|**Character Recognition**|
|---|---|---|
|1|0.09|0.03|
|2|-0.07|-0.08|
|3|-0.17|0.06|
|4|-0.03|-0.10|
|5|0.07|-0.25|
|6|-0.01|0.21|
|7|0.32|0.03|
|8|-0.10|0.33|


**Results.** Table 17 presents the performance of LoRA-based adaptation across a range of rank values ( _r ∈{_ 8 _,_ 16 _,_ 32 _,_ 48 _,_ 64 _}_ ) for both Action Recognition (AR) and Character Recognition (CR) tasks, across all prompt formats. We report exact match (EM) and ROUGE-F1 averaged over three runs. Increasing the rank beyond _r_ = 8 yields no consistent improvements across tasks or formats. Performance on binary prompts remains close to random, while performance on multiple-choice and open-ended formats stays near zero across all ranks. These results suggest that LoRA, even with increased capacity, is insufficient for capturing the fine-grained temporal and semantic dependencies required by our evaluation protocol. Given the lack of benefit from increasing rank—and the added parameter cost—it is inefficient to scale LoRA rank beyond _r_ = 8. Accordingly, all results reported in the main paper use _r_ = 8, while extended comparisons with higher ranks are presented here for completeness. 

## H COMPARISON WITH EXISTING EVALUATION BASELINES 

To validate that UNIVERSE captures evaluation dimensions beyond existing automated metrics, we analyze its correlation with two representative baselines: Fréchet Video Distance (FVD), a standard distributional metric for video generation quality, and VBench, a comprehensive multi-dimensional benchmark for text-to-video evaluation. These comparisons assess whether UNIVERSE’s focus on action-conditioned semantic alignment provides complementary signal to metrics designed primarily for perceptual quality and temporal coherence. 

### H.1 COMPARISON WITH FVD 

FVD Unterthiner et al. (2018) is a widely used reference-free metric for evaluating generative video models, defined as a distance between feature distributions of real and generated videos. Although commonly treated as a default quantitative proxy for rollout quality in world-model evaluation, FVD is agnostic to task semantics and action alignment—the dimensions UNIVERSE is specifically designed to capture. Across the eight environments, raw FVD values are tightly clustered (means between 3.23 and 3.27 with standard deviations below 0.05), reflecting limited dynamic range and strong datasetdependent scale effects. As a result, raw scores are not directly comparable across settings, making correlations a more informative basis for analysis. We therefore assess the relationship between the two metrics by computing Pearson correlations between FVD and UNIVERSE’s human-aligned scores across all environments for both Action Recognition and Character Recognition tasks. 

**Results.** For each environment (Settings 1–8) and each task, we obtain FVD scores on the same set of rollouts evaluated by UNIVERSE, report the scores and compute the correlation between the two. The resulting coefficients are reported in Table 18. Correlations are small in magnitude and unstable in sign, ranging from _−_ 0 _._ 25 to 0 _._ 33, with most values close to zero. The largest positive correlations are modest (Action Recognition, Setting 7: _r_ = 0 _._ 32; Character Recognition, Setting 8: _r_ = 0 _._ 33), and several settings exhibit weak negative correlations (e.g., Character Recognition, Setting 5: _r_ = _−_ 0 _._ 25). None of these correlations are statistically significant ( _p >_ 0 _._ 05 for all settings), indicating UNIVERSE captures complementary semantic cues. These results demonstrate that FVD and UNIVERSE provide complementary evaluation signals: FVD captures distribution- 

41 

Preprint 


Figure 17: Correlation between UNIVERSE and VBench evaluation suite across eight environments and six dimensions. The _human action_ dimension is omitted as it was constant and non-informative. Correlations remain consistently low to moderate (|r| < 0.4), with none of the correlations are statistically significant (all _p >_ 0 _._ 05). 

level perceptual quality and temporal coherence, while UNIVERSE quantifies task-specific semantic alignment through human-grounded assessment. 

### H.2 CORRELATION WITH VBENCH METRICS 

To validate that UNIVERSE captures evaluative dimensions beyond existing automated benchmarks, we compare its human-aligned evaluation scores against VBench Huang et al. (2024), a comprehensive state-of-the-art benchmark for generative video evaluation. We computed correlations on identical rollout sets across eight experimental environments using six evaluation configurations, parameterized by task (Action Recognition or Character Recognition) and prompt type (binary, multiple-choice, open-ended). The analysis spans seven VBench dimensions: Temporal Flickering, Temporal Style, Background Consistency, Overall Consistency, Subject Consistency, Dynamic Degree, and Human Action. The Human Action dimension is omitted from visualization as it exhibited no variance across samples. 

**Results.** Figure 17 shows that correlations between UNIVERSE and VBench metrics remain consistently low to moderate ( _|r| <_ 0 _._ 4) across all valid comparisons. Average correlations range from -0.037 for Subject Consistency to 0.06 for Temporal Flickering, with most values falling within 0.1-0.4. Notably, the sign variability across settings (including both positive and negative correlations) indicates that UNIVERSE captures complementary semantic cues not reflected in VBench’s quality dimensions. This divergence is expected: while VBench focuses on low-level perceptual quality and temporal coherence, UNIVERSE explicitly targets semantic alignment. 

**Summary.** The consistent orthogonality observed across both analyses demonstrates that UNIVERSE provides a complementary evaluation dimension to existing benchmarks. While standard distributional metrics (FVD) capture visual fidelity and text-to-video benchmarks (VBench) assess perceptual quality, UNIVERSE quantifies action-conditioned semantic alignment through human-grounded evaluation. Comprehensive world model assessment therefore benefits from combining these approaches: existing metrics for perceptual coherence and UNIVERSE for task-relevant semantic fidelity. 

42 

