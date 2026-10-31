---
title: "HiST-VLA: A Hierarchical Spatio-Temporal Vision-Language-Action Model for End-to-End Autonomous Driving"
date: "2026-02-11"
authors: "Yiru Wang; Zichong Gu; Yu Gao; Anqing Jiang; Zhigang Sun; Shuo Wang"
url: https://arxiv.org/abs/2602.13329
pdf: https://arxiv.org/pdf/2602.13329
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.13329)** / [論文ページ](https://arxiv.org/abs/2602.13329)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HiST-VLA: A Hierarchical Spatio-Temporal Vision-Language-Action Model for End-to-End Autonomous Driving** 

Yiru Wang<sup>1</sup> , Zichong Gu<sup>2</sup> , Yu Gao<sup>1</sup> , Anqing Jiang<sup>1</sup> , Zhigang Sun<sup>1</sup> , Shuo Wang<sup>1</sup> , Yuwen Heng<sup>1</sup> , Hao Sun<sup>1</sup> 

**_Abstract_ — Vision-Language-Action (VLA) models offer promising capabilities for autonomous driving through multimodal understanding. However, their utilization in safetycritical scenarios is constrained by inherent limitations, including imprecise numerical reasoning, weak 3D spatial awareness, and high sensitivity to context. To address these challenges, we propose HiST-VLA, a novel** **_Hi_ erarchical** **_S_ patio-** **_T_ emporal VLA model designed for reliable trajectory generation.** 

**Our framework enhances 3D spatial and temporal reasoning by integrating geometric awareness with fine-grained driving commands and state history prompting. To ensure computational efficiency, we integrate dynamic token sparsification into the VLA architecture. This approach fuses redundant tokens rather than filtering them, effectively reducing redundancy without sacrificing model performance. Furthermore, we employ a hierarchical transformer-based planner to progressively refine coarse VLA waypoints into fine-grained trajectories. Crucially, the planner utilizes dynamic latent regularization to incorporate language commands, ensuring strict spatial grounding and temporal coherence. Extensive evaluation on the NAVSIM v2 benchmark demonstrates state-of-the-art performance on Navtest, achieving an EPDMS of 88.6, and EPDMS of 50.9 on pseudo closed-loop Navhard benchmark.** 

## I. INTRODUCTION 

Contemporary autonomous driving (AD) systems operate through a cascaded pipeline of perception, prediction, planning, and control to achieve real-time environment understanding and behavior generation. While demonstrating reliability in typical scenarios, these architectures remain susceptible to failures at module boundaries and often underperform in complex social interactions or require deeper semantic reasoning. 

Recent advances in vision-language models (VLMs) have shown extensive semantic knowledge and strong generalization to unfamiliar inputs. They can interpret complex scenes and detect rare objects often missed by conventional perception modules. Integrating these capabilities into AD systems by fine-tuning pre-trained VLMs on diverse driving datasets, can significantly enhance robustness in challenging scenarios and enable human-AD interaction. A prevalent strategy for such integration is VLM-enhanced end-to-end (E2E) dualsystem architecture [1]–[3]. However, a key challenge lies in the loose coupling between high-level language outputs and low-level vehicle control, which can lead to unreliable 

This work was supported by Bosch Corporate Research. ( _Corresponding author: : hao.sun4@cn.bosch.com_ ) 

> 1 Yiru Wang, Yu Gao, Anqing Jiang, Zhigang Sun, Shuo Wang, Yuwen Heng, Hao Sun are with Bosch Corporate Research, Bosch (China) Investment Ltd., Shanghai, China. 

> 2 Zichong Gu is with School of Communication and Information Engineering, Shanghai University, Shanghai, China 

reactions to natural instructions and increased false positives. Additionally, performance heavily depends on large-scale annotated datasets, while intermediate representations often impair latency and generalizability. Thus, despite improving interpretability, loosely coupled VLM systems remain insufficient for generating fully trustworthy driving actions. 

Other than VLM dual systems, recent Vision-LanguageAction (VLA) models can be broadly categorized into two architectural paradigms: E2E VLA trajectory prediction models, and hybrid approaches where the VLA generates coarse trajectories that are subsequently refined by a dedicated trajectory head. Among these, E2E VLAs [4]–[7], which directly map multimodal inputs to trajectory sequences, can face limitations in aspects such as spatial reasoning, 3D geometric interpretation, and action-space granularity, affecting the model’s ability of detailed situational understanding and precise trajectory generation, especially in highly complex or unstructured driving scenarios. 

In contrast, the hybrid architecture [8]–[10], where a VLA generates an initial trajectory or trajectory tokens, subsequently refined by a secondary trajectory optimization head, offers a balance between architectural consistency and functional performance. This approach maintains the VLA as the core planner while compensating for its perceptual and representational limitations through a dedicated refinement module. The trajectory head, often implemented as a lightweight network or an optimization layer, enhances the physical plausibility, smoothness, kinematic feasibility, and task compliance of the resulting trajectory. This method is increasingly regarded as a “pure” VLA model extension, as it builds upon and refines the VLA’s inherent capabilities without relying on additional E2E systems. 

To address key limitations in current VLAs, such as the lack of granular 3D spatial awareness, insufficient temporal coherence, and difficulties in generating precise controlready trajectories, we propose HiST-VLA: a **_Hi_** erarchical **_S_** patially-grounded and **_T_** emporally coherent VLA that integrates 3D geometric reasoning and temporal modeling with multi-stage trajectory refinement. Unlike prior hybrid designs, our model introduces a novel hierarchical architecture supporting multi-stage decoding of coarse VLA trajectories, which enhances trajectory safety, comfort, and interpretability without auxiliary E2E models or costly annotations. The spatio-temporal VLA structure integrates enhanced 3D spatial understanding through explicit geometric encoding and temporal state prompting to capture historical states. This module further incorporates a dynamic token sparsification mechanism based on self-similarity in attention space, 

effectively reducing redundancy while preserving semantically critical features. Within an extended chain-of-thought (CoT) reasoning process, fine-grained driving commands are interpreted to strengthen spatial and behavioral alignment. The model outputs trajectories accompanied by confidence scores, explicitly indicating prediction certainty. This design not only enhances spatio-temporal grounding but also enables efficient, semantics-aware reasoning, supporting the generation of precise and reliability-conscious trajectories. 

Furthermore, we propose a hierarchical planner that refines the coarse trajectory from the VLA through structured processing stages. The pipeline employs a variational autoencoder (VAE) to learn compact latent representations of feasible trajectories, further enabling efficient semantic alignment with interpreted driving commands. This is followed by a scorer-guided optimization step to enhance safety, feasibility, and comfort. This multi-granular refinement strategy significantly extends conventional single-stage decoders, effectively bridging high-level instructions and executable controls in a fully differentiable architecture. 

To ensure a comprehensive and realistic validation of our VLA-based driving system, we leverage the NAVSIM v2 benchmark [11]. This framework provides a rigorous evaluation that integrates both open-loop and pseudo closedloop testing, offering a more reliable and robust assessment of real-world driving performance compared to traditional offline metrics. 

Our contributions can be summarized as follows: 

- HiST-VLA Architecture: A novel framework that integrates spatial grounding and temporal coherence with multi-stage trajectory refinement in a fully integrated framework, enhancing trajectory comfort and safety. 

- Efficient Spatio-Temporal Representation with Token Sparsification: Incorporates 3D encoding and temporal state prompting with a dynamic token sparsification mechanism. By leveraging self-similarity guided token fusion, our approach effectively reduces redundancy while preserving semantically critical features. 

- Semantics-Aligned Hierarchical Planning: Refines trajectories via a multi-stage pipeline aligning granular driving commands with motion, ensuring safety and comfort trajectory generation through confidence-aware regularization and multi-criteria scoring. 

## II. RELATED WORK 

## _A. E2E Autonomous Driving_ 

Autonomous driving systems have transitioned to E2E approaches that map sensors directly to controllable waypoints [12], [13]. To address challenges in data efficiency and robustness, recent works introduce efficient vectorized (VAD [14]) and sparse architectures (SparseDrive [15]). While optimization-based refinement exists [16], newer methods focus on expressive policies via iterative refinement (iPad [17]). SimScale further improves generalization through scalable simulation and data co-training [18]. Despite these advances, most E2E methods still lack semantic 

interpretability and natural language interfaces for humanvehicle interaction. 

## _B. VLM for E2E Autonomous Driving_ 

The integration of linguistic modalities leverages LLMs and VLMs to enhance reasoning, interpretability, and generalization in vehicle decision-making. By leveraging large language models (LLMs) and VLMs [19], [20], modern systems unify perception and reasoning within a shared semantic space, incorporating commonsense knowledge (e.g., “flashing hazard lights” implies “vehicle in distress”) to improve adaptation to novel scenarios [1], [2]. 

However, foundation models face challenges including limited spatial awareness, imprecise outputs, high latency, and hallucination risks. Recent work addresses these limitations by improving spatial representations [21]–[23] and reduce latency through distillation or advisory architectures [24], [25]. In spite of these advancements, current VLM-based driving systems often lack closed-loop control integration, and struggle to align semantic reasoning with safe, continuous motion planning. 

## _C. VLA in E2E Autonomous Driving_ 

Inspired by advances in embodied intelligence [26], [27], recent works integrate multimodal perception and language into unified architectures to bridge the semantic-control gap. These VLA models forms cohesive perception-reasoningcontrol pipelines that support adaptation to rare scenarios, robustness under partial observability, and comprehension of high-level instructions [10], [28]. Built upon VLMs, VLAs exhibit strong cross-domain generalization. Some explicitly model multi-step CoT reasoning for interpretability, as in DriveCoT [29]. Others focus on aligning language to actions: Orion bridges a language reasoning space and a trajectory action space via a generative planner [9], while SimLingo unifies closed-loop driving with vision-language understanding and language-action alignment [6]. To improve driving quality, others incorporate advanced optimization mechanisms: RecogDrive utilizes a diffusion-based planner to generate diverse, human-like trajectories [8], while IRL-VLA employs a reward world model to enable efficient closed-loop optimization without relying on high-fidelity simulation [3]. 

Despite these advances, current VLAs often lack the granular 3D spatial reasoning and temporal coherence required for robust, control-ready planning in dynamic environments. 

## III. METHOD 

In this paper, we propose HiST-VLA, an E2E framework that integrates perception, semantic reasoning, and trajectory planning within a unified architecture. The framework comprises: (1) a unified architecture combining 3D-aware geometric representation and semantic reasoning for multistage trajectory refinement, (2) a Spatio-Temporal VLA backbone featuring multi-view 3D understanding, temporal modeling, CoT reasoning and dynamic token sparsification to reduce redundancy; and (3) a hierarchical planner that generates continuous trajectories from coarse VLA outputs via semantic conditioning and multi-criteria scoring. 


Fig. 1. The Framework of the proposed HiST-VLA, including the Spatio-Temporal VLA architecture, hierarchical planner and main training stages. 

## _A. HiST-VLA Framework_ 

As illustrated in Fig. 1, the Spatio-Temporal VLA and hierarchical planner enable spatial grounding, temporal modeling and precise trajectory refinement through a multistage process. The Spatio-Temporal VLA acts as the primary policy generator, responsible for producing an initial driving plan and coarse trajectories. Given multi-view camera inputs _C_ of the current timestep _t_ , the Spatio-Temporal VLA first processes the visual inputs through a vision encoder to obtain _Fv_ . This representation is further enhanced with depth estimation **_ED_** and the combined 3D visual features are processed by a dynamic token sparser to produce spatiallyaware visual tokens. Concurrently, the instruction _S_ , the time-series navigation information _I_ = ( _it, it−_ 1 _, ..., it−k_ ) and time-series ego-vehicle states _E_ = ( _et, et−_ 1 _, ..., et−k_ ) for the past _k_ frames are encoded by a text encoder. These visual tokens and textual embeddings are then fed into the large language model (LLM). Following a CoT reasoning process, the model then auto-regressively generates three outputs based on the derived reasoning steps: a granular driving command _Dc_ for the next four seconds, a candidate trajectory _τ_ 0 with a confidence score _ϵ_ . 

Then the hierarchical planner optimizes the coarse trajectory _τ_ 0. It first encodes _τ_ 0 into a latent space using a VAE and then semantically aligns it with the granular driving command _Dc_ . A multi-criteria scorer then assesses feasibility, safety, and comfort, refining it through additive offsets to produce an optimized trajectory _τ_<sup>_∗_</sup> . This multistage refinement mechanism forms the core of our hierarchical planning strategy, enabling progressive refinement from coarse trajectory and semantic intention to precise motion. 

## _B. Spatio-Temporal VLA Model_ 

Fig. 2 illustrates the Spatio-Temporal VLA model, which integrates spatially-aware visual inputs and temporal history to enable structured reasoning. Its architecture is detailed in the following sub-sections. 

_1) Spatially-Aware Visual Encoding:_ We extract 2D patch features from multi-view images using a ViT-L/14 from 

CLIP [30] as vision encoder. To recover 3D scene geometry, a pretrained monocular depth estimator [31] generates dense depth maps. Using camera intrinsics, each 2D image patch is back-projected into the ego-vehicle’s 3D coordinate frame. The resulting 3D coordinates are encoded via a Multi-Layer Perceptron (MLP) with positional embeddings, and this encoded 3D information is added to the original 2D features. This process yields spatially-augmented visual tokens that explicitly encode the metric structure of the scene. 

_2) Dynamic Token Sparser:_ Unlike conventional methods that apply MLPs to transform all image tokens equally without explicit selection [2], [32], our approach leverages the intrinsic self-attention scores of image tokens to perform adaptive token sparsification. This module is built upon the intra-block Joint Token Pruning and Squeezing (eTPS) [33]. By retaining tokens with high self-attention activation and merging less salient ones, we achieve more efficient and feature-aware visual token reduction. The top- _k_ most informative tokens are retained, while the remaining tokens are adaptively merged into the kept ones through a learnable transformer-based fusion module. This self-similarity guided merging mechanism preserves structurally critical regions while reducing computational sequence length. The resulting compressed visual tokens are projected into the LLM’s embedding space to enable efficient multimodal interaction. 

_3) Temporal State Modeling:_ Furthermore, to enhance the smoothness and comfort of the generated driving commands and trajectories, we incorporate temporal modeling into the text prompt. Specifically, the long-term navigation information _I_ (discrete maneuver labels: left, straight, right [11]) and ego vehicle states _E_ (longitudinal/latitudinal speed/velocity: _vx_ , _vy_ , _ax_ , _ay_ ) for the previous _k_ frames are used as part of the prompt for the current step _t_ . The above text, along with the user instruction ( _What are your predicted driving intention and waypoints for next four seconds?_ ), is inserted into the prompt. This prompt conditioning transforms the model from a reactive function _π_ ( _at|st_ ) to a more informed function _π_ ( _at|st, st−_ 1 _, ..., st−k_ ), where _st_ = ( _it, et_ ), improv- 


Fig. 2. Spatio-Temporal VLA Model: Leveraging multi-view images, long-term navigation information, and ego state, our model employs CoT reasoning and dynamic token sparsification to produce a granular driving command and a coarse trajectory with confidence for the next four seconds. 

ing temporal coherence, reducing abrupt command changes, and yielding more continuous, human-like trajectory planning that better aligns with comfort expectations. 

_4) Granular Meta-Action and Confidence-Aware Trajectory Reasoning Enhanced CoT:_ The CoT performs structured reasoning to generate justified driving actions. Given the fused multimodal input, the LLM first analyzes the ego state and perceived scene context, interprets the high-level semantic intent conveyed by the language instruction (e.g., “Turn Left”), and proposes a granular driving command for the next four seconds. Prior work in meta-action planning often struggles to capture the nuanced intent embedded in language instructions, relying on simplistic categorical actions [1], [2], [34] (e.g., Lateral: Left, Straight, Right; Longitudinal: Accelerate, Keep, Decelerate), which lack the expressiveness for nuanced vehicle control. Such coarse discretizations fail to capture essential behavioral variations, resulting in suboptimal performance in complex scenarios. 

To overcome this and further enhance the spatial awareness of VLA, we introduce a finely-grained metaaction schema designed directly from the geometric and kinematic characteristics of real-world trajectories. Rather than relying on basic directional and speed labels, our method derives action distinctions from the shape and profile of future trajectory truths. For lateral control, we propose a diverse set of primitives including: Sharp ~~L~~ eft ~~T~~ urn, Slight ~~L~~ eft ~~T~~ urn, Left ~~L~~ aneChange, Sharp ~~R~~ ight ~~T~~ urn, Slight ~~R~~ ight ~~T~~ urn, Right ~~L~~ aneChange, Straight ~~S~~ trict, and Lane ~~M~~ icro ~~A~~ djust. This reflects tangible differences in curvature and lateral displacement, allowing the model to differentiate between subtle variations of a single language command like “Turn Left”. 

For longitudinal control, we define a hierarchy of ac- 

celeration profiles based on kinematic patterns: Full ~~S~~ top, Creeping, Emergency ~~D~~ ecel, Mild ~~D~~ ecel, Controlled ~~D~~ ecel, Constant ~~S~~ peed ~~L~~ oose, Constant ~~S~~ peed ~~S~~ trict, Mild ~~A~~ ccel and Aggressive ~~A~~ ccel, covering a spectrum from precise speed keeping to safety-critical deceleration. This granularity allows the model to precisely execute complex instructions that involve speed adjustments. 

The proposed granular driving command reasoning, translating semantic intent into precise actions, significantly improves discriminative capacity for decision-making and generates smoother, more human-like behavior. Based on this command, the model generates a coarse trajectory _τ_ 0 that geometrically instantiates the intended maneuver. Finally, the model estimates a confidence score _ϵ_ for the proposed trajectory. This score is derived derived from token confidences. For each token, the final transformer layer of the VLA produces a probability distribution via a softmax function, and the token’s confidence is the maximum probability in this distribution. The overall trajectory confidence _ϵ_ is then calculated as the geometric mean of these individual token confidences. This multi-step reasoning approach not only decomposes the decision process into human-interpretable stages but also contributes to improved trustworthiness in motion planning. 

## _C. Transformer-based Hierarchical Planner_ 

The coarse trajectory _τ_ 0 from the Spatio-Temporal VLA serves as a semantic and structural prior for the hierarchical planner. In the first refinement stage, we introduce a confidence-aware VAE module that dynamically perturbs and regularizes _τ_ 0 based on its confidence score _s_ . The latent feature of the trajectory is sampled from _N_ ( _µ, σ_<sup>2</sup> ), where the variance _σ_<sup>2</sup> = _α_ (1 _− s_ ) and _α_ as a scaling factor. This adaptive noise injection focuses refinement on regions of 

high uncertainty, improving both efficiency and targeting. 

The encoded trajectory features are then fused with the granular driving command embedding through multi-head cross-attention, enabling dynamic alignment of latent maneuver representations with precise control objectives. A lightweight pre-trained Scorer module, introduced in the prior work [3] and trained on NAVSIM v2 [11], selects the highest-scoring candidate trajectory _τ_<sup>_∗_</sup> by predicting the Extended Predictive Driver Model Score (EPDMS). This score assesses trajectories based on safety, efficiency, and comfort criteria, enabling simulator-free evaluation. 

The transformer-based trajectory head refines candidate trajectories by leveraging geometric constraints, and latent distribution regularization. Specifically, the refinement loss _L_ refine is a weighted combination of an L1 regression term for geometric alignment, and a KL divergence constraint from the confidence-aware VAE: 


where _L_ 1 is the L1 loss deviation from ground truth trajectory _τ_ gt, _p_ ( **z** ) is a standard Gaussian prior, and _q_ ( **z** _|τ_<sup>_∗_(</sup><sup>_i_)</sup> ) is the latent distribution for the _i_ -th candidate of trajectory _τ_<sup>_∗_</sup> , promoting safe and high-scoring trajectories. 

Leveraging confidence-aware regularization, semanticsguided optimization, and multi-criteria scoring, our multistage planner progressively refines _τ_ 0 into a dynamically feasible and contextually appropriate trajectory. The hierarchical architecture ensures both high-level interpretability and lowlevel control precision: the Spatio-Temporal VLA generates semantic proposals and coarse trajectories, while the subsequent refinement stages handle geometric optimization. _D. Training Strategy_ 

Our training process consists of three sequential stages, as illustrated in Fig 1: First, we pre-train the dynamic token sparser. Next, we jointly optimize the sparser, LLM, and text encoder to enable reasoning of granular driving commands, coarse trajectories, and confidence scores. Finally, we train the command encoder and the transformer-based hierarchical trajectory head by minimizing _L_ refine. The visual questionanswering (VQA) data used in these stages are generated from ground truth trajectories, as described in Sec. III-B.4. 

## IV. EXPERIMENTS 

To validate the effectiveness of our proposed framework, we conduct comprehensive evaluations on the established NAVSIM v2 benchmark [11], comparing against a range of state-of-the-art methods. We further perform detailed ablation studies to isolate the contribution of each key component within our architecture. 

## _A. Experimental Setup and Metrics_ 

Our analysis uses two NAVSIM v2 benchmarks: the Navtest set for general open-loop planning, and the more challenging Navhard set, designed to evaluate robustness under pseudo closed-loop conditions through synthetic perturbations. Performance is rigorously evaluated using the EPDMS, a comprehensive score that aggregates nine critical 

sub-metrics: No At-Fault Collision (NC), Drivable Area Compliance (DAC), Driving Direction Compliance (DDC), Traffic Light Compliance (TLC), Ego Progress (EP), Time to Collision (TTC), Lane Keeping (LK), History Comfort (HC), and Extended Comfort (EC). The EPDMS score provides a holistic measure of an autonomous driving system’s safety, efficiency, and comfort. 

Our implementation builds upon LLaVA-v1.5-7B [32] as the base VLM, which comprises 7 billion parameters, integrates ViT-L/14 from CLIP as the vison encoder, MLPs for vision-language adapter, and Vicuna-7B as the LLM. We enhance this architecture by incorporating depth-aware spatial encoding and replacing the standard adapter with our proposed dynamic token sparsification module, as detailed in Sections III-B.1 and III-B.2. 

Our model is first pre-trained for 1 epoch on the NAVSIM trainval split using 8 × NVIDIA H20 GPUs with a batch size of 32 and a learning rate of 1 _×_ 10<sup>_−_3</sup> . Subsequently, stage-1 training is performed under the same hardware setup for 1 epoch on trainval, with a batch size of 8 and a learning rate of 1 _×_ 10<sup>_−_5</sup> . Finally, stage-2 training is conducted on the navtrain split for 30 epochs using 8 × NVIDIA A800 GPUs, a batch size of 2, and a learning rate of 1 _×_ 10<sup>_−_5</sup> . 

We evaluate two variants of our proposed model: **HiSTE2E** uses a ResNet-34 [41] backbone to extract visual features, HiST-VLA to generate granular driving commands only, and then feeds these features to an external motion planner (DiffusionDrive [37]) to produce the final trajectory; and **HiST-VLA** , our fully integrated “pure” VLA model that directly generates trajectories without relying on any external E2E modules, operating as a single unified system. 

## _B. Quantitative Results_ 

_1) Performance on Navtest Benchmark:_ Table I summarizes the experimental results on the NAVSIM v2 Navtest benchmark. Notably, our HiST-VLA model establishes a new state-of-the-art with an EPDMS score of 88.6, significantly outperforming established baselines such as VADv2 (76.6), Transfuser (76.7), and prior SOTA methods including DriveSuprim (87.1), the diffusion-based DiffusionDrive (84.3), GTRS-Dence w/ SimScale (84.6) and ZTRS (86.2). Remarkably, this score closely approaches the human expert performance of 90.3, demonstrating the model’s humanlike decision-making capabilities. Such robust performance is anchored by exceptional results in safety-critical metrics, specifically NC (99.6), DAC (99.1), DDC (99.7), and LK (98.9), proving the effectiveness of our hierarchical design in ensuring driving safety. Crucially, the HiST-E2E variant, which fuses the driving command only from HiST-VLA and uses an external E2E planner (DiffusionDrive [37]) to produce the final trajectory, also attains a competitive EPDMS score of 85.4, surpassing the DiffusionDrive baseline (84.3). This result validates that our spatio-temporal reasoning mechanism provides substantial performance gains even when integrated with external planners, highlighting its generalizability. Collectively, these results confirm the superiority of our proposed framework. 

TABLE I 

EVALUATION ON NAVSIM V2 NAVTEST BENCHMARK FOR PLANNING ORIENTED E2E AUTONOMOUS DRIVING. 

|**Method**|**VLM**|**VLA**|**NC** _↑_|**DAC** _↑_|**DDC** _↑_|**TL** _↑_|**EP** _↑_|**TTC** _↑_|**LK** _↑_|**HC** _↑_|**EC** _↑_|**EPDMS** _↑_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Human Agent|✗|✗|100|100|99.8|100|87.4|100|100|98.1|90.1|90.3|
|Transfuser [12]|✗|✗|96.9|89.9|97.8|99.7|87.1|95.4|92.7|98.3|87.2|76.7|
|VADv2 [16]|✗|✗|97.3|91.7|77.6|92.7|100|99.9|98.2|66.0|97.4|76.6|
|HydraMDP++ [35]|✗|✗|97.2|97.5|99.4|99.6|83.1|96.5|94.4|98.2|70.9|81.4|
|GTRS-Dense [36]|✗|✗|97.6|98.5|99.5|99.9|89.5|97.2|96.8|97.2|57.2|84.0|
|GTRS-Dence w/ SimScale [18]|✗|✗|98.4|98.8|99.4|99.9|87.9|98.1|96.4|97.6|58.8|84.6|
|DiffusionDrive [37]|✗|✗|98.0|96.0|99.5|99.8|87.7|97.1|97.2|98.3|87.6|84.3|
|ZTRS [38]|✗|✗|98.2|99.1|99.7|99.8|86.9|97.5|96.6|98.2|78.2|86.2|
|DriveSuprim [39]|✗|✗|98.4|98.6|99.6|99.8|90.5|97.8|97.0|98.3|78.6|87.1|
|Senna-E2E [2]|✓|✗|98.4|97.4|99.6|99.8|83.8|97.9|97.3|98.3|85.2|84.8|
|**HiST-E2E (Ours)**|✓|✗|98.6|97.8|99.6|99.8|83.9|98.1|97.3|98.3|85.1|**85.4(**+1_._3%**)**|
|**HiST-VLA (Ours)**|✓|✓|99.6|99.1|99.7|99.9|89.2|99.4|98.9|98.4|66.0|**88.6**|


TABLE II 

EVALUATION ON NAVSIM-V2 NAVHARD BENCHMARK FOR PLANNING ORIENTED E2E AUTONOMOUS DRIVING. 

|**Method**<br>|**VLM**|**VLA**|**Stage**|**NC**_↑_|**DAC**_↑_|**DDC**_↑_|**TLC**_↑_|**EP**_↑_|**TTC**_↑_|**LK**_↑_|**HC**_↑_|**EC**_↑_|**EPDMS**_↑_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|PDM-Closed [40]|✗|✗|Stage 1<br>Stage 2|94.4<br>88.1|98.8<br>90.6|100<br>96.3|99.5<br>98.5|100<br>100|93.5<br>83.1|99.3<br>73.7|87.7<br>91.5|36.0<br>25.4|51.3|
|Transfuser [12]|✗|✗|Stage 1<br>Stage 2|96.2<br>77.7|79.5<br>70.2|99.1<br>84.2|99.5<br>98.0|84.1<br>85.1|95.1<br>75.6|94.2<br>45.4|97.5<br>95.7|79.1<br>75.9|23.1|
|DiffusionDrive [37]|✗|✗|Stage 1<br>Stage 2|95.9<br>79.5|84.0<br>72.8|98.6<br>84.1|99.8<br>98.4|84.4<br>87.5|96.0<br>76.2|95.1<br>46.6|97.6<br>96.1|71.1<br>62.4|26.0|
|Senna-E2E [2]|✓|✗|Stage 1<br>Stage 2|95.6<br>78.6|86.0<br>74.8|98.9<br>84.8|99.6<br>98.2|83.9<br>88.2|95.1<br>75.7|95.3<br>46.9|97.6<br>96.0|75.6<br>65.8|27.2|
|ZTRS [38]|✗|✗|Stage 1<br>Stage 2|98.9<br>91.1|97.6<br>90.4|100<br>95.8|100<br>99.0|66.7<br>63.6|98.9<br>89.8|96.2<br>60.4|96.7<br>97.6|44<br>66.1|48.1|
|GTRS-Dence w/ SimScale [18]|✗|✗|Stage 1<br>Stage 2|99.1<br>92.3|98.2<br>93.8|99.8<br>94.9|100<br>99.3|71.9<br>75.4|99.3<br>90.7|95.6<br>60.3|93.8<br>95.9|28.0<br>37.4|47.2|
|GTRS-E [36]|✗|✗|Stage 1<br>Stage 2|98.9<br>92.3|99.3<br>93.3|99.8<br>94.6|99.8<br>99.2|75.2<br>73.1|98.4<br>91.2|96.0<br>53.9|97.6<br>96.7|51.6<br>56.8|49.4|
|**HiST-E2E (Ours)**|✓|✗|Stage 1<br>Stage 2|97.3<br>84.5|89.6<br>78.2|99.4<br>91.0|99.6<br>98.8|78.7<br>78.7|97.6<br>81.7|95.1<br>50.9|97.8<br>98.7|72.9<br>75.2|**34.2(**+31_._5%**)**|
|**HiST-VLA (Ours)**|✓|✓|Stage 1<br>Stage 2|99.8<br>86.4|98.7<br>83.7|99.7<br>89.9|99.6<br>98.5|87.3<br>87.5|99.6<br>83.1|99.6<br>56.7|97.8<br>96.3|73.3<br>60.9|**50.9**|


TABLE III 

_2) Performance on Navhard Benchmark:_ Table II presents the evaluation results on the rigorous Navhard benchmark, which is to test robustness in pseudo closed-loop scenarios. Our HiST-VLA model achieves a competitive EPDMS score of 50.9, substantially outperforming established baselines such as DiffusionDrive (26.0) and Transfuser (23.1), while exhibiting superior performance compared to GTRS-E (49.4). Furthermore, the HiST-E2E variant attains an EPDMS of 34.2, representing a remarkable 31.5% relative improvement over the DiffusionDrive planner baseline (26.0). This substantial gain validates that our spatio-temporal reasoning mechanism effectively enhances trajectory quality even when integrated with external planners. Collectively, these results demonstrate the robustness and generalizability of the HiST-VLA architecture across both open-loop (Navtest) and pseudo closed-loop (Navhard) settings. 

## _C. Ablation Studies_ 

To evaluate the contribution of each proposed component, we conduct three ablation studies on Navtest benchmark. 

ABLATION STUDY OF SPATIO-TEMPORAL VLA MODULES ON NAVTEST. 

|**Spatial**<br>**Encoding**|**Temporal**<br>**Prompting**|**Granular**<br>**Meta-Action**|**EPDMS** _↑_|
|---|---|---|---|
|✗|✗|✗|77.2|
|✗|✓|✓|85.0|
|✓|✗|✓|86.3|
|✓|✓|✗|83.3|
|✓|✓|✓|**88.6**|


_1) Component Analysis of Spatio-Temporal VLA:_ Table III presents an ablation study evaluating the contribution of each component in VLA model. The full HiSTVLA model achieves the highest EPDMS of 88.6, showing substantial gains over the baseline of 77.2, where we simply integrate LLaVA-7B model with the proposed hierarchical planner. Removing spatial encoding results in a score of 85.0, while omitting temporal prompting causes a drop to 86.3. The token sparsification module contributes modestly to the overall performance, with its absence reducing the 

score to 87.9. Most substantially, ablating the Granular MetaAction module leads to a pronounced decrease to 83.3, underscoring its critical role. These results demonstrate that all components contribute synergistically to the framework’s effectiveness, with the complete system achieving a remarkable 11.4-point improvement over the baseline. 

TABLE IV 

EFFICIENCY ANALYSIS OF SPATIO-TEMPORAL VLA ON NAVTEST. 

|**Dynamic Token Sparser**|**GFLOPs** _↓_|**EPDMS** _↑_|
|---|---|---|
|w/o|9,105<br>|87.9<br>|
|w/|**7,630(**_−_23_._7%|**)**<br>**88.6**|


_2) Efficiency Analysis of Dynamic Token Sparser Module:_ Table IV demonstrates the pivotal role of the dynamic token sparser in balancing computational efficiency and planning performance. Without the sparser, the model operates at a high computational cost of 9,105 GFLOPs, achieving an EPDMS of 87.9. By integrating the sparser with a fusion rate of 0.8, which effectively merges 20% of redundant vision tokens, the model eliminates visual noise and significantly reduces the computational load to 7,630 GFLOPs while simultaneously boosting the EPDMS to 88.6. 


Fig. 3. Trajectory visualization on Navhard across: (a) stage 1 real-world and (b) stage 2 synthetic scenes. Driving commands are shown above each scenario. Rows depict, from top to bottom: VLA coarse trajectory, semantics-aligned trajectory, and HiST-VLA trajectory. 

TABLE V 

ABLATION STUDY OF HIERARCHICAL PLANNER ON NAVTEST. 

|**HiST-VLA**<br>**Coarse Traj.**|**Semantics**<br>**Alignment**|**Regularization**<br>**& Scoring**|**EPDMS** _↑_|
|---|---|---|---|
|✓|✗|✗|73.1|
|✓|✓|✗|84.3|
|✓|✗|✓|85.0|
|✓|✓|✓|**88.6**|


_3) Module Analysis of Hierarchical Planner:_ Table V evaluates the hierarchical modules within the planner of our HiST-VLA framework. The baseline model, which outputs only a coarse trajectory without any planner, achieves an EPDMS score of 73.1. Incorporating the semanticsaligned granular driving command encoding module by a transformer-based planner leads to a significant improvement, raising the score to 84.3. When the confidence-aware regularization and the multi-criteria scorer is added to refine the coarse trajectory, performance increases to 85.0 EPDMS score, highlighting its essential role in enhancing safety and compliance through trajectory evaluation and correction. 

These results demonstrate that the proposed hierarchical components—individually and collectively—contribute substantially to the overall performance, establishing a new state-of-the-art in VLA autonomous driving systems. 

## _D. Trajecotory Visualization of Hierarchical Planner_ 

Figure 3 illustrates the hierarchical refinement of trajectories across two distinct scenarios: (a) stage 1 real-world and (b) stage 2 synthetic environments. In scenario (a), the coarse trajectory exhibits ambiguous intent, partially intruding into green spaces. In contrast, the trajectory refined by the confidence-aware regularization and scorer module is both smoother and more tightly aligned with the drivable 

area. In scenario (b), both the coarse and semantics-aligned trajectories infringe upon parked vehicles to the right. The final hierarchically-refined trajectory, however, successfully avoids these obstacles, demonstrating improved adaptability and safety awareness. These visual comparisons highlight the progressive enhancement achieved through our refinement pipeline. Each stage effectively addresses limitations present in the previous one, resulting in a robust and human-like motion planning outcome. 

## V. CONCLUSION 

This paper introduces HiST-VLA, a novel VLA framework designed to elevate autonomous driving systems through integrated 3D geometric reasoning and hierarchical trajectory refinement. By eliminating reliance on external E2E modules and expensive annotations, our approach significantly enhances spatial awareness and motion planning fidelity. The core of our architecture lies in two innovations: a spatio-temporally grounded reasoning module featuring dynamic token sparsification, and a hierarchical planner that aligns language commands with trajectory generation through confidence-aware regularization and multi-criteria scoring. Extensive experiments on NAVSIM v2 show that HiST-VLA achieves state-of-the-art performance on Navtest open-loop benchmark, with an EPDMS score of 88.6, markedly surpassing existing methods. Furthermore, comprehensive ablation studies validate the critical contribution of each individual component to the overall system efficacy. 

## REFERENCES 

> [1] A. Jiang, Y. Gao, Z. Sun, Y. Wang, J. Wang, J. Chai, Q. Cao, Y. Heng, H. Jiang, Y. Dong _et al._ , “Diffvla: Vision-language guided diffusion planning for autonomous driving,” _arXiv preprint arXiv:2505.19381_ , 2025. 

- [2] B. Jiang, S. Chen, B. Liao, X. Zhang, W. Yin, Q. Zhang, C. Huang, W. Liu, and X. Wang, “Senna: Bridging large visionlanguage models and end-to-end autonomous driving,” _arXiv preprint arXiv:2410.22313_ , 2024. 

- [3] A. Jiang, Y. Gao, Y. Wang, Z. Sun, S. Wang, Y. Heng, H. Sun, S. Tang, L. Zhu, J. Chai _et al._ , “Irl-vla: Training an vision-language-action policy via reward world model,” _arXiv preprint arXiv:2508.06571_ , 2025. 

- [4] H. Arai, K. Miwa, K. Sasaki, K. Watanabe, Y. Yamaguchi, S. Aoki, and I. Yamamoto, “Covla: Comprehensive vision-language-action dataset for autonomous driving,” in _2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ . IEEE, 2025, pp. 1933– 1943. 

- [5] J.-J. Hwang, R. Xu, H. Lin, W.-C. Hung, J. Ji, K. Choi, D. Huang, T. He, P. Covington, B. Sapp _et al._ , “Emma: End-to-end multimodal model for autonomous driving,” _arXiv preprint arXiv:2410.23262_ , 2024. 

- [6] K. Renz, L. Chen, E. Arani, and O. Sinavski, “Simlingo: Visiononly closed-loop autonomous driving with language-action alignment,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 11 993–12 003. 

- [7] X. Zhou, X. Han, F. Yang, Y. Ma, and A. C. Knoll, “Opendrivevla: Towards end-to-end autonomous driving with large vision language action model,” _arXiv preprint arXiv:2503.23463_ , 2025. 

- [8] Y. Li, K. Xiong, X. Guo, F. Li, S. Yan, G. Xu, L. Zhou, L. Chen, H. Sun, B. Wang _et al._ , “Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving,” _arXiv preprint arXiv:2506.08052_ , 2025. 

- [9] H. Fu, D. Zhang, Z. Zhao, J. Cui, D. Liang, C. Zhang, D. Zhang, H. Xie, B. Wang, and X. Bai, “Orion: A holistic end-to-end autonomous driving framework by vision-language instructed action generation,” _arXiv preprint arXiv:2503.19755_ , 2025. 

- [10] X. Tian, J. Gu, B. Li, Y. Liu, Y. Wang, Z. Zhao, K. Zhan, P. Jia, X. Lang, and H. Zhao, “Drivevlm: The convergence of autonomous driving and large vision-language models,” _arXiv preprint arXiv:2402.12289_ , 2024. 

- [11] D. Dauner, M. Hallgarten, T. Li, X. Weng, Z. Huang, Z. Yang, H. Li, I. Gilitschenski, B. Ivanovic, M. Pavone _et al._ , “Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 28 706– 28 719, 2024. 

- [12] K. Chitta, A. Prakash, B. Jaeger, Z. Yu, K. Renz, and A. Geiger, “Transfuser: Imitation with transformer-based sensor fusion for autonomous driving,” _IEEE transactions on pattern analysis and machine intelligence_ , vol. 45, no. 11, pp. 12 878–12 895, 2022. 

- [13] J. Hawke, R. Shen, C. Gurau, S. Sharma, D. Reda, N. Nikolov, P. Mazur, S. Micklethwaite, N. Griffiths, A. Shah _et al._ , “Urban driving with conditional imitation learning,” in _2020 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2020, pp. 251–257. 

- [14] B. Jiang, S. Chen, Q. Xu, B. Liao, J. Chen, H. Zhou, Q. Zhang, W. Liu, C. Huang, and X. Wang, “Vad: Vectorized scene representation for efficient autonomous driving,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2023, pp. 8340–8350. 

- [15] W. Sun, X. Lin, Y. Shi, C. Zhang, H. Wu, and S. Zheng, “Sparsedrive: End-to-end autonomous driving via sparse scene representation,” _arXiv preprint arXiv:2405.19620_ , 2024. 

- [16] S. Chen, B. Jiang, H. Gao, B. Liao, Q. Xu, Q. Zhang, C. Huang, W. Liu, and X. Wang, “Vadv2: End-to-end vectorized autonomous driving via probabilistic planning,” _arXiv preprint arXiv:2402.13243_ , 2024. 

- [17] K. Guo, H. Liu, X. Wu, J. Pan, and C. Lv, “ipad: Iterative proposal-centric end-to-end autonomous driving,” _arXiv preprint arXiv:2505.15111_ , 2025. 

- [18] H. Tian, T. Li, H. Liu, J. Yang, Y. Qiu, G. Li, J. Wang, Y. Gao, Z. Zhang, L. Wang _et al._ , “Simscale: Learning to drive via real-world simulation at scale,” _arXiv preprint arXiv:2511.23369_ , 2025. 

- [19] H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux, T. Lacroix, B. Rozi`ere, N. Goyal, E. Hambro, F. Azhar _et al._ , “Llama: Open and efficient foundation language models,” _arXiv preprint arXiv:2302.13971_ , 2023. 

- [20] H. Liu, C. Li, Q. Wu, and Y. J. Lee, “Visual instruction tuning,” _Advances in neural information processing systems_ , vol. 36, pp. 34 892–34 916, 2023. 

- [21] R. Tian, B. Li, X. Weng, Y. Chen, E. Schmerling, Y. Wang, B. Ivanovic, and M. Pavone, “Tokenize the world into object-level knowledge to address long-tail events in autonomous driving,” _arXiv preprint arXiv:2407.00959_ , 2024. 

- [22] K. Winter, M. Azer, and F. B. Flohr, “Bevdriver: Leveraging bev maps in llms for robust closed-loop driving,” _arXiv preprint arXiv:2503.03074_ , 2025. 

- [23] M. Zhai, C. Li, Z. Guo, N. Yang, X. Qin, S. Zhao, J. Han, J. Tao, Y. Wu, and Y. Jia, “World knowledge-enhanced reasoning using instruction-guided interactor in autonomous driving,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 39, no. 9, 2025, pp. 9842–9850. 

- [24] Y. Chen, Z.-h. Ding, Z. Wang, Y. Wang, L. Zhang, and S. Liu, “Asynchronous large language model enhanced planner for autonomous driving,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 22–38. 

- [25] C. Pan, B. Yaman, T. Nesti, A. Mallik, A. G. Allievi, S. Velipasalar, and L. Ren, “Vlp: Vision language planning for autonomous driving,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 14 760–14 769. 

- [26] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [27] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [28] Z. Xu, Y. Zhang, E. Xie, Z. Zhao, Y. Guo, K.-Y. K. Wong, Z. Li, and H. Zhao, “Drivegpt4: Interpretable end-to-end autonomous driving via large language model,” _IEEE Robotics and Automation Letters_ , 2024. 

- [29] T. Wang, E. Xie, R. Chu, Z. Li, and P. Luo, “Drivecot: Integrating chain-of-thought reasoning with end-to-end driving,” _arXiv preprint arXiv:2403.16996_ , 2024. 

- [30] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark _et al._ , “Learning transferable visual models from natural language supervision,” in _International conference on machine learning_ . PmLR, 2021, pp. 8748–8763. 

- [31] S. F. Bhat, R. Birkl, D. Wofk, P. Wonka, and M. M¨uller, “Zoedepth: Zero-shot transfer by combining relative and metric depth,” _arXiv preprint arXiv:2302.12288_ , 2023. 

- [32] H. Liu, C. Li, Y. Li, and Y. J. Lee, “Improved baselines with visual instruction tuning,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2024, pp. 26 296–26 306. 

- [33] S. Wei, T. Ye, S. Zhang, Y. Tang, and J. Liang, “Joint token pruning and squeezing towards more aggressive compression of vision transformers,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2023, pp. 2092–2101. 

- [34] B. Jiang, S. Chen, Q. Zhang, W. Liu, and X. Wang, “Alphadrive: Unleashing the power of vlms in autonomous driving via reinforcement learning and reasoning,” _arXiv preprint arXiv:2503.07608_ , 2025. 

- [35] K. Li, Z. Li, S. Lan, J. Liu, Y. Xie, Z. Wu, Z. Yu, J. M. Alvarez _et al._ , “Hydra-mdp++: Advancing end-to-end driving via hydra-distillation with expert-guided decision analysis.” 

- [36] Z. Li, W. Yao, Z. Wang, X. Sun, J. Chen, N. Chang, M. Shen, Z. Wu, S. Lan, and J. M. Alvarez, “Generalized trajectory scoring for end-toend multimodal planning,” _arXiv preprint arXiv:2506.06664_ , 2025. 

- [37] B. Liao, S. Chen, H. Yin, B. Jiang, C. Wang, S. Yan, X. Zhang, X. Li, Y. Zhang, Q. Zhang _et al._ , “Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 12 037–12 047. 

- [38] Z. Li, W. Yao, Z. Wang, X. Sun, J. Chen, N. Chang, M. Shen, J. Song, Z. Wu, S. Lan _et al._ , “Ztrs: Zero-imitation end-to-end autonomous driving with trajectory scoring,” _arXiv preprint arXiv:2510.24108_ , 2025. 

- [39] W. Yao, Z. Li, S. Lan, Z. Wang, X. Sun, J. M. Alvarez, and Z. Wu, “Drivesuprim: Towards precise trajectory selection for end-to-end planning,” _arXiv preprint arXiv:2506.06659_ , 2025. 

- [40] D. Dauner, M. Hallgarten, A. Geiger, and K. Chitta, “Parting with misconceptions about learning-based vehicle motion planning,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 1268–1281. 

- [41] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2016, pp. 770–778. 

