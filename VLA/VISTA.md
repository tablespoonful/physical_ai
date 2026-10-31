---
title: "VISTA: Enhancing Visual Conditioning via Track-Following Preference Optimization in Vision-Language-Action Models"
date: "2026-02-04"
authors: "Yiye Chen; Yanan Jian; Xiaoyi Dong; Shuxin Cao; Jing Wu; Patricio Vela"
url: https://arxiv.org/abs/2602.05049
pdf: https://arxiv.org/pdf/2602.05049
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.05049)** / [論文ページ](https://arxiv.org/abs/2602.05049)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Enhancing Visual Conditioning via Track-Following Preference Optimization in Vision-Language-Action Models** 

**Yiye Chen**<sup>1</sup><sup>_†_</sup> **Yanan Jian**<sup>2</sup><sup>_‡_</sup> **Xiaoyi Dong**<sup>3</sup> **Shuxin Cao**<sup>1</sup> **Jing Wu**<sup>4</sup><sup>_†_</sup> **Patricio Vela**<sup>1</sup> **Benjamin E. Lundell**<sup>5</sup><sup>_‡_</sup> **Dongdong Chen**<sup>3</sup> 

# **Abstract** 

Vision–Language–Action (VLA) models have demonstrated strong performance across a wide range of robotic manipulation tasks. Despite the success, extending large pretrained VisionLanguage Models (VLMs) to the action space can induce vision-action misalignment, where action predictions exhibit weak dependence on the current visual state, leading to unreliable action outputs. In this work, we study VLA models through the lens of visual conditioning and empirically show that successful rollouts consistently exhibit stronger visual dependence than failed ones. Motivated by this observation, we propose a training framework that explicitly strengthens visual conditioning in VLA models. Our approach first aligns action prediction with visual input via preference optimization on a track-following surrogate task, and then transfers the enhanced alignment to instruction-following task through latent-space distillation during supervised finetuning. Without introducing architectural modifications or additional data collection, our method improves both visual conditioning and task performance for discrete OpenVLA, and further yields consistent gains when extended to the continuous OpenVLA-OFT setting. Project website: https://vista-vla.github.io/. 

# **1. Introduction** 

Recent research has shown increasing interest in the important challenge of developing instruction-following robots capable of completing manipulation tasks conditioned on natural language commands(Chen et al., 2021; Huang et al., 2022; Shridhar et al., 2022; 2023). Vision-Language-Action 

> _†_ Work done during an internship at Microsoft. _‡_ Work done while working at Microsoft. 1Georgia Tech 2Nvidia 3Microsoft 

> 4University of Oxford 5ARM. Correspondence to: Yiye Chen _<_ yychen2019@gatech.edu _>_ . 

_Preprint. February 6, 2026._ 


_Figure 1._ **VISTA Overview.** We align VLA action outputs to visual tracks via preference optimization, followed by supervised finetuning with latent distillation. Our experiments show that VISTA enhances visual conditioning and improves performance. 

(VLA) models seek to address this challenge by extending large Vision-Language Models (VLMs) with action prediction modules. This paradigm seeks to transfer the rich perceptual and reasoning capabilities learned during VLM pretraining to embodied action prediction. 

Despite the current success, it remains unclear to what extent the world knowledge and visual understanding encoded in VLMs effectively propagates to the VLA. Recent studies (Zhang et al., 2025; Yuan et al., 2025) suggest that information extracted from VLMs may be insufficient for embodied decision-making, due to the discrepancy of the feature granularity required by the vision-language reasoning and visuomotor control. Other work (Kachaev et al., 2025; Driess et al., 2025) further shows the degradation in the visual representation due to finetuning on the extended action output domain. These findings point to the potential _misalignment_ between perceptual understanding and action generation, wherein policies underutilize visual evidence and instead rely on spurious priors, resulting in unreliable action outputs. To mitigate this issue, existing approaches introduce auxiliary tasks, such as video prediction (Wu et al., 2024; Hu et al., 2025), dynamics understanding (Bu et al., 2025; Ye et al., 2024; Chen et al., 2025a), spatial question answering (Black et al., 2025; Zhou et al., 2025), and distil- 

1 

**Submission and Formatting Instructions for ICML 2026** 

lation from external experts (Dong et al., 2025), to enhance fine-grained visual understanding. However, despite the incured substantial training cost, it remains unclear how those external knowledge translates to better action prediction, as their impact on the policy decision is hard to characterize. 

In this paper, we study the problem through the novel lens of _visual conditioning_ , which explicitly measures the extent of the impact of visual clue on the action prediction. Intuitively, stronger visual conditioning is desirable for VLA models, as weak conditioning might indicate insufficient consideration of the current state and poor utilization of the VLM knowledge, leading to brittle action outputs. To consolidate this notion, we quantify visual conditioning by measuring the shift in the predicted action distribution under the distortion of the visual input. Under this formulation, we empirically demonstrate on the state-of-the-art VLA that successful rollouts exhibit stronger visual conditioning than failure ones, which validates the significance of visual conditioning for robust action generation. 

Based on this observation, we aim to improve VLA performance by explicitly strengthening visual conditioning during action prediction. Our approach is motivated by the success of _preference optimization_ in mitigating VLMs hallucinations, where training on pairs of preferred and dispreferred responses encourages stronger reliance on visual evidence (Peng et al., 2025; Zhou et al., 2024a; Ouali et al., 2024). However, extending preference optimization to instruction-following VLA policies is non-trivial, as constructing meaningful preference pairs requires dispreferred action chunks that are both in-distribution and less likely to accomplish the task. This necessitates costly on-policy rollouts and expert-defined trajectory ranking (Zhang et al., 2024), which limits scalability and flexibility. 

To address this challenge, we propose **_VISTA_** _: Improving Visuomotor Coordination by Aligning_ **_Vis_** _ual_ **_T_** _racks and_ **_A_** _ctions in VLA_ . The core idea of VISTA is to leverage visual tracks to make vision–action correspondence explicit, thereby enabling principled construction of preference pairs without model rollouts. As illusrated in Figure 1, VISTA augments standard supervised fine-tuning (SFT) with two additional training stages. In the first stage, we apply Direct Preference Optimization (Rafailov et al., 2023) to the _trackfollowing_ task, where the VLA model predicts actions based on track-annotated images. The track-following data are readily constructed from the instruction-following dataset by annotating the image with pixel tracks and applying minimal prompt modifications. Preference pairs are then constructed entirely offline via in-batch pairing, which treats action chunks from other samples within the same batch as dispreferred responses. We show that the track-following DPO implicitly optimizes inverse dynamics understanding in the VLA policy and greatly improves visual conditioning 

during action prediction. In the second stage, VISTA performs instruction-following SFT with feature-space distillation from the frozen track-following model, which leverages the correspondence between the two tasks to transfer the enhanced visual grounding to the target task. 

Without introducing architectural changes, auxiliary datasets, or on-policy rollouts, VISTA consistently improves visual conditioning and performance in the vanilla discrete autoregressive VLA model. In particular, it improves OpenVLA (Kim et al., 2024) by 3 _._ 15% in average success rate on the LIBERO benchmark, demonstrating the benefit of strengthening visual conditioning through training. Moreover, we also show that our method naturally extends to continuous parallel-decoding architectures by modifying only the final training stage. This simple extension improves OpenVLA-OFT (Kim et al., 2025) on Calvin ABC _→_ D from 3 _._ 87 to 4 _._ 02 in average task completion count, corresponding to a 4% relative improvement. 

In summary, our contributions are: 

- We study Vision-Language-Action (VLA) models through the novel lens of _visual conditioning_ and demonstrate its importance for VLA performance. 

- We introduce VISTA, a new training framework that improves visual conditioning in VLA policies by aligning action predictions to visual tracks. 

- We show that VISTA enhances visual conditioning and consistently improves the performance of both discrete OpenVLA and continuous OpenVLA-OFT on standard benchmarks. 

# **2. Related Works** 

**Vision-Language-Action Models** Early work in robot learning leverages vision and language foundation models as modular components within larger systems (Yang et al., 2023; Rana et al., 2023; Chen et al., 2025b; Huang et al., 2023). More recent efforts instead focus on endowing large pretrained Vision–Language Models (VLMs) with end-to-end action prediction capabilities. By tokenizing actions through discretization (Brohan et al., 2022; Kim et al., 2024) or frequency decomposition (Pertsch et al., 2025), the vanilla discrete autoregressive VLA models achieve strong performance powered by large-scale action-labeled datasets (Wang et al., 2024; Black et al., 2025). Moderate architectural extensions, such as continuous-action experts (Kim et al., 2025; Wang et al., 2025a; Li et al., 2024) and paralleldecoding schemes (Kim et al., 2025; Zhao et al., 2025), have further improved the model expressivity and performance. 

Despite the progress, recent studies report lack of finegrained visual feature in VLM for embodied tasks (Zhang 

2 

**Submission and Formatting Instructions for ICML 2026** 

et al., 2025; Hancock et al., 2025; Yuan et al., 2025; Chen et al., 2024) or degraded multimodal representation during VLA finetuning (Kachaev et al., 2025; Dong et al., 2025; Driess et al., 2025). A broad line of work seeks to address the issue by injecting world knowledge into VLAs, through the task of latent action modeling (Chen et al., 2025a; Ye et al., 2024; Bu et al., 2025), embodied vision-language reasoning (Zhou et al., 2025; Zawalski et al., 2024), dynamic modeling (Wang et al., 2025b; Li et al., 2025; Bi et al., 2025), or video prediction (Zhao et al., 2025; Bu et al., 2024b; Black et al., 2024; Wu et al., 2024). However, these approaches rely on auxiliary objectives whose impact on instruction-following action prediction is indirect and difficult to quantify, especially given separate training stages or distinct internal computation paths. In contrast, we explicitly quantifies visual clue utilization in action generation, and propose a training method to enhance visual grounding. 

**Visual Track Guidance in Robot Learning** Visual tracks, which depict pixel-level trajectories, have been widely used as a general representation of scene dynamics across diverse applications (Zholus et al., 2025; Geng et al., 2025). In robotics, visual track has facilitated policy training by serving as intermediate motion representations (Wen et al., 2023; Bharadhwaj et al., 2024) and enabling the extraction of dynamic knowledge from generic video data (Ren et al., 2025). In the context of VLA models, LLARVA (Niu et al., 2024) employs future track prediction as an auxiliary objective, while TraceVLA (Zheng et al., 2024) uses visual tracks to represent historical action context. In contrast, we leverage visual tracks to formulate a preference optimization objective to align action prediction with visual input. 

**Multimodal Alignment and Preference Optimization** Multimodal misalignment is a central challenge for large multimodal models. In Vision Language Models (VLMs), such misalignment often manifests as underutilization of visual input, leading to hallucinated output (Shu et al., 2025; Liu et al., 2023b). Preference optimization has emerged as an effective strategy to address the issue, in which the models are trained on paired preferred and dispreferred responses for stronger visual grounding (Zhou et al., 2024a; Zhao et al., 2023; Ouali et al., 2024; Zhou et al., 2024b). In this paper, we study VLAs through the same lens, by showing the connection between visual conditioning and action prediction performance. Building on this insight, we introduce a preference optimization framework that aligns action prediction with visual input, strengthening visual grounding and improving downstream performance. 

# **3. Visual Conditioning in VLA Models** 

## **3.1. VLA Preliminaries** 

**Problem Formulation** We consider the problem of building a VLA model _πθ_ , parameterized by _θ_ , which processes a language instruction _g_ and a third-person RGB observation _ot_ at time step _t_ , and outputs a chunk of _H_ actions _at_ : _t_ + _H_ : 


Although some work incorporates additional inputs such as robot proprioception and wrist-camera images, we exclude those modalities in all experiments for fair comparison. 

**Standard VLA Structures** The VLA model _π_ consists of a multimodal backbone _f_ that encodes inputs into a set of _M_ latents, followed by an action expert _ϕ_ that maps these latents to the actions. Two main categories of _ϕ_ involve: Existing VLA approaches broadly fall into two representative categories based on the design of attention in _f_ and architecture of _ϕ_ : (1) Vainlla _autoregressive discrete_ formulation, which inherits the autoregressive backbone and token classification head from VLMs and outputs a distribution over a set of discrete action tokens: _at_ : _t_ + _H ∼ π_ ( _·|ot, g_ ); (2) Extended _parallel-decoding continuous_ formulation, which adopts parallel-decoding attention and replaces the token head with a regression expert from the scratch that directly outputs the actions: _at_ : _t_ + _H_ = _π_ ( _ot, g_ ). 

In this work, we study training method under both formulations through OpenVLA (Kim et al., 2024) and OpenVLAOFT (Kim et al., 2025) architectures. In both cases, _f_ is finetuned from Prismatic VLM (Karamcheti et al., 2024), and each output latent corresponds to one action dimension, leading to _M_ = 7 _H_ for a standard 7-DoF action space (translation, rotation, gripper). OpenVLA instantiates the autoregressive discrete formulation, whereas OpenVLA-OFT realizes the parallel-decoding continuous scheme, where _ϕ_ is implemented as a 4-layer MLP network. 

**Instruction-following Dataset** Training of a VLA requires an instruction-following dataset _D_ = _{_ ( _ζ, g_ ) _}_ , where the trajectory _ζ_ records a sequence of actions and observations to accomplish the task _g_ given initial observation _o_ 1: _ζ_ = _{_ ( _ot, at_ ) _}_<sup>_T_</sup> _t_ =1<sup>.The trajectories are further segmented</sup> into action chunks of fixed length _H_ via sliding window, which supervises the outputs of VLA formulated in Eq. 1. 

## **3.2. Quantifying Visual Conditioning** 

Inspired by Visual Contrastive Decoding (VCD) (Leng et al., 2024), we probe visual conditioning in the autoregressive discrete VLA by measuring the sensitivity of action predictions to visual input. Formally, we define the visual conditioning at token position _τ_ as the KL-divergence between the predicted action token distributions conditioned 

3 

**Submission and Formatting Instructions for ICML 2026** 

on the original and perturbed observations, respectively: 


where _a_<sup>_<τ_</sup> _t_ are predicted tokens prior to position _τ_ . _o_<sup>_′_</sup> _t_<sup>is</sup> the distorted image based on _ot_ . We follow VCD to implement the distortion as the forward diffusion process (Ho et al., 2020), by repetitively shrinking the original image and adding Gaussian noise for _K_ step. Equivalently, _o_<sup>_′_</sup> _t_<sup>is</sup> sampled from the following distribution: 


where **I** refers to an identity matrix. We follow VCD to set _K_ = 999 and schedule the variance linearly from _β_ 1 = 10<sup>_−_5</sup> to _βK_ = 0 _._ 005. 

## **3.3. Visual Conditioning and VLA Performance** 

We begin by probing visual conditioning in OpenVLA finetuned on LIBERO-Spatial benchmark (Sec. 5.1.1) with chunk size _H_ = 8 (i.e. _M_ = 56). Using the definition in Eq. (2), we measure visual conditioning across all output tokens over 100 rollouts (10 tasks with 10 rollouts per task). Rollouts are categorized into successful and failed groups based on simulation outcomes, and we report the mean and standard deviation aggregated over time steps and rollouts. 

As shown in Figure 2, successful rollouts consistently exhibit stronger visual conditioning than failed ones. This gap is most pronounced for early action tokens, which depend more heavily on visual input due to limited preceding token predictions. These results establish a clear correlation between visual conditioning and VLA performance, which supports our notion that effective VLA policy requires strong visual grounding. Motivated by the observation, we design a training approach to explicitly enhance vision-action alignment in Sec. 4. As previewed in Figure 2, our method increases visual conditioning in OpenVLA, and leads to consistent performance improvement across multiple benchmarks as discussed in Sec. 5. 

# **4. Methodology** 

As illusrated in Figure 3, VISTA involves 3 training stages. In Stage 0, we begin with standard instruction-following supervised fine-tuning (SFT) on a discrete autoregressive VLA, which provides a base model for the subsequent stages. In Stage 1 (Sec. 4.1), we produce track-following data from the instruction-following dataset _D_ and apply Direct Preference Optimization (DPO) to enhance vision-action alignment. In Stage 2 (Sec. 4.2), we propagate the enhanced 


_Figure 2._ **Visual Conditioning of the 8-step OpenVLA and VISTA (Ours) in LIBERO-Spatial** . The periodic vertical grids indicate that each block of seven tokens decodes to a single action, leading to 56 output tokens for 8 actions. 

alignment to the instruction-following task of interest by additional SFT with latent distillation from the frozen copy of track-aligned VLA. 

## **4.1. Track-Follow Preference Optimization** 

## 4.1.1. TRACK-FOLLOWING DPO DESIGN 

**Track-following Preference Dataset Construction.** This stage starts from a base instruction-following VLA model to improve its visual conditioning via preference optimization. To avoid the need for costly on-policy rollouts and expert-defined rewards when defining preference pairs for instruction-following tasks (Zhang et al., 2024), we instead formulate preference optimization for the _track-following_ task, where the action prediction is guided by the annotated tracks on the image. These tracks establish deterministic correspondence between visual input and action chunks output, enabling principled preference construction directly from the offline instruction-following dataset _D_ . 

We first construct a track-following dataset _D_<sup>˜</sup> by annotating _D_ . Specifically, for each time step _t_ within trajectory _ζ_ , we employ an off-the-shelf point tracking model to track _N_ points over the next _H_ frames ( _ot, ot_ +1 _, . . . , ot_ + _min_ ( _t_ + _H−_ 1 _,T_ )). Following TraceVLA (Zheng et al., 2024) we retain only the active points by filtering based on L1 moving distances, and then randomly sample _n_ active tracks. These tracks are overlaid on the initial frame _ot_ to produce a track-annotated image ˜ _ot_ , which depicts both the current state and the future dynamics given the labeled actions. By repeating the process for all frames in _D_ , we obtain the track-following dataset _D_<sup>˜</sup> = _{_ ( _ζ,_<sup>˜</sup> ˜ _g_ ) _}_ , where the track-annotated trajectory _ζ_<sup>˜</sup> = _{_ (˜ _ot, at_ ) _}_<sup>_T_</sup> _t_ =1<sup>, and</sup> _g_ ˜ is the updated prompt as shown in Figure 3. 

We then construct track-following preference pairs on _D_<sup>˜</sup> via _in-batch preference pairing_ . Since visual tracks deterministically specify the preferred actions, action chunks drawn from other batch samples can naturally serve as in-distribution yet visuallly misaligned responses. Concretely, given a randomly shuffled track-following batch 

4 

**Submission and Formatting Instructions for ICML 2026** 


_Figure 3._ **VISTA Methodology** . Starting from a vanilla instruction-following SFT model, we apply DPO on track-following preference samples constructed from the instruction-following dataset to align action prediction with visual input. We then transfer the alignment to the instruction-following policy via latent distillation, resulting in enhanced visual conditioning and VLA performance. 

_{_ (˜ _o_<sup>_b_</sup> _t_<sup>_,_˜</sup><sup>_gb, ab_</sup> _t_ : _t_ + _H_<sup>)</sup><sup>_}_</sup> _b_<sup>_B_</sup> =1<sup>, where</sup><sup>_B_is set as even, we create the</sup> preference batch _{_ (˜ _o_<sup>_b_</sup> _t_<sup>_,_˜</sup><sup>_gb, ab_</sup> _w_<sup>_, ab_</sup> _l_<sup>)</sup><sup>_}B_</sup> _b_ =1<sup>, where the preferred</sup> _a_<sup>_b_</sup> _w_<sup>and dispreferred</sup><sup>_ab_</sup> _l_<sup>are set as:</sup> 

(Du et al., 2023; Tian et al., 2024), we show that our designed DPO program implicitly achieves this. As derived in Rafailov et al. (2023), the DPO program in Eq. 5 implicitly optimizes the following RL objective: 


**Track-following DPO Formulation** With the trackfollowing preference data, we align action predictions to visual tracks via Direct Preference Optimization (DPO) (Rafailov et al., 2023). We optimize the objective: 


where _σ_ denotes the logistic function and _α_ controls the deviation from the reference policy _πref_ , which is fixed as the frozen Stage 0 SFT model. Here, _π_ ( _a_ ; ˜ _o,_ ˜ _g_ ) is the conditional likelihood of an action chunk estimated by the autoregressive VLA model, which is calculated as the sequential product of the token-level probabilities from the model outputs. By contrasting against preferred and dispreferred action chunks based on the visual track guidance, DPO encourages the policy to align predictions with visual evidence, thereby strengthening the visual conditioning. 

## 4.1.2. TRACK-FOLLOWING DPO IMPLICITLY TRAINS INVERSE DYNAMICS UNDERSTANDING 

Unlike prior approaches that explicitly learn inverse dynamics that recover actions based on the current and future states 

where the reward is estimated via the binary preference classification under the Bradley-Terry preference model (Bradley & Terry, 1952): 


Because preference pairs ( _aw, al_ ) are constructed from action chunks that are aligned or misaligned with _o_ ˜, which encodes both the current visual state and future evolution through visual tracks, the learned reward function evaluates how consistent an action chunk is with the observed visual motion. Consequently, maximizing the reward, maximizing the reward encourages the policy to infer the action configurations encoded by visual tracks, thereby inducing inverse dynamics understanding within the policy model. 

## **4.2. Instruction-Following SFT with Latent Distillation** 

While the track-following DPO stage strengthens visual conditioning, the target instruction-following task does not provide visual track guidance at inference. To transfer the improved vision–action alignment to instruction-following policies, we introduce a final training stage of SFT with latent-space distillation. 

5 

**Submission and Formatting Instructions for ICML 2026** 

Specifically, given the aligned autoregressive VLA _π_ align, we freeze it as a teacher model and initialize a trainable student _πθ_ from its weights. We then optimize _πθ_ using the paired instruction and track-following _D_ and _D_<sup>˜</sup> , where each track-following sample is a track-annotated counterpart of an instruction-following sample. The training objective: 


where _ℓSF T_ is standard SFT loss, and _ℓsim_ encourages the student to match the latent produced by the aligned teacher, thereby preserving the strengthened visual grounding. 

Importantly, this distillation-based SFT framework allows the student _πθ_ to differ from _π_ align in architecture. In our experiments, _π_ align is consistently instantiated as a discrete autoregressive OpenVLA model from prior stages, while _πθ_ is either kept as the same or updated into a continuous parallel-decoding OpenVLA-OFT. Accordingly, _ℓ_ SFT corresponds to the discrete next-token prediction loss or the continuous _L_ 1 regression loss. We empirically show that this procedure consistently improves performance in both settings, which indicates that the learned vision–action alignment transfers effectively across architectures. 

## **4.3. Implementation Details** 

In this work, we use off-the-shelf BootsTAPNext (Zholus et al., 2025) as the tracker. We track _N_ = 900 points on an uniform grid on the image and randomly sample _n_ = 16 active tracks for annotation. The DPO parameter is fixed to _α_ = 0 _._ 1. Unless otherwise specified, distillation loss _ℓ_ sim is set as the negative mean cosine similarity. We denote the discrete and continuous instantiation of our method as **VISTA** and **VISTA-OFT** , respectively. For VISTA, all three training stages utilize OpenVLA-7B. For VISTA-OFT, the first two stages use OpenVLA-7B, while the final stage switches to the OpenVLA-OFT-7B. We adopt LoRA (Hu et al., 2022) with rank=32 in all training. 

# **5. Experiments** 

## **5.1. LIBERO Benchmark Evaluation** 

## 5.1.1. EXPERIMENTAL SETUPS 

**Evaluation Settings** We first evaluate VISTA on the LIBERO manipulation benchmark (Liu et al., 2023a) to verify if our method improves visual conditioning and model performance. VISTA-OFT is excluded from this experiment and is evaluated only on the larger CALVIN benchmark (Sec. 5.2) due to its stronger expressivity. As shown in Figure 4, LIBERO consists of four suites: Spatial, Object, Goal, 

and Long. Each suite contains 10 tasks, with 50 demonstrations per task for training. We preprocess the data following OpenVLA (Kim et al., 2024) to upscale the image resolution to 256 _×_ 256, exclude failure trajectories, and remove static actions. Each method is evaluated under the success rate (SR) on 500 episodes per suite (10 tasks _×_ 50 episodes per task). The training configuration of VISTA is detailed in Appendix A.3. 

**Ablation on Distillation Function** We further ablate the choice of distillation loss _ℓ_ sim on LIBERO by replacing the negative cosine similarity with an L2 distance. The resulting variant is denoted as _VISTA (L2)_ . 

**Baselines** We compare against OpenVLA (Kim et al., 2024) trained with vanilla SFT under both _H_ = 8 and its original _H_ = 1. We additionally compare with TraceVLA (Zheng et al., 2024), which adopts the same OpenVLA architecture but augments it with historical visual trace inputs. Further state-of-the-art baselines include Diffusion Policy (Chi et al., 2023), LAPA (Ye et al., 2024), Octo (Team et al., 2024), and SpatialVLA (Qu et al., 2025). All methods are evaluated using only static third-person RGB observations. 

## 5.1.2. EXPERIMENTAL RESULTS 

For OpenVLA-8Step, VISTA, and VISTA (L2), we report the results with Receding Horizon Control (RHC), executing only the first 4 actions out of the predicted _H_ = 8 before replanning. We found that RHC improves their performance in the relatively small LIBERO benchmark. Performance without RHC is reported in Appendix B.1 

**Overall Results.** The results are summarized in Table 2. Without introducing any model architectural modifications or additional training data, VISTA consistently improves upon OpenVLA across all LIBERO suites, achieving an average SR gain of 3 _._ 1%. Coupled with the improved visual conditioning shown in Figure 2, these performance gains validate our training design and support our hypothesis that stronger visual conditioning benefits VLA performance. Moreover, VISTA surpasses other baselines including TraceVLA, justifying the performance the gains from improved training recipe relative to the mere inclusion of track guidance. Overall, VISTA demonstrates competitive performance relative to all evaluated baselines. 

**Distillation Function Ablation Results.** As shown in Table 2, VISTA (L2) variant also outperforms the baseline OpenVLA, which further demonstrate the effectiveness of our method regardless of the distillation loss instantiation. However, compared to cosine similarity, the L2 variant achieves an average SR that is 0 _._ 5% lower, with less consistent gains across task suites due to the 1 _._ 9% decrease 

6 

### **Submission and Formatting Instructions for ICML 2026** 


_Figure 4._ Illustration of benchmarks. 

|Method||Task com|pleted in a|row (%)_↑_||Avg.|
|---|---|---|---|---|---|---|
||1|2|3|4|5|Len.|
|SuSIE|87.0|69.0|49.0|38.0|26.0|2.69|
|GR-1|85.4|71.2|59.6|49.7|40.1|3.06|
|VPP|90.9|81.5|71.3|62.0|51.8|3.58|
|DITA|94.5|82.5|72.8|61.3|50.0|3.61|
|CLOVER|96.0|83.5|70.8|57.5|45.4|3.53|
|RoboDual|94.4|82.7|72.1|62.4|54.4|3.66|
|RoboVLMs|93.1|83.6|75.2|68.3|61.6|3.82|
|UniVLA|95.5|85.8|75.4|66.9|56.5|3.80|
|ReconVLA|95.6|87.6|76.9|69.3|64.1|3.95|
|OpenVLA<sup>_∗_</sup>|92.8|78.3|63.7|52.3|44.0|3.31|
|VISTA|93.5|78.6|64.6|53.9|43.1|3.34|
||(+0.7)|(+0.3)|(+0.9)|(+1.6)|(-0.9)|(+0.03)|
|OpenVLA-OFT<sup>_∗_</sup>|92.1|83.2|76.3|70.9|64.3|3.87|
|VISTA-OFT|94.8|87.5|80.1|73.3|66.6|**4.02**|
||(+2.7)|(+4.3)|(+3.8)|(+2.4)|(+2.3)|(+0.15)|


_Table 1._ **CALVIN ABC** _→_ **D Evaluation Results** . Green (red) numbers indicate performance gains (drops) relative to the OpenVLA or OpenVLA-OFT counterpart.<sup>_∗_</sup> Results are reproduced 

|Methods|Spatial|Object|Goal|Long|Mean|
|---|---|---|---|---|---|
|Diffusion Policy|78.3|92.5|68.3|50.5|72.4|
|Octo|78.9|85.7|84.6|51.1|75.1|
|LAPA|73.8|74.6|58.8|55.4|65.7|
|TraceVLA|84.6|85.2|75.1|54.1|74.8|
|SpatialVLA|88.2|89.9|78.6|55.5|78.1|
|OpenVLA-1Step|84.7|88.4|79.2|53.7|76.5|
|OpenVLA-8Step<sup>_∗_</sup>|79.6|88.6|82.4|54.4|76.3|
|VISTA (L2)|87.8|89.4|80.5|58.6|79.1|
||(+8.2)|(+0.8)|(-1.9)|(+4.9)|(+2.6)|
|VISTA|84.8|91.6|84.2|57.0|**79.4**|
||(+5.2)|(+3.0)|(+1.8)|(+2.6)|(+3.1)|


_Table 2._ **LIBERO Evaluation Results.** VISTA improves upon OpenVLA and outperforms a range of baseline methods. Green (red) numbers indicate performance gains (drops) relative to the OpenVLA-8Step counterpart.<sup>_∗_</sup> Results are reproduced. 

relative to OpenVLA on LIBERO-Goal. Hence, we default to the cosine similarity in remaining experiments. 

## **5.2. Calvin Benchmark Evaluation** 

## 5.2.1. EXPERIMENTAL SETUPS 

**Evaluation Settings** Next, we evaluate the generalization and long-horizon instruction-following capacities of VLA models on the CALVIN (Mees et al., 2022) manipulation benchmark, which comprises 4 environments (A–D) as illustrated in Figure 4. We focus on the most challenging ABC _→_ D setting, where policies are trained on environments A–C and evaluated on D to test the generalization capacity. Our training is conducted using only the subset annotated with language instruction, which includes 17 _,_ 870 episodes spanning 34 diverse tasks. Evaluation follows the 

Long-Horizon Multi-Task Language Control protocol, under which the models are tested in 1000 sequences of five sequential tasks. Within each sequence, the policy must solve each new task starting from the final state of the previous, which increases difficulty due to broader state-space coverage. Performance is measured by per-task completion rate and the average task completion length. We evaluate both VISTA and VISTA-OFT, with detailed training configurations listed in Appendix. A.3. 

**Baselines** We compare VISTA and VISTA-OFT against OpenVLA and OpenVLA-OFT to highlight the advantage of the proposed training method. We further benchmark diverse VLA designs, including RoboDual (Bu et al., 2024a), which is a cooperation system of the OpenVLA and a trained specialist, and DITA (Hou et al., 2025), which is a generalist policy based on Diffusion Transformer (DiT). Other than that, we benchmark a range of VLAs that incorporate additional action-free vision-language auxiliary tasks, including SuSIE (Black et al., 2024), CLOVER (Bu et al., 2024b), GR-1 (Wu et al., 2024), VPP (Hu et al., 2025), UniVLA (Bu et al., 2025), and ReconVLA (Song et al., 2025). Note that for RoboVLMs and VPP, we tabulate their best performance under the single static third-person view setting. 

## 5.2.2. EXPERIMENTAL RESULTS 

As shown in Table 1, our training method consistently improves both OpenVLA and OpenVLA-OFT in average length. In particular, VISTA-OFT improves the task completion rate across all tasks of OpenVLA-OFT by more than 2 _._ 3% and yields a 4% relative increase in average completion length. This suggests that our designed track-following 

7 

**Submission and Formatting Instructions for ICML 2026** 


_Figure 5._ **Analysis and Ablation on LIBERO-Spatial** . **(A)** Change of visual conditioning during the VISTA training stages; **(B)** Ablation on the visual conditioning and VLA performance of alternative training strategies. 

DPO extracts latents richer with vision and dynamic information, which guides better action generation. What’s more, despite relying on no external non-robotic dataset for additional pretraining or co-finetuning, VISTA-OFT surpasses a series of baselines in this category, and achieves the state-ofthe-art performance in the CALVIN ABC _→_ D benchmark. This further supports the efficacy of our training method designed to enhance visual conditioning. 

## **5.3. Analysis and Ablation** 

**Change of model visual conditioning during VISTA training.** To examine how VISTA modulates visual conditioning in VLA models, we track its evolution across all training stages using the metric defined in Eq. 2. Specifically, we measure the visual conditioning of the discrete VISTA at each stage on a 200 randomly sampled time steps from the LIBERO-Spatial training split. Models from Stages 0 and 2 are evaluated on the instruction-following task with track-free images, while the Stage 1 model is evaluated on the track-following task with track-annotated observations. 

Results are shown in Figure 5(A). The model trained solely with instruction-following SFT (Stage 0, equivalent to OpenVLA) exhibits the weakest visual conditioning, with nearzero values for some tokens, indicating complete ignorance of visual clue. Applying track-following DPO in Stage 1 substantially increases visual conditioning. Although the subsequent instruction-following training slightly reduces this effect, the final model retains markedly stronger visual conditioning than the Stage 0 baseline thanks to our distillation design. These results support our claim that VISTA improves visual grounding of the VLA model, which explains its performance gain compared to OpenVLA. 

**Ablation on alternative strategies.** We further validate our design by comparing VISTA against two naive alternatives: (1) _DPO-then-SFT_ applies track-following DPO followed by instruction-following SFT without latent dis- 

tillation, analogous to a single iteration of DPO and SFT as in GRAPE (Zhang et al., 2024). and serves to validate the efficacy of adding distillation loss _L_ Distill as in VISTA; This baseline isolates the contribution of the distillation loss _L_ Distill. (2) _Co-SFT_ , performs a single-stage SFT on a mixture of instruction-following and track-following data, which resembles approaches that jointly train on action prediction and auxiliary world-modeling objectives. 

Figure 5(B) shows visual conditioning and performance for all methods. We observe the same ordering in both metrics: VISTA achieves the highest visual conditioning and performance, followed by DPO-then-SFT, and then Co-SFT. This monotonic trend further justifies the clear correlation between visual conditioning and downstream VLA performance empirically. Co-SFT yields the weakest visual conditioning and lowest performance, indicating that naive co-training with auxiliary objectives is insufficient for improving visual grounding. While DPO-then-SFT improves upon Co-SFT, it remains inferior to VISTA, underscoring the importance of latent distillation for effectively transferring visual grounding to instruction-following policies. 

# **6. Conclusion** 

Our work examines the visual conditioning in VLA, which is quantified as the impact of visual clue on the output action distribution, and show its correlation with the VLA model performance. Motivated by this finding, we further propose a VLA training recipe, named VISTA, that aligns the action prediction with the visual track guidance. Our experiments show that VISTA facilitates the visual grounding, and consistently improves the VLA performance under both the naive discrete autoregressive and the continuous parallel-decoding (i.e. OFT) configurations. 

Due to compute constraints, our study focuses on the finetuning stage. However, we hope that this work can inspire future efforts on aligning action predictions with visual in- 

8 

**Submission and Formatting Instructions for ICML 2026** 

puts in VLAs through extensive pretraining with mixed action-free video data, which can potentially enhances the performance and generalizability of VLA models. 

# **Impact Statement** 

Our work aims to advance command-following robotic manipulation, enabling robots to physically interact with the environment in response to human instructions. Such capabilities have the potential to improve efficiency across many societal activities. By enhancing the visual dynamic understanding in a robot, our method represents a step toward more robust and reliable manipulation systems. 

# **References** 

- Bharadhwaj, H., Mottaghi, R., Gupta, A., and Tulsiani, S. Track2act: Predicting point tracks from internet videos enables generalizable robot manipulation. In _European Conference on Computer Vision_ , pp. 306–324. Springer, 2024. 

- Bi, H., Tan, H., Xie, S., Wang, Z., Huang, S., Liu, H., Zhao, R., Feng, Y., Xiang, C., Rong, Y., et al. Motus: A unified latent action world model. _arXiv preprint arXiv:2512.13030_ , 2025. 

- Black, K., Nakamoto, M., Atreya, P., Walke, H. R., Finn, C., Kumar, A., and Levine, S. Zero-shot robotic manipulation with pre-trained image-editing diffusion models. In _The Twelfth International Conference on Learning Representations_ , 2024. URL https://openreview. net/forum?id=c0chJTSbci. 

- Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M. R., Finn, C., Fusai, N., Galliker, M. Y., Ghosh, D., Groom, L., Hausman, K., ichter, b., Jakubczak, S., Jones, T., Ke, L., LeBlanc, D., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Ren, A. Z., Shi, L. X., Smith, L., Springenberg, J. T., Stachowicz, K., Tanner, J., Vuong, Q., Walke, H., Walling, A., Wang, H., Yu, L., and Zhilinsky, U. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In Lim, J., Song, S., and Park, H.-W. (eds.), _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pp. 17–40. PMLR, 27–30 Sep 2025. URL https://proceedings.mlr.press/ v305/black25a.html. 

- Bradley, R. A. and Terry, M. E. Rank analysis of incomplete block designs: I. the method of paired comparisons. _Biometrika_ , 39(3/4):324–345, 1952. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., 

Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Bu, Q., Li, H., Chen, L., Cai, J., Zeng, J., Cui, H., Yao, M., and Qiao, Y. Towards synergistic, generalized, and efficient dual-system for robotic manipulation. _arXiv preprint arXiv:2410.08001_ , 2024a. 

- Bu, Q., Zeng, J., Chen, L., Yang, Y., Zhou, G., Yan, J., Luo, P., Cui, H., Ma, Y., and Li, H. Closed-loop visuomotor control with generative expectation for robotic manipulation. _Advances in Neural Information Processing Systems_ , 37:139002–139029, 2024b. 

- Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., and Li, H. Univla: Learning to act anywhere with taskcentric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 

- Chen, B., Xu, Z., Kirmani, S., Ichter, B., Sadigh, D., Guibas, L., and Xia, F. Spatialvlm: Endowing vision-language models with spatial reasoning capabilities. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 14455–14465, 2024. 

- Chen, Y., Xu, R., Lin, Y., and Vela, P. A. A joint network for grasp detection conditioned on natural language commands. In _International Conference on Robotics and Automation (ICRA)_ , pp. 4576–4582. IEEE, 2021. 

- Chen, Y., Ge, Y., Tang, W., Li, Y., Ge, Y., Ding, M., Shan, Y., and Liu, X. Moto: Latent motion token as the bridging language for learning robot manipulation from videos. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 19752–19763, 2025a. 

- Chen, Y., Sawhney, H., Gyde, N., Jian, Y., Saunders, J., Vela,´ P., and Lundell, B. Schema-guided scene-graph reasoning based on multi-agent large language model system. In _The Fortieth AAAI Conference on Artificial Intelligence_ , 2025b. 

- Chi, C., Feng, S., Du, Y., Xu, Z., Cousineau, E., Burchfiel, B., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. In _Robotics: Science and Systems_ , 2023. 

- Dong, S., Fu, C., Gao, H., Zhang, Y.-F., Yan, C., Wu, C., Liu, X., Shen, Y., Huo, J., Jiang, D., et al. Vita-vla: Efficiently teaching vision-language models to act via action expert distillation. _arXiv preprint arXiv:2510.09607_ , 2025. 

- Driess, D., Springenberg, J. T., Ichter, B., Yu, L., Li-Bell, A., Pertsch, K., Ren, A. Z., Walke, H., Vuong, Q., Shi, L. X., et al. Knowledge insulating vision-language-action models: Train fast, run fast, generalize better. _arXiv preprint arXiv:2505.23705_ , 2025. 

9 

**Submission and Formatting Instructions for ICML 2026** 

- Du, Y., Yang, S., Dai, B., Dai, H., Nachum, O., Tenenbaum, J., Schuurmans, D., and Abbeel, P. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 

- Geng, D., Herrmann, C., Hur, J., Cole, F., Zhang, S., Pfaff, T., Lopez-Guevara, T., Aytar, Y., Rubinstein, M., Sun, C., et al. Motion prompting: Controlling video generation with motion trajectories. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1–12, 2025. 

- Hancock, A. J., Wu, X., Zha, L., Russakovsky, O., and Majumdar, A. Actions as language: Fine-tuning vlms into vlas without catastrophic forgetting. _arXiv preprint arXiv:2509.22195_ , 2025. 

- Ho, J., Jain, A., and Abbeel, P. Denoising diffusion probabilistic models. _Advances in neural information processing systems_ , 33:6840–6851, 2020. 

- Hou, Z., Zhang, T., Xiong, Y., Duan, H., Pu, H., Tong, R., Zhao, C., Zhu, X., Qiao, Y., Dai, J., and Chen, Y. Dita: Scaling diffusion transformer for generalist visionlanguage-action policy. _arXiv preprint arXiv:2503.19757_ , 2025. 

- Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W., et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- Hu, Y., Guo, Y., Wang, P., Chen, X., Wang, Y.-J., Zhang, J., Sreenath, K., Lu, C., and Chen, J. Video prediction policy: A generalist robot policy with predictive visual representations. In _Forty-second International Conference on Machine Learning_ , 2025. URL https: //openreview.net/forum?id=c0dhw1du33. 

- Huang, W., Xia, F., Xiao, T., Chan, H., Liang, J., Florence, P., Zeng, A., Tompson, J., Mordatch, I., Chebotar, Y., et al. Inner monologue: Embodied reasoning through planning with language models. _arXiv preprint arXiv:2207.05608_ , 2022. 

- Huang, W., Wang, C., Zhang, R., Li, Y., Wu, J., and Fei-Fei, L. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ , 2023. 

- Kachaev, N., Kolosov, M., Zelezetsky, D., Kovalev, A. K., and Panov, A. I. Don’t blind your vla: Aligning visual representations for ood generalization, 2025. URL https://arxiv.org/abs/2510.25616. 

- Karamcheti, S., Nair, S., Balakrishna, A., Liang, P., Kollar, T., and Sadigh, D. Prismatic vlms: Investigating 

the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Leng, S., Zhang, H., Chen, G., Li, X., Lu, S., Miao, C., and Bing, L. Mitigating object hallucinations in large visionlanguage models through visual contrastive decoding. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 13872–13882, 2024. 

- Li, S., Gao, Y., Sadigh, D., and Song, S. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025. 

- Li, X., Li, P., Liu, M., Wang, D., Liu, J., Kang, B., Ma, X., Kong, T., Zhang, H., and Liu, H. Towards generalist robot policies: What matters in building vision-language-action models. _arXiv preprint arXiv:2412.14058_ , 2024. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023a. 

- Liu, F., Lin, K., Li, L., Wang, J., Yacoob, Y., and Wang, L. Mitigating hallucination in large multi-modal models via robust instruction tuning. _arXiv preprint arXiv:2306.14565_ , 2023b. 

- Mees, O., Hermann, L., Rosete-Beas, E., and Burgard, W. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

- Niu, D., Sharma, Y., Biamby, G., Quenum, J., Bai, Y., Shi, B., Darrell, T., and Herzig, R. Llarva: Vision-action instruction tuning enhances robot learning. _arXiv preprint arXiv:2406.11815_ , 2024. 

- Ouali, Y., Bulat, A., Martinez, B., and Tzimiropoulos, G. Clip-dpo: Vision-language models as a source of preference for fixing hallucinations in lvlms. In _European Conference on Computer Vision_ , pp. 395–413. Springer, 2024. 

- Peng, S., Yang, S., Jiang, L., and Tian, Z. Mitigating object hallucinations via sentence-level early intervention. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 635–646, 2025. 

10 

**Submission and Formatting Instructions for ICML 2026** 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Rafailov, R., Sharma, A., Mitchell, E., Manning, C. D., Ermon, S., and Finn, C. Direct preference optimization: Your language model is secretly a reward model. _Advances in neural information processing systems_ , 36: 53728–53741, 2023. 

- Rana, K., Haviland, J., Garg, S., Abou-Chakra, J., Reid, I., and Suenderhauf, N. Sayplan: Grounding large language models using 3d scene graphs for scalable robot task planning. _arXiv preprint arXiv:2307.06135_ , 2023. 

- Ren, J., Sundaresan, P., Sadigh, D., Choudhury, S., and Bohg, J. Motion tracks: A unified representation for human-robot transfer in few-shot imitation learning. _arXiv preprint arXiv:2501.06994_ , 2025. 

- Shridhar, M., Manuelli, L., and Fox, D. Cliport: What and where pathways for robotic manipulation. In Faust, A., Hsu, D., and Neumann, G. (eds.), _Proceedings of the 5th Conference on Robot Learning_ , volume 164 of _Proceedings of Machine Learning Research_ , pp. 894–906. PMLR, 08–11 Nov 2022. URL https://proceedings. mlr.press/v164/shridhar22a.html. 

- Shridhar, M., Manuelli, L., and Fox, D. Perceiver-actor: A multi-task transformer for robotic manipulation. In _Conference on Robot Learning_ , pp. 785–799. PMLR, 2023. 

- Shu, D., Zhao, H., Hu, J., Liu, W., Payani, A., Cheng, L., and Du, M. Large vision-language model alignment and misalignment: A survey through the lens of explainability. _arXiv preprint arXiv:2501.01346_ , 2025. 

- Song, W., Zhou, Z., Zhao, H., Chen, J., Ding, P., Yan, H., Huang, Y., Tang, F., Wang, D., and Li, H. Reconvla: Reconstructive vision-language-action model as effective robot perceiver. _arXiv preprint arXiv:2508.10333_ , 2025. 

- Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Tian, Y., Yang, S., Zeng, J., Wang, P., Lin, D., Dong, H., and Pang, J. Predictive inverse dynamics models are scalable learners for robotic manipulation. _arXiv preprint arXiv:2412.15109_ , 2024. 

- Wang, L., Chen, X., Zhao, J., and He, K. Scaling proprioceptive-visual learning with heterogeneous pretrained transformers. _Advances in neural information processing systems_ , 37:124420–124450, 2024. 

- Wang, Y., Ding, P., Li, L., Cui, C., Ge, Z., Tong, X., Song, W., Zhao, H., Zhao, W., Hou, P., et al. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. _arXiv preprint arXiv:2509.09372_ , 2025a. 

- Wang, Y., Li, X., Wang, W., Zhang, J., Li, Y., Chen, Y., Wang, X., and Zhang, Z. Unified vision-language-action model. _arXiv preprint arXiv:2506.19850_ , 2025b. 

- Wen, C., Lin, X., So, J., Chen, K., Dou, Q., Gao, Y., and Abbeel, P. Any-point trajectory modeling for policy learning, 2023. 

- Wu, H., Jing, Y., Cheang, C., Chen, G., Xu, J., Li, X., Liu, M., Li, H., and Kong, T. Unleashing large-scale video generative pre-training for visual robot manipulation. In _The Twelfth International Conference on Learning Representations_ , 2024. URL https://openreview. net/forum?id=NxoFmGgWC9. 

- Yang, Z., Chen, Y., Wang, J., Manivasagam, S., Ma, W.-C., Yang, A. J., and Urtasun, R. Unisim: A neural closedloop sensor simulator. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 1389–1399, 2023. 

- Ye, S., Jang, J., Jeon, B., Joo, S., Yang, J., Peng, B., Mandlekar, A., Tan, R., Chao, Y.-W., Lin, B. Y., et al. Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ , 2024. 

- Yuan, Y., Cui, H., Huang, Y., Chen, Y., Ni, F., Dong, Z., Li, P., Zheng, Y., and Hao, J. Embodied-r1: Reinforced embodied reasoning for general robotic manipulation. _arXiv preprint arXiv:2508.13998_ , 2025. 

- Zawalski, M., Chen, W., Pertsch, K., Mees, O., Finn, C., and Levine, S. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 

- Zhang, J., Guo, Y., Hu, Y., Chen, X., Zhu, X., and Chen, J. Up-vla: A unified understanding and prediction model for embodied agent. _arXiv preprint arXiv:2501.18867_ , 2025. 

- Zhang, Z., Zheng, K., Chen, Z., Jang, J., Li, Y., Han, S., Wang, C., Ding, M., Fox, D., and Yao, H. Grape: Generalizing robot policy via preference alignment. _arXiv preprint arXiv:2411.19309_ , 2024. 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action 

11 

**Submission and Formatting Instructions for ICML 2026** 

models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025. 

- Zhao, Z., Wang, B., Ouyang, L., Dong, X., Wang, J., and He, C. Beyond hallucinations: Enhancing lvlms through hallucination-aware direct preference optimization. _arXiv preprint arXiv:2311.16839_ , 2023. 

- Zheng, R., Liang, Y., Huang, S., Gao, J., Daume´ III, H., Kolobov, A., Huang, F., and Yang, J. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 

- Zholus, A., Doersch, C., Yang, Y., Koppula, S., Patraucean, V., He, X. O., Rocco, I., Sajjadi, M. S., Chandar, S., and Goroshin, R. Tapnext: Tracking any point (tap) as next token prediction. _arXiv preprint arXiv:2504.05579_ , 2025. 

- Zhou, Y., Cui, C., Rafailov, R., Finn, C., and Yao, H. Aligning modalities in vision large language models via preference fine-tuning. _arXiv preprint arXiv:2402.11411_ , 2024a. 

- Zhou, Y., Fan, Z., Cheng, D., Yang, S., Chen, Z., Cui, C., Wang, X., Li, Y., Zhang, L., and Yao, H. Calibrated self-rewarding vision language models. _Advances in Neural Information Processing Systems_ , 37:51503–51531, 2024b. 

- Zhou, Z., Zhu, Y., Zhu, M., Wen, J., Liu, N., Xu, Z., Meng, W., Peng, Y., Shen, C., Feng, F., et al. Chatvla: Unified multimodal understanding and robot control with vision-language-action model. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , pp. 5377–5395, 2025. 

12 

**Submission and Formatting Instructions for ICML 2026** 

# **A. Additional Implementation Details** 

## **A.1. Visual Track Generation Details** 

This section provides additional details on visual track generation. We adopt different strategies for LIBERO and CALVIN benchmarks. For LIBERO, we follow the protocol in TraceVLA (Zheng et al., 2024) to track over overlapping video segments. Specifically, each demonstration is divided into overlapping segments of 32 size (e.g. [1, 32], [17, 48], etc). For each segment, we initialize _N_ = 900 tracking points in the first frame of the segment and track their coordinates throughout the entire 32-frame window. With this design, any track whose starting frame falls within the first 16 frames of a segment is guaranteed to have a future trajectory of at least 16 frames. This design also enables the inclusion of newly visible regions and increases diversity of visual tracks across segments. For Calvin, since each language-annotated demonstration has a maximum length of 64 frames, we directly track the initialized points over the entire trajectory without further segmentation. 

To btain valid and active visual tracks, we apply several filtering criteria. First, we remove static points by calculating frame-to-frame pixel displacement over the tracking interval (32 frames for LIBERO and up to 64 frames for CALVIN). Points with an average displacement below 2 pixels are discarded. Next, we remove points that exhibit insufficient temporal motion consistency, defined as having displacements greater than 2 pixels in fewer than one quarter of the tracked frames. Finally, we discard points that exhibit abrupt motion, specifically those with a displacement exceeding 10 pixels between any pair of consecutive frames. This filtering strategy effectively removes false-positive tracks, particularly those with spurious jumps. 

We provide qualitative demonstrations of the annotated visual tracks in Figure 6 (LIBERO) and Figure 7 (CALVIN). 


_Figure 6._ **Track annotation results on LIBERO dataset** . Top: LIBERO-Spatial; Bottom: LIBERO-Long. _Best viewed when zoomed in!_ 


_Figure 7._ **Track annotation results on CALVIN dataset** . We select 4 sequences for visualization. _Best viewed when zoomed in!_ 

## **A.2. VLA Prompt** 

Given a task such as: 

**[TASK]** _pick up the black bowl between the plate and the ramekin and place it on the plate_ 

The instruction-following prompt _g_ and track-following prompt ˜ _g_ are: 

13 

**Submission and Formatting Instructions for ICML 2026** 

**[Instruction-following Prompt]** _What 8 step actions should the robot take to [TASK]_ **[Track-following Prompt]** _The visual trajectory depicts a way to [TASK]. What 8 step actions should the robot take to follow it?_ 

## **A.3. Training Configuration Details** 

**VISTA training configurations** We show VISTA training configurations for all experiments in Table 3. 

|**Experi**|**ment**|**Optimizer **|**Scheduler **|<sup>**LoRA**</sup><br>**Rank**|**Global**<br>**Batch Size**|**GPU**<sup>_†_</sup><br>**Count**|**Learning**<br>**Rate**|**Total**<br>**Steps/Epochs**|
|---|---|---|---|---|---|---|---|---|
||Stage 0|Adam|Constant|32|128|8|5e-4|60K Steps (others)<br>80K Steps(Long)|
|LIBERO|Stage 1|Adam|Constant|32|16|4|1e-5|60K Steps|
||Stage 2|Adam|Constant|32|96|8|5e-4|20K Steps (Spatial, Goal)<br>30K Steps (Object, Long)|
||Stage 0|Adam|Constant|32|128|8|5e-4|200K Steps|
|CALVIN|Stage 1|Adam|Constant|32|48|8|1e-5|5 Epochs|
||Stage 2|Adam|Constant|32|96 (VISTA)<br>64 (VISTA-OFT)|8|5e-4|12 Epochs (VISTA)<br>6 Epochs (VISTA-OFT)|


_Table 3._ **VISTA Training Configurations** .<sup>_†_</sup> We use NVIDIA A100 for all of our training experiments. 

**Baseline OpenVLA/OpenVLA-OFT reproduction details** For 8-Step OpenVLA (Kim et al., 2024), we use the VISTA Stage 1 model in all experiments since they are equivalent. For OpenVLA-OFT (Kim et al., 2025), which is also 8-step, we tabulate the LIBERO results directly from the original paper. For CALVIN, we train OpenVLA-OFT for 6 epochs with global batch size of 64. We observe that _OpenVLA-OFT does not benefit from longer training_ . When increasing the training epochs from 6 to 12, OpenVLA-OFT performance in CALVIN ABC _→_ D drops from 3.868 to 3.861. 

**Alternative training strategies details.** Here we summarize the training details of the alternative approaches shown in Figure 5 (B). For DPO-then-SFT, we follow the same configuration as VISTA in LIBERO-Spatial. For Co-SFT, we train the model for 100K steps, which is 40K steps more than the OpenVLA to accommodate the auxiliary task and additional training data. 

# **B. Additional Results** 

## **B.1. LIBERO Results without Receding Horizon Control** 

|Methods|Plan-Execute<br>Horizon|Spatial|Object|Goal|Long|Mean|
|---|---|---|---|---|---|---|
|OenVLA|8-8|73|84.2|72|52.8|70.5|
|p|8-4|79.6|88.6|82.4|54.4|76.3|
||8-8|75.8|87.6|81.4|49.4|**73.5**|
|VISTA||(+2.8)|(+3.4)|(+9.4)|(-3.4)|(+3)|
||8-4|84.8|91.6|84.2|57.0|**79.4**|
|||(+5.2)|(+3.0)|(+1.8)|(+2.6)|(+3.1)|


_Table 4._ **LIBERO Results without Receding Horizon Control.** Green (red) numbers indicate performance gains (drops) relative to the OpenVLA counterpart. 

We show the performance of OpenVLA and VISTA with and without the Receding Horizon Control (RHC) in Table 4. In both settings, VISTA improves OpenVLA by at least 3% in success rate, which futher proves the effectiveness of our approach. In addition, removing RHC leads to a performance drop for both VISTA and OpenVLA in LIBERO. This degradation is potentially due to the declining visual conditioning when predicting later action tokens as illusrated in Figure 2, which suggests that the later tokens are less reliable. In that regime, action prediction becomes more dominated by the 

14 

**Submission and Formatting Instructions for ICML 2026** 

action distribution prior learnt from the dataset, which makes them less grounded on the world observations. However, we do not observe performance gain by adding RHC in CALVIN. A plausible explanation is that the CALVIN training dataset is substantially larger than LIBERO, which may mitigate overfitting to action priors and support more stable long-horizon action prediction. 

## **B.2. Visual conditioning in other LIBERO suites** 

In addition to Figure 2, we illustrate our quantified visual conditioning of OpenVLA and VISTA model in the remaining LIBERO suites in Figure 8 following the protocol in Sec. 3.2. We make two observations from the plots. First, the successful trials of OpenVLA constantly feature stronger visual grounding compared to failure ones across all suites, which further support our claim on the importance of visual clue utilization to the performance of VLA. Second, VISTA improves the visual conditioning of all action tokens in LIBERO-Goal as in LIBERO-Spatial. As for LIBERO-Object and LIBERO-Long, although the visual conditioning is not improved in the prediction of later tokens, it is enhanced to the level of the average successful OpenVLA rollouts at the early stage of the prediction as highlighed by the goal bounding box. Coupled with Receding Horizon Control (RHC), the performance is improved as presented in Table 2. However, the inability to raise visual conditioning at the later stage might explain the degraded performance of VISTA without RHC in Table 4, which is left for future work. 


_Figure 8._ **Visual Conditioning of VISTA and OpenVLA in more LIBERO Suites** . Left: LIBERO-Goal; Middle: LIBERO-Object; Right: LIBERO-Long. 

## **B.3. Ablation on the Distillation Loss Weight** 

We ablate on the distillation loss weight _γ_ on LIBERO-Spatial. We experiment on _γ ∈_ [0 _._ 01 _,_ 0 _._ 1 _,_ 1] in VISTA Stage 3 training, where all training configurations are the same as the ones tabulated in Table 3, except that we reduce the global batch size from 96 to 48 to reduce the required GPU from 8 to 4 to save compute. We also evaluate on 200 trails instead of 500 as in the main paper. As shown in Table 5, althought VISTA with all _γ_ outperforms OpenVLA (presented in Table 4), _γ_ = 0 _._ 1 achieves the best result. Hence we fix _γ_ = 0 _._ 1 in all main experiments. 

|Plan-Execute||_γ_||
|---|---|---|---|
|Horizon|0.01|0.1<br>|1|
|8-8|72|**76**|73|
|8-4|81.5|**86**|85|


_Table 5._ **LIBERO-Spatial Success Rate (%) under Different Distillation Loss Weight** _γ_ **.** 

15 

