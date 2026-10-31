---
title: "Reshaping Action Error Distributions for Reliable Vision-Language-Action Models"
date: "2026-02-04"
authors: "Shuanghao Bai; Dakai Wang; Cheng Chi; Wanqi Zhou; Jing Lyu; Xiaoguang Zhao"
url: https://arxiv.org/abs/2602.04228
pdf: https://arxiv.org/pdf/2602.04228
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.04228)** / [論文ページ](https://arxiv.org/abs/2602.04228)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Reshaping Action Error Distributions for Reliable Vision-Language-Action Models 

Shuanghao Bai<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> Dakai Wang<sup>1</sup><sup>_∗_</sup> Cheng Chi<sup>2</sup><sup>_∗_</sup> Wanqi Zhou<sup>1</sup> Jing Lyu<sup>2</sup><sup>_,_3</sup><sup>_,_4</sup> Xiaoguang Zhao<sup>3</sup> Pengwei Wang<sup>2</sup> Zhongyuan Wang<sup>2</sup> Lei Xing<sup>1</sup> Shanghang Zhang<sup>2</sup><sup>_,_5</sup><sup>_†_</sup> Badong Chen<sup>1</sup><sup>_†_</sup> 

> 1 Institute of Artificial Intelligence and Robotics, Xi’an Jiaotong University 

> 2 Beijing Academy of Artificial Intelligence 

> 3 Institute of Automation, University of Chinese Academy of Sciences 

> 4 School of Artificial Intelligence, University of Chinese Academy of Sciences 

> 5 Peking University 

**_Abstract_ —In robotic manipulation, vision–language–action (VLA) models have emerged as a promising paradigm for learning generalizable and scalable robot policies. Most existing VLA frameworks rely on standard supervised objectives, typically cross-entropy for discrete actions and mean squared error (MSE) for continuous action regression, which impose strong pointwise constraints on individual predictions. In this work, we focus on continuous-action VLA models and move beyond conventional MSE-based regression by reshaping action error distributions during training. Drawing on information-theoretic principles, we introduce Minimum Error Entropy (MEE) into modern VLA architectures and propose a trajectory-level MEE objective, together with two weighted variants, combined with MSE for continuous-action VLA training. We evaluate our approaches across standard, few-shot, and noisy settings on multiple representative VLA architectures, using simulation benchmarks such as LIBERO and SimplerEnv as well as real-world robotic manipulation tasks. Experimental results demonstrate consistent improvements in success rates and robustness across these settings. Under imbalanced data regimes, the gains persist within a well-characterized operating range, while incurring negligible additional training cost and no impact on inference efficiency. We further provide theoretical analyses that explain why MEEbased supervision is effective and characterize its practical range. Project Page: VLA-TMEE Website.** 

## I. INTRODUCTION 

Information-theoretic principles have long served as a foundational driver of modern deep learning. In recent years, the rapid emergence of large-scale foundation models has further accelerated progress in artificial intelligence, leading to unprecedented growth across a wide range of domains. In robotic manipulation, Vision-Language-Action (VLA) models have demonstrated strong potential for generalization and scalability by leveraging the powerful visual and linguistic understanding, reasoning, and generation capabilities inherited from large Vision-Language Models (VLMs) [47, 27, 2]. Within this paradigm, classical information-theoretic learning objectives, such as cross entropy for classification and mean squared error (MSE) for regression, remain fundamental components. These objectives play central roles in discrete action modeling [20, 8] and continuous action generation [36, 19], respectively. 

As both discrete and continuous action modeling paradigms continue to evolve, we focus on continuous-action VLA models because they represent actions in a metric space with a well-defined notion of prediction error. This modeling choice naturally leads to pointwise regression objectives, most commonly mean squared error (MSE), which provide a simple and effective supervision signal for continuous control and are widely adopted in practice [30, 26]. Despite their empirical success and stable optimization behavior, MSEbased objectives operate solely at the level of individual action predictions. From an analysis perspective, however, action prediction errors can be viewed not only as isolated deviations, but also as samples drawn from an underlying error distribution that evolves across time and action dimensions. Such distributions often exhibit structured patterns, including dispersion, skewness, or correlated variations, even when perstep regression losses are well optimized, as illustrated in Figure 1. This observation suggests that beyond per-step accuracy, the collective organization and geometry of action errors are not explicitly regulated by pointwise regression objectives. 

From a distributional perspective, the behavior of a policy is governed not only by the magnitude of individual errors, but also by the uncertainty, concentration, and structure of the error distribution as a whole. Information-theoretic criteria provide a natural framework for characterizing such distribution-level properties, as they operate directly on probability distributions rather than individual samples. In particular, entropy-based objectives offer a principled way to quantify how concentrated or dispersed an error distribution is, without committing to strong parametric assumptions. Among such objectives, the minimum error entropy (MEE) criterion [25, 9] directly targets the entropy of the action error distribution, enabling interactions among errors within a batch or trajectory and providing a mechanism to aggregate errors beyond pointwise regression. 

To operationalize entropy-based error aggregation in VLA models, we adapt the MEE criterion to the action prediction setting by reformulating it over trajectory-level action errors, resulting in Trajectory-level MEE (T-MEE). Building on this formulation, we further introduce two complementary 

> * Equal contribution. _†_ Corresponding authors. 


Fig. 1. **PCA visualization of action error distributions with and without trajectory-level MEE (T-MEE).** Each point represents an action error at a specific time step along a trajectory. The top-10 most extreme outliers are highlighted with numeric labels, while red circles indicate compact action error clusters. Results are shown for BC-Transformer and GR00T trained with standard MSE-based behavior cloning and with the proposed T-MEE objective on LIBERO-Object. Per-task success rates (SR) for the two visualized tasks are annotated in the figure. For reference, the overall SR on the full 10-task LIBEROObject suite improves from 57.4% to 68.2% for BC-Transformer and from 94.4% to 97.8% for GR00T. Across both architectures and tasks, incorporating T-MEE leads to more compact and coherent action error distributions in the projected space. 

weighted variants: Chunk-weighted T-MEE (Cw-TMEE) and Element-weighted T-MEE (Ew-TMEE). These variants provide finer-grained control over how action errors are aggregated and interact within the entropy objective. We conduct a comprehensive empirical evaluation across multiple VLA architectures and model scales. Our experiments span nearbalanced, few-shot, noisy, and imbalanced data regimes, and demonstrate consistent improvements across a broad range of settings. By systematically varying the degree of data imbalance, we further characterize the effective operating regime of entropy-based error aggregation and identify conditions under which it is most beneficial. Complementary analysis experiments provide insights into the resulting error distribution dynamics induced by the proposed objectives. 

In addition to empirical validation, we provide a theoretical analysis of the optimization behavior induced by the MEE objective. Our analysis characterizes three key properties that help explain the observed empirical behavior. First, we show that MEE induces similarity-weighted interactions among action errors, resulting in a distribution-level optimization effect that regulates the relative geometry of the error space rather than penalizing individual error magnitudes. Second, we establish that the influence of outlying or highly corrupted errors is inherently bounded under MEE, offering a principled explanation for its robustness compared to conventional regression objectives. Finally, we analyze how MEE induces coupling or decoupling among multiple tasks through interactions in error space, and show that cross-task transfer and interference are jointly governed by task similarity, as reflected by the overlap of their error distributions, and by sample imbalance. 

Our contributions are threefold. First, we revisit action 

errors from a distributional perspective and adapt MEE to the VLA setting, proposing three trajectory-level variants to capture structured action error distributions. Second, we provide theoretical analyses that characterize the optimization behavior of the proposed objectives and establish conditions under which they are effective. Finally, we conduct extensive empirical evaluations on two simulation benchmarks and realrobot manipulation tasks across multiple VLA architectures and model scales, spanning balanced, few-shot, noisy, and imbalanced training regimes, and complement these results with targeted analysis to validate effectiveness and provide insights into the behavior of the proposed methods. 

## II. RELATED WORK 

**Information-Theoretic Supervision for Continuous Regres-** 

**sion.** Mean squared error (MSE) is among the most widely used regression loss functions in machine learning due to its favorable optimization properties and stable behavior in practice [24]. By penalizing squared deviations between predictions and targets, MSE enforces pointwise agreement but captures only a single aspect of prediction errors, namely their second-order moment, without explicitly modeling the global structure of the underlying error distribution. This limitation has motivated prior work on characterizing error distributions beyond pointwise loss measures [6]. Information-theoretic objectives address this limitation by operating directly at the distribution level. In particular, Minimum Error Entropy (MEE) [25, 9, 10] minimizes the entropy of the empirical error distribution, encouraging errors to concentrate into compact and structured configurations without assuming a predefined parametric form. Compared to alternative informationtheoretic criteria, such as KL divergence–based [44] or mutual 

information–based [3] objectives, MEE avoids the need to specify a target distribution or to perform explicit information estimation in high-dimensional continuous spaces. In this work, we introduce MEE into the VLA setting and adapt it to continuous action regression. We further propose three trajectory-level variants and provide a comprehensive theoretical analysis to characterize their optimization behavior and effectiveness. A detailed review of related MEE literature is provided in Appendix E. 

**Vision-Language-Action (VLA) Models.** VLA models build upon advances in vision-language models, inheriting strong visual-language understanding, reasoning, and generation capabilities [47, 27, 45]. These capabilities enable unified action modeling and have demonstrated favorable scaling behavior in robotic manipulation [39]. Beyond large-scale foundation models, the VLA paradigm has also been extended to smallerscale architectures that take visual-language inputs and directly produce action outputs, further broadening its applicability. Existing VLA approaches broadly fall into two paradigms. The first formulates action generation as autoregressive token prediction, in which actions are discretized and generated in a token space [20, 41]. The second focuses on continuous action generation, predicting continuous control signals via learnable action queries [3, 26], specialized action experts [29, 5, 4, 23], or their combinations [42]. This paradigm also includes dualsystem VLA architectures, where a fast System 1 executes low-level actions at high frequency, while a slower System 2 provides contextual guidance over longer timescales [7, 15]. In this work, we focus on the continuous-action paradigm and study its modeling properties from the perspective of reshaping action error distributions. Across diverse architectures and model scales, we conduct extensive experiments to evaluate the effectiveness and applicability range of the proposed approach under varied training regimes and data conditions. 

## III. PRELIMINARIES 

**Problem Setting.** We consider VLA learning under a behavior cloning (BC) paradigm for robotic manipulation. The environment is modeled as an instruction-conditioned sequential decision process, where a robot interacts with the environment under a natural language instruction. At each timestep _t_ , the robot receives a multimodal observation consisting of a visual observation _o_<sup>_t_</sup> , an optional proprioceptive state _s_<sup>_t_</sup> , and a language instruction _l_ . We denote the overall input as _x_<sup>_t_</sup> = ( _o_<sup>_t_</sup> _, s_<sup>_t_</sup> _, l_ ). The robot outputs a continuous action _a_<sup>_t_</sup> _∈A_ , such as end-effector motion commands or arm-gripper controls. In VLA, the policy _πθ_ is trained from an expert demonstration dataset _De_ = _{_ ( _x_<sup>_t_</sup> _, a_<sup>_t_</sup> ) _}_ by supervised learning. The objective is to learn a policy that mimics expert actions conditioned on the observed images and instructions. Formally, the BC objective is defined as 


In continuous-action VLA, the loss _L_ denotes a regression objective and is typically chosen as the MSE, yielding 


This pointwise regression objective enforces per-timestep agreement between predicted and expert actions and serves as the standard training objective for continuous-action VLA models. In the following sections, we revisit action errors from a distributional perspective and introduce information-theoretic supervision to reshape action error distributions. 

**Definition of MEE.** In a standard regression setting, an input _x_ is mapped to an output by a parametric model _fθ_ . Let _y ∈_ R<sup>_d_</sup> denote the ground-truth target, _y_ ˆ = _fθ_ ( _x_ ) the prediction, and _e_ = _y − y_ ˆ the prediction error. The Minimum Error Entropy (MEE) principle learns model parameters by minimizing the entropy of the error distribution. When instantiated with Shannon entropy [37], the objective is 


where _p_ ( _e_ ) denotes the probability density of the error variable. Minimizing _H_ ( _e_ ) encourages prediction errors to concentrate into a low-uncertainty distribution, rather than merely reducing their expected magnitude. However, direct optimization of Shannon entropy is generally intractable due to the need for explicit density estimation. In practice, MEE is commonly instantiated using the quadratic R´enyi entropy [35], 


which provides a tractable approximation to Shannon entropy. Minimizing _H_ 2( _e_ ) is equivalent to maximizing the squared density integral and favors compact error distributions. 

## IV. METHOD 

## _A. Adapt MEE to VLA Models_ 

Classical MEE formulations are typically defined over scalar, sample-level prediction errors and are primarily applied in i.i.d. regression or adaptive filtering settings [10, 13]. In contrast, action prediction in VLA models is structured, involving high-dimensional actions generated over temporally correlated trajectories. To bridge this gap, we reformulate MEE at the trajectory level by treating action prediction errors across time and batch as samples from a shared error distribution. This trajectory-level MEE (T-MEE) enables entropy-based supervision to operate on the collective geometry of action errors induced by VLA policies. Building on this formulation, we further introduce Chunk-weighted and Element-weighted T-MEE variants, which provide finer-grained control over error shaping across temporal segments and action dimensions. 

In VLA models, let ˆ **a** _b,k_<sup>_t∈_R</sup><sup>_D_and</sup><sup>**a**</sup><sup>_t_</sup> _b,k_<sup>denote the predicted</sup> and ground-truth actions at the _k_ -th step of an action chunk generated at time _t_ for trajectory _b_ , where _k ∈{_ 0 _, . . . , K −_ 1 _}_ and _K_ is the chunk size. We define the action prediction error as **e** _b,k_<sup>_t_=</sup><sup>**a**ˆ</sup> _b,k_<sup>_t−_</sup><sup>**a**</sup><sup>_t_</sup> _b,k_<sup>.Ratherthantreatingerrorsatindividual</sup> timesteps independently, we aggregate action prediction errors across batch, time, and chunk dimensions and regard them as samples drawn from a shared error random variable. This formulation aligns naturally with action chunking in VLA models, where multiple future actions are generated jointly 


Fig. 2. **Architectural taxonomy of continuous-action VLA models evaluated in this work.** We summarize representative small- and large-scale VLA architectures. (a–b) Small-scale models regress actions from multimodal features using lightweight backbones: (a) BC-RNN / BC-Transformer with MLP policy heads, and (b) BC-DP with a diffusion-based action expert. (c–f) Large-scale models build upon pretrained VLMs: (c) OFT introduces learnable action queries into autoregressive VLMs; (d) GR00T conditions an action expert (AE) on final-layer VLM features; (e) _π_ 0 variants enable tighter VLM–action coupling via multi-layer conditioning or shared attention; and (f) DS-VLA adopts a dual-system design with a fast System 1 for action execution and a slower System 2 for contextual guidance. Here, V denotes image tokens, L denotes language tokens, Q denotes query tokens, and N denotes noise inputs. 

as temporally correlated chunks. Formally, given a batch of _B_ trajectories with horizon _T_ and chunk size _K_ , the resulting set of error samples is 


We then apply the quadratic R´enyi entropy to the aggregated action error distribution. Specifically, all action error vectors **e** _b,k_<sup>_t_acrossthebatch,temporal,andchunkdimensionsare</sup> flattened into a set of _N_ = _B × T × K_ samples, denoted as _{_ **e** _i}_<sup>_N_</sup> _i_ =1<sup>. This yields the following T-MEE empirical objective:</sup> 


where _σ_ denotes the kernel bandwidth. Following standard practice in information-theoretic learning and prior MEEbased methods, _σ_ is chosen from the range [0 _._ 5 _,_ 2 _._ 0]. 

Building upon the T-MEE objective, we introduce a unified weighted formulation that accounts for the varying reliability of action error samples. Let _{_ **e** _i}_<sup>_N_</sup> _i_ =1<sup>denotetheaggregated</sup> action error vectors. Each error sample is assigned a nonnegative importance weight based on its magnitude: 


where _σw_ denotes the kernel bandwidth, which is fixed to 0.5. Using these weights, we define a weighted quadratic R´enyi 

entropy estimator as 


where _σ_ denotes the kernel bandwidth and _ωij_ specifies the weighting scheme. We set _ωij_ = _N_ <u>1</u><sup>2</sup><sup>_wi_,yieldingan</sup> asymmetric weighting that emphasizes reliable action chunks while aggregating errors across trajectories, which results in Chunk-weighted T-MEE (Cw-TMEE). Alternatively, we define _ωij_ = _wiwj_ , leading to a symmetric, element-weighted quadratic R´enyi entropy estimator, referred to as Elementweighted T-MEE (Ew-TMEE). 

Accurate trajectory imitation requires prediction errors to be not only structured but also centered near zero at each timestep. Pointwise regression supervision, such as MSE, provides this anchoring effect by directly penalizing the magnitude of individual action deviations and driving the error distribution toward the origin. Accordingly, we combine the distribution-level T-MEE objective with the standard MSE loss, yielding the final training objective: 


where _α_ balances the anchoring effect of pointwise accuracy and the distribution-level shaping. 

## _B. Model Architecture_ 

All evaluated models are summarized in Figure 2. We consider both small-scale and large-scale VLA models. For smallscale models, BC-RNN and BC-Transformer [32] regress 

actions from multimodal features using lightweight sequence models with a shared perception backbone. Both adopt ResNet-18 [22] as the image encoder and a BERT-based language encoder [17]. BC-RNN employs a 2-layer RNN backbone, while BC-Transformer uses a lightweight 4-layer Transformer [40], resulting in approximately 20M and 10M parameters, respectively. BC-DP [14, 3] follows a similar perception setup but replaces the policy head with a diffusionbased action expert implemented as a 12-layer Transformer, yielding an overall model size of approximately 100M parameters. For large-scale VLA models, we evaluate four representative architectural paradigms. OpenVLA-OFT-style methods regress continuous actions via action queries within autoregressive VLMs [26]. GR00T-style models condition an action expert on final-layer VLM features [4], while _π_ 0 variants explore tighter VLM–action coupling through multilayer conditioning [5]. DS-VLA adopts a dual-system design, where a fast System 1 executes actions at high frequency and a slower System 2 provides long-horizon contextual guidance [7, 15]. To ensure a fair comparison, we standardize the vision–language backbone across all large-scale models by replacing it with Qwen3-VL [1] (using the 2B variant unless otherwise specified) and adopting its native image encoder. Except for OFT, all large-scale models employ a shared flowmatching action head implemented as a 16-layer Transformer. As a result, all large-scale models have comparable capacity, with approximately 2.3B parameters each, enabling systematic evaluation of our method across diverse architectural designs. 

## _C. Theoretical Analysis_ 

This section analyzes the optimization behavior induced by the proposed T-MEE objective. We identify three fundamental properties that explain how T-MEE shapes error interactions, improves robustness to non-Gaussian noise, and induces structured coupling in multi-task learning scenarios. 

_1) Similarity-Weighted Interaction Between Trajectory Errors:_ T-MEE operates in error space by inducing structured interactions among action prediction errors through pairwise similarity. Let _{_ **e** _i}_<sup>_N_</sup> _i_ =1<sup>denote the set of trajectory-level action</sup> prediction errors. We define the Gaussian kernel measuring error similarity as: 


where _Z_ denotes the corresponding information potential. The T-MEE objective can be written compactly as _L_ T-MEE = _−_ log( _Z/N_<sup>2</sup> ). 

**_Proposition 1 (Similarity-Weighted Error Interaction)._** _Under the T-MEE objective, the negative gradient of each error sample induces a similarity-weighted interaction of the form:_ 


This result shows that T-MEE does not penalize errors independently. Instead, each error sample is attracted toward other 

errors in proportion to their similarity, leading to clustering behavior in error space. As a consequence, optimization under T-MEE regulates the collective geometry and entropy of the error distribution rather than merely reducing individual error magnitudes. The proof is provided in Appendix A. 

_2) Robustness to Non-Gaussian Noise and Outliers:_ Beyond shaping error geometry, T-MEE exhibits inherent robustness to non-Gaussian noise and outliers due to its distributionlevel formulation. 

**_Proposition 2 (Robustness via Higher-Order Statistics)._** _By minimizing R´enyi’s quadratic entropy, T-MEE implicitly optimizes higher-order statistics of the error distribution, making it less sensitive to non-Gaussian perturbations than quadratic regression losses._ The proof is provided in Appendix B. **_Proposition 3 (Bounded Influence of Outliers)._** _For an outlying error sample_ **e** _o far from the bulk of the error distribution, the gradient contribution induced by_ **e** _o under T-MEE is exponentially bounded. In particular,_ 


_where c denotes the normalized distance to other error samples._ In contrast to MSE, whose gradients grow linearly with error magnitude, the kernel-based weighting in T-MEE adaptively suppresses the influence of extreme deviations. As a result, the optimization dynamics are governed by the consensus structure of the error distribution rather than by isolated outliers. A full analysis is provided in Appendix C. 

_3) Interaction Structure in Multi-Task Settings:_ We analyze multi-task interaction under the T-MEE objective in the error space, where optimization dynamics are governed by the geometry of action prediction errors rather than task labels. **_Proposition 4 (Imbalance-Induced Task Coupling)._** _Consider two tasks A and B trained jointly under T-MEE. If their error distributions exhibit non-negligible overlap in error space, then sufficiently large sample imbalance causes the optimization of the minority task B to be dominated by crosstask interactions from the majority task A. Conversely, when cross-task overlap is negligible, tasks evolve independently regardless of their relative sample sizes._ 

Multi-task coupling under T-MEE is jointly governed by _task similarity_ in error space and _sample imbalance_ , and can be quantified by the coupling ratio 


which characterizes the relative strength of cross-task interactions acting on the minority task _B_ . When _RB ≫_ 1, task _B_ is dominated by majority-task errors, whereas _RB ≪_ 1 indicates effective decoupling. In benchmarks such as LIBERO, tasks sharing similar visual contexts and action primitives often exhibit substantial error-space overlap, and under severe data imbalance this leads to degraded performance on underrepresented tasks, consistent with our empirical observations. A formal analysis is provided in Appendix D. 

TABLE I 

PERFORMANCE ON LIBERO ACROSS DIFFERENT MODEL SCALES. WE EVALUATE 40 TASKS ACROSS FOUR SUITES, EACH WITH 50 TRIALS. RESULTS ARE 

REPORTED AS SUCCESS RATES. BEST RESULTS ARE BOLDED. 

|Params|Method|Spatial|Goal|Object|Long|Avg|
|---|---|---|---|---|---|---|
||BC-RNN [32]|40.0|8.2|11.0|0.8|15.0|
|20M|+ T-MEE|**50.4**|**36.8**|**21.0**|**4.8**|**28.3**|
|_<_|BC-Transformer [32]|69.6|68.4|57.4|14.8|52.6|
||+ T-MEE|**85.2**|**73.2**|**68.2**|**27.2**|**63.5**|
|100M|BC-DP [14]|65.6|79.2|91.2|**80.2**|79.1|
|_∼_|+ T-MEE|**72.6**|**82.4**|**92.6**|80.0|**81.9**|
||GR00T [4]|98.4|95.4|98.8|92.8|96.4|
||+ T-MEE|**98.8**|**96.2**|**99.4**|**93.4**|**97.0**|
||OFT [26]|98.8|93.6|98.4|91.2|95.5|
|2B|+ T-MEE|**99.0**|**96.8**|**99.2**|**92.8**|**97.0**|
|_>_|_π_0 [5]|99.4|96.4|98.6|92.8|96.8|
||+ T-MEE|**99.8**|**98.2**|**100.0**|**95.6**|**98.4**|
||DS-VLA [38]|98.2|96.4|99.2|89.2|95.8|
||+ T-MEE|**98.6**|**97.6**|**99.8**|**96.8**|**98.2**|


TABLE II 

PERFORMANCE OF DIFFERENT VLA ARCHITECTURES ACROSS 2B AND 4B BASE VLM SCALES ON THE SIMPLERENV-WIDOWX BENCHMARK. RESULTS ARE REPORTED AS SUCCESS RATES. BEST RESULTS ARE BOLDED. 

|||(a) 2B Base|VLM|||||(b) 4B Base|VLM|||
|---|---|---|---|---|---|---|---|---|---|---|---|
|Method|Put<br>Spoon|Put<br>Carrot|Stack<br>Cube|Put<br>Eggplant|Avg|Method|Put<br>Spoon|Put<br>Carrot|Stack<br>Cube|Put<br>Eggplant|Avg|
|GR00T [4]|87.5|54.2|12.5|45.8|50.0|GR00T [4]|83.3|33.3|12.5|83.3|53.1|
|+ T-MEE|66.7|50.0|16.7|83.3|**54.2**|+ T-MEE|75.0|45.8|16.7|95.8|**58.3**|
|OFT [26]|37.5|25.0|0.0|91.7|38.5|OFT [26]|20.8|33.3|12.5|95.8|40.6|
|+ T-MEE|29.2|8.3|25.0|95.8|**39.6**|+ T-MEE|45.8|33.3|4.2|83.3|**41.7**|
|_π_0 [5]|37.5|25.0|4.2|70.8|43.8|_π_0 [5]|70.8|33.3|16.7|91.7|53.1|
|+ T-MEE|62.5|41.7|16.7|62.5|**45.8**|+ T-MEE|79.2|41.7|33.3|91.7|**61.5**|
|DS-VLA [38]|58.3|54.2|12.5|70.8|49.0|DS-VLA [38]|75.0|29.2|16.7|83.3|51.0|
|+ T-MEE|62.5|58.3|25.0|79.2|**56.3**|+ T-MEE|75.0|45.8|12.5|91.7|**56.3**|


V. EXPERIMENTS 

## _A. Experiment Setup_ 

**Simulation Benchmark.** We evaluate our methods on two established benchmarks for robotic manipulation, LIBERO [32] and SimplerEnv [31]. We select four task suites from LIBERO, including Spatial, Goal, Object, and Long, each of which contains 10 single-arm manipulation tasks. For each suite, we report both suite-level success rates and the overall average, with 50 evaluation rollouts conducted per task. SimplerEnv is a real-to-sim benchmark designed to measure the generalization and robustness of manipulation policies trained on real-world demonstrations. We evaluate on four WidowX manipulation tasks and report per-task success rates along with the overall average, based on 24 rollouts per task. 

**Real-world Setup.** As shown in Figure 4, our real-world setup uses an Agilex Cobot Magic wheeled platform equipped with three RGB-D cameras. We consider three categories of manipulation tasks: placing a banana into the basket, wiping the whiteboard, and handing over a cup, along with one outof-distribution task that involves handing over a cup in the presence of visual distractors. For data collection, we record 100 demonstration trajectories per task category at 30 Hz. During evaluation, each task is executed for 12 rollout trials. 

## _B. Main Results under Near-Balanced Data_ 

**Simulation Experiments.** As shown in Table I, incorporating T-MEE consistently improves performance across all four suites. For small-scale models, including BC-RNN, BCTransformer, and BC-DP, T-MEE yields substantial gains, improving the average success rate by up to +13.3% for BCRNN and +10.9% for BC-Transformer. For large-scale VLA models, the improvements are more moderate but remain consistent, typically ranging from +0.5 to +2.4%. As these models already achieve near-saturated performance, the marginal gains from further reshaping action error distributions are naturally smaller. Overall, these results demonstrate that T-MEE remains effective even under near-balanced data regimes. 

**Real-world Robot Experiments.** We select GR00T N1.5 [4] as the baseline for real-world evaluation. During real-robot experiments, we observe that incorporating T-MEE leads to noticeably **more stable and accurate** action execution, reflected in smoother trajectories and fewer corrective motions. As shown in Figure 4, T-MEE consistently improves the success rate of GR00T in real-world settings, indicating that the distribution-level regularization induced by T-MEE generalizes beyond simulation benchmarks and transfers effectively to physical robotic systems. 

**Comparison of T-MEE Variants.** As shown in Figure 3, all three T-MEE variants consistently outperform the baseline 


Fig. 3. **Performance comparison of MEE-based variants on LIBERO.** We compare the baseline regression objective with three informationtheoretic variants, including T-MEE, Chunk-weighted T-MEE (Cw-TMEE), and Element-weighted T-MEE (Ew-TMEE). Results are reported for representative continuous-action VLA architectures. All MEE-based objectives consistently improve performance over the baseline, while different variants exhibit complementary advantages across architectures and task suites, highlighting the flexibility of distribution-level error shaping. 


Fig. 4. Real-world evaluation. (a) Real-world robotic setup and representative manipulation tasks. (b) Task success rates comparing GR00T and GR00T + T-MEE, showing consistent performance gains from T-MEE across all tasks. 

regression objective across multiple VLA architectures on LIBERO, demonstrating the effectiveness of distribution-level error supervision. Across architectures and evaluation suites, we find that the standard T-MEE objective accounts for most of the performance gains. While the weighted variants can provide additional improvements in certain settings, these gains are not consistent across models and tasks. In contrast, T-MEE exhibits robust performance across all architectures, indicating that T-MEE minimization alone is sufficient to effectively reshape action error distributions in practice. 

## _C. More Analyses_ 

**Few-Shot Learning.** We evaluate T-MEE under few-shot supervision by varying the training data ratio on the LIBERO benchmarks. As shown in Figure 6, T-MEE consistently improves success rates over the GR00T baseline across all task suites and data regimes, with more pronounced gains as the amount of training data decreases. These results indicate that 


Fig. 5. Average success rates of GR00T with and without T-MEE under different noise corruptions on LIBERO. 

T-MEE enhances data efficiency by providing distributionlevel supervision, enabling more robust learning from limited demonstrations. Additional few-shot results across different models are provided in Appendix H. 

**Robustness to Noises.** The preceding theoretical analysis suggests that MEE is inherently robust to non-Gaussian noise and outliers. Accordingly, we consider two types of image corruptions, motion blur and salt-and-pepper noise, as well as two types of action noise, namely Cauchy noise and impulse noise. Detailed noise definitions and additional experiments are provided in Appendix I. As shown in Figure 5, we finetune GR00T under each noise setting and evaluate performance on LIBERO. Across all noise types, incorporating T- MEE consistently improves the average success rate over the baseline. These results indicate that distribution-level supervision enhances robustness to corrupted observations and noisy demonstrations, providing a strong inductive bias for VLA training under noisy supervision. 

**Imbalanced Data Regimes.** Since each LIBERO suite con- 


Fig. 6. Radar plots comparing GR00T and GR00T + T-MEE under different few-shot ratios. Each subplot reports success rates across the four LIBERO task suites and the overall average. As the amount of training data decreases, T-MEE consistently improves performance across task suites, with more pronounced gains in low-data regimes, indicating enhanced data efficiency and robustness to limited supervision. 


yet T-MEE continues to improve performance when evaluated on dominant tasks, suggesting that the benefits of T-MEE can manifest even when long-tail tasks are under-represented or not directly evaluated. Additional results under imbalanced data regimes are provided in Appendix J. 

Fig. 7. Success rates of GR00T with and without T-MEE under different imbalance ratios on LIBERO. 

**Error Analysis of One Trajectory.** As shown in Figure 1, we observe a distinct behavior in small models. Action prediction errors at early timesteps exhibit pronounced outliers, whereas the aggregated error distribution over the full trajectory remains relatively compact and centered near zero. Despite these early outliers, the model attains a higher overall success rate. We attribute this phenomenon to limited model capacity. In the initial acceleration or initialization phase of the trajectory, smaller models may struggle to precisely predict action magnitudes, resulting in large instantaneous errors while still capturing correct directional trends. In contrast, larger models do not exhibit this behavior. Their action errors remain tightly clustered throughout the trajectory, reflecting more consistent action execution and correspondingly higher task success. **Error Entropy Visualizations.** Figure 8 visualizes the evolution of action error entropy during training. Since T-MEE is introduced after 10k training steps, the two curves largely overlap in the early stage. After T-MEE is activated, the entropy under T-MEE decreases more rapidly and converges to a lower level compared to the baseline. This indicates that trajectory-level MEE effectively reshapes the error distribution once applied, leading to more compact and stable action errors. Additional analyses are provided in Appendix K. 

sists of ten tasks with relatively balanced demonstrations, we construct imbalanced training regimes by assigning 40 demonstrations to five tasks as the majority group, while progressively reducing the remaining five tasks to 10, 4, and 1 demonstration, corresponding to imbalance ratios of 4, 10, and 40, respectively. As shown in Figure 7, we evaluate GR00T under varying degrees of task-level data imbalance. Under mild to moderate imbalance, incorporating T-MEE consistently improves performance across all task suites. However, when the imbalance becomes extreme, corresponding to an imbalance ratio of 40, the benefits of T-MEE diminish and may no longer hold. This observation is consistent with our theoretical analysis, indicating that while T-MEE effectively mitigates moderate task imbalance by reshaping error distributions, its robustness has a practical limit when supervision for minority tasks becomes severely insufficient. These results characterize the effective operating range of T-MEE under imbalanced data regimes. Notably, when evaluation focuses primarily on dominant tasks and does not explicitly probe long-tail tasks with very few demonstrations, performance gains can still be observed. As shown in Table II, experiments on SimplerEnv further support this phenomenon. The Bridge dataset in SimplerEnv follows a highly long-tailed distribution, 

## VI. CONCLUSION 

We revisit action regression objectives for VLA models from an information-theoretic perspective and propose trajectory-level Minimum Error Entropy with two weighted variants. By reshaping action error distributions beyond pointwise regression, T-MEE promotes compact and structured errors without assuming a predefined parametric form. Experiments on simulation benchmarks and real-robot tasks demonstrate consistent improvements under standard, fewshot, noisy, and moderately imbalanced settings, with negligible training overhead. These results underscore the effectiveness of distribution-level supervision for enhancing robustness and data efficiency in continuous-action VLA models. 

## REFERENCES 

- [1] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao, Chunjiang Ge, et al. Qwen3-vl technical report, 2025a. _URL https://arxiv. org/abs/2511.21631_ , 2025. 

- [2] Shuanghao Bai, Wenxuan Song, Jiayi Chen, Yuheng Ji, Zhide Zhong, Jin Yang, Han Zhao, Wanqi Zhou, Wei Zhao, Zhe Li, et al. Towards a unified understanding of robot manipulation: A comprehensive survey. _arXiv preprint arXiv:2510.10903_ , 2025. 

- [3] Shuanghao Bai, Wanqi Zhou, Pengxiang Ding, Wei Zhao, Donglin Wang, and Badong Chen. Rethinking latent redundancy in behavior cloning: An information bottleneck approach for robot manipulation. In _Forty-second International Conference on Machine Learning_ , 2025. 

- [4] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [5] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _pi_ <u>0:</u> A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [6] Alexei Botchkarev. Performance metrics (error measures) in machine learning regression, forecasting and prognostics: Properties and typology. _arXiv preprint arXiv:1809.03006_ , 2018. 

- [7] Qingwen Bu, Hongyang Li, Li Chen, Jisong Cai, Jia Zeng, Heming Cui, Maoqing Yao, and Yu Qiao. Towards synergistic, generalized, and efficient dual-system for robotic manipulation. _arXiv preprint arXiv:2410.08001_ , 2024. 

- [8] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. In _Robotics: Science and Systems_ , 2025. 

- [9] Badong Chen, Yu Zhu, and Jinchun Hu. Mean-square convergence analysis of adaline training with minimum 

error entropy criterion. _IEEE transactions on neural networks_ , 21(7):1168–1179, 2010. 

- [10] Badong Chen, Zejian Yuan, Nanning Zheng, and Jos´e C Pr´ıncipe. Kernel minimum error entropy algorithm. _Neurocomputing_ , 121:160–169, 2013. 

- [11] Badong Chen, Lei Xing, Bin Xu, Haiquan Zhao, and Jose C Principe. Insights into the robustness of minimum error entropy estimation. _IEEE transactions on neural networks and learning systems_ , 29(3):731–737, 2016. 

- [12] Badong Chen, Lei Xing, Nanning Zheng, and Jose C Principe. Quantized minimum error entropy criterion. _IEEE transactions on neural networks and learning systems_ , 30(5):1370–1380, 2018. 

- [13] Badong Chen, Lujuan Dang, Yuantao Gu, Nanning Zheng, and Jos´e C Pr´ıncipe. Minimum error entropy kalman filter. _IEEE Transactions on Systems, Man, and Cybernetics: Systems_ , 51(9):5819–5829, 2019. 

- [14] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

- [15] Can Cui, Pengxiang Ding, Wenxuan Song, Shuanghao Bai, Xinyang Tong, Zirui Ge, Runze Suo, Wanqi Zhou, Yang Liu, Bofang Jia, et al. Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation. _arXiv preprint arXiv:2505.03912_ , 2025. 

- [16] Lujuan Dang, Badong Chen, Shiyuan Wang, Wentao Ma, and Pengju Ren. Robust power system state estimation with minimum error entropy unscented kalman filter. _IEEE Transactions on Instrumentation and Measurement_ , 69(11):8797–8808, 2020. 

- [17] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. In _Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers)_ , pages 4171–4186, 2019. 

- [18] Deniz Erdogmus and Jose C Principe. An error-entropy minimization algorithm for supervised training of nonlinear adaptive systems. _IEEE Transactions on Signal Processing_ , 50(7):1780–1786, 2002. 

- [19] Yiguo Fan, Shuanghao Bai, Xinyang Tong, Pengxiang Ding, Yuyang Zhu, Hongchao Lu, Fengqi Dai, Wei Zhao, Yang Liu, Siteng Huang, et al. Long-vla: Unleashing long-horizon capability of vision language action model for robot manipulation. In _Conference on Robot Learning_ , pages 2018–2037. PMLR, 2025. 

- [20] Dibya Ghosh, Homer Rich Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, et al. Octo: An opensource generalist robot policy. In _Robotics: Science and Systems_ , 2024. 

- [21] Jiacheng He, Gang Wang, Kui Cao, He Diao, Guotai 

Wang, and Bei Peng. Generalized minimum error entropy for robust learning. _Pattern Recognition_ , 135:109188, 2023. 

- [22] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 770–778, 2016. 

- [23] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: A vision-language-action model with open-world generalization. In _Conference on Robot Learning_ , 2025. 

- [24] Aryan Jadon, Avinash Patil, and Shruti Jadon. A comprehensive survey of regression-based loss functions for time series forecasting. In _International Conference on Data Management, Analytics & Innovation_ , pages 117– 147. Springer, 2024. 

- [25] Martin Janzura, Timo Koski, and Antonin Ot´ahal. Minimum entropy of error principle in estimation. _Information sciences_ , 79(1-2):123–144, 1994. 

- [26] Moo Jin Kim, Chelsea Finn, and Percy Liang. Finetuning vision-language-action models: Optimizing speed and success. In _Robotics: Science and Systems_ , 2025. 

- [27] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, et al. Openvla: An open-source vision-language-action model. In _Conference on Robot Learning_ , pages 2679–2713. PMLR, 2025. 

- [28] Hao Li, Shuai Yang, Yilun Chen, Yang Tian, Xiaoda Yang, Xinyi Chen, Hanqing Wang, Tai Wang, Feng Zhao, Dahua Lin, et al. Cronusvla: Transferring latent motion across time for multi-frame prediction in manipulation. In _Proceedings of the AAAI conference on artificial intelligence_ , 2026. 

- [29] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- [30] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- [31] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Oier Mees, Karl Pertsch, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. In _Conference on Robot Learning_ , pages 3705–3728. PMLR, 2025. 

- [32] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances_ 

_in Neural Information Processing Systems_ , 36:44776– 44791, 2023. 

- [33] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin ElNouby, et al. Dinov2: Learning robust visual features without supervision. _Transactions on Machine Learning Research Journal_ , pages 1–31, 2024. 

- [34] Jose Principe and John Iii. Information-theoretic learning. _Advances in unsupervised adaptive filtering_ , 09 2000. 

- [35] Alfr´ed R´enyi. On measures of entropy and information. In _Proceedings of the fourth Berkeley symposium on mathematical statistics and probability, volume 1: contributions to the theory of statistics_ , volume 4, pages 547–562. University of California Press, 1961. 

- [36] Moritz Reuss, Omer<sup>¨</sup> Erdinc¸ Ya˘gmurlu, Fabian Wenzel, and Rudolf Lioutikov. Multimodal diffusion transformer: Learning versatile behavior from multimodal goals. _Robotics: Science and Systems XX. Ed.: D. Kulic_ , 2024. 

- [37] Claude E Shannon. A mathematical theory of communication. _The Bell system technical journal_ , 27(3):379–423, 1948. 

- [38] starVLA Contributors. Starvla: A lego-like codebase for vision-language-action model developing. GitHub repository, 1 2025. URL https://github.com/starVLA/starVLA. 

- [39] GA Team et al. Gen-0: Embodied foundation models that scale with physical interaction. _Generalist AI Blog_ , 2025. 

- [40] A Vaswani. Attention is all you need. _Advances in Neural Information Processing Systems_ , 2017. 

- [41] Yating Wang, Haoyi Zhu, Mingyu Liu, Jiange Yang, HaoShu Fang, and Tong He. Vq-vla: Improving visionlanguage-action models via scaling vector-quantized action tokenizers. _arXiv preprint arXiv:2507.01016_ , 2025. 

- [42] Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, et al. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. In _Proceedings of the AAAI conference on artificial intelligence_ , 2026. 

- [43] Yuqing Xie, Yingsong Li, Yuantao Gu, Jiuwen Cao, and Badong Chen. Fixed-point minimum error entropy with fiducial points. _IEEE Transactions on Signal Processing_ , 68:3824–3833, 2020. 

- [44] Yang Zhang, Chenwei Wang, Ouyang Lu, Yuan Zhao, Yunfei Ge, Zhenglong Sun, Xiu Li, Chi Zhang, Chenjia Bai, and Xuelong Li. Align-then-steer: Adapting the vision-language action models through unified latent guidance. _arXiv preprint arXiv:2509.02055_ , 2025. 

- [45] Wei Zhao, Pengxiang Ding, Zhang Min, Zhefei Gong, Shuanghao Bai, Han Zhao, and Donglin Wang. Vlas: Vision-language-action model with speech instructions for customized robot manipulation. In _The Thirteenth International Conference on Learning Representations_ , 

2025. 

- [46] Wanqi Zhou, Shuanghao Bai, Yuqing Xie, Yicong He, Qibin Zhao, and Badong Chen. An information-theoretic approach for heterogeneous differentiable causal discovery. _Neural Networks_ , 188:107417, 2025. 

- [47] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

APPENDIX 

## _A. Proof of Proposition 1_ 


Considering the summation _Z_ =<sup>�</sup> _a_ � _b_<sup>_kab_, the gradient</sup><sup>_∇_</sup><sup>**e**</sup> _i_<sup>_Z_only involves terms where the index</sup><sup>_a_=</sup><sup>_i_or</sup><sup>_b_=</sup><sup>_i_. Exploiting</sup> the symmetry of the Gaussian kernel ( _kij_ = _kji_ ), we obtain: 


Substituting this result into the gradient of the loss and negating the sign yields the force **F** _i_ : 


This formulation reveals that each error **e** _i_ is “pulled” toward other errors **e** _j_ with a strength proportional to their similarity _kij_ , fostering a global clustering effect in the error space. 

## _B. Proof of Proposition 2_ 

_Proof:_ To analyze the statistical structure of the T-MEE objective, we consider a Taylor expansion of the information potential 


with respect to the kernel bandwidth _σ_ . For sufficiently large _σ_ and any finite truncation order _n ≥_ 2, the exponential can be expanded as 


Substituting _x_ and summing over ( _t, s_ ) gives 


In particular, the first two non-constant terms can be written explicitly as 


The leading non-constant term recovers the MSE structure. Using the identity 


we see that minimizing the second-order term is equivalent to minimizing the empirical MSE loss. 

The higher-order terms with _k ≥_ 2 depend on<sup>�</sup> _t,s_<sup>_∥et−es∥_2</sup><sup>_k_andarethereforesensitivetohigher-ordermoments</sup> (e.g., kurtosis) and heavy-tailed structure in the error distribution. While a pure MSE objective only controls the secondorder moment, the T-MEE objective incorporates these higher-order contributions, penalizing large pairwise deviations and encouraging trajectory errors to concentrate in a compact region of the error manifold, thereby suppressing stochastic outliers. 

## _C. Proof of Proposition 3_ 

_Consider an outlying error sample_ **e** _o far from the consensus, i.e., ∥_ **e** _o −_ **e** _j∥≥ cσ for all j̸_ = _o with c ≫_ 1 _. The gradient contribution induced by_ **e** _o is exponentially bounded, ensuring the stability of the optimization:_ 


Robustness is manifested through the _adaptive importance weights kij_ within the gradient expression. In standard MSE, the gradient _∇L_ MSE _∝_ ( **e** _o −_ **e** _j_ ) grows linearly with the error magnitude, allowing a single outlier to dominate the parameter updates (the ”leverage point” effect). In contrast, within the T-MEE framework, as the distance _∥_ **e** _o−_ **e** _j∥_ increases, the Gaussian kernel _koj_ decays exponentially. For _c ≫_ 1, the product _koj∥_ **e** _o −_ **e** _j∥_ vanishes after reaching a finite maximum, effectively ”rejecting” the outlier. Consequently, the optimization trajectory remains governed by the consensus of the error distribution rather than extreme values. 

## _D. Proof of Proposition 4_ 

In this section, we provide a formal analysis of the interaction structure induced by the T-MEE objective in multi-task learning settings, and derive the coupling criterion stated in Proposition 4. 

_a) Setup:_ Consider two task groups _A_ and _B_ , with _NA_ and _NB_ error samples, respectively. Let **e** _i_ denote an error sample, and let 


denote the Gaussian kernel similarity between error samples _i_ and _j_ . Recall that the T-MEE objective is defined as 


## where _N_ = _NA_ + _NB_ . 

_b) Within- and cross-task interaction scaling:_ We analyze the optimization dynamics acting on an error sample **e** _i_ belonging to task _B_ . From the gradient expression of T-MEE, the force acting on **e** _i_ is proportional to a similarity-weighted sum over all other error samples. This interaction naturally decomposes into two components: (i) within-task interactions with other samples from task _B_ , and (ii) cross-task interactions with samples from task _A_ . To characterize their relative strength, we define the empirical average kernel similarities: 


For an error sample **e** _i ∈ B_ , the expected magnitude of within-task interactions scales as _O_ � _NB k_<sup>¯</sup> _BB_ �, while the expected magnitude of cross-task interactions scales as _O_ � _NA k_<sup>¯</sup> _AB_ �. These scalings reflect the fact that each error sample interacts with all other samples, weighted by their kernel similarity. 

_c) Coupling criterion:_ Comparing the two interaction terms, the relative strength of cross-task interactions acting on task _B_ is characterized by the ratio 


where the factor of 2 accounts for symmetric cross-task contributions arising from pairs ( _i, j_ ) _∈ A × B_ and ( _i, j_ ) _∈ B × A_ in the kernel aggregation. 

When _RB ≫_ 1, cross-task interactions from task _A_ dominate the optimization dynamics of task _B_ , causing the minority task to be strongly coupled to the majority task. In contrast, when _RB ≪_ 1, within-task interactions dominate and task _B_ evolves largely independently. This establishes that multi-task coupling under T-MEE is jointly governed by sample imbalance and the overlap of error distributions in error space, as reflected by the kernel similarity ratio _k_<sup>¯</sup> _AB/k_<sup>¯</sup> _BB_ . 

_d) Relation to kernel aggregation.:_ For completeness, the kernel aggregation term admits the exact decomposition 


where _k_<sup>¯</sup> _AA_ denotes the average within-task similarity for task _A_ . This decomposition makes explicit how within-task and crosstask interactions contribute to the overall information potential, but the coupling behavior of individual tasks are governed by the relative scaling captured by Equation (27). 

## _E. Additional Related Work of Minimum Error Entropy_ 

Minimum Error Entropy (MEE) was originally introduced in the early 1990s as an estimation principle based on minimizing the entropy of the error distribution by Janzura et al. [25]. It was later developed into a learning criterion within the informationtheoretic learning framework by Principe and collaborators [18, 34], and subsequently further advanced in the context of robust learning and signal processing [9]. Prior work has established important theoretical properties of MEE, including its convergence behavior [9, 43] and robustness to non-Gaussian noise and outliers [11, 13, 16, 21, 46]. By directly operating on the error distribution, MEE is more sensitive to higher-order statistical characteristics of the error signal, such as heavy tails and peakedness, and provides more stable gradient directions when noise deviates from Gaussian assumptions. The computational complexity of MEE has also been studied extensively [10, 12]. Early work emphasized the quadratic complexity induced by kernel-based entropy estimation, particularly in online learning and adaptive filtering settings where model capacity was limited and the loss computation dominated the overall cost. In contrast, in modern large-scale Vision–Language–Action models, the computational overhead of MEE-based objectives becomes negligible relative to the dominant cost of deep representation learning and action generation. When implemented with GPU-parallelized tensor operations over mini-batches or trajectories, the additional cost introduced by MEE is effectively amortized by the forward and backward passes of the backbone network. As a result, in the regime of large-scale VLA models, the primary challenge of applying MEE is no longer computational feasibility, but how to properly structure error interactions and integrate distribution-level supervision with modern action generation objectives. 

## _F. Implementation Details_ 

## _1) Simulation Experiments:_ 

_a) Small-scale VLA models:_ We evaluate T-MEE on three representative small-scale behavior cloning models, including BC-DP, BC-RNN, and BC-Transformer. All models share the same visual encoder, language processing pipeline, data augmentation strategy, and evaluation protocol, while differing in temporal modeling and action head architectures. 

**Shared Settings.** All small-scale models share the same visual encoder, language processing pipeline, data augmentation strategy, and training protocol. Specifically, we use a ResNet-based image encoder with the last four layers removed, trained from scratch without pretrained weights or frozen parameters. Models are trained for 50 epochs with a batch size of 128 on a single A100 GPU, using the AdamW optimizer with a learning rate of 1 _×_ 10<sup>_−_4</sup> , _β_ = (0 _._ 9 _,_ 0 _._ 999), and weight decay 1 _×_ 10<sup>_−_4</sup> . Visual observations include agent-view and eye-in-hand RGB images at a resolution of 128 _×_ 128, together with gripper and joint states. Language instructions are encoded using a BERT-based tokenizer and fused into the visual stream via FiLM conditioning. All models are evaluated over 50 rollout episodes per task. 

TABLE III 

SHARED SETTINGS FOR SMALL-SCALE VLA MODELS. 

|**Category**|**Configuration**|
|---|---|
|Image Encoder|ResNet, last 4 layers removed, trained from scratch|
|Image Resolution|128_×_128 (agent-view, eye-in-hand)|
|Language Encoder|BERT tokenizer, max length 25|
|Language Fusion|FiLM conditioning<br>|
|Optimizer|AdamW (1_×_10<sup>_−_4</sup>, _β_ = (0_._9_,_0_._999))<br>|
|Weight Decay|1_×_10<sup>_−_4</sup>|
|Batch Size|128|
|Training Epochs|50|
|Hardware|Single NVIDIA A100 GPU|
|Data Augmentation|Brightness/contrast/saturation/hue (0.3), noise _ϵ_= 0_._1|
|Evaluation|50 rollouts per task (LIBERO)|


**MEE-based Settings.** During training, we adopt a two-phase optimization strategy. In the first one-third of the total training steps, we optimize the model using only the MSE objective to stabilize the action error distribution. In the remaining two-thirds of training, we activate the MEE-based objectives. For T-MEE, the kernel bandwidth _σ_ is fixed to 0 _._ 5, and the loss weight _α_ is selected from _{_ 0 _._ 01 _,_ 0 _._ 1 _,_ 1 _._ 0 _}_ . For the weighted variants, Cw-TMEE and Ew-TMEE, all hyperparameters follow the T-MEE setting, with the additional bandwidth parameter _σw_ also fixed to 0 _._ 5. 

**BC-DP.** The BC-DP model adopts a diffusion-based action head with a DiT-B backbone. The diffusion head operates on tokens of dimension 64, predicts 7-dimensional actions, and models a future action window of 9 steps (corresponding to an action chunk length of 10), with 8 repeated diffusion steps. Temporal dependencies are modeled using a 4-layer transformer with 6 attention heads and a maximum sequence length of 10. For T-MEE, the kernel bandwidth is fixed to _σ_ = 0 _._ 5, while the MEE loss weight is set to 0.01 for spatial and object tasks, and 0.1 for goal and long-horizon tasks. 

**BC-RNN.** The BC-RNN model employs a two-layer unidirectional RNN with a hidden size of 1024 to capture temporal dependencies. Actions are predicted using a two-layer MLP head with a hidden size of 1024. The kernel bandwidth is set 

to _σ_ = 0 _._ 5 for all task suites. The T-MEE loss weight is set to 1.0 for spatial, goal, and long-horizon tasks, and 0.1 for object-centric tasks. 

**BC-Transformer.** The BC-Transformer model uses the same temporal transformer configuration as BC-DP, consisting of 4 layers, 6 attention heads, and a maximum sequence length of 10. Action prediction is performed using a two-layer MLP head with a hidden size of 1024. For T-MEE, the kernel bandwidth is fixed to _σ_ = 0 _._ 5, and the MEE loss weight follows the same setting as BC-RNN, with higher weights for spatial, goal, and long-horizon tasks, and a lower weight for object-centric tasks. 

_2) Large-scale VLA models:_ All large-scale models share the same training protocol and optimization settings unless otherwise specified. We use separate learning rates for the vision–language backbone and the action model, and train all models with a unified optimizer, scheduler, batch size, and training budget. The number of training steps and action chunk length differ between LIBERO and SimplerEnv. For models equipped with an action head (except OFT), we adopt a diffusionbased action model with a DiT-B backbone. Detailed configurations are summarized in Table IV. 

### TABLE IV 

SHARED TRAINING AND ARCHITECTURE SETTINGS FOR LARGE-SCALE VLA MODELS. 

|**Category**|**Configuration**|
|---|---|
|Optimizer|AdamW (_β_ = (0_._9_,_0_._95), _ϵ_= 1_×_10<sup>_−_8</sup>, weight decay 1_×_10<sup>_−_8</sup>)<br>|
|Learning Rate|1_×_10<sup>_−_5 </sup>(VLM), 1_×_10<sup>_−_4 </sup>(action expert)<br>|
|LR Scheduler|Cosine with minimum LR 1_×_10<sup>_−_6</sup>|
|Warm-up Steps|5k steps|
|Training Steps|30k (LIBERO), 40k (SimplerEnv)|
|Batch Size|128 (8 GPUs _×_ 16 samples per GPU)|
|Action Chunk Length|8 (LIBERO), 16 (SimplerEnv)|
|Action Head Type|Diffusion-based (DiT-B), except OFT|
|Diffusion Steps|4 repeated steps, 1000 timestep buckets|
|DiT Backbone|16 layers, 12 heads, head dim 64, input dim 768|
|Cross-Attention Dim|2048|
|Dropout|0.2 (final-layer dropout enabled)|
|Action Hidden Dim|1024|
|Evaluation|50 rollouts per task (LIBERO), 24 rollouts per task (SimplerEnv)|


**GR00T** conditions the action expert on the final-layer vision-language features produced by the backbone, using these features as the sole conditioning signal for action generation. 

**PI** conditions the action expert on multi-layer VL features, aggregating representations from multiple backbone layers rather than relying only on the final-layer output. 

**DS-VLA** similarly conditions the action expert on the final-layer VL features. In addition, the image encoder used in its System 1 branch is DINOv2-ViT-S/14 [33]. 

**OFT** augments the VLA backbone by appending learnable tokens corresponding to the action chunk length multiplied by the action dimensionality. These tokens are jointly optimized with the backbone to directly model temporally chunked action representations. 

_3) Real-world Experiments:_ We adopt a single baseline, namely the original GR00T N1.5 [4] implementation with its default architecture and a continuous-action flow-matching head. 

**Shared Settings.** For real-robot experiments, we train GR00T with an action chunk size of _K_ = 25 and batch size 128 on a single H100 GPU. We follow the recommended optimization hyperparameters, using AdamW with a learning rate 1 _×_ 10<sup>_−_4</sup> , weight decay 1 _×_ 10<sup>_−_5</sup> , and a warmup ratio of 0.05 of the total training steps. Consistent with the original setup, we freeze both the language model backbone and the vision tower, and fine-tune only the projector and diffusion policy head. 

**MEE-based Settings.** During training, we adopt a two-phase optimization strategy with a total of 10k training steps. In the first one-third of the training process, the model is optimized using only the MSE objective to stabilize the action error distribution. In the remaining two-thirds of training, we activate the MEE-based objectives. For T-MEE, the kernel bandwidth _σ_ is fixed to 0 _._ 5, and the loss weight _α_ is set to 1 _._ 0. 

## _G. Additional Experiments with Original GR00T N1.5 Models_ 

We further evaluate T-MEE on the original GR00T N1.5 models [4] without architectural or training modifications. As shown in Table V, incorporating T-MEE consistently improves performance across all LIBERO task suites, leading to a higher overall average success rate. These results demonstrate that the effectiveness of T-MEE is not limited to re-trained or modified backbones, but also extends to strong off-the-shelf VLA models. This further confirms the general applicability of T-MEE as a lightweight and architecture-agnostic supervision objective. 

## _H. Additional Experiments with Few-shot Learning Across Models_ 

Table VI presents few-shot evaluation results on LIBERO under a fixed training ratio of 0.2 across multiple VLA architectures. Across all models, incorporating T-MEE consistently improves the overall average success rate, demonstrating that the benefits 

TABLE V 

PERFORMANCE COMPARISON ON LIBERO WITH ORIGINAL GR00T N1.5. RESULTS ARE REPORTED AS SUCCESS RATES. 

|Method|Spatial|Goal|Object|Long|Avg|
|---|---|---|---|---|---|
|GR00T N1.5 [4]|93.4|85.0|89.4|78.4|86.6|
|+ T-MEE|**93.8**|**87.2**|**93.2**|**80.4**|**88.7**|


### TABLE VI 

FEW-SHOT EVALUATION ON LIBERO UNDER A 0.2 TRAINING RATIO. SUCCESS RATES (%) ARE REPORTED FOR EACH TASK SUITE AND THE OVERALL AVERAGE ACROSS DIFFERENT VLA ARCHITECTURES. 

|Method|Spatial|Goal|Object|Long|Avg|
|---|---|---|---|---|---|
|BC-Transformer [32]|42.4|51.0|57.6|8.8|40.0|
|+ T-MEE|**48.6**|**57.4**|**67.6**|**9.4**|**45.8**|
|GR00T [4]|**85.0**|77.2|94.4|53.0|77.4|
|+ T-MEE|84.8|**79.0**|**97.8**|**60.2**|**80.5**|
|OFT [26]|93.4|86.4|92.0|58.4|82.6|
|+ T-MEE|**93.4**|**88.0**|**96.4**|**59.6**|**84.4**|
|_π_0 [5]|90.4|77.2|93.6|61.6|80.7|
|+ T-MEE|**92.4**|**82.4**|**96.0**|**63.2**|**83.5**|
|DS-VLA [38]|77.4|74.6|89.0|54.4|73.9|
|+ T-MEE|**81.0**|**76.8**|**96.6**|**55.0**|**77.4**|


of T-MEE are not tied to a specific backbone or action head. These results further confirm that T-MEE serves as a generally applicable, architecture-agnostic supervision objective that enhances data efficiency in few-shot learning settings. 

_I. Additional Experiments with Noise Across Models_ 

_1) Noise Types in Our Study:_ We consider four types of noise to evaluate robustness under corrupted supervision, including two image-level corruptions and two action-level noise models. 

_a) Image-level Noise:_ We follow the experimental setup of [28] for image-level noise injection. Specifically, **motion blur** is applied using a horizontal linear kernel with size _k_ = 5. For **salt-and-pepper (SAP) noise** , a fraction of 0 _._ 2 of image pixels is corrupted, with equal probability assigned to salt and pepper noise. **Gaussian noise** is added with a standard deviation of 10 _._ 0. We next describe the three types of image-level noise considered in our experiments. 

**Motion Blur** simulates camera or object motion during image acquisition. We apply a linear motion blur by convolving the input image with a normalized directional kernel of fixed size. This corruption primarily degrades spatial details while preserving global structure, and represents common observation noise in real-world robotic perception. **Salt-and-pepper (SAP) noise** randomly replaces a subset of image pixels with extreme values. This corruption introduces sparse but high-magnitude perturbations, leading to impulsive outliers in the visual observation space. SAP noise is commonly used to model sensor faults or transmission errors. **Gaussian Noise** adds zero-mean Gaussian perturbations to image intensities. Unlike SAP noise, which produces sparse and extreme outliers, Gaussian noise induces dense but small-magnitude deviations and serves as a standard baseline for modeling observation noise under Gaussian assumptions. We visualize these three noise types in Figure 9. 


_b) Action-level Noise:_ Action-level noise perturbs the continuous action commands directly in the action space, modeling execution-time disturbances such as actuator uncertainty, control jitter, or occasional command corruption. Formally, given a clean action **a** _∈_ R<sup>_d_</sup> , action-level noise produces a corrupted action **a** ˜ by adding stochastic perturbations to **a** . In our experiments, we consider two representative types of action-level noise: _Cauchy noise_ , which introduces continuous heavytailed perturbations, and _impulse noise_ , which produces sparse but extreme outliers. 

**Cauchy Noise** is added to continuous action values by sampling from a Cauchy distribution. Given a clean action **a** _∈_ R<sup>_d_</sup> , the corrupted action is defined as 


where _γ_ denotes the scale parameter. In our experiments, we set _γ_ = 0 _._ 02. Due to its heavy-tailed nature and undefined variance, Cauchy noise induces frequent large-magnitude perturbations, serving as a representative non-Gaussian noise model for action corruption. The sampled noise is truncated to a bounded range in practice. 

**Impulse Noise** corrupts actions by injecting large deviations with a small probability. Specifically, the corrupted action is given by 


where **_δ_** is sampled from a zero-mean distribution with large variance. In our implementation, the impulse probability is set to _p_ = 0 _._ 05. Unlike Cauchy noise, which is continuously heavy-tailed, impulse noise produces sparse but extreme outliers, modeling occasional execution failures or actuator glitches. 

_2) Additional Experiments:_ We further evaluate robustness by directly testing models on noisy observations without any noise-specific fine-tuning. As shown in Figure 10, adding T-MEE consistently improves performance across different VLA architectures under both Gaussian and SAP noise. Notably, the gains are more pronounced under SAP noise, which introduces sparse and high-magnitude perturbations. This suggests that T-MEE enhances inherent robustness to outliers and non-Gaussian corruptions, even in the absence of explicit noise exposure during training. Overall, these results indicate that T-MEE improves zero-shot robustness to observation noise by shaping action error distributions in a noise-agnostic manner. 


Fig. 10. Performance under image-level noise without noise-specific training on LIBERO. Evaluation is conducted by directly testing models on noisy observations. T-MEE improves robustness across different architectures, particularly under salt-and-pepper noise. 

## _J. Additional Experiments with Imbalance Across Models_ 

Table VII reports performance under a fixed imbalance ratio of 0.25 across multiple VLA architectures. Across all evaluated models, incorporating T-MEE consistently improves the overall average success rate compared to the corresponding baselines. The gains are observed across different task suites, including spatial, goal-oriented, object-centric, and long-horizon tasks, indicating that the benefits of T-MEE are not restricted to a specific architecture or task type. These results further demonstrate that T-MEE provides a generally effective supervision signal under moderate task-level imbalance. Combined with the main text analysis, they also suggest that the effectiveness of T-MEE holds within a practical range of imbalance, while extreme imbalance remains a challenging regime. 

## _K. Additional Analysis Experiments_ 

_1) Hyperparameter Sensitivity:_ Figure 11 analyzes the sensitivity of T-MEE to its key hyperparameters. Overall, performance remains stable across a wide range of the loss weight _α_ in Equation 9 and the kernel bandwidth _σ_ in Equation 6. While extreme values lead to mild performance degradation, intermediate settings consistently yield strong results. These findings indicate that T-MEE does not require precise hyperparameter tuning and admits a broad and stable operating regime in practice. 

TABLE VII 

PERFORMANCE ON LIBERO UNDER AN IMBALANCE RATIO OF 0.25. RESULTS ARE REPORTED AS SUCCESS RATES. BEST RESULTS WITHIN EACH 

METHOD BLOCK ARE BOLDED. 

|Method<br>Spatial|Goal|Object|Long<br>Avg|
|---|---|---|---|
|BC-Transformer [32]<br>65.6|62.4|44.8|12.4<br>46.3|
|+ T-MEE<br>**66.4**|**67.8**|**50.2**|**14.2**<br>**49.7**|
|GR00T [4]<br>95.6|84.6|98.6|74.6<br>88.4|
|+ T-MEE<br>**95.8**|**86.2**|**99.4**|**78.2**<br>**89.9**|
|OFT [26]<br>96.6|86.6|95.8|79.2<br>89.6|
|+ T-MEE<br>**98.0**|**89.2**|**96.0**|**82.4**<br>**91.4**|
|_π_0 [5]<br>97.6|85.2|99.4|78.4<br>90.2|
|+ T-MEE<br>**97.8**|**86.2**|**99.4**|**84.2**<br>**91.9**|
|DS-VLA [38]<br>89.6|84.2|99.0|80.4<br>88.3|
|+ T-MEE<br>**96.6**|**84.8**|**99.4**|**81.4**<br>**90.6**|
|(a) Sensitivity to𝛼𝛼<br>f T-MEE hyperparameters. (a) Sens<br>tLIBER|itivity to the lo<br>|ss weight|(b) Sensitivity to𝜎𝜎<br> _α_ in Equation 9. (b) Sensi|


Fig. 11. Sensitivity analysis of T-MEE hyperparameters. (a) Sensitivity to the loss weight _α_ in Equation 9. (b) Sensitivity to the kernel bandwidth _σ_ in Equation 6. Results are reported as average success rates on LIBERO. 

_2) Training Overhead:_ Early studies on MEE in the 2010s primarily focused on improving its computational efficiency to enable practical deployment under limited hardware resources. In modern training regimes, however, this concern has largely diminished due to advances in GPU hardware and the substantially increased cost of large-scale model training and data loading. In our experiments, the additional computational overhead introduced by T-MEE is negligible. On LIBERO, we measure the per-iteration forward and backward pass time on a single NVIDIA H100 GPU to be approximately 0.59 seconds both with and without T-MEE, with no observable difference between the two settings. In practice, overall training time is dominated by model execution, data loading, and system-level resource scheduling, rather than the entropy-based loss computation itself. These results indicate that T-MEE incurs essentially no additional training cost in modern VLA training pipelines. 

## _L. Limitations_ 

While our method consistently improves performance across a range of VLA architectures and data regimes, it also introduces several limitations. First, T-MEE introduces additional hyperparameters, including the loss weight and kernel bandwidth, as well as practical design choices such as the warm-up length before enabling the entropy objective. The need for hyperparameter tuning is a common limitation shared by many information-theoretic learning methods. Second, trajectory-level error entropy estimation requires sufficient sample support. Under extremely imbalanced data regimes, where certain tasks are represented by only a few demonstrations, the reliability of entropy estimation degrades, and the effectiveness of T-MEE diminishes. This characterizes a practical range of imbalance within which our method remains effective, rather than providing robustness under arbitrarily severe imbalance. 

