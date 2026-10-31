---
title: "VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model"
date: "2026-05-02"
authors: "Wenhao Li; Xiu Su; Yichao Cao; Hongyan Xu; Xiaobo Xia; Shan You"
venue: "ICML 2026"
url: https://arxiv.org/abs/2605.01194
pdf: https://arxiv.org/pdf/2605.01194
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.01194)** / [論文ページ](https://arxiv.org/abs/2605.01194)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model** 

**Wenhao Li**<sup>1</sup> **Xiu Su**<sup>2</sup> **Yichao Cao**<sup>2</sup> **Hongyan Xu**<sup>2</sup> **Xiaobo Xia**<sup>3</sup> **Shan You**<sup>4</sup> **Yi Chen**<sup>5</sup> **Chang Xu**<sup>1</sup> 

## **Abstract** 

Vision-Language-Action (VLA) models have demonstrated remarkable capabilities and generalization in embodied manipulation. However, their decision-making relies on a fast, instinctive process that lacks deliberation. This strategy often leads to suboptimal or catastrophic actions when facing complex or ambiguous scenarios that require greater consideration. In this paper, we introduce **VLA-ATTC** , a framework that endows VLA models with adaptive test-time compute (TTC). VLA-ATTC employs an uncertainty-based “cognitive clutch” to dynamically transition from reflexive execution to a TTC deliberation phase when necessary. During TTC phase, a novel **Relative Action Critic** (RAC) model identifies the optimal action from generated candidates via pairwise comparisons. This relative mechanism replaces unstable absolute value estimation, significantly simplifying the learning objective. Furthermore, we introduce an efficient sampling strategy to amortize computational costs and an automated data pipeline that curates preference pairs without manual annotation. On the LIBERO-LONG benchmark, VLA-ATTC reduces the failure rate of the SOTA model PI0.5 by over 50%. 

## **1 Introduction** 

The advent of VLA models (Team et al., 2024; Black et al., 2024; Kim et al., 2024; Shukor et al., 2025; Kim et al., 2025; Li et al., 2024; Xu et al., 2025c;b; Yang et al., 2026; Li et al., 2026a;b) marks a significant milestone in Embodied AI (Liu et al., 2025; Paolo et al., 2024; Memarian & Doleck, 2024; Duan et al., 2022; Fung et al., 2025; Feng et al., 2025; Li et al., 2025c;d; Chen et al., 2026; Li et al., 

1University of Sydney 2Central South University 3University of Science and Technology of China 4Sensetime Research 5Hong Kong University of Science and Technology. Correspondence to: Xiu Su, Chang Xu _<_ xiusu1994@csu.edu.cn, c.xu@sydney.edu.au _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 


_Figure 1._ Performance overview and efficiency comparison. 

2021; 2023; Tan et al., 2025). By leveraging the vast world knowledge embedded in pre-trained backbones (Wang et al., 2025a; Zeng et al., 2026; Li et al., 2025b), these models have demonstrated impressive generalization capability across diverse complex manipulation tasks. However, their decisionmaking is governed by a fast, intuitive inference process (Xu et al., 2025a). While this fast, intuitive strategy is sufficient for simple scenarios, it often leads to suboptimal or even catastrophic failures when facing complex or ambiguous situations that require deeper deliberation. This capability gap raises a fundamental question: _How can we endow VLA models with a powerful deliberation process, enabling them to evolve from fast, intuitive System 1 reasoning to the more considerate inference of System 2?_ 

Conceptually, deliberation can be classified into sequential and parallel paradigms (Muennighoff et al., 2025; Zhang et al., 2025; Li et al., 2025a; Huang et al., 2025; Zeng et al., 2025). Sequential approaches (Miao et al., 2024; Wang et al., 2025c), such as Chain-of-Thought (CoT) (Wang & Zhou, 2024; Xia et al., 2024; Chen et al., 2025; Yeo et al., 2025), have seen some exploration in VLA models (Zhao et al., 2025; Liu et al., 2024; Black et al., 2025; Zhou et al., 2025b;a; Song et al., 2025; Lin et al., 2025). However, these methods impose significant overhead, necessitating costly fine-tuning, laborious CoT data annotation, and often degrading action performance by forcing action-centric models to generate text reasoning. 

In contrast, parallel deliberation strategies (Sessa et al., 2024; Zhang et al., 2024; Wang et al., 2025d; 2024b;a)—wherein the model generates a set of candidates and deliberates to select the one with the highest value—align better with the nature of embodied decision- 

1 

**VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model** 


_Figure 2._ Comparison of VLA inference paradigms. (a) Standard Inference is fast but prone to failure in complex scenarios. (b) Sequential Deliberation needs costly retraining and data annotation. (c) Existing Parallel Deliberation incurs high costs and relies on unstable absolute scoring. (d) VLA-ATTC triggers deliberation only on hard situations, employing RAC model for robust candidate selection. 

making. However, its exploration in VLA models remains nascent. Some works attempt (Kwok et al., 2025; Nakamoto et al., 2024) to employ a large-scale external critic model to select the best action from large number of candidates, while others (Guo et al., 2025) utilize a world model to guide exploration in a Monte Carlo Tree Search-like pattern. Although pioneering, these approaches apply deliberation to all scenarios indiscriminately and their deliberation processes are prohibitively costly, rendering them impractical for real-world application. This highlights that practical parallel deliberation methods for VLA models must address three critical challenges: _i) quantifying situational difficulty for adaptive deliberation_ ; _ii) minimizing the computational overhead of multi-action sampling_ ; and _iii) designing a lightweight yet high-fidelity action critic model._ 

To address these challenges, we introduce VLA-ATTC, a framework that equips VLA models with adaptive test-time deliberation without modifying the base model. VLA-ATTC incorporates a “cognitive clutch” that monitors uncertainty in the base VLA’s generation, triggering TTC deliberation phase only when necessary. During TTC phase, we mitigate candidates sampling costs via an efficient parallel strategy that amortizes vision-language computation. To solve the evaluation bottleneck, we propose a lightweight yet highly accurate relative critic model. This model shifts from predicting an absolute score to making a relative comparison—asking “Is action A preferable to action B?”—dramatically reduces the training difficulty and the required capacity of the evaluation model. Finally, to ensure scalability, we introduce an automated pipeline that curates high-quality preference pairs from existing manipulation datasets, eliminating the need for manual annotation. To sum up, our contributions are as follows: 

- We propose VLA-ATTC, a plug-and-play framework that enables VLA models to adaptively trigger an efficient test-time deliberation phase in uncertain scenar- 

ios, requiring no fine-tuning of the base model. 

- We design a lightweight yet robust RAC model, which identifies optimal actions via iterative pairwise comparisons, overcoming the accuracy and efficiency bottlenecks of prior parallel deliberation methods. 

- We develop a fully automated data pipeline that curates high-quality preference pairs directly from existing datasets, bypassing laborious manual data collection. 

- Extensive experiments demonstrate that VLA-ATTC reduces LIBERO-LONG’s SOTA failure rate by over 50% and boosts real-world success by 17.3% while maintaining a practical 20.8 Hz control frequency. 

### **Conflict of Interest Disclosure** None. 

## **2 Related Work** 

**Sequential Deliberation in VLA models.** Early approaches like ECoT (Zawalski et al., 2024), CoT-VLA (Zhao et al., 2025), RoboMamba (Liu et al., 2024) and PI0.5 (Black et al., 2025) output predefined, structured information, such as sub-task decompositions, before an action. Subsequent works like ChatVLA (Zhou et al., 2025b), ChatVLA2 (Zhou et al., 2025a), Hume (Song et al., 2025), and OneTwoVLA (Lin et al., 2025) moved towards generating more adaptive, free-form natural language thoughts. However, all approaches demand costly fine-tuning to adapt the VLA for the auxiliary task of reasoning. Furthermore, they possess a conflict between the optimization of text and action. 

**Parallel Deliberation in VLA models.** Parallel deliberation typically employs Best-of-N sampling (Sessa et al., 2024; Zhang et al., 2024; Wang et al., 2025d; Verdun et al., 2025; Toshniwal et al., 2025; Nguyen et al., 2025) or SelfConsistency (Wang et al., 2024b;a; Prasad et al., 2024; Wang et al., 2025b). For VLAs, one direction (Guo et al., 2025) uses a world model to guide Monte Carlo Tree Search, but is hampered by the immense computational cost and the lim- 

2 

**VLA-ATTC: Adaptive Test-Time Comp** 

**ute for VLA Models with Relative Action Critic Model** 

ited fidelity of world models in real-world scenarios. Others (Kwok et al., 2025; Nakamoto et al., 2024) sample numerous action candidates and use a large external critic model for selection. However, their indiscriminate deliberation is costly, and the absolute action scoring is unstable. 

## **3 Preliminaries: VLA Inference Paradigm** 

Contemporary VLA models, such as PI0 (Black et al., 2025), typically operate in a two-stage inference process. Given a multi-modal observation at timestep _t_ , comprising an image _It_ and a language instruction _T_ , the process is as follows: **Vision-Language Encoding:** A high-capacity, pre-trained VLM backbone, Φ _V LM_ , processes the inputs to produce a rich, multi-modal context embedding or inner features, _Ct_ : 


This context _Ct_ encapsulates the semantic understanding of the scene and the task objective. This operation, often involving a forward pass through a large Transformer, is computationally intensive. 

**Action Decoding:** A specialized action head, Ψ _Action_ , then conditions on this context _Ct_ to generate an action chunk _at_ : 


where **z** represents the initial noise vector or random seed required for the stochastic generation process. Modern VLAs predominantly employ generative models like diffusion or flow-matching for this stage. 

Critically, the computational cost is highly asymmetric. The VLM encoding constitutes the vast majority of the latency, a process we term “pre-filling”. In contrast, the action decoding, even with multiple sampling steps, is significantly faster. For example, in PI0 policy, action decoding accounts for only 27ms of the total 86ms inference time on RTX4090. Our VLA-ATTC framework is designed such that multiple action candidates can be sampled efficiently by performing the expensive pre-fill operation only once per timestep, amortizing its cost across all generated actions. 

## **4 VLA-ATTC** 

### **4.1 Uncertainty Quantification as Clutch** 

A practical test-time deliberation method should only be activated when necessary to ensure manageable inference overhead. To evaluate the necessity of deliberation, we first need to quantify the model’s uncertainty. Lower uncertainty implies greater model confidence, thus requiring less deliberation. We posit that a confident model will produce consistent actions despite variations in the random seed _z_ , while an uncertain model will exhibit high variance. 

At each timestep _t_ , we generate two action chunks, _a_ 1 and 

**Algorithm 1** VLA-ATTC Inference 

**Require:** VLM Backbone Φ _V LM_ , Action Head Ψ _Action_ , Relative Action Critic _R_ , Image _It_ , Instruction _T_ , State _st_ , Uncertainty threshold _τ_ , Candidate count _N_ 1: _Ct ←_ Φ _V LM_ ( _It, T_ ) _▷_ Prefill VLM once 2: _a_ 1 _, a_ 2 _←_ Ψ _Action_ ( _Ct_ ) _▷_ Generate two actions 3: _Ut ←_ DTW( _a_ 1 _, a_ 2) _▷_ Calculate DTW as uncertainty 4: **if** _Ut < τ_ **then** _▷_ High confidence 5: _afinal ← a_ 1 6: **else** _▷_ Low confidence: trigger deliberation 7: _A ←{ai}_<sup>_N_</sup> _i_ =1<sup>_←_Ψ</sup><sup>_Action_(</sup><sup>_Ct_)</sup><sup>_▷_Batch Generation</sup> 8: **while** LEN( _A_ ) _>_ 1 **do** 9: _Anext ←∅ ▷_ Initialize next round’s winners 10: **for** ( _ai, aj_ ) in PAIRWISE( _A_ ) **do** 11: _pij ←R_ ( _ai, aj, Ct, st_ ) _▷_ RAC predicts 12: **if** _pij ≥_ 0 _._ 5 **then** 13: ADD( _Anext, ai_ ) 14: **else** 15: ADD( _Anext, aj_ ) 16: **end if** 17: **end for** 18: _A ←Anext ▷_ Update candidate set 19: **end while** 20: _afinal ←A_ [0] _▷_ Single best action remains 21: **end if** 22: EXECUTE( _afinal_ ) 

_a_ 2, by sharing the VLM context _Ct_ but using different seeds: 


The additional overhead from the second action is negligible with shared pre-filling. Let each action chunk be a sequence of _H_ poses, _a_ = ( _p_<sup>1</sup> _, . . . , p_<sup>_H_</sup> ), where each pose _p_<sup>_k_</sup> _∈_ R<sup>_D_</sup> and _D_ is the action dimension. To measure the consistency between these two action chunks, we employ Dynamic Time Warping (DTW) distance. 

To compute the DTW distance, we construct an _H × H_ cumulative cost matrix Γ. Each element Γ( _i, j_ ) stores the minimum cumulative cost required to align the first _i_ poses of _a_ 1 with the first _j_ poses of _a_ 2. This matrix is computed iteratively using the following recurrence relation: 


where _d_ ( _p_ 1<sup>_i, pj_</sup> 2<sup>) is a local cost measure, which we define as</sup> the Euclidean distance _||p_ 1<sup>_i−pj_</sup> 2<sup>_||_2 between the two poses.</sup> The matrix is initialized with Γ(0 _,_ 0) = 0 and Γ( _i,_ 0) = Γ(0 _, j_ ) = _∞_ for _i, j >_ 0. 

The final scalar uncertainty score _Ut_ is the total cumulative cost found in the top-right corner of the matrix, representing 

3 

**VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model** 


_Figure 3._ The overall architecture of the VLA-ATTC framework. The process begins with the “Cognitive Clutch” (Sec 4.1), which quantifies the VLA’s action generation uncertainty. If uncertainty is low , the model executes the initial action reflexively. If uncertainty exceeds the threshold, the Deliberation Phase (Sec 4.2) is activated. This phase 1) efficiently generates N action candidates in parallel by amortizing the expensive VLM backbone computation, and 2) employs a Tournament Selection mechanism. Our lightweight Relative Action Critic model then performs iterative pairwise comparisons to identify the final optimal action. 

the optimal alignment cost between the two full sequences: 


The uncertainty score _Ut_ serves as a signal for our “Cognitive Clutch”. We establish a threshold _τ_ by taking the K-th percentile of uncertainty scores computed over an offline dataset. At test-time, the final policy _π_ deploy adaptively switches between reflexive execution and TTC Deliberation: 


### **4.2 TTC Deliberation Phase** 

When TTC deliberation is triggered, we first generate _N_ candidate action chunks _{a_ 1 _, ..., aN }_ parallel with the action head Ψ _Action_ and prefilled context _Ct_ : 


The parallel batched sampling makes the cost of generating multiple candidates marginal. 

Then we need to select the best action from these candidates. A significant challenge in this process is the inherent difficulty of action quality evaluation. Assigning an absolute, scalar quality score to a complex action chunk is often illdefined and ambiguous. To circumvent this, our framework reframes the evaluation from absolute scoring to relative, pairwise comparison. We posit that determining whether action _ai_ is preferable to _aj_ (denoted _ai ≻ aj_ ) given the current context is a more well-defined and less biased task. 

We leverage this principle by implementing a tournamentstyle selection process. This mechanism iteratively filters the candidates by conducting a series of pairwise comparisons. Let _R_ be our RAC model, which is detailed in the following section. The RAC model can estimate the preference probability _pij_ given two actions, the proprioceptive state _st_ , and the shared context _Ct_ : 


In each round of the tournament, the set of candidates is organized into pairs. For each pair ( _ai, aj_ ), the preferred action is selected to advance to the next round based on the critic’s output: 


This single-elimination process discards half of the candidates in each round. It repeats until a single, optimal action _a∗_ remains. 

### **4.3 Relative Action Critic (RAC) Model** 

The cornerstone of our TTC deliberation phase is the RAC, a model trained to act as a pairwise preference critic. It determines if action _ai_ is preferable to _aj_ given the context. It is lightweight but powerful, as it can leverage the internal features of the VLM to reduce computation. 

### **4.3.1 Input Representation** 

The RAC takes four distinct inputs: two action chunks to be compared, _ai_ and _aj_ ; their difference _ai − aj_ ; and the current proprioceptive state _st_ . Each input is independently mapped by a dedicated MLP into the model’s embedding dimension _dmodel_ : 


These four embedding vectors are then concatenated to form the initial hidden state for the RAC’s Transformer tower: _X_<sup>0</sup> = Concat[ _ei_ ; _ej_ ; _ediff_ ; _es_ ]. 

### **4.3.2 Hierarchical Context Condition** 

To equip the RAC with task-relevant context, we introduce a set of _Nq_ randomly initialized, learnable query tokens _qrac ∈_ R<sup>_Nq×dmodel_</sup> . These tokens are appended to the VLM’s input sequence. During the VLM’s prefilling computations, these queries distill high-level semantic information from VLM’s raw features _Fvlm_ , effectively creating 

4 

**VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model** 


_Figure 4._ Detailed architecture of the Relative Action Critic (RAC) model (Sec 4.3). (Left) The VLM backbone is augmented with _Nq_ learnable queries. During the single pre-filling pass, these queries distill high-level semantic context query features from the image and instruction, alongside the standard raw features. (Middle) The RAC model itself is a Transformer with consistent depth of VLM. It takes four inputs processed by dedicated MLPs: Action i, Action j, their difference (Actioni - Action j), and the current proprioceptive State. (Right) The core component is the Multi-branch RAC Attention block. At each layer, this block hierarchically fuses information from three sources: (1) Self-Attention over the RAC’s own features, (2) Raw Cross-Attention to the VLM’s raw features at same layer, and (3) Query Cross-Attention to the distilled query features. This architecture allows the RAC to be lightweight yet highly context-aware. 

a compressed, task-oriented summary of the VLM’s understanding. The final hidden states of these query tokens, _Fquery_ , serve as a rich source of context for the RAC. 


### **4.3.3 Multi-Branch Attention Architecture** 

The RAC is a Transformer of depth _L_ , matching the VLM backbone’s depth. Each layer _l ∈_ [1 _, L_ ] of the RAC updates its input _X_<sup>_l−_1</sup> through a sophisticated three-branch attention block, as depicted in Fig. 4. 

1. **Self-Attention (SA):** The first branch computes selfattention over the RAC’s own representations: 


2. **Raw Cross-Attention:** The second branch injects broad contextual information by attending to raw features of the corresponding layer _l_ in the VLM backbone, _Fvlm_<sup>_l_:</sup> 


3. **Query Cross-Attention:** The third branch attends to the specialized, distilled context features from the VLM’s learnable query tokens from the same layer _l_ , _Fquery_<sup>_l_:</sup> 


These three outputs are then fused. The query crossattention branch is modulated by a learnable scalar gating parameter _g_<sup>_l_</sup> , which allows the model to dynamically control the influence of the distilled context. The fused representation _Ofused_<sup>_l_is created by concatenation:</sup> 


This fused vector is then passed through the standard Transformer layer components: a feed-forward network (FFN) and layer normalization (LN), with a residual connection from the input _X_<sup>_l−_1</sup> : 


After the final layer _L_ , the output representation _X_<sup>_L_</sup> is processed by a classification head (an MLP) to produce a single logit. This logit is passed through a sigmoid function to predict the probability that _ai_ is preferred over _aj_ , trained with a focal loss. 

### **4.4 Automated Action Preference Pair Curation** 

To train the RAC, we require a large-scale dataset of preference pairs. Thus, we introduce a fully automated pipeline that generates this dataset by manipulating the generation process of flow-matching-based action head. 

**Principle of Conditional Flow-Matching.** The flowmatching action head learns a context-conditioned vector field that transforms a simple prior distribution _pprior_ ( _a_ ) (e.g., Gaussian noise) into the complex data distribution _pdata_ ( _a|Ct_ ) of expert actions. Generation is achieved by solving the corresponding ODE numerically over a flow timestep _τ_ from _τ_ = 1 down to _τ_ = 0: 


The quality of the final sample is highly dependent on the number of integration steps ( _Nsteps_ ) used by the solver. A higher _Nsteps_ yields a more accurate approximation of the 

5 

**VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model** 

_Table 1._ Average task success rates (%) on the LIBERO-LONG. Ours (Full) represents VLA-ATTC without Cognitive Clutch. 

|Task|Robomonkey|PI0|**+Ours (Full)**|**+Ours**|PI0.5|**+Ours (Full)**|**+Ours**|
|---|---|---|---|---|---|---|---|
|Soup and sauce in basket|59%|86%|94% (+8%)|92% (+6%)|92%|96% (+4%)|96% (+4%)|
|Box and butter in basket|79%|98%|100% (+2%)|100% (+2%)|96%|100% (+4%)|100% (+4%)|
|Turn on stove and put pot|58%|90%|96% (+6%)|94% (+4%)|92%|98% (+6%)|96% (+4%)|
|Bowl in drawer and close|37%|96%|100% (+4%)|98% (+2%)|98%|98% (=)|98% (=)|
|Two mugs on two plates|55%|90%|98% (+8%)|96% (+6%)|94%|100% (+6%)|100% (+6%)|
|Book in compartment|86%|86%|96% (+10%)|94% (+8%)|96%|100% (+4%)|98% (+2%)|
|Mug and pudding on plate|59%|84%|94% (+10%)|90% (+6%)|90%|98% (+8%)|92% (+2%)|
|Soup and box in Basket|62%|96%|98% (+2%)|98% (+2%)|98%|98% (=)|98% (=)|
|Both pots on stove|26%|40%|58% (+18%)|56% (+16%)|54%|68% (+14%)|66% (+12%)|
|Mug in microwave and close|44%|62%|88% (+26%)|88% (+26%)|92%|98% (+6%)|96% (+4%)|
|Average|56.5%|82.8%|92.2% (+9.4%)|90.6% (+7.8%)|90.6%|95.4% (+4.8%)|94% (+3.4%)|


_Table 2._ Success rates (%) on real-world tasks with the Agilex Piper arm. VLA-ATTC consistently outperforms the baseline. 

|Task|Robomonkey|PI0|**+Ours (Full)**|**+Ours**|PI0.5|**+Ours (Full)**|**+Ours**|
|---|---|---|---|---|---|---|---|
|Stack cubes|18%|46%|62% (+16%)|58% (12%)|50%|60% (+10%)|60% (+10%)|
|Pour water|24%|50%|66% (+16%)|64% (+14%)|54%|68% (+14%)|66% (+12%)|
|Sweep rubbish|36%|42%|62% (+20%)|56% (14%)|52%|60% (+8%)|60% (+8%)|
|Average|26%|46%|63.3% (+17.3%)|58.7% (+12.7%)|52%|62.7% (+10.7%)|62% (+10%)|


true trajectory along the vector field, resulting in a sample that is more faithful to the learned expert distribution. 

**Data Curation Pipeline.** We leverage this principle to create actions of varying quality from a single pre-trained VLA. For each state-action pair ( _ot, a_<sup>_expert_</sup> _t_ ) from an expert dataset, we generate: 

- **High-quality action (** _a_<sup>_good_</sup> _t_ **):** By solving the ODE with a large number of steps, _Nhigh_ . 

- **Low-quality action (** _a_<sup>_bad_</sup> _t_ **):** By solving the ODE with a small number of steps, _Nlow_ . 

This establishes clear preference orderings: _a_<sup>_expert_</sup> _t ≻ a_<sup>_bad_</sup> _t_ and _a_<sup>_good_</sup> _t ≻ a_<sup>_bad_</sup> _t_ , where _≻_ denotes superiority. We then form a dataset of preference pairs with clear quality distinction, primarily using _⟨a_<sup>_expert_</sup> _t , a_<sup>_bad_</sup> _t ⟩_ and _⟨a_<sup>_good_</sup> _t , a_<sup>_bad_</sup> _t ⟩_ . To ensure the model learns the relative quality rather than positional cues, we augment the dataset with the symmetric versions of each pair (e.g., also including _⟨a_<sup>_bad_</sup> _t , a_<sup>_expert_</sup> _t ⟩_ with the inverse label). This scalable, automated process allows us to generate a massive, high-quality preference dataset without any human intervention. 

## **5 Experiments** 

In this section, we conduct extensive experiments to address the following research questions (RQ): 

- **RQ1 (Effectiveness)** : Can VLA-ATTC significantly enhance the performance on complex tasks? 

- **RQ2 (Ablation)** : What are the contributions of core components and the impact of candidate scaling and uncertainty threshold? 

- **RQ3 (Mechanism)** : Are the proposed uncertainty measurement and automated data curation pipeline scientifically valid and necessary? 

- **RQ4 (Efficiency)** : While delivering performance gains, does VLA-ATTC maintain the high control frequency required for practical applications? 

**Environments and Tasks** Our experiments are conducted across a challenging simulation platforms LIBERO-LONG (Liu et al., 2023) and a real-world robotic system on an Agilex Piper Arm. 

**Base Models and Implementation Details** We select PI0 (Black et al., 2024) and PI0.5 (Black et al., 2025), two SOTA VLA models, as our base models. Unless specified otherwise in our ablation studies, the uncertainty threshold _τ_ is set to the 80th percentile, the number of learnable queries _Nq_ is set to 8, and the number of candidates is 16. The training step of RAC models in all experiments is 30000. For our automated data curation, we used a mixed set of two pairs for ( _Nhigh, Nlow_ ), specifically _⟨_ 10 _,_ 3 _⟩_ and _⟨_ 9 _,_ 2 _⟩_ . “Ours (Full))” signifies that we do not use the “cognitive clutch”, activating TTC at all time steps. Each task is executed 50 times to calculate the success rate. 

### **5.1 Effectiveness of VLA-ATTC (RQ1)** 

**Obs1: VLA-ATTC boost the performance of SOTA VLA models significantly.** We first compare the performance of the original base VLA models against their VLA-ATTCaugmented counterparts on the LIBERO-LONG benchmarks and real-world settings. As shown in Table 1 and Table 2 , VLA-ATTC yields substantial performance improvements. On the highly challenging “Both pots on stove” task, VLA-ATTC improves the average success rate of PI0 from 40% to 58%, demonstrating that deliberate decisionmaking at critical moments effectively prevents catastrophic failures. Notably, VLA-ATTC increased the average success rate of PI0 by 17.3% on real-robot tasks, demonstrating its 

6 

**VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model** 

_Table 3._ Effect of the uncertainty threshold ( _τ_ , set by K-th percentile) on success rate and latency on PI0-ATTC and PI0.5-ATTC. 

|K-th percentile|PI0-0%|PI0-40%|PI0-60%|PI0-80%|PI0.5-0%|PI0.5-40%|PI0.5-60%|PI0.5-80%|
|---|---|---|---|---|---|---|---|---|
|Soup and sauce in basket|94%|92%|92%|92%|96%|96%|96%|96%|
|Box and butter in basket|100%|100%|100%|100%|100%|100%|100%|100%|
|Turn on stove and put pot|96%|96%|94%|94%|98%|98%|96%|96%|
|Bowl in drawer and close|100%|98%|98%|98%|98%|98%|98%|98%|
|Two mugs on two plates|98%|98%|98%|96%|100%|100%|100%|100%|
|Book in compartment|96%|96%|94%|94%|100%|98%|98%|98%|
|Mug and pudding on plate|94%|94%|92%|90%|98%|96%|96%|92%|
|Soup and box in Basket|98%|98%|98%|98%|98%|98%|98%|98%|
|Both pots on stove|58%|58%|58%|56%|68%|66%|66%|66%|
|Mug in microwave and close|88%|88%|88%|88%|98%|96%|96%|96%|
|Average|92.2%|91.8%|91.2%|90.6%|95.4%|94.6%|94.4%|94%|


_Table 4._ Effect of the number of candidate actions ( _N_ <u>) during deliberation on success rate on LIBERO-LONG.</u> 

|Number of candidate actions|4 (PI0)|8 (PI0)|16 (PI0)|32 (PI0)|4 (PI0.5)|8 (PI0.5)|16 (PI0.5)|32 (PI0.5)|
|---|---|---|---|---|---|---|---|---|
|Soup and sauce in basket|90%|90%|92%|92%|94%|96%|96%|96%|
|Box and butter in basket|100%|100%|100%|100%|100%|100%|100%|100%|
|Turn on stove and put pot|92%|94%|94%|94%|94%|96%|96%|98%|
|Bowl in drawer and close|98%|98%|98%|98%|94%|98%|98%|100%|
|Two mugs on two plates|94%|94%|96%|98%|100%|100%|100%|100%|
|Book in compartment|90%|94%|94%|96%|98%|100%|98%|100%|
|Mug and pudding on plate|86%|88%|90%|94%|92%|94%|92%|96%|
|Soup and box in Basket|96%|96%|98%|98%|96%|98%|98%|100%|
|Both pots on stove|48%|52%|56%|60%|56%|60%|66%|66%|
|Mug in microwave and close|76%|82%|88%|88%|96%|96%|96%|96%|
|Average|87%|88.8%|90.6%|91.8%|92.0%|93.8%|94%|95.2%|


excellent performance on physical hardware. VLA-ATTC consistently surpasses previous representative deliberation method Robomonkey (Kwok et al., 2025). 

### **5.2 Ablation Studies and Analysis (RQ2)** 

**Obs2: Cognitive Clutch is accurate, with difficult states being sparse.** The sensitivity of the “Cognitive Clutch” is governed by the uncertainty threshold _τ_ , set as the K-th percentile. We study the effect of varying _τ_ on task success rate. As shown in Table 3, although lower _τ_ triggers more deliberation, the performance does not improve significantly. This suggests that only a few scenarios during the operation are difficult, which also proves that our cognitive clutch can effectively identify these few critical, difficult scenarios. 

**Obs3: More candidate actions yield higher performance gains.** During the TTC deliberation phase, we explore better solutions by sampling _N_ candidate actions in parallel. We study how the choice of _N_ affects the final success rate. As presented in Table 4, performance improves substantially even with a small number of candidates (e.g., _N_ = 4). While performance improves steadily as the number of candidate actions increases, we consider _N_ = 16 to be an efficient and effective choice given the increased computational cost. 

**Obs4: All specialized components of the RAC are essential for accurate preference prediction.** The ablation studies presented in Figure 5 show that removing key architectural elements—specifically the learnable weights, ac- 


_Figure 5._ Comparison of success rate over different RAC model’s variant on LIBERO-LONG. 

tion difference inputs, or learnable queries—consistently degrades performance on the LIBERO-LONG benchmark. While the full RAC model achieves the highest success rates (94% for PI0.5+ATTC and 90.8% for PI0+ATTC), removing the “Learnable Query” component causes the most significant performance drop, lowering success rates to 92.4% and 88% respectively. These findings confirm that each design choice in the RAC framework is necessary to effectively evaluate and select optimal actions. 

### **5.3 Mechanism Analysis (RQ3)** 

To validate the scientific validity of our core design choices—specifically the uncertainty measurement and the automated data curation pipeline—we conducted targeted controlled experiments. 

7 

**VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model** 

_Table 5._ Comparison of average control frequency (Hz). VLA-ATTC maintains a high control rate. 


_Figure 6._ Two representative cases of PI0.5-ATTC. It adaptively triggers TTC when facing difficult situations. 

_Table 6._ Validation of Uncertainty Estimation Strategies against Human Expert Rankings. Tested on 1,000 observation pairs. 

|**Method**|**Metric**<br>**Human**|**Agree. (%)**|**Cost (Rel.)**|
|---|---|---|---|
|Ours (_N_ = 2)|Pairwise DTW|89.2|1_._0_×_|
|Baseline (_N_ = 4)|Mean Pairwise Dist.|90.1|2_._0_×_|
|Baseline (_N_ = 8)|Mean Pairwise Dist.|90.4|4_._0_×_|


_Table 7._ Impact of ODE Integration Steps on Action Quality. Realworld success rates on the “Pour water” task (50 trials each). 

|**ODE Steps (**_Nsteps_**)**|**Success Rate (%)**|**Behavior Description**|
|---|---|---|
|10 (High Quality)|54|Precise execution|
|5 (Mid Quality)|42|Coherent, misaligned|
|1 (Low Quality)|18|Rough, frequent failure|


**Obs5: Minimal sampling (** _N_ = 2 **) is sufficient for effective uncertainty estimation.** A potential concern regarding our “Cognitive Clutch” is whether comparing merely two action candidates is robust enough to accurately gauge situational uncertainty. To investigate this, we constructed a specialized evaluation dataset comprising 1,000 pairs of observation scenarios. Four human experts annotated these pairs to identify which scenario in each pair presented a higher difficulty level (i.e., higher likelihood of failure), serving as the ground truth. 

We compared our proposed strategy (2 actions with Dynamic Time Warping, DTW) against baselines using more samples ( _N_ = 4 and _N_ = 8) utilizing Mean Pairwise Distance (MPD) as the uncertainty metric. As shown in Table 6, our method achieves an agreement accuracy of 89.2% with human experts. Crucially, scaling the sample size to 4 or 8 yields only marginal improvements ( _<_ 1 _._ 5%) while linearly increasing the computational overhead of the action head. 

**Obs6: Reducing ODE steps creates valid preference gradients, not random noise.** Our automated data curation pipeline relies on the premise that reducing the number of ODE integration steps ( _Nsteps_ ) degrades action quality gracefully without devolving into random noise, thereby creating valid “expert vs. sub-optimal” preference pairs. To validate this empirically, we conducted real-world experiments on the Agilex Piper arm using the “Pour water” task, varying _Nsteps_ at 10, 5, and 1. 

The results, presented in Table 7, confirm our hypothesis. While the high-quality setting ( _Nsteps_ = 10) achieves a 54% success rate, reducing steps to 5 and 1 leads to a progressive decline in performance (42% and 18%, respectively). This reveals that actions generated with lower steps remain semantically coherent (e.g., moving generally towards the cup) but suffer from precision errors (e.g., spilling or misalignment), rather than exhibiting random jitter. 

### **5.4 Efficiency Analysis (RQ4)** 

**Obs7: VLA-ATTC maintains high control frequency suitable for real-time robotics.** A core advantage of VLA-ATTC is its ability to improve decision quality while minimally impacting control frequency. Due to the “Cognitive Clutch”, the expensive deliberation process is invoked only when necessary. As shown in Table 5, the baseline model operates at approximately 23.3 Hz. With VLA-ATTC integrated, the average control frequency drops only slightly to 20.8 Hz, as deliberation is active for only a few timesteps. This speed is significantly higher than other indiscriminate parallel deliberation methods that rely on heavyweight critic models or MCTS, such as RoboMonkey (Kwok et al., 2025) at 1.5 Hz. This demonstrates the immense practical advantage of our framework, making it suitable for robotic tasks that demand real-time responsiveness. 

## **6 Conclusion** 

In this work, we introduced VLA-ATTC, a framework that fundamentally challenges the static, “one-size-fits-all” inference paradigm of VLA models. By dynamically triggering a test-time deliberation phase via an uncertainty-based “cognitive clutch”, and employing an efficient, lightweight Relative Action Critic model for pairwise selection, our method significantly enhances decision-making robustness in complex scenarios without sacrificing the high control frequencies required for robotics. This work demonstrates the critical value of adaptive computation and opens a promising new direction for developing more efficient, deliberative, and intelligent agents that can strategically allocate 

8 

**VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model** 

resources to the problem at hand. 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning, specifically within Embodied AI and Robotic Manipulation. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

## **References** 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. pi0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Galliker, M. Y., et al. pi0.5: a vision-language-action model with openworld generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Chen, Q., Qin, L., Liu, J., Peng, D., Guan, J., Wang, P., Hu, M., Zhou, Y., Gao, T., and Che, W. Towards reasoning era: A survey of long chain-of-thought for reasoning large language models. _arXiv preprint arXiv:2503.09567_ , 2025. 

- Chen, Y., Cao, Z., Ren, H., Yang, C., Li, W., Wang, S., Wang, Y., Zhang, L., Shao, Y., Zhao, Z., et al. Roborouter: Training-free policy routing for robotic manipulation. _arXiv preprint arXiv:2603.07892_ , 2026. 

- Duan, J., Yu, S., Tan, H. L., Zhu, H., and Tan, C. A survey of embodied ai: From simulators to research tasks. _IEEE Transactions on Emerging Topics in Computational Intelligence_ , 6(2):230–244, 2022. 

- Feng, Z., Xue, R., Yuan, L., Yu, Y., Ding, N., Liu, M., Gao, B., Sun, J., Zheng, X., and Wang, G. Multi-agent embodied ai: Advances and future directions. _arXiv preprint arXiv:2505.05108_ , 2025. 

- Fung, P., Bachrach, Y., Celikyilmaz, A., Chaudhuri, K., Chen, D., Chung, W., Dupoux, E., Gong, H., Jegou, H.,´ Lazaric, A., et al. Embodied ai agents: Modeling the world. _arXiv preprint arXiv:2506.22355_ , 2025. 

- Guo, W., Lu, G., Deng, H., Wu, Z., Tang, Y., and Wang, Z. Vla-reasoner: Empowering vision-language-action models with reasoning via online monte carlo tree search. _arXiv preprint arXiv:2509.22643_ , 2025. 

- Huang, C., Huang, L., Leng, J., Liu, J., and Huang, J. Efficient test-time scaling via self-calibration. _arXiv preprint arXiv:2503.00031_ , 2025. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Kwok, J., Agia, C., Sinha, R., Foutter, M., Li, S., Stoica, I., Mirhoseini, A., and Pavone, M. Robomonkey: Scaling test-time sampling and verification for vision-languageaction models. _arXiv preprint arXiv:2506.17811_ , 2025. 

- Li, D., Cao, S., Cao, C., Li, X., Tan, S., Keutzer, K., Xing, J., Gonzalez, J. E., and Stoica, I. S*: Test time scaling for code generation. _arXiv preprint arXiv:2502.14382_ , 2025a. 

- Li, M., Huang, X., and Zhang, Z. Self-supervised geometric features discovery via interpretable attention for vehicle re-identification and beyond. In _ICCV_ , 2021. 

- Li, M., Liu, J., Zheng, C., Huang, X., and Zhang, Z. Exploiting multi-view part-wise correlation via an efficient transformer for vehicle re-identification. _IEEE Transactions on Multimedia_ , 25:919–929, 2023. doi: 10.1109/TMM.2021.3134839. 

- Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., Wei, F., Deng, Y., Xu, S., Zhang, Y., et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- Li, W., Su, X., Wu, J., Yang, F., Liu, Y., Chen, Y., You, S., and Xu, C. Identify, isolate, and purge: Mitigating hallucinations in lvlms via self-evolving distillation. In _Proceedings of the 33rd ACM International Conference on Multimedia_ , pp. 6791–6800, 2025b. 

- Li, W., Su, X., Cao, Y., Xu, H., Xia, X., You, S., Chen, Y., and Xu, C. Sentinel-vla: A metacognitive vla model with active status monitoring for dynamic reasoning and error recovery, 2026a. URL https://arxiv.org/abs/ 2605.01191. 

- Li, W., Su, X., Niu, D., Cao, Y., Xu, H., Qu, Z., Fan, L., You, S., and Xu, C. Vla-attc: Adaptive test-time compute for vla models with relative action critic model, 2026b. URL https://arxiv.org/abs/2605.01194. 

- Li, Z., Chi, C., Wei, Y., Zhu, B., Huang, T., Sun, Z., Peng, Y., Wang, P., Wang, Z., Liu, F., et al. Do you have freestyle? expressive humanoid locomotion via audio control. _arXiv preprint arXiv:2512.23650_ , 2025c. 

9 

**VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model** 

- Li, Z., Chi, C., Zhu, B., Wei, Y., Bai, S., Ji, Y., Peng, Y., Huang, T., Wang, P., Wang, Z., et al. Robomirror: Understand before you imitate for video to humanoid locomotion. _arXiv preprint arXiv:2512.23649_ , 2025d. 

- Lin, F., Nai, R., Hu, Y., You, J., Zhao, J., and Gao, Y. Onetwovla: A unified vision-language-action model with adaptive reasoning. _arXiv preprint arXiv:2505.11917_ , 2025. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Liu, J., Liu, M., Wang, Z., Lee, L., Zhou, K., An, P., Yang, S., Zhang, R., Guo, Y., and Zhang, S. Robomamba: Multimodal state space model for efficient robot reasoning and manipulation. _arXiv e-prints_ , pp. arXiv–2406, 2024. 

- Liu, Y., Chen, W., Bai, Y., Liang, X., Li, G., Gao, W., and Lin, L. Aligning cyber space with physical world: A comprehensive survey on embodied ai. _IEEE/ASME Transactions on Mechatronics_ , 2025. 

- Memarian, B. and Doleck, T. Embodied ai in education: A review on the body, environment, and mind. _Education and Information Technologies_ , 29(1):895–916, 2024. 

- Miao, J., Thongprayoon, C., Suppadungsuk, S., Krisanapan, P., Radhakrishnan, Y., and Cheungpasitporn, W. Chain of thought utilization in large language models and application in nephrology. _Medicina_ , 60(1):148, 2024. 

- Muennighoff, N., Yang, Z., Shi, W., Li, X. L., Fei-Fei, L., Hajishirzi, H., Zettlemoyer, L., Liang, P., Candes,` E., and Hashimoto, T. s1: Simple test-time scaling. _arXiv preprint arXiv:2501.19393_ , 2025. 

- Nakamoto, M., Mees, O., Kumar, A., and Levine, S. Steering your generalists: Improving robotic foundation models via value guidance. _arXiv preprint arXiv:2410.13816_ , 2024. 

- Nguyen, H. T., Nguyen, B., and Nguyen, V. A. Structured pruning for diverse best-of-n reasoning optimization. _arXiv preprint arXiv:2506.03978_ , 2025. 

- Paolo, G., Gonzalez-Billandon, J., and Kegl, B.´ Position: a call for embodied ai. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Prasad, A., Yuan, W., Pang, R. Y., Xu, J., Fazel-Zarandi, M., Bansal, M., Sukhbaatar, S., Weston, J., and Yu, J. Self-consistency preference optimization. _arXiv preprint arXiv:2411.04109_ , 2024. 

- Sessa, P. G., Dadashi, R., Hussenot, L., Ferret, J., Vieillard, N., Rame, A., Shariari, B., Perrin, S., Friesen, A.,´ Cideron, G., et al. Bond: Aligning llms with best-of-n distillation. _arXiv preprint arXiv:2407.14622_ , 2024. 

- Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., Aractingi, M., Pascal, C., Russi, M., Marafioti, A., et al. Smolvla: A vision-languageaction model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- Song, H., Qu, D., Yao, Y., Chen, Q., Lv, Q., Tang, Y., Shi, M., Ren, G., Yao, M., Zhao, B., et al. Hume: Introducing system-2 thinking in visual-language-action model. _arXiv preprint arXiv:2505.21432_ , 2025. 

- Tan, S., Qiu, X., Shu, Y., Xu, G., Xu, L., Xu, X., Zhuang, H., Li, M., and Yu, F. WMarkGPT: Watermarked image understanding via multimodal large language models. In _Proceedings of the 42nd International Conference on Machine Learning_ , volume 267 of _Proceedings of Machine Learning Research_ , pp. 58621–58636. PMLR, 13–19 Jul 2025. 

- Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Toshniwal, S., Sorokin, I., Ficek, A., Moshkov, I., and Gitman, I. Genselect: A generative approach to best-of-n. _arXiv preprint arXiv:2507.17797_ , 2025. 

- Verdun, C. M., Oesterling, A., Lakkaraju, H., and Calmon, F. P. Soft best-of-n sampling for model alignment. _arXiv preprint arXiv:2505.03156_ , 2025. 

- Wang, C., Guo, J., Li, H., Tian, Y., Nie, Y., Xu, C., and Han, K. Circle-rope: Cone-like decoupled rotary positional embedding for large vision-language models. _arXiv preprint arXiv:2505.16416_ , 2025a. 

- Wang, H., Prasad, A., Stengel-Eskin, E., and Bansal, M. Soft self-consistency improves language model agents. _arXiv preprint arXiv:2402.13212_ , 2024a. 

- Wang, X. and Zhou, D. Chain-of-thought reasoning without prompting. _Advances in Neural Information Processing Systems_ , 37:66383–66409, 2024. 

- Wang, X., Feng, S., Li, Y., Yuan, P., Zhang, Y., Tan, C., Pan, B., Hu, Y., and Li, K. Make every penny count: Difficulty-adaptive self-consistency for cost-efficient reasoning. _arXiv preprint arXiv:2408.13457_ , 2024b. 

- Wang, X., Feng, S., Li, Y., Yuan, P., Zhang, Y., Tan, C., Pan, B., Hu, Y., and Li, K. Make every penny count: 

10 

**VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model** 

- Difficulty-adaptive self-consistency for cost-efficient reasoning. In _Findings of the Association for Computational Linguistics: NAACL 2025_ , pp. 6904–6917, 2025b. 

- Wang, Y., Wu, S., Zhang, Y., Yan, S., Liu, Z., Luo, J., and Fei, H. Multimodal chain-of-thought reasoning: A comprehensive survey. _arXiv preprint arXiv:2503.12605_ , 2025c. 

- Wang, Y., Zhang, P., Huang, S., Yang, B., Zhang, Z., Huang, F., and Wang, R. Sampling-efficient test-time scaling: Self-estimating the best-of-n sampling in early decoding. _arXiv preprint arXiv:2503.01422_ , 2025d. 

- Xia, Y., Wang, R., Liu, X., Li, M., Yu, T., Chen, X., McAuley, J., and Li, S. Beyond chain-of-thought: A survey of chain-of-x paradigms for llms. _arXiv preprint arXiv:2404.15676_ , 2024. 

- Xu, S., Wang, Y., Xia, C., Zhu, D., Huang, T., and Xu, C. Vla-cache: Towards efficient vision-language-action model via adaptive token caching in robotic manipulation. _arXiv preprint arXiv:2502.02175_ , 2025a. 

- Xu, S., Wang, Y., Xia, C., Zhu, D., Huang, T., and Xu, C. Vla-cache: Efficient vision-language-action manipulation via adaptive token caching. _arXiv preprint arXiv:2502.02175_ , 2025b. 

   - Zhang, Q., Lyu, F., Sun, Z., Wang, L., Zhang, W., Hua, W., Wu, H., Guo, Z., Wang, Y., Muennighoff, N., et al. A survey on test-time scaling in large language models: What, how, where, and how well? _arXiv preprint arXiv:2503.24235_ , 2025. 

   - Zhang, R., Haider, M., Yin, M., Qiu, J., Wang, M., Bartlett, P., and Zanette, A. Accelerating best-of-n via speculative rejection. In _ICML 2024 Workshop on Structured Probabilistic Inference Generative Modeling_ , 2024. 

   - Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025. 

   - Zhou, Z., Zhu, Y., Wen, J., Shen, C., and Xu, Y. Chatvla-2: Vision-language-action model with open-world embodied reasoning from pretrained knowledge. _arXiv preprint arXiv:2505.21906_ , 2025a. 

   - Zhou, Z., Zhu, Y., Zhu, M., Wen, J., Liu, N., Xu, Z., Meng, W., Cheng, R., Peng, Y., Shen, C., et al. Chatvla: Unified multimodal understanding and robot control with visionlanguage-action model. _arXiv preprint arXiv:2502.14420_ , 2025b. 

- Xu, S., Wang, Z., Wang, Y., Xia, C., Huang, T., and Xu, C. Affordance field intervention: Enabling vlas to escape memory traps in robotic manipulation. _arXiv preprint arXiv:2512.07472_ , 2025c. 

- Yang, Y., Zeng, S., Lin, T., Chang, X., Qi, D., Xiao, J., Liu, H., Chen, R., Chen, Y., Huo, D., et al. Abot-m0: Vla foundation model for robotic manipulation with action manifold learning. _arXiv preprint arXiv:2602.11236_ , 2026. 

- Yeo, E., Tong, Y., Niu, M., Neubig, G., and Yue, X. Demystifying long chain-of-thought reasoning in llms. _arXiv preprint arXiv:2502.03373_ , 2025. 

- Zawalski, M., Chen, W., Pertsch, K., Mees, O., Finn, C., and Levine, S. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 

- Zeng, X., Xu, Q., Wang, Y., and Xu, C. Hici: Hierarchical construction-integration for long-context attention. _arXiv preprint arXiv:2603.20843_ , 2026. 

- Zeng, Z., Cheng, Q., Yin, Z., Zhou, Y., and Qiu, X. Revisiting the test-time scaling of o1-like models: Do they truly possess test-time scaling capabilities? _arXiv preprint arXiv:2502.12215_ , 2025. 

11 

**VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model** 

## **A Verification of Semantic Preference Learning in RAC** 

A potential concern regarding our automated data curation pipeline (Sec. 3.4) is that the RAC model might solely rely on distinguishing low-level generation artifacts (e.g., trajectory smoothness or noise levels) resulting from different ODE integration steps ( _Nhigh_ vs. _Nlow_ ), rather than acquiring a semantic understanding of task fulfillment. 

To rule out this possibility and verify that the RAC genuinely aligns actions with visual context and language instructions, we conducted a controlled ”Cross-Task” experiment. 

**Experimental Setup.** We utilized the real-world ”Stack Cubes” task for this validation. We collected a dataset of 1,000 observations from successful execution trajectories. For each observation, we generated a pair of action candidates to be evaluated by the RAC model trained on the ”Stack Cubes” task: 

- **Positive Sample (Task-Aligned):** Actions generated by the ”Stack Cubes” expert policy. 

- **Negative Sample (Task-Misaligned):** Actions generated by a policy trained on a completely different task (”Pour Water”), applied to the ”Stack Cubes” observations. 

Crucially, **both policies generated actions using a high number of ODE integration steps (** _Nsteps_ = 10 **)** . This setup ensures that both candidates possess high trajectory quality and smoothness, eliminating low-level generation artifacts as a discriminative feature. The only distinguishing factor is the semantic alignment with the ”Stack Cubes” task. 

**Results.** The RAC model demonstrated a high accuracy of **97.3%** in identifying the actions from the ”Stack Cubes” policy as the preferred candidates. This result strongly evidences that the RAC goes beyond detecting generation quality; it successfully learns to evaluate the semantic compatibility between the proposed action, the visual observation, and the task instruction. 

12 

