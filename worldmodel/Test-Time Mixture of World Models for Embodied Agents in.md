---
title: "Test-Time Mixture of World Models for Embodied Agents in Dynamic Environments"
date: "2026-01-30"
authors: "Jinwoo Jang; Minjong Yoo; Sihyung Yoon; Honguk Woo"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2601.22647
pdf: https://arxiv.org/pdf/2601.22647
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.22647)** / [論文ページ](https://arxiv.org/abs/2601.22647)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Published as a conference paper at ICLR 2026 

# TEST-TIME MIXTURE OF WORLD MODELS FOR EMBODIED AGENTS IN DYNAMIC ENVIRONMENTS 

**Jinwoo Jang, Minjong Yoo, Sihyung Yoon & Honguk Woo**<sup>_∗_</sup> Department of Computer Science and Engineering Sungkyunkwan University Suwon, Republic of Korea _{_ jinustar, mjyoo2, godboy3752, hwoo _}_ @skku.edu 

## ABSTRACT 

Language model (LM)-based embodied agents are increasingly deployed in realworld settings. Yet, their adaptability remains limited in dynamic environments, where constructing accurate and flexible world models is crucial for effective reasoning and decision-making. To address this challenge, we extend the Mixtureof-Experts (MoE) paradigm to embodied agents. While conventional MoE architectures modularize knowledge into expert components with pre-trained routing, they remain rigid once deployed, making them less effective for adapting to unseen domains in dynamic environments. We therefore propose Test-time Mixture of World Models (TMoW), a framework that enhances adaptability to unseen and evolving domains. TMoW updates its routing function over world models at test time, unlike conventional MoE where the function remains fixed, enabling agents to recombine existing models and integrate new ones for continual adaptation. It achieves this through (i) multi-granular prototype-based routing, which adapts mixtures across object- to scene-level similarities, (ii) test-time refinement that aligns unseen domain features with prototypes during inference, and (iii) distilled mixture-based augmentation, which efficiently constructs new models from few-shot data and existing prototypes. We evaluate TMoW on VirtualHome, ALFWorld, and RLBench benchmarks, demonstrating strong performance in both zero-shot adaptation and few-shot expansion scenarios, and showing that it enables embodied agents to operate effectively in dynamic environments. 

## 1 INTRODUCTION 

Embodied agents powered by language models (LMs) are increasingly deployed in diverse environments such as households (Song et al., 2023; Ahn et al., 2022), factories (Kang et al., 2024; Zhang et al., 2023), and virtual games (Zhao et al., 2024; Fan et al., 2022). However, their monolithic architectures restrict adaptation, with capabilities frozen at training and domain knowledge buried in billions of shared parameters. This is especially problematic for embodied agents in real-world settings, where tasks and environments change constantly beyond training. In practice, this lack of adaptability leaves retraining as the only option, which imposes significant computational and data collection burdens and hinders real-world deployment. While in-context learning (Song et al., 2023; Kim et al., 2025) attempts to address this through domain-specific prompting, it merely shifts computational burden to inference with inflated context windows, highlighting the need for truly modular architectures. 

Mixture-of-Experts (MoE) (Jacobs et al., 1991) architectures provide structural modularity by selectively activating expert modules per input, thereby supporting scalable inference and domain specialization. Building on this property, recent work has applied MoE to domain adaptation in LM-based agents through techniques such as meta-distillation (Zhong et al., 2022), vision-language models (Iftee et al., 2024), and anomaly detection (Lei et al., 2024). 

In this work, we investigate MoE architectures for LM-based embodied agents, aiming to support rapid adaptation to unseen domains in dynamic environments. While MoE can flexibly activate 

> _∗_ Corresponding author 

1 

Published as a conference paper at ICLR 2026 


Figure 1: Existing Mixture-of-Experts employs a fixed router after training, making adaptation to unseen domains costly and requiring retraining (left). In contrast, **Test-time Mixture of World Models (TMoW)** overcomes this through prototype-based routing and test-time training of the routing function to reflect new domain characteristics without demonstrations (right). 

domain-specific experts, their routing functions, responsible for selecting appropriate expert modules for each input, remain fixed after training, making adaptation to novel domains possible only through costly retraining. For embodied agents in temporally and spatially changing environments, it is essential to overcome this rigidity by adaptively reconfiguring routing functions and extending domain experts to meet these evolving conditions. 

To address this need, we present a Test-time Mixture of World Models (TMoW) framework (Figure 1), which performs test-time training of a routing function without requiring demonstrations. This test-time training approach enables rapid adaptation to environments with temporal and spatial variations beyond the training distribution, facilitating continuous expansion of the model’s capabilities. In the framework, world models act as internal simulators that allow the agent to predict environmental dynamics, reason about future outcomes, and plan appropriate actions, where each model corresponds to a distinct domain within the environment (Zhu et al., 2025; Janner et al., 2021). 

TMoW employs a **multi-granular prototype-based router** that adapts world model mixtures by comparing input observations with learned prototype representations across different levels of spatial abstraction, ranging from local objects to global scenes. We adopt this hierarchical design inspired by LMs’ proven ability to build effective representations through layer-wise progression from local tokens to global context (Van Aken et al., 2019). This router enables **test-time prototype refinement** to unseen domains by refining prototypes through weighted interpolation between existing prototypes based on their similarity to the current environment. Furthermore, TMoW supports **distilled mixture-based model augmentation** for data-efficient creation of new world models. Unlike test-time prototype refinement, this technique requires few-shot demonstrations and distills knowledge from existing model mixtures to construct new models for unseen domains, thereby incrementally expanding TMoW’s repertoire after deployment. 

To evaluate TMoW, we conduct experiments on VirtualHome (Puig et al., 2018), ALFWorld (Shridhar et al., 2021), RLBench (James et al., 2020), and real-world robotic scenarios, demonstrating its capability for rapid and scalable adaptation for evolving and expanding environments. Our framework achieves a 27.21% improvement over SayCanPay (Hazra et al., 2024), state-of-the-art baselines in zero-shot adaptation, and a 25.66% gain in few-shot expansion scenarios when constructing new world models. 

Our contributions are as follows. (1) We propose the TMoW framework, a novel extension of MoE that supports test-time reconfiguration of expert mixtures (i.e., test-time mixture), allowing embodied agents to adapt to unseen domains without costly retraining. (2) We develop a multi-granular prototype-based routing mechanism that realizes this test-time mixture capability, leveraging prototype similarity across spatial levels ranging from local objects to global scenes. (3) We devise 

2 

Published as a conference paper at ICLR 2026 

a distilled mixture-based model augmentation strategy that expands TMoW’s adaptability by dataefficiently constructing new world models. (4) We validate TMoW on diverse benchmarks and real-world scenarios, demonstrating that it advances MoE-based adaptation and offers an effective solution for embodied agents operating in evolving physical environments. 

## 2 RELATED WORK 

**LM-based embodied instruction following.** Embodied instruction following requires agents to ground language instructions in physical environments through sequential action execution, which in turn necessitates robust world models capable of representing diverse environmental configurations. Several approaches have been introduced. Code-driven policies (Singh et al., 2023; Liang et al., 2023) generate executable programs from instructions, while reward-based methods (Yu et al., 2023; Adeniji et al., 2023) learn value functions to guide action selection. Furthermore, LM-based reasoning has been combined with domain-specific models to assess environmental affordances (Ahn et al., 2022; Hazra et al., 2024), and in-context learning approaches incorporate relevant demonstrations directly into the agent’s decision-making process (Song et al., 2023). However, these existing approaches often struggle to generalize to new environments without significant retraining or increase inference-time overhead. Our TMoW framework addresses these challenges by introducing testtime adaptation directly into the MoE architecture, enabling efficient adjustment to unseen domains without retraining. 

**Mixture-of-Experts.** The Mixture-of-Experts (MoE) provides efficient model scaling by activating only a subset of experts, as shown in sparse MoE transformers like GShard (Lepikhin et al., 2020) and Switch Transformer (Fedus et al., 2022). MoE has also been applied to various adaptation settings including Meta-DMoE (Zhong et al., 2022) which uses meta-distillation from domainspecific experts, and MoE-TTA (Iftee et al., 2024) which supports adaptation for vision-language models. Yet, existing MoE architectures face limitations in knowledge expansion, as experts are tightly coupled within a single training graph. Incorporating new domains typically requires endto-end retraining or costly knowledge distillation, thereby restricting modular extensibility. This rigid design prevents modular growth, making it unsuitable for evolving physical environments with diverse tasks and domains. Our approach addresses this through prototype-based routing, which directly supports rapid integration of new world models and dynamic mixture adaptation, while also facilitating knowledge expansion through few-shot model augmentation. 

**Test-time adaptation.** Test-time adaptation has emerged as a critical capability for deploying models in dynamic environments where training and test distributions may differ significantly. Metalearning approaches (Finn et al., 2017; Nichol et al., 2018) learn optimization procedures that enable rapid adaptation to new tasks with limited data. More recent studies have explored lightweight methods. L-TTA (Shin & Kim, 2024) focuses on adapting only the stem layer using uncertainty minimization, while training-free methods such as TDA (Karmanov et al., 2024) leverage key-value caches to enable progressive adaptation without backpropagation. Our TMoW framework brings test-time adaptation to LM-based embodied agents by supporting both dynamic adaptation and continual expansion of world model mixtures. 

## 3 APPROACH 

### 3.1 OVERALL FRAMEWORK 

We present the TMoW framework, which enables agents to dynamically adapt world model mixtures and continuously expand their knowledge in response to evolving environments. Similar to unified world model approaches (Zhu et al., 2025; Janner et al., 2021), each world model in the framework captures environment dynamics through a state transition function and policy. 

As illustrated in Figure 2, TMoW integrates three core procedures into an MoE-based world model structure. These procedures not only allow test-time reconfiguration of world model mixtures by adjusting the mixture strategy itself, but also support efficient expansion through few-shot world model construction. (i) **Multi-granular prototype-based routing:** At test time, the most relevant 

3 

Published as a conference paper at ICLR 2026 


Figure 2: Overall framework of TMoW. 

world models are dynamically selected and composed based on multi-granular prototypes that capture domain semantics at varying levels of abstraction, from local object interactions to global scene structures. A hierarchical message-passing network aggregates these multi-level features, enabling the layer-wise world model mixture where each granularity level can draw knowledge from different domain experts. This network works as a router across world models, allowing the framework to leverage partial domain similarities, such as shared object knowledge across different domains. (ii) **Test-time prototype refinement:** When encountering unseen domains, the router adapts by refining prototypes through weighted interpolation between existing prototypes based on similarity to the current environment. Specifically, through similarity-based refinement during ongoing environment interactions, the router expands existing prototypes to absorb new domain traits, while preserving core knowledge, thereby enabling efficient adaptation to unseen domains via dynamic reconfiguration of world model mixtures. (iii) **Distilled mixture-based model augmentation:** When encountering environments that differ significantly from seen domains, a new world model can be constructed by distilling knowledge from the mixture of existing world models based on few-shot demonstrations. This strategy leverages the collective knowledge of existing models, enabling rapid domain expansion while consolidating fragmented knowledge across diverse domains into a coherent representation of the new domain. The newly distilled world model integrates seamlessly into the framework, with its multi-granular prototype directly incorporated by the router for future mixture decisions. As such, this augmentation supports long-term expansion by introducing new world models, whereas test-time prototype refinement enables immediate adaptation by reconfiguring the mixture weights of existing models. 

### 3.2 MULTI-GRANULAR PROTOTYPE-BASED ROUTER 

**Datasets and world model.** We assume access to a pre-trained base model _M_ and demonstrations _{Dj}_<sup>_N_</sup> _j_ =1<sup>collected from domains</sup><sup>_{Dj}N_</sup> _j_ =1<sup>.Following parameter-efficient MoE designs (Li et al.,</sup> 2024), we integrate domain-specific world models into _M_ using lightweight adapters _{mj}_<sup>_N_</sup> _j_ =1<sup>(e.g.,</sup> LoRA (Hu et al., 2022)), which preserve the backbone parameters while enabling selective activation of multiple world models within each layer. Each adapter _mj_ captures the environmental dynamics and policies of domain _Dj_ by learning from its corresponding _Dj_ . Once trained, they are combined with the base model _M_ to form a mixture of world models, denoted as _M ⊕{mj}_<sup>_N_</sup> _j_ =1<sup>.Each demon-</sup> stration _Dj_ = _{_ ( _in,⃗τn_ ) _}n_ contains instruction-trajectory pairs, where _in ∈I_ specifies the task, and _τn_ = _{_ ( _ot, at, ot_ +1) _}t_ represents the execution trajectory consisting of observations _ot, ot_ +1 _∈O_ and actions _at ∈A_ . 

**Multi-granular prototype.** We introduce multi-granular prototypes that capture environmental semantics across multiple levels of abstraction through hierarchical graph representations. This 

4 

Published as a conference paper at ICLR 2026 


Figure 3: Graph representation in multi-granular prototype. As layers deepen, node representations evolve from local object features to global scene structures. 

design exploits a key insight: while domains may differ globally, they often share common patterns at specific granularities. For instance, object interactions in kitchens and offices follow similar affordance patterns despite different houses. By maintaining representations from fine-grained node features to coarse-grained structural patterns, our multi-granular prototypes enable the layer-wise hierarchical model mixture, identifying which models share relevant patterns at each granularity. 

To implement this multi-granular representation, we employ a graph processor that embeds observations into hierarchical structures, ensuring comparability at each granularity level. Given a mini-batch _B_ sampled from demonstrations _Dj_ , the prototype at each layer _l_ for world model _j_ is computed as 


where the graph processor _f_<sup>(</sup><sup>_l_)</sup> transforms observation graphs _G_<sup>(</sup><sup>_o_)</sup> conditioned on instruction _i_ . We use a Message Passing Neural Network (MPNN) (Gilmer et al., 2017) architecture, introducing a context-aware edge matrix **_E_**<sup>˜(</sup><sup>_l_)</sup> that dynamically adjusts neighbor aggregation based on task requirements. 


The adjustment function captures observation-context interactions through 


where queries **_Q_** _H ,_ **_Q_** _i_ and keys **_K_** _H ,_ **_K_** _i_ are obtained through separate layer-wise learned projections of **_H_**<sup>(</sup><sup>_l−_1)</sup> and the embeddings of the instruction Φ( _i_ ) respectively, and _d_ is the dimension of queries and keys. 

The prototype initially contains only local information but progressively gathers neighbor information through layers, with instruction-based adjustment factors controlling this aggregation (Figure 3). This creates a natural progression from node-level features in early layers to graph-level patterns in deeper layers, analogous to how LMs progress from token-level to paragraph-level reasoning. 

**Prototype-based router.** To select which world models to activate and with what routing scores, the router compares the embedding extracted from the current input data with the prototype of each world model. The router receives an instruction _i_ , and observation _o_ as input and returns expert routing scores ( _w_ 1<sup>(</sup><sup>_l_)</sup><sup>_, · · ·, w_</sup> _N_<sup>(</sup><sup>_l_)) for each layer</sup><sup>_f_(</sup><sup>_l_) of the base model.Specifically, given input (</sup><sup>_i, o_),</sup> the routing score for expert _j_ at _l_<sup>th</sup> layer is computed as 


where _E_<sup>(</sup><sup>_l_)</sup> is a _domain embedding_ produced by the _l_<sup>th</sup> layer of the graph processor’s MPNN, **_p_**<sup>(</sup> _j_<sup>_l_)</sup> is the prototype of world model _j_ at layer _l_ , and sim( _·, ·_ ) denotes cosine similarity. The score vector ( ¯ _w_ 1<sup>(</sup><sup>_l_)</sup><sup>_, · · ·,w_¯</sup> _N_<sup>(</sup><sup>_l_)) at layer</sup><sup>_l_is sparsified by retaining only the top-</sup><sup>_K_entries and then normalized with</sup> a softmax and scaling hyperparameter _τ_ ( _τ >_ 0). 


Finally, the output at _l_<sup>th</sup> layer is calculated by combining the base model with the _N_ adapters, weighted by the normalized scores ( ¯ _w_ 1<sup>(</sup><sup>_l_)</sup><sup>_, · · ·,w_¯</sup> _N_<sup>(</sup><sup>_l_)).</sup> 

5 

Published as a conference paper at ICLR 2026 


Figure 4: Comparison of the routing score heatmap before (left) and after (right) test-time prototype refinement for (a) seen and (b) unseen domains. 

### 3.3 TEST-TIME PROTOTYPE REFINEMENT 

We introduce test-time prototype refinement that dynamically adjusts prototype representations through environment interactions, enabling adaptation to unseen domains without retraining. Our refinement expands prototype space and densifies prototype allocation around frequently encountered features, exploiting previously underutilized knowledge within existing world models (Wang et al., 2023). 


where ∆ **_p_**<sup>(</sup> _j_<sup>_l_)</sup> is a refinement term, _E_<sup>(</sup><sup>_l_)</sup> is a domain embedding for the unseen domain from the environment interaction, and _α_ is a refinement rate. The refinement term is then obtained by computing refinement weights _r_ ¯ _j,k_<sup>(</sup><sup>_l_)fromprototype–prototype similarity,which are usedto form the weighted</sup> sum where the weights (¯ _rj,_<sup>(</sup><sup>_l_</sup> 1<sup>)</sup><sup>_, · · ·,_¯</sup><sup>_r_</sup> _j,N_<sup>(</sup><sup>_l_)) are obtained through similarity measurement and softmax</sup> normalization with a scaling hyperparameter _τr_ ( _τr >_ 0): 


Figure 4 illustrates the comparison of routing scores before and after refinement. In the seen domain (Figure 4a), the heatmap showed minimal changes, though there is a slight tendency toward utilizing more diverse world models. In the unseen domain (Figure 4b), this diversification is more pronounced, facilitating the utilization of relatively diverse world models. The iterative prototype refinement enhances shared knowledge across world models by densifying prototype allocation around frequently encountered domains. This expands the effective coverage of the prototype space while constructing dense clusters in high-frequency regions, thereby enabling fine-grained routing strategies that foster knowledge sharing across world models. 

### 3.4 DISTILLED MIXTURE-BASED MODEL AUGMENTATION 

We introduce a distillation-based model augmentation that enables rapid expansion to novel domains by constructing new world models from mixtures of existing ones using few-shot demonstrations. When encountering novel domains with fundamentally different characteristics, this approach constructs new world models by distilling knowledge from weighted mixtures of existing models, where the router’s weights indicate which knowledge fragments are most relevant to the unseen domain. Unlike test-time refinement, which adapts unseen domains solely by reconfiguring mixtures of existing models, this augmentation further extends the framework’s capacity by generating new models that integrate seamlessly into the routing system. This seamless integration is enabled by prototypebased routing, which allows newly created models to align with existing ones and immediately join the routing process without structural changes. 

Specifically, we leverage the router’s weighted mixture, where the weights indicate which fragments of knowledge from models are most relevant to the unseen domain’s features. Given few-shot demonstrations _D_<sup>_′_</sup> = _{_ ( _i_<sup>_′_</sup> _,⃗τ_<sup>_′_</sup> ) _}_ , we construct a combined graph _G_<sup>_′_</sup> from the trajectory and process it through an _f_ to obtain the layer-wise routing scores ( ¯ _w_ 1<sup>(</sup><sup>_l_)</sup><sup>_, · · ·,w_¯</sup> _N_<sup>(</sup><sup>_l_)) for each layer</sup><sup>_l_.We initialize</sup> a new world model _m_<sup>_′_</sup> as mixture of existing models, then fine-tune it on _D_<sup>_′_</sup> before integration into 

6 

Published as a conference paper at ICLR 2026 

Table 1: Zero-shot adaptation performance in VirtualHome, ALFWorld, and RLBench. Throughout the following experiments, we report 95% confidence intervals computed across 5 random seeds. 

|**Seen domains**|_VirtualH_|_ome_|_ALFWo_|_rld_|_RLBen_|_ch_|
|---|---|---|---|---|---|---|
|Baselines|SR (_↑_)|PS (_↓_)|SR (_↑_)|PS (_↓_)|SR (_↑_)|PS (_↓_)|
|ZSP (Huang et al., 2022)|10_._78%_±_1.50%|27_._81_±_0.07|2_._32%_±_0.19%|49_._34_±_0.66|11_._26%_±_1.59%|17_._57_±_0.46|
|LLM+FT|61_._37%_±_6.96%|17_._98_±_1.71|51_._78%_±_1.13%|13_._22_±_1.37|65_._53%_±_2.43%|11_._04_±_0.19|
|LLM-Planner (Song et al., 2023)|50_._98%_±_6.37%|17_._85_±_0.51|11_._67%_±_0.22%|37_._19_±_0.25|35_._21%_±_1.59%|14_._77_±_0.08|
|FLARE (Kim et al., 2025)|54_._69%_±_6.91%|19_._93_±_0.12|21_._22%_±_0.20%|34_._40_±_1.44|53_._05%_±_4.78%|14_._77_±_0.84|
|SayCanPay (Hazra et al., 2024)|64_._14%_±_6.17%|15_._70_±_0.98|51_._48%_±_1.72%|13_._19_±_0.84|68_._08%_±_2.93%|8_._69_±_0.61|
|TMoW|**83.61%**_±_**1.28%**|**11.07**_±_**0.53**|**72.05%**_±_**0.62%**|**6.94**_±_**0.21**|**71.89%**_±_**2.73**%|**6.30**_±_**0.16**|
|**Unseen domains**|_VirtualH_|_ome_|_ALFWo_|_rld_|_RLBen_|_ch_|
|Baselines|SR (_↑_)|PS (_↓_)|SR (_↑_)|PS (_↓_)|SR (_↑_)|PS (_↓_)|
|ZSP (Huang et al., 2022)|7_._32%_±_0.52%|28_._22_±_0.04|2_._08%_±_0.03%|49_._68_±_0.32|10_._42%_±_2.04%|18_._73_±_0.31|
|LLM+FT|44_._24%_±_6.02%|21_._00_±_0.39|39_._61%_±_0.47%|41_._24_±_0.47|15_._63%_±_3.54%|17_._44_±_1.10|
|LLM-Planner (Song et al., 2023)|36_._05%_±_0.23%|22_._93_±_0.01|8_._46%_±_0.49%|43_._54_±_0.11|19_._79%_±_4.08%|17_._19_±_1.54|
|FLARE (Kim et al., 2025)|40_._07%_±_1.02%|22_._57_±_0.13|11_._31%_±_0.45%|42_._85_±_0.90|34_._37%_±_1.80%|11_._37_±_0.42|
|SayCanPay (Hazra et al., 2024)|49_._53%_±_0.44%|18_._55_±_0.01|42_._04%_±_1.74%|40_._64_±_0.43|38_._54%_±_1.80%|10_._76_±_0.49|
|<br>TMoW|**80.16%**_±_**1.45%**|**13.20**_±_**0.82**|**68.83%**_±_**1.15%**|**37.44**_±_**3.82**|**62.75%**_±_**2.65**%|**8.95**_±_**0.39**|


the mixture. Then, new world model _m_<sup>_′_</sup> and its corresponding prototype **_p_**<sup>_′_(</sup><sup>_l_)</sup> are computed as 


where _η_ is learning rate, and the _L_ TF is teacher-forcing training loss that supervises next action and observation along the trajectory, similar to Janner et al. (2021). 

## 4 EXPERIMENTS 

**Environments and datasets.** We evaluate TMoW with embodied environments such as VirtualHome (Puig et al., 2018), ALFWorld (Shridhar et al., 2021), and RLBench (James et al., 2020). VirtualHome is a 3D virtual environment for simulating activities in a household, ALFWorld is an indoor task simulation environment that aligns text and embodied robotic manipulation, and RLBench is a robotic manipulation benchmark for tabletop tasks, which we adapted to support language-based actions. In VirtualHome, 78 tasks (16 seen, 62 unseen) are paired with 20 distinct scenes (10 seen, 10 unseen) to form 445 demonstrations. In ALFWorld, following the CL-ALFRED benchmark (Kim et al., 2024), 6 task categories (4 seen, 2 unseen) are paired with 4 scene categories (3 seen, 1 unseen) to form 1,304 demonstrations. In RLBench, 4 task categories (3 seen, 1 unseen) are paired with 6 scene categories (4 seen, 2 unseen) to form 163 demonstrations from seen domain. Detailed descriptions of environments and datasets are provided in Appendix A. 

**Evaluation Metrics.** We adopt two evaluation metrics: Success Rate (SR) and Pending Steps (PS). SR denotes the ratio of successfully completed tasks. PS stands for the average timestep taken to complete tasks, akin to cost-effectiveness in (Hazra et al., 2024). 

**Baselines.** For comparison, we use five baselines. **ZSP** (Huang et al., 2022) is a zero-shot approach of using a pre-trained model to adapt to unknown domains without additional training. **LLM+FT** is an LLM that is fine-tuned with domain-specific demonstrations to improve performance in new environments. **LLM-Planner** (Song et al., 2023) is a few-shot in-context learning method to generate and refine high-level plans for new domains. **SayCanPay** (Hazra et al., 2024) is a state-of-the-art model that integrates LLMs with a heuristic cost minimization method to generate cost-effective plans. Lastly, **FLARE** (Kim et al., 2025) is a state-of-the-art embodied task planning model that combines environmental perception with adaptive replanning to generate grounded task plans by correcting predictions to align with environment features with few examples. We use Llama-3.23B (AI@Meta, 2024) for ZSP, LLM-Planner, FLARE, and the Say model in SayCanPay, while using trainable Llama-3.2-1B for LLM+FT, the Pay model in SayCanPay, and TMoW. 

7 

Published as a conference paper at ICLR 2026 

Table 2: Few-shot expansion performance in VirtualHome. 

|**Unseen domains**,_VirtualHome_<br>_1-Shot_|_5-Sho_|_t_|_Averag_|_e_|
|---|---|---|---|---|
|Baselines<br>SR (_↑_)<br>PS (_↓_)|SR (_↑_)|PS (_↓_)|SR (_↑_)|PS (_↓_)|
|LLM+FT<br>50_._46%_±_0.44%<br>19_._51_±_0.05|54_._36%_±_7.18%|18_._55_±_0.04|52_._41%_±_3.81%|19_._03_±_0.04|
|LLM-Planner (Song et al., 2023)<br>40_._97%_±_6.02%<br>22_._07_±_0.19|43_._61%_±_0.92%|21_._06_±_0.17|43_._30%_±_3.33%|21_._45_±_0.15|
|FLARE (Kim et al., 2025)<br>42_._17%_±_0.37%<br>22_._19_±_0.19|46_._64%_±_7.02%|20_._67_±_0.12|42_._29%_±_3.47%|21_._56_±_0.18|
|SayCanPay (Hazra et al., 2024)<br>54_._98%_±_2.09%<br>17_._77_±_0.04|58_._88%_±_10.63%|16_._92_±_0.22|56_._93%_±_6.36%|17_._35_±_0.13|
|TMoW<br>**81.56%**_±_**1.69%**<br>**13.20**_±_**0.48**|**83.61%**_±_**1.33%**|**12.04**_±_**0.64**|**82.59%**_±_**1.49%**|**12.62**_±_**0.56**|
|main<br>Can you stack up the boxes that are on the desk?|**Seen Domains**||_Real-wo_|_rld_|
|do|Baselines||SR (_↑_)|PS (_↓_)|
|Seen|FLARE (Kim et a<br>SayCanPay (Hazr<br>TMoW|l., 2025)<br>a et al., 2024)|57_._10% _±_5.99%<br>52_._90% _±_8.13%<br>**91.46%**_±_**2.88%**|7_._26 _±_0.56<br>7_._00 _±_0.37<br>**4.23**_±_**0.12**|
|in<br>C  l  th th  th dk?|**Unseen Domains**||_Real-wo_|_rld_|
|ma<br>an you cean up e ras on e es|Baselines||SR (_↑_)|PS (_↓_)|
|Unseen do|FLARE (Kim et a<br>SayCanPay (Hazr<br>TMoW|l., 2025)<br>a et al., 2024)|36_._04% _±_11.18%<br>7_._80% _±_4.60%<br>**74.64%**_±_**2.99%**|7_._87 _±_0.56<br>9_._71 _±_0.22<br>**4.89**_±_**0.18**|


Figure 5: Examples of Real-world environment. 

Table 3: Zero-shot adaptation performance in Real-world Scenario. 

### 4.1 MAIN RESULTS 

**Zero-shot adaptation.** We evaluate each method in zero-shot adaptation scenarios, where agents must generalize across diverse seen and unseen domains, without access to any additional demonstrations. Each domain represents a unique combination of task and scene. 

As shown in Table 1, TMoW consistently outperforms all baselines across both seen and unseen domains, particularly showing robust generalization to unseen domains. The results demonstrate the superiority of our test-time mixture approach, where multi-granular prototypes effectively capture shareable domain characteristics and enable immediate generalization through world model mixture, achieving an average improvement of 14.61% in SR and 4.42 reduction (35.31% improvement) in PS across environments for seen domains. Furthermore, test-time prototype refinement allows our model to effectively process unseen domain data by aligning unseen features with prototypes, thereby appropriately exploiting partial knowledge from existing models. This approach particularly excels in unseen domains, where we observe an average improvement of 27.21% in SR and a reduction of 3.45 steps (14.81% improvement) in PS across environments for unseen domains. 

**Few-shot expansion.** We further evaluate few-shot expansion scenarios, where each target domain provides only a few demonstrations at test time. This setup examines how effectively TMoW expands its knowledge through distilled mixture-based augmentation with minimal supervision. 

Table 2 compares performance across different few-shot settings (1 and 5 shots) in VirtualHome, illustrating how the number of available demonstrations affects adaptation quality. As shown, TMoW surpasses all baselines, achieving on average a 25.66% gain in SR and 4.73 step reduction in PS in VirtualHome. These results demonstrate that our distilled mixture-based augmentation efficiently achieves additional performance improvements through knowledge expansion while maintaining the modularity of the overall framework. 

**Real-world scenario.** We conduct experiments in real-world environments similar to RLBench to validate the practical applicability of our approach. As shown in Figure 5, we use Franka Research 3 robot arm, and these experiments involve user instruction execution in specific object settings. In Table 3, TMoW achieves an average improvement of 34.36% in SR compared to the best baseline and 2.77 reduction (39.57% improvement) in PS for seen domains. For unseen domains, our method demonstrates even more substantial gains with an average improvement of 38.60% in SR and 2.98 reduction (37.86% improvement) in PS compared to the best performing baseline, FLARE. 

8 

Published as a conference paper at ICLR 2026 

Our TMoW demonstrates superior adaptation capabilities in these real-world scenarios, successfully handling tasks that require intricate manipulation sequences and environmental understanding. The results confirm that TMoW effectively transfers from simulation to reality, maintaining robust performance despite the inherent uncertainties and variations present in physical environments. 

**Ablation study.** We validate TMoW’s components through ablation studies in VirtualHome, Unseen domains settings. For multi-granular prototypes, we compare against TMoW-Object (using only local object features for routing) and TMoW-Scene (using only global scene features for routing) variants. To assess test-time refinement, TMoW-NoRefine uses fixed prototypes without adaptation. In Table 4a, TMoW outperforms TMoWObject 15 _._ 49% improvement in SR and 3.60 reduction in PS, and TMoW-Scene 72 _._ 00% in SR and 14.26% in PS. This confirms that the multi-granularity approach enables efficient knowledge sharing while preserving an overall understanding of domain structure, thereby contributing to improved performance. Dynamic refinement improves SR by 7.65%, validating its effectiveness for unseen scenarios. Finally, we evaluate our distilled mixture approach against TMoW-Scratch (training from scratch). In Table 4b, our method achieves 18.39% higher SR than scratch training while using 40% less data, demonstrating superior efficiency in knowledge distillation from mixture of the existing world models. 

Table 4: Ablation study of TMoW 

|Model<br>SR (_↑_)|PS (_↓_)|
|---|---|
|_Multi-granular Prototype-base_<br>TMoW-Object<br>65_._25%_±_4.44%<br>|_d Routing_<br>16_._72_±_1.99|
|TMoW-Scene<br>8_._74%_±_0.60%|27_._38_±_0.33|
|_Test-time Prototype Refine_|_iment_|
|TMoW-NoRefine<br>73_._30%_±_1.47%|14_._85_±_0.53|
|TMoW<br>**80.74%**_±_**1.69%**|**13.12**_±_**0.87**|
|(a) Zero-shot adaptation|scenario|
|Model<br>SR (_↑_)|PS (_↓_)|
|_Distilled Mixture-based Model A_|_ugmentation_|
|TMoW-Scratch<br>59_._84%_±_1.28%|18_._16_±_0.74|
|TMoW<br>**81.56%**_±_**1.69%**|**13.20**_±_**0.48**|
|(b) Few-shot expansion|scenario|


### 4.2 ANALYSIS 

**Analysis for multi-granular prototype.** Figure 6a illustrates the routing score entropy across layers, revealing distinct mixture patterns of world models. We observe high entropy in early layers, indicating that multiple world models contribute equally to local object-level representations, maximizing knowledge sharing for fine-grained features. Conversely, later layers exhibit lower entropy, suggesting that global structural and scene-level embeddings become more specialized to specific world models. This hierarchical transition from shared local features to isolated global representations demonstrates how our multi-granular approach naturally balances knowledge sharing and domain specialization across different levels of abstraction. 

**Analysis for test-time prototype refinement.** Figure 6b shows the routing score entropy before (TMoW-NoRefine) and after (TMoW) prototype refinement, demonstrating increased average entropy across all layers. This entropy increase reveals that refinement corrects the initial misalignment between prototypes and unseen domains, enabling the router to recognize previously underutilized knowledge within existing world models. By expanding prototype coverage to better capture unseen domain characteristics, the refinement process facilitates more active knowledge sharing across models, allowing previously underutilized models to contribute to unseen domains. This means the agent can now leverage a more diverse mixture of world model expertise. (a) Layer-wise routing score entropy heatmap (b) Routing score entropy changes after refinement 

Figure 6: Analysis for multi-granular prototype-based routing and test-time prototype refinement. 

9 

Published as a conference paper at ICLR 2026 

**Analysis for top-K routing.** Table 5 presents the impact of varying _K_ values in our top- _K_ routing mechanism. TMoW-Top-3 (default, same as TMoW) achieves the best overall performance (80.16% SR, 13.20 PS), significantly outperforming single-expert selection (Top-1: 65.43% SR, 17.34 PS). This validates that combining knowledge from multiple world models is essential for handling unseen domains. Notably, increasing _K_ beyond 3 leads to performance degradation, with Top-5 showing slight decline (77.52% SR, 15.19 PS) and Top-7 exhibiting substantial drops (66.01% SR, 17.67 PS), comparable to single-expert performance. This suggests that excessive expert activation introduces noise rather than useful knowledge, as irrelevant world models dilute the contribution of domain-relevant experts. The optimal _K_ = 3 configuration balances knowledge diversity with focused expertise, enabling effective mixture without information overflow. 

Table 5: Analysis for top- _K_ routing 

|TMoW-Top-1|TMoW-Top-3|(TMoW)|TMoW-T|op-5|TMoW-|Top-7|
|---|---|---|---|---|---|---|
|SR (_↑_)<br>PS (_↓_)|SR (_↑_)|PS (_↓_)|SR (_↑_)|PS (_↓_)|SR (_↑_)|PS (_↓_)|
|65_._43%_±_2.22%<br>17_._34_±_0.52|80_._16%_±_1.45%|13_._20_±_0.82|77_._52%_±_0.40%|15_._19_±_0.45|66_._01%_±_1.33%|17_._67_±_0.36|


**Continuous expansion.** Figure 7 presents our TMoW’s performance in continuous domain expansion scenarios. As domains are added in new phase, the framework incorporates new world models through distilled augmentation, with refinement facilitating efficient integration. The performance improves not only for new domains but for existing ones, indicating positive knowledge transfer, Figure 7: Continuous expansion scenario. while maintaining high performance on previously encountered domains without forgetting. This validates our prototype-based routing’s ability to preserve existing knowledge while enabling cross-domain synergy through expanded coverage. 

## 5 CONCLUSION 

We presented the TMoW framework to enable embodied agents to effectively adapt to evolving environments at test time. By extending the MoE paradigm with multi-granular prototype-based routing and distilled mixture-based model augmentation, TMoW allows embodied agents to flexibly reconfigure world model mixtures at test time and efficiently construct new world models from few-shot demonstrations without retraining the entire system. Through extensive evaluation on VirtualHome and ALFWorld, we demonstrated that TMoW achieves strong performance in various adaptation scenarios, validating its effectiveness and scalability in dynamic embodied settings. 

**Future work and limitation.** TMoW has two main limitations: (1) its performance is inherently bounded by the capabilities of the underlying LLM used for planning, and (2) the world model approach may face challenges in highly non-stationary environments like multi-agent settings where other agents’ behaviors continuously change the environment dynamics. For future work, we plan to enhance the safety and interpretability of TMoW’s routing decisions while extending it to multi-agent systems, enabling more reliable deployment and coordinated decision-making in safety-critical applications. 

### ACKNOWLEDGMENTS 

This work was supported by the Institute of Information & Communications Technology Planning & Evaluation(IITP) grant funded by the Korea government(MSIT) (RS-2025-25442569, AI Star Fellowship Support Program(Sungkyunkwan Univ.), 15%, RS-2025-02218768, Accelerated Insight Reasoning via Continual Learning, 15%, RS-2022-II221045 (2022-0-01045), Self-directed multi-modal Intelligence for solving unknown, open domain problems, 15%, RS-2022-II220043 (2022-0-00043), Adaptive Personality for Intelligent Agents, 15%, RS-2020-II201821, ICT Creative Consilience Program, 15%, and RS-2019-II190421, Artificial Intelligence Graduate School Program (Sungkyunkwan University)), 15%), and IITP-ITRC (Information Technology Research Center) grant funded by the Korea government(MIST) (IITP-2024-RS-2024-00437633, 10%). 

10 

Published as a conference paper at ICLR 2026 

## REFERENCES 

- Ademi Adeniji, Amber Xie, Pieter Abbeel, and Archit Sharma. Language reward modulation for pretraining reinforcement learning, 2023. 

- Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang, Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil J Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao, Kanishka Rao, Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Mengyuan Yan, and Andy Zeng. Do as i can, not as i say: Grounding language in robotic affordances. In _Conference on Robot Learning_ , 2022. 

- AI@Meta. Llama 3.2 model card. 2024. URL https://github.com/meta-llama/ llama-models/blob/main/models/llama3_2/MODEL_CARD.md. 

- Linxi Fan, Guanzhi Wang, Yunfan Jiang, Ajay Mandlekar, Yuncong Yang, Haoyi Zhu, Andrew Tang, De-An Huang, Yuke Zhu, and Anima Anandkumar. Minedojo: Building open-ended embodied agents with internet-scale knowledge. _Advances in Neural Information Processing Systems_ , 35: 18343–18362, 2022. 

- William Fedus, Barret Zoph, and Noam Shazeer. Switch transformers: scaling to trillion parameter models with simple and efficient sparsity. _Journal of Machine Learning Research_ , 23(120):1–39, 2022. 

- Chelsea Finn, Pieter Abbeel, and Sergey Levine. Model-agnostic meta-learning for fast adaptation of deep networks. In _International Conference on Machine Learning_ , pp. 1126–1135, 2017. 

- Justin Gilmer, Samuel S. Schoenholz, Patrick F. Riley, Oriol Vinyals, and George E. Dahl. Neural message passing for quantum chemistry, 2017. URL https://arxiv.org/abs/1704. 01212. 

- Rishi Hazra, Pedro Zuidberg Dos Martires, and Luc De Raedt. Saycanpay: Heuristic planning with large language models using learnable domain knowledge. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pp. 20123–20133, 2024. 

- Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. Language models as zero-shot planners: Extracting actionable knowledge for embodied agents. In _International conference on machine learning_ , pp. 9118–9147. PMLR, 2022. 

- Md Akil Raihan Iftee, Wahida Mahjabin, Anik Ekka, and Sunanda Das. Moe-tta: Enhancing continual test-time adaptation for vision-language models through mixture of experts. In _2024 27th International Conference on Computer and Information Technology (ICCIT)_ , pp. 3278–3283. IEEE, 2024. 

- Robert A. Jacobs, Michael I. Jordan, Steven J. Nowlan, and Geoffrey E. Hinton. Adaptive mixtures of local experts. _Neural Computation_ , 3(1):79–87, 1991. doi: 10.1162/neco.1991.3.1.79. 

- Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019– 3026, 2020. 

- Michael Janner, Qiyang Li, and Sergey Levine. Offline reinforcement learning as one big sequence modeling problem. _Advances in neural information processing systems_ , 34:1273–1286, 2021. 

- Jeon Ho Kang, Neel Dhanaraj, Siddhant Wadaskar, and Satyandra K Gupta. Using large language models to generate and apply contingency handling procedures in collaborative assembly applications. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 15585–15592. IEEE, 2024. 

11 

Published as a conference paper at ICLR 2026 

- Adilbek Karmanov, Dayan Guan, Shijian Lu, Abdulmotaleb El Saddik, and Eric Xing. Efficient test-time adaptation of vision-language models, 2024. 

- Byeonghwi Kim, Minhyuk Seo, and Jonghyun Choi. Online continual learning for interactive instruction following agents. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- Taewoong Kim, Byeonghwi Kim, and Jonghyun Choi. Multi-modal grounded planning and efficient replanning for learning embodied agents with a few examples. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pp. 4329–4337, 2025. 

- Tianwu Lei, Silin Chen, Bohan Wang, Zhengkai Jiang, and Ningmu Zou. Adapted-moe: Mixture of experts with test-time adaption for anomaly detection. _arXiv preprint arXiv:2409.05611_ , 2024. 

- Dmitry Lepikhin, HyoukJoong Lee, Yuanzhong Xu, Dehao Chen, Orhan Firat, Yanping Huang, Maxim Krikun, Noam Shazeer, and Zhifeng Chen. Gshard: Scaling giant models with conditional computation and automatic sharding, 2020. 

- Dengchun Li, Yingzi Ma, Naizheng Wang, Zhengmao Ye, Zhiyuan Cheng, Yinghao Tang, Yan Zhang, Lei Duan, Jie Zuo, Cal Yang, and Mingjie Tang. Mixlora: Enhancing large language models fine-tuning with lora-based mixture of experts, 2024. URL https://arxiv.org/ abs/2404.15159. 

- Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. Code as policies: Language model programs for embodied control, 2023. 

- Alex Nichol, Joshua Achiam, and John Schulman. On first-order meta-learning algorithms. 2018. 

- Xavier Puig, Kevin Ra, Marko Boben, Jiaman Li, Tingwu Wang, Sanja Fidler, and Antonio Torralba. Virtualhome: Simulating household activities via programs. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pp. 8494–8502, 2018. 

- Jin Shin and Hyun Kim. L-tta: Lightweight test-time adaptation using a versatile stem layer, 2024. 

- Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Cote, Yonatan Bisk, Adam Trischler, and Matthew Hausknecht. Alfworld: Aligning text and embodied environments for interactive learning. In _International Conference on Learning Representations_ , 2021. 

- Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, Danfei Xu, Jonathan Tremblay, Dieter Fox, Jesse Thomason, and Animesh Garg. Progprompt: Generating situated robot task plans using large language models, 2023. 

- Chan Hee Song, Jiaman Wu, Clayton Washington, Brian M Sadler, Wei-Lun Chao, and Yu Su. Llm-planner: Few-shot grounded planning for embodied agents with large language models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 2998–3009, 2023. 

- Betty Van Aken, Benjamin Winter, Alexander L¨oser, and Felix A Gers. How does bert answer questions? a layer-wise analysis of transformer representations. In _Proceedings of the 28th ACM international conference on information and knowledge management_ , pp. 1823–1832, 2019. 

- Qi-Wei Wang, Da-Wei Zhou, Yi-Kai Zhang, De-Chuan Zhan, and Han-Jia Ye. Few-shot classincremental learning via training-free prototype calibration. _Advances in Neural Information Processing Systems_ , 36:15060–15076, 2023. 

- Wenhao Yu, Nimrod Gileadi, Chuyuan Fu, Sean Kirmani, Kuang-Huei Lee, Montse Gonzalez Arenas, Hao-Tien Lewis Chiang, Tom Erez, Leonard Hasenclever, Jan Humplik, Brian Ichter, Ted Xiao, Peng Xu, Andy Zeng, Tingnan Zhang, Nicolas Heess, Dorsa Sadigh, Jie Tan, Yuval Tassa, and Fei Xia. Language to rewards for robotic skill synthesis, 2023. 

- Jesse Zhang, Jiahui Zhang, Karl Pertsch, Ziyi Liu, Xiang Ren, Minsuk Chang, Shao-Hua Sun, and Joseph J Lim. Bootstrap your own skills: Learning to solve new tasks with large language model guidance. _arXiv preprint arXiv:2310.10021_ , 2023. 

12 

Published as a conference paper at ICLR 2026 

- Zhonghan Zhao, Wenhao Chai, Xuan Wang, Boyi Li, Shengyu Hao, Shidong Cao, Tian Ye, and Gaoang Wang. See and think: Embodied agent in virtual environment. In _European Conference on Computer Vision_ , pp. 187–204. Springer, 2024. 

- Tao Zhong, Zhixiang Chi, Li Gu, Yang Wang, Yuanhao Yu, and Jin Tang. Meta-dmoe: Adapting to domain shift by meta-distillation from mixture-of-experts. _Advances in Neural Information Processing Systems_ , 35:22243–22257, 2022. 

- Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets, 2025. URL https://arxiv.org/abs/2504.02792. 

13 

Published as a conference paper at ICLR 2026 

## A ENVIRONMENTS 

### A.1 VIRTUALHOME 

We conduct our experiments using VirtualHome (Puig et al., 2018), a Unity-based simulation platform that enables embodied agents to execute complex household tasks through natural language instructions. The environment provides 20 distinct house configurations, each featuring diverse room architectures and object arrangements that capture the heterogeneity of real-world domestic spaces. 

**Environment structure.** VirtualHome represents environmental states as directed graphs, where nodes correspond to entities (agents, objects, rooms) and edges encode spatial and functional relationships. Each state observation consists of relational triples ( _e_ 1 _, r, e_ 2) encoding relationships such as spatial containment (e.g., _faucet inside bathroom_ ), proximity (e.g., _character close plum_ ), adjacency (e.g., _bedroom adjacent kitchen_ ), and agent-object interactions (e.g., _character hold breadslice_ ). This graph-based representation naturally captures the compositional structure of household environments and enables reasoning about object affordances and spatial constraints. 


Figure A.1: The example top-view scene of the VirtualHome environment. 

**Action space.** Agents interact with the environment through six primitive action types: walk (navigation), grab (object manipulation), open (state changes), put (placement), putin (container interactions), and switch (device activation). These actions modify the environment graph according to deterministic transition rules, enabling predictable yet complex multi-step behaviors. The constrained action space reflects common household interactions while maintaining computational tractability for learning algorithms. 

**[System]** 

You are a home robot agent. You can use 6 skills, ( _walk [object or room], grab [object], switch [object], open [object], putin [target object], put [target object]_ ). You should return only a skill after “ _Action_ :”. Room: _livingroom, bathroom, kitchen, bedroom_ . 

**[User]** Instruction: _{instruction}_ Observation: _{observation}_ Action: 

Figure A.2: System prompt in VirtualHome 

**Task specifications.** We evaluate on 78 household instructions spanning four task categories that test different aspects of embodied reasoning. Each instruction defines success criteria through target graph configurations, requiring agents to transform the initial environment state through appropriate action sequences. Tasks vary from simple object retrieval to complex multi-room activities involving 

14 

Published as a conference paper at ICLR 2026 


Figure A.3: The available scenes of the ALFWorld environment. 

sequential dependencies and state preconditions, providing a comprehensive benchmark for evaluating adaptation capabilities across varying complexity levels. 

### A.2 ALFWORLD 

ALFWorld (Shridhar et al., 2021) is a text-based embodied reasoning environment that translates the ALFRED benchmark’s visual tasks into natural language interactions. This environment challenges agents to execute multi-step household tasks through textual observations and instructions, emphasizing task planning and state reasoning in partially observable settings. 

**Environment structure.** ALFWorld presents environmental states through natural language descriptions that include spatial information, object locations, and agent positioning. After initialization, agents receive textual observations (e.g., _“You are in the middle of a room. Looking quickly around you, you see a armchair 1, a coffeetable 1...”_ ) alongside the instruction (e.g., _“Your task is to: put a pillow in armchair”_ ). 

**[System]** You are a home robot agent. You can use 10 skills, ( _go to [object], take [object] from [object], put [object] on [object], open [object], close [object], toggle [object], heat [object] with [object], cool [object] with [object], clean [object] with [object], look_ ). You should return only a skill after “ _Action_ :”. Room: _livingroom, bathroom, kitchen, bedroom_ . **[User]** Instruction: _{instruction}_ Observation: _{observation_ 0 _}_ Action: _{action_ 0 _}_ Observation: _{observation_ 1 _}_ Action: _{action_ 1 _}_ ... Action: 

Figure A.4: System prompt in ALFWorld 

**Action space.** Agents interact with the environment through structured text commands. The action space contains navigation (go to [location]), perceptual query (look, examine [object]), object manipulation (take [object], put [object] in/on [receptacle]), and state modification (open/close [container], use 

15 

Published as a conference paper at ICLR 2026 


Figure A.5: The example scenes of RLBench simulator. 

[appliance]). Each action triggers deterministic state transitions with corresponding textual feedback, enabling agents to track environmental changes and plan subsequent steps. 

**Task specification and dataset construction.** This environment has 6 fundamental task templates that, when instantiated across various object-receptacle-room combinations, yield 1,304 unique scenarios. These tasks cover a lot of scenarios from simple object relocation to complex multi-stage procedures involving tool use. Each task requires agents to infer implicit subgoals, manage partial observability, and execute precise action sequences to achieve specified goal states. We utilize 6 task categories (4 seen, 2 unseen) with 4 scene categories (3 seen, 1 unseen) to form 1,304 episodes, and construct episodic dataset which contains task-trajectory pairs. 

### A.3 RLBENCH 

We evaluate in the RLBench simulator (James et al., 2020) for manipulation scenarios. Built on the CoppeliaSim simulator, RLBench provides diverse robotic platforms and a rich set of manipulation objects with varying complexity. We adapt this framework to support language-based task specification, enabling natural language instructions as input for our evaluation benchmark. 

**Environment structure.** RLBench includes tables, shelves, and storage units. Across the scenes we vary furniture layouts, object types, and initial states to reflect the heterogeneity of the real environment. Each scene contains 4-6 everyday objects distributed across tables, shelves, and storage units. 

**Action space.** The robot interacts through 6 primitive actions: open [object], pick [object], place [object] on [object], close [object], wipe [object], pour [object]. Each action is executed with collision checking and inverse kinematics validation in simulation. 

**[System]** 

You are a home robot agent. You can use 6 skills, ( _open [object], pick [object], place [object] on [object], close [object], wipe [object], pour [object]_ ). If the question is ”Action:” you should answer with a skill. If the question is ”Next observation:” you should answer with the next observation. You must answer only with what is requested and nothing else. 

**[User]** Instruction: _{instruction}_ Observation: _{observation}_ Action: 

Figure A.6: System prompt in RLBench 

16 

Published as a conference paper at ICLR 2026 


Figure A.7: The examples of the Real-world scenarios. 

**Task specification and dataset construction.** Tasks span home manipulations, object relocation/organization, surface cleaning, and container handling, and specify success as satisfying a target scene graph (e.g., (yellow plate, is, clean), (yellow plate, on, yellow dishrack)). Tasks embed state preconditions and sequential dependencies (e.g., pick sponge before wipe), encouraging planning that couples perception with action. We construct datasets across 4 task categories: Place (e.g., place knife on chopboard), Pour (e.g., pour water in cup), Clean (e.g., Clean the plate) (3 seen) and Putin (e.g., Put carrot in the frying pan) (1 unseen), paired with 6 scene categories (4 seen, 2 unseen), resulting in a total of 163 episodes for the seen datasets. 

### A.4 REAL-WORLD ENVIRONMENT 

We evaluate in a real-world setup using a Franka Research 3 robot arm for household manipulation scenarios. Our real-world experiments assess robustness, generalization, and closed-loop adaptability under sensing uncertainty and imperfect actuation. 

**Environment structure.** The workspace includes tables, shelves, and storage units. Across scenes we vary furniture layouts, object types, and initial states to reflect the heterogeneity of real homes. At episode start, the robot waits at a home pose, then uses RGB-D perception combined with VLM to extract scene-graph inference (object and relation candidates) to describe targets and constraints (e.g., container relations, surface placement, open/close capability). 

**Action space.** The robot interacts through nine primitive actions: open [object], pick [object], place on [object], close [object], wipe [object], pour [object], sweep [object], flip [object], push [object]. Each action is executed with collision checking and inverse kinematics validation. 

**Task specification and Dataset construction.** Tasks span canonical home manipulations, object relocation/organization, surface cleaning, and container handling, and specify success as satisfying a target scene graph (e.g., (yellow plate, is, clean), (yellow plate, on, yellow dishrack)). Tasks embed state preconditions and sequential dependencies (e.g., pick sponge before wipe), encouraging planning that couples perception with action. We construct 8 scenes (4 seen, 4 unseen) reflecting heterogeneous household setups, and define 3–5 tasks per scene for a total of 29 episodes. Each scene contains 8–12 everyday objects distributed across tables, shelves, and storage units. 

## B IMPLEMENTATION DETAILS 

In this section, we provide the implementation details of our proposed framework TMoW and each baseline. Our framework is implemented using Python v3.12 and trained on a system of an Intel(R) Core (TM) i9-10980XE processor and two NVIDIA RTX A6000 GPUs. 

17 

Published as a conference paper at ICLR 2026 

**[System]** You are a home robot agent. You can use 9 skills, ( _open [object], pick [object], place on [object], close [object], wipe [object], pour [object], sweep [object], flip [object], push [object]_ ). If the question is ”Action:” you should answer with a skill. If the question is ”Next observation:” you should answer with the next observation. You must answer only with what is requested and nothing else. **[User]** Instruction: _{instruction}_ Observation: _{observation}_ Action: 

Figure A.8: System prompt in Real-world Environment 

### B.1 BASELINES 

**ZSP.** We use the zero-shot policy (ZSP) as a non-adaptation reference to assess the improvements achieved by TMoW. A single pretrained LLM(Llama-3.2-3B-Instruct) receives the observation from the environment, which is injected into the prompt as described in Figure A.2 and A.4. The model generates the next action step by step without any fine-tuning or additional supervision. Our implementation follows the open-source<sup>1</sup> with only minimal I/O adjustments to match our environment API. 

**LLM+FT.** This baseline represents adaptation via fine-tuning on limited domain-specific data. It allows us to compare the efficiency and effectiveness of TMoW against conventional parameter adaptation. For the few-shot adaptation scenario, we further train the already fine-tuned model with the few-shot data from the target domain. 

**LLM-Planner.** We evaluate an embodied planner that leverages in-context learning for high-level reasoning. We aim to demonstrate the effectiveness of TMoW over in-context learning through this baseline. Given the current observation and instruction, relevant demonstration snippets are concatenated with the planner prompt, then the pretrained LLM proposes the next action. For data retrieval, we use a DPR-based sentence embedding model that collects relevant data from the same dataset employed in the fine-tuning of other baselines (LLM+FT, SayCanPay). For the few-shot adaptation scenario, we augment the dataset with the target domain examples. Our implementation follows the open-source<sup>2</sup> . 

**SayCanPay.** We include a Reinforcement Learning-based planner that integrates LLM reasoning with heuristic cost minimization. By comparing against this approach, we evaluate the effectiveness of TMoW. This baseline uses three models: (1) pretrained LLM(Llama-3.2-3B-Instruct) for the Say model, (2) environment-provided optimal affordances as the Can model, and a fine-tuned LLM(Llama-3.2-1B-Instruct) for the Pay model. The hyperparameters of SayCanPay are listed in Table A.1. We follow the implementation of the open-source<sup>3</sup> . 

**FLARE.** This state-of-the-art baseline extends conventional in-context learning with an environment-adaptive replanning module that revises plans based on observed scene states. We demonstrate the superiority of TMoW in cross-domain problems by comparing with the newest method. The retriever, conditioned on the observation and instruction, collects relevant dataset examples and builds the planner prompt. If the agent fails, the model substitutes targets via semantic similarity over observed objects when names mismatch. For the few-shot adaptation scenario, target- 

> 1https://github.com/huangwl18/language-planner 

> 2https://github.com/OSU-NLP-Group/LLM-Planner 

> 3https://github.com/RishiHazra/saycanpay 

18 

Published as a conference paper at ICLR 2026 

domain samples are additionally included in the training data. We follow the implementation of the open-source<sup>4</sup> . 

Table A.1: Hyperparameter settings and configurations of baselines 

|**Hyperparameter**|**Value**|
|---|---|
|Trainable model (LLM+FT, and Pay <sup>5</sup>)<br>|Llama-3.2-1B|
|Reasoning model for Simulation (ZSP, LLM-Planner, FLARE and Say <sup>6</sup>)<br>|Llama-3.2-3B|
|Reasoning model for Real-world (FLARE and Say <sup>6</sup>)|Llama-3.2-8B|
|Batch size|4|
|Gradient steps|200|
|Learning rate scheduler|cosine|
|Initial learning rate|5_×_10<sup>_−_5</sup>|
|Learning rate (for few-shot learning)|1_×_10<sup>_−_6</sup>|
|Temperature (both of Llama-3.2-1B and Llama-3.2-3B)|1_._0|


### B.2 TMOW (OURS) 

Our framework, Test-time Mixture of World Models (TMoW), builds upon the parameter-efficient MoE architecture (Li et al., 2024). We employ Llama-3.2-1B as our base model with LoRA for parameter-efficient fine-tuning. 

**Algorithms.** Detailed procedures of TMoW are described in Algorithms 1 through 3. Algorithm 1 describes the construction of the mixture of world models, which ranges from training each world model to extracting multi-granular prototypes. The second (Algorithm 2) contains details on testtime prototype refinement, focusing on how it works while interacting with the environment. The last algorithm (Algorithm 3) provides details of distilled model augmentation, describing the actual construction and training process of the augmented world model. 

**Detailed implementation of multi-granular prototype-based router.** The multi-granular prototype-based router adopts an MPNN (Gilmer et al., 2017) structure, specifically utilizing GCN models. A key consideration in our design is the _oversmoothing_ phenomenon inherent to MPNNs, where node representations become indistinguishable with increasing depth. To address this, we strategically limit MPNN layers while using standard MLPs for the remaining layers. Given that our base model (Llama-3.2-1B) contains 16 layers, we implement a hybrid architecture where the 0<sup>th</sup> , 4<sup>th</sup> , 8<sup>th</sup> , and 12<sup>th</sup> layers employ GCN to capture graph structure at multiple granularities, while all remaining layers use standard MLPs to preserve representational diversity. 

Each layer of MPNN aggregates information from neighboring nodes through three functions: message(MSG), aggregate(AGG), and update(UPD). These functions recurrently compute the hidden states for the observation graph _G_<sup>(</sup><sup>_o_)</sup> = ( **_V_** _,_ **_E_** _,_ **_R_** ) and the instruction _i_ . Specifically, the hidden state of the _l_<sup>th</sup> MPNN layer is computed by 


where the initial **_H_**<sup>(0)</sup> is the same as **_V_** . The three functions are computed by 


where **_D_**<sup>˜</sup> is a diagonal matrix such that **_D_**<sup>˜</sup> _jj_ =<sup>�</sup> _k_<sup>**_E_**˜</sup><sup>_jk_,</sup><sup>**_E_**˜is the context-aware edge matrix, and</sup><sup>_σ_</sup> is a sigmoid function. **_W_** _M_<sup>(</sup><sup>_l_)and</sup><sup>**_W_**(</sup> _U_<sup>_l_)are learnable weight matrices.</sup> 

> 4https://github.com/snumprlab/flare 

> 5Pay model in SayCanPay 

> 6Say model in SayCanPay 

19 

Published as a conference paper at ICLR 2026 

**Algorithm 1** Mixture of World Models Construction 

**Require:** Base model _M_ , demonstrations _{Dj}_<sup>_N_</sup> _j_ =1<sup>, learning rate</sup><sup>_η_1and</sup><sup>_η_2, gradient steps</sup><sup>_T_1and</sup> _T_ 2 **Ensure:** Mixture of world models _M ⊕{mj}_<sup>_N_</sup> _j_ =1<sup>, prototypes</sup><sup>_{_</sup><sup>**_p_**(</sup> _j_<sup>_l_)</sup><sup>_}_</sup> _j_<sup>_N_</sup> =1<sup>for each layer</sup><sup>_l_</sup> 1: **for** each domain _j ∈{_ 1 _, ..., N }_ **do** 2: // Adapter training 3: Initialize the adapter _mj_ 4: **for** _step_ := 1 **to** _T_ 1 **do** 5: Sample mini-batch _B_ from demonstration _Dj_ 6: Train adapter _mj_ on mini-batch data _B_ : 7: _mj ← mj − η_ 1 _∇mj_ �E( _·,⃗τ_ ) _∈BL_ TF( _M ⊕ mj,⃗τ_ )� 8: **end for** 9: // Prototype extraction 10: **for** each layer _l ∈{_ 1 _, · · · , L}_ **do** 11: Sample mini-batch _B_ from demonstration _Dj_ 12: Extract prototype using MPNN: **_p_**<sup>(</sup> _j_<sup>_l_)</sup> := E( _i,⃗τ_ ) _∈B_ E( _o,·,·_ ) _∈⃗τ_ [ _f_<sup>(</sup><sup>_l_)</sup> ( _G_<sup>(</sup><sup>_o_)</sup> _, i_ )] 13: **end for** 14: **end for** 15: // Mixture of world models construction 16: **for** _step_ := 1 **to** _T_ 2 **do** 17: Sample mini-batch _B_ from a combination of the demonstrations _∪_<sup>_N_</sup> _j_ =1<sup>_Dj_</sup> 18: Train mixture of world models _M ⊕{mj}_<sup>_N_</sup> _j_ =1<sup>on mini-batch data</sup><sup>_B_:</sup> 19: _mj ← mj − η_ 2 _∇mj_ �E( _·,⃗τ_ ) _∈BL_ TF( _M ⊕{mj}_<sup>_N_</sup> _j_ =1<sup>_,⃗τ_)</sup> � _∀j ∈{_ 1 _, · · · , N }_ 20: **end for** 21: **return** Mixture of world models _M ⊕{mj}_<sup>_N_</sup> _j_ =1<sup>, prototypes</sup><sup>_{_</sup><sup>**_p_**(</sup> _j_<sup>_l_)</sup><sup>_}_</sup> _j_<sup>_N_</sup> =1<sup>for each layer</sup><sup>_l_</sup> 

**Detailed implementation of context-aware edge matrix.** In equation A.2, we adjust the amount of the aggregation based on the instruction and context. The context-aware edge matrix **_E_**<sup>˜</sup> is calculated as 


where _⊙_ represents the Hadamard product and **_I_** is the identity matrix. 

To incorporate the instruction into prototypes, we introduce an adjustment function _f_ adj that modulates neighbor information aggregation based on these inputs: 


Here, _f_ gate is a gate function (e.g., ReLU) and _d_ is the embedding dimension. The adjacency function employs a cross-attention mechanism that captures the interaction between observations and context. Specifically, we project the hidden states and context into query and key spaces by 


where **_WQ_**<sup>(</sup><sup>_l_</sup> _H_<sup>),</sup><sup>**_W_**</sup> **_Q_**<sup>(</sup><sup>_l_</sup> _i_<sup>),</sup><sup>**_W_**</sup> **_K_**<sup>(</sup><sup>_l_)</sup> _H_<sup>,and</sup><sup>**_W_**</sup> **_K_**<sup>(</sup><sup>_l_)</sup> _i_<sup>arelearnableweightmatrices,andΦdenotesembedding</sup> functions for instructions, e.g., from language models. 

**Router pretraining.** We pretrain the router using contrastive learning with a compound loss function. For input data **X** = _{G_ 1 _, G_ 2 _, . . . , GN }_ , we define an instance-level contrastive loss that learns augmentation-invariant representations: 


Additionally, we incorporate a domain-aware contrastive loss that encourages domain clustering: 


20 

Published as a conference paper at ICLR 2026 

**Algorithm 2** Test-time Prototype Refinement 

**Require:** Test environment Env : ( _O, A_ ) _→O_ , instruction _i_ 1: Take an initial observation _o_ from the environment 2: **repeat** 3: // Step 1: Prototype-based routing 4: **for** each layer _l ∈{_ 1 _, · · · , L}_ **do** 5: Extract domain embedding: _E_<sup>(</sup><sup>_l_)</sup> = _f_<sup>(</sup><sup>_l_)</sup> ( _G_<sup>(</sup><sup>_o_)</sup> _, i_ ) 6: Compute routing scores: _wj_<sup>(</sup><sup>_l_)</sup> = sim( _E_<sup>(</sup><sup>_l_)</sup> _,_ **_p_**<sup>(</sup> _j_<sup>_l_)) for all</sup><sup>_j_</sup> 7: Sparsify and normalize: ( ¯ _w_ 1<sup>(</sup><sup>_l_)</sup><sup>_, · · ·,w_¯</sup> _N_<sup>(</sup><sup>_l_)) = softmax(top</sup> _K_<sup>((</sup><sup>_w_</sup> 1<sup>(</sup><sup>_l_)</sup><sup>_, · · ·, w_</sup> _N_<sup>(</sup><sup>_l_))</sup><sup>_/τ_))</sup> 8: **end for** 9: // Step 2: Mixture of world model execution 10: _y_<sup>(0)</sup> := ( _i, o_ ) 11: **for** each layer _l ∈{_ 1 _, · · · , L}_ **do** 12: _y_<sup>(</sup><sup>_l_)</sup> := _M_<sup>(</sup><sup>_l_) �</sup> _y_<sup>(</sup><sup>_l−_1)�</sup> +<sup>�</sup><sup>_N_</sup> _j_ =1<sup>_w_¯</sup> _j_<sup>(</sup><sup>_l_)</sup><sup>_m_(</sup> _j_<sup>_l_)</sup> � _y_<sup>(</sup><sup>_l−_1)�</sup> 13: **end for** 14: Predicted action _a_ := _y_<sup>(</sup><sup>_L_)</sup> 15: Take next observation _o ←_ Env( _o, a_ ) 16: // Step 3: Test-time prototype refinement 17: **for** each layer _l ∈{_ 1 _, · · · , L}_ **do** 18: **for** _j ∈{_ 1 _,_ 2 _, · · · , N }_ **do** 19: _rj,k_ := sim( **_p_**<sup>(</sup> _j_<sup>_l_)</sup><sup>_,_</sup><sup>**_p_**</sup> _k_<sup>(</sup><sup>_l_))</sup> _∀k ∈{_ 1 _, · · · , N }_ 20: (¯ _rj,_ 1 _, · · · ,_ ¯ _rj,N_ ) := softmax(( _rj,_ 1 _, · · · , rj,N_ ) _/τr_ ) 21: Compute refinement term: ∆ **_p_**<sup>(</sup> _j_<sup>_l_)</sup> :=<sup>�</sup><sup>_N_</sup> _k_ =1<sup>_r_</sup> _j,k_<sup>(</sup><sup>_l_)</sup><sup>**_p_**</sup> _k_<sup>(</sup><sup>_l_)</sup> 22: Update prototypes: **_p_**<sup>(</sup> _j_<sup>_l_)</sup> _←_ (1 _− α_ sim( _E_<sup>(</sup><sup>_l_)</sup> _,_ **_p_**<sup>(</sup> _j_<sup>_l_)))</sup><sup>**_p_**(</sup> _j_<sup>_l_)</sup> + _α_ sim( _E_<sup>(</sup><sup>_l_)</sup> _,_ **_p_**<sup>(</sup> _j_<sup>_l_))∆</sup><sup>**_p_**(</sup> _j_<sup>_l_)</sup> 23: **end for** 24: **end for** 25: **until** episode done **Algorithm 3** Distilled Model Augmentation **Require:** Few-shot demonstrations _D_<sup>_′_</sup> , learning rate _η_ , gradient steps _T_ **Ensure:** Distilled mixture of world models _M ⊕{mj}_<sup>_N_</sup> _j_ =1<sup>+1, prototypes</sup><sup>_{_</sup><sup>**_p_**(</sup> _j_<sup>_l_)</sup><sup>_}N_</sup> _j_ =1<sup>+1for each layer</sup><sup>_l_</sup> 1: **if** few-shot demonstrations _D_<sup>_′_</sup> available for unseen domain **then** 2: Construct combined graph and take instruction: _G_<sup>_′_</sup> , _i_<sup>_′_</sup> from observations in _D_<sup>_′_</sup> 3: **for** each layer _l ∈{_ 1 _, · · · , L}_ **do** 4: Forward through MPNN to get routing scores: ( ¯ _w_ 1<sup>(</sup><sup>_l_)</sup><sup>_, · · ·,w_¯</sup> _N_<sup>(</sup><sup>_l_))</sup> 5: Initialize new adapter: _m_<sup>_′_(</sup><sup>_l_)</sup> :=<sup>�</sup><sup>_N_</sup> _j_ =1<sup>_w_¯</sup> _j_<sup>(</sup><sup>_l_)</sup><sup>_m_(</sup> _j_<sup>_l_)</sup> 6: Compute new prototype: **_p_**<sup>_′_(</sup><sup>_l_)</sup> := _f_<sup>(</sup><sup>_l_)</sup> ( _G_<sup>_′_</sup> _, i_<sup>_′_</sup> ) 7: **end for** 8: **for** _step_ := 1 to _T_ **do** 9: Fine-tune _m_<sup>_′_</sup> on _D_<sup>_′_</sup> : 10: _m_<sup>_′_</sup> _← m_<sup>_′_</sup> _− η∇m′_<sup>�</sup> E( _·,⃗τ_ ) _∈D′L_ TF( _M ⊕ m_<sup>_′_</sup> _,⃗τ_ )� 11: **end for** 12: _mN_ +1 := _m_<sup>_′_</sup> ; **_p_**<sup>(</sup> _N_<sup>_l_)</sup> +1<sup>:=</sup><sup>**_p_**</sup><sup>_′_(</sup><sup>_l_)</sup> _∀l ∈{_ 1 _, · · · , L}_ 13: Add to model mixture: _{mj}_<sup>_N_</sup> _j_ =1<sup>+1and layer-wise prototype set:</sup><sup>_{_</sup><sup>**_p_**(</sup> _j_<sup>_l_)</sup><sup>_}N_</sup> _j_ =1<sup>+1</sup> 14: **end if** 15: **return** Mixture of world models _M ⊕{mj}_<sup>_N_</sup> _j_ =1<sup>+1, prototypes</sup><sup>_{_</sup><sup>**_p_**(</sup> _j_<sup>_l_)</sup><sup>_}N_</sup> _j_ =1<sup>+1for each layer</sup><sup>_l_</sup> 

The final training loss _L_ CL combines two contrastive losses: 


21 

Published as a conference paper at ICLR 2026 

where Ψ1 _,_ Ψ2 are augmentation functions for creating different views, sim( _·, ·_ ) is the similarity metric (e.g., cosine similarity), _d_ [ _m_ ] denotes the domain label of graph _Gm_ , _τ_ is the temperature parameter for contrastive learning, and _λ_ is the balancing coefficient between instance and domain objectives. 

**Hyperparameters.** The hyperparameters of TMoW are listed in Table A.2. 

Table A.2: Hyperparameter settings and configurations of TMoW training 

|**Hyperparameter**|**Value**|
|---|---|
|_Common_||
|Base model|Llama-3.2-1B|
|Learning rate scheduler|cosine|
|Warmup steps|200|
|Temperature|1_._0|
|_World models_||
|Batch size|16|
|Rank of LoRA|32|
|Gradient steps|2000|
|Initial learning rate|1_×_10<sup>_−_5</sup>|
|_TMoW_||
|Batch size|1|
|Gradient steps|10000|
|Initial learning rate|1_×_10<sup>_−_4</sup><br>|
|Learning rate (for few-shot learning)|1_×_10<sup>_−_7</sup>|


## C ADDITIONAL ANALYSIS 

### C.1 EXTENSION RESULTS 

Table A.3: Few-shot expansion performance in VirtualHome and ALFWorld. 

|**Unseen domains**,_VirtualHome_|_1-Sh_|_ot_|_5-Sho_|_t_|_Avera_|_ge_|
|---|---|---|---|---|---|---|
|Baselines|SR (_↑_)|PS (_↓_)|SR (_↑_)|PS (_↓_)|SR (_↑_)|PS (_↓_)|
|LLM+FT|50_._46%_±_0.44%|19_._51_±_0.05|54_._36%_±_7.18%|18_._55_±_0.04|52_._41%_±_3.81%|19_._03_±_0.04|
|LLM-Planner (Song et al., 2023)|40_._97%_±_6.02%|22_._07_±_0.19|43_._61%_±_0.92%|21_._06_±_0.17|43_._30%_±_3.33%|21_._45_±_0.15|
|FLARE (Kim et al., 2025)|42_._17%_±_0.37%|22_._19_±_0.19|46_._64%_±_7.02%|20_._67_±_0.12|42_._29%_±_3.47%|21_._56_±_0.18|
|SayCanPay (Hazra et al., 2024)<br>TMoW|54_._98%_±_2.09%<br>**81.56%**_±_**1.69%**|17_._77_±_0.04<br>**13.20**_±_**0.48**|58_._88%_±_10.63%<br>**83.61%**_±_**1.33%**|16_._92_±_0.22<br>**12.04**_±_**0.64**|56_._93%_±_6.36%<br>**82.59%**_±_**1.49%**|17_._35_±_0.13<br>**12.62**_±_**0.56**|
|**Unseen domains**,_ALFWorld_|_1-Sh_|_ot_|_5-Sho_|_t_|_Avera_|_ge_|
|Baselines|SR (_↑_)|PS (_↓_)|SR (_↑_)|PS (_↓_)|SR (_↑_)|PS (_↓_)|
|LLM+FT|43_._12%_±_2.00%|40_._18_±_0.32|48_._86%_±_1.06%|35_._14_±_2.24|45_._99%_±_1.53%|37_._66_±_1.28|
|LLM-Planner (Song et al., 2023)|8_._91%_±_1.51%|47_._43_±_0.64|7_._39%_±_0.22%|46_._79_±_0.00|8_._18%_±_0.87%|47_._11_±_0.32|
|FLARE (Kim et al., 2025)|12_._28%_±_0.23%|43_._67_±_0.88|11_._46%_±_0.54%|44_._40_±_0.79|11_._87%_±_0.39%|44_._04_±_0.84|
|SayCanPay (Hazra et al., 2024)<br>TMoW|46_._08%_±_1.33%<br>**71.28%**_±_**0.05**%|39_._00_±_0.33<br>**34.23**_±_**15.56**|49_._34%_±_1.18%<br>**71.88%**_±_**0.01**%|37_._55_±_0.24<br>**25.73**_±_**14.40**|47_._71%_±_1.92%<br>**71.58%**_±_**0.03**%|38_._28_±_0.29<br>**29.98**_±_**14.98**|


**Few-shot expansion scenario.** We evaluate few-shot expansion scenarios, where each target domain provides only a few demonstrations at test time. This setup examines how effectively TMoW expands its knowledge through distilled mixture-based augmentation with minimal supervision. Table A.3 compares performance across different few-shot settings (1 and 5 shots) in VirtualHome and ALFWorld, illustrating how the number of available demonstrations affects adaptation quality. As shown, TMoW surpasses all baselines, achieving on average a 25.66% gain in SR and 4.73 step reduction in PS in VirtualHome, and a 23.87% gain in SR and 8.30 step reduction in PS in ALFWorld, compared to SayCanPay. 

22 

Published as a conference paper at ICLR 2026 

These results demonstrate that our distilled mixture-based augmentation efficiently achieves additional performance improvements through knowledge expansion while maintaining the modularity of the overall framework. 

**Outdoor environment.** We conducted additional experiments in CARLA, an outdoor autonomous driving simulator, to validate TMoW’s effectiveness in outdoor environments. We configured 6 town scenes (Town01-04 as seen, Town05, 06 as unseen). Table A.4 shows that TMoW achieves 47.49% SR and 12.03 PS, significantly outperforming baselines (FLARE: 18.34% SR, 27.51 PS). The outdoor environment presents different challenges from indoor settings, including varying weather conditions, diverse road structures, and multiple moving agents. TMoW’s test-time adaptation effectively handles these environmental variations. 

Table A.4: Performance comparison in CARLA outdoor environment 

|Method|SR (_↑_)|PS (_↓_)|
|---|---|---|
|FLARE|18.34%|27.51|
|TMoW (Ours)|**47.49%**|**12.03**|


**Vision-language model integration.** To enable direct processing of RGB visual observations, we integrated a pre-trained Vision-Language Model (VLM) as a graph generation module upstream of our pipeline. The VLM processes raw RGB images into text-based observations, extracting objects, relations, and states that are then converted into our graph structure. 

Table A.5 presents the performance comparison between text-based and vision-based inputs in VirtualHome. Vision-based TMoW achieves 75.05% SR and 13.93 PS, showing a moderate decrease from text-based input (80.16% SR, 13.20 PS). This gap is attributed to noise in VLM’s object detection and relation extraction compared to ground-truth text descriptions. However, the results demonstrate that TMoW effectively operates with real visual observations, maintaining substantial performance advantages over baselines even with noisy visual inputs. 

Table A.5: Performance with Vision-Language Model integration in VirtualHome 

|Input Type|SR (_↑_)|PS (_↓_)|
|---|---|---|
|Text-based (Ground Truth)|80.16%|13.20|
|Vision-based (VLM)|75.05%|13.93|


These results validate that our graph-based approach is robust to different input modalities and can be seamlessly integrated with vision systems for real-world deployment, despite the inherent noise in visual perception systems. 

### C.2 MULTI-GRANULAR ROUTING FOR OVERLAPPING DOMAIN FEATURES 

Our multi-granular prototype-based routing addresses domains with overlapping features at specific granularity levels. When domains share characteristics at one granularity while differing at others (e.g., office and classroom with distinct objects but similar spatial layouts), single-granularity approaches cannot leverage these complementary distinctions. Our layer-wise approach exploits these differences across abstraction levels. Early layers distinguish domains through unique local features, while deeper layers may show convergence when global scene structures are similar. 

Figure A.9 demonstrates routing score distributions for domains with shared global features but distinct local objects. Initial layers show clear separation as different object types (office equipment vs. educational materials) activate distinct experts. As layers progress, routing patterns converge when domains share similar global layouts (rectangular rooms with central tables and peripheral storage). This pattern validates that our multi-granular approach captures both distinctive and shared characteristics at appropriate levels. 

23 

Published as a conference paper at ICLR 2026 


Figure A.9: The comparison of the routing score distribution. 

### C.3 CORRELATION WITH ROUTING SCORE ENTROPY AND PERFORMANCE 

Our analysis uncovers an insight that the routing score entropy distributions directly impact model performance. We observe that successful episodes demonstrate higher routing entropy than failed ones. 

Figure A.10 compares the distribution of the routing score entropy between Success and Fail cases on unseen domains. Success cases exhibit higher entropy values (mean = 0.23, blue dashed line) compared to failed cases (mean = 0.20, red dashed line), demonstrating that distributed routing patterns correlate with task success. This indicates that leveraging diverse world models through higher entropy routing enables the framework to capture multiple domain characteristics simultaneously, leading to more robust adaptation and improved performance in complex, unseen domains. 


Figure A.10: The comparison of the routing score entropy distribution between success and failed case. 

### C.4 ANALYSIS FOR REFINEMENT RATE _α_ 

Figure A.11 illustrates the impact of the refinement rate _α_ on success rate. When _α_ is too small, insufficient refinement occurs, leading to degraded performance compared to the baseline. This suggests that with low _α_ values, refinement acts as noise rather than meaningful adaptation. Due to the test-time refinement nature where updates occur during inference, insufficient learning rates require too many steps to converge, harming performance. 

However, once _α_ reaches a sufficient threshold ( _α ≥_ 0 _._ 5), the model consistently achieves performance above the baseline (red dashed line) and can rapidly adapt within fewer steps. This demonstrates that while an appropriately sized refinement rate is crucial for enabling efficient test-time adaptation, our framework robustly improves performance once this threshold is met, validating the effectiveness of our approach across a range of hyperparameter settings. 

24 

Published as a conference paper at ICLR 2026 


Figure A.11: The success rate per refinement rate _α_ in test-time prototype refinement. 

### C.5 COMPUTATION OVERHEAD 

As shown in Table A.6, ZSP and LLM+FT exhibit the lowest latency, followed by our TMoW approach which achieves the next best performance. While our method uses Llama-3.2-1B in experiments, the baselines such as LLM-Planner, FLARE, SayCanPay, employ larger Llama-3.2-3B models for reasoning without training. Moreover, in-context learning methods like LLM-Planner and FLARE suffer from increased latency due to lengthy prompt processing. SayCanPay shows significantly higher latency as it requires inference across multiple models. 

In contrast, our TMoW leverages adapter-based MoE architecture, enabling efficient test-time adaptation while maintaining competitive inference speed through lightweight parameter updates and selective world model routing. The prototype refinement component introduces an average overhead of only 43.40 ms, indicating that the refinement stage remains computationally minor relative to the overall inference process. 

Table A.6: Average latency comparison across baselines. 

|Baselines|Latency (ms)|
|---|---|
|ZSP|115.43 _±_24.91|
|LLM+FT|115.87 _±_24.88|
|LLM-Planner|740.46 _±_40.42|
|FLARE|917.44 _±_49.16|
|SayCanPay|2470.30 _±_106.06|
|TMoW-NoRefine|656.72 _±_15.71|
|TMoW|700.12 _±_88.41|


25 

