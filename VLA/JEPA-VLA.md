---
title: "JEPA-VLA: Video Predictive Embedding is Needed for VLA Models"
date: "2026-02-12"
authors: "Shangchen Miao; Ningya Feng; Jialong Wu; Ye Lin; Xu He; Dong Li"
url: https://arxiv.org/abs/2602.11832
pdf: https://arxiv.org/pdf/2602.11832
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.11832)** / [論文ページ](https://arxiv.org/abs/2602.11832)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 

**Shangchen Miao**<sup>1</sup> **Ningya Feng**<sup>1</sup> **Jialong Wu**<sup>1</sup> **Ye Lin**<sup>1</sup> **Xu He**<sup>2</sup> **Dong Li**<sup>2</sup> **Mingsheng Long**<sup>1</sup> 

# **Abstract** 

Recent vision-language-action (VLA) models built upon pretrained vision-language models (VLMs) have achieved significant improvements in robotic manipulation. However, current VLAs still suffer from low sample efficiency and limited generalization. This paper argues that these limitations are closely tied to an overlooked component, pretrained visual representation, which offers insufficient knowledge on both aspects of _environment understanding_ and _policy prior_ . Through an in-depth analysis, we find that commonly used visual representations in VLAs, whether pretrained via language-image contrastive learning or imagebased self-supervised learning, remain inadequate at capturing crucial, task-relevant environment information and at inducing effective policy priors, i.e., anticipatory knowledge of how the environment evolves under successful task execution. In contrast, we discover that predictive embeddings pretrained on videos, in particular V-JEPA 2, are adept at flexibly discarding unpredictable environment factors and encoding task-relevant temporal dynamics, thereby effectively compensating for key shortcomings of existing visual representations in VLAs. Building on these observations, we introduce JEPA-VLA, a simple yet effective approach that adaptively integrates predictive embeddings into existing VLAs. Our experiments demonstrate that JEPA-VLA yields substantial performance gains across a range of benchmarks, including LIBERO, LIBERO-plus, RoboTwin2.0, and real-robot tasks. 

# **1. Introduction** 

Recent advances in Vision-Language-Action (VLA) models have significantly improved the integration of visual perception, natural language understanding, and action generation, 

> 1Tsinghua University 2Huawei Noah’s Ark Lab. Correspondence to: Mingsheng Long _<_ mingsheng@tsinghua.edu.cn _>_ . 

_Preprint. February 13, 2026._ 

enabling general-purpose agents to interpret and execute human instructions across diverse environments (Kim et al., 2025a; Cen et al., 2025a). These VLAs typically build upon large-scale pretrained Vision-Language Models (VLMs) by incorporating action heads or other specialized action generation modules. Despite these advances, current VLAs still struggle with low sample efficiency and limited generalization to new scenarios. Many VLAs are trained on millions of trajectories (Bjorck et al., 2025; Zitkovich et al., 2023; Qu et al., 2025), yet cover only tens of tasks, and they can experience substantial performance degradation– sometimes up to _∼_ 40%–when evaluated on unseen tasks or under distribution shifts (Sapkota et al., 2025). 

We argue that these limitations are closely tied to bottlenecks in visual understanding imposed by VLM’s vision backbones or other visual processors (Sapkota et al., 2025; Shao et al., 2025). In particular, robotics requires two critical forms of visual knowledge: (i) _environment understanding_ , which precisely captures task-relevant object attributes (e.g., coordinates of targets) while flexibly discarding taskirrelevant information (e.g., lighting conditions); (ii) _policy priors_ , which encode anticipatory knowledge of how the environment evolves during successful task execution, thereby guiding action learning toward favorable future states. 

However, visual representations used in most VLMs and VLAs are pretrained on large-scale datasets via either image-based self-supervised learning (e.g., the DINO family (Caron et al., 2021; Oquab et al., 2024; Simeoni et al.´ , 2025)) or language-image contrastive learning (e.g., CLIP (Radford et al., 2021) and the SigLIP family (Zhai et al., 2023; Tschannen et al., 2025)). These representations exhibit notable deficiencies in providing the visual knowledge required for robotic control. First, they can be suboptimal for _environment understanding_ . Image-level self-supervised objectives like DINO encourage invariance to a broad set of augmentations, which may introduce inductive biases that are misaligned with manipulation tasks. For instance, invariance to random crops can reduce sensitivity to object positions and spatial configurations. In contrast, languageimage contrastive objectives emphasize semantics grounded in text-referred entities, but are often less effective at preserving other task-relevant cues (e.g., obstacles not mentioned in instructions, captions, or descriptions). Second, these representations provide weak _policy priors_ . Since they are 

1 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 


_Figure 1._ **Comparison of visual representations commonly used in VLAs: (a) Image-based self-supervised learning (e.g., the DINO family)** yields precise visual representations, but is relatively insensitive to task relevance and preserves task-irrelevant details. **(b) Language-image contrastive learning (e.g., CLIP and the SigLIP family)** emphasizes instruction-aligned entities and semantics, yet may capture less low-level task-relevant information beyond what is explicitly described in text. **(c) Video-based predictive learning (e.g., V-JEPA 2)** provides state-centric representations for task-relevant objects while also encoding temporal regularities that act as policy priors, which are difficult to obtain from image-only pretraining. 

typically learned from single images, they remain largely static and fail to adequately capture the temporal dynamics of successful action execution reflected in pretraining data, which are crucial for effective policy learning. 

Motivated by these insights, we turn to predictive embeddings (LeCun, 2022) learned from videos. In particular, we consider V-JEPA 2 (Assran et al., 2025), a jointembedding predictive architecture pretrained on internetscale videos. By predicting masked video patches in a latent space, V-JEPA 2 encourages representations that emphasize predictable, task-relevant factors while suppressing unpredictable nuisances. As a result, it is better suited to encoding dynamic cues about objects and agents (e.g., motion-relevant signals) that are critical for understanding the environment in robotics. Moreover, video-based pretraining allows V-JEPA 2 to internalize temporal regularities in how scenes evolve over successful task executions, which can serve as effective policy priors—a capability that is difficult to obtain from static, image-only pretraining. 

To substantiate these insights, we conduct in-depth analyses on underlying state estimation and prediction. Notably, V-JEPA 2 outperforms all prior representations in these tasks (see Section 2), indicating its superior ability to capture precisely task-relevant environment information and crucial temporal regularities for robotic decision making. Building on these findings, we propose _JEPA-VLA_ , a simple yet effective approach to incorporate V-JEPA 2 representations into VLAs, thereby strengthening their knowledge of both environment understanding and policy priors. We evaluate our approach across multiple benchmarks, includ- 

ing LIBERO (Liu et al., 2023), LIBERO-plus (Fei et al., 2025), RoboTwin2.0 (Chen et al., 2025), and a real-world experiment, demonstrating consistent and substantial improvements in task performance. 

The main contributions of this work are threefold: 

- We identify two essential aspects of visual knowledge required by VLAs—environment understanding and policy priors—and show that commonly used static visual representations do not adequately provide either. 

- We demonstrate that V-JEPA 2, a video-based predictive representation, effectively captures both knowledge and outperforms image-based and languageimage-based representations in our analysis tasks. 

- We propose JEPA-VLA, a simple and general framework for integrating video-predictive visual representations into existing VLAs, yielding consistent improvements in sample efficiency and generalization across multiple benchmarks and real-world tasks. 

# **2. An Analysis of Vision Representations for VLAs** 

We denote trajectories of robotic manipulation tasks as a partially observable Markov decision process (POMDP), formulated as a tuple _⟨S, O, ϕ, A, p⟩_ . At each time step, _st ∈S_ denotes the underlying environment state, while the agent only observes _ot_ = _ϕ_ ( _st_ ), which provides incomplete 

2 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 


_Figure 2._ **Analysis of visual representations for VLAs. (a) Trajectory demonstration and state definition.** Given observations _{ot}_ , we factorize the underlying state at each timestep as task-relevant and task-irrelevant parts. **(b) Experimental setup.** We freeze different vision encoders and train a lightweight ViT head to regress or predict environment states. More details can be found in Appendix A. **(c) Experimental results.** V-JEPA 2 achieves consistently lower relative loss on task-relevant regression and prediction, compared to DINOv2 and SigLIP, while showing no advantage on task-irrelevant (lighting/background) regression, suggesting that V-JEPA 2 better captures task-relevant environment states and policy priors while discarding nuisance factors. 

information about _st_ . Given an action _at ∼ π_ ( _o_ 1: _t_ ), the environment transitions to a new state _st_ +1 _∼ p_ ( _st_ +1 _| st, at_ ). This formulation highlights that effective robotic manipulation critically depends on inferring latent environment states and their evolution from partial visual observations. 

Effective VLAs must therefore embrace two forms of knowledge from visual representations. First, they must infer task-relevant environment states from partial observations, which can be formalized as learning an internal state estimator _qθ_ ( _st | o_ 1: _t_ ). Second, they must acquire policy-aligned anticipatory knowledge that captures how states evolve under successful action _a_<sup>_∗_</sup> when completing specific tasks, i.e., _pθ_ ( _st_ +1 _| st, a_<sup>_∗_</sup> _t_<sup>), which in turn induces policy priors.This</sup> perspective is related to recent work on video generation models as policies (Du et al., 2023; Feng et al., 2025), which leverage large-scale video generative pretraining to transfer temporal regularities as inductive biases for control. By focusing on visual representations, our approach requires only minimal, plug-and-play modifications to existing VLAs and 

may benefit from the efficiency of focusing on predictable aspects while ignoring unpredictable details that generative objectives emphasize. 

As discussed earlier, most visual encoders in current VLAs are pretrained on static images and provide insufficient support for policy learning with either form of knowledge. In contrast, we adopt V-JEPA 2 and hypothesize that its videobased predictive objective enables the encoding of temporal regularities that simultaneously support accurate environment understanding and induce effective policy priors. 

In the remainder of this section, we conduct a comparative analysis to examine whether different visual representations (i) understand the current environment state, capturing crucial task-relevant information while discarding nuisance factors, and (ii) offer effective policy priors that anticipate how the environment evolves under successful actions. An overview of these experiments is shown in Figure 2. 

3 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 

## **2.1. Environment Understanding** 

Effective manipulation requires visual representations to capture task-relevant aspects of the environment, such as the states of the robot arm and movable objects, while discarding nuisance factors that do not affect action execution (e.g., background texture and lighting). To evaluate whether different visual representations exhibit these properties, we design two probing experiments that separately assess their ability to encode task-relevant states and to ignore taskirrelevant variations. 

nuisance factors, suggesting that its representations selectively focus on dynamics and visual cues that are more relevant to manipulation. Such insensitivity to irrelevant variations is desirable and contributes to improved robustness and generalization. 

**Finding 2.** _V-JEPA 2 representations encode less information about task-irrelevant visual factors, compared to DINOv2 and SigLIP._ 

## **2.2. Policy Priors** 

## 2.1.1. TASK-RELEVANT STATE ESTIMATION 

**Setup** We conduct experiments on the LIBERO-10 benchmark (Liu et al., 2023) by regressing the states of the robot arm and task-relevant objects from visual representations. The vision encoders are frozen, and a lightweight regression head is trained using representations extracted from the most recent two frames. We use the mean squared error (MSE) as the evaluation metric. 

**Results** As shown in Figure 2c _(left)_ , V-JEPA 2 achieves a lower MSE when regressing current task-relevant states compared to DINOv2 and SigLIP. Image-based selfsupervised representations such as DINOv2 tend to preserve detailed visual information across the entire image, which may introduce inductive biases misaligned with manipulation tasks, resulting in generally precise but not task-focused representations. In contrast, language–image representations like SigLIP emphasize entities referred to in the text but may overlook task-relevant objects that are not commonly explicitly mentioned. V-JEPA 2, pretrained with video-based predictive objectives, captures object-centric and motion-related cues, providing representations more aligned with task-relevant states. 

**Finding 1.** _V-JEPA 2 representations encode taskrelevant environment states more precisely than DINOv2 and SigLIP._ 

Policy priors correspond to anticipatory knowledge of how task-relevant environment states are expected to evolve under successful action execution. Rather than directly predicting future observations, we evaluate whether visual representations encode crucial transition-aware information that reflects changes in task-relevant states despite partial observability. 

**Setup** We train models on the LIBERO-10 benchmark to predict future state changes. Specifically, to mitigate the effects of partial observations on inaccurate state estimation, we train a lightweight head to predict the residual between the task-relevant state 10 steps later and the current state, using frozen visual representations. 

**Results** As shown in Figure 2c (middle), V-JEPA 2 achieves lower MSE in predicting state residuals compared to DINOv2 and SigLIP. This suggests that V-JEPA 2 encodes transition-aware representations that capture temporal regularities aligned with successful task execution. In contrast, image-based representations pretrained on static images lack explicit temporal supervision and struggle to capture such transition dynamics, limiting their ability to induce effective policy priors. 

**Finding 3.** _V-JEPA 2 representations effectively embed policy priors._ 

## 2.1.2. TASK-IRRELEVANT STATE ESTIMATION 

**Setup** We further evaluate the sensitivity of visual representations to task-irrelevant factors using the LIBERO-plus benchmark (Fei et al., 2025), which introduces perturbations that do not affect the required action sequence. We focus on lighting and background variations, and train models to regress these perturbation attributes from visual representations. Since such perturbations remain constant within each trajectory, only the first frame is used as input. 

**Results** As shown in Figure 2c _(right)_ , V-JEPA 2 exhibits higher error in regressing lighting and background perturbations compared to DINOv2 and SigLIP. This result indicates that V-JEPA 2 encodes less information about task-irrelevant 

# **3. JEPA-VLA** 

In light of these findings, we propose JEPA-VLA, a simple yet effective approach for incorporating powerful V-JEPA 2 representations into VLAs. 

## **3.1. Problem Formulation** 

We consider two main components: an action model _πθ_ and a frozen, pretrained V-JEPA 2 encoder _Eϕ_ . The action model _πθ_ follows a standard VLA formulation: it takes as input a language instruction _l_ , multi-view observations from _N_ cameras (e.g., head, wrist, and auxiliary views) _o_<sup>0:</sup> _t_<sup>_N_</sup> , and the robot’s proprioceptive state _st_ , and produces an action 

4 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 

_at_ according to 


Meanwhile, the frozen V-JEPA 2 encoder is built on a ViT (Dosovitskiy, 2020) backbone and maps a video clip _ot−h_ : _t ∈_ R<sup>_T ×H×W ×_3</sup> to visual representations _ht ∈_ R<sup>_N×C_</sup> , where _N_ scales with the spatial and temporal resolution _H_ , _W_ , and _T_ . This process is formalized as 


We aim to learn an enhanced action model that effectively leverages the predictive visual representation _ht_ : 


thereby leading to improved environment understanding and more reliable action generation. 

## **3.2. Representation Fusion** 

To condition the action model on additional visual representations, we instantiate two fusion strategies. 

**Early Fusion** Most VLAs are built on Transformer backbones. A natural approach is to treat V-JEPA 2 representations as _additional input embeddings_ and concatenate them with the original token sequence. This design is lightweight, as it introduces only a linear projection to align representation dimensions before fusion. Empirically, this simple concatenation works well for VLAs _without_ large-scale robotmanipulation pretraining, where the policy is largely learned from scratch (despite sharing common VLM priors). 

**Gated Fusion** However, this naive fusion is ineffective for VLAs pretrained on large-scale robot-manipulation data. Directly injecting extra tokens can shift the input distribution and interfere with the pretrained representations, leading to degraded transfer. To better adapt V-JEPA 2 representations to this more commonly used and data-efficient setting, we design an alternative architecture that preserves pretrained priors. Inspired by Flamingo (Alayrac et al., 2022), we incorporate V-JEPA 2 representations via several _gated crossattention_ layers, where the original VLA tokens serve as queries, and the V-JEPA 2 representations serve as keys and values. This gated design allows the VLA to selectively attend to predictive embeddings when beneficial, enabling adaptive integration while minimally disrupting pretrained knowledge. 

In practice, to balance learning performance, memory usage, and inference latency, we do not insert a gated crossattention layer after every transformer decoder layer. Instead, guided by empirical results, we adopt a sparse fusion 

scheme that inserts gated cross-attention at a fixed interval across the decoder stack, which we find to be both efficient and sufficiently effective. To stably incorporate complementary information from V-JEPA 2 without disrupting pretrained VLA representations, we follow the design principles of Flamingo (Alayrac et al., 2022) to set the learning rate of the newly introduced fusion layers substantially lower than that of the original VLA parameters. Further architectural details are provided in Appendix B. 

# **4. Experiments** 

In this section, we investigate whether simply integrating V-JEPA 2 representations can consistently improve manipulation policies not only in in-domain, data-rich regimes, but also under out-of-domain shifts and limited-data settings. We describe the simulation and real-world benchmarks in Section 4.1 and provide implementation details in Section 4.2. Section 4.3 presents the benchmark results. Finally, in Section 4.4, we examine whether V-JEPA 2 outperforms other pretrained visual representations across a broader range of embodied AI tasks. 

## **4.1. Benchmarks** 

We validate JEPA-VLA across diverse environments, as shown in Figure 3. 

**LIBERO** (Liu et al., 2023) is a benchmark comprising four task suites designed to study lifelong learning and knowledge transfer in robotics. Each suite contains 10 tasks with 50 tele-operated demonstrations. We use all four suites: _LIBERO-Spatial_ (spatial reasoning), _LIBERO-Object_ (object understanding), _LIBERO-Goal_ (instruction following), and _LIBERO-Long_ (long-horizon tasks with diverse layouts). 

**LIBERO-plus** (Fei et al., 2025) extends LIBERO by introducing controlled perturbations along multiple dimensions, including camera viewpoint, initial state, language instructions, lighting, background, noise, and layout. 

**RoboTwin** (Mu et al., 2025; Chen et al., 2025) provides simulation benchmarks for dual-arm manipulation. We use **RoboTwin2.0** (Chen et al., 2025) in our experiments. RoboTwin2.0 includes 50 tasks across multiple robot platforms and comprises 731 object instances spanning 147 categories. It also incorporates comprehensive domain randomization (e.g., clutter, lighting, background, tabletop height, and language instructions), requiring policies to remain robust under transfer. We adopt the Aloha-AgileX dual-arm setup and evaluate on six tasks. 

**Real-World Task** We evaluate on a single Piper robot arm. We design a pick-and-place task and train both the baseline and our method. To assess performance under limited data, we additionally train our method on a one-fifth subset of 

5 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 


_Figure 3._ Evaluation benchmarks, including (a) LIBERO, (b) LIBERO-plus, (c) RoboTwin, (d) a real-world task, and (e) CortexBench. 

_Table 1._ **LIBERO task success rate (%) in the basic VLA setting.** _Baseline_ denotes the basic VLA without V-JEPA 2 fusion. 

|MODEL|SPATIAL|OBJECT|GOAL|LONG|AVERAGE|
|---|---|---|---|---|---|
|BASELINE|58.2|74.8|87.8|25.8|61.65|
|**W/ OURS**|**69.2**|**78.2**|**87.8**|**41.0**|**69.05**|
|∆|+11.0|+3.4|0.0|+15.2|+7.40|


_Table 2._ **LIBERO-plus task success rate (%) in the basic VLA setting.** _Baseline_ denotes the Basic VLA without V-JEPA 2 fusion. 

|MODEL|CAMERA|ROBOT|LANGUAGE|LIGHT|BACKGROUND|NOISE|LAYOUT|TOTAL|
|---|---|---|---|---|---|---|---|---|
|WORLDVLA|0.1|27.9|41.6|43.7|17.1|10.9|38.0|25.0|
|BASELINE|0.1|20.8|43.9|26.3|10.1|4.1|26.9|18.9|
|**W/ OURS**|**0.4**|**25.7**|**54.4**|**38.0**|**23.9**|**4.1**|**32.8**|**25.6**|
|∆|+0.3|+4.9|+10.5|+11.7|+13.8|0.0|+5.9|+6.7|


the training trajectories (22 trajectories). We conduct tests under various settings to verify whether JEPA-VLA can improve generalization. More settings and implementation details can be found in Appendix E. 

## **4.2. Implementation Details** 

We implement JEPA-VLA in a standard VLA setting where the policy conditions on a third-person visual observation and a language instruction. Concretely, we extract V-JEPA 2 representations from the two most recent frames and use them as additional conditioning signals alongside the current observation when predicting actions. Two base VLAs are experimented with, as described below. 

**Basic VLA Experiments** To assess the effectiveness of V-JEPA 2 representations for VLAs, we begin by implementing a basic VLA model architecture, consisting of a pretrained Vision-Language Model (VLM) backbone and a linear action prediction head. Inspired by the architecture of WorldVLA (Cen et al., 2025b), we use Chameleon (Team, 2024) as the VLM backbone and discretize the actions into 256 tokens, as done in previous works (Kim et al., 2025b). We evaluate this setting on both LIBERO and LIBERO-plus. For both datasets, as this is an experimental trial, we train using only 1/10 of the LIBERO data. Additionally, we conduct trials with the same architecture for real-world experiments. 

**Mainstream VLA Experiments** We further evaluate our method by incorporating V-JEPA 2 representations into 

mainstream VLAs on LIBERO and RoboTwin2.0. We implement one of the standard OpenVLA-OFT (Kim et al., 2025a) configurations, using third-person images and language instructions as input, with parallel decoding, action chunking, and continuous action prediction, employing an _ℓ_ 1 regression loss. For LIBERO, we follow the official data preprocessing procedure provided by the OpenVLA-OFT implementation. For RoboTwin2.0, we train with the official 50 clean trajectories and evaluate under both clean and domain-randomized settings.We insert gated cross-attention layers every _eight_ decoder layers for both benchmarks. 

**Training Details** We follow the official baseline training settings whenever possible, adjusting only the batch size to accommodate limited computational resources. For LIBERO and LIBERO-plus, we train both our method and the baselines with a batch size of 16. The Basic VLA is trained for 40 epochs to ensure convergence, while OpenVLA-OFT is trained for 150k steps following the official schedule. For RoboTwin2.0, we use a batch size of 8 and train for approximately 100k steps. For the newly introduced fusion layers, we set a smaller learning rate of 1 _×_ 10<sup>_−_5</sup> to 1 _×_ 10<sup>_−_4</sup> , compared to 5 _×_ 10<sup>_−_4</sup> for the original VLA parameters in OpenVLA-OFT. 

## **4.3. Main Results** 

As shown in Tables 1 and 2, incorporating V-JEPA 2 representations into the basic VLA improves success rates by 7.4% on LIBERO and 6.7% on LIBERO-plus. Notably, on 

6 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 

_Table 3._ **LIBERO task success rate (%) in the mainstream VLA setting.**<sup>_†_</sup> Results are taken from official paper (Kim et al., 2025a). 

|MODEL|SPATIAL|OBJECT|GOAL|LONG|AVERAGE|
|---|---|---|---|---|---|
|OPENVLA-OFT<sup>_†_</sup>|96.2|98.3|96.2|90.7|95.35|
|OPENVLA-OFT|84.4|91.8|95.2|89.8|90.30|
|**W/ OURS**|**97.2**|**98.0**|**95.6**|**94.8**|**96.40**|
|∆|+12.8|+6.2|+0.4|+5.0|+6.10|


_Table 4._ **RoboTwin2.0 task success rate (%) in the mainstream VLA setting.** _Baseline_ denotes our implementation of OpenVLA-OFT. 

||Beat Blo|ck Hammer|Click A|larmclock|Lift|Pot|Place|Fan|Place P|hone Stand|Stack B|owls Two|Aver|age|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Model|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|
|Baseline|18.0|0.0|85.0|26.0|93.0|18.0|25.0|0.0|33.0|4.0|75.0|8.0|54.8|9.3|
|**Ours**|**65.0**|**13.0**|**92.0**|**30.0**|**98.0**|**21.0**|**38.0**|**0.0**|**60.0**|**16.0**|**88.0**|**26.0**|**73.5**|**17.7**|
|∆|+47.0|+13.0|+7.0|+4.0|+5.0|+3.0|+13.0|0.0|+27.0|+12.0|+13.0|+18.0|+18.7|+8.4|


_Table 5._ **Real-world task (pick the yellow bowl into the plate) success rate (%)** . _Layout_ means different desktop item layouts, and _light_ means different brightness. 

_Table 7._ **LIBERO-Long task success rate (%)** with different visual representations. Baseline denotes our implementation of the basic VLA. 

|MODEL|AVERAGE|LAYOUT|LIGHT|
|---|---|---|---|
|BASELINE|50.0|0.0|0.0|
|W/ OURS1/5 DATA|60.0|33.3|66.7|
|**W/ OURS** FULL DATA|**80.0**|**100.0**|**100.0**|


|MODEL<br>|LONGSR (%)|
|---|---|
|BASELINE|25.8|
|BASELINE+DINOV2|26.0|
|BASELINE+DINOV2|31.2|
|BASELINE+SIGLIP|33.6|
|**BASELINE+V-JEPA 2**|**41.0**|


LIBERO-plus, our method outperforms the official WorldVLA model despite being trained with only one-tenth of the action-model data and without any world-model training data, indicating that V-JEPA 2 representations substantially enhance generalization (see Appendix C for per-task details). In real-world experiments (Table 5), V-JEPA 2 representations enable training with only one-fifth of the trajectories while still outperforming the baseline, further validating improved performance and generalization in deployment settings (trajectory examples are provided in Appendix E). 

Our method also transfers effectively to mainstream VLA architectures. As shown in Table 3, despite using a smaller batch size, our method improves over the baseline by 6.1% and even surpasses the official OpenVLA-OFT results. On RoboTwin2.0 (Table 4), our method achieves consistent average gains of 18.7% and 8.4% in the clean and domainrandomized settings, respectively. Overall, these results indicate that JEPA-VLA is not only effective in controlled, simplified evaluations but also yields robust improvements on mainstream VLA backbones, demonstrating the generality of our method. 

## **4.4. Comparative Evaluation of Visual Representations** 

We next evaluate whether V-JEPA 2 provides greater downstream benefits than other visual representations commonly used in VLAs and broader embodied AI tasks. 

**VLAs** Motivated by the analysis in Section 2, which suggests that static image-based representations may fail to capture key task-relevant states and effective policy priors, we conduct controlled replacement experiments by directly swapping the visual representation in the basic VLA baseline (Section 4.2). As shown in Table 7, adapting DINOv2 yields marginal or even negative gains, while SigLIP leads to only modest improvements. In contrast, incorporating V-JEPA 2 results in substantially larger performance gains. 

**Broader Embodied AI Tasks** Beyond the VLA backbones commonly adopted in robotic manipulation, we further compare V-JEPA 2 with strong pretrained visual representations (PVRs) evaluated in the broader embodied AI literature. Specifically, we consider CortexBench (Majumdar et al., 2023), which comprises 17 tasks designed to assess the utility of pretrained visual representations for embodied control. We focus on 10 representative tasks and compare V-JEPA 2 against VC-1, a high-performing PVR reported in the same benchmark to outperform prior methods on average. Results in Tables 6 and 6 show remarkable improvements across the evaluated tasks: V-JEPA 2 outperforms VC-1 on most subtasks, indicating that videopredictive pretraining yields representations that transfer effectively to embodied decision making. Additional details are provided in Appendix D. 

7 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 

_Table 6._ **CortexBench results.** _Top:_ MetaWorld task success rate (%). _Bottom:_ DMControl episode reward. 

|METAWORLD|ASSEMBLY|BIN PICKING<br>|BUTTON PRESS<br>|DRAWER OPEN|HAMMER|AVERAGE|
|---|---|---|---|---|---|---|
|CLIP (VIT-B)|70.7|68.0|48.0|100.0|90.7|75.5|
|VC-1 (VIT-L)|88.0|**84.0**|80.0|100.0|92.0|88.8|
|**V-JEPA 2 (VIT-L)**|**96.0**|80.0|**84.0**|**100.0**|**92.0**|**90.4**|
|DMCONTROL<br>WAL|KER STAND|WALKER WALK|REACHER EASY|CHEETAH RU|N<br>FINGER S|PIN<br>AVERAGE|
|VC-1 (VIT-L)|811|338|**836**|155|540|536.0|
|**V-JEPA 2 (VIT-L)**|**825**|**436**|821|**156**|**681**|**583.8**|


# **5. Related Work** 

**Vision-Language-Action Models** Building on the success of VLMs, recent VLAs have been able to process task instructions and visual observations and generate actions for manipulation. VLAs have made remarkable progress in language-conditioned control and generalization over taskspecific controllers, enabling semantic reasoning and even achieving zero-shot performance on unseen tasks (Zitkovich et al., 2023; Yang et al., 2025; Glossop et al., 2025; Li et al., 2025). However, despite advancements in instructionfollowing, current VLAs still struggle with insufficient visual understanding (Sapkota et al., 2025; Shao et al., 2025). Although several approaches have been proposed to improve visual understanding , including integrating explicit perception modules (Yuan et al., 2025; Huang et al., 2025), incorporating visual chain-of-thought reasoning (Zhao et al., 2025; Cen et al., 2025b;a; Zhong et al., 2025), and utilizing methods based on 3D modeling and point clouds (Lin et al., 2025; Qu et al., 2025). However, these methods are often overly complex, difficult to implement in real-world settings or lack the desired effectiveness. Our goal is to identify a minimal and more general approach to enhance the visual understanding of current mainstream VLAs. 

**Pretrained Vision Representations for Robotics.** A growing body of work has developed pretrained visual representations tailored for robotics and manipulation (Nair et al., 2023; Ma et al., 2023; Xiao et al., 2022). While these representations improve transfer in specific settings, they are often not sufficiently general to serve as universal backbones for modern VLA models. In practice, most VLM vision backbones used in recent VLAs (e.g., OpenVLA (Kim et al., 2025b) and RDT (Liu et al., 2024)) are pretrained via either image-based self-supervised learning (e.g., the DINO family (Caron et al., 2021; Oquab et al., 2024; Simeoni et al.´ , 2025)) or language–image contrastive learning (e.g., the SigLIP family (Zhai et al., 2023; Tschannen et al., 2025)). Despite their success, these pretraining paradigms can be suboptimal for robotic environment understanding and lack of policy priors as discussed in Section 1. Motivated by these limitations, we explore pretrained video predictive representations for downstream robotic control. 

**The Evolution of JEPA** The Joint-Embedding Predictive Architecture (JEPA) framework was first introduced to build predictive models of the world through self-supervised learning, enabling efficient understanding, prediction, and reasoning about the real world without relying on large labeled datasets or traditional generative objectives (LeCun, 2022). This was followed by the development of I- JEPA (Assran et al., 2023), V-JEPA (Bardes et al., 2024), and V-JEPA 2 (Assran et al., 2025), demonstrating that this architecture is scalable and can generate visual representations that perform well across a wide range of tasks (e.g., motion understanding). Subsequent work has further shown that intuitive physics understanding emerges during the training of V-JEPA (Garrido et al., 2025), suggesting that the latent predictive learning approach inherent in V-JEPA produces broadly generalizable representations capable of understanding the physical world, predicting future states, and planning effectively in new situations. We aim to leverage these capabilities in robotics. 

# **6. Conclusion and Future Work** 

We identify two critical forms of visual knowledge required by VLAs—environment understanding and policy priors—and show that widely used vision encoders fail to provide them, resulting in poor sample efficiency and weak generalization of VLAs. Crucially, we demonstrate that video-predictive embeddings, exemplified by V-JEPA 2, fill this gap by capturing task-relevant state representations and encoding temporal regularities that act as effective policy priors. Building on this finding, we introduce JEPA-VLA, a simple and general integration framework that consistently boosts VLA performance across multiple benchmarks. 

This work opens several promising directions for future research. While we focus on a straightforward fusion strategy, more principled mechanisms for integrating predictive embeddings remain largely unexplored. More broadly, our findings suggest that leveraging large-scale video pretraining is a key ingredient for advancing visual understanding in robotics, and we hope this work will encourage further investigation into vision-centric approaches for building more robust and generalizable embodied agents. 

8 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 

# **References** 

- Alayrac, J.-B., Donahue, J., Luc, P., Miech, A., Barr, I., Hasson, Y., Lenc, K., Mensch, A., Millican, K., Reynolds, M., et al. Flamingo: a visual language model for fewshot learning. _Advances in neural information processing systems_ , 35:23716–23736, 2022. 

- Assran, M., Duval, Q., Misra, I., Bojanowski, P., Vincent, P., Rabbat, M., LeCun, Y., and Ballas, N. Self-supervised learning from images with a joint-embedding predictive architecture. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 15619– 15629, 2023. 

- Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., et al. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- Bardes, A., Garrido, Q., Ponce, J., Chen, X., Rabbat, M., LeCun, Y., Assran, M., and Ballas, N. Revisiting feature prediction for learning visual representations from video. _Transactions on Machine Learning Research_ , 2024. 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Caron, M., Touvron, H., Misra, I., Jegou, H., Mairal, J., Bojanowski, P., and Joulin, A. Emerging properties in self-supervised vision transformers. In _ICCV 2021International Conference on Computer Vision_ , pp. 1–21. IEEE, 2021. 

- Cen, J., Huang, S., Yuan, Y., Yuan, H., Yu, C., Jiang, Y., Guo, J., Li, K., Luo, H., Wang, F., et al. Rynnvla-002: A unified vision-language-action and world model. _arXiv preprint arXiv:2511.17502_ , 2025a. 

- Cen, J., Yu, C., Yuan, H., Jiang, Y., Huang, S., Guo, J., Li, X., Song, Y., Luo, H., Wang, F., et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025b. 

- Chen, T., Chen, Z., Chen, B., Cai, Z., Liu, Y., Li, Z., Liang, Q., Lin, X., Ge, Y., Gu, Z., et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- Dosovitskiy, A. An image is worth 16x16 words: Transformers for image recognition at scale. _arXiv preprint arXiv:2010.11929_ , 2020. 

- Du, Y., Yang, S., Dai, B., Dai, H., Nachum, O., Tenenbaum, J., Schuurmans, D., and Abbeel, P. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 

- Fei, S., Wang, S., Shi, J., Dai, Z., Cai, J., Qian, P., Ji, L., He, X., Zhang, S., Fei, Z., et al. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 

- Feng, Y., Tan, H., Mao, X., Xiang, C., Liu, G., Huang, S., Su, H., and Zhu, J. Vidar: Embodied video diffusion model for generalist manipulation. _arXiv preprint arXiv:2507.12898_ , 2025. 

- Garrido, Q., Ballas, N., Assran, M., Bardes, A., Najman, L., Rabbat, M., Dupoux, E., and LeCun, Y. Intuitive physics understanding emerges from self-supervised pretraining on natural videos. _arXiv preprint arXiv:2502.11831_ , 2025. 

- Glossop, C., Chen, W., Bhorkar, A., Shah, D., and Levine, S. Cast: Counterfactual labels improve instruction following in vision-language-action models. _arXiv preprint arXiv:2508.13446_ , 2025. 

- Huang, J., Wang, S., Lin, F., Hu, Y., Wen, C., and Gao, Y. Tactile-vla: unlocking vision-language-action model’s physical knowledge for tactile generalization. _arXiv preprint arXiv:2507.09160_ , 2025. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025a. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E. P., Sanketi, P. R., Vuong, Q., et al. Openvla: An open-source visionlanguage-action model. In _Conference on Robot Learning_ , pp. 2679–2713. PMLR, 2025b. 

- LeCun, Y. A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. _Open Review_ , 62(1):1–62, 2022. 

- Li, M., Zhao, Z., Che, Z., Liao, F., Wu, K., Xu, Z., Ren, P., Jin, Z., Liu, N., and Tang, J. Switchvla: Execution-aware task switching for vision-language-action models. _arXiv preprint arXiv:2506.03574_ , 2025. 

- Lin, T., Li, G., Zhong, Y., Zou, Y., Du, Y., Liu, J., Gu, E., and Zhao, B. Evo-0: Vision-language-action model with implicit spatial understanding. _arXiv preprint arXiv:2507.00416_ , 2025. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for 

9 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 

- lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 

- Liu, S., Wu, L., Li, B., Tan, H., Chen, H., Wang, Z., Xu, K., Su, H., and Zhu, J. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- Ma, Y. J., Sodhani, S., Jayaraman, D., Bastani, O., Kumar, V., and Zhang, A. Vip: Towards universal visual reward and representation via value-implicit pre-training. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- Majumdar, A., Yadav, K., Arnaud, S., Ma, J., Chen, C., Silwal, S., Jain, A., Berges, V.-P., Wu, T., Vakil, J., et al. Where are we in the search for an artificial visual cortex for embodied intelligence? _Advances in Neural Information Processing Systems_ , 36:655–677, 2023. 

- Mu, Y., Chen, T., Chen, Z., Peng, S., Lan, Z., Gao, Z., Liang, Z., Yu, Q., Zou, Y., Xu, M., et al. Robotwin: Dual-arm robot benchmark with generative digital twins. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 27649–27660, 2025. 

- Nair, S., Rajeswaran, A., Kumar, V., Finn, C., and Gupta, A. R3m: A universal visual representation for robot manipulation. In _Conference on Robot Learning_ , pp. 892– 909. PMLR, 2023. 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec, M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., ElNouby, A., et al. Dinov2: Learning robust visual features without supervision. _Transactions on Machine Learning Research Journal_ , 2024. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pp. 8748–8763. PmLR, 2021. 

- Sapkota, R., Cao, Y., Roumeliotis, K. I., and Karkee, M. Vision-language-action models: Concepts, progress, applications and challenges. _arXiv preprint arXiv:2505.04769_ , 2025. 

   - Simeoni, O., Vo, H. V., Seitzer, M., Baldassarre, F., Oquab,´ M., Jose, C., Khalidov, V., Szafraniec, M., Yi, S., Ramamonjisoa, M., et al. Dinov3. _arXiv preprint arXiv:2508.10104_ , 2025. 

   - Team, C. Chameleon: Mixed-modal early-fusion foundation models. _arXiv preprint arXiv:2405.09818_ , 2024. 

   - Tschannen, M., Gritsenko, A., Wang, X., Naeem, M. F., Alabdulmohsin, I., Parthasarathy, N., Evans, T., Beyer, L., Xia, Y., Mustafa, B., et al. Siglip 2: Multilingual vision-language encoders with improved semantic understanding, localization, and dense features. _arXiv preprint arXiv:2502.14786_ , 2025. 

   - Xiao, T., Radosavovic, I., Darrell, T., and Malik, J. Masked visual pre-training for motor control. _arXiv preprint arXiv:2203.06173_ , 2022. 

   - Yang, S., Li, H., Chen, Y., Wang, B., Tian, Y., Wang, T., Wang, H., Zhao, F., Liao, Y., and Pang, J. Instructvla: Vision-language-action instruction tuning from understanding to manipulation. _arXiv preprint arXiv:2507.17520_ , 2025. 

   - Yuan, T., Liu, Y., Lu, C., Chen, Z., Jiang, T., and Zhao, H. Depthvla: Enhancing vision-language-action models with depth-aware spatial reasoning. _arXiv preprint arXiv:2510.13375_ , 2025. 

   - Zhai, X., Mustafa, B., Kolesnikov, A., and Beyer, L. Sigmoid loss for language image pre-training. In _2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ , pp. 11941–11952. IEEE, 2023. 

   - Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025. 

   - Zhong, Z., Yan, H., Li, J., Liu, X., Gong, X., Zhang, T., Song, W., Chen, J., Zheng, X., Wang, H., et al. Flowvla: Visual chain of thought-based motion reasoning for vision-language-action models. _arXiv preprint arXiv:2508.18269_ , 2025. 

   - Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

- Shao, R., Li, W., Zhang, L., Zhang, R., Liu, Z., Chen, R., and Nie, L. Large vlm-based vision-language-action models for robotic manipulation: A survey. _arXiv preprint arXiv:2508.13073_ , 2025. 

10 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 

# **A. Details of Vision Representation Analysis** 

This section provides implementation details for the analysis tasks introduced in Section 2. The hyperparameters used across all analysis experiments are summarized in Table 8. 

For all experiments, we split the dataset into training, validation, and test sets with a ratio of 8:1:1. Models are trained with early stopping: training terminates if the validation loss does not decrease for 10 consecutive epochs. The checkpoint with the lowest validation loss is selected for final evaluation on the test set. 

_Table 8._ Hyperparameters used for vision representation analysis. 

|HYPERPARAMETER|VALUE|
|---|---|
|ATTENTIONHEADS|16|
|BATCH SIZE|32|
|DECODERLAYERS|12|
|DROPOUTRATE|0.1|
|FEEDFORWARDDIMENSION|3072<br>|
|LEARNINGRATE|1_×_10<sup>_−_4</sup>|
|MAXIMUMEPOCHS|100|
|OPTIMIZER|ADAMW|
|WEIGHTDECAY|1_×_10<sup>_−_5</sup>|


**Task-Relevant State Regression** To evaluate whether visual representations encode task-relevant environment information, we regress the current relevant states from frozen visual features. Specifically, we prepend an additional [CLS] token to the representation sequence and use its output embedding for state regression. All relevant-state labels are normalized to have zero mean and unit variance to stabilize training. 

**Task-Irrelevant State Regression** We assess sensitivity to task-irrelevant factors by regressing lighting parameters and background appearance. 

For lighting regression, all lighting-related parameters (e.g., light direction, position, and diffuse components) are concatenated into a single target vector. An additional [CLS] token is introduced, and its embedding is used to predict the lighting parameters. 

For background regression, we employ an additional linear upsampling head to reconstruct the background texture from the frozen visual representations. Reconstruction is supervised using the standard mean absolute error (MAE) loss. 

**Task-Relevant State Prediction** To evaluate whether representations encode transition-aware information, we predict future changes in task-relevant states. Since control in LIBERO-10 is precise and state changes between adjacent time steps are often subtle, we predict the residual between the current state and the state after 10 time steps. 

Unlike the regression setting, we do not normalize state values in this task, as normalization would distort the semantic meaning of residuals. Except for this difference, all other settings remain identical to those used in _Task-Relevant State Regression_ . 

# **B. JEPA-VLA Fusion Method Details** 

The overall JEPA-VLA fusion architecture is illustrated in Figure 4. We consider two representative scenarios depending on whether the underlying Vision-Language-Action (VLA) model has been pretrained on large-scale robotic manipulation datasets. 

For VLAs trained from scratch or without extensive robot-specific pretraining, a simple fusion strategy is sufficient. In this setting, V-JEPA 2 representations are treated as additional input embeddings and concatenated with the original token sequence. This straightforward design effectively injects video-predictive knowledge into the VLA, enabling the policy to leverage temporal and state-centric information provided by V-JEPA 2. 

However, for VLAs that have already been pretrained on large-scale robotic datasets, naive concatenation can be detrimental. Directly introducing extra embeddings shifts the input distribution and may interfere with the pretrained representations, 

11 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 


_Figure 4._ **JEPA-VLA fusion architecture.** (a) For VLAs without large-scale robotic pretraining, V-JEPA 2 representations are concatenated as additional input embeddings. (b) For VLAs pretrained on large-scale robotic datasets, we integrate V-JEPA 2 representations using gated cross-attention, which enables adaptive fusion while preserving pretrained priors. 

thereby disrupting the learned priors and leading to degraded performance. This issue is particularly pronounced when the pretrained VLA has already internalized strong task-specific or action-aligned representations. 

To address this challenge, we incorporate V-JEPA 2 representations through gated cross-attention layers. In this design, the original VLA token embeddings serve as queries, while the V-JEPA 2 representations act as keys and values. The gating mechanism allows the model to adaptively control the contribution of predictive visual representations, selectively attending to V-JEPA 2 features when beneficial while preserving the original pretrained priors. This adaptive fusion enables effective knowledge transfer from V-JEPA 2 without destabilizing pretrained VLA representations. 

# **C. LIBERO-plus Benchmark Implementation Details** 

Following the official LIBERO-plus evaluation protocol, each Vision-Language-Action (VLA) model is trained separately on the four LIBERO task suites. For each task suite, multiple checkpoints are saved during training, and the final performance is obtained by evaluating four selected checkpoints and reporting their average score. This protocol is designed to mitigate variance introduced by checkpoint selection. 

In our experiments, we evaluate the same set of checkpoints reported in Table 1. We further report detailed LIBERO-plus results for each task suite separately, including Spatial, Object, Goal, and Long tasks. The corresponding results are presented in Tables 9, 10, 11, and 12, respectively. 

# **D. CortexBench Benchmark Implementation Details** 

CortexBench is a comprehensive benchmark consisting of 17 tasks that span a wide range of robotic manipulation scenarios. While the benchmark provides reference results for several pretrained visual representations, we found that the reported 

12 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 

performance of VC-1 could not be reliably reproduced for all tasks using the publicly released code and configurations. 

As a result, we restrict our evaluation to a subset of 10 CortexBench tasks for which we are able to consistently reproduce baseline VC-1 results. On this subset, we compare the performance of V-JEPA 2 representations against VC-1 under identical experimental settings. 

Furthermore, we note that the official CortexBench implementation reports task rewards rather than binary success rates for MetaWorld tasks. Since no explicit mapping from reward values to success criteria is provided, we report the reproduced reward scores for both VC-1 and V-JEPA 2 to ensure a fair and transparent comparison. 

# **E. Real-World Experiment Details** 

**Data Collection** We manually collect a total of 100 demonstration trajectories for a real-world pick-and-place task using a single robotic arm. These trajectories are used to train both the baseline model and JEPA-VLA. To evaluate the effectiveness of JEPA-VLA in data-limited settings, we additionally train our method using only one-fifth of the collected data. 

**Training Details** All models are trained for 30 epochs with an action chunk size of 10, a learning rate of 5 _×_ 10<sup>_−_6</sup> , and a batch size of 32. For JEPA-VLA, we extract representations from the V-JEPA 2 encoder using the two most recent visual frames. The resulting embeddings are concatenated with the original token sequence and provided as additional inputs to the VLA model. 

**Evaluation Details** During evaluation, we adopt the attention masking mechanism proposed in WorldVLA (Cen et al., 2025b), which prevents action tokens from attending to future actions. This masking strategy naturally supports parallel decoding during inference. We implement parallel decoding to accelerate evaluation and interpolate between consecutive actions to ensure smooth and coherent trajectories. 

Each model is evaluated over 10 independent trials. In addition to in-domain evaluation, we assess generalization performance under variations in lighting conditions and object layouts. Representative test scenarios and examples of successful trajectories are illustrated in Figure 5. 


_Figure 5._ Examples of real-world testing, respectively in standard, modified layouts and lights settings. 

13 

**JEPA-VLA: Video Predictive Embedding is Needed for VLA Models** 

_Table 9._ LIBERO-plus task success rate(%) of 1/10 LIBERO-Spatial training data. 

|MODEL|CAMERA|ROBOT|LANGUAGE|LIGHT|BACKGROUND|NOISE|LAYOUT|TOTAL|
|---|---|---|---|---|---|---|---|---|
|WORLDVLA|0.0|44.3|46.3|65.1|19.8|11.7|46.1|32.5|
|BASELINE|0.0|24.9|51.5|44.2|10.5|1.7|31.4|23.8|
|**W/OURS**|**0.8**|**29.7**|**53.3**|**57.2**|**44.2**|**1.4**|**44.2**|**32.1**|
|∆|0.8|4.8|1.8|13.0|33.7|-0.3|12.8|8.3|


_Table 10._ LIBERO-plus task success rate(%) of 1/10 LIBERO-Object training data. 

|MODEL|CAMERA|ROBOT|LANGUAGE|LIGHT|BACKGROUND|NOISE|LAYOUT|TOTAL|
|---|---|---|---|---|---|---|---|---|
|WORLDVLA|0.0|26.4|57.2|20.5|17.3|18.0|53.6|28.6|
|BASELINE|0.0|25.4|72.0|19.5|3.2|5.2|25.3|21.7|
|**W/OURS**|**0.0**|**33.0**|**91.5**|**35.0**|**7.3**|**6.4**|**34.7**|**29.6**|
|∆|0.0|7.6|19.5|15.5|4.1|1.2|9.4|7.9|


_Table 11._ LIBERO-plus task success rate(%) of 1/10 LIBERO-Goal training data. 

|MODEL|CAMERA|ROBOT|LANGUAGE|LIGHT|BACKGROUND|NOISE|LAYOUT|TOTAL|
|---|---|---|---|---|---|---|---|---|
|WORLDVLA|0.3|30.6|42.2|68.8|30.3|13.5|47.4|31.8|
|BASELINE|0.5|25.4|29.8|35.1|19.6|9.0|30.8|21.1|
|**W/OURS**|**0.5**|**28.9**|**39.5**|**40.5**|**36.3**|**7.7**|**36.0**|**26.2**|
|∆|0.0|3.5|9.7|5.4|16.7|-1.3|5.2|5.1|


_Table 12._ LIBERO-plus task success rate(%) of 1/10 LIBERO-Long training data. 

|MODEL|CAMERA|ROBOT|LANGUAGE|LIGHT|BACKGROUND|NOISE|LAYOUT|TOTAL|
|---|---|---|---|---|---|---|---|---|
|WORLDVLA|0.0|12.2|20.6|20.4|1.7|1.6|4.4|8.2|
|BASELINE|0.0|7.4|22.5|6.2|7.3|0.7|19.9|8.7|
|**W/OURS**|**0.5**|**11.5**|**33.2**|**19.3**|**8.0**|**0.9**|**16.4**|**12.1**|
|∆|0.5|4.1|10.7|13.1|0.7|0.2|-3.5|3.4|


14 

