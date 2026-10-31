---
title: "Think Proprioceptively: State-Grounded Visual Token Selection for VLA Policies"
date: "2026-02-06"
authors: "Fangyuan Wang; Peng Zhou; Jiaming Qi; Shipeng Lyu; Chengyang He; David Navarro-Alarcon"
venue: "CoRL 2026"
url: https://arxiv.org/abs/2602.06575
pdf: https://arxiv.org/pdf/2602.06575
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.06575)** / [論文ページ](https://arxiv.org/abs/2602.06575)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Think Proprioceptively: State-Grounded Visual Token Selection for VLA Policies** 

Fangyuan Wang<sup>1,2</sup> Peng Zhou<sup>3</sup> Jiaming Qi<sup>4</sup> Shipeng Lyu<sup>1,2</sup> Chengyang He<sup>5</sup> David Navarro-Alarcon<sup>1,*</sup> Guodong Guo<sup>2,*</sup> 1The Hong Kong Polytechnic University 2Eastern Institute of Technology 3Great Bay University 4Northeast Forestry University 5National University of Singapore 


Figure 1: ThinkProprio investigates what role proprioception should play in VLA models. **Left:** Across simulation, and real-world tasks, instruction selection (blue) and state selection (purple) highlight complementary visual evidence. **Middle:** Four representative VLA designs: (a) proprioception as late input to the action expert, (b) proprioception as VLM context tokens, (c) generic token compression before the action expert, and (d) ThinkProprio uses both language and proprioception to gate visual tokens _before_ VLM. **Right:** ThinkProprio matches strong baselines across CALVIN and LIBERO while achieving the lowest inference latency with a compact visual-token budget. 

**Abstract:** Vision-language-action (VLA) models typically inject proprioception only as a late conditioning signal, preventing robot state from grounding instruction understanding or directing visual attention. We introduce ThinkProprio, which discretizes proprioception into VLM-vocabulary tokens and uses them jointly with the instruction to gate visual patches before VLM computation, steering the model toward action-relevant evidence while discarding redundant tokens early. We find that proprioception added as a passive conditioning signal leaves performance essentially unchanged; its value emerges when token-form state acts as an active query that, with the instruction, selects which visual patches the VLM processes. Systematic ablations show that VLM-vocabulary tokens outperform learned projectors as the state encoding, and that retaining only about 12 % of the visual tokens surpasses on CALVIN ABC _→_ D. Across CALVIN, LIBERO, and real-world manipulation, ThinkProprio reduces end-to-end inference latency while improving the matched full-token baseline. 

**Keywords:** Robot manipulation, Vision-language-action models 

*Corresponding authors. 

## **1 Introduction** 

Vision-language-action (VLA) models translate visual observations and language instructions into executable actions through large-scale pretraining [1, 2, 3]. Yet contact-rich manipulation depends not only on what is visible and what is requested, but also on the robot’s embodiment, including its joint configuration and motion. Most current VLA pipelines treat proprioception as a late conditioning signal for the action head, couple it only weakly to perception, or omit it altogether. This raises a concrete design question: _should robot state be a late conditioning signal for action generation, or an active participant in instruction grounding and visual attention?_ 

Holding the backbone, action head, data, and training budget fixed, we vary only how proprioception is encoded and where it enters, finetuning on CALVIN ABC _→_ D (Table 7). Passive late conditioning at the action head matches omitting state entirely, and an MLP projection into the VLM hurts; only VLM-vocabulary tokens routed through the VLM improve over the no-proprioception baseline. 

In published systems, proprioceptive design is typically entangled with vision-language aggregation and the action conditioning mechanism (see Table 1), making the functional role of proprioception hard to attribute. We therefore vary these axes systematically. Prior work treats efficient visual-token selection [11, 12] and routing proprioception through the VLM token interface [4] as separate developments; once proprioception lives in this token space, it can also serve as a query signal for visual evidence, complementary to the instruction. 

Table 1: Taxonomy of representative VLA designs. Subheaders specify the order of slash-separated fields. Tok. = tokenized and Comp. = compressed. 

|**Model**|**VL**<br>repr. / act. cond.|**Proprio.**<br>enc. / entry / act. cond.|
|---|---|---|
|_π_0 [3]|Dense / Cross-attn|MLP / ACT / Cross-attn|
|_π_0_._5 [4]|Dense / Cross-attn|Tok. / VLM / Cross-attn|
|SmolVLA [5]|Dense / Cross-attn|MLP / VLM / Cross-attn|
|FLOWER [6]|Dense / Cross-attn|MLP / ACT / AdaLN|
|Dita [7]|Dense / In-context|MLP / ACT / In-context|
|CogACT [8]|Comp. / In-context|N/A|
|OTTER [9]|Pooled / Cross-attn|MLP / ACT / Cross-attn|
|DiT-Blocks [10]|Pooled / AdaLN|MLP / VLM / Cross-attn|


We instantiate this idea as ThinkProprio, which gates visual patches before VLM computation using separate instruction and proprioception branches. Our contributions are: 

- A systematic study isolating proprioceptive encoding and entry point from vision-language aggregation and action conditioning, showing that encoding proprioception as VLM-vocabulary tokens both preserves baseline performance and exposes state to downstream visual reasoning. 

- ThinkProprio, a state-grounded visual-token gating mechanism that uses language and proprioception as complementary query branches before VLM computation. 

- Empirical evaluation on CALVIN, LIBERO, and a 14-task real-world benchmark, where ThinkProprio matches or surpasses strong baselines at a fraction of the visual tokens and the lowest per-step latency. 

## **2 Related Work** 

**Vision-Language Feature Extraction.** VLA systems differ in how vision-language backbone outputs are presented to the action head. Some pass dense token sets directly, as in _π_ 0 [3], _π_ 0 _._ 5 [4], and FLOWER [6], preserving fine-grained information but increasing computation. Others aggregate tokens before control: CogACT [8] compresses the set, while DiT-Block [10], OTTER [9], and LightVLA [11] apply pooling-style reductions that inherit from the broader token-reduction literature [12, 13]. These methods span a spectrum from indiscriminate aggregation, which reduces tokens without regard to task content, to guided selection that conditions retention on an external signal. 

**Proprioceptive Encoding and Entry.** Prior work integrates proprioception with different encodings and entry points. _π_ 0 _._ 5 [4] serializes proprioception as text before VLM input, whereas ThinkProprio maps discretized state bins directly to VLM vocabulary IDs. GR00T-N1 [14] and SmolVLA [5] instead project proprioception with multilayer perceptrons into the VLM feature space, which increases representational flexibility but can introduce mismatch relative to pretrained token features. FLOWER [6] conditions the action head directly on proprioceptive inputs, bypassing the backbone, 

2 

and some single-system VLAs such as CogACT [8] omit explicit proprioceptive input entirely. Encoding and entry point co-vary in the literature: MLP-encoded state is almost always fed to the action head, token-form state enters the VLM, and proprio-free designs cluster among single-system policies. This coupling has historically been treated as a fixed architectural package rather than as two independent design axes. 

**Action Conditioning Mechanisms.** VLA action heads adopt three main conditioning mechanisms. _In-context_ approaches concatenate vision-language and proprioceptive embeddings with the action sequence, as in Dita [7] and decoder-only systems such as OpenVLA [2]. _AdaLN-style_ modulation predicts layer-wise scale and shift from pooled features and is used by DiT-Block [10], FLOWER [6], and MDT [15]. _Cross-attention_ retains token-level access at higher cost and is used by _π_ 0 [3], _π_ 0 _._ 5 [4], and FLOWER’s Flow Transformer [6]. The three families trade expressivity for cost: cross-attention is most expressive but scales with the context-token count, AdaLN is cheapest but collapses tokens into a global modulation, and in-context conditioning falls in between. 

Across these methods, proprioception is treated as a passive conditioning signal, but not used to select what the policy looks at. ThinkProprio departs from this convention by using state as an active query against visual tokens, alongside the instruction, before the VLM consumes them. 

## **3 Method** 

We consider a policy _πθ_ composed of a vision-language backbone and a separate action head. At timestep _t_ , the policy receives an observation _ot_ comprising _n_ RGB images ( _It_<sup>1</sup><sup>_, . . . , I_</sup> _t_<sup>_n_),a</sup> language instruction _ℓ_ , and a proprioceptive state **_q_** _t_ that encodes the robot’s current configuration, including joint angles and end-effector pose. We represent each input stream as a token sequence with shared embedding dimension _D_ : vision tokens _Hv ∈_ R<sup>_Nv×D_</sup> , language tokens _Hl ∈_ R<sup>_Nl×D_</sup> , and proprioceptive tokens _Hq ∈_ R<sup>_Nq×D_</sup> , where _Nv_ , _Nl_ , and _Nq_ denote the corresponding token counts. As shown in Figure 2, ThinkProprio instantiates this dual-system policy by discretizing proprioception into VLM-vocabulary tokens and using instruction and proprioceptive tokens in two separate guidance branches to select visual patches before VLM computation. The backbone _f_ VLM maps the resulting compact multimodal sequence to conditioning features _C_ , and the action head _f_ ACT predicts a continuous action chunk **_a_** _t_ : _t_ + _H_ conditioned on _C_ . 

### **3.1 Proprioceptive State Encoding** 

The proprioceptive state **_q_** _t_ contains _dq_ scalar values, so _Nq_ = _dq_ . We discretize each value with uniform binning over a clipped range, where _q_ min and _q_ max are shared scalar clipping bounds applied to each dimension and _B_ is the number of bins. For each state element _qt,k_ with _k ∈{_ 1 _, . . . , dq}_ , we compute the bin index 


We map each bin index to a proprioceptive token ID using the reverse mapping _τt,k_ = _V −_ 1 _− bt,k_ , where _V_ is the VLM vocabulary size. These IDs are vocabulary aliases for discretized state values, not the output of the language tokenizer. Reusing the existing embedding table adds no new embedding parameters and uses the same lookup pathway as text inputs; the reverse indexing keeps the proprioceptive token range disjoint from the tokens produced by the language tokenizer for our prompts, so the two streams do not collide. We then obtain the corresponding embeddings from the VLM token embedding table, _Hq_ = Embed( **_τ_** _t_ ), where **_τ_** _t_ = [ _τt,_ 1 _, . . . , τt,dq_ ]. 

### **3.2 Embodied Visual Token Gating** 

We gate visual tokens before they enter the VLM so that subsequent VLM computation operates on a compact set of action-relevant patches. The selector uses two complementary guidance branches, one driven by the instruction and one by proprioception. The instruction branch emphasizes task-semantic 

3 


Figure 2: Overview of ThinkProprio. Proprioception is used with the instruction in two guidance branches to select task-relevant visual patches before VLM computation, alongside a global context token. The action head attends to the resulting features to generate actions. 

evidence such as objects and goals, while the proprioception branch emphasizes configurationdependent evidence such as the gripper and contact regions. 

**Branch-specific scoring.** Let Ω= _{_ lang _,_ prop _}_ index the two branches, with guidance tokens _G_ lang = _Hl_ and _G_ prop = _Hq_ . We normalize the visual and guidance tokens as _H_<sup>˜</sup> _v_ = RMSNorm( _Hv_ ) and _G_<sup>˜</sup> _ω_ = RMSNorm( _Gω_ ) for each _ω ∈_ Ω. Rather than scoring visual tokens directly from the guidance tokens, we use a vote-based construction that conditions each vote on a visual token, so the selector forms visual-context-dependent votes instead of a single top-down saliency map. For branch _ω_ , we compute 


Each row of _Qω_ is obtained by letting visual token _i_ attend to the branch guidance tokens and extract the guidance information most relevant to it. The resulting guidance-conditioned query then scores all visual tokens as candidates for retention. The matrix _Sω ∈_ R<sup>_Nv×Nv_</sup> is therefore a branch-specific vote matrix in which row index _i_ denotes the visual token that issues the query and column index _j_ denotes a candidate visual token for retention; entry _Sω_ [ _i, j_ ] measures how strongly guidance-conditioned visual token _i_ votes for retaining visual token _j_ . 

**Vote-based gating with straight-through relaxation.** Each branch converts its score matrix into a hard selection mask for the forward pass and a soft relaxation for gradient propagation. During training, we perturb each branch score matrix as _S_<sup>ˆ</sup> _ω_ = _Sω_ + _α_ Γ _ω_ , where Γ _ω_ is sampled elementwise from the standard Gumbel distribution and _α_ is cosine-annealed from _α_ start to _α_ end. This perturbation encourages exploration early in training and approaches deterministic selection near convergence. At inference time, we remove the perturbation by setting _S_<sup>ˆ</sup> _ω_ = _Sω_ . 

In the hard forward path, each row _i_ casts one vote for a candidate visual token, _zω_ [ _i_ ] = arg max _j∈{_ 1 _,...,Nv} S_<sup>ˆ</sup> _ω_ [ _i, j_ ]. Branch _ω_ selects token _j_ if it receives at least one vote, _mω_ [ _j_ ] = **1** [ _∃ i_ : _zω_ [ _i_ ] = _j_ ], and we merge the two branch masks by union, 


In parallel, we compute the soft relaxation used for backpropagation. The row-wise probabilities _Pω_ = softmax( _S_<sup>ˆ</sup> _ω_ ) give _Pω_ [ _i, j_ ] as the relaxed probability that row _i_ votes for token _j_ . Treating perrow votes as conditionally independent, the probability that token _j_ receives at least one vote within branch _ω_ is the _noisy-OR_ [16] over rows (see Appendix Section A), _ρω_ [ _j_ ] = 1 _−_<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_v_(1</sup><sup>_−Pω_[</sup><sup>_i, j_]).</sup> 

4 

We aggregate the two branches by an analogous noisy-OR over branches: 


The straight-through gate combines the hard union mask and the soft union probability _w_ [ _j_ ] = _m_ [ _j_ ] + _ρ_ [ _j_ ] _−_ sg( _ρ_ [ _j_ ]), where sg( _·_ ) denotes stop-gradient. Thus, _w_ [ _j_ ] equals the hard mask _m_ [ _j_ ] in the forward pass, while gradients through _w_ [ _j_ ] follow the soft probability _ρ_ [ _j_ ]. During training, each retained token _Hv_ [ _j_ ] with _j ∈ M_ is multiplied by _w_ [ _j_ ] before being packed into _Hv_<sup>_M_.At inference</sup> time, we use the hard mask directly. 

**Diversity regularization.** To prevent the instruction and proprioception branches from selecting identical token sets, we aggregate the unperturbed scores over voting rows, _rω_ [ _j_ ] =<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_vSω_[</sup><sup>_i, j_],</sup> and penalize agreement between the resulting normalized selection distributions: 


where simcos( _·, ·_ ) denotes cosine similarity and _γ_ is the diversity margin. This encourages complementary instruction and proprioception guidance while still allowing the union mask _M_ to retain evidence supported by both branches. 

**Global context token.** Aggressive token selection can remove scene-level information that receives little support from individual votes but remains useful for action generation. To preserve coarse visual context, we append a learned global token computed from the full pre-selection visual sequence, 


where _Wc_ is a learned linear projection. 

### **3.3 Training Objective** 

After visual token gating, the VLM maps the compact multimodal sequence to conditioning features, _C_ = _f_ VLM([ _Hv_<sup>_M_;</sup><sup>_H_ctx;</sup><sup>_Hq_;</sup><sup>_Hl_]).The selector,VLM backbone,and action head are trained end-</sup> to-end. We train the action head with flow matching [17]. We sample a continuous flow time _T ∼_ Unif(0 _,_ 1) and construct a noisy action chunk **_a_**<sup>_T_</sup> _t_ : _t_ + _H_<sup>= (1</sup><sup>_−T_)</sup><sup>**_a_**</sup><sup>_t_:</sup><sup>_t_+</sup><sup>_H_+</sup><sup>_Tϵ_, where</sup><sup>_ϵ ∼N_(0</sup><sup>_,_</sup><sup>**I**).</sup> Following FLOWER, we embed _T_ and inject it into the action Transformer through global AdaLNstyle modulation, while the action tokens cross-attend to _C_ . Under this linear interpolation, the target velocity field is _dTd_<sup>**_a_**</sup><sup>_T_</sup> _t_ : _t_ + _H_<sup>=</sup><sup>_ϵ −_</sup><sup>**_a_**</sup><sup>_t_:</sup><sup>_t_+</sup><sup>_H_.The action head predicts</sup><sup>_vθ_=</sup><sup>_f_ACT(</sup><sup>**_a_**</sup><sup>_T_</sup> _t_ : _t_ + _H_<sup>_, T, C_), and</sup> we optimize _L_ fm = E _T,ϵ_ . The final training objective combines the flow � _∥vθ −_ ( _ϵ −_ **_a_** _t_ : _t_ + _H_ ) _∥_<sup>2�</sup> matching loss with the branch diversity regularizer, 


where _λ_ div controls the strength of the diversity regularizer. 

## **4 Experiments** 

We address the following research questions: **RQ1** : How should proprioception be represented and incorporated into a VLA policy? **RQ2** : Can proprioception guide visual-token selection to retain taskand state-relevant evidence while reducing inference cost? **RQ3** : Do the resulting design choices improve manipulation performance and efficiency across simulation and real-world tasks? 

### **4.1 Experiments Setup** 

**Baselines.** On CALVIN, we compare against single-system VLAs such as OpenVLA [2], which represents actions as discrete tokens, and methods with dedicated continuous-control action heads, including GR-1 [18], RoboFlamingo [19], _π_ 0 [3], _π_ 0 _._ 5 [4], and FLOWER [6]. We report _π_ 0 and 

5 

Table 2: Simulation benchmark results. CALVIN ABC _→_ D reports success rate (%) at each chain length and average completed chain length. LIBERO reports success rate (%) across 10 tasks per suite.<sup>_∗_</sup> Finetuned by us. Best results are in **bold** ; second-best are underlined. 

||**(**|**a) CALV**|**IN ABC**_→_|**D**||||**(**|**b) LIBER**|**O**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|**LH-1**_↑_|**LH-2**_↑_|**LH-3**_↑_|**LH-4**_↑_|**LH-5**_↑_|**Avg.** _↑_|**Method**|**Spa.** _↑_|**Obj.** _↑_|**Goal**_↑_|**Long**_↑_|**Avg.** _↑_|
|OpenVLA|91.3|77.8|62.0|52.1|43.5|3.27|OpenVLA|84.7|88.4|79.2|53.7|76.5|
|GR-1|85.4|71.2|59.6|49.7|40.1|3.06|WorldVLA|85.6|89.0|82.6|59.0|79.1|
|RoboFlamingo|82.4|61.9|46.6|33.1|23.5|2.47|SmolVLA|93.0|94.0|91.0|77.0|88.8|
|_π_<sup>_∗_</sup><br>0|70.0|48.0|37.0|28.0|18.0|2.01|OpenVLA-OFT|97.6|98.4|97.9|94.5|97.1|
|_π_<sup>_∗_</sup><br>0_._5|71.0|56.0|45.0|37.0|29.0|2.38|COA-VLA|85.3|93.1|85.8|55.0|79.8|
|SuSIE|87.0|69.0|49.0|38.0|26.0|2.69|_π_0|96.8|98.8|95.8|85.2|94.2|
|VPP|95.7|91.2|86.3|81.0|75.0|4.29|_π_0_._5|98.0|97.8|95.6|85.8|94.3|
|Seer|96.3|91.6|86.1|80.3|74.0|4.29|FLOWER|97.5|99.1|96.1|94.9|96.9|
|FLOWER|**99.3**|**96.0**|90.3|82.3|75.5|4.44|LightVLA|**98.4**|98.4|**98.2**|94.6|97.4|
|**ThinkProprio**|98.9|95.4|**91.6**|**86.4**|**79.1**|**4.52**|**ThinkProprio**|**98.4**|**99.2**|98.0|**95.2**|**97.7**|


Table 3: Real-world task success rates. Left: <u>pick-place tasks.</u> Right: drawer tasks. 

|**Pick-place**|**B**|**anana**|**C**|**orn**||**Tape**||**Dr**|**awer**|
|---|---|---|---|---|---|---|---|---|---|
||**FLOWER**|**ThinkProprio**|**FLOWER**|**ThinkProprio**|**FLOWER**|**ThinkProprio**||**FLOWER**|**ThinkProprio**|
|Basket_→_Plate|16/20|17/20|17/20|19/20|16/20|19/20||162|12|
|Basket_→_Table|16/20|18/20|15/20|18/20|17/20|19/20|Open|/0|8/0|
|Plate_→_Basket|19/20|17/20|15/20|16/20|16/20|16/20|Cl|16/20|18/20|
|Table_→_Basket|16/20|18/20|15/20|17/20|16/20|19/20|ose|||


_π_ 0 _._ 5 results from our own fine-tuning runs, marked with<sup>_∗_</sup> . We further compare with visual planning methods, including SuSIE [20], VPP [21], and Seer [22]. On LIBERO, we compare with strong OpenVLA variants and recent VLA baselines, including OpenVLA-OFT [23], COA-VLA [24], LightVLA [11], WorldVLA [25] and SmolVLA [5]. Unless otherwise noted, all reported results are means over 5 seeds. 

**Simulation & Real-world setup.** We evaluate ThinkProprio in both simulation and the real world. **CALVIN** [26] evaluates Realsense D455 UR3 long-horizon control by requiring policies to complete chains of five tasks. **LIBERO** [27] evaluates generalization across four suites, Spatial, Object, Goal, and Long. For real-world Realsense D435 evaluation, we use a UR3 arm with a parallel gripper and two Robo ~~t~~ iq RGB cameras: a fixed third-person view and a wrist-mounted view, as shown in Figure 3. We collect approximately 120 minutes of teleoperated demonstrations and fine-tune from a pretrained checkpoint. The real-world experiments contains 14 tasks: 12 pick-and-place tasks across three objects (banana, Figure 3: Real-world task setup. corn, and tape), and two drawer tasks (open and close). The Gumbel exploration noise annealed from 1.0 to 0.01 and a diversity regularizer using weight 5 _×_ 10<sup>_−_4</sup> , margin _γ_ = 0 _._ 75. Full implementation details are in Appendix Section B. 

### **4.2 Performance and Efficiency** 

**Simulation performance.** On CALVIN ABC _→_ D (Table 2a), success drops with chain length, consistent with compounding errors. ThinkProprio achieves the best Avg. Len. of 4 _._ 52, exceeding FLOWER’s 4 _._ 44. FLOWER is stronger at LH-1 and LH-2, while ThinkProprio leads from LH-3 to LH-5, consistent with state-conditioned gating helping most when configuration drift accumulates over longer chains. The gains are strongest at longer horizons: ThinkProprio reaches 86 _._ 4 % at LH-4 and 79 _._ 1 % at LH-5, reducing FLOWER’s LH-5 failure rate by roughly 15 %. This supports the intuition that state- and instruction-guided token selection helps retain key visual evidence as the configuration evolves. On LIBERO (Table 2b), ThinkProprio achieves the best overall success, ties on LIBERO-Spatial, and leads on LIBERO-Object and LIBERO-Long. 

6 


Figure 4: Qualitative token-selection results on LIBERO, CALVIN, and the real-world setup. Across time, the retained tokens track task-relevant objects, targets, and robot–object interaction regions. 

**Real-world robot evaluation.** We compare against FLOWER as the strongest baseline for real world experiments. Table 3 reports successful trials out of 20 for each task. ThinkProprio achieves an overall success rate of 88 _._ 9 % against 80 _._ 7 % for FLOWER. Gains are consistent across objects and task categories: ThinkProprio matches or exceeds FLOWER on 13 of 14 tasks, with the single exception being Banana Plate _→_ Basket (17/20 vs. 19/20). Drawer manipulation shows a uniform improvement of 18/20 versus 16/20 on both open and close. These results confirm that selected visual tokens provide consistent gains across diverse task configurations. 

**Computational efficiency.** Table 4 compares inference cost on CALVIN ABC _→_ D. ThinkProprio keeps only about 12 of 100 visual tokens per step on average, shortening the sequence processed by both the VLM and the action head. The selector gathers the kept tokens, pads to the per-batch max, and supplies an attention mask. Despite this overhead, ThinkProprio reaches lower endto-end latency than FLOWER (22 ms vs. 52 ms). Peak VRAM grows marginally over FLOWER from selector parameters, still far below OpenVLA. 

Table 4: Inference efficiency on CALVIN ABC _→_ D. Latency is per timestep in ms; VRAM is MB. 

|**Method**|**Tokens **|**Latency **|**VRAM **|**Avg. Len.**|
|---|---|---|---|---|
|OpenVLA|256|164|14574|3.27|
|_π_0|256|104|6692|2.01|
|_π_0_._5|256|138|7038|2.38|
|FLOWER|100|52|1848|4.44|
|**ThinkProprio**|**12**|**22**|**1899**|**4.52**|


### **4.3 Token Selection Analysis** 

**Qualitative behavior.** Figure 4 visualizes retained tokens across simulation and real-world rollouts. The two streams play complementary roles: instruction selected tokens cover task-referenced objects and target regions, while proprioception selected tokens track the gripper and its immediate contact area, with overlap concentrated at the moment of interaction. 

**Complementary query sources.** Table 5 decomposes retained tokens by query source. The overlap stays below one token across all benchmarks, an order of magnitude smaller than either stream alone, so the proprioception branch contributes genuinely complementary evidence rather than re-selecting languagegrounded objects. The retained set thus extends beyond a language-conditioned object mask to include configuration-dependent interaction cues. 

Table 5: Retained-token counts by query source. Both gives their overlap. 

|**Benchmark**|lang|prop|**Both**|
|---|---|---|---|
|CALVIN|8_._60_±_0_._36|3_._52_±_0_._39|0_._25_±_0_._10|
|LIBERO-Spa.|4_._78_±_0_._83|3_._37_±_0_._57|0_._35_±_0_._08|
|LIBERO-Obj.|4_._48_±_0_._44|2_._58_±_0_._27|0_._18_±_0_._14|
|LIBERO-Goal|3_._43_±_0_._48|2_._60_±_0_._50|0_._10_±_0_._08|
|LIBERO-Long|4_._17_±_0_._49|3_._47_±_0_._17|0_._17_±_0_._08|
|Real-World|9_._36_±_0_._42|5_._87_±_0_._28|0_._61_±_0_._13|


7 

### **4.4 Ablation Studies** 

We isolate the design choices behind ThinkProprio with others fixed, ablating each component’s contribution and the entry point for proprioception driving visual-token selection. 

**Component ablation.** In Table 6, VLMvocabulary proprioceptive tokens give a small but consistent gain across CALVIN and LIBERO-Spatial. Visual token selection alone reduces the visual-token budget but slightly hurts performance, suggesting that local selection can discard scenelevel evidence needed for action generation. Adding the global context token _H_<sup>ctx</sup> recovers this loss, and the diversity loss gives the best result on both benchmarks by encouraging selected tokens to cover complementary evidence. 

Table 6: Ablations on CALVIN ABC _→_ D and LIBEROSpatial. Tokens denotes the retained visual-token budget. 

||**CALV**|**IN ABC**_→_**D**|**LIBE**|**RO-Spatial**|
|---|---|---|---|---|
|**Method variant **|**Tokens**|**Avg. Len.** _↑_|**Tokens**|**SR**_↑_|
|FLOWER|All|4_._44_±_0_._03|All|97_._5_±_0_._08|
|+Proprio tokens|All|4_._45_±_0_._02|All|97_._8_±_0_._05|
|+Token selection <br>|_∼_12 %|4_._35_±_0_._04|_∼_23 %|97_._2_±_0_._06|
|+_H_<sup>ctx</sup>|_∼_12 %|4_._48_±_0_._03|_∼_23 %|98_._2_±_0_._04|
|+Div. loss|_∼_12 %|**4**_._**52**_±_**0**_._**02**|_∼_23 %|**98**_._**4**_±_**0**_._**03**|
|Ω= _{_lang_}_<br>|_∼_8 %<br>|3_._40_±_0_._06|_∼_14 %<br>|96_._6_±_0_._05|
|Ω= _{_prop_}_|_∼_3 %|3_._12_±_0_._10|_∼_10 %|96_._0_±_0_._04|
|Mean pooling|1 %<br>|4_._20_±_0_._02<br>|1 %<br>|90_._3_±_0_._04<br>|
|Max pooling|25 %<br>|4_._33_±_0_._03|25 %<br>|92_._8_±_0_._02|
|Random|50 %|4_._24_±_0_._02|50 %|87_._4_±_0_._08|


**Query signal for token retention.** The Random 50 % 4 _._ 24 _±_ 0 _._ 02 50 % 87 _._ 4 _±_ 0 _._ 08 lower panel of Table 6 compares practical retention strategies. Task-agnostic pooling and random baselines retain much of FLOWER’s performance, indicating substantial visual redundancy in CALVIN. Query-guided retention is sensitive to the guidance signal: instruction-only captures task-referenced objects but lacks embodiment context, proprioception-only is too narrow without task semantics, and only their combination keeps both object-centric and configuration-dependent cues. The 1 _._ 1 Avg. Len. gap on CALVIN exceeds any plausible budget effect, and the near-zero cross-branch overlap indicates the streams are complementary rather than redundant. 

**Proprioceptive encoding and entry point.** Table 7 isolates proprioceptive integration methods. Where state enters the policy matters as much as whether it is present: late action-head modulation leaves the baseline unchanged, while projecting continuous state into the VLM input hurts performance. VLM-vocabulary proprioceptive tokens avoid this projection mismatch by using the backbone’s native embedding lookup rather 

Table 7: Proprioceptive integration ablation on CALVIN ABC _→_ D. 

|**Encoding**|**Entry**|**ACT cond.**|**Avg. Len.** _↑_|
|---|---|---|---|
|None|–|–|4.44|
|MLP|ACT|AdaLN|4.44|
|MLP|VLM|Cross-attn|4.15|
|VLM-vocab|VLM|Cross-attn|**4.48**|


than a learned feature projector. The standalone gain is modest, but this is the only entry point that both preserves performance and exposes proprioceptive tokens to the downstream visual selector. 

## **5 Conclusion** 

We presented ThinkProprio, a VLA policy that exposes proprioception as VLM-vocabulary tokens and pairs it with language to guide visual-token retention. Across simulation and real-world experiments, ThinkProprio improves strong baselines while substantially reducing inference latency. The ablations show that proprioception is most effective when used as an active signal for visual selection. 

## **Limitations** 

Our real-world evaluation is confined to a setup with rigid objects, broader embodiments, object categories, and baselines remaining future work. The pre-VLM selector forms a vote matrix, incurring _O_ ( _Nv_<sup>2</sup><sup>_D_) cost that may bottleneck higher visual resolutions.Finally, although the selector retains</sup> human-interpretable evidence, it occasionally preserves uninformative patches such as background, as it is supervised by the action objective rather than explicit relevance signals; tightening selection toward interpretable evidence is a promising direction for future work. 

8 

## **References** 

- [1] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

- [2] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, et al. Openvla: An open-source vision-language-action model. In _Conference on Robot Learning_ , pages 2679–2713. PMLR, 2025. 

- [3] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky. _π_ 0: A vision-languageaction flow model for general robot control, 2024. URL `https://arxiv.org/abs/2410. 24164` . 

- [4] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, M. Y. Galliker, D. Ghosh, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, D. LeBlanc, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, A. Z. Ren, L. X. Shi, L. Smith, J. T. Springenberg, K. Stachowicz, J. Tanner, Q. Vuong, H. Walke, A. Walling, H. Wang, L. Yu, and U. Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. URL `https://arxiv.org/abs/2504.16054` . 

- [5] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- [6] M. Reuss, H. Zhou, M. Ruhle, O. E. Ya¨ gmurlu, F. Otto, and R. Lioutikov. Flower: Democratizing˘ generalist robot policies with efficient vision-language-flow models. In J. Lim, S. Song, and H.-W. Park, editors, _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 3736–3761. PMLR, 27–30 Sep 2025. URL `https://proceedings.mlr.press/v305/reuss25a.html` . 

- [7] Z. Hou, T. Zhang, Y. Xiong, H. Duan, H. Pu, R. Tong, C. Zhao, X. Zhu, Y. Qiao, J. Dai, and Y. Chen. Dita: Scaling diffusion transformer for generalist vision-language-action policy. _arXiv preprint arXiv:2503.19757_ , 2025. 

- [8] Q. Li, Y. Liang, Z. Wang, L. Luo, X. Chen, M. Liao, F. Wei, Y. Deng, S. Xu, Y. Zhang, et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- [9] H. Huang, F. Liu, L. Fu, T. Wu, M. Mukadam, J. Malik, K. Goldberg, and P. Abbeel. Otter: A vision-language-action model with text-aware visual feature extraction. _arXiv preprint arXiv:2503.03734_ , 2025. 

- [10] S. Dasari, O. Mees, S. Zhao, M. K. Srirama, and S. Levine. The ingredients for robotic diffusion transformers. _arXiv preprint arXiv:2410.10088_ , 2024. 

- [11] T. Jiang, X. Jiang, Y. Ma, X. Wen, B. Li, K. Zhan, P. Jia, Y. Liu, S. Sun, and X. Lang. The better you learn, the smarter you prune: Towards efficient vision-language-action models via differentiable token pruning. _arXiv preprint arXiv:2509.12594_ , 2025. 

- [12] Y. Rao, W. Zhao, B. Liu, J. Lu, J. Zhou, and C.-J. Hsieh. Dynamicvit: Efficient vision transformers with dynamic token sparsification. _Advances in neural information processing systems_ , 34:13937–13949, 2021. 

- [13] M. S. Ryoo, A. Piergiovanni, A. Arnab, M. Dehghani, and A. Angelova. Tokenlearner: What can 8 learned tokens do for images and videos? _arXiv preprint arXiv:2106.11297_ , 2021. 

9 

- [14] J. Bjorck, F. Castaneda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang,˜ et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [15] M. Reuss, O. E. Ya<sup>¨</sup> gmurlu, F. Wenzel, and R. Lioutikov.˘ Multimodal diffusion transformer: Learning versatile behavior from multimodal goals. _arXiv preprint arXiv:2407.05996_ , 2024. 

- [16] J. Pearl. _Probabilistic reasoning in intelligent systems: networks of plausible inference_ . Elsevier, 2014. 

- [17] Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le. Flow matching for generative modeling, 2023. URL `https://arxiv.org/abs/2210.02747` . 

- [18] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong. Unleashing largescale video generative pre-training for visual robot manipulation. In _The Twelfth International Conference on Learning Representations_ , 2024. URL `https://openreview.net/forum? id=NxoFmGgWC9` . 

- [19] X. Li, M. Liu, H. Zhang, C. Yu, J. Xu, H. Wu, C. Cheang, Y. Jing, W. Zhang, H. Liu, H. Li, and T. Kong. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 

- [20] K. Black, M. Nakamoto, P. Atreya, H. R. Walke, C. Finn, A. Kumar, and S. Levine. Zeroshot robotic manipulation with pre-trained image-editing diffusion models. In _The Twelfth International Conference on Learning Representations_ , 2024. URL `https://openreview. net/forum?id=c0chJTSbci` . 

- [21] Y. Hu, Y. Guo, P. Wang, X. Chen, Y.-J. Wang, J. Zhang, K. Sreenath, C. Lu, and J. Chen. Video prediction policy: A generalist robot policy with predictive visual representations. In _Forty-second International Conference on Machine Learning_ , 2025. 

- [22] Y. Tian, S. Yang, J. Zeng, P. Wang, D. Lin, H. Dong, and J. Pang. Predictive inverse dynamics models are scalable learners for robotic manipulation. _arXiv preprint arXiv:2412.15109_ , 2024. 

- [23] M. J. Kim, C. Finn, and P. Liang. Fine-tuning vision-language-action models: Optimizing speed and success, 2025. URL `https://arxiv.org/abs/2502.19645` . 

- [24] J. Li, Y. Zhu, Z. Tang, J. Wen, M. Zhu, X. Liu, C. Li, R. Cheng, Y. Peng, Y. Peng, and F. Feng. Coa-vla: Improving vision-language-action models via visual-textual chain-of-affordance, 2025. URL `https://arxiv.org/abs/2412.20451` . 

- [25] J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- [26] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

- [27] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36: 44776–44791, 2023. 

- [28] P. Wu, Y. Shentu, Z. Yi, X. Lin, and P. Abbeel. Gello: A general, low-cost, and intuitive teleoperation framework for robot manipulators, 2024. URL `https://arxiv.org/abs/2309. 13037` . 

- [29] Y. Yue, Y. Wang, B. Kang, Y. Han, S. Wang, S. Song, J. Feng, and G. Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution. _Advances in Neural Information Processing Systems_ , 37:56619–56643, 2024. 

10 

- [30] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

## **A Noisy-OR Relaxation for Mask Union** 

This appendix expands the noisy-OR construction inlined in Section 3.2: how it arises as the expected hard mask under a natural row-wise voting model, why it is preferred to simpler differentiable surrogates, and how it interacts with the diversity regularizer. The instantiations used by the selector — across voting rows within a branch and across branches — are stated in the main text and are not repeated here. 

**Boolean union and its noisy-OR relaxation.** The Boolean union of events _b_ 1 _, . . . , bn ∈{_ 0 _,_ 1 _}_ , 


is non-differentiable. Replacing each _bi_ by a Bernoulli probability _pi ∈_ [0 _,_ 1] and assuming the events are conditionally independent gives the differentiable surrogate 


known as the _noisy-OR_ [16]. The term<sup>�</sup> _i_<sup>(1</sup><sup>_−pi_)istheprobabilitythatnoeventoccurs,so</sup> subtracting it from one gives the probability that at least one does. 

**Probabilistic interpretation in the selector.** The noisy-OR is not introduced from the outside as a smooth approximation of _∨_ . Treating each row’s softmax _Pω_ [ _i, ·_ ] as a categorical distribution over which token row _i_ votes for, and the rows as conditionally independent, the probability that token _j_ receives at least one vote across the _Nv_ rows is exactly 


where _mω_ [ _j_ ] = **1** [ _∃ i_ : _zω_ [ _i_ ] = _j_ ] is the hard branch mask. The same identity applies across branches when branch decisions are taken as independent. The soft scores _ρω_ [ _j_ ] and _ρ_ [ _j_ ] used in Section 3.2 are therefore the expected hard masks under the row-wise and cross-branch surrogate voting models, not arbitrary smooth surrogates. 

### **Properties relied on by the selector.** 

- **(P1) Boundary agreement with hard OR.** _ρ∨_ = 0 iff every _pi_ = 0, and _ρ∨ →_ 1 if any _pi →_ 1. The forward-pass mask and the soft expectation agree at the corners of [0 _,_ 1]<sup>_n_</sup> . 

- **(P2) Strict monotonicity with non-degenerate gradient.** _∂ρ∨/∂pi_ =<sup>�</sup> _k̸_ = _i_<sup>(1</sup><sup>_−pk_)</sup><sup>_≥_0, with</sup> equality only when some other _pk_ = 1. Every input receives a gradient unless the union is already saturated by another event. 

- **(P3) Bounded without renormalization.** _ρ∨ ∈_ [0 _,_ 1] for any _n_ , so evidence aggregated over _Nv_ rows or two branches needs no division by _n_ . 

- **(P4) Union-style accumulation without dilution or overshoot.** Two independent moderate votes reinforce (e.g. _p_ 1 = _p_ 2 = 0 _._ 5 give _ρ∨_ = 0 _._ 75), a single confident vote keeps the union near 1 regardless of how many low-confidence votes accompany it, and the value never exceeds 1. 

11 

Table 8: Differentiable surrogates for the Boolean union of _n_ Bernoulli events. Only the noisy-OR satisfies all four properties. 

|**Surrogate**|**P1**|**P2**|**P3**|**P4**|
|---|---|---|---|---|
|max_i pi_|Yes|Partial|Yes|No|
|�<br>_i _<sup>_pi_</sup><br>|No|Yes|No|No|
|1<br>_n_<br>�<br>_i _<sup>_pi_</sup>|No|Yes|Yes|No|
|**Noisy-OR**1_−_<sup>�</sup><br>_i_<sup>(1</sup><sup>_−pi_)</sup>|Yes|Yes|Yes|Yes|


**Comparison with simpler surrogates.** Table 8 contrasts noisy-OR with three natural alternatives. The maximum max _i pi_ satisfies P1 and P3 but is gradient-zero away from the arg max (P2 partial) and does not accumulate: two votes at _p_ = 0 _._ 5 stay at 0 _._ 5 rather than reinforcing each other (P4 violated). The sum<sup>�</sup> _i_<sup>_pi_violates P1 and P3 by exceeding 1.The normalized mean</sup> _n_<sup><u>1</u></sup> � _i_<sup>_pi_restores</sup> boundedness but breaks P1, and _dilutes_ one confident vote among many low-confidence ones down toward 1 _/n_ — exactly the regime the selector operates in, where only a small fraction of rows vote confidently for any given column. 

**Independence assumption and the role of the diversity regularizer.** The expected-mask identity above holds exactly when the underlying votes are conditionally independent; otherwise the noisy-OR is an approximation. In the selector this assumption appears at two scales. 

_Across voting rows within a branch._ The rows share a single score matrix and are not strictly independent, but each row casts at most one effective vote and the guidance-conditioned queries separate row distributions, so we expect the residual dependence to be limited. 

_Across branches._ We do not attempt to enforce probabilistic independence between the language and proprioception branches. The diversity regularizer _L_ div instead discourages branch collapse by penalizing cosine similarity between the row-aggregated selection distributions softmax( _r_ lang) and softmax( _r_ prop), which reduces empirical overlap and keeps branch behavior aligned with the complementary-branch intent of the architecture. This narrows the regime in which the cross-branch noisy-OR is loosest — heavily overlapping branches — without claiming the approximation is exact. 

**Role in the forward pass.** The noisy-OR never enters the forward computation. The selector uses the hard Boolean union _m_ [ _j_ ] = _m_ lang[ _j_ ] _∨ m_ prop[ _j_ ] both at inference and at the forward step of training, and the straight-through gate routes gradients through the soft _ρ_ [ _j_ ] while leaving the forward value equal to _m_ [ _j_ ]. The relaxation therefore only shapes the learning signal; deployed model behavior is identical to that of a deterministic argmax-union selector. 

**Gradient flow and token exploration.** The straight-through gate passes gradient only to tokens in the current selection _M_ : tokens with _m_ [ _j_ ] = 0 are dropped from _Hv_<sup>_M_</sup> before the VLM, so their gate value _w_ [ _j_ ] never enters the loss and they receive no direct gradient in that step. Coverage of the full token set is instead provided over training by the Gumbel perturbation _S_<sup>ˆ</sup> _ω_ = _Sω_ + _α_ Γ _ω_ . Early in training, the large exploration scale _α_ makes the per-row argmax votes stochastic, so the realized selection _M_ varies from step to step and, across steps, most visual tokens are eventually selected and updated at least once. A dropped token also continues to shape learning indirectly, since it participates in the scores of other tokens (as a voting row in _H_<sup>˜</sup> _v_ and through the row-wise normalization) and in the aggregated selection distributions _rω_ used by _L_ div. As _α_ anneals from 1 _._ 0 to 0 _._ 01, selection sharpens toward the deterministic argmax-union used at inference, so exploration is concentrated early and the gate becomes effectively hard by convergence. This is distinct from property (P2), which concerns the gradient of the noisy-OR surrogate with respect to its probability inputs rather than the realization of the discrete forward selection. 

12 


(a) Overhead view. 


(b) Side view. 

Figure 5: Customized GELLO-style leader-side teleoperation interface used for collecting real-world demonstrations. 

## **B Experiment Details** 

### **B.1 Observations and Proprioceptive State** 

Image preprocessing follows the dataset transform configs. For CALVIN, the static and grippercamera views are resized to 224 _×_ 224. During training, we apply RandomShiftsAug with padding 10 for the static view and padding 4 for the gripper view, then scale images to [0 _,_ 1] and normalize with CLIP statistics. Validation disables RandomShiftsAug but keeps resize and normalization. The proprioceptive state is the 15D robot observation vector, normalized using dataset statistics and with additional normalization of orientation entries. Actions are 7D relative end-effector commands scaled to [ _−_ 1 _,_ 1]. 

For LIBERO, we use the same augmentation and normalization structure, resizing images to 112 _×_ 112. We form a 9D proprioceptive state by concatenating seven joint values with the 2D gripper state. Actions use the same 7D relative command parameterization and are scaled to [ _−_ 1 _,_ 1]. 

For real-world evaluation, we use the same two-stream policy interface with a fixed third-person camera and a wrist-mounted camera. Both views are resized to 224 _×_ 224 and normalized with Florence/CLIP-style image statistics; training additionally uses RandomShiftsAug with padding 10 for the static view, padding 4 for the wrist view, and color jitter. The UR3 proprioceptive state is a 16D vector containing end-effector position (3), end-effector quaternion (4), gripper state (1), six joint values (6), and two zero-padded dimensions, normalized using statistics computed from training episodes. Actions contain six relative pose deltas and one gripper command; the motion dimensions are normalized and the gripper target is binarized. Across CALVIN, LIBERO, and real-world runs, unless otherwise specified, normalized proprioceptive values are clipped to [ _−_ 3 _,_ 3], uniformly discretized into _B_ = 256 bins, and mapped to VLM-vocabulary token IDs as in Section 3.1; Table 14 studies this bin and clip choice. The real-world dataset contains approximately 120 minutes of teleoperated demonstrations over 14 tasks: 12 pick-and-place tasks across banana, corn, and tape using Basket _→_ Plate, Basket _→_ Table, Plate _→_ Basket, and Table _→_ Basket routes, plus two drawer tasks, open and close. 

**Teleoperation interface.** The real-world demonstrations were collected with the customized GELLO-style leader-side teleoperation interface shown in Figure 5 [28]. The operator moves a lightweight linkage and gripper handle, and the adapted software maps these inputs to the UR3 during data collection. The policy observations remain the fixed and wrist-mounted RGB streams together with the robot proprioceptive state described above. 

13 

Table 9: Training and optimization hyperparameters used across experiments. 

|Setting|Value|
|---|---|
|Optimizer|AdamW<br>|
|Learning rate|2_×_10<sup>_−_5</sup>|
|AdamW betas|(0_._9_,_0_._95)|
|Weight decay|0_._05(no decay on norm/bias)|
|Per-GPU batch size|8|
|Number of GPUs|1|
|Total steps|50_,_000|
|LR schedule|tri-stage (warmup_→_hold_→_cosine)|
|Warmup / hold / decay|0_._05_/_0_._10_/_0_._85|
|Warmup start lr|0_._1_×_lr|
|Final lr|0_._5_×_lr|
|Precision|bf16-mixed|
|EMA decay|0_._999|
|<br>VLM token dropout|0_._1|
|Gumbel scale|1_._0_→_0_._01|
|Diversity loss|_λ_div = 5_×_10<sup>_−_4</sup>, margin_γ_ = 0_._75|


### **B.2 Model Architecture** 

We build on FLOWER and use Florence-2-Large ( `microsoft/Florence-2-large` ) as the visionlanguage backbone. Following FLOWER’s recipe, we fine-tune Florence rather than freezing it, so comparisons use the same backbone adaptation regime. A special token `<Flow>` is embedded and inserted to mark the conditioning boundary, and we apply token dropout with probability 0.1 to the VLM encoder outputs during training. The pre-VLM selector uses the branch-specific vote-matrix scoring described in Section 3.2 for the instruction and proprioception branches, and its global context token uses the learned linear projection _Wc_ to compute _H_<sup>ctx</sup> from the mean pre-selection visual feature. The action generator is a rectified-flow / Diffusion Transformer with hidden size 1024, 18 transformer layers, and 16 attention heads, using dropout 0.1 in attention, residual, and MLP blocks. The policy predicts an action chunk of length 10, executed with chunked replanning every 10 environment steps. 

### **B.3 Optimization Hyperparameters** 

We train end-to-end with AdamW using learning rate 2 _×_ 10<sup>_−_5</sup> , betas (0 _._ 9 _,_ 0 _._ 95), and weight decay 0.05 applied to non-normalization and non-bias parameters (norm/bias parameters use zero weight decay). Training uses bf16-mixed precision with per-GPU batch size 8 on one GPU. We use a tri-stage learning-rate schedule over 50k steps (matching `max` ~~`e`~~ `pochs=50` and `limit` ~~`t`~~ `rain` ~~`b`~~ `atches=1000` ): (i) linear warmup for 5% of steps from 0 _._ 1 _×_ lr to lr, (ii) constant hold for 10% of steps, and (iii) cosine decay for the remaining 85% to a final learning rate of 0 _._ 5 _×_ lr. Selector training anneals the Gumbel exploration scale from 1.0 to 0.01 and uses the branch diversity coefficient _λ_ div = 5 _×_ 10<sup>_−_4</sup> from the objective _L_ = _L_ fm + _λ_ div _L_ div, with margin _γ_ = 0 _._ 75. We additionally maintain an exponential moving average (EMA) of parameters with decay 0.999 and use EMA weights for evaluation. 

### **B.4 Inference Settings and Measurement Protocol** 

At inference time, we run rectified-flow sampling with 4 steps ( `num` ~~`s`~~ `ampling` ~~`s`~~ `teps=4` ) per action chunk. The model predicts a 10-step chunk and replans every 10 environment steps. Inference is performed in bf16 and always uses both camera views. 

CALVIN long-horizon evaluation follows the standard 5-subtask instruction-chain protocol: each subtask is given up to 360 environment steps, and we report success rates for completing 1 through 5 

14 

subtasks as well as the average successful sequence length. LIBERO evaluation uses 50 trials per task with a maximum horizon of 520 environment steps; we report per-task success and suite averages. 

For latency and VRAM profiling, we measure per-environment-step end-to-end inference time including vision encoding, the pre-VLM selector, the Florence encoder forward pass, and all diffusion sampling steps. Although the policy predicts 10-action chunks, the latency values in Tables 4 and 13 are reported per environment step rather than as a total per action chunk. We compute latency with CUDA synchronization to avoid asynchronous kernel overlap artifacts, and report the mean over a fixed number of inference steps (1000 steps in our efficiency tables). In Table 13, the Vision column includes encoding both camera views. Peak VRAM is reported as the maximum allocated GPU memory during inference. All profiling numbers in the paper are collected on a single RTX 4090 GPU under the same bf16 and two-view settings as evaluation. 

### **B.5 Baseline Details** 

For the extended tables, we keep only the architecture attributes needed to interpret efficiency: scale, backbone, and visual-token count; “–” denotes not applicable or not reported. 

**FLOWER.** FLOWER [6] is the closest dual-system baseline to our implementation. It uses Florence2-Large as the vision-language backbone and conditions a flow-based action generator through dense cross-attention. We compare against FLOWER under the same benchmark settings used in the main simulation table. 

_π_ 0 **and** _π_ 0 _._ 5 **.** _π_ 0 [3] and _π_ 0 _._ 5 [4] pair a PaliGemma VLM with a flow-based action generator. We fine-tune the open variants on CALVIN ABC _→_ D, using them to compare continuous proprioceptive action-head conditioning against token-form proprioceptive input. These are the<sup>_∗_</sup> -marked _π_ 0 and _π_ 0 _._ 5 rows in the main CALVIN table. 

**OpenVLA and OpenVLA-OFT.** OpenVLA [2] is a single-system VLA that discretizes actions as language-model tokens. OpenVLA-OFT [23] extends this family with an action expert and improved fine-tuning recipe, and is included for LIBERO comparisons. 

**GR-1.** GR-1 [18] is a generative robot policy that combines visual encoders with a sequence model for language-conditioned manipulation. We include it as a compact VLA-style baseline on CALVIN. 

**RoboFlamingo and DeerVLA.** RoboFlamingo [19] adapts a Flamingo-style vision-language model to robot control. DeerVLA [29] builds on this family with improved data and training choices, providing additional single-system VLA comparisons on CALVIN. 

**LightVLA.** LightVLA [11] is the closest efficiency-oriented baseline. We distinguish it from ThinkProprio along four axes: 

- **Target.** LightVLA targets visual-token computation reduction through instruction-guided pruning, whereas ThinkProprio asks how proprioception should participate in visual grounding. 

- **Guidance signal.** LightVLA uses the instruction as the pruning signal; ThinkProprio uses separate language and proprioception branches so task semantics and robot-state cues can make complementary votes. 

- **Selection mechanism.** ThinkProprio merges branch masks with a hard union in the forward pass and a noisy-OR relaxation for gradients. 

- **Regularization and context.** ThinkProprio uses a diversity loss to discourage the two branches from collapsing to the same selection pattern, and keeps a global context token so aggressive local selection does not discard coarse scene information. 

**Diff-P-CNN and MDT.** Diff-P-CNN [30] and MDT [15] are diffusion-style manipulation policies without a large VLM backbone. They provide non-VLM references for CALVIN, especially on the D _→_ D split. 

15 

**SuSIE, VPP, and Seer.** SuSIE [20], VPP [21], and Seer [22] are visual planning or predictive representation baselines. They are included to compare against methods that rely on planningoriented visual abstractions rather than a VLM-action-head decomposition. 

**RoboUniView.** RoboUniView is included in the CALVIN D _→_ D comparison as a prior multi-view robot learning baseline. We report it only where the corresponding split result is available. 

## **C Additional Results** 

### **C.1 CALVIN Long-Horizon Results** 

Table 10 extends the main CALVIN ABC _→_ D comparison in Table 2a with architecture details, while Tables 11 and 12 report the additional ABCD _→_ D and D _→_ D splits. In these tables, the Tokens column is the average number of retained visual tokens per timestep out of 100 input visual tokens. The split-specific means for ThinkProprio are 12, 15, and 14 tokens; the “around 15 %” statement in the main text is a rounded summary across CALVIN settings. 

Table 10: CALVIN ABC _→_ D long-horizon success with architecture details. 

|**Method**||**Architecture**||||**Perfo**|**rmance**|||
|---|---|---|---|---|---|---|---|---|---|
||**Scale (B)**|**Backbone**|**Tokens**_↓_|**LH-1**_↑_|**LH-2**_↑_|**LH-3**_↑_|**LH-4**_↑_|**LH-5**_↑_|**Avg. Len.** _↑_|
|SuSIE|–|–|–|87_._0|69_._0|49_._0|38_._0|26_._0|2_._69|
|VPP|1.5|SVD+CLIP|–|95_._7|91_._2|86_._3|81_._0|75_._0|4_._29|
|Seer|0.3|ViT+CLIP<br>Llama-2|–|96_._3|91_._6|86_._1|80_._3|74_._0|4_._29|
|OpenVLA|7.7|DINOv2+SigLIP<br>CLIP|256|91_._3|77_._8|62_._0|52_._1|43_._5|3_._27|
|GR-1|0.195|MAE-ViT<br>OpenFlamingo|–|85_._4|71_._2|59_._6|49_._7|40_._1|3_._06|
|RoboFlamingo|3|ViT|128|82_._4|61_._9|46_._6|33_._1|23_._5|2_._47|
|_π_<sup>_∗_</sup><br>0|3.3|PaliGemma|512|70_._0|48_._0|37_._0|28_._0|18_._0|2_._01|
|_π_<sup>_∗_</sup><br>0_._5|3.3|PaliGemma|512|71_._0|56_._0|45_._0|37_._0|29_._0|2_._38|
|FLOWER|0.95|Florence-2-L|100|**99****_._3**|**96****_._0**|90.3|82.3|75.5|4.44|
|**ThinkProprio**|0.95|Florence-2-L|**12**|98.9|95.4|**91****_._6**|**86****_._4**|**79****_._1**|**4****_._52**|


Table 11: CALVIN ABCD _→_ D long-horizon success with architecture details. 

|**Method**||**Architecture**||||**Perfo**|**rmance**|||
|---|---|---|---|---|---|---|---|---|---|
||**Scale (B)**|**Backbone**|**Tokens**_↓_|**LH-1**_↑_|**LH-2**_↑_|**LH-3**_↑_|**LH-4**_↑_|**LH-5**_↑_|**Avg. Len.** _↑_|
|Diff-P-CNN|0.32|–<br>OpenFlamingo|–|86_._3|72_._7|60_._1|51_._2|41_._7|3_._16|
|RoboFlamingo|3.0|ViT|128|96_._4|89_._6|82_._4|74_._0|66_._0|4_._09|
|DeerVLA|3.0|OpenFlamingo<br>MAE-ViT|128|99_._1|93_._3|82_._1|74_._6|63_._8|4_._13|
|GR-1|0.195|GPT|–|94_._9|89_._6|84_._4|78_._9|73_._1|4_._21|
|FLOWER|0.95|Florence-2-L|100|98_._9|96_._7|93_._9|90_._2|85_._5|4_._62|
|**ThinkProprio**|0.95|Florence-2-L|**15**|**99.5**|**97.2**|**96.6**|**92.3**|**88.5**|**4.74**|


Table 12: CALVIN D _→_ D long-horizon success with architecture details. 

|**Method**||**Architecture**||||**Perf**|**ormance**|||
|---|---|---|---|---|---|---|---|---|---|
||**Scale (B)**|**Backbone**|**Tokens**_↓_|**LH-1**_↑_|**LH-2**_↑_|**LH-3**_↑_|**LH-4**_↑_|**LH-5**_↑_|**Avg. Len.** _↑_|
|MDT|–|–|–|93_._7|84_._5|74_._1|64_._4|55_._6|3_._72|
|RoboUniView|–|–|–|96_._2|88_._8|77_._6|66_._6|56_._3|3_._85|
|**ThinkProprio**|0.95|Florence-2-L|**14**|**96****_._9**|**89****_._8**|**83****_._6**|**80****_._5**|**72****_._7**|**4****_._23**|


LH- _k_ is the success rate (%) of completing _k_ consecutive subtasks in the five-subtask evaluation chain, and Avg. Len. is the mean number of consecutively completed subtasks. The architecture columns provide model scale, backbone, and visual-token count when available. In the ABCD _→_ D setting, ThinkProprio achieves the best Avg. Len. (4.74) and the best LH-5 result (88.5). In D _→_ D, ThinkProprio exceeds the remaining prior baselines reported in Table 12. 

16 

### **C.2 CALVIN Subtask Breakdown** 


Figure 6: Subtask-level breakdown of ThinkProprio on CALVIN ABC _→_ D. We plot the 12 lowestsuccess subtasks among the 34 CALVIN subtasks, ordered by failure rate. Bars report failure rate; right annotations report success rate with successful/evaluated rollout counts. 

Figure 6 complements the chain-level CALVIN metrics by showing where the remaining ABC _→_ D errors occur. Most subtasks are near saturation, so residual failures concentrate in a small set of contact-sensitive or placement-sensitive interactions. Only three subtasks fall below 80% success in this evaluation: _Lift Pink Block Drawer_ (78 _._ 6%), _Push Pink Block Right_ (78 _._ 8%), and _Push Into Drawer_ (79 _._ 4%). The next hardest cases, such as _Place In Slider_ and _Stack Block_ , also require precise placement or sustained contact. This pattern is consistent with the main CALVIN result: ThinkProprio improves long-horizon chain completion, while the remaining failures are concentrated in interactions where small state-estimation or contact-control errors can accumulate. Section D.5 revisits the same contact-and-approach failure mode in real-world rollouts. 

### **C.3 Long-Horizon Qualitative Rollouts** 

17 


Figure 7: Qualitative CALVIN LH-5 rollout from ThinkProprio. Rows correspond to the five consecutive subtasks in the evaluation chain, and columns show representative timesteps within each subtask. Colored overlays visualize visual tokens retained by the instruction and proprioception guidance branches. 


Figure 8: Qualitative LIBERO-Long rollout from ThinkProprio for placing the black bowl in the bottom drawer and closing it. Colored overlays visualize retained visual tokens as the policy transitions from reaching and grasping to drawer interaction and closing. 

18 

Figures 7 and 8 provide qualitative examples of the long-horizon settings where proprioceptive visual grounding is most useful. Across both CALVIN and LIBERO-Long, the retained patches move with the task phase: they cover task-referenced objects and target regions during approach, then shift toward the gripper, drawer, and contact regions during manipulation. These examples complement the aggregate long-horizon metrics by showing that token retention remains state-conditioned over multi-stage execution rather than staying fixed on the initial target object. 

## **D Analysis and Ablations** 

### **D.1 Inference-Time Breakdown** 

Table 13: Mean per-environment-step latency in ms on CALVIN and LIBERO. Tokens reports the average retained visual-token count over the total available visual tokens. 

|**Benchmark**|**Tokens**|**Vision**|**Selector**|**VLM**|**Action**|**Total**|
|---|---|---|---|---|---|---|
|CALVIN ABC_→_D|12/100|5.8|0.1|0.9|15.4|22.2|
|LIBERO|7.8/34|6.5|0.1|1.1|16.1|23.8|


Table 13 decomposes the end-to-end inference time used in Table 4. The token denominators reflect the two-view preprocessing resolutions: CALVIN uses 224 _×_ 224 inputs and produces 100 visual tokens per timestep, whereas LIBERO uses 112 _×_ 112 inputs and produces 34. The Vision column includes encoding both camera views. The selector adds only about 0 _._ 1 ms per step in both benchmarks, while the diffusion action head remains the dominant cost. The total latency is therefore reduced mainly by shortening the sequence processed by the VLM and consumed by the cross-attention action head, rather than by changing the action generator itself. 

### **D.2 Proprioceptive Discretization Sensitivity** 

Table 14: Auxiliary LIBERO-Spatial sensitivity runs for proprioceptive discretization. We vary the number of bins and clipping range used before mapping state values to VLM-vocabulary token IDs. 

|**Bins**|**Clip range**|**Success rate (%)**_↑_|
|---|---|---|
|32|[_−_3_,_3]|94_._5_±_0_._1|
|256|[_−_3_,_3]|98_._4_±_0_._2|
|512|<br>[_−_3_,_3]|98_._4_±_0_._3|
|256|<br>[_−_1_,_1]|96_._1_±_0_._9|
|256|[_−_5_,_5]|96_._2_±_0_._6|


Table 14 shows that proprioceptive tokenization is sensitive to both quantization resolution and clipping range. Too few bins coarsen the state representation, and too narrow or too wide clipping ranges reduce useful variation in the resulting token IDs. Increasing from 256 to 512 bins does not improve performance in this setup, so we use 256 bins over [ _−_ 3 _,_ 3] as the default. These are the defaults used by the VLM-vocabulary proprioceptive encoding in Section 3.1 and by the observation/model setup in Sections B.1 and B.2. This supports the view that VLM-vocabulary proprioception is not simply a free replacement for continuous state: the discretization must retain enough resolution for the robot state while remaining stable under the normalized proprioceptive distribution. 

### **D.3 Selection Consistency** 

Table 15 quantifies whether retained-token masks are structured rather than arbitrary. Each mask records the visual tokens kept in one forward pass, so higher IoU means greater overlap between selected token sets; the matched token budgets are 12/100 for CALVIN ABC _→_ D and 7.8/34 for LIBERO-Spatial. Cross-scene and temporal IoU are both above the random baseline on CALVIN 

19 

Table 15: Intersection-over-Union (IoU) between binary retained-token masks. Cross-scene compares the same instruction across different initial states; Temporal compares neighboring rollout steps; Random is the expected IoU from uniform random retention with the matched token budget (12/100 for CALVIN ABC _→_ D, 7.8/34 for LIBERO-Spatial). 

|**IU**|**CALVIN**|**LIBERO**|
|---|---|---|
|**o**|**ABC**_→_**D**|**Spatial**|
|Cross-scene|0.170|0.644|
|Temporal|0.196|0.418|
|Random|0.064|0.130|


Figure 9: Phase-wise selector behavior on LIBERO-Spatial. Bars show within-phase mask IoU, and the line shows mean tokens kept. Phases are equal thirds of each rollout. 

and LIBERO-Spatial, indicating that selection is task- and state-conditioned. The lower CALVIN cross-scene IoU reflects stronger variation across long-horizon configurations, while the higher LIBERO-Spatial IoU is consistent with the more constrained scene layouts in that suite. 

### **D.4 Phase-Wise Selection Adaptation** 

Figure 9 shows that the selector is not static over an episode. The mean-token line peaks in the middle phase, and the middle-phase IoU bar is the lowest, consistent with grasping and lifting being the most visually dynamic portion of the task. Late-phase masks become more consistent as the robot moves toward the placement target, and the Early–Late IoU bar is approximately 0.29, indicating substantial cross-phase drift. This phase-wise view complements the qualitative rollouts in Figures 7 and 8, where retained tokens shift with objects, gripper motion, and contact regions over execution. 

### **D.5 Qualitative Failure Cases** 

Figure 10 shows two representative real-world failures. In the tape case, the gripper reaches the correct object but contacts it with a misaligned approach, so the final manipulation fails despite the target being visually identified. In the corn case, the approach trajectory clips a nearby banana before establishing clean contact with the corn. These examples point to control-side and contactside limitations, complementing the main-paper Limitations section, which focuses on the tabletop evaluation scope and deployment assumptions. 

20 


Figure 10: Representative real-world failure cases. Top: the gripper reaches the tape but makes misaligned contact. Bottom: the approach to the corn collides with a nearby banana. 

21 

