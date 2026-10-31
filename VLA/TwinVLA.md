---
title: "TwinVLA: Data-Efficient Bimanual Manipulation with Twin Single-Arm Vision-Language-Action Models"
date: "2025-11-07"
authors: "Hokyun Im; Euijin Jeong; Andrey Kolobov; Jianlong Fu; Youngwoon Lee"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2511.05275
pdf: https://arxiv.org/pdf/2511.05275
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.05275)** / [論文ページ](https://arxiv.org/abs/2511.05275)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Published as a conference paper at ICLR 2026 

TWINVLA: DATA-EFFICIENT BIMANUAL MANIPULATION WITH TWIN SINGLE-ARM VISION-LANGUAGEACTION MODELS 

**Hokyun Im**<sup>**1,2**</sup> **Euijin Jeong**<sup>**1**</sup> **Andrey Kolobov**<sup>**2**</sup> **Jianlong Fu**<sup>**2**</sup> **Youngwoon Lee**<sup>**1**</sup> 1Department of Artificial Intelligence, Yonsei University 2Microsoft Research `https://jellyho.github.io/TwinVLA/` 

# ABSTRACT 

Vision-language-action models (VLAs) trained on large-scale robotic datasets have demonstrated strong performance on manipulation tasks, including bimanual tasks. However, because most public datasets focus on single-arm demonstrations, adapting VLAs for bimanual tasks typically requires substantial additional bimanual data and fine-tuning. To address this challenge, we introduce TwinVLA, a modular framework that composes two copies of a pretrained single-arm VLA into a coordinated bimanual VLA. Unlike monolithic cross-embodiment models trained on mixtures of single-arm and bimanual data, TwinVLA improves both data efficiency and performance by composing pretrained single-arm policies. Across diverse bimanual tasks in real-world and simulation settings, TwinVLA outperforms a comparably-sized monolithic RDT-1B model without requiring _any_ bimanual pretraining. Furthermore, it narrows the gap to state-of-the-art model _π_ 0, which relies on extensive proprietary bimanual data and compute cost. These results establish our modular composition approach as a data-efficient and scalable path toward high-performance bimanual manipulation, leveraging public single-arm data. 

# 1 INTRODUCTION 

Thanks to publicly available large-scale robotic datasets, vision-language-action models (VLAs) have shown impressive performance in single-arm robotic manipulation, effectively adapting to downstream tasks and generalizing across diverse tasks, objects, and environments (Zitkovich et al., 2023; Open X-Embodiment Collaboration et al., 2024; Kim et al., 2024; Black et al., 2024). However, extending these successes to _bimanual_ manipulation remains challenging, as public bimanual datasets are scarce, and existing approaches often rely on large, proprietary datasets that require thousands of hours of data collection and curation (Black et al., 2024), limiting reproducibility and progress. 

Can we build strong bimanual VLAs without collecting or fine-tuning on large bimanual datasets by leveraging existing single-arm data? In this work, we propose a highly data-efficient adaptation paradigm for bimanual control that eliminates the need for prohibitive bimanual pretraining. By effectively repurposing a single-arm VLA, we demonstrate that complex bimanual skills can be mastered using only minimal target-domain demonstrations, establishing a practical and reproducible pathway to bimanual manipulation. 

To effectively realize this transfer of single-arm priors to bimanual control, the choice of underlying architecture is critical. Recent cross-embodiment learning work typically trains monolithic models on multi-robot datasets (Open X-Embodiment Collaboration et al., 2024) employing embodimentspecific action decoders (Octo Model Team et al., 2024; NVIDIA et al., 2025) or shared, zero-padded action spaces (Liu et al., 2024; Black et al., 2024). Although promising, differences in observation and action spaces introduce heterogeneity, forcing a single model to handle disparate action spaces, and monolithic training underutilizes the _modular_ structure inherent to bimanual tasks. 

A _modular_ perspective on bimanual manipulation is supported by neuroscience: human bimanual manipulation is the coordination of arm-specific motor primitives rather than a single monolithic controller. Dedicated neural circuits, such as the Supplementary Motor Area (SMA) and the corpus callosum, orchestrate and synchronize the two arms (Sadato et al., 1997; Swinnen, 2002). Similar 

1 

Published as a conference paper at ICLR 2026 


Figure 1: **Overview of TwinVLA.** Inspired by humans’ two-arm coordination for bimanual manipulation, TwinVLA duplicates a VLM backbone pretrained on cross-embodiment single-arm data ( _Left_ ) to form two arm-specific branches linked via **Joint Attention** ( _Right_ ). Shared inputs (ego-centric views, language instructions) are routed via a mixture-of-experts (MoE) to improve computational efficiency. Only the VLM backbone is duplicated, keeping the increase in model size minimal. 

principles have proven effective in vision-language modeling, where interaction between modalityspecific backbones improves its efficiency and effectiveness (Liang et al., 2024). 

Inspired by these insights, we propose TwinVLA, a modular architecture that operationalizes this coordination-centric view. Instead of training from scratch, TwinVLA leverages a pretrained singlearm VLA. Specifically, we first design a lightweight, compact single-arm VLA, which we call SingleVLA (Section A). We pre-train a 0.8B-size SingleVLA for single-arm manipulation on the OXE dataset (Open X-Embodiment Collaboration et al., 2024). We then duplicate this SingleVLA and integrate the two “twin” instances through a lightweight coordination method. This design is highly data-efficient: it eliminates the need for a bimanual pretraining dataset and achieves strong performance with only a small amount of bimanual demonstrations for fine-tuning. 

To integrate two SingleVLAs into a bimanual policy, TwinVLA utilizes a joint attention (Liang et al., 2024) across the twin models, as illustrated in Figure 1. This allows the twin SingleVLAs to exchange information and coordinate their actions, while preserving their pretrained capabilities. This approach is made feasible without significant overhead, as we duplicate only the VLM backbone and utilize a Mixture-of-Experts (MoE) to efficiently manage shared inputs. In contrast to monolithic cross-embodiment models (Liu et al., 2024; Octo Model Team et al., 2024; Doshi et al., 2024), our approach yields better performance and data efficiency, significantly reducing the need for large-scale bimanual data collection and compute. 

We evaluate TwinVLA across a broad range of environments, including a complex, long-horizon real-world task and a diverse suite of bimanual manipulation tasks in simulations. Despite leveraging only public single-arm data and limited bimanual fine-tuning data, TwinVLA achieves performance comparable to state-of-the-art bimanual policies. 

In summary, our main contributions are threefold: 

- We propose a novel modular architecture for bimanual manipulation that integrates two copies of a pretrained SingleVLA with a lightweight coordination method based on joint attention with MoE, enabling synchronized two-arm control. 

- We present a data-efficient paradigm that adapts our twin architecture into a capable bimanual policy for a target task by fine-tuning on only a small bimanual dataset, crucially without requiring additional pretraining, thereby eliminating the need for large-scale bimanual data. 

- Through extensive experiments across real and simulated bimanual tasks, TwinVLA matches or surpasses state-of-the-art models trained on far larger bimanual data and compute. 

Together, these findings identify our modular SingleVLA composition approach as a scalable, efficient path to high-performance bimanual manipulation. 

2 

Published as a conference paper at ICLR 2026 


Figure 2: **(a) Data efficiency.** TwinVLA requires only _∼_ 800h of single-arm and 50 episodes of target bimanual data, significantly less than RDT-1B ( _∼_ 2 _,_ 400h) and _π_ 0 ( _∼_ 10 _,_ 900h) in total. **(b) Compute efficiency.** RDT-1B and _π_ 0 require high compute (exceeding 1 _,_ 000 H100 GPU-days), whereas TwinVLA achieves higher or comparable performance with only 25 H100 GPU-days. 

# 2 RELATED WORK 

Bimanual manipulation policies are essential to enable robots to perform complex tasks that require coordinated two-handed control, such as folding laundry (Bersch et al., 2011; Avigal et al., 2022), assembling parts (Stavridis & Doulgeri, 2018), or wiping the plate (Black et al., 2025; Chi et al., 2024b). Learning effective bimanual policies is challenging due to high-dimensional, tightly coupled action spaces and the scarcity of high-quality bimanual demonstrations (Lee et al., 2020; Xie et al., 2020). Consequently, specialist methods, such as Diffusion policy (Chi et al., 2024a) and ACT (Zhao et al., 2023), trained only on target-task demonstrations, struggle on precise, long-horizon tasks. 

Recent works have explored various architectures for bimanual control to explicitly model the interdependencies between arms (Lee et al., 2024; Kobayashi & Buamanee, 2025), or focus on high-level language planning via VLM (Gbagbe et al., 2024). Anybimanual (Lu et al., 2025) introduces a high-level skill manager to coordinate primitives and visual aligner to mask 3D voxels for decoupled policies, benefiting from both high-level managing and architectural inductive bias. While promising, it is difficult to generalize these methods, as they are often limited to small-scale scenarios, handle only low-dexterity tasks, or backbone constraints (Grotz et al., 2024; Shridhar et al., 2022). 

Alternatively, another line of research extends successful unimanual Vision-Language-Action (VLA) models (Liu et al., 2023b; Zitkovich et al., 2023; Li et al., 2024b) to bimanual tasks. This transition is challenging due to the scarcity of bimanual data, as public datasets are predominantly unimanual. To overcome this, prior work trains ‘monolithic’ models, requiring large-scale bimanual data collection and intensive pretraining. For example, RDT-1B (Liu et al., 2024) required massive pretraining and fine-tuning (reportedly a month on 48 H100 GPUs), and _π_ 0 (Black et al., 2024) relies on a 10 _,_ 000hour proprietary dataset, both incurring high computational costs. Furthermore, the proprietary nature of these datasets limits reproducibility and broader adoption. 

In contrast to both monolithic, compute-heavy pretraining and specialized architectural designs, our approach adopts a modular, coordination-centric design. While Anybimanual (Lu et al., 2025) introduces novel inductive biases for coordination, these are often difficult to integrate into generalpurpose VLA frameworks due to specific backbone constraints. Our method, however, is designed to leverage and scale the existing generalist VLAs. We first train a SingleVLA on large-scale public single-arm data, duplicate to couple them, and then fine-tune it on bimanual tasks—allowing each stage to benefit from the most suitable data (see Figure 2). This composition-based approach avoids bimanual pretraining, requires only a small amount of bimanual fine-tuning, better preserves the strong capabilities of single-arm policies, and significantly improves data and compute efficiency. 

# 3 PRELIMINARIES 

This paper aims to develop a data-efficient framework for learning bimanual manipulation policies by building upon pretrained single-arm Vision-Language-Action (SingleVLA) models. This section 

3 

Published as a conference paper at ICLR 2026 

formalizes the single-arm and bimanual settings, briefly describes the VLA training objective, and introduces the core architectural concepts we leverage. 

## 3.1 FORMULATING THE BIMANUAL VLA POLICY 

Our goal is to extend a pretrained SingleVLA _π_ single into a bimanual policy _π_ twin applicable to target bimanual tasks. A VLA _π_ ( _At | ot_ ) predicts an _action chunk At_ = ( _at, at_ +1 _, . . . , at_ + _T −_ 1) of length _T_ from an observation _ot_ . For single-arm manipulation, the observation _o_<sup>single</sup> _t_ = (( _l, I_ ego) _t,_ ( _I_ wrist _, d_ ) _t_ ) includes a language prompt _l_ , an ego-centric image _I_ ego (shared input), and an arm-specific wrist image _I_ wrist with proprioception _d_ (arm-specific input). We train _π_ single( _At | ot_<sup>single</sup> ) to predict the action chunk for one arm. For bimanual manipulation, the observation aggregates both right = ( _R_ ) and left ( _L_ ) arm-specific input, _o_<sup>twin</sup> _t_ �( _l, I_ ego) _t,_ ( _I_ wrist<sup>_R, dR_)</sup><sup>_t,_(</sup><sup>_I_</sup> wrist<sup>_L, dL_)</sup><sup>_t_</sup> �, and the policy _π_ twin( _A_<sup>_R_</sup> _t_<sup>_, AL_</sup> _t_<sup>_| o_twin</sup> _t_ ) outputs a joint action chunk for right and left arms. 

## 3.2 TRAINING VLAS WITH CONDITIONAL FLOW MATCHING 

We train our VLA models to predict continuous robot actions from observations. Each observation _ot_ is tokenized and fed into the VLM backbone to produce an output embedding _ht_ (from a learnable readout token _rt_ ). To enable continuous action prediction from _ht_ , we attach an action head _vθ_ ( _A_<sup>_τ_</sup> _t_<sup>_, ht, dt_) and train it using a conditional flow matching objective.The action head is trained</sup> with the following loss function: 


where _ht_ is the VLM output embedding and _dt_ is proprioception. This objective trains the action head _vθ_ to predict the reference flow **u** from a noised action chunk _A_<sup>_τ_</sup> _t_<sup>to the target action chunk</sup><sup>_At_,</sup> conditioned on the VLM output and proprioception. 

During inference, we sample actions using the forward Euler integration method. Starting from _A_ 0 _∼ N_ (0 _, I_ ), we iteratively update the action using the learned flow _vθ_ : 


## 3.3 MIXTURE-BASED ARCHITECTURES 

To adapt Transformers for multi-modal inputs, various mixture-based architectures have been explored and shown to be effective. These approaches range from combining entire, modality-specific backbones to ensembling or mixing individual layers within a single backbone. We briefly introduce two such paradigms that inform our design: a _model-level_ Mixture-of-Transformers (MoT), which coordinates separate backbones, and a _layer-level_ Mixture-of-Experts (MoE), which enables efficient, sparse computation. 

The MoT architecture (Liang et al., 2024) enables efficient information sharing between separate, modality-specific backbones (e.g., text and image). It introduces _joint attention_ , a shared self-attention layer performed over the union of multimodal inputs, allowing each modality to directly attend to the others. Meanwhile, modality-specific components such as feed-forward networks remain separate, making fusion lightweight yet effective. 

MoE (Shazeer et al., 2017) scales model capacity efficiently by routing each input _x_ through a weighted combination of expert feed-forward networks using a gating function, yielding MoE( _x_ ) = � _i_<sup>_wiEi_(</sup><sup>_x_), where</sup><sup>_wi_denotes the routing weight.</sup> 

# 4 TWINVLA 

TwinVLA is a modular architecture that transforms a pretrained single-arm VLA into a coordinated bimanual policy. The overall computation flow of our architecture is described in Algorithm 1 and Figure 3. TwinVLA integrates single-arm policies through three core principles: (1) selective module duplication (Section 4.1), (2) cross-arm fusion via joint attention (Section 4.2), and (3) efficient shared representation via Mixture-of-Experts (Section 4.3). 

4 

Published as a conference paper at ICLR 2026 

## **Algorithm 1** TwinVLA 

_X_ 0<sup>_m_:encoded inputs from</sup><sup>_o_</sup> _t_<sup>twin</sup> (Section 3.1) for each input _m ∈{_ shared _,_ left _,_ right _}_ . FFN _b_ : feed-forward network layer from each backbone _b ∈{_ left _,_ right _}_ . _N_ : Number of transformer layers **for** _n_ = 0 to _N −_ 1 **do** _▷_ Iterate every transformer layer // Prepare Q, K, V for each input _m_ **for** each input _m ∈{_ shared _,_ left _,_ right _}_ **do** _Q_<sup>_m_</sup> _n_<sup>_, K_</sup> _n_<sup>_m, V_</sup> _n_<sup>_m←_Norm(Proj(</sup><sup>_X_</sup> _n_<sup>_m_))</sup> _▷_ Input-specific projections, Algorithm 3 **end for** // Joint attention across inputs with attention re-weighting _{A_<sup>_m_</sup> _n_<sup>_} ←_JointAttention(</sup><sup>_{Q_</sup> _n_<sup>_m}, {K_</sup> _n_<sup>_m}, {V_</sup> _n_<sup>_m}, M_)</sup> _▷_ Algorithm 2, with mask _M_ Figure 3a // Residual & FFN / MoE **for** each input _m ∈{_ shared _,_ left _,_ right _}_ **do** _Hn_<sup>_m←X_</sup> _n_<sup>_m_+ Norm(Proj(</sup><sup>_Am_</sup> _n_<sup>))</sup> _▷_ Input-specific output projection, Algorithm 3 _Fn_<sup>_m←_MoE(</sup><sup>_H_</sup> _n_<sup>_m_)</sup><sup>**if**</sup><sup>_m_= shared</sup><sup>**else**FFN</sup><sup>_m_(</sup><sup>_H_</sup> _n_<sup>_m_)</sup> _▷_ MoE for shared input, Equation (3) _Xn_<sup>_m_</sup> +1<sup>_←H_</sup> _n_<sup>_m_+ Norm(</sup><sup>_F m_</sup> _n_<sup>)</sup> _▷_ Residual connection with norm, Algorithm 3 **end for end for return** _{XN_<sup>_m}_</sup> _▷_ Return outputs, this will be used for action decoding 

## 4.1 SINGLE-ARM POLICY DUPLICATION 

We first pre-train a VLA on a single-arm dataset, which we refer to as SingleVLA. Note that existing pre-trained models can also be used for this purpose. To construct TwinVLA from SingleVLA, we initialize the twin policies for the left and right arms by copying the pretrained SingleVLA. However, instead of duplicating the full model, we share the vision encoder and DiT (Peebles & Xie, 2023) action head while fully replicating the VLM. Each arm has its own lightweight proprioception encoder. This design yields a compact 1 _._ 3B-parameter model, comparable to the 1 _._ 2B-parameter RDT-1B, without significantly increasing computational cost. 

Visual inputs are processed by the shared encoder, and each VLM produces readout tokens that are jointly decoded by the shared DiT. This design is motivated by the principle that general visual understanding (image encoding) and low-level motor control (action decoding) are largely embodiment-agnostic skills that can be effectively shared for both arms. In contrast, the VLM, which decides output action given encoded observation, is fully replicated to allow for specialized control. 

## 4.2 JOINT ATTENTION FOR CROSS-ARM FUSION 

We integrate arm-specific inputs using a Joint Attention mechanism inspired by MoT (Liang et al., 2024). As illustrated in Figure 3b and Algorithm 1, this is achieved by sharing only the self-attention layers across the VLM backbones. Specifically, we concatenate the _Q, K, V_ from both backbones, perform self-attention, and subsequently split the outputs back to their respective streams, while other components such as projections use arm-specific networks from each arm’s VLM backbone. Unlike _π_ 0 (Black et al., 2024), which links a VLM with an action head, we connect two VLMs directly. We elaborate joint attention mechanism in detail on Algorithm 2. 

**Causal joint attention mask.** Effective joint attention requires appropriate attention masking. Standard LLMs use a lower-triangular attention mask for causal prediction. To support joint attention among the shared and arm-specific inputs, we designed the attention mask for TwinVLA as shown in Figure 3a. Specifically, we embed lower-triangular masks within each arm’s region while treating the shared modality as fully accessible. Each arm also attends to half of the other’s tokens, enabling symmetric cross-arm interaction without violating autoregressive constraints. 

## 4.3 MIXTURE-OF-EXPERTS INTEGRATION 

In TwinVLA, feeding shared inputs ( _l, I_ ego) _t_ redundantly to both VLMs significantly increases VRAM usage. To address this, we process shared tokens as a single sequence by employing a MoE 

5 

Published as a conference paper at ICLR 2026 


Figure 3: **(a) Causal attention mask for joint attention.** It preserves causality while processing shared, left, and right inputs in parallel. **(b) TwinVLA joint attention mechanism.** The two VLMs share information, and the shared modality ( _l, I_ ego) _t_ is further processed by MoE to more efficiently leverage both VLMs. 

mechanism that dynamically routes shared tokens between the two VLM experts: 

MoE( _x_ ) = _w_ left _·_ FFNleft( _x_ ) + (1 _− w_ left) _·_ FFNright( _x_ ) _._ (3) 

For calculating _w_ left, we add a linear layer that takes the embedding as input and outputs the weights via a softmax function. For other components like Projection _,_ LayerNorm, we implement an outputaveraging strategy inspired by task arithmetic (Tang et al., 2024). By processing inputs through both backbones and averaging their outputs, we functionally simulate a shared layer without physically merging parameters (see Figure 3b center). This efficient design reduces VRAM usage by 21%, enabling training with a batch size of 8 on a single 40 GB GPU. 

**Attention re-weighting.** A potential side effect of introducing new arm-specific tokens is that the model’s learned attention patterns can be disrupted, shifting focus away from the pretrained shared modalities. To mitigate this and preserve the valuable pretrained knowledge, we re-scale the attention scores for the shared modality (Algorithm 4). This maintains pretrained modality importance, allowing the model to bypass an initial adaptation phase and focus directly on the target task—a benefit evidenced by a lower initial loss and converged loss during fine-tuning. 

# 5 EXPERIMENTS 

In this paper, we propose TwinVLA to achieve strong bimanual manipulation performance with minimal bimanual data by fully leveraging a single-arm VLA pretrained on abundant single-arm data. Our empirical studies aim to answer the following questions: 

- How does TwinVLA compare to state-of-the-art methods across diverse bimanual tasks, without any bimanual pretraining (Sections 5.2 and 5.3)? 

- How quickly can TwinVLA adapt to new bimanual tasks (Section 5.4)? 

- Does TwinVLA retain core VLA properties—language-following and robustness to unseen scenes and instructions (Sections 5.5 and 5.6)? 

- How much does each key design choice contribute to overall performance (Section 5.7)? 

## 5.1 COMPARED METHODS 

We evaluate TwinVLA against three bimanual manipulation policies, each representing a different point in the design space. 

- **RDT-1B** (Liu et al., 2024): This serves as our direct baseline. With a comparable size(1 _._ 2B vs. TwinVLA’s 1 _._ 3B parameters), it represents the standard monolithic approach that requires 

6 

Published as a conference paper at ICLR 2026 


Figure 4: **Experimental setups.** (a) We evaluate TwinVLA on five real-world bimanual tasks using an Anubis robot. (b) We further analyze TwinVLA on a large suite of simulation tasks: 5 tasks in Tabletop-Sim and 50 tasks in RoboTwin 2.0. 

substantially larger resources ( _∼_ 2,400h data, _∼_ 1,440 H100 days vs. _∼_ 800h single-arm data, _∼_ 25 H100 days). 

- **_π_ 0** (Black et al., 2024): We include this as an upper-bound, as this is 3 _._ 3B-parameter VLA trained on over 10K hours of proprietary robot data. Our goal is to assess how closely TwinVLA can approach this performance ceiling with far greater efficiency. 

- **Diffusion Policy (DP)** (Chi et al., 2024a): This is a strong baseline method in low-data regime with 271M parameters, used to demonstrate the crucial benefits of pretraining. 


Figure 5: **Success rates on real-world tasks.** TwinVLA outperforms RDT-1B and DP on average. Moreover, TwinVLA shows comparable performance with _π_ 0 while trained only on target data. 

## 5.2 REAL-WORLD EXPERIMENTS 

**Environment.** For real-world experiments, we use a dual-arm robot, Anubis (Kang et al., 2025), as shown in Figure 4a. Anubis has two 6 DoF arms with parallel-jaw grippers. The robot is equipped with two wrist-mounted cameras and a single ego-centric view camera. 

**Tasks.** We design five long-horizon tabletop manipulation tasks, which require careful coordination and accurate motions: `Fold towel` , `Extract hexkey` , `Carrot to bag` , `Brush to dustpan` , and `Take towel off` , and one task set, `Put X into pot` . We collect 50 episodes for each task using absolute EEF control. Each method is fine-tuned for each task and evaluated with 20 rollouts. 

**Results.** As presented in Figure 5, our model, TwinVLA, significantly outperforms RDT-1B. This achievement is remarkable considering the data disparity: TwinVLA is pretrained on just _∼_ 800h of single-arm data, in contrast to RDT-1B’s usage of a _∼_ 2,400h dataset mixed with bimanual trajectories, which highlights the data efficiency of our approach. While DP’s low performance confirms the necessity of pretraining, _π_ 0 achieved the highest overall performance with significantly higher costs. 

7 

Published as a conference paper at ICLR 2026 


Figure 6: **Average success rates for diverse bimanual tasks.** Despite being pretrained solely on single-arm datasets, **TwinVLA** outperforms other methods except _π_ 0. 

## 5.3 SIMULATION EXPERIMENTS 

**RoboTwin 2.0.** We use the RoboTwin 2.0 benchmark (Chen et al., 2025a), consisting of 50 bimanual tasks. Adhering to the official evaluation protocol, we fine-tune a model per task with 50 generated demonstrations and perform 100 test rollouts under both “Easy” and “Hard” settings. For Easy tasks, test scenes match the training data, but the instructions are novel. The Hard tasks introduce variations in texture, object position, and height. For compared methods, we use the results reported from RoboTwin 2.0 (Chen et al., 2025a). 

**Tabletop-Sim.** To assess dexterous scenarios beyond tasks in RoboTwin, we develop Tabletop-Sim<sup>1</sup> , a tabletop simulation environment based on `dm_control` (Tunyasuvunakool et al., 2020) and assets from ALOHA2 (Team et al., 2024) and GSO object dataset (Downs et al., 2022). We design 5 representative tasks that require precise bimanual coordination. Specifically, we define four singletasks and one multi-task: `dish-drainer` , `handover-box` , `shoes-table` , `lift-box` , and `put X box into Y pot` . In the “Hard” tasks, we vary background textures and objects. We collect 50 episodes on each task using absolute EEF control, and fine-tune a model per task, and perform 500 evaluation rollouts for both “Easy” and “Hard” settings. 

**Results.** The results in Figure 6 show the average success rates of TwinVLA and compared methods. DP, trained from scratch, shows the worst performance, highlighting the importance of pretraining. Once again, we observe that TwinVLA outperforms RDT-1B in most scenarios, except for the RoboTwin Hard tasks, and achieves comparable performance with _π_ 0 by effectively leveraging single-arm data and modularity of bimanual manipulation. Notably, in Tabletop-Sim Easy tasks, TwinVLA even outperforms _π_ 0, which is trained on an extensive corpus of high-quality bimanual pretraining data. This demonstrates TwinVLA’s advantages in scenarios demanding higher dexterity and significant bimanual coordination. 

## 5.4 DATA EFFICIENCY 

TwinVLA exhibits data efficiency in two key aspects: pretraining and fine-tuning. For pretraining, it is efficient because it does not require supplemental bimanual data. For fine-tuning, it learns new tasks rapidly because its structural inductive bias facilitates the efficient transfer and application of its pretrained single-arm knowledge. We validate this efficiency in TabletopSim Easy environment, comparing model’s average success rates with varying amounts of demonstration data. As illustrated in Figure 7, TwinVLA exhibits a steep learning curve. Despite a modest start with 20 demonstrations, it quickly surpasses the performance of RDT with just 50 demonstrations, highlighting its exceptional data efficiency. 


Figure 7: **Average success rates on the Tabletop-Sim Easy tasks.** Models are evaluated after finetuning with 20, 35, and 50 demonstrations. 

> 1Our simulation setup is similar to the concurrent work Aloha-Sim, released by Google DeepMind (Google DeepMind, 2025). 

8 

Published as a conference paper at ICLR 2026 

## 5.5 POLICY ROBUSTNESS 

One of the advantages of VLAs is their robustness to unseen situations and novel language instructions, thanks to pretraining. As shown in Figure 6, TwinVLA outperforms RDT-1B by 3 _._ 3% even in the Hard setup of Tabletop-Sim, which involves different textures and objects. 

The RoboTwin benchmark, both in the Easy and Hard setups, uses evaluation language instructions that are unseen during training. Here, TwinVLA again shows 7 _._ 48% better performance than RDT-1B in the Easy setup. Although TwinVLA’s performance on the RoboTwin Hard tasks is 3 _._ 72% lower than that of RDT-1B, it still outperforms a non-pretrained Diffusion policy by 9 _._ 38%. This result demonstrates that TwinVLA possesses sufficient robustness as a bimanual VLA, even without being pretrained on large-scale bimanual manipulation data. 

Table 1: Comparison of success rates for the `Fold towel` task in challenging scenes. 

|Model|Low light|With distractors|
|---|---|---|
|RDT|15.0%|15.0%|
|_π_0|40.0%|**60.0%**|
|**TwinVLA**|**45.0%**|25.0%|


In Table 1, we additionally compared success rates in unseen real-world settings (see Figure 13)—specifically low-light and distractor-heavy environments—using the `Fold towel` task. TwinVLA is robust to lighting changes but less effective with distractors. Meanwhile, _π_ 0 works robustly in both cases, and RDT-1B achieves the lowest success rates. 

## 5.6 LANGUAGE FOLLOWING EVALUATIONS 

A known challenge is that fine-tuning VLMs on robotic data can degrade their ability to faithfully follow nuanced instructions. We therefore evaluate how effectively our model preserves this core capability in a multi-task setting. We evaluated the “ `Put X into pot` ” task across both simulation and real-world settings. As observed in Figure 8a, TwinVLA outperforms both RDT-1B and _π_ 0. We believe this performance stems from effectively preserving the knowledge acquired during single-arm pretraining through careful fine-tuning. 


Figure 8: **Language following task and ablation results.** (a) We evaluate average success rates on the language following tasks in the real world and Tabletop-Sim. (b) Ablation studies in the real world and Tabletop-Sim Easy tasks. 

## 5.7 ABLATIONS 

In this section, we conduct a sequential ablation study to analyze the cumulative impact of our key design choices on performance. Starting from the full TwinVLA model, we progressively remove each component in a specific order: first Attention Re-weighting, followed by MoE integration, and finally Joint Attention. This method reveals how performance degrades as each component of our architecture is stripped away. The results on our real-world and Tabletop-Sim Easy tasks are reported in Figure 8b. 

**Attention re-weighting.** Removing the attention re-weighting mechanism ( _w/o Re-weighting_ ) increased the initial fine-tuning loss by **40%** and decreased final performance by **1.1%** and **4.0%** in simulation and real world, respectively. This demonstrates that our re-weighting strategy successfully mitigates the input distribution shift between pretraining and fine-tuning. 

9 

Published as a conference paper at ICLR 2026 

**MoE integration.** Building on the previous ablation, we next remove the MoE integration ( _w/o MoE_ ). This additional change increased the token sequence length by **28%** and increased VRAM usage by **21%** , making VLA training more burdensome. Surprisingly, it also further decreases the success rate by **1.1%** and **5.0%** , suggesting that MoE integration eliminates redundant processing of shared inputs while maintaining the performance. 

**Joint attention.** Lastly, removing the joint attention mechanism ( _w/o Joint attn_ ) causes the most significant additional performance drops of **4.0%** and **27.0%** in simulation and the real world, respectively. This impact is particularly pronounced in real-world tightly coupled bimanual tasks, confirming that joint attention is a critical mechanism for bimanual coordination. 

**Effect of single-arm pretraining.** As a separate, foundational experiment, we assess the role of pretraining by training a model from scratch without OXE dataset ( _Scratch_ ). This resulted in a **4.6%** performance drop in simulation and a stark **46.0%** in real world. This result confirms that effective cross-arm coordination is essential for bimanual manipulation and validates joint attention as the critical mechanism for achieving it in our model. 

**Twin structure.** While we have confirmed that joint attention effectively connects the two modules, a crucial question remains: how does this approach compare to a monolithic model that is inherently unified from the start? To answer this, we revisit our comparison against RDT-1B, a monolithic model of a comparable 1.2B parameter size. The results are telling: TwinVLA outperforms RDT-1B by **26.0%** in the real world, **5.0%** in simulation, and **21.8%** in language-following tasks on average. This provides strong evidence that the inductive bias from the Twin Structure itself is highly beneficial for bimanual manipulation, validating our design choice over a monolithic approach. 

# 6 LIMITATIONS 

Generalization remains limited due to the visual disparity of two arms, which differs from the singlearm pretraining distribution. Future research into mechanisms that prevent this could address data scarcity by integrating diverse data, while also improving the model explainability and the better generalization ability to unseen tasks. 

Moreover, we adopt absolute end-effector (EEF) pose control, as its embodiment-agnostic nature facilitates single-arm transfer, unlike DOF-specific joint positions. Future exploration of relative absolute actions (Chi et al., 2024b) or shared representations could further enhance transfer efficiency. 

# 7 CONCLUSION 

In this paper, we introduce TwinVLA, a data-efficient VLA model for bimanual manipulation. TwinVLA provides a new perspective on solving bimanual manipulation under scarce bimanual data by leveraging abundant single-arm datasets. From a small amount of bimanual demonstration data, TwinVLA learns to coordinate two copies of a SingleVLA pretrained on large-scale singlearm data via our proposed method. Through exhaustive experiments both in the real world and simulation, TwinVLA demonstrates its data-efficient learning of bimanual tasks compared to prior monolithic approaches. Beyond the bimanual setting, we believe this work serves as a blueprint for addressing inherent dataset imbalances across modalities. By illustrating how modular relationships can be exploited to bridge these data gaps, TwinVLA opens promising ways for other complex domains—such as mobile manipulation—thereby broadening the impact of large-scale robotic learning. 

## ACKNOWLEDGMENTS 

This project was supported in part by Microsoft Research Asia and the Microsoft Accelerate Foundation Models Research (AFMR) grant program. This research was also supported by the Institute of Information & Communications Technology Planning & Evaluation (IITP) grants funded by the Korean Government (MSIT) (RS-2020-II201361, Artificial Intelligence Graduate School Program (Yonsei University); RS-2024-00436680, Global Research Support Program in the Digital Field Program), the Alchemist Project (RS-2024-00432143) funded by the Ministry of Trade, Industry & Energy (MOTIE, Korea), and the Electronics and Telecommunications Research Institute (ETRI) 

10 

Published as a conference paper at ICLR 2026 

grant funded by the Korean government (26ZR1100, Research on Intelligent Industrial Convergence). LG Electronics provided the Anubis robot, which was used for the experiments. The authors would like to thank Byeongjin Kang for the assistance with the preliminary experiments. 

# REFERENCES 

- N. Ahmed, T. Natarajan, and K.R. Rao. Discrete cosine transform. _IEEE Transactions on Computers_ , C-23(1):90–93, 1974. doi: 10.1109/T-C.1974.223784. 

- Yahav Avigal, Lars Berscheid, Tamim Asfour, Torsten Kröger, and Ken Goldberg. Speedfolding: Learning efficient bimanual folding of garments. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pp. 1–8. IEEE, 2022. 

- Shikhar Bahl, Russell Mendonca, Lili Chen, Unnat Jain, and Deepak Pathak. Affordances from human videos as a versatile representation for robotics. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023. 

- Suneel Belkhale, Yuchen Cui, and Dorsa Sadigh. Hydra: Hybrid robot actions for imitation learning. In _Conference on Robot Learning_ , 2023. 

- Christian Bersch, Benjamin Pitzer, and Sören Kammel. Bimanual robotic cloth manipulation for laundry folding. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pp. 1413–1419. IEEE, 2011. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. In _Robotics: Science and Systems_ , 2024. 

- Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, brian ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. $\pi_{0.5}$: a visionlanguage-action model with open-world generalization. In _Conference on Robot Learning_ , 2025. URL `https://openreview.net/forum?id=vlhoswksBO` . 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Kuang-Huei Lee, Sergey Levine, Yao Lu, Utsav Malla, Deeksha Manjunath, Igor Mordatch, Ofir Nachum, Carolina Parada, Jodilyn Peralta, Emily Perez, Karl Pertsch, Jornell Quiambao, Kanishka Rao, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Kevin Sayed, Jaspiar Singh, Sumedh Sontakke, Austin Stone, Clayton Tan, Huong Tran, Vincent Vanhoucke, Steve Vega, Quan Vuong, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-1: Robotics transformer for real-world control at scale. In _Robotics: Science and Systems_ , 2022. 

- Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, and Thomas Wolf. Lerobot: State-of-the-art machine learning for real-world robotics in pytorch. `https: //github.com/huggingface/lerobot` , 2024. 

- Lawrence Yunliang Chen, Simeon Adebola, and Ken Goldberg. Berkeley UR5 demonstration dataset. `https://sites.google.com/view/berkeley-ur5/home` , 2023. 

- Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Qiwei Liang, Zixuan Li, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025a. 

11 

Published as a conference paper at ICLR 2026 

- Zhe Chen, Weiyun Wang, Yue Cao, Yangzhou Liu, Zhangwei Gao, Erfei Cui, Jinguo Zhu, Shenglong Ye, Hao Tian, Zhaoyang Liu, Lixin Gu, Xuehui Wang, Qingyun Li, Yimin Ren, Zixuan Chen, Jiapeng Luo, Jiahao Wang, Tan Jiang, Bo Wang, Conghui He, Botian Shi, Xingcheng Zhang, Han Lv, Yi Wang, Wenqi Shao, Pei Chu, Zhongying Tu, Tong He, Zhiyong Wu, Huipeng Deng, Jiaye Ge, Kai Chen, Kaipeng Zhang, Limin Wang, Min Dou, Lewei Lu, Xizhou Zhu, Tong Lu, Dahua Lin, Yu Qiao, Jifeng Dai, and Wenhai Wang. Expanding performance boundaries of open-source multimodal models with model, data, and test-time scaling. _CoRR_ , 2025b. 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 2024a. 

- Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots. In _Robotics: Science and Systems_ , 2024b. 

- Zichen Jeff Cui, Yibin Wang, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. From play to policy: Conditional behavior generation from uncurated robot data. In _International Conference on Learning Representations_ , 2023. 

- Shivin Dass, Jullian Yapeter, Jesse Zhang, Jiahui Zhang, Karl Pertsch, Stefanos Nikolaidis, and Joseph J. Lim. Clvr jaco play dataset, 2023. URL `https://github.com/clvrai/clvr_jaco_ play_dataset` . 

- Ria Doshi, Homer Rich Walke, Oier Mees, Sudeep Dasari, and Sergey Levine. Scaling crossembodied learning: One policy for manipulation, navigation, locomotion and aviation. In _Conference on Robot Learning_ , 2024. 

- Laura Downs, Anthony Francis, Nate Koenig, Brandon Kinman, Ryan Hickman, Krista Reymann, Thomas B McHugh, and Vincent Vanhoucke. Google scanned objects: A high-quality dataset of 3d scanned household items. In _IEEE International Conference on Robotics and Automation_ , pp. 2553–2560. IEEE, 2022. 

- Zipeng Fu, Tony Z. Zhao, and Chelsea Finn. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. In _Conference on Robot Learning_ , 2024. 

- Koffivi Fidèle Gbagbe, Miguel Altamirano Cabrera, Ali Alabbas, Oussama Alyunes, Artem Lykov, and Dzmitry Tsetserukou. Bi-vla: Vision-language-action model-based system for bimanual robotic dexterous manipulations. In _IEEE International Conference on Systems, Man, and Cybernetics (SMC)_ , pp. 2864–2869, 2024. doi: 10.1109/SMC54092.2024.10831380. 

- Google DeepMind. Aloha-sim. `https://github.com/google-deepmind/aloha_sim` , 2025. Accessed: 2025-10-24. 

- Markus Grotz, Mohit Shridhar, Tamim Asfour, and Dieter Fox. Peract2: Benchmarking and learning for robotic bimanual manipulation tasks. _CoRR_ , abs/2407.00278, 2024. URL `https://doi.org/ 10.48550/arXiv.2407.00278` . 

- Minho Heo, Youngwoon Lee, Doohyun Lee, and Joseph J. Lim. Furniturebench: Reproducible real-world benchmark for long-horizon complex manipulation. In _Robotics: Science and Systems_ , 2023. 

- Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. BC-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , 2021. 

- Zhenyu Jiang, Yuqi Xie, Kevin Lin, Zhenjia Xu, Weikang Wan, Ajay Mandlekar, Linxi Jim Fan, and Yuke Zhu. Dexmimicgen: Automated data generation for bimanual dexterous manipulation via imitation learning. In _IEEE International Conference on Robotics and Automation_ , pp. 16923– 16930, 2025. doi: 10.1109/ICRA55743.2025.11127809. 

12 

Published as a conference paper at ICLR 2026 

- Taewoong Kang, Joonyoung Kim, Shady Nasrat, Dongwoon Song, Gijae Ahn, Minseong Jo, Seonil Lee, and Seung-Joon Yi. Anubis: A compact, low-cost, compliant humanoid mobile manipulation robot. In _IEEE-RAS International Conference on Humanoid Robots_ , 2025. URL `https://ras. papercept.net/conferences/scripts/rtf/ICHR25_ContentListWeb_2.html` . 

- Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, Peter David Fagan, Joey Hejna, Masha Itkina, Marion Lepert, Yecheng Jason Ma, Patrick Tree Miller, Jimmy Wu, Suneel Belkhale, Shivin Dass, Huy Ha, Arhan Jain, Abraham Lee, Youngwoon Lee, Marius Memmel, Sungjae Park, Ilija Radosavovic, Kaiyuan Wang, Albert Zhan, Kevin Black, Cheng Chi, Kyle Beltran Hatch, Shan Lin, Jingpei Lu, Jean Mercat, Abdul Rehman, Pannag R Sanketi, Archit Sharma, Cody Simpson, Quan Vuong, Homer Rich Walke, Blake Wulfe, Ted Xiao, Jonathan Heewon Yang, Arefeh Yavary, Tony Z. Zhao, Christopher Agia, Rohan Baijal, Mateo Guaman Castro, Daphne Chen, Qiuyu Chen, Trinity Chung, Jaimyn Drake, Ethan Paul Foster, Jensen Gao, David Antonio Herrera, Minho Heo, Kyle Hsu, Jiaheng Hu, Donovon Jackson, Charlotte Le, Yunshuang Li, Kevin Lin, Roy Lin, Zehan Ma, Abhiram Maddukuri, Suvir Mirchandani, Daniel Morton, Tony Nguyen, Abigail O’Neill, Rosario Scalise, Derick Seale, Victor Son, Stephen Tian, Emi Tran, Andrew E. Wang, Yilin Wu, Annie Xie, Jingyun Yang, Patrick Yin, Yunchu Zhang, Osbert Bastani, Glen Berseth, Jeannette Bohg, Ken Goldberg, Abhinav Gupta, Abhishek Gupta, Dinesh Jayaraman, Joseph J Lim, Jitendra Malik, Roberto Martín-Martín, Subramanian Ramamoorthy, Dorsa Sadigh, Shuran Song, Jiajun Wu, Michael C. Yip, Yuke Zhu, Thomas Kollar, Sergey Levine, and Chelsea Finn. Droid: A large-scale in-the-wild robot manipulation dataset. In _Robotics: Science and Systems_ , 2024. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. OpenVLA: An open-source vision-language-action model. In _Conference on Robot Learning_ , 2024. 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. In _Robotics: Science and Systems_ , 2025. 

- Masato Kobayashi and Thanpimon Buamanee. Bi-vla: Bilateral control-based imitation learning via vision-language fusion for action generation, 2025. URL `https://arxiv.org/abs/2509. 18865` . 

- Andrew Choong-Won Lee, Ian Chuang, Ling-Yuan Chen, and Iman Soltani. InterACT: Interdependency aware action chunking with hierarchical attention transformers for bimanual manipulation. In _Conference on Robot Learning_ , 2024. URL `https://openreview.net/forum?id= lKGRPJFPCM` . 

- Youngwoon Lee, Jingyun Yang, and Joseph J. Lim. Learning to coordinate manipulation skills via skill behavior diversification. In _International Conference on Learning Representations_ , 2020. 

- Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, Xiaofan Wang, Bei Liu, Jianlong Fu, Jianmin Bao, Dong Chen, Yuanchun Shi, Jiaolong Yang, and Baining Guo. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _CoRR_ , 2024a. 

- Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. In _International Conference on Learning Representations_ , 2024b. 

- Zhiqi Li, Guo Chen, Shilong Liu, Shihao Wang, Vibashan VS, Yishen Ji, Shiyi Lan, Hao Zhang, Yilin Zhao, Subhashree Radhakrishnan, Nadine Chang, Karan Sapra, Amala Sanjay Deshmukh, Tuomas Rintamaki, Matthieu Le, Ilia Karmanov, Lukas Voegtle, Philipp Fischer, De-An Huang, Timo Roman, Tong Lu, Jose M. Alvarez, Bryan Catanzaro, Jan Kautz, Andrew Tao, Guilin Liu, and Zhiding Yu. Eagle 2: Building post-training data strategies from scratch for frontier vision-language models. _CoRR_ , 2025. 

- Weixin Liang, Lili Yu, Liang Luo, Srinivasan Iyer, Ning Dong, Chunting Zhou, Gargi Ghosh, Mike Lewis, Wen tau Yih, Luke Zettlemoyer, and Xi Victoria Lin. Mixture-of-transformers: A sparse 

13 

Published as a conference paper at ICLR 2026 

and scalable architecture for multi-modal foundation models. In _Conference on Parsimony and Learning_ , 2024. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems_ , volume 36, pp. 44776–44791, 2023a. 

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. In _Advances in Neural Information Processing Systems_ , volume 36, pp. 34892–34916, 2023b. 

- Huihan Liu, Soroush Nasiriany, Lance Zhang, Zhiyao Bao, and Yuke Zhu. Robot learning on the job: Human-in-the-loop autonomy and learning during deployment. In _Robotics: Science and Systems_ , 2023c. 

- Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. In _International Conference on Learning Representations_ , 2024. 

- Guanxing Lu, Tengbo Yu, Haoyuan Deng, Season Si Chen, Yansong Tang, and Ziwei Wang. Anybimanual: Transferring unimanual policy for general bimanual manipulation. In _IEEE/CVF International Conference on Computer Vision_ , 2025. 

- Jianlan Luo, Charles Xu, Fangchen Liu, Liam Tan, Zipeng Lin, Jeffrey Wu, Pieter Abbeel, and Sergey Levine. Fmb: A functional manipulation benchmark for generalizable robotic learning. _The International Journal of Robotics Research_ , 44(4):592–606, 2025. 

- Russell Mendonca, Shikhar Bahl, and Deepak Pathak. Structured world models from human videos. _Conference on Robot Learning_ , 2023. 

- Yao Mu, Tianxing Chen, Zanxin Chen, Shijia Peng, Zhiqian Lan, Zeyu Gao, Zhixuan Liang, Qiaojun Yu, Yude Zou, Mingkun Xu, Lunkai Lin, Zhiqiang Xie, Mingyu Ding, and Ping Luo. Robotwin: Dual-arm robot benchmark with generative digital twins. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 27649–27660, June 2025. 

- Soroush Nasiriany, Tian Gao, Ajay Mandlekar, and Yuke Zhu. Learning and retrieval from prior data for skill-based imitation learning. In _Conference on Robot Learning_ , 2022. 

- NVIDIA, Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi "Jim" Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. URL `https://arxiv.org/abs/2503.14734` . 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- Open X-Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, Andrew Wang, Andrey Kolobov, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Schölkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter Büchler, Dinesh Jayaraman, Dmitry Kalashnikov, 

14 

Published as a conference paper at ICLR 2026 

Dorsa Sadigh, Edward Johns, Ethan Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Felipe Vieira Frujeri, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guangwen Yang, Guanzhi Wang, Hao Su, Hao-Shu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homanga Bharadhwaj, Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan Schneider, Jasmine Hsu, Jay Vakil, Jeannette Bohg, Jeffrey Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun Yang, Jitendra Malik, João Silvério, Joey Hejna, Jonathan Booher, Jonathan Tompson, Jonathan Yang, Jordi Salvador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran Lekkala, Kirsty Ellis, Krishan Rana, Krishnan Srinivasan, Kuan Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen, Lerrel Pinto, Li Fei-Fei, Liam Tan, Linxi "Jim" Fan, Lionel Ott, Lisa Lee, Luca Weihs, Magnum Chen, Marion Lepert, Marius Memmel, Masayoshi Tomizuka, Masha Itkina, Mateo Guaman Castro, Max Spero, Maximilian Du, Michael Ahn, Michael C. Yip, Mingtong Zhang, Mingyu Ding, Minho Heo, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Ning Liu, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Osbert Bastani, Pannag R Sanketi, Patrick "Tree" Miller, Patrick Yin, Paul Wohlhart, Peng Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet, Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Mart’in-Mart’in, Rohan Baijal, Rosario Scalise, Rose Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Shan Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham Sonawani, Shubham Tulsiani, Shuran Song, Sichun Xu, Siddhant Haldar, Siddharth Karamcheti, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Subramanian Ramamoorthy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung, Vidhi Jain, Vikash Kumar, Vincent Vanhoucke, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiangyu Chen, Xiaolong Wang, Xinghao Zhu, Xinyang Geng, Xiyuan Liu, Xu Liangwei, Xuanlin Li, Yansong Pang, Yao Lu, Yecheng Jason Ma, Yejin Kim, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yongqiang Dou, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao, Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang, Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff Cui, Zichen Zhang, Zipeng Fu, and Zipeng Lin. Open X-Embodiment: Robotic learning datasets and RT-X models. In _IEEE International Conference on Robotics and Automation_ , 2024. 

- William S. Peebles and Saining Xie. Scalable diffusion models with transformers. In _IEEE/CVF International Conference on Computer Vision_ , pp. 4172–4182, 2023. 

- Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. In _Robotics: Science and Systems_ , 2025. 

- Gabriel Quere, Annette Hagengruber, Maged Iskandar, Samuel Bustamante, Daniel Leidner, Freek Stulp, and Joern Vogel. Shared Control Templates for Assistive Robotics. In _IEEE International Conference on Robotics and Automation_ , Paris, France, 2020. 

- Erick Rosete-Beas, Oier Mees, Gabriel Kalweit, Joschka Boedecker, and Wolfram Burgard. Latent plans for task agnostic offline reinforcement learning. In _Conference on Robot Learning_ , 2022. 

- Norihiro Sadato, Yoshiharu Yonekura, Atsuo Waki, Hiroki Yamada, and Yasushi Ishii. Role of the supplementary motor area and the right premotor cortex in the coordination of bimanual finger movements. _Journal of Neuroscience_ , 17(24):9667–9674, 1997. ISSN 0270-6474. doi: 10.1523/JNEUROSCI.17-24-09667.1997. URL `https://www.jneurosci.org/content/17/ 24/9667` . 

15 

Published as a conference paper at ICLR 2026 

- Nur Muhammad Mahi Shafiullah, Anant Rai, Haritheja Etukuru, Yiqian Liu, Ishan Misra, Soumith Chintala, and Lerrel Pinto. On bringing robots home, 2023. 

- Rutav Shah, Roberto Martín-Martín, and Yuke Zhu. Mutex: Learning unified policies from multimodal task specifications. In _Conference on Robot Learning_ , 2023. URL `https://openreview. net/forum?id=PwqiqaaEzJ` . 

- Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. In _International Conference on Learning Representations_ , 2017. URL `https://openreview.net/ forum?id=B1ckMDqlg` . 

- Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiver-actor: A multi-task transformer for robotic manipulation. In _Conference on Robot Learning_ , 2022. 

- Sotiris Stavridis and Zoe Doulgeri. Bimanual assembly of two parts with relative motion generation and task related optimization. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pp. 7131–7136. IEEE, 2018. 

- Stephan P. Swinnen. Intermanual coordination: From behavioural principles to neural-network interactions. _Nature Reviews Neuroscience_ , 3(5):348–359, 2002. doi: 10.1038/nrn807. 

- Anke Tang, Li Shen, Yong Luo, Nan Yin, Lefei Zhang, and Dacheng Tao. Merging multi-task models via weight-ensembling mixture of experts. In _International Conference on Machine Learning_ , 2024. 

- ALOHA 2 Team, Jorge Aldaco, Travis Armstrong, Robert Baruch, Jeff Bingham, Sanky Chan, Kenneth Draper, Debidatta Dwibedi, Chelsea Finn, Pete Florence, Spencer Goodrich, Wayne Gramlich, Torr Hage, Alexander Herzog, Jonathan Hoech, Thinh Nguyen, Ian Storz, Baruch Tabanpour, Leila Takayama, Jonathan Tompson, Ayzaan Wahid, Ted Wahrburg, Sichun Xu, Sergey Yaroshenko, Kevin Zakka, and Tony Z. Zhao. Aloha 2: An enhanced low-cost hardware for bimanual teleoperation, 2024. URL `https://arxiv.org/abs/2405.02292` . 

- Saran Tunyasuvunakool, Alistair Muldal, Yotam Doron, Siqi Liu, Steven Bohez, Josh Merel, Tom Erez, Timothy Lillicrap, Nicolas Heess, and Yuval Tassa. dm_control: Software and tasks for continuous control. _Software Impacts_ , 6:100022, 2020. ISSN 2665-9638. doi: https://doi.org/ 10.1016/j.simpa.2020.100022. URL `https://www.sciencedirect.com/science/article/ pii/S2665963820300099` . 

- Jörn Vogel, Annette Hagengruber, Maged Iskandar, Gabriel Quere, Ulrike Leipscher, Samuel Bustamante, Alexander Dietrich, Hannes Hoeppner, Daniel Leidner, and Alin Albu-Schäffer. Edan - an emg-controlled daily assistant to help people with physical disabilities. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2020. 

- Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe Hansen-Estruch, Quan Vuong, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , 2023. 

- Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Yang Fan, Kai Dang, Mengfei Du, Xuancheng Ren, Rui Men, Dayiheng Liu, Chang Zhou, Jingren Zhou, and Junyang Lin. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _CoRR_ , 2024. 

- Philipp Wu, Yide Shentu, Zhongke Yi, Xingyu Lin, and Pieter Abbeel. Gello: A general, lowcost, and intuitive teleoperation framework for robot manipulators. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pp. 12156–12163. IEEE, 2024. 

- Fan Xie, Alexander Chowdhury, M De Paolis Kaluza, Linfeng Zhao, Lawson Wong, and Rose Yu. Deep imitation learning for bimanual robotic manipulation. In _Advances in Neural Information Processing Systems_ , volume 33, pp. 2327–2337, 2020. 

- Sudhir Pratap Yadav, Rajendra Nagar, and Suril V. Shah. Learning vision-based robotic manipulation tasks sequentially in offline reinforcement learning settings. _Robotica_ , 42(6):1715–1730, 2024. 

16 

Published as a conference paper at ICLR 2026 

- Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _Robotics: Science and Systems_ , 2023. 

- Yi Zhou, Connelly Barnes, Jingwan Lu, Jimei Yang, and Hao Li. On the continuity of rotation representations in neural networks. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 5738–5746, 2019. doi: 10.1109/CVPR.2019.00589. 

- Xinghao Zhu, Ran Tian, Chenfeng Xu, Mingxiao Huo, Wei Zhan, Masayoshi Tomizuka, and Mingyu Ding. Fanuc manipulation: A dataset for learning-based manipulation with fanuc mate 200id robot. `https://sites.google.com/berkeley.edu/fanuc-manipulation` , 2023. 

- Yifeng Zhu, Abhishek Joshi, Peter Stone, and Yuke Zhu. Viola: Imitation learning for vision-based manipulation with object proposal priors. _Conference on Robot Learning_ , 2022a. 

- Yifeng Zhu, Peter Stone, and Yuke Zhu. Bottom-up skill discovery from unsegmented demonstrations for long-horizon robot manipulation. _IEEE Robotics and Automation Letters_ , 7(2):4126–4133, 2022b. doi: 10.1109/LRA.2022.3146589. 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

17 

Published as a conference paper at ICLR 2026 

# APPENDIX 

A SINGLEVLA: EFFICIENT SINGLE-ARM POLICY DESIGN AND PRETRAINING 


Figure 9: **Overview of SingleVLA architecture design and pretraining method.** 

This section presents the design of the SingleVLA _π_ single. While SingleVLA follows established VLA conventions, our key novelty is a duplication strategy that enables the construction of TwinVLA. Prior 7B-scale models (Kim et al., 2024; 2025; Li et al., 2024a) are prohibitively large for such duplication, motivating a more efficient, lightweight Eagle2-1B (Li et al., 2025) based SingleVLA (Fig. 9). Since we do not use language head, the overall model size became 0.8B. To acquire generalizable knowledge, we pretrain SingleVLA on a _∼_ 800h subset of the OXE mix, enabling transfer across diverse environments and embodiments. Pretraining ran for **120k** steps and took about **5 days** on a cluster with **5** _×_ **H100** GPUs. 

To ensure effective transfer to bimanual manipulation, it is crucial to choose an appropriate _action space_ . Heterogeneous joint configurations across robots induce incompatible action spaces and complicate joint training. Prior work mitigates this with robot-specific decoders or high-dimensional zero-padded spaces (NVIDIA et al., 2025; Doshi et al., 2024; Octo Model Team et al., 2024; Black et al., 2024; Liu et al., 2024). Instead, we convert all actions into absolute end-effector (EEF) poses, providing a consistent, semantically meaningful representation across robots that naturally extends to bimanual control. For rotation, we adopt a 6D representation (Zhou et al., 2019), which is well suited for neural network learning. 

## A.1 PRETRAINING 

SingleVLA is pretrained on an OXE subset ( _∼_ 800h); dataset composition and sampling rates appear in Table 2. We adopt the dataset loader from the OpenVLA (Kim et al., 2024) codebase and apply sampling according to the designated weights. Because some datasets (e.g., Kuka and BC-Z) include failed trajectories, we pre-process to retain only successful ones. Regarding the action space, we convert all actions to absolute EEF control with 6D rotations. We deliberately selected an absolute representation to mitigate the error accumulation and drift issues often amplified in high-frequency bimanual control. Unlike absolute joint positions, however, absolute EEF poses preserve the embodiment-agnostic property required for heterogeneous pretraining. We define these poses relative to the robot’s base frame, resulting in a 10-Dimensional action space. We further apply _frequency matching_ as described below. 

**Frequency matching.** Robotic datasets differ in control frequency, making fixed-length actionchunk prediction misaligned in real time. For example, a 20-step chunk spans _∼_ 7 seconds in RT-1 (Brohan et al., 2022) (3 Hz) but only _∼_ 1 _._ 3 seconds in DROID (Khazatsky et al., 2024) (15 Hz). Mixing low-frequency data like OXE (Open X-Embodiment Collaboration et al., 2024) with highfrequency datasets can degrade pretraining quality. Inspired by _π_ 0-FAST (Pertsch et al., 2025), which uses DCT (Ahmed et al., 1974) to map 1-second actions into a consistent space, we perform frequency matching via interpolation: all datasets are resampled to 20 Hz, improving temporal alignment and transfer to high-frequency bimanual tasks. 

18 

Published as a conference paper at ICLR 2026 

Table 2: **SingleVLA pretraining datasets and sampling percentages.** 

|**Dataset**|**Sample Percentage**|
|---|---|
|RT-1 (Brohan et al., 2022)|24_._49%|
|Kuka (filtered) (Yadav et al., 2024)|12_._40%|
|BridgeV2 (Walke et al., 2023)|13_._74%|
|Taco Play (Rosete-Beas et al., 2022)|3_._10%|
|Jaco Play (Dass et al., 2023)|0_._50%|
|Viola (Zhu et al., 2022a)|1_._00%|
|Berkeley Autolab UR5 (Chen et al., 2023)|1_._28%|
|Stanford Hydra (Belkhale et al., 2023)|4_._73%|
|Austin Buds (Zhu et al., 2022b)|0_._22%|
|NYU Franka Play (Cui et al., 2023)|0_._88%|
|FurnitureBench (Heo et al., 2023)|2_._40%|
|Austin Sailor (Nasiriany et al., 2022)|2_._33%|
|Austin Sirius (Liu et al., 2023c)|1_._84%|
|DLR EDAN (shared control) (Vogel et al., 2020; Quere et al., 2020)|0_._05%|
|UT Austin Mutex (Shah et al., 2023)|2_._38%|
|Berkeley FANUC manipulation (Zhu et al., 2023)|0_._82%|
|CMU Stretch (Bahl et al., 2023; Mendonca et al., 2023)|0_._16%|
|BC-Z (filtered) (Jang et al., 2021)|7_._90%|
|FMB (Luo et al., 2025)|7_._40%|
|Dobb-E (Shafiullah et al., 2023)|1_._50%|
|DROID (Khazatsky et al., 2024)|10_._70%|


## A.2 HYPERPARAMETERS AND COMPUTE 

Table 3: **Key hyperparameters for TWINVLA training.** 

|**Hyperparameter**|**SingleVLA**|**TwinVLA**|
|---|---|---|
|Global batch size|256|8|
|Precision|BF16|BF16|
|Gradient clipping (_L_2)|1_._0|1_._0|
|Learning rate|1_×_10<sup>_−_4</sup>|1_×_10<sup>_−_4</sup>|
|LR scheduler|cosine|cosine|
|Warm-up ratio|0_._01|0_._05|
|Total steps|120k|100k|
|Optimizer|AdamW|AdamW|
|Weight decay|1_×_10<sup>_−_5</sup>|1_×_10<sup>_−_5</sup>|
|Adam_ϵ_|1_×_10<sup>_−_8</sup>|1_×_10<sup>_−_8</sup>|
|Vision backbone frozen|true|true|
|Image augmentation|true|false|
|Action chunk size|20|20|
|Sampling step|10|10|


Table 3 summarizes training hyperparameters for SingleVLA and TwinVLA. SingleVLA pretraining used 5 _×_ H100 GPUs for about 5 days. TwinVLA fine-tuning used 1 _×_ L40S GPU for about 2 days. 

## A.3 SINGLEVLA VLM ABLATION 

We validate SingleVLA’s VLM choice in the LIBERO (Liu et al., 2023a) environment using several VLMs. The LIBERO actions are converted to absolute EEF 6D control. Due to computational limits, we directly fine-tune the pretrained VLM checkpoints on LIBERO (i.e., without additional pretraining on LIBERO). Each model is evaluated with 500 rollouts per task suite under identical random seeds. Results are shown in Table 4. 

19 

Published as a conference paper at ICLR 2026 

Table 4: **Performance of different VLMs on LIBERO.** 

|**VLM**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|---|
|Qwen2VL-2B (Wang et al., 2024)|80_._4%|88_._6%|83_._8%|43_._0%|73_._9%|
|InternVL2.5-1B (Chen et al., 2025b)|64_._6%|84_._8%|78_._4%|46_._2%|68_._5%|
|Eagle2-1B (Li et al., 2025)|73_._4%|85_._4%|90_._8%|46_._6%|**74**_._**0**%|


Although Qwen2VL is widely regarded as robust, Eagle2-1B achieves comparable or slightly better results while using roughly half the parameters and providing significantly faster inference. We therefore select **Eagle2-1B** as the VLM backbone for SingleVLA. 

Table 5: **Performance of pretrained SingleVLA on LIBERO.** 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Average**|
|---|---|---|---|---|---|
|SingleVLA (Eagle2-1B, no pretraining)|73_._4%|85_._4%|90_._8%|46_._6%|74_._0%|
|SingleVLA (pretrained)|**92**_._**4**%|**94**_._**5**%|**93**_._**5**%|**63**_._**7**%|**86**_._**0**%|
|OpenVLA (Kim et al., 2024)|84_._7%|88_._4%|79_._2%|53_._7%|76_._5%|
|Octo (Octo Model Team et al., 2024)|78_._9%|85_._7%|84_._6%|51_._1%|75_._1%|


After pretraining SingleVLA with Eagle2-1B, we fine-tune it on LIBERO to assess single-arm capability. As shown in Table 5, the pretrained SingleVLA substantially improves performance and even surpasses the 7B model OpenVLA, indicating that the learned single-arm policy is both effective and sufficiently strong to benefit the bimanual policy. 

# B TRAINING DETAILS 

Table 6: **Training hyperparameters for baseline models.** 

|**Method**|**# of params**|**Learning rate**|**Lr scheduler**|**Batch size**|**Training steps**|
|---|---|---|---|---|---|
|TwinVLA|1.3B|1e-4|cosine|8|100k|
|RDT-1B|1.2B|1e-4|constant|8|100k|
|DP|271M|2e-5|cosine|8|100k|
|_π_0|3.3B|2.5e-5|cosine|8|100k|


We use the official implementation of RDT-1B. Diffusion Policy and _π_ 0 are evaluated via the public LEROBOT release (Cadene et al., 2024), with two modifications for a fair comparison. First, the LEROBOT evaluation script normalized images differently from training; we corrected this to match the training pipeline. 

All models are fine-tuned with the same number of steps and batch size so that the total number of training samples is consistent across methods. For learning rates, we began with each model’s default and tuned within a similar compute budget. In practice, defaults worked well for DP and RDT-1B. For _π_ 0, we observed better final returns by slowing the cosine decay; we therefore extended the LR schedule from 30k to 100k steps. 

# C TWINVLA DETAILS 

## C.1 JOINT ATTENTION 

The joint attention in TwinVLA is fundamentally almost identical to the implementation in the Mixture-of-Transformers (MoT) (Liang et al., 2024), but we applied attention-reweighting (Section C.3). While MoT has transformers for text, image, and speech inputs, in TwinVLA, the inputs for the left and right arms correspond to these. 

20 

Published as a conference paper at ICLR 2026 

- **Algorithm 2** Joint Attention 1: **function** JOINTATTENTION( _{Qm}, {Km}, {Vm}, M_ ) 2: _Q, K, V ←_ Concatenate( _<u>{Qm}, {Km}, {Vm}</u>_ ) _▷_ Concatenate modality-specific Q, K, V 3: _S ←_ Softmax(( _QK_<sup>_⊤_</sup> _/_<sup>_~~√~~_</sup> _dk_ ) + _M_ ) _▷_ Apply causal joint mask M (Figure 3a) 4: _S ←_ ApplyReweighting( _S_ ) _▷_ Apply re-weighting (Algorithm 4) 5: _A ← S · V ▷_ Calculate output A 6: **return** _{Am} ←_ Split( _A_ ) _▷_ Split output _A_ into modality-specific _Am_ 7: **end function** 

Furthermore, MoT requires an operation to group mixed inputs by modality and then restore their original order. However, this process is unnecessary in TwinVLA because the inputs are fed in a fixed sequence: left arm, then right arm. The detailed computation process is shown in Algorithm 2. 

## C.2 MOE INTEGRATION 

To enable sharing of the shared inputs between the two-arm models, we duplicated the entire VLM transformer. This necessitates different strategies for sharing the FFNs and the other components. This section details the strategy used for each component of the transformer. 

**Feed-Forward Networks.** To share FFNs, we adopt the common approach of using a gating-based MoE. In standard MoE, multiple FFNs are included within a transformer, and a gating mechanism activates a subset for each input. In TwinVLA, the two VLMs act as distinct FFN experts. 

Because shared inputs (e.g., ego-centric views or language prompts) may have asymmetric relevance for each arm, the gating mechanism learns how much each FFN should contribute to processing the shared input. This approach is widely used and has been shown to improve training stability and preserve information more effectively than simple averaging (Shazeer et al., 2017). We computed _w_ left by applying a simple linear layer and softmax to the token embeddings. 

**Other Components.** Beyond FFNs, elements such as layer normalization and projection layers also require integration. For these, we apply task arithmetic (Tang et al., 2024), merging the two VLMs via simple parameter averaging with weight _λ_ = 0 _._ 5, elaborated Algorithm 3. This extends MoE-style computation to the full transformer architecture. 

**Algorithm 3** Integration of other components 

1: Let Projection _b_ be projection layer from each backbone _b ∈{_ left _,_ right _}_ . 2: Let LayerNorm _b_ be layernorm from each backbone _b ∈{_ left _,_ right _}_ . 3: **function** PROJ( _X_<sup>_m_</sup> ) 4: **if** _m_ = shared **then** 5: _F_<sup>_m_</sup> _←_ 0 _._ 5 _·_ (Projectionleft( _X_<sup>_m_</sup> ) + Projectionright( _X_<sup>_m_</sup> )) _▷_ Task arithmetic 6: **else** 7: _F_<sup>_m_</sup> _←_ Projection _m_ ( _X_<sup>_m_</sup> ) 8: **end if** 9: **return** _F_<sup>_m_</sup> 10: **end function** 11: 12: **function** NORM( _X_<sup>_m_</sup> ) 13: **if** _m_ = shared **then** 14: _F_<sup>_m_</sup> _←_ 0 _._ 5 _·_ (LayerNormleft( _X_<sup>_m_</sup> ) + LayerNormright( _X_<sup>_m_</sup> )) _▷_ Task arithmetic 15: **else** 16: _F_<sup>_m_</sup> _←_ LayerNorm _m_ ( _X_<sup>_m_</sup> ) 17: **end if** 18: **return** _F_<sup>_m_</sup> 19: **end function** 

21 

Published as a conference paper at ICLR 2026 


Figure 10: Due to the increased token length and softmax normalization, each VLM of TwinVLA refers to arm-specific inputs more than during pretraining, requiring the model to adapt. 

|**Algorithm 4**Attention Re-weighting|
|---|
|**function**APPLYREWEIGHTING(**A**,_α_= 2)<br>|
|2:<br>Create mask**Mr** = (_m̸_=shared)<br>_▷_Create a mask for arm-specific inputs|
|**Areweighted** _←_**A**_⊙_(**Mr**+_α · ¬_**Mr**)_▷_Apply scaling to attention weights using the mask<br>|
|4:<br>**Areweighted** _←_Normalize(**Areweighted**)<br>_▷_Normalize the new weights<br>**return A**+ (**Areweighted**_−_**A**)<br>_▷_Return weights as a residual update for gradient flow<br>6: **end function**|


## C.3 ATTENTION RE-WEIGHTING 

Attention re-weighting is a technique we employ to improve the efficiency of adapting a pretrained SingleVLA into a bimanual TwinVLA. Constructing TwinVLA involves adding a second set of arm-specific modality tokens. During operation, input tokens are processed by their corresponding arm’s VLM backbone, pass through a joint attention layer, and then flow back to the individual VLMs. However, the softmax normalization within this joint attention layer presents a challenge. Although the total sequence length doubles, the number of tokens for shared inputs remains unchanged. Consequently, the proportion of attention allocated to these shared inputs is significantly diluted compared to the pretraining phase, creating a distribution shift for each VLM backbone’s inputs, as illustrated in Figure 10. 

This discrepancy requires greater adaptation effort for TwinVLA during fine-tuning on bimanual tasks. To address this, we introduce a simple re-weighting trick immediately after the attention scores are calculated. Specifically, we double the attention weights corresponding to the shared modality tokens and then re-normalize all weights to sum to one. This adjustment effectively restores the proportional attention each VLM backbone assigns to the shared inputs, aligning it with the pretraining conditions (see Figure 11). Applying this method reduced the initial fine-tuning loss by approximately 40%. While TwinVLA could learn bimanual manipulation without this technique, the required adaptation 

22 

Published as a conference paper at ICLR 2026 


Figure 11: By re-weighting the attention weights, we can make each VLM refer to each modality identically to its pretraining stage, resulting in no adaptation and a lower initial loss. 

period would be substantially longer. This simple trick makes the process significantly more efficient and faster. We illustrate our implementation with simple pseudocode in Algorithm 4. 

- D REAL-WORLD ROBOT EXPERIMENT DETAILS 

- D.1 TASK DETAILS 


Figure 12: Initial distribution of each tasks in real-world. 

To illustrate the diversity of initial configurations in our dataset, Figure 12 shows an overlay of the first frames from all 50 demonstrations. For each demonstration, the position and orientation of the objects were randomized, resulting in a unique starting setup. 


Figure 13: Challenging scene of `Fold towel` task. 

23 

Published as a conference paper at ICLR 2026 

Furthermore, to evaluate policy robustness in the real world, we tested the `Fold towel` task under more challenging conditions, such as reduced lighting and the presence of distractors. These scenarios are visualized in Figure 13. 

## D.2 QUANTITATIVE RESULTS 

Table 7: **Success rates for each model across all subtasks.** The best overall performance is highlighted in bold. As _π_ 0 is included as an upper-bound, as this is excluded from this direct comparison. 

|**Task**|**Subtask**|**DP**|**TwinVLA**|**RDT-1B**|**_π_0**|
|---|---|---|---|---|---|
||`First fold`|0_._00<br>|1_._00<br>|0_._90<br>|1_._00<br>|
|`Fold towel`|`Rotate`|0_._00|1_._00|0_._85|1_._00|
||`Second fold`|0_._00|**0.90**|0_._45|**0.90**|
||`Pick up`|0_._60|0_._90|0_._90|1_._00|
|`Extract hexkey`|`Extract`|0_._35|0_._80|0_._55|0_._90|
||`Put into bowl`|0_._30|**0.80**|0_._45|**0.80**|
||`Pick up carrot`|0_._50|1_._00|0_._75|0_._85|
|`Carrot to bag`|`Put carrot`|0_._20|0_._70|0_._40|0_._65|
||`Close bag`|0_._15|0_._60|0_._35|**0.65**|
||`Move the brush`|0_._70|1_._00|1_._00|1_._00|
|`Brush to dustpan`|`Pick up the brush`|0_._65|1_._00|1_._00|1_._00|
||`Put onto dustpan`|0_._35|**0.80**|0.40|**0.80**|
||`Dragging`|0_._40|0_._90|0_._80|0_._95|
|`Take towel off`|`Half off`|0_._35|0_._70|0_._70|0_._85|
||`Entirely off`|0_._20|0_._45|0_._60|**0.65**|


We provide the quantitative results on real-world experiments in subtask-level detail in Table 7. The results reveal the main bottleneck in each long-horizon task. First, for the two tasks, `Fold towel` and `Extract hexkey` , requiring tightly coupled bimanual coordination, the phase where both arms meet to execute the action appears to be critical. The `Carrot to bag` task is challenging when inserting the carrot, which requires precisely opening the bag. The `Brush to dustpan` task’s bottleneck is the high-precision insertion of the brush into the dustpan. Lastly, in `Take towel off` , the final unfolding is difficult—unlike the simple initial steps—as it requires a successful switch between the arms. In the next subsection, we show qualitative results from these specific bottleneck phases. 

## D.3 QUALITATIVE RESULTS 

Figure 14 presents qualitative results highlighting challenging situations for each task. A check mark was used when the model succeeded with a probability above 0.5, an X mark for probabilities below 0.3, and an exclamation mark icon for intermediate cases. 

- `Carrot to bag.` _π_ 0 showed the highest success rate, followed by TwinVLA, RDT, and DP. DP failed to interact meaningfully with the bag, especially struggling to grasp the cover properly. RDT failed to complete the task successfully, primarily due to its inability to accurately localize and grasp the bag’s opening. 

- `Brush to dustpan.` DP struggled either to grasp the brush itself or to successfully insert it. Interestingly, the RDT managed to grasp the brush well but lacked precision during the insertion. In this task, TwinVLA and _π_ 0 demonstrated the same success rate. 

- `Take towel off.` DP mostly failed to pull the doll from a distant position toward the center, while the other models succeeded in pulling it to the center but showed differences in towel removal. Both RDT and _π_ 0 tended to successfully remove one side of the towel and then easily remove the other side as well. In contrast, TwinVLA struggled with removing the remaining part and repeated the same action. This is likely because the longer action chunk length of RDT and _π_ 0 helped them overcome the multimodality challenge. 

24 

Published as a conference paper at ICLR 2026 


Figure 14: **Qualitative visualization of real world experiments.** 

- `Fold towel.` _π_ 0 and TwinVLA successfully completed the task. RDT also generally performed well, but occasionally failed to fully rotate the towel by 90 degrees, which caused downstream failures. DP experienced substantial difficulty with the fold-towel task and ultimately failed to solve it. 

- `Extract hexkey.` _π_ 0 and TwinVLA generally solved the task reliably. RDT performed the subtask of lifting the hexkey case well but often failed during extraction due to insufficient precision in grasping the hexkey once the case was lifted. DP failed both to reliably pick up the hexkey case and to extract the hexkey itself. 

## D.4 ROBOT HARDWARE SPEC 

We conduct our real-world experiments using a custom-built robot named Anubis. The platform features a teleoperation system inspired by the Mobile ALOHA setup (Fu et al., 2024). Each arm has 6 DoF and is equipped with a parallel gripper and a wrist-mounted camera. At the center of the robot, an Intel RealSense camera is mounted on a height-adjustable mechanism, serving as the ego-centric view camera. Details are described in Table 8. Anubis is equipped with a 3-wheel omni-directional base that supports planar locomotion; however, in this work, the mobility feature is not utilized. 

25 

Published as a conference paper at ICLR 2026 

Table 8: **Anubis Robot Hardware Specifications.** 

|**Component**|**Specification**|
|---|---|
|Base Type|3-wheel omni-directional chassis|
|Mobility DOF|3 (X, Y, Yaw)|
|Arm DOF|2 × (6 DOF + gripper) = 14|
|Total Action Space|17 DOF|
|Wrist Cameras|Intel RealSense D405|
|Gripper|Parallel transparent gripper (hole design, ALOHA-<br>style)|
|Power System|3 × Greenworks 40V 5.0Ah batteries (PC, wheels<br>& leader/follower)|
|Frame|3D-printed custom components|


Figure 15: **The Anubis robot.** 

# E SIMULATION EXPERIMENT DETAILS 


Figure 16: **Task list of Tabletop-Sim.** 

## E.1 TABLETOP-SIM 

To test bimanual policies in simulation, we developed Tabletop-Sim, a new benchmark specifically engineered to evaluate dexterous manipulation skills, in contrast to other benchmarks (Mu et al., 2025) that primarily focus on task diversity. The code are publicly available at `https://github. com/jellyho/Tabletop-Sim` . The benchmark comprises four single-task environments and one multi-task setup. Our task selection was guided by the taxonomy in DexMimicGen (Jiang et al., 2025), which categorizes bimanual tasks into: (1) parallel (two arms are doing separate tasks simultaneously), (2) coordinated (two arms are closely working together), and (3) sequential (one arm completes the task, and the other arm takes over) interactions. Using a custom controller similar to GELLO (Wu et al., 2024), we collected 50 demonstrations for each single-task and 60 for the multi-task environment. 

The multi-task setup is a language-following task requiring the policy to place a specific box (out of three) into a designated pot (out of two) based on a language instruction. This task is designed to rigorously assess a model’s instruction-following capabilities, as Vision-Language-Action (VLA) models often disregard instructions after fine-tuning. 

Furthermore, to evaluate policy robustness, we established two difficulty settings for the four singletasks. The original tasks are designated as the Easy setting, while a Hard variant for each task incorporates challenging variations such as different textures, object models, and the presence of distractor objects. Figure 16 presents snapshots of each task. 

26 

Published as a conference paper at ICLR 2026 

## E.2 QUANTITATIVE RESULTS 

This section describes the detailed results for the simulation tasks. The results for **Tabletop-Sim** are listed in Table 9, while the results for the **RoboTwin 2.0** benchmark are in Table 10. For RoboTwin, the results for other baselines were referenced from the official benchmark results. 

Although _π_ **0** achieves the highest overall performance, this result is unsurprising considering its larger model size and pretraining dataset. Meanwhile, **TwinVLA** demonstrates consistently superior performance compared to **RDT-1B** , a model of a similar scale. 

Table 9: **Performance comparison on the Tabletop-Sim benchmark.** 

|||||Tabletop|-Sim|||||
|---|---|---|---|---|---|---|---|---|---|
||`Dish `|`drainer `|`Handov`|`er box`|`Lift `|`box`|`Shoes `|`table`|`Put X cube in`|
|Model|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|`to Y pot`|
|DP|0_._686|0_._590|0_._180|0_._086|0_._100|0_._006|0_._028|0_._260|-|
|RDT-1B|0_._810|0_._780|0_._694|0_._508|0_._300|0_._076|0_._660|0_._192|0_._555|
|TwinVLA|**0.954**|**0.836**|0_._780|**0.530**|0_._452|0_._044|**0.848**|0_._306|**0.806**|
|PI-0|0_._774|0_._520|**0.788**|0_._444|**0.512**|**0.136**|0_._824|**0.660**|0_._792|


Table 10: **Success rates of TwinVLA for** 50 **bimanual tasks in RoboTwin 2.0.** 

|`Task Name`|Easy|Hard|`Task `|`Name`|Easy|Hard|
|---|---|---|---|---|---|---|
|`adjust bottle`|0_._97|0_._35|`place `|`can basket`|0_._40|0_._00|
|`beat block hammer`|0_._77|0_._10|`place `|`cans plasticbox`|0_._47|0_._08|
|`blocks ranking rgb`|0_._58|0_._00|`place `|`container plate`|0_._77|0_._04|
|`blocks ranking size`|0_._03|0_._00|`place `|`dual shoes`|0_._18|0_._03|
|`click alarmclock`|0_._33|0_._01|`place `|`empty cup`|0_._50|0_._01|
|`click bell`|0_._58|0_._13|`place `|`fan`|0_._34|0_._00|
|`dump bin bigbin`|0_._80|0_._34|`place `|`mouse pad`|0_._50|0_._00|
|`grab roller`|0_._96|0_._22|`place `|`object basket`|0_._48|0_._03|
|`handover block`|0_._17|0_._00|`place `|`object scale`|0_._06|0_._00|
|`handover mic`|0_._84|0_._02|`place `|`object stand`|0_._20|0_._02|
|`hanging mug`|0_._10|0_._05|`place `|`phone stand`|0_._34|0_._02|
|`lift pot`|0_._87|0_._07|`place `|`shoe`|0_._48|0_._04|
|`move can pot`|0_._45|0_._05|`press `|`stapler`|0_._62|0_._26|
|`move pillbottle pad`|0_._32|0_._02|`put b`|`ottles dustbin`|0_._08|0_._04|
|`move playingcard away`|0_._61|0_._35|`put o`|`bject cabinet`|0_._39|0_._16|
|`move stapler pad`|0_._11|0_._00|`rotat`|`e qrcode`|0_._54|0_._03|
|`open laptop`|0_._80|0_._17|`scan `|`object`|0_._11|0_._04|
|`open microwave`|0_._03|0_._01|`shake `|`bottle horizontally`|0_._96|0_._55|
|`pick diverse bottles`|0_._16|0_._08|`shake `|`bottle`|0_._93|0_._58|
|`pick dual bottles`|0_._18|0_._12|`stack `|`blocks three`|0_._00|0_._00|
|`place a2b left`|0_._27|0_._05|`stack `|`blocks two`|0_._26|0_._00|
|`place a2b right`|0_._15|0_._01|`stack `|`bowls three`|0_._77|0_._15|
|`place bread basket`|0_._11|0_._03|`stack `|`bowls two`|0_._84|0_._11|
|`place bread skillet`|0_._20|0_._01|`stamp `|`seal`|0_._16|0_._01|
|`place burger fries`|0_._67|0_._13|`turn `|`switch`|0_._25|0_._15|
|**Average**|||||||
|Diffusion Policy|0_._280|0_._006|||||
|<br>RDT-1B|0_._345|0_._137|||||
|TwinVLA|0_._420|0_._089|||||
|_π_0|0_._464|0_._163|||||


27 

