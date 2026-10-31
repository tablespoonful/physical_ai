---
title: "VLA Knows Its Limits: Adaptive Execution Horizons for Robot Policies"
date: "2026-02-24"
authors: "Haoxuan Wang; Gengyu Zhang; Yan Yan; Ramana Rao Kompella; Gaowen Liu"
url: https://arxiv.org/abs/2602.21445
pdf: https://arxiv.org/pdf/2602.21445
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.21445)** / [論文ページ](https://arxiv.org/abs/2602.21445)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **VLA Knows Its Limits: Adaptive Execution Horizons for Robot Policies** 

**Haoxuan Wang**<sup>1</sup><sup>_,_2</sup> , **Gengyu Zhang**<sup>1</sup><sup>_,_2</sup> , **Yan Yan**<sup>1</sup> , **Ramana Rao Kompella**<sup>2</sup> , **Gaowen Liu**<sup>2</sup><sup>_,†_</sup> 1University of Illinois Chicago 2Cisco Research 

## **Abstract** 

_Action chunking has recently emerged as a standard practice in flow-based Vision-Language-Action (VLA) models. However, the effect and choice of the execution horizon—the number of actions to be executed from each predicted chunk—remains underexplored. In this work, we first show that varying the execution horizon leads to substantial performance deviations, with performance initially improving and then declining as the horizon increases. To uncover the reasons, we analyze the cross- and self-attention weights in flow-based VLAs and reveal two key phenomena: (i) intrachunk actions attend invariantly to vision–language tokens, limiting adaptability to environmental changes; and (ii) the initial and terminal action tokens serve as stable anchors, forming latent centers around which intermediate actions are organized. Motivated by these insights, we interpret action self-attention weights as a proxy for the model’s predictive limit and propose_ **_AutoHorizon_** _, the first test-time method that dynamically estimates the execution horizon for each predicted action chunk to adapt to changing perceptual conditions. Across simulated and real-world robotic manipulation tasks, AutoHorizon is performant, incurs negligible computational overhead, and generalizes across diverse tasks and flow-based models. Video demos are available at this project page._ 

## **1. Introduction** 

As a key milestone toward artificial general intelligence, embodied AI seeks to endow agents with the ability to perceive, reason, and act within the physical world [14, 22]. Recent advances in machine-learning–based control have enabled these agents to directly interact with realworld environments through learned representations [8, 35, 39]. Within this paradigm, Vision-Language-Action (VLA) models [3, 12, 16, 19, 26, 27, 40] have emerged as a promising direction for their ability to ground visual perception and linguistic instruction into executable actions, demonstrating strong performance across diverse languageconditioned robot manipulation tasks. 


Figure 1. **Illustration of the average success rates on the LIBERO benchmark using** _π_ 0 _._ 5 **.** Varying the execution horizon leads to substantial success rate fluctuations, and the policy performance exhibits a peaked pattern, initially improving and then declining as the execution horizon increases. 

To better capture multimodal action distributions and enforce temporal consistency, _action chunking_ [8, 17, 39] has become a standard practice for VLAs trained via imitation learning [1, 34]. Instead of predicting a single action at each step, the policy outputs a sequence of actions—an action chunk. During policy rollout, the robot executes the initial portion (and only rarely the entirety) of the predicted chunk before re-planning, discarding the remaining actions [3, 8]. The total chunk length is termed the _prediction horizon_ , and the executed prefix is the _execution horizon_ [4]. This formulation establishes a closed-loop prediction mechanism, sacrificing long-term consistency for reactivity [21]. 

Empirically, we observed that the policy’s behavior is inherently tied to the length of its executed prefix. As illustrated in Fig. 1, varying the execution horizon leads to substantial performance fluctuations—ranging from consistent successes to frequent failures. Interestingly, the performance also exhibits a characteristic trend: it initially improves and then declines as the execution horizon increases. These findings underscore the importance of selecting an appropriate execution horizon and motivate a fundamental yet underexplored question in action chunking: **How should the execution horizon be determined?** 

Prior works [3, 8, 12, 24, 39] typically set a _fixed_ execu- 

1 

tion horizon, chosen either by human heuristics or through exhaustive evaluation across multiple configurations. Such brute-force tuning quickly becomes time- and computeintensive as the prediction horizon and task complexity increases. Furthermore, we argue that a fixed execution horizon is inherently suboptimal. Liu et al. [21] showed that short horizons improve reactivity but induce instability due to frequent cross-chunk transitions, whereas long horizons enhance temporal smoothness at the expense of responsiveness. Since the balance between consistency and reactivity naturally varies across different phases of policy rollout, the optimal execution horizon should likewise adapt over time. For instance, reaching toward a coffee carafe favors a longer horizon for smooth motion, whereas pouring into a cup requires shorter horizons for heightened responsiveness. These insights emphasize the need of determining the execution horizon adaptively on a per-chunk basis. 

In this paper, we aim to automatically and efficiently determine the execution horizon for each action chunk within flow-based VLAs [12, 24]. To explain why the policy performance exhibits the characteristic trend shown in Fig. 1, we analyze how action generation integrates linguistic and visual information through the attention mechanism [30]. Our analysis reveals two key phenomena: ❶ Intra-chunk actions consistently attend to the same vision–language tokens, indicating that they rely on fixed perceptual contexts. These contexts provide useful guidance for early actions but become increasingly outdated for later ones as the environment changes, revealing the limited adaptability of the predicted chunks. ❷ Predicted actions exhibit strong attention to the initial and terminal action tokens, with correspondence strength remaining high before sharply decaying as temporal distance increases. We refer to these boundary tokens as _radial action sinks_ , which serve as stable anchors around which intermediate actions are organized. 

Building on the observations of the limited adaptability of intra-chunk actions and their reliance on radial action sinks, we formulate execution horizon determination as **estimating the predictive limit of VLAs** . We interpret the action self-attention weights as implicit indicators of the model’s prediction confidence and propose **AutoHorizon** , a dynamic execution horizon estimation strategy for flowbased VLAs trained with action chunking. Our approach leverages the intrinsic structure of attention weights to infer the temporal limit of the model’s reliable forecasting capability. Specifically, we introduce a bidirectional soft-pointer mechanism that locates the first turning points where the attention mass ceases to advance and begins to plateau. These turning points, identified for both initial and terminal radial action sinks, define the estimated execution horizon. 

Our contributions are threefold. **(1)** We focus on flowbased VLAs trained with action chunking, and provide both theoretical and empirical analyses of their performance pat- 

tern with respect to the execution horizon. We further uncover its underlying causes through two key observations linking attention correspondences to the model’s predictive limit. **(2)** Building on these insights, we propose AutoHorizon, a novel attention-guided strategy that dynamically estimates the execution horizon for each action chunk, allowing the policy to adapt to varying perceptual conditions. **(3)** Extensive experiments on simulated and real-world robot manipulation tasks demonstrate that our method generalizes across different flow-based policies, incurs negligible computational overhead, and outperforms strong baselines that rely on exhaustive fixed-horizon tuning. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

The remarkable progress of large language models (LLMs) [25, 29, 33] and vision-language models (VLMs) [2, 6, 41] has sparked growing interest in AI systems capable of acting within the physical world. Among these advances, _Vision-Language-Action (VLA) models_ [3, 5, 11, 12, 16, 18, 19, 24, 31, 36, 38, 40, 42] have emerged as a unifying paradigm that integrates perception, reasoning, and control. By jointly training on large-scale datasets of robotic and human demonstrations, VLAs enable end-to-end learning from visual and linguistic inputs to motor actions, demonstrating strong generalization across diverse language-conditioned manipulation tasks. Within this paradigm, diffusion- and flow-based VLAs [3, 12, 24, 27] have received particular attention for their sample-efficient generation process and high-quality action synthesis. Conditioned on the visual and linguistic embeddings extracted from the backbone VLMs [2, 6], these models iteratively sample from an action distribution to produce low-level motor commands for robotic control, achieving fine-grained temporal consistency and robust performance across complex environments. 

### **2.2. Action Chunking** 

Action chunking policies [3, 8, 12, 35, 39] generate short sequences of consecutive actions for a given state. ACT [39] first introduced the idea of action chunking using Transformers [30] and demonstrated that modeling temporally consistent action sequences enables the learning of finegrained behaviors, outperforming policies that predict single actions. Subsequent works have extended this concept in several directions. ACT further applied weighted averaging to overlapping actions between chunks to enhance policy smoothness. BID [21] provided a theoretical analysis from a policy learning perspective, showing that action chunking promotes long-term temporal consistency but sacrifices short-term reactivity. They also proposed a rejection sampling strategy to select the best-performing chunk 

2 


Figure 2. **Left:** (a) In conventional action chunking, the execution horizon _e_ is heuristically chosen by humans and remains fixed across chunks. (b) In contrast, AutoHorizon (our method) dynamically estimates the execution horizon for each predicted chunk based on the attention weights from the VLA model. **Right:** Real-world demonstration of showing how the estimated execution horizons evolve during policy rollout. When the environment is stable and reactivity is less critical ( _e.g_ ., reaching the cube or moving toward the bowl), the estimated horizon increases to promote smooth, stable motion. Conversely, during physical interaction ( _e.g_ ., grasping or placing the cube), the execution horizon shortens to enhance reactivity and adaptability. 

to address this trade-off. RTC [4] explored action chunking under asynchronous execution [27], formulating chunk prediction as an image inpainting problem [28]. 

Despite these advances, the _choice_ of the execution horizon remains largely unexplored. Existing works [3, 8, 39] typically set this value using human heuristics, determined by the robot’s control frequency and the desired duration of each motion segment. This practice has left the influence of the execution horizon on VLA performance largely unexplored, prompting a fundamental question: _are there better ways to determine the execution horizon?_ 

### **2.3. Attention Weights** 

Attention weights [9, 13, 32, 37] serve as interpretable indicators of information flow between tokens in Transformerbased models [30]. By examining self-attention patterns in large language models, StreamingLLM [32] observed that LLMs tend to focus disproportionately on initial tokens—a phenomenon termed the _attention sink_ . Preserving the corresponding key–value pairs was shown to enable efficient, infinite-length text processing without additional finetuning. Extending this concept to multimodal architectures, Kang et al. [13] found that large vision-language models often assign high attention weights to visually salient but semantically irrelevant tokens. To mitigate this, they proposed redistributing attention away from such tokens to improve cross-modal alignment and visual grounding. 

In this work, we analyze the attention weights within flow-based VLAs [12, 24], uncovering key insights into how actions attend to other modalities and therefore propose to interpret action self-attention weights as informative cues for estimating the execution horizon. 

## **3. Methodology** 

### **3.1. Preliminary** 

Denote the pretrained diffusion-/flow-based VisionLanguage-Action (VLA) model as _π_ ( **A** _t|_ **o** _t,_ **c** ), where 

**o** _t_ represents the input visual observations at time step _t_ , and **c** denotes the corresponding language command. The policy is trained to predict a sequence of _p_ continuous actions, **A** _t_ = [ **a** _t,_ **a** _t_ +1 _, . . . ,_ **a** _t_ + _p−_ 1 ] _,_ referred to as an _action chunk_ . Here, the parameter _p ∈_ N specifies the **prediction horizon** , _i.e_ ., the temporal window over which the model forecasts future actions conditioned on the current perceptual-linguistic context ( **o** _t,_ **c** ). During execution, the agent typically performs the first _e_ actions from the predicted chunk before re-sampling new input observations and generating the next action chunk, where _e ∈_ N defines the **execution horizon** . 

Attention weights are widely employed to quantify the correspondence between different tokens. Let _Tv_ , _Tl_ , and _Ta_ denote the number of encoded vision, language, and action tokens within the VLA respectively. Within a standard transformer-based attention mechanism, the attention weight matrix **S** is defined as the post-softmax similarity between the query and key embeddings: 


where **Q** _∈_ R<sup>_Ta×d_</sup> represents the queries derived from action tokens, **K** _∈_ R<sup>(</sup><sup>_Tv_+</sup><sup>_Tl_+</sup><sup>_Ta_)</sup><sup>_×d_</sup> denotes the concatenated keys from vision, language, and action tokens, and _d_ is the shared token feature dimension. Each entry **S** _ij_ captures the relative attention weight between the _i_ -th action query and the _j_ -th key token, thus encoding how strongly the policy attends to specific visual regions, linguistic cues, or consecutive actions when generating its action sequence. 

In the following, we first show that flow-matching policy performance exhibits a peaked trend with respect to the execution horizon, underscoring the need and feasibility to identify an optimal value. To explain this phenomenon, we analyze the attention weights and reveal two key phenomena that shape predicted chunk behavior. Building on these insights, we introduce an efficient strategy for execution 

3 


Figure 3. **Visualization of average attention weights in** _π_ 0 _._ 5 **across different stages of task execution.** Intra-chunk actions consistently attend to the same vision and language tokens across predicted chunks throughout the rollout. This invariance is consistently observed across different sampling steps, task rollouts, and pretrained models. The x-axis is rescaled for clarity of visualization. 

horizon estimation. Unless otherwise specified, all analyses are conducted using the state-of-the-art _π_ 0 _._ 5 [12] model. 

### **3.2. Existence of Optimal Execution Horizon** 

Consider an action chunking policy that employs a fixed execution horizon of length _e_ throughout its rollout. Assume the policy executes a total of _L_ low-level actions before task termination. Let _δ_<sup>_c_</sup> denote the loss in final task reward incurred at each chunk transition, assumed to be independent of _e_ . Let _δj_<sup>_d_(</sup><sup>_e_) represent the total divergence loss between</sup> the _j_ -th executed action chunk and its corresponding expert trajectory segment. With _m_ = _⌈L/e⌉_ executed chunks in total, the expected error accumulated over the rollout can be expressed as: 


**Proposition 1** ( _Unique Error Minimizer_ ) **.** _Suppose δj_<sup>_d_(</sup><sup>_e_)</sup><sup>_is_</sup> _a monotonically increasing function with respect to e and can be modeled as δj_<sup>_d_(</sup><sup>_e_) =</sup><sup>_ke_log</sup><sup>_e, where k>_0</sup><sup>_is a scal-_</sup> _ing factor. Denote p as the prediction horizon. Assuming L is divisible by e, there exists a unique minimizer of L_ ( _e_ ) _:_ 


_such that L_ ( _e_ ) _is strictly decreasing on_ (0 _, e_<sup>_∗_</sup> ) _and strictly increasing on_ ( _e_<sup>_∗_</sup> _, ∞_ ) _._ 

Proof is provided in Sec. 6. Eq. (3) indicates that when the policy is trained on a diverse set of the underlying action distributions and the chunk transition loss _δ_<sup>_c_</sup> is large, a longer execution horizon is preferred to promote temporally consistent action sequences. Conversely, when the policy struggles to accurately model the implicit environment dynamics and the intra-chunk divergence loss _δ_<sup>_d_</sup> ( _e_ ) dominates, a shorter execution horizon becomes more favorable, enhancing reactivity to environmental changes. Our analysis can be viewed as an extension of Liu et al. [21]. By 

modeling the total policy rollout error, we demonstrate that an optimal execution horizon exists and that performance monotonically decreases as the horizon deviates from this optimum, thereby establishing an _explicit_ trade-off between long-term consistency and short-term reactivity. Note that Eq. 3 serves only as a theoretical proof of existence and does not directly guide method design. 

Empirically, we also observe the characteristic relationship between policy performance and execution horizon. As shown in Fig. 1, varying the execution horizon leads to substantial performance deviations, underscoring the importance of selecting an appropriate value of _e_ . Across all evaluated tasks, the behavior of the policy performance aligns with our theoretical findings: the success rate initially increases and then declines as _e_ grows, peaking at an intermediate value. This indicates that optimal performance arises from balancing consistency with reactivity. Fig. 7 further illustrates the case with a smaller prediction horizon ( _p_ = 10). In this constrained setting, the best performance typically occurs at the horizon boundary, i.e., _e_<sup>_∗_</sup> = _p_ . This behavior arises because the policy is well-trained under a small _p_ , allowing it to accurately capture the implicit environment dynamics. As a result, the predicted trajectories closely match the expert demonstrations, leading to _k →_ 0. However, once the execution horizon exceeds the prediction horizon ( _e > p_ ), a pronounced performance drop emerges. We attribute this to a train–test mismatch, since the model has not been trained on trajectories longer than _p_ . 

### **3.3. VLA Knows Its Limits** 

To uncover the underlying causes of the observed performance pattern, we analyze the model’s attention weights to examine how the VLA allocates focus across vision, language, and action tokens during action generation. By interpreting these attention distributions, we identify two key phenomena that jointly explain the empirical patterns reported in Sec. 3.2 and shed light on how attention dynamics reflect the VLA’s intrinsic predictive limits. ❶ **Intra-chunk actions attend invariantly to vi-** 

4 


Figure 4. **Visualization of normalized action self-attention weights.** Across different prediction horizons, the predicted actions exhibit strong attention to the initial and terminal action tokens, with correspondence strength remaining high before sharply decaying as temporal distance increases. These boundary tokens (encircled in black) are referred to as _radial action sinks_ . 

**sion–language tokens.** We visualize the cross-attention maps of the last sampling step from the _π_ 0 _._ 5 model ( _p_ = 50) in Fig. 3. Each row in the heatmap represents the attention distribution between action queries and the concatenated sequence of vision, language, and action keys. The first 768 tokens correspond to visual input, followed by 200 language tokens, and the remaining correspond to action tokens. Column widths are rescaled for improved clarity. 

From the figure, we observe a striking invariance: actions within the same chunk consistently attend to the same vision–language tokens with nearly identical importance. This suggests that, although the model predicts a temporally extended sequence of future actions, later actions fail to adaptively adjust to environmental changes. Instead, they repeatedly rely on static visual–linguistic features that are informative for early actions but increasingly outdated or misleading for later ones. Consequently, executing these later actions may become redundant or even detrimental, contributing little new contextual information and corrective flexibility. This property manifests as overconfident policy rollouts with reduced reactivity and adaptability. 

We also observe an unusually high concentration of attention on the _first language token_ , a phenomenon that persists across all transformer blocks and sampling steps. This pattern resembles the attention sink effect reported in large language models [32]. However, unlike in LLMs, where sink tokens often encode structural or positional information, the language attention sink in VLAs appears largely redundant and carries minimal semantic value. Empirically, masking all language tokens (by setting their attention weights to zero) may results in only a marginal drop in task success rate (Sec. 8.5). We infer that, due to the strong vision–language pretraining of the backbone model, most linguistic semantics are already embedded within the visual representations during action generation, making explicit linguistic attention largely superfluous. 

❷ **Radial action sinks emerge at the sequence boundaries.** In Fig. 4, we visualize the normalized self-attention maps among action tokens under varying prediction horizons. A consistent pattern emerges: strong attention is con- 

centrated on both the initial and terminal action tokens. The correspondence strength remains high for a short span, then rapidly decays over a few actions before stabilizing into a low-attention plateau. We refer to these highly attended boundary tokens as **radial action sinks** . 

Why do flow-based VLAs consistently concentrate attention at the beginning and end of each predicted chunk? We infer two underlying reasons. First, the initial action tends to exhibit the lowest cumulative error and thus serves as a stable anchor for subsequent actions. Later actions follow this anchor’s guidance while gradually attending more to adjacent tokens, resulting in smooth and temporally consistent trajectories. Second, because the policies are trained on expert demonstrations with randomly sampled starting timestamps, both the initial and terminal actions play a role in preserving inter-chunk continuity, reflecting the model’s implicit objective to ensure smooth transitions across chunk boundaries. Together, these radial action sinks establish an attention structure in which the initial and terminal tokens define latent centers around which intermediate actions are organized, revealing an intrinsic bias in the model’s temporal reasoning process. 

**Action self-attention as an indicator of predictive limit.** Building on these two observations, we conclude that intra-chunk actions exhibit limited adaptability and attend strongly to radial action sinks. Therefore, we _pose to interpret the action self-attention weights as implicit indicators of the model’s predictive limit_ . Specifically, when the selfattention weights associated with the radial action sinks remain high, the model is confident that its predicted actions are still aligned with the guiding anchors and thus valid under the current observation. In contrast, as these attention weights decline, the model increasingly conditions on its own previously generated actions rather than grounded sensory inputs. This shift toward self-referential dependence amplifies compounding errors and ultimately degrades reactivity and performance during extended rollouts. 

### **3.4. AutoHorizon** 

Motivated by the above analysis, we propose leveraging attention weights as a proxy to estimate the execution horizon for _each_ action chunk. Adopting a per-chunk horizon is intuitive: as task difficulty and environmental dynamics fluctuate throughout the policy rollout, the optimal execution horizon should adapt correspondingly to maintain an effective balance between temporal consistency and reactivity. 

To this end, we introduce **AutoHorizon** —a dataadaptive approach that estimates execution horizons directly from the model’s intrinsic attention dynamics. Given the attention weights obtained at each sampling step _t_ , we first extract the action self-attention maps and average them across all transformer blocks and attention heads, followed by row-wise normalization to ensure that each query–key 

5 

Table 1. **Performance comparison of** _π_ 0 _._ 5 **on LIBERO benchmark under different prediction horizons.** Best results are in **bold** . 

|Se|tting||_p_=|10|||_p_=|50||
|---|---|---|---|---|---|---|---|---|---|
|Tas|k Suite|LIB-Spatial|LIB-Object|LIB-Goal|LIB-10|LIB-Spatial|LIB-Object|LIB-Goal|LIB-10|
||_e_= 0_._2_p_|98.5_±_0.5|94.1_±_1.0|90.4_±_0.0|76.0_±_1.2|94.9_±_0.2|97.1_±_0.2|92.7_±_1.0|91.2_±_2.3|
||_e_= 0_._4_p_|98.9_±_0.4|98.1_±_0.5|94.8_±_0.9|82.8_±_1.5|92.4_±_0.3|94.1_±_1.9|90.9_±_0.7|88.7_±_0.8|
|Static<br>|_e_= 0_._6_p_|98.8_±_0.3|98.7_±_0.7|95.2_±_0.7|85.9_±_0.8|87.1_±_1.9|91.5_±_2.5|86.0_±_3.3|82.4_±_2.0|
|Oracle|_e_= 0_._8_p_|98.9_±_0.4|99.1_±_0.5|95.1_±_1.1|88.5_±_1.5|81.2_±_2.7|88.9_±_1.6|78.4_±_2.0|76.3_±_2.5|
||_e_= 1_._0_p_|99.1_±_0.5|98.8_±_0.9|97.2_±_1.0|90.4_±_0.6|71.5_±_1.3|67.9_±_0.9|74.5_±_2.7|68.6_±_1.2|
|Static|Oracle+|99.1_±_0.5|99.1_±_0.5|97.2_±_1.0|90.4_±_0.6|96.4_±_0.3|97.6_±_0.6|93.9_±_0.5|91.9_±_0.4|
|Ra|ndom|98.4_±_1.2|98.4_±_0.7|96.3_±_0.7|86.3_±_1.5|82.8_±_1.5|90.3_±_1.6|85.3_±_2.3|83.3_±_0.7|
|**Auto**|**Horizon**|**99.1**_±_**0.2**|**99.2**_±_**0.3**|**97.5**_±_**0.2**|**91.6**_±_**0.7**|**96.5**_±_**0.9**|**98.0**_±_**0.6**|**94.4**_±_**1.0**|**92.1**_±_**1.0**|


distribution sums to one. The resulting normalized attention matrix is denoted as **S** _t ∈_ R<sup>_p×p_</sup> _,_ where _p_ is the prediction horizon, and notations are reused from Eq. (1) for simplicity. Intuitively, **S** _t_ [ _i, j_ ] quantifies how strongly the _i_ -th query action attends to the _j_ -th key action, revealing how far the model effectively “looks ahead.” Our objective is to identify the first turning point in the attention trajectory—where the attention mass stops advancing and begins to plateau—which marks the natural boundary of the VLA’s predictive limit, ensuring that all executed actions remain reliable while maximizing temporal consistency. 

To estimate this turning point, we first retain only the rows of **S** _t_ that exhibit low entropy, defined as 


where 


and _Qq_ denotes the _q_ -quantile of the entropy distribution across rows. This filtering step removes actions with uniformly diffused attention, preserving those with sharper, more confident patterns that provide reliable structural cues. 

Next, we employ a bidirectional soft-pointer mechanism to locate the plateau. Two pointers, _qs_ = 0 and _qe_ = _p −_ 1, are initialized at the start and end of the chunk, respectively. For the forward pointer _qs_ , the expected predictive horizon for each row _i_ is computed as 


where the non-decreasing constraint enforces monotonic progression and prevents backward jumps. We then compute the incremental change ∆ _µt_ [ _i_ ] = _µt_ [ _i_ ] _− µt_ [ _i −_ 1], which tracks the evolution of the attention trajectory. A large ∆ _µt_ [ _i_ ] indicates a sudden shift in attention focus, signaling the onset of a plateau. The set of actions preceding 

this plateau is defined as 


where _τ_ is a fixed threshold. At sampling step _t_ , the forward execution horizon is then determined as 


The same procedure is applied to the reversed attention matrix **S**<sup>˜</sup> _t_ to obtain the backward horizon _Nb_ . If the combined coverage satisfies _Nf_ + _Nb ≥ p_ , a full-range coverage is adopted ( _N_ = _p_ ); otherwise, only the forward prefix length is used as the effective execution horizon ( _N_ = _Nf_ ). Empirically, we find that the former case typically occurs when the prediction horizon _p_ is small, whereas the latter dominates for larger _p_ . A concrete example illustrating the full procedure is shown in Fig. 6. 

## **4. Experiments** 

### **4.1. Experimental Settings** 

**Models.** We evaluate our method on two representative flow-based Vision–Language–Action models: _π_ 0 _._ 5 [12] and GR00T N1.5 [24]. For _π_ 0 _._ 5, we conduct experiments with two variants using prediction horizons of _p_ = 10 and _p_ = 50 to examine horizon-dependent behavior. For GR00T N1.5, we adopt the publicly released pretrained checkpoints with the default prediction horizon of _p_ = 16. AutoHorizon operates on the first or third sampling step and typically uses fixed hyperparameters of _q_ = 0 _._ 9 and _τ_ = 0 _._ 3, requiring no additional parameter tuning. **Baselines.** We compare against the following baselines: 

- **Static Oracle.** This corresponds to the conventional setting in action chunking policies, where a fixed execution horizon is maintained throughout rollout. Execution horizons are uniformly sampled for full range coverage. 

- **Static Oracle+.** An enhanced version of Static Oracle that performs brute-force search over the prediction horizon, thereby achieving optimal performance under fixed horizon settings. It serves as a strong yet costly baseline, as it requires _p_ rollouts per task. 

6 

Table 2. **Performance comparison using GR00T N1.5 on the LIBERO benchmark.** Best results are highlighted in **bold** . 

|Task|Suite|LIB-Spatial|LIB-Object|LIB-Goal|LIB-10|
|---|---|---|---|---|---|
||_e_= 1|92.7_±_0.9|94.7_±_3.4|82.7_±_0.9|74.7_±_3.4|
|Stti|_e_= 2|96.0_±_1.6|95.3_±_3.8|82.0_±_1.6|83.3_±_0.9|
|ac<br>Ol|_e_= 4|94.7_±_3.4|95.3_±_2.5|90.7_±_0.9|88.7_±_1.9|
|race|_e_= 8|95.3_±_0.9|97.3_±_0.9|94.7_±_3.4|86.0_±_5.9|
||_e_= 12|91.3_±_2.5|96.0_±_0.0|90.0_±_0.0|86.0_±_4.3|
||_e_= 16|94.0_±_3.3|94.7_±_0.9|90.7_±_0.9|90.0_±_1.6|
|Static|Oracle+|96.0_±_1.6|97.3_±_0.9|94.7_±_3.4|90.0_±_1.6|
|Ran|dom|93.3_±_0.9|96.0_±_2.8|92.0_±_1.6|88.7_±_1.9|
|**AutoH**|**orizon**|**96.7**_±_**0.9**|**98.7**_±_**1.8**|**96.0**_±_**1.6**|**92.7**_±_**2.5**|


- **Random:** To assess the effect of adaptive horizon selection, we include a stochastic baseline where the execution horizon is randomly sampled at each rollout step, following _e ∼U_ (1 _, p_ ). This baseline isolates the contribution of structured, attention-guided adaptation from performance variations arising purely from random horizon changes. 

- For all experiments, we report both the mean and standard deviation to ensure fair comparison and robust evaluation. We also compare against two adaptive re-planning baselines, Action Trigger and Uncertainty Proxy, in Sec. 8. Although these baselines are not central to the focus of this paper, we include them to further demonstrate the effectiveness of AutoHorizon. 

### **4.2. Simulation Results** 

We evaluate AutoHorizon in simulated robotic manipulation environments that require both short- and long-horizon decision making. Our experiments leverage two benchmark datasets: the LIBERO dataset [20], which offers a diverse suite of single-arm manipulation tasks, and the RoboTwin dataset [7, 23], which focuses on bimanual coordination tasks. For LIBERO, we include four subsets— _LIBEROSpatial_ , _LIBERO-Goal_ , _LIBERO-Object_ , and _LIBERO10_ —and perform 25 independent rollouts per task. For RoboTwin, we evaluate on seven manipulation tasks: _adjust bottle position_ , _pick dual bottles_ , _place container onto plate_ , _stack two bowls_ , _place empty cup on coaster_ , _open laptop_ , and _press stapler_ . Each task is executed for 100 trials. All experiments are repeated three times to account for stochasticity in action sampling and environment initialization, ensuring statistical robustness. 

**LIBERO Benchmark.** Tab. 1 reports the results of _π_ 0 _._ 5 on the LIBERO benchmark. Under a small prediction horizon ( _p_ = 10), the optimal execution horizon for the _Static Oracle_ baseline typically appears at the upper bound of valid values. The _Random_ baseline also performs relatively well, suggesting that models trained with short prediction horizons tend to overfit and accurately capture short trajectory segments. When the prediction horizon increases to _p_ = 50, we observe a significantly different behavior. The performance of _Static Oracle_ first rises and then declines 


Figure 5. **Estimated execution horizon distributions by AutoHorizon.** The legend displays the mean values of the distributions. 

as the execution horizon extends, while the _Random_ baseline suffers a pronounced drop in performance. In many cases, suboptimal horizon choices even cause _Static Oracle_ to underperform the _Random_ baseline, underscoring the importance of selecting an appropriate execution horizon. The enhanced _Static Oracle+_ consistently achieves strong results, and the specific horizon values used for this baseline are listed in Sec. 8.2. Across both horizon configurations, AutoHorizon consistently outperforms all baselines. We attribute this improvement to its ability to dynamically adapt execution horizons during rollout, effectively balancing long-term consistency with short-term reactivity. 

We further evaluate AutoHorizon on the LIBERO benchmark using GR00T N1.5 [24], which differs from _π_ 0 _._ 5 in both architectural design and training pipeline. As shown in Tab. 2, although the precise performance trends vary, _Static Oracle_ again exhibits a characteristic peak followed by degradation as the execution horizon increases. Our method consistently achieves superior results, demonstrating robustness and generalization across different architectures and training regimes. In Sec. 9, we also visualize the attention weight distributions for GR00T N1.5, which yield conclusions consistent with our earlier analysis. 

**RoboTwin Benchmark.** Tab. 3 presents the results on the RoboTwin benchmark across tasks with varying difficulty. For both tasks that are highly sensitive ( _pick bottles_ ) and those that are relatively insensitive ( _stack bowls_ ) to the choice of execution horizon, our method achieves comparable or superior performance to the baselines, demonstrating its adaptability across diverse task dynamics. 

**Ablation.** Fig. 5 visualizes the value distribution of execution horizons estimated by AutoHorizon across the four LIBERO task suites. AutoHorizon yields a broad range of horizon lengths during rollout, demonstrating adaptability to diverse input conditions and capturing the frequent shifts in VLA’s prediction dynamics. Most estimated horizons fall within moderately low values—favoring reactivity—while occasional larger horizons facilitate faster task 

7 

Table 3. **Performance comparison using** _π_ 0 _._ 5 **on the RoboTwin tasks.** Best results are highlighted in **bold** . 

|Tas|k Suite|Adjust Bottle|Pick Bottles|Place Container|Stack Bowls|Place Cup|Open Laptop|Press Stapler|
|---|---|---|---|---|---|---|---|---|
||_e_= 0_._2_p_|79.0_±_1.4|40.7_±_0.5|84.0_±_2.8|90.7_±_1.2|83.7_±_0.9|68.3_±_1.9|44.0_±_0.0|
|Static|_e_= 0_._4_p_|89.0_±_0.0|67.0_±_0.0|83.0_±_0.0|87.3_±_1.7|77.7_±_2.5|78.3_±_0.5|48.0_±_0.0|
|Ol|_e_= 0_._6_p_|89.3_±_0.9|65.0_±_0.0|82.0_±_0.0|86.7_±_2.5|68.3_±_0.5|71.7_±_2.1|67.0_±_0.0|
|race|_e_= 0_._8_p_|76.7_±_1.2|58.0_±_1.4|81.0_±_0.0|90.0_±_2.8|66.0_±_1.6|78.7_±_0.5|70.0_±_0.0|
||_e_= 1_._0_p_|58.7_±_1.2|30.0_±_0.0|76.7_±_0.5|87.7_±_1.2|56.3_±_3.8|84.0_±_0.0|71.0_±_0.0|
|Static|Oracle+|98.7_±_0.5|67.0_±_0.0|91.0_±_0.8|90.7_±_1.2|83.7_±_0.9|84.0_±_0.0|72.0_±_0.0|
|Ra|ndom|85.3_±_0.5|60.0_±_0.0|86.0_±_0.0|88.7_±_3.4|70.7_±_2.5|82.0_±_0.0|69.0_±_0.0|
|**Auto**|**Horizon**|**100.0**_±_**0.0**|**68.0**_±_**0.0**|**91.0**_±_**0.8**|**92.0**_±_**0.8**|**85.3**_±_**2.1**|**84.7**_±_**0.9**|**75.0**_±_**0.0**|


completion when long-term consistency is beneficial. We further compare with a variation of _Static Oracle_ using fixed horizons closest to AutoHorizon’s mean estimated values ( _e.g_ ., _e_ = 14 and _e_ = 15 for LIBERO-10) in Sec. 8, and find that AutoHorizon consistently achieves higher success rates. These results confirm the effectiveness of dynamic horizon adjustment over fixed-horizon strategies. 

We also examine the effect of hyperparameters in Sec. 8.7. The results show that AutoHorizon’s performance remains stable across different combinations of parameter settings. Compared with the strong _Static Oracle+_ baseline, it always achieves comparable or even superior results, demonstrating robustness to hyperparameter choices. 

### **4.3. Real-World Results** 

**Setup.** We further evaluate AutoHorizon in real-world robotic manipulation scenarios. Experiments are conducted on a Franka Research 3 robot (7-DoF arm) [10] following the DROID experimental setup [15]. The backbone VLA is _π_ 0 _._ 5, configured with a prediction horizon of _p_ = 50. 

We assess all methods on three single-arm pick-andplace tasks of increasing difficulty: _put cucumber on plate_ , _put Rubik’s cube on plate_ , and _put Rubik’s cube into bowl_ . A total of 150 trajectories are collected for model finetuning. For evaluation, we adopt a stage-based solve rate that measures progress across four phases: (1) reaching the object, (2) grasping and lifting it, (3) moving it toward the target location, and (4) successfully placing it in the container. Each task is evaluated over ten trials per setting, with each trial capped at 300 control steps, amounting to approximately three hours of total robot execution time. Object positions and orientations are randomized across trials to ensure robustness and generalization. 

**Results.** Tab. 4 summarizes the performance across the three tasks. The occasionally large standard deviations arise from the binary nature of the outcomes, where some rollouts successfully complete the task, while others fail entirely. Several key observations emerge from the execution process. When the execution horizon is too short ( _i.e_ ., _e ∈_ [1 _,_ 5]), the robot frequently hesitates or stalls during motion. This behavior stems from the policy’s tendency to 

Table 4. **Performance comparison on real-world tasks.** Best results are highlighted in **bold** . 

|Task|Suite|Cucumber Plate|Cube Plate|Cube Bowl|
|---|---|---|---|---|
||_e_= 5|91.5_±_12.7|0.0_±_0.0|76.0_±_40.7|
|Static|_e_= 10|94.0_±_11.5|81.5_±_35.4|97.5_±_4.2|
|Oracle|_e_= 20|88.0_±_20.3|54.0_±_43.9|89.5_±_17.6|
||_e_= 30|89.0_±_19.0|74.5_±_36.3|87.5_±_17.0|
||_e_= 40|79.0_±_24.5|81.5_±_28.7|56.5_±_31.3|
||_e_= 50|50.0_±_40.8|51.5_±_38.6|58.5_±_34.0|
|Static|Oracle+|97.0_±_7.9|81.5_±_35.4|97.5_±_4.2|
|Ran|dom|88.5_±_14.7|60.5_±_44.1|77.0_±_27.3|
|**AutoH**|**orizon**|**98.0**_±_**4.8**|**92.0**_±_**15.7**|**99.0**_±_**2.1**|


predict subtle, low-amplitude movements for the initial few actions within a chunk, resulting in insufficient overall progression. At moderate horizons ( _e ∈_ [20 _,_ 40]), the robot often overreaches or collides with the workspace, reflecting a loss of reactivity. When the execution horizon becomes excessively long ( _e >_ 40), the robot struggles to maintain accurate object localization, leading to frequent object drops and a diminished ability to correct errors during execution. 

In contrast, AutoHorizon dynamically adjusts the execution horizon throughout the rollout. As shown in Fig. 2, under stable conditions—such as reaching for or transporting the object—the estimated horizons increase, accelerating execution progress. When the robot begins to physically interact with the environment ( _e.g_ ., grasping or placing the cube), the estimated horizons adaptively shorten, enhancing reactivity to environmental changes. 

## **5. Conclusion** 

Determining the execution horizon in action chunking flow policies remains an underexplored yet crucial challenge. In this work, we analyze the predictive behaviors of flowbased VLAs through attention weight inspection. Our analysis reveals that predicted action chunks exhibit limited temporal adaptability and consistently rely on radial action sinks for structural guidance. Building on these insights, we interpret action self-attention weights as implicit indicators of the model’s predictive confidence and 

8 

propose an autonomous, attention-guided execution horizon estimation algorithm that dynamically assigns chunkspecific horizons. Extensive evaluations in both simulated and real-world robotic manipulation tasks demonstrate that our method consistently outperforms other baselines, highlighting its effectiveness and generalizability. 

## **References** 

- [1] Brenna D. Argall, Sonia Chernova, Manuela Veloso, and Brett Browning. A survey of robot learning from demonstration. _Robotics and Autonomous Systems_ , 57(5):469–483, 2009. 1 

- [2] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, Thomas Unterthiner, Daniel Keysers, Skanda Koppula, Fangyu Liu, Adam Grycner, Alexey Gritsenko, Neil Houlsby, Manoj Kumar, Keran Rong, Julian Eisenschlos, Rishabh Kabra, Matthias Bauer, Matko Boˇsnjak, Xi Chen, Matthias Minderer, Paul Voigtlaender, Ioana Bica, Ivana Balazevic, Joan Puigcerver, Pinelopi Papalampidi, Olivier Henaff, Xi Xiong, Radu Soricut, Jeremiah Harmsen, and Xiaohua Zhai. Paligemma: A versatile 3b vlm for transfer, 2024. 2 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. 1, 2, 3 

- [4] Kevin Black, Manuel Y. Galliker, and Sergey Levine. Realtime execution of action chunking flow policies, 2025. 1, 3 

- [5] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, Hanbo Zhang, and Minzhao Zhu. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation, 2024. 2 

- [6] Guo Chen, Zhiqi Li, Shihao Wang, Jindong Jiang, Yicheng Liu, Lidong Lu, De-An Huang, Wonmin Byeon, Matthieu Le, Tuomas Rintamaki, Tyler Poon, Max Ehrlich, Tuomas Rintamaki, Tyler Poon, Tong Lu, Limin Wang, Bryan Catanzaro, Jan Kautz, Andrew Tao, Zhiding Yu, and Guilin Liu. Eagle 2.5: Boosting long-context post-training for frontier vision-language models, 2025. 2 

- [7] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 7 

- [8] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion, 2024. 1, 2, 3 

- [9] Xiangming Gu, Tianyu Pang, Chao Du, Qian Liu, Fengzhuo Zhang, Cunxiao Du, Ye Wang, and Min Lin. When attention sink emerges in language models: An empirical view. _arXiv preprint arXiv:2410.10781_ , 2024. 3 

- [10] Sami Haddadin. The franka emika robot: A standard platform in robotics research. _IEEE Robotics & Automation Magazine_ , 31(4):136–148, 2024. 8 

- [11] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations, 2025. 2 

- [12] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. 1, 2, 3, 4, 6 

- [13] Seil Kang, Jinyeong Kim, Junhyeok Kim, and Seong Jae Hwang. See what you are told: Visual attention sink in large multimodal models, 2025. 3 

- [14] Kento Kawaharazuka, Jihoon Oh, Jun Yamada, Ingmar Posner, and Yuke Zhu. Vision-language-action models for robotics: A review towards real-world applications. _IEEE Access_ , 13:162467–162504, 2025. 1 

- [15] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, Peter David Fagan, Joey Hejna, Masha Itkina, Marion Lepert, Yecheng Jason Ma, Patrick Tree Miller, Jimmy Wu, Suneel Belkhale, Shivin Dass, Huy Ha, Arhan Jain, Abraham Lee, Youngwoon Lee, Marius Memmel, Sungjae Park, Ilija Radosavovic, Kaiyuan Wang, Albert Zhan, Kevin Black, Cheng Chi, Kyle Beltran Hatch, Shan Lin, Jingpei Lu, Jean Mercat, Abdul Rehman, Pannag R Sanketi, Archit Sharma, Cody Simpson, Quan Vuong, Homer Rich Walke, Blake Wulfe, Ted Xiao, Jonathan Heewon Yang, Arefeh Yavary, Tony Z. Zhao, Christopher Agia, Rohan Baijal, Mateo Guaman Castro, Daphne Chen, Qiuyu Chen, Trinity Chung, Jaimyn Drake, Ethan Paul Foster, Jensen Gao, Vitor Guizilini, David Antonio Herrera, Minho Heo, Kyle Hsu, Jiaheng Hu, Muhammad Zubair Irshad, Donovon Jackson, Charlotte Le, Yunshuang Li, Kevin Lin, Roy Lin, Zehan Ma, Abhiram Maddukuri, Suvir Mirchandani, Daniel Morton, Tony Nguyen, Abigail O’Neill, Rosario Scalise, Derick Seale, Victor Son, Stephen Tian, Emi Tran, Andrew E. Wang, Yilin Wu, Annie Xie, Jingyun Yang, Patrick Yin, Yunchu Zhang, Osbert Bastani, Glen Berseth, Jeannette Bohg, Ken Goldberg, Abhinav Gupta, Abhishek Gupta, Dinesh Jayaraman, Joseph J Lim, Jitendra Malik, Roberto Mart´ın-Mart´ın, Subramanian Ramamoorthy, Dorsa Sadigh, Shuran Song, Jiajun Wu, Michael C. Yip, Yuke Zhu, Thomas Kollar, Sergey Levine, and Chelsea Finn. 

9 

Droid: A large-scale in-the-wild robot manipulation dataset, 2025. 8 

- [16] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An opensource vision-language-action model, 2024. 1, 2 

- [17] Lucy Lai, Ann Zixiang Huang, and Samuel J Gershman. Action chunking as policy compression. _PsyArXiv_ , 2022. 1 

- [18] Chengmeng Li, Junjie Wen, Yan Peng, Yaxin Peng, Feifei Feng, and Yichen Zhu. Pointvla: Injecting the 3d world into vision-language-action models. _arXiv preprint arXiv:2503.07511_ , 2025. 2 

- [19] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model, 2025. 1, 2 

- [20] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning, 2023. 7 

- [21] Yuejiang Liu, Jubayer Ibn Hamid, Annie Xie, Yoonho Lee, Max Du, and Chelsea Finn. Bidirectional decoding: Improving action chunking via closed-loop resampling. _International Conference on Learning Representations (ICLR)_ , 2025. 1, 2, 4 

- [22] Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on vision-language-action models for embodied ai, 2025. 1 

- [23] Yao Mu, Tianxing Chen, Zanxin Chen, Shijia Peng, Zhiqian Lan, Zeyu Gao, Zhixuan Liang, Qiaojun Yu, Yude Zou, Mingkun Xu, Lunkai Lin, Zhiqiang Xie, Mingyu Ding, and Ping Luo. Robotwin: Dual-arm robot benchmark with generative digital twins. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , pages 27649– 27660, 2025. 7 

- [24] NVIDIA, :, Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi ”Jim” Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. 1, 2, 3, 6, 7 

- [25] OpenAI. Gpt-4 technical report, 2024. 2 

- [26] Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, Adrian Li-Bell, Danny Driess, Lachy Groom, Sergey Levine, and Chelsea Finn. Hi robot: Open-ended instruction following with hierarchical vision-language-action models, 2025. 1 

- [27] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and Remi Ca- 

dene. Smolvla: A vision-language-action model for affordable and efficient robotics, 2025. 1, 2, 3 

- [28] Jiaming Song, Arash Vahdat, Morteza Mardani, and Jan Kautz. Pseudoinverse-guided diffusion models for inverse problems. In _International Conference on Learning Representations_ , 2023. 3 

- [29] Gemini Team. Gemini: A family of highly capable multimodal models, 2025. 2 

- [30] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need, 2023. 2, 3 

- [31] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 2 

- [32] Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. Efficient streaming language models with attention sinks, 2024. 3, 5 

- [33] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao Ge, Haoran Wei, Huan Lin, Jialong Tang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jing Zhou, Jingren Zhou, Junyang Lin, Kai Dang, Keqin Bao, Kexin Yang, Le Yu, Lianghao Deng, Mei Li, Mingfeng Xue, Mingze Li, Pei Zhang, Peng Wang, Qin Zhu, Rui Men, Ruize Gao, Shixuan Liu, Shuang Luo, Tianhao Li, Tianyi Tang, Wenbiao Yin, Xingzhang Ren, Xinyu Wang, Xinyu Zhang, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yinger Zhang, Yu Wan, Yuqiong Liu, Zekun Wang, Zeyu Cui, Zhenru Zhang, Zhipeng Zhou, and Zihan Qiu. Qwen3 technical report, 2025. 2 

- [34] Maryam Zare, Parham M. Kebria, Abbas Khosravi, and Saeid Nahavandi. A survey of imitation learning: Algorithms, recent developments, and challenges, 2023. 1 

- [35] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations, 2024. 1, 2 

- [36] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, Fan Lu, He Wang, et al. Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge. _arXiv preprint arXiv:2507.04447_ , 2025. 2 

- [37] Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong Chen, Lianmin Zheng, Ruisi Cai, Zhao Song, Yuandong Tian, Christopher R´e, Clark Barrett, Zhangyang Wang, and Beidi Chen. H2o: Heavy-hitter oracle for efficient generative inference of large language models, 2023. 3 

- [38] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 2 

- [39] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea 

10 

Finn. Learning fine-grained bimanual manipulation with low-cost hardware, 2023. 1, 2, 3 

- [40] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 1, 2 

- [41] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, Zhangwei Gao, Erfei Cui, Xuehui Wang, Yue Cao, Yangzhou Liu, Xingguang Wei, Hongjie Zhang, Haomin Wang, Weiye Xu, Hao Li, Jiahao Wang, Nianchen Deng, Songze Li, Yinan He, Tan Jiang, Jiapeng Luo, Yi Wang, Conghui He, Botian Shi, Xingcheng Zhang, Wenqi Shao, Junjun He, Yingtong Xiong, Wenwen Qu, Peng Sun, Penglong Jiao, Han Lv, Lijun Wu, Kaipeng Zhang, Huipeng Deng, Jiaye Ge, Kai Chen, Limin Wang, Min Dou, Lewei Lu, Xizhou Zhu, Tong Lu, Dahua Lin, Yu Qiao, Jifeng Dai, and Wenhai Wang. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models, 2025. 2 

- [42] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Proceedings of The 7th Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 2 

11 

# **VLA Knows Its Limits: Adaptive Execution Horizons for Robot Policies** 

# Supplementary Material 

## **6. Proof of Proposition 1** 

Under the assumptions of Proposition 1, let _L_ be divisible by _e_ (for simplicity), and let _δj_<sup>_d_(</sup><sup>_e_)=</sup><sup>_k e_log</sup><sup>_e_with</sup><sup>_k>_0</sup> (independent of _j_ ). If _m_ = _L/e_ denotes the number of executed chunks, then there are _m −_ 1 chunk transitions. Hence, from Eq. (2) the total loss can be written as 


Treating _e >_ 0 as a continuous variable, differentiate: 


The unique stationary point is at ˆ _e_ = _δ_<sup>_c_</sup> _/k_ . Moreover, 


so _L_ ( _e_ ) is strictly decreasing on (0 _,_ ˆ _e_ ) and strictly increasing on (ˆ _e, ∞_ ), hence _e_ ˆ is the unique global minimizer in the continuous domain. (Thus _L_ is _unimodal_ ; it need not be globally convex.) 

Since _e ∈_ N (and, in practice, 1 _≤ e ≤ p_ ), the discrete minimizer lies among the two integers nearest to ˆ _e_ : 


Equivalently, without the upper bound _p_ , 


choosing the value that yields the smaller _L_ ( _e_ ). Finally, since lim _e→∞ L_ ( _e_ ) = + _∞_ and _L_ is unimodal, this discrete minimizer is global. 

## **7. Method Demonstration** 

We provide an algorithm demonstration in Alg. 1, detailing the proposed method. Also, Fig. 6 illustrates AutoHorizon on a toy example rollout, clarifying the steps for estimating the per-chunk execution horizon: row-wise normalization, low-entropy row selection, forward soft-pointer plateau detection (the backward pointer is not shown), and horizon fusion. 

#### **Algorithm 1** AutoHorizon 

- **Input:** Attention matrix **S** _t_ and its reverse **S**<sup>˜</sup> _t_ at time _t_ , quantile _q_ , threshold _τ_ 

- 1: Obtain row entropy _Ht_ with Eq. (5) 

- 2: Retain low-entropy rows with Eq. (4) 

   - // **Forward traversal** 

- 3: Compute _µt_ with Eq. (6) 

- 4: ∆ _µt ←_ diff( _µt_ ) 

- 5: _Pt ←{ i |_ ∆ _µt_ [ _i_ ] _< τ }_ 

- 6: _Nf ←⌊µt_ [min( _Rt ∩ Pt_ )] _⌋_ + 1 

   - // **Backward traversal** 

- 7: Apply step 3-6 to **S**<sup>˜</sup> _t_ 

- 8: Obtain backward horizon _Nb_ // **Horizon determination** 

- 9: **if** _Nf_ + _Nb ≥ p_ **then** _N ← p_ **else** _N ← Nf_ 

- **Output:** _N_ 


Figure 6. **Example demonstration of how AutoHorizon works.** 

## **8. Additional Results** 

### **8.1. More Baselines** 

We further include two re-planning baselines for comparison, including: 

- **Action Trigger:** Based on the action chunk distribution, it sets the execution horizon as the first index where the difference between consecutive actions exceeds _τa_ . 

- **Uncertainty Proxy:** It samples 4 chunks per observation and estimates per-step uncertainty via Monte Carlo variance, calculating the horizon as the earliest step where uncertainty exceeds the threshold of _τu_ . The executed ac- 

1 

tions are obtained by averaging sampled chunks. Tab. 5 shows the results. AutoHorizon consistently outperforms these two baselines over various threshold settings. We also observe that these two baselines are very sensitive to the change of hyper-parameters. Moreover, Uncertainty Proxy incurs much more computation latency as it needs to compute 4 chunks for every observation, hindering its applicability under real-world settings. 

Table 5. Comparison with additional baselines. 

|Task|Suite|LIB-Spatial|LIB-Object|LIB-Goal|LIB-10|Press Stapler|
|---|---|---|---|---|---|---|
||_τa_ = 1_e_<sup>_−_2</sup>|95.2_±_0.3|90.5_±_1.3|84.9_±_2.4|77.7_±_1.1|32.0_±_0.0|
|Action|_τa_ = 5_e_<sup>_−_2</sup>|94.4_±_0.9|94.3_±_1.3|85.3_±_1.5|77.5_±_0.9|58.0_±_0.0|
|Trigger|_τa_ = 1_e_<sup>_−_1</sup>|93.9_±_1.9|88.9_±_2.6|85.7_±_0.9|79.6_±_0.7|60.0_±_0.0|
||_τa_ = 3_e_<sup>_−_1</sup>|79.1_±_0.1|74.9_±_1.9|76.9_±_0.8|74.8_±_0.9|71.0_±_0.0|
||_τu_ = 1_e_<sup>_−_2</sup>|94.9_±_1.1|84.5_±_0.7|84.4_±_0.9|70.3_±_1.1|40.0_±_0.0|
|Uncertainty|_τu_ = 5_e_<sup>_−_2</sup>|94.8_±_0.7|84.8_±_1.6|85.7_±_3.8|68.9_±_2.8|72.0_±_0.0|
|Proxy|_τu_ = 1_e_<sup>_−_1</sup>|94.9_±_0.2|89.5_±_0.8|87.7_±_1.6|79.2_±_1.1|71.0_±_0.0|
||_τu_ = 3_e_<sup>_−_1</sup>|91.5_±_0.5|82.0_±_2.6|87.2_±_1.1|77.6_±_2.0|72.0_±_0.0|
|**Ou**|**rs**|**96.5**_±_**0.9**|**98.0**_±_**0.6**|**94.4**_±_**1.0**|**92.1**_±_**1.0**|**75.0**_±_**0.0**|


### **8.2. Execution Horizons for Static Oracle+** 

Table 6 lists the fixed execution horizons selected for _Static Oracle+_ on the LIBERO benchmark. Note that we do not sweep the entire range of possible values; instead, we perform a targeted grid search over a plausible interval where the optimal static _e_ is likely to lie. 

Table 6. **Execution horizons found by Static Oracle+.** 

|Task Suite|LIB-Spatial|LIB-Object|LIB-Goal|LIB-10|
|---|---|---|---|---|
|_π_0_._5 (_p_= 10)|10|8|10|10|
|_π_0_._5 (_p_= 50)|5|13|15|15|
|GR00T(_p_= 16)|2|8|8|16|


The results show substantial variability across tasks and models: the optimal static execution horizon differs markedly, and no clear, generalizable pattern emerges from final success rates alone. For example, _LIBERO-Spatial_ tends to prefer shorter execution horizons as the prediction horizon increases, whereas _LIBERO-10_ exhibits the opposite trend. 

### **8.3. Comparison with Nearest Static Oracle** 

To assess the benefit of the dynamic horizon strategy, we compare AutoHorizon with _Static Oracle_ baselines whose fixed horizons are the nearest neighbors to the mean horizon estimated by our method, such that: _e ∈{⌊e_<sup>_∗_</sup> _⌋ , ⌊e_<sup>_∗_</sup> _⌋_ + 1 _}_ . Table 7 reports results on the LIBERO benchmark using _π_ 0 _._ 5 with _p_ = 50, and the corresponding mean horizons from our method are shown in Fig. 5. 

Table 7. **Comparison with Nearest Static Oracle on LIBERO.** _m_ indicates the mean of the estimated execution horizon distribution by our method. 

|Task Suite|LIB-Spatial|LIB-Object|LIB-Goal|LIB-10|
|---|---|---|---|---|
|Static Oracle (_e_=|_⌊m⌋_)<br>95.7_±_0.2|97.6_±_0.6|92.4_±_0.0|89.1_±_1.4|
|Static Oracle (_e_=|_⌈m⌉_)<br>95.1_±_0.2|97.2_±_0.0|93.9_±_0.2|91.9_±_0.4|
|**Ours**|**96.5**_±_**0.9**|**98.0**_±_**0.6**|**94.4**_±_**1.0**|**92.1**_±_**1.0**|


Across different task configurations, AutoHorizon achieves higher or comparable success rates relative to the nearest _Static Oracle_ , demonstrating the effectiveness of dynamic horizon estimation. We further observe that the mean execution horizon produced by AutoHorizon closely approximates the optimal static choice, while its occasional selection of larger or smaller horizons enables handling corner cases during long rollouts—an advantage unattainable with a single fixed horizon. 

### **8.4. Performance under Shorter Prediction Horizon** 


Figure 7. **Average success rates on the LIBERO benchmark with a prediction horizon of 10 using** _π_ 0 _._ 5 **.** 

Fig. 7 reports results under a shorter prediction horizon ( _p_ = 10) using _π_ 0 _._ 5. The relationship between performance and execution-horizon persists, with peak performance often attained at the boundary _e_ = _p_ . When _e > p_ , performance drops sharply. We attribute this to a train–test mismatch: the policy is trained on chunks of length at most _p_ and does not generalize to longer horizons. This observation provides a natural upper bound for the execution horizon such that 1 _≤ e ≤ p_ . 

### **8.5. Effect of Language Tokens** 

We investigate the role of language tokens in action generation by analyzing their contribution within the crossattention mechanism of _π_ 0 _._ 5 on the LIBERO benchmark. Although the language tokens exhibit high attention weights, we find that they carry only subtle semantic influence on action prediction. To quantify this effect, we perform ablation studies summarized in Tab. 8. _Original_ denotes using the unaltered attention weights, while _Mask Lang_ indicates fully masking the language tokens’ attention weights (with re-normalization applied to preserve the softmax distribution). 

The results show that masking the language tokens leads to mixed but generally minor performance changes, often resulting in only marginal degradation. This suggests that most linguistic information has been absorbed into the vision tokens during training, rendering explicit language at- 

2 


tention largely redundant at inference time. 

To further examine this redundancy, we apply the Visual Attention Redistribution (VAR) technique proposed by Kang et al. [13], which redistributes a portion of the attention mass from certain tokens to others. Under our case, we redistribute the attention mass from the language tokens to other modalities. We denote this variant as _VARL-p_ , where _p_ represents the fraction of language attention weights redistributed ( _e.g_ ., _VAR-L-0.5_ redistributes 50% of the language attention). This strategy acts as a soft version of language masking, since _Original_ corresponds to _VAR-L-1.0_ . When setting _p_ = 0 _._ 5, performance notably improves—sometimes even surpassing the _Original_ baseline ( _e.g_ ., cases under _p_ = 50, _e_ = 10). This finding indicates that partially redistributing language attention to vision–action tokens can enhance model performance, reinforcing the conclusion that language token attention contains substantial redundancy in pretrained VLAs. 

Table 8. **Effect of language tokens on LIBERO benchmark.** 

|Tas|k Suite|LIB-Spatial|LIB-Object|LIB-Goal|LIB-10|
|---|---|---|---|---|---|
|= 10|Original|99.1_±_0.5|98.8_±_0.9|97.2_±_1.0|90.4_±_0.6|
|_p_ <br>= 10|Mask Lang|97.7_±_0.5|99.5_±_0.5|96.1_±_0.8|91.3_±_1.6|
|_e_|VAR-L-0.5|98.5_±_0.5|99.2_±_0.6|96.9_±_1.0|90.7_±_1.0|
|50|Original|91.2_±_2.3|94.9_±_0.2|97.1_±_0.2|92.7_±_1.0|
|_p_=<br>10|Mask Lang|92.8_±_0.9|93.7_±_0.5|81.7_±_1.5|79.6_±_1.5|
|_e_=|VAR-L-0.5|94.8_±_1.2|96.7_±_0.8|89.6_±_1.6|92.1_±_1.5|


### **8.6. Smoothness Analysis** 

We visualize the robot kinematics over time through calculating the joint velocity norm. Fig. 9 shows that AutoHorizon produces smoother velocity transitions over time, demonstrating its potential of achieving stable and smooth actions with improved performance. 


Figure 9. Smoothness analysis. 

### **8.7. Hyper-parameter Sensitivity** 

To verify the effect of hyper-parameter choices, we conducted experiments using _π_ 0 _._ 5 on LIBERO-10. Tab. 9 shows that AutoHorizon remains stable across variations in attention choice _L_ , entropy quantile _q_ , and threshold _τ_ . During analysis, we fix the other parameters choices for fair comparison. We also provide a brief analysis on the effect of combining different hyper-parameters in Tab. 10, where the model performance remains stable across a wide range of settings. 

Table 9. **Hyper-parameter sensitivity analysis.** 

|_L_= 2<br>89.9_±_1.2|_L_= 3<br>92.1_±_1.0|_L_= 4<br>90.9_±_2.5|_L_= 5<br>_L_= 6<br>89.5_±_1.8<br>90.4_±_1.4|
|---|---|---|---|
|_q_ = 0_._7<br>90.8_±_0.3|_q_ = 0_._8<br>92.0_±_1.4|_q_ = 0_._9<br>92.1_±_1.0|_q_ = 0_._99<br>_q_ = 0_._999<br>91.9_±_1.2<br>91.5_±_2.0|
|_τ_ = 0_._1|_τ_ = 0_._2|_τ_ = 0_._3|_τ_ = 0_._4<br>_τ_ = 0_._5|
|90.9_±_1.0|90.0_±_0.9|92.1_±_1.0|91.7_±_1.0<br>91.6_±_1.4|
|Table 10.|**More ab**|**lations on**|**hyper-parameters.**|
|Params|_q_ = 0|_._8<br>_q_ =|0_._9<br>_q_ = 0_._99|
|_τ_ = 0_._2|90.0_±_|0.9<br>90.5|_±_1.9<br>90.0_±_1.7|
|_τ_ = 0_._3|92.0_±_|1.4<br>92.1|_±_1.0<br>91.9_±_1.2|
|_τ_ = 0_._4|91.7_±_|1.0<br>88.3|_±_0.8<br>90.0_±_2.1|


## **9. Attention Mechanism within GR00T N1.5** 

We further demonstrate that our observations are not limited to _π_ 0 _._ 5 but also generalize to other flow-based VLA models such as GR00T N1.5, which employs a substantially different architecture and training pipeline. Unlike _π_ 0 _._ 5, GR00T N1.5 adopts an alternating modality fusion process: one block performs cross-attention between action and vision–language tokens, followed by another block that applies action self-attention. This alternating pattern repeats multiple times during the forward pass, enabling iterative refinement of multimodal representations. 

In Fig. 8, we visualize the cross-attention maps between generated actions and vision–language tokens over different policy execution steps. The token indices 0–19, 276–282, and 539 to the end correspond to visual input. The visualization reveals that the cross-attention mechanism in GR00T N1.5 exhibits the same invariance pattern observed in _π_ 0 _._ 5—different generated actions consistently attend to the same vision–language tokens. 

3 


Figure 10. **Visualization of normalized action self-attention in GR00T N1.5 over different rollout steps.** 

In Fig. 10, we visualize the action self-attention maps over different rollout steps. GR00T N1.5 likewise displays the radial action sink phenomenon, where the initial and terminal action tokens receive disproportionately high attention weights. This consistent structural bias across models reinforces our interpretation that radial action sinks act as implicit indicators of the model’s predictive limits and can therefore inform execution horizon estimation. 

4 

