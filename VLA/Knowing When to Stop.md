---
title: "Knowing When to Stop: Adaptive Action Chunking via Internal Cross-Attention Dynamics in VLAs"
date: "2026-09-01"
authors: "Runze Xu; Xiaolong Shan; Shuang Dai; Yu Wang; Jincheng Yu"
url: https://arxiv.org/abs/2609.00908
pdf: https://arxiv.org/pdf/2609.00908
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.00908)** / [論文ページ](https://arxiv.org/abs/2609.00908)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Knowing When to Stop: Adaptive Action Chunking via Internal Cross-Attention Dynamics in VLAs** 

Runze Xu<sup>1</sup> , Xiaolong Shan<sup>1</sup> , Shuang Dai<sup>1</sup> , Yu Wang<sup>1</sup> , and Jincheng Yu<sup>1</sup> 

**_Abstract_ — Action chunking is a standard execution strategy in modern Vision-Language-Action (VLA) frameworks, but fixed execution horizons impose a trade-off between efficiency and accuracy. Short chunks require frequent inference and may cause oscillatory behavior, whereas long chunks can become misaligned with newly observed states. We address this limitation with an adaptive action chunking approach based on internal cross-attention dynamics in the action expert. We observe that, as the prediction horizon extends, action-toobservation cross-attention becomes increasingly dispersed and its entropy rises toward a plateau. This pattern is associated with higher action prediction error and provides an online signal that the current observation offers limited grounding for further open-loop execution. Based on this observation, we introduce a training-free truncation mechanism that detects sustained high-entropy plateaus and dynamically selects the execution horizon during inference. The method uses attention weights already computed by the policy and introduces negligible additional overhead. Evaluations on** _π_ 0 _._ 5 **and X- VLA across RoboTwin 2.0, LIBERO, and three real-world manipulation tasks show improved average task success over fixed-horizon and adaptive chunking baselines, while preserving efficient closed-loop control. These results show that crossattention dynamics can provide a practical internal signal for adaptive action execution in VLAs.** 

## I. INTRODUCTION 

Vision-Language-Action (VLA) models have demonstrated significant success in robotic manipulation by integrating large-scale multimodal pre-training with physical execution [1]–[9]. These models typically combine a VisionLanguage Model (VLM) backbone for high-level reasoning with a specialized action expert for fine-grained control. To capture multimodal trajectory distributions, action experts often employ generative denoising techniques such as diffusion [10]–[12] or flow matching [13], [14]. Conditioned on VLM hidden states, these experts sample continuous action sequences representing future trajectories rather than isolated points. 

This serialized output paradigm effectively utilizes action chunking, a concept introduced by ALOHA [15] to address the challenges of error accumulation and temporal interference in imitation learning. In single-step regimes (Fig. 1a), minor deviations in predicted actions accumulate over successive steps, leading to large divergence. Additionally, single-step policies often fail to capture temporal logic within training trajectories such as varying rhythms. In contrast, using action chunks (Fig. 1b) as the primary units of prediction and execution suppresses error propagation by reducing replanning frequency and improves the modeling 


Fig. 1: **Different action execution paradigms.** The model receives observation _O_<sup>_t_</sup> and predicts a sequence of actions _{a_<sup>_t_</sup> _j_<sup>_}_overapredictedhorizon</sup><sup>_Hp_.(a)Singlestep:Predicts</sup> and executes one action per observation. (b) Fixed Action Chunking: Executes a fixed number of actions from the predicted horizon. (c) Adaptive Action Chunking: Dynamically adjusts the execution horizon to balance reactivity and efficiency. 

of complex temporal patterns. During inference, the model generates an action sequence over a temporal window _Hp_ , termed the predicted horizon. To maintain reactivity to environmental changes, the robot typically executes only the first _He_ steps, defined as the execution horizon [16]. 

However, fixed execution horizons necessitate a trade-off between precision and efficiency [17]–[20]. Short horizons increase computational costs through frequent inference and may induce oscillatory behaviors. Conversely, excessively long horizons misalign execution with real-time observations; as visual feedback relevance decays, predictive accuracy collapses [21], [22]. Furthermore, optimal horizons vary both across tasks and within single-task stages, such as transitioning from rapid approach to fine-grained manipulation [18]. Current reliance on manual tuning or static heuristics [2], [5] thus limits VLA generalization in diverse scenarios. 

To address the limitations of fixed horizons, we examine the internal attention allocation of action experts (Fig. 2), focusing on cross-attention from action queries to VLM tokens. Across the predicted horizon, we observe a systematic change in this distribution. Early action tokens attend sparsely to a small set of perceptual and linguistic features, whereas later tokens distribute their attention over a broader context. The corresponding entropy typically rises with the action index and may eventually enter a high-value saturation regime. Empirically, sustained high entropy indicates reduced concentration on the current perceptual context and is associated with elevated offline action error. It therefore provides a practical proxy for identifying predictions that are at greater risk of becoming weakly grounded in the current observation. Based on this insight, we propose an adaptive truncation mechanism. This mechanism monitors 

> 1Tsinghua University 


Fig. 2: **Method Overview.** Our framework dynamically determines𝒆 **𝒆 𝒆 𝒆 𝒆** action **𝒆** chunk sizes by monitoring the cross-attention entropy within the action expert. Conditioned on VLM states, the action expert identifies chunk boundaries by monitoring attention focus. This enables adaptive execution across task stages. 

cross-attention entropy during inference and dynamically determines the execution horizon _He_ when the entropy reaches its plateau. This approach establishes a dynamic closed loop between perception and action with near-zero computational overhead. 

The primary contributions of this work are three-fold. (1) We characterize the horizon-wise dispersion of actionto-VLM attention in flow-based VLA policies and show that sustained high-entropy saturation is associated with increased offline action error, supporting its use as an empirical indicator of reduced perceptual grounding and elevated prediction risk. (2) Based on these findings, we design a training-free dynamic truncation mechanism that adaptively adjusts the execution horizon during inference without requiring architectural modifications. (3) Extensive evaluations across multiple state-of-the-art VLA models in both simulated and real-world environments demonstrate that our method achieves higher average success rates than the evaluated fixed-horizon baselines and adaptive baselines, while incurring little additional inference latency. 

## II. RELATED WORK 

## _A. Vision-Language-Action (VLA) Models_ 

VLA architectures combine visual observations, language instructions, and robot actions within a shared policy framework. A common design uses a pre-trained VLM to encode semantic and perceptual context, which then conditions a dedicated action-generation module. Early systems formulate control as autoregressive prediction over discretized action tokens [23], [24]. This formulation directly reuses language-model training objectives, but action discretization and sequential decoding can limit precision and increase the cost of modeling long trajectories. More recent approaches employ continuous action experts based on diffusion or flow matching to represent multimodal action distributions and generate an entire future trajectory in parallel [1]–[3], [5], [25], [26]. Their architectures range from decoupled designs, in which action queries attend to fixed VLM features, to coupled designs that jointly update VLM and action tokens through a shared attention stack. 

Existing work has primarily focused on improving policy training and action generation, while typically relying on 

a manually selected, fixed execution horizon at inference time. In contrast, we study when predicted future actions cease to be sufficiently grounded in the current observation. Our method treats sustained dispersion in action-to-VLM attention as an empirical signal and uses it to adapt the action-execution horizon at inference time. 

## _B. Action Chunking_ 

Unlike single-step action inference, action chunking [27] generates and executes a sequence of actions in a single pass, which mitigates cumulative errors and enhances the temporal modeling capabilities of the model. Following its introduction in ALOHA [15], this technique became the standard paradigm for VLA models [1], [2], [5], [25]. However, fixed execution horizons require tedious manual tuning for specific tasks and restrict adaptive generalization. While BID [20] attempts to identify optimal chunk lengths, it maintains static horizons during execution, remaining unresponsive to task dynamics. [18] performs **multiple sampling (MS)** during the flow matching denoising process to estimate action uncertainty via entropy for dynamic truncation. Alternatively, [19] utilizes **self-attention (SA)** weights of action tokens relative to sequence anchors to evaluate confidence. This strategy essentially relies on internal sequence consistency but overlooks the root cause of action drift, specifically that current observations become stale for long-range predictions. To address these challenges, we propose an adaptive action chunking method based on the dispersion of crossattention. By measuring the distribution characteristics of attention from action tokens to VLM tokens, we characterize prediction confidence with negligible computational burden. Experimental results demonstrate that our approach improves adaptive execution performance in multi-task environments without introducing substantial overhead. 

## III. METHODS 

## _A. Unified Interaction Formulation in VLA_ 

To develop a general adaptive chunking mechanism, we first examine how different VLA architectures handle the interaction between actions and perceptions. While specific implementations vary, most modern frameworks rely on an attention-based interface to fuse multimodal information. For 


Fig. 3: **Visualization of attention dynamics within the action expert of** _π_ 0 _._ 5 **.** (a) provides a comprehensive view across all 18 layers, where the vertical axis represents 50 action queries per layer and the horizontal axis comprises 1,018 key tokens (768 visual, 200 language, and 50 action tokens). (b) and (c) present magnified views of Layer 9 and Layer 14. Red boxes highlight the pronounced attention dispersion for later-stage actions, whereas tokens with smaller indices exhibit negligible reliance on these visual features. 

instance, _π_ 0 _._ 5 adopts a decoupled paradigm where VLM tokens serve as static keys and values that remain unchanged across all layers. In contrast, X-VLA utilizes a coupled paradigm where VLM and action tokens are concatenated and updated jointly via self-attention. 

Despite these architectural differences, the underlying action generation process can be unified as a cross-attentional retrieval. Specifically, as shown in Fig. 2, the expert uses a set of **action queries** _{aj}_<sup>_H_</sup> _j_ =1<sup>_p_toextractinformationfrom</sup> **perceptual keys** _{vi}_<sup>_N_</sup> _i_ =1<sup>providedbytheVLMbackbone.</sup> This interaction is captured by an attention weight matrix, where the row index _j_ represents the temporal step of the predicted action sequence, and the column index _i_ corresponds to the perceptual features of the observation. This unified formulation enables us to seek an internal signal within the attention matrix that is associated with reduced perceptual grounding of future actions. In the following sections, we instantiate our methodology using _π_ 0 _._ 5 as the representative model to analyze cross-attention dynamics, with X-VLAspecific adaptations discussed in the experimental evaluation. 

## _B. Attention Dispersion and Entropy Dynamics_ 

_1) Qualitative Observation of Attention Maps:_ We begin by visualizing the head-averaged action-query attention matrix **A**<sup>¯</sup> _l ∈_ [0 _,_ 1]<sup>_Hp×_(</sup><sup>_N_+</sup><sup>_Hp_)</sup> at each layer _l_ of the action expert. As illustrated in Fig. 3a, the vertical axis represents the _Hp_ = 50 action queries at each layer, while the horizontal axis comprises both VLM and action-token keys. Specifically, the first _N_ = 968 columns correspond to 768 visual tokens and 200 language tokens, and the remaining 50 columns correspond to action tokens. Because the qualitative patterns are consistent across denoising steps, 

we visualize the final denoising step (step 10). The crossmodal component analyzed by our method is the action-toVLM submatrix **W** _l_ , corresponding to the first _N_ columns of **A**<sup>¯</sup> _l_ . 

A global inspection of the intermediate and deep layers, specifically from Layer 9 to Layer 15, reveals a systematic shift in attention focus. For actions at the beginning of the sequence, the attention exhibits sharp and concentrated saliency, primarily localized on language tokens. However, as the action index increases, the attention focus shifts toward visual tokens and becomes significantly dispersed. We magnify Layer 9 (Fig. 3b) and Layer 14 (Fig. 3c) as representative examples. As indicated by the red boxes, attention for later actions is distributed across nearly the entire visual field. This intra-layer transition shows an empirically observed regime in which later action tokens are less selectively grounded in the current perceptual context; we therefore examine attention dispersion as a candidate empirical risk signal associated with reduced perceptual grounding of future actions. 

_2) Quantification via Cross-Attention Entropy:_ To quantify this phenomenon, we isolate the action-to-VLM dependency from the full attention matrix. Let _αl,j,i_ = _Wl_ [ _j, i_ ] denote the attention weight of the _j_ th action token on the _i_ th VLM token _vi_ at layer _l_ . We introduce cross-attention weight entropy to quantify how focus is distributed across VLM tokens, where higher values indicate a more divergent allocation. To mitigate layer-specific noise and enhance stability, we aggregate the action-to-VLM attention coefficients along the layer axis. These values are subsequently normalized to obtain a probability distribution _pj,i_ describing the relative 

attention assigned to each VLM token _vi_ by action token _aj_ : 


where Norm( _·_ ) ensures that<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_pj,i_=1foreachaction</sup> token _aj_ . Based on this distribution, the cross-attention weight entropy _Ej_ for each action token _aj_ is computed as 


Because _pj,i_ is defined over _N_ retained VLM tokens, its entropy is bounded by 0 _≤Ej ≤_ ln _N_ , with equality at the upper bound when attention is uniformly distributed. This architecture-dependent bound provides a normalized reference for distinguishing a genuinely dispersed highentropy plateau from a locally flat but still concentrated attention pattern. 

We analyze the evolution of cross-attention weight entropy _E_ relative to the action index _j_ . As illustrated in Fig. 4a, entropy consistently increases with the action index before reaching a stable plateau. This plateau indicates an empirically observed regime in which action-to-VLM attention is highly dispersed and temporally stable. We restrict this interpretation to the observed attention pattern and evaluate its association with action error below. The onset of this regime varies with the task stage. During coarse approach maneuvers, entropy increases gradually and attention remains concentrated over a longer action prefix. In contrast, during precise pre-interaction phases, entropy rises sharply and plateaus at a much earlier index. These observations motivate a stage-dependent execution rule: a fixed horizon cannot accommodate changes in the action-to-observation grounding pattern across different manipulation stages. 

_3) Entropy as Accuracy Proxy:_ To test whether entropy is associated with action prediction error rather than merely action index position, we conduct an inference analysis on held-out demonstration trajectories from the validation set. At each evaluated frame, the policy predicts a horizon of 50 actions. For every valid horizon index, we compare the predicted action with the ground-truth action at the corresponding future time step in the recorded trajectory and associate the resulting MSE with that action token’s crossattention entropy, with predictions extending beyond the end of a trajectory excluded. Entropy and MSE exhibit significant positive dependence (Pearson _r_ = 0 _._ 187, Spearman _ρ_ = 0 _._ 432; both _p <_ 10<sup>_−_120</sup> ). After regressing both variables on the within-chunk action index, their partial correlation remains significant ( _r_ = 0 _._ 214), showing that the relationship is not explained solely by later actions being harder to predict. 

To construct Fig. 4c, we sort all valid pairs by entropy and partition them into 12 equal-frequency bins. Each point reports the mean entropy and mean MSE of all pairs within one bin, thereby showing how average action prediction error varies across different entropy ranges while keeping the number of samples in each range comparable. The 

resulting relationship is strongly nonlinear: the average MSE rises sharply in the high-entropy regime near _E_ = 6 _._ 5, which is approximately 95% of the theoretical entropy upper bound ln(968). Moreover, samples in the highest-entropy quartile exhibit 10.4 times the mean MSE and 12.1 times the MSE standard deviation of samples in the remaining three quartiles. This marked increase in both prediction error and error variability indicates that high cross-attention entropy is associated with elevated prediction risk, supporting its use as an online signal for adaptive truncation. 

## _C. Adaptive Action Chunking_ 

Based on the observed entropy dynamics, we propose an Adaptive Action Chunking strategy that dynamically selects the execution horizon during inference. Given the crossattention entropy sequence **E** = _{E_ 1 _, E_ 2 _, . . . , EHp}_ computed at the final denoising step, the method identifies the earliest point at which attention enters a sustained high-dispersion regime. 

To reduce noise in the entropy sequence, we first apply a moving-average filter with a window size of _k_ : 


We then compute the first-order change of the smoothed entropy sequence: 


A low entropy gradient alone is not sufficient to indicate saturation, because entropy can also vary slowly while remaining concentrated. Therefore, we detect a plateau only when the smoothed entropy is both high and temporally stable. Specifically, we define the set of candidate plateau locations as 


where _η_ is the normalized high-entropy threshold and _τ_ is the stability threshold. The first condition requires every smoothed entropy value in the _k_ -step window to exceed a fraction _η_ of the maximum entropy ln _N_ . The second condition requires the average absolute entropy change within the same window to remain small. The adaptive execution horizon is then defined as 


The offset + _k_ accounts for the _k_ -step window used to detect the plateau. Consequently, a low-entropy plateau does not trigger truncation: if no window satisfies both conditions, the policy executes the full predicted horizon _Hp_ . 

By selecting the execution horizon from the observed action-to-VLM attention dynamics, the method retains longer action chunks while attention remains concentrated and 


Fig. 4: **Action entropy analysis.** (a) Attention entropy exhibits distinct growth rates across the task stages visualized in (b). Precise interactions (pre-grasping) lead to a sharper rise and earlier saturation than coarse movements (approaching). (c) Offline evaluation on the validation set shows that the action-prediction MSE rises sharply as cross-attention entropy approaches its theoretical maximum. Samples in the highest-entropy quartile exhibit 10.4 times the mean MSE and 12.1 times the MSE standard deviation of remaining samples. 


Fig. 5: **Entropy patterns in X-VLA.** Two distinct patterns are observed: the rising-plateau pattern reaches a sustained high-entropy regime, whereas the fluctuating-ascent pattern continues to vary without forming a stable plateau. 


Fig. 6: **Real-world tasks.** We evaluate the generalizability of our adaptive chunking method across three representative real-world tasks: Hang mug, Stack cups, and Tidy pens. 

truncates only after detecting a sustained high-dispersion regime associated with increased prediction error. The rule uses attention weights already produced by the action expert and requires neither retraining nor additional sampling. 

## IV. EXPERIMENTS 

We evaluate our adaptive action chunking method using state-of-the-art _π_ 0 _._ 5 and X-VLA models across the RoboTwin 2.0 [28], [29] and LIBERO [30] benchmarks, as well as three real-world tasks. Systematic comparisons against fixedlength, multi-sampling [18] (MS), and self-attention-based 

TABLE I: RoboTwin 2.0 task statistics. 

|**Task**|**Avg. Frames**|**Horizon**|
|---|---|---|
|Place phone stand|127.74|Short|
|Place fan|147.66|Short|
|Move can pot|151.68|Short|
|Place dual shoes|227.94|Medium|
|Place bread basket|238.80|Medium|
|Hand over block|284.98|Medium|
|Stack blocks two|313.58|Medium|
|Blocks rank rgb|461.00|Long|
|Stack blocks three|473.16|Long|
|Put bottles dustbin|622.42|Long|


[19] (SA) baselines demonstrate that our method improves success rates and generalizability. 

_Hyperparameters._ We use a common configuration of _k_ = 5, _τ_ = 0 _._ 01, and _η_ = 0 _._ 95 across models, benchmarks, and tasks. The normalized high-entropy ratio _η_ is selected once according to the entropy–MSE relationship in Fig. 4c, which shows a rapid increase in action error in the high-entropy regime, and is not tuned for individual tasks or architectures. The sole exception is _π_ 0 _._ 5 on LIBERO: because this policy predicts only _Hp_ = 10 actions per query, we use a proportionally shorter smoothing window of _k_ = 3. All four LIBERO suites share this setting, while _τ_ and _η_ remain unchanged. 

## _A. Simulation_ 

_1) RoboTwin 2.0 Experiments:_ To ensure comprehensive assessment, we evaluate 10 representative RoboTwin 2.0 tasks, categorized by average episode length into short (3 tasks), medium (4 tasks), and long-horizon (3 tasks) tiers. The selected tasks and their average episode lengths are summarized in Tab. I. For _π_ 0 _._ 5, we fine-tune individual checkpoints for 40,000 steps (batch size 32) using 50 Aloha Agilex demonstrations per task. For X-VLA, we evaluate the open-source checkpoint trained on all 50 RoboTwin tasks. All evaluations are conducted in RoboTwin’s clean mode using three random seeds per configuration, with 100 rollouts each. 

_Evaluation on π_ 0 _._ 5 _._ The fine-tuned _π_ 0 _._ 5 model generates a candidate sequence of _Hp_ = 50 actions per inference step. 

TABLE II: Success Rate (%) and Average Action Length for _π_ 0 _._ 5 in RoboTwin 2.0 benchmark. 

||||**Success Rate**|**(%) by Exe**|**cution Chunk**|||**Ours**|
|---|---|---|---|---|---|---|---|---|
|**Task Name**|**10**|**15**|**20**|**25**|**SA**|**MS**|**Ours**|**Avg. Len.**|
|Blocks rank rgb|80.0|62.0|52.7|43.3|58.3|74.7|77.3|20.83|
|Put bottles dustbin|89.3|90.0|84.7|82.7|87.3|78.0|91.3|19.54|
|Stack blocks three|63.0|43.3|28.7|36.7|53.0|66.0|62.3|18.30|
|Stack blocks two|91.7|85.0|82.0|77.3|85.0|81.3|89.3|20.31|
|Hand over block|19.0|27.0|29.0|25.3|26.0|10.0|25.3|15.91|
|Place dual shoes|31.0|37.0|37.0|38.7|36.0|33.7|39.3|17.10|
|Place bread basket|55.7|54.7|55.7|55.0|52.3|48.0|57.3|14.88|
|Move can pot|90.7|87.0|73.0|68.3|75.3|84.7|87.3|17.89|
|Place fan|44.0|42.7|37.3|39.0|41.3|51.0|42.7|21.42|
|Place phone stand|52.0|51.0|58.0|55.3|61.0|42.7|56.7|14.88|
|**Average**|61.6|58.0|53.8|52.2|57.6|57.0|**62.9**|18.11|


We evaluate several fixed execution chunk lengths, specifically 10, 15, 20, and 25, while omitting longer horizons due to their significantly degraded success rates. Dynamic baselines include the multi-sampling method, which utilizes 20 iterations to estimate action entropy, and the self-attentionbased approach. The mean success rates across three seeds are summarized in Tab. II. Our method achieves a leading average success rate of 62.9%, outperforming all fixed-chunk baselines and established methods such as self-attentionbased (SA) and multi-sampling (MS). While fixed-chunk baselines can achieve competitive performance on individual tasks, their adaptability across a diverse multi-task suite is limited compared to our approach. Our method achieves the highest average success rate across the evaluated task suite, demonstrating both stability and effective generalization. It outperforms the strongest baseline (chunk size = 10) despite having a much longer average execution horizon of 18.11 steps. This indicates that stage-aware dynamic adjustment can improve success rates while reducing inference frequency. By extending execution during high-confidence phases, our strategy lowers computational overhead, providing a better trade-off between task precision and inference efficiency. 

_Evaluation on X-VLA._ To further validate the generalizability of our method, we conduct the same experiments on X-VLA. X-VLA generates a candidate sequence of _Hp_ = 30 actions at each inference step. We evaluate fixed execution horizons of 15, 20, 25 and 30, while omitting shorter horizons due to their low success rates. Although X-VLA employs coupled self-attention over concatenated VLM and action tokens, we apply the same extraction procedure described in Sec. III. Specifically, we first average the action-query attention weights across heads to obtain **A**<sup>¯</sup> _l_ and then extract the action-query-to-VLM-key block **W** _l_ . For X-VLA, this block contains the attention assigned by each action query to the _N_ = 200 VLM tokens. We compute the normalized distribution _pj,i_ and its entropy _Ej_ following Eq. 1 and Eq. 2. As shown in Fig. 5, X-VLA exhibits both risingplateau and fluctuating-ascent patterns. We apply exactly the same normalized criterion in Eq. 5 as for _π_ 0 _._ 5, without an architecture-specific entropy-increment threshold. A rising 

TABLE III: Success Rate (%) for X-VLA. 

||**S**|**R (%) **|**by Exec**|**ution Ch**|**unk**|
|---|---|---|---|---|---|
|**Task Name**|**15**|**20**|**25**|**30**|**Ours**|
|Blocks rank rgb|33.0|84.0|85.7|82.7|84.0|
|Put bottles dustbin|46.0|72.7|80.0|80.0|71.3|
|Stack blocks three|22.0|52.7|58.0|45.3|59.3|
|Stack blocks two|32.0|94.0|90.0|81.3|94.0|
|Hand over block|80.3|61.7|80.3|90.0|94.0|
|Place dual shoes|72.0|70.0|76.0|76.7|76.0|
|Place bread basket|50.7|67.3|64.3|71.0|64.7|
|Move can pot|32.7|61.0|82.0|76.3|88.0|
|Place fan|26.0|40.7|72.3|66.0|74.3|
|Place phone stand|40.0|45.0|52.0|91.3|84.0|
|**Average**|43.5|64.9|74.1|76.1|**79.0**|


or fluctuating sequence that never forms a sustained highentropy plateau leaves _C_ empty and therefore executes the full 30-action horizon; only a sustained high-entropy plateau triggers truncation. Results in Tab. III show that although fixed execution lengths achieve peak performance on individual tasks, their performance varies substantially across the task suite. Our method attains the highest average success rate without model-specific threshold design. 

_2) LIBERO Experiments:_ We evaluate our method on all four LIBERO task suites using a publicly available _π_ 0 _._ 5 checkpoint trained on LIBERO. We compare adaptive execution against fixed execution chunks of 2, 4, 6, 8, and 10 actions without modifying the policy parameters. As shown in Tab. IV, our method achieves the highest success rate on every suite and improves the overall average from 94.88% for the strongest fixed-chunk baseline (chunk size 6) to 97.25%. The improvement is most pronounced on LIBEROLong, where our method reaches 94.5%, exceeding the best fixed setting by 4.5 percentage points. These results indicate that a single static execution horizon cannot consistently accommodate tasks with different temporal structures, whereas adaptive action chunking transfers effectively to a separately trained policy and benchmark. 

TABLE IV: Success rate (%) on the LIBERO benchmark. 

|**Execution**|**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|
|Fixed-2|97.5|96.5|93.0|85.0|93.00|
|Fixed-4|97.5|97.0|94.5|89.5|94.63|
|Fixed-6|98.0|97.0|94.5|90.0|94.88|
|Fixed-8|97.0|97.5|92.5|89.5|94.13|
|Fixed-10|97.0|97.0|95.5|89.5|94.75|
|**Ours**|**99.5**|**98.5**|**96.5**|**94.5**|**97.25**|


TABLE V: Success rate for real-world tasks. 

||||**SR (%)**|**by E**|**xecutio**|**n Ch**|**unk**||
|---|---|---|---|---|---|---|---|---|
|**Task Name**|**10**|**20**|**30**|**40**|**50**|**SA**|**MS**|**Ours**|
|Hang Mug|55|45|60|60|65|60|20|**75**|
|Stack Cups|60|55|60|65|50|65|15|**70**|
|Tidy Pens|20|**40**|35|15|10|**40**|20|**40**|
|Average|45|46.7|51.7|46.7|41.7|55|18.3|**61.7**|


## _B. Real-World Experiments_ 

_1) Platform and Tasks:_ Our real-world system uses a dual-arm ARX R5 follower robot and an ARX X5 leader for bilateral teleoperation. Two wrist-mounted fisheye cameras provide local manipulation views, while a head-mounted RGB camera observes the full workspace. Images are captured at 20 Hz and the low-level control loop runs at 60 Hz. We evaluate three tasks shown in Fig. 6: _Hang mug_ , a single-arm task requiring precise placement on a mug-tree branch under partial occlusion; _Tidy pens_ , which transitions from single-arm placement to a dual-arm handover; and _Stack cups_ , a contact-rich dual-arm task requiring three cups to be stacked vertically. 

_2) Training and Evaluation Protocol:_ For each task, we collect 50 expert demonstrations and fine-tune a separate _π_ 0 _._ 5 policy for 40,000 steps with batch size 32. Each execution method is evaluated over 20 independent trials per task. 

As shown in Tab. V, our method consistently improves success rates for both single-arm and dual-arm tasks. The average success rate across the three tasks increases by 10 percentage points compared to the best fixed-chunk configuration (chunk = 30) and by 6.7 percentage points relative to the strongest adaptive action chunking baseline (SA). It is also observed that the multi-sampling (MS) method struggles due to the fragmented execution resulting from the small chunk size. Using the configuration reported in the original literature, the robot exhibits intermittent pauses during movement, which impacts the overall success rate. These results demonstrate the effectiveness of utilizing the dispersion of cross-attention within the action expert as a metric to characterize the accuracy of predicted actions. 

## _C. Efficiency Analysis_ 

We analyze the computational latency for a single action chunk inference cycle on a single NVIDIA A100 GPU using _π_ 0 _._ 5. As shown in Tab. VI, the multi-sampling (MS) method increases the latency of each inference cycle by 29.5 ms. 

TABLE VI: Latency Analysis 

|Method|Fixed|MS|SA|**Ours**|
|---|---|---|---|---|
|Latency / s _↓_|0.2661|0.2956|0.2728|**0.2725**|


Although MS employs parallel execution for multiple sampling passes, such overhead remains considerable for highfrequency closed-loop control. Conversely, attention-based strategies, including the self-attention-based (SA) baseline and our approach, introduce less than 7 ms of additional latency relative to fixed chunking. By exploiting intrinsic model signals rather than executing redundant sampling passes, our method facilitates real-time dynamic action chunking with minimal computational cost. 

## V. CONCLUSION 

This paper introduces an adaptive action chunking strategy using internal cross-attention dynamics in action expert modules. By calculating attention entropy from weight distributions, we characterize model predictive boundaries relative to observations. This enables a training-free dynamic truncation mechanism that adjusts the execution horizon during inference. Our experiments demonstrate improved success rates and robustness across multiple state-of-the-art VLA models in various multi-task settings. These improvements, achieved with negligible overhead, indicate that intrinsic epistemic uncertainty can be effectively used to enhance closed-loop robotic control. 

## VI. LIMITATIONS 

Our framework currently depends on identifiable crossattention pathways. Architectures with highly interleaved or hierarchical structures present challenges in aggregating unified uncertainty signals. Furthermore, we have yet to evaluate our method on emerging World Action Models (WAMs) [31]–[33] exhibiting distinct generative dynamics. Extending this adaptive strategy to such complex paradigms remains a promising future direction. 

## REFERENCES 

- [1] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [2] K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. R. Equi, C. Finn, N. Fusai, M. Y. Galliker _et al._ , “ _π_ 0 _._ 5 : a visionlanguage-action model with open-world generalization,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [3] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” _arXiv preprint arXiv:2410.07864_ , 2024. 

- [4] S. Liu, B. Li, K. Ma, L. Wu, H. Tan, X. Ouyang, H. Su, and J. Zhu, “Rdt2: Exploring the scaling limit of umi data towards zero-shot crossembodiment generalization,” _arXiv preprint arXiv:2602.03310_ , 2026. 

- [5] NVIDIA, :, J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. J. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, J. Jang, Z. Jiang, J. Kautz, K. Kundalia, L. Lao, Z. Li, Z. Lin, K. Lin, G. Liu, E. Llontop, L. Magne, A. Mandlekar, A. Narayan, S. Nasiriany, S. Reed, Y. L. Tan, G. Wang, Z. Wang, J. Wang, Q. Wang, J. Xiang, Y. Xie, Y. Xu, Z. Xu, S. Ye, Z. Yu, A. Zhang, H. Zhang, Y. Zhao, R. Zheng, and Y. Zhu, “Gr00t n1: An open foundation model for generalist humanoid robots,” 2025. [Online]. Available: https://arxiv.org/abs/2503.14734 

- [6] Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Hu, X. Huang _et al._ , “Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems,” _arXiv preprint arXiv:2503.06669_ , 2025. 

- [7] Q. Bu, Y. Yang, J. Cai, S. Gao, G. Ren, M. Yao, P. Luo, and H. Li, “Univla: Learning to act anywhere with task-centric latent actions,” _arXiv preprint arXiv:2505.06111_ , 2025. 

- [8] G. R. Team, S. Abeyruwan, J. Ainslie, J.-B. Alayrac, M. G. Arenas, T. Armstrong, A. Balakrishna, R. Baruch, M. Bauza, M. Blokzijl _et al._ , “Gemini robotics: Bringing ai into the physical world,” _arXiv preprint arXiv:2503.20020_ , 2025. 

- [9] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti _et al._ , “Smolvla: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [10] J. Sohl-Dickstein, E. Weiss, N. Maheswaranathan, and S. Ganguli, “Deep unsupervised learning using nonequilibrium thermodynamics,” in _International conference on machine learning_ . pmlr, 2015, pp. 2256–2265. 

- [11] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” _Advances in neural information processing systems_ , vol. 33, pp. 6840–6851, 2020. 

- [12] J. Song, C. Meng, and S. Ermon, “Denoising diffusion implicit models,” _arXiv preprint arXiv:2010.02502_ , 2020. 

- [13] Y. Lipman, M. Havasi, P. Holderrieth, N. Shaul, M. Le, B. Karrer, R. T. Chen, D. Lopez-Paz, H. Ben-Hamu, and I. Gat, “Flow matching guide and code,” _arXiv preprint arXiv:2412.06264_ , 2024. 

- [14] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” _arXiv preprint arXiv:2210.02747_ , 2022. 

- [15] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” _arXiv preprint arXiv:2304.13705_ , 2023. 

- [16] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , vol. 44, no. 10-11, pp. 1684–1704, 2025. 

- [17] J. So, C. Lee, S. Lee, J. Ok, and E. Park, “Improving generative behavior cloning via self-guidance and adaptive chunking,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 84 432–84 456, 2026. 

- [18] Y. Liang, X. Wang, K. Wang, S. Wang, X. Peng, H. Chen, D. K. H. Chua, and P. Vadakkepat, “Adaptive action chunking at inference-time for vision-language-action models,” _arXiv preprint arXiv:2604.04161_ , 2026. 

- [19] H. Wang, G. Zhang, Y. Yan, R. R. Kompella, and G. Liu, “Vla knows its limits,” _arXiv preprint arXiv:2602.21445_ , 2026. 

- [20] Y. Liu, J. Hamid, A. Xie, Y. Lee, M. Du, and C. Finn, “Bidirectional decoding: Improving action chunking via guided test-time sampling,” in _International Conference on Learning Representations_ , vol. 2025, 2025, pp. 4594–4627. 

- [21] K. Black, M. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 33 383–33 407, 2026. 

- [22] Y. Liu, H. Yu, J. Zhao, B. Li, D. Zhang, M. Li, W. Wu, Y. Hu, J. Xie, J. Guo _et al._ , “Learning native continuation for action chunking flow policies,” _arXiv preprint arXiv:2602.12978_ , 2026. 

- [23] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [24] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [25] J. Zheng, J. Li, Z. Wang, D. Liu, X. Kang, Y. Feng, Y. Zheng, J. Zou, Y. Chen, J. Zeng _et al._ , “X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model,” _arXiv preprint arXiv:2510.10274_ , 2025. 

- [26] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn _et al._ , “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 1702–1713. 

- [27] L. Lai, A. Z. Huang, and S. J. Gershman, “Action chunking as policy compression,” _PsyArXiv_ , 2022. 

- [28] T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Z. Li, Q. Liang, X. Lin, Y. Ge, Z. Gu _et al._ , “Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation,” _arXiv preprint arXiv:2506.18088_ , 2025. 

- [29] Y. Mu, T. Chen, Z. Chen, S. Peng, Z. Lan, Z. Gao, Z. Liang, Q. Yu, Y. Zou, M. Xu _et al._ , “Robotwin: Dual-arm robot benchmark with generative digital twins,” in _Proceedings of the computer vision and pattern recognition conference_ , 2025, pp. 27 649–27 660. 

- [30] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” in _Advances in Neural Information Processing Systems_ , vol. 36, 2023. 

- [31] S. Ye, Y. Ge, K. Zheng, S. Gao, S. Yu, G. Kurian, S. Indupuru, Y. L. Tan, C. Zhu, J. Xiang _et al._ , “World action models are zeroshot policies,” _arXiv preprint arXiv:2602.15922_ , 2026. 

- [32] L. Li, Q. Zhang, Y. Luo, S. Yang, R. Wang, F. Han, M. Yu, Z. Gao, N. Xue, X. Zhu _et al._ , “Causal world modeling for robot control,” _arXiv preprint arXiv:2601.21998_ , 2026. 

- [33] T. Yuan, Z. Dong, Y. Liu, and H. Zhao, “Fast-wam: Do world action models need test-time future imagination?” _arXiv preprint arXiv:2603.16666_ , 2026. 

