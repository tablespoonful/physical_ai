---
title: "ColaVLA: Leveraging Cognitive Latent Reasoning for Hierarchical Parallel Trajectory Planning in Autonomous Driving"
date: "2025-12-28"
authors: "Qihang Peng; Xuesong Chen; Chenye Yang; Shaoshuai Shi; Hongsheng Li"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2512.22939
pdf: https://arxiv.org/pdf/2512.22939
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.22939)** / [論文ページ](https://arxiv.org/abs/2512.22939)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **ColaVLA: Leveraging Cognitive Latent Reasoning for Hierarchical Parallel Trajectory Planning in Autonomous Driving** 

Qihang Peng<sup>1,2,3</sup> Xuesong Chen<sup>2, 3,</sup><sup>_†_</sup> Chenye Yang<sup>1</sup> Shaoshuai Shi<sup>3, �</sup> Hongsheng Li<sup>2, �</sup> 1 Tsinghua University 2 CUHK MMLab 3 Voyager Research, Didi Chuxing pqh22@mails.tsinghua.edu.cn, shaoshuaics@gmail.com, hsli@ee.cuhk.edu.hk 

> _†_ Project Leader �Corresponding author 

## **Abstract** 

_Autonomous driving requires generating safe and reliable trajectories from complex multimodal inputs. Traditional modular pipelines separate perception, prediction, and planning, while recent end-to-end (E2E) systems learn them jointly. Vision–language models (VLMs) further enrich this paradigm by introducing cross-modal priors and commonsense reasoning, yet current VLM-based planners face three key challenges: (i) a mismatch between discrete text reasoning and continuous control, (ii) high latency from autoregressive chain-of-thought decoding, and (iii) inefficient or non-causal planners that limit real-time deployment. We propose_ **_ColaVLA_** _, a unified vision–language–action framework that transfers reasoning from text to a unified latent space and couples it with a hierarchical, parallel trajectory decoder. The_ **_Cognitive Latent Reasoner_** _compresses scene understanding into compact, decisionoriented meta-action embeddings through ego-adaptive selection and only two VLM forward passes. The_ **_Hierarchical Parallel Planner_** _then generates multi-scale, causalityconsistent trajectories in a single forward pass. Together, these components preserve the generalization and interpretability of VLMs while enabling efficient, accurate and safe trajectory generation. Experiments on the nuScenes benchmark show that ColaVLA achieves state-of-the-art performance in both open-loop and closed-loop settings with favorable efficiency and robustness. The project is at https://github.com/pqh22/ColaVLA._ 

## **1. Introduction** 

Autonomous driving aims to predict safe and comfortable motion from rich multimodal observations. Early systems were organised as modular perception–prediction–planning stacks with dedicated 3D perception [25, 27, 40, 41, 44, 59, 60], forecasting [5, 15, 16, 31], and planning components [4, 10, 13, 29, 43]. Recent end-to-end approaches unify 


Figure 1. **Illustration of inference paradigms.** (a) Previous driving VLMs use text-based chain-of-thought, autoregressively emitting intermediate texts for sub-tasks; repeated decoding increases token cost and error compounding, causing high latency. (b) Our model performs latent reasoning in a VLA space with **three** forward passes, _i.e_ . scene understanding, latent rethink, and parallel action decoding, removing autoregressive text and cutting inference latency while preserving decision-level interpretability. 

the stack and learn from pixels to waypoints or controls in a single pipeline [7, 20, 21, 23, 37–39, 45, 52, 61]. In parallel, vision–language models (VLMs) [1, 2, 30, 51, 53] are increasingly integrated to inject cross-modal priors and world knowledge, either as agentic planning models that output controls or trajectories [22, 26, 36, 42, 49, 54, 56] or as reasoning assistants that guide end-to-end modules [8, 24, 46]. 

Despite rapid progress, important gaps remain between accuracy in benchmarks and reliability in deployment. Modular systems provide interpretable components and strong geometric priors, but brittle interfaces can propagate errors 

17809 

and make global optimization difficult. End-to-end systems reduce manual interfaces and achieve high open-loop accuracy [7, 20, 21, 23, 52, 61], yet they often rely on sparse trajectory supervision, intertwine perception and control in ways that obscure causal structure, and struggle to generalize to out-of-distribution scenarios. Text-based VLM planners add powerful priors but introduce some practical issues: (1) Modality mismatch. Discrete text tokens do not align with the continuous geometry and dynamics of trajectories and can lead to format violations or physically inconsistent waypoints [22, 36]. (2) Chain-of-thought reasoning latency. The computation overhead of autoregressive decoding arises from its iterative token-by-token generation, where each new token depends on previously ones, causing the sequence to grow over time and significantly increasing inference delay. 

To bridge the above gaps, we revisit the role of the VLM in the driving task and introduce a transition from explicit textual chains of thoughts to unified latent reasoning. Our key idea is to execute reasoning entirely in a unified latent space and to pair it with a planner that preserves causal structure while decoding in parallel. This retains the knowledge priors and reasoning ability of VLMs, yet avoids lengthy autoregressive reasoning and its latency. At a high level, ColaVLA consists of a **Cognitive Latent Reasoner** that distills scene evidence into compact meta-action priors, and a **Hierarchical Parallel Planner** that converts these priors to multi-scale trajectories under a causality-preserving scheme. 

First, the cognitive latent reasoner efficiently accomplishes scene understanding and the final meta-action decision through two forward passes. Specifically, during the first forward pass, the reasoner constructs a multimodal input sequence comprising a fixed driving prompt, multiview visual images, and ego status, and passes it through a VLM to obtain unified tokens that have undergone complete contextual interaction. However, the visual tokens contain substantial redundant information irrelevant to the driving decision. To extract decision-relevant information from the scene, we introduce an ego-adaptive modulation to align these tokens with the instantaneous vehicle state, after which a lightweight router scores and selects the top- _K_ safetycritical vision tokens. Subsequently, for the second forward pass, we concatenate the selected context with learnable meta queries as input, enabling each meta-action embedding to query the driving-critical context via cross-attention and ultimately yield the final driving decision. Guided by the reasoner’s decision, the hierarchical parallel planner, using the same VLMs as our reasoner, predicts multi-scale finegrained trajectories through parallel decoding. Specifically, we retrieve the corresponding meta-action embedding from an action bank based on the chosen decision. With the selected meta-action, we instantiate a full-time-domain action block using temporal embeddings, which is then resampled into _S_ nested, coarse-to-fine scales. Finally, the embeddings 

from all scales are concatenated with the pruned context to serve as the planner’s input, which are then decoded into trajectories in parallel within a single forward pass. This design yields a coherent and causally consistent planning process and produces multi-scale continuous trajectories with substantially reduced inference latency. 

Our main contributions are as follows. (1) We present ColaVLA, a unified vision–language–action framework for end-to-end autonomous driving that operates directly on continuous trajectories, avoiding modality mismatch while leveraging VLM priors. (2) We design a Cognitive Latent Reasoner that relocates reasoning from textual chain-of-thought to a unified latent space, allowing the model to observe broadly, focus selectively, rethink carefully and decide efficiently through ego-adaptive routing and meta information compression. (3) We propose a Hierarchical Parallel Planner that decodes all temporal scales and modes in a single forward pass, achieving efficient, reasonable and safe trajectory generation under tight latency constraints. (4) Comprehensive experiments on the nuScenes benchmark demonstrate that ColaVLA establishes new state-of-the-art performance in both open-loop and closed-loop evaluations, while maintaining strong interpretability and computational efficiency. 

## **2. Related Work** 

### **2.1. End-to-end Autonomous Driving** 

Classical autonomous driving stacks decompose perception, prediction, and planning into separate modules, easing engineering but causing information loss and suboptimal coordination. End-to-end (E2E) systems instead learn a single differentiable mapping from sensor inputs to trajectories or control commands. Early demonstrations proved feasibility but suffered from limited transparency and data efficiency. Recent works enhance this paradigm with richer supervision and unified architectures: UniAD [21] integrates perception and planning within a Transformer, and VAD [7, 23] employs vectorized abstractions for efficiency and uncertainty modeling. Other directions explore task dependency [52], latent generative modeling [29, 61], or simplified ego-centric controllers [28, 57]. Despite progress, most E2E methods rely on sparse supervision from a single ground truth trajectory, which limits reasoning and diversity, highlighting the need for higher-level semantic and cognitive guidance. 

### **2.2. VLMs for Autonomous Driving** 

Vision–Language Models (VLMs) bring broad world knowledge and remarkable reasoning ability to autonomous driving, inspiring two main integration paradigms. _Singlesystem_ approaches treat planning as language modeling: visual inputs and prompts are translated into textual trajectories or control commands with chain-of-thought explanations [6, 22, 35, 54, 56]. _Dual-system_ designs pair a VLM 

17810 

with an end-to-end planner, where the VLM proposes highlevel commands or low-frequency trajectories to guide a lightweight action controller [8, 24, 46]. Other efforts align vision–language features in BEV [50], extend reasoning to 3D [49], or use VLMs as teachers to supervise E2E planning models [55]. While these methods improve interpretability and generalization, they still rely on explicit text-level reasoning or suffer from a feature gap between the VLM and the downstream action planner. This motivates our unified vision–language–action framework, which performs reasoning entirely in a shared latent space, bridging perception, cognition, and control within a single coherent architecture. 

## **3. Method** 

### **3.1. Framework Overview** 

Given multimodal representation **S** _t_ comprising multi–view images, LiDAR points, radar grids, a text prompt and ego state, or a subset thereof, the trajectory planning task reduces to mapping **S** _t_ to a _K_ -step trajectory **Y**<sup>�</sup> _t_ = [( _xt_ +1 _, yt_ +1) _, . . . ,_ ( _xt_ + _K, yt_ + _K_ )]. Existing planning systems generally consist of two unified learnable components: **REASONER** ( _Rθ_ ), usually implemented as ResNet [18], PointNet [41], Q-Former [11], or VLM Transformer that extracts and fuses multimodal features or optionally refines them with chain-of-thought, and **PLANNER** ( _Pϕ_ ), usually instantiated as an deterministic MLP planner, stochastic diffusion sampler, or standard Transformer [47] decoder that injects action queries and regresses continuous way-points. Their interaction is succinctly captured by 


where **Z** _t ∈_ R<sup>_L×D_</sup> is a latent token sequence and **A** represents a learnable action bank. This abstraction subsumes three dominant paradigms in the field: (1) classical modular pipelines with separate perception, decision, and planning stages; (2) end-to-end planners without explicit reasoning; and (3) VLM-based models that formulate planning as autoregressive text generation with chain-of-thought reasoning. 

To unify the generalization ability of VLMs with the efficiency of action-based planners, we reformulate trajectory planning under a unified VLA framework as shown in Fig. 2. Rather than relying on textual chain-of-thought reasoning, we introduce **Cognitive Latent Reasoning** in Sec. 3.2 that operates fully in the unified latent space, requiring only two forward passes to yield an interpretable, decision-oriented meta representation. This compact meta-action prior captures high-level intent and contextual awareness without the substantial latency of autoregressive decoding. Built upon this, ColaVLA employs a **Hierarchical Parallel Planner** (detailed in Sec. 3.3) that performs structured trajectory refinement under a causality-preserving hybrid attention mask. This design enables multi-scale trajectory generation and 

parallel multi-mode decoding in a single forward pass, bridging knowledge-driven reasoning and continuous control for a unified, interpretable, and low-latency planning pipeline. 

### **3.2. Cognitive Latent Reasoning** 

Recent vision–language models show strong generalization in autonomous driving by performing a driver-like reasoning process: perceiving the scene, identifying critical entities, rethinking carefully and deciding final strategies. However, most existing approaches realize this reasoning at the text level, leading to high latency and exposure bias from autoregressive decoding. Inspired by advances in latent-space reasoning for large language models [17], we shift this cognitive process to a unified latent space. Our reasoner performs that within only two forward passes, preserving the semantic richness of language-based reasoning while avoiding tokengeneration overhead. This interpretable design forms an efficient foundation for hierarchical parallel planning. **Driving Scene Comprehension.** The cognitive process of a human driver begins with a holistic survey of the environment. To emulate this step, we form an input sequence by mixing a fixed driving prompt encoded as text embeddings **T** _∈_ R<sup>_Lt×D_</sup> , multi-view vision embeddings **V** _∈_ R<sup>_Lv×D_</sup> produced by the perception front-end, and an ego token **E** _∈_ R<sup>1</sup><sup>_×D_</sup> that represents the vehicle state. The shared VLM transformer _D_ VLM processes this sequence, and we keep only the visual slice of the hidden states: 


The updated text and ego embeddings are discarded so that the prompt remains immutable and no redundant information is introduced. And **Q** V thus provides a temporally causal, globally coherent representation of spatial semantics, lane topology, and dynamic agents, establishing a stable foundation for the subsequent identification of critical entities. **Critical Entity Recognition.** Selecting only safety-critical cues is essential for both efficiency and reliability. We introduce an ego-adaptive router _Hϕ_ that first applies FiLM conditioning to align visual tokens with the current ego state: 


where the scale _γ_ R _e_ ( **E** ) and shift _β_ R _e_ ( **E** ) are generated from the ego token through two independent linear projections. This conditioning highlights scene elements consistent with the ego vehicle’s velocity, heading, and curvature, emphasizing dynamic agents and lane boundaries within the collision cone while suppressing irrelevant background details. 

Next, the router evaluates the ego-modulated tokens and then selects the most informative subset: 


17811 


Figure 2. Overview of the **ColaVLA** framework. Multi-view image sequences are first processed by an image backbone and a Q-Former to perceive 3D objects and vectorized maps, producing visual tokens for subsequent reasoning and planning. On the left, the **Cognitive Latent Reasoning** module performs implicit reasoning through four stages, _i.e_ . _Understand_ , _Recognize_ , _Rethink_ , and _Decide_ , to derive a driving strategy. On the right, the derived strategy selects corresponding meta-action queries from action bank, which are then transformed to multi-scale targets. These targets, together with the pruned context are fed into a **Hierarchical Parallel Planner** for one-pass, parallel trajectory decoding. The resulting multi-scale trajectories enable efficient, causal, and interpretable end-to-end planning. 

During training, the selection is made differentiable using a Gumbel–Softmax relaxation to form a _K_ -hot mask, while at inference time the top- _K_ tokens are retained directly. The resulting compact set **Q**<sup>_∗_</sup> _∈_ R<sup>_K×D_</sup> effectively captures the most safety-relevant visual cues, _e.g_ . lanes, nearby vehicles, pedestrians, and traffic lights, serving as an efficient information bottleneck for the subsequent latent reasoning stage. **Latent Rethinking.** After pruning irrelevant cues, a human driver would reassess the condensed evidence and form a provisional plan. We emulate this process by concatenating four components: the fixed driving prompt **T** , the _K_ salient vision tokens **Q**<sup>_∗_</sup> _∈_ R<sup>_K×D_</sup> , the ego token **E** _∈_ R<sup>1</sup><sup>_×D_</sup> , and a bank of _C_ learnable meta-queries **M** = [ **m** 1 _, . . . ,_ **m** _C_ ] _∈_ R<sup>_C×D_</sup> . This sequence is passed through a second forward pass of the shared VLM transformer: 


Sharing VLM ensures temporal and semantic consistency, while the smaller token budget ( _C ≪ Lv_ ) keeps computation efficient. Each **m** _c_ is initialized to represent a corresponding meta-action, such as straight cruising, unprotected left turn, or hard braking, derived from clustering training trajectories. The updated embeddings **Q** M represents different driving strategies, which are ready for final decision-making. **Strategic Decision Synthesis.** The meta-query embeddings **Q** M are adapted to the ego state through FiLM modulation and cross-attend to the driving-critical visual tokens **Q**<sup>_∗_</sup> , 

followed by a self-attention layer over the meta tokens. A shared two-layer MLP then maps each refined meta token to a maneuver logit, trained with a focal loss that emphasizes hard and safety-critical cases. By constraining the reasoning space to _C_ meta-action tokens, the process achieves entropy reduction and produces multiple probable driving strategies, which form structured priors for subsequent prediction. 

### **3.3. Hierarchical Parallel Planning** 

We introduce a Hierarchical Parallel Planner that generates trajectories through multi-stage intent-to-motion decoding. It integrates temporal abstraction, a causality-preserving attention scheme, and confidence-guided multi-mode decoding, with three key properties: (i) intent-to-motion refinement, where final destination is progressively resolved into detailed motion plans; (ii) stage-wise independence, enabling parallel decoding across temporal scales for efficient inference; and (iii) confidence-aware diversity, maintaining multiple plausible modes to enhance robustness. **Stage-Aware Trajectory Querying.** Given a prediction horizon of _T_ steps, _T_ = _{_ 0 _, . . . , T −_ 1 _}_ , we divide it into _S_ nested stages _I_ 1 _⊂· · · ⊂IS_ = _T_ , where earlier stages represent coarse temporal resolutions and later stages progressively refine the trajectory. For each scale _s_ , the meta-action query **A** _∈_ R<sup>_D_</sup> selected by the cognitive reasoner is expanded with temporal embeddings to form trajectory targets **F** _∈_ R<sup>_T ×D_</sup> , which are resampled into multi-scale subsets **F** _s ∈_ R<sup>_|Is|×D_</sup> 

17812 


Figure 3. **Causality-Preserving Hybrid Mask.** Our mask is designed for the multi-scale targets within our planner. It enables information flow from the pruned context to all temporal scales, while maintaining temporal causality between adjacent scales. 

following the predefined order. The pruned context and all scale-wise targets are then concatenated in temporal order to form the complete multi-scale input stream: 


where **Q**<sup>_∗_</sup> represents the pruned context encoding the historical and environmental information. This hierarchical composition ensures that coarse trajectories precede finer refinements, establishing the foundation for the subsequent causality-preserving masking mechanism to perform structured multi-mode planning within a single forward pass. **Causality-Preserving Hybrid Attention.** We design a hybrid attention mask _M_ to regulate information flow between the pruned context and multi-scale trajectory tokens as shown in Fig. 3. It satisfies three principles: (i) bidirectional interaction within each category, enabling context tokens and same-scale trajectory tokens to maintain local consistency; (ii) global context aggregation, allowing every trajectory token to attend to all context tokens; and (iii) causal preservation, where tokens at scale _s_ can only access those from the preceding coarser scale _s−_ 1, preventing information leakage from future finer scales. 

Formally, the mask is defined as 


where _Lc_ is the length of pruned context and _s_ indexes the current scale. **X** denotes the concatenated sequence. The 

mask thus allows each token at scale _s_ to attend to both the pruned context and the immediately preceding scale _Is−_ 1, while preventing access to future scales _Is_ +1 _, . . . , IS_ . This design effectively combines global context aggregation with strictly causal refinement, ensuring that trajectory decoding proceeds in a physically consistent coarse-to-fine manner. **Confidence-Guided Parallel Decoding.** In the final decoding stage, the planner simultaneously processes multiple candidate driving strategies, each producing a set of latent trajectory targets. Two lightweight MLP heads are applied independently to estimate the confidence score and to regress the corresponding multi-scale trajectory for each hypothesis. During training, a one-hot supervision signal is assigned based on the distance between each predicted trajectory and the ground-truth, where only the closest hypothesis receives direct regression supervision. This confidence-guided mechanism enables the model to prioritize the most reliable trajectory while preserving diversity across hypotheses. The parallel decoding further processes all candidates within a single forward pass, ensuring high efficiency and enhanced generalization by effectively preventing mode collapse. 

## **4. Experiments** 

### **4.1. Experiment Settings** 

**Datasets and evaluation metrics.** We conduct experiments on the challenging nuScenes [3] dataset, which contains 1,000 driving scenes of approximately 20 seconds each, providing six camera images, LiDAR data, semantic maps, and 3D bounding box annotations for keyframes. To enhance the planning-related supervision of our VLM, we additionally use the OmniDrive-nuScenes [49] extension, which augments nuScenes with QA-style annotations spanning perception, prediction, and planning. These annotations enable both offline reasoning supervision and online spatial reasoning. 

We evaluate our model in both **open-loop** and **closedloop** settings. Open-loop evaluation follows prior works [21, 23] and measures trajectory accuracy and safety using two standard metrics: the L2 displacement error (distance between predicted and ground-truth trajectories) and the collision rate. For closed-loop evaluation, we employ the NeuroNCAP simulator [32], a photorealistic framework built upon nuScenes that reconstructs diverse, safety-critical urban interactions for realistic policy assessment. Performance is measured by the NeuroNCAP Score, a five-star metric that rewards safe, low-impact behavior, and the collision rate, jointly reflecting both safety and operational efficiency. Together, these benchmarks provide a comprehensive evaluation of the model’s accuracy, robustness, and generalization in both static and dynamic driving scenarios. 

**Implementation details.** Our implementation is based on the LLaVA v1.5 [30] framework, which uses LLaMA-7B as the language model. Following prior work, we initialize 

17813 

|||||**L2 (**|_m_**)**_↓_||**C**|**ol. Ra**|**te (%)**|_↓_|
|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|**Reference**|**Ego**||<br>|<br>|||<br>|<br>|<br>|
||||1_s_|2_s_|3_s_|Avg.|1_s_|2_s_|3_s_|Avg.|
||_T_<br>|_ext-Ba_<br>|_sed Driv_<br>|_ing Mo_<br>|_dels_<br>||||||
|DriveVLM [46]|CoRL 2024|✓|0.18|0.34|0.68|0.40|–|–|–|–|
|DriveVLM-Dual [46]|CoRL 2024|✓|0.15|0.29|0.48|0.31|–|–|–|–|
|OmniDrive [49]|CVPR 2025|✓|0.14|0.29|0.55|0.33|**0.00**|**0.13**|0.78|0.30|
|EMMA [22]|TMLR|✓|0.14|0.29|0.54|0.32|–|–|–|–|
|EMMA+ [22]|TMLR|✓|**0.13**|0.27|0.48|0.29|–|–|–|–|
|ImpromptuVLA [9]|NeurIPS 2025|✓|**0.13**|0.27|0.53|0.30|–|–|–|–|
|SOLVE-VLM [8]|CVPR 2025|✓|**0.13**|**0.25**|**0.47**|**0.28**|**0.00**|0.16|0.43|**0.20**|
||_Ac_|_tion-B_|_ased Dr_|_iving M_|_odels_||||||
|UniAD [21]|CVPR 2023|–|0.59|1.01|1.48|1.03|0.16|0.51|1.64|0.77|
|VAD-Base [23]|ICCV 2023|–|0.69|1.22|1.83|1.25|0.06|0.68|2.52|1.09|
|BEV-Planner [28]|CVPR 2024|–|0.30|0.52|0.83|0.55|0.10|0.37|1.30|0.59|
|UniAD [21]|CVPR 2023|✓|0.20|0.42|0.75|0.46|0.02|0.25|0.84|0.37|
|VAD-Base [23]|ICCV 2023|✓|0.17|0.34|0.60|0.37|0.04|0.27|0.67|0.33|
|AD-MLP [57]|arXiv 2023|✓|0.15|0.32|0.59|0.35|**0.00**|0.27|0.85|0.37|
|BEV-Planner++ [28]|CVPR 2024|✓|0.16|0.32|0.57|0.35|**0.00**|0.29|0.73|0.34|
|SOLVE-E2E [8]|CVPR 2025|✓|0.14|0.28|0.50|0.31|0.04|**0.17**|0.68|0.30|
|ColaVLA|–|✓|**0.14**|**0.27**|**0.50**|**0.30**|0.04|**0.17**|**0.47**|**0.23**|


Table 1. Open-loop planning results on the nuScenes benchmark. Methods are grouped into text-based driving models (top) and action-based driving models (bottom). Within action-based approaches, ColaVLA achieves the best overall results, _i.e_ . lowest average L2 and the best collision rates, demonstrating accuracy and safety while retaining high inference efficiency. 

|**Method**|**Reference**||**Neuro**|**NCAP Scor**|**e**_↑_||**Collisio**|**n rate (%)**|_↓_|
|---|---|---|---|---|---|---|---|---|---|
|||**Avg.**|**Stat.**|**Frontal**|**Side**|**Avg.**|**Stat.**|**Frontal**|**Side**|
|UniAD [21]|CVPR 2023|0.73|0.84|0.10|1.26|88.6|87.8|98.4|79.6|
|VAD [23]|ICCV 2023|0.66|0.47|0.04|1.45|92.5|96.2|99.6|81.6|
|SparseDrive [45]|ICRA 2025|0.92|–|–|–|93.9|–|–|–|
|BridgeAD-S [58]|CVPR 2025|1.52|–|–|–|76.2|–|–|–|
|BridgeAD-B [58]<br>|CVPR 2025|1.60|–|–|–|72.6|–|–|–|
|ImpromptuVLA<sup>_†_ </sup>[9]<br>|NeurIPS 2025|2.06|2.55|1.86|1.78|65.1|54.8|72.8|67.6|
|BridgeAD-S<sup>_‡_ </sup>[58]<br>|CVPR 2025|2.98|–|–|–|46.1|–|–|–|
|BridgeAD-B<sup>_‡_ </sup>[58]|CVPR 2025|3.06|–|–|–|44.3|–|–|–|
|ColaVLA|–|**3.48**|**3.54**|**3.16**|**3.75**|**36.8**|**32.3**|**51.6**|**26.4**|


Table 2. Closed-loop simulation results on NeuroNCAP [32]. _†_ indicates that it utilizes additional training data and is a text-based driving VLM model. _‡_ refers to trajectory post-processing. Our proposed method achieves a substantial improvement in the closed-loop evaluation, demonstrating strong adaptability to safety-critical scenarios and highlighting the model’s efficiency and generalization capability. In this evaluation, we adopt only the **top-1 driving strategy** to better simulate realistic decision-making in closed-loop settings, ensuring fair comparison and faithfully reflecting the model’s safety and robustness in real-world driving situations. Best scores are in **bold** . 

the image encoder with EVA-02-L [14] and adopt the SQFormer [8] architecture for better visual reasoning. The detection decoder and lane decoder follow StreamPETR [48], with 900 object queries and 300 lane queries, respectively. 

We use a multi-stage training strategy. In the first stage, our VLM is pretrained on QA pairs from OmniDrivenuScenes, where LoRA layers [19] are applied to prompt and adapt the VLM efficiently for perception–planning align- 

ment. In the second stage, we integrate our action-based planner and perform joint fine-tuning. Within the VLM, we only update the LoRA parameters to retain pretrained knowledge while improving decision capability. Training is conducted with the AdamW optimizer [33] with Cosine Annealing [34], using a weight decay of 1 _×_ 10<sup>_−_4</sup> and an initial learning rate of 1 _×_ 10<sup>_−_4</sup> . Additional details and hyperparameters are provided in the supplementary material. 

17814 

|Method|Action-based|Latency (ms) _↓_|Reasonin|Rethink||L2 (|cm)_↓_||
|---|---|---|---|---|---|---|---|---|
|OmniDrive [49]|✗|3727|g||1s|2s|3s|Avg|
|SOLVE-VLM [8]|✗|3719|✗|✗|14.1|28.5|54.2|32.2|
|Ours|✓|**727**|✓|✗|14.5|28.5|50.7|31.3|
||||✓|✓|**14.0**|**27.1**|**50.2**|**30.4**|


Table 3. Inference latency comparison on a single NVIDIA H20 GPU without flash-attention [12]. We report end-to-end inference latency (ms per frame) under identical batch settings. 

### **4.2. Comparison with State-of-the-art Methods** 

**Open-loop planning results.** Tab. 1 reports results on the nuScenes open-loop benchmark. Among action-based approaches, ColaVLA attains the best overall accuracy and safety, achieving the lowest average L2 error (0 _._ 30m) and the lowest average collision rate (0 _._ 23%). Compared with the strongest prior action-based baseline, SOLVE-E2E (Avg. L2 0 _._ 31m; Avg. Col. 0 _._ 30%), our method reduces L2 by 3% and collision rate by 23%, indicating more precise and safer trajectory predictions. Notably, ColaVLA is also competitive with the latest text-based VLM planners while avoiding autoregressive text decoding. By relocating reasoning to a latent space and introducing cognitive latent reasoning with hierarchical parallel decoding, our framework reduces the number of VLM forward passes by over **5** _×_ fewer than typical text-based pipelines, highlighting its superior efficiency while operating directly in the latent action space. 

**Closed-loop planning results.** On the NeuroNCAP closedloop benchmark Tab. 2), ColaVLA establishes a new state of the art with a NeuroNCAP score of 3 _._ 16, surpassing the strongest prior method, ImpromptuVLA, by an absolute margin of +1 _._ 10 (53% relative). In terms of safety, our model lowers the average collision rate from 65 _._ 1% to 42 _._ 5%, with particularly large gains on static collisions (54 _._ 8% _→_ 15 _._ 0%; about 73% reduction) and the best performance on side collisions. The overall lower collision profile and the substantially higher NeuroNCAP score highlight strong closed-loop robustness. Importantly, ImpromptuVLA is a text-based VLM trained with additional curated data, whereas ColaVLA reaches higher scores without textual chain-of-thought inference and additional safety-critical data. These results validate the effectiveness of our cognitive latent reasoning and hierarchical parallel planner: relocating reasoning to a vision-aligned latent space and decoding trajectories in a single parallel pass translates into better decision quality and improved safety under closed-loop evaluation. 

**Inference latency comparison.** As shown in Tab. 3, our ColaVLA achieves the lowest latency among all compared methods while maintaining strong planning accuracy and safety performance. Compared with SOLVE-VLM [8] and OmniDrive [49], which depend on autoregressive chain-ofthought reasoning at the text level, our latent reasoning and single-pass hierarchical decoding deliver over **5** _×_ faster inference, enabling efficient and interpretable planning. 

Table 4. Ablation on Latent Reasoning. We evaluate the effect of the reasoning process for latent driving strategy inference and the reflective rethinking of critical cues within the cognitive reasoner. 

|Planner|N<br>Static|euroNCAP<br>Frontal|Score_↑_<br>Side|<br>Avg|
|---|---|---|---|---|
|MLP-based|1.18|0.65|1.31|1.05|
|Diffusion-based|1.05|0.58|**1.43**|1.02|
|Ours|**2.58**|**1.10**|0.82|**1.50**|


Table 5. Ablation on the action-based planner under closed-loop evaluation on NeuroNCAP benchmark. We use deterministic MLP and stochastic diffusion heads to compare against our planner. 

### **4.3. Qualitative Results** 

Fig. 4 shows qualitative results from our Hierarchical Parallel Planner. In both straight and turning scenarios, coarse trajectories (red) capture global intent, while finer scales (yellow, purple) progressively refine spatial details and curvature, converging closely to the ground truth (green). These results demonstrate that our hierarchical decoding produces smooth, and accurate plans within a single forward pass. 

### **4.4. Ablation Studies** 

In this section, we systematically ablate the proposed components and key hyperparameters to assess their individual and combined contributions. We report results on nuScenes [3] using two complementary metrics: the open-loop L2 average error and the closed-loop NeuroNCAP Score. 

**Ablation on Latent Reasoning.** As shown in Tab. 4, we conduct ablation experiments on our reasoning module to verify its effectiveness. Introducing latent reasoning significantly enhances the model’s reasoning ability, enabling accurate prediction and reducing the average L2 error. Furthermore, adding the Rethink stage allows our model to re-evaluate the compressed key information from the current driving scene, refining visual understanding and facilitating better decisionmaking in subsequent stages. This progressive reasoning process improves the model’s generalization and robustness, especially in complex or dynamic traffic scenarios. 

**Ablation on action-based planner.** As action-based planners can often achieve similar open-loop metrics, we focus here on their closed-loop performance to better assess realworld driving behavior. To isolate the planner’s contribution, the reasoning module is disabled in this comparison. As shown in Tab. 5, our Hierarchical Parallel Planner significantly outperforms both MLP- and diffusion-based planners under the NeuroNCAP benchmark. In particular, our 

17815 


Figure 4. **Qualitative visualization of multi-scale trajectory predictions.** Red, yellow, and purple curves denote endpoint-only to full-trajectory predictions, while the green curve is the ground-truth. Right: BEV visualization with ego vehicle, agents, and trajectories. 

|||L2 (|cm)_↓_||
|---|---|---|---|---|
|Retained token number_K_|1s|2s|3s|Avg|
|128|14.4|28.3|50.8|31.2|
|192|14.2|28.1|50.5|30.9|
|256|**14.0**|**27.1**|**50.2**|**30.4**|
|320|14.6|28.8|51.8|31.7|


Table 6. Ablation on the number of retained critical tokens _K_ . 

|Strategy Type|1s|L2 (<br>2s|cm)_↓_<br>3s|Avg|
|---|---|---|---|---|
|Single scale|**13.8**|28.4|53.4|31.9|
|Multi-scale (Sequential)|14.5|28.7|52.2|31.8|
|Multi-scale (Reverse)|14.7|28.5|51.1|31.4|
|Multi-scale (Interpolate)|14.0|**27.1**|**50.2**|**30.4**|


Table 7. Ablation on the strategy of hierarchical regression. All variants share the same parallel decoding framework but differ in their specific selection strategy of trajectory subsets across scales. 

method yields substantial improvements in static and frontal scenarios, highlighting its ability to generate smoother, more stable, and safer trajectories. By decoding trajectories from coarse to fine while preserving causal dependencies across temporal scales, our planner effectively refines intermediate predictions and adapts robustly to complex or dynamic traffic conditions, demonstrating superior safety and generalization. **Ablation on the number of retained critical tokens** _K_ **.** We further analyze the influence of the number of retained visual tokens _K_ in the ego-adaptive router. The original object and lane queries contain 900 and 300 tokens, respectively. As shown in Tab. 6, retaining too few tokens limits the representational capacity, causing significant loss of visual information and degraded performance. Conversely, retaining too many tokens introduces redundancy, increasing computational overhead during both training and inference. Finally we choose _K_ =256 as our default configuration, which achieves the best trade-off, providing sufficient semantic 

coverage while maintaining computational efficiency. **Ablation on the strategy of hierarchical regression.** We investigate different strategies for hierarchical trajectory regression, all under the same parallel decoding framework but with varied ordering schemes. The Single scale baseline directly regresses the final trajectory without temporal abstraction, serving as a non-causal reference. The Sequential strategy extends trajectories forward from the start, while the Reverse strategy begins from the final point and propagates backward. Our proposed Interpolate strategy instead first predicts key endpoints and then fills in intermediate points across scales, aligned with the causal structure of driving motion. As shown in Tab. 7, all multi-scale designs outperform the single-scale baseline, demonstrating the benefits of temporal abstraction. Among them, the Interpolate strategy yields the best performance, validating its effectiveness in structured and causally consistent trajectory reasoning. 

## **5. Conclusion** 

We introduced ColaVLA, a unified vision–language–action framework for end-to-end autonomous driving. By relocating reasoning from text to a unified latent space and coupling it with a hierarchical parallel planner, ColaVLA bridges the gap between VLM cognition and continuous action generation. Its cognitive latent reasoner efficiently compresses scene understanding into compact meta-action representations through ego-adaptive token selection, while the causality-preserving planner decodes multi-scale trajectories in a single forward pass. This design achieves efficient, interpretable, and safe planning with minimal latency. Experiments on nuScenes demonstrate that ColaVLA sets new state-of-the-art performance in both open-loop and closedloop evaluations while maintaining strong efficiency and robustness. These results suggest that transferring reasoning from text to latent space provides a scalable path toward efficient, knowledge-driven autonomous driving systems. 

17816 

## **Acknowledgement** 

This study was supported in part by National Key R&D Program of China Project 2022ZD0161100, in part by Smart Traffic Fund PSRI/76/2311/PR, in part by the Centre for Perceptual and Interactive Intelligence, a CUHK-led InnoCentre under the InnoHK initiative of the Innovation and Technology Commission of the Hong Kong Special Administrative Region Government, in part by NSFC-RGC Project N ~~C~~ UHK498/24. 

## **References** 

- [1] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 1 

- [2] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. In _NeurIPS_ , 2020. 1 

- [3] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _CVPR_ , 2020. 5, 7 

- [4] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. _arXiv preprint arXiv:2106.11810_ , 2021. 1 

- [5] Yuning Chai, Benjamin Sapp, Mayank Bansal, and Dragomir Anguelov. Multipath: Multiple probabilistic anchor trajectory hypotheses for behavior prediction. _arXiv preprint arXiv:1910.05449_ , 2019. 1 

- [6] Long Chen, Oleg Sinavski, Jan Hunermann, Alice Karnsund,¨ Andrew James Willmott, Danny Birch, Daniel Maund, and Jamie Shotton. Driving with llms: Fusing object-level vector modality for explainable autonomous driving. In _IEEE International Conference on Robotics and Automation._ , pages 14093–14100. IEEE, 2024. 2 

- [7] Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. _arXiv preprint arXiv:2402.13243_ , 2024. 1, 2 

- [8] Xuesong Chen, Linjiang Huang, Tao Ma, Rongyao Fang, Shaoshuai Shi, and Hongsheng Li. Solve: Synergy of language-vision and end-to-end networks for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 12068–12077, 2025. 1, 3, 6, 7 

- [9] Haohan Chi, Huan-ang Gao, Ziming Liu, Jianing Liu, Chenyu Liu, Jinwei Li, Kaisen Yang, Yangcheng Yu, Zeda Wang, Wenyi Li, et al. Impromptu vla: Open weights and open data for driving vision-language-action models. _arXiv preprint arXiv:2505.23757_ , 2025. 6 

- [10] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. Transfuser: Imitation 

with transformer-based sensor fusion for autonomous driving. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 45(11):12878–12895, 2022. 1 

- [11] Francesco Dalmonte, Emirhan Bayar, Emre Akbas, and Mariana-Iuliana Georgescu. Q-former autoencoder: A modern framework for medical anomaly detection, 2025. 3 

- [12] Tri Dao, Dan Fu, Stefano Ermon, Atri Rudra, and Christopher Re.´ Flashattention: Fast and memory-efficient exact attention with io-awareness. _Advances in neural information processing systems_ , 35:16344–16359, 2022. 7 

- [13] Scott Ettinger, Shuyang Cheng, Benjamin Caine, Chenxi Liu, Hang Zhao, Sabeek Pradhan, Yuning Chai, Ben Sapp, Charles R Qi, Yin Zhou, et al. Large scale interactive motion forecasting for autonomous driving: The waymo open motion dataset. In _ICCV_ , pages 9710–9719, 2021. 1 

- [14] Yuxin Fang, Quan Sun, Xinggang Wang, Tiejun Huang, Xinlong Wang, and Yue Cao. Eva-02: A visual representation for neon genesis. _Image and Vision Computing_ , 149:105171, 2024. 6 

- [15] Junru Gu, Chen Sun, and Hang Zhao. Densetnt: End-to-end trajectory prediction from dense goal sets. In _ICCV_ , pages 15303–15312, 2021. 1 

- [16] Junru Gu, Chenxu Hu, Tianyuan Zhang, Xuanyao Chen, Yilun Wang, Yue Wang, and Hang Zhao. Vip3d: End-to-end visual trajectory prediction via 3d agent queries. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 5496–5506, 2023. 1 

- [17] Shibo Hao, Sainbayar Sukhbaatar, DiJia Su, Xian Li, Zhiting Hu, Jason Weston, and Yuandong Tian. Training large language models to reason in a continuous latent space. _arXiv preprint arXiv:2412.06769_ , 2024. 3 

- [18] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In _CVPR_ , 2016. 3 

- [19] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. _arXiv preprint arXiv:2106.09685_ , 2021. 6 

- [20] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In _ECCV_ , 2022. 1, 2 

- [21] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In _CVPR_ , pages 17853–17862, 2023. 1, 2, 5, 6 

- [22] Jyh-Jing Hwang, Runsheng Xu, Hubert Lin, Wei-Chih Hung, Jingwei Ji, Kristy Choi, Di Huang, Tong He, Paul Covington, Benjamin Sapp, et al. Emma: End-to-end multimodal model for autonomous driving. _arXiv preprint arXiv:2410.23262_ , 2024. 1, 2, 6 

- [23] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In _ICCV_ , pages 8340–8350, 2023. 1, 2, 5, 6 

- [24] Bo Jiang, Shaoyu Chen, Bencheng Liao, Xingyu Zhang, Wei Yin, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang 

17817 

Wang. Senna: Bridging large vision-language models and endto-end autonomous driving. _arXiv preprint arXiv:2410.22313_ , 2024. 1, 3 

- [25] Alex H Lang, Sourabh Vora, Holger Caesar, Lubing Zhou, Jiong Yang, and Oscar Beijbom. Pointpillars: Fast encoders for object detection from point clouds. In _CVPR_ , pages 12697– 12705, 2019. 1 

- [26] Peizheng Li, Zhenghao Zhang, David Holtz, Hang Yu, Yutong Yang, Yuzhi Lai, Rui Song, Andreas Geiger, and Andreas Zell. Spacedrive: Infusing spatial awareness into vlm-based autonomous driving, 2025. 1 

- [27] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Yu Qiao, and Jifeng Dai. Bevformer: Learning bird’s-eye-view representation from multi-camera images via spatiotemporal transformers. In _ECCV_ , pages 1–18. Springer, 2022. 1 

- [28] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and Jose M Alvarez. Is ego status all you need for openloop end-to-end autonomous driving? In _CVPR_ , pages 14864– 14873, 2024. 2, 6 

- [29] Bencheng Liao, Shaoyu Chen, Haoran Yin, Bo Jiang, Cheng Wang, Sixu Yan, Xinbang Zhang, Xiangyu Li, Ying Zhang, Qian Zhang, et al. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. _arXiv preprint arXiv:2411.15139_ , 2024. 1, 2 

- [30] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _NeurIPS_ , 36, 2024. 1, 5 

- [31] Yicheng Liu, Jinghuai Zhang, Liangji Fang, Qinhong Jiang, and Bolei Zhou. Multimodal motion prediction with stacked transformers. In _CVPR_ , pages 7577–7586, 2021. 1 

- [32] William Ljungbergh, Adam Tonderski, Joakim Johnander, Holger Caesar, Kalle Astr<sup>˚</sup> om, Michael Felsberg, and Christof-¨ fer Petersson. Neuroncap: Photorealistic closed-loop safety testing for autonomous driving. In _European Conference on Computer Vision_ , pages 161–177. Springer, 2024. 5, 6 

- [33] I Loshchilov. Decoupled weight decay regularization. In _ICLR_ , 2019. 6 

- [34] Ilya Loshchilov and Frank Hutter. Sgdr: Stochastic gradient descent with warm restarts. In _ICLR_ , 2017. 6 

- [35] Jiageng Mao, Yuxi Qian, Junjie Ye, Hang Zhao, and Yue Wang. Gpt-driver: Learning to drive with gpt. _arXiv preprint arXiv:2310.01415_ , 2023. 2 

- [36] Jiageng Mao, Junjie Ye, Yuxi Qian, Marco Pavone, and Yue Wang. A language agent for autonomous driving. _arXiv preprint arXiv:2311.10813_ , 2023. 1, 2 

- [37] Muleilan Pei, Shaoshuai Shi, Xuesong Chen, Xu Liu, and Shaojie Shen. Foresight in motion: Reinforcing trajectory prediction with reward heuristics. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 28303–28312, 2025. 1 

- [38] Muleilan Pei, Shaoshuai Shi, and Shaojie Shen. Advancing multi-agent traffic simulation via r1-style reinforcement finetuning. _arXiv preprint arXiv:2509.23993_ , 2025. 

- [39] Muleilan Pei, Shaoshuai Shi, Lu Zhang, Peiliang Li, and Shaojie Shen. Goirl: Graph-oriented inverse reinforcement learning for multimodal trajectory prediction. _arXiv preprint arXiv:2506.21121_ , 2025. 1 

- [40] Qihang Peng, Henry Zheng, and Gao Huang. Proxytransformation: Preshaping point cloud manifold with proxy attention for 3d visual grounding. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 24582– 24592, 2025. 1 

- [41] Charles R Qi, Hao Su, Kaichun Mo, and Leonidas J Guibas. Pointnet: Deep learning on point sets for 3d classification and segmentation. In _CVPR_ , pages 652–660, 2017. 1, 3 

- [42] Chonghao Sima, Katrin Renz, Kashyap Chitta, Li Chen, Hanxue Zhang, Chengen Xie, Jens Beißwenger, Ping Luo, Andreas Geiger, and Hongyang Li. Drivelm: Driving with graph visual question answering. _arXiv preprint arXiv:2312.14150_ , 2023. 1 

- [43] Haoran Song, Wenchao Ding, Yuxuan Chen, Shaojie Shen, Michael Yu Wang, and Qifeng Chen. Pip: Planning-informed trajectory prediction for autonomous driving. In _ECCV_ , pages 598–614. Springer, 2020. 1 

- [44] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. Scalability in perception for autonomous driving: Waymo open dataset. In _CVPR_ , pages 2446–2454, 2020. 1 

- [45] Wenchao Sun, Xuewu Lin, Yining Shi, Chuang Zhang, Haoran Wu, and Sifa Zheng. Sparsedrive: End-to-end autonomous driving via sparse scene representation. _arXiv preprint arXiv:2405.19620_ , 2024. 1, 6 

- [46] Xiaoyu Tian, Junru Gu, Bailin Li, Yicheng Liu, Chenxu Hu, Yang Wang, Kun Zhan, Peng Jia, Xianpeng Lang, and Hang Zhao. Drivevlm: The convergence of autonomous driving and large vision-language models. _arXiv preprint arXiv:2402.12289_ , 2024. 1, 3, 6 

- [47] A Vaswani. Attention is all you need. In _NeurIPS_ , 2017. 3 

- [48] Shihao Wang, Yingfei Liu, Tiancai Wang, Ying Li, and Xiangyu Zhang. Exploring object-centric temporal modeling for efficient multi-view 3d object detection. In _ICCV_ , pages 3621–3631, 2023. 6 

- [49] Shihao Wang, Zhiding Yu, Xiaohui Jiang, Shiyi Lan, Min Shi, Nadine Chang, Jan Kautz, Ying Li, and Jose M Alvarez. Omnidrive: A holistic llm-agent framework for autonomous driving with 3d perception, reasoning and planning. _arXiv preprint arXiv:2405.01533_ , 2024. 1, 3, 5, 6, 7 

- [50] Tsun-Hsuan Wang, Alaa Maalouf, Wei Xiao, Yutong Ban, Alexander Amini, Guy Rosman, Sertac Karaman, and Daniela Rus. Drive anywhere: Generalizable end-to-end autonomous driving with multi-modal foundation models. In _IEEE International Conference on Robotics and Automation._ , pages 6687–6694. IEEE, 2024. 3 

- [51] Weihan Wang, Qingsong Lv, Wenmeng Yu, Wenyi Hong, Ji Qi, Yan Wang, Junhui Ji, Zhuoyi Yang, Lei Zhao, Xixuan Song, et al. Cogvlm: Visual expert for pretrained language models. _arXiv preprint arXiv:2311.03079_ , 2023. 1 

- [52] Xinshuo Weng, Boris Ivanovic, Yan Wang, Yue Wang, and Marco Pavone. Para-drive: Parallelized architecture for realtime autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15449–15458, 2024. 1, 2 

- [53] Zhiyu Wu, Xiaokang Chen, Zizheng Pan, Xingchao Liu, Wen Liu, Damai Dai, Huazuo Gao, Yiyang Ma, Chengyue Wu, 

17818 

Bingxuan Wang, Zhenda Xie, Yu Wu, Kai Hu, Jiawei Wang, Yaofeng Sun, Yukun Li, Yishi Piao, Kang Guan, Aixin Liu, Xin Xie, Yuxiang You, Kai Dong, Xingkai Yu, Haowei Zhang, Liang Zhao, Yisong Wang, and Chong Ruan. Deepseekvl2: Mixture-of-experts vision-language models for advanced multimodal understanding. https://arxiv.org/abs/ 2412.10302, 2024. Accessed: 2025-05-16. 1 

- [54] Shuo Xing, Chengyuan Qian, Yuping Wang, Hongyuan Hua, Kexin Tian, Yang Zhou, and Zhengzhong Tu. Openemma: Open-source multimodal model for end-to-end autonomous driving. _arXiv preprint arXiv:2412.15208_ , 2024. 1, 2 

- [55] Yi Xu, Yuxin Hu, Zaiwei Zhang, Gregory P Meyer, Siva Karthik Mustikovela, Siddhartha Srinivasa, Eric M Wolff, and Xin Huang. Vlm-ad: End-to-end autonomous driving through vision-language model supervision. _arXiv preprint arXiv:2412.14446_ , 2024. 3 

- [56] Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kwan-Yee K Wong, Zhenguo Li, and Hengshuang Zhao. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. _IEEE Robotics and Automation Letters_ , 2024. 1, 2 

- [57] Jiang-Tian Zhai, Ze Feng, Jinhao Du, Yongqiang Mao, JiangJiang Liu, Zichang Tan, Yifu Zhang, Xiaoqing Ye, and Jingdong Wang. Rethinking the open-loop evaluation of end-toend autonomous driving in nuscenes. _arXiv preprint_ , 2023. 2, 6 

- [58] Bozhou Zhang, Nan Song, Xin Jin, and Li Zhang. Bridging past and future: End-to-end autonomous driving with historical prediction and planning. _arXiv preprint arXiv:2503.14182_ , 2025. 6 

- [59] Henry Zheng, Hao Shi, Yong Xien Chng, Rui Huang, Zanlin Ni, Tianyi Tan, Qihang Peng, Yepeng Weng, Zhongchao Shi, and Gao Huang. Denseg: Alleviating vision-language feature sparsity in multi-view 3d visual grounding. In _Autonomous Grand Challenge CVPR 2024 Workshop_ , page 6, 2024. 1 

- [60] Henry Zheng, Hao Shi, Qihang Peng, Yong Xien Chng, Rui Huang, Yepeng Weng, zhongchao shi, and Gao Huang. Densegrounding: Improving dense language-vision semantics for ego-centric 3d visual grounding. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

   - 1 

- [61] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. Genad: Generative end-to-end autonomous driving. _arXiv preprint arXiv:2402.11502_ , 2024. 1, 2 

17819 

