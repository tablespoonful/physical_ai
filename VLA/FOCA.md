---
title: "FOCA: Future-Oriented Conditioning for Data-Efficient Vision-Language-Action Adaptation"
date: "2026-06-18"
authors: "Duc Minh Nguyen; Nghiem Tuong Diep; Binh Gia Nguyen; Trong-Bao Ho; Doanh Le; Tan Q. Nguyen"
venue: "ICML 2026"
url: https://arxiv.org/abs/2606.20867
pdf: https://arxiv.org/pdf/2606.20867
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.20867)** / [論文ページ](https://arxiv.org/abs/2606.20867)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **FOCA: Future-Oriented Conditioning for Data-Efficient Vision-Language-Action Adaptation** 

**Duc Minh Nguyen**<sup>* 1 2</sup> **Nghiem Tuong Diep**<sup>* 1 2</sup> **Binh Gia Nguyen**<sup>* 1 2</sup> **Trong-Bao Ho**<sup>1</sup> **Doanh Le**<sup>2</sup> **Tan Q. Nguyen**<sup>1</sup> **Thien-Loc Ha**<sup>1</sup> **Nhiem Tran**<sup>1</sup> **Bao Thach**<sup>1 3</sup> **Nhat X. Tran**<sup>1</sup> **Tuan A. Tran**<sup>4</sup> **Artur Habuda**<sup>5</sup> **Philip Lund Møller**<sup>5</sup> **Tran Nguyen Le**<sup>5</sup> **Daniel Sonntag**<sup>4 6</sup> **Mathias Niepert**<sup>7 8</sup> **Khoa D. Doan**<sup>2</sup> **Vu Duong**<sup>2</sup> **Hung Quoc Ngo**<sup>1</sup> **Minh N. Vu**<sup>1 2</sup> **Duy M. H. Nguyen**<sup>_†_4 7 8</sup> **An Thai Le**<sup>_†_1 2</sup> **Ngo Anh Vien**<sup>_†_1 2</sup> 

## **Abstract** 

Vision–Language–Action (VLA) models enable general-purpose robotic control via large-scale multimodal pretraining, yet their effectiveness under few-shot imitation learning remains limited. We conduct a systematic stress test of state-ofthe-art VLA models and show that performance degrades sharply as demonstrations are reduced, revealing a key weakness of existing adaptation strategies. To address this, we introduce FOCA, a future-oriented conditioning framework for dataefficient VLA adaptation. FOCA combines _explicit prediction of task-grounded future interaction_ embeddings with _implicit alignment to future goal observations_ , enabling long-horizon reasoning in latent space without pixel-level prediction. This formulation naturally _supports actionfree_ co-training with synthetic videos from video world models and can be interpreted as learning a future-conditioned value-like representation. Extensive experiments demonstrate FOCA achieves 95.7% success with 20 demonstrations on LIBERO, improves 7–12% on RoboCasa, and delivers up to 26% absolute gains on real robots, establishing a new state of the art in few-shot VLA adaptation. Our code is available at this link. 

## **1. Introduction** 

Vision–Language–Action (VLA) models extend large vision–language models to generate robot actions condi- 

> *Equal contribution . _†_ : Senior Authors (Scientific Advisor: Duy M. H. Nguyen; Core Developers: An Thai Le, Ngo Anh Vien). 1VinRobotics, Vietnam; 2Center for AI Research, VinUniversity, Vietnam;<sup>3</sup> University of Utah, USA;<sup>4</sup> German Research Center for Artificial Intelligence (DFKI);<sup>5</sup> Technical University of Denmark, Denmark;<sup>6</sup> University of Oldenburg, Germany;<sup>7</sup> University of Stuttgart, Germany;<sup>8</sup> Max Planck Research School for Intelligent Systems (IMPRS-IS), Germany. Correspondence to: Ngo Anh Vien _<_ v.vienna@vinrobotics.net _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

tioned on visual observations and language instructions, enabling scalable robotic control across tasks, embodiments, and environments. Leveraging large-scale multimodal pretraining, recent VLA systems - spanning web-knowledge transfer to robotics and open generalist robot policies - have demonstrated impressive generalization across diverse manipulation settings and platforms (Zitkovich et al., 2023; Kim et al., 2024; Qu et al., 2025b; Team et al., 2024; Black et al., 2024; Intelligence et al., 2025; Bjorck et al., 2025; Team et al., 2025b;a). Alongside these rapidly advancing model families, recent analyses have begun to clarify key design choices that influence the performance of generalist VLA policies (Liu et al., 2025). 

Despite these advances, the data efficiency of VLA models during task adaptation remains insufficiently understood. In practice, collecting task-specific robot demonstrations is costly, and deployment often involves continual distribution shifts - new object instances, changed viewpoints, or minor workspace reconfigurations - that make large demonstration budgets impractical. Yet many evaluations of modern VLAs still adapt with substantially more than a handful of trajectories, leaving open whether pretrained VLA representations reliably translate into _few-shot_ adaptability. In particular, the behavior of state-of-the-art VLA models under few-shot imitation learning (e.g., adapting with only 10–30 demonstrations) has not been systematically stress tested. Motivated by this gap, we evaluate strong pretrained VLA models under severely limited demonstration budgets and observe substantial performance degradation, highlighting the need for more data-efficient adaptation mechanisms. 

Our key observation is that few-shot adaptation is limited not only by the number of action-labeled trajectories, but also by how much _learning signal_ each trajectory provides. Standard behavioral cloning fine-tuning provides one supervised action target per time step; however, each demonstration also contains rich _future observations_ that reveal how the scene should evolve when the task is executed successfully. Existing adaptation largely treats demonstrations as independent (observation, action) pairs and does not explicitly leverage the long-horizon structure visible in future frames. These future observations can provide dense, task-aligned supervision about long-horizon task progress, beyond local 

1 

**FOCA-VLA** 

action matching. Moreover, future-conditioned learning has long been a principled way to capture long-horizon structure, as in goal-/future-conditioned value functions and successorstyle representations (Schaul et al., 2015; Dayan, 1993). We therefore propose FOCA, a _future-oriented conditioning_ approach for data-efficient VLA adaptation that explicitly exploits future observations to shape representations and improve long-horizon decision-making. 

In contrast to prior approaches that predict pixel-level future frames (Zhao et al., 2025; Hu et al., 2025), FOCA operates entirely in latent embedding space, avoiding the computational cost and redundancy of dense scene reconstruction. Moreover, rather than modeling full scenes, FOCA focuses supervision on task-grounded dynamic regions corresponding to robot–object interactions inferred from the current observation and instruction. We achieve this by introducing a small set of representative tokens that summarize joint vision–language context and are decoded to predict future latent embeddings of interaction regions. This design conditions the policy on anticipated outcomes while remaining invariant to static or task-irrelevant content, aligning with recent advances in self-supervised learning that emphasize prediction in representation space over pixel-space generation (Oord et al., 2018; Assran et al., 2023). 

Beyond explicit prediction, FOCA introduces an implicit future-conditioning objective that provides an action-free _auxiliary_ supervision signal during adaptation. Instead of predicting future states explicitly, FOCA aligns taskgrounded interaction tokens extracted from the current observation with vision embeddings of future goal frames sampled later in the same episode, while contrasting them against embeddings from other tasks. This formulation allows FOCA to directly leverage _synthetic rollouts generated by video world models_ (e.g., DreamGen (Jang et al., 2025)) as additional future-structured supervision, without requiring pseudo-actions (Ye et al., 2025) or inverse dynamics (Baker et al., 2022). As a result, the policy can be rapidly adapted to new scenarios by modifying prompts and generating corresponding videos. 

Conceptually, the implicit alignment objective encourages the model to encode long-horizon task structure and goal progression directly in representation space. Under geometric future sampling, this objective can be interpreted as estimating goal-conditioned discounted occupancies, a valuelike notion of reachability, thereby connecting FOCA to contrastive formulations of goal-conditioned reinforcement learning and successor representations (Watkins & Dayan, 1992; Dayan, 1993). This perspective explains why futureoriented conditioning can provide effective long-horizon supervision during imitation-based adaptation, even though the implicit auxiliary objective itself does not require action labels (Eysenbach et al., 2021). 

**Contributions.** We make the following contributions: 

- **Few-shot stress test for VLA adaptation.** We provide a systematic evaluation of state-of-the-art VLA models under few-shot imitation learning, revealing substantial degradation when adapting from only 10–30 demonstrations. 

- **Future-oriented conditioning for data-efficient adaptation.** We introduce FOCA, which augments VLA adaptation with explicit and implicit futureconditioning objectives in latent space, focusing on task-grounded interaction tokens rather than dense pixel prediction. The implicit objective naturally supports action-free auxiliary supervision from synthetic videos. 

- **Strong empirical results across simulation and real robots.** We run experiments across a diverse set of 9 simulated benchmarks, a simulated humanoid and 3 real-robot setups with an Aloha robot arm, observing consistent improvements in few-shot adaptation over strong VLA baselines and adaptation methods. 

## **2. Related Works** 

**VLA Models and Generalist Robot Policies.** Recent work on VLA models unifies perception, language understanding, and control to enable general-purpose robotic manipulation from images and natural language. Existing approaches largely fall into two paradigms. Autoregressive VLAs (e.g., RT-1/2 (Brohan et al., 2022; Zitkovich et al., 2023), OpenVLA (Kim et al., 2024), Gemini (Team et al., 2025b)) generate actions sequentially using large language model backbones, achieving strong generalization through large-scale imitation learning. Diffusion-based VLAs (e.g., _π_ 0 (Black et al., 2024), Octo (Team et al., 2024), GR00T (Bjorck et al., 2025)) instead synthesize continuous action sequences via diffusion or flow-matching, offering improved robustness and parallel action generation. Despite their success, these models are typically trained and adapted using substantial demonstration budgets, leaving their data efficiency under few-shot adaptation largely unexplored. 

FOCA complements these lines of work by addressing dataefficient VLA adaptation. Rather than proposing a new policy architecture, FOCA injects future-oriented learning signals into pretrained VLAs during fine-tuning, enabling effective few-shot transfer across tasks and robot embodiments with significantly fewer demonstrations. 

**Few-shot Imitation Learning and Data-Efficient Adaptation.** Adapting a robot policy to new tasks with few demonstrations remains a central challenge in robotics (Duan et al., 2017). Classic behavior cloning is brittle under compounding error, motivating expressive visuomotor imitation models such as Action Chunking with Transformers (ACT) (Zhao et al., 2023) and diffusion-based 

2 

**FOCA-VLA** 


_Figure 1._ FOCA augments VLA adaptation by injecting future-oriented conditioning into a vision–language model _Fθ_ ( _·_ ) and a diffusionbased action policy _Aϕ_ ( _·_ ). It jointly learns explicit latent prediction of task-grounded future interaction (bounding boxes _Bt_<sup>_i_+) embeddings</sup> via learnable **r**<sup>exp</sup> _t_ tokens and implicit alignment to future goal observations via **r**<sup>imp</sup> _t_ tokens, enabling data-efficient, action-free adaptation and seamless integration with synthetic videos from video world models. 

policies (Chi et al., 2023). While effective within their training distributions, these models are typically trained from scratch or with limited pretraining, which restricts their ability to generalize to unseen environments and often necessitates substantial task-specific data for adaptation. 

At the same time, to mitigate the computational and data cost of adapting pretrained VLA models in low-resource settings (Kim et al., 2024; Mitra et al., 2025), parameterefficient fine-tuning (PEFT) approaches such as LoRA (Hu et al., 2021) and DoRA (Liu et al., 2024b) have been explored. ControlVLA (Li et al., 2025) in another direction introduces object-centric conditioning via a ControlNet-style interface (Zhang et al., 2023). In contrast, FOCA explicitly incorporates _future-oriented_ auxiliary objectives via explicit prediction and implicit alignment to increase the learning signal per demonstration and enable more data-efficient adaptation, including the use of action-free video data. 

**Robot Knowledge Prediction and Contrastive Objectives.** Prior VLA models incorporate auxiliary prediction objectives, such as chain-of-thought reasoning (Huang et al., 2025), trajectory generation (Zheng et al., 2025a), or futurestate forecasting (Team et al., 2025a), to improve spatial and temporal understanding. In particular, pixel-level future frame prediction has been explored as a form of selfsupervision (Seo et al., 2023a; Zhao et al., 2025), but dense image reconstruction is often redundant and difficult to optimize, especially in low-data regimes. FOCA instead predicts future information directly in latent space and focuses 

supervision on task-grounded interaction regions, avoiding full-scene reconstruction while preserving control-relevant structure. 

Contrastive learning has also been widely used in robotics to improve transfer and generalization, including temporal (Sermanet et al., 2018), multimodal (Rana et al., 2023; Ma et al., 2024), and trajectory-level objectives (Lee et al., 2025). However, most existing methods are designed for CLIP-style models or relatively small policies, and do not readily scale to large pretrained VLA models. FOCA addresses this by introducing a compact set of representative tokens that summarize vision–language context and serve as an efficient interface for future alignment within the VLM. While closely related to FLARE (Zheng et al., 2025b), which applies future alignment during diffusionpolicy pretraining, FOCA injects future-oriented objectives directly into the VLM during downstream adaptation and yields additional gains even on GR00T-N1.5 (Bjorck et al., 2025), whose diffusion policy already incorporates FLAREstyle pretraining. We present in the Appendix more details of the discussion on those related works. 

## **3. Methods** 

### **3.1. Problem Definition** 

We formulate FOCA as a plug-and-play framework that augments diffusion-based VLA policies, such as _π_ 0 and GR00T-N1.5, for few-shot imitation learning. An overview is shown in Figure 1. 

3 

**FOCA-VLA** 

Let _D_ = _{_ ( _τm, lm_ ) _}_<sup>_M_</sup> _m_ =1<sup>denote a dataset of episodes paired</sup> with task instructions. Each episode _τ_ = _{_ ( **o** _t,_ **a** _t_ ) _}_<sup>_T_</sup> _t_ =1 consists of multi-view observations **o** _t_ = [ _It_<sup>1</sup><sup>_, . . . , I_</sup> _t_<sup>_N_] and</sup> action chunks **a** _t_ = ( _at, . . . , at_ + _k_ ). Given an instruction _l_ and observation **o** _t_ , the pretrained vision–language model (VLM) _Fθ_ produces a hidden representation: **h** _t_ = _Fθ_ ( _l,_ **o** _t_ ) _._ (1) 

FOCA augments the VLM by introducing two _types of auxiliary tokens_ : an explicit future token set **r**<sup>exp</sup> _t_ and an implicit future token set **r**<sup>imp</sup> _t_ . These tokens are concatenated with ( _l,_ **o** _t_ ) and jointly processed by the VLM: 


The token outputs are mapped by lightweight heads. The explicit head _Pω_<sup>exp</sup> ( _·_ ) produces interaction-focused embeddings from ˜ **r**<sup>exp</sup> _t_ for predicting future gripper–object interactions, while the implicit head _Pψ_<sup>imp</sup> ( _·_ ) maps ˜ **r**<sup>imp</sup> _t_ to a contrastive embedding used for alignment with future goal observations across time and episodes. 

### **Action Generation with Future-Aware Representations.** 

Given the future-aware representations from the VLM, actions are generated using a denoising diffusion Transformer _Aϕ_ ( _·_ ). At diffusion (flow-matching) time _ρ ∈_ [0 _,_ 1], the policy is conditioned on the robot state **s** _t_ , a noised action chunk ˜ **a** _t,ρ_ , and the joint vision–language embeddings _{_ **h** _t,_ ˜ **r**<sup>exp</sup> _t ,_ ˜ **r**<sup>imp</sup> _t }_ : 


where **v** ˆ _t,ρ_ denotes the predicted denoising direction/velocity for the action chunk. At inference time, we start from Gaussian noise and integrate (or iteratively denoise) to obtain the action chunk **a** _t_ . 

The conditioning mechanism depends on the underlying VLA architecture. GR00T-N1.5 injects the final VLM embedding into _Aϕ_ via cross-attention at every Transformer layer, whereas _π_ 0 conditions each diffusion layer using intermediate VLM features through layer-wise cross-attention. We next introduce the future-oriented training objectives. 

### **3.2. Explicit Future Latent Prediction** 

For manipulation, successful execution is largely determined by the future evolution of interactions between the robot’s gripper and task-relevant objects specified by the instruction. This motivates forecasting future representations of _object-centric interaction regions_ where the gripper engages with language-grounded objects, providing a direct and data-efficient learning signal for action generation. 

**Object-Centric Region Construction.** Given a view _It_<sup>_i_+</sup> at time _t_<sup>+</sup> _> t_ within the same episode and instruction _l_ , we use an off-the-shelf grounding model _G_ ( _·_ ) to localize 

task-relevant objects and the robot gripper: 


where each _Bt_<sup>_i_+</sup> _,q_<sup>isaboundingboxcorrespondingtoa</sup> language-grounded object or the gripper. We define a single _object-centric interaction region_ as the minimal enclosing box: 


which captures the spatial extent of robot–object interactions and serves as the target region for explicit future latent prediction. 

**Latent-space Future Interaction Prediction.** At each timestep _t_ , we initialize a set of explicit prediction tokens **r**<sup>exp</sup> _t ∈_ R<sup>_n_e</sup><sup>_×d_</sup> as learnable parameters (optionally allocating _n_ e _/N_ tokens per view) and append them together with the visual tokens from **o** _t_ and language tokens from _l_ as input to the VLM. We map the explicit token outputs ˜ **r**<sup>exp</sup> _t_ to a prediction space via a lightweight predictor _Pω_<sup>exp</sup> ( _·_ ) to produce a future region embedding for view _i_ at time _t_<sup>+</sup> : **y** ˆ _t_<sup>_i_+=</sup><sup>_P_</sup> _ω_<sup>exp</sup> �˜ **r** _t_ exp _,_ PE( _Bt_<sup>_i_+)</sup> � _∈_ R<sup>_Np×de_</sup> _,_ (4) where _Np_ denotes the number of patch tokens used to represent the interaction region (e.g., via cropping/resizing to a fixed patch grid), PE( _·_ ) is a positional encoding of _Bt_<sup>_i_+(e.g.,</sup> normalized box coordinates), and _Pω_<sup>exp</sup> can be implemented as a small Transformer. 

To form the prediction target, we extract object-centric patch features from _It_<sup>_i_+restrictedto</sup><sup>_B_</sup> _t_<sup>_i_+usingafrozenvision</sup> encoder _V_ ( _·_ ) inside the VLM: 


where Patch( _._ ) denotes a patch layer inside the vision encoder _V_ ( _._ ) (Zhai et al., 2023), extracting image local features and further restricted to tokens inside _Bt_<sup>_i_+, so the target</sup> captures only interaction-relevant content. Finally, we formulate the predicted embedding to the target in the _latent space across views_ as: 


### **3.3. Implicit Future Alignment** 

While explicit prediction encourages the model to anticipate _how_ object-centric interactions will evolve, the implicit future alignment provides a complementary signal that captures _where_ the task is heading at a representation level, encouraging long-horizon task semantics and goal reachability. 

Given multi-view observation **o** _t_ = _{It_<sup>_i}N_</sup> _i_ =1<sup>, we initialize</sup> implicit tokens **r**<sup>imp</sup> _t ∈_ R<sup>_N×d_</sup> by pooling features from the frozen vision encoder _V_ ( _._ ) followed by another shared learnable projection layer _W_<sup>imp</sup> as: 

**r**<sup>imp</sup> _t_ = Agg � _{W_<sup>imp</sup> (Pool( _V_ ( _It_<sup>_i_)))</sup><sup>_}N_</sup> _i_ =1� (7) where Agg( _._ ) denotes the concatenation operator and 

4 

**FOCA-VLA** 

Pool( _._ ) denotes for mean pooling layer. 

The output ˜ **r**<sup>imp</sup> _t_ of **r**<sup>imp</sup> _t_ after the VLM model is mapped to a contrastive embedding space via a projection head _Pψ_<sup>imp</sup> ( _._ ): 


Similarly to in equation (5), we also define the future goal embeddings at timestep _t_<sup>+</sup> within the same episode as: 


that extract global embedding vision using Pool( _._ ) function and restricted inside the region _Bt_<sup>_i_+.Our goal is to make the</sup> representative token **r**<sup>imp</sup> out<sup>encode future-aware representa-</sup> tions while remaining discriminative against semantically similar but task-mismatched episodes ( _l_<sup>_′̸_</sup> = _l_ ). Accordingly, we construct the negative set from other minibatch episodes with different task descriptions: 


where all embeddings **y** _t_<sup>_j′_arecomputedusingthesame</sup> object-centric aggregation operator over the corresponding region _Bt_<sup>_j′_(</sup><sup>_t′> t_).Finally, we optimize the InfoNCE-style</sup> loss (Oord et al., 2018): 


where _s_ ( _._ ; _,_ ) is cosine similarity, _λ_ is a temperature. We sample the future offset _k_ = _t_<sup>+</sup> _− t_ from a (truncated) geometric distribution, matching the discounted reachability interpretation in Sec. 4.2. 

### **3.4. Co-training Future Prediction with Denoising Diffusion Transformer** 

**Structured Token Isolation between Explicit and Implicit Tasks.** To enforce functional disentanglement between explicit and implicit future modeling, we introduce a _structured token-isolation mask_ within the VLM attention layers (Zhao et al., 2025). Specifically, we block direct information exchange between the explicit prediction tokens **r**<sup>exp</sup> _t_ and the implicit alignment tokens **r**<sup>imp</sup> _t_ , while allowing both to attend to shared vision and language tokens: Attn( **r**<sup>exp</sup> _t ↔_ **r**<sup>imp</sup> _t_ ) = 0, and Attn( **r**<sup>exp</sup> _t ↔_ vision/text), Attn( **r**<sup>imp</sup> _t ↔_ vision/text) are unconstrained. The isolation constraint is implemented differently depending on the attention structure of the VLA backbone (bidirectional vs. causal), ensuring the two token groups learn complementary roles without supervisory leakage. 

**Co-training across Objectives.** We sample a flowmatching time _ρ ∈_ [0 _,_ 1] and noise _ϵ ∼N_ ( **0** _,_ **I** ), and form a noised action chunk: 

For this linear interpolation, the target velocity is ( **a** _t − ϵ_ ). We train the diffusion policy to match this target via the flow-matching loss: 


In summary, we co-train three objectives: _L_ total = _L_ fm + _L_ exp+ _L_ imp _._ For action-free videos (e.g., synthetic rollouts), we omit _L_ fm and optimize only _L_ exp and _L_ imp. During inference, the learned tokens are used solely to condition action prediction; no future prediction is performed. 

## **4. Analysis of Future-Conditioned Objectives** 

### **4.1. Action-Free Learning from Synthetic Rollouts** 

We next highlight a key advantage of FOCA stemming from its implicit future-alignment objective. By relaxing the requirement for precisely localized interaction regions, the objective _L_ imp can be directly applied to synthetic videos generated by video world models such as DreamGen (Jang et al., 2025), without relying on pseudo-action labels or inverse-dynamics modeling (Ye et al., 2025). To exploit this property, we adopt a two-stage training strategy: (i) we first fine-tune the video world model using an existing few-shot demonstration, then generate diverse, prompt-conditioned synthetic rollouts to optimize _L_ imp( _._ ). This _action-free supervision_ shapes FOCA’s representations to predict future task goals, enabling effective adaptation with limited realworld data. (ii) We then co-train on real robot demonstrations by jointly optimizing the full objective _L_ total This curriculum enables FOCA to absorb future-structured knowledge from large-scale, action-free video while retaining precise control through explicit prediction and action supervision, yielding strong data-efficient adaptation ( **Q2. in experiment.** ). 

### **4.2. Implicit Future Alignment as Goal-Conditioned Discounted Occupancy** 

FOCA’s implicit objective _L_ imp (Eq. (11) performs _futureconditioned contrastive learning_ between a _context_ token from the current input and a _future_ interaction/goal embedding sampled later in the same episode. Concretely, let _st_ denote the VLA input (multi-view observation plus language) at time _t_ . FOCA forms the implicit context token _xt_ := _zt_ (Eq. (8)) and a future interaction embedding _gt_ + _k_ := _yt_ + _k_ = _h_ ( _st_ + _k_ ) (Eq. (9)), where _h_ ( _·_ ) denotes the region-restricted pooling over dynamic interaction regions. Negatives are drawn from the task-mismatched pool _N¬_ task (Eq. (10), which we model as a proposal distribution _p_ neg( _g_ ). We show that _L_ imp learns a value-like _reachability_ score corresponding to discounted goal occupancy under demonstrations (proofs in Appendix F). 


5 

**FOCA-VLA** 

_Table 1._ Performance comparison of FOCA vs SOTA VLA models under different data scales. _(a)_ Sensitivity to few-shot imitation learning rate _(b)_ 

||_(a)_ S|ensitivit|y to few-|shot imi|tation le<br>D|arning ra<br>emonstra|te<br>tion Rat|io|||||_(b)_ Comparison wit   i<br>methods for VLA <br>Libero.|h general  i<br>adaptatio|and taski<br>n (avera|-specific PEFT<br>ge success) in|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Method||100|%|||40|%|||10|%|||Demo|nstration|Ratio|
||Avg|10|Obj.|Spa.|Avg|10|Obj.|Spa.|Avg|10|Obj.|Spa.|PEFT methods|100%|40%|10%|
|_π_0|94.6|90.0|98.2|94.6|89.9|82.0|95.2|89.6|77.6|59.0|80.6|83.4||Avg|Avg|Avg|
|Groot-N1.5|94.6|**92.8**|98.4|94.4|91.4|84.5|98.9|90.6|78.2|62.6|85.7|85.7|||||
|EO-1|94.1|91.4|96.6|89.8|91.0|**88.4**|96.0|86.8|82.2|65.0|89.6|83.0|Control-VLA|95.6|91.3|78.4|
|SmolVLA|92.5|82|99|93|90.3|80|96.0|90.0|77.3|51.3|86|81.0|LoRA (_r_=64)|94.2|90.2|78.2|
|**FOCA**|**96.6**|92.4|**99.8**|**97.0**|**94.0**|88.0|**99.6**|**93.6**|**85.3**|**69.4**|**90.4**|**89.4**|DoRA (_r_=64)|94.7|92|78.6|
||||||||||||||**FOCA**|**96.6**|**94.0**|**85.3**|


|_(a)_ FOCA vs wid|e range of|VLA mod|els when u|sing full 1|00% data|
|---|---|---|---|---|---|
|Method|Avg|10|Goal|Object|Spatial|
|Diff. Policy|72.4|50.5|68.3|92.5|78.3|
|Octo|75.1|51.1|84.6|85.7|78.9|
|Open-VLA|76.5|53.7|79.2|88.4|84.7|
|Spatial-VLA|78.1|55.5|78.6|89.9|88.2|
|CoT-VLA|69.0|87.6|91.6|87.5|81.1|
|DreamVLA|92.6|89.5|89.5|94.0|**97.5**|
|Groot-N1.0|93.9|90.6|93.0|97.6|94.4|
|Groot-N1.5|94.6|**92.8**|92.8|98.4|94.4|
|EO-1|94.1|91.4|**98.6**|96.6|89.8|
|Think-Act|84.4|70.9|87.1|91.4|88.3|
|SmolVLA|92.5|82.0|96.0|99.0|93.0|
|_π_0 Fast|85.5|60.2|88.6|96.8|96.4|
|_π_0|94.6|90.0|95.4|98.2|94.6|
|**FOCA (Ours)**|**96.6**|92.4|97.4|**99.8**|97.0|


_Figure 2._ FOCA vs SoTA VLA models on full data scale. 10, Goal, Object, and Spatial denote the Libero-10, Libero-Goal, Libero-Object, and Libero-Spatial benchmark suites, respectively. 

**Discounted goal occupancy induced by geometric sampling.** We sample a future offset _k ∼_ Geom(1 _− γ_ ) on _{_ 1 _,_ 2 _, . . .}_ and treat ( _xt, gt_ + _k_ ) as a positive pair. This induces the goal-conditioned _discounted occupancy_ under the demonstration distribution: 


where the probability is taken over trajectories in the offline dataset and the goal extractor _h_ . 

**Theorem 4.1** (Implicit alignment estimates a goal-conditioned value (log occupancy ratio)) **.** _Assume negatives are sampled from a proposal p_ neg( _g_ ) _independent of xt (instantiated in FOCA via N¬_ task _), and L_ imp _is optimized to the population optimum. Then the optimal score satisfies_ 


**Proposition 4.2** (Explicit future prediction estimates an occupancy mean) **.** _Let_ � _gθ_ ( _xt_ ) _denote FOCA’s explicit prediction of the future interaction embedding and suppose L_ exp _is the squared-error loss in Eq._ (6) _. Under the same geometric sampling as in Eq._ (14) _, any population-optimal predictor satisfies_ 

_g_ �<sup>_∗_</sup> ( _xt_ ) = E _g∼ρµ_ ( _·|xt_ )[ _g_ ] _,_ (16) _i.e., explicit prediction estimates the conditional mean under the goal-occupancy distribution._ 

**Implications for FOCA.** Eq. (15) shows that the similarity score in Eq. (11) acts as a value-like reachability signal in representation space. Because it depends only on observation/language tokens and goal extractor _h_ , _L_ imp naturally supports action-free training on world-model videos (Sec. 4.1). Meanwhile, Proposition 4.2 clarifies that _L_ exp provides a complementary signal by predicting a concrete summary (occupancy mean) of future interaction embeddings, which is directly useful for control. See Appendix F for assumptions, proofs, and more extensions (fixed-horizon futures, robustness bounds, and factorization analyses). 

## **5. Experiments** 

### **5.1. Main results** 

In this section, we present the main experimental results of FOCA in both simulated and real-world environments (Figure 2-right and Section C Appendix). For details about implementation, other robot setups, we refer readers to the Sections D, E in the Appendix. To systematically evaluate the proposed framework, we design experiments to address the following questions. 

**Q1: Data efficiency of FOCA for VLA model adapta-** 

**tion.** We aim to evaluate the data efficiency and robustness of FOCA for VLA adaptation, with an emphasis on few-shot imitation learning. We study its (i) performance across varying demonstration budgets on LIBERO (Liu et al., 2023), corresponding to 10%, 40%, and 100% of 

6 

**FOCA-VLA** 


_Figure 3._ (a) FOCA’s performance on <mark>four real-robot tasks</mark> using a humanoid (VinR-H3, a simulated task) (GR00T N1.5 VLA, evaluation on 50 trials), and three other with bi-arm Aloha robot using _π_ 0 VLA; (b) Ablation study on explicit future prediction ; (c) FOCA’s generalization performance across _π_ 0 and <mark>GR00T N1.5</mark> on <mark>Robocasa,</mark> with 30 demos ( **top** ) and 100 demos ( **bottom** ) on most 5 challenge tasks; (d) _π_ 0 vs FOCA, <mark>FOCA</mark> w e <mark>xplicit</mark> , and <mark>FOCA</mark> w i <mark>mplicit</mark> at 100%, 40% and 10%; (b) and (e) be ablation study on explicit and implicit future prediction. 

_Table 2._ Performance comparison between FOCA variants and pseudo-actions learned via inverse generative modeling (IGM) from DreamGen-generated synthetic videos. 

|||Demonstration Ratio||
|---|---|---|---|
|Method|100%|40%|10%|
||Avg 10 Go. Obj. Spa.|Avg 10 Go. Obj. Spa.|Avg 10 Go. Obj. Spa.|
|_π_0|94.6 90.0 95.4 98.2 94.6|89.9 82.0 92.6 95.2 89.6|77.6 59.0 87.4 80.6 83.4|
|IGM|94.3 90.0 95.2 98.2 93.6|90.2 82.8 95.6 94.8 87.8|76.8 61.8 84.0 79.8 81.4|
|**FOCA(Imp.)**|95.8<br>91.0<br>97.2<br>98.4<br>96.6|93.0<br>87.0<br>94.4<br>97.6<br>92.9|83.6<br>65.6<br>91.0<br>90.0<br>87.6|
|**FOCA(D.G.)**|**96.7**<br>**92.6**<br>**96.8**<br>**99.2**<br>**98.0**|**95.7**<br>**89.4**<br>**96.6**<br>**98.6**<br>**98.0**|**86.4**<br>**73.2**<br>**91.4**<br>**91.8**<br>**89.2**|


the training data (approximately 5, 20, and approximately 43 demonstrations per task, respectively); (ii) compare it against parameter-efficient fine-tuning methods, and assess (iii) its competitiveness with state-of-the-art VLA models under scarce and full supervision. 

_→_ **Baselines and evaluation protocol.** We integrate FOCA into the _π_ 0 (Black et al., 2024) vision–language–action (VLA) model and compare against a diverse set of strong pretrained VLA baselines adapted via standard imitation learning, including GR00T-N1.5 (Bjorck et al., 2025), EO1 (Qu et al., 2025a), and SMOLVLA (Shukor et al., 2025). These models represent state-of-the-art (SOTA) generalist policies across diverse architectural scales, with SMOLVLA demonstrating competitive generalization despite its smaller backbone. All methods are evaluated under identical data splits, training budgets, and evaluation protocols. 

To disentangle the effect of future-oriented conditioning from parameter efficiency, we additionally compare against 

representative parameter-efficient fine-tuning (PEFT) methods applied to the same _π_ 0 backbone, including LORA (Hu et al., 2021), DORA (Liu et al., 2024b), and CONTROLVLA (Li et al., 2025). These baselines capture a broad spectrum of recent PEFT strategies designed to stabilize or regularize VLA adaptation under limited supervision. 

Finally, under the full-data setting (100%), we benchmark FOCA against a wide range of state-of-the-art generalized robot policies and VLA systems reported in the literature, including DIFFUSION POLICY (Chi et al., 2023), OCTO (Team et al., 2024), OPEN-VLA (Kim et al., 2024), SPATIALVLA (Qu et al., 2025b), COT-VLA (Zhao et al., 2025), DREAMVLA (Zhang et al., 2025), THINK-ACT (Huang et al., 2025), and _π_ 0-fast (Pertsch et al., 2025). Among these, THINK-ACT, COT-VLA, and DREAMVLA also incorporate future prediction objectives, but operate at the text reasoning or pixel level, and do not model task-grounded interaction representations in latent space. Reported results are taken from the original publications, except for EO-1, which we reimplement due to prohibitive default training time (40 hours), while FOCA and other methods converge within 20 hours under our setup. 

_→_ **Result.** As shown in Table 1 and Fig. 2(a), FOCA consistently improves data efficiency for VLA adaptation. With only **40% of demonstrations** , **FOCA** achieves **94.0%** success on LIBERO, closely matching _π_ 0 trained with **100% data (94.6%)** , while in the 10% regime it substantially re- 

7 

**FOCA-VLA** 

duces the few-shot gap, improving success **from 77.6% to 85.3%** and outperforming PEFT methods, which plateau around _∼_ 78%. FOCA also attains state-of-the-art performance under full supervision. These results suggest that _few-shot VLA adaptation is limited more by the quality of supervision than by model capacity_ ; FOCA addresses this by using future observations to provide richer learning signals that improve long-horizon behavior. 

**Q2: Leveraging synthetic videos without action supervision.** We investigate whether FOCA effectively leverages synthetic rollouts from video world models without access to action labels, and how this compares to approaches that rely on pseudo-actions inferred from video. 

_→_ **Baseline setup.** For each data regime (10%, 40%, and 100%), we first fine-tune the open-world model DreamGen (Jang et al., 2025) on the corresponding real demonstrations. Using the resulting checkpoint, we generate synthetic task-consistent videos conditioned on task descriptions and initial frames from training episodes. These videos are then used in two ways. 

- Inverse generative modeling (IGM) (Baker et al., 2022): we train the IGM model on the synthetic videos to infer pseudo-actions, which are subsequently used to finetune the _π_ 0 VLA model. 

- FOCA variants: we consider two setups. (a) FOCA + IMPLICIT co-trains the VLA model using action supervision on real data together with FOCA’s implicit future-alignment objective _(we disable explicit future prediction)_ . (b) FOCA + DREAMGEN first pretrains the VLA model using FOCA’s implicit objective on DreamGen-generated videos only, then continues training as in FOCA + Implicit using real demonstrations. 

_→_ **Results.** As shown in Table 2, pseudo-action–based **IGM yields no consistent improvement** over _π_ 0, matching performance only with full data and degrading under limited supervision. In contrast, **FOCA consistently improves** performance across all regimes: even with implicit alignment alone, FOCA outperforms both _π_ 0 and IGM, and incorporating synthetic videos further amplifies these gains at **40% data** , **FOCA + DreamGen (95.7%)** surpasses _π_ 0 trained with **100% data (94.6%)** . These results indicate that pseudo-action inference is brittle due to noise in recovered actions, while FOCA’s **future-oriented conditioning** leverages synthetic videos as representation-level supervision, remaining robust even when generated rollouts are imperfect. We present additional details about DreamGen’s synthetic rollouts in the Appendix. 

### **Q3: How does FOCA generalize across different VLA architectures and different real robotic embodiments?** 

**FOCA on GR00T N1.5.** To assess whether FOCA generalizes beyond a single backbone, we integrate it with two 

architecturally distinct VLA models, _π_ 0 and GR00T-N1.5, and evaluate on the ROBOCASA benchmark under both 30- and 100-demonstration regimes across five challenging manipulation tasks. We additionally compare against GR00T-N1.0 and SMOLVLA. As shown in Fig. 3c, FOCA consistently improves performance across all tasks and data scales, yielding **gains of 4.4 - 12%** on _π_ **0** and **7.2 - 10.4%** on **GR00T-N1.5** . These results demonstrate that FOCA generalizes effectively across VLA architectures. Full results are provided in the appendix (Figure 10). 

**FOCA in real-world setups.** We further evaluate FOCA in three real-robot setups spanning two distinct robotic platforms - bimanual ALOHA ROBOT (Aldaco et al., 2024) and a simulated HUMANOID PLATFORM - and diverse manipulation tasks: _Place Parts, Open Bag, Set Table, and Tie Shoelaces_ . The details for robot setup are presented in detail in Sec. E, with task examples that can be visualized in Sec. C, Appendix. The results are summarized in Figure 3a. 

Across real-world robot platforms, FOCA consistently improves performance over base VLA models under both limited and full supervision. On the simulated **humanoid** , FOCA boosts GR00T-N1.5 from **58% to 84%** success rate on the Place Part task, demonstrating strong transfer to an industrial-scale robot with distinct kinematics and sensing. 

On the **Aloha bimanual robot** , FOCA yields substantial gains across challenging household tasks using _π_ 0 as the backbone. Notably, FOCA doubles success on _Open Bag_ under limited data _(20% → 40%)_ and improves full-data performance to 45%. On the highly dexterous Tie Shoelaces task, it reaches 95% success. Together, these results demonstrate that FOCA generalizes robustly across robot embodiments, task types, and real-world deployment conditions. 

### **5.2. Ablation study** 

**Contribution of explicit and implicit components.** We ablate FOCA’s explicit and implicit modules on LIBERO across different data regimes (Fig. 3d). Full FOCA consistently outperforms both ablations and the base _π_ 0, with the gap widening as data decreases; at 10% data, FOCA achieves 85.3%, substantially outperforming either component alone. This confirms that explicit interaction-centric prediction and implicit goal-level alignment provide complementary signals that are critical in low-data settings. 

**Explicit and implicit ablations.** We ablate FOCA’s explicit and implicit future-conditioning designs under moderate and low-data regimes. For explicit one (Fig.3(b)), operating in a _latent, object-centric space_ consistently _outperforms pixel-level alternatives_ , showing that structured representations provide more robust supervision by suppressing task-irrelevant visual variability; performance is further sensitive to the number of representative tokens, with a moderate token count yielding the best results. For implicit 

8 

**FOCA-VLA** 

_Table 3._ Ablation study on token initialization strategies for implicit and explicit tokens in FOCA on LIBERO at 40% data scale. 

|**Method**|**10**|**Go.**|**Obj.**|**Spa.**|**Avg**|
|---|---|---|---|---|---|
|_π_0 Baseline|82|92.6|95.2|89.6|89.85|
|FOCA (ada. impli., rand. expli.)|88|94.6|99.6|93.6|93.95|
|FOCA (both random)|84.2|92.6|97.8|92.2|91.7|
|**FOCA (both adaptive)**|**87.8**|**96**|**98.4**|**95**|**94.3**|


_Table 4._ Ablation study on token initialization strategies for implicit and explicit tokens in FOCA on LIBERO at 100% data scale. 

|**Method**|**10**|**Go.**|**Obj.**|**Spa.**|**Avg**|
|---|---|---|---|---|---|
|_π_0 Baseline|90|95.4|98.2|94.6|94.6|
|FOCA (ada. impli., rand. expli.)|92.4|**97.4**|**99.8**|**97**|96.6|
|**FOCA ((both adaptive)**|**92.8**|97.2|99.6|**98.2**|**97**|


alignment (Fig. 3(e)), focusing on a single, well-aligned future frame with object-centric representations yields strong performance, while extending alignment to _multiple future frames achieves comparable results_ . In contrast, _alternative contrastive objectives are less effective_ . Together, these ablations show that our design choices are critical for extracting long-horizon learning signals in few-shot settings. 

**Token initialization strategies for implicit and explicit tokens.** We also compare four variants: the _π_ 0 baseline, static (random) initialization for both token types, dynamic (adaptive) initialization for implicit tokens only, and dynamic initialization for both token types. Results from Table 3 and 4 show that dynamic initialization consistently improves performance, with the fully adaptive variant achieving the best average score, validating the importance of grounding both token types in visual features for effective future-oriented conditioning. 

**Comparison with re-implemented future-oriented baselines.** We also compare FOCA with representative futureoriented baselines, including DreamVLA-style (Zhang et al., 2025) and FLARE (Zheng et al., 2025b), under the same policy backbones and fine-tuning settings, as shown in Tables 5, 6, and 7. For fair comparison, DreamVLA-style dynamic future conditioning is integrated into _π_ 0, while FLARE is re-implemented following its original design due to the absence of publicly available fine-tuning code. Results show that future-oriented conditioning generally improves over the corresponding baselines across most tasks and benchmarks. However, FOCA consistently achieves the best overall performance in all settings. On LIBERO with _π_ 0 at 40% data scale, FOCA improves the average score from 92.1 (DreamVLA) and 91.0 (FLARE) to 94.0. Similarly, at 100% data scale, FOCA outperforms DreamVLA-style conditioning by +1.0 average score. On RoboCasa with Gr00t-N1.5, FOCA further achieves 34.4 average success rate compared to 28.4 for FLARE. These results demonstrate the effectiveness and robustness of FOCA across different future-oriented baselines, policy architectures, and 

_Table 5._ Comparison of _π_ 0 fine-tuned with DreamVLA-style future conditioning, FLARE, and FOCA on LIBERO at 40% data scale. 

|**Method**|**10**|**Go.**|**Obj.**|**Spa.**|**Avg**|
|---|---|---|---|---|---|
|_π_0 Baseline|82|92.6|95.2|89.6|89.85|
|_π_0 + DreamVLA|84.8|93.2|96.4|94|92.1|
|_π_0 + FLARE|83.6|93|96.8|90.6|91|
|**FOCA**|**88**|**94.6**|**99.6**|**93.6**|**94**|


_Table 6._ Comparison of _π_ 0 fine-tuned with DreamVLA-style future conditioning and FOCA on LIBERO at 100% data scale. 

|**Method**|**10**|**Go.**|**Obj.**|**Spa.**|**Avg**|
|---|---|---|---|---|---|
|_π_0 Baseline|90|95.4|98.2|94.6|94.6|
|_π_0 + DreamVLA|90.8|96.4|98.8|96.2|95.6|
|**FOCA**|**92.4**|**97.4**|**99.8**|**97**|**96.6**|


robotic manipulation benchmarks. 

_Table 7._ Comparison of Gr00t-N1.5 fine-tuned with FLARE and FOCA on RoboCasa at 100 demos. 

|**Method**|**Pick-an**<br>**Cab**_→_**Counter**|**d-Place**<br>**Counter**_→_**Cab**|**Coffee**<br>**Setup**|**Off**<br>**Stove**|**On**<br>**MW**|**Avg**|
|---|---|---|---|---|---|---|
|Gr00t-N1.5 Baseline|28|40|12|14|36|26|
|Gr00t-N1.5 + FLARE|24|34|20|14|50|28.4|
|**Gr00t-N1.5 + FOCA**|**30**|**36**|**10**|**24**|**72**|**34.4**|


**Contribution of DreamGen on FOCA on table setup tasks using bimanual Aloha robot.** We ablate the effectiveness of DreamGen on FOCA when apply to realrobot (bimanual Aloha) on table set up tasks. Our models are trained with the _π_ 0 VLA architecture using either 40% (120 demonstrations) or 100% (300 demonstrations) of the dataset. As shown in Table 8, incorporating FOCA improves performance over _π_ 0, and combining FOCA with DreamGen yields the largest gains. 

_Table 8._ Comparison of task success rates on real-robot. 

||_π_0|FOCA (_π_0)|**FOCA + DreamGen**|
|---|---|---|---|
|40%|10%|20%|55%|
|100%|10%|45%|60%|


## **6. Conclusions** 

We show that few-shot VLA adaptation is limited by the learning signal extracted per demonstration. FOCA addresses this by combining explicit and implicit future supervision in the latent space to enable data-efficient, action-free adaptation of pretrained VLA models. Extensive experiments across simulation and real robots demonstrate consistent gains, robustness to imperfect synthetic rollouts, and competitive generalization across architectures and embodiments, positioning future-conditioned representation learning as a promising route toward scalable robotic adaptation. 

9 

**FOCA-VLA** 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of Data Efficiency in Robotics and Vision-Language-Action models. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

## **Acknowledgment** 

Duy M. H. Nguyen and M. Niepert acknowledge funding by Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) under Germany’s Excellence Strategy - EXC 2075 – 390740016 and the International Max Planck Research School for Intelligent Systems (IMPRS-IS). Tuan Anh Tran, Duy M. H. Nguyen, and Daniel Sonntag are also supported by the No-IDLE project (BMFTR, 16IW23002), the MASTER project (EU, 101093079), and the Endowed Chair of Applied Artificial Intelligence, Oldenburg University. 

## **References** 

- Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., et al. Cosmos world foundation model platform for physical ai. In _arXiv preprint arXiv:2501.03575_ , 2025a. 

- Agarwal, N. N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., Dworakowski, D., Fan, J., Fenzi, M., Ferroni, F., Fidler, S., Fox, D., Ge, S., Ge, Y., Gu, J., Gururani, S., He, E., Huang, J., Huffman, J. S., Jannaty, P., Jin, J., Kim, S. W., Kl’ar, G., Lam, G., Lan, S., Leal-Taixe, L., Li, A., Li, Z.,´ Lin, C.-H., Lin, T.-Y., Ling, H., Liu, M.-Y., Liu, X., Luo, A., Ma, Q., Mao, H., Mo, K., Mousavian, A., Nah, S., Niverty, S., Page, D., Paschalidou, D., Patel, Z., Pavao, L., Ramezanali, M., Reda, F. A., Ren, X.-S., Sabavat, V. R. N., Schmerling, E., Shi, S., Stefaniak, B., Tang, S., Tchapmi, L. P., Tredak, P., Tseng, W.-C., Varghese, J. R., Wang, H., Wang, H., Wang, H., Wang, T., Wei, F., Wei, X., Wu, J. Z., Xu, J., Yang, W., Yen-Chen, L., Zeng, X., Zeng, Y., Zhang, J., Zhang, Q., Zhang, Y., Zhao, Q., and Zolkowski, A. Cosmos world foundation model platform for physical ai. _ArXiv_ , abs/2501.03575, 2025b. URL https://api.semanticscholar. org/CorpusID:275342594. 

- Aldaco, J., Armstrong, T., Baruch, R., Bingham, J., Chan, S., Draper, K., Dwibedi, D., Finn, C., Florence, P., Goodrich, S., et al. Aloha 2: An enhanced low-cost hardware for bimanual teleoperation. _arXiv preprint arXiv:2405.02292_ , 2024. 

- Ali, A., Bai, J., Bala, M., Balaji, Y., Blakeman, A., Cai, T., et al. World simulation with video foundation models for physical ai. In _arXiv preprint arXiv:2511.00062_ , 2025. 

- Assran, M., Duval, Q., Misra, I., Bojanowski, P., Vincent, P., Rabbat, M., LeCun, Y., and Ballas, N. Self-supervised learning from images with a joint-embedding predictive architecture. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 15619– 15629, 2023. 

- Baker, B., Akkaya, I., Zhokov, P., Huizinga, J., Tang, J., Ecoffet, A., Houghton, B., Sampedro, R., and Clune, J. Video pretraining (vpt): Learning to act by watching unlabeled online videos. _Advances in Neural Information Processing Systems_ , 35:24639–24654, 2022. 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Chen, L. Y., Xu, C., Dharmarajan, K., Irshad, M. Z., Cheng, R., Keutzer, K., Tomizuka, M., Vuong, Q., and Goldberg, K. Rovi-aug: Robot and viewpoint augmentation for cross-embodiment robot learning. In _Conference on Robot Learning (CoRL)_ , 2024. 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. In _arXiv preprint arXiv:2303.04137_ , 2023. 

- Dayan, P. Improving generalization for temporal difference learning: The successor representation. _Neural computation_ , 5(4):613–624, 1993. 

- Duan, Y., Andrychowicz, M., Stadie, B., Jonathan Ho, O., Schneider, J., Sutskever, I., Abbeel, P., and Zaremba, W. One-shot imitation learning. _Advances in neural information processing systems_ , 30, 2017. 

- Eysenbach, B., Salakhutdinov, R., and Levine, S. C- learning: Learning to achieve goals via recursive classification. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2021. 

- Eysenbach, B., Zhang, T., Levine, S., and Salakhutdinov, R. R. Contrastive learning as goal-conditioned reinforcement learning. _Advances in Neural Information Processing Systems_ , 35:35603–35620, 2022. 

10 

**FOCA-VLA** 

- Goyal, A., Blukis, V., Xu, J., Guo, Y., Chao, Y.-W., and Fox, D. Rvt-2: Learning precise manipulation from few demonstrations. _arXiv preprint arXiv:2406.08545_ , 2024. 

- Gutmann, M. U. and Hyvarinen, A.¨ Noise-contrastive estimation of unnormalized statistical models, with applications to natural image statistics. _The journal of machine learning research_ , 13(1):307–361, 2012. 

- Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., and Chen, W. Lora: Low-rank adaptation of large language models. In _arXiv preprint arXiv:2106.09685_ , 2021. 

- Hu, Y., Guo, Y., Wang, P., Chen, X., Wang, Y.-J., Zhang, J., Sreenath, K., Lu, C., and Chen, J. Video prediction policy: A generalist robot policy with predictive visual representations. In _Proceedings of the Forty-Second International Conference on Machine Learning (ICML)_ , 2025. 

- Huang, C.-P., Wu, Y.-H., Chen, M.-H., Wang, Y.-C. F., and Yang, F.-E. Thinkact: Vision-language-action reasoning via reinforced visual latent planning. In _Advances in Neural Information Processing Systems_ , 2025. Accepted at Advances in Neural Information Processing Systems 2025. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0 _._ 5: a vision-language-action model with openworld generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Jang, J., Ye, S., Lin, Z., Xiang, J., Bjorck, J., Fang, Y., Hu, F., Huang, S., Kundalia, K., Lin, Y.-C., et al. Dreamgen: Unlocking generalization in robot learning through video world models. _arXiv preprint arXiv:2505.12705_ , 2025. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Lee, S.-W., Kang, X., Yang, B. Y., and Kuo, Y.-L. Class: Contrastive learning via action sequence supervision for robot manipulation. In _Conference on Robot Learning_ , pp. 4743–4766. PMLR, 2025. 

- Li, P., Wu, Y., Xi, Z., Li, W., Huang, Y., Zhang, Z., Chen, Y., Wang, J., Zhu, S.-C., Liu, T., and Huang, S. Controlvla: Few-shot object-centric adaptation for pretrained vision-language-action models. In _arXiv preprint arXiv:2506.16211_ , 2025. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Liu, H., Li, X., Li, P., Liu, M., Wang, D., Liu, J., Kang, B., Ma, X., Kong, T., and Zhang, H. Towards generalist robot policies: What matters in building vision-language-action models. 2025. 

- Liu, S., Zeng, Z., Ren, T., Li, F., Zhang, H., Yang, J., Jiang, Q., Li, C., Yang, J., Su, H., et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. In _European conference on computer vision_ , pp. 38–55. Springer, 2024a. 

- Liu, S.-Y., Wang, C.-Y., Yin, H., Molchanov, P., Wang, Y.-C. F., Cheng, K.-T., and Chen, M.-H. Dora: Weightdecomposed low-rank adaptation. In _International Conference on Machine Learning (ICML)_ , 2024b. 

- Ma, T., Zhou, J., Wang, Z., Qiu, R., and Liang, J. Contrastive imitation learning for language-guided multi-task robotic manipulation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2024. 

- Mitra, C., Luo, Y., Saravanan, R., Niu, D., Pai, A., Thomason, J., Darrell, T., Anwar, A., Ramanan, D., and Herzig, R. Mechanistic finetuning of vision-language-action models via few-shot demonstrations. _arXiv preprint arXiv:2511.22697_ , 2025. 

- Nasiriany, S., Maddukuri, A., Zhang, L., Parikh, A., Lo, A., Joshi, A., Mandlekar, A., and Zhu, Y. Robocasa: Largescale simulation of everyday tasks for generalist robots. In _Proceedings of Robotics: Science and Systems_ , 2024. 

- Oord, A. v. d., Li, Y., and Vinyals, O. Representation learning with contrastive predictive coding. _arXiv preprint arXiv:1807.03748_ , 2018. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- Qu, D., Song, H., Chen, Q., Chen, Z., Gao, X., Ye, X., Lv, Q., Shi, M., Ren, G., Ruan, C., et al. Eo-1: Interleaved vision-text-action pretraining for general robot control. _arXiv preprint arXiv:2508.21112_ , 2025a. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025b. 

- Rana, K., Melnik, A., and Sunderhauf,¨ N. Contrastive language, action, and state pre-training for robot learning. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- Schaul, T., Horgan, D., Gregor, K., and Silver, D. Universal value function approximators. In _International conference on machine learning_ , pp. 1312–1320. PMLR, 2015. 

11 

**FOCA-VLA** 

- Seo, Y., Kim, J., James, S., Lee, K., Shin, J., and Abbeel, P. Multi-view masked world models for visual robotic manipulation. In _International Conference on Machine Learning_ , pp. 30613–30632. PMLR, 2023a. 

- Seo, Y., Kim, J., James, S., Lee, K., Shin, J., and Abbeel, P. Multi-view masked world models for visual robotic manipulation. In _International Conference on Machine Learning (ICML)_ , 2023b. 

- Sermanet, P., Lynch, C., Chebotar, Y., Hsu, J., Jang, E., Schaal, S., Levine, S., and Brain, G. Time-contrastive networks: Self-supervised learning from video. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pp. 1134–1141. IEEE, 2018. 

- Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., Aractingi, M., Pascal, C., Russi, M., Marafioti, A., et al. Smolvla: A vision-languageaction model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- Sridhar, K., Dutta, S., Jayaraman, D., and Lee, I. Ricl: Adding in-context adaptability to pre-trained vision-language-action models. In _arXiv preprint arXiv:2508.02062_ , 2025. 

- Team, G. R., Abdolmaleki, A., Abeyruwan, S., Ainslie, J., Alayrac, J.-B., Arenas, M. G., Balakrishna, A., Batchelor, N., Bewley, A., Bingham, J., et al. Gemini robotics 1.5: Pushing the frontier of generalist robots with advanced embodied reasoning, thinking, and motion transfer. _arXiv preprint arXiv:2510.03342_ , 2025a. 

- Team, G. R., Abeyruwan, S., Ainslie, J., Alayrac, J.-B., Arenas, M. G., Armstrong, T., Balakrishna, A., Baruch, R., Bauza, M., Blokzijl, M., et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025b. 

- Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Todorov, E., Erez, T., and Tassa, Y. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pp. 5026–5033. IEEE, 2012. 

- Watkins, C. J. and Dayan, P. Q-learning. _Machine learning_ , 8(3):279–292, 1992. 

- Yang, Q. A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Li, C., Liu, D., Huang, F., Dong, G., Wei, H., Lin, H., Yang, J., Tu, J., Zhang, J., Yang, J., Yang, J., Zhou, J., Lin, J., Dang, K., Lu, K., Bao, K., Yang, K., Yu, L., Li, M., Xue, M., Zhang, P., 

Zhu, Q., Men, R., Lin, R., Li, T., Xia, T., Ren, X., Ren, X., Fan, Y., Su, Y., Zhang, Y.-C., Wan, Y., Liu, Y., Cui, Z., Zhang, Z., Qiu, Z., Quan, S., and Wang, Z. Qwen2.5 technical report. _ArXiv_ , abs/2412.15115, 2024. URL https://api.semanticscholar. org/CorpusID:274859421. 

- Ye, S., Jang, J., Jeon, B., Joo, S., Yang, J., Peng, B., Mandlekar, A., Tan, R., Chao, Y.-W., Lin, B. Y., et al. Latent action pretraining from videos. In _Proceedings of the Thirteenth International Conference on Learning Representations (ICLR)_ , 2025. 

- Zhai, X., Mustafa, B., Kolesnikov, A., and Beyer, L. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 11975–11986, 2023. 

- Zhang, L., Rao, A., and Agrawala, M. Adding conditional control to text-to-image diffusion models. In _arXiv preprint arXiv:2302.05543_ , 2023. 

- Zhang, W., Liu, H., Qi, Z., Wang, Y., Yu, X., Zhang, J., Dong, R., He, J., Lu, F., Wang, H., et al. Dreamvla: A vision-language-action model dreamed with comprehensive world knowledge. In _Advances in Neural Information Processing Systems_ , 2025. Accepted at NeurIPS 2025. 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025. 

- Zhao, T., Kumar, V., Levine, S., and Finn, C. Learning finegrained bimanual manipulation with low-cost hardware. In _Robotics: Science and Systems (RSS)_ , 2023. 

- Zheng, C., Eysenbach, B., Walke, H., Yin, P., Fang, K., Salakhutdinov, R., and Levine, S. Stabilizing contrastive rl: Techniques for robotic goal reaching from offline data. _arXiv preprint arXiv:2306.03346_ , 2023. 

- Zheng, R., Liang, Y., Huang, S., Gao, J., Daume´ III, H., Kolobov, A., Huang, F., and Yang, J. Tracevla: Visual trace prompting enhances spatial–temporal awareness for generalist robotic policies. In _Proceedings of the Thirteenth International Conference on Learning Representations (ICLR)_ , 2025a. 

- Zheng, R., Wang, J., Reed, S., Bjorck, J., Fang, Y., Hu, F., Jang, J., Kundalia, K., Lin, Z., Magne, L., et al. Flare: Robot learning with implicit world modeling. _arXiv preprint arXiv:2505.15659_ , 2025b. 

- Ziebart, B. D., Maas, A. L., Bagnell, J. A., Dey, A. K., et al. Maximum entropy inverse reinforcement learning. In _Aaai_ , volume 8, pp. 1433–1438. Chicago, IL, USA, 2008. 

12 

**FOCA-VLA** 

- Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., 

- Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

13 

**FOCA-VLA** 

# SUPPLEMENTARY MATERIAL FOR 

“FOCA: FUTURE-ORIENTED CONDITIONING FOR DATA-EFFICIENT VISION-LANGUAGE-ACTION ADAPTATION” 

## **Contents** 

|**A Lim**|**itations and Future Works**|**15**|
|---|---|---|
|**B Add**|**itional Related Works.**|**15**|
|**C Visu**|**alizations**|**16**|
|C.1|Rollout Visualizations on Simulated and Real-World Robots<br>. . . . . . . . . . . . . . . . .|. . . . . . .<br>16|
|C.2|Failure correction via future conditioning<br>. . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>16|
|C.3|DreamGen hallucination analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>17|
|**D Imp**|**lementation Details**|**17**|
|D.1|Architecture designs<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>17|
|D.2|Task-Grounded Object-Centric Representation Generation across Timesteps . . . . . . . . .|. . . . . . .<br>17|
|D.3|Computational Resources . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>20|
|D.4|DreamGen Configurations<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>20|
|**E**<br>**Sim**|**ulation Environment and Real-Robot Tasks**|**22**|
|E.1|Libero Simulation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>22|
|E.2|Robocasa Simulation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>23|
|E.3|ALOHA Tasks<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>25|
|E.4|UR5 Tasks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>25|
|E.5|Place Part . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>26|
|**F**<br>**The**|**oretical Investigation**|**28**|
|F.1|Problem setting and notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>28|
|F.2|Discounted future occupancy and Bellman recursions . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>28|
|F.3|Implicit alignment as density-ratio estimation (InfoNCE_⇒_occupancy/value) . . . . . . . .|. . . . . . .<br>29|
|F.4|Multi-frame futures and_n_-step structure . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>31|
|F.5|Explicit object-centric prediction as restricted world modeling<br>. . . . . . . . . . . . . . . .|. . . . . . .<br>31|
|F.6|Hybrid objective and object-centric factorization . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>31|
|F.7|DreamGen (video-only) augmentation . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>32|
|F.8|Universal evaluation and multi-positive futures<br>. . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . .<br>33|


14 

**FOCA-VLA** 

## **A. Limitations and Future Works** 

**Limitations.** While FOCA improves few-shot adaptation by injecting future-oriented supervision, it does not explicitly model long-term symbolic reasoning or task decomposition. In complex, multi-stage tasks that require remembering completed subtasks and planning several steps ahead (e.g., scenarios with multiple similar objects such as bartender-style setups), the lack of an explicit memory or chain-of-thought mechanism can lead to ambiguity or confusion. FOCA captures long-horizon structure implicitly in representation space, but it does not generate intermediate reasoning traces or maintain a persistent task state, which may limit performance on tasks requiring explicit temporal abstraction and bookkeeping. 

**Future work.** An important direction is to extend FOCA with explicit reasoning and memory components, such as lightweight task-state memories or structured chain-of-thought generation, to better handle long-horizon, compositional tasks. Another promising avenue is to investigate FOCA’s applicability to autoregressive VLA architectures, including EO-1 and CoT-VLA, where future-oriented conditioning could be integrated at the token-generation level rather than within diffusion policies. More broadly, combining FOCA with structured reasoning, memory, and autoregressive control may offer a unified framework that bridges representation-level future conditioning with explicit planning and decision-making. 

## **B. Additional Related Works.** 

**Synthetic Data and Viewpoint Augmentation.** A complementary line of work improves data efficiency by augmenting demonstrations with additional observations, including synthesizing trajectories under novel robot embodiments or camera viewpoints to improve robustness and transfer (e.g., RoVi-Aug (Chen et al., 2024)). Relatedly, multi-view representation learning exploits auxiliary viewpoints during training to improve downstream control without requiring camera calibration at deployment (Seo et al., 2023b). More broadly, video and world models can generate plausible future rollouts that serve as auxiliary supervision or evaluation scaffolding, including robotics-oriented generators such as DreamGen (Jang et al., 2025) and large-scale world-model platforms such as Cosmos (Agarwal et al., 2025a; Ali et al., 2025). FOCA is compatible with these approaches but is motivated by a distinct observation: synthetic videos can provide useful future supervision even when action labels are unavailable. 

Rather than introducing a new VLA backbone or pretraining recipe, FOCA operates as a fine-tuning–time adaptation mechanism that can be layered on top of existing VLA models and adaptation strategies, including parameter-efficient updates and object-centric conditioning (Hu et al., 2021; Liu et al., 2024b; Li et al., 2025; Sridhar et al., 2025). By injecting future-oriented objectives in latent space over task-grounded interaction tokens, FOCA introduces long-horizon structure while remaining lightweight and effective in few-shot regimes. Crucially, its implicit future alignment naturally extends to action-free videos generated by world models, enabling the use of synthetic rollouts without inverse dynamics or pseudo-action labeling (Agarwal et al., 2025a). Overall, FOCA bridges large-scale VLA pretraining and data-efficient downstream adaptation in a principled and modular manner. 

**Future Prediction in VLA models** Recent VLA models incorporate auxiliary prediction objectives to improve spatial reasoning, including chain-of-thought prediction, trajectory generation, visual question answering, and future state forecasting (Zheng et al., 2025a; Qu et al., 2025a; Team et al., 2025a). Among these directions, pixel-level future frame prediction has emerged as a particularly appealing form of self-supervision (Seo et al., 2023a; Zhao et al., 2025), but dense image reconstruction is often redundant and difficult to optimize, especially in low-data regimes. In contrast, FOCA predicts future information directly in latent embedding space and restricts supervision to task-grounded dynamic regions capturing gripper–object interactions, which can be efficiently identified using off-the-shelf visual grounding models (e.g., DINO (Liu et al., 2024a)), thereby avoiding full-scene reconstruction while preserving the control-relevant inductive bias needed for effective robot adaptation. 

**Contrastive Learning in Robotic Manipulation** Contrastive learning has been widely used to improve transfer and generalization in robotic learning, including time-contrastive objectives across multi-view observations (Sermanet et al., 2018), multimodal alignment between vision, language, and actions (Rana et al., 2023; Ma et al., 2024), and trajectory-level contrastive losses in latent diffusion spaces (Lee et al., 2025). However, these methods are largely developed for CLIP-based models or relatively small policies such as ACT and Diffusion Policy (Chi et al., 2023). Directly applying them to large pretrained VLA models is challenging due to model scale and the domain gap between pretraining and downstream control. To address this, FOCA introduces a small set of representative tokens that summarize vision–language information via attention within the VLM and serve as a compact interface for contrastive future alignment. The most closely related work is 

15 

**FOCA-VLA** 

FLARE (Zheng et al., 2025b), which integrates future alignment during large-scale _diffusion_ pretraining; in contrast, FOCA applies future-oriented objectives directly _within the VLM modules_ during downstream adaptation. Furthermore, we show that FOCA further improves GR00T-N1.5 (Bjorck et al., 2025) performance, whose diffusion policy is already pretrained with FLARE, demonstrating that FOCA provides additional gains beyond diffusion-level pretraining alone. 

## **C. Visualizations** 

This section provides qualitative visualizations to complement the quantitative results presented in the paper. We include representative examples from both simulated and real-world environments to illustrate task diversity, long-horizon structure, and failure modes addressed by FOCA. 

### **C.1. Rollout Visualizations on Simulated and Real-World Robots** 

Figures 4 and 5 show example task executions from the LIBERO and RoboCasa benchmarks, respectively. These environments span a wide range of manipulation challenges, including object placement, spatial reasoning, and multi-step goal completion under varying initial conditions. Figures 6 and 7 present example rollouts collected on two real-world robotic platforms: the bimanual ALOHA robot and a simulated humanoid robot. These figures illustrate the visual complexity and embodiment-specific challenges present in real-world settings, including partial observability, viewpoint variation, and contact-rich manipulation. 


_Figure 4._ **Example rollouts from LIBERO simulation.** 

### **C.2. Failure correction via future conditioning** 

To better understand the behavioral differences induced by future-oriented conditioning, we visualize continuous frame sequences for representative failure cases (Figure. 8). In particular, we compare baseline VLA policies that fail to complete the task with FOCA-enhanced policies that successfully recover and reach the goal under the same initial conditions. These examples qualitatively demonstrate that FOCA improves long-horizon consistency and prevents early commitment to suboptimal interaction trajectories, consistent with its future-conditioned design. 

16 

**FOCA-VLA** 


_Figure 5._ **Example rollouts from ROBOCASA simulation.** 

### **C.3. DreamGen hallucination analysis** 

Figure 9 illustrates sequences generated by the DreamGen video world model under different training regimes. When trained with limited demonstrations (40%), the generated videos exhibit hallucinations. In contrast, DreamGen trained with a larger few-shot imitation ratio (100%) produces more coherent and physically plausible future trajectories. 

## **D. Implementation Details** 

### **D.1. Architecture designs** 

We evaluate our proposed method, **FOCA** (explicit module is demonstrated in Figure 11), on two public simulation datasets - _LIBERO_ and _RoboCasa_ - as well as two distinct robotic platforms - bimanual ALOHA ROBOT and simulated HUMANOID PLATFORM, version VR-H3 designed by VinRobotics, using Inspire’s 6-DOF hands. We apply FOCA to _π_ 0 on both public datasets and ALOHA ROBOT tasks. For GR00T-N1.5, FOCA is evaluated on RoboCasa and the simulated HUMANOID PLATFORM. For the _π_ 0 architecture, the batch size is set to 18 for LIBERO and 12 for RoboCasa. The learning rate and maximum number of training steps are fixed to 1 _×_ 10<sup>_−_4</sup> and 100k steps, respectively, for both datasets. For the GR00T-N1.5 architecture on RoboCasa, the batch size, learning rate, and maximum number of training steps are set to 32, 1 _×_ 10<sup>_−_4</sup> , and 60k steps, respectively. Note that both the baseline methods and our proposed FOCA use identical hyperparameter settings to ensure a fair comparison. The training process can be early-stopped once the loss curve has sufficiently converged. 

For the decoder in the explicit module, we employ two Transformer blocks with 16 attention heads, followed by a linear layer that projects the outputs into the visual _local_ feature space. We set the query length to 4 for each observation and use a shared decoder across all observations, with the explicit loss weighted by 0.1. For the implicit module, we use a single linear layer to project the implicit tokens produced by the VLM into the visual _global_ feature space. The number of parameters for each model before and after applying FOCA is reported in Table 9. 

### **D.2. Task-Grounded Object-Centric Representation Generation across Timesteps** 

To construct the the _Object-of-interest regions_ used in our experiments, we derive spatial supervision differently for simulation datsets and realworld data. 

For the simulation environments include LIBERO and RoboCasa, we extract segmentation masks from simulator. From 

17 

**FOCA-VLA** 


_Figure 6._ **Example rollouts from ALOHA real-world robot.** 

18 

**FOCA-VLA** 

##### **placing part into a rack** 


_Figure 7._ **Example episodes from Place Part performed by VinRobotics’ simulated VR-H3 humanoid on Mujoco.** 


_Figure 8._ **Example rollouts where the baseline** _π_ 0 **policy fails (top) and FOCA succeeds (bottom).** 

_Table 9._ The number of parameters that FOCA integrates into _π_ 0 and Gr00tN1.5. 

|Method|Total Parameters|Trainable Parameters|
|---|---|---|
|Pi0|3.5B|3.1B|
|Pi0 + FOCA|3.6B|3.2B|
|GR00T-N1.5|2.4B|1.1B|
|GR00T-N1.5 + FOCA|2.5B|1.2B|


this ground-truth masks combining with task descriptions, we isolate the pixels corresponding to all objects referenced in the task description and gripper then compute the bounding box that tightly encloses every object of interest as shown in Figure 12. By applying this pipeline across all timesteps, we successfully prepare consistent task-grounded spatial region over entire trajectory. 

In contrast, for real-world experiments where ground-truth masks are unavailable, we use **Grounding-DINO** (Liu et al., 2024a) to detect all objects specified by the task instruction. The model provides bounding boxes for each queried object class, and we aggregate these detections to output the final object-of-interest areas used at each time steps. This process allows the same task-grounded methodology used in simulation to transfer effectively to real-world settings as shown in Figure 13. Note that these object-of-interest regions are only utilized during training to supervise the Explicit Future Latent Prediction and Implicit Future Alignment modules, and are not required during inference. 

19 

**FOCA-VLA** 

#### **a, Typical hallucinated cases by DreamGen trained with 40% data** 


#### **b, Typical success cases by DreamGen trained with 100% data** 


_Figure 9._ **Synthetic rollouts generated by DreamGen at different data scales.** (a) Hallucinated cases with 40% training data; (b) successful cases with 100% training data. 

_Table 10._ Our computational overhead when integrating VWM. Importantly, our training structure is consistent with prior pipelines that incorporate video world models. FOCA replaces the pseudo-action generation stage with action-free supervision, rather than introducing an extra stage. 

|**Training Stages**|**Training Hours**|
|---|---|
|(i) Finetune DreamGen|_∼_28 hours with 8 H100 (65k steps). This step has a similar cost to the<br>DreamGen paper.|
|(ii) Action-free supervision with FOCA (phase 1)|_∼_15 hours with 4 A100. DreamGen does not include this step, but<br>extracting pseudo-action from generated videos in (i) takes_∼_8 hours.|
|(iii) FOCA fine-tuning with explicit and implicit tokens<br>(phase 2)|_∼_18 hours with 4 A100. This cost is comparable to other baselines.|


### **D.3. Computational Resources** 

For the _π_ 0 architecture, all experimental settings are trained on four NVIDIA H100 GPUs, while all settings for GR00T-N1.5 are trained on a single NVIDIA H100 GPU. For _π_ 0, the total training time for the baseline and FOCA on LIBERO is around 18 and 21 hours, respectively, and 20 hours and 23 hours for 100k steps on RoboCasa. For GR00T-N1.5 on RoboCasa, the total training time for the baseline and FOCA is 11 hours and 13 hours for 60k steps, respectively. For detail computational overhead when integrating Video World Model DreamGen, see in Table 10. 

### **D.4. DreamGen Configurations** 

In this section, we provide a comprehensive overview of our implementation of the **DreamGen** (Jang et al., 2025) pipeline. This framework is utilized for co-training with synthetic rollouts, video generation, and pseudo-action labeling. 

D.4.1. THE FOUR-STAGE WORKFLOW: FROM DATA PREPARATION TO INFERENCE 

Our workflow is organized into four distinct stages: 

- **Step 1: Structured Video Annotation:** Given an original video, we utilize the Qwen 2.5 32B Vision-Language Model (VLM) (Yang et al., 2024) to generate a hierarchical semantic decomposition of the scene. Rather than a simple 

20 

**FOCA-VLA** 


_Figure 10._ FOCA’s generalizations performance across Pi-Zero and Groot N1.5 on Robocasa, with 30 demos (top) and 100 demos (bottom) on most 5 challenge tasks 

caption, the model produces a structured analysis divided into distinct categories: Setting, Robotic Agent, Task Objectives, Action Sequence, and Environmental Interaction. This structured output acts as a high-fidelity semantic bridge, explicitly isolating the visual features of the robot’s morphology and the temporal dynamics of the manipulation task. The standardized system prompt used to enforce this output structure is provided in Figure 14. 

- **Step 2: World Model Post-Training (Cosmos-Predict 2.0):** We perform domain-specific post-training on the _NVIDIA_ _~~C~~ osmos-Predict2-2B-Video2World_ model (Agarwal et al., 2025b). We utilize LIBERO dataset; detailed statistics regarding our data splits are shown in Table 11. The model is trained to predict future video frames conditioned on context frames and a text description. The specific training hyperparameters are detailed in Table 12. 

- **Step 3: Large-Scale Inference (Synthesis):** Utilizing the fine-tuned checkpoints, we generate synthetic videos with a duration of 17 seconds. The generation is conditioned on an initial screenshot frame from the original video and the corresponding text description generated by the VLM in Step 1. 

- **Step 4: Pseudo-Action Labeling (IDM):** To extract pseudo-action labels for the generated videos, we train an **Inverse Dynamics Model (IDM)** . The IDM is conditioned on two image frames (start and end) and is trained to predict the action chunks occurring between them using a flow-matching loss objective, as described in the original DreamGen pipeline (Jang et al., 2025). Once trained, the IDM processes the synthetic videos from Step 3 to generate predicted actions (pseudo-actions) for every frame transition. 

We adhere to the IDM configuration specified in the DreamGen framework. The model consists of a **SigLIP-2 Vision Encoder** that processes the start and end frames, and an **Action Encoder** that embeds the temporal action sequence. These features are processed by a **Diffusion Transformer** to model the joint distribution. An **Action Decoder** then recovers the final action sequence. We incorporate a feedback loop _k_ between the Action Decoder and Action Encoder to iteratively refine the consistency of the generated pseudo-actions. 

### D.4.2. STAGE 1: VLM PROMPT ENGINEERING 

The fidelity of the synthetic video is highly dependent on the quality of the conditioning text. Figure 14 details the standardized prompt used to extract structured metadata from the original dataset. 

21 

**FOCA-VLA** 


_Figure 11._ Architecture overview of the explicit alignment setting. 

_Table 11._ Libero Training Data Splits for DreamGen Implementation. 

|**Dataset**|**Length (Frames)**|**Duration (hr)**|**FPS**|**Category**|
|---|---|---|---|---|
|Libero (10% Tasks)|33,587|0.46|20|Simulation|
|Libero (40% Tasks)|133,851|1.86|20|Simulation|
|Libero (100% Tasks)|269,918|3.75|20|Simulation|


## **E. Simulation Environment and Real-Robot Tasks** 

In this section, we describe in detail the tasks and datasets used in our experiments, as well as the procedure for generating object-centric bounding boxes for FOCA training. Note that object-centric boxes are generated and used only during training and are not required at inference time. 

### **E.1. Libero Simulation** 

**LIBERO** (Liu et al., 2023) dataset consists of 4 subsets: LIBERO-10, LIBERO-Object, LIBERO-Goal, LIBERO-Spatial designed to evaluate different aspects of generalization. Each subset contains 10 tasks, and each task provides 50 demostrations episodes, totaling 500 episodes per subset and 2000 episodes in original dataset. Each episode includes observations from two camera viewpoints: a fixed static agentview ~~c~~ amera and an onboard gripper eye ~~i~~ n ~~h~~ and ~~c~~ amera, as illustrated in Figure 15. 

To obtain segmentation masks to build Task-grounded Object-centric areas, we re-render the entire dataset using simulator. 

_Table 12._ Hyperparameters and Model Configurations for DreamGen Implementation. 

|**Parameter**|**Value**|
|---|---|
|Base World Model|Cosmos-Predict2-2B-Video2World|
|Resolution|1280_×_720(720p)|
|Post-Training LR|1_×_10<sup>_−_4</sup>|
|LoRA Config|Rank 4, Alpha 4|
|RoboCasa and Libero Training|100 Epochs, Batch Size 32|


22 

**FOCA-VLA** 

**Task: pick the mug from the counter and place it under the coffee machine dispenser** 


_Figure 12._ **Region of interest in RoboCasa** 


_Figure 13._ **Region of interest in real-world settings** 

For each episode, we reset the enviroment to its saved initial state and replay each action from the demotration labels. During re-rendering, we record observations that now include segmentation masks, which are not provided in the original datasets. Moreover, to ensure the constructed dataset maintains high quality, we perform additional filtering to remove no-op actions, since the produce no change in the robot state as well as discard unsuccessful demostrations, which could introduce inconsistent or misleading supervision. After this process, the final dataset reduces from 2000 episodes to 1676 valid demostrations. For experiments with different scale datasets, we construct 10% and 40% subsets by random sampling 5 episodes and 20 episodes per tasks for each subset respectively. After training, we evaluate models using 50 trials per task, and the results are summarized in Figure 2. 

### **E.2. Robocasa Simulation** 

**RoboCasa Kitchen** (Nasiriany et al., 2024) is a large-scale simulation benchmark designed to model everyday manipulation tasks with different kitchen environments. It includes 24 tasks, each providing appriximately 3000 demostrations, along with numerous predefined subsets. Each demonstration provides three synchronized visual viewpoints from 3 different cameras include: agentview ~~l~~ eft ~~c~~ amera, agentview ~~r~~ ight ~~c~~ amera, eye ~~i~~ n ~~h~~ and ~~c~~ amera as shown in Figure 15. In our experiments, we adopt the 30-demos and 100-demos configuration. Besides, the tasks in RoboCasa can be categorize into different types which are pick-and-place, turn on/off, open/close, and others. From the full set of 24 tasks, we select 5 representative tasks for our experiments include PnPCabToCounter, PnPCounterToCab, CoffeeSetupMug, TurnOffStove, TurnOnMicrowave. These tasks cover a range of obkect interaction and scene configurations, making them suitable for evaluating task-grounded object-centric modeling. 

To contruct the consistent object of interest regions accross all timesteps for selected RoboCasa demostrations, we apply the same re-rendering and segmentation-mask extraction process used for LIBERO mentioned above. We perform 50 evaluation trials for each selected task and report the outcomes in Figure 3c. 

23 

**FOCA-VLA** 

### System Prompt for Structured Video Annotation 

### **System Instruction:** 

You are an expert in robotic manipulation analysis. Watch the video and generate a structured description. Strictly follow this output format: 

### **1. Setting:** 

   - Describe the environment type (e.g., kitchen, lab). 

   - List key features (furniture, lighting, surfaces). 

**2. Robotic Arm:** 

   - Describe the robot’s appearance (color, joints) and design style. 

   - Note its position relative to target objects/containers. 

### **3. Task:** 

   - Define the specific operation (e.g., reaching, retrieving). 

   - Identify the target object and its location. 

**4. Action Sequence:** 

   - Detail the maneuvering of joints and end-effector interaction. 

   - Describe the smoothness and precision of the movement. 

**5. Environment Interaction:** 

   - Analyze how the robot navigates constraints (e.g., open doors, confined spaces). 

**6. Focus on Details:** 

   - Emphasize fine motor control and specific design elements. 

### **7. Purpose:** 

- Summarize the broader capability demonstrated (e.g., home automation). 

### **Assistant’s Generated Output (Example Segment):** 

**1. Setting:** The video is set in a kitchen environment... 

**2. Robotic Arm:** The robotic arm is white with black joints... 

**3. Task:** The arm extends its joints to reach inside the cabinet... ... 

_Figure 14._ Standardized prompt template for Stage 1: The VLM is instructed to decompose the video into a 7-point structured attribute analysis. 

24 

**FOCA-VLA** 


_(a)_ LIBERO camera views 


_(b)_ RoboCasa camera views 

_Figure 15._ **Camera views in LIBERO and RoboCasa** 

### **E.3. ALOHA Tasks** 

We evaluate our method on three real-robot manipulation tasks using the Mobile ALOHA platform. All tasks require bimanual manipulation and multi-view visual observations. The experiments are executed on a single workstation equipped with an NVIDIA RTX 5090 GPU. Task definitions, initialization, and the number of demonstrations are described below. 

**Open Bag.** The robot holds the bag with its left arm and grasps the zipper keychain with its right arm. The task is completed successfully when the bag is fully opened. The bag is initialized near the center of the table with a uniformly random planar position offset of 0 to 5 cm and a random in-plane rotation of 0 to 10°. Each demonstration consists of 240 control steps (16 seconds). We collect 100 demonstrations. 

**Tie Shoelaces.** The robot grasps the two shoelaces with both arms, forms a loop, and tightens the knot by pulling the laces in opposite directions. The task is completed when the knot is tightened. The shoe is initialized near the center of the workspace with a uniformly random planar position offset of 0 to 5 cm and a random in-plane rotation of 0 to 10°. Each demonstration consists of 300 control steps (20 seconds). We collect 300 demonstrations. 

**Set Table.** The robot places chopsticks onto the table mat using the right arm, places a plate at the center of the mat using the left arm, and places a bowl at the center of the plate using the right arm. The table mat is initialized with a uniformly random horizontal offset of 0 to 5 cm. The chopsticks and bowl are initialized randomly on the left-arm side of the workspace, and the plate is initialized randomly on the right-arm side, subject to reachability constraints. Each demonstration consists of 600 control steps (40 seconds). We collect 300 demonstrations. 

### **E.4. UR5 Tasks** 

We further evaluate our method on an additional robotic embodiment, the UR5. We employ two different variations UR5 arms, one UR5e equipped with a Robotiq Hand-E gripper, and one UR5 is equipped with a OnRobot-RG2 gripper. Two camera views are provided: one mounted on the table and the other on the robot wrist. On this real-robot platform, we design three handcrafted tabletop tasks, as illustrated in Figure 16 and Figure 17. 

**Dispense Napkin** : The robot dispenses a napkin from a container. The napkin box is uniformly distributed between these environments, where the napkin box is moved around within an area of 50x30 cm and rotated between 0-90 degrees. The task is considered successful if the napkin is fully dispensed. The trajectories for this task are on average about 95 frames long, we evaluate each trial with a maximum limit of 60 seconds: if the task has not been completed by then, the episode is counted as a failure. 

**Handle Bulk Material** : The robot picks up a bowl containing bulk material and pours the material into a designated target container. 

**Short Chemistry Test Tube** : The robot picks up the chemistry test tube with the prompted content color and place into a designated target. 

For each task, we collect 100 demonstrations for training (correspond to 100% training data regimes). The experiments are executed on a single workstation equipped with an NVIDIA RTX 5090 GPU. 

**Results** Figure 18 highlights the effectiveness of FOCA in real-world robotic manipulation tasks on the UR5 platform. Across all three evaluated tasks, FOCA consistently outperforms the baseline VLA model under both partial-data (40%) and full-data (100%) training settings. The improvement is especially noticeable in the more challenging manipulation scenarios: 

25 

**FOCA-VLA** 


_Figure 16._ The three handcrafted tabletop tasks with UR5. 


_Figure 17._ Example of FOCA rollout episode from UR5. 

- Handle bulk material (UR5): FOCA achieves the largest gain, improving success rates from 30% _→_ 50% under full-data training, while the baseline completely fails under the 40% setting (0%). This suggests that FOCA learns more robust action representations and generalizes better to complex contact-rich interactions. 

- Dispense napkin (UR5e): FOCA improves performance from 20% → 45% using 100% data and from 10% _→_ 25% with only 40% data. The consistent gap indicates stronger policy reliability even when training data is limited. 

- Short chemistry test tube (UR5): FOCA again surpasses the baseline in both settings, reaching 25% success compared to 15% for Base-VLA under full-data training. Although the absolute scores are lower due to the precision required in this task, FOCA still demonstrates better fine-grained manipulation capability. 

All in all, these results show two key strengths of FOCA: (1) higher task success rates across diverse real-world manipulation tasks; and (2) better data efficiency, since FOCA maintains clear advantages even when trained with only 40% of the dataset. This indicates that FOCA improves both the robustness and generalization ability of the manipulation policy, particularly in difficult real-world settings where perception noise, contact dynamics, and limited training data are major challenges. 

### **E.5. Place Part** 

We implement this task in MuJoCo (Todorov et al., 2012) using a humanoid robot. Figure 19a illustrates our multi-view camera setup, providing observations to the policy. This task evaluates the robot’s ability to perceive, align, and insert parts under tight constraints. We record synchronized observations from three RGB cameras that provide complementary viewpoints, using a teleoperation method in simulation. 

Robot proprioception is represented by a 26-dimensional joint-state vector, comprising: 

26 

**FOCA-VLA** 


_Figure 18._ Real-world results of the three manipulation tasks on UR5 


_Figure 19._ **Place Part in MuJoCo: camera views, key execution stages, and virtual views** . (a) Left, front, and right camera views. (b) Task stages: Start, Align, and Place. (c) Bottom-up virtual views. Green annotations illustrate the strict spatial alignment constraints of the task, requiring the two holes on either side of the part to be precisely aligned with and seated onto the two small pins on either side of the jig. 

- 1 left_shoulder_pitch_joint 14 right_wrist_pitch_joint 2 left_shoulder_roll_joint 15 L_thumb_swing_joint 3 left_shoulder_yaw_joint 16 L_thumb_1_joint 

- 4 left_elbow_pitch_joint 

- 5 left_wrist_yaw_joint 6 left_wrist_roll_joint 

- 7 left_wrist_pitch_joint 8 right_shoulder_pitch_joint 9 right_shoulder_roll_joint 

- 10 right_shoulder_yaw_joint 

- 11 right_elbow_pitch_joint 

- 12 right_wrist_yaw_joint 

- 13 right_wrist_roll_joint 

- 17 L_index_1_joint 

- 18 L_middle_1_joint 

- 19 L_ring_1_joint 

- 20 L_pinky_1_joint 

- 21 R_thumb_swing_joint 

- 22 R_thumb_1_joint 

- 23 R_index_1_joint 

- 24 R_middle_1_joint 

- 25 R_ring_1_joint 

- 26 R_pinky_1_joint 

Figure 19b illustrates the key stages of a successful sequence. At first, the robot is initialized in a raised, overhead grasping pose while holding the target part. The model is then started to control the robot to adjust the part’s position and orientation relative to the jig. Successful completion is achieved when the part is placed and stably seated in the jig, with the two holes 

27 

**FOCA-VLA** 

on either side of the part precisely aligned with and seated onto the two small pins on either side of the jig. 

Additionally, we use a render in RVT-2 (Goyal et al., 2024) to generate two virtual views (Figure 19c) in order to reduce occlusions and provide more information. Specifically, we reconstruct point clouds from RGB-D images and the camera intrinsics, and transform them into a shared world coordinate frame using the camera extrinsics. Virtual RGB-D images are then rendered by projecting these points onto two 2D image planes. 

## **F. Theoretical Investigation** 

### **F.1. Problem setting and notation** 

We model the environment as a discounted MDP _M_ = ( _S, A, P, γ_ ) with _γ ∈_ (0 _,_ 1). A _state s ∈S_ represents the VLA input at a time step (e.g., image observation, robot state, and instruction), and _a ∈A_ is an action. We are given an offline dataset of expert trajectories _D_ = _{τ }_ , where _τ_ = ( _s_ 0 _, a_ 0 _, s_ 1 _, a_ 1 _, . . . , sT_ ) is generated by a behavior policy _µ_ ( _a | s_ ). We write expectations over _D_ as E _τ ∼D_ [ _·_ ]. 

**Mapping to main-text notation.** In the main paper, the context for implicit future alignment is the projected implicit token _xt_ := _zt_ (Eq. (8)), which is a deterministic function of the VLA input _st_ . The goal variable is the future interaction embedding _gt_ + _k_ := _yt_ + _k_ = _h_ ( _st_ + _k_ ) (Eq. (9)). Negatives are drawn from a proposal _p_ neg, instantiated in FOCA by the task-mismatched pool _N¬_ task (Eq. (10)). For readability, the analysis below is written in terms of _st_ (or ( _st, at_ )); the same results apply when conditioning on _xt_ by treating the representation as part of the observation. We use _L_ fm to denote the action-supervised loss (flow matching for diffusion policies) and _L_ imp for the implicit InfoNCE loss. 

**Measure-theoretic note.** For clarity, proofs are written for the _discrete_ case where probabilities are well-defined. For continuous/high-dimensional observations, interpret _ρ_<sup>_π_</sup> ( _· | x_ ) and _p_ neg( _·_ ) as densities w.r.t. a common base measure (or as measures with Radon–Nikodym derivatives). In particular, statements involving log _ρ_<sup>_π_</sup> ( _g | x_ ) _−_ log _p_ neg( _g_ ) require absolute continuity of _ρ_<sup>_π_</sup> ( _· | x_ ) w.r.t. _p_ neg on the support of interest. 

**Object-centric structure.** Let _ξ_ ( _s_ ) be an object extractor returning _m_ object regions (e.g., masks/boxes): _ξ_ ( _s_ ) = _{r_<sup>(</sup><sup>_i_)</sup> ( _s_ ) _}_<sup>_m_</sup> _i_ =1<sup>.We consider an encoder producing a global embedding and object embeddings:</sup> 


We do not assume _ξ_ is perfect; its errors will enter as a misspecification term. 

**Goal space.** Let _G_ denote a goal space and let _h_ : _S →G_ be a measurable _goal map_ . We write _gt_ := _h_ ( _st_ ). In our setting, _h_ may be the identity map id (full-state goals) or an object-centric extractor (e.g., a cropped region/mask, or a learned token derived from _r_<sup>(</sup><sup>_i_)</sup> ( _st_ )). When _h_ = id we have _G_ = _S_ and we may write _gt_ = _st_ for convenience. 

### **F.2. Discounted future occupancy and Bellman recursions** 

We define the _discounted future-occupancy (reachability)_ distribution under policy _π_ (Dayan, 1993; Schaul et al., 2015): 

**Definition F.1** (Discounted future occupancy) **.** Fix a policy _π_ and write _gt_ := _h_ ( _st_ ) _∈G_ . For a state _s_ , define the _state-conditional_ discounted future-occupancy (reachability) distribution: 


and, if we additionally condition on the initial action, define the _action-conditional_ occupancy: 


**Proposition F.2** (Occupancy Bellman equations (Dayan, 1993; Schaul et al., 2015)) **.** _Fix a policy π and a goal g ∈G. Define the state value Vg_<sup>_π_(</sup><sup>_s_) :=</sup><sup>_ρπ_(</sup><sup>_g| s_)</sup><sup>_and the action value Qπ_</sup> _g_<sup>(</sup><sup>_s, a_) :=</sup><sup>_ρπ_(</sup><sup>_g| s, a_)</sup><sup>_.Let P π_(</sup><sup>_s′| s_) := E</sup> _a∼π_ ( _·|s_ )<sup>[</sup><sup>_P_(</sup><sup>_s′| s, a_)]</sup> 

28 

**FOCA-VLA** 

_denote the policy-induced state transition kernel. Then the state-conditional occupancy satisfies_ 


_and the action-conditional occupancy satisfies_ 


_Equivalently, Vg_<sup>_πand Qπ_</sup> _g_<sup>_are the state-/action-value functions for the sparse goal-reaching reward rg_(</sup><sup>_s, a, s′_)=(1</sup><sup>_−_</sup> _γ_ ) **1** _{h_ ( _s_<sup>_′_</sup> ) = _g}._ 

_Proof._ We first prove the action-conditional recursion (21) for _Q_<sup>_π_</sup> _g_<sup>(</sup><sup>_s, a_) :=</sup><sup>_ρπ_(</sup><sup>_g| s, a_).</sup> By Definition F.1, 


Separate the _k_ = 1 term: 


where _s_<sup>_′_</sup> _∼ P_ ( _· | s, a_ ) and _a_<sup>_′_</sup> _∼ π_ ( _· | s_<sup>_′_</sup> ). Combining terms yields Eq. (21). 

For the state-conditional recursion (20), note that by the law of total probability, _Vg_<sup>_π_(</sup><sup>_s_)=</sup><sup>_ρπ_(</sup><sup>_g|s_)=E</sup> _a∼π_ ( _·|s_ )<sup>[</sup><sup>_ρπ_(</sup><sup>_g|_</sup> _s, a_ )] = E _a∼π_ ( _·|s_ )[ _Q_<sup>_π_</sup> _g_<sup>(</sup><sup>_s, a_)].Taking expectation of (21) over</sup><sup>_a ∼π_(</sup><sup>_· | s_) and using</sup><sup>_P π_(</sup><sup>_s′| s_) = E</sup> _a∼π_ ( _·|s_ )<sup>[</sup><sup>_P_(</sup><sup>_s′| s, a_)]</sup> yields Eq. (20). 

_Remark_ F.3 (What is actually learned?) _._ FOCA’s implicit future alignment operates on the model’s _representations_ of the current observation/instruction, and does _not_ condition on action outputs. Therefore, the implicit objective targets the state-conditional occupancy/value _Vg_<sup>_µ_(</sup><sup>_s_) :=</sup><sup>_ρµ_(</sup><sup>_g| s_) under the demonstration distribution.If one augments the context</sup> to include an action embedding (an optional extension), the same analysis would instead target the action-conditional occupancy _Q_<sup>_µ_</sup> _g_<sup>(</sup><sup>_s, a_) :=</sup><sup>_ρµ_(</sup><sup>_g| s, a_).Both satisfy Bellman-style recursions (Proposition F.2), but only the latter has a direct</sup> _Q_ -function interpretation. 

### **F.3. Implicit alignment as density-ratio estimation (InfoNCE** _⇒_ **occupancy/value)** 

We formalize the implicit module as learning a score _fθ_ between a _context_ (current state or state-action) and a _goal_ (future state), trained with negatives from a proposal distribution _p_ neg. 

**Positive sampling scheme.** A critical detail is how we sample future positives. Let _k ∼_ Geom(1 _− γ_ ) over _{_ 1 _,_ 2 _, . . . }_ , i.e., Pr( _k_ ) = (1 _− γ_ ) _γ_<sup>_k−_1</sup> , and let _g_ = _gt_ + _k_ = _h_ ( _st_ + _k_ ). If we take the context to be the current state _x_ = _st_ (as in FOCA’s implicit alignment), then the induced conditional distribution of _g_ is exactly _ρ_<sup>_µ_</sup> ( _· | st_ ). (For completeness, if the context includes the initial action _x_ = ( _st, at_ ), the same sampling yields _ρ_<sup>_µ_</sup> ( _· | st, at_ ).) 

29 

**FOCA-VLA** 

**Lemma F.4** (Geometric sampling matches discounted occupancy) **.** _If k ∼_ Geom(1 _− γ_ ) _and g_ = _gt_ + _k, then_ Pr( _g_ = _g_ ˜ _| xt_ ) = _ρ_<sup>_µ_</sup> (˜ _g | xt_ ) _for all_ ˜ _g ∈G._ 

_Proof._ Fix ( _st, at_ ) = ( _s, a_ ). Let _k ∼_ Geom(1 _− γ_ ) on _{_ 1 _,_ 2 _, . . . }_ so that Pr( _k_ ) = (1 _− γ_ ) _γ_<sup>_k−_1</sup> , and let _g_ = _gt_ + _k_ . Then for any ˜ _g ∈G_ , 


where the last equality is Definition F.1 with _π_ = _µ_ . 

Since FOCA uses state-only context _x_ = _st_ , the same sampling scheme yields _p_<sup>+</sup> ( _g | s_ ) = _ρ_<sup>_µ_</sup> ( _g | s_ ). (If one conditions on ( _s, a_ ) instead, Lemma F.4 gives _p_<sup>+</sup> ( _g | s, a_ ) = _ρ_<sup>_µ_</sup> ( _g | s, a_ ).) 

**Contrastive objective.** Let _x_ denote the context (either ( _s, a_ ) or _s_ ). Let _fθ_ ( _x, g_ ) _∈_ R be a score; in practice this is implemented by dot-product similarity between learned embeddings. We sample a positive _g_<sup>+</sup> _∼ p_<sup>+</sup> ( _g | x_ ) and _N_ negatives _g_ 1<sup>_−, . . . , g_</sup> _N_<sup>_−_i</sup><sup>_._i</sup><sup>_._d</sup><sup>_. p_neg(Eysenbach et al., 2022; Zheng et al., 2023).We optimize the InfoNCE loss (Gutmann & Hyvarinen¨,</sup> 2012; Oord et al., 2018): 


**Lemma F.5** (Bayes-optimal logit is a density ratio) **.** _Consider binary classification between samples from p_<sup>+</sup> ( _g | x_ ) _(positive) and p_ neg( _g_ ) _(negative). The Bayes-optimal logit f_<sup>_∗_</sup> ( _x, g_ ) _satisfies_ 


_for an arbitrary function c that does not depend on g._ 

_Proof._ Consider binary labels _Y ∈{_ + _, −}_ with conditional distributions _G |_ ( _X_ = _x, Y_ = +) _∼ p_<sup>+</sup> ( _· | x_ ) and _G |_ ( _Y_ = _−_ ) _∼ p_ neg( _·_ ). Let _π_ +( _x_ ) = Pr( _Y_ = + _| X_ = _x_ ) and _π−_ ( _x_ ) = 1 _− π_ +( _x_ ). Bayes’ rule gives 


Hence the Bayes-optimal log-odds is 


Setting _c_ ( _x_ ) := log _ππ−_ <u>+((</u> _xx_ <u>))</u><sup>yields the claim.</sup> 

_Proof of Theorem 4.1._ We use a standard “one-positive among negatives” generative model for InfoNCE. Fix a context _x_ . Sample an index _I_ uniformly from _{_ 0 _,_ 1 _, . . . , N }_ . Sample _gI ∼ p_<sup>+</sup> ( _· | x_ ) and _gj_ i _._ i _._ d _.p_ neg( _·_ ) for _j̸_ = _I_ . Let _G_ = _{g_ 0 _, . . . , gN }_ denote the resulting multiset. 

The InfoNCE loss in (22) is the expected multiclass cross-entropy for predicting _I_ from _G_ using the softmax model 


For any fixed ( _x, G_ ), cross-entropy is uniquely minimized (a.s.) when the model matches the true posterior: _qθ_ ( _· | x, G_ ) = Pr( _· | x, G_ ). We therefore compute Pr( _I_ = _i | x, G_ ). By Bayes’ rule and conditional independence, 


Since the factor<sup>�</sup><sup>_N_</sup> _j_ =0<sup>_p_neg(</sup><sup>_gj_) does not depend on</sup><sup>_i_and the prior on</sup><sup>_I_is uniform, we obtain</sup> 


30 

**FOCA-VLA** 

Thus a sufficient condition for _qθ_ ( _· | x, G_ ) to match the posterior for all sets _G_ is 


where _c_ ( _x_ ) is any function independent of _g_ (it cancels in the softmax). This proves the density-ratio form. 

Finally, by Lemma F.4, geometric future sampling implies _p_<sup>+</sup> ( _g | x_ ) = _ρ_<sup>_µ_</sup> ( _g | x_ ), yielding (15). 

_Remark_ F.6 (Optional connection to (soft) _Q_ -learning and RL-as-inference) _._ Equation (15) implies that exp( _fθ_ ) estimates an _unnormalized_ goal-conditioned occupancy (Ziebart et al., 2008). This already yields a value-like reachability score in the state-conditioned setting used by FOCA. 

If one instead uses an _action-conditioned_ score _fθ_ ( _s, a, g_ ) (an optional extension, not required by FOCA’s implicit alignment), one may interpret _fθ_ as an energy over actions for a fixed goal _g_ and define an energy-based policy _πθ_ ( _a | s, g_ ) _∝_ exp( _fθ_ ( _s, a, g_ )), which is structurally aligned with maximum-entropy RL. Making this connection rigorous in high-dimensional action spaces requires additional assumptions and a gauge-fixing/normalization to remove additive terms that depend on ( _s, a_ ); otherwise the InfoNCE optimum is identifiable only up to _c_ ( _s, a_ ). 

_Remark_ F.7 (Critical caveat: negative sampling matters) _._ If _p_ neg is far from the marginal goal distribution induced by the dataset, the ratio in (15) may prioritize “easy negatives” and distort the learned metric (Zheng et al., 2023). Empirically, this manifests as unstable or task-irrelevant alignment unless negatives are carefully chosen. In FOCA we draw negatives from the task-mismatched pool _N¬_ task (Eq. (10)), which can be viewed as choosing a task-conditioned proposal that yields informative (hard) negatives. 

### **F.4. Multi-frame futures and** _n_ **-step structure** 

Theorems above hold exactly for geometric sampling. If instead one chooses a fixed horizon _k_ , then _p_<sup>+</sup> ( _g | x_ ) becomes the _k_ -step transition distribution, not the discounted occupancy. This is still useful, but it no longer corresponds to a Bellman fixed point for a single discount. 

**Proposition F.8** (Fixed-horizon positives learn _k_ -step transitions) **.** _If positives are sampled as g_ = _gt_ + _k_ = _h_ ( _st_ + _k_ ) _with deterministic k ≥_ 1 _, then fθ_ ( _x, g_ ) _estimates_ log Pr _µ_ ( _gt_ + _k_ = _g | x_ ) _−_ log _p_ neg( _g_ ) _up to c_ ( _x_ ) _._ 

_Proof._ Under fixed-horizon sampling _g_ = _gt_ + _k_ (deterministic _k ≥_ 1), the positive conditional distribution is 


where _x_ denotes the chosen context (state or state-action). Applying the argument in the proof of Theorem 4.1 with this _p_<sup>+</sup> gives 


as claimed. In the special case _h_ = id, then _gt_ + _k_ = _st_ + _k_ and the positive distribution reduces to the standard _k_ -step state transition. 

_Remark_ F.9 (Practical implication) _._ Using a mixture over multiple horizons corresponds to learning a mixture of _k_ -step transition distributions (Oord et al., 2018). Choosing a geometric distribution is the unique memoryless choice (up to constants) that yields a single discounted occupancy target with a Bellman-style fixed point (Proposition F.2). 

### **F.5. Explicit object-centric prediction as restricted world modeling** 

FOCA’s explicit head predicts a future interaction embedding in latent space (Sec. 3.2), focusing supervision on task-grounded dynamic regions. Abstractly, let _x_ denote the current context (in FOCA, _x_ = _xt_ = _zt_ ) and let _g_<sup>+</sup> = _h_ ( _st_ + _k_ ) denote the sampled future interaction embedding. The explicit loss in the main paper (Eq. (6)) is a deterministic regression objective: 


_Proof of Proposition 4.2._ Fix a context _x_ . The conditional objective is _L_ exp( _x_ ; � _g_ ) = E[ _∥g_ �( _x_ ) _− g_<sup>+</sup> _∥_<sup>2</sup> 2<sup>_| x_]</sup><sup>_._Expanding the square and</sup> dropping terms independent of � _g_ ( _x_ ) gives _L_ exp( _x_ ; � _g_ ) = _∥g_ �( _x_ ) _∥_<sup>2</sup> 2<sup>_−_2 �</sup><sup>_g_(</sup><sup>_x_)</sup><sup>_⊤_E[</sup><sup>_g_+</sup><sup>_| x_] + const</sup><sup>_._This quadratic is minimized uniquely by</sup> _g_ �<sup>_∗_</sup> ( _x_ ) = E[ _g_<sup>+</sup> _| x_ ]. Under geometric future sampling (Lemma F.4), _g_<sup>+</sup> _| x ∼ ρ_<sup>_µ_</sup> ( _· | x_ ), hence � _g_<sup>_∗_</sup> ( _x_ ) = E _g∼ρµ_ ( _·|x_ )[ _g_ ]. 

_Remark_ F.10 (Connection to likelihood modeling) _._ The squared loss (24) is equivalent to a Gaussian negative log-likelihood with fixed variance, so Proposition 4.2 can be interpreted as maximum-likelihood estimation of the Gaussian mean. However, unlike the implicit contrastive objective (Theorem 4.1), this regression loss does not estimate the full occupancy distribution in multimodal futures; it summarizes it through a point estimate, which is why it complements (rather than replaces) implicit alignment in practice. 

### **F.6. Hybrid objective and object-centric factorization** 

We combine action supervision (flow matching / imitation) with future-oriented auxiliary losses: 


31 

**FOCA-VLA** 

**Assumption F.11** (Log-domain factorization gaps) **.** There exists a decomposition _g_ = ( _g_<sup>(1)</sup> _, . . . , g_<sup>(</sup><sup>_m_)</sup> ) and _x_ = ( _x_<sup>(1)</sup> _, . . . , x_<sup>(</sup><sup>_m_)</sup> ) and candidate factors _{ρ_<sup>_µ_</sup> _i_<sup>(</sup><sup>_· | x_(</sup><sup>_i_))</sup><sup>_}_</sup> _i_<sup>_m_</sup> =1<sup>and</sup><sup>_{p_neg</sup><sup>_,i}_</sup> _i_<sup>_m_</sup> =1<sup>such that the log-densities admit bounded residuals:</sup> 


and there exist constants _ερ, ε_ neg _≥_ 0 such that 


on the support of the training pairs ( _x, g_ ). 

**Theorem F.12** (Additive decomposition with explicit approximation error) **.** _Under Assumption F.11 and the conditions of Theorem 4.1, there exists a function c_ ( _x_ ) _independent of g such that any population-optimal score satisfies_ 


_where the residual δ_ ( _x, g_ ) _obeys the uniform bound_ 


_Proof._ By Theorem 4.1, the population-optimal score has the form 

_f_<sup>_∗_</sup> ( _x, g_ ) = log _ρ_<sup>_µ_</sup> ( _g | x_ ) _−_ log _p_ neg( _g_ ) + _c_ ( _x_ ) _,_ 

for some _c_ ( _x_ ) independent of _g_ . Add and subtract the factorized log terms: 


This proves the decomposition (29). Under Assumption F.11, we have _|_ ∆ _ρ_ ( _x, g_ ) _| ≤ ερ_ and _|_ ∆neg( _g_ ) _| ≤ ε_ neg on the support of training pairs, hence by the triangle inequality 


_Remark_ F.13 (Interpretation and a design knob) _._ Assumption F.11 is intentionally explicit: it isolates _why_ object-centric additivity can fail in manipulation. The residual ∆ _ρ_ captures inter-object coupling and any information loss induced by the object-centric projection _x �→_ ( _x_<sup>(</sup><sup>_i_)</sup> ); ∆neg captures non-factorized negative sampling. In particular, if negatives are constructed to factorize across objects (so that _p_ neg( _g_ ) =<sup>�</sup> _i_<sup>_p_neg</sup><sup>_,i_(</sup><sup>_g_(</sup><sup>_i_))), then</sup><sup>_ε_neg=0 and the decomposition error is controlled purely by the dynamics/representation coupling</sup> term _ερ_ . 

_Remark_ F.14 (Expected factorization gap (KL / multi-information)) _._ If one chooses _ρ_<sup>_µ_</sup> _i_<sup>(</sup><sup>_·|x_) such that �</sup> _i_<sup>_ρ_</sup> _i_<sup>_µ_(</sup><sup>_·|x_) forms a product</sup> distribution over _G_ for each _x_ , then E _g∼ρµ_ ( _·|x_ )[∆ _ρ_ ( _x, g_ )] = KL( _ρ_<sup>_µ_</sup> ( _· | x_ ) _∥_<sup>�</sup> _i_<sup>_ρ_</sup> _i_<sup>_µ_(</sup><sup>_·|x_(</sup><sup>_i_))).Thus,∆</sup><sup>_ρ_canbeinterpretedasa</sup> conditional multi-information term measuring inter-object coupling and information loss from the object-centric projection. This suggests a principled diagnostic: estimate the KL gap (or a lower bound) to quantify when additive object-wise critics are justified. 

Assumption F.11 is violated in manipulation due to contacts, occlusions, and coupled dynamics. The value of the object-centric architecture is therefore not that factorization is exact, but that attention over object tokens can approximate sparse interaction graphs (a structured critic), potentially improving credit assignment relative to monolithic global embeddings. 

### **F.7. DreamGen (video-only) augmentation** 

Let _D_<sup>�</sup> denote synthetic videos generated by a world model (e.g., DreamGen (Jang et al., 2025)), which provide state sequences but no actions. Training the implicit objective on _D_<sup>�</sup> corresponds to learning a goal-occupancy under a different rollout distribution _ρ_ ˜. **Proposition F.15** (Mixture bias from synthetic rollouts) **.** _If L_ imp _is trained on a mixture of real demonstrations and action-free synthetic rollouts with mixing weight α ∈_ [0 _,_ 1] _, then the learned score corresponds to fθ_ ( _xt, g_ ) = log _ρ_ mix( _g | xt_ ) _−_ log _p_ neg( _g_ ) + _c_ ( _xt_ ) _, where ρ_ mix = (1 _− α_ ) _ρ_<sup>_µ_</sup> + _αρ_ ˜ _and ρ_ ˜ _is the discounted occupancy induced by the synthetic rollouts._ 

_Proof._ Let _p_<sup>+</sup> real<sup>(</sup><sup>_g| x_) =</sup><sup>_ρµ_(</sup><sup>_g| x_) and</sup><sup>_p_+</sup> syn<sup>(</sup><sup>_g| x_) =</sup><sup>_ρ_˜(</sup><sup>_g| x_).If each positive is drawn from the real source w.p. 1</sup><sup>_−α_and from the</sup> 

32 

**FOCA-VLA** 

synthetic source w.p. _α_ , then by the law of total probability, 

_p_<sup>+</sup> mix<sup>(</sup><sup>_g| x_) = (1</sup><sup>_−α_)</sup><sup>_ρµ_(</sup><sup>_g| x_) +</sup><sup>_αρ_˜(</sup><sup>_g| x_) =:</sup><sup>_ρ_mix(</sup><sup>_g| x_)</sup><sup>_._</sup> 

Applying Theorem 4.1 with _p_<sup>+</sup> = _p_<sup>+</sup> mix<sup>yields</sup> 


which proves the claim. 

**Theorem F.16** (A simple robustness bound (relative error regime)) **.** _Assume αϵ <_ 1 _and ρ_ ˜( _g | x_ ) _satisfies a uniform relative-error bound_ (1 _− ϵ_ ) _ρ_<sup>_µ_</sup> ( _g | x_ ) _≤ ρ_ ˜( _g | x_ ) _≤_ (1 + _ϵ_ ) _ρ_<sup>_µ_</sup> ( _g | x_ ) _for all_ ( _x, g_ ) _. Then the mixture score bias is bounded as_ 


_Proof._ Assume (1 _− ϵ_ ) _ρ_<sup>_µ_</sup> ( _g | x_ ) _≤ ρ_ ˜( _g | x_ ) _≤_ (1 + _ϵ_ ) _ρ_<sup>_µ_</sup> ( _g | x_ ) for all ( _x, g_ ). Then the mixture occupancy _ρ_ mix = (1 _− α_ ) _ρ_<sup>_µ_</sup> + _αρ_ ˜ satisfies (1 _− α_ ) _ρ_<sup>_µ_</sup> + _α_ (1 _− ϵ_ ) _ρ_<sup>_µ_</sup> _≤ ρ_ mix _≤_ (1 _− α_ ) _ρ_<sup>_µ_</sup> + _α_ (1 + _ϵ_ ) _ρ_<sup>_µ_</sup> _,_ 

i.e., 


Assuming _αϵ <_ 1 (so the lower bound is positive), taking logs gives 


Therefore, 


Finally, note that max _{−_ log(1 _− αϵ_ ) _,_ log(1 + _αϵ_ ) _} ≤_ log(1 + _αϵ_ ) _−_ log(1 _− αϵ_ ), which yields the (looser) bound stated in the theorem. 

_Remark_ F.17 (Critical caveat: hallucinations destroy uniform bounds) _._ Theorem F.16 requires a strong uniform approximation; in practice video generators can hallucinate (Jang et al., 2025), especially in low-data regimes. This motivates conservative weighting schemes that downweight synthetic positives unless they are validated by a discriminator or consistency check. Such conservatism is analogous in spirit to offline RL methods that penalize out-of-distribution value estimates, but extending those guarantees to representation-level occupancy estimation remains open. 

In the video-only setting, the implicit objective is applied with state-only context _x_ = _s_ , hence estimating _ρ_ ( _g | s_ ); learning _ρ_ ( _g | s, a_ ) would require pseudo-actions (IDM/IGM/LAPA). 

### **F.8. Universal evaluation and multi-positive futures** 

**Proposition F.18** (Universal evaluation from occupancy) **.** _Let u_ : _G →_ R _be bounded, and define the reward ru_ ( _s, a, s_<sup>_′_</sup> ) := _u_ ( _h_ ( _s_<sup>_′_</sup> )) = _u_ ( _gt_ +1) _. Let Q_<sup>_π_</sup> _u_<sup>(</sup><sup>_s, a_)</sup><sup>_denote the standard discounted action-value function under π for reward r_</sup> _u_<sup>_.Then_</sup> 


_Similarly, Vu_<sup>_π_(</sup><sup>_s_) =</sup> 1 _−_ <u>1</u> _γ_<sup>E</sup><sup>_g∼ρπ_(</sup><sup>_·|s_)[</sup><sup>_u_(</sup><sup>_g_)]</sup><sup>_._</sup> 

_Proof._ By definition of _Q_<sup>_π_</sup> _u_<sup>with reward</sup><sup>_r_</sup> _u_<sup>(</sup><sup>_s_</sup> _t_<sup>_, a_</sup> _t_<sup>_, s_</sup> _t_ +1<sup>) =</sup><sup>_u_(</sup><sup>_g_</sup> _t_ +1<sup>),</sup> 


On the other hand, 


which implies _Q_<sup>_π_</sup> _u_<sup>(</sup><sup>_s, a_) =</sup> 1 _−_ <u>1</u> _γ_<sup>E</sup><sup>_g∼ρπ_(</sup><sup>_·|s,a_)[</sup><sup>_u_(</sup><sup>_g_)].The state-value case follows by marginalizing over</sup><sup>_a ∼π_(</sup><sup>_· | s_).</sup> 

33 

**FOCA-VLA** 

_Remark_ F.19 (Why this matters) _._ Proposition F.18 shows _ρ_<sup>_π_</sup> ( _· | s, a_ ) is a _universal critic_ for any reward that depends on future goal variables (Dayan, 1993; Schaul et al., 2015). The sparse goal-reaching case in Proposition F.2 is recovered (up to the (1 _−γ_ ) normalization) by choosing _u_ (˜ _g_ ) = **1** _{g_ ˜ = _g}_ ; equivalently, choosing _u_ (˜ _g_ ) = (1 _− γ_ ) **1** _{g_ ˜ = _g}_ matches the reward in Proposition F.2 exactly. **Proposition F.20** (Multi-positive (multi-frame) sampling learns a mixture occupancy) **.** _Let ν be a distribution over horizons {_ 1 _,_ 2 _, . . . }. Define the induced positive distribution_ 


_where x is the chosen context (either s or_ ( _s, a_ ) _). If the implicit contrastive objective samples k ∼ ν and uses g_ = _gt_ + _k as the positive, then the population-optimal InfoNCE score satisfies_ 

_fθ_ ( _x, g_ ) = log _ρ_<sup>_µ_</sup> _ν_<sup>(</sup><sup>_g| x_)</sup><sup>_−_log</sup><sup>_p_</sup> neg<sup>(</sup><sup>_g_) +</sup><sup>_c_(</sup><sup>_x_)</sup><sup>_,_</sup> (34) _for some c_ ( _x_ ) _independent of g. In particular, if ν_ = Geom(1 _− γ_ ) _on {_ 1 _,_ 2 _, . . . }, then ρν_<sup>_µ_=</sup><sup>_ρµin Definition F.1._</sup> 

_Proof._ Under the stated sampling scheme, the positive conditional distribution is exactly _p_<sup>+</sup> ( _g | x_ ) = _ρν_<sup>_µ_(</sup><sup>_g|x_) by the law of total</sup> probability over _k ∼ ν_ . Applying Theorem 4.1 with this _p_<sup>+</sup> yields _fθ_ ( _x, g_ ) = log _ρ_<sup>_µ_</sup> _ν_<sup>(</sup><sup>_g| x_)</sup><sup>_−_log</sup><sup>_p_</sup> neg<sup>(</sup><sup>_g_) +</sup><sup>_c_(</sup><sup>_x_).For geometric</sup><sup>_ν_on</sup> _{_ 1 _,_ 2 _, . . . }_ with _ν_ ( _k_ ) = (1 _− γ_ ) _γ_<sup>_k−_1</sup> , we have _ρν_<sup>_µ_=</sup><sup>_ρµ_by Definition F.1.</sup> 

_Remark_ F.21 (Interpreting “multi-frame” alignment) _._ Sampling multiple future frames (or multiple offsets) corresponds to learning log _ρν_<sup>_µ_</sup> for a _mixture_ over horizons (Oord et al., 2018). Geometric _ν_ is the special choice that recovers a discounted Bellman fixed point. 

**Summary.** Under geometric future sampling, the implicit future-alignment objective is equivalent (at the population optimum) to estimating the log density ratio of a goal-conditioned discounted occupancy (a value-like reachability quantity). In the state-conditioned setting used by FOCA, this corresponds to the state occupancy/value _ρ_<sup>_µ_</sup> ( _g | s_ ); an action-conditioned variant would instead recover _ρ_<sup>_µ_</sup> ( _g | s, a_ ) and a more direct _Q_ -function interpretation for sparse goal-reaching rewards (Proposition F.2). Explicit object-centric prediction instead summarizes this occupancy via regression (Proposition 4.2), estimating a conditional mean that is directly useful for control. Their combination can be interpreted as a hybrid estimator with complementary failure modes; however, claims about policy improvement beyond the dataset behavior require additional offline RL machinery and careful distribution-shift analysis, especially when incorporating synthetic rollouts. 

34 

